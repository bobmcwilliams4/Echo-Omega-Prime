import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Tuple

# --- Data Classes ---

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

# --- SearchIndex Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            term_counts = Counter(tokens)
            for term, count in term_counts.items():
                self.term_doc_freqs[term][doc.id] = count
                self.doc_freqs[term] += 1
            self._recompute_stats = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_doc_freqs.get(term, {}).keys())
        scored_results: List[Tuple[str, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc_weight = self.documents[doc_id].weight
            # Combine BM25 and TF-IDF (weighted sum, BM25 0.7, TF-IDF 0.3)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            final_score *= doc_weight
            scored_results.append((doc_id, final_score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            if self._recompute_stats:
                self._update_stats()
            return {
                "total_docs": self.total_docs,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove punctuation, split on whitespace
        text = text.lower()
        text = re.sub(r'[\W_]+', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        # IDF with BM25 smoothing
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        N = self.total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        with self.lock:
            if self._recompute_stats:
                self._update_stats()
            doc = self.documents[doc_id]
            tokens = self._tokenize(doc.content)
            doc_len = self.doc_lengths[doc_id]
            avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
            term_counts = Counter(tokens)
            score = 0.0
            for term in query_terms:
                tf = term_counts.get(term, 0)
                if tf == 0:
                    continue
                idf = self._compute_idf(term)
                denom = tf + k1 * (1 - b + b * doc_len / avgdl)
                score += idf * ((tf * (k1 + 1)) / denom)
            return score

    def _score_tfidf(self, doc_id: str, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        tokens = self._tokenize(doc.content)
        doc_len = self.doc_lengths[doc_id]
        term_counts = Counter(tokens)
        score = 0.0
        for term in query_terms:
            tf = term_counts.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _update_stats(self):
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.total_docs if self.total_docs > 0 else 0.0
        self.idf_cache.clear()
        self._recompute_stats = False

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = []
        for idx, token in enumerate(tokens):
            if token in query_terms:
                positions.append(idx)
        if not positions:
            snippet = ' '.join(tokens[:window])
            return snippet + ('...' if len(tokens) > window else '')
        # Take window around first occurrence
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return '...' + snippet + ('...' if end < len(tokens) else '')

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

# --- Pre-seed Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Stare Decisis: The Doctrine of Precedent",
            content="Stare decisis is the legal principle of determining points in litigation according to precedent. It ensures consistency and predictability in the law.",
            tags=["stare decisis", "precedent", "doctrine"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Binding vs Persuasive Authority Explained",
            content="Binding authority must be followed by courts, while persuasive authority may influence but does not bind. The distinction is crucial for legal analysis.",
            tags=["binding authority", "persuasive authority", "legal analysis"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Circuit Split Identification and Its Importance",
            content="A circuit split occurs when two or more federal circuit courts of appeals offer conflicting rulings on the same legal question, often prompting Supreme Court review.",
            tags=["circuit split", "supreme court", "federal courts"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="En Banc Reconsideration in Appellate Courts",
            content="En banc reconsideration allows all judges of an appellate court to review a decision, typically used to resolve conflicts or address important questions.",
            tags=["en banc", "appellate court", "reconsideration"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Supreme Court Certiorari: Granting Review",
            content="The Supreme Court grants certiorari based on factors such as circuit splits, importance of the issue, and the need to resolve inconsistencies in the law.",
            tags=["certiorari", "supreme court", "review"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Signals of Overruling Precedent",
            content="Courts may signal intent to overrule precedent through dicta, concurring opinions, or explicit statements, alerting practitioners to possible doctrinal shifts.",
            tags=["overruling", "precedent", "signals"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Distinguishing Methodology in Case Law",
            content="Distinguishing involves showing that a precedent does not apply due to factual or legal differences, allowing courts to avoid binding authority.",
            tags=["distinguishing", "precedent", "case law"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Case Treatment Taxonomy",
            content="Case treatment refers to how later courts interpret and apply earlier decisions, including following, distinguishing, overruling, or criticizing precedent.",
            tags=["case treatment", "precedent", "taxonomy"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Authority Weight Scoring in Legal Research",
            content="Authority weight scoring evaluates the persuasive and binding strength of legal sources, factoring in jurisdiction, recency, and court hierarchy.",
            tags=["authority weight", "legal research", "scoring"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Recency vs Landmark Weight in Precedent",
            content="Recent cases may be more relevant, but landmark decisions often carry greater precedential weight due to their foundational nature.",
            tags=["recency", "landmark", "precedent"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Vertical Stare Decisis: Absolute Adherence",
            content="Vertical stare decisis requires lower courts to follow higher court decisions absolutely, ensuring a hierarchical consistency in the law.",
            tags=["vertical stare decisis", "hierarchy", "adherence"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Horizontal Stare Decisis: Flexibility Among Peers",
            content="Horizontal stare decisis allows appellate courts to reconsider their own past decisions, offering flexibility but risking instability.",
            tags=["horizontal stare decisis", "flexibility", "appellate"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Persuasive Authority Weight Factors",
            content="Factors affecting persuasive authority include the reasoning quality, jurisdictional proximity, recency, and the court's reputation.",
            tags=["persuasive authority", "weight", "factors"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Shepardizing and Citator Services",
            content="Shepardizing is the process of checking the subsequent history and treatment of a case using citator services, ensuring good law.",
            tags=["shepardizing", "citator", "case treatment"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Analogical Reasoning in Legal Analysis",
            content="Analogical reasoning involves comparing facts and principles of past cases to current disputes, forming the core of common law adjudication.",
            tags=["analogical reasoning", "legal analysis", "common law"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Plurality Opinion Precedential Effect",
            content="Plurality opinions, lacking a majority, have limited precedential value; courts may look to the narrowest grounds for guidance.",
            tags=["plurality opinion", "precedential effect", "majority"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Concurring and Dissenting Opinions: Value and Limits",
            content="Concurring and dissenting opinions do not bind but may influence future cases or signal doctrinal shifts.",
            tags=["concurring opinion", "dissenting opinion", "value"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Per Curiam Opinions: Precedential Weight",
            content="Per curiam opinions, issued collectively by the court, may carry precedential weight depending on context and jurisdiction.",
            tags=["per curiam", "precedential weight", "opinion"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Unpublished Opinions and Citation Rules",
            content="Unpublished opinions generally lack precedential value but may be cited for persuasive purposes in some jurisdictions.",
            tags=["unpublished opinion", "citation", "rules"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Interlocutory vs Final Judgment Precedent",
            content="Interlocutory decisions are not final and usually lack precedential effect, while final judgments may bind future cases.",
            tags=["interlocutory", "final judgment", "precedent"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Dictum vs Holding: The Distinction",
            content="A holding is the court's determination of a matter essential to the outcome, while dictum is commentary not necessary to the decision.",
            tags=["dictum", "holding", "distinction"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="State Court Precedent in Federal Court",
            content="Federal courts must follow state supreme court precedent on state law issues but may disregard lower state court decisions.",
            tags=["state court", "federal court", "precedent"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Superseded by Statute: Precedent and Legislative Change",
            content="A precedent may be superseded by statute if the legislature enacts a law that overrides the court's decision.",
            tags=["superseded", "statute", "precedent"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Landmark Case Identification Criteria",
            content="Landmark cases are identified by their lasting impact, novelty, and the breadth of issues resolved.",
            tags=["landmark", "case identification", "criteria"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Trend Analysis Across Jurisdictions",
            content="Trend analysis examines how legal principles evolve across different jurisdictions, revealing shifts in doctrine or consensus.",
            tags=["trend analysis", "jurisdictions", "doctrine"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Negative Precedent Treatment Analysis",
            content="Negative treatment, such as overruling or criticism, diminishes a precedent's authority and may signal doctrinal change.",
            tags=["negative treatment", "precedent", "analysis"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="The Role of Precedent in Common Law Systems",
            content="Precedent forms the backbone of common law systems, guiding judicial decisions and ensuring legal continuity.",
            tags=["precedent", "common law", "judicial decisions"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Hierarchy of Courts and Precedential Value",
            content="The hierarchical structure of courts determines the binding or persuasive value of their decisions.",
            tags=["hierarchy", "courts", "precedential value"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="The Process of Overruling Precedent",
            content="Overruling precedent requires a court to expressly reject a prior decision, often after careful consideration of reliance and doctrinal development.",
            tags=["overruling", "precedent", "process"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Factors Influencing Supreme Court Certiorari",
            content="The Supreme Court considers factors like national importance, conflict among lower courts, and the need to clarify federal law when granting certiorari.",
            tags=["supreme court", "certiorari", "factors"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)