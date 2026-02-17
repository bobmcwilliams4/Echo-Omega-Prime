import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional, Tuple

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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[Tuple[int, str], float] = {}
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = dict(tf)
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()
            self.tf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores: Dict[int, float] = defaultdict(float)
        for term in set(query_terms):
            idf = self._compute_idf(term)
            for doc_id, tf_dict in self.term_freqs.items():
                if term in tf_dict:
                    score = self._score_bm25(doc_id, term, idf)
                    doc_scores[doc_id] += score
        # TF-IDF scoring (normalized)
        tfidf_scores: Dict[int, float] = defaultdict(float)
        for term in set(query_terms):
            idf = self._compute_idf(term)
            for doc_id, tf_dict in self.term_freqs.items():
                tf = tf_dict.get(term, 0)
                norm_tf = tf / self.doc_lengths[doc_id] if self.doc_lengths[doc_id] else 0.0
                tfidf_scores[doc_id] += norm_tf * idf
        # Combine BM25 and TF-IDF (weighted average)
        combined_scores: List[Tuple[float, int]] = []
        for doc_id in doc_scores:
            bm25 = doc_scores[doc_id]
            tfidf = tfidf_scores[doc_id]
            doc = self.documents[doc_id]
            combined = 0.7 * bm25 + 0.3 * tfidf
            combined *= doc.weight
            combined_scores.append((combined, doc_id))
        top_docs = heapq.nlargest(limit, combined_scores)
        results = []
        for score, doc_id in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5)) if df else 0.0
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, term: str, idf: float) -> float:
        key = (doc_id, term)
        if key in self.tf_cache:
            return self.tf_cache[key]
        tf = self.term_freqs[doc_id].get(term, 0)
        dl = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        denom = tf + self.k1 * (1 - self.b + self.b * dl / avg_dl)
        score = idf * ((tf * (self.k1 + 1)) / denom) if denom != 0 else 0.0
        self.tf_cache[key] = score
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        # Highlight query terms
        for term in set(query_terms):
            snippet = re.sub(rf'\b({re.escape(term)})\b', r'*\1*', snippet, flags=re.IGNORECASE)
        return snippet + ('...' if end < len(tokens) else '')

