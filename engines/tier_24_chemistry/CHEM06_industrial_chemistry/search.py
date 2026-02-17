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
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self.k1 = 1.5
        self.b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.term_freqs[doc.id] = Counter(tokens)
            for token in set(tokens):
                self.term_doc_freq[token] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            score += idf * (numerator / denominator)
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            f = tf.get(term, 0)
            if f == 0:
                continue
            tf_norm = f / doc_len if doc_len > 0 else 0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(doc_id, query_terms)
            else:
                score = self._score_bm25(doc_id, query_terms)
            if score > 0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, token in enumerate(tokens) if token in query_terms]
        if not positions:
            return content[:snippet_len] + ('...' if len(content) > snippet_len else '')
        start = max(positions[0] - 10, 0)
        end = min(start + 40, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet[:snippet_len] + ('...' if len(snippet) > snippet_len else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Haber-Bosch Process: Overview",
            "The Haber-Bosch process synthesizes ammonia from nitrogen and hydrogen gases under high temperature and pressure using an iron catalyst. It revolutionized fertilizer production and supports global agriculture.",
            ["haber-bosch", "ammonia", "synthesis", "catalyst"],
            1.0
        ),
        SearchDocument(
            2,
            "Ammonia Synthesis Reaction Conditions",
            "Optimal conditions for ammonia synthesis include temperatures of 400-500°C, pressures of 150-300 atm, and an iron-based catalyst. The equilibrium favors ammonia formation at lower temperatures but requires high pressure.",
            ["haber-bosch", "conditions", "temperature", "pressure"],
            1.0
        ),
        SearchDocument(
            3,
            "Catalysts in the Haber-Bosch Process",
            "Iron catalysts are used in the Haber-Bosch process, often promoted with potassium and aluminum oxides. Catalysts increase the reaction rate and improve ammonia yield.",
            ["haber-bosch", "catalyst", "iron", "promoters"],
            1.0
        ),
        SearchDocument(
            4,
            "Contact Process: Sulfuric Acid Production",
            "The Contact Process produces sulfuric acid by oxidizing sulfur dioxide to sulfur trioxide using a vanadium(V) oxide catalyst, followed by absorption in water. It is the primary industrial method for sulfuric acid manufacture.",
            ["contact-process", "sulfuric-acid", "production", "catalyst"],
            1.0
        ),
        SearchDocument(
            5,
            "Sulfur Dioxide Oxidation in the Contact Process",
            "Sulfur dioxide is oxidized to sulfur trioxide in the presence of a vanadium(V) oxide catalyst at temperatures of 400-600°C. The reaction is exothermic and equilibrium is achieved at moderate temperatures.",
            ["contact-process", "oxidation", "sulfur-dioxide", "catalyst"],
            1.0
        ),
        SearchDocument(
            6,
            "Absorption of Sulfur Trioxide",
            "Sulfur trioxide is absorbed in concentrated sulfuric acid to form oleum, which is then diluted to produce sulfuric acid. Direct absorption in water is avoided due to the formation of a corrosive mist.",
            ["contact-process", "absorption", "sulfur-trioxide", "oleum"],
            1.0
        ),
        SearchDocument(
            7,
            "Chloralkali Process: Membrane Cell Technology",
            "The chloralkali process uses membrane cell technology to electrolyze brine, producing chlorine, hydrogen, and sodium hydroxide. Membrane cells provide high purity and energy efficiency compared to older methods.",
            ["chloralkali", "membrane-cell", "electrolysis", "brine"],
            1.0
        ),
        SearchDocument(
            8,
            "Electrolysis of Brine in Chloralkali Process",
            "Brine is electrolyzed in a membrane cell, separating chlorine gas at the anode and hydrogen gas at the cathode. Sodium ions pass through the membrane to form sodium hydroxide.",
            ["chloralkali", "electrolysis", "brine", "sodium-hydroxide"],
            1.0
        ),
        SearchDocument(
            9,
            "Advantages of Membrane Cell Technology",
            "Membrane cells in the chloralkali process reduce contamination, improve product purity, and lower energy consumption compared to diaphragm and mercury cells.",
            ["chloralkali", "membrane-cell", "advantages", "purity"],
            1.0
        ),
        SearchDocument(
            10,
            "Environmental Impact of Industrial Chemistry",
            "Industrial chemical processes such as Haber-Bosch, Contact, and Chloralkali have environmental impacts including greenhouse gas emissions, energy consumption, and waste generation. Modern technologies aim to reduce these effects.",
            ["environment", "industrial-chemistry", "impact", "sustainability"],
            1.0
        ),
        SearchDocument(
            11,
            "Ammonia Uses in Industry",
            "Ammonia produced by the Haber-Bosch process is used in fertilizers, explosives, and cleaning agents. Its synthesis is vital for food production and industrial applications.",
            ["ammonia", "uses", "industry", "haber-bosch"],
            1.0
        ),
        SearchDocument(
            12,
            "Sulfuric Acid Applications",
            "Sulfuric acid is used in fertilizer production, petroleum refining, wastewater treatment, and chemical synthesis. The Contact Process ensures high purity and large-scale production.",
            ["sulfuric-acid", "applications", "contact-process", "industry"],
            1.0
        ),
        SearchDocument(
            13,
            "Chlorine Production and Uses",
            "Chlorine from the chloralkali process is used for water disinfection, PVC manufacturing, and bleaching. Membrane cell technology ensures high purity chlorine output.",
            ["chlorine", "production", "chloralkali", "membrane-cell"],
            1.0
        ),
        SearchDocument(
            14,
            "Industrial Safety in Chemical Processes",
            "Safety measures in industrial chemistry include pressure monitoring, catalyst handling, and containment of toxic gases. Automation and sensors improve process safety.",
            ["safety", "industrial-chemistry", "automation", "monitoring"],
            1.0
        ),
        SearchDocument(
            15,
            "Energy Efficiency in Ammonia Synthesis",
            "Energy efficiency in the Haber-Bosch process is improved by heat recovery, catalyst optimization, and process integration. Lowering energy consumption reduces costs and environmental impact.",
            ["haber-bosch", "energy-efficiency", "ammonia", "optimization"],
            1.0
        ),
        SearchDocument(
            16,
            "Catalyst Regeneration in Contact Process",
            "Vanadium(V) oxide catalysts in the Contact Process can be regenerated to maintain activity and extend catalyst life. Regeneration reduces operational costs.",
            ["contact-process", "catalyst", "regeneration", "vanadium"],
            1.0
        ),
        SearchDocument(
            17,
            "Membrane Cell Maintenance",
            "Regular maintenance of membrane cells in the chloralkali process ensures consistent performance and prevents fouling. Cleaning protocols and monitoring are essential.",
            ["chloralkali", "membrane-cell", "maintenance", "performance"],
            1.0
        ),
        SearchDocument(
            18,
            "Process Control in Industrial Chemistry",
            "Advanced process control systems monitor reaction conditions, optimize yields, and ensure product quality in industrial chemical processes.",
            ["process-control", "industrial-chemistry", "optimization", "quality"],
            1.0
        ),
        SearchDocument(
            19,
            "Green Chemistry in Ammonia Synthesis",
            "Green chemistry principles are applied to ammonia synthesis by reducing energy use, minimizing emissions, and developing alternative catalysts.",
            ["green-chemistry", "haber-bosch", "ammonia", "sustainability"],
            1.0
        ),
        SearchDocument(
            20,
            "Waste Management in Sulfuric Acid Production",
            "Waste management strategies in sulfuric acid production include recycling sulfur dioxide, treating effluents, and reducing emissions.",
            ["waste-management", "sulfuric-acid", "contact-process", "recycling"],
            1.0
        ),
        SearchDocument(
            21,
            "Hydrogen Production for Haber-Bosch",
            "Hydrogen for the Haber-Bosch process is typically produced by steam reforming of methane. Purity and supply are critical for efficient ammonia synthesis.",
            ["hydrogen", "haber-bosch", "steam-reforming", "purity"],
            1.0
        ),
        SearchDocument(
            22,
            "Sulfur Recovery in Contact Process",
            "Sulfur recovery from industrial waste streams is integrated with the Contact Process to improve sustainability and reduce environmental impact.",
            ["sulfur-recovery", "contact-process", "sustainability", "waste"],
            1.0
        ),
        SearchDocument(
            23,
            "Electrochemical Principles in Chloralkali",
            "Electrochemical principles govern the chloralkali process, including electrode reactions, ion transport, and cell voltage optimization.",
            ["chloralkali", "electrochemistry", "membrane-cell", "electrodes"],
            1.0
        ),
        SearchDocument(
            24,
            "Industrial Scale-Up of Chemical Processes",
            "Scaling up chemical processes involves reactor design, heat transfer, and process optimization to achieve industrial production rates.",
            ["scale-up", "industrial-chemistry", "reactor", "optimization"],
            1.0
        ),
        SearchDocument(
            25,
            "Alternative Methods for Ammonia Synthesis",
            "Research into alternative ammonia synthesis methods includes electrochemical and photochemical approaches, aiming to reduce energy consumption and environmental impact.",
            ["ammonia", "alternative-methods", "haber-bosch", "research"],
            1.0
        ),
        SearchDocument(
            26,
            "Mercury Cell vs Membrane Cell in Chloralkali",
            "Mercury cells were historically used in the chloralkali process but have been replaced by membrane cells due to environmental concerns and improved safety.",
            ["chloralkali", "mercury-cell", "membrane-cell", "environment"],
            1.0
        ),
        SearchDocument(
            27,
            "Process Optimization in Sulfuric Acid Production",
            "Process optimization in sulfuric acid production involves controlling temperature, catalyst activity, and gas flow to maximize yield and minimize waste.",
            ["sulfuric-acid", "optimization", "contact-process", "yield"],
            1.0
        ),
        SearchDocument(
            28,
            "Feedstock Preparation for Haber-Bosch",
            "Feedstock preparation for the Haber-Bosch process includes purification of nitrogen and hydrogen gases to prevent catalyst poisoning.",
            ["haber-bosch", "feedstock", "purification", "catalyst"],
            1.0
        ),
        SearchDocument(
            29,
            "Oleum Handling and Storage",
            "Oleum produced in the Contact Process requires careful handling and storage due to its corrosive nature and tendency to release sulfur trioxide.",
            ["oleum", "contact-process", "storage", "handling"],
            1.0
        ),
        SearchDocument(
            30,
            "Brine Purification in Chloralkali Process",
            "Purification of brine before electrolysis in the chloralkali process is essential to prevent membrane fouling and ensure high purity products.",
            ["chloralkali", "brine", "purification", "membrane-cell"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)