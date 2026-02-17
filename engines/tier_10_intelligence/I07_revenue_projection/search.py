import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# -----------------------------
# Data Classes
# -----------------------------

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

# -----------------------------
# Search Index
# -----------------------------

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_frequencies: Dict[int, Counter] = defaultdict(Counter)
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.total_terms: int = 0
        self.lock = threading.Lock()
        self.avg_doc_length: float = 0.0
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_frequencies[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            for term in tf:
                self.inverted_index[term].add(doc.id)
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / len(self.doc_lengths)
                if self.doc_lengths else 0.0
            )
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scores = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            doc = self.documents[doc_id]
            final_score = bm25_score * 0.7 + tfidf_score * 0.3
            final_score *= doc.weight
            snippet = self._make_snippet(doc, query_terms)
            scores.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": len(self.documents),
                "avg_doc_length": self.avg_doc_length,
                "total_terms": self.total_terms,
                "unique_terms": len(self.inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self.documents)
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length or 1.0
        tf = self.term_frequencies[doc_id]
        for term in set(query_terms):
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            numer = f * (self._bm25_k1 + 1)
            score += idf * numer / denom
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_frequencies[doc_id]
        doc_len = self.doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in set(query_terms):
            term_tf = tf.get(term, 0) / doc_len
            idf = self._compute_idf(term)
            score += term_tf * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in set(query_terms):
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(min(positions) - 30, 0)
        end = min(start + 160, len(content))
        snippet = content[start:end]
        for term in set(query_terms):
            snippet = re.sub(r'(?i)(' + re.escape(term) + r')', r'**\1**', snippet)
        return snippet + ("..." if end < len(content) else "")

# -----------------------------
# Singleton Factory
# -----------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                idx = SearchIndex()
                _seed_domain_documents(idx)
                _search_index_instance = idx
    return _search_index_instance

# -----------------------------
# Domain Documents Seeding
# -----------------------------

