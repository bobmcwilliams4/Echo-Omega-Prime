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
        self.N = 0
        self.avgdl = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._re_token = re.compile(r"\b\w+\b", re.UNICODE)

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in self._re_token.findall(text)]

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.doc_freqs[term] += 1
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_tokens: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        score = 0.0
        doc = self.documents[doc_id]
        for term in query_tokens:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            score += idf * freq * (self.k1 + 1) / denom
        return score * doc.weight

    def _score_tfidf(self, query_tokens: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        score = 0.0
        doc = self.documents[doc_id]
        for term in query_tokens:
            if term not in tf:
                continue
            tf_norm = tf[term] / dl
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        doc_scores = []
        for doc_id in self.documents:
            if method == "bm25":
                score = self._score_bm25(query_tokens, doc_id)
            elif method == "tfidf":
                score = self._score_tfidf(query_tokens, doc_id)
            else:
                raise ValueError("Unknown scoring method: %s" % method)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_tokens)
                doc_scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        doc_scores.sort(key=lambda x: x.score, reverse=True)
        return doc_scores[:limit]

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], snippet_len: int = 32) -> str:
        content_tokens = self._tokenize(doc.content)
        positions = [i for i, t in enumerate(content_tokens) if t in query_tokens]
        if not positions:
            return doc.content[:160] + "..." if len(doc.content) > 160 else doc.content
        start = max(positions[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(content_tokens))
        snippet = " ".join(content_tokens[start:end])
        for qt in set(query_tokens):
            snippet = re.sub(rf"\b({re.escape(qt)})\b", r"<b>\1</b>", snippet, flags=re.IGNORECASE)
        return snippet

    def get_stats(self) -> Dict[str, float]:
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avgdl,
            "vocab_size": len(self.doc_freqs)
        }

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "PEM Electrolysis for Green Hydrogen",
            "Proton Exchange Membrane (PEM) electrolysis enables high-purity green hydrogen production using renewable electricity. PEM cells use a solid polymer electrolyte and operate at low temperatures.",
            ["PEM", "Electrolysis", "Green Hydrogen", "Renewable"],
            1.0
        ),
        SearchDocument(
            2,
            "Steam Methane Reforming with CCS",
            "Blue hydrogen is produced via Steam Methane Reforming (SMR) with Carbon Capture and Storage (CCS), reducing CO2 emissions compared to conventional SMR.",
            ["Blue Hydrogen", "SMR", "CCS", "CO2"],
            1.0
        ),
        SearchDocument(
            3,
            "Alkaline Electrolysis Technology",
            "Alkaline electrolysis uses a liquid electrolyte (KOH or NaOH) and nickel-based electrodes for hydrogen production. It is a mature and cost-effective technology.",
            ["Alkaline", "Electrolysis", "Hydrogen"],
            1.0
        ),
        SearchDocument(
            4,
            "Type IV Hydrogen Storage at 700 bar",
            "Type IV composite pressure vessels are used for compressed hydrogen storage at 700 bar, offering high gravimetric efficiency and safety for mobility applications.",
            ["Type IV", "Storage", "700 bar", "Compressed Hydrogen"],
            1.0
        ),
        SearchDocument(
            5,
            "Liquid Hydrogen Storage and Boil-Off",
            "Liquid hydrogen (LH2) is stored at cryogenic temperatures. Boil-off losses must be managed through insulation and venting systems.",
            ["LH2", "Storage", "Boil-Off", "Cryogenic"],
            1.0
        ),
        SearchDocument(
            6,
            "PEM Fuel Cell MEA Structure",
            "The Membrane Electrode Assembly (MEA) in PEM fuel cells consists of a proton-conducting membrane, catalyst layers, and gas diffusion layers.",
            ["PEM", "Fuel Cell", "MEA", "Membrane"],
            1.0
        ),
        SearchDocument(
            7,
            "Solid Oxide Fuel Cell for Stationary Power",
            "SOFCs operate at high temperatures and can utilize a variety of fuels, making them suitable for stationary power generation with high electrical efficiency.",
            ["SOFC", "Fuel Cell", "Stationary Power"],
            1.0
        ),
        SearchDocument(
            8,
            "Hydrogen Pipeline Embrittlement (ASME B31.12)",
            "Hydrogen pipelines must comply with ASME B31.12 to mitigate embrittlement risks. Material selection and stress analysis are critical.",
            ["Pipeline", "Embrittlement", "ASME B31.12"],
            1.0
        ),
        SearchDocument(
            9,
            "Hydrogen Refueling Station Design (ISO 19880-1)",
            "ISO 19880-1 provides guidelines for hydrogen refueling station safety, performance, and design, including dispenser, storage, and compression systems.",
            ["Refueling Station", "ISO 19880-1", "Design"],
            1.0
        ),
        SearchDocument(
            10,
            "Hydrogen Safety Standards (NFPA 2)",
            "NFPA 2 outlines fire protection and safety requirements for hydrogen technologies, including storage, piping, and dispensing.",
            ["NFPA 2", "Safety", "Hydrogen"],
            1.0
        ),
        SearchDocument(
            11,
            "Levelized Cost of Hydrogen (LCOH) Analysis",
            "LCOH is a metric for comparing hydrogen production costs, accounting for capital, operational, and feedstock expenses over the system's lifetime.",
            ["LCOH", "Cost", "Analysis"],
            1.0
        ),
        SearchDocument(
            12,
            "Hydrogen Color Classification and Carbon Intensity",
            "Hydrogen is classified by color (green, blue, grey, etc.) based on production method and carbon intensity. Green hydrogen is renewable; blue uses CCS.",
            ["Color", "Classification", "Carbon Intensity"],
            1.0
        ),
        SearchDocument(
            13,
            "Solid-State Hydrogen Storage in Metal Hydrides",
            "Metal hydrides offer solid-state hydrogen storage with high volumetric density and reversible absorption/desorption.",
            ["Solid-State", "Storage", "Metal Hydrides"],
            1.0
        ),
        SearchDocument(
            14,
            "Hydrogen Fuel Quality (ISO 14687, SAE J2719)",
            "ISO 14687 and SAE J2719 specify hydrogen fuel quality standards for fuel cell vehicles, limiting impurities to protect MEA performance.",
            ["Fuel Quality", "ISO 14687", "SAE J2719"],
            1.0
        ),
        SearchDocument(
            15,
            "PEM Electrolyzer Stack Design",
            "PEM electrolyzer stacks are modular, enabling scalable green hydrogen production. Stack design impacts efficiency and durability.",
            ["PEM", "Electrolyzer", "Stack"],
            1.0
        ),
        SearchDocument(
            16,
            "CCS Technologies for Blue Hydrogen",
            "Carbon Capture and Storage (CCS) technologies include amine scrubbing, pressure swing adsorption, and geological sequestration for blue hydrogen plants.",
            ["CCS", "Blue Hydrogen", "Capture"],
            1.0
        ),
        SearchDocument(
            17,
            "Hydrogen Compression Methods",
            "Hydrogen is compressed using mechanical, ionic, or electrochemical compressors for storage and transport applications.",
            ["Compression", "Storage", "Transport"],
            1.0
        ),
        SearchDocument(
            18,
            "Hydrogen Purification Techniques",
            "Pressure Swing Adsorption (PSA), membrane separation, and cryogenic distillation are used to purify hydrogen for fuel cell use.",
            ["Purification", "PSA", "Membrane"],
            1.0
        ),
        SearchDocument(
            19,
            "Hydrogen Dispensing Protocols",
            "Hydrogen refueling follows SAE J2601 protocols for pressure, temperature, and flow rate to ensure safe and efficient vehicle fueling.",
            ["Dispensing", "SAE J2601", "Refueling"],
            1.0
        ),
        SearchDocument(
            20,
            "Hydrogen Embrittlement Mechanisms",
            "Hydrogen embrittlement can cause cracking in metals. Alloy selection and stress minimization are key mitigation strategies.",
            ["Embrittlement", "Metals", "Alloy"],
            1.0
        ),
        SearchDocument(
            21,
            "Hydrogen Storage System Thermal Management",
            "Thermal management is critical for high-pressure and cryogenic hydrogen storage to prevent overpressure and minimize losses.",
            ["Thermal Management", "Storage", "Cryogenic"],
            1.0
        ),
        SearchDocument(
            22,
            "Hydrogen Fuel Cell Vehicle Architecture",
            "Fuel cell vehicles integrate hydrogen storage, PEM fuel cells, power electronics, and electric drive systems for zero-emission transport.",
            ["Fuel Cell", "Vehicle", "Architecture"],
            1.0
        ),
        SearchDocument(
            23,
            "Hydrogen Pipeline Leak Detection",
            "Leak detection in hydrogen pipelines employs acoustic, fiber optic, and mass balance methods to ensure safety.",
            ["Pipeline", "Leak Detection", "Safety"],
            1.0
        ),
        SearchDocument(
            24,
            "Hydrogen Boil-Off Gas Management",
            "Boil-off gas from LH2 storage can be reliquefied, vented, or used for power generation to improve system efficiency.",
            ["Boil-Off", "LH2", "Management"],
            1.0
        ),
        SearchDocument(
            25,
            "Hydrogen Infrastructure Codes and Standards",
            "Codes and standards such as ASME B31.12, ISO 19880-1, and NFPA 2 govern hydrogen infrastructure design, operation, and safety.",
            ["Codes", "Standards", "Infrastructure"],
            1.0
        ),
        SearchDocument(
            26,
            "Alkaline Electrolyzer Stack Durability",
            "Stack durability in alkaline electrolyzers is influenced by electrode corrosion, separator degradation, and operational cycling.",
            ["Alkaline", "Electrolyzer", "Durability"],
            1.0
        ),
        SearchDocument(
            27,
            "Hydrogen Fuel Cell System Balance of Plant",
            "Balance of plant (BoP) includes compressors, humidifiers, and thermal management for optimal fuel cell system operation.",
            ["Fuel Cell", "BoP", "System"],
            1.0
        ),
        SearchDocument(
            28,
            "Hydrogen Storage in Metal-Organic Frameworks",
            "Metal-organic frameworks (MOFs) are being researched for high-capacity, reversible hydrogen storage at moderate pressures.",
            ["MOF", "Storage", "Hydrogen"],
            1.0
        ),
        SearchDocument(
            29,
            "Hydrogen Refueling Station Safety Systems",
            "Safety systems at hydrogen refueling stations include leak detection, emergency shutdown, and fire suppression per ISO 19880-1.",
            ["Refueling Station", "Safety", "ISO 19880-1"],
            1.0
        ),
        SearchDocument(
            30,
            "Hydrogen Fuel Quality Impacts on PEM MEA",
            "Impurities in hydrogen fuel can poison PEM MEA catalysts, reducing performance and durability. ISO 14687 sets impurity limits.",
            ["Fuel Quality", "PEM", "MEA"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)