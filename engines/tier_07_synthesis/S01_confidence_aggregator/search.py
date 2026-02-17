import math
import threading
import re
import heapq
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[str, SearchDocument] = {}
        self._doc_tokens: Dict[str, List[str]] = {}
        self._inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._term_freqs: Dict[str, Counter] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._avg_doc_length: float = 0.0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75
        self._total_docs = 0
        self._total_terms = 0

    # --- Tokenization ---
    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return tokens

    # --- Add Document ---
    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title) + self._tokenize(doc.content)
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            tf = Counter(tokens)
            self._term_freqs[doc.id] = tf
            self._doc_lengths[doc.id] = len(tokens)
            self._total_terms += len(tokens)
            for term in tf:
                self._inverted_index[term].add(doc.id)
                self._doc_freqs[term] += 1
            self._total_docs += 1
            self._avg_doc_length = self._total_terms / self._total_docs if self._total_docs > 0 else 0.0
            self._idf_cache.clear()

    # --- IDF Calculation ---
    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freqs.get(term, 0)
        N = self._total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    # --- BM25 Scoring ---
    def _score_bm25(self, query_tokens: List[str], doc_id: str) -> float:
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_tokens:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / self._avg_doc_length)
            score += idf * freq * (self._bm25_k1 + 1) / denom
        doc_weight = self._documents[doc_id].weight
        return score * doc_weight

    # --- TF-IDF Scoring ---
    def _score_tfidf(self, query_tokens: List[str], doc_id: str) -> float:
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_tokens:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        doc_weight = self._documents[doc_id].weight
        return score * doc_weight

    # --- Snippet Extraction ---
    def _extract_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:160] + '...' if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + '...' if end < len(tokens) else snippet

    # --- Search ---
    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        candidate_docs = set()
        for term in query_tokens:
            candidate_docs.update(self._inverted_index.get(term, set()))
        scored = []
        for doc_id in candidate_docs:
            if method == 'bm25':
                score = self._score_bm25(query_tokens, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_tokens, doc_id)
            else:
                score = self._score_bm25(query_tokens, doc_id)
            if score > 0:
                doc = self._documents[doc_id]
                snippet = self._extract_snippet(doc, query_tokens)
                scored.append(SearchResult(doc_id, score, doc.title, snippet))
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:limit]

    # --- Stats ---
    def get_stats(self) -> Dict[str, float]:
        return {
            'total_documents': self._total_docs,
            'avg_doc_length': self._avg_doc_length,
            'unique_terms': len(self._doc_freqs),
        }

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
            title="Bayesian Confidence Aggregation Overview",
            content="Bayesian methods combine evidence from multiple sources to estimate confidence. Aggregation involves updating beliefs based on observed data and prior reliability.",
            tags=["bayesian", "aggregation", "confidence"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Weighted Scoring by Engine Reliability",
            content="Reliability-weighted scoring assigns higher influence to engines with proven accuracy. Weights are calibrated using historical performance metrics.",
            tags=["weighted scoring", "reliability", "ensemble"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Detecting Inter-Engine Correlation",
            content="Correlation detection identifies dependencies between engines. High inter-engine correlation can bias aggregated confidence estimates.",
            tags=["correlation", "dependency", "ensemble"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Confidence Calibration Methods",
            content="Calibration aligns predicted confidence with observed outcomes. Techniques include Platt scaling, isotonic regression, and temperature scaling.",
            tags=["calibration", "confidence", "methods"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Bootstrap Uncertainty Estimation",
            content="Bootstrap resampling quantifies uncertainty in confidence estimates. By sampling with replacement, we generate distributions over possible outcomes.",
            tags=["bootstrap", "uncertainty", "estimation"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Score Normalization Techniques",
            content="Normalization ensures scores from different engines are comparable. Methods include min-max scaling and z-score normalization.",
            tags=["normalization", "score", "scaling"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Outlier Detection in Confidence Scores",
            content="Outlier detection identifies anomalous confidence values that may indicate engine malfunction or data drift.",
            tags=["outlier", "detection", "confidence"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Ensemble Methods for Confidence Aggregation",
            content="Ensemble methods, such as stacking and bagging, improve confidence aggregation by leveraging diverse engine outputs.",
            tags=["ensemble", "aggregation", "methods"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Reliability Weighting in Score Fusion",
            content="Score fusion combines outputs from multiple engines, weighting them by reliability to produce robust confidence estimates.",
            tags=["reliability", "fusion", "score"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Score Fusion Techniques",
            content="Techniques for score fusion include weighted averaging, Dempster-Shafer theory, and Bayesian model averaging.",
            tags=["fusion", "score", "techniques"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Disagreement Quantification",
            content="Quantifying disagreement among engines helps assess uncertainty and identify cases where aggregation may be unreliable.",
            tags=["disagreement", "quantification", "uncertainty"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Dempster-Shafer Evidence Theory",
            content="Dempster-Shafer theory generalizes Bayesian inference, allowing for explicit representation of uncertainty and ignorance.",
            tags=["dempster-shafer", "evidence", "theory"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Confidence Interval Construction",
            content="Confidence intervals provide a range within which the true value likely lies. Construction methods include bootstrap and Bayesian credible intervals.",
            tags=["confidence interval", "construction", "uncertainty"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Monte Carlo Confidence Estimation",
            content="Monte Carlo methods estimate confidence by simulating many possible outcomes, providing empirical distributions for uncertainty quantification.",
            tags=["monte carlo", "confidence", "estimation"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Calibration Curve Analysis",
            content="Calibration curves plot predicted confidence against observed accuracy, revealing over- or under-confidence in engine outputs.",
            tags=["calibration", "curve", "analysis"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Brier Score Evaluation",
            content="The Brier score measures the accuracy of probabilistic predictions, penalizing both over- and under-confidence.",
            tags=["brier score", "evaluation", "probability"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Log-Loss Scoring",
            content="Log-loss, or cross-entropy, evaluates the quality of confidence estimates by penalizing incorrect high-confidence predictions.",
            tags=["log-loss", "scoring", "cross-entropy"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Precision-Recall Tradeoff",
            content="Precision and recall metrics often trade off against each other. Aggregation strategies must balance these to optimize overall performance.",
            tags=["precision", "recall", "tradeoff"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="ROC AUC Aggregation",
            content="ROC AUC summarizes the tradeoff between true and false positive rates. Aggregated confidence can be evaluated using AUC metrics.",
            tags=["roc", "auc", "aggregation"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Confidence Decay Over Time",
            content="Confidence decay models account for the decreasing reliability of predictions as time passes since the last calibration.",
            tags=["confidence", "decay", "time"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Platt Scaling for Confidence Calibration",
            content="Platt scaling fits a logistic regression model to map raw scores to calibrated probabilities, improving confidence estimation.",
            tags=["platt scaling", "calibration", "confidence"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Isotonic Regression in Calibration",
            content="Isotonic regression is a non-parametric calibration method that fits a monotonically increasing function to map scores to probabilities.",
            tags=["isotonic regression", "calibration", "probability"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Temperature Scaling for Neural Networks",
            content="Temperature scaling adjusts the softmax output of neural networks to calibrate confidence scores without affecting classification accuracy.",
            tags=["temperature scaling", "calibration", "neural networks"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Stacked Generalization in Ensembles",
            content="Stacked generalization, or stacking, uses a meta-learner to combine engine outputs, often improving aggregated confidence.",
            tags=["stacking", "ensemble", "aggregation"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Bagging and Bootstrap Aggregation",
            content="Bagging leverages bootstrap samples to train multiple engines, reducing variance and improving confidence estimates.",
            tags=["bagging", "bootstrap", "aggregation"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Z-Score Normalization in Score Fusion",
            content="Z-score normalization standardizes engine outputs, allowing fair comparison and fusion of confidence scores.",
            tags=["z-score", "normalization", "fusion"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Handling Missing Engine Outputs",
            content="Robust aggregation methods can handle missing engine outputs by imputing values or adjusting weights dynamically.",
            tags=["missing data", "aggregation", "robustness"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Correlation Matrix Analysis",
            content="A correlation matrix quantifies dependencies among engines, informing aggregation strategies and reliability weighting.",
            tags=["correlation", "matrix", "analysis"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Prior and Posterior in Bayesian Aggregation",
            content="Bayesian aggregation distinguishes between prior beliefs and posterior updates after observing engine outputs.",
            tags=["bayesian", "prior", "posterior"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Ignorance and Uncertainty Representation",
            content="Dempster-Shafer theory allows explicit representation of ignorance, complementing Bayesian uncertainty quantification.",
            tags=["ignorance", "uncertainty", "dempster-shafer"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)