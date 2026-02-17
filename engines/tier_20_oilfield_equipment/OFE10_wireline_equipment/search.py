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
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9\-]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_doc_ids = set()
        for term in query_terms:
            for doc_id in self.documents:
                if term in self.term_freqs[doc_id]:
                    candidate_doc_ids.add(doc_id)
        scored = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            combined_score = 0.7 * bm25_score + 0.3 * tfidf_score
            if combined_score > 0:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc, query_terms)
                scored.append(SearchResult(doc_id, combined_score, doc.title, snippet))
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

    def get_stats(self) -> Dict[str, int]:
        return {
            'documents': self.N,
            'unique_terms': len(self.doc_freqs),
            'avg_doc_length': int(self.avg_doc_length),
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

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Slickline Gauge Ring Run Procedure",
            "Step-by-step process for running a gauge ring on slickline. Includes tool string assembly, BHA check, pressure control rig-up, depth correlation, and post-run inspection. Emphasizes safety and well control at all stages.",
            ["slickline", "gauge ring", "procedure", "safety"],
            1.0
        ),
        SearchDocument(
            2,
            "Wireline Pressure Control Equipment Overview",
            "Describes lubricators, stuffing boxes, grease injectors, and quick test subs. Discusses pressure ratings, redress intervals, and compatibility with wellhead equipment for safe wireline operations.",
            ["pressure control", "wireline", "equipment", "lubricator"],
            1.0
        ),
        SearchDocument(
            3,
            "TCP Perforating Gun Systems: Components and Safety",
            "Explains the structure of Tubing Conveyed Perforating (TCP) gun systems, including firing heads, detonation transfer, and safety lockouts. Covers arming procedures and pressure testing.",
            ["TCP", "perforating", "gun", "safety"],
            1.0
        ),
        SearchDocument(
            4,
            "Wireline Logging Tool String Design",
            "Guidelines for assembling logging tool strings: cable head, weak point, CCL, gamma ray, neutron, and resistivity tools. Focus on tool compatibility, length, and weight.",
            ["wireline", "logging", "tool string", "design"],
            1.0
        ),
        SearchDocument(
            5,
            "Bridge Plug Setting Procedures",
            "Detailed steps for setting bridge plugs with wireline: tool string make-up, depth control, setting tool operation, and confirmation of set. Includes troubleshooting common issues.",
            ["bridge plug", "setting", "wireline", "procedure"],
            1.0
        ),
        SearchDocument(
            6,
            "Wireline Fishing and Stuck Tool Recovery",
            "Covers wireline fishing tools: pulling tools, jars, spears, and overshots. Outlines procedures for freeing stuck tools, fishing in deviated wells, and weak point selection.",
            ["wireline", "fishing", "stuck tool", "recovery"],
            1.0
        ),
        SearchDocument(
            7,
            "Wireline Cable Specifications and Weak Points",
            "Discusses wireline cable types (slick, braided, E-line), breaking strengths, weak point ratings, and selection criteria for various operations.",
            ["wireline", "cable", "specifications", "weak point"],
            1.0
        ),
        SearchDocument(
            8,
            "Wireline Truck and Unit Design",
            "Describes truck-mounted and skid-mounted wireline units: winch systems, measuring heads, control cabins, and power requirements. Notes on maintenance and safety features.",
            ["wireline", "truck", "unit", "design"],
            1.0
        ),
        SearchDocument(
            9,
            "Wellbore Deviation Effects on Wireline Operations",
            "Analyzes how well deviation impacts tool conveyance, depth accuracy, and risk of sticking. Recommends deviation limits and mitigation strategies.",
            ["wellbore", "deviation", "wireline", "operations"],
            1.0
        ),
        SearchDocument(
            10,
            "E-Line Cable Head Design and Weak Point Integration",
            "Explains E-line cable head components: electrical connection, mechanical weak point, and pressure integrity. Covers assembly and testing.",
            ["E-line", "cable head", "weak point", "design"],
            1.0
        ),
        SearchDocument(
            11,
            "Memory Tool vs Real-Time Logging Trade-offs",
            "Compares memory logging tools and real-time (surface readout) systems in terms of data quality, operational risk, and cost. Lists scenarios favoring each.",
            ["memory tool", "real-time", "logging", "comparison"],
            1.0
        ),
        SearchDocument(
            12,
            "Perforating Gun Detonation Transfer Systems",
            "Describes transfer systems: detonating cord, boosters, and transfer blocks. Discusses reliability, safety, and troubleshooting misfires.",
            ["perforating gun", "detonation", "transfer", "system"],
            1.0
        ),
        SearchDocument(
            13,
            "Lubricator Pressure Testing Procedure",
            "Stepwise method for pressure testing lubricators before and after wireline runs. Includes pressure ramping, leak checks, and documentation.",
            ["lubricator", "pressure testing", "procedure"],
            1.0
        ),
        SearchDocument(
            14,
            "Grease Injector Maintenance for Wireline",
            "Routine maintenance tasks for grease injectors: seal replacement, pressure checks, and grease selection for different temperature/pressure regimes.",
            ["grease injector", "maintenance", "wireline"],
            1.0
        ),
        SearchDocument(
            15,
            "Wireline Depth Correlation Techniques",
            "Methods for correlating wireline depth: CCL, gamma ray, and marker correlation. Discusses accuracy, calibration, and error sources.",
            ["wireline", "depth", "correlation", "technique"],
            1.0
        ),
        SearchDocument(
            16,
            "Weak Point Selection and Calculation",
            "How to select and calculate weak point ratings based on cable strength, tool weight, and expected overpull. Includes safety factors.",
            ["weak point", "selection", "calculation", "wireline"],
            1.0
        ),
        SearchDocument(
            17,
            "Wireline Safety Lockouts and Interlocks",
            "Overview of mechanical and electrical lockouts in wireline pressure control equipment. Prevents accidental tool drop or firing.",
            ["wireline", "safety", "lockout", "interlock"],
            1.0
        ),
        SearchDocument(
            18,
            "Wireline Unit Power and Hydraulic Systems",
            "Describes power sources (diesel, electric), hydraulic winch operation, and emergency shutdown systems in wireline units.",
            ["wireline", "unit", "power", "hydraulic"],
            1.0
        ),
        SearchDocument(
            19,
            "Bridge Plug Setting Tool Redress",
            "Procedure for redressing bridge plug setting tools: inspection, part replacement, and function testing before next run.",
            ["bridge plug", "setting tool", "redress", "maintenance"],
            1.0
        ),
        SearchDocument(
            20,
            "Wireline Cable Head Electrical Testing",
            "Process for electrical continuity and insulation resistance testing of E-line cable heads. Ensures reliable tool communication.",
            ["wireline", "cable head", "electrical", "testing"],
            1.0
        ),
        SearchDocument(
            21,
            "Wireline Jar Operation and Types",
            "Explains the function of wireline jars, types (hydraulic, mechanical), and best practices for operation and redress.",
            ["wireline", "jar", "operation", "type"],
            1.0
        ),
        SearchDocument(
            22,
            "TCP Gun Arming and Safety Procedures",
            "Covers safe arming of TCP guns, pressure testing, and lockout/tagout steps. Details on arming tools and personnel protection.",
            ["TCP", "gun", "arming", "safety"],
            1.0
        ),
        SearchDocument(
            23,
            "Wireline Cable Lubrication and Handling",
            "Best practices for lubricating and handling wireline cables to prevent corrosion, fatigue, and mechanical damage.",
            ["wireline", "cable", "lubrication", "handling"],
            1.0
        ),
        SearchDocument(
            24,
            "Deviated Well Wireline Tool Conveyance",
            "Techniques for running wireline tools in deviated wells: roller centralizers, tractors, and gravity assist. Discusses risk mitigation.",
            ["deviated well", "wireline", "tool", "conveyance"],
            1.0
        ),
        SearchDocument(
            25,
            "Wireline Tool String Weight Calculation",
            "How to calculate tool string weight for safe wireline operations. Considers buoyancy, cable tension, and maximum overpull.",
            ["wireline", "tool string", "weight", "calculation"],
            1.0
        ),
        SearchDocument(
            26,
            "Wireline Pressure Control Stack Assembly",
            "Assembly sequence for wireline pressure control stack: wellhead adapter, lubricator, grease injector, and quick test sub.",
            ["wireline", "pressure control", "stack", "assembly"],
            1.0
        ),
        SearchDocument(
            27,
            "Memory Logging Tool Battery Management",
            "Guidelines for battery selection, installation, and management in memory logging tools. Includes temperature and run-time considerations.",
            ["memory logging", "tool", "battery", "management"],
            1.0
        ),
        SearchDocument(
            28,
            "Wireline Weak Point Failure Analysis",
            "Common causes of weak point failure: corrosion, fatigue, improper selection. Methods for failure analysis and prevention.",
            ["wireline", "weak point", "failure", "analysis"],
            1.0
        ),
        SearchDocument(
            29,
            "Wireline Tool String Centralization",
            "Importance of centralizing tool strings in deviated wells. Discusses centralizer types and placement strategies.",
            ["wireline", "tool string", "centralization", "deviated well"],
            1.0
        ),
        SearchDocument(
            30,
            "E-Line Surface Readout System Components",
            "Describes surface readout system for E-line: telemetry panel, depth encoder, and data acquisition. Notes on troubleshooting.",
            ["E-line", "surface readout", "system", "component"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)