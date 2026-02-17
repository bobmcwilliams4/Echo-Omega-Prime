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
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents = {}
        self.doc_freqs = defaultdict(int)
        self.term_doc_freqs = defaultdict(lambda: defaultdict(int))
        self.doc_lengths = {}
        self.avg_doc_length = 0.0
        self.N = 0
        self.lock = threading.Lock()
        self._idf_cache = {}
        self._tfidf_cache = {}

    def _tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())

    def add_document(self, doc):
        with self.lock:
            if doc.id in self.documents:
                return
            tokens = self._tokenize(doc.content)
            tf = Counter(tokens)
            self.documents[doc.id] = doc
            self.doc_lengths[doc.id] = len(tokens)
            for term, freq in tf.items():
                self.term_doc_freqs[term][doc.id] = freq
            for term in set(tokens):
                self.doc_freqs[term] += 1
            self.N += 1
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.N if self.N else 0.0
            self._idf_cache.clear()
            self._tfidf_cache.clear()

    def _compute_idf(self, term):
        if term in self._idf_cache:
            return self._idf_cache[term]
        df = self.doc_freqs.get(term, 0)
        idf = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        self._idf_cache[term] = idf
        return idf

    def _score_bm25(self, query_terms, doc_id):
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = self.term_doc_freqs
        for term in query_terms:
            if doc_id not in tf[term]:
                continue
            f = tf[term][doc_id]
            idf = self._compute_idf(term)
            denom = f + self.k1 * (1 - self.b + self.b * doc_len / (self.avg_doc_length or 1))
            score += idf * (f * (self.k1 + 1)) / (denom or 1)
        return score * doc.weight

    def _score_tfidf(self, query_terms, doc_id):
        score = 0.0
        doc = self.documents[doc_id]
        doc_len = self.doc_lengths[doc_id]
        tf = self.term_doc_freqs
        for term in query_terms:
            if doc_id not in tf[term]:
                continue
            f = tf[term][doc_id]
            tf_norm = f / (doc_len or 1)
            idf = self._compute_idf(term)
            score += tf_norm * idf
        return score * doc.weight

    def search(self, query, limit=10, method='bm25'):
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        doc_scores = {}
        for doc_id in self.documents:
            if method == 'bm25':
                score = self._score_bm25(query_terms, doc_id)
            else:
                score = self._score_tfidf(query_terms, doc_id)
            if score > 0:
                doc_scores[doc_id] = score
        top_docs = heapq.nlargest(limit, doc_scores.items(), key=lambda x: x[1])
        results = []
        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._make_snippet(doc.content, query_terms)
            results.append(SearchResult(doc_id, score, doc.title, snippet))
        return results

    def _make_snippet(self, content, query_terms, window=30):
        tokens = self._tokenize(content)
        positions = [i for i, t in enumerate(tokens) if t in query_terms]
        if not positions:
            return ' '.join(tokens[:window]) + ('...' if len(tokens) > window else '')
        start = max(positions[0] - window // 2, 0)
        end = min(start + window, len(tokens))
        snippet = tokens[start:end]
        return '...' + ' '.join(snippet) + '...'

    def get_stats(self):
        return {
            'num_documents': self.N,
            'avg_doc_length': self.avg_doc_length,
            'vocab_size': len(self.doc_freqs)
        }

# Singleton factory
_search_index_instance = None
_search_index_lock = threading.Lock()

def get_search_index():
    global _search_index_instance
    with _search_index_lock:
        if _search_index_instance is None:
            _search_index_instance = SearchIndex()
            _preseed_documents(_search_index_instance)
        return _search_index_instance

def _preseed_documents(index):
    docs = [
        SearchDocument(
            1,
            "Sepsis-3 Criteria and qSOFA Screening",
            "Sepsis is defined as life-threatening organ dysfunction caused by a dysregulated host response to infection. The Sepsis-3 criteria recommend using the Sequential Organ Failure Assessment (SOFA) score. The quick SOFA (qSOFA) screening tool uses three criteria: altered mentation, systolic blood pressure ≤100 mmHg, and respiratory rate ≥22/min. Two or more qSOFA points suggest high risk of poor outcome.",
            ["sepsis", "qSOFA", "SOFA", "criteria"],
            1.0
        ),
        SearchDocument(
            2,
            "Empiric Antibiotic Selection for Sepsis",
            "Empiric antibiotic therapy for sepsis should be broad-spectrum and initiated as soon as possible. Consider local resistance patterns, suspected source, and patient allergies. Double coverage for Pseudomonas or MRSA may be indicated in certain cases. De-escalate therapy based on culture results.",
            ["sepsis", "antibiotics", "empiric", "therapy"],
            1.0
        ),
        SearchDocument(
            3,
            "Blood Culture Interpretation: True Positive vs Contaminant",
            "Blood cultures are essential in diagnosing sepsis. True positives are indicated by growth of typical pathogens in multiple sets. Common contaminants include coagulase-negative staphylococci, Corynebacterium, and Bacillus species. Repeat cultures and clinical correlation are important.",
            ["blood culture", "contaminant", "diagnosis"],
            1.0
        ),
        SearchDocument(
            4,
            "MRSA Management and Vancomycin Dosing",
            "Methicillin-resistant Staphylococcus aureus (MRSA) infections require vancomycin or alternative agents. Vancomycin dosing should be based on actual body weight and renal function. Monitor trough levels to ensure efficacy and minimize toxicity. Consider alternative agents if vancomycin MIC ≥2 mg/L.",
            ["MRSA", "vancomycin", "dosing", "antibiotic"],
            1.0
        ),
        SearchDocument(
            5,
            "C. difficile Infection Diagnosis and Management",
            "Clostridioides difficile infection (CDI) is diagnosed by detecting toxin or PCR in stool. Management includes stopping inciting antibiotics, starting oral vancomycin or fidaxomicin, and implementing infection control measures. Recurrence may require prolonged or pulsed therapy.",
            ["C. difficile", "CDI", "infection", "management"],
            1.0
        ),
        SearchDocument(
            6,
            "Antimicrobial Stewardship Program Core Elements",
            "Effective antimicrobial stewardship programs (ASP) include leadership commitment, accountability, drug expertise, action, tracking, reporting, and education. ASPs aim to optimize antibiotic use and reduce resistance.",
            ["antimicrobial stewardship", "ASP", "antibiotic", "resistance"],
            1.0
        ),
        SearchDocument(
            7,
            "Procalcitonin-Guided Antibiotic Therapy",
            "Procalcitonin is a biomarker that can help guide antibiotic therapy in sepsis and lower respiratory tract infections. Low or decreasing procalcitonin levels may support early discontinuation of antibiotics, reducing unnecessary exposure.",
            ["procalcitonin", "antibiotic", "biomarker", "therapy"],
            1.0
        ),
        SearchDocument(
            8,
            "HIV Treatment: ART Initiation and Regimens",
            "Antiretroviral therapy (ART) should be initiated in all patients with HIV regardless of CD4 count. Preferred regimens include integrase inhibitor-based combinations. Monitor for drug interactions and resistance.",
            ["HIV", "ART", "antiretroviral", "therapy"],
            1.0
        ),
        SearchDocument(
            9,
            "Tuberculosis Diagnosis and RIPE Therapy",
            "Tuberculosis (TB) is diagnosed by sputum smear, culture, and nucleic acid amplification tests. Initial therapy includes rifampin, isoniazid, pyrazinamide, and ethambutol (RIPE). Monitor for drug toxicity and adherence.",
            ["tuberculosis", "RIPE", "diagnosis", "therapy"],
            1.0
        ),
        SearchDocument(
            10,
            "Carbapenem-Resistant Enterobacterales (CRE) Management",
            "CRE infections are challenging due to limited treatment options. Consider ceftazidime-avibactam, meropenem-vaborbactam, or polymyxins. Infection control measures are critical to prevent spread.",
            ["CRE", "carbapenem-resistant", "Enterobacterales", "management"],
            1.0
        ),
        SearchDocument(
            11,
            "Healthcare-Associated Infections (HAI) Prevention",
            "Preventing HAIs involves hand hygiene, environmental cleaning, device care, and antimicrobial stewardship. Surveillance and feedback are key components. Bundle approaches reduce device-associated infections.",
            ["HAI", "prevention", "infection control"],
            1.0
        ),
        SearchDocument(
            12,
            "Febrile Neutropenia Management",
            "Febrile neutropenia is an oncologic emergency. Start empiric broad-spectrum antibiotics immediately. Risk stratification guides outpatient vs inpatient management. Monitor for complications and adjust therapy based on cultures.",
            ["febrile neutropenia", "management", "antibiotics"],
            1.0
        ),
        SearchDocument(
            13,
            "Antibiotic Dosing in Renal Impairment",
            "Renal impairment affects antibiotic pharmacokinetics. Dose adjustments are required for many agents. Monitor renal function and drug levels where appropriate. Consult dosing references for specific recommendations.",
            ["antibiotic", "dosing", "renal impairment"],
            1.0
        ),
        SearchDocument(
            14,
            "Infection Control: Isolation Precautions",
            "Isolation precautions include standard, contact, droplet, and airborne precautions. Use appropriate personal protective equipment (PPE) and signage. Cohorting and dedicated equipment reduce transmission.",
            ["infection control", "isolation", "precautions"],
            1.0
        ),
        SearchDocument(
            15,
            "Sepsis Resuscitation and Early Goal-Directed Therapy",
            "Early resuscitation in sepsis includes fluid administration, vasopressors for hypotension, and lactate monitoring. Early goal-directed therapy improves outcomes by targeting perfusion parameters.",
            ["sepsis", "resuscitation", "goal-directed therapy"],
            1.0
        ),
        SearchDocument(
            16,
            "De-escalation of Antibiotic Therapy in Sepsis",
            "De-escalation involves narrowing antibiotic spectrum based on culture results and clinical response. This reduces resistance and adverse effects. Daily review of antibiotic necessity is recommended.",
            ["antibiotic", "de-escalation", "sepsis"],
            1.0
        ),
        SearchDocument(
            17,
            "Vancomycin Therapeutic Drug Monitoring",
            "Monitor vancomycin trough levels to optimize efficacy and minimize nephrotoxicity. Target troughs of 15-20 mg/L for serious infections. Adjust dosing based on renal function and levels.",
            ["vancomycin", "monitoring", "dosing"],
            1.0
        ),
        SearchDocument(
            18,
            "Clostridioides difficile Infection Prevention",
            "Preventing C. difficile infection includes antimicrobial stewardship, hand hygiene with soap and water, environmental cleaning with sporicidal agents, and contact precautions.",
            ["C. difficile", "prevention", "infection control"],
            1.0
        ),
        SearchDocument(
            19,
            "HIV Drug Resistance and Genotype Testing",
            "Genotype resistance testing is recommended before starting ART. Resistance mutations may affect regimen choice. Adherence is crucial to prevent resistance.",
            ["HIV", "resistance", "genotype", "ART"],
            1.0
        ),
        SearchDocument(
            20,
            "Latent Tuberculosis Infection (LTBI) Treatment",
            "LTBI is treated with isoniazid or rifampin-based regimens. Rule out active TB before starting therapy. Monitor for hepatotoxicity.",
            ["tuberculosis", "LTBI", "treatment"],
            1.0
        ),
        SearchDocument(
            21,
            "CRE Infection Control Measures",
            "Strict infection control is required for CRE, including contact precautions, screening, and cohorting. Environmental cleaning and hand hygiene are essential.",
            ["CRE", "infection control", "precautions"],
            1.0
        ),
        SearchDocument(
            22,
            "Central Line-Associated Bloodstream Infection (CLABSI) Prevention",
            "CLABSI prevention bundles include hand hygiene, maximal sterile barrier precautions, chlorhexidine skin antisepsis, and prompt removal of unnecessary lines.",
            ["CLABSI", "prevention", "bloodstream infection"],
            1.0
        ),
        SearchDocument(
            23,
            "Antibiotic Stewardship in the ICU",
            "ICU stewardship focuses on appropriate empiric therapy, timely de-escalation, and minimizing unnecessary antibiotic use. Multidisciplinary teams improve outcomes.",
            ["antibiotic stewardship", "ICU", "antibiotic"],
            1.0
        ),
        SearchDocument(
            24,
            "Contact Precautions for Multidrug-Resistant Organisms (MDROs)",
            "Contact precautions, including gown and glove use, are recommended for patients with MDROs such as MRSA, VRE, and CRE. Dedicated equipment and environmental cleaning reduce transmission.",
            ["contact precautions", "MDRO", "MRSA", "CRE"],
            1.0
        ),
        SearchDocument(
            25,
            "Procalcitonin Interpretation in Sepsis",
            "High procalcitonin levels suggest bacterial infection and may support sepsis diagnosis. Serial measurements can guide duration of antibiotic therapy.",
            ["procalcitonin", "sepsis", "antibiotic"],
            1.0
        ),
        SearchDocument(
            26,
            "Fever Workup in Neutropenic Patients",
            "Neutropenic fever requires prompt evaluation for infection sources, including blood cultures, chest imaging, and urinalysis. Empiric antibiotics should not be delayed.",
            ["neutropenia", "fever", "workup", "antibiotics"],
            1.0
        ),
        SearchDocument(
            27,
            "Droplet and Airborne Precautions in Infection Control",
            "Droplet precautions are used for pathogens spread by respiratory droplets, such as influenza. Airborne precautions are required for tuberculosis and measles. Use N95 respirators for airborne pathogens.",
            ["droplet precautions", "airborne precautions", "infection control"],
            1.0
        ),
        SearchDocument(
            28,
            "Antibiotic Allergies and Cross-Reactivity",
            "Assess reported antibiotic allergies carefully. Cross-reactivity between penicillins and cephalosporins is low. Skin testing may clarify true allergy.",
            ["antibiotic", "allergy", "cross-reactivity"],
            1.0
        ),
        SearchDocument(
            29,
            "Hand Hygiene in Healthcare Settings",
            "Hand hygiene is the single most important measure to prevent healthcare-associated infections. Use alcohol-based hand rubs or soap and water. Adherence to hand hygiene protocols reduces infection rates.",
            ["hand hygiene", "infection prevention", "HAI"],
            1.0
        ),
        SearchDocument(
            30,
            "Antimicrobial De-escalation Strategies",
            "Antimicrobial de-escalation involves narrowing therapy based on culture data and clinical improvement. This reduces resistance and adverse events.",
            ["antimicrobial", "de-escalation", "antibiotic"],
            1.0
        ),
        SearchDocument(
            31,
            "Environmental Cleaning in Infection Control",
            "Routine and terminal cleaning of patient care areas reduces transmission of pathogens. Use appropriate disinfectants for C. difficile and MDROs.",
            ["environmental cleaning", "infection control", "C. difficile"],
            1.0
        ),
        SearchDocument(
            32,
            "Antibiotic Pharmacokinetics and Pharmacodynamics",
            "Understanding PK/PD relationships helps optimize antibiotic dosing. Time-dependent vs concentration-dependent killing influences dosing strategies.",
            ["pharmacokinetics", "pharmacodynamics", "antibiotic"],
            1.0
        ),
        SearchDocument(
            33,
            "Rapid Diagnostic Tests in Infectious Diseases",
            "Rapid diagnostics, including PCR and antigen tests, enable early identification of pathogens and guide targeted therapy.",
            ["rapid diagnostics", "PCR", "infectious diseases"],
            1.0
        ),
        SearchDocument(
            34,
            "VRE (Vancomycin-Resistant Enterococcus) Management",
            "VRE infections require alternative agents such as linezolid or daptomycin. Infection control measures are essential to prevent transmission.",
            ["VRE", "vancomycin-resistant", "Enterococcus", "management"],
            1.0
        ),
        SearchDocument(
            35,
            "Antibiotic Stewardship Metrics and Outcomes",
            "Metrics for stewardship programs include antibiotic utilization, resistance rates, and clinical outcomes. Regular feedback supports improvement.",
            ["stewardship", "metrics", "outcomes", "antibiotic"],
            1.0
        ),
    ]
    for doc in docs:
        index.add_document(doc)