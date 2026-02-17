import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
        self.doc_tokens: Dict[int, List[str]] = {}
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.doc_id_counter: int = 1
        self.lock = threading.Lock()
        self._dirty = True
        self._idf_cache: Dict[str, float] = {}

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self.lock:
            doc_id = self.doc_id_counter
            self.doc_id_counter += 1
            doc = SearchDocument(doc_id, title, content, tags, weight)
            tokens = self._tokenize(title + " " + content + " " + " ".join(tags))
            self.documents[doc_id] = doc
            self.doc_tokens[doc_id] = tokens
            self.term_freqs[doc_id] = Counter(tokens)
            self.doc_lengths[doc_id] = len(tokens)
            for token in set(tokens):
                self.inverted_index[token].add(doc_id)
            self.N = len(self.documents)
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._dirty = True
            return doc_id

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        candidate_doc_ids = set()
        for token in query_tokens:
            candidate_doc_ids.update(self.inverted_index.get(token, set()))
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_doc_ids:
            score = self._score_bm25(doc_id, query_tokens)
            scored_results.append((doc_id, score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "document_count": self.N,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if self._dirty or term not in self._idf_cache:
            df = len(self.inverted_index.get(term, []))
            if df == 0:
                idf = 0.0
            else:
                idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
            self._idf_cache[term] = idf
        return self._idf_cache[term]

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = self.term_freqs[doc_id]
        score = 0.0
        for term in query_tokens:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            score += idf * numerator / denominator
        return score * doc.weight

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:160]
            return snippet + "..." if len(content) > 160 else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + "..." if end < len(tokens) else snippet

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_tokens:
            tf_norm = tf.get(term, 0) / (doc_len or 1)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

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
        {
            "title": "MacPherson Strut Geometry Fundamentals",
            "content": "The MacPherson strut is a type of automotive suspension system that uses a simple geometry. It consists of a strut assembly that combines the shock absorber and coil spring into a single unit. Key parameters include camber gain, kingpin inclination, and scrub radius.",
            "tags": ["macpherson_strut_geometry", "camber", "kingpin_inclination"],
            "weight": 1.2
        },
        {
            "title": "Double Wishbone Suspension: Geometry and Kinematics",
            "content": "Double wishbone suspensions use two arms to control wheel motion. This allows for precise control of camber, caster, and toe throughout suspension travel. The upper and lower control arms can be tuned for optimal handling and tire contact.",
            "tags": ["double_wishbone_geometry", "camber", "caster", "toe"],
            "weight": 1.1
        },
        {
            "title": "Spring Rate Calculation Methods",
            "content": "Spring rate is a critical parameter in suspension design. It is calculated as the force required to compress the spring by a unit distance. The formula is k = F/Δx, where k is the spring rate, F is force, and Δx is displacement.",
            "tags": ["spring_rate_calculation", "coil_spring", "suspension_design"],
            "weight": 1.0
        },
        {
            "title": "Damper Valving: Compression and Rebound Tuning",
            "content": "Dampers control the oscillation of the suspension by providing resistance during compression and rebound. Compression valving affects how the damper absorbs energy when the wheel moves up, while rebound valving controls the return motion.",
            "tags": ["damper_valving_compression_rebound", "damping", "suspension"],
            "weight": 1.0
        },
        {
            "title": "Anti-Roll Bar Sizing and Effects",
            "content": "Anti-roll bars, also known as sway bars, reduce body roll during cornering. The stiffness of the bar is determined by its diameter, material, and length. Proper sizing balances understeer and oversteer characteristics.",
            "tags": ["anti_roll_bar_sizing", "sway_bar", "cornering"],
            "weight": 1.0
        },
        {
            "title": "Wheel Alignment Parameters Explained",
            "content": "Wheel alignment includes camber, caster, and toe. Proper alignment ensures optimal tire contact, handling, and tire wear. Adjustments are made using control arms, tie rods, and strut mounts.",
            "tags": ["wheel_alignment_parameters", "camber", "caster", "toe"],
            "weight": 1.0
        },
        {
            "title": "Magnetorheological (Magneride) Active Dampers",
            "content": "Magnetorheological dampers use a fluid whose viscosity changes with an applied magnetic field. This allows real-time adjustment of damping force, improving ride comfort and handling.",
            "tags": ["magenride_active_damper", "active_suspension", "magnetorheological"],
            "weight": 1.2
        },
        {
            "title": "Bump Steer Kinematics in Suspension Design",
            "content": "Bump steer refers to the change in toe angle as the suspension moves through its travel. It is influenced by the geometry of steering and suspension linkages. Minimizing bump steer improves vehicle stability.",
            "tags": ["bump_steer_kinematics", "toe", "steering"],
            "weight": 1.0
        },
        {
            "title": "Multi-Link Rear Suspension Overview",
            "content": "Multi-link suspensions use three or more arms to control wheel motion. This design allows for independent adjustment of camber, toe, and anti-squat characteristics, providing excellent handling and ride comfort.",
            "tags": ["multi_link_rear_suspension", "camber", "toe", "anti_squat"],
            "weight": 1.1
        },
        {
            "title": "Suspension NVH (Noise, Vibration, Harshness) Control",
            "content": "NVH control in suspension systems involves isolating the vehicle body from road irregularities. Techniques include using compliant bushings, tuned mass dampers, and subframe isolation.",
            "tags": ["suspension_nvh_control", "nvh", "bushings"],
            "weight": 1.0
        },
        {
            "title": "Active Suspension: Adaptive Body Control (ABC)",
            "content": "Active suspension systems like ABC use hydraulic actuators and sensors to adjust suspension characteristics in real time. This provides superior ride quality and handling by minimizing body roll and pitch.",
            "tags": ["active_suspension_abc", "adaptive_suspension", "hydraulic"],
            "weight": 1.2
        },
        {
            "title": "Understeer and Oversteer Gradient Analysis",
            "content": "The understeer gradient quantifies how a vehicle responds to steering input. Positive gradient indicates understeer, while negative indicates oversteer. It is influenced by suspension geometry, tire characteristics, and weight distribution.",
            "tags": ["understeer_oversteer_gradient", "handling", "tire"],
            "weight": 1.0
        },
        {
            "title": "Suspension Testing: K&C Rig Procedures",
            "content": "Kinematics and Compliance (K&C) rigs are used to measure suspension parameters such as camber gain, toe change, and compliance steer under controlled loads. Data from K&C testing informs suspension tuning.",
            "tags": ["suspension_testing_kc_rig", "kinematics", "compliance"],
            "weight": 1.1
        },
        {
            "title": "Coilover Suspension Design Principles",
            "content": "Coilovers combine a coil spring and damper into a single adjustable unit. They allow for fine-tuning of ride height, spring rate, and damping, making them popular in motorsports and performance vehicles.",
            "tags": ["coilover_suspension_design", "coilover", "adjustable"],
            "weight": 1.1
        },
        {
            "title": "Air Suspension Systems: Components and Operation",
            "content": "Air suspension replaces coil springs with air springs, allowing ride height adjustment and load leveling. Key components include air bags, compressors, and height sensors.",
            "tags": ["air_suspension_systems", "air_spring", "compressor"],
            "weight": 1.0
        },
        {
            "title": "Solid Axle Suspension Characteristics",
            "content": "Solid axle suspensions use a single rigid axle connecting both wheels. They are robust and simple, commonly used in trucks and off-road vehicles. Drawbacks include limited wheel independence.",
            "tags": ["solid_axle_suspension", "rigid_axle", "offroad"],
            "weight": 1.0
        },
        {
            "title": "Tire Vertical Stiffness and Its Effects",
            "content": "Tire vertical stiffness affects ride comfort and handling. It is determined by the tire's construction and inflation pressure. Higher stiffness improves response but can increase harshness.",
            "tags": ["tire_vertical_stiffness", "tire", "stiffness"],
            "weight": 1.0
        },
        {
            "title": "Unsprung Mass Effects in Suspension Systems",
            "content": "Unsprung mass includes all components not supported by the springs, such as wheels, brakes, and a portion of the suspension. Lower unsprung mass improves ride and handling.",
            "tags": ["unsprung_mass_effects", "unsprung_mass", "handling"],
            "weight": 1.0
        },
        {
            "title": "Suspension Geometry: Roll Center Analysis",
            "content": "Roll center is the point around which the vehicle body rolls during cornering. Its height is determined by the suspension geometry and affects handling balance.",
            "tags": ["macpherson_strut_geometry", "double_wishbone_geometry", "roll_center"],
            "weight": 1.1
        },
        {
            "title": "Camber Gain in Suspension Travel",
            "content": "Camber gain refers to the change in camber angle as the suspension compresses or extends. Proper camber gain helps maintain tire contact during cornering.",
            "tags": ["macpherson_strut_geometry", "double_wishbone_geometry", "camber_gain"],
            "weight": 1.0
        },
        {
            "title": "Suspension Bushings: Types and Materials",
            "content": "Bushings isolate vibration and noise between suspension components and the vehicle body. Common materials include rubber, polyurethane, and spherical bearings.",
            "tags": ["suspension_nvh_control", "bushings", "materials"],
            "weight": 1.0
        },
        {
            "title": "Toe and Ackermann Steering Geometry",
            "content": "Ackermann geometry ensures that wheels turn at appropriate angles during cornering. Toe settings influence straight-line stability and tire wear.",
            "tags": ["wheel_alignment_parameters", "bump_steer_kinematics", "ackermann"],
            "weight": 1.0
        },
        {
            "title": "Anti-Squat and Anti-Dive Suspension Design",
            "content": "Anti-squat and anti-dive refer to suspension geometry that resists squat under acceleration and dive under braking. Achieved by adjusting control arm angles and mounting points.",
            "tags": ["multi_link_rear_suspension", "double_wishbone_geometry", "anti_squat", "anti_dive"],
            "weight": 1.0
        },
        {
            "title": "Suspension Subframes and Isolation",
            "content": "Subframes support suspension components and isolate road noise and vibration from the passenger compartment. Proper isolation improves NVH performance.",
            "tags": ["suspension_nvh_control", "subframe", "isolation"],
            "weight": 1.0
        },
        {
            "title": "Hydraulic vs. Pneumatic Suspension Systems",
            "content": "Hydraulic suspensions use fluid pressure for actuation, while pneumatic systems use compressed air. Each has advantages in ride quality, adjustability, and complexity.",
            "tags": ["active_suspension_abc", "air_suspension_systems", "hydraulic", "pneumatic"],
            "weight": 1.0
        },
        {
            "title": "Suspension Travel and Bump Stops",
            "content": "Bump stops limit suspension travel to prevent damage. Proper sizing ensures smooth operation and protects components during extreme compression.",
            "tags": ["macpherson_strut_geometry", "bump_stop", "suspension_travel"],
            "weight": 1.0
        },
        {
            "title": "Cornering Forces and Suspension Tuning",
            "content": "Suspension tuning balances cornering forces by adjusting spring rates, anti-roll bars, and alignment. Proper tuning maximizes grip and stability.",
            "tags": ["spring_rate_calculation", "anti_roll_bar_sizing", "cornering"],
            "weight": 1.0
        },
        {
            "title": "Suspension Kinematics: Instant Center",
            "content": "The instant center is the point about which a suspension arm rotates at any instant. Its location affects roll center height and camber gain.",
            "tags": ["double_wishbone_geometry", "multi_link_rear_suspension", "instant_center"],
            "weight": 1.0
        },
        {
            "title": "Ride Height Adjustment Techniques",
            "content": "Ride height can be adjusted using coilovers, air suspension, or adjustable spring perches. Proper ride height is crucial for handling and tire wear.",
            "tags": ["coilover_suspension_design", "air_suspension_systems", "ride_height"],
            "weight": 1.0
        },
        {
            "title": "Suspension Compliance and Steering Feel",
            "content": "Compliance in suspension bushings and joints affects steering feel and response. Excessive compliance can lead to vague handling.",
            "tags": ["suspension_testing_kc_rig", "suspension_nvh_control", "compliance"],
            "weight": 1.0
        },
        {
            "title": "Progressive vs. Linear Spring Rates",
            "content": "Progressive springs increase in stiffness as they compress, while linear springs have constant rate. Choice affects ride comfort and handling.",
            "tags": ["spring_rate_calculation", "coilover_suspension_design", "progressive_spring"],
            "weight": 1.0
        },
        {
            "title": "Electronic Damping Control Systems",
            "content": "Electronic damping systems adjust damper force via solenoids or valves in response to sensors. This enables adaptive ride and handling.",
            "tags": ["magenride_active_damper", "active_suspension_abc", "electronic_damping"],
            "weight": 1.1
        }
    ]
    for doc in docs:
        index.add_document(doc["title"], doc["content"], doc["tags"], doc["weight"])