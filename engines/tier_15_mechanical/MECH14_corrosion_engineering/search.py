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
        self.tags_index: Dict[str, set] = defaultdict(set)
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[int, str], float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.doc_freqs[term] += 1
            for tag in doc.tags:
                self.tags_index[tag.lower()].add(doc.id)
            self.documents[doc.id] = doc
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, tf in self.term_freqs.items():
                score = self._score_bm25(term, doc_id, idf)
                doc_scores[doc_id] += score
        # TF-IDF normalization
        for term in query_terms:
            for doc_id in self.documents.keys():
                tfidf = self._score_tfidf(term, doc_id)
                doc_scores[doc_id] += 0.25 * tfidf  # Blend in TF-IDF (tunable weight)
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self):
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avgdl,
            "num_terms": len(self.doc_freqs),
            "tags": list(self.tags_index.keys())
        }

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in re.findall(r'\b\w+\b', text)]

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: int, idf: Optional[float] = None) -> float:
        if idf is None:
            idf = self._compute_idf(term)
        tf = self.term_freqs[doc_id][term]
        dl = self.doc_lengths[doc_id]
        avgdl = self.avgdl if self.avgdl > 0 else 1
        doc = self.documents[doc_id]
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * dl / avgdl)
        score = idf * (numerator / denominator) * doc.weight
        return score

    def _score_tfidf(self, term: str, doc_id: int) -> float:
        key = (doc_id, term)
        if key in self._tfidf_cache:
            return self._tfidf_cache[key]
        tf = self.term_freqs[doc_id][term]
        if tf == 0:
            return 0.0
        max_tf = max(self.term_freqs[doc_id].values()) if self.term_freqs[doc_id] else 1
        tf_norm = tf / max_tf
        idf = self._compute_idf(term)
        score = tf_norm * idf * self.documents[doc_id].weight
        self._tfidf_cache[key] = score
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        for i, tok in enumerate(snippet_tokens):
            if tok in query_terms:
                snippet_tokens[i] = f'*{tok}*'
        return ' '.join(snippet_tokens) + ('...' if end < len(tokens) else '')

