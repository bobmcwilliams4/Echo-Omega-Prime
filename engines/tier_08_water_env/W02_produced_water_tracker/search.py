import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.doc_tags: Dict[int, Set[str]] = {}
        self.doc_weights: Dict[int, float] = {}
        self.total_terms = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._avg_doc_length = 0.0

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            term_freq = Counter(tokens)
            self.documents[doc.id] = doc
            self.term_freqs[doc.id] = term_freq
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_tags[doc.id] = set(doc.tags)
            self.doc_weights[doc.id] = doc.weight
            self.total_terms += len(tokens)
            for term in term_freq:
                self.inverted_index[term].add(doc.id)
            self._idf_cache.clear()
            self._avg_doc_length = self.total_terms / max(1, len(self.documents))

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        candidate_docs = set()
        for term in query_tokens:
            candidate_docs |= self.inverted_index.get(term, set())
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            snippet = self._make_snippet(self.documents[doc_id], query_tokens)
            scored_results.append(SearchResult(doc_id, final_score, self.documents[doc_id].title, snippet))
        scored_results.sort(key=lambda x: (-x.score, x.title))
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": len(self.documents),
                "avg_doc_length": self._avg_doc_length,
                "vocab_size": len(self.inverted_index),
                "total_terms": self.total_terms
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        df = len(self.inverted_index.get(term, []))
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avgdl = self._avg_doc_length
        term_freq = self.term_freqs[doc_id]
        for term in query_tokens:
            if term not in term_freq:
                continue
            idf = self._compute_idf(term)
            tf = term_freq[term]
            numerator = tf * (self.bm25_k1 + 1)
            denominator = tf + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * doc_len / avgdl)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        term_freq = self.term_freqs[doc_id]
        tf_norm = {term: (term_freq[term] / doc_len) for term in term_freq}
        for term in query_tokens:
            if term not in term_freq:
                continue
            idf = self._compute_idf(term)
            score += tf_norm[term] * idf
        return score * doc.weight

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(r'\b({})\b'.format(re.escape(qt)), r'**\1**', snippet, flags=re.IGNORECASE)
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
            1,
            "Produced Water Volume Calculation",
            "Calculate produced water volumes using oil and gas production data, applying water cut and formation volume factors. Accurate volume tracking is essential for regulatory compliance and operational optimization.",
            ["volume", "calculation", "regulatory"], 1.0
        ),
        SearchDocument(
            2,
            "Water-Oil Ratio Analysis",
            "Analyze water-oil ratios (WOR) to assess reservoir performance, identify water breakthrough, and optimize water handling strategies. High WOR may indicate reservoir issues or coning.",
            ["analysis", "WOR", "reservoir"], 1.0
        ),
        SearchDocument(
            3,
            "Saltwater Disposal (SWD) Well Permitting",
            "Obtain SWD well permits by preparing RRC Form H-1, demonstrating disposal zone suitability, and meeting all regulatory requirements for injection and monitoring.",
            ["SWD", "permitting", "regulatory"], 1.0
        ),
        SearchDocument(
            4,
            "RRC Form H-1 Requirements",
            "Form H-1 is required for SWD well permitting in Texas. It includes data on well location, disposal interval, injection rates, and pressure limits.",
            ["RRC", "Form H-1", "SWD"], 1.0
        ),
        SearchDocument(
            5,
            "Disposal Well Capacity Determination",
            "Determine disposal well capacity by evaluating injection zone properties, pressure gradients, and historical injection data. Capacity impacts operational planning and cost.",
            ["capacity", "disposal", "well"], 1.0
        ),
        SearchDocument(
            6,
            "Injection Pressure Limits",
            "Monitor and enforce injection pressure limits to prevent formation fracturing and ensure safe disposal operations. Limits are set by regulatory agencies such as the RRC.",
            ["injection", "pressure", "limits"], 1.0
        ),
        SearchDocument(
            7,
            "Disposal Cost Modeling",
            "Model disposal costs by accounting for transportation, treatment, injection, and regulatory fees. Cost optimization requires accurate volume and logistics data.",
            ["cost", "modeling", "disposal"], 1.0
        ),
        SearchDocument(
            8,
            "Produced Water Recycling Economics",
            "Evaluate recycling economics by comparing treatment costs, reuse potential, and disposal savings. Recycling can reduce operational costs and environmental impact.",
            ["recycling", "economics", "reuse"], 1.0
        ),
        SearchDocument(
            9,
            "Water Transfer Pipeline Routing",
            "Optimize water transfer pipeline routes by considering topography, land use, permitting, and construction costs. Routing impacts project feasibility and OPEX.",
            ["pipeline", "routing", "transfer"], 1.0
        ),
        SearchDocument(
            10,
            "Disposal Well Network Optimization",
            "Optimize disposal well networks by balancing injection capacity, logistics, and regulatory constraints. Network models improve reliability and reduce costs.",
            ["network", "optimization", "disposal"], 1.0
        ),
        SearchDocument(
            11,
            "Produced Water Chemistry: TDS and Chlorides",
            "Analyze produced water chemistry, focusing on total dissolved solids (TDS) and chloride concentrations. Chemistry affects treatment selection and reuse feasibility.",
            ["chemistry", "TDS", "chlorides"], 1.0
        ),
        SearchDocument(
            12,
            "Frac Water Reuse Standards",
            "Meet frac water reuse standards by treating produced water to required quality levels. Standards are set by operators and regulatory agencies.",
            ["frac", "reuse", "standards"], 1.0
        ),
        SearchDocument(
            13,
            "Produced Water Hauling Logistics",
            "Plan produced water hauling by optimizing truck routes, scheduling, and disposal site selection. Logistics impact cost and regulatory compliance.",
            ["hauling", "logistics", "disposal"], 1.0
        ),
        SearchDocument(
            14,
            "RRC H-10 Reporting",
            "Submit RRC Form H-10 to report injection volumes, pressures, and well status for SWD operations. Accurate reporting is required for compliance.",
            ["RRC", "H-10", "reporting"], 1.0
        ),
        SearchDocument(
            15,
            "Formation Compatibility Assessment",
            "Assess formation compatibility by analyzing water chemistry and formation mineralogy. Compatibility prevents scaling, plugging, and formation damage.",
            ["formation", "compatibility", "assessment"], 1.0
        ),
        SearchDocument(
            16,
            "Injection Zone Pressure Monitoring",
            "Monitor injection zone pressure using downhole gauges and surface sensors. Pressure trends indicate formation response and potential interference.",
            ["injection", "pressure", "monitoring"], 1.0
        ),
        SearchDocument(
            17,
            "Water Cut Trending",
            "Track water cut trends to identify reservoir changes, optimize production, and plan water management strategies. Trending supports forecasting and diagnostics.",
            ["water cut", "trending", "forecasting"], 1.0
        ),
        SearchDocument(
            18,
            "Disposal Well Interference",
            "Evaluate disposal well interference by monitoring pressure communication and injection profiles. Interference can reduce well performance and capacity.",
            ["interference", "disposal", "well"], 1.0
        ),
        SearchDocument(
            19,
            "Produced Water Treatment Technologies",
            "Select produced water treatment technologies based on water chemistry, reuse goals, and disposal requirements. Technologies include filtration, chemical treatment, and evaporation.",
            ["treatment", "technologies", "produced water"], 1.0
        ),
        SearchDocument(
            20,
            "Produced Water Forecasting",
            "Forecast produced water volumes using decline curves, reservoir models, and production trends. Accurate forecasting informs infrastructure planning.",
            ["forecasting", "produced water", "planning"], 1.0
        ),
        SearchDocument(
            21,
            "Water Transfer Pipeline Permitting",
            "Obtain permits for water transfer pipelines by submitting route maps, environmental impact assessments, and construction plans to regulatory agencies.",
            ["pipeline", "permitting", "transfer"], 1.0
        ),
        SearchDocument(
            22,
            "Saltwater Disposal Well Integrity Testing",
            "Conduct integrity tests on SWD wells to ensure casing and cement integrity, preventing leaks and environmental contamination.",
            ["integrity", "testing", "SWD"], 1.0
        ),
        SearchDocument(
            23,
            "Disposal Well Siting Criteria",
            "Select disposal well sites based on geology, hydrology, regulatory setbacks, and proximity to produced water sources.",
            ["siting", "criteria", "disposal"], 1.0
        ),
        SearchDocument(
            24,
            "Produced Water Storage Tank Management",
            "Manage produced water storage tanks by monitoring levels, preventing overflows, and ensuring regulatory compliance.",
            ["storage", "tank", "management"], 1.0
        ),
        SearchDocument(
            25,
            "Water Hauling Cost Optimization",
            "Optimize water hauling costs by analyzing route efficiency, truck utilization, and disposal site selection.",
            ["hauling", "cost", "optimization"], 1.0
        ),
        SearchDocument(
            26,
            "Water Quality Monitoring for Reuse",
            "Monitor water quality parameters such as TDS, bacteria, and oil content to ensure suitability for reuse in hydraulic fracturing.",
            ["quality", "monitoring", "reuse"], 1.0
        ),
        SearchDocument(
            27,
            "Produced Water Evaporation Ponds",
            "Use evaporation ponds for produced water disposal where permitted, considering evaporation rates, liner integrity, and environmental controls.",
            ["evaporation", "ponds", "disposal"], 1.0
        ),
        SearchDocument(
            28,
            "Water Transfer Pump Station Design",
            "Design pump stations for water transfer systems, accounting for flow rates, pressure requirements, and reliability.",
            ["pump", "station", "design"], 1.0
        ),
        SearchDocument(
            29,
            "Regulatory Compliance for Produced Water",
            "Maintain regulatory compliance by tracking permits, reporting, and operational standards for produced water management.",
            ["regulatory", "compliance", "produced water"], 1.0
        ),
        SearchDocument(
            30,
            "Disposal Well Shut-In Procedures",
            "Follow shut-in procedures for disposal wells to prevent environmental incidents and maintain well integrity during downtime.",
            ["shut-in", "procedures", "disposal"], 1.0
        ),
        SearchDocument(
            31,
            "Produced Water Pipeline Leak Detection",
            "Implement leak detection systems in produced water pipelines using pressure monitoring, flow balance, and remote sensing.",
            ["pipeline", "leak", "detection"], 1.0
        ),
        SearchDocument(
            32,
            "Water Cut Measurement Techniques",
            "Measure water cut using test separators, Coriolis meters, and inline sensors to support accurate volume reporting.",
            ["water cut", "measurement", "techniques"], 1.0
        ),
        SearchDocument(
            33,
            "Disposal Well Step Rate Testing",
            "Perform step rate tests on disposal wells to determine formation parting pressure and optimize injection rates.",
            ["step rate", "testing", "disposal"], 1.0
        ),
        SearchDocument(
            34,
            "Produced Water Blending for Reuse",
            "Blend produced water with fresh or brackish water to meet reuse quality standards for hydraulic fracturing.",
            ["blending", "reuse", "produced water"], 1.0
        ),
        SearchDocument(
            35,
            "SWD Well Annular Pressure Monitoring",
            "Monitor annular pressure in SWD wells to detect casing leaks and maintain well integrity.",
            ["annular", "pressure", "SWD"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)