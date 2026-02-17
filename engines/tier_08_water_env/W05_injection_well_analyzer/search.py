import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Tuple

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str] = None, weight: float = 1.0):
        self.id = id
        self.title = title
        self.content = content
        self.tags = tags or []
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id: str, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

class SearchIndex:
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)  # term -> doc_id -> freq
        self.doc_freqs: Dict[str, int] = defaultdict(int)  # term -> doc freq
        self.N: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[str, str], float] = {}  # (term, doc_id) -> tfidf

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-alphanum, split on whitespace
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_doc_freqs[term][doc.id] = freq
                self.doc_freqs[term] += 1
            self.N += 1
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            )
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        tokens = self._tokenize(doc.content)
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        term_counts = Counter(tokens)
        for term in query_terms:
            if doc_id not in self.term_doc_freqs.get(term, {}):
                continue
            f = self.term_doc_freqs[term][doc_id]
            idf = self._compute_idf(term)
            denom = f + self.bm25_k1 * (
                1 - self.bm25_b + self.bm25_b * doc_len / (self.avg_doc_length or 1.0)
            )
            numer = f * (self.bm25_k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        tokens = self._tokenize(doc.content)
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        term_counts = Counter(tokens)
        for term in query_terms:
            tf = term_counts.get(term, 0) / (doc_len or 1)
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_doc_freqs.get(term, {}).keys())
        scored = []
        for doc_id in candidate_docs:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc.content, query_terms)
                scored.append(SearchResult(doc_id, score, doc.title, snippet))
        scored.sort(key=lambda r: r.score, reverse=True)
        return scored[:limit]

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = tokens[start:end]
        return ' '.join(snippet) + ('...' if end < len(tokens) else '')

    def get_stats(self) -> Dict[str, int]:
        return {
            'num_documents': self.N,
            'avg_doc_length': int(self.avg_doc_length),
            'num_terms': len(self.doc_freqs),
        }

