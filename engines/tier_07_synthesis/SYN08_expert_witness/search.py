import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._doc_tags: Dict[str, Set[int]] = defaultdict(set)
        self._lock = threading.Lock()
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self._documents[doc.id] = doc
            self._term_freqs[doc.id] = tf
            self._doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self._inverted_index[term].add(doc.id)
            for tag in doc.tags:
                self._doc_tags[tag.lower()].add(doc.id)
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_candidates = set()
        for term in query_terms:
            doc_candidates.update(self._inverted_index.get(term, set()))
        scored_results: List[Tuple[float, int]] = []
        for doc_id in doc_candidates:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self._documents[doc_id]
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            score *= doc.weight
            scored_results.append((score, doc_id))
        top_hits = heapq.nlargest(limit, scored_results)
        results = []
        for score, doc_id in top_hits:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        with self._lock:
            return {
                "documents": self._total_docs,
                "unique_terms": len(self._inverted_index),
                "avg_doc_length": int(self._avg_doc_length),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = self._total_docs
        df = len(self._inverted_index.get(term, []))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        avg_dl = self._avg_doc_length if self._avg_doc_length > 0 else 1
        score = 0.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            score += idf * (f * (self._bm25_k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            term_freq = tf.get(term, 0)
            if term_freq == 0:
                continue
            tf_norm = term_freq / (doc_len if doc_len > 0 else 1)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:snippet_len] + ('...' if len(content) > snippet_len else '')
        start = max(min(positions) - 30, 0)
        end = min(start + snippet_len, len(content))
        snippet = content[start:end]
        for term in query_terms:
            snippet = re.sub(r'(?i)\b({})\b'.format(re.escape(term)), r'**\1**', snippet)
        if start > 0:
            snippet = '...' + snippet
        if end < len(content):
            snippet += '...'
        return snippet

# Singleton factory for search index
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_search_index(_search_index_instance)
        return _search_index_instance

def _seed_search_index(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Daubert Standard: Federal Admissibility of Expert Testimony",
            "The Daubert Standard governs the admissibility of expert testimony under Federal Rule of Evidence 702. It requires that expert evidence be both relevant and reliable, considering factors such as testability, peer review, error rates, and general acceptance.",
            ["daubert", "federal", "admissibility", "expert testimony", "FRE 702"],
            1.0
        ),
        SearchDocument(
            2,
            "Frye General Acceptance Test",
            "The Frye test requires that scientific evidence is admissible only if the methodology or principle is generally accepted by the relevant scientific community. This test predates Daubert and is still used in some jurisdictions.",
            ["frye", "general acceptance", "scientific evidence"],
            1.0
        ),
        SearchDocument(
            3,
            "Federal Rule of Evidence 702: Expert Testimony Requirements",
            "FRE 702 sets forth the requirements for expert testimony: the witness must be qualified, the testimony must help the trier of fact, and must be based on sufficient facts or data, reliable principles and methods, and proper application.",
            ["FRE 702", "expert testimony", "qualifications", "reliability"],
            1.0
        ),
        SearchDocument(
            4,
            "Kumho Tire v. Carmichael: Extension to Technical Experts",
            "The Supreme Court in Kumho Tire extended Daubert's gatekeeping role to all expert testimony, not just scientific, including technical and other specialized knowledge.",
            ["kumho tire", "technical experts", "daubert", "gatekeeping"],
            1.0
        ),
        SearchDocument(
            5,
            "FRCP Rule 26(a)(2): Expert Disclosure Requirements",
            "Federal Rule of Civil Procedure 26(a)(2) requires parties to disclose the identity of expert witnesses and provide a written report containing opinions, data considered, exhibits, qualifications, prior testimony, and compensation.",
            ["FRCP 26(a)(2)", "expert disclosure", "expert report"],
            1.0
        ),
        SearchDocument(
            6,
            "Expert Report Content Requirements",
            "Expert reports must include a complete statement of all opinions, the basis and reasons, facts or data considered, exhibits, qualifications, prior testimony, and compensation details.",
            ["expert report", "content", "requirements", "FRCP 26"],
            1.0
        ),
        SearchDocument(
            7,
            "FRE 703: Basis of Expert Opinion",
            "Federal Rule of Evidence 703 allows experts to base opinions on facts or data perceived or made known to them, even if such information is not admissible, provided it is of a type reasonably relied upon by experts in the field.",
            ["FRE 703", "expert opinion", "basis", "facts", "data"],
            1.0
        ),
        SearchDocument(
            8,
            "Daubert Motion Practice and Timing",
            "A Daubert motion is a pretrial motion to exclude expert testimony that does not meet the standards of reliability and relevance. Timing varies by jurisdiction but is typically filed before trial.",
            ["daubert motion", "timing", "exclude", "expert testimony"],
            1.0
        ),
        SearchDocument(
            9,
            "Qualifications of Expert Witness",
            "An expert witness must possess knowledge, skill, experience, training, or education sufficient to qualify as an expert under FRE 702.",
            ["qualifications", "expert witness", "FRE 702"],
            1.0
        ),
        SearchDocument(
            10,
            "Hypothetical Questions to Experts",
            "Attorneys may pose hypothetical questions to expert witnesses to elicit opinions based on assumed facts, provided the facts are supported by evidence in the record.",
            ["hypothetical questions", "expert witness", "opinion"],
            1.0
        ),
        SearchDocument(
            11,
            "Cross-Examination of Expert Witnesses",
            "Cross-examination is a critical tool for challenging the credibility, methodology, and conclusions of expert witnesses, including the basis for their opinions.",
            ["cross-examination", "expert witness", "credibility"],
            1.0
        ),
        SearchDocument(
            12,
            "Rebuttal Expert Testimony",
            "Rebuttal experts are permitted to address new matters raised by opposing experts. Disclosure timing is governed by court order and FRCP 26(a)(2)(D).",
            ["rebuttal", "expert testimony", "FRCP 26"],
            1.0
        ),
        SearchDocument(
            13,
            "Expert Deposition Preparation",
            "Preparation for expert depositions includes reviewing reports, underlying data, prior testimony, and anticipated lines of questioning.",
            ["expert deposition", "preparation", "testimony"],
            1.0
        ),
        SearchDocument(
            14,
            "Opinion Scope and Ultimate Issue",
            "Experts may testify to the ultimate issue in a case, but cannot offer legal conclusions. FRE 704 governs the admissibility of such opinions.",
            ["opinion scope", "ultimate issue", "FRE 704"],
            1.0
        ),
        SearchDocument(
            15,
            "Expert Witness Immunity and Ethics",
            "Expert witnesses generally have immunity from suit for their testimony, but are subject to ethical obligations including honesty and avoidance of conflicts of interest.",
            ["immunity", "ethics", "expert witness"],
            1.0
        ),
        SearchDocument(
            16,
            "Testability and Falsifiability: Daubert Factor",
            "Testability and falsifiability are key Daubert factors for assessing the reliability of scientific methodology. Courts examine whether a theory can be empirically tested.",
            ["testability", "falsifiability", "daubert", "reliability"],
            1.0
        ),
        SearchDocument(
            17,
            "Peer Review and Publication: Daubert Factor",
            "Peer review and publication status of a methodology are considered under Daubert as indicators of reliability, though not dispositive.",
            ["peer review", "publication", "daubert", "reliability"],
            1.0
        ),
        SearchDocument(
            18,
            "Known or Potential Error Rate: Daubert Factor",
            "Courts consider the known or potential error rate of a scientific technique as part of the Daubert reliability analysis.",
            ["error rate", "daubert", "reliability"],
            1.0
        ),
        SearchDocument(
            19,
            "Standards and Controls: Daubert Factor",
            "The existence and maintenance of standards and controls is a Daubert factor for evaluating the reliability of expert methodology.",
            ["standards", "controls", "daubert", "methodology"],
            1.0
        ),
        SearchDocument(
            20,
            "General Acceptance in Scientific Community",
            "General acceptance of a methodology within the relevant scientific community is a factor under both Frye and Daubert for admissibility.",
            ["general acceptance", "scientific community", "frye", "daubert"],
            1.0
        ),
        SearchDocument(
            21,
            "Relevance and Fit Requirement",
            "Expert testimony must be relevant and fit the facts of the case to be admissible under Daubert and FRE 702.",
            ["relevance", "fit", "daubert", "FRE 702"],
            1.0
        ),
        SearchDocument(
            22,
            "Supplementation of Expert Disclosures",
            "Parties must supplement expert disclosures under FRCP 26(e) if additional information is learned or opinions change.",
            ["supplementation", "expert disclosures", "FRCP 26(e)"],
            1.0
        ),
        SearchDocument(
            23,
            "Exclusion of Expert Testimony as Sanction",
            "Failure to properly disclose expert opinions can result in exclusion of testimony as a sanction under FRCP 37(c)(1).",
            ["exclusion", "expert testimony", "sanction", "FRCP 37"],
            1.0
        ),
        SearchDocument(
            24,
            "Court-Appointed Experts Under FRE 706",
            "FRE 706 authorizes courts to appoint their own expert witnesses, who must advise the parties of findings and may be deposed and cross-examined.",
            ["court-appointed expert", "FRE 706", "expert witness"],
            1.0
        ),
        SearchDocument(
            25,
            "Treating Physician as Expert Witness",
            "A treating physician may testify as an expert regarding diagnosis and treatment, but may require disclosure as an expert if offering opinions beyond treatment.",
            ["treating physician", "expert witness", "disclosure"],
            1.0
        ),
        SearchDocument(
            26,
            "Ipse Dixit Rejection and Explained Methodology",
            "Courts may reject expert opinions based solely on the expert's assertion (ipse dixit) without an explained methodology, requiring a reasoned basis for the opinion.",
            ["ipse dixit", "explained methodology", "expert opinion"],
            1.0
        ),
        SearchDocument(
            27,
            "Burden of Proof in Daubert Hearings",
            "The proponent of expert evidence bears the burden of establishing admissibility under Daubert by a preponderance of the evidence.",
            ["burden of proof", "daubert", "admissibility"],
            1.0
        ),
        SearchDocument(
            28,
            "Reliability Factors: Non-Exclusive List",
            "Daubert factors are not exclusive; courts may consider other indicia of reliability depending on the context and field.",
            ["reliability", "daubert", "factors", "non-exclusive"],
            1.0
        ),
        SearchDocument(
            29,
            "Expert Testimony and Summary Judgment",
            "Expert evidence may be critical at summary judgment. Courts may exclude expert opinions that do not meet Daubert or FRE 702 requirements.",
            ["expert testimony", "summary judgment", "daubert", "FRE 702"],
            1.0
        ),
        SearchDocument(
            30,
            "Expert Compensation and Bias",
            "Disclosure of expert compensation is required to assess potential bias under FRCP 26(a)(2)(B)(vi).",
            ["compensation", "bias", "expert witness", "FRCP 26"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)