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
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.id_counter = 1

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r"\b\w+\b", text.lower())
        return tokens

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self.lock:
            doc_id = self.id_counter
            self.id_counter += 1
            doc = SearchDocument(doc_id, title, content, tags, weight)
            self.documents[doc_id] = doc
            tokens = self._tokenize(content)
            self.doc_lengths[doc_id] = len(tokens)
            self.term_freqs[doc_id] = Counter(tokens)
            for term in set(tokens):
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0
            return doc_id

    def _compute_idf(self, term: str) -> float:
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            idf = self._compute_idf(term)
            numerator = freq * (k1 + 1)
            denominator = freq + k1 * (1 - b + b * (doc_length / avg_dl))
            score += idf * (numerator / denominator)
        return score * self.documents[doc_id].weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:window])
        else:
            start = max(positions[0] - window // 2, 0)
            end = min(start + window, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq)
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
            "title": "Fair Market Value Standard in Estate Valuation",
            "content": "Fair market value is defined as the price at which property would change hands between a willing buyer and seller, neither being under any compulsion to buy or sell and both having reasonable knowledge of relevant facts. This standard is central to estate tax valuation.",
            "tags": ["fair_market_value_standard"],
            "weight": 1.0
        },
        {
            "title": "Alternate Valuation Date under IRC 2032",
            "content": "IRC Section 2032 allows estates to elect an alternate valuation date, six months after the decedent's death, if it reduces estate tax liability. Property values are determined as of this date, subject to eligibility criteria.",
            "tags": ["alternate_valuation_date_irc_2032"],
            "weight": 1.0
        },
        {
            "title": "Special Use Valuation for Real Property (IRC 2032A)",
            "content": "IRC 2032A provides special use valuation for qualified real property used in farming or closely held businesses, allowing valuation based on actual use rather than highest and best use, subject to strict requirements.",
            "tags": ["special_use_valuation_irc_2032a", "real_property_appraisal_methods"],
            "weight": 1.0
        },
        {
            "title": "Real Property Appraisal Methods",
            "content": "Appraisal methods for real property include the sales comparison approach, income capitalization, and cost approach. Each method is selected based on property type and market conditions.",
            "tags": ["real_property_appraisal_methods"],
            "weight": 1.0
        },
        {
            "title": "Mineral Rights Valuation in Estates",
            "content": "Mineral rights are valued based on reserves, production history, market prices, and lease terms. Appraisals may require geological reports and income projections.",
            "tags": ["mineral_rights_valuation"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Closely Held Businesses",
            "content": "Closely held business interests are valued using income, market, and asset approaches. Discounts for lack of marketability and minority interest may apply.",
            "tags": ["closely_held_business_valuation", "lack_of_marketability_discount", "minority_interest_discount"],
            "weight": 1.0
        },
        {
            "title": "Securities Valuation for Estate Purposes",
            "content": "Publicly traded securities are valued at their mean trading price on the valuation date. Thinly traded or restricted securities require appraisal and may be subject to discounts.",
            "tags": ["securities_valuation"],
            "weight": 1.0
        },
        {
            "title": "Life Insurance Proceeds in Estate Valuation",
            "content": "Life insurance proceeds are included in the estate if the decedent possessed incidents of ownership. The value is generally the face amount payable at death.",
            "tags": ["life_insurance_proceeds"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Retirement Accounts",
            "content": "Retirement accounts such as IRAs and 401(k)s are valued at their fair market value as of the date of death. Tax implications may affect net estate value.",
            "tags": ["retirement_accounts_valuation"],
            "weight": 1.0
        },
        {
            "title": "Personal Property Inventory and Valuation",
            "content": "Personal property, including art, jewelry, and collectibles, must be inventoried and appraised. Qualified appraisers are required for high-value items.",
            "tags": ["personal_property_inventory", "qualified_appraisal_requirements"],
            "weight": 1.0
        },
        {
            "title": "Debts and Liabilities in Estate Valuation",
            "content": "Debts and liabilities are deducted from the gross estate to determine the taxable estate. Proper documentation and substantiation are required.",
            "tags": ["debts_and_liabilities"],
            "weight": 1.0
        },
        {
            "title": "Lack of Marketability Discount",
            "content": "A lack of marketability discount reflects the reduced value of assets that cannot be readily sold or transferred. This is commonly applied to closely held business interests.",
            "tags": ["lack_of_marketability_discount"],
            "weight": 1.0
        },
        {
            "title": "Minority Interest Discount in Estate Valuation",
            "content": "Minority interest discounts are applied to ownership interests that lack control over business decisions. The discount rate depends on the degree of control and marketability.",
            "tags": ["minority_interest_discount"],
            "weight": 1.0
        },
        {
            "title": "Qualified Appraisal Requirements",
            "content": "IRS regulations require qualified appraisals for certain estate assets. Appraisers must meet educational and experience standards and provide detailed reports.",
            "tags": ["qualified_appraisal_requirements"],
            "weight": 1.0
        },
        {
            "title": "Fractional Interest in Real Estate",
            "content": "Fractional interests in real estate are valued based on their proportionate share and may be subject to discounts for lack of control and marketability.",
            "tags": ["fractional_interest_real_estate", "lack_of_marketability_discount", "minority_interest_discount"],
            "weight": 1.0
        },
        {
            "title": "Environmental Contamination Impact on Valuation",
            "content": "Environmental contamination can significantly reduce real property value. Appraisers must consider remediation costs and regulatory compliance.",
            "tags": ["environmental_contamination_impact", "real_property_appraisal_methods"],
            "weight": 1.0
        },
        {
            "title": "Buy-Sell Agreement Valuation",
            "content": "Buy-sell agreements may establish the value of business interests for estate purposes. The IRS may disregard values not reflecting fair market value.",
            "tags": ["buy_sell_agreement_valuation", "closely_held_business_valuation"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Farm Property",
            "content": "Farm property may qualify for special use valuation under IRC 2032A. The value is based on actual agricultural use rather than development potential.",
            "tags": ["special_use_valuation_irc_2032a", "real_property_appraisal_methods"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Oil and Gas Interests",
            "content": "Oil and gas interests are valued based on production, reserves, lease terms, and market prices. Specialized appraisals may be required.",
            "tags": ["mineral_rights_valuation"],
            "weight": 1.0
        },
        {
            "title": "Valuing Restricted Stock in Estates",
            "content": "Restricted stock is valued based on trading restrictions, market conditions, and potential discounts for lack of marketability.",
            "tags": ["securities_valuation", "lack_of_marketability_discount"],
            "weight": 1.0
        },
        {
            "title": "Estate Tax Implications of Retirement Accounts",
            "content": "Retirement account values are included in the gross estate. Taxable distributions may affect net value and estate tax liability.",
            "tags": ["retirement_accounts_valuation"],
            "weight": 1.0
        },
        {
            "title": "Inventorying Household Goods for Estate Valuation",
            "content": "Household goods must be inventoried and valued at fair market value. Appraisals may be required for antiques and collectibles.",
            "tags": ["personal_property_inventory", "qualified_appraisal_requirements"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Partnership Interests",
            "content": "Partnership interests are valued based on income, asset, and market approaches. Discounts for lack of marketability and minority interest may apply.",
            "tags": ["closely_held_business_valuation", "lack_of_marketability_discount", "minority_interest_discount"],
            "weight": 1.0
        },
        {
            "title": "Impact of Environmental Liabilities on Estate Valuation",
            "content": "Environmental liabilities, such as contamination or remediation obligations, can reduce estate asset values and must be considered in appraisals.",
            "tags": ["environmental_contamination_impact", "debts_and_liabilities"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Art and Collectibles",
            "content": "Art and collectibles are valued based on recent sales, expert appraisals, and market trends. IRS requires qualified appraisals for high-value items.",
            "tags": ["personal_property_inventory", "qualified_appraisal_requirements"],
            "weight": 1.0
        },
        {
            "title": "Valuing Life Insurance Policies Held in Trust",
            "content": "Life insurance policies held in trust may be included in the estate if the decedent retained incidents of ownership. Valuation is based on policy proceeds.",
            "tags": ["life_insurance_proceeds"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Stock Options",
            "content": "Stock options are valued based on exercise price, market value, vesting schedule, and restrictions. Specialized appraisals may be required.",
            "tags": ["securities_valuation"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Debt Instruments in Estates",
            "content": "Debt instruments, such as promissory notes and bonds, are valued at their present value, considering interest rates and payment terms.",
            "tags": ["debts_and_liabilities"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Real Estate with Environmental Issues",
            "content": "Real estate affected by environmental issues may require specialized appraisal, considering remediation costs and regulatory compliance.",
            "tags": ["environmental_contamination_impact", "real_property_appraisal_methods"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Fractional Interests in Commercial Property",
            "content": "Fractional interests in commercial property are valued based on their share of income and asset value, subject to discounts for lack of control.",
            "tags": ["fractional_interest_real_estate", "lack_of_marketability_discount", "minority_interest_discount"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Mineral Leases",
            "content": "Mineral leases are valued based on lease terms, production history, and market prices. Appraisals may require expert reports.",
            "tags": ["mineral_rights_valuation"],
            "weight": 1.0
        },
        {
            "title": "Buy-Sell Agreements and Estate Valuation",
            "content": "Buy-sell agreements may establish business interest values for estate purposes, but must reflect fair market value to be accepted by the IRS.",
            "tags": ["buy_sell_agreement_valuation", "closely_held_business_valuation"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Qualified Retirement Plans",
            "content": "Qualified retirement plans are valued at their account balance as of the date of death. Taxation of distributions may affect net estate value.",
            "tags": ["retirement_accounts_valuation"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Business Interests Subject to Buy-Sell Agreements",
            "content": "Business interests subject to buy-sell agreements are valued based on agreement terms, but must meet fair market value standards for estate tax purposes.",
            "tags": ["buy_sell_agreement_valuation", "closely_held_business_valuation"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Contaminated Properties",
            "content": "Contaminated properties are valued considering remediation costs, regulatory compliance, and market impact. Specialized appraisals may be required.",
            "tags": ["environmental_contamination_impact", "real_property_appraisal_methods"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Minority Business Interests",
            "content": "Minority business interests are valued with discounts for lack of control and marketability, based on industry standards and appraisal methods.",
            "tags": ["minority_interest_discount", "lack_of_marketability_discount", "closely_held_business_valuation"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Real Property with Special Use",
            "content": "Real property used for farming or business may qualify for special use valuation under IRC 2032A, reducing estate tax liability.",
            "tags": ["special_use_valuation_irc_2032a", "real_property_appraisal_methods"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Securities with Limited Market",
            "content": "Securities with limited market are valued based on trading restrictions, market conditions, and applicable discounts for lack of marketability.",
            "tags": ["securities_valuation", "lack_of_marketability_discount"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Personal Property Collections",
            "content": "Personal property collections, such as coins or stamps, are valued based on recent sales, expert appraisals, and market trends.",
            "tags": ["personal_property_inventory", "qualified_appraisal_requirements"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Debts and Liabilities in Estates",
            "content": "Debts and liabilities, including mortgages and loans, are deducted from the gross estate to determine taxable estate value.",
            "tags": ["debts_and_liabilities"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Life Insurance with Cash Value",
            "content": "Life insurance policies with cash value are valued based on the policy's cash surrender value at the date of death.",
            "tags": ["life_insurance_proceeds"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Real Estate with Fractional Ownership",
            "content": "Fractional ownership in real estate is valued based on its share of income and asset value, subject to discounts for lack of control and marketability.",
            "tags": ["fractional_interest_real_estate", "lack_of_marketability_discount", "minority_interest_discount"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Environmental Remediation Obligations",
            "content": "Environmental remediation obligations can reduce estate asset values and must be considered in appraisals.",
            "tags": ["environmental_contamination_impact", "debts_and_liabilities"],
            "weight": 1.0
        },
        {
            "title": "Qualified Appraisal Standards for Estate Assets",
            "content": "Qualified appraisals must meet IRS standards, including detailed reporting, appraiser credentials, and valuation methodologies.",
            "tags": ["qualified_appraisal_requirements"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Business Interests with Buy-Sell Agreements",
            "content": "Business interests with buy-sell agreements are valued based on agreement terms, but must reflect fair market value for estate tax purposes.",
            "tags": ["buy_sell_agreement_valuation", "closely_held_business_valuation"],
            "weight": 1.0
        },
        {
            "title": "Valuation of Mineral Rights with Lease Income",
            "content": "Mineral rights with lease income are valued based on lease terms, production history, and market prices.",
            "tags": ["mineral_rights_valuation"],
            "weight": 1.0
        },
        {
            "title": "Estate Valuation of Real Property with Environmental Concerns",
            "content": "Real property with environmental concerns is valued considering remediation costs, regulatory compliance, and market impact.",
            "tags": ["environmental_contamination_impact", "real_property_appraisal_methods"],
            "weight": 1.0
        }
    ]
    for doc in docs:
        idx.add_document(doc["title"], doc["content"], doc["tags"], doc["weight"])