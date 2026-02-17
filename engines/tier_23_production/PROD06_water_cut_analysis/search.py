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
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            for token in tokens:
                self.term_freqs[doc.id][token] += 1
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 1)
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length or 1))
            score += idf * numerator / denominator
        return score * self.documents[doc_id].weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tfidf_score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 1)
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_length
            idf = self._compute_idf(term)
            tfidf_score += tf_norm * idf
        return tfidf_score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = {}
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(doc_id, query_terms)
            else:
                score = self._score_bm25(doc_id, query_terms)
            if score > 0.0:
                doc_scores[doc_id] = score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], max_len: int = 160) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:max_len] + ('...' if len(content) > max_len else '')
            return snippet
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        if len(snippet) > max_len:
            snippet = snippet[:max_len] + '...'
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# Pre-seed documents
def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Water Cut Definition and Calculation",
            "Water cut is the ratio of water produced compared to total liquids. Calculation involves measuring produced water and oil volumes and expressing water cut as a percentage.",
            ["water cut", "definition", "calculation"],
            1.0
        ),
        SearchDocument(
            2,
            "BSW Measurement Techniques - Centrifuge Method",
            "The centrifuge method for Basic Sediment and Water (BSW) measurement separates water and solids from oil using centrifugal force. Accurate readings depend on proper sample handling.",
            ["BSW", "centrifuge", "measurement", "technique"],
            1.0
        ),
        SearchDocument(
            3,
            "Karl Fischer Titration for Water Content",
            "Karl Fischer titration is a chemical analysis technique for quantifying water content in oil samples. It is highly sensitive and suitable for low water concentrations.",
            ["Karl Fischer", "titration", "water content"],
            1.0
        ),
        SearchDocument(
            4,
            "Waterflood Performance - Buckley-Leverett Theory",
            "Buckley-Leverett theory models waterflood displacement in reservoirs, predicting oil recovery and water breakthrough based on fractional flow and relative permeability.",
            ["waterflood", "Buckley-Leverett", "performance"],
            1.0
        ),
        SearchDocument(
            5,
            "Water Breakthrough Prediction - Channel and Frontal Advance",
            "Water breakthrough occurs when injected water reaches production wells. Prediction methods include channel advance and frontal advance models to estimate timing and impact.",
            ["water breakthrough", "prediction", "channel", "frontal advance"],
            1.0
        ),
        SearchDocument(
            6,
            "Chan Diagnostic Plots for Water Production Analysis",
            "Chan diagnostic plots visualize water production trends and help identify breakthrough, channeling, and conformance issues in waterflooded reservoirs.",
            ["Chan plots", "diagnostic", "water production"],
            1.0
        ),
        SearchDocument(
            7,
            "Water Coning in Vertical Wells",
            "Water coning is the upward movement of water towards the wellbore in vertical wells. It is influenced by production rate, permeability, and reservoir heterogeneity.",
            ["water coning", "vertical wells"],
            1.0
        ),
        SearchDocument(
            8,
            "Produced Water Handling and Treatment",
            "Produced water handling involves separation, treatment, and disposal. Treatment methods include filtration, chemical dosing, and reinjection to meet regulatory standards.",
            ["produced water", "handling", "treatment"],
            1.0
        ),
        SearchDocument(
            9,
            "Injection Water Quality Requirements",
            "Injection water must meet quality requirements to prevent reservoir damage. Parameters include suspended solids, bacteria, and compatibility with formation fluids.",
            ["injection water", "quality", "requirements"],
            1.0
        ),
        SearchDocument(
            10,
            "Water-Oil Ratio (WOR) Decline Analysis",
            "Water-Oil Ratio (WOR) decline analysis tracks water production relative to oil. It helps diagnose reservoir performance and predict future water cut trends.",
            ["WOR", "decline analysis", "water-oil ratio"],
            1.0
        ),
        SearchDocument(
            11,
            "Relative Permeability and Fractional Flow",
            "Relative permeability curves and fractional flow equations are essential for modeling multiphase flow in reservoirs and optimizing waterflood strategies.",
            ["relative permeability", "fractional flow"],
            1.0
        ),
        SearchDocument(
            12,
            "Water Cut Measurement - Online Meters vs Manual Sampling",
            "Water cut can be measured using online meters or manual sampling. Online meters provide real-time data, while manual methods offer accuracy for calibration.",
            ["water cut", "measurement", "online meters", "manual sampling"],
            1.0
        ),
        SearchDocument(
            13,
            "Water Disposal Regulations - UIC Class II Wells",
            "Water disposal in oilfields is regulated under the Underground Injection Control (UIC) Class II program. Compliance ensures safe injection and environmental protection.",
            ["water disposal", "regulations", "UIC Class II"],
            1.0
        ),
        SearchDocument(
            14,
            "Declining Oil Rate with Constant Liquid Rate - Artificial Lift Constraints",
            "Artificial lift systems may maintain constant liquid rate while oil rate declines due to increasing water cut. Proper lift selection and optimization are critical.",
            ["artificial lift", "oil rate", "liquid rate", "constraints"],
            1.0
        ),
        SearchDocument(
            15,
            "Waterflood Pattern Balancing - Injection-Production Ratio",
            "Pattern balancing in waterfloods involves managing injection-production ratios to optimize sweep efficiency and minimize water channeling.",
            ["waterflood", "pattern balancing", "injection-production ratio"],
            1.0
        ),
        SearchDocument(
            16,
            "Emulsion Stability and Demulsification",
            "Emulsion stability affects oil-water separation. Demulsification techniques include chemical additives, heating, and mechanical separation to break emulsions.",
            ["emulsion", "stability", "demulsification"],
            1.0
        ),
        SearchDocument(
            17,
            "Water Influx from Aquifer - Material Balance",
            "Material balance methods estimate water influx from aquifers into oil reservoirs, aiding reservoir management and production forecasting.",
            ["water influx", "aquifer", "material balance"],
            1.0
        ),
        SearchDocument(
            18,
            "Water Saturation from Well Logs - Archie Equation",
            "Archie equation calculates water saturation from resistivity logs. It is fundamental for evaluating hydrocarbon reserves and reservoir quality.",
            ["water saturation", "well logs", "Archie equation"],
            1.0
        ),
        SearchDocument(
            19,
            "Produced Water Salinity and Water Type Identification",
            "Salinity analysis of produced water helps identify water types and sources. It is important for reservoir characterization and waterflood planning.",
            ["produced water", "salinity", "water type"],
            1.0
        ),
        SearchDocument(
            20,
            "Waterflood Conformance - Gel and Polymer Treatments",
            "Gel and polymer treatments improve waterflood conformance by reducing channeling and improving sweep efficiency in heterogeneous reservoirs.",
            ["waterflood", "conformance", "gel", "polymer"],
            1.0
        ),
        SearchDocument(
            21,
            "Economic Limit - Oil Price Sensitivity and Operating Cost",
            "Economic limit is reached when oil price and operating cost make production unprofitable. Water cut increases operating costs and impacts economic limit.",
            ["economic limit", "oil price", "operating cost"],
            1.0
        ),
        SearchDocument(
            22,
            "Water Production Forecasting - Koval and X-plot Methods",
            "Koval and X-plot methods are used for forecasting water production in reservoirs. They help estimate future water cut and optimize waterflood operations.",
            ["water production", "forecasting", "Koval", "X-plot"],
            1.0
        ),
        SearchDocument(
            23,
            "Water Cut Trends in Mature Fields",
            "Mature fields often exhibit increasing water cut due to reservoir depletion and waterflooding. Monitoring trends is essential for production planning.",
            ["water cut", "trends", "mature fields"],
            1.0
        ),
        SearchDocument(
            24,
            "Online Water Cut Meter Calibration",
            "Calibration of online water cut meters ensures measurement accuracy. Procedures involve comparison with manual samples and adjustment for process conditions.",
            ["water cut", "meter", "calibration", "online"],
            1.0
        ),
        SearchDocument(
            25,
            "Waterflood Sweep Efficiency",
            "Sweep efficiency measures the effectiveness of waterflood in displacing oil. Influenced by reservoir heterogeneity, pattern design, and injection strategy.",
            ["waterflood", "sweep efficiency"],
            1.0
        ),
        SearchDocument(
            26,
            "Produced Water Reuse and Environmental Impact",
            "Produced water can be reused for injection or other purposes. Environmental impact assessment is required to ensure compliance and sustainability.",
            ["produced water", "reuse", "environmental impact"],
            1.0
        ),
        SearchDocument(
            27,
            "Water Cut Impact on Artificial Lift Selection",
            "High water cut affects artificial lift selection and performance. Pump sizing, corrosion, and gas handling must be considered for optimal operation.",
            ["water cut", "artificial lift", "impact"],
            1.0
        ),
        SearchDocument(
            28,
            "Waterflood Surveillance and Diagnostics",
            "Surveillance techniques for waterfloods include tracer tests, production logging, and diagnostic plots to monitor water movement and conformance.",
            ["waterflood", "surveillance", "diagnostics"],
            1.0
        ),
        SearchDocument(
            29,
            "Water Cut Reduction Strategies",
            "Strategies to reduce water cut include conformance treatments, selective completions, and reservoir management to maximize oil recovery.",
            ["water cut", "reduction", "strategies"],
            1.0
        ),
        SearchDocument(
            30,
            "Water Cut and Oil Recovery Factor",
            "Water cut trends are linked to oil recovery factor. Monitoring water cut helps optimize recovery and identify reservoir management opportunities.",
            ["water cut", "oil recovery", "factor"],
            1.0
        ),
        SearchDocument(
            31,
            "Produced Water Sampling Protocols",
            "Proper sampling protocols for produced water ensure accurate analysis of water cut, salinity, and contaminants for regulatory compliance.",
            ["produced water", "sampling", "protocols"],
            1.0
        ),
        SearchDocument(
            32,
            "Waterflood Optimization - Injection Rate Control",
            "Controlling injection rate in waterfloods optimizes sweep efficiency and minimizes water breakthrough. Rate adjustments are based on reservoir response.",
            ["waterflood", "optimization", "injection rate"],
            1.0
        ),
        SearchDocument(
            33,
            "Water Cut Measurement Uncertainty",
            "Measurement uncertainty in water cut arises from sampling errors, meter calibration, and process variability. Understanding uncertainty is vital for decision making.",
            ["water cut", "measurement", "uncertainty"],
            1.0
        ),
        SearchDocument(
            34,
            "Waterflood Reservoir Characterization",
            "Reservoir characterization for waterfloods includes petrophysical analysis, fluid properties, and geological modeling to predict water movement.",
            ["waterflood", "reservoir characterization"],
            1.0
        ),
        SearchDocument(
            35,
            "Water Cut and Emulsion Formation",
            "High water cut can promote emulsion formation, complicating oil-water separation. Demulsification is necessary to maintain process efficiency.",
            ["water cut", "emulsion", "formation"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)