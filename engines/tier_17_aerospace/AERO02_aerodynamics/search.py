import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores: Dict[int, float] = defaultdict(float)
        for term in set(query_terms):
            idf = self._compute_idf(term)
            for doc_id, tf in self.term_freqs.items():
                if term in tf:
                    score = self._score_bm25(term, doc_id, idf)
                    doc_scores[doc_id] += score
        # TF-IDF fallback for zero BM25 matches
        if not doc_scores:
            for doc_id, tf in self.term_freqs.items():
                tfidf_score = 0.0
                for term in set(query_terms):
                    tf_val = tf[term]
                    idf = self._compute_idf(term)
                    norm_tf = tf_val / (self.doc_lengths[doc_id] + 1)
                    tfidf_score += norm_tf * idf
                if tfidf_score > 0:
                    doc_scores[doc_id] = tfidf_score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score * doc.weight, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.doc_freqs)
        }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9\-]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: int, idf: Optional[float] = None) -> float:
        tf = self.term_freqs[doc_id][term]
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        k1 = self.bm25_k1
        b = self.bm25_b
        if idf is None:
            idf = self._compute_idf(term)
        denom = tf + k1 * (1 - b + b * doc_len / avg_dl)
        score = idf * ((tf * (k1 + 1)) / (denom + 1e-10))
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ('...' if end < len(tokens) else '')

# --- Singleton Factory ---

