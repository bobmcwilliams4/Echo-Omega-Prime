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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.inverted_index[term][doc.id] = freq
            self.N = len(self.documents)
            self._recompute_stats = True

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            return 0.0
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        term_counts = Counter(self._tokenize(doc.content))
        for term in query_terms:
            if doc_id not in self.inverted_index.get(term, {}):
                continue
            f = term_counts[term]
            idf = self._compute_idf(term)
            denom = f + k1 * (1 - b + b * doc_len / avgdl)
            score += idf * (f * (k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        term_counts = Counter(self._tokenize(doc.content))
        for term in query_terms:
            tf = term_counts[term] / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def _update_stats(self):
        if not self._recompute_stats:
            return
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.N if self.N > 0 else 0.0
        self.idf_cache.clear()
        self._recompute_stats = False

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        self._update_stats()
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            score = bm25_score + 0.2 * tfidf_score
            snippet = self._make_snippet(self.documents[doc_id], query_terms)
            scored.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + '...' if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + '...'

    def get_stats(self) -> Dict[str, float]:
        self._update_stats()
        return {
            'num_documents': self.N,
            'avg_doc_length': self.avg_doc_length,
            'vocab_size': len(self.inverted_index),
        }

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
        SearchDocument(
            1,
            "Annular Preventer Design and Function",
            "Annular preventers use a flexible sealing element to close around drill pipe, casing, or open hole. Their design allows sealing on irregular shapes, making them versatile in well control. The element is compressed by a piston, expanding radially to seal the wellbore. Annular preventers are commonly used as the uppermost BOP in a stack.",
            ["annular", "preventer", "design", "function", "well control"],
            1.0
        ),
        SearchDocument(
            2,
            "Ram Preventer Types and Applications",
            "Ram preventers use steel rams to seal the wellbore. Types include pipe rams, blind rams, shear rams, and blind-shear rams. Pipe rams seal around drill pipe, blind rams close an open hole, and shear rams cut pipe before sealing. Selection depends on well conditions and operational requirements.",
            ["ram", "preventer", "types", "applications", "well control"],
            1.0
        ),
        SearchDocument(
            3,
            "BOP Testing Protocols Per API RP 53",
            "API RP 53 outlines procedures for testing BOPs, including pressure and function tests. Testing intervals, acceptance criteria, and documentation are specified to ensure BOP reliability. Both surface and subsea stacks must be tested according to these protocols.",
            ["BOP", "testing", "API RP 53", "protocols"],
            1.0
        ),
        SearchDocument(
            4,
            "Accumulator System Design and Sizing",
            "Accumulator systems store hydraulic energy for BOP operation. Sizing is based on the number of BOP functions, required closing force, and regulatory standards. Proper accumulator sizing ensures sufficient energy for multiple BOP operations during well control events.",
            ["accumulator", "system", "design", "sizing", "hydraulic"],
            1.0
        ),
        SearchDocument(
            5,
            "BOP Control Systems: Hydraulic, MUX, Electro-Hydraulic",
            "BOP control systems include hydraulic, multiplexed (MUX), and electro-hydraulic designs. Hydraulic systems use pressurized fluid, MUX systems transmit signals via electrical cables, and electro-hydraulic systems combine both. Selection depends on stack type, water depth, and response time requirements.",
            ["BOP", "control", "systems", "hydraulic", "MUX", "electro-hydraulic"],
            1.0
        ),
        SearchDocument(
            6,
            "Surface BOP Stack Configuration",
            "Surface BOP stacks are arranged on the wellhead and typically include an annular preventer and multiple ram preventers. The configuration is determined by well pressure, expected hazards, and regulatory requirements. Proper stack-up ensures redundancy and operational flexibility.",
            ["surface", "BOP", "stack", "configuration"],
            1.0
        ),
        SearchDocument(
            7,
            "Subsea BOP System Design and Components",
            "Subsea BOP systems are deployed on the seafloor and include a lower marine riser package (LMRP), multiple ram and annular preventers, and control pods. Components are designed for remote operation and high reliability in deepwater environments.",
            ["subsea", "BOP", "system", "design", "components"],
            1.0
        ),
        SearchDocument(
            8,
            "BOP Pressure Ratings and Selection",
            "BOPs are rated for maximum working pressure (MWP), typically ranging from 2,000 to 20,000 psi. Selection is based on maximum anticipated surface pressure (MASP), formation strength, and regulatory standards. Proper rating ensures well control integrity.",
            ["BOP", "pressure", "ratings", "selection"],
            1.0
        ),
        SearchDocument(
            9,
            "Kill Line Operations and Procedures",
            "Kill lines provide a means to pump fluids into the wellbore below the BOP stack. Procedures include pressure testing, line flushing, and monitoring for leaks. Kill line integrity is critical during well control operations.",
            ["kill line", "operations", "procedures", "well control"],
            1.0
        ),
        SearchDocument(
            10,
            "Choke Manifold Design and Operation",
            "Choke manifolds regulate wellbore pressure during well control. Design includes multiple chokes, valves, and pressure gauges to allow controlled flow. Operation requires coordination with BOP functions and monitoring of pressure and flow rates.",
            ["choke", "manifold", "design", "operation", "well control"],
            1.0
        ),
        SearchDocument(
            11,
            "H2S Service BOP Equipment Requirements",
            "BOPs used in H2S service must meet NACE MR0175/ISO 15156 requirements for sour service. Materials are selected for resistance to sulfide stress cracking. Additional safety features include gas detection and emergency shutdown systems.",
            ["H2S", "BOP", "equipment", "requirements", "sour service"],
            1.0
        ),
        SearchDocument(
            12,
            "BOP Failure Modes and Root Cause Analysis",
            "Common BOP failure modes include seal leakage, hydraulic loss, control system malfunction, and mechanical wear. Root cause analysis involves reviewing maintenance records, testing data, and operational history to prevent recurrence.",
            ["BOP", "failure", "modes", "root cause", "analysis"],
            1.0
        ),
        SearchDocument(
            13,
            "Deepwater BOP Considerations and Challenges",
            "Deepwater operations require BOPs with enhanced reliability, remote control, and high-pressure ratings. Challenges include extreme hydrostatic pressure, low temperatures, and limited access for intervention. Redundancy and robust control systems are essential.",
            ["deepwater", "BOP", "considerations", "challenges"],
            1.0
        ),
        SearchDocument(
            14,
            "Cameron vs NOV vs Hydril BOP Comparison",
            "Major BOP manufacturers include Cameron, NOV, and Hydril. Differences include ram design, control system integration, and service support. Selection depends on compatibility, performance, and operator preference.",
            ["Cameron", "NOV", "Hydril", "BOP", "comparison"],
            1.0
        ),
        SearchDocument(
            15,
            "BOP Stack-Up Design for Specific Well Conditions",
            "Stack-up design considers expected pressures, formation fluids, and operational risks. The arrangement of annular and ram preventers, choke and kill lines, and valves is tailored to the well profile and regulatory requirements.",
            ["BOP", "stack-up", "design", "well conditions"],
            1.0
        ),
        SearchDocument(
            16,
            "Diverter Systems for Shallow Gas Hazards",
            "Diverter systems redirect shallow gas away from the rig during drilling. Components include a diverter housing, vent lines, and control valves. Proper operation prevents blowouts and protects personnel and equipment.",
            ["diverter", "systems", "shallow gas", "hazards"],
            1.0
        ),
        SearchDocument(
            17,
            "BOP Maintenance Programs and Intervals",
            "Preventive maintenance ensures BOP reliability. Programs include regular inspection, function testing, and component replacement at defined intervals. Documentation is required for compliance and performance tracking.",
            ["BOP", "maintenance", "programs", "intervals"],
            1.0
        ),
        SearchDocument(
            18,
            "MAASP Calculations and BOP Rating Selection",
            "Maximum Allowable Annular Surface Pressure (MAASP) is calculated based on formation strength, mud weight, and casing design. BOP rating selection must ensure control of the highest anticipated pressure.",
            ["MAASP", "calculations", "BOP", "rating", "selection"],
            1.0
        ),
        SearchDocument(
            19,
            "BOP Control System Redundancy and Deadman Configuration",
            "Redundant control systems and deadman configurations ensure BOP closure in case of primary control loss. Deadman systems automatically close shear rams when communication is lost, providing a last line of defense.",
            ["BOP", "control", "system", "redundancy", "deadman"],
            1.0
        ),
        SearchDocument(
            20,
            "Wellbore Pressure Calculations During Well Control",
            "Accurate wellbore pressure calculations are essential during well control. Factors include mud weight, formation pressure, and friction losses. Monitoring allows timely response to kicks and blowouts.",
            ["wellbore", "pressure", "calculations", "well control"],
            1.0
        ),
        SearchDocument(
            21,
            "BOP Component Leak Detection and Troubleshooting",
            "Leak detection methods include pressure testing, visual inspection, and acoustic monitoring. Troubleshooting involves isolating the leaking component and repairing or replacing seals and valves.",
            ["BOP", "component", "leak detection", "troubleshooting"],
            1.0
        ),
        SearchDocument(
            22,
            "Shear Ram Functionality and Cutting Capability",
            "Shear rams are designed to cut drill pipe and seal the wellbore in emergency situations. Their cutting capability depends on ram design, hydraulic force, and pipe material. Regular testing ensures readiness.",
            ["shear ram", "functionality", "cutting", "BOP"],
            1.0
        ),
        SearchDocument(
            23,
            "Annular Element Wear and Replacement",
            "Annular elements experience wear due to repeated operation and exposure to drilling fluids. Inspection and timely replacement prevent seal failure and maintain well control integrity.",
            ["annular", "element", "wear", "replacement"],
            1.0
        ),
        SearchDocument(
            24,
            "MUX Control Pod Operation in Subsea BOPs",
            "MUX control pods transmit electrical signals to hydraulic actuators on subsea BOPs. They enable rapid, remote operation of BOP functions and support redundancy for reliability in deepwater operations.",
            ["MUX", "control pod", "subsea", "BOP", "operation"],
            1.0
        ),
        SearchDocument(
            25,
            "Choke and Kill Line Integration in BOP Stacks",
            "Choke and kill lines are integrated into BOP stacks to allow controlled circulation and well kill operations. Proper integration ensures accessibility, pressure integrity, and compliance with standards.",
            ["choke", "kill line", "BOP", "integration"],
            1.0
        ),
        SearchDocument(
            26,
            "API RP 53 Documentation and Recordkeeping",
            "API RP 53 requires detailed documentation of BOP tests, maintenance, and operational events. Accurate recordkeeping supports regulatory compliance and incident investigation.",
            ["API RP 53", "documentation", "recordkeeping", "BOP"],
            1.0
        ),
        SearchDocument(
            27,
            "Emergency Disconnect Systems (EDS) in Subsea BOPs",
            "EDS allow rapid disconnection of the marine riser from the BOP stack in emergencies. The system activates shear rams and unlatches the LMRP to protect personnel and the environment.",
            ["emergency disconnect", "EDS", "subsea", "BOP"],
            1.0
        ),
        SearchDocument(
            28,
            "Hydraulic Fluid Selection for BOP Control",
            "Hydraulic fluid for BOP control must be compatible with system materials, provide adequate lubrication, and operate across expected temperature ranges. Fluid selection impacts system reliability and maintenance.",
            ["hydraulic fluid", "BOP", "control", "selection"],
            1.0
        ),
        SearchDocument(
            29,
            "BOP Stack Testing: Low and High Pressure",
            "BOP stack testing includes both low and high pressure tests to verify seal integrity and component performance. Test procedures follow API RP 53 and operator guidelines.",
            ["BOP", "stack testing", "low pressure", "high pressure"],
            1.0
        ),
        SearchDocument(
            30,
            "Subsea BOP Intervention Methods",
            "Intervention methods for subsea BOPs include remotely operated vehicles (ROVs), hot stabs, and control pod replacement. These methods restore BOP functionality during deepwater operations.",
            ["subsea", "BOP", "intervention", "methods"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)