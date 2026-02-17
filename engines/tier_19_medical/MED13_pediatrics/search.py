import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.doc_term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self.idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            term_freq = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_term_freqs[doc.id] = term_freq
            self.doc_lengths[doc.id] = len(tokens)
            for term in term_freq:
                self.inverted_index[term].add(doc.id)
                self.term_doc_freq[term] += 1
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0.0
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidate_docs: Set[int] = set()
        for term in query_terms:
            candidate_docs.update(self.inverted_index.get(term, set()))
        scores: Dict[int, float] = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc_weight = self.documents[doc_id].weight
            # Combine BM25 and TF-IDF (weighted sum)
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            scores[doc_id] = score * doc_weight
        top_docs = heapq.nlargest(limit, scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avgdl,
                "vocabulary_size": len(self.inverted_index),
            }

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, remove punctuation, split on whitespace
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 0)
        avgdl = self.avgdl if self.avgdl > 0 else 1.0
        term_freqs = self.doc_term_freqs.get(doc_id, Counter())
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            denom = tf + self.k1 * (1 - self.b + self.b * doc_len / avgdl)
            score += idf * (tf * (self.k1 + 1)) / denom
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        score = 0.0
        doc_len = self.doc_lengths.get(doc_id, 1)
        term_freqs = self.doc_term_freqs.get(doc_id, Counter())
        for term in query_terms:
            tf = term_freqs.get(term, 0)
            if tf == 0:
                continue
            tf_norm = tf / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], window: int = 30) -> str:
        tokens = self._tokenize(content)
        positions = []
        for i, token in enumerate(tokens):
            if token in query_terms:
                positions.append(i)
        if not positions:
            snippet_tokens = tokens[:window]
        else:
            start = max(positions[0] - window // 2, 0)
            end = min(start + window, len(tokens))
            snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        return snippet[:200] + ('...' if len(snippet) > 200 else '')

# Singleton factory for SearchIndex
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
            "Growth Chart Percentile Interpretation",
            "Growth charts are tools used to track a child's growth over time. Percentiles indicate the relative position of the child's measurement compared to peers. Consistent tracking on a percentile curve is more important than the absolute percentile. A sudden change in percentile may indicate underlying health issues.",
            ["growth", "percentile", "pediatrics", "assessment"],
            1.0
        ),
        SearchDocument(
            2,
            "Developmental Milestone Assessment",
            "Developmental milestones are behaviors or physical skills seen in infants and children as they grow and develop. Examples include rolling over, sitting, walking, and talking. Assess milestones at each well-child visit to detect delays early.",
            ["development", "milestones", "assessment"],
            1.0
        ),
        SearchDocument(
            3,
            "Routine Childhood Immunization Schedule",
            "The routine immunization schedule includes vaccines such as DTaP, IPV, MMR, Hib, HepB, Varicella, and PCV13. Follow the CDC or local guidelines for timing and catch-up schedules. Immunizations prevent serious childhood diseases.",
            ["immunization", "vaccines", "schedule", "prevention"],
            1.0
        ),
        SearchDocument(
            4,
            "Neonatal Jaundice Management",
            "Neonatal jaundice is common and usually benign. Assess total serum bilirubin and risk factors. Use phototherapy for high levels. Monitor for signs of kernicterus. Early feeding helps reduce jaundice.",
            ["neonatal", "jaundice", "management"],
            1.0
        ),
        SearchDocument(
            5,
            "Neonatal Sepsis Evaluation",
            "Neonatal sepsis presents with nonspecific symptoms such as temperature instability, lethargy, and poor feeding. Evaluation includes blood cultures, CBC, and lumbar puncture if indicated. Start empiric antibiotics promptly.",
            ["neonatal", "sepsis", "infection", "evaluation"],
            1.0
        ),
        SearchDocument(
            6,
            "Weight-Based Medication Dosing",
            "Pediatric medication dosing is typically calculated based on weight in kilograms. Always verify the dose and check for maximum allowed dose. Double-check calculations to avoid dosing errors.",
            ["medication", "dosing", "weight", "pediatrics"],
            1.0
        ),
        SearchDocument(
            7,
            "Acute Otitis Media Diagnosis and Treatment",
            "Acute otitis media is diagnosed by bulging tympanic membrane, ear pain, and fever. First-line treatment is amoxicillin. Watchful waiting is appropriate for mild cases in older children.",
            ["otitis", "media", "ear", "infection", "treatment"],
            1.0
        ),
        SearchDocument(
            8,
            "Streptococcal Pharyngitis Management",
            "Streptococcal pharyngitis presents with sore throat, fever, and anterior cervical lymphadenopathy. Diagnosis is confirmed with rapid antigen test or throat culture. Treat with penicillin or amoxicillin.",
            ["pharyngitis", "strep", "throat", "infection", "management"],
            1.0
        ),
        SearchDocument(
            9,
            "Asthma Severity Classification and Management",
            "Asthma severity is classified as intermittent, mild persistent, moderate persistent, or severe persistent. Management includes inhaled corticosteroids, bronchodilators, and trigger avoidance. Develop an asthma action plan.",
            ["asthma", "management", "severity", "classification"],
            1.0
        ),
        SearchDocument(
            10,
            "Bronchiolitis Clinical Management",
            "Bronchiolitis is a viral lower respiratory tract infection, most commonly caused by RSV. Supportive care is mainstay; avoid routine bronchodilators or steroids. Monitor for respiratory distress.",
            ["bronchiolitis", "RSV", "respiratory", "management"],
            1.0
        ),
        SearchDocument(
            11,
            "Infant Feeding and Breastfeeding Support",
            "Breastfeeding is recommended exclusively for the first 6 months. Support mothers with proper latch and feeding techniques. Formula is an alternative if breastfeeding is not possible.",
            ["feeding", "breastfeeding", "infant", "nutrition"],
            1.0
        ),
        SearchDocument(
            12,
            "Pediatric Febrile Seizure Management",
            "Febrile seizures are common in children aged 6 months to 5 years. Most are benign and do not require long-term anticonvulsants. Evaluate for underlying infection and provide parental reassurance.",
            ["febrile", "seizure", "pediatrics", "management"],
            1.0
        ),
        SearchDocument(
            13,
            "ADHD Diagnosis in Children",
            "Attention-Deficit/Hyperactivity Disorder is diagnosed based on persistent patterns of inattention and/or hyperactivity-impulsivity. Symptoms must be present in multiple settings and interfere with functioning.",
            ["ADHD", "diagnosis", "behavior", "children"],
            1.0
        ),
        SearchDocument(
            14,
            "Pediatric Dehydration Assessment and Fluid Management",
            "Assess dehydration severity by clinical signs: capillary refill, mucous membranes, and urine output. Mild cases can be managed with oral rehydration. Severe dehydration requires IV fluids.",
            ["dehydration", "fluid", "management", "assessment"],
            1.0
        ),
        SearchDocument(
            15,
            "Sudden Infant Death Syndrome Prevention",
            "To reduce SIDS risk, place infants on their backs to sleep, use a firm mattress, and avoid soft bedding. Do not bed-share. Promote a smoke-free environment.",
            ["SIDS", "prevention", "infant", "safety"],
            1.0
        ),
        SearchDocument(
            16,
            "Catch-Up Immunization Guidelines",
            "Children who are behind on vaccines should follow catch-up schedules as per CDC guidelines. Ensure minimum intervals between doses are maintained.",
            ["immunization", "catch-up", "schedule", "vaccines"],
            0.9
        ),
        SearchDocument(
            17,
            "Failure to Thrive Evaluation",
            "Failure to thrive is defined as inadequate growth or inability to maintain growth. Causes include inadequate intake, malabsorption, or chronic illness. Evaluate with thorough history and physical.",
            ["growth", "failure to thrive", "nutrition", "evaluation"],
            1.0
        ),
        SearchDocument(
            18,
            "Normal Growth Patterns in Pediatrics",
            "Children typically double their birth weight by 5 months and triple it by 1 year. Height increases by about 50% in the first year. Deviations from expected patterns may indicate health concerns.",
            ["growth", "patterns", "pediatrics", "normal"],
            1.0
        ),
        SearchDocument(
            19,
            "Lead Screening in Children",
            "Lead exposure can cause cognitive and behavioral problems. Screen at-risk children at ages 1 and 2 years. Remove sources of lead if elevated levels are detected.",
            ["screening", "lead", "pediatrics", "prevention"],
            1.0
        ),
        SearchDocument(
            20,
            "Hearing and Vision Screening",
            "Routine hearing and vision screening is recommended at key ages. Early detection of deficits allows for timely intervention and improved outcomes.",
            ["screening", "hearing", "vision", "pediatrics"],
            1.0
        ),
        SearchDocument(
            21,
            "Pediatric Anemia Evaluation",
            "Anemia in children is most commonly due to iron deficiency. Screen with hemoglobin at 12 months. Evaluate dietary intake and consider supplementation if needed.",
            ["anemia", "screening", "iron", "pediatrics"],
            1.0
        ),
        SearchDocument(
            22,
            "Constipation in Children",
            "Constipation is common in children and is often functional. Encourage high-fiber diet, adequate fluids, and regular toilet habits. Laxatives may be used if lifestyle changes are insufficient.",
            ["constipation", "bowel", "children", "management"],
            1.0
        ),
        SearchDocument(
            23,
            "Pediatric Urinary Tract Infection",
            "UTIs present with fever, irritability, or vomiting in young children. Diagnosis is by urinalysis and culture. Treat promptly to prevent renal scarring.",
            ["UTI", "urinary", "infection", "pediatrics"],
            1.0
        ),
        SearchDocument(
            24,
            "Juvenile Idiopathic Arthritis Overview",
            "JIA is the most common chronic rheumatologic disease in children. Presents with joint swelling and stiffness. Early diagnosis and treatment improve outcomes.",
            ["arthritis", "JIA", "rheumatology", "children"],
            1.0
        ),
        SearchDocument(
            25,
            "Childhood Obesity Prevention",
            "Obesity prevention includes promoting physical activity, healthy diet, and limiting screen time. Early intervention is key to reducing long-term health risks.",
            ["obesity", "prevention", "nutrition", "children"],
            1.0
        ),
        SearchDocument(
            26,
            "Pediatric Allergic Rhinitis",
            "Allergic rhinitis presents with sneezing, rhinorrhea, and nasal congestion. Management includes allergen avoidance and antihistamines.",
            ["allergy", "rhinitis", "children", "management"],
            1.0
        ),
        SearchDocument(
            27,
            "Newborn Screening Overview",
            "Newborn screening detects metabolic and genetic disorders early. Common conditions screened include PKU, hypothyroidism, and sickle cell disease.",
            ["newborn", "screening", "genetic", "metabolic"],
            1.0
        ),
        SearchDocument(
            28,
            "Pediatric Asthma Action Plan",
            "An asthma action plan outlines daily management and how to handle worsening symptoms. Involve families in education and trigger avoidance.",
            ["asthma", "action plan", "management", "children"],
            1.0
        ),
        SearchDocument(
            29,
            "Pediatric Immunization Contraindications",
            "Contraindications to vaccines include severe allergic reaction to a previous dose or component. Mild illness is not a contraindication.",
            ["immunization", "contraindications", "vaccines", "children"],
            1.0
        ),
        SearchDocument(
            30,
            "Pediatric Head Injury Assessment",
            "Assess for red flags such as loss of consciousness, vomiting, or neurologic deficits. Use clinical decision rules to guide imaging.",
            ["head injury", "assessment", "trauma", "children"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)