_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seeded Documents ---

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Bernoulli vs Circulation Theory of Lift",
            "Bernoulli's principle explains lift as a result of pressure differences due to airflow speed. Circulation theory, based on the Kutta-Joukowski theorem, attributes lift to the circulation of air around the airfoil. Both theories describe the same phenomenon from different perspectives.",
            ["lift", "bernoulli", "circulation", "theory"]
        ),
        SearchDocument(
            2,
            "Drag Decomposition: Parasitic, Induced, Wave",
            "Total drag on an aircraft is the sum of parasitic drag (form, skin friction, interference), induced drag (from lift generation), and wave drag (due to compressibility effects at high speeds). Each component varies with speed and configuration.",
            ["drag", "parasitic", "induced", "wave"]
        ),
        SearchDocument(
            3,
            "NACA Airfoil Designation and Characteristics",
            "NACA airfoils are designated by a series of numbers indicating camber, thickness, and other properties. For example, a NACA 2412 airfoil has 2% camber at 40% chord and 12% thickness. These designations help engineers select appropriate airfoils for performance requirements.",
            ["naca", "airfoil", "designation", "characteristics"]
        ),
        SearchDocument(
            4,
            "Boundary Layer Transition and Turbulence",
            "The boundary layer transitions from laminar to turbulent flow depending on Reynolds number, surface roughness, and pressure gradients. Turbulent boundary layers are thicker and have higher skin friction but are more resistant to separation.",
            ["boundary layer", "transition", "turbulence"]
        ),
        SearchDocument(
            5,
            "Stall Characteristics: Leading Edge vs Trailing Edge",
            "Stall can initiate at the leading edge or trailing edge of an airfoil. Leading edge stall is abrupt and can cause loss of control, while trailing edge stall is more gradual. Airfoil shape and angle of attack influence stall behavior.",
            ["stall", "leading edge", "trailing edge", "characteristics"]
        ),
        SearchDocument(
            6,
            "High-Lift Devices: Slats, Flaps, Krueger Flaps",
            "High-lift devices such as slats, flaps, and Krueger flaps increase the maximum lift coefficient by modifying the wing's camber and delaying stall. They are deployed during takeoff and landing to reduce required speeds.",
            ["high-lift", "slats", "flaps", "krueger"]
        ),
        SearchDocument(
            7,
            "Wing Planform Design: Aspect Ratio, Sweep, Taper",
            "Wing planform parameters include aspect ratio (span squared over area), sweep angle, and taper ratio. High aspect ratio reduces induced drag, sweep delays compressibility effects, and taper optimizes lift distribution.",
            ["wing", "planform", "aspect ratio", "sweep", "taper"]
        ),
        SearchDocument(
            8,
            "Compressibility Effects and Critical Mach Number",
            "As aircraft approach the speed of sound, compressibility effects become significant. The critical Mach number is the lowest Mach at which local airflow reaches Mach 1, leading to shock formation and increased drag.",
            ["compressibility", "critical mach", "mach number"]
        ),
        SearchDocument(
            9,
            "Supersonic Aerodynamics: Shocks, Expansion Fans, Wave Drag",
            "Supersonic flight involves shock waves, expansion fans, and significant wave drag. Shock waves cause abrupt changes in pressure and temperature, while expansion fans allow smooth turning of supersonic flows.",
            ["supersonic", "shocks", "expansion fans", "wave drag"]
        ),
        SearchDocument(
            10,
            "Longitudinal Stability: Static Margin and Neutral Point",
            "Longitudinal static stability depends on the position of the center of gravity relative to the neutral point. The static margin is the distance between these points, with a positive margin indicating stability.",
            ["longitudinal stability", "static margin", "neutral point"]
        ),
        SearchDocument(
            11,
            "Aircraft Performance: Breguet Range Equation",
            "The Breguet range equation relates the range of an aircraft to its lift-to-drag ratio, fuel consumption, and initial/final weight. It is fundamental for estimating the endurance and range of powered aircraft.",
            ["performance", "breguet", "range", "equation"]
        ),
        SearchDocument(
            12,
            "V-Speeds: Vs, Vmc, Vr, V1, Vx, Vy, Vne",
            "V-speeds are standardized airspeeds for safe operation: Vs (stall), Vmc (minimum control), Vr (rotation), V1 (decision), Vx (best angle climb), Vy (best rate climb), Vne (never exceed). Each has specific operational significance.",
            ["v-speeds", "vs", "vmc", "vr", "v1", "vx", "vy", "vne"]
        ),
        SearchDocument(
            13,
            "Propeller Aerodynamics: Blade Element Theory",
            "Blade element theory divides the propeller into small elements to analyze lift and drag forces. Each element is treated as a small airfoil, and the total thrust and torque are obtained by integrating along the blade.",
            ["propeller", "blade element", "theory", "aerodynamics"]
        ),
        SearchDocument(
            14,
            "Rotary Wing Aerodynamics: Momentum Theory and Blade Flapping",
            "Rotary wing aerodynamics involves momentum theory, which models the rotor as an actuator disk, and blade flapping, which compensates for dissymmetry of lift in forward flight.",
            ["rotary wing", "momentum theory", "blade flapping"]
        ),
        SearchDocument(
            15,
            "Wind Tunnel Testing: Scaling, Reynolds Number Effects",
            "Wind tunnel models are scaled to match Reynolds number and Mach number effects. Reynolds number similarity ensures that boundary layer behavior and separation are representative of full-scale conditions.",
            ["wind tunnel", "scaling", "reynolds number"]
        ),
        SearchDocument(
            16,
            "Ground Effect: Reduced Induced Drag, Increased Lift",
            "Ground effect occurs when an aircraft flies close to the ground, reducing induced drag and increasing lift due to altered airflow patterns around the wing and reduced wingtip vortices.",
            ["ground effect", "induced drag", "lift"]
        ),
        SearchDocument(
            17,
            "Atmospheric Effects: Density Altitude, Wind Shear, Icing",
            "Atmospheric conditions such as density altitude, wind shear, and icing affect aircraft performance and safety. High density altitude reduces engine and aerodynamic performance, while icing alters airfoil shape and increases drag.",
            ["atmospheric", "density altitude", "wind shear", "icing"]
        ),
        SearchDocument(
            18,
            "Induced Drag and Lift Distribution",
            "Induced drag arises from the generation of lift and is minimized by an elliptical lift distribution. High aspect ratio wings and winglets help reduce induced drag.",
            ["induced drag", "lift distribution", "aspect ratio"]
        ),
        SearchDocument(
            19,
            "Wave Drag at Transonic and Supersonic Speeds",
            "Wave drag increases sharply near and above the speed of sound due to shock wave formation. Area ruling and swept wings are used to mitigate wave drag in high-speed aircraft.",
            ["wave drag", "transonic", "supersonic", "area rule"]
        ),
        SearchDocument(
            20,
            "Boundary Layer Control Techniques",
            "Boundary layer control methods include suction, blowing, and vortex generators. These techniques delay separation, reduce drag, and improve lift by managing the behavior of the boundary layer.",
            ["boundary layer", "control", "separation", "drag"]
        ),
        SearchDocument(
            21,
            "Airfoil Stall: Effects of Reynolds Number",
            "The Reynolds number affects the stall characteristics of airfoils. At low Reynolds numbers, stall occurs at lower angles of attack and is more gradual, while at high Reynolds numbers, stall is more abrupt.",
            ["stall", "reynolds number", "airfoil"]
        ),
        SearchDocument(
            22,
            "Leading Edge Devices: Slats and Krueger Flaps",
            "Leading edge devices such as slats and Krueger flaps delay stall by increasing the maximum lift coefficient and allowing higher angles of attack before separation.",
            ["leading edge", "slats", "krueger", "stall"]
        ),
        SearchDocument(
            23,
            "Trailing Edge Devices: Plain, Split, Fowler, and Slotted Flaps",
            "Trailing edge flaps come in various types: plain, split, Fowler, and slotted. Each type increases lift and modifies the wing's camber, with slotted flaps providing the greatest lift increase.",
            ["trailing edge", "flaps", "plain", "split", "fowler", "slotted"]
        ),
        SearchDocument(
            24,
            "Sweep Angle and Critical Mach Number",
            "Swept wings increase the critical Mach number by reducing the component of airflow perpendicular to the leading edge, delaying the onset of compressibility effects and shock formation.",
            ["sweep", "critical mach", "compressibility"]
        ),
        SearchDocument(
            25,
            "Neutral Point and Aircraft Stability",
            "The neutral point is the aerodynamic center of the aircraft. Stability requires the center of gravity to be ahead of the neutral point, ensuring a positive static margin.",
            ["neutral point", "stability", "static margin"]
        ),
        SearchDocument(
            26,
            "Breguet Endurance Equation",
            "The Breguet endurance equation estimates how long an aircraft can stay aloft based on fuel consumption, lift-to-drag ratio, and engine efficiency.",
            ["breguet", "endurance", "equation"]
        ),
        SearchDocument(
            27,
            "Vmc: Minimum Control Speed",
            "Vmc is the minimum speed at which the aircraft can be controlled with one engine inoperative. It is critical for multi-engine aircraft safety during takeoff and climb.",
            ["vmc", "minimum control", "v-speeds"]
        ),
        SearchDocument(
            28,
            "Blade Flapping in Helicopters",
            "Blade flapping allows helicopter rotors to compensate for dissymmetry of lift in forward flight, maintaining balanced lift across the rotor disk.",
            ["blade flapping", "helicopter", "rotary wing"]
        ),
        SearchDocument(
            29,
            "Wind Tunnel Corrections: Wall and Blockage Effects",
            "Wind tunnel results are corrected for wall interference and blockage effects to ensure accurate scaling to real-world conditions.",
            ["wind tunnel", "corrections", "blockage", "wall effects"]
        ),
        SearchDocument(
            30,
            "Ground Effect on Takeoff and Landing",
            "During takeoff and landing, ground effect reduces induced drag and increases lift, allowing aircraft to become airborne at lower speeds.",
            ["ground effect", "takeoff", "landing"]
        ),
        SearchDocument(
            31,
            "Icing Effects on Airfoil Performance",
            "Icing alters the shape of airfoils, increasing drag and reducing lift. It can lead to premature stall and loss of control if not managed.",
            ["icing", "airfoil", "performance"]
        ),
        SearchDocument(
            32,
            "Mach Number and Compressibility",
            "Mach number is the ratio of aircraft speed to the speed of sound. Compressibility effects become important as Mach number increases, leading to changes in lift, drag, and stability.",
            ["mach number", "compressibility", "lift", "drag"]
        ),
        SearchDocument(
            33,
            "Aspect Ratio and Induced Drag",
            "A high aspect ratio wing reduces induced drag by spreading lift over a greater span, improving aerodynamic efficiency especially at low speeds.",
            ["aspect ratio", "induced drag", "wing"]
        ),
        SearchDocument(
            34,
            "Stall Warning and Prevention Systems",
            "Modern aircraft employ stall warning and prevention systems, such as stick shakers and angle of attack indicators, to alert pilots and prevent unintentional stalls.",
            ["stall", "warning", "prevention", "systems"]
        ),
        SearchDocument(
            35,
            "Expansion Fans in Supersonic Flow",
            "Expansion fans are regions where supersonic flow turns smoothly, resulting in a decrease in pressure and temperature. They are essential in nozzle and wing design for supersonic aircraft.",
            ["expansion fans", "supersonic", "nozzle"]
        ),
    ]
    for doc in docs:
        index.add_document(doc)