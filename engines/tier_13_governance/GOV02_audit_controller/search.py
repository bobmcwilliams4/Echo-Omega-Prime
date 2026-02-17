import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id: str, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[str, int] = {}
        self.tags_index: Dict[str, set] = defaultdict(set)
        self.N = 0
        self.avgdl = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = dict(tf)
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            for tag in doc.tags:
                self.tags_index[tag.lower()].add(doc.id)
            self.documents[doc.id] = doc
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores = defaultdict(float)
        doc_snippets = {}
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            if final_score > 0:
                scores[doc_id] = final_score * doc.weight
                doc_snippets[doc_id] = self._make_snippet(doc, query_terms)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = doc_snippets.get(doc_id, "")
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        return {
            "documents": self.N,
            "unique_terms": len(self.doc_freqs),
            "average_doc_length": int(self.avgdl),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / (self.avgdl + 1e-9))
            numer = tf * (self.k1 + 1)
            score += idf * numer / denom
        return score

    def _score_tfidf(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        tf_norm = lambda tf: tf / doc_len
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            score += tf_norm(tf) * idf
        return score

    def _make_snippet(self, doc: SearchDocument, terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            snippet = content[:window*2] + "..." if len(content) > window*2 else content
            return snippet
        start = max(0, min(positions) - window)
        end = min(len(content), max(positions) + window)
        snippet = content[start:end]
        for term in terms:
            snippet = re.sub(f"({re.escape(term)})", r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ("..." if end < len(content) else "")

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Public Policy Analysis",
            content="Public policy analysis involves evaluating government policies and their impacts on society. Key methods include cost-benefit analysis, stakeholder engagement, and evidence-based decision making.",
            tags=["policy", "analysis", "governance"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Government Audit Standards",
            content="Government audits are conducted according to established standards such as the Yellow Book. These standards ensure accountability, transparency, and integrity in public sector auditing.",
            tags=["audit", "standards", "accountability"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Risk Management in the Public Sector",
            content="Risk management frameworks help government agencies identify, assess, and mitigate risks. Effective risk management supports better resource allocation and program outcomes.",
            tags=["risk", "management", "public sector"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Ethics in Government Operations",
            content="Ethical conduct is fundamental in government. Codes of ethics guide public servants in decision making, conflict of interest management, and maintaining public trust.",
            tags=["ethics", "government", "integrity"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Budgeting and Financial Control",
            content="Public budgeting involves planning, allocating, and controlling financial resources. Techniques include zero-based budgeting, performance budgeting, and fiscal discipline.",
            tags=["budget", "finance", "control"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Performance Measurement in Government",
            content="Performance measurement systems track the efficiency and effectiveness of government programs. Key performance indicators (KPIs) and benchmarking are common tools.",
            tags=["performance", "measurement", "KPIs"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Transparency and Open Government",
            content="Open government initiatives promote transparency, citizen participation, and access to information. Open data portals and freedom of information laws are essential components.",
            tags=["transparency", "open government", "citizen"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Internal Controls in Public Administration",
            content="Internal controls are processes designed to ensure reliable financial reporting, compliance, and operational effectiveness in government agencies.",
            tags=["internal controls", "compliance", "administration"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Fraud Detection and Prevention",
            content="Fraud detection in government uses data analytics, whistleblower systems, and regular audits to prevent and identify fraudulent activities.",
            tags=["fraud", "detection", "prevention"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Procurement and Contract Management",
            content="Government procurement must follow principles of fairness, transparency, and value for money. Contract management ensures suppliers meet obligations.",
            tags=["procurement", "contract", "management"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Public Sector Governance Models",
            content="Governance models define the structures and processes for directing and controlling public organizations, including roles, responsibilities, and accountability mechanisms.",
            tags=["governance", "models", "public sector"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Audit Committees and Oversight",
            content="Audit committees provide independent oversight of government financial reporting, risk management, and internal controls.",
            tags=["audit", "committee", "oversight"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Regulatory Compliance in Government",
            content="Compliance with laws and regulations is critical for government agencies. Compliance programs include training, monitoring, and enforcement mechanisms.",
            tags=["compliance", "regulation", "government"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Information Security in the Public Sector",
            content="Protecting sensitive government information requires robust security policies, access controls, and incident response plans.",
            tags=["information security", "public sector", "policy"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Data Analytics for Government Audits",
            content="Data analytics enhances audit effectiveness by identifying anomalies, trends, and risks in large datasets.",
            tags=["data analytics", "audit", "government"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Public Expenditure Review",
            content="Expenditure reviews assess the efficiency and effectiveness of government spending, identifying opportunities for savings and improved outcomes.",
            tags=["expenditure", "review", "public spending"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Change Management in Public Organizations",
            content="Change management strategies help public organizations adapt to reforms, new technologies, and evolving stakeholder expectations.",
            tags=["change management", "public organizations", "reform"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Citizen Engagement in Policy Making",
            content="Engaging citizens in policy making improves legitimacy, responsiveness, and the quality of government decisions.",
            tags=["citizen engagement", "policy", "participation"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Public Sector Innovation",
            content="Innovation in the public sector includes adopting new technologies, processes, and service delivery models to improve outcomes.",
            tags=["innovation", "public sector", "technology"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Government Accountability Mechanisms",
            content="Accountability mechanisms such as audits, ombudsmen, and parliamentary committees ensure government actions are transparent and responsible.",
            tags=["accountability", "mechanisms", "government"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Strategic Planning in Government Agencies",
            content="Strategic planning aligns agency resources with mission objectives, guiding long-term priorities and performance measurement.",
            tags=["strategic planning", "government", "agency"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Financial Reporting in the Public Sector",
            content="Accurate financial reporting supports transparency and informed decision making in government finance.",
            tags=["financial reporting", "public sector", "finance"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Audit Evidence and Documentation",
            content="Collecting sufficient and appropriate audit evidence is essential for forming audit opinions and supporting findings.",
            tags=["audit", "evidence", "documentation"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Public Service Delivery Improvement",
            content="Improving public service delivery involves process optimization, technology adoption, and customer-centric approaches.",
            tags=["service delivery", "improvement", "public service"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Internal Audit Function in Government",
            content="The internal audit function provides assurance on risk management, control, and governance processes in government entities.",
            tags=["internal audit", "government", "assurance"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Legal Frameworks for Government Auditing",
            content="Legal frameworks establish the authority, independence, and scope of government audit institutions.",
            tags=["legal", "framework", "audit"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Public Sector Human Resource Management",
            content="Effective HR management in the public sector ensures recruitment, retention, and development of skilled personnel.",
            tags=["human resources", "public sector", "management"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Sustainability Reporting in Government",
            content="Sustainability reporting discloses government actions on environmental, social, and governance (ESG) issues.",
            tags=["sustainability", "reporting", "ESG"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Audit Sampling Techniques",
            content="Audit sampling enables auditors to draw conclusions about populations based on representative samples.",
            tags=["audit", "sampling", "techniques"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Public Sector Project Management",
            content="Project management in the public sector addresses unique challenges such as regulatory compliance, stakeholder engagement, and public accountability.",
            tags=["project management", "public sector", "stakeholder"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)