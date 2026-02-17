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
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
        self.doc_lengths: Dict[int, int] = {}
        self.avg_doc_length: float = 0.0
        self.N: int = 0
        self.lock = threading.Lock()
        self._idf_cache: Dict[str, float] = {}
        self._tfidf_cache: Dict[int, Dict[str, float]] = {}
        self._recompute_stats = True

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.title + " " + doc.content)
            self.doc_lengths[doc.id] = len(tokens)
            self.documents[doc.id] = doc
            freq = Counter(tokens)
            for term, count in freq.items():
                self.inverted_index[term].append((doc.id, count))
                self.doc_freqs[term] += 1
            self.N += 1
            self._recompute_stats = True

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        with self.lock:
            if self._recompute_stats:
                self._update_stats()
            candidate_docs = self._get_candidate_docs(query_terms)
            scored = []
            for doc_id in candidate_docs:
                bm25_score = self._score_bm25(doc_id, query_terms)
                tfidf_score = self._score_tfidf(doc_id, query_terms)
                doc = self.documents[doc_id]
                score = bm25_score * 0.7 + tfidf_score * 0.3
                snippet = self._make_snippet(doc, query_terms)
                scored.append(SearchResult(doc_id, score * doc.weight, doc.title, snippet))
            scored.sort(key=lambda x: x.score, reverse=True)
            return scored[:limit]

    def get_stats(self) -> Dict[str, float]:
        with self.lock:
            if self._recompute_stats:
                self._update_stats()
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "num_terms": len(self.doc_freqs)
            }

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_]+\b', text)
        return tokens

    def _update_stats(self):
        total_length = sum(self.doc_lengths.values())
        self.avg_doc_length = total_length / self.N if self.N > 0 else 0.0
        self._idf_cache.clear()
        self._tfidf_cache.clear()
        self._recompute_stats = False

    def _compute_idf(self, term: str) -> float:
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5)) if df > 0 else 0.0
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, doc_id: int, query_terms: List[str]) -> float:
        doc = self.documents[doc_id]
        tokens = self._tokenize(doc.title + " " + doc.content)
        freq = Counter(tokens)
        score = 0.0
        for term in set(query_terms):
            if term not in freq:
                continue
            idf = self._compute_idf(term)
            tf = freq[term]
            denom = tf + self.k1 * (1 - self.b + self.b * (self.doc_lengths[doc_id] / self.avg_doc_length))
            score += idf * ((tf * (self.k1 + 1)) / denom)
        return score

    def _score_tfidf(self, doc_id: int, query_terms: List[str]) -> float:
        if doc_id in self._tfidf_cache:
            tfidf_vec = self._tfidf_cache[doc_id]
        else:
            doc = self.documents[doc_id]
            tokens = self._tokenize(doc.title + " " + doc.content)
            freq = Counter(tokens)
            tfidf_vec = {}
            for term, tf in freq.items():
                idf = self._compute_idf(term)
                tfidf_vec[term] = (tf / len(tokens)) * idf
            self._tfidf_cache[doc_id] = tfidf_vec
        score = 0.0
        for term in set(query_terms):
            score += tfidf_vec.get(term, 0.0)
        return score

    def _get_candidate_docs(self, query_terms: List[str]) -> set:
        candidate_docs = set()
        for term in set(query_terms):
            for doc_id, _ in self.inverted_index.get(term, []):
                candidate_docs.add(doc_id)
        return candidate_docs

    def _make_snippet(self, doc: SearchDocument, query_terms: List[str], snippet_len: int = 160) -> str:
        content = doc.content
        content_lower = content.lower()
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                start = max(0, idx - 40)
                end = min(len(content), idx + snippet_len - 40)
                snippet = content[start:end]
                # Highlight term
                snippet = re.sub(f"({term})", r"**\1**", snippet, flags=re.IGNORECASE)
                return snippet.strip()
        # fallback: start of content
        snippet = content[:snippet_len]
        return snippet.strip()

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

