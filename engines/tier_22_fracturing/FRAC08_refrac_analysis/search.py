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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_terms = 0
        self.lock = threading.Lock()
        self.avg_doc_length = 0.0
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            term_counts = Counter(tokens)
            self.term_freqs[doc.id] = term_counts
            for term in term_counts:
                self.term_doc_freqs[term] += 1
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / len(self.doc_lengths)
                if self.doc_lengths else 0.0
            )

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freqs.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        if doc_id in self._tfidf_cache and all(term in self._tfidf_cache[doc_id] for term in query_terms):
            return sum(self._tfidf_cache[doc_id][term] for term in query_terms)
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            norm_tf = tf / doc_len
            idf = self._compute_idf(term)
            tfidf = norm_tf * idf
            self._tfidf_cache[doc_id][term] = tfidf
            score += tfidf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(doc_id, query_terms)
            else:
                score = self._score_bm25(doc_id, query_terms)
            if score > 0:
                doc_scores.append((doc_id, score))
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in doc_scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 40) -> str:
        tokens = self._tokenize(doc.content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return doc.content[:window*2] + ('...' if len(doc.content) > window*2 else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + ('...' if end < len(tokens) else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'total_terms': self.total_terms,
            'unique_terms': len(self.term_doc_freqs)
        }

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
            1,
            "Production Decline Analysis for Refrac Candidates",
            "Detailed decline curve analysis (DCA) is used to identify wells with rapid production drop-off, indicating potential for refrac. Methods include Arps, stretched exponential, and machine learning-based DCA.",
            ["production", "decline", "refrac", "DCA"],
            1.2
        ),
        SearchDocument(
            2,
            "Stress Reorientation Theory in Refrac Operations",
            "Refrac can alter stress fields in the reservoir, reorienting fracture propagation. Understanding local stress changes is crucial for optimizing refrac effectiveness and avoiding interference with existing fractures.",
            ["stress", "reorientation", "fracture", "refrac"],
            1.0
        ),
        SearchDocument(
            3,
            "Mechanical Diversion: Bridge Plugs and Composite Plugs",
            "Bridge plugs and composite plugs are used for mechanical diversion during refrac. They isolate zones to ensure new fractures are created in previously untreated intervals.",
            ["mechanical", "diversion", "bridge plug", "composite plug", "refrac"],
            1.1
        ),
        SearchDocument(
            4,
            "Chemical Diversion Techniques for Refrac",
            "Chemical diverters, such as particulate slurries and polymer gels, temporarily block existing fractures, enabling refrac treatments to access new reservoir rock.",
            ["chemical", "diversion", "refrac", "polymer", "gel"],
            1.0
        ),
        SearchDocument(
            5,
            "Bullhead Refrac Technique Overview",
            "Bullhead refrac involves pumping treatment fluid directly down the casing without isolating individual intervals. This technique is cost-effective but may have limited diversion control.",
            ["bullhead", "refrac", "casing", "diversion"],
            0.9
        ),
        SearchDocument(
            6,
            "Economic Analysis: Refrac vs New Drill Decision",
            "Economic models compare refrac costs and incremental EUR to new well drilling. Factors include capital expenditure, expected production uplift, and risk of failure.",
            ["economic", "analysis", "refrac", "new drill", "EUR"],
            1.3
        ),
        SearchDocument(
            7,
            "Production History Analysis for Refrac Timing",
            "Analyzing production history helps determine optimal refrac timing. Key indicators include rate decline, water cut increase, and pressure behavior.",
            ["production", "history", "timing", "refrac"],
            1.0
        ),
        SearchDocument(
            8,
            "Casing Integrity Assessment Before Refrac",
            "Casing inspection using caliper logs, pressure tests, and ultrasonic imaging ensures wellbore integrity before refrac. Identifying leaks or deformation is critical.",
            ["casing", "integrity", "assessment", "refrac"],
            1.2
        ),
        SearchDocument(
            9,
            "Refrac Flowback Protocols",
            "Flowback protocols after refrac involve gradual pressure reduction and monitoring for sand production. Proper flowback prevents screenout and protects well integrity.",
            ["flowback", "protocol", "refrac", "screenout"],
            1.0
        ),
        SearchDocument(
            10,
            "Permian Basin Horizontal Well Refrac Case Studies",
            "Case studies from the Permian Basin highlight refrac best practices, including candidate selection, diversion methods, and incremental EUR results.",
            ["case study", "Permian Basin", "horizontal", "refrac"],
            1.1
        ),
        SearchDocument(
            11,
            "Refrac Pump Schedule Design",
            "Pump schedule design for refrac considers fluid volumes, rates, and stage sequencing. Optimizing schedule improves fracture geometry and production response.",
            ["pump", "schedule", "design", "refrac"],
            1.0
        ),
        SearchDocument(
            12,
            "Refrac Risk Assessment: Screenout and Casing Failure",
            "Risk assessment for refrac includes evaluating screenout probability and casing failure risk. Mitigation strategies involve diversion, pressure management, and real-time monitoring.",
            ["risk", "assessment", "screenout", "casing", "refrac"],
            1.2
        ),
        SearchDocument(
            13,
            "Refrac Through Existing Perforations vs New Perforations",
            "Choosing between refrac through existing or new perforations impacts fracture placement and production. New perforations may access bypassed zones, while existing ones reduce operational complexity.",
            ["perforation", "existing", "new", "refrac"],
            1.0
        ),
        SearchDocument(
            14,
            "Production History DCA Methodology for Refrac Selection",
            "Applying decline curve analysis to production history enables systematic refrac candidate selection. Models include hyperbolic, exponential, and hybrid approaches.",
            ["DCA", "production", "history", "refrac", "selection"],
            1.1
        ),
        SearchDocument(
            15,
            "Degraded Cement Evaluation Before Refrac",
            "Cement integrity evaluation before refrac uses sonic logs and cement bond logs to detect degradation. Remediation may be required for successful refrac.",
            ["cement", "degradation", "evaluation", "refrac"],
            1.0
        ),
        SearchDocument(
            16,
            "Refrac Incremental EUR Forecasting Methods",
            "Incremental EUR forecasting for refrac employs statistical models, analog well comparison, and machine learning to predict production uplift.",
            ["EUR", "forecasting", "incremental", "refrac"],
            1.2
        ),
        SearchDocument(
            17,
            "Frac08 Engine: Refrac Candidate Selection Workflow",
            "FRAC08 engine integrates production decline analysis, stress reorientation, and economic modeling for refrac candidate selection. Workflow includes screening, risk assessment, and scheduling.",
            ["FRAC08", "candidate", "workflow", "refrac"],
            1.3
        ),
        SearchDocument(
            18,
            "Machine Learning in Refrac Candidate Selection",
            "Machine learning models analyze production, completion, and reservoir data to improve refrac candidate selection accuracy. Features include decline rates, completion quality, and reservoir heterogeneity.",
            ["machine learning", "candidate", "selection", "refrac"],
            1.2
        ),
        SearchDocument(
            19,
            "Reservoir Characterization for Refrac Planning",
            "Reservoir properties such as porosity, permeability, and stress regime are evaluated to optimize refrac design and maximize incremental EUR.",
            ["reservoir", "characterization", "planning", "refrac"],
            1.0
        ),
        SearchDocument(
            20,
            "Hydraulic Fracture Modeling for Refrac",
            "Hydraulic fracture modeling predicts fracture geometry and interaction with existing fractures. Simulation tools help design refrac treatments for improved reservoir contact.",
            ["hydraulic", "fracture", "modeling", "refrac"],
            1.1
        ),
        SearchDocument(
            21,
            "Refrac Candidate Screening Criteria",
            "Screening criteria for refrac candidates include production decline rate, completion quality, reservoir properties, and economic potential.",
            ["candidate", "screening", "criteria", "refrac"],
            1.2
        ),
        SearchDocument(
            22,
            "Completion Quality Assessment Before Refrac",
            "Completion quality is assessed using production logs, pressure profiles, and fracture diagnostics to identify wells suitable for refrac.",
            ["completion", "quality", "assessment", "refrac"],
            1.0
        ),
        SearchDocument(
            23,
            "Pressure Management During Refrac Operations",
            "Pressure management during refrac includes real-time monitoring, pump schedule optimization, and diversion techniques to minimize risk and maximize production.",
            ["pressure", "management", "operation", "refrac"],
            1.1
        ),
        SearchDocument(
            24,
            "Refrac Candidate Selection in Tight Oil Reservoirs",
            "Tight oil reservoirs require specialized refrac candidate selection methods, including advanced DCA, reservoir modeling, and economic analysis.",
            ["tight oil", "candidate", "selection", "refrac"],
            1.2
        ),
        SearchDocument(
            25,
            "Frac08 Engine: Economic Modeling for Refrac",
            "FRAC08 engine provides economic modeling tools for refrac, including cost estimation, incremental EUR forecasting, and risk analysis.",
            ["FRAC08", "economic", "modeling", "refrac"],
            1.3
        ),
        SearchDocument(
            26,
            "Refrac Diversion Technology Comparison",
            "Comparison of mechanical and chemical diversion technologies for refrac, including bridge plugs, composite plugs, and polymer diverters.",
            ["diversion", "technology", "comparison", "refrac"],
            1.1
        ),
        SearchDocument(
            27,
            "Refrac Candidate Selection: Data Requirements",
            "Data requirements for refrac candidate selection include production history, completion records, reservoir characterization, and economic parameters.",
            ["candidate", "selection", "data", "refrac"],
            1.0
        ),
        SearchDocument(
            28,
            "Refrac Treatment Design Optimization",
            "Optimization of refrac treatment design involves stage sequencing, fluid selection, and diversion planning to maximize production uplift.",
            ["treatment", "design", "optimization", "refrac"],
            1.1
        ),
        SearchDocument(
            29,
            "Wellbore Preparation for Refrac",
            "Wellbore preparation before refrac includes cleaning, casing inspection, and plug installation to ensure successful treatment.",
            ["wellbore", "preparation", "casing", "refrac"],
            1.0
        ),
        SearchDocument(
            30,
            "Refrac Candidate Selection: Permian Basin Insights",
            "Permian Basin refrac candidate selection leverages regional production trends, completion practices, and reservoir heterogeneity.",
            ["Permian Basin", "candidate", "selection", "refrac"],
            1.2
        ),
        SearchDocument(
            31,
            "Refrac Candidate Selection: Decline Curve Screening",
            "Decline curve screening for refrac candidates uses hyperbolic and exponential models to identify wells with high incremental EUR potential.",
            ["decline curve", "screening", "refrac"],
            1.1
        ),
        SearchDocument(
            32,
            "Refrac Candidate Selection: Risk Mitigation Strategies",
            "Risk mitigation strategies for refrac candidate selection include casing integrity checks, diversion planning, and real-time monitoring.",
            ["risk", "mitigation", "candidate", "selection", "refrac"],
            1.2
        ),
        SearchDocument(
            33,
            "Refrac Candidate Selection: Machine Learning Workflow",
            "Machine learning workflow for refrac candidate selection integrates data preprocessing, feature engineering, and predictive modeling.",
            ["machine learning", "workflow", "candidate", "selection", "refrac"],
            1.2
        ),
        SearchDocument(
            34,
            "Refrac Candidate Selection: Economic Screening",
            "Economic screening for refrac candidate selection evaluates cost-benefit ratio, incremental EUR, and risk-adjusted returns.",
            ["economic", "screening", "candidate", "selection", "refrac"],
            1.3
        ),
        SearchDocument(
            35,
            "Refrac Candidate Selection: Casing Integrity Evaluation",
            "Casing integrity evaluation for refrac candidate selection uses caliper logs, pressure tests, and ultrasonic imaging.",
            ["casing", "integrity", "candidate", "selection", "refrac"],
            1.2
        ),
    ]
    for doc in docs:
        index.add_document(doc)