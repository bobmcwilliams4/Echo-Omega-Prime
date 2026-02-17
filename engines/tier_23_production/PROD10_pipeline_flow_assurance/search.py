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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_tags: Dict[int, List[str]] = {}
        self.total_docs: int = 0
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in self.term_freqs[doc.id]:
                self.term_doc_freqs[term][doc.id] = self.term_freqs[doc.id][term]
            self.doc_tags[doc.id] = doc.tags
            self.total_docs = len(self.documents)
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            )
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_doc_freqs.get(term, {}).keys())
        scored_results: List[Tuple[int, float]] = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc_weight = self.documents[doc_id].weight
            combined_score = bm25_score * 0.7 + tfidf_score * 0.3
            combined_score *= doc_weight
            scored_results.append((doc_id, combined_score))
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.term_doc_freqs.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs.get(doc_id, Counter())
        for term in query_terms:
            f = tf.get(term, 0)
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            if denom == 0:
                continue
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf = self.term_freqs.get(doc_id, Counter())
        doc_len = self.doc_lengths.get(doc_id, 0)
        for term in query_terms:
            term_tf = tf.get(term, 0) / (doc_len if doc_len > 0 else 1)
            idf = self._compute_idf(term)
            score += term_tf * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        positions = []
        for i, token in enumerate(tokens):
            if token in query_terms:
                positions.append(i)
        if not positions:
            snippet = ' '.join(tokens[:30])
        else:
            start = max(positions[0] - 10, 0)
            end = min(positions[0] + 20, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet + ('...' if len(tokens) > end else '')

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Hydrate Formation Thermodynamics",
            "Hydrate formation occurs when water and hydrocarbon gases combine under low temperature and high pressure. Thermodynamic prediction involves phase equilibrium calculations using models like van der Waals-Platteeuw and gas composition analysis.",
            ["hydrate", "thermodynamics", "phase equilibrium"],
            1.0
        ),
        SearchDocument(
            2,
            "Monoethylene Glycol (MEG) Hydrate Inhibition",
            "MEG is injected into pipelines to inhibit hydrate formation. It lowers the hydrate formation temperature, allowing safe operation. MEG recovery and regeneration are critical for cost-effective flow assurance.",
            ["MEG", "hydrate inhibition", "flow assurance"],
            1.0
        ),
        SearchDocument(
            3,
            "Low Dosage Hydrate Inhibitor (LDHI) Application",
            "LDHIs are specialized chemicals that prevent hydrate nucleation and growth at low concentrations. Their effectiveness depends on water cut, temperature, and gas composition. Selection requires laboratory testing and field trials.",
            ["LDHI", "hydrate", "chemical inhibition"],
            1.0
        ),
        SearchDocument(
            4,
            "Wax Appearance Temperature (WAT) and Cloud Point",
            "WAT is the temperature at which wax crystals first appear in crude oil. Cloud point is related but often used for refined products. Accurate WAT prediction is essential for pipeline design and wax management.",
            ["wax", "WAT", "cloud point", "pipeline"],
            1.0
        ),
        SearchDocument(
            5,
            "Wax Deposition Modeling and Prediction",
            "Wax deposition in pipelines leads to flow restrictions and increased pressure drop. Modeling approaches include empirical correlations, molecular diffusion, and heat transfer analysis. Prediction tools help optimize pigging and inhibitor dosing.",
            ["wax", "deposition", "modeling", "prediction"],
            1.0
        ),
        SearchDocument(
            6,
            "Chemical Wax Inhibitors and Pour Point Depressants",
            "Wax inhibitors modify crystal structure and reduce deposition. Pour point depressants lower the minimum temperature for oil flow. Selection depends on crude properties and operational conditions.",
            ["wax", "inhibitors", "pour point", "depressants"],
            1.0
        ),
        SearchDocument(
            7,
            "Asphaltene Onset Pressure and Precipitation Envelope",
            "Asphaltenes precipitate when pressure drops below onset pressure or composition changes. Precipitation envelope modeling uses equations of state and experimental data. Managing asphaltene risk prevents plugging and equipment fouling.",
            ["asphaltene", "onset pressure", "precipitation", "envelope"],
            1.0
        ),
        SearchDocument(
            8,
            "Scale Prediction and Saturation Index Modeling",
            "Scale forms when dissolved salts exceed solubility limits. Saturation index models predict scaling tendency based on water chemistry and temperature. Common scales include calcium carbonate and barium sulfate.",
            ["scale", "prediction", "saturation index", "water chemistry"],
            1.0
        ),
        SearchDocument(
            9,
            "Scale Inhibitor Squeeze Treatment Design",
            "Squeeze treatments involve injecting scale inhibitor into the reservoir matrix. Design considers inhibitor retention, squeeze lifetime, and compatibility with formation fluids. Monitoring ensures effective scale control.",
            ["scale", "inhibitor", "squeeze", "treatment", "design"],
            1.0
        ),
        SearchDocument(
            10,
            "Terrain-Induced Slugging in Hilly Pipelines",
            "Slugging occurs in pipelines with elevation changes, causing intermittent flow and pressure surges. Modeling uses multiphase flow simulations and terrain mapping. Mitigation strategies include slug catchers and pipeline re-routing.",
            ["slugging", "terrain", "pipeline", "multiphase flow"],
            1.0
        ),
        SearchDocument(
            11,
            "Multiphase Flow Correlations and Pressure Drop Prediction",
            "Pressure drop prediction in multiphase flow uses correlations like Beggs-Brill, Hagedorn-Brown, and Mukherjee-Brill. Accurate modeling requires input on fluid properties, pipe geometry, and flow regime.",
            ["multiphase flow", "pressure drop", "correlations", "modeling"],
            1.0
        ),
        SearchDocument(
            12,
            "Intelligent Pigging for Pipeline Inspection",
            "Intelligent pigs use sensors to detect corrosion, cracks, and wall thickness changes. Data analysis identifies pipeline integrity issues and guides maintenance planning. Pigging frequency depends on risk assessment and regulatory requirements.",
            ["pigging", "pipeline inspection", "intelligent pig", "corrosion"],
            1.0
        ),
        SearchDocument(
            13,
            "Pigging Frequency Optimization for Wax Removal",
            "Optimizing pigging frequency balances wax removal efficiency and operational costs. Models consider wax deposition rates, pipeline length, and pigging tool performance. Data-driven approaches improve reliability.",
            ["pigging", "wax removal", "optimization", "frequency"],
            1.0
        ),
        SearchDocument(
            14,
            "Emergency Depressurization and Hydrate Dissociation Risk",
            "Rapid depressurization can cause hydrate dissociation, leading to blockages and safety hazards. Risk assessment involves thermodynamic modeling and operational procedures. Mitigation includes controlled depressurization and inhibitor injection.",
            ["depressurization", "hydrate", "risk", "dissociation"],
            1.0
        ),
        SearchDocument(
            15,
            "Sweet Corrosion from CO2 in Production Systems",
            "CO2 causes sweet corrosion by forming carbonic acid in water. Prediction models use partial pressure, temperature, and water chemistry. Corrosion inhibitors and material selection reduce risk.",
            ["corrosion", "CO2", "sweet corrosion", "production"],
            1.0
        ),
        SearchDocument(
            16,
            "Erosional Velocity and API RP 14E Criterion",
            "Erosional velocity is the maximum allowable flow velocity to prevent pipe erosion. API RP 14E provides guidelines based on pipe material and fluid properties. Monitoring ensures safe operation and asset integrity.",
            ["erosion", "velocity", "API RP 14E", "pipe", "integrity"],
            1.0
        ),
        SearchDocument(
            17,
            "Hydrate Phase Equilibrium Modeling",
            "Phase equilibrium modeling predicts hydrate formation conditions using equations of state and fugacity calculations. Accurate models support inhibitor selection and operational planning.",
            ["hydrate", "phase equilibrium", "modeling", "prediction"],
            1.0
        ),
        SearchDocument(
            18,
            "MEG Recovery and Regeneration Technologies",
            "MEG recovery involves separating MEG from produced water and contaminants. Regeneration processes include distillation and filtration. Efficient recovery reduces operational costs and environmental impact.",
            ["MEG", "recovery", "regeneration", "technology"],
            1.0
        ),
        SearchDocument(
            19,
            "LDHI Performance Evaluation and Field Trials",
            "LDHI performance is evaluated through laboratory testing and field trials. Parameters include subcooling, water cut, and gas composition. Data analysis guides chemical selection and dosing strategies.",
            ["LDHI", "performance", "evaluation", "field trials"],
            1.0
        ),
        SearchDocument(
            20,
            "Wax Inhibitor Selection and Laboratory Testing",
            "Wax inhibitor selection uses laboratory tests like cold finger and flow loop experiments. Results inform chemical selection and dosing rates. Compatibility with crude oil and operational conditions is critical.",
            ["wax", "inhibitor", "selection", "laboratory testing"],
            1.0
        ),
        SearchDocument(
            21,
            "Asphaltene Precipitation Mechanisms",
            "Asphaltene precipitation is triggered by changes in pressure, temperature, and composition. Mechanisms include flocculation and aggregation. Prevention strategies involve chemical inhibitors and process optimization.",
            ["asphaltene", "precipitation", "mechanisms", "inhibitors"],
            1.0
        ),
        SearchDocument(
            22,
            "Scale Inhibitor Chemistry and Compatibility",
            "Scale inhibitor chemistry includes phosphonates, polymers, and organic acids. Compatibility with formation fluids and other chemicals is essential for effective scale control.",
            ["scale", "inhibitor", "chemistry", "compatibility"],
            1.0
        ),
        SearchDocument(
            23,
            "Slug Catcher Design and Operation",
            "Slug catchers are vessels that temporarily store slugs in pipelines. Design considers slug volume, flow rate, and separation efficiency. Operation involves monitoring and maintenance to prevent overflow.",
            ["slug catcher", "design", "operation", "pipeline"],
            1.0
        ),
        SearchDocument(
            24,
            "Multiphase Flow Regime Identification",
            "Flow regime identification uses pressure, temperature, and flow rate data. Regimes include stratified, slug, annular, and bubble flow. Accurate identification improves modeling and operational decisions.",
            ["multiphase flow", "regime", "identification", "modeling"],
            1.0
        ),
        SearchDocument(
            25,
            "Pipeline Integrity Management and Inspection",
            "Pipeline integrity management involves regular inspection, risk assessment, and maintenance. Intelligent pigging and corrosion monitoring are key tools. Regulatory compliance ensures safe and reliable operation.",
            ["pipeline", "integrity", "management", "inspection"],
            1.0
        ),
        SearchDocument(
            26,
            "Wax Deposition Mitigation Strategies",
            "Mitigation strategies for wax deposition include thermal insulation, chemical inhibitors, and regular pigging. Selection depends on crude properties and pipeline conditions.",
            ["wax", "deposition", "mitigation", "strategies"],
            1.0
        ),
        SearchDocument(
            27,
            "Asphaltene Inhibitor Selection and Performance",
            "Asphaltene inhibitors are selected based on crude composition and precipitation risk. Performance is evaluated through laboratory tests and field monitoring.",
            ["asphaltene", "inhibitor", "selection", "performance"],
            1.0
        ),
        SearchDocument(
            28,
            "Scale Removal Techniques and Equipment",
            "Scale removal uses mechanical, chemical, and hydrojetting methods. Equipment selection depends on scale type and pipeline accessibility.",
            ["scale", "removal", "techniques", "equipment"],
            1.0
        ),
        SearchDocument(
            29,
            "Pigging Tool Types and Selection",
            "Pigging tools include foam pigs, scraper pigs, and intelligent pigs. Selection depends on pipeline diameter, debris type, and inspection requirements.",
            ["pigging", "tool", "selection", "pipeline"],
            1.0
        ),
        SearchDocument(
            30,
            "Corrosion Inhibitor Application and Monitoring",
            "Corrosion inhibitors are applied to production systems to reduce metal loss. Monitoring involves corrosion coupons, probes, and data analysis.",
            ["corrosion", "inhibitor", "application", "monitoring"],
            1.0
        ),
        SearchDocument(
            31,
            "API RP 14E Erosional Velocity Calculation",
            "API RP 14E provides formulas for calculating erosional velocity based on pipe material and fluid density. Exceeding erosional velocity increases risk of pipe failure.",
            ["API RP 14E", "erosional velocity", "calculation", "pipe"],
            1.0
        ),
        SearchDocument(
            32,
            "Hydrate Inhibitor Dosing Optimization",
            "Hydrate inhibitor dosing is optimized using thermodynamic models and field data. Overdosing increases costs, while underdosing risks hydrate formation.",
            ["hydrate", "inhibitor", "dosing", "optimization"],
            1.0
        ),
        SearchDocument(
            33,
            "Wax Crystal Structure Modification",
            "Wax inhibitors modify crystal structure to reduce deposition and improve flow. Laboratory testing evaluates effectiveness under varying temperatures.",
            ["wax", "crystal structure", "modification", "inhibitor"],
            1.0
        ),
        SearchDocument(
            34,
            "Asphaltene Flocculation and Aggregation",
            "Asphaltene flocculation leads to aggregation and precipitation. Chemical inhibitors disrupt aggregation, preventing plugging and fouling.",
            ["asphaltene", "flocculation", "aggregation", "inhibitor"],
            1.0
        ),
        SearchDocument(
            35,
            "Scale Prediction Software and Tools",
            "Scale prediction software uses water chemistry and operational data to model scaling risk. Tools include saturation index calculators and simulation platforms.",
            ["scale", "prediction", "software", "tools"],
            1.0
        ),
        SearchDocument(
            36,
            "Slugging Mitigation Techniques",
            "Slugging mitigation includes pipeline re-routing, slug catchers, and flow control devices. Modeling supports selection of appropriate techniques.",
            ["slugging", "mitigation", "pipeline", "modeling"],
            1.0
        ),
        SearchDocument(
            37,
            "Multiphase Flow Simulation Platforms",
            "Simulation platforms model multiphase flow behavior in pipelines. Features include pressure drop prediction, flow regime identification, and terrain mapping.",
            ["multiphase flow", "simulation", "platforms", "pipeline"],
            1.0
        ),
        SearchDocument(
            38,
            "Pigging Data Analysis and Maintenance Planning",
            "Pigging data analysis identifies pipeline integrity issues and guides maintenance planning. Regular pigging ensures reliable operation and prevents blockages.",
            ["pigging", "data analysis", "maintenance", "pipeline"],
            1.0
        ),
        SearchDocument(
            39,
            "Emergency Depressurization Procedures",
            "Emergency depressurization procedures are designed to minimize hydrate dissociation risk. Controlled depressurization and inhibitor injection are key strategies.",
            ["depressurization", "procedures", "hydrate", "risk"],
            1.0
        ),
        SearchDocument(
            40,
            "CO2 Corrosion Modeling and Prevention",
            "CO2 corrosion modeling uses thermodynamic and kinetic models to predict metal loss. Prevention includes corrosion inhibitors and material selection.",
            ["CO2", "corrosion", "modeling", "prevention"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)