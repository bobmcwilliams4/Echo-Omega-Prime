import math
import threading
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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self._bm25_k1 = bm25_k1
        self._bm25_b = bm25_b
        self._documents: Dict[str, SearchDocument] = {}
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self._doc_lengths: Dict[str, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.RLock()

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            term_freq = Counter(tokens)
            self._documents[doc.id] = doc
            self._doc_lengths[doc.id] = len(tokens)
            for term, freq in term_freq.items():
                self._term_doc_freqs[term][doc.id] = freq
                self._doc_freqs[term] += 1
            self._total_docs += 1
            self._avg_doc_length = (
                sum(self._doc_lengths.values()) / self._total_docs
                if self._total_docs else 0.0
            )
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []
        candidate_docs = set()
        for term in tokens:
            candidate_docs.update(self._term_doc_freqs.get(term, {}).keys())
        scored: List[Tuple[str, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, tokens)
            tfidf_score = self._score_tfidf(doc_id, tokens)
            doc_weight = self._documents[doc_id].weight
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            score *= doc_weight
            scored.append((doc_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored[:limit]:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                'total_documents': self._total_docs,
                'avg_doc_length': self._avg_doc_length,
                'unique_terms': len(self._doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        with self._lock:
            if term in self._idf_cache:
                return self._idf_cache[term]
            df = self._doc_freqs.get(term, 0)
            N = self._total_docs
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5)) if df else 0.0
            self._idf_cache[term] = idf
            return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 0)
        avg_dl = self._avg_doc_length or 1.0
        for term in query_terms:
            tf = self._term_doc_freqs.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self._bm25_k1 + 1)
            denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 1)
        for term in query_terms:
            tf = self._term_doc_freqs.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        best_idx = -1
        best_term = ''
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1 and (best_idx == -1 or idx < best_idx):
                best_idx = idx
                best_term = term
        if best_idx == -1:
            snippet = content[:window * 2]
        else:
            start = max(0, best_idx - window)
            end = min(len(content), best_idx + window)
            snippet = content[start:end]
        # Highlight query terms
        for term in set(query_terms):
            snippet = re.sub(r'(?i)\b' + re.escape(term) + r'\b', r'**\g<0>**', snippet)
        return snippet.strip()

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

