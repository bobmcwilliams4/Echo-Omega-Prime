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
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.total_docs = 0

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
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
            self._update_avg_doc_length()

    def _update_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id][term]
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id][term]
            if doc_len == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = []
        for doc_id in self.documents:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        indices = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indices:
            return content[:160] + ('...' if len(content) > 160 else '')
        start = max(indices[0] - 10, 0)
        end = min(indices[0] + 20, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
            'bm25_k1': self.k1,
            'bm25_b': self.b
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
        SearchDocument(1, "Unbalance Diagnosis Fundamentals",
            "Unbalance in rotating machinery is a primary cause of excessive vibration. Diagnosis involves measuring amplitude and phase at running speed. Typical symptoms include high vibration at 1X RPM, phase consistency, and response to balancing.",
            ["unbalance_diagnosis"], 1.2),
        SearchDocument(2, "Misalignment Diagnosis Techniques",
            "Misalignment between coupled machines causes vibration at 1X and 2X RPM. Diagnosis uses vibration spectrum, shaft measurements, and thermal imaging. Corrective actions include realignment and coupling checks.",
            ["misalignment_diagnosis"], 1.1),
        SearchDocument(3, "Bearing Defect Frequencies Reference",
            "Rolling element bearing defects generate characteristic frequencies: BPFO, BPFI, BSF, FTF. Vibration analysis identifies these using FFT and envelope detection. Early detection prevents catastrophic failures.",
            ["bearing_defect_frequencies"], 1.3),
        SearchDocument(4, "Vibration Severity Standards Overview",
            "ISO 10816 and API 670 provide vibration severity guidelines for machinery. Severity is classified by RMS velocity and displacement. Standards help assess machine health and maintenance needs.",
            ["vibration_severity_standards"], 1.0),
        SearchDocument(5, "Resonance Identification in Rotors",
            "Resonance occurs when excitation frequency matches natural frequency. Symptoms include rapid amplitude increase and phase shift. Modal analysis and run-up tests are used for identification.",
            ["resonance_identification"], 1.2),
        SearchDocument(6, "Gear Mesh Frequency Analysis",
            "Gear mesh frequencies are calculated as number of teeth times rotational speed. Sidebands indicate gear defects. FFT spectrum analysis reveals mesh frequency and harmonics.",
            ["gear_mesh_frequency_analysis"], 1.1),
        SearchDocument(7, "Mechanical Looseness Diagnosis",
            "Mechanical looseness produces harmonics and subharmonics in vibration spectrum. Symptoms include erratic amplitude changes and phase instability. Inspection and tightening are required.",
            ["mechanical_looseness_diagnosis"], 1.0),
        SearchDocument(8, "Rotor Dynamics: Critical Speeds",
            "Critical speeds are natural frequencies of rotors. Crossing critical speed causes resonance. Analysis involves Campbell diagrams and modal testing.",
            ["rotor_dynamics_critical_speeds"], 1.3),
        SearchDocument(9, "Balancing Methodology for Rotors",
            "Balancing reduces unbalance forces. Methods include single-plane and two-plane balancing. Procedure involves measurement, calculation of correction weights, and verification.",
            ["balancing_methodology"], 1.2),
        SearchDocument(10, "Proximity Probe Installation Guide",
            "Proximity probes measure shaft displacement. Installation requires correct gap, orientation, and calibration. API 670 standards recommend probe placement and wiring.",
            ["proximity_probe_installation"], 1.1),
        SearchDocument(11, "Accelerometer Selection and Mounting",
            "Accelerometers are selected based on frequency range, sensitivity, and mounting method. Mounting affects signal quality: stud, adhesive, and magnetic mounts are common.",
            ["accelerometer_selection_mounting"], 1.0),
        SearchDocument(12, "Oil Whirl and Whip Instability",
            "Oil whirl and whip are fluid-induced instabilities in hydrodynamic bearings. Symptoms include vibration at sub-synchronous frequencies. Diagnosis uses spectrum and orbit analysis.",
            ["oil_whirl_whip_instability"], 1.2),
        SearchDocument(13, "FFT Spectrum Analysis in Vibration",
            "FFT transforms time waveform into frequency spectrum. Peaks at characteristic frequencies indicate faults. Analysis includes windowing, averaging, and spectral interpretation.",
            ["fft_spectrum_analysis"], 1.3),
        SearchDocument(14, "Time Waveform Analysis Techniques",
            "Time waveform analysis reveals transient events and impacts. Useful for diagnosing bearing faults, looseness, and gear defects. Complementary to FFT analysis.",
            ["time_waveform_analysis"], 1.1),
        SearchDocument(15, "Orbit Analysis and Shaft Centerline",
            "Orbit plots visualize shaft movement in bearings. Centerline analysis detects rubs, misalignment, and instability. Data from proximity probes is used.",
            ["orbit_analysis_shaft_centerline"], 1.2),
        SearchDocument(16, "Electrical Motor Vibration Causes",
            "Electrical motors exhibit vibration due to electrical and mechanical sources. Causes include unbalance, misalignment, rotor eccentricity, and electromagnetic forces.",
            ["electrical_motor_vibration"], 1.0),
        SearchDocument(17, "Advanced Unbalance Diagnosis",
            "Advanced techniques include multi-plane balancing, influence coefficient method, and modal analysis. Used for complex rotors and high-speed machinery.",
            ["unbalance_diagnosis"], 1.4),
        SearchDocument(18, "Laser Alignment for Misalignment Correction",
            "Laser alignment tools provide precise shaft alignment. Reduces vibration and increases equipment life. Procedure includes measurement, adjustment, and verification.",
            ["misalignment_diagnosis"], 1.2),
        SearchDocument(19, "Bearing Defect Frequency Calculation",
            "Defect frequencies depend on bearing geometry and speed. Calculations use ball diameter, pitch diameter, and number of rolling elements. Software tools automate analysis.",
            ["bearing_defect_frequencies"], 1.1),
        SearchDocument(20, "API 670 Vibration Severity Criteria",
            "API 670 defines vibration limits for critical machinery. Criteria are based on RMS velocity and displacement. Used for monitoring and protection systems.",
            ["vibration_severity_standards"], 1.2),
        SearchDocument(21, "Modal Testing for Resonance Identification",
            "Modal testing determines natural frequencies and mode shapes. Used to identify resonance and optimize rotor design. Techniques include impact testing and shaker excitation.",
            ["resonance_identification"], 1.3),
        SearchDocument(22, "Gear Defect Diagnosis via Sideband Analysis",
            "Sidebands around gear mesh frequency indicate defects like eccentricity and wear. Analysis uses FFT and time synchronous averaging.",
            ["gear_mesh_frequency_analysis"], 1.2),
        SearchDocument(23, "Types of Mechanical Looseness",
            "Mechanical looseness can be structural, component, or foundation related. Each type produces distinct vibration patterns. Diagnosis involves inspection and vibration analysis.",
            ["mechanical_looseness_diagnosis"], 1.1),
        SearchDocument(24, "Campbell Diagram for Critical Speed Prediction",
            "Campbell diagrams plot natural frequencies against speed. Used to predict critical speeds and avoid resonance during operation.",
            ["rotor_dynamics_critical_speeds"], 1.2),
        SearchDocument(25, "Field Balancing Procedures",
            "Field balancing involves measuring vibration, calculating correction weights, and applying them to the rotor. Ensures minimal unbalance and smooth operation.",
            ["balancing_methodology"], 1.1),
        SearchDocument(26, "Proximity Probe Troubleshooting",
            "Common issues include incorrect gap, electrical noise, and calibration errors. Troubleshooting involves checking wiring, signal quality, and probe placement.",
            ["proximity_probe_installation"], 1.0),
        SearchDocument(27, "Accelerometer Frequency Response",
            "Frequency response determines accelerometer suitability for vibration analysis. High-frequency accelerometers are used for bearing and gear fault detection.",
            ["accelerometer_selection_mounting"], 1.2),
        SearchDocument(28, "Oil Whip Instability Case Study",
            "Case study of oil whip in a steam turbine. Diagnosis involved orbit analysis, spectrum review, and corrective action on bearing design.",
            ["oil_whirl_whip_instability"], 1.3),
        SearchDocument(29, "FFT Windowing and Averaging",
            "Windowing reduces spectral leakage in FFT analysis. Averaging improves signal-to-noise ratio. Common windows: Hanning, Hamming, Blackman.",
            ["fft_spectrum_analysis"], 1.1),
        SearchDocument(30, "Time Waveform for Impact Detection",
            "Impact events appear as spikes in time waveform. Analysis helps identify bearing and gear defects missed in frequency spectrum.",
            ["time_waveform_analysis"], 1.2),
        SearchDocument(31, "Orbit Plot Interpretation",
            "Orbit plots reveal shaft behavior: circular, elliptical, or chaotic. Used for diagnosing rubs, misalignment, and instability.",
            ["orbit_analysis_shaft_centerline"], 1.1),
        SearchDocument(32, "Electrical Motor Vibration Monitoring",
            "Continuous monitoring detects early signs of faults. Techniques include vibration sensors, spectrum analysis, and thermal imaging.",
            ["electrical_motor_vibration"], 1.2),
        SearchDocument(33, "Balancing High-Speed Rotors",
            "High-speed rotors require precision balancing. Methods include modal balancing and trial weight method. Measurement accuracy is critical.",
            ["balancing_methodology"], 1.3),
        SearchDocument(34, "Proximity Probe Calibration Procedure",
            "Calibration ensures accurate displacement measurement. Procedure includes gap setting, signal verification, and reference checks.",
            ["proximity_probe_installation"], 1.2),
        SearchDocument(35, "Accelerometer Mounting Best Practices",
            "Proper mounting maximizes signal fidelity. Stud mounting is preferred for permanent installations. Avoid loose or contaminated surfaces.",
            ["accelerometer_selection_mounting"], 1.3),
        SearchDocument(36, "Oil Whirl Instability Prevention",
            "Prevention involves proper bearing design, lubrication control, and monitoring. Early detection via vibration analysis is essential.",
            ["oil_whirl_whip_instability"], 1.1),
        SearchDocument(37, "FFT for Gear Mesh Faults",
            "FFT reveals gear mesh frequency and sidebands. Used for diagnosing gear wear, eccentricity, and misalignment.",
            ["fft_spectrum_analysis"], 1.2),
        SearchDocument(38, "Time Waveform for Looseness Diagnosis",
            "Looseness produces repetitive impacts in time waveform. Analysis distinguishes between structural and component looseness.",
            ["time_waveform_analysis"], 1.3),
        SearchDocument(39, "Orbit Analysis for Oil Whip Detection",
            "Orbit plots show characteristic patterns during oil whip instability. Combined with spectrum analysis for diagnosis.",
            ["orbit_analysis_shaft_centerline", "oil_whirl_whip_instability"], 1.4),
        SearchDocument(40, "Electrical Motor Vibration Case Study",
            "Case study on vibration due to rotor eccentricity. Diagnosis involved spectrum analysis, balancing, and realignment.",
            ["electrical_motor_vibration"], 1.3),
        SearchDocument(41, "Rotor Dynamics: Campbell Diagram Interpretation",
            "Interpreting Campbell diagrams helps avoid resonance and optimize rotor design. Used in turbine and compressor engineering.",
            ["rotor_dynamics_critical_speeds"], 1.1),
        SearchDocument(42, "Gear Mesh Frequency Calculation Example",
            "Example calculation for gear mesh frequency: 30 teeth at 1500 RPM yields 750 Hz. Used for diagnostic and design purposes.",
            ["gear_mesh_frequency_analysis"], 1.3),
        SearchDocument(43, "Mechanical Looseness Case Study",
            "Case study of looseness in pump foundation. Diagnosis involved vibration analysis, inspection, and corrective action.",
            ["mechanical_looseness_diagnosis"], 1.2),
        SearchDocument(44, "Bearing Defect Frequency Software Tools",
            "Software tools automate calculation of bearing defect frequencies. Input parameters: geometry, speed, and load. Results used in predictive maintenance.",
            ["bearing_defect_frequencies"], 1.2),
        SearchDocument(45, "Balancing Methodology: Influence Coefficient",
            "Influence coefficient method allows multi-plane balancing. Used for complex rotors and high-speed machinery.",
            ["balancing_methodology"], 1.4),
        SearchDocument(46, "Proximity Probe Installation for Turbines",
            "Turbine proximity probe installation requires precise gap setting, orientation, and vibration isolation.",
            ["proximity_probe_installation"], 1.3),
        SearchDocument(47, "Accelerometer Selection for Gear Faults",
            "Gear faults require accelerometers with high-frequency response and robust mounting.",
            ["accelerometer_selection_mounting"], 1.1),
        SearchDocument(48, "Oil Whirl Instability in Compressors",
            "Compressors are prone to oil whirl instability. Diagnosis uses vibration spectrum and orbit analysis.",
            ["oil_whirl_whip_instability"], 1.2),
        SearchDocument(49, "FFT Spectrum for Bearing Faults",
            "FFT spectrum reveals characteristic bearing defect frequencies. Envelope analysis enhances detection.",
            ["fft_spectrum_analysis"], 1.4),
        SearchDocument(50, "Time Waveform for Resonance Detection",
            "Resonance produces sustained oscillations in time waveform. Analysis helps identify natural frequencies.",
            ["time_waveform_analysis", "resonance_identification"], 1.2),
    ]
    for doc in docs:
        idx.add_document(doc)