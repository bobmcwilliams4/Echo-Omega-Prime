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

# --- BM25 and TF-IDF Search Index ---

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self._re_token = re.compile(r"\b\w+\b", re.UNICODE)

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # skip duplicates
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            self.documents[doc.id] = doc
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores: Dict[int, float] = defaultdict(float)
        tfidf_scores: Dict[int, float] = defaultdict(float)
        doc_ids = set()
        for term in query_terms:
            if term in self.doc_freqs:
                doc_ids.update(doc_id for doc_id in self.term_freqs if term in self.term_freqs[doc_id])
        for doc_id in doc_ids:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            # Combine BM25 and TF-IDF (weighted sum)
            combined_score = 0.7 * bm25_score + 0.3 * tfidf_score
            scores[doc_id] = combined_score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "num_terms": len(self.doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._re_token.findall(text)]

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

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in set(query_terms):
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            numer = f * (self.k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in set(query_terms):
            term_tf = tf.get(term, 0)
            if term_tf == 0:
                continue
            tf_norm = term_tf / (doc_len or 1)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], maxlen: int = 160) -> str:
        text = doc.content
        tokens = self._tokenize(text)
        term_set = set(query_terms)
        positions = [i for i, t in enumerate(tokens) if t in term_set]
        if not positions:
            snippet = text[:maxlen]
        else:
            start = max(positions[0] - 5, 0)
            end = min(positions[0] + 15, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = " ".join(snippet_tokens)
            # Highlight terms
            for t in term_set:
                snippet = re.sub(rf'\b({re.escape(t)})\b', r'*\1*', snippet, flags=re.IGNORECASE)
        return snippet.strip()[:maxlen] + ("..." if len(snippet) > maxlen else "")

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

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            id=1,
            title="Alpha Decay: Mechanism and Energetics",
            content="Alpha decay is a nuclear process in which an unstable nucleus emits an alpha particle (helium-4 nucleus). The decay reduces the atomic number by two and the mass number by four. The process is governed by quantum tunneling through the Coulomb barrier. Alpha particles have discrete energies characteristic of the parent nucleus.",
            tags=["alpha decay", "nuclear decay", "radioactivity"],
            weight=1.0
        ),
        SearchDocument(
            id=2,
            title="Beta Minus Decay and Neutrino Emission",
            content="Beta minus decay occurs when a neutron in the nucleus transforms into a proton, emitting an electron (beta particle) and an antineutrino. The process conserves charge, lepton number, and energy. The energy spectrum of emitted electrons is continuous due to the sharing of energy with the antineutrino.",
            tags=["beta decay", "neutrino", "nuclear decay"],
            weight=1.0
        ),
        SearchDocument(
            id=3,
            title="Beta Plus Decay and Electron Capture",
            content="In beta plus decay, a proton is converted into a neutron, emitting a positron and a neutrino. Alternatively, electron capture involves the nucleus capturing an orbital electron, converting a proton into a neutron and emitting a neutrino. Both processes decrease the atomic number by one.",
            tags=["beta decay", "electron capture", "positron emission"],
            weight=1.0
        ),
        SearchDocument(
            id=4,
            title="Gamma Emission and Internal Conversion",
            content="Gamma emission is the de-excitation of a nucleus via photon emission, typically following alpha or beta decay. Internal conversion is a competing process where excess energy is transferred to an orbital electron, which is then ejected from the atom.",
            tags=["gamma emission", "internal conversion", "nuclear de-excitation"],
            weight=1.0
        ),
        SearchDocument(
            id=5,
            title="Radioactive Decay Kinetics and Half-Life",
            content="Radioactive decay follows first-order kinetics. The half-life is the time required for half the nuclei in a sample to decay. The decay constant relates to the half-life by λ = ln(2)/t½. Activity decreases exponentially with time.",
            tags=["decay kinetics", "half-life", "radioactivity"],
            weight=1.0
        ),
        SearchDocument(
            id=6,
            title="Secular and Transient Equilibrium in Decay Chains",
            content="In decay chains, secular equilibrium occurs when the parent half-life is much longer than the daughter. The activity of the daughter approaches that of the parent. Transient equilibrium occurs when the parent half-life is only moderately longer than the daughter's.",
            tags=["secular equilibrium", "transient equilibrium", "decay chains"],
            weight=1.0
        ),
        SearchDocument(
            id=7,
            title="Nuclear Fission: Mechanism and Energy Release",
            content="Nuclear fission is the splitting of a heavy nucleus (e.g., U-235) into lighter nuclei, accompanied by the release of neutrons and a large amount of energy. Fission can be spontaneous or induced by neutron absorption.",
            tags=["nuclear fission", "energy release", "neutron"],
            weight=1.0
        ),
        SearchDocument(
            id=8,
            title="Fission Product Yields and Chain Reactions",
            content="Fission produces a variety of neutron-rich fragments and releases additional neutrons, enabling chain reactions. The probability of sustaining a chain reaction depends on the neutron multiplication factor (k).",
            tags=["fission products", "chain reaction", "neutron multiplication"],
            weight=1.0
        ),
        SearchDocument(
            id=9,
            title="Nuclear Fusion and Stellar Nucleosynthesis",
            content="Nuclear fusion involves the combination of light nuclei to form heavier nuclei, releasing energy. In stars, fusion processes such as the proton-proton chain and CNO cycle are responsible for energy production and element synthesis.",
            tags=["nuclear fusion", "stellar nucleosynthesis", "energy production"],
            weight=1.0
        ),
        SearchDocument(
            id=10,
            title="Fusion Reactions: Lawson Criterion and Confinement",
            content="For fusion to be sustained, the Lawson criterion must be met, relating plasma density, temperature, and confinement time. Magnetic and inertial confinement are two main approaches to achieving fusion conditions on Earth.",
            tags=["fusion", "lawson criterion", "plasma confinement"],
            weight=1.0
        ),
        SearchDocument(
            id=11,
            title="Radiation Detection: Gas-Filled Detectors",
            content="Gas-filled detectors, such as ionization chambers, proportional counters, and Geiger-Müller tubes, detect radiation by collecting ion pairs produced in a gas. Their response varies with applied voltage.",
            tags=["radiation detection", "gas-filled detector", "ionization chamber"],
            weight=1.0
        ),
        SearchDocument(
            id=12,
            title="Scintillation Detectors and Photomultiplier Tubes",
            content="Scintillation detectors use materials that emit light when struck by radiation. The light is detected and amplified by photomultiplier tubes, allowing for sensitive measurement of radiation.",
            tags=["scintillation detector", "photomultiplier", "radiation measurement"],
            weight=1.0
        ),
        SearchDocument(
            id=13,
            title="Semiconductor Detectors: HPGe and Si(Li)",
            content="High-purity germanium (HPGe) and silicon-lithium [Si(Li)] detectors offer excellent energy resolution for gamma and X-ray spectroscopy. They operate by collecting electron-hole pairs created by incident radiation.",
            tags=["semiconductor detector", "HPGe", "Si(Li)", "gamma spectroscopy"],
            weight=1.0
        ),
        SearchDocument(
            id=14,
            title="Radiation Dosimetry: Absorbed and Equivalent Dose",
            content="Absorbed dose is the energy deposited per unit mass (gray, Gy). Equivalent dose accounts for radiation type using a quality factor (sievert, Sv). Dosimetry is essential for radiation protection.",
            tags=["dosimetry", "absorbed dose", "equivalent dose", "sievert"],
            weight=1.0
        ),
        SearchDocument(
            id=15,
            title="ALARA Principle and Radiation Protection",
            content="The ALARA (As Low As Reasonably Achievable) principle guides radiation protection practices. It emphasizes minimizing exposure by optimizing time, distance, and shielding.",
            tags=["ALARA", "radiation protection", "exposure minimization"],
            weight=1.0
        ),
        SearchDocument(
            id=16,
            title="Shielding Calculations: Attenuation and Buildup",
            content="Radiation shielding calculations involve determining the thickness of material needed to reduce exposure. The attenuation follows an exponential law, and buildup factors account for scattered radiation.",
            tags=["shielding", "attenuation", "buildup factor"],
            weight=1.0
        ),
        SearchDocument(
            id=17,
            title="Nuclear Waste: Classification and Management",
            content="Nuclear waste is classified as low, intermediate, or high level based on radioactivity. Management strategies include containment, storage, and disposal in engineered facilities.",
            tags=["nuclear waste", "waste management", "radioactivity"],
            weight=1.0
        ),
        SearchDocument(
            id=18,
            title="Neutron Activation Analysis (NAA)",
            content="NAA is a sensitive analytical technique that determines elemental composition by irradiating samples with neutrons and measuring induced radioactivity. It is non-destructive and highly precise.",
            tags=["neutron activation analysis", "NAA", "elemental analysis"],
            weight=1.0
        ),
        SearchDocument(
            id=19,
            title="PUREX Process for Spent Fuel Reprocessing",
            content="The PUREX (Plutonium Uranium Redox EXtraction) process separates uranium and plutonium from spent nuclear fuel using solvent extraction. It is the most widely used reprocessing method.",
            tags=["PUREX", "spent fuel", "reprocessing", "solvent extraction"],
            weight=1.0
        ),
        SearchDocument(
            id=20,
            title="NORM in Oil and Gas Operations",
            content="Naturally Occurring Radioactive Material (NORM) can accumulate in oil and gas equipment, posing radiological hazards. Management includes monitoring, decontamination, and regulatory compliance.",
            tags=["NORM", "oil and gas", "radioactive material"],
            weight=1.0
        ),
        SearchDocument(
            id=21,
            title="Radiation Effects on Materials: Displacement Damage",
            content="Radiation can displace atoms in solids, creating defects and degrading material properties. Displacement damage is significant in reactor components and semiconductor devices.",
            tags=["radiation effects", "displacement damage", "materials"],
            weight=1.0
        ),
        SearchDocument(
            id=22,
            title="Monte Carlo Methods in Radiation Transport",
            content="Monte Carlo simulations, such as those implemented in MCNP, model the stochastic transport of radiation through materials. They are essential for shielding design and dosimetry.",
            tags=["Monte Carlo", "MCNP", "radiation transport"],
            weight=1.0
        ),
        SearchDocument(
            id=23,
            title="MCNP: Features and Applications",
            content="MCNP (Monte Carlo N-Particle) is a general-purpose code for simulating neutron, photon, electron, and coupled transport. Applications include reactor design, shielding, and medical physics.",
            tags=["MCNP", "simulation", "neutron transport"],
            weight=1.0
        ),
        SearchDocument(
            id=24,
            title="Neutrino Physics in Beta Decay",
            content="Neutrinos are nearly massless, neutral particles emitted in beta decay. Their existence was postulated to conserve energy and momentum. Neutrino detection is challenging due to their weak interaction.",
            tags=["neutrino", "beta decay", "particle physics"],
            weight=1.0
        ),
        SearchDocument(
            id=25,
            title="Decay Schemes and Nuclear Level Diagrams",
            content="Decay schemes graphically represent the sequence of nuclear transitions, including energy levels, emitted particles, and gamma rays. They are essential for understanding nuclear decay processes.",
            tags=["decay scheme", "nuclear levels", "gamma ray"],
            weight=1.0
        ),
        SearchDocument(
            id=26,
            title="Radiation Units and Measurement Standards",
            content="Radiation is measured in units such as becquerel (Bq), gray (Gy), and sievert (Sv). International standards ensure consistency in measurement and reporting.",
            tags=["radiation units", "measurement", "standards"],
            weight=1.0
        ),
        SearchDocument(
            id=27,
            title="Criticality Safety in Fission Systems",
            content="Criticality safety ensures that fissionable material configurations remain subcritical. Control of mass, geometry, moderation, and reflection are key factors.",
            tags=["criticality", "fission", "safety"],
            weight=1.0
        ),
        SearchDocument(
            id=28,
            title="Decay Heat and Reactor Shutdown",
            content="After reactor shutdown, decay heat from fission products continues to generate thermal energy. Proper heat removal is essential to prevent overheating.",
            tags=["decay heat", "reactor", "shutdown"],
            weight=1.0
        ),
        SearchDocument(
            id=29,
            title="Spent Fuel Storage and Containment",
            content="Spent nuclear fuel is stored in pools or dry casks to allow radioactive decay and heat dissipation. Containment prevents release of radioactivity.",
            tags=["spent fuel", "storage", "containment"],
            weight=1.0
        ),
        SearchDocument(
            id=30,
            title="Radiation Buildup and Shielding Optimization",
            content="Buildup factors account for secondary radiation produced by scattering and reactions in shielding materials. Optimization balances protection and material cost.",
            tags=["buildup", "shielding", "optimization"],
            weight=1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)