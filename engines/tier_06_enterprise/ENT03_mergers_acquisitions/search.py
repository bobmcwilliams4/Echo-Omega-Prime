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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.total_terms = 0
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            term_counts = Counter(tokens)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            self.N += 1
            self.documents[doc.id] = doc
            for term, count in term_counts.items():
                self.term_doc_freqs[term][doc.id] = count
                self.doc_freqs[term] += 1
            self.avgdl = self.total_terms / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()
            self.tf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, tf in self.term_doc_freqs.get(term, {}).items():
                score = self._score_bm25(term, doc_id, idf)
                doc_scores[doc_id] += score
        results = []
        for doc_id, score in doc_scores.items():
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avgdl,
                "unique_terms": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
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

    def _score_bm25(self, term: str, doc_id: str, idf: Optional[float] = None) -> float:
        if idf is None:
            idf = self._compute_idf(term)
        tf = self.term_doc_freqs[term][doc_id]
        dl = self.doc_lengths[doc_id]
        avgdl = self.avgdl if self.avgdl > 0 else 1
        doc = self.documents[doc_id]
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * dl / avgdl)
        bm25 = idf * (numerator / denominator) * doc.weight
        return bm25

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_tokens = self._tokenize(content)
        positions = []
        for i, token in enumerate(content_tokens):
            if token in query_terms:
                positions.append(i)
        if not positions:
            snippet = content[:160]
            return snippet + ("..." if len(content) > 160 else "")
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(content_tokens))
        snippet_tokens = content_tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + ("..." if end < len(content_tokens) else "")

    # TF-IDF scoring with term frequency normalization
    def tfidf_score(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, tf in self.term_doc_freqs.get(term, {}).items():
                tf_norm = tf / self.doc_lengths[doc_id]
                doc = self.documents[doc_id]
                score = tf_norm * idf * doc.weight
                doc_scores[doc_id] += score
        results = []
        for doc_id, score in doc_scores.items():
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

# Singleton factory
_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            idx = SearchIndex()
            _seed_documents(idx)
            _search_index_instance = idx
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="Asset Purchase vs Stock Purchase: Key Structural Differences",
            content="An asset purchase involves the buyer acquiring selected assets and liabilities of the target, allowing for greater flexibility and potential tax benefits. In contrast, a stock purchase entails acquiring the equity interests of the target, resulting in the buyer assuming all assets and liabilities by operation of law.",
            tags=["asset purchase", "stock purchase", "structure"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Hart-Scott-Rodino (HSR) Act: Filing Thresholds for M&A Transactions",
            content="The HSR Act requires parties to certain mergers and acquisitions to file premerger notifications with the FTC and DOJ if the transaction value exceeds specified thresholds. As of 2024, the size-of-transaction threshold is $119.5 million. Failure to file can result in significant penalties.",
            tags=["HSR", "thresholds", "regulatory"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="CFIUS Review and FIRRMA: Foreign Investment in the United States",
            content="The Committee on Foreign Investment in the United States (CFIUS) reviews certain foreign investments for national security concerns. FIRRMA expanded CFIUS jurisdiction to cover non-controlling investments and real estate transactions near sensitive sites.",
            tags=["CFIUS", "FIRRMA", "foreign investment"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Tax-Free Reorganizations under IRC Section 368",
            content="IRC Section 368 provides for tax-free treatment of certain corporate reorganizations if statutory requirements are met. Types include mergers, consolidations, and divisive reorganizations, each with specific continuity and business purpose requirements.",
            tags=["tax-free", "IRC 368", "reorganization"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Delaware Merger Statute: DGCL Section 251 Explained",
            content="DGCL Section 251 governs statutory mergers in Delaware, requiring board and stockholder approval of the merger agreement. The statute sets forth procedural requirements and appraisal rights for dissenting stockholders.",
            tags=["Delaware", "DGCL 251", "merger"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Material Adverse Change (MAC) Clauses in M&A Agreements",
            content="MAC clauses allow buyers to walk away from a deal if the target suffers a significant negative event before closing. Courts interpret MAC clauses narrowly, focusing on durational significance and excluding general market risks.",
            tags=["MAC", "material adverse change", "agreements"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Representations and Warranties Insurance: Risk Allocation",
            content="Reps & warranties insurance transfers certain M&A risks from seller to insurer, covering breaches of representations in the purchase agreement. It can facilitate negotiations and reduce escrow requirements.",
            tags=["insurance", "representations", "warranties"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Earnouts and Contingent Consideration in M&A",
            content="Earnouts tie a portion of the purchase price to the future performance of the target. They bridge valuation gaps but can lead to post-closing disputes over performance metrics and management control.",
            tags=["earnout", "contingent consideration", "valuation"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Due Diligence and Sandbagging Provisions",
            content="Sandbagging provisions address whether a buyer can claim indemnity for breaches of representations it knew about before closing. Jurisdictions differ on default rules, making express contract language important.",
            tags=["due diligence", "sandbagging", "indemnity"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Working Capital Adjustments in Purchase Price Mechanisms",
            content="Working capital adjustments ensure the target delivers a normalized level of working capital at closing. Disputes often arise over calculation methodologies and post-closing true-ups.",
            tags=["working capital", "adjustment", "purchase price"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Tender Offers and the Williams Act",
            content="The Williams Act regulates tender offers for public companies, requiring disclosure of offer terms and background, and providing time for shareholders to decide. It aims to ensure transparency and fairness.",
            tags=["tender offer", "Williams Act", "public companies"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Indemnification Baskets and Caps in M&A",
            content="Indemnity baskets set a threshold before sellers are liable for breaches, while caps limit the maximum liability. These provisions allocate risk and are heavily negotiated in private deals.",
            tags=["indemnification", "basket", "cap"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Financing Conditions and Committed Financing Letters",
            content="Buyers may condition closing on obtaining financing. Committed financing letters from lenders provide assurance to sellers, but the terms and enforceability of such letters are critical.",
            tags=["financing", "conditions", "commitment"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Regulatory Approval Conditions and Efforts Standards",
            content="M&A agreements often require parties to use 'reasonable best efforts' or similar standards to obtain regulatory approvals. The scope of these obligations can affect deal certainty and timing.",
            tags=["regulatory", "approval", "efforts"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Non-Compete and Non-Solicitation Covenants in M&A",
            content="Non-compete and non-solicitation covenants restrict sellers from competing with or soliciting customers/employees of the target post-closing. Enforceability depends on scope, duration, and jurisdiction.",
            tags=["non-compete", "non-solicitation", "covenant"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Reverse Break Fees in M&A Transactions",
            content="Reverse break fees require buyers to pay a fee if they fail to close, often due to financing failure or regulatory issues. They incentivize deal completion and compensate sellers for lost opportunities.",
            tags=["reverse break fee", "termination", "M&A"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Appraisal Rights and Fair Value in Delaware Mergers",
            content="Dissenting stockholders in Delaware mergers may seek judicial appraisal to determine the fair value of their shares, exclusive of synergies. The process is governed by DGCL Sections 262 and 251.",
            tags=["appraisal", "fair value", "Delaware"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Successor Liability in Asset Purchases",
            content="Asset purchases generally avoid successor liability, but exceptions exist for product liability, fraud, or de facto merger. Buyers should conduct diligence and seek indemnities where risks are identified.",
            tags=["successor liability", "asset purchase", "diligence"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Anti-Assignment Clauses and Change of Control Provisions",
            content="Contracts may restrict assignment or trigger rights upon a change of control. Asset purchases often require third-party consents, while stock purchases may not, depending on contract language.",
            tags=["anti-assignment", "change of control", "contracts"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Disclosure Schedules in M&A Agreements",
            content="Disclosure schedules qualify representations and warranties, providing exceptions and additional detail. Careful drafting is essential to avoid post-closing disputes.",
            tags=["disclosure schedule", "representations", "warranties"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Purchase Price Allocation for Tax Purposes",
            content="In asset deals, the purchase price must be allocated among assets for tax reporting. The allocation affects depreciation, amortization, and gain recognition for both buyer and seller.",
            tags=["purchase price", "allocation", "tax"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Drag-Along and Tag-Along Rights in Private Company M&A",
            content="Drag-along rights allow majority holders to force minority shareholders to sell, while tag-along rights let minorities join a sale. These rights facilitate exits and protect shareholder interests.",
            tags=["drag-along", "tag-along", "shareholder"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="Interim Operating Covenants Between Signing and Closing",
            content="Interim covenants restrict the target’s operations between signing and closing, preserving business value. Breaches may trigger termination rights or indemnity claims.",
            tags=["interim covenant", "operations", "closing"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Go-Shop and No-Shop Provisions in Merger Agreements",
            content="Go-shop provisions allow the target to solicit other bids post-signing, while no-shop provisions prohibit such solicitation. The choice affects deal certainty and competitive tension.",
            tags=["go-shop", "no-shop", "solicitation"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Escrow Arrangements in M&A Transactions",
            content="Escrows hold back a portion of the purchase price to secure indemnity obligations or purchase price adjustments. The terms of release and dispute resolution are key negotiation points.",
            tags=["escrow", "indemnity", "purchase price"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Representation and Warranty Bring-Downs at Closing",
            content="A bring-down requires representations and warranties to be true at closing. The standard (absolute or materiality qualified) affects the buyer’s ability to walk away or seek indemnity.",
            tags=["bring-down", "representations", "warranties"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Locked Box vs Completion Accounts Mechanisms",
            content="Locked box mechanisms fix the purchase price based on a historical balance sheet, while completion accounts adjust price post-closing. Each method has pros and cons for risk allocation.",
            tags=["locked box", "completion accounts", "purchase price"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Section 338(h)(10) Elections in Stock Acquisitions",
            content="A Section 338(h)(10) election allows certain stock acquisitions to be treated as asset purchases for tax purposes, providing a step-up in basis for the buyer. Eligibility and consequences must be considered.",
            tags=["338(h)(10)", "stock acquisition", "tax"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Anti-Sandbagging and Pro-Sandbagging Approaches",
            content="Anti-sandbagging clauses prevent buyers from claiming indemnity for known breaches, while pro-sandbagging allows it. The choice impacts diligence strategy and post-closing remedies.",
            tags=["anti-sandbagging", "pro-sandbagging", "indemnity"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Staple Financing in Auction Processes",
            content="Staple financing refers to pre-arranged financing offered by the seller’s advisor to potential buyers in an auction. It can speed up the process but raises potential conflicts of interest.",
            tags=["staple financing", "auction", "process"],
            weight=1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)