_index_instance: Optional[SearchIndex] = None
_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _index_instance
    with _index_lock:
        if _index_instance is None:
            _index_instance = SearchIndex()
            _preseed_documents(_index_instance)
        return _index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id=1,
            title="Protein Primary Structure",
            content="The primary structure of a protein is its unique sequence of amino acids. This sequence determines the protein's properties and function.",
            tags=["protein_primary_structure", "amino_acids"],
            weight=1.0
        ),
        SearchDocument(
            id=2,
            title="Protein Secondary Structure: Alpha Helix and Beta Sheet",
            content="Secondary structure refers to local folded structures that form within a polypeptide due to hydrogen bonding. The most common are alpha helices and beta sheets.",
            tags=["protein_secondary_structure", "alpha_helix", "beta_sheet"],
            weight=1.0
        ),
        SearchDocument(
            id=3,
            title="Protein Tertiary Structure",
            content="Tertiary structure describes the overall 3D shape of a single polypeptide chain, stabilized by interactions such as disulfide bonds, hydrophobic interactions, and ionic bonds.",
            tags=["protein_tertiary_structure", "disulfide_bonds"],
            weight=1.0
        ),
        SearchDocument(
            id=4,
            title="Protein Quaternary Structure",
            content="Quaternary structure is the arrangement of multiple polypeptide subunits in a protein complex. Hemoglobin is a classic example.",
            tags=["protein_quaternary_structure", "hemoglobin"],
            weight=1.0
        ),
        SearchDocument(
            id=5,
            title="Enzyme Kinetics: Michaelis-Menten Equation",
            content="The Michaelis-Menten equation describes the rate of enzymatic reactions. It relates reaction rate to substrate concentration, enzyme concentration, Km, and Vmax.",
            tags=["enzyme_kinetics_michaelis_menten", "km", "vmax"],
            weight=1.0
        ),
        SearchDocument(
            id=6,
            title="Enzyme Inhibition Types",
            content="Enzyme inhibition can be competitive, noncompetitive, or uncompetitive. Each type affects Km and Vmax differently.",
            tags=["enzyme_inhibition", "competitive_inhibition", "noncompetitive_inhibition"],
            weight=1.0
        ),
        SearchDocument(
            id=7,
            title="Allosteric Regulation of Enzymes",
            content="Allosteric regulation involves effectors binding to sites other than the active site, causing conformational changes that alter enzyme activity.",
            tags=["allosteric_regulation", "enzyme_regulation"],
            weight=1.0
        ),
        SearchDocument(
            id=8,
            title="Glycolysis Pathway Overview",
            content="Glycolysis is the metabolic pathway that converts glucose into pyruvate, generating ATP and NADH. It occurs in the cytoplasm.",
            tags=["glycolysis", "glucose_metabolism"],
            weight=1.0
        ),
        SearchDocument(
            id=9,
            title="Tricarboxylic Acid (TCA) Cycle",
            content="The TCA cycle, also known as the Krebs cycle, oxidizes acetyl-CoA to CO2 and generates NADH, FADH2, and GTP.",
            tags=["tca_cycle", "krebs_cycle"],
            weight=1.0
        ),
        SearchDocument(
            id=10,
            title="Oxidative Phosphorylation and Electron Transport Chain",
            content="Oxidative phosphorylation uses the electron transport chain to generate ATP from NADH and FADH2. Oxygen is the final electron acceptor.",
            tags=["oxidative_phosphorylation", "electron_transport_chain"],
            weight=1.0
        ),
        SearchDocument(
            id=11,
            title="Gluconeogenesis: Synthesis of Glucose",
            content="Gluconeogenesis is the process of synthesizing glucose from non-carbohydrate precursors such as lactate, glycerol, and amino acids.",
            tags=["gluconeogenesis", "glucose_synthesis"],
            weight=1.0
        ),
        SearchDocument(
            id=12,
            title="Fatty Acid Oxidation (Beta-Oxidation)",
            content="Fatty acid oxidation breaks down fatty acids into acetyl-CoA units, producing NADH and FADH2. This occurs in the mitochondria.",
            tags=["fatty_acid_oxidation", "beta_oxidation"],
            weight=1.0
        ),
        SearchDocument(
            id=13,
            title="Fatty Acid Synthesis",
            content="Fatty acid synthesis is the creation of fatty acids from acetyl-CoA and malonyl-CoA, primarily in the cytoplasm of liver cells.",
            tags=["fatty_acid_synthesis", "lipogenesis"],
            weight=1.0
        ),
        SearchDocument(
            id=14,
            title="Amino Acid Metabolism",
            content="Amino acid metabolism includes transamination, deamination, and the urea cycle. It is essential for nitrogen balance.",
            tags=["amino_acid_metabolism", "urea_cycle"],
            weight=1.0
        ),
        SearchDocument(
            id=15,
            title="Purine Metabolism and Disorders",
            content="Purine metabolism involves the synthesis and breakdown of purines. Disorders include gout and Lesch-Nyhan syndrome.",
            tags=["purine_metabolism", "gout", "lesch_nyhan"],
            weight=1.0
        ),
        SearchDocument(
            id=16,
            title="Pyrimidine Metabolism",
            content="Pyrimidine metabolism is responsible for the synthesis and degradation of cytosine, thymine, and uracil.",
            tags=["pyrimidine_metabolism", "nucleotide_metabolism"],
            weight=1.0
        ),
        SearchDocument(
            id=17,
            title="DNA Replication Mechanism",
            content="DNA replication is a semiconservative process involving DNA polymerase, helicase, primase, and ligase.",
            tags=["dna_replication", "dna_polymerase"],
            weight=1.0
        ),
        SearchDocument(
            id=18,
            title="DNA Repair Systems",
            content="DNA repair mechanisms include base excision repair, nucleotide excision repair, and mismatch repair.",
            tags=["dna_repair", "base_excision_repair", "nucleotide_excision_repair"],
            weight=1.0
        ),
        SearchDocument(
            id=19,
            title="Transcription: DNA to RNA",
            content="Transcription is the synthesis of RNA from a DNA template by RNA polymerase. Promoters and enhancers regulate transcription.",
            tags=["transcription", "rna_polymerase"],
            weight=1.0
        ),
        SearchDocument(
            id=20,
            title="RNA Processing",
            content="RNA processing includes capping, polyadenylation, and splicing to produce mature mRNA.",
            tags=["rna_processing", "splicing"],
            weight=1.0
        ),
        SearchDocument(
            id=21,
            title="Translation: Protein Synthesis",
            content="Translation is the process of synthesizing proteins from mRNA using ribosomes, tRNA, and amino acids.",
            tags=["translation", "protein_synthesis"],
            weight=1.0
        ),
        SearchDocument(
            id=22,
            title="GPCR Signal Transduction",
            content="G protein-coupled receptors (GPCRs) transmit signals via G proteins, activating second messengers like cAMP.",
            tags=["signal_transduction_gpcr", "g_protein"],
            weight=1.0
        ),
        SearchDocument(
            id=23,
            title="Receptor Tyrosine Kinase (RTK) Signaling",
            content="RTKs are membrane receptors that, upon ligand binding, activate intracellular signaling cascades via phosphorylation.",
            tags=["signal_transduction_rtk", "receptor_tyrosine_kinase"],
            weight=1.0
        ),
        SearchDocument(
            id=24,
            title="Membrane Transport Mechanisms",
            content="Membrane transport includes passive diffusion, facilitated diffusion, active transport, and endocytosis.",
            tags=["membrane_transport", "active_transport"],
            weight=1.0
        ),
        SearchDocument(
            id=25,
            title="Vitamins and Coenzymes in Metabolism",
            content="Vitamins often serve as coenzymes or precursors for coenzymes in metabolic reactions. Examples include NAD+, FAD, and CoA.",
            tags=["vitamins_coenzymes", "coenzyme"],
            weight=1.0
        ),
        SearchDocument(
            id=26,
            title="Clinical Biochemistry: Diagnostic Markers",
            content="Clinical biochemistry uses biomarkers such as ALT, AST, creatinine, and troponin to diagnose diseases.",
            tags=["clinical_biochemistry", "biomarkers"],
            weight=1.0
        ),
        SearchDocument(
            id=27,
            title="Hemoglobin Structure and Function",
            content="Hemoglobin is a tetrameric protein responsible for oxygen transport in blood. It exhibits cooperative binding.",
            tags=["protein_quaternary_structure", "hemoglobin", "oxygen_transport"],
            weight=1.0
        ),
        SearchDocument(
            id=28,
            title="Lactate Dehydrogenase in Glycolysis",
            content="Lactate dehydrogenase catalyzes the conversion of pyruvate to lactate during anaerobic glycolysis.",
            tags=["glycolysis", "lactate_dehydrogenase"],
            weight=1.0
        ),
        SearchDocument(
            id=29,
            title="Mitochondrial Electron Transport Chain Complexes",
            content="The electron transport chain consists of complexes I-IV, cytochrome c, and ATP synthase, embedded in the inner mitochondrial membrane.",
            tags=["oxidative_phosphorylation", "electron_transport_chain", "mitochondria"],
            weight=1.0
        ),
        SearchDocument(
            id=30,
            title="Regulation of Gluconeogenesis",
            content="Gluconeogenesis is regulated by allosteric effectors, substrate availability, and hormonal control (insulin, glucagon).",
            tags=["gluconeogenesis", "regulation"],
            weight=1.0
        ),
        SearchDocument(
            id=31,
            title="Beta-Oxidation of Fatty Acids: Steps and Enzymes",
            content="Beta-oxidation involves the sequential removal of two-carbon units from fatty acids, producing acetyl-CoA, NADH, and FADH2.",
            tags=["fatty_acid_oxidation", "beta_oxidation"],
            weight=1.0
        ),
        SearchDocument(
            id=32,
            title="Urea Cycle: Removal of Ammonia",
            content="The urea cycle converts toxic ammonia to urea for excretion. Key enzymes include carbamoyl phosphate synthetase I and ornithine transcarbamylase.",
            tags=["amino_acid_metabolism", "urea_cycle"],
            weight=1.0
        ),
        SearchDocument(
            id=33,
            title="DNA Polymerase: Proofreading Activity",
            content="DNA polymerase has 3' to 5' exonuclease activity for proofreading and correcting errors during DNA replication.",
            tags=["dna_replication", "dna_polymerase", "proofreading"],
            weight=1.0
        ),
        SearchDocument(
            id=34,
            title="Mismatch Repair in DNA",
            content="Mismatch repair corrects errors that escape proofreading during DNA replication, reducing mutation rates.",
            tags=["dna_repair", "mismatch_repair"],
            weight=1.0
        ),
        SearchDocument(
            id=35,
            title="Alternative Splicing in RNA Processing",
            content="Alternative splicing allows a single gene to code for multiple proteins by including or excluding certain exons.",
            tags=["rna_processing", "alternative_splicing"],
            weight=1.0
        ),
        SearchDocument(
            id=36,
            title="Initiation of Translation in Eukaryotes",
            content="Translation initiation in eukaryotes involves the small ribosomal subunit, initiation factors, and the recognition of the start codon.",
            tags=["translation", "initiation"],
            weight=1.0
        ),
        SearchDocument(
            id=37,
            title="GPCRs and Second Messenger Systems",
            content="GPCR activation leads to the production of second messengers like cAMP, IP3, and DAG, amplifying cellular responses.",
            tags=["signal_transduction_gpcr", "second_messenger"],
            weight=1.0
        ),
        SearchDocument(
            id=38,
            title="RTK Dimerization and Autophosphorylation",
            content="RTK activation involves ligand-induced dimerization and autophosphorylation, triggering downstream signaling.",
            tags=["signal_transduction_rtk", "autophosphorylation"],
            weight=1.0
        ),
        SearchDocument(
            id=39,
            title="Facilitated Diffusion and Glucose Transporters",
            content="Facilitated diffusion uses transport proteins such as GLUTs to move glucose across membranes down its concentration gradient.",
            tags=["membrane_transport", "facilitated_diffusion", "glut"],
            weight=1.0
        ),
        SearchDocument(
            id=40,
            title="Vitamin B12 as a Coenzyme",
            content="Vitamin B12 acts as a coenzyme in the conversion of homocysteine to methionine and in fatty acid metabolism.",
            tags=["vitamins_coenzymes", "vitamin_b12"],
            weight=1.0
        ),
        SearchDocument(
            id=41,
            title="Clinical Biochemistry: Liver Function Tests",
            content="Liver function tests include measurements of ALT, AST, ALP, and bilirubin to assess hepatic health.",
            tags=["clinical_biochemistry", "liver_function"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)