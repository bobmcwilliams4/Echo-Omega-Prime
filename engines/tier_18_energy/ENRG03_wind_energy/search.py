import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# -------------------------------
# Data Classes
# -------------------------------

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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

# -------------------------------
# Search Index Implementation
# -------------------------------

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_needed = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            token_counts = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
                self.doc_freqs[token] += 1
            self.total_docs += 1
            self._recompute_needed = True

    def _update_stats(self):
        if not self._recompute_needed:
            return
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.total_docs if self.total_docs > 0 else 0.0
        self.idf_cache.clear()
        self._recompute_needed = False

    def get_stats(self):
        self._update_stats()
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'vocab_size': len(self.inverted_index)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        self._update_stats()
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        N = self.total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1=1.5, b=0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        doc = self.documents[doc_id]
        for term in set(query_terms):
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            norm_tf = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_dl))
            score += idf * norm_tf
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 1)
        doc = self.documents[doc_id]
        for term in set(query_terms):
            tf = self.inverted_index.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores: Dict[int, float] = defaultdict(float)
        candidate_docs: Set[int] = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            combined_score = 0.7 * bm25_score + 0.3 * tfidf_score
            doc_scores[doc_id] = combined_score
        top_docs = heapq.nlargest(limit, doc_scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 160) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(min(positions) - 30, 0)
            end = min(start + snippet_len, len(content))
            snippet = content[start:end]
            if start > 0:
                snippet = "..." + snippet
            if end < len(content):
                snippet = snippet + "..."
            return snippet
        else:
            return content[:snippet_len] + ("..." if len(content) > snippet_len else "")

# -------------------------------
# Singleton Factory
# -------------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                idx = SearchIndex()
                _seed_documents(idx)
                _search_index_instance = idx
    return _search_index_instance

