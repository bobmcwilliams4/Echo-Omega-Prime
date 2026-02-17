import math
import threading
import heapq
import re
from collections import defaultdict, Counter

class SearchDocument:
    def __init__(self, id, title, content, tags=None, weight=1.0):
        self.id = id
        self.title = title
        self.content = content
        self.tags = tags or []
        self.weight = weight

class SearchResult:
    def __init__(self, doc_id, score, title, snippet):
        self.doc_id = doc_id
        self.score = score
        self.title = title
        self.snippet = snippet

class SearchIndex:
    def __init__(self):
        self.documents = {}
        self.doc_lengths = {}
        self.avg_doc_length = 0.0
        self.term_doc_freq = defaultdict(int)  # term -> doc freq
        self.term_freqs = defaultdict(lambda: defaultdict(int))  # term -> doc_id -> freq
        self.doc_term_counts = defaultdict(Counter)  # doc_id -> Counter(term)
        self.N = 0
        self.lock = threading.Lock()
        self.k1 = 1.5
        self.b = 0.75
        self.idf_cache = {}
        self._recompute_stats()

    def add_document(self, doc):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + " " + doc.content)
            term_counts = Counter(tokens)
            self.doc_term_counts[doc.id] = term_counts
            doc_len = sum(term_counts.values())
            self.doc_lengths[doc.id] = doc_len
            for term, freq in term_counts.items():
                self.term_freqs[term][doc.id] = freq
                self.term_doc_freq[term] += 1
            self.N += 1
            self._recompute_stats()
            self.idf_cache.clear()

    def search(self, query, limit=10):
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        scores = defaultdict(float)
        doc_snippets = {}
        for term in set(query_terms):
            idf = self._compute_idf(term)
            postings = self.term_freqs.get(term, {})
            for doc_id, freq in postings.items():
                doc = self.documents[doc_id]
                bm25_score = self._score_bm25(term, doc_id, freq, idf)
                tfidf_score = self._score_tfidf(term, doc_id, freq, idf)
                score = bm25_score * 0.7 + tfidf_score * 0.3
                score *= doc.weight
                scores[doc_id] += score
        for doc_id in scores:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc, query_terms)
            doc_snippets[doc_id] = snippet
        top_docs = heapq.nlargest(limit, scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = doc_snippets.get(doc_id, "")
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self):
        with self.lock:
            return {
                "num_documents": self.N,
                "avg_doc_length": self.avg_doc_length,
                "vocab_size": len(self.term_doc_freq),
            }

    def _tokenize(self, text):
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9\-]+\b', text)
        return tokens

    def _compute_idf(self, term):
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = self.term_doc_freq.get(term, 0)
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, term, doc_id, freq, idf):
        dl = self.doc_lengths[doc_id]
        avgdl = self.avg_doc_length if self.avg_doc_length > 0 else 1.0
        k1 = self.k1
        b = self.b
        numerator = freq * (k1 + 1)
        denominator = freq + k1 * (1 - b + b * dl / avgdl)
        return idf * numerator / denominator

    def _score_tfidf(self, term, doc_id, freq, idf):
        tf = freq / (self.doc_lengths[doc_id] if self.doc_lengths[doc_id] > 0 else 1)
        return tf * idf

    def _make_snippet(self, doc, query_terms, window=30):
        content = doc.content
        content_lower = content.lower()
        positions = []
        for term in query_terms:
            idx = content_lower.find(term)
            if idx != -1:
                positions.append(idx)
        if not positions:
            return content[:window*2] + "..." if len(content) > window*2 else content
        start = max(min(positions) - window, 0)
        end = min(max(positions) + window, len(content))
        snippet = content[start:end]
        for term in set(query_terms):
            snippet = re.sub(r'(?i)\b(' + re.escape(term) + r')\b', r'**\1**', snippet)
        return snippet + ("..." if end < len(content) else "")

    def _recompute_stats(self):
        if not self.doc_lengths:
            self.avg_doc_length = 0.0
        else:
            self.avg_doc_length = sum(self.doc_lengths.values()) / max(len(self.doc_lengths), 1)

