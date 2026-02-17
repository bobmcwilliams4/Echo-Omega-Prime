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
        self.term_doc_tfs: Dict[int, Counter] = {}
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}
        self._preseeded = False

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.term_doc_tfs[doc.id] = tf
            for term in tf.keys():
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = (
                sum(self.doc_lengths.values()) / self.total_docs
                if self.total_docs > 0 else 0.0
            )
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        N = self.total_docs
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_doc_tfs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avg_len = self.avg_doc_length
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / avg_len)
            score += idf * numerator / denominator
        return score * self.documents[doc_id].weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_doc_tfs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: List[Tuple[int, float]] = []
        for doc_id in self.documents:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                raise ValueError("Unknown search method: %s" % method)
            if score > 0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in scores[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet + ('...' if end < len(tokens) else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

    def _preseed(self):
        if self._preseeded:
            return
        docs = [
            SearchDocument(
                1, "Obstructive Spirometry Pattern",
                "Obstructive pattern is characterized by reduced FEV1/FVC ratio (<0.7 or below LLN). Causes include asthma, COPD, bronchiectasis, and upper airway obstruction.",
                ["spirometry", "obstructive", "PFT"], 1.0
            ),
            SearchDocument(
                2, "Diffusing Capacity (DLCO) Interpretation",
                "DLCO assesses gas transfer across the alveolar-capillary membrane. Reduced DLCO may indicate interstitial lung disease, emphysema, pulmonary vascular disease, or anemia.",
                ["DLCO", "PFT", "diffusion"], 1.0
            ),
            SearchDocument(
                3, "Asthma Diagnosis and Phenotyping",
                "Asthma diagnosis is based on variable airflow obstruction and reversibility. Phenotyping includes allergic, eosinophilic, and non-eosinophilic asthma.",
                ["asthma", "diagnosis", "phenotype"], 1.0
            ),
            SearchDocument(
                4, "COPD Diagnosis and Severity Grading",
                "COPD diagnosis requires FEV1/FVC <0.7 post-bronchodilator. Severity is graded by GOLD criteria based on FEV1 percent predicted.",
                ["COPD", "diagnosis", "severity"], 1.0
            ),
            SearchDocument(
                5, "Interstitial Lung Disease (ILD) Diagnostic Approach",
                "ILD diagnosis involves clinical history, HRCT imaging, serologic testing, and sometimes lung biopsy. Common causes include idiopathic pulmonary fibrosis, connective tissue disease, and drug-induced ILD.",
                ["ILD", "diagnosis", "HRCT"], 1.0
            ),
            SearchDocument(
                6, "Pulmonary Hypertension Classification and Diagnosis",
                "Pulmonary hypertension is classified into five groups. Diagnosis includes echocardiography, right heart catheterization, and exclusion of secondary causes.",
                ["pulmonary hypertension", "diagnosis", "classification"], 1.0
            ),
            SearchDocument(
                7, "Sleep Apnea Diagnosis and Therapy",
                "Obstructive sleep apnea is diagnosed by polysomnography. Treatment includes CPAP, weight loss, and oral appliances.",
                ["sleep apnea", "diagnosis", "therapy"], 1.0
            ),
            SearchDocument(
                8, "Mechanical Ventilation: Modes and Initial Settings",
                "Common modes include volume control, pressure control, and SIMV. Initial settings: tidal volume 6-8 ml/kg, respiratory rate, FiO2, and PEEP.",
                ["mechanical ventilation", "modes", "settings"], 1.0
            ),
            SearchDocument(
                9, "Pleural Effusion Analysis and Light's Criteria",
                "Light's criteria distinguish exudate from transudate. Exudate if any: pleural/serum protein >0.5, pleural/serum LDH >0.6, or pleural LDH >2/3 upper limit normal.",
                ["pleural effusion", "Light's criteria", "analysis"], 1.0
            ),
            SearchDocument(
                10, "Lung Cancer Screening and Staging",
                "Screening is recommended for high-risk patients with low-dose CT. Staging uses TNM system and guides treatment options.",
                ["lung cancer", "screening", "staging"], 1.0
            ),
            SearchDocument(
                11, "Acute Exacerbation of COPD (AECOPD) Management",
                "AECOPD management includes bronchodilators, corticosteroids, antibiotics if indicated, and oxygen therapy. Noninvasive ventilation may be required.",
                ["AECOPD", "management", "COPD"], 1.0
            ),
            SearchDocument(
                12, "Bronchiectasis Diagnosis and Management",
                "Bronchiectasis is diagnosed by HRCT showing airway dilation. Management includes airway clearance, antibiotics for exacerbations, and treating underlying causes.",
                ["bronchiectasis", "diagnosis", "management"], 1.0
            ),
            SearchDocument(
                13, "Pulmonary Embolism Diagnosis and Risk Stratification",
                "PE diagnosis uses Wells score, D-dimer, CT pulmonary angiography. Risk stratification guides anticoagulation and thrombolysis decisions.",
                ["pulmonary embolism", "diagnosis", "risk"], 1.0
            ),
            SearchDocument(
                14, "Sarcoidosis Diagnosis and Treatment",
                "Sarcoidosis is diagnosed by clinical, radiographic, and histologic findings of non-caseating granulomas. Treatment is with corticosteroids for symptomatic disease.",
                ["sarcoidosis", "diagnosis", "treatment"], 1.0
            ),
            SearchDocument(
                15, "Pneumonia Severity Assessment and Antibiotic Selection",
                "Severity is assessed by CURB-65 or PSI. Antibiotic selection depends on likely pathogens and patient risk factors.",
                ["pneumonia", "severity", "antibiotics"], 1.0
            ),
            SearchDocument(
                16, "Chronic Cough Evaluation",
                "Chronic cough evaluation includes history, chest imaging, and spirometry. Common causes: postnasal drip, asthma, GERD, ACE inhibitors.",
                ["chronic cough", "evaluation", "causes"], 1.0
            ),
            SearchDocument(
                17, "Oxygen Therapy Prescription and Monitoring",
                "Oxygen therapy is prescribed for hypoxemia. Monitoring includes pulse oximetry and arterial blood gases. Target saturation: 88-92% in COPD.",
                ["oxygen therapy", "prescription", "monitoring"], 1.0
            ),
            SearchDocument(
                18, "Pulmonary Nodule Biopsy Techniques",
                "Biopsy techniques include transthoracic needle, bronchoscopy, and surgical resection. Choice depends on nodule size, location, and patient risk.",
                ["pulmonary nodule", "biopsy", "techniques"], 1.0
            ),
            SearchDocument(
                19, "Restrictive Lung Disease PFT Pattern",
                "Restrictive pattern shows reduced FVC with normal or increased FEV1/FVC. Causes include ILD, chest wall disorders, and neuromuscular disease.",
                ["restrictive", "PFT", "lung disease"], 1.0
            ),
            SearchDocument(
                20, "Hemoptysis Evaluation",
                "Hemoptysis evaluation includes history, chest imaging, and bronchoscopy. Common causes: bronchitis, bronchiectasis, lung cancer, TB.",
                ["hemoptysis", "evaluation", "causes"], 1.0
            ),
            SearchDocument(
                21, "Alpha-1 Antitrypsin Deficiency in COPD",
                "Alpha-1 antitrypsin deficiency is a genetic cause of COPD, especially in young, non-smoking patients. Diagnosis is by serum levels and genotyping.",
                ["COPD", "alpha-1 antitrypsin", "genetic"], 1.0
            ),
            SearchDocument(
                22, "High-Resolution CT (HRCT) in ILD",
                "HRCT is essential for ILD diagnosis, showing patterns like UIP, NSIP, and ground-glass opacities. Guides further management and biopsy decisions.",
                ["HRCT", "ILD", "imaging"], 1.0
            ),
            SearchDocument(
                23, "Pulmonary Rehabilitation in Chronic Lung Disease",
                "Pulmonary rehabilitation improves exercise tolerance, symptoms, and quality of life in COPD, ILD, and bronchiectasis.",
                ["pulmonary rehabilitation", "COPD", "ILD"], 1.0
            ),
            SearchDocument(
                24, "Noninvasive Positive Pressure Ventilation (NPPV)",
                "NPPV is used in COPD exacerbations, acute pulmonary edema, and neuromuscular disease. Reduces intubation rates and mortality.",
                ["NPPV", "COPD", "ventilation"], 1.0
            ),
            SearchDocument(
                25, "Pulmonary Hypertension: Group 1 (PAH)",
                "Group 1 pulmonary arterial hypertension is idiopathic or associated with connective tissue disease, HIV, or drugs. Diagnosis by right heart catheterization.",
                ["pulmonary hypertension", "PAH", "diagnosis"], 1.0
            ),
            SearchDocument(
                26, "Light's Criteria for Pleural Effusion",
                "Light's criteria: exudate if pleural/serum protein >0.5, pleural/serum LDH >0.6, or pleural LDH >2/3 upper limit normal. Used to differentiate exudate from transudate.",
                ["pleural effusion", "Light's criteria", "exudate"], 1.0
            ),
            SearchDocument(
                27, "Bronchoscopy in Lung Cancer Diagnosis",
                "Bronchoscopy is used for central lung lesions, biopsy, and staging. Endobronchial ultrasound improves yield for mediastinal nodes.",
                ["bronchoscopy", "lung cancer", "diagnosis"], 1.0
            ),
            SearchDocument(
                28, "Pulmonary Function Test Interpretation",
                "PFT interpretation includes spirometry, lung volumes, and DLCO. Patterns: obstructive, restrictive, mixed, and diffusion impairment.",
                ["PFT", "interpretation", "spirometry"], 1.0
            ),
            SearchDocument(
                29, "Management of Severe Asthma",
                "Severe asthma may require biologics, high-dose inhaled steroids, and oral corticosteroids. Phenotyping guides therapy selection.",
                ["asthma", "management", "severe"], 1.0
            ),
            SearchDocument(
                30, "Pulmonary Embolism: Massive vs Submassive",
                "Massive PE presents with hypotension and shock; submassive with RV dysfunction but stable BP. Thrombolysis is considered for massive PE.",
                ["pulmonary embolism", "massive", "submassive"], 1.0
            ),
        ]
        for doc in docs:
            self.add_document(doc)
        self._preseeded = True

def get_search_index() -> SearchIndex:
    global _med15_search_index
    try:
        return _med15_search_index
    except NameError:
        _med15_search_index = SearchIndex()
        _med15_search_index._preseed()
        return _med15_search_index