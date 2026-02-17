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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._re_token = re.compile(r'\b\w+\b', re.UNICODE)
        self._tf_cache: Dict[int, Dict[str, float]] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._re_token.findall(text)]

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            length = len(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = length
            tf = Counter(tokens)
            for term, freq in tf.items():
                self.inverted_index[term][doc.id] = freq
                self.doc_freqs[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self._tf_cache[doc.id] = {term: freq / length for term, freq in tf.items()}
            self._tfidf_cache[doc.id] = {}
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

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        length = self.doc_lengths[doc_id]
        for term in set(query_terms):
            freq = self.inverted_index.get(term, {}).get(doc_id, 0)
            if freq == 0:
                continue
            idf = self._compute_idf(term)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * (length / self.avg_doc_length))
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tfidf = 0.0
        doc = self.documents[doc_id]
        tf_dict = self._tf_cache[doc_id]
        for term in set(query_terms):
            tf = tf_dict.get(term, 0.0)
            idf = self._compute_idf(term)
            tfidf += tf * idf
        return tfidf * doc.weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            combined_score = 0.7 * bm25_score + 0.3 * tfidf_score
            snippet = self._make_snippet(self.documents[doc_id], query_terms)
            scored.append(SearchResult(doc_id, combined_score, self.documents[doc_id].title, snippet))
        scored.sort(key=lambda r: r.score, reverse=True)
        return scored[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:snippet_len] + ('...' if len(content) > snippet_len else '')
        start = max(positions[0] - 10, 0)
        end = min(start + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:snippet_len] + ('...' if len(snippet) > snippet_len else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'vocab_size': len(self.inverted_index),
        }

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "ASME Section VIII Division 1 Shell Thickness Calculation",
            "Calculate minimum required shell thickness for internal pressure using UG-27. Consider design pressure, diameter, allowable stress, joint efficiency, and corrosion allowance. Formula: t = (P*R)/(SE-0.6P) + CA.",
            ["ASME VIII-1", "shell", "thickness", "pressure vessel"],
            1.0
        ),
        SearchDocument(
            2,
            "Ellipsoidal Head Design per ASME VIII-1",
            "Ellipsoidal (2:1) heads are designed per UG-32. Minimum thickness: t = (P*D)/(2SE-0.2P) + CA. Ensure knuckle radius and crown radius per code.",
            ["ellipsoidal head", "ASME VIII-1", "head design"],
            1.0
        ),
        SearchDocument(
            3,
            "Hemispherical Head Design - Most Efficient Geometry",
            "Hemispherical heads require less thickness than other types for the same pressure and diameter. Use t = (P*R)/(2SE-0.2P) + CA. Ideal for high-pressure applications.",
            ["hemispherical head", "efficient", "pressure vessel"],
            1.0
        ),
        SearchDocument(
            4,
            "Torispherical Head Design (ASME F&D Head)",
            "Torispherical (flanged and dished) heads per ASME VIII-1 UG-32: t = (P*D)/(2SE+0.2P) + CA. Check knuckle and crown radii. Less efficient than ellipsoidal or hemispherical.",
            ["torispherical head", "ASME F&D", "head design"],
            1.0
        ),
        SearchDocument(
            5,
            "Nozzle Reinforcement - Area Replacement Method",
            "Nozzle reinforcement per UG-37: Required area = area removed by nozzle opening. Reinforcement may include excess shell, nozzle wall, welds, and reinforcing pads.",
            ["nozzle", "reinforcement", "area replacement", "ASME VIII-1"],
            1.0
        ),
        SearchDocument(
            6,
            "ASME Section VIII Division 2 - Design by Analysis",
            "Division 2 allows design by analysis: stress categorization, elastic/plastic analysis, and fatigue. More rigorous, allows higher allowable stresses than Division 1.",
            ["ASME VIII-2", "design by analysis", "pressure vessel"],
            1.0
        ),
        SearchDocument(
            7,
            "Maximum Allowable Working Pressure (MAWP) Calculation",
            "MAWP is the maximum pressure a vessel can withstand at the top of the vessel in normal operating position. Calculated using minimum thickness, material strength, and joint efficiency.",
            ["MAWP", "pressure vessel", "calculation"],
            1.0
        ),
        SearchDocument(
            8,
            "Hydrostatic Testing Requirements per ASME VIII-1",
            "Hydrotest pressure = 1.3 x MAWP x (S_test/S_design). Hold for 10 minutes. All welds must be visually inspected before and after test.",
            ["hydrostatic test", "ASME VIII-1", "pressure vessel"],
            1.0
        ),
        SearchDocument(
            9,
            "Saddle Support Design Using Zick Analysis",
            "Zick analysis evaluates stresses in horizontal vessel saddles: bending, shear, and local shell stresses. Check for allowable limits per code.",
            ["saddle support", "Zick analysis", "pressure vessel"],
            1.0
        ),
        SearchDocument(
            10,
            "Material Selection - Carbon Steel SA-516 Grade 70",
            "SA-516 Gr. 70 is a common carbon steel for pressure vessels. Good weldability, toughness, and strength. Check MDMT and corrosion allowance.",
            ["material selection", "SA-516", "carbon steel"],
            1.0
        ),
        SearchDocument(
            11,
            "Material Selection - Stainless Steel SA-240 Type 304/316",
            "SA-240 304/316 stainless steels are used for corrosion resistance. 316 offers better resistance to chlorides. Consider cost, fabrication, and service environment.",
            ["material selection", "SA-240", "stainless steel"],
            1.0
        ),
        SearchDocument(
            12,
            "Post-Weld Heat Treatment (PWHT) Requirements",
            "PWHT relieves residual stresses and improves toughness. Required per UCS-56 for certain thicknesses and materials. Follow time and temperature per code.",
            ["PWHT", "post-weld heat treatment", "ASME VIII-1"],
            1.0
        ),
        SearchDocument(
            13,
            "Non-Destructive Examination (NDE) Requirements",
            "NDE methods: radiography, ultrasonic, magnetic particle, dye penetrant. Required for weld quality assurance per ASME VIII-1, depending on joint category and service.",
            ["NDE", "non-destructive examination", "ASME VIII-1"],
            1.0
        ),
        SearchDocument(
            14,
            "API 510 In-Service Inspection and Remaining Life Assessment",
            "API 510 covers inspection, repair, alteration, and rerating of in-service pressure vessels. Remaining life = (t_actual - t_min) / corrosion rate.",
            ["API 510", "inspection", "remaining life"],
            1.0
        ),
        SearchDocument(
            15,
            "Fitness-for-Service Assessment per API 579-1/ASME FFS-1",
            "API 579-1/ASME FFS-1 provides procedures for assessing flaws, corrosion, and remaining life. Levels 1-3 analyses based on flaw severity and data.",
            ["fitness-for-service", "API 579-1", "ASME FFS-1"],
            1.0
        ),
        SearchDocument(
            16,
            "Oilfield Production Vessels per API 12F and 12J",
            "API 12F and 12J specify design, fabrication, and testing of oilfield production vessels. Standardized sizes and construction details.",
            ["API 12F", "API 12J", "oilfield vessel"],
            1.0
        ),
        SearchDocument(
            17,
            "Wind and Seismic Loads per ASCE 7",
            "ASCE 7 provides procedures for determining wind and seismic loads on pressure vessels. Consider vessel geometry, location, and anchorage.",
            ["ASCE 7", "wind load", "seismic load"],
            1.0
        ),
        SearchDocument(
            18,
            "National Board Registration and R-Stamp",
            "Pressure vessels must be registered with the National Board. R-Stamp required for repairs and alterations by authorized organizations.",
            ["National Board", "R-Stamp", "registration"],
            1.0
        ),
        SearchDocument(
            19,
            "Corrosion Allowance Selection and Design Life",
            "Corrosion allowance is added to thickness to compensate for expected metal loss. Select based on service, design life, and inspection interval.",
            ["corrosion allowance", "design life", "pressure vessel"],
            1.0
        ),
        SearchDocument(
            20,
            "Minimum Design Metal Temperature (MDMT) and Impact Testing",
            "MDMT is the lowest temperature at which the vessel is designed. Impact testing required if MDMT is below certain limits per UCS-66.",
            ["MDMT", "impact testing", "ASME VIII-1"],
            1.0
        ),
        SearchDocument(
            21,
            "Fabrication Tolerances per ASME VIII-1 UG-80 and UG-81",
            "UG-80 and UG-81 specify tolerances for out-of-roundness, straightness, and alignment. Critical for fit-up and pressure integrity.",
            ["fabrication tolerance", "UG-80", "UG-81"],
            1.0
        ),
        SearchDocument(
            22,
            "Joint Efficiency in Pressure Vessel Design",
            "Joint efficiency depends on weld type and inspection. Fully radiographed butt welds: E=1.0. Partial: E=0.85 or less. Impacts required thickness.",
            ["joint efficiency", "weld", "ASME VIII-1"],
            1.0
        ),
        SearchDocument(
            23,
            "External Pressure Design per ASME VIII-1 UG-28",
            "UG-28 covers shell and head design for external pressure. Use external pressure charts and stiffening rings as required.",
            ["external pressure", "UG-28", "pressure vessel"],
            1.0
        ),
        SearchDocument(
            24,
            "Welded vs. Forged Nozzle Attachments",
            "Welded nozzles are most common; forged nozzles used for high pressure or severe service. Both require reinforcement per code.",
            ["nozzle", "welded", "forged", "ASME VIII-1"],
            1.0
        ),
        SearchDocument(
            25,
            "Design of Supports for Vertical Pressure Vessels",
            "Vertical vessels may use skirts, legs, or brackets. Design for dead load, wind, seismic, and thermal expansion.",
            ["vertical vessel", "support", "skirt", "ASME VIII-1"],
            1.0
        ),
        SearchDocument(
            26,
            "Calculation of Required Thickness for Flat Heads",
            "Flat heads are weaker and require greater thickness. Use UG-34 formulas. Consider unsupported diameter and edge conditions.",
            ["flat head", "thickness", "UG-34"],
            1.0
        ),
        SearchDocument(
            27,
            "Design Pressure and Design Temperature",
            "Design pressure is the maximum pressure for design. Design temperature is the highest temperature for design. Both affect material selection and thickness.",
            ["design pressure", "design temperature", "ASME VIII-1"],
            1.0
        ),
        SearchDocument(
            28,
            "Weld Category and Inspection Requirements",
            "ASME VIII-1 defines weld categories (A, B, C, D) for inspection and testing. Category A: longitudinal, Category B: circumferential, etc.",
            ["weld category", "inspection", "ASME VIII-1"],
            1.0
        ),
        SearchDocument(
            29,
            "Calculation of Required Thickness for Conical Sections",
            "Conical shells use UG-32 formulas. Consider large end, small end, and junction reinforcement. Check for local stresses.",
            ["conical shell", "thickness", "UG-32"],
            1.0
        ),
        SearchDocument(
            30,
            "Design for Cyclic Service and Fatigue",
            "Cyclic service requires fatigue analysis. Division 2 provides detailed procedures. Consider stress concentration and material selection.",
            ["cyclic service", "fatigue", "ASME VIII-2"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)