import math
import re
import threading
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional


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


class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, SearchDocument] = {}
        self.doc_term_freqs: Dict[str, Counter] = {}
        self.term_doc_freqs: Dict[str, int] = defaultdict(int)
        self.avg_doc_len: float = 0.0
        self.total_doc_len: int = 0
        self.N: int = 0
        self.lock = threading.Lock()
        self.idf_cache: Dict[str, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                # Remove old doc term frequencies from index
                old_tf = self.doc_term_freqs.get(doc.id, Counter())
                for term in old_tf:
                    self.term_doc_freqs[term] -= 1
                    if self.term_doc_freqs[term] <= 0:
                        del self.term_doc_freqs[term]
                self.total_doc_len -= sum(old_tf.values())
                self.N -= 1
                del self.doc_term_freqs[doc.id]

            tokens = self._tokenize(doc.title + " " + doc.content + " " + " ".join(doc.tags))
            tf = Counter(tokens)
            self.doc_term_freqs[doc.id] = tf
            for term in tf.keys():
                self.term_doc_freqs[term] += 1

            doc_len = sum(tf.values())
            self.total_doc_len += doc_len
            self.N += 1
            self.avg_doc_len = self.total_doc_len / self.N if self.N > 0 else 0.0

            self.documents[doc.id] = doc
            self.idf_cache.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        # Compute IDF for query terms
        idf = {term: self._compute_idf(term) for term in query_terms}

        scores: Dict[str, float] = defaultdict(float)
        for term in query_terms:
            if term not in self.term_doc_freqs:
                continue
            for doc_id, tf in self.doc_term_freqs.items():
                freq = tf.get(term, 0)
                if freq == 0:
                    continue
                score = self._score_bm25(freq, idf[term], sum(tf.values()))
                scores[doc_id] += score

        # Apply document weight multiplier
        for doc_id in scores:
            scores[doc_id] *= self.documents[doc_id].weight

        # Sort results by score descending
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id=doc_id, score=score, title=doc.title, snippet=snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "total_documents": self.N,
                "average_document_length": self.avg_doc_len,
                "unique_terms": len(self.term_doc_freqs),
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _compute_idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        n_q = self.term_doc_freqs.get(term, 0)
        if n_q == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - n_q + 0.5) / (n_q + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, freq: int, idf: float, doc_len: int) -> float:
        denom = freq + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len if self.avg_doc_len > 0 else 1))
        score = idf * (freq * (self.k1 + 1)) / denom if denom > 0 else 0.0
        return score

    def _make_snippet(self, content: str, query_terms: List[str], snippet_len: int = 160) -> str:
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            for match in re.finditer(r'\b' + re.escape(term) + r'\b', content_lower):
                positions.append(match.start())
        if not positions:
            snippet = content[:snippet_len].strip()
            if len(content) > snippet_len:
                snippet += "..."
            return snippet

        positions.sort()
        start_pos = max(positions[0] - snippet_len // 4, 0)
        end_pos = start_pos + snippet_len
        if end_pos > len(content):
            end_pos = len(content)
            start_pos = max(end_pos - snippet_len, 0)
        snippet = content[start_pos:end_pos].strip()
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet = snippet + "..."
        return snippet


_singleton_instance: Optional[SearchIndex] = None
_singleton_lock = threading.Lock()


def get_search_index() -> SearchIndex:
    global _singleton_instance
    with _singleton_lock:
        if _singleton_instance is None:
            _singleton_instance = SearchIndex()
            _seed_documents(_singleton_instance)
    return _singleton_instance


def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            doc_id="doc001",
            title="Water-Based Mud (WBM) Formulation Design",
            content=(
                "Water-Based Mud (WBM) formulation involves selecting appropriate base fluids, "
                "clays, weighting agents, and additives to achieve desired rheological properties, "
                "fluid loss control, and shale inhibition."
            ),
            tags=["WBM", "formulation", "rheology", "fluid loss", "shale inhibition"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc002",
            title="Oil-Based Mud (OBM) and Synthetic-Based Mud (SBM) Systems",
            content=(
                "OBM and SBM systems provide enhanced lubricity and shale inhibition in challenging formations. "
                "Synthetic-based muds offer environmental advantages with lower toxicity and improved biodegradability."
            ),
            tags=["OBM", "SBM", "lubricity", "shale inhibition", "environmental"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc003",
            title="Mud Weight Control and Barite Addition Calculations",
            content=(
                "Accurate mud weight control is critical for wellbore stability. Barite is commonly added as a weighting agent. "
                "Calculations ensure proper barite concentration to achieve target mud density."
            ),
            tags=["mud weight", "barite", "weighting agent", "calculations"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc004",
            title="Mud Rheology: Plastic Viscosity, Yield Point, and Gel Strength",
            content=(
                "Mud rheology parameters such as plastic viscosity, yield point, and gel strength determine the fluid's carrying capacity "
                "and flow behavior under static and dynamic conditions."
            ),
            tags=["rheology", "plastic viscosity", "yield point", "gel strength"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc005",
            title="Fluid Loss Control: API Filtrate and HPHT Filtration",
            content=(
                "Controlling fluid loss is essential to prevent formation damage. API filtrate tests and HPHT filtration tests "
                "evaluate the mud's fluid loss characteristics under various conditions."
            ),
            tags=["fluid loss", "API filtrate", "HPHT filtration", "formation damage"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc006",
            title="Shale Inhibition via Potassium Chloride (KCl) Muds",
            content=(
                "Potassium chloride (KCl) is widely used in water-based muds to inhibit shale swelling and dispersion, "
                "improving wellbore stability in reactive formations."
            ),
            tags=["shale inhibition", "KCl", "water-based mud", "wellbore stability"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc007",
            title="Lost Circulation Materials: Bridging and Sealing Formulations",
            content=(
                "Lost circulation materials (LCMs) are designed to bridge and seal fractures or vugs in the formation, "
                "preventing mud loss and maintaining well control."
            ),
            tags=["lost circulation", "LCM", "bridging", "sealing"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc008",
            title="Solids Control Equipment: Shale Shakers, Centrifuges, and Degassers",
            content=(
                "Solids control equipment such as shale shakers, centrifuges, and degassers remove drilled solids and gas from the mud, "
                "maintaining mud properties and preventing operational issues."
            ),
            tags=["solids control", "shale shaker", "centrifuge", "degasser"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc009",
            title="Cement Contamination: Diagnosis and Treatment",
            content=(
                "Cement contamination in drilling fluids can cause rheological and filtration problems. "
                "Diagnosis involves testing mud properties and treatment includes dilution or reconditioning."
            ),
            tags=["cement contamination", "diagnosis", "treatment", "mud properties"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc010",
            title="High-Pressure High-Temperature (HPHT) Drilling Fluid Systems",
            content=(
                "HPHT drilling fluid systems are engineered to withstand extreme temperature and pressure conditions, "
                "maintaining stability and performance in challenging wells."
            ),
            tags=["HPHT", "drilling fluid", "high pressure", "high temperature"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc011",
            title="Completion and Workover Fluids: Clear Brines and Low-Solids Systems",
            content=(
                "Completion and workover fluids often use clear brines or low-solids formulations to minimize formation damage "
                "and facilitate well interventions."
            ),
            tags=["completion fluids", "workover fluids", "clear brines", "low solids"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc012",
            title="Environmental Regulations for Drilling Fluid Disposal and Discharge",
            content=(
                "Compliance with environmental regulations is critical for drilling fluid disposal and discharge, "
                "requiring proper treatment and monitoring to minimize ecological impact."
            ),
            tags=["environmental regulations", "disposal", "discharge", "treatment"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc013",
            title="pH and Alkalinity Management in Water-Based Muds",
            content=(
                "Maintaining proper pH and alkalinity in water-based muds ensures chemical stability and optimal performance "
                "of additives and shale inhibitors."
            ),
            tags=["pH", "alkalinity", "water-based mud", "chemical stability"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc014",
            title="Wellbore Stability Analysis and Mud Weight Windows",
            content=(
                "Wellbore stability analysis determines the safe mud weight window to prevent collapse or fracturing, "
                "ensuring safe drilling operations."
            ),
            tags=["wellbore stability", "mud weight window", "analysis", "drilling safety"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc015",
            title="Glycol and Amine Shale Inhibitors for Extreme Reactive Formations",
            content=(
                "Glycol and amine-based shale inhibitors provide effective stabilization in highly reactive formations "
                "where conventional inhibitors may fail."
            ),
            tags=["glycol", "amine", "shale inhibitors", "reactive formations"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc016",
            title="Barite Sag Prevention in Deviated Wells",
            content=(
                "Barite sag can cause density variation and well control issues in deviated wells. "
                "Formulation and operational practices help prevent sagging."
            ),
            tags=["barite sag", "deviated wells", "mud density", "well control"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc017",
            title="Emulsion Stability in Oil-Based Muds",
            content=(
                "Stable emulsions in oil-based muds are essential for maintaining rheology and inhibitive properties "
                "during drilling operations."
            ),
            tags=["emulsion stability", "oil-based mud", "rheology", "inhibition"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc018",
            title="Salt Contamination Diagnosis and Treatment",
            content=(
                "Salt contamination affects mud properties and can cause flocculation or viscosity changes. "
                "Diagnosis and treatment restore mud performance."
            ),
            tags=["salt contamination", "diagnosis", "treatment", "mud properties"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc019",
            title="Anhydrite (CaSO4) Contamination Treatment",
            content=(
                "Anhydrite contamination in drilling fluids requires specific treatment to prevent rheological issues "
                "and formation damage."
            ),
            tags=["anhydrite", "CaSO4", "contamination", "treatment"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc020",
            title="Drilling Fluid Hydraulics and Equivalent Circulating Density (ECD)",
            content=(
                "Understanding drilling fluid hydraulics and managing equivalent circulating density (ECD) "
                "are vital for pressure control and wellbore integrity."
            ),
            tags=["hydraulics", "ECD", "pressure control", "wellbore integrity"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc021",
            title="Synthetic-Based Mud (SBM) Systems and Environmental Advantages",
            content=(
                "SBM systems combine performance benefits of OBM with improved environmental profiles, "
                "offering reduced toxicity and better biodegradability."
            ),
            tags=["SBM", "synthetic mud", "environmental", "biodegradability"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc022",
            title="Managed Pressure Drilling (MPD) Fluid Systems",
            content=(
                "MPD fluid systems enable precise control of annular pressure, improving safety and efficiency "
                "in challenging drilling environments."
            ),
            tags=["MPD", "managed pressure drilling", "fluid systems", "pressure control"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc023",
            title="Underbalanced Drilling (UBD) Fluids: Gas, Foam, and Aerated Muds",
            content=(
                "UBD fluids such as gas, foam, and aerated muds reduce formation damage and improve rate of penetration "
                "in sensitive reservoirs."
            ),
            tags=["UBD", "underbalanced drilling", "gas mud", "foam", "aerated mud"],
            weight=1.2,
        ),
        SearchDocument(
            doc_id="doc024",
            title="API RP 13B-1 Testing Procedures: Standardization and QA/QC",
            content=(
                "API RP 13B-1 provides standardized testing procedures for drilling fluids, ensuring quality assurance "
                "and quality control in mud properties."
            ),
            tags=["API RP 13B-1", "testing", "QA/QC", "standardization"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc025",
            title="Formate Brines: Potassium and Cesium Formate for Ultra-HPHT",
            content=(
                "Formate brines such as potassium and cesium formate are used in ultra-HPHT drilling fluids "
                "for their high density and environmental compatibility."
            ),
            tags=["formate brines", "potassium formate", "cesium formate", "ultra-HPHT"],
            weight=1.3,
        ),
        SearchDocument(
            doc_id="doc026",
            title="Barite Addition Best Practices and Safety Considerations",
            content=(
                "Proper handling and addition of barite are essential to maintain mud weight and ensure safety "
                "during drilling operations."
            ),
            tags=["barite", "mud weight", "safety", "best practices"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc027",
            title="Rheology Modifiers and Their Impact on Drilling Fluid Performance",
            content=(
                "Rheology modifiers adjust viscosity and gel strength, optimizing drilling fluid performance "
                "under various downhole conditions."
            ),
            tags=["rheology modifiers", "viscosity", "gel strength", "drilling fluid"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc028",
            title="Mud Gas Separator Operation and Maintenance",
            content=(
                "Mud gas separators remove entrained gas from drilling fluids, preventing kick hazards "
                "and ensuring safe rig operations."
            ),
            tags=["mud gas separator", "gas removal", "safety", "maintenance"],
            weight=1.0,
        ),
        SearchDocument(
            doc_id="doc029",
            title="Chemical Compatibility of Drilling Fluid Additives",
            content=(
                "Understanding chemical compatibility among drilling fluid additives prevents adverse reactions "
                "and maintains fluid stability."
            ),
            tags=["chemical compatibility", "additives", "fluid stability"],
            weight=1.1,
        ),
        SearchDocument(
            doc_id="doc030",
            title="Drilling Fluid Sampling and Laboratory Analysis Techniques",
            content=(
                "Proper sampling and laboratory analysis of drilling fluids are critical for monitoring mud properties "
                "and making informed adjustments."
            ),
            tags=["sampling", "laboratory analysis", "mud properties", "monitoring"],
            weight=1.2,
        ),
    ]

    for doc in docs:
        index.add_document(doc)