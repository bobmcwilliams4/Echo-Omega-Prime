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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        scores = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25 = self._score_bm25(doc_id, query_tokens)
            tfidf = self._score_tfidf(doc_id, query_tokens)
            # Combine BM25 and TF-IDF (weighted sum, can be tuned)
            final_score = 0.7 * bm25 + 0.3 * tfidf
            if final_score > 0:
                scores[doc_id] = final_score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'num_terms': len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanum, split on whitespace
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

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

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in set(query_tokens):
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            s = idf * (f * (self.k1 + 1)) / (denom or 1)
            score += s
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in set(query_tokens):
            term_tf = tf.get(term, 0)
            if term_tf == 0:
                continue
            tf_norm = term_tf / (doc_len or 1)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        token_positions = {t: [] for t in set(query_tokens)}
        for idx, t in enumerate(tokens):
            if t in token_positions:
                token_positions[t].append(idx)
        all_positions = [pos for positions in token_positions.values() for pos in positions]
        if not all_positions:
            snippet = content[:150]
        else:
            min_pos = min(all_positions)
            start = max(min_pos - window // 2, 0)
            end = min(start + window, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        # Highlight query terms
        for t in set(query_tokens):
            snippet = re.sub(r'\b{}\b'.format(re.escape(t)), f'**{t}**', snippet, flags=re.IGNORECASE)
        return snippet

# Singleton factory
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
            "Two-Phase Separator Design Fundamentals",
            "Covers sizing, retention time, and internals for two-phase oil-gas separators. Includes inlet diverter, mist extractor, and liquid level control.",
            ["separator", "two-phase", "design"],
            1.0
        ),
        SearchDocument(
            2,
            "Three-Phase Separator Sizing and Operation",
            "Design and operation of three-phase separators for oil, water, and gas streams. Discusses weir, interface control, and emulsion handling.",
            ["separator", "three-phase", "design", "operation"],
            1.0
        ),
        SearchDocument(
            3,
            "Heater Treater Emulsion Breaking",
            "Principles of heater treaters for breaking oil-water emulsions. Focus on temperature control, coalescing, and chemical aids.",
            ["heater treater", "emulsion", "breaking"],
            1.0
        ),
        SearchDocument(
            4,
            "Free Water Knockout (FWKO) Residence Time Calculation",
            "FWKO vessel sizing based on required residence time for water separation. Includes API recommendations and field best practices.",
            ["fwko", "residence time", "water separation"],
            1.0
        ),
        SearchDocument(
            5,
            "Gun Barrel Wash Tank Settling Velocity",
            "Design of gun barrel tanks for oil-water separation. Settling velocity, interface control, and skimming methods.",
            ["gun barrel", "wash tank", "settling velocity"],
            1.0
        ),
        SearchDocument(
            6,
            "Stock Tank Atmospheric Storage Design",
            "Atmospheric storage tank sizing, venting, and vapor recovery. API 650/12F standards, thief hatches, and fire safety.",
            ["stock tank", "atmospheric", "storage"],
            1.0
        ),
        SearchDocument(
            7,
            "LACT Unit (Lease Automatic Custody Transfer) Overview",
            "LACT system components: positive displacement pump, BS&W monitor, prover connections, and ticketing. API 6.2 compliance.",
            ["lact", "custody transfer", "bs&w"],
            1.0
        ),
        SearchDocument(
            8,
            "Meter Proving: Coriolis, Turbine, and PD Meters",
            "Procedures for meter proving using Coriolis, turbine, and positive displacement (PD) meters. Includes prover loop setup and data correction.",
            ["meter proving", "coriolis", "turbine", "pd"],
            1.0
        ),
        SearchDocument(
            9,
            "BS&W Measurement Techniques",
            "Basic Sediment & Water (BS&W) measurement using centrifuge, probe, and inline sensors. API 10.4 and field calibration.",
            ["bs&w", "measurement", "centrifuge"],
            1.0
        ),
        SearchDocument(
            10,
            "Vapor Recovery Unit (VRU) Flash Gas Compression",
            "VRU system design for flash gas recovery from tanks. Compressor selection, pressure control, and emissions reduction.",
            ["vru", "flash gas", "compression"],
            1.0
        ),
        SearchDocument(
            11,
            "Tank Gauging: Automatic and Manual Methods",
            "Tank gauging procedures: float & tape, radar, servo, and hydrostatic systems. Strapping tables and volume correction.",
            ["tank gauging", "automatic", "manual"],
            1.0
        ),
        SearchDocument(
            12,
            "Tank Battery Piping Header and Manifold Design",
            "Design of piping headers and manifolds for tank batteries. Includes flow balancing, isolation, and maintenance access.",
            ["piping", "header", "manifold"],
            1.0
        ),
        SearchDocument(
            13,
            "Dump Valve Level Control: Pneumatic and Electric",
            "Dump valve operation for separator and tank level control. Pneumatic pilots, electric actuators, and fail-safe design.",
            ["dump valve", "level control", "pneumatic", "electric"],
            1.0
        ),
        SearchDocument(
            14,
            "Glycol Dehydration: TEG Reboiler and Still Column",
            "Triethylene glycol (TEG) dehydration system design. Reboiler sizing, still column operation, and glycol circulation.",
            ["glycol dehydration", "teg", "reboiler", "still column"],
            1.0
        ),
        SearchDocument(
            15,
            "Amine Sweetening: H2S Removal Contact Tower",
            "Amine sweetening process for H2S removal. Contact tower design, amine circulation, and regeneration.",
            ["amine", "sweetening", "h2s removal", "contact tower"],
            1.0
        ),
        SearchDocument(
            16,
            "Produced Water Treatment: Skim Tank and Flotation",
            "Produced water treatment using skim tanks and dissolved gas flotation. Oil removal efficiency and chemical aids.",
            ["produced water", "skim tank", "flotation"],
            1.0
        ),
        SearchDocument(
            17,
            "Chemical Injection Pump: Methanol and Paraffin Control",
            "Chemical injection pump selection for methanol and paraffin. Sizing, calibration, and maintenance best practices.",
            ["chemical injection", "pump", "methanol", "paraffin"],
            1.0
        ),
        SearchDocument(
            18,
            "Tank Battery Automation: RTU, SCADA, and PLC",
            "Automation of tank batteries using RTU, SCADA, and PLC systems. Remote monitoring, alarms, and control logic.",
            ["automation", "rtu", "scada", "plc"],
            1.0
        ),
        SearchDocument(
            19,
            "Artificial Lift Methods: ESP, Rod Pump, Gas Lift, Plunger",
            "Overview of artificial lift: electric submersible pump (ESP), rod pump, gas lift, and plunger lift. Selection criteria and troubleshooting.",
            ["artificial lift", "esp", "rod pump", "gas lift", "plunger"],
            1.0
        ),
        SearchDocument(
            20,
            "Wellhead Choke Bean: Fixed and Adjustable",
            "Wellhead choke bean types: fixed and adjustable. Sizing, erosion, and flow control strategies.",
            ["wellhead", "choke bean", "fixed", "adjustable"],
            1.0
        ),
        SearchDocument(
            21,
            "Flowline Gathering System Piping Design",
            "Design considerations for flowline gathering systems. Pipe sizing, pressure drop, and corrosion control.",
            ["flowline", "gathering system", "piping"],
            1.0
        ),
        SearchDocument(
            22,
            "Separator Internals: Inlet Diverters and Mist Extractors",
            "Separator internals including inlet diverters, vane packs, and mesh pads for efficient phase separation.",
            ["separator", "internals", "mist extractor"],
            1.0
        ),
        SearchDocument(
            23,
            "Tank Battery Fire Safety and Emergency Response",
            "Fire safety systems for tank batteries. Emergency shutdown, foam systems, and firewater deluge.",
            ["tank battery", "fire safety", "emergency"],
            1.0
        ),
        SearchDocument(
            24,
            "API Standards for Tank Battery Systems",
            "Relevant API standards: 12F, 650, 620, 2000 for tanks; 14C for safety; 21.1 for flow measurement.",
            ["api", "standards", "tank battery"],
            1.0
        ),
        SearchDocument(
            25,
            "Corrosion Monitoring in Tank Battery Piping",
            "Corrosion monitoring techniques: coupons, probes, and ultrasonic testing. Mitigation strategies for piping systems.",
            ["corrosion", "monitoring", "piping"],
            1.0
        ),
        SearchDocument(
            26,
            "Produced Water Disposal and Injection Wells",
            "Produced water disposal options: injection wells, evaporation ponds, and regulatory compliance.",
            ["produced water", "disposal", "injection well"],
            1.0
        ),
        SearchDocument(
            27,
            "Tank Blanketing and Inert Gas Systems",
            "Tank blanketing with nitrogen or other inert gases for vapor space protection and oxygen exclusion.",
            ["tank blanketing", "inert gas", "nitrogen"],
            1.0
        ),
        SearchDocument(
            28,
            "Emulsion Treating Chemicals and Dosage Control",
            "Types of emulsion treating chemicals and dosage control methods for optimal separation.",
            ["emulsion", "chemicals", "dosage"],
            1.0
        ),
        SearchDocument(
            29,
            "Piping Stress Analysis for Tank Batteries",
            "Stress analysis fundamentals for tank battery piping. Expansion loops, supports, and code compliance.",
            ["piping", "stress analysis", "tank battery"],
            1.0
        ),
        SearchDocument(
            30,
            "SCADA Alarm Management for Tank Batteries",
            "Best practices for SCADA alarm management. Prioritization, suppression, and operator response.",
            ["scada", "alarm", "management"],
            1.0
        ),
        SearchDocument(
            31,
            "API 12F Shop-Fabricated Tank Construction",
            "API 12F requirements for shop-fabricated tanks. Design, fabrication, and inspection procedures.",
            ["api 12f", "tank", "fabrication"],
            1.0
        ),
        SearchDocument(
            32,
            "Pressure Relief Devices for Tank Batteries",
            "Pressure relief valves, conservation vents, and rupture disks for tank battery overpressure protection.",
            ["pressure relief", "valve", "vent", "rupture disk"],
            1.0
        ),
        SearchDocument(
            33,
            "Sampling Systems for Oil and Water Quality",
            "Sampling system design for representative oil and water quality analysis. Grab, inline, and automatic samplers.",
            ["sampling", "oil", "water", "quality"],
            1.0
        ),
        SearchDocument(
            34,
            "Tank Battery Electrical Grounding and Bonding",
            "Electrical grounding and bonding requirements for tank batteries. Lightning protection and static dissipation.",
            ["electrical", "grounding", "bonding"],
            1.0
        ),
        SearchDocument(
            35,
            "Field Data Acquisition and Historian Integration",
            "Field data acquisition methods and integration with historian databases for tank battery operations.",
            ["data acquisition", "historian", "integration"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)