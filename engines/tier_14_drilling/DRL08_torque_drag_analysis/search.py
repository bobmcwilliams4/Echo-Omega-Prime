import math
import re
import threading
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
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.avg_doc_len: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old document term frequencies from index
                old_tf = self.doc_term_freqs.get(doc.id)
                if old_tf:
                    for term in old_tf:
                        self.term_doc_freqs[term] -= 1
                        if self.term_doc_freqs[term] <= 0:
                            del self.term_doc_freqs[term]
                self.total_docs -= 1

            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            tf = Counter(tokens)
            self.doc_term_freqs[doc.id] = tf

            # Update document frequencies
            unique_terms = set(tf.keys())
            for term in unique_terms:
                self.term_doc_freqs[term] += 1

            self.documents[doc.id] = doc
            self.total_docs += 1

            # Recalculate average document length
            total_len = sum(sum(freq for freq in tf.values()) for tf in self.doc_term_freqs.values())
            self.avg_doc_len = total_len / self.total_docs if self.total_docs > 0 else 0.0

            # Clear IDF cache
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        scores: Dict[str, float] = defaultdict(float)
        idf_values = {term: self._compute_idf(term) for term in query_terms}

        for doc_id, tf in self.doc_term_freqs.items():
            doc_len = sum(tf.values())
            score = 0.0
            for term in query_terms:
                if term not in tf:
                    continue
                freq = tf[term]
                idf = idf_values.get(term, 0.0)
                score += self._score_bm25(freq, idf, doc_len)
            if score > 0:
                # Weight boost
                score *= self.documents[doc_id].weight
                scores[doc_id] = score

        # Sort by score descending
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'total_documents': self.total_docs,
                'average_document_length': self.avg_doc_len,
                'unique_terms': len(self.term_doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, freq: int, idf: float, doc_len: int) -> float:
        denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len) if self.avg_doc_len > 0 else freq + self.k1
        score = idf * freq * (self.k1 + 1) / denom if denom > 0 else 0.0
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 150) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + len(term)
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += '...'
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_len // 4, 0)
        end_pos = min(start_pos + snippet_len, len(content))
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = '...' + snippet
        if end_pos < len(content):
            snippet += '...'
        return snippet


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _preseed_documents(_singleton_instance)
        return _singleton_instance


