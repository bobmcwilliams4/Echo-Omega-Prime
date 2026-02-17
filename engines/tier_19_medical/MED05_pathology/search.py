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
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.avg_doc_length: float = 0.0
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}
        self._token_pattern = re.compile(r'\b\w+\b')

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            tf_counter = Counter(tokens)
            self.term_freqs[doc.id] = dict(tf_counter)
            for term in tf_counter:
                self.term_doc_freq[term] += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        doc_scores: Dict[int, float] = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, tf_dict in self.term_freqs.items():
                tf = tf_dict.get(term, 0)
                score = self._score_bm25(tf, self.doc_lengths[doc_id], idf)
                doc_scores[doc_id] += score * self.documents[doc_id].weight
        tfidf_scores = self._tfidf_search(query_terms)
        for doc_id, tfidf_score in tfidf_scores.items():
            doc_scores[doc_id] += tfidf_score * 0.3  # Blend TF-IDF with BM25
        results = []
        for doc_id, score in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        return [token.lower() for token in self._token_pattern.findall(text)]

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, tf: int, doc_len: int, idf: float) -> float:
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / (self.avg_doc_length + 1e-6)))
        return idf * (numerator / (denominator + 1e-6))

    def _tfidf_search(self, query_terms: List[str]) -> Dict[int, float]:
        tfidf_scores = defaultdict(float)
        for term in query_terms:
            idf = self._compute_idf(term)
            for doc_id, tf_dict in self.term_freqs.items():
                tf = tf_dict.get(term, 0)
                norm_tf = tf / (self.doc_lengths[doc_id] + 1e-6)
                tfidf_scores[doc_id] += norm_tf * idf
        return tfidf_scores

    def _make_snippet(self, content: str, query_terms: List[str]) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:30])
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 20, len(tokens))
        snippet = ' '.join(tokens[start:end])
        return snippet

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "CBC Differential Interpretation",
            "The complete blood count (CBC) with differential provides information on white blood cell types: neutrophils, lymphocytes, monocytes, eosinophils, and basophils. Neutrophilia suggests bacterial infection, lymphocytosis viral infection, and eosinophilia allergy or parasitic disease.",
            ["cbc", "differential", "hematology"],
            1.0
        ),
        SearchDocument(
            2,
            "Coagulation Studies: PT, INR, PTT",
            "Prothrombin time (PT) and international normalized ratio (INR) assess the extrinsic pathway, while partial thromboplastin time (PTT) evaluates the intrinsic pathway. Prolonged PT/INR may indicate liver dysfunction or vitamin K deficiency. Prolonged PTT may suggest hemophilia or heparin therapy.",
            ["coagulation", "pt", "inr", "ptt"],
            1.0
        ),
        SearchDocument(
            3,
            "Fibrinogen and D-dimer",
            "Fibrinogen is a clotting factor; low levels may indicate disseminated intravascular coagulation (DIC). D-dimer is a fibrin degradation product, elevated in thrombotic events such as deep vein thrombosis (DVT) or pulmonary embolism (PE).",
            ["fibrinogen", "d-dimer", "thrombosis"],
            1.0
        ),
        SearchDocument(
            4,
            "Basic Metabolic Panel (BMP) Interpretation",
            "The BMP includes sodium, potassium, chloride, bicarbonate, blood urea nitrogen (BUN), creatinine, glucose, and calcium. It is used to assess renal function, electrolyte balance, and metabolic status.",
            ["bmp", "electrolytes", "renal"],
            1.0
        ),
        SearchDocument(
            5,
            "Comprehensive Metabolic Panel (CMP) and Liver Enzymes",
            "CMP expands on BMP by including liver enzymes (ALT, AST, ALP), albumin, and total bilirubin. Elevated ALT/AST indicate hepatocellular injury. ALP elevation may suggest cholestasis or bone disease.",
            ["cmp", "liver", "enzymes"],
            1.0
        ),
        SearchDocument(
            6,
            "Cardiac Biomarkers: Troponin, BNP, CK-MB",
            "Troponin is highly specific for myocardial injury. BNP is elevated in heart failure. CK-MB is less specific but may be used for reinfarction detection.",
            ["cardiac", "troponin", "bnp", "ck-mb"],
            1.0
        ),
        SearchDocument(
            7,
            "Thyroid Function Tests: TSH, Free T4, T3",
            "TSH is the primary screening test. Low TSH and high T4/T3 suggest hyperthyroidism. High TSH and low T4 indicate hypothyroidism. Free T4 is preferred for diagnosis.",
            ["thyroid", "tsh", "t4", "t3"],
            1.0
        ),
        SearchDocument(
            8,
            "Lipid Panel Interpretation",
            "Lipid panel includes total cholesterol, LDL, HDL, and triglycerides. High LDL increases cardiovascular risk. HDL is protective. Elevated triglycerides may be seen in metabolic syndrome.",
            ["lipid", "cholesterol", "ldl", "hdl", "triglycerides"],
            1.0
        ),
        SearchDocument(
            9,
            "Urinalysis: Dipstick, Microscopy, and Culture",
            "Urinalysis assesses kidney function and infection. Dipstick detects protein, blood, leukocytes, nitrites, glucose. Microscopy identifies casts, crystals, cells. Culture diagnoses urinary tract infection (UTI).",
            ["urinalysis", "dipstick", "microscopy", "culture"],
            1.0
        ),
        SearchDocument(
            10,
            "Blood Gas Analysis: ABG and VBG",
            "Arterial blood gas (ABG) evaluates pH, pCO2, pO2, HCO3. Used to diagnose acid-base disorders and respiratory/metabolic dysfunction. Venous blood gas (VBG) is less accurate for oxygenation.",
            ["abg", "vbg", "blood gas", "acid-base"],
            1.0
        ),
        SearchDocument(
            11,
            "Hemoglobin A1c for Diabetes Monitoring",
            "Hemoglobin A1c reflects average blood glucose over 2-3 months. Values above 6.5% indicate diabetes. Used for diagnosis and monitoring glycemic control.",
            ["hemoglobin a1c", "diabetes", "glycemic"],
            1.0
        ),
        SearchDocument(
            12,
            "Blood Culture Identification and Sensitivity",
            "Blood cultures are used to detect bacteremia. Identification of organisms and sensitivity testing guide antibiotic therapy. Multiple sets increase sensitivity.",
            ["blood culture", "bacteremia", "sensitivity"],
            1.0
        ),
        SearchDocument(
            13,
            "CSF Analysis: Cell Count, Protein, Glucose",
            "Cerebrospinal fluid (CSF) analysis aids in diagnosing meningitis, encephalitis, and subarachnoid hemorrhage. Elevated white cells suggest infection. Low glucose and high protein may indicate bacterial meningitis.",
            ["csf", "cell count", "protein", "glucose"],
            1.0
        ),
        SearchDocument(
            14,
            "Tumor Markers: PSA, CEA, CA-125, AFP",
            "Tumor markers are used for cancer screening and monitoring. PSA for prostate, CEA for colon, CA-125 for ovarian, AFP for liver and testicular cancers.",
            ["tumor markers", "psa", "cea", "ca-125", "afp"],
            1.0
        ),
        SearchDocument(
            15,
            "Iron Studies: Ferritin, TIBC, Transferrin Saturation",
            "Ferritin reflects iron stores. TIBC measures binding capacity. Low ferritin and high TIBC suggest iron deficiency anemia. Transferrin saturation assesses iron availability.",
            ["iron", "ferritin", "tibc", "transferrin"],
            1.0
        ),
        SearchDocument(
            16,
            "Autoimmune Panel: ANA, anti-dsDNA, RF, CCP",
            "ANA is sensitive for lupus. Anti-dsDNA is specific for SLE. Rheumatoid factor (RF) and anti-CCP are used in rheumatoid arthritis diagnosis.",
            ["autoimmune", "ana", "dsdna", "rf", "ccp"],
            1.0
        ),
        SearchDocument(
            17,
            "Hepatitis Serology: HBsAg, anti-HBs, anti-HCV",
            "HBsAg indicates active hepatitis B infection. Anti-HBs suggests immunity. Anti-HCV is used for hepatitis C screening.",
            ["hepatitis", "serology", "hbsag", "anti-hbs", "anti-hcv"],
            1.0
        ),
        SearchDocument(
            18,
            "HIV Testing Algorithm: 4th Generation Combo",
            "4th generation HIV tests detect both antigen and antibody. Early detection is possible. Positive results require confirmatory testing.",
            ["hiv", "testing", "algorithm", "4th generation"],
            1.0
        ),
        SearchDocument(
            19,
            "Drug Screening: Immunoassay and GC-MS Confirmation",
            "Drug screening uses immunoassay for rapid detection. GC-MS is used for confirmation and quantification. Common drugs screened include opioids, amphetamines, cocaine, and cannabis.",
            ["drug screening", "immunoassay", "gc-ms"],
            1.0
        ),
        SearchDocument(
            20,
            "Molecular Diagnostics: PCR, FISH, NGS",
            "PCR amplifies DNA for pathogen detection. FISH identifies chromosomal abnormalities. Next-generation sequencing (NGS) allows comprehensive genetic analysis.",
            ["molecular", "diagnostics", "pcr", "fish", "ngs"],
            1.0
        ),
        SearchDocument(
            21,
            "Flow Cytometry: Immunophenotyping in Lymphoma/Leukemia",
            "Flow cytometry analyzes cell surface markers. Immunophenotyping distinguishes lymphoma and leukemia subtypes. Used for diagnosis and monitoring.",
            ["flow cytometry", "immunophenotyping", "lymphoma", "leukemia"],
            1.0
        ),
        SearchDocument(
            22,
            "BMP vs CMP: Clinical Utility",
            "BMP is used for basic metabolic assessment. CMP adds liver function and protein analysis. CMP is preferred when liver disease is suspected.",
            ["bmp", "cmp", "clinical utility"],
            1.0
        ),
        SearchDocument(
            23,
            "Interpretation of Elevated Troponin",
            "Elevated troponin is most commonly due to myocardial infarction. Other causes include myocarditis, heart failure, renal failure, and sepsis.",
            ["troponin", "myocardial", "interpretation"],
            1.0
        ),
        SearchDocument(
            24,
            "PT/INR Monitoring in Warfarin Therapy",
            "Warfarin therapy requires regular PT/INR monitoring. Target INR depends on indication. High INR increases bleeding risk.",
            ["pt", "inr", "warfarin", "monitoring"],
            1.0
        ),
        SearchDocument(
            25,
            "D-dimer in Pulmonary Embolism Diagnosis",
            "D-dimer is sensitive but not specific for pulmonary embolism. Negative D-dimer can rule out PE in low-risk patients.",
            ["d-dimer", "pulmonary embolism", "diagnosis"],
            1.0
        ),
        SearchDocument(
            26,
            "Thyroid Panel in Pregnancy",
            "TSH levels may decrease in pregnancy. Free T4 is preferred. Hypothyroidism in pregnancy increases risk of complications.",
            ["thyroid", "pregnancy", "tsh", "t4"],
            1.0
        ),
        SearchDocument(
            27,
            "Urinalysis for Glomerulonephritis",
            "Urinalysis shows proteinuria, hematuria, and red cell casts in glomerulonephritis. Microscopy is essential for diagnosis.",
            ["urinalysis", "glomerulonephritis", "proteinuria"],
            1.0
        ),
        SearchDocument(
            28,
            "ABG Interpretation: Respiratory vs Metabolic",
            "ABG helps distinguish respiratory from metabolic acid-base disorders. Look at pH, pCO2, and HCO3 for interpretation.",
            ["abg", "acid-base", "respiratory", "metabolic"],
            1.0
        ),
        SearchDocument(
            29,
            "BNP in Heart Failure Diagnosis",
            "BNP is released in response to ventricular stretch. Elevated BNP supports heart failure diagnosis.",
            ["bnp", "heart failure", "diagnosis"],
            1.0
        ),
        SearchDocument(
            30,
            "ANA Patterns in Autoimmune Disease",
            "ANA patterns (homogeneous, speckled, nucleolar) help differentiate autoimmune diseases. Homogeneous pattern is common in SLE.",
            ["ana", "autoimmune", "patterns"],
            1.0
        ),
        SearchDocument(
            31,
            "Hepatitis B Serology Interpretation",
            "HBsAg positive indicates infection. Anti-HBs positive indicates immunity. Anti-HBc distinguishes acute from chronic infection.",
            ["hepatitis b", "serology", "interpretation"],
            1.0
        ),
        SearchDocument(
            32,
            "NGS in Cancer Genomics",
            "Next-generation sequencing (NGS) identifies mutations in cancer. Used for targeted therapy selection.",
            ["ngs", "cancer", "genomics"],
            1.0
        ),
        SearchDocument(
            33,
            "Ferritin in Inflammatory States",
            "Ferritin is an acute phase reactant. Elevated ferritin may indicate inflammation or infection, not just iron overload.",
            ["ferritin", "inflammation", "acute phase"],
            1.0
        ),
        SearchDocument(
            34,
            "Blood Culture Contamination",
            "Contamination is common in blood cultures. Proper technique reduces false positives. Skin flora are typical contaminants.",
            ["blood culture", "contamination", "false positive"],
            1.0
        ),
        SearchDocument(
            35,
            "CK-MB vs Troponin in Myocardial Injury",
            "CK-MB rises earlier but is less specific than troponin. Troponin remains elevated longer and is preferred for diagnosis.",
            ["ck-mb", "troponin", "myocardial injury"],
            1.0
        ),
        SearchDocument(
            36,
            "AFP in Hepatocellular Carcinoma",
            "Alpha-fetoprotein (AFP) is elevated in hepatocellular carcinoma and germ cell tumors. Used for screening and monitoring.",
            ["afp", "hepatocellular carcinoma", "screening"],
            1.0
        ),
        SearchDocument(
            37,
            "PCR in Infectious Disease Diagnosis",
            "PCR is used to detect viral and bacterial pathogens. Rapid and sensitive, especially for tuberculosis and viral meningitis.",
            ["pcr", "infectious disease", "diagnosis"],
            1.0
        ),
        SearchDocument(
            38,
            "Flow Cytometry in Leukemia Classification",
            "Flow cytometry identifies cell surface markers. Essential for leukemia subtype classification and prognosis.",
            ["flow cytometry", "leukemia", "classification"],
            1.0
        ),
        SearchDocument(
            39,
            "TSH Suppression in Thyroid Cancer",
            "TSH suppression therapy is used in thyroid cancer to reduce recurrence risk. Monitor TSH and free T4 regularly.",
            ["tsh", "thyroid cancer", "suppression"],
            1.0
        ),
        SearchDocument(
            40,
            "Drug Screening for Opioids",
            "Immunoassay detects opioids in urine. GC-MS confirms and quantifies specific drugs. False positives are possible.",
            ["drug screening", "opioids", "gc-ms"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)