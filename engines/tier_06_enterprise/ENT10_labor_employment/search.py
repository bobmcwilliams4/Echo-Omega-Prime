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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_norms: Dict[str, float] = {}
        self._preprocessed: bool = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            tf = Counter(tokens)
            for term, freq in tf.items():
                self.inverted_index[term][doc.id] = freq
            for term in tf:
                self.doc_freqs[term] += 1
            self.total_docs += 1
            self._preprocessed = False

    def _preprocess(self):
        with self.lock:
            if self._preprocessed:
                return
            if self.total_docs == 0:
                self.avg_doc_length = 0.0
            else:
                self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self._idf_cache.clear()
            self._tfidf_norms.clear()
            for term in self.inverted_index:
                self._idf_cache[term] = self._compute_idf(term)
            for doc_id, doc in self.documents.items():
                tf = self._get_doc_tf(doc_id)
                norm = 0.0
                for term, freq in tf.items():
                    idf = self._idf_cache.get(term, 0.0)
                    tfidf = (freq / self.doc_lengths[doc_id]) * idf
                    norm += tfidf ** 2
                self._tfidf_norms[doc_id] = math.sqrt(norm)
            self._preprocessed = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        self._preprocess()
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        # BM25 scoring
        bm25_scores = defaultdict(float)
        for term in query_terms:
            if term not in self.inverted_index:
                continue
            idf = self._idf_cache.get(term, 0.0)
            for doc_id, freq in self.inverted_index[term].items():
                doc_len = self.doc_lengths[doc_id]
                tf = freq
                score = self._score_bm25(tf, idf, doc_len)
                bm25_scores[doc_id] += score * self.documents[doc_id].weight
        # TF-IDF scoring
        tfidf_scores = defaultdict(float)
        query_tf = Counter(query_terms)
        query_norm = 0.0
        for term, freq in query_tf.items():
            idf = self._idf_cache.get(term, 0.0)
            tfidf = (freq / len(query_terms)) * idf
            query_norm += tfidf ** 2
        query_norm = math.sqrt(query_norm) if query_norm > 0 else 1.0
        for doc_id in self.documents:
            doc_tf = self._get_doc_tf(doc_id)
            doc_norm = self._tfidf_norms.get(doc_id, 1.0)
            score = 0.0
            for term in query_terms:
                if term in doc_tf:
                    idf = self._idf_cache.get(term, 0.0)
                    doc_tfidf = (doc_tf[term] / self.doc_lengths[doc_id]) * idf
                    query_tfidf = (query_tf[term] / len(query_terms)) * idf
                    score += doc_tfidf * query_tfidf
            if doc_norm > 0 and query_norm > 0:
                tfidf_scores[doc_id] = (score / (doc_norm * query_norm)) * self.documents[doc_id].weight
        # Combine scores (BM25 + TF-IDF, weighted)
        combined_scores = defaultdict(float)
        for doc_id in self.documents:
            combined_scores[doc_id] = 0.7 * bm25_scores.get(doc_id, 0.0) + 0.3 * tfidf_scores.get(doc_id, 0.0)
        # Rank and return results
        ranked = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        self._preprocess()
        return {
            "total_documents": self.total_docs,
            "total_terms": len(self.inverted_index),
            "avg_doc_length": int(self.avg_doc_length),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))

    def _score_bm25(self, tf: int, idf: float, doc_len: int) -> float:
        denom = tf + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * (doc_len / (self.avg_doc_length or 1)))
        return idf * ((tf * (self.bm25_k1 + 1)) / (denom + 1e-6))

    def _get_doc_tf(self, doc_id: str) -> Dict[str, int]:
        tf = {}
        for term in self.inverted_index:
            if doc_id in self.inverted_index[term]:
                tf[term] = self.inverted_index[term][doc_id]
        return tf

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + '...' if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + '...'

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
            id="1",
            title="FLSA Overtime Exemption - Executive Duties",
            content="To qualify for the executive exemption under the Fair Labor Standards Act (FLSA), an employee must primarily manage the enterprise or a recognized department, regularly direct at least two full-time employees, and have authority over hiring or firing. Salary basis and minimum salary threshold also apply.",
            tags=["FLSA", "Overtime", "Executive Exemption"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="FMLA Eligibility Requirements",
            content="The Family and Medical Leave Act (FMLA) provides eligible employees up to 12 weeks of unpaid leave. Eligibility requires 12 months of employment, 1,250 hours worked in the preceding year, and employment at a location with 50 or more employees within 75 miles.",
            tags=["FMLA", "Eligibility"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="FMLA Entitlement and Job Protection",
            content="FMLA entitles eligible employees to job-protected leave for specified family and medical reasons. Upon return, employees must be restored to the same or an equivalent position with equivalent pay, benefits, and terms of employment.",
            tags=["FMLA", "Entitlement", "Job Protection"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="ADA Reasonable Accommodation - Interactive Process",
            content="The ADA requires employers to engage in an interactive process with employees requesting reasonable accommodation for disabilities. This process involves dialogue to identify limitations and potential accommodations, and is an ongoing obligation.",
            tags=["ADA", "Reasonable Accommodation", "Interactive Process"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Title VII Disparate Treatment - McDonnell Douglas Framework",
            content="In disparate treatment claims under Title VII, courts apply the McDonnell Douglas burden-shifting framework: (1) plaintiff establishes a prima facie case; (2) employer articulates a legitimate, nondiscriminatory reason; (3) plaintiff shows pretext.",
            tags=["Title VII", "Disparate Treatment", "McDonnell Douglas"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Title VII Disparate Impact - Statistical Evidence",
            content="Disparate impact claims under Title VII focus on facially neutral policies that disproportionately affect protected groups. Plaintiffs must identify a specific practice and show statistical disparity; employers can defend by showing business necessity.",
            tags=["Title VII", "Disparate Impact"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="ADEA Age Discrimination - Protected Class",
            content="The Age Discrimination in Employment Act (ADEA) prohibits discrimination against employees aged 40 and over. Plaintiffs must show adverse action was taken because of age; mixed-motive claims are not permitted.",
            tags=["ADEA", "Age Discrimination"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="WARN Act - Mass Layoff Notification Requirements",
            content="The WARN Act requires employers with 100 or more employees to provide 60 days' advance written notice of plant closings or mass layoffs affecting 50 or more employees at a single site of employment.",
            tags=["WARN Act", "Mass Layoff", "Notification"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="NLRA Section 7 - Protected Concerted Activity",
            content="Section 7 of the National Labor Relations Act (NLRA) protects employees' rights to engage in concerted activities for mutual aid or protection, including discussing wages and working conditions, regardless of union status.",
            tags=["NLRA", "Section 7", "Protected Activity"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="ERISA Fiduciary Duty - Retirement Plan Management",
            content="ERISA imposes strict fiduciary duties on those managing retirement plans, including the duty of loyalty, prudence, diversification, and adherence to plan documents. Fiduciaries must act solely in the interest of plan participants.",
            tags=["ERISA", "Fiduciary Duty", "Retirement Plan"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Non-Compete Agreement - Reasonableness Factors",
            content="A non-compete agreement is enforceable if it is reasonable in duration, geographic scope, and protects legitimate business interests. Overbroad restrictions may be invalidated by courts.",
            tags=["Non-Compete", "Reasonableness"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Trade Secrets - DTSA and State UTSA",
            content="The Defend Trade Secrets Act (DTSA) and Uniform Trade Secrets Act (UTSA) provide civil remedies for misappropriation of trade secrets, defined as information that derives independent economic value from not being generally known.",
            tags=["Trade Secrets", "DTSA", "UTSA"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Independent Contractor vs Employee - ABC Test",
            content="The ABC test presumes worker is an employee unless (A) free from control, (B) work outside usual business, and (C) customarily engaged in independent trade. Used in wage and hour and unemployment contexts.",
            tags=["Independent Contractor", "ABC Test"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="Independent Contractor vs Employee - Economic Reality Test",
            content="The economic reality test considers factors such as degree of control, opportunity for profit or loss, investment in equipment, permanency, and skill required to determine worker status under the FLSA.",
            tags=["Independent Contractor", "Economic Reality"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="At-Will Employment - Exceptions to Terminability",
            content="At-will employment allows termination for any reason not prohibited by law. Exceptions include public policy, implied contract, and covenant of good faith. Statutory protections may also apply.",
            tags=["At-Will Employment", "Exceptions"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Employee Handbook - Contractual Effect and Disclaimers",
            content="Employee handbooks may create enforceable contractual rights unless they include clear disclaimers stating the handbook is not a contract and employment is at-will.",
            tags=["Employee Handbook", "Contractual Effect", "Disclaimers"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="FLSA Salary Basis Test for Exempt Employees",
            content="To be exempt from FLSA overtime, employees must be paid on a salary basis at not less than the minimum threshold. Deductions from salary may jeopardize exemption status.",
            tags=["FLSA", "Salary Basis", "Exempt Employees"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="FMLA Covered Employers",
            content="Covered employers under FMLA include private-sector employers with 50 or more employees, public agencies, and public or private elementary or secondary schools.",
            tags=["FMLA", "Covered Employer"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="ADA - Essential Job Functions",
            content="Reasonable accommodation under the ADA does not require elimination of essential job functions. Employers may require employees to perform essential functions with or without accommodation.",
            tags=["ADA", "Essential Functions"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="Title VII - Retaliation Protection",
            content="Title VII prohibits retaliation against employees who oppose discrimination, file a charge, or participate in an investigation or proceeding.",
            tags=["Title VII", "Retaliation"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="ADEA - Bona Fide Occupational Qualification (BFOQ)",
            content="ADEA allows age to be a bona fide occupational qualification only where age is reasonably necessary to the normal operation of the particular business.",
            tags=["ADEA", "BFOQ"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="WARN Act - Exceptions to Notice Requirement",
            content="The WARN Act notice requirement does not apply in cases of faltering company, unforeseeable business circumstances, or natural disaster, but employers must provide as much notice as practicable.",
            tags=["WARN Act", "Exceptions"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="NLRA - Weingarten Rights",
            content="Employees have the right to union representation during investigatory interviews that may lead to discipline, known as Weingarten rights, under the NLRA.",
            tags=["NLRA", "Weingarten Rights"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="ERISA - Prohibited Transactions",
            content="ERISA prohibits fiduciaries from engaging in transactions that present conflicts of interest, including self-dealing and certain transactions with parties in interest.",
            tags=["ERISA", "Prohibited Transactions"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Non-Compete - Blue Pencil Doctrine",
            content="Some states permit courts to modify overbroad non-compete agreements to make them reasonable, a practice known as the blue pencil doctrine.",
            tags=["Non-Compete", "Blue Pencil"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Trade Secrets - Reasonable Measures to Protect",
            content="To qualify as a trade secret under DTSA or UTSA, the owner must take reasonable measures to keep the information secret, such as confidentiality agreements and restricted access.",
            tags=["Trade Secrets", "Protection Measures"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Independent Contractor - IRS 20-Factor Test",
            content="The IRS 20-factor test evaluates behavioral and financial control, relationship of the parties, and other factors to determine worker classification for tax purposes.",
            tags=["Independent Contractor", "IRS Test"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="At-Will Employment - Public Policy Exception",
            content="The public policy exception to at-will employment prohibits termination for reasons that violate a well-established public policy, such as refusing to commit an illegal act.",
            tags=["At-Will Employment", "Public Policy"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Employee Handbook - Implied Contract",
            content="An employee handbook may create an implied contract if it contains specific promises regarding job security or disciplinary procedures, absent a clear disclaimer.",
            tags=["Employee Handbook", "Implied Contract"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="FLSA Administrative Exemption",
            content="The administrative exemption under the FLSA applies to employees whose primary duty is office or non-manual work related to management or general business operations, and who exercise discretion and independent judgment.",
            tags=["FLSA", "Administrative Exemption"],
            weight=1.0
        ),
        SearchDocument(
            id="31",
            title="FMLA - Serious Health Condition Definition",
            content="A serious health condition under FMLA is an illness, injury, impairment, or physical or mental condition that involves inpatient care or continuing treatment by a health care provider.",
            tags=["FMLA", "Serious Health Condition"],
            weight=1.0
        ),
        SearchDocument(
            id="32",
            title="ADA - Undue Hardship Defense",
            content="An employer may deny a requested accommodation under the ADA if it would impose an undue hardship, defined as significant difficulty or expense in light of the employer's resources and business needs.",
            tags=["ADA", "Undue Hardship"],
            weight=1.0
        ),
        SearchDocument(
            id="33",
            title="Title VII - Hostile Work Environment",
            content="A hostile work environment under Title VII exists when discriminatory conduct is severe or pervasive enough to create an abusive working environment for a reasonable person.",
            tags=["Title VII", "Hostile Work Environment"],
            weight=1.0
        ),
        SearchDocument(
            id="34",
            title="ADEA - Waiver of Rights",
            content="A waiver of rights under the ADEA must be knowing and voluntary, in writing, and meet specific statutory requirements, including a 21-day consideration period and 7-day revocation period.",
            tags=["ADEA", "Waiver"],
            weight=1.0
        ),
        SearchDocument(
            id="35",
            title="WARN Act - Calculation of Employees",
            content="For WARN Act coverage, part-time employees are excluded from the count of employees, and layoffs must meet threshold numbers within a 30-day period.",
            tags=["WARN Act", "Employee Calculation"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)