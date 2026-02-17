"""
TX10 State Nexus Engine - Vector Search Fallback
Semantic retrieval when doctrine cache misses
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import hashlib
import json


@dataclass
class SearchResult:
    """Search result with relevance scoring"""
    content: str
    relevance_score: float
    source: str
    metadata: Dict[str, Any]
    doc_id: str


class VectorSearchEngine:
    """Fallback search when doctrine cache doesn't match"""

    def __init__(self, cloud_retriever=None):
        """Initialize with optional cloud retriever"""
        self.cloud_retriever = cloud_retriever
        self.cache = {}

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.7,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Perform semantic search for state nexus information

        Args:
            query: Search query
            top_k: Number of results to return
            min_score: Minimum relevance score threshold
            filters: Optional filters (state, category, date range)

        Returns:
            List of SearchResult objects
        """
        # Check cache first
        cache_key = self._generate_cache_key(query, top_k, min_score, filters)
        if cache_key in self.cache:
            return self.cache[cache_key]

        results = []

        # Try cloud retriever if available
        if self.cloud_retriever:
            try:
                cloud_results = self._search_cloud(query, top_k, min_score, filters)
                results.extend(cloud_results)
            except Exception as e:
                # Log error but continue with fallback
                pass

        # Fallback: local heuristic search
        if not results:
            results = self._heuristic_search(query, top_k, min_score, filters)

        # Cache results
        self.cache[cache_key] = results

        return results

    def _search_cloud(
        self,
        query: str,
        top_k: int,
        min_score: float,
        filters: Optional[Dict[str, Any]]
    ) -> List[SearchResult]:
        """Search cloud vector database"""
        if not self.cloud_retriever:
            return []

        # Build search params
        params = {
            "query": query,
            "top_k": top_k,
            "min_score": min_score,
            "domain": "state_tax_nexus"
        }

        if filters:
            params["filters"] = filters

        # Execute cloud search
        cloud_response = self.cloud_retriever.search(**params)

        # Convert to SearchResult objects
        results = []
        for item in cloud_response.get("results", []):
            results.append(SearchResult(
                content=item.get("content", ""),
                relevance_score=item.get("score", 0.0),
                source=item.get("source", "cloud_vector_db"),
                metadata=item.get("metadata", {}),
                doc_id=item.get("doc_id", "")
            ))

        return results

    def _heuristic_search(
        self,
        query: str,
        top_k: int,
        min_score: float,
        filters: Optional[Dict[str, Any]]
    ) -> List[SearchResult]:
        """
        Fallback heuristic search based on keyword matching
        Used when cloud retriever unavailable
        """
        # Sample knowledge base (would be expanded with real docs)
        knowledge_base = self._get_fallback_knowledge_base()

        # Simple keyword scoring
        query_lower = query.lower()
        scored_results = []

        for doc in knowledge_base:
            # Skip if filters don't match
            if filters and not self._matches_filters(doc, filters):
                continue

            # Calculate relevance score
            score = self._calculate_keyword_score(query_lower, doc)

            if score >= min_score:
                scored_results.append((score, doc))

        # Sort by score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)

        # Convert to SearchResult objects
        results = []
        for score, doc in scored_results[:top_k]:
            results.append(SearchResult(
                content=doc["content"],
                relevance_score=score,
                source=doc.get("source", "local_fallback"),
                metadata=doc.get("metadata", {}),
                doc_id=doc.get("doc_id", hashlib.md5(doc["content"].encode()).hexdigest())
            ))

        return results

    def _calculate_keyword_score(self, query: str, doc: Dict[str, Any]) -> float:
        """Calculate relevance score based on keyword matching"""
        content = doc.get("content", "").lower()
        title = doc.get("title", "").lower()
        keywords = doc.get("keywords", [])

        score = 0.0

        # Exact phrase match in title (high weight)
        if query in title:
            score += 0.5

        # Exact phrase match in content
        if query in content:
            score += 0.3

        # Individual word matches
        query_words = set(query.split())
        content_words = set(content.split())
        keyword_set = set(k.lower() for k in keywords)

        word_overlap = query_words & content_words
        keyword_overlap = query_words & keyword_set

        # Word overlap scoring
        if query_words:
            score += 0.1 * (len(word_overlap) / len(query_words))
            score += 0.1 * (len(keyword_overlap) / len(query_words))

        return min(score, 1.0)

    def _matches_filters(self, doc: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if document matches filters"""
        metadata = doc.get("metadata", {})

        for key, value in filters.items():
            if key == "state":
                if metadata.get("state") != value:
                    return False
            elif key == "category":
                if metadata.get("category") != value:
                    return False
            elif key == "date_after":
                doc_date = metadata.get("date")
                if not doc_date or doc_date < value:
                    return False
            elif key == "date_before":
                doc_date = metadata.get("date")
                if not doc_date or doc_date > value:
                    return False

        return True

    def _generate_cache_key(
        self,
        query: str,
        top_k: int,
        min_score: float,
        filters: Optional[Dict[str, Any]]
    ) -> str:
        """Generate cache key for search results"""
        filter_str = json.dumps(filters, sort_keys=True) if filters else ""
        key_input = f"{query}|{top_k}|{min_score}|{filter_str}"
        return hashlib.md5(key_input.encode()).hexdigest()

    def _get_fallback_knowledge_base(self) -> List[Dict[str, Any]]:
        """Fallback knowledge base for local search"""
        return [
            {
                "doc_id": "wayfair_summary",
                "title": "South Dakota v. Wayfair - Economic Nexus",
                "content": "South Dakota v. Wayfair, 138 S. Ct. 2080 (2018) overruled Quill's physical presence requirement. States may impose sales tax collection obligations on remote sellers based on economic nexus. South Dakota's statute had $100,000 sales OR 200 transactions threshold, prospective application, and Streamlined Sales Tax membership.",
                "keywords": ["wayfair", "economic nexus", "quill", "physical presence", "remote seller", "sales threshold"],
                "metadata": {"category": "economic_nexus", "date": "2018-06-21", "authority": "supreme_court"}
            },
            {
                "doc_id": "pl_86_272_basics",
                "title": "P.L. 86-272 Protection Scope",
                "content": "P.L. 86-272 (15 U.S.C. §§ 381-384) prohibits states from imposing net income tax on out-of-state sellers whose only activity is solicitation of orders for tangible personal property. Does NOT protect services, intangibles, rentals, or activities beyond mere solicitation. Does NOT apply to gross receipts taxes or sales tax.",
                "keywords": ["pl 86-272", "solicitation", "tangible personal property", "net income tax", "safe harbor"],
                "metadata": {"category": "pl_86_272_protection", "authority": "federal_statute"}
            },
            {
                "doc_id": "complete_auto_test",
                "title": "Complete Auto Transit Four-Prong Test",
                "content": "Complete Auto Transit, Inc. v. Brady, 430 U.S. 274 (1977) established four-prong test: (1) substantial nexus, (2) fair apportionment, (3) no discrimination, (4) fair relation to services. All four prongs must be satisfied for constitutional state tax.",
                "keywords": ["complete auto", "substantial nexus", "fair apportionment", "discrimination", "commerce clause"],
                "metadata": {"category": "constitutional_nexus", "date": "1977", "authority": "supreme_court"}
            },
            {
                "doc_id": "texas_franchise_tax",
                "title": "Texas Franchise Tax Nexus and Margin",
                "content": "Texas franchise tax is privilege tax measured by taxable margin (not net income). $500,000 Texas receipts creates economic nexus. P.L. 86-272 does NOT apply. Margin = lesser of (revenue-COGS, revenue-comp, revenue×70%). Single receipts factor apportionment.",
                "keywords": ["texas", "franchise tax", "margin tax", "economic nexus", "$500,000"],
                "metadata": {"category": "texas_franchise_tax", "state": "texas", "authority": "state_statute"}
            },
            {
                "doc_id": "marketplace_facilitator",
                "title": "Marketplace Facilitator Collection Laws",
                "content": "44+ states require marketplace facilitators (Amazon, eBay, Etsy) to collect sales tax on behalf of third-party sellers. Third-party sellers relieved of collection obligation for marketplace sales. Hold harmless provisions protect sellers from facilitator non-compliance.",
                "keywords": ["marketplace facilitator", "amazon fba", "third party seller", "sales tax collection"],
                "metadata": {"category": "marketplace_facilitator", "date": "2019-2020", "authority": "state_statutes"}
            },
            {
                "doc_id": "salt_cap_ptet",
                "title": "SALT Cap and PTET Workarounds",
                "content": "IRC § 164(b)(6) caps SALT deduction at $10,000 for individuals (2018-2025). Pass-through entity tax (PTET) workarounds allow entity-level state tax deduction. IRS Notice 2020-75 approved PTETs. 30+ states enacted PTET legislation. Owners receive credit on state returns.",
                "keywords": ["salt cap", "$10,000", "ptet", "pass-through entity tax", "164(b)(6)", "irs notice 2020-75"],
                "metadata": {"category": "salt_cap_planning", "date": "2020", "authority": "irs_notice"}
            },
            {
                "doc_id": "factor_presence_nexus",
                "title": "Factor Presence Nexus Standards",
                "content": "Factor presence nexus statutes create income tax nexus based on apportionment factor thresholds. Common: $500K sales, $50K property/payroll. Constitutional post-Wayfair. P.L. 86-272 may still protect TPP sales even with factor nexus.",
                "keywords": ["factor presence", "bright-line nexus", "sales threshold", "$500,000", "$50,000"],
                "metadata": {"category": "factor_presence", "authority": "state_statutes"}
            },
            {
                "doc_id": "combined_reporting",
                "title": "Combined Reporting and Unitary Business",
                "content": "28 states require combined reporting for unitary businesses. Unitary business test: three unities (ownership, operation, use) or contribution/dependency. Water's edge election limits to U.S. corporations. Joyce vs. Finnigan methods for numerator inclusion.",
                "keywords": ["combined reporting", "unitary business", "water's edge", "joyce", "finnigan"],
                "metadata": {"category": "combined_reporting", "authority": "state_statutes"}
            },
            {
                "doc_id": "market_based_sourcing",
                "title": "Market-Based Sourcing for Services",
                "content": "30+ states adopted market-based sourcing for service receipts. Assigns receipts to customer's market state, not where service performed. Cascading hierarchy: benefit received → billing address → domicile. Shifts sales factor from service states to customer states.",
                "keywords": ["market-based sourcing", "customer location", "service receipts", "cascading rules"],
                "metadata": {"category": "sourcing_rules", "authority": "state_regulations"}
            },
            {
                "doc_id": "affiliate_nexus",
                "title": "Affiliate and Attribution Nexus",
                "content": "Affiliate nexus imputes in-state affiliate's physical presence to out-of-state seller. Geoffrey doctrine: intangibles exploited in-state create nexus. KFC interbrand competition test. Borders Online: shared services/returns created nexus. Click-through nexus: commissions to in-state referrers.",
                "keywords": ["affiliate nexus", "attribution nexus", "geoffrey", "kfc", "click-through"],
                "metadata": {"category": "attribution_nexus", "authority": "case_law"}
            }
        ]

    def clear_cache(self):
        """Clear search cache"""
        self.cache = {}

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "cache_size": len(self.cache),
            "cache_keys": list(self.cache.keys())
        }
