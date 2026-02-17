import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_tokens: Dict[int, List[str]] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}
        self._recompute_stats()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freqs[term] += 1
            self.N += 1
            self._recompute_stats()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            if score > 0:
                doc_scores[doc_id] = score * doc.weight
        top_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "documents": self.N,
                "avgdl": self.avgdl,
                "unique_terms": len(self.term_doc_freqs)
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
        doc_len = self.doc_lengths.get(doc_id, 0)
        tf = self.term_freqs.get(doc_id, Counter())
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / (self.avgdl or 1))
            score += idf * freq * (self.k1 + 1) / (denom or 1)
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 0)
        for term in query_terms:
            tf_norm = tf[term] / (doc_len or 1)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], size: int = 180) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if positions:
            start = max(min(positions) - 30, 0)
            end = min(start + size, len(content))
            snippet = content[start:end]
        else:
            snippet = content[:size]
        for term in set(query_terms):
            snippet = re.sub(r'(?i)(' + re.escape(term) + r')', r'**\1**', snippet)
        return snippet.strip()

    def _recompute_stats(self):
        total_len = sum(self.doc_lengths.values())
        self.avgdl = (total_len / self.N) if self.N > 0 else 0.0
        self._idf_cache.clear()
        self._tfidf_cache.clear()

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seeded Domain Documents ---

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Texas Incapacity Standard Definition",
            "Under Texas law, incapacity means an adult is substantially unable to provide food, clothing, or shelter, to care for their own physical health, or to manage their own financial affairs due to a physical or mental condition.",
            ["incapacity", "definition", "texas"]
        ),
        SearchDocument(
            2,
            "Least Restrictive Alternative Requirement",
            "Before appointing a guardian, Texas courts must consider whether less restrictive alternatives to guardianship are available and feasible, such as powers of attorney or supported decision-making agreements.",
            ["least restrictive", "alternative", "requirement"]
        ),
        SearchDocument(
            3,
            "Guardian Qualification and Priority",
            "Texas law sets out qualifications for guardians, including age, residency, and absence of disqualifying criminal history. Priority is given to certain relatives, but the court may appoint another if in the ward's best interest.",
            ["guardian", "qualification", "priority"]
        ),
        SearchDocument(
            4,
            "Guardian of Person: Duties and Powers",
            "A guardian of the person in Texas is responsible for the ward's care, supervision, and protection, including determining residence, consenting to medical care, and ensuring personal needs are met.",
            ["guardian", "person", "duties", "powers"]
        ),
        SearchDocument(
            5,
            "Guardian of Estate: Financial Duties",
            "A guardian of the estate manages the ward's property, pays debts, collects income, and must prudently invest assets. Court approval is required for certain transactions.",
            ["guardian", "estate", "financial", "duties"]
        ),
        SearchDocument(
            6,
            "Annual Report and Accounting Requirements",
            "Guardians must file annual reports on the ward's well-being and a detailed accounting of estate assets, income, and expenditures with the Texas court.",
            ["annual", "report", "accounting", "requirements"]
        ),
        SearchDocument(
            7,
            "Guardian Ad Litem: Role and Duties",
            "A guardian ad litem is appointed by the court to represent the ward's best interests during guardianship proceedings, independent of all parties.",
            ["guardian ad litem", "role", "duties"]
        ),
        SearchDocument(
            8,
            "Temporary Guardianship and Emergency Appointment",
            "Texas courts may appoint a temporary guardian without notice if there is substantial evidence of imminent danger to the ward's health or estate.",
            ["temporary guardianship", "emergency", "appointment"]
        ),
        SearchDocument(
            9,
            "Removal of Guardian for Cause",
            "A guardian may be removed for cause, including mismanagement, neglect, incapacity, or failure to comply with court orders, to protect the ward.",
            ["removal", "guardian", "cause"]
        ),
        SearchDocument(
            10,
            "Ward Rights and Due Process Protections",
            "Wards are entitled to notice, representation, and a hearing before guardianship is imposed. They have the right to attend hearings and appeal decisions.",
            ["ward", "rights", "due process"]
        ),
        SearchDocument(
            11,
            "Modification and Restoration of Capacity",
            "Guardianship orders may be modified or terminated if the ward's capacity is restored. The ward or interested party may petition for restoration at any time.",
            ["modification", "restoration", "capacity"]
        ),
        SearchDocument(
            12,
            "Minor Guardianship Distinctions",
            "Guardianship of minors in Texas differs from adult guardianship, with parents having priority and the court focusing on the child's best interests.",
            ["minor", "guardianship", "distinctions"]
        ),
        SearchDocument(
            13,
            "Guardian Bond Requirements and Waiver",
            "A guardian must typically post a bond to protect the ward's estate. The court may waive the bond requirement in certain circumstances.",
            ["guardian", "bond", "requirements", "waiver"]
        ),
        SearchDocument(
            14,
            "Guardianship Venue and Jurisdiction",
            "Venue for guardianship proceedings is generally in the county where the proposed ward resides or is located. Texas courts have exclusive jurisdiction.",
            ["guardianship", "venue", "jurisdiction"]
        ),
        SearchDocument(
            15,
            "Supported Decision-Making Agreement Alternative",
            "Supported decision-making agreements allow adults with disabilities to make their own decisions with assistance, serving as a less restrictive alternative to guardianship.",
            ["supported decision-making", "agreement", "alternative"]
        ),
        SearchDocument(
            16,
            "Interstate Transfer of Guardianship",
            "Texas recognizes and provides procedures for transferring guardianship to and from other states to facilitate continuity of care for the ward.",
            ["interstate", "transfer", "guardianship"]
        ),
        SearchDocument(
            17,
            "Guardian Compensation and Expenses",
            "Guardians may be compensated for their services and reimbursed for reasonable expenses, subject to court approval and statutory limits.",
            ["guardian", "compensation", "expenses"]
        ),
        SearchDocument(
            18,
            "Medical Consent and Treatment Decisions",
            "A guardian of the person may consent to medical and psychiatric treatment for the ward, except for certain procedures that require specific court approval.",
            ["medical consent", "treatment", "decisions"]
        ),
        SearchDocument(
            19,
            "Guardian Duty to Avoid Conflicts of Interest",
            "Guardians must act in the ward's best interest and avoid self-dealing or conflicts of interest. The court may remove a guardian for breach of fiduciary duty.",
            ["guardian", "duty", "conflicts of interest"]
        ),
        SearchDocument(
            20,
            "Limited Guardianship Tailored to Individual Needs",
            "Texas law encourages limited guardianships, granting only those powers necessary to protect the ward and preserving as much autonomy as possible.",
            ["limited guardianship", "individual needs"]
        ),
        SearchDocument(
            21,
            "Powers of Attorney as Guardianship Alternative",
            "A durable power of attorney or medical power of attorney may eliminate the need for guardianship if the principal's needs are met through these alternatives.",
            ["powers of attorney", "guardianship", "alternative"]
        ),
        SearchDocument(
            22,
            "Guardianship of Veterans and VA Benefits",
            "Special rules apply to guardianships involving veterans or those receiving VA benefits, including appointment of a fiduciary approved by the Department of Veterans Affairs.",
            ["guardianship", "veterans", "va benefits"]
        ),
        SearchDocument(
            23,
            "Appointment of Corporate or Professional Guardians",
            "Texas courts may appoint a corporate or professional guardian if no qualified family member is available or appropriate.",
            ["appointment", "corporate guardian", "professional guardian"]
        ),
        SearchDocument(
            24,
            "Guardian's Authority Over Ward's Residence",
            "A guardian of the person may determine the ward's residence, but must seek court approval for placement in certain facilities.",
            ["guardian", "authority", "residence", "living situation"]
        ),
        SearchDocument(
            25,
            "Emergency Orders and Immediate Protection",
            "Courts may issue emergency orders to protect the ward or estate pending a full guardianship hearing, including temporary restraining orders.",
            ["emergency", "orders", "immediate protection"]
        ),
        SearchDocument(
            26,
            "Guardian Liability for Negligence or Misconduct",
            "A guardian may be held personally liable for losses to the ward's estate caused by negligence, fraud, or misconduct in the performance of their duties.",
            ["guardian", "liability", "negligence", "misconduct"]
        ),
        SearchDocument(
            27,
            "Notice and Service Requirements in Guardianship",
            "Texas law requires notice of guardianship proceedings to the proposed ward and interested parties, with strict service requirements to ensure due process.",
            ["notice", "service", "requirements", "guardianship"]
        ),
        SearchDocument(
            28,
            "Court Visitor Program in Guardianship",
            "The court may appoint a court visitor to investigate the circumstances of the proposed ward and report findings to assist the court in determining incapacity.",
            ["court visitor", "guardianship", "investigation"]
        ),
        SearchDocument(
            29,
            "Restoration of Rights and Termination of Guardianship",
            "If a ward regains capacity, the court may restore rights and terminate the guardianship. The process includes medical evidence and a hearing.",
            ["restoration", "rights", "termination", "guardianship"]
        ),
        SearchDocument(
            30,
            "Guardian's Duty to Encourage Independence",
            "A guardian must encourage the ward to participate in decisions and develop or regain capacity to the extent possible.",
            ["guardian", "duty", "independence"]
        ),
    ]
    for doc in docs:
        idx.add_document(doc)