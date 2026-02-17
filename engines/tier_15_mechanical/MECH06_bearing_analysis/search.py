import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# -----------------------------
# Data Classes
# -----------------------------

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

# -----------------------------
# Search Index
# -----------------------------

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.RLock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self._documents[doc.id] = doc
            self._term_freqs[doc.id] = tf
            self._doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self._inverted_index[term].add(doc.id)
                self._doc_freq[term] += 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self._lock:
            query_terms = self._tokenize(query)
            candidate_docs = set()
            for term in query_terms:
                candidate_docs.update(self._inverted_index.get(term, set()))
            scored_results = []
            for doc_id in candidate_docs:
                bm25_score = self._score_bm25(doc_id, query_terms)
                tfidf_score = self._score_tfidf(doc_id, query_terms)
                # Combine BM25 and TF-IDF (weighted sum, BM25 dominant)
                score = 0.7 * bm25_score + 0.3 * tfidf_score
                doc = self._documents[doc_id]
                snippet = self._make_snippet(doc.content, query_terms)
                scored_results.append(SearchResult(doc_id, score, doc.title, snippet))
            scored_results.sort(key=lambda x: x.score, reverse=True)
            return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_documents": self._total_docs,
                "avg_doc_length": self._avg_doc_length,
                "unique_terms": len(self._inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanum, split on whitespace
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        with self._lock:
            if term in self._idf_cache:
                return self._idf_cache[term]
            df = self._doc_freq.get(term, 0)
            if df == 0:
                idf = 0.0
            else:
                idf = math.log(1 + (self._total_docs - df + 0.5) / (df + 0.5))
            self._idf_cache[term] = idf
            return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_length = self._doc_lengths[doc_id]
        avg_dl = self._avg_doc_length if self._avg_doc_length > 0 else 1
        doc = self._documents[doc_id]
        score = 0.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            numerator = f * (self._bm25_k1 + 1)
            denominator = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / avg_dl)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_length = self._doc_lengths[doc_id]
        doc = self._documents[doc_id]
        score = 0.0
        for term in query_terms:
            term_tf = tf.get(term, 0) / (doc_length if doc_length > 0 else 1)
            idf = self._compute_idf(term)
            score += term_tf * idf
        return score * doc.weight

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(min(positions) - 30, 0)
            end = min(start + snippet_len, len(content))
            snippet = content[start:end]
            # Highlight terms
            for term in query_terms:
                snippet = re.sub(r'(?i)(' + re.escape(term) + r')', r'**\1**', snippet)
            return snippet
        else:
            return content[:snippet_len] + ('...' if len(content) > snippet_len else '')

