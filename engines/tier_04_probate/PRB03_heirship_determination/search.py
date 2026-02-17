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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_terms: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self.next_doc_id: int = 1

        self.k1 = 1.5
        self.b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self.lock:
            doc_id = self.next_doc_id
            self.next_doc_id += 1

        doc = SearchDocument(doc_id, title, content, tags, weight)
        tokens = self._tokenize(content)
        self.documents[doc_id] = doc
        self.doc_lengths[doc_id] = len(tokens)
        self.total_terms += len(tokens)

        tf_counter = Counter(tokens)
        self.term_freqs[doc_id] = tf_counter

        for term in tf_counter:
            self.term_doc_freq[term] += 1

        self.avg_doc_length = self.total_terms / max(1, len(self.documents))
        return doc_id

    def _compute_idf(self, term: str) -> float:
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        return math.log(1 + (N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf_counter = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf_counter = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = tf_counter.get(term, 0) / doc_length if doc_length > 0 else 0
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_ids = set()
        for term in query_terms:
            for doc_id in self.documents:
                if self.term_freqs[doc_id].get(term, 0) > 0:
                    candidate_ids.add(doc_id)

        scored_results = []
        for doc_id in candidate_ids:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id].content, query_terms)
                scored_results.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))

        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        indexes = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indexes:
            return ' '.join(tokens[:30]) + ('...' if len(tokens) > 30 else '')
        start = max(indexes[0] - 10, 0)
        end = min(indexes[0] + 20, len(tokens))
        snippet = tokens[start:end]
        return ' '.join(snippet) + ('...' if end < len(tokens) else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'total_terms': self.total_terms,
            'unique_terms': len(self.term_doc_freq)
        }

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
    return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        {
            "title": "Intestate Succession: Surviving Spouse with Descendants",
            "content": "When a decedent leaves a surviving spouse and descendants, the estate is divided according to jurisdictional statutes. Typically, the spouse receives a portion, with the remainder distributed per stirpes among descendants.",
            "tags": ["intestate succession", "surviving spouse", "descendants", "distribution"],
            "weight": 1.0
        },
        {
            "title": "Intestate Succession: No Spouse, Descendants Only",
            "content": "If the decedent is not survived by a spouse but has descendants, the entire estate passes to the descendants, usually distributed per stirpes.",
            "tags": ["intestate succession", "descendants", "no spouse", "per stirpes"],
            "weight": 1.0
        },
        {
            "title": "Per Stirpes Distribution Mechanics",
            "content": "Per stirpes distribution divides the estate at each generational level. Each branch receives an equal share, and the share of a deceased descendant passes to their own descendants.",
            "tags": ["per stirpes", "distribution", "mechanics", "descendants"],
            "weight": 1.0
        },
        {
            "title": "Community Property Classification",
            "content": "Community property is property acquired during marriage, except by gift or inheritance. Upon death, the surviving spouse retains their half, and the decedent's half is subject to succession.",
            "tags": ["community property", "classification", "marriage", "succession"],
            "weight": 1.0
        },
        {
            "title": "Pretermitted Heir Rights",
            "content": "A pretermitted heir is a child omitted from a will. Statutes may grant such heirs a share of the estate unless intentional omission is proven.",
            "tags": ["pretermitted heir", "rights", "will", "omission"],
            "weight": 1.0
        },
        {
            "title": "Adopted Children's Inheritance Rights",
            "content": "Adopted children inherit from adoptive parents as biological children, unless the adoption decree specifies otherwise. They may not inherit from biological parents unless permitted by statute.",
            "tags": ["adopted children", "inheritance", "rights", "adoption"],
            "weight": 1.0
        },
        {
            "title": "Posthumous Heirs and Gestation Period",
            "content": "Heirs conceived before but born after the decedent's death may inherit if born within the statutory gestation period, typically 280 days.",
            "tags": ["posthumous heirs", "gestation", "inheritance", "succession"],
            "weight": 1.0
        },
        {
            "title": "Half-Blood Relatives' Inheritance Rights",
            "content": "Half-blood relatives may inherit, but often receive only half the share of full-blood relatives unless statutes provide otherwise.",
            "tags": ["half-blood", "relatives", "inheritance", "succession"],
            "weight": 1.0
        },
        {
            "title": "Simultaneous Death and 120-Hour Survival Rule",
            "content": "If individuals die simultaneously or within 120 hours of each other, each is presumed to have predeceased the other for inheritance purposes, preventing reciprocal inheritance.",
            "tags": ["simultaneous death", "120-hour rule", "inheritance", "succession"],
            "weight": 1.0
        },
        {
            "title": "Ancestral Property and Collateral Heirs",
            "content": "Ancestral property passes to collateral heirs of the bloodline from which the property originated, according to jurisdictional rules.",
            "tags": ["ancestral property", "collateral heirs", "succession", "bloodline"],
            "weight": 1.0
        },
        {
            "title": "Anti-Lapse Statute for Testamentary Gifts",
            "content": "Anti-lapse statutes prevent gifts from lapsing when a beneficiary predeceases the testator, allowing the gift to pass to the beneficiary's descendants.",
            "tags": ["anti-lapse", "statute", "testamentary gifts", "beneficiary"],
            "weight": 1.0
        },
        {
            "title": "Intestate Succession Without Spouse or Descendants",
            "content": "If the decedent leaves no spouse or descendants, the estate passes to parents, siblings, or more remote relatives according to statutory priority.",
            "tags": ["intestate succession", "no spouse", "no descendants", "priority"],
            "weight": 1.0
        },
        {
            "title": "Inheritance Rights of Non-Marital Children",
            "content": "Non-marital children inherit from their parents if paternity is established. Statutes may require proof of relationship for inheritance.",
            "tags": ["non-marital children", "inheritance", "paternity", "succession"],
            "weight": 1.0
        },
        {
            "title": "Stepchildren and Foster Children - No Inheritance Rights",
            "content": "Stepchildren and foster children generally do not inherit unless legally adopted or named in a will.",
            "tags": ["stepchildren", "foster children", "inheritance", "adoption"],
            "weight": 1.0
        },
        {
            "title": "Advancements and Hotchpot Doctrine",
            "content": "Advancements are gifts made during life intended as part of inheritance. The hotchpot doctrine requires adding advancements to the estate before division among heirs.",
            "tags": ["advancements", "hotchpot", "inheritance", "estate"],
            "weight": 1.0
        },
        {
            "title": "Disclaimer of Inheritance Rights",
            "content": "An heir may disclaim inheritance rights, causing the disclaimed property to pass as if the heir predeceased the decedent.",
            "tags": ["disclaimer", "inheritance", "rights", "succession"],
            "weight": 1.0
        },
        {
            "title": "Burden of Proof for Survivorship",
            "content": "The burden of proof for survivorship lies with the party asserting inheritance. If survivorship cannot be proven, inheritance may fail.",
            "tags": ["burden of proof", "survivorship", "inheritance", "succession"],
            "weight": 1.0
        },
        {
            "title": "Surviving Spouse's Right of Election",
            "content": "A surviving spouse may elect to take a statutory share of the estate, overriding the will. Election periods and procedures are governed by statute.",
            "tags": ["surviving spouse", "right of election", "statutory share", "will"],
            "weight": 1.0
        },
        {
            "title": "Intestate Succession Priority Flow Chart",
            "content": "Succession follows a statutory priority: spouse, descendants, parents, siblings, and more remote relatives. Flow charts clarify the order of inheritance.",
            "tags": ["intestate succession", "priority", "flow chart", "inheritance"],
            "weight": 1.0
        },
        {
            "title": "Calculating Degree of Relationship",
            "content": "Degree of relationship is calculated by counting generations between the decedent and the heir. Closer degrees take priority in inheritance.",
            "tags": ["degree of relationship", "inheritance", "succession", "priority"],
            "weight": 1.0
        },
        {
            "title": "Slayer Statute - Killer Disqualified",
            "content": "A person who intentionally kills the decedent is disqualified from inheriting under the slayer statute.",
            "tags": ["slayer statute", "killer", "disqualification", "inheritance"],
            "weight": 1.0
        },
        {
            "title": "Tracing Separate Property Character",
            "content": "Separate property is traced to its origin, such as inheritance or gift. Proper tracing determines its classification at death.",
            "tags": ["separate property", "tracing", "inheritance", "classification"],
            "weight": 1.0
        },
        {
            "title": "Surviving Spouse's Homestead Rights",
            "content": "The surviving spouse may have homestead rights, allowing continued residence or a life estate in the marital home.",
            "tags": ["surviving spouse", "homestead", "rights", "marital home"],
            "weight": 1.0
        },
        {
            "title": "Distribution of Community Property Upon Death",
            "content": "Upon death, community property is divided equally between the surviving spouse and the decedent's heirs. Separate property is distributed according to succession laws.",
            "tags": ["community property", "distribution", "death", "succession"],
            "weight": 1.0
        },
        {
            "title": "Posthumous Children and Inheritance",
            "content": "Children born after the decedent's death inherit if conceived before death and born within the statutory period.",
            "tags": ["posthumous children", "inheritance", "gestation", "succession"],
            "weight": 1.0
        },
        {
            "title": "Collateral Relatives and Intestate Succession",
            "content": "Collateral relatives, such as siblings and cousins, inherit when no spouse or descendants survive. Statutes define the order of priority.",
            "tags": ["collateral relatives", "intestate succession", "priority", "inheritance"],
            "weight": 1.0
        },
        {
            "title": "Inheritance Rights of Grandchildren",
            "content": "Grandchildren inherit by representation if their parent predeceases the decedent. Distribution is typically per stirpes.",
            "tags": ["grandchildren", "inheritance", "representation", "per stirpes"],
            "weight": 1.0
        },
        {
            "title": "Hotchpot Doctrine Explained",
            "content": "The hotchpot doctrine ensures fairness by combining advancements with the estate before dividing among heirs.",
            "tags": ["hotchpot", "doctrine", "advancements", "estate"],
            "weight": 1.0
        },
        {
            "title": "Statutory Share for Surviving Spouse",
            "content": "Statutes grant the surviving spouse a share of the estate, regardless of the will's terms. The share varies by jurisdiction.",
            "tags": ["statutory share", "surviving spouse", "estate", "succession"],
            "weight": 1.0
        },
        {
            "title": "Inheritance Rights of Parents",
            "content": "If no spouse or descendants survive, parents may inherit the estate, either in whole or in part.",
            "tags": ["parents", "inheritance", "succession", "priority"],
            "weight": 1.0
        },
        {
            "title": "Distribution Among Siblings",
            "content": "Siblings inherit equally when no spouse, descendants, or parents survive. Half-blood siblings may receive reduced shares.",
            "tags": ["siblings", "inheritance", "distribution", "succession"],
            "weight": 1.0
        },
        {
            "title": "Advancements: Intent and Evidence",
            "content": "To qualify as an advancement, the decedent must intend the gift to count toward inheritance. Evidence may include written statements or acknowledgments.",
            "tags": ["advancements", "intent", "evidence", "inheritance"],
            "weight": 1.0
        },
        {
            "title": "Inheritance Rights of Descendants",
            "content": "Descendants inherit according to statutory schemes, often per stirpes. Adopted and non-marital children may be included.",
            "tags": ["descendants", "inheritance", "succession", "statute"],
            "weight": 1.0
        },
        {
            "title": "Statutory Priority in Intestate Succession",
            "content": "Statutes establish priority for inheritance: spouse, descendants, parents, siblings, and further relatives.",
            "tags": ["statutory priority", "intestate succession", "inheritance", "succession"],
            "weight": 1.0
        },
        {
            "title": "Effect of Disclaimer on Distribution",
            "content": "When an heir disclaims inheritance, their share passes as if they predeceased the decedent, often to their own descendants.",
            "tags": ["disclaimer", "distribution", "inheritance", "succession"],
            "weight": 1.0
        },
        {
            "title": "Proof of Paternity for Inheritance",
            "content": "Non-marital children must prove paternity to inherit. Proof may include genetic testing or acknowledgment by the parent.",
            "tags": ["proof of paternity", "inheritance", "non-marital children", "succession"],
            "weight": 1.0
        },
        {
            "title": "Inheritance Rights of Adopted Children",
            "content": "Adopted children inherit from adoptive parents as if biological. Statutes may restrict inheritance from biological parents.",
            "tags": ["adopted children", "inheritance", "adoption", "succession"],
            "weight": 1.0
        },
        {
            "title": "Distribution of Separate Property",
            "content": "Separate property is distributed according to succession laws, often to descendants or collateral relatives.",
            "tags": ["separate property", "distribution", "succession", "inheritance"],
            "weight": 1.0
        },
        {
            "title": "Inheritance Rights of Stepchildren",
            "content": "Stepchildren do not inherit unless adopted or named in a will. Foster children are similarly excluded.",
            "tags": ["stepchildren", "inheritance", "succession", "adoption"],
            "weight": 1.0
        },
        {
            "title": "120-Hour Survival Rule Explained",
            "content": "The 120-hour rule requires heirs to survive the decedent by at least 120 hours to inherit. Failure to survive results in disqualification.",
            "tags": ["120-hour rule", "survival", "inheritance", "succession"],
            "weight": 1.0
        },
        {
            "title": "Inheritance Rights of Collateral Heirs",
            "content": "Collateral heirs inherit when no spouse or descendants survive. Statutes define the order and degree of relationship required.",
            "tags": ["collateral heirs", "inheritance", "succession", "priority"],
            "weight": 1.0
        },
        {
            "title": "Surviving Spouse's Election Rights",
            "content": "The surviving spouse may elect to take a statutory share, overriding the will. Election must be made within statutory periods.",
            "tags": ["surviving spouse", "election", "statutory share", "will"],
            "weight": 1.0
        },
        {
            "title": "Slayer Statute: Disqualification Explained",
            "content": "The slayer statute disqualifies individuals who intentionally kill the decedent from inheriting any portion of the estate.",
            "tags": ["slayer statute", "disqualification", "inheritance", "succession"],
            "weight": 1.0
        },
        {
            "title": "Tracing Community Property",
            "content": "Community property is traced to marital acquisition. Separate property is traced to inheritance or gift.",
            "tags": ["community property", "tracing", "inheritance", "marriage"],
            "weight": 1.0
        },
        {
            "title": "Homestead Rights of Surviving Spouse",
            "content": "Homestead rights allow the surviving spouse to reside in the marital home or receive a life estate, protecting housing security.",
            "tags": ["homestead", "surviving spouse", "rights", "marital home"],
            "weight": 1.0
        },
        {
            "title": "Distribution to Descendants Per Stirpes",
            "content": "Per stirpes distribution ensures each branch of descendants receives an equal share, with shares passing to their own descendants if predeceased.",
            "tags": ["per stirpes", "distribution", "descendants", "inheritance"],
            "weight": 1.0
        },
        {
            "title": "Inheritance Rights of Foster Children",
            "content": "Foster children do not inherit unless legally adopted or named in a will. Statutory rights are limited.",
            "tags": ["foster children", "inheritance", "adoption", "succession"],
            "weight": 1.0
        },
        {
            "title": "Advancements and Estate Division",
            "content": "Advancements are considered in estate division to ensure fairness among heirs. The hotchpot doctrine may apply.",
            "tags": ["advancements", "estate division", "hotchpot", "inheritance"],
            "weight": 1.0
        },
        {
            "title": "Disclaimer Procedures and Effects",
            "content": "Disclaimer procedures require written statements. Disclaimed shares pass as if the heir predeceased the decedent.",
            "tags": ["disclaimer", "procedures", "inheritance", "succession"],
            "weight": 1.0
        },
        {
            "title": "Burden of Proof in Simultaneous Death",
            "content": "In cases of simultaneous death, the burden of proof lies with the party asserting survivorship. Statutes may presume predeceasing.",
            "tags": ["burden of proof", "simultaneous death", "survivorship", "inheritance"],
            "weight": 1.0
        },
        {
            "title": "Statutory Priority: Parents and Siblings",
            "content": "If no spouse or descendants survive, parents and siblings inherit according to statutory priority and degree of relationship.",
            "tags": ["statutory priority", "parents", "siblings", "inheritance"],
            "weight": 1.0
        },
        {
            "title": "Distribution of Estate Without Will",
            "content": "When no will exists, the estate is distributed according to intestate succession statutes, prioritizing spouse, descendants, and collateral relatives.",
            "tags": ["distribution", "estate", "intestate succession", "priority"],
            "weight": 1.0
        }
    ]
    for doc in docs:
        idx.add_document(doc["title"], doc["content"], doc["tags"], doc["weight"])