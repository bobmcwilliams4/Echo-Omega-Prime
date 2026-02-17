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
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._doc_id_seq = 1

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self.lock:
            doc_id = self._doc_id_seq
            self._doc_id_seq += 1
            doc = SearchDocument(doc_id, title, content, tags, weight)
            self.documents[doc_id] = doc
            tokens = self._tokenize(content)
            self.doc_lengths[doc_id] = len(tokens)
            self.term_freqs[doc_id] = Counter(tokens)
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            self._update_avg_doc_length()
            self.idf_cache.clear()
            return doc_id

    def _update_avg_doc_length(self):
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)
        else:
            self.avg_doc_length = 0.0

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            term_tf = tf.get(term, 0)
            if term_tf == 0:
                continue
            norm_tf = term_tf / doc_len
            idf = self._compute_idf(term)
            score += norm_tf * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if positions:
            start = max(positions[0] - 5, 0)
            end = min(positions[0] + 15, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
            for term in query_terms:
                snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
            return snippet
        else:
            return content[:160] + ('...' if len(content) > 160 else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'num_unique_terms': len(self.term_doc_freq),
        }

# Singleton factory for SearchIndex
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
        {
            "title": "Will Validity: Formalities Required",
            "content": "A valid will must be in writing, signed by the testator, and witnessed by two credible persons. Failure to comply with statutory formalities may render the will invalid.",
            "tags": ["will_validity_formalities"]
        },
        {
            "title": "Testamentary Capacity: Legal Standards",
            "content": "Testamentary capacity requires that the testator understands the nature of the act, the property disposed of, and the natural objects of their bounty.",
            "tags": ["testamentary_capacity"]
        },
        {
            "title": "Intestate Succession Hierarchy",
            "content": "When a person dies without a will, their estate passes according to the intestate succession hierarchy: spouse, children, parents, siblings, and more remote kin.",
            "tags": ["intestate_succession_hierarchy"]
        },
        {
            "title": "Homestead Exemption in Probate",
            "content": "The homestead exemption protects the decedent's primary residence from certain creditor claims and ensures surviving family members retain occupancy rights.",
            "tags": ["homestead_exemption_probate"]
        },
        {
            "title": "Independent Administration of Estates",
            "content": "Independent administration allows the executor to manage the estate without court supervision, streamlining probate and reducing costs.",
            "tags": ["independent_administration"]
        },
        {
            "title": "Grounds for Will Contest",
            "content": "Will contests may be based on undue influence, fraud, duress, lack of capacity, or improper execution. Evidence must support the alleged grounds.",
            "tags": ["will_contest_grounds"]
        },
        {
            "title": "Creditor Claims Priority in Probate",
            "content": "Creditor claims are paid in a statutory order: funeral expenses, administration costs, secured debts, taxes, and unsecured claims.",
            "tags": ["creditor_claims_priority"]
        },
        {
            "title": "Elective Share and Spousal Rights",
            "content": "A surviving spouse may claim an elective share of the estate, overriding the will's provisions to ensure minimum inheritance.",
            "tags": ["elective_share_spousal_rights"]
        },
        {
            "title": "Executor's Fiduciary Duties",
            "content": "Executors must act in good faith, avoid self-dealing, account for assets, and distribute property according to the will or law.",
            "tags": ["executor_fiduciary_duties"]
        },
        {
            "title": "Pour-Over Will and Trust Integration",
            "content": "A pour-over will directs assets into a living trust upon death, integrating probate and trust administration for seamless estate management.",
            "tags": ["pour_over_will_trust_integration"]
        },
        {
            "title": "Muniment of Title Proceedings",
            "content": "Muniment of title allows probate of a will without administration when there are no debts, providing clear title to heirs.",
            "tags": ["muniment_of_title"]
        },
        {
            "title": "Ademption and Abatement of Gifts",
            "content": "Ademption occurs when a specific bequest is no longer in the estate. Abatement reduces gifts proportionally if assets are insufficient.",
            "tags": ["ademption_abatement"]
        },
        {
            "title": "Will Interpretation and Testator's Intent",
            "content": "Courts interpret wills to ascertain the testator's intent, considering the language, circumstances, and extrinsic evidence if ambiguous.",
            "tags": ["will_interpretation_intent"]
        },
        {
            "title": "Heirship Determination in Probate",
            "content": "Heirship proceedings establish heirs when no will exists, relying on testimony and statutory presumptions to determine succession.",
            "tags": ["heirship_determination"]
        },
        {
            "title": "Anti-Lapse Statute in Will Construction",
            "content": "Anti-lapse statutes preserve gifts to deceased beneficiaries by passing them to their descendants, preventing unintended disinheritance.",
            "tags": ["anti_lapse_statute"]
        },
        {
            "title": "Small Estate Affidavit Procedure",
            "content": "A small estate affidavit expedites transfer of assets when the estate value is below statutory thresholds and no administration is needed.",
            "tags": ["small_estate_affidavit"]
        },
        {
            "title": "Witness Requirements for Will Execution",
            "content": "Wills must be witnessed by two credible individuals who observe the testator's signature and attest to the document's authenticity.",
            "tags": ["will_validity_formalities"]
        },
        {
            "title": "Undue Influence in Will Contests",
            "content": "Undue influence is proven by showing that the testator's free will was overcome by another, resulting in an unnatural disposition.",
            "tags": ["will_contest_grounds"]
        },
        {
            "title": "Fraud and Duress in Probate",
            "content": "Fraud or duress invalidates a will if the testator was deceived or coerced into executing the instrument.",
            "tags": ["will_contest_grounds"]
        },
        {
            "title": "Lost Wills and Probate",
            "content": "A lost will may be admitted to probate if its contents and proper execution are proven by clear and convincing evidence.",
            "tags": ["will_validity_formalities"]
        },
        {
            "title": "Revocation of Wills",
            "content": "Wills can be revoked by physical destruction, executing a new will, or by express written revocation.",
            "tags": ["will_validity_formalities"]
        },
        {
            "title": "Partial Intestacy",
            "content": "If a will fails to dispose of all assets, the undisposed property passes by intestate succession.",
            "tags": ["intestate_succession_hierarchy"]
        },
        {
            "title": "Homestead Rights of Surviving Spouse",
            "content": "The surviving spouse retains homestead rights, including occupancy and protection from certain creditors, regardless of will provisions.",
            "tags": ["homestead_exemption_probate"]
        },
        {
            "title": "Notice to Creditors in Probate",
            "content": "Executors must provide notice to known and unknown creditors, allowing them to present claims within statutory deadlines.",
            "tags": ["creditor_claims_priority"]
        },
        {
            "title": "Fiduciary Duty Breach Remedies",
            "content": "Beneficiaries may seek removal of an executor or damages for breach of fiduciary duty, including mismanagement or self-dealing.",
            "tags": ["executor_fiduciary_duties"]
        },
        {
            "title": "Spousal Election Against the Will",
            "content": "A spouse may elect to take a statutory share, rejecting the will's terms, to protect marital property rights.",
            "tags": ["elective_share_spousal_rights"]
        },
        {
            "title": "Integration of Pour-Over Will and Trust",
            "content": "A pour-over will ensures probate assets are transferred to a trust, facilitating unified estate administration.",
            "tags": ["pour_over_will_trust_integration"]
        },
        {
            "title": "Muniment of Title: Requirements",
            "content": "Muniment of title is available when the decedent left a valid will, there are no unpaid debts, and heirs seek title transfer.",
            "tags": ["muniment_of_title"]
        },
        {
            "title": "Ademption: Specific Bequests",
            "content": "Ademption applies when a specifically bequeathed asset is not part of the estate at death, resulting in the gift's failure.",
            "tags": ["ademption_abatement"]
        },
        {
            "title": "Abatement: Order of Reduction",
            "content": "If estate assets are insufficient, gifts abate in a statutory order: residuary, general, and specific bequests.",
            "tags": ["ademption_abatement"]
        },
        {
            "title": "Will Construction: Ambiguities",
            "content": "Ambiguous will provisions may be clarified by extrinsic evidence to effectuate the testator's intent.",
            "tags": ["will_interpretation_intent"]
        },
        {
            "title": "Heirship Determination: Evidence",
            "content": "Heirship is proven by testimony, family records, and statutory presumptions regarding kinship and descent.",
            "tags": ["heirship_determination"]
        },
        {
            "title": "Anti-Lapse: Descendant Substitution",
            "content": "Anti-lapse statutes substitute descendants for deceased beneficiaries, preserving gifts within the family.",
            "tags": ["anti_lapse_statute"]
        },
        {
            "title": "Small Estate Affidavit: Eligibility",
            "content": "Eligibility for a small estate affidavit requires the estate's value to be below statutory limits and absence of administration.",
            "tags": ["small_estate_affidavit"]
        },
        {
            "title": "Testamentary Capacity: Mental Disorders",
            "content": "Mental disorders do not necessarily preclude testamentary capacity if the testator understands the will's nature and effect.",
            "tags": ["testamentary_capacity"]
        },
        {
            "title": "Creditor Claims: Statute of Limitations",
            "content": "Claims against the estate must be presented within statutory deadlines or are barred from recovery.",
            "tags": ["creditor_claims_priority"]
        },
        {
            "title": "Executor's Duty: Inventory and Accounting",
            "content": "The executor must file an inventory of estate assets and provide regular accountings to beneficiaries and the court.",
            "tags": ["executor_fiduciary_duties"]
        },
        {
            "title": "Pour-Over Will: Trust Funding",
            "content": "A pour-over will funds a trust with probate assets, ensuring unified management and distribution.",
            "tags": ["pour_over_will_trust_integration"]
        },
        {
            "title": "Muniment of Title: No Administration",
            "content": "Muniment of title is used when no administration is required, streamlining title transfer to heirs.",
            "tags": ["muniment_of_title"]
        },
        {
            "title": "Ademption: Replacement Property",
            "content": "If a bequeathed asset is replaced, courts may determine whether the replacement qualifies for the gift or ademption applies.",
            "tags": ["ademption_abatement"]
        },
        {
            "title": "Will Interpretation: Precatory Language",
            "content": "Precatory language expresses wishes but does not create enforceable rights unless intent is clear.",
            "tags": ["will_interpretation_intent"]
        },
        {
            "title": "Heirship: Collateral Relatives",
            "content": "Collateral relatives inherit only if direct descendants and parents are absent, following statutory hierarchy.",
            "tags": ["heirship_determination"]
        },
        {
            "title": "Anti-Lapse: Class Gifts",
            "content": "Anti-lapse statutes may apply to class gifts, preserving bequests for surviving class members or their descendants.",
            "tags": ["anti_lapse_statute"]
        },
        {
            "title": "Small Estate Affidavit: Procedure",
            "content": "The affidavit must be sworn by heirs and submitted to the court, enabling asset transfer without formal probate.",
            "tags": ["small_estate_affidavit"]
        },
        {
            "title": "Will Validity: Holographic Wills",
            "content": "Holographic wills, written entirely in the testator's handwriting, are valid if signed and meet statutory requirements.",
            "tags": ["will_validity_formalities"]
        },
        {
            "title": "Testamentary Capacity: Age Requirements",
            "content": "The testator must be at least 18 years old or legally emancipated to execute a valid will.",
            "tags": ["testamentary_capacity"]
        },
        {
            "title": "Intestate Succession: Adopted Children",
            "content": "Adopted children inherit from adoptive parents as natural children, but not from biological parents unless specified.",
            "tags": ["intestate_succession_hierarchy"]
        },
        {
            "title": "Homestead Exemption: Creditor Protection",
            "content": "Homestead property is exempt from most creditor claims, except for mortgages, taxes, and certain liens.",
            "tags": ["homestead_exemption_probate"]
        },
        {
            "title": "Independent Administration: Bond Waiver",
            "content": "Independent executors may serve without posting bond if the will expressly waives the requirement.",
            "tags": ["independent_administration"]
        },
        {
            "title": "Will Contest: Burden of Proof",
            "content": "The contestant bears the burden of proof in challenging a will, requiring clear evidence of invalidity.",
            "tags": ["will_contest_grounds"]
        },
        {
            "title": "Creditor Claims: Priority of Taxes",
            "content": "Estate taxes and government claims are prioritized over unsecured debts in probate distributions.",
            "tags": ["creditor_claims_priority"]
        },
        {
            "title": "Elective Share: Community Property",
            "content": "In community property states, the surviving spouse may claim half of marital assets regardless of will provisions.",
            "tags": ["elective_share_spousal_rights"]
        },
        {
            "title": "Executor's Duty: Asset Distribution",
            "content": "Executors must distribute assets according to the will or intestacy laws, ensuring compliance with court orders.",
            "tags": ["executor_fiduciary_duties"]
        },
        {
            "title": "Pour-Over Will: Trust Amendment",
            "content": "Trusts receiving pour-over assets may be amended before death, affecting the ultimate distribution of estate property.",
            "tags": ["pour_over_will_trust_integration"]
        },
        {
            "title": "Muniment of Title: Title Transfer",
            "content": "Muniment of title proceedings result in court orders transferring title to heirs without administration.",
            "tags": ["muniment_of_title"]
        },
        {
            "title": "Ademption: Partial Ademption",
            "content": "Partial ademption occurs when only part of a bequeathed asset remains, reducing the gift proportionally.",
            "tags": ["ademption_abatement"]
        },
        {
            "title": "Will Interpretation: Extrinsic Evidence",
            "content": "Extrinsic evidence may be admitted to resolve ambiguities and clarify the testator's intent in will construction.",
            "tags": ["will_interpretation_intent"]
        },
        {
            "title": "Heirship: Presumptions of Paternity",
            "content": "Statutory presumptions may establish paternity for inheritance purposes, affecting heirship determination.",
            "tags": ["heirship_determination"]
        },
        {
            "title": "Anti-Lapse: Stepchildren",
            "content": "Anti-lapse statutes may not apply to stepchildren unless expressly included in the will.",
            "tags": ["anti_lapse_statute"]
        },
        {
            "title": "Small Estate Affidavit: Asset Limits",
            "content": "Asset limits for small estate affidavits are set by statute and exclude homestead and exempt property.",
            "tags": ["small_estate_affidavit"]
        }
    ]
    for doc in docs:
        index.add_document(doc["title"], doc["content"], doc["tags"])