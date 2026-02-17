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
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.tf_idf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9\-]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in set(tokens):
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self.idf_cache.clear()
            self.tf_idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            score += idf * (numerator / (denominator + 1e-10))
        return score * doc.weight

    def _score_tf_idf(self, doc_id: int, query_terms: List[str]) -> float:
        if doc_id in self.tf_idf_cache and all(term in self.tf_idf_cache[doc_id] for term in query_terms):
            return sum(self.tf_idf_cache[doc_id][term] for term in query_terms)
        doc_len = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        tf_idf_score = 0.0
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            tf_norm = tf / (doc_len or 1)
            idf = self._compute_idf(term)
            tf_idf = tf_norm * idf * doc.weight
            self.tf_idf_cache[doc_id][term] = tf_idf
            tf_idf_score += tf_idf
        return tf_idf_score

    def search(self, query: str, limit: int = 10, use_tf_idf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = []
        for doc_id in self.documents:
            if use_tf_idf:
                score = self._score_tf_idf(doc_id, query_terms)
            else:
                score = self._score_bm25(doc_id, query_terms)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            return content[:160] + ("..." if len(content) > 160 else "")
        start = max(indices[0] - 10, 0)
        end = min(indices[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b(' + re.escape(term) + r')\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ("..." if end < len(tokens) else "")

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_documents": self.total_docs,
            "average_document_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
        }

_search_index_singleton: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_singleton
    with _search_index_lock:
        if _search_index_singleton is None:
            _search_index_singleton = SearchIndex()
            _seed_documents(_search_index_singleton)
        return _search_index_singleton

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Hohmann Transfer Orbit Delta-V Calculation",
            "The Hohmann transfer is an efficient method for moving between two circular orbits. Delta-V is calculated using the vis-viva equation. For LEO to GEO, the total delta-V is the sum of the burns at perigee and apogee.",
            ["orbital mechanics", "delta-v", "hohmann transfer"],
            1.0
        ),
        SearchDocument(
            2,
            "Multi-Layer Insulation (MLI) Thermal Performance",
            "MLI is used to minimize heat transfer in spacecraft. Its performance depends on the number of layers, material properties, and vacuum quality. Typical heat flux reduction is 90-99%.",
            ["thermal control", "MLI", "spacecraft insulation"],
            1.0
        ),
        SearchDocument(
            3,
            "Reaction Wheel Momentum Management",
            "Reaction wheels accumulate momentum due to external torques. Momentum unloading is achieved using magnetic torquers or thrusters. Proper management ensures attitude control and prevents wheel saturation.",
            ["attitude control", "reaction wheel", "momentum management"],
            1.0
        ),
        SearchDocument(
            4,
            "Bipropellant Rocket Engine Specific Impulse",
            "Specific impulse (Isp) is a measure of engine efficiency. Bipropellant engines typically use fuel and oxidizer, such as hydrazine and nitrogen tetroxide. Isp values range from 250 to 350 seconds.",
            ["propulsion", "bipropellant", "specific impulse"],
            1.0
        ),
        SearchDocument(
            5,
            "Van Allen Belt Radiation Dose Calculation",
            "Spacecraft traversing the Van Allen belts are exposed to high radiation. Dose calculation considers orbit, shielding, and mission duration. Typical doses are mitigated by aluminum shielding and operational constraints.",
            ["radiation", "Van Allen belt", "dose calculation"],
            1.0
        ),
        SearchDocument(
            6,
            "Hall Thruster Performance and Efficiency",
            "Hall thrusters use electric fields to accelerate ions. Performance metrics include thrust, specific impulse, and efficiency. Typical Isp is 1500-2000 seconds with efficiency up to 60%.",
            ["electric propulsion", "hall thruster", "efficiency"],
            1.0
        ),
        SearchDocument(
            7,
            "Solar Array Power Degradation in LEO",
            "Solar arrays degrade due to atomic oxygen, radiation, and thermal cycling in LEO. Power output decreases by 2-4% per year. Proper material selection and shielding can mitigate degradation.",
            ["solar array", "LEO", "power degradation"],
            1.0
        ),
        SearchDocument(
            8,
            "Geostationary Orbit Station-Keeping Delta-V Budget",
            "Station-keeping in GEO requires regular delta-V to counteract gravitational perturbations and solar radiation pressure. Annual delta-V budget is typically 50-70 m/s.",
            ["GEO", "station-keeping", "delta-v budget"],
            1.0
        ),
        SearchDocument(
            9,
            "Thermal Radiator Sizing for Heat Rejection",
            "Thermal radiators reject excess heat from spacecraft systems. Sizing depends on heat load, radiator emissivity, and environmental temperature. Stefan-Boltzmann law is used for calculations.",
            ["thermal control", "radiator", "heat rejection"],
            1.0
        ),
        SearchDocument(
            10,
            "Star Tracker Accuracy and Noise Sources",
            "Star trackers provide precise attitude determination. Accuracy is affected by sensor noise, optical aberrations, and stray light. Typical accuracy is 1-10 arcseconds.",
            ["attitude determination", "star tracker", "accuracy"],
            1.0
        ),
        SearchDocument(
            11,
            "Launch Vehicle Fairing Acoustic Environment",
            "During launch, payloads are subjected to intense acoustic loads inside the fairing. Sound pressure levels can exceed 140 dB. Acoustic mitigation includes damping materials and isolation mounts.",
            ["launch vehicle", "fairing", "acoustics"],
            1.0
        ),
        SearchDocument(
            12,
            "S-Band Communication Link Budget",
            "S-band is commonly used for spacecraft communications. Link budget analysis includes transmitter power, antenna gain, path loss, and receiver sensitivity. Typical data rates are 1-10 Mbps.",
            ["communications", "S-band", "link budget"],
            1.0
        ),
        SearchDocument(
            13,
            "Tsiolkovsky Rocket Equation and Mass Ratio",
            "The rocket equation relates delta-V, exhaust velocity, and mass ratio. Delta-V = Ve * ln(m0/mf). Efficient staging and propellant selection maximize mass ratio.",
            ["rocket equation", "delta-v", "mass ratio"],
            1.0
        ),
        SearchDocument(
            14,
            "Spacecraft Bus Structural Design for Launch Loads",
            "Structural design must withstand launch loads including vibration, shock, and acceleration. Finite element analysis is used to verify strength and stiffness. Materials include aluminum and composites.",
            ["structural design", "launch loads", "spacecraft bus"],
            1.0
        ),
        SearchDocument(
            15,
            "Constellation Design for Global Coverage",
            "Satellite constellations provide global coverage by optimizing orbital planes and phasing. Parameters include altitude, inclination, and number of satellites. Examples include Iridium and Starlink.",
            ["constellation", "global coverage", "orbital design"],
            1.0
        ),
        SearchDocument(
            16,
            "Technology Readiness Level (TRL) Assessment",
            "TRL is a metric for assessing technology maturity. Levels range from 1 (basic principles) to 9 (flight proven). NASA and ESA use TRL for project management.",
            ["TRL", "technology assessment", "space systems"],
            1.0
        ),
        SearchDocument(
            17,
            "Solar Sail Propulsion and Characteristic Acceleration",
            "Solar sails use photon pressure for propulsion. Characteristic acceleration depends on sail area, mass, and reflectivity. Typical values are 0.1-1 mm/s^2.",
            ["solar sail", "propulsion", "characteristic acceleration"],
            1.0
        ),
        SearchDocument(
            18,
            "Satellite Drag and Orbital Decay in LEO",
            "Atmospheric drag causes orbital decay in LEO. Drag force depends on altitude, cross-sectional area, and atmospheric density. Satellites require periodic reboost.",
            ["LEO", "drag", "orbital decay"],
            1.0
        ),
        SearchDocument(
            19,
            "Cryogenic Propellant Boiloff and Storage",
            "Cryogenic propellants like liquid hydrogen and oxygen boil off due to heat leaks. Storage solutions include MLI, vapor cooling, and active refrigeration. Boiloff rates impact mission duration.",
            ["cryogenic", "propellant", "boiloff", "storage"],
            1.0
        ),
        SearchDocument(
            20,
            "Gravity Assist Trajectory Design",
            "Gravity assist maneuvers use planetary flybys to change spacecraft velocity and trajectory. Design involves timing, approach angle, and target planet. Used in missions like Voyager and Cassini.",
            ["trajectory", "gravity assist", "planetary flyby"],
            1.0
        ),
        SearchDocument(
            21,
            "Micrometeoroid and Orbital Debris (MMOD) Shielding",
            "MMOD shielding protects spacecraft from impacts. Designs include Whipple shields and multi-layer barriers. Shielding effectiveness is tested with hypervelocity impact experiments.",
            ["MMOD", "shielding", "orbital debris"],
            1.0
        ),
        SearchDocument(
            22,
            "Nuclear Thermal Propulsion (NTP) Specific Impulse",
            "NTP engines use nuclear reactors to heat propellant. Specific impulse is 800-900 seconds, much higher than chemical engines. Challenges include reactor safety and radiation shielding.",
            ["nuclear propulsion", "NTP", "specific impulse"],
            1.0
        ),
        SearchDocument(
            23,
            "Pointing Stability and Jitter Requirements",
            "Spacecraft pointing stability is critical for imaging and communications. Jitter sources include reaction wheels, thrusters, and structural vibrations. Requirements are specified in arcseconds or microradians.",
            ["pointing stability", "jitter", "requirements"],
            1.0
        ),
        SearchDocument(
            24,
            "Spacecraft Bus Thermal Control Systems",
            "Thermal control systems include radiators, heaters, and MLI. Active and passive methods maintain component temperatures within limits. Design is driven by power dissipation and environmental conditions.",
            ["thermal control", "spacecraft bus", "temperature"],
            1.0
        ),
        SearchDocument(
            25,
            "Spacecraft Power System Sizing",
            "Power system sizing considers peak and average loads, solar array degradation, and battery capacity. Margin is added for contingencies. Typical sizing methods use worst-case scenarios.",
            ["power system", "sizing", "spacecraft"],
            1.0
        ),
        SearchDocument(
            26,
            "LEO Radiation Environment and Shielding",
            "LEO radiation includes trapped particles, cosmic rays, and solar events. Shielding effectiveness depends on material thickness and density. Aluminum is commonly used for protection.",
            ["LEO", "radiation", "shielding"],
            1.0
        ),
        SearchDocument(
            27,
            "Spacecraft Attitude Determination Sensors",
            "Attitude sensors include star trackers, sun sensors, gyroscopes, and magnetometers. Sensor fusion improves accuracy and reliability. Calibration is critical for performance.",
            ["attitude determination", "sensors", "spacecraft"],
            1.0
        ),
        SearchDocument(
            28,
            "Spacecraft Propulsion System Selection",
            "Propulsion selection depends on mission requirements, delta-V, and available technologies. Options include chemical, electric, and nuclear propulsion. Trade studies evaluate performance and cost.",
            ["propulsion", "system selection", "spacecraft"],
            1.0
        ),
        SearchDocument(
            29,
            "Orbital Maneuver Planning and Optimization",
            "Orbital maneuvers are planned to minimize delta-V and maximize mission objectives. Optimization techniques include Lambert's problem and numerical simulations.",
            ["orbital mechanics", "maneuver", "optimization"],
            1.0
        ),
        SearchDocument(
            30,
            "Spacecraft Communication Antenna Design",
            "Antenna design considers frequency, gain, beamwidth, and polarization. S-band and X-band are common for spacecraft. Deployable antennas maximize coverage and minimize stowage volume.",
            ["communications", "antenna", "spacecraft"],
            1.0
        ),
        SearchDocument(
            31,
            "Spacecraft Launch Mass Budgeting",
            "Launch mass budgeting includes dry mass, propellant, payload, and margin. Accurate budgeting ensures compatibility with launch vehicle performance.",
            ["mass budgeting", "launch", "spacecraft"],
            1.0
        ),
        SearchDocument(
            32,
            "Spacecraft Structural Materials Selection",
            "Material selection balances strength, weight, thermal properties, and cost. Common materials are aluminum alloys, titanium, and composites.",
            ["structural materials", "spacecraft", "selection"],
            1.0
        ),
        SearchDocument(
            33,
            "Spacecraft Orbit Determination Algorithms",
            "Orbit determination uses tracking data and estimation algorithms. Methods include least squares and Kalman filtering. Accurate orbit knowledge is essential for mission operations.",
            ["orbit determination", "algorithms", "spacecraft"],
            1.0
        ),
        SearchDocument(
            34,
            "Spacecraft Thermal Analysis Tools",
            "Thermal analysis tools simulate heat flow and temperature distribution. Software includes SINDA, Thermal Desktop, and ESATAN. Analysis supports design and verification.",
            ["thermal analysis", "tools", "spacecraft"],
            1.0
        ),
        SearchDocument(
            35,
            "Spacecraft Power Distribution Architecture",
            "Power distribution architecture includes primary and secondary buses, protection devices, and load management. Reliability and redundancy are key design drivers.",
            ["power distribution", "architecture", "spacecraft"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)