import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Optional

# ----------------------------
# Data Classes
# ----------------------------

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

# ----------------------------
# SearchIndex Class
# ----------------------------

class SearchIndex:
    def __init__(self, bm25_k1: float = 1.5, bm25_b: float = 0.75):
        self._bm25_k1 = bm25_k1
        self._bm25_b = bm25_b
        self._documents: Dict[int, SearchDocument] = {}
        self._inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self._doc_freq: Dict[str, int] = defaultdict(int)
        self._term_freqs: Dict[int, Counter] = {}
        self._doc_lengths: Dict[int, int] = {}
        self._avg_doc_length: float = 0.0
        self._idf_cache: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._next_id = 1

    def add_document(self, title: str, content: str, tags: List[str], weight: float = 1.0) -> int:
        with self._lock:
            doc_id = self._next_id
            self._next_id += 1
        doc = SearchDocument(doc_id, title, content, tags, weight)
        tokens = self._tokenize(content)
        tf = Counter(tokens)
        self._documents[doc_id] = doc
        self._term_freqs[doc_id] = tf
        self._doc_lengths[doc_id] = len(tokens)
        for term in tf:
            self._inverted_index[term].add(doc_id)
            self._doc_freq[term] += 1
        self._avg_doc_length = sum(self._doc_lengths.values()) / max(len(self._doc_lengths), 1)
        self._idf_cache.clear()
        return doc_id

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            candidate_docs.update(self._inverted_index.get(term, set()))
        scored = []
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            final_score = bm25_score + 0.4 * tfidf_score
            doc = self._documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            scored.append(SearchResult(doc_id, final_score, doc.title, snippet))
        scored.sort(key=lambda r: r.score, reverse=True)
        return scored[:limit]

    def get_stats(self) -> Dict[str, int]:
        return {
            'document_count': len(self._documents),
            'unique_terms': len(self._doc_freq),
            'avg_doc_length': int(self._avg_doc_length),
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        N = len(self._documents)
        df = self._doc_freq.get(term, 0)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self._documents[doc_id]
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        avg_dl = self._avg_doc_length
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self._bm25_k1 * (1 - self._bm25_b + self._bm25_b * doc_len / avg_dl)
            numer = freq * (self._bm25_k1 + 1)
            score += idf * numer / denom
        return score * doc.weight

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = self._term_freqs[doc_id]
        doc_len = self._doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score

    def _make_snippet(self, content: str, query_terms: List[str], length: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:length] + ('...' if len(content) > length else '')
        start = max(min(positions) - 30, 0)
        end = start + length
        snippet = content[start:end]
        if start > 0:
            snippet = '...' + snippet
        if end < len(content):
            snippet = snippet + '...'
        return snippet

# ----------------------------
# Singleton Factory
# ----------------------------

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    if _search_index_instance is None:
        with _search_index_lock:
            if _search_index_instance is None:
                idx = SearchIndex()
                _seed_documents(idx)
                _search_index_instance = idx
    return _search_index_instance

# ----------------------------
# Pre-seeded Documents
# ----------------------------

def _seed_documents(idx: SearchIndex):
    docs = [
        {
            "title": "Stages of General Anesthesia",
            "content": (
                "General anesthesia is divided into four stages: "
                "Stage I (analgesia), Stage II (excitement), Stage III (surgical anesthesia), and Stage IV (overdose). "
                "Recognition of these stages is critical for safe anesthetic management."
            ),
            "tags": ["general anesthesia", "stages", "anesthetic depth"],
        },
        {
            "title": "Minimum Alveolar Concentration (MAC)",
            "content": (
                "MAC is the alveolar concentration of an inhaled anesthetic at which 50% of patients do not move in response to surgical stimulus. "
                "MAC values are additive and influenced by age, temperature, and concurrent medications."
            ),
            "tags": ["MAC", "inhaled anesthetics", "pharmacology"],
        },
        {
            "title": "Propofol Total Intravenous Anesthesia (TIVA)",
            "content": (
                "Propofol is commonly used for TIVA due to its rapid onset and recovery profile. "
                "TIVA avoids inhaled agents and is preferred in patients at risk for malignant hyperthermia or PONV."
            ),
            "tags": ["propofol", "TIVA", "intravenous anesthesia"],
        },
        {
            "title": "Succinylcholine vs Rocuronium for Rapid Sequence Induction",
            "content": (
                "Succinylcholine provides the fastest onset and shortest duration for rapid sequence induction, but is contraindicated in certain conditions. "
                "Rocuronium is an alternative, especially when sugammadex is available for reversal."
            ),
            "tags": ["succinylcholine", "rocuronium", "RSI", "neuromuscular blockade"],
        },
        {
            "title": "Sugammadex Reversal of Neuromuscular Blockade",
            "content": (
                "Sugammadex rapidly reverses aminosteroid neuromuscular blockers such as rocuronium and vecuronium. "
                "It encapsulates the drug molecule, allowing for prompt recovery of muscle function."
            ),
            "tags": ["sugammadex", "reversal", "neuromuscular blockade"],
        },
        {
            "title": "Difficult Airway Prediction and Management",
            "content": (
                "Predictors of a difficult airway include limited mouth opening, Mallampati score III/IV, reduced neck mobility, and history of difficult intubation. "
                "Preparation includes having alternative airway devices and a clear plan for failed airway."
            ),
            "tags": ["difficult airway", "airway management", "intubation"],
        },
        {
            "title": "Supraglottic Airway Devices (LMA)",
            "content": (
                "Laryngeal Mask Airways (LMAs) are supraglottic devices used for airway management. "
                "They are easy to insert and useful in both elective and rescue situations."
            ),
            "tags": ["LMA", "supraglottic airway", "airway devices"],
        },
        {
            "title": "Invasive Arterial Blood Pressure Monitoring",
            "content": (
                "Arterial lines provide beat-to-beat blood pressure monitoring and allow for frequent blood sampling. "
                "Common sites include the radial, femoral, and dorsalis pedis arteries."
            ),
            "tags": ["arterial line", "blood pressure", "monitoring"],
        },
        {
            "title": "Central Venous Pressure Monitoring",
            "content": (
                "Central venous pressure (CVP) monitoring assesses right heart preload. "
                "It is influenced by volume status, venous tone, and right ventricular function."
            ),
            "tags": ["CVP", "central venous", "monitoring"],
        },
        {
            "title": "ASA Physical Status Classification",
            "content": (
                "The ASA Physical Status Classification system stratifies patients based on preoperative health. "
                "Classes range from ASA I (healthy) to ASA VI (brain-dead organ donor)."
            ),
            "tags": ["ASA", "physical status", "preoperative"],
        },
        {
            "title": "NPO Guidelines and Aspiration Risk",
            "content": (
                "NPO guidelines recommend fasting from clear liquids for 2 hours, breast milk for 4 hours, and solids for 6-8 hours before anesthesia. "
                "Adherence reduces the risk of perioperative aspiration."
            ),
            "tags": ["NPO", "aspiration", "preoperative fasting"],
        },
        {
            "title": "Malignant Hyperthermia Crisis Management",
            "content": (
                "Malignant hyperthermia is a life-threatening reaction to certain anesthetics. "
                "Immediate treatment includes discontinuing triggering agents, administering dantrolene, and supportive care."
            ),
            "tags": ["malignant hyperthermia", "crisis", "dantrolene"],
        },
        {
            "title": "Postoperative Nausea and Vomiting (PONV) Prophylaxis",
            "content": (
                "PONV risk factors include female gender, non-smoker status, history of PONV, and opioid use. "
                "Prophylaxis includes multimodal antiemetic therapy and minimizing emetogenic agents."
            ),
            "tags": ["PONV", "nausea", "vomiting", "prophylaxis"],
        },
        {
            "title": "Spinal Anesthesia Technique and Complications",
            "content": (
                "Spinal anesthesia involves injecting local anesthetic into the subarachnoid space. "
                "Complications include hypotension, post-dural puncture headache, and high spinal block."
            ),
            "tags": ["spinal anesthesia", "technique", "complications"],
        },
        {
            "title": "Epidural Anesthesia and Labor Analgesia",
            "content": (
                "Epidural anesthesia is commonly used for labor analgesia. "
                "It provides excellent pain relief with minimal motor block when low concentrations of local anesthetics are used."
            ),
            "tags": ["epidural", "labor analgesia", "regional anesthesia"],
        },
        {
            "title": "Ultrasound-Guided Regional Anesthesia and Nerve Blocks",
            "content": (
                "Ultrasound guidance improves the safety and efficacy of regional anesthesia. "
                "Common nerve blocks include brachial plexus, femoral, and sciatic blocks."
            ),
            "tags": ["ultrasound", "regional anesthesia", "nerve block"],
        },
        {
            "title": "Preoperative Assessment in Anesthesiology",
            "content": (
                "A thorough preoperative assessment includes evaluation of airway, cardiac and pulmonary status, medications, and allergies. "
                "Identifying comorbidities allows for risk stratification and optimization."
            ),
            "tags": ["preoperative", "assessment", "risk"],
        },
        {
            "title": "Anesthetic Considerations in Obesity",
            "content": (
                "Obesity increases the risk of difficult airway, hypoventilation, and perioperative complications. "
                "Drug dosing may require adjustment based on ideal or lean body weight."
            ),
            "tags": ["obesity", "anesthesia", "airway"],
        },
        {
            "title": "Airway Management Algorithms",
            "content": (
                "Standardized airway algorithms guide clinicians through steps for anticipated and unanticipated difficult airways. "
                "They emphasize early recognition and use of alternative devices."
            ),
            "tags": ["airway", "algorithm", "management"],
        },
        {
            "title": "Rapid Sequence Induction Protocol",
            "content": (
                "Rapid sequence induction involves preoxygenation, administration of induction and paralytic agents, and cricoid pressure. "
                "It is indicated in patients at high risk for aspiration."
            ),
            "tags": ["RSI", "induction", "aspiration"],
        },
        {
            "title": "Monitoring Depth of Anesthesia",
            "content": (
                "Depth of anesthesia can be monitored clinically and with devices such as BIS. "
                "Avoiding awareness under anesthesia is a primary goal."
            ),
            "tags": ["depth", "anesthesia", "monitoring"],
        },
        {
            "title": "Local Anesthetic Systemic Toxicity (LAST)",
            "content": (
                "LAST is a rare but serious complication of regional anesthesia. "
                "Symptoms include CNS and cardiovascular toxicity. "
                "Treatment involves lipid emulsion therapy and supportive care."
            ),
            "tags": ["LAST", "local anesthetic", "toxicity"],
        },
        {
            "title": "Pediatric Anesthesia Considerations",
            "content": (
                "Children have unique anesthetic requirements, including higher MAC, rapid desaturation, and differences in airway anatomy. "
                "Careful dosing and monitoring are essential."
            ),
            "tags": ["pediatric", "anesthesia", "children"],
        },
        {
            "title": "Anesthesia for Ambulatory Surgery",
            "content": (
                "Ambulatory anesthesia emphasizes rapid recovery, minimal side effects, and early discharge. "
                "Short-acting agents and multimodal analgesia are preferred."
            ),
            "tags": ["ambulatory", "outpatient", "anesthesia"],
        },
        {
            "title": "Peripheral Nerve Block Complications",
            "content": (
                "Complications of peripheral nerve blocks include nerve injury, hematoma, infection, and local anesthetic toxicity. "
                "Ultrasound guidance reduces but does not eliminate risks."
            ),
            "tags": ["peripheral nerve block", "complications", "regional anesthesia"],
        },
        {
            "title": "Anesthesia Machine Safety Checks",
            "content": (
                "Pre-use anesthesia machine checks include verifying gas supplies, ventilator function, and leak testing. "
                "Proper checks prevent intraoperative equipment failures."
            ),
            "tags": ["anesthesia machine", "safety", "equipment"],
        },
        {
            "title": "Perioperative Fluid Management",
            "content": (
                "Fluid management aims to maintain euvolemia and organ perfusion. "
                "Crystalloids are commonly used, with colloids reserved for specific indications."
            ),
            "tags": ["fluid management", "perioperative", "crystalloids"],
        },
        {
            "title": "Awareness Under Anesthesia",
            "content": (
                "Awareness during anesthesia is rare but can have serious psychological consequences. "
                "Risk factors include light anesthesia, TIVA, and certain surgeries."
            ),
            "tags": ["awareness", "anesthesia", "risk"],
        },
        {
            "title": "Neuraxial Anesthesia Contraindications",
            "content": (
                "Absolute contraindications to neuraxial anesthesia include patient refusal, infection at the site, and coagulopathy. "
                "Relative contraindications include sepsis and fixed cardiac output states."
            ),
            "tags": ["neuraxial", "anesthesia", "contraindications"],
        },
        {
            "title": "Difficult IV Access in Anesthesia",
            "content": (
                "Difficult intravenous access can be managed with ultrasound guidance, external jugular cannulation, or intraosseous access. "
                "Preparation is key in patients with poor vascular access."
            ),
            "tags": ["IV access", "difficult", "ultrasound"],
        },
        {
            "title": "Prevention of Perioperative Hypothermia",
            "content": (
                "Perioperative hypothermia increases the risk of surgical site infection and coagulopathy. "
                "Active warming and temperature monitoring are recommended."
            ),
            "tags": ["hypothermia", "perioperative", "warming"],
        },
        {
            "title": "Anesthetic Management in Renal Failure",
            "content": (
                "Renal failure affects drug metabolism and fluid balance. "
                "Avoid nephrotoxic agents and adjust dosing as necessary."
            ),
            "tags": ["renal failure", "anesthesia", "management"],
        },
        {
            "title": "Antibiotic Prophylaxis in Anesthesia",
            "content": (
                "Antibiotics are administered within 60 minutes before incision to reduce surgical site infections. "
                "Choice depends on procedure and patient allergies."
            ),
            "tags": ["antibiotic", "prophylaxis", "surgery"],
        },
        {
            "title": "Anesthesia for Emergency Surgery",
            "content": (
                "Emergency surgery requires rapid assessment and optimization. "
                "Consider aspiration risk, full stomach, and hemodynamic instability."
            ),
            "tags": ["emergency", "surgery", "anesthesia"],
        },
        {
            "title": "Prevention of Peripheral Nerve Injury",
            "content": (
                "Proper positioning and padding reduce the risk of perioperative peripheral nerve injury. "
                "Monitor for signs of compression or stretch."
            ),
            "tags": ["nerve injury", "positioning", "prevention"],
        },
        {
            "title": "Anesthetic Implications of Liver Disease",
            "content": (
                "Liver disease alters drug metabolism, coagulation, and fluid status. "
                "Use short-acting agents and monitor for bleeding."
            ),
            "tags": ["liver disease", "anesthesia", "implications"],
        },
    ]
    for doc in docs:
        idx.add_document(doc["title"], doc["content"], doc["tags"])