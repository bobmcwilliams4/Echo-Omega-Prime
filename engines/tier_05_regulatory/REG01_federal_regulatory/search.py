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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[str, str], float] = {}
        self._recompute_stats()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.N += 1
            tf = Counter(tokens)
            for term, freq in tf.items():
                self.term_doc_freqs[term][doc.id] = freq
            for term in tf:
                self.doc_freqs[term] += 1
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self._recompute_stats()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores: Dict[str, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, freq in self.term_doc_freqs.get(term, {}).items():
                bm25_score = self._score_bm25(term, doc_id, freq, idf)
                tfidf_score = self._score_tfidf(term, doc_id, freq, idf)
                doc = self.documents[doc_id]
                score = bm25_score * 0.7 + tfidf_score * 0.3
                doc_scores[doc_id] += score * doc.weight
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: str, freq: int, idf: float) -> float:
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        k1 = self.bm25_k1
        b = self.bm25_b
        tf = freq
        denom = tf + k1 * (1 - b + b * doc_length / avg_dl)
        score = idf * ((tf * (k1 + 1)) / (denom + 1e-9))
        return score

    def _score_tfidf(self, term: str, doc_id: str, freq: int, idf: float) -> float:
        key = (term, doc_id)
        if key in self._tfidf_cache:
            return self._tfidf_cache[key]
        doc_length = self.doc_lengths.get(doc_id, 1)
        tf_norm = freq / doc_length
        tfidf = tf_norm * idf
        self._tfidf_cache[key] = tfidf
        return tfidf

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + '...'
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet + '...'

    def _recompute_stats(self):
        if self.N == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / max(1, self.N)

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
            title="APA Notice and Comment Rulemaking",
            content="The Administrative Procedure Act (APA) requires federal agencies to provide notice of proposed rulemaking and an opportunity for public comment before issuing substantive rules. This process ensures transparency and public participation in regulatory development.",
            tags=["APA", "notice", "comment", "rulemaking"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Chevron Deference Framework",
            content="Chevron U.S.A., Inc. v. Natural Resources Defense Council established a two-step framework for judicial review of agency interpretations of statutes. Courts first ask whether Congress has spoken directly to the precise question at issue. If not, courts defer to the agency's reasonable interpretation.",
            tags=["Chevron", "deference", "statutory interpretation"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Auer/Kisor Deference to Regulatory Interpretation",
            content="Auer deference, reaffirmed in Kisor v. Wilkie, directs courts to defer to an agency's reasonable interpretation of its own ambiguous regulations, provided the interpretation is authoritative, implicates the agency's expertise, and reflects fair and considered judgment.",
            tags=["Auer", "Kisor", "regulatory interpretation", "deference"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Major Questions Doctrine",
            content="The Major Questions Doctrine holds that courts should not defer to agency interpretations of statutes involving issues of vast economic and political significance unless Congress has spoken clearly. This doctrine limits agency authority in significant regulatory actions.",
            tags=["major questions", "doctrine", "agency authority"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Arbitrary and Capricious Review - APA Section 706",
            content="Under APA Section 706, courts must set aside agency actions found to be arbitrary, capricious, an abuse of discretion, or otherwise not in accordance with law. Agencies must provide a rational connection between the facts found and the choices made.",
            tags=["arbitrary", "capricious", "APA", "section 706"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Executive Order 12866 and OIRA Review",
            content="Executive Order 12866 requires significant regulatory actions to be reviewed by the Office of Information and Regulatory Affairs (OIRA) for cost-benefit analysis and consistency with presidential priorities. OIRA review is a key part of the regulatory process.",
            tags=["Executive Order 12866", "OIRA", "cost-benefit"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Regulatory Flexibility Act - Small Business Impact",
            content="The Regulatory Flexibility Act requires agencies to analyze the impact of proposed rules on small entities and consider less burdensome alternatives. Agencies must publish initial and final regulatory flexibility analyses.",
            tags=["Regulatory Flexibility Act", "small business", "impact"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Congressional Review Act",
            content="The Congressional Review Act allows Congress to review and potentially disapprove new federal regulations by passing a joint resolution of disapproval within a specified period after the rule is submitted.",
            tags=["Congressional Review Act", "regulation", "disapproval"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Administrative Exhaustion Requirement",
            content="Administrative exhaustion requires parties to pursue all available administrative remedies before seeking judicial review of agency action. This doctrine promotes agency expertise and efficiency.",
            tags=["administrative exhaustion", "judicial review"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Enforcement Discretion and Prosecutorial Discretion",
            content="Agencies have enforcement and prosecutorial discretion to decide whether and how to enforce laws and regulations. Courts generally do not review agency decisions not to enforce unless there is a clear abuse of discretion.",
            tags=["enforcement discretion", "prosecutorial discretion"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Consent Decrees and Settlements",
            content="Consent decrees are court-approved agreements between agencies and regulated parties to resolve disputes without admission of liability. Settlements can shape regulatory enforcement and compliance.",
            tags=["consent decrees", "settlements", "enforcement"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Preemption of State Law by Federal Regulation",
            content="Federal regulations may preempt state law under the Supremacy Clause. Preemption can be express or implied, depending on congressional intent and the scope of federal regulation.",
            tags=["preemption", "state law", "federal regulation"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="OMB Circular A-4 Cost-Benefit Analysis",
            content="OMB Circular A-4 provides guidance to federal agencies on the development of regulatory analysis, emphasizing cost-benefit analysis, risk assessment, and the consideration of alternatives.",
            tags=["OMB Circular A-4", "cost-benefit", "analysis"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Unfunded Mandates Reform Act",
            content="The Unfunded Mandates Reform Act requires agencies to assess the effects of federal mandates on state, local, and tribal governments and the private sector, and to consider less burdensome alternatives.",
            tags=["Unfunded Mandates Reform Act", "mandates", "assessment"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Paperwork Reduction Act",
            content="The Paperwork Reduction Act seeks to minimize the paperwork burden for individuals, businesses, and governments resulting from federal information collection requirements. Agencies must obtain OMB approval for information collections.",
            tags=["Paperwork Reduction Act", "paperwork", "OMB"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Federal Advisory Committee Act",
            content="The Federal Advisory Committee Act governs the establishment and operation of advisory committees in the executive branch, ensuring transparency, balanced representation, and public involvement.",
            tags=["Federal Advisory Committee Act", "advisory", "transparency"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Negotiated Rulemaking Act",
            content="The Negotiated Rulemaking Act encourages agencies to use negotiated rulemaking to develop proposed rules through consensus-based processes involving affected stakeholders.",
            tags=["Negotiated Rulemaking Act", "negotiation", "stakeholders"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Data Quality Act and Information Quality",
            content="The Data Quality Act requires federal agencies to ensure the quality, objectivity, utility, and integrity of information disseminated to the public. Agencies must establish procedures for correcting information.",
            tags=["Data Quality Act", "information quality", "correction"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Regulatory Lookback and Retrospective Review",
            content="Regulatory lookback and retrospective review involve agencies reviewing existing regulations to determine their effectiveness and consider modification or repeal of outdated or unnecessary rules.",
            tags=["regulatory lookback", "retrospective review", "modification"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Interim Final Rules and Good Cause Exception",
            content="Agencies may issue interim final rules without prior notice and comment if they find good cause that notice and comment are impracticable, unnecessary, or contrary to the public interest.",
            tags=["interim final rules", "good cause", "exception"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Direct Final Rules",
            content="Direct final rules are issued when an agency expects no significant adverse comment. If no significant adverse comment is received, the rule becomes effective without further proceedings.",
            tags=["direct final rules", "adverse comment"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Guidance Documents and Interpretive Rules",
            content="Guidance documents and interpretive rules clarify existing regulations without creating new binding requirements. They are not subject to notice and comment but must be consistent with governing statutes and regulations.",
            tags=["guidance documents", "interpretive rules", "clarification"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Scientific and Technical Rulemaking Standards",
            content="Agencies must base regulatory decisions on sound scientific and technical standards, ensuring that rules are supported by reliable data and analysis.",
            tags=["scientific standards", "technical standards", "data"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Environmental Justice in Rulemaking",
            content="Federal agencies must consider environmental justice in rulemaking, ensuring that regulations do not disproportionately impact minority and low-income communities.",
            tags=["environmental justice", "rulemaking", "communities"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Regulatory Takings and Fifth Amendment",
            content="Regulatory takings occur when government regulation limits the use of private property to such a degree that it effectively deprives the owner of economically reasonable use, raising Fifth Amendment concerns.",
            tags=["regulatory takings", "Fifth Amendment", "property"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="APA Exemptions from Rulemaking",
            content="The APA exempts certain categories of rules from notice and comment procedures, including interpretive rules, general statements of policy, and rules of agency organization, procedure, or practice.",
            tags=["APA", "exemptions", "rulemaking"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Judicial Review Standards under APA",
            content="Judicial review under the APA involves several standards, including review for substantial evidence, de novo review, and review for abuse of discretion, depending on the nature of the agency action.",
            tags=["judicial review", "APA", "standards"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Standing to Challenge Agency Rules",
            content="To challenge an agency rule, a party must demonstrate standing, including injury in fact, causation, and redressability. Standing ensures that only parties with a concrete stake may seek judicial review.",
            tags=["standing", "agency rules", "judicial review"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Recordkeeping and Transparency Requirements",
            content="Agencies must maintain administrative records supporting regulatory actions, ensuring transparency and facilitating judicial review. The record must include all materials considered by the agency.",
            tags=["recordkeeping", "transparency", "administrative record"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Public Participation in Rulemaking",
            content="Public participation is a cornerstone of the APA rulemaking process. Agencies must consider public comments and respond to significant issues raised during the comment period.",
            tags=["public participation", "rulemaking", "comments"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)