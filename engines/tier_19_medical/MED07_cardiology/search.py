import math
import threading
import heapq
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
        self.documents: Dict[int, SearchDocument] = dict()
        self.doc_lengths: Dict[int, int] = dict()
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Counter] = dict()
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = dict()
        self.k1 = 1.5
        self.b = 0.75

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            for term in tf:
                self.term_doc_freq[term] += 1
            self.documents[doc.id] = doc
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / max(1, self.total_docs)
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        n = self.total_docs
        idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
            score += idf * numerator / denominator
        doc = self.documents[doc_id]
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_length = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_length
            idf = self._compute_idf(term)
            score += tf_norm * idf
        doc = self.documents[doc_id]
        return score * doc.weight

    def search(self, query: str, limit: int = 10, method: str = "bm25") -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_ids = set()
        for term in query_terms:
            for doc_id in self.term_freqs:
                if term in self.term_freqs[doc_id]:
                    candidate_ids.add(doc_id)
        heap: List[Tuple[float, int]] = []
        for doc_id in candidate_ids:
            if method == "bm25":
                score = self._score_bm25(query_terms, doc_id)
            elif method == "tfidf":
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                heapq.heappush(heap, (-score, doc_id))
        results = []
        for _ in range(min(limit, len(heap))):
            neg_score, doc_id = heapq.heappop(heap)
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, -neg_score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        indexes = [i for i, t in enumerate(tokens) if t in query_terms]
        if not indexes:
            return ' '.join(tokens[:30]) + ('...' if len(tokens) > 30 else '')
        start = max(0, indexes[0] - 10)
        end = min(len(tokens), indexes[0] + 20)
        snippet = ' '.join(tokens[start:end])
        return snippet + ('...' if end < len(tokens) else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            "total_docs": self.total_docs,
            "avg_doc_length": self.avg_doc_length,
            "unique_terms": len(self.term_doc_freq),
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

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "STEMI Diagnosis: ECG Criteria",
            "ST-Elevation Myocardial Infarction (STEMI) is diagnosed by new ST elevation at the J point in two contiguous leads. Elevation thresholds: ≥2mm in men or ≥1.5mm in women in V2-V3, ≥1mm in other leads. Reciprocal changes and new LBBB may also indicate STEMI.",
            ["STEMI", "ECG", "Diagnosis"],
            1.0
        ),
        SearchDocument(
            2,
            "NSTEMI and Unstable Angina: Differentiation",
            "NSTEMI presents with elevated cardiac biomarkers but without ST elevation on ECG. Unstable angina has similar symptoms but normal biomarkers. Both are types of Acute Coronary Syndrome (ACS).",
            ["NSTEMI", "Unstable Angina", "ACS"],
            1.0
        ),
        SearchDocument(
            3,
            "Heart Failure Classification: HFrEF vs HFpEF",
            "Heart failure is classified by ejection fraction: HFrEF (<40%), HFpEF (≥50%), HFmrEF (41-49%). Symptoms include dyspnea, orthopnea, and edema. Diagnosis uses echocardiography and natriuretic peptides.",
            ["Heart Failure", "Classification", "Ejection Fraction"],
            1.0
        ),
        SearchDocument(
            4,
            "Heart Failure Staging: ACC/AHA Stages",
            "Stages: A (risk factors), B (structural disease, no symptoms), C (symptoms), D (refractory). Management includes lifestyle, medications (ACEi, beta-blockers), and device therapy.",
            ["Heart Failure", "Staging", "ACC/AHA"],
            1.0
        ),
        SearchDocument(
            5,
            "Atrial Fibrillation: Rate vs Rhythm Control",
            "AF management includes rate control (beta-blockers, calcium channel blockers), rhythm control (antiarrhythmics, ablation), and anticoagulation based on CHA2DS2-VASc score.",
            ["Atrial Fibrillation", "Management", "Anticoagulation"],
            1.0
        ),
        SearchDocument(
            6,
            "Anticoagulation in AF: CHA2DS2-VASc and HAS-BLED",
            "Stroke risk in AF is estimated by CHA2DS2-VASc score. Anticoagulation indicated for score ≥2. Bleeding risk assessed by HAS-BLED. Options: warfarin, DOACs.",
            ["Atrial Fibrillation", "Anticoagulation", "Risk Scores"],
            1.0
        ),
        SearchDocument(
            7,
            "Bundle Branch Block: ECG Interpretation",
            "Right bundle branch block (RBBB): rsR' in V1, wide S in V6. Left bundle branch block (LBBB): broad QRS, absent Q in V6, deep S in V1. LBBB may mask STEMI.",
            ["Bundle Branch Block", "ECG", "Interpretation"],
            1.0
        ),
        SearchDocument(
            8,
            "Aortic Stenosis: Assessment and Management",
            "Aortic stenosis presents with systolic murmur, crescendo-decrescendo at right upper sternal border. Severe AS: valve area <1.0 cm², mean gradient >40 mmHg. Management: valve replacement for symptomatic severe AS.",
            ["Aortic Stenosis", "Assessment", "Management"],
            1.0
        ),
        SearchDocument(
            9,
            "Mitral Regurgitation: Assessment and Management",
            "Mitral regurgitation causes holosystolic murmur at apex, radiates to axilla. Severe MR: regurgitant volume >60 mL, effective regurgitant orifice >0.4 cm². Management: repair or replacement for symptomatic severe MR.",
            ["Mitral Regurgitation", "Assessment", "Management"],
            1.0
        ),
        SearchDocument(
            10,
            "QT Prolongation and Torsades Risk",
            "QT prolongation (>450ms men, >470ms women) increases risk of Torsades de Pointes. Causes: drugs (antiarrhythmics, macrolides), hypokalemia, hypomagnesemia. Management: remove offending agent, correct electrolytes, magnesium sulfate for Torsades.",
            ["QT Prolongation", "Torsades", "Risk"],
            1.0
        ),
        SearchDocument(
            11,
            "Ventricular Tachycardia: Classification",
            "VT classified as monomorphic (uniform QRS) or polymorphic (variable QRS). Sustained VT >30s or requiring intervention. Management: antiarrhythmics, ICD for structural heart disease.",
            ["Ventricular Tachycardia", "Classification", "Management"],
            1.0
        ),
        SearchDocument(
            12,
            "Cardiac Biomarkers in ACS",
            "Troponin I/T is the most sensitive and specific biomarker for myocardial injury. CK-MB used for reinfarction. BNP/NT-proBNP for heart failure. Serial measurements improve diagnostic accuracy.",
            ["Cardiac Biomarkers", "ACS", "Diagnosis"],
            1.0
        ),
        SearchDocument(
            13,
            "Framingham Risk Score: Primary Prevention",
            "Framingham Risk Score estimates 10-year cardiovascular risk using age, cholesterol, BP, smoking, diabetes. Guides statin therapy and lifestyle interventions.",
            ["Framingham Risk Score", "Prevention", "Risk Assessment"],
            1.0
        ),
        SearchDocument(
            14,
            "Cardiogenic Shock: Diagnosis and Management",
            "Cardiogenic shock: hypotension, low cardiac output, end-organ hypoperfusion. Causes: MI, severe HF. Diagnosis: clinical, echo, hemodynamics. Management: inotropes, vasopressors, mechanical support (IABP, ECMO).",
            ["Cardiogenic Shock", "Diagnosis", "Management"],
            1.0
        ),
        SearchDocument(
            15,
            "Acute Pericarditis: Diagnosis and Management",
            "Acute pericarditis: chest pain, pericardial friction rub, diffuse ST elevation, PR depression. Etiologies: viral, idiopathic. Management: NSAIDs, colchicine, avoid steroids unless refractory.",
            ["Acute Pericarditis", "Diagnosis", "Management"],
            1.0
        ),
        SearchDocument(
            16,
            "Cardiac Tamponade: Recognition and Management",
            "Tamponade: hypotension, JVD, muffled heart sounds (Beck's triad), pulsus paradoxus. Diagnosis: echo shows diastolic collapse. Management: urgent pericardiocentesis.",
            ["Cardiac Tamponade", "Recognition", "Management"],
            1.0
        ),
        SearchDocument(
            17,
            "Hypertrophic Cardiomyopathy: Diagnosis",
            "HCM: asymmetric septal hypertrophy, systolic murmur increases with Valsalva. Diagnosis: echo, genetic testing. Risk stratification for sudden death: family history, syncope, wall thickness, arrhythmias.",
            ["Hypertrophic Cardiomyopathy", "Diagnosis", "Sudden Death Risk"],
            1.0
        ),
        SearchDocument(
            18,
            "Sudden Death Risk in HCM",
            "Risk factors: prior cardiac arrest, family history, unexplained syncope, LV wall thickness >30mm, nonsustained VT. ICD indicated for high-risk patients.",
            ["Hypertrophic Cardiomyopathy", "Sudden Death", "ICD"],
            1.0
        ),
        SearchDocument(
            19,
            "STEMI Management: Reperfusion Strategies",
            "Primary PCI within 90 minutes is preferred for STEMI. Fibrinolysis if PCI unavailable within 120 minutes. Adjuncts: antiplatelets, anticoagulants, statins, beta-blockers.",
            ["STEMI", "Management", "Reperfusion"],
            1.0
        ),
        SearchDocument(
            20,
            "NSTEMI Management: Early Invasive vs Conservative",
            "NSTEMI management: risk stratification (TIMI, GRACE), early invasive for high-risk, conservative for low-risk. Antiplatelets, anticoagulants, statins, beta-blockers.",
            ["NSTEMI", "Management", "Risk Stratification"],
            1.0
        ),
        SearchDocument(
            21,
            "Heart Failure: Diuretics and Volume Management",
            "Loop diuretics relieve congestion in HF. Monitor electrolytes and renal function. Add thiazides for resistance. Avoid over-diuresis.",
            ["Heart Failure", "Diuretics", "Volume Management"],
            1.0
        ),
        SearchDocument(
            22,
            "Atrial Fibrillation: Catheter Ablation",
            "Catheter ablation indicated for symptomatic AF refractory to medical therapy. Pulmonary vein isolation is standard. Risks: tamponade, stroke.",
            ["Atrial Fibrillation", "Catheter Ablation", "Management"],
            1.0
        ),
        SearchDocument(
            23,
            "Bundle Branch Block: Clinical Implications",
            "LBBB may indicate underlying cardiac disease and mask STEMI. RBBB often benign but may be seen in pulmonary embolism. New BBB in ACS increases risk.",
            ["Bundle Branch Block", "Clinical Implications", "ACS"],
            1.0
        ),
        SearchDocument(
            24,
            "Aortic Stenosis: Symptoms and Timing for Surgery",
            "Symptoms: angina, syncope, heart failure. Surgery indicated for symptomatic severe AS or asymptomatic with LV dysfunction. TAVR for high-risk patients.",
            ["Aortic Stenosis", "Symptoms", "Surgery"],
            1.0
        ),
        SearchDocument(
            25,
            "Mitral Regurgitation: Surgical vs Medical Management",
            "Medical management: diuretics, afterload reduction. Surgery for symptomatic severe MR or LV dysfunction. Timing critical to prevent irreversible damage.",
            ["Mitral Regurgitation", "Surgical Management", "Medical Management"],
            1.0
        ),
        SearchDocument(
            26,
            "QT Prolongation: Drug-Induced Causes",
            "Common drugs causing QT prolongation: antiarrhythmics (amiodarone, sotalol), macrolides, fluoroquinolones, antipsychotics. Monitor ECG and electrolytes.",
            ["QT Prolongation", "Drug-Induced", "ECG"],
            1.0
        ),
        SearchDocument(
            27,
            "Ventricular Tachycardia: Acute Management",
            "Stable VT: antiarrhythmics (amiodarone, lidocaine). Unstable VT: synchronized cardioversion. Pulseless VT: defibrillation. ICD for secondary prevention.",
            ["Ventricular Tachycardia", "Acute Management", "ICD"],
            1.0
        ),
        SearchDocument(
            28,
            "Cardiac Biomarkers: Serial Measurement",
            "Serial troponin measurements improve ACS diagnosis. Rise and fall pattern confirms acute injury. CK-MB useful for reinfarction.",
            ["Cardiac Biomarkers", "Serial Measurement", "ACS"],
            1.0
        ),
        SearchDocument(
            29,
            "Framingham Risk Score: Calculation Example",
            "Example: 55-year-old male, total cholesterol 220, HDL 45, BP 140, smoker, no diabetes. 10-year risk calculated using Framingham tables.",
            ["Framingham Risk Score", "Calculation", "Example"],
            1.0
        ),
        SearchDocument(
            30,
            "Cardiogenic Shock: Mechanical Support",
            "Mechanical support options: intra-aortic balloon pump (IABP), Impella, ECMO. Indications: refractory shock, bridge to recovery or transplant.",
            ["Cardiogenic Shock", "Mechanical Support", "Management"],
            1.0
        ),
        SearchDocument(
            31,
            "Acute Pericarditis: ECG Findings",
            "ECG: diffuse ST elevation, PR depression. Differentiate from STEMI: pericarditis lacks reciprocal changes and localizes to multiple leads.",
            ["Acute Pericarditis", "ECG", "Diagnosis"],
            1.0
        ),
        SearchDocument(
            32,
            "Cardiac Tamponade: Pulsus Paradoxus",
            "Pulsus paradoxus: drop in systolic BP >10mmHg during inspiration. Seen in tamponade, severe asthma. Pathophysiology: impaired ventricular filling.",
            ["Cardiac Tamponade", "Pulsus Paradoxus", "Pathophysiology"],
            1.0
        ),
        SearchDocument(
            33,
            "Hypertrophic Cardiomyopathy: Genetic Testing",
            "Genetic testing recommended for HCM patients and first-degree relatives. Common genes: MYH7, MYBPC3. Counseling important for risk stratification.",
            ["Hypertrophic Cardiomyopathy", "Genetic Testing", "Risk Stratification"],
            1.0
        ),
        SearchDocument(
            34,
            "STEMI: Complications and Prognosis",
            "Complications: arrhythmias, heart failure, cardiogenic shock, pericarditis, mechanical defects. Prognosis depends on infarct size, reperfusion, comorbidities.",
            ["STEMI", "Complications", "Prognosis"],
            1.0
        ),
        SearchDocument(
            35,
            "NSTEMI: Complications and Prognosis",
            "Complications: recurrent ischemia, arrhythmias, heart failure. Prognosis improved with early invasive management and secondary prevention.",
            ["NSTEMI", "Complications", "Prognosis"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)