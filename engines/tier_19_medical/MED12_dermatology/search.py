import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# -----------------------------
# Data Classes
# -----------------------------

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

# -----------------------------
# Search Index
# -----------------------------

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats()

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            for token in tokens:
                self.inverted_index[token][doc.id] = self.inverted_index[token].get(doc.id, 0) + 1
            self._recompute_stats()
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_tokens = self._tokenize(query)
        scores = defaultdict(float)
        doc_snippets = {}
        if not query_tokens:
            return []
        for token in query_tokens:
            if token not in self.inverted_index:
                continue
            posting = self.inverted_index[token]
            idf = self._compute_idf(token)
            for doc_id, freq in posting.items():
                doc = self.documents[doc_id]
                if method == 'bm25':
                    score = self._score_bm25(token, doc_id, freq, idf, doc.weight)
                elif method == 'tfidf':
                    score = self._score_tfidf(token, doc_id, freq, idf, doc.weight)
                else:
                    score = self._score_bm25(token, doc_id, freq, idf, doc.weight)
                scores[doc_id] += score
                if doc_id not in doc_snippets:
                    doc_snippets[doc_id] = self._make_snippet(doc, query_tokens)
        if not scores:
            return []
        top_docs = heapq.nlargest(limit, scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = doc_snippets[doc_id]
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "num_unique_terms": len(self.inverted_index)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, term: str, doc_id: str, freq: int, idf: float, weight: float) -> float:
        k1 = 1.5
        b = 0.75
        dl = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length > 0 else 1
        tf = freq
        denom = tf + k1 * (1 - b + b * dl / avg_dl)
        score = idf * ((tf * (k1 + 1)) / denom)
        return score * weight

    def _score_tfidf(self, term: str, doc_id: str, freq: int, idf: float, weight: float) -> float:
        tf = 1 + math.log(freq)
        norm = math.sqrt(sum((1 + math.log(f)) ** 2 for f in Counter(self.doc_tokens[doc_id]).values()))
        tf_norm = tf / norm if norm > 0 else tf
        return tf_norm * idf * weight

    def _make_snippet(self, doc: SearchDocument, query_tokens: List[str], window: int = 30) -> str:
        content = doc.content
        content_tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(content_tokens) if t in query_tokens]
        if not positions:
            snippet = content[:160]
        else:
            start = max(positions[0] - window // 2, 0)
            end = min(start + window, len(content_tokens))
            snippet_tokens = content_tokens[start:end]
            snippet = ' '.join(snippet_tokens)
        # Highlight
        for qt in set(query_tokens):
            snippet = re.sub(r'\b({})\b'.format(re.escape(qt)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet

    def _recompute_stats(self):
        self.N = len(self.documents)
        if self.N > 0:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N
        else:
            self.avg_doc_length = 0.0

# -----------------------------
# Singleton Factory
# -----------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

# -----------------------------
# Pre-seed Documents
# -----------------------------

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            id="melanoma_1",
            title="ABCDE Criteria for Melanoma Detection",
            content="The ABCDE criteria for melanoma include Asymmetry, Border irregularity, Color variation, Diameter >6mm, and Evolution. Early recognition is crucial.",
            tags=["melanoma", "abcde", "diagnosis"],
            weight=1.0
        ),
        SearchDocument(
            id="melanoma_2",
            title="Asymmetry in Melanoma Lesions",
            content="Asymmetry is a key feature of melanoma. Benign nevi are typically symmetric, while melanomas are not.",
            tags=["melanoma", "asymmetry"],
            weight=1.0
        ),
        SearchDocument(
            id="melanoma_3",
            title="Border Irregularity in Melanoma",
            content="Melanomas often have uneven, notched, or scalloped borders, distinguishing them from benign lesions.",
            tags=["melanoma", "border"],
            weight=1.0
        ),
        SearchDocument(
            id="melanoma_4",
            title="Color Variation in Melanoma",
            content="Multiple colors such as brown, black, red, white, or blue within a lesion suggest melanoma.",
            tags=["melanoma", "color"],
            weight=1.0
        ),
        SearchDocument(
            id="melanoma_5",
            title="Diameter and Evolution in Melanoma",
            content="Lesions larger than 6mm or those that change in size, shape, or color (evolution) are concerning for melanoma.",
            tags=["melanoma", "diameter", "evolution"],
            weight=1.0
        ),
        SearchDocument(
            id="bcc_1",
            title="Basal Cell Carcinoma: Clinical Diagnosis",
            content="Basal cell carcinoma presents as pearly papules with telangiectasia, often ulcerated. Diagnosis is clinical but may require biopsy.",
            tags=["basal_cell_carcinoma", "diagnosis"],
            weight=1.0
        ),
        SearchDocument(
            id="bcc_2",
            title="High-Risk Features in Basal Cell Carcinoma",
            content="Aggressive BCC subtypes include morpheaform, infiltrative, and micronodular. Perineural invasion increases risk.",
            tags=["basal_cell_carcinoma", "risk"],
            weight=1.0
        ),
        SearchDocument(
            id="bcc_3",
            title="Treatment Options for Basal Cell Carcinoma",
            content="Surgical excision is standard for BCC. Mohs micrographic surgery is preferred for high-risk or facial lesions.",
            tags=["basal_cell_carcinoma", "treatment"],
            weight=1.0
        ),
        SearchDocument(
            id="scc_1",
            title="Squamous Cell Carcinoma: Risk Factors",
            content="Risk factors for SCC include UV exposure, immunosuppression, chronic wounds, and HPV infection.",
            tags=["squamous_cell_carcinoma", "risk"],
            weight=1.0
        ),
        SearchDocument(
            id="scc_2",
            title="Clinical Presentation of Squamous Cell Carcinoma",
            content="SCC often presents as a scaly, erythematous plaque or nodule that may ulcerate.",
            tags=["squamous_cell_carcinoma", "diagnosis"],
            weight=1.0
        ),
        SearchDocument(
            id="scc_3",
            title="Management of High-Risk Squamous Cell Carcinoma",
            content="High-risk SCC requires wide excision and may need adjuvant radiation. Sentinel lymph node biopsy is considered.",
            tags=["squamous_cell_carcinoma", "management"],
            weight=1.0
        ),
        SearchDocument(
            id="ad_1",
            title="Atopic Dermatitis: Management Principles",
            content="Management of atopic dermatitis includes emollients, topical corticosteroids, and trigger avoidance.",
            tags=["atopic_dermatitis", "management"],
            weight=1.0
        ),
        SearchDocument(
            id="ad_2",
            title="Topical Therapies for Atopic Dermatitis",
            content="Topical calcineurin inhibitors are alternatives to steroids for sensitive areas in atopic dermatitis.",
            tags=["atopic_dermatitis", "topical"],
            weight=1.0
        ),
        SearchDocument(
            id="ad_3",
            title="Systemic Treatments for Severe Atopic Dermatitis",
            content="Systemic immunomodulators and biologics are options for refractory atopic dermatitis.",
            tags=["atopic_dermatitis", "systemic"],
            weight=1.0
        ),
        SearchDocument(
            id="psoriasis_1",
            title="Biologic Selection in Psoriasis",
            content="Biologic agents for psoriasis include TNF-alpha inhibitors, IL-17, IL-23, and IL-12/23 inhibitors. Selection depends on comorbidities.",
            tags=["psoriasis", "biologics", "selection"],
            weight=1.0
        ),
        SearchDocument(
            id="psoriasis_2",
            title="TNF-alpha Inhibitors for Psoriasis",
            content="Etanercept, infliximab, and adalimumab are TNF-alpha inhibitors used in moderate-to-severe psoriasis.",
            tags=["psoriasis", "tnf_alpha"],
            weight=1.0
        ),
        SearchDocument(
            id="psoriasis_3",
            title="IL-17 and IL-23 Inhibitors in Psoriasis",
            content="Secukinumab and ixekizumab (IL-17 inhibitors), guselkumab and tildrakizumab (IL-23 inhibitors) are highly effective.",
            tags=["psoriasis", "il17", "il23"],
            weight=1.0
        ),
        SearchDocument(
            id="wound_1",
            title="Phases of Wound Healing",
            content="Wound healing occurs in hemostasis, inflammation, proliferation, and remodeling phases.",
            tags=["wound_healing", "phases"],
            weight=1.0
        ),
        SearchDocument(
            id="wound_2",
            title="Inflammatory Phase of Wound Healing",
            content="The inflammatory phase involves neutrophil and macrophage infiltration to clear debris and bacteria.",
            tags=["wound_healing", "inflammation"],
            weight=1.0
        ),
        SearchDocument(
            id="wound_3",
            title="Proliferative and Remodeling Phases",
            content="Fibroblast proliferation, collagen deposition, and angiogenesis characterize the proliferative phase; remodeling strengthens the scar.",
            tags=["wound_healing", "proliferation", "remodeling"],
            weight=1.0
        ),
        SearchDocument(
            id="phototherapy_1",
            title="Phototherapy Protocols in Dermatology",
            content="Narrowband UVB is commonly used for psoriasis and atopic dermatitis. Protocols specify dose, frequency, and monitoring.",
            tags=["phototherapy", "protocols"],
            weight=1.0
        ),
        SearchDocument(
            id="phototherapy_2",
            title="PUVA Therapy Protocol",
            content="PUVA combines psoralen with UVA exposure. Indications include psoriasis, vitiligo, and cutaneous T-cell lymphoma.",
            tags=["phototherapy", "puva"],
            weight=1.0
        ),
        SearchDocument(
            id="dermatopath_1",
            title="Dermatopathology: Melanoma Interpretation",
            content="Histopathology of melanoma shows atypical melanocytes, pagetoid spread, and mitoses. Breslow depth guides prognosis.",
            tags=["dermatopathology", "melanoma"],
            weight=1.0
        ),
        SearchDocument(
            id="dermatopath_2",
            title="Basal Cell Carcinoma: Pathology Features",
            content="BCC histology reveals basaloid cells with peripheral palisading and stromal retraction.",
            tags=["dermatopathology", "bcc"],
            weight=1.0
        ),
        SearchDocument(
            id="cosmetic_1",
            title="Botulinum Toxin in Cosmetic Dermatology",
            content="Botulinum toxin is used to reduce dynamic wrinkles by inhibiting acetylcholine release at neuromuscular junctions.",
            tags=["cosmetic", "botulinum_toxin"],
            weight=1.0
        ),
        SearchDocument(
            id="cosmetic_2",
            title="Injection Techniques for Botulinum Toxin",
            content="Proper dilution, injection depth, and anatomical knowledge are essential for safe cosmetic botulinum toxin use.",
            tags=["cosmetic", "botulinum_toxin", "technique"],
            weight=1.0
        ),
        SearchDocument(
            id="acne_1",
            title="Acne Treatment Ladder: Overview",
            content="Acne management starts with topical retinoids and benzoyl peroxide, progressing to oral antibiotics and isotretinoin for severe cases.",
            tags=["acne", "treatment_ladder"],
            weight=1.0
        ),
        SearchDocument(
            id="acne_2",
            title="Topical Therapies in Acne",
            content="Topical retinoids, benzoyl peroxide, and antibiotics are first-line for mild-to-moderate acne.",
            tags=["acne", "topical"],
            weight=1.0
        ),
        SearchDocument(
            id="acne_3",
            title="Oral Isotretinoin in Severe Acne",
            content="Oral isotretinoin is reserved for severe, nodulocystic acne or cases unresponsive to other therapies.",
            tags=["acne", "isotretinoin"],
            weight=1.0
        ),
        SearchDocument(
            id="acne_4",
            title="Hormonal Therapy for Acne",
            content="Hormonal therapy, including oral contraceptives and spironolactone, is effective for female patients with acne.",
            tags=["acne", "hormonal"],
            weight=1.0
        ),
        SearchDocument(
            id="psoriasis_4",
            title="Comorbidities in Psoriasis Biologic Selection",
            content="Consider cardiovascular disease, IBD, and MS when choosing biologics for psoriasis.",
            tags=["psoriasis", "biologics", "comorbidities"],
            weight=1.0
        ),
        SearchDocument(
            id="wound_4",
            title="Chronic Wounds and Healing Impairment",
            content="Diabetes, vascular insufficiency, and infection can impair wound healing, requiring multidisciplinary management.",
            tags=["wound_healing", "chronic"],
            weight=1.0
        ),
        SearchDocument(
            id="dermatopath_3",
            title="Squamous Cell Carcinoma: Histopathology",
            content="SCC shows keratin pearls, intercellular bridges, and variable differentiation on histology.",
            tags=["dermatopathology", "scc"],
            weight=1.0
        ),
        SearchDocument(
            id="phototherapy_3",
            title="Phototherapy: Adverse Effects",
            content="Potential adverse effects of phototherapy include erythema, photoaging, and increased skin cancer risk.",
            tags=["phototherapy", "adverse_effects"],
            weight=1.0
        ),
        SearchDocument(
            id="cosmetic_3",
            title="Complications of Botulinum Toxin",
            content="Ptosis, asymmetry, and unwanted muscle weakness are possible complications of cosmetic botulinum toxin.",
            tags=["cosmetic", "botulinum_toxin", "complications"],
            weight=1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)