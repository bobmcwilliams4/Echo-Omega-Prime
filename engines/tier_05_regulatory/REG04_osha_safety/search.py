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
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self.idf_cache: Dict[str, float] = {}
        self._recompute_stats = True

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

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
                self.doc_freqs[term] += 1
            self.total_docs += 1
            self._recompute_stats = True

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            if doc_id not in self.inverted_index.get(term, {}):
                continue
            tf = self.inverted_index[term][doc_id]
            idf = self._compute_idf(term)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            term_score = idf * (tf * (self.k1 + 1)) / denom
            score += term_score
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf_counter = Counter(self._tokenize(doc.content))
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            df = self.doc_freqs.get(term, 0)
            if df == 0:
                continue
            idf = math.log((self.total_docs + 1) / (df + 1)) + 1
            score += tf_norm * idf
        return score * doc.weight

    def _update_stats(self):
        if not self._recompute_stats:
            return
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.total_docs if self.total_docs > 0 else 0.0
        self.idf_cache.clear()
        self._recompute_stats = False

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        self._update_stats()
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored_results: List[Tuple[str, float]] = []
        for doc_id in candidate_docs:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0:
                scored_results.append((doc_id, score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], maxlen: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:maxlen] + '...' if len(content) > maxlen else content
        start = max(positions[0] - 5, 0)
        end = min(start + 30, len(tokens))
        snippet = ' '.join(tokens[start:end])
        for term in query_terms:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:maxlen] + '...' if len(snippet) > maxlen else snippet

    def get_stats(self) -> Dict[str, float]:
        self._update_stats()
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.doc_freqs),
        }

