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

# --- SearchIndex Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        doc_scores = defaultdict(float)
        for doc_id, doc in self.documents.items():
            score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            final_score = score * 0.7 + tfidf_score * 0.3
            if final_score > 0:
                doc_scores[doc_id] = final_score * doc.weight
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            return 0.0
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs[doc_id]
        for term in set(query_tokens):
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            idf = self._compute_idf(term)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in set(query_tokens):
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_tokens: List[str], length: int = 160) -> str:
        content_lower = content.lower()
        for term in query_tokens:
            idx = content_lower.find(term)
            if idx != -1:
                start = max(0, idx - 40)
                end = min(len(content), idx + 120)
                snippet = content[start:end]
                return snippet.strip() + ('...' if end < len(content) else '')
        return content[:length].strip() + ('...' if len(content) > length else '')

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_domain_documents(_search_index_instance)
        return _search_index_instance

# --- Domain Documents Seed ---

def _seed_domain_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Texas State Plane Coordinate System Overview",
            "The Texas State Plane Coordinate System (SPCS) is a set of coordinate systems designed for Texas, based on the Lambert Conformal Conic projection. It enables accurate mapping and surveying across the state.",
            ["SPCS", "Texas", "Lambert Conformal Conic", "Coordinate System"],
            1.0
        ),
        SearchDocument(
            2,
            "North Central Zone - Texas SPCS",
            "The North Central Zone of the Texas State Plane Coordinate System covers Dallas, Fort Worth, and surrounding counties. It uses NAD83 and EPSG: 2276 for mapping and surveying.",
            ["North Central Zone", "SPCS", "EPSG:2276", "NAD83"],
            1.0
        ),
        SearchDocument(
            3,
            "NAD83 to NAD27 Transformation",
            "Transforming coordinates from NAD83 to NAD27 in Texas requires applying specific grid shift files and transformation algorithms. The process is critical for legacy data compatibility.",
            ["NAD83", "NAD27", "Transformation", "Grid Shift"],
            1.0
        ),
        SearchDocument(
            4,
            "WGS84 Datum and Texas Mapping",
            "WGS84 is a global geodetic datum used for GPS and mapping. In Texas, WGS84 coordinates can be transformed to State Plane using EPSG codes and projection formulas.",
            ["WGS84", "Datum", "Texas", "EPSG"],
            1.0
        ),
        SearchDocument(
            5,
            "EPSG Codes for Texas State Plane",
            "Texas State Plane Coordinate System zones have unique EPSG codes. For example, EPSG:2276 is for North Central Zone, EPSG:2277 for Central Zone, and EPSG:2278 for South Central Zone.",
            ["EPSG", "Texas", "SPCS", "Zones"],
            1.0
        ),
        SearchDocument(
            6,
            "Lambert Conformal Conic Projection",
            "The Lambert Conformal Conic projection is used for Texas SPCS zones, providing minimal distortion for large east-west extents. It is defined by standard parallels and a central meridian.",
            ["Lambert Conformal Conic", "Projection", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            7,
            "Survey Coordinate Validation in Texas",
            "Validating survey coordinates in Texas involves checking zone, datum, and projection parameters. The G01_survey_coordinate_validator engine automates these checks for accuracy.",
            ["Survey", "Validation", "Texas", "G01_survey_coordinate_validator"],
            1.0
        ),
        SearchDocument(
            8,
            "Datum Shifts and Grid Files",
            "Datum shifts between NAD83 and NAD27 in Texas are performed using grid files such as NADCON. These files provide precise transformation values for each zone.",
            ["Datum Shift", "NADCON", "Grid Files", "Texas"],
            1.0
        ),
        SearchDocument(
            9,
            "Texas SPCS Zone Boundaries",
            "Texas is divided into multiple SPCS zones, each with specific boundaries and EPSG codes. Accurate zone selection is essential for coordinate validation.",
            ["SPCS", "Zone Boundaries", "Texas", "EPSG"],
            1.0
        ),
        SearchDocument(
            10,
            "Coordinate System Projections",
            "Texas SPCS uses Lambert Conformal Conic projection for most zones, but some use Transverse Mercator. Understanding projection type is key for transformations.",
            ["Projection", "Lambert", "Transverse Mercator", "Texas"],
            1.0
        ),
        SearchDocument(
            11,
            "EPSG:2276 - Texas North Central Zone",
            "EPSG:2276 defines the Texas North Central Zone in NAD83. It is used for mapping and surveying in Dallas, Fort Worth, and surrounding areas.",
            ["EPSG:2276", "North Central Zone", "NAD83", "Texas"],
            1.0
        ),
        SearchDocument(
            12,
            "Coordinate Transformation Algorithms",
            "Coordinate transformation between datums and projections in Texas uses algorithms such as Helmert and NADCON. These ensure accurate conversion of survey data.",
            ["Transformation", "Helmert", "NADCON", "Texas"],
            1.0
        ),
        SearchDocument(
            13,
            "Surveying with State Plane Coordinates",
            "Surveyors in Texas use State Plane Coordinates for precise land measurements. The system reduces distortion and simplifies calculations.",
            ["Surveying", "State Plane", "Texas", "Measurement"],
            1.0
        ),
        SearchDocument(
            14,
            "NAD83 - North American Datum 1983",
            "NAD83 is the current geodetic datum for Texas SPCS. It replaced NAD27 and is compatible with modern GPS systems.",
            ["NAD83", "Datum", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            15,
            "NAD27 - North American Datum 1927",
            "NAD27 was the original datum for Texas State Plane. It is now obsolete but still used for legacy data and historical surveys.",
            ["NAD27", "Datum", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            16,
            "Texas Central Zone - EPSG:2277",
            "The Texas Central Zone uses EPSG:2277 for mapping and surveying. It covers Austin, San Antonio, and surrounding counties.",
            ["Central Zone", "EPSG:2277", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            17,
            "Texas South Central Zone - EPSG:2278",
            "EPSG:2278 defines the Texas South Central Zone. It is used for mapping in Houston, Corpus Christi, and adjacent areas.",
            ["South Central Zone", "EPSG:2278", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            18,
            "G01_survey_coordinate_validator Engine",
            "The G01_survey_coordinate_validator engine validates Texas SPCS coordinates, ensuring correct zone, datum, and projection parameters for survey data.",
            ["G01_survey_coordinate_validator", "Validation", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            19,
            "Texas SPCS and GIS Integration",
            "Texas SPCS coordinates are widely used in GIS applications for mapping, planning, and analysis. Integration with EPSG codes ensures interoperability.",
            ["GIS", "SPCS", "Texas", "EPSG"],
            1.0
        ),
        SearchDocument(
            20,
            "Lambert Conformal Conic Parameters",
            "Lambert Conformal Conic projection parameters for Texas SPCS include standard parallels, central meridian, and false easting/northing.",
            ["Lambert Conformal Conic", "Parameters", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            21,
            "Coordinate Validation Rules",
            "Coordinate validation in Texas requires checking zone boundaries, datum, projection, and EPSG code. Automated tools like G01_survey_coordinate_validator simplify this process.",
            ["Validation", "Rules", "Texas", "G01_survey_coordinate_validator"],
            1.0
        ),
        SearchDocument(
            22,
            "EPSG Database for Texas",
            "The EPSG database contains codes for all Texas SPCS zones. It is essential for accurate coordinate transformations and GIS integration.",
            ["EPSG", "Database", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            23,
            "Survey Data Conversion",
            "Converting survey data between NAD83, NAD27, and WGS84 in Texas requires careful application of transformation algorithms and zone selection.",
            ["Survey Data", "Conversion", "Texas", "Transformation"],
            1.0
        ),
        SearchDocument(
            24,
            "Texas SPCS Zone Selection",
            "Selecting the correct SPCS zone in Texas depends on project location. Each zone has unique parameters and EPSG codes.",
            ["Zone Selection", "SPCS", "Texas", "EPSG"],
            1.0
        ),
        SearchDocument(
            25,
            "Lambert Conformal Conic vs Transverse Mercator",
            "Texas SPCS uses Lambert Conformal Conic for most zones, but Transverse Mercator is used for the westernmost zone. Understanding the differences is important for accurate mapping.",
            ["Lambert Conformal Conic", "Transverse Mercator", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            26,
            "Survey Coordinate Validator Use Cases",
            "The G01_survey_coordinate_validator engine is used for validating survey coordinates in Texas, ensuring compliance with SPCS and EPSG standards.",
            ["G01_survey_coordinate_validator", "Use Cases", "Texas", "SPCS"],
            1.0
        ),
        SearchDocument(
            27,
            "EPSG:2279 - Texas West Zone",
            "EPSG:2279 defines the Texas West Zone, which uses Transverse Mercator projection. It covers El Paso and western Texas counties.",
            ["EPSG:2279", "West Zone", "Transverse Mercator", "Texas"],
            1.0
        ),
        SearchDocument(
            28,
            "Texas SPCS and Survey Accuracy",
            "Texas SPCS provides high accuracy for land surveys, minimizing distortion and simplifying coordinate calculations.",
            ["SPCS", "Survey Accuracy", "Texas", "Land Surveys"],
            1.0
        ),
        SearchDocument(
            29,
            "Datum Transformation Tools",
            "Tools for datum transformation in Texas include NADCON, PROJ, and custom scripts. These tools automate conversion between NAD83, NAD27, and WGS84.",
            ["Datum Transformation", "Tools", "Texas", "NADCON"],
            1.0
        ),
        SearchDocument(
            30,
            "Texas SPCS Zone Parameters",
            "Each Texas SPCS zone has unique parameters, including standard parallels, central meridian, and EPSG code. Accurate parameters are essential for coordinate validation.",
            ["SPCS", "Zone Parameters", "Texas", "EPSG"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)