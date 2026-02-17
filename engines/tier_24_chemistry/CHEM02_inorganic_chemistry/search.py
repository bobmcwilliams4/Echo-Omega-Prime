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
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)  # term -> doc_id -> freq
        self.doc_lengths: Dict[str, int] = {}  # doc_id -> length in tokens
        self.avg_doc_length: float = 0.0
        self.N: int = 0  # total number of documents
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()

    def add_document(self, document: SearchDocument):
        with self.lock:
            if document.id in self.documents:
                # Remove old document stats
                self._remove_document(document.id)

            tokens = self._tokenize(document.content)
            length = len(tokens)
            self.documents[document.id] = document
            self.doc_lengths[document.id] = length
            self.N = len(self.documents)

            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                if document.id not in self.term_freqs[term]:
                    self.doc_freqs[term] += 1
                self.term_freqs[term][document.id] = freq

            self._update_avg_doc_length()
            self.idf_cache.clear()

    def _remove_document(self, doc_id: str):
        if doc_id not in self.documents:
            return
        old_doc = self.documents[doc_id]
        old_tokens = self._tokenize(old_doc.content)
        old_term_counts = Counter(old_tokens)
        for term in old_term_counts:
            if doc_id in self.term_freqs[term]:
                del self.term_freqs[term][doc_id]
                self.doc_freqs[term] -= 1
                if self.doc_freqs[term] <= 0:
                    del self.doc_freqs[term]
                    del self.term_freqs[term]
        del self.documents[doc_id]
        del self.doc_lengths[doc_id]
        self.N = len(self.documents)
        self._update_avg_doc_length()
        self.idf_cache.clear()

    def _update_avg_doc_length(self):
        if self.N == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N

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

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        for term in query_terms:
            if doc_id not in self.term_freqs.get(term, {}):
                continue
            tf = self.term_freqs[term][doc_id]
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length) if self.avg_doc_length > 0 else 1
            score += idf * numerator / denominator
        doc_weight = self.documents[doc_id].weight if doc_id in self.documents else 1.0
        return score * doc_weight

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms or self.N == 0:
            return []

        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_freqs.get(term, {}).keys())

        scored_docs: List[Tuple[str, float]] = []
        for doc_id in candidate_docs:
            score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scored_docs.append((doc_id, score))

        scored_docs.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scored_docs[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            for match in re.finditer(r'\b' + re.escape(term) + r'\b', content_lower):
                positions.append(match.start())
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += "..."
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_len // 4, 0)
        end_pos = start_pos + snippet_len
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet += "..."
        return snippet

    def get_stats(self) -> Dict[str, int]:
        return {
            "total_documents": self.N,
            "total_terms": len(self.doc_freqs),
            "average_document_length": int(self.avg_doc_length),
        }


_singleton_instance = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _seed_documents(_singleton_instance)
    return _singleton_instance


def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="coordination_chemistry_fundamentals_01",
            title="Coordination Chemistry: Ligands and Complexes",
            content=(
                "Coordination chemistry studies the structures and properties of complexes formed between metal ions "
                "and ligands. Ligands are ions or molecules that donate electron pairs to the metal center, forming "
                "coordinate covalent bonds. Common ligands include water, ammonia, and halides."
            ),
            tags=["coordination_chemistry_fundamentals", "ligands", "complexes"]
        ),
        SearchDocument(
            doc_id="crystal_field_theory_01",
            title="Crystal Field Theory Basics",
            content=(
                "Crystal Field Theory explains the electronic structure of transition metal complexes by considering "
                "the effect of the electrostatic field produced by ligands on the d-orbitals of the metal ion. "
                "It accounts for the splitting of d-orbitals into different energy levels."
            ),
            tags=["crystal_field_theory", "transition_metal_chemistry"]
        ),
        SearchDocument(
            doc_id="transition_metal_chemistry_01",
            title="Properties of Transition Metals",
            content=(
                "Transition metals are characterized by partially filled d-orbitals, variable oxidation states, and "
                "the ability to form colored compounds. They often act as catalysts in chemical reactions."
            ),
            tags=["transition_metal_chemistry", "catalysis_homogeneous_heterogeneous"]
        ),
        SearchDocument(
            doc_id="main_group_chemistry_01",
            title="Main Group Elements and Their Chemistry",
            content=(
                "Main group chemistry involves the study of s- and p-block elements. These elements exhibit predictable "
                "oxidation states and form a wide variety of compounds including oxides, halides, and hydrides."
            ),
            tags=["main_group_chemistry"]
        ),
        SearchDocument(
            doc_id="lanthanides_actinides_01",
            title="Lanthanides and Actinides Overview",
            content=(
                "Lanthanides and actinides are f-block elements characterized by their filling of 4f and 5f orbitals, "
                "respectively. They exhibit unique magnetic and spectroscopic properties and are important in nuclear chemistry."
            ),
            tags=["lanthanides_actinides", "nuclear_chemistry_basics"]
        ),
        SearchDocument(
            doc_id="bioinorganic_chemistry_01",
            title="Bioinorganic Chemistry: Metal Ions in Biology",
            content=(
                "Bioinorganic chemistry studies the role of metal ions in biological systems, including metalloproteins, "
                "enzymes, and electron transfer processes."
            ),
            tags=["bioinorganic_chemistry"]
        ),
        SearchDocument(
            doc_id="solid_state_chemistry_01",
            title="Introduction to Solid State Chemistry",
            content=(
                "Solid state chemistry focuses on the synthesis, structure, and properties of solid materials, including "
                "crystals, ceramics, and semiconductors."
            ),
            tags=["solid_state_chemistry", "ceramic_chemistry", "semiconductor_chemistry"]
        ),
        SearchDocument(
            doc_id="catalysis_homogeneous_heterogeneous_01",
            title="Homogeneous and Heterogeneous Catalysis",
            content=(
                "Catalysis can be homogeneous, where the catalyst is in the same phase as the reactants, or heterogeneous, "
                "where the catalyst is in a different phase. Transition metals often serve as catalysts."
            ),
            tags=["catalysis_homogeneous_heterogeneous", "transition_metal_chemistry"]
        ),
        SearchDocument(
            doc_id="organometallic_chemistry_01",
            title="Organometallic Chemistry Fundamentals",
            content=(
                "Organometallic chemistry studies compounds containing metal-carbon bonds. These compounds are important "
                "in catalysis and synthesis."
            ),
            tags=["organometallic_chemistry", "catalysis_homogeneous_heterogeneous"]
        ),
        SearchDocument(
            doc_id="symmetry_group_theory_01",
            title="Symmetry and Group Theory in Chemistry",
            content=(
                "Group theory provides a mathematical framework to describe symmetry in molecules, which helps predict "
                "spectroscopic properties and chemical reactivity."
            ),
            tags=["symmetry_group_theory", "spectroscopic_methods_inorganic"]
        ),
        SearchDocument(
            doc_id="thermodynamics_inorganic_reactions_01",
            title="Thermodynamics of Inorganic Reactions",
            content=(
                "Thermodynamics studies energy changes in inorganic reactions, including enthalpy, entropy, and Gibbs free energy."
            ),
            tags=["thermodynamics_inorganic_reactions"]
        ),
        SearchDocument(
            doc_id="kinetics_inorganic_reactions_01",
            title="Kinetics of Inorganic Reactions",
            content=(
                "Kinetics focuses on the rates and mechanisms of inorganic reactions, including factors affecting reaction speed."
            ),
            tags=["kinetics_inorganic_reactions"]
        ),
        SearchDocument(
            doc_id="electrochemistry_redox_01",
            title="Electrochemistry and Redox Reactions",
            content=(
                "Electrochemistry studies redox reactions and electron transfer processes, including galvanic and electrolytic cells."
            ),
            tags=["electrochemistry_redox"]
        ),
        SearchDocument(
            doc_id="corrosion_science_01",
            title="Corrosion Science Fundamentals",
            content=(
                "Corrosion is the degradation of materials due to chemical reactions with the environment, often involving oxidation."
            ),
            tags=["corrosion_science", "electrochemistry_redox"]
        ),
        SearchDocument(
            doc_id="materials_science_fundamentals_01",
            title="Materials Science: Fundamentals",
            content=(
                "Materials science explores the properties, structure, and applications of materials including metals, ceramics, and polymers."
            ),
            tags=["materials_science_fundamentals", "ceramic_chemistry"]
        ),
        SearchDocument(
            doc_id="ceramic_chemistry_01",
            title="Ceramic Chemistry and Properties",
            content=(
                "Ceramics are inorganic, non-metallic solids with high melting points and hardness, used in various industrial applications."
            ),
            tags=["ceramic_chemistry", "solid_state_chemistry"]
        ),
        SearchDocument(
            doc_id="semiconductor_chemistry_01",
            title="Semiconductor Chemistry Basics",
            content=(
                "Semiconductors have electrical conductivity between conductors and insulators, essential for electronic devices."
            ),
            tags=["semiconductor_chemistry", "solid_state_chemistry"]
        ),
        SearchDocument(
            doc_id="nuclear_chemistry_basics_01",
            title="Basics of Nuclear Chemistry",
            content=(
                "Nuclear chemistry studies radioactive elements, nuclear reactions, and applications in energy and medicine."
            ),
            tags=["nuclear_chemistry_basics", "lanthanides_actinides"]
        ),
        SearchDocument(
            doc_id="environmental_inorganic_chemistry_01",
            title="Environmental Inorganic Chemistry",
            content=(
                "This field studies the behavior and impact of inorganic substances in the environment, including pollutants and remediation."
            ),
            tags=["environmental_inorganic_chemistry", "water_treatment_chemistry"]
        ),
        SearchDocument(
            doc_id="industrial_inorganic_processes_01",
            title="Industrial Inorganic Chemical Processes",
            content=(
                "Industrial inorganic chemistry involves large-scale chemical processes such as Haber-Bosch ammonia synthesis and contact process."
            ),
            tags=["industrial_inorganic_processes"]
        ),
        SearchDocument(
            doc_id="water_treatment_chemistry_01",
            title="Chemistry of Water Treatment",
            content=(
                "Water treatment chemistry focuses on removing contaminants and pathogens from water using chemical and physical methods."
            ),
            tags=["water_treatment_chemistry", "environmental_inorganic_chemistry"]
        ),
        SearchDocument(
            doc_id="geochemistry_01",
            title="Geochemistry: Inorganic Elements in Earth",
            content=(
                "Geochemistry studies the distribution and cycling of inorganic elements and minerals in the Earth's crust and oceans."
            ),
            tags=["geochemistry", "solid_state_chemistry"]
        ),
        SearchDocument(
            doc_id="spectroscopic_methods_inorganic_01",
            title="Spectroscopic Methods in Inorganic Chemistry",
            content=(
                "Spectroscopy techniques such as UV-Vis, IR, NMR, and EPR are used to analyze inorganic compounds and their electronic structures."
            ),
            tags=["spectroscopic_methods_inorganic", "symmetry_group_theory"]
        ),
        SearchDocument(
            doc_id="acid_base_concepts_01",
            title="Acid-Base Concepts in Inorganic Chemistry",
            content=(
                "Acid-base chemistry involves proton transfer, Lewis acid-base theory, and the behavior of acids and bases in inorganic systems."
            ),
            tags=["acid_base_concepts"]
        ),
        SearchDocument(
            doc_id="coordination_chemistry_fundamentals_02",
            title="Chelation and Stability of Complexes",
            content=(
                "Chelation involves ligands that form multiple bonds to a single metal center, increasing complex stability and affecting reactivity."
            ),
            tags=["coordination_chemistry_fundamentals"]
        ),
        SearchDocument(
            doc_id="crystal_field_theory_02",
            title="Octahedral and Tetrahedral Field Splitting",
            content=(
                "Crystal field splitting differs in octahedral and tetrahedral geometries, influencing the color and magnetic properties of complexes."
            ),
            tags=["crystal_field_theory"]
        ),
        SearchDocument(
            doc_id="transition_metal_chemistry_02",
            title="Catalytic Cycles of Transition Metals",
            content=(
                "Transition metals facilitate catalytic cycles involving oxidative addition, reductive elimination, and ligand exchange."
            ),
            tags=["transition_metal_chemistry", "catalysis_homogeneous_heterogeneous"]
        ),
        SearchDocument(
            doc_id="organometallic_chemistry_02",
            title="Common Organometallic Reagents",
            content=(
                "Organometallic reagents such as Grignard reagents and organolithiums are key tools in synthetic inorganic and organic chemistry."
            ),
            tags=["organometallic_chemistry"]
        ),
        SearchDocument(
            doc_id="electrochemistry_redox_02",
            title="Redox Potentials and Electrochemical Cells",
            content=(
                "Redox potentials determine the direction of electron flow in electrochemical cells, important for batteries and corrosion."
            ),
            tags=["electrochemistry_redox", "corrosion_science"]
        ),
    ]

    for doc in docs:
        index.add_document(doc)