import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._lock = threading.Lock()
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._term_freqs: Dict[int, Counter] = {}
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self._term_freqs[doc.id] = tf
            self._doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self._inverted_index[term].add(doc.id)
                self._doc_freq[term] += 1
            self._documents[doc.id] = doc
            self._total_docs += 1
            self._avg_doc_length = (
                sum(self._doc_lengths.values()) / self._total_docs
                if self._total_docs > 0 else 0.0
            )
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_candidates = set()
        for term in query_terms:
            doc_candidates.update(self._inverted_index.get(term, set()))
        scored_results: List[Tuple[float, int]] = []
        for doc_id in doc_candidates:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            scored_results.append((final_score, doc_id))
        top_docs = heapq.nlargest(limit, scored_results)
        results = []
        for score, doc_id in top_docs:
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        return {
            "total_documents": self._total_docs,
            "unique_terms": len(self._inverted_index),
            "avg_doc_length": int(self._avg_doc_length),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freq.get(term, 0)
        N = self._total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5)) if df else 0.0
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self._documents[doc_id]
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        avg_dl = self._avg_doc_length or 1.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            numer = f * (self._bm25_k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self._documents[doc_id].weight

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:window*2] + "..." if len(content) > window*2 else content
        start = max(min(positions) - window, 0)
        end = min(max(positions) + window, len(content))
        snippet = content[start:end]
        for term in query_terms:
            snippet = re.sub(f'({re.escape(term)})', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ("..." if end < len(content) else "")

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

# --- Pre-seed Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Peng-Robinson Equation of State",
            "The Peng-Robinson EOS is widely used for vapor-liquid equilibrium calculations, especially for hydrocarbons. It is defined as: P = RT/(V-b) - a/(V^2+2bV-b^2). The parameters a and b are substance-specific and can be calculated from critical properties.",
            ["EOS", "VLE", "hydrocarbons", "critical properties"],
        ),
        SearchDocument(
            2,
            "NRTL Activity Coefficient Model",
            "The Non-Random Two-Liquid (NRTL) model is used to predict activity coefficients in non-ideal liquid mixtures. It accounts for local composition effects and is parameterized by binary interaction parameters.",
            ["activity coefficient", "NRTL", "non-ideal", "liquids"],
        ),
        SearchDocument(
            3,
            "Gibbs Free Energy Minimization for Chemical Equilibrium",
            "Chemical equilibrium can be determined by minimizing the total Gibbs free energy of the system. This approach is general and can handle complex reaction networks and phase equilibria.",
            ["Gibbs free energy", "chemical equilibrium", "minimization"],
        ),
        SearchDocument(
            4,
            "Rachford-Rice Flash Calculation",
            "The Rachford-Rice equation is used in two-phase flash calculations to determine the vapor and liquid fractions for a given mixture at specified temperature and pressure.",
            ["flash calculation", "Rachford-Rice", "two-phase", "VLE"],
        ),
        SearchDocument(
            5,
            "UNIFAC Group Contribution Method",
            "UNIFAC predicts activity coefficients using group contributions. It is useful for estimating vapor-liquid equilibria in mixtures where experimental data is unavailable.",
            ["UNIFAC", "group contribution", "activity coefficient", "VLE"],
        ),
        SearchDocument(
            6,
            "Fugacity and Fugacity Coefficient in Phase Equilibria",
            "Fugacity is an effective pressure that replaces the real pressure in phase equilibrium calculations. The fugacity coefficient quantifies deviation from ideal gas behavior.",
            ["fugacity", "phase equilibrium", "fugacity coefficient"],
        ),
        SearchDocument(
            7,
            "Hess's Law and Standard Enthalpy of Reaction",
            "Hess's Law states that the total enthalpy change for a reaction is the sum of the enthalpy changes for individual steps. Standard enthalpy of reaction can be calculated from standard enthalpies of formation.",
            ["Hess's Law", "enthalpy", "reaction", "thermodynamics"],
        ),
        SearchDocument(
            8,
            "Second Law Analysis and Entropy Generation",
            "The second law of thermodynamics introduces the concept of entropy generation, which quantifies irreversibility in processes. Minimizing entropy generation improves process efficiency.",
            ["second law", "entropy generation", "irreversibility"],
        ),
        SearchDocument(
            9,
            "Azeotrope Formation and Breaking Strategies",
            "Azeotropes are mixtures with constant boiling points. Breaking azeotropes can be achieved via pressure-swing distillation, entrainers, or membrane separation.",
            ["azeotrope", "distillation", "membrane", "entrainer"],
        ),
        SearchDocument(
            10,
            "Soave-Redlich-Kwong (SRK) Equation of State",
            "The SRK EOS is a cubic equation of state used for phase equilibrium calculations, especially for natural gases and light hydrocarbons.",
            ["SRK", "EOS", "natural gas", "phase equilibrium"],
        ),
        SearchDocument(
            11,
            "UNIQUAC Activity Coefficient Model",
            "UNIQUAC is a two-parameter model for predicting activity coefficients in non-ideal mixtures, accounting for both combinatorial and residual contributions.",
            ["UNIQUAC", "activity coefficient", "non-ideal", "mixtures"],
        ),
        SearchDocument(
            12,
            "Wilson Activity Coefficient Model",
            "The Wilson model predicts activity coefficients in liquid mixtures, particularly for systems with complete miscibility. It uses binary interaction parameters.",
            ["Wilson", "activity coefficient", "liquid mixtures"],
        ),
        SearchDocument(
            13,
            "Virial Equation of State for Moderate Pressures",
            "The virial EOS expresses the compressibility factor as a power series in density. It is accurate for gases at moderate pressures.",
            ["virial EOS", "compressibility", "moderate pressure"],
        ),
        SearchDocument(
            14,
            "Bubble Point and Dew Point Calculations",
            "Bubble point is the temperature (or pressure) at which the first bubble of vapor forms. Dew point is where the first drop of liquid condenses. Both are key in distillation and VLE.",
            ["bubble point", "dew point", "distillation", "VLE"],
        ),
        SearchDocument(
            15,
            "Excess Gibbs Energy and Excess Properties",
            "Excess properties, such as excess Gibbs energy, quantify deviations from ideal solution behavior. They are central to activity coefficient models.",
            ["excess Gibbs energy", "excess properties", "solution"],
        ),
        SearchDocument(
            16,
            "Supercritical Fluid Thermodynamics and CO2 Applications",
            "Supercritical fluids, such as CO2 above its critical point, exhibit unique solvent properties. They are used in extraction and material processing.",
            ["supercritical fluid", "CO2", "critical point", "extraction"],
        ),
        SearchDocument(
            17,
            "Thermodynamic Package Selection in Process Simulation",
            "Selecting an appropriate thermodynamic package is crucial for accurate process simulation. The choice depends on mixture type, phase behavior, and operating conditions.",
            ["thermodynamic package", "process simulation", "phase behavior"],
        ),
        SearchDocument(
            18,
            "GERG-2008 Equation of State for Natural Gas",
            "The GERG-2008 EOS is a reference equation for natural gas properties, accounting for multi-component mixtures and non-idealities.",
            ["GERG-2008", "natural gas", "EOS", "multi-component"],
        ),
        SearchDocument(
            19,
            "Le Chatelier's Principle and Reaction Equilibrium Shifts",
            "Le Chatelier's Principle predicts how a system at equilibrium responds to disturbances in concentration, pressure, or temperature.",
            ["Le Chatelier", "equilibrium", "reaction", "disturbance"],
        ),
        SearchDocument(
            20,
            "Activity and Activity Coefficient in Non-Ideal Solutions",
            "Activity is the effective concentration of a species in a mixture. The activity coefficient corrects for non-ideal behavior.",
            ["activity", "activity coefficient", "non-ideal", "solutions"],
        ),
        SearchDocument(
            21,
            "van der Waals Mixing Rules in Equation of State",
            "Mixing rules are used to extend pure-component EOS to mixtures. The van der Waals mixing rules are commonly applied to cubic EOS.",
            ["van der Waals", "mixing rules", "EOS", "mixtures"],
        ),
        SearchDocument(
            22,
            "Joule-Thomson Effect and Coefficient",
            "The Joule-Thomson effect describes the temperature change of a real gas when it is expanded at constant enthalpy. The coefficient varies with temperature and pressure.",
            ["Joule-Thomson", "real gas", "enthalpy", "expansion"],
        ),
        SearchDocument(
            23,
            "Critical Point and Critical Phenomena",
            "The critical point is defined by the temperature and pressure at which the liquid and vapor phases become indistinguishable. Critical phenomena include opalescence and large density fluctuations.",
            ["critical point", "critical phenomena", "phase transition"],
        ),
        SearchDocument(
            24,
            "Parameter Estimation for EOS and Activity Models",
            "Parameter estimation involves fitting model parameters to experimental data. Methods include regression, optimization, and error minimization.",
            ["parameter estimation", "regression", "optimization", "EOS"],
        ),
        SearchDocument(
            25,
            "Vapor-Liquid Equilibrium (VLE) Fundamentals",
            "VLE describes the distribution of chemical species between vapor and liquid phases. Accurate VLE modeling is essential for distillation and separation processes.",
            ["VLE", "vapor-liquid equilibrium", "distillation", "separation"],
        ),
        SearchDocument(
            26,
            "Thermodynamic Consistency Tests for VLE Data",
            "Consistency tests, such as the Herington and Redlich-Kister tests, are applied to experimental VLE data to ensure reliability before parameter fitting.",
            ["consistency test", "VLE", "Redlich-Kister", "Herington"],
        ),
        SearchDocument(
            27,
            "Electrolyte Thermodynamics and Pitzer Model",
            "The Pitzer model is used for electrolyte solutions, accounting for ionic strength and specific ion interactions in thermodynamic calculations.",
            ["Pitzer", "electrolyte", "ionic strength", "thermodynamics"],
        ),
        SearchDocument(
            28,
            "Phase Envelope Calculations for Hydrocarbon Mixtures",
            "Phase envelope calculations map the boundaries between single-phase and two-phase regions for hydrocarbon mixtures, critical for reservoir and process engineering.",
            ["phase envelope", "hydrocarbon", "reservoir", "process"],
        ),
        SearchDocument(
            29,
            "Thermodynamic Property Estimation from Group Contributions",
            "Group contribution methods estimate properties like enthalpy, entropy, and heat capacity from molecular structure, enabling predictions for novel compounds.",
            ["group contribution", "property estimation", "enthalpy", "entropy"],
        ),
        SearchDocument(
            30,
            "Non-Ideal Solution Behavior and Excess Functions",
            "Non-ideal solutions exhibit excess functions such as excess enthalpy and excess volume, which are important for understanding mixing thermodynamics.",
            ["non-ideal", "excess function", "enthalpy", "mixing"],
        ),
    ]
    for doc in docs:
        index.add_document(doc)