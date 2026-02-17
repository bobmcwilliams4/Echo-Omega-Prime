import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)
        self.lock = threading.Lock()
        self._initialized = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
            self._update_avg_doc_length()
            self._initialized = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        doc_tf_scores: Dict[int, float] = defaultdict(float)
        for token in tokens:
            idf = self._compute_idf(token)
            docs_with_token = self.inverted_index.get(token, {})
            for doc_id, freq in docs_with_token.items():
                doc = self.documents[doc_id]
                score = self._score_bm25(token, freq, doc_id, idf, doc.weight)
                doc_scores[doc_id] += score
                tf_score = self._score_tf_idf(token, freq, doc_id, idf, doc.weight)
                doc_tf_scores[doc_id] += tf_score
        # Combine BM25 and TF-IDF scores (weighted sum)
        results = []
        for doc_id in doc_scores:
            bm25 = doc_scores[doc_id]
            tfidf = doc_tf_scores[doc_id]
            combined_score = 0.7 * bm25 + 0.3 * tfidf
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, tokens)
            results.append(SearchResult(doc_id, combined_score, doc.title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.inverted_index)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, token: str) -> float:
        if token in self.idf_cache:
            return self.idf_cache[token]
        N = self.total_docs
        n = len(self.inverted_index.get(token, {}))
        # BM25 idf formula
        idf = math.log(1 + (N - n + 0.5) / (n + 0.5))
        self.idf_cache[token] = idf
        return idf

    def _score_bm25(self, token: str, freq: int, doc_id: int, idf: float, weight: float) -> float:
        k1 = 1.5
        b = 0.75
        doc_len = self.doc_lengths.get(doc_id, 1)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        tf = freq
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * doc_len / avg_dl)
        score = idf * (numerator / denominator) * weight
        return score

    def _score_tf_idf(self, token: str, freq: int, doc_id: int, idf: float, weight: float) -> float:
        doc_len = self.doc_lengths.get(doc_id, 1)
        tf_norm = freq / doc_len
        score = tf_norm * idf * weight
        return score

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _make_snippet(self, content: str, query_tokens: List[str], snippet_len: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return ' '.join(tokens[:snippet_len])
        start = max(positions[0] - 10, 0)
        end = min(start + snippet_len, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

# --- Singleton Factory ---

_search_index_singleton: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_singleton
    with _search_index_lock:
        if _search_index_singleton is None:
            _search_index_singleton = SearchIndex()
            _preseed_documents(_search_index_singleton)
        return _search_index_singleton

# --- Pre-seed Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Horner Buildup Analysis Fundamentals",
            "Horner buildup analysis is a classical method for interpreting pressure data from well tests. It involves plotting pressure versus the Horner time ratio to estimate reservoir properties such as permeability and skin factor. The technique assumes radial flow and negligible wellbore storage effects.",
            ["horner_buildup_analysis", "permeability_estimation_methods"],
            1.0
        ),
        SearchDocument(
            2,
            "Bourdet Derivative Analysis for Well Testing",
            "Bourdet derivative analysis enhances the interpretation of pressure transient data by calculating the pressure derivative with respect to logarithmic time. This approach helps identify flow regimes, boundary effects, and wellbore storage impacts.",
            ["bourdet_derivative_analysis", "pressure_derivative_diagnostic_features"],
            1.0
        ),
        SearchDocument(
            3,
            "Skin Factor Determination Techniques",
            "Skin factor quantifies the additional pressure drop caused by near-wellbore damage or stimulation. It is determined using buildup or drawdown tests, often through Horner or derivative analysis. Accurate skin estimation is critical for optimizing well productivity.",
            ["skin_factor_determination", "horner_buildup_analysis"],
            1.0
        ),
        SearchDocument(
            4,
            "Dual Porosity Interpretation in Well Testing",
            "Dual porosity models describe reservoirs with matrix and fracture systems. Well test interpretation in such reservoirs requires specialized type curves and superposition principles to distinguish between matrix and fracture contributions.",
            ["dual_porosity_interpretation", "type_curve_matching_methodology"],
            1.0
        ),
        SearchDocument(
            5,
            "Boundary Effect Identification in Pressure Transients",
            "Boundary effects manifest as deviations in pressure response during well tests. Identifying boundaries such as faults, sealing layers, or reservoir limits is essential for accurate reservoir characterization. Derivative analysis and type curve matching are commonly used.",
            ["boundary_effect_identification", "pressure_derivative_diagnostic_features"],
            1.0
        ),
        SearchDocument(
            6,
            "Horizontal Well Testing: Principles and Practices",
            "Horizontal wells exhibit complex flow regimes including linear, radial, and elliptical flow. Well test interpretation must account for well length, reservoir anisotropy, and boundary effects. Superposition principles are often applied.",
            ["horizontal_well_testing", "superposition_principles"],
            1.0
        ),
        SearchDocument(
            7,
            "Rate Transient Analysis in Unconventional Reservoirs",
            "Rate transient analysis (RTA) is used to estimate reservoir properties in unconventional plays. By analyzing production rate and pressure data over time, RTA can reveal permeability, fracture effectiveness, and boundary conditions.",
            ["rate_transient_analysis_unconventional", "permeability_estimation_methods"],
            1.0
        ),
        SearchDocument(
            8,
            "Wellbore Storage Effects in Pressure Transient Testing",
            "Wellbore storage causes early-time deviations in pressure data. It is characterized by rapid pressure changes due to fluid expansion or compression in the wellbore. Correcting for wellbore storage is vital for accurate permeability and skin estimation.",
            ["wellbore_storage_effects", "skin_factor_determination"],
            1.0
        ),
        SearchDocument(
            9,
            "Formation Interval Testing Procedures",
            "Formation interval tests isolate specific reservoir zones to evaluate their properties. These tests involve shutting in the well and monitoring pressure response, enabling estimation of permeability, skin, and fluid contacts.",
            ["formation_interval_testing", "permeability_estimation_methods"],
            1.0
        ),
        SearchDocument(
            10,
            "Interference and Pulse Testing Methodology",
            "Interference and pulse tests involve multiple wells to assess reservoir connectivity and transmissibility. Pressure changes in one well are monitored in another, providing insights into reservoir heterogeneity and boundaries.",
            ["interference_pulse_testing", "boundary_effect_identification"],
            1.0
        ),
        SearchDocument(
            11,
            "Drill Stem Test Interpretation Best Practices",
            "Drill stem tests (DST) provide valuable information about reservoir pressure, permeability, and fluid properties. Interpretation involves analyzing pressure buildup and drawdown data, often using Horner and derivative methods.",
            ["drill_stem_test_interpretation", "horner_buildup_analysis"],
            1.0
        ),
        SearchDocument(
            12,
            "Type Curve Matching Methodology Explained",
            "Type curve matching compares observed well test data to theoretical models. This technique helps identify reservoir parameters, flow regimes, and boundary effects. It is widely used in dual porosity and unconventional reservoir analysis.",
            ["type_curve_matching_methodology", "dual_porosity_interpretation"],
            1.0
        ),
        SearchDocument(
            13,
            "Superposition Principles in Well Test Analysis",
            "Superposition principles allow for the analysis of complex well test scenarios involving multiple flow periods or variable rates. By summing individual responses, analysts can interpret multi-rate and multi-well tests.",
            ["superposition_principles", "multi_rate_testing"],
            1.0
        ),
        SearchDocument(
            14,
            "Multi-Rate Testing and Interpretation",
            "Multi-rate tests involve changing the flow rate during a well test to enhance interpretation. Superposition and derivative analysis are used to extract permeability, skin, and boundary information from the resulting pressure data.",
            ["multi_rate_testing", "pressure_derivative_diagnostic_features"],
            1.0
        ),
        SearchDocument(
            15,
            "Permeability Estimation Methods in Well Testing",
            "Permeability estimation relies on analyzing pressure and rate data from well tests. Methods include Horner analysis, derivative techniques, and rate transient analysis. Accurate permeability estimation is crucial for reservoir management.",
            ["permeability_estimation_methods", "horner_buildup_analysis"],
            1.0
        ),
        SearchDocument(
            16,
            "Pressure Derivative Diagnostic Features",
            "Pressure derivative plots reveal diagnostic features such as wellbore storage, boundary effects, and flow regime transitions. Bourdet derivative analysis is commonly used to enhance interpretation.",
            ["pressure_derivative_diagnostic_features", "bourdet_derivative_analysis"],
            1.0
        ),
        SearchDocument(
            17,
            "Well Test Design and Duration Optimization",
            "Test design and duration impact the quality of well test interpretation. Proper planning ensures sufficient data for permeability, skin, and boundary identification. Factors include shut-in time, flow periods, and reservoir heterogeneity.",
            ["test_design_and_duration", "boundary_effect_identification"],
            1.0
        ),
        SearchDocument(
            18,
            "Advanced Horner Analysis for Complex Reservoirs",
            "Advanced Horner analysis adapts classical techniques for reservoirs with non-radial flow or significant wellbore storage. It integrates derivative and superposition principles for improved parameter estimation.",
            ["horner_buildup_analysis", "superposition_principles"],
            1.0
        ),
        SearchDocument(
            19,
            "Unconventional Well Testing: RTA and Type Curves",
            "Unconventional reservoirs require specialized well test interpretation. Rate transient analysis and type curve matching are used to estimate permeability, fracture properties, and boundary effects.",
            ["rate_transient_analysis_unconventional", "type_curve_matching_methodology"],
            1.0
        ),
        SearchDocument(
            20,
            "Matrix-Fracture Interaction in Dual Porosity Reservoirs",
            "Dual porosity reservoirs exhibit matrix-fracture interaction, affecting pressure response. Interpretation uses type curves and superposition to distinguish between flow regimes and estimate reservoir parameters.",
            ["dual_porosity_interpretation", "superposition_principles"],
            1.0
        ),
        SearchDocument(
            21,
            "Boundary Identification Using Derivative Analysis",
            "Derivative analysis is effective for boundary identification in well tests. Pressure derivative plots highlight deviations indicating faults, sealing boundaries, or reservoir limits.",
            ["boundary_effect_identification", "pressure_derivative_diagnostic_features"],
            1.0
        ),
        SearchDocument(
            22,
            "Horizontal Well Test Interpretation: Key Considerations",
            "Horizontal well tests require consideration of well length, reservoir anisotropy, and boundary effects. Superposition and derivative analysis are essential for accurate interpretation.",
            ["horizontal_well_testing", "superposition_principles"],
            1.0
        ),
        SearchDocument(
            23,
            "Wellbore Storage Correction Techniques",
            "Correcting for wellbore storage is necessary for early-time pressure data interpretation. Techniques include derivative analysis and specialized type curves to minimize errors in permeability and skin estimation.",
            ["wellbore_storage_effects", "pressure_derivative_diagnostic_features"],
            1.0
        ),
        SearchDocument(
            24,
            "Formation Interval Testing: Applications and Challenges",
            "Formation interval testing isolates reservoir zones to assess permeability, skin, and fluid contacts. Challenges include wellbore storage, boundary effects, and test design.",
            ["formation_interval_testing", "test_design_and_duration"],
            1.0
        ),
        SearchDocument(
            25,
            "Pulse Testing for Reservoir Connectivity",
            "Pulse tests involve alternating flow and shut-in periods to assess reservoir connectivity. Interpretation uses pressure response in observation wells to estimate transmissibility and boundary effects.",
            ["interference_pulse_testing", "boundary_effect_identification"],
            1.0
        ),
        SearchDocument(
            26,
            "DST Interpretation: Pressure Buildup and Drawdown",
            "Drill stem test interpretation focuses on pressure buildup and drawdown analysis. Techniques include Horner and derivative methods for permeability and skin estimation.",
            ["drill_stem_test_interpretation", "horner_buildup_analysis"],
            1.0
        ),
        SearchDocument(
            27,
            "Type Curve Matching for Dual Porosity Reservoirs",
            "Type curve matching is essential for interpreting dual porosity reservoirs. It distinguishes matrix and fracture contributions and aids in permeability estimation.",
            ["type_curve_matching_methodology", "dual_porosity_interpretation"],
            1.0
        ),
        SearchDocument(
            28,
            "Superposition in Multi-Rate Well Testing",
            "Superposition principles are applied in multi-rate well testing to analyze variable flow periods. This enhances parameter estimation and boundary identification.",
            ["superposition_principles", "multi_rate_testing"],
            1.0
        ),
        SearchDocument(
            29,
            "Multi-Rate Testing: Diagnostic Features",
            "Multi-rate testing reveals diagnostic features in pressure data. Derivative analysis and superposition are used to interpret flow regimes and boundaries.",
            ["multi_rate_testing", "pressure_derivative_diagnostic_features"],
            1.0
        ),
        SearchDocument(
            30,
            "Estimating Permeability from Well Test Data",
            "Permeability estimation uses Horner, derivative, and rate transient analysis. Accurate estimation requires correcting for wellbore storage and boundary effects.",
            ["permeability_estimation_methods", "horner_buildup_analysis"],
            1.0
        ),
        SearchDocument(
            31,
            "Pressure Derivative Analysis: Flow Regimes",
            "Pressure derivative analysis identifies flow regimes such as radial, linear, and boundary-dominated flow. Bourdet derivative is commonly used for diagnostic purposes.",
            ["pressure_derivative_diagnostic_features", "bourdet_derivative_analysis"],
            1.0
        ),
        SearchDocument(
            32,
            "Optimizing Well Test Design and Duration",
            "Well test design and duration are optimized to ensure reliable interpretation. Factors include shut-in time, flow periods, and reservoir heterogeneity.",
            ["test_design_and_duration", "boundary_effect_identification"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)