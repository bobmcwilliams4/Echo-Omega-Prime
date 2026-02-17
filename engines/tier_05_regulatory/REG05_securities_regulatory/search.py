import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
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
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_tf: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_term_freq: Dict[str, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.doc_term_freq[doc.id] = tf
            for term in tf:
                self.term_doc_freq[term] += 1
                self.term_doc_tf[term][doc.id] = tf[term]
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = self.doc_term_freq[doc_id]
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        tf = self.doc_term_freq[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[str, float] = {}
        for doc_id in self.documents:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            score = bm25_score + tfidf_score
            if score > 0.0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

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
            "1",
            "Securities Act Section 5 Registration Requirement",
            "Section 5 of the Securities Act prohibits the sale of securities unless a registration statement is filed and declared effective, or an exemption applies. The registration requirement ensures full disclosure to investors.",
            ["registration", "section 5", "securities act"],
            1.0
        ),
        SearchDocument(
            "2",
            "Regulation D Rule 506(b) Private Placement Exemption",
            "Rule 506(b) under Regulation D provides a private placement exemption from registration for offerings to accredited investors and up to 35 non-accredited investors, with no general solicitation permitted.",
            ["regulation d", "rule 506b", "private placement", "exemption"],
            1.0
        ),
        SearchDocument(
            "3",
            "Regulation D Rule 506(c) General Solicitation Exemption",
            "Rule 506(c) allows issuers to engage in general solicitation and advertising, provided all purchasers are verified accredited investors. This exemption requires strict investor verification procedures.",
            ["regulation d", "rule 506c", "general solicitation", "exemption"],
            1.0
        ),
        SearchDocument(
            "4",
            "Regulation A+ Mini-IPO Exemption",
            "Regulation A+ permits companies to raise up to $75 million annually through a streamlined registration process, known as a mini-IPO. Tier 1 and Tier 2 offerings have different disclosure and reporting requirements.",
            ["regulation a+", "mini-ipo", "exemption"],
            1.0
        ),
        SearchDocument(
            "5",
            "Regulation Crowdfunding Exemption",
            "Regulation Crowdfunding enables issuers to raise capital from the public through online platforms, subject to investment limits, disclosure requirements, and SEC oversight.",
            ["crowdfunding", "regulation crowdfunding", "exemption"],
            1.0
        ),
        SearchDocument(
            "6",
            "Rule 144 Resale of Restricted Securities",
            "Rule 144 provides a safe harbor for the resale of restricted and control securities, subject to holding periods, volume limitations, and manner of sale requirements.",
            ["rule 144", "resale", "restricted securities"],
            1.0
        ),
        SearchDocument(
            "7",
            "Exchange Act Section 10(b) and Rule 10b-5 Antifraud",
            "Section 10(b) and Rule 10b-5 prohibit fraud, manipulation, and misrepresentation in connection with the purchase or sale of securities. These provisions are the foundation of securities antifraud enforcement.",
            ["section 10b", "rule 10b-5", "antifraud", "exchange act"],
            1.0
        ),
        SearchDocument(
            "8",
            "Section 16(b) Short-Swing Profit Recovery",
            "Section 16(b) requires officers, directors, and 10% shareholders of public companies to disgorge profits from purchases and sales of company stock within a six-month period.",
            ["section 16b", "short-swing", "profit recovery"],
            1.0
        ),
        SearchDocument(
            "9",
            "Section 13(d) Beneficial Ownership Reporting",
            "Section 13(d) mandates that any person acquiring more than 5% of a class of registered equity securities must file a Schedule 13D with the SEC, disclosing beneficial ownership.",
            ["section 13d", "beneficial ownership", "reporting"],
            1.0
        ),
        SearchDocument(
            "10",
            "Sarbanes-Oxley Section 302 CEO/CFO Certifications",
            "Section 302 of Sarbanes-Oxley requires CEOs and CFOs to certify the accuracy of financial statements and internal controls in periodic reports filed with the SEC.",
            ["sarbanes-oxley", "section 302", "certification"],
            1.0
        ),
        SearchDocument(
            "11",
            "Sarbanes-Oxley Section 404 Internal Control Audits",
            "Section 404 mandates management and auditor assessment of internal controls over financial reporting, increasing transparency and accountability.",
            ["sarbanes-oxley", "section 404", "internal control", "audit"],
            1.0
        ),
        SearchDocument(
            "12",
            "Dodd-Frank Section 922 Whistleblower Protections and Bounties",
            "Section 922 of Dodd-Frank establishes whistleblower protections and financial incentives for reporting securities law violations to the SEC.",
            ["dodd-frank", "section 922", "whistleblower", "protections", "bounties"],
            1.0
        ),
        SearchDocument(
            "13",
            "Broker-Dealer Registration and Finder Exemptions",
            "Broker-dealers must register with the SEC and FINRA unless an exemption applies. Finders may be exempt from registration if their activities are limited and do not involve securities sales.",
            ["broker-dealer", "registration", "finder", "exemption"],
            1.0
        ),
        SearchDocument(
            "14",
            "Integration of Securities Offerings",
            "Integration doctrine determines whether multiple securities offerings should be considered a single offering for regulatory purposes, affecting exemption eligibility.",
            ["integration", "securities offerings"],
            1.0
        ),
        SearchDocument(
            "15",
            "Accredited Investor Definition and Verification",
            "Accredited investors are defined by Regulation D as individuals or entities meeting specific income, net worth, or professional criteria. Verification is required for Rule 506(c) offerings.",
            ["accredited investor", "definition", "verification"],
            1.0
        ),
        SearchDocument(
            "16",
            "Form 10-K Annual Report and MD&A Disclosure",
            "Form 10-K is the annual report filed by public companies, containing audited financial statements and Management's Discussion and Analysis (MD&A) of financial condition and results of operations.",
            ["form 10-k", "annual report", "md&a", "disclosure"],
            1.0
        ),
        SearchDocument(
            "17",
            "Regulation S Offshore Sales Exemption",
            "Regulation S provides an exemption for offers and sales of securities made outside the United States, subject to conditions ensuring offshore transactions.",
            ["regulation s", "offshore", "exemption"],
            1.0
        ),
        SearchDocument(
            "18",
            "Regulation FD Selective Disclosure Prohibition",
            "Regulation FD prohibits selective disclosure of material nonpublic information to certain market participants, requiring simultaneous public disclosure.",
            ["regulation fd", "selective disclosure", "prohibition"],
            1.0
        ),
        SearchDocument(
            "19",
            "Investment Company Act Section 3(c)(1) and 3(c)(7) Exemptions",
            "Sections 3(c)(1) and 3(c)(7) of the Investment Company Act provide exemptions for private investment funds, based on the number and type of investors.",
            ["investment company act", "section 3c1", "section 3c7", "exemption"],
            1.0
        ),
        SearchDocument(
            "20",
            "Blue Sky State Securities Registration and Coordination",
            "Blue Sky laws require registration or qualification of securities offerings at the state level, with coordination between state and federal regulators.",
            ["blue sky", "state registration", "coordination"],
            1.0
        ),
        SearchDocument(
            "21",
            "JOBS Act Emerging Growth Company Benefits",
            "The JOBS Act provides emerging growth companies with reduced disclosure and compliance requirements, facilitating capital formation and IPOs.",
            ["jobs act", "emerging growth", "company", "benefits"],
            1.0
        ),
        SearchDocument(
            "22",
            "Proxy Solicitation and Schedule 14A Requirements",
            "Proxy solicitation rules require companies to provide shareholders with information necessary to make informed voting decisions, including Schedule 14A disclosures.",
            ["proxy solicitation", "schedule 14a", "requirements"],
            1.0
        ),
        SearchDocument(
            "23",
            "Tender Offer Regulation and Schedule TO",
            "Tender offer regulations govern the acquisition of securities through public offers, requiring Schedule TO filings and compliance with procedural rules.",
            ["tender offer", "regulation", "schedule to"],
            1.0
        ),
        SearchDocument(
            "24",
            "Executive Compensation Disclosure and Say-on-Pay",
            "Public companies must disclose executive compensation and provide shareholders with a non-binding say-on-pay vote, promoting transparency and accountability.",
            ["executive compensation", "disclosure", "say-on-pay"],
            1.0
        ),
        SearchDocument(
            "25",
            "Section 12(g) Registration Thresholds",
            "Section 12(g) of the Exchange Act requires companies with a certain number of shareholders and assets to register securities with the SEC.",
            ["section 12g", "registration", "thresholds"],
            1.0
        ),
        SearchDocument(
            "26",
            "Form S-1 Registration Statement",
            "Form S-1 is used by companies to register securities for public offerings under the Securities Act, requiring detailed disclosures about the issuer and offering.",
            ["form s-1", "registration", "statement"],
            1.0
        ),
        SearchDocument(
            "27",
            "Rule 504 Regulation D Small Offerings",
            "Rule 504 under Regulation D allows issuers to raise up to $10 million in a 12-month period, subject to state law and limited disclosure requirements.",
            ["rule 504", "regulation d", "small offerings"],
            1.0
        ),
        SearchDocument(
            "28",
            "Rule 701 Employee Benefit Plan Exemption",
            "Rule 701 provides an exemption for securities issued to employees, directors, and consultants under benefit plans, subject to disclosure thresholds.",
            ["rule 701", "employee benefit", "plan", "exemption"],
            1.0
        ),
        SearchDocument(
            "29",
            "Section 14(e) Tender Offer Antifraud",
            "Section 14(e) prohibits fraudulent, deceptive, or manipulative acts in connection with tender offers, supplementing Rule 10b-5 antifraud provisions.",
            ["section 14e", "tender offer", "antifraud"],
            1.0
        ),
        SearchDocument(
            "30",
            "Schedule 13G Short-Form Beneficial Ownership",
            "Schedule 13G is a short-form beneficial ownership report for passive investors acquiring more than 5% of a class of equity securities.",
            ["schedule 13g", "beneficial ownership", "reporting"],
            1.0
        ),
        SearchDocument(
            "31",
            "Form 8-K Current Report Disclosure",
            "Form 8-K requires public companies to disclose material events, such as mergers, bankruptcies, and changes in executive officers, on a timely basis.",
            ["form 8-k", "current report", "disclosure"],
            1.0
        ),
        SearchDocument(
            "32",
            "Rule 415 Continuous Offering Registration",
            "Rule 415 allows issuers to register securities for continuous or delayed offerings, providing flexibility in capital raising.",
            ["rule 415", "continuous offering", "registration"],
            1.0
        ),
        SearchDocument(
            "33",
            "Rule 12b-25 Notification of Late Filing",
            "Rule 12b-25 permits issuers to notify the SEC of late filings and obtain an extension for periodic reports, subject to conditions.",
            ["rule 12b-25", "notification", "late filing"],
            1.0
        ),
        SearchDocument(
            "34",
            "Rule 10b5-1 Trading Plans",
            "Rule 10b5-1 allows insiders to adopt trading plans for buying or selling securities, providing an affirmative defense against insider trading allegations.",
            ["rule 10b5-1", "trading plan", "insider trading"],
            1.0
        ),
        SearchDocument(
            "35",
            "Rule 3a11-1 Definition of Security",
            "Rule 3a11-1 defines what constitutes a security under the Exchange Act, clarifying the scope of regulated instruments.",
            ["rule 3a11-1", "definition", "security"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)