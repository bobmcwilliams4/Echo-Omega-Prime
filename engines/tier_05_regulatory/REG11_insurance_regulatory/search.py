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
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in set(tokens):
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            combined_score = (bm25_score * 0.7 + tfidf_score * 0.3) * doc.weight
            if combined_score > 0:
                scores[doc_id] = combined_score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self):
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_length,
            "vocab_size": len(self.doc_freqs)
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
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs.get(doc_id, Counter())
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avgdl)
            numer = f * (self._bm25_k1 + 1)
            score += idf * numer / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 0)
        if doc_len == 0:
            return 0.0
        for term in query_terms:
            tf_norm = tf.get(term, 0) / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:160]
            return snippet + "..." if len(snippet) < len(content) else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + "..."

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
            "McCarran-Ferguson Act: Federal Antitrust Exemption",
            "The McCarran-Ferguson Act of 1945 grants insurance companies a limited exemption from federal antitrust laws, provided that the activities are regulated by state law. This allows states to retain primary authority over insurance regulation, including rate setting and market conduct.",
            ["McCarran-Ferguson", "antitrust", "federal exemption", "state regulation"],
            1.0
        ),
        SearchDocument(
            2,
            "Texas Rate Filing: Prior Approval Requirement",
            "In Texas, certain lines of insurance require prior approval of rates by the Texas Department of Insurance (TDI). Insurers must submit rate filings and receive approval before implementing new rates. The requirement is designed to ensure rates are not excessive, inadequate, or unfairly discriminatory.",
            ["Texas", "rate filing", "prior approval", "TDI"],
            1.0
        ),
        SearchDocument(
            3,
            "Surplus Lines Eligibility and Texas Tax Code Section 226",
            "Surplus lines insurers must meet eligibility criteria under Texas Insurance Code and Tax Code Section 226. Taxes on surplus lines premiums must be remitted to the state, and only eligible surplus lines insurers may write non-admitted business in Texas.",
            ["surplus lines", "eligibility", "tax code", "section 226"],
            1.0
        ),
        SearchDocument(
            4,
            "Risk-Based Capital (RBC) Requirements and Solvency Monitoring",
            "Risk-Based Capital (RBC) standards require insurers to maintain minimum capital based on the risk profile of their business. Regulators use RBC ratios to monitor solvency and may take corrective action if an insurer falls below threshold levels.",
            ["RBC", "solvency", "capital requirements", "regulation"],
            1.0
        ),
        SearchDocument(
            5,
            "Market Conduct Examinations and NAIC Market Regulation Handbook",
            "Market conduct exams assess insurer compliance with laws governing sales, claims, and policyholder treatment. The NAIC Market Regulation Handbook provides uniform standards for conducting these examinations.",
            ["market conduct", "NAIC", "examination", "regulation handbook"],
            1.0
        ),
        SearchDocument(
            6,
            "Unfair Claims Settlement Practices Act (UCSPA)",
            "The UCSPA prohibits insurers from engaging in unfair claims settlement practices, such as misrepresenting policy provisions, failing to promptly investigate claims, or refusing to pay valid claims without reasonable cause.",
            ["UCSPA", "unfair claims", "settlement", "insurance practices"],
            1.0
        ),
        SearchDocument(
            7,
            "Producer Licensing and Appointment Requirements in Texas",
            "All insurance producers must be licensed by the Texas Department of Insurance. Insurers must also appoint producers to act on their behalf. Licensing includes background checks, pre-licensing education, and continuing education requirements.",
            ["producer licensing", "appointment", "Texas", "TDI"],
            1.0
        ),
        SearchDocument(
            8,
            "Texas Guaranty Association: Coverage and Assessments",
            "The Texas Property and Casualty Insurance Guaranty Association provides a safety net for policyholders if an insurer becomes insolvent. Member insurers are assessed to fund the association, and coverage limits apply to claims paid.",
            ["guaranty association", "Texas", "coverage", "assessments"],
            1.0
        ),
        SearchDocument(
            9,
            "Form Approval and Policy Language Requirements",
            "Insurance policy forms and endorsements must be approved by the Texas Department of Insurance before use. Forms must be clear, comply with state law, and not contain unfair or ambiguous language.",
            ["form approval", "policy language", "Texas", "TDI"],
            1.0
        ),
        SearchDocument(
            10,
            "Reinsurance Credit and Unauthorized Reinsurer Collateral Requirements",
            "Insurers may take financial statement credit for reinsurance ceded to authorized reinsurers. For unauthorized reinsurers, collateral must be posted to secure obligations, as required by Texas Insurance Code and NAIC Model Laws.",
            ["reinsurance", "credit", "unauthorized", "collateral"],
            1.0
        ),
        SearchDocument(
            11,
            "NAIC Model Laws and Uniform State Adoption",
            "The National Association of Insurance Commissioners (NAIC) develops model laws and regulations to promote uniformity among states. States may adopt, modify, or reject NAIC models, leading to variations in insurance regulation.",
            ["NAIC", "model laws", "uniform adoption", "state regulation"],
            1.0
        ),
        SearchDocument(
            12,
            "Insurance Holding Company System and Form B/C/D/E Filings",
            "Insurers that are part of a holding company system must file annual and event-driven disclosures (Forms B, C, D, E) with the Texas Department of Insurance. These filings provide transparency regarding ownership, transactions, and enterprise risk.",
            ["holding company", "Form B", "Form C", "Form D", "Form E"],
            1.0
        ),
        SearchDocument(
            13,
            "Rebating Prohibition and Permitted Inducements",
            "Texas law prohibits rebating, which is the offering of inducements not specified in the insurance contract. Certain promotional items and value-added services may be permitted if they meet regulatory guidelines.",
            ["rebating", "inducements", "prohibition", "Texas"],
            1.0
        ),
        SearchDocument(
            14,
            "Twisting and Replacement Regulation",
            "Twisting involves misrepresentation to induce policy replacement. Texas regulations prohibit twisting and require specific disclosures and procedures for policy replacements to protect consumers.",
            ["twisting", "replacement", "regulation", "disclosure"],
            1.0
        ),
        SearchDocument(
            15,
            "Advertising and Marketing Regulation for Insurers",
            "Insurance advertising is regulated to prevent misleading or deceptive statements. The Texas Department of Insurance enforces standards for advertisements, including required disclosures and prohibitions on certain claims.",
            ["advertising", "marketing", "regulation", "Texas"],
            1.0
        ),
        SearchDocument(
            16,
            "Privacy and Information Security: GLBA and State Laws",
            "Insurers must comply with the Gramm-Leach-Bliley Act (GLBA) and Texas privacy laws regarding the collection, use, and disclosure of nonpublic personal information. Information security programs are required to protect consumer data.",
            ["privacy", "GLBA", "information security", "Texas"],
            1.0
        ),
        SearchDocument(
            17,
            "Annual Financial Statement Filing and Statutory Accounting",
            "Insurers must file annual financial statements with the Texas Department of Insurance, prepared in accordance with statutory accounting principles (SAP). These filings are used to assess financial condition and compliance.",
            ["financial statement", "statutory accounting", "SAP", "filing"],
            1.0
        ),
        SearchDocument(
            18,
            "Financial Examination Authority and Examination Report",
            "The Texas Department of Insurance has authority to conduct financial examinations of insurers. Examinations assess solvency, compliance, and risk management practices, and result in a formal report.",
            ["financial examination", "authority", "report", "TDI"],
            1.0
        ),
        SearchDocument(
            19,
            "Own Risk and Solvency Assessment (ORSA) Requirement",
            "ORSA requires insurers to conduct an internal assessment of their risk and solvency position. The ORSA Summary Report must be filed with regulators and is a key part of enterprise risk management.",
            ["ORSA", "solvency", "risk assessment", "enterprise risk"],
            1.0
        ),
        SearchDocument(
            20,
            "Texas Insurance Code: Unfair Discrimination Prohibitions",
            "The Texas Insurance Code prohibits unfair discrimination in rates, premiums, or policy terms based on race, color, religion, or national origin. Insurers must justify rating factors and ensure fairness in underwriting.",
            ["unfair discrimination", "insurance code", "Texas", "underwriting"],
            1.0
        ),
        SearchDocument(
            21,
            "Prompt Payment of Claims Statute",
            "Texas law requires insurers to promptly acknowledge, investigate, and pay valid claims. Penalties may apply for late payment, and the statute establishes timelines for each step of the claims process.",
            ["prompt payment", "claims", "Texas", "statute"],
            1.0
        ),
        SearchDocument(
            22,
            "Insurance Fraud Prevention and Reporting",
            "Insurers must implement anti-fraud programs and report suspected fraud to the Texas Department of Insurance. Fraud prevention efforts include employee training, claim review, and cooperation with law enforcement.",
            ["insurance fraud", "prevention", "reporting", "Texas"],
            1.0
        ),
        SearchDocument(
            23,
            "Corporate Governance Annual Disclosure (CGAD)",
            "The CGAD requires insurers to disclose their corporate governance structure, policies, and practices to regulators. The disclosure aims to enhance oversight and transparency in insurer management.",
            ["corporate governance", "CGAD", "disclosure", "regulation"],
            1.0
        ),
        SearchDocument(
            24,
            "Texas Surplus Lines Stamping Office Requirements",
            "All surplus lines transactions must be reported to the Surplus Lines Stamping Office of Texas. The office reviews filings for compliance with eligibility, tax, and documentation rules.",
            ["surplus lines", "stamping office", "Texas", "compliance"],
            1.0
        ),
        SearchDocument(
            25,
            "NAIC Accreditation Standards for State Insurance Departments",
            "NAIC accreditation ensures that state insurance departments meet baseline standards for solvency regulation, financial analysis, and market conduct oversight. Accredited states must adopt key NAIC model laws.",
            ["NAIC", "accreditation", "solvency", "model laws"],
            1.0
        ),
        SearchDocument(
            26,
            "Texas Insurance Holding Company Act: Enterprise Risk Reporting",
            "The Texas Insurance Holding Company Act requires insurers in a holding company system to file enterprise risk reports, including Form F, to disclose material risks that could affect the insurer or affiliates.",
            ["holding company", "enterprise risk", "Form F", "Texas"],
            1.0
        ),
        SearchDocument(
            27,
            "Reinsurance Intermediary Licensing and Regulation",
            "Reinsurance intermediaries must be licensed in Texas and comply with regulations governing their activities, including disclosure, recordkeeping, and fiduciary responsibilities.",
            ["reinsurance", "intermediary", "licensing", "Texas"],
            1.0
        ),
        SearchDocument(
            28,
            "Group Capital Calculation (GCC) and Group Supervision",
            "The NAIC's Group Capital Calculation (GCC) framework requires insurance groups to assess capital adequacy on a group-wide basis. Group supervision standards apply to internationally active insurance groups.",
            ["group capital", "GCC", "group supervision", "NAIC"],
            1.0
        ),
        SearchDocument(
            29,
            "Texas Insurance Code: Policyholder Notice Requirements",
            "Insurers must provide specific notices to policyholders regarding policy changes, nonrenewal, cancellation, and other material events, as required by the Texas Insurance Code.",
            ["policyholder notice", "insurance code", "Texas", "cancellation"],
            1.0
        ),
        SearchDocument(
            30,
            "Cybersecurity Regulation for Insurers in Texas",
            "Texas law requires insurers to implement cybersecurity programs to protect sensitive information. Requirements include risk assessments, incident response planning, and notification of data breaches.",
            ["cybersecurity", "regulation", "Texas", "data breach"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)