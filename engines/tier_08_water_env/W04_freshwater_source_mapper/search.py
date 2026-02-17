import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

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
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        avgdl = self.avg_doc_length
        doc = self.documents[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_length / avgdl)
            score += idf * (f * (self.k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        doc = self.documents[doc_id]
        for term in query_terms:
            key = (doc_id, term)
            if key in self._tfidf_cache:
                tfidf = self._tfidf_cache[key]
            else:
                tf_raw = tf.get(term, 0)
                tf_norm = tf_raw / doc_length if doc_length > 0 else 0
                idf = self._compute_idf(term)
                tfidf = tf_norm * idf
                self._tfidf_cache[key] = tfidf
            score += tfidf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores = []
        for doc_id in self.documents:
            if use_bm25:
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(doc_id, query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str], maxlen: int = 160) -> str:
        doc = self.documents[doc_id]
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:maxlen]
            if len(content) > maxlen:
                snippet += "..."
            return snippet
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        if len(snippet) > maxlen:
            snippet = snippet[:maxlen] + "..."
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_length,
            "vocab_size": len(self.doc_freqs),
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
            1,
            "Ogallala Aquifer: Source Viability for Frac Operations",
            "The Ogallala Aquifer, spanning multiple states, is a major groundwater source for hydraulic fracturing. Viability depends on local recharge rates, water table depth, and regulatory restrictions. Operators must assess drawdown impacts and sustainability before sourcing water for frac operations.",
            ["Ogallala", "Frac", "Viability", "Hydrogeology"],
            1.0
        ),
        SearchDocument(
            2,
            "Pecos Valley Aquifer: Regulatory and Hydrogeologic Constraints",
            "Frac water sourcing from the Pecos Valley Aquifer is subject to state and local regulations. Hydrogeologic constraints include variable transmissivity and potential for induced drawdown. Permitting requires detailed hydrogeologic studies and compliance with conservation district rules.",
            ["Pecos Valley", "Regulation", "Hydrogeology", "Permitting"],
            1.0
        ),
        SearchDocument(
            3,
            "Edwards-Trinity Aquifer: Legal and Quality Considerations",
            "The Edwards-Trinity Aquifer presents legal complexities due to overlapping water rights and groundwater districts. Water quality, particularly TDS and hardness, may limit direct use for frac operations without treatment.",
            ["Edwards-Trinity", "Legal", "Water Quality", "TDS"],
            1.0
        ),
        SearchDocument(
            4,
            "Dockum Aquifer: Suitability and Regulatory Barriers",
            "Dockum Aquifer water is often brackish, posing challenges for frac use. Regulatory barriers include production limits and required blending or treatment. Operators must navigate GCD rules and demonstrate non-impairment of existing wells.",
            ["Dockum", "Suitability", "Regulatory", "Brackish"],
            1.0
        ),
        SearchDocument(
            5,
            "Santa Rosa Aquifer: Freshwater Sourcing and Drought Resilience",
            "The Santa Rosa Aquifer is an important freshwater source with moderate drought resilience. Sourcing for frac operations requires evaluation of seasonal recharge and potential impacts on municipal supply.",
            ["Santa Rosa", "Freshwater", "Drought", "Frac"],
            1.0
        ),
        SearchDocument(
            6,
            "TWDB Freshwater Well Permitting: Process and Pitfalls",
            "The Texas Water Development Board (TWDB) oversees freshwater well permitting. The process involves hydrogeologic assessment, public notice, and compliance with spacing and production requirements. Common pitfalls include incomplete applications and failure to address local GCD rules.",
            ["TWDB", "Permitting", "Well", "Process"],
            1.0
        ),
        SearchDocument(
            7,
            "GCD Production Limits: Enforcement and Variance",
            "Groundwater Conservation Districts (GCDs) set production limits to manage aquifer withdrawals. Enforcement mechanisms include metering, reporting, and penalties. Variance requests must demonstrate non-impairment and public benefit.",
            ["GCD", "Production Limits", "Enforcement", "Variance"],
            1.0
        ),
        SearchDocument(
            8,
            "Water Quality Parameters: TDS and Hardness for Frac Use",
            "Total Dissolved Solids (TDS) and hardness are critical parameters for frac water. High TDS can cause scaling and reduce frac fluid effectiveness. Operators must test and treat water to meet operational standards.",
            ["Water Quality", "TDS", "Hardness", "Frac"],
            1.0
        ),
        SearchDocument(
            9,
            "Seasonal Availability: Aquifer Response to Drought",
            "Aquifer water levels fluctuate seasonally and respond to drought conditions. Operators must plan for reduced availability during extended dry periods and monitor water table trends.",
            ["Seasonal", "Drought", "Aquifer", "Availability"],
            1.0
        ),
        SearchDocument(
            10,
            "Drought Index Correlation: Predictive Planning",
            "Drought indices, such as the Palmer Drought Severity Index, correlate with aquifer recharge and availability. Predictive planning uses these indices to forecast frac water sourcing risks.",
            ["Drought", "Index", "Planning", "Forecast"],
            1.0
        ),
        SearchDocument(
            11,
            "Frac Water Quality Requirements: Regulatory and Operational Standards",
            "Regulatory standards for frac water quality include limits on TDS, hardness, and bacteria. Operational standards may be more stringent, requiring advanced treatment and monitoring.",
            ["Frac", "Water Quality", "Regulation", "Standards"],
            1.0
        ),
        SearchDocument(
            12,
            "Ogallala Aquifer Recharge and Sustainability",
            "Recharge rates in the Ogallala Aquifer are low, making sustainability a key concern for frac operations. Long-term withdrawals can lead to significant declines in water levels.",
            ["Ogallala", "Recharge", "Sustainability", "Frac"],
            1.0
        ),
        SearchDocument(
            13,
            "Pecos Valley Aquifer: Induced Drawdown and Management",
            "Large-scale frac water withdrawals from the Pecos Valley Aquifer can induce drawdown, affecting nearby wells. Management strategies include staged pumping and aquifer monitoring.",
            ["Pecos Valley", "Drawdown", "Management", "Monitoring"],
            1.0
        ),
        SearchDocument(
            14,
            "Edwards-Trinity Aquifer: Groundwater District Jurisdictions",
            "Multiple groundwater districts overlap the Edwards-Trinity Aquifer, complicating permitting and management. Coordination is essential to avoid legal conflicts.",
            ["Edwards-Trinity", "Districts", "Jurisdiction", "Permitting"],
            1.0
        ),
        SearchDocument(
            15,
            "Dockum Aquifer: Blending Strategies for Frac Water",
            "Blending Dockum Aquifer water with fresher sources can reduce TDS and hardness to acceptable levels for frac operations. Blending ratios must be calculated based on water quality data.",
            ["Dockum", "Blending", "TDS", "Frac"],
            1.0
        ),
        SearchDocument(
            16,
            "Santa Rosa Aquifer: Municipal Supply and Competing Demands",
            "Municipal supply from the Santa Rosa Aquifer may compete with industrial frac water demands. Stakeholder engagement and impact assessments are required.",
            ["Santa Rosa", "Municipal", "Competing", "Frac"],
            1.0
        ),
        SearchDocument(
            17,
            "TWDB Permitting: Hydrogeologic Assessment Requirements",
            "TWDB requires detailed hydrogeologic assessments for new freshwater wells, including aquifer tests and water quality sampling.",
            ["TWDB", "Permitting", "Hydrogeology", "Assessment"],
            1.0
        ),
        SearchDocument(
            18,
            "GCD Enforcement: Metering and Reporting",
            "GCDs enforce production limits through metering and mandatory reporting. Failure to comply can result in fines or permit revocation.",
            ["GCD", "Enforcement", "Metering", "Reporting"],
            1.0
        ),
        SearchDocument(
            19,
            "Water Quality: Bacteria and Disinfection Requirements",
            "Bacterial contamination in frac water can cause operational issues. Disinfection is required to meet regulatory and operational standards.",
            ["Water Quality", "Bacteria", "Disinfection", "Frac"],
            1.0
        ),
        SearchDocument(
            20,
            "Seasonal Variability: Frac Water Sourcing Strategies",
            "Seasonal variability in aquifer levels requires flexible frac water sourcing strategies, including storage and alternative supplies.",
            ["Seasonal", "Variability", "Frac", "Sourcing"],
            1.0
        ),
        SearchDocument(
            21,
            "Drought Planning: Use of Drought Indices",
            "Operators use drought indices to inform frac water sourcing plans and mitigate supply risks during dry periods.",
            ["Drought", "Planning", "Indices", "Frac"],
            1.0
        ),
        SearchDocument(
            22,
            "Frac Water: Regulatory Approval Process",
            "Obtaining regulatory approval for frac water sourcing involves coordination with GCDs, TWDB, and local stakeholders.",
            ["Frac", "Regulatory", "Approval", "Process"],
            1.0
        ),
        SearchDocument(
            23,
            "Ogallala Aquifer: Cross-State Water Management",
            "The Ogallala Aquifer spans several states, requiring cross-jurisdictional management for frac water sourcing.",
            ["Ogallala", "Cross-State", "Management", "Frac"],
            1.0
        ),
        SearchDocument(
            24,
            "Pecos Valley Aquifer: Conservation District Rules",
            "Local conservation district rules govern frac water withdrawals from the Pecos Valley Aquifer, including permit conditions and monitoring requirements.",
            ["Pecos Valley", "Conservation", "Rules", "Monitoring"],
            1.0
        ),
        SearchDocument(
            25,
            "Edwards-Trinity Aquifer: Water Quality Sampling Protocols",
            "Sampling protocols for the Edwards-Trinity Aquifer ensure that water quality meets frac operation requirements.",
            ["Edwards-Trinity", "Sampling", "Water Quality", "Frac"],
            1.0
        ),
        SearchDocument(
            26,
            "Dockum Aquifer: Regulatory Variance Process",
            "Operators seeking variances from Dockum Aquifer production limits must provide technical justification and public notice.",
            ["Dockum", "Variance", "Regulatory", "Process"],
            1.0
        ),
        SearchDocument(
            27,
            "Santa Rosa Aquifer: Drought Contingency Planning",
            "Drought contingency planning for the Santa Rosa Aquifer includes monitoring recharge rates and adjusting frac water withdrawals.",
            ["Santa Rosa", "Drought", "Contingency", "Planning"],
            1.0
        ),
        SearchDocument(
            28,
            "TWDB: Common Well Permitting Mistakes",
            "Common mistakes in TWDB well permitting include missing hydrogeologic data and failure to notify affected landowners.",
            ["TWDB", "Permitting", "Mistakes", "Well"],
            1.0
        ),
        SearchDocument(
            29,
            "GCD Variance: Demonstrating Non-Impairment",
            "Variance applications to GCDs must demonstrate that increased withdrawals will not impair existing wells or aquifer sustainability.",
            ["GCD", "Variance", "Non-Impairment", "Sustainability"],
            1.0
        ),
        SearchDocument(
            30,
            "Water Quality: Scale and Corrosion Control for Frac Use",
            "Scale and corrosion control are essential for maintaining frac water system integrity, especially when using high-TDS sources.",
            ["Water Quality", "Scale", "Corrosion", "Frac"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)