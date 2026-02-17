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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = defaultdict(list)  # term -> list of (doc_id, freq)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            freq = Counter(tokens)
            self.doc_lengths[doc.id] = len(tokens)
            for term, count in freq.items():
                self.inverted_index[term].append((doc.id, count))
                self.doc_freqs[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, query_tf: Counter) -> float:
        doc = self.documents[doc_id]
        doc_tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
        doc_tf = Counter(doc_tokens)
        score = 0.0
        for term in query_terms:
            if term not in doc_tf:
                continue
            idf = self._compute_idf(term)
            tf = doc_tf[term]
            norm = (1 - self.b) + self.b * (self.doc_lengths[doc_id] / self.avg_doc_length if self.avg_doc_length else 1)
            bm25 = idf * ((tf * (self.k1 + 1)) / (tf + self.k1 * norm))
            score += bm25
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int, query_tf: Counter) -> float:
        doc = self.documents[doc_id]
        doc_tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
        doc_tf = Counter(doc_tokens)
        score = 0.0
        for term in query_terms:
            tf = doc_tf.get(term, 0)
            if tf == 0:
                continue
            df = self.doc_freqs.get(term, 1)
            idf = math.log((self.total_docs + 1) / df)
            norm_tf = tf / len(doc_tokens) if len(doc_tokens) else 0
            score += norm_tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        query_tf = Counter(query_terms)
        candidate_docs = set()
        for term in query_terms:
            postings = self.inverted_index.get(term, [])
            for doc_id, _ in postings:
                candidate_docs.add(doc_id)
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id, query_tf)
            tfidf_score = self._score_tfidf(query_terms, doc_id, query_tf)
            score = bm25_score + 0.5 * tfidf_score
            snippet = self._make_snippet(self.documents[doc_id], query_terms)
            scored_results.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:snippet_len]
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + 30, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
            for term in set(query_terms):
                snippet = re.sub(rf'(\b{re.escape(term)}\b)', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:snippet_len] + ('...' if len(snippet) > snippet_len else '')

    def get_stats(self) -> Dict[str, int]:
        return {
            'documents': self.total_docs,
            'unique_terms': len(self.inverted_index),
            'avg_doc_length': int(self.avg_doc_length)
        }

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Fixed vs Variable Displacement Pumps",
            "Fixed displacement pumps deliver a constant flow at a given speed, while variable displacement pumps allow flow adjustment. Variable pumps are preferred for energy efficiency and precise control in hydraulic systems.",
            ["hydraulic", "pump", "selection", "fixed", "variable"],
            1.0
        ),
        SearchDocument(
            2,
            "Hydraulic Cylinder Sizing: Bore and Rod Selection",
            "Choosing the correct bore and rod diameter is essential for hydraulic cylinder performance. Bore size determines force output, while rod diameter affects buckling resistance and retraction speed.",
            ["hydraulic", "cylinder", "sizing", "bore", "rod"],
            1.0
        ),
        SearchDocument(
            3,
            "Directional Control Valves: Spool vs Poppet",
            "Spool valves offer smooth operation and are suited for precise control, whereas poppet valves provide tight sealing and are ideal for high-pressure applications. Selection depends on system requirements.",
            ["directional", "control", "valve", "spool", "poppet"],
            1.0
        ),
        SearchDocument(
            4,
            "Hydraulic Fluid Selection: ISO VG Grades",
            "ISO VG (Viscosity Grade) classification helps select hydraulic fluids based on operating temperature and system requirements. Proper fluid selection ensures lubrication, efficiency, and component life.",
            ["hydraulic", "fluid", "iso", "vg", "selection"],
            1.0
        ),
        SearchDocument(
            5,
            "Contamination Control: ISO 4406 Cleanliness Codes",
            "ISO 4406 codes classify hydraulic fluid cleanliness by counting particles of different sizes. Maintaining cleanliness with proper filtration is critical for system reliability and longevity.",
            ["contamination", "control", "iso", "4406", "filtration"],
            1.0
        ),
        SearchDocument(
            6,
            "Hydraulic Circuit Design: Open vs Closed Center",
            "Open center circuits allow flow when valves are neutral, minimizing heat. Closed center systems block flow in neutral, enabling multiple simultaneous operations and energy savings.",
            ["hydraulic", "circuit", "design", "open", "closed"],
            1.0
        ),
        SearchDocument(
            7,
            "Accumulator Sizing: Bladder and Piston Types",
            "Accumulators store energy in hydraulic systems. Bladder types offer rapid response, while piston accumulators are suitable for higher volumes and pressures. Proper sizing ensures system stability.",
            ["accumulator", "sizing", "bladder", "piston", "energy"],
            1.0
        ),
        SearchDocument(
            8,
            "Pressure Drop and Heat Generation",
            "Excessive pressure drop in hydraulic systems leads to heat generation, reducing efficiency and component life. Proper line sizing and flow control minimize losses.",
            ["pressure", "drop", "heat", "generation", "efficiency"],
            1.0
        ),
        SearchDocument(
            9,
            "Electrohydraulic Motion Control: Proportional and Servo Valves",
            "Proportional valves provide variable control of flow and pressure, while servo valves enable precise, high-speed motion control. Selection depends on accuracy, response, and cost.",
            ["electrohydraulic", "motion", "control", "proportional", "servo"],
            1.0
        ),
        SearchDocument(
            10,
            "Hydraulic System Troubleshooting: Diagnostics",
            "Effective troubleshooting involves systematic checks: verifying pressure, flow, temperature, and contamination. Diagnostic tools include pressure gauges, flow meters, and oil analysis kits.",
            ["hydraulic", "system", "troubleshooting", "diagnostics"],
            1.0
        ),
        SearchDocument(
            11,
            "Predictive Maintenance: Oil Analysis and Vibration Monitoring",
            "Predictive maintenance uses oil analysis to detect wear particles and vibration monitoring to identify mechanical issues before failure, reducing downtime and repair costs.",
            ["predictive", "maintenance", "oil", "analysis", "vibration"],
            1.0
        ),
        SearchDocument(
            12,
            "Hydraulic Pump Efficiency",
            "Pump efficiency is affected by internal leakage, fluid viscosity, and operating pressure. Variable displacement pumps can improve efficiency under varying load conditions.",
            ["hydraulic", "pump", "efficiency", "variable"],
            1.0
        ),
        SearchDocument(
            13,
            "Cylinder Speed and Flow Requirements",
            "Cylinder speed is determined by flow rate and effective area. Accurate sizing ensures desired motion profiles and prevents system overloading.",
            ["cylinder", "speed", "flow", "sizing"],
            1.0
        ),
        SearchDocument(
            14,
            "Valve Response Time in Motion Control",
            "Servo valves offer faster response times than proportional valves, critical for applications requiring high-precision and rapid actuation.",
            ["valve", "response", "servo", "proportional"],
            1.0
        ),
        SearchDocument(
            15,
            "Hydraulic Fluid Types: Mineral vs Synthetic",
            "Mineral oils are common in hydraulics, but synthetic fluids offer better temperature stability, oxidation resistance, and extended service life.",
            ["hydraulic", "fluid", "mineral", "synthetic"],
            1.0
        ),
        SearchDocument(
            16,
            "Filtration Methods in Contamination Control",
            "Filtration removes particles from hydraulic fluid. Common methods include pressure, return, and off-line filtration. Filter selection is based on ISO 4406 cleanliness targets.",
            ["filtration", "contamination", "iso", "4406"],
            1.0
        ),
        SearchDocument(
            17,
            "Accumulator Precharge and Maintenance",
            "Proper precharge pressure is essential for accumulator performance. Routine checks prevent bladder or piston failure and maintain energy storage capacity.",
            ["accumulator", "precharge", "maintenance"],
            1.0
        ),
        SearchDocument(
            18,
            "Heat Exchangers in Hydraulic Systems",
            "Heat exchangers dissipate excess heat generated by pressure drops and friction. Sizing is based on system flow, temperature rise, and ambient conditions.",
            ["heat", "exchanger", "hydraulic", "cooling"],
            1.0
        ),
        SearchDocument(
            19,
            "Open Center Circuit Applications",
            "Open center circuits are common in mobile hydraulics, offering simplicity and low cost. They are ideal where simultaneous actuator operation is not required.",
            ["open", "center", "circuit", "mobile"],
            1.0
        ),
        SearchDocument(
            20,
            "Closed Center Circuit Advantages",
            "Closed center circuits allow multiple actuators to operate independently, improving efficiency and control in industrial hydraulic systems.",
            ["closed", "center", "circuit", "industrial"],
            1.0
        ),
        SearchDocument(
            21,
            "Hydraulic Cylinder Buckling and Safety",
            "Rod diameter must be selected to prevent buckling under compressive loads. Euler's formula is used to calculate critical load for safe operation.",
            ["hydraulic", "cylinder", "buckling", "safety"],
            1.0
        ),
        SearchDocument(
            22,
            "Servo Valve Maintenance",
            "Servo valves require clean fluid and regular maintenance to prevent contamination-related failures. Fine filtration and scheduled inspections are recommended.",
            ["servo", "valve", "maintenance", "filtration"],
            1.0
        ),
        SearchDocument(
            23,
            "Hydraulic System Diagnostics: Common Faults",
            "Common hydraulic faults include leaks, slow actuator movement, overheating, and abnormal noises. Systematic diagnostics help isolate and correct issues.",
            ["hydraulic", "system", "diagnostics", "faults"],
            1.0
        ),
        SearchDocument(
            24,
            "Vibration Analysis in Predictive Maintenance",
            "Vibration analysis detects imbalance, misalignment, and bearing wear in hydraulic machinery, enabling proactive maintenance and reducing unplanned downtime.",
            ["vibration", "analysis", "predictive", "maintenance"],
            1.0
        ),
        SearchDocument(
            25,
            "Hydraulic Oil Sampling Techniques",
            "Proper oil sampling ensures accurate contamination analysis. Samples should be taken from turbulent zones and analyzed for ISO 4406 compliance.",
            ["hydraulic", "oil", "sampling", "iso", "4406"],
            1.0
        ),
        SearchDocument(
            26,
            "Accumulator Applications in Energy Storage",
            "Accumulators provide energy for peak demands, emergency operations, and shock absorption. Selection depends on volume, pressure, and response time.",
            ["accumulator", "energy", "storage", "selection"],
            1.0
        ),
        SearchDocument(
            27,
            "Hydraulic System Heat Load Calculation",
            "Heat load is calculated from input power, efficiency losses, and ambient conditions. Accurate calculation is critical for selecting cooling components.",
            ["hydraulic", "system", "heat", "calculation"],
            1.0
        ),
        SearchDocument(
            28,
            "Hydraulic Fluid Compatibility",
            "Fluid compatibility with seals, hoses, and metals must be verified to prevent degradation and leaks. Consult manufacturer recommendations for each fluid type.",
            ["hydraulic", "fluid", "compatibility", "seals"],
            1.0
        ),
        SearchDocument(
            29,
            "Poppet Valve Features",
            "Poppet valves are robust, provide zero leakage, and are suitable for high-pressure, on-off applications. They are less suited for proportional control.",
            ["poppet", "valve", "features", "high-pressure"],
            1.0
        ),
        SearchDocument(
            30,
            "Hydraulic Circuit Simulation Tools",
            "Simulation tools help design and analyze hydraulic circuits, predicting pressure drops, flow rates, and heat generation before system build.",
            ["hydraulic", "circuit", "simulation", "design"],
            1.0
        ),
        SearchDocument(
            31,
            "Servo vs Proportional Valve Applications",
            "Servo valves are used for high-precision, dynamic applications, while proportional valves are suited for general flow and pressure control.",
            ["servo", "proportional", "valve", "applications"],
            1.0
        ),
        SearchDocument(
            32,
            "Hydraulic System Oil Analysis Parameters",
            "Oil analysis measures viscosity, particle count, water content, and wear metals. Trends in these parameters indicate system health and maintenance needs.",
            ["hydraulic", "oil", "analysis", "parameters"],
            1.0
        ),
        SearchDocument(
            33,
            "Hydraulic Cylinder Cushioning",
            "Cushioning at end-of-stroke reduces impact and noise, improving cylinder life. Adjustable cushions can be specified for both extension and retraction.",
            ["hydraulic", "cylinder", "cushioning", "design"],
            1.0
        ),
        SearchDocument(
            34,
            "Hydraulic System Startup Procedures",
            "Proper startup includes system flushing, air bleeding, and gradual pressurization. These steps prevent contamination and component damage.",
            ["hydraulic", "system", "startup", "procedures"],
            1.0
        ),
        SearchDocument(
            35,
            "Hydraulic Filtration Beta Ratio",
            "The Beta ratio indicates filter efficiency by comparing upstream and downstream particle counts. Higher Beta ratios mean better filtration performance.",
            ["hydraulic", "filtration", "beta", "ratio"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)