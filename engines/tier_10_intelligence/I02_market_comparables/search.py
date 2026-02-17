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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.doc_count = 0

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_count += 1
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freq[term] += 1
            self._update_avg_doc_length()

    def _update_avg_doc_length(self):
        if self.doc_count == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.doc_count

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        N = self.doc_count
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf_doc = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = tf_doc.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        tf_doc = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = tf_doc.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scored_docs = []
        for doc_id in self.documents:
            if use_bm25:
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(doc_id, query_terms)
                scored_docs.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored_docs.sort(key=lambda x: x.score, reverse=True)
        return scored_docs[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str]) -> str:
        doc = self.documents[doc_id]
        content = doc.content
        tokens = self._tokenize(content)
        indexes = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indexes:
            return content[:160] + '...' if len(content) > 160 else content
        start = max(indexes[0] - 10, 0)
        end = min(indexes[0] + 10, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b(' + re.escape(term) + r')\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            'doc_count': self.doc_count,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
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

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Lease Bonus Rate Analysis: Midland County Wolfcamp",
            "Midland County Wolfcamp lease bonus rates averaged $3,500/acre in Q1 2024, with high variance based on block size and proximity to core. Larger blocks (>100 acres) commanded premiums, while fringe areas saw rates as low as $1,200/acre.",
            ["lease bonus", "midland", "wolfcamp", "county analysis"],
            1.0
        ),
        SearchDocument(
            2,
            "Royalty Rate Negotiation Ranges: Delaware Basin Bone Spring",
            "Delaware Basin Bone Spring royalty rates ranged from 22.5% to 25% in recent negotiations. Operators prefer higher royalties for core acreage, but 20% remains common for legacy leases. Market adjustment factors include depth, formation, and operator reputation.",
            ["royalty rate", "negotiation", "delaware", "bone spring"],
            1.0
        ),
        SearchDocument(
            3,
            "Mineral Deed Valuation: Loving County Spraberry",
            "Mineral deeds in Loving County targeting Spraberry formation traded at $8,000-$12,000 per net mineral acre in Q2 2024. Valuation drivers include production history, lease terms, and recent comparable transactions.",
            ["mineral deed", "loving", "spraberry", "valuation"],
            1.0
        ),
        SearchDocument(
            4,
            "PV-10 Valuation: Producing Property in Reeves County Wolfcamp",
            "PV-10 values for producing properties in Reeves County Wolfcamp formation averaged $2.5MM per well, based on strip pricing and decline curve analysis. Adjustments for royalty burden and lease expiration impact final valuation.",
            ["pv-10", "producing property", "reeves", "wolfcamp"],
            1.0
        ),
        SearchDocument(
            5,
            "Working Interest vs. ORRI Pricing: Howard County Bone Spring",
            "Working interest deals in Howard County Bone Spring formation priced at $4,000/acre, while ORRI interests traded at $1,000/acre. ORRI pricing reflects lower risk and shorter revenue duration. Market adjustment factors include operator, lease terms, and formation.",
            ["working interest", "orri", "howard", "bone spring"],
            1.0
        ),
        SearchDocument(
            6,
            "Net Mineral Acre Calculation: Martin County Spraberry",
            "Net mineral acre calculation in Martin County Spraberry formation requires consideration of leasehold depth, fractional ownership, and royalty burden. Example: 50% mineral interest in 100 gross acres with 25% royalty yields 50 NMA.",
            ["net mineral acre", "martin", "spraberry", "calculation"],
            1.0
        ),
        SearchDocument(
            7,
            "Comparable Transaction Identification: Wolfcamp Formation",
            "Wolfcamp formation comparable transactions are identified by matching lease bonus, royalty rate, and acreage size. Recent deals in Glasscock County show $3,800/acre bonuses and 24% royalty for core blocks.",
            ["comparable transaction", "wolfcamp", "glasscock", "identification"],
            1.0
        ),
        SearchDocument(
            8,
            "Market Adjustment Factors: Bone Spring Valuation",
            "Bone Spring formation valuations are adjusted for depth, proximity to infrastructure, operator reputation, and time-based depreciation. Recent market factors include increased drilling activity and improved completion techniques.",
            ["market adjustment", "bone spring", "valuation", "depreciation"],
            1.0
        ),
        SearchDocument(
            9,
            "Time-Based Depreciation of Comparables: Spraberry",
            "Spraberry comparables depreciate 10-15% per year if not offset by new drilling or lease renewals. Market adjustment factors include commodity price trends and operator activity.",
            ["time-based depreciation", "spraberry", "comparables"],
            1.0
        ),
        SearchDocument(
            10,
            "Formation-Specific Valuations: Wolfcamp Core vs. Fringe",
            "Wolfcamp core acreage commands up to $4,500/acre lease bonus, while fringe areas average $1,500/acre. Royalty rates are higher in core blocks, with 25% common. Valuation models must account for formation quality and operator plans.",
            ["wolfcamp", "core", "fringe", "valuation"],
            1.0
        ),
        SearchDocument(
            11,
            "Lease Bonus Rate Analysis: Glasscock County Bone Spring",
            "Glasscock County Bone Spring lease bonus rates averaged $2,800/acre in Q1 2024. Market adjustment factors include block size, operator, and proximity to producing wells.",
            ["lease bonus", "glasscock", "bone spring", "county analysis"],
            1.0
        ),
        SearchDocument(
            12,
            "Royalty Rate Negotiation Ranges: Martin County Spraberry",
            "Martin County Spraberry royalty rates ranged from 20% to 25%. Negotiation leverage depends on acreage location and operator competition. Recent deals favor higher royalties for core blocks.",
            ["royalty rate", "martin", "spraberry", "negotiation"],
            1.0
        ),
        SearchDocument(
            13,
            "Mineral Deed Dollar per Acre Valuation: Howard County Wolfcamp",
            "Howard County Wolfcamp mineral deeds traded at $7,500-$10,000 per acre. Valuation factors include lease bonus history, production, and comparable transactions.",
            ["mineral deed", "howard", "wolfcamp", "valuation"],
            1.0
        ),
        SearchDocument(
            14,
            "PV-10 Valuation: Producing Property in Midland County Bone Spring",
            "PV-10 values for Midland County Bone Spring producing properties averaged $2MM per well. Adjustments for lease expiration and royalty burden are critical for accurate valuation.",
            ["pv-10", "producing property", "midland", "bone spring"],
            1.0
        ),
        SearchDocument(
            15,
            "Working Interest vs. ORRI Pricing: Reeves County Spraberry",
            "Reeves County Spraberry working interest deals priced at $5,000/acre, while ORRI trades averaged $1,200/acre. Market adjustment factors include operator, lease terms, and formation-specific risk.",
            ["working interest", "orri", "reeves", "spraberry"],
            1.0
        ),
        SearchDocument(
            16,
            "Net Mineral Acre Calculation: Glasscock County Wolfcamp",
            "Glasscock County Wolfcamp net mineral acre calculations require fractional ownership and leasehold depth analysis. Example: 25% mineral interest in 80 gross acres yields 20 NMA.",
            ["net mineral acre", "glasscock", "wolfcamp", "calculation"],
            1.0
        ),
        SearchDocument(
            17,
            "Comparable Transaction Identification: Bone Spring Formation",
            "Bone Spring formation comparable transactions are identified by matching lease bonus, royalty rate, and block size. Recent deals in Howard County show $2,900/acre bonuses and 22.5% royalty.",
            ["comparable transaction", "bone spring", "howard", "identification"],
            1.0
        ),
        SearchDocument(
            18,
            "Market Adjustment Factors: Spraberry Valuation",
            "Spraberry formation valuations are adjusted for depth, lease terms, operator reputation, and time-based depreciation. Recent market factors include increased drilling and commodity price volatility.",
            ["market adjustment", "spraberry", "valuation", "depreciation"],
            1.0
        ),
        SearchDocument(
            19,
            "Time-Based Depreciation of Comparables: Wolfcamp",
            "Wolfcamp comparables depreciate 8-12% per year, with faster depreciation in fringe areas. Market adjustment factors include drilling activity and lease renewal rates.",
            ["time-based depreciation", "wolfcamp", "comparables"],
            1.0
        ),
        SearchDocument(
            20,
            "Formation-Specific Valuations: Bone Spring Core vs. Fringe",
            "Bone Spring core acreage commands up to $3,200/acre lease bonus, while fringe areas average $1,200/acre. Royalty rates are higher in core blocks, with 24% common. Valuation models must account for formation quality.",
            ["bone spring", "core", "fringe", "valuation"],
            1.0
        ),
        SearchDocument(
            21,
            "Lease Bonus Rate Analysis: Reeves County Spraberry",
            "Reeves County Spraberry lease bonus rates averaged $2,500/acre in Q1 2024. Market adjustment factors include block size, operator, and proximity to producing wells.",
            ["lease bonus", "reeves", "spraberry", "county analysis"],
            1.0
        ),
        SearchDocument(
            22,
            "Royalty Rate Negotiation Ranges: Glasscock County Wolfcamp",
            "Glasscock County Wolfcamp royalty rates ranged from 21% to 25%. Negotiation leverage depends on acreage location and operator competition. Recent deals favor higher royalties for core blocks.",
            ["royalty rate", "glasscock", "wolfcamp", "negotiation"],
            1.0
        ),
        SearchDocument(
            23,
            "Mineral Deed Dollar per Acre Valuation: Martin County Bone Spring",
            "Martin County Bone Spring mineral deeds traded at $6,500-$9,000 per acre. Valuation factors include lease bonus history, production, and comparable transactions.",
            ["mineral deed", "martin", "bone spring", "valuation"],
            1.0
        ),
        SearchDocument(
            24,
            "PV-10 Valuation: Producing Property in Howard County Spraberry",
            "PV-10 values for Howard County Spraberry producing properties averaged $1.8MM per well. Adjustments for lease expiration and royalty burden are critical for accurate valuation.",
            ["pv-10", "producing property", "howard", "spraberry"],
            1.0
        ),
        SearchDocument(
            25,
            "Working Interest vs. ORRI Pricing: Midland County Wolfcamp",
            "Midland County Wolfcamp working interest deals priced at $4,200/acre, while ORRI trades averaged $1,100/acre. Market adjustment factors include operator, lease terms, and formation-specific risk.",
            ["working interest", "orri", "midland", "wolfcamp"],
            1.0
        ),
        SearchDocument(
            26,
            "Net Mineral Acre Calculation: Howard County Bone Spring",
            "Howard County Bone Spring net mineral acre calculations require fractional ownership and leasehold depth analysis. Example: 33% mineral interest in 60 gross acres yields 20 NMA.",
            ["net mineral acre", "howard", "bone spring", "calculation"],
            1.0
        ),
        SearchDocument(
            27,
            "Comparable Transaction Identification: Spraberry Formation",
            "Spraberry formation comparable transactions are identified by matching lease bonus, royalty rate, and block size. Recent deals in Martin County show $2,700/acre bonuses and 21% royalty.",
            ["comparable transaction", "spraberry", "martin", "identification"],
            1.0
        ),
        SearchDocument(
            28,
            "Market Adjustment Factors: Wolfcamp Valuation",
            "Wolfcamp formation valuations are adjusted for depth, lease terms, operator reputation, and time-based depreciation. Recent market factors include increased drilling and commodity price volatility.",
            ["market adjustment", "wolfcamp", "valuation", "depreciation"],
            1.0
        ),
        SearchDocument(
            29,
            "Time-Based Depreciation of Comparables: Bone Spring",
            "Bone Spring comparables depreciate 12-18% per year, with faster depreciation in fringe areas. Market adjustment factors include drilling activity and lease renewal rates.",
            ["time-based depreciation", "bone spring", "comparables"],
            1.0
        ),
        SearchDocument(
            30,
            "Formation-Specific Valuations: Spraberry Core vs. Fringe",
            "Spraberry core acreage commands up to $2,900/acre lease bonus, while fringe areas average $1,000/acre. Royalty rates are higher in core blocks, with 23% common. Valuation models must account for formation quality.",
            ["spraberry", "core", "fringe", "valuation"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)