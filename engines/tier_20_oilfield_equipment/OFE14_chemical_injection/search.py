import math
import threading
import heapq
import re
from collections import defaultdict, Counter

class SearchDocument:
    def __init__(self, doc_id, title, content, tags=None, weight=1.0):
        self.id = doc_id
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
        self.term_doc_freq = defaultdict(set)
        self.term_freq = defaultdict(lambda: defaultdict(int))
        self.idf_cache = {}
        self.lock = threading.Lock()
        self.total_docs = 0
        self.tags_index = defaultdict(set)
        self._re_token = re.compile(r'\b\w+\b')
        self._bm25_k1 = 1.5
        self._bm25_b = 0.75

    def add_document(self, doc: SearchDocument):
        with self.lock:
            if doc.id in self.documents:
                return
            self.documents[doc.id] = doc
            tokens = self._tokenize(doc.title + ' ' + doc.content)
            doc_len = len(tokens)
            self.doc_lengths[doc.id] = doc_len
            for token in tokens:
                self.term_doc_freq[token].add(doc.id)
                self.term_freq[token][doc.id] += 1
            for tag in doc.tags:
                self.tags_index[tag.lower()].add(doc.id)
            self.total_docs += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs
            self.idf_cache.clear()

    def search(self, query, limit=10):
        query_tokens = self._tokenize(query)
        doc_scores = defaultdict(float)
        doc_snippets = {}
        for token in query_tokens:
            idf = self._compute_idf(token)
            for doc_id in self.term_doc_freq.get(token, []):
                tf = self.term_freq[token][doc_id]
                score = self._score_bm25(tf, self.doc_lengths[doc_id], idf)
                doc_scores[doc_id] += score * self.documents[doc_id].weight
                if doc_id not in doc_snippets:
                    doc_snippets[doc_id] = self._make_snippet(self.documents[doc_id], query_tokens)
        # TF-IDF scoring
        tfidf_scores = self._tfidf_scores(query_tokens)
        for doc_id, tfidf_score in tfidf_scores.items():
            doc_scores[doc_id] += tfidf_score * 0.2  # blend factor
        top_docs = heapq.nlargest(limit, doc_scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = doc_snippets.get(doc_id, self._make_snippet(doc, query_tokens))
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def get_stats(self):
        with self.lock:
            stats = {
                'total_documents': self.total_docs,
                'average_document_length': self.avg_doc_length,
                'unique_terms': len(self.term_doc_freq),
                'tags': list(self.tags_index.keys())
            }
            return stats

    def _tokenize(self, text):
        tokens = [t.lower() for t in self._re_token.findall(text)]
        return tokens

    def _compute_idf(self, term):
        if term in self.idf_cache:
            return self.idf_cache[term]
        df = len(self.term_doc_freq.get(term, []))
        if df == 0:
            idf = 0.0
        else:
            idf = math.log(1 + (self.total_docs - df + 0.5) / (df + 0.5))
        self.idf_cache[term] = idf
        return idf

    def _score_bm25(self, tf, doc_len, idf):
        k1 = self._bm25_k1
        b = self._bm25_b
        denom = tf + k1 * (1 - b + b * doc_len / (self.avg_doc_length or 1))
        if denom == 0:
            return 0.0
        return idf * ((tf * (k1 + 1)) / denom)

    def _make_snippet(self, doc, query_tokens):
        content = doc.content
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_tokens]
        if positions:
            start = max(positions[0] - 10, 0)
            end = min(positions[0] + 10, len(tokens))
            snippet_tokens = tokens[start:end]
            snippet = ' '.join(snippet_tokens)
            for qt in query_tokens:
                snippet = re.sub(r'\b(%s)\b' % re.escape(qt), r'**\1**', snippet, flags=re.IGNORECASE)
            return snippet
        else:
            return content[:180] + ('...' if len(content) > 180 else '')

    def _tfidf_scores(self, query_tokens):
        scores = defaultdict(float)
        for term in query_tokens:
            idf = self._compute_idf(term)
            for doc_id in self.term_doc_freq.get(term, []):
                tf = self.term_freq[term][doc_id]
                norm_tf = tf / (self.doc_lengths[doc_id] or 1)
                scores[doc_id] += norm_tf * idf
        return scores

_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index():
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _seed_documents(_search_index_instance)
        return _search_index_instance

