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
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.lock = threading.Lock()
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.tf_idf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            for token in tokens:
                self.term_freqs[token][doc.id] += 1
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.term_doc_freq[token] += 1
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            )
            self.idf_cache.clear()
            self.tf_idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        for term in query_terms:
            tf = self.term_freqs[term].get(doc_id, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length or 1))
            score += idf * (numerator / (denominator or 1))
        return score * doc.weight

    def _score_tf_idf(self, query_terms: List[str], doc_id: str) -> float:
        doc = self.documents[doc_id]
        doc_length = self.doc_lengths.get(doc_id, 0)
        score = 0.0
        for term in query_terms:
            tf = self.term_freqs[term].get(doc_id, 0)
            if doc_length > 0:
                norm_tf = tf / doc_length
            else:
                norm_tf = 0.0
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_freqs[term].keys())
        scored_docs = []
        for doc_id in candidate_docs:
            if method == "bm25":
                score = self._score_bm25(query_terms, doc_id)
            elif method == "tfidf":
                score = self._score_tf_idf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scored_docs.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored_docs.sort(key=lambda x: x.score, reverse=True)
        return scored_docs[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], max_length: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:max_length] + ("..." if len(content) > max_length else "")
            return snippet
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        if len(snippet) > max_length:
            snippet = snippet[:max_length] + "..."
        for term in query_terms:
            snippet = re.sub(r'\b(' + re.escape(term) + r')\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_documents": self.total_docs,
            "average_document_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
        }

