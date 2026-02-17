import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional


class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight


class SearchResult:
    def __init__(self, doc_id: str, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet


class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.avg_doc_len: float = 0.0
        self.total_doc_len: int = 0
        self.N: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old frequencies from index
                old_tf = self.doc_term_freqs.get(doc.id)
                if old_tf:
                    for term in old_tf:
                        self.term_doc_freqs[term] -= 1
                        if self.term_doc_freqs[term] <= 0:
                            del self.term_doc_freqs[term]
                    self.total_doc_len -= sum(old_tf.values())
                    self.N -= 1
                    del self.doc_term_freqs[doc.id]
                    del self.documents[doc.id]

            tokens = self._tokenize(doc.title + ' ' + doc.content)
            tf = Counter(tokens)
            self.doc_term_freqs[doc.id] = tf
            self.documents[doc.id] = doc
            for term in tf:
                self.term_doc_freqs[term] += 1
            doc_len = sum(tf.values())
            self.total_doc_len += doc_len
            self.N += 1
            self.avg_doc_len = self.total_doc_len / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms or self.N == 0:
            return []

        # Compute IDF for query terms
        idf = {term: self._compute_idf(term) for term in set(query_terms)}

        scores: Dict[str, float] = defaultdict(float)

        for term in query_terms:
            if term not in self.term_doc_freqs:
                continue
            idf_term = idf[term]
            for doc_id, tf in self.doc_term_freqs.items():
                f = tf.get(term, 0)
                if f == 0:
                    continue
                doc_len = sum(tf.values())
                score = self._score_bm25(f, idf_term, doc_len)
                scores[doc_id] += score

        # Incorporate document weight
        for doc_id in scores:
            scores[doc_id] *= self.documents[doc_id].weight

        # Sort results by score descending
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_len': self.avg_doc_len,
                'num_terms': len(self.term_doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, f: int, idf: float, doc_len: int) -> float:
        denom = f + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
        return idf * f * (self.k1 + 1) / denom if denom > 0 else 0.0

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            pos = content_lower.find(term)
            if pos >= 0:
                positions.append(pos)
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += '...'
            return snippet

        start = max(min(positions) - snippet_len // 4, 0)
        end = start + snippet_len
        snippet = content[start:end].strip()
        if start > 0:
            snippet = '...' + snippet
        if end < len(content):
            snippet += '...'
        return snippet


_singleton_index: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_index
    with _singleton_lock:
        if _singleton_index is None:
            _singleton_index = SearchIndex()
            _preseed_documents(_singleton_index)
        return _singleton_index


def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="ECD_Fundamentals",
            title="Equivalent Circulating Density (ECD) Fundamentals",
            content=(
                "Equivalent Circulating Density (ECD) is the effective density of the drilling fluid "
                "in the annulus when the fluid is circulating. It accounts for the pressure losses "
                "due to fluid movement and is critical for wellbore stability and pressure management."
            ),
            tags=["ECD", "hydraulics", "pressure", "drilling"]
        ),
        SearchDocument(
            doc_id="Bingham_Plastic_Model",
            title="Bingham Plastic Rheological Model",
            content=(
                "The Bingham Plastic model describes drilling fluid rheology with a yield point and "
                "plastic viscosity. It is used to predict pressure losses and flow behavior in drilling operations."
            ),
            tags=["rheology", "Bingham Plastic", "fluid mechanics"]
        ),
        SearchDocument(
            doc_id="Power_Law_Model",
            title="Power Law Rheological Model",
            content=(
                "The Power Law model characterizes non-Newtonian fluids without a yield point, "
                "using consistency and flow behavior indices to describe shear thinning or thickening."
            ),
            tags=["rheology", "Power Law", "non-Newtonian"]
        ),
        SearchDocument(
            doc_id="Annular_Velocity_Cleaning",
            title="Annular Velocity and Hole Cleaning",
            content=(
                "Annular velocity is the speed of drilling fluid in the annulus, essential for effective "
                "cuttings transport and hole cleaning to prevent stuck pipe and wellbore instability."
            ),
            tags=["annular velocity", "hole cleaning", "cuttings transport"]
        ),
        SearchDocument(
            doc_id="Standpipe_Pressure",
            title="Standpipe Pressure Components",
            content=(
                "Standpipe pressure is the pressure measured at the standpipe, consisting of pressure losses "
                "in the drillpipe, bit nozzles, and annulus, critical for hydraulic optimization."
            ),
            tags=["standpipe pressure", "hydraulics", "pressure loss"]
        ),
        SearchDocument(
            doc_id="Bit_Hydraulic_Max_HSI",
            title="Bit Hydraulic Optimization - Maximum Hydraulic Specific Energy (HSI)",
            content=(
                "Optimizing bit hydraulics to maximize Hydraulic Specific Energy (HSI) improves drilling efficiency "
                "by enhancing rock breaking and cleaning at the bit face."
            ),
            tags=["bit hydraulics", "HSI", "optimization"]
        ),
        SearchDocument(
            doc_id="Bit_Hydraulic_Max_Impact",
            title="Bit Hydraulic Optimization - Maximum Impact Force",
            content=(
                "Maximizing impact force at the bit through hydraulic design enhances drilling rate and reduces wear."
            ),
            tags=["bit hydraulics", "impact force", "optimization"]
        ),
        SearchDocument(
            doc_id="Surge_Swab_Pressure",
            title="Surge and Swab Pressure Calculations",
            content=(
                "Surge and swab pressures occur during pipe movement in the wellbore, affecting wellbore pressure "
                "and stability, calculated using fluid dynamics principles."
            ),
            tags=["surge pressure", "swab pressure", "wellbore pressure"]
        ),
        SearchDocument(
            doc_id="Triplex_Pump_Output",
            title="Triplex Pump Output Calculation",
            content=(
                "Triplex pump output is calculated based on pump displacement, stroke rate, and efficiency, "
                "important for flow rate and pressure predictions."
            ),
            tags=["triplex pump", "pump output", "hydraulics"]
        ),
        SearchDocument(
            doc_id="MPD_Principles",
            title="Managed Pressure Drilling (MPD) Principles",
            content=(
                "MPD involves controlling the annular pressure profile to precisely manage wellbore pressure, "
                "enhancing safety and efficiency in drilling operations."
            ),
            tags=["MPD", "managed pressure drilling", "pressure control"]
        ),
        SearchDocument(
            doc_id="Equivalent_Static_Density",
            title="Equivalent Static Density (ESD)",
            content=(
                "Equivalent Static Density (ESD) is the static fluid density equivalent to the dynamic pressure "
                "conditions in the wellbore, used for well control and pressure management."
            ),
            tags=["ESD", "pressure", "well control"]
        ),
        SearchDocument(
            doc_id="Mud_Motor_Pressure_Drop",
            title="Pressure Drop Across Mud Motor",
            content=(
                "Pressure drop across the mud motor affects motor performance and is influenced by flow rate, "
                "mud rheology, and motor design."
            ),
            tags=["mud motor", "pressure drop", "hydraulics"]
        ),
        SearchDocument(
            doc_id="Fann_35_Viscometer",
            title="Fann 35 Viscometer and Rheology Measurement",
            content=(
                "The Fann 35 viscometer measures drilling fluid rheology parameters including plastic viscosity, "
                "yield point, and gel strengths."
            ),
            tags=["Fann 35", "rheology", "measurement"]
        ),
        SearchDocument(
            doc_id="Herschel_Bulkley_Model",
            title="Herschel-Bulkley Rheological Model",
            content=(
                "The Herschel-Bulkley model generalizes Bingham and Power Law models, describing fluids with "
                "yield stress and shear-dependent viscosity."
            ),
            tags=["rheology", "Herschel-Bulkley", "non-Newtonian"]
        ),
        SearchDocument(
            doc_id="Critical_Transport_Velocity",
            title="Critical Transport Velocity for Cuttings",
            content=(
                "Critical transport velocity is the minimum annular velocity required to keep cuttings suspended "
                "and transported out of the wellbore."
            ),
            tags=["cuttings transport", "velocity", "hole cleaning"]
        ),
        SearchDocument(
            doc_id="Nozzle_Selection_TFA",
            title="Nozzle Selection and Total Flow Area (TFA)",
            content=(
                "Nozzle selection and total flow area impact bit hydraulics, pressure drop, and cleaning efficiency."
            ),
            tags=["nozzle", "TFA", "hydraulics"]
        ),
        SearchDocument(
            doc_id="Drillstring_Pressure_Drop",
            title="Drillstring Pressure Drop - Laminar vs Turbulent Flow",
            content=(
                "Drillstring pressure drop depends on flow regime, with laminar and turbulent flows having distinct "
                "pressure loss characteristics."
            ),
            tags=["drillstring", "pressure drop", "flow regime"]
        ),
        SearchDocument(
            doc_id="Narrow_Margin_ECD_Management",
            title="Narrow Margin Well ECD Management",
            content=(
                "Managing ECD in narrow margin wells is critical to avoid formation fracture or wellbore collapse."
            ),
            tags=["ECD", "narrow margin", "well control"]
        ),
        SearchDocument(
            doc_id="Annular_Pressure_Loss",
            title="Annular Pressure Loss (APL) Calculation",
            content=(
                "Annular pressure loss calculation accounts for frictional losses in the annulus, essential for "
                "accurate pressure modeling."
            ),
            tags=["annular pressure loss", "APL", "hydraulics"]
        ),
        SearchDocument(
            doc_id="PMCD_Principles",
            title="Pressurized Mud Cap Drilling (PMCD)",
            content=(
                "PMCD uses a pressurized mud cap to control wellbore pressure in challenging drilling environments."
            ),
            tags=["PMCD", "mud cap", "pressure control"]
        ),
        SearchDocument(
            doc_id="Float_Equipment_Hydraulics",
            title="Float Equipment and Drillstring Hydraulics",
            content=(
                "Float equipment affects drillstring hydraulics and pressure profiles during drilling and tripping."
            ),
            tags=["float equipment", "drillstring", "hydraulics"]
        ),
        SearchDocument(
            doc_id="Cuttings_Bed_Formation",
            title="Cuttings Bed Formation and Remediation",
            content=(
                "Cuttings bed formation can cause stuck pipe; remediation involves optimizing hydraulics and flow."
            ),
            tags=["cuttings bed", "stuck pipe", "remediation"]
        ),
        SearchDocument(
            doc_id="Temperature_Effects_Mud_Rheology",
            title="Temperature Effects on Mud Rheology",
            content=(
                "Temperature changes affect mud rheology properties, impacting flow behavior and pressure losses."
            ),
            tags=["temperature", "mud rheology", "fluid properties"]
        ),
        SearchDocument(
            doc_id="Drillstring_Rotation_Annular_Friction",
            title="Drillstring Rotation Effect on Annular Friction",
            content=(
                "Drillstring rotation reduces annular friction, influencing pressure losses and torque."
            ),
            tags=["drillstring rotation", "annular friction", "hydraulics"]
        ),
        SearchDocument(
            doc_id="Hydraulics_Software_RealTime",
            title="Hydraulics Software and Real-Time Modeling",
            content=(
                "Real-time hydraulics software models wellbore conditions to optimize drilling performance and safety."
            ),
            tags=["hydraulics software", "real-time", "modeling"]
        ),
        SearchDocument(
            doc_id="Barite_Sag_Density",
            title="Barite Sag and Dynamic vs Static Density",
            content=(
                "Barite sag causes density variations between dynamic and static conditions, affecting well control."
            ),
            tags=["barite sag", "density", "well control"]
        ),
    ]

    for doc in docs:
        index.add_document(doc)