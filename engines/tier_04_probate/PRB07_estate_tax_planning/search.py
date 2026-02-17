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
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in set(tokens):
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            idf = self._compute_idf(term)
            freq = tf.get(term, 0)
            numerator = freq * (self._bm25_k1 + 1)
            denominator = freq + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator if denominator > 0 else 0.0
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            term_tf = tf.get(term, 0) / doc_len if doc_len > 0 else 0.0
            idf = self._compute_idf(term)
            score += term_tf * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0.0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            return content[:length] + ('...' if len(content) > length else '')
        start = max(indices[0] - 10, 0)
        end = min(indices[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:length] + ('...' if len(snippet) > length else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq)
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

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Gross Estate Inclusion",
            "All property owned at death is included in the gross estate under IRC §2031, including real estate, stocks, bonds, business interests, and tangible assets.",
            ["gross_estate_inclusion", "IRC_2031"], 1.0
        ),
        SearchDocument(
            2,
            "Unified Credit & Lifetime Exemption",
            "The unified credit offsets estate and gift tax liability, allowing a lifetime exemption (currently $12.92 million in 2023) under IRC §2010.",
            ["unified_credit_lifetime_exemption", "IRC_2010"], 1.0
        ),
        SearchDocument(
            3,
            "Annual Gift Exclusion",
            "The annual gift exclusion permits gifts up to $17,000 per recipient per year without gift tax, under IRC §2503(b).",
            ["annual_gift_exclusion", "IRC_2503"], 1.0
        ),
        SearchDocument(
            4,
            "Marital Deduction",
            "Transfers to a surviving spouse are deductible from the gross estate, provided the spouse is a U.S. citizen, under IRC §2056.",
            ["marital_deduction", "IRC_2056"], 1.0
        ),
        SearchDocument(
            5,
            "Charitable Deduction",
            "Bequests to qualifying charities are fully deductible from the gross estate under IRC §2055, reducing estate tax liability.",
            ["charitable_deduction", "IRC_2055"], 1.0
        ),
        SearchDocument(
            6,
            "Life Insurance Inclusion",
            "Life insurance proceeds are included in the gross estate if the decedent owned the policy or retained incidents of ownership, per IRC §2042.",
            ["life_insurance_inclusion", "IRC_2042"], 1.0
        ),
        SearchDocument(
            7,
            "Retained Life Estate (IRC §2036)",
            "Property transferred with a retained life estate is included in the gross estate under IRC §2036 if the decedent retained the right to income or enjoyment.",
            ["retained_life_estate_2036", "IRC_2036"], 1.0
        ),
        SearchDocument(
            8,
            "Revocable Transfers (IRC §2038)",
            "Assets subject to the decedent's power to alter, amend, revoke, or terminate are included in the gross estate under IRC §2038.",
            ["revocable_transfers_2038", "IRC_2038"], 1.0
        ),
        SearchDocument(
            9,
            "Generation-Skipping Transfer Tax (GSTT)",
            "GSTT applies to transfers to skip persons (e.g., grandchildren) and is imposed in addition to estate or gift tax under IRC §2601.",
            ["generation_skipping_transfer_tax", "IRC_2601"], 1.0
        ),
        SearchDocument(
            10,
            "Special Use Valuation (IRC §2032A)",
            "Family farms or businesses may be valued based on actual use rather than fair market value under IRC §2032A, reducing estate tax.",
            ["special_use_valuation_2032A", "IRC_2032A"], 1.0
        ),
        SearchDocument(
            11,
            "Qualified Personal Residence Trust (QPRT)",
            "A QPRT allows a grantor to transfer a residence to a trust, retaining use for a term. The value transferred is discounted for gift tax purposes.",
            ["QPRT_qualified_personal_residence_trust"], 1.0
        ),
        SearchDocument(
            12,
            "Grantor Retained Annuity Trust (GRAT)",
            "A GRAT is an irrevocable trust where the grantor retains the right to fixed annuity payments; remainder passes to beneficiaries at a reduced gift tax value.",
            ["GRAT_grantor_retained_annuity_trust"], 1.0
        ),
        SearchDocument(
            13,
            "Family Limited Partnership Valuation Discounts",
            "FLPs may offer valuation discounts for lack of marketability and minority interests, reducing taxable estate value.",
            ["family_limited_partnership_valuation_discounts"], 1.0
        ),
        SearchDocument(
            14,
            "Portability Election (DSUE)",
            "The surviving spouse may elect to use the deceased spouse's unused exemption (DSUE) by filing Form 706, increasing their own exemption.",
            ["portability_election_DSUE"], 1.0
        ),
        SearchDocument(
            15,
            "Stepped-Up Basis (IRC §1014)",
            "Assets receive a stepped-up basis to fair market value at death, minimizing capital gains tax for heirs under IRC §1014.",
            ["stepped_up_basis_IRC_1014", "IRC_1014"], 1.0
        ),
        SearchDocument(
            16,
            "Disclaimers (IRC §2518)",
            "Qualified disclaimers allow beneficiaries to refuse inherited property, enabling tax-efficient redistribution under IRC §2518.",
            ["disclaimers_IRC_2518", "IRC_2518"], 1.0
        ),
        SearchDocument(
            17,
            "Inadequate Consideration (IRC §2043)",
            "Transfers for less than full and adequate consideration may be included in the gross estate under IRC §2043.",
            ["inadequate_consideration_2043", "IRC_2043"], 1.0
        ),
        SearchDocument(
            18,
            "Powers of Appointment (IRC §2041)",
            "Property subject to a general power of appointment held by the decedent is included in the gross estate under IRC §2041.",
            ["powers_of_appointment_IRC_2041", "IRC_2041"], 1.0
        ),
        SearchDocument(
            19,
            "Deathbed Transfers (IRC §2035)",
            "Certain gifts made within three years of death are included in the gross estate under IRC §2035, including life insurance transfers.",
            ["deathbed_transfers_IRC_2035", "IRC_2035"], 1.0
        ),
        SearchDocument(
            20,
            "Alternate Valuation (IRC §2032)",
            "The executor may elect alternate valuation, valuing assets six months after death, if it lowers estate tax under IRC §2032.",
            ["alternate_valuation_IRC_2032", "IRC_2032"], 1.0
        ),
        SearchDocument(
            21,
            "Charitable Lead Trust (IRC §2522)",
            "A CLT provides income to charity for a term, with remainder to heirs. The charitable deduction is calculated under IRC §2522.",
            ["charitable_lead_trust_IRC_2522", "IRC_2522"], 1.0
        ),
        SearchDocument(
            22,
            "Minority Discount Valuation",
            "Minority interests in closely held entities may be valued at a discount, reflecting lack of control and marketability.",
            ["minority_discount_valuation"], 1.0
        ),
        SearchDocument(
            23,
            "Marketability Discount Valuation",
            "Lack of marketability discounts reduce the value of illiquid assets for estate tax purposes, especially in family entities.",
            ["marketability_discount_valuation"], 1.0
        ),
        SearchDocument(
            24,
            "Defined Value Formula Clause",
            "Defined value clauses allocate assets based on IRS-determined values, limiting gift or estate tax exposure.",
            ["defined_value_formula_clause"], 1.0
        ),
        SearchDocument(
            25,
            "Estate Freeze (IRC §2701)",
            "Estate freeze techniques (e.g., preferred equity) lock in asset values for senior family members, shifting appreciation to heirs under IRC §2701.",
            ["estate_freeze_IRC_2701", "IRC_2701"], 1.0
        ),
        SearchDocument(
            26,
            "Installment Sale to Grantor Trust",
            "An installment sale to a grantor trust allows appreciation to pass to heirs, freezing estate value while avoiding recognition of gain.",
            ["installment_sale_to_grantor_trust"], 1.0
        ),
        SearchDocument(
            27,
            "IRC §2031 - Gross Estate Definition",
            "IRC §2031 defines the gross estate as all property, real or personal, tangible or intangible, wherever situated, owned at death.",
            ["gross_estate_inclusion", "IRC_2031"], 0.9
        ),
        SearchDocument(
            28,
            "Form 706 - Estate Tax Return",
            "Form 706 is used to report the gross estate, deductions, and calculate estate tax, including elections for portability and alternate valuation.",
            ["estate_tax_return", "portability_election_DSUE", "alternate_valuation_IRC_2032"], 1.0
        ),
        SearchDocument(
            29,
            "IRC §2503(b) - Annual Gift Exclusion Details",
            "IRC §2503(b) provides the annual exclusion for gifts of present interest, currently $17,000 per donee per year.",
            ["annual_gift_exclusion", "IRC_2503"], 0.9
        ),
        SearchDocument(
            30,
            "IRC §2056 - Marital Deduction Requirements",
            "IRC §2056 allows deduction for property passing to a surviving spouse, subject to QTIP trust rules and citizenship requirements.",
            ["marital_deduction", "IRC_2056"], 0.9
        ),
        SearchDocument(
            31,
            "IRC §2055 - Charitable Deduction Examples",
            "IRC §2055 permits deduction for bequests to qualifying charities, including public charities and private foundations.",
            ["charitable_deduction", "IRC_2055"], 0.9
        ),
        SearchDocument(
            32,
            "IRC §2042 - Life Insurance Estate Inclusion",
            "IRC §2042 includes life insurance proceeds in the estate if the decedent retained incidents of ownership or transferred within three years.",
            ["life_insurance_inclusion", "deathbed_transfers_IRC_2035", "IRC_2042"], 0.9
        ),
        SearchDocument(
            33,
            "IRC §2036 - Retained Life Estate Examples",
            "IRC §2036 includes property in the estate if the decedent retained income, enjoyment, or control over the transferred asset.",
            ["retained_life_estate_2036", "IRC_2036"], 0.9
        ),
        SearchDocument(
            34,
            "IRC §2038 - Revocable Transfers Explained",
            "IRC §2038 includes assets subject to the decedent's power to revoke or amend, even if not exercised.",
            ["revocable_transfers_2038", "IRC_2038"], 0.9
        ),
        SearchDocument(
            35,
            "IRC §2601 - Generation-Skipping Transfer Tax",
            "IRC §2601 imposes GSTT on transfers to skip persons, with exemptions and exclusions similar to estate and gift tax.",
            ["generation_skipping_transfer_tax", "IRC_2601"], 0.9
        ),
        SearchDocument(
            36,
            "IRC §2032A - Special Use Valuation Application",
            "IRC §2032A allows family farms and businesses to be valued based on actual use, subject to strict eligibility requirements.",
            ["special_use_valuation_2032A", "IRC_2032A"], 0.9
        ),
        SearchDocument(
            37,
            "QPRT - Qualified Personal Residence Trust Mechanics",
            "A QPRT removes a residence from the estate by transferring it to a trust, with the grantor retaining occupancy for a set term.",
            ["QPRT_qualified_personal_residence_trust"], 0.9
        ),
        SearchDocument(
            38,
            "GRAT - Grantor Retained Annuity Trust Structure",
            "A GRAT provides annuity payments to the grantor, with the remainder passing to heirs at a discounted gift tax value.",
            ["GRAT_grantor_retained_annuity_trust"], 0.9
        ),
        SearchDocument(
            39,
            "FLP - Family Limited Partnership Valuation Discounts",
            "Family limited partnerships enable valuation discounts for minority interests and lack of marketability, reducing estate tax.",
            ["family_limited_partnership_valuation_discounts"], 0.9
        ),
        SearchDocument(
            40,
            "DSUE - Portability Election Process",
            "The DSUE allows a surviving spouse to use the deceased spouse's unused exemption by timely filing Form 706.",
            ["portability_election_DSUE"], 0.9
        ),
        SearchDocument(
            41,
            "IRC §1014 - Stepped-Up Basis Effects",
            "IRC §1014 provides a stepped-up basis for inherited assets, reducing capital gains tax for beneficiaries.",
            ["stepped_up_basis_IRC_1014", "IRC_1014"], 0.9
        ),
        SearchDocument(
            42,
            "IRC §2518 - Qualified Disclaimers",
            "IRC §2518 allows beneficiaries to disclaim inherited property, provided the disclaimer is irrevocable and timely.",
            ["disclaimers_IRC_2518", "IRC_2518"], 0.9
        ),
        SearchDocument(
            43,
            "IRC §2043 - Inadequate Consideration Transfers",
            "IRC §2043 includes property in the estate if transferred for less than full and adequate consideration.",
            ["inadequate_consideration_2043", "IRC_2043"], 0.9
        ),
        SearchDocument(
            44,
            "IRC §2041 - Powers of Appointment",
            "IRC §2041 includes property subject to a general power of appointment in the gross estate.",
            ["powers_of_appointment_IRC_2041", "IRC_2041"], 0.9
        ),
        SearchDocument(
            45,
            "IRC §2035 - Deathbed Transfers",
            "IRC §2035 includes certain gifts made within three years of death, including life insurance, in the gross estate.",
            ["deathbed_transfers_IRC_2035", "IRC_2035"], 0.9
        ),
        SearchDocument(
            46,
            "IRC §2032 - Alternate Valuation Election",
            "IRC §2032 allows alternate valuation six months after death if it reduces estate tax.",
            ["alternate_valuation_IRC_2032", "IRC_2032"], 0.9
        ),
        SearchDocument(
            47,
            "IRC §2522 - Charitable Lead Trust Deduction",
            "IRC §2522 provides a deduction for charitable lead trusts, calculated based on present value of income stream to charity.",
            ["charitable_lead_trust_IRC_2522", "IRC_2522"], 0.9
        ),
        SearchDocument(
            48,
            "Minority Discount Valuation in Estate Planning",
            "Minority discounts reflect lack of control in closely held entities, reducing estate tax value.",
            ["minority_discount_valuation"], 0.9
        ),
        SearchDocument(
            49,
            "Marketability Discount Valuation in FLPs",
            "Marketability discounts apply to illiquid assets, such as family limited partnership interests.",
            ["marketability_discount_valuation"], 0.9
        ),
        SearchDocument(
            50,
            "Defined Value Formula Clause Examples",
            "Defined value clauses allocate assets based on IRS-determined values, protecting against gift or estate tax adjustments.",
            ["defined_value_formula_clause"], 0.9
        ),
        SearchDocument(
            51,
            "Estate Freeze Techniques (IRC §2701)",
            "Estate freeze strategies shift future appreciation to heirs, using preferred equity or GRATs under IRC §2701.",
            ["estate_freeze_IRC_2701", "GRAT_grantor_retained_annuity_trust", "IRC_2701"], 0.9
        ),
        SearchDocument(
            52,
            "Installment Sale to Grantor Trust Advantages",
            "Installment sales to grantor trusts freeze estate value, allowing appreciation to pass to heirs without immediate income tax.",
            ["installment_sale_to_grantor_trust"], 0.9
        ),
    ]
    for doc in docs:
        idx.add_document(doc)