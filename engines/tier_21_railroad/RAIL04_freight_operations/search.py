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
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.total_terms: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            self.total_docs += 1
            term_counts = Counter(tokens)
            self.term_freqs[doc.id] = term_counts
            for term in term_counts:
                self.term_doc_freqs[term] += 1
            self.avg_doc_length = self.total_terms / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores: Dict[int, float] = defaultdict(float)
        tfidf_scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            scores[doc_id] = combined_score * doc.weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'total_terms': self.total_terms,
            'unique_terms': len(self.term_doc_freqs)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1)
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 1)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        term_counts = self.term_freqs.get(doc_id, {})
        for term in query_tokens:
            tf = term_counts.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_length / avg_dl)
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vector = self._tfidf_cache[doc_id]
        else:
            tfidf_vector = {}
            term_counts = self.term_freqs.get(doc_id, {})
            doc_length = self.doc_lengths.get(doc_id, 1)
            for term, tf in term_counts.items():
                tf_norm = tf / doc_length
                idf = self._compute_idf(term)
                tfidf_vector[term] = tf_norm * idf
            self._tfidf_cache[doc_id] = tfidf_vector
        score = 0.0
        for term in query_tokens:
            score += tfidf_vector.get(term, 0.0)
        return score

    def _make_snippet(self, content: str, query_tokens: List[str], snippet_len: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return ' '.join(tokens[:snippet_len])
        start = max(positions[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(tokens))
        snippet = ' '.join(tokens[start:end])
        for term in query_tokens:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1, "Turbofan Engine Operation",
                "The RAIL04 engine utilizes a high-bypass turbofan design for optimal fuel efficiency and thrust. Engine control is managed by FADEC, monitoring N1/N2 speeds, EGT, and fuel flow.",
                ["turbofan", "engine", "FADEC", "N1", "N2", "EGT", "fuel"], 1.0
            ),
            SearchDocument(
                2, "Fly-by-Wire Flight Controls",
                "RAIL04 features fly-by-wire flight control systems, replacing mechanical linkages with electronic signals. Flight computers interpret pilot inputs and adjust control surfaces for stability.",
                ["fly_by_wire", "flight_controls", "electronics", "stability"], 1.0
            ),
            SearchDocument(
                3, "Glass Cockpit Avionics",
                "The glass cockpit integrates digital displays for navigation, engine monitoring, and system status. Avionics include PFD, MFD, and EICAS, enhancing situational awareness.",
                ["glass_cockpit", "avionics", "PFD", "MFD", "EICAS"], 1.0
            ),
            SearchDocument(
                4, "Aircraft Electrical System",
                "RAIL04 electrical system distributes power from generators, batteries, and external sources. Bus architecture ensures redundancy for critical systems and flight controls.",
                ["electrical", "generators", "batteries", "bus", "redundancy"], 1.0
            ),
            SearchDocument(
                5, "Hydraulic Flight Control System",
                "Hydraulic actuators power RAIL04's primary flight controls. Multiple hydraulic circuits provide fail-safe operation for ailerons, elevators, and rudder.",
                ["hydraulic", "actuators", "flight_controls", "fail_safe"], 1.0
            ),
            SearchDocument(
                6, "Aircraft Fuel System",
                "Fuel tanks, pumps, and valves are managed by the FMS to ensure proper distribution and balance. Crossfeed capability allows fuel transfer between tanks during flight.",
                ["fuel_system", "tanks", "pumps", "valves", "FMS", "crossfeed"], 1.0
            ),
            SearchDocument(
                7, "Bleed Air Pneumatic System",
                "Engine bleed air is used for cabin pressurization, anti-icing, and pneumatic systems. Pressure regulators and heat exchangers maintain safe operation.",
                ["bleed_air", "pneumatic", "pressurization", "anti_icing"], 1.0
            ),
            SearchDocument(
                8, "Landing Gear System",
                "RAIL04's landing gear is hydraulically actuated, with electronic sensors for position indication. Emergency extension is available in case of hydraulic failure.",
                ["landing_gear", "hydraulic", "sensors", "emergency"], 1.0
            ),
            SearchDocument(
                9, "Environmental Control System",
                "Cabin temperature, humidity, and air quality are regulated by the ECS. The system uses bleed air, refrigeration units, and HEPA filters for passenger comfort.",
                ["environmental_control", "ECS", "bleed_air", "refrigeration", "HEPA"], 1.0
            ),
            SearchDocument(
                10, "Fire Detection and Suppression",
                "RAIL04 is equipped with fire detection sensors in the engine, APU, and cargo compartments. Suppression systems use halon or water mist to extinguish fires.",
                ["fire_detection", "suppression", "halon", "APU", "cargo"], 1.0
            ),
            SearchDocument(
                11, "Oxygen System",
                "Passenger and crew oxygen systems provide supplemental oxygen during depressurization. Chemical generators and storage bottles are monitored for pressure and flow.",
                ["oxygen", "depressurization", "chemical_generators", "storage_bottles"], 1.0
            ),
            SearchDocument(
                12, "APU Auxiliary Power Unit",
                "The APU supplies electrical and pneumatic power during ground operations. It can be started automatically or manually, and monitored via cockpit displays.",
                ["APU", "auxiliary_power", "electrical", "pneumatic", "cockpit"], 1.0
            ),
            SearchDocument(
                13, "Ice Protection Systems",
                "RAIL04 uses thermal and pneumatic anti-icing for engine inlets, wing leading edges, and pitot tubes. Automatic and manual modes are available.",
                ["ice_protection", "thermal", "pneumatic", "anti_icing", "pitot"], 1.0
            ),
            SearchDocument(
                14, "Flight Management System",
                "The FMS automates navigation, performance calculations, and fuel management. It interfaces with autopilot and glass cockpit for route optimization.",
                ["FMS", "navigation", "performance", "autopilot", "glass_cockpit"], 1.0
            ),
            SearchDocument(
                15, "TCAS Traffic Alert and Collision Avoidance",
                "TCAS monitors nearby aircraft and issues traffic advisories and resolution alerts to prevent mid-air collisions. Integrated with cockpit displays.",
                ["TCAS", "traffic_alert", "collision_avoidance", "cockpit"], 1.0
            ),
            SearchDocument(
                16, "EGPWS Terrain Awareness",
                "EGPWS uses terrain databases and radar altimeter data to warn pilots of terrain proximity. Visual and audio alerts are provided for safety.",
                ["EGPWS", "terrain_awareness", "radar_altimeter", "alerts"], 1.0
            ),
            SearchDocument(
                17, "Autopilot and Autothrottle",
                "RAIL04 autopilot controls pitch, roll, and yaw, while autothrottle manages engine thrust. Integrated with FMS for automated flight profiles.",
                ["autopilot", "autothrottle", "pitch", "roll", "yaw", "thrust"], 1.0
            ),
            SearchDocument(
                18, "MSG-3 Maintenance Program",
                "MSG-3 methodology structures maintenance tasks based on reliability and safety. Scheduled inspections and component replacements ensure airworthiness.",
                ["MSG3", "maintenance", "reliability", "inspections", "airworthiness"], 1.0
            ),
            SearchDocument(
                19, "Airworthiness Directives",
                "Airworthiness directives mandate corrective actions for safety issues. Compliance is tracked in the maintenance program and reported to authorities.",
                ["airworthiness", "directives", "safety", "maintenance"], 1.0
            ),
            SearchDocument(
                20, "Part 25 Certification",
                "RAIL04 complies with FAA Part 25 certification standards for transport category aircraft. Requirements cover structure, systems, and performance.",
                ["Part_25", "certification", "FAA", "structure", "systems"], 1.0
            ),
            SearchDocument(
                21, "Weight and Balance",
                "Proper weight and balance calculations are essential for safe flight. The FMS assists with load distribution and center of gravity management.",
                ["weight", "balance", "FMS", "load_distribution", "center_of_gravity"], 1.0
            ),
            SearchDocument(
                22, "Engine Bleed Air for Cabin Pressurization",
                "Bleed air from the RAIL04 engine is routed through pressure regulators and heat exchangers to maintain cabin altitude and comfort.",
                ["bleed_air", "cabin_pressurization", "heat_exchanger", "regulator"], 1.0
            ),
            SearchDocument(
                23, "Hydraulic System Redundancy",
                "RAIL04 hydraulic systems are designed with multiple circuits and reservoirs to ensure continued operation in case of leaks or failures.",
                ["hydraulic", "redundancy", "circuits", "reservoirs", "failures"], 1.0
            ),
            SearchDocument(
                24, "FADEC Engine Control",
                "Full Authority Digital Engine Control (FADEC) automates engine management, optimizing performance and protecting against overspeed and overtemperature.",
                ["FADEC", "engine_control", "performance", "overspeed", "overtemperature"], 1.0
            ),
            SearchDocument(
                25, "Cabin Environmental Monitoring",
                "Sensors monitor cabin temperature, humidity, and air quality. ECS adjusts airflow and filtration to maintain passenger comfort.",
                ["environmental", "monitoring", "ECS", "air_quality", "filtration"], 1.0
            ),
            SearchDocument(
                26, "Landing Gear Emergency Extension",
                "RAIL04 landing gear can be extended manually in case of hydraulic failure. Mechanical locks secure gear in the down position.",
                ["landing_gear", "emergency", "manual_extension", "mechanical_locks"], 1.0
            ),
            SearchDocument(
                27, "Aircraft Fuel Crossfeed Operations",
                "Crossfeed valves allow fuel transfer between tanks to balance weight and ensure engine supply during abnormal operations.",
                ["fuel", "crossfeed", "valves", "balance", "engine_supply"], 1.0
            ),
            SearchDocument(
                28, "Fire Detection Sensors",
                "RAIL04 fire detection system uses thermal and optical sensors to identify fires in engines and cargo compartments.",
                ["fire_detection", "thermal", "optical", "engine", "cargo"], 1.0
            ),
            SearchDocument(
                29, "APU Start and Monitoring",
                "The APU can be started from the cockpit or automatically during ground operations. Monitoring includes temperature, RPM, and electrical output.",
                ["APU", "start", "monitoring", "temperature", "RPM", "electrical"], 1.0
            ),
            SearchDocument(
                30, "Ice Protection for Pitot Tubes",
                "Pitot tubes are heated electrically to prevent ice formation, ensuring accurate airspeed readings during flight.",
                ["ice_protection", "pitot", "electrical", "heated", "airspeed"], 1.0
            ),
            SearchDocument(
                31, "Flight Management System Route Optimization",
                "FMS calculates optimal flight routes based on weather, fuel, and performance data, interfacing with autopilot for automated navigation.",
                ["FMS", "route_optimization", "weather", "fuel", "autopilot"], 1.0
            ),
            SearchDocument(
                32, "TCAS Resolution Advisory",
                "TCAS issues resolution advisories to pilots, instructing climb or descent to avoid collision with conflicting traffic.",
                ["TCAS", "resolution_advisory", "climb", "descent", "collision"], 1.0
            ),
            SearchDocument(
                33, "EGPWS Visual and Audio Alerts",
                "EGPWS provides visual and audio alerts for terrain proximity, using radar altimeter and terrain database inputs.",
                ["EGPWS", "visual_alert", "audio_alert", "radar_altimeter", "terrain"], 1.0
            ),
            SearchDocument(
                34, "Autopilot Flight Profiles",
                "Autopilot manages flight profiles including climb, cruise, and descent, adjusting pitch, roll, and yaw as needed.",
                ["autopilot", "flight_profile", "climb", "cruise", "descent"], 1.0
            ),
            SearchDocument(
                35, "MSG-3 Scheduled Inspections",
                "Scheduled inspections under MSG-3 ensure continued airworthiness and reliability of RAIL04 components.",
                ["MSG3", "scheduled_inspections", "airworthiness", "reliability"], 1.0
            ),
            SearchDocument(
                36, "FAA Part 25 Structural Requirements",
                "RAIL04 meets FAA Part 25 structural requirements for transport category aircraft, including load factors and fatigue limits.",
                ["Part_25", "FAA", "structural", "load_factors", "fatigue"], 1.0
            ),
            SearchDocument(
                37, "Weight and Balance Center of Gravity",
                "FMS assists in calculating center of gravity to ensure proper weight and balance for safe flight.",
                ["weight", "balance", "center_of_gravity", "FMS"], 1.0
            ),
            SearchDocument(
                38, "Bleed Air Heat Exchanger",
                "Heat exchangers cool bleed air before it enters the cabin, preventing excessive temperatures and maintaining comfort.",
                ["bleed_air", "heat_exchanger", "cabin", "temperature"], 1.0
            ),
            SearchDocument(
                39, "Hydraulic Circuit Failures",
                "Multiple hydraulic circuits ensure continued operation of flight controls in case of circuit failure or leaks.",
                ["hydraulic", "circuit", "failure", "flight_controls"], 1.0
            ),
            SearchDocument(
                40, "FADEC Overspeed Protection",
                "FADEC monitors engine speed and provides overspeed protection, shutting down the engine if limits are exceeded.",
                ["FADEC", "overspeed", "engine", "protection"], 1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

def get_search_index() -> SearchIndex:
    if not hasattr(get_search_index, "_instance"):
        get_search_index._instance = SearchIndex()
        get_search_index._instance._preseed_documents()
    return get_search_index._instance