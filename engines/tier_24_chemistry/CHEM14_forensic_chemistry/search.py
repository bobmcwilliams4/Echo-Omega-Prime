import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_map: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.tf_cache: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._preseed_documents()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                self.term_doc_freq[token] += 1
                self.term_doc_map[token][doc.id] = count
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self.idf_cache.clear()
            self.tf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores = defaultdict(float)
        snippets = {}
        for token in query_tokens:
            idf = self._compute_idf(token)
            for doc_id, tf in self.term_doc_map.get(token, {}).items():
                doc = self.documents[doc_id]
                score = self._score_bm25(token, doc_id, idf)
                scores[doc_id] += score * doc.weight
                if doc_id not in snippets:
                    snippets[doc_id] = self._make_snippet(doc.content, query_tokens)
        results = []
        for doc_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]:
            doc = self.documents[doc_id]
            results.append(SearchResult(doc_id, score, doc.title, snippets[doc_id]))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
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

    def _score_bm25(self, term: str, doc_id: str, idf: float, k1: float = 1.5, b: float = 0.75) -> float:
        tf = self.term_doc_map.get(term, {}).get(doc_id, 0)
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * doc_length / avg_dl)
        return idf * numerator / denominator if denominator != 0 else 0.0

    def _make_snippet(self, content: str, query_tokens: List[str], length: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if positions:
            start = max(positions[0] - length // 2, 0)
            end = min(start + length, len(tokens))
            snippet = ' '.join(tokens[start:end])
            return snippet
        else:
            return ' '.join(tokens[:length])

    def tfidf_score(self, query: str, doc_id: str) -> float:
        query_tokens = self._tokenize(query)
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        if doc_length == 0:
            return 0.0
        for token in query_tokens:
            tf = self.term_doc_map.get(token, {}).get(doc_id, 0) / doc_length
            idf = self._compute_idf(token)
            score += tf * idf
        return score

    def _preseed_documents(self):
        docs = [
            SearchDocument(
                "1",
                "Presumptive Color Tests for Controlled Substances",
                "Presumptive color tests are rapid screening methods used to indicate the possible presence of controlled substances. Common tests include Marquis, Scott, and Duquenois-Levine. These tests rely on characteristic color changes when reagents react with specific drug classes.",
                ["color test", "presumptive", "controlled substances", "screening"],
                1.0
            ),
            SearchDocument(
                "2",
                "GC-MS Confirmatory Analysis for Controlled Substances",
                "Gas Chromatography-Mass Spectrometry (GC-MS) is the gold standard for confirmatory analysis of controlled substances. It provides both separation and identification based on mass spectra, allowing for precise compound determination.",
                ["GC-MS", "confirmatory", "controlled substances", "analysis"],
                1.0
            ),
            SearchDocument(
                "3",
                "Trace Fiber Evidence Comparison and Analysis",
                "Trace fiber evidence is compared using microscopy, FTIR, and microspectrophotometry. Fiber morphology, color, and chemical composition are evaluated to link fibers to potential sources.",
                ["fiber", "trace evidence", "comparison", "microscopy"],
                1.0
            ),
            SearchDocument(
                "4",
                "Ignitable Liquid Residue Analysis for Arson Investigation",
                "Ignitable liquid residue analysis involves sampling fire debris and analyzing it via GC-MS or GC-FID. Patterns are compared to known ignitable liquids to determine the presence of accelerants.",
                ["arson", "ignitable liquid", "residue", "GC-MS", "accelerant"],
                1.0
            ),
            SearchDocument(
                "5",
                "Forensic Toxicology Immunoassay Screening and Confirmatory Testing",
                "Immunoassay screening is used for rapid detection of drugs in biological samples. Confirmatory testing is performed using LC-MS/MS or GC-MS to ensure specificity and accuracy.",
                ["toxicology", "immunoassay", "screening", "confirmatory", "LC-MS/MS"],
                1.0
            ),
            SearchDocument(
                "6",
                "Gunshot Residue Analysis by SEM-EDS",
                "Gunshot residue (GSR) analysis by Scanning Electron Microscopy with Energy Dispersive X-ray Spectroscopy (SEM-EDS) identifies characteristic particles containing lead, antimony, and barium.",
                ["gunshot residue", "SEM-EDS", "forensic", "analysis"],
                1.0
            ),
            SearchDocument(
                "7",
                "Chain of Custody Protocols for Forensic Evidence",
                "Chain of custody protocols ensure the integrity and traceability of forensic evidence from collection to courtroom. Documentation and secure storage are critical for admissibility.",
                ["chain of custody", "protocols", "forensic evidence", "integrity"],
                1.0
            ),
            SearchDocument(
                "8",
                "DNA Profiling by STR Analysis and CODIS Database Searching",
                "DNA profiling uses Short Tandem Repeat (STR) analysis to generate genetic profiles. Profiles are compared and searched in the CODIS database to identify suspects or link cases.",
                ["DNA profiling", "STR", "CODIS", "database", "genetic"],
                1.0
            ),
            SearchDocument(
                "9",
                "Fingerprint Chemistry: Cyanoacrylate Fuming and Ninhydrin Development",
                "Fingerprint chemistry involves cyanoacrylate fuming for latent print visualization and ninhydrin development for amino acid detection on porous surfaces.",
                ["fingerprint", "cyanoacrylate", "ninhydrin", "development", "chemistry"],
                1.0
            ),
            SearchDocument(
                "10",
                "ISO 17025 Laboratory Accreditation and Quality Management",
                "ISO 17025 accreditation ensures laboratory competence and quality management. It covers technical requirements, documentation, and proficiency testing.",
                ["ISO 17025", "accreditation", "quality management", "laboratory"],
                1.0
            ),
            SearchDocument(
                "11",
                "Daubert Standard for Expert Testimony Admissibility",
                "The Daubert standard governs the admissibility of expert testimony in court, focusing on scientific validity, peer review, error rates, and acceptance in the scientific community.",
                ["Daubert", "expert testimony", "admissibility", "court"],
                1.0
            ),
            SearchDocument(
                "12",
                "Paint Evidence Analysis and Comparison",
                "Paint evidence is analyzed using microscopy, FTIR, and Py-GC-MS. Layer structure, color, and chemical composition are compared to link paint samples to sources.",
                ["paint", "evidence", "analysis", "comparison", "microscopy"],
                1.0
            ),
            SearchDocument(
                "13",
                "Glass Refractive Index Determination and Comparison",
                "Glass evidence is compared by measuring refractive index using immersion methods or automated systems. Statistical analysis is used to assess the significance of matches.",
                ["glass", "refractive index", "comparison", "evidence"],
                1.0
            ),
            SearchDocument(
                "14",
                "Questioned Document Examination and Ink Analysis",
                "Questioned document examination includes handwriting analysis, ink comparison, and detection of alterations using chromatography and spectroscopy.",
                ["questioned document", "ink", "examination", "chromatography"],
                1.0
            ),
            SearchDocument(
                "15",
                "Explosives Residue Analysis and Identification",
                "Explosives residue is analyzed using GC-MS, LC-MS/MS, and ion chromatography. Identification relies on characteristic ions and comparison to reference materials.",
                ["explosives", "residue", "analysis", "identification", "GC-MS"],
                1.0
            ),
            SearchDocument(
                "16",
                "Forensic Quality Assurance and Proficiency Testing Programs",
                "Quality assurance in forensic laboratories includes proficiency testing, internal audits, and corrective actions to ensure reliability and accuracy.",
                ["quality assurance", "proficiency testing", "forensic", "laboratory"],
                1.0
            ),
            SearchDocument(
                "17",
                "Microspectrophotometry in Fiber and Paint Analysis",
                "Microspectrophotometry provides objective color measurement for fiber and paint evidence, aiding in comparison and discrimination of samples.",
                ["microspectrophotometry", "fiber", "paint", "analysis"],
                1.0
            ),
            SearchDocument(
                "18",
                "FTIR Spectroscopy for Forensic Evidence",
                "FTIR spectroscopy is used to identify organic and inorganic compounds in forensic evidence, including drugs, fibers, and paints.",
                ["FTIR", "spectroscopy", "forensic", "evidence"],
                1.0
            ),
            SearchDocument(
                "19",
                "LC-MS/MS in Forensic Toxicology",
                "Liquid Chromatography-Tandem Mass Spectrometry (LC-MS/MS) is used for confirmatory testing of drugs and poisons in biological samples.",
                ["LC-MS/MS", "toxicology", "confirmatory", "drugs"],
                1.0
            ),
            SearchDocument(
                "20",
                "Pyrolysis GC-MS for Paint and Polymer Analysis",
                "Pyrolysis GC-MS breaks down polymers and paints for analysis, providing chemical fingerprints for comparison and identification.",
                ["Py-GC-MS", "paint", "polymer", "analysis"],
                1.0
            ),
            SearchDocument(
                "21",
                "Forensic Fiber Comparison Using Polarized Light Microscopy",
                "Polarized light microscopy is used to differentiate fiber types and assess optical properties, supporting forensic fiber comparison.",
                ["fiber", "polarized light microscopy", "comparison"],
                1.0
            ),
            SearchDocument(
                "22",
                "Automated Glass Refractive Index Measurement Systems",
                "Automated systems provide rapid and precise refractive index measurements for glass evidence, improving comparison accuracy.",
                ["glass", "automated", "refractive index", "measurement"],
                1.0
            ),
            SearchDocument(
                "23",
                "Handwriting Analysis in Questioned Document Examination",
                "Handwriting analysis evaluates letter formation, slant, and spacing to determine authorship in questioned documents.",
                ["handwriting", "questioned document", "analysis"],
                1.0
            ),
            SearchDocument(
                "24",
                "Ion Chromatography for Explosives Residue Analysis",
                "Ion chromatography separates and identifies anions and cations in explosives residue, supporting forensic identification.",
                ["ion chromatography", "explosives", "residue", "analysis"],
                1.0
            ),
            SearchDocument(
                "25",
                "Forensic Laboratory Internal Audits and Corrective Actions",
                "Internal audits and corrective actions are essential components of forensic laboratory quality assurance, ensuring compliance and reliability.",
                ["internal audit", "corrective action", "forensic", "quality assurance"],
                1.0
            ),
            SearchDocument(
                "26",
                "CODIS Database Matching and DNA Profile Interpretation",
                "CODIS database matching compares DNA profiles across cases, aiding in suspect identification and case linkage.",
                ["CODIS", "DNA profile", "database", "interpretation"],
                1.0
            ),
            SearchDocument(
                "27",
                "Accelerant Detection in Arson Investigation",
                "Accelerant detection relies on chemical analysis of fire debris, using GC-MS and pattern recognition to identify ignitable liquids.",
                ["accelerant", "arson", "GC-MS", "detection"],
                1.0
            ),
            SearchDocument(
                "28",
                "Ninhydrin Reaction Mechanism in Fingerprint Development",
                "Ninhydrin reacts with amino acids in fingerprint residues, producing a purple color for latent print visualization.",
                ["ninhydrin", "fingerprint", "reaction", "development"],
                1.0
            ),
            SearchDocument(
                "29",
                "Daubert Criteria for Scientific Evidence",
                "Daubert criteria include testability, peer review, known error rates, and general acceptance, guiding admissibility of scientific evidence.",
                ["Daubert", "criteria", "scientific evidence", "admissibility"],
                1.0
            ),
            SearchDocument(
                "30",
                "Proficiency Testing in ISO 17025 Accredited Laboratories",
                "Proficiency testing evaluates laboratory performance and supports ISO 17025 accreditation, ensuring consistent quality.",
                ["proficiency testing", "ISO 17025", "laboratory", "quality"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
        return _search_index_instance