import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

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
        self.inverted_index: Dict[str, set] = defaultdict(set)
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in re.findall(r"\b\w+\b", text)]

    def add_document(self, doc: SearchDocument):
        with self.lock:
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.N = len(self.documents)
            self.avg_doc_length = sum(self.doc_lengths.values()) / max(1, self.N)
            self._idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * (freq * (self.k1 + 1)) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf_norm = tf[term] / doc_len if doc_len else 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scored: List[Tuple[float, int]] = []
        for doc_id in candidate_docs:
            if use_bm25:
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0:
                scored.append((score, doc_id))
        scored.sort(reverse=True)
        results = []
        for score, doc_id in scored[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:snippet_len] + ("..." if len(content) > snippet_len else "")
        start = max(positions[0] - 10, 0)
        end = min(start + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(rf"\b({re.escape(term)})\b", r"**\1**", snippet, flags=re.IGNORECASE)
        return snippet[:snippet_len] + ("..." if len(snippet) > snippet_len else "")

    def get_stats(self) -> Dict[str, float]:
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avg_doc_length,
            "vocab_size": len(self.doc_freqs)
        }

# Singleton factory
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
            "Anionic Friction Reducers in Slickwater Fracs",
            "Anionic polyacrylamide friction reducers are widely used in slickwater hydraulic fracturing. They provide efficient drag reduction in low-salinity water but may be sensitive to high hardness and divalent cations.",
            ["anionic", "friction reducer", "slickwater", "polyacrylamide"],
            1.0
        ),
        SearchDocument(
            2,
            "Cationic Friction Reducers for High-Hardness Brines",
            "Cationic friction reducers are designed for high-TDS and high-hardness brines, maintaining performance in the presence of calcium and magnesium ions where anionic FRs fail.",
            ["cationic", "friction reducer", "high-hardness", "brine"],
            1.0
        ),
        SearchDocument(
            3,
            "Borate-Crosslinked Guar Gel Systems",
            "Borate crosslinkers react with guar polymers to form a three-dimensional gel network, providing high viscosity for proppant transport in hydraulic fracturing fluids.",
            ["borate", "crosslinker", "guar", "gel", "viscosity"],
            1.0
        ),
        SearchDocument(
            4,
            "Zirconate and Titanate Crosslinkers for High-Temp Gels",
            "Zirconate and titanate crosslinkers are used to create stable gels at elevated temperatures, extending the operational window for guar-based fracturing fluids.",
            ["zirconate", "titanate", "crosslinker", "high-temperature", "gel"],
            1.0
        ),
        SearchDocument(
            5,
            "Hybrid Frac Design: Slickwater and Gel Stages",
            "Hybrid fracturing combines slickwater and gel stages to optimize proppant placement and minimize fluid costs, leveraging the benefits of both fluid types.",
            ["hybrid", "frac design", "slickwater", "gel", "proppant"],
            1.0
        ),
        SearchDocument(
            6,
            "Viscoelastic Surfactant (VES) Fluids",
            "VES fluids use surfactant micelles to generate viscosity without polymers, offering clean fluid recovery and minimal residue in the formation.",
            ["viscoelastic", "surfactant", "ves", "fluid", "micelle"],
            1.0
        ),
        SearchDocument(
            7,
            "Enzyme Breakers for Guar-Based Fluids",
            "Enzyme breakers selectively degrade guar polymers after fracturing, reducing viscosity and facilitating flowback while minimizing formation damage.",
            ["enzyme", "breaker", "guar", "viscosity", "flowback"],
            1.0
        ),
        SearchDocument(
            8,
            "Oxidizer Breakers: Persulfate and Peroxide Systems",
            "Oxidizer breakers like ammonium persulfate and hydrogen peroxide are used to break down polymer gels, with activation controlled by temperature or encapsulation.",
            ["oxidizer", "breaker", "persulfate", "peroxide", "polymer"],
            1.0
        ),
        SearchDocument(
            9,
            "Biocide Selection: Glutaraldehyde vs THPS vs Chlorine Dioxide",
            "Choosing the right biocide depends on water quality, microbial load, and compatibility. Glutaraldehyde, THPS, and chlorine dioxide each have unique efficacy and safety profiles.",
            ["biocide", "glutaraldehyde", "thps", "chlorine dioxide", "microbial"],
            1.0
        ),
        SearchDocument(
            10,
            "Scale Inhibitors: Phosphonate vs Polycarboxylate",
            "Phosphonate and polycarboxylate scale inhibitors prevent mineral scaling in frac fluids. Selection depends on water chemistry, temperature, and compatibility with other additives.",
            ["scale inhibitor", "phosphonate", "polycarboxylate", "scaling"],
            1.0
        ),
        SearchDocument(
            11,
            "Clay Stabilizers: KCl vs TMAC vs Choline Chloride",
            "Clay stabilizers prevent swelling and migration of formation clays. KCl, TMAC, and choline chloride are commonly used, each with specific advantages and limitations.",
            ["clay stabilizer", "kcl", "tmac", "choline chloride", "formation"],
            1.0
        ),
        SearchDocument(
            12,
            "Iron Control: Chelating Agents and Reducing Agents",
            "Iron control additives prevent precipitation and scaling by chelating iron or reducing ferric to ferrous states, maintaining fluid clarity and performance.",
            ["iron control", "chelating agent", "reducing agent", "scaling"],
            1.0
        ),
        SearchDocument(
            13,
            "Acid Frac Design: HCl Concentration and Retardation",
            "Acid fracturing fluids use hydrochloric acid with retarders to optimize etching and minimize near-wellbore damage. Acid concentration and additives are tailored to reservoir conditions.",
            ["acid frac", "hcl", "retarder", "etching", "reservoir"],
            1.0
        ),
        SearchDocument(
            14,
            "Fluid Compatibility Testing: Jar Testing and Filtration",
            "Compatibility testing ensures frac fluid additives do not precipitate or form gels when mixed. Jar testing and filtration are standard procedures.",
            ["compatibility", "jar test", "filtration", "precipitation"],
            1.0
        ),
        SearchDocument(
            15,
            "Friction Reducer Performance Testing: Loop Rheometer",
            "Loop rheometers measure friction reduction under dynamic flow, providing quantitative data for friction reducer selection and optimization.",
            ["friction reducer", "performance", "loop rheometer", "testing"],
            1.0
        ),
        SearchDocument(
            16,
            "Proppant Transport: Slickwater vs Gel",
            "Gel fluids provide higher viscosity for proppant transport, while slickwater relies on high flow rates and turbulence. Hybrid designs balance both approaches.",
            ["proppant", "transport", "slickwater", "gel", "hybrid"],
            1.0
        ),
        SearchDocument(
            17,
            "Produced Water Recycling for Frac Fluid",
            "Recycling produced water for fracturing fluids reduces freshwater demand but requires careful treatment to manage TDS, hardness, and bacteria.",
            ["produced water", "recycling", "frac fluid", "treatment"],
            1.0
        ),
        SearchDocument(
            18,
            "Water Quality Requirements: TDS, Hardness, Iron, Bacteria",
            "Frac fluid performance depends on water quality parameters including total dissolved solids (TDS), hardness, iron content, and microbial contamination.",
            ["water quality", "tds", "hardness", "iron", "bacteria"],
            1.0
        ),
        SearchDocument(
            19,
            "FracFocus Chemical Disclosure Requirements",
            "FracFocus is a public registry for hydraulic fracturing chemical disclosures, requiring operators to report fluid additives and concentrations.",
            ["fracfocus", "chemical disclosure", "regulation", "additive"],
            1.0
        ),
        SearchDocument(
            20,
            "Fluid Viscosity at Temperature and Shear",
            "Frac fluid viscosity is affected by temperature and shear rate. Rheological testing ensures fluids maintain performance under downhole conditions.",
            ["viscosity", "temperature", "shear", "rheology"],
            1.0
        ),
        SearchDocument(
            21,
            "Nonionic Friction Reducers: Broad Salinity Tolerance",
            "Nonionic friction reducers offer broad tolerance to salinity and hardness, making them suitable for diverse water sources in hydraulic fracturing.",
            ["nonionic", "friction reducer", "salinity", "hardness"],
            1.0
        ),
        SearchDocument(
            22,
            "Linear Gel Systems: Non-Crosslinked Guar",
            "Linear gel systems use non-crosslinked guar for moderate viscosity, balancing proppant transport and fluid cleanup.",
            ["linear gel", "guar", "non-crosslinked", "viscosity"],
            1.0
        ),
        SearchDocument(
            23,
            "Encapsulated Breakers: Delayed Activation Systems",
            "Encapsulated breakers provide delayed gel breaking, allowing for controlled viscosity reduction and improved proppant placement.",
            ["encapsulated breaker", "delayed activation", "viscosity", "proppant"],
            1.0
        ),
        SearchDocument(
            24,
            "Polyacrylamide Chemistry in Friction Reduction",
            "Polyacrylamide is the primary polymer used in friction reducers, with molecular weight and charge density affecting performance and compatibility.",
            ["polyacrylamide", "friction reducer", "chemistry", "compatibility"],
            1.0
        ),
        SearchDocument(
            25,
            "Guar Derivatives: Hydroxypropyl Guar and Carboxymethyl Guar",
            "Guar derivatives such as hydroxypropyl guar (HPG) and carboxymethyl guar (CMG) offer improved hydration and viscosity control in fracturing fluids.",
            ["guar", "hydroxypropyl guar", "carboxymethyl guar", "derivative"],
            1.0
        ),
        SearchDocument(
            26,
            "Chelating Agents: EDTA and DTPA in Iron Control",
            "EDTA and DTPA are chelating agents used to sequester iron, preventing precipitation and scaling in frac fluids.",
            ["chelating agent", "edta", "dtpa", "iron control"],
            1.0
        ),
        SearchDocument(
            27,
            "Enzyme Breaker Activation: Temperature and pH Effects",
            "Enzyme breaker activity is influenced by temperature and pH, requiring careful selection for optimal gel breaking in downhole environments.",
            ["enzyme breaker", "activation", "temperature", "ph"],
            1.0
        ),
        SearchDocument(
            28,
            "Oxidizer Breaker Encapsulation for Delayed Release",
            "Encapsulated oxidizer breakers enable delayed gel breaking, improving proppant placement and reducing premature viscosity loss.",
            ["oxidizer breaker", "encapsulation", "delayed release"],
            1.0
        ),
        SearchDocument(
            29,
            "Microbial Control: Biocide Dosing Strategies",
            "Effective microbial control in frac fluids requires appropriate biocide dosing, monitoring, and compatibility with other additives.",
            ["microbial control", "biocide", "dosing", "compatibility"],
            1.0
        ),
        SearchDocument(
            30,
            "Polycarboxylate Scale Inhibitor Mechanisms",
            "Polycarboxylate scale inhibitors prevent mineral precipitation by dispersing scale-forming ions, effective across a range of temperatures and water chemistries.",
            ["polycarboxylate", "scale inhibitor", "mechanism", "temperature"],
            1.0
        ),
        SearchDocument(
            31,
            "TMAC as a Clay Stabilizer: Advantages and Limitations",
            "Tetramethylammonium chloride (TMAC) is a quaternary ammonium salt used as a clay stabilizer, offering improved performance over KCl in some formations.",
            ["tmac", "clay stabilizer", "quaternary ammonium", "formation"],
            1.0
        ),
        SearchDocument(
            32,
            "Water Hardness Impact on Friction Reducer Performance",
            "High water hardness can reduce the effectiveness of anionic friction reducers, necessitating the use of cationic or nonionic alternatives.",
            ["water hardness", "friction reducer", "performance"],
            1.0
        ),
        SearchDocument(
            33,
            "Choline Chloride: Environmentally Friendly Clay Stabilizer",
            "Choline chloride is a biodegradable clay stabilizer, offering environmental benefits and effective clay control in hydraulic fracturing.",
            ["choline chloride", "clay stabilizer", "biodegradable"],
            1.0
        ),
        SearchDocument(
            34,
            "Retarded Acid Systems: Organic and Inorganic Retarders",
            "Retarded acid systems use organic or inorganic retarders to slow acid reaction rates, improving acid penetration and minimizing near-wellbore damage.",
            ["retarded acid", "organic retarder", "inorganic retarder"],
            1.0
        ),
        SearchDocument(
            35,
            "Jar Testing Protocols for Frac Fluid Compatibility",
            "Standard jar testing protocols assess fluid compatibility, precipitation risk, and filterability before field application.",
            ["jar testing", "protocol", "compatibility", "precipitation"],
            1.0
        ),
        SearchDocument(
            36,
            "Loop Rheometer Calibration and Data Interpretation",
            "Proper calibration and interpretation of loop rheometer data are essential for accurate friction reducer performance evaluation.",
            ["loop rheometer", "calibration", "data interpretation"],
            1.0
        ),
        SearchDocument(
            37,
            "Produced Water Treatment: Removing Iron and Bacteria",
            "Produced water treatment systems remove iron and bacteria to ensure compatibility with friction reducers and minimize scaling.",
            ["produced water", "treatment", "iron", "bacteria"],
            1.0
        ),
        SearchDocument(
            38,
            "TDS and Salinity Effects on Frac Fluid Chemistry",
            "Total dissolved solids (TDS) and salinity influence additive selection and performance in frac fluids, especially for friction reducers and scale inhibitors.",
            ["tds", "salinity", "frac fluid", "chemistry"],
            1.0
        ),
        SearchDocument(
            39,
            "Regulatory Trends in Frac Chemical Disclosure",
            "Evolving regulations require more detailed chemical disclosure, impacting additive selection and reporting for hydraulic fracturing operations.",
            ["regulation", "chemical disclosure", "frac", "additive"],
            1.0
        ),
        SearchDocument(
            40,
            "Rheological Testing: Viscosity Measurement Methods",
            "Rheological testing methods, including rotational and oscillatory rheometry, are used to characterize frac fluid viscosity under various conditions.",
            ["rheology", "viscosity", "measurement", "testing"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)