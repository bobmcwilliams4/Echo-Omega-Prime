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
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs = 0
        self.total_length = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_length += len(tokens)
            self.total_docs += 1
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freq[term] += 1
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        avgdl = self._get_avg_doc_length()
        for doc_id, doc in self.documents.items():
            score = self._score_bm25(doc_id, query_terms, avgdl)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            score = 0.7 * score + 0.3 * tfidf_score
            if score > 0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self._get_avg_doc_length(),
            "unique_terms": len(self.term_doc_freq)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str], avgdl: float) -> float:
        tf = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 0)
        score = 0.0
        doc = self.documents[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / avgdl)
            score += idf * f * (self.k1 + 1) / denom
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vec = self._tfidf_cache[doc_id]
        else:
            tf = self.term_freqs.get(doc_id, Counter())
            doc_len = self.doc_lengths.get(doc_id, 0)
            tfidf_vec = {}
            for term, freq in tf.items():
                tf_norm = freq / doc_len if doc_len > 0 else 0
                idf = self._compute_idf(term)
                tfidf_vec[term] = tf_norm * idf
            self._tfidf_cache[doc_id] = tfidf_vec
        score = 0.0
        for term in query_terms:
            score += tfidf_vec.get(term, 0.0)
        return score

    def _get_avg_doc_length(self) -> float:
        if self.total_docs == 0:
            return 0.0
        return self.total_length / self.total_docs

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
                _seed_documents(_search_index_instance)
    return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "CFRP Quasi-Isotropic Layup Design Principles",
            "Quasi-isotropic layups in carbon fiber reinforced polymers (CFRP) are achieved by orienting plies at 0, 90, and ±45 degrees. This design ensures uniform in-plane properties and is critical for primary aircraft structures. Typical stacking sequences include [0/±45/90]s. Layup optimization considers fiber volume fraction, ply thickness, and damage tolerance.",
            ["CFRP", "Layup", "Quasi-Isotropic", "Aircraft", "Design"],
            1.2
        ),
        SearchDocument(
            2,
            "Aluminum 7075-T6 vs 2024-T3 Alloy Selection",
            "7075-T6 offers superior strength and fatigue resistance compared to 2024-T3, but 2024-T3 provides better fracture toughness and corrosion resistance. Selection depends on application: wing spars favor 7075-T6, while fuselage skins often use 2024-T3. Both alloys require proper corrosion protection schemes.",
            ["Aluminum", "7075-T6", "2024-T3", "Alloy", "Selection"],
            1.0
        ),
        SearchDocument(
            3,
            "Titanium Ti-6Al-4V Applications and Heat Treatment",
            "Ti-6Al-4V is widely used in aircraft engine components and airframe structures due to its high strength-to-weight ratio and corrosion resistance. Heat treatment processes like solution treatment and aging optimize mechanical properties. Typical applications include landing gear, fasteners, and turbine disks.",
            ["Titanium", "Ti-6Al-4V", "Heat Treatment", "Applications"],
            1.1
        ),
        SearchDocument(
            4,
            "Nickel Superalloys for Turbine Hot Section",
            "Nickel-based superalloys such as Inconel 718 and Rene 88 are essential for turbine hot section components due to their high-temperature strength and oxidation resistance. These alloys undergo precipitation hardening and advanced casting techniques. Damage tolerance and crack growth resistance are critical for engine reliability.",
            ["Nickel", "Superalloy", "Turbine", "Hot Section"],
            1.2
        ),
        SearchDocument(
            5,
            "S-N Curve Fatigue Analysis and Endurance Limit",
            "S-N curves plot stress amplitude versus number of cycles to failure, revealing the endurance limit for metals like aluminum and titanium. Fatigue analysis considers loading spectra, mean stress effects, and environmental factors. Statistical allowables are derived from S-N data for design certification.",
            ["Fatigue", "S-N Curve", "Endurance Limit", "Analysis"],
            1.0
        ),
        SearchDocument(
            6,
            "Paris Law Crack Growth and Damage Tolerance",
            "Paris Law describes crack growth rate (da/dN) as a function of stress intensity range (ΔK). Damage tolerance analysis uses Paris parameters (C, m) to predict crack propagation in aircraft structures. Inspection intervals and fail-safe design are based on crack growth modeling.",
            ["Paris Law", "Crack Growth", "Damage Tolerance"],
            1.1
        ),
        SearchDocument(
            7,
            "CMH-17 Statistical Allowables Development",
            "CMH-17 provides guidelines for developing statistical allowables for composite materials. Allowables are based on test data, typically using A-basis (99%/95%) and B-basis (90%/95%) values. Proper sampling and data analysis ensure reliability for certification and structural design.",
            ["CMH-17", "Statistical Allowables", "Composite", "Certification"],
            1.2
        ),
        SearchDocument(
            8,
            "BVID and Compression After Impact (CAI) Testing",
            "Barely Visible Impact Damage (BVID) is critical for CFRP structures. CAI testing evaluates residual strength after impact, using drop-weight or quasi-static tests. Results inform design allowables and maintenance procedures for aircraft composite panels.",
            ["BVID", "CAI", "Impact", "Testing", "CFRP"],
            1.1
        ),
        SearchDocument(
            9,
            "Corrosion Protection Schemes for Aluminum Alloys",
            "Aluminum alloys require corrosion protection such as anodizing, conversion coatings, and paint systems. Chromate conversion and alodine treatments improve durability. Selection of protection scheme depends on alloy, environment, and maintenance requirements.",
            ["Corrosion", "Aluminum", "Protection", "Schemes"],
            1.0
        ),
        SearchDocument(
            10,
            "Additive Manufacturing Qualification for Aerospace",
            "Qualification of additive manufacturing (AM) processes for aerospace includes material characterization, process control, and mechanical testing. Powder bed fusion and directed energy deposition are common AM methods. Qualification standards address defects, microstructure, and fatigue performance.",
            ["Additive Manufacturing", "Qualification", "Aerospace"],
            1.2
        ),
        SearchDocument(
            11,
            "Fiber Volume Fraction and Void Content in Composites",
            "Fiber volume fraction (FVF) is a key parameter in composite design, affecting strength and stiffness. Void content must be minimized to ensure quality. Measurement techniques include burn-off, microscopy, and ultrasonic inspection. Typical FVF for aerospace CFRP is 55-60%.",
            ["Fiber Volume Fraction", "Void Content", "Composites"],
            1.1
        ),
        SearchDocument(
            12,
            "Resin Transfer Molding (RTM) Process Overview",
            "RTM is a closed-mold process for manufacturing composite parts. Resin is injected into a mold containing dry fiber preforms. RTM enables complex shapes and high fiber volume fractions. Process parameters include injection pressure, mold temperature, and cure cycle.",
            ["RTM", "Resin Transfer Molding", "Process", "Composites"],
            1.0
        ),
        SearchDocument(
            13,
            "Honeycomb Core Selection and Properties",
            "Honeycomb cores are used in sandwich structures for lightweight stiffness. Materials include aluminum, Nomex, and Kevlar. Properties depend on cell size, density, and material. Selection considers compressive strength, shear modulus, and fire resistance.",
            ["Honeycomb", "Core", "Selection", "Properties"],
            1.2
        ),
        SearchDocument(
            14,
            "Composite Damage Tolerance and Inspection",
            "Damage tolerance in composites involves understanding impact, delamination, and fatigue. Inspection methods include ultrasonic, thermography, and visual techniques. Maintenance strategies are based on damage size, location, and residual strength.",
            ["Composite", "Damage Tolerance", "Inspection"],
            1.1
        ),
        SearchDocument(
            15,
            "Aluminum Alloy Heat Treatment and Temper Designations",
            "Heat treatment of aluminum alloys includes solution heat treatment, quenching, and aging. Temper designations (T3, T6, T7) indicate mechanical property levels. Proper heat treatment enhances strength, ductility, and corrosion resistance.",
            ["Aluminum", "Heat Treatment", "Temper", "Designations"],
            1.0
        ),
        SearchDocument(
            16,
            "Titanium Alloy Corrosion and Surface Treatments",
            "Titanium alloys exhibit excellent corrosion resistance. Surface treatments such as anodizing and shot peening improve fatigue life and wear resistance. Applications include engine components and fasteners exposed to harsh environments.",
            ["Titanium", "Corrosion", "Surface Treatments"],
            1.1
        ),
        SearchDocument(
            17,
            "Fatigue Life Prediction for Aircraft Structures",
            "Fatigue life prediction uses S-N curves, crack growth models, and loading spectra. Damage tolerance and inspection intervals are determined by predicted crack propagation. Statistical methods ensure reliability for certification.",
            ["Fatigue", "Life Prediction", "Aircraft", "Structures"],
            1.2
        ),
        SearchDocument(
            18,
            "Composite Ply Drop and Transition Design",
            "Ply drops and transitions in composite laminates require careful design to avoid stress concentrations. Techniques include tapering, staggered drops, and resin-rich zones. Analysis considers interlaminar stresses and damage initiation.",
            ["Composite", "Ply Drop", "Transition", "Design"],
            1.0
        ),
        SearchDocument(
            19,
            "Advanced Aluminum Alloys for Aircraft",
            "Advanced aluminum alloys such as 7055 and 7150 offer improved strength and corrosion resistance. Applications include wing structures and fuselage frames. Selection criteria include fatigue, fracture toughness, and manufacturability.",
            ["Aluminum", "Advanced Alloys", "Aircraft"],
            1.1
        ),
        SearchDocument(
            20,
            "Titanium Alloy Fatigue and Crack Growth",
            "Fatigue and crack growth in titanium alloys are influenced by microstructure, heat treatment, and loading conditions. Paris Law parameters are used for damage tolerance analysis. Applications include engine disks and landing gear.",
            ["Titanium", "Fatigue", "Crack Growth"],
            1.2
        ),
        SearchDocument(
            21,
            "Nickel Superalloy Heat Treatment and Microstructure",
            "Heat treatment of nickel superalloys involves solution treatment, aging, and precipitation hardening. Microstructure control is critical for high-temperature performance. Applications include turbine blades and combustor liners.",
            ["Nickel", "Superalloy", "Heat Treatment", "Microstructure"],
            1.1
        ),
        SearchDocument(
            22,
            "Composite Panel CAI and BVID Allowables",
            "Compression After Impact (CAI) and Barely Visible Impact Damage (BVID) allowables are derived from testing composite panels. Results inform design and maintenance for aircraft structures. Statistical methods ensure reliability.",
            ["Composite", "CAI", "BVID", "Allowables"],
            1.0
        ),
        SearchDocument(
            23,
            "Corrosion Testing Methods for Aluminum Alloys",
            "Corrosion testing includes salt spray, humidity, and cyclic exposure tests. Results guide selection of protection schemes for aluminum alloys in aircraft. Testing standards include ASTM B117 and ISO 9227.",
            ["Corrosion", "Testing", "Aluminum", "Alloys"],
            1.1
        ),
        SearchDocument(
            24,
            "Additive Manufacturing Defects and Inspection",
            "Defects in additive manufacturing include porosity, lack of fusion, and residual stresses. Inspection methods include X-ray, ultrasonic, and CT scanning. Qualification standards require defect detection and process control.",
            ["Additive Manufacturing", "Defects", "Inspection"],
            1.2
        ),
        SearchDocument(
            25,
            "Fiber Volume Fraction Optimization in RTM",
            "Optimizing fiber volume fraction in RTM involves controlling preform architecture and resin flow. High FVF improves mechanical properties but increases processing complexity. Quality control ensures low void content and consistent performance.",
            ["Fiber Volume Fraction", "RTM", "Optimization"],
            1.1
        ),
        SearchDocument(
            26,
            "Honeycomb Core Bonding and Failure Modes",
            "Bonding honeycomb cores to face sheets requires adhesive selection and surface preparation. Failure modes include delamination, core shear, and face sheet buckling. Testing standards ensure structural integrity.",
            ["Honeycomb", "Core", "Bonding", "Failure Modes"],
            1.0
        ),
        SearchDocument(
            27,
            "Composite Laminate Fatigue and Damage Mechanisms",
            "Fatigue in composite laminates involves matrix cracking, delamination, and fiber breakage. Damage mechanisms depend on ply orientation, loading, and environment. S-N curves and CAI testing inform design allowables.",
            ["Composite", "Laminate", "Fatigue", "Damage"],
            1.2
        ),
        SearchDocument(
            28,
            "Aluminum Alloy Corrosion Fatigue",
            "Corrosion fatigue in aluminum alloys is influenced by environment, stress, and protection schemes. Analysis combines S-N curves and corrosion testing. Applications include aircraft skins and structural members.",
            ["Aluminum", "Corrosion", "Fatigue"],
            1.1
        ),
        SearchDocument(
            29,
            "Titanium Alloy Additive Manufacturing",
            "Additive manufacturing of titanium alloys enables complex geometries and weight reduction. Process qualification includes microstructure analysis, mechanical testing, and defect detection. Applications include engine components and brackets.",
            ["Titanium", "Additive Manufacturing", "Qualification"],
            1.0
        ),
        SearchDocument(
            30,
            "Nickel Superalloy Fatigue and Crack Growth",
            "Fatigue and crack growth in nickel superalloys are critical for turbine reliability. Paris Law and S-N curves are used for damage tolerance analysis. Heat treatment and microstructure control optimize performance.",
            ["Nickel", "Superalloy", "Fatigue", "Crack Growth"],
            1.2
        ),
        SearchDocument(
            31,
            "Composite Sandwich Panel Design and Honeycomb Cores",
            "Sandwich panels use honeycomb cores for lightweight stiffness. Design considers face sheet material, core density, and bonding methods. Applications include aircraft floors, control surfaces, and radomes.",
            ["Composite", "Sandwich Panel", "Honeycomb", "Design"],
            1.1
        ),
        SearchDocument(
            32,
            "CMH-17 Data Analysis for Composite Allowables",
            "CMH-17 outlines statistical methods for analyzing composite test data. Proper sampling, outlier detection, and regression analysis ensure accurate A-basis and B-basis allowables for certification.",
            ["CMH-17", "Data Analysis", "Composite", "Allowables"],
            1.0
        ),
        SearchDocument(
            33,
            "Resin Transfer Molding Defects and Quality Control",
            "RTM defects include dry spots, voids, and resin-rich zones. Quality control involves process monitoring, ultrasonic inspection, and destructive testing. Standards ensure consistent mechanical properties.",
            ["RTM", "Defects", "Quality Control"],
            1.1
        ),
        SearchDocument(
            34,
            "Aluminum Alloy Selection for Aircraft Structures",
            "Selection of aluminum alloys for aircraft structures considers strength, fatigue, corrosion resistance, and manufacturability. 7075-T6, 2024-T3, and advanced alloys are used for wings, fuselage, and landing gear.",
            ["Aluminum", "Selection", "Aircraft", "Structures"],
            1.2
        ),
        SearchDocument(
            35,
            "Composite Ply Orientation and Quasi-Isotropic Properties",
            "Ply orientation in composite laminates determines mechanical properties. Quasi-isotropic layups use 0, 90, and ±45 degree plies for uniform in-plane strength. Analysis includes fiber volume fraction and ply thickness.",
            ["Composite", "Ply Orientation", "Quasi-Isotropic"],
            1.1
        ),
    ]
    for doc in docs:
        index.add_document(doc)