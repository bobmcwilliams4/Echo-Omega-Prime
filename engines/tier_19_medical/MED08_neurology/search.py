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
        self.doc_tokens: Dict[int, List[str]] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.term_doc_tfs: Dict[int, Counter] = {}
        self.term_idf_cache: Dict[str, float] = {}
        self.avg_doc_length: float = 0.0
        self.lock = threading.Lock()
        self._doc_id_counter = 1

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self.lock:
            doc_id = self._doc_id_counter
            self._doc_id_counter += 1
            doc = SearchDocument(doc_id, title, content, tags, weight)
            self.documents[doc_id] = doc
            tokens = self._tokenize(content)
            self.doc_tokens[doc_id] = tokens
            self.doc_lengths[doc_id] = len(tokens)
            tf_counter = Counter(tokens)
            self.term_doc_tfs[doc_id] = tf_counter
            for term in tf_counter:
                self.term_doc_freqs[term] += 1
            self._update_avg_doc_length()
            self.term_idf_cache.clear()
            return doc_id

    def _update_avg_doc_length(self):
        total_length = sum(self.doc_lengths.values())
        num_docs = len(self.doc_lengths)
        self.avg_doc_length = total_length / num_docs if num_docs > 0 else 0.0

    def _compute_idf(self, term: str) -> float:
        if term in self.term_idf_cache:
            return self.term_idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freqs.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.term_idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        tf_counter = self.term_doc_tfs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator
        score *= self.documents[doc_id].weight
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf_counter = self.term_doc_tfs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            tf = tf_counter.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        score *= self.documents[doc_id].weight
        return score

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = []
        for doc_id in self.documents:
            if use_bm25:
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0.0:
                snippet = self._make_snippet(doc_id, query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str], snippet_len: int = 40) -> str:
        content = self.documents[doc_id].content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:snippet_len] + '...'
        start = max(positions[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b(' + re.escape(term) + r')\b', r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + '...'

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'num_unique_terms': len(self.term_doc_freqs)
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
        # Acute Ischemic Stroke tPA Eligibility
        ("tPA Eligibility Criteria for Acute Ischemic Stroke", 
         "tPA may be administered within 4.5 hours of symptom onset. Exclusion criteria include intracranial hemorrhage, recent surgery, severe hypertension, and active bleeding. Assess NIHSS and imaging before administration.", 
         ["stroke", "tPA", "eligibility"], 1.2),
        ("Contraindications to tPA in Stroke", 
         "Absolute contraindications: prior intracranial hemorrhage, known bleeding diathesis, recent major surgery, uncontrolled hypertension (>185/110 mmHg), and active internal bleeding.", 
         ["stroke", "tPA", "contraindications"], 1.1),
        ("tPA Administration Protocol", 
         "Confirm ischemic stroke via CT. Dose: 0.9 mg/kg (max 90 mg), 10% bolus, remainder over 1 hour. Monitor for complications: bleeding, angioedema, hypotension.", 
         ["stroke", "tPA", "protocol"], 1.0),
        # Mechanical Thrombectomy for LVO
        ("Mechanical Thrombectomy Indications", 
         "Mechanical thrombectomy is indicated for acute ischemic stroke with large vessel occlusion (LVO) within 6 hours of onset. Extended window up to 24 hours if salvageable tissue on imaging.", 
         ["stroke", "thrombectomy", "LVO"], 1.2),
        ("Imaging Criteria for Thrombectomy", 
         "CT angiography or MRI confirms LVO. ASPECTS score >6, absence of large infarct, and presence of salvageable penumbra are required for thrombectomy eligibility.", 
         ["stroke", "thrombectomy", "imaging"], 1.1),
        ("Post-Thrombectomy Management", 
         "Monitor for reperfusion injury, hemorrhagic transformation, and neurological improvement. Antiplatelet therapy may be initiated post-procedure.", 
         ["stroke", "thrombectomy", "management"], 1.0),
        # ILAE 2017 Seizure Classification
        ("ILAE 2017 Seizure Types", 
         "Seizures are classified as focal, generalized, or unknown. Focal seizures may be aware or impaired awareness, with motor or non-motor onset. Generalized seizures include tonic-clonic, absence, myoclonic, and atonic.", 
         ["seizure", "ILAE", "classification"], 1.1),
        ("ILAE 2017 Focal Seizures", 
         "Focal seizures originate in one hemisphere. May present with motor symptoms, sensory changes, or autonomic phenomena. Awareness may be retained or impaired.", 
         ["seizure", "ILAE", "focal"], 1.0),
        ("ILAE 2017 Generalized Seizures", 
         "Generalized seizures involve both hemispheres. Types include absence, tonic-clonic, myoclonic, and atonic. EEG shows generalized spike-and-wave discharges.", 
         ["seizure", "ILAE", "generalized"], 1.0),
        # First-Line AED Selection Algorithm
        ("First-Line AEDs for Focal Seizures", 
         "Carbamazepine, lamotrigine, and levetiracetam are first-line for focal seizures. Consider comorbidities, drug interactions, and side effect profiles.", 
         ["AED", "focal", "first-line"], 1.1),
        ("First-Line AEDs for Generalized Seizures", 
         "Valproate, lamotrigine, and levetiracetam are first-line for generalized seizures. Avoid valproate in women of childbearing age due to teratogenicity.", 
         ["AED", "generalized", "first-line"], 1.1),
        ("AED Selection Algorithm", 
         "Assess seizure type, patient comorbidities, and potential drug interactions. Start with monotherapy and titrate dose. Monitor for efficacy and adverse effects.", 
         ["AED", "selection", "algorithm"], 1.0),
        # Parkinson Disease Diagnosis and Staging
        ("Parkinson Disease Diagnostic Criteria", 
         "Diagnosis requires bradykinesia plus at least one of: rigidity, resting tremor, or postural instability. Exclude secondary causes and atypical features.", 
         ["Parkinson", "diagnosis", "criteria"], 1.2),
        ("Parkinson Disease Staging (Hoehn and Yahr)", 
         "Hoehn and Yahr stages: 1-unilateral, 2-bilateral, 3-postural instability, 4-severe disability, 5-wheelchair/bedbound.", 
         ["Parkinson", "staging", "Hoehn-Yahr"], 1.1),
        ("Differential Diagnosis of Parkinsonism", 
         "Consider drug-induced parkinsonism, multiple system atrophy, progressive supranuclear palsy, and essential tremor. MRI may help exclude structural lesions.", 
         ["Parkinson", "differential", "diagnosis"], 1.0),
        # Alzheimer Disease Diagnosis and Cognitive Assessment
        ("Alzheimer Disease Diagnostic Criteria", 
         "Diagnosis based on insidious onset and progressive memory impairment. Supportive features: language, visuospatial, and executive dysfunction. Rule out reversible causes.", 
         ["Alzheimer", "diagnosis", "criteria"], 1.2),
        ("Cognitive Assessment Tools for Alzheimer", 
         "Mini-Mental State Examination (MMSE) and Montreal Cognitive Assessment (MoCA) are used to assess cognitive impairment. Scores <24 suggest dementia.", 
         ["Alzheimer", "assessment", "cognitive"], 1.1),
        ("Imaging in Alzheimer Disease", 
         "MRI may show hippocampal atrophy. PET imaging can demonstrate reduced glucose metabolism in temporoparietal regions.", 
         ["Alzheimer", "imaging", "MRI"], 1.0),
        # Multiple Sclerosis McDonald Criteria and DMT Selection
        ("McDonald Criteria for MS Diagnosis", 
         "Requires dissemination in space and time. MRI shows lesions in periventricular, juxtacortical, infratentorial, and spinal cord regions. Oligoclonal bands in CSF support diagnosis.", 
         ["MS", "McDonald", "diagnosis"], 1.2),
        ("Disease-Modifying Therapy Selection in MS", 
         "First-line DMTs: interferon-beta, glatiramer acetate. Escalate to fingolimod, natalizumab, or ocrelizumab for aggressive disease. Monitor for adverse effects.", 
         ["MS", "DMT", "selection"], 1.1),
        ("MS Relapse Management", 
         "Acute relapses treated with high-dose corticosteroids. Plasma exchange for severe cases. Avoid triggers and infections.", 
         ["MS", "relapse", "management"], 1.0),
        # Glasgow Coma Scale and TBI Severity Classification
        ("Glasgow Coma Scale (GCS) Scoring", 
         "GCS assesses eye, verbal, and motor responses. Scores: mild TBI (13-15), moderate (9-12), severe (<9). Repeated assessment guides prognosis.", 
         ["GCS", "TBI", "scoring"], 1.2),
        ("TBI Severity Classification", 
         "Mild TBI: GCS 13-15, moderate: 9-12, severe: <9. Assess for intracranial injury and monitor for deterioration.", 
         ["TBI", "severity", "classification"], 1.1),
        ("CT Findings in TBI", 
         "CT may show contusions, hemorrhage, diffuse axonal injury. Immediate imaging required for GCS <13 or focal deficits.", 
         ["TBI", "CT", "findings"], 1.0),
        # CT and MRI Stroke Protocol Interpretation
        ("CT Stroke Protocol Interpretation", 
         "Non-contrast CT rules out hemorrhage. Early ischemic changes: loss of gray-white differentiation, sulcal effacement. ASPECTS scoring quantifies infarct.", 
         ["stroke", "CT", "protocol"], 1.1),
        ("MRI Stroke Protocol Interpretation", 
         "MRI DWI detects acute infarct. FLAIR distinguishes old from new lesions. MR angiography identifies vessel occlusion.", 
         ["stroke", "MRI", "protocol"], 1.1),
        ("Imaging Signs of Acute Stroke", 
         "Hyperdense MCA sign, loss of insular ribbon, and early infarct signs on CT. MRI DWI positive within minutes of onset.", 
         ["stroke", "imaging", "acute"], 1.0),
        # Lumbar Puncture and CSF Interpretation
        ("Lumbar Puncture Procedure", 
         "Indications: suspected CNS infection, subarachnoid hemorrhage, demyelinating disease. Contraindications: increased ICP, coagulopathy. Use L3-L4 or L4-L5 interspace.", 
         ["LP", "procedure", "CSF"], 1.1),
        ("CSF Interpretation in CNS Disease", 
         "Bacterial meningitis: high WBC, low glucose, high protein. Viral: lymphocytic predominance, normal glucose. MS: oligoclonal bands.", 
         ["CSF", "interpretation", "disease"], 1.1),
        ("Complications of Lumbar Puncture", 
         "Post-LP headache, infection, bleeding, and herniation risk. Monitor for neurological deterioration.", 
         ["LP", "complications", "CSF"], 1.0),
        # Migraine Diagnosis and Prophylactic Treatment
        ("Migraine Diagnostic Criteria", 
         "Recurrent headaches lasting 4-72 hours, unilateral, pulsatile, moderate-severe, aggravated by activity. Associated symptoms: nausea, photophobia, phonophobia.", 
         ["migraine", "diagnosis", "criteria"], 1.2),
        ("Migraine Prophylactic Treatments", 
         "First-line: propranolol, amitriptyline, topiramate. Consider comorbidities and contraindications. Lifestyle modification is essential.", 
         ["migraine", "prophylaxis", "treatment"], 1.1),
        ("Acute Migraine Management", 
         "Triptans, NSAIDs, and antiemetics for acute attacks. Avoid overuse to prevent medication-overuse headache.", 
         ["migraine", "acute", "management"], 1.0),
    ]
    for title, content, tags, weight in docs:
        idx.add_document(title, content, tags, weight)