import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Optional

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
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.doc_count: int = 0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.inverted_index[term].add(doc.id)
                self.doc_freqs[term] += 1
            self.doc_count += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.doc_count if self.doc_count else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            final_score = (bm25_score * 0.7 + tfidf_score * 0.3) * doc.weight
            snippet = self._make_snippet(doc, query_terms)
            scored_results.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, int]:
        return {
            "documents": self.doc_count,
            "unique_terms": len(self.inverted_index),
            "avg_doc_length": int(self.avg_doc_length)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.doc_count - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            numer = f * (self._bm25_k1 + 1)
            score += idf * numer / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            tf_norm = f / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:window*2] + ("..." if len(content) > window*2 else "")
        start = max(min(positions) - window, 0)
        end = min(max(positions) + window, len(content))
        snippet = content[start:end]
        # Highlight terms
        for term in set(query_terms):
            snippet = re.sub(r'(?i)\b({})\b'.format(re.escape(term)), r'**\1**', snippet)
        return snippet

_index_instance: Optional[SearchIndex] = None
_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _index_instance
    with _index_lock:
        if _index_instance is None:
            _index_instance = SearchIndex()
            _preseed_documents(_index_instance)
        return _index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(1, "Probability Assessment Scales", 
            "Defines qualitative and quantitative scales for assessing probability in risk analysis. Includes likelihood descriptors, numeric ranges, and calibration techniques.", 
            ["probability_assessment_scales", "risk_analysis"], 1.0),
        SearchDocument(2, "Impact Severity Classification", 
            "Framework for classifying impact severity, including financial, operational, reputational, and regulatory dimensions. Provides examples and scoring grids.", 
            ["impact_severity_classification", "risk_scoring"], 1.0),
        SearchDocument(3, "Risk Scoring Models", 
            "Overview of risk scoring models: matrix, weighted, and algorithmic approaches. Discusses aggregation, normalization, and subjectivity mitigation.", 
            ["risk_scoring_models", "risk_matrix"], 1.0),
        SearchDocument(4, "COSO ERM Framework", 
            "Summary of COSO Enterprise Risk Management: components, principles, and integration with strategy and performance. Emphasizes risk appetite and governance.", 
            ["coso_erm_framework", "risk_governance"], 1.0),
        SearchDocument(5, "ISO 31000 Risk Management", 
            "Key elements of ISO 31000: risk identification, assessment, treatment, monitoring, and communication. Focus on continual improvement.", 
            ["iso_31000_risk_management", "risk_standards"], 1.0),
        SearchDocument(6, "Risk Appetite Definitions", 
            "Defines risk appetite, tolerance, and capacity. Explains cascading risk appetite through the organization and alignment with objectives.", 
            ["risk_appetite_definitions", "risk_governance"], 1.0),
        SearchDocument(7, "Inherent vs Residual Risk", 
            "Distinguishes inherent risk (before controls) from residual risk (after controls). Provides calculation examples and implications for decision-making.", 
            ["inherent_vs_residual_risk", "risk_measurement"], 1.0),
        SearchDocument(8, "Control Effectiveness Rating", 
            "Methods for rating control effectiveness: design, implementation, and operating effectiveness. Includes scoring templates and common pitfalls.", 
            ["control_effectiveness_rating", "risk_controls"], 1.0),
        SearchDocument(9, "Monte Carlo Simulation in Risk", 
            "Explains Monte Carlo simulation for risk quantification: random sampling, probability distributions, and scenario analysis. Includes practical steps.", 
            ["monte_carlo_simulation", "quantitative_risk"], 1.0),
        SearchDocument(10, "Sensitivity Analysis & Tornado Diagrams", 
            "Describes sensitivity analysis for risk drivers and tornado diagram construction. Shows how to prioritize variables and interpret results.", 
            ["sensitivity_analysis_tornado", "risk_visualization"], 1.0),
        SearchDocument(11, "Risk Register Structure", 
            "Best practices for structuring a risk register: fields, taxonomy, update cycles, and ownership. Sample templates provided.", 
            ["risk_register_structure", "risk_documentation"], 1.0),
        SearchDocument(12, "Key Risk Indicators (KRIs)", 
            "Defines KRIs, their selection, calibration, and monitoring. Discusses leading vs lagging indicators and integration with dashboards.", 
            ["key_risk_indicators", "risk_monitoring"], 1.0),
        SearchDocument(13, "Risk Adjusted Return", 
            "Explains risk-adjusted return metrics: RAROC, Sharpe ratio, and economic value added. Application in capital allocation and performance measurement.", 
            ["risk_adjusted_return", "financial_risk"], 1.0),
        SearchDocument(14, "Expected Value Analysis", 
            "Covers expected value calculation for risk events, including probability-weighted outcomes and decision tree examples.", 
            ["expected_value_analysis", "quantitative_risk"], 1.0),
        SearchDocument(15, "Risk Heat Map Generation", 
            "Step-by-step guide to generating risk heat maps: data preparation, scoring, visualization, and interpretation.", 
            ["risk_heat_map_generation", "risk_visualization"], 1.0),
        SearchDocument(16, "Risk Mitigation Strategies", 
            "Catalog of risk mitigation strategies: avoidance, reduction, transfer, and acceptance. Includes practical examples and selection criteria.", 
            ["risk_mitigation_strategies", "risk_treatment"], 1.0),
        SearchDocument(17, "Risk Category Classification", 
            "Taxonomy of risk categories: strategic, operational, financial, compliance, and emerging risks. Guidance on classification and reporting.", 
            ["risk_category_classification", "risk_taxonomy"], 1.0),
        SearchDocument(18, "Risk Aggregation Methods", 
            "Methods for aggregating risks: simple summation, correlation matrices, and copulas. Discusses limitations and best practices.", 
            ["risk_aggregation_methods", "risk_analysis"], 1.0),
        SearchDocument(19, "Risk Appetite Cascade", 
            "Describes cascading risk appetite from board level to business units. Tools for communication and alignment.", 
            ["risk_appetite_cascade", "risk_governance"], 1.0),
        SearchDocument(20, "Scenario Analysis Design", 
            "How to design effective scenario analyses: scenario selection, plausibility, quantification, and stress testing.", 
            ["scenario_analysis_design", "risk_scenarios"], 1.0),
        SearchDocument(21, "Bow-Tie Analysis", 
            "Introduction to bow-tie analysis: visualizing risk pathways, barriers, and escalation factors. Includes diagramming tips.", 
            ["bow_tie_analysis", "risk_visualization"], 1.0),
        SearchDocument(22, "Risk Velocity Assessment", 
            "Methods for assessing risk velocity: time to impact, detection lag, and prioritization. Application in risk registers.", 
            ["risk_velocity_assessment", "risk_prioritization"], 1.0),
        SearchDocument(23, "Risk Culture Assessment", 
            "Frameworks and tools for assessing risk culture: surveys, interviews, and behavioral indicators. Links to risk appetite and governance.", 
            ["risk_culture_assessment", "risk_governance"], 1.0),
        SearchDocument(24, "Emerging Risk Identification", 
            "Techniques for identifying emerging risks: horizon scanning, environmental scanning, and expert panels. Integration with risk registers.", 
            ["emerging_risk_identification", "risk_monitoring"], 1.0),
        SearchDocument(25, "Risk Reporting Structure", 
            "Best practices for risk reporting: escalation pathways, reporting templates, and board dashboards. Ensures timely and effective communication.", 
            ["risk_reporting_structure", "risk_communication"], 1.0),
        SearchDocument(26, "Three Lines Model", 
            "Overview of the Three Lines Model: roles of management, risk/compliance, and internal audit. Clarifies accountability and assurance.", 
            ["three_lines_model", "risk_governance"], 1.0),
        SearchDocument(27, "Advanced Probability Scales", 
            "Explores advanced probability scales, including Bayesian updating and subjective probability calibration.", 
            ["probability_assessment_scales", "advanced_methods"], 0.9),
        SearchDocument(28, "Quantifying Control Effectiveness", 
            "Quantitative methods for measuring control effectiveness, including control self-assessment and key control indicators.", 
            ["control_effectiveness_rating", "quantitative_risk"], 0.95),
        SearchDocument(29, "Risk Aggregation with Copulas", 
            "Explains the use of copulas in risk aggregation for non-linear dependencies and tail risk assessment.", 
            ["risk_aggregation_methods", "copulas"], 0.95),
        SearchDocument(30, "Risk Appetite in ISO 31000", 
            "How ISO 31000 addresses risk appetite and tolerance, with practical examples for policy development.", 
            ["iso_31000_risk_management", "risk_appetite_definitions"], 0.95),
        SearchDocument(31, "Scenario Analysis for Emerging Risks", 
            "Applying scenario analysis to identify and assess emerging risks, with case studies and facilitation tips.", 
            ["scenario_analysis_design", "emerging_risk_identification"], 0.95),
        SearchDocument(32, "Risk Heat Maps: Pitfalls", 
            "Common pitfalls in risk heat map design and interpretation. How to avoid misrepresentation and bias.", 
            ["risk_heat_map_generation", "risk_visualization"], 0.9),
        SearchDocument(33, "KRIs in Financial Services", 
            "Selection and calibration of key risk indicators for financial institutions. Regulatory expectations and best practices.", 
            ["key_risk_indicators", "financial_risk"], 0.9),
        SearchDocument(34, "Monte Carlo for Credit Risk", 
            "Using Monte Carlo simulation to model credit risk portfolios. Includes loss distribution and stress testing.", 
            ["monte_carlo_simulation", "credit_risk"], 0.9),
        SearchDocument(35, "Risk Register Automation", 
            "Tools and techniques for automating risk register updates, notifications, and analytics.", 
            ["risk_register_structure", "automation"], 0.9),
    ]
    for doc in docs:
        index.add_document(doc)