import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_map: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}
        self._preseeded = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_doc_freq[term] += 1
                self.term_doc_map[term][doc.id] = freq
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tokens = self._tokenize(doc.content)
        doc_len = len(tokens)
        score = 0.0
        term_counts = Counter(tokens)
        for term in query_terms:
            idf = self._compute_idf(term)
            freq = term_counts.get(term, 0)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            bm25 = idf * (numerator / (denominator or 1))
            score += bm25
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_map = self._tfidf_cache[doc_id]
        else:
            doc = self.documents[doc_id]
            tokens = self._tokenize(doc.content)
            doc_len = len(tokens)
            term_counts = Counter(tokens)
            tfidf_map = {}
            for term in set(tokens):
                tf = term_counts[term] / (doc_len or 1)
                idf = self._compute_idf(term)
                tfidf_map[term] = tf * idf
            self._tfidf_cache[doc_id] = tfidf_map
        score = sum(tfidf_map.get(term, 0.0) for term in query_terms)
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0.0:
                doc_scores.append((doc_id, score))
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in doc_scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet + ('...' if end < len(tokens) else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

    def preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1, "Artificial Lift Selection Matrix",
                "Comprehensive matrix for selecting artificial lift methods based on reservoir properties, production rates, and operational constraints. Includes gas lift, rod pump, ESP, and hydraulic pump options.",
                ["artificial_lift", "selection_matrix", "optimization"], 1.0
            ),
            SearchDocument(
                2, "Gas Lift Optimization: Injection Rate",
                "Optimizing gas injection rate for gas lift wells to maximize production efficiency. Analysis of injection performance, gas utilization, and lift efficiency.",
                ["gas_lift", "injection_rate", "optimization"], 1.0
            ),
            SearchDocument(
                3, "Gas Lift Valve Spacing Design",
                "Guidelines for designing valve spacing in gas lift operations. Covers depth selection, pressure profiles, and operational flexibility.",
                ["gas_lift", "valve_spacing", "design"], 1.0
            ),
            SearchDocument(
                4, "Rod Pump Optimization: Pump Speed",
                "Strategies for optimizing rod pump speed to balance production rate and equipment longevity. Includes vibration analysis and pump-off control.",
                ["rod_pump", "pump_speed", "optimization"], 1.0
            ),
            SearchDocument(
                5, "Rod Pump Stroke Length Adjustment",
                "Impact of stroke length on rod pump performance. Recommendations for adjusting stroke length based on well conditions and fluid properties.",
                ["rod_pump", "stroke_length", "performance"], 1.0
            ),
            SearchDocument(
                6, "ESP Optimization: Frequency Control",
                "Optimizing ESP frequency for variable production rates. Discusses motor efficiency, pump curve matching, and electrical considerations.",
                ["esp", "frequency", "optimization"], 1.0
            ),
            SearchDocument(
                7, "ESP Staging and Well Performance",
                "Designing ESP staging for multi-zone production. Covers pump selection, stage configuration, and well productivity enhancement.",
                ["esp", "staging", "well_performance"], 1.0
            ),
            SearchDocument(
                8, "Wellbore Integrity Monitoring: Leak Detection",
                "Techniques for monitoring wellbore integrity and detecting casing and tubing leaks. Includes pressure testing, acoustic monitoring, and fiber optic sensing.",
                ["wellbore_integrity", "leak_detection", "monitoring"], 1.0
            ),
            SearchDocument(
                9, "Scale Management: Calcium Carbonate Control",
                "Methods for preventing and removing calcium carbonate scale in production wells. Chemical inhibition, mechanical removal, and predictive modeling.",
                ["scale_management", "calcium_carbonate", "control"], 1.0
            ),
            SearchDocument(
                10, "Scale Management: Barium Sulfate and Iron Sulfide",
                "Approaches for managing barium sulfate and iron sulfide scale. Treatment options, risk assessment, and impact on production equipment.",
                ["scale_management", "barium_sulfate", "iron_sulfide"], 1.0
            ),
            SearchDocument(
                11, "Paraffin Management in Production Wells",
                "Best practices for paraffin prevention and removal. Thermal, chemical, and mechanical methods for maintaining flow assurance.",
                ["paraffin_management", "flow_assurance", "production"], 1.0
            ),
            SearchDocument(
                12, "Asphaltene Management Strategies",
                "Strategies for controlling asphaltene deposition in oil wells. Includes solvent injection, dispersant use, and predictive analysis.",
                ["asphaltene_management", "deposition", "control"], 1.0
            ),
            SearchDocument(
                13, "Corrosion Monitoring Programs",
                "Designing corrosion monitoring programs for production operations. Covers corrosion coupons, electrical resistance probes, and real-time monitoring.",
                ["corrosion_monitoring", "production", "programs"], 1.0
            ),
            SearchDocument(
                14, "Corrosion Inhibition Techniques",
                "Overview of corrosion inhibition methods. Selection of inhibitors, injection strategies, and performance evaluation.",
                ["corrosion_inhibition", "techniques", "evaluation"], 1.0
            ),
            SearchDocument(
                15, "Production Surveillance: Well Testing",
                "Principles and practices of well testing for production surveillance. Includes pressure transient analysis, flow rate measurement, and allocation.",
                ["production_surveillance", "well_testing", "allocation"], 1.0
            ),
            SearchDocument(
                16, "Production Allocation Methods",
                "Methods for allocating production among multiple wells. Covers allocation algorithms, uncertainty analysis, and regulatory compliance.",
                ["production_allocation", "methods", "compliance"], 1.0
            ),
            SearchDocument(
                17, "Well Intervention Planning: Workover",
                "Planning workover operations for well intervention. Decision criteria, cost analysis, and risk management.",
                ["well_intervention", "workover", "planning"], 1.0
            ),
            SearchDocument(
                18, "Well Intervention: Stimulation Techniques",
                "Stimulation techniques for enhancing well productivity. Acidizing, hydraulic fracturing, and matrix treatments.",
                ["well_intervention", "stimulation", "productivity"], 1.0
            ),
            SearchDocument(
                19, "Recompletion Strategies for Mature Wells",
                "Recompletion options for mature wells. Includes zone isolation, sidetracking, and completion redesign.",
                ["recompletion", "mature_wells", "strategies"], 1.0
            ),
            SearchDocument(
                20, "Facility Optimization: Separator Pressure",
                "Optimizing separator pressure for maximum oil and gas recovery. Covers pressure control, phase separation, and equipment sizing.",
                ["facility_optimization", "separator_pressure", "recovery"], 1.0
            ),
            SearchDocument(
                21, "Facility Optimization: Separator Temperature",
                "Impact of separator temperature on oil and gas separation efficiency. Recommendations for temperature control and heat integration.",
                ["facility_optimization", "separator_temperature", "efficiency"], 1.0
            ),
            SearchDocument(
                22, "Gas Gathering System Optimization: Compression",
                "Optimizing compression in gas gathering systems. Compressor selection, pressure balancing, and energy efficiency.",
                ["gas_gathering", "compression", "optimization"], 1.0
            ),
            SearchDocument(
                23, "Gas Gathering System: Pipeline Sizing",
                "Pipeline sizing for gas gathering systems. Hydraulic calculations, flow assurance, and material selection.",
                ["gas_gathering", "pipeline_sizing", "flow_assurance"], 1.0
            ),
            SearchDocument(
                24, "Produced Water Handling: Separation and Treatment",
                "Techniques for separating and treating produced water. Covers oil-water separation, filtration, and chemical treatment.",
                ["produced_water", "separation", "treatment"], 1.0
            ),
            SearchDocument(
                25, "Produced Water Disposal Options",
                "Options for disposing produced water. Injection, evaporation, and regulatory requirements.",
                ["produced_water", "disposal", "regulatory"], 1.0
            ),
            SearchDocument(
                26, "ESG Metrics in Production Operations",
                "Environmental, social, and governance metrics for production operations. Emissions monitoring, water management, and community impact assessment.",
                ["esg_metrics", "production_operations", "emissions"], 1.0
            ),
            SearchDocument(
                27, "Emissions Reduction Strategies",
                "Strategies for reducing emissions in oil and gas production. Includes flare minimization, methane capture, and carbon footprint analysis.",
                ["emissions_reduction", "production", "strategies"], 1.0
            ),
            SearchDocument(
                28, "Water Management in Production",
                "Best practices for water management in oil and gas production. Recycling, reuse, and minimizing environmental impact.",
                ["water_management", "production", "environmental"], 1.0
            ),
            SearchDocument(
                29, "Community Impact of Oil Production",
                "Assessing and mitigating community impact from oil production operations. Stakeholder engagement, impact studies, and sustainable development.",
                ["community_impact", "oil_production", "sustainability"], 1.0
            ),
            SearchDocument(
                30, "Hydraulic Pump Optimization",
                "Optimizing hydraulic pump operations for artificial lift. Includes pump selection, fluid power calculations, and maintenance strategies.",
                ["hydraulic_pump", "optimization", "artificial_lift"], 1.0
            ),
            SearchDocument(
                31, "Fiber Optic Sensing in Well Integrity",
                "Application of fiber optic sensing for real-time well integrity monitoring. Leak detection, temperature profiling, and pressure analysis.",
                ["fiber_optic", "well_integrity", "monitoring"], 1.0
            ),
            SearchDocument(
                32, "Predictive Modeling for Scale Formation",
                "Using predictive modeling to forecast scale formation in wells. Data-driven approaches, machine learning, and risk mitigation.",
                ["predictive_modeling", "scale_formation", "risk"], 1.0
            ),
            SearchDocument(
                33, "Pump-Off Control in Rod Pump Systems",
                "Implementing pump-off control to optimize rod pump operations. Sensor integration, automation, and production maximization.",
                ["pump_off_control", "rod_pump", "automation"], 1.0
            ),
            SearchDocument(
                34, "Separator Sizing for Facility Optimization",
                "Guidelines for sizing separators in production facilities. Capacity calculations, efficiency factors, and operational flexibility.",
                ["separator_sizing", "facility_optimization", "guidelines"], 1.0
            ),
            SearchDocument(
                35, "Regulatory Compliance in Produced Water Disposal",
                "Ensuring regulatory compliance in produced water disposal. Permitting, reporting, and environmental protection.",
                ["regulatory_compliance", "produced_water", "disposal"], 1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            idx = SearchIndex()
            idx.preseed_documents()
            _search_index_instance = idx
        return _search_index_instance