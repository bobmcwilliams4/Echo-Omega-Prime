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
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._re_token = re.compile(r"\b\w+\b")
    
    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._re_token.findall(text)]
    
    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N
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
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (f * (self.k1 + 1)) / denom
        doc = self.documents[doc_id]
        return score * doc.weight
    
    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        doc = self.documents[doc_id]
        return score * doc.weight
    
    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores = {}
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc_scores[doc_id] = score
        top_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results
    
    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        hit_indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not hit_indices:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(hit_indices[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        # Highlight query terms
        for term in set(query_terms):
            snippet = re.sub(r'\b{}\b'.format(re.escape(term)), f'**{term}**', snippet, flags=re.IGNORECASE)
        return snippet + "..."
    
    def get_stats(self) -> Dict[str, int]:
        return {
            "num_documents": self.N,
            "num_terms": len(self.doc_freqs),
            "avg_doc_length": int(self.avg_doc_length)
        }

# Singleton pattern for SearchIndex
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
            "Due Diligence Checklist Overview",
            "A comprehensive checklist for due diligence in asset and deal (A&D) transactions, including legal, financial, operational, and compliance aspects.",
            ["overview", "checklist", "A&D", "compliance"],
            1.0
        ),
        SearchDocument(
            2,
            "Title Due Diligence Essentials",
            "Procedures for verifying title ownership, reviewing encumbrances, and identifying title defects in property and asset transactions.",
            ["title", "ownership", "encumbrances", "defects"],
            1.0
        ),
        SearchDocument(
            3,
            "Environmental Due Diligence Steps",
            "Key steps in environmental due diligence: Phase I ESA, site inspections, regulatory compliance, and environmental liability assessment.",
            ["environmental", "ESA", "liability", "compliance"],
            1.0
        ),
        SearchDocument(
            4,
            "Regulatory Due Diligence Guidelines",
            "Assessing regulatory risk, permits, licenses, and compliance with local, state, and federal regulations in A&D transactions.",
            ["regulatory", "permits", "licenses", "risk"],
            1.0
        ),
        SearchDocument(
            5,
            "Financial Due Diligence Checklist",
            "Review of financial statements, tax records, debt obligations, and revenue streams to identify financial risks and opportunities.",
            ["financial", "statements", "tax", "revenue"],
            1.0
        ),
        SearchDocument(
            6,
            "Operational Due Diligence Framework",
            "Evaluation of operational processes, asset integrity, production history, and key personnel in transaction targets.",
            ["operational", "processes", "integrity", "personnel"],
            1.0
        ),
        SearchDocument(
            7,
            "Reserve Due Diligence in Oil & Gas",
            "Analysis of reserve reports, engineering data, and third-party audits to validate reserve quantities and classifications.",
            ["reserve", "oil & gas", "engineering", "audit"],
            1.0
        ),
        SearchDocument(
            8,
            "Contractual Due Diligence Review",
            "Examination of material contracts, change of control clauses, and assignment provisions in transaction documentation.",
            ["contractual", "contracts", "assignment", "clauses"],
            1.0
        ),
        SearchDocument(
            9,
            "Litigation Due Diligence Process",
            "Identification of pending, threatened, or historical litigation, and assessment of potential liabilities and legal exposures.",
            ["litigation", "legal", "liabilities", "exposure"],
            1.0
        ),
        SearchDocument(
            10,
            "Tax Due Diligence Procedures",
            "Review of tax compliance, outstanding liabilities, tax structure, and planning opportunities in M&A transactions.",
            ["tax", "compliance", "liabilities", "planning"],
            1.0
        ),
        SearchDocument(
            11,
            "Compliance Due Diligence Checklist",
            "Assessment of anti-corruption, anti-bribery, sanctions, and other compliance risks in cross-border transactions.",
            ["compliance", "anti-corruption", "sanctions", "bribery"],
            1.0
        ),
        SearchDocument(
            12,
            "Material Contract Review Best Practices",
            "Guidelines for reviewing material contracts, including termination rights, indemnities, and representations and warranties.",
            ["material contract", "review", "indemnities", "warranties"],
            1.0
        ),
        SearchDocument(
            13,
            "Data Room Organization for Due Diligence",
            "Best practices for organizing virtual data rooms: document indexing, access controls, and version management.",
            ["data room", "organization", "indexing", "access"],
            1.0
        ),
        SearchDocument(
            14,
            "Red Flag Identification in Due Diligence",
            "Techniques for identifying red flags such as undisclosed liabilities, regulatory violations, and inconsistent disclosures.",
            ["red flag", "identification", "liabilities", "violations"],
            1.0
        ),
        SearchDocument(
            15,
            "A&D Transaction Due Diligence Workflow",
            "Step-by-step workflow for conducting due diligence in asset and deal transactions, from initial screening to closing.",
            ["A&D", "workflow", "screening", "closing"],
            1.0
        ),
        SearchDocument(
            16,
            "Title Defect Curing Strategies",
            "Approaches to curing title defects, including corrective deeds, curative affidavits, and quiet title actions.",
            ["title", "defect", "curative", "deed"],
            1.0
        ),
        SearchDocument(
            17,
            "Environmental Liabilities and Remediation",
            "Assessing environmental liabilities, remediation obligations, and cost recovery in asset transactions.",
            ["environmental", "liabilities", "remediation", "cost"],
            1.0
        ),
        SearchDocument(
            18,
            "Regulatory Permitting Risks",
            "Identifying and mitigating risks related to regulatory permitting, reporting obligations, and compliance deadlines.",
            ["regulatory", "permitting", "risk", "reporting"],
            1.0
        ),
        SearchDocument(
            19,
            "Financial Statement Analysis for Due Diligence",
            "Analyzing balance sheets, income statements, and cash flows to uncover financial health and hidden risks.",
            ["financial", "analysis", "balance sheet", "cash flow"],
            1.0
        ),
        SearchDocument(
            20,
            "Operational Synergies in M&A",
            "Evaluating operational synergies, integration challenges, and value creation opportunities in mergers and acquisitions.",
            ["operational", "synergy", "integration", "M&A"],
            1.0
        ),
        SearchDocument(
            21,
            "Reserve Report Interpretation",
            "How to interpret engineering reserve reports, SEC classifications, and third-party reserve audits.",
            ["reserve", "report", "engineering", "SEC"],
            1.0
        ),
        SearchDocument(
            22,
            "Change of Control Clauses in Contracts",
            "Understanding the implications of change of control clauses and anti-assignment provisions in material agreements.",
            ["contract", "change of control", "assignment", "agreements"],
            1.0
        ),
        SearchDocument(
            23,
            "Pending Litigation Risk Assessment",
            "Evaluating the impact of pending litigation, settlement negotiations, and contingent liabilities on deal value.",
            ["litigation", "risk", "settlement", "contingent"],
            1.0
        ),
        SearchDocument(
            24,
            "Tax Structure Optimization in Transactions",
            "Strategies for optimizing tax structure, minimizing liabilities, and leveraging tax credits in M&A.",
            ["tax", "structure", "optimization", "credits"],
            1.0
        ),
        SearchDocument(
            25,
            "Compliance Risk Scoring Models",
            "Developing risk scoring models for compliance due diligence, including KYC, AML, and sanctions screening.",
            ["compliance", "risk", "KYC", "AML"],
            1.0
        ),
        SearchDocument(
            26,
            "Virtual Data Room Security",
            "Security best practices for virtual data rooms: encryption, access logs, and user authentication.",
            ["data room", "security", "encryption", "authentication"],
            1.0
        ),
        SearchDocument(
            27,
            "Red Flag Reporting Templates",
            "Templates and reporting formats for documenting and communicating red flag findings during due diligence.",
            ["red flag", "reporting", "templates", "communication"],
            1.0
        ),
        SearchDocument(
            28,
            "Operational KPI Benchmarking",
            "Benchmarking operational KPIs to assess efficiency, productivity, and performance in target assets.",
            ["operational", "KPI", "benchmarking", "performance"],
            1.0
        ),
        SearchDocument(
            29,
            "Material Adverse Change Provisions",
            "Reviewing material adverse change (MAC) provisions and their impact on deal certainty and closing conditions.",
            ["material contract", "MAC", "provisions", "closing"],
            1.0
        ),
        SearchDocument(
            30,
            "Litigation Hold and Preservation",
            "Implementing litigation hold and preservation protocols to safeguard evidence during due diligence.",
            ["litigation", "hold", "preservation", "evidence"],
            1.0
        ),
        SearchDocument(
            31,
            "Tax Due Diligence in Cross-Border Deals",
            "Special considerations for tax due diligence in cross-border transactions, including transfer pricing and treaty benefits.",
            ["tax", "cross-border", "transfer pricing", "treaty"],
            1.0
        ),
        SearchDocument(
            32,
            "Compliance Audit Trail Requirements",
            "Maintaining robust audit trails for compliance, including documentation, approvals, and exception handling.",
            ["compliance", "audit trail", "documentation", "approvals"],
            1.0
        ),
        SearchDocument(
            33,
            "Data Room Indexing Strategies",
            "Effective strategies for indexing documents in virtual data rooms to enhance searchability and user experience.",
            ["data room", "indexing", "strategy", "searchability"],
            1.0
        ),
        SearchDocument(
            34,
            "Red Flag Escalation Procedures",
            "Procedures for escalating red flag issues to management and legal counsel during due diligence.",
            ["red flag", "escalation", "procedure", "management"],
            1.0
        ),
        SearchDocument(
            35,
            "Reserve Due Diligence: SEC vs PRMS",
            "Comparing SEC and PRMS standards for reserve due diligence in oil and gas transactions.",
            ["reserve", "SEC", "PRMS", "oil & gas"],
            1.0
        ),
        SearchDocument(
            36,
            "Contract Assignment and Novation",
            "Key considerations for contract assignment, novation, and third-party consents in asset transfers.",
            ["contract", "assignment", "novation", "consent"],
            1.0
        ),
        SearchDocument(
            37,
            "Operational Risk Matrix for Due Diligence",
            "Building an operational risk matrix to prioritize and mitigate risks in transaction targets.",
            ["operational", "risk", "matrix", "mitigation"],
            1.0
        ),
        SearchDocument(
            38,
            "Financial Red Flags in M&A",
            "Common financial red flags: revenue recognition issues, unrecorded liabilities, and aggressive accounting.",
            ["financial", "red flag", "M&A", "accounting"],
            1.0
        ),
        SearchDocument(
            39,
            "Environmental Site Assessment Checklist",
            "Checklist for conducting Phase I and II Environmental Site Assessments (ESA) in asset transactions.",
            ["environmental", "ESA", "site assessment", "checklist"],
            1.0
        ),
        SearchDocument(
            40,
            "Litigation Exposure Quantification",
            "Methods for quantifying litigation exposure and estimating settlement ranges in due diligence.",
            ["litigation", "exposure", "quantification", "settlement"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)