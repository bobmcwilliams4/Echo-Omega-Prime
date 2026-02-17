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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_map: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}
        self._re_token = re.compile(r'\b\w+\b')
        self._stats = {
            'total_docs': 0,
            'avg_doc_length': 0.0,
            'unique_terms': 0
        }

    def _tokenize(self, text: str) -> List[str]:
        tokens = self._re_token.findall(text.lower())
        return tokens

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
            self._update_stats()

    def _update_stats(self):
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.total_docs if self.total_docs > 0 else 0.0
        self._stats['total_docs'] = self.total_docs
        self._stats['avg_doc_length'] = self.avg_doc_length
        self._stats['unique_terms'] = len(self.term_doc_freq)

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        term_counts = self.term_doc_map
        for term in query_terms:
            if doc_id not in term_counts.get(term, {}):
                continue
            tf = term_counts[term][doc_id]
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        term_counts = self.term_doc_map
        tfidf_score = 0.0
        for term in query_terms:
            tf = term_counts.get(term, {}).get(doc_id, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            tfidf_score += tf_norm * idf
        return tfidf_score * doc.weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = {}
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        indices = []
        for i, token in enumerate(tokens):
            if token in query_terms:
                indices.append(i)
        if not indices:
            snippet = ' '.join(tokens[:length])
        else:
            start = max(indices[0] - 10, 0)
            end = min(start + length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return dict(self._stats)

# Singleton factory for SearchIndex
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Amine Scrubbing for Post-Combustion CO2 Capture",
            "Amine scrubbing is a widely used technology for capturing CO2 from flue gas after combustion. Monoethanolamine (MEA) is a common solvent. The process involves absorption, regeneration, and solvent recycling.",
            ["post-combustion", "amine", "scrubbing", "MEA", "CO2 capture"],
            1.0
        ),
        SearchDocument(
            2,
            "Pre-Combustion CO2 Capture in IGCC with Shift Reactor",
            "Integrated Gasification Combined Cycle (IGCC) plants use a shift reactor to convert CO into CO2 and H2. CO2 is separated before combustion, enabling efficient capture and storage.",
            ["pre-combustion", "IGCC", "shift reactor", "CO2 capture"],
            1.0
        ),
        SearchDocument(
            3,
            "Direct Air Capture with Solid Sorbent Technology",
            "Solid sorbents such as amine-functionalized materials are used to capture CO2 directly from ambient air. The process involves adsorption, regeneration, and CO2 collection.",
            ["direct air capture", "solid sorbent", "CO2", "adsorption"],
            1.0
        ),
        SearchDocument(
            4,
            "Direct Air Capture with Liquid Solvent (Alkaline Solution)",
            "Liquid solvents, typically alkaline solutions like sodium hydroxide, absorb CO2 from air. The process includes absorption, regeneration, and CO2 recovery.",
            ["direct air capture", "liquid solvent", "alkaline", "CO2"],
            1.0
        ),
        SearchDocument(
            5,
            "CO2 Pipeline Transport in Dense Phase",
            "CO2 is transported via pipelines in a dense phase to optimize efficiency and minimize leaks. Pipeline design considers pressure, temperature, and material compatibility.",
            ["CO2 transport", "pipeline", "dense phase", "pressure"],
            1.0
        ),
        SearchDocument(
            6,
            "Geological CO2 Storage in Deep Saline Aquifers",
            "Deep saline aquifers are geological formations suitable for long-term CO2 storage. Injection wells, monitoring, and verification are critical for safe sequestration.",
            ["CO2 storage", "saline aquifer", "geological", "injection"],
            1.0
        ),
        SearchDocument(
            7,
            "CO2 Enhanced Oil Recovery (EOR) and Incidental Storage",
            "CO2 EOR involves injecting CO2 into oil reservoirs to boost recovery and incidentally store CO2. Monitoring and accounting are required for regulatory compliance.",
            ["CO2 EOR", "oil recovery", "incidental storage", "monitoring"],
            1.0
        ),
        SearchDocument(
            8,
            "Section 45Q Tax Credit for Carbon Capture and Sequestration",
            "The U.S. Section 45Q tax credit incentivizes carbon capture and sequestration projects. Credits are awarded based on CO2 captured and stored or utilized.",
            ["45Q", "tax credit", "carbon capture", "sequestration"],
            1.0
        ),
        SearchDocument(
            9,
            "Oxy-Combustion CO2 Capture Technology",
            "Oxy-combustion burns fuel in pure oxygen, producing a flue gas rich in CO2 and water vapor. This simplifies CO2 capture and reduces nitrogen oxide emissions.",
            ["oxy-combustion", "CO2 capture", "oxygen", "flue gas"],
            1.0
        ),
        SearchDocument(
            10,
            "CO2 Compression for Pipeline Transport and Storage",
            "CO2 must be compressed to high pressures for pipeline transport and geological storage. Compression systems are designed for reliability and energy efficiency.",
            ["CO2 compression", "pipeline", "storage", "pressure"],
            1.0
        ),
        SearchDocument(
            11,
            "CCUS Lifecycle Carbon Accounting and Net Climate Benefit",
            "Lifecycle carbon accounting evaluates the net climate benefit of CCUS projects. It includes emissions from capture, transport, storage, and utilization.",
            ["CCUS", "carbon accounting", "net benefit", "lifecycle"],
            1.0
        ),
        SearchDocument(
            12,
            "EPA Class VI Injection Well Permitting Process",
            "EPA Class VI permits regulate wells used for CO2 injection into deep geologic formations. The process includes site characterization, risk assessment, and public engagement.",
            ["EPA", "Class VI", "injection well", "permitting"],
            1.0
        ),
        SearchDocument(
            13,
            "Monitoring, Verification, and Accounting (MVA) for CO2 Storage",
            "MVA protocols ensure CO2 remains securely stored in geological formations. Techniques include seismic surveys, pressure monitoring, and tracer studies.",
            ["MVA", "CO2 storage", "monitoring", "verification", "accounting"],
            1.0
        ),
        SearchDocument(
            14,
            "Amine Solvent Degradation and Management",
            "Amine solvents degrade over time due to impurities and temperature. Management strategies include reclaiming, filtration, and periodic replacement.",
            ["amine", "solvent", "degradation", "management"],
            1.0
        ),
        SearchDocument(
            15,
            "CO2 Pipeline Safety and Leak Detection",
            "Safety protocols for CO2 pipelines include leak detection systems, emergency response plans, and regular inspections. Dense phase transport minimizes risks.",
            ["CO2 pipeline", "safety", "leak detection", "dense phase"],
            1.0
        ),
        SearchDocument(
            16,
            "Geological Characterization for CO2 Storage",
            "Characterizing geological formations is essential for CO2 storage. Key parameters include porosity, permeability, caprock integrity, and seismic activity.",
            ["geological", "characterization", "CO2 storage", "porosity"],
            1.0
        ),
        SearchDocument(
            17,
            "CO2 Utilization in Concrete and Building Materials",
            "Captured CO2 can be used in concrete curing, producing stronger materials and reducing emissions. Utilization pathways contribute to circular carbon economy.",
            ["CO2 utilization", "concrete", "building materials", "circular economy"],
            1.0
        ),
        SearchDocument(
            18,
            "CO2 Storage Site Closure and Long-Term Monitoring",
            "After CO2 injection ends, site closure involves sealing wells and monitoring for leaks. Long-term surveillance ensures environmental safety.",
            ["CO2 storage", "site closure", "monitoring", "environmental safety"],
            1.0
        ),
        SearchDocument(
            19,
            "CO2 Capture Cost and Economic Analysis",
            "Economic analysis of CO2 capture includes capital costs, operating expenses, and incentives like 45Q. Cost optimization is critical for project viability.",
            ["CO2 capture", "cost", "economic analysis", "45Q"],
            1.0
        ),
        SearchDocument(
            20,
            "Solid Sorbent Regeneration Techniques",
            "Regeneration of solid sorbents is achieved by heating or pressure swing. Efficient regeneration is vital for direct air capture economics.",
            ["solid sorbent", "regeneration", "direct air capture", "economics"],
            1.0
        ),
        SearchDocument(
            21,
            "Alkaline Solution Chemistry for CO2 Capture",
            "Alkaline solutions react with CO2 to form carbonate and bicarbonate. Reaction kinetics and solvent regeneration impact capture efficiency.",
            ["alkaline solution", "CO2 capture", "chemistry", "regeneration"],
            1.0
        ),
        SearchDocument(
            22,
            "CO2 Transport Infrastructure Planning",
            "Planning CO2 transport infrastructure involves route selection, permitting, and stakeholder engagement. Dense phase pipelines are preferred for long distances.",
            ["CO2 transport", "infrastructure", "planning", "pipeline"],
            1.0
        ),
        SearchDocument(
            23,
            "Risk Assessment for Geological CO2 Storage",
            "Risk assessment evaluates potential leakage, induced seismicity, and environmental impacts of CO2 storage. Mitigation measures are implemented as needed.",
            ["risk assessment", "geological storage", "CO2", "leakage"],
            1.0
        ),
        SearchDocument(
            24,
            "CO2 Enhanced Oil Recovery Project Economics",
            "CO2 EOR project economics depend on oil prices, CO2 supply, and regulatory incentives. Incidental storage can qualify for 45Q tax credits.",
            ["CO2 EOR", "project economics", "oil recovery", "45Q"],
            1.0
        ),
        SearchDocument(
            25,
            "EPA Class VI Well Monitoring Requirements",
            "EPA Class VI wells require continuous monitoring of pressure, temperature, and CO2 plume migration. Compliance ensures safe storage and regulatory approval.",
            ["EPA", "Class VI", "monitoring", "CO2 storage"],
            1.0
        ),
        SearchDocument(
            26,
            "CO2 Compression Energy Consumption",
            "Energy consumption for CO2 compression is a major operating cost. Optimization strategies include multi-stage compression and heat integration.",
            ["CO2 compression", "energy consumption", "optimization"],
            1.0
        ),
        SearchDocument(
            27,
            "Carbon Capture Technology Comparison",
            "Comparison of carbon capture technologies includes amine scrubbing, oxy-combustion, direct air capture, and pre-combustion methods. Each has unique advantages and challenges.",
            ["carbon capture", "technology", "comparison", "amine", "oxy-combustion"],
            1.0
        ),
        SearchDocument(
            28,
            "CO2 Storage Regulatory Framework",
            "Regulatory frameworks for CO2 storage include EPA Class VI, state regulations, and international protocols. Permitting and compliance are essential.",
            ["CO2 storage", "regulatory", "EPA", "Class VI"],
            1.0
        ),
        SearchDocument(
            29,
            "CO2 Pipeline Route Selection Criteria",
            "Route selection for CO2 pipelines considers geology, population density, environmental impact, and cost. Stakeholder engagement is critical.",
            ["CO2 pipeline", "route selection", "environmental impact", "cost"],
            1.0
        ),
        SearchDocument(
            30,
            "CO2 Storage Capacity Estimation Methods",
            "Estimating CO2 storage capacity involves geological surveys, modeling, and reservoir simulation. Accurate estimation supports project planning.",
            ["CO2 storage", "capacity estimation", "geological survey", "modeling"],
            1.0
        ),
        SearchDocument(
            31,
            "CO2 Monitoring Technologies for Storage Sites",
            "Monitoring technologies for CO2 storage sites include seismic imaging, soil gas sensors, and satellite remote sensing. Early detection prevents leaks.",
            ["CO2 monitoring", "storage sites", "seismic imaging", "remote sensing"],
            1.0
        ),
        SearchDocument(
            32,
            "CO2 Capture Integration with Power Plants",
            "Integrating CO2 capture with power plants requires process optimization, heat recovery, and minimal impact on plant efficiency.",
            ["CO2 capture", "power plant", "integration", "heat recovery"],
            1.0
        ),
        SearchDocument(
            33,
            "CO2 Storage Site Selection and Characterization",
            "Site selection for CO2 storage involves geological characterization, risk assessment, and regulatory review. Suitable sites have secure caprock and high porosity.",
            ["CO2 storage", "site selection", "characterization", "caprock"],
            1.0
        ),
        SearchDocument(
            34,
            "CO2 Pipeline Maintenance and Inspection",
            "Regular maintenance and inspection of CO2 pipelines prevent leaks and ensure system reliability. Inspection techniques include pigging and pressure testing.",
            ["CO2 pipeline", "maintenance", "inspection", "reliability"],
            1.0
        ),
        SearchDocument(
            35,
            "CO2 Storage Environmental Impact Assessment",
            "Environmental impact assessment for CO2 storage evaluates effects on groundwater, ecosystems, and air quality. Mitigation strategies are developed as needed.",
            ["CO2 storage", "environmental impact", "assessment", "groundwater"],
            1.0
        ),
        SearchDocument(
            36,
            "CO2 Storage Monitoring and Verification Protocols",
            "Protocols for monitoring and verification of CO2 storage include baseline surveys, periodic sampling, and data reporting to regulatory agencies.",
            ["CO2 storage", "monitoring", "verification", "protocols"],
            1.0
        ),
        SearchDocument(
            37,
            "CO2 Capture Solvent Selection Criteria",
            "Solvent selection for CO2 capture considers absorption capacity, regeneration energy, corrosion, and environmental impact.",
            ["CO2 capture", "solvent", "selection", "absorption"],
            1.0
        ),
        SearchDocument(
            38,
            "CO2 Storage Site Risk Management",
            "Risk management for CO2 storage sites includes contingency planning, insurance, and stakeholder communication.",
            ["CO2 storage", "risk management", "contingency", "insurance"],
            1.0
        ),
        SearchDocument(
            39,
            "CO2 Pipeline Emergency Response Planning",
            "Emergency response planning for CO2 pipelines involves training, equipment deployment, and coordination with local authorities.",
            ["CO2 pipeline", "emergency response", "planning", "coordination"],
            1.0
        ),
        SearchDocument(
            40,
            "CO2 Storage Monitoring Data Interpretation",
            "Interpreting monitoring data for CO2 storage sites requires expertise in geophysics, chemistry, and environmental science.",
            ["CO2 storage", "monitoring", "data interpretation", "geophysics"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)