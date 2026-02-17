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
        self.doc_count: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            self.doc_count += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.doc_count if self.doc_count else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            scores[doc_id] = combined_score * doc.weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "doc_count": self.doc_count,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.doc_count - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        tf = self.term_freqs[doc_id]
        for term in query_tokens:
            f = tf.get(term, 0)
            idf = self._compute_idf(term)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        if doc_id in self._tfidf_cache:
            tfidf = self._tfidf_cache[doc_id]
        else:
            tfidf = {}
            tf = self.term_freqs[doc_id]
            doc_len = self.doc_lengths[doc_id]
            for term in tf:
                tf_norm = tf[term] / doc_len if doc_len > 0 else 0
                idf = self._compute_idf(term)
                tfidf[term] = tf_norm * idf
            self._tfidf_cache[doc_id] = tfidf
        score = 0.0
        for term in query_tokens:
            score += tfidf.get(term, 0.0)
        return score

    def _make_snippet(self, content: str, query_tokens: List[str], length: int = 80) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not indices:
            snippet = ' '.join(tokens[:length])
        else:
            start = max(indices[0] - 10, 0)
            end = min(indices[0] + length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1,
                "ISA-75.01.01 Control Valve Cv Sizing",
                "Cv sizing for control valves per ISA-75.01.01 involves calculating the required flow coefficient based on process conditions, including pressure drop, flow rate, and fluid properties.",
                ["Cv", "ISA-75.01.01", "Sizing"],
                1.0
            ),
            SearchDocument(
                2,
                "Globe Valve vs Butterfly Valve Selection",
                "Globe valves are preferred for precise throttling and control, while butterfly valves are suitable for larger flows and lower pressure drops. Selection depends on application requirements.",
                ["Globe Valve", "Butterfly Valve", "Selection"],
                1.0
            ),
            SearchDocument(
                3,
                "API 520 Safety Relief Valve Sizing",
                "Safety relief valve sizing per API 520 requires determining the required relieving capacity based on process pressure, temperature, and fluid characteristics.",
                ["Safety Relief Valve", "API 520", "Sizing"],
                1.0
            ),
            SearchDocument(
                4,
                "Equal Percentage vs Linear Control Valve Characteristics",
                "Equal percentage valves provide exponential flow change per stem movement, ideal for applications with varying pressure drops. Linear valves offer proportional flow change.",
                ["Valve Characteristics", "Equal Percentage", "Linear"],
                1.0
            ),
            SearchDocument(
                5,
                "Pneumatic vs Electric Actuator Selection",
                "Pneumatic actuators are favored for fast response and fail-safe operation, while electric actuators offer precise control and integration with automation systems.",
                ["Actuator", "Pneumatic", "Electric", "Selection"],
                1.0
            ),
            SearchDocument(
                6,
                "NACE MR0175 Material Selection for Sour Service",
                "Material selection per NACE MR0175 ensures resistance to sulfide stress cracking in sour environments, requiring specific alloys and heat treatments.",
                ["NACE MR0175", "Material Selection", "Sour Service"],
                1.0
            ),
            SearchDocument(
                7,
                "API 6A Wellhead and Christmas Tree Valve Requirements",
                "API 6A specifies requirements for wellhead and Christmas tree valves, including pressure ratings, material compatibility, and testing procedures for oilfield production.",
                ["API 6A", "Wellhead", "Christmas Tree", "Valve"],
                1.0
            ),
            SearchDocument(
                8,
                "Valve Noise Prediction per IEC 60534-8-3",
                "IEC 60534-8-3 provides methods for predicting valve noise based on flow conditions, valve geometry, and pressure drop, aiding in noise mitigation strategies.",
                ["Valve Noise", "IEC 60534-8-3", "Prediction"],
                1.0
            ),
            SearchDocument(
                9,
                "Cavitation and Flashing in Control Valves",
                "Cavitation occurs when liquid vaporizes inside a valve due to pressure drop, causing damage. Flashing is similar but vapor persists downstream. Proper sizing and trim selection mitigate these effects.",
                ["Cavitation", "Flashing", "Control Valves"],
                1.0
            ),
            SearchDocument(
                10,
                "Fugitive Emissions Standards for Valve Packing",
                "Valve packing must comply with fugitive emissions standards such as ISO 15848 and API 622 to minimize leakage of hazardous gases.",
                ["Fugitive Emissions", "Valve Packing", "Standards"],
                1.0
            ),
            SearchDocument(
                11,
                "Fire-Safe Valve Design per API 607",
                "API 607 outlines fire-safe design requirements for valves, including testing procedures to ensure valve integrity during fire exposure.",
                ["Fire-Safe", "API 607", "Valve Design"],
                1.0
            ),
            SearchDocument(
                12,
                "Choke Valve Sizing for Oilfield Production",
                "Choke valve sizing involves determining the required orifice area to control production flow rates and pressure in oilfield applications.",
                ["Choke Valve", "Sizing", "Oilfield Production"],
                1.0
            ),
            SearchDocument(
                13,
                "Pressure Regulating Valve Selection and Sizing",
                "Pressure regulating valves maintain downstream pressure within set limits. Sizing considers flow rate, pressure drop, and valve characteristics.",
                ["Pressure Regulating Valve", "Selection", "Sizing"],
                1.0
            ),
            SearchDocument(
                14,
                "Gate Valve vs Ball Valve for Isolation Service",
                "Gate valves are suitable for full open/close isolation, while ball valves offer tight shutoff and quick operation. Selection depends on process requirements.",
                ["Gate Valve", "Ball Valve", "Isolation"],
                1.0
            ),
            SearchDocument(
                15,
                "Check Valve Selection and Slam Prevention",
                "Check valves prevent backflow. Slam prevention methods include using damped designs and selecting appropriate closing speeds.",
                ["Check Valve", "Selection", "Slam Prevention"],
                1.0
            ),
            SearchDocument(
                16,
                "Valve Body Material Selection for Temperature Service",
                "Valve body material selection considers temperature limits, corrosion resistance, and mechanical strength. Common materials include carbon steel, stainless steel, and alloys.",
                ["Valve Body", "Material Selection", "Temperature Service"],
                1.0
            ),
            SearchDocument(
                17,
                "Valve End Connection Selection: Flanged vs Threaded vs Welded",
                "Flanged connections allow easy maintenance, threaded are used for small sizes, and welded offer leak-tight performance for high-pressure applications.",
                ["Valve End Connection", "Flanged", "Threaded", "Welded"],
                1.0
            ),
            SearchDocument(
                18,
                "Valve Stem Sealing: Packing vs Bellows Seal",
                "Packing provides flexible sealing but may require maintenance. Bellows seal eliminates stem leakage, ideal for hazardous fluids.",
                ["Valve Stem", "Sealing", "Packing", "Bellows"],
                1.0
            ),
            SearchDocument(
                19,
                "Valve Testing Requirements per API and ASME Standards",
                "Valve testing per API and ASME includes hydrostatic, seat leakage, and functional tests to ensure compliance and performance.",
                ["Valve Testing", "API", "ASME", "Requirements"],
                1.0
            ),
            SearchDocument(
                20,
                "Valve Maintenance and Testing Schedules",
                "Regular valve maintenance and testing schedules are essential for reliability, including inspection, lubrication, and performance verification.",
                ["Valve Maintenance", "Testing", "Schedules"],
                1.0
            ),
            SearchDocument(
                21,
                "Double Block and Bleed (DBB) Valve Configuration",
                "DBB valves provide isolation and venting for critical applications, enhancing safety during maintenance and shutdowns.",
                ["DBB Valve", "Double Block and Bleed", "Configuration"],
                1.0
            ),
            SearchDocument(
                22,
                "Control Valve Sizing for Steam Service",
                "Steam service requires control valve sizing based on pressure, temperature, and flow rate, considering flashing and cavitation risks.",
                ["Control Valve", "Sizing", "Steam Service"],
                1.0
            ),
            SearchDocument(
                23,
                "Valve Trim Selection for Severe Service",
                "Severe service trim includes hardened materials and special designs to resist erosion, cavitation, and flashing in high-pressure applications.",
                ["Valve Trim", "Severe Service", "Selection"],
                1.0
            ),
            SearchDocument(
                24,
                "Low-Emission Valve Design per API 641",
                "API 641 specifies requirements for low-emission valve designs, focusing on packing and stem sealing to minimize fugitive emissions.",
                ["Low-Emission", "API 641", "Valve Design"],
                1.0
            ),
            SearchDocument(
                25,
                "Valve Actuator Sizing and Selection",
                "Actuator sizing considers valve torque requirements, supply pressure, and fail-safe operation. Selection depends on control system integration.",
                ["Valve Actuator", "Sizing", "Selection"],
                1.0
            ),
            SearchDocument(
                26,
                "Valve Positioner Selection and Calibration",
                "Valve positioners improve control accuracy. Selection depends on actuator type, control signal, and calibration procedures.",
                ["Valve Positioner", "Selection", "Calibration"],
                1.0
            ),
            SearchDocument(
                27,
                "Valve Leakage Classes per ANSI/FCI 70-2",
                "ANSI/FCI 70-2 defines valve leakage classes from Class I to VI, specifying allowable leakage rates for different applications.",
                ["Valve Leakage", "ANSI/FCI 70-2", "Classes"],
                1.0
            ),
            SearchDocument(
                28,
                "Valve Flow Characterization and Rangeability",
                "Valve flow characterization determines how flow changes with stem position. Rangeability is the ratio of maximum to minimum controllable flow.",
                ["Valve Flow", "Characterization", "Rangeability"],
                1.0
            ),
            SearchDocument(
                29,
                "Valve Sizing for Liquid and Gas Applications",
                "Valve sizing for liquids and gases involves different equations, considering density, viscosity, compressibility, and flow regime.",
                ["Valve Sizing", "Liquid", "Gas", "Applications"],
                1.0
            ),
            SearchDocument(
                30,
                "Valve Selection for Corrosive Service",
                "Corrosive service requires valve materials and designs resistant to chemical attack, such as alloys and special coatings.",
                ["Valve Selection", "Corrosive Service", "Materials"],
                1.0
            ),
            SearchDocument(
                31,
                "Valve Automation and Remote Control",
                "Valve automation enables remote operation and monitoring, integrating actuators, positioners, and control systems.",
                ["Valve Automation", "Remote Control"],
                1.0
            ),
            SearchDocument(
                32,
                "Valve Pressure Drop Calculations",
                "Pressure drop across a valve is calculated using flow rate, Cv, and fluid properties. Accurate calculations ensure proper sizing and performance.",
                ["Valve Pressure Drop", "Calculations"],
                1.0
            ),
            SearchDocument(
                33,
                "Valve Selection for Cryogenic Service",
                "Cryogenic service valves require materials and designs suitable for low temperatures, preventing embrittlement and leakage.",
                ["Valve Selection", "Cryogenic Service", "Materials"],
                1.0
            ),
            SearchDocument(
                34,
                "Valve Selection for High-Pressure Service",
                "High-pressure service valves must withstand elevated pressures, requiring robust designs, materials, and testing per API standards.",
                ["Valve Selection", "High-Pressure Service", "API"],
                1.0
            ),
            SearchDocument(
                35,
                "Valve Selection for Slurry and Abrasive Service",
                "Slurry and abrasive service valves use hardened trims and special designs to resist wear and maintain performance.",
                ["Valve Selection", "Slurry Service", "Abrasive"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

def get_search_index() -> SearchIndex:
    if not hasattr(get_search_index, "_instance"):
        idx = SearchIndex()
        idx._preseed_documents()
        get_search_index._instance = idx
    return get_search_index._instance