def _seed_documents(index: SearchIndex):
    docs = [
        SearchDocument(
            1,
            "Nuclear Fission Chain Reaction",
            "A nuclear fission chain reaction occurs when a fissile atom such as uranium-235 absorbs a neutron and splits, releasing additional neutrons. These neutrons can induce further fissions, sustaining the reaction. Control of the chain reaction is essential for safe reactor operation.",
            ["nuclear_fission_chain_reaction", "reactor_physics"],
            1.0
        ),
        SearchDocument(
            2,
            "Neutron Moderation and Thermalization",
            "Neutron moderation is the process of slowing down fast neutrons produced by fission to thermal energies, increasing the probability of further fission events. Common moderators include light water, heavy water, and graphite.",
            ["neutron_moderation_thermalization", "reactor_physics"],
            1.0
        ),
        SearchDocument(
            3,
            "PWR Primary and Secondary Loop",
            "Pressurized Water Reactors (PWR) use two separate coolant loops. The primary loop circulates water under high pressure through the reactor core, transferring heat to the secondary loop via a steam generator. This separation prevents radioactive contamination of the turbine.",
            ["pwr_primary_secondary_loop", "pwr_design"],
            1.0
        ),
        SearchDocument(
            4,
            "PWR Reactivity Control: Boron and Control Rods",
            "In PWRs, reactivity is managed by dissolving boric acid in the coolant (chemical shim) and by inserting or withdrawing control rods made of neutron-absorbing materials. This allows fine control of the reactor's power output and shutdown capability.",
            ["pwr_reactivity_control_boron_rods", "pwr_design"],
            1.0
        ),
        SearchDocument(
            5,
            "BWR Direct Cycle Design",
            "Boiling Water Reactors (BWR) use a direct cycle where water boils inside the reactor core, producing steam that directly drives the turbine. This design simplifies the system but requires careful management of radioactive steam.",
            ["bwr_direct_cycle_design", "bwr_design"],
            1.0
        ),
        SearchDocument(
            6,
            "BWR Control Rods: Cruciform Shape",
            "BWR control rods are typically cruciform (cross-shaped) and are inserted from below the core. Their geometry allows for effective neutron absorption and fine reactivity control during operation.",
            ["bwr_control_rods_cruciform", "bwr_design"],
            1.0
        ),
        SearchDocument(
            7,
            "Nuclear Fuel: UO2 and Zircaloy Cladding",
            "Most commercial reactors use uranium dioxide (UO2) fuel pellets encased in zircaloy cladding. Zircaloy provides corrosion resistance and structural integrity while allowing neutrons to pass through with minimal absorption.",
            ["nuclear_fuel_uo2_zircaloy", "fuel_technology"],
            1.0
        ),
        SearchDocument(
            8,
            "Fuel Burnup and Depletion",
            "Fuel burnup measures the amount of energy extracted from nuclear fuel, typically in gigawatt-days per metric ton. As burnup increases, fission products accumulate and fuel composition changes, affecting reactor operation and waste characteristics.",
            ["fuel_burnup_depletion", "fuel_management"],
            1.0
        ),
        SearchDocument(
            9,
            "Delayed Neutrons and Reactor Period",
            "Delayed neutrons are emitted by certain fission products seconds after fission. They are crucial for reactor control, as they slow the rate of power changes and allow operators to respond to reactivity changes. The reactor period quantifies how quickly power changes.",
            ["delayed_neutrons_reactor_period", "reactor_control"],
            1.0
        ),
        SearchDocument(
            10,
            "Xenon Poisoning and Iodine Dynamics",
            "Xenon-135 is a potent neutron absorber produced from iodine-135 decay. Its buildup after power changes can significantly affect reactivity, a phenomenon known as xenon poisoning. Operators must manage xenon transients to maintain stable power.",
            ["xenon_poisoning_iodine_dynamics", "reactor_control"],
            1.0
        ),
        SearchDocument(
            11,
            "Defense-in-Depth Safety Philosophy",
            "Defense-in-depth is a safety strategy that employs multiple, redundant barriers and safety systems to prevent and mitigate accidents. It includes physical barriers, engineered safety features, and administrative controls.",
            ["defense_in_depth_safety_philosophy", "nuclear_safety"],
            1.0
        ),
        SearchDocument(
            12,
            "Emergency Core Cooling Systems (ECCS)",
            "ECCS are designed to provide cooling to the reactor core during loss-of-coolant accidents. They include high-pressure and low-pressure injection systems, accumulators, and containment spray systems.",
            ["eccs_emergency_core_cooling", "nuclear_safety"],
            1.0
        ),
        SearchDocument(
            13,
            "Containment Structure Function",
            "The containment structure is a robust, airtight building surrounding the reactor vessel. It serves as the final barrier to prevent the release of radioactive materials during accidents.",
            ["containment_structure_function", "nuclear_safety"],
            1.0
        ),
        SearchDocument(
            14,
            "ALARA Dose Limits",
            "The ALARA (As Low As Reasonably Achievable) principle guides radiation protection practices. Dose limits are set by regulatory bodies, and operators must minimize exposures through engineering controls and administrative procedures.",
            ["alara_dose_limits", "radiation_protection"],
            1.0
        ),
        SearchDocument(
            15,
            "Spent Fuel Pool Storage",
            "After removal from the reactor, spent fuel assemblies are stored underwater in spent fuel pools. The water provides cooling and radiation shielding, allowing for safe handling and decay of short-lived isotopes.",
            ["spent_fuel_pool_storage", "fuel_management"],
            1.0
        ),
        SearchDocument(
            16,
            "Dry Cask Storage and ISFSI",
            "After sufficient cooling in pools, spent fuel can be transferred to dry cask storage at an Independent Spent Fuel Storage Installation (ISFSI). Casks provide passive cooling and shielding for long-term storage.",
            ["dry_cask_storage_isfsi", "fuel_management"],
            1.0
        ),
        SearchDocument(
            17,
            "Nuclear Waste Classification: HLW and LLW",
            "Nuclear waste is classified based on radioactivity and origin. High-Level Waste (HLW) includes spent fuel and reprocessing waste, while Low-Level Waste (LLW) includes contaminated materials from plant operations.",
            ["nuclear_waste_classification_hlw_llw", "waste_management"],
            1.0
        ),
        SearchDocument(
            18,
            "NRC 10 CFR 50 Licensing",
            "The U.S. Nuclear Regulatory Commission (NRC) regulates nuclear power plants under Title 10, Code of Federal Regulations, Part 50. Licensing covers design, construction, operation, and decommissioning, ensuring safety and environmental protection.",
            ["nrc_10cfr50_licensing", "regulation"],
            1.0
        ),
        SearchDocument(
            19,
            "Small Modular Reactors (SMR)",
            "Small Modular Reactors are advanced nuclear designs with reduced size and modular construction. SMRs offer enhanced safety features, flexible deployment, and potential cost savings compared to traditional large reactors.",
            ["small_modular_reactors_smr", "advanced_reactors"],
            1.0
        ),
        SearchDocument(
            20,
            "Fusion Energy and Tokamak Basics",
            "Fusion energy seeks to replicate the sun's process by fusing light nuclei at high temperatures. Tokamaks use strong magnetic fields to confine hot plasma, enabling fusion reactions and energy production.",
            ["fusion_energy_tokamak_basics", "fusion"],
            1.0
        ),
        SearchDocument(
            21,
            "Moderator Materials: Light Water, Heavy Water, Graphite",
            "Moderator materials slow down neutrons to thermal energies. Light water is common in PWRs and BWRs, heavy water in CANDU reactors, and graphite in some gas-cooled reactors.",
            ["neutron_moderation_thermalization", "moderator_materials"],
            1.0
        ),
        SearchDocument(
            22,
            "Reactor Coolant Chemistry and Boron Concentration",
            "Controlling boron concentration in PWR coolant is essential for reactivity management. Chemistry control also prevents corrosion and maintains fuel and component integrity.",
            ["pwr_reactivity_control_boron_rods", "reactor_chemistry"],
            1.0
        ),
        SearchDocument(
            23,
            "Boiling Crisis and Critical Heat Flux in BWRs",
            "The boiling crisis, or departure from nucleate boiling, occurs when heat flux exceeds a critical value, causing a rapid rise in fuel temperature. BWRs are designed to avoid this condition through careful thermal-hydraulic analysis.",
            ["bwr_direct_cycle_design", "thermal_hydraulics"],
            1.0
        ),
        SearchDocument(
            24,
            "Zircaloy Cladding: Properties and Failure Modes",
            "Zircaloy cladding provides mechanical strength and corrosion resistance for fuel rods. Failure modes include cladding breach, hydriding, and stress corrosion cracking.",
            ["nuclear_fuel_uo2_zircaloy", "materials"],
            1.0
        ),
        SearchDocument(
            25,
            "Decay Heat and Spent Fuel Management",
            "Even after shutdown, spent fuel continues to generate decay heat. Spent fuel pools and dry casks are designed to remove this heat and prevent overheating.",
            ["spent_fuel_pool_storage", "dry_cask_storage_isfsi"],
            1.0
        ),
        SearchDocument(
            26,
            "Redundancy and Diversity in Defense-in-Depth",
            "Redundancy ensures backup systems are available, while diversity uses different principles or technologies to achieve safety functions. Both are key to defense-in-depth in nuclear safety.",
            ["defense_in_depth_safety_philosophy", "nuclear_safety"],
            1.0
        ),
        SearchDocument(
            27,
            "Iodine Spiking During Reactor Transients",
            "During power changes, iodine-135 concentrations can spike, affecting xenon-135 buildup and reactor reactivity. Operators monitor and manage these transients to maintain control.",
            ["xenon_poisoning_iodine_dynamics", "reactor_control"],
            1.0
        ),
        SearchDocument(
            28,
            "Fusion vs. Fission: Key Differences",
            "Fission splits heavy nuclei to release energy, while fusion combines light nuclei. Fusion produces less long-lived radioactive waste and has inherent safety advantages.",
            ["fusion_energy_tokamak_basics", "nuclear_fission_chain_reaction"],
            1.0
        ),
        SearchDocument(
            29,
            "Passive Safety in Small Modular Reactors",
            "SMRs often employ passive safety systems that rely on natural forces like gravity and convection, reducing reliance on active components and operator intervention.",
            ["small_modular_reactors_smr", "nuclear_safety"],
            1.0
        ),
        SearchDocument(
            30,
            "Low-Level Waste Disposal Techniques",
            "LLW is typically disposed of in near-surface facilities with engineered barriers. Waste classification ensures proper handling, transport, and disposal.",
            ["nuclear_waste_classification_hlw_llw", "waste_management"],
            1.0
        ),
        SearchDocument(
            31,
            "Reactor Shutdown: Control Rod Insertion and Boron Injection",
            "Rapid reactor shutdown (scram) is achieved by fully inserting control rods and, in PWRs, injecting soluble boron. These measures quickly halt the chain reaction.",
            ["pwr_reactivity_control_boron_rods", "reactor_control"],
            1.0
        ),
        SearchDocument(
            32,
            "Containment Leak Rate Testing",
            "Periodic leak rate tests verify the integrity of the containment structure, ensuring it can perform its safety function during an accident.",
            ["containment_structure_function", "nuclear_safety"],
            1.0
        ),
        SearchDocument(
            33,
            "Fuel Depletion Codes and Burnup Calculations",
            "Computer codes model fuel depletion and burnup, predicting isotopic changes and reactivity over time. Accurate calculations support safe fuel management.",
            ["fuel_burnup_depletion", "fuel_management"],
            1.0
        ),
        SearchDocument(
            34,
            "Fusion Plasma Confinement: Magnetic and Inertial",
            "Tokamaks use magnetic confinement, while other approaches use inertial confinement. Both aim to maintain plasma conditions for sustained fusion.",
            ["fusion_energy_tokamak_basics", "fusion"],
            1.0
        ),
        SearchDocument(
            35,
            "NRC Licensing: Safety Analysis Report (SAR)",
            "A Safety Analysis Report is a key part of NRC licensing, documenting plant design, safety systems, and accident analyses.",
            ["nrc_10cfr50_licensing", "regulation"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)