import math
import threading
import heapq
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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.doc_count: int = 0
        self.total_terms: int = 0
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
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = sum(tf.values())
            self.total_terms += self.doc_lengths[doc.id]
            self.documents[doc.id] = doc
            for term in tf:
                self.inverted_index[term].add(doc.id)
            self.doc_count += 1
            self.avg_doc_length = self.total_terms / self.doc_count if self.doc_count else 0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, []))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.doc_count - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (f * (self.k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_val = tf.get(term, 0) / doc_len if doc_len else 0
            idf = self._compute_idf(term)
            score += tf_val * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs: Set[int] = set()
        for term in query_terms:
            candidate_docs |= self.inverted_index.get(term, set())
        scored: List[Tuple[float, int]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            scored.append((score, doc_id))
        top = heapq.nlargest(limit, scored)
        results = []
        for score, doc_id in top:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], maxlen: int = 180) -> str:
        text = doc.content
        tokens = self._tokenize(text)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = text[:maxlen] + ('...' if len(text) > maxlen else '')
            return snippet
        start = max(positions[0] - 8, 0)
        end = min(start + 32, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        if len(snippet) > maxlen:
            snippet = snippet[:maxlen] + '...'
        return snippet

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'doc_count': self.doc_count,
                'avg_doc_length': self.avg_doc_length,
                'total_terms': self.total_terms,
                'unique_terms': len(self.inverted_index),
            }

# Singleton factory for the search index
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
            1, "Differential Sticking Mechanism",
            "Differential sticking occurs when the drill pipe becomes embedded against the wellbore wall due to pressure differentials. This mechanism is common in permeable formations with high overbalance. Key indicators include inability to move pipe in either direction and normal circulation.",
            ["differential sticking", "mechanism", "stuck pipe"], 1.0
        ),
        SearchDocument(
            2, "Mechanical Pipe Sticking Diagnosis",
            "Mechanical sticking is typically caused by cuttings accumulation, key seats, or wellbore collapse. Diagnosis involves checking for loss of circulation, pipe movement, and sudden increases in drag or torque.",
            ["mechanical sticking", "diagnosis", "stuck pipe"], 1.0
        ),
        SearchDocument(
            3, "Free Point Determination Methods",
            "Free point tools are used to locate the stuck point in the drill string. Methods include mechanical jars, wireline free point indicators, and stretch measurements. Accurate determination is critical for effective fishing operations.",
            ["free point", "fishing", "wireline"], 1.0
        ),
        SearchDocument(
            4, "Hydraulic vs Mechanical Jar Selection",
            "Hydraulic jars provide controlled impact force and are less dependent on operator skill, while mechanical jars offer immediate action but require precise manipulation. Selection depends on well conditions and operator preference.",
            ["hydraulic jar", "mechanical jar", "selection"], 1.0
        ),
        SearchDocument(
            5, "Jar Placement Engineering",
            "Proper jar placement is essential for effective jarring. Placement should consider the stuck point, string length, and jar stroke. Placing the jar too close to the stuck point may reduce effectiveness.",
            ["jar placement", "engineering", "fishing"], 1.0
        ),
        SearchDocument(
            6, "Overshot vs Spear Selection Criteria",
            "Overshots are used for external engagement of fish, while spears are for internal engagement. Selection depends on fish OD, ID, and condition. Overshots are preferred when the top of the fish is accessible.",
            ["overshot", "spear", "selection", "fishing"], 1.0
        ),
        SearchDocument(
            7, "Washover Pipe Operations",
            "Washover pipes are used to free stuck pipe by washing away debris or cement. Operations require careful monitoring of pressure and torque to avoid further sticking or pipe damage.",
            ["washover", "operations", "stuck pipe"], 1.0
        ),
        SearchDocument(
            8, "Junk Mill vs Section Mill Selection",
            "Junk mills are designed for milling up small pieces of metal or junk, while section mills are used to mill out entire sections of casing. Selection is based on the size and type of fish.",
            ["junk mill", "section mill", "selection", "milling"], 1.0
        ),
        SearchDocument(
            9, "Milling Parameters Optimization",
            "Optimizing milling parameters such as weight on bit, rotary speed, and fluid flow improves efficiency and reduces tool wear. Monitor torque and vibration for best results.",
            ["milling", "optimization", "parameters"], 1.0
        ),
        SearchDocument(
            10, "Wireline Fishing Tools and Techniques",
            "Wireline tools include pulling tools, jars, and spears. Techniques involve careful manipulation of the wireline to engage and retrieve the fish. Wireline is ideal for light fishing jobs.",
            ["wireline", "fishing", "tools", "techniques"], 1.0
        ),
        SearchDocument(
            11, "String Shot Backoff Procedures",
            "String shot backoff uses an explosive charge to unscrew the pipe at a predetermined joint. Proper placement and calculation of torque are critical for success.",
            ["string shot", "backoff", "procedures"], 1.0
        ),
        SearchDocument(
            12, "Fish vs Sidetrack Economics",
            "Economic analysis compares the cost of fishing operations versus sidetracking. Factors include lost time, tool cost, and probability of recovery. Sidetracking is considered when fishing becomes uneconomical.",
            ["fish", "sidetrack", "economics"], 1.0
        ),
        SearchDocument(
            13, "Whipstock Sidetrack Operations",
            "Whipstocks are used to initiate sidetracks. Proper orientation and anchoring are essential. Operations require precise measurement and control to avoid wellbore damage.",
            ["whipstock", "sidetrack", "operations"], 1.0
        ),
        SearchDocument(
            14, "Differential Sticking Prevention",
            "Prevention strategies include maintaining low overbalance, using oil-based muds, and minimizing pipe contact with the wellbore. Frequent pipe movement and proper hole cleaning are also effective.",
            ["differential sticking", "prevention", "stuck pipe"], 1.0
        ),
        SearchDocument(
            15, "Key Seat Prevention Strategies",
            "Key seats are narrow grooves in the wellbore that trap pipe. Prevention includes proper hole angle control, reduced dogleg severity, and regular reaming.",
            ["key seat", "prevention", "wellbore"], 1.0
        ),
        SearchDocument(
            16, "Fishing Job Risk Assessment and Planning",
            "Risk assessment evaluates the likelihood of fishing success and potential hazards. Planning includes equipment selection, contingency procedures, and safety measures.",
            ["fishing", "risk assessment", "planning"], 1.0
        ),
        SearchDocument(
            17, "Fishing Tool Safety Joint Application",
            "Safety joints allow for easy disconnection of the fishing assembly if required. Application depends on anticipated downhole conditions and fishing tool design.",
            ["fishing tool", "safety joint", "application"], 1.0
        ),
        SearchDocument(
            18, "Stuck Pipe Spotting Fluids",
            "Spotting fluids are pumped to the stuck point to reduce friction and free the pipe. Selection depends on formation, mud type, and sticking mechanism.",
            ["stuck pipe", "spotting fluids", "fishing"], 1.0
        ),
        SearchDocument(
            19, "Fishing Assembly Design and Makeup",
            "Assembly design considers fish type, well conditions, and tool compatibility. Proper makeup ensures tool strength and minimizes risk of further sticking.",
            ["fishing assembly", "design", "makeup"], 1.0
        ),
        SearchDocument(
            20, "Hydraulic Jar Operation Best Practices",
            "Best practices for hydraulic jar operation include preloading, proper placement, and monitoring jar stroke. Avoid excessive jarring to prevent tool damage.",
            ["hydraulic jar", "operation", "best practices"], 1.0
        ),
        SearchDocument(
            21, "Wireline Free Point Indicator Use",
            "Wireline free point indicators help locate the stuck point by measuring pipe stretch. Accurate use requires calibration and interpretation of readings.",
            ["wireline", "free point", "indicator"], 1.0
        ),
        SearchDocument(
            22, "Overshot Grapple Selection",
            "Grapple selection for overshots depends on fish OD, condition, and engagement length. Proper selection ensures secure retrieval.",
            ["overshot", "grapple", "selection"], 1.0
        ),
        SearchDocument(
            23, "Section Milling for Casing Removal",
            "Section milling removes casing sections for sidetracking or plug installation. Requires careful control of milling parameters and tool selection.",
            ["section mill", "casing removal", "milling"], 1.0
        ),
        SearchDocument(
            24, "Junk Mill Applications",
            "Junk mills are used to grind up small metal debris, bit cones, or junk in the wellbore. Selection depends on debris size and hardness.",
            ["junk mill", "application", "fishing"], 1.0
        ),
        SearchDocument(
            25, "Washover Pipe Selection and Use",
            "Selecting the correct washover pipe involves matching OD/ID to the fish and ensuring sufficient circulation. Use requires monitoring for signs of sticking.",
            ["washover pipe", "selection", "use"], 1.0
        ),
        SearchDocument(
            26, "Fishing Assembly Make-Up Torque",
            "Proper make-up torque is critical to prevent tool back-off or failure during fishing operations. Follow manufacturer recommendations for each tool.",
            ["fishing assembly", "makeup", "torque"], 1.0
        ),
        SearchDocument(
            27, "Wireline Jar Impact Optimization",
            "Optimizing wireline jar impact involves adjusting jar tension, stroke, and release timing. Proper optimization increases retrieval success.",
            ["wireline", "jar", "impact", "optimization"], 1.0
        ),
        SearchDocument(
            28, "Sidetrack Planning and Execution",
            "Sidetrack planning includes wellbore survey, whipstock selection, and trajectory design. Execution requires precise measurement and control.",
            ["sidetrack", "planning", "execution"], 1.0
        ),
        SearchDocument(
            29, "Key Seat Remediation Techniques",
            "Remediation of key seats involves reaming, backreaming, and use of stabilizers. Early detection and correction prevent pipe sticking.",
            ["key seat", "remediation", "techniques"], 1.0
        ),
        SearchDocument(
            30, "Fishing Tool Jar Placement Guidelines",
            "Guidelines for jar placement include considering the stuck point, string length, and jar stroke. Proper placement maximizes jarring effectiveness.",
            ["fishing tool", "jar placement", "guidelines"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)