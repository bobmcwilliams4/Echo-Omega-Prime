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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._tf_cache: Dict[Tuple[int, str], float] = {}
        self._dirty = True

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            term_counts = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_lengths[doc.id] = len(tokens)
            for term, count in term_counts.items():
                self._inverted_index[term][doc.id] = count
                self._doc_freq[term] += 1
            self._total_docs += 1
            self._dirty = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
        with self._lock:
            if self._dirty:
                self._recompute_stats()
            candidate_docs = set()
            for term in tokens:
                candidate_docs.update(self._inverted_index.get(term, {}).keys())
            scored: List[Tuple[int, float]] = []
            for doc_id in candidate_docs:
                bm25_score = self._score_bm25(doc_id, tokens)
                tfidf_score = self._score_tfidf(doc_id, tokens)
                doc_weight = self._documents[doc_id].weight
                score = 0.7 * bm25_score + 0.3 * tfidf_score
                score *= doc_weight
                scored.append((doc_id, score))
            scored.sort(key=lambda x: x[1], reverse=True)
            results = []
            for doc_id, score in scored[:limit]:
                doc = self._documents[doc_id]
                snippet = self._make_snippet(doc, tokens)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            if self._dirty:
                self._recompute_stats()
            return {
                "total_docs": self._total_docs,
                "avg_doc_length": self._avg_doc_length,
                "unique_terms": len(self._inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\-\._ ]+', ' ', text)
        tokens = text.split()
        return [t for t in tokens if len(t) > 1 or t.isdigit()]

    def _recompute_stats(self):
        total_length = sum(self._doc_lengths.values())
        self._avg_doc_length = total_length / self._total_docs if self._total_docs else 0.0
        self._idf_cache.clear()
        self._tf_cache.clear()
        self._dirty = False

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freq.get(term, 0)
        N = self._total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5)) if df else 0.0
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self._documents[doc_id]
        doc_len = self._doc_lengths[doc_id]
        avgdl = self._avg_doc_length or 1.0
        for term in query_terms:
            tf = self._inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + k1 * (1 - b + b * doc_len / avgdl)
            score += idf * (tf * (k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self._doc_lengths[doc_id]
        for term in query_terms:
            tf = self._inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], maxlen: int = 180) -> str:
        content = doc.content
        content_lc = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lc.find(term)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(0, min(positions) - 30)
            end = min(len(content), start + maxlen)
            snippet = content[start:end]
            for term in query_terms:
                snippet = re.sub(r'(?i)\b(%s)\b' % re.escape(term), r'**\1**', snippet)
            return snippet.strip()
        return content[:maxlen].strip()

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