def _seed_domain_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Exponential Decline Curve Analysis",
            "Exponential decline analysis assumes a constant percentage decline rate. The production rate at time t is given by q = q0 * exp(-D * t), where D is the decline rate.",
            ["arps", "exponential", "decline", "analysis"],
            1.0
        ),
        SearchDocument(
            2,
            "Hyperbolic Decline Curve Analysis",
            "Hyperbolic decline analysis models production with a changing decline rate. The rate equation is q = q0 / (1 + b * D * t)^(1/b), where b is the b-factor.",
            ["arps", "hyperbolic", "decline", "analysis"],
            1.0
        ),
        SearchDocument(
            3,
            "Harmonic Decline Curve Analysis",
            "Harmonic decline is a special case of hyperbolic decline with b = 1. The equation is q = q0 / (1 + D * t).",
            ["arps", "harmonic", "decline", "analysis"],
            1.0
        ),
        SearchDocument(
            4,
            "b-factor Estimation in Decline Curve Analysis",
            "The b-factor in Arps decline analysis is estimated by fitting historical production data to the hyperbolic decline model. Typical b values range from 0 (exponential) to 1 (harmonic).",
            ["arps", "b-factor", "hyperbolic", "estimation"],
            1.0
        ),
        SearchDocument(
            5,
            "Initial Production (IP) Rate Determination",
            "The initial production rate (IP) is the starting point for decline curve analysis. It is typically the stabilized rate after well cleanup.",
            ["ip", "initial production", "decline", "analysis"],
            1.0
        ),
        SearchDocument(
            6,
            "Estimated Ultimate Recovery (EUR) Calculation",
            "EUR is calculated by integrating the decline curve over the well's economic life. For exponential decline, EUR = q0 / D.",
            ["eur", "ultimate recovery", "decline", "calculation"],
            1.0
        ),
        SearchDocument(
            7,
            "Type Curve Construction",
            "Type curves are built by normalizing and averaging production data from multiple wells to forecast future performance.",
            ["type curve", "forecast", "production", "analysis"],
            1.0
        ),
        SearchDocument(
            8,
            "Net Revenue Interest (NRI) Calculation",
            "NRI is the share of production revenue accruing to the working interest owner after deducting royalty interests. NRI = Working Interest * (1 - Royalty Rate).",
            ["nri", "net revenue interest", "royalty", "calculation"],
            1.0
        ),
        SearchDocument(
            9,
            "Working Interest Cash Flow Calculation",
            "Working interest cash flow is calculated by multiplying NRI by gross revenue and subtracting expenses and taxes.",
            ["working interest", "cash flow", "nri", "calculation"],
            1.0
        ),
        SearchDocument(
            10,
            "Severance Tax Rates - Texas",
            "Texas imposes severance taxes on oil and gas production. Oil: 4.6% of market value; Gas: 7.5% of market value.",
            ["severance tax", "texas", "oil", "gas"],
            1.0
        ),
        SearchDocument(
            11,
            "Ad Valorem Tax Deduction",
            "Ad valorem taxes are property taxes based on the value of oil and gas reserves. These are deductible from gross revenue for net income calculation.",
            ["ad valorem", "tax", "deduction", "property"],
            1.0
        ),
        SearchDocument(
            12,
            "Gathering, Transportation, and Processing Deductions",
            "Gathering, transportation, and processing costs are deducted from gross revenue to determine net revenue. These costs vary by operator and region.",
            ["gathering", "transportation", "processing", "deductions"],
            1.0
        ),
        SearchDocument(
            13,
            "COPAS Overhead Charges",
            "COPAS overhead charges are standardized administrative fees charged to joint interest partners for well operations.",
            ["copas", "overhead", "charges", "joint interest"],
            1.0
        ),
        SearchDocument(
            14,
            "Lease Operating Expense (LOE) Deduction",
            "LOE includes all recurring costs to operate and maintain a producing well, such as labor, materials, and utilities.",
            ["lease operating expense", "loe", "deduction", "costs"],
            1.0
        ),
        SearchDocument(
            15,
            "CAPEX Recovery - AFE vs Actual",
            "CAPEX recovery compares actual capital expenditures to the original Authorization for Expenditure (AFE) to track project economics.",
            ["capex", "afe", "recovery", "expenditure"],
            1.0
        ),
        SearchDocument(
            16,
            "Payout Calculation",
            "Payout is the point at which cumulative net revenue equals cumulative investment. Calculated by summing net cash flows until investment is recovered.",
            ["payout", "calculation", "investment", "net revenue"],
            1.0
        ),
        SearchDocument(
            17,
            "Rate of Return Analysis",
            "Rate of return (ROR) is calculated by finding the discount rate that sets the net present value (NPV) of cash flows to zero.",
            ["rate of return", "ror", "npv", "analysis"],
            1.0
        ),
        SearchDocument(
            18,
            "PV-10 Valuation",
            "PV-10 is the present value of future net revenue discounted at 10% per year. Used for SEC reserves reporting.",
            ["pv-10", "valuation", "discount", "net revenue"],
            1.0
        ),
        SearchDocument(
            19,
            "NYMEX Strip Pricing",
            "NYMEX strip pricing uses futures contracts to forecast oil and gas prices for economic evaluation.",
            ["nymex", "strip pricing", "futures", "forecast"],
            1.0
        ),
        SearchDocument(
            20,
            "Basis Differential Adjustment",
            "Basis differential adjusts NYMEX prices to reflect local market conditions, accounting for transportation and quality differences.",
            ["basis differential", "adjustment", "nymex", "pricing"],
            1.0
        ),
        SearchDocument(
            21,
            "BTU Adjustment for Gas Revenue",
            "BTU adjustment scales gas revenue based on the heating value of produced gas relative to standard conditions.",
            ["btu", "adjustment", "gas", "revenue"],
            1.0
        ),
        SearchDocument(
            22,
            "Condensate Yield Projection",
            "Condensate yield is projected using historical gas and condensate production ratios to forecast future liquids recovery.",
            ["condensate", "yield", "projection", "gas"],
            1.0
        ),
        SearchDocument(
            23,
            "Decline Curve Model Selection",
            "Model selection between exponential, hyperbolic, and harmonic decline is based on production history and reservoir characteristics.",
            ["decline curve", "model", "selection", "arps"],
            1.0
        ),
        SearchDocument(
            24,
            "Economic Limit Determination",
            "The economic limit is the production rate at which operating costs equal revenue, signaling well abandonment.",
            ["economic limit", "production", "abandonment", "costs"],
            1.0
        ),
        SearchDocument(
            25,
            "Production Forecasting Workflow",
            "A typical workflow includes data gathering, decline curve fitting, type curve construction, and economic evaluation.",
            ["production", "forecasting", "workflow", "type curve"],
            1.0
        ),
        SearchDocument(
            26,
            "Discounted Cash Flow (DCF) in Oil & Gas",
            "DCF analysis discounts future cash flows to present value, incorporating all revenue, expenses, and taxes.",
            ["dcf", "discounted cash flow", "valuation", "oil and gas"],
            1.0
        ),
        SearchDocument(
            27,
            "Royalty Interest Types",
            "Royalty interests include lessor, overriding, and non-participating royalties, each affecting NRI differently.",
            ["royalty", "interest", "nri", "types"],
            1.0
        ),
        SearchDocument(
            28,
            "Well Life Cycle and Decline Analysis",
            "The well life cycle includes drilling, completion, production, decline, and abandonment phases, each impacting reserves and economics.",
            ["well life cycle", "decline", "production", "economics"],
            1.0
        ),
        SearchDocument(
            29,
            "Forecasting with Limited Production Data",
            "When production history is short, analog wells and type curves are used to supplement decline analysis.",
            ["forecasting", "limited data", "type curve", "analog"],
            1.0
        ),
        SearchDocument(
            30,
            "Sensitivity Analysis in Revenue Projection",
            "Sensitivity analysis tests the impact of price, cost, and production assumptions on projected revenue and value.",
            ["sensitivity analysis", "revenue", "projection", "assumptions"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)