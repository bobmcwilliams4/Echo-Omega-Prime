import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

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
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}
        self._preseeded = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freq[term] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        score = 0.0
        doc_length = self.doc_lengths[doc_id]
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_length / (self.avg_doc_length if self.avg_doc_length > 0 else 1))
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        if doc_id in self._tfidf_cache:
            tfidf = self._tfidf_cache[doc_id]
        else:
            tf = self.term_freqs[doc_id]
            doc_length = self.doc_lengths[doc_id]
            tfidf = {}
            for term in tf:
                norm_tf = tf[term] / doc_length if doc_length > 0 else 0
                idf = self._compute_idf(term)
                tfidf[term] = norm_tf * idf
            self._tfidf_cache[doc_id] = tfidf
        score = sum(tfidf.get(term, 0.0) for term in query_terms)
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(doc_id, query_terms)
                doc_scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        doc_scores.sort(key=lambda x: x.score, reverse=True)
        return doc_scores[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str], max_len: int = 160) -> str:
        content = self.documents[doc_id].content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:max_len]
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + 30, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        return snippet[:max_len] + ('...' if len(snippet) > max_len else '')

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
            'documents': list(self.documents.keys())
        }

    def _preseed_documents(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(1, "Primary Voltage Selection for Oilfield Power Distribution",
                "Guidelines for selecting primary voltage in oilfield electrical systems. Factors include distance, load size, transformer ratings, and NEC requirements.",
                ["primary voltage", "NEC", "transformer", "oilfield"], 1.0),
            SearchDocument(2, "Secondary Voltage Selection and Transformer Sizing",
                "Secondary voltage selection impacts transformer sizing and load compatibility. Typical voltages: 480V, 600V, 4160V. Sizing based on kVA, impedance, and tap changing.",
                ["secondary voltage", "transformer sizing", "kVA", "impedance"], 1.0),
            SearchDocument(3, "Transformer Impedance and Tap Changing in Oilfield Applications",
                "Transformer impedance affects voltage regulation and fault current. Tap changers allow voltage adjustment under load. Oilfield transformers require robust tap changing mechanisms.",
                ["impedance", "tap changer", "oilfield", "transformer"], 1.0),
            SearchDocument(4, "Motor Control Center (MCC) Breaker and Starter Selection",
                "Selecting MCC breakers and starters for oilfield motors involves sizing for load, short-circuit protection, and coordination. Consider NEMA and IEC standards.",
                ["MCC", "breaker", "starter", "motor", "NEMA", "IEC"], 1.0),
            SearchDocument(5, "Variable Frequency Drive (VFD) Application for ESP and Rod Pump Motors",
                "VFDs control speed and torque for ESP and rod pump motors. Benefits include energy savings, soft start, and improved reliability. Selection based on motor specs and load profile.",
                ["VFD", "ESP", "rod pump", "motor", "energy savings"], 1.0),
            SearchDocument(6, "Hazardous Area Classification: NEC 500, 505 and API RP 500",
                "Hazardous area classification per NEC 500, 505, and API RP 500 defines explosion risk zones. Class I, Division 1 and 2 areas require special equipment.",
                ["hazardous area", "NEC 500", "NEC 505", "API RP 500", "explosion"], 1.0),
            SearchDocument(7, "Explosion-Proof Equipment for Class I, Division 1 and 2 Areas",
                "Explosion-proof equipment is required in Class I, Division 1 and 2 hazardous locations. Equipment must withstand internal explosions without igniting external atmosphere.",
                ["explosion-proof", "Class I", "Division 1", "Division 2", "hazardous"], 1.0),
            SearchDocument(8, "Intrinsically Safe Barriers: Zener and Shunt Diode Application",
                "Intrinsically safe barriers, including Zener and shunt diode types, limit energy in hazardous areas. Used for instrumentation and control circuits.",
                ["intrinsically safe", "Zener", "shunt diode", "barrier", "hazardous"], 1.0),
            SearchDocument(9, "Power Cable Sizing: Ampacity and Voltage Drop per NEC 310",
                "Cable sizing per NEC 310 considers ampacity, voltage drop, insulation type, and ambient temperature. Proper sizing ensures safe and efficient operation.",
                ["cable sizing", "ampacity", "voltage drop", "NEC 310"], 1.0),
            SearchDocument(10, "Grounding System: Electrode and Grid Resistance",
                "Grounding systems use electrodes and grids to achieve low resistance paths for fault currents. Testing and design per IEEE 80 and NEC 250.",
                ["grounding", "electrode", "grid", "resistance", "IEEE 80", "NEC 250"], 1.0),
            SearchDocument(11, "Lightning Protection System: Rod, Conductor, and Ground Integration",
                "Lightning protection integrates rods, conductors, and grounding to safely dissipate strikes. Design per NFPA 780 and IEC 62305 standards.",
                ["lightning protection", "rod", "conductor", "ground", "NFPA 780", "IEC 62305"], 1.0),
            SearchDocument(12, "Switchgear: Medium Voltage, Vacuum and SF6 Breaker Application",
                "Medium voltage switchgear uses vacuum and SF6 breakers for arc interruption. Selection based on voltage, current, and environmental factors.",
                ["switchgear", "medium voltage", "vacuum breaker", "SF6 breaker"], 1.0),
            SearchDocument(13, "Protective Relays: Overcurrent, Differential, and Ground Fault",
                "Protective relays detect overcurrent, differential, and ground fault conditions. Coordination ensures selective tripping and system reliability.",
                ["protective relay", "overcurrent", "differential", "ground fault"], 1.0),
            SearchDocument(14, "Power Quality: Harmonics and Total Harmonic Distortion (THD) per IEEE 519",
                "Power quality issues include harmonics and THD. IEEE 519 provides limits for harmonic distortion in oilfield power systems.",
                ["power quality", "harmonics", "THD", "IEEE 519"], 1.0),
            SearchDocument(15, "Power Factor Correction: Capacitor Bank Application",
                "Capacitor banks correct power factor in oilfield electrical systems. Proper sizing reduces losses and improves voltage stability.",
                ["power factor", "correction", "capacitor bank", "voltage stability"], 1.0),
            SearchDocument(16, "Generator Set Sizing: Diesel and Natural Gas Applications",
                "Generator sizing for oilfield applications considers load profile, starting currents, and fuel type. Diesel and natural gas generators have different sizing criteria.",
                ["generator", "diesel", "natural gas", "sizing", "load profile"], 1.0),
            SearchDocument(17, "Automatic Transfer Switch (ATS) and Load Shedding",
                "ATS provides automatic switching between power sources. Load shedding prioritizes critical loads during outages. Integration improves reliability.",
                ["ATS", "load shedding", "automatic transfer", "critical loads"], 1.0),
            SearchDocument(18, "UPS: Uninterruptible Power Supply and Battery Sizing",
                "UPS systems provide backup power. Battery sizing depends on load, runtime, and environmental conditions. Selection per IEEE 1184 and NEC 480.",
                ["UPS", "battery sizing", "backup power", "IEEE 1184", "NEC 480"], 1.0),
            SearchDocument(19, "Solar Panel Application for Off-Grid Oilfield Power",
                "Solar panels supply off-grid power for remote oilfield sites. System design includes panel sizing, battery storage, and inverter selection.",
                ["solar panel", "off-grid", "battery storage", "inverter"], 1.0),
            SearchDocument(20, "Electrical One-Line Diagram and Coordination Study",
                "One-line diagrams provide system overview. Coordination studies ensure proper relay and breaker operation for selective protection.",
                ["one-line diagram", "coordination study", "relay", "breaker"], 1.0),
            SearchDocument(21, "Arc Flash Analysis and Incident Energy Calculation per NFPA 70E",
                "Arc flash analysis calculates incident energy and PPE requirements. NFPA 70E outlines procedures for oilfield electrical safety.",
                ["arc flash", "incident energy", "NFPA 70E", "PPE"], 1.0),
            SearchDocument(22, "Transformer Cooling Methods: Oil, Air, and Forced Cooling",
                "Transformer cooling methods include oil, air, and forced cooling. Selection depends on load, ambient temperature, and reliability requirements.",
                ["transformer", "cooling", "oil", "air", "forced cooling"], 1.0),
            SearchDocument(23, "Cable Tray and Raceway Selection for Oilfield Installations",
                "Cable trays and raceways organize and protect cables. Selection based on load, environmental conditions, and NEC 392 requirements.",
                ["cable tray", "raceway", "NEC 392", "oilfield"], 1.0),
            SearchDocument(24, "Short Circuit and Coordination Analysis in Oilfield Power Systems",
                "Short circuit analysis determines fault levels. Coordination analysis ensures proper relay and breaker operation for system protection.",
                ["short circuit", "coordination", "relay", "breaker"], 1.0),
            SearchDocument(25, "Load Flow Study and Voltage Regulation in Oilfield Distribution",
                "Load flow studies analyze voltage regulation and power flow. Results guide transformer tap settings and capacitor placement.",
                ["load flow", "voltage regulation", "tap setting", "capacitor"], 1.0),
            SearchDocument(26, "Cable Insulation Types and Selection Criteria",
                "Cable insulation types include PVC, XLPE, and EPR. Selection based on voltage, temperature, and chemical exposure.",
                ["cable insulation", "PVC", "XLPE", "EPR"], 1.0),
            SearchDocument(27, "Electrical Safety in Oilfield Environments: PPE and Procedures",
                "Electrical safety in oilfields requires PPE, lockout/tagout, and hazard identification. Procedures per OSHA and NFPA 70E.",
                ["electrical safety", "PPE", "lockout", "OSHA", "NFPA 70E"], 1.0),
            SearchDocument(28, "Medium Voltage Cable Termination and Testing",
                "Medium voltage cable termination requires proper techniques and testing. Standards include IEEE 404 and IEC 60502.",
                ["medium voltage", "cable termination", "testing", "IEEE 404", "IEC 60502"], 1.0),
            SearchDocument(29, "Electrical Load Calculation for Oilfield Facilities",
                "Load calculation includes motors, lighting, and process equipment. Accurate calculation ensures proper sizing of transformers and generators.",
                ["load calculation", "motors", "lighting", "transformer", "generator"], 1.0),
            SearchDocument(30, "Remote Monitoring and SCADA Integration in Oilfield Power Systems",
                "SCADA systems enable remote monitoring and control of oilfield power. Integration improves reliability and maintenance.",
                ["SCADA", "remote monitoring", "oilfield", "power system"], 1.0),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

def get_search_index() -> SearchIndex:
    if not hasattr(get_search_index, "_instance"):
        get_search_index._instance = SearchIndex()
        get_search_index._instance._preseed_documents()
    return get_search_index._instance