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
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._next_doc_id = 1
        self._total_terms = 0
        self._doc_count = 0

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self._lock:
            doc_id = self._next_doc_id
            self._next_doc_id += 1
            doc = SearchDocument(doc_id, title, content, tags, weight)
            tokens = self._tokenize(content)
            self._documents[doc_id] = doc
            self._doc_tokens[doc_id] = tokens
            term_freq = Counter(tokens)
            self._term_freqs[doc_id] = term_freq
            self._doc_lengths[doc_id] = len(tokens)
            self._total_terms += len(tokens)
            self._doc_count += 1
            for term in term_freq:
                self._inverted_index[term].add(doc_id)
            self._avg_doc_length = self._total_terms / self._doc_count if self._doc_count else 0.0
            self._idf_cache.clear()
            return doc_id

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self._inverted_index.get(token, set()))
        scores = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            doc = self._documents[doc_id]
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            final_score *= doc.weight
            snippet = self._make_snippet(doc, query_tokens)
            scores.append((final_score, SearchResult(doc_id, final_score, doc.title, snippet)))
        top_results = heapq.nlargest(limit, scores, key=lambda x: x[0])
        return [result for _, result in top_results]

    def get_stats(self) -> Dict[str, float]:
        with self._lock:
            return {
                "document_count": self._doc_count,
                "average_document_length": self._avg_doc_length,
                "total_terms": self._total_terms,
                "vocabulary_size": len(self._inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = self._doc_count
        df = len(self._inverted_index.get(term, []))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        k1 = 1.5
        b = 0.75
        score = 0.0
        doc_len = self._doc_lengths.get(doc_id, 0)
        avgdl = self._avg_doc_length if self._avg_doc_length > 0 else 1.0
        term_freqs = self._term_freqs.get(doc_id, {})
        for term in query_tokens:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + k1 * (1 - b + b * doc_len / avgdl)
            score += idf * (tf * (k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        term_freqs = self._term_freqs.get(doc_id, {})
        doc_len = self._doc_lengths.get(doc_id, 1)
        for term in query_tokens:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:160]
            return snippet + ("..." if len(content) > 160 else "")
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for qt in set(query_tokens):
            snippet = re.sub(r'\b({})\b'.format(re.escape(qt)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ("..." if end < len(tokens) else "")

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Domain Documents ---

def _seed_documents(index: SearchIndex):
    docs = [
        {
            "title": "First Law of Thermodynamics",
            "content": (
                "The First Law of Thermodynamics states that energy cannot be created or destroyed, "
                "only transformed from one form to another. The change in internal energy of a system "
                "equals the heat added to the system minus the work done by the system."
            ),
            "tags": ["thermodynamics", "energy", "internal energy", "first law"],
        },
        {
            "title": "Second Law of Thermodynamics and Entropy",
            "content": (
                "The Second Law of Thermodynamics asserts that for any spontaneous process, "
                "the total entropy of the universe increases. Entropy is a measure of disorder or randomness. "
                "Processes with positive entropy change are favored."
            ),
            "tags": ["thermodynamics", "entropy", "second law", "spontaneity"],
        },
        {
            "title": "Gibbs Free Energy and Spontaneity",
            "content": (
                "Gibbs free energy (G) determines the spontaneity of a process at constant temperature and pressure. "
                "A negative change in Gibbs free energy (ΔG < 0) indicates a spontaneous process."
            ),
            "tags": ["gibbs free energy", "spontaneity", "thermodynamics"],
        },
        {
            "title": "Chemical Potential",
            "content": (
                "Chemical potential is the partial molar free energy of a component in a mixture. "
                "It drives chemical reactions and phase changes, and is fundamental in equilibrium thermodynamics."
            ),
            "tags": ["chemical potential", "thermodynamics", "equilibrium"],
        },
        {
            "title": "Rate Laws and Reaction Order",
            "content": (
                "Rate laws express the relationship between the rate of a chemical reaction and the concentration of reactants. "
                "The reaction order is the sum of the exponents in the rate law equation."
            ),
            "tags": ["kinetics", "rate law", "reaction order"],
        },
        {
            "title": "Arrhenius Equation",
            "content": (
                "The Arrhenius equation relates the rate constant of a reaction to temperature and activation energy: "
                "k = A * exp(-Ea/(RT)). It explains the temperature dependence of reaction rates."
            ),
            "tags": ["arrhenius equation", "kinetics", "activation energy"],
        },
        {
            "title": "Transition State Theory",
            "content": (
                "Transition State Theory describes chemical reactions as proceeding through a high-energy transition state. "
                "The rate of reaction depends on the concentration of this activated complex."
            ),
            "tags": ["transition state", "kinetics", "reaction mechanism"],
        },
        {
            "title": "Catalysis Mechanisms",
            "content": (
                "Catalysts increase reaction rates by providing alternative pathways with lower activation energy. "
                "Mechanisms include homogeneous and heterogeneous catalysis."
            ),
            "tags": ["catalysis", "kinetics", "mechanism"],
        },
        {
            "title": "Schrödinger Equation and Wavefunctions",
            "content": (
                "The Schrödinger equation is the fundamental equation of quantum mechanics. "
                "Its solutions, called wavefunctions, describe the probability distribution of particles."
            ),
            "tags": ["schrodinger equation", "quantum mechanics", "wavefunction"],
        },
        {
            "title": "Molecular Orbital Theory",
            "content": (
                "Molecular Orbital Theory explains chemical bonding by combining atomic orbitals to form molecular orbitals. "
                "Electrons in bonding orbitals stabilize molecules, while those in antibonding orbitals destabilize them."
            ),
            "tags": ["molecular orbital theory", "bonding", "quantum chemistry"],
        },
        {
            "title": "Hartree-Fock Method",
            "content": (
                "The Hartree-Fock method is an approximate procedure for determining the wavefunction and energy of a quantum many-body system. "
                "It uses a mean-field approach to simplify electron-electron interactions."
            ),
            "tags": ["hartree-fock", "quantum chemistry", "computational methods"],
        },
        {
            "title": "Statistical Mechanics Foundations",
            "content": (
                "Statistical mechanics connects microscopic particle behavior to macroscopic thermodynamic properties. "
                "It uses probability distributions to describe ensembles of particles."
            ),
            "tags": ["statistical mechanics", "thermodynamics", "ensemble"],
        },
        {
            "title": "Adsorption Isotherms",
            "content": (
                "Adsorption isotherms describe how molecules adhere to surfaces at constant temperature. "
                "Common models include Langmuir and Freundlich isotherms."
            ),
            "tags": ["adsorption", "isotherm", "surface chemistry"],
        },
        {
            "title": "Electrochemistry and Nernst Equation",
            "content": (
                "Electrochemistry studies the relationship between electricity and chemical reactions. "
                "The Nernst equation relates electrode potential to ion concentrations: "
                "E = E° - (RT/nF) * ln(Q)."
            ),
            "tags": ["electrochemistry", "nernst equation", "redox"],
        },
        {
            "title": "Spectroscopy Fundamentals",
            "content": (
                "Spectroscopy involves the interaction of electromagnetic radiation with matter. "
                "It provides information about molecular structure, dynamics, and composition."
            ),
            "tags": ["spectroscopy", "molecular structure", "analytical chemistry"],
        },
        {
            "title": "Phase Diagrams and Phase Rule",
            "content": (
                "Phase diagrams show the stability of phases as a function of temperature and pressure. "
                "The Gibbs phase rule relates the number of phases, components, and degrees of freedom."
            ),
            "tags": ["phase diagram", "gibbs phase rule", "thermodynamics"],
        },
        {
            "title": "Diffusion and Transport Phenomena",
            "content": (
                "Diffusion is the movement of particles from high to low concentration. "
                "Transport phenomena include diffusion, convection, and migration in chemical systems."
            ),
            "tags": ["diffusion", "transport phenomena", "kinetics"],
        },
        {
            "title": "Colligative Properties",
            "content": (
                "Colligative properties depend on the number of solute particles in a solution, not their identity. "
                "Examples include boiling point elevation and freezing point depression."
            ),
            "tags": ["colligative properties", "solutions", "thermodynamics"],
        },
        {
            "title": "Computational Chemistry Methods",
            "content": (
                "Computational chemistry uses algorithms and computers to solve chemical problems. "
                "Methods include ab initio, density functional theory, and molecular dynamics."
            ),
            "tags": ["computational chemistry", "ab initio", "DFT", "molecular dynamics"],
        },
        {
            "title": "Photochemistry Principles",
            "content": (
                "Photochemistry studies chemical reactions initiated by light. "
                "Key concepts include quantum yield, excited states, and photochemical pathways."
            ),
            "tags": ["photochemistry", "excited state", "quantum yield"],
        },
        {
            "title": "Polymer Physical Chemistry",
            "content": (
                "Polymer physical chemistry examines the structure, dynamics, and thermodynamics of polymers. "
                "Topics include molecular weight distribution, glass transition, and crystallinity."
            ),
            "tags": ["polymer", "physical chemistry", "thermodynamics"],
        },
        {
            "title": "Chemical Equilibrium Thermodynamics",
            "content": (
                "Chemical equilibrium occurs when the rates of forward and reverse reactions are equal. "
                "Thermodynamics provides criteria for equilibrium using Gibbs free energy."
            ),
            "tags": ["chemical equilibrium", "thermodynamics", "gibbs free energy"],
        },
        {
            "title": "Real Gas Behavior",
            "content": (
                "Real gases deviate from ideal gas behavior at high pressures and low temperatures. "
                "Equations of state like van der Waals account for intermolecular forces and finite molecular volume."
            ),
            "tags": ["real gas", "van der waals", "equation of state"],
        },
        {
            "title": "Boltzmann Distribution in Statistical Mechanics",
            "content": (
                "The Boltzmann distribution gives the probability of a system being in a particular energy state. "
                "It is fundamental to statistical mechanics and thermodynamic calculations."
            ),
            "tags": ["boltzmann distribution", "statistical mechanics", "thermodynamics"],
        },
        {
            "title": "Langmuir and Freundlich Adsorption Isotherms",
            "content": (
                "The Langmuir isotherm assumes monolayer adsorption on a homogeneous surface, "
                "while the Freundlich isotherm applies to heterogeneous surfaces."
            ),
            "tags": ["langmuir isotherm", "freundlich isotherm", "adsorption"],
        },
        {
            "title": "Electrochemical Cells and Potentials",
            "content": (
                "Electrochemical cells convert chemical energy to electrical energy. "
                "Cell potential depends on the nature of electrodes and ion concentrations."
            ),
            "tags": ["electrochemical cell", "cell potential", "electrochemistry"],
        },
        {
            "title": "Infrared and UV-Vis Spectroscopy",
            "content": (
                "Infrared spectroscopy probes molecular vibrations, while UV-Vis spectroscopy examines electronic transitions. "
                "Both are essential tools in molecular characterization."
            ),
            "tags": ["infrared spectroscopy", "uv-vis spectroscopy", "molecular characterization"],
        },
        {
            "title": "Phase Transitions and Critical Points",
            "content": (
                "Phase transitions occur when a substance changes state, such as melting or boiling. "
                "Critical points mark the end of phase boundaries in phase diagrams."
            ),
            "tags": ["phase transition", "critical point", "phase diagram"],
        },
        {
            "title": "Fick's Laws of Diffusion",
            "content": (
                "Fick's first law relates diffusion flux to concentration gradient. "
                "Fick's second law describes how concentration changes with time due to diffusion."
            ),
            "tags": ["fick's law", "diffusion", "transport"],
        },
        {
            "title": "Raoult's Law and Colligative Properties",
            "content": (
                "Raoult's law states that the vapor pressure of a solution is proportional to the mole fraction of solvent. "
                "It explains colligative properties such as boiling point elevation."
            ),
            "tags": ["raoult's law", "colligative properties", "solutions"],
        },
        {
            "title": "Density Functional Theory in Computational Chemistry",
            "content": (
                "Density Functional Theory (DFT) is a quantum mechanical method for investigating the electronic structure of molecules. "
                "It is widely used in computational chemistry due to its balance of accuracy and efficiency."
            ),
            "tags": ["density functional theory", "DFT", "computational chemistry"],
        },
        {
            "title": "Photochemical Reaction Mechanisms",
            "content": (
                "Photochemical reactions involve the absorption of light and formation of excited states. "
                "Mechanisms include intersystem crossing, internal conversion, and fluorescence."
            ),
            "tags": ["photochemical reaction", "excited state", "mechanism"],
        },
        {
            "title": "Polymerization Kinetics",
            "content": (
                "Polymerization kinetics studies the rates and mechanisms of polymer formation. "
                "Chain-growth and step-growth are two main types of polymerization."
            ),
            "tags": ["polymerization", "kinetics", "polymer"],
        },
        {
            "title": "Le Chatelier's Principle in Chemical Equilibrium",
            "content": (
                "Le Chatelier's Principle states that a system at equilibrium responds to disturbances by shifting to counteract the change. "
                "It predicts the effect of concentration, pressure, and temperature changes."
            ),
            "tags": ["le chatelier", "chemical equilibrium", "thermodynamics"],
        },
        {
            "title": "Virial Equation for Real Gases",
            "content": (
                "The virial equation is an empirical equation of state for real gases. "
                "It expresses pressure as a power series in terms of molar volume."
            ),
            "tags": ["virial equation", "real gas", "equation of state"],
        },
        {
            "title": "Partition Functions in Statistical Mechanics",
            "content": (
                "The partition function is a central quantity in statistical mechanics. "
                "It encodes all thermodynamic information about a system in equilibrium."
            ),
            "tags": ["partition function", "statistical mechanics", "thermodynamics"],
        },
        {
            "title": "Surface Catalysis and Reaction Mechanisms",
            "content": (
                "Surface catalysis involves reactions occurring at the interface between phases. "
                "Mechanisms include adsorption, reaction, and desorption steps."
            ),
            "tags": ["surface catalysis", "mechanism", "adsorption"],
        },
        {
            "title": "Quantum Yield in Photochemistry",
            "content": (
                "Quantum yield is the efficiency of a photochemical process, defined as the number of events per photon absorbed. "
                "High quantum yield indicates efficient conversion of light energy."
            ),
            "tags": ["quantum yield", "photochemistry", "efficiency"],
        },
        {
            "title": "Glass Transition in Polymers",
            "content": (
                "The glass transition is the reversible change in amorphous polymers from a hard, glassy state to a soft, rubbery state. "
                "It is characterized by a temperature called the glass transition temperature (Tg)."
            ),
            "tags": ["glass transition", "polymer", "physical chemistry"],
        },
        {
            "title": "Chemical Kinetics: Zero, First, and Second Order Reactions",
            "content": (
                "Chemical kinetics classifies reactions by order. Zero-order reactions have constant rate, "
                "first-order depend linearly on concentration, and second-order depend on the square or product of concentrations."
            ),
            "tags": ["kinetics", "reaction order", "rate law"],
        },
        {
            "title": "Quantum Mechanical Tunneling in Reactions",
            "content": (
                "Quantum tunneling allows particles to pass through energy barriers lower than their kinetic energy. "
                "It can significantly affect reaction rates, especially at low temperatures."
            ),
            "tags": ["quantum tunneling", "reaction rate", "quantum mechanics"],
        },
        {
            "title": "Nernst Equation Applications in Electrochemistry",
            "content": (
                "The Nernst equation is used to calculate cell potentials under non-standard conditions. "
                "It is essential for understanding batteries, sensors, and corrosion."
            ),
            "tags": ["nernst equation", "electrochemistry", "cell potential"],
        },
        {
            "title": "Spectroscopic Selection Rules",
            "content": (
                "Selection rules determine which transitions are allowed in spectroscopy. "
                "They depend on quantum numbers and symmetry properties of molecules."
            ),
            "tags": ["selection rules", "spectroscopy", "quantum mechanics"],
        },
        {
            "title": "Phase Rule Calculations",
            "content": (
                "The phase rule, F = C - P + 2, helps determine the degrees of freedom in a system. "
                "It is fundamental for interpreting phase diagrams."
            ),
            "tags": ["phase rule", "phase diagram", "thermodynamics"],
        },
        {
            "title": "Transport Number in Electrolyte Solutions",
            "content": (
                "The transport number is the fraction of current carried by each ion type in an electrolyte. "
                "It is important in understanding conductivity and migration."
            ),
            "tags": ["transport number", "electrolyte", "conductivity"],
        },
        {
            "title": "Boiling Point Elevation and Freezing Point Depression",
            "content": (
                "Boiling point elevation and freezing point depression are colligative properties. "
                "They depend on the number of solute particles and are used to determine molar mass."
            ),
            "tags": ["boiling point elevation", "freezing point depression", "colligative properties"],
        },
        {
            "title": "Molecular Dynamics Simulations",
            "content": (
                "Molecular dynamics simulations model the motion of atoms and molecules over time. "
                "They are widely used in computational chemistry and materials science."
            ),
            "tags": ["molecular dynamics", "simulation", "computational chemistry"],
        },
        {
            "title": "Photophysical Processes: Fluorescence and Phosphorescence",
            "content": (
                "Fluorescence and phosphorescence are photophysical processes involving emission of light. "
                "They differ in timescale and electronic state transitions."
            ),
            "tags": ["fluorescence", "phosphorescence", "photochemistry"],
        },
        {
            "title": "Polymer Crystallinity and Amorphous Regions",
            "content": (
                "Polymers can have crystalline and amorphous regions. "
                "Crystallinity affects mechanical, thermal, and optical properties."
            ),
            "tags": ["polymer", "crystallinity", "amorphous"],
        },
        {
            "title": "Equilibrium Constants and Reaction Quotients",
            "content": (
                "The equilibrium constant (K) quantifies the ratio of products to reactants at equilibrium. "
                "The reaction quotient (Q) indicates the direction a reaction will proceed."
            ),
            "tags": ["equilibrium constant", "reaction quotient", "chemical equilibrium"],
        },
        {
            "title": "Compressibility Factor for Real Gases",
            "content": (
                "The compressibility factor (Z) measures deviation of a real gas from ideal behavior. "
                "It is defined as Z = PV/nRT and is used in real gas calculations."
            ),
            "tags": ["compressibility factor", "real gas", "thermodynamics"],
        },
    ]
    for doc in docs:
        index.add_document(doc['title'], doc['content'], doc['tags'])