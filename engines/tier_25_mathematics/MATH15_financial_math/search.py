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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.doc_tags: Dict[int, List[str]] = {}
        self.doc_weights: Dict[int, float] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_tags[doc.id] = doc.tags
            self.doc_weights[doc.id] = doc.weight
            term_counts = Counter(tokens)
            for term, count in term_counts.items():
                self.inverted_index[term][doc.id] = count
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        weight = self.doc_weights.get(doc_id, 1.0)
        for term in query_terms:
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            term_score = idf * (numerator / (denominator if denominator > 0 else 1))
            score += term_score
        return score * weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vector = self._tfidf_cache[doc_id]
        else:
            tokens = self._tokenize(self.documents[doc_id].content)
            term_counts = Counter(tokens)
            doc_len = len(tokens)
            tfidf_vector = {}
            for term in term_counts:
                tf = term_counts[term] / doc_len if doc_len > 0 else 0
                idf = self._compute_idf(term)
                tfidf_vector[term] = tf * idf
            self._tfidf_cache[doc_id] = tfidf_vector
        score = 0.0
        for term in query_terms:
            score += tfidf_vector.get(term, 0.0)
        return score * self.doc_weights.get(doc_id, 1.0)

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scored_results.append((doc_id, score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:snippet_len])
        start = max(positions[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.inverted_index),
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

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(1, "Compound Interest", 
            "Compound interest is the process of earning interest on both the principal and accumulated interest. The formula is A = P*(1+r/n)^(nt).", 
            ["interest", "compound", "formula"], 1.0),
        SearchDocument(2, "Simple Interest", 
            "Simple interest is calculated only on the principal amount. Formula: I = P*r*t.", 
            ["interest", "simple", "formula"], 1.0),
        SearchDocument(3, "Present Value", 
            "Present value determines the current worth of a future sum of money given a specified rate of return. PV = FV/(1+r)^n.", 
            ["present value", "discounting", "formula"], 1.0),
        SearchDocument(4, "Future Value", 
            "Future value computes the value of an investment after a certain period. FV = PV*(1+r)^n.", 
            ["future value", "investment", "formula"], 1.0),
        SearchDocument(5, "Annuities", 
            "An annuity is a series of equal payments at regular intervals. Ordinary annuity formula: PV = PMT*(1-(1+r)^-n)/r.", 
            ["annuity", "payments", "formula"], 1.0),
        SearchDocument(6, "Perpetuities", 
            "A perpetuity is a stream of equal payments that continues forever. PV = PMT/r.", 
            ["perpetuity", "payments", "formula"], 1.0),
        SearchDocument(7, "Loan Amortization", 
            "Loan amortization schedules show how payments are split between principal and interest. Amortization formula: PMT = P*r*(1+r)^n/((1+r)^n-1).", 
            ["loan", "amortization", "schedule"], 1.0),
        SearchDocument(8, "Discount Rate", 
            "The discount rate is used to determine the present value of future cash flows. It reflects the time value of money and risk.", 
            ["discount rate", "present value", "risk"], 1.0),
        SearchDocument(9, "Net Present Value (NPV)", 
            "NPV is the sum of present values of incoming and outgoing cash flows over time. NPV = Σ(CFt/(1+r)^t).", 
            ["NPV", "cash flow", "investment"], 1.0),
        SearchDocument(10, "Internal Rate of Return (IRR)", 
            "IRR is the discount rate that makes the NPV of all cash flows from a project equal to zero.", 
            ["IRR", "investment", "cash flow"], 1.0),
        SearchDocument(11, "Effective Annual Rate (EAR)", 
            "EAR accounts for compounding periods in a year. EAR = (1 + r/n)^n - 1.", 
            ["EAR", "compounding", "rate"], 1.0),
        SearchDocument(12, "Continuous Compounding", 
            "Continuous compounding uses the formula A = Pe^(rt) for calculating interest.", 
            ["compounding", "continuous", "interest"], 1.0),
        SearchDocument(13, "Bond Pricing", 
            "Bond price is the present value of future cash flows discounted at the market rate. Price = Σ(C/(1+r)^t) + F/(1+r)^T.", 
            ["bond", "pricing", "cash flow"], 1.0),
        SearchDocument(14, "Yield to Maturity (YTM)", 
            "YTM is the rate of return anticipated on a bond if held until maturity.", 
            ["YTM", "bond", "return"], 1.0),
        SearchDocument(15, "Duration", 
            "Duration measures the sensitivity of a bond's price to changes in interest rates.", 
            ["duration", "bond", "interest rate"], 1.0),
        SearchDocument(16, "Capital Budgeting", 
            "Capital budgeting involves evaluating investment projects using NPV, IRR, payback period, and profitability index.", 
            ["capital budgeting", "NPV", "IRR"], 1.0),
        SearchDocument(17, "Payback Period", 
            "Payback period is the time required to recover the initial investment from cash flows.", 
            ["payback period", "investment", "cash flow"], 1.0),
        SearchDocument(18, "Profitability Index", 
            "Profitability index is the ratio of present value of future cash flows to initial investment.", 
            ["profitability index", "investment", "cash flow"], 1.0),
        SearchDocument(19, "Risk and Return", 
            "Risk and return are fundamental concepts in financial decision-making. Higher risk typically demands higher expected return.", 
            ["risk", "return", "investment"], 1.0),
        SearchDocument(20, "Portfolio Theory", 
            "Portfolio theory analyzes how investors can construct portfolios to maximize return for a given level of risk.", 
            ["portfolio", "risk", "return"], 1.0),
        SearchDocument(21, "Diversification", 
            "Diversification reduces risk by investing in a variety of assets.", 
            ["diversification", "risk", "portfolio"], 1.0),
        SearchDocument(22, "Time Value of Money", 
            "The time value of money means a dollar today is worth more than a dollar tomorrow.", 
            ["time value", "money", "interest"], 1.0),
        SearchDocument(23, "Financial Ratios", 
            "Financial ratios analyze a company's performance, including liquidity, profitability, and solvency ratios.", 
            ["financial ratios", "liquidity", "profitability"], 1.0),
        SearchDocument(24, "Leverage", 
            "Leverage refers to the use of borrowed funds to increase potential return.", 
            ["leverage", "borrowed funds", "return"], 1.0),
        SearchDocument(25, "Cost of Capital", 
            "Cost of capital is the required return necessary to make a capital budgeting project worthwhile.", 
            ["cost of capital", "capital budgeting", "return"], 1.0),
        SearchDocument(26, "Weighted Average Cost of Capital (WACC)", 
            "WACC is the average rate of return a company expects to pay its security holders.", 
            ["WACC", "cost of capital", "return"], 1.0),
        SearchDocument(27, "Cash Flow Analysis", 
            "Cash flow analysis tracks inflows and outflows to assess liquidity and profitability.", 
            ["cash flow", "liquidity", "profitability"], 1.0),
        SearchDocument(28, "Depreciation Methods", 
            "Depreciation methods include straight-line and declining balance to allocate asset cost over time.", 
            ["depreciation", "asset", "cost"], 1.0),
        SearchDocument(29, "Financial Statements", 
            "Financial statements include the balance sheet, income statement, and cash flow statement.", 
            ["financial statements", "balance sheet", "income statement"], 1.0),
        SearchDocument(30, "Market Value", 
            "Market value is the price at which an asset would trade in a competitive auction setting.", 
            ["market value", "asset", "price"], 1.0),
        SearchDocument(31, "Liquidity", 
            "Liquidity is the ability to quickly convert assets to cash without significant loss.", 
            ["liquidity", "asset", "cash"], 1.0),
        SearchDocument(32, "Solvency", 
            "Solvency is a company's ability to meet its long-term obligations.", 
            ["solvency", "company", "obligations"], 1.0),
        SearchDocument(33, "Return on Investment (ROI)", 
            "ROI measures the gain or loss generated on an investment relative to its cost.", 
            ["ROI", "investment", "return"], 1.0),
        SearchDocument(34, "Financial Modeling", 
            "Financial modeling uses mathematical models to represent financial performance and forecast future outcomes.", 
            ["financial modeling", "forecast", "performance"], 1.0),
        SearchDocument(35, "Option Pricing", 
            "Option pricing models like Black-Scholes estimate the value of financial options.", 
            ["option pricing", "Black-Scholes", "options"], 1.0),
        SearchDocument(36, "Stock Valuation", 
            "Stock valuation methods include dividend discount model and price-earnings ratio.", 
            ["stock valuation", "dividend", "price-earnings"], 1.0),
        SearchDocument(37, "Dividend Policy", 
            "Dividend policy determines how much profit is distributed to shareholders versus retained.", 
            ["dividend policy", "profit", "shareholders"], 1.0),
        SearchDocument(38, "Capital Structure", 
            "Capital structure is the mix of debt and equity used to finance a company's operations.", 
            ["capital structure", "debt", "equity"], 1.0),
        SearchDocument(39, "Financial Planning", 
            "Financial planning involves budgeting, forecasting, and managing cash flows to achieve financial goals.", 
            ["financial planning", "budgeting", "forecasting"], 1.0),
        SearchDocument(40, "Interest Rate Risk", 
            "Interest rate risk is the potential for investment losses due to fluctuations in interest rates.", 
            ["interest rate risk", "investment", "loss"], 1.0),
    ]
    for doc in docs:
        idx.add_document(doc)