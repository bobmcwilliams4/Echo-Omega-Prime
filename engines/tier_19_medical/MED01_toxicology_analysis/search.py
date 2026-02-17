import math
import threading
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set

# --- Data Classes ---

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

# --- Search Index ---

class SearchIndex:
    def __init__(self):
        self.documents: Dict[int, SearchDocument] = {}
        self.doc_tokens: Dict[int, List[str]] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.term_doc_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.term_df: Dict[str, int] = defaultdict(int)
        self.N: int = 0
        self.avgdl: float = 0.0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_norms: Dict[int, float] = {}

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.documents[doc.id] = doc
            self.doc_tokens[doc.id] = tokens
            self.doc_lengths[doc.id] = len(tokens)
            tf = Counter(tokens)
            for term, freq in tf.items():
                self.term_doc_freqs[term][doc.id] = freq
            for term in set(tokens):
                self.term_df[term] += 1
            self.N += 1
            self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self._idf_cache.clear()
            self._tfidf_norms.clear()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        candidate_docs: Set[int] = set()
        for term in query_terms:
            candidate_docs.update(self.term_doc_freqs.get(term, {}).keys())
        scores: Dict[int, float] = {}
        for doc_id in candidate_docs:
            bm25_score = self._score_bm25(doc_id, query_terms)
            tfidf_score = self._score_tfidf(doc_id, query_terms)
            doc_weight = self.documents[doc_id].weight
            score = 0.7 * bm25_score + 0.3 * tfidf_score
            score *= doc_weight
            scores[doc_id] = score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results = []
        for doc_id, score in ranked:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avgdl,
                "vocab_size": len(self.term_df)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
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
        score = 0.0
        doc_len = self.doc_lengths[doc_id]
        tf = Counter(self.doc_tokens[doc_id])
        for term in query_terms:
            if doc_id not in self.term_doc_freqs.get(term, {}):
                continue
            f = tf[term]
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / (self.avgdl if self.avgdl > 0 else 1))
            s = idf * (f * (self.k1 + 1)) / (denom + 1e-9)
            score += s
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        tf = Counter(self.doc_tokens[doc_id])
        norm = self._get_tfidf_norm(doc_id)
        score = 0.0
        for term in query_terms:
            tf_raw = tf.get(term, 0)
            if tf_raw == 0:
                continue
            tf_norm = tf_raw / self.doc_lengths[doc_id]
            idf = self._compute_idf(term)
            score += tf_norm * idf
        if norm > 0:
            score /= norm
        return score

    def _get_tfidf_norm(self, doc_id: int) -> float:
        if doc_id in self._tfidf_norms:
            return self._tfidf_norms[doc_id]
        tf = Counter(self.doc_tokens[doc_id])
        norm = 0.0
        for term, freq in tf.items():
            tf_norm = freq / self.doc_lengths[doc_id]
            idf = self._compute_idf(term)
            norm += (tf_norm * idf) ** 2
        norm = math.sqrt(norm)
        self._tfidf_norms[doc_id] = norm
        return norm

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], window: int = 30) -> str:
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            snippet = content[:200]
            return snippet + "..." if len(content) > 200 else snippet
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
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
            _seed_documents(_search_index_instance)
        return _search_index_instance

