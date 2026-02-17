import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_tokens: Dict[int, List[str]] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.inverted_index: Dict[str, List[int]] = defaultdict(list)
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._doc_term_freqs: Dict[int, Counter] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            self._doc_term_freqs[doc.id] = Counter(tokens)
            for token in set(tokens):
                self.inverted_index[token].append(doc.id)
                self.term_doc_freq[token] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self.inverted_index.get(token, []))
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            # Combine BM25 and TF-IDF (weighted average)
            combined_score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            scored_results.append(SearchResult(doc_id, combined_score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.total_docs,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.term_doc_freq),
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        N = self.total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avgdl = self.avg_doc_length
        tf = self._doc_term_freqs[doc_id]
        for term in query_tokens:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + k1 * (1 - b + b * doc_len / avgdl)
            term_score = idf * freq * (k1 + 1) / denom
            score += term_score
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self._doc_term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_tokens:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        content_tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(content_tokens) if t in query_tokens]
        if not positions:
            snippet = content[:160] + "..." if len(content) > 160 else content
            return snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(content_tokens))
        snippet_tokens = content_tokens[start:end]
        snippet = " ".join(snippet_tokens)
        # Highlight query terms
        for qt in set(query_tokens):
            snippet = re.sub(r'\b({})\b'.format(re.escape(qt)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
                _preseed_documents(_search_index_instance)
    return _search_index_instance

# --- Pre-seeded Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "SMAW Stick Welding Process Selection",
            "Shielded Metal Arc Welding (SMAW), also known as stick welding, is selected based on material type, thickness, position, and code requirements. SMAW is suitable for field repairs and construction due to its portability and versatility.",
            ["SMAW", "process selection", "stick welding"],
            1.0,
        ),
        SearchDocument(
            2,
            "GMAW/MIG Welding Process Parameters",
            "Gas Metal Arc Welding (GMAW or MIG) process parameters include voltage, amperage, wire feed speed, shielding gas composition, and travel speed. Proper parameter selection ensures weld quality and minimizes defects.",
            ["GMAW", "MIG", "parameters"],
            1.0,
        ),
        SearchDocument(
            3,
            "GTAW/TIG Welding for Critical Applications",
            "Gas Tungsten Arc Welding (GTAW or TIG) is preferred for critical joints, thin materials, and non-ferrous metals. GTAW offers precise control and high-quality welds with minimal spatter.",
            ["GTAW", "TIG", "critical applications"],
            1.0,
        ),
        SearchDocument(
            4,
            "Welding Procedure Specification (WPS) per ASME Section IX",
            "A Welding Procedure Specification (WPS) is a qualified document per ASME Section IX that details welding variables, base materials, filler metals, preheat, interpass temperature, and post-weld heat treatment requirements.",
            ["WPS", "ASME IX", "procedure"],
            1.0,
        ),
        SearchDocument(
            5,
            "Welder Performance Qualification per ASME Section IX",
            "Welder performance qualification tests are conducted per ASME Section IX to ensure welders can produce sound welds using specified procedures. Test coupons are examined for defects and mechanical properties.",
            ["welder qualification", "ASME IX"],
            1.0,
        ),
        SearchDocument(
            6,
            "Preheat and Interpass Temperature Requirements",
            "Preheat and interpass temperatures are specified to reduce the risk of cracking and hydrogen-induced failures. These requirements depend on material composition, thickness, and applicable codes.",
            ["preheat", "interpass", "temperature"],
            1.0,
        ),
        SearchDocument(
            7,
            "Post-Weld Heat Treatment (PWHT) Requirements",
            "PWHT relieves residual stresses, improves toughness, and reduces hardness in weldments. PWHT cycles are defined by temperature, holding time, and cooling rate per code requirements.",
            ["PWHT", "heat treatment"],
            1.0,
        ),
        SearchDocument(
            8,
            "Filler Metal Selection and AWS Classification",
            "Filler metals are selected based on base material compatibility, mechanical properties, and service environment. AWS classification provides a standard designation for filler materials.",
            ["filler metal", "AWS", "classification"],
            1.0,
        ),
        SearchDocument(
            9,
            "Weld Joint Design and Preparation",
            "Proper joint design and preparation are essential for weld quality. Joint types include butt, fillet, groove, and corner joints. Preparation involves cleaning, fit-up, and beveling as required.",
            ["joint design", "preparation"],
            1.0,
        ),
        SearchDocument(
            10,
            "Weld Defects: Porosity",
            "Porosity is caused by trapped gas in the solidifying weld metal. Common sources include contaminated base metal, improper shielding gas, and excessive moisture. Visual and radiographic inspection can detect porosity.",
            ["defects", "porosity"],
            1.0,
        ),
        SearchDocument(
            11,
            "Weld Defects: Lack of Fusion and Incomplete Penetration",
            "Lack of fusion occurs when weld metal does not properly fuse with base metal or previous weld beads. Incomplete penetration results from insufficient heat or improper joint preparation.",
            ["defects", "lack of fusion", "penetration"],
            1.0,
        ),
        SearchDocument(
            12,
            "Weld Defects: Cracks (Hot Cracks and Cold Cracks)",
            "Cracks in welds can be classified as hot cracks (solidification cracks) or cold cracks (hydrogen-induced or delayed cracking). Causes include high restraint, rapid cooling, and hydrogen presence.",
            ["defects", "cracks", "hot cracks", "cold cracks"],
            1.0,
        ),
        SearchDocument(
            13,
            "Ultrasonic Testing (UT) for Weld Inspection",
            "Ultrasonic Testing (UT) uses high-frequency sound waves to detect internal discontinuities in welds. UT is sensitive to cracks, lack of fusion, and inclusions, and provides depth information.",
            ["UT", "ultrasonic testing", "inspection"],
            1.0,
        ),
        SearchDocument(
            14,
            "Radiographic Testing (RT) for Weld Inspection",
            "Radiographic Testing (RT) uses X-rays or gamma rays to produce images of weld interiors. RT is effective for detecting porosity, slag inclusions, and cracks, but may miss planar defects.",
            ["RT", "radiographic testing", "inspection"],
            1.0,
        ),
        SearchDocument(
            15,
            "Magnetic Particle Testing (MT) for Surface Crack Detection",
            "Magnetic Particle Testing (MT) is used to detect surface and near-surface cracks in ferromagnetic materials. Indications are revealed by magnetic particles accumulating at discontinuities.",
            ["MT", "magnetic particle", "crack detection"],
            1.0,
        ),
        SearchDocument(
            16,
            "Liquid Penetrant Testing (PT) for Non-Magnetic Materials",
            "Liquid Penetrant Testing (PT) is suitable for detecting surface-breaking defects in non-magnetic materials. Penetrant is applied, excess is removed, and developer reveals indications.",
            ["PT", "liquid penetrant", "inspection"],
            1.0,
        ),
        SearchDocument(
            17,
            "Visual Inspection (VT) and Acceptance Criteria",
            "Visual Inspection (VT) is the first step in weld quality assessment. Acceptance criteria are defined by applicable codes and standards, covering dimensions, appearance, and surface discontinuities.",
            ["VT", "visual inspection", "acceptance"],
            1.0,
        ),
        SearchDocument(
            18,
            "API 1104 Pipeline Welding Standard",
            "API 1104 covers welding requirements for pipelines and related facilities. It specifies procedure qualification, welder qualification, inspection, and acceptance criteria for pipeline welds.",
            ["API 1104", "pipeline", "standard"],
            1.0,
        ),
        SearchDocument(
            19,
            "AWS D1.1 Structural Welding Code - Steel",
            "AWS D1.1 is the standard for welding steel structures. It includes requirements for design, qualification, fabrication, inspection, and repair of welded steel structures.",
            ["AWS D1.1", "structural", "steel"],
            1.0,
        ),
        SearchDocument(
            20,
            "NACE MR0175/ISO 15156 Sour Service Welding Requirements",
            "NACE MR0175/ISO 15156 specifies requirements for welding in sour service environments to prevent sulfide stress cracking. It covers material selection, welding procedures, and post-weld heat treatment.",
            ["NACE MR0175", "ISO 15156", "sour service"],
            1.0,
        ),
        SearchDocument(
            21,
            "Repair Welding Procedures and Limitations",
            "Repair welding must follow qualified procedures to ensure integrity. Limitations may include maximum number of repairs, heat input, and post-weld heat treatment requirements.",
            ["repair welding", "procedures", "limitations"],
            1.0,
        ),
        SearchDocument(
            22,
            "Weld Documentation and Traceability",
            "Weld documentation includes WPS, PQR, welder qualification records, and inspection reports. Traceability ensures each weld can be linked to procedures, materials, and personnel.",
            ["documentation", "traceability", "records"],
            1.0,
        ),
        SearchDocument(
            23,
            "Selection of Shielding Gas for GMAW",
            "Shielding gas selection in GMAW affects arc stability, penetration, and weld appearance. Common gases include argon, CO2, and mixtures. Selection depends on base metal and desired properties.",
            ["GMAW", "shielding gas", "parameters"],
            1.0,
        ),
        SearchDocument(
            24,
            "Qualification of Welding Consumables",
            "Welding consumables such as electrodes and filler wires must be qualified per applicable codes to ensure compatibility and performance in the intended service environment.",
            ["consumables", "qualification", "filler metal"],
            1.0,
        ),
        SearchDocument(
            25,
            "Weld Fit-Up and Alignment",
            "Proper fit-up and alignment are critical for weld quality. Gaps, misalignment, and poor joint preparation can lead to defects such as lack of fusion and incomplete penetration.",
            ["fit-up", "alignment", "joint preparation"],
            1.0,
        ),
        SearchDocument(
            26,
            "Hydrogen Control in Welding",
            "Controlling hydrogen in welding is essential to prevent cold cracking. Methods include using low-hydrogen electrodes, preheating, and minimizing moisture in consumables.",
            ["hydrogen control", "cracking", "preheat"],
            1.0,
        ),
        SearchDocument(
            27,
            "Weld Overlay and Cladding",
            "Weld overlay and cladding are used to improve corrosion and wear resistance. Procedures must ensure proper bonding and minimal dilution between base and overlay materials.",
            ["overlay", "cladding", "corrosion"],
            1.0,
        ),
        SearchDocument(
            28,
            "Hardness Testing of Welds",
            "Hardness testing evaluates the mechanical properties of welds and heat-affected zones. Excessive hardness may indicate susceptibility to cracking or improper heat treatment.",
            ["hardness", "testing", "mechanical properties"],
            1.0,
        ),
        SearchDocument(
            29,
            "Weld Metal Toughness Testing",
            "Toughness testing, such as Charpy V-notch, assesses the ability of weld metal to absorb energy and resist brittle fracture, especially at low temperatures.",
            ["toughness", "testing", "charpy"],
            1.0,
        ),
        SearchDocument(
            30,
            "Weld Size and Throat Measurement",
            "Accurate measurement of weld size and throat is necessary for structural integrity. Tools include fillet weld gauges and ultrasonic thickness gauges.",
            ["weld size", "measurement", "throat"],
            1.0,
        ),
    ]
    for doc in docs:
        index.add_document(doc)