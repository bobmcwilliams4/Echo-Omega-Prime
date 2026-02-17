import math
import threading
import re
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
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.lock = threading.Lock()
        self._update_stats()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.term_freqs[token][doc.id] = count
                self.term_doc_freqs[token] += 1
            self._update_stats()

    def _update_stats(self):
        if self.documents:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)
        else:
            self.avg_doc_length = 0.0
        self.idf_cache.clear()
        self.tf_cache.clear()

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freqs.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            score += idf * (numerator / (denominator + 1e-10))
        return score * doc.weight

    def _score_tf_idf(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs.get(term, {}).get(doc_id, 0)
            norm_tf = tf / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: Dict[str, float] = {}
        for doc_id in self.documents:
            if use_bm25:
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tf_idf(query_terms, doc_id)
            if score > 0:
                scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 40) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            return ' '.join(tokens[:snippet_len])
        start = max(indices[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(tokens))
        snippet = tokens[start:end]
        return ' '.join(snippet)

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'num_unique_terms': len(self.term_doc_freqs)
        }

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
            "1",
            "Turbofan Engine Operation Overview",
            "Turbofan engines provide thrust by combining core combustion with bypass airflow. Operation involves monitoring EGT, N1, N2, fuel flow, and vibration. Emergency procedures include engine shutdown, fire suppression, and restart protocols.",
            ["turbofan_engine_operation", "emergency_procedures"],
            1.0
        ),
        SearchDocument(
            "2",
            "Fly-By-Wire Flight Controls",
            "Fly-by-wire systems replace mechanical linkages with electronic signals. Flight control computers interpret pilot inputs, apply laws for stability, and actuate hydraulic servos. Fault isolation and redundancy are critical for safe operation.",
            ["fly_by_wire_flight_controls", "hydraulic_flight_control_system"],
            1.0
        ),
        SearchDocument(
            "3",
            "Glass Cockpit Avionics",
            "Glass cockpits use digital displays for flight, navigation, and engine data. Integrated systems include EFIS, FMS, and EICAS. Crew must monitor alerts, perform system resets, and follow abnormal procedures for display failures.",
            ["glass_cockpit_avionics", "flight_management_system"],
            1.0
        ),
        SearchDocument(
            "4",
            "Aircraft Electrical System",
            "Aircraft electrical systems distribute power from generators, batteries, and external sources. Bus architecture ensures redundancy. Emergency procedures involve load shedding, generator isolation, and battery-only operation.",
            ["aircraft_electrical_system", "emergency_procedures"],
            1.0
        ),
        SearchDocument(
            "5",
            "Hydraulic Flight Control System",
            "Hydraulic systems actuate flight controls, landing gear, and brakes. Fluid pressure is monitored for leaks and failures. Backup systems include electric pumps and manual reversion. Emergency landing gear extension is a key procedure.",
            ["hydraulic_flight_control_system", "landing_gear_system"],
            1.0
        ),
        SearchDocument(
            "6",
            "Aircraft Fuel System",
            "Fuel systems manage storage, transfer, and delivery to engines and APU. Crossfeed valves, boost pumps, and fuel quantity indication are monitored. Emergency procedures include fuel leak isolation and single-engine operation.",
            ["aircraft_fuel_system", "APU_auxiliary_power_unit"],
            1.0
        ),
        SearchDocument(
            "7",
            "Bleed Air Pneumatic System",
            "Bleed air is extracted from engines for cabin pressurization, anti-ice, and pneumatic systems. Overheat and leak detection are critical. Crew must follow procedures for bleed air failure and alternate source selection.",
            ["bleed_air_pneumatic_system", "ice_protection_systems"],
            1.0
        ),
        SearchDocument(
            "8",
            "Landing Gear System",
            "Landing gear systems include extension, retraction, and steering. Hydraulic actuators and electrical controls are monitored. Emergency extension uses gravity or alternate hydraulic sources. Tire and brake inspection is routine.",
            ["landing_gear_system", "hydraulic_flight_control_system"],
            1.0
        ),
        SearchDocument(
            "9",
            "Environmental Control System",
            "Environmental control systems regulate cabin temperature, humidity, and pressurization. Sensors monitor air quality and pressure. Emergency procedures address smoke, loss of pressurization, and alternate air sources.",
            ["environmental_control_system", "bleed_air_pneumatic_system"],
            1.0
        ),
        SearchDocument(
            "10",
            "Fire Detection and Suppression",
            "Fire detection systems use sensors in engines, APU, and cargo compartments. Suppression involves discharge of extinguishing agents. Crew follows checklists for fire warning, engine shutdown, and evacuation.",
            ["fire_detection_suppression", "APU_auxiliary_power_unit"],
            1.0
        ),
        SearchDocument(
            "11",
            "Oxygen System",
            "Oxygen systems provide supplemental and emergency oxygen to crew and passengers. Portable bottles, masks, and chemical generators are used. Crew must monitor pressure, flow, and perform emergency descent procedures.",
            ["oxygen_system", "emergency_procedures"],
            1.0
        ),
        SearchDocument(
            "12",
            "APU Auxiliary Power Unit",
            "The APU supplies electrical and pneumatic power for ground operations and engine start. Monitoring includes EGT, RPM, and oil pressure. Emergency shutdown procedures are followed for fire or overspeed.",
            ["APU_auxiliary_power_unit", "aircraft_electrical_system"],
            1.0
        ),
        SearchDocument(
            "13",
            "Ice Protection Systems",
            "Ice protection uses bleed air, electrical heaters, and chemical anti-ice. Wing, engine, and probe heating are monitored. Crew follows procedures for icing conditions, system failures, and alternate protection.",
            ["ice_protection_systems", "bleed_air_pneumatic_system"],
            1.0
        ),
        SearchDocument(
            "14",
            "Flight Management System",
            "FMS automates navigation, performance, and fuel management. Inputs include route, altitude, and speed. Crew monitors database integrity, performs updates, and follows procedures for FMS failure.",
            ["flight_management_system", "glass_cockpit_avionics"],
            1.0
        ),
        SearchDocument(
            "15",
            "TCAS Traffic Alert and Collision Avoidance",
            "TCAS monitors transponder signals to detect and avoid collisions. Resolution advisories direct climb or descent. Crew must follow advisories and report TCAS events according to regulations.",
            ["TCAS_traffic_alert", "glass_cockpit_avionics"],
            1.0
        ),
        SearchDocument(
            "16",
            "EGPWS Terrain Awareness",
            "EGPWS uses GPS and radar altimeter data to warn of terrain proximity. Crew responds to warnings with escape maneuvers. System integrity is checked during preflight and after alerts.",
            ["EGPWS_terrain_awareness", "glass_cockpit_avionics"],
            1.0
        ),
        SearchDocument(
            "17",
            "Autopilot and Autothrottle",
            "Autopilot controls pitch, roll, and yaw. Autothrottle manages engine thrust. Crew monitors mode annunciations, disengages for manual control, and follows procedures for system failures.",
            ["autopilot_autothrottle", "glass_cockpit_avionics"],
            1.0
        ),
        SearchDocument(
            "18",
            "MSG-3 Maintenance Program",
            "MSG-3 defines maintenance tasks based on reliability and safety. Crew performs scheduled inspections, defect reporting, and corrective actions. Documentation is maintained for airworthiness compliance.",
            ["MSG3_maintenance_program", "airworthiness_directives"],
            1.0
        ),
        SearchDocument(
            "19",
            "Airworthiness Directives",
            "Airworthiness directives mandate corrective actions for safety issues. Crew reviews directives, implements changes, and records compliance. Non-compliance may result in grounding.",
            ["airworthiness_directives", "Part_25_certification"],
            1.0
        ),
        SearchDocument(
            "20",
            "Part 25 Certification",
            "Part 25 certification sets standards for transport aircraft design, performance, and safety. Crew ensures compliance with structural, systems, and operational requirements.",
            ["Part_25_certification", "airworthiness_directives"],
            1.0
        ),
        SearchDocument(
            "21",
            "Weight and Balance",
            "Weight and balance calculations ensure safe aircraft operation. Crew monitors loading, fuel distribution, and center of gravity. Procedures address out-of-limit conditions and corrective actions.",
            ["weight_and_balance", "aircraft_fuel_system"],
            1.0
        ),
        SearchDocument(
            "22",
            "Engine Fire Emergency Procedures",
            "Engine fire procedures include identification, shutdown, fire suppression, and evacuation. Crew follows checklists, communicates with ATC, and coordinates with cabin crew.",
            ["fire_detection_suppression", "turbofan_engine_operation"],
            1.0
        ),
        SearchDocument(
            "23",
            "Cabin Pressurization Loss",
            "Loss of cabin pressurization requires emergency descent, oxygen mask deployment, and passenger briefing. Crew follows procedures for alternate air sources and landing at nearest airport.",
            ["environmental_control_system", "oxygen_system"],
            1.0
        ),
        SearchDocument(
            "24",
            "Electrical Failure Emergency",
            "Electrical failure procedures include load shedding, generator isolation, and battery operation. Crew uses standby instruments and follows checklists for safe flight and landing.",
            ["aircraft_electrical_system", "glass_cockpit_avionics"],
            1.0
        ),
        SearchDocument(
            "25",
            "Hydraulic System Failure",
            "Hydraulic failure procedures include identifying affected controls, switching to backup systems, and manual reversion. Crew follows checklists for landing gear extension and brake operation.",
            ["hydraulic_flight_control_system", "landing_gear_system"],
            1.0
        ),
        SearchDocument(
            "26",
            "Fuel Leak Emergency",
            "Fuel leak procedures involve isolation, crossfeed management, and monitoring fuel quantity. Crew follows checklists for single-engine operation and landing at nearest airport.",
            ["aircraft_fuel_system", "emergency_procedures"],
            1.0
        ),
        SearchDocument(
            "27",
            "Bleed Air Leak Emergency",
            "Bleed air leak procedures include isolation, alternate source selection, and monitoring for overheat. Crew follows checklists for safe operation and landing.",
            ["bleed_air_pneumatic_system", "emergency_procedures"],
            1.0
        ),
        SearchDocument(
            "28",
            "Landing Gear Extension Failure",
            "Landing gear extension failure procedures include alternate hydraulic activation, gravity extension, and visual inspection. Crew follows checklists for safe landing.",
            ["landing_gear_system", "hydraulic_flight_control_system"],
            1.0
        ),
        SearchDocument(
            "29",
            "Smoke and Fire in Cabin",
            "Smoke and fire in cabin procedures include identifying source, using fire extinguishers, and deploying oxygen masks. Crew follows checklists for evacuation and communication with ATC.",
            ["fire_detection_suppression", "oxygen_system"],
            1.0
        ),
        SearchDocument(
            "30",
            "APU Fire Emergency",
            "APU fire procedures include shutdown, fire suppression, and evacuation. Crew follows checklists and communicates with ground personnel.",
            ["APU_auxiliary_power_unit", "fire_detection_suppression"],
            1.0
        ),
        SearchDocument(
            "31",
            "Ice Protection Failure",
            "Ice protection failure procedures include alternate system activation, monitoring for icing, and adjusting flight path. Crew follows checklists for safe operation.",
            ["ice_protection_systems", "bleed_air_pneumatic_system"],
            1.0
        ),
        SearchDocument(
            "32",
            "Flight Management System Failure",
            "FMS failure procedures include manual navigation, alternate system use, and database integrity checks. Crew follows checklists for safe flight.",
            ["flight_management_system", "glass_cockpit_avionics"],
            1.0
        ),
        SearchDocument(
            "33",
            "TCAS Failure",
            "TCAS failure procedures include visual traffic monitoring, communication with ATC, and following standard separation procedures.",
            ["TCAS_traffic_alert", "glass_cockpit_avionics"],
            1.0
        ),
        SearchDocument(
            "34",
            "EGPWS Failure",
            "EGPWS failure procedures include manual terrain awareness, chart review, and communication with ATC. Crew follows checklists for safe operation.",
            ["EGPWS_terrain_awareness", "glass_cockpit_avionics"],
            1.0
        ),
        SearchDocument(
            "35",
            "Autopilot Failure",
            "Autopilot failure procedures include manual control, mode disengagement, and monitoring flight parameters. Crew follows checklists for safe operation.",
            ["autopilot_autothrottle", "glass_cockpit_avionics"],
            1.0
        ),
        SearchDocument(
            "36",
            "MSG-3 Inspection Procedures",
            "MSG-3 inspection procedures include scheduled maintenance, defect reporting, and corrective actions. Crew maintains documentation for airworthiness compliance.",
            ["MSG3_maintenance_program", "airworthiness_directives"],
            1.0
        ),
        SearchDocument(
            "37",
            "Weight and Balance Emergency",
            "Weight and balance emergency procedures include redistribution of load, fuel transfer, and monitoring center of gravity. Crew follows checklists for safe flight.",
            ["weight_and_balance", "aircraft_fuel_system"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)