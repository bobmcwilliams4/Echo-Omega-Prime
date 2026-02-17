import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set

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
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # No duplicate IDs
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self.inverted_index.get(term, set()))
        scored_results = []
        for doc_id in candidate_doc_ids:
            score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            final_score = 0.7 * score + 0.3 * tfidf_score
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            scored_results.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, int]:
        return {
            'total_documents': self.total_docs,
            'unique_terms': len(self.doc_freqs),
            'avg_doc_length': int(self.avg_doc_length)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        doc = self.documents[doc_id]
        score = 0.0
        for term in query_terms:
            idf = self._compute_idf(term)
            freq = tf.get(term, 0)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            if denominator == 0:
                continue
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            term_freq = tf.get(term, 0)
            if term_freq == 0:
                continue
            tf_norm = term_freq / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:160]
            return snippet + '...' if len(content) > 160 else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + '...'

# Singleton factory for SearchIndex
_search_index_instance = None
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

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "BSA Currency Transaction Reporting Requirements",
            "Banks must file a Currency Transaction Report (CTR) for each transaction in currency over $10,000 by, through, or to the bank, per the Bank Secrecy Act (BSA). Aggregation rules apply to multiple related transactions.",
            ["BSA", "CTR", "Currency Transaction Reporting"],
            1.0
        ),
        SearchDocument(
            2,
            "Suspicious Activity Reporting (SAR) Obligations",
            "Financial institutions are required to file Suspicious Activity Reports (SARs) for transactions involving possible money laundering, fraud, or other suspicious activities. SARs must be filed within 30 days of detection.",
            ["BSA", "SAR", "AML"],
            1.0
        ),
        SearchDocument(
            3,
            "Customer Due Diligence (CDD) Rule",
            "The CDD Rule requires banks to identify and verify the identity of beneficial owners of legal entity customers, and to understand the nature and purpose of customer relationships for ongoing monitoring.",
            ["CDD", "Beneficial Ownership", "AML"],
            1.0
        ),
        SearchDocument(
            4,
            "Regulation Z - TILA APR Disclosure",
            "Regulation Z implements the Truth in Lending Act (TILA), requiring clear disclosure of the annual percentage rate (APR), finance charges, and other terms for consumer credit transactions.",
            ["Regulation Z", "TILA", "APR"],
            1.0
        ),
        SearchDocument(
            5,
            "RESPA Section 8 Kickback Prohibition",
            "Section 8 of the Real Estate Settlement Procedures Act (RESPA) prohibits giving or accepting fees, kickbacks, or anything of value for referrals of settlement service business related to federally related mortgage loans.",
            ["RESPA", "Kickback", "Section 8"],
            1.0
        ),
        SearchDocument(
            6,
            "ECOA Regulation B Fair Lending",
            "The Equal Credit Opportunity Act (ECOA) and Regulation B prohibit discrimination in any aspect of a credit transaction on the basis of race, color, religion, national origin, sex, marital status, or age.",
            ["ECOA", "Regulation B", "Fair Lending"],
            1.0
        ),
        SearchDocument(
            7,
            "Community Reinvestment Act (CRA)",
            "The CRA encourages banks to help meet the credit needs of the communities in which they operate, including low- and moderate-income neighborhoods, consistent with safe and sound operations.",
            ["CRA", "Community Development"],
            1.0
        ),
        SearchDocument(
            8,
            "Basel III Capital Requirements",
            "Basel III establishes minimum capital requirements for banks, including Common Equity Tier 1 (CET1), Tier 1, and Total Capital ratios, as well as capital conservation and countercyclical buffers.",
            ["Basel III", "Capital", "CET1"],
            1.0
        ),
        SearchDocument(
            9,
            "DFAST Dodd-Frank Stress Testing",
            "The Dodd-Frank Act Stress Test (DFAST) requires certain banks to conduct annual stress tests to assess capital adequacy under adverse economic conditions, reporting results to regulators.",
            ["DFAST", "Stress Test", "Dodd-Frank"],
            1.0
        ),
        SearchDocument(
            10,
            "Volcker Rule Proprietary Trading Restrictions",
            "The Volcker Rule prohibits banking entities from engaging in proprietary trading and restricts ownership interests in hedge funds and private equity funds, with certain exemptions.",
            ["Volcker Rule", "Proprietary Trading"],
            1.0
        ),
        SearchDocument(
            11,
            "Regulation E - Electronic Fund Transfers",
            "Regulation E implements the Electronic Fund Transfer Act (EFTA), establishing rights, liabilities, and responsibilities of consumers and financial institutions regarding electronic fund transfers.",
            ["Regulation E", "EFTA", "Electronic Transfers"],
            1.0
        ),
        SearchDocument(
            12,
            "GLBA Privacy and Safeguards Rule",
            "The Gramm-Leach-Bliley Act (GLBA) requires financial institutions to protect the privacy of consumer information and implement safeguards to ensure the security and confidentiality of customer records.",
            ["GLBA", "Privacy", "Safeguards"],
            1.0
        ),
        SearchDocument(
            13,
            "Bank Secrecy Act Recordkeeping Requirements",
            "The BSA requires banks to maintain records of certain transactions, such as wire transfers and monetary instrument sales, to assist law enforcement in detecting and preventing financial crimes.",
            ["BSA", "Recordkeeping"],
            1.0
        ),
        SearchDocument(
            14,
            "OFAC Sanctions Compliance",
            "Banks must comply with Office of Foreign Assets Control (OFAC) sanctions programs, including screening transactions and customers against government lists of sanctioned individuals and entities.",
            ["OFAC", "Sanctions", "Compliance"],
            1.0
        ),
        SearchDocument(
            15,
            "Liquidity Coverage Ratio (LCR)",
            "The LCR requires large banks to hold a sufficient stock of high-quality liquid assets to cover total net cash outflows over a 30-day stress period, as part of Basel III liquidity standards.",
            ["LCR", "Liquidity", "Basel III"],
            1.0
        ),
        SearchDocument(
            16,
            "UDAAP - Unfair, Deceptive, or Abusive Acts or Practices",
            "UDAAP prohibits banks from engaging in unfair, deceptive, or abusive acts or practices in connection with consumer financial products or services, as enforced by the CFPB.",
            ["UDAAP", "CFPB", "Consumer Protection"],
            1.0
        ),
        SearchDocument(
            17,
            "Durbin Amendment - Interchange Fee Regulation",
            "The Durbin Amendment limits interchange fees that large debit card issuers can charge merchants, and requires routing and exclusivity provisions for electronic debit transactions.",
            ["Durbin Amendment", "Interchange Fee", "Regulation II"],
            1.0
        ),
        SearchDocument(
            18,
            "Home Mortgage Disclosure Act (HMDA)",
            "HMDA requires certain financial institutions to collect, report, and disclose data about home mortgage applications, originations, and purchases to help ensure fair lending and inform public policy.",
            ["HMDA", "Mortgage", "Disclosure"],
            1.0
        ),
        SearchDocument(
            19,
            "TILA-RESPA Integrated Disclosures (TRID)",
            "TRID combines TILA and RESPA disclosures for closed-end consumer mortgage loans, requiring the Loan Estimate and Closing Disclosure to help consumers understand loan terms and costs.",
            ["TRID", "TILA", "RESPA"],
            1.0
        ),
        SearchDocument(
            20,
            "Affiliate Marketing Opt-Out - FCRA Section 624",
            "Section 624 of the Fair Credit Reporting Act (FCRA) allows consumers to opt out of marketing solicitations from affiliates based on certain information shared among affiliated companies.",
            ["FCRA", "Affiliate Marketing", "Opt-Out"],
            1.0
        ),
        SearchDocument(
            21,
            "Expedited Funds Availability Act - Regulation CC",
            "Regulation CC implements the Expedited Funds Availability Act, setting rules for the availability of deposited funds and disclosure of funds availability policies to customers.",
            ["Regulation CC", "Funds Availability"],
            1.0
        ),
        SearchDocument(
            22,
            "HMDA Loan Data Integrity and Accuracy",
            "Financial institutions must ensure the integrity and accuracy of HMDA loan data, including proper collection, recording, and reporting of required data fields for regulatory compliance.",
            ["HMDA", "Data Integrity", "Reporting"],
            1.0
        ),
        SearchDocument(
            23,
            "OCC Heightened Standards for Large Banks",
            "The OCC's heightened standards require large national banks to establish and maintain effective risk governance frameworks, including board oversight and independent risk management.",
            ["OCC", "Heightened Standards", "Risk Governance"],
            1.0
        ),
        SearchDocument(
            24,
            "AML Program Requirements under the Bank Secrecy Act",
            "Banks must implement an anti-money laundering (AML) program that includes internal controls, independent testing, designation of a compliance officer, and ongoing employee training.",
            ["AML", "BSA", "Compliance Program"],
            1.0
        ),
        SearchDocument(
            25,
            "Countercyclical Capital Buffer under Basel III",
            "The countercyclical capital buffer is a Basel III tool that requires banks to hold additional capital during periods of high credit growth to protect against systemic risk.",
            ["Basel III", "Capital Buffer", "Systemic Risk"],
            1.0
        ),
        SearchDocument(
            26,
            "Beneficial Ownership Identification and Verification",
            "Banks must identify and verify the beneficial owners of legal entity customers as part of the CDD Rule, including collecting information on individuals with significant ownership or control.",
            ["CDD", "Beneficial Ownership", "KYC"],
            1.0
        ),
        SearchDocument(
            27,
            "Regulation Z - Right of Rescission",
            "Regulation Z provides consumers with a right of rescission for certain home-secured loans, allowing them to cancel the loan within three business days after closing.",
            ["Regulation Z", "TILA", "Rescission"],
            1.0
        ),
        SearchDocument(
            28,
            "OFAC List Screening Procedures",
            "Banks must have procedures to screen customers and transactions against OFAC lists, including the Specially Designated Nationals (SDN) list, to prevent prohibited transactions.",
            ["OFAC", "SDN", "List Screening"],
            1.0
        ),
        SearchDocument(
            29,
            "Stress Testing Governance and Controls",
            "Banks subject to DFAST must have strong governance and internal controls over their stress testing processes, including model risk management and board oversight.",
            ["DFAST", "Stress Testing", "Governance"],
            1.0
        ),
        SearchDocument(
            30,
            "UDAAP Enforcement Actions",
            "The CFPB and other regulators may take enforcement actions against banks for UDAAP violations, including monetary penalties and remediation for harmed consumers.",
            ["UDAAP", "CFPB", "Enforcement"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)