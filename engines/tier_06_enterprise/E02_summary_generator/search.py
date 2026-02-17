import threading
import math
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[str, str], float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = dict(tf)
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scores = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            doc_weight = self.documents[doc_id].weight
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            final_score *= doc_weight
            scores[doc_id] = final_score
        top_docs = heapq.nlargest(limit, scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "document_count": self.N,
                "average_document_length": self.avg_doc_length,
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
        N = self.N
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5)) if df > 0 else 0.0
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf_doc = self.term_freqs.get(doc_id, {})
        for term in query_terms:
            tf = tf_doc.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            score += idf * tf * (self.k1 + 1) / denom
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        tf_doc = self.term_freqs.get(doc_id, {})
        doc_len = self.doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in query_terms:
            key = (term, doc_id)
            if key in self._tfidf_cache:
                score += self._tfidf_cache[key]
                continue
            tf = tf_doc.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            tfidf = tf_norm * idf
            self._tfidf_cache[key] = tfidf
            score += tfidf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({term})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

# Singleton factory for SearchIndex
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
            "1",
            "Executive Summary Structure Best Practices",
            "An effective executive summary should begin with a concise overview, followed by key findings, risks, and recommendations. Structure enhances clarity and ensures all critical points are addressed.",
            ["structure", "summary", "best_practices"],
            1.0
        ),
        SearchDocument(
            "2",
            "Extracting Key Findings from Reports",
            "Key findings extraction involves identifying statements that have significant impact, are supported by evidence, and are actionable. Use bullet points for clarity.",
            ["key_findings", "extraction", "reports"],
            1.0
        ),
        SearchDocument(
            "3",
            "Formatting Risk Highlights in Executive Summaries",
            "Risks should be formatted using bold or bullet points. Prioritize risks by likelihood and materiality. Each risk should be succinctly described.",
            ["risk", "formatting", "summary"],
            1.0
        ),
        SearchDocument(
            "4",
            "Synthesizing Recommendations for Executives",
            "Recommendations must be actionable, prioritized, and directly linked to findings. Use clear, audience-appropriate language and avoid technical jargon.",
            ["recommendations", "synthesis", "executive"],
            1.0
        ),
        SearchDocument(
            "5",
            "Aggregating Insights from Multiple Sources",
            "Multi-source aggregation requires reconciling conflicting information and highlighting consensus. Use comparative tables or summary bullets.",
            ["aggregation", "multi-source", "insights"],
            1.0
        ),
        SearchDocument(
            "6",
            "Generating Document Abstracts",
            "A document abstract should summarize the purpose, methods, key findings, and recommendations in 3-5 sentences.",
            ["abstract", "generation", "summary"],
            1.0
        ),
        SearchDocument(
            "7",
            "Prioritizing Findings in Executive Summaries",
            "Findings should be ranked by materiality and relevance to the audience. Use numbering or bullet points to indicate priority.",
            ["prioritization", "findings", "executive"],
            1.0
        ),
        SearchDocument(
            "8",
            "Filtering Materiality in Summaries",
            "Materiality filtering ensures only findings with significant impact are included. Exclude minor or irrelevant details.",
            ["materiality", "filtering", "summary"],
            1.0
        ),
        SearchDocument(
            "9",
            "Adapting Language for Executive Audiences",
            "Use concise, non-technical language. Avoid jargon and focus on actionable insights relevant to business objectives.",
            ["language", "audience", "executive"],
            1.0
        ),
        SearchDocument(
            "10",
            "Optimizing Summary Length",
            "Summaries should be brief, typically one page or less. Remove redundancies and focus on essential information only.",
            ["length", "optimization", "summary"],
            1.0
        ),
        SearchDocument(
            "11",
            "Distilling Bullet Points from Complex Reports",
            "Distillation involves breaking down complex findings into short, clear bullet points. Each bullet should represent a single idea.",
            ["bullet_points", "distillation", "reports"],
            1.0
        ),
        SearchDocument(
            "12",
            "Executive Summary: Structure and Flow",
            "Start with context, present key findings, highlight risks, and conclude with recommendations. Maintain logical flow.",
            ["structure", "flow", "summary"],
            1.0
        ),
        SearchDocument(
            "13",
            "Key Findings: Evidence and Actionability",
            "Key findings must be evidence-based and actionable. Link each finding to supporting data.",
            ["key_findings", "evidence", "actionability"],
            1.0
        ),
        SearchDocument(
            "14",
            "Risk Highlighting: Visual Emphasis",
            "Use color, bolding, or icons to emphasize critical risks. Place risk highlights near the beginning of the summary.",
            ["risk", "visual", "highlighting"],
            1.0
        ),
        SearchDocument(
            "15",
            "Recommendation Synthesis: Grouping and Prioritization",
            "Group recommendations by theme and prioritize based on impact and feasibility.",
            ["recommendations", "synthesis", "prioritization"],
            1.0
        ),
        SearchDocument(
            "16",
            "Multi-Source Aggregation: Conflict Resolution",
            "When sources conflict, note discrepancies and provide rationale for chosen conclusions.",
            ["aggregation", "conflict", "resolution"],
            1.0
        ),
        SearchDocument(
            "17",
            "Abstract Generation: Automation Techniques",
            "Leverage NLP tools to automate abstract generation, ensuring consistency and completeness.",
            ["abstract", "automation", "NLP"],
            1.0
        ),
        SearchDocument(
            "18",
            "Findings Prioritization: Scoring Models",
            "Apply scoring models to rank findings by materiality, risk, and relevance.",
            ["prioritization", "scoring", "findings"],
            1.0
        ),
        SearchDocument(
            "19",
            "Materiality Filtering: Threshold Setting",
            "Set clear thresholds for materiality to filter findings. Document rationale for inclusion/exclusion.",
            ["materiality", "filtering", "threshold"],
            1.0
        ),
        SearchDocument(
            "20",
            "Audience-Appropriate Language: Examples",
            "Example: Instead of 'systemic risk exposure,' use 'potential for significant loss.'",
            ["language", "audience", "examples"],
            1.0
        ),
        SearchDocument(
            "21",
            "Summary Length Optimization: Metrics",
            "Track summary length and readability metrics to ensure optimal communication.",
            ["length", "optimization", "metrics"],
            1.0
        ),
        SearchDocument(
            "22",
            "Bullet Point Distillation: Templates",
            "Use templates for bullet points to ensure consistency in format and tone.",
            ["bullet_points", "templates", "distillation"],
            1.0
        ),
        SearchDocument(
            "23",
            "Executive Summary: Common Pitfalls",
            "Avoid excessive detail, technical jargon, and unsubstantiated claims in executive summaries.",
            ["summary", "pitfalls", "executive"],
            1.0
        ),
        SearchDocument(
            "24",
            "Key Findings Extraction: Automation",
            "Automate extraction of key findings using text analysis tools to improve efficiency.",
            ["key_findings", "automation", "extraction"],
            1.0
        ),
        SearchDocument(
            "25",
            "Materiality Filtering: Case Studies",
            "Case studies demonstrate the impact of effective materiality filtering on decision-making.",
            ["materiality", "filtering", "case_study"],
            1.0
        ),
        SearchDocument(
            "26",
            "Summary Bullet Points: Impactful Writing",
            "Write bullet points that are direct, specific, and outcome-focused for maximum impact.",
            ["bullet_points", "writing", "impact"],
            1.0
        ),
        SearchDocument(
            "27",
            "Risk Highlight Formatting: Regulatory Compliance",
            "Ensure risk highlights comply with regulatory requirements and internal standards.",
            ["risk", "formatting", "compliance"],
            1.0
        ),
        SearchDocument(
            "28",
            "Recommendation Synthesis: Stakeholder Alignment",
            "Align recommendations with stakeholder interests and strategic objectives.",
            ["recommendations", "synthesis", "stakeholders"],
            1.0
        ),
        SearchDocument(
            "29",
            "Multi-Source Aggregation: Data Integration",
            "Integrate data from multiple sources to create a unified executive summary.",
            ["aggregation", "data_integration", "multi-source"],
            1.0
        ),
        SearchDocument(
            "30",
            "Document Abstract Generation: Best Practices",
            "Follow best practices for abstract generation: clarity, brevity, and focus on outcomes.",
            ["abstract", "generation", "best_practices"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)