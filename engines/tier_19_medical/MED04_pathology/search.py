import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional

# --- Data Classes ---

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

# --- SearchIndex Class ---

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)  # term -> doc_id -> freq
        self.doc_term_freqs: Dict[str, Counter] = {}  # doc_id -> Counter(term)
        self.term_df: Dict[str, int] = defaultdict(int)  # term -> document frequency
        self.total_docs = 0
        self.total_terms = 0
        self.avg_doc_length = 0.0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # ignore duplicate
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_terms += len(tokens)
            self.doc_term_freqs[doc.id] = Counter(tokens)
            for term, freq in self.doc_term_freqs[doc.id].items():
                self.term_doc_freqs[term][doc.id] = freq
                self.term_df[term] += 1
            self.total_docs += 1
            self.avg_doc_length = self.total_terms / self.total_docs if self.total_docs > 0 else 0.0
            self.idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_df.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        term_freqs = self.doc_term_freqs[doc_id]
        for term in query_terms:
            if term not in term_freqs:
                continue
            idf = self._compute_idf(term)
            tf = term_freqs[term]
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: str) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        term_freqs = self.doc_term_freqs[doc_id]
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self.term_doc_freqs.get(term, {}).keys())
        scored_results = []
        for doc_id in candidate_docs:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scored_results.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scored_results.sort(key=lambda x: x.score, reverse=True)
        return scored_results[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if positions:
            start = max(positions[0] - 10, 0)
            end = min(positions[0] + 10, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        else:
            snippet = ' '.join(tokens[:20])
        return snippet + '...'

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'total_terms': self.total_terms,
            'unique_terms': len(self.term_df),
        }

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Domain Documents ---

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="1",
            title="Acute Inflammation",
            content="Acute inflammation is a rapid response to injury or infection characterized by redness, heat, swelling, pain, and loss of function. Neutrophils are the predominant cell type. Key mediators include histamine, prostaglandins, and cytokines.",
            tags=["inflammation", "acute", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="2",
            title="Chronic Inflammation",
            content="Chronic inflammation is a prolonged inflammatory response involving lymphocytes, macrophages, and plasma cells. It may lead to tissue destruction and fibrosis. Common causes include persistent infections, autoimmune diseases, and prolonged exposure to toxins.",
            tags=["inflammation", "chronic", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="3",
            title="Granulomatous Inflammation",
            content="Granulomatous inflammation is a form of chronic inflammation characterized by granuloma formation. Granulomas consist of macrophages, epithelioid cells, and multinucleated giant cells. Causes include tuberculosis, sarcoidosis, and foreign bodies.",
            tags=["granuloma", "chronic", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="4",
            title="Cell Injury and Necrosis",
            content="Cell injury can be reversible or irreversible. Necrosis is irreversible cell death characterized by cell swelling, loss of membrane integrity, and inflammation. Types include coagulative, liquefactive, caseous, fat, and fibrinoid necrosis.",
            tags=["cell injury", "necrosis", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="5",
            title="Apoptosis",
            content="Apoptosis is programmed cell death without inflammation. It involves cell shrinkage, chromatin condensation, and formation of apoptotic bodies. Key regulators include caspases, Bcl-2 family proteins, and p53.",
            tags=["apoptosis", "cell death", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="6",
            title="Hypertrophy and Hyperplasia",
            content="Hypertrophy is an increase in cell size, while hyperplasia is an increase in cell number. Both are adaptive responses to increased demand or hormonal stimulation. Examples include muscle hypertrophy and endometrial hyperplasia.",
            tags=["hypertrophy", "hyperplasia", "adaptation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="7",
            title="Atrophy and Metaplasia",
            content="Atrophy is a decrease in cell size or number, often due to decreased workload or loss of innervation. Metaplasia is a reversible change from one cell type to another, commonly seen in chronic irritation, such as squamous metaplasia in bronchi.",
            tags=["atrophy", "metaplasia", "adaptation"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="8",
            title="Edema",
            content="Edema is the accumulation of fluid in the interstitial space. Causes include increased hydrostatic pressure, decreased oncotic pressure, lymphatic obstruction, and inflammation. Examples are pulmonary edema and cerebral edema.",
            tags=["edema", "fluid", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="9",
            title="Hemorrhage and Shock",
            content="Hemorrhage is the escape of blood from vessels. Shock is a state of inadequate tissue perfusion. Types include hypovolemic, cardiogenic, septic, and anaphylactic shock. Clinical features include hypotension, tachycardia, and organ dysfunction.",
            tags=["hemorrhage", "shock", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="10",
            title="Thrombosis and Embolism",
            content="Thrombosis is the formation of a blood clot within a vessel. Virchow's triad includes endothelial injury, stasis, and hypercoagulability. Embolism is the occlusion of vessels by material such as thrombus, fat, air, or amniotic fluid.",
            tags=["thrombosis", "embolism", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="11",
            title="Atherosclerosis",
            content="Atherosclerosis is a chronic inflammatory disease of arteries characterized by plaque formation. Risk factors include hyperlipidemia, hypertension, smoking, and diabetes. Complications include myocardial infarction, stroke, and peripheral vascular disease.",
            tags=["atherosclerosis", "vascular", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="12",
            title="Ischemia and Infarction",
            content="Ischemia is reduced blood supply to tissues, leading to hypoxia. Infarction is tissue death due to prolonged ischemia. Common sites include heart (myocardial infarction), brain (stroke), and bowel (intestinal infarction).",
            tags=["ischemia", "infarction", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="13",
            title="Neoplasia",
            content="Neoplasia is abnormal growth of cells, resulting in tumors. Benign tumors are non-invasive, while malignant tumors invade and metastasize. Hallmarks include self-sufficiency in growth signals, evasion of apoptosis, and angiogenesis.",
            tags=["neoplasia", "tumor", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="14",
            title="Carcinogenesis",
            content="Carcinogenesis is the process of cancer development. It involves initiation, promotion, and progression. Genetic mutations, oncogenes, tumor suppressor genes, and environmental factors contribute to carcinogenesis.",
            tags=["carcinogenesis", "cancer", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="15",
            title="Tumor Markers",
            content="Tumor markers are substances produced by cancer cells or by the body in response to cancer. Examples include PSA, AFP, CEA, and CA-125. They are used for diagnosis, prognosis, and monitoring treatment response.",
            tags=["tumor markers", "cancer", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="16",
            title="Metastasis",
            content="Metastasis is the spread of cancer cells from the primary site to distant organs. Common routes include lymphatic, hematogenous, and transcoelomic spread. Sites include liver, lungs, bone, and brain.",
            tags=["metastasis", "cancer", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="17",
            title="Genetic Disorders",
            content="Genetic disorders are caused by mutations in DNA. Types include single-gene disorders, chromosomal abnormalities, and multifactorial inheritance. Examples are cystic fibrosis, Down syndrome, and sickle cell anemia.",
            tags=["genetic", "disorders", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="18",
            title="Immunopathology",
            content="Immunopathology is the study of immune system disorders. Includes hypersensitivity reactions, autoimmune diseases, and immunodeficiency. Examples are systemic lupus erythematosus, rheumatoid arthritis, and HIV/AIDS.",
            tags=["immunopathology", "immune", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="19",
            title="Hypersensitivity Reactions",
            content="Hypersensitivity reactions are excessive immune responses. Types include Type I (allergy), Type II (cytotoxic), Type III (immune complex), and Type IV (delayed). Examples are anaphylaxis, hemolytic anemia, and contact dermatitis.",
            tags=["hypersensitivity", "immune", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="20",
            title="Autoimmune Diseases",
            content="Autoimmune diseases occur when the immune system attacks self-antigens. Examples include type 1 diabetes, multiple sclerosis, and Graves' disease. Mechanisms involve loss of tolerance and molecular mimicry.",
            tags=["autoimmune", "immune", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="21",
            title="Amyloidosis",
            content="Amyloidosis is a group of diseases characterized by extracellular deposition of amyloid proteins. Types include AL, AA, and hereditary amyloidosis. Clinical features include nephrotic syndrome, heart failure, and neuropathy.",
            tags=["amyloidosis", "protein", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="22",
            title="Hemostasis Disorders",
            content="Hemostasis disorders include bleeding and clotting abnormalities. Examples are hemophilia, von Willebrand disease, and disseminated intravascular coagulation (DIC). Symptoms include bleeding, bruising, and thrombosis.",
            tags=["hemostasis", "bleeding", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="23",
            title="Environmental Pathology",
            content="Environmental pathology studies the effects of environmental factors on health. Includes pollution, toxins, radiation, and occupational hazards. Examples are asbestosis, lead poisoning, and radiation sickness.",
            tags=["environmental", "toxins", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="24",
            title="Nutritional Disorders",
            content="Nutritional disorders are caused by deficiencies or excess of nutrients. Examples include kwashiorkor, marasmus, obesity, and vitamin deficiencies. Clinical features depend on the specific nutrient involved.",
            tags=["nutrition", "deficiency", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="25",
            title="Infectious Diseases",
            content="Infectious diseases are caused by pathogens such as bacteria, viruses, fungi, and parasites. Pathogenesis involves invasion, toxin production, and immune response. Examples are tuberculosis, hepatitis, and malaria.",
            tags=["infection", "pathogen", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="26",
            title="Pathology of Aging",
            content="Aging is associated with cellular and molecular changes. Pathological features include decreased regenerative capacity, accumulation of DNA damage, and increased risk of neoplasia and degenerative diseases.",
            tags=["aging", "degeneration", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="27",
            title="Wound Healing",
            content="Wound healing involves hemostasis, inflammation, proliferation, and remodeling. Healing can be by primary or secondary intention. Complications include infection, dehiscence, and keloid formation.",
            tags=["wound healing", "repair", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="28",
            title="Pathology of the Kidney",
            content="Renal pathology includes glomerulonephritis, nephrotic syndrome, and acute tubular necrosis. Clinical features are hematuria, proteinuria, and renal failure. Diagnosis involves biopsy and laboratory tests.",
            tags=["kidney", "renal", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="29",
            title="Pathology of the Liver",
            content="Liver pathology includes hepatitis, cirrhosis, and hepatocellular carcinoma. Symptoms are jaundice, ascites, and hepatic encephalopathy. Causes include viral infection, alcohol, and toxins.",
            tags=["liver", "hepatic", "pathology"],
            weight=1.0
        ),
        SearchDocument(
            doc_id="30",
            title="Pathology of the Heart",
            content="Cardiac pathology includes myocardial infarction, heart failure, and cardiomyopathy. Symptoms are chest pain, dyspnea, and edema. Diagnosis involves ECG, biomarkers, and imaging.",
            tags=["heart", "cardiac", "pathology"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)