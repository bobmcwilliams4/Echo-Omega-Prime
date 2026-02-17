import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# -----------------------------
# Data Classes
# -----------------------------

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

# -----------------------------
# Search Index
# -----------------------------

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.RLock()
        self._idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = dict(tf)
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        candidate_docs = set()
        for term in tokens:
            candidate_docs |= self.inverted_index.get(term, set())
        scored = []
        for doc_id in candidate_docs:
            score = self._score_bm25(doc_id, tokens)
            scored.append((score, doc_id))
        top = heapq.nlargest(limit, scored)
        results = []
        for score, doc_id in top:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_docs": self.total_docs,
                "avg_doc_length": self.avg_doc_length,
                "unique_terms": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_tokens: List[str]) -> float:
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in set(query_tokens):
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length + 1e-9))
            term_score = idf * freq * (self.k1 + 1) / (denom + 1e-9)
            score += term_score
        score *= doc.weight
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:160]
            return snippet + "..." if len(content) > 160 else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + "..." if end < len(tokens) else snippet

    # TF-IDF scoring for reference/alternative
    def score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in set(query_tokens):
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

# -----------------------------
# Singleton Factory
# -----------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_domain_documents(_search_index_instance)
        return _search_index_instance

# -----------------------------
# Domain Document Seeding
# -----------------------------