# --- Pre-seed Domain Documents ---

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Dose-Response Relationships in Toxicology",
            "Dose-response relationships describe how the magnitude of exposure to a chemical relates to the severity of the toxic effect. The threshold dose is the lowest dose at which an effect is observed.",
            ["dose_response", "toxicology"],
            1.0
        ),
        SearchDocument(
            2,
            "Lead Poisoning: Clinical Features and Management",
            "Lead poisoning presents with abdominal pain, anemia, neuropathy, and cognitive deficits. Chelation therapy with EDTA or dimercaprol is indicated for severe cases.",
            ["lead", "heavy_metal", "poisoning"],
            1.0
        ),
        SearchDocument(
            3,
            "Organophosphate Poisoning: Cholinergic Crisis",
            "Organophosphate compounds inhibit acetylcholinesterase, leading to muscarinic and nicotinic toxicity. Treatment includes atropine and pralidoxime.",
            ["organophosphate", "cholinergic", "poisoning"],
            1.0
        ),
        SearchDocument(
            4,
            "Acetaminophen Overdose: N-Acetylcysteine Protocol",
            "Acetaminophen toxicity causes hepatic necrosis. Early administration of N-acetylcysteine (NAC) prevents liver failure. Monitor transaminases and use the Rumack-Matthew nomogram.",
            ["acetaminophen", "overdose", "nac"],
            1.0
        ),
        SearchDocument(
            5,
            "Opioid Toxicity and Naloxone Reversal",
            "Opioid overdose presents with respiratory depression, miosis, and decreased consciousness. Naloxone is an opioid antagonist used for rapid reversal.",
            ["opioid", "naloxone", "toxicity"],
            1.0
        ),
        SearchDocument(
            6,
            "Carbon Monoxide Poisoning: Diagnosis and Treatment",
            "CO poisoning causes headache, confusion, and cherry-red skin. Diagnosis is by carboxyhemoglobin levels. Treatment is 100% oxygen or hyperbaric oxygen.",
            ["carbon_monoxide", "poisoning", "co"],
            1.0
        ),
        SearchDocument(
            7,
            "Cyanide Poisoning: Antidotes and Supportive Care",
            "Cyanide inhibits cytochrome oxidase, causing lactic acidosis and cardiovascular collapse. Hydroxocobalamin and sodium thiosulfate are antidotes.",
            ["cyanide", "poisoning", "antidote"],
            1.0
        ),
        SearchDocument(
            8,
            "Methanol and Ethylene Glycol Poisoning",
            "Methanol and ethylene glycol are toxic alcohols causing metabolic acidosis and end-organ damage. Fomepizole or ethanol inhibits alcohol dehydrogenase.",
            ["methanol", "ethylene_glycol", "poisoning"],
            1.0
        ),
        SearchDocument(
            9,
            "Occupational Exposure Limits for Heavy Metals",
            "Regulatory agencies set permissible exposure limits (PELs) for lead, mercury, and cadmium in the workplace. Monitoring and PPE are essential.",
            ["occupational", "exposure", "limits", "heavy_metals"],
            1.0
        ),
        SearchDocument(
            10,
            "Carcinogenicity Classification Systems",
            "IARC and EPA classify chemicals based on carcinogenic risk. Group 1 agents are carcinogenic to humans, while Group 2A are probable carcinogens.",
            ["carcinogenicity", "classification", "iarc"],
            1.0
        ),
        SearchDocument(
            11,
            "Snake Envenomation: Crotalidae (Pit Vipers)",
            "Crotalidae bites cause local tissue damage, coagulopathy, and systemic toxicity. Antivenom is the mainstay of treatment.",
            ["snake", "envenomation", "crotalidae"],
            1.0
        ),
        SearchDocument(
            12,
            "Lithium Toxicity: Recognition and Management",
            "Lithium toxicity presents with tremor, ataxia, confusion, and GI upset. Hemodialysis is indicated in severe cases.",
            ["lithium", "toxicity", "management"],
            1.0
        ),
        SearchDocument(
            13,
            "Chelation Therapy for Heavy Metal Poisoning",
            "Chelators such as EDTA, dimercaprol, and succimer are used to treat lead, mercury, and arsenic poisoning.",
            ["chelation", "heavy_metal", "poisoning"],
            1.0
        ),
        SearchDocument(
            14,
            "Rumack-Matthew Nomogram for Acetaminophen",
            "The Rumack-Matthew nomogram guides acetaminophen toxicity management based on serum levels and time since ingestion.",
            ["acetaminophen", "nomogram", "overdose"],
            1.0
        ),
        SearchDocument(
            15,
            "Delayed Neuropathy in Organophosphate Poisoning",
            "Organophosphate-induced delayed neuropathy (OPIDN) can occur weeks after exposure, presenting as distal weakness.",
            ["organophosphate", "neuropathy", "poisoning"],
            1.0
        ),
        SearchDocument(
            16,
            "Clinical Features of Carbon Monoxide Toxicity",
            "Symptoms include headache, dizziness, and altered mental status. Pulse oximetry is unreliable; use co-oximetry.",
            ["carbon_monoxide", "toxicity", "symptoms"],
            1.0
        ),
        SearchDocument(
            17,
            "Fomepizole in Toxic Alcohol Ingestion",
            "Fomepizole is a competitive inhibitor of alcohol dehydrogenase, used in methanol and ethylene glycol poisoning.",
            ["fomepizole", "methanol", "ethylene_glycol"],
            1.0
        ),
        SearchDocument(
            18,
            "Occupational Lead Exposure: Monitoring and Prevention",
            "Blood lead levels should be monitored in workers. Engineering controls and personal protective equipment reduce risk.",
            ["lead", "occupational", "exposure"],
            1.0
        ),
        SearchDocument(
            19,
            "IARC Carcinogen Groups Explained",
            "Group 1: Carcinogenic to humans. Group 2A: Probably carcinogenic. Group 2B: Possibly carcinogenic. Group 3: Not classifiable.",
            ["carcinogenicity", "iarc", "classification"],
            1.0
        ),
        SearchDocument(
            20,
            "Snakebite Management: Antivenom Dosing",
            "Antivenom dosing is based on clinical severity, not patient size. Monitor for allergic reactions.",
            ["snake", "antivenom", "management"],
            1.0
        ),
        SearchDocument(
            21,
            "Naloxone Administration in Opioid Overdose",
            "Naloxone can be administered IV, IM, or intranasally. Repeat dosing may be necessary for long-acting opioids.",
            ["naloxone", "opioid", "overdose"],
            1.0
        ),
        SearchDocument(
            22,
            "Cyanide Toxicity: Clinical Manifestations",
            "Symptoms include headache, confusion, and cardiovascular collapse. Bitter almond odor may be noted.",
            ["cyanide", "toxicity", "symptoms"],
            1.0
        ),
        SearchDocument(
            23,
            "Permissible Exposure Limits (PELs) for Carcinogens",
            "OSHA sets PELs for known carcinogens in the workplace. Regular monitoring and reporting are required.",
            ["occupational", "carcinogen", "limits"],
            1.0
        ),
        SearchDocument(
            24,
            "Chronic Effects of Low-Level Lead Exposure",
            "Even low levels of lead exposure can cause cognitive deficits in children and hypertension in adults.",
            ["lead", "chronic", "exposure"],
            1.0
        ),
        SearchDocument(
            25,
            "Snake Envenomation: Local and Systemic Effects",
            "Crotalidae venom causes pain, swelling, and coagulopathy. Systemic symptoms may include hypotension and shock.",
            ["snake", "envenomation", "effects"],
            1.0
        ),
        SearchDocument(
            26,
            "Carcinogenicity: Mechanisms of Chemical Carcinogens",
            "Chemical carcinogens can cause DNA damage, promote cell proliferation, and inhibit apoptosis.",
            ["carcinogenicity", "mechanisms"],
            1.0
        ),
        SearchDocument(
            27,
            "Organophosphate Poisoning: Muscarinic and Nicotinic Effects",
            "Muscarinic effects: salivation, lacrimation, urination, defecation. Nicotinic effects: muscle fasciculations, weakness.",
            ["organophosphate", "muscarinic", "nicotinic"],
            1.0
        ),
        SearchDocument(
            28,
            "Lithium Toxicity: Risk Factors",
            "Renal impairment, dehydration, and drug interactions increase the risk of lithium toxicity.",
            ["lithium", "toxicity", "risk"],
            1.0
        ),
        SearchDocument(
            29,
            "Methanol Poisoning: Ocular Toxicity",
            "Methanol is metabolized to formic acid, causing optic nerve damage and blindness.",
            ["methanol", "ocular", "toxicity"],
            1.0
        ),
        SearchDocument(
            30,
            "Ethylene Glycol Poisoning: Renal Failure",
            "Ethylene glycol is metabolized to oxalic acid, leading to renal tubular damage and hypocalcemia.",
            ["ethylene_glycol", "renal", "toxicity"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)