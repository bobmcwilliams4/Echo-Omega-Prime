import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional


class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old doc stats
                old_tf = self.doc_term_freqs[doc.id]
                for term in old_tf:
                    self.term_doc_freqs[term] -= 1
                    if self.term_doc_freqs[term] <= 0:
                        del self.term_doc_freqs[term]
                del self.doc_term_freqs[doc.id]
                del self.doc_lengths[doc.id]
                del self.documents[doc.id]
                self.N -= 1

            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.doc_term_freqs[doc.id] = tf
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = sum(tf.values())
            self.N += 1

            for term in tf.keys():
                self.term_doc_freqs[term] += 1

            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        if not tokens:
            return []

        scores: Dict[str, float] = defaultdict(float)
        idf_values = {term: self._compute_idf(term) for term in tokens}

        for doc_id, tf in self.doc_term_freqs.items():
            score = 0.0
            doc_len = self.doc_lengths[doc_id]
            doc_weight = self.documents[doc_id].weight
            for term in tokens:
                if term not in tf:
                    continue
                freq = tf[term]
                idf = idf_values.get(term, 0.0)
                score += self._score_bm25(freq, idf, doc_len)
            if score > 0:
                scores[doc_id] = score * doc_weight

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, tokens)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.N,
                "average_document_length": self.avg_doc_length,
                "unique_terms": len(self.term_doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, freq: int, idf: float, doc_len: int) -> float:
        denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length) if self.avg_doc_length > 0 else freq + self.k1
        score = idf * (freq * (self.k1 + 1)) / denom if denom > 0 else 0.0
        return score

    def _make_snippet(self, content: str, terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + 1
        if not positions:
            snippet = content[:snippet_len] + ("..." if len(content) > snippet_len else "")
            return snippet.strip()

        start_pos = max(min(positions) - snippet_len // 4, 0)
        end_pos = start_pos + snippet_len
        snippet = content[start_pos:end_pos]
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet = snippet + "..."
        return snippet.strip()


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _seed_index(_singleton_instance)
        return _singleton_instance


def _seed_index(index: SearchIndex):
    docs = [
        SearchDocument(
            id="GCF001",
            title="Gas Chromatography Fundamentals",
            content=(
                "Gas Chromatography (GC) is an analytical technique used to separate and analyze compounds "
                "that can be vaporized without decomposition. It involves a mobile gas phase and a stationary liquid or solid phase."
            ),
            tags=["gas chromatography", "separation", "analytical chemistry"],
            weight=1.2,
        ),
        SearchDocument(
            id="GCF002",
            title="Retention Time and Factors Affecting Gas Chromatography",
            content=(
                "Retention time in GC is the time taken for a compound to travel through the column to the detector. "
                "It depends on the interaction between the compound and stationary phase, temperature, and carrier gas flow rate."
            ),
            tags=["retention time", "gas chromatography", "factors"],
        ),
        SearchDocument(
            id="HPLC001",
            title="High Performance Liquid Chromatography Principles",
            content=(
                "HPLC is a technique in analytical chemistry used to separate, identify, and quantify components in a mixture. "
                "It uses high pressure to push solvents through a column filled with a stationary phase."
            ),
            tags=["HPLC", "liquid chromatography", "separation"],
            weight=1.1,
        ),
        SearchDocument(
            id="HPLC002",
            title="Types of HPLC Columns and Stationary Phases",
            content=(
                "Common HPLC columns include reversed-phase, normal phase, ion-exchange, and size exclusion. "
                "Selection depends on the chemical nature of analytes and separation goals."
            ),
            tags=["HPLC", "columns", "stationary phase"],
        ),
        SearchDocument(
            id="MSP001",
            title="Mass Spectrometry Principles",
            content=(
                "Mass spectrometry (MS) is an analytical technique that measures the mass-to-charge ratio of ions. "
                "It is used to determine molecular weight and structure of compounds."
            ),
            tags=["mass spectrometry", "ionization", "mass analyzer"],
            weight=1.3,
        ),
        SearchDocument(
            id="MSP002",
            title="Ionization Techniques in Mass Spectrometry",
            content=(
                "Common ionization methods include Electron Ionization (EI), Electrospray Ionization (ESI), and Matrix-Assisted Laser Desorption Ionization (MALDI)."
            ),
            tags=["mass spectrometry", "ionization", "EI", "ESI", "MALDI"],
        ),
        SearchDocument(
            id="UVV001",
            title="UV-Visible Spectroscopy Basics",
            content=(
                "UV-Visible spectroscopy measures absorption of ultraviolet or visible light by molecules, "
                "providing information about electronic transitions."
            ),
            tags=["UV-Vis", "spectroscopy", "absorption"],
        ),
        SearchDocument(
            id="IRP001",
            title="Infrared Spectroscopy Principles",
            content=(
                "Infrared (IR) spectroscopy identifies functional groups by measuring molecular vibrations "
                "absorbing infrared light at characteristic frequencies."
            ),
            tags=["infrared spectroscopy", "functional groups", "vibrations"],
            weight=1.0,
        ),
        SearchDocument(
            id="NMR001",
            title="Nuclear Magnetic Resonance Spectroscopy Fundamentals",
            content=(
                "NMR spectroscopy exploits magnetic properties of atomic nuclei to determine molecular structure and dynamics."
            ),
            tags=["NMR", "magnetic resonance", "structure determination"],
            weight=1.4,
        ),
        SearchDocument(
            id="PHM001",
            title="Potentiometry and pH Measurement",
            content=(
                "Potentiometry measures the voltage of an electrochemical cell to determine analyte concentration, "
                "commonly used for pH measurement with glass electrodes."
            ),
            tags=["potentiometry", "pH", "electrochemical"],
        ),
        SearchDocument(
            id="VOL001",
            title="Voltammetry and Electrochemical Detection",
            content=(
                "Voltammetry involves measuring current as a function of applied voltage to analyze redox-active species."
            ),
            tags=["voltammetry", "electrochemical detection", "redox"],
        ),
        SearchDocument(
            id="ABT001",
            title="Acid-Base Titration Techniques",
            content=(
                "Acid-base titration determines concentration of an acid or base by neutralization with a titrant of known concentration."
            ),
            tags=["acid-base titration", "neutralization", "analytical chemistry"],
        ),
        SearchDocument(
            id="RCT001",
            title="Redox and Complexometric Titration",
            content=(
                "Redox titrations involve electron transfer reactions, while complexometric titrations use complex formation for endpoint detection."
            ),
            tags=["redox titration", "complexometric titration", "endpoint"],
        ),
        SearchDocument(
            id="GRA001",
            title="Gravimetric Analysis Principles",
            content=(
                "Gravimetric analysis quantifies analytes by measuring mass of a solid precipitate formed in a chemical reaction."
            ),
            tags=["gravimetric analysis", "precipitation", "quantification"],
        ),
        SearchDocument(
            id="MVP001",
            title="Method Validation Parameters",
            content=(
                "Validation parameters include accuracy, precision, specificity, limit of detection, limit of quantitation, linearity, and robustness."
            ),
            tags=["method validation", "accuracy", "precision", "LOD", "LOQ"],
            weight=1.2,
        ),
        SearchDocument(
            id="QCS001",
            title="Quality Control and Statistical Analysis",
            content=(
                "Quality control ensures analytical results meet required standards using control charts, replicate analysis, and statistical tests."
            ),
            tags=["quality control", "statistics", "control charts"],
        ),
        SearchDocument(
            id="GLP001",
            title="Good Laboratory Practices and Compliance",
            content=(
                "GLP guidelines ensure reliability, reproducibility, and traceability of laboratory data and operations."
            ),
            tags=["GLP", "compliance", "laboratory standards"],
        ),
        SearchDocument(
            id="CMS001",
            title="Calibration Methods and Standards",
            content=(
                "Calibration involves establishing relationship between instrument response and known standards to ensure accurate measurements."
            ),
            tags=["calibration", "standards", "instrumentation"],
        ),
        SearchDocument(
            id="AAS001",
            title="Atomic Absorption Spectroscopy",
            content=(
                "AAS measures concentration of elements by absorption of light by free atoms in gaseous state."
            ),
            tags=["atomic absorption spectroscopy", "AAS", "elemental analysis"],
        ),
        SearchDocument(
            id="ICP001",
            title="Inductively Coupled Plasma Spectroscopy",
            content=(
                "ICP spectroscopy uses plasma source to excite atoms and ions for elemental analysis with high sensitivity."
            ),
            tags=["ICP", "plasma spectroscopy", "elemental analysis"],
            weight=1.3,
        ),
        SearchDocument(
            id="SAM001",
            title="Sampling Theory and Representative Sampling",
            content=(
                "Proper sampling ensures collected samples accurately represent the whole batch or environment."
            ),
            tags=["sampling theory", "representative sampling", "analytical chemistry"],
        ),
        SearchDocument(
            id="SPE001",
            title="Sample Preparation and Extraction Techniques",
            content=(
                "Sample preparation includes filtration, extraction, concentration, and cleanup to improve analysis accuracy."
            ),
            tags=["sample preparation", "extraction", "cleanup"],
        ),
        SearchDocument(
            id="ENV001",
            title="Environmental Analysis Methods",
            content=(
                "Techniques for detecting pollutants and contaminants in air, water, and soil to assess environmental quality."
            ),
            tags=["environmental analysis", "pollutants", "contaminants"],
        ),
        SearchDocument(
            id="PHA001",
            title="Pharmaceutical and Clinical Analysis",
            content=(
                "Analytical methods for drug development, quality control, and clinical diagnostics."
            ),
            tags=["pharmaceutical analysis", "clinical analysis", "drug quality"],
            weight=1.2,
        ),
        SearchDocument(
            id="FOO001",
            title="Food and Agricultural Analysis",
            content=(
                "Methods to detect contaminants, nutrients, and residues in food and agricultural products."
            ),
            tags=["food analysis", "agricultural analysis", "contaminants"],
        ),
        SearchDocument(
            id="FOR001",
            title="Forensic Chemistry and Toxicology",
            content=(
                "Application of analytical chemistry to legal investigations, including drug testing and poison detection."
            ),
            tags=["forensic chemistry", "toxicology", "legal analysis"],
            weight=1.3,
        ),
    ]

    for doc in docs:
        index.add_document(doc)