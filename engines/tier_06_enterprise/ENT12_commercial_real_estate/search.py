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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_term_freqs: Dict[int, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.doc_lengths: Dict[int, int] = {}
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.term_doc_freqs[term] += 1
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            for doc_id, tf in self.doc_term_freqs.items():
                if term in tf:
                    candidate_docs.add(doc_id)
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            final_score = bm25_score * 0.7 + tfidf_score * 0.3
            snippet = self._make_snippet(doc.content, query_terms)
            scored_results.append(SearchResult(doc_id, final_score * doc.weight, doc.title, snippet))
        scored_results.sort(key=lambda x: x.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avgdl,
                'num_terms': len(self.term_doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf = self.doc_term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * dl / (self.avgdl if self.avgdl > 0 else 1))
            score += idf * (freq * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf = self.doc_term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        for term in query_terms:
            key = (doc_id, term)
            if key in self._tfidf_cache:
                score += self._tfidf_cache[key]
                continue
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / dl
            idf = self._compute_idf(term)
            tfidf = tf_norm * idf
            self._tfidf_cache[key] = tfidf
            score += tfidf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 40) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:window] + '...' if len(content) > window else content
        start = max(min(positions) - window // 2, 0)
        end = min(start + window, len(content))
        snippet = content[start:end]
        for term in query_terms:
            snippet = re.sub(f'({re.escape(term)})', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ('...' if end < len(content) else '')

# Singleton factory for SearchIndex
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Triple Net Lease Structure Explained",
            "A triple net lease (NNN) is a lease agreement where the tenant is responsible for property taxes, insurance, and maintenance, in addition to rent. This structure is common in commercial real estate, especially for freestanding retail and industrial properties.",
            ["lease", "NNN", "tenant", "landlord"],
            1.0
        ),
        SearchDocument(
            2,
            "CMBS Loan Servicing Standards Overview",
            "Commercial Mortgage-Backed Securities (CMBS) loans are governed by strict servicing standards. These include requirements for payment processing, escrow management, property inspections, and default resolution. Master and special servicers play distinct roles in the servicing process.",
            ["CMBS", "loan", "servicing", "standards"],
            1.0
        ),
        SearchDocument(
            3,
            "IRC Section 1031 Like-Kind Exchange",
            "Section 1031 of the Internal Revenue Code allows investors to defer capital gains taxes on the exchange of like-kind real property held for investment or business use. Strict timelines and identification rules apply to qualify for tax deferral.",
            ["1031", "exchange", "tax", "deferral"],
            1.0
        ),
        SearchDocument(
            4,
            "Qualified Opportunity Zone Investment",
            "Qualified Opportunity Zones (QOZ) were created to spur economic development by providing tax incentives for investments in designated areas. Investors can defer and reduce capital gains taxes by investing in Qualified Opportunity Funds.",
            ["QOZ", "investment", "tax", "incentives"],
            1.0
        ),
        SearchDocument(
            5,
            "REIT Qualification Requirements",
            "To qualify as a Real Estate Investment Trust (REIT), an entity must meet income, asset, and distribution tests. At least 75% of assets must be in real estate, and 90% of taxable income must be distributed to shareholders annually.",
            ["REIT", "qualification", "requirements", "tax"],
            1.0
        ),
        SearchDocument(
            6,
            "Phase I Environmental Site Assessment",
            "A Phase I ESA is a report prepared for real estate holdings that identifies potential or existing environmental contamination liabilities. It includes a site inspection, records review, and interviews but does not involve sampling.",
            ["environmental", "assessment", "ESA", "liability"],
            1.0
        ),
        SearchDocument(
            7,
            "ALTA Title Insurance Endorsements",
            "ALTA title insurance endorsements modify the coverage of a standard policy. Common endorsements include zoning, access, and survey coverage, which protect lenders and owners against specific title risks.",
            ["ALTA", "title", "insurance", "endorsement"],
            1.0
        ),
        SearchDocument(
            8,
            "Subordination, Non-Disturbance, and Attornment Agreement (SNDA)",
            "An SNDA agreement defines the relationship between tenants and lenders in the event of foreclosure. It ensures tenants are not evicted if the landlord defaults, provided they comply with lease terms.",
            ["SNDA", "subordination", "attornment", "tenant"],
            1.0
        ),
        SearchDocument(
            9,
            "Gross Lease vs Modified Gross Lease",
            "A gross lease requires the landlord to pay all property expenses, while a modified gross lease splits expenses between landlord and tenant. The allocation of operating expenses is negotiated in the lease agreement.",
            ["gross lease", "modified gross", "expenses", "landlord"],
            1.0
        ),
        SearchDocument(
            10,
            "Mezzanine Loan and Intercreditor Agreement",
            "A mezzanine loan is a subordinate loan secured by equity interests rather than real property. Intercreditor agreements establish the rights and remedies of senior and mezzanine lenders in the event of borrower default.",
            ["mezzanine", "loan", "intercreditor", "agreement"],
            1.0
        ),
        SearchDocument(
            11,
            "Construction Loan Mechanics and Holdbacks",
            "Construction loans are short-term, interest-only loans used to finance building projects. Lenders disburse funds in stages, known as draws, and may hold back a portion of funds until project milestones are met.",
            ["construction", "loan", "holdback", "draw"],
            1.0
        ),
        SearchDocument(
            12,
            "CAM Reconciliation and Audit Rights",
            "Common Area Maintenance (CAM) charges are reconciled annually to ensure tenants pay their share of operating expenses. Leases often grant tenants audit rights to review the landlord's CAM calculations.",
            ["CAM", "reconciliation", "audit", "tenant"],
            1.0
        ),
        SearchDocument(
            13,
            "Percentage Rent in Retail Leases",
            "Percentage rent is a lease provision requiring tenants to pay a base rent plus a percentage of gross sales. This structure aligns landlord and tenant interests in retail properties.",
            ["percentage rent", "retail", "lease", "sales"],
            1.0
        ),
        SearchDocument(
            14,
            "Tenant Improvement Allowance and Delivery Condition",
            "A tenant improvement (TI) allowance is a sum provided by the landlord for customizing leased space. Delivery condition describes the state of the premises at lease commencement, such as shell or turnkey.",
            ["tenant improvement", "allowance", "delivery", "condition"],
            1.0
        ),
        SearchDocument(
            15,
            "Zoning Variance and Special Use Permit",
            "A zoning variance allows property owners to deviate from zoning requirements. Special use permits authorize land uses not otherwise permitted in a zoning district, subject to conditions.",
            ["zoning", "variance", "special use", "permit"],
            1.0
        ),
        SearchDocument(
            16,
            "Defeasance in CMBS Loans",
            "Defeasance is a process in CMBS loans where the borrower replaces the real estate collateral with government securities, allowing the release of the property from the mortgage while maintaining payments to investors.",
            ["defeasance", "CMBS", "loan", "collateral"],
            1.0
        ),
        SearchDocument(
            17,
            "Lease Abstracting Best Practices",
            "Lease abstracting involves summarizing key lease terms, including rent, term, options, and obligations. Accurate abstracts are essential for due diligence and portfolio management.",
            ["lease", "abstract", "due diligence", "management"],
            0.9
        ),
        SearchDocument(
            18,
            "Understanding Estoppel Certificates",
            "An estoppel certificate is a document signed by a tenant confirming lease terms and the absence of landlord defaults. Lenders and buyers use estoppels to verify lease status during transactions.",
            ["estoppel", "certificate", "lease", "lender"],
            0.9
        ),
        SearchDocument(
            19,
            "Operating Expense Pass-Throughs",
            "Operating expense pass-throughs require tenants to pay a share of property expenses. Methods include base year, expense stop, and net lease structures. Clear lease language is critical.",
            ["operating expense", "pass-through", "lease", "tenant"],
            0.9
        ),
        SearchDocument(
            20,
            "Loan-to-Value (LTV) Ratio in Commercial Lending",
            "The loan-to-value ratio measures the loan amount relative to property value. Lenders use LTV to assess risk and determine loan terms. Lower LTVs generally result in more favorable rates.",
            ["LTV", "loan", "value", "risk"],
            0.8
        ),
        SearchDocument(
            21,
            "Recourse vs Non-Recourse Loans",
            "Recourse loans allow lenders to pursue borrower assets beyond the collateral, while non-recourse loans limit recovery to the property. Most CMBS loans are non-recourse.",
            ["recourse", "non-recourse", "loan", "CMBS"],
            0.8
        ),
        SearchDocument(
            22,
            "Assignment and Subletting in Commercial Leases",
            "Assignment transfers the tenant's leasehold interest to another party, while subletting allows the tenant to lease part or all of the premises to a subtenant. Landlord consent is typically required.",
            ["assignment", "subletting", "lease", "tenant"],
            0.8
        ),
        SearchDocument(
            23,
            "Due Diligence Checklist for CRE Transactions",
            "A comprehensive due diligence checklist covers title, environmental, zoning, leases, and financials. Thorough due diligence mitigates risk in commercial real estate transactions.",
            ["due diligence", "checklist", "CRE", "risk"],
            0.8
        ),
        SearchDocument(
            24,
            "Understanding Debt Yield in CMBS Lending",
            "Debt yield is a risk metric calculated as net operating income divided by loan amount. CMBS lenders use debt yield to assess property cash flow and loan risk.",
            ["debt yield", "CMBS", "lender", "risk"],
            0.8
        ),
        SearchDocument(
            25,
            "Non-Disturbance Clauses in Leases",
            "Non-disturbance clauses protect tenants from eviction if the landlord's lender forecloses, provided the tenant complies with lease terms. These clauses are often part of SNDA agreements.",
            ["non-disturbance", "lease", "SNDA", "tenant"],
            0.8
        ),
        SearchDocument(
            26,
            "Ground Lease Fundamentals",
            "A ground lease separates ownership of land and improvements. The tenant leases the land and typically constructs and owns the building during the lease term. Ground leases are common in retail and office developments.",
            ["ground lease", "land", "improvements", "tenant"],
            0.8
        ),
        SearchDocument(
            27,
            "Escrow Accounts in Loan Servicing",
            "Escrow accounts are used to collect and disburse funds for property taxes, insurance, and repairs. CMBS loan servicers manage escrow to ensure compliance with loan documents.",
            ["escrow", "loan servicing", "CMBS", "taxes"],
            0.8
        ),
        SearchDocument(
            28,
            "Special Servicer Role in CMBS",
            "A special servicer manages defaulted or specially serviced CMBS loans. Responsibilities include workout negotiations, foreclosure, and property disposition.",
            ["special servicer", "CMBS", "default", "workout"],
            0.8
        ),
        SearchDocument(
            29,
            "Lease Renewal and Expansion Options",
            "Commercial leases may include renewal and expansion options, allowing tenants to extend the lease term or lease additional space. Option terms must be clearly defined in the lease.",
            ["lease", "renewal", "expansion", "option"],
            0.8
        ),
        SearchDocument(
            30,
            "Insurance Requirements in Commercial Leases",
            "Leases specify insurance requirements for tenants and landlords, including liability, property, and business interruption coverage. Adequate insurance protects both parties from risk.",
            ["insurance", "lease", "liability", "coverage"],
            0.8
        ),
    ]
    for doc in docs:
        index.add_document(doc)