# Singleton factory
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
            "General Duty Clause 5(a)(1) Overview",
            "The General Duty Clause, Section 5(a)(1) of the OSH Act, requires employers to provide a workplace free from recognized hazards likely to cause death or serious physical harm.",
            ["general duty clause", "osha", "section 5(a)(1)"],
            1.0
        ),
        SearchDocument(
            "2",
            "PSM 29 CFR 1910.119 Covered Processes Thresholds",
            "Process Safety Management (PSM) applies to processes involving threshold quantities of highly hazardous chemicals as listed in Appendix A of 29 CFR 1910.119.",
            ["psm", "process safety management", "1910.119", "threshold"],
            1.0
        ),
        SearchDocument(
            "3",
            "Lockout/Tagout 1910.147 Energy Control Procedures",
            "Employers must establish energy control procedures under 29 CFR 1910.147 to ensure machines are properly shut off and not started up again before maintenance is complete.",
            ["lockout", "tagout", "energy control", "1910.147"],
            1.0
        ),
        SearchDocument(
            "4",
            "Confined Space Entry 1910.146 Permit System",
            "Permit-required confined spaces must be identified and a written program implemented as per 29 CFR 1910.146, including entry permits and atmospheric testing.",
            ["confined space", "permit", "1910.146"],
            1.0
        ),
        SearchDocument(
            "5",
            "Fall Protection 1926.501 Construction Standards",
            "1926.501 requires employers to provide fall protection systems for employees working at heights in construction, including guardrails, safety nets, or personal fall arrest systems.",
            ["fall protection", "1926.501", "construction"],
            1.0
        ),
        SearchDocument(
            "6",
            "HazCom 2012 GHS SDS and Labeling Requirements",
            "The Hazard Communication Standard (HazCom 2012) requires chemical manufacturers to provide Safety Data Sheets (SDS) and labels in accordance with the Globally Harmonized System (GHS).",
            ["hazcom", "ghs", "sds", "labeling"],
            1.0
        ),
        SearchDocument(
            "7",
            "OSHA 300 Log Recordkeeping Requirements",
            "Employers must record work-related injuries and illnesses on the OSHA 300 Log, as required by 29 CFR 1904, including criteria for recordability and retention.",
            ["osha 300", "recordkeeping", "injury", "illness"],
            1.0
        ),
        SearchDocument(
            "8",
            "OSHA Citation Classifications and Penalty Calculations",
            "OSHA citations are classified as serious, other-than-serious, willful, or repeat. Penalties are calculated based on gravity, size, history, and good faith.",
            ["citation", "penalty", "classification"],
            1.0
        ),
        SearchDocument(
            "9",
            "Multi-Employer Worksite Citation Policy",
            "OSHA's multi-employer worksite policy holds multiple employers responsible for hazards, including creating, exposing, correcting, and controlling employers.",
            ["multi-employer", "worksite", "policy"],
            1.0
        ),
        SearchDocument(
            "10",
            "Abatement Requirements and Verification",
            "Employers must abate cited hazards by the abatement date and provide verification to OSHA, including abatement certification and documentation.",
            ["abatement", "verification", "osha"],
            1.0
        ),
        SearchDocument(
            "11",
            "Whistleblower Retaliation Section 11(c) Protection",
            "Section 11(c) of the OSH Act prohibits employers from retaliating against employees who exercise their safety and health rights, including filing complaints.",
            ["whistleblower", "retaliation", "section 11(c)"],
            1.0
        ),
        SearchDocument(
            "12",
            "Recognized Hazards under the General Duty Clause",
            "A recognized hazard is one that is known to be hazardous in the industry or by the employer. The General Duty Clause applies only to recognized hazards.",
            ["general duty clause", "recognized hazard"],
            1.0
        ),
        SearchDocument(
            "13",
            "Elements of a Valid Energy Control Procedure",
            "A valid energy control procedure must include steps for shutting down, isolating, blocking, and securing machines, as well as verifying zero energy state.",
            ["lockout", "tagout", "energy control", "procedure"],
            1.0
        ),
        SearchDocument(
            "14",
            "Permit-Required Confined Space Entry Steps",
            "Entry into permit-required confined spaces requires atmospheric testing, entry permits, attendant, and rescue procedures, per 1910.146.",
            ["confined space", "permit", "entry", "1910.146"],
            1.0
        ),
        SearchDocument(
            "15",
            "Threshold Quantities for PSM Coverage",
            "Appendix A of 1910.119 lists threshold quantities for highly hazardous chemicals, such as 10,000 pounds for flammable liquids and 5,000 pounds for ammonia.",
            ["psm", "threshold", "highly hazardous chemical"],
            1.0
        ),
        SearchDocument(
            "16",
            "Fall Protection Systems and Criteria",
            "Acceptable fall protection systems include guardrails, safety nets, and personal fall arrest systems. Each system must meet criteria in 1926.502.",
            ["fall protection", "system", "criteria"],
            1.0
        ),
        SearchDocument(
            "17",
            "GHS Label Elements under HazCom 2012",
            "GHS labels must include product identifier, signal word, hazard statement, pictogram, precautionary statement, and supplier information.",
            ["ghs", "label", "hazcom"],
            1.0
        ),
        SearchDocument(
            "18",
            "OSHA 300 Log: Recordable Cases",
            "A recordable case is a work-related injury or illness that results in death, days away from work, restricted work, transfer, medical treatment, or loss of consciousness.",
            ["osha 300", "recordable", "injury", "illness"],
            1.0
        ),
        SearchDocument(
            "19",
            "Serious vs. Willful OSHA Citation",
            "A serious violation exists when there is a substantial probability of death or serious harm. Willful violations are committed with intentional disregard or plain indifference.",
            ["citation", "serious", "willful"],
            1.0
        ),
        SearchDocument(
            "20",
            "Employer Roles on Multi-Employer Worksites",
            "On multi-employer worksites, the creating, exposing, correcting, and controlling employers may all be cited depending on their role in the hazard.",
            ["multi-employer", "roles", "worksite"],
            1.0
        ),
        SearchDocument(
            "21",
            "Abatement Verification Documentation",
            "Employers must submit abatement certification and, in some cases, abatement documentation such as photos, receipts, or other proof to OSHA.",
            ["abatement", "documentation", "verification"],
            1.0
        ),
        SearchDocument(
            "22",
            "Filing a Whistleblower Complaint",
            "Employees must file a whistleblower complaint within 30 days of alleged retaliation under Section 11(c) of the OSH Act.",
            ["whistleblower", "complaint", "section 11(c)"],
            1.0
        ),
        SearchDocument(
            "23",
            "Hazard Communication Program Requirements",
            "Employers must have a written hazard communication program, maintain SDSs, ensure proper labeling, and train employees on chemical hazards.",
            ["hazcom", "program", "sds", "labeling"],
            1.0
        ),
        SearchDocument(
            "24",
            "Energy Control Procedure Annual Review",
            "Employers must review energy control procedures annually to ensure effectiveness and correct any deficiencies.",
            ["lockout", "tagout", "energy control", "review"],
            1.0
        ),
        SearchDocument(
            "25",
            "Permit System for Confined Spaces",
            "A permit system must specify the space to be entered, purpose, date, authorized entrants, attendants, and entry supervisor.",
            ["confined space", "permit", "system"],
            1.0
        ),
        SearchDocument(
            "26",
            "Fall Hazards in Construction",
            "Common fall hazards in construction include unprotected edges, floor holes, and improper scaffold use. 1926.501 addresses these hazards.",
            ["fall hazard", "construction", "1926.501"],
            1.0
        ),
        SearchDocument(
            "27",
            "SDS Sections Required by HazCom 2012",
            "Safety Data Sheets must contain 16 sections, including identification, hazard(s), composition, first-aid, firefighting, and more.",
            ["sds", "hazcom", "sections"],
            1.0
        ),
        SearchDocument(
            "28",
            "OSHA 300 Log Retention Period",
            "OSHA 300 Logs must be retained for at least five years following the end of the calendar year that the records cover.",
            ["osha 300", "retention", "recordkeeping"],
            1.0
        ),
        SearchDocument(
            "29",
            "Penalty Adjustments for OSHA Citations",
            "OSHA may adjust penalties for size, history, and good faith. Maximum penalties are set by law and adjusted for inflation.",
            ["penalty", "adjustment", "citation"],
            1.0
        ),
        SearchDocument(
            "30",
            "Correcting Hazards on Multi-Employer Worksites",
            "Correcting employers are responsible for correcting hazards even if they did not create or expose employees to the hazard.",
            ["multi-employer", "correcting", "worksite"],
            1.0
        ),
        SearchDocument(
            "31",
            "Abatement Certification Requirements",
            "Abatement certification must be signed by an employer representative and submitted to OSHA when required.",
            ["abatement", "certification", "osha"],
            1.0
        ),
        SearchDocument(
            "32",
            "Prohibited Retaliation under Section 11(c)",
            "Prohibited retaliation includes firing, demotion, denial of overtime, or reduction in pay for reporting safety concerns.",
            ["whistleblower", "retaliation", "section 11(c)"],
            1.0
        ),
        SearchDocument(
            "33",
            "Process Hazard Analysis in PSM",
            "A process hazard analysis (PHA) is required for processes covered by PSM to identify, evaluate, and control hazards.",
            ["psm", "process hazard analysis", "pha"],
            1.0
        ),
        SearchDocument(
            "34",
            "Training Requirements for Lockout/Tagout",
            "Employees must be trained in the purpose and function of the energy control program and procedures for lockout/tagout.",
            ["lockout", "tagout", "training"],
            1.0
        ),
        SearchDocument(
            "35",
            "Entry Supervisor Duties in Confined Space Entry",
            "The entry supervisor must verify permit completion, test results, and that rescue services are available before entry.",
            ["confined space", "entry supervisor", "permit"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)