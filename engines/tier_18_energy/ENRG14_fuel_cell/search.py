import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self._documents: Dict[int, SearchDocument] = {}
        self._doc_tokens: Dict[int, List[str]] = {}
        self._inverted_index: Dict[str, set] = defaultdict(set)
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._term_freq: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._total_docs: int = 0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove punctuation, split on whitespace
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self._lock:
            if doc.id in self._documents:
                return  # No duplicates
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            self._documents[doc.id] = doc
            self._doc_tokens[doc.id] = tokens
            tf = Counter(tokens)
            self._term_freq[doc.id] = tf
            self._doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self._inverted_index[term].add(doc.id)
                self._doc_freq[term] += 1
            self._total_docs += 1
            self._avg_doc_length = sum(self._doc_lengths.values()) / self._total_docs
            self._idf_cache.clear()  # Invalidate cache

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self._doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self._total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc_len = self._doc_lengths[doc_id]
        tf = self._term_freq[doc_id]
        doc = self._documents[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / self._avg_doc_length)
            numer = f * (self._bm25_k1 + 1)
            bm25 = idf * numer / denom
            score += bm25
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self._term_freq[doc_id]
        doc_len = self._doc_lengths[doc_id]
        doc = self._documents[doc_id]
        score = 0.0
        for term in query_terms:
            term_tf = tf.get(term, 0) / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += term_tf * idf
        return score * doc.weight

    def _snippet(self, doc: SearchDocument, query_terms: List[str], maxlen: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:maxlen]
        else:
            idx = positions[0]
            start = max(0, idx - 10)
            end = min(len(tokens), idx + 20)
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        # Highlight query terms
        for term in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:maxlen] + ('...' if len(snippet) > maxlen else '')

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs |= self._inverted_index.get(term, set())
        scores = []
        for doc_id in candidate_docs:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                doc = self._documents[doc_id]
                snippet = self._snippet(doc, query_terms)
                scores.append(SearchResult(doc_id, score, doc.title, snippet))
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self._total_docs,
            'avg_doc_length': self._avg_doc_length,
            'unique_terms': len(self._doc_freq)
        }

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
        SearchDocument(
            1,
            "PEM Fuel Cell Nafion Membrane Humidification",
            "Proper humidification of the Nafion membrane is critical for optimal proton conductivity in PEM fuel cells. Insufficient humidity leads to increased ohmic resistance, while excess water causes flooding. Water management strategies include external humidifiers, recirculation, and advanced flow field designs.",
            ["PEM", "Nafion", "humidification", "water management"],
            1.2
        ),
        SearchDocument(
            2,
            "SOFC YSZ Electrolyte Stability",
            "Yttria-stabilized zirconia (YSZ) is the standard electrolyte in solid oxide fuel cells (SOFCs) due to its high oxygen ion conductivity and chemical stability at elevated temperatures. Degradation can occur via impurity poisoning and phase changes under reducing conditions.",
            ["SOFC", "YSZ", "electrolyte", "stability"],
            1.1
        ),
        SearchDocument(
            3,
            "MCFC Lithium Potassium Carbonate Chemistry",
            "Molten carbonate fuel cells (MCFCs) utilize a eutectic mixture of lithium and potassium carbonate as the electrolyte. The carbonate ions conduct charge between electrodes, but electrolyte loss via vaporization and corrosion of cell components are key challenges.",
            ["MCFC", "carbonate", "lithium", "potassium", "electrolyte"],
            1.0
        ),
        SearchDocument(
            4,
            "PAFC Phosphoric Acid Fuel Cell Pt Catalyst",
            "Phosphoric acid fuel cells (PAFCs) use platinum catalysts on both anode and cathode. Catalyst poisoning by CO and phosphate ions reduces performance. Advances in catalyst support materials and alloying improve durability and activity.",
            ["PAFC", "phosphoric acid", "platinum", "catalyst"],
            1.0
        ),
        SearchDocument(
            5,
            "AFC Alkaline Fuel Cell KOH Electrolyte Management",
            "Alkaline fuel cells (AFCs) employ potassium hydroxide (KOH) as the electrolyte. Carbon dioxide contamination leads to carbonate formation, reducing conductivity. Electrolyte management includes CO2 scrubbing and periodic replacement.",
            ["AFC", "alkaline", "KOH", "electrolyte", "management"],
            1.0
        ),
        SearchDocument(
            6,
            "DMFC Direct Methanol Crossover and Efficiency",
            "Direct methanol fuel cells (DMFCs) suffer from methanol crossover through the membrane, which reduces fuel efficiency and causes cathode depolarization. Membrane development and operating condition optimization are active research areas.",
            ["DMFC", "methanol", "crossover", "efficiency"],
            1.1
        ),
        SearchDocument(
            7,
            "Hydrogen Production via Water Electrolysis",
            "Water electrolysis splits water into hydrogen and oxygen using electricity. PEM and alkaline electrolyzers differ in membrane and catalyst requirements. Efficiency depends on overpotentials and cell design.",
            ["hydrogen", "electrolysis", "PEM", "alkaline"],
            1.2
        ),
        SearchDocument(
            8,
            "Hydrogen Production via Steam Methane Reforming (SMR)",
            "Steam methane reforming (SMR) is the dominant industrial method for hydrogen production. Methane reacts with steam over a nickel catalyst to produce hydrogen and carbon monoxide. CO2 emissions and catalyst deactivation are key issues.",
            ["hydrogen", "SMR", "steam methane reforming", "nickel", "catalyst"],
            1.1
        ),
        SearchDocument(
            9,
            "Hydrogen Storage: Compressed, Liquid, and Metal Hydrides",
            "Hydrogen can be stored as compressed gas, cryogenic liquid, or in metal hydrides. Each method has trade-offs in terms of energy density, safety, and infrastructure requirements. Metal hydrides offer high volumetric density but require thermal management.",
            ["hydrogen", "storage", "compressed", "liquid", "metal hydride"],
            1.1
        ),
        SearchDocument(
            10,
            "Fuel Cell Stack: Bipolar Plate, MEA, and GDL Integration",
            "A fuel cell stack integrates multiple single cells using bipolar plates, membrane electrode assemblies (MEA), and gas diffusion layers (GDL). Stack design affects power density, durability, and thermal management.",
            ["fuel cell", "stack", "bipolar plate", "MEA", "GDL"],
            1.2
        ),
        SearchDocument(
            11,
            "Nernst Equation and Open Circuit Voltage Losses",
            "The Nernst equation predicts the theoretical open circuit voltage (OCV) of a fuel cell based on reactant activities. Real cells exhibit OCV losses due to gas crossover, mixed potentials, and non-idealities.",
            ["Nernst equation", "OCV", "voltage loss"],
            1.0
        ),
        SearchDocument(
            12,
            "Activation Overpotential: Butler-Volmer and Tafel Analysis",
            "Activation overpotential arises from the energy barrier for electrochemical reactions. The Butler-Volmer equation describes current-overpotential behavior, while the Tafel slope provides kinetic parameters for electrode reactions.",
            ["activation overpotential", "Butler-Volmer", "Tafel", "kinetics"],
            1.1
        ),
        SearchDocument(
            13,
            "Ohmic Losses: Membrane and Contact Resistance",
            "Ohmic losses in fuel cells result from ionic resistance in the membrane and electronic resistance at contacts. Minimizing these losses involves optimizing membrane thickness and improving electrical connections.",
            ["ohmic loss", "membrane", "contact resistance"],
            1.1
        ),
        SearchDocument(
            14,
            "Concentration Losses: Mass Transport and Limiting Current",
            "Concentration losses occur when reactant transport to the electrode is insufficient at high current densities, leading to limiting current. Optimizing flow fields and GDL properties mitigates these losses.",
            ["concentration loss", "mass transport", "limiting current"],
            1.0
        ),
        SearchDocument(
            15,
            "PEM Fuel Cell Water Management Strategies",
            "Effective water management in PEM fuel cells balances membrane hydration and prevents flooding. Techniques include humidified reactant gases, hydrophobic GDLs, and micro-porous layers.",
            ["PEM", "water management", "flooding", "hydration"],
            1.0
        ),
        SearchDocument(
            16,
            "YSZ Electrolyte Degradation Mechanisms in SOFCs",
            "YSZ electrolytes degrade via impurity poisoning, grain boundary migration, and phase instability under reducing atmospheres. Dopant optimization and protective coatings enhance longevity.",
            ["YSZ", "SOFC", "degradation", "impurity"],
            1.0
        ),
        SearchDocument(
            17,
            "MCFC Cathode Corrosion and Electrolyte Loss",
            "MCFC cathodes are susceptible to corrosion, leading to electrolyte loss and cell performance decline. Material selection and atmosphere control are key mitigation strategies.",
            ["MCFC", "cathode", "corrosion", "electrolyte loss"],
            1.0
        ),
        SearchDocument(
            18,
            "Platinum Catalyst Durability in PAFCs",
            "Platinum catalyst durability in PAFCs is challenged by phosphate adsorption and CO poisoning. Alloying and alternative supports improve resistance to deactivation.",
            ["PAFC", "platinum", "catalyst", "durability"],
            1.0
        ),
        SearchDocument(
            19,
            "CO2 Management in Alkaline Fuel Cells",
            "CO2 ingress in AFCs leads to potassium carbonate formation, reducing electrolyte conductivity. CO2 scrubbers and sealed designs are used to maintain performance.",
            ["AFC", "CO2", "potassium carbonate", "conductivity"],
            1.0
        ),
        SearchDocument(
            20,
            "Methanol Crossover Mitigation in DMFCs",
            "Methanol crossover in DMFCs is mitigated by using barrier membranes, lower methanol concentrations, and temperature optimization.",
            ["DMFC", "methanol", "crossover", "barrier membrane"],
            1.0
        ),
        SearchDocument(
            21,
            "PEM Electrolyzer Efficiency and Catalyst Selection",
            "PEM electrolyzer efficiency is influenced by catalyst activity, membrane conductivity, and cell design. Iridium oxide and platinum are common catalysts.",
            ["PEM", "electrolyzer", "efficiency", "catalyst"],
            1.0
        ),
        SearchDocument(
            22,
            "Nickel Catalyst Deactivation in SMR",
            "Nickel catalysts in SMR deactivate due to carbon deposition and sintering. Steam-to-carbon ratio and catalyst supports are optimized to extend lifespan.",
            ["SMR", "nickel", "catalyst", "deactivation"],
            1.0
        ),
        SearchDocument(
            23,
            "Hydrogen Storage in Metal Hydrides",
            "Metal hydrides store hydrogen via reversible absorption. Alloys such as LaNi5 and MgH2 are studied for their storage capacity and kinetics.",
            ["hydrogen", "metal hydride", "storage", "alloy"],
            1.0
        ),
        SearchDocument(
            24,
            "Fuel Cell Stack Cooling and Thermal Management",
            "Thermal management in fuel cell stacks ensures even temperature distribution and prevents hot spots. Cooling plates and heat exchangers are integrated into stack designs.",
            ["fuel cell", "stack", "thermal management", "cooling"],
            1.0
        ),
        SearchDocument(
            25,
            "Open Circuit Voltage Losses in PEM Fuel Cells",
            "PEM fuel cells experience OCV losses due to hydrogen crossover, catalyst contamination, and membrane defects. Diagnostic techniques include cyclic voltammetry and gas analysis.",
            ["PEM", "OCV", "voltage loss", "diagnostics"],
            1.0
        ),
        SearchDocument(
            26,
            "Tafel Slope Analysis for Electrocatalysts",
            "Tafel slope analysis provides insight into the rate-determining step of electrode reactions. Lower slopes indicate faster kinetics and more efficient catalysts.",
            ["Tafel", "electrocatalyst", "kinetics", "analysis"],
            1.0
        ),
        SearchDocument(
            27,
            "Membrane Resistance and Ohmic Losses in PEM Cells",
            "Membrane resistance is a major contributor to ohmic losses in PEM fuel cells. Thinner membranes and improved ionomer formulations reduce resistance.",
            ["PEM", "membrane", "ohmic loss", "resistance"],
            1.0
        ),
        SearchDocument(
            28,
            "Limiting Current Phenomena in Fuel Cells",
            "Limiting current occurs when reactant supply cannot meet demand at high loads, leading to sharp voltage drops. Flow field and GDL design are critical to avoid this regime.",
            ["limiting current", "fuel cell", "flow field", "GDL"],
            1.0
        ),
        SearchDocument(
            29,
            "Advanced Flow Field Designs for PEM Water Management",
            "Innovative flow field geometries enhance water removal and distribution in PEM fuel cells, improving performance and durability.",
            ["PEM", "flow field", "water management", "durability"],
            1.0
        ),
        SearchDocument(
            30,
            "Gas Diffusion Layer (GDL) Optimization in Fuel Cells",
            "GDL properties such as porosity, hydrophobicity, and thickness influence mass transport and water management in fuel cells.",
            ["GDL", "fuel cell", "mass transport", "optimization"],
            1.0
        ),
        SearchDocument(
            31,
            "Hydrogen Storage: Compressed Gas Safety Considerations",
            "Compressed hydrogen storage requires robust vessel design and safety mechanisms to prevent leaks and explosions.",
            ["hydrogen", "storage", "compressed", "safety"],
            1.0
        ),
        SearchDocument(
            32,
            "Cryogenic Hydrogen Storage Technologies",
            "Cryogenic storage of hydrogen as a liquid enables high energy density but requires insulation and boil-off management.",
            ["hydrogen", "storage", "cryogenic", "liquid"],
            1.0
        ),
        SearchDocument(
            33,
            "Proton Conductivity in Nafion Membranes",
            "Nafion membranes conduct protons via hydrated ionic clusters. Conductivity depends on water content and temperature.",
            ["Nafion", "proton conductivity", "membrane", "hydration"],
            1.0
        ),
        SearchDocument(
            34,
            "Electrolyte Vaporization in MCFCs",
            "Electrolyte vaporization in MCFCs leads to loss of carbonate and reduced cell life. Operating temperature and pressure are optimized to minimize losses.",
            ["MCFC", "electrolyte", "vaporization", "carbonate"],
            1.0
        ),
        SearchDocument(
            35,
            "Pt Alloy Catalysts for Improved PAFC Performance",
            "Alloying platinum with transition metals enhances catalyst activity and durability in phosphoric acid fuel cells.",
            ["PAFC", "platinum", "alloy", "catalyst"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)