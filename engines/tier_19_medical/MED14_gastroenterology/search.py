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
        self.term_freqs: Dict[int, Counter] = defaultdict(Counter)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._doc_id_counter = 1

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self.lock:
            doc_id = self._doc_id_counter
            self._doc_id_counter += 1
            doc = SearchDocument(doc_id, title, content, tags, weight)
            self.documents[doc_id] = doc
            tokens = self._tokenize(content)
            self.doc_lengths[doc_id] = len(tokens)
            self.term_freqs[doc_id] = Counter(tokens)
            for term in set(tokens):
                self.term_doc_freq[term] += 1
            self._update_avg_doc_length()
            self.idf_cache.clear()
            return doc_id

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores = defaultdict(float)
        tfidf_scores = defaultdict(float)
        for doc_id, doc in self.documents.items():
            bm25_score = self._score_bm25(doc_id, query_tokens)
            tfidf_score = self._score_tfidf(doc_id, query_tokens)
            combined_score = bm25_score + 0.3 * tfidf_score
            scores[doc_id] = combined_score * doc.weight
            tfidf_scores[doc_id] = tfidf_score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:limit]:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_tokens)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        return {
            'num_documents': len(self.documents),
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        N = len(self.documents)
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_tokens: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.term_freqs[doc_id]
        for term in query_tokens:
            idf = self._compute_idf(term)
            freq = tf.get(term, 0)
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / avgdl)
            if denominator == 0:
                continue
            score += idf * numerator / denominator
        return score

    def _score_tfidf(self, doc_id: int, query_tokens: List[str]) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths.get(doc_id, 0)
        score = 0.0
        for term in query_tokens:
            term_freq = tf.get(term, 0)
            if doc_len == 0:
                continue
            tf_norm = term_freq / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _update_avg_doc_length(self):
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)
        else:
            self.avg_doc_length = 0.0

    def _make_snippet(self, content: str, query_tokens: List[str], window: int = 40) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if not positions:
            snippet = ' '.join(tokens[:window])
        else:
            start = max(positions[0] - window // 2, 0)
            end = min(start + window, len(tokens))
            snippet = ' '.join(tokens[start:end])
        snippet = snippet.strip()
        return snippet

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
        {
            "title": "Interpretation of Upper Endoscopy Findings",
            "content": "Upper endoscopy reveals esophageal erosions, gastric ulcers, and duodenal inflammation. Interpretation requires assessment of mucosal integrity, presence of bleeding, and biopsy for H. pylori.",
            "tags": ["endoscopy", "esophagus", "stomach", "duodenum", "findings"]
        },
        {
            "title": "Colonoscopy Polyp Management Guidelines",
            "content": "Colonoscopy identifies polyps which are classified as adenomatous, hyperplastic, or sessile serrated. Management includes removal, histopathological evaluation, and surveillance intervals based on size and histology.",
            "tags": ["colonoscopy", "polyp", "management", "surveillance"]
        },
        {
            "title": "Surveillance After Polypectomy",
            "content": "Post-polypectomy surveillance is determined by polyp type, number, and size. High-risk adenomas require shorter intervals. Low-risk polyps may warrant longer intervals.",
            "tags": ["polypectomy", "surveillance", "adenoma", "intervals"]
        },
        {
            "title": "Staging Chronic Liver Disease",
            "content": "Chronic liver disease staging uses clinical assessment, laboratory markers, and imaging. Fibrosis is evaluated via elastography or biopsy. Child-Pugh and MELD scores guide prognosis.",
            "tags": ["liver", "chronic", "staging", "fibrosis", "MELD", "Child-Pugh"]
        },
        {
            "title": "Monitoring Chronic Liver Disease Progression",
            "content": "Monitoring involves serial liver function tests, imaging for cirrhosis, and screening for hepatocellular carcinoma. Non-invasive markers like FIB-4 and APRI are used.",
            "tags": ["liver", "monitoring", "progression", "screening", "FIB-4", "APRI"]
        },
        {
            "title": "Inflammatory Bowel Disease Activity Assessment",
            "content": "IBD activity is monitored by symptoms, fecal calprotectin, CRP, and endoscopic findings. Escalation of therapy is considered for moderate to severe disease.",
            "tags": ["IBD", "activity", "monitoring", "calprotectin", "CRP", "endoscopy"]
        },
        {
            "title": "Escalation Strategies in IBD",
            "content": "Escalation in IBD includes optimizing current therapy, switching biologics, or adding immunomodulators. Assessment of response and adverse effects is crucial.",
            "tags": ["IBD", "escalation", "biologics", "immunomodulators", "therapy"]
        },
        {
            "title": "Hepatocellular Carcinoma Screening Protocols",
            "content": "Screening for HCC in cirrhosis involves ultrasound every 6 months, with or without AFP measurement. Early detection improves outcomes.",
            "tags": ["hepatocellular carcinoma", "screening", "cirrhosis", "ultrasound", "AFP"]
        },
        {
            "title": "Diagnosis of Hepatocellular Carcinoma",
            "content": "HCC diagnosis is based on imaging criteria (LI-RADS), elevated AFP, and biopsy when imaging is inconclusive. MRI and CT are preferred modalities.",
            "tags": ["HCC", "diagnosis", "imaging", "AFP", "MRI", "CT"]
        },
        {
            "title": "GERD Diagnosis and Management",
            "content": "GERD diagnosis relies on symptoms, response to PPI therapy, and sometimes pH monitoring. Management includes lifestyle modification, acid suppression, and surgical options for refractory cases.",
            "tags": ["GERD", "diagnosis", "management", "PPI", "pH monitoring", "surgery"]
        },
        {
            "title": "Celiac Disease Diagnosis",
            "content": "Celiac disease diagnosis involves serologic testing (tTG-IgA), duodenal biopsy, and response to gluten-free diet. Genetic testing may be supportive.",
            "tags": ["celiac", "diagnosis", "serology", "biopsy", "gluten-free"]
        },
        {
            "title": "Celiac Disease Management",
            "content": "Management of celiac disease requires strict gluten-free diet, nutritional assessment, and monitoring for complications such as osteoporosis and malignancy.",
            "tags": ["celiac", "management", "gluten-free", "nutrition", "complications"]
        },
        {
            "title": "Acute Pancreatitis Diagnosis",
            "content": "Diagnosis of acute pancreatitis is based on abdominal pain, elevated amylase or lipase, and imaging. Severity is assessed by Ranson criteria and organ dysfunction.",
            "tags": ["pancreatitis", "diagnosis", "amylase", "lipase", "imaging", "severity"]
        },
        {
            "title": "Severity Assessment in Acute Pancreatitis",
            "content": "Severity is determined by clinical scoring systems (Ranson, APACHE II), imaging findings, and presence of organ failure. Early aggressive fluid resuscitation is key.",
            "tags": ["pancreatitis", "severity", "assessment", "Ranson", "APACHE II", "organ failure"]
        },
        {
            "title": "Endoscopic Findings in Barrett's Esophagus",
            "content": "Barrett's esophagus is identified by salmon-colored mucosa above the gastroesophageal junction. Biopsy is needed to assess dysplasia.",
            "tags": ["endoscopy", "Barrett's", "esophagus", "dysplasia", "biopsy"]
        },
        {
            "title": "Surveillance of Barrett's Esophagus",
            "content": "Surveillance intervals depend on presence and grade of dysplasia. Endoscopic ablation may be considered for high-grade dysplasia.",
            "tags": ["Barrett's", "surveillance", "dysplasia", "ablation", "endoscopy"]
        },
        {
            "title": "Management of Colonoscopy Findings: Sessile Serrated Polyps",
            "content": "Sessile serrated polyps are removed endoscopically and require closer surveillance due to higher risk of malignancy.",
            "tags": ["colonoscopy", "sessile serrated", "polyp", "management", "surveillance"]
        },
        {
            "title": "Chronic Liver Disease: Child-Pugh Classification",
            "content": "Child-Pugh score evaluates ascites, bilirubin, albumin, INR, and encephalopathy to classify liver disease severity.",
            "tags": ["liver", "Child-Pugh", "classification", "ascites", "bilirubin", "albumin", "INR", "encephalopathy"]
        },
        {
            "title": "MELD Score in Liver Disease Prognosis",
            "content": "MELD score uses creatinine, bilirubin, INR, and sodium to predict mortality in chronic liver disease.",
            "tags": ["liver", "MELD", "prognosis", "creatinine", "bilirubin", "INR", "sodium"]
        },
        {
            "title": "IBD Monitoring: Fecal Calprotectin Utility",
            "content": "Fecal calprotectin is a non-invasive marker for intestinal inflammation in IBD, useful for monitoring disease activity.",
            "tags": ["IBD", "calprotectin", "monitoring", "inflammation", "activity"]
        },
        {
            "title": "Imaging Modalities in Liver Disease",
            "content": "Ultrasound, CT, and MRI are used to assess liver parenchyma, detect masses, and evaluate for cirrhosis.",
            "tags": ["liver", "imaging", "ultrasound", "CT", "MRI", "cirrhosis"]
        },
        {
            "title": "Endoscopic Management of Bleeding Ulcers",
            "content": "Bleeding ulcers are managed endoscopically with injection, thermal coagulation, or hemoclips. Risk stratification guides intervention.",
            "tags": ["endoscopy", "ulcer", "bleeding", "management", "coagulation", "hemoclips"]
        },
        {
            "title": "GERD: Indications for Surgical Management",
            "content": "Surgical management is considered for refractory GERD, large hiatal hernia, or complications such as strictures.",
            "tags": ["GERD", "surgery", "hiatal hernia", "stricture", "management"]
        },
        {
            "title": "Celiac Disease: Monitoring and Complications",
            "content": "Monitoring includes serology, nutritional status, and screening for complications like anemia, osteoporosis, and lymphoma.",
            "tags": ["celiac", "monitoring", "complications", "anemia", "osteoporosis", "lymphoma"]
        },
        {
            "title": "Pancreatitis: Imaging and Severity",
            "content": "CT and MRI are used to assess pancreatitis severity, necrosis, and complications. Early imaging is reserved for severe cases.",
            "tags": ["pancreatitis", "imaging", "severity", "necrosis", "complications", "CT", "MRI"]
        },
        {
            "title": "Endoscopic Surveillance in IBD",
            "content": "Regular endoscopic surveillance in IBD is recommended to detect dysplasia and colorectal cancer, especially in long-standing disease.",
            "tags": ["IBD", "endoscopy", "surveillance", "dysplasia", "colorectal cancer"]
        },
        {
            "title": "Polyp Histology and Surveillance Intervals",
            "content": "Histology determines surveillance intervals: adenomas, serrated polyps, and hyperplastic polyps have different recommendations.",
            "tags": ["polyp", "histology", "surveillance", "adenoma", "serrated", "hyperplastic"]
        },
        {
            "title": "Advanced Imaging for HCC Diagnosis",
            "content": "Multiphasic CT and MRI are used for HCC diagnosis, with arterial enhancement and washout as key features.",
            "tags": ["HCC", "imaging", "CT", "MRI", "diagnosis", "arterial enhancement", "washout"]
        },
        {
            "title": "IBD: Biologic Therapy Escalation",
            "content": "Escalation to biologic therapy is indicated for moderate to severe IBD unresponsive to conventional treatment.",
            "tags": ["IBD", "biologic", "therapy", "escalation", "moderate", "severe"]
        },
        {
            "title": "Liver Elastography in Fibrosis Assessment",
            "content": "Elastography provides non-invasive assessment of liver fibrosis, reducing need for biopsy.",
            "tags": ["liver", "elastography", "fibrosis", "assessment", "biopsy"]
        },
        {
            "title": "Endoscopic Management of Varices",
            "content": "Varices are managed endoscopically with band ligation or sclerotherapy. Surveillance is essential in cirrhotic patients.",
            "tags": ["endoscopy", "varices", "band ligation", "sclerotherapy", "surveillance", "cirrhosis"]
        },
        {
            "title": "Pancreatitis: Organ Failure and Prognosis",
            "content": "Organ failure in pancreatitis predicts poor prognosis. Monitoring includes renal, respiratory, and cardiovascular function.",
            "tags": ["pancreatitis", "organ failure", "prognosis", "monitoring", "renal", "respiratory", "cardiovascular"]
        }
    ]
    for doc in docs:
        index.add_document(doc["title"], doc["content"], doc["tags"])