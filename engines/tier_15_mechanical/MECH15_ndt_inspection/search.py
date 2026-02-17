import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

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
# Search Index Implementation
# -----------------------------

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = defaultdict(list)  # term -> list of (doc_id, freq)
        self.doc_lengths: Dict[int, int] = {}  # doc_id -> length
        self.avg_doc_length: float = 0.0
        self.doc_count: int = 0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)  # term -> doc freq
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._recompute_stats = True

    # -------------------------
    # Document Management
    # -------------------------

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # Do not add duplicates
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_count += 1

            term_freq = Counter(tokens)
            for term, freq in term_freq.items():
                self.inverted_index[term].append((doc.id, freq))
                self.term_doc_freq[term] += 1

            self._recompute_stats = True

    # -------------------------
    # Tokenization
    # -------------------------

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    # -------------------------
    # IDF Computation
    # -------------------------

    def _compute_idf(self, term: str) -> float:
        # Use cache for efficiency
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = self.doc_count
        n_q = self.term_doc_freq.get(term, 0)
        # BM25 IDF formula with log smoothing
        idf = math.log(1 + (N - n_q + 0.5) / (n_q + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _update_stats(self):
        if not self._recompute_stats:
            return
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.doc_count if self.doc_count > 0 else 0.0
        self._idf_cache.clear()
        self._recompute_stats = False

    # -------------------------
    # BM25 Scoring
    # -------------------------

    def _score_bm25(self, query_tokens: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        doc = self.documents[doc_id]
        doc_tokens = self._tokenize(doc.content)
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        term_freq = Counter(doc_tokens)
        for term in set(query_tokens):
            if term not in term_freq:
                continue
            idf = self._compute_idf(term)
            freq = term_freq[term]
            denom = freq + k1 * (1 - b + b * doc_len / self.avg_doc_length)
            score += idf * freq * (k1 + 1) / denom
        return score * doc.weight

    # -------------------------
    # TF-IDF Scoring
    # -------------------------

    def _score_tfidf(self, query_tokens: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        doc_tokens = self._tokenize(doc.content)
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        term_freq = Counter(doc_tokens)
        for term in set(query_tokens):
            if term not in term_freq:
                continue
            tf = term_freq[term] / doc_len
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    # -------------------------
    # Search
    # -------------------------

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        self._update_stats()
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for term in set(query_tokens):
            for doc_id, _ in self.inverted_index.get(term, []):
                candidate_docs.add(doc_id)
        scored_results = []
        for doc_id in candidate_docs:
            if use_bm25:
                score = self._score_bm25(query_tokens, doc_id)
            else:
                score = self._score_tfidf(query_tokens, doc_id)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_tokens)
                scored_results.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], snippet_len: int = 160) -> str:
        content = doc.content
        content_lower = content.lower()
        for term in query_tokens:
            idx = content_lower.find(term)
            if idx != -1:
                start = max(0, idx - 40)
                end = min(len(content), idx + snippet_len)
                snippet = content[start:end]
                if start > 0:
                    snippet = "..." + snippet
                if end < len(content):
                    snippet = snippet + "..."
                return snippet
        # Fallback: start of content
        return content[:snippet_len] + ("..." if len(content) > snippet_len else "")

    # -------------------------
    # Stats
    # -------------------------

    def get_stats(self) -> Dict[str, float]:
        self._update_stats()
        return {
            "document_count": self.doc_count,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq)
        }

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
# Pre-seeded Domain Documents
# -----------------------------

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "UT Pulse-Echo Thickness Measurement Accuracy",
            "Pulse-echo ultrasonic thickness measurement accuracy depends on calibration, couplant quality, and instrument settings. ASME Section V Article 5 outlines requirements for calibration blocks and accuracy verification. Typical accuracy is ±0.1 mm for steel.",
            ["UT", "Pulse-Echo", "Thickness", "ASME V"],
            1.0
        ),
        SearchDocument(
            2,
            "Phased Array UT Sector Scan Coverage for Weld Inspection",
            "Phased Array Ultrasonic Testing (PAUT) sector scans provide volumetric coverage of welds. Sector scan angles (e.g., 45°-70°) are selected per weld geometry. Coverage maps are documented per ASME Section V Article 4.",
            ["PAUT", "Sector Scan", "Weld", "ASME V"],
            1.0
        ),
        SearchDocument(
            3,
            "TOFD Crack Height Sizing Accuracy",
            "Time-of-Flight Diffraction (TOFD) is effective for crack height sizing in welds. Accuracy is typically within ±1 mm for cracks >3 mm height. Sizing may be affected by grain noise and probe alignment.",
            ["TOFD", "Crack Sizing", "Weld"],
            1.0
        ),
        SearchDocument(
            4,
            "Radiographic Film IQI Sensitivity Requirements",
            "Film radiography requires Image Quality Indicator (IQI) sensitivity per ASME Section V Article 2. Wire or hole type IQIs are used. Sensitivity must meet code acceptance (e.g., 2-2T for wire IQI).",
            ["Radiography", "Film", "IQI", "ASME V"],
            1.0
        ),
        SearchDocument(
            5,
            "Digital Radiography (DR) vs Computed Radiography (CR) Sensitivity",
            "Digital Radiography (DR) offers higher sensitivity and faster results compared to Computed Radiography (CR). DR systems must demonstrate equivalent or better IQI sensitivity per code.",
            ["Radiography", "DR", "CR", "IQI"],
            1.0
        ),
        SearchDocument(
            6,
            "Magnetic Particle Testing AC vs DC Magnetization",
            "AC magnetization is preferred for surface crack detection due to shallow penetration. DC magnetization provides deeper field penetration for subsurface flaws. Selection depends on flaw orientation and depth.",
            ["MT", "AC", "DC", "Magnetization"],
            1.0
        ),
        SearchDocument(
            7,
            "Liquid Penetrant Testing Type I Fluorescent Sensitivity Levels",
            "Type I fluorescent penetrants are classified by sensitivity levels 1/2 to 4. Higher levels provide better flaw detection but may increase false indications. Selection is based on code and application.",
            ["PT", "Fluorescent", "Sensitivity"],
            1.0
        ),
        SearchDocument(
            8,
            "Eddy Current Testing Frequency Selection for Depth of Penetration",
            "Eddy current test frequency selection affects depth of penetration. Lower frequencies penetrate deeper but reduce sensitivity to small flaws. Skin depth is inversely proportional to the square root of frequency.",
            ["ET", "Frequency", "Penetration"],
            1.0
        ),
        SearchDocument(
            9,
            "Acoustic Emission Monitoring for Crack Growth Detection",
            "Acoustic emission (AE) monitoring detects crack growth by capturing transient elastic waves. AE sensors are placed on the structure and monitored during loading. ASME Section V Article 13 covers AE method.",
            ["AE", "Crack Growth", "ASME V"],
            1.0
        ),
        SearchDocument(
            10,
            "ASNT SNT-TC-1A Personnel Qualification Requirements",
            "ASNT SNT-TC-1A provides recommended practice for NDT personnel qualification. Levels I, II, and III are defined with requirements for training, experience, and examinations.",
            ["ASNT", "SNT-TC-1A", "Qualification"],
            1.0
        ),
        SearchDocument(
            11,
            "ASME Section V Code Requirements for NDE Methods",
            "ASME Section V specifies requirements for Nondestructive Examination (NDE) methods including UT, RT, MT, PT, ET, and AE. Each article covers technique, calibration, and acceptance criteria.",
            ["ASME V", "NDE", "Code"],
            1.0
        ),
        SearchDocument(
            12,
            "API 510 Pressure Vessel Inspection Acceptance Criteria",
            "API 510 outlines acceptance criteria for pressure vessel inspection. Flaw evaluation, thickness measurements, and NDE methods must comply with code requirements for continued service.",
            ["API 510", "Pressure Vessel", "Acceptance"],
            1.0
        ),
        SearchDocument(
            13,
            "UT Couplant Selection and Application",
            "Proper couplant selection ensures efficient ultrasonic energy transmission. Water-based gels are common for carbon steel. Couplant must not corrode or damage the test surface.",
            ["UT", "Couplant"],
            1.0
        ),
        SearchDocument(
            14,
            "Phased Array UT Focal Law Calibration",
            "Focal law calibration is essential for accurate phased array UT. Calibration blocks with known reflectors are used to verify beam steering and focusing.",
            ["PAUT", "Calibration"],
            1.0
        ),
        SearchDocument(
            15,
            "TOFD Probe Selection and Setup",
            "TOFD probe selection depends on material thickness and expected flaw size. Probe separation and frequency are adjusted for optimal lateral and vertical resolution.",
            ["TOFD", "Probe", "Setup"],
            1.0
        ),
        SearchDocument(
            16,
            "Radiographic Film Processing and Handling",
            "Proper film processing and handling are critical for image quality. Darkroom cleanliness, chemical control, and film storage conditions must be maintained.",
            ["Radiography", "Film", "Processing"],
            1.0
        ),
        SearchDocument(
            17,
            "Digital Detector Array (DDA) in Digital Radiography",
            "Digital Detector Arrays (DDA) are used in DR for real-time imaging. They offer high dynamic range and rapid image acquisition compared to traditional film.",
            ["Radiography", "DR", "DDA"],
            1.0
        ),
        SearchDocument(
            18,
            "Yoke and Prod Techniques in Magnetic Particle Testing",
            "Yoke and prod techniques are common in MT. Yokes induce a longitudinal field, while prods are used for localized field application. Both methods must achieve adequate field strength.",
            ["MT", "Yoke", "Prod"],
            1.0
        ),
        SearchDocument(
            19,
            "Penetrant Removal Methods in Liquid Penetrant Testing",
            "Removal of excess penetrant is critical to avoid false indications. Water-washable, solvent-removable, and post-emulsifiable methods are used based on penetrant type.",
            ["PT", "Removal"],
            1.0
        ),
        SearchDocument(
            20,
            "Eddy Current Array Probes for Surface Crack Detection",
            "Eddy current array probes enable rapid surface crack detection over large areas. Arrays provide increased coverage and sensitivity compared to single-coil probes.",
            ["ET", "Array", "Surface Crack"],
            1.0
        ),
        SearchDocument(
            21,
            "Acoustic Emission Source Location Techniques",
            "Source location in AE monitoring uses arrival time differences at multiple sensors. Triangulation algorithms estimate the position of crack growth or active flaws.",
            ["AE", "Source Location"],
            1.0
        ),
        SearchDocument(
            22,
            "NDT Personnel Certification per ISO 9712",
            "ISO 9712 provides requirements for third-party certification of NDT personnel. It covers training, experience, and examination for UT, RT, MT, PT, and ET methods.",
            ["ISO 9712", "Certification"],
            1.0
        ),
        SearchDocument(
            23,
            "ASME Section V Article 4: Ultrasonic Examination",
            "Article 4 of ASME Section V details ultrasonic examination requirements, including calibration, scanning patterns, and acceptance criteria for weld inspection.",
            ["ASME V", "UT", "Article 4"],
            1.0
        ),
        SearchDocument(
            24,
            "API 510 Thickness Measurement Intervals",
            "API 510 specifies minimum and maximum intervals for thickness measurements of pressure vessels. Intervals depend on corrosion rates and service conditions.",
            ["API 510", "Thickness", "Interval"],
            1.0
        ),
        SearchDocument(
            25,
            "Acceptance Criteria for Weld Indications in Radiography",
            "Radiographic acceptance criteria for welds are based on flaw type, size, and location. ASME Section V and API 510 provide detailed tables for allowable indications.",
            ["Radiography", "Weld", "Acceptance"],
            1.0
        ),
        SearchDocument(
            26,
            "Magnetic Particle Testing Field Indicator Use",
            "Field indicators such as pie gauges and shims are used to verify adequate magnetic field strength during MT. Proper field ensures reliable flaw detection.",
            ["MT", "Field Indicator"],
            1.0
        ),
        SearchDocument(
            27,
            "Liquid Penetrant Testing Developer Application",
            "Developer application enhances flaw visibility in PT. Dry, wet, and non-aqueous developers are selected based on penetrant type and inspection conditions.",
            ["PT", "Developer"],
            1.0
        ),
        SearchDocument(
            28,
            "Eddy Current Lift-off Effect and Compensation",
            "Lift-off refers to the distance between probe and test surface in ET. Excessive lift-off reduces sensitivity. Compensation techniques include reference standards and probe design.",
            ["ET", "Lift-off"],
            1.0
        ),
        SearchDocument(
            29,
            "Acoustic Emission Data Interpretation",
            "AE data interpretation involves analyzing hit counts, amplitude, and energy. Patterns may indicate crack initiation, growth, or stable conditions.",
            ["AE", "Data Interpretation"],
            1.0
        ),
        SearchDocument(
            30,
            "ASNT Level III Responsibilities",
            "ASNT Level III personnel are responsible for NDT procedure development, personnel training, and technical oversight per SNT-TC-1A.",
            ["ASNT", "Level III"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)