def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="doc001",
            title="Soft String vs Stiff String Models",
            content=(
                "Comparison of soft string and stiff string models in drillstring analysis. "
                "Soft string models consider flexibility and axial deformation, while stiff string models "
                "assume rigid behavior. The choice affects torque and drag predictions."
            ),
            tags=["modeling", "soft string", "stiff string", "drillstring", "torque", "drag"]
        ),
        SearchDocument(
            doc_id="doc002",
            title="Friction Factor Estimation in Drillstrings",
            content=(
                "Methods for estimating friction factors in drillstring components including drill pipe, "
                "collars, and casing. Factors influencing friction include surface roughness, lubrication, "
                "and contact pressure."
            ),
            tags=["friction", "torque", "drag", "estimation", "drillstring"]
        ),
        SearchDocument(
            doc_id="doc003",
            title="Hook Load Calculations - Tripping In",
            content=(
                "Calculating hook load during tripping in operations. Considerations include string weight, "
                "drag forces, and fluid buoyancy effects."
            ),
            tags=["hook load", "tripping in", "drag", "buoyancy", "weight"]
        ),
        SearchDocument(
            doc_id="doc004",
            title="Hook Load Calculations - Tripping Out",
            content=(
                "Analysis of hook load during tripping out. Includes effects of drag, fluid velocity, and "
                "string acceleration."
            ),
            tags=["hook load", "tripping out", "drag", "fluid velocity"]
        ),
        SearchDocument(
            doc_id="doc005",
            title="Hook Load - Rotating and Sliding",
            content=(
                "Modeling hook load when the drillstring is rotating and sliding simultaneously. "
                "Torque and drag interactions are critical."
            ),
            tags=["hook load", "rotating", "sliding", "torque", "drag"]
        ),
        SearchDocument(
            doc_id="doc006",
            title="Make-Up Torque for Connections (API RP 7G)",
            content=(
                "Guidelines for calculating make-up torque for drillstring connections based on API RP 7G. "
                "Includes factors such as thread geometry and lubrication."
            ),
            tags=["make-up torque", "connections", "API RP 7G", "thread", "lubrication"]
        ),
        SearchDocument(
            doc_id="doc007",
            title="Drill Collar Weight on Bit and Neutral Point",
            content=(
                "Determining drill collar weight on bit and locating the neutral point where axial load "
                "transitions from tension to compression."
            ),
            tags=["drill collar", "weight on bit", "neutral point", "axial load"]
        ),
        SearchDocument(
            doc_id="doc008",
            title="Buckling Analysis - Sinusoidal and Helical",
            content=(
                "Buckling behavior of drillstrings under compressive loads. Sinusoidal and helical buckling "
                "modes are analyzed with respect to axial force and torque."
            ),
            tags=["buckling", "sinusoidal", "helical", "compressive load", "drillstring"]
        ),
        SearchDocument(
            doc_id="doc009",
            title="Overpull Limits and Pipe Tensile Capacity",
            content=(
                "Calculations of overpull limits based on pipe tensile strength and operational safety factors. "
                "Includes effects of temperature and corrosion."
            ),
            tags=["overpull", "tensile capacity", "pipe strength", "safety"]
        ),
        SearchDocument(
            doc_id="doc010",
            title="Jarring Operations - Mechanical and Hydraulic Jars",
            content=(
                "Principles and calculations for mechanical and hydraulic jarring operations used to free stuck pipe. "
                "Includes jar impact energy and force estimations."
            ),
            tags=["jarring", "mechanical jar", "hydraulic jar", "stuck pipe"]
        ),
        SearchDocument(
            doc_id="doc011",
            title="Stuck Pipe Mechanisms - Differential Sticking",
            content=(
                "Analysis of differential sticking mechanisms where pressure differential causes pipe to adhere "
                "to the wellbore wall."
            ),
            tags=["stuck pipe", "differential sticking", "pressure differential"]
        ),
        SearchDocument(
            doc_id="doc012",
            title="Stuck Pipe Mechanisms - Keyseating",
            content=(
                "Keyseating formation and its effect on pipe sticking. Modeling the interaction between pipe and "
                "wellbore irregularities."
            ),
            tags=["stuck pipe", "keyseating", "wellbore", "pipe interaction"]
        ),
        SearchDocument(
            doc_id="doc013",
            title="Stuck Pipe Mechanisms - Pack-Off and Cuttings Bed",
            content=(
                "Mechanisms of pack-off and cuttings bed formation leading to pipe sticking. Analysis includes "
                "cuttings transport and hole cleaning."
            ),
            tags=["stuck pipe", "pack-off", "cuttings bed", "hole cleaning"]
        ),
        SearchDocument(
            doc_id="doc014",
            title="Drillstring Fatigue Analysis",
            content=(
                "Fatigue life estimation of drillstrings under cyclic loads. Includes stress calculations and "
                "fatigue damage accumulation."
            ),
            tags=["fatigue", "drillstring", "cyclic loads", "stress"]
        ),
        SearchDocument(
            doc_id="doc015",
            title="Drillstring Vibration - Lateral, Axial, Torsional",
            content=(
                "Modeling and analysis of drillstring vibrations in lateral, axial, and torsional modes. "
                "Effects on tool life and drilling efficiency."
            ),
            tags=["vibration", "lateral", "axial", "torsional", "drillstring"]
        ),
        SearchDocument(
            doc_id="doc016",
            title="Stick-Slip Mitigation Techniques",
            content=(
                "Strategies to mitigate stick-slip vibrations including drilling parameter optimization and "
                "tool design."
            ),
            tags=["stick-slip", "vibration mitigation", "drilling parameters"]
        ),
        SearchDocument(
            doc_id="doc017",
            title="Casing Running Torque and Drag",
            content=(
                "Calculations of torque and drag during casing running operations. Considerations include "
                "casing weight, friction, and wellbore geometry."
            ),
            tags=["casing", "torque", "drag", "running operations"]
        ),
        SearchDocument(
            doc_id="doc018",
            title="BHA Stability Analysis",
            content=(
                "Analysis of Bottom Hole Assembly (BHA) stability to prevent lateral vibrations and improve "
                "drilling performance."
            ),
            tags=["BHA", "stability", "vibration", "drilling"]
        ),
        SearchDocument(
            doc_id="doc019",
            title="Drillstring Axial Force Distribution",
            content=(
                "Modeling axial force distribution along the drillstring during various operations including "
                "tripping and drilling."
            ),
            tags=["axial force", "drillstring", "force distribution"]
        ),
        SearchDocument(
            doc_id="doc020",
            title="Torque and Drag Effects of Tool Joints",
            content=(
                "Influence of tool joint geometry and condition on torque and drag in the drillstring."
            ),
            tags=["torque", "drag", "tool joints", "geometry"]
        ),
        SearchDocument(
            doc_id="doc021",
            title="Mud Motor Torque and Drag Analysis",
            content=(
                "Calculations of torque and drag when using mud motors. Effects on drillstring dynamics."
            ),
            tags=["mud motor", "torque", "drag", "drillstring"]
        ),
        SearchDocument(
            doc_id="doc022",
            title="Effects of Wellbore Inclination on Torque and Drag",
            content=(
                "Impact of wellbore trajectory and inclination on torque and drag forces experienced by the drillstring."
            ),
            tags=["wellbore", "inclination", "torque", "drag"]
        ),
        SearchDocument(
            doc_id="doc023",
            title="Drillstring Buckling Prevention Methods",
            content=(
                "Techniques to prevent sinusoidal and helical buckling including weight management and centralizers."
            ),
            tags=["buckling", "prevention", "centralizers", "weight management"]
        ),
        SearchDocument(
            doc_id="doc024",
            title="Hydraulic Effects on Drillstring Torque and Drag",
            content=(
                "Influence of drilling fluid hydraulics on torque and drag including annular pressure losses."
            ),
            tags=["hydraulics", "torque", "drag", "fluid"]
        ),
        SearchDocument(
            doc_id="doc025",
            title="Drillstring Fatigue Damage Models",
            content=(
                "Models for predicting fatigue damage accumulation in drillstrings under complex loading cycles."
            ),
            tags=["fatigue", "damage", "models", "drillstring"]
        ),
        SearchDocument(
            doc_id="doc026",
            title="Torque and Drag Modeling Software Overview",
            content=(
                "Overview of software tools and algorithms used for torque and drag modeling in drilling engineering."
            ),
            tags=["software", "modeling", "torque", "drag"]
        ),
        SearchDocument(
            doc_id="doc027",
            title="API RP 7G Connection Make-Up and Break-Out Torque",
            content=(
                "Detailed procedures for calculating make-up and break-out torque for drillstring connections "
                "following API RP 7G standards."
            ),
            tags=["API RP 7G", "make-up torque", "break-out torque", "connections"]
        ),
    ]

    for doc in docs:
        index.add_document(doc)