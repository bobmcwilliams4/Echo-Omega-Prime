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
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_tags: Dict[int, List[str]] = {}
        self.N = 0
        self.avg_doc_length = 0.0
        self.k1 = k1
        self.b = b
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for token in self.term_freqs[doc.id]:
                self.term_doc_freqs[token][doc.id] = self.term_freqs[doc.id][token]
            self.doc_tags[doc.id] = doc.tags
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for token in query_tokens:
            idf = self._compute_idf(token)
            docs_with_token = self.term_doc_freqs.get(token, {})
            for doc_id, freq in docs_with_token.items():
                score = self._score_bm25(token, doc_id, idf)
                doc_scores[doc_id] += score
        # TF-IDF scoring (normalized)
        tfidf_scores = self._tfidf_scores(query_tokens)
        for doc_id, tfidf_score in tfidf_scores.items():
            doc_scores[doc_id] += tfidf_score
        # Weight adjustment
        for doc_id in doc_scores:
            doc_scores[doc_id] *= self.documents[doc_id].weight
        # Sort and create results
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': self.N,
            'avg_doc_length': self.avg_doc_length,
            'num_terms': len(self.term_doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, token: str) -> float:
        if token in self._idf_cache:
            return self._idf_cache[token]
        df = len(self.term_doc_freqs.get(token, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[token] = idf
        return idf

    def _score_bm25(self, token: str, doc_id: int, idf: float) -> float:
        freq = self.term_freqs[doc_id][token]
        doc_length = self.doc_lengths[doc_id]
        denom = freq + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
        score = idf * (freq * (self.k1 + 1)) / (denom + 1e-10)
        return score

    def _tfidf_scores(self, query_tokens: List[str]) -> Dict[int, float]:
        scores = defaultdict(float)
        for token in query_tokens:
            idf = self._compute_idf(token)
            docs_with_token = self.term_doc_freqs.get(token, {})
            for doc_id, freq in docs_with_token.items():
                tf = freq / self.doc_lengths[doc_id]
                scores[doc_id] += tf * idf
        return scores

    def _make_snippet(self, content: str, query_tokens: List[str], window: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = ' '.join(tokens[:window])
        else:
            start = max(positions[0] - window // 2, 0)
            end = min(start + window, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet + '...'

    def _preseed(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1, "Thornhill-Craver Gas Lift Valve Equation",
                "The Thornhill-Craver equation describes the relationship between injection pressure, valve opening pressure, and flow rate in gas lift valves. It is fundamental for designing gas lift systems and optimizing valve performance.",
                ["gas_lift", "valve_equation", "thornhill_craver"], 1.2
            ),
            SearchDocument(
                2, "Injection Pressure Design and Gradient Matching",
                "Injection pressure design involves matching the pressure gradient of injected gas with the well's requirements. Proper gradient matching ensures efficient gas lift operation and prevents premature valve opening.",
                ["injection_pressure", "gradient_matching", "design"], 1.1
            ),
            SearchDocument(
                3, "Gas-Liquid Ratio (GLR) Optimization",
                "Optimizing the gas-liquid ratio (GLR) is crucial for maximizing production and minimizing gas usage. GLR optimization balances reservoir pressure, fluid properties, and lift efficiency.",
                ["glr", "optimization", "production"], 1.0
            ),
            SearchDocument(
                4, "Unloading Valve Spacing and Design",
                "Unloading valve spacing determines the sequence of gas injection during well startup. Proper design ensures smooth unloading, prevents backflow, and maintains well stability.",
                ["unloading_valve", "spacing", "design"], 1.0
            ),
            SearchDocument(
                5, "Continuous vs Intermittent Gas Lift Selection",
                "Gas lift can be operated in continuous or intermittent mode. Selection depends on well characteristics, production goals, and operational constraints.",
                ["continuous_gas_lift", "intermittent_gas_lift", "selection"], 1.0
            ),
            SearchDocument(
                6, "Gas Lift Kickoff Procedures",
                "Kickoff procedures initiate gas lift operations in a well. Proper kickoff ensures rapid unloading, minimizes formation damage, and optimizes startup efficiency.",
                ["kickoff", "procedures", "startup"], 1.0
            ),
            SearchDocument(
                7, "Gas Lift Troubleshooting - Flowing Pressure Surveys",
                "Flowing pressure surveys help diagnose gas lift problems such as valve malfunction, tubing leaks, or improper injection rates. Survey data guides corrective actions.",
                ["troubleshooting", "pressure_surveys", "diagnostics"], 1.0
            ),
            SearchDocument(
                8, "Plunger-Assisted Gas Lift",
                "Plunger-assisted gas lift combines plunger lift and gas lift techniques to enhance liquid removal and improve production in wells with low reservoir pressure.",
                ["plunger_lift", "gas_lift", "production"], 1.0
            ),
            SearchDocument(
                9, "Multi-Well Gas Allocation Optimization",
                "Optimizing gas allocation across multiple wells maximizes field production and minimizes compression costs. Allocation models consider well productivity, injection constraints, and economic factors.",
                ["multi_well", "allocation", "optimization"], 1.1
            ),
            SearchDocument(
                10, "Gas Lift Valve Types and Selection",
                "Various gas lift valve types exist, including bellows, stem, and pilot valves. Selection depends on well depth, injection pressure, and operational requirements.",
                ["valve_types", "selection", "gas_lift"], 1.0
            ),
            SearchDocument(
                11, "Gas Lift System Economics and Compression",
                "System economics evaluates gas lift costs, including gas supply, compression, and maintenance. Compression optimization reduces energy usage and improves profitability.",
                ["economics", "compression", "system"], 1.0
            ),
            SearchDocument(
                12, "Gas Lift Instability and Heading",
                "Instability and heading in gas lift systems cause production fluctuations and operational challenges. Diagnosis involves pressure monitoring and valve adjustment.",
                ["instability", "heading", "gas_lift"], 1.0
            ),
            SearchDocument(
                13, "Gas Lift System Monitoring and Performance Tracking",
                "Monitoring gas lift systems involves real-time data acquisition, pressure analysis, and performance tracking. Effective monitoring improves reliability and production.",
                ["monitoring", "performance_tracking", "gas_lift"], 1.0
            ),
            SearchDocument(
                14, "Valve Opening Pressure Calibration",
                "Calibration of valve opening pressure is essential for precise gas injection. Calibration procedures use test benches and pressure surveys to ensure accuracy.",
                ["calibration", "valve_opening", "pressure"], 1.0
            ),
            SearchDocument(
                15, "Tubing and Casing Pressure Management",
                "Managing tubing and casing pressures prevents gas migration, ensures valve integrity, and maintains well safety. Pressure management strategies include monitoring and control systems.",
                ["tubing_pressure", "casing_pressure", "management"], 1.0
            ),
            SearchDocument(
                16, "Gas Lift Design for Deep Wells",
                "Deep wells require specialized gas lift design, including high-pressure valves, reinforced tubing, and advanced injection strategies to overcome hydrostatic challenges.",
                ["deep_wells", "design", "gas_lift"], 1.0
            ),
            SearchDocument(
                17, "Gas Lift Optimization Using Reservoir Simulation",
                "Reservoir simulation models predict gas lift performance and guide optimization. Simulation integrates reservoir properties, injection schedules, and production forecasts.",
                ["simulation", "optimization", "reservoir"], 1.0
            ),
            SearchDocument(
                18, "Gas Lift Valve Malfunction Diagnosis",
                "Diagnosing valve malfunctions involves pressure surveys, acoustic monitoring, and flow analysis. Early detection prevents production losses and equipment damage.",
                ["valve_malfunction", "diagnosis", "gas_lift"], 1.0
            ),
            SearchDocument(
                19, "Gas Lift System Automation",
                "Automation in gas lift systems uses sensors, controllers, and algorithms to optimize injection rates and improve reliability. Automated systems reduce manual intervention.",
                ["automation", "gas_lift", "control"], 1.0
            ),
            SearchDocument(
                20, "Gas Lift in Marginal Wells",
                "Gas lift enables production from marginal wells with low reservoir pressure. Design considerations include minimal gas usage, cost-effective valve selection, and intermittent operation.",
                ["marginal_wells", "gas_lift", "production"], 1.0
            ),
            SearchDocument(
                21, "Gas Lift Compression System Design",
                "Compression system design ensures adequate gas supply for lift operations. Design factors include compressor sizing, pressure regulation, and safety controls.",
                ["compression", "system_design", "gas_lift"], 1.0
            ),
            SearchDocument(
                22, "Gas Lift System Safety and Environmental Considerations",
                "Safety and environmental considerations in gas lift systems include gas containment, leak prevention, and emissions monitoring. Compliance with regulations is essential.",
                ["safety", "environmental", "gas_lift"], 1.0
            ),
            SearchDocument(
                23, "Gas Lift Valve Selection for High-Pressure Applications",
                "High-pressure applications require robust valve designs, material selection, and precise calibration to ensure reliable operation and prevent failures.",
                ["valve_selection", "high_pressure", "gas_lift"], 1.0
            ),
            SearchDocument(
                24, "Gas Lift System Troubleshooting Guide",
                "Troubleshooting gas lift systems involves systematic diagnosis of injection problems, valve failures, and pressure anomalies. Guide includes common symptoms and solutions.",
                ["troubleshooting", "guide", "gas_lift"], 1.0
            ),
            SearchDocument(
                25, "Gas Lift System Performance Metrics",
                "Performance metrics for gas lift systems include injection efficiency, production rate, and downtime. Metrics guide optimization and maintenance strategies.",
                ["performance_metrics", "optimization", "gas_lift"], 1.0
            ),
            SearchDocument(
                26, "Gas Lift Valve Spacing Optimization",
                "Optimizing valve spacing improves unloading efficiency and prevents gas wastage. Spacing models consider well geometry, injection rates, and production targets.",
                ["valve_spacing", "optimization", "gas_lift"], 1.0
            ),
            SearchDocument(
                27, "Gas Lift System Data Analytics",
                "Data analytics in gas lift systems leverages historical and real-time data to identify trends, predict failures, and optimize injection schedules.",
                ["data_analytics", "gas_lift", "optimization"], 1.0
            ),
            SearchDocument(
                28, "Gas Lift System Integration with Field SCADA",
                "Integration with SCADA systems enables centralized monitoring and control of gas lift operations. SCADA interfaces provide alarms, reports, and remote access.",
                ["scada", "integration", "gas_lift"], 1.0
            ),
            SearchDocument(
                29, "Gas Lift System Maintenance Best Practices",
                "Maintenance best practices include regular valve inspection, pressure testing, and compressor servicing. Preventive maintenance reduces downtime and extends equipment life.",
                ["maintenance", "best_practices", "gas_lift"], 1.0
            ),
            SearchDocument(
                30, "Gas Lift System Retrofit Strategies",
                "Retrofit strategies upgrade existing gas lift systems with new valves, automation, and monitoring technologies to improve performance and reduce costs.",
                ["retrofit", "strategies", "gas_lift"], 1.0
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
            idx._preseed()
            _search_index_instance = idx
        return _search_index_instance