import math
import threading
import re
import heapq
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

# --- Data Classes ---

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
        self.title = title
        self.content = content
        self.tags = tags
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id: str, score: float, title: str, snippet: str):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

# --- SearchIndex Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_map: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_doc_freq[term] += 1
                self.term_doc_map[term][doc.id] = freq
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self._update_avg_doc_length()

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove punctuation, split on whitespace
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        # BM25 idf formula
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        term_counts = self.term_doc_map
        for term in query_terms:
            freq = term_counts.get(term, {}).get(doc_id, 0)
            if freq == 0:
                continue
            idf = self._compute_idf(term)
            numerator = freq * (self._bm25_k1 + 1)
            denominator = freq + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_length / (self.avg_doc_length + 1e-9))
            score += idf * numerator / (denominator + 1e-9)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        doc = self.documents[doc_id]
        term_counts = self.term_doc_map
        for term in query_terms:
            freq = term_counts.get(term, {}).get(doc_id, 0)
            if freq == 0:
                continue
            tf = freq / (doc_length + 1e-9)
            idf = self._compute_idf(term)
            score += tf * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores = {}
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc_scores[doc_id] = score
        top_docs = heapq.nlargest(limit, doc_scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            return ' '.join(tokens[:length])
        start = max(indices[0] - 10, 0)
        end = min(start + length, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# --- Preseed Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="doc1",
            title="Optimal Frac Fleet Configuration: Pump Count and Horsepower",
            content="Determining the optimal pump count and horsepower for frac fleets involves balancing stage throughput, redundancy, and cost. Typical fleets range from 8 to 20 pumps, each rated at 2,500 to 5,000 HP. Higher horsepower enables greater pump rate capacity and flexibility for multi-well zipper operations.",
            tags=["configuration", "pump count", "horsepower", "fleet"],
            weight=1.0
        ),
        SearchDocument(
            id="doc2",
            title="Triplex vs Quintuplex Plunger Frac Pumps",
            content="Triplex pumps utilize three plungers, offering simplicity and easier maintenance, but quintuplex pumps with five plungers provide smoother flow and higher efficiency. Quintuplex designs reduce pulsation and wear, improving reliability and stage performance.",
            tags=["pump types", "triplex", "quintuplex", "plunger"],
            weight=1.0
        ),
        SearchDocument(
            id="doc3",
            title="Electric Frac Fleet (E-Frac) Direct Drive Turbine Technology",
            content="E-Frac fleets employ direct drive turbines powered by natural gas or field gas, reducing emissions and fuel costs. Electric pumps deliver consistent power, minimize downtime, and integrate seamlessly with SCADA systems for real-time monitoring.",
            tags=["e-frac", "electric", "turbine", "direct drive"],
            weight=1.1
        ),
        SearchDocument(
            id="doc4",
            title="Diesel Frac Fleet: Conventional and Tier 4 DGB",
            content="Diesel fleets use conventional engines or Tier 4 Dual Fuel (DGB) systems, allowing substitution of diesel with CNG or field gas. Tier 4 DGB reduces emissions, improves fuel economics, and supports regulatory compliance in environmentally sensitive regions.",
            tags=["diesel", "tier 4", "dgb", "dual fuel"],
            weight=1.0
        ),
        SearchDocument(
            id="doc5",
            title="Pump Rate Capacity: 100 BPM per Pump",
            content="Modern frac pumps typically achieve 100 barrels per minute (BPM) per unit, enabling high-rate stimulation and faster stage completion. Fleet configuration must ensure sufficient rate capacity for multi-well zipper operations and minimize non-productive time.",
            tags=["pump rate", "capacity", "bpm", "fleet"],
            weight=1.0
        ),
        SearchDocument(
            id="doc6",
            title="Treating Iron: High-Pressure Manifold and Missile",
            content="Treating iron assemblies, including high-pressure manifolds and missiles, are critical for safe fluid transfer during fracturing. Proper selection and maintenance prevent leaks, reduce downtime, and ensure compliance with safety standards.",
            tags=["treating iron", "manifold", "missile", "pressure"],
            weight=1.0
        ),
        SearchDocument(
            id="doc7",
            title="Blender Tub: Proppant Addition Rate and Mixing",
            content="The blender tub manages proppant addition and mixing with base fluid and chemicals. Accurate proppant metering and homogeneous mixing are essential for consistent fracture propagation and optimal stage performance.",
            tags=["blender", "proppant", "mixing", "addition rate"],
            weight=1.0
        ),
        SearchDocument(
            id="doc8",
            title="Hydration Unit: Gel Mixing and Chemical Addition",
            content="Hydration units facilitate gel mixing and chemical addition, ensuring proper viscosity and fluid properties for fracturing. Automated systems improve accuracy, reduce manual intervention, and enhance operational efficiency.",
            tags=["hydration", "gel", "chemical", "mixing"],
            weight=1.0
        ),
        SearchDocument(
            id="doc9",
            title="Data Van: Treatment Monitoring and SCADA Integration",
            content="The data van centralizes treatment monitoring, integrating with SCADA systems for real-time data acquisition, control, and reporting. Advanced analytics enable proactive troubleshooting and optimize stage design.",
            tags=["data van", "monitoring", "scada", "analytics"],
            weight=1.0
        ),
        SearchDocument(
            id="doc10",
            title="Wireline Operations: Plug Pump-Down and Gun Deployment",
            content="Wireline operations include plug pump-down and gun deployment for perforating and stage isolation. Efficient wireline logistics reduce cycle time and improve overall fleet productivity.",
            tags=["wireline", "plug", "gun", "deployment"],
            weight=1.0
        ),
        SearchDocument(
            id="doc11",
            title="Coiled Tubing: Milling, Drillout, and Cleanout",
            content="Coiled tubing is used for milling, drillout, and cleanout operations post-fracturing. High-reliability units minimize downtime and support rapid stage turnover in multi-well pads.",
            tags=["coiled tubing", "milling", "drillout", "cleanout"],
            weight=1.0
        ),
        SearchDocument(
            id="doc12",
            title="Frac Fleet Fuel Consumption: Diesel, CNG, and Field Gas",
            content="Fuel consumption analysis covers diesel, compressed natural gas (CNG), and field gas. Dual-fuel fleets optimize cost and reduce emissions, with substitution ratios tailored to local gas availability and economics.",
            tags=["fuel", "diesel", "cng", "field gas"],
            weight=1.0
        ),
        SearchDocument(
            id="doc13",
            title="Dual-Fuel Substitution Ratio and Field Gas Economics",
            content="Dual-fuel substitution ratios impact fleet economics and emissions. Field gas utilization lowers fuel costs, but requires infrastructure for gas processing and delivery. Economic models guide optimal substitution strategies.",
            tags=["dual fuel", "substitution", "economics", "field gas"],
            weight=1.0
        ),
        SearchDocument(
            id="doc14",
            title="Frac Fleet Mobilization, Demobilization, and Rig-Up",
            content="Mobilization and rig-up processes affect fleet readiness and stage throughput. Efficient logistics, crew scheduling, and equipment layout minimize setup time and maximize operational efficiency.",
            tags=["mobilization", "demobilization", "rig-up", "logistics"],
            weight=1.0
        ),
        SearchDocument(
            id="doc15",
            title="Pump Maintenance: Plunger, Fluid End, and Power End",
            content="Routine maintenance of plungers, fluid ends, and power ends extends pump life and reduces unplanned downtime. Predictive analytics and scheduled interventions optimize maintenance cycles and fleet reliability.",
            tags=["maintenance", "plunger", "fluid end", "power end"],
            weight=1.0
        ),
        SearchDocument(
            id="doc16",
            title="Equipment Reliability: MTBF and Pump Hours",
            content="Equipment reliability is measured by mean time between failures (MTBF) and cumulative pump hours. Reliability engineering improves fleet uptime, reduces NPT, and supports high stage-per-day rates.",
            tags=["reliability", "mtbf", "pump hours", "uptime"],
            weight=1.0
        ),
        SearchDocument(
            id="doc17",
            title="Frac Crew Scheduling: 24-Hour Operations and Shift Management",
            content="24-hour operations require effective crew scheduling and shift management. Balanced shift rotations, fatigue mitigation, and cross-training improve safety and productivity.",
            tags=["crew", "scheduling", "shift", "24-hour"],
            weight=1.0
        ),
        SearchDocument(
            id="doc18",
            title="Zipper Frac Operations: Simultaneous Multi-Well Stimulation",
            content="Zipper frac operations enable simultaneous stimulation of multiple wells, reducing cycle time and maximizing asset utilization. Coordinated logistics and real-time monitoring are essential for success.",
            tags=["zipper", "multi-well", "stimulation", "operations"],
            weight=1.0
        ),
        SearchDocument(
            id="doc19",
            title="Frac Fleet Efficiency: NPT Analysis and Stages per Day",
            content="Non-productive time (NPT) analysis identifies bottlenecks and inefficiencies in frac fleet operations. Optimizing stage-per-day rates improves asset utilization and reduces overall project costs.",
            tags=["efficiency", "npt", "stages per day", "analysis"],
            weight=1.0
        ),
        SearchDocument(
            id="doc20",
            title="Frac Fleet Cost per Stage and Market Pricing Trends",
            content="Cost per stage is influenced by fleet configuration, fuel choice, maintenance, and market pricing trends. Benchmarking against regional data supports competitive pricing and margin optimization.",
            tags=["cost", "stage", "pricing", "market"],
            weight=1.0
        ),
        SearchDocument(
            id="doc21",
            title="Multi-Doctrine Synthesis: Integrating Fleet Technologies",
            content="Synthesizing multiple doctrines involves integrating electric and diesel fleets, optimizing pump types, and leveraging real-time data for operational decision-making. Hybrid approaches maximize flexibility and performance.",
            tags=["multi-doctrine", "synthesis", "integration", "fleet"],
            weight=1.0
        ),
        SearchDocument(
            id="doc22",
            title="SCADA Integration for Frac Fleet Optimization",
            content="SCADA integration enables automated control and monitoring of frac fleet equipment. Real-time data acquisition supports predictive maintenance, operational efficiency, and rapid troubleshooting.",
            tags=["scada", "integration", "optimization", "data"],
            weight=1.0
        ),
        SearchDocument(
            id="doc23",
            title="Field Gas Processing and Delivery Infrastructure",
            content="Field gas processing infrastructure is essential for dual-fuel fleets. Gas conditioning, compression, and delivery systems must be reliable and scalable to support continuous operations.",
            tags=["field gas", "processing", "delivery", "infrastructure"],
            weight=1.0
        ),
        SearchDocument(
            id="doc24",
            title="Stage Design Optimization in Frac Operations",
            content="Stage design optimization leverages data analytics, pump configuration, and proppant selection to maximize reservoir stimulation. Adaptive designs respond to real-time feedback and geological variability.",
            tags=["stage design", "optimization", "analytics", "proppant"],
            weight=1.0
        ),
        SearchDocument(
            id="doc25",
            title="Regulatory Compliance in Frac Fleet Operations",
            content="Regulatory compliance requires adherence to environmental, safety, and emissions standards. Tier 4 DGB and electric fleets support compliance, while documentation and reporting ensure audit readiness.",
            tags=["regulatory", "compliance", "emissions", "safety"],
            weight=1.0
        ),
        SearchDocument(
            id="doc26",
            title="Frac Fleet Logistics: Equipment Layout and Pad Design",
            content="Efficient equipment layout and pad design reduce mobilization time and improve safety. Strategic placement of pumps, treating iron, and data vans streamlines operations and minimizes risk.",
            tags=["logistics", "layout", "pad design", "equipment"],
            weight=1.0
        ),
        SearchDocument(
            id="doc27",
            title="Advanced Analytics for Frac Fleet Performance",
            content="Advanced analytics drive performance improvements in frac fleets. Machine learning models predict maintenance needs, optimize stage design, and identify operational bottlenecks.",
            tags=["analytics", "performance", "machine learning", "optimization"],
            weight=1.0
        ),
        SearchDocument(
            id="doc28",
            title="Frac Fleet Safety Protocols and Incident Response",
            content="Safety protocols and incident response plans are critical for frac fleet operations. Regular training, equipment inspections, and emergency drills minimize risk and ensure regulatory compliance.",
            tags=["safety", "protocols", "incident", "response"],
            weight=1.0
        ),
        SearchDocument(
            id="doc29",
            title="Fleet Redundancy and Backup Strategies",
            content="Fleet redundancy, including backup pumps and spare parts, ensures continuous operations during equipment failures. Redundant systems minimize downtime and support high stage-per-day rates.",
            tags=["redundancy", "backup", "operations", "fleet"],
            weight=1.0
        ),
        SearchDocument(
            id="doc30",
            title="Proppant Logistics and Inventory Management",
            content="Proppant logistics and inventory management are essential for uninterrupted fracturing operations. Automated tracking and real-time inventory updates reduce supply chain disruptions.",
            tags=["proppant", "logistics", "inventory", "management"],
            weight=1.0
        ),
        SearchDocument(
            id="doc31",
            title="Frac Fleet Environmental Impact Assessment",
            content="Environmental impact assessment evaluates emissions, water usage, and waste management in frac fleet operations. Electric fleets and dual-fuel systems reduce environmental footprint.",
            tags=["environmental", "impact", "assessment", "emissions"],
            weight=1.0
        ),
        SearchDocument(
            id="doc32",
            title="Pump Selection Criteria for Frac Fleet Design",
            content="Pump selection criteria include horsepower, rate capacity, reliability, and maintenance requirements. Matching pump types to operational needs maximizes fleet efficiency.",
            tags=["pump selection", "criteria", "design", "fleet"],
            weight=1.0
        ),
        SearchDocument(
            id="doc33",
            title="Chemical Management in Frac Operations",
            content="Chemical management covers storage, handling, and dosing systems for fracturing fluids. Automated dosing improves accuracy and safety, while compliance protocols ensure regulatory adherence.",
            tags=["chemical", "management", "dosing", "compliance"],
            weight=1.0
        ),
        SearchDocument(
            id="doc34",
            title="Real-Time Monitoring and Troubleshooting",
            content="Real-time monitoring enables rapid troubleshooting of frac fleet equipment. Integrated sensors and analytics platforms detect anomalies and support proactive maintenance.",
            tags=["monitoring", "troubleshooting", "real-time", "analytics"],
            weight=1.0
        ),
        SearchDocument(
            id="doc35",
            title="Frac Fleet Crew Training and Certification",
            content="Crew training and certification programs ensure operational readiness and safety. Ongoing education and skills development reduce incidents and improve fleet performance.",
            tags=["crew", "training", "certification", "safety"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)