# -------------------------------
# Pre-seeded Domain Documents
# -------------------------------

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "S-Corporation Reasonable Compensation",
            "The IRS requires S-Corporation shareholder-employees to receive reasonable compensation for services rendered. Failure to pay reasonable wages may result in reclassification of distributions as wages and assessment of payroll taxes.",
            ["s-corporation", "reasonable compensation", "wages", "irs"],
            1.0
        ),
        SearchDocument(
            2,
            "Capital vs Labor Profit Attribution",
            "Determining whether profits are attributable to capital or labor is crucial for tax treatment. The IRS examines the source of income to distinguish between returns on investment and compensation for services.",
            ["capital", "labor", "profit attribution", "irs"],
            1.0
        ),
        SearchDocument(
            3,
            "Constructive Receipt Doctrine",
            "Under the constructive receipt doctrine, income is taxable when it is credited to the taxpayer's account or made available without restriction, even if not physically received.",
            ["constructive receipt", "doctrine", "income", "taxable"],
            1.0
        ),
        SearchDocument(
            4,
            "Economic Substance Doctrine",
            "The economic substance doctrine denies tax benefits for transactions lacking a substantial purpose other than tax avoidance. Both objective and subjective tests are applied.",
            ["economic substance", "doctrine", "tax avoidance", "irs"],
            1.0
        ),
        SearchDocument(
            5,
            "Hobby Loss Rules - IRC §183",
            "IRC §183 limits deductions for activities not engaged in for profit, commonly known as the hobby loss rules. Taxpayers must demonstrate a profit motive to deduct losses.",
            ["hobby loss", "irc 183", "profit motive", "deductions"],
            1.0
        ),
        SearchDocument(
            6,
            "Home Office Deduction - IRC §280A",
            "IRC §280A allows deductions for home office expenses if the space is used regularly and exclusively for business. Strict substantiation is required.",
            ["home office", "deduction", "irc 280a", "business use"],
            1.0
        ),
        SearchDocument(
            7,
            "Passive Activity Loss Rules - IRC §469",
            "IRC §469 limits the deduction of passive activity losses. Losses can only offset passive income unless the taxpayer materially participates in the activity.",
            ["passive activity", "loss", "irc 469", "material participation"],
            1.0
        ),
        SearchDocument(
            8,
            "Like-Kind Exchange - IRC §1031",
            "IRC §1031 permits deferral of gain on exchanges of like-kind property held for productive use in business or investment, subject to strict identification and timing rules.",
            ["like-kind exchange", "irc 1031", "deferral", "property"],
            1.0
        ),
        SearchDocument(
            9,
            "Percentage Depletion - Oil & Gas (IRC §613A)",
            "IRC §613A allows percentage depletion for certain oil and gas producers, providing a deduction based on a fixed percentage of gross income rather than cost.",
            ["percentage depletion", "oil and gas", "irc 613a", "deduction"],
            1.0
        ),
        SearchDocument(
            10,
            "Intangible Drilling Costs (IDC) - IRC §263(c)",
            "Intangible drilling costs are expenditures for drilling oil and gas wells that are generally deductible under IRC §263(c), subject to capitalization rules.",
            ["intangible drilling costs", "idc", "irc 263c", "oil and gas"],
            1.0
        ),
        SearchDocument(
            11,
            "Qualified Business Income Deduction - IRC §199A",
            "IRC §199A provides a deduction of up to 20% of qualified business income for certain pass-through entities, subject to wage and income limitations.",
            ["qualified business income", "irc 199a", "deduction", "pass-through"],
            1.0
        ),
        SearchDocument(
            12,
            "Statute of Limitations - Assessment & Collection",
            "The IRS generally has three years to assess additional tax and ten years to collect assessed tax. Exceptions apply for fraud or substantial understatement.",
            ["statute of limitations", "assessment", "collection", "irs"],
            1.0
        ),
        SearchDocument(
            13,
            "Offer in Compromise (OIC) - IRC §7122",
            "An Offer in Compromise allows taxpayers to settle tax liabilities for less than the full amount owed, subject to IRS acceptance under IRC §7122.",
            ["offer in compromise", "oic", "irc 7122", "settlement"],
            1.0
        ),
        SearchDocument(
            14,
            "Employee Retention Credit (ERC) - COVID Relief",
            "The Employee Retention Credit provides a refundable tax credit for wages paid to employees during the COVID-19 pandemic, subject to eligibility requirements.",
            ["employee retention credit", "erc", "covid", "tax credit"],
            1.0
        ),
        SearchDocument(
            15,
            "Worker Classification - Employee vs Independent Contractor",
            "Correct worker classification affects tax withholding and reporting. The IRS uses common law rules to determine whether a worker is an employee or independent contractor.",
            ["worker classification", "employee", "independent contractor", "irs"],
            1.0
        ),
        SearchDocument(
            16,
            "Conservation Easements - Syndicated Transactions",
            "Syndicated conservation easement transactions are subject to IRS scrutiny due to potential overvaluation and abuse of charitable deduction rules.",
            ["conservation easements", "syndicated transactions", "irs", "charitable deduction"],
            1.0
        ),
        SearchDocument(
            17,
            "Micro-Captive Insurance - §831(b) Elections",
            "Micro-captive insurance arrangements under §831(b) allow small insurance companies to elect alternative tax treatment, but abusive structures are targeted by the IRS.",
            ["micro-captive", "insurance", "section 831b", "irs"],
            1.0
        ),
        SearchDocument(
            18,
            "Related Party Transactions - §267 and §707(b)",
            "Sections 267 and 707(b) limit deductions and recognize gains on transactions between related parties to prevent tax avoidance.",
            ["related party", "transactions", "section 267", "section 707b"],
            1.0
        ),
        SearchDocument(
            19,
            "Partnership Special Allocations - §704(b)",
            "Special allocations of partnership income, gain, loss, or deduction must have substantial economic effect under §704(b) to be respected for tax purposes.",
            ["partnership", "special allocations", "section 704b", "economic effect"],
            1.0
        ),
        SearchDocument(
            20,
            "Wash Sale Rules - §1091",
            "The wash sale rules under §1091 disallow losses on the sale of securities if substantially identical securities are acquired within 30 days before or after the sale.",
            ["wash sale", "section 1091", "loss disallowance", "securities"],
            1.0
        ),
        SearchDocument(
            21,
            "Net Operating Losses - §172",
            "Net operating losses (NOLs) under §172 may be carried forward to offset taxable income in future years, subject to limitations.",
            ["net operating loss", "nol", "section 172", "carryforward"],
            1.0
        ),
        SearchDocument(
            22,
            "S-Corporation Shareholder Basis - Loss Limitations",
            "S-Corporation shareholders may only deduct losses to the extent of their stock and debt basis. Losses exceeding basis are suspended until basis is restored.",
            ["s-corporation", "shareholder basis", "loss limitation", "deductions"],
            1.0
        ),
        SearchDocument(
            23,
            "Self-Employment Tax - §1401",
            "Self-employment tax under §1401 applies to net earnings from self-employment, including income from partnerships and sole proprietorships.",
            ["self-employment tax", "section 1401", "partnership", "sole proprietorship"],
            1.0
        ),
        SearchDocument(
            24,
            "Hobby Loss - §183 Activity Not Engaged for Profit",
            "If an activity is not engaged in for profit under §183, deductions are limited to the income generated by the activity, and losses cannot offset other income.",
            ["hobby loss", "section 183", "profit motive", "deductions"],
            1.0
        ),
        SearchDocument(
            25,
            "Passive Activity Loss Limitations - §469",
            "Section 469 limits the ability to deduct passive activity losses against non-passive income. Material participation is required to avoid limitation.",
            ["passive activity", "loss limitation", "section 469", "material participation"],
            1.0
        ),
        SearchDocument(
            26,
            "At-Risk Limitations - §465",
            "At-risk limitations under §465 restrict the amount of loss a taxpayer can deduct to the amount at risk in the activity, preventing artificial tax losses.",
            ["at-risk limitation", "section 465", "loss deduction", "tax"],
            1.0
        ),
        SearchDocument(
            27,
            "Like-Kind Exchange - §1031",
            "A like-kind exchange under §1031 allows for the deferral of gain on the exchange of similar business or investment property, provided all requirements are met.",
            ["like-kind exchange", "section 1031", "deferral", "property"],
            1.0
        ),
        SearchDocument(
            28,
            "Cancellation of Debt Income - §61/§108",
            "Income from cancellation of debt is generally includible under §61, but exclusions may apply under §108 for insolvency or bankruptcy.",
            ["cancellation of debt", "section 61", "section 108", "income exclusion"],
            1.0
        ),
        SearchDocument(
            29,
            "Substantial Understatement Penalty - §6662",
            "A substantial understatement of income tax may result in a penalty under §6662, generally 20% of the underpayment attributable to the understatement.",
            ["substantial understatement", "penalty", "section 6662", "irs"],
            1.0
        ),
        SearchDocument(
            30,
            "Home Office Deduction - §280A",
            "The home office deduction under §280A allows taxpayers to deduct expenses for business use of their home, subject to strict rules and substantiation.",
            ["home office", "deduction", "section 280a", "business use"],
            1.0
        ),
        SearchDocument(
            31,
            "Material Participation Test - Passive Activity Rules",
            "Material participation is a key factor in determining whether losses from an activity are passive or non-passive under §469.",
            ["material participation", "passive activity", "section 469", "loss"],
            1.0
        ),
        SearchDocument(
            32,
            "Partnership Allocations - Substantial Economic Effect",
            "For partnership allocations to be respected, they must have substantial economic effect as required by §704(b) and related regulations.",
            ["partnership", "allocation", "economic effect", "section 704b"],
            1.0
        ),
        SearchDocument(
            33,
            "Syndicated Conservation Easements - IRS Enforcement",
            "The IRS has increased enforcement against syndicated conservation easement transactions, challenging valuations and deduction claims.",
            ["conservation easement", "syndicated", "irs", "deduction"],
            1.0
        ),
        SearchDocument(
            34,
            "Micro-Captive Insurance Arrangements - IRS Guidance",
            "IRS guidance warns taxpayers about abusive micro-captive insurance arrangements and increased scrutiny of §831(b) elections.",
            ["micro-captive", "insurance", "irs", "section 831b"],
            1.0
        ),
        SearchDocument(
            35,
            "Worker Classification - Tax Implications",
            "Misclassification of workers as independent contractors instead of employees can result in significant tax liabilities and penalties.",
            ["worker classification", "independent contractor", "employee", "tax"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)