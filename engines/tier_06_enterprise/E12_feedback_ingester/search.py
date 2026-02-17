import math
import threading
import re
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
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.total_docs: int = 0
        self.stats: Dict[str, int] = {
            'documents': 0,
            'terms': 0,
            'avg_doc_length': 0
        }

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_freqs[term][doc.id] = freq
                self.term_doc_freq[term] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self.stats['documents'] = self.total_docs
            self.stats['terms'] = len(self.term_doc_freq)
            self.stats['avg_doc_length'] = self.avg_doc_length
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: Dict[str, float] = defaultdict(float)
        bm25_params = {'k1': 1.5, 'b': 0.75}
        tfidf_scores: Dict[str, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            docs_with_term = self.term_freqs.get(term, {})
            for doc_id, freq in docs_with_term.items():
                doc_length = self.doc_lengths[doc_id]
                bm25_score = self._score_bm25(freq, doc_length, idf, bm25_params)
                scores[doc_id] += bm25_score * self.documents[doc_id].weight
                tf = freq / doc_length
                tfidf_scores[doc_id] += tf * idf * self.documents[doc_id].weight
        combined_scores = {}
        for doc_id in scores:
            combined_scores[doc_id] = scores[doc_id] + 0.5 * tfidf_scores[doc_id]
        ranked = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        return dict(self.stats)

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1)
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, tf: int, doc_length: int, idf: float, params: Dict[str, float]) -> float:
        k1 = params['k1']
        b = params['b']
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        denom = tf + k1 * (1 - b + b * (doc_length / avg_dl))
        score = idf * ((tf * (k1 + 1)) / (denom + 1e-6))
        return score

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if positions:
            start = max(positions[0] - 5, 0)
            end = min(positions[0] + 15, len(tokens))
            snippet = ' '.join(tokens[start:end])
        else:
            snippet = ' '.join(tokens[:20])
        return snippet

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
            "doc1",
            "Correction Intake Protocols",
            "Guidelines for processing correction intake submissions, including validation and routing.",
            ["correction_intake", "validation", "routing"],
            1.0
        ),
        SearchDocument(
            "doc2",
            "Rating Aggregation Methods",
            "Aggregating ratings from multiple sources using weighted averages and aggregation rules.",
            ["rating_aggregation", "aggregation_rules"],
            1.0
        ),
        SearchDocument(
            "doc3",
            "Rejection Processing Workflow",
            "Steps for handling rejected feedback, including conflict detection and flagging.",
            ["rejection_processing", "conflict_detection", "flag_processing"],
            1.0
        ),
        SearchDocument(
            "doc4",
            "Approval Tracking System",
            "Tracking approvals across correction intake and suggestion processing pipelines.",
            ["approval_tracking", "correction_intake", "suggestion_processing"],
            1.0
        ),
        SearchDocument(
            "doc5",
            "Suggestion Processing Guidelines",
            "Processing suggestions with credential validation and override processing.",
            ["suggestion_processing", "credential_validation", "override_processing"],
            1.0
        ),
        SearchDocument(
            "doc6",
            "Flag Processing Doctrine",
            "Flagging errors and anomalies in feedback routing and regression detection.",
            ["flag_processing", "feedback_routing", "regression_detection"],
            1.0
        ),
        SearchDocument(
            "doc7",
            "Override Processing Rules",
            "Rules for overriding aggregated ratings and doctrine update signals.",
            ["override_processing", "aggregation_rules", "doctrine_update_signal"],
            1.0
        ),
        SearchDocument(
            "doc8",
            "Credential Validation Procedures",
            "Validating credentials for feedback submitters and auto-apply rules.",
            ["credential_validation", "auto_apply_rules"],
            1.0
        ),
        SearchDocument(
            "doc9",
            "Conflict Detection Algorithms",
            "Detecting conflicts in feedback and correction intake using error pattern detection.",
            ["conflict_detection", "error_pattern_detection"],
            1.0
        ),
        SearchDocument(
            "doc10",
            "Aggregation Rules Reference",
            "Reference for aggregation rules in rating aggregation and impact tracking.",
            ["aggregation_rules", "rating_aggregation", "impact_tracking"],
            1.0
        ),
        SearchDocument(
            "doc11",
            "Doctrine Update Signal Handling",
            "Handling doctrine update signals and keyword adjustment signals.",
            ["doctrine_update_signal", "keyword_adjustment_signal"],
            1.0
        ),
        SearchDocument(
            "doc12",
            "Keyword Adjustment Signal Processing",
            "Processing keyword adjustment signals for confidence recalibration.",
            ["keyword_adjustment_signal", "confidence_recalibration_signal"],
            1.0
        ),
        SearchDocument(
            "doc13",
            "Confidence Recalibration Signal",
            "Recalibrating confidence scores based on error pattern detection.",
            ["confidence_recalibration_signal", "error_pattern_detection"],
            1.0
        ),
        SearchDocument(
            "doc14",
            "Error Pattern Detection Guide",
            "Guide to detecting error patterns in feedback and training pair generation.",
            ["error_pattern_detection", "training_pair_generation"],
            1.0
        ),
        SearchDocument(
            "doc15",
            "Training Pair Generation",
            "Generating training pairs from correction intake and suggestion processing.",
            ["training_pair_generation", "correction_intake", "suggestion_processing"],
            1.0
        ),
        SearchDocument(
            "doc16",
            "Impact Tracking Metrics",
            "Tracking the impact of auto-applied rules and feedback routing.",
            ["impact_tracking", "auto_apply_rules", "feedback_routing"],
            1.0
        ),
        SearchDocument(
            "doc17",
            "Auto Apply Rules Doctrine",
            "Doctrine for auto-applying rules in credential validation and approval tracking.",
            ["auto_apply_rules", "credential_validation", "approval_tracking"],
            1.0
        ),
        SearchDocument(
            "doc18",
            "Feedback Routing Mechanisms",
            "Mechanisms for routing feedback based on flag processing and regression detection.",
            ["feedback_routing", "flag_processing", "regression_detection"],
            1.0
        ),
        SearchDocument(
            "doc19",
            "Quality Dashboard Metrics",
            "Metrics for quality dashboard including rating aggregation and impact tracking.",
            ["quality_dashboard_metrics", "rating_aggregation", "impact_tracking"],
            1.0
        ),
        SearchDocument(
            "doc20",
            "Regression Detection Procedures",
            "Procedures for detecting regressions in feedback and correction intake.",
            ["regression_detection", "feedback_routing", "correction_intake"],
            1.0
        ),
        SearchDocument(
            "doc21",
            "Correction Intake Validation",
            "Validation steps for correction intake submissions and credential checks.",
            ["correction_intake", "validation", "credential_validation"],
            1.0
        ),
        SearchDocument(
            "doc22",
            "Rating Aggregation Quality",
            "Ensuring quality in rating aggregation using aggregation rules and metrics.",
            ["rating_aggregation", "aggregation_rules", "quality_dashboard_metrics"],
            1.0
        ),
        SearchDocument(
            "doc23",
            "Rejection Processing Signals",
            "Signals and triggers for rejection processing and conflict detection.",
            ["rejection_processing", "conflict_detection", "doctrine_update_signal"],
            1.0
        ),
        SearchDocument(
            "doc24",
            "Approval Tracking Metrics",
            "Metrics for tracking approvals in suggestion processing and auto apply rules.",
            ["approval_tracking", "suggestion_processing", "auto_apply_rules"],
            1.0
        ),
        SearchDocument(
            "doc25",
            "Suggestion Processing Impact",
            "Impact of suggestion processing on aggregation rules and impact tracking.",
            ["suggestion_processing", "aggregation_rules", "impact_tracking"],
            1.0
        ),
        SearchDocument(
            "doc26",
            "Flag Processing and Routing",
            "Flag processing in feedback routing and regression detection pipelines.",
            ["flag_processing", "feedback_routing", "regression_detection"],
            1.0
        ),
        SearchDocument(
            "doc27",
            "Override Processing Signals",
            "Signals for override processing and doctrine update handling.",
            ["override_processing", "doctrine_update_signal"],
            1.0
        ),
        SearchDocument(
            "doc28",
            "Credential Validation Impact",
            "Impact of credential validation on auto apply rules and conflict detection.",
            ["credential_validation", "auto_apply_rules", "conflict_detection"],
            1.0
        ),
        SearchDocument(
            "doc29",
            "Conflict Detection Patterns",
            "Patterns for conflict detection in correction intake and error pattern detection.",
            ["conflict_detection", "correction_intake", "error_pattern_detection"],
            1.0
        ),
        SearchDocument(
            "doc30",
            "Aggregation Rules Doctrine",
            "Doctrine for aggregation rules in rating aggregation and impact tracking.",
            ["aggregation_rules", "rating_aggregation", "impact_tracking"],
            1.0
        ),
        SearchDocument(
            "doc31",
            "Doctrine Update Signal Reference",
            "Reference for doctrine update signals and keyword adjustment signals.",
            ["doctrine_update_signal", "keyword_adjustment_signal"],
            1.0
        ),
        SearchDocument(
            "doc32",
            "Keyword Adjustment Signal Guide",
            "Guide for keyword adjustment signals and confidence recalibration.",
            ["keyword_adjustment_signal", "confidence_recalibration_signal"],
            1.0
        ),
        SearchDocument(
            "doc33",
            "Confidence Recalibration Patterns",
            "Patterns for recalibrating confidence scores using error pattern detection.",
            ["confidence_recalibration_signal", "error_pattern_detection"],
            1.0
        ),
        SearchDocument(
            "doc34",
            "Error Pattern Detection Metrics",
            "Metrics for error pattern detection in feedback and training pair generation.",
            ["error_pattern_detection", "training_pair_generation"],
            1.0
        ),
        SearchDocument(
            "doc35",
            "Training Pair Generation Impact",
            "Impact of training pair generation on correction intake and suggestion processing.",
            ["training_pair_generation", "correction_intake", "suggestion_processing"],
            1.0
        ),
        SearchDocument(
            "doc36",
            "Impact Tracking Dashboard",
            "Dashboard for tracking impact of auto-applied rules and feedback routing.",
            ["impact_tracking", "auto_apply_rules", "feedback_routing"],
            1.0
        ),
        SearchDocument(
            "doc37",
            "Auto Apply Rules Reference",
            "Reference for auto apply rules in credential validation and approval tracking.",
            ["auto_apply_rules", "credential_validation", "approval_tracking"],
            1.0
        ),
        SearchDocument(
            "doc38",
            "Feedback Routing Quality",
            "Quality metrics for feedback routing based on flag processing and regression detection.",
            ["feedback_routing", "flag_processing", "regression_detection"],
            1.0
        ),
        SearchDocument(
            "doc39",
            "Quality Dashboard Metrics Guide",
            "Guide for quality dashboard metrics including rating aggregation and impact tracking.",
            ["quality_dashboard_metrics", "rating_aggregation", "impact_tracking"],
            1.0
        ),
        SearchDocument(
            "doc40",
            "Regression Detection Impact",
            "Impact of regression detection on feedback and correction intake.",
            ["regression_detection", "feedback_routing", "correction_intake"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)