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
        tokens = re.findall(r'\b[a-zA-Z0-9\-]+\b', text.lower())
        return tokens

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            for term in tf:
                self.term_doc_freq[term] += 1
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        doc = self.documents[doc_id]
        tf = self.term_freqs[doc_id]
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length if self.avg_doc_length else 1.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / avg_dl)
            score += idf * numerator / denominator
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        doc_len = self.doc_lengths[doc_id]
        score = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if freq == 0:
                continue
            tf_norm = freq / doc_len if doc_len else 0.0
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * self.documents[doc_id].weight

    def search(self, query: str, limit: int = 10, use_tfidf: bool = False) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores = []
        for doc_id in self.documents:
            if use_tfidf:
                score = self._score_tfidf(query_terms, doc_id)
            else:
                score = self._score_bm25(query_terms, doc_id)
            if score > 0:
                snippet = self._make_snippet(doc_id, query_terms)
                scores.append(SearchResult(doc_id, score, self.documents[doc_id].title, snippet))
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def _make_snippet(self, doc_id: int, query_terms: List[str], length: int = 160) -> str:
        doc = self.documents[doc_id]
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:length]
        else:
            start = max(positions[0] - 10, 0)
            end = min(start + 30, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
            for term in query_terms:
                snippet = re.sub(r'\b({})\b'.format(re.escape(term)), r'**\1**', snippet, flags=re.IGNORECASE)
        return snippet[:length] + ('...' if len(snippet) > length else '')

    def get_stats(self) -> Dict[str, float]:
        return {
            'total_docs': self.total_docs,
            'avg_doc_length': self.avg_doc_length,
            'unique_terms': len(self.term_doc_freq),
        }

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Deep Penetrating Charge Design",
            "Deep penetrating charges are engineered to maximize perforation tunnel length, improving connectivity with the reservoir. These charges are ideal for tight formations where deep penetration is critical for effective stimulation.",
            ["charge design", "deep penetration", "tight formations"],
            1.2
        ),
        SearchDocument(
            2,
            "Big Hole Charge Design",
            "Big hole charges create larger entry holes in casing, facilitating higher flow rates and reducing formation damage. Used in unconsolidated formations and for sand control applications.",
            ["charge design", "big hole", "sand control"],
            1.1
        ),
        SearchDocument(
            3,
            "Shot Density and Phasing in Horizontal Wells",
            "Optimizing shot density and phasing is essential for uniform fracture initiation and maximizing reservoir contact in horizontal wells. Typical phasing angles are 60, 90, and 120 degrees.",
            ["shot density", "phasing", "horizontal wells"],
            1.0
        ),
        SearchDocument(
            4,
            "Limited Entry Perforation Friction Diversion",
            "Limited entry perforating uses friction to divert fluid into multiple clusters, enhancing stimulation efficiency. Proper calculation of friction pressure is key to successful diversion.",
            ["limited entry", "friction diversion", "cluster efficiency"],
            1.3
        ),
        SearchDocument(
            5,
            "Underbalanced vs Overbalanced Perforating",
            "Underbalanced perforating minimizes formation damage and aids in debris removal, while overbalanced perforating can reduce risk of uncontrolled flow but may cause more damage.",
            ["underbalanced", "overbalanced", "perforating"],
            1.0
        ),
        SearchDocument(
            6,
            "API RP 19B Perforating Performance Testing",
            "API RP 19B provides standardized methods for evaluating perforating performance, including penetration depth, hole size, and debris generation. Compliance ensures reliable data for charge selection.",
            ["API RP 19B", "performance testing", "charge selection"],
            1.2
        ),
        SearchDocument(
            7,
            "Tubing-Conveyed Perforating (TCP) vs Wireline Operations",
            "TCP allows perforating in challenging well conditions and high pressure environments, while wireline is preferred for rapid deployment and flexibility in completion operations.",
            ["TCP", "wireline", "completion"],
            1.1
        ),
        SearchDocument(
            8,
            "Perforation Friction Pressure Calculation",
            "Friction pressure across perforations is calculated using entry hole size, shot density, and flow rate. Accurate calculation is vital for limited entry and fracture diversion strategies.",
            ["friction pressure", "calculation", "limited entry"],
            1.3
        ),
        SearchDocument(
            9,
            "Gun Debris Management and Wellbore Cleanout",
            "Effective debris management post-perforating prevents wellbore obstruction and ensures optimal flow. Cleanout techniques include circulation, coiled tubing, and chemical washes.",
            ["debris management", "cleanout", "wellbore"],
            1.0
        ),
        SearchDocument(
            10,
            "Oriented Perforating for Fracture Initiation",
            "Oriented perforating aligns perforation tunnels with the preferred fracture direction, increasing fracture efficiency and reservoir contact. Tools include gyro and magnetic orientation systems.",
            ["oriented perforating", "fracture initiation", "orientation"],
            1.2
        ),
        SearchDocument(
            11,
            "Extreme Overbalanced Perforating (EOP)",
            "EOP uses high overbalance pressures to minimize formation damage and control wellbore fluids during perforating. It is applied in sensitive formations and HPHT wells.",
            ["EOP", "overbalanced", "HPHT"],
            1.1
        ),
        SearchDocument(
            12,
            "Cluster Efficiency in Plug-and-Perf Completions",
            "Cluster efficiency measures the effectiveness of fluid distribution among perforation clusters. High efficiency is achieved through proper shot density, phasing, and limited entry techniques.",
            ["cluster efficiency", "plug-and-perf", "fluid distribution"],
            1.3
        ),
        SearchDocument(
            13,
            "Perforation Design for Hydraulic Fracturing",
            "Perforation design impacts fracture initiation, propagation, and overall stimulation success. Key parameters include charge type, shot density, phasing, and entry hole size.",
            ["perforation design", "hydraulic fracturing", "stimulation"],
            1.2
        ),
        SearchDocument(
            14,
            "Casing Gun vs Through-Tubing Gun Selection",
            "Casing guns offer larger charges and deeper penetration, while through-tubing guns provide flexibility for re-entry and remedial operations. Selection depends on well geometry and objectives.",
            ["casing gun", "through-tubing", "gun selection"],
            1.1
        ),
        SearchDocument(
            15,
            "Perforation Erosion During Hydraulic Fracturing",
            "Perforation erosion occurs when high-rate fracturing fluids enlarge entry holes, affecting cluster efficiency and stimulation outcomes. Monitoring and modeling are essential for mitigation.",
            ["perforation erosion", "hydraulic fracturing", "mitigation"],
            1.0
        ),
        SearchDocument(
            16,
            "Perforating in HPHT Environments",
            "HPHT wells require specialized perforating systems and charges to withstand extreme temperatures and pressures. Materials selection and operational procedures are critical for safety.",
            ["HPHT", "perforating", "materials"],
            1.2
        ),
        SearchDocument(
            17,
            "Propellant-Assisted Perforating Systems",
            "Propellant-assisted systems use energetic materials to enhance perforation tunnel cleaning and reduce debris. They are effective in low-pressure and damage-prone formations.",
            ["propellant", "perforating", "debris reduction"],
            1.1
        ),
        SearchDocument(
            18,
            "Abrasive Jetting as Perforating Alternative",
            "Abrasive jetting creates perforations using high-pressure fluid and abrasive particles, suitable for challenging environments where conventional charges are ineffective.",
            ["abrasive jetting", "perforating", "alternative"],
            1.0
        ),
        SearchDocument(
            19,
            "Gun Loading and Safety Procedures",
            "Safe gun loading requires strict adherence to procedures, including charge handling, electrical isolation, and personnel protection. Training and compliance are essential for incident prevention.",
            ["gun loading", "safety", "procedures"],
            1.3
        ),
        SearchDocument(
            20,
            "Perforation Tunnel Geometry and Reservoir Connectivity",
            "Tunnel geometry influences reservoir connectivity and stimulation effectiveness. Deep, clean tunnels maximize flow and reduce skin effects.",
            ["tunnel geometry", "reservoir connectivity", "stimulation"],
            1.2
        ),
        SearchDocument(
            21,
            "Perforation Damage Mechanisms",
            "Damage mechanisms include crushed zone formation, debris blockage, and thermal effects. Mitigation strategies involve charge selection and underbalanced perforating.",
            ["damage mechanisms", "mitigation", "charge selection"],
            1.1
        ),
        SearchDocument(
            22,
            "Perforation Debris Removal Techniques",
            "Debris removal is achieved through circulation, reverse flow, and mechanical intervention. Proper planning ensures clean tunnels and optimal production.",
            ["debris removal", "clean tunnels", "production"],
            1.0
        ),
        SearchDocument(
            23,
            "Perforation Phasing Tools and Techniques",
            "Phasing tools enable precise alignment of perforations for optimal fracture initiation. Techniques include mechanical indexing and electronic orientation.",
            ["phasing tools", "alignment", "fracture initiation"],
            1.2
        ),
        SearchDocument(
            24,
            "Perforating in Unconsolidated Formations",
            "Unconsolidated formations require big hole charges and sand control screens to prevent collapse and maintain productivity.",
            ["unconsolidated", "big hole", "sand control"],
            1.1
        ),
        SearchDocument(
            25,
            "Wireline Perforating Best Practices",
            "Wireline perforating offers rapid deployment and flexibility. Best practices include proper tool selection, depth control, and post-perforation evaluation.",
            ["wireline", "best practices", "depth control"],
            1.0
        ),
        SearchDocument(
            26,
            "Perforation Entry Hole Measurement",
            "Entry hole measurement is performed using caliper tools and image logs. Accurate data is critical for evaluating charge performance and cluster efficiency.",
            ["entry hole", "measurement", "charge performance"],
            1.2
        ),
        SearchDocument(
            27,
            "Perforation Modeling and Simulation",
            "Modeling and simulation predict perforation tunnel behavior, erosion, and cluster efficiency. Software tools aid in optimizing design and operational parameters.",
            ["modeling", "simulation", "optimization"],
            1.3
        ),
        SearchDocument(
            28,
            "Perforation Charge Selection Criteria",
            "Charge selection is based on formation properties, desired tunnel geometry, and operational constraints. API RP 19B data guides selection for optimal results.",
            ["charge selection", "criteria", "API RP 19B"],
            1.2
        ),
        SearchDocument(
            29,
            "Perforation Fluid Loss Control",
            "Fluid loss control during perforating is managed with specialized fluids and mechanical barriers. Proper control prevents formation damage and enhances stimulation.",
            ["fluid loss", "control", "stimulation"],
            1.1
        ),
        SearchDocument(
            30,
            "Perforation Completion Integration",
            "Perforation design must integrate with completion hardware and stimulation plans for maximum production. Coordination ensures seamless operations and reservoir access.",
            ["completion", "integration", "production"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)