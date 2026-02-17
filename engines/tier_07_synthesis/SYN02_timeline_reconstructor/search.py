import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Tuple

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
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_tf: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.term_doc_tfidf: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.total_terms: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # Ignore duplicates
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.term_doc_freq[token] += 1
                self.term_doc_tf[token][doc.id] = count
            self._update_avg_doc_length()
            self._invalidate_idf_cache()
            self._update_tfidf(doc.id, token_counts)

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        doc_scores: Dict[str, float] = defaultdict(float)
        doc_snippets: Dict[str, str] = {}
        for token in tokens:
            idf = self._compute_idf(token)
            for doc_id in self.term_doc_tf[token]:
                tf = self.term_doc_tf[token][doc_id]
                score = self._score_bm25(token, doc_id, tf, idf)
                doc_scores[doc_id] += score
        # Add TF-IDF scoring
        for token in tokens:
            for doc_id in self.term_doc_tfidf[token]:
                doc_scores[doc_id] += self.term_doc_tfidf[token][doc_id]
        # Weight adjustment
        for doc_id in doc_scores:
            doc_scores[doc_id] *= self.documents[doc_id].weight
        # Snippet generation
        for doc_id in doc_scores:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, tokens)
            doc_snippets[doc_id] = snippet
        # Sort and return
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            results.append(SearchResult(doc_id, score, doc.title, doc_snippets[doc_id]))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": len(self.documents),
                "avg_doc_length": self.avg_doc_length,
                "total_terms": self.total_terms,
                "num_unique_terms": len(self.term_doc_freq)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, token: str) -> float:
        if token in self._idf_cache:
            return self._idf_cache[token]
        N = len(self.documents)
        df = self.term_doc_freq.get(token, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[token] = idf
        return idf

    def _score_bm25(self, token: str, doc_id: str, tf: int, idf: float) -> float:
        doc_len = self.doc_lengths[doc_id]
        avg_len = self.avg_doc_length if self.avg_doc_length > 0 else 1
        numerator = tf * (self._bm25_k1 + 1)
        denominator = tf + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_len)
        return idf * numerator / denominator

    def _update_avg_doc_length(self):
        if self.documents:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.documents)
        else:
            self.avg_doc_length = 0.0

    def _invalidate_idf_cache(self):
        self._idf_cache = {}

    def _update_tfidf(self, doc_id: str, token_counts: Counter):
        doc_len = self.doc_lengths[doc_id]
        for token, tf in token_counts.items():
            norm_tf = tf / doc_len
            idf = self._compute_idf(token)
            self.term_doc_tfidf[token][doc_id] = norm_tf * idf

    def _make_snippet(self, content: str, tokens: List[str], window: int = 30) -> str:
        content_lower = content.lower()
        best_pos = -1
        best_token = ''
        for token in tokens:
            pos = content_lower.find(token)
            if pos != -1:
                best_pos = pos
                best_token = token
                break
        if best_pos == -1:
            return content[:window] + '...' if len(content) > window else content
        start = max(0, best_pos - window // 2)
        end = min(len(content), best_pos + window // 2)
        snippet = content[start:end]
        # Highlight token
        snippet = re.sub(r'(?i)\b{}\b'.format(re.escape(best_token)), '[{}]'.format(best_token), snippet)
        return snippet + '...'

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

# --- Pre-seed Domain Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            "doc1",
            "Event Extraction from Pleadings",
            "This document discusses methodologies for extracting events from legal pleadings, including entity recognition, event triggers, and argument identification.",
            ["event_extraction", "pleadings", "nlp"],
            1.0
        ),
        SearchDocument(
            "doc2",
            "Date Normalization and Formatting",
            "Techniques for normalizing dates found in legal documents, including conversion to ISO formats and handling ambiguous date expressions.",
            ["date_normalization", "formatting", "legal_dates"],
            1.0
        ),
        SearchDocument(
            "doc3",
            "Temporal Ordering Algorithms",
            "Overview of algorithms for ordering events temporally, such as topological sort, interval trees, and causal inference in legal timelines.",
            ["temporal_ordering", "algorithms", "timeline"],
            1.0
        ),
        SearchDocument(
            "doc4",
            "Gap Detection Heuristics",
            "Heuristics for detecting gaps in event timelines, including missing dates, unexplained periods, and legal consequences of timeline gaps.",
            ["gap_detection", "heuristics", "timeline"],
            1.0
        ),
        SearchDocument(
            "doc5",
            "Parallel Track Identification",
            "Identifying parallel procedural tracks in litigation, such as concurrent discovery, appeals, and regulatory actions.",
            ["parallel_tracks", "litigation", "procedural"],
            1.0
        ),
        SearchDocument(
            "doc6",
            "Statute of Limitations Calculation",
            "Methods for calculating statutes of limitations, including tolling, accrual, and jurisdictional differences.",
            ["statute_of_limitations", "calculation", "tolling"],
            1.0
        ),
        SearchDocument(
            "doc7",
            "Deadline Cascade Analysis",
            "Analysis of cascading deadlines in legal proceedings, including dependencies between deadlines and risk of deadline failures.",
            ["deadline_cascade", "analysis", "legal_deadlines"],
            1.0
        ),
        SearchDocument(
            "doc8",
            "Critical Path Identification",
            "Identifying the critical path in legal timelines, focusing on bottlenecks and essential events for case resolution.",
            ["critical_path", "timeline", "bottleneck"],
            1.0
        ),
        SearchDocument(
            "doc9",
            "Temporal Inconsistency Detection",
            "Detecting inconsistencies in event timelines, such as contradictory dates, overlapping events, and retroactive actions.",
            ["temporal_inconsistency", "detection", "timeline"],
            1.0
        ),
        SearchDocument(
            "doc10",
            "Gantt Chart Representation",
            "Using Gantt charts to visually represent legal timelines, including event durations, dependencies, and milestones.",
            ["gantt_chart", "visualization", "timeline"],
            1.0
        ),
        SearchDocument(
            "doc11",
            "Relation Back Doctrine",
            "Explaining the relation back doctrine in civil procedure, including amendment of pleadings and retroactive effect.",
            ["relation_back", "doctrine", "civil_procedure"],
            1.0
        ),
        SearchDocument(
            "doc12",
            "Nunc Pro Tunc Orders",
            "Legal principles behind nunc pro tunc orders, retroactive judicial actions, and their effect on timelines.",
            ["nunc_pro_tunc", "orders", "retroactive"],
            1.0
        ),
        SearchDocument(
            "doc13",
            "Retroactive Application of Law",
            "Analysis of retroactive application of statutes and judicial decisions, including ex post facto concerns.",
            ["retroactive_application", "law", "statutes"],
            1.0
        ),
        SearchDocument(
            "doc14",
            "Document Dating Forensics",
            "Forensic techniques for dating legal documents, including ink analysis, paper aging, and metadata examination.",
            ["document_dating", "forensics", "legal_documents"],
            1.0
        ),
        SearchDocument(
            "doc15",
            "Multi-Jurisdiction Timeline Conflicts",
            "Resolving timeline conflicts across jurisdictions, including forum shopping, concurrent proceedings, and choice of law.",
            ["multi_jurisdiction", "timeline", "conflicts"],
            1.0
        ),
        SearchDocument(
            "doc16",
            "Discovery Timeline Planning",
            "Planning discovery timelines, including scheduling orders, production deadlines, and managing delays.",
            ["discovery_timeline", "planning", "scheduling"],
            1.0
        ),
        SearchDocument(
            "doc17",
            "Contract Performance Milestones",
            "Identifying and tracking contract performance milestones, including payment schedules, deliverables, and breach triggers.",
            ["contract_performance", "milestones", "contracts"],
            1.0
        ),
        SearchDocument(
            "doc18",
            "Appeal Timeline and Finality",
            "Understanding appeal timelines, finality of judgments, and procedural steps for appellate review.",
            ["appeal_timeline", "finality", "judgments"],
            1.0
        ),
        SearchDocument(
            "doc19",
            "Regulatory Compliance Deadlines",
            "Managing regulatory compliance deadlines, including periodic filings, reporting requirements, and enforcement actions.",
            ["regulatory_compliance", "deadlines", "filings"],
            1.0
        ),
        SearchDocument(
            "doc20",
            "Bankruptcy Timeline and Automatic Stay",
            "Bankruptcy timeline analysis, automatic stay triggers, and effects on ongoing litigation.",
            ["bankruptcy_timeline", "automatic_stay", "litigation"],
            1.0
        ),
        SearchDocument(
            "doc21",
            "Witness Testimony Timeline Consistency",
            "Ensuring consistency of witness testimony with event timelines, including cross-examination and impeachment strategies.",
            ["witness_testimony", "timeline", "consistency"],
            1.0
        ),
        SearchDocument(
            "doc22",
            "Corporate Transaction Timeline",
            "Tracking corporate transaction timelines, including mergers, acquisitions, and regulatory approvals.",
            ["corporate_transaction", "timeline", "mergers"],
            1.0
        ),
        SearchDocument(
            "doc23",
            "Statute of Repose",
            "Explaining statute of repose, differences from statute of limitations, and impact on legal claims.",
            ["statute_of_repose", "limitations", "legal_claims"],
            1.0
        ),
        SearchDocument(
            "doc24",
            "Laches and Equitable Estoppel",
            "Legal doctrines of laches and equitable estoppel, including delay, prejudice, and timeline effects.",
            ["laches", "equitable_estoppel", "timeline"],
            1.0
        ),
        SearchDocument(
            "doc25",
            "Insurance Notice and Claim Timeline",
            "Managing insurance notice and claim timelines, including reporting requirements, coverage triggers, and denial risks.",
            ["insurance_notice", "claim_timeline", "coverage"],
            1.0
        ),
        SearchDocument(
            "doc26",
            "Legal Timeline Reconstruction Algorithms",
            "Survey of algorithms for reconstructing legal timelines from pleadings, evidence, and procedural history.",
            ["timeline_reconstruction", "algorithms", "pleadings"],
            1.0
        ),
        SearchDocument(
            "doc27",
            "Deadline Management in Multi-Party Litigation",
            "Strategies for managing deadlines in multi-party litigation, including coordination, communication, and risk mitigation.",
            ["deadline_management", "multi_party", "litigation"],
            1.0
        ),
        SearchDocument(
            "doc28",
            "Temporal Reasoning in Legal AI",
            "Approaches to temporal reasoning in legal artificial intelligence, including event extraction, timeline generation, and inconsistency detection.",
            ["temporal_reasoning", "legal_ai", "event_extraction"],
            1.0
        ),
        SearchDocument(
            "doc29",
            "Procedural Timeline Visualization Tools",
            "Overview of visualization tools for procedural timelines, including Gantt charts, flow diagrams, and interactive dashboards.",
            ["procedural_timeline", "visualization", "tools"],
            1.0
        ),
        SearchDocument(
            "doc30",
            "Deadline Tolling and Extensions",
            "Legal principles of deadline tolling and extensions, including statutory exceptions, judicial discretion, and equitable doctrines.",
            ["deadline_tolling", "extensions", "legal_deadlines"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)