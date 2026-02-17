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
        self.term_freqs: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_docs: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = defaultdict(dict)

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.total_docs += 1
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_doc_freq[term] += 1
                self.term_freqs[doc.id][term] = freq
            self._idf_cache.clear()
            self._tfidf_cache.clear()
            self._recompute_avg_doc_length()

    def _recompute_avg_doc_length(self):
        if self.total_docs == 0:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        tf_norm = lambda tf: tf / doc_len if doc_len > 0 else 0
        for term in query_terms:
            tf = self.term_freqs[doc_id].get(term, 0)
            if tf == 0:
                continue
            idf = self._compute_idf(term)
            score += tf_norm(tf) * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = []
        for doc_id in self.documents.keys():
            if tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(self.documents[doc_id], query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda r: r.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str]) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + ('...' if len(content) > 160 else '')
        start = max(positions[0] - 10, 0)
        end = min(positions[0] + 30, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = ' '.join(snippet_tokens)
        for term in query_terms:
            snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet + ('...' if end < len(tokens) else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
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

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "PDC Bit Cutter Design Fundamentals",
            "Polycrystalline Diamond Compact (PDC) bits utilize synthetic diamond cutters arranged in a strategic pattern. Cutter geometry, size, and placement affect bit aggressiveness and durability. Key design parameters include cutter density, back rake angle, and exposure. Optimizing these factors enhances ROP and bit life.",
            ["PDC", "Cutter Design", "Fundamentals"],
            1.2
        ),
        SearchDocument(
            2,
            "IADC Bit Classification System",
            "The International Association of Drilling Contractors (IADC) bit classification system categorizes bits based on type, bearing, and cutting structure. The IADC code aids in bit selection and performance evaluation. Understanding the code is essential for matching bit to formation.",
            ["IADC", "Classification", "Bit Selection"],
            1.0
        ),
        SearchDocument(
            3,
            "Bit Hydraulics: TFA and Nozzle Selection",
            "Total Flow Area (TFA) and nozzle selection are critical for optimizing bit hydraulics. Proper TFA ensures efficient cuttings removal and cooling. Nozzle size and placement affect jet impact and pressure drop. Hydraulic optimization improves ROP and prevents bit balling.",
            ["Hydraulics", "TFA", "Nozzle"],
            1.1
        ),
        SearchDocument(
            4,
            "IADC Dull Bit Grading System",
            "The IADC dull grading system provides a standardized method to assess bit wear and failure modes. Grading includes cutting structure, bearing, and gauge. Accurate grading informs bit selection and maintenance strategies.",
            ["IADC", "Dull Grading", "Bit Wear"],
            1.0
        ),
        SearchDocument(
            5,
            "ROP Optimization via Specific Energy",
            "Specific energy analysis quantifies the energy required to remove a unit volume of rock. Lowering specific energy through bit design and operational parameters increases rate of penetration (ROP). Monitoring torque, weight on bit, and RPM allows real-time optimization.",
            ["ROP", "Specific Energy", "Optimization"],
            1.2
        ),
        SearchDocument(
            6,
            "PDC Bit Balling Prevention",
            "Bit balling occurs when sticky formations adhere to the bit, reducing cutting efficiency. Prevention strategies include optimized hydraulics, anti-balling cutter geometry, and proper mud properties. Real-time monitoring and adaptive drilling reduce balling risk.",
            ["PDC", "Balling", "Prevention"],
            1.1
        ),
        SearchDocument(
            7,
            "Roller Cone vs PDC Bit Selection",
            "Roller cone bits are suited for soft to medium formations and offer robust durability. PDC bits excel in hard, abrasive formations with higher ROP. Selection depends on formation characteristics, cost per foot, and operational constraints.",
            ["Roller Cone", "PDC", "Bit Selection"],
            1.0
        ),
        SearchDocument(
            8,
            "Bit Vibration: Whirl, Stick-Slip, and Bounce",
            "Bit vibration phenomena such as whirl, stick-slip, and bounce can damage cutters and reduce ROP. Mitigation includes stabilizer placement, bit design adjustments, and real-time vibration monitoring. Understanding vibration modes is key to bit longevity.",
            ["Vibration", "Whirl", "Stick-Slip", "Bounce"],
            1.1
        ),
        SearchDocument(
            9,
            "Diamond Impregnated Bits",
            "Diamond impregnated bits feature a matrix with embedded diamond particles. These bits are ideal for hard, abrasive formations where conventional cutters fail. Impregnated bits offer slow but steady penetration and superior durability.",
            ["Diamond", "Impregnated", "Bit Design"],
            1.0
        ),
        SearchDocument(
            10,
            "Cost Per Foot Analysis",
            "Cost per foot is a critical metric for bit selection. It considers bit price, run length, and ROP. Lower cost per foot indicates efficient drilling. Analysis tools help compare bit types and optimize drilling economics.",
            ["Cost", "Analysis", "Bit Selection"],
            1.2
        ),
        SearchDocument(
            11,
            "Hybrid Bit Technology",
            "Hybrid bits combine PDC and roller cone elements to maximize performance in variable formations. They offer improved durability and ROP in challenging drilling environments. Hybrid technology bridges the gap between conventional bit types.",
            ["Hybrid", "Bit Technology", "PDC", "Roller Cone"],
            1.1
        ),
        SearchDocument(
            12,
            "Bit Selection for Directional Drilling",
            "Directional drilling requires bits with enhanced steerability and durability. PDC bits with optimized cutter placement and gauge design are preferred. Bit selection impacts build rate, trajectory control, and overall drilling efficiency.",
            ["Directional Drilling", "Bit Selection", "PDC"],
            1.2
        ),
        SearchDocument(
            13,
            "Hole Opener and Under-Reamer Selection",
            "Hole openers and under-reamers enlarge boreholes for casing and completion. Selection criteria include formation hardness, tool compatibility, and hydraulic requirements. Proper selection ensures borehole quality and operational success.",
            ["Hole Opener", "Under-Reamer", "Selection"],
            1.0
        ),
        SearchDocument(
            14,
            "Formation-Specific Bit Selection: Shale",
            "Shale formations require bits with anti-balling features and optimized hydraulics. PDC bits with high cutter density and aggressive geometry perform well. Mud properties and real-time monitoring further enhance performance.",
            ["Shale", "Formation", "Bit Selection"],
            1.1
        ),
        SearchDocument(
            15,
            "Formation-Specific Bit Selection: Limestone and Dolomite",
            "Limestone and dolomite formations demand bits with durable cutters and robust gauge protection. PDC bits with moderate aggressiveness and optimized hydraulics are ideal. Roller cone bits may be used in softer zones.",
            ["Limestone", "Dolomite", "Bit Selection"],
            1.0
        ),
        SearchDocument(
            16,
            "Cutter Wear Patterns and Diagnosis",
            "Cutter wear patterns reveal operational and formation-related issues. Common patterns include chipping, flat wear, and thermal damage. Diagnosis guides bit selection and operational adjustments for improved performance.",
            ["Cutter Wear", "Diagnosis", "Bit Selection"],
            1.1
        ),
        SearchDocument(
            17,
            "Core Bit Selection and Design",
            "Core bits are designed for rock sampling during drilling. Selection depends on formation type, required core size, and bit material. Diamond impregnated and PDC core bits offer different advantages based on application.",
            ["Core Bit", "Design", "Selection"],
            1.0
        ),
        SearchDocument(
            18,
            "Baker Hughes vs Halliburton vs NOV Bit Comparison",
            "Major bit manufacturers like Baker Hughes, Halliburton, and NOV offer diverse bit technologies. Comparison focuses on cutter design, durability, and cost per foot. Selecting the right manufacturer depends on project requirements and performance history.",
            ["Baker Hughes", "Halliburton", "NOV", "Bit Comparison"],
            1.2
        ),
        SearchDocument(
            19,
            "PDC Cutter Back Rake Angle Optimization",
            "Back rake angle influences cutter aggressiveness and durability. Optimizing rake angle balances penetration rate and wear resistance. Advanced modeling and field testing guide optimal rake selection for specific formations.",
            ["PDC", "Cutter", "Back Rake", "Optimization"],
            1.1
        ),
        SearchDocument(
            20,
            "Bit Gauge Protection Strategies",
            "Gauge protection prevents bit diameter loss and maintains borehole quality. Strategies include hardfacing, gauge pad design, and material selection. Effective protection extends bit life and reduces drilling costs.",
            ["Gauge Protection", "Bit Design", "Material"],
            1.0
        ),
        SearchDocument(
            21,
            "PDC Bit Run Length Maximization",
            "Maximizing PDC bit run length reduces operational costs. Factors include cutter quality, hydraulic optimization, and real-time monitoring. Proper bit selection and maintenance extend run length and improve economics.",
            ["PDC", "Run Length", "Optimization"],
            1.1
        ),
        SearchDocument(
            22,
            "Bit Selection for High Abrasive Formations",
            "High abrasive formations require bits with enhanced wear resistance. Diamond impregnated and PDC bits with premium cutters are preferred. Hydraulic optimization and mud properties further improve performance.",
            ["Abrasive", "Bit Selection", "Diamond"],
            1.0
        ),
        SearchDocument(
            23,
            "PDC Bit Cutter Density Impact",
            "Cutter density affects bit aggressiveness and durability. High density increases ROP but may reduce bit life in abrasive formations. Balancing density with cutter quality and hydraulic design is essential.",
            ["PDC", "Cutter Density", "Bit Design"],
            1.1
        ),
        SearchDocument(
            24,
            "Roller Cone Bit Bearing Types",
            "Roller cone bits utilize different bearing types: sealed, open, and journal. Bearing selection impacts bit durability and performance. Proper lubrication and bearing material extend bit life.",
            ["Roller Cone", "Bearing", "Bit Selection"],
            1.0
        ),
        SearchDocument(
            25,
            "Bit Hydraulics: Jet Impact and Pressure Drop",
            "Jet impact and pressure drop are key hydraulic parameters. Optimizing nozzle placement and size improves cuttings removal and cooling. Hydraulic modeling guides bit design and operational settings.",
            ["Hydraulics", "Jet Impact", "Pressure Drop"],
            1.1
        ),
        SearchDocument(
            26,
            "PDC Bit Material Selection",
            "Material selection for PDC bits includes matrix and steel body options. Matrix bits offer abrasion resistance, while steel bits provide toughness. Selection depends on formation, operational parameters, and cost.",
            ["PDC", "Material", "Bit Selection"],
            1.0
        ),
        SearchDocument(
            27,
            "Bit Selection for Soft Formations",
            "Soft formations require bits with high aggressiveness and efficient cuttings removal. PDC bits with large cutters and optimized hydraulics perform well. Roller cone bits may be used for cost-effective drilling.",
            ["Soft Formation", "Bit Selection", "PDC"],
            1.0
        ),
        SearchDocument(
            28,
            "Bit Selection for Hard Formations",
            "Hard formations demand bits with durable cutters and robust design. Diamond impregnated bits and PDC bits with premium cutters are preferred. Hydraulic optimization and real-time monitoring enhance performance.",
            ["Hard Formation", "Bit Selection", "Diamond"],
            1.1
        ),
        SearchDocument(
            29,
            "Bit Selection for Unconventional Reservoirs",
            "Unconventional reservoirs require bits with adaptive design and enhanced durability. Hybrid bits and PDC bits with specialized cutters are used. Bit selection impacts drilling efficiency and reservoir access.",
            ["Unconventional", "Reservoir", "Bit Selection"],
            1.0
        ),
        SearchDocument(
            30,
            "Bit Selection for Extended Reach Drilling",
            "Extended reach drilling demands bits with high durability and steerability. PDC bits with optimized geometry and hybrid bits are preferred. Bit selection affects trajectory control and operational success.",
            ["Extended Reach", "Drilling", "Bit Selection"],
            1.1
        ),
    ]
    for doc in docs:
        index.add_document(doc)