# Singleton factory for SearchIndex
_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index():
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(idx):
    docs = [
        SearchDocument(
            id="1",
            title="Free Radical Addition Polymerization: Mechanism and Kinetics",
            content="Free radical addition polymerization involves initiation, propagation, and termination steps. Initiators such as benzoyl peroxide generate radicals that add to monomers like styrene or methyl methacrylate. The process is characterized by chain reactions and is widely used for producing polymers like polystyrene and PMMA.",
            tags=["free radical", "addition", "polymerization", "mechanism", "kinetics"],
            weight=1.0
        ),
        SearchDocument(
            id="2",
            title="Living/Controlled Radical Polymerization: ATRP, RAFT, and NMP",
            content="Living radical polymerization techniques such as Atom Transfer Radical Polymerization (ATRP), Reversible Addition-Fragmentation Chain Transfer (RAFT), and Nitroxide Mediated Polymerization (NMP) allow precise control over molecular weight and architecture. These methods minimize termination and enable block copolymer synthesis.",
            tags=["living", "controlled", "radical", "ATRP", "RAFT", "NMP"],
            weight=1.0
        ),
        SearchDocument(
            id="3",
            title="Condensation Step-Growth Polymerization: Polyesters and Polyamides",
            content="Condensation (step-growth) polymerization involves the reaction of bifunctional or multifunctional monomers, with the elimination of small molecules like water or methanol. Examples include the synthesis of polyesters (PET) and polyamides (nylon). The process is distinct from chain-growth polymerization.",
            tags=["condensation", "step-growth", "polyester", "polyamide"],
            weight=1.0
        ),
        SearchDocument(
            id="4",
            title="Molecular Weight Distribution in Polymers and GPC/SEC Analysis",
            content="Gel Permeation Chromatography (GPC) or Size Exclusion Chromatography (SEC) is used to determine the molecular weight distribution of polymers. Key parameters include number average (Mn), weight average (Mw), and polydispersity index (PDI). Accurate MWD analysis is crucial for polymer property control.",
            tags=["GPC", "SEC", "molecular weight", "distribution", "PDI"],
            weight=1.0
        ),
        SearchDocument(
            id="5",
            title="Thermal Analysis of Polymers: Differential Scanning Calorimetry (DSC)",
            content="DSC measures heat flow associated with thermal transitions in polymers, such as glass transition (Tg), melting (Tm), and crystallization. It provides insights into polymer crystallinity, purity, and thermal stability, which are essential for processing and application development.",
            tags=["DSC", "thermal analysis", "glass transition", "melting"],
            weight=1.0
        ),
        SearchDocument(
            id="6",
            title="Polymer Rheology and Viscoelasticity: Fundamentals and Applications",
            content="Polymer rheology examines the flow and deformation behavior of polymer melts and solutions. Viscoelastic properties, including storage modulus (G') and loss modulus (G''), are measured using oscillatory rheometry. Understanding rheology is vital for processing and end-use performance.",
            tags=["rheology", "viscoelasticity", "modulus", "oscillatory"],
            weight=1.0
        ),
        SearchDocument(
            id="7",
            title="Injection Molding: Principles of Polymer Processing",
            content="Injection molding is a widely used polymer processing technique involving the injection of molten polymer into a mold. Key parameters include melt temperature, injection pressure, and cooling rate. The process enables mass production of complex plastic parts with high precision.",
            tags=["injection molding", "processing", "polymer", "manufacturing"],
            weight=1.0
        ),
        SearchDocument(
            id="8",
            title="Polymer Degradation: Thermal, UV, Oxidative, and Hydrolytic Mechanisms",
            content="Polymers can degrade via thermal, ultraviolet (UV), oxidative, and hydrolytic pathways. Degradation leads to changes in molecular weight, mechanical properties, and appearance. Stabilizers and antioxidants are often added to enhance polymer durability.",
            tags=["degradation", "thermal", "UV", "oxidative", "hydrolytic"],
            weight=1.0
        ),
        SearchDocument(
            id="9",
            title="Polymer Blends and Compatibilization Strategies",
            content="Polymer blends combine two or more polymers to achieve desired properties. Compatibilizers, such as block copolymers, are used to improve interfacial adhesion and phase dispersion. Blends can exhibit synergistic mechanical, thermal, or barrier properties.",
            tags=["blends", "compatibilization", "block copolymer"],
            weight=1.0
        ),
        SearchDocument(
            id="10",
            title="Biopolymers and Biodegradable Polymers: PLA, PHA, and Starch Derivatives",
            content="Biopolymers such as polylactic acid (PLA), polyhydroxyalkanoates (PHA), and starch-based polymers are derived from renewable resources and are biodegradable. They are used in packaging, agriculture, and biomedical applications as sustainable alternatives to conventional plastics.",
            tags=["biopolymer", "biodegradable", "PLA", "PHA", "starch"],
            weight=1.0
        ),
        SearchDocument(
            id="11",
            title="Oilfield Polymer Applications: Enhanced Oil Recovery (EOR) and Drilling Fluids",
            content="Polymers such as polyacrylamide and xanthan gum are used in oilfield applications for enhanced oil recovery (EOR) and as viscosifiers in drilling fluids. These polymers improve sweep efficiency and control fluid loss in challenging reservoir conditions.",
            tags=["oilfield", "EOR", "drilling", "polyacrylamide", "xanthan"],
            weight=1.0
        ),
        SearchDocument(
            id="12",
            title="Polymer Composites: Fiber Reinforcement and Matrix Selection",
            content="Polymer composites consist of a polymer matrix reinforced with fibers such as glass, carbon, or aramid. The choice of matrix and reinforcement affects mechanical properties, thermal stability, and processability. Applications include aerospace, automotive, and construction.",
            tags=["composite", "fiber", "reinforcement", "matrix"],
            weight=1.0
        ),
        SearchDocument(
            id="13",
            title="Chain Transfer Agents in Radical Polymerization",
            content="Chain transfer agents are used in free radical polymerization to control molecular weight by transferring the active center to another molecule. Common agents include thiols and halogenated compounds. This technique is important for tailoring polymer properties.",
            tags=["chain transfer", "radical", "polymerization"],
            weight=1.0
        ),
        SearchDocument(
            id="14",
            title="RAFT Polymerization: Mechanism and Applications",
            content="RAFT (Reversible Addition-Fragmentation Chain Transfer) polymerization uses chain transfer agents to mediate radical polymerization, enabling control over polymer architecture. RAFT is versatile and applicable to a wide range of monomers.",
            tags=["RAFT", "polymerization", "mechanism"],
            weight=1.0
        ),
        SearchDocument(
            id="15",
            title="Atom Transfer Radical Polymerization (ATRP): Catalysts and Kinetics",
            content="ATRP employs transition metal catalysts (e.g., CuBr/ligand) to reversibly activate and deactivate growing polymer chains. This allows for precise control of molecular weight and low polydispersity. ATRP is widely used for block copolymer synthesis.",
            tags=["ATRP", "catalyst", "kinetics"],
            weight=1.0
        ),
        SearchDocument(
            id="16",
            title="Nitroxide Mediated Polymerization (NMP): Principles and Applications",
            content="NMP utilizes stable nitroxide radicals to mediate the polymerization process, providing living characteristics. It is particularly effective for styrenic and acrylate monomers, enabling the synthesis of well-defined polymers.",
            tags=["NMP", "nitroxide", "polymerization"],
            weight=1.0
        ),
        SearchDocument(
            id="17",
            title="Polymerization Kinetics: Rate Laws and Mechanistic Insights",
            content="Understanding the kinetics of polymerization reactions is crucial for process optimization. Rate laws describe the dependence of polymerization rate on monomer, initiator, and catalyst concentrations. Mechanistic studies inform the design of new polymerization systems.",
            tags=["kinetics", "rate law", "mechanism"],
            weight=1.0
        ),
        SearchDocument(
            id="18",
            title="Polymer Molecular Weight Determination: Mn, Mw, and PDI",
            content="Number average molecular weight (Mn), weight average molecular weight (Mw), and polydispersity index (PDI) are key parameters for characterizing polymers. Techniques such as GPC/SEC and light scattering are commonly used for determination.",
            tags=["Mn", "Mw", "PDI", "GPC", "SEC"],
            weight=1.0
        ),
        SearchDocument(
            id="19",
            title="Thermal Stability and Degradation of Polymers",
            content="Thermal stability is a critical property for polymers used in high-temperature applications. Degradation mechanisms include chain scission and crosslinking, which affect performance. Thermogravimetric analysis (TGA) is often used to assess stability.",
            tags=["thermal stability", "degradation", "TGA"],
            weight=1.0
        ),
        SearchDocument(
            id="20",
            title="DSC Analysis: Glass Transition and Melting Behavior",
            content="Differential Scanning Calorimetry (DSC) is used to study glass transition (Tg), melting (Tm), and crystallization of polymers. The technique provides valuable information on thermal transitions and phase behavior.",
            tags=["DSC", "glass transition", "melting"],
            weight=1.0
        ),
        SearchDocument(
            id="21",
            title="Viscoelastic Properties of Polymers: Time-Temperature Superposition",
            content="Time-temperature superposition is a technique used to predict long-term viscoelastic behavior of polymers from short-term tests. Master curves are constructed by shifting data along the time or frequency axis.",
            tags=["viscoelastic", "time-temperature", "superposition"],
            weight=1.0
        ),
        SearchDocument(
            id="22",
            title="Injection Molding Defects and Troubleshooting",
            content="Common injection molding defects include sink marks, warpage, short shots, and flash. Troubleshooting involves adjusting processing parameters and mold design to minimize defects and improve part quality.",
            tags=["injection molding", "defect", "troubleshooting"],
            weight=1.0
        ),
        SearchDocument(
            id="23",
            title="UV Stabilizers and Antioxidants in Polymer Formulations",
            content="UV stabilizers and antioxidants are additives used to enhance the durability of polymers exposed to sunlight and oxygen. Hindered amine light stabilizers (HALS) and phenolic antioxidants are commonly employed.",
            tags=["UV", "stabilizer", "antioxidant"],
            weight=1.0
        ),
        SearchDocument(
            id="24",
            title="Compatibilizers for Polymer Blends: Block and Graft Copolymers",
            content="Compatibilizers such as block and graft copolymers improve phase adhesion in immiscible polymer blends. They are essential for achieving uniform morphology and enhanced mechanical properties.",
            tags=["compatibilizer", "block copolymer", "graft copolymer"],
            weight=1.0
        ),
        SearchDocument(
            id="25",
            title="Biodegradation Mechanisms of Biopolymers",
            content="Biopolymers degrade via enzymatic, hydrolytic, and microbial pathways. The rate of biodegradation depends on polymer structure, environmental conditions, and presence of microorganisms.",
            tags=["biodegradation", "biopolymer", "mechanism"],
            weight=1.0
        ),
        SearchDocument(
            id="26",
            title="Polymer Nanocomposites: Structure and Properties",
            content="Polymer nanocomposites incorporate nanoscale fillers such as clay, silica, or carbon nanotubes to enhance mechanical, thermal, and barrier properties. Dispersion and interfacial adhesion are key factors for performance.",
            tags=["nanocomposite", "nanotube", "clay", "silica"],
            weight=1.0
        ),
        SearchDocument(
            id="27",
            title="Hydrolytic Degradation of Polyesters",
            content="Polyesters such as PLA and PET are susceptible to hydrolytic degradation, especially under moist or acidic conditions. Hydrolysis leads to chain scission and reduction in molecular weight.",
            tags=["hydrolytic", "degradation", "polyester"],
            weight=1.0
        ),
        SearchDocument(
            id="28",
            title="Polymer Processing: Extrusion and Blow Molding",
            content="Extrusion and blow molding are essential polymer processing techniques for producing films, pipes, and bottles. Process parameters such as temperature profile and screw speed influence product quality.",
            tags=["extrusion", "blow molding", "processing"],
            weight=1.0
        ),
        SearchDocument(
            id="29",
            title="Fiber Reinforced Polymer Composites: Glass and Carbon Fibers",
            content="Glass and carbon fibers are widely used to reinforce polymer matrices, resulting in composites with high strength-to-weight ratios. Surface treatments and sizing agents improve fiber-matrix adhesion.",
            tags=["fiber", "glass", "carbon", "composite"],
            weight=1.0
        ),
        SearchDocument(
            id="30",
            title="Polymer Additives: Plasticizers, Fillers, and Flame Retardants",
            content="Additives such as plasticizers, fillers, and flame retardants are incorporated into polymers to modify properties and enhance performance. Selection depends on application requirements and regulatory considerations.",
            tags=["additive", "plasticizer", "filler", "flame retardant"],
            weight=1.0
        ),
    ]
    for doc in docs:
        idx.add_document(doc)