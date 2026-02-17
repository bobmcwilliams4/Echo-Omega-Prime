import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
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
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.idf_cache: Dict[str, float] = {}
        self.N = 0
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old doc data
                old_terms = self.doc_term_freqs.get(doc.id, {})
                for term in old_terms:
                    if doc.id in self.inverted_index[term]:
                        del self.inverted_index[term][doc.id]
                del self.doc_term_freqs[doc.id]
                del self.doc_lengths[doc.id]
                del self.documents[doc.id]
                self.N -= 1

            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            term_freqs = Counter(tokens)
            doc_length = sum(term_freqs.values())
            self.documents[doc.id] = doc
            self.doc_term_freqs[doc.id] = term_freqs
            self.doc_lengths[doc.id] = doc_length
            self.N += 1

            for term, freq in term_freqs.items():
                self.inverted_index[term][doc.id] = freq

            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        scores: Dict[str, float] = defaultdict(float)
        idf_vals = {term: self._compute_idf(term) for term in query_terms}

        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())

        for doc_id in candidate_docs:
            score = self._score_bm25(doc_id, query_terms, idf_vals)
            if score > 0:
                scores[doc_id] = score * self.documents[doc_id].weight

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'num_terms': len(self.inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str], idf_vals: Dict[str, float]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        term_freqs = self.doc_term_freqs.get(doc_id, Counter())
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            idf = idf_vals.get(term, 0.0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length) if self.avg_doc_length > 0 else 1
            score += idf * (numerator / denominator)
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_length: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            for match in re.finditer(r'\b' + re.escape(term) + r'\b', content_lower):
                positions.append(match.start())
        if not positions:
            snippet = content[:snippet_length].strip()
            if len(content) > snippet_length:
                snippet += '...'
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_length // 4, 0)
        end_pos = start_pos + snippet_length
        if end_pos > len(content):
            end_pos = len(content)
            start_pos = max(end_pos - snippet_length, 0)
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = '...' + snippet
        if end_pos < len(content):
            snippet = snippet + '...'
        return snippet

_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _preseed_index(_singleton_instance)
        return _singleton_instance

