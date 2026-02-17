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
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_doc_tfs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.k1 = k1
        self.b = b
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            tf_counter = Counter(tokens)
            for term, freq in tf_counter.items():
                self.term_doc_tfs[doc.id][term] = freq
                self.term_doc_freqs[term] += 1
            self.total_docs += 1
            self._recompute_avg_doc_length()
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for doc_id, doc in self.documents.items():
            score_bm25 = self._score_bm25(doc_id, query_terms)
            score_tfidf = self._score_tfidf(doc_id, query_terms)
            total_score = 0.7 * score_bm25 + 0.3 * score_tfidf
            total_score *= doc.weight
            if total_score > 0:
                doc_scores[doc_id] = total_score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freqs),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _recompute_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf_counter = self.term_doc_tfs.get(doc_id, {})
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vec = self._tfidf_cache[doc_id]
        else:
            tfidf_vec = {}
            tf_counter = self.term_doc_tfs.get(doc_id, {})
            doc_len = self.doc_lengths.get(doc_id, 1)
            for term, tf in tf_counter.items():
                tf_norm = tf / doc_len
                idf = self._compute_idf(term)
                tfidf_vec[term] = tf_norm * idf
            self._tfidf_cache[doc_id] = tfidf_vec
        score = 0.0
        for term in query_terms:
            score += tfidf_vec.get(term, 0.0)
        return score

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        for term in query_terms:
            snippet = re.sub(r'\b(%s)\b' % re.escape(term), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                _search_index_instance = SearchIndex()
                _seed_documents(_search_index_instance)
    return _search_index_instance

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "CT Fatigue Life Prediction - Low-Cycle Fatigue",
            "Predicting coiled tubing fatigue life using low-cycle fatigue models. Includes stress analysis, load cycles, and material properties for CT string longevity.",
            ["fatigue", "life", "prediction", "low-cycle", "stress", "material"],
            1.0
        ),
        SearchDocument(
            2,
            "CT String Design - OD Selection and Wall Thickness",
            "Guidelines for selecting coiled tubing outer diameter and wall thickness for optimal performance. Covers collapse pressure, yield strength, and operational safety.",
            ["string design", "OD", "wall thickness", "collapse", "yield"],
            1.0
        ),
        SearchDocument(
            3,
            "Downhole Motor Selection for CTD - PDM Sizing",
            "Criteria for selecting positive displacement motors (PDM) for coiled tubing drilling. Includes torque, flow rate, and motor length considerations.",
            ["motor selection", "PDM", "torque", "flow rate", "CTD"],
            1.0
        ),
        SearchDocument(
            4,
            "Weight Transfer in Horizontal CTD - Friction and Buckling",
            "Analysis of weight transfer in horizontal coiled tubing drilling. Discusses friction, buckling, and drag forces affecting CT string movement.",
            ["weight transfer", "friction", "buckling", "horizontal", "drag"],
            1.0
        ),
        SearchDocument(
            5,
            "CT Drilling BHA Design - Orienting Tool, MWD, Check Valve",
            "Designing bottom hole assemblies (BHA) for CT drilling. Includes orienting tools, measurement while drilling (MWD), and check valve integration.",
            ["BHA", "design", "orienting tool", "MWD", "check valve"],
            1.0
        ),
        SearchDocument(
            6,
            "CT Milling Operations - Window Milling and Junk Milling",
            "Procedures for window milling and junk milling using coiled tubing. Covers milling tool selection, operational parameters, and debris removal.",
            ["milling", "window", "junk", "tool selection", "debris"],
            1.0
        ),
        SearchDocument(
            7,
            "CT Acid Stimulation - Matrix Acidizing via CT",
            "Matrix acidizing operations using coiled tubing. Discusses acid types, pumping rates, and zonal isolation for effective stimulation.",
            ["acid stimulation", "matrix acidizing", "coiled tubing", "pumping", "zonal isolation"],
            1.0
        ),
        SearchDocument(
            8,
            "CT Nitrogen Kickoff - Gas Lift Unloading",
            "Gas lift unloading techniques with coiled tubing and nitrogen. Includes kickoff procedures, pressure management, and well productivity enhancement.",
            ["nitrogen", "kickoff", "gas lift", "unloading", "pressure"],
            1.0
        ),
        SearchDocument(
            9,
            "CT Cleanout Operations - Sand and Debris Removal",
            "Sand and debris removal during coiled tubing cleanout operations. Covers fluid selection, circulation rates, and tool deployment strategies.",
            ["cleanout", "sand", "debris", "removal", "fluid selection"],
            1.0
        ),
        SearchDocument(
            10,
            "CT Real-Time Monitoring - WHP, Pump Pressure, Weight",
            "Real-time monitoring of wellhead pressure (WHP), pump pressure, and CT weight during operations. Includes sensor integration and data analytics.",
            ["real-time", "monitoring", "WHP", "pump pressure", "weight"],
            1.0
        ),
        SearchDocument(
            11,
            "CT Reel Management and Inspection - ICoTA Guidelines",
            "Best practices for coiled tubing reel management and inspection based on ICoTA guidelines. Covers reel storage, inspection frequency, and defect detection.",
            ["reel management", "inspection", "ICoTA", "storage", "defect"],
            1.0
        ),
        SearchDocument(
            12,
            "CT Connector and Dimple Technology",
            "Overview of connector and dimple technology for coiled tubing. Discusses connector types, dimple formation, and reliability considerations.",
            ["connector", "dimple", "technology", "reliability", "coiled tubing"],
            1.0
        ),
        SearchDocument(
            13,
            "CT Well Intervention in Horizontal Wells - Extended Reach",
            "Techniques for coiled tubing well intervention in horizontal wells. Includes extended reach operations, friction reduction, and tool conveyance.",
            ["well intervention", "horizontal", "extended reach", "friction", "conveyance"],
            1.0
        ),
        SearchDocument(
            14,
            "CT Drilling Rate of Penetration - ROP Optimization",
            "Optimizing rate of penetration (ROP) in coiled tubing drilling. Covers bit selection, motor parameters, and drilling fluid properties.",
            ["rate of penetration", "ROP", "optimization", "bit", "fluid"],
            1.0
        ),
        SearchDocument(
            15,
            "CT Drilling Fluid Selection - Drilling Mud Properties",
            "Selecting drilling fluids for coiled tubing drilling. Discusses mud properties, viscosity, density, and fluid loss control.",
            ["drilling fluid", "mud", "properties", "viscosity", "density"],
            1.0
        ),
        SearchDocument(
            16,
            "CT Drilling Directional Control - Slide Drilling with Bent Motor",
            "Directional control in coiled tubing drilling using slide drilling and bent motors. Includes toolface orientation and trajectory planning.",
            ["directional control", "slide drilling", "bent motor", "toolface", "trajectory"],
            1.0
        ),
        SearchDocument(
            17,
            "CT Drilling Well Control - Kick Detection and Response",
            "Well control procedures for coiled tubing drilling. Covers kick detection, shut-in protocols, and pressure management.",
            ["well control", "kick detection", "response", "shut-in", "pressure"],
            1.0
        ),
        SearchDocument(
            18,
            "CT String Fatigue Analysis - Load History Tracking",
            "Tracking load history for coiled tubing string fatigue analysis. Includes cycle counting, stress range evaluation, and fatigue damage calculation.",
            ["fatigue", "load history", "cycle counting", "stress range", "damage"],
            1.0
        ),
        SearchDocument(
            19,
            "CTD BHA Hydraulics - Flow Path Optimization",
            "Optimizing hydraulics in coiled tubing drilling BHA. Discusses flow path design, pressure drops, and tool efficiency.",
            ["BHA", "hydraulics", "flow path", "optimization", "pressure drop"],
            1.0
        ),
        SearchDocument(
            20,
            "CTD Extended Reach - Weight Transfer and Friction",
            "Managing weight transfer and friction in extended reach coiled tubing drilling. Includes drag reduction techniques and string selection.",
            ["extended reach", "weight transfer", "friction", "drag reduction", "string selection"],
            1.0
        ),
        SearchDocument(
            21,
            "CTD Window Milling - Tool Selection and Parameters",
            "Selecting tools and parameters for window milling in coiled tubing drilling. Covers milling tool types, operational limits, and debris management.",
            ["window milling", "tool selection", "parameters", "debris management", "CTD"],
            1.0
        ),
        SearchDocument(
            22,
            "CTD Acidizing - Fluid Compatibility and Pumping",
            "Ensuring fluid compatibility and proper pumping rates in coiled tubing drilling acidizing operations. Includes acid selection and corrosion control.",
            ["acidizing", "fluid compatibility", "pumping", "corrosion", "CTD"],
            1.0
        ),
        SearchDocument(
            23,
            "CTD Kickoff Operations - Nitrogen and Gas Lift",
            "Kickoff operations in coiled tubing drilling using nitrogen and gas lift. Discusses pressure control and well startup procedures.",
            ["kickoff", "nitrogen", "gas lift", "pressure control", "startup"],
            1.0
        ),
        SearchDocument(
            24,
            "CTD Cleanout - Sand and Debris Circulation",
            "Circulating sand and debris during coiled tubing drilling cleanout. Covers fluid selection, tool deployment, and operational best practices.",
            ["cleanout", "sand", "debris", "circulation", "tool deployment"],
            1.0
        ),
        SearchDocument(
            25,
            "CTD Real-Time Data Acquisition - Sensors and Telemetry",
            "Acquiring real-time data in coiled tubing drilling using sensors and telemetry. Includes WHP, pump pressure, and weight monitoring.",
            ["real-time", "data acquisition", "sensors", "telemetry", "monitoring"],
            1.0
        ),
        SearchDocument(
            26,
            "CTD Reel Inspection - Defect Detection and Guidelines",
            "Inspecting coiled tubing reels for defects using industry guidelines. Covers reel management, inspection frequency, and defect classification.",
            ["reel inspection", "defect detection", "guidelines", "management", "classification"],
            1.0
        ),
        SearchDocument(
            27,
            "CT Connector Reliability - Dimple Technology",
            "Assessing connector reliability in coiled tubing using dimple technology. Discusses connector types, formation methods, and operational impact.",
            ["connector", "reliability", "dimple", "technology", "formation"],
            1.0
        ),
        SearchDocument(
            28,
            "CTD Well Intervention - Horizontal Well Techniques",
            "Intervening in horizontal wells using coiled tubing drilling. Includes extended reach, friction reduction, and tool conveyance strategies.",
            ["well intervention", "horizontal", "extended reach", "friction", "conveyance"],
            1.0
        ),
        SearchDocument(
            29,
            "CTD ROP Optimization - Bit and Motor Selection",
            "Optimizing rate of penetration in coiled tubing drilling through bit and motor selection. Covers drilling fluid properties and operational parameters.",
            ["ROP optimization", "bit selection", "motor", "drilling fluid", "parameters"],
            1.0
        ),
        SearchDocument(
            30,
            "CTD Mud Selection - Fluid Loss and Viscosity Control",
            "Selecting mud for coiled tubing drilling with focus on fluid loss and viscosity control. Includes density management and mud additives.",
            ["mud selection", "fluid loss", "viscosity", "density", "additives"],
            1.0
        ),
        SearchDocument(
            31,
            "CTD Directional Drilling - Bent Motor and Toolface",
            "Directional drilling in coiled tubing using bent motors and toolface orientation. Discusses slide drilling and trajectory planning.",
            ["directional drilling", "bent motor", "toolface", "slide drilling", "trajectory"],
            1.0
        ),
        SearchDocument(
            32,
            "CTD Well Control - Kick Detection and Shut-in",
            "Well control in coiled tubing drilling with emphasis on kick detection and shut-in protocols. Includes pressure management and response strategies.",
            ["well control", "kick detection", "shut-in", "pressure management", "response"],
            1.0
        ),
        SearchDocument(
            33,
            "CTD Fatigue Monitoring - Real-Time Stress Analysis",
            "Monitoring coiled tubing fatigue in real-time using stress analysis. Includes load tracking, cycle counting, and damage prediction.",
            ["fatigue monitoring", "real-time", "stress analysis", "load tracking", "cycle counting"],
            1.0
        ),
        SearchDocument(
            34,
            "CTD BHA Design - Tool Integration and Reliability",
            "Designing coiled tubing drilling BHA with integrated tools for reliability. Includes orienting tool, MWD, and check valve selection.",
            ["BHA design", "tool integration", "reliability", "orienting tool", "MWD"],
            1.0
        ),
        SearchDocument(
            35,
            "CTD Milling Operations - Junk Removal and Tool Selection",
            "Junk removal during coiled tubing drilling milling operations. Covers tool selection, operational parameters, and debris management.",
            ["milling operations", "junk removal", "tool selection", "parameters", "debris"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)