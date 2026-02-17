import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: int, title: str, content: str, tags: List[str] = None, weight: float = 1.0):
        self.id = doc_id
        self.title = title
        self.content = content
        self.tags = tags or []
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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.doc_count: int = 0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            term_freq = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            for term, freq in term_freq.items():
                self.inverted_index[term][doc.id] = freq
                self.term_doc_freq[term] += 1
            self.doc_count += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.doc_count if self.doc_count else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
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

    def _score_bm25(self, query_terms: List[str], doc: SearchDocument) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc.id, 0)
        tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
        term_freq = Counter(tokens)
        for term in set(query_terms):
            f = term_freq.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * (doc_len / (self.avg_doc_length or 1)))
            numer = f * (self.k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc: SearchDocument) -> float:
        score = 0.0
        tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
        term_freq = Counter(tokens)
        max_tf = max(term_freq.values()) if term_freq else 1
        for term in set(query_terms):
            tf = term_freq.get(term, 0) / max_tf
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored: List[Tuple[float, int]] = []
        for doc_id in candidate_docs:
            doc = self.documents[doc_id]
            if use_bm25:
                score = self._score_bm25(query_terms, doc)
            else:
                score = self._score_tfidf(query_terms, doc)
            if score > 0:
                scored.append((score, doc_id))
        scored.sort(reverse=True)
        results = []
        for score, doc_id in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], max_len: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:max_len] + ("..." if len(content) > max_len else "")
        start = max(positions[0] - 5, 0)
        end = min(start + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        if len(snippet) > max_len:
            snippet = snippet[:max_len] + "..."
        return snippet

    def get_stats(self) -> Dict[str, int]:
        return {
            "doc_count": self.doc_count,
            "unique_terms": len(self.inverted_index),
            "avg_doc_length": int(self.avg_doc_length),
        }

# Singleton factory for SearchIndex
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Kick Detection: Pit Gain Method",
            "The pit gain method involves monitoring the active pit volume for unexpected increases, which may indicate influx of formation fluids (kick). Accurate pit level measurement and trending are essential for early kick detection.",
            ["kick detection", "pit gain", "well control"]
        ),
        SearchDocument(
            2,
            "Flow Check Procedure",
            "A flow check is performed to confirm whether the well is flowing. After shutting down pumps, observe the flow at the flowline. Continued flow indicates a kick. No flow suggests the well is static.",
            ["flow check", "kick detection", "well control"]
        ),
        SearchDocument(
            3,
            "Hard Shut-In vs Soft Shut-In",
            "Hard shut-in involves closing the BOP immediately after detecting a kick, while soft shut-in allows for gradual closure to minimize pressure surges. The chosen method depends on well conditions and company policy.",
            ["shut-in", "BOP", "well control"]
        ),
        SearchDocument(
            4,
            "SIDPP and SICP Interpretation",
            "SIDPP (Shut-In Drill Pipe Pressure) and SICP (Shut-In Casing Pressure) are measured after well shut-in. SIDPP reflects formation pressure minus hydrostatic, while SICP includes annular friction. Both are critical for kill calculations.",
            ["SIDPP", "SICP", "pressure interpretation"]
        ),
        SearchDocument(
            5,
            "Driller's Method: Two Circulation Kill",
            "The Driller's Method uses two circulations: first to remove influx with original mud, second to circulate kill mud weight. It is simple and does not require immediate kill mud preparation.",
            ["driller's method", "well kill", "circulation"]
        ),
        SearchDocument(
            6,
            "Wait and Weight Method",
            "The Wait and Weight Method involves preparing kill mud before circulation. The influx is circulated out in one pass with heavier mud, reducing annular pressures and time to kill the well.",
            ["wait and weight", "well kill", "kill mud"]
        ),
        SearchDocument(
            7,
            "Kill Mud Weight Calculation",
            "Kill mud weight is calculated to balance formation pressure using the formula: KMW = (SIDPP / TVD) * 0.052 + current mud weight. Accurate calculation ensures effective well control.",
            ["kill mud weight", "calculation", "well control"]
        ),
        SearchDocument(
            8,
            "Initial and Final Circulating Pressure",
            "ICP (Initial Circulating Pressure) is the pressure required to circulate kill mud at kill rate. FCP (Final Circulating Pressure) is expected at the end of the kill. Both guide choke adjustments.",
            ["ICP", "FCP", "circulating pressure"]
        ),
        SearchDocument(
            9,
            "Gas Behavior: Boyle's Law and Migration",
            "Boyle's Law describes gas expansion as pressure decreases. During migration, gas expands and rises, increasing surface pressure risk. Understanding gas behavior is vital for safe well control.",
            ["gas behavior", "Boyle's Law", "migration"]
        ),
        SearchDocument(
            10,
            "BOP Stack Components and Function",
            "The Blowout Preventer (BOP) stack includes annular and ram preventers, spools, and valves. Each component serves to seal, control, or divert well fluids during well control operations.",
            ["BOP", "stack", "components"]
        ),
        SearchDocument(
            11,
            "Accumulator System Requirements",
            "Accumulator systems provide hydraulic power to operate BOPs. Sufficient volume and pressure are required to ensure all preventers can be closed in an emergency.",
            ["accumulator", "BOP", "hydraulic system"]
        ),
        SearchDocument(
            12,
            "Underground Blowout",
            "An underground blowout is uncontrolled flow between subsurface formations. It can compromise well integrity and requires specialized intervention techniques.",
            ["underground blowout", "well integrity", "well control"]
        ),
        SearchDocument(
            13,
            "Volumetric Method for Gas Kicks",
            "The volumetric method controls surface pressure while allowing gas to expand and migrate upward. It is used when circulation is not possible, such as with plugged drill pipe.",
            ["volumetric method", "gas kick", "well control"]
        ),
        SearchDocument(
            14,
            "Well Control During Tripping",
            "During tripping, maintain adequate mud level and monitor for swabbing. Use trip sheets and flow checks to detect kicks early and respond appropriately.",
            ["tripping", "kick detection", "well control"]
        ),
        SearchDocument(
            15,
            "Floating Rig Well Control",
            "Floating rigs require consideration of riser margin, heave, and subsea BOPs. Well control procedures must account for dynamic positioning and marine riser systems.",
            ["floating rig", "well control", "marine riser"]
        ),
        SearchDocument(
            16,
            "H2S Well Control Considerations",
            "H2S (hydrogen sulfide) presence requires specialized equipment, procedures, and PPE. Emergency response plans and gas detection systems are mandatory for personnel safety.",
            ["H2S", "well control", "safety"]
        ),
        SearchDocument(
            17,
            "Barrier Philosophy and Well Integrity",
            "Well integrity relies on multiple physical barriers (mud column, casing, BOPs). Barrier philosophy ensures redundancy and systematic verification throughout well operations.",
            ["barrier philosophy", "well integrity", "redundancy"]
        ),
        SearchDocument(
            18,
            "WellCAP and IWCF Certification",
            "WellCAP and IWCF are industry-recognized certifications for well control. They ensure personnel are trained in kick detection, shut-in, and kill procedures.",
            ["WellCAP", "IWCF", "certification"]
        ),
        SearchDocument(
            19,
            "MAASP: Maximum Allowable Annular Surface Pressure",
            "MAASP is the highest pressure that can be safely applied to the annulus without risking formation fracture or equipment failure. It is calculated based on formation strength and casing design.",
            ["MAASP", "annular pressure", "well control"]
        ),
        SearchDocument(
            20,
            "Relief Well Planning",
            "Relief wells are drilled to intersect and control a blowout well. Planning involves trajectory design, kill fluid selection, and coordination with surface response teams.",
            ["relief well", "blowout", "well control"]
        ),
        SearchDocument(
            21,
            "Shallow Gas Hazards",
            "Shallow gas zones present high risk due to low overburden pressure and rapid gas migration. Early detection and appropriate shut-in procedures are critical.",
            ["shallow gas", "hazards", "well control"]
        ),
        SearchDocument(
            22,
            "Choke Management During Kill",
            "Choke management involves adjusting the choke to maintain desired pressures during kill operations. Proper technique prevents pressure surges and formation damage.",
            ["choke management", "kill operations", "well control"]
        ),
        SearchDocument(
            23,
            "Well Control During Connections",
            "During connections, monitor for flow and pit gain. Minimize connection time and perform flow checks to detect kicks before resuming drilling.",
            ["connections", "kick detection", "well control"]
        ),
        SearchDocument(
            24,
            "Bullheading Kill Method",
            "Bullheading involves pumping kill fluid directly down the casing or tubing to force influx back into the formation. It is used when conventional circulation is not possible.",
            ["bullheading", "kill method", "well control"]
        ),
        SearchDocument(
            25,
            "Snubbing and Stripping Operations",
            "Snubbing and stripping allow pipe movement in and out of a pressured well. Specialized equipment and procedures are required to maintain pressure control.",
            ["snubbing", "stripping", "well control"]
        ),
        SearchDocument(
            26,
            "Kick During Casing Operations",
            "Kicks can occur during casing running due to loss of hydrostatic head. Maintain adequate mud returns and monitor for flow to prevent well control incidents.",
            ["casing operations", "kick detection", "well control"]
        ),
        SearchDocument(
            27,
            "Bit Nozzle Plugging During Kill",
            "Plugged bit nozzles can restrict flow and complicate kill operations. Monitor pump pressure and returns, and be prepared to use alternative kill methods if necessary.",
            ["bit nozzle", "plugging", "kill operations"]
        ),
        SearchDocument(
            28,
            "SIMOPS Well Control",
            "Simultaneous operations (SIMOPS) require coordination between drilling, completion, and intervention teams. Clear communication and defined procedures are essential for safe well control.",
            ["SIMOPS", "simultaneous operations", "well control"]
        ),
        SearchDocument(
            29,
            "Driller's Method vs Wait and Weight",
            "Comparison of Driller's Method and Wait and Weight: Driller's is simpler and faster to initiate; Wait and Weight reduces annular pressure and total kill time. Selection depends on crew readiness and equipment.",
            ["driller's method", "wait and weight", "comparison"]
        ),
        SearchDocument(
            30,
            "Well Control Equipment Testing",
            "Regular testing of BOPs, accumulators, and related equipment is required to ensure functionality. Document all tests and address deficiencies before resuming operations.",
            ["equipment testing", "BOP", "well control"]
        ),
        SearchDocument(
            31,
            "Gas Migration Rate Estimation",
            "Estimating gas migration rate is essential for planning well control operations. Factors include formation permeability, gas bubble size, and mud properties.",
            ["gas migration", "estimation", "well control"]
        ),
        SearchDocument(
            32,
            "Choke Line Friction Effects",
            "Choke line friction can increase surface pressure readings during well control. Account for friction loss in kill sheet calculations to avoid underestimating pressures.",
            ["choke line", "friction", "well control"]
        ),
        SearchDocument(
            33,
            "Kick Tolerance Calculation",
            "Kick tolerance is the maximum influx volume that can be safely shut in without exceeding MAASP or fracturing formation. Calculate based on mud weight, formation strength, and casing design.",
            ["kick tolerance", "calculation", "well control"]
        ),
        SearchDocument(
            34,
            "Well Control Drills and Training",
            "Frequent well control drills improve crew readiness for kick detection, shut-in, and kill operations. Training should cover equipment, procedures, and emergency response.",
            ["well control", "drills", "training"]
        ),
        SearchDocument(
            35,
            "Managed Pressure Drilling (MPD) and Well Control",
            "MPD uses surface backpressure and precise mud weight management to control formation pressure. Integration with conventional well control procedures is critical for safety.",
            ["MPD", "managed pressure drilling", "well control"]
        ),
    ]
    for doc in docs:
        idx.add_document(doc)