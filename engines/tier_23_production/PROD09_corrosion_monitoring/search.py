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
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self.tf_cache: Dict[int, Counter] = {}
        self._seeded = False

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.tf_cache[doc.id] = Counter(tokens)
            for token in tokens:
                self.inverted_index[token][doc.id] = self.inverted_index[token].get(doc.id, 0) + 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        tokens = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for token in tokens:
            idf = self._compute_idf(token)
            for doc_id, tf in self.inverted_index.get(token, {}).items():
                doc = self.documents[doc_id]
                score = self._score_bm25(token, doc_id, idf)
                doc_scores[doc_id] += score * doc.weight
        results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        output = []
        for doc_id, score in results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, tokens)
            output.append(SearchResult(doc_id, score, doc.title, snippet))
        return output

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.inverted_index),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: int, idf: float) -> float:
        tf = self.tf_cache[doc_id][term]
        doc_length = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / avg_dl)
        return idf * numerator / denominator if denominator != 0 else 0.0

    def _make_snippet(self, content: str, query_tokens: List[str], length: int = 120) -> str:
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not indices:
            snippet = content[:length] + ('...' if len(content) > length else '')
            return snippet
        start = max(indices[0] - 10, 0)
        end = min(indices[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet[:length] + ('...' if len(snippet) > length else '')

    def tfidf_score(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            tf_counter = self.tf_cache[doc_id]
            doc_length = self.doc_lengths[doc_id]
            score = 0.0
            for token in query_tokens:
                tf = tf_counter[token] / doc_length if doc_length > 0 else 0.0
                idf = self._compute_idf(token)
                score += tf * idf
            doc_scores[doc_id] = score * doc.weight
        results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        output = []
        for doc_id, score in results[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            output.append(SearchResult(doc_id, score, doc.title, snippet))
        return output

    def seed_documents(self):
        if self._seeded:
            return
        docs = [
            SearchDocument(
                1,
                "CO2 Corrosion Mechanism",
                "CO2 corrosion occurs when carbon dioxide dissolves in water, forming carbonic acid. This acid reacts with steel surfaces, leading to metal loss. The de Waard-Milliams model predicts corrosion rates based on partial pressure of CO2, temperature, and flow conditions.",
                ["CO2", "corrosion", "de Waard-Milliams", "mechanism"],
                1.0
            ),
            SearchDocument(
                2,
                "de Waard-Milliams Model",
                "The de Waard-Milliams model is an empirical formula used to estimate CO2 corrosion rates in carbon steel pipelines. It considers CO2 partial pressure, temperature, and flow velocity. Accurate prediction helps in material selection and inhibitor dosing.",
                ["CO2", "de Waard-Milliams", "corrosion", "model"],
                1.0
            ),
            SearchDocument(
                3,
                "H2S Corrosion and Sulfide Stress Cracking (SSC)",
                "Hydrogen sulfide (H2S) causes corrosion and can induce sulfide stress cracking (SSC) in susceptible alloys. SSC is a form of hydrogen embrittlement, particularly dangerous in high-strength steels. Mitigation includes material selection and environmental control.",
                ["H2S", "corrosion", "SSC", "hydrogen embrittlement"],
                1.0
            ),
            SearchDocument(
                4,
                "Microbiologically Influenced Corrosion (MIC)",
                "MIC is caused by microorganisms such as sulfate-reducing bacteria (SRB) and acid-producing bacteria. These microbes accelerate corrosion by producing corrosive metabolites and altering local chemistry. Monitoring involves biofilm detection and coupon analysis.",
                ["MIC", "SRB", "acid-producing bacteria", "biofilm"],
                1.0
            ),
            SearchDocument(
                5,
                "Corrosion Coupon Monitoring",
                "Corrosion coupons are metal samples exposed to process environments to measure corrosion rates. Weight loss analysis provides average corrosion rate. Coupons are used for validating inhibitor performance and detecting localized corrosion.",
                ["corrosion coupon", "monitoring", "weight loss", "inhibitor"],
                1.0
            ),
            SearchDocument(
                6,
                "Electrical Resistance (ER) Probes",
                "ER probes measure metal loss by monitoring changes in electrical resistance. They provide real-time corrosion rate data and are suitable for continuous monitoring in pipelines and vessels.",
                ["electrical resistance", "ER probe", "monitoring"],
                1.0
            ),
            SearchDocument(
                7,
                "Linear Polarization Resistance (LPR) Probes",
                "LPR probes estimate corrosion rates by measuring the polarization resistance of a metal electrode. The technique is rapid and sensitive to changes in corrosion conditions, commonly used in water treatment and oil and gas systems.",
                ["LPR", "polarization resistance", "corrosion rate"],
                1.0
            ),
            SearchDocument(
                8,
                "Ultrasonic Thickness Measurement (UTM)",
                "UTM uses ultrasonic waves to measure wall thickness of pipes and vessels. It detects metal loss due to corrosion or erosion, supporting inspection and integrity management programs.",
                ["UTM", "ultrasonic", "thickness", "inspection"],
                1.0
            ),
            SearchDocument(
                9,
                "Corrosion Inhibitor Selection - Film-Forming Amines",
                "Film-forming amines are corrosion inhibitors that create a protective layer on metal surfaces. Selection depends on compatibility, effectiveness, and environmental regulations. Proper dosing and monitoring are essential for optimal protection.",
                ["corrosion inhibitor", "film-forming amine", "selection"],
                1.0
            ),
            SearchDocument(
                10,
                "Corrosion-Resistant Alloy (CRA) Material Selection",
                "CRA materials such as duplex stainless steels and nickel alloys are chosen for their resistance to CO2, H2S, and MIC. Selection criteria include PRE, mechanical properties, and cost. Proper alloy selection prevents premature failure.",
                ["CRA", "material selection", "PRE", "corrosion-resistant"],
                1.0
            ),
            SearchDocument(
                11,
                "Cathodic Protection (CP) for Pipelines and Structures",
                "CP systems protect pipelines and structures from corrosion by applying a direct current. Sacrificial anodes and impressed current systems are used. Monitoring and maintenance ensure long-term effectiveness.",
                ["cathodic protection", "CP", "pipeline", "structure"],
                1.0
            ),
            SearchDocument(
                12,
                "Pipeline Integrity Management (IIM) and Inline Inspection (ILI)",
                "IIM involves risk assessment, monitoring, and mitigation to ensure pipeline safety. ILI tools such as smart pigs detect corrosion, cracks, and wall loss. Data analysis supports maintenance and repair decisions.",
                ["pipeline integrity", "IIM", "ILI", "inspection"],
                1.0
            ),
            SearchDocument(
                13,
                "Erosion-Corrosion in High-Velocity Systems",
                "Erosion-corrosion occurs when high-velocity fluids remove protective films, accelerating metal loss. It is common in elbows, tees, and pumps. Mitigation includes material upgrades and flow control.",
                ["erosion-corrosion", "high-velocity", "mitigation"],
                1.0
            ),
            SearchDocument(
                14,
                "Galvanic Corrosion in Mixed-Metallurgy Systems",
                "Galvanic corrosion arises when dissimilar metals are electrically connected in a corrosive environment. The more active metal corrodes faster. Prevention includes insulation and careful material selection.",
                ["galvanic corrosion", "mixed-metallurgy", "dissimilar metals"],
                1.0
            ),
            SearchDocument(
                15,
                "Pitting Corrosion and Pitting Resistance Equivalent (PRE)",
                "Pitting corrosion is a localized form of corrosion resulting in small holes. PRE is a measure of alloy resistance to pitting, calculated from chromium, molybdenum, and nitrogen content. High PRE alloys are preferred for severe environments.",
                ["pitting corrosion", "PRE", "localized corrosion"],
                1.0
            ),
            SearchDocument(
                16,
                "Sulfate-Reducing Bacteria (SRB) and MIC",
                "SRB are key contributors to MIC, producing hydrogen sulfide and accelerating corrosion. Detection methods include molecular analysis and coupon exposure. Control strategies involve biocide dosing and environmental management.",
                ["SRB", "MIC", "hydrogen sulfide", "biocide"],
                1.0
            ),
            SearchDocument(
                17,
                "Corrosion Monitoring Data Interpretation",
                "Interpreting corrosion monitoring data requires understanding probe response, environmental conditions, and process changes. Data trends inform maintenance and inhibitor optimization.",
                ["corrosion monitoring", "data interpretation", "maintenance"],
                1.0
            ),
            SearchDocument(
                18,
                "Corrosion Inhibitor Performance Evaluation",
                "Performance evaluation involves laboratory testing, field trials, and monitoring. Key metrics include corrosion rate reduction, compatibility, and environmental impact.",
                ["corrosion inhibitor", "performance", "evaluation"],
                1.0
            ),
            SearchDocument(
                19,
                "Localized Corrosion Detection Techniques",
                "Techniques for detecting localized corrosion include high-resolution ultrasonic inspection, radiography, and coupon analysis. Early detection prevents catastrophic failures.",
                ["localized corrosion", "detection", "inspection"],
                1.0
            ),
            SearchDocument(
                20,
                "Pipeline Corrosion Risk Assessment",
                "Risk assessment combines corrosion rate data, material properties, and environmental factors. Models predict likelihood of failure, guiding mitigation and inspection planning.",
                ["pipeline", "corrosion", "risk assessment", "mitigation"],
                1.0
            ),
            SearchDocument(
                21,
                "Corrosion Under Insulation (CUI)",
                "CUI occurs when moisture penetrates insulation, causing corrosion on external surfaces. Detection methods include visual inspection, moisture meters, and ultrasonic testing.",
                ["CUI", "corrosion", "insulation", "detection"],
                1.0
            ),
            SearchDocument(
                22,
                "Hydrogen Embrittlement in SSC",
                "SSC is aggravated by hydrogen embrittlement, where atomic hydrogen diffuses into steel, causing cracking. Prevention includes alloy selection and environmental control.",
                ["hydrogen embrittlement", "SSC", "cracking"],
                1.0
            ),
            SearchDocument(
                23,
                "Corrosion Fatigue in Pipelines",
                "Corrosion fatigue combines cyclic loading and corrosive environments, leading to crack initiation and growth. Monitoring involves ultrasonic inspection and fracture mechanics analysis.",
                ["corrosion fatigue", "pipeline", "crack", "inspection"],
                1.0
            ),
            SearchDocument(
                24,
                "Corrosion Mapping and Inspection",
                "Corrosion mapping uses advanced inspection tools to visualize metal loss and damage. Techniques include ultrasonic phased array and magnetic flux leakage.",
                ["corrosion mapping", "inspection", "metal loss"],
                1.0
            ),
            SearchDocument(
                25,
                "Corrosion Inhibitor Dosing Strategies",
                "Effective dosing strategies depend on process conditions, inhibitor properties, and monitoring feedback. Overdosing can cause fouling, while underdosing leads to insufficient protection.",
                ["corrosion inhibitor", "dosing", "strategy"],
                1.0
            ),
            SearchDocument(
                26,
                "Corrosion Monitoring in Sour Environments",
                "Sour environments contain H2S, increasing corrosion risk and SSC susceptibility. Monitoring includes ER probes, coupons, and regular inspection.",
                ["corrosion monitoring", "sour environment", "H2S"],
                1.0
            ),
            SearchDocument(
                27,
                "Smart Pigging for Pipeline Inspection",
                "Smart pigs are inline inspection tools that detect corrosion, cracks, and wall loss. Technologies include magnetic flux leakage and ultrasonic testing.",
                ["smart pig", "pipeline", "inspection", "ILI"],
                1.0
            ),
            SearchDocument(
                28,
                "Corrosion Rate Prediction Models",
                "Corrosion rate prediction uses empirical and mechanistic models, including de Waard-Milliams for CO2 and NACE standards for H2S. Accurate prediction guides material selection and inhibitor application.",
                ["corrosion rate", "prediction", "model", "NACE"],
                1.0
            ),
            SearchDocument(
                29,
                "Corrosion Inhibitor Environmental Impact",
                "Environmental impact assessment considers toxicity, biodegradability, and regulatory compliance. Selection favors inhibitors with minimal ecological risk.",
                ["corrosion inhibitor", "environmental impact", "regulation"],
                1.0
            ),
            SearchDocument(
                30,
                "Corrosion-Resistant Alloy (CRA) Welding Considerations",
                "Welding CRAs requires control of heat input and filler selection to maintain corrosion resistance. Post-weld inspection ensures integrity and performance.",
                ["CRA", "welding", "corrosion resistance", "inspection"],
                1.0
            ),
            SearchDocument(
                31,
                "Cathodic Protection System Maintenance",
                "Maintenance of CP systems includes regular potential measurements, anode replacement, and rectifier checks. Proper maintenance ensures continuous protection.",
                ["cathodic protection", "maintenance", "anode", "rectifier"],
                1.0
            ),
            SearchDocument(
                32,
                "Corrosion Inhibitor Compatibility Testing",
                "Compatibility testing ensures inhibitors do not react adversely with process fluids or materials. Laboratory tests include emulsion tendency and scaling.",
                ["corrosion inhibitor", "compatibility", "testing"],
                1.0
            ),
            SearchDocument(
                33,
                "Corrosion Monitoring System Integration",
                "Integration of monitoring systems enables real-time data collection, analysis, and reporting. Systems include ER, LPR, and ultrasonic sensors.",
                ["corrosion monitoring", "system integration", "real-time"],
                1.0
            ),
            SearchDocument(
                34,
                "Galvanic Series and Material Selection",
                "The galvanic series ranks metals by their electrochemical activity. Selecting metals with similar potentials minimizes galvanic corrosion risk.",
                ["galvanic series", "material selection", "corrosion"],
                1.0
            ),
            SearchDocument(
                35,
                "Erosion-Corrosion Mitigation Techniques",
                "Mitigation techniques include reducing flow velocity, using erosion-resistant alloys, and optimizing pipe geometry. Regular inspection detects early signs.",
                ["erosion-corrosion", "mitigation", "inspection"],
                1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._seeded = True

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _search_index_instance.seed_documents()
        return _search_index_instance