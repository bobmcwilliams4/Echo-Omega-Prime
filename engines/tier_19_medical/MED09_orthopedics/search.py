import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

class SearchDocument:
    def __init__(self, id: int, title: str, content: str, tags: List[str], weight: float = 1.0):
        self.id = id
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
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.idf_cache: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._recompute_stats = True

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-z0-9]+\b', text.lower())

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            token_counts = Counter(tokens)
            self.doc_lengths[doc.id] = len(tokens)
            for token, count in token_counts.items():
                self.inverted_index[token][doc.id] = count
                self.doc_freqs[token] += 1
            self.N += 1
            self._recompute_stats = True

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

    def _score_bm25(self, query_terms: List[str], doc_id: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        tf = self.inverted_index
        for term in query_terms:
            f = tf.get(term, {}).get(doc_id, 0)
            if f == 0:
                continue
            idf = self._compute_idf(term)
            denom = f + k1 * (1 - b + b * doc_len / avgdl)
            numer = f * (k1 + 1)
            score += idf * numer / denom
        score *= doc.weight
        return score

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = self.inverted_index
        score = 0.0
        for term in query_terms:
            tf_raw = tf.get(term, {}).get(doc_id, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        score *= doc.weight
        return score

    def _update_stats(self):
        if not self._recompute_stats:
            return
        total_len = sum(self.doc_lengths.values())
        self.avg_doc_length = total_len / self.N if self.N > 0 else 0.0
        self.idf_cache.clear()
        self._recompute_stats = False

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        with self.lock:
            self._update_stats()
            query_terms = self._tokenize(query)
            candidate_docs = set()
            for term in query_terms:
                candidate_docs.update(self.inverted_index.get(term, {}).keys())
            scored: List[Tuple[int, float]] = []
            for doc_id in candidate_docs:
                if method == 'bm25':
                    score = self._score_bm25(query_terms, doc_id)
                elif method == 'tfidf':
                    score = self._score_tfidf(query_terms, doc_id)
                else:
                    score = self._score_bm25(query_terms, doc_id)
                if score > 0:
                    scored.append((doc_id, score))
            scored.sort(key=lambda x: x[1], reverse=True)
            results = []
            for doc_id, score in scored[:limit]:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc, query_terms)
                results.append(SearchResult(doc_id, score, doc.title, snippet))
            return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + '...' if len(content) > 160 else content
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in set(query_terms):
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ('...' if end < len(tokens) else '')

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            self._update_stats()
            return {
                'num_documents': self.N,
                'avg_doc_length': self.avg_doc_length,
                'num_terms': len(self.doc_freqs)
            }

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "AO/OTA Fracture Classification: Overview",
            "The AO/OTA fracture classification system is a comprehensive method for categorizing fractures based on anatomical location, fracture morphology, and complexity. It is widely used in orthopedic trauma for communication and research.",
            ["AO/OTA", "fracture", "classification", "trauma"],
            1.2
        ),
        SearchDocument(
            2,
            "Gustilo-Anderson Open Fracture Classification",
            "The Gustilo-Anderson classification categorizes open fractures into types I, II, and III (with IIIA, IIIB, IIIC subtypes) based on wound size, contamination, and soft tissue injury. It guides management and prognosis.",
            ["Gustilo-Anderson", "open fracture", "classification"],
            1.1
        ),
        SearchDocument(
            3,
            "Total Hip Arthroplasty: Cemented vs Uncemented",
            "Total hip arthroplasty (THA) can be performed using cemented or uncemented fixation. Cemented stems use bone cement for immediate stability, while uncemented stems rely on bone ingrowth. Patient age, bone quality, and surgeon preference influence choice.",
            ["THA", "hip arthroplasty", "cemented", "uncemented"],
            1.0
        ),
        SearchDocument(
            4,
            "Total Knee Arthroplasty: Mechanical vs Kinematic Alignment",
            "Mechanical alignment aims for neutral limb alignment in total knee arthroplasty (TKA), while kinematic alignment restores the patient's native joint lines. Each approach has implications for implant longevity and patient satisfaction.",
            ["TKA", "knee arthroplasty", "mechanical alignment", "kinematic alignment"],
            1.0
        ),
        SearchDocument(
            5,
            "Lumbar Spine: Fusion vs Disc Arthroplasty",
            "Lumbar spine surgery for degenerative disc disease includes fusion and disc arthroplasty. Fusion eliminates motion at the segment, while arthroplasty preserves motion. Patient selection and long-term outcomes differ.",
            ["lumbar spine", "fusion", "disc arthroplasty"],
            1.0
        ),
        SearchDocument(
            6,
            "Adolescent Idiopathic Scoliosis: Lenke Classification",
            "The Lenke classification system for adolescent idiopathic scoliosis (AIS) uses curve type, lumbar modifier, and sagittal thoracic modifier to guide surgical planning and instrumentation.",
            ["scoliosis", "Lenke", "AIS", "classification"],
            1.1
        ),
        SearchDocument(
            7,
            "ACL Reconstruction: Graft Selection",
            "Graft options for anterior cruciate ligament (ACL) reconstruction include bone-patellar tendon-bone (BTB), hamstring, and quadriceps tendon autografts. Each has unique advantages and complications.",
            ["ACL", "reconstruction", "graft", "BTB", "hamstring", "quad tendon"],
            1.0
        ),
        SearchDocument(
            8,
            "Rotator Cuff Repair: Indications and Techniques",
            "Indications for rotator cuff repair include symptomatic full-thickness tears and failed conservative management. Techniques include open, mini-open, and arthroscopic repair, with selection based on tear size and tissue quality.",
            ["rotator cuff", "repair", "technique", "indications"],
            1.0
        ),
        SearchDocument(
            9,
            "Compartment Syndrome: Diagnosis and Management",
            "Compartment syndrome is diagnosed clinically by pain out of proportion, pain with passive stretch, and tense compartments. Emergent fasciotomy is the definitive treatment to prevent irreversible damage.",
            ["compartment syndrome", "diagnosis", "management", "fasciotomy"],
            1.2
        ),
        SearchDocument(
            10,
            "Bone Healing: The Diamond Concept",
            "The diamond concept of bone healing emphasizes the importance of osteogenic cells, osteoconductive scaffold, growth factors, mechanical stability, and vascularity for optimal fracture repair.",
            ["bone healing", "diamond concept", "fracture repair"],
            1.1
        ),
        SearchDocument(
            11,
            "Musculoskeletal MRI: Meniscal Tear Classification",
            "MRI is the gold standard for meniscal tear classification, distinguishing between longitudinal, radial, horizontal, and complex tears. Accurate classification guides management.",
            ["MRI", "meniscus", "tear", "classification"],
            1.0
        ),
        SearchDocument(
            12,
            "AO/OTA: Proximal Femur Fractures",
            "AO/OTA classifies proximal femur fractures (hip fractures) into 31A (trochanteric), 31B (femoral neck), and 31C (head) types. This guides treatment and prognosis.",
            ["AO/OTA", "proximal femur", "hip fracture", "classification"],
            1.0
        ),
        SearchDocument(
            13,
            "Gustilo-Anderson: Type III Open Fractures",
            "Type III open fractures involve extensive soft tissue damage, high-energy trauma, and may require vascular repair (IIIC). These injuries have higher infection and complication rates.",
            ["Gustilo-Anderson", "type III", "open fracture"],
            1.1
        ),
        SearchDocument(
            14,
            "Total Hip Arthroplasty: Indications",
            "Indications for total hip arthroplasty include osteoarthritis, rheumatoid arthritis, avascular necrosis, and certain femoral neck fractures. Patient selection is critical for good outcomes.",
            ["THA", "indications", "hip arthroplasty"],
            1.0
        ),
        SearchDocument(
            15,
            "Total Knee Arthroplasty: Implant Longevity",
            "Implant longevity in total knee arthroplasty depends on alignment, fixation, patient factors, and surgical technique. Both mechanical and kinematic alignment strategies are used.",
            ["TKA", "implant longevity", "alignment"],
            1.0
        ),
        SearchDocument(
            16,
            "Lumbar Fusion: Indications and Techniques",
            "Lumbar fusion is indicated for instability, deformity, or failed disc arthroplasty. Techniques include PLIF, TLIF, ALIF, and posterolateral fusion.",
            ["lumbar fusion", "indications", "techniques"],
            1.0
        ),
        SearchDocument(
            17,
            "Disc Arthroplasty: Patient Selection",
            "Ideal candidates for lumbar disc arthroplasty are young, active patients with single-level degenerative disc disease and no significant facet arthropathy.",
            ["disc arthroplasty", "patient selection"],
            1.0
        ),
        SearchDocument(
            18,
            "Lenke Classification: Curve Types",
            "Lenke curve types (1-6) describe the major structural curves in adolescent idiopathic scoliosis, influencing surgical approach and instrumentation.",
            ["Lenke", "curve types", "scoliosis"],
            1.0
        ),
        SearchDocument(
            19,
            "ACL Graft: BTB vs Hamstring",
            "BTB grafts have higher initial strength and bone-to-bone healing, but increased anterior knee pain. Hamstring grafts have less donor site morbidity but may have increased laxity.",
            ["ACL", "BTB", "hamstring", "graft"],
            1.0
        ),
        SearchDocument(
            20,
            "Quad Tendon Graft for ACL Reconstruction",
            "Quadriceps tendon grafts are an alternative for ACL reconstruction, offering a large graft diameter and lower anterior knee pain risk compared to BTB.",
            ["ACL", "quad tendon", "graft"],
            1.0
        ),
        SearchDocument(
            21,
            "Rotator Cuff Repair: Arthroscopic vs Open",
            "Arthroscopic rotator cuff repair is less invasive, with faster recovery and less pain, but open repair may be preferred for massive or complex tears.",
            ["rotator cuff", "arthroscopic", "open repair"],
            1.0
        ),
        SearchDocument(
            22,
            "Compartment Syndrome: Intracompartmental Pressure",
            "Measurement of intracompartmental pressure can aid diagnosis of compartment syndrome, especially in obtunded patients. Thresholds >30 mmHg or within 30 mmHg of diastolic pressure are concerning.",
            ["compartment syndrome", "pressure", "diagnosis"],
            1.1
        ),
        SearchDocument(
            23,
            "Bone Healing: Role of Vascularity",
            "Adequate vascularity is essential for bone healing. The diamond concept highlights the interplay of blood supply, cells, scaffold, and growth factors.",
            ["bone healing", "vascularity", "diamond concept"],
            1.0
        ),
        SearchDocument(
            24,
            "Meniscal Tear: Radial vs Longitudinal",
            "Radial tears disrupt the circumferential fibers and compromise meniscal function, while longitudinal tears may be amenable to repair, especially in the vascular zone.",
            ["meniscus", "radial tear", "longitudinal tear"],
            1.0
        ),
        SearchDocument(
            25,
            "MRI: Horizontal and Complex Meniscal Tears",
            "Horizontal meniscal tears are often degenerative, while complex tears involve multiple planes. MRI helps differentiate tear types for treatment planning.",
            ["MRI", "meniscus", "horizontal tear", "complex tear"],
            1.0
        ),
        SearchDocument(
            26,
            "AO/OTA: Distal Radius Fracture Classification",
            "AO/OTA classifies distal radius fractures into types A (extra-articular), B (partial articular), and C (complete articular), guiding management and prognosis.",
            ["AO/OTA", "distal radius", "fracture", "classification"],
            1.0
        ),
        SearchDocument(
            27,
            "Gustilo-Anderson: Wound Management",
            "Wound management in open fractures includes irrigation, debridement, and timely antibiotics. Gustilo-Anderson type influences timing and method of closure.",
            ["Gustilo-Anderson", "wound management", "open fracture"],
            1.0
        ),
        SearchDocument(
            28,
            "Total Hip Arthroplasty: Cementless Fixation",
            "Cementless fixation in THA relies on press-fit and biological bone ingrowth. Indicated in younger patients with good bone quality.",
            ["THA", "cementless", "fixation", "hip arthroplasty"],
            1.0
        ),
        SearchDocument(
            29,
            "Total Knee Arthroplasty: Patient Satisfaction",
            "Patient satisfaction after TKA is influenced by alignment, soft tissue balancing, and expectations. Kinematic alignment may improve satisfaction in select patients.",
            ["TKA", "patient satisfaction", "alignment"],
            1.0
        ),
        SearchDocument(
            30,
            "Lumbar Disc Arthroplasty: Outcomes",
            "Long-term outcomes of lumbar disc arthroplasty show preserved motion and reduced adjacent segment disease compared to fusion in selected patients.",
            ["lumbar disc", "arthroplasty", "outcomes"],
            1.0
        ),
        SearchDocument(
            31,
            "AIS: Surgical Planning with Lenke Classification",
            "Lenke classification guides surgical planning in adolescent idiopathic scoliosis by identifying structural curves and modifiers.",
            ["AIS", "Lenke", "surgical planning"],
            1.0
        ),
        SearchDocument(
            32,
            "ACL Reconstruction: Allograft vs Autograft",
            "Allografts reduce surgical morbidity but may have higher failure rates in young, active patients compared to autografts for ACL reconstruction.",
            ["ACL", "allograft", "autograft", "reconstruction"],
            1.0
        ),
        SearchDocument(
            33,
            "Rotator Cuff Repair: Massive Tears",
            "Massive rotator cuff tears may require partial repair, tendon transfer, or superior capsular reconstruction. Patient factors and tissue quality guide technique selection.",
            ["rotator cuff", "massive tear", "repair", "technique"],
            1.0
        ),
        SearchDocument(
            34,
            "Compartment Syndrome: Late Sequelae",
            "Late sequelae of compartment syndrome include Volkmann contracture, muscle necrosis, and chronic pain. Early diagnosis and fasciotomy are critical.",
            ["compartment syndrome", "sequelae", "fasciotomy"],
            1.0
        ),
        SearchDocument(
            35,
            "Bone Healing: Mechanical Stability",
            "Mechanical stability is a key pillar of the diamond concept, allowing cellular and molecular processes to proceed for bone healing.",
            ["bone healing", "mechanical stability", "diamond concept"],
            1.0
        ),
        SearchDocument(
            36,
            "MRI: Meniscal Root Tears",
            "Meniscal root tears are best visualized on MRI and can lead to rapid joint degeneration if untreated. Repair is indicated in young, active patients.",
            ["MRI", "meniscus", "root tear"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)