# --- Pre-seeding Domain Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            "1",
            "Template Architecture Overview",
            "Describes the modular structure of document templates, including inheritance, composition, and extensibility for legal documents.",
            ["template", "architecture", "modularity"], 1.0
        ),
        SearchDocument(
            "2",
            "Clause Library Taxonomy",
            "Outlines the hierarchical organization of clause libraries, including tagging, categorization, and cross-domain mapping.",
            ["clause", "library", "taxonomy"], 1.0
        ),
        SearchDocument(
            "3",
            "Conditional Clause Inclusion Logic",
            "Explains the rules and logic for conditional inclusion of clauses based on deal parameters and jurisdiction.",
            ["conditional", "logic", "assembly"], 1.0
        ),
        SearchDocument(
            "4",
            "Variable Substitution and Data Binding",
            "Details the mechanisms for variable substitution, data binding, and runtime value resolution in document assembly.",
            ["variable", "substitution", "data"], 1.0
        ),
        SearchDocument(
            "5",
            "Cross-Reference Integrity Management",
            "Covers techniques for managing and validating cross-references within complex assembled documents.",
            ["cross-reference", "integrity", "validation"], 1.0
        ),
        SearchDocument(
            "6",
            "Defined Terms Consistency",
            "Discusses strategies to ensure consistent use and definition of terms across assembled documents.",
            ["defined terms", "consistency"], 1.0
        ),
        SearchDocument(
            "7",
            "Exhibit and Schedule Auto-Generation",
            "Describes automated generation and attachment of exhibits and schedules based on template logic.",
            ["exhibit", "schedule", "auto-generation"], 1.0
        ),
        SearchDocument(
            "8",
            "Redlining and Document Comparison",
            "Explains redlining features, change tracking, and document comparison workflows in the engine.",
            ["redlining", "comparison", "change tracking"], 1.0
        ),
        SearchDocument(
            "9",
            "Document Version Control and Branching",
            "Outlines version control, branching, and merge strategies for document templates and assembled documents.",
            ["version control", "branching", "merge"], 1.0
        ),
        SearchDocument(
            "10",
            "Signature Block Standards",
            "Defines standards and formatting rules for signature blocks, including multi-party and jurisdictional requirements.",
            ["signature", "standards", "formatting"], 1.0
        ),
        SearchDocument(
            "11",
            "Jurisdictional Customization and Compliance",
            "Explores methods for customizing templates and clauses to comply with specific jurisdictional requirements.",
            ["jurisdiction", "customization", "compliance"], 1.0
        ),
        SearchDocument(
            "12",
            "Template Version Control Lifecycle",
            "Describes the lifecycle of template versions, including approval, deprecation, and migration.",
            ["template", "version control", "lifecycle"], 1.0
        ),
        SearchDocument(
            "13",
            "Clause Approval and Governance Workflow",
            "Explains the governance process for clause approval, audit trails, and workflow automation.",
            ["clause", "approval", "governance"], 1.0
        ),
        SearchDocument(
            "14",
            "External Data Source Integration",
            "Covers integration patterns for external data sources, APIs, and real-time data feeds in document assembly.",
            ["integration", "external data", "api"], 1.0
        ),
        SearchDocument(
            "15",
            "Multi-Format Output Generation",
            "Details supported output formats (PDF, DOCX, HTML, XML) and conversion strategies.",
            ["output", "format", "conversion"], 1.0
        ),
        SearchDocument(
            "16",
            "Assembly Performance and Scalability",
            "Discusses performance optimization and scalability strategies for high-volume document assembly.",
            ["performance", "scalability", "optimization"], 1.0
        ),
        SearchDocument(
            "17",
            "Assembly Audit Trail and Compliance",
            "Explains audit trail generation, compliance logging, and traceability in document assembly.",
            ["audit", "compliance", "traceability"], 1.0
        ),
        SearchDocument(
            "18",
            "Error Handling and Recovery in Assembly",
            "Describes error detection, reporting, and recovery mechanisms in the assembly process.",
            ["error handling", "recovery", "robustness"], 1.0
        ),
        SearchDocument(
            "19",
            "Template Testing and Quality Assurance",
            "Covers automated and manual testing strategies for template correctness and quality.",
            ["testing", "quality assurance", "template"], 1.0
        ),
        SearchDocument(
            "20",
            "User Interface for Document Assembly",
            "Describes UI/UX patterns for interactive document assembly, including preview, editing, and collaboration.",
            ["user interface", "ui", "collaboration"], 1.0
        ),
        SearchDocument(
            "21",
            "Bulk Document Generation",
            "Explains batch processing, bulk generation, and parallel assembly of documents.",
            ["bulk", "batch", "processing"], 1.0
        ),
        SearchDocument(
            "22",
            "Collaborative Document Assembly",
            "Discusses real-time and asynchronous collaboration features in document assembly workflows.",
            ["collaboration", "real-time", "workflow"], 1.0
        ),
        SearchDocument(
            "23",
            "Regulatory Compliance Document Generation",
            "Outlines strategies for generating documents that meet regulatory compliance standards.",
            ["regulatory", "compliance", "generation"], 1.0
        ),
        SearchDocument(
            "24",
            "Change Impact Analysis for Templates",
            "Explains tools and methods for analyzing the impact of template changes on downstream documents.",
            ["change", "impact analysis", "templates"], 1.0
        ),
        SearchDocument(
            "25",
            "Contract Lifecycle Management Integration",
            "Describes integration points and data flows with contract lifecycle management (CLM) systems.",
            ["contract", "lifecycle", "integration"], 1.0
        ),
        SearchDocument(
            "26",
            "AI-Assisted Natural Language Generation",
            "Covers the use of AI for generating and suggesting legal language in templates and clauses.",
            ["ai", "natural language", "generation"], 1.0
        ),
        SearchDocument(
            "27",
            "Dynamic Clause Parameterization",
            "Explains parameter-driven clause customization and dynamic assembly logic.",
            ["dynamic", "parameterization", "clause"], 1.0
        ),
        SearchDocument(
            "28",
            "Automated Cross-Reference Updating",
            "Describes algorithms for automatic updating of cross-references after document edits.",
            ["cross-reference", "automation", "updating"], 1.0
        ),
        SearchDocument(
            "29",
            "Template Migration and Backward Compatibility",
            "Covers migration strategies for template upgrades and ensuring backward compatibility.",
            ["migration", "compatibility", "template"], 1.0
        ),
        SearchDocument(
            "30",
            "Clause Usage Analytics",
            "Discusses analytics and reporting on clause usage, frequency, and effectiveness.",
            ["analytics", "usage", "clause"], 1.0
        ),
        SearchDocument(
            "31",
            "Document Assembly Security Best Practices",
            "Outlines security considerations and best practices for document assembly systems.",
            ["security", "best practices", "assembly"], 1.0
        ),
        SearchDocument(
            "32",
            "Template Localization and Internationalization",
            "Explains localization, translation, and internationalization of templates and clauses.",
            ["localization", "internationalization", "template"], 1.0
        ),
        SearchDocument(
            "33",
            "Automated Signature Collection",
            "Describes workflows and integrations for automated electronic signature collection.",
            ["signature", "automation", "collection"], 1.0
        ),
        SearchDocument(
            "34",
            "Clause Dependency Resolution",
            "Explains logic for resolving dependencies between clauses during assembly.",
            ["clause", "dependency", "resolution"], 1.0
        ),
        SearchDocument(
            "35",
            "Template Approval Workflow Automation",
            "Covers automation of template approval, notifications, and audit trails.",
            ["template", "approval", "workflow"], 1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)