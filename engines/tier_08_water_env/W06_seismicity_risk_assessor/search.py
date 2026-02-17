import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# --- Data Classes ---

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.term_df: Dict[str, int] = defaultdict(int)
        self.N: int = 0
        self.avgdl: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            tf = Counter(tokens)
            for term, freq in tf.items():
                self.term_doc_freqs[term][doc.id] = freq
            for term in tf.keys():
                self.term_df[term] += 1
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs: Set[str] = set()
        for term in query_terms:
            candidate_docs.update(self.term_doc_freqs.get(term, {}).keys())
        scores: Dict[str, float] = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc_weight = self.documents[doc_id].weight
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            final_score *= doc_weight
            scores[doc_id] = final_score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        return {
            "num_documents": self.N,
            "avg_doc_length": int(self.avgdl),
            "vocab_size": len(self.term_df),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-/\.]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_df.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        tf = Counter(self.doc_tokens[doc_id])
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
            term_score = idf * (f * (self.k1 + 1)) / denom
            score += term_score
        return score

    def _score_tfidf(self, doc_id: str, query_terms: List[str]) -> float:
        tf = Counter(self.doc_tokens[doc_id])
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            tf_norm = f / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:160]
            return snippet + "..." if len(content) > 160 else snippet
        start = max(positions[0] - 8, 0)
        end = min(positions[0] + 12, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Domain Documents ---

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Induced Seismicity Mechanisms Overview",
            content="Induced seismicity refers to earthquakes caused by human activities such as fluid injection, extraction, or reservoir impoundment. Mechanisms include pore pressure diffusion, Coulomb stress transfer, and fault reactivation.",
            tags=["induced seismicity", "mechanisms", "pore pressure", "coulomb stress"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="RRC Seismicity Response Plan Requirements",
            content="The Railroad Commission of Texas (RRC) requires operators to submit a Seismicity Response Plan (SRP) for areas of increased seismic risk. The SRP must outline monitoring, notification, and mitigation protocols.",
            tags=["RRC", "seismicity response plan", "SRP", "regulation"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Traffic Light Protocol for Seismicity Management",
            content="The Traffic Light Protocol (TLP) is a risk management tool using color codes (green, amber, red) to guide operational responses to detected seismicity. Thresholds are based on magnitude and ground motion.",
            tags=["traffic light protocol", "TLP", "risk management"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="TexNet Seismic Monitoring Network",
            content="TexNet is a statewide seismic monitoring network in Texas, providing real-time earthquake data. It supports regulatory decision-making and historical seismicity baseline establishment.",
            tags=["TexNet", "seismic monitoring", "earthquake data"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Establishing a Historical Seismicity Baseline",
            content="A historical seismicity baseline is established by analyzing past earthquake catalogs. This baseline is used to assess changes in seismicity rates and inform risk assessments.",
            tags=["historical seismicity", "baseline", "earthquake catalog"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Gutenberg-Richter b-value Analysis",
            content="The Gutenberg-Richter law describes the frequency-magnitude distribution of earthquakes. The b-value is a key parameter indicating relative proportions of small to large events.",
            tags=["Gutenberg-Richter", "b-value", "frequency-magnitude"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Fault Proximity Assessment for Injection Wells",
            content="Assessing the proximity of injection wells to mapped faults is critical for seismic risk evaluation. Wells near critically stressed faults may require additional mitigation measures.",
            tags=["fault proximity", "injection well", "risk assessment"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Coulomb Stress Transfer in Induced Seismicity",
            content="Coulomb stress transfer quantifies how stress changes from one earthquake or injection event can promote or inhibit failure on nearby faults.",
            tags=["coulomb stress", "stress transfer", "faults"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Pore Pressure Diffusion and Seismicity",
            content="Pore pressure diffusion describes the migration of injected fluids through subsurface formations, potentially triggering fault slip and seismic events.",
            tags=["pore pressure", "diffusion", "fluid injection"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Injection Volume-Seismicity Correlation",
            content="Statistical analyses often reveal correlations between injection volume and seismicity rates, informing operational thresholds and mitigation strategies.",
            tags=["injection volume", "seismicity correlation"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Magnitude-Frequency Relationships in Seismic Hazard",
            content="Magnitude-frequency relationships, such as the Gutenberg-Richter law, are used to estimate the probability of future earthquakes of various sizes.",
            tags=["magnitude-frequency", "seismic hazard"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Seismic Moment Calculations",
            content="Seismic moment is a measure of earthquake size based on fault area, slip, and rigidity. It is used to estimate moment magnitude (Mw).",
            tags=["seismic moment", "moment magnitude", "Mw"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Ground Motion Prediction Equations (GMPEs)",
            content="GMPEs are empirical models that predict ground shaking intensity (PGA, PGV) as a function of magnitude, distance, and site conditions.",
            tags=["GMPE", "PGA", "PGV", "ground motion"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="PGA and PGV Thresholds for Damage Assessment",
            content="Peak Ground Acceleration (PGA) and Peak Ground Velocity (PGV) thresholds are used to assess the potential for structural damage during earthquakes.",
            tags=["PGA", "PGV", "damage assessment"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Building Damage Assessment after Seismic Events",
            content="Post-earthquake building damage assessments involve visual inspections and structural analysis to determine safety and repair needs.",
            tags=["building damage", "assessment", "earthquake"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="RRC Rule 46: Injection Well Compliance",
            content="RRC Rule 46 governs the permitting and operation of injection wells in Texas, including requirements for seismicity monitoring and reporting.",
            tags=["RRC Rule 46", "injection well", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Operator Notification Requirements for Seismic Events",
            content="Operators must notify the RRC and local stakeholders when seismic events exceed regulatory thresholds, as outlined in the Seismicity Response Plan.",
            tags=["operator notification", "seismic event", "regulation"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Injection Rate Reduction Protocols",
            content="Protocols for reducing injection rates are implemented when seismicity exceeds predefined thresholds, aiming to mitigate further earthquake risk.",
            tags=["injection rate", "reduction", "protocol"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Well Suspension Criteria in Response to Seismicity",
            content="Wells may be suspended if seismicity persists or escalates despite mitigation efforts, based on criteria in the Seismicity Response Plan.",
            tags=["well suspension", "criteria", "seismicity"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Seismic Hazard Mapping for Risk Assessment",
            content="Seismic hazard maps display the likelihood of earthquake shaking across a region, supporting risk-informed decision making for infrastructure and operations.",
            tags=["seismic hazard", "mapping", "risk assessment"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Induced Seismicity Case Studies in Texas",
            content="Case studies of induced seismicity in Texas highlight the importance of monitoring, regulatory response, and adaptive management.",
            tags=["case study", "Texas", "induced seismicity"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Real-Time Seismic Monitoring Technologies",
            content="Advances in seismic instrumentation and telemetry enable real-time monitoring of induced seismicity, supporting rapid operational response.",
            tags=["seismic monitoring", "real-time", "instrumentation"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Seismicity Rate Change Detection Methods",
            content="Statistical methods such as CUSUM and moving window analysis are used to detect changes in seismicity rates over time.",
            tags=["seismicity rate", "change detection", "statistics"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Fault Mapping and Characterization",
            content="Accurate mapping and characterization of faults are essential for assessing seismic hazard and designing mitigation strategies.",
            tags=["fault mapping", "characterization", "hazard"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Seismic Hazard Assessment Workflow",
            content="A typical workflow includes data collection, baseline establishment, hazard modeling, and risk communication to stakeholders.",
            tags=["seismic hazard", "workflow", "risk communication"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Microseismic Monitoring for Injection Operations",
            content="Microseismic monitoring detects small magnitude events associated with injection, providing early warning of fault activation.",
            tags=["microseismic", "monitoring", "injection"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Operator Best Practices for Seismicity Mitigation",
            content="Best practices include seismic monitoring, data sharing, adaptive management, and transparent communication with regulators and the public.",
            tags=["best practices", "mitigation", "operator"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Seismicity Data Reporting Standards",
            content="Consistent data reporting standards facilitate regulatory oversight and scientific analysis of induced seismicity.",
            tags=["data reporting", "standards", "regulation"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Injection Well Siting and Design Considerations",
            content="Siting and design of injection wells should consider fault proximity, formation properties, and seismic hazard to minimize risk.",
            tags=["well siting", "design", "seismic hazard"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Seismic Hazard Communication with Stakeholders",
            content="Effective communication of seismic hazard and risk is essential for public trust and regulatory compliance.",
            tags=["hazard communication", "stakeholders", "risk"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)