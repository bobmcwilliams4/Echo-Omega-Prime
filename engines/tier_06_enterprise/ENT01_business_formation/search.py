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
        self.lock = threading.RLock()
        self._recompute_stats()

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.N = len(self.documents)
            self._recompute_stats()
            self.idf_cache.clear()

    def _recompute_stats(self):
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths.values()) / max(1, len(self.doc_lengths))
        else:
            self.avg_doc_length = 0.0

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
            score += idf * freq * (self.k1 + 1) / denom
        doc = self.documents[doc_id]
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        doc = self.documents[doc_id]
        return score * doc.weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores: Dict[int, float] = {}
        for doc_id in self.documents:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            score = 0.8 * bm25_score + 0.2 * tfidf_score
            if score > 0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
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
            start = max(0, min(positions) - 30)
        else:
            start = 0
        snippet = content[start:start + snippet_len]
        return snippet.replace('\n', ' ')

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'unique_terms': len(self.doc_freqs)
            }

# Singleton factory for search index
_SEARCH_INDEX_INSTANCE: Optional[SearchIndex] = None
_SEARCH_INDEX_LOCK = threading.Lock()

def get_search_index() -> SearchIndex:
    global _SEARCH_INDEX_INSTANCE
    with _SEARCH_INDEX_LOCK:
        if _SEARCH_INDEX_INSTANCE is None:
            idx = SearchIndex()
            _seed_documents(idx)
            _SEARCH_INDEX_INSTANCE = idx
        return _SEARCH_INDEX_INSTANCE

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "LLC Formation Requirements Under TBOC",
            "To form a Texas LLC, a Certificate of Formation must be filed with the Secretary of State. The certificate must include the LLC's name, duration, address, registered agent, and whether the LLC is member-managed or manager-managed. At least one organizer is required. Filing fees apply.",
            ["llc", "formation", "tboc", "certificate"],
            1.0
        ),
        SearchDocument(
            2,
            "LLC Member-Managed vs Manager-Managed",
            "A Texas LLC can be managed by its members or by managers. In a member-managed LLC, all members participate in management. In a manager-managed LLC, management is vested in designated managers, who may or may not be members. The management structure must be stated in the Certificate of Formation.",
            ["llc", "management", "member-managed", "manager-managed"],
            1.0
        ),
        SearchDocument(
            3,
            "Corporation Formation: C-Corp vs S-Corp",
            "A Texas corporation is formed by filing a Certificate of Formation. C-Corps are taxed at the entity level, while S-Corps are pass-through entities for tax purposes. S-Corp status requires an IRS election, a limited number of shareholders, and only certain types of shareholders are allowed.",
            ["corporation", "c-corp", "s-corp", "formation"],
            1.0
        ),
        SearchDocument(
            4,
            "General Partnership Formation by Operation of Law",
            "A general partnership in Texas may be formed without filing any documents. If two or more persons associate to carry on a business for profit as owners, a partnership is created by operation of law, regardless of intent. However, a written partnership agreement is recommended.",
            ["partnership", "general", "operation of law"],
            1.0
        ),
        SearchDocument(
            5,
            "Limited Partnership Formation Requirements",
            "A Texas limited partnership (LP) is formed by filing a Certificate of Formation with the Secretary of State. At least one general partner and one limited partner are required. The partnership agreement governs internal affairs. General partners have management authority and liability.",
            ["limited partnership", "lp", "formation"],
            1.0
        ),
        SearchDocument(
            6,
            "Series LLC Structure and Liability Segregation",
            "A Series LLC allows the creation of separate series with distinct assets, liabilities, and members within a single LLC. Under Texas law, if formalities are observed, the debts and obligations of one series are not enforceable against another series or the LLC as a whole.",
            ["series llc", "liability", "segregation"],
            1.0
        ),
        SearchDocument(
            7,
            "Benefit Corporation Social Purpose Requirements",
            "A Texas benefit corporation must state its public benefit purpose in the Certificate of Formation. Directors must consider the effect of corporate actions on stakeholders and the public benefit. Annual benefit reports are required to demonstrate pursuit of the stated purpose.",
            ["benefit corporation", "social purpose", "requirements"],
            1.0
        ),
        SearchDocument(
            8,
            "Professional Entity Restrictions and Requirements",
            "Professional entities, such as PLLCs and PCs, may only render professional services by licensed individuals. Ownership and management are restricted to licensed professionals. The Certificate of Formation must specify the professional service and all owners must be licensed.",
            ["professional entity", "pllc", "pc", "restrictions"],
            1.0
        ),
        SearchDocument(
            9,
            "Check-the-Box Entity Classification Election",
            "The IRS allows eligible entities to elect their federal tax classification using Form 8832. By default, an LLC with two or more members is taxed as a partnership, but it may elect to be taxed as a corporation. Single-member LLCs are disregarded unless an election is made.",
            ["check-the-box", "entity classification", "irs"],
            1.0
        ),
        SearchDocument(
            10,
            "Registered Agent Requirements and Non-Compliance Consequences",
            "All Texas entities must maintain a registered agent and office. Failure to maintain a registered agent may result in involuntary termination or revocation of the entity's existence, and the entity may not maintain lawsuits in Texas courts until compliance is restored.",
            ["registered agent", "requirements", "non-compliance"],
            1.0
        ),
        SearchDocument(
            11,
            "Annual Franchise Tax and Public Information Report Requirements",
            "Most Texas entities must file an annual franchise tax report and a public information report with the Comptroller. Failure to file may result in forfeiture of the entity's right to transact business and loss of limited liability protection.",
            ["franchise tax", "public information", "annual report"],
            1.0
        ),
        SearchDocument(
            12,
            "Sole Proprietorship: No Filing Required",
            "A sole proprietorship is created when an individual operates a business without forming a separate legal entity. No filings are required with the Secretary of State. The owner is personally liable for all business debts and obligations.",
            ["sole proprietorship", "no filing", "liability"],
            1.0
        ),
        SearchDocument(
            13,
            "LLP Formation and Limited Liability for Partners",
            "A Texas LLP is formed by filing a registration with the Secretary of State. Partners in an LLP are not personally liable for partnership obligations incurred while the LLP registration is in effect, except for their own misconduct.",
            ["llp", "limited liability", "partners"],
            1.0
        ),
        SearchDocument(
            14,
            "Joint Venture Versus Partnership Distinction",
            "A joint venture is similar to a partnership but is typically limited to a single project or transaction. Texas law generally applies partnership principles to joint ventures, but the intent and scope of the relationship are key distinctions.",
            ["joint venture", "partnership", "distinction"],
            1.0
        ),
        SearchDocument(
            15,
            "Delaware vs Texas Formation Comparison",
            "Delaware entities are favored for their flexible laws and business court system. Texas entities are often preferred for businesses operating primarily in Texas, due to lower costs and simpler compliance. Foreign entities must register in Texas to do business here.",
            ["delaware", "texas", "formation", "comparison"],
            1.0
        ),
        SearchDocument(
            16,
            "Close Corporation Election and Shareholder Agreements",
            "A Texas close corporation may elect close status in its Certificate of Formation. Shareholder agreements may restrict board powers, management, and transfer of shares. Close corporations are exempt from some formalities required of regular corporations.",
            ["close corporation", "shareholder agreement", "election"],
            1.0
        ),
        SearchDocument(
            17,
            "Certificate of Formation Amendment Procedures",
            "To amend a Certificate of Formation, a Texas entity must file a Certificate of Amendment with the Secretary of State. Amendments require approval by the governing persons or shareholders as provided by the entity's governing documents and the TBOC.",
            ["certificate of formation", "amendment", "procedures"],
            1.0
        ),
        SearchDocument(
            18,
            "Foreign Entity Registration Requirements",
            "A foreign entity transacting business in Texas must file an Application for Registration with the Secretary of State. Failure to register may result in fines and the inability to maintain lawsuits in Texas courts.",
            ["foreign entity", "registration", "requirements"],
            1.0
        ),
        SearchDocument(
            19,
            "Operating Agreement Governance and Enforceability",
            "An LLC's operating agreement governs the relations among members and managers. Texas law generally enforces operating agreements unless they violate the TBOC or public policy. Oral agreements may be enforceable but written agreements are recommended.",
            ["operating agreement", "governance", "enforceability"],
            1.0
        ),
        SearchDocument(
            20,
            "Member/Shareholder Approval for Fundamental Transactions",
            "Fundamental transactions, such as mergers, conversions, or sales of all assets, generally require approval by a specified percentage of members or shareholders as set forth in the entity's governing documents and the TBOC.",
            ["member approval", "shareholder approval", "fundamental transactions"],
            1.0
        ),
        SearchDocument(
            21,
            "Pre-Formation Contracts and Promoter Liability",
            "Promoters who enter into contracts on behalf of a proposed entity may be personally liable unless the contract provides otherwise or the entity adopts the contract after formation. Adoption generally requires an act of the entity's governing persons.",
            ["pre-formation", "promoter", "liability", "contracts"],
            1.0
        ),
        SearchDocument(
            22,
            "Entity Name Reservation and Availability",
            "An entity name may be reserved with the Texas Secretary of State for 120 days. The name must be distinguishable from existing entities. Name availability may be checked online, and certain words are restricted or require approval.",
            ["name reservation", "availability", "entity name"],
            1.0
        ),
        SearchDocument(
            23,
            "Piercing the Corporate Veil and Alter Ego Doctrine",
            "Texas courts may pierce the corporate veil and hold owners personally liable if the entity is used to perpetrate fraud, for personal purposes, or if formalities are ignored. The alter ego doctrine is a common basis for veil piercing.",
            ["piercing the veil", "alter ego", "liability"],
            1.0
        ),
        SearchDocument(
            24,
            "Entity Dissolution and Winding Up Procedures",
            "Dissolution of a Texas entity requires filing a Certificate of Termination. The entity must wind up its affairs, pay debts, and distribute remaining assets. Failure to properly dissolve may result in continued tax and reporting obligations.",
            ["dissolution", "winding up", "procedures"],
            1.0
        ),
        SearchDocument(
            25,
            "Single-Member LLC Liability Protection and Formalities",
            "A single-member LLC provides limited liability protection if the entity is properly maintained. Observing formalities such as separate accounts and records is critical to avoid veil piercing. The IRS disregards single-member LLCs for tax unless an election is made.",
            ["single-member llc", "liability", "formalities"],
            1.0
        ),
        SearchDocument(
            26,
            "Series LLC: Internal Affairs and Asset Protection",
            "Each series in a Texas Series LLC may have separate members, managers, assets, and liabilities. Proper recordkeeping and notice in the Certificate of Formation are essential for liability segregation. Creditors of one series cannot reach assets of another.",
            ["series llc", "asset protection", "internal affairs"],
            1.0
        ),
        SearchDocument(
            27,
            "PLLC and PC: Professional Entity Formation",
            "A Professional Limited Liability Company (PLLC) or Professional Corporation (PC) must comply with Texas professional entity statutes. Only licensed professionals may be owners or managers. The Certificate of Formation must specify the profession.",
            ["pllc", "pc", "professional formation"],
            1.0
        ),
        SearchDocument(
            28,
            "Franchise Tax: No Tax Due Threshold",
            "Entities with annualized total revenue below the Texas no-tax-due threshold are not required to pay franchise tax but must still file the public information report. The threshold is adjusted periodically by the Comptroller.",
            ["franchise tax", "no tax due", "threshold"],
            1.0
        ),
        SearchDocument(
            29,
            "LLC Operating Agreement: Default Rules",
            "If an LLC has no operating agreement, the default rules of the Texas Business Organizations Code (TBOC) govern management, distributions, and member rights. An operating agreement may override most default provisions.",
            ["llc", "operating agreement", "default rules"],
            1.0
        ),
        SearchDocument(
            30,
            "LLC Name Requirements and Restrictions",
            "A Texas LLC name must contain 'Limited Liability Company,' 'LLC,' or 'L.L.C.' Certain words, such as 'bank' or 'insurance,' are restricted and require approval. The name must be distinguishable from other entities on file.",
            ["llc", "name", "requirements", "restrictions"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)