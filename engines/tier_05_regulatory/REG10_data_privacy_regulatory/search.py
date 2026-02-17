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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.inverted_index[term][doc.id] = freq
            for term in term_counts:
                self.doc_freqs[term] += 1
            self.N += 1
            self._recompute_stats = True

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

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

    def _score_bm25(self, query_terms: List[str], doc_id: int, query_tf: Dict[str, int]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            if doc_id not in self.inverted_index.get(term, {}):
                continue
            tf = self.inverted_index[term][doc_id]
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int, query_tf: Dict[str, int]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            if doc_id not in self.inverted_index.get(term, {}):
                continue
            tf = self.inverted_index[term][doc_id] / doc_len
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def _update_stats(self):
        if not self._recompute_stats:
            return
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.N if self.N > 0 else 0.0
        self.idf_cache.clear()
        self._recompute_stats = False

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        with self.lock:
            self._update_stats()
            query_terms = self._tokenize(query)
            query_tf = Counter(query_terms)
            candidate_docs = set()
            for term in query_terms:
                candidate_docs.update(self.inverted_index.get(term, {}).keys())
            scored_results: List[Tuple[int, float]] = []
            for doc_id in candidate_docs:
                bm25_score = self._score_bm25(query_terms, doc_id, query_tf)
                tfidf_score = self._score_tfidf(query_terms, doc_id, query_tf)
                score = bm25_score * 0.7 + tfidf_score * 0.3
                scored_results.append((doc_id, score))
            scored_results.sort(key=lambda x: x[1], reverse=True)
            results = []
            for doc_id, score in scored_results[:limit]:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc.content, query_terms)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:snippet_len] + ('...' if len(content) > snippet_len else '')
        start = max(0, min(positions) - 30)
        end = min(len(content), start + snippet_len)
        snippet = content[start:end]
        for term in query_terms:
            snippet = re.sub(r'(?i)(' + re.escape(term) + r')', r'**\1**', snippet)
        return snippet

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            self._update_stats()
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'unique_terms': len(self.doc_freqs)
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
            1,
            "CCPA Consumer Rights: Access",
            "The California Consumer Privacy Act (CCPA) grants consumers the right to request access to the personal information that businesses collect about them. Businesses must provide this information within 45 days of receiving a verifiable consumer request.",
            ["CCPA", "Access", "Consumer Rights"],
            1.0
        ),
        SearchDocument(
            2,
            "CCPA Consumer Rights: Deletion",
            "Under the CCPA, consumers have the right to request deletion of their personal information held by a business, subject to certain exceptions such as legal obligations or security purposes.",
            ["CCPA", "Deletion", "Consumer Rights"],
            1.0
        ),
        SearchDocument(
            3,
            "CCPA Consumer Rights: Portability",
            "The CCPA requires that when consumers request access to their data, businesses must provide the information in a portable and readily usable format, enabling consumers to transmit the data to another entity.",
            ["CCPA", "Portability", "Consumer Rights"],
            1.0
        ),
        SearchDocument(
            4,
            "CPRA Amendments: Sensitive Personal Information",
            "The California Privacy Rights Act (CPRA) introduces new rights and obligations regarding sensitive personal information, including the right to limit its use and disclosure.",
            ["CPRA", "Sensitive Information", "Amendments"],
            1.0
        ),
        SearchDocument(
            5,
            "CPRA Opt-Out Rights",
            "CPRA expands opt-out rights, allowing consumers to direct businesses to stop sharing their personal information for cross-context behavioral advertising.",
            ["CPRA", "Opt-Out", "Consumer Rights"],
            1.0
        ),
        SearchDocument(
            6,
            "GDPR Lawful Basis for Processing",
            "The General Data Protection Regulation (GDPR) requires organizations to have a lawful basis for processing personal data, such as consent, contract performance, legal obligation, vital interests, public task, or legitimate interests.",
            ["GDPR", "Lawful Basis", "Data Processing"],
            1.0
        ),
        SearchDocument(
            7,
            "GDPR Data Minimization Principle",
            "GDPR mandates that personal data collected must be adequate, relevant, and limited to what is necessary in relation to the purposes for which it is processed.",
            ["GDPR", "Data Minimization"],
            1.0
        ),
        SearchDocument(
            8,
            "GDPR Data Subject Rights: Access",
            "Data subjects have the right to obtain confirmation as to whether or not personal data concerning them is being processed, and access to that data.",
            ["GDPR", "Data Subject Rights", "Access"],
            1.0
        ),
        SearchDocument(
            9,
            "GDPR Data Subject Rights: Rectification",
            "Under GDPR, individuals have the right to request rectification of inaccurate personal data concerning them without undue delay.",
            ["GDPR", "Data Subject Rights", "Rectification"],
            1.0
        ),
        SearchDocument(
            10,
            "GDPR Data Subject Rights: Erasure",
            "Also known as the 'right to be forgotten', GDPR allows individuals to request erasure of their personal data in certain circumstances.",
            ["GDPR", "Data Subject Rights", "Erasure"],
            1.0
        ),
        SearchDocument(
            11,
            "GDPR Data Subject Rights: Portability",
            "GDPR grants individuals the right to receive their personal data in a structured, commonly used, and machine-readable format, and to transmit it to another controller.",
            ["GDPR", "Data Subject Rights", "Portability"],
            1.0
        ),
        SearchDocument(
            12,
            "COPPA Parental Consent Requirements",
            "The Children's Online Privacy Protection Act (COPPA) requires operators of websites or online services directed to children under 13 to obtain verifiable parental consent before collecting personal information.",
            ["COPPA", "Parental Consent"],
            1.0
        ),
        SearchDocument(
            13,
            "COPPA Notice Requirements",
            "COPPA mandates that operators provide clear and comprehensive notice of their information practices, including what information is collected from children, how it is used, and with whom it is shared.",
            ["COPPA", "Notice Requirements"],
            1.0
        ),
        SearchDocument(
            14,
            "FERPA Education Records Privacy",
            "The Family Educational Rights and Privacy Act (FERPA) protects the privacy of student education records and gives parents certain rights with respect to their children's education records.",
            ["FERPA", "Education Records", "Privacy"],
            1.0
        ),
        SearchDocument(
            15,
            "FERPA Disclosure Exceptions",
            "FERPA allows schools to disclose education records, without consent, to certain parties such as school officials with legitimate educational interests, or in compliance with a judicial order.",
            ["FERPA", "Disclosure", "Exceptions"],
            1.0
        ),
        SearchDocument(
            16,
            "GLBA Privacy Rule",
            "The Gramm-Leach-Bliley Act (GLBA) Privacy Rule requires financial institutions to provide customers with privacy notices explaining their information-sharing practices and to safeguard sensitive data.",
            ["GLBA", "Privacy Rule", "Financial Institutions"],
            1.0
        ),
        SearchDocument(
            17,
            "GLBA Safeguards Rule",
            "GLBA's Safeguards Rule mandates that financial institutions develop, implement, and maintain a comprehensive information security program to protect customer information.",
            ["GLBA", "Safeguards Rule", "Security"],
            1.0
        ),
        SearchDocument(
            18,
            "FTC Act Section 5: Unfair or Deceptive Practices",
            "Section 5 of the FTC Act prohibits unfair or deceptive acts or practices in or affecting commerce, including those related to privacy and data security.",
            ["FTC Act", "Section 5", "Privacy", "Security"],
            1.0
        ),
        SearchDocument(
            19,
            "State Data Breach Notification Laws: General Obligations",
            "Most U.S. states have enacted data breach notification laws requiring businesses to notify affected individuals and sometimes regulators when certain types of personal information are compromised.",
            ["State Laws", "Data Breach", "Notification"],
            1.0
        ),
        SearchDocument(
            20,
            "GDPR Data Protection Impact Assessment (DPIA)",
            "GDPR requires organizations to conduct a Data Protection Impact Assessment (DPIA) when processing is likely to result in a high risk to the rights and freedoms of individuals.",
            ["GDPR", "DPIA", "Impact Assessment"],
            1.0
        ),
        SearchDocument(
            21,
            "GDPR Cross-Border Data Transfers",
            "GDPR restricts transfers of personal data outside the European Economic Area unless adequate safeguards, such as Standard Contractual Clauses, are in place.",
            ["GDPR", "Cross-Border", "Data Transfers"],
            1.0
        ),
        SearchDocument(
            22,
            "Standard Contractual Clauses under GDPR",
            "Standard Contractual Clauses (SCCs) are legal tools approved by the European Commission to facilitate lawful cross-border transfers of personal data under the GDPR.",
            ["GDPR", "Standard Contractual Clauses", "SCCs"],
            1.0
        ),
        SearchDocument(
            23,
            "CCPA: Right to Non-Discrimination",
            "The CCPA prohibits businesses from discriminating against consumers for exercising their privacy rights, such as denying goods or services or charging different prices.",
            ["CCPA", "Non-Discrimination", "Consumer Rights"],
            1.0
        ),
        SearchDocument(
            24,
            "CCPA: Notice at Collection",
            "Businesses subject to the CCPA must provide notice at or before the point of collection, informing consumers about the categories of personal information collected and the purposes for which it will be used.",
            ["CCPA", "Notice", "Collection"],
            1.0
        ),
        SearchDocument(
            25,
            "GDPR Accountability Principle",
            "The GDPR accountability principle requires controllers to demonstrate compliance with all data protection principles, including maintaining records and conducting assessments.",
            ["GDPR", "Accountability", "Compliance"],
            1.0
        ),
        SearchDocument(
            26,
            "CCPA: Sale of Personal Information",
            "The CCPA gives consumers the right to opt out of the sale of their personal information by businesses to third parties.",
            ["CCPA", "Sale", "Opt-Out"],
            1.0
        ),
        SearchDocument(
            27,
            "GDPR: Data Protection Officer (DPO)",
            "Organizations may be required to appoint a Data Protection Officer (DPO) under GDPR to oversee data protection strategy and compliance.",
            ["GDPR", "DPO", "Compliance"],
            1.0
        ),
        SearchDocument(
            28,
            "GDPR: Pseudonymization and Encryption",
            "GDPR encourages the use of pseudonymization and encryption to enhance the security of personal data.",
            ["GDPR", "Pseudonymization", "Encryption", "Security"],
            1.0
        ),
        SearchDocument(
            29,
            "FERPA: Directory Information",
            "FERPA allows schools to disclose 'directory information' such as name and address without consent, unless parents opt out.",
            ["FERPA", "Directory Information", "Opt-Out"],
            1.0
        ),
        SearchDocument(
            30,
            "GLBA: Customer Information Safeguards",
            "Financial institutions must implement administrative, technical, and physical safeguards to protect customer information as required by the GLBA.",
            ["GLBA", "Safeguards", "Customer Information"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)