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
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.total_docs: int = 0
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]{2,}\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title) + self._tokenize(doc.content)
            length = len(tokens)
            self.doc_lengths[doc.id] = length
            tf = Counter(tokens)
            for term, freq in tf.items():
                self.inverted_index[term][doc.id] = freq
                self.doc_freqs[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

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

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = Counter(self._tokenize(doc.title) + self._tokenize(doc.content))
        for term in query_terms:
            if doc_id not in self.inverted_index.get(term, {}):
                continue
            f = tf[term]
            idf = self._compute_idf(term)
            denom = f + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * doc_len / (self.avg_doc_length + 1e-6))
            score += idf * (f * (self.bm25_k1 + 1)) / (denom + 1e-6)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf = Counter(self._tokenize(doc.title) + self._tokenize(doc.content))
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf_norm = tf[term] / (doc_len + 1e-6)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def _snippet(self, doc: SearchDocument, query_terms: List[str], max_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = []
        for i, token in enumerate(tokens):
            if token in query_terms:
                positions.append(i)
        if not positions:
            snippet = content[:max_len]
        else:
            start = max(positions[0] - 8, 0)
            end = min(start + 24, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        return snippet[:max_len].strip()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored: List[Tuple[float, int]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(query_terms, doc_id)
            tfidf_score = self._score_tfidf(query_terms, doc_id)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            scored.append((final_score, doc_id))
        scored.sort(reverse=True)
        results = []
        for score, doc_id in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.inverted_index),
        }

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            idx = SearchIndex()
            _preseed_documents(idx)
            _search_index_instance = idx
        return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            id=1,
            title="Northern White Sand Mine Selection Criteria",
            content="Key factors in selecting a Northern White sand mine include deposit quality, proximity to rail infrastructure, mine capacity, and compliance with API RP 19C standards.",
            tags=["mine selection", "northern white", "api", "quality"],
            weight=1.0
        ),
        SearchDocument(
            id=2,
            title="In-Basin Sand Economics in West Texas",
            content="In-basin sand offers cost advantages over Northern White due to lower transport costs. Economic analysis includes mine gate pricing, delivered cost per ton, and regional supply-demand balance.",
            tags=["in-basin", "economics", "west texas", "cost"],
            weight=1.0
        ),
        SearchDocument(
            id=3,
            title="API Specifications for Proppant Sand Quality",
            content="API RP 19C outlines specifications for proppant sand including sphericity, roundness, crush resistance, and turbidity. Compliance ensures optimal well performance.",
            tags=["api", "specifications", "sand quality"],
            weight=1.0
        ),
        SearchDocument(
            id=4,
            title="Proppant Logistics: Truck, Rail, and Transload",
            content="Efficient proppant logistics require coordination of truck fleets, rail shipments, and transload facilities. Key metrics include cycle times and demurrage minimization.",
            tags=["logistics", "truck", "rail", "transload"],
            weight=1.0
        ),
        SearchDocument(
            id=5,
            title="Last-Mile Delivery: Sand Hauling Truck Management",
            content="Managing sand hauling trucks involves route optimization, real-time GPS tracking, and coordination with wellsite schedules to minimize wait times and maximize asset utilization.",
            tags=["last-mile", "truck", "delivery"],
            weight=1.0
        ),
        SearchDocument(
            id=6,
            title="Wellsite Silo Management: Sand Storage Capacity",
            content="Silo management at the wellsite is critical for maintaining sufficient sand inventory. Monitoring fill levels and coordinating deliveries prevent non-productive time.",
            tags=["silo", "wellsite", "storage"],
            weight=1.0
        ),
        SearchDocument(
            id=7,
            title="Sand Conveyor Belt Delivery System Operations",
            content="Automated conveyor belt systems deliver sand from storage silos to blender units. System reliability and dust control are essential for safe operations.",
            tags=["conveyor", "belt", "delivery"],
            weight=1.0
        ),
        SearchDocument(
            id=8,
            title="Proppant On-Location Inventory Management",
            content="On-location inventory management tracks sand volumes, consumption rates, and re-order points, ensuring continuous frac operations and reducing excess inventory costs.",
            tags=["inventory", "on-location", "management"],
            weight=1.0
        ),
        SearchDocument(
            id=9,
            title="Multi-Well Pad Sand Logistics Coordination",
            content="Coordinating sand supply for multi-well pads requires advanced scheduling, buffer inventory, and real-time communication between logistics and frac crews.",
            tags=["multi-well", "pad", "coordination"],
            weight=1.0
        ),
        SearchDocument(
            id=10,
            title="Proppant Procurement: Contract and Spot Market Pricing",
            content="Procurement strategies balance long-term contracts and spot market purchases. Key considerations include price volatility, supplier reliability, and delivery terms.",
            tags=["procurement", "contract", "spot market"],
            weight=1.0
        ),
        SearchDocument(
            id=11,
            title="Sand Consumption Forecasting: Wells Per Month",
            content="Forecasting sand consumption uses planned wells per month, lateral lengths, and proppant intensity trends to optimize procurement and logistics.",
            tags=["forecasting", "consumption", "wells"],
            weight=1.0
        ),
        SearchDocument(
            id=12,
            title="Proppant Intensity Trends: Pounds Per Lateral Foot",
            content="Recent trends show increasing proppant intensity, measured in pounds per lateral foot, driving higher sand demand and influencing mine capacity planning.",
            tags=["intensity", "lateral", "trends"],
            weight=1.0
        ),
        SearchDocument(
            id=13,
            title="Regional Sand Supply Demand: Permian, Midland, Delaware",
            content="Permian Basin sand supply-demand dynamics are shaped by local mine production, well completion activity, and regional infrastructure constraints.",
            tags=["regional", "supply", "demand", "permian"],
            weight=1.0
        ),
        SearchDocument(
            id=14,
            title="Sand Mine Capacity Utilization and Market Dynamics",
            content="Mine capacity utilization rates impact delivered sand pricing and supply reliability. Market dynamics include new mine startups and consolidation trends.",
            tags=["mine", "capacity", "market"],
            weight=1.0
        ),
        SearchDocument(
            id=15,
            title="Proppant Cost Per Pound Delivered Economics",
            content="Delivered cost per pound of proppant includes mine gate price, rail/truck transport, transload fees, and last-mile delivery. Cost optimization is critical for frac economics.",
            tags=["cost", "delivered", "economics"],
            weight=1.0
        ),
        SearchDocument(
            id=16,
            title="Dual Fuel Truck Fleet: Diesel and CNG Operations",
            content="Dual fuel fleets using diesel and CNG reduce fuel costs and emissions. Fleet management focuses on refueling logistics and maintenance scheduling.",
            tags=["dual fuel", "truck", "cng"],
            weight=1.0
        ),
        SearchDocument(
            id=17,
            title="Sand Transload Facility: Rail to Truck Operations",
            content="Transload facilities transfer sand from railcars to trucks. Key factors include throughput capacity, dust mitigation, and truck turn times.",
            tags=["transload", "rail", "truck"],
            weight=1.0
        ),
        SearchDocument(
            id=18,
            title="Container POD Delivery System: Unit Train Operations",
            content="Container POD systems enable efficient unit train shipments and rapid unloading at wellsite or transload. System design impacts demurrage and logistics costs.",
            tags=["container", "pod", "unit train"],
            weight=1.0
        ),
        SearchDocument(
            id=19,
            title="Sand Quality Control: Wellsite Testing and Sampling",
            content="Quality control at the wellsite includes sieve analysis, crush resistance testing, and turbidity checks to ensure proppant meets API specifications.",
            tags=["quality", "control", "testing"],
            weight=1.0
        ),
        SearchDocument(
            id=20,
            title="Proppant Blending: On-The-Fly Mesh Mixing",
            content="On-the-fly blending of multiple sand mesh sizes optimizes fracture conductivity. Automated systems adjust blend ratios in real time based on job design.",
            tags=["blending", "mesh", "mixing"],
            weight=1.0
        ),
        SearchDocument(
            id=21,
            title="Deep Analysis: Sand Supply Chain Optimization",
            content="Comprehensive analysis of the sand supply chain identifies bottlenecks, cost drivers, and opportunities for efficiency improvements across mining, logistics, and wellsite operations.",
            tags=["analysis", "supply chain", "optimization"],
            weight=1.0
        ),
        SearchDocument(
            id=22,
            title="Frac Sand Railcar Fleet Management",
            content="Managing a dedicated railcar fleet for frac sand improves delivery reliability and reduces demurrage. Fleet tracking and maintenance are essential.",
            tags=["railcar", "fleet", "management"],
            weight=1.0
        ),
        SearchDocument(
            id=23,
            title="Sand Handling Safety Best Practices",
            content="Implementing safety protocols for sand handling reduces silica exposure and injury risk. Includes PPE, dust suppression, and equipment maintenance.",
            tags=["safety", "handling", "best practices"],
            weight=1.0
        ),
        SearchDocument(
            id=24,
            title="Permian Basin Sand Market Outlook",
            content="Market outlook for Permian Basin sand considers new mine capacity, demand growth from horizontal drilling, and competitive dynamics with Northern White sand.",
            tags=["permian", "market", "outlook"],
            weight=1.0
        ),
        SearchDocument(
            id=25,
            title="Sand Storage Solutions for Multi-Well Pads",
            content="Innovative sand storage solutions for multi-well pads include mobile silos, containerized storage, and automated inventory tracking systems.",
            tags=["storage", "multi-well", "solutions"],
            weight=1.0
        ),
        SearchDocument(
            id=26,
            title="Wellsite Sand Delivery Scheduling Algorithms",
            content="Advanced scheduling algorithms optimize sand delivery timing to minimize truck wait times and ensure continuous frac operations.",
            tags=["scheduling", "wellsite", "delivery"],
            weight=1.0
        ),
        SearchDocument(
            id=27,
            title="Sand Mine Environmental Compliance",
            content="Environmental compliance for sand mines covers air quality, water management, and land reclamation. Regulatory adherence is critical for permitting.",
            tags=["environmental", "compliance", "mine"],
            weight=1.0
        ),
        SearchDocument(
            id=28,
            title="Proppant Supply Chain Risk Management",
            content="Risk management in the proppant supply chain addresses disruptions from weather, rail congestion, and supplier insolvency.",
            tags=["risk", "supply chain", "management"],
            weight=1.0
        ),
        SearchDocument(
            id=29,
            title="Sand Hauling Truck Telematics",
            content="Telematics systems monitor truck location, speed, and idle time, enabling data-driven improvements in sand hauling efficiency.",
            tags=["telematics", "truck", "hauling"],
            weight=1.0
        ),
        SearchDocument(
            id=30,
            title="Frac Sand Procurement Digital Platforms",
            content="Digital procurement platforms streamline sourcing, contract management, and spot market transactions for frac sand buyers.",
            tags=["procurement", "digital", "platforms"],
            weight=1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)