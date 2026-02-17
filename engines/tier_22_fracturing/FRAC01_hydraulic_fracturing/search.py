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
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_tokens: Dict[int, List[str]] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_df: Dict[str, int] = defaultdict(int)
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + ' ' + doc.content + ' ' + ' '.join(doc.tags))
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            token_counts = Counter(tokens)
            for term, freq in token_counts.items():
                self.term_doc_freqs[term][doc.id] = freq
            for term in token_counts:
                self.term_df[term] += 1
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self._idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs = set()
        for term in query_terms:
            if term in self.term_doc_freqs:
                candidate_docs.update(self.term_doc_freqs[term].keys())
        scores = []
        for doc_id in candidate_docs:
            score = self._score_bm25(doc_id, query_terms)
            if score > 0:
                doc = self.documents[doc_id]
                snippet = self._make_snippet(doc, query_terms)
                scores.append(SearchResult(doc_id, score, doc.title, snippet))
        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:limit]

    def get_stats(self) -> Dict[str, float]:
        return {
            "num_documents": self.N,
            "avg_doc_length": self.avgdl,
            "num_terms": len(self.term_df)
        }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.term_df.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = Counter(tokens)
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
            bm25 = idf * freq * (self.k1 + 1) / denom
            score += bm25
        score *= doc.weight
        return score

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:window] + '...' if len(content) > window else content
        start = max(min(positions) - window // 2, 0)
        end = min(start + window, len(content))
        snippet = content[start:end]
        if start > 0:
            snippet = '...' + snippet
        if end < len(content):
            snippet = snippet + '...'
        return snippet

    def tfidf_score(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        tokens = self.doc_tokens[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = Counter(tokens)
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / doc_len
            df = self.term_df.get(term, 0)
            if df == 0:
                continue
            idf = math.log(self.N / df)
            score += tf_norm * idf
        score *= doc.weight
        return score

# Singleton factory
_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            idx = SearchIndex()
            _preseed_documents(idx)
            _search_index_instance = idx
        return _search_index_instance

def _preseed_documents(idx: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Net Pressure and Closure Stress Fundamentals",
            "Net pressure is the difference between the pressure inside the fracture and the minimum in-situ stress. Closure stress is critical for fracture containment and proppant selection.",
            ["net pressure", "closure stress", "frac design"],
            1.0
        ),
        SearchDocument(
            2,
            "PKN vs KGD Fracture Geometry Models",
            "The PKN model assumes fracture height is constant and width varies, suitable for long fractures. The KGD model assumes constant width and variable height, applicable for short, tall fractures.",
            ["PKN", "KGD", "fracture geometry", "model"],
            1.0
        ),
        SearchDocument(
            3,
            "Treatment Scheduling: Pad, Slurry, and Flush Stages",
            "A typical hydraulic fracturing treatment includes pad injection to initiate fracture, slurry stages for proppant placement, and flush to clear the wellbore.",
            ["treatment scheduling", "pad", "slurry", "flush"],
            1.0
        ),
        SearchDocument(
            4,
            "Pump Rate Optimization for Fracture Geometry",
            "Optimizing pump rate affects fracture width, length, and height. Higher rates can increase fracture complexity but may risk tip screenout.",
            ["pump rate", "optimization", "fracture geometry"],
            1.0
        ),
        SearchDocument(
            5,
            "Formation Stress Profiling: Mini-Frac and DFIT Analysis",
            "Mini-frac and Diagnostic Fracture Injection Tests (DFIT) help determine in-situ stress, closure pressure, and leak-off characteristics for accurate frac design.",
            ["formation stress", "mini-frac", "DFIT", "profiling"],
            1.0
        ),
        SearchDocument(
            6,
            "Fracture Height Containment and Stress Barriers",
            "Stress barriers such as shale layers can contain fracture height growth, preventing out-of-zone propagation and optimizing proppant placement.",
            ["fracture height", "containment", "stress barriers"],
            1.0
        ),
        SearchDocument(
            7,
            "Fracture Conductivity and Proppant Pack Permeability",
            "Fracture conductivity is determined by proppant type, size, and closure stress. High permeability proppant packs ensure effective hydrocarbon flow.",
            ["fracture conductivity", "proppant", "permeability"],
            1.0
        ),
        SearchDocument(
            8,
            "Tip Screenout (TSO) Design for Maximum Proppant Placement",
            "TSO occurs when proppant bridges at the fracture tip, halting growth. Proper design maximizes proppant placement and fracture conductivity.",
            ["tip screenout", "TSO", "proppant placement"],
            1.0
        ),
        SearchDocument(
            9,
            "Multi-Stage Completion: Plug-and-Perf vs Sliding Sleeve",
            "Plug-and-perf enables selective stage isolation, while sliding sleeves allow rapid stage access. Both methods impact stage count and frac efficiency.",
            ["multi-stage", "plug-and-perf", "sliding sleeve", "completion"],
            1.0
        ),
        SearchDocument(
            10,
            "Permian Basin Frac Designs: Wolfcamp, Bone Spring, Spraberry",
            "Frac designs in the Permian Basin vary by formation. Wolfcamp, Bone Spring, and Spraberry require tailored proppant, fluid, and stage strategies.",
            ["Permian Basin", "Wolfcamp", "Bone Spring", "Spraberry", "frac design"],
            1.0
        ),
        SearchDocument(
            11,
            "Delaware Basin vs Midland Basin Frac Design Differences",
            "Delaware Basin often uses higher fluid volumes and closer cluster spacing than Midland Basin, reflecting geological and operational differences.",
            ["Delaware Basin", "Midland Basin", "frac design"],
            1.0
        ),
        SearchDocument(
            12,
            "Frac Hit Mitigation and Parent-Child Well Interactions",
            "Frac hits occur when a new well communicates with an existing well. Mitigation strategies include sequencing, pressure management, and diverters.",
            ["frac hit", "parent-child", "well interaction", "mitigation"],
            1.0
        ),
        SearchDocument(
            13,
            "Stress Shadowing Effects on Multi-Stage Completions",
            "Stress shadowing from adjacent fractures can alter stress fields, impacting fracture propagation and cluster efficiency in multi-stage completions.",
            ["stress shadowing", "multi-stage", "completions"],
            1.0
        ),
        SearchDocument(
            14,
            "Limited Entry Perforating for Uniform Flow Distribution",
            "Limited entry perforating restricts flow through each cluster, promoting uniform proppant placement and maximizing stimulated reservoir volume.",
            ["limited entry", "perforating", "flow distribution"],
            1.0
        ),
        SearchDocument(
            15,
            "Chemical Diversion Agents for Improved Fracture Complexity",
            "Diversion agents temporarily block dominant flow paths, encouraging new fractures and increasing complexity for better reservoir stimulation.",
            ["chemical diversion", "fracture complexity", "stimulation"],
            1.0
        ),
        SearchDocument(
            16,
            "Real-Time Frac Monitoring and Treating Pressure Interpretation",
            "Real-time monitoring of treating pressure, rate, and proppant concentration enables on-the-fly adjustments for optimal fracture placement.",
            ["real-time", "frac monitoring", "treating pressure"],
            1.0
        ),
        SearchDocument(
            17,
            "Frac Gradient Calculations for Treatment Design",
            "Frac gradient is the pressure required to propagate a fracture per unit depth. Accurate calculation is vital for safe and effective treatment design.",
            ["frac gradient", "treatment design", "calculation"],
            1.0
        ),
        SearchDocument(
            18,
            "Proppant Selection: Sand vs Ceramic vs Resin-Coated",
            "Sand is cost-effective but less crush-resistant. Ceramics offer high strength at higher cost. Resin-coated proppants reduce flowback and embedment.",
            ["proppant selection", "sand", "ceramic", "resin-coated"],
            1.0
        ),
        SearchDocument(
            19,
            "Cluster Spacing Optimization for Stimulated Reservoir Volume",
            "Optimizing cluster spacing maximizes stimulated reservoir volume (SRV) and production. Too close causes interference; too far reduces coverage.",
            ["cluster spacing", "SRV", "optimization"],
            1.0
        ),
        SearchDocument(
            20,
            "Fracture Fluid Selection: Slickwater vs Crosslinked Gel vs Hybrid",
            "Slickwater provides high rate, low viscosity. Crosslinked gels carry more proppant. Hybrid designs combine both for optimal conductivity and cost.",
            ["fracture fluid", "slickwater", "crosslinked gel", "hybrid"],
            1.0
        ),
        SearchDocument(
            21,
            "Post-Frac Flowback and Cleanup Strategy",
            "Effective flowback removes excess fluid and proppant, restoring reservoir pressure and minimizing damage for optimal production.",
            ["post-frac", "flowback", "cleanup"],
            1.0
        ),
        SearchDocument(
            22,
            "DFIT Analysis: Pressure Decline and Leak-Off",
            "DFIT analysis interprets pressure decline to estimate leak-off coefficient, fracture closure, and reservoir permeability.",
            ["DFIT", "pressure decline", "leak-off"],
            1.0
        ),
        SearchDocument(
            23,
            "Fracture Height Growth Control",
            "Controlling fracture height involves adjusting pad volume, rate, and using stress barriers to prevent out-of-zone growth.",
            ["fracture height", "growth control", "stress barrier"],
            1.0
        ),
        SearchDocument(
            24,
            "Proppant Pack Damage and Permeability Loss",
            "Proppant pack damage from fines migration or embedment reduces permeability. Proper selection and placement mitigate these effects.",
            ["proppant pack", "damage", "permeability loss"],
            1.0
        ),
        SearchDocument(
            25,
            "Mini-Frac Test Interpretation",
            "Mini-frac tests provide closure pressure, leak-off, and net pressure data for calibration of frac models and treatment design.",
            ["mini-frac", "test", "interpretation"],
            1.0
        ),
        SearchDocument(
            26,
            "Hybrid Fracture Fluid Systems",
            "Hybrid systems use slickwater for pad and crosslinked gel for proppant stages, balancing cost and transport capacity.",
            ["hybrid", "fracture fluid", "system"],
            1.0
        ),
        SearchDocument(
            27,
            "Stage Count and Lateral Length Optimization",
            "Increasing stage count and lateral length can improve reservoir contact but may increase costs and operational complexity.",
            ["stage count", "lateral length", "optimization"],
            1.0
        ),
        SearchDocument(
            28,
            "Parent-Child Well Spacing Strategies",
            "Optimal spacing between parent and child wells reduces frac hit risk and maximizes resource recovery in multi-well pads.",
            ["parent-child", "well spacing", "frac hit"],
            1.0
        ),
        SearchDocument(
            29,
            "Resin-Coated Proppant Applications",
            "Resin-coated proppants reduce proppant flowback, fines generation, and embedment, improving long-term fracture conductivity.",
            ["resin-coated", "proppant", "application"],
            1.0
        ),
        SearchDocument(
            30,
            "Limited Entry Design in the Delaware Basin",
            "Delaware Basin completions often use limited entry to manage high pressure and ensure uniform cluster stimulation.",
            ["limited entry", "Delaware Basin", "cluster stimulation"],
            1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)