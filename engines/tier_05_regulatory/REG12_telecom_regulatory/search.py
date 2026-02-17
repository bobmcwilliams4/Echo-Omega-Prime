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
        self.term_idf: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.total_docs: int = 0
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, freq in token_counts.items():
                self.term_doc_tf[token][doc.id] = freq
                self.term_doc_freq[token] += 1
            self._update_avg_doc_length()
            self._compute_idf()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores: Dict[str, float] = defaultdict(float)
        tfidf_scores: Dict[str, float] = defaultdict(float)
        for token in query_tokens:
            if token not in self.term_idf:
                continue
            idf = self.term_idf[token]
            for doc_id in self.term_doc_tf[token]:
                tf = self.term_doc_tf[token][doc_id]
                doc_length = self.doc_lengths[doc_id]
                bm25 = self._score_bm25(tf, idf, doc_length)
                doc_weight = self.documents[doc_id].weight
                scores[doc_id] += bm25 * doc_weight
                tf_norm = tf / doc_length if doc_length > 0 else 0
                tfidf_scores[doc_id] += tf_norm * idf * doc_weight
        results = []
        for doc_id in scores:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            combined_score = scores[doc_id] + 0.5 * tfidf_scores[doc_id]
            results.append(SearchResult(doc_id, combined_score, doc.title, snippet))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self):
        N = self.total_docs
        self.term_idf = {}
        for term, df in self.term_doc_freq.items():
            self.term_idf[term] = math.log(1 + (N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, tf: int, idf: float, doc_length: int) -> float:
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / avg_dl))
        return idf * (numerator / denominator)

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _make_snippet(self, content: str, query_tokens: List[str], window: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return ' '.join(tokens[:window])
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                "doc1",
                "FCC Title II Common Carrier Classification",
                "Title II of the Communications Act classifies telecommunications carriers as common carriers, subjecting them to regulation by the FCC. This includes requirements for nondiscriminatory service, just and reasonable rates, and obligations to interconnect with other carriers.",
                ["FCC", "Title II", "Common Carrier", "Classification"],
                1.0
            ),
            SearchDocument(
                "doc2",
                "TCPA Robocall and Autodialer Restrictions",
                "The Telephone Consumer Protection Act (TCPA) restricts the use of robocalls and autodialers. It requires prior express consent for calls to wireless numbers and imposes penalties for violations. The FCC enforces these rules to protect consumers from unwanted calls.",
                ["TCPA", "Robocall", "Autodialer", "FCC Enforcement"],
                1.0
            ),
            SearchDocument(
                "doc3",
                "Spectrum Licensing and Auction Rules",
                "The FCC manages spectrum allocation through licensing and auctions. Rules govern eligibility, bidding procedures, and post-auction obligations. Spectrum licensees must comply with technical and service requirements to avoid forfeiture.",
                ["Spectrum", "Licensing", "Auction", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc4",
                "Universal Service Fund Contribution Obligations",
                "Telecommunications providers are required to contribute to the Universal Service Fund (USF), which supports affordable communications for rural, low-income, and high-cost areas. The FCC determines contribution factors and enforces compliance.",
                ["USF", "Universal Service Fund", "FCC", "Contribution"],
                1.0
            ),
            SearchDocument(
                "doc5",
                "E-Rate Program for Schools and Libraries",
                "The E-Rate program provides discounts to schools and libraries for telecommunications and internet access. Applicants must follow FCC rules for eligibility, competitive bidding, and recordkeeping. Funding is distributed annually based on need.",
                ["E-Rate", "Schools", "Libraries", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc6",
                "Interconnection Obligations Under Sections 251-252",
                "Sections 251 and 252 of the Communications Act require carriers to interconnect networks and negotiate agreements. The FCC and state commissions oversee arbitration and approval of interconnection agreements. Disputes are resolved through regulatory processes.",
                ["Interconnection", "Section 251", "Section 252", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc7",
                "Local Number Portability Administration",
                "Local Number Portability (LNP) allows customers to retain their phone numbers when switching providers. The FCC mandates LNP to promote competition and consumer choice. Carriers must comply with technical standards and administrative procedures.",
                ["LNP", "Local Number Portability", "FCC", "Competition"],
                1.0
            ),
            SearchDocument(
                "doc8",
                "STIR/SHAKEN Caller ID Authentication",
                "STIR/SHAKEN is a framework for authenticating caller ID information to combat spoofed robocalls. The FCC requires carriers to implement STIR/SHAKEN protocols and report compliance. Enforcement actions target non-compliant providers.",
                ["STIR", "SHAKEN", "Caller ID", "Authentication", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc9",
                "State PUC Certificate of Public Convenience and Necessity",
                "State Public Utility Commissions (PUCs) issue Certificates of Public Convenience and Necessity (CPCN) to telecommunications providers. The process involves demonstrating financial, technical, and managerial qualifications. State rules vary by jurisdiction.",
                ["PUC", "CPCN", "State Regulation", "Telecommunications"],
                1.0
            ),
            SearchDocument(
                "doc10",
                "Broadband Deployment and Mapping Requirements",
                "The FCC requires broadband providers to submit deployment data for mapping purposes. Accurate reporting supports policy decisions and funding allocations. The Broadband DATA Act mandates standardized reporting formats and verification.",
                ["Broadband", "Deployment", "Mapping", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc11",
                "Net Neutrality Open Internet Rules",
                "Net neutrality rules prohibit blocking, throttling, and paid prioritization of internet traffic. The FCC enforces open internet principles to ensure equal access. Legal challenges have shaped the scope and enforcement of these rules.",
                ["Net Neutrality", "Open Internet", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc12",
                "FCC Enforcement Actions and Forfeiture",
                "The FCC investigates violations of communications laws and imposes forfeitures. Enforcement actions may include fines, license revocation, and compliance orders. The process involves notice, response, and adjudication.",
                ["FCC", "Enforcement", "Forfeiture", "Compliance"],
                1.0
            ),
            SearchDocument(
                "doc13",
                "Telecommunications Carrier Obligations Under Title II",
                "Title II imposes obligations on telecommunications carriers, including nondiscriminatory access, interconnection, and reporting. The FCC monitors compliance and may grant waivers for specific requirements.",
                ["Title II", "Carrier", "Obligations", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc14",
                "TCPA Consent Requirements for Robocalls",
                "The TCPA requires prior express written consent for certain types of robocalls. The FCC clarifies consent standards and exemptions for informational calls. Violations may result in statutory damages.",
                ["TCPA", "Consent", "Robocalls", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc15",
                "Spectrum Auction Bidding Procedures",
                "FCC spectrum auctions use competitive bidding to allocate licenses. Procedures include bidder qualification, reserve prices, and anti-collusion rules. Winning bidders must meet post-auction obligations.",
                ["Spectrum", "Auction", "Bidding", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc16",
                "Universal Service Fund Compliance Audits",
                "The FCC conducts audits of USF contributors and recipients to ensure compliance. Audits review financial records, eligibility, and use of funds. Non-compliance may result in recovery of funds and penalties.",
                ["USF", "Compliance", "Audit", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc17",
                "E-Rate Competitive Bidding Requirements",
                "E-Rate applicants must conduct competitive bidding for eligible services. The FCC enforces rules to prevent waste, fraud, and abuse. Documentation is required for all bids and contracts.",
                ["E-Rate", "Bidding", "FCC", "Schools"],
                1.0
            ),
            SearchDocument(
                "doc18",
                "Interconnection Agreement Arbitration",
                "Disputes over interconnection agreements may be resolved through arbitration by the FCC or state commissions. The process includes submission of proposals, hearings, and issuance of binding decisions.",
                ["Interconnection", "Arbitration", "FCC", "State"],
                1.0
            ),
            SearchDocument(
                "doc19",
                "Local Number Portability Technical Standards",
                "LNP implementation relies on technical standards for database management and routing. The FCC oversees compliance and updates standards as technology evolves.",
                ["LNP", "Technical Standards", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc20",
                "STIR/SHAKEN Implementation Deadlines",
                "The FCC sets deadlines for carriers to implement STIR/SHAKEN protocols. Extensions may be granted for smaller providers. Progress reports are required to demonstrate compliance.",
                ["STIR", "SHAKEN", "Implementation", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc21",
                "State PUC Application Process for CPCN",
                "Applying for a CPCN involves submitting financial statements, technical plans, and service descriptions. State PUCs review applications and may hold public hearings.",
                ["PUC", "CPCN", "Application", "State"],
                1.0
            ),
            SearchDocument(
                "doc22",
                "Broadband DATA Act Reporting Standards",
                "The Broadband DATA Act requires providers to submit standardized deployment data. The FCC verifies submissions and updates national broadband maps.",
                ["Broadband", "DATA Act", "Reporting", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc23",
                "Net Neutrality Legal Challenges",
                "Legal challenges to FCC net neutrality rules have resulted in court decisions affecting enforcement. The current status depends on ongoing litigation and regulatory actions.",
                ["Net Neutrality", "Legal", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc24",
                "FCC Forfeiture Calculation Guidelines",
                "The FCC uses guidelines to calculate forfeitures for violations. Factors include severity, duration, and prior history. Licensees may appeal forfeiture decisions.",
                ["FCC", "Forfeiture", "Guidelines"],
                1.0
            ),
            SearchDocument(
                "doc25",
                "Telecommunications Carrier Reporting Requirements",
                "Carriers must file periodic reports with the FCC, including financial, operational, and compliance information. Failure to report may result in enforcement actions.",
                ["Carrier", "Reporting", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc26",
                "TCPA Safe Harbor Provisions",
                "The TCPA provides safe harbor provisions for certain autodialed calls made in error. The FCC defines criteria for eligibility and documentation requirements.",
                ["TCPA", "Safe Harbor", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc27",
                "Spectrum License Renewal Procedures",
                "Spectrum licensees must follow FCC procedures for renewal, including demonstrating ongoing compliance and service provision. Failure to renew may result in license forfeiture.",
                ["Spectrum", "License", "Renewal", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc28",
                "Universal Service Fund Lifeline Program",
                "The Lifeline program provides discounted phone and broadband service to low-income consumers. The FCC sets eligibility criteria and monitors provider compliance.",
                ["USF", "Lifeline", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc29",
                "E-Rate Recordkeeping Requirements",
                "E-Rate participants must maintain records of bids, contracts, and invoices for audit purposes. The FCC may request documentation during compliance reviews.",
                ["E-Rate", "Recordkeeping", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc30",
                "Interconnection Pricing Standards",
                "The FCC establishes pricing standards for interconnection agreements to ensure fairness and promote competition. Rates are subject to review and adjustment.",
                ["Interconnection", "Pricing", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc31",
                "Local Number Portability Administration Costs",
                "Carriers share costs for LNP administration, including database management and technical upgrades. The FCC oversees cost allocation and reimbursement.",
                ["LNP", "Costs", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc32",
                "STIR/SHAKEN Enforcement Actions",
                "The FCC takes enforcement actions against carriers that fail to implement STIR/SHAKEN protocols. Penalties may include fines and compliance orders.",
                ["STIR", "SHAKEN", "Enforcement", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc33",
                "State PUC Revocation of CPCN",
                "State PUCs may revoke CPCNs for non-compliance or abandonment of service. The process involves notice, hearings, and final orders.",
                ["PUC", "CPCN", "Revocation", "State"],
                1.0
            ),
            SearchDocument(
                "doc34",
                "Broadband Mapping Verification Procedures",
                "The FCC verifies broadband deployment data through audits and field testing. Accurate mapping is essential for funding and policy decisions.",
                ["Broadband", "Mapping", "Verification", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc35",
                "Net Neutrality Transparency Requirements",
                "ISPs must disclose network management practices, performance, and commercial terms under FCC transparency rules. Consumers rely on disclosures to make informed choices.",
                ["Net Neutrality", "Transparency", "FCC"],
                1.0
            ),
            SearchDocument(
                "doc36",
                "FCC Enforcement Process Overview",
                "The FCC enforcement process includes investigation, notice of apparent liability, response, and final order. Licensees have opportunities to contest allegations.",
                ["FCC", "Enforcement", "Process"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _search_index_instance._preseed_documents()
        return _search_index_instance