# --- Pre-seed Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "ASME B31.3 Process Piping Code Applicability",
            "Defines the scope and applicability of ASME B31.3 for process piping systems in chemical, petroleum, and related plants. Covers design, materials, fabrication, assembly, erection, examination, inspection, and testing.",
            ["ASME B31.3", "process piping", "applicability"], 1.0
        ),
        SearchDocument(
            2,
            "ASME B31.4 Pipeline Transportation Code Overview",
            "Covers design, construction, inspection, and testing of liquid pipeline transportation systems for hydrocarbons and other liquids. Includes requirements for buried and aboveground pipelines.",
            ["ASME B31.4", "pipeline", "transportation"], 1.0
        ),
        SearchDocument(
            3,
            "ASME B31.8 Gas Transmission and Distribution",
            "Provides requirements for design, construction, testing, and operation of gas transmission and distribution piping systems. Addresses materials, welding, and safety.",
            ["ASME B31.8", "gas transmission", "distribution"], 1.0
        ),
        SearchDocument(
            4,
            "Pipe Sizing for Liquid Flow - Darcy-Weisbach Equation",
            "The Darcy-Weisbach equation is used to calculate pressure drop due to friction in pipe flow. It is applicable to all fluids and pipe materials. The equation: ΔP = f (L/D) (ρV²/2), where f is the friction factor.",
            ["pipe sizing", "darcy-weisbach", "liquid flow"], 1.0
        ),
        SearchDocument(
            5,
            "Hazen-Williams Equation for Water Flow",
            "The Hazen-Williams equation estimates pressure drop and flow in water pipes. It is empirical and suitable for water at typical temperatures. The equation: V = k C R^0.63 S^0.54.",
            ["hazen-williams", "water flow", "pipe sizing"], 1.0
        ),
        SearchDocument(
            6,
            "Pipe Schedule and Wall Thickness Calculation",
            "Pipe schedule defines wall thickness for a given nominal diameter. Wall thickness is selected based on design pressure, temperature, and material strength per ASME B31 codes.",
            ["pipe schedule", "wall thickness", "calculation"], 1.0
        ),
        SearchDocument(
            7,
            "Material Specifications - Carbon Steel Pipe",
            "Common carbon steel pipe grades include ASTM A106, A53, and API 5L. Selection depends on service conditions, temperature, and code requirements.",
            ["material", "carbon steel", "ASTM A106", "ASTM A53"], 1.0
        ),
        SearchDocument(
            8,
            "Low-Temperature Carbon Steel - ASTM A333",
            "ASTM A333 covers seamless and welded steel pipe for low-temperature service. It requires impact testing and is used in cryogenic and cold service applications.",
            ["ASTM A333", "low temperature", "carbon steel"], 1.0
        ),
        SearchDocument(
            9,
            "Stainless Steel Pipe - ASTM A312 Austenitic Grades",
            "ASTM A312 specifies seamless and welded austenitic stainless steel pipes for high-temperature and general corrosive service. Common grades: 304, 316, 321.",
            ["ASTM A312", "stainless steel", "austenitic"], 1.0
        ),
        SearchDocument(
            10,
            "Duplex Stainless Steel - ASTM A790",
            "ASTM A790 covers duplex stainless steel pipe, combining high strength and corrosion resistance. Used in aggressive environments such as offshore and chemical plants.",
            ["ASTM A790", "duplex stainless", "pipe"], 1.0
        ),
        SearchDocument(
            11,
            "Flange Ratings and Selection - ASME B16.5",
            "ASME B16.5 defines dimensions, pressure-temperature ratings, and materials for pipe flanges and flanged fittings. Flange class selection is based on design pressure and temperature.",
            ["flange", "ASME B16.5", "rating", "selection"], 1.0
        ),
        SearchDocument(
            12,
            "Gasket Selection - Spiral Wound, Ring Joint, Compressed Fiber",
            "Gasket type is chosen based on flange type, pressure, temperature, and media. Spiral wound, ring joint, and compressed fiber gaskets are common in process piping.",
            ["gasket", "spiral wound", "ring joint", "compressed fiber"], 1.0
        ),
        SearchDocument(
            13,
            "Pipe Stress Analysis - Sustained, Thermal Expansion, Occasional Loads",
            "Pipe stress analysis evaluates sustained (weight, pressure), thermal expansion, and occasional (wind, seismic) loads to ensure code compliance and safe operation.",
            ["pipe stress", "thermal expansion", "occasional loads"], 1.0
        ),
        SearchDocument(
            14,
            "Pipe Support Design - Types and Applications",
            "Pipe supports include hangers, shoes, guides, and anchors. Selection depends on load, movement, and thermal expansion. Proper support prevents excessive stress and vibration.",
            ["pipe support", "design", "hangers", "anchors"], 1.0
        ),
        SearchDocument(
            15,
            "ASME B16.9 Fittings - Elbows, Tees, Reducers, Caps",
            "ASME B16.9 covers factory-made wrought buttwelding fittings such as elbows, tees, reducers, and caps for use in pressure piping systems.",
            ["ASME B16.9", "fittings", "elbows", "tees", "reducers"], 1.0
        ),
        SearchDocument(
            16,
            "Pipe Welding - WPS, PQR, Welder Qualification",
            "Welding Procedure Specification (WPS), Procedure Qualification Record (PQR), and Welder Qualification are required for code-compliant welding in piping systems.",
            ["welding", "WPS", "PQR", "welder qualification"], 1.0
        ),
        SearchDocument(
            17,
            "Two-Phase Flow in Pipelines - Flow Regimes and Baker Chart",
            "Two-phase flow involves simultaneous gas and liquid phases. Flow regimes (slug, annular, stratified) are identified using the Baker chart for design and analysis.",
            ["two-phase flow", "baker chart", "flow regimes"], 1.0
        ),
        SearchDocument(
            18,
            "Pipeline Pigging - Cleaning and Inspection",
            "Pipeline pigging uses devices called pigs to clean, inspect, and maintain pipelines. Types include cleaning, gauging, and intelligent pigs for inline inspection.",
            ["pipeline", "pigging", "cleaning", "inspection"], 1.0
        ),
        SearchDocument(
            19,
            "Cathodic Protection for Buried Pipelines",
            "Cathodic protection prevents external corrosion of buried pipelines. Methods include impressed current and sacrificial anode systems, as per NACE standards.",
            ["cathodic protection", "buried pipelines", "corrosion"], 1.0
        ),
        SearchDocument(
            20,
            "Pipeline Integrity Management - ASME B31.8S and 49 CFR Part 192",
            "Integrity management programs per ASME B31.8S and 49 CFR Part 192 require risk assessment, inspection, and mitigation to ensure pipeline safety and reliability.",
            ["pipeline integrity", "ASME B31.8S", "49 CFR 192"], 1.0
        ),
        SearchDocument(
            21,
            "Oilfield Flowline and Gathering System Design",
            "Oilfield flowlines and gathering systems transport multiphase fluids from wells to processing facilities. Design considers pressure, temperature, corrosion, and flow assurance.",
            ["oilfield", "flowline", "gathering system", "design"], 1.0
        ),
        SearchDocument(
            22,
            "Pressure-Temperature Ratings for Flanges",
            "Flange pressure-temperature ratings are found in ASME B16.5 tables. Ratings depend on flange class, material group, and service temperature.",
            ["flange", "pressure-temperature", "ASME B16.5"], 1.0
        ),
        SearchDocument(
            23,
            "Pipe Corrosion Allowance and Mill Tolerance",
            "Corrosion allowance is added to wall thickness to compensate for expected material loss. Mill tolerance accounts for manufacturing variations.",
            ["corrosion allowance", "mill tolerance", "wall thickness"], 1.0
        ),
        SearchDocument(
            24,
            "Expansion Loops and Joints in Piping Systems",
            "Expansion loops and joints absorb thermal expansion in long piping runs, reducing stress and preventing damage.",
            ["expansion loop", "expansion joint", "thermal expansion"], 1.0
        ),
        SearchDocument(
            25,
            "Pipe Insulation - Types and Purposes",
            "Pipe insulation reduces heat loss, prevents freezing, and protects personnel. Materials include mineral wool, calcium silicate, and cellular glass.",
            ["pipe insulation", "thermal", "personnel protection"], 1.0
        ),
        SearchDocument(
            26,
            "Hydrostatic Testing of Pipelines",
            "Hydrostatic testing verifies the integrity of new and existing pipelines by pressurizing with water above design pressure and checking for leaks.",
            ["hydrostatic test", "pipeline", "integrity"], 1.0
        ),
        SearchDocument(
            27,
            "Design Pressure and Temperature per ASME B31 Codes",
            "Design pressure and temperature are the basis for selecting pipe, fittings, and flanges. ASME B31 codes provide formulas and requirements for determination.",
            ["design pressure", "design temperature", "ASME B31"], 1.0
        ),
        SearchDocument(
            28,
            "Branch Connections - Weldolet, Sockolet, Threadolet",
            "Branch connections such as weldolet, sockolet, and threadolet provide reinforced outlets from main pipes. Selection depends on size, pressure, and code.",
            ["branch connection", "weldolet", "sockolet", "threadolet"], 1.0
        ),
        SearchDocument(
            29,
            "Pipeline Route Selection and Right-of-Way",
            "Route selection considers environmental, social, and technical factors. Right-of-way acquisition is necessary for pipeline construction and operation.",
            ["pipeline", "route selection", "right-of-way"], 1.0
        ),
        SearchDocument(
            30,
            "Hot Tapping and Line Stopping in Pipelines",
            "Hot tapping allows connection to live pipelines without shutdown. Line stopping temporarily blocks flow for maintenance or repair.",
            ["hot tapping", "line stopping", "pipeline"], 1.0
        ),
        SearchDocument(
            31,
            "Pipe Material Traceability and Certification",
            "Traceability ensures each pipe and fitting can be traced to its material certificate, complying with code and client requirements.",
            ["traceability", "material certificate", "pipe"], 1.0
        ),
        SearchDocument(
            32,
            "Nondestructive Examination (NDE) Methods in Piping",
            "NDE methods such as radiography, ultrasonic, magnetic particle, and dye penetrant testing are used to detect flaws in welds and materials.",
            ["NDE", "radiography", "ultrasonic", "magnetic particle", "dye penetrant"], 1.0
        ),
        SearchDocument(
            33,
            "Pipe Bending and Cold Forming",
            "Pipe bending and cold forming techniques allow fabrication of custom shapes. Bending radius and method must comply with code requirements.",
            ["pipe bending", "cold forming", "fabrication"], 1.0
        ),
        SearchDocument(
            34,
            "Valve Types and Selection for Piping Systems",
            "Valve selection considers type (gate, globe, ball, butterfly), pressure class, material, and service conditions for reliable operation.",
            ["valve", "gate valve", "ball valve", "selection"], 1.0
        ),
        SearchDocument(
            35,
            "Fire Protection in Process Piping",
            "Fire protection measures include fireproofing, deluge systems, and isolation valves to minimize risk in process piping installations.",
            ["fire protection", "process piping", "deluge"], 1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)