import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            for token in tokens:
                self.inverted_index[token][doc.id] = self.inverted_index[token].get(doc.id, 0) + 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        doc_scores: Dict[str, float] = defaultdict(float)
        for token in query_tokens:
            idf = self._compute_idf(token)
            postings = self.inverted_index.get(token, {})
            for doc_id, freq in postings.items():
                doc = self.documents[doc_id]
                bm25 = self._score_bm25(token, doc_id, freq, idf)
                tfidf = self._score_tfidf(token, doc_id, freq, idf)
                score = 0.7 * bm25 + 0.3 * tfidf
                doc_scores[doc_id] += score * doc.weight
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        return {
            "documents": self.total_docs,
            "unique_terms": len(self.inverted_index),
            "avg_doc_length": int(self.avg_doc_length)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: str, freq: int, idf: float) -> float:
        dl = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        k1 = self._bm25_k1
        b = self._bm25_b
        tf = freq
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * dl / avg_dl)
        return idf * numerator / denominator

    def _score_tfidf(self, term: str, doc_id: str, freq: int, idf: float) -> float:
        tf = freq / self.doc_lengths[doc_id]
        return tf * idf

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], snippet_len: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:160] + ("..." if len(content) > 160 else "")
        start = max(positions[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in query_tokens:
            snippet = re.sub(rf'\b({re.escape(qt)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ("..." if end < len(tokens) else "")

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
            id="1",
            title="Notice to Creditors: Publication Requirements",
            content="A personal representative must publish a notice to creditors in a newspaper of general circulation. The notice must run once a week for three consecutive weeks. Failure to publish may extend the claims period for unknown creditors.",
            tags=["notice", "publication", "creditors"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Four-Month Claims Period for Known Creditors",
            content="Known creditors must present their claims within four months after the date of the first publication of notice to creditors. If a creditor is known and reasonably ascertainable, actual notice must be provided.",
            tags=["claims period", "known creditors"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Priority of Claims: Funeral Expenses First Class",
            content="Funeral expenses are classified as first priority claims and must be paid before other debts. The amount allowed for funeral expenses is subject to statutory limits.",
            tags=["priority", "funeral expenses"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Secured Claims: Priority and Rights",
            content="Secured creditors retain their security interests and may enforce their liens against estate property. If the collateral is insufficient, the deficiency is treated as an unsecured claim.",
            tags=["secured claims", "priority", "liens"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Family Allowance and Exempt Property",
            content="The surviving spouse and minor children are entitled to a family allowance and exempt property, which have priority over most creditor claims except for funeral and administration expenses.",
            tags=["family allowance", "exempt property"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Insolvent Estate Administration and Abatement",
            content="When an estate is insolvent, claims are paid in the statutory order of priority. Abatement rules determine the reduction of bequests to satisfy creditor claims.",
            tags=["insolvent estate", "abatement"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Nonclaim Statute: Two-Year Absolute Bar",
            content="No claim against an estate may be brought more than two years after the decedent's death, regardless of notice. This is an absolute bar under the nonclaim statute.",
            tags=["nonclaim statute", "absolute bar"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Contingent and Unliquidated Claims",
            content="Contingent or unliquidated claims must be presented within the claims period. The personal representative may allow, reject, or compromise such claims.",
            tags=["contingent claims", "unliquidated claims"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Personal Representative Liability for Improper Payments",
            content="A personal representative who pays a claim improperly may be personally liable to the extent of the improper payment. Proper order of payment is essential.",
            tags=["personal representative", "liability"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Federal Tax Lien Priority Over Probate Claims",
            content="Federal tax liens have priority over most probate claims, including family allowance and exempt property, except for certain administrative expenses.",
            tags=["federal tax lien", "priority"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Medicaid Estate Recovery Claims",
            content="State Medicaid agencies may assert claims against the estate for recovery of benefits paid. Medicaid claims are subject to statutory priority rules.",
            tags=["medicaid", "estate recovery"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Claim Rejection and Lawsuit Requirements",
            content="If a claim is rejected by the personal representative, the creditor must file suit within the statutory period or the claim is barred.",
            tags=["claim rejection", "lawsuit"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Child Support Arrearages as Priority Claims",
            content="Child support arrearages are classified as priority claims and must be paid before general unsecured creditors.",
            tags=["child support", "priority"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Classification Disputes Among Creditors",
            content="Disputes among creditors regarding claim classification are resolved by the court. The classification affects the order and amount of payment.",
            tags=["classification", "disputes"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Setoff and Recoupment Against Estate Claims",
            content="Creditors may assert setoff or recoupment rights against the estate's claims, subject to limitations. These rights can reduce the amount payable to the creditor.",
            tags=["setoff", "recoupment"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Notice to Creditors: Actual vs. Constructive",
            content="Actual notice must be given to known or reasonably ascertainable creditors. Constructive notice by publication suffices for unknown creditors.",
            tags=["notice", "actual notice", "constructive notice"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Late-Filed Claims and Exceptions",
            content="Late-filed claims are generally barred unless the creditor can show lack of notice and due diligence. Statutory exceptions may apply.",
            tags=["late claims", "exceptions"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Order of Payment: Statutory Classes",
            content="Claims are paid in the following order: (1) costs of administration, (2) funeral expenses, (3) debts and taxes, (4) all other claims.",
            tags=["order of payment", "statutory classes"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Secured Claims: Election to Surrender Collateral",
            content="The personal representative may elect to surrender collateral to a secured creditor in satisfaction of the claim, subject to court approval.",
            tags=["secured claims", "collateral"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Family Allowance: Duration and Amount",
            content="The family allowance is limited in duration and amount by statute. It is intended to provide support during estate administration.",
            tags=["family allowance", "duration"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Insolvent Estate: Pro Rata Distribution",
            content="If the estate is insolvent, creditors of the same class share pro rata in the available assets after higher priority claims are paid.",
            tags=["insolvent estate", "pro rata"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Nonclaim Statute: Exceptions for Government Claims",
            content="Certain government claims may be excepted from the two-year absolute bar under the nonclaim statute.",
            tags=["nonclaim statute", "government claims"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Contingent Claims: Allowance and Rejection",
            content="The personal representative may allow or reject contingent claims. If rejected, the creditor must timely file suit to establish the claim.",
            tags=["contingent claims", "allowance", "rejection"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Personal Representative: Duty to Investigate Claims",
            content="The personal representative must investigate the validity of all claims and may require supporting documentation before payment.",
            tags=["personal representative", "investigation"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Medicaid Estate Recovery: Notice and Priority",
            content="Notice of estate administration must be given to the state Medicaid agency. Medicaid recovery claims have statutory priority.",
            tags=["medicaid", "notice", "priority"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Family Allowance and Exempt Property: Limitations",
            content="Statutory limits apply to the family allowance and exempt property. Excess claims may be subject to abatement.",
            tags=["family allowance", "exempt property", "abatement"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Abatement of Bequests to Satisfy Claims",
            content="When estate assets are insufficient, general and then specific bequests abate in order to satisfy creditor claims.",
            tags=["abatement", "bequests"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Federal Tax Lien: Exceptions and Limitations",
            content="Certain administrative expenses may take priority over federal tax liens in probate. The scope of the lien is defined by federal law.",
            tags=["federal tax lien", "exceptions"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Setoff: Mutual Debts Between Estate and Creditor",
            content="A creditor owing a debt to the estate may set off the mutual debts, reducing the amount payable on the claim.",
            tags=["setoff", "mutual debts"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Recoupment: Defense Against Estate Claims",
            content="Recoupment allows a creditor to reduce the estate's claim by asserting a related counterclaim arising from the same transaction.",
            tags=["recoupment", "defense"],
            weight=1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)