import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# -----------------------------
# Data Classes
# -----------------------------

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

# -----------------------------
# Search Index Implementation
# -----------------------------

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.N: int = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_norms: Dict[int, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            tf = Counter(tokens)
            self.doc_lengths[doc.id] = len(tokens)
            for term, freq in tf.items():
                self.inverted_index[term][doc.id] = freq
                self.doc_freqs[term] += 1
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_norms.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_tokens: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = Counter(self._tokenize(doc.title + ' ' + doc.content))
        score = 0.0
        for term in query_tokens:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            score += idf * freq * (self.k1 + 1) / (denom + 1e-10)
        return score * doc.weight

    def _score_tfidf(self, query_tokens: List[str], doc_id: int) -> float:
        tf = Counter(self._tokenize(self.documents[doc_id].title + ' ' + self.documents[doc_id].content))
        doc_len = self.doc_lengths[doc_id]
        norm = self._tfidf_norms.get(doc_id)
        if norm is None:
            norm = 0.0
            for term, freq in tf.items():
                idf = self._compute_idf(term)
                norm += ((freq / doc_len) * idf) ** 2
            norm = math.sqrt(norm)
            self._tfidf_norms[doc_id] = norm
        score = 0.0
        for term in query_tokens:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            idf = self._compute_idf(term)
            score += (freq / doc_len) * idf
        return (score / (norm + 1e-10)) * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        candidate_docs = set()
        for term in query_tokens:
            candidate_docs.update(self.inverted_index.get(term, {}).keys())
        scored: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            if use_bm25:
                score = self._score_bm25(query_tokens, doc_id)
            else:
                score = self._score_tfidf(query_tokens, doc_id)
            if score > 0:
                scored.append((doc_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            return content[:160] + '...' if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(r'\b(' + re.escape(qt) + r')\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + '...'

    def get_stats(self) -> Dict[str, int]:
        return {
            'documents': self.N,
            'unique_terms': len(self.inverted_index),
            'avg_doc_length': int(self.avg_doc_length)
        }

# -----------------------------
# Singleton Factory
# -----------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# -----------------------------
# Pre-seeded Domain Documents
# -----------------------------

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "LFP vs NMC: Chemistry Selection for Grid-Scale BESS",
            "Lithium Iron Phosphate (LFP) and Nickel Manganese Cobalt (NMC) are the leading chemistries for grid-scale battery energy storage systems (BESS). LFP offers superior thermal stability, lower cost, and longer cycle life, while NMC provides higher energy density. Selection depends on project requirements such as safety, footprint, and total cost of ownership.",
            ["chemistry", "LFP", "NMC", "selection"],
            1.0
        ),
        SearchDocument(
            2,
            "Battery Management System (BMS) Cell Balancing Strategies",
            "Cell balancing in BMS ensures uniform state of charge across all cells, maximizing usable capacity and lifespan. Passive balancing dissipates excess energy as heat, while active balancing redistributes charge. Grid-scale BESS typically use passive balancing for simplicity and cost, but active methods are considered for high-value applications.",
            ["BMS", "cell balancing", "passive", "active"],
            1.0
        ),
        SearchDocument(
            3,
            "State of Charge Estimation Using Extended Kalman Filter",
            "The Extended Kalman Filter (EKF) is widely used for accurate state of charge (SOC) estimation in lithium-ion batteries. EKF models battery dynamics and updates SOC estimates based on voltage and current measurements, improving reliability in grid-scale BESS operation.",
            ["SOC", "EKF", "estimation", "battery"],
            1.0
        ),
        SearchDocument(
            4,
            "Grid-Scale BESS Sizing for 4-Hour Duration Standard",
            "Sizing grid-scale BESS for a 4-hour duration involves calculating the required energy and power capacity to meet grid services. Factors include load profiles, round-trip efficiency, and degradation over time. Proper sizing ensures compliance with utility and market requirements.",
            ["sizing", "4-hour", "duration", "grid"],
            1.0
        ),
        SearchDocument(
            5,
            "SEI Layer Growth and Capacity Fade Mechanisms",
            "Solid Electrolyte Interphase (SEI) layer growth on the anode is a primary cause of capacity fade in lithium-ion batteries. SEI formation consumes lithium and increases cell impedance, accelerated by high temperatures and cycling. Understanding SEI dynamics is crucial for BESS longevity.",
            ["SEI", "capacity fade", "degradation"],
            1.0
        ),
        SearchDocument(
            6,
            "Thermal Runaway Propagation and NFPA 855 Compliance",
            "Thermal runaway in BESS can propagate between cells and modules, leading to catastrophic failure. NFPA 855 sets safety standards for installation, requiring fire barriers, gas detection, and thermal management to mitigate propagation risks.",
            ["thermal runaway", "NFPA 855", "safety"],
            1.0
        ),
        SearchDocument(
            7,
            "Levelized Cost of Storage (LCOS) Economic Analysis",
            "LCOS is a key metric for evaluating the economic viability of grid-scale BESS. It accounts for capital cost, operating expenses, degradation, and revenue streams over the system's lifetime. Lower LCOS indicates better cost-effectiveness for storage projects.",
            ["LCOS", "economics", "cost"],
            1.0
        ),
        SearchDocument(
            8,
            "Investment Tax Credit and Inflation Reduction Act Benefits",
            "The Investment Tax Credit (ITC) and Inflation Reduction Act (IRA) provide significant incentives for BESS deployment. ITC allows a percentage of capital cost to be credited, while IRA includes additional credits for domestic content and energy communities.",
            ["ITC", "IRA", "incentives"],
            1.0
        ),
        SearchDocument(
            9,
            "Frequency Regulation Service Revenue and Performance Requirements",
            "Grid-scale BESS can participate in frequency regulation markets, earning revenue by rapidly injecting or absorbing power. Performance requirements include response time, accuracy, and sustained output. Market participation depends on system design and controls.",
            ["frequency regulation", "revenue", "performance"],
            1.0
        ),
        SearchDocument(
            10,
            "Cylindrical vs Prismatic vs Pouch Cell Format Selection",
            "Cell format impacts BESS design, safety, and cost. Cylindrical cells offer robust mechanical properties, prismatic cells provide higher packing efficiency, and pouch cells enable flexible layouts. Selection depends on application, integration, and manufacturer.",
            ["cell format", "cylindrical", "prismatic", "pouch"],
            1.0
        ),
        SearchDocument(
            11,
            "Grid-Forming vs Grid-Following Inverter Control Strategies",
            "Grid-forming inverters can establish voltage and frequency, enabling islanded operation, while grid-following inverters synchronize with the existing grid. Advanced BESS projects may require grid-forming capabilities for black start and microgrid support.",
            ["inverter", "grid-forming", "grid-following"],
            1.0
        ),
        SearchDocument(
            12,
            "State of Health Estimation and Remaining Useful Life Prediction",
            "State of Health (SOH) estimation assesses battery degradation and predicts remaining useful life (RUL). Methods include coulomb counting, impedance tracking, and machine learning. Accurate SOH is essential for BESS maintenance and warranty planning.",
            ["SOH", "RUL", "estimation"],
            1.0
        ),
        SearchDocument(
            13,
            "HVAC Thermal Management System Design for Container-Based BESS",
            "Effective HVAC design is critical for containerized BESS to maintain optimal temperature and prevent thermal runaway. Strategies include air and liquid cooling, redundancy, and integration with fire suppression systems.",
            ["HVAC", "thermal management", "container"],
            1.0
        ),
        SearchDocument(
            14,
            "Augmentation vs Full Replacement Strategy for Degraded Systems",
            "As BESS degrade, operators can choose between augmenting with new modules or full system replacement. Augmentation extends life and reduces cost, but may introduce complexity in controls and warranties.",
            ["augmentation", "replacement", "degradation"],
            1.0
        ),
        SearchDocument(
            15,
            "UL 9540A Thermal Runaway Testing Protocol and Pass Criteria",
            "UL 9540A outlines test methods for evaluating thermal runaway in BESS. Passing criteria include containment of fire, prevention of propagation, and gas emission limits. Compliance is required for permitting and insurance.",
            ["UL 9540A", "thermal runaway", "testing"],
            1.0
        ),
        SearchDocument(
            16,
            "Energy Arbitrage Revenue Optimization and Market Volatility",
            "BESS can optimize energy arbitrage by charging during low-price periods and discharging during high-price events. Market volatility increases revenue potential but requires advanced forecasting and dispatch algorithms.",
            ["arbitrage", "market", "optimization"],
            1.0
        ),
        SearchDocument(
            17,
            "Battery Cell Degradation: Calendar vs Cycle Aging",
            "Battery degradation occurs due to calendar aging (time-based) and cycle aging (usage-based). Calendar aging is driven by temperature and SOC, while cycle aging depends on depth of discharge and charge rates.",
            ["degradation", "calendar aging", "cycle aging"],
            1.0
        ),
        SearchDocument(
            18,
            "Fire Suppression Systems for Grid-Scale BESS",
            "Fire suppression in BESS includes clean agent systems, water mist, and aerosol-based solutions. Integration with detection and HVAC is essential for rapid response and compliance with NFPA 855.",
            ["fire suppression", "BESS", "NFPA 855"],
            1.0
        ),
        SearchDocument(
            19,
            "Round-Trip Efficiency and System Losses in BESS",
            "Round-trip efficiency measures the ratio of energy output to input in BESS, accounting for inverter, HVAC, and battery losses. High efficiency improves project economics and reduces operational costs.",
            ["efficiency", "losses", "economics"],
            1.0
        ),
        SearchDocument(
            20,
            "Black Start Capability with Grid-Forming Inverters",
            "Grid-forming inverters enable black start, allowing BESS to energize a dead grid without external reference. This is critical for grid resilience and microgrid applications.",
            ["black start", "grid-forming", "inverter"],
            1.0
        ),
        SearchDocument(
            21,
            "Battery Warranty Terms and Performance Guarantees",
            "BESS warranties specify guaranteed capacity retention, cycle life, and response time. Performance guarantees impact LCOS and project bankability. Understanding warranty terms is essential for risk management.",
            ["warranty", "guarantee", "performance"],
            1.0
        ),
        SearchDocument(
            22,
            "Containerization and Modularization in BESS Deployment",
            "Containerized and modular BESS designs enable rapid deployment, scalability, and simplified logistics. Standardized containers support efficient transportation and installation.",
            ["container", "modular", "deployment"],
            1.0
        ),
        SearchDocument(
            23,
            "Battery Safety Standards: UL 1973, UL 9540, and IEC 62619",
            "Compliance with safety standards such as UL 1973, UL 9540, and IEC 62619 is mandatory for BESS. These standards cover cell, module, and system-level safety requirements.",
            ["UL 1973", "UL 9540", "IEC 62619", "safety"],
            1.0
        ),
        SearchDocument(
            24,
            "Revenue Stacking: Multiple Value Streams for BESS",
            "BESS can stack revenue from multiple services such as frequency regulation, energy arbitrage, and capacity markets. Revenue stacking improves project economics but requires advanced controls.",
            ["revenue stacking", "value streams", "BESS"],
            1.0
        ),
        SearchDocument(
            25,
            "Battery System Integration with SCADA and EMS",
            "Integration with SCADA and Energy Management Systems (EMS) enables real-time monitoring, control, and optimization of BESS operations. Data analytics support predictive maintenance and performance improvement.",
            ["SCADA", "EMS", "integration"],
            1.0
        ),
        SearchDocument(
            26,
            "Battery Recycling and End-of-Life Management",
            "End-of-life management for BESS includes recycling, repurposing, and safe disposal. Regulatory compliance and circular economy principles are increasingly important for project developers.",
            ["recycling", "end-of-life", "management"],
            1.0
        ),
        SearchDocument(
            27,
            "Impact of Depth of Discharge on Battery Lifespan",
            "Depth of discharge (DoD) significantly affects battery cycle life. Shallow cycles extend lifespan, while deep discharges accelerate degradation. BESS operation strategies should optimize DoD for longevity.",
            ["depth of discharge", "lifespan", "degradation"],
            1.0
        ),
        SearchDocument(
            28,
            "Cybersecurity Considerations for Grid-Scale BESS",
            "Cybersecurity is critical for BESS connected to the grid. Threats include unauthorized access, data breaches, and control system manipulation. Best practices involve network segmentation, encryption, and regular security audits.",
            ["cybersecurity", "BESS", "security"],
            1.0
        ),
        SearchDocument(
            29,
            "Battery Module Fire Testing and Certification",
            "Fire testing of battery modules is required for certification and permitting. Tests evaluate thermal runaway, fire propagation, and suppression effectiveness according to standards such as UL 9540A.",
            ["fire testing", "certification", "UL 9540A"],
            1.0
        ),
        SearchDocument(
            30,
            "Advanced Forecasting for BESS Dispatch Optimization",
            "Forecasting algorithms improve BESS dispatch by predicting load, price, and renewable generation. Machine learning and statistical models enhance revenue and reduce operational risk.",
            ["forecasting", "dispatch", "optimization"],
            1.0
        ),
        SearchDocument(
            31,
            "BESS Project Development Timeline and Milestones",
            "A typical BESS project includes feasibility studies, permitting, procurement, construction, commissioning, and operation. Understanding the timeline helps manage risks and stakeholder expectations.",
            ["project", "development", "timeline"],
            1.0
        ),
        SearchDocument(
            32,
            "Impact of Ambient Temperature on BESS Performance",
            "Ambient temperature affects battery performance, degradation, and safety. HVAC systems and thermal insulation are necessary to maintain optimal operating conditions in grid-scale BESS.",
            ["temperature", "performance", "HVAC"],
            1.0
        ),
        SearchDocument(
            33,
            "BESS Controls: Power Conversion System (PCS) Integration",
            "The Power Conversion System (PCS) manages energy flow between the grid and batteries. Integration with BMS and EMS ensures safe, efficient, and reliable operation.",
            ["PCS", "controls", "integration"],
            1.0
        ),
        SearchDocument(
            34,
            "BESS Decommissioning and Site Remediation",
            "Decommissioning involves safe removal of batteries, recycling, and site remediation. Planning for end-of-life reduces environmental impact and supports regulatory compliance.",
            ["decommissioning", "remediation", "end-of-life"],
            1.0
        ),
        SearchDocument(
            35,
            "BESS Asset Management and Performance Monitoring",
            "Asset management systems track BESS performance, schedule maintenance, and optimize lifecycle costs. Real-time monitoring enables early detection of faults and performance issues.",
            ["asset management", "monitoring", "performance"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)