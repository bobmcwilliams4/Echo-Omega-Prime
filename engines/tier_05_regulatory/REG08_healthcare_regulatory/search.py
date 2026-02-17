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
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.term_df: Dict[str, int] = defaultdict(int)
        self.N: int = 0
        self.avgdl: float = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            token_counts = Counter(tokens)
            for token, freq in token_counts.items():
                self.term_doc_freqs[token][doc.id] = freq
                self.term_df[token] += 1
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self.term_doc_freqs.get(token, {}).keys())
        scored_results: List[Tuple[str, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc = self.documents[doc_id]
            final_score = bm25_score * 0.7 + tfidf_score * 0.3
            final_score *= doc.weight
            scored_results.append((doc_id, final_score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        return {
            "num_documents": self.N,
            "num_terms": len(self.term_df),
            "avg_doc_length": int(self.avgdl),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_df.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        for term in set(query_tokens):
            tf = self.term_doc_freqs.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
            score += idf * (tf * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: str, query_tokens: List[str]) -> float:
        tfidf = 0.0
        doc_len = self.doc_lengths[doc_id]
        token_counts = Counter(self.doc_tokens[doc_id])
        for term in set(query_tokens):
            tf = token_counts.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            tfidf += tf_norm * idf
        return tfidf

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        content_tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(content_tokens) if t in query_tokens]
        if not positions:
            snippet = content[:200]
            if len(content) > 200:
                snippet += "..."
            return snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(content_tokens))
        snippet_tokens = content_tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + ("..." if end < len(content_tokens) else "")

_index_instance: Optional[SearchIndex] = None
_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _index_instance
    if _index_instance is None:
        with _index_lock:
            if _index_instance is None:
                _index_instance = SearchIndex()
                _seed_documents(_index_instance)
    return _index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="1",
            title="HIPAA Privacy Rule: Protected Health Information",
            content="The HIPAA Privacy Rule establishes national standards to protect individuals' medical records and other personal health information. It applies to health plans, healthcare clearinghouses, and healthcare providers that conduct certain healthcare transactions electronically. Protected Health Information (PHI) includes any individually identifiable health information.",
            tags=["HIPAA", "Privacy", "PHI", "Protected Health Information"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="HIPAA Security Rule: Technical Safeguards",
            content="The HIPAA Security Rule requires covered entities to implement technical safeguards to protect electronic protected health information (ePHI). These include access controls, audit controls, integrity controls, authentication, and transmission security.",
            tags=["HIPAA", "Security", "Technical Safeguards", "ePHI"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Stark Law: Physician Self-Referral Prohibition",
            content="The Stark Law prohibits physicians from referring Medicare or Medicaid patients to entities with which they have a financial relationship for certain designated health services, unless an exception applies.",
            tags=["Stark Law", "Self-Referral", "Medicare", "Medicaid"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Anti-Kickback Statute: Remuneration for Referrals",
            content="The Anti-Kickback Statute makes it a criminal offense to knowingly and willfully offer, pay, solicit, or receive any remuneration to induce or reward referrals of items or services reimbursable by federal healthcare programs.",
            tags=["Anti-Kickback", "Remuneration", "Referrals", "Healthcare Fraud"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="False Claims Act: Healthcare Fraud",
            content="The False Claims Act imposes liability on individuals and companies who defraud governmental programs. It is the government's primary tool in combating healthcare fraud and abuse.",
            tags=["False Claims Act", "Healthcare Fraud", "Government Programs"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Medicare Conditions of Participation: Hospital Requirements",
            content="Hospitals must meet Medicare Conditions of Participation to receive program payments. Requirements include patient rights, quality assessment, infection control, and medical staff qualifications.",
            tags=["Medicare", "Conditions of Participation", "Hospital", "Requirements"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="EMTALA: Emergency Medical Treatment and Labor Act",
            content="EMTALA requires hospitals to provide emergency medical screening and stabilizing treatment to all patients, regardless of their ability to pay, and prohibits patient dumping.",
            tags=["EMTALA", "Emergency", "Medical Treatment", "Patient Rights"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="340B Drug Pricing Program",
            content="The 340B Drug Pricing Program enables eligible healthcare organizations to purchase outpatient drugs at significantly reduced prices, improving access to medications for vulnerable populations.",
            tags=["340B", "Drug Pricing", "Healthcare", "Access"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="FDA Drug Approval: New Drug Application",
            content="A New Drug Application (NDA) is submitted to the FDA to obtain approval to market a new pharmaceutical for sale in the United States. The NDA must include data on safety, efficacy, labeling, and manufacturing.",
            tags=["FDA", "Drug Approval", "NDA", "Pharmaceutical"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="DEA Controlled Substances: Schedule Classification",
            content="The DEA classifies controlled substances into five schedules based on their potential for abuse, accepted medical use, and safety. Schedule I drugs have no accepted medical use and high abuse potential.",
            tags=["DEA", "Controlled Substances", "Schedule", "Drug Enforcement"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Telehealth: Interstate Licensure",
            content="Telehealth providers must comply with state licensure laws when delivering care across state lines. The Interstate Medical Licensure Compact facilitates multistate practice for eligible physicians.",
            tags=["Telehealth", "Licensure", "Interstate", "Medical Practice"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Medicaid Managed Care: Network Adequacy",
            content="Medicaid managed care organizations must maintain a network of providers sufficient to ensure that all covered services are available and accessible to enrollees within reasonable time and distance standards.",
            tags=["Medicaid", "Managed Care", "Network Adequacy", "Access"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="State Medical Board: Scope of Practice",
            content="State medical boards define the scope of practice for healthcare professionals, including physicians, nurses, and allied health providers, to ensure safe and competent care.",
            tags=["State Medical Board", "Scope of Practice", "Licensure"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="HIPAA Breach Notification",
            content="HIPAA requires covered entities and business associates to notify affected individuals, the Secretary of HHS, and sometimes the media, following a breach of unsecured protected health information.",
            tags=["HIPAA", "Breach Notification", "PHI", "Security"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Medicare Part D: Medication Therapy Management",
            content="Medicare Part D plans must offer Medication Therapy Management (MTM) programs to eligible beneficiaries to optimize therapeutic outcomes and reduce adverse events.",
            tags=["Medicare Part D", "Medication Therapy Management", "MTM"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Clinical Laboratory Improvement Amendments (CLIA)",
            content="CLIA regulations establish quality standards for laboratory testing to ensure the accuracy, reliability, and timeliness of patient test results regardless of where the test is performed.",
            tags=["CLIA", "Laboratory", "Quality Standards", "Testing"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="FDA Medical Device Classification",
            content="The FDA classifies medical devices into Class I, II, or III based on the level of control necessary to assure safety and effectiveness. Class III devices require the most stringent regulatory controls.",
            tags=["FDA", "Medical Device", "Classification", "Regulation"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="HIPAA Business Associate Agreements",
            content="Covered entities must have Business Associate Agreements (BAAs) with vendors or contractors who handle protected health information on their behalf, outlining each party's responsibilities.",
            tags=["HIPAA", "Business Associate Agreement", "BAA", "PHI"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Medicare Physician Fee Schedule: Physician Self-Referral",
            content="The Medicare Physician Fee Schedule includes rules to prevent physician self-referral for certain designated health services, consistent with the Stark Law.",
            tags=["Medicare", "Physician Fee Schedule", "Self-Referral", "Stark Law"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="State Certificate of Need Laws",
            content="Certificate of Need (CON) laws require healthcare providers to obtain state approval before offering certain new or expanded services, aiming to control healthcare costs and avoid duplication.",
            tags=["State", "Certificate of Need", "CON", "Healthcare Planning"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="FDA Dietary Supplement Regulation",
            content="The FDA regulates dietary supplements under a different set of regulations than those covering conventional foods and drug products. Manufacturers are responsible for ensuring their products are safe and properly labeled.",
            tags=["FDA", "Dietary Supplement", "Regulation", "Labeling"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Medicare Advantage Risk Adjustment",
            content="Medicare Advantage plans receive risk-adjusted payments based on the health status and demographic characteristics of their enrollees, incentivizing accurate documentation and coding.",
            tags=["Medicare Advantage", "Risk Adjustment", "Payment", "Coding"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="HIPAA Right of Access",
            content="The HIPAA Right of Access requires covered entities to provide individuals with access to their protected health information in a timely manner, in the form and format requested, if readily producible.",
            tags=["HIPAA", "Right of Access", "PHI", "Patient Rights"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="FDA Accelerated Approval Pathway",
            content="The FDA's Accelerated Approval Pathway allows earlier approval of drugs that treat serious conditions and fill an unmet medical need based on a surrogate endpoint.",
            tags=["FDA", "Accelerated Approval", "Drug Approval", "Surrogate Endpoint"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="HIPAA Administrative Safeguards",
            content="HIPAA Administrative Safeguards require policies and procedures to manage the selection, development, and use of security measures to protect electronic protected health information.",
            tags=["HIPAA", "Administrative Safeguards", "ePHI", "Security"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Medicaid Fraud and Abuse Control",
            content="Medicaid Fraud and Abuse Control Units investigate and prosecute Medicaid provider fraud and patient abuse or neglect in healthcare facilities.",
            tags=["Medicaid", "Fraud", "Abuse Control", "Investigation"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="HITECH Act: Strengthening HIPAA",
            content="The HITECH Act promotes the adoption and meaningful use of health information technology and strengthens HIPAA privacy and security protections.",
            tags=["HITECH", "HIPAA", "Health IT", "Privacy"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="FDA Postmarket Surveillance",
            content="FDA postmarket surveillance monitors the safety and effectiveness of medical devices after they are approved and marketed, requiring manufacturers to report adverse events.",
            tags=["FDA", "Postmarket Surveillance", "Medical Device", "Adverse Events"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Medicare Enrollment and Eligibility",
            content="Medicare enrollment is available to individuals aged 65 or older, certain younger people with disabilities, and people with End-Stage Renal Disease. Eligibility is determined by federal regulations.",
            tags=["Medicare", "Enrollment", "Eligibility", "Regulations"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="HIPAA Physical Safeguards",
            content="HIPAA Physical Safeguards are measures to protect electronic information systems and related buildings and equipment from natural and environmental hazards and unauthorized intrusion.",
            tags=["HIPAA", "Physical Safeguards", "ePHI", "Security"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)