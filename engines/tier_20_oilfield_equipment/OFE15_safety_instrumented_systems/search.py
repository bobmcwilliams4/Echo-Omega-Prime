import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._total_docs: int = 0
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            self._doc_lengths[doc.id] = len(tokens)
            for token in set(tokens):
                self._inverted_index[token].add(doc.id)
                self._doc_freqs[token] += 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self._inverted_index.get(token, set()))
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc = self._documents[doc_id]
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            combined_score *= doc.weight
            scored_results.append((doc_id, combined_score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_documents": self._total_docs,
                "avg_doc_length": self._avg_doc_length,
                "unique_terms": len(self._inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]{2,}\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self._total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        doc_tokens = self._doc_tokens[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        term_freqs = Counter(doc_tokens)
        for term in query_tokens:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / self._avg_doc_length)
            score += idf * (tf * (self._bm25_k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        doc_tokens = self._doc_tokens[doc_id]
        doc_len = self._doc_lengths[doc_id]
        term_freqs = Counter(doc_tokens)
        score = 0.0
        for term in query_tokens:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], length: int = 160) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for token in query_tokens:
            idx = content_lower.find(token)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(min(positions) - 30, 0)
        else:
            start = 0
        snippet = content[start:start + length]
        if len(snippet) < len(content):
            snippet += "..."
        return snippet

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seeded Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "SIL Determination Using Risk Graph Method",
            "The risk graph method is a qualitative approach to determine the required Safety Integrity Level (SIL) for a Safety Instrumented Function (SIF). It considers factors such as consequence, frequency, probability of failure, and the possibility of avoiding the hazard.",
            ["SIL", "risk graph", "SIF", "IEC 61511"],
            1.0
        ),
        SearchDocument(
            2,
            "1oo1, 1oo2, 2oo3 Safety PLC Architectures",
            "Comparison of Safety PLC architectures: 1oo1 (one out of one), 1oo2 (one out of two), and 2oo3 (two out of three). 1oo2 and 2oo3 architectures provide higher fault tolerance and lower Probability of Failure on Demand (PFD) than 1oo1.",
            ["Safety PLC", "architecture", "1oo1", "1oo2", "2oo3"],
            1.0
        ),
        SearchDocument(
            3,
            "Designing ESD System Cause and Effect Matrix",
            "A Cause and Effect Matrix defines the logic for Emergency Shutdown (ESD) systems. It maps input signals (causes) to output actions (effects), ensuring correct system response to hazardous events.",
            ["ESD", "cause and effect", "matrix", "shutdown"],
            1.0
        ),
        SearchDocument(
            4,
            "Fire and Gas Detection: Detector Types and Coverage",
            "Fire and Gas Detection Systems use various detector types: flame, smoke, heat, and gas detectors. Coverage studies ensure detectors are optimally placed for maximum risk reduction.",
            ["fire and gas", "detector", "coverage", "safety"],
            1.0
        ),
        SearchDocument(
            5,
            "Pressure Safety Valve Sizing per API 520/521",
            "API 520 and API 521 provide guidelines for sizing and selection of Pressure Safety Valves (PSVs), considering set pressure, overpressure, and required relief rates.",
            ["PSV", "API 520", "API 521", "sizing"],
            1.0
        ),
        SearchDocument(
            6,
            "HIPPS as PSV Alternative",
            "High Integrity Pressure Protection Systems (HIPPS) can be used as an alternative to traditional PSVs to prevent overpressure by shutting off the source before relief is required.",
            ["HIPPS", "PSV", "pressure protection"],
            1.0
        ),
        SearchDocument(
            7,
            "Proof Test Intervals and PFD Calculation",
            "Proof test intervals directly affect the average Probability of Failure on Demand (PFDavg) for a SIF. Shorter intervals reduce PFDavg, improving SIL verification.",
            ["proof test", "PFD", "SIL", "verification"],
            1.0
        ),
        SearchDocument(
            8,
            "Functional Safety Management per IEC 61511",
            "IEC 61511 requires a Functional Safety Management (FSM) plan covering all lifecycle phases: hazard analysis, design, operation, maintenance, and decommissioning.",
            ["FSM", "IEC 61511", "lifecycle"],
            1.0
        ),
        SearchDocument(
            9,
            "SIF Validation Testing: FAT and SAT",
            "SIFs must be validated through Factory Acceptance Testing (FAT) and Site Acceptance Testing (SAT) to ensure all safety requirements are met before operation.",
            ["SIF", "FAT", "SAT", "validation"],
            1.0
        ),
        SearchDocument(
            10,
            "Common Cause Failure and Beta Factor Estimation",
            "Common cause failures (CCF) are failures affecting multiple channels simultaneously. The beta factor method estimates the proportion of failures due to CCF in redundant systems.",
            ["common cause", "failure", "beta factor"],
            1.0
        ),
        SearchDocument(
            11,
            "Layer of Protection Analysis (LOPA) in SIL Assignment",
            "LOPA is a semi-quantitative method to determine SIL by evaluating independent protection layers and their risk reduction capabilities.",
            ["LOPA", "SIL", "protection layers"],
            1.0
        ),
        SearchDocument(
            12,
            "Redundancy and Diversity in Safety Instrumented Systems",
            "Redundancy (e.g., 1oo2, 2oo3) and diversity (using different technologies) enhance system reliability and reduce common cause failures.",
            ["redundancy", "diversity", "SIS"],
            1.0
        ),
        SearchDocument(
            13,
            "Voting Logic in Safety PLCs",
            "Voting logic (e.g., 1oo2, 2oo3) determines how many channels must agree before a safety action is taken. Higher voting increases fault tolerance.",
            ["voting logic", "PLC", "safety"],
            1.0
        ),
        SearchDocument(
            14,
            "SIL Verification: PFDavg Calculation Example",
            "To verify SIL, calculate the average Probability of Failure on Demand (PFDavg) using failure rates, test intervals, and architecture factors.",
            ["SIL", "PFDavg", "verification"],
            1.0
        ),
        SearchDocument(
            15,
            "Fire and Gas Mapping Study",
            "A Fire and Gas Mapping Study determines optimal detector placement to achieve required coverage and risk reduction targets.",
            ["fire and gas", "mapping", "coverage"],
            1.0
        ),
        SearchDocument(
            16,
            "Proof Test Coverage and Effectiveness",
            "Proof test coverage is the proportion of dangerous failures detected by proof testing. High coverage improves SIL verification confidence.",
            ["proof test", "coverage", "SIL"],
            1.0
        ),
        SearchDocument(
            17,
            "SIS Lifecycle Management",
            "Managing the SIS lifecycle per IEC 61511 includes hazard identification, risk assessment, design, implementation, operation, and decommissioning.",
            ["SIS", "lifecycle", "IEC 61511"],
            1.0
        ),
        SearchDocument(
            18,
            "SIF Functional Testing Requirements",
            "Functional testing of SIFs ensures all logic and outputs perform as intended under simulated process conditions.",
            ["SIF", "functional testing"],
            1.0
        ),
        SearchDocument(
            19,
            "ESD System Trip Matrix Example",
            "An ESD Trip Matrix shows how process conditions trigger shutdown actions, supporting safe plant operation.",
            ["ESD", "trip matrix", "shutdown"],
            1.0
        ),
        SearchDocument(
            20,
            "Gas Detector Types: Point, Open Path, Ultrasonic",
            "Point gas detectors measure concentration at a location, open path detectors monitor a beam, and ultrasonic detectors sense leaks by sound.",
            ["gas detector", "point", "open path", "ultrasonic"],
            1.0
        ),
        SearchDocument(
            21,
            "Pressure Relief System Design per API 521",
            "API 521 covers design of pressure relief systems, including scenario identification, relief load calculation, and disposal system sizing.",
            ["pressure relief", "API 521", "design"],
            1.0
        ),
        SearchDocument(
            22,
            "HIPPS SIF Design Considerations",
            "HIPPS SIFs require fast response, high reliability, and must meet SIL requirements for overpressure protection.",
            ["HIPPS", "SIF", "design"],
            1.0
        ),
        SearchDocument(
            23,
            "Proof Test Interval Optimization",
            "Optimizing proof test intervals balances maintenance effort and SIL verification by minimizing PFDavg while considering operational constraints.",
            ["proof test", "interval", "optimization"],
            1.0
        ),
        SearchDocument(
            24,
            "IEC 61511 Functional Safety Lifecycle Phases",
            "IEC 61511 defines phases: concept, hazard and risk assessment, allocation, design, implementation, operation, maintenance, and decommissioning.",
            ["IEC 61511", "lifecycle", "phases"],
            1.0
        ),
        SearchDocument(
            25,
            "SIL Target Selection for SIFs",
            "SIL targets for SIFs are selected based on risk reduction requirements determined through risk assessment methods such as risk graphs or LOPA.",
            ["SIL", "SIF", "risk assessment"],
            1.0
        ),
        SearchDocument(
            26,
            "Beta Factor Method for Common Cause Failure",
            "The beta factor method quantifies the percentage of failures in redundant channels due to common cause, impacting overall system reliability.",
            ["beta factor", "common cause", "redundancy"],
            1.0
        ),
        SearchDocument(
            27,
            "Factory Acceptance Test (FAT) Checklist for SIFs",
            "A FAT checklist for SIFs includes logic verification, input/output simulation, and documentation review to ensure compliance with safety requirements.",
            ["FAT", "SIF", "checklist"],
            1.0
        ),
        SearchDocument(
            28,
            "Site Acceptance Test (SAT) for Safety Systems",
            "SAT verifies safety system performance in the installed environment, including field device integration and system response to simulated faults.",
            ["SAT", "safety system", "testing"],
            1.0
        ),
        SearchDocument(
            29,
            "Diversity in Fire and Gas Detection",
            "Using diverse detector types (e.g., flame, gas, smoke) reduces the likelihood of common cause failures in fire and gas systems.",
            ["diversity", "fire and gas", "detection"],
            1.0
        ),
        SearchDocument(
            30,
            "SIL Verification Report Contents",
            "A SIL verification report documents calculations, assumptions, and test results supporting the assigned SIL for each SIF.",
            ["SIL", "verification", "report"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)