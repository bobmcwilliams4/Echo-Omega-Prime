import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Optional

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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        for doc_id in candidate_docs:
            score = self._score_bm25(doc_id, query_terms)
            doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_length,
            "vocab_size": len(self.doc_freqs)
        }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

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

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        doc = self.documents[doc_id]
        score = 0.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            numer = f * (self.k1 + 1)
            score += idf * numer / denom
        score *= doc.weight
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 30) -> str:
        text = doc.content
        tokens = self._tokenize(text)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return text[:160] + ("..." if len(text) > 160 else "")
        start = max(positions[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ("..." if end < len(tokens) else "")

    def tfidf_score(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        score = 0.0
        for term in query_terms:
            term_tf = tf.get(term, 0) / doc_len if doc_len else 0
            idf = self._compute_idf(term)
            score += term_tf * idf
        score *= doc.weight
        return score

# Singleton factory for search index
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Participating vs Non-Participating Preferred Stock",
            "Participating preferred stock allows investors to receive their liquidation preference and also participate pro-rata with common stockholders in remaining proceeds. Non-participating preferred only receives the greater of the liquidation preference or as-converted common.",
            ["preferred stock", "participating", "liquidation preference", "venture capital"]
        ),
        SearchDocument(
            2,
            "Weighted Average vs Full Ratchet Anti-Dilution",
            "Weighted average anti-dilution adjusts conversion price based on the size and price of new issuances, softening dilution. Full ratchet resets conversion price to the lowest new price, maximizing anti-dilution protection for investors.",
            ["anti-dilution", "weighted average", "full ratchet", "conversion"]
        ),
        SearchDocument(
            3,
            "SAFE Post-Money Valuation Mechanics",
            "Post-money SAFEs calculate investor ownership based on the company's valuation after the SAFE investment, providing greater clarity to investors but potentially more dilution to founders.",
            ["SAFE", "post-money", "valuation", "dilution"]
        ),
        SearchDocument(
            4,
            "409A Valuation Safe Harbors",
            "409A valuations provide safe harbor for setting fair market value of private company stock for tax purposes. Common safe harbors include independent appraisals and illiquid startup valuation methods.",
            ["409A", "valuation", "safe harbor", "tax"]
        ),
        SearchDocument(
            5,
            "Section 83(b) Election Timing",
            "The 83(b) election allows recipients of restricted stock to be taxed at grant rather than vesting. The election must be filed with the IRS within 30 days of the grant date.",
            ["83(b)", "election", "timing", "tax"]
        ),
        SearchDocument(
            6,
            "QSBS Section 1202 Exclusion Requirements",
            "Qualified Small Business Stock (QSBS) under Section 1202 allows exclusion of capital gains if held for 5+ years, subject to active business and gross asset tests.",
            ["QSBS", "Section 1202", "capital gains", "exclusion"]
        ),
        SearchDocument(
            7,
            "Protective Provisions - Investor Veto Rights",
            "Protective provisions give investors veto rights over major company actions such as mergers, new securities issuances, or amendments to charter documents.",
            ["protective provisions", "veto rights", "investor"]
        ),
        SearchDocument(
            8,
            "Drag-Along and Tag-Along Rights",
            "Drag-along rights allow majority shareholders to force minority holders to join in a sale. Tag-along rights let minority holders participate in sales by major shareholders.",
            ["drag-along", "tag-along", "sale", "minority"]
        ),
        SearchDocument(
            9,
            "Board Composition and Observer Rights",
            "Board composition determines investor and founder representation. Observer rights allow non-voting attendance at board meetings, providing information without voting power.",
            ["board", "composition", "observer", "governance"]
        ),
        SearchDocument(
            10,
            "Registration Rights - Demand and Piggyback",
            "Registration rights give investors the ability to require the company to register shares for public sale (demand) or to join company registrations (piggyback).",
            ["registration rights", "demand", "piggyback", "IPO"]
        ),
        SearchDocument(
            11,
            "Information Rights and Financial Reporting",
            "Information rights entitle investors to receive regular financial statements and other company information, ensuring transparency and oversight.",
            ["information rights", "financial reporting", "investor"]
        ),
        SearchDocument(
            12,
            "Vesting Schedules and Acceleration",
            "Vesting schedules determine when founders and employees earn equity. Acceleration provisions speed up vesting upon events like acquisition or termination.",
            ["vesting", "acceleration", "founder", "employee"]
        ),
        SearchDocument(
            13,
            "Right of First Refusal and Co-Sale Rights",
            "Right of first refusal (ROFR) allows the company or investors to purchase shares before they are sold to outsiders. Co-sale rights let investors join in sales by founders.",
            ["ROFR", "co-sale", "right of first refusal", "founder"]
        ),
        SearchDocument(
            14,
            "Pay-to-Play Provisions",
            "Pay-to-play provisions require investors to participate in future financings to retain certain rights, incentivizing ongoing support for the company.",
            ["pay-to-play", "financing", "investor"]
        ),
        SearchDocument(
            15,
            "No-Shop and Exclusivity in Term Sheets",
            "No-shop clauses prevent companies from soliciting other offers during negotiations, providing exclusivity to lead investors and expediting deal closure.",
            ["no-shop", "exclusivity", "term sheet"]
        ),
        SearchDocument(
            16,
            "Convertible Note Terms - Interest and Conversion Mechanics",
            "Convertible notes accrue interest and convert into equity upon a qualified financing, often at a discount or with a valuation cap to reward early investors.",
            ["convertible note", "interest", "conversion", "valuation cap"]
        ),
        SearchDocument(
            17,
            "Accredited Investor and Reg D Exemptions",
            "Accredited investors meet income or net worth thresholds, allowing companies to raise capital under Regulation D exemptions without full SEC registration.",
            ["accredited investor", "Reg D", "exemption", "SEC"]
        ),
        SearchDocument(
            18,
            "Equity Compensation - ISOs vs NSOs",
            "Incentive Stock Options (ISOs) offer tax advantages but have strict requirements. Non-Qualified Stock Options (NSOs) are more flexible but taxed as ordinary income.",
            ["equity compensation", "ISO", "NSO", "stock options"]
        ),
        SearchDocument(
            19,
            "Liquidation Preference Stacking and Seniority",
            "Liquidation preference stacking defines payout order among preferred stockholders. Seniority determines which series are paid first in a liquidation event.",
            ["liquidation preference", "stacking", "seniority", "preferred"]
        ),
        SearchDocument(
            20,
            "Pro-Rata Rights and Super Pro-Rata Allocation",
            "Pro-rata rights allow investors to maintain ownership by participating in future rounds. Super pro-rata grants the right to purchase more than their current share.",
            ["pro-rata", "super pro-rata", "ownership", "future rounds"]
        ),
        SearchDocument(
            21,
            "Founder Stock Repurchase and Vesting Cliffs",
            "Repurchase rights allow companies to buy back unvested founder shares. Vesting cliffs require a minimum period before any shares vest.",
            ["founder", "repurchase", "vesting cliff", "stock"]
        ),
        SearchDocument(
            22,
            "Management Rights Letters and ERISA/BHC Compliance",
            "Management rights letters grant certain investors access to company information, helping maintain ERISA and Bank Holding Company Act compliance.",
            ["management rights", "ERISA", "BHC", "compliance"]
        ),
        SearchDocument(
            23,
            "Founder Restricted Covenants - Non-Compete and IP Assignment",
            "Founders are often subject to non-compete clauses and must assign intellectual property developed to the company, protecting company interests.",
            ["non-compete", "IP assignment", "founder", "covenant"]
        ),
        SearchDocument(
            24,
            "Down Round Financing and Anti-Dilution Adjustments",
            "A down round occurs when shares are sold at a lower price than previous rounds. Anti-dilution provisions protect earlier investors from excessive dilution.",
            ["down round", "anti-dilution", "financing"]
        ),
        SearchDocument(
            25,
            "Major Investor Rights and Thresholds",
            "Major investor rights are granted to investors meeting certain investment thresholds, often including board seats, information rights, and veto powers.",
            ["major investor", "threshold", "board seat", "rights"]
        ),
        SearchDocument(
            26,
            "Option Pool Shuffle and Pre-Money vs Post-Money",
            "The option pool shuffle refers to whether the employee option pool is included in the pre-money or post-money valuation, affecting founder dilution.",
            ["option pool", "pre-money", "post-money", "dilution"]
        ),
        SearchDocument(
            27,
            "Founder Vesting Acceleration Triggers",
            "Single-trigger acceleration occurs upon acquisition; double-trigger requires both acquisition and termination. These affect when founders fully vest.",
            ["vesting", "acceleration", "trigger", "founder"]
        ),
        SearchDocument(
            28,
            "Series Seed vs Series A Terms",
            "Series Seed rounds typically have simpler terms than Series A, with fewer protective provisions and lighter governance requirements.",
            ["Series Seed", "Series A", "terms", "governance"]
        ),
        SearchDocument(
            29,
            "Bridge Loans and Warrants",
            "Bridge loans provide interim financing, often with warrants allowing investors to purchase equity at a set price in the future.",
            ["bridge loan", "warrant", "financing"]
        ),
        SearchDocument(
            30,
            "Founder Reverse Vesting",
            "Reverse vesting requires founders to earn back shares over time, aligning incentives and protecting the company if a founder departs early.",
            ["reverse vesting", "founder", "incentive"]
        ),
    ]
    for doc in docs:
        index.add_document(doc)