# -----------------------------
# Singleton Factory
# -----------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# -----------------------------
# Pre-seed Domain Documents
# -----------------------------

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "ISO 281: Rolling Bearing Life Calculation",
            "ISO 281 provides the basic dynamic load rating and life calculation for rolling bearings. The L10 life is the number of revolutions at which 90% of a group of identical bearings will still be operational. The basic formula is L10 = (C/P)^p, where C is the dynamic load rating, P is the equivalent dynamic bearing load, and p is the exponent (3 for ball bearings, 10/3 for roller bearings).",
            ["ISO 281", "life calculation", "rolling bearing"],
            1.0
        ),
        SearchDocument(
            2,
            "Bearing Fit Selection: Shaft and Housing",
            "Proper fit selection between bearing and shaft/housing is crucial for performance. Fits are categorized as loose, transition, or interference. ISO 286 and bearing manufacturer tables provide recommended fits based on load direction, rotation, and operating temperature. Too tight a fit can cause excessive preload or mounting damage.",
            ["fit selection", "shaft", "housing", "ISO 286"],
            1.0
        ),
        SearchDocument(
            3,
            "Grease vs Oil: Bearing Lubrication Selection",
            "Choosing between grease and oil lubrication depends on speed, temperature, and load. Grease is preferred for moderate speeds and temperatures, offering simpler sealing. Oil is used for high-speed or high-temperature applications, and when heat removal is necessary. Lubricant selection affects bearing life and maintenance intervals.",
            ["lubrication", "grease", "oil", "selection"],
            1.0
        ),
        SearchDocument(
            4,
            "Fatigue Spalling: Bearing Failure Analysis",
            "Fatigue spalling is a common failure mode in rolling bearings, characterized by subsurface crack initiation due to cyclic stress. Spalling appears as flaking or pitting on raceways or rolling elements. Root causes include overloading, poor lubrication, contamination, and improper mounting.",
            ["failure analysis", "fatigue", "spalling"],
            1.0
        ),
        SearchDocument(
            5,
            "Vibration Analysis: Bearing Defect Frequencies",
            "Vibration analysis detects bearing defects by identifying characteristic frequencies: BPFO (Ball Pass Frequency Outer), BPFI (Ball Pass Frequency Inner), BSF (Ball Spin Frequency), and FTF (Fundamental Train Frequency). These frequencies are calculated from bearing geometry and shaft speed.",
            ["vibration analysis", "defect frequency", "BPFO", "BPFI", "BSF", "FTF"],
            1.0
        ),
        SearchDocument(
            6,
            "API 610 Bearing Requirements for Centrifugal Pumps",
            "API 610 specifies bearing types, minimum L10 life, and lubrication requirements for centrifugal pumps in the oil and gas industry. Typical requirements include an L10 life of 25,000 hours and provisions for oil mist lubrication in critical services.",
            ["API 610", "centrifugal pump", "bearing requirements"],
            1.0
        ),
        SearchDocument(
            7,
            "Journal Bearing Design: Hydrodynamic Lubrication",
            "Journal bearings support radial loads via a hydrodynamic oil film. Key design parameters include clearance ratio, surface finish, and oil viscosity. The Sommerfeld number characterizes operating regime. Proper design prevents metal-to-metal contact and reduces friction.",
            ["journal bearing", "hydrodynamic lubrication", "design"],
            1.0
        ),
        SearchDocument(
            8,
            "Tilting Pad Bearing Design for Turbomachinery",
            "Tilting pad bearings accommodate misalignment and dynamic loads in high-speed machinery. Each pad pivots to form a wedge-shaped oil film, enhancing stability. Design factors include pad pivot location, preload, and material selection.",
            ["tilting pad", "bearing design", "turbomachinery"],
            1.0
        ),
        SearchDocument(
            9,
            "Bearing Contamination Control: ISO 4406 Codes",
            "ISO 4406 quantifies fluid cleanliness using a three-number code representing particle counts at 4, 6, and 14 microns. Cleanliness control is vital for bearing life, especially in hydraulic and lubrication systems. Filtration and regular monitoring are recommended.",
            ["contamination", "ISO 4406", "cleanliness", "filtration"],
            1.0
        ),
        SearchDocument(
            10,
            "Brinelling vs False Brinelling in Bearings",
            "Brinelling is permanent indentation of raceways caused by static overload or impact. False brinelling results from vibration or micro-movement under load, leading to wear marks that resemble brinelling but are not true plastic deformation.",
            ["brinelling", "false brinelling", "bearing damage"],
            1.0
        ),
        SearchDocument(
            11,
            "Electrical Erosion: VFD-Induced Bearing Damage",
            "Variable Frequency Drives (VFDs) can induce shaft voltages that discharge through bearings, causing electrical erosion. Symptoms include fluting, pitting, and premature failure. Mitigation includes insulated bearings, shaft grounding, and conductive grease.",
            ["electrical erosion", "VFD", "bearing damage"],
            1.0
        ),
        SearchDocument(
            12,
            "Bearing Preload: Angular Contact and Tapered Roller",
            "Preload is the application of an axial force to bearings to remove internal clearance. Angular contact and tapered roller bearings often require preload for rigidity and precise positioning. Excessive preload increases friction and heat, reducing life.",
            ["preload", "angular contact", "tapered roller"],
            1.0
        ),
        SearchDocument(
            13,
            "Bearing Mounting and Dismounting Procedures",
            "Proper mounting and dismounting of bearings prevents damage and ensures performance. Methods include thermal expansion, hydraulic nuts, and mechanical presses. Cleanliness and correct tools are essential. Follow manufacturer guidelines for fit and lubrication.",
            ["mounting", "dismounting", "procedures"],
            1.0
        ),
        SearchDocument(
            14,
            "Equivalent Dynamic Load Calculation",
            "The equivalent dynamic load (P) combines radial and axial loads into a single value for life calculation. For deep groove ball bearings: P = X*Fr + Y*Fa, where Fr is radial load, Fa is axial load, and X, Y are factors from bearing tables.",
            ["dynamic load", "life calculation", "ball bearing"],
            1.0
        ),
        SearchDocument(
            15,
            "Bearing Clearance: Radial and Axial",
            "Bearing clearance is the total movement possible between inner and outer rings. Radial clearance affects heat generation and noise. Clearance classes (C2, CN, C3, etc.) are selected based on fit, temperature, and application.",
            ["clearance", "radial", "axial"],
            1.0
        ),
        SearchDocument(
            16,
            "Lubricant Viscosity Selection for Bearings",
            "Lubricant viscosity must match bearing speed and load. Too low viscosity leads to metal contact and wear; too high increases drag and heat. Viscosity index and operating temperature are key selection criteria.",
            ["lubricant", "viscosity", "selection"],
            1.0
        ),
        SearchDocument(
            17,
            "Bearing Material Selection",
            "Common bearing materials include through-hardened steel (e.g., 52100), case-hardened steel, and ceramics. Material selection affects fatigue life, corrosion resistance, and speed capability.",
            ["material", "selection", "steel", "ceramic"],
            1.0
        ),
        SearchDocument(
            18,
            "Bearing Cage Design and Materials",
            "Cages (retainers) separate rolling elements and guide motion. Materials include pressed steel, machined brass, and polyamide. Cage design impacts speed, lubrication, and noise.",
            ["cage", "design", "material"],
            1.0
        ),
        SearchDocument(
            19,
            "Sealing Solutions for Bearings",
            "Seals protect bearings from contamination and retain lubricant. Types include contact, non-contact, and labyrinth seals. Selection depends on environment, speed, and temperature.",
            ["seal", "contamination", "lubricant retention"],
            1.0
        ),
        SearchDocument(
            20,
            "Bearing Failure Modes: Overview",
            "Common bearing failure modes include fatigue spalling, wear, corrosion, electrical erosion, and brinelling. Root cause analysis is essential for corrective action.",
            ["failure mode", "analysis", "spalling", "wear"],
            1.0
        ),
        SearchDocument(
            21,
            "Bearing Noise and Vibration Troubleshooting",
            "Unusual noise or vibration in bearings may indicate defects, contamination, or improper mounting. Vibration spectrum analysis helps pinpoint the defect type and location.",
            ["noise", "vibration", "troubleshooting"],
            1.0
        ),
        SearchDocument(
            22,
            "Bearing Lubrication: Relubrication Intervals",
            "Relubrication intervals depend on bearing type, speed, temperature, and grease quality. Over-lubrication can cause churning and heat, while under-lubrication leads to wear.",
            ["lubrication", "relubrication", "interval"],
            1.0
        ),
        SearchDocument(
            23,
            "Bearing Housing Design Considerations",
            "Bearing housings must provide support, alignment, and protection. Design factors include material, sealing, and provision for thermal expansion. Split housings simplify maintenance.",
            ["housing", "design", "support"],
            1.0
        ),
        SearchDocument(
            24,
            "Bearing Internal Clearance Measurement",
            "Internal clearance is measured with feeler gauges or dial indicators before and after mounting. Clearance changes due to fit, temperature, and load must be considered.",
            ["internal clearance", "measurement"],
            1.0
        ),
        SearchDocument(
            25,
            "Bearing Lubrication Systems: Circulating Oil",
            "Circulating oil systems provide continuous lubrication and cooling for high-speed or heavily loaded bearings. System design includes pumps, filters, and heat exchangers.",
            ["lubrication", "circulating oil", "system"],
            1.0
        ),
        SearchDocument(
            26,
            "Bearing Failure Analysis: Case Study",
            "A failed bearing from a centrifugal pump exhibited fatigue spalling and evidence of electrical erosion. Investigation revealed inadequate lubrication and VFD-induced shaft currents. Corrective actions included improved lubrication and shaft grounding.",
            ["failure analysis", "case study", "spalling", "electrical erosion"],
            1.0
        ),
        SearchDocument(
            27,
            "ISO 76: Static Load Rating",
            "ISO 76 defines the static load rating for rolling bearings. The static equivalent load is used to assess risk of permanent deformation under non-rotating or slow oscillating loads.",
            ["ISO 76", "static load", "rating"],
            1.0
        ),
        SearchDocument(
            28,
            "Bearing Mounting Tools and Techniques",
            "Specialized tools such as induction heaters, hydraulic nuts, and pullers are used for safe bearing mounting and removal. Proper technique prevents brinelling and misalignment.",
            ["mounting", "tools", "technique"],
            1.0
        ),
        SearchDocument(
            29,
            "Bearing Life: L10 vs L50",
            "L10 life is the standard for bearing selection, but L50 (median life) may be used for reliability analysis. L50 is approximately 5 times L10 for ball bearings.",
            ["life", "L10", "L50", "reliability"],
            1.0
        ),
        SearchDocument(
            30,
            "Bearing Grease Types and Properties",
            "Grease types include lithium, polyurea, and calcium sulfonate. Properties such as base oil viscosity, thickener type, and NLGI grade influence performance and compatibility.",
            ["grease", "type", "property"],
            1.0
        ),
        SearchDocument(
            31,
            "Bearing Preload Methods",
            "Preload can be applied by springs, shims, or controlled axial tightening. Method selection depends on application and required stiffness.",
            ["preload", "method", "stiffness"],
            1.0
        ),
        SearchDocument(
            32,
            "Bearing Failure: Lubricant Contamination",
            "Contaminated lubricant accelerates bearing wear and fatigue. Sources include ingress of dust, water, or metal particles. Effective sealing and filtration are critical.",
            ["failure", "lubricant", "contamination"],
            1.0
        ),
        SearchDocument(
            33,
            "Bearing Defect Frequency Calculator",
            "Defect frequencies are calculated using bearing geometry: BPFO = n/2 * (1 - d/D * cos(θ)), BPFI = n/2 * (1 + d/D * cos(θ)), where n is number of rolling elements, d is ball diameter, D is pitch diameter, θ is contact angle.",
            ["defect frequency", "calculator", "geometry"],
            1.0
        ),
        SearchDocument(
            34,
            "Journal Bearing Failure: Wiping",
            "Wiping is severe damage to journal bearings caused by loss of hydrodynamic film, typically due to lubricant starvation or overload. Symptoms include metal transfer and scoring.",
            ["journal bearing", "failure", "wiping"],
            1.0
        ),
        SearchDocument(
            35,
            "Bearing Lubrication: Oil Mist Systems",
            "Oil mist lubrication is used in process pumps and compressors. Fine oil droplets are carried by air to bearing housings, reducing friction and contamination risk.",
            ["lubrication", "oil mist", "system"],
            1.0
        ),
        SearchDocument(
            36,
            "Bearing Temperature Monitoring",
            "Temperature rise in bearings can indicate excessive load, poor lubrication, or impending failure. Monitoring methods include RTDs, thermocouples, and infrared sensors.",
            ["temperature", "monitoring", "failure"],
            1.0
        ),
        SearchDocument(
            37,
            "Bearing Alignment in Rotating Machinery",
            "Correct shaft and housing alignment prevents uneven load distribution and premature bearing failure. Laser alignment tools improve accuracy.",
            ["alignment", "rotating machinery", "failure prevention"],
            1.0
        ),
        SearchDocument(
            38,
            "Bearing Dynamic Load Rating: C Value",
            "The dynamic load rating (C) is the constant load a bearing can endure for 1 million revolutions with 90% reliability. Provided by manufacturers per ISO 281.",
            ["dynamic load", "rating", "C value"],
            1.0
        ),
        SearchDocument(
            39,
            "Bearing Lubrication: Solid Lubricants",
            "Solid lubricants like graphite or MoS2 are used in extreme environments where oil or grease is unsuitable. They provide low friction under high temperature or vacuum.",
            ["lubrication", "solid lubricant", "extreme environment"],
            1.0
        ),
        SearchDocument(
            40,
            "Bearing Failure Analysis: Wear and Corrosion",
            "Wear occurs from inadequate lubrication or contamination. Corrosion results from water ingress or chemical attack. Both reduce bearing life and require root cause correction.",
            ["failure analysis", "wear", "corrosion"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)