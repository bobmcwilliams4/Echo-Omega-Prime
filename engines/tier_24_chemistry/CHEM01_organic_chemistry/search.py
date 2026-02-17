import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Optional

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

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_tokens: Dict[int, List[str]] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.N: int = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for token in set(tokens):
                self.inverted_index[token].add(doc.id)
                self.term_doc_freq[token] += 1
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        candidate_docs = set()
        for token in query_tokens:
            candidate_docs.update(self.inverted_index.get(token, set()))
        scored_results = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            final_score = 0.7 * bm25_score + 0.3 * tfidf_score
            snippet = self._make_snippet(self.documents[doc_id], query_tokens)
            scored_results.append(SearchResult(doc_id, final_score, self.documents[doc_id].title, snippet))
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_length,
            "vocab_size": len(self.inverted_index)
        }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r"\b[a-zA-Z0-9']+\b", text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            return 0.0
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = self.term_freqs[doc_id]
        for term in query_tokens:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (f * (self.k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_tokens:
            term_tf = tf.get(term, 0) / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += term_tf * idf
        return score * self.documents[doc_id].weight

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], maxlen: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = content[:maxlen] + ("..." if len(content) > maxlen else "")
            return snippet
        start = max(positions[0] - 8, 0)
        end = min(positions[0] + 12, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        if len(snippet) > maxlen:
            snippet = snippet[:maxlen] + "..."
        return snippet

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

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "SN2 Nucleophilic Substitution",
            "The SN2 reaction is a bimolecular nucleophilic substitution where the nucleophile attacks the electrophilic carbon, displacing the leaving group in a single concerted step. It is favored by primary substrates and strong nucleophiles.",
            ["SN2_Nucleophilic_Substitution", "Mechanism", "Kinetics"],
            1.0
        ),
        SearchDocument(
            2,
            "SN1 Nucleophilic Substitution",
            "The SN1 reaction proceeds via a two-step mechanism involving carbocation formation followed by nucleophilic attack. It is favored by tertiary substrates and polar protic solvents.",
            ["SN1_Nucleophilic_Substitution", "Mechanism", "Carbocation"],
            1.0
        ),
        SearchDocument(
            3,
            "E2 Elimination Reaction",
            "E2 elimination is a concerted process where a base abstracts a proton while the leaving group departs, forming a double bond. It is stereospecific and often competes with SN2 reactions.",
            ["E2_Elimination", "Mechanism", "Base"],
            1.0
        ),
        SearchDocument(
            4,
            "Grignard Reagent Chemistry",
            "Grignard reagents are organomagnesium compounds that react with carbonyls to form alcohols. They are highly nucleophilic and sensitive to moisture.",
            ["Grignard_Reagent_Chemistry", "Organometallic", "Alcohol_Synthesis"],
            1.0
        ),
        SearchDocument(
            5,
            "Wittig Reaction",
            "The Wittig reaction converts aldehydes or ketones into alkenes using phosphonium ylides. It is a key method for carbon-carbon double bond formation.",
            ["Wittig_Reaction", "Alkene_Synthesis", "Ylide"],
            1.0
        ),
        SearchDocument(
            6,
            "Diels-Alder Reaction",
            "The Diels-Alder reaction is a [4+2] cycloaddition between a conjugated diene and a dienophile, forming six-membered rings with high stereoselectivity.",
            ["Diels_Alder_Reaction", "Cycloaddition", "Pericyclic"],
            1.0
        ),
        SearchDocument(
            7,
            "Aldol Condensation",
            "Aldol condensation involves the formation of a β-hydroxy carbonyl compound from two carbonyl precursors, followed by dehydration to yield an α,β-unsaturated carbonyl.",
            ["Aldol_Condensation", "Carbonyl_Chemistry", "Enolate"],
            1.0
        ),
        SearchDocument(
            8,
            "Protecting Groups Strategy",
            "Protecting groups are used to temporarily mask reactive functional groups during multi-step synthesis, allowing selective reactions to occur elsewhere in the molecule.",
            ["Protecting_Groups_Strategy", "Synthesis", "Functional_Groups"],
            1.0
        ),
        SearchDocument(
            9,
            "Oxidation Reactions of Alcohols",
            "Alcohols can be oxidized to aldehydes, ketones, or carboxylic acids using reagents such as PCC, Jones reagent, or KMnO4. Selectivity depends on the substrate and conditions.",
            ["Oxidation_Reactions_Alcohols", "Alcohol", "Reagents"],
            1.0
        ),
        SearchDocument(
            10,
            "Reduction Reactions of Carbonyls",
            "Carbonyl compounds can be reduced to alcohols using hydride donors like NaBH4 and LiAlH4. Selectivity and reactivity depend on the carbonyl type.",
            ["Reduction_Reactions_Carbonyls", "Hydride", "Alcohol_Synthesis"],
            1.0
        ),
        SearchDocument(
            11,
            "Electrophilic Aromatic Substitution",
            "Aromatic rings undergo electrophilic substitution reactions such as nitration, sulfonation, halogenation, and Friedel-Crafts alkylation/acylation.",
            ["Electrophilic_Aromatic_Substitution", "Aromatic", "Mechanism"],
            1.0
        ),
        SearchDocument(
            12,
            "Nucleophilic Aromatic Substitution",
            "Nucleophilic aromatic substitution occurs on electron-deficient aromatic rings, often requiring strong electron-withdrawing groups ortho or para to the leaving group.",
            ["Nucleophilic_Aromatic_Substitution", "Aromatic", "Mechanism"],
            1.0
        ),
        SearchDocument(
            13,
            "Stereochemistry and Chirality",
            "Stereochemistry involves the study of spatial arrangement of atoms. Chirality refers to molecules that are non-superimposable on their mirror images, often leading to optical activity.",
            ["Stereochemistry_Chirality", "Isomerism", "Optical_Activity"],
            1.0
        ),
        SearchDocument(
            14,
            "Retrosynthetic Analysis",
            "Retrosynthetic analysis is a problem-solving technique for transforming a target molecule into simpler precursors by breaking bonds in a logical sequence.",
            ["Retrosynthetic_Analysis", "Synthesis", "Strategy"],
            1.0
        ),
        SearchDocument(
            15,
            "NMR Spectroscopy",
            "NMR spectroscopy provides information about the number and environment of hydrogen and carbon atoms in a molecule, aiding in structural elucidation.",
            ["NMR_Spectroscopy", "Spectroscopy", "Structure_Elucidation"],
            1.0
        ),
        SearchDocument(
            16,
            "IR Spectroscopy",
            "IR spectroscopy identifies functional groups by measuring vibrational transitions, with characteristic absorption bands for bonds such as C=O, O-H, and N-H.",
            ["IR_Spectroscopy", "Spectroscopy", "Functional_Groups"],
            1.0
        ),
        SearchDocument(
            17,
            "Mass Spectrometry",
            "Mass spectrometry determines the molecular weight and structure of compounds by ionizing molecules and analyzing the mass-to-charge ratio of the fragments.",
            ["Mass_Spectrometry", "Spectroscopy", "Structure_Elucidation"],
            1.0
        ),
        SearchDocument(
            18,
            "Radical Reactions",
            "Radical reactions involve species with unpaired electrons and include processes such as halogenation of alkanes and polymerization.",
            ["Radical_Reactions", "Mechanism", "Polymerization"],
            1.0
        ),
        SearchDocument(
            19,
            "Pericyclic Reactions",
            "Pericyclic reactions are concerted processes involving cyclic transition states, such as electrocyclic reactions, cycloadditions, and sigmatropic rearrangements.",
            ["Pericyclic_Reactions", "Mechanism", "Transition_State"],
            1.0
        ),
        SearchDocument(
            20,
            "Green Chemistry Principles",
            "Green chemistry emphasizes the design of chemical processes that reduce or eliminate hazardous substances, focusing on sustainability and environmental impact.",
            ["Green_Chemistry_Principles", "Sustainability", "Safety"],
            1.0
        ),
        SearchDocument(
            21,
            "Polymer Chemistry Fundamentals",
            "Polymer chemistry studies the synthesis and properties of macromolecules formed by the repetitive linking of monomers, including addition and condensation polymers.",
            ["Polymer_Chemistry_Fundamentals", "Macromolecules", "Monomers"],
            1.0
        ),
        SearchDocument(
            22,
            "Carbohydrate Chemistry",
            "Carbohydrate chemistry explores the structure, reactivity, and synthesis of sugars and polysaccharides, including glycosidic bond formation and stereochemistry.",
            ["Carbohydrate_Chemistry", "Sugars", "Glycosidic_Bond"],
            1.0
        ),
        SearchDocument(
            23,
            "Amino Acid and Peptide Chemistry",
            "Amino acids are the building blocks of peptides and proteins. Peptide synthesis involves coupling amino acids with protection and deprotection strategies.",
            ["Amino_Acid_Peptide_Chemistry", "Peptide_Synthesis", "Protection"],
            1.0
        ),
        SearchDocument(
            24,
            "Lipid Chemistry",
            "Lipid chemistry covers the structure and reactivity of fats, oils, and related molecules, including saponification and lipid biosynthesis.",
            ["Lipid_Chemistry", "Fats", "Saponification"],
            1.0
        ),
        SearchDocument(
            25,
            "Organometallic Cross Coupling",
            "Organometallic cross coupling reactions, such as Suzuki and Heck, form carbon-carbon bonds using metal catalysts like palladium.",
            ["Organometallic_Cross_Coupling", "Catalysis", "C-C_Bond_Formation"],
            1.0
        ),
        SearchDocument(
            26,
            "Safety and Handling of Organic Reagents",
            "Proper safety protocols must be followed when handling organic reagents, including the use of PPE, fume hoods, and safe disposal practices.",
            ["Safety_Handling_Organic_Reagents", "Safety", "Lab_Practices"],
            1.0
        ),
        SearchDocument(
            27,
            "Factors Affecting SN2 Reactions",
            "Steric hindrance, nucleophile strength, and solvent polarity all affect the rate and outcome of SN2 nucleophilic substitution reactions.",
            ["SN2_Nucleophilic_Substitution", "Sterics", "Solvent_Effects"],
            1.0
        ),
        SearchDocument(
            28,
            "Carbocation Rearrangements in SN1",
            "Carbocation intermediates in SN1 reactions may undergo rearrangements such as hydride or alkyl shifts, leading to unexpected products.",
            ["SN1_Nucleophilic_Substitution", "Carbocation", "Rearrangement"],
            1.0
        ),
        SearchDocument(
            29,
            "E2 vs E1 Elimination",
            "E2 is a concerted elimination, while E1 involves carbocation intermediates. Substrate structure and base strength determine the preferred pathway.",
            ["E2_Elimination", "E1_Elimination", "Mechanism"],
            1.0
        ),
        SearchDocument(
            30,
            "Applications of Grignard Reagents",
            "Grignard reagents are used to synthesize alcohols, carboxylic acids, and other functional groups by reacting with various electrophiles.",
            ["Grignard_Reagent_Chemistry", "Applications", "Synthesis"],
            1.0
        ),
        SearchDocument(
            31,
            "Protecting Groups for Alcohols",
            "Common protecting groups for alcohols include silyl ethers (TBDMS, TMS) and esters. They are stable under many conditions and can be removed selectively.",
            ["Protecting_Groups_Strategy", "Alcohol", "Silyl_Ether"],
            1.0
        ),
        SearchDocument(
            32,
            "Interpretation of NMR Spectra",
            "NMR spectra are interpreted by analyzing chemical shifts, coupling constants, and integration to deduce molecular structure.",
            ["NMR_Spectroscopy", "Interpretation", "Structure_Elucidation"],
            1.0
        ),
        SearchDocument(
            33,
            "Green Chemistry in Synthesis",
            "Green chemistry approaches in organic synthesis include solvent selection, atom economy, and the use of renewable feedstocks.",
            ["Green_Chemistry_Principles", "Synthesis", "Atom_Economy"],
            1.0
        ),
        SearchDocument(
            34,
            "Stereoselectivity in Diels-Alder Reaction",
            "The Diels-Alder reaction exhibits endo/exo selectivity, influenced by substituents on the diene and dienophile.",
            ["Diels_Alder_Reaction", "Stereochemistry", "Selectivity"],
            1.0
        ),
        SearchDocument(
            35,
            "Mass Spectrometry Fragmentation Patterns",
            "Fragmentation patterns in mass spectrometry help identify functional groups and molecular structure.",
            ["Mass_Spectrometry", "Fragmentation", "Structure_Elucidation"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)