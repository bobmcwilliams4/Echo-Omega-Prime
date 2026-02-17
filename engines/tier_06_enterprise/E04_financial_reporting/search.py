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
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.total_terms: int = 0
        self.lock = threading.Lock()
        self.avg_doc_length: float = 0.0
        self.idf_cache: Dict[str, float] = {}
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freq[term] += 1
            self._update_avg_doc_length()
            self.idf_cache.clear()

    def _update_avg_doc_length(self):
        if self.documents:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.documents)
        else:
            self.avg_doc_length = 0.0

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if len(t) > 1]

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1=1.5, b=0.75) -> float:
        tf = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 0)
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            idf = self._compute_idf(term)
            denom = freq + k1 * (1 - b + b * doc_len / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            score += idf * ((freq * (k1 + 1)) / denom)
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 0)
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / (doc_len if doc_len > 0 else 1)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_ids = set()
        for term in query_terms:
            for doc_id in self.documents:
                if term in self.term_freqs.get(doc_id, {}):
                    candidate_ids.add(doc_id)
        if not candidate_ids:
            candidate_ids = set(self.documents.keys())
        scored_results = []
        for doc_id in candidate_ids:
            doc = self.documents[doc_id]
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id) * doc.weight
            else:
                score = self._score_bm25(query_terms, doc_id) * doc.weight
            snippet = self._make_snippet(doc.content, query_terms)
            scored_results.append(SearchResult(doc_id, score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            snippet = ' '.join(tokens[:snippet_len])
        else:
            start = max(indices[0] - 10, 0)
            end = min(start + snippet_len, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet[:snippet_len] + ('...' if len(snippet) == snippet_len else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'total_terms': self.total_terms,
            'unique_terms': len(self.term_doc_freq),
        }

    def _preseed(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1,
                "ASC 606 Revenue Recognition - Five-Step Model",
                "ASC 606 outlines a five-step model for revenue recognition: identify the contract, identify performance obligations, determine transaction price, allocate price to obligations, and recognize revenue as obligations are satisfied.",
                ["ASC 606", "Revenue Recognition", "Five-Step Model"],
                1.0
            ),
            SearchDocument(
                2,
                "ASC 842 Lease Accounting - Lessee Model",
                "ASC 842 requires lessees to recognize right-of-use assets and lease liabilities for most leases. Classification as operating or finance lease affects income statement presentation.",
                ["ASC 842", "Lease Accounting", "Lessee Model"],
                1.0
            ),
            SearchDocument(
                3,
                "ASC 326 Current Expected Credit Losses (CECL)",
                "ASC 326 introduces the CECL model for estimating credit losses on financial assets, requiring forward-looking estimates and consideration of historical, current, and forecasted information.",
                ["ASC 326", "CECL", "Credit Losses"],
                1.0
            ),
            SearchDocument(
                4,
                "Income Statement Presentation and Classification",
                "Proper classification and presentation of revenues, expenses, gains, and losses in the income statement is essential for clarity and compliance with GAAP.",
                ["Income Statement", "Presentation", "Classification"],
                1.0
            ),
            SearchDocument(
                5,
                "Balance Sheet Classification and Presentation",
                "Assets and liabilities must be appropriately classified as current or noncurrent and presented in accordance with ASC 210 and other relevant standards.",
                ["Balance Sheet", "Classification", "Presentation"],
                1.0
            ),
            SearchDocument(
                6,
                "Statement of Cash Flows - ASC 230",
                "ASC 230 governs the classification of cash flows into operating, investing, and financing activities, requiring reconciliation of net income to net cash provided by operating activities.",
                ["Statement of Cash Flows", "ASC 230"],
                1.0
            ),
            SearchDocument(
                7,
                "DuPont Analysis Framework",
                "DuPont analysis decomposes return on equity into profit margin, asset turnover, and financial leverage, providing insight into drivers of profitability.",
                ["DuPont Analysis", "Profitability", "ROE"],
                1.0
            ),
            SearchDocument(
                8,
                "Altman Z-Score Bankruptcy Prediction",
                "The Altman Z-Score combines financial ratios to assess bankruptcy risk, including working capital, retained earnings, EBIT, market value, and sales.",
                ["Altman Z-Score", "Bankruptcy Prediction", "Financial Ratios"],
                1.0
            ),
            SearchDocument(
                9,
                "Sarbanes-Oxley Section 404 - Internal Controls",
                "SOX 404 mandates management and auditor assessment of internal controls over financial reporting, requiring documentation, testing, and remediation.",
                ["Sarbanes-Oxley", "Section 404", "Internal Controls"],
                1.0
            ),
            SearchDocument(
                10,
                "PCAOB Audit Standards - Materiality and Risk",
                "PCAOB standards require auditors to assess materiality and risk, design procedures to address risks, and evaluate misstatements in the context of financial statements.",
                ["PCAOB", "Audit Standards", "Materiality", "Risk"],
                1.0
            ),
            SearchDocument(
                11,
                "ASC 740 Income Tax Provision",
                "ASC 740 addresses accounting for income taxes, including current and deferred tax assets and liabilities, and the recognition of uncertain tax positions.",
                ["ASC 740", "Income Tax Provision", "Deferred Taxes"],
                1.0
            ),
            SearchDocument(
                12,
                "Multi-Entity Consolidation - ASC 810",
                "ASC 810 provides guidance on consolidating financial statements of entities under common control, including variable interest entities and noncontrolling interests.",
                ["ASC 810", "Consolidation", "Multi-Entity"],
                1.0
            ),
            SearchDocument(
                13,
                "Foreign Currency Translation - ASC 830",
                "ASC 830 prescribes methods for translating foreign currency financial statements, including the use of functional currency and translation adjustments.",
                ["ASC 830", "Foreign Currency", "Translation"],
                1.0
            ),
            SearchDocument(
                14,
                "Fair Value Measurement - ASC 820",
                "ASC 820 defines fair value, establishes a framework for measuring fair value, and expands disclosures about fair value measurements.",
                ["ASC 820", "Fair Value Measurement"],
                1.0
            ),
            SearchDocument(
                15,
                "Goodwill Impairment Testing - ASC 350",
                "ASC 350 requires annual goodwill impairment testing, using a qualitative assessment and, if necessary, a quantitative comparison of carrying and fair values.",
                ["ASC 350", "Goodwill", "Impairment Testing"],
                1.0
            ),
            SearchDocument(
                16,
                "Stock-Based Compensation - ASC 718",
                "ASC 718 governs accounting for stock-based compensation, including measurement at grant date fair value and expense recognition over vesting periods.",
                ["ASC 718", "Stock-Based Compensation"],
                1.0
            ),
            SearchDocument(
                17,
                "Segment Reporting - ASC 280",
                "ASC 280 requires disclosure of information about operating segments, including segment profit, assets, and reconciliation to consolidated totals.",
                ["ASC 280", "Segment Reporting"],
                1.0
            ),
            SearchDocument(
                18,
                "Pension and Post-Retirement Benefits - ASC 715",
                "ASC 715 addresses accounting for pensions and post-retirement benefits, requiring recognition of net benefit cost and disclosure of plan assets and obligations.",
                ["ASC 715", "Pension", "Post-Retirement Benefits"],
                1.0
            ),
            SearchDocument(
                19,
                "ASC 815 Hedge Accounting",
                "ASC 815 provides guidance on hedge accounting, including qualifying criteria, effectiveness assessment, and recognition of gains and losses.",
                ["ASC 815", "Hedge Accounting"],
                1.0
            ),
            SearchDocument(
                20,
                "Going Concern Assessment - ASC 205-40",
                "ASC 205-40 requires management to evaluate whether there is substantial doubt about an entity's ability to continue as a going concern and to disclose relevant information.",
                ["ASC 205-40", "Going Concern"],
                1.0
            ),
            SearchDocument(
                21,
                "IFRS Convergence - Key Differences from US GAAP",
                "IFRS and US GAAP differ in areas such as revenue recognition, lease accounting, impairment, and financial instruments. Convergence efforts aim to reduce differences.",
                ["IFRS", "US GAAP", "Convergence", "Differences"],
                1.0
            ),
            SearchDocument(
                22,
                "Liquidity Ratio Analysis",
                "Liquidity ratios, including current ratio and quick ratio, measure an entity's ability to meet short-term obligations.",
                ["Liquidity Ratio", "Analysis", "Current Ratio", "Quick Ratio"],
                1.0
            ),
            SearchDocument(
                23,
                "Profitability Ratio Analysis",
                "Profitability ratios, such as gross margin, operating margin, and net margin, assess an entity's ability to generate earnings relative to sales, assets, or equity.",
                ["Profitability Ratio", "Analysis", "Gross Margin", "Net Margin"],
                1.0
            ),
            SearchDocument(
                24,
                "Leverage and Solvency Ratio Analysis",
                "Leverage and solvency ratios, including debt-to-equity and interest coverage, evaluate an entity's financial structure and ability to meet long-term obligations.",
                ["Leverage Ratio", "Solvency Ratio", "Debt-to-Equity", "Interest Coverage"],
                1.0
            ),
            SearchDocument(
                25,
                "Variance Analysis - Budget vs Actual",
                "Variance analysis compares budgeted amounts to actual results, identifying causes of variances and supporting management decision-making.",
                ["Variance Analysis", "Budget", "Actual"],
                1.0
            ),
            SearchDocument(
                26,
                "Inventory Accounting - ASC 330",
                "ASC 330 covers inventory accounting, including cost determination, lower of cost or market, and disclosure requirements.",
                ["ASC 330", "Inventory Accounting"],
                1.0
            ),
            SearchDocument(
                27,
                "Business Combinations - ASC 805",
                "ASC 805 provides guidance on accounting for business combinations, including acquisition method, recognition of assets and liabilities, and measurement of goodwill.",
                ["ASC 805", "Business Combinations", "Acquisition Method"],
                1.0
            ),
            SearchDocument(
                28,
                "Debt and Equity Classification - ASC 480/ASC 815",
                "ASC 480 and ASC 815 address classification of financial instruments as debt or equity, including convertible instruments and derivatives.",
                ["ASC 480", "ASC 815", "Debt", "Equity", "Classification"],
                1.0
            ),
            SearchDocument(
                29,
                "Revenue Disaggregation and Contract Assets/Liabilities",
                "ASC 606 requires disaggregation of revenue and disclosure of contract assets and liabilities, providing users with information about revenue streams and performance obligations.",
                ["ASC 606", "Revenue Disaggregation", "Contract Assets", "Contract Liabilities"],
                1.0
            ),
            SearchDocument(
                30,
                "Subsequent Events - ASC 855",
                "ASC 855 defines subsequent events and requires disclosure of events occurring after the balance sheet date but before financial statements are issued.",
                ["ASC 855", "Subsequent Events", "Disclosure"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _search_index_instance._preseed()
        return _search_index_instance