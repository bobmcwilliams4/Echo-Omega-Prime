import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
        self.doc_tokens: Dict[int, List[str]] = {}
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.inverted_index[term].add(doc.id)
                self.doc_freqs[term] += 1
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

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

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            s = idf * ((freq * (self.k1 + 1)) / denom)
            score += s
        doc = self.documents[doc_id]
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_norm = tf[term] / doc_len if doc_len > 0 else 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        doc = self.documents[doc_id]
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs: Set[int] = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scored.append((doc_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results: List[SearchResult] = []
        for doc_id, score in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:window])
        else:
            start = max(positions[0] - window // 2, 0)
            end = min(start + window, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'vocab_size': len(self.inverted_index)
            }

# Singleton factory for search index
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
            id=1,
            title="Frontal Airbag Non-Deployment Case Study",
            content="Analysis of frontal airbag non-deployment in moderate overlap crashes. Focus on sensor logic, deployment thresholds, and occupant position.",
            tags=["frontal airbag", "non-deployment", "crash analysis"],
            weight=1.0
        ),
        SearchDocument(
            id=2,
            title="Seatbelt Pretensioner Failure Modes",
            content="Review of pretensioner pyrotechnic device failures, electrical connector issues, and diagnostic trouble codes affecting seatbelt performance.",
            tags=["seatbelt", "pretensioner", "failure"],
            weight=1.0
        ),
        SearchDocument(
            id=3,
            title="AEB False Negative Investigation",
            content="Automatic Emergency Braking (AEB) systems may fail to activate in certain low-contrast or oblique angle scenarios. Case examples and sensor limitations discussed.",
            tags=["AEB", "false negative", "sensor"],
            weight=1.0
        ),
        SearchDocument(
            id=4,
            title="Side-Impact Airbag Deployment Thresholds",
            content="Defines acceleration and velocity thresholds for side-impact airbag deployment. Includes discussion of FMVSS 214 compliance.",
            tags=["side-impact", "airbag", "threshold"],
            weight=1.0
        ),
        SearchDocument(
            id=5,
            title="Blind Spot Monitoring System Limitations",
            content="Explores radar and camera-based BSM system limitations, including detection gaps, weather effects, and false alerts.",
            tags=["BSM", "blind spot", "monitoring", "limitations"],
            weight=1.0
        ),
        SearchDocument(
            id=6,
            title="Pedestrian Detection System Performance",
            content="Evaluation of pedestrian detection accuracy in day and night conditions. Includes test results and NHTSA protocol references.",
            tags=["pedestrian detection", "AEB", "performance"],
            weight=1.0
        ),
        SearchDocument(
            id=7,
            title="FMVSS 208 Advanced Airbag Rule Compliance",
            content="Summary of advanced airbag requirements under FMVSS 208, including suppression logic for children and small adults.",
            tags=["FMVSS 208", "advanced airbag", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id=8,
            title="LDW vs. LKA Functionality Comparison",
            content="Compares Lane Departure Warning (LDW) and Lane Keep Assist (LKA) system functions, intervention types, and driver alerts.",
            tags=["LDW", "LKA", "lane departure", "assist"],
            weight=1.0
        ),
        SearchDocument(
            id=9,
            title="Rollover Crash Roof Strength and Occupant Protection",
            content="Discusses roof crush resistance, FMVSS 216, and the role of curtain airbags in rollover occupant protection.",
            tags=["rollover", "roof strength", "occupant protection"],
            weight=1.0
        ),
        SearchDocument(
            id=10,
            title="Crash Data Recorder (CDR) Admissibility and Interpretation",
            content="Legal and technical considerations for CDR data use in crash reconstruction. Includes event data parameters and court precedents.",
            tags=["CDR", "crash data", "admissibility"],
            weight=1.0
        ),
        SearchDocument(
            id=11,
            title="Occupant Classification System Suppression Logic",
            content="Explains OCS sensor types, weight thresholds, and suppression logic for airbag deployment.",
            tags=["OCS", "occupant classification", "suppression"],
            weight=1.0
        ),
        SearchDocument(
            id=12,
            title="TPMS Warnings and Blowout Crash Analysis",
            content="Examines tire pressure monitoring system (TPMS) warning effectiveness and its relation to high-speed blowout crashes.",
            tags=["TPMS", "tire pressure", "blowout"],
            weight=1.0
        ),
        SearchDocument(
            id=13,
            title="ESC Intervention and Limitations",
            content="Electronic Stability Control (ESC) system operation, intervention scenarios, and known limitations in icy or gravel conditions.",
            tags=["ESC", "stability control", "limitations"],
            weight=1.0
        ),
        SearchDocument(
            id=14,
            title="Seatbelt Webbing Failure and Load Limiter Function",
            content="Analysis of seatbelt webbing material failures and the function of load limiters in occupant restraint.",
            tags=["seatbelt", "webbing", "load limiter"],
            weight=1.0
        ),
        SearchDocument(
            id=15,
            title="Adaptive Cruise Control Following Distance",
            content="Explores ACC settable following distances, sensor fusion, and emergency braking integration.",
            tags=["ACC", "adaptive cruise", "following distance"],
            weight=1.0
        ),
        SearchDocument(
            id=16,
            title="Curtain Airbag Deployment in Rollover Crashes",
            content="Timing and logic for curtain airbag deployment in rollover scenarios. Includes sensor types and multi-stage deployment.",
            tags=["curtain airbag", "rollover", "deployment"],
            weight=1.0
        ),
        SearchDocument(
            id=17,
            title="Forward Collision Warning Alert Timing",
            content="FCW system alert timing, driver reaction, and integration with AEB. Includes test protocols and real-world data.",
            tags=["FCW", "forward collision", "alert timing"],
            weight=1.0
        ),
        SearchDocument(
            id=18,
            title="Rear Cross-Traffic Alert Detection Zones",
            content="Defines RCTA detection zones, sensor coverage, and limitations in angled parking scenarios.",
            tags=["RCTA", "rear cross-traffic", "detection zone"],
            weight=1.0
        ),
        SearchDocument(
            id=19,
            title="Headrest Design and Whiplash Injury Mitigation",
            content="Discusses headrest geometry, active head restraints, and whiplash injury reduction in rear-end collisions.",
            tags=["headrest", "whiplash", "injury mitigation"],
            weight=1.0
        ),
        SearchDocument(
            id=20,
            title="Child Safety Seat Compatibility and LATCH System",
            content="Covers LATCH anchor locations, child seat compatibility, and FMVSS 225 requirements.",
            tags=["child safety", "LATCH", "compatibility"],
            weight=1.0
        ),
        SearchDocument(
            id=21,
            title="Daytime Running Lights and Rear-End Collision Visibility",
            content="Examines DRL effectiveness in improving vehicle visibility and reducing rear-end collisions.",
            tags=["DRL", "daytime running lights", "visibility"],
            weight=1.0
        ),
        SearchDocument(
            id=22,
            title="Backup Camera and Rear Visibility Standards",
            content="Details FMVSS 111 requirements for rear visibility, backup camera field of view, and display timing.",
            tags=["backup camera", "FMVSS 111", "rear visibility"],
            weight=1.0
        ),
        SearchDocument(
            id=23,
            title="Knee Airbag Deployment and Lower Extremity Injury",
            content="Explores knee airbag deployment logic, crash test data, and injury mitigation for lower extremities.",
            tags=["knee airbag", "lower extremity", "injury"],
            weight=1.0
        ),
        SearchDocument(
            id=24,
            title="Post-Crash Fuel System Integrity and Fire Risk",
            content="FMVSS 301 requirements for post-crash fuel system integrity, fire risk, and fuel shutoff strategies.",
            tags=["fuel system", "FMVSS 301", "fire risk"],
            weight=1.0
        ),
        SearchDocument(
            id=25,
            title="Advanced Airbag Sensor Technologies",
            content="Overview of multi-stage inflators, occupant detection, and adaptive deployment strategies in advanced airbag systems.",
            tags=["advanced airbag", "sensor", "deployment"],
            weight=1.0
        ),
        SearchDocument(
            id=26,
            title="Crash Data Recorder Event Data Parameters",
            content="Lists common CDR parameters: delta-V, seatbelt status, pre-crash speed, and airbag deployment time.",
            tags=["CDR", "event data", "parameters"],
            weight=1.0
        ),
        SearchDocument(
            id=27,
            title="Lane Keep Assist Limitations in Snow",
            content="LKA system performance in snow-covered roads, camera occlusion, and lane marking detection challenges.",
            tags=["LKA", "lane keep", "snow"],
            weight=1.0
        ),
        SearchDocument(
            id=28,
            title="Side Curtain Airbag Coverage Zones",
            content="Defines side curtain airbag coverage, head protection, and ejection mitigation in side and rollover crashes.",
            tags=["curtain airbag", "side impact", "coverage"],
            weight=1.0
        ),
        SearchDocument(
            id=29,
            title="FMVSS 208 Child Occupant Airbag Suppression",
            content="Details suppression requirements for child occupants under FMVSS 208 advanced airbag rules.",
            tags=["FMVSS 208", "child", "suppression"],
            weight=1.0
        ),
        SearchDocument(
            id=30,
            title="TPMS Sensor Battery Failure and Warning Reliability",
            content="Analysis of TPMS sensor battery life, failure rates, and warning reliability in extended vehicle operation.",
            tags=["TPMS", "sensor", "battery failure"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)