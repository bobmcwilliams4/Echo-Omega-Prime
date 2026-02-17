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
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            tf_counter = Counter(tokens)
            self.term_freqs[doc.id] = tf_counter
            for term in tf_counter:
                self.term_doc_freq[term] += 1
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self._update_avg_doc_length()

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf_counter = self.term_freqs[doc_id]
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf_counter = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0.0:
                doc_scores.append((doc_id, score))
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in doc_scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._generate_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _generate_snippet(self, content: str, query_terms: List[str], max_length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_length])
            return snippet[:max_length] + ('...' if len(snippet) > max_length else '')
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet[:max_length] + ('...' if len(snippet) > max_length else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

# Singleton Factory
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
            1,
            "Flowback Equipment Configuration",
            "Proper configuration of flowback equipment is critical to ensure safe and efficient operations. Key components include separators, sand traps, chokes, and flow meters. Equipment selection depends on expected flow rates, proppant concentration, and well pressure.",
            ["equipment", "configuration", "flowback"],
            1.0
        ),
        SearchDocument(
            2,
            "Choke Management Strategy: Aggressive vs Conservative",
            "Choke management during flowback can follow aggressive or conservative strategies. Aggressive choke opening increases initial production but may risk proppant flowback and formation damage. Conservative choke management prioritizes well integrity and gradual load recovery.",
            ["choke", "strategy", "aggressive", "conservative"],
            1.0
        ),
        SearchDocument(
            3,
            "Flowback Data Acquisition and Monitoring",
            "Continuous data acquisition during flowback includes pressure, temperature, flow rate, and sand production monitoring. Real-time data enables optimization of choke settings and early detection of operational issues.",
            ["data", "monitoring", "flowback"],
            1.0
        ),
        SearchDocument(
            4,
            "Load Recovery Calculations and Optimization",
            "Load recovery is calculated by measuring recovered fluid volumes versus injected volumes. Optimization involves balancing recovery rate with proppant retention and formation protection.",
            ["load", "recovery", "optimization"],
            1.0
        ),
        SearchDocument(
            5,
            "Proppant Flowback Prevention and Management",
            "Preventing proppant flowback requires proper equipment, choke management, and chemical additives. Sand traps and screens capture proppant, while surfactants and polymers stabilize the fracture network.",
            ["proppant", "flowback", "prevention"],
            1.0
        ),
        SearchDocument(
            6,
            "Flowback Water Quality and Chemistry",
            "Water quality during flowback affects downstream processing and disposal. Key parameters include TDS, pH, hardness, and presence of hydrocarbons. Chemistry adjustments may be needed for recycling or disposal.",
            ["water", "quality", "chemistry"],
            1.0
        ),
        SearchDocument(
            7,
            "Flare Operations and EPA Methane Regulations",
            "Flare operations during flowback must comply with EPA methane regulations. Monitoring flare efficiency and emissions is essential to minimize environmental impact and regulatory risk.",
            ["flare", "EPA", "methane", "regulations"],
            1.0
        ),
        SearchDocument(
            8,
            "Water Disposal and Recycling Planning",
            "Effective planning for water disposal and recycling reduces environmental footprint and operational costs. Options include injection wells, evaporation, and onsite treatment for reuse.",
            ["water", "disposal", "recycling"],
            1.0
        ),
        SearchDocument(
            9,
            "Initial Production (IP) Rate Determination",
            "IP rate is determined by measuring flow rates during early production. Accurate IP calculation informs reservoir performance and future development planning.",
            ["IP", "production", "rate"],
            1.0
        ),
        SearchDocument(
            10,
            "Surfactant-Assisted Flowback",
            "Surfactants are used to enhance flowback by reducing surface tension and improving fluid mobility. Selection of surfactant type and concentration is based on reservoir characteristics.",
            ["surfactant", "flowback", "enhancement"],
            1.0
        ),
        SearchDocument(
            11,
            "Nitrogen-Assisted Flowback",
            "Nitrogen injection during flowback increases pressure and aids in fluid recovery. Nitrogen-assisted flowback is particularly useful in low-pressure reservoirs.",
            ["nitrogen", "flowback", "recovery"],
            1.0
        ),
        SearchDocument(
            12,
            "Formation Damage Prevention During Flowback",
            "Preventing formation damage involves controlling flow rates, minimizing proppant movement, and using compatible fluids. Monitoring for pressure anomalies helps detect early signs of damage.",
            ["formation", "damage", "prevention"],
            1.0
        ),
        SearchDocument(
            13,
            "Separator Selection for Flowback Operations",
            "Choosing the right separator for flowback operations depends on expected fluid composition and flow rates. Three-phase separators are preferred when both oil and gas are present.",
            ["separator", "selection", "flowback"],
            1.0
        ),
        SearchDocument(
            14,
            "Sand Trap Design and Maintenance",
            "Sand traps are essential for capturing proppant during flowback. Regular maintenance ensures efficient operation and prevents equipment wear.",
            ["sand", "trap", "maintenance"],
            1.0
        ),
        SearchDocument(
            15,
            "Choke Sizing and Adjustment Best Practices",
            "Proper choke sizing and adjustment optimize flowback rates and minimize formation damage. Automated choke systems allow for precise control and real-time adjustments.",
            ["choke", "sizing", "adjustment"],
            1.0
        ),
        SearchDocument(
            16,
            "Real-Time Flowback Data Analytics",
            "Advanced analytics of real-time flowback data enable predictive maintenance and operational optimization. Machine learning models can forecast sand production and pressure trends.",
            ["data", "analytics", "flowback"],
            1.0
        ),
        SearchDocument(
            17,
            "Load Recovery Curve Interpretation",
            "Interpreting load recovery curves helps identify optimal flowback strategies and potential formation issues. Curve analysis is integrated with pressure and sand production data.",
            ["load", "recovery", "curve"],
            1.0
        ),
        SearchDocument(
            18,
            "Proppant Retention Technologies",
            "Technologies for proppant retention include resin-coated proppants, fiber additives, and mechanical screens. Selection depends on reservoir conditions and desired production profile.",
            ["proppant", "retention", "technology"],
            1.0
        ),
        SearchDocument(
            19,
            "Water Chemistry Adjustment for Flowback Recycling",
            "Adjusting water chemistry for flowback recycling involves pH balancing, hardness reduction, and removal of organic contaminants. Proper treatment ensures compatibility with future fracturing operations.",
            ["water", "chemistry", "recycling"],
            1.0
        ),
        SearchDocument(
            20,
            "EPA Compliance Checklist for Flowback Operations",
            "EPA compliance during flowback includes monitoring methane emissions, reporting flare volumes, and maintaining proper records. Regular audits ensure adherence to regulations.",
            ["EPA", "compliance", "flowback"],
            1.0
        ),
        SearchDocument(
            21,
            "Water Disposal Cost Optimization",
            "Optimizing water disposal costs involves selecting the most economical disposal method, negotiating contracts, and minimizing transportation expenses.",
            ["water", "disposal", "cost"],
            1.0
        ),
        SearchDocument(
            22,
            "IP Rate Forecasting Models",
            "Forecasting IP rates uses historical flowback data, reservoir properties, and statistical models. Accurate forecasts guide investment and operational decisions.",
            ["IP", "rate", "forecasting"],
            1.0
        ),
        SearchDocument(
            23,
            "Surfactant Selection Criteria for Flowback",
            "Criteria for surfactant selection include compatibility with reservoir fluids, effectiveness in reducing surface tension, and environmental impact.",
            ["surfactant", "selection", "criteria"],
            1.0
        ),
        SearchDocument(
            24,
            "Nitrogen Injection Safety Protocols",
            "Safety protocols for nitrogen injection include monitoring pressure, ensuring proper equipment, and training personnel. Emergency shutdown procedures must be established.",
            ["nitrogen", "injection", "safety"],
            1.0
        ),
        SearchDocument(
            25,
            "Formation Damage Detection Techniques",
            "Techniques for detecting formation damage during flowback include pressure transient analysis, tracer studies, and microseismic monitoring.",
            ["formation", "damage", "detection"],
            1.0
        ),
        SearchDocument(
            26,
            "Automated Flowback Equipment Monitoring",
            "Automated monitoring systems track flow rates, sand production, and equipment status. Integration with SCADA platforms enables remote operation and alerts.",
            ["equipment", "monitoring", "automation"],
            1.0
        ),
        SearchDocument(
            27,
            "Choke Management Impact on Proppant Flowback",
            "Choke management directly impacts proppant flowback rates. Gradual choke opening reduces sand production and improves well longevity.",
            ["choke", "proppant", "management"],
            1.0
        ),
        SearchDocument(
            28,
            "Flowback Water Quality Monitoring Technologies",
            "Technologies for monitoring flowback water quality include inline sensors, laboratory analysis, and remote data transmission.",
            ["water", "quality", "monitoring"],
            1.0
        ),
        SearchDocument(
            29,
            "EPA Methane Emission Reporting Requirements",
            "Methane emission reporting during flowback must follow EPA guidelines. Accurate measurement and documentation are required for compliance.",
            ["EPA", "methane", "reporting"],
            1.0
        ),
        SearchDocument(
            30,
            "Water Recycling System Design",
            "Designing water recycling systems for flowback involves capacity planning, treatment technology selection, and integration with existing infrastructure.",
            ["water", "recycling", "design"],
            1.0
        ),
        SearchDocument(
            31,
            "Optimizing Initial Production Rate with Choke Management",
            "Optimizing IP rate requires careful choke management, balancing flow rates with proppant retention and formation protection.",
            ["IP", "choke", "optimization"],
            1.0
        ),
        SearchDocument(
            32,
            "Surfactant Application Methods in Flowback",
            "Surfactant application methods include batch injection, continuous dosing, and post-fracture treatment. Method selection depends on operational goals.",
            ["surfactant", "application", "methods"],
            1.0
        ),
        SearchDocument(
            33,
            "Nitrogen-Assisted Flowback in Tight Formations",
            "Nitrogen-assisted flowback is effective in tight formations, enhancing fluid recovery and reducing formation damage.",
            ["nitrogen", "tight", "formation"],
            1.0
        ),
        SearchDocument(
            34,
            "Formation Damage Prevention Chemicals",
            "Chemical additives for formation damage prevention include scale inhibitors, biocides, and friction reducers. Selection is based on reservoir chemistry.",
            ["formation", "damage", "chemicals"],
            1.0
        ),
        SearchDocument(
            35,
            "Sand Management During Flowback Operations",
            "Sand management involves capturing, monitoring, and disposing of proppant during flowback. Efficient sand handling reduces equipment wear and environmental risk.",
            ["sand", "management", "flowback"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)