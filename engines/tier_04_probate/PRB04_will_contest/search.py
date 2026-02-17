import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Optional

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
        self._doc_freqs: Dict[str, int] = defaultdict(int)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._lock = threading.Lock()
        self._next_doc_id = 1
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self._lock:
            doc_id = self._next_doc_id
            self._next_doc_id += 1
            doc = SearchDocument(doc_id, title, content, tags, weight)
            self._documents[doc_id] = doc

            tokens = self._tokenize(content)
            tf = Counter(tokens)
            self._term_freqs[doc_id] = tf
            doc_length = len(tokens)
            self._doc_lengths[doc_id] = doc_length

            for term in tf:
                self._inverted_index[term].add(doc_id)
                self._doc_freqs[term] += 1

            self._avg_doc_length = (
                sum(self._doc_lengths.values()) / len(self._doc_lengths)
                if self._doc_lengths else 0.0
            )
            self._idf_cache.clear()
            return doc_id

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self._inverted_index.get(term, set()))

        scored: List[Tuple[float, int]] = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self._documents[doc_id]
            score = bm25_score * 0.7 + tfidf_score * 0.3
            score *= doc.weight
            scored.append((score, doc_id))

        top_docs = heapq.nlargest(limit, scored)
        results = []
        for score, doc_id in top_docs:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        with self._lock:
            return {
                "document_count": len(self._documents),
                "unique_terms": len(self._inverted_index),
                "total_terms": sum(len(tf) for tf in self._term_freqs.values()),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self._documents)
        df = self._doc_freqs.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_length = self._doc_lengths[doc_id]
        avgdl = self._avg_doc_length or 1.0
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / avgdl)
            score += idf * freq * (self._bm25_k1 + 1) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_length = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_length if doc_length else 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = []
        for idx, token in enumerate(tokens):
            if token in query_terms:
                positions.append(idx)
        if not positions:
            snippet = content[:length]
            return snippet + "..." if len(content) > length else snippet
        start = max(positions[0] - 10, 0)
        end = min(start + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + "..." if len(snippet_tokens) < len(tokens) else snippet

# Singleton factory
_search_index_singleton: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_singleton
    with _search_index_lock:
        if _search_index_singleton is None:
            _search_index_singleton = SearchIndex()
            _seed_documents(_search_index_singleton)
        return _search_index_singleton

def _seed_documents(index: SearchIndex):
    docs = [
        {
            "title": "Testamentary Capacity Standard",
            "content": (
                "A testator must possess testamentary capacity at the time of will execution. "
                "This requires understanding the nature of the act, the extent of property, "
                "the natural objects of bounty, and the disposition being made."
            ),
            "tags": ["testamentary_capacity_standard"]
        },
        {
            "title": "Undue Influence: Elements and Burden",
            "content": (
                "A will is invalid if procured by undue influence. The contestant must show "
                "susceptibility, opportunity, disposition to exert influence, and a result "
                "reflecting undue influence."
            ),
            "tags": ["undue_influence_standard"]
        },
        {
            "title": "Fraud in Execution of Wills",
            "content": (
                "Fraud in execution occurs when a testator is deceived as to the nature "
                "of the document being signed, rendering the will invalid."
            ),
            "tags": ["fraud_in_execution"]
        },
        {
            "title": "Improper Execution Formalities",
            "content": (
                "A will must be executed with required formalities, including the testator's "
                "signature and attestation by witnesses. Failure may invalidate the will."
            ),
            "tags": ["improper_execution_formalities"]
        },
        {
            "title": "Express and Implied Revocation of Wills",
            "content": (
                "A will may be revoked expressly by a subsequent writing or impliedly by "
                "physical act or inconsistency with a later instrument."
            ),
            "tags": ["revocation_express_implied"]
        },
        {
            "title": "Holographic Will Validity",
            "content": (
                "A holographic will is valid if it is entirely in the testator's handwriting "
                "and signed, even without witnesses, in many jurisdictions."
            ),
            "tags": ["holographic_will_validity"]
        },
        {
            "title": "No-Contest Clause Enforceability",
            "content": (
                "A no-contest clause penalizes beneficiaries who contest the will. "
                "Enforceability depends on probable cause and state law."
            ),
            "tags": ["no_contest_clause_enforceability"]
        },
        {
            "title": "Tortious Interference with Inheritance",
            "content": (
                "A tort claim may arise when a third party intentionally interferes with "
                "an expected inheritance, causing loss to the intended beneficiary."
            ),
            "tags": ["tortious_interference_with_inheritance"]
        },
        {
            "title": "Burden of Proof in Will Contests",
            "content": (
                "The proponent of the will bears the burden to prove due execution. "
                "The contestant bears the burden to prove undue influence or incapacity."
            ),
            "tags": ["burden_of_proof_allocation"]
        },
        {
            "title": "Interested Witness Rule",
            "content": (
                "A will attested by an interested witness may be invalid as to that witness's "
                "share unless there are sufficient disinterested witnesses."
            ),
            "tags": ["interested_witness_rule"]
        },
        {
            "title": "Dependent Relative Revocation Doctrine",
            "content": (
                "Dependent relative revocation allows a revoked will to be revived if "
                "the revocation was based on a mistaken belief that a new disposition "
                "would be effective."
            ),
            "tags": ["dependent_relative_revocation"]
        },
        {
            "title": "Integration and Incorporation by Reference",
            "content": (
                "Integration allows documents present at execution to be part of the will. "
                "A writing may be incorporated by reference if it existed at execution, "
                "is identified, and intended to be part of the will."
            ),
            "tags": ["integration_incorporation_by_reference"]
        },
        {
            "title": "Class Gifts and Lapse",
            "content": (
                "A class gift is a bequest to a group described as a class. If a member "
                "predeceases, anti-lapse statutes may apply to preserve the gift."
            ),
            "tags": ["class_gifts_and_lapse"]
        },
        {
            "title": "Ademption by Extinction",
            "content": (
                "Ademption by extinction occurs when a specific bequest is not in the estate "
                "at death. The beneficiary takes nothing unless a contrary intent appears."
            ),
            "tags": ["ademption_by_extinction"]
        },
        {
            "title": "Abatement Order of Gifts",
            "content": (
                "If the estate is insufficient, gifts abate in a prescribed order: "
                "residuary, general, then specific devises."
            ),
            "tags": ["abatement_order"]
        },
        {
            "title": "Advancements and Satisfaction",
            "content": (
                "An advancement is a lifetime gift intended as a prepayment of inheritance. "
                "Satisfaction applies to testamentary gifts fulfilled during life."
            ),
            "tags": ["advancements_and_satisfaction"]
        },
        {
            "title": "Elective Share and Community Property",
            "content": (
                "A surviving spouse may claim an elective share or community property portion, "
                "regardless of will terms, to prevent disinheritance."
            ),
            "tags": ["elective_share_and_community_property"]
        },
        {
            "title": "Standing to Contest a Will",
            "content": (
                "Only interested parties, such as heirs or beneficiaries with pecuniary interest, "
                "have standing to contest a will."
            ),
            "tags": ["standing_to_contest"]
        },
        {
            "title": "Venue and Jurisdiction in Will Contests",
            "content": (
                "Venue is proper where the decedent was domiciled at death. Jurisdiction "
                "is in probate court with authority over the estate."
            ),
            "tags": ["venue_and_jurisdiction"]
        },
        {
            "title": "Statute of Limitations for Will Contests",
            "content": (
                "A will contest must be filed within the statutory period after probate, "
                "or the claim is barred."
            ),
            "tags": ["statute_of_limitations"]
        },
        {
            "title": "Harmless Error Doctrine",
            "content": (
                "The harmless error doctrine allows courts to excuse minor defects in will "
                "execution if clear and convincing evidence shows the testator's intent."
            ),
            "tags": ["harmless_error_doctrine"]
        },
        {
            "title": "Capacity: Lucid Interval Doctrine",
            "content": (
                "A testator with a mental disorder may execute a valid will during a lucid interval, "
                "if capacity is present at the time."
            ),
            "tags": ["testamentary_capacity_standard"]
        },
        {
            "title": "Presumption of Undue Influence",
            "content": (
                "A presumption arises if a confidential relationship, active procurement, "
                "and an unnatural disposition are shown."
            ),
            "tags": ["undue_influence_standard"]
        },
        {
            "title": "Fraud in Inducement",
            "content": (
                "Fraud in inducement occurs when a testator is misled as to facts, "
                "causing a disposition they would not otherwise make."
            ),
            "tags": ["fraud_in_execution"]
        },
        {
            "title": "Partial Revocation and Republication",
            "content": (
                "A will may be partially revoked by physical act or by subsequent instrument. "
                "Republication by codicil may revive revoked provisions."
            ),
            "tags": ["revocation_express_implied"]
        },
        {
            "title": "Lost and Destroyed Wills",
            "content": (
                "A lost or destroyed will may be probated if its contents and due execution "
                "are proved by clear and convincing evidence."
            ),
            "tags": ["improper_execution_formalities"]
        },
        {
            "title": "Integration: Stapled and Attached Pages",
            "content": (
                "Pages physically present and intended to be part of the will at execution "
                "are integrated, even if not all are signed."
            ),
            "tags": ["integration_incorporation_by_reference"]
        },
        {
            "title": "Anti-Lapse Statute Application",
            "content": (
                "Anti-lapse statutes save gifts to certain relatives who predecease, "
                "passing the gift to their descendants."
            ),
            "tags": ["class_gifts_and_lapse"]
        },
        {
            "title": "Specific, General, and Demonstrative Gifts",
            "content": (
                "Specific gifts are particular items, general gifts are from general assets, "
                "and demonstrative gifts are payable from a specific source."
            ),
            "tags": ["class_gifts_and_lapse"]
        },
        {
            "title": "Satisfaction of Legacies",
            "content": (
                "A legacy may be satisfied by inter vivos gift if the testator intended "
                "the gift to count against the testamentary bequest."
            ),
            "tags": ["advancements_and_satisfaction"]
        },
        {
            "title": "Community Property: Quasi-Community Assets",
            "content": (
                "Quasi-community property acquired during marriage may be subject to "
                "spousal elective share rights."
            ),
            "tags": ["elective_share_and_community_property"]
        },
        {
            "title": "Venue: Ancillary Probate",
            "content": (
                "Ancillary probate may be required for real property located outside the "
                "decedent's domicile."
            ),
            "tags": ["venue_and_jurisdiction"]
        },
        {
            "title": "Statute of Limitations: Tolling",
            "content": (
                "The statute of limitations may be tolled for fraud or concealment, "
                "extending the period to contest a will."
            ),
            "tags": ["statute_of_limitations"]
        },
        {
            "title": "Harmless Error: Substantial Compliance",
            "content": (
                "Substantial compliance with execution formalities may be sufficient if "
                "the testator's intent is clear."
            ),
            "tags": ["harmless_error_doctrine"]
        },
        {
            "title": "Tortious Interference: Remedies",
            "content": (
                "Remedies for tortious interference with inheritance may include damages "
                "or imposition of a constructive trust."
            ),
            "tags": ["tortious_interference_with_inheritance"]
        },
        {
            "title": "Interested Witness: Purging Statute",
            "content": (
                "A purging statute may reduce an interested witness's share to what they "
                "would take in intestacy."
            ),
            "tags": ["interested_witness_rule"]
        },
        {
            "title": "Abatement: Order of Reduction",
            "content": (
                "Gifts abate in the following order: property not disposed of by will, "
                "residuary devises, general devises, specific devises."
            ),
            "tags": ["abatement_order"]
        },
        {
            "title": "Holographic Will: Jurisdictional Variations",
            "content": (
                "Some states require holographic wills to be dated, others do not. "
                "Witnesses are generally not required."
            ),
            "tags": ["holographic_will_validity"]
        },
        {
            "title": "No-Contest Clause: Probable Cause Exception",
            "content": (
                "A no-contest clause is unenforceable if the contestant had probable cause "
                "to challenge the will."
            ),
            "tags": ["no_contest_clause_enforceability"]
        },
        {
            "title": "Dependent Relative Revocation: Application",
            "content": (
                "If a testator revokes a will under a mistaken belief that another will is valid, "
                "the doctrine of dependent relative revocation may revive the prior will."
            ),
            "tags": ["dependent_relative_revocation"]
        },
        {
            "title": "Standing: Disinherited Heirs",
            "content": (
                "Disinherited heirs have standing to contest a will if they would take "
                "under intestacy but for the will."
            ),
            "tags": ["standing_to_contest"]
        },
        {
            "title": "Burden of Proof: Presumptions",
            "content": (
                "A presumption of due execution arises if formalities are met. "
                "The burden shifts to the contestant to rebut the presumption."
            ),
            "tags": ["burden_of_proof_allocation"]
        },
        {
            "title": "Ademption: Stock Splits and Changes",
            "content": (
                "If a specific bequest of stock is subject to a stock split or merger, "
                "the beneficiary may take the new shares."
            ),
            "tags": ["ademption_by_extinction"]
        },
        {
            "title": "Revocation by Physical Act",
            "content": (
                "A will may be revoked by burning, tearing, canceling, or obliterating "
                "with the intent to revoke."
            ),
            "tags": ["revocation_express_implied"]
        },
        {
            "title": "Integration: Extrinsic Evidence",
            "content": (
                "Extrinsic evidence is admissible to show which pages were present at "
                "execution and intended to be part of the will."
            ),
            "tags": ["integration_incorporation_by_reference"]
        },
        {
            "title": "Venue: Multiple States",
            "content": (
                "If property is located in multiple states, ancillary proceedings may "
                "be necessary in each state."
            ),
            "tags": ["venue_and_jurisdiction"]
        },
        {
            "title": "Community Property: Transmutation",
            "content": (
                "Spouses may change the character of property by express agreement, "
                "affecting elective share rights."
            ),
            "tags": ["elective_share_and_community_property"]
        },
        {
            "title": "No-Contest Clause: Scope",
            "content": (
                "A no-contest clause may apply to direct and indirect challenges, "
                "depending on will language and state law."
            ),
            "tags": ["no_contest_clause_enforceability"]
        },
        {
            "title": "Advancements: Proof of Intent",
            "content": (
                "A writing or contemporaneous evidence is required to prove a lifetime "
                "gift was intended as an advancement."
            ),
            "tags": ["advancements_and_satisfaction"]
        },
        {
            "title": "Statute of Limitations: Discovery Rule",
            "content": (
                "The discovery rule may delay the start of the limitations period until "
                "the contestant knew or should have known of the grounds."
            ),
            "tags": ["statute_of_limitations"]
        },
    ]
    for doc in docs:
        index.add_document(doc["title"], doc["content"], doc["tags"])