import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
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

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.total_docs: int = 0
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            for token in tokens:
                self.term_freqs[doc.id][token] += 1
            self._update_avg_doc_length()
            self.idf_cache.clear()

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_tokens: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        for term in query_tokens:
            idf = self._compute_idf(term)
            tf = self.term_freqs[doc_id].get(term, 0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length + 1e-6))
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_tokens: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        tf_counter = self.term_freqs[doc_id]
        for term in query_tokens:
            tf = tf_counter.get(term, 0) / (doc_length + 1e-6)
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_tokens, doc_id)
            else:
                score = self._score_bm25(query_tokens, doc_id)
            if score > 0:
                snippet = self._make_snippet(doc_id, query_tokens)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc_id: str, query_tokens: List[str]) -> str:
        doc = self.documents[doc_id]
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:160] + ('...' if len(content) > 160 else '')
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet[:160] + ('...' if len(snippet) > 160 else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

_search_index_singleton: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_singleton
    with _search_index_lock:
        if _search_index_singleton is None:
            _search_index_singleton = SearchIndex()
            _seed_documents(_search_index_singleton)
        return _search_index_singleton

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            "doc1",
            "Unleased Mineral Identification in Texas",
            "Identify unleased mineral interests using county records, GIS overlays, and production data. Focus on gaps in leasehold and mineral ownership.",
            ["unleased", "mineral", "texas", "identification"],
            1.0
        ),
        SearchDocument(
            "doc2",
            "Dormant Mineral Act Application (Texas NRC Ch. 75)",
            "Apply Texas Natural Resources Code Chapter 75 to dormant mineral interests. Procedures for notice, affidavit, and recordation to claim dormant minerals.",
            ["dormant", "mineral", "act", "texas", "nrc", "ch75"],
            1.0
        ),
        SearchDocument(
            "doc3",
            "Heirship Opportunity Scoring",
            "Score mineral interests for heirship acquisition. Analyze probate records, intestate succession, and family tree mapping to identify fragmented ownership.",
            ["heirship", "opportunity", "scoring", "mineral", "probate"],
            1.0
        ),
        SearchDocument(
            "doc4",
            "Title Defect Acquisition Strategy",
            "Acquire mineral interests with title defects. Target clouded titles, missing heirs, and ambiguous conveyances. Use curative actions and risk pricing.",
            ["title", "defect", "acquisition", "mineral", "curative"],
            1.0
        ),
        SearchDocument(
            "doc5",
            "Mineral Interest Fragmentation Analysis",
            "Analyze fragmentation in mineral interests. Use GIS mapping, historical conveyances, and family partitions to identify acquisition targets.",
            ["fragmentation", "mineral", "analysis", "gis", "conveyance"],
            1.0
        ),
        SearchDocument(
            "doc6",
            "Estate Planning Gaps and Mineral Acquisition",
            "Identify estate planning gaps affecting mineral ownership. Focus on unprobated wills, intestate estates, and trust failures for acquisition.",
            ["estate", "planning", "gaps", "mineral", "acquisition"],
            1.0
        ),
        SearchDocument(
            "doc7",
            "Tax Delinquent Mineral Interest Acquisition",
            "Acquire mineral interests subject to tax delinquency. Review county tax rolls, foreclosure notices, and redemption periods for opportunities.",
            ["tax", "delinquent", "mineral", "acquisition", "foreclosure"],
            1.0
        ),
        SearchDocument(
            "doc8",
            "Forced Pooling Opportunities",
            "Identify forced pooling opportunities under Texas law. Analyze spacing units, unleased tracts, and regulatory filings for acquisition.",
            ["forced", "pooling", "opportunity", "texas", "regulatory"],
            1.0
        ),
        SearchDocument(
            "doc9",
            "Farmout Opportunity Identification",
            "Identify farmout opportunities in mineral acquisition. Review drilling commitments, acreage positions, and operator farmout offers.",
            ["farmout", "opportunity", "mineral", "drilling", "operator"],
            1.0
        ),
        SearchDocument(
            "doc10",
            "JV Partner Matching for Mineral Acquisition",
            "Match JV partners for mineral acquisition. Analyze partner profiles, capital requirements, and deal flow for joint venture structuring.",
            ["jv", "partner", "matching", "mineral", "acquisition"],
            1.0
        ),
        SearchDocument(
            "doc11",
            "Texas County Records for Mineral Ownership",
            "Utilize Texas county records to trace mineral ownership. Review deeds, leases, and probate filings for unleased and dormant interests.",
            ["texas", "county", "records", "mineral", "ownership"],
            1.0
        ),
        SearchDocument(
            "doc12",
            "GIS Mapping for Mineral Interest Analysis",
            "Use GIS mapping to visualize mineral interest fragmentation and leasehold gaps. Overlay production data and historical conveyances.",
            ["gis", "mapping", "mineral", "fragmentation", "leasehold"],
            1.0
        ),
        SearchDocument(
            "doc13",
            "Probate and Intestate Succession in Mineral Acquisition",
            "Analyze probate and intestate succession for mineral acquisition. Identify heirs, unprobated estates, and title defects.",
            ["probate", "intestate", "succession", "mineral", "acquisition"],
            1.0
        ),
        SearchDocument(
            "doc14",
            "Clouded Title and Curative Actions",
            "Resolve clouded title issues in mineral acquisition. Use affidavits, quitclaim deeds, and judicial actions to cure defects.",
            ["clouded", "title", "curative", "mineral", "affidavit"],
            1.0
        ),
        SearchDocument(
            "doc15",
            "Mineral Interest Acquisition from Trust Failures",
            "Acquire mineral interests from failed trusts. Identify trust dissolution, successor trustee issues, and unadministered assets.",
            ["trust", "failure", "mineral", "acquisition", "assets"],
            1.0
        ),
        SearchDocument(
            "doc16",
            "Mineral Interest Acquisition via Foreclosure",
            "Target mineral interests acquired through foreclosure. Review foreclosure sales, tax liens, and redemption statutes.",
            ["foreclosure", "mineral", "acquisition", "tax", "liens"],
            1.0
        ),
        SearchDocument(
            "doc17",
            "Regulatory Filings for Forced Pooling",
            "Analyze regulatory filings for forced pooling opportunities. Review spacing unit applications and commission orders.",
            ["regulatory", "filing", "forced", "pooling", "spacing"],
            1.0
        ),
        SearchDocument(
            "doc18",
            "Drilling Commitments and Farmout Deals",
            "Identify farmout deals based on drilling commitments. Analyze operator obligations and acreage positions.",
            ["drilling", "commitment", "farmout", "operator", "acreage"],
            1.0
        ),
        SearchDocument(
            "doc19",
            "JV Capital Requirements in Mineral Acquisition",
            "Assess JV capital requirements for mineral acquisition. Match partners based on investment criteria and deal flow.",
            ["jv", "capital", "requirement", "mineral", "acquisition"],
            1.0
        ),
        SearchDocument(
            "doc20",
            "Unleased Mineral Interest Mapping",
            "Map unleased mineral interests using GIS overlays and county records. Identify leasehold gaps and dormant interests.",
            ["unleased", "mineral", "mapping", "gis", "county"],
            1.0
        ),
        SearchDocument(
            "doc21",
            "Heirship Mapping for Mineral Acquisition",
            "Map heirship for mineral acquisition using family trees, probate records, and intestate succession analysis.",
            ["heirship", "mapping", "mineral", "probate", "succession"],
            1.0
        ),
        SearchDocument(
            "doc22",
            "Title Defect Pricing in Mineral Acquisition",
            "Price mineral interests with title defects. Use risk-adjusted pricing models for clouded titles and ambiguous conveyances.",
            ["title", "defect", "pricing", "mineral", "risk"],
            1.0
        ),
        SearchDocument(
            "doc23",
            "Fragmented Mineral Ownership Acquisition",
            "Acquire fragmented mineral ownership using GIS mapping and historical conveyances. Target partitioned interests and family splits.",
            ["fragmented", "ownership", "mineral", "gis", "conveyance"],
            1.0
        ),
        SearchDocument(
            "doc24",
            "Estate Planning Failures Affecting Mineral Interests",
            "Identify estate planning failures impacting mineral interests. Focus on unprobated wills, intestate estates, and trust dissolution.",
            ["estate", "planning", "failure", "mineral", "dissolution"],
            1.0
        ),
        SearchDocument(
            "doc25",
            "Tax Sale Acquisition of Mineral Interests",
            "Acquire mineral interests through tax sale. Review county tax sale notices, redemption periods, and foreclosure statutes.",
            ["tax", "sale", "acquisition", "mineral", "foreclosure"],
            1.0
        ),
        SearchDocument(
            "doc26",
            "Forced Pooling Under Texas Law",
            "Review Texas law on forced pooling. Analyze regulatory filings, spacing units, and unleased tracts for acquisition.",
            ["forced", "pooling", "texas", "regulatory", "spacing"],
            1.0
        ),
        SearchDocument(
            "doc27",
            "Farmout Offers and Operator Deal Flow",
            "Identify farmout offers from operators. Analyze deal flow, drilling commitments, and acreage positions.",
            ["farmout", "offer", "operator", "deal", "drilling"],
            1.0
        ),
        SearchDocument(
            "doc28",
            "JV Partner Profiles for Mineral Acquisition",
            "Match JV partners based on profiles, capital requirements, and acquisition criteria. Structure joint ventures for mineral deals.",
            ["jv", "partner", "profile", "mineral", "acquisition"],
            1.0
        ),
        SearchDocument(
            "doc29",
            "Texas NRC Ch. 75 Dormant Mineral Procedures",
            "Apply Texas NRC Chapter 75 procedures for dormant mineral interests. Review notice, affidavit, and recordation requirements.",
            ["texas", "nrc", "ch75", "dormant", "mineral"],
            1.0
        ),
        SearchDocument(
            "doc30",
            "Unleased Mineral Opportunity Scoring",
            "Score unleased mineral opportunities using GIS mapping, county records, and production overlays.",
            ["unleased", "mineral", "opportunity", "scoring", "gis"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)