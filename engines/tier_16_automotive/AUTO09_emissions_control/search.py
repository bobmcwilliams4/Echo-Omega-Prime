import math
import threading
import heapq
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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._inverted_index: Dict[str, set] = defaultdict(set)
        self._doc_term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._N: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._tokenizer = re.compile(r"\b\w+\b", re.UNICODE)

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.content)
            term_freq = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_term_freqs[doc.id] = term_freq
            self._doc_lengths[doc.id] = len(tokens)
            for term in term_freq:
                self._doc_freqs[term] += 1
                self._inverted_index[term].add(doc.id)
            self._N += 1
            self._avg_doc_length = (
                sum(self._doc_lengths.values()) / self._N if self._N else 0.0
            )
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self._inverted_index.get(term, set()))
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            scored_results.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "num_documents": self._N,
                "avg_doc_length": self._avg_doc_length,
                "vocab_size": len(self._doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._tokenizer.findall(text)]

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freqs.get(term, 0)
        N = self._N
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5)) if df else 0.0
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        k1 = 1.5
        b = 0.75
        score = 0.0
        doc = self._documents[doc_id]
        term_freqs = self._doc_term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        for term in set(query_terms):
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + k1 * (1 - b + b * doc_len / avgdl)
            numer = tf * (k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tfidf = 0.0
        term_freqs = self._doc_term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        for term in set(query_terms):
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            tfidf += tf_norm * idf
        return tfidf * self._documents[doc_id].weight

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        term_set = set(query_terms)
        positions = [i for i, t in enumerate(tokens) if t in term_set]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in term_set:
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

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

# --- Preseed Domain Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Three-Way Catalytic Converter Chemistry",
            "Three-way catalytic converters (TWCs) simultaneously reduce NOx, CO, and HC emissions. The catalyst promotes oxidation of CO and HC and reduction of NOx. Light-off temperature is critical for efficiency.",
            ["TWC", "catalyst", "chemistry", "light-off"],
            1.0
        ),
        SearchDocument(
            2,
            "Catalyst Light-Off Temperature Strategies",
            "Catalyst light-off is the temperature at which the converter becomes effective. Strategies include retarded ignition timing and secondary air injection to accelerate heating after cold start.",
            ["catalyst", "light-off", "cold-start", "strategy"],
            1.0
        ),
        SearchDocument(
            3,
            "Diesel Particulate Filter Regeneration",
            "DPF regeneration burns off accumulated soot using passive or active methods. Active regeneration may use post-injection or fuel burners. Ash accumulation from lube oil and additives is not removed by regeneration.",
            ["DPF", "regeneration", "ash", "diesel"],
            1.0
        ),
        SearchDocument(
            4,
            "Ash Accumulation in DPFs",
            "Ash in diesel particulate filters originates from engine oil additives and is not combustible. Excessive ash increases backpressure and requires filter cleaning or replacement.",
            ["DPF", "ash", "maintenance", "diesel"],
            1.0
        ),
        SearchDocument(
            5,
            "SCR and DEF Dosing Control",
            "Selective Catalytic Reduction (SCR) reduces NOx using ammonia from Diesel Exhaust Fluid (DEF). Accurate DEF dosing is vital to minimize ammonia slip and maximize NOx conversion.",
            ["SCR", "DEF", "NOx", "dosing"],
            1.0
        ),
        SearchDocument(
            6,
            "SCR Catalyst Chemistry and NOx Reduction",
            "SCR catalysts use vanadium, zeolite, or iron to promote NOx reduction with ammonia. Temperature window for optimal conversion is typically 200-400°C.",
            ["SCR", "catalyst", "NOx", "chemistry"],
            1.0
        ),
        SearchDocument(
            7,
            "Exhaust Gas Recirculation (EGR) System Design",
            "EGR reduces NOx by recirculating a portion of exhaust back into the intake. Cooled EGR further lowers combustion temperatures, improving NOx control.",
            ["EGR", "NOx", "system", "design"],
            1.0
        ),
        SearchDocument(
            8,
            "Benefits of Cooled EGR",
            "Cooled EGR systems lower intake charge temperature, enabling higher EGR rates and improved NOx reduction with minimal impact on engine performance.",
            ["EGR", "cooled", "NOx", "benefits"],
            1.0
        ),
        SearchDocument(
            9,
            "Evaporative Emission Control (EVAP) System Overview",
            "EVAP systems capture fuel vapors from the tank and route them to the engine for combustion. Leak detection monitors system integrity to meet regulatory standards.",
            ["EVAP", "emission", "leak", "control"],
            1.0
        ),
        SearchDocument(
            10,
            "EVAP Leak Detection Standards",
            "OBDII requires EVAP leak detection for leaks as small as 0.020 inches. Methods include pressure decay, vacuum, and natural vacuum leak detection (NVLD).",
            ["EVAP", "leak", "OBDII", "standards"],
            1.0
        ),
        SearchDocument(
            11,
            "OBDII Catalyst Efficiency Monitor",
            "OBDII monitors catalyst efficiency using upstream and downstream oxygen sensor signals. The oxygen sensor ratio method detects catalyst deterioration.",
            ["OBDII", "catalyst", "monitor", "oxygen sensor"],
            1.0
        ),
        SearchDocument(
            12,
            "Oxygen Sensor Ratio Method Explained",
            "The oxygen sensor ratio method compares the switching frequency of pre- and post-catalyst oxygen sensors to infer catalyst performance.",
            ["oxygen sensor", "ratio", "catalyst", "OBDII"],
            1.0
        ),
        SearchDocument(
            13,
            "Gasoline Particulate Filter (GPF) in GDI Engines",
            "GPFs trap particulate matter from gasoline direct injection (GDI) engines. Like DPFs, they require periodic regeneration to prevent backpressure.",
            ["GPF", "GDI", "emissions", "particulate"],
            1.0
        ),
        SearchDocument(
            14,
            "GDI Emissions and Control Technologies",
            "GDI engines emit more particulates than port-injected engines. GPFs and optimized injection strategies help meet particulate emission standards.",
            ["GDI", "emissions", "GPF", "control"],
            1.0
        ),
        SearchDocument(
            15,
            "Cold-Start Emissions and Catalyst Light-Off",
            "Cold-start emissions dominate total HC and CO output. Rapid catalyst heating strategies, such as electric heaters or exhaust gas management, are used to minimize cold-start impact.",
            ["cold-start", "catalyst", "emissions", "light-off"],
            1.0
        ),
        SearchDocument(
            16,
            "Real Driving Emissions (RDE) Testing",
            "RDE testing uses Portable Emissions Measurement Systems (PEMS) to measure real-world emissions. It complements lab-based certification and addresses discrepancies.",
            ["RDE", "PEMS", "testing", "emissions"],
            1.0
        ),
        SearchDocument(
            17,
            "PEMS Technology for RDE",
            "Portable Emissions Measurement Systems (PEMS) provide on-road data for NOx, CO2, and particulates, enabling compliance with RDE regulations.",
            ["PEMS", "RDE", "technology", "emissions"],
            1.0
        ),
        SearchDocument(
            18,
            "EPA Tier 3 vs CARB LEV III Standards",
            "EPA Tier 3 and CARB LEV III set stringent limits for NOx, NMOG, and particulates. LEV III generally requires lower fleet-average emissions and longer durability.",
            ["EPA", "CARB", "Tier 3", "LEV III", "standards"],
            1.0
        ),
        SearchDocument(
            19,
            "OBDII Readiness Monitors Explained",
            "OBDII readiness monitors indicate whether emission control systems have been checked. Monitors must be set before emissions inspection and maintenance (I/M) testing.",
            ["OBDII", "readiness", "monitor", "I/M"],
            1.0
        ),
        SearchDocument(
            20,
            "Emission Testing and I/M Programs",
            "Inspection and Maintenance (I/M) programs use OBDII data and tailpipe testing to ensure vehicles meet emission standards throughout their life.",
            ["emission", "testing", "I/M", "OBDII"],
            1.0
        ),
        SearchDocument(
            21,
            "Diesel Oxidation Catalyst (DOC) Function",
            "DOCs oxidize CO and HC and convert some NO to NO2, which is beneficial for DPF regeneration and SCR NOx reduction.",
            ["DOC", "diesel", "oxidation", "NO2", "DPF", "SCR"],
            1.0
        ),
        SearchDocument(
            22,
            "NO to NO2 Conversion in DOCs",
            "The conversion of NO to NO2 in diesel oxidation catalysts enhances soot oxidation in DPFs and improves SCR efficiency.",
            ["DOC", "NO2", "conversion", "DPF", "SCR"],
            1.0
        ),
        SearchDocument(
            23,
            "Crankcase Emission Control (PCV System)",
            "Positive Crankcase Ventilation (PCV) systems route blow-by gases and oil vapors back to the intake, reducing hydrocarbon emissions.",
            ["PCV", "crankcase", "emission", "oil vapor"],
            1.0
        ),
        SearchDocument(
            24,
            "Oil Vapor Management in PCV Systems",
            "Effective oil vapor separation in PCV systems prevents oil consumption and intake deposit formation, maintaining emission compliance.",
            ["PCV", "oil vapor", "management", "emission"],
            1.0
        ),
        SearchDocument(
            25,
            "Advanced Catalyst Light-Off Strategies",
            "Advanced strategies for catalyst light-off include electrically heated catalysts, exhaust insulation, and variable valve timing to increase exhaust temperature.",
            ["catalyst", "light-off", "strategy", "advanced"],
            1.0
        ),
        SearchDocument(
            26,
            "DPF Regeneration Monitoring and Control",
            "Modern DPF systems monitor backpressure and temperature to trigger regeneration events, ensuring filter efficiency and preventing damage.",
            ["DPF", "regeneration", "monitor", "control"],
            1.0
        ),
        SearchDocument(
            27,
            "SCR Ammonia Slip Catalyst (ASC)",
            "Ammonia slip catalysts (ASC) are used downstream of SCR to oxidize excess ammonia, preventing NH3 emissions.",
            ["SCR", "ASC", "ammonia", "catalyst"],
            1.0
        ),
        SearchDocument(
            28,
            "EGR Cooler Fouling and Maintenance",
            "EGR coolers can foul with soot and hydrocarbons, reducing efficiency. Regular maintenance is required to ensure optimal NOx reduction.",
            ["EGR", "cooler", "fouling", "maintenance"],
            1.0
        ),
        SearchDocument(
            29,
            "OBDII GPF Monitoring",
            "OBDII monitors GPF performance using differential pressure and temperature sensors to detect filter loading and regeneration events.",
            ["OBDII", "GPF", "monitor", "emissions"],
            1.0
        ),
        SearchDocument(
            30,
            "Cold-Start Emission Reduction Technologies",
            "Technologies such as electrically heated catalysts, secondary air injection, and exhaust gas management are used to reduce cold-start emissions.",
            ["cold-start", "emission", "reduction", "technology"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)