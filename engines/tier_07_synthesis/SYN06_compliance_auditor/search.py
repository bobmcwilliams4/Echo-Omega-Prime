import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id: int, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self.idf_cache: Dict[str, float] = {}
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in set(tokens):
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            score *= doc.weight
            if score > 0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        return {
            "num_documents": self.N,
            "avg_doc_length": int(self.avg_doc_length),
            "unique_terms": len(self.doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if t]

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs.get(doc_id, {})
        for term in set(query_terms):
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs.get(doc_id, {})
        doc_len = self.doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in set(query_terms):
            term_tf = tf.get(term, 0) / doc_len
            idf = self._compute_idf(term)
            score += term_tf * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return " ".join(tokens[:window]) + "..."
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({term})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

    def preseed(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1,
                "COSO Internal Control Framework Overview",
                "The COSO Internal Control Framework provides a comprehensive basis for designing, implementing, and evaluating effective internal controls. It is structured around five components: Control Environment, Risk Assessment, Control Activities, Information & Communication, and Monitoring Activities.",
                ["COSO", "Internal Control", "Framework", "Components"],
                1.0
            ),
            SearchDocument(
                2,
                "Three Lines of Defense Model Explained",
                "The Three Lines of Defense Model defines roles and responsibilities for risk management and control: operational management (first line), risk and compliance functions (second line), and internal audit (third line).",
                ["Three Lines of Defense", "Risk Management", "Internal Audit"],
                1.0
            ),
            SearchDocument(
                3,
                "Risk-Based Audit Planning Methodology",
                "Risk-based audit planning involves identifying and prioritizing audit areas based on risk assessments. This ensures audit resources are focused on areas of highest risk and impact.",
                ["Audit Planning", "Risk Assessment", "Methodology"],
                1.0
            ),
            SearchDocument(
                4,
                "Control Testing: Sampling and Evidence",
                "Effective control testing requires appropriate sampling methods and sufficient, relevant evidence. Sampling techniques include random, judgmental, and stratified sampling.",
                ["Control Testing", "Sampling", "Evidence"],
                1.0
            ),
            SearchDocument(
                5,
                "IIA International Standards for Professional Practice",
                "The Institute of Internal Auditors (IIA) sets standards for the professional practice of internal auditing, including independence, objectivity, and proficiency.",
                ["IIA", "Standards", "Internal Audit"],
                1.0
            ),
            SearchDocument(
                6,
                "DOJ Evaluation of Corporate Compliance Programs",
                "The U.S. Department of Justice evaluates corporate compliance programs based on design, implementation, and effectiveness, focusing on risk assessment, policies, training, and investigations.",
                ["DOJ", "Compliance", "Evaluation"],
                1.0
            ),
            SearchDocument(
                7,
                "Federal Sentencing Guidelines for Organizations",
                "The Federal Sentencing Guidelines for Organizations (FSGO) provide criteria for effective compliance and ethics programs, influencing penalty mitigation.",
                ["FSGO", "Compliance", "Ethics"],
                1.0
            ),
            SearchDocument(
                8,
                "Gap Analysis Methodology",
                "Gap analysis identifies differences between current and desired states, enabling organizations to prioritize remediation and improvement actions.",
                ["Gap Analysis", "Remediation", "Improvement"],
                1.0
            ),
            SearchDocument(
                9,
                "Regulatory Change Management and Horizon Scanning",
                "Regulatory change management involves monitoring, assessing, and implementing regulatory requirements. Horizon scanning anticipates emerging risks and regulations.",
                ["Regulatory Change", "Horizon Scanning", "Compliance"],
                1.0
            ),
            SearchDocument(
                10,
                "Audit Workpaper Standards and Documentation",
                "Audit workpapers must be accurate, complete, and support audit conclusions. Documentation standards ensure consistency and facilitate review.",
                ["Audit Workpapers", "Documentation", "Standards"],
                1.0
            ),
            SearchDocument(
                11,
                "Finding Classification: Critical, Major, Minor, Observation",
                "Audit findings are classified as critical, major, minor, or observations based on severity and impact on the organization.",
                ["Findings", "Classification", "Severity"],
                1.0
            ),
            SearchDocument(
                12,
                "Corrective Action Plan (CAP) Development and Tracking",
                "A Corrective Action Plan (CAP) outlines steps to address audit findings. Tracking CAPs ensures timely remediation and accountability.",
                ["CAP", "Corrective Action", "Tracking"],
                1.0
            ),
            SearchDocument(
                13,
                "Regulatory Exam Preparation and Response",
                "Preparing for regulatory exams involves organizing documentation, conducting self-assessments, and coordinating responses to examiner requests.",
                ["Regulatory Exam", "Preparation", "Response"],
                1.0
            ),
            SearchDocument(
                14,
                "Compliance Calendar and Periodic Deliverables Tracking",
                "A compliance calendar tracks periodic deliverables and deadlines, supporting timely compliance with regulatory requirements.",
                ["Compliance Calendar", "Deliverables", "Tracking"],
                1.0
            ),
            SearchDocument(
                15,
                "Control Environment: Foundation of Internal Control",
                "The control environment sets the tone for the organization, influencing the control consciousness of its people and forming the foundation for all other components.",
                ["Control Environment", "COSO", "Foundation"],
                1.0
            ),
            SearchDocument(
                16,
                "Risk Assessment in Internal Control",
                "Risk assessment involves identifying and analyzing risks to achieving objectives, forming a basis for determining control activities.",
                ["Risk Assessment", "Internal Control"],
                1.0
            ),
            SearchDocument(
                17,
                "Control Activities: Policies and Procedures",
                "Control activities are the policies and procedures that help ensure management directives are carried out.",
                ["Control Activities", "Policies", "Procedures"],
                1.0
            ),
            SearchDocument(
                18,
                "Information & Communication in COSO",
                "Effective information and communication systems support the identification, capture, and exchange of information in a timely and useful manner.",
                ["Information", "Communication", "COSO"],
                1.0
            ),
            SearchDocument(
                19,
                "Monitoring Activities in Internal Control",
                "Monitoring activities assess the quality of internal control performance over time and ensure controls continue to operate effectively.",
                ["Monitoring", "Internal Control"],
                1.0
            ),
            SearchDocument(
                20,
                "Role of Internal Audit in the Third Line of Defense",
                "Internal audit provides independent assurance on the effectiveness of governance, risk management, and control processes.",
                ["Internal Audit", "Third Line", "Assurance"],
                1.0
            ),
            SearchDocument(
                21,
                "Audit Universe and Risk Ranking",
                "An audit universe is a comprehensive list of all auditable entities, which are risk-ranked to prioritize audit coverage.",
                ["Audit Universe", "Risk Ranking"],
                1.0
            ),
            SearchDocument(
                22,
                "Sampling Techniques in Control Testing",
                "Sampling techniques such as statistical and non-statistical sampling are used to select items for control testing.",
                ["Sampling", "Control Testing"],
                1.0
            ),
            SearchDocument(
                23,
                "Evidence Types in Audit",
                "Audit evidence includes physical, documentary, analytical, and testimonial evidence to support audit findings.",
                ["Audit Evidence", "Types"],
                1.0
            ),
            SearchDocument(
                24,
                "IIA Code of Ethics",
                "The IIA Code of Ethics promotes integrity, objectivity, confidentiality, and competency in internal auditing.",
                ["IIA", "Code of Ethics"],
                1.0
            ),
            SearchDocument(
                25,
                "Remediation Tracking and Escalation",
                "Remediation tracking ensures that corrective actions are implemented and escalated when deadlines are missed.",
                ["Remediation", "Tracking", "Escalation"],
                1.0
            ),
            SearchDocument(
                26,
                "Key Elements of a Compliance Program",
                "A compliance program includes policies, procedures, training, monitoring, and reporting mechanisms to ensure adherence to laws and regulations.",
                ["Compliance Program", "Policies", "Training"],
                1.0
            ),
            SearchDocument(
                27,
                "Horizon Scanning: Anticipating Regulatory Change",
                "Horizon scanning is the process of identifying emerging risks and regulatory changes that may impact the organization.",
                ["Horizon Scanning", "Regulatory Change"],
                1.0
            ),
            SearchDocument(
                28,
                "Audit Documentation Best Practices",
                "Best practices for audit documentation include clarity, completeness, and timely preparation to support audit conclusions.",
                ["Audit Documentation", "Best Practices"],
                1.0
            ),
            SearchDocument(
                29,
                "Classification of Audit Findings",
                "Audit findings are classified to prioritize remediation efforts and communicate risk to stakeholders.",
                ["Audit Findings", "Classification"],
                1.0
            ),
            SearchDocument(
                30,
                "Developing Effective Corrective Action Plans",
                "Effective CAPs address root causes, assign accountability, and include timelines for remediation.",
                ["Corrective Action Plan", "CAP", "Remediation"],
                1.0
            ),
            SearchDocument(
                31,
                "Tracking Compliance Deliverables",
                "Tracking compliance deliverables ensures that all regulatory submissions and periodic requirements are met on time.",
                ["Compliance", "Deliverables", "Tracking"],
                1.0
            ),
            SearchDocument(
                32,
                "Responding to Regulatory Examinations",
                "Effective response to regulatory examinations involves prompt, accurate, and complete information provision.",
                ["Regulatory Examination", "Response"],
                1.0
            ),
            SearchDocument(
                33,
                "Internal Audit Workpaper Retention",
                "Workpaper retention policies ensure audit documentation is available for review and regulatory requirements are met.",
                ["Workpaper Retention", "Audit Documentation"],
                1.0
            ),
            SearchDocument(
                34,
                "Audit Finding Severity and Impact Assessment",
                "Severity and impact assessment of audit findings guide management response and remediation prioritization.",
                ["Audit Finding", "Severity", "Impact"],
                1.0
            ),
            SearchDocument(
                35,
                "Periodic Compliance Reporting",
                "Periodic compliance reporting provides management and regulators with updates on compliance status and outstanding issues.",
                ["Compliance Reporting", "Periodic", "Regulators"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

_search_index_singleton: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_singleton
    with _search_index_lock:
        if _search_index_singleton is None:
            idx = SearchIndex()
            idx.preseed()
            _search_index_singleton = idx
        return _search_index_singleton