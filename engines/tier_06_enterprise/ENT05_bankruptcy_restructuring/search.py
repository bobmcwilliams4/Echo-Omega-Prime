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
        self.doc_term_freqs: Dict[int, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            tokens = self._tokenize(doc.content)
            term_freq = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_term_freqs[doc.id] = term_freq
            self.doc_lengths[doc.id] = len(tokens)
            for term in term_freq:
                self.term_doc_freqs[term] += 1
            self.total_docs = len(self.documents)
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            )
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores: Dict[int, float] = defaultdict(float)
        snippets: Dict[int, str] = {}
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            final_score = bm25_score * 0.7 + tfidf_score * 0.3
            if final_score > 0:
                scores[doc_id] = final_score * doc.weight
                snippets[doc_id] = self._make_snippet(doc.content, query_tokens)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = [
            SearchResult(doc_id, score, self.documents[doc_id].title, snippets[doc_id])
            for doc_id, score in ranked
        ]
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        term_freqs = self.doc_term_freqs.get(doc_id, Counter())
        for term in set(query_tokens):
            idf = self._compute_idf(term)
            tf = term_freqs.get(term, 0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / avgdl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vec = self._tfidf_cache[doc_id]
        else:
            tfidf_vec = {}
            doc_length = self.doc_lengths.get(doc_id, 1)
            term_freqs = self.doc_term_freqs.get(doc_id, Counter())
            for term in term_freqs:
                tf = term_freqs[term] / doc_length
                idf = self._compute_idf(term)
                tfidf_vec[term] = tf * idf
            self._tfidf_cache[doc_id] = tfidf_vec
        query_vec = {}
        query_length = len(query_tokens)
        for term in set(query_tokens):
            tf = query_tokens.count(term) / query_length if query_length > 0 else 0
            idf = self._compute_idf(term)
            query_vec[term] = tf * idf
        # Cosine similarity
        dot = sum(tfidf_vec.get(term, 0) * query_vec.get(term, 0) for term in query_vec)
        doc_norm = math.sqrt(sum(v ** 2 for v in tfidf_vec.values()))
        query_norm = math.sqrt(sum(v ** 2 for v in query_vec.values()))
        if doc_norm == 0 or query_norm == 0:
            return 0.0
        return dot / (doc_norm * query_norm)

    def _make_snippet(self, content: str, query_tokens: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:length]
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + length // 8, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        return snippet[:length] + ('...' if len(snippet) < len(content) else '')

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Automatic Stay Under 11 USC §362",
            "The automatic stay halts all collection activities upon bankruptcy filing. Exceptions include criminal proceedings and certain family law matters.",
            ["automatic stay", "section 362", "bankruptcy"],
            1.0
        ),
        SearchDocument(
            2,
            "Priority Claims in Bankruptcy - 11 USC §507",
            "Section 507 establishes the order of priority for claims, including administrative expenses, wage claims, and tax obligations.",
            ["priority claims", "section 507", "bankruptcy"],
            1.0
        ),
        SearchDocument(
            3,
            "Chapter 11 Plan Confirmation - 11 USC §1129",
            "Plan confirmation requires compliance with statutory requirements, including feasibility, good faith, and best interests of creditors.",
            ["plan confirmation", "section 1129", "chapter 11"],
            1.0
        ),
        SearchDocument(
            4,
            "Fraudulent Transfers - 11 USC §548",
            "Section 548 allows avoidance of transfers made with actual intent to hinder, delay, or defraud creditors, or for less than reasonably equivalent value.",
            ["fraudulent transfers", "section 548", "avoidance"],
            1.0
        ),
        SearchDocument(
            5,
            "Preference Actions - 11 USC §547",
            "Preference actions recover payments made within 90 days prior to bankruptcy that favor certain creditors over others.",
            ["preference", "section 547", "avoidance"],
            1.0
        ),
        SearchDocument(
            6,
            "DIP Financing - 11 USC §364",
            "Debtor-in-Possession financing enables the debtor to obtain new credit during bankruptcy, often with priority or secured status.",
            ["DIP financing", "section 364", "debtor-in-possession"],
            1.0
        ),
        SearchDocument(
            7,
            "Executory Contracts - 11 USC §365",
            "Executory contracts may be assumed or rejected by the debtor, subject to court approval and cure of defaults.",
            ["executory contracts", "section 365", "assumption", "rejection"],
            1.0
        ),
        SearchDocument(
            8,
            "Discharge in Bankruptcy - 11 USC §§727, 523, 1141, 1328",
            "Discharge releases the debtor from personal liability for certain debts. Exceptions include fraud, taxes, and student loans.",
            ["discharge", "section 727", "section 523", "section 1141", "section 1328"],
            1.0
        ),
        SearchDocument(
            9,
            "Secured Claims - 11 USC §506",
            "Section 506 determines the extent to which a claim is secured based on the value of collateral.",
            ["secured claims", "section 506", "collateral"],
            1.0
        ),
        SearchDocument(
            10,
            "Cramdown and Absolute Priority Rule",
            "Cramdown allows plan confirmation over creditor objection if requirements are met. The absolute priority rule protects junior creditors.",
            ["cramdown", "absolute priority", "plan confirmation"],
            1.0
        ),
        SearchDocument(
            11,
            "Small Business Debtor - Subchapter V",
            "Subchapter V streamlines Chapter 11 for small business debtors, reducing costs and simplifying plan confirmation.",
            ["small business", "subchapter v", "chapter 11"],
            1.0
        ),
        SearchDocument(
            12,
            "Exceptions to Automatic Stay",
            "Certain actions, such as criminal proceedings and domestic support obligations, are not stayed by bankruptcy.",
            ["automatic stay", "exceptions", "section 362"],
            1.0
        ),
        SearchDocument(
            13,
            "Administrative Expenses - Priority Claims",
            "Administrative expenses, including professional fees and post-petition trade debt, are given priority under Section 507(a)(2).",
            ["administrative expenses", "priority claims", "section 507"],
            1.0
        ),
        SearchDocument(
            14,
            "Requirements for Plan Confirmation",
            "A Chapter 11 plan must be feasible, proposed in good faith, and provide adequate means for implementation.",
            ["plan confirmation", "feasibility", "good faith"],
            1.0
        ),
        SearchDocument(
            15,
            "Actual vs Constructive Fraudulent Transfers",
            "Actual fraudulent transfers require intent, while constructive transfers occur when the debtor receives less than reasonably equivalent value.",
            ["fraudulent transfers", "actual", "constructive", "section 548"],
            1.0
        ),
        SearchDocument(
            16,
            "Defenses to Preference Actions",
            "Ordinary course of business and contemporaneous exchange for new value are common defenses to preference claims.",
            ["preference", "defenses", "section 547"],
            1.0
        ),
        SearchDocument(
            17,
            "Superpriority in DIP Financing",
            "Superpriority status grants DIP lenders repayment ahead of other creditors, often requiring court approval.",
            ["DIP financing", "superpriority", "section 364"],
            1.0
        ),
        SearchDocument(
            18,
            "Assumption and Rejection of Executory Contracts",
            "Debtors may assume or reject executory contracts, subject to cure of defaults and adequate assurance of future performance.",
            ["executory contracts", "assumption", "rejection", "section 365"],
            1.0
        ),
        SearchDocument(
            19,
            "Non-Dischargeable Debts",
            "Certain debts, such as taxes, fraud, and student loans, are not dischargeable under Sections 523 and 727.",
            ["discharge", "non-dischargeable", "section 523", "section 727"],
            1.0
        ),
        SearchDocument(
            20,
            "Valuation of Collateral for Secured Claims",
            "The value of collateral determines the amount of a secured claim under Section 506.",
            ["secured claims", "collateral", "valuation", "section 506"],
            1.0
        ),
        SearchDocument(
            21,
            "Absolute Priority Rule in Chapter 11",
            "The absolute priority rule prevents junior creditors and equity from receiving value unless senior creditors are paid in full.",
            ["absolute priority", "chapter 11", "plan confirmation"],
            1.0
        ),
        SearchDocument(
            22,
            "Subchapter V Eligibility",
            "Subchapter V is available to small business debtors with aggregate noncontingent debts below a statutory threshold.",
            ["subchapter v", "eligibility", "small business"],
            1.0
        ),
        SearchDocument(
            23,
            "Relief from Automatic Stay",
            "Creditors may seek relief from the automatic stay for cause, including lack of adequate protection or bad faith.",
            ["automatic stay", "relief", "section 362"],
            1.0
        ),
        SearchDocument(
            24,
            "Priority of Wage Claims",
            "Wage claims up to a statutory limit are given priority under Section 507(a)(4).",
            ["priority claims", "wage claims", "section 507"],
            1.0
        ),
        SearchDocument(
            25,
            "Confirmation Standards for Subchapter V Plans",
            "Subchapter V plans require fair and equitable treatment of creditors and do not require acceptance by impaired classes.",
            ["subchapter v", "plan confirmation", "chapter 11"],
            1.0
        ),
        SearchDocument(
            26,
            "Fraudulent Transfer Lookback Periods",
            "Section 548 provides a two-year lookback period for fraudulent transfers, while state law may allow longer periods.",
            ["fraudulent transfers", "lookback", "section 548"],
            1.0
        ),
        SearchDocument(
            27,
            "Preference Lookback Periods",
            "Preference actions typically involve transfers made within 90 days before bankruptcy, or one year for insiders.",
            ["preference", "lookback", "section 547"],
            1.0
        ),
        SearchDocument(
            28,
            "Treatment of Executory Contracts in Chapter 11",
            "Executory contracts may be assumed, rejected, or assigned, subject to court approval and cure of defaults.",
            ["executory contracts", "chapter 11", "section 365"],
            1.0
        ),
        SearchDocument(
            29,
            "Discharge in Chapter 11 - Section 1141",
            "Section 1141 provides for discharge of debts upon plan confirmation, subject to exceptions for certain types of claims.",
            ["discharge", "chapter 11", "section 1141"],
            1.0
        ),
        SearchDocument(
            30,
            "Secured vs Unsecured Claims",
            "Secured claims are backed by collateral, while unsecured claims lack such security and are paid after secured creditors.",
            ["secured claims", "unsecured claims", "collateral"],
            1.0
        ),
        SearchDocument(
            31,
            "Absolute Priority Rule Exceptions",
            "Exceptions to the absolute priority rule may apply in individual Chapter 11 cases, permitting retention of property.",
            ["absolute priority", "exceptions", "chapter 11"],
            1.0
        ),
        SearchDocument(
            32,
            "Small Business Plan Deadlines",
            "Subchapter V requires small business debtors to file a plan within 90 days of the bankruptcy filing.",
            ["subchapter v", "plan deadlines", "small business"],
            1.0
        ),
        SearchDocument(
            33,
            "Adequate Protection in DIP Financing",
            "DIP lenders may require adequate protection to safeguard their interests, including liens and superpriority claims.",
            ["DIP financing", "adequate protection", "section 364"],
            1.0
        ),
        SearchDocument(
            34,
            "Executory Contracts: Adequate Assurance",
            "Assumption of executory contracts requires adequate assurance of future performance to protect counterparties.",
            ["executory contracts", "adequate assurance", "section 365"],
            1.0
        ),
        SearchDocument(
            35,
            "Discharge in Chapter 13 - Section 1328",
            "Section 1328 provides for discharge of debts in Chapter 13, subject to exceptions for certain types of claims.",
            ["discharge", "chapter 13", "section 1328"],
            1.0
        ),
        SearchDocument(
            36,
            "Secured Claim Bifurcation",
            "Section 506 allows bifurcation of secured claims into secured and unsecured portions based on collateral value.",
            ["secured claims", "bifurcation", "section 506"],
            1.0
        ),
        SearchDocument(
            37,
            "Plan Cramdown Requirements",
            "Cramdown requires that the plan does not discriminate unfairly and is fair and equitable to dissenting classes.",
            ["cramdown", "plan confirmation", "chapter 11"],
            1.0
        ),
        SearchDocument(
            38,
            "Small Business Debtor Reporting Requirements",
            "Subchapter V imposes reporting requirements on small business debtors, including periodic financial statements.",
            ["small business", "reporting", "subchapter v"],
            1.0
        ),
        SearchDocument(
            39,
            "Fraudulent Transfer Defenses",
            "Defenses to fraudulent transfer claims include good faith and reasonably equivalent value.",
            ["fraudulent transfers", "defenses", "section 548"],
            1.0
        ),
        SearchDocument(
            40,
            "Preference Action Defenses: New Value",
            "A contemporaneous exchange for new value is a defense to preference actions under Section 547.",
            ["preference", "new value", "section 547"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)