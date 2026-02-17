import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

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
        self.term_doc_tf: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.lock = threading.Lock()
        self.total_docs = 0
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.term_doc_freq[token] += 1
                self.term_doc_tf[doc.id][token] = count
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_doc_tf[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        if doc_id in self._tfidf_cache and all(term in self._tfidf_cache[doc_id] for term in query_terms):
            return sum(self._tfidf_cache[doc_id][term] for term in query_terms)
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_doc_tf[doc_id].get(term, 0)
            if tf == 0:
                continue
            norm_tf = tf / doc_len
            idf = self._compute_idf(term)
            tfidf = norm_tf * idf
            self._tfidf_cache[doc_id][term] = tfidf
            score += tfidf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(doc_id, query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str]) -> str:
        doc = self.documents[doc_id]
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, token in enumerate(tokens) if token in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b{}\b'.format(re.escape(term)), f'**{term}**', snippet, flags=re.IGNORECASE)
        return snippet + "..." if len(snippet) < len(content) else snippet

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
        }

# Singleton factory for search index
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
            1,
            "Pumped Hydro Storage Fundamentals",
            "Pumped hydro storage is the most mature and widely deployed grid-scale energy storage technology. It operates by moving water between two reservoirs at different elevations. During periods of excess electricity, water is pumped uphill; during demand, water is released downhill to generate electricity. Key parameters include round-trip efficiency, site selection, environmental impact, and operational flexibility.",
            ["pumped hydro", "fundamentals", "grid-scale", "efficiency", "site selection"],
            1.0
        ),
        SearchDocument(
            2,
            "Compressed Air Energy Storage (CAES) Technology",
            "CAES stores energy by compressing air in underground caverns or tanks. When electricity is needed, the compressed air is released, heated, and expanded through turbines to generate power. CAES systems are characterized by their scalability, long-duration capabilities, and integration challenges related to heat management and site geology.",
            ["CAES", "compressed air", "technology", "long-duration", "integration"],
            1.0
        ),
        SearchDocument(
            3,
            "Flywheel Energy Storage Systems",
            "Flywheel systems store energy in the rotational motion of a mass. They offer high power density, rapid response, and long cycle life. Applications include frequency regulation, uninterruptible power supply, and short-duration grid services. Key considerations are material selection, bearing technology, and safety standards.",
            ["flywheel", "energy storage", "frequency regulation", "cycle life", "safety"],
            1.0
        ),
        SearchDocument(
            4,
            "Supercapacitor and Ultracapacitor Technology",
            "Supercapacitors provide high power output and fast charge/discharge cycles. They are used for bridging power gaps, supporting renewables, and enhancing battery systems. Ultracapacitors extend these capabilities with greater energy density. Challenges include cost, voltage balancing, and integration with other storage technologies.",
            ["supercapacitor", "ultracapacitor", "power output", "integration", "energy density"],
            1.0
        ),
        SearchDocument(
            5,
            "Thermal Energy Storage Systems",
            "Thermal energy storage involves storing heat or cold for later use. Technologies include molten salt, chilled water, and phase change materials. Applications range from grid-scale storage to district heating and cooling. Efficiency depends on insulation, material properties, and system design.",
            ["thermal storage", "molten salt", "phase change", "district heating", "efficiency"],
            1.0
        ),
        SearchDocument(
            6,
            "Grid-Scale Storage Economics and Optimization",
            "Grid-scale storage economics consider capital costs, operational expenses, revenue streams, and market participation. Optimization strategies include dispatch algorithms, revenue stacking, and cost-benefit analyses. Regulatory frameworks and incentives play a significant role in project viability.",
            ["economics", "optimization", "grid-scale", "revenue stacking", "regulatory"],
            1.0
        ),
        SearchDocument(
            7,
            "Battery Energy Storage System (BESS) Integration",
            "BESS integration involves connecting battery systems to the grid or distributed assets. Key factors include inverter technology, control systems, safety standards, and communication protocols. Integration challenges include managing degradation, warranty structures, and ensuring reliable operation.",
            ["BESS", "integration", "inverter", "control systems", "degradation"],
            1.0
        ),
        SearchDocument(
            8,
            "Hybrid Storage Systems and Multi-Technology Optimization",
            "Hybrid storage systems combine multiple technologies (e.g., batteries, supercapacitors, thermal storage) to optimize performance. Multi-technology optimization leverages complementary strengths, such as rapid response and long-duration storage. Control strategies and system design are critical for maximizing benefits.",
            ["hybrid storage", "multi-technology", "optimization", "control", "system design"],
            1.0
        ),
        SearchDocument(
            9,
            "Long-Duration Energy Storage (LDES) Technologies",
            "LDES technologies provide storage for hours to days, supporting renewable integration and grid reliability. Examples include pumped hydro, CAES, flow batteries, and hydrogen storage. Key metrics are duration, efficiency, scalability, and cost.",
            ["LDES", "long-duration", "renewable integration", "scalability", "cost"],
            1.0
        ),
        SearchDocument(
            10,
            "Storage Siting and Environmental Considerations",
            "Storage siting involves selecting locations based on resource availability, grid access, and environmental impact. Environmental considerations include land use, water resources, emissions, and community engagement. Regulatory compliance and permitting are essential for project success.",
            ["siting", "environmental", "regulatory", "permitting", "community"],
            1.0
        ),
        SearchDocument(
            11,
            "Round-Trip Efficiency Analysis and Optimization",
            "Round-trip efficiency measures the ratio of energy output to input in storage systems. Optimization focuses on minimizing losses through improved materials, system design, and operational strategies. Accurate measurement and benchmarking are vital for comparing technologies.",
            ["efficiency", "analysis", "optimization", "losses", "benchmarking"],
            1.0
        ),
        SearchDocument(
            12,
            "Storage Safety Standards and Fire Protection",
            "Safety standards address risks such as thermal runaway, fire, and electrical hazards in storage systems. Fire protection involves detection, suppression, and containment strategies. Compliance with international standards ensures safe operation and public acceptance.",
            ["safety", "fire protection", "standards", "thermal runaway", "hazards"],
            1.0
        ),
        SearchDocument(
            13,
            "Storage Interconnection and Grid Integration",
            "Interconnection involves connecting storage assets to the grid, requiring technical, regulatory, and operational coordination. Grid integration ensures reliable operation, supports renewables, and enables ancillary services. Standards and protocols guide interoperability.",
            ["interconnection", "grid integration", "ancillary services", "protocols", "standards"],
            1.0
        ),
        SearchDocument(
            14,
            "Storage Market Participation and Revenue Stacking",
            "Market participation allows storage systems to earn revenue from multiple services, including energy arbitrage, frequency regulation, and capacity markets. Revenue stacking maximizes returns by providing several services simultaneously. Market rules and pricing structures influence profitability.",
            ["market participation", "revenue stacking", "arbitrage", "frequency regulation", "capacity"],
            1.0
        ),
        SearchDocument(
            15,
            "Storage Degradation Modeling and Warranty Structures",
            "Degradation modeling predicts performance loss over time in storage systems. Warranty structures define coverage for capacity, efficiency, and cycle life. Accurate modeling supports asset management, financial planning, and risk mitigation.",
            ["degradation", "modeling", "warranty", "capacity", "cycle life"],
            1.0
        ),
        SearchDocument(
            16,
            "Seasonal and Multi-Day Storage Applications",
            "Seasonal storage addresses energy needs over months, supporting renewables and grid balancing. Multi-day applications bridge gaps during extended outages or low generation periods. Technologies include hydrogen, CAES, and pumped hydro.",
            ["seasonal storage", "multi-day", "hydrogen", "CAES", "pumped hydro"],
            1.0
        ),
        SearchDocument(
            17,
            "Distributed vs. Centralized Storage Deployment",
            "Distributed storage deploys assets near loads or generation, enhancing resilience and flexibility. Centralized storage aggregates capacity at grid nodes, supporting large-scale integration. Deployment strategies depend on grid topology, economics, and policy.",
            ["distributed", "centralized", "deployment", "resilience", "flexibility"],
            1.0
        ),
        SearchDocument(
            18,
            "Storage and Renewable Integration Strategies",
            "Integration strategies align storage with renewable generation to maximize grid benefits. Approaches include co-location, hybrid systems, and advanced control algorithms. Key outcomes are improved reliability, reduced curtailment, and enhanced economics.",
            ["integration", "renewable", "co-location", "hybrid", "control algorithms"],
            1.0
        ),
        SearchDocument(
            19,
            "Flow Battery Fundamentals",
            "Flow batteries store energy in liquid electrolytes, offering scalable capacity and long cycle life. Common chemistries include vanadium and zinc-bromine. Applications focus on grid-scale storage, renewable integration, and long-duration services.",
            ["flow battery", "electrolyte", "scalable", "cycle life", "grid-scale"],
            1.0
        ),
        SearchDocument(
            20,
            "Hydrogen Energy Storage",
            "Hydrogen storage converts electricity to hydrogen via electrolysis, storing it for later use. Applications include seasonal storage, grid balancing, and fuel cell integration. Challenges include efficiency, infrastructure, and safety.",
            ["hydrogen", "energy storage", "electrolysis", "seasonal", "fuel cell"],
            1.0
        ),
        SearchDocument(
            21,
            "Molten Salt Thermal Storage",
            "Molten salt stores thermal energy for power generation or industrial use. It is widely used in concentrated solar power plants. Key factors are thermal stability, insulation, and system integration.",
            ["molten salt", "thermal storage", "solar", "insulation", "integration"],
            1.0
        ),
        SearchDocument(
            22,
            "Battery Chemistry and Performance",
            "Battery chemistry determines energy density, cycle life, and safety. Lithium-ion, lead-acid, and flow batteries are common types. Performance metrics include capacity, efficiency, and degradation rate.",
            ["battery", "chemistry", "performance", "energy density", "degradation"],
            1.0
        ),
        SearchDocument(
            23,
            "Fire Protection in Battery Storage",
            "Fire protection in battery storage systems requires robust detection, suppression, and containment. Standards address risks from thermal runaway, electrical faults, and external hazards. Proper design and maintenance are critical.",
            ["fire protection", "battery", "thermal runaway", "standards", "maintenance"],
            1.0
        ),
        SearchDocument(
            24,
            "Energy Storage Asset Management",
            "Asset management involves monitoring, maintenance, and optimization of storage systems. Tools include performance analytics, predictive modeling, and warranty tracking. Effective management extends asset life and maximizes returns.",
            ["asset management", "monitoring", "maintenance", "optimization", "analytics"],
            1.0
        ),
        SearchDocument(
            25,
            "Revenue Stacking Strategies for Storage",
            "Revenue stacking combines multiple value streams, such as energy arbitrage, frequency regulation, and capacity payments. Strategies depend on market rules, system design, and operational flexibility. Maximizing returns requires careful planning and execution.",
            ["revenue stacking", "energy arbitrage", "frequency regulation", "capacity", "planning"],
            1.0
        ),
        SearchDocument(
            26,
            "Grid Interconnection Standards",
            "Grid interconnection standards define requirements for connecting storage systems to the grid. Compliance ensures safety, reliability, and interoperability. Key standards include IEEE 1547 and UL 9540.",
            ["grid interconnection", "standards", "IEEE 1547", "UL 9540", "compliance"],
            1.0
        ),
        SearchDocument(
            27,
            "Energy Storage Policy and Regulation",
            "Policy and regulation shape the deployment and operation of energy storage systems. Incentives, permitting, and market rules influence project economics and viability. Regulatory frameworks evolve with technology and market needs.",
            ["policy", "regulation", "incentives", "permitting", "market rules"],
            1.0
        ),
        SearchDocument(
            28,
            "Distributed Energy Storage Applications",
            "Distributed storage applications include backup power, peak shaving, and renewable integration. Systems are deployed at homes, businesses, and microgrids. Benefits include resilience, flexibility, and reduced transmission needs.",
            ["distributed", "energy storage", "backup", "peak shaving", "microgrid"],
            1.0
        ),
        SearchDocument(
            29,
            "Centralized Storage for Grid Reliability",
            "Centralized storage supports grid reliability by providing bulk energy, frequency regulation, and capacity. Large-scale assets are sited at substations or generation facilities. Challenges include transmission constraints and market participation.",
            ["centralized", "grid reliability", "bulk energy", "frequency regulation", "capacity"],
            1.0
        ),
        SearchDocument(
            30,
            "Energy Storage System Design Principles",
            "System design principles for energy storage include sizing, technology selection, control strategies, and integration. Design impacts performance, cost, and safety. Iterative optimization ensures alignment with project goals.",
            ["system design", "sizing", "technology selection", "control", "integration"],
            1.0
        ),
        SearchDocument(
            31,
            "Battery Storage Degradation and Maintenance",
            "Battery storage degradation is influenced by chemistry, cycling, temperature, and operating conditions. Maintenance strategies include monitoring, replacement, and warranty management. Accurate modeling supports asset longevity.",
            ["battery", "degradation", "maintenance", "monitoring", "warranty"],
            1.0
        ),
        SearchDocument(
            32,
            "Energy Storage Analytics and Optimization",
            "Analytics optimize storage operation through performance monitoring, predictive modeling, and benchmarking. Optimization improves efficiency, revenue, and asset life. Data-driven strategies support decision-making.",
            ["analytics", "optimization", "performance", "predictive modeling", "benchmarking"],
            1.0
        ),
        SearchDocument(
            33,
            "Fire Safety in Grid-Scale Storage",
            "Fire safety in grid-scale storage requires robust standards, detection systems, and emergency response planning. Technologies include fire suppression, containment, and thermal management. Regulatory compliance is essential.",
            ["fire safety", "grid-scale", "detection", "suppression", "containment"],
            1.0
        ),
        SearchDocument(
            34,
            "Energy Storage Cycle Life and Warranty",
            "Cycle life measures the number of charge/discharge cycles a storage system can endure. Warranty structures cover capacity, efficiency, and performance. Accurate cycle life prediction supports financial planning.",
            ["cycle life", "warranty", "capacity", "efficiency", "performance"],
            1.0
        ),
        SearchDocument(
            35,
            "Multi-Technology Storage Optimization",
            "Multi-technology optimization combines batteries, supercapacitors, and thermal storage for enhanced performance. Control algorithms manage dispatch, balancing power and energy needs. System design is critical for maximizing benefits.",
            ["multi-technology", "optimization", "control algorithms", "dispatch", "system design"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)