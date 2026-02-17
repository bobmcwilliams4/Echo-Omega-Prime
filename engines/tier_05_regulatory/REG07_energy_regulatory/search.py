import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
        self._inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._doc_titles: Dict[int, str] = {}
        self._doc_contents: Dict[int, str] = {}
        self._doc_tags: Dict[int, List[str]] = {}
        self._doc_weights: Dict[int, float] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.content)
            term_freqs = Counter(tokens)
            for term, freq in term_freqs.items():
                self._inverted_index[term][doc.id] = freq
            self._documents[doc.id] = doc
            self._doc_lengths[doc.id] = len(tokens)
            self._doc_titles[doc.id] = doc.title
            self._doc_contents[doc.id] = doc.content
            self._doc_tags[doc.id] = doc.tags
            self._doc_weights[doc.id] = doc.weight
            self._total_docs += 1
            self._avg_doc_length = (
                sum(self._doc_lengths.values()) / self._total_docs
                if self._total_docs > 0 else 0.0
            )
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        doc_snippets: Dict[int, str] = {}
        for term in query_terms:
            idf = self._compute_idf(term)
            postings = self._inverted_index.get(term, {})
            for doc_id, freq in postings.items():
                score = self._score_bm25(term, doc_id, freq, idf)
                doc_scores[doc_id] += score
        # TF-IDF scoring (normalized)
        for term in query_terms:
            postings = self._inverted_index.get(term, {})
            idf = self._compute_idf(term)
            for doc_id, freq in postings.items():
                tf = freq / self._doc_lengths[doc_id] if self._doc_lengths[doc_id] > 0 else 0
                doc_scores[doc_id] += tf * idf * 0.5  # weight TF-IDF lower than BM25
        # Prepare snippets
        for doc_id in doc_scores:
            content = self._doc_contents[doc_id]
            snippet = self._make_snippet(content, query_terms)
            doc_snippets[doc_id] = snippet
        # Weight by document weight
        for doc_id in doc_scores:
            doc_scores[doc_id] *= self._doc_weights.get(doc_id, 1.0)
        # Sort results
        results = sorted(
            ((doc_id, score) for doc_id, score in doc_scores.items()),
            key=lambda x: x[1], reverse=True
        )[:limit]
        return [
            SearchResult(
                doc_id=doc_id,
                score=score,
                title=self._doc_titles.get(doc_id, ""),
                snippet=doc_snippets.get(doc_id, "")
            )
            for doc_id, score in results
        ]

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "total_documents": self._total_docs,
                "avg_doc_length": self._avg_doc_length,
                "unique_terms": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = len(self._inverted_index.get(term, {}))
        N = self._total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5)) if df > 0 else 0.0
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: int, freq: int, idf: float) -> float:
        k1 = self._bm25_k1
        b = self._bm25_b
        dl = self._doc_lengths.get(doc_id, 0)
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1
        tf = freq
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * dl / avgdl)
        return idf * (numerator / denominator) if denominator != 0 else 0.0

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:window] + "..." if len(content) > window else content
        start = max(min(positions) - window // 2, 0)
        end = start + window
        snippet = content[start:end]
        return snippet + "..." if end < len(content) else snippet

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id=1,
            title="FERC Jurisdiction Over Interstate Transmission",
            content="The Federal Energy Regulatory Commission (FERC) has exclusive jurisdiction over the transmission of electric energy in interstate commerce. This includes the regulation of rates, terms, and conditions for transmission service under the Federal Power Act.",
            tags=["FERC", "Transmission", "Jurisdiction"],
            weight=1.0
        ),
        SearchDocument(
            id=2,
            title="NERC CIP Critical Infrastructure Protection Standards",
            content="NERC's Critical Infrastructure Protection (CIP) standards require registered entities to identify and protect Bulk Electric System (BES) cyber systems to ensure the reliability and security of the grid.",
            tags=["NERC", "CIP", "Cybersecurity"],
            weight=1.0
        ),
        SearchDocument(
            id=3,
            title="ERCOT Nodal Market Protocols and Settlement",
            content="ERCOT's nodal market protocols govern the operation and settlement of the Texas electricity market, including energy pricing, congestion management, and ancillary services.",
            tags=["ERCOT", "Market", "Protocols"],
            weight=1.0
        ),
        SearchDocument(
            id=4,
            title="FERC Market-Based Rate Authority and Mitigation",
            content="Market-Based Rate (MBR) authority allows sellers to transact at market rates, subject to FERC's mitigation policies to prevent the exercise of market power and ensure just and reasonable rates.",
            tags=["FERC", "Market-Based Rate", "Mitigation"],
            weight=1.0
        ),
        SearchDocument(
            id=5,
            title="FERC Section 205 Rate Filing Requirements",
            content="Under Section 205 of the Federal Power Act, public utilities must file all rates and charges with FERC, including supporting documentation and justification for any changes.",
            tags=["FERC", "Section 205", "Rates"],
            weight=1.0
        ),
        SearchDocument(
            id=6,
            title="Natural Gas Pipeline Certificate Authority Under NGA Section 7",
            content="The Natural Gas Act (NGA) Section 7 requires pipeline companies to obtain a certificate of public convenience and necessity from FERC before constructing or operating interstate natural gas pipelines.",
            tags=["NGA", "Pipeline", "Certificate"],
            weight=1.0
        ),
        SearchDocument(
            id=7,
            title="Pipeline Safety Regulations 49 CFR 192 and 195",
            content="Pipeline safety regulations under 49 CFR Parts 192 and 195 establish minimum safety standards for the design, construction, operation, and maintenance of natural gas and hazardous liquid pipelines.",
            tags=["Pipeline", "Safety", "CFR 192", "CFR 195"],
            weight=1.0
        ),
        SearchDocument(
            id=8,
            title="PUCT Ratemaking for Texas Electric Utilities",
            content="The Public Utility Commission of Texas (PUCT) oversees ratemaking for electric utilities, including rate base, cost of service, and return on equity determinations.",
            tags=["PUCT", "Ratemaking", "Texas"],
            weight=1.0
        ),
        SearchDocument(
            id=9,
            title="Renewable Portfolio Standards and REC Compliance",
            content="Renewable Portfolio Standards (RPS) require utilities to procure a certain percentage of their electricity from renewable resources, with compliance tracked through Renewable Energy Certificates (RECs).",
            tags=["RPS", "REC", "Renewable"],
            weight=1.0
        ),
        SearchDocument(
            id=10,
            title="FERC Anti-Manipulation Rule and Market Behavior",
            content="FERC's anti-manipulation rule prohibits fraudulent or deceptive schemes in energy markets, with enforcement actions targeting market manipulation and improper market behavior.",
            tags=["FERC", "Anti-Manipulation", "Market"],
            weight=1.0
        ),
        SearchDocument(
            id=11,
            title="Large Generator Interconnection Process",
            content="The Large Generator Interconnection Process (LGIP) provides procedures for generators seeking to interconnect with the transmission grid, including feasibility studies and agreements.",
            tags=["Generator", "Interconnection", "LGIP"],
            weight=1.0
        ),
        SearchDocument(
            id=12,
            title="FERC Reliability Coordinator and Balancing Authority Registration",
            content="Entities performing reliability coordination or balancing authority functions must register with FERC and comply with applicable reliability standards.",
            tags=["FERC", "Reliability", "Balancing Authority"],
            weight=1.0
        ),
        SearchDocument(
            id=13,
            title="Texas Transmission Cost Recovery Factor (TCCRF)",
            content="The Transmission Cost Recovery Factor (TCCRF) mechanism allows Texas utilities to recover transmission investment costs through a rider on customer bills, subject to PUCT approval.",
            tags=["TCCRF", "Transmission", "Texas"],
            weight=1.0
        ),
        SearchDocument(
            id=14,
            title="FERC Demand Response Compensation Order 745",
            content="Order 745 requires that demand response resources be compensated at the market price for energy when they provide a net benefit to the system, ensuring fair treatment of demand-side resources.",
            tags=["FERC", "Demand Response", "Order 745"],
            weight=1.0
        ),
        SearchDocument(
            id=15,
            title="Environmental Compliance for Generation Facilities",
            content="Generation facilities must comply with federal and state environmental regulations, including air and water permits, emissions limits, and reporting requirements.",
            tags=["Environmental", "Generation", "Compliance"],
            weight=1.0
        ),
        SearchDocument(
            id=16,
            title="FERC Open Access Transmission Tariff (OATT) Administration",
            content="The OATT requires transmission providers to offer open, non-discriminatory access to their transmission systems, with rates and terms governed by FERC.",
            tags=["FERC", "OATT", "Transmission"],
            weight=1.0
        ),
        SearchDocument(
            id=17,
            title="State Renewable Energy Siting and Permitting",
            content="States regulate the siting and permitting of renewable energy projects, balancing environmental, land use, and community concerns.",
            tags=["State", "Renewable", "Siting", "Permitting"],
            weight=1.0
        ),
        SearchDocument(
            id=18,
            title="Electric Reliability Council (ERCOT) Governance and Oversight",
            content="ERCOT's governance structure includes stakeholder committees and an independent board, overseeing market rules and grid reliability in Texas.",
            tags=["ERCOT", "Governance", "Oversight"],
            weight=1.0
        ),
        SearchDocument(
            id=19,
            title="Tax Treatment of Renewable Energy Tax Credits",
            content="Federal tax credits, such as the Production Tax Credit (PTC) and Investment Tax Credit (ITC), provide incentives for renewable energy development, with specific IRS rules for claiming and transferring credits.",
            tags=["Tax", "Renewable", "Credits"],
            weight=1.0
        ),
        SearchDocument(
            id=20,
            title="FERC Compliance and Self-Reporting Obligations",
            content="Market participants must comply with FERC regulations and are encouraged to self-report potential violations to mitigate penalties.",
            tags=["FERC", "Compliance", "Self-Reporting"],
            weight=1.0
        ),
        SearchDocument(
            id=21,
            title="RTO/ISO Capacity Market Mechanisms",
            content="Regional Transmission Organizations (RTOs) and Independent System Operators (ISOs) operate capacity markets to ensure resource adequacy, with mechanisms for auctions, obligations, and penalties.",
            tags=["RTO", "ISO", "Capacity Market"],
            weight=1.0
        ),
        SearchDocument(
            id=22,
            title="FERC Abandonment Authority for Pipelines",
            content="Pipeline companies must obtain FERC approval before abandoning pipeline facilities or services, ensuring continued service to customers.",
            tags=["FERC", "Pipeline", "Abandonment"],
            weight=1.0
        ),
        SearchDocument(
            id=23,
            title="Bulk Electric System (BES) Definition and Registration",
            content="The Bulk Electric System (BES) includes all transmission elements operated at 100 kV or higher, with entities required to register with NERC for compliance.",
            tags=["BES", "NERC", "Registration"],
            weight=1.0
        ),
        SearchDocument(
            id=24,
            title="ERCOT Resource Adequacy and Reserve Margin",
            content="ERCOT monitors resource adequacy and maintains reserve margins to ensure reliable electric service, with regular assessments and market signals.",
            tags=["ERCOT", "Resource Adequacy", "Reserve Margin"],
            weight=1.0
        ),
        SearchDocument(
            id=25,
            title="NERC Reliability Standards Development Process",
            content="NERC develops reliability standards through an open, consensus-based process involving industry stakeholders and subject to FERC approval.",
            tags=["NERC", "Reliability", "Standards"],
            weight=1.0
        ),
        SearchDocument(
            id=26,
            title="Transmission Planning and Regional Coordination",
            content="Transmission planning involves regional coordination among utilities, RTOs, and state agencies to ensure adequate infrastructure and reliability.",
            tags=["Transmission", "Planning", "Regional Coordination"],
            weight=1.0
        ),
        SearchDocument(
            id=27,
            title="Renewable Energy Certificate (REC) Tracking Systems",
            content="REC tracking systems record the creation, transfer, and retirement of renewable energy certificates, supporting RPS compliance and market transparency.",
            tags=["REC", "Tracking", "Renewable"],
            weight=1.0
        ),
        SearchDocument(
            id=28,
            title="FERC Enforcement and Penalty Guidelines",
            content="FERC's enforcement program includes investigation of violations and imposition of civil penalties, guided by policy statements and penalty guidelines.",
            tags=["FERC", "Enforcement", "Penalties"],
            weight=1.0
        ),
        SearchDocument(
            id=29,
            title="PUCT Certificate of Convenience and Necessity (CCN)",
            content="Texas utilities must obtain a Certificate of Convenience and Necessity (CCN) from the PUCT before constructing new transmission lines or facilities.",
            tags=["PUCT", "CCN", "Transmission"],
            weight=1.0
        ),
        SearchDocument(
            id=30,
            title="FERC Order 1000 Transmission Planning Reforms",
            content="Order 1000 requires transmission providers to participate in regional planning processes and consider public policy requirements in transmission planning.",
            tags=["FERC", "Order 1000", "Transmission Planning"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)