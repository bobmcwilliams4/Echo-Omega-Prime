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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[Tuple[int, str], float] = {}
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            term_counts = Counter(tokens)
            for term, count in term_counts.items():
                self.inverted_index[term][doc.id] = count
            self._recompute_stats = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        with self.lock:
            if self._recompute_stats:
                self._update_stats()
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self.inverted_index.get(term, {}).keys())
        scores = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            score = bm25_score * 0.7 + tfidf_score * 0.3
            score *= doc.weight
            snippet = self._make_snippet(doc, query_terms)
            scores.append(SearchResult(doc_id, score, doc.title, snippet))
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def get_stats(self):
        with self.lock:
            if self._recompute_stats:
                self._update_stats()
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def _update_stats(self):
        self.N = len(self.documents)
        if self.N == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N
        self.idf_cache.clear()
        self.tf_cache.clear()
        self._recompute_stats = False

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _compute_tf(self, doc_id: int, term: str) -> float:
        key = (doc_id, term)
        if key in self.tf_cache:
            return self.tf_cache[key]
        tf = self.inverted_index.get(term, {}).get(doc_id, 0)
        doc_len = self.doc_lengths.get(doc_id, 1)
        norm_tf = tf / doc_len
        self.tf_cache[key] = norm_tf
        return norm_tf

    def _score_bm25(self, doc_id: int, query_terms: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        for term in query_terms:
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            denom = tf + k1 * (1 - b + b * doc_len / avgdl)
            if denom == 0:
                continue
            score += idf * (tf * (k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        for term in query_terms:
            tf = self._compute_tf(doc_id, term)
            idf = self._compute_idf(term)
            score += tf * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

_index_instance: Optional[SearchIndex] = None
_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _index_instance
    with _index_lock:
        if _index_instance is None:
            _index_instance = SearchIndex()
            _preseed_documents(_index_instance)
        return _index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Texas Water Code Fundamentals",
            "The Texas Water Code establishes the legal framework for the allocation, management, and protection of water resources in Texas. It covers both surface and groundwater, outlining the roles of state agencies such as the Texas Commission on Environmental Quality (TCEQ) and the Texas Water Development Board (TWDB).",
            ["Texas Water Code", "Fundamentals", "TCEQ", "TWDB"],
            1.0
        ),
        SearchDocument(
            2,
            "Prior Appropriation Doctrine in Texas",
            "Texas applies the prior appropriation doctrine to surface water, meaning 'first in time, first in right.' Water rights are granted based on the date of appropriation, and senior rights holders have priority during shortages.",
            ["Prior Appropriation", "Surface Water", "Doctrine"],
            1.0
        ),
        SearchDocument(
            3,
            "Rule of Capture for Groundwater",
            "The rule of capture allows Texas landowners to pump and use groundwater beneath their land with minimal regulation. However, exceptions exist for malicious or wasteful use, and local Groundwater Conservation Districts may impose rules.",
            ["Rule of Capture", "Groundwater", "Landowner Rights"],
            1.0
        ),
        SearchDocument(
            4,
            "Groundwater Conservation District Rules",
            "Groundwater Conservation Districts (GCDs) are the primary regulators of groundwater in Texas. GCDs can require permits, limit production, and adopt rules to conserve, preserve, and protect groundwater resources.",
            ["GCD", "Groundwater", "Conservation", "Permitting"],
            1.0
        ),
        SearchDocument(
            5,
            "Permian Basin GCD Regulations",
            "The Permian Basin Groundwater Conservation District regulates groundwater withdrawals in Howard and Martin counties. The district sets well spacing, production limits, and reporting requirements to manage aquifer resources.",
            ["Permian Basin", "GCD", "Groundwater", "Regulations"],
            1.0
        ),
        SearchDocument(
            6,
            "Surface Water Permits and TCEQ",
            "Surface water in Texas is owned by the state. The TCEQ issues permits for the use of surface water, considering factors such as availability, environmental flows, and existing rights.",
            ["Surface Water", "Permits", "TCEQ"],
            1.0
        ),
        SearchDocument(
            7,
            "Water Rights Transfers in Texas",
            "Water rights in Texas can be transferred through sale, lease, or gift, subject to approval by the TCEQ. Transfers must not adversely affect other water rights holders or the environment.",
            ["Water Rights", "Transfers", "TCEQ"],
            1.0
        ),
        SearchDocument(
            8,
            "Produced Water Regulations",
            "Produced water, a byproduct of oil and gas extraction, is regulated by the Railroad Commission of Texas and TCEQ. Permits are required for disposal, reuse, or discharge to protect water quality.",
            ["Produced Water", "Oil and Gas", "Regulations"],
            1.0
        ),
        SearchDocument(
            9,
            "Recycled Water Permits",
            "The TCEQ regulates the use of recycled water, including graywater and treated effluent. Permits are required for large-scale reuse projects to ensure public health and environmental protection.",
            ["Recycled Water", "Permits", "Reuse", "TCEQ"],
            1.0
        ),
        SearchDocument(
            10,
            "Water Marketing in Texas",
            "Water marketing involves the buying, selling, or leasing of water rights. In Texas, marketing is subject to state approval and must comply with water availability and public interest requirements.",
            ["Water Marketing", "Water Rights", "Transfers"],
            1.0
        ),
        SearchDocument(
            11,
            "Edwards Aquifer Authority",
            "The Edwards Aquifer Authority manages groundwater withdrawals from the Edwards Aquifer, imposing strict permitting and conservation measures to protect springflows and endangered species.",
            ["Edwards Aquifer", "Authority", "Groundwater"],
            1.0
        ),
        SearchDocument(
            12,
            "Ogallala Aquifer Depletion",
            "The Ogallala Aquifer, underlying much of the Texas Panhandle, faces significant depletion due to irrigation. Conservation districts and state agencies monitor usage and promote sustainable practices.",
            ["Ogallala Aquifer", "Depletion", "Groundwater"],
            1.0
        ),
        SearchDocument(
            13,
            "Brackish Water Zones",
            "Texas designates certain areas as brackish groundwater production zones to encourage development of alternative water supplies. Permitting is streamlined for projects in these zones.",
            ["Brackish Water", "Groundwater", "Permitting"],
            1.0
        ),
        SearchDocument(
            14,
            "Desalination Permits in Texas",
            "Desalination projects, both for seawater and brackish groundwater, require permits from the TCEQ. The process includes environmental review and public participation.",
            ["Desalination", "Permits", "TCEQ"],
            1.0
        ),
        SearchDocument(
            15,
            "Interstate Water Compacts",
            "Texas is a party to several interstate water compacts, including the Rio Grande and Pecos River Compacts. These agreements allocate water among states and resolve disputes.",
            ["Interstate Compacts", "Rio Grande", "Pecos River"],
            1.0
        ),
        SearchDocument(
            16,
            "Rio Grande Compact",
            "The Rio Grande Compact apportions water among Colorado, New Mexico, and Texas. The Rio Grande Compact Commission oversees compliance and dispute resolution.",
            ["Rio Grande", "Compact", "Interstate"],
            1.0
        ),
        SearchDocument(
            17,
            "Pecos River Compact",
            "The Pecos River Compact governs the allocation of Pecos River water between Texas and New Mexico, with a commission ensuring compliance and addressing conflicts.",
            ["Pecos River", "Compact", "Interstate"],
            1.0
        ),
        SearchDocument(
            18,
            "Water Conservation Requirements",
            "Texas law requires water suppliers to implement water conservation plans and report on progress. Conservation measures may include leak detection, public education, and incentives for efficient use.",
            ["Water Conservation", "Requirements", "Suppliers"],
            1.0
        ),
        SearchDocument(
            19,
            "Drought Contingency Planning",
            "Drought contingency plans are required for public water systems and large water users. Plans outline strategies for reducing demand and ensuring supply during drought conditions.",
            ["Drought", "Contingency", "Planning"],
            1.0
        ),
        SearchDocument(
            20,
            "Water Availability Modeling",
            "Water availability models (WAMs) are used by the TCEQ to evaluate the impact of new water rights and ensure that existing rights are protected. WAMs simulate river flows and reservoir operations.",
            ["Water Availability", "Modeling", "WAM", "TCEQ"],
            1.0
        ),
        SearchDocument(
            21,
            "Groundwater Management Areas",
            "Groundwater Management Areas (GMAs) coordinate planning among GCDs to achieve desired future conditions for aquifers. GMAs develop joint planning and management strategies.",
            ["Groundwater", "Management Areas", "GMA"],
            1.0
        ),
        SearchDocument(
            22,
            "Surface Water Rights Adjudication",
            "Texas has conducted adjudication proceedings to clarify and confirm surface water rights. The process involves legal hearings and issuance of certificates of adjudication.",
            ["Surface Water", "Rights", "Adjudication"],
            1.0
        ),
        SearchDocument(
            23,
            "Conjunctive Management of Surface and Groundwater",
            "Conjunctive management refers to coordinated regulation of surface water and groundwater to optimize resource use and sustainability, particularly in areas where the two interact.",
            ["Conjunctive Management", "Surface Water", "Groundwater"],
            1.0
        ),
        SearchDocument(
            24,
            "Environmental Flows in Texas",
            "Environmental flows are water allocations set aside to maintain healthy rivers, bays, and estuaries. The TCEQ considers environmental flows when issuing new surface water permits.",
            ["Environmental Flows", "Surface Water", "TCEQ"],
            1.0
        ),
        SearchDocument(
            25,
            "Reuse of Produced Water",
            "Reuse of produced water from oil and gas operations is encouraged to reduce freshwater demand. Projects must comply with Railroad Commission and TCEQ regulations.",
            ["Produced Water", "Reuse", "Oil and Gas"],
            1.0
        ),
        SearchDocument(
            26,
            "Brackish Groundwater Desalination Incentives",
            "Texas offers incentives for the development of brackish groundwater desalination facilities, including expedited permitting and grant funding for pilot projects.",
            ["Brackish Groundwater", "Desalination", "Incentives"],
            1.0
        ),
        SearchDocument(
            27,
            "Water Rights Forfeiture and Cancellation",
            "Water rights may be forfeited or cancelled for non-use or violation of permit conditions. The TCEQ administers forfeiture proceedings and reallocation of rights.",
            ["Water Rights", "Forfeiture", "Cancellation", "TCEQ"],
            1.0
        ),
        SearchDocument(
            28,
            "Groundwater Well Permitting Process",
            "Most GCDs require permits for drilling and operating groundwater wells. The permitting process considers well location, spacing, and potential impacts on neighboring wells.",
            ["Groundwater", "Well Permitting", "GCD"],
            1.0
        ),
        SearchDocument(
            29,
            "Texas Watermaster Programs",
            "Watermasters appointed by the TCEQ manage water distribution in certain river basins, ensuring compliance with water rights and responding to complaints.",
            ["Watermaster", "TCEQ", "Water Rights"],
            1.0
        ),
        SearchDocument(
            30,
            "Aquifer Storage and Recovery",
            "Aquifer storage and recovery (ASR) projects store water underground for later use. Texas law provides a permitting framework for ASR to enhance drought resilience.",
            ["Aquifer Storage", "Recovery", "ASR", "Permitting"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)