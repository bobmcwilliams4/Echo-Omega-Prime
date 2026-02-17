import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._bm25_k1 = bm25_k1
        self._bm25_b = bm25_b
        self._lock = threading.Lock()
        self._doc_term_freqs: Dict[int, Counter] = {}
        self._idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            term_freqs = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_term_freqs[doc.id] = term_freqs
            self._doc_lengths[doc.id] = len(tokens)
            for term in term_freqs:
                self._inverted_index[term].add(doc.id)
                self._doc_freqs[term] += 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs if self._total_docs > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self._inverted_index.get(term, set()))
        scored_results = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            scored_results.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_documents": self._total_docs,
            "avg_doc_length": self._avg_doc_length,
            "unique_terms": len(self._inverted_index)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
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

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self._documents[doc_id]
        term_freqs = self._doc_term_freqs[doc_id]
        doc_length = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in term_freqs:
                continue
            tf = term_freqs[term]
            idf = self._compute_idf(term)
            denom = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / (self._avg_doc_length + 1e-9))
            score += idf * ((tf * (self._bm25_k1 + 1)) / (denom + 1e-9))
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        term_freqs = self._doc_term_freqs[doc_id]
        doc_length = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / (doc_length + 1e-9)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self._documents[doc_id].weight

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], max_len: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:max_len]
            if len(content) > max_len:
                snippet += "..."
            return snippet
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({term})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        if len(snippet) > max_len:
            snippet = snippet[:max_len] + "..."
        return snippet

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
                _preseed_documents(_search_index_instance)
    return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Permian Basin Stage Spacing Evolution",
            "A historical overview of stage spacing practices in the Permian Basin, highlighting the transition from wide to tighter spacing as completion technology advanced. Discusses the impact on recovery factors and well interference.",
            ["Permian", "Stage Spacing", "Evolution"],
            1.0
        ),
        SearchDocument(
            2,
            "Optimal Cluster Spacing Within Stages",
            "Analysis of cluster spacing optimization within hydraulic fracture stages. Reviews field trials and simulation results showing the effect of cluster count and spacing on stimulated reservoir volume (SRV) and production.",
            ["Cluster Spacing", "Optimization", "SRV"],
            1.0
        ),
        SearchDocument(
            3,
            "Well Spacing Optimization: Parent-Child Relationships",
            "Explores parent-child well interactions in tight oil plays. Focuses on how infill well performance is affected by depletion and fracture-driven interference, and strategies to mitigate negative impacts through optimal well and stage spacing.",
            ["Well Spacing", "Parent-Child", "Interference"],
            1.0
        ),
        SearchDocument(
            4,
            "Cube Development and Stacked Lateral Strategy",
            "Describes cube development concepts in the Permian, with stacked laterals across multiple benches. Reviews how vertical and horizontal spacing, along with stage placement, affect resource recovery and economics.",
            ["Cube Development", "Stacked Laterals", "Spacing"],
            1.0
        ),
        SearchDocument(
            5,
            "Completion Intensity Metrics and EUR Correlation",
            "Examines the relationship between completion intensity (stages per lateral length, proppant/fluids per foot) and estimated ultimate recovery (EUR). Includes statistical analysis from multiple Permian operators.",
            ["Completion Intensity", "EUR", "Metrics"],
            1.0
        ),
        SearchDocument(
            6,
            "Lateral Length Optimization in Unconventionals",
            "Investigates optimal lateral length for maximizing NPV and EUR. Considers the trade-off between incremental recovery and increased capital/operational complexity.",
            ["Lateral Length", "Optimization", "NPV"],
            1.0
        ),
        SearchDocument(
            7,
            "Frac-Driven Interactions (FBI) and Mitigation Strategies",
            "Summarizes mechanisms of frac-driven interactions (FBI) in multi-well pads. Reviews mitigation techniques such as modified stage sequencing, pressure monitoring, and real-time shut-in protocols.",
            ["Frac-Driven Interactions", "FBI", "Mitigation"],
            1.0
        ),
        SearchDocument(
            8,
            "Economic Optimization Framework for Completion Design",
            "Presents a workflow for integrating economic models with completion design. Includes case studies where stage and cluster spacing were optimized for NPV under various commodity price scenarios.",
            ["Economic Optimization", "Completion Design", "NPV"],
            1.0
        ),
        SearchDocument(
            9,
            "Field Development Planning and Sequencing",
            "Outlines best practices for field development planning, including sequencing of parent and child wells, stage spacing, and integration with reservoir simulation models.",
            ["Field Development", "Sequencing", "Planning"],
            1.0
        ),
        SearchDocument(
            10,
            "Stage Spacing in Low vs High Permeability Zones",
            "Compares recommended stage spacing in low-perm versus high-perm intervals. Discusses the impact of rock quality on fracture propagation and optimal stage count.",
            ["Stage Spacing", "Permeability", "Rock Quality"],
            1.0
        ),
        SearchDocument(
            11,
            "Simul-Frac and Zipper Frac Operational Strategies",
            "Details operational considerations for simul-frac and zipper frac approaches. Highlights how stage and cluster spacing must be adapted for simultaneous operations to minimize interference.",
            ["Simul-Frac", "Zipper Frac", "Operations"],
            1.0
        ),
        SearchDocument(
            12,
            "Proppant Type and Size Selection for Stage Spacing",
            "Reviews how proppant selection (type, size, concentration) interacts with stage spacing to influence conductivity and fracture geometry. Includes field examples from the Delaware and Midland Basins.",
            ["Proppant", "Stage Spacing", "Conductivity"],
            1.0
        ),
        SearchDocument(
            13,
            "Regulatory and Unitization Constraints on Spacing",
            "Summarizes regulatory frameworks affecting stage and well spacing in the Permian. Discusses unitization, lease lines, and how operators adapt completion design to legal boundaries.",
            ["Regulatory", "Unitization", "Spacing"],
            1.0
        ),
        SearchDocument(
            14,
            "Completion Design for Naturally Fractured Reservoirs",
            "Explores completion design modifications for naturally fractured zones. Focuses on stage placement, proppant selection, and pressure management to maximize connectivity.",
            ["Completion Design", "Natural Fractures", "Reservoirs"],
            1.0
        ),
        SearchDocument(
            15,
            "Standardization vs Customization in Completion Design",
            "Debates the merits of standardized versus customized completion designs. Reviews how stage spacing templates are balanced with geologic heterogeneity.",
            ["Standardization", "Customization", "Completion Design"],
            1.0
        ),
        SearchDocument(
            16,
            "Advanced Diagnostics for Stage Spacing Evaluation",
            "Describes use of fiber optics, tracers, and microseismic to evaluate stage spacing effectiveness. Presents diagnostic workflows for real-time adjustment.",
            ["Diagnostics", "Stage Spacing", "Fiber Optics"],
            1.0
        ),
        SearchDocument(
            17,
            "Machine Learning for Spacing Optimization",
            "Presents machine learning approaches for predicting optimal stage and well spacing. Includes feature engineering from geologic, completion, and production datasets.",
            ["Machine Learning", "Spacing Optimization", "Prediction"],
            1.0
        ),
        SearchDocument(
            18,
            "Parent Well Protection During Child Well Fracs",
            "Discusses operational protocols to protect parent wells during infill completions. Includes pressure monitoring, stage sequencing, and shut-in strategies.",
            ["Parent Well", "Protection", "Child Well"],
            1.0
        ),
        SearchDocument(
            19,
            "Impact of Stage Spacing on Well Interference",
            "Quantifies how stage spacing affects well interference and production degradation. Reviews simulation and field data from cube developments.",
            ["Stage Spacing", "Well Interference", "Production"],
            1.0
        ),
        SearchDocument(
            20,
            "Completion Cost Analysis: Stage and Cluster Spacing",
            "Breaks down completion costs as a function of stage and cluster count. Provides economic sensitivity to spacing decisions.",
            ["Cost Analysis", "Stage Spacing", "Cluster Spacing"],
            1.0
        ),
        SearchDocument(
            21,
            "Geomechanical Modeling for Spacing Decisions",
            "Explains how geomechanical models inform stage and well spacing. Discusses stress shadowing, fracture containment, and rock fabric considerations.",
            ["Geomechanics", "Modeling", "Spacing"],
            1.0
        ),
        SearchDocument(
            22,
            "SRV Maximization Through Stage Placement",
            "Details strategies for maximizing stimulated reservoir volume (SRV) via stage placement. Includes examples of variable stage length and density.",
            ["SRV", "Stage Placement", "Maximization"],
            1.0
        ),
        SearchDocument(
            23,
            "Production Type Curves by Stage Spacing",
            "Presents type curve analysis segmented by stage spacing. Shows how tighter or wider spacing impacts decline rates and EUR.",
            ["Type Curves", "Stage Spacing", "Production"],
            1.0
        ),
        SearchDocument(
            24,
            "Fluid System Selection and Stage Spacing",
            "Reviews the interaction of fluid system (slickwater, hybrid, crosslinked) with stage spacing. Discusses impact on proppant transport and fracture complexity.",
            ["Fluid System", "Stage Spacing", "Proppant"],
            1.0
        ),
        SearchDocument(
            25,
            "Operational Constraints: Pump Rates and Stage Spacing",
            "Analyzes how maximum allowable pump rates and surface equipment limit stage spacing and cluster count. Provides operational guidelines.",
            ["Operations", "Pump Rates", "Stage Spacing"],
            1.0
        ),
        SearchDocument(
            26,
            "Wellbore Integrity and Stage Spacing",
            "Examines how stage spacing influences wellbore integrity risks such as casing deformation and microannulus. Includes mitigation recommendations.",
            ["Wellbore Integrity", "Stage Spacing", "Casing"],
            1.0
        ),
        SearchDocument(
            27,
            "Data Analytics for Spacing Optimization",
            "Highlights data analytics workflows for evaluating stage and well spacing. Includes integration of production, completion, and diagnostic data.",
            ["Data Analytics", "Spacing Optimization", "Evaluation"],
            1.0
        ),
        SearchDocument(
            28,
            "Frac Hit Prediction and Stage Spacing",
            "Reviews models for predicting frac hits based on stage spacing and pad layout. Discusses mitigation and monitoring approaches.",
            ["Frac Hit", "Prediction", "Stage Spacing"],
            1.0
        ),
        SearchDocument(
            29,
            "Stage Spacing in Unconventional Reservoirs: Case Studies",
            "Provides case studies from the Permian, Eagle Ford, and Bakken on stage spacing optimization. Includes lessons learned and best practices.",
            ["Stage Spacing", "Case Studies", "Unconventional"],
            1.0
        ),
        SearchDocument(
            30,
            "Environmental Considerations in Stage Spacing",
            "Discusses water usage, emissions, and surface disturbance as a function of stage and cluster spacing. Reviews regulatory compliance.",
            ["Environmental", "Stage Spacing", "Regulation"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)