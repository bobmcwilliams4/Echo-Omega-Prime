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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_tokens: Dict[int, List[str]] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)  # term -> doc_id -> freq
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[Tuple[int, str], float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            for term in tokens:
                self.inverted_index[term][doc.id] = self.inverted_index[term].get(doc.id, 0) + 1
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()
            self.tf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            snippet = self._make_snippet(doc, query_terms)
            scored_results.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocabulary_size": len(self.inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        term_freqs = Counter(tokens)
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * doc_len / (self.avg_doc_length + 1e-9))
            score += idf * ((tf * (self.bm25_k1 + 1)) / (denom + 1e-9))
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        term_freqs = Counter(tokens)
        score = 0.0
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            norm_tf = tf / doc_len
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score * doc.weight

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

# Singleton factory
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
            "API 6A Pressure Rating Selection",
            "Guidelines for selecting pressure ratings for wellhead equipment per API 6A. Includes tables for 2,000 to 20,000 psi. Consider maximum anticipated surface pressure and temperature derating.",
            ["api-6a", "pressure-rating", "wellhead"],
            1.0
        ),
        SearchDocument(
            2,
            "Material Class Selection (API 6A)",
            "Material classes AA, BB, CC, DD, EE, FF, HH define material properties for sour and non-sour environments. Selection depends on H2S/CO2 content, temperature, and pressure.",
            ["api-6a", "material-class", "sour-service"],
            1.0
        ),
        SearchDocument(
            3,
            "Product Specification Level (PSL) Requirements",
            "API 6A defines PSL 1 to PSL 4. PSL 3 and 4 require additional NDE, traceability, and documentation. PSL selection is based on well criticality and operator requirements.",
            ["api-6a", "psl", "traceability"],
            1.0
        ),
        SearchDocument(
            4,
            "Casing Head (Braden Head) Configuration",
            "Casing heads provide the primary interface between surface casing and wellhead. Options include weld-on, slip-on, and threaded. Braden head design allows for pressure testing and annulus access.",
            ["casing-head", "braden-head", "wellhead"],
            1.0
        ),
        SearchDocument(
            5,
            "Tubing Head Spool and Hanger",
            "Tubing head spools support tubing hangers and seal the tubing-casing annulus. Hanger types: mandrel and slip. Secondary seals may be elastomeric or metal-to-metal.",
            ["tubing-head", "tubing-hanger", "wellhead"],
            1.0
        ),
        SearchDocument(
            6,
            "Christmas Tree Selection: Vertical vs Horizontal",
            "Vertical trees are standard for onshore and shallow offshore wells. Horizontal trees allow tubing access with the tree in place, preferred for subsea and high intervention wells.",
            ["christmas-tree", "vertical", "horizontal", "wellhead"],
            1.0
        ),
        SearchDocument(
            7,
            "Choke Valve Selection: Positive vs Adjustable",
            "Positive chokes use fixed orifice beans, suitable for stable flow. Adjustable chokes allow variable flow control, used during well cleanup and testing.",
            ["choke-valve", "positive", "adjustable"],
            1.0
        ),
        SearchDocument(
            8,
            "Wellhead Seal Technology: Metal vs Elastomeric",
            "Metal-to-metal seals offer high integrity for HPHT and sour service. Elastomeric seals provide flexibility but are limited by temperature and chemical compatibility.",
            ["seal", "metal", "elastomeric", "wellhead"],
            1.0
        ),
        SearchDocument(
            9,
            "Flanged vs Studded Connections",
            "Flanged connections are bolted and allow easier maintenance. Studded connections are compact and common in space-constrained applications, such as subsea trees.",
            ["flanged", "studded", "connections"],
            1.0
        ),
        SearchDocument(
            10,
            "Pressure Testing and Verification (API 6A)",
            "All wellhead equipment must be pressure tested per API 6A. PR1 and PR2 tests verify pressure integrity and performance under temperature cycling.",
            ["pressure-testing", "api-6a", "pr1", "pr2"],
            1.0
        ),
        SearchDocument(
            11,
            "Surface Safety Valve (SSV) Requirements",
            "SSVs are required for surface-controlled subsurface safety. Must meet API 6A and 14A. Selection based on pressure rating, material class, and actuation method.",
            ["ssv", "surface-safety-valve", "api-6a"],
            1.0
        ),
        SearchDocument(
            12,
            "Cameron vs FMC vs Dril-Quip Wellhead Systems",
            "Cameron, FMC, and Dril-Quip offer proprietary wellhead systems. Key differences include hanger running tools, seal designs, and field serviceability.",
            ["cameron", "fmc", "dril-quip", "wellhead"],
            1.0
        ),
        SearchDocument(
            13,
            "Subsea Wellhead vs Surface Wellhead",
            "Subsea wellheads are designed for remote operation and intervention. Surface wellheads are accessible and allow direct manual operation and maintenance.",
            ["subsea", "surface", "wellhead"],
            1.0
        ),
        SearchDocument(
            14,
            "Casing Hanger Selection: Slip vs Mandrel",
            "Slip-type hangers use slips to grip casing; mandrel hangers suspend casing via a shoulder. Mandrel hangers provide better sealing for HPHT wells.",
            ["casing-hanger", "slip", "mandrel"],
            1.0
        ),
        SearchDocument(
            15,
            "Temperature Class and Derating",
            "API 6A temperature classes range from K (-60°C) to X (+250°C). Pressure ratings must be derated for high temperatures according to API tables.",
            ["temperature-class", "derating", "api-6a"],
            1.0
        ),
        SearchDocument(
            16,
            "PR1 vs PR2 Performance Requirements",
            "PR1 requires basic pressure testing. PR2 includes thermal cycling and endurance testing. PR2 is mandatory for critical service and subsea applications.",
            ["pr1", "pr2", "performance", "api-6a"],
            1.0
        ),
        SearchDocument(
            17,
            "Wellhead Valve Types: Gate vs Ball",
            "Gate valves are standard for wellhead isolation. Ball valves offer quick operation and are used in some high-flow applications.",
            ["valve", "gate", "ball", "wellhead"],
            1.0
        ),
        SearchDocument(
            18,
            "API Monogram Licensing and Verification",
            "API monogram indicates compliance with API 6A. Manufacturers must undergo audits and maintain quality management systems.",
            ["api-monogram", "licensing", "verification"],
            1.0
        ),
        SearchDocument(
            19,
            "HPHT Wellhead Equipment Considerations",
            "High Pressure High Temperature (HPHT) wells require special materials, metal-to-metal seals, and PR2 testing. Consult API 6A Annex F.",
            ["hpht", "wellhead", "api-6a"],
            1.0
        ),
        SearchDocument(
            20,
            "Annulus Access and Monitoring",
            "Wellhead systems should provide annulus access for pressure monitoring and chemical injection. Side outlets and monitoring ports are standard.",
            ["annulus", "monitoring", "wellhead"],
            1.0
        ),
        SearchDocument(
            21,
            "Elastomer Selection for Wellhead Seals",
            "Elastomer selection is critical for chemical compatibility and temperature rating. Common types: NBR, HNBR, FKM. Refer to API 6A Annex G.",
            ["elastomer", "seal", "api-6a"],
            1.0
        ),
        SearchDocument(
            22,
            "Double Studded Adapter Flanges (DSAF)",
            "DSAFs allow connection between different flange sizes or pressure ratings. Used for wellhead upgrades and tie-ins.",
            ["dsaf", "flange", "adapter"],
            1.0
        ),
        SearchDocument(
            23,
            "Wellhead Lockdown Systems",
            "Lockdown systems prevent hanger movement under high pressure or thermal loads. Mandated for subsea and HPHT wells.",
            ["lockdown", "wellhead", "hpht"],
            1.0
        ),
        SearchDocument(
            24,
            "Wellhead Running Tools",
            "Specialized running tools are required for casing and tubing hanger installation. Selection depends on wellhead system and hanger type.",
            ["running-tool", "wellhead", "hanger"],
            1.0
        ),
        SearchDocument(
            25,
            "API 6A PSL Documentation Requirements",
            "PSL 3 and 4 require full material traceability, NDE, and pressure test records. Documentation must be retained for the equipment lifecycle.",
            ["psl", "documentation", "api-6a"],
            1.0
        ),
        SearchDocument(
            26,
            "Metal-to-Metal Seal Qualification",
            "Metal-to-metal seals must pass gas and liquid pressure tests per API 6A Annex F. Qualification includes multiple pressure and temperature cycles.",
            ["metal-to-metal", "seal", "qualification"],
            1.0
        ),
        SearchDocument(
            27,
            "Subsea Wellhead Connector Types",
            "Common connector types: clamp, collet, and mandrel. Selection depends on intervention requirements and system compatibility.",
            ["subsea", "connector", "wellhead"],
            1.0
        ),
        SearchDocument(
            28,
            "API 6A Marking and Traceability",
            "All wellhead equipment must be marked with API monogram, PSL, material class, and pressure rating. Traceability is required for PSL 2 and above.",
            ["api-6a", "marking", "traceability"],
            1.0
        ),
        SearchDocument(
            29,
            "Welded vs Threaded Casing Heads",
            "Welded casing heads provide higher integrity for HPHT and sour service. Threaded heads are used for low pressure, land wells.",
            ["casing-head", "welded", "threaded"],
            1.0
        ),
        SearchDocument(
            30,
            "API 6A Annex F: HPHT Requirements",
            "Annex F of API 6A details requirements for HPHT equipment, including material testing, seal qualification, and PR2 performance validation.",
            ["api-6a", "annex-f", "hpht"],
            1.0
        ),
        SearchDocument(
            31,
            "Wellhead Adapter Spools",
            "Adapter spools connect wellhead components with different sizes or pressure ratings. Must be rated for maximum anticipated pressure.",
            ["adapter-spool", "wellhead", "connection"],
            1.0
        ),
        SearchDocument(
            32,
            "API 6A PSL 2 NDE Requirements",
            "PSL 2 requires additional NDE such as ultrasonic and magnetic particle inspection for critical components.",
            ["psl-2", "nde", "api-6a"],
            1.0
        ),
        SearchDocument(
            33,
            "Surface Wellhead Test Plugs",
            "Test plugs allow pressure testing of wellhead bores. Selection depends on bore size, pressure rating, and seal type.",
            ["test-plug", "wellhead", "pressure-test"],
            1.0
        ),
        SearchDocument(
            34,
            "API 6A PSL 3G and 4G Gas Testing",
            "PSL 3G and 4G require gas testing for wellhead equipment, simulating service conditions for gas wells.",
            ["psl-3g", "psl-4g", "gas-test"],
            1.0
        ),
        SearchDocument(
            35,
            "API 6A Wellhead Valve Testing",
            "Valve testing per API 6A includes hydrostatic, gas, and low-pressure seat tests. PR2 valves require additional endurance testing.",
            ["valve", "testing", "api-6a"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)