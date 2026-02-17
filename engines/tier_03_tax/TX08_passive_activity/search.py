"""
TX08 Passive Activity Loss - Vector Search Fallback
Semantic search when doctrine cache misses
"""

from typing import List, Dict, Any, Optional
import hashlib


class PassiveActivityVectorSearch:
    """Vector search fallback for passive activity queries."""

    def __init__(self, cloud_retriever_available: bool = True):
        self.cloud_retriever_available = cloud_retriever_available
        self.search_index = self._build_search_index()

    def _build_search_index(self) -> Dict[str, Dict[str, Any]]:
        """Build keyword-based search index for passive activity concepts."""
        return {
            "material_participation_500_hours": {
                "keywords": ["500 hours", "test 1", "material participation", "hour requirement"],
                "authority": "Temp. Reg. §1.469-5T(a)(1)",
                "summary": "Taxpayer participates >500 hours during year - most straightforward material participation test.",
                "related_topics": ["hour_substantiation", "operational_vs_investment_work", "spouse_hours_separate"]
            },
            "material_participation_substantially_all": {
                "keywords": ["substantially all", "test 2", "sole operator", "90%"],
                "authority": "Temp. Reg. §1.469-5T(a)(2)",
                "summary": "Taxpayer's participation constitutes substantially all participation (generally 90%+).",
                "related_topics": ["sole_proprietor", "employee_participation_counts"]
            },
            "material_participation_100_hours_not_less": {
                "keywords": ["100 hours", "test 3", "not less than anyone", "equal participation"],
                "authority": "Temp. Reg. §1.469-5T(a)(3)",
                "summary": "Taxpayer participates >100 hours and not less than any other individual.",
                "related_topics": ["comparative_hours", "employee_hours"]
            },
            "significant_participation_activity": {
                "keywords": ["SPA", "test 4", "aggregation", "significant participation", "500 hours total"],
                "authority": "Temp. Reg. §1.469-5T(a)(4)",
                "summary": "Activity is SPA (>100 hours, no material participation) and aggregate SPA hours >500.",
                "related_topics": ["trade_or_business_only", "rental_excluded_from_spa"]
            },
            "material_participation_5_of_10": {
                "keywords": ["5 of 10 years", "test 5", "prior years", "historical participation"],
                "authority": "Temp. Reg. §1.469-5T(a)(5)",
                "summary": "Materially participated in 5 of prior 10 years (any 5, not consecutive).",
                "related_topics": ["retiree_planning", "activity_continuity"]
            },
            "personal_service_activity_3_years": {
                "keywords": ["personal service", "test 6", "3 prior years", "health law engineering"],
                "authority": "Temp. Reg. §1.469-5T(a)(6)",
                "summary": "Personal service activity (health, law, engineering, etc.) + materially participated 3 prior years.",
                "related_topics": ["indefinite_status", "capital_not_material"]
            },
            "facts_and_circumstances": {
                "keywords": ["test 7", "facts and circumstances", "regular continuous substantial", "management limitation"],
                "authority": "Temp. Reg. §1.469-5T(a)(7)",
                "summary": "Regular, continuous, substantial participation, but management participation excluded if others compensated or spend more hours.",
                "related_topics": ["100_hour_floor", "last_resort_test"]
            },
            "rental_per_se_passive": {
                "keywords": ["rental activity", "per se passive", "469(c)(2)", "material participation doesn't apply"],
                "authority": "IRC §469(c)(2)",
                "summary": "Rental activities are per se passive regardless of participation hours (exceptions apply).",
                "related_topics": ["7_day_exception", "30_day_exception", "extraordinary_services"]
            },
            "real_estate_professional": {
                "keywords": ["real estate professional", "REP", "469(c)(7)", "750 hours", "more than half"],
                "authority": "IRC §469(c)(7)",
                "summary": ">50% of services in real property trades/businesses AND >750 hours. Eliminates per se passive for rentals.",
                "related_topics": ["grouping_election", "high_audit_risk", "contemporaneous_logs_critical"]
            },
            "$25k_allowance": {
                "keywords": ["$25,000 allowance", "469(i)", "active participation", "AGI phaseout"],
                "authority": "IRC §469(i)",
                "summary": "Up to $25K rental real estate losses offset non-passive income if actively participated. Phases out $100K-$150K AGI.",
                "related_topics": ["active_vs_material_participation", "10_percent_ownership", "management_decisions"]
            },
            "grouping_of_activities": {
                "keywords": ["grouping", "appropriate economic unit", "Reg 1.469-4", "activity definition"],
                "authority": "Reg. §1.469-4",
                "summary": "Group activities into appropriate economic units (5 factors). Aggregates hours for material participation.",
                "related_topics": ["rental_trade_or_business_restriction", "regrouping_material_change", "Rev_Proc_2010_13"]
            },
            "disposition_entire_interest": {
                "keywords": ["disposition", "469(g)", "suspended losses", "entire interest", "fully taxable"],
                "authority": "IRC §469(g)",
                "summary": "Dispose entire interest in fully taxable transaction to unrelated party → all suspended losses deductible.",
                "related_topics": ["offset_non_passive_income", "installment_sale_exception", "death_loses_suspended_losses"]
            },
            "installment_sale_469g3": {
                "keywords": ["installment sale", "469(g)(3)", "pro-rata release", "suspended losses deferred"],
                "authority": "IRC §469(g)(3)",
                "summary": "Installment sale releases suspended losses pro-rata as gain recognized (not all in year of sale).",
                "related_topics": ["elect_out_of_installment", "recognize_all_gain_year_1"]
            },
            "self_rental_recharacterization": {
                "keywords": ["self-rental", "Reg 1.469-2(f)(6)", "recharacterization", "non-passive income"],
                "authority": "Reg. §1.469-2(f)(6)",
                "summary": "Rental income from property rented to taxpayer's materially participated business is non-passive income.",
                "related_topics": ["net_income_only_not_losses", "common_control_50_percent"]
            },
            "publicly_traded_partnership": {
                "keywords": ["PTP", "publicly traded partnership", "MLP", "469(k)", "separate basket"],
                "authority": "IRC §469(k)",
                "summary": "PTP losses only offset income from SAME PTP (separate basket rule). Cannot offset other passive income.",
                "related_topics": ["master_limited_partnership", "disposition_releases_suspended_losses"]
            },
            "net_investment_income_tax": {
                "keywords": ["NIIT", "1411", "3.8% tax", "net investment income", "passive income"],
                "authority": "IRC §1411",
                "summary": "3.8% tax on lesser of NII or MAGI exceeding threshold. Passive income is NII unless materially participated.",
                "related_topics": ["material_participation_excludes_from_niit", "250k_threshold_mfj"]
            },
            "limited_partner_material_participation": {
                "keywords": ["limited partner", "LP", "material participation", "test 1 5 6 only"],
                "authority": "Temp. Reg. §1.469-5T(e)(3)",
                "summary": "Limited partners can only use tests 1, 5, 6 for material participation (not tests 2, 3, 4, 7).",
                "related_topics": ["LLC_member_treated_as_LP", "management_rights_exception"]
            },
            "working_interest_oil_gas": {
                "keywords": ["working interest", "oil and gas", "469(c)(3)", "not passive", "unlimited liability"],
                "authority": "IRC §469(c)(3)",
                "summary": "Working interest in oil/gas well NOT passive if taxpayer has unlimited liability (not held through limited partnership).",
                "related_topics": ["exception_to_passive_rule", "unlimited_liability_required"]
            },
            "closely_held_c_corp_pal": {
                "keywords": ["closely held C corp", "469(a)(2)", "passive activity", "active business test"],
                "authority": "IRC §469(a)(2)",
                "summary": "Closely held C corps: PAL can offset active business income (not just passive). Different from individuals.",
                "related_topics": ["5_or_fewer_shareholders", "50_percent_ownership"]
            },
            "hour_substantiation": {
                "keywords": ["substantiation", "hours", "time log", "contemporaneous record", "proof"],
                "authority": "Temp. Reg. §1.469-5T(f)(4)",
                "summary": "Contemporaneous time logs gold standard. Appointment books, calendars acceptable if reasonable and credible.",
                "related_topics": ["goshorn_case_substantiation_failure", "reconstructed_records_risky"]
            },
            "spouse_participation": {
                "keywords": ["spouse", "husband", "wife", "community property", "separate counting"],
                "authority": "Temp. Reg. §1.469-5T(f)(3)",
                "summary": "Each spouse's participation counted separately (not aggregated). Community property rules don't aggregate hours.",
                "related_topics": ["individual_counting", "mfs_special_rules"]
            },
            "activity_definition_undertaking": {
                "keywords": ["activity", "undertaking", "definition", "what is an activity"],
                "authority": "Temp. Reg. §1.469-4",
                "summary": "Activity = undertaking consisting of one or more trades/businesses or rental activities. Grouping rules apply.",
                "related_topics": ["grouping_election", "appropriate_economic_unit"]
            },
            "regrouping_material_change": {
                "keywords": ["regrouping", "regroup", "material change", "Rev Proc 2010-13"],
                "authority": "Rev. Proc. 2010-13",
                "summary": "Regrouping generally prohibited unless material change in facts. Rev. Proc. 2010-13 provides safe harbor.",
                "related_topics": ["original_grouping_binding", "sale_or_acquisition_material_change"]
            },
            "average_period_7_day_exception": {
                "keywords": ["7 day", "average period", "hotel", "car rental", "not rental activity"],
                "authority": "Temp. Reg. §1.469-1T(e)(3)(ii)(A)",
                "summary": "If average customer use ≤7 days, NOT rental activity (e.g., hotel, car rental). Subject to material participation.",
                "related_topics": ["short_term_rental", "trade_or_business_not_rental"]
            },
            "average_period_30_day_exception": {
                "keywords": ["30 day", "significant services", "vacation rental", "not rental activity"],
                "authority": "Temp. Reg. §1.469-1T(e)(3)(ii)(B)",
                "summary": "If average use ≤30 days AND significant personal services provided, NOT rental activity.",
                "related_topics": ["cleaning_services", "concierge_services"]
            },
            "extraordinary_services_exception": {
                "keywords": ["extraordinary services", "hospital", "boarding school", "services primary"],
                "authority": "Temp. Reg. §1.469-1T(e)(3)(ii)(C)",
                "summary": "If extraordinary personal services provided, NOT rental activity (use of property incidental to services).",
                "related_topics": ["hospital_example", "services_by_individuals"]
            }
        }

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant passive activity concepts.

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            List of search results with scores
        """
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        # Score each index entry
        results = []
        for topic_id, data in self.search_index.items():
            score = 0.0

            # Keyword matching
            for keyword in data["keywords"]:
                keyword_terms = set(keyword.lower().split())
                # Exact phrase match
                if keyword.lower() in query_lower:
                    score += 5.0
                # Partial term overlap
                overlap = len(query_terms & keyword_terms)
                if overlap > 0:
                    score += overlap * 1.5

            # Authority citation matching
            if any(term in data["authority"].lower() for term in query_terms):
                score += 3.0

            # Summary matching
            summary_terms = set(data["summary"].lower().split())
            summary_overlap = len(query_terms & summary_terms)
            score += summary_overlap * 0.5

            if score > 0:
                results.append({
                    "topic_id": topic_id,
                    "score": score,
                    "authority": data["authority"],
                    "summary": data["summary"],
                    "related_topics": data["related_topics"],
                    "keywords": data["keywords"]
                })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]

    def get_related_topics(self, topic_id: str) -> List[str]:
        """Get related topics for a given topic."""
        if topic_id in self.search_index:
            return self.search_index[topic_id]["related_topics"]
        return []

    def cloud_search_fallback(self, query: str, top_k: int = 3) -> Optional[List[Dict[str, Any]]]:
        """
        Fallback to cloud retriever if available.

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            Cloud search results or None if unavailable
        """
        if not self.cloud_retriever_available:
            return None

        try:
            # Import cloud retriever if available
            import sys
            from pathlib import Path
            shared_path = Path(__file__).parent.parent / "_shared"
            if shared_path.exists():
                sys.path.insert(0, str(shared_path))
                from cloud_retriever import CloudKnowledgeRetriever

                retriever = CloudKnowledgeRetriever(domain="tax_passive_activity")
                results = retriever.search(query, top_k=top_k)
                return results
        except ImportError:
            return None
        except Exception:
            return None

    def generate_search_hash(self, query: str) -> str:
        """Generate deterministic hash for search query."""
        normalized = query.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
