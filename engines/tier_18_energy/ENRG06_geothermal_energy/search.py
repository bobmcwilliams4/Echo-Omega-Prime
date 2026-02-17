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
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.total_doc_length = 0
        self.N = 0
        self.avg_doc_length = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._preprocessed = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            self.total_doc_length += len(tokens)
            self.N += 1
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self._preprocessed = False

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _ensure_preprocessed(self):
        if not self._preprocessed:
            if self.N > 0:
                self.avg_doc_length = self.total_doc_length / self.N
            else:
                self.avg_doc_length = 0.0
            self.idf_cache.clear()
            self._preprocessed = True

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        self._ensure_preprocessed()
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * ((freq * (self.k1 + 1)) / denom)
        score *= self.documents[doc_id].weight
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_norm = tf[term] / doc_len if doc_len > 0 else 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        score *= self.documents[doc_id].weight
        return score

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        self._ensure_preprocessed()
        scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if method == "bm25":
                score = self._score_bm25(query_terms, doc_id)
            elif method == "tfidf":
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:window] + "..." if len(content) > window else content
        start = max(min(positions) - window // 2, 0)
        end = min(start + window, len(content))
        snippet = content[start:end]
        for term in query_terms:
            snippet = re.sub(r'(?i)(' + re.escape(term) + r')', r'**\1**', snippet)
        return snippet + ("..." if end < len(content) else "")

    def get_stats(self) -> Dict[str, float]:
        self._ensure_preprocessed()
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_length,
            "vocab_size": len(self.doc_freqs)
        }

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
            1,
            "USGS Geothermal Resource Classification System",
            "The USGS Geothermal Resource Classification System provides a framework for categorizing geothermal resources based on their level of exploration, confirmation, and development. It distinguishes between identified and undiscovered resources, and further classifies them as inferred, indicated, measured, or producing.",
            ["USGS", "classification", "resource"],
            1.0
        ),
        SearchDocument(
            2,
            "Geothermal Gradient and Heat Flow Assessment",
            "Geothermal gradient is the rate of temperature increase with depth in the Earth's crust. Heat flow assessment involves measuring temperature and thermal conductivity to estimate subsurface heat, which is critical for geothermal exploration.",
            ["gradient", "heat flow", "exploration"],
            1.0
        ),
        SearchDocument(
            3,
            "Flash Steam vs Binary Cycle Technology Selection",
            "Flash steam plants use high-temperature geothermal fluids to produce steam directly, while binary cycle plants use a secondary working fluid with a lower boiling point. Technology selection depends on resource temperature, chemistry, and project economics.",
            ["flash steam", "binary cycle", "technology"],
            1.0
        ),
        SearchDocument(
            4,
            "Enhanced Geothermal Systems (EGS) Hydraulic Stimulation",
            "EGS involves hydraulic stimulation to increase permeability in hot dry rocks. Techniques include water injection, microseismic monitoring, and pressure management to optimize reservoir performance and minimize induced seismicity.",
            ["EGS", "hydraulic stimulation", "permeability"],
            1.0
        ),
        SearchDocument(
            5,
            "Geothermal Well Design for High Temperature Environments",
            "High temperature geothermal wells require specialized casing, cementing, and completion strategies to withstand thermal stress, corrosion, and scaling. Material selection and wellhead design are critical for long-term operation.",
            ["well design", "high temperature", "materials"],
            1.0
        ),
        SearchDocument(
            6,
            "Silica and Calcite Scaling Management",
            "Silica and calcite scaling can reduce geothermal plant efficiency. Management strategies include pH adjustment, chemical inhibitors, and controlled cooling to prevent scale deposition in wells and surface equipment.",
            ["scaling", "silica", "calcite", "management"],
            1.0
        ),
        SearchDocument(
            7,
            "Induced Seismicity Traffic Light Protocol",
            "The traffic light protocol is used to manage induced seismicity during geothermal operations. It sets thresholds for seismic events and prescribes operational responses such as reducing injection rates or shutting down wells.",
            ["induced seismicity", "traffic light", "protocol"],
            1.0
        ),
        SearchDocument(
            8,
            "Ground-Source Heat Pump Coefficient of Performance (COP)",
            "The coefficient of performance (COP) measures the efficiency of ground-source heat pumps. It is the ratio of heat output to electrical input, and is influenced by ground temperature, system design, and load profile.",
            ["heat pump", "COP", "performance"],
            1.0
        ),
        SearchDocument(
            9,
            "Geothermal Reservoir Modeling with TOUGH2",
            "TOUGH2 is a numerical simulator for non-isothermal multiphase flow in geothermal reservoirs. It models fluid and heat transport, allowing engineers to predict reservoir behavior and optimize production.",
            ["reservoir modeling", "TOUGH2", "simulation"],
            1.0
        ),
        SearchDocument(
            10,
            "Geothermal Levelized Cost of Energy (LCOE) Analysis",
            "LCOE analysis calculates the average cost per unit of electricity generated by a geothermal plant over its lifetime. It includes capital, operating, and maintenance costs, and is used to compare project economics.",
            ["LCOE", "cost analysis", "economics"],
            1.0
        ),
        SearchDocument(
            11,
            "Non-Condensable Gas (NCG) Extraction and H2S Abatement",
            "NCG extraction systems remove gases such as CO2 and H2S from geothermal steam. H2S abatement technologies include Stretford, LO-CAT, and caustic scrubbing to meet environmental regulations.",
            ["NCG", "H2S", "abatement", "extraction"],
            1.0
        ),
        SearchDocument(
            12,
            "Geothermal Reinjection Strategy and Pressure Maintenance",
            "Reinjection of spent geothermal fluids maintains reservoir pressure and sustainability. Strategies include selecting appropriate injection zones, monitoring pressure, and managing thermal breakthrough.",
            ["reinjection", "pressure maintenance", "sustainability"],
            1.0
        ),
        SearchDocument(
            13,
            "Geothermal Exploration Risk and Drilling Success Rates",
            "Exploration risk in geothermal projects arises from subsurface uncertainty. Drilling success rates depend on resource characterization, geophysical surveys, and well targeting strategies.",
            ["exploration risk", "drilling", "success rates"],
            1.0
        ),
        SearchDocument(
            14,
            "Binary Cycle Organic Rankine Cycle (ORC) Working Fluid Selection",
            "ORC systems use organic fluids such as isobutane or pentane as the working medium. Fluid selection is based on thermodynamic properties, environmental impact, and compatibility with resource temperature.",
            ["binary cycle", "ORC", "working fluid"],
            1.0
        ),
        SearchDocument(
            15,
            "Geothermal Power Plant Capacity Factor and Availability",
            "Capacity factor is the ratio of actual output to maximum possible output over time. Geothermal plants typically have high capacity factors and availability due to baseload operation.",
            ["capacity factor", "availability", "power plant"],
            1.0
        ),
        SearchDocument(
            16,
            "Geothermal Direct Use Applications",
            "Direct use of geothermal energy includes district heating, greenhouse heating, aquaculture, and industrial processes. These applications utilize moderate-temperature resources for thermal energy.",
            ["direct use", "applications", "district heating"],
            1.0
        ),
        SearchDocument(
            17,
            "Geothermal Environmental Impact Assessment",
            "Environmental impact assessment (EIA) for geothermal projects evaluates effects on land, water, air, and ecosystems. Key issues include land subsidence, induced seismicity, and chemical emissions.",
            ["environmental impact", "assessment", "EIA"],
            1.0
        ),
        SearchDocument(
            18,
            "Geothermal Resource Temperature Classification",
            "Geothermal resources are classified as low, medium, or high temperature based on reservoir conditions. This classification guides technology selection and project design.",
            ["resource classification", "temperature", "project design"],
            1.0
        ),
        SearchDocument(
            19,
            "Reservoir Stimulation and Microseismic Monitoring",
            "Reservoir stimulation enhances permeability through hydraulic fracturing. Microseismic monitoring tracks fracture growth and helps manage induced seismicity risks.",
            ["stimulation", "microseismic", "monitoring"],
            1.0
        ),
        SearchDocument(
            20,
            "Geothermal Well Logging Techniques",
            "Well logging provides subsurface data such as temperature, resistivity, and porosity. Common techniques include temperature logs, spinner flowmeter, and acoustic televiewer.",
            ["well logging", "temperature", "resistivity"],
            1.0
        ),
        SearchDocument(
            21,
            "Geothermal Surface Manifestations and Geochemistry",
            "Surface manifestations like hot springs, fumaroles, and mud pots indicate geothermal activity. Geochemical analysis of fluids helps locate and characterize resources.",
            ["surface manifestations", "geochemistry", "hot springs"],
            1.0
        ),
        SearchDocument(
            22,
            "Geothermal Drilling Fluids and Lost Circulation Control",
            "Drilling fluids cool the bit, remove cuttings, and control formation pressure. Lost circulation is managed with additives, bridging agents, and cement plugs.",
            ["drilling fluids", "lost circulation", "control"],
            1.0
        ),
        SearchDocument(
            23,
            "Geothermal Plant Operation and Maintenance",
            "Operation and maintenance (O&M) of geothermal plants includes equipment inspection, scaling control, and performance monitoring to ensure reliability and efficiency.",
            ["operation", "maintenance", "scaling"],
            1.0
        ),
        SearchDocument(
            24,
            "Geothermal Resource Assessment Methods",
            "Resource assessment methods include volumetric, numerical, and decline curve analysis. Accurate assessment is essential for project financing and development.",
            ["resource assessment", "methods", "financing"],
            1.0
        ),
        SearchDocument(
            25,
            "Geothermal Project Financing and Risk Mitigation",
            "Project financing involves securing capital through equity, debt, or grants. Risk mitigation strategies include insurance, phased development, and government support.",
            ["financing", "risk mitigation", "project"],
            1.0
        ),
        SearchDocument(
            26,
            "Geothermal Binary Cycle Heat Exchanger Design",
            "Heat exchangers in binary cycle plants transfer heat from geothermal fluid to the working fluid. Design considerations include fouling, pressure drop, and thermal efficiency.",
            ["binary cycle", "heat exchanger", "design"],
            1.0
        ),
        SearchDocument(
            27,
            "Geothermal Brine Chemistry and Scaling Prediction",
            "Brine chemistry analysis predicts scaling and corrosion potential. Common scales include silica, calcite, and barite, which can impact plant performance.",
            ["brine chemistry", "scaling", "prediction"],
            1.0
        ),
        SearchDocument(
            28,
            "Geothermal Resource Exploration Techniques",
            "Exploration techniques include geophysical surveys, geochemical sampling, and slimhole drilling to identify and characterize geothermal resources.",
            ["exploration", "techniques", "geophysical"],
            1.0
        ),
        SearchDocument(
            29,
            "Geothermal Power Purchase Agreements (PPAs)",
            "PPAs are contracts between power producers and utilities, defining terms for electricity sale, pricing, and delivery. They are critical for project bankability.",
            ["PPA", "power purchase", "agreement"],
            1.0
        ),
        SearchDocument(
            30,
            "Geothermal Induced Seismicity Case Studies",
            "Case studies of induced seismicity in geothermal projects highlight the importance of monitoring, traffic light protocols, and community engagement.",
            ["induced seismicity", "case study", "monitoring"],
            1.0
        ),
        SearchDocument(
            31,
            "Geothermal Resource Sustainability and Management",
            "Sustainable management of geothermal resources involves balancing production and reinjection, monitoring reservoir response, and adapting operations.",
            ["sustainability", "management", "reinjection"],
            1.0
        ),
        SearchDocument(
            32,
            "Geothermal Plant Emissions and Air Quality",
            "Geothermal plants emit trace gases such as CO2, H2S, and mercury. Air quality management includes emission controls and regulatory compliance.",
            ["emissions", "air quality", "regulation"],
            1.0
        ),
        SearchDocument(
            33,
            "Geothermal Plant Automation and SCADA Systems",
            "Automation and SCADA systems enable remote monitoring and control of geothermal plant operations, improving reliability and efficiency.",
            ["automation", "SCADA", "control"],
            1.0
        ),
        SearchDocument(
            34,
            "Geothermal Resource Mapping and GIS Applications",
            "GIS applications support geothermal resource mapping, site selection, and spatial analysis for exploration and development.",
            ["GIS", "mapping", "site selection"],
            1.0
        ),
        SearchDocument(
            35,
            "Geothermal Reservoir Pressure and Temperature Monitoring",
            "Continuous monitoring of reservoir pressure and temperature is essential for managing production, reinjection, and reservoir sustainability.",
            ["pressure monitoring", "temperature", "reservoir"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)