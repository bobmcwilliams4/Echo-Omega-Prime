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
        self.doc_tokens: Dict[str, List[str]] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._dirty = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            tf_counter = Counter(tokens)
            for term, freq in tf_counter.items():
                self.term_freqs[doc.id][term] = freq
                self.term_doc_freq[term] += 1
            self._dirty = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        with self.lock:
            if self._dirty:
                self._recalculate_stats()
        scores = {}
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, tokens)
            tfidf_score = self._score_tfidf(doc_id, tokens)
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            scores[doc_id] = combined_score * doc.weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": len(self.documents),
                "avg_doc_length": self.avg_doc_length,
                "num_terms": len(self.term_doc_freq)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        with self.lock:
            if self._dirty:
                self._recalculate_stats()
            if term in self._idf_cache:
                return self._idf_cache[term]
            N = len(self.documents)
            df = self.term_doc_freq.get(term, 0)
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
            self._idf_cache[term] = idf
            return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        for term in query_terms:
            idf = self._compute_idf(term)
            tf = self.term_freqs[doc_id].get(term, 0)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_length / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        if doc_length == 0:
            return 0.0
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            tf_norm = tf / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _recalculate_stats(self):
        total_length = sum(self.doc_lengths.values())
        num_docs = len(self.documents)
        self.avg_doc_length = total_length / num_docs if num_docs > 0 else 0.0
        self._idf_cache.clear()
        self._dirty = False

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + '...'
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet + '...'

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
            id="1",
            title="Turbofan Engine Operation Principles",
            content="The AERO01 turbofan engine utilizes a high bypass ratio for efficient thrust generation. Operation involves monitoring N1 and N2 spool speeds, EGT, and fuel flow. Engine control is managed via FADEC, ensuring optimal performance and safety.",
            tags=["turbofan_engine_operation", "FADEC", "N1", "N2", "EGT"],
            weight=1.2
        ),
        SearchDocument(
            id="2",
            title="Fly-By-Wire Flight Controls Overview",
            content="Fly-by-wire flight control systems on AERO01 aircraft replace mechanical linkages with electronic signals. Control laws, redundancy, and failure modes are managed by the flight control computers, providing enhanced stability and maneuverability.",
            tags=["fly_by_wire_flight_controls", "flight_control_computers", "redundancy"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Glass Cockpit Avionics Integration",
            content="AERO01 glass cockpit features advanced avionics, including multi-function displays (MFDs), primary flight displays (PFDs), and integrated flight management systems. Data from sensors and systems is presented for pilot situational awareness.",
            tags=["glass_cockpit_avionics", "MFD", "PFD", "flight_management_system"],
            weight=1.1
        ),
        SearchDocument(
            id="4",
            title="Aircraft Electrical System Architecture",
            content="The electrical system provides power distribution to all aircraft subsystems. AERO01 uses AC and DC buses, generators, batteries, and emergency power sources. Electrical load management is critical for safe operation.",
            tags=["aircraft_electrical_system", "power_distribution", "generators", "batteries"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Hydraulic Flight Control System",
            content="Hydraulic actuators power the primary flight controls. The AERO01 system includes redundant hydraulic pumps, reservoirs, and accumulators. System pressure and fluid levels are monitored for reliability.",
            tags=["hydraulic_flight_control_system", "hydraulic_actuators", "redundancy"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Aircraft Fuel System Management",
            content="Fuel tanks, pumps, and valves are managed to ensure proper engine feed and balance. The AERO01 fuel system includes cross-feed capability and automatic transfer functions.",
            tags=["aircraft_fuel_system", "fuel_tanks", "cross-feed", "automatic_transfer"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Bleed Air Pneumatic System",
            content="Bleed air is extracted from the engine compressors for cabin pressurization, anti-icing, and pneumatic systems. The AERO01 bleed air system features pressure regulation and overheat protection.",
            tags=["bleed_air_pneumatic_system", "cabin_pressurization", "anti-icing"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Landing Gear System and Operation",
            content="The landing gear system includes retractable main and nose gear, hydraulic actuators, and electronic control. Gear position indicators and emergency extension procedures are part of AERO01 design.",
            tags=["landing_gear_system", "hydraulic_actuators", "emergency_extension"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Environmental Control System (ECS)",
            content="ECS manages cabin temperature, humidity, and air quality. The AERO01 ECS uses bleed air, refrigeration units, and HEPA filters to ensure passenger comfort and safety.",
            tags=["environmental_control_system", "ECS", "bleed_air", "HEPA_filters"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Fire Detection and Suppression",
            content="Fire detection sensors monitor engine, APU, and cargo compartments. Suppression systems use halon or water mist for rapid response. AERO01 integrates automatic and manual activation.",
            tags=["fire_detection_suppression", "halon", "water_mist", "automatic_activation"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Oxygen System for Crew and Passengers",
            content="The oxygen system provides supplemental O2 during emergencies. AERO01 features chemical oxygen generators and pressurized tanks, with automatic deployment in case of cabin depressurization.",
            tags=["oxygen_system", "chemical_oxygen_generator", "pressurized_tanks"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="APU Auxiliary Power Unit",
            content="The APU supplies electrical and pneumatic power during ground operations and engine start. AERO01 APU features automatic start, shutdown, and fire protection.",
            tags=["APU_auxiliary_power_unit", "electrical_power", "pneumatic_power"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Ice Protection Systems",
            content="Ice protection includes wing and engine anti-ice, pitot heat, and windshield heating. AERO01 uses bleed air and electrical heaters to prevent ice accumulation.",
            tags=["ice_protection_systems", "wing_anti_ice", "pitot_heat", "windshield_heating"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Flight Management System (FMS)",
            content="FMS automates navigation, performance calculations, and flight planning. AERO01 integrates FMS with autopilot and glass cockpit displays for efficient route management.",
            tags=["flight_management_system", "navigation", "performance_calculation"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="TCAS Traffic Alert and Collision Avoidance",
            content="TCAS monitors nearby aircraft and provides traffic advisories and resolution alerts. AERO01 TCAS integrates with cockpit displays and autopilot for automated avoidance.",
            tags=["TCAS_traffic_alert", "collision_avoidance", "traffic_advisory"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="EGPWS Terrain Awareness",
            content="EGPWS uses GPS and terrain databases to alert pilots of potential ground proximity hazards. AERO01 EGPWS issues visual and audio warnings for terrain avoidance.",
            tags=["EGPWS_terrain_awareness", "GPS", "terrain_database", "audio_warning"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Autopilot and Autothrottle Systems",
            content="Autopilot controls pitch, roll, and yaw, while autothrottle manages engine thrust. AERO01 integrates these systems with FMS and glass cockpit for automated flight.",
            tags=["autopilot_autothrottle", "pitch_control", "thrust_management"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="MSG-3 Maintenance Program",
            content="MSG-3 methodology optimizes maintenance intervals and tasks based on reliability analysis. AERO01 maintenance program includes scheduled inspections and predictive maintenance.",
            tags=["MSG3_maintenance_program", "reliability_analysis", "scheduled_inspection"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Airworthiness Directives Compliance",
            content="Airworthiness directives (ADs) mandate corrective actions for safety issues. AERO01 tracks AD compliance through maintenance records and automated alerts.",
            tags=["airworthiness_directives", "AD_compliance", "maintenance_records"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Part 25 Certification Standards",
            content="AERO01 is certified under FAA Part 25 standards for transport category aircraft. Certification covers structural integrity, systems safety, and performance requirements.",
            tags=["Part_25_certification", "FAA", "structural_integrity", "systems_safety"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Weight and Balance Management",
            content="Proper weight and balance is critical for safe flight. AERO01 uses digital load management systems to calculate center of gravity and ensure compliance with limits.",
            tags=["weight_and_balance", "load_management", "center_of_gravity"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Engine FADEC Control Logic",
            content="Full Authority Digital Engine Control (FADEC) manages engine parameters, including thrust, fuel flow, and temperature. AERO01 FADEC provides real-time diagnostics and fault detection.",
            tags=["turbofan_engine_operation", "FADEC", "diagnostics", "fault_detection"],
            weight=1.1
        ),
        SearchDocument(
            id="23",
            title="Cabin Pressurization and Safety",
            content="Cabin pressure is regulated by outflow valves and monitored by sensors. AERO01 ECS ensures safe altitude and oxygen levels for passengers and crew.",
            tags=["environmental_control_system", "cabin_pressurization", "outflow_valve"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Redundant Hydraulic Systems",
            content="AERO01 features triple-redundant hydraulic systems for flight control reliability. Each system operates independently with cross-connect capability.",
            tags=["hydraulic_flight_control_system", "redundancy", "cross_connect"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Integrated Avionics for Engine Monitoring",
            content="Glass cockpit avionics display real-time engine parameters, including N1, N2, EGT, and fuel flow. AERO01 integrates engine monitoring with alerting systems for pilot awareness.",
            tags=["glass_cockpit_avionics", "engine_monitoring", "alerting_system"],
            weight=1.1
        ),
        SearchDocument(
            id="26",
            title="Landing Gear Emergency Extension Procedures",
            content="AERO01 landing gear system includes manual and hydraulic emergency extension options. Procedures ensure safe gear deployment during system failures.",
            tags=["landing_gear_system", "emergency_extension", "manual_extension"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Bleed Air Overheat Protection",
            content="Bleed air system incorporates temperature sensors and shutoff valves to prevent overheating. AERO01 safety protocols include automatic shutdown and alerting.",
            tags=["bleed_air_pneumatic_system", "overheat_protection", "temperature_sensor"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Fuel Cross-Feed Operations",
            content="AERO01 fuel system supports cross-feed between tanks for balance and redundancy. Automated valves and sensors manage fuel distribution during flight.",
            tags=["aircraft_fuel_system", "cross-feed", "automated_valve"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Fire Suppression in Engine Compartments",
            content="Engine fire suppression uses halon discharge and temperature sensors for rapid response. AERO01 integrates automatic and manual activation for safety.",
            tags=["fire_detection_suppression", "engine_fire", "halon_discharge"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="APU Fire Detection and Shutdown",
            content="APU fire detection system uses sensors and automatic shutdown logic. AERO01 ensures rapid response and crew alerting for fire safety.",
            tags=["APU_auxiliary_power_unit", "fire_detection", "automatic_shutdown"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)