def _seed_documents(index):
    docs = [
        SearchDocument(
            doc_id="API675-001",
            title="API 675 Chemical Metering Pump Selection Guide",
            content="API 675 defines standards for reciprocating positive displacement pumps used in chemical injection. Selection criteria include flow rate, pressure, material compatibility, and stroke adjustment. Considerations for corrosion inhibitor, scale inhibitor, and demulsifier dosing are outlined.",
            tags=["API 675", "Pump Selection", "Chemical Injection"],
            weight=1.2
        ),
        SearchDocument(
            doc_id="INJ-QUILL-002",
            title="Injection Quill Design and Placement Best Practices",
            content="Injection quills ensure proper dispersion of chemicals in pipelines. Design features include check valves, atomizing tips, and corrosion-resistant materials. Placement should avoid dead zones and ensure turbulent flow for optimal mixing.",
            tags=["Injection Quill", "Design", "Placement"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="CORR-INHIB-003",
            title="Corrosion Inhibitor Film-Forming Amine Programs",
            content="Film-forming amines provide surface protection against corrosion in oilfield systems. Program design includes selection of amine type, dosing rate optimization, compatibility testing, and monitoring via iron counts and coupon analysis.",
            tags=["Corrosion Inhibitor", "Amine", "Film-Forming"],
            weight=1.15
        ),
        SearchDocument(
            doc_id="SCALE-SQZ-004",
            title="Scale Inhibitor Squeeze Treatment Design",
            content="Squeeze treatments involve injecting scale inhibitors into the formation to prevent mineral deposition. Key steps include chemical selection, squeeze volume calculation, adsorption/desorption modeling, and post-treatment monitoring.",
            tags=["Scale Inhibitor", "Squeeze Treatment", "Design"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="PARAFFIN-005",
            title="Paraffin Management: Crystal Modifiers vs Solvents",
            content="Paraffin deposition can be managed using crystal modifiers or solvents. Crystal modifiers alter wax crystallization, reducing deposition. Solvents dissolve existing paraffin. Selection depends on operational conditions, economics, and compatibility.",
            tags=["Paraffin", "Crystal Modifier", "Solvent"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="DEMUL-BOTTLE-006",
            title="Demulsifier Optimization via Bottle Testing",
            content="Bottle testing is used to optimize demulsifier selection and dosage. Procedures include emulsion preparation, demulsifier addition, mixing, and separation analysis. Results guide field application and dosage adjustment.",
            tags=["Demulsifier", "Bottle Testing", "Optimization"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="H2S-SCAV-007",
            title="H2S Scavenger Systems: Triazine vs Solid-Based",
            content="H2S scavenging can be achieved using triazine-based liquid systems or solid-based scavengers. Triazine offers rapid reaction but may form byproducts. Solid scavengers provide sustained removal but require periodic replacement.",
            tags=["H2S Scavenger", "Triazine", "Solid-Based"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="BIOCIDE-008",
            title="Biocide Programs for Microbiological Control",
            content="Biocide selection and dosing are critical for controlling microbiological activity in oilfield systems. Program design includes biocide type, dosing frequency, compatibility, and monitoring via ATP and culture tests.",
            tags=["Biocide", "Microbiological Control", "Program"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="CHEM-DOSE-009",
            title="Chemical Dosing Rate Optimization via MEC Testing",
            content="Minimum Effective Concentration (MEC) testing determines optimal chemical dosing rates. Procedures involve laboratory testing, field validation, and adjustment based on performance metrics such as corrosion rate and scale inhibition.",
            tags=["Chemical Dosing", "MEC Testing", "Optimization"],
            weight=1.2
        ),
        SearchDocument(
            doc_id="COMPAT-010",
            title="Chemical Compatibility Testing Protocol",
            content="Compatibility testing ensures injected chemicals do not react adversely. Protocols include jar testing, phase separation analysis, and monitoring for precipitate formation. Results inform chemical selection and injection sequencing.",
            tags=["Chemical Compatibility", "Testing", "Protocol"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="INVENTORY-011",
            title="Chemical Inventory and Tote Farm Management",
            content="Effective inventory management includes tracking chemical usage, storage conditions, and tote farm layout. Automated systems improve accuracy and reduce risk of stockouts or overstocking. Safety and compliance are critical.",
            tags=["Inventory", "Tote Farm", "Management"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="SDS-GHS-012",
            title="Safety Data Sheet (SDS) and GHS Compliance",
            content="SDS documentation and GHS labeling are required for chemical handling. Compliance ensures worker safety, environmental protection, and regulatory adherence. Procedures include document review, training, and audit.",
            tags=["SDS", "GHS", "Compliance"],
            weight=1.2
        ),
        SearchDocument(
            doc_id="API675-MATERIAL-013",
            title="API 675 Pump Material Selection for Corrosive Service",
            content="Material selection for API 675 pumps depends on chemical compatibility, corrosion resistance, and mechanical properties. Common materials include stainless steel, Hastelloy, and PTFE. Selection guides ensure long-term reliability.",
            tags=["API 675", "Material Selection", "Corrosive Service"],
            weight=1.15
        ),
        SearchDocument(
            doc_id="QUILL-CHECK-014",
            title="Injection Quill Check Valve Functionality",
            content="Check valves in injection quills prevent backflow and contamination. Selection criteria include cracking pressure, material compatibility, and maintenance requirements. Regular inspection ensures reliable operation.",
            tags=["Injection Quill", "Check Valve", "Functionality"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="CORR-MONITOR-015",
            title="Corrosion Monitoring Techniques for Chemical Programs",
            content="Corrosion monitoring includes coupon analysis, electrical resistance probes, and iron count measurements. Data informs chemical program adjustments and effectiveness evaluation.",
            tags=["Corrosion Monitoring", "Chemical Program", "Techniques"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="SCALE-ADSORB-016",
            title="Scale Inhibitor Adsorption/Desorption Modeling",
            content="Adsorption and desorption models predict scale inhibitor retention and release in squeeze treatments. Parameters include formation mineralogy, inhibitor chemistry, and injection volume.",
            tags=["Scale Inhibitor", "Adsorption", "Desorption"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="PARAFFIN-FIELD-017",
            title="Field Application of Paraffin Crystal Modifiers",
            content="Crystal modifiers are injected to prevent paraffin deposition in pipelines. Field application involves dosage determination, injection point selection, and performance monitoring.",
            tags=["Paraffin", "Crystal Modifier", "Field Application"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="DEMUL-SEPARATION-018",
            title="Demulsifier Separation Analysis in Bottle Testing",
            content="Separation analysis evaluates demulsifier effectiveness in bottle tests. Metrics include water clarity, oil separation, and emulsion stability. Results guide chemical selection and dosage.",
            tags=["Demulsifier", "Separation Analysis", "Bottle Testing"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="H2S-BYPRODUCT-019",
            title="Triazine Byproduct Management in H2S Scavenging",
            content="Triazine-based scavengers can produce byproducts such as thiadiazine. Management strategies include monitoring, alternative scavenger selection, and process optimization.",
            tags=["H2S Scavenger", "Triazine", "Byproduct Management"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="BIOCIDE-ATP-020",
            title="ATP Testing for Biocide Program Effectiveness",
            content="ATP testing measures microbiological activity to assess biocide effectiveness. Procedures include sample collection, reagent addition, and luminescence measurement.",
            tags=["Biocide", "ATP Testing", "Effectiveness"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="CHEM-ADJUST-021",
            title="Field Adjustment of Chemical Dosing Rates",
            content="Field adjustment of dosing rates involves performance monitoring, sample analysis, and operational feedback. Adjustments ensure optimal protection and cost efficiency.",
            tags=["Chemical Dosing", "Field Adjustment", "Optimization"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="COMPAT-SEQUENCE-022",
            title="Chemical Injection Sequencing for Compatibility",
            content="Injection sequencing prevents adverse chemical reactions. Guidelines include order of injection, flushing procedures, and compatibility testing.",
            tags=["Chemical Compatibility", "Injection Sequencing", "Guidelines"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="INVENTORY-AUTO-023",
            title="Automated Chemical Inventory Tracking Systems",
            content="Automated tracking systems use RFID, barcodes, and sensors to monitor chemical inventory. Benefits include improved accuracy, real-time data, and reduced manual errors.",
            tags=["Inventory", "Automated Tracking", "Systems"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="SDS-TRAINING-024",
            title="SDS Training and Audit Procedures",
            content="SDS training ensures workers understand chemical hazards and safe handling. Audit procedures verify compliance and document accuracy.",
            tags=["SDS", "Training", "Audit"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="API675-STROKE-025",
            title="API 675 Pump Stroke Adjustment Methods",
            content="Stroke adjustment allows fine-tuning of pump flow rates. Methods include manual, electronic, and automatic adjustment. Proper calibration ensures accurate chemical dosing.",
            tags=["API 675", "Stroke Adjustment", "Pump"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="QUILL-MATERIAL-026",
            title="Injection Quill Material Selection for Harsh Environments",
            content="Material selection for injection quills depends on chemical compatibility and mechanical strength. Options include stainless steel, Hastelloy, and PTFE.",
            tags=["Injection Quill", "Material Selection", "Harsh Environment"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="CORR-COUPON-027",
            title="Corrosion Coupon Analysis for Program Validation",
            content="Corrosion coupons provide direct measurement of metal loss. Analysis includes weight loss, pit depth, and surface inspection. Results validate chemical program effectiveness.",
            tags=["Corrosion Coupon", "Analysis", "Validation"],
            weight=1.1
        ),
        SearchDocument(
            doc_id="SCALE-MONITOR-028",
            title="Scale Monitoring Techniques in Squeeze Treatments",
            content="Scale monitoring includes water analysis, wellhead sampling, and downhole sensors. Data informs squeeze treatment effectiveness and re-treatment scheduling.",
            tags=["Scale Monitoring", "Squeeze Treatment", "Techniques"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="PARAFFIN-ECON-029",
            title="Economic Evaluation of Paraffin Management Strategies",
            content="Economic evaluation compares costs and benefits of crystal modifiers and solvents. Factors include chemical cost, downtime reduction, and maintenance savings.",
            tags=["Paraffin", "Economic Evaluation", "Management"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="DEMUL-FIELD-030",
            title="Field Implementation of Demulsifier Programs",
            content="Field implementation involves dosage determination, injection point selection, and performance monitoring. Adjustments are based on separation analysis and operational feedback.",
            tags=["Demulsifier", "Field Implementation", "Program"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="H2S-SOLID-031",
            title="Solid-Based H2S Scavenger Replacement Scheduling",
            content="Solid-based scavengers require periodic replacement. Scheduling is based on H2S load, scavenger capacity, and operational data.",
            tags=["H2S Scavenger", "Solid-Based", "Replacement"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="BIOCIDE-COMPAT-032",
            title="Biocide Compatibility with Other Oilfield Chemicals",
            content="Compatibility testing ensures biocides do not react adversely with other chemicals. Procedures include jar testing, phase separation, and monitoring for precipitate formation.",
            tags=["Biocide", "Compatibility", "Oilfield Chemicals"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="CHEM-OPTIM-033",
            title="Chemical Dosing Optimization for Cost Efficiency",
            content="Optimization involves balancing protection and cost. Techniques include MEC testing, field adjustment, and performance monitoring.",
            tags=["Chemical Dosing", "Optimization", "Cost Efficiency"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="COMPAT-PRECIP-034",
            title="Precipitate Formation in Chemical Compatibility Testing",
            content="Precipitate formation indicates incompatibility. Testing protocols include visual inspection, filtration, and chemical analysis.",
            tags=["Chemical Compatibility", "Precipitate Formation", "Testing"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="INVENTORY-STORAGE-035",
            title="Chemical Storage Conditions for Tote Farms",
            content="Proper storage conditions include temperature control, spill containment, and segregation of incompatible chemicals. Compliance reduces risk and ensures chemical integrity.",
            tags=["Inventory", "Storage", "Tote Farm"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="SDS-ENV-036",
            title="Environmental Compliance in SDS Documentation",
            content="SDS documentation includes environmental hazard information. Compliance ensures regulatory adherence and environmental protection.",
            tags=["SDS", "Environmental Compliance", "Documentation"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="API675-FLOW-037",
            title="API 675 Pump Flow Rate Calculation",
            content="Flow rate calculation involves stroke length, pump speed, and displacement volume. Accurate calculation ensures proper chemical dosing.",
            tags=["API 675", "Flow Rate", "Calculation"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="QUILL-TURBULENCE-038",
            title="Injection Quill Placement for Turbulent Mixing",
            content="Placement in turbulent flow zones ensures optimal chemical dispersion. Guidelines include avoiding dead zones and ensuring adequate velocity.",
            tags=["Injection Quill", "Placement", "Turbulent Mixing"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="CORR-IRON-039",
            title="Iron Count Monitoring for Corrosion Control",
            content="Iron count monitoring provides indirect measurement of corrosion rates. Data informs program adjustments and chemical effectiveness.",
            tags=["Corrosion Monitoring", "Iron Count", "Control"],
            weight=1.05
        ),
        SearchDocument(
            doc_id="SCALE-RETREAT-040",
            title="Re-Treatment Scheduling for Scale Inhibitor Squeeze",
            content="Re-treatment scheduling is based on scale monitoring data, inhibitor retention, and well performance.",
            tags=["Scale Inhibitor", "Re-Treatment", "Scheduling"],
            weight=1.05
        ),
    ]
    for doc in docs:
        index.add_document(doc)