def _preseed_index(index: SearchIndex):
    docs = [
        SearchDocument(
            "doc001",
            "Succession Planning Fundamentals",
            "Succession planning fundamentals involve identifying and developing new leaders to replace old leaders when they leave, retire or die.",
            ["succession_planning_fundamentals", "family_governance", "legacy_preservation"],
            1.2
        ),
        SearchDocument(
            "doc002",
            "Power Transfer Protocols",
            "Power transfer protocols define the formal processes and ceremonies involved in transferring authority within a dynasty or corporation.",
            ["power_transfer_protocols", "corporate_succession", "dynasty_continuity"],
            1.1
        ),
        SearchDocument(
            "doc003",
            "Dynasty Continuity Strategies",
            "Maintaining dynasty continuity requires careful planning, heir validation, and competency assessment to ensure leadership stability.",
            ["dynasty_continuity", "heir_validation", "competency_assessment"],
            1.3
        ),
        SearchDocument(
            "doc004",
            "Heir Validation Procedures",
            "Heir validation involves verifying the legitimacy, capability, and readiness of successors to assume leadership roles.",
            ["heir_validation", "competency_assessment", "trust_succession"],
            1.1
        ),
        SearchDocument(
            "doc005",
            "Competency Assessment in Succession",
            "Competency assessment evaluates the skills and qualifications of potential heirs to ensure they meet leadership requirements.",
            ["competency_assessment", "succession_training", "succession_review"],
            1.0
        ),
        SearchDocument(
            "doc006",
            "Emergency Succession Planning",
            "Emergency succession plans prepare organizations for unexpected leadership vacancies to maintain operational continuity.",
            ["emergency_succession", "succession_timeline", "stakeholder_management"],
            1.4
        ),
        SearchDocument(
            "doc007",
            "Regent Designation Protocols",
            "Regent designation protocols establish temporary leadership arrangements during transitions or incapacitations.",
            ["regent_designation", "power_transfer_protocols", "family_governance"],
            1.0
        ),
        SearchDocument(
            "doc008",
            "Trust Succession Mechanisms",
            "Trust succession mechanisms use legal trusts to manage the transfer of assets and authority within families or corporations.",
            ["trust_succession", "legacy_preservation", "succession_documentation"],
            1.2
        ),
        SearchDocument(
            "doc009",
            "Corporate Succession Planning",
            "Corporate succession planning ensures smooth leadership transitions to sustain company performance and shareholder value.",
            ["corporate_succession", "stakeholder_management", "succession_metrics"],
            1.3
        ),
        SearchDocument(
            "doc010",
            "Family Governance and Succession",
            "Family governance frameworks support succession by defining roles, responsibilities, and decision-making processes.",
            ["family_governance", "succession_communication", "stakeholder_management"],
            1.1
        ),
        SearchDocument(
            "doc011",
            "Succession Timeline Management",
            "Managing the succession timeline involves scheduling key milestones to prepare successors effectively.",
            ["succession_timeline", "succession_training", "succession_review"],
            1.0
        ),
        SearchDocument(
            "doc012",
            "Parallel Succession Tracks",
            "Parallel succession tracks allow multiple potential successors to be developed simultaneously to mitigate risks.",
            ["parallel_succession_tracks", "competency_assessment", "succession_metrics"],
            1.2
        ),
        SearchDocument(
            "doc013",
            "Contested Succession Resolution",
            "Contested succession requires conflict resolution strategies to handle disputes among heirs or stakeholders.",
            ["contested_succession", "stakeholder_management", "succession_communication"],
            1.3
        ),
        SearchDocument(
            "doc014",
            "Succession Documentation Standards",
            "Succession documentation standards ensure all plans, agreements, and protocols are clearly recorded and accessible.",
            ["succession_documentation", "trust_succession", "legacy_preservation"],
            1.0
        ),
        SearchDocument(
            "doc015",
            "Succession Training Programs",
            "Succession training programs develop the skills and knowledge of future leaders through structured learning.",
            ["succession_training", "competency_assessment", "succession_review"],
            1.1
        ),
        SearchDocument(
            "doc016",
            "Legacy Preservation Techniques",
            "Legacy preservation techniques protect family or corporate heritage during leadership transitions.",
            ["legacy_preservation", "family_governance", "trust_succession"],
            1.2
        ),
        SearchDocument(
            "doc017",
            "Succession Communication Strategies",
            "Effective succession communication strategies ensure transparency and stakeholder alignment during transitions.",
            ["succession_communication", "stakeholder_management", "contested_succession"],
            1.0
        ),
        SearchDocument(
            "doc018",
            "Stakeholder Management in Succession",
            "Managing stakeholders during succession involves balancing interests and maintaining trust throughout the process.",
            ["stakeholder_management", "succession_communication", "corporate_succession"],
            1.3
        ),
        SearchDocument(
            "doc019",
            "Succession Metrics and KPIs",
            "Succession metrics and KPIs measure the effectiveness and readiness of succession plans and candidates.",
            ["succession_metrics", "competency_assessment", "succession_review"],
            1.1
        ),
        SearchDocument(
            "doc020",
            "Succession Review Processes",
            "Regular succession review processes update plans and assess progress to adapt to changing conditions.",
            ["succession_review", "succession_training", "succession_timeline"],
            1.0
        ),
        SearchDocument(
            "doc021",
            "Heir Competency Development",
            "Focused development programs enhance heir competencies to meet future leadership challenges.",
            ["heir_validation", "succession_training", "competency_assessment"],
            1.2
        ),
        SearchDocument(
            "doc022",
            "Emergency Regent Appointment",
            "Emergency regent appointment protocols ensure immediate leadership coverage during crises.",
            ["emergency_succession", "regent_designation", "power_transfer_protocols"],
            1.1
        ),
        SearchDocument(
            "doc023",
            "Trust-Based Succession Planning",
            "Trust-based succession planning integrates fiduciary responsibilities with leadership transition strategies.",
            ["trust_succession", "legacy_preservation", "succession_documentation"],
            1.2
        ),
        SearchDocument(
            "doc024",
            "Corporate Heir Grooming",
            "Corporate heir grooming focuses on preparing successors for executive roles through mentorship and training.",
            ["corporate_succession", "succession_training", "stakeholder_management"],
            1.3
        ),
        SearchDocument(
            "doc025",
            "Managing Parallel Succession Risks",
            "Managing risks in parallel succession tracks involves monitoring and adjusting development paths.",
            ["parallel_succession_tracks", "succession_metrics", "contested_succession"],
            1.0
        ),
        SearchDocument(
            "doc026",
            "Succession Conflict Mediation",
            "Mediation techniques resolve conflicts arising from contested succession scenarios.",
            ["contested_succession", "succession_communication", "stakeholder_management"],
            1.1
        ),
        SearchDocument(
            "doc027",
            "Succession Plan Legal Framework",
            "Legal frameworks underpinning succession plans ensure enforceability and compliance.",
            ["succession_documentation", "trust_succession", "corporate_succession"],
            1.0
        ),
        SearchDocument(
            "doc028",
            "Succession Training Curriculum Design",
            "Designing effective succession training curricula aligns learning objectives with leadership competencies.",
            ["succession_training", "competency_assessment", "succession_review"],
            1.2
        ),
        SearchDocument(
            "doc029",
            "Preserving Family Legacy Through Succession",
            "Succession strategies that emphasize preserving family legacy strengthen long-term dynasty stability.",
            ["legacy_preservation", "family_governance", "succession_planning_fundamentals"],
            1.3
        ),
        SearchDocument(
            "doc030",
            "Succession Communication Best Practices",
            "Best practices in succession communication foster clarity, trust, and stakeholder engagement.",
            ["succession_communication", "stakeholder_management", "succession_review"],
            1.0
        ),
    ]

    for doc in docs:
        index.add_document(doc)