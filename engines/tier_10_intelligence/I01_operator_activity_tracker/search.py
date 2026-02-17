import math
import threading
import heapq
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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self._re_token = re.compile(r'\b\w+\b')
        self._preseeded = False

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._re_token.findall(text)]

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.doc_freqs[term] += 1
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        doc = self.documents[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + k1 * (1 - b + b * doc_len / avg_dl)
            score += idf * (f * (k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        score = 0.0
        for term in query_terms:
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores = []
        for doc_id in self.documents:
            if method == "bm25":
                score = self._score_bm25(query_terms, doc_id)
            elif method == "tfidf":
                score = self._score_tfidf(query_terms, doc_id)
            else:
                raise ValueError("Unknown search method")
            if score > 0:
                scores.append((score, doc_id))
        top = heapq.nlargest(limit, scores)
        results = []
        for score, doc_id in top:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:snippet_len]
        else:
            pos = positions[0]
            start = max(0, pos - 10)
            end = min(len(tokens), pos + 20)
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:snippet_len] + ('...' if len(snippet) > snippet_len else '')

    def get_stats(self) -> Dict[str, int]:
        return {
            'num_documents': self.N,
            'num_terms': len(self.doc_freqs),
            'avg_doc_length': int(self.avg_doc_length),
        }

    def _preseed(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1,
                "RRC Operator P-5 Organization Report Requirements",
                "The P-5 Organization Report is required for all operators in Texas. It includes details on company structure, responsible parties, and financial assurance. Annual renewal is mandatory.",
                ["P-5", "RRC", "Operator", "Regulatory"], 1.0
            ),
            SearchDocument(
                2,
                "W-1 Drilling Permit Application Process",
                "Operators must file a W-1 Drilling Permit Application before commencing drilling operations. The application includes well location, target formation, and proposed depth.",
                ["W-1", "Permit", "Drilling", "Application"], 1.0
            ),
            SearchDocument(
                3,
                "W-1A Recompletions and Amendments",
                "The W-1A form is used to report recompletions and amendments to existing drilling permits. Operators must provide updated wellbore information and completion intervals.",
                ["W-1A", "Recompletion", "Amendment"], 1.0
            ),
            SearchDocument(
                4,
                "Completion Reports: G-1 and G-4",
                "Completion reports G-1 (Gas) and G-4 (Oil) are filed after well completion. They detail production test results, completion intervals, and stimulation methods.",
                ["Completion", "G-1", "G-4", "Reporting"], 1.0
            ),
            SearchDocument(
                5,
                "Production Report PR Filing",
                "Monthly PR (Production Report) filings are required for all producing wells. Reports must include oil, gas, and water volumes for each lease.",
                ["Production", "PR", "Reporting"], 1.0
            ),
            SearchDocument(
                6,
                "Operator Transfer: P-4 Requirements",
                "P-4 forms are used to transfer operator responsibility for wells. Both the current and new operator must submit documentation to the RRC.",
                ["P-4", "Operator Transfer", "Regulatory"], 1.0
            ),
            SearchDocument(
                7,
                "Well Plugging: W-3 and W-3A",
                "W-3 and W-3A forms are required for plugging and abandoning wells. The operator must provide details on cementing, casing removal, and site restoration.",
                ["W-3", "Plugging", "Abandonment"], 1.0
            ),
            SearchDocument(
                8,
                "Operator Activity Scoring Methodology",
                "Operator activity is scored based on permit filings, completions, production volumes, and regulatory compliance. Scores are normalized for portfolio size.",
                ["Activity", "Scoring", "Operator"], 1.2
            ),
            SearchDocument(
                9,
                "Drilling Rig Count Analysis",
                "Rig count analysis tracks active drilling rigs by basin, operator, and well type. Trends indicate capital allocation and drilling intensity.",
                ["Rig Count", "Drilling", "Analysis"], 1.0
            ),
            SearchDocument(
                10,
                "Permit-to-Spud Timing Metrics",
                "Permit-to-spud timing measures the interval between permit approval and drilling commencement. Shorter intervals suggest operational efficiency.",
                ["Permit", "Spud", "Timing"], 1.0
            ),
            SearchDocument(
                11,
                "Completion Success Rates",
                "Completion success rates are calculated as the ratio of successful completions to total attempts. High rates indicate effective project execution.",
                ["Completion", "Success Rate"], 1.0
            ),
            SearchDocument(
                12,
                "Horizontal vs Vertical Well Trends",
                "Analysis of horizontal and vertical well trends reveals shifts in drilling strategy, technology adoption, and reservoir targeting.",
                ["Horizontal", "Vertical", "Well", "Trends"], 1.0
            ),
            SearchDocument(
                13,
                "Operator Portfolio Analysis",
                "Portfolio analysis evaluates an operator's asset base, well count, and production mix across basins. Diversification reduces risk.",
                ["Portfolio", "Operator", "Analysis"], 1.0
            ),
            SearchDocument(
                14,
                "Multi-Basin Operator Tracking",
                "Multi-basin tracking identifies operators active in multiple basins, highlighting geographic diversification and operational scale.",
                ["Multi-Basin", "Operator", "Tracking"], 1.0
            ),
            SearchDocument(
                15,
                "Acreage Position Estimation",
                "Acreage position estimation uses permit and lease data to infer operator land holdings and potential drilling inventory.",
                ["Acreage", "Estimation", "Land"], 1.0
            ),
            SearchDocument(
                16,
                "Operator Financial Health Indicators",
                "Financial health is assessed using metrics such as debt-to-equity ratio, cash flow, and capital expenditures. Strong financials support sustained activity.",
                ["Financial", "Health", "Operator"], 1.0
            ),
            SearchDocument(
                17,
                "JV Partner Identification",
                "Joint venture (JV) partner identification analyzes working interest assignments, P-5 affiliations, and public disclosures.",
                ["JV", "Partner", "Identification"], 1.0
            ),
            SearchDocument(
                18,
                "Frac Fleet Scheduling Optimization",
                "Frac fleet scheduling balances equipment availability, pad readiness, and crew logistics to minimize downtime and maximize completions.",
                ["Frac", "Fleet", "Scheduling"], 1.0
            ),
            SearchDocument(
                19,
                "Rig Release Analysis",
                "Rig release analysis examines the timing and frequency of rig releases, indicating project completion and capital redeployment.",
                ["Rig Release", "Analysis"], 1.0
            ),
            SearchDocument(
                20,
                "Operator Competitive Benchmarking",
                "Competitive benchmarking compares operator performance on key metrics such as drilling speed, completion efficiency, and production growth.",
                ["Benchmarking", "Operator", "Competitive"], 1.0
            ),
            SearchDocument(
                21,
                "Wellbore Data Integration for Activity Tracking",
                "Integrating wellbore data from W-1, G-1, and PR filings enables comprehensive operator activity tracking and performance analysis.",
                ["Wellbore", "Integration", "Activity"], 1.0
            ),
            SearchDocument(
                22,
                "Regulatory Compliance Monitoring",
                "Monitoring regulatory compliance involves tracking timely filings of P-5, W-1, and PR reports, as well as adherence to plugging requirements.",
                ["Compliance", "Regulatory", "Monitoring"], 1.0
            ),
            SearchDocument(
                23,
                "Inactive Well Identification",
                "Inactive wells are identified through analysis of PR filings and lack of reported production. Operators must address inactive status per RRC rules.",
                ["Inactive", "Well", "Identification"], 1.0
            ),
            SearchDocument(
                24,
                "Lease Expiration Risk Assessment",
                "Lease expiration risk is assessed by tracking permit activity and production status. Expiring leases may prompt increased drilling.",
                ["Lease", "Expiration", "Risk"], 1.0
            ),
            SearchDocument(
                25,
                "Well Spacing and Density Analysis",
                "Well spacing and density analysis evaluates permit filings and completion data to optimize resource recovery and minimize interference.",
                ["Spacing", "Density", "Analysis"], 1.0
            ),
            SearchDocument(
                26,
                "Surface Location vs Bottomhole Location Analysis",
                "Comparing surface and bottomhole locations from W-1 and G-1 filings reveals lateral lengths and drilling practices.",
                ["Surface", "Bottomhole", "Location"], 1.0
            ),
            SearchDocument(
                27,
                "Plugging Liability Estimation",
                "Plugging liability estimation uses well count, age, and plugging cost data to estimate future operator obligations.",
                ["Plugging", "Liability", "Estimation"], 1.0
            ),
            SearchDocument(
                28,
                "Pad Development Trends",
                "Pad development trends are tracked through permit clustering and completion timing, indicating multi-well development strategies.",
                ["Pad", "Development", "Trends"], 1.0
            ),
            SearchDocument(
                29,
                "Production Allocation by Operator",
                "Production allocation analysis attributes lease-level production to operators, supporting portfolio and benchmarking studies.",
                ["Production", "Allocation", "Operator"], 1.0
            ),
            SearchDocument(
                30,
                "Well Re-entry and Re-frac Activity",
                "Re-entry and re-frac activity is identified through W-1A and G-1 filings, indicating efforts to enhance recovery from existing wells.",
                ["Re-entry", "Re-frac", "Activity"], 1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

def get_search_index() -> SearchIndex:
    if not hasattr(get_search_index, "_instance"):
        idx = SearchIndex()
        idx._preseed()
        get_search_index._instance = idx
    return get_search_index._instance