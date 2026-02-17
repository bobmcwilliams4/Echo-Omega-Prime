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
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            doc_scores[doc_id] = combined_score * doc.weight
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_len = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs.get(doc_id, Counter())
        for term in query_terms:
            f = tf.get(term, 0)
            idf = self._compute_idf(term)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_len / avg_len)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vec = self._tfidf_cache[doc_id]
        else:
            tfidf_vec = {}
            tf = self.term_freqs.get(doc_id, Counter())
            doc_len = self.doc_lengths.get(doc_id, 1)
            for term, freq in tf.items():
                tf_norm = freq / doc_len
                idf = self._compute_idf(term)
                tfidf_vec[term] = tf_norm * idf
            self._tfidf_cache[doc_id] = tfidf_vec
        score = 0.0
        for term in query_terms:
            score += tfidf_vec.get(term, 0.0)
        return score

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:30]) + ('...' if len(tokens) > 30 else '')
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ('...' if end < len(tokens) else '')

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
            1,
            "Prime Mover Overhaul Cycles",
            "Locomotive prime movers require overhaul every 8 years or 1,000,000 miles, whichever comes first. Overhaul includes cylinder inspection, piston replacement, and turbocharger evaluation. Maintenance records must be kept for regulatory compliance.",
            ["prime-mover", "overhaul", "maintenance", "regulatory"],
            1.0
        ),
        SearchDocument(
            2,
            "Wheel Impact Load Detector (WILD) Response",
            "WILD systems detect excessive wheel impacts. Immediate inspection is required if impact exceeds 90 kips. Wheels with defects such as spalling, shelling, or flat spots must be replaced according to AAR condemning limits.",
            ["wild", "wheel", "impact", "inspection", "aar"],
            1.0
        ),
        SearchDocument(
            3,
            "Wheel Condemning Limits",
            "Freight car wheels are condemned if flange thickness exceeds 1 1/2 inches, or if tread wear is greater than 1 inch. Wheels with cracks, broken flanges, or severe shelling must be removed from service.",
            ["wheel", "condemning", "limits", "inspection"],
            1.0
        ),
        SearchDocument(
            4,
            "Air Brake Testing Requirements",
            "Class I, IA, and III freight car inspections require air brake testing. Brake pipe leakage must not exceed 3 psi per minute. All brake valves, hoses, and reservoirs must be examined for leaks and proper operation.",
            ["air-brake", "testing", "inspection", "freight-car"],
            1.0
        ),
        SearchDocument(
            5,
            "Journal Bearing Hot Box Detection",
            "Hot box detectors monitor journal bearing temperatures. Bearings exceeding 200°F trigger alarms. Immediate removal and inspection is required to prevent catastrophic failure and derailment.",
            ["journal-bearing", "hot-box", "detection", "failure"],
            1.0
        ),
        SearchDocument(
            6,
            "Journal Bearing Failure Prevention",
            "Routine lubrication and periodic inspection prevent journal bearing failures. Signs of overheating, discoloration, or excessive wear indicate imminent failure and require bearing replacement.",
            ["journal-bearing", "failure", "prevention", "maintenance"],
            1.0
        ),
        SearchDocument(
            7,
            "Coupler Knuckle Inspection Criteria",
            "Coupler knuckles must be inspected for cracks, excessive wear, and proper fit. Replacement is mandatory if wear exceeds 1/4 inch or if cracks are detected. Securement pins must be checked for integrity.",
            ["coupler", "knuckle", "inspection", "replacement"],
            1.0
        ),
        SearchDocument(
            8,
            "Tank Car Qualification: DOT-111 vs DOT-117",
            "DOT-117 tank cars feature enhanced safety with thicker shells, head shields, and improved valve protection compared to DOT-111. Qualification requires periodic inspection, hydrostatic testing, and compliance with PHMSA standards.",
            ["tank-car", "dot-111", "dot-117", "qualification", "phmsa"],
            1.0
        ),
        SearchDocument(
            9,
            "Traction Motor Inspection",
            "Traction motors must be inspected for brush wear, commutator condition, and insulation integrity. Excessive vibration or abnormal noise indicates potential failure. Commutator maintenance includes cleaning and undercutting.",
            ["traction-motor", "inspection", "commutator", "maintenance"],
            1.0
        ),
        SearchDocument(
            10,
            "Condition-Based Maintenance: Vibration Analysis",
            "Vibration analysis is used to detect bearing defects, misalignment, and imbalance in locomotive components. Condition-based maintenance reduces unscheduled downtime and extends asset life.",
            ["condition-based", "maintenance", "vibration", "analysis"],
            1.0
        ),
        SearchDocument(
            11,
            "Oil Sampling for Locomotive Maintenance",
            "Periodic oil sampling detects contaminants, wear metals, and degradation in locomotive engines. Results guide maintenance actions such as filter replacement or overhaul scheduling.",
            ["oil-sampling", "locomotive", "maintenance", "engine"],
            1.0
        ),
        SearchDocument(
            12,
            "Injector Testing and Cleaning",
            "Locomotive fuel injectors must be tested for spray pattern, flow rate, and leakage. Cleaning is performed using ultrasonic baths or chemical solvents. Faulty injectors cause power loss and increased emissions.",
            ["injector", "testing", "cleaning", "fuel-system"],
            1.0
        ),
        SearchDocument(
            13,
            "Radiator and Coolant Management",
            "Locomotive cooling systems require regular radiator inspection, coolant level checks, and leak detection. Use of proper coolant prevents corrosion and overheating.",
            ["radiator", "coolant", "management", "cooling-system"],
            1.0
        ),
        SearchDocument(
            14,
            "Truck Frame Inspection",
            "Truck (bogie) frames must be inspected for cracks, corrosion, and weld integrity. Ultrasonic testing is recommended for detecting subsurface defects. Frames with cracks must be removed from service.",
            ["truck", "bogie", "frame", "inspection", "crack"],
            1.0
        ),
        SearchDocument(
            15,
            "Safety Appliance Inspection",
            "Ladders, handholds, and sill steps must be inspected for secure attachment, deformation, and corrosion. Defective safety appliances must be repaired or replaced before car returns to service.",
            ["safety-appliance", "inspection", "ladder", "handhold", "sill-step"],
            1.0
        ),
        SearchDocument(
            16,
            "Prime Mover Cylinder Inspection",
            "Cylinder inspection includes checking for scoring, wear, and proper ring seating. Non-conforming cylinders must be replaced during overhaul. Use of borescope is recommended.",
            ["prime-mover", "cylinder", "inspection", "overhaul"],
            1.0
        ),
        SearchDocument(
            17,
            "Turbocharger Evaluation",
            "Turbochargers are evaluated for shaft play, oil leakage, and compressor wheel damage. Replacement is required if excessive wear or imbalance is detected.",
            ["turbocharger", "evaluation", "prime-mover", "maintenance"],
            1.0
        ),
        SearchDocument(
            18,
            "Freight Car Brake Valve Inspection",
            "Brake valves must be inspected for leaks, proper operation, and compliance with AAR standards. Faulty valves are replaced during Class I/IA/III inspections.",
            ["brake-valve", "inspection", "freight-car", "aar"],
            1.0
        ),
        SearchDocument(
            19,
            "Wheel Spalling and Shelling",
            "Wheel spalling and shelling are defects caused by material fatigue and impact loads. WILD systems help detect these defects early, preventing wheel failure and derailment.",
            ["wheel", "spalling", "shelling", "wild", "failure"],
            1.0
        ),
        SearchDocument(
            20,
            "Flat Spot Detection",
            "Flat spots on wheels are detected using WILD and visual inspection. Wheels with flat spots exceeding 2 inches must be replaced to prevent track damage and unsafe operation.",
            ["wheel", "flat-spot", "detection", "wild"],
            1.0
        ),
        SearchDocument(
            21,
            "Locomotive Fuel System Maintenance",
            "Fuel system maintenance includes filter replacement, injector testing, and pump inspection. Contaminated fuel causes injector clogging and engine misfire.",
            ["fuel-system", "maintenance", "injector", "filter"],
            1.0
        ),
        SearchDocument(
            22,
            "Locomotive Cooling System Inspection",
            "Cooling system inspection includes radiator cleaning, coolant sampling, and leak checks. Overheated engines may indicate radiator blockage or coolant loss.",
            ["cooling-system", "inspection", "radiator", "coolant"],
            1.0
        ),
        SearchDocument(
            23,
            "Bogie Crack Detection",
            "Crack detection in bogie frames uses ultrasonic and magnetic particle inspection. Early detection prevents catastrophic failure and derailment.",
            ["bogie", "crack", "detection", "inspection"],
            1.0
        ),
        SearchDocument(
            24,
            "Handhold and Sill Step Maintenance",
            "Handholds and sill steps must be maintained for crew safety. Loose or corroded steps are replaced during safety appliance inspections.",
            ["handhold", "sill-step", "maintenance", "safety-appliance"],
            1.0
        ),
        SearchDocument(
            25,
            "Periodic Tank Car Hydrostatic Testing",
            "Tank cars undergo hydrostatic testing every 10 years. DOT-117 cars require more rigorous testing standards than DOT-111. Testing ensures structural integrity and leak prevention.",
            ["tank-car", "hydrostatic", "testing", "dot-117", "dot-111"],
            1.0
        ),
        SearchDocument(
            26,
            "Commutator Maintenance Procedures",
            "Commutator maintenance includes cleaning, undercutting, and brush replacement. Proper maintenance prevents arcing and extends traction motor life.",
            ["commutator", "maintenance", "traction-motor", "brush"],
            1.0
        ),
        SearchDocument(
            27,
            "Vibration Analysis for Bearing Defects",
            "Vibration analysis identifies bearing defects, misalignment, and imbalance. Early detection allows for targeted maintenance and reduces downtime.",
            ["vibration", "analysis", "bearing", "defect", "maintenance"],
            1.0
        ),
        SearchDocument(
            28,
            "Oil Sampling for Wear Metal Detection",
            "Oil sampling detects wear metals such as iron, copper, and lead. High levels indicate component wear and guide overhaul decisions.",
            ["oil-sampling", "wear-metal", "detection", "maintenance"],
            1.0
        ),
        SearchDocument(
            29,
            "Injector Flow Rate Testing",
            "Injector flow rate testing ensures proper fuel delivery. Faulty injectors cause uneven power and increased emissions.",
            ["injector", "flow-rate", "testing", "fuel-system"],
            1.0
        ),
        SearchDocument(
            30,
            "Radiator Leak Detection",
            "Radiator leak detection uses pressure testing and visual inspection. Leaks cause coolant loss and engine overheating.",
            ["radiator", "leak", "detection", "cooling-system"],
            1.0
        ),
        SearchDocument(
            31,
            "Truck Frame Weld Integrity",
            "Weld integrity in truck frames is assessed using ultrasonic testing. Cracked welds compromise structural strength and must be repaired.",
            ["truck", "frame", "weld", "integrity", "inspection"],
            1.0
        ),
        SearchDocument(
            32,
            "Safety Appliance Securement",
            "Safety appliances must be securely attached. Loose ladders or handholds pose safety hazards and are addressed during inspections.",
            ["safety-appliance", "securement", "inspection", "ladder", "handhold"],
            1.0
        ),
        SearchDocument(
            33,
            "Locomotive Cooling System Corrosion Prevention",
            "Corrosion prevention in cooling systems uses proper coolant and regular sampling. Corroded radiators are replaced to maintain cooling efficiency.",
            ["cooling-system", "corrosion", "prevention", "radiator"],
            1.0
        ),
        SearchDocument(
            34,
            "Coupler Knuckle Securement Pin Inspection",
            "Securement pins in coupler knuckles are inspected for wear and integrity. Pins with cracks or excessive wear are replaced.",
            ["coupler", "knuckle", "securement", "pin", "inspection"],
            1.0
        ),
        SearchDocument(
            35,
            "Tank Car Valve Protection",
            "Tank car valves are protected by shields and periodic inspection. DOT-117 standards require improved valve protection compared to DOT-111.",
            ["tank-car", "valve", "protection", "dot-117", "dot-111"],
            1.0
        ),
        SearchDocument(
            36,
            "Traction Motor Brush Wear Inspection",
            "Brush wear in traction motors is inspected during routine maintenance. Worn brushes cause arcing and must be replaced.",
            ["traction-motor", "brush", "wear", "inspection"],
            1.0
        ),
        SearchDocument(
            37,
            "Condition-Based Maintenance Scheduling",
            "Condition-based maintenance schedules are determined by vibration analysis and oil sampling results. This approach reduces unscheduled repairs.",
            ["condition-based", "maintenance", "scheduling", "vibration", "oil-sampling"],
            1.0
        ),
        SearchDocument(
            38,
            "Locomotive Fuel Filter Replacement",
            "Fuel filters are replaced during routine locomotive maintenance. Clogged filters cause injector failure and engine misfire.",
            ["fuel-filter", "replacement", "maintenance", "locomotive"],
            1.0
        ),
        SearchDocument(
            39,
            "Coolant Sampling Procedures",
            "Coolant sampling detects contamination and degradation. Proper sampling ensures cooling system reliability and prevents overheating.",
            ["coolant", "sampling", "procedure", "cooling-system"],
            1.0
        ),
        SearchDocument(
            40,
            "Bogie Ultrasonic Inspection",
            "Ultrasonic inspection of bogie frames detects cracks and weld defects. Early intervention prevents failure and derailment.",
            ["bogie", "ultrasonic", "inspection", "crack", "weld"],
            1.0
        ),
        SearchDocument(
            41,
            "Safety Appliance Corrosion Inspection",
            "Corrosion inspection of safety appliances ensures crew safety. Corroded ladders and handholds are replaced during scheduled maintenance.",
            ["safety-appliance", "corrosion", "inspection", "ladder", "handhold"],
            1.0
        ),
        SearchDocument(
            42,
            "Prime Mover Piston Replacement",
            "Pistons in prime movers are replaced during overhaul if wear or scoring is detected. Proper piston fit ensures engine reliability.",
            ["prime-mover", "piston", "replacement", "overhaul"],
            1.0
        ),
        SearchDocument(
            43,
            "Wheel Flange Thickness Measurement",
            "Wheel flange thickness is measured during inspection. Flanges exceeding condemning limits are replaced to ensure safe operation.",
            ["wheel", "flange", "thickness", "measurement", "inspection"],
            1.0
        ),
        SearchDocument(
            44,
            "Brake Pipe Leakage Testing",
            "Brake pipe leakage is tested during Class I/IA/III inspections. Leakage must not exceed regulatory limits to ensure brake reliability.",
            ["brake-pipe", "leakage", "testing", "inspection"],
            1.0
        ),
        SearchDocument(
            45,
            "Journal Bearing Lubrication",
            "Lubrication of journal bearings prevents overheating and failure. Proper lubricant selection and application are critical for bearing life.",
            ["journal-bearing", "lubrication", "maintenance", "failure"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)