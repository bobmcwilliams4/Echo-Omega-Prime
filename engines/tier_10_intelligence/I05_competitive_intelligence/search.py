import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Tuple

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

# --- SearchIndex Implementation ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_doc_freqs: Dict[str, Dict[str, int]] = defaultdict(dict)  # term -> doc_id -> freq
        self.term_df: Dict[str, int] = defaultdict(int)  # term -> doc freq
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[Tuple[str, str], float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return  # skip duplicates
            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            length = len(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = length
            term_counts = Counter(tokens)
            for term, freq in term_counts.items():
                self.term_doc_freqs[term][doc.id] = freq
            for term in term_counts:
                self.term_df[term] += 1
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / max(1, self.N)
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_doc_ids = set()
        for term in query_terms:
            candidate_doc_ids.update(self.term_doc_freqs.get(term, {}).keys())
        scored_docs = []
        for doc_id in candidate_doc_ids:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc = self.documents[doc_id]
            # Weighted sum: BM25 (0.7), TF-IDF (0.3), times doc.weight
            score = (0.7 * bm25_score + 0.3 * tfidf_score) * doc.weight
            snippet = self._make_snippet(doc, query_terms)
            scored_docs.append(SearchResult(doc_id, score, doc.title, snippet))
        scored_docs.sort(key=lambda r: r.score, reverse=True)
        return scored_docs[:limit]

    def get_stats(self):
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avgdl,
                "vocab_size": len(self.term_df)
            }

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_df.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: str, query_terms: List[str]) -> float:
        k1 = 1.5
        b = 0.75
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        doc_tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
        tf = Counter(doc_tokens)
        for term in query_terms:
            if doc_id not in self.term_doc_freqs.get(term, {}):
                continue
            f = tf[term]
            idf = self._compute_idf(term)
            denom = f + k1 * (1 - b + b * doc_len / self.avgdl)
            score += idf * (f * (k1 + 1)) / (denom + 1e-9)
        return score

    def _score_tfidf(self, doc_id: str, query_terms: List[str]) -> float:
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        doc_tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
        tf = Counter(doc_tokens)
        max_tf = max(tf.values()) if tf else 1
        for term in query_terms:
            key = (doc_id, term)
            if key in self._tfidf_cache:
                score += self._tfidf_cache[key]
                continue
            if doc_id not in self.term_doc_freqs.get(term, {}):
                continue
            tf_norm = tf[term] / max_tf
            idf = self._compute_idf(term)
            tfidf = tf_norm * idf
            self._tfidf_cache[key] = tfidf
            score += tfidf
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return content[:160] + "..." if len(content) > 160 else content
        start = max(positions[0] - snippet_len // 2, 0)
        end = min(start + snippet_len, len(tokens))
        snippet_tokens = tokens[start:end]
        snippet = " ".join(snippet_tokens)
        return snippet + "..."

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
            "1",
            "Competitor Landman Activity Surges in Reeves County",
            "Recent months have seen a marked increase in landman filings and lease negotiations by multiple competitors in Reeves County, with notable activity from Alpha Energy and Delta Resources.",
            ["landman", "activity", "Reeves County", "competitor"],
            1.2
        ),
        SearchDocument(
            "2",
            "Lease Acquisition Velocity: Q2 2024 Benchmarking",
            "Beta Oil has accelerated its lease acquisition rate by 35% quarter-over-quarter, outpacing regional rivals. Analysis of county records reveals a focus on contiguous acreage blocks.",
            ["lease", "acquisition", "velocity", "benchmarking"],
            1.1
        ),
        SearchDocument(
            "3",
            "Permit-to-Completion Ratio Trends: Delaware Basin",
            "The permit-to-completion ratio for the Delaware Basin has tightened, with Gamma Petroleum completing 82% of permitted wells within 9 months, indicating operational efficiency.",
            ["permit", "completion", "Delaware Basin", "ratios"],
            1.0
        ),
        SearchDocument(
            "4",
            "Acreage Position Mapping: Competitor Holdings Visualization",
            "Updated GIS mapping of competitor acreage positions shows Epsilon Drilling consolidating a 14,000-acre position near the Loving-Winkler line, suggesting future pad development.",
            ["acreage", "mapping", "GIS", "competitor"],
            1.1
        ),
        SearchDocument(
            "5",
            "Broker Activity Monitoring: Title Transfers Q1-Q2",
            "Title company search logs and broker filings indicate a spike in assignments and transfers, with Zeta Land Services brokering 47 deals in the first half of 2024.",
            ["broker", "activity", "title", "transfers"],
            1.0
        ),
        SearchDocument(
            "6",
            "Title Company Search Patterns Reveal Hotspots",
            "Analysis of title search frequency highlights increased due diligence in Ward and Pecos counties, with Omega Title focusing on large tract parcels.",
            ["title", "search", "patterns", "hotspots"],
            1.0
        ),
        SearchDocument(
            "7",
            "Drilling Program Inference from Permit Clustering",
            "Clustering of recent drilling permits by Sigma Exploration suggests a phased development program targeting Wolfcamp A and B benches.",
            ["drilling", "program", "inference", "permits"],
            1.2
        ),
        SearchDocument(
            "8",
            "Completion Design Trends: Frac Stage Density",
            "Competitor completions show a shift toward higher stage density and increased proppant loading, with Lambda Oil adopting 50+ stages per lateral.",
            ["completion", "design", "trends", "frac"],
            1.1
        ),
        SearchDocument(
            "9",
            "Well Spacing Optimization Signals Detected",
            "Recent well spacing adjustments by Theta Energy, now at 660 feet between laterals, indicate ongoing optimization to balance recovery and interference.",
            ["well", "spacing", "optimization", "signals"],
            1.0
        ),
        SearchDocument(
            "10",
            "Competitor Cost Structure Estimation: 2024 Models",
            "Cost benchmarking suggests Mu Resources has reduced drilling and completion costs by 12% via pad drilling and supply chain renegotiations.",
            ["cost", "structure", "estimation", "benchmarking"],
            1.0
        ),
        SearchDocument(
            "11",
            "Market Share Analysis by County: Midland Basin",
            "Nu Oil & Gas increased its market share in Martin and Howard counties, now controlling 18% of active rigs, according to state production data.",
            ["market", "share", "analysis", "county"],
            1.1
        ),
        SearchDocument(
            "12",
            "Competitive Moat Assessment: Infrastructure Advantage",
            "Omicron Energy's dedicated water pipeline system provides a logistical moat, reducing completion delays and lowering LOE relative to peers.",
            ["competitive", "moat", "infrastructure", "assessment"],
            1.2
        ),
        SearchDocument(
            "13",
            "First-Mover Advantage Analysis: Early Permitting",
            "Pi Drilling's early entry into the Central Basin Platform allowed rapid lease capture and favorable JV terms, establishing a first-mover advantage.",
            ["first-mover", "advantage", "permitting", "JV"],
            1.1
        ),
        SearchDocument(
            "14",
            "Partnership JV Pattern Detection: Recent Deals",
            "Recent JV announcements between Rho Oil and Sigma Exploration indicate a trend toward risk-sharing and capital efficiency in large-scale projects.",
            ["partnership", "JV", "pattern", "detection"],
            1.0
        ),
        SearchDocument(
            "15",
            "Talent Movement Tracking: Key Landman Hires",
            "Tracking LinkedIn and state filings reveals that several senior landmen have moved from Tau Energy to Upsilon Resources since January.",
            ["talent", "movement", "tracking", "landman"],
            1.0
        ),
        SearchDocument(
            "16",
            "Competitor Technology Adoption: Digital Land Systems",
            "Phi Petroleum has implemented a new digital land management platform, accelerating lease analysis and improving data integrity.",
            ["technology", "adoption", "digital", "land"],
            1.1
        ),
        SearchDocument(
            "17",
            "Press Release Analysis: Strategic Announcements",
            "Recent press releases by Chi Oil highlight expansion plans into the Central Basin Platform and a new focus on carbon capture partnerships.",
            ["press", "release", "analysis", "strategic"],
            1.0
        ),
        SearchDocument(
            "18",
            "Earnings Call Intelligence: Capex Guidance",
            "Earnings call transcripts from Psi Energy reveal a 20% increase in 2024 capex, with emphasis on horizontal development in the Delaware Basin.",
            ["earnings", "call", "intelligence", "capex"],
            1.1
        ),
        SearchDocument(
            "19",
            "Competitor Strategic Intent Classification",
            "Text classification of competitor statements suggests a pivot toward liquids-rich targets and increased M&A activity in the Midland Basin.",
            ["strategic", "intent", "classification", "competitor"],
            1.0
        ),
        SearchDocument(
            "20",
            "Landman Activity Patterns: Weekly Heatmap",
            "Weekly heatmap visualizations show peak landman activity on Tuesdays and Thursdays, correlating with county courthouse schedules.",
            ["landman", "activity", "patterns", "heatmap"],
            1.0
        ),
        SearchDocument(
            "21",
            "Lease Expiration Risk: Competitor Exposure",
            "Analysis of lease expiration schedules indicates that Omega Oil faces significant exposure in Glasscock County over the next 12 months.",
            ["lease", "expiration", "risk", "competitor"],
            1.0
        ),
        SearchDocument(
            "22",
            "Drilling Permit Filing Velocity: 2024 Update",
            "Kappa Drilling has filed 62 drilling permits in Q2, leading the region and signaling aggressive development plans.",
            ["drilling", "permit", "velocity", "update"],
            1.0
        ),
        SearchDocument(
            "23",
            "Title Company Search Patterns: Competitive Insights",
            "Title search data from 2024 shows increased activity by Delta Title in Howard County, likely tied to new lease rounds.",
            ["title", "company", "search", "patterns"],
            1.0
        ),
        SearchDocument(
            "24",
            "JV Partnership Structures: Recent Trends",
            "Analysis of JV partnership filings reveals a shift toward carried interest structures and multi-operator pads.",
            ["JV", "partnership", "structures", "trends"],
            1.0
        ),
        SearchDocument(
            "25",
            "Completion Design Trends: Proppant Intensity",
            "Competitors are increasing proppant intensity per foot, with Zeta Oil now averaging 2,500 lbs/ft in the Wolfcamp formation.",
            ["completion", "design", "trends", "proppant"],
            1.0
        ),
        SearchDocument(
            "26",
            "Well Spacing Optimization: Simulation Results",
            "Simulation results from Upsilon Resources indicate optimal well spacing at 700 feet for maximizing EUR and minimizing parent-child interference.",
            ["well", "spacing", "optimization", "simulation"],
            1.0
        ),
        SearchDocument(
            "27",
            "Broker Activity: Emerging Players",
            "Emerging brokers such as Sigma Land Group are increasing their market share in lease assignments, especially in the Delaware Basin.",
            ["broker", "activity", "emerging", "players"],
            1.0
        ),
        SearchDocument(
            "28",
            "Market Share Analysis: Competitive Shifts",
            "Competitive shifts in market share are evident as Epsilon Drilling acquires new acreage positions in Reeves and Ward counties.",
            ["market", "share", "analysis", "competitive"],
            1.0
        ),
        SearchDocument(
            "29",
            "Technology Adoption: Automated Title Search",
            "Lambda Oil's adoption of automated title search tools has reduced due diligence time by 40%, improving lease acquisition velocity.",
            ["technology", "adoption", "automated", "title"],
            1.0
        ),
        SearchDocument(
            "30",
            "Strategic Intent: M&A Focus",
            "Recent statements by Alpha Energy executives point to a strategic focus on mergers and acquisitions in the Permian Basin.",
            ["strategic", "intent", "M&A", "focus"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)