def _seed_domain_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="General Warranty Deed",
            content="A General Warranty Deed conveys real property with the broadest guarantee of title. The grantor fully warrants the title against any claims.",
            tags=["warranty", "deed", "property", "title"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Special Warranty Deed",
            content="A Special Warranty Deed conveys property but only warrants against claims arising during the grantor's ownership. It limits the scope of the warranty.",
            tags=["special", "warranty", "deed", "property"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Quitclaim Deed",
            content="A Quitclaim Deed transfers any interest the grantor may have in the property, without warranties or guarantees of title.",
            tags=["quitclaim", "deed", "property", "transfer"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Oil and Gas Lease",
            content="An Oil and Gas Lease grants exploration and production rights for oil and gas on the described property, subject to terms and royalties.",
            tags=["oil", "gas", "lease", "energy"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Mineral Deed",
            content="A Mineral Deed transfers ownership of mineral rights, such as oil, gas, or coal, separate from the surface estate.",
            tags=["mineral", "deed", "rights", "property"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Royalty Deed",
            content="A Royalty Deed conveys a royalty interest in oil, gas, or minerals produced from the property, entitling the holder to a share of production.",
            tags=["royalty", "deed", "interest", "production"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Deed of Trust",
            content="A Deed of Trust secures a loan on real property by conveying title to a trustee, who holds it as security for the lender.",
            tags=["deed", "trust", "loan", "security"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Release of Lien",
            content="A Release of Lien is a document that removes a previously placed lien from the property, indicating the debt has been satisfied.",
            tags=["release", "lien", "property", "debt"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Affidavit of Heirship",
            content="An Affidavit of Heirship is used to establish ownership of property when the owner dies without a will, identifying the legal heirs.",
            tags=["affidavit", "heirship", "inheritance", "property"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Probate Court Order",
            content="A Probate Court Order is issued by a court to transfer property from a deceased person's estate to the rightful heirs or beneficiaries.",
            tags=["probate", "court", "order", "estate"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Divorce Decree Property Division",
            content="A Divorce Decree Property Division outlines the distribution of marital property between spouses upon divorce, as ordered by the court.",
            tags=["divorce", "decree", "property", "division"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Assignment of Overriding Royalty Interest",
            content="This document assigns an overriding royalty interest in oil and gas production to another party, entitling them to a percentage of gross production.",
            tags=["assignment", "overriding", "royalty", "interest"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Assignment of Working Interest",
            content="An Assignment of Working Interest transfers a share of the operational rights and obligations in an oil and gas lease to another party.",
            tags=["assignment", "working", "interest", "oil", "gas"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Pipeline Right of Way",
            content="A Pipeline Right of Way grants a company the right to construct and maintain a pipeline across the property, subject to specified terms.",
            tags=["pipeline", "right", "way", "easement"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Division Order",
            content="A Division Order is a directive to distribute proceeds from oil and gas production among interest owners according to their ownership percentages.",
            tags=["division", "order", "oil", "gas", "proceeds"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Pooling Agreement",
            content="A Pooling Agreement combines mineral or leasehold interests to facilitate efficient oil and gas development and production.",
            tags=["pooling", "agreement", "oil", "gas"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Unitization Agreement",
            content="A Unitization Agreement consolidates multiple tracts of land or leases for joint oil and gas operations to maximize resource recovery.",
            tags=["unitization", "agreement", "oil", "gas"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Power of Attorney",
            content="A Power of Attorney authorizes another person to act on one's behalf in legal or financial matters, including real estate transactions.",
            tags=["power", "attorney", "legal", "authority"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Correction Deed",
            content="A Correction Deed is executed to correct errors in a previously recorded deed, such as misspelled names or incorrect legal descriptions.",
            tags=["correction", "deed", "error", "record"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Gift Deed",
            content="A Gift Deed transfers property ownership from one party to another as a gift, without consideration or payment.",
            tags=["gift", "deed", "property", "transfer"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Surface Lease",
            content="A Surface Lease grants the right to use the surface of land for a specific purpose, such as agriculture, grazing, or commercial use.",
            tags=["surface", "lease", "land", "use"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Affidavit of Identity",
            content="An Affidavit of Identity is used to verify the identity of a person in legal documents or proceedings.",
            tags=["affidavit", "identity", "verification", "legal"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Affidavit of Non-Production",
            content="An Affidavit of Non-Production certifies that no oil or gas production has occurred on a property during a specified period.",
            tags=["affidavit", "non-production", "oil", "gas"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Ratification of Lease",
            content="A Ratification of Lease confirms and approves the terms of an existing lease, often required when ownership interests change.",
            tags=["ratification", "lease", "approval", "confirmation"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Subordination Agreement",
            content="A Subordination Agreement establishes the priority of one debt or lien over another, often used in real estate financing.",
            tags=["subordination", "agreement", "debt", "lien"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="UCC Financing Statement",
            content="A UCC Financing Statement is filed to give public notice of a secured party's interest in the personal property of a debtor.",
            tags=["ucc", "financing", "statement", "secured"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Partition Order",
            content="A Partition Order is a court order dividing jointly owned property among co-owners, either physically or by sale and division of proceeds.",
            tags=["partition", "order", "property", "court"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Wind/Solar Energy Lease",
            content="A Wind or Solar Energy Lease allows the installation and operation of wind turbines or solar panels on the property for energy generation.",
            tags=["wind", "solar", "energy", "lease"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Receivership Order",
            content="A Receivership Order appoints a receiver to manage property or assets during litigation or insolvency proceedings.",
            tags=["receivership", "order", "court", "assets"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Stipulation of Interest",
            content="A Stipulation of Interest clarifies and confirms the ownership interests of parties in property or mineral rights.",
            tags=["stipulation", "interest", "ownership", "property"],
            weight=1.0
        ),
        # Additional documents for more coverage
        SearchDocument(
            id="31",
            title="Correction Mineral Deed",
            content="A Correction Mineral Deed is used to amend errors in a previously recorded mineral deed, ensuring accurate mineral rights transfer.",
            tags=["correction", "mineral", "deed", "rights"],
            weight=1.0
        ),
        SearchDocument(
            id="32",
            title="Affidavit of Death and Heirship",
            content="This affidavit establishes the death of a property owner and identifies the rightful heirs for title transfer.",
            tags=["affidavit", "death", "heirship", "title"],
            weight=1.0
        ),
        SearchDocument(
            id="33",
            title="Release of Mortgage",
            content="A Release of Mortgage is a document that removes the lender's claim on the property after the mortgage is paid in full.",
            tags=["release", "mortgage", "property", "lender"],
            weight=1.0
        ),
        SearchDocument(
            id="34",
            title="Surface Use Agreement",
            content="A Surface Use Agreement outlines the terms for using the surface of land, often in conjunction with mineral development.",
            tags=["surface", "use", "agreement", "land"],
            weight=1.0
        ),
        SearchDocument(
            id="35",
            title="Assignment of Lease",
            content="An Assignment of Lease transfers the rights and obligations of a lease from the original lessee to a new party.",
            tags=["assignment", "lease", "transfer", "rights"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)