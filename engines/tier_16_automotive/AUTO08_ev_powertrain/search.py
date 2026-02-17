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
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old doc term frequencies
                old_tf = self.doc_term_freqs.get(doc.id, Counter())
                for term in old_tf:
                    self.term_doc_freqs[term] -= 1
                    if self.term_doc_freqs[term] <= 0:
                        del self.term_doc_freqs[term]
                self.total_docs -= 1

            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.doc_term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freqs[term] += 1

            self.documents[doc.id] = doc
            self.total_docs = len(self.documents)
            self.avg_doc_len = self._compute_avg_doc_len()
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        idf = {term: self._compute_idf(term) for term in set(query_terms)}
        scores: Dict[str, float] = defaultdict(float)

        for doc_id, tf in self.doc_term_freqs.items():
            score = self._score_bm25(tf, idf, query_terms, doc_id)
            if score > 0:
                scores[doc_id] = score * self.documents[doc_id].weight

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, int]:
        with self.lock:
            return {
                "total_documents": self.total_docs,
                "unique_terms": len(self.term_doc_freqs),
                "average_document_length": int(self.avg_doc_len),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_avg_doc_len(self) -> float:
        if not self.doc_term_freqs:
            return 0.0
        total_len = sum(sum(tf.values()) for tf in self.doc_term_freqs.values())
        return total_len / len(self.doc_term_freqs)

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        n_q = self.term_doc_freqs.get(term, 0)
        if n_q == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - n_q + 0.5) / (n_q + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, tf: Counter, idf: Dict[str, float], query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc_len = sum(tf.values())
        for term in query_terms:
            if term not in tf:
                continue
            f = tf[term]
            term_idf = idf.get(term, 0.0)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
            score += term_idf * (f * (self.k1 + 1)) / denom
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_length: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            start = 0
            while True:
                idx = content_lower.find(term, start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + len(term)
        if not positions:
            snippet = content[:snippet_length]
            if len(content) > snippet_length:
                snippet += "..."
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_length // 4, 0)
        end_pos = start_pos + snippet_length
        if end_pos > len(content):
            end_pos = len(content)
            start_pos = max(end_pos - snippet_length, 0)
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet += "..."
        return snippet


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _preseed_documents(_singleton_instance)
        return _singleton_instance


def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            "doc001",
            "PMSM vs Induction Motor Selection Criteria",
            "Comparison of Permanent Magnet Synchronous Motors (PMSM) and Induction Motors for electric vehicle powertrains. "
            "Discusses efficiency, cost, control complexity, and performance trade-offs.",
            ["PMSM", "Induction Motor", "Motor Selection", "EV Powertrain"]
        ),
        SearchDocument(
            "doc002",
            "Interior Permanent Magnet (IPM) Motor Design",
            "Design principles and advantages of Interior Permanent Magnet motors including flux weakening, torque density, and thermal management.",
            ["IPM Motor", "Motor Design", "Permanent Magnet", "Thermal Management"]
        ),
        SearchDocument(
            "doc003",
            "SiC vs IGBT Inverter Technology Selection",
            "Analysis of Silicon Carbide (SiC) versus Insulated Gate Bipolar Transistor (IGBT) inverter technologies for EV inverters. "
            "Focus on efficiency, switching speed, thermal performance, and cost.",
            ["SiC", "IGBT", "Inverter Technology", "EV Inverter"]
        ),
        SearchDocument(
            "doc004",
            "DC-DC Converter Topology for HV to LV Conversion",
            "Overview of DC-DC converter topologies used to step down high voltage battery packs to low voltage systems in electric vehicles.",
            ["DC-DC Converter", "HV to LV", "Power Electronics", "EV Systems"]
        ),
        SearchDocument(
            "doc005",
            "400V vs 800V Battery Architecture Trade-offs",
            "Comparison of 400V and 800V battery architectures in electric vehicles, including impacts on charging speed, efficiency, and component cost.",
            ["Battery Architecture", "400V", "800V", "EV Battery"]
        ),
        SearchDocument(
            "doc006",
            "Cell-to-Pack (CTP) Battery Design",
            "Innovations in Cell-to-Pack battery design that eliminate modules to improve energy density, reduce weight, and simplify manufacturing.",
            ["Cell-to-Pack", "Battery Design", "Energy Density", "Manufacturing"]
        ),
        SearchDocument(
            "doc007",
            "Battery Management System (BMS) Cell Balancing",
            "Techniques for cell balancing in battery management systems to ensure longevity and safety of lithium-ion battery packs.",
            ["BMS", "Cell Balancing", "Battery Safety", "Lithium-ion"]
        ),
        SearchDocument(
            "doc008",
            "Battery Thermal Management System Design",
            "Design strategies for battery thermal management to maintain optimal operating temperatures and extend battery life.",
            ["Battery Thermal Management", "Cooling", "Heating", "Battery Life"]
        ),
        SearchDocument(
            "doc009",
            "Motor and Inverter Thermal Management",
            "Approaches to thermal management for electric motors and inverters to improve reliability and performance under various operating conditions.",
            ["Thermal Management", "Motor Cooling", "Inverter Cooling", "Reliability"]
        ),
        SearchDocument(
            "doc010",
            "Regenerative Braking Strategy and Blending",
            "Methods for blending regenerative and friction braking in electric vehicles to maximize energy recovery and ensure safety.",
            ["Regenerative Braking", "Braking Strategy", "Energy Recovery", "Safety"]
        ),
        SearchDocument(
            "doc011",
            "EV Charging Standards and Connector Types",
            "Overview of electric vehicle charging standards including CCS, CHAdeMO, and Tesla connectors with their specifications and compatibility.",
            ["EV Charging", "Standards", "Connectors", "CCS", "CHAdeMO", "Tesla"]
        ),
        SearchDocument(
            "doc012",
            "DC Fast Charging Protocol and Battery Thermal Pre-Conditioning",
            "Protocols for DC fast charging and techniques for pre-conditioning battery temperature to optimize charging speed and battery health.",
            ["DC Fast Charging", "Battery Pre-Conditioning", "Charging Protocols", "Battery Health"]
        ),
        SearchDocument(
            "doc013",
            "EV Range Estimation and Energy Consumption Modeling",
            "Models and algorithms to estimate electric vehicle range based on driving conditions, battery state, and energy consumption patterns.",
            ["Range Estimation", "Energy Modeling", "EV Range", "Battery State"]
        ),
        SearchDocument(
            "doc014",
            "Field-Oriented Control (FOC) for PMSM Motors",
            "Implementation and benefits of Field-Oriented Control techniques for precise torque and speed control of PMSM motors.",
            ["FOC", "PMSM", "Motor Control", "Torque Control"]
        ),
        SearchDocument(
            "doc015",
            "Direct Torque Control (DTC) for Induction Motors",
            "Direct Torque Control methods for induction motors providing fast dynamic response and robustness in EV applications.",
            ["DTC", "Induction Motor", "Motor Control", "Dynamic Response"]
        ),
        SearchDocument(
            "doc016",
            "Electric Powertrain Packaging and Weight Distribution",
            "Strategies for packaging electric powertrain components and optimizing vehicle weight distribution for performance and efficiency.",
            ["Powertrain Packaging", "Weight Distribution", "EV Design", "Performance"]
        ),
        SearchDocument(
            "doc017",
            "High-Voltage Power Distribution Architecture",
            "Design considerations for high-voltage power distribution systems in electric vehicles ensuring safety and efficiency.",
            ["High-Voltage", "Power Distribution", "EV Architecture", "Safety"]
        ),
        SearchDocument(
            "doc018",
            "Hairpin Winding Technology for Stator Design",
            "Advantages and manufacturing considerations of hairpin winding technology in stator design for improved motor performance.",
            ["Hairpin Winding", "Stator Design", "Motor Performance", "Manufacturing"]
        ),
        SearchDocument(
            "doc019",
            "Advanced Cooling Techniques for SiC Inverters",
            "Exploration of cooling solutions tailored for Silicon Carbide inverters to handle high switching frequencies and thermal loads.",
            ["SiC Inverter", "Cooling", "Thermal Management", "Power Electronics"]
        ),
        SearchDocument(
            "doc020",
            "Battery State of Health (SOH) Estimation Methods",
            "Techniques for estimating battery state of health to predict remaining useful life and schedule maintenance.",
            ["Battery SOH", "Estimation", "Battery Life", "Maintenance"]
        ),
        SearchDocument(
            "doc021",
            "Impact of Battery Voltage on EV Safety Systems",
            "How battery voltage levels influence the design and operation of safety systems in electric vehicles.",
            ["Battery Voltage", "Safety Systems", "EV Safety", "High Voltage"]
        ),
        SearchDocument(
            "doc022",
            "Torque Ripple Minimization in PMSM Motors",
            "Methods to reduce torque ripple in PMSM motors for smoother operation and reduced noise.",
            ["Torque Ripple", "PMSM", "Motor Smoothness", "Noise Reduction"]
        ),
        SearchDocument(
            "doc023",
            "Integration of Regenerative Braking with ABS and ESC",
            "Techniques for integrating regenerative braking systems with Anti-lock Braking System (ABS) and Electronic Stability Control (ESC).",
            ["Regenerative Braking", "ABS", "ESC", "Braking Integration"]
        ),
        SearchDocument(
            "doc024",
            "Optimization of DC-DC Converter Efficiency in EVs",
            "Design and control strategies to maximize efficiency of DC-DC converters in electric vehicles.",
            ["DC-DC Converter", "Efficiency", "Power Electronics", "EV Systems"]
        ),
        SearchDocument(
            "doc025",
            "Thermal Runaway Prevention in Lithium-ion Batteries",
            "Approaches to detect and prevent thermal runaway events in lithium-ion battery packs.",
            ["Thermal Runaway", "Battery Safety", "Lithium-ion", "Prevention"]
        ),
        SearchDocument(
            "doc026",
            "Advanced Field Weakening Techniques for IPM Motors",
            "Field weakening control strategies to extend speed range of Interior Permanent Magnet motors without sacrificing torque.",
            ["Field Weakening", "IPM Motor", "Speed Control", "Motor Performance"]
        ),
        SearchDocument(
            "doc027",
            "High-Voltage Connector Design for 800V Battery Systems",
            "Design challenges and solutions for connectors used in 800V high-voltage battery architectures.",
            ["High-Voltage Connector", "800V Battery", "Connector Design", "EV Systems"]
        ),
        SearchDocument(
            "doc028",
            "Battery Pack Structural Design for Crash Safety",
            "Engineering battery pack structures to withstand crash impacts and protect cells in electric vehicles.",
            ["Battery Pack", "Crash Safety", "Structural Design", "EV Safety"]
        ),
        SearchDocument(
            "doc029",
            "SiC MOSFET Gate Driver Design Considerations",
            "Key design aspects of gate drivers for Silicon Carbide MOSFETs to optimize switching performance and reliability.",
            ["SiC MOSFET", "Gate Driver", "Switching", "Power Electronics"]
        ),
        SearchDocument(
            "doc030",
            "Energy Recovery Optimization in Urban Driving Cycles",
            "Strategies to maximize regenerative braking energy recovery in stop-and-go urban driving conditions.",
            ["Energy Recovery", "Regenerative Braking", "Urban Driving", "Efficiency"]
        ),
    ]
    for doc in docs:
        index.add_document(doc)