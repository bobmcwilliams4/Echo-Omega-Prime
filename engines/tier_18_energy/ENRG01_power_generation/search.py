import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_map: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[str, Dict[str, float]] = {}
        self._initialized = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.term_doc_freq[token] += 1
                self.term_doc_map[token][doc.id] = count
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self._initialized = False

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            return 0.0
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        tokens = self._tokenize(doc.content)
        doc_len = len(tokens)
        score = 0.0
        for term in query_terms:
            tf = self.term_doc_map.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length if self.avg_doc_length > 0 else 1)
            score += idf * (numerator / denominator if denominator > 0 else 0)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        tokens = self._tokenize(doc.content)
        doc_len = len(tokens)
        tfidf_score = 0.0
        token_counts = Counter(tokens)
        for term in query_terms:
            tf = token_counts.get(term, 0) / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            tfidf_score += tf * idf
        return tfidf_score * doc.weight

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        with self.lock:
            if not self._initialized:
                self._update_avg_doc_length()
                self._initialized = True
        query_terms = self._tokenize(query)
        scores = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(doc.content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:window])
        else:
            start = max(positions[0] - window // 2, 0)
            end = min(start + window, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
            'top_terms': sorted(self.term_doc_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        }

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            id="coal_001",
            title="Coal-Fired Power Plant Operation Fundamentals",
            content="Coal-fired power plants operate by burning coal to heat water, producing steam that drives turbines. Key parameters include boiler temperature, steam pressure, and emissions control. Efficiency improvements focus on supercritical steam cycles and advanced material use.",
            tags=["coal_fired_power_plant_operation", "steam_cycle", "boiler", "emissions"],
            weight=1.0
        ),
        SearchDocument(
            id="coal_002",
            title="Emissions Control in Coal Plants: SCR and SO2 Scrubbers",
            content="Selective Catalytic Reduction (SCR) systems reduce NOx emissions using ammonia and catalysts. Flue Gas Desulfurization (FGD) scrubbers remove SO2 by chemical absorption. Integration of SCR and FGD is critical for regulatory compliance and environmental protection.",
            tags=["selective_catalytic_reduction_scr_nox_control", "flue_gas_desulfurization_so2_scrubber", "coal_fired_power_plant_operation"],
            weight=1.0
        ),
        SearchDocument(
            id="ccgt_001",
            title="Combined Cycle Gas Turbine (CCGT) Efficiency",
            content="CCGT plants combine gas turbines and steam turbines to maximize efficiency. Exhaust heat from gas turbines is used to generate steam for the steam cycle. Typical efficiency exceeds 60%. Operational flexibility and fast ramp rates are key advantages.",
            tags=["combined_cycle_gas_turbine_ccgt", "steam_cycle", "efficiency"],
            weight=1.0
        ),
        SearchDocument(
            id="ccgt_002",
            title="CCGT Plant Operation and Maintenance",
            content="Routine maintenance of CCGT plants includes inspection of turbine blades, heat recovery steam generators, and control systems. Predictive maintenance using vibration analysis and thermography improves reliability and reduces downtime.",
            tags=["combined_cycle_gas_turbine_ccgt", "maintenance", "reliability"],
            weight=1.0
        ),
        SearchDocument(
            id="gas_001",
            title="Simple Cycle Gas Turbine Peaking Applications",
            content="Simple cycle gas turbines are used for peaking power due to rapid startup and shutdown capabilities. They operate with lower efficiency than combined cycles but provide critical grid support during high demand periods.",
            tags=["simple_cycle_gas_turbine_peaking", "grid_support", "peaking"],
            weight=1.0
        ),
        SearchDocument(
            id="pwr_001",
            title="Pressurized Water Reactor (PWR) Basics",
            content="PWRs use pressurized water as both coolant and moderator. The reactor core heats water under high pressure, preventing boiling. Heat is transferred to a secondary loop to generate steam. Safety systems include containment structures and emergency cooling.",
            tags=["pressurized_water_reactor_pwr", "nuclear", "safety"],
            weight=1.0
        ),
        SearchDocument(
            id="bwr_001",
            title="Boiling Water Reactor (BWR) Operation",
            content="BWRs generate steam directly in the reactor vessel. Control rods regulate fission rate. Steam drives turbines and is condensed for reuse. Key concerns include radiation shielding and water chemistry control.",
            tags=["boiling_water_reactor_bwr", "nuclear", "operation"],
            weight=1.0
        ),
        SearchDocument(
            id="solar_001",
            title="Solar Photovoltaic (PV) System Design",
            content="PV systems convert sunlight to electricity using semiconductor materials. Design considerations include panel orientation, inverter selection, and shading analysis. Maximum Power Point Tracking (MPPT) optimizes energy yield.",
            tags=["solar_photovoltaic_pv_systems", "design", "mppt"],
            weight=1.0
        ),
        SearchDocument(
            id="solar_002",
            title="Grid Integration of Solar PV under IEEE 1547",
            content="IEEE 1547 standard governs interconnection of distributed resources like solar PV. Requirements include voltage regulation, anti-islanding, and communication protocols. Compliance ensures safe and reliable grid operation.",
            tags=["ieee_1547_grid_interconnection_standard", "solar_photovoltaic_pv_systems", "grid"],
            weight=1.0
        ),
        SearchDocument(
            id="wind_001",
            title="Wind Turbine Power Generation Principles",
            content="Wind turbines convert kinetic energy from wind into mechanical energy, then electricity. Key factors include blade design, wind speed, and generator type. Variable speed turbines optimize power output across wind conditions.",
            tags=["wind_turbine_power_generation", "blade_design", "generator"],
            weight=1.0
        ),
        SearchDocument(
            id="wind_002",
            title="Wind Farm Operation and Grid Compliance",
            content="Wind farms must comply with NERC reliability standards and grid codes. Control systems manage power output, frequency, and voltage. Remote monitoring and predictive maintenance enhance performance.",
            tags=["wind_turbine_power_generation", "nerc_reliability_standards_compliance", "grid"],
            weight=1.0
        ),
        SearchDocument(
            id="hydro_001",
            title="Hydroelectric Dam Operation and Control",
            content="Hydroelectric dams use water flow to spin turbines and generate electricity. Operation involves managing reservoir levels, flow rates, and turbine efficiency. Environmental concerns include fish migration and water quality.",
            tags=["hydroelectric_dam_operation", "turbine", "environment"],
            weight=1.0
        ),
        SearchDocument(
            id="hydro_002",
            title="Hydroelectric Grid Integration and Reliability",
            content="Hydroelectric plants provide grid stability through fast ramping and ancillary services. Compliance with NERC standards ensures reliability. Automation systems optimize dispatch and load balancing.",
            tags=["hydroelectric_dam_operation", "nerc_reliability_standards_compliance", "grid"],
            weight=1.0
        ),
        SearchDocument(
            id="scr_001",
            title="Selective Catalytic Reduction (SCR) NOx Control",
            content="SCR systems use catalysts and ammonia injection to convert NOx to nitrogen and water. Operating parameters include temperature, ammonia flow, and catalyst activity. Regular catalyst replacement maintains efficiency.",
            tags=["selective_catalytic_reduction_scr_nox_control", "emissions", "maintenance"],
            weight=1.0
        ),
        SearchDocument(
            id="fgd_001",
            title="Flue Gas Desulfurization (FGD) SO2 Scrubber Design",
            content="FGD scrubbers remove sulfur dioxide from flue gas using limestone slurry. Reaction produces gypsum as a byproduct. Design focuses on absorber efficiency, slurry management, and corrosion control.",
            tags=["flue_gas_desulfurization_so2_scrubber", "emissions", "design"],
            weight=1.0
        ),
        SearchDocument(
            id="ieee_001",
            title="IEEE 1547 Grid Interconnection Standard Overview",
            content="IEEE 1547 defines requirements for interconnecting distributed energy resources with the grid. Key aspects include voltage regulation, harmonics, and anti-islanding protection. Compliance is mandatory for grid-connected PV and wind systems.",
            tags=["ieee_1547_grid_interconnection_standard", "solar_photovoltaic_pv_systems", "wind_turbine_power_generation"],
            weight=1.0
        ),
        SearchDocument(
            id="nerc_001",
            title="NERC Reliability Standards for Power Generation",
            content="NERC standards ensure reliability of the bulk power system. Requirements cover frequency control, voltage regulation, and contingency planning. Compliance audits and reporting are essential for generators.",
            tags=["nerc_reliability_standards_compliance", "grid", "reliability"],
            weight=1.0
        ),
        SearchDocument(
            id="lcoe_001",
            title="Levelized Cost of Energy (LCOE) Calculation",
            content="LCOE measures the average cost of electricity generation over a plant's lifetime. Inputs include capital costs, fuel, operation, maintenance, and discount rate. Used to compare technologies like coal, gas, nuclear, solar, and wind.",
            tags=["levelized_cost_of_energy_lcoe", "economics", "comparison"],
            weight=1.0
        ),
        SearchDocument(
            id="ppa_001",
            title="Power Purchase Agreement (PPA) Structure",
            content="PPAs define terms for selling electricity between generators and buyers. Key elements include pricing, contract duration, delivery obligations, and risk allocation. PPAs support financing for renewable and conventional projects.",
            tags=["power_purchase_agreement_ppa_structure", "contract", "financing"],
            weight=1.0
        ),
        SearchDocument(
            id="chp_001",
            title="Combined Heat and Power (CHP) Cogeneration",
            content="CHP systems produce electricity and useful heat from a single fuel source. Applications include industrial plants and district heating. Benefits include improved efficiency and reduced emissions.",
            tags=["combined_heat_and_power_chp_cogeneration", "efficiency", "industrial"],
            weight=1.0
        ),
        SearchDocument(
            id="chp_002",
            title="CHP System Design and Operation",
            content="Designing CHP systems involves selecting prime movers, heat recovery units, and integration with site energy needs. Operation focuses on balancing electricity and heat output for optimal performance.",
            tags=["combined_heat_and_power_chp_cogeneration", "design", "operation"],
            weight=1.0
        ),
        SearchDocument(
            id="microgrid_001",
            title="Microgrid Design and Operation Principles",
            content="Microgrids integrate distributed generation, storage, and loads. Control systems manage islanding, synchronization, and dispatch. Benefits include resilience, local energy optimization, and renewable integration.",
            tags=["microgrid_design_and_operation", "distributed_generation", "resilience"],
            weight=1.0
        ),
        SearchDocument(
            id="microgrid_002",
            title="Microgrid Grid Interconnection and Standards",
            content="Microgrids must comply with IEEE 1547 and NERC standards for interconnection and reliability. Protection schemes and communication protocols ensure safe operation during grid-connected and islanded modes.",
            tags=["microgrid_design_and_operation", "ieee_1547_grid_interconnection_standard", "nerc_reliability_standards_compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="solar_003",
            title="Solar PV Maintenance and Performance Monitoring",
            content="Regular cleaning, inspection, and inverter maintenance improve PV system performance. Monitoring systems track energy yield, detect faults, and optimize operation. Data analytics support predictive maintenance.",
            tags=["solar_photovoltaic_pv_systems", "maintenance", "monitoring"],
            weight=1.0
        ),
        SearchDocument(
            id="wind_003",
            title="Wind Turbine Maintenance Strategies",
            content="Maintenance of wind turbines includes blade inspection, gearbox lubrication, and generator testing. Predictive analytics and remote monitoring reduce downtime and improve reliability.",
            tags=["wind_turbine_power_generation", "maintenance", "reliability"],
            weight=1.0
        ),
        SearchDocument(
            id="hydro_003",
            title="Hydroelectric Environmental Impact Mitigation",
            content="Mitigation measures for hydroelectric dams include fish ladders, sediment management, and water quality monitoring. Environmental compliance is essential for sustainable operation.",
            tags=["hydroelectric_dam_operation", "environment", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="coal_003",
            title="Advanced Coal Plant Technologies",
            content="Ultra-supercritical coal plants operate at higher temperatures and pressures, improving efficiency and reducing emissions. Integrated gasification combined cycle (IGCC) enables carbon capture and cleaner operation.",
            tags=["coal_fired_power_plant_operation", "igcc", "carbon_capture"],
            weight=1.0
        ),
        SearchDocument(
            id="pwr_002",
            title="PWR Safety Systems and Emergency Procedures",
            content="PWRs feature multiple safety systems including emergency core cooling, containment, and backup power. Procedures for loss of coolant, reactor shutdown, and evacuation are regularly drilled.",
            tags=["pressurized_water_reactor_pwr", "safety", "emergency"],
            weight=1.0
        ),
        SearchDocument(
            id="bwr_002",
            title="BWR Radiation Protection and Water Chemistry",
            content="Radiation protection in BWRs includes shielding, monitoring, and controlled access. Water chemistry management prevents corrosion and maintains reactor integrity.",
            tags=["boiling_water_reactor_bwr", "radiation", "chemistry"],
            weight=1.0
        ),
        SearchDocument(
            id="ccgt_003",
            title="CCGT Flexibility and Ancillary Services",
            content="CCGT plants provide ancillary services such as frequency regulation and spinning reserve. Fast ramping and part-load operation support grid stability and renewable integration.",
            tags=["combined_cycle_gas_turbine_ccgt", "ancillary_services", "grid"],
            weight=1.0
        ),
        SearchDocument(
            id="microgrid_003",
            title="Microgrid Energy Storage Integration",
            content="Energy storage systems in microgrids enable load balancing, peak shaving, and backup power. Technologies include lithium-ion batteries, flow batteries, and thermal storage.",
            tags=["microgrid_design_and_operation", "energy_storage", "integration"],
            weight=1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)