# Singleton factory for the search index
_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1, "Electrochemical Corrosion Fundamentals",
            "Electrochemical corrosion involves anodic metal dissolution and cathodic reduction reactions. The corrosion rate is governed by the mixed potential theory and polarization behavior.",
            ["fundamentals", "electrochemical", "corrosion"], 1.0
        ),
        SearchDocument(
            2, "Galvanic Corrosion between Dissimilar Metals",
            "Galvanic corrosion occurs when two dissimilar metals are electrically connected in an electrolyte. The more active metal corrodes preferentially. The galvanic series ranks metals by their corrosion potential.",
            ["galvanic", "dissimilar metals", "corrosion"], 1.0
        ),
        SearchDocument(
            3, "Pitting Corrosion due to Chloride-Induced Passivity Breakdown",
            "Pitting corrosion is a localized attack resulting from the breakdown of passive films, often induced by chloride ions. Stainless steels are particularly susceptible in chloride environments.",
            ["pitting", "chloride", "passivity"], 1.0
        ),
        SearchDocument(
            4, "Crevice Corrosion due to Differential Aeration",
            "Crevice corrosion occurs in shielded areas where oxygen concentration differs, leading to aggressive localized attack. Gasketed joints and lap joints are common sites.",
            ["crevice", "differential aeration", "localized"], 1.0
        ),
        SearchDocument(
            5, "Stress Corrosion Cracking (SCC) in Chloride and Caustic Environments",
            "SCC is the brittle failure of metals under tensile stress and corrosive environments, such as chlorides or caustics. Austenitic stainless steels are vulnerable to chloride SCC.",
            ["scc", "chloride", "caustic", "cracking"], 1.0
        ),
        SearchDocument(
            6, "Hydrogen Embrittlement Mechanisms",
            "Hydrogen embrittlement involves the ingress of atomic hydrogen into metals, reducing ductility and causing cracking. High-strength steels are particularly susceptible.",
            ["hydrogen embrittlement", "cracking"], 1.0
        ),
        SearchDocument(
            7, "Hydrogen Induced Cracking (HIC) and Stepwise Cracking (SOHIC)",
            "HIC occurs when hydrogen diffuses into steel, forming blisters and cracks. SOHIC is a stepwise form of HIC, often seen in sour service environments.",
            ["hic", "sohic", "hydrogen", "cracking"], 1.0
        ),
        SearchDocument(
            8, "Sulfide Stress Cracking (SSC) and NACE MR0175/ISO 15156",
            "SSC is a form of hydrogen embrittlement in the presence of H2S. NACE MR0175/ISO 15156 provides material selection guidelines for sour service.",
            ["ssc", "nace", "h2s", "sour service"], 1.0
        ),
        SearchDocument(
            9, "Erosion Corrosion due to Flow Velocity and Impingement",
            "Erosion corrosion results from the combined action of mechanical wear and corrosion, accelerated by high flow velocities and impingement of particles.",
            ["erosion corrosion", "flow velocity", "impingement"], 1.0
        ),
        SearchDocument(
            10, "Microbiologically Influenced Corrosion (MIC) by SRB and APB",
            "MIC is caused by the metabolic activity of microorganisms such as sulfate-reducing bacteria (SRB) and acid-producing bacteria (APB), leading to localized corrosion.",
            ["mic", "srb", "apb", "microbiological"], 1.0
        ),
        SearchDocument(
            11, "CO2 Corrosion (Sweet Corrosion) and de Waard-Milliams Model",
            "CO2 corrosion, also known as sweet corrosion, affects carbon steels in oil and gas pipelines. The de Waard-Milliams model predicts corrosion rates based on CO2 partial pressure and temperature.",
            ["co2", "sweet corrosion", "de waard-milliams"], 1.0
        ),
        SearchDocument(
            12, "H2S Corrosion (Sour Service) and NACE MR0175/ISO 15156",
            "H2S corrosion, or sour service corrosion, leads to sulfide stress cracking and hydrogen-induced cracking. NACE MR0175/ISO 15156 outlines requirements for material selection.",
            ["h2s", "sour service", "nace", "corrosion"], 1.0
        ),
        SearchDocument(
            13, "Cathodic Protection: Impressed Current Systems",
            "Impressed current cathodic protection (ICCP) uses an external power source to provide protective current, preventing corrosion of buried or submerged structures.",
            ["cathodic protection", "impressed current", "iccp"], 1.0
        ),
        SearchDocument(
            14, "Cathodic Protection: Sacrificial Anode Systems",
            "Sacrificial anode systems use more active metals such as zinc, magnesium, or aluminum to protect steel structures by corroding preferentially.",
            ["cathodic protection", "sacrificial anode"], 1.0
        ),
        SearchDocument(
            15, "Coating Systems: Epoxy, Polyurethane, FBE, and Three-Layer",
            "Protective coatings such as epoxy, polyurethane, fusion-bonded epoxy (FBE), and three-layer systems provide barrier protection against corrosion.",
            ["coating", "epoxy", "polyurethane", "fbe", "three-layer"], 1.0
        ),
        SearchDocument(
            16, "Corrosion Inhibitors: Film-Forming and Neutralizing Types",
            "Corrosion inhibitors are chemicals that reduce corrosion rates. Film-forming inhibitors create a protective layer, while neutralizing inhibitors adjust pH.",
            ["inhibitors", "film-forming", "neutralizing"], 1.0
        ),
        SearchDocument(
            17, "Material Selection: Corrosion Resistant Alloys (CRA)",
            "CRAs such as Inconel, Hastelloy, and Monel are selected for their superior corrosion resistance in aggressive environments.",
            ["material selection", "cra", "alloys"], 1.0
        ),
        SearchDocument(
            18, "Material Selection: Duplex and Super Duplex Stainless Steels",
            "Duplex and super duplex stainless steels combine high strength with excellent resistance to chloride-induced corrosion and stress corrosion cracking.",
            ["material selection", "duplex", "super duplex"], 1.0
        ),
        SearchDocument(
            19, "Corrosion Monitoring: Coupons, Electrical Resistance (ER), Linear Polarization Resistance (LPR), and Field Signature Method (FSM)",
            "Corrosion monitoring techniques include weight loss coupons, ER probes, LPR measurements, and FSM for real-time assessment.",
            ["monitoring", "coupons", "er", "lpr", "fsm"], 1.0
        ),
        SearchDocument(
            20, "Internal Corrosion Direct Assessment (ICDA)",
            "ICDA is a methodology for assessing internal corrosion threats in pipelines, using data integration and corrosion modeling.",
            ["icda", "internal corrosion", "assessment"], 1.0
        ),
        SearchDocument(
            21, "External Corrosion Direct Assessment (ECDA)",
            "ECDA is used to evaluate external corrosion risks on buried pipelines, involving indirect inspection, direct examination, and remediation.",
            ["ecda", "external corrosion", "assessment"], 1.0
        ),
        SearchDocument(
            22, "Pipeline Integrity Management: ASME B31G and RSTRENG",
            "ASME B31G and RSTRENG are engineering assessment methods for evaluating the remaining strength of corroded pipelines.",
            ["pipeline integrity", "asme b31g", "rstreng"], 1.0
        ),
        SearchDocument(
            23, "Corrosion Allowance and Remaining Life Assessment",
            "Corrosion allowance is the extra material thickness provided to compensate for expected corrosion loss. Remaining life assessment estimates service life based on corrosion rates.",
            ["corrosion allowance", "remaining life", "assessment"], 1.0
        ),
        SearchDocument(
            24, "High Temperature Corrosion: Oxidation, Sulfidation, Carburization",
            "High temperature corrosion includes oxidation, sulfidation, and carburization, affecting materials exposed to elevated temperatures and reactive environments.",
            ["high temperature", "oxidation", "sulfidation", "carburization"], 1.0
        ),
        SearchDocument(
            25, "Corrosion Fatigue in Marine Environments",
            "Corrosion fatigue is the reduction of fatigue life due to the combined action of cyclic stress and corrosive marine environments.",
            ["corrosion fatigue", "marine", "cyclic stress"], 1.0
        ),
        SearchDocument(
            26, "Localized Corrosion: Mechanisms and Prevention",
            "Localized corrosion includes pitting, crevice, and intergranular corrosion. Prevention involves material selection, coatings, and inhibitors.",
            ["localized corrosion", "pitting", "crevice", "prevention"], 1.0
        ),
        SearchDocument(
            27, "Passivation and Passive Film Stability",
            "Passivation is the formation of a stable oxide film that protects metals from corrosion. Stability depends on environment and alloy composition.",
            ["passivation", "passive film", "stability"], 1.0
        ),
        SearchDocument(
            28, "Intergranular Corrosion in Stainless Steels",
            "Intergranular corrosion occurs along grain boundaries, often due to chromium carbide precipitation in stainless steels.",
            ["intergranular", "stainless steel", "grain boundary"], 1.0
        ),
        SearchDocument(
            29, "Corrosion Under Insulation (CUI)",
            "CUI is a hidden form of corrosion occurring beneath thermal insulation, often due to trapped moisture and contaminants.",
            ["cui", "insulation", "hidden corrosion"], 1.0
        ),
        SearchDocument(
            30, "Atmospheric Corrosion and Protective Measures",
            "Atmospheric corrosion is influenced by humidity, pollutants, and temperature. Protective measures include coatings and cathodic protection.",
            ["atmospheric", "humidity", "protection"], 1.0
        ),
        SearchDocument(
            31, "Anodic and Cathodic Reactions in Corrosion Cells",
            "Corrosion cells involve anodic metal dissolution and cathodic reduction, such as oxygen or hydrogen evolution reactions.",
            ["anodic", "cathodic", "corrosion cell"], 1.0
        ),
        SearchDocument(
            32, "Role of pH and Redox Potential in Corrosion",
            "pH and redox potential influence corrosion rates and the stability of passive films. Pourbaix diagrams map stability regions.",
            ["ph", "redox", "pourbaix"], 1.0
        ),
        SearchDocument(
            33, "Corrosion Testing: ASTM Standards",
            "ASTM standards provide methodologies for corrosion testing, including salt spray, immersion, and electrochemical tests.",
            ["testing", "astm", "standards"], 1.0
        ),
        SearchDocument(
            34, "Corrosion in Oil and Gas Pipelines",
            "Oil and gas pipelines face internal and external corrosion threats from water, CO2, H2S, and bacteria. Integrity management is critical.",
            ["pipelines", "oil and gas", "integrity"], 1.0
        ),
        SearchDocument(
            35, "Environmental Cracking: Mechanisms and Control",
            "Environmental cracking includes SCC, hydrogen embrittlement, and corrosion fatigue. Control involves stress reduction and material selection.",
            ["environmental cracking", "scc", "embrittlement"], 1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)