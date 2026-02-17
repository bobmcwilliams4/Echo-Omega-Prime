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
        self.avg_doc_length: float = 0.0
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.total_docs: int = 0
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in set(tokens):
                self.term_doc_freqs[term] += 1
            self.total_docs = len(self.documents)
            self.avg_doc_length = sum(self.doc_lengths.values()) / max(1, self.total_docs)
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, doc in self.documents.items():
                tf = self.term_freqs[doc_id][term]
                score = self._score_bm25(tf, idf, self.doc_lengths[doc_id], doc.weight)
                doc_scores[doc_id] += score
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
            'unique_terms': len(self.term_doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, tf: int, idf: float, doc_len: int, weight: float) -> float:
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
        score = idf * (numerator / (denominator or 1)) * weight
        return score

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            return content[:160] + '...' if len(content) > 160 else content
        start = max(indices[0] - 5, 0)
        end = min(indices[0] + 15, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + '...' if len(snippet_tokens) < len(tokens) else snippet

    def tfidf_score(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, doc in self.documents.items():
                tf = self.term_freqs[doc_id][term]
                norm_tf = tf / (self.doc_lengths[doc_id] or 1)
                score = norm_tf * idf * doc.weight
                doc_scores[doc_id] += score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
                _preseed_documents(_search_index_instance)
    return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Build Rate Limits in Directional Drilling",
            "Build rate is the rate at which the wellbore changes inclination. Typical limits depend on BHA design, motor yield, and formation properties. Excessive build rates can cause tool failure and wellbore tortuosity.",
            ["build rate", "directional drilling", "BHA", "tortuosity"],
            1.0
        ),
        SearchDocument(
            2,
            "Dogleg Severity Calculation and Limits",
            "Dogleg severity (DLS) quantifies the curvature of the wellbore, calculated using survey data. High DLS can increase stuck pipe risk and reduce directional control. Industry limits vary by hole size and BHA.",
            ["dogleg severity", "survey", "stuck pipe", "directional control"],
            1.0
        ),
        SearchDocument(
            3,
            "Motor Yield and Slide Drilling Efficiency",
            "Motor yield refers to the build rate achievable with a positive displacement motor. Slide drilling efficiency depends on toolface control, formation response, and motor design. Monitoring yield is critical for directional performance.",
            ["motor yield", "slide drilling", "toolface", "formation"],
            1.0
        ),
        SearchDocument(
            4,
            "Survey Calculation Methods and Accuracy",
            "Survey calculation methods include minimum curvature, tangential, and radius of curvature. Accuracy depends on sensor calibration, magnetic interference, and survey frequency. Minimum curvature is the industry standard.",
            ["survey", "accuracy", "minimum curvature", "magnetic interference"],
            1.0
        ),
        SearchDocument(
            5,
            "Push vs Point the Bit Rotary Steerable Systems",
            "Rotary Steerable Systems (RSS) are classified as push-the-bit or point-the-bit. Push-the-bit systems apply lateral force, while point-the-bit systems orient the bit. Selection depends on formation, trajectory, and desired build rates.",
            ["RSS", "rotary steerable", "push-the-bit", "point-the-bit"],
            1.0
        ),
        SearchDocument(
            6,
            "Geosteering and Formation Evaluation While Drilling",
            "Geosteering uses real-time formation evaluation to adjust well trajectory. Logging-while-drilling (LWD) tools provide gamma ray, resistivity, and density data. Effective geosteering maximizes reservoir contact.",
            ["geosteering", "formation evaluation", "LWD", "reservoir"],
            1.0
        ),
        SearchDocument(
            7,
            "Anti-Collision Analysis and Separation Factor",
            "Anti-collision analysis ensures safe separation between wellbores. Separation factor is calculated using survey uncertainty and proximity. Proper anti-collision planning prevents wellbore intersection and operational hazards.",
            ["anti-collision", "separation factor", "survey", "hazards"],
            1.0
        ),
        SearchDocument(
            8,
            "Magnetic Interference and Correction Methods",
            "Magnetic interference affects survey accuracy, especially near casing or other wells. Correction methods include In-Field Referencing (IFR) and Multi-Field Modeling (MFM). Proper correction improves well placement.",
            ["magnetic interference", "IFR", "MFM", "survey"],
            1.0
        ),
        SearchDocument(
            9,
            "BHA Design for Directional Control",
            "Bottom Hole Assembly (BHA) design is critical for directional control. Components include stabilizers, motors, and rotary steerable systems. BHA configuration affects build rate, dogleg severity, and trajectory.",
            ["BHA", "directional control", "build rate", "dogleg severity"],
            1.0
        ),
        SearchDocument(
            10,
            "Horizontal Well Landing Techniques",
            "Landing a horizontal well requires precise control of inclination and azimuth. Techniques include using RSS, optimized BHA, and real-time geosteering. Success depends on survey accuracy and formation response.",
            ["horizontal well", "landing", "RSS", "geosteering"],
            1.0
        ),
        SearchDocument(
            11,
            "Wellbore Tortuosity and Quality Metrics",
            "Wellbore tortuosity measures deviations from a smooth trajectory. Quality metrics include DLS, tortuosity index, and survey uncertainty. High tortuosity increases torque, drag, and operational risks.",
            ["tortuosity", "quality metrics", "DLS", "survey"],
            1.0
        ),
        SearchDocument(
            12,
            "Whipstock and Sidetracking Operations",
            "Whipstock tools are used for sidetracking from an existing wellbore. Proper orientation and setting are critical for successful sidetrack. Surveying ensures accurate entry into the new trajectory.",
            ["whipstock", "sidetracking", "survey", "orientation"],
            1.0
        ),
        SearchDocument(
            13,
            "Toolface Orientation: Gravity vs Magnetic",
            "Toolface orientation is referenced to gravity or magnetic north. Gravity toolface is used in vertical wells, magnetic toolface in deviated wells. Accurate orientation improves slide drilling efficiency.",
            ["toolface", "gravity", "magnetic", "slide drilling"],
            1.0
        ),
        SearchDocument(
            14,
            "Stuck Pipe Risk in Directional Drilling",
            "Stuck pipe risk increases with high dogleg severity, poor hole cleaning, and excessive tortuosity. Preventive measures include optimized BHA, proper mud properties, and regular survey updates.",
            ["stuck pipe", "dogleg severity", "tortuosity", "BHA"],
            1.0
        ),
        SearchDocument(
            15,
            "Extended Reach Drilling (ERD) Torque and Drag",
            "Extended Reach Drilling (ERD) presents challenges in torque and drag management. Solutions include lubricants, optimized trajectory, and advanced modeling. ERD enables access to distant reservoirs.",
            ["ERD", "torque", "drag", "trajectory"],
            1.0
        ),
        SearchDocument(
            16,
            "Minimum Curvature Survey Method",
            "The minimum curvature method calculates wellbore position using inclination and azimuth changes between survey stations. It provides accurate trajectory modeling and is widely used in directional drilling.",
            ["minimum curvature", "survey", "trajectory", "directional drilling"],
            1.0
        ),
        SearchDocument(
            17,
            "Positive Displacement Motor Performance",
            "Positive displacement motors are used for slide drilling and directional control. Performance is measured by motor yield, torque output, and reliability. Proper motor selection improves build rate.",
            ["positive displacement motor", "slide drilling", "motor yield", "build rate"],
            1.0
        ),
        SearchDocument(
            18,
            "Rotary Steerable System Selection Criteria",
            "RSS selection depends on trajectory complexity, formation hardness, and desired build rates. Push-the-bit systems excel in soft formations, point-the-bit in hard formations. Cost and reliability are also factors.",
            ["RSS", "selection", "push-the-bit", "point-the-bit"],
            1.0
        ),
        SearchDocument(
            19,
            "Formation Evaluation While Drilling (FEWD)",
            "FEWD uses LWD tools to provide real-time formation data. Gamma ray, resistivity, and density logs guide geosteering decisions. Accurate FEWD improves reservoir contact and well placement.",
            ["FEWD", "LWD", "geosteering", "formation evaluation"],
            1.0
        ),
        SearchDocument(
            20,
            "Anti-Collision Planning for Multi-Well Pads",
            "Multi-well pads require rigorous anti-collision planning. Survey uncertainty, separation factor, and proximity rules are used to prevent wellbore intersection. Software tools automate collision risk analysis.",
            ["anti-collision", "multi-well", "survey", "separation factor"],
            1.0
        ),
        SearchDocument(
            21,
            "Magnetic Survey Correction: IFR and MFM",
            "In-Field Referencing (IFR) and Multi-Field Modeling (MFM) correct for magnetic interference in surveys. IFR uses local field measurements, MFM models multiple fields. Both improve directional accuracy.",
            ["magnetic survey", "IFR", "MFM", "accuracy"],
            1.0
        ),
        SearchDocument(
            22,
            "BHA Stabilizer Placement for Build Rate Control",
            "Stabilizer placement in the BHA affects build rate and directional response. Shorter distance between stabilizers increases build rate. Proper placement reduces dogleg severity and improves trajectory.",
            ["BHA", "stabilizer", "build rate", "dogleg severity"],
            1.0
        ),
        SearchDocument(
            23,
            "Horizontal Well Landing: Survey and Geosteering",
            "Landing a horizontal well requires accurate survey data and real-time geosteering. LWD tools provide formation evaluation to guide trajectory. Proper landing maximizes reservoir exposure.",
            ["horizontal well", "survey", "geosteering", "LWD"],
            1.0
        ),
        SearchDocument(
            24,
            "Wellbore Quality Metrics: Tortuosity Index",
            "Tortuosity index quantifies wellbore smoothness. Lower index indicates better quality and reduced torque/drag. Survey data is used to calculate tortuosity and optimize drilling parameters.",
            ["wellbore quality", "tortuosity index", "survey", "drilling"],
            1.0
        ),
        SearchDocument(
            25,
            "Sidetracking Operations: Whipstock Setting",
            "Sidetracking requires whipstock tools to divert the wellbore. Proper setting and orientation are essential for successful sidetrack. Surveying confirms entry into the new trajectory.",
            ["sidetracking", "whipstock", "survey", "orientation"],
            1.0
        ),
        SearchDocument(
            26,
            "Toolface Control in Slide Drilling",
            "Toolface control is critical for slide drilling efficiency. Gravity and magnetic toolface references are used depending on well inclination. Accurate control improves directional performance.",
            ["toolface", "slide drilling", "gravity", "magnetic"],
            1.0
        ),
        SearchDocument(
            27,
            "Stuck Pipe Prevention Strategies",
            "Preventing stuck pipe involves managing dogleg severity, maintaining hole cleaning, and optimizing BHA design. Regular survey updates and proper mud properties reduce risk.",
            ["stuck pipe", "prevention", "dogleg severity", "BHA"],
            1.0
        ),
        SearchDocument(
            28,
            "ERD: Torque and Drag Modeling",
            "Torque and drag modeling is essential for ERD operations. Software tools simulate wellbore friction and predict operational limits. Lubricants and optimized trajectory reduce torque and drag.",
            ["ERD", "torque", "drag", "modeling"],
            1.0
        ),
        SearchDocument(
            29,
            "Directional Drilling: Survey Frequency Optimization",
            "Survey frequency affects trajectory accuracy and collision risk. Frequent surveys improve well placement but increase operational time. Optimization balances accuracy and efficiency.",
            ["directional drilling", "survey frequency", "accuracy", "collision risk"],
            1.0
        ),
        SearchDocument(
            30,
            "Rotary Steerable: Push vs Point Performance",
            "Push-the-bit RSS systems provide high build rates in soft formations, while point-the-bit systems offer precise control in hard formations. Performance depends on formation and trajectory complexity.",
            ["rotary steerable", "push-the-bit", "point-the-bit", "performance"],
            1.0
        ),
        SearchDocument(
            31,
            "Geosteering: Real-Time Formation Data",
            "Real-time formation data from LWD tools enables geosteering adjustments. Gamma ray and resistivity logs guide trajectory changes to maximize reservoir contact.",
            ["geosteering", "real-time", "formation data", "LWD"],
            1.0
        ),
        SearchDocument(
            32,
            "Anti-Collision: Survey Uncertainty Management",
            "Managing survey uncertainty is key to anti-collision planning. Separation factor calculations and proximity rules ensure safe wellbore spacing.",
            ["anti-collision", "survey uncertainty", "separation factor", "proximity"],
            1.0
        ),
        SearchDocument(
            33,
            "Magnetic Interference: Correction Techniques",
            "Correction techniques for magnetic interference include IFR, MFM, and sensor calibration. Accurate corrections improve survey reliability and well placement.",
            ["magnetic interference", "correction", "IFR", "MFM"],
            1.0
        ),
        SearchDocument(
            34,
            "BHA Design: Directional Control Optimization",
            "Optimizing BHA design improves directional control and build rate. Component selection and stabilizer placement are critical for trajectory management.",
            ["BHA", "directional control", "optimization", "build rate"],
            1.0
        ),
        SearchDocument(
            35,
            "Horizontal Well Landing: RSS and Geosteering",
            "RSS and geosteering techniques are used for horizontal well landing. Survey accuracy and real-time formation evaluation guide well trajectory.",
            ["horizontal well", "RSS", "geosteering", "survey"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)