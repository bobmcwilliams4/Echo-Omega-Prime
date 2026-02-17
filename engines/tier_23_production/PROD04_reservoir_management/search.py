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
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self._preseeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for term in set(tokens):
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: Dict[int, float] = defaultdict(float)
        tfidf_scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            scores[doc_id] = bm25_score * doc.weight
            tfidf_scores[doc_id] = tfidf_score * doc.weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 1)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        tf = self.term_freqs[doc_id]
        for term in query_terms:
            idf = self._compute_idf(term)
            freq = tf.get(term, 0)
            numerator = freq * (k1 + 1)
            denominator = freq + k1 * (1 - b + b * doc_len / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths.get(doc_id, 1)
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            tf_norm = freq / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:snippet_len])
        start = max(positions[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(tokens))
        snippet = tokens[start:end]
        return ' '.join(snippet)

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1,
                "Material Balance Equation - Havlena-Odeh Method",
                "The Havlena-Odeh method is a graphical approach to material balance analysis for reservoir management. It allows identification of drive mechanisms and estimation of original hydrocarbons in place (OOIP/OGIP) by plotting reservoir pressure versus cumulative production and water influx.",
                ["material balance", "havlena-odeh", "reservoir management", "drive mechanism"],
                1.0
            ),
            SearchDocument(
                2,
                "Drive Mechanism Identification",
                "Drive mechanisms in reservoirs include solution gas drive, gas cap drive, water drive, and compaction drive. Identifying the dominant drive mechanism is crucial for predicting reservoir performance and recovery factor.",
                ["drive mechanism", "solution gas", "water drive", "gas cap", "compaction"],
                1.0
            ),
            SearchDocument(
                3,
                "Recovery Factor Estimation by Drive Type",
                "Recovery factor depends on the drive mechanism. Water drive reservoirs typically have higher recovery factors than solution gas drive. Gas cap and compaction drives have intermediate recovery factors.",
                ["recovery factor", "drive type", "water drive", "solution gas", "gas cap", "compaction"],
                1.0
            ),
            SearchDocument(
                4,
                "Waterflood Design - Pattern Selection",
                "Pattern selection in waterflooding involves choosing between five-spot, seven-spot, line drive, and staggered patterns. The choice depends on reservoir geometry, heterogeneity, and well spacing.",
                ["waterflood", "pattern selection", "five-spot", "seven-spot", "line drive", "staggered"],
                1.0
            ),
            SearchDocument(
                5,
                "Waterflood Optimization - Injection Rate and Fractional Flow",
                "Optimizing injection rate and fractional flow in waterflooding maximizes oil recovery and minimizes water production. Fractional flow theory helps determine the optimal water injection rate based on relative permeability curves.",
                ["waterflood", "optimization", "injection rate", "fractional flow", "relative permeability"],
                1.0
            ),
            SearchDocument(
                6,
                "CO2 EOR - Miscible vs Immiscible Displacement",
                "CO2 enhanced oil recovery (EOR) can be miscible or immiscible. Miscible displacement occurs when CO2 mixes with oil, reducing viscosity and interfacial tension. Immiscible displacement relies on CO2 as a gas drive agent.",
                ["CO2 EOR", "miscible", "immiscible", "displacement", "viscosity", "interfacial tension"],
                1.0
            ),
            SearchDocument(
                7,
                "WAG (Water Alternating Gas) Process Design",
                "The WAG process alternates water and gas injection to improve sweep efficiency and reduce gas breakthrough. Key design parameters include WAG ratio, cycle length, and injection rates.",
                ["WAG", "water alternating gas", "process design", "sweep efficiency", "gas breakthrough"],
                1.0
            ),
            SearchDocument(
                8,
                "Reservoir Simulation - Black Oil vs Compositional Models",
                "Black oil models simplify reservoir simulation by lumping oil, gas, and water into three phases. Compositional models track individual hydrocarbon components, providing more accurate predictions for volatile oil and gas condensate reservoirs.",
                ["reservoir simulation", "black oil", "compositional", "model", "volatile oil", "gas condensate"],
                1.0
            ),
            SearchDocument(
                9,
                "History Matching Methodology",
                "History matching adjusts reservoir model parameters to fit observed production and pressure data. Techniques include manual tuning, automatic optimization, and assisted history matching using statistical methods.",
                ["history matching", "reservoir model", "production data", "pressure data", "optimization"],
                1.0
            ),
            SearchDocument(
                10,
                "OOIP/OGIP Estimation - Volumetric Method",
                "The volumetric method estimates original oil or gas in place (OOIP/OGIP) using reservoir volume, porosity, saturation, and formation volume factor. It is a fundamental technique in reservoir engineering.",
                ["OOIP", "OGIP", "volumetric method", "porosity", "saturation", "formation volume factor"],
                1.0
            ),
            SearchDocument(
                11,
                "PVT Properties - Bo Correlations (Standing, Vasquez-Beggs)",
                "Formation volume factor (Bo) correlations such as Standing and Vasquez-Beggs are used to estimate oil expansion and shrinkage. Accurate Bo estimation is critical for material balance and reservoir simulation.",
                ["PVT", "Bo", "Standing", "Vasquez-Beggs", "formation volume factor", "correlation"],
                1.0
            ),
            SearchDocument(
                12,
                "Gas Viscosity - Lee-Gonzalez Correlation",
                "The Lee-Gonzalez correlation estimates gas viscosity as a function of pressure, temperature, and gas composition. It is widely used in reservoir simulation and material balance calculations.",
                ["gas viscosity", "Lee-Gonzalez", "correlation", "pressure", "temperature", "composition"],
                1.0
            ),
            SearchDocument(
                13,
                "Relative Permeability and Capillary Pressure",
                "Relative permeability curves describe multiphase flow behavior in porous media. Capillary pressure affects fluid distribution and recovery. Laboratory measurements and correlations are used for reservoir characterization.",
                ["relative permeability", "capillary pressure", "multiphase flow", "porous media", "recovery"],
                1.0
            ),
            SearchDocument(
                14,
                "Reservoir Heterogeneity - Dykstra-Parsons Coefficient",
                "The Dykstra-Parsons coefficient quantifies reservoir heterogeneity by comparing permeability variations. High heterogeneity reduces sweep efficiency and impacts waterflood and EOR performance.",
                ["reservoir heterogeneity", "Dykstra-Parsons", "coefficient", "permeability", "sweep efficiency"],
                1.0
            ),
            SearchDocument(
                15,
                "Field Development Planning - Infill Drilling Economics",
                "Infill drilling increases recovery by adding wells in underdeveloped areas. Economic analysis considers drilling costs, incremental production, and reservoir depletion effects.",
                ["field development", "infill drilling", "economics", "incremental production", "depletion"],
                1.0
            ),
            SearchDocument(
                16,
                "Permian Basin Reservoir Characteristics",
                "Permian Basin reservoirs are characterized by carbonate and sandstone lithologies, variable porosity, and complex structural features. Understanding these characteristics is essential for successful development.",
                ["Permian Basin", "reservoir characteristics", "carbonate", "sandstone", "porosity", "structure"],
                1.0
            ),
            SearchDocument(
                17,
                "Material Balance Equation - Water Influx Models",
                "Water influx models such as the Hantush and Fetkovich methods are used to quantify water encroachment in reservoirs. Accurate water influx estimation is vital for material balance calculations.",
                ["material balance", "water influx", "Hantush", "Fetkovich", "encroachment", "reservoir"],
                1.0
            ),
            SearchDocument(
                18,
                "Gas Cap Expansion and Reservoir Performance",
                "Gas cap expansion provides additional energy for oil recovery. Monitoring gas cap behavior is important for optimizing production and preventing excessive gas breakthrough.",
                ["gas cap", "expansion", "reservoir performance", "oil recovery", "breakthrough"],
                1.0
            ),
            SearchDocument(
                19,
                "Compaction Drive and Reservoir Depletion",
                "Compaction drive occurs when reservoir pressure drops, causing rock compaction and fluid expulsion. It is common in unconsolidated formations and can contribute significantly to recovery.",
                ["compaction drive", "reservoir depletion", "rock compaction", "fluid expulsion", "unconsolidated"],
                1.0
            ),
            SearchDocument(
                20,
                "Waterflood Surveillance and Performance Monitoring",
                "Surveillance techniques include tracer tests, production logging, and pressure monitoring. These help assess waterflood performance and identify areas of poor sweep efficiency.",
                ["waterflood", "surveillance", "performance monitoring", "tracer test", "logging", "pressure"],
                1.0
            ),
            SearchDocument(
                21,
                "CO2 EOR Screening Criteria",
                "Screening criteria for CO2 EOR include reservoir depth, oil viscosity, permeability, and formation heterogeneity. Proper screening ensures technical and economic feasibility.",
                ["CO2 EOR", "screening", "criteria", "reservoir depth", "viscosity", "permeability", "heterogeneity"],
                1.0
            ),
            SearchDocument(
                22,
                "WAG Process Optimization",
                "Optimizing WAG involves adjusting water and gas injection rates, cycle lengths, and monitoring breakthrough. Simulation and field data are used to refine WAG strategies.",
                ["WAG", "optimization", "injection rate", "cycle length", "breakthrough", "simulation"],
                1.0
            ),
            SearchDocument(
                23,
                "Compositional Simulation for Gas Condensate Reservoirs",
                "Compositional simulation tracks individual hydrocarbon components and phase behavior. It is essential for gas condensate and volatile oil reservoirs where black oil models are insufficient.",
                ["compositional simulation", "gas condensate", "volatile oil", "phase behavior", "hydrocarbon"],
                1.0
            ),
            SearchDocument(
                24,
                "History Matching with Assisted Techniques",
                "Assisted history matching uses statistical and machine learning methods to automate parameter adjustment and improve model fit. It reduces manual effort and increases reliability.",
                ["history matching", "assisted", "statistical", "machine learning", "parameter adjustment"],
                1.0
            ),
            SearchDocument(
                25,
                "OOIP/OGIP Estimation - Uncertainty Analysis",
                "Uncertainty analysis quantifies the range of OOIP/OGIP estimates due to variability in input parameters. Monte Carlo simulation and sensitivity analysis are commonly used.",
                ["OOIP", "OGIP", "uncertainty analysis", "Monte Carlo", "sensitivity", "input parameters"],
                1.0
            ),
            SearchDocument(
                26,
                "PVT Properties - Gas Compressibility Factor (Z)",
                "The gas compressibility factor (Z) is determined from laboratory measurements or correlations. Z-factor is essential for gas material balance and volumetric calculations.",
                ["PVT", "compressibility factor", "Z", "gas", "material balance", "correlation"],
                1.0
            ),
            SearchDocument(
                27,
                "Relative Permeability Measurement Techniques",
                "Relative permeability is measured using laboratory core flooding experiments. Data is used to generate curves for reservoir simulation and performance prediction.",
                ["relative permeability", "measurement", "core flooding", "simulation", "prediction"],
                1.0
            ),
            SearchDocument(
                28,
                "Capillary Pressure Measurement and Interpretation",
                "Capillary pressure is measured using centrifuge and porous plate methods. Interpretation of capillary pressure curves aids in understanding fluid distribution and recovery.",
                ["capillary pressure", "measurement", "interpretation", "centrifuge", "porous plate", "recovery"],
                1.0
            ),
            SearchDocument(
                29,
                "Reservoir Heterogeneity Impact on Waterflood",
                "Heterogeneity affects waterflood performance by causing uneven sweep and early breakthrough. Dykstra-Parsons coefficient is used to quantify heterogeneity.",
                ["reservoir heterogeneity", "waterflood", "Dykstra-Parsons", "sweep", "breakthrough"],
                1.0
            ),
            SearchDocument(
                30,
                "Permian Basin - Wolfcamp Formation",
                "Wolfcamp Formation in the Permian Basin is a major target for unconventional oil and gas development. It exhibits complex stratigraphy and variable reservoir quality.",
                ["Permian Basin", "Wolfcamp", "formation", "unconventional", "stratigraphy", "reservoir quality"],
                1.0
            ),
            SearchDocument(
                31,
                "Field Development - Well Spacing Optimization",
                "Optimizing well spacing in field development maximizes recovery and minimizes interference. Simulation and economic analysis guide spacing decisions.",
                ["field development", "well spacing", "optimization", "recovery", "interference", "simulation"],
                1.0
            ),
            SearchDocument(
                32,
                "Material Balance Equation - Gas Reservoirs",
                "Material balance for gas reservoirs involves tracking gas production, pressure decline, and water influx. The method helps estimate OGIP and predict future performance.",
                ["material balance", "gas reservoir", "OGIP", "pressure decline", "water influx", "performance"],
                1.0
            ),
            SearchDocument(
                33,
                "Waterflood Pattern Efficiency",
                "Pattern efficiency in waterflooding is influenced by reservoir heterogeneity, well placement, and injection strategy. Five-spot and line drive are common patterns.",
                ["waterflood", "pattern efficiency", "heterogeneity", "well placement", "injection strategy"],
                1.0
            ),
            SearchDocument(
                34,
                "CO2 EOR - Minimum Miscibility Pressure",
                "Minimum miscibility pressure (MMP) is the pressure at which CO2 becomes miscible with oil. Achieving MMP is critical for successful miscible CO2 EOR projects.",
                ["CO2 EOR", "minimum miscibility pressure", "MMP", "miscible", "oil", "pressure"],
                1.0
            ),
            SearchDocument(
                35,
                "Reservoir Simulation - Grid Design",
                "Grid design in reservoir simulation affects accuracy and computational efficiency. Fine grids are used in areas of interest, while coarser grids are applied elsewhere.",
                ["reservoir simulation", "grid design", "accuracy", "efficiency", "fine grid", "coarse grid"],
                1.0
            ),
            SearchDocument(
                36,
                "History Matching - Objective Functions",
                "Objective functions in history matching quantify the difference between observed and simulated data. Common functions include least squares and weighted error metrics.",
                ["history matching", "objective function", "least squares", "error metric", "simulation"],
                1.0
            ),
            SearchDocument(
                37,
                "OOIP/OGIP Estimation - Material Balance Approach",
                "Material balance approach estimates OOIP/OGIP by integrating production, pressure, and water influx data. It complements volumetric and simulation methods.",
                ["OOIP", "OGIP", "material balance", "production", "pressure", "water influx"],
                1.0
            ),
            SearchDocument(
                38,
                "Permian Basin - Delaware Basin Characteristics",
                "Delaware Basin is part of the Permian Basin with deep, overpressured reservoirs and complex faulting. Development strategies focus on horizontal drilling and hydraulic fracturing.",
                ["Permian Basin", "Delaware Basin", "characteristics", "overpressured", "faulting", "drilling"],
                1.0
            ),
            SearchDocument(
                39,
                "Field Development - Enhanced Recovery Techniques",
                "Enhanced recovery techniques include waterflood, CO2 EOR, and polymer flooding. Selection depends on reservoir properties and economic considerations.",
                ["field development", "enhanced recovery", "waterflood", "CO2 EOR", "polymer flooding"],
                1.0
            ),
            SearchDocument(
                40,
                "Material Balance Equation - Reservoir Pressure Analysis",
                "Reservoir pressure analysis is integral to material balance calculations. It involves measuring static and flowing pressures to assess depletion and drive mechanisms.",
                ["material balance", "reservoir pressure", "analysis", "depletion", "drive mechanism"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

def get_search_index() -> SearchIndex:
    if not hasattr(get_search_index, "_instance"):
        get_search_index._instance = SearchIndex()
        get_search_index._instance._preseed_documents()
    return get_search_index._instance