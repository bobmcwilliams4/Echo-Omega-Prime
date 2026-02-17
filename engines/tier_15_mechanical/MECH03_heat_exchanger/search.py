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
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_tags: Dict[int, List[str]] = {}
        self.total_terms: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            term_freq = Counter(tokens)
            self.term_freqs[doc.id] = term_freq
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_tags[doc.id] = doc.tags
            for term in term_freq:
                self.term_doc_freqs[term][doc.id] = term_freq[term]
            self.total_terms += len(tokens)
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / len(self.doc_lengths) if self.doc_lengths else 0.0
            )
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        doc_snippets: Dict[int, str] = {}
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, freq in self.term_doc_freqs.get(term, {}).items():
                doc = self.documents[doc_id]
                score = self._score_bm25(term, doc_id, freq, idf, doc.weight)
                doc_scores[doc_id] += score
                if doc_id not in doc_snippets:
                    doc_snippets[doc_id] = self._extract_snippet(doc.content, term)
        # TF-IDF scoring for normalization
        tfidf_scores = self._compute_tfidf_scores(query_terms)
        for doc_id in doc_scores:
            doc_scores[doc_id] += tfidf_scores.get(doc_id, 0.0)
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = doc_snippets.get(doc_id, self._extract_snippet(doc.content, query_terms[0] if query_terms else ""))
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "num_documents": len(self.documents),
            "avg_doc_length": self.avg_doc_length,
            "total_terms": self.total_terms,
            "unique_terms": len(self.term_doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        df = len(self.term_doc_freqs.get(term, {}))
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: int, freq: int, idf: float, weight: float) -> float:
        dl = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        k1 = self._bm25_k1
        b = self._bm25_b
        tf = freq
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * dl / avg_dl)
        score = idf * (numerator / denominator) * weight
        return score

    def _extract_snippet(self, content: str, term: str, window: int = 40) -> str:
        content_lower = content.lower()
        term_lower = term.lower()
        idx = content_lower.find(term_lower)
        if idx == -1:
            return content[:window] + "..." if len(content) > window else content
        start = max(0, idx - window // 2)
        end = min(len(content), idx + window // 2)
        snippet = content[start:end]
        return "..." + snippet + "..." if start > 0 else snippet + "..."

    def _compute_tfidf_scores(self, query_terms: List[str]) -> Dict[int, float]:
        tfidf_scores: Dict[int, float] = defaultdict(float)
        N = len(self.documents)
        for term in query_terms:
            df = len(self.term_doc_freqs.get(term, {}))
            if df == 0:
                continue
            idf = math.log(N / (df + 1))
            for doc_id, freq in self.term_doc_freqs[term].items():
                tf = freq / self.doc_lengths[doc_id] if self.doc_lengths[doc_id] > 0 else 0.0
                tfidf_scores[doc_id] += tf * idf
        return tfidf_scores

# Singleton factory for SearchIndex
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# Pre-seed documents for MECH03_heat_exchanger domain
def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "TEMA Classification Overview",
            "Shell-and-tube heat exchangers are classified by TEMA into types such as B, C, E, F, G, H, J, K, L, M, N, P, R, S, T, U, W, X. Each letter represents a specific shell or head configuration. Selection impacts maintenance, performance, and mechanical design.",
            ["TEMA", "classification", "shell-and-tube"],
            1.0
        ),
        SearchDocument(
            2,
            "LMTD vs NTU Method in Thermal Design",
            "The Log Mean Temperature Difference (LMTD) and Number of Transfer Units (NTU) methods are used for thermal design of heat exchangers. LMTD is preferred for known inlet/outlet temperatures, while NTU is used for unknown outlet conditions or optimization.",
            ["LMTD", "NTU", "thermal design"],
            1.0
        ),
        SearchDocument(
            3,
            "Fouling Factor Selection and Impact",
            "Fouling factors are added to design to account for deposit formation on heat transfer surfaces. Selection depends on fluid type, temperature, and maintenance schedule. Higher fouling factors reduce design efficiency and increase required surface area.",
            ["fouling", "design", "heat transfer"],
            1.0
        ),
        SearchDocument(
            4,
            "Tubeside Heat Transfer Coefficient Calculation",
            "Tubeside heat transfer coefficients are calculated using correlations such as Dittus-Boelter for turbulent flow and Sieder-Tate for laminar flow. Tube material, diameter, and flow regime affect the coefficient.",
            ["tubeside", "heat transfer", "coefficient"],
            1.0
        ),
        SearchDocument(
            5,
            "Shellside Heat Transfer Coefficient Calculation",
            "Shellside heat transfer coefficients depend on baffle configuration, shell diameter, and flow pattern. Kern's method is commonly used for estimation. Proper design improves efficiency and reduces pressure drop.",
            ["shellside", "heat transfer", "coefficient"],
            1.0
        ),
        SearchDocument(
            6,
            "Tube Layout and Pitch Selection",
            "Tube layout options include triangular, square, and rotated square patterns. Tube pitch affects heat transfer, pressure drop, and mechanical strength. Minimum pitch is typically 1.25 times the tube outer diameter.",
            ["tube layout", "pitch", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            7,
            "Baffle Design: Types and Spacing",
            "Baffle types include segmental, double segmental, and disk-and-doughnut. Baffle spacing impacts shellside heat transfer and tube support. Closer spacing increases heat transfer but also pressure drop and risk of tube vibration.",
            ["baffle", "design", "spacing"],
            1.0
        ),
        SearchDocument(
            8,
            "ASME Section VIII Mechanical Design",
            "ASME Section VIII sets mechanical design requirements for pressure vessels, including heat exchangers. It covers wall thickness, material selection, and stress analysis. Compliance ensures safety and reliability.",
            ["ASME", "mechanical design", "pressure vessel"],
            1.0
        ),
        SearchDocument(
            9,
            "Tube Vibration Analysis and Prevention",
            "Tube vibration can lead to tube failure in shell-and-tube heat exchangers. Analysis includes flow-induced vibration, resonance, and vortex shedding. Prevention methods include proper baffle spacing and tube support.",
            ["tube vibration", "analysis", "prevention"],
            1.0
        ),
        SearchDocument(
            10,
            "Material Selection for Temperature and Corrosion",
            "Material selection considers temperature, corrosion resistance, and mechanical properties. Common materials include carbon steel, stainless steel, and alloys. Selection impacts longevity and maintenance costs.",
            ["material selection", "corrosion", "temperature"],
            1.0
        ),
        SearchDocument(
            11,
            "Oilfield Heater Treater Heat Transfer Design",
            "Heater treaters in oilfields use shell-and-tube or plate heat exchangers for crude oil heating and separation. Design considers fouling, temperature control, and corrosion resistance.",
            ["oilfield", "heater treater", "heat transfer"],
            1.0
        ),
        SearchDocument(
            12,
            "Plate Heat Exchanger Design and Selection",
            "Plate heat exchangers offer compactness and high efficiency. Design involves plate material, gasket selection, and flow arrangement. Suitable for clean fluids and moderate pressures.",
            ["plate heat exchanger", "design", "selection"],
            1.0
        ),
        SearchDocument(
            13,
            "Air-Cooled Heat Exchanger (ACHE) Design",
            "ACHEs use ambient air as coolant. Design includes tube bundle arrangement, fan selection, and vibration analysis. Used in oil & gas, petrochemical, and power industries.",
            ["air-cooled", "heat exchanger", "ACHE"],
            1.0
        ),
        SearchDocument(
            14,
            "Corrosion Under Insulation (CUI) Prevention",
            "CUI is a major concern for insulated heat exchangers. Prevention includes proper insulation material, sealing, and regular inspection. Stainless steel and aluminum are preferred materials.",
            ["corrosion", "insulation", "CUI"],
            1.0
        ),
        SearchDocument(
            15,
            "Thermal Design: LMTD Correction Factor",
            "LMTD correction factor accounts for heat exchanger configuration, such as multi-pass arrangements. It is calculated using charts or equations based on flow arrangement.",
            ["LMTD", "correction factor", "thermal design"],
            1.0
        ),
        SearchDocument(
            16,
            "Heat Exchanger Pressure Drop Analysis",
            "Pressure drop is analyzed for both shellside and tubeside. Excessive drop can cause operational issues. Calculations use empirical correlations and consider fouling, tube layout, and baffle spacing.",
            ["pressure drop", "analysis", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            17,
            "Mechanical Design: Tube Sheet Thickness",
            "Tube sheet thickness is determined by ASME codes and operational pressure. Proper thickness prevents leakage and tube sheet failure. Material selection is critical.",
            ["tube sheet", "mechanical design", "ASME"],
            1.0
        ),
        SearchDocument(
            18,
            "Heat Exchanger Cleaning and Maintenance",
            "Regular cleaning prevents fouling and maintains efficiency. Methods include chemical cleaning, hydroblasting, and mechanical tube brushing. Maintenance schedules depend on fluid type and operational conditions.",
            ["cleaning", "maintenance", "fouling"],
            1.0
        ),
        SearchDocument(
            19,
            "Heat Exchanger Expansion Joint Design",
            "Expansion joints accommodate thermal expansion and prevent mechanical failure. Design considers temperature, pressure, and material compatibility.",
            ["expansion joint", "design", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            20,
            "Shell-and-Tube Heat Exchanger Flow Arrangements",
            "Common flow arrangements include counterflow, parallel flow, and crossflow. Counterflow maximizes heat transfer efficiency. Selection impacts LMTD and NTU calculations.",
            ["flow arrangement", "shell-and-tube", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            21,
            "Double Pipe Heat Exchanger Design",
            "Double pipe heat exchangers are used for small-scale applications. Design is simple and maintenance is easy. Suitable for high-pressure and temperature duties.",
            ["double pipe", "heat exchanger", "design"],
            1.0
        ),
        SearchDocument(
            22,
            "Heat Exchanger Tube Diameter Selection",
            "Tube diameter affects heat transfer, pressure drop, and mechanical strength. Smaller diameters increase heat transfer but also pressure drop. Selection depends on fluid properties and operational requirements.",
            ["tube diameter", "selection", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            23,
            "Heat Exchanger Gasket Selection",
            "Gasket selection is critical for leak prevention. Materials include rubber, PTFE, and graphite. Selection depends on temperature, pressure, and fluid compatibility.",
            ["gasket", "selection", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            24,
            "Heat Exchanger Thermal Stress Analysis",
            "Thermal stress analysis prevents mechanical failure due to temperature gradients. Analysis uses finite element methods and considers material properties and operational conditions.",
            ["thermal stress", "analysis", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            25,
            "Heat Exchanger Design for Corrosive Fluids",
            "Design for corrosive fluids includes material selection, protective coatings, and proper sealing. Stainless steel, titanium, and nickel alloys are commonly used.",
            ["corrosive fluids", "design", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            26,
            "Heat Exchanger Tube Bundle Removal",
            "Tube bundle removal is required for maintenance and cleaning. Design should allow easy access and minimal downtime. Removable bundle designs include floating head and U-tube.",
            ["tube bundle", "removal", "maintenance"],
            1.0
        ),
        SearchDocument(
            27,
            "Heat Exchanger Baffle Cut and Orientation",
            "Baffle cut and orientation affect shellside flow and heat transfer. Typical baffle cuts range from 20% to 25% of shell diameter. Proper orientation minimizes dead zones and tube vibration.",
            ["baffle", "cut", "orientation"],
            1.0
        ),
        SearchDocument(
            28,
            "Heat Exchanger Pass Partition Design",
            "Pass partition design allows multiple tube passes for improved heat transfer. Partition plates are used in tube sheets to direct flow. Design impacts LMTD correction factor.",
            ["pass partition", "design", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            29,
            "Heat Exchanger Nozzle Arrangement",
            "Nozzle arrangement impacts flow distribution and maintenance access. Proper design prevents dead zones and ensures uniform flow. Nozzle size and location are determined by operational requirements.",
            ["nozzle", "arrangement", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            30,
            "Heat Exchanger Design for High Pressure",
            "Design for high-pressure applications includes thicker tube sheets, reinforced shells, and high-strength materials. ASME codes provide guidelines for safe operation.",
            ["high pressure", "design", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            31,
            "Heat Exchanger Leak Detection Methods",
            "Leak detection methods include pressure testing, dye penetrant, and ultrasonic testing. Early detection prevents operational issues and environmental hazards.",
            ["leak detection", "methods", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            32,
            "Heat Exchanger Design for Cryogenic Service",
            "Cryogenic heat exchanger design uses materials with low-temperature toughness, such as stainless steel and aluminum. Insulation and expansion joints are critical.",
            ["cryogenic", "design", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            33,
            "Heat Exchanger Tube Cleaning Technologies",
            "Tube cleaning technologies include mechanical brushing, chemical cleaning, and ultrasonic cleaning. Selection depends on fouling type and tube material.",
            ["tube cleaning", "technologies", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            34,
            "Heat Exchanger Baffle Support Design",
            "Baffle support design ensures tube stability and prevents vibration. Supports include tie rods, spacers, and brackets. Proper design extends exchanger life.",
            ["baffle support", "design", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            35,
            "Heat Exchanger Thermal Expansion Analysis",
            "Thermal expansion analysis prevents mechanical failure due to temperature changes. Expansion joints and flexible supports are used to accommodate movement.",
            ["thermal expansion", "analysis", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            36,
            "Heat Exchanger Design for Oil Refinery",
            "Oil refinery heat exchangers require robust design for high temperatures, pressures, and corrosive fluids. Material selection and fouling prevention are critical.",
            ["oil refinery", "design", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            37,
            "Heat Exchanger Tube Sheet Sealing Methods",
            "Tube sheet sealing methods include welding, rolling, and gasketed joints. Proper sealing prevents leaks and ensures operational safety.",
            ["tube sheet", "sealing", "methods"],
            1.0
        ),
        SearchDocument(
            38,
            "Heat Exchanger Design for Steam Service",
            "Steam service heat exchangers require materials with high-temperature resistance and proper condensate drainage. Design includes steam traps and corrosion prevention.",
            ["steam service", "design", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            39,
            "Heat Exchanger Tube Arrangement Optimization",
            "Tube arrangement optimization maximizes heat transfer and minimizes pressure drop. Computational fluid dynamics (CFD) is used for advanced analysis.",
            ["tube arrangement", "optimization", "heat exchanger"],
            1.0
        ),
        SearchDocument(
            40,
            "Heat Exchanger Shell Design Considerations",
            "Shell design considers diameter, thickness, and material. Proper shell design prevents mechanical failure and ensures efficient heat transfer.",
            ["shell design", "considerations", "heat exchanger"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)