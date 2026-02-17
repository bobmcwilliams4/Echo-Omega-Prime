import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)  # term -> doc_id -> freq
        self.term_df: Dict[str, int] = defaultdict(int)  # term -> document frequency
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # Avoid duplicates
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            term_freqs = Counter(tokens)
            for term, freq in term_freqs.items():
                self.term_doc_freqs[term][doc.id] = freq
                self.term_df[term] += 1
            self.total_docs += 1
            self._recompute_avg_doc_length()
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[str, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            docs_with_term = self.term_doc_freqs.get(term, {})
            for doc_id, freq in docs_with_term.items():
                doc_length = self.doc_lengths[doc_id]
                bm25_score = self._score_bm25(freq, doc_length, idf)
                tfidf_score = self._score_tfidf(term, doc_id)
                doc = self.documents[doc_id]
                total_score = doc.weight * (bm25_score + 0.3 * tfidf_score)
                doc_scores[doc_id] += total_score
        ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked_docs[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc.id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_docs": self.total_docs,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.term_df),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_df.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, freq: int, doc_length: int, idf: float) -> float:
        denom = freq + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length + 1e-6))
        score = idf * (freq * (self.k1 + 1)) / (denom + 1e-6)
        return score

    def _score_tfidf(self, term: str, doc_id: str) -> float:
        if term in self._tfidf_cache and doc_id in self._tfidf_cache[term]:
            return self._tfidf_cache[term][doc_id]
        freq = self.term_doc_freqs.get(term, {}).get(doc_id, 0)
        doc_length = self.doc_lengths.get(doc_id, 1)
        tf = freq / doc_length
        idf = self._compute_idf(term)
        score = tf * idf
        self._tfidf_cache[term][doc_id] = score
        return score

    def _recompute_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 120) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            snippet = ' '.join(tokens[:length])
        else:
            start = max(indices[0] - 10, 0)
            end = min(indices[0] + 30, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet[:length] + ('...' if len(snippet) > length else '')

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Documents (Authority Resolution Doctrine Topics) ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="1",
            title="Authority Resolution: Principles",
            content="Authority resolution is the process of determining the source, reliability, and legitimacy of information or claims within a system. It is foundational for AGI01_cortex to ensure accurate and trustworthy knowledge integration.",
            tags=["authority", "resolution", "principles"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="2",
            title="Source Trustworthiness Assessment",
            content="Evaluating the trustworthiness of sources involves analyzing provenance, reputation, consistency, and corroboration. AGI01_cortex employs multi-factor scoring to determine source reliability.",
            tags=["trustworthiness", "assessment", "source"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="3",
            title="Provenance Tracking in AGI01",
            content="Provenance tracking records the origin and transmission of information. AGI01_cortex maintains detailed provenance logs to facilitate authority resolution and auditability.",
            tags=["provenance", "tracking", "audit"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="4",
            title="Legitimacy Criteria for Claims",
            content="Legitimacy of claims is determined by evidence, logical coherence, and alignment with established doctrine. AGI01_cortex applies formal criteria to filter and rank claims.",
            tags=["legitimacy", "claims", "criteria"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="5",
            title="Multi-source Corroboration",
            content="Corroboration across independent sources increases confidence in information. AGI01_cortex cross-references data to resolve conflicting claims and establish authority.",
            tags=["corroboration", "multi-source", "confidence"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="6",
            title="Reputation Scoring Algorithms",
            content="Reputation scoring quantifies the historical reliability of sources. AGI01_cortex uses adaptive algorithms to update reputation scores based on observed accuracy and consistency.",
            tags=["reputation", "scoring", "algorithms"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="7",
            title="Authority Hierarchies",
            content="Authority hierarchies define precedence among sources. AGI01_cortex models hierarchical relationships to resolve disputes and prioritize information.",
            tags=["authority", "hierarchies", "precedence"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="8",
            title="Conflict Resolution Strategies",
            content="When sources disagree, AGI01_cortex applies conflict resolution strategies such as weighted voting, arbitration, and evidence aggregation.",
            tags=["conflict", "resolution", "strategies"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="9",
            title="Evidence Aggregation Methods",
            content="Aggregating evidence from multiple sources enhances authority resolution. AGI01_cortex implements statistical and logical aggregation methods.",
            tags=["evidence", "aggregation", "methods"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="10",
            title="Formal Verification of Claims",
            content="Formal verification ensures that claims meet rigorous standards of proof. AGI01_cortex integrates formal logic and proof systems for claim validation.",
            tags=["formal", "verification", "claims"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="11",
            title="Semantic Consistency Checks",
            content="Semantic consistency checks detect contradictions and ambiguities in information. AGI01_cortex uses semantic analysis to maintain coherence.",
            tags=["semantic", "consistency", "checks"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="12",
            title="Authority Resolution Workflow",
            content="The authority resolution workflow in AGI01_cortex involves source identification, trust assessment, evidence evaluation, and claim ranking.",
            tags=["workflow", "authority", "resolution"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="13",
            title="Audit Trails for Authority Decisions",
            content="Audit trails record the decision-making process for authority resolution. AGI01_cortex maintains transparent logs for accountability.",
            tags=["audit", "trails", "decisions"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="14",
            title="Dynamic Authority Adaptation",
            content="AGI01_cortex adapts authority resolution strategies based on changing contexts, new evidence, and evolving reputations.",
            tags=["dynamic", "adaptation", "authority"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="15",
            title="Authority Resolution in Distributed Systems",
            content="Distributed systems pose unique challenges for authority resolution. AGI01_cortex employs decentralized protocols for source verification.",
            tags=["distributed", "systems", "protocols"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="16",
            title="Uncertainty Quantification",
            content="Quantifying uncertainty is essential for authority resolution. AGI01_cortex models uncertainty using probabilistic and fuzzy logic methods.",
            tags=["uncertainty", "quantification", "probabilistic"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="17",
            title="Authority Resolution Metrics",
            content="Metrics such as precision, recall, and confidence scores are used to evaluate authority resolution performance in AGI01_cortex.",
            tags=["metrics", "precision", "recall"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="18",
            title="Human-in-the-loop Authority Resolution",
            content="AGI01_cortex supports human-in-the-loop workflows for authority resolution, allowing expert intervention and oversight.",
            tags=["human", "loop", "oversight"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="19",
            title="Authority Resolution in Knowledge Graphs",
            content="Knowledge graphs facilitate authority resolution by modeling entities, relationships, and provenance. AGI01_cortex leverages graph analytics.",
            tags=["knowledge", "graphs", "analytics"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="20",
            title="Temporal Authority Dynamics",
            content="Authority changes over time as new information emerges. AGI01_cortex tracks temporal dynamics to update authority rankings.",
            tags=["temporal", "dynamics", "authority"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="21",
            title="Authority Resolution in AGI01_cortex Architecture",
            content="AGI01_cortex architecture integrates authority resolution modules for source evaluation, claim verification, and evidence aggregation.",
            tags=["architecture", "modules", "integration"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="22",
            title="Authority Resolution: Use Cases",
            content="Use cases for authority resolution include scientific research, legal analysis, and autonomous decision-making in AGI01_cortex.",
            tags=["use", "cases", "decision-making"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="23",
            title="Authority Resolution: Challenges",
            content="Challenges include conflicting evidence, dynamic reputations, and distributed sources. AGI01_cortex addresses these with robust algorithms.",
            tags=["challenges", "conflicting", "distributed"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="24",
            title="Authority Resolution: Future Directions",
            content="Future directions involve integrating machine learning, expanding provenance tracking, and enhancing transparency in AGI01_cortex.",
            tags=["future", "directions", "transparency"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="25",
            title="Authority Resolution: Ethical Considerations",
            content="Ethical considerations include fairness, accountability, and privacy in authority resolution. AGI01_cortex incorporates ethical guidelines.",
            tags=["ethical", "considerations", "privacy"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="26",
            title="Authority Resolution: Machine Learning Integration",
            content="Machine learning models can assist in authority resolution by predicting source reliability and detecting anomalies. AGI01_cortex integrates ML pipelines.",
            tags=["machine", "learning", "integration"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="27",
            title="Authority Resolution: Transparency and Explainability",
            content="Transparency and explainability are critical for authority resolution. AGI01_cortex provides interpretable decision logs and rationale.",
            tags=["transparency", "explainability", "logs"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="28",
            title="Authority Resolution: Autonomous Agents",
            content="Autonomous agents in AGI01_cortex utilize authority resolution to make informed decisions and collaborate effectively.",
            tags=["autonomous", "agents", "collaboration"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="29",
            title="Authority Resolution: Policy Frameworks",
            content="Policy frameworks guide authority resolution processes in AGI01_cortex, ensuring compliance and consistency.",
            tags=["policy", "frameworks", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="30",
            title="Authority Resolution: Real-time Processing",
            content="Real-time processing enables AGI01_cortex to resolve authority rapidly in dynamic environments.",
            tags=["real-time", "processing", "dynamic"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)