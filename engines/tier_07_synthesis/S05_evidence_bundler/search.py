import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[str, SearchDocument] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._total_terms: int = 0
        self._lock = threading.RLock()
        self._avg_doc_length: float = 0.0
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            term_counts = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_lengths[doc.id] = len(tokens)
            self._total_terms += len(tokens)
            for term, count in term_counts.items():
                self._inverted_index[term][doc.id] = count
                self._doc_freq[term] += 1
            self._avg_doc_length = self._total_terms / max(1, len(self._documents))
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
        with self._lock:
            candidate_docs = set()
            for token in tokens:
                candidate_docs.update(self._inverted_index.get(token, {}).keys())
            scores = {}
            for doc_id in candidate_docs:
                bm25 = self._score_bm25(doc_id, tokens)
                tfidf = self._score_tfidf(doc_id, tokens)
                doc = self._documents[doc_id]
                # Combine BM25 and TF-IDF, weighted by doc.weight
                score = (0.7 * bm25 + 0.3 * tfidf) * doc.weight
                scores[doc_id] = score
            top_docs = heapq.nlargest(limit, scores.items(), key=lambda x: x[1])
            results = []
            for doc_id, score in top_docs:
                doc = self._documents[doc_id]
                snippet = self._make_snippet(doc, tokens)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def get_stats(self) -> Dict[str, int]:
        with self._lock:
            return {
                "document_count": len(self._documents),
                "unique_terms": len(self._inverted_index),
                "total_terms": self._total_terms,
                "average_doc_length": int(self._avg_doc_length)
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove non-word chars, split on whitespace
        text = text.lower()
        text = re.sub(r'[^a-z0-9_#\-\s]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if len(t) > 1 or t.isdigit()]

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self._documents)
        df = self._doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_tokens: List[str]) -> float:
        doc = self._documents[doc_id]
        doc_length = self._doc_lengths[doc_id]
        score = 0.0
        term_counts = self._inverted_index
        for term in set(query_tokens):
            f = term_counts.get(term, {}).get(doc_id, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            numerator = f * (self._bm25_k1 + 1)
            denominator = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / self._avg_doc_length)
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        doc = self._documents[doc_id]
        doc_length = self._doc_lengths[doc_id]
        tfidf = 0.0
        for term in set(query_tokens):
            tf = self._inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            # Term frequency normalization (logarithmic)
            tf_norm = 1 + math.log(tf)
            idf = self._compute_idf(term)
            tfidf += tf_norm * idf
        # Normalize by document length
        if doc_length > 0:
            tfidf /= math.sqrt(doc_length)
        return tfidf

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 32) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:window*2] + "..." if len(content) > window*2 else content
        start = max(positions[0] - window//2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(r'\b(' + re.escape(qt) + r')\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seeded Documents ---

def _preseed_documents(idx: SearchIndex):
    if getattr(idx, '_preseeded', False):
        return
    docs = [
        SearchDocument(
            "1",
            "Evidence Packaging Standards Overview",
            "A comprehensive guide to evidence packaging standards, including chain of custody protocols, WORM storage compliance, and tamper-evident sealing.",
            ["packaging", "standards", "chain_of_custody", "worm"],
            1.0
        ),
        SearchDocument(
            "2",
            "Constructing SHA-256 Hash Chains for Evidence Integrity",
            "Step-by-step instructions for building SHA-256 hash chains to ensure digital evidence integrity and support tamper detection.",
            ["hash_chain", "sha256", "integrity", "tamper_detection"],
            1.0
        ),
        SearchDocument(
            "3",
            "Chain of Custody Tracking Best Practices",
            "Methods and tools for robust chain of custody tracking, including digital signatures, time-stamping, and audit trails.",
            ["chain_of_custody", "tracking", "audit_trail"],
            1.0
        ),
        SearchDocument(
            "4",
            "WORM Storage Compliance for Digital Evidence",
            "Requirements and implementation strategies for Write Once Read Many (WORM) storage in evidence management systems.",
            ["worm", "storage", "compliance", "evidence"],
            1.0
        ),
        SearchDocument(
            "5",
            "RFC 3161 Timestamping for Legal Evidence",
            "Applying RFC 3161-compliant timestamping authorities to evidence for court admissibility and provenance tracking.",
            ["rfc3161", "timestamp", "provenance", "court"],
            1.0
        ),
        SearchDocument(
            "6",
            "Evidence Deduplication Techniques",
            "Approaches to deduplication in evidence repositories, leveraging document fingerprinting and hash-based comparison.",
            ["deduplication", "fingerprinting", "hash"],
            1.0
        ),
        SearchDocument(
            "7",
            "Document Fingerprinting Algorithms",
            "An analysis of document fingerprinting algorithms for identifying duplicate or altered evidence files.",
            ["fingerprinting", "algorithms", "evidence"],
            1.0
        ),
        SearchDocument(
            "8",
            "Metadata Preservation in Evidence Handling",
            "Guidelines for preserving metadata during evidence acquisition, transfer, and storage.",
            ["metadata", "preservation", "handling"],
            1.0
        ),
        SearchDocument(
            "9",
            "Evidence Integrity Verification Methods",
            "Techniques for verifying the integrity of digital evidence, including hash validation and chain of custody review.",
            ["integrity", "verification", "hash", "chain_of_custody"],
            1.0
        ),
        SearchDocument(
            "10",
            "Tamper Detection Mechanisms",
            "Overview of tamper detection mechanisms for physical and digital evidence, such as seals and cryptographic hashes.",
            ["tamper_detection", "cryptography", "seals"],
            1.0
        ),
        SearchDocument(
            "11",
            "Evidence Classification Taxonomy",
            "Developing a taxonomy for classifying evidence types to support retrieval and retention policy enforcement.",
            ["classification", "taxonomy", "retention"],
            1.0
        ),
        SearchDocument(
            "12",
            "Retention Policy Enforcement in Evidence Systems",
            "Automated and manual strategies for enforcing evidence retention policies in compliance with legal requirements.",
            ["retention", "policy", "enforcement", "compliance"],
            1.0
        ),
        SearchDocument(
            "13",
            "Evidence Retrieval Indexing Techniques",
            "Indexing strategies for efficient evidence retrieval, including inverted indexes and cross-reference mapping.",
            ["retrieval", "indexing", "cross_reference"],
            1.0
        ),
        SearchDocument(
            "14",
            "Cross-Reference Mapping for Evidence",
            "How to implement cross-reference mapping to link related evidence items and support provenance tracking.",
            ["cross_reference", "mapping", "provenance"],
            1.0
        ),
        SearchDocument(
            "15",
            "Evidence Provenance Tracking",
            "Best practices for tracking the provenance of evidence, ensuring authenticity and admissibility.",
            ["provenance", "tracking", "authenticity"],
            1.0
        ),
        SearchDocument(
            "16",
            "Court Admissibility Requirements for Digital Evidence",
            "Legal standards and requirements for admitting digital evidence in court, including integrity and chain of custody.",
            ["court", "admissibility", "digital_evidence"],
            1.0
        ),
        SearchDocument(
            "17",
            "Electronic Discovery Compliance",
            "Ensuring evidence management systems comply with electronic discovery (e-discovery) regulations.",
            ["ediscovery", "compliance", "regulations"],
            1.0
        ),
        SearchDocument(
            "18",
            "Evidence Sealing Procedures",
            "Procedures for sealing evidence, both physical and digital, to maintain integrity and prevent tampering.",
            ["sealing", "procedures", "integrity"],
            1.0
        ),
        SearchDocument(
            "19",
            "Evidence Redaction Guidelines",
            "Guidelines for redacting sensitive information from evidence while preserving admissibility.",
            ["redaction", "guidelines", "admissibility"],
            1.0
        ),
        SearchDocument(
            "20",
            "Evidence Access Control Models",
            "Models for controlling access to evidence, including role-based and attribute-based access control.",
            ["access_control", "models", "evidence"],
            1.0
        ),
        SearchDocument(
            "21",
            "Digital Evidence Audit Trails",
            "Maintaining comprehensive audit trails for all evidence actions to support chain of custody and compliance.",
            ["audit_trail", "digital_evidence", "chain_of_custody"],
            1.0
        ),
        SearchDocument(
            "22",
            "Hash Chain Construction in Evidence Bundling",
            "How to construct and verify hash chains when bundling multiple pieces of evidence.",
            ["hash_chain", "bundling", "verification"],
            1.0
        ),
        SearchDocument(
            "23",
            "WORM Storage: Implementation Pitfalls",
            "Common pitfalls in implementing WORM storage for evidence and how to avoid them.",
            ["worm", "storage", "pitfalls"],
            1.0
        ),
        SearchDocument(
            "24",
            "RFC 3161 Timestamping Authorities",
            "Selecting and integrating RFC 3161-compliant timestamping authorities in evidence workflows.",
            ["rfc3161", "timestamping", "authorities"],
            1.0
        ),
        SearchDocument(
            "25",
            "Evidence Bundler: System Architecture",
            "An overview of the S05 Evidence Bundler's architecture, focusing on hash chain construction, deduplication, and metadata preservation.",
            ["evidence_bundler", "architecture", "hash_chain", "deduplication", "metadata"],
            1.0
        ),
        SearchDocument(
            "26",
            "Retention Policy Automation",
            "Automating retention policy enforcement using classification taxonomy and evidence indexing.",
            ["retention", "automation", "classification", "indexing"],
            1.0
        ),
        SearchDocument(
            "27",
            "Tamper-Evident Packaging Materials",
            "A review of tamper-evident packaging materials for physical evidence and their compliance standards.",
            ["tamper_evident", "packaging", "compliance"],
            1.0
        ),
        SearchDocument(
            "28",
            "Evidence Access Logs and Monitoring",
            "Implementing access logs and monitoring to detect unauthorized evidence access.",
            ["access_logs", "monitoring", "evidence"],
            1.0
        ),
        SearchDocument(
            "29",
            "Document Fingerprinting for Deduplication",
            "Using document fingerprinting for efficient deduplication in large-scale evidence repositories.",
            ["fingerprinting", "deduplication", "repositories"],
            1.0
        ),
        SearchDocument(
            "30",
            "Metadata Handling in Evidence Transfers",
            "Ensuring metadata is preserved and validated during evidence transfers between systems.",
            ["metadata", "transfers", "validation"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)
    idx._preseeded = True