import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.total_docs: int = 0

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, freq in token_counts.items():
                self.term_freqs[token][doc.id] = freq
                self.term_doc_freqs[token] += 1
            self._update_avg_doc_length()

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

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
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_freqs.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_length / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        score *= doc.weight
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_freqs.get(term, {}).get(doc_id, 0)
            if doc_length == 0:
                continue
            tf_norm = tf / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        score *= doc.weight
        return score

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_freqs.get(term, {}).keys())
        scored_results = []
        for doc_id in candidate_docs:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc = self.documents[doc_id]
                snippet = self._generate_snippet(doc.content, query_terms)
                scored_results.append(SearchResult(doc_id, score, doc.title, snippet))
        scored_results.sort(key=lambda x: x.score, reverse=True)
        return scored_results[:limit]

    def _generate_snippet(self, content: str, query_terms: List[str], window: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freqs),
        }

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

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="tceq_permit_001",
            title="TCEQ Permit Requirements for Oilfield Operations",
            content="Texas Commission on Environmental Quality (TCEQ) requires oilfield operators to obtain permits for activities impacting air, water, and soil. Key requirements include registration, emissions reporting, and compliance with state standards. Permits may include air quality, wastewater discharge, and waste management.",
            tags=["TCEQ", "permit", "oilfield", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="epa_npdes_002",
            title="EPA NPDES Permit Applicability",
            content="The EPA's National Pollutant Discharge Elimination System (NPDES) permit is required for oilfield operations discharging pollutants into waters of the United States. Applicability depends on the nature of discharge, location, and compliance with Clean Water Act Section 402.",
            tags=["EPA", "NPDES", "water", "permit"],
            weight=1.0
        ),
        SearchDocument(
            id="cwa_section_402_003",
            title="Clean Water Act Section 402 Compliance",
            content="Section 402 of the Clean Water Act establishes the NPDES permit program, regulating the discharge of pollutants from oilfield operations. Operators must monitor effluent, maintain records, and submit reports to ensure compliance.",
            tags=["Clean Water Act", "Section 402", "NPDES", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="ca_pbr_004",
            title="Clean Air Act Permit by Rule (PBR) Applicability",
            content="Permit by Rule (PBR) under the Clean Air Act allows certain oilfield operations to operate without a traditional permit if they meet specific criteria. Operators must adhere to emission limits, reporting requirements, and operational standards.",
            tags=["Clean Air Act", "PBR", "air", "permit"],
            weight=1.0
        ),
        SearchDocument(
            id="spcc_plan_005",
            title="SPCC Plan Requirements",
            content="Spill Prevention, Control, and Countermeasure (SPCC) plans are required for oilfield facilities storing significant quantities of oil. Plans must address spill prevention, response, and facility design. The threshold is 1,320 gallons aboveground or 42,000 gallons underground.",
            tags=["SPCC", "spill", "oil", "plan"],
            weight=1.0
        ),
        SearchDocument(
            id="tier2_epcra_312_006",
            title="Tier II Chemical Reporting (EPCRA §312)",
            content="EPCRA Section 312 requires oilfield operators to submit Tier II reports for hazardous chemicals stored onsite. Reports must include chemical inventory, storage locations, and emergency contact information. Submission is annual to local and state agencies.",
            tags=["EPCRA", "Tier II", "chemical", "reporting"],
            weight=1.0
        ),
        SearchDocument(
            id="rcra_hazardous_007",
            title="RCRA Hazardous Waste Determination",
            content="Resource Conservation and Recovery Act (RCRA) mandates oilfield operators to determine if waste generated is hazardous. Determination involves waste analysis, classification, and proper disposal. Non-hazardous and hazardous wastes must be managed separately.",
            tags=["RCRA", "hazardous waste", "determination"],
            weight=1.0
        ),
        SearchDocument(
            id="norm_disposal_008",
            title="NORM Disposal Compliance",
            content="Naturally Occurring Radioactive Material (NORM) disposal in oilfield operations requires compliance with state and federal regulations. Operators must characterize NORM waste, select approved disposal methods, and maintain records.",
            tags=["NORM", "disposal", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="air_quality_standard_009",
            title="Air Quality Standard Permit Applicability",
            content="Oilfield operations may require a Standard Air Quality Permit if emissions exceed regulatory thresholds. Permits specify allowable emissions, monitoring requirements, and operational controls. Application must include emission calculations and site information.",
            tags=["air quality", "standard permit", "emissions"],
            weight=1.0
        ),
        SearchDocument(
            id="flaring_venting_010",
            title="Flaring and Venting Regulations",
            content="Flaring and venting of gases in oilfield operations are regulated to minimize air pollution. Operators must comply with state and federal limits, record volumes, and report excess events. Permits may be required for routine or emergency flaring.",
            tags=["flaring", "venting", "regulations"],
            weight=1.0
        ),
        SearchDocument(
            id="stormwater_swppp_011",
            title="Stormwater SWPPP Requirements",
            content="Stormwater Pollution Prevention Plans (SWPPP) are required for oilfield sites to control runoff and prevent contamination. Plans must identify potential sources, implement BMPs, and monitor stormwater discharges. Compliance with NPDES is essential.",
            tags=["stormwater", "SWPPP", "oilfield", "requirements"],
            weight=1.0
        ),
        SearchDocument(
            id="spill_notification_012",
            title="Spill Notification Thresholds",
            content="Oilfield operators must notify authorities when spills exceed regulatory thresholds. Thresholds vary by substance and location. Immediate notification is required for hazardous materials, followed by written reports and corrective actions.",
            tags=["spill", "notification", "thresholds"],
            weight=1.0
        ),
        SearchDocument(
            id="cercla_reporting_013",
            title="CERCLA Reporting Requirements",
            content="Comprehensive Environmental Response, Compensation, and Liability Act (CERCLA) requires reporting of releases of hazardous substances above reportable quantities. Oilfield operators must notify the National Response Center and maintain records.",
            tags=["CERCLA", "reporting", "hazardous", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="epcra_tier2_014",
            title="EPCRA Tier II Reporting",
            content="EPCRA Tier II reporting is required for oilfield facilities storing hazardous chemicals above threshold quantities. Reports must be submitted annually to local emergency planning committees and fire departments.",
            tags=["EPCRA", "Tier II", "reporting", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="sip_compliance_015",
            title="State Implementation Plan (SIP) Compliance",
            content="State Implementation Plans (SIP) outline air quality standards and compliance requirements for oilfield operations. Operators must adhere to emission limits, monitoring, and reporting as specified in the SIP.",
            tags=["SIP", "compliance", "air quality"],
            weight=1.0
        ),
        SearchDocument(
            id="opacity_monitoring_016",
            title="Opacity Monitoring Requirements",
            content="Oilfield operations emitting visible pollutants must monitor opacity to ensure compliance with air quality standards. Monitoring methods include continuous opacity monitors and periodic visual inspections.",
            tags=["opacity", "monitoring", "air quality"],
            weight=1.0
        ),
        SearchDocument(
            id="voc_emissions_017",
            title="VOC Emissions Calculation and Control",
            content="Volatile Organic Compound (VOC) emissions from oilfield operations must be calculated and controlled. Operators use emission factors, monitoring equipment, and control technologies to reduce VOCs and comply with regulatory limits.",
            tags=["VOC", "emissions", "calculation", "control"],
            weight=1.0
        ),
        SearchDocument(
            id="ghg_reporting_018",
            title="Greenhouse Gas (GHG) Reporting",
            content="Oilfield operators must report greenhouse gas (GHG) emissions under EPA regulations. Reporting includes CO2, methane, and other GHGs. Operators must use approved calculation methods and submit annual reports.",
            tags=["GHG", "reporting", "oilfield", "EPA"],
            weight=1.0
        ),
        SearchDocument(
            id="title_v_permit_019",
            title="Title V Operating Permit Applicability",
            content="Title V Operating Permits are required for oilfield facilities with major sources of air pollution. Permits consolidate all air quality requirements and require regular monitoring, reporting, and compliance certification.",
            tags=["Title V", "operating permit", "air pollution"],
            weight=1.0
        ),
        SearchDocument(
            id="area_source_neshap_020",
            title="Area Source NESHAP Applicability",
            content="National Emission Standards for Hazardous Air Pollutants (NESHAP) apply to area sources in oilfield operations. Operators must identify applicable standards, implement controls, and maintain records for compliance.",
            tags=["NESHAP", "area source", "hazardous", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="oilfield_wastewater_021",
            title="Oilfield Wastewater Discharge Permits",
            content="Oilfield wastewater discharge requires permits under NPDES and state programs. Operators must characterize wastewater, monitor discharges, and comply with effluent limits. Permits specify treatment requirements and reporting obligations.",
            tags=["wastewater", "discharge", "permit", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="chemical_inventory_022",
            title="Chemical Inventory Management for Oilfield Operations",
            content="Oilfield operators must maintain accurate chemical inventories for compliance with EPCRA and Tier II reporting. Inventory management includes tracking quantities, storage locations, and safety data sheets.",
            tags=["chemical", "inventory", "management", "EPCRA"],
            weight=1.0
        ),
        SearchDocument(
            id="stormwater_bmps_023",
            title="Stormwater BMPs for Oilfield Sites",
            content="Best Management Practices (BMPs) for stormwater at oilfield sites include sediment control, erosion prevention, and spill containment. BMPs are implemented as part of SWPPP to minimize environmental impact.",
            tags=["stormwater", "BMPs", "SWPPP", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="hazardous_materials_training_024",
            title="Hazardous Materials Training Requirements",
            content="Oilfield personnel must receive training on hazardous materials handling, spill response, and emergency procedures. Training is required by OSHA, EPA, and state agencies to ensure safety and compliance.",
            tags=["hazardous materials", "training", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="emission_reporting_025",
            title="Emission Reporting for Oilfield Operations",
            content="Oilfield operators must report emissions of regulated pollutants to EPA and state agencies. Reporting includes air, water, and waste emissions. Accurate data collection and timely submission are essential for compliance.",
            tags=["emission", "reporting", "oilfield", "EPA"],
            weight=1.0
        ),
        SearchDocument(
            id="waste_management_026",
            title="Waste Management Compliance in Oilfield Operations",
            content="Oilfield waste management includes segregation, storage, and disposal of hazardous and non-hazardous wastes. Compliance with RCRA, state regulations, and proper documentation is required.",
            tags=["waste management", "compliance", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="emergency_response_027",
            title="Emergency Response Planning for Oilfield Facilities",
            content="Oilfield facilities must develop emergency response plans addressing spills, fires, and releases. Plans include notification procedures, response actions, and coordination with local agencies.",
            tags=["emergency response", "planning", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="air_monitoring_028",
            title="Air Monitoring Requirements for Oilfield Sites",
            content="Air monitoring at oilfield sites is required to assess compliance with permit limits and detect pollutant releases. Monitoring methods include continuous analyzers, periodic sampling, and recordkeeping.",
            tags=["air monitoring", "requirements", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="chemical_spill_response_029",
            title="Chemical Spill Response Procedures",
            content="Oilfield operators must follow established procedures for chemical spill response, including containment, cleanup, and reporting. Procedures must comply with SPCC, CERCLA, and local regulations.",
            tags=["chemical", "spill", "response", "oilfield"],
            weight=1.0
        ),
        SearchDocument(
            id="annual_compliance_audit_030",
            title="Annual Compliance Audit for Oilfield Operations",
            content="Annual compliance audits are conducted to evaluate oilfield operations against regulatory requirements. Audits review permits, records, training, and operational practices to identify deficiencies and corrective actions.",
            tags=["compliance", "audit", "oilfield", "annual"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)