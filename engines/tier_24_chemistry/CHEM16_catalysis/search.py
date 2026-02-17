import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional


class SearchDocument:
    def __init__(self, doc_id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = doc_id
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


class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)  # document frequency per term
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))  # term -> doc_id -> freq
        self.doc_lengths: Dict[str, int] = {}  # doc_id -> length in tokens
        self.avg_doc_length: float = 0.0
        self.N: int = 0  # total number of documents
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                self._remove_document(doc.id)
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            length = len(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = length
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                if self.term_freqs[term][doc.id] == 0:
                    self.doc_freqs[term] += 1
                self.term_freqs[term][doc.id] = freq
            self.N = len(self.documents)
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0

    def _remove_document(self, doc_id: str):
        if doc_id not in self.documents:
            return
        old_doc = self.documents[doc_id]
        tokens = self._tokenize(old_doc.title + " " + old_doc.content + " " + " ".join(old_doc.tags))
        term_counts = Counter(tokens)
        for term in term_counts:
            if doc_id in self.term_freqs[term]:
                del self.term_freqs[term][doc_id]
                self.doc_freqs[term] -= 1
                if self.doc_freqs[term] <= 0:
                    del self.doc_freqs[term]
                    del self.term_freqs[term]
        del self.documents[doc_id]
        del self.doc_lengths[doc_id]
        self.N = len(self.documents)
        self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms or self.N == 0:
            return []
        idf_scores = {term: self._compute_idf(term) for term in set(query_terms)}
        scores: Dict[str, float] = defaultdict(float)
        for term in query_terms:
            if term not in self.term_freqs:
                continue
            idf = idf_scores.get(term, 0.0)
            postings = self.term_freqs[term]
            for doc_id, freq in postings.items():
                score = self._score_bm25(freq, idf, self.doc_lengths[doc_id])
                scores[doc_id] += score
        # Incorporate document weight as a multiplier
        for doc_id in scores:
            scores[doc_id] *= self.documents[doc_id].weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.N,
                "average_document_length": self.avg_doc_length,
                "unique_terms": len(self.doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, freq: int, idf: float, doc_len: int) -> float:
        denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
        return idf * freq * (self.k1 + 1) / denom if denom > 0 else 0.0

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + len(term)
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += "..."
            return snippet
        start_pos = max(min(positions) - snippet_len // 4, 0)
        end_pos = start_pos + snippet_len
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet += "..."
        return snippet


_singleton_instance = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _preseed_index(_singleton_instance)
        return _singleton_instance


def _preseed_index(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="hetero_adsorption_langmuir",
            title="Heterogeneous Catalysis: Surface Adsorption and Langmuir Isotherm",
            content=(
                "Surface adsorption phenomena are critical in heterogeneous catalysis. "
                "The Langmuir isotherm describes adsorption equilibrium assuming monolayer coverage "
                "and no interactions between adsorbed species. It is fundamental for modeling surface reactions."
            ),
            tags=["heterogeneous", "adsorption", "langmuir", "surface", "catalysis"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="homogeneous_wilkinson_grubbs",
            title="Homogeneous Catalysis: Organometallic Mechanisms (Wilkinson, Grubbs)",
            content=(
                "Organometallic complexes such as Wilkinson's catalyst and Grubbs catalysts "
                "are pivotal in homogeneous catalysis. Their mechanisms involve oxidative addition, "
                "reductive elimination, and ligand exchange facilitating selective transformations."
            ),
            tags=["homogeneous", "organometallic", "wilkinson", "grubbs", "mechanism"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="enzyme_michaelis_menten",
            title="Enzyme Kinetics: Michaelis-Menten and Inhibition",
            content=(
                "Michaelis-Menten kinetics describe enzyme-catalyzed reaction rates with substrate concentration. "
                "Inhibition types include competitive, non-competitive, and uncompetitive, affecting enzyme activity."
            ),
            tags=["enzyme", "kinetics", "michaelis-menten", "inhibition"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="catalyst_characterization_xrd_bet",
            title="Catalyst Characterization: XRD, BET, TPR, TPD, XPS",
            content=(
                "Characterization techniques such as XRD for crystallinity, BET for surface area, "
                "TPR and TPD for redox and adsorption properties, and XPS for surface composition "
                "are essential in catalyst analysis."
            ),
            tags=["characterization", "xrd", "bet", "tpr", "tpd", "xps"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="reaction_kinetics_arrhenius",
            title="Reaction Kinetics: Rate Laws and Arrhenius Equation",
            content=(
                "Rate laws express reaction rates as functions of reactant concentrations. "
                "The Arrhenius equation relates rate constants to temperature and activation energy."
            ),
            tags=["kinetics", "rate law", "arrhenius", "activation energy"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="reactor_design_cstr_pfr_batch",
            title="Reactor Design: CSTR, PFR, Batch, Semi-batch",
            content=(
                "Reactor types include Continuous Stirred Tank Reactor (CSTR), Plug Flow Reactor (PFR), "
                "batch, and semi-batch reactors, each with unique flow and mixing characteristics."
            ),
            tags=["reactor", "design", "cstr", "pfr", "batch", "semi-batch"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="catalyst_deactivation_sintering_poisoning",
            title="Catalyst Deactivation: Sintering, Poisoning, Coking",
            content=(
                "Catalyst deactivation mechanisms include sintering (particle growth), poisoning "
                "(adsorption of poisons), and coking (carbon deposition), reducing catalyst activity."
            ),
            tags=["deactivation", "sintering", "poisoning", "coking"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="zeolite_shape_selectivity_acidity",
            title="Zeolite Catalysis: Shape Selectivity and Acidity",
            content=(
                "Zeolites exhibit shape selectivity due to their pore structure and acidity, "
                "which influence catalytic activity and selectivity in hydrocarbon transformations."
            ),
            tags=["zeolite", "shape selectivity", "acidity", "catalysis"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="fischer_tropsch_cobalt_iron",
            title="Fischer-Tropsch Synthesis: Cobalt and Iron Catalysts",
            content=(
                "Fischer-Tropsch synthesis converts syngas to hydrocarbons using cobalt or iron catalysts, "
                "each with distinct activity and selectivity profiles."
            ),
            tags=["fischer-tropsch", "cobalt", "iron", "catalysts"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="hydrocracking_hydrodesulfurization_hydrotreating",
            title="Hydrocracking, Hydrodesulfurization, and Hydrotreating",
            content=(
                "Hydrocracking breaks heavy hydrocarbons into lighter fractions; hydrodesulfurization "
                "removes sulfur compounds; hydrotreating improves fuel quality via catalytic hydrogenation."
            ),
            tags=["hydrocracking", "hydrodesulfurization", "hydrotreating"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="fcc_riser_regenerator",
            title="Fluid Catalytic Cracking (FCC): Riser and Regenerator",
            content=(
                "FCC units consist of riser reactors for cracking and regenerators to burn coke off catalysts, "
                "enabling continuous operation."
            ),
            tags=["fcc", "fluid catalytic cracking", "riser", "regenerator"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="haber_bosch_iron_catalyst",
            title="Haber-Bosch Ammonia Synthesis: Iron Catalyst",
            content=(
                "The Haber-Bosch process synthesizes ammonia from nitrogen and hydrogen over iron catalysts "
                "under high temperature and pressure."
            ),
            tags=["haber-bosch", "ammonia", "iron catalyst"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="catalytic_converter_twc",
            title="Catalytic Converter: TWC (Platinum, Palladium, Rhodium)",
            content=(
                "Three-way catalytic converters (TWC) use platinum, palladium, and rhodium to reduce "
                "NOx, CO, and hydrocarbons in automotive exhaust."
            ),
            tags=["catalytic converter", "twc", "platinum", "palladium", "rhodium"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="photocatalysis_tio2_bandgap_uv",
            title="Photocatalysis: TiO2, Band Gap, UV/Visible Activation",
            content=(
                "TiO2 is a widely studied photocatalyst activated by UV light due to its band gap, "
                "enabling oxidation and reduction reactions under light irradiation."
            ),
            tags=["photocatalysis", "tio2", "band gap", "uv", "visible"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="electrocatalysis_her_oer_orr",
            title="Electrocatalysis: HER, OER, ORR, Overpotential",
            content=(
                "Electrocatalysis involves reactions like Hydrogen Evolution Reaction (HER), Oxygen Evolution Reaction (OER), "
                "and Oxygen Reduction Reaction (ORR), with overpotential as a key performance metric."
            ),
            tags=["electrocatalysis", "her", "oer", "orr", "overpotential"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="biocatalysis_immobilized_enzymes_whole_cells",
            title="Biocatalysis: Immobilized Enzymes and Whole Cells",
            content=(
                "Biocatalysis uses enzymes or whole cells to catalyze reactions. Immobilization enhances stability and reuse."
            ),
            tags=["biocatalysis", "immobilized enzymes", "whole cells"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="catalyst_selectivity_conversion_yield_ton_tof",
            title="Catalyst Selectivity, Conversion, Yield, TON, TOF",
            content=(
                "Catalyst performance metrics include selectivity, conversion, yield, Turnover Number (TON), "
                "and Turnover Frequency (TOF) to evaluate efficiency."
            ),
            tags=["selectivity", "conversion", "yield", "ton", "tof"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="mass_transfer_thiele_modulus_effectiveness_factor",
            title="Mass Transfer Limitations: Thiele Modulus and Effectiveness Factor",
            content=(
                "Mass transfer limitations in porous catalysts are quantified by the Thiele modulus and effectiveness factor, "
                "which influence reaction rates."
            ),
            tags=["mass transfer", "thiele modulus", "effectiveness factor"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="catalyst_regeneration_oxidative_reductive",
            title="Catalyst Regeneration: Oxidative and Reductive Methods",
            content=(
                "Catalyst regeneration restores activity via oxidative or reductive treatments to remove poisons or coke."
            ),
            tags=["regeneration", "oxidative", "reductive", "catalyst"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="green_chemistry_atom_e_factor",
            title="Green Chemistry: Atom Economy and E-Factor",
            content=(
                "Green chemistry metrics such as atom economy and E-factor assess the environmental impact of chemical processes."
            ),
            tags=["green chemistry", "atom economy", "e-factor"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="langmuir_adsorption_equation",
            title="Langmuir Adsorption Equation",
            content=(
                "The Langmuir adsorption equation models the fractional coverage of adsorbates on catalyst surfaces "
                "as a function of pressure and adsorption constants."
            ),
            tags=["langmuir", "adsorption", "equation", "surface"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="wilkinson_catalyst_mechanism",
            title="Wilkinson Catalyst Mechanism",
            content=(
                "Wilkinson's catalyst operates via oxidative addition, migratory insertion, and reductive elimination "
                "steps in homogeneous hydrogenation reactions."
            ),
            tags=["wilkinson", "catalyst", "mechanism", "homogeneous"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="grubbs_catalyst_metathesis",
            title="Grubbs Catalyst and Olefin Metathesis",
            content=(
                "Grubbs catalysts facilitate olefin metathesis through a well-defined organometallic mechanism "
                "involving metallacyclobutane intermediates."
            ),
            tags=["grubbs", "catalyst", "olefin", "metathesis"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="michaelis_menten_equation",
            title="Michaelis-Menten Equation",
            content=(
                "The Michaelis-Menten equation relates reaction velocity to substrate concentration, "
                "defining parameters Vmax and Km for enzyme kinetics."
            ),
            tags=["michaelis-menten", "enzyme", "kinetics", "equation"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="competitive_inhibition",
            title="Competitive Enzyme Inhibition",
            content=(
                "Competitive inhibition occurs when inhibitors compete with substrates for active sites, "
                "increasing apparent Km without affecting Vmax."
            ),
            tags=["enzyme", "inhibition", "competitive"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="tpr_tpd_methods",
            title="Temperature Programmed Reduction and Desorption (TPR, TPD)",
            content=(
                "TPR and TPD techniques analyze catalyst redox properties and adsorption strength "
                "by monitoring gas evolution during controlled temperature ramps."
            ),
            tags=["tpr", "tpd", "catalyst", "characterization"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="xps_surface_analysis",
            title="X-ray Photoelectron Spectroscopy (XPS) for Surface Analysis",
            content=(
                "XPS provides elemental composition and chemical state information of catalyst surfaces "
                "via photoelectron emission spectra."
            ),
            tags=["xps", "surface", "analysis", "catalyst"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="arrhenius_activation_energy",
            title="Arrhenius Equation and Activation Energy",
            content=(
                "The Arrhenius equation models the temperature dependence of reaction rates, "
                "with activation energy as a key parameter."
            ),
            tags=["arrhenius", "activation energy", "kinetics"],
            weight=1.0,
        ),
    ]
    for doc in docs:
        index.add_document(doc)