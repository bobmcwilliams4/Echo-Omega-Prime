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
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, List[int]] = defaultdict(list)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].append(doc.id)
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self.inverted_index.get(term, []))
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            score = bm25_score * 0.7 + tfidf_score * 0.3
            score *= doc.weight
            scored_results.append((doc_id, score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.total_docs,
                "average_document_length": self.avg_doc_length,
                "unique_terms": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        tf = self.term_freqs.get(doc_id, {})
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + k1 * (1 - b + b * doc_len / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            score += idf * (f * (k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs.get(doc_id, {})
        doc_len = self.doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in query_terms:
            tf_norm = tf.get(term, 0) / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:160]
            return snippet + "..." if len(content) > 160 else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet + "..."

def get_search_index() -> SearchIndex:
    if not hasattr(get_search_index, "_instance"):
        get_search_index._instance = SearchIndex()
        _preseed_documents(get_search_index._instance)
    return get_search_index._instance

def _preseed_documents(idx: SearchIndex):
    if getattr(idx, "_preseeded", False):
        return
    docs = [
        SearchDocument(
            1,
            "UIC 406 Line Capacity Methodology",
            "The UIC 406 methodology provides a standardized approach for evaluating rail line capacity by segmenting the network and analyzing occupancy. It supports capacity enhancement decisions and identifies bottlenecks.",
            ["UIC406", "capacity", "bottleneck", "methodology"],
            1.0
        ),
        SearchDocument(
            2,
            "Train Performance Calculation (TPC Curves)",
            "Train Performance Calculation (TPC) curves are essential for simulating train movement, energy consumption, and running times. They account for gradients, resistance, and traction characteristics.",
            ["TPC", "performance", "simulation", "energy"],
            1.0
        ),
        SearchDocument(
            3,
            "Intermodal Terminal Capacity and Design",
            "Intermodal terminal capacity analysis involves evaluating yard layout, crane productivity, track configuration, and dwell times to optimize throughput and minimize congestion.",
            ["intermodal", "terminal", "capacity", "design"],
            1.0
        ),
        SearchDocument(
            4,
            "Centralized Traffic Control (CTC) Dispatching Optimization",
            "CTC systems centralize train routing and signaling, enabling efficient dispatching and conflict resolution. Optimization algorithms can minimize delays and maximize network throughput.",
            ["CTC", "dispatch", "optimization", "signaling"],
            1.0
        ),
        SearchDocument(
            5,
            "Benefit-Cost Analysis for Rail Infrastructure Investment",
            "Benefit-cost analysis (BCA) quantifies the economic viability of rail projects by comparing discounted benefits and costs, including travel time savings, accident reduction, and environmental impacts.",
            ["BCA", "investment", "economics", "infrastructure"],
            1.0
        ),
        SearchDocument(
            6,
            "Double-Stack Clearance Requirements",
            "Double-stack container trains require sufficient vertical and horizontal clearance. Clearance analysis includes structure gauging, bridge modifications, and tunnel improvements.",
            ["double-stack", "clearance", "container", "infrastructure"],
            1.0
        ),
        SearchDocument(
            7,
            "Rail Yard Classification and Design",
            "Classification yards sort railcars by destination using hump or flat switching. Design factors include track layout, automation, and throughput requirements.",
            ["yard", "classification", "design", "switching"],
            1.0
        ),
        SearchDocument(
            8,
            "Grade Crossing Elimination and Priority Ranking",
            "Eliminating grade crossings improves safety and reduces delays. Priority ranking considers accident history, traffic volumes, and community impact.",
            ["grade crossing", "elimination", "safety", "priority"],
            1.0
        ),
        SearchDocument(
            9,
            "Network Simulation with RailSys and OpenTrack",
            "Rail network simulation tools like RailSys and OpenTrack model train operations, schedule adherence, and infrastructure utilization for capacity planning.",
            ["simulation", "RailSys", "OpenTrack", "capacity"],
            1.0
        ),
        SearchDocument(
            10,
            "Short Line Railroad Economics and Viability",
            "Short line railroads connect rural industries to the main network. Economic analysis includes traffic base, operating costs, and public-private partnerships.",
            ["short line", "economics", "viability", "operations"],
            1.0
        ),
        SearchDocument(
            11,
            "Class I Railroad Operations Planning and PSR",
            "Precision Scheduled Railroading (PSR) emphasizes scheduled operations, asset utilization, and network fluidity for Class I railroads.",
            ["Class I", "PSR", "operations", "planning"],
            1.0
        ),
        SearchDocument(
            12,
            "Positive Train Control (PTC) Implementation and Impact",
            "PTC systems prevent train-to-train collisions, overspeed derailments, and unauthorized movements. Implementation challenges include interoperability and cost.",
            ["PTC", "safety", "implementation", "technology"],
            1.0
        ),
        SearchDocument(
            13,
            "Rail Corridor Environmental Impact Assessment",
            "Environmental impact assessments (EIA) for rail corridors address noise, vibration, air quality, and ecological effects, supporting regulatory compliance.",
            ["environmental", "EIA", "corridor", "assessment"],
            1.0
        ),
        SearchDocument(
            14,
            "Rail Infrastructure Financing Mechanisms",
            "Financing options for rail infrastructure include public grants, private investment, tax credits, and innovative mechanisms like public-private partnerships.",
            ["financing", "infrastructure", "PPP", "investment"],
            1.0
        ),
        SearchDocument(
            15,
            "Rail Freight Demand Forecasting Methodology",
            "Freight demand forecasting uses econometric models, commodity flow analysis, and scenario planning to predict rail traffic growth.",
            ["freight", "demand", "forecasting", "methodology"],
            1.0
        ),
        SearchDocument(
            16,
            "Passenger Rail Service Planning and Operating Cost Estimation",
            "Passenger rail planning balances service frequency, rolling stock, and fare policy. Cost estimation considers crew, energy, maintenance, and capital expenses.",
            ["passenger", "planning", "cost", "service"],
            1.0
        ),
        SearchDocument(
            17,
            "Rail Bridge Load Rating and Replacement Priority",
            "Load rating evaluates bridge capacity for modern rail traffic. Replacement priority is based on structural condition, age, and network criticality.",
            ["bridge", "load rating", "replacement", "priority"],
            1.0
        ),
        SearchDocument(
            18,
            "Rail Electrification Feasibility and Economics",
            "Electrification feasibility considers capital costs, energy prices, traffic density, and emissions reduction. Economic analysis compares lifecycle costs to diesel.",
            ["electrification", "feasibility", "economics", "energy"],
            1.0
        ),
        SearchDocument(
            19,
            "Rail Network Resilience and Disaster Recovery",
            "Resilience planning addresses natural hazards, redundancy, and rapid recovery. Strategies include hardening infrastructure and emergency response protocols.",
            ["resilience", "disaster", "recovery", "network"],
            1.0
        ),
        SearchDocument(
            20,
            "Rail Corridor Land Use and Transit-Oriented Development (TOD)",
            "TOD integrates land use planning with rail infrastructure to promote walkable, mixed-use communities and increase ridership.",
            ["TOD", "land use", "corridor", "development"],
            1.0
        ),
        SearchDocument(
            21,
            "Rail Safety Performance Metrics and FRA Reporting",
            "Safety metrics include accident rates, employee injuries, and regulatory compliance. FRA reporting ensures transparency and continuous improvement.",
            ["safety", "FRA", "metrics", "reporting"],
            1.0
        ),
        SearchDocument(
            22,
            "High-Speed Rail Corridor Planning and Engineering Standards",
            "High-speed rail planning involves alignment selection, geometric standards, and system integration for speeds above 250 km/h.",
            ["high-speed", "corridor", "planning", "engineering"],
            1.0
        ),
        SearchDocument(
            23,
            "Rail Infrastructure Asset Management and Life-Cycle Costing",
            "Asset management systems track infrastructure condition, maintenance, and renewal costs. Life-cycle costing optimizes long-term investment.",
            ["asset management", "life-cycle", "costing", "infrastructure"],
            1.0
        ),
        SearchDocument(
            24,
            "Rail Cybersecurity and SCADA System Protection",
            "Railway cybersecurity protects SCADA and signaling systems from cyber threats. Measures include network segmentation, intrusion detection, and staff training.",
            ["cybersecurity", "SCADA", "protection", "signaling"],
            1.0
        ),
        SearchDocument(
            25,
            "Rail Labor Agreements and Crew Scheduling Optimization",
            "Labor agreements affect crew scheduling, work rules, and cost. Optimization models minimize crew costs while meeting regulatory and contractual constraints.",
            ["labor", "crew", "scheduling", "optimization"],
            1.0
        ),
        SearchDocument(
            26,
            "Rail Network Bottleneck Analysis",
            "Bottleneck analysis identifies capacity constraints using train movement data, occupancy modeling, and simulation to prioritize investments.",
            ["bottleneck", "capacity", "analysis", "simulation"],
            1.0
        ),
        SearchDocument(
            27,
            "Rail Electrification System Design Standards",
            "Design standards for rail electrification address voltage selection, catenary design, and substation placement for reliable operations.",
            ["electrification", "design", "standards", "system"],
            1.0
        ),
        SearchDocument(
            28,
            "Rail Environmental Mitigation Strategies",
            "Mitigation strategies for rail projects include noise barriers, wildlife crossings, and stormwater management to reduce environmental impacts.",
            ["environmental", "mitigation", "rail", "strategy"],
            1.0
        ),
        SearchDocument(
            29,
            "Rail Corridor Right-of-Way Acquisition",
            "Right-of-way acquisition involves legal, environmental, and community considerations to secure land for new rail corridors.",
            ["right-of-way", "acquisition", "corridor", "land"],
            1.0
        ),
        SearchDocument(
            30,
            "Rail System Redundancy and Reliability Planning",
            "Redundancy planning ensures alternative routes and backup systems are available to maintain service during disruptions.",
            ["redundancy", "reliability", "planning", "system"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)
    idx._preseeded = True