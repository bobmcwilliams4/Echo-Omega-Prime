import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# --- Data Classes ---

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

# --- Search Index Implementation ---

class SearchIndex:
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freq: Dict[str, int] = defaultdict(int)
        self.term_doc_map: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.total_docs: int = 0
        self.bm25_k1 = bm25_k1
        self.bm25_b = bm25_b
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            for term in set(tokens):
                self.term_doc_freq[term] += 1
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_doc_map[term][doc.id] = freq
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

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

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            freq = self.term_doc_map.get(term, {}).get(doc_id, 0)
            if freq == 0:
                continue
            idf = self._compute_idf(term)
            numerator = freq * (self.bm25_k1 + 1)
            denominator = freq + self.bm25_k1 * (1 - self.bm25_b + self.bm25_b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vec = self._tfidf_cache[doc_id]
        else:
            doc = self.documents[doc_id]
            tokens = self._tokenize(doc.content)
            term_counts = Counter(tokens)
            tfidf_vec = {}
            for term in term_counts:
                tf = term_counts[term] / len(tokens)
                idf = self._compute_idf(term)
                tfidf_vec[term] = tf * idf
            self._tfidf_cache[doc_id] = tfidf_vec
        query_vec = {}
        for term in query_terms:
            idf = self._compute_idf(term)
            query_vec[term] = idf
        # Cosine similarity
        dot = sum(tfidf_vec.get(term, 0.0) * query_vec.get(term, 0.0) for term in query_terms)
        doc_norm = math.sqrt(sum(v ** 2 for v in tfidf_vec.values()))
        query_norm = math.sqrt(sum(v ** 2 for v in query_vec.values()))
        if doc_norm == 0 or query_norm == 0:
            return 0.0
        return (dot / (doc_norm * query_norm)) * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, method: str = 'bm25') -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = {}
        for doc_id in self.documents:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            elif method == 'tfidf':
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content: str, query_terms: List[str], max_length: int = 160) -> str:
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = ' '.join(tokens[:max_length])
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + max_length, len(tokens))
            snippet = ' '.join(tokens[start:end])
        return snippet[:max_length] + ('...' if len(snippet) > max_length else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

# --- Singleton Factory ---

_search_index_singleton: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_singleton
    with _search_index_lock:
        if _search_index_singleton is None:
            _search_index_singleton = SearchIndex()
            _preseed_documents(_search_index_singleton)
        return _search_index_singleton

# --- Preseed Domain Documents ---

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "ASA Physical Status Classification Overview",
            "The ASA Physical Status Classification System is a method for assessing the fitness of patients before surgery. It ranges from ASA I (healthy) to ASA VI (brain-dead).",
            ["ASA", "preoperative", "risk"],
            1.0
        ),
        SearchDocument(
            2,
            "ASA Classification: Clinical Examples",
            "ASA II includes patients with mild systemic disease, such as controlled hypertension or diabetes. ASA III includes severe systemic disease.",
            ["ASA", "examples", "systemic disease"],
            1.0
        ),
        SearchDocument(
            3,
            "Mallampati Airway Assessment",
            "Mallampati scoring evaluates airway visibility. Class I: full visibility of tonsils, uvula, and soft palate. Class IV: only hard palate visible.",
            ["airway", "Mallampati", "anesthesia"],
            1.0
        ),
        SearchDocument(
            4,
            "Mallampati Score and Difficult Intubation",
            "Higher Mallampati classes correlate with increased risk of difficult intubation. Combine with thyromental distance and neck mobility for comprehensive assessment.",
            ["airway", "intubation", "risk"],
            1.0
        ),
        SearchDocument(
            5,
            "WHO Surgical Safety Checklist",
            "The WHO Surgical Safety Checklist improves patient safety by ensuring critical steps are not missed. Includes sign-in, time-out, and sign-out phases.",
            ["safety", "WHO", "checklist"],
            1.0
        ),
        SearchDocument(
            6,
            "Implementing the WHO Checklist",
            "Successful implementation requires team training and leadership support. Checklist adherence reduces complications and mortality.",
            ["safety", "implementation", "outcomes"],
            1.0
        ),
        SearchDocument(
            7,
            "Laparoscopic vs Open Surgery: Criteria",
            "Laparoscopic surgery is preferred for reduced pain and faster recovery. Open surgery may be indicated for extensive disease or adhesions.",
            ["laparoscopic", "open", "criteria"],
            1.0
        ),
        SearchDocument(
            8,
            "Robotic-Assisted Surgery: da Vinci Platform",
            "The da Vinci robotic system offers enhanced dexterity and 3D visualization. Used in urology, gynecology, and general surgery.",
            ["robotic", "da Vinci", "technology"],
            1.0
        ),
        SearchDocument(
            9,
            "Robotic Surgery: Indications and Limitations",
            "Robotic-assisted surgery is ideal for complex procedures requiring precision. Limitations include cost and learning curve.",
            ["robotic", "indications", "limitations"],
            1.0
        ),
        SearchDocument(
            10,
            "Surgical Site Infection Prevention Bundle",
            "SSI prevention includes preoperative antibiotics, skin antisepsis, normothermia, and glycemic control. Bundle implementation reduces infection rates.",
            ["infection", "prevention", "bundle"],
            1.0
        ),
        SearchDocument(
            11,
            "Enhanced Recovery After Surgery (ERAS) Protocols",
            "ERAS protocols optimize perioperative care: minimal fasting, early mobilization, multimodal analgesia, and reduced drains.",
            ["ERAS", "recovery", "protocols"],
            1.0
        ),
        SearchDocument(
            12,
            "ERAS: Outcomes and Compliance",
            "High compliance with ERAS protocols leads to shorter hospital stays and fewer complications. Multidisciplinary team involvement is key.",
            ["ERAS", "outcomes", "compliance"],
            1.0
        ),
        SearchDocument(
            13,
            "Electrosurgery Safety: Monopolar vs Bipolar",
            "Monopolar electrosurgery uses a single electrode and return pad; bipolar uses two electrodes. Bipolar reduces risk of burns and stray currents.",
            ["electrosurgery", "monopolar", "bipolar"],
            1.0
        ),
        SearchDocument(
            14,
            "Electrosurgery: Precautions and Complications",
            "Proper grounding and pad placement are essential in monopolar electrosurgery. Complications include burns, electrical injuries, and interference.",
            ["electrosurgery", "safety", "complications"],
            1.0
        ),
        SearchDocument(
            15,
            "Blood Loss Estimation Techniques",
            "Blood loss can be estimated visually, by weighing sponges, or using gravimetric methods. Accurate estimation guides transfusion decisions.",
            ["blood loss", "estimation", "transfusion"],
            1.0
        ),
        SearchDocument(
            16,
            "Transfusion Thresholds in Surgery",
            "Transfusion is indicated when hemoglobin falls below 7-8 g/dL in stable patients. Consider comorbidities and ongoing bleeding.",
            ["transfusion", "thresholds", "hemoglobin"],
            1.0
        ),
        SearchDocument(
            17,
            "Sterilization Methods for Surgical Instruments",
            "Steam sterilization (autoclaving) is standard. Alternatives include ethylene oxide, hydrogen peroxide plasma, and dry heat.",
            ["sterilization", "instruments", "methods"],
            1.0
        ),
        SearchDocument(
            18,
            "Sterilization Quality Assurance",
            "Biological indicators and chemical strips verify sterilization. Regular maintenance and monitoring are essential.",
            ["sterilization", "quality", "assurance"],
            1.0
        ),
        SearchDocument(
            19,
            "Patient Positioning in Surgery",
            "Proper positioning prevents nerve injury and pressure ulcers. Common positions: supine, prone, lateral, lithotomy.",
            ["positioning", "pressure injury", "prevention"],
            1.0
        ),
        SearchDocument(
            20,
            "Pressure Injury Prevention Strategies",
            "Use padding, reposition regularly, and monitor high-risk areas. Early detection and intervention reduce complications.",
            ["pressure injury", "prevention", "strategies"],
            1.0
        ),
        SearchDocument(
            21,
            "ASA Classification: Pediatric Considerations",
            "Pediatric ASA classification considers age-specific risks. Neonates and infants may have unique comorbidities.",
            ["ASA", "pediatric", "risk"],
            1.0
        ),
        SearchDocument(
            22,
            "Mallampati Assessment in Pediatrics",
            "Mallampati scoring in children may be less predictive. Combine with other airway assessments for safety.",
            ["Mallampati", "pediatric", "airway"],
            1.0
        ),
        SearchDocument(
            23,
            "WHO Checklist: Team Communication",
            "Effective communication during checklist use improves outcomes. Encourage speaking up and clarifying roles.",
            ["WHO", "communication", "teamwork"],
            1.0
        ),
        SearchDocument(
            24,
            "Laparoscopic Surgery: Contraindications",
            "Contraindications include severe cardiopulmonary disease, extensive adhesions, and inability to tolerate pneumoperitoneum.",
            ["laparoscopic", "contraindications", "criteria"],
            1.0
        ),
        SearchDocument(
            25,
            "Robotic Surgery: Training and Credentialing",
            "Surgeons require specialized training for robotic platforms. Credentialing ensures safety and competence.",
            ["robotic", "training", "credentialing"],
            1.0
        ),
        SearchDocument(
            26,
            "SSI Bundle: Antibiotic Timing",
            "Administer antibiotics within 60 minutes before incision. Redosing may be needed for prolonged procedures.",
            ["SSI", "antibiotics", "timing"],
            1.0
        ),
        SearchDocument(
            27,
            "ERAS: Nutrition and Fasting",
            "Early oral intake and minimal fasting are key ERAS principles. Avoid prolonged NPO status.",
            ["ERAS", "nutrition", "fasting"],
            1.0
        ),
        SearchDocument(
            28,
            "Electrosurgery: Pediatric Safety",
            "Pediatric electrosurgery requires lower energy settings and careful pad placement. Monitor for burns and arrhythmias.",
            ["electrosurgery", "pediatric", "safety"],
            1.0
        ),
        SearchDocument(
            29,
            "Blood Loss in Pediatric Surgery",
            "Children have lower blood volume; estimate loss carefully. Use age-appropriate transfusion thresholds.",
            ["blood loss", "pediatric", "transfusion"],
            1.0
        ),
        SearchDocument(
            30,
            "Sterilization: Low-Temperature Methods",
            "Low-temperature sterilization is used for heat-sensitive instruments. Methods include hydrogen peroxide plasma and ozone.",
            ["sterilization", "low-temperature", "instruments"],
            1.0
        ),
        SearchDocument(
            31,
            "Patient Positioning: Lithotomy Risks",
            "Lithotomy position increases risk of nerve injury and compartment syndrome. Monitor limb perfusion and duration.",
            ["positioning", "lithotomy", "risks"],
            1.0
        ),
        SearchDocument(
            32,
            "Pressure Injury: Risk Assessment Tools",
            "Use tools like the Braden Scale to assess risk. Document findings and implement preventive measures.",
            ["pressure injury", "assessment", "tools"],
            1.0
        ),
        SearchDocument(
            33,
            "ASA Classification: Emergency Surgery",
            "Emergency cases are designated 'E' (e.g., ASA II E). Risk assessment may be limited by time constraints.",
            ["ASA", "emergency", "risk"],
            1.0
        ),
        SearchDocument(
            34,
            "Mallampati: Combined Airway Assessment",
            "Combine Mallampati with Cormack-Lehane and thyromental distance for comprehensive airway evaluation.",
            ["Mallampati", "airway", "assessment"],
            1.0
        ),
        SearchDocument(
            35,
            "WHO Checklist: Infection Control",
            "Checklist includes infection control steps: hand hygiene, sterile technique, and antibiotic prophylaxis.",
            ["WHO", "infection control", "checklist"],
            1.0
        ),
        SearchDocument(
            36,
            "Laparoscopic Surgery: Postoperative Recovery",
            "Patients undergoing laparoscopy typically experience less pain and faster recovery compared to open surgery.",
            ["laparoscopic", "recovery", "postoperative"],
            1.0
        ),
        SearchDocument(
            37,
            "Robotic Surgery: Cost Analysis",
            "Robotic platforms incur higher costs but may reduce complications and length of stay in selected cases.",
            ["robotic", "cost", "analysis"],
            1.0
        ),
        SearchDocument(
            38,
            "SSI Bundle: Skin Preparation",
            "Use chlorhexidine or iodine-based solutions for skin antisepsis. Allow adequate drying before incision.",
            ["SSI", "skin preparation", "antisepsis"],
            1.0
        ),
        SearchDocument(
            39,
            "ERAS: Multimodal Analgesia",
            "Combine opioids, NSAIDs, and regional anesthesia for pain control. Reduces opioid consumption and side effects.",
            ["ERAS", "analgesia", "pain control"],
            1.0
        ),
        SearchDocument(
            40,
            "Electrosurgery: Smoke Evacuation",
            "Use smoke evacuation systems to reduce exposure to surgical plume, which contains hazardous chemicals.",
            ["electrosurgery", "smoke evacuation", "safety"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)