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
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.avg_doc_len: float = 0.0
        self.total_doc_len: int = 0
        self.N: int = 0
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                self._remove_document(doc.id)
            tokens = self._tokenize(doc.content)
            term_freqs = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_term_freqs[doc.id] = term_freqs
            for term in term_freqs.keys():
                self.term_doc_freqs[term] += 1
            doc_len = sum(term_freqs.values())
            self.total_doc_len += doc_len
            self.N += 1
            self.avg_doc_len = self.total_doc_len / self.N if self.N > 0 else 0.0

    def _remove_document(self, doc_id: str):
        old_term_freqs = self.doc_term_freqs.get(doc_id)
        if not old_term_freqs:
            return
        for term in old_term_freqs.keys():
            self.term_doc_freqs[term] -= 1
            if self.term_doc_freqs[term] <= 0:
                del self.term_doc_freqs[term]
        doc_len = sum(old_term_freqs.values())
        self.total_doc_len -= doc_len
        self.N -= 1
        self.avg_doc_len = self.total_doc_len / self.N if self.N > 0 else 0.0
        del self.doc_term_freqs[doc_id]
        del self.documents[doc_id]

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        idf = self._compute_idf(query_terms)
        scores: Dict[str, float] = defaultdict(float)
        for term in query_terms:
            if term not in self.term_doc_freqs:
                continue
            for doc_id, term_freqs in self.doc_term_freqs.items():
                tf = term_freqs.get(term, 0)
                if tf == 0:
                    continue
                score = self._score_bm25(tf, idf[term], sum(term_freqs.values()))
                scores[doc_id] += score
        # Adjust scores by document weight
        for doc_id in scores.keys():
            scores[doc_id] *= self.documents[doc_id].weight
        # Sort by score descending
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
                "average_document_length": self.avg_doc_len,
                "unique_terms": len(self.term_doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, terms: List[str]) -> Dict[str, float]:
        idf = {}
        for term in terms:
            df = self.term_doc_freqs.get(term, 0)
            if df == 0:
                idf[term] = 0.0
            else:
                idf[term] = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        return idf

    def _score_bm25(self, tf: int, idf: float, doc_len: int) -> float:
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len if self.avg_doc_len > 0 else 1))
        return idf * (numerator / denominator)

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            pos = content_lower.find(term)
            if pos >= 0:
                positions.append(pos)
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += "..."
            return snippet
        start = max(min(positions) - snippet_len // 4, 0)
        end = start + snippet_len
        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet += "..."
        return snippet


_singleton_instance: Optional[SearchIndex] = None
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
            doc_id="BL01",
            title="Beer-Lambert Law Application",
            content=(
                "The Beer-Lambert Law relates the absorption of light to the properties of the material through "
                "which the light is traveling. It is fundamental for quantitative spectroscopy and concentration "
                "determination. Deviations occur due to chemical equilibria, stray light, and high concentrations."
            ),
            tags=["Beer-Lambert Law", "Absorption", "Spectroscopy", "Quantitative Analysis"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="BL02",
            title="Deviations from Beer-Lambert Law",
            content=(
                "Common deviations from the Beer-Lambert Law include chemical deviations caused by association or "
                "dissociation of absorbing species, instrumental deviations such as stray light, and photochemical "
                "reactions during measurement."
            ),
            tags=["Beer-Lambert Law", "Deviations", "Spectroscopy"],
        ),
        SearchDocument(
            doc_id="CF01",
            title="Chromophore Identification",
            content=(
                "Chromophores are parts of molecules responsible for their color by absorbing visible or UV light. "
                "Identification involves analyzing absorption maxima and intensities."
            ),
            tags=["Chromophore", "UV-Vis", "Spectroscopy"],
        ),
        SearchDocument(
            doc_id="WF01",
            title="Woodward-Fieser Rules",
            content=(
                "Woodward-Fieser rules provide empirical guidelines to predict the absorption maxima of conjugated "
                "dienes and carbonyl compounds based on substituent effects and conjugation length."
            ),
            tags=["Woodward-Fieser", "UV-Vis", "Chromophores"],
        ),
        SearchDocument(
            doc_id="FG01",
            title="Functional Group Identification by IR Spectroscopy",
            content=(
                "Infrared spectroscopy allows identification of functional groups by their characteristic absorption "
                "bands due to molecular vibrations."
            ),
            tags=["IR Spectroscopy", "Functional Groups", "Vibrational Spectroscopy"],
        ),
        SearchDocument(
            doc_id="NMR01",
            title="1H NMR Chemical Shift Interpretation",
            content=(
                "Proton NMR chemical shifts provide information about the electronic environment of hydrogens, "
                "helping to elucidate molecular structure."
            ),
            tags=["1H NMR", "Chemical Shift", "Spectroscopy"],
        ),
        SearchDocument(
            doc_id="NMR02",
            title="Spin-Spin Coupling in 1H NMR",
            content=(
                "Spin-spin coupling splits NMR signals into multiplets, revealing connectivity and neighboring proton "
                "environments."
            ),
            tags=["1H NMR", "Spin-Spin Coupling", "Spectroscopy"],
        ),
        SearchDocument(
            doc_id="NMR13C01",
            title="13C NMR Spectroscopy",
            content=(
                "Carbon-13 NMR provides structural information by detecting signals from carbon atoms, with chemical "
                "shifts influenced by hybridization and substituents."
            ),
            tags=["13C NMR", "Spectroscopy"],
        ),
        SearchDocument(
            doc_id="DEPT01",
            title="DEPT Experiments in 13C NMR",
            content=(
                "Distortionless Enhancement by Polarization Transfer (DEPT) experiments differentiate CH, CH2, and CH3 "
                "groups in 13C NMR spectra."
            ),
            tags=["DEPT", "13C NMR", "Spectroscopy"],
        ),
        SearchDocument(
            doc_id="MS01",
            title="Electron Ionization Mass Spectrometry",
            content=(
                "Electron Ionization (EI) MS ionizes molecules by electron impact, causing fragmentation patterns useful "
                "for structural elucidation."
            ),
            tags=["Mass Spectrometry", "Electron Ionization", "Fragmentation"],
        ),
        SearchDocument(
            doc_id="MS02",
            title="Fragmentation Patterns in EI-MS",
            content=(
                "Characteristic fragmentation patterns in EI-MS help identify molecular structure and functional groups."
            ),
            tags=["Mass Spectrometry", "Fragmentation", "EI-MS"],
        ),
        SearchDocument(
            doc_id="MS03",
            title="Electrospray Ionization and Soft Ionization Techniques",
            content=(
                "Electrospray Ionization (ESI) is a soft ionization technique that produces intact molecular ions, "
                "allowing analysis of large biomolecules."
            ),
            tags=["Mass Spectrometry", "ESI", "Soft Ionization"],
        ),
        SearchDocument(
            doc_id="RAMAN01",
            title="Raman Spectroscopy Principles",
            content=(
                "Raman spectroscopy measures inelastic scattering of light, providing vibrational information complementary "
                "to IR spectroscopy."
            ),
            tags=["Raman Spectroscopy", "Vibrational Spectroscopy"],
        ),
        SearchDocument(
            doc_id="SERS01",
            title="Surface-Enhanced Raman Scattering (SERS)",
            content=(
                "SERS enhances Raman signals using metal nanostructures, enabling sensitive detection of molecules at low "
                "concentrations."
            ),
            tags=["SERS", "Raman Spectroscopy", "Nanotechnology"],
        ),
        SearchDocument(
            doc_id="XRF01",
            title="X-ray Fluorescence (XRF) for Elemental Analysis",
            content=(
                "XRF spectroscopy detects elemental composition by measuring characteristic X-ray emissions from a sample."
            ),
            tags=["XRF", "Elemental Analysis", "Spectroscopy"],
        ),
        SearchDocument(
            doc_id="AAS01",
            title="Atomic Absorption Spectroscopy (AAS)",
            content=(
                "AAS quantifies trace metals by measuring absorption of light by free atoms in the gaseous state."
            ),
            tags=["AAS", "Trace Metals", "Spectroscopy"],
        ),
        SearchDocument(
            doc_id="ICP01",
            title="ICP-OES for Trace Metal Analysis",
            content=(
                "Inductively Coupled Plasma Optical Emission Spectroscopy (ICP-OES) detects trace metals via emission spectra "
                "from plasma-excited atoms."
            ),
            tags=["ICP-OES", "Trace Metals", "Spectroscopy"],
        ),
        SearchDocument(
            doc_id="VAL01",
            title="Analytical Method Validation for Spectroscopic Techniques",
            content=(
                "Validation ensures accuracy, precision, sensitivity, and specificity of spectroscopic analytical methods."
            ),
            tags=["Validation", "Spectroscopy", "Analytical Chemistry"],
        ),
        SearchDocument(
            doc_id="GCMS01",
            title="Hyphenated Technique: GC-MS",
            content=(
                "Gas Chromatography-Mass Spectrometry (GC-MS) combines separation and mass analysis for complex mixture "
                "identification."
            ),
            tags=["GC-MS", "Hyphenated Techniques", "Mass Spectrometry"],
        ),
        SearchDocument(
            doc_id="LCMS01",
            title="Hyphenated Technique: LC-MS",
            content=(
                "Liquid Chromatography-Mass Spectrometry (LC-MS) couples liquid separation with mass spectrometry for "
                "analyzing non-volatile compounds."
            ),
            tags=["LC-MS", "Hyphenated Techniques", "Mass Spectrometry"],
        ),
        SearchDocument(
            doc_id="FLUOR01",
            title="Fluorescence Spectroscopy for Sensitive Detection",
            content=(
                "Fluorescence spectroscopy detects molecules based on their emission of light after excitation, offering "
                "high sensitivity."
            ),
            tags=["Fluorescence", "Spectroscopy", "Sensitive Detection"],
        ),
        SearchDocument(
            doc_id="ATRFTIR01",
            title="ATR-FTIR Sampling and Qualitative Analysis",
            content=(
                "Attenuated Total Reflectance Fourier Transform Infrared (ATR-FTIR) spectroscopy enables surface sampling "
                "and qualitative analysis of solids and liquids."
            ),
            tags=["ATR-FTIR", "IR Spectroscopy", "Qualitative Analysis"],
        ),
        SearchDocument(
            doc_id="BL03",
            title="Quantitative Analysis Using Beer-Lambert Law",
            content=(
                "Quantitative analysis by Beer-Lambert Law requires calibration curves and careful control of experimental "
                "conditions to avoid deviations."
            ),
            tags=["Beer-Lambert Law", "Quantitative Analysis"],
        ),
        SearchDocument(
            doc_id="NMR03",
            title="Factors Affecting 1H NMR Chemical Shifts",
            content=(
                "Electronegativity, hybridization, and hydrogen bonding influence 1H NMR chemical shifts and peak positions."
            ),
            tags=["1H NMR", "Chemical Shift"],
        ),
        SearchDocument(
            doc_id="MS04",
            title="Soft Ionization Techniques Overview",
            content=(
                "Soft ionization techniques like ESI and MALDI preserve molecular ions, facilitating analysis of fragile molecules."
            ),
            tags=["Mass Spectrometry", "Soft Ionization"],
        ),
        SearchDocument(
            doc_id="RAMAN02",
            title="Applications of Raman Spectroscopy",
            content=(
                "Raman spectroscopy is used in material science, pharmaceuticals, and biological systems for molecular characterization."
            ),
            tags=["Raman Spectroscopy", "Applications"],
        ),
        SearchDocument(
            doc_id="XRF02",
            title="Quantitative Elemental Analysis by XRF",
            content=(
                "Quantitative XRF requires standards and matrix corrections to accurately determine elemental concentrations."
            ),
            tags=["XRF", "Elemental Analysis", "Quantitative"],
        ),
        SearchDocument(
            doc_id="AAS02",
            title="Limitations of Atomic Absorption Spectroscopy",
            content=(
                "AAS is limited by interference effects, detection limits, and the need for atomization sources."
            ),
            tags=["AAS", "Limitations"],
        ),
        SearchDocument(
            doc_id="VAL02",
            title="Parameters in Analytical Method Validation",
            content=(
                "Key validation parameters include accuracy, precision, linearity, limit of detection, limit of quantification, "
                "and robustness."
            ),
            tags=["Validation", "Analytical Chemistry"],
        ),
    ]
    for doc in docs:
        index.add_document(doc)