# Singleton factory for SearchIndex
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
            id="1",
            title="UIC Class II Injection Well Permit Requirements",
            content=(
                "Class II injection wells require permits under the EPA's UIC program. "
                "Permit applications must include well construction details, "
                "area of review calculations, mechanical integrity demonstration, "
                "and plans for monitoring and reporting. Compliance with 40 CFR 144-148 is mandatory."
            ),
            tags=["permit", "UIC", "Class II", "EPA"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Injection Pressure Limits and Fracture Gradient",
            content=(
                "Injection pressure must not exceed the fracture gradient of the confining zone. "
                "Operators calculate the maximum allowable injection pressure (MAIP) based on "
                "formation tests and regulatory guidelines to prevent formation fracturing and migration."
            ),
            tags=["pressure", "fracture", "gradient", "MAIP"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Mechanical Integrity Test (MIT) Requirements",
            content=(
                "Mechanical Integrity Tests are required to demonstrate that the well "
                "does not have significant leaks in casing, tubing, or packer, and that "
                "there is no fluid movement behind the casing. MITs include pressure tests, "
                "radioactive tracer surveys, and temperature logs."
            ),
            tags=["MIT", "mechanical integrity", "testing"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Area of Review (AOR) Calculations",
            content=(
                "The Area of Review (AOR) is the region surrounding an injection well "
                "where potential migration of injected fluids is assessed. AOR calculations "
                "consider formation properties, injection rates, and pressure interference. "
                "EPA regulations require periodic reevaluation of the AOR."
            ),
            tags=["AOR", "area of review", "migration"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Well Casing Requirements for Injection Wells",
            content=(
                "Injection wells must have casing designed to withstand injection pressures "
                "and prevent fluid migration. Casing must be properly cemented across all "
                "confining zones. Regular evaluation of casing integrity is required."
            ),
            tags=["casing", "well construction", "integrity"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Cement Bond Evaluation for Injection Wells",
            content=(
                "Cement bond logs are used to evaluate the quality of cementing around well casing. "
                "Good cement bonds prevent fluid migration and maintain well integrity. "
                "Operators must perform cement evaluation logs during well construction and workovers."
            ),
            tags=["cement", "bond", "logs", "evaluation"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Annular Pressure Monitoring Requirements",
            content=(
                "Continuous annular pressure monitoring is required to detect leaks or "
                "loss of mechanical integrity. Operators must report annular pressure "
                "readings and investigate any abnormal pressure changes."
            ),
            tags=["annular", "pressure", "monitoring"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Plugging and Abandonment Requirements",
            content=(
                "Wells must be plugged and abandoned in accordance with EPA regulations "
                "to prevent fluid migration. Plugging plans must include cement plugs, "
                "mechanical plugs, and verification of isolation. Recordkeeping is required."
            ),
            tags=["plugging", "abandonment", "regulations"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="EPA UIC Regulations 40 CFR 144-148 Overview",
            content=(
                "The EPA's Underground Injection Control (UIC) regulations are codified in "
                "40 CFR Parts 144-148. These rules govern permitting, construction, operation, "
                "monitoring, and closure of injection wells to protect underground sources of drinking water."
            ),
            tags=["EPA", "UIC", "regulations", "CFR"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Injection Well Classification (Class I, II, III, IV, V, VI)",
            content=(
                "Injection wells are classified by the EPA into six classes based on "
                "injected fluid type and purpose. Class II wells are used for oil and gas "
                "production, while Class VI wells are for CO2 sequestration."
            ),
            tags=["classification", "Class I", "Class II", "Class VI"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Enhanced Oil Recovery (EOR) Injection Wells",
            content=(
                "EOR wells inject fluids such as water, steam, or CO2 to enhance oil recovery. "
                "Operators must demonstrate formation compatibility and monitor for pressure interference "
                "with nearby wells."
            ),
            tags=["EOR", "enhanced oil recovery", "CO2", "compatibility"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="CO2 Sequestration Class VI Injection Wells",
            content=(
                "Class VI wells are designed for long-term geologic sequestration of CO2. "
                "They require rigorous site characterization, monitoring, and demonstration of "
                "mechanical integrity. EPA regulations require post-injection site care."
            ),
            tags=["CO2", "sequestration", "Class VI"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Formation Compatibility Testing",
            content=(
                "Formation compatibility testing ensures that injected fluids will not react "
                "adversely with formation minerals or fluids. Testing is required for EOR and "
                "CO2 sequestration projects to prevent scaling, precipitation, or corrosion."
            ),
            tags=["formation", "compatibility", "testing"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Injection Rate Optimization",
            content=(
                "Optimizing injection rates maximizes resource recovery while maintaining well integrity. "
                "Operators use reservoir modeling, pressure monitoring, and step-rate tests to determine "
                "optimal injection rates."
            ),
            tags=["injection", "rate", "optimization"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Wellbore Failure Modes and Risk Mitigation",
            content=(
                "Wellbore failure can result from corrosion, mechanical damage, or formation movement. "
                "Risk mitigation includes regular integrity testing, corrosion monitoring, and "
                "proper well design."
            ),
            tags=["wellbore", "failure", "risk", "mitigation"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Corrosion Monitoring in Injection Wells",
            content=(
                "Corrosion monitoring is essential for maintaining well integrity. "
                "Techniques include coupon testing, electrical resistance probes, and fluid analysis. "
                "Operators must take corrective action if corrosion rates exceed thresholds."
            ),
            tags=["corrosion", "monitoring", "integrity"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Injection Well Network Design and Pressure Interference",
            content=(
                "Designing an injection well network requires analysis of pressure interference "
                "between wells. Proper spacing and monitoring prevent unwanted migration and "
                "formation fracturing."
            ),
            tags=["network", "design", "pressure", "interference"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Pressure Interference and Formation Fracture Risk",
            content=(
                "Pressure interference from nearby wells can increase fracture risk. "
                "Operators must monitor injection pressures and adjust rates to avoid exceeding "
                "the fracture gradient of the confining zone."
            ),
            tags=["pressure", "interference", "fracture", "risk"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Injection Well Permit Renewal and Compliance",
            content=(
                "Permit renewal requires demonstration of ongoing compliance with UIC regulations. "
                "Operators must submit updated monitoring data, integrity test results, and "
                "evidence of proper operation and maintenance."
            ),
            tags=["permit", "renewal", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Injection Well Data Reporting Requirements",
            content=(
                "Operators must report injection volumes, pressures, and monitoring results "
                "to regulatory agencies. Data must be accurate, timely, and retained for "
                "the required recordkeeping period."
            ),
            tags=["data", "reporting", "requirements"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Epistemic Gap Detection in Injection Well Analysis",
            content=(
                "Epistemic gap detection identifies areas where knowledge is insufficient "
                "for reliable injection well analysis. Addressing epistemic gaps improves "
                "risk assessment and decision-making."
            ),
            tags=["epistemic", "gap", "detection", "analysis"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Drift Detection in Injection Well Compliance",
            content=(
                "Drift detection involves monitoring for deviations from expected well "
                "performance or compliance metrics. Early detection of drift enables "
                "corrective actions before regulatory violations occur."
            ),
            tags=["drift", "detection", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Injection Well Audit Trail and Recordkeeping",
            content=(
                "Maintaining a complete audit trail and proper recordkeeping is required "
                "for regulatory compliance. Records must include construction, operation, "
                "monitoring, and abandonment activities."
            ),
            tags=["audit", "trail", "recordkeeping"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Injection Well Determinism and Reproducibility",
            content=(
                "Determinism and reproducibility in injection well analysis ensure that "
                "results can be reliably replicated. Standardized procedures and data normalization "
                "are essential for reproducible outcomes."
            ),
            tags=["determinism", "reproducibility", "standardization"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Injection Well Epistemic Guardrails",
            content=(
                "Epistemic guardrails are controls that limit the impact of uncertainty in "
                "injection well analysis. Implementing guardrails improves safety and regulatory compliance."
            ),
            tags=["epistemic", "guardrails", "uncertainty"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Injection Well Semantic Normalization",
            content=(
                "Semantic normalization standardizes terminology and data formats in injection well "
                "analysis. This enables consistent interpretation and comparison of well performance data."
            ),
            tags=["semantic", "normalization", "standardization"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Well Casing and Cementing Best Practices",
            content=(
                "Best practices for casing and cementing include centralizer placement, "
                "proper mud removal, and verification of cement top. These practices "
                "ensure long-term well integrity and regulatory compliance."
            ),
            tags=["casing", "cementing", "best practices"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Class II Well Conversion and Testing",
            content=(
                "Converting existing wells to Class II injection service requires "
                "evaluation of casing, cement, and mechanical integrity. Testing must "
                "demonstrate compliance with UIC requirements prior to injection."
            ),
            tags=["Class II", "conversion", "testing"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Formation Pressure Monitoring Techniques",
            content=(
                "Formation pressure monitoring is performed using downhole gauges, "
                "surface pressure readings, and periodic shut-in tests. Monitoring "
                "ensures that injection does not exceed safe pressure limits."
            ),
            tags=["formation", "pressure", "monitoring"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Plugging Materials and Verification Methods",
            content=(
                "Plugging materials include cement, mechanical plugs, and resins. "
                "Verification methods include tagging plugs, pressure testing, and "
                "cement bond logs to ensure proper isolation."
            ),
            tags=["plugging", "materials", "verification"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)