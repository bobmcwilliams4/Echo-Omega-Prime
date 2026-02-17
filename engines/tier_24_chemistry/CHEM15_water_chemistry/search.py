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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._lock = threading.RLock()
        self._total_docs = 0
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            self._doc_lengths[doc.id] = len(tokens)
            self._total_docs += 1
            for token in tokens:
                self._inverted_index[token][doc.id] = self._inverted_index[token].get(doc.id, 0) + 1
            for token in set(tokens):
                self._doc_freqs[token] += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
            self._idf_cache.clear()
            self._tfidf_cache.pop(doc.id, None)

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self._inverted_index.get(token, {}).keys())
        scores: Dict[int, float] = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc_weight = self._documents[doc_id].weight
            total_score = bm25_score * 0.7 + tfidf_score * 0.3
            scores[doc_id] = total_score * doc_weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                'total_docs': self._total_docs,
                'avg_doc_length': self._avg_doc_length,
                'unique_terms': len(self._inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freqs.get(term, 0)
        N = self._total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc_tokens = self._doc_tokens[doc_id]
        doc_len = self._doc_lengths[doc_id]
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1
        freq = Counter(doc_tokens)
        for term in query_tokens:
            if term not in freq:
                continue
            tf = freq[term]
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avgdl)
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vec = self._tfidf_cache[doc_id]
        else:
            doc_tokens = self._doc_tokens[doc_id]
            tf = Counter(doc_tokens)
            doc_len = self._doc_lengths[doc_id]
            tfidf_vec = {}
            for term in set(doc_tokens):
                tf_norm = tf[term] / doc_len
                idf = self._compute_idf(term)
                tfidf_vec[term] = tf_norm * idf
            self._tfidf_cache[doc_id] = tfidf_vec
        score = 0.0
        for term in query_tokens:
            score += tfidf_vec.get(term, 0.0)
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:160]
            return snippet + "..." if len(snippet) < len(content) else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(r'\b(%s)\b' % re.escape(qt), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

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

# --- Pre-seed Domain Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "pH Control in Water Treatment",
            "pH control is essential for optimizing coagulation, disinfection, and corrosion control in water treatment systems. Common chemicals include lime, soda ash, and carbon dioxide.",
            ["pH_control_treatment_systems", "coagulation", "disinfection", "corrosion"],
            1.0
        ),
        SearchDocument(
            2,
            "Langelier Saturation Index (LSI) Calculation",
            "The Langelier Saturation Index predicts calcium carbonate stability in water. LSI = pH - pHs, where pHs is the saturation pH. LSI > 0 indicates scaling, LSI < 0 indicates corrosive water.",
            ["langelier_saturation_index_lsi", "scaling", "corrosion"],
            1.0
        ),
        SearchDocument(
            3,
            "Jar Testing for Coagulation and Flocculation",
            "Jar testing determines optimal coagulant and flocculant dosages for turbidity and color removal. Parameters include rapid mix, slow mix, and settling times.",
            ["coagulation_flocculation_jar_testing", "turbidity", "color_removal"],
            1.0
        ),
        SearchDocument(
            4,
            "Chlorination and Disinfection CT Values",
            "CT (Concentration x Time) values are used to ensure effective inactivation of pathogens during chlorination. Regulatory CT tables specify required values for Giardia, viruses, and Cryptosporidium.",
            ["chlorination_disinfection_ct_values", "ct", "giardia", "cryptosporidium"],
            1.0
        ),
        SearchDocument(
            5,
            "Microfiltration and Ultrafiltration Membrane Processes",
            "Membrane filtration processes such as microfiltration (MF) and ultrafiltration (UF) remove particulates, bacteria, and some viruses. Key parameters include flux, transmembrane pressure, and recovery.",
            ["membrane_filtration_microfiltration_ultrafiltration", "mf", "uf"],
            1.0
        ),
        SearchDocument(
            6,
            "Produced Water Oil Removal Using Dissolved Air Flotation (DAF)",
            "DAF systems remove oil and suspended solids from produced water by attaching air bubbles to particles, causing them to float. Design involves recycle ratio, air-to-solids ratio, and surface loading rate.",
            ["produced_water_oil_removal_daf", "daf", "oil_removal"],
            1.0
        ),
        SearchDocument(
            7,
            "Ion Exchange for Water Softening",
            "Ion exchange softening replaces calcium and magnesium ions with sodium using resin beds. Regeneration is performed with brine. Hardness removal efficiency depends on resin capacity and flow rate.",
            ["ion_exchange_water_softening", "softening", "hardness"],
            1.0
        ),
        SearchDocument(
            8,
            "NPDES Permit Discharge Limits",
            "The National Pollutant Discharge Elimination System (NPDES) sets limits for pollutants in wastewater discharges. Compliance requires monitoring parameters such as BOD, TSS, ammonia, and metals.",
            ["npdes_permit_discharge_limits", "npdes", "wastewater"],
            1.0
        ),
        SearchDocument(
            9,
            "Safe Drinking Water Act (SDWA) MCL Compliance",
            "The SDWA mandates Maximum Contaminant Levels (MCLs) for drinking water. Utilities must monitor for regulated contaminants and report violations to the EPA.",
            ["safe_drinking_water_act_mcl_compliance", "sdwa", "mcl"],
            1.0
        ),
        SearchDocument(
            10,
            "Reverse Osmosis (RO) Desalination System Design",
            "RO systems use semi-permeable membranes to remove dissolved salts from water. Design considerations include feedwater quality, recovery rate, and antiscalant dosing.",
            ["reverse_osmosis_desalination_design", "ro", "desalination"],
            1.0
        ),
        SearchDocument(
            11,
            "UV Disinfection for Cryptosporidium Inactivation",
            "Ultraviolet (UV) light is effective for inactivating Cryptosporidium and Giardia. Dose is measured in mJ/cm2. UV transmittance and lamp aging affect performance.",
            ["uv_disinfection_cryptosporidium", "uv", "cryptosporidium"],
            1.0
        ),
        SearchDocument(
            12,
            "Water Quality Parameters and Monitoring",
            "Key water quality parameters include pH, turbidity, residual chlorine, conductivity, and temperature. Continuous monitoring ensures regulatory compliance and process control.",
            ["water_quality_parameters_monitoring", "monitoring", "compliance"],
            1.0
        ),
        SearchDocument(
            13,
            "Stiff Diagram for Water Typing",
            "Stiff diagrams graphically represent water chemistry by plotting cation and anion concentrations. Useful for comparing water sources and tracking changes over time.",
            ["stiff_diagram_water_typing", "water_typing", "hydrochemistry"],
            1.0
        ),
        SearchDocument(
            14,
            "Boiler Feedwater Quality Specifications",
            "Boiler feedwater must meet strict quality specs for hardness, silica, dissolved oxygen, and alkalinity to prevent scaling and corrosion. Treatment may include softening, deaeration, and chemical dosing.",
            ["boiler_feedwater_quality_specs", "boiler", "feedwater"],
            1.0
        ),
        SearchDocument(
            15,
            "Optimizing Coagulant Dose in Surface Water Treatment",
            "Coagulant dose optimization improves turbidity removal and reduces sludge production. Jar tests and online streaming current detectors are used for control.",
            ["coagulation_flocculation_jar_testing", "coagulant", "surface_water"],
            1.0
        ),
        SearchDocument(
            16,
            "Corrosion Control Using pH Adjustment",
            "Raising pH can reduce corrosion by shifting carbonate equilibrium. Langelier and Ryznar indices help assess scaling or corrosive tendencies.",
            ["pH_control_treatment_systems", "corrosion", "langelier_saturation_index_lsi"],
            1.0
        ),
        SearchDocument(
            17,
            "Disinfection Byproduct (DBP) Control in Chlorination",
            "Chlorination can form DBPs such as trihalomethanes (THMs) and haloacetic acids (HAAs). Control strategies include precursor removal, pH adjustment, and alternative disinfectants.",
            ["chlorination_disinfection_ct_values", "dbp", "thm", "haa"],
            1.0
        ),
        SearchDocument(
            18,
            "Membrane Integrity Testing for MF/UF Systems",
            "Membrane integrity is verified using pressure decay, diffusive air, or particle challenge tests. Integrity monitoring is critical for pathogen removal credits.",
            ["membrane_filtration_microfiltration_ultrafiltration", "integrity", "mf", "uf"],
            1.0
        ),
        SearchDocument(
            19,
            "Produced Water Treatment Train Design",
            "Produced water treatment trains may include oil removal (DAF), media filtration, softening, and reverse osmosis. Selection depends on oil, TDS, and discharge requirements.",
            ["produced_water_oil_removal_daf", "reverse_osmosis_desalination_design", "treatment_train"],
            1.0
        ),
        SearchDocument(
            20,
            "Ion Exchange Resin Fouling and Cleaning",
            "Fouling of ion exchange resins by iron, organics, or silica reduces softening efficiency. Cleaning protocols include acid, caustic, and brine soaks.",
            ["ion_exchange_water_softening", "resin", "fouling"],
            1.0
        ),
        SearchDocument(
            21,
            "NPDES Monitoring and Reporting Requirements",
            "NPDES permits require routine monitoring of effluent parameters and timely reporting to regulatory agencies. Non-compliance can result in penalties.",
            ["npdes_permit_discharge_limits", "monitoring", "reporting"],
            1.0
        ),
        SearchDocument(
            22,
            "SDWA MCLs for Inorganic Contaminants",
            "Inorganic MCLs under the SDWA include arsenic, lead, nitrate, and fluoride. Monitoring frequency and treatment depend on contaminant type and concentration.",
            ["safe_drinking_water_act_mcl_compliance", "inorganic", "mcl"],
            1.0
        ),
        SearchDocument(
            23,
            "RO Membrane Scaling and Antiscalant Selection",
            "Scaling in RO systems is controlled by antiscalants, pH adjustment, and periodic cleaning. Common scalants include calcium carbonate and sulfate.",
            ["reverse_osmosis_desalination_design", "scaling", "antiscalant"],
            1.0
        ),
        SearchDocument(
            24,
            "UV Dose Monitoring and Validation",
            "UV systems require dose monitoring and validation using sensors and bioassays. Proper maintenance ensures consistent pathogen inactivation.",
            ["uv_disinfection_cryptosporidium", "uv", "dose"],
            1.0
        ),
        SearchDocument(
            25,
            "Continuous Water Quality Data Acquisition",
            "SCADA systems collect real-time water quality data for parameters such as pH, turbidity, and chlorine, supporting rapid response to process upsets.",
            ["water_quality_parameters_monitoring", "scada", "data"],
            1.0
        ),
        SearchDocument(
            26,
            "Interpreting Stiff Diagrams in Hydrogeology",
            "Stiff diagrams help visualize changes in water chemistry due to mixing, ion exchange, or contamination. Patterns indicate dominant cations and anions.",
            ["stiff_diagram_water_typing", "hydrogeology", "ion_exchange_water_softening"],
            1.0
        ),
        SearchDocument(
            27,
            "Boiler Water Blowdown and Conductivity Control",
            "Blowdown removes dissolved solids from boiler water. Conductivity is monitored to control blowdown rate and prevent scaling.",
            ["boiler_feedwater_quality_specs", "blowdown", "conductivity"],
            1.0
        ),
        SearchDocument(
            28,
            "Jar Test Protocol for Coagulant Selection",
            "A standard jar test protocol involves dosing, rapid mixing, slow mixing, and settling. The best coagulant is selected based on turbidity and color removal.",
            ["coagulation_flocculation_jar_testing", "jar_test", "coagulant"],
            1.0
        ),
        SearchDocument(
            29,
            "Chlorine Demand and Residual Monitoring",
            "Chlorine demand is the amount of chlorine consumed by reactions with water constituents. Maintaining a residual ensures effective disinfection.",
            ["chlorination_disinfection_ct_values", "chlorine", "residual"],
            1.0
        ),
        SearchDocument(
            30,
            "Membrane Fouling Control in UF/MF Systems",
            "Fouling in ultrafiltration and microfiltration membranes is controlled by pre-treatment, backwashing, and chemical cleaning. Monitoring transmembrane pressure is essential.",
            ["membrane_filtration_microfiltration_ultrafiltration", "fouling", "backwash"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)