_search_index_singleton: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_singleton
    if _search_index_singleton is None:
        with _search_index_lock:
            if _search_index_singleton is None:
                _search_index_singleton = SearchIndex()
                _preseed_documents(_search_index_singleton)
    return _search_index_singleton

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="flsa_01",
            title="FLSA Overtime Classification Guidelines",
            content="The Fair Labor Standards Act (FLSA) defines overtime eligibility for employees. Exempt and non-exempt classifications depend on job duties and salary thresholds. Employers must ensure accurate classification to avoid penalties.",
            tags=["flsa", "overtime", "classification", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="fmla_01",
            title="FMLA Eligibility and Entitlement Criteria",
            content="The Family and Medical Leave Act (FMLA) provides eligible employees up to 12 weeks of unpaid leave for specified family and medical reasons. Eligibility requires 12 months of service and 1,250 hours worked in the previous year.",
            tags=["fmla", "leave", "eligibility", "entitlement"],
            weight=1.0
        ),
        SearchDocument(
            id="pay_equity_01",
            title="Pay Equity Analysis Best Practices",
            content="Pay equity analysis involves comparing compensation across similar roles to identify disparities. Statistical methods and regression analysis are used to ensure fair pay regardless of gender, race, or other protected characteristics.",
            tags=["pay_equity", "analysis", "compensation", "fairness"],
            weight=1.0
        ),
        SearchDocument(
            id="ada_01",
            title="ADA Reasonable Accommodation Process",
            content="The Americans with Disabilities Act (ADA) requires employers to provide reasonable accommodations for qualified employees with disabilities. The interactive process includes assessment, documentation, and implementation of accommodations.",
            tags=["ada", "accommodation", "disability", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="turnover_01",
            title="Workforce Turnover Analysis Techniques",
            content="Turnover analysis examines employee exit trends to identify root causes. Metrics include voluntary and involuntary turnover rates, retention strategies, and predictive modeling for flight risk assessment.",
            tags=["turnover", "analysis", "retention", "flight_risk"],
            weight=1.0
        ),
        SearchDocument(
            id="comp_band_01",
            title="Compensation Band Design Framework",
            content="Compensation bands establish salary ranges for job families. Design principles include market benchmarking, internal equity, and progression paths to support talent management and pay transparency.",
            tags=["compensation", "band", "design", "salary"],
            weight=1.0
        ),
        SearchDocument(
            id="perf_calib_01",
            title="Performance Calibration Process",
            content="Performance calibration aligns employee ratings across departments to ensure fairness and consistency. Calibration sessions involve managers reviewing evaluations, discussing criteria, and adjusting ratings as needed.",
            tags=["performance", "calibration", "evaluation", "fairness"],
            weight=1.0
        ),
        SearchDocument(
            id="succession_01",
            title="Succession Planning Framework",
            content="Succession planning identifies and develops future leaders for critical roles. Key steps include talent assessment, readiness evaluation, and targeted development plans to mitigate leadership gaps.",
            tags=["succession", "planning", "leadership", "talent"],
            weight=1.0
        ),
        SearchDocument(
            id="benefits_cost_01",
            title="Benefits Cost Optimization Strategies",
            content="Benefits cost optimization involves analyzing plan utilization, negotiating with providers, and implementing wellness programs. Data-driven decisions help reduce expenses while maintaining employee satisfaction.",
            tags=["benefits", "cost", "optimization", "wellness"],
            weight=1.0
        ),
        SearchDocument(
            id="recruit_metrics_01",
            title="Recruiting Metrics Pipeline",
            content="Recruiting metrics track sourcing, screening, and hiring effectiveness. Key indicators include time-to-fill, quality-of-hire, and candidate experience scores for continuous improvement.",
            tags=["recruiting", "metrics", "pipeline", "hiring"],
            weight=1.0
        ),
        SearchDocument(
            id="engagement_01",
            title="Employee Engagement Measurement Tools",
            content="Employee engagement measurement uses surveys, pulse checks, and feedback platforms. Metrics such as Net Promoter Score (NPS) and engagement index inform retention and productivity strategies.",
            tags=["engagement", "measurement", "survey", "retention"],
            weight=1.0
        ),
        SearchDocument(
            id="title_vii_01",
            title="Title VII Discrimination Prevention",
            content="Title VII of the Civil Rights Act prohibits workplace discrimination based on race, color, religion, sex, or national origin. Employers must implement policies, training, and reporting mechanisms to ensure compliance.",
            tags=["title_vii", "discrimination", "compliance", "training"],
            weight=1.0
        ),
        SearchDocument(
            id="harassment_01",
            title="Workplace Harassment Prevention Program",
            content="Workplace harassment prevention includes policy development, training, and reporting procedures. Employers must foster a respectful culture and promptly address complaints to mitigate legal risks.",
            tags=["harassment", "prevention", "policy", "training"],
            weight=1.0
        ),
        SearchDocument(
            id="warn_act_01",
            title="WARN Act Compliance Checklist",
            content="The Worker Adjustment and Retraining Notification (WARN) Act requires employers to provide 60 days' notice before mass layoffs or plant closings. Compliance involves notification procedures and documentation.",
            tags=["warn_act", "compliance", "layoff", "notification"],
            weight=1.0
        ),
        SearchDocument(
            id="flight_risk_01",
            title="Flight Risk Assessment Models",
            content="Flight risk assessment uses predictive analytics to identify employees likely to leave. Factors include engagement scores, tenure, performance, and external market conditions.",
            tags=["flight_risk", "assessment", "analytics", "retention"],
            weight=1.0
        ),
        SearchDocument(
            id="org_design_01",
            title="Organizational Design Principles",
            content="Organizational design defines structure, roles, and reporting relationships. Principles include agility, scalability, and alignment with business strategy to optimize performance.",
            tags=["organizational_design", "structure", "agility", "strategy"],
            weight=1.0
        ),
        SearchDocument(
            id="learning_roi_01",
            title="Learning and Development ROI Measurement",
            content="Learning and development ROI measures training effectiveness through pre- and post-assessment, business impact, and cost-benefit analysis. Continuous improvement relies on data-driven insights.",
            tags=["learning", "development", "roi", "training"],
            weight=1.0
        ),
        SearchDocument(
            id="dei_01",
            title="DEI Strategy and Metrics",
            content="Diversity, Equity, and Inclusion (DEI) strategies focus on representation, belonging, and fairness. Metrics include demographic analysis, promotion rates, and inclusion surveys for accountability.",
            tags=["dei", "strategy", "metrics", "inclusion"],
            weight=1.0
        ),
        SearchDocument(
            id="hr_tech_01",
            title="HR Technology Selection Guide",
            content="HR technology selection involves requirements analysis, vendor evaluation, and implementation planning. Key considerations include scalability, integration, and user adoption.",
            tags=["hr_technology", "selection", "vendor", "integration"],
            weight=1.0
        ),
        SearchDocument(
            id="employee_rel_01",
            title="Employee Relations Investigation Process",
            content="Employee relations investigations address workplace complaints and conflicts. Steps include intake, fact-finding, documentation, and resolution to ensure fairness and compliance.",
            tags=["employee_relations", "investigation", "compliance", "resolution"],
            weight=1.0
        ),
        SearchDocument(
            id="total_rewards_01",
            title="Total Rewards Strategy Components",
            content="Total rewards strategy integrates compensation, benefits, recognition, and career development. Alignment with organizational goals enhances attraction, retention, and engagement.",
            tags=["total_rewards", "strategy", "compensation", "benefits"],
            weight=1.0
        ),
        SearchDocument(
            id="workforce_planning_01",
            title="Workforce Planning Methodology",
            content="Workforce planning aligns talent supply with business demand. Methodology includes forecasting, gap analysis, and action planning to ensure optimal staffing.",
            tags=["workforce_planning", "methodology", "forecasting", "talent"],
            weight=1.0
        ),
        SearchDocument(
            id="handbook_01",
            title="Employee Handbook Essentials",
            content="Employee handbook essentials cover policies, procedures, and expectations. Clear communication supports compliance, culture, and onboarding effectiveness.",
            tags=["handbook", "essentials", "policy", "onboarding"],
            weight=1.0
        ),
        SearchDocument(
            id="hr_analytics_01",
            title="HR Analytics Maturity Model",
            content="HR analytics maturity progresses from descriptive to predictive and prescriptive insights. Key capabilities include data integration, dashboarding, and advanced modeling.",
            tags=["hr_analytics", "maturity", "model", "data"],
            weight=1.0
        ),
        SearchDocument(
            id="shrm_comp_01",
            title="SHRM Competency Model Overview",
            content="The SHRM competency model outlines behavioral and technical competencies for HR professionals. Core areas include leadership, ethical practice, and business acumen.",
            tags=["shrm", "competency", "model", "hr"],
            weight=1.0
        ),
        SearchDocument(
            id="workers_comp_01",
            title="Workers' Compensation Management",
            content="Workers' compensation management covers claims processing, injury reporting, and return-to-work programs. Compliance with state regulations is essential.",
            tags=["workers_compensation", "management", "claims", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="remote_policy_01",
            title="Remote and Hybrid Work Policy Design",
            content="Remote and hybrid work policy addresses eligibility, technology, and performance management. Clear guidelines support flexibility and productivity.",
            tags=["remote", "hybrid", "policy", "work"],
            weight=1.0
        ),
        SearchDocument(
            id="okr_kpi_01",
            title="OKR and KPI Framework for HR",
            content="Objectives and Key Results (OKR) and Key Performance Indicators (KPI) frameworks drive HR goal alignment and measurement. Regular review ensures progress and accountability.",
            tags=["okr", "kpi", "framework", "hr"],
            weight=1.0
        ),
        SearchDocument(
            id="i9_verify_01",
            title="I-9 Employment Verification Process",
            content="I-9 employment verification ensures eligibility to work in the U.S. Employers must complete Form I-9, verify documents, and maintain records to comply with federal regulations.",
            tags=["i9", "verification", "employment", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="discipline_01",
            title="Progressive Discipline Framework",
            content="Progressive discipline framework includes verbal warnings, written notices, suspension, and termination. Consistent application supports fairness and legal compliance.",
            tags=["discipline", "framework", "compliance", "fairness"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)