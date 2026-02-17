import math
import threading
import heapq
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

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

# --- Search Index ---

class SearchIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, Set[int]] = defaultdict(set)
        self.term_freqs: Dict[int, Counter] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.N = 0
        self.avgdl = 0.0
        self.lock = threading.RLock()
        self._idf_cache: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        # Simple tokenizer: lowercase, split on non-word
        return [t for t in re.findall(r'\b\w+\b', text.lower()) if t]

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title) + self._tokenize(doc.content)
            tf = Counter(tokens)
            self.term_freqs[doc.id] = tf
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            for term in tf:
                self.doc_freqs[term] += 1
                self.inverted_index[term].add(doc.id)
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self._idf_cache.clear()

    def _compute_idf(self, term: str) -> float:
        # Cached IDF calculation
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        score = 0.0
        doc = self.documents[doc_id]
        for term in query_terms:
            if term not in tf:
                continue
            idf = self._compute_idf(term)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            score += idf * freq * (self.k1 + 1) / denom
        return score * doc.weight

    def _score_tfidf(self, query_terms: List[str], doc_id: int) -> float:
        tf = self.term_freqs[doc_id]
        dl = self.doc_lengths[doc_id]
        doc = self.documents[doc_id]
        score = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            tf_norm = tf[term] / dl
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query: str, limit: int = 10, use_bm25: bool = True) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        candidates: Set[int] = set()
        for term in query_terms:
            candidates |= self.inverted_index.get(term, set())
        scored: List[Tuple[float, int]] = []
        for doc_id in candidates:
            score = self._score_bm25(query_terms, doc_id) if use_bm25 else self._score_tfidf(query_terms, doc_id)
            if score > 0:
                scored.append((score, doc_id))
        top = heapq.nlargest(limit, scored)
        results = []
        for score, doc_id in top:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], maxlen: int = 180) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:maxlen]
        else:
            pos = positions[0]
            start = max(0, pos - 8)
            end = min(len(tokens), pos + 12)
            snippet = ' '.join(tokens[start:end])
        return snippet[:maxlen] + ('...' if len(snippet) > maxlen else '')

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                'documents': self.N,
                'avgdl': self.avgdl,
                'unique_terms': len(self.doc_freqs)
            }

# --- Singleton Factory ---

_search_index_instance: Optional[SearchIndex] = None
_search_index_lock = threading.Lock()

def get_search_index() -> SearchIndex:
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-Seeding Domain Documents ---

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Drug Absorption Mechanisms",
            "Drug absorption involves passive diffusion, facilitated diffusion, active transport, and endocytosis. Factors affecting absorption include drug solubility, ionization, and gastrointestinal motility.",
            ["absorption", "pharmacokinetics", "mechanisms"],
            1.0
        ),
        SearchDocument(
            2,
            "Volume of Distribution and Tissue Binding",
            "Volume of distribution (Vd) quantifies drug dispersion in body compartments. High tissue binding increases Vd, while plasma protein binding restricts distribution.",
            ["distribution", "tissue binding", "pharmacokinetics"],
            1.0
        ),
        SearchDocument(
            3,
            "Hepatic Drug Metabolism and CYP450 System",
            "The liver metabolizes drugs via phase I (oxidation, reduction, hydrolysis) and phase II (conjugation) reactions. The CYP450 enzyme family is central to phase I metabolism and drug-drug interactions.",
            ["hepatic metabolism", "CYP450", "enzymes"],
            1.0
        ),
        SearchDocument(
            4,
            "Renal and Biliary Elimination",
            "Drugs are eliminated by glomerular filtration, tubular secretion, and reabsorption in the kidney, or via bile into the feces. Impaired renal or hepatic function alters elimination rates.",
            ["elimination", "renal", "biliary"],
            1.0
        ),
        SearchDocument(
            5,
            "Dose-Response Relationships and Therapeutic Window",
            "Dose-response curves illustrate efficacy and potency. The therapeutic window is the concentration range where a drug is effective without unacceptable toxicity.",
            ["dose-response", "therapeutic window"],
            1.0
        ),
        SearchDocument(
            6,
            "Receptor Theory and Drug-Receptor Interactions",
            "Drugs bind to receptors with varying affinity and intrinsic activity. Agonists, antagonists, partial agonists, and inverse agonists modulate physiological responses.",
            ["receptor theory", "interactions", "pharmacodynamics"],
            1.0
        ),
        SearchDocument(
            7,
            "CYP450-Mediated Drug-Drug Interactions",
            "CYP450 inducers increase, and inhibitors decrease, the metabolism of substrate drugs, leading to altered plasma concentrations and potential toxicity or therapeutic failure.",
            ["CYP450", "drug interactions"],
            1.0
        ),
        SearchDocument(
            8,
            "P-glycoprotein Drug Interactions",
            "P-glycoprotein (P-gp) is an efflux transporter affecting drug absorption and elimination. Inhibitors and inducers of P-gp can alter drug bioavailability and tissue distribution.",
            ["P-glycoprotein", "transporters", "interactions"],
            1.0
        ),
        SearchDocument(
            9,
            "Cholinergic Agonists and Parasympathomimetics",
            "Cholinergic agonists mimic acetylcholine, stimulating muscarinic and nicotinic receptors. Used in glaucoma, myasthenia gravis, and to reverse anticholinergic toxicity.",
            ["cholinergic", "parasympathomimetics", "agonists"],
            1.0
        ),
        SearchDocument(
            10,
            "Anticholinergic Agents and Muscarinic Antagonists",
            "Anticholinergic drugs block muscarinic receptors, reducing secretions, relaxing smooth muscle, and treating bradycardia, motion sickness, and Parkinsonism.",
            ["anticholinergic", "muscarinic antagonists"],
            1.0
        ),
        SearchDocument(
            11,
            "Adrenergic Agonists and Sympathomimetics",
            "Adrenergic agonists activate alpha and beta receptors, increasing heart rate, bronchodilation, and vasoconstriction. Used in shock, asthma, and cardiac arrest.",
            ["adrenergic", "sympathomimetics", "agonists"],
            1.0
        ),
        SearchDocument(
            12,
            "β-Adrenergic Antagonists (Beta-Blockers)",
            "Beta-blockers inhibit beta-adrenergic receptors, reducing heart rate and blood pressure. Indicated for hypertension, arrhythmias, angina, and heart failure.",
            ["beta-blockers", "adrenergic antagonists"],
            1.0
        ),
        SearchDocument(
            13,
            "Antihypertensive Agents",
            "Antihypertensives include ACE inhibitors, ARBs, beta-blockers, calcium channel blockers, and diuretics. Selection depends on comorbidities and side effect profiles.",
            ["antihypertensive", "hypertension", "agents"],
            1.0
        ),
        SearchDocument(
            14,
            "Anticoagulants and Thrombolytics",
            "Anticoagulants inhibit clotting factors, while thrombolytics dissolve formed clots. Used in atrial fibrillation, DVT, PE, and acute MI.",
            ["anticoagulants", "thrombolytics", "clotting"],
            1.0
        ),
        SearchDocument(
            15,
            "Antiplatelet Agents",
            "Antiplatelet drugs inhibit platelet aggregation, preventing arterial thrombosis. Aspirin, clopidogrel, and GP IIb/IIIa inhibitors are common examples.",
            ["antiplatelet", "platelet aggregation"],
            1.0
        ),
        SearchDocument(
            16,
            "HMG-CoA Reductase Inhibitors (Statins)",
            "Statins lower cholesterol by inhibiting HMG-CoA reductase, reducing cardiovascular risk. Monitor for myopathy and liver enzyme elevations.",
            ["statins", "HMG-CoA", "lipids"],
            1.0
        ),
        SearchDocument(
            17,
            "Opioid Analgesics",
            "Opioids bind mu, kappa, and delta receptors to relieve pain. Risks include respiratory depression, constipation, tolerance, and dependence.",
            ["opioid", "analgesics", "pain"],
            1.0
        ),
        SearchDocument(
            18,
            "Benzodiazepines and GABA-A Agonists",
            "Benzodiazepines enhance GABA-A receptor activity, producing anxiolytic, sedative, muscle relaxant, and anticonvulsant effects.",
            ["benzodiazepines", "GABA-A", "sedatives"],
            1.0
        ),
        SearchDocument(
            19,
            "Antidepressant Agents",
            "Antidepressants include SSRIs, SNRIs, TCAs, and MAOIs. Selection is based on efficacy, side effect profile, and patient comorbidities.",
            ["antidepressants", "depression", "agents"],
            1.0
        ),
        SearchDocument(
            20,
            "Antipsychotic Agents",
            "Antipsychotics treat schizophrenia and bipolar disorder. Typical and atypical agents differ in receptor profiles and side effects.",
            ["antipsychotics", "psychosis", "agents"],
            1.0
        ),
        SearchDocument(
            21,
            "Antibiotic Mechanisms and Resistance",
            "Antibiotics target bacterial cell wall synthesis, protein synthesis, or DNA replication. Resistance arises via mutation, efflux pumps, or enzymatic degradation.",
            ["antibiotics", "mechanisms", "resistance"],
            1.0
        ),
        SearchDocument(
            22,
            "Antiviral Agents",
            "Antivirals inhibit viral entry, replication, or release. Classes include nucleoside analogs, protease inhibitors, and neuraminidase inhibitors.",
            ["antivirals", "viral infections", "agents"],
            1.0
        ),
        SearchDocument(
            23,
            "Non-Steroidal Anti-Inflammatory Drugs",
            "NSAIDs inhibit cyclooxygenase (COX), reducing prostaglandin synthesis and inflammation. Risks include GI ulceration, renal injury, and bleeding.",
            ["NSAIDs", "anti-inflammatory", "COX"],
            1.0
        ),
        SearchDocument(
            24,
            "Corticosteroids and Glucocorticoid Therapy",
            "Corticosteroids modulate gene expression to suppress inflammation and immune responses. Chronic use can cause adrenal suppression, osteoporosis, and hyperglycemia.",
            ["corticosteroids", "glucocorticoids", "therapy"],
            1.0
        ),
        SearchDocument(
            25,
            "Insulin Therapy and Diabetes Management",
            "Insulin lowers blood glucose by promoting cellular uptake. Diabetes management includes lifestyle, oral agents, and insulin regimens tailored to patient needs.",
            ["insulin", "diabetes", "management"],
            1.0
        ),
        SearchDocument(
            26,
            "Chemotherapy Mechanisms and Toxicity",
            "Chemotherapeutic agents target rapidly dividing cells via DNA damage, mitotic inhibition, or antimetabolite effects. Toxicities include myelosuppression and mucositis.",
            ["chemotherapy", "toxicity", "cancer"],
            1.0
        ),
        SearchDocument(
            27,
            "Pharmacogenomics and Individualized Therapy",
            "Pharmacogenomics studies genetic variability in drug response. Individualized therapy optimizes efficacy and minimizes adverse effects.",
            ["pharmacogenomics", "individualized therapy"],
            1.0
        ),
        SearchDocument(
            28,
            "Adverse Drug Reactions Classification",
            "Adverse drug reactions (ADRs) are classified as type A (predictable, dose-dependent) or type B (idiosyncratic, unpredictable). Monitoring and reporting are essential.",
            ["adverse reactions", "ADR", "classification"],
            1.0
        ),
        SearchDocument(
            29,
            "Controlled Substance Scheduling and Regulation",
            "Controlled substances are categorized into schedules based on abuse potential and medical use. Regulation involves prescribing restrictions and monitoring.",
            ["controlled substances", "scheduling", "regulation"],
            1.0
        ),
        SearchDocument(
            30,
            "Pediatric and Geriatric Pharmacology",
            "Drug pharmacokinetics and pharmacodynamics differ in children and the elderly due to organ function, body composition, and polypharmacy.",
            ["pediatric", "geriatric", "pharmacology"],
            1.0
        ),
        SearchDocument(
            31,
            "Drug Ionization and Absorption",
            "The degree of drug ionization affects absorption across biological membranes. Weak acids are better absorbed in acidic environments, weak bases in alkaline.",
            ["ionization", "absorption", "membranes"],
            1.0
        ),
        SearchDocument(
            32,
            "First-Pass Metabolism",
            "First-pass metabolism refers to the hepatic metabolism of drugs before reaching systemic circulation, reducing bioavailability of orally administered drugs.",
            ["first-pass", "hepatic metabolism", "bioavailability"],
            1.0
        ),
        SearchDocument(
            33,
            "Therapeutic Drug Monitoring",
            "Therapeutic drug monitoring (TDM) measures plasma drug concentrations to optimize efficacy and minimize toxicity, especially for drugs with narrow therapeutic windows.",
            ["TDM", "monitoring", "therapeutic window"],
            1.0
        ),
        SearchDocument(
            34,
            "Drug Clearance and Half-Life",
            "Drug clearance is the volume of plasma cleared of drug per unit time. Half-life determines dosing intervals and time to steady state.",
            ["clearance", "half-life", "dosing"],
            1.0
        ),
        SearchDocument(
            35,
            "Enzyme Induction and Inhibition",
            "Enzyme inducers increase, and inhibitors decrease, the activity of drug-metabolizing enzymes, impacting drug levels and efficacy.",
            ["enzyme induction", "inhibition", "metabolism"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)