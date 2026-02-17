import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, id: str, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
        self.doc_freqs: Dict[str, int] = defaultdict(int)  # document frequency per term
        self.term_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)  # term_freqs[doc_id][term] = freq
        self.doc_lengths: Dict[str, int] = {}  # length in tokens per document
        self.avg_doc_length: float = 0.0
        self.N: int = 0  # total number of documents
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old doc data
                old_terms = self.term_freqs.get(doc.id, {})
                for term in old_terms:
                    self.doc_freqs[term] -= 1
                    if self.doc_freqs[term] <= 0:
                        del self.doc_freqs[term]
                del self.term_freqs[doc.id]
                del self.doc_lengths[doc.id]
                self.N -= 1

            tokens = self._tokenize(doc.title + " " + doc.content)
            term_count = Counter(tokens)
            self.documents[doc.id] = doc
            self.term_freqs[doc.id] = dict(term_count)
            self.doc_lengths[doc.id] = len(tokens)
            self.N += 1
            for term in term_count:
                self.doc_freqs[term] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        scores: Dict[str, float] = defaultdict(float)
        idf_values = {term: self._compute_idf(term) for term in query_terms}

        for doc_id, doc in self.documents.items():
            score = self._score_bm25(doc_id, query_terms, idf_values)
            if score > 0:
                scores[doc_id] = score * doc.weight

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.N,
                "average_document_length": self.avg_doc_length,
                "unique_terms": len(self.doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

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

    def _score_bm25(self, doc_id: str, query_terms: List[str], idf_values: Dict[str, float]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        freqs = self.term_freqs.get(doc_id, {})
        for term in query_terms:
            tf = freqs.get(term, 0)
            if tf == 0:
                continue
            idf = idf_values.get(term, 0)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length) if self.avg_doc_length > 0 else tf + self.k1
            score += idf * tf * (self.k1 + 1) / denom
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_length: int = 150) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            for match in re.finditer(r'\b' + re.escape(term) + r'\b', content_lower):
                positions.append(match.start())
        if not positions:
            snippet = content[:snippet_length].strip()
            if len(content) > snippet_length:
                snippet += "..."
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_length // 4, 0)
        end_pos = start_pos + snippet_length
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet += "..."
        return snippet

_singleton_index: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _singleton_index
    with _singleton_lock:
        if _singleton_index is None:
            _singleton_index = SearchIndex()
            _preseed_documents(_singleton_index)
        return _singleton_index

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="P0xxx_OBD-II_Powertrain_Codes",
            title="OBD-II P0xxx Powertrain Codes Overview",
            content=(
                "The OBD-II standard defines P0xxx codes for powertrain diagnostics. "
                "These codes indicate issues related to engine, transmission, and emissions control systems. "
                "Understanding P0xxx codes is essential for accurate fault diagnosis and repair."
            ),
            tags=["OBD-II", "Powertrain", "Diagnostics", "P0xxx"]
        ),
        SearchDocument(
            id="P030x_Engine_Misfire_Diagnosis",
            title="Engine Misfire Diagnosis - P030x Codes",
            content=(
                "P030x codes indicate engine misfires on specific cylinders. "
                "Diagnosis involves checking ignition coils, spark plugs, fuel injectors, and compression. "
                "Misfires can cause rough running, increased emissions, and catalytic converter damage."
            ),
            tags=["Engine", "Misfire", "P030x", "Ignition", "Fuel"]
        ),
        SearchDocument(
            id="GDI_Systems_Basics",
            title="Gasoline Direct Injection (GDI) Systems",
            content=(
                "GDI systems inject fuel directly into the combustion chamber, improving efficiency and power. "
                "Common issues include carbon buildup on intake valves and injector failures. "
                "Proper diagnosis requires fuel pressure and injector pulse analysis."
            ),
            tags=["GDI", "Fuel Injection", "Engine", "Diagnostics"]
        ),
        SearchDocument(
            id="Catalytic_Converter_Diagnostics",
            title="Catalytic Converter Diagnostics",
            content=(
                "Catalytic converters reduce harmful emissions by converting exhaust gases. "
                "Failures cause increased emissions and P0420 codes. "
                "Diagnosis includes temperature sensors, backpressure tests, and oxygen sensor analysis."
            ),
            tags=["Catalytic Converter", "Emissions", "Oxygen Sensor", "P0420"]
        ),
        SearchDocument(
            id="MAF_Sensor_Diagnosis",
            title="Mass Airflow (MAF) Sensor Diagnosis",
            content=(
                "The MAF sensor measures the amount of air entering the engine. "
                "Faulty MAF sensors cause rough idle, poor fuel economy, and drivability issues. "
                "Diagnosis involves voltage signal checks and sensor cleaning."
            ),
            tags=["MAF Sensor", "Airflow", "Engine", "Diagnostics"]
        ),
        SearchDocument(
            id="Turbocharger_Diagnostics",
            title="Turbocharger Diagnostics and Troubleshooting",
            content=(
                "Turbochargers increase engine power by forcing more air into the combustion chamber. "
                "Common issues include boost leaks, wastegate failures, and bearing wear. "
                "Diagnosis requires boost pressure testing and visual inspections."
            ),
            tags=["Turbocharger", "Boost", "Engine", "Diagnostics"]
        ),
        SearchDocument(
            id="VVT_Systems_Overview",
            title="Variable Valve Timing (VVT) Systems",
            content=(
                "VVT systems optimize engine performance by adjusting valve timing. "
                "Failures cause rough running and reduced power. "
                "Diagnosis includes camshaft position sensor checks and oil control valve testing."
            ),
            tags=["VVT", "Valve Timing", "Engine", "Diagnostics"]
        ),
        SearchDocument(
            id="Diesel_Engine_Diagnostics",
            title="Diesel Engine Diagnostics Fundamentals",
            content=(
                "Diesel engines require specialized diagnostics including glow plug testing, fuel system checks, and compression tests. "
                "Common codes include injector circuit faults and EGR system issues."
            ),
            tags=["Diesel", "Engine", "Diagnostics", "Glow Plug", "EGR"]
        ),
        SearchDocument(
            id="Engine_Cooling_System_Diagnostics",
            title="Engine Cooling System Diagnostics",
            content=(
                "The cooling system prevents engine overheating. "
                "Diagnosis includes thermostat operation, radiator pressure testing, and coolant temperature sensor checks."
            ),
            tags=["Cooling System", "Thermostat", "Radiator", "Diagnostics"]
        ),
        SearchDocument(
            id="Hybrid_Powertrain_Basics",
            title="Hybrid Vehicle Powertrain Basics",
            content=(
                "Hybrid powertrains combine internal combustion engines with electric motors. "
                "Diagnostics include battery state of charge, inverter operation, and regenerative braking systems."
            ),
            tags=["Hybrid", "Powertrain", "Electric Motor", "Diagnostics"]
        ),
        SearchDocument(
            id="No_Start_Diagnosis_Decision_Tree",
            title="No-Start Diagnosis Decision Tree",
            content=(
                "A systematic approach to diagnosing no-start conditions includes checking battery voltage, starter operation, fuel delivery, and ignition systems."
            ),
            tags=["No-Start", "Diagnosis", "Battery", "Starter", "Fuel", "Ignition"]
        ),
        SearchDocument(
            id="Oxygen_Sensor_Operation_Diagnosis",
            title="Oxygen Sensor Operation and Diagnosis",
            content=(
                "Oxygen sensors monitor exhaust oxygen levels to optimize fuel mixture. "
                "Failures cause poor fuel economy and emissions. "
                "Diagnosis includes voltage signal analysis and heater circuit testing."
            ),
            tags=["Oxygen Sensor", "Emissions", "Fuel Mixture", "Diagnostics"]
        ),
        SearchDocument(
            id="EGR_System_Diagnosis",
            title="Exhaust Gas Recirculation (EGR) System Diagnosis",
            content=(
                "The EGR system reduces NOx emissions by recirculating exhaust gases. "
                "Common failures include valve sticking and sensor faults. "
                "Diagnosis involves vacuum tests and sensor voltage checks."
            ),
            tags=["EGR", "Emissions", "Diagnostics"]
        ),
        SearchDocument(
            id="EVAP_System_Diagnosis",
            title="Evaporative Emission Control (EVAP) System Diagnosis",
            content=(
                "The EVAP system prevents fuel vapors from escaping. "
                "Leaks cause check engine lights and P0440 codes. "
                "Diagnosis includes smoke testing and purge valve operation checks."
            ),
            tags=["EVAP", "Emissions", "Leak Detection", "Diagnostics"]
        ),
        SearchDocument(
            id="Crankshaft_Camshaft_Position_Sensors",
            title="Crankshaft and Camshaft Position Sensors",
            content=(
                "These sensors provide engine position data for ignition and fuel injection timing. "
                "Failures cause misfires and no-start conditions. "
                "Diagnosis includes signal waveform analysis and resistance checks."
            ),
            tags=["Crankshaft Sensor", "Camshaft Sensor", "Ignition", "Diagnostics"]
        ),
        SearchDocument(
            id="Ignition_Coil_Diagnosis",
            title="Ignition Coil Diagnosis (Coil-on-Plug)",
            content=(
                "Coil-on-plug ignition systems deliver high voltage directly to spark plugs. "
                "Failures cause misfires and rough running. "
                "Diagnosis involves primary and secondary resistance testing and scan tool data."
            ),
            tags=["Ignition Coil", "Coil-on-Plug", "Misfire", "Diagnostics"]
        ),
        SearchDocument(
            id="OBD-II_Scan_Tool_Usage",
            title="Using OBD-II Scan Tools for Diagnostics",
            content=(
                "OBD-II scan tools read and clear diagnostic trouble codes, view live data, and perform system tests. "
                "Proper use accelerates fault diagnosis and repair."
            ),
            tags=["OBD-II", "Scan Tool", "Diagnostics"]
        ),
        SearchDocument(
            id="Fuel_Injector_Diagnostics",
            title="Fuel Injector Diagnostics and Testing",
            content=(
                "Fuel injectors deliver precise fuel amounts to cylinders. "
                "Failures cause misfires and poor performance. "
                "Testing includes resistance checks, pulse width analysis, and flow testing."
            ),
            tags=["Fuel Injector", "Engine", "Diagnostics"]
        ),
        SearchDocument(
            id="Intake_Manifold_Leak_Diagnosis",
            title="Intake Manifold Leak Diagnosis",
            content=(
                "Leaks in the intake manifold cause rough idle and lean conditions. "
                "Diagnosis includes smoke testing and vacuum gauge analysis."
            ),
            tags=["Intake Manifold", "Leak", "Diagnostics"]
        ),
        SearchDocument(
            id="Exhaust_System_Diagnostics",
            title="Exhaust System Diagnostics",
            content=(
                "Exhaust leaks and restrictions affect engine performance and emissions. "
                "Diagnosis includes visual inspection and backpressure testing."
            ),
            tags=["Exhaust", "Diagnostics"]
        ),
        SearchDocument(
            id="Battery_and_Charging_System_Diagnostics",
            title="Battery and Charging System Diagnostics",
            content=(
                "Proper battery and charging system operation is critical for vehicle function. "
                "Testing includes voltage, load, and alternator output checks."
            ),
            tags=["Battery", "Charging System", "Diagnostics"]
        ),
        SearchDocument(
            id="Throttle_Body_Diagnostics",
            title="Throttle Body Diagnostics and Cleaning",
            content=(
                "Throttle body issues cause poor idle and hesitation. "
                "Cleaning and sensor checks restore proper operation."
            ),
            tags=["Throttle Body", "Idle", "Diagnostics"]
        ),
        SearchDocument(
            id="Camshaft_Timing_Chain_Diagnostics",
            title="Camshaft Timing Chain Diagnostics",
            content=(
                "Timing chain wear or failure causes engine noise and performance loss. "
                "Diagnosis includes tensioner checks and timing alignment."
            ),
            tags=["Timing Chain", "Camshaft", "Diagnostics"]
        ),
        SearchDocument(
            id="Vacuum_System_Diagnostics",
            title="Vacuum System Diagnostics",
            content=(
                "Vacuum leaks cause drivability issues and emissions problems. "
                "Diagnosis includes smoke testing and vacuum gauge readings."
            ),
            tags=["Vacuum", "Leak", "Diagnostics"]
        ),
        SearchDocument(
            id="Ignition_System_Basics",
            title="Ignition System Basics and Troubleshooting",
            content=(
                "The ignition system provides spark for combustion. "
                "Troubleshooting includes coil, distributor, and spark plug testing."
            ),
            tags=["Ignition", "Spark", "Diagnostics"]
        ),
        SearchDocument(
            id="Fuel_Pump_Diagnostics",
            title="Fuel Pump Diagnostics and Testing",
            content=(
                "Fuel pump failures cause no-start and performance issues. "
                "Testing includes pressure and current draw measurements."
            ),
            tags=["Fuel Pump", "Fuel System", "Diagnostics"]
        ),
        SearchDocument(
            id="Engine_Oil_System_Diagnostics",
            title="Engine Oil System Diagnostics",
            content=(
                "Proper oil pressure and quality are vital for engine longevity. "
                "Diagnosis includes pressure sensor checks and oil analysis."
            ),
            tags=["Engine Oil", "Diagnostics"]
        ),
        SearchDocument(
            id="Engine_Sensors_Overview",
            title="Engine Sensors Overview and Diagnostics",
            content=(
                "Engine sensors provide critical data for engine management. "
                "Common sensors include MAP, TPS, coolant temp, and knock sensors."
            ),
            tags=["Engine Sensors", "Diagnostics"]
        ),
    ]
    for doc in docs:
        index.add_document(doc)