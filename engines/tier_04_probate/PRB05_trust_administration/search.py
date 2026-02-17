import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

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

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.inverted_index: Dict[str, set] = defaultdict(set)

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.documents[doc.id] = doc
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
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

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        dl = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            score += idf * (f * (self.k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        for term in query_terms:
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / dl if dl > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], length: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:length] + ("..." if len(content) > length else "")
        first = positions[0]
        start = max(0, first - 10)
        end = min(len(tokens), first + 20)
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf"\b({re.escape(term)})\b", r"<b>\1</b>", snippet, flags=re.IGNORECASE)
        return snippet[:length] + ("..." if len(snippet) > length else "")

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        if not candidate_docs:
            return []
        scores = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc, query_terms)
                scores.append(SearchResult(doc_id, score, doc.title, snippet))
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def get_stats(self) -> Dict[str, int]:
        return {
            "documents": self.N,
            "unique_terms": len(self.doc_freqs),
            "avg_doc_length": int(self.avgdl),
        }

# Singleton factory for SearchIndex
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

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Duty of Loyalty: Self-Dealing Prohibition",
            "A trustee must avoid self-dealing and conflicts of interest. Transactions that benefit the trustee personally are generally voidable by beneficiaries unless authorized by the trust or court.",
            ["duty of loyalty", "self-dealing", "trustee", "fiduciary"]
        ),
        SearchDocument(
            2,
            "Prudent Investor Rule and Modern Portfolio Theory",
            "Trustees are required to invest trust assets as a prudent investor would, considering risk and return objectives. Diversification is generally required under modern portfolio theory.",
            ["prudent investor", "modern portfolio theory", "investment", "trustee"]
        ),
        SearchDocument(
            3,
            "Duty to Inform: Regular Reporting Requirements",
            "Trustees must keep beneficiaries reasonably informed about the trust's administration, including providing annual accountings and responding to beneficiary requests for information.",
            ["duty to inform", "reporting", "accounting", "beneficiaries"]
        ),
        SearchDocument(
            4,
            "HEMS Distribution Standard: Ascertainable Standard",
            "Distributions under the HEMS standard are limited to a beneficiary's health, education, maintenance, or support, providing an ascertainable standard for trustee discretion.",
            ["HEMS", "ascertainable standard", "distribution", "trustee discretion"]
        ),
        SearchDocument(
            5,
            "Spendthrift Clause: Creditor Protection",
            "A spendthrift clause restricts a beneficiary's ability to transfer their interest and protects trust assets from most creditors until distributed.",
            ["spendthrift", "creditor protection", "beneficiary", "trust"]
        ),
        SearchDocument(
            6,
            "Trust Modification: Changed Circumstances Doctrine",
            "Courts may modify a trust if unforeseen circumstances arise that defeat or substantially impair the trust's purposes, under the doctrine of changed circumstances.",
            ["trust modification", "changed circumstances", "court", "doctrine"]
        ),
        SearchDocument(
            7,
            "Trustee Removal: Cause Standard",
            "Beneficiaries may petition for trustee removal for cause, such as breach of trust, incapacity, or persistent failure to administer the trust effectively.",
            ["trustee removal", "cause", "beneficiaries", "breach of trust"]
        ),
        SearchDocument(
            8,
            "Duty of Impartiality: Income vs Remainder Beneficiaries",
            "A trustee must act impartially between income and remainder beneficiaries, balancing their respective interests in trust distributions and investments.",
            ["duty of impartiality", "income beneficiary", "remainder beneficiary", "trustee"]
        ),
        SearchDocument(
            9,
            "Crummey Powers: Annual Exclusion Gifts",
            "Crummey powers allow beneficiaries to withdraw contributions for a limited period, qualifying gifts for the annual exclusion from federal gift tax.",
            ["crummey powers", "annual exclusion", "gift tax", "beneficiary"]
        ),
        SearchDocument(
            10,
            "Generation-Skipping Transfer Tax: Dynasty Trust Planning",
            "Dynasty trusts are designed to avoid estate and generation-skipping transfer taxes by holding assets for multiple generations, subject to GST tax rules.",
            ["generation-skipping", "dynasty trust", "GST", "tax planning"]
        ),
        SearchDocument(
            11,
            "Trust Decanting: Trustee Power to Modify",
            "Trust decanting allows a trustee to distribute assets from one trust to another with more favorable terms, subject to statutory and fiduciary limitations.",
            ["trust decanting", "trustee power", "modification", "fiduciary"]
        ),
        SearchDocument(
            12,
            "Virtual Representation: Binding Absent Beneficiaries",
            "Virtual representation permits certain beneficiaries to represent and bind others with similar interests in trust proceedings, streamlining administration.",
            ["virtual representation", "beneficiaries", "trust proceedings"]
        ),
        SearchDocument(
            13,
            "Trustee Compensation: Reasonable Fees",
            "Trustees are entitled to reasonable compensation for their services, considering the complexity of administration, time spent, and results achieved.",
            ["trustee compensation", "fees", "administration"]
        ),
        SearchDocument(
            14,
            "Revocable Trust: Settlor Rights and Control",
            "A revocable trust allows the settlor to retain control over trust assets and amend or revoke the trust during their lifetime.",
            ["revocable trust", "settlor", "control", "amendment"]
        ),
        SearchDocument(
            15,
            "Trust Protector: Third-Party Oversight Powers",
            "A trust protector is a third party empowered to oversee trustee actions, modify trust terms, or resolve disputes, enhancing flexibility and oversight.",
            ["trust protector", "oversight", "third party", "modification"]
        ),
        SearchDocument(
            16,
            "Breach of Trust: Remedies and Surcharge",
            "When a trustee breaches fiduciary duties, beneficiaries may seek remedies including removal, damages, or surcharge to restore trust losses.",
            ["breach of trust", "remedies", "surcharge", "fiduciary"]
        ),
        SearchDocument(
            17,
            "Trust Accounting: Principal and Income Allocation",
            "Trustees must allocate receipts and disbursements between principal and income in accordance with the trust instrument and applicable law.",
            ["trust accounting", "principal", "income", "allocation"]
        ),
        SearchDocument(
            18,
            "Special Needs Trust: Preserving Government Benefits",
            "Special needs trusts are structured to supplement, not supplant, government benefits for disabled beneficiaries, preserving eligibility.",
            ["special needs trust", "government benefits", "disabled beneficiary"]
        ),
        SearchDocument(
            19,
            "Charitable Remainder Trust: Split Interest Requirements",
            "Charitable remainder trusts provide an income stream to non-charitable beneficiaries with the remainder passing to charity, subject to IRS requirements.",
            ["charitable remainder trust", "split interest", "IRS", "charity"]
        ),
        SearchDocument(
            20,
            "Dynasty Trust: Perpetuities and Asset Protection",
            "Dynasty trusts avoid the rule against perpetuities in some jurisdictions, allowing long-term asset protection and tax planning for future generations.",
            ["dynasty trust", "perpetuities", "asset protection"]
        ),
        SearchDocument(
            21,
            "Unitrust Conversion: UPIA Power to Adjust",
            "The Uniform Principal and Income Act allows conversion to a unitrust, enabling trustees to pay a fixed percentage of trust assets as income.",
            ["unitrust", "UPIA", "principal and income", "conversion"]
        ),
        SearchDocument(
            22,
            "Trust Termination: Uneconomic to Continue",
            "A trust may be terminated if its value is insufficient to justify continued administration, typically by court order or trustee discretion.",
            ["trust termination", "uneconomic", "administration", "court"]
        ),
        SearchDocument(
            23,
            "Trustee Delegation: Investment and Administrative Functions",
            "Trustees may delegate investment and administrative functions to qualified agents, but must exercise reasonable care in selection and monitoring.",
            ["trustee delegation", "investment", "administration", "agents"]
        ),
        SearchDocument(
            24,
            "Qualified Personal Residence Trust: Estate Tax Reduction",
            "A QPRT allows a grantor to transfer a residence to a trust, reducing estate tax by removing future appreciation from the taxable estate.",
            ["QPRT", "personal residence", "estate tax", "grantor"]
        ),
        SearchDocument(
            25,
            "Alaska Self-Settled Asset Protection Trust: Creditor Shield",
            "Alaska law permits self-settled trusts that shield assets from most creditors, provided statutory requirements are met.",
            ["alaska trust", "asset protection", "creditor shield", "self-settled"]
        ),
        SearchDocument(
            26,
            "Nonjudicial Settlement Agreement: Consent Modification",
            "Nonjudicial settlement agreements allow interested parties to resolve trust matters and modify terms without court involvement, within statutory limits.",
            ["nonjudicial settlement", "modification", "consent", "trust"]
        ),
        SearchDocument(
            27,
            "Trustee Investment Policy Statement: Best Practices",
            "A trustee should develop a written investment policy statement to guide prudent investment decisions and document compliance with fiduciary duties.",
            ["investment policy", "trustee", "prudent investor", "fiduciary"]
        ),
        SearchDocument(
            28,
            "Directed Trusts: Division of Trustee Functions",
            "Directed trusts allow certain powers, such as investment or distribution decisions, to be exercised by a party other than the trustee.",
            ["directed trust", "trustee", "division of powers"]
        ),
        SearchDocument(
            29,
            "Trust Reformation: Correcting Mistakes",
            "A court may reform a trust to correct mistakes or effectuate the settlor's intent, provided clear and convincing evidence is presented.",
            ["trust reformation", "mistake", "settlor intent", "court"]
        ),
        SearchDocument(
            30,
            "Trustee Duty to Diversify Investments",
            "Trustees must diversify trust investments unless the trust instrument or circumstances indicate otherwise, to reduce risk.",
            ["diversification", "trustee", "investment", "risk"]
        ),
    ]
    for doc in docs:
        index.add_document(doc)