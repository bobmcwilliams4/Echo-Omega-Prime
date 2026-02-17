import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

"""
MED02 Pharmacology Intelligence Engine
Port: 9092
Version: 1.0.0

Comprehensive pharmaceutical knowledge covering pharmacokinetics, pharmacodynamics,
drug interactions, therapeutic classes, adverse effects, and clinical pharmacology.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from loguru import logger
import hashlib
import json
from datetime import datetime
from dataclasses import dataclass, asdict
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

APP = FastAPI(title="MED02 Pharmacology Engine", version="1.0.0")
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.add(
    "pharmacology_engine_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)

# ============================================================================
# MODELS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    answer: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    reasoning_chain: List[str]
    determinism_hash: str
    metadata: Dict[str, Any]

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    clinical_considerations: List[str]
    adverse_effects: List[str]
    contraindications: List[str]

# ============================================================================
# DOCTRINE CACHE - PHARMACOLOGY KNOWLEDGE
# ============================================================================

DOCTRINE_CACHE = {
    "PHARMACOKINETICS_ABSORPTION": DoctrineBlock(
        topic="Drug Absorption Mechanisms",
        keywords=["absorption", "bioavailability", "first-pass", "oral", "IV", "bioequivalence", "Cmax", "Tmax"],
        conclusion_template=[
            "Drug absorption is governed by physicochemical properties and route of administration",
            "Bioavailability represents fraction of dose reaching systemic circulation",
            "First-pass metabolism significantly reduces oral bioavailability for some drugs"
        ],
        reasoning_framework="""
        Absorption analysis requires:
        1. Route assessment (oral, IV, IM, SC, transdermal, sublingual)
        2. Physicochemical factors (lipophilicity, molecular weight, ionization)
        3. Gastrointestinal factors (pH, motility, food effects, P-gp efflux)
        4. First-pass metabolism (hepatic extraction ratio)
        5. Bioavailability calculation (AUCoral/AUCIV)
        6. Food-drug interactions affecting absorption
        7. Modified release formulations impact
        """,
        key_factors=[
            "Lipid solubility (log P) determines membrane permeability",
            "Henderson-Hasselbalch equation predicts ionization state",
            "P-glycoprotein efflux reduces absorption of substrates",
            "First-pass effect ranges from 0% (IV) to >90% (high extraction drugs)",
            "Food increases absorption of lipophilic drugs, decreases others",
            "Gastric pH affects weak acid/base ionization and dissolution"
        ],
        primary_authority=[
            "Goodman & Gilman's Pharmacological Basis of Therapeutics",
            "FDA Bioavailability and Bioequivalence Studies Guidance",
            "Biopharmaceutics Classification System (BCS)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Take levothyroxine on empty stomach (food reduces absorption 40%)",
            "Fluoroquinolones chelate with divalent cations (separate by 2-4 hours)",
            "Sublingual nitroglycerin bypasses first-pass metabolism",
            "Enteric coating prevents gastric degradation of acid-labile drugs"
        ],
        adverse_effects=[
            "Gastric irritation from NSAIDs (direct mucosal damage)",
            "Esophageal ulceration from bisphosphonates if not taken upright"
        ],
        contraindications=[
            "Oral route contraindicated in severe vomiting or malabsorption"
        ]
    ),

    "PHARMACOKINETICS_DISTRIBUTION": DoctrineBlock(
        topic="Volume of Distribution and Tissue Binding",
        keywords=["Vd", "volume distribution", "protein binding", "albumin", "tissue penetration", "BBB", "placenta"],
        conclusion_template=[
            "Volume of distribution reflects extent of drug distribution into tissues",
            "Plasma protein binding affects free drug concentration and distribution",
            "Barriers (BBB, placenta) restrict distribution of hydrophilic/large molecules"
        ],
        reasoning_framework="""
        Distribution analysis considers:
        1. Volume of distribution calculation (Vd = dose/C0)
        2. Protein binding (albumin for acids, α1-AGP for bases)
        3. Free vs bound drug (only free drug is active)
        4. Tissue binding and sequestration
        5. Barrier penetration (blood-brain, placental, blood-testis)
        6. Distribution phase vs elimination phase
        7. Pathophysiological effects (hypoalbuminemia, inflammation)
        """,
        key_factors=[
            "Vd <0.1 L/kg indicates plasma compartment confinement",
            "Vd >1 L/kg indicates extensive tissue distribution",
            "Only unbound drug crosses membranes and exerts effects",
            "Hypoalbuminemia increases free fraction of highly bound drugs",
            "Lipophilic drugs cross BBB; hydrophilic drugs do not",
            "Displacement interactions clinically significant only for highly bound, narrow therapeutic index drugs"
        ],
        primary_authority=[
            "Rowland & Tozer Clinical Pharmacokinetics",
            "Therapeutic Drug Monitoring Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Warfarin 99% protein-bound; displacement increases bleeding risk",
            "Phenytoin exhibits saturable protein binding (nonlinear kinetics)",
            "Digoxin Vd 7 L/kg; extensive tissue binding requires loading dose",
            "CNS infections increase BBB permeability to antibiotics"
        ],
        adverse_effects=[
            "Increased free phenytoin in renal failure causes toxicity despite 'therapeutic' total level"
        ],
        contraindications=[
            "Avoid highly protein-bound drugs in severe hypoalbuminemia without dose adjustment"
        ]
    ),

    "PHARMACOKINETICS_METABOLISM": DoctrineBlock(
        topic="Hepatic Drug Metabolism and CYP450 System",
        keywords=["metabolism", "CYP450", "phase I", "phase II", "glucuronidation", "induction", "inhibition", "prodrug"],
        conclusion_template=[
            "Hepatic metabolism via CYP450 enzymes is primary clearance mechanism for lipophilic drugs",
            "CYP induction/inhibition causes drug-drug interactions affecting efficacy and toxicity",
            "Genetic polymorphisms (pharmacogenomics) alter metabolic capacity"
        ],
        reasoning_framework="""
        Metabolism evaluation requires:
        1. Phase I reactions (oxidation, reduction, hydrolysis via CYP450)
        2. Phase II conjugation (glucuronidation, sulfation, acetylation)
        3. CYP450 isoenzyme identification (1A2, 2C9, 2C19, 2D6, 3A4)
        4. Induction effects (increases metabolism, reduces efficacy)
        5. Inhibition effects (decreases metabolism, increases toxicity)
        6. Genetic polymorphisms (poor/extensive/ultra-rapid metabolizers)
        7. Hepatic disease impact (Child-Pugh score)
        8. Prodrug activation considerations
        """,
        key_factors=[
            "CYP3A4 metabolizes 50% of drugs; highly inducible/inhibitable",
            "CYP2D6 polymorphic (7% Caucasians poor metabolizers)",
            "Grapefruit juice irreversibly inhibits intestinal CYP3A4",
            "Rifampin potent CYP3A4 inducer (onset 7-10 days, offset 2-3 weeks)",
            "Azole antifungals potent CYP3A4 inhibitors",
            "First-pass metabolism occurs before systemic circulation"
        ],
        primary_authority=[
            "FDA Drug Interaction Studies Guidance",
            "PharmGKB Pharmacogenomics Database",
            "Flockhart CYP450 Drug Interaction Table"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Warfarin/rifampin: rifampin induces CYP2C9, increases warfarin dose requirement 3-5x",
            "Simvastatin/clarithromycin: CYP3A4 inhibition causes rhabdomyolysis risk",
            "Codeine ineffective in CYP2D6 poor metabolizers (cannot convert to morphine)",
            "Clopidogrel ineffective in CYP2C19 poor metabolizers (cannot activate prodrug)"
        ],
        adverse_effects=[
            "CYP3A4 inhibition increases statin levels → rhabdomyolysis",
            "CYP2D6 ultra-rapid metabolism of codeine → morphine toxicity in infants via breast milk"
        ],
        contraindications=[
            "Avoid simvastatin/gemfibrozil (CYP3A4 inhibition + OATP inhibition)"
        ]
    ),

    "PHARMACOKINETICS_EXCRETION": DoctrineBlock(
        topic="Renal and Biliary Elimination",
        keywords=["clearance", "excretion", "GFR", "creatinine clearance", "renal", "biliary", "half-life", "steady-state"],
        conclusion_template=[
            "Renal clearance via glomerular filtration, tubular secretion, and reabsorption",
            "Clearance determines dosing rate required to maintain steady-state concentration",
            "Half-life determines dosing interval and time to steady-state (4-5 half-lives)"
        ],
        reasoning_framework="""
        Elimination analysis includes:
        1. Clearance calculation (CL = Vd × ke)
        2. Half-life determination (t½ = 0.693/ke)
        3. Renal clearance mechanisms (GFR, secretion, reabsorption)
        4. Creatinine clearance estimation (Cockcroft-Gault)
        5. Dose adjustment in renal impairment
        6. Biliary excretion and enterohepatic recirculation
        7. Steady-state achievement (5 half-lives)
        8. Loading dose calculation for rapid onset
        """,
        key_factors=[
            "Clearance defines maintenance dose; Vd defines loading dose",
            "Aminoglycosides primarily renally eliminated; require dose adjustment",
            "Probenecid blocks tubular secretion (increases penicillin levels)",
            "Alkalinization of urine increases excretion of weak acids (aspirin)",
            "Digoxin half-life 36 hours; takes 7 days to reach steady-state",
            "Hemodialysis removes drugs with low Vd, low protein binding, small molecular weight"
        ],
        primary_authority=[
            "Kidney Disease: Improving Global Outcomes (KDIGO) Guidelines",
            "Nephrology Pharmacotherapy Textbooks"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Vancomycin dosing based on CrCl and target trough 10-20 mcg/mL",
            "Metformin contraindicated if CrCl <30 mL/min (lactic acidosis risk)",
            "Digoxin loading dose 0.5-1 mg IV over 24h for rapid digitalization",
            "Lithium narrow therapeutic index; requires monitoring in renal impairment"
        ],
        adverse_effects=[
            "Aminoglycoside accumulation in renal failure → nephrotoxicity, ototoxicity"
        ],
        contraindications=[
            "Avoid NSAIDs in severe renal impairment (CrCl <30)"
        ]
    ),

    "PHARMACODYNAMICS_DOSE_RESPONSE": DoctrineBlock(
        topic="Dose-Response Relationships and Therapeutic Window",
        keywords=["dose-response", "ED50", "EC50", "TD50", "therapeutic index", "Emax", "efficacy", "potency"],
        conclusion_template=[
            "Dose-response curve characterizes relationship between drug dose and pharmacologic effect",
            "Potency (EC50) differs from efficacy (Emax); efficacy more clinically relevant",
            "Therapeutic index (TD50/ED50) indicates safety margin"
        ],
        reasoning_framework="""
        Dose-response evaluation:
        1. Graded vs quantal dose-response curves
        2. EC50 (potency) - dose producing 50% maximal effect
        3. Emax (efficacy) - maximal achievable effect
        4. Slope - steepness indicates dose-response precision
        5. Therapeutic index calculation (TD50/ED50 or LD50/ED50)
        6. Therapeutic window - range between minimum effective and toxic concentrations
        7. Margin of safety - distance between therapeutic and toxic doses
        """,
        key_factors=[
            "Potency determines dose size; efficacy determines maximal effect",
            "Partial agonist has Emax < full agonist regardless of dose",
            "Warfarin narrow therapeutic index (2-3); requires monitoring",
            "Penicillin wide therapeutic index (>100); safe even at high doses",
            "Steep dose-response curve indicates small dose changes produce large effect changes",
            "Individual variability (genetics, disease) shifts curves"
        ],
        primary_authority=[
            "Katzung Basic & Clinical Pharmacology",
            "Therapeutic Drug Monitoring Textbooks"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Narrow therapeutic index drugs: warfarin, digoxin, phenytoin, lithium, aminoglycosides",
            "Warfarin INR 2-3 for DVT; 2.5-3.5 for mechanical valves",
            "Phenytoin non-linear kinetics; small dose increases cause large level increases",
            "Gentamicin peak 5-10 mcg/mL (efficacy), trough <2 mcg/mL (toxicity)"
        ],
        adverse_effects=[
            "Digoxin toxicity at levels >2 ng/mL (arrhythmias, GI, visual)"
        ],
        contraindications=[]
    ),

    "PHARMACODYNAMICS_RECEPTORS": DoctrineBlock(
        topic="Receptor Theory and Drug-Receptor Interactions",
        keywords=["receptor", "agonist", "antagonist", "affinity", "intrinsic activity", "competitive", "non-competitive", "inverse agonist"],
        conclusion_template=[
            "Drug effects mediated by binding to specific receptors (GPCRs, ion channels, enzymes, nuclear)",
            "Agonists activate receptors; antagonists block receptor activation",
            "Competitive antagonists surmountable by increasing agonist; non-competitive are not"
        ],
        reasoning_framework="""
        Receptor interaction analysis:
        1. Receptor type identification (GPCR, ligand-gated ion channel, enzyme-linked, nuclear)
        2. Affinity (Kd) - drug-receptor binding strength
        3. Intrinsic activity - ability to activate receptor (α = 0 to 1)
        4. Full agonist (α = 1), partial agonist (0 < α < 1), antagonist (α = 0)
        5. Competitive antagonism (parallel rightward shift, no Emax change)
        6. Non-competitive antagonism (decreased Emax, no shift)
        7. Irreversible antagonism (covalent binding)
        8. Inverse agonist (reduces constitutive receptor activity)
        """,
        key_factors=[
            "β-blockers competitive antagonists at β-adrenergic receptors",
            "Aspirin irreversible COX-1/2 inhibitor (covalent acetylation)",
            "Buprenorphine partial μ-opioid agonist (ceiling effect on respiratory depression)",
            "Flumazenil competitive GABA-A antagonist (reverses benzodiazepines)",
            "Naloxone competitive μ-opioid antagonist (reverses opioids)",
            "Spare receptors allow maximal response with <100% receptor occupancy"
        ],
        primary_authority=[
            "IUPHAR/BPS Guide to Pharmacology",
            "Receptor classification databases"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Propranolol non-selective β-blocker; metoprolol β1-selective",
            "Buprenorphine difficult to reverse with naloxone (high affinity)",
            "Atropine competitive muscarinic antagonist (surmountable by acetylcholine)",
            "Tamoxifen partial agonist in bone/uterus, antagonist in breast"
        ],
        adverse_effects=[
            "β-blocker bronchoconstriction in asthma (β2 blockade)",
            "Atropine anticholinergic effects (dry mouth, urinary retention, confusion)"
        ],
        contraindications=[
            "Non-selective β-blockers contraindicated in asthma/COPD"
        ]
    ),

    "DRUG_INTERACTIONS_CYP450": DoctrineBlock(
        topic="CYP450-Mediated Drug-Drug Interactions",
        keywords=["drug interaction", "CYP450", "inhibitor", "inducer", "substrate", "3A4", "2D6", "2C9", "2C19"],
        conclusion_template=[
            "CYP450 inhibition increases substrate levels (toxicity risk)",
            "CYP450 induction decreases substrate levels (treatment failure)",
            "Clinical significance depends on substrate therapeutic index and alternative pathways"
        ],
        reasoning_framework="""
        Drug interaction risk assessment:
        1. Identify substrate CYP450 isoenzyme(s)
        2. Determine if substrate has narrow therapeutic index
        3. Assess inhibitor potency (strong/moderate/weak)
        4. Evaluate inducer magnitude and time course
        5. Consider alternative metabolic pathways
        6. Quantify interaction magnitude (AUC fold-change)
        7. Determine clinical management strategy
        """,
        key_factors=[
            "Strong CYP3A4 inhibitors: ketoconazole, itraconazole, clarithromycin, ritonavir",
            "Strong CYP3A4 inducers: rifampin, phenytoin, carbamazepine, St. John's Wort",
            "CYP2D6 substrates: codeine, tramadol, metoprolol, TCAs, SSRIs",
            "CYP2C9 substrates: warfarin, phenytoin, NSAIDs",
            "CYP2C19 substrates: clopidogrel, PPIs, diazepam",
            "Grapefruit juice irreversible CYP3A4 inhibition (lasts 24-72 hours)"
        ],
        primary_authority=[
            "FDA Drug Interaction Studies Guidance",
            "University of Washington Drug Interaction Database",
            "Lexicomp/Micromedex Interaction Databases"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Simvastatin + clarithromycin: avoid (CYP3A4 inhibition → rhabdomyolysis)",
            "Warfarin + rifampin: increase warfarin dose 2-5x during rifampin, taper after",
            "Tacrolimus + fluconazole: reduce tacrolimus dose 50-75% (CYP3A4 inhibition)",
            "Oral contraceptives + rifampin: use backup contraception (CYP3A4 induction)"
        ],
        adverse_effects=[
            "Statin + azole: myopathy, rhabdomyolysis",
            "Warfarin + azole: bleeding",
            "Cyclosporine + St. John's Wort: transplant rejection"
        ],
        contraindications=[
            "Simvastatin >10 mg contraindicated with strong CYP3A4 inhibitors"
        ]
    ),

    "DRUG_INTERACTIONS_PGP": DoctrineBlock(
        topic="P-glycoprotein Drug Interactions",
        keywords=["P-gp", "P-glycoprotein", "efflux", "absorption", "CNS penetration", "digoxin", "ABCB1"],
        conclusion_template=[
            "P-glycoprotein efflux transporter limits absorption and CNS penetration of substrates",
            "P-gp inhibition increases substrate bioavailability and tissue distribution",
            "P-gp induction decreases substrate levels"
        ],
        reasoning_framework="""
        P-gp interaction assessment:
        1. Identify substrate (digoxin, dabigatran, rivaroxaban, fexofenadine)
        2. Determine inhibitor/inducer status
        3. Predict effect on absorption (intestinal P-gp)
        4. Predict effect on distribution (BBB, placenta)
        5. Overlap with CYP3A4 (many drugs substrate/inhibitor of both)
        6. Clinical significance evaluation
        """,
        key_factors=[
            "Digoxin prototypical P-gp substrate (not metabolized, narrow therapeutic index)",
            "P-gp inhibitors: verapamil, amiodarone, quinidine, clarithromycin, cyclosporine",
            "P-gp inducers: rifampin, St. John's Wort, carbamazepine",
            "P-gp and CYP3A4 overlap: many drugs affect both systems",
            "Intestinal P-gp reduces oral bioavailability; CNS P-gp limits brain penetration"
        ],
        primary_authority=[
            "International Transporter Consortium Guidelines",
            "FDA Drug Interaction Guidance"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Digoxin + verapamil: reduce digoxin dose 50% (P-gp inhibition doubles levels)",
            "Dabigatran + dronedarone: avoid (P-gp inhibition increases bleeding)",
            "Loperamide normally doesn't cross BBB due to P-gp; inhibition causes CNS effects",
            "Fexofenadine non-sedating because P-gp blocks CNS entry"
        ],
        adverse_effects=[
            "Digoxin toxicity when combined with P-gp inhibitors"
        ],
        contraindications=[
            "Dabigatran contraindicated with strong P-gp inhibitors in renal impairment"
        ]
    ),

    "AUTONOMIC_CHOLINERGICS": DoctrineBlock(
        topic="Cholinergic Agonists and Parasympathomimetics",
        keywords=["acetylcholine", "cholinergic", "muscarinic", "nicotinic", "parasympathetic", "pilocarpine", "bethanechol"],
        conclusion_template=[
            "Cholinergic agonists stimulate muscarinic (smooth muscle, glands, heart) and nicotinic receptors",
            "Clinical uses limited by widespread parasympathetic side effects",
            "Acetylcholinesterase inhibitors increase synaptic ACh concentration"
        ],
        reasoning_framework="""
        Cholinergic pharmacology:
        1. Direct agonists (carbachol, pilocarpine, bethanechol)
        2. Indirect agonists/AChE inhibitors (neostigmine, pyridostigmine, donepezil)
        3. Muscarinic effects (SLUDGE: Salivation, Lacrimation, Urination, Defecation, GI upset, Emesis)
        4. Nicotinic effects (neuromuscular, autonomic ganglia)
        5. Organophosphate poisoning (irreversible AChE inhibition)
        6. Antidote therapy (atropine for muscarinic, pralidoxime for reactivation)
        """,
        key_factors=[
            "Pilocarpine treats glaucoma (miosis, increased trabecular outflow)",
            "Bethanechol treats urinary retention (bladder contraction)",
            "Neostigmine reverses neuromuscular blockade (increases ACh at NMJ)",
            "Donepezil treats Alzheimer's (increases CNS ACh)",
            "Organophosphates cause cholinergic crisis (antidote: atropine + pralidoxime)",
            "Echothiophate irreversible AChE inhibitor (glaucoma)"
        ],
        primary_authority=[
            "American Academy of Ophthalmology Guidelines",
            "Toxicology textbooks (organophosphate poisoning)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Pilocarpine 1-2% ophthalmic drops for acute angle-closure glaucoma",
            "Neostigmine 0.5-2.5 mg IV + glycopyrrolate (prevent bradycardia)",
            "Donepezil 5-10 mg/day for mild-moderate Alzheimer's",
            "Atropine 2 mg IV/IM q5-10min until secretions controlled (organophosphate)"
        ],
        adverse_effects=[
            "SLUDGE syndrome (cholinergic excess)",
            "Bradycardia, bronchospasm, increased secretions"
        ],
        contraindications=[
            "Asthma (bronchospasm risk)",
            "Mechanical GI/GU obstruction"
        ]
    ),

    "AUTONOMIC_ANTICHOLINERGICS": DoctrineBlock(
        topic="Anticholinergic Agents and Muscarinic Antagonists",
        keywords=["atropine", "scopolamine", "anticholinergic", "muscarinic", "mydriasis", "cycloplegia", "antiemetic"],
        conclusion_template=[
            "Muscarinic antagonists block parasympathetic effects on smooth muscle, glands, heart",
            "Clinical uses: bradycardia, organophosphate poisoning, motion sickness, COPD, overactive bladder",
            "Anticholinergic syndrome: dry as bone, red as beet, hot as hare, blind as bat, mad as hatter"
        ],
        reasoning_framework="""
        Anticholinergic pharmacology:
        1. Non-selective antagonists (atropine, scopolamine)
        2. Selective antagonists (ipratropium, tiotropium, oxybutynin, tolterodine)
        3. Cardiovascular effects (tachycardia via vagal blockade)
        4. Ocular effects (mydriasis, cycloplegia, increased IOP)
        5. GI/GU effects (constipation, urinary retention)
        6. CNS effects (confusion, hallucinations, hyperthermia)
        7. Antidote for overdose (physostigmine)
        """,
        key_factors=[
            "Atropine 0.5-1 mg IV for bradycardia (blocks vagal tone)",
            "Scopolamine transdermal for motion sickness",
            "Ipratropium/tiotropium inhaled for COPD (quaternary ammonium, minimal systemic absorption)",
            "Oxybutynin/tolterodine for overactive bladder",
            "Tropicamide ophthalmic for mydriasis (cycloplegic refraction)",
            "Glycopyrrolate quaternary (doesn't cross BBB, less CNS effects)"
        ],
        primary_authority=[
            "GOLD COPD Guidelines",
            "AUA Overactive Bladder Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Atropine 2 mg IV for organophosphate poisoning (repeat until secretions dry)",
            "Ipratropium 0.5 mg nebulized q6h for COPD exacerbation",
            "Avoid tertiary anticholinergics in elderly (CNS effects, falls)",
            "Use glycopyrrolate instead of atropine in elderly"
        ],
        adverse_effects=[
            "Dry mouth, constipation, urinary retention",
            "Tachycardia, confusion, blurred vision",
            "Precipitate acute angle-closure glaucoma in predisposed individuals",
            "Hyperthermia (impaired sweating)"
        ],
        contraindications=[
            "Narrow-angle glaucoma",
            "Obstructive uropathy, bowel obstruction",
            "Myasthenia gravis"
        ]
    ),

    "AUTONOMIC_ADRENERGICS": DoctrineBlock(
        topic="Adrenergic Agonists and Sympathomimetics",
        keywords=["epinephrine", "norepinephrine", "dobutamine", "dopamine", "phenylephrine", "α-agonist", "β-agonist"],
        conclusion_template=[
            "Adrenergic agonists stimulate α (vasoconstriction) and β (cardiac, bronchodilation) receptors",
            "Catecholamines (epi, norepi, dopamine, dobutamine) have short half-lives due to COMT/MAO",
            "Receptor selectivity determines clinical use and side effect profile"
        ],
        reasoning_framework="""
        Adrenergic agonist selection:
        1. Receptor selectivity (α1, α2, β1, β2, dopamine)
        2. Clinical indication (shock, heart failure, anaphylaxis, asthma, nasal congestion)
        3. Hemodynamic effects (HR, contractility, SVR, CO)
        4. Direct vs indirect mechanism (tyramine, ephedrine release endogenous NE)
        5. Metabolism (COMT, MAO) and duration
        6. Dose-dependent effects (dopamine)
        """,
        key_factors=[
            "Epinephrine α+β agonist: anaphylaxis, cardiac arrest, bronchospasm",
            "Norepinephrine α1>>β1: septic shock (pure vasoconstrictor)",
            "Dobutamine β1>β2: cardiogenic shock (inotrope)",
            "Dopamine dose-dependent: low=dopamine receptors, mid=β1, high=α1",
            "Phenylephrine pure α1: hypotension, nasal decongestant",
            "Albuterol selective β2: bronchodilation"
        ],
        primary_authority=[
            "Surviving Sepsis Campaign Guidelines",
            "ACLS/PALS Guidelines",
            "GINA Asthma Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Epinephrine 0.3-0.5 mg IM (1:1000) for anaphylaxis",
            "Norepinephrine 8-12 mcg/min IV for septic shock (titrate to MAP ≥65)",
            "Dobutamine 2-20 mcg/kg/min for cardiogenic shock",
            "Albuterol 2.5 mg nebulized for acute asthma",
            "Phenylephrine 100-200 mcg IV for hypotension"
        ],
        adverse_effects=[
            "Tachycardia, arrhythmias, myocardial ischemia",
            "Hypertension, peripheral ischemia/necrosis (extravasation)",
            "Tremor, hypokalemia (β2 effects)"
        ],
        contraindications=[
            "Non-selective β-agonists in coronary artery disease (ischemia risk)"
        ]
    ),

    "AUTONOMIC_BETA_BLOCKERS": DoctrineBlock(
        topic="β-Adrenergic Antagonists (Beta-Blockers)",
        keywords=["beta-blocker", "metoprolol", "propranolol", "carvedilol", "atenolol", "cardioselective", "ISA"],
        conclusion_template=[
            "β-blockers reduce HR, contractility, BP via β1 blockade; prevent bronchoconstriction via β2 selectivity",
            "Indicated for HTN, CAD, HF, arrhythmias; contraindicated in severe asthma/bradycardia/decompensated HF",
            "Lipophilic β-blockers cross BBB (CNS effects); hydrophilic renally eliminated"
        ],
        reasoning_framework="""
        β-blocker selection:
        1. Cardioselectivity (β1 vs non-selective β1+β2)
        2. Intrinsic sympathomimetic activity (ISA)
        3. α-blocking activity (carvedilol, labetalol)
        4. Lipophilicity (CNS penetration, metabolism)
        5. Indication-specific (post-MI, HF, HTN)
        6. Renal vs hepatic elimination
        """,
        key_factors=[
            "Cardioselective (β1): metoprolol, atenolol, bisoprolol, esmolol",
            "Non-selective (β1+β2): propranolol, nadolol, timolol",
            "Mixed α+β: carvedilol, labetalol",
            "ISA: pindolol, acebutolol (less bradycardia)",
            "Lipophilic: propranolol, metoprolol (hepatic metabolism, CNS effects)",
            "Hydrophilic: atenolol, nadolol (renal elimination)"
        ],
        primary_authority=[
            "ACC/AHA Heart Failure Guidelines",
            "ACC/AHA Hypertension Guidelines",
            "Post-MI beta-blocker trials (MERIT-HF, COPERNICUS)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Metoprolol 25-200 mg BID for HTN, post-MI, HF",
            "Carvedilol 3.125-25 mg BID for HF (titrate slowly)",
            "Esmolol 50-300 mcg/kg/min IV for SVT (ultra-short acting)",
            "Propranolol 10-40 mg TID for essential tremor, migraine prophylaxis"
        ],
        adverse_effects=[
            "Bradycardia, AV block, hypotension",
            "Bronchoconstriction in asthma/COPD (non-selective)",
            "Fatigue, depression, sexual dysfunction",
            "Mask hypoglycemia symptoms in diabetes",
            "Worsening HF if started high-dose or during decompensation"
        ],
        contraindications=[
            "Severe asthma/COPD (non-selective β-blockers)",
            "Decompensated heart failure (start after euvolemia)",
            "2nd/3rd degree AV block, severe bradycardia",
            "Cardiogenic shock"
        ]
    ),

    "CARDIOVASCULAR_ANTIHYPERTENSIVES": DoctrineBlock(
        topic="Antihypertensive Agents",
        keywords=["hypertension", "ACE inhibitor", "ARB", "CCB", "diuretic", "amlodipine", "lisinopril", "losartan"],
        conclusion_template=[
            "First-line agents: ACEi/ARB, CCB, thiazide diuretics per JNC 8/ACC guidelines",
            "ACEi/ARB provide renoprotection in diabetes and HF; contraindicated in pregnancy",
            "Combination therapy required for most patients to achieve BP <130/80"
        ],
        reasoning_framework="""
        Antihypertensive selection:
        1. Patient factors (age, race, comorbidities)
        2. Compelling indications (DM, CKD, HF, post-MI)
        3. First-line agent selection (ACEi/ARB/CCB/thiazide)
        4. Combination therapy strategy
        5. Resistant HTN workup (secondary causes, adherence)
        6. BP targets (130/80 general, 140/90 elderly)
        """,
        key_factors=[
            "ACE inhibitors: lisinopril, enalapril (reduce RAAS, renoprotective)",
            "ARBs: losartan, valsartan (ACEi alternative without cough)",
            "CCBs: amlodipine, diltiazem (vasodilation, no metabolic effects)",
            "Thiazides: HCTZ, chlorthalidone (volume depletion)",
            "β-blockers: NOT first-line unless compelling indication (CAD, HF)",
            "Black patients respond better to CCB/thiazide than ACEi/ARB monotherapy"
        ],
        primary_authority=[
            "ACC/AHA 2017 Hypertension Guideline",
            "JNC 8",
            "SPRINT, ACCORD BP trials"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Lisinopril 10-40 mg daily for HTN + DM/CKD",
            "Amlodipine 5-10 mg daily for HTN (elderly, black patients)",
            "Chlorthalidone 12.5-25 mg daily (superior to HCTZ for CV outcomes)",
            "Losartan 50-100 mg daily for HTN + ACEi intolerance"
        ],
        adverse_effects=[
            "ACEi: dry cough (10-15%), hyperkalemia, angioedema",
            "ARB: hyperkalemia, less cough than ACEi",
            "CCB: peripheral edema, constipation (diltiazem)",
            "Thiazides: hypokalemia, hyperuricemia, hyperglycemia"
        ],
        contraindications=[
            "ACEi/ARB in pregnancy (teratogenic), bilateral RAS",
            "CCB in decompensated HF (negative inotrope)",
            "Thiazides in gout"
        ]
    ),

    "CARDIOVASCULAR_ANTICOAGULANTS": DoctrineBlock(
        topic="Anticoagulants and Thrombolytics",
        keywords=["warfarin", "heparin", "DOAC", "rivaroxaban", "apixaban", "dabigatran", "INR", "aPTT"],
        conclusion_template=[
            "Anticoagulants prevent thrombus formation; indication determines agent (VTE, AFib, mechanical valve)",
            "Warfarin requires INR monitoring; DOACs fixed-dose without monitoring",
            "Bleeding risk vs thrombotic benefit assessed via CHA2DS2-VASc and HAS-BLED"
        ],
        reasoning_framework="""
        Anticoagulant selection:
        1. Indication (VTE, AFib, mechanical valve, ACS)
        2. Renal function (DOACs renally eliminated; avoid if CrCl <15-30)
        3. Drug interactions (warfarin extensive, DOACs moderate)
        4. Monitoring requirements (warfarin yes, DOACs no)
        5. Reversal agents (warfarin=vitamin K/PCC, dabigatran=idarucizumab, Xa inhibitors=andexanet)
        6. Bleeding risk (HAS-BLED score)
        7. Cost and adherence
        """,
        key_factors=[
            "Warfarin inhibits vitamin K epoxide reductase (VKORC1); affects factors II, VII, IX, X",
            "DOACs: dabigatran (direct thrombin inhibitor), rivaroxaban/apixaban/edoxaban (factor Xa inhibitors)",
            "Heparin/LMWH bridge warfarin (delayed onset 3-5 days)",
            "Warfarin INR 2-3 (VTE, AFib), 2.5-3.5 (mechanical valve)",
            "DOACs contraindicated in mechanical valves (RE-ALIGN trial)",
            "CrCl <30: avoid dabigatran; reduce DOAC doses"
        ],
        primary_authority=[
            "CHEST Antithrombotic Guidelines",
            "AHA/ACC AFib Guidelines",
            "DOAC trial data (RE-LY, ROCKET-AF, ARISTOTLE, ENGAGE-AF)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Warfarin 5 mg daily, titrate to INR 2-3 (check INR q3-7d initially)",
            "Apixaban 5 mg BID for AFib (2.5 mg BID if ≥2 of: age ≥80, weight ≤60 kg, Cr ≥1.5)",
            "Rivaroxaban 20 mg daily with food for AFib",
            "Dabigatran 150 mg BID for AFib (75 mg BID if CrCl 15-30)",
            "Enoxaparin 1 mg/kg SC BID for VTE bridge"
        ],
        adverse_effects=[
            "Major bleeding (GI, intracranial hemorrhage)",
            "Warfarin: skin necrosis (protein C deficiency), teratogenic",
            "Heparin: HIT (thrombocytopenia + thrombosis), osteoporosis"
        ],
        contraindications=[
            "Active bleeding, severe thrombocytopenia",
            "Recent surgery/trauma with high bleeding risk",
            "Pregnancy (warfarin teratogenic; LMWH preferred)"
        ]
    ),

    "CARDIOVASCULAR_ANTIPLATELETS": DoctrineBlock(
        topic="Antiplatelet Agents",
        keywords=["aspirin", "clopidogrel", "ticagrelor", "prasugrel", "DAPT", "P2Y12", "COX-1"],
        conclusion_template=[
            "Aspirin irreversibly inhibits COX-1 (TXA2), preventing platelet aggregation",
            "P2Y12 inhibitors (clopidogrel, ticagrelor, prasugrel) block ADP-mediated platelet activation",
            "Dual antiplatelet therapy (DAPT) for ACS and post-PCI; duration depends on bleeding risk"
        ],
        reasoning_framework="""
        Antiplatelet regimen design:
        1. Indication (primary/secondary prevention, ACS, post-PCI)
        2. Aspirin 81 mg daily (all patients unless contraindicated)
        3. P2Y12 inhibitor selection (clopidogrel prodrug vs ticagrelor/prasugrel active)
        4. DAPT duration (ACS 12 months, stable CAD 6 months post-PCI)
        5. Bleeding risk (PRECISE-DAPT, DAPT score)
        6. CYP2C19 polymorphism (clopidogrel non-responders)
        """,
        key_factors=[
            "Aspirin 81 mg daily for secondary prevention",
            "Clopidogrel 75 mg daily (prodrug, CYP2C19-activated)",
            "Ticagrelor 90 mg BID (reversible P2Y12 inhibitor, faster onset than clopidogrel)",
            "Prasugrel 10 mg daily (irreversible, more potent than clopidogrel, higher bleeding)",
            "DAPT = aspirin + P2Y12 inhibitor",
            "CYP2C19 poor metabolizers have reduced clopidogrel efficacy"
        ],
        primary_authority=[
            "ACC/AHA DAPT Guideline",
            "ESC Dual Antiplatelet Therapy Guidelines",
            "PLATO, TRITON-TIMI 38 trials"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "STEMI/NSTEMI: aspirin 162-325 mg load, then 81 mg daily + ticagrelor/prasugrel",
            "Stable CAD post-PCI: aspirin + clopidogrel × 6-12 months, then aspirin alone",
            "High bleeding risk: consider shorter DAPT (3-6 months) or clopidogrel monotherapy",
            "CYP2C19 poor metabolizers: consider ticagrelor/prasugrel instead of clopidogrel"
        ],
        adverse_effects=[
            "Bleeding (GI most common)",
            "Aspirin: GI ulceration, tinnitus, Reye syndrome (children)",
            "Ticagrelor: dyspnea (10-15%), bradycardia",
            "Prasugrel: higher bleeding than clopidogrel"
        ],
        contraindications=[
            "Active bleeding, history ICH",
            "Prasugrel if history stroke/TIA or age >75",
            "Aspirin allergy (consider desensitization)"
        ]
    ),

    "CARDIOVASCULAR_STATINS": DoctrineBlock(
        topic="HMG-CoA Reductase Inhibitors (Statins)",
        keywords=["statin", "atorvastatin", "rosuvastatin", "simvastatin", "LDL", "cholesterol", "ASCVD"],
        conclusion_template=[
            "Statins reduce LDL-C via HMG-CoA reductase inhibition, proven to reduce ASCVD events",
            "Intensity determines LDL reduction: high (≥50%), moderate (30-50%), low (<30%)",
            "Statin benefit > myopathy risk for most patients; monitor CK if symptoms"
        ],
        reasoning_framework="""
        Statin therapy decision:
        1. ASCVD risk assessment (10-year Pooled Cohort Equation)
        2. Intensity selection (high, moderate, low)
        3. High-intensity: atorvastatin 40-80 mg, rosuvastatin 20-40 mg
        4. Moderate-intensity: atorvastatin 10-20 mg, rosuvastatin 5-10 mg, simvastatin 20-40 mg
        5. Drug interaction assessment (CYP3A4)
        6. Renal/hepatic function
        7. LDL goal (secondary prevention <70 mg/dL)
        """,
        key_factors=[
            "High-intensity statins: atorvastatin 40-80 mg, rosuvastatin 20-40 mg",
            "Moderate-intensity: atorvastatin 10-20 mg, simvastatin 20-40 mg",
            "All statins metabolized by CYP3A4 except rosuvastatin (minimal), pravastatin (not CYP)",
            "Simvastatin dose limit 10 mg with strong CYP3A4 inhibitors",
            "Myopathy risk increased with gemfibrozil, high-dose statin, renal impairment, age >80",
            "Hydrophilic statins (pravastatin, rosuvastatin) less drug interactions"
        ],
        primary_authority=[
            "ACC/AHA Cholesterol Guideline 2018",
            "Statin trials: 4S, HPS, PROVE-IT, TNT"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "ASCVD (MI, stroke): high-intensity statin (atorvastatin 40-80 mg)",
            "DM age 40-75: moderate-intensity statin (atorvastatin 10-20 mg)",
            "LDL ≥190: high-intensity statin regardless of risk score",
            "10-year ASCVD risk ≥7.5%: moderate-intensity statin"
        ],
        adverse_effects=[
            "Myopathy (muscle pain, weakness, CK elevation)",
            "Rhabdomyolysis (rare, CK >10x ULN + renal failure)",
            "Hepatotoxicity (transaminitis, usually asymptomatic)",
            "New-onset diabetes (9% increase, outweighed by CV benefit)",
            "Cognitive complaints (reversible, no dementia association)"
        ],
        contraindications=[
            "Active liver disease",
            "Pregnancy/lactation",
            "Simvastatin >10 mg with strong CYP3A4 inhibitors"
        ]
    ),

    "CNS_OPIOIDS": DoctrineBlock(
        topic="Opioid Analgesics",
        keywords=["morphine", "oxycodone", "hydrocodone", "fentanyl", "opioid", "μ-receptor", "naloxone"],
        conclusion_template=[
            "Opioids activate μ, δ, κ opioid receptors for analgesia; μ-receptor mediates euphoria and respiratory depression",
            "Titrate to pain control; risk of tolerance, dependence, respiratory depression, constipation",
            "Naloxone reverses opioid toxicity via competitive μ-receptor antagonism"
        ],
        reasoning_framework="""
        Opioid prescribing:
        1. Pain severity assessment (mild/moderate/severe)
        2. Opioid selection (short-acting vs long-acting, route)
        3. Dose calculation (morphine milligram equivalents MME)
        4. Titration strategy (start low, go slow in opioid-naive)
        5. Monitoring (pain score, respiratory rate, sedation, bowel function)
        6. Naloxone prescribing for overdose risk (>50 MME/day)
        7. Addiction risk screening (SOAPP-R, ORT)
        """,
        key_factors=[
            "Morphine standard comparator (MME reference)",
            "Fentanyl 100x more potent than morphine (IV)",
            "Oxycodone 1.5x morphine potency",
            "Codeine/tramadol prodrugs (CYP2D6-activated)",
            "Methadone long half-life (24-36h), risk of QT prolongation, nonlinear conversion",
            "Constipation occurs in 90% (tolerance doesn't develop); prophylactic laxatives required"
        ],
        primary_authority=[
            "CDC Opioid Prescribing Guideline",
            "WHO Pain Ladder",
            "State prescription drug monitoring programs (PDMPs)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Morphine 5-10 mg PO q4h PRN for moderate-severe pain",
            "Oxycodone 5-10 mg PO q4-6h for moderate-severe pain",
            "Fentanyl 25 mcg/h patch for chronic pain (opioid-tolerant only)",
            "Naloxone 0.4-2 mg IV/IM/IN for opioid overdose (repeat q2-3min if needed)",
            "Prescribe naloxone kit if MME >50/day or risk factors"
        ],
        adverse_effects=[
            "Respiratory depression (dose-dependent, risk with benzodiazepines)",
            "Constipation (universal; use stimulant laxative + stool softener)",
            "Nausea/vomiting, sedation, pruritus",
            "Tolerance (increasing dose needed), physical dependence",
            "Opioid-induced hyperalgesia (paradoxical increased pain sensitivity)"
        ],
        contraindications=[
            "Severe respiratory depression, acute asthma",
            "Paralytic ileus",
            "Concurrent benzodiazepines (black box warning, respiratory depression)"
        ]
    ),

    "CNS_BENZODIAZEPINES": DoctrineBlock(
        topic="Benzodiazepines and GABA-A Agonists",
        keywords=["benzodiazepine", "diazepam", "lorazepam", "alprazolam", "GABA", "anxiolytic", "flumazenil"],
        conclusion_template=[
            "Benzodiazepines enhance GABA-A receptor chloride conductance for anxiolysis, sedation, anticonvulsant effects",
            "Short-term use for anxiety/insomnia; chronic use risks dependence, cognitive impairment, falls",
            "Flumazenil reverses benzodiazepine effects (caution: seizure risk in chronic users)"
        ],
        reasoning_framework="""
        Benzodiazepine selection:
        1. Indication (anxiety, insomnia, seizure, alcohol withdrawal, procedural sedation)
        2. Onset speed (alprazolam fast, oxazepam slow)
        3. Half-life (short: triazolam; intermediate: lorazepam; long: diazepam)
        4. Metabolism (lorazepam/oxazepam glucuronidation only, safe in liver disease)
        5. Duration of use (avoid >2-4 weeks chronic)
        6. Taper strategy (reduce 10-25% every 1-2 weeks)
        """,
        key_factors=[
            "Short-acting: triazolam (insomnia), midazolam (procedural sedation)",
            "Intermediate: alprazolam, lorazepam (anxiety, seizures)",
            "Long-acting: diazepam, clonazepam (alcohol withdrawal, chronic anxiety)",
            "Lorazepam/oxazepam metabolized by glucuronidation (no CYP, safe in cirrhosis)",
            "All benzodiazepines are DEA Schedule IV controlled substances",
            "Tolerance develops to sedation but not anxiolysis"
        ],
        primary_authority=[
            "Beers Criteria (avoid in elderly)",
            "CIWA-Ar protocol (alcohol withdrawal)",
            "American Geriatrics Society guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Lorazepam 0.5-2 mg PO/IV q6-8h for anxiety or seizures",
            "Diazepam 5-10 mg PO/IV for alcohol withdrawal (CIWA >8)",
            "Midazolam 1-2 mg IV for procedural sedation (titrate slowly)",
            "Alprazolam 0.25-0.5 mg TID for panic disorder (short-term)",
            "Taper slowly to avoid withdrawal seizures"
        ],
        adverse_effects=[
            "Sedation, cognitive impairment, anterograde amnesia",
            "Respiratory depression (especially with opioids or alcohol)",
            "Falls and fractures in elderly (Beers criteria: AVOID)",
            "Paradoxical agitation in children/elderly",
            "Withdrawal: anxiety, insomnia, tremor, seizures (abrupt cessation)"
        ],
        contraindications=[
            "Acute narrow-angle glaucoma",
            "Severe respiratory insufficiency",
            "Sleep apnea (worsens hypoxemia)",
            "Concurrent opioids (black box warning)"
        ]
    ),

    "CNS_ANTIDEPRESSANTS": DoctrineBlock(
        topic="Antidepressant Agents",
        keywords=["SSRI", "SNRI", "TCA", "MAOI", "sertraline", "fluoxetine", "bupropion", "serotonin syndrome"],
        conclusion_template=[
            "SSRIs first-line for depression/anxiety via selective serotonin reuptake inhibition",
            "SNRIs add norepinephrine reuptake inhibition (useful for pain, ADHD)",
            "Serotonin syndrome risk with multiple serotonergic agents; tricyclics cardiotoxic in overdose"
        ],
        reasoning_framework="""
        Antidepressant selection:
        1. Diagnosis (MDD, GAD, panic, OCD, PTSD, neuropathic pain)
        2. First-line: SSRIs (sertraline, escitalopram, fluoxetine)
        3. Second-line: SNRIs (duloxetine, venlafaxine), bupropion, mirtazapine
        4. Side effect profile (sexual dysfunction, weight gain, sedation, activation)
        5. Drug interactions (CYP2D6 for fluoxetine/paroxetine, MAOIs)
        6. Onset 4-6 weeks; trial duration 8-12 weeks before switching
        7. Suicide risk monitoring (black box warning age <25)
        """,
        key_factors=[
            "SSRIs: sertraline, escitalopram, fluoxetine, paroxetine, citalopram, fluvoxamine",
            "SNRIs: duloxetine, venlafaxine, desvenlafaxine (NE + 5-HT reuptake inhibition)",
            "Bupropion (NE/DA reuptake inhibitor, no sexual side effects, seizure risk)",
            "Mirtazapine (α2 antagonist, sedating, weight gain)",
            "TCAs: amitriptyline, nortriptyline (cardiotoxic, anticholinergic, lethal in overdose)",
            "MAOIs: phenelzine, tranylcypromine (tyramine hypertensive crisis, dietary restrictions)"
        ],
        primary_authority=[
            "APA Practice Guideline for MDD",
            "STAR*D trial data",
            "FDA black box warning (suicidality age <25)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Sertraline 50-200 mg daily for MDD/GAD (first-line)",
            "Escitalopram 10-20 mg daily for MDD/GAD",
            "Duloxetine 60-120 mg daily for MDD + neuropathic pain",
            "Bupropion 150-300 mg daily for MDD (avoid in seizure history)",
            "Fluoxetine long half-life (4-6 days); self-tapering, CYP2D6 inhibitor"
        ],
        adverse_effects=[
            "Sexual dysfunction (SSRI/SNRI 30-50%): anorgasmia, decreased libido",
            "GI upset, nausea (initial, transient)",
            "Weight gain (paroxetine, mirtazapine > others)",
            "Serotonin syndrome (hyperthermia, rigidity, autonomic instability, altered mental status)",
            "QTc prolongation (citalopram >40 mg, escitalopram >20 mg)",
            "Discontinuation syndrome (paroxetine, venlafaxine - taper slowly)"
        ],
        contraindications=[
            "MAOIs within 2 weeks of SSRIs (serotonin syndrome), 5 weeks for fluoxetine",
            "Bupropion in seizure disorder, eating disorders",
            "TCAs in recent MI, arrhythmia"
        ]
    ),

    "CNS_ANTIPSYCHOTICS": DoctrineBlock(
        topic="Antipsychotic Agents",
        keywords=["antipsychotic", "haloperidol", "risperidone", "olanzapine", "quetiapine", "EPS", "tardive dyskinesia", "NMS"],
        conclusion_template=[
            "Antipsychotics block dopamine D2 receptors for treatment of schizophrenia, bipolar mania, agitation",
            "First-generation (typical) cause more EPS; second-generation (atypical) cause more metabolic effects",
            "Monitor for EPS, tardive dyskinesia, metabolic syndrome, QTc prolongation, NMS"
        ],
        reasoning_framework="""
        Antipsychotic selection:
        1. Indication (schizophrenia, bipolar mania, delirium, agitation)
        2. First-generation (FGA) vs second-generation (SGA)
        3. FGA: haloperidol, fluphenazine (high potency, high EPS)
        4. SGA: risperidone, olanzapine, quetiapine, aripiprazole (less EPS, more metabolic)
        5. Side effect profile (EPS, sedation, weight gain, prolactin)
        6. Long-acting injectables for adherence
        7. Monitoring (metabolic panel, lipids, HbA1c, AIMS for TD)
        """,
        key_factors=[
            "FGAs: haloperidol, fluphenazine, chlorpromazine (D2 blockade, high EPS)",
            "SGAs: risperidone, olanzapine, quetiapine, aripiprazole, clozapine",
            "Clozapine most effective (treatment-resistant schizophrenia), requires ANC monitoring (agranulocytosis risk)",
            "Risperidone/paliperidone increase prolactin (galactorrhea, amenorrhea)",
            "Olanzapine/quetiapine cause weight gain, metabolic syndrome",
            "Aripiprazole partial D2 agonist (less EPS, less metabolic effects)"
        ],
        primary_authority=[
            "APA Practice Guideline for Schizophrenia",
            "CATIE, CUtLASS trials",
            "FDA REMS for clozapine"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Haloperidol 5-10 mg IM/PO for acute agitation",
            "Risperidone 2-6 mg daily for schizophrenia",
            "Olanzapine 10-20 mg daily for schizophrenia/bipolar mania",
            "Quetiapine 300-800 mg daily (also used for sleep, off-label)",
            "Clozapine 300-900 mg daily for treatment-resistant schizophrenia (requires ANC monitoring)"
        ],
        adverse_effects=[
            "EPS: akathisia, dystonia, parkinsonism, tardive dyskinesia (13-year risk 32%)",
            "Neuroleptic malignant syndrome (hyperthermia, rigidity, autonomic instability, CK elevation)",
            "Metabolic syndrome (weight gain, DM, dyslipidemia): olanzapine/clozapine highest risk",
            "QTc prolongation (haloperidol, ziprasidone, quetiapine)",
            "Prolactin elevation (risperidone, paliperidone, FGAs)",
            "Sedation, orthostatic hypotension",
            "Clozapine: agranulocytosis (1%), seizures (dose-dependent)"
        ],
        contraindications=[
            "Clozapine if history agranulocytosis, uncontrolled epilepsy",
            "Avoid FGAs in Parkinson's disease (worsens motor symptoms)",
            "QTc >500 ms (avoid high-risk agents)"
        ]
    ),

    "ANTIMICROBIALS_ANTIBIOTICS": DoctrineBlock(
        topic="Antibiotic Mechanisms and Resistance",
        keywords=["antibiotic", "beta-lactam", "penicillin", "cephalosporin", "vancomycin", "resistance", "MRSA", "ESBL"],
        conclusion_template=[
            "Antibiotics categorized by mechanism: cell wall (β-lactams, vancomycin), protein synthesis (aminoglycosides, macrolides, tetracyclines), DNA/RNA (fluoroquinolones, rifampin), folate synthesis (sulfonamides, trimethoprim)",
            "Resistance mechanisms: β-lactamase production, altered PBPs, efflux pumps, target modification",
            "Empiric therapy based on likely pathogens and local resistance patterns; de-escalate based on cultures"
        ],
        reasoning_framework="""
        Antibiotic selection:
        1. Infection site (pneumonia, UTI, cellulitis, meningitis, sepsis)
        2. Likely pathogens (Gram-positive, Gram-negative, anaerobes, atypicals)
        3. Local resistance patterns (antibiogram)
        4. Empiric broad-spectrum vs targeted narrow-spectrum
        5. Bactericidal vs bacteriostatic
        6. Renal/hepatic dose adjustment
        7. Culture results and de-escalation
        """,
        key_factors=[
            "β-lactams: penicillins, cephalosporins, carbapenems, monobactams (cell wall synthesis inhibition)",
            "Vancomycin: Gram-positive (MRSA), nephrotoxic, requires trough monitoring",
            "Fluoroquinolones: broad-spectrum, DNA gyrase inhibition, C. diff risk, tendon rupture",
            "Aminoglycosides: Gram-negative, concentration-dependent killing, nephro/ototoxic",
            "Macrolides: atypicals (Mycoplasma, Legionella), Gram-positive",
            "Carbapenems: broad-spectrum (ESBL, Pseudomonas), last-line agents"
        ],
        primary_authority=[
            "IDSA Clinical Practice Guidelines",
            "Sanford Guide to Antimicrobial Therapy",
            "Local hospital antibiograms"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "CAP: ceftriaxone + azithromycin or levofloxacin",
            "HAP/VAP: pip/tazo or cefepime or carbapenem + vancomycin (if MRSA risk)",
            "Complicated UTI/pyelonephritis: ceftriaxone or fluoroquinolone",
            "MRSA: vancomycin (trough 15-20 for serious infections) or daptomycin or linezolid",
            "ESBL: carbapenem (ertapenem, meropenem)"
        ],
        adverse_effects=[
            "β-lactam allergy (rash, anaphylaxis 1-5%)",
            "Vancomycin: red man syndrome (infusion-related), nephrotoxicity",
            "Fluoroquinolones: tendon rupture, QTc prolongation, C. diff",
            "Aminoglycosides: nephrotoxicity (trough <2), ototoxicity (irreversible)",
            "C. difficile colitis (fluoroquinolones, cephalosporins, clindamycin highest risk)"
        ],
        contraindications=[
            "Fluoroquinolones in pregnancy (cartilage damage), children (except cipro for anthrax/complicated UTI)",
            "Avoid ceftriaxone in neonates with hyperbilirubinemia"
        ]
    ),

    "ANTIMICROBIALS_ANTIVIRALS": DoctrineBlock(
        topic="Antiviral Agents",
        keywords=["antiviral", "acyclovir", "oseltamivir", "HIV", "HAART", "hepatitis", "influenza"],
        conclusion_template=[
            "Antivirals target viral replication: DNA polymerase (acyclovir, ganciclovir), reverse transcriptase (NRTIs, NNRTIs), protease (PIs), neuraminidase (oseltamivir)",
            "HIV requires combination therapy (HAART) to prevent resistance",
            "Influenza neuraminidase inhibitors reduce symptom duration if started within 48 hours"
        ],
        reasoning_framework="""
        Antiviral selection:
        1. Virus identification (HSV, VZV, CMV, influenza, HIV, HBV, HCV)
        2. Mechanism of action
        3. Resistance patterns (HIV genotype, influenza surveillance)
        4. Combination therapy for HIV (2 NRTIs + 1 NNRTI or PI or INSTI)
        5. Renal dose adjustment (acyclovir, tenofovir)
        6. Drug interactions (ritonavir CYP3A4 inhibitor)
        """,
        key_factors=[
            "Acyclovir: HSV, VZV (guanosine analog, viral DNA polymerase inhibitor)",
            "Ganciclovir: CMV (more toxic than acyclovir, bone marrow suppression)",
            "Oseltamivir: influenza A/B (neuraminidase inhibitor, start within 48h)",
            "HIV NRTIs: tenofovir, emtricitabine (reverse transcriptase inhibitors)",
            "HIV INSTIs: dolutegravir, bictegravir (integrase inhibitors, first-line)",
            "HCV DAAs: sofosbuvir, ledipasvir (cure rate >95%)"
        ],
        primary_authority=[
            "DHHS HIV Treatment Guidelines",
            "IDSA Influenza Guidelines",
            "AASLD/IDSA HCV Guidance"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "HSV encephalitis: acyclovir 10 mg/kg IV q8h × 14-21 days",
            "Influenza: oseltamivir 75 mg PO BID × 5 days (start within 48h)",
            "HIV: bictegravir/emtricitabine/tenofovir alafenamide (single-tablet regimen)",
            "HCV: sofosbuvir/velpatasvir × 12 weeks (pangenotypic)",
            "HSV suppression: acyclovir 400 mg PO BID or valacyclovir 500 mg daily"
        ],
        adverse_effects=[
            "Acyclovir: nephrotoxicity (crystalline nephropathy), neurotoxicity at high doses",
            "Ganciclovir: bone marrow suppression (neutropenia, thrombocytopenia)",
            "Oseltamivir: nausea, vomiting",
            "Tenofovir: nephrotoxicity, Fanconi syndrome, bone loss",
            "NNRTIs: rash (Stevens-Johnson syndrome risk with nevirapine)"
        ],
        contraindications=[
            "Ganciclovir if ANC <500 (bone marrow suppression)"
        ]
    ),

    "ANTI_INFLAMMATORY_NSAIDS": DoctrineBlock(
        topic="Non-Steroidal Anti-Inflammatory Drugs",
        keywords=["NSAID", "ibuprofen", "naproxen", "celecoxib", "COX-1", "COX-2", "GI bleed"],
        conclusion_template=[
            "NSAIDs inhibit cyclooxygenase (COX-1 and COX-2) for anti-inflammatory, analgesic, antipyretic effects",
            "COX-1 inhibition causes GI toxicity (ulcers, bleeding); COX-2 selective (celecoxib) reduces GI risk",
            "All NSAIDs increase cardiovascular risk (MI, stroke), contraindicated in severe CKD"
        ],
        reasoning_framework="""
        NSAID selection:
        1. Indication (pain, inflammation, fever)
        2. GI risk (history PUD, age >65, anticoagulants)
        3. CV risk (MI, stroke, HTN)
        4. Renal function (avoid if CrCl <30, reduce dose if <60)
        5. Non-selective (ibuprofen, naproxen) vs COX-2 selective (celecoxib)
        6. GI prophylaxis (PPI if high risk)
        """,
        key_factors=[
            "Non-selective: ibuprofen, naproxen, ketorolac, indomethacin, diclofenac",
            "COX-2 selective: celecoxib (lower GI risk, same CV risk)",
            "Aspirin irreversibly inhibits COX-1 (antiplatelet effect lasts platelet lifespan 7-10 days)",
            "Naproxen may have lowest CV risk among NSAIDs",
            "All NSAIDs reduce renal prostaglandins (cause Na/H2O retention, hyperkalemia, AKI)",
            "Ketorolac parenteral for severe pain (max 5 days, high GI bleed risk)"
        ],
        primary_authority=[
            "ACR Osteoarthritis Guidelines",
            "FDA NSAID Cardiovascular/GI Safety Review"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Ibuprofen 400-800 mg q6-8h for pain/inflammation (max 3200 mg/day)",
            "Naproxen 500 mg BID for chronic arthritis",
            "Celecoxib 200 mg daily for OA (lower GI risk than non-selective)",
            "Add PPI if high GI risk (age >65, anticoagulant, steroid, history PUD)",
            "Ketorolac 30 mg IV for acute pain (max 5 days)"
        ],
        adverse_effects=[
            "GI: dyspepsia, ulceration, bleeding, perforation (1-4%/year)",
            "CV: MI, stroke, HTN, HF exacerbation",
            "Renal: AKI, hyperkalemia, Na/H2O retention, papillary necrosis",
            "Hypersensitivity: aspirin-exacerbated respiratory disease (asthma/nasal polyps)",
            "Platelet inhibition (bleeding risk)"
        ],
        contraindications=[
            "CABG perioperative period (14 days)",
            "Active GI bleed, PUD",
            "Severe CKD (CrCl <30), decompensated HF",
            "Aspirin allergy (cross-reactivity)"
        ]
    ),

    "ANTI_INFLAMMATORY_CORTICOSTEROIDS": DoctrineBlock(
        topic="Corticosteroids and Glucocorticoid Therapy",
        keywords=["prednisone", "dexamethasone", "hydrocortisone", "steroid", "immunosuppression", "adrenal suppression"],
        conclusion_template=[
            "Corticosteroids suppress inflammation via genomic (anti-inflammatory genes) and non-genomic mechanisms",
            "Indicated for inflammatory/autoimmune diseases, asthma/COPD exacerbation, adrenal insufficiency",
            "Chronic use causes HPA axis suppression, hyperglycemia, osteoporosis, infection risk; taper slowly"
        ],
        reasoning_framework="""
        Corticosteroid therapy:
        1. Indication (asthma/COPD exacerbation, autoimmune, adrenal insufficiency, cerebral edema)
        2. Agent selection (potency, mineralocorticoid activity, half-life)
        3. Dose and duration (short-term high-dose vs chronic low-dose)
        4. Route (oral, IV, inhaled, topical, intra-articular)
        5. Taper strategy (>3 weeks use requires taper to avoid adrenal crisis)
        6. Adverse effect mitigation (PPI, calcium/vitamin D, glucose monitoring)
        """,
        key_factors=[
            "Hydrocortisone (short-acting, 1:1 glucocorticoid:mineralocorticoid, adrenal insufficiency)",
            "Prednisone (intermediate, 4:1 ratio, most common oral)",
            "Dexamethasone (long-acting, 25:1 ratio, cerebral edema, no mineralocorticoid)",
            "Equivalencies: hydrocortisone 20 mg = prednisone 5 mg = dexamethasone 0.75 mg",
            "HPA suppression after >3 weeks at >5 mg prednisone equivalent",
            "Inhaled steroids (fluticasone, budesonide) minimize systemic effects"
        ],
        primary_authority=[
            "GINA Asthma Guidelines",
            "GOLD COPD Guidelines",
            "Endocrine Society Adrenal Insufficiency Guideline"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "COPD exacerbation: prednisone 40 mg daily × 5 days",
            "Asthma exacerbation: prednisone 40-60 mg daily × 5-7 days",
            "Cerebral edema: dexamethasone 10 mg IV load, then 4 mg q6h",
            "Adrenal insufficiency: hydrocortisone 15-25 mg daily (divide BID/TID)",
            "Taper if >3 weeks use: reduce by 10% every 1-2 weeks"
        ],
        adverse_effects=[
            "Hyperglycemia, diabetes mellitus (monitor glucose)",
            "Osteoporosis, fractures (prophylaxis: calcium 1200 mg + vitamin D 800 IU)",
            "Infection risk (bacterial, fungal, TB reactivation)",
            "HPA axis suppression (adrenal crisis if abrupt cessation)",
            "GI ulceration (use PPI if high risk)",
            "Cushingoid features (moon facies, buffalo hump, striae)",
            "Psychiatric effects (insomnia, mood lability, psychosis)",
            "Cataracts, glaucoma, avascular necrosis"
        ],
        contraindications=[
            "Systemic fungal infection (relative; may require treatment first)",
            "Live vaccines (immunosuppressed)"
        ]
    ),

    "ENDOCRINE_INSULIN": DoctrineBlock(
        topic="Insulin Therapy and Diabetes Management",
        keywords=["insulin", "diabetes", "DKA", "HbA1c", "hypoglycemia", "NPH", "glargine", "lispro"],
        conclusion_template=[
            "Insulin types: rapid (lispro, aspart), short (regular), intermediate (NPH), long (glargine, detemir)",
            "Type 1 DM requires basal-bolus; Type 2 DM add insulin if HbA1c >9% on oral agents",
            "DKA treatment: IV regular insulin + fluids + potassium replacement"
        ],
        reasoning_framework="""
        Insulin regimen design:
        1. Diabetes type (T1DM requires insulin, T2DM add if inadequate control)
        2. Basal insulin (glargine, detemir, NPH) for fasting glucose control
        3. Bolus insulin (lispro, aspart, regular) for meal coverage
        4. Correction factor (1 unit reduces glucose by 50 mg/dL in most)
        5. Insulin-to-carb ratio (1 unit per 10-15g carb)
        6. Hypoglycemia prevention and treatment (glucose 15g)
        7. HbA1c target <7% (individualize)
        """,
        key_factors=[
            "Rapid-acting: lispro, aspart, glulisine (onset 5-15 min, peak 1-2h, duration 4h)",
            "Short-acting: regular (onset 30 min, peak 2-4h, duration 6-8h)",
            "Intermediate: NPH (onset 1-2h, peak 4-12h, duration 18-24h)",
            "Long-acting: glargine, detemir (onset 1-2h, no peak, duration 20-24h)",
            "DKA: regular insulin 0.1 unit/kg/h IV infusion",
            "Hypoglycemia: 15g fast-acting carb (glucose tabs, juice), recheck in 15 min"
        ],
        primary_authority=[
            "ADA Standards of Care in Diabetes",
            "AACE Diabetes Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "T1DM: glargine 0.2-0.3 units/kg qHS (basal) + lispro 0.5-1 unit/10g carb AC (bolus)",
            "T2DM starting insulin: glargine 10 units qHS, titrate by 2-4 units q3d to FBG 80-130",
            "DKA: NS 1L/h × 2, then 250 mL/h; regular insulin 0.1 unit/kg/h; K repletion goal 4-5",
            "Hypoglycemia treatment: 15g glucose, recheck in 15 min, repeat if still <70"
        ],
        adverse_effects=[
            "Hypoglycemia (glucose <70 mg/dL): shakiness, diaphoresis, confusion, seizure, coma",
            "Weight gain (3-5 kg common)",
            "Injection site reactions (lipohypertrophy, lipoatrophy)",
            "Hypokalemia during DKA treatment (K shifts intracellular)"
        ],
        contraindications=[
            "Hypoglycemia (hold insulin if glucose <70)"
        ]
    ),

    "CHEMOTHERAPY_MECHANISMS": DoctrineBlock(
        topic="Chemotherapy Mechanisms and Toxicity",
        keywords=["chemotherapy", "alkylating", "antimetabolite", "cisplatin", "5-FU", "myelosuppression", "emetogenic"],
        conclusion_template=[
            "Chemotherapy classes: alkylating agents (cyclophosphamide), antimetabolites (5-FU, methotrexate), anthracyclines (doxorubicin), platinum (cisplatin), taxanes (paclitaxel)",
            "Toxicities: myelosuppression (nadir 7-14 days), nausea/vomiting, mucositis, cardiotoxicity (anthracyclines), neurotoxicity (cisplatin, taxanes)",
            "Targeted therapy (imatinib, trastuzumab) more selective, fewer off-target effects"
        ],
        reasoning_framework="""
        Chemotherapy regimen:
        1. Cancer type and stage
        2. Curative vs palliative intent
        3. Performance status (ECOG 0-4)
        4. Organ function (renal, hepatic, cardiac)
        5. Combination therapy (FOLFOX, R-CHOP, etc.)
        6. Supportive care (antiemetics, G-CSF, hydration)
        7. Toxicity monitoring and dose modifications
        """,
        key_factors=[
            "Alkylating agents: cyclophosphamide, ifosfamide (DNA cross-linking, hemorrhagic cystitis)",
            "Antimetabolites: 5-FU, capecitabine, methotrexate, gemcitabine (inhibit DNA/RNA synthesis)",
            "Platinum: cisplatin, carboplatin (DNA cross-linking, nephrotoxic, ototoxic, emetogenic)",
            "Anthracyclines: doxorubicin, epirubicin (DNA intercalation, cardiotoxic - dose limit 450-550 mg/m²)",
            "Taxanes: paclitaxel, docetaxel (microtubule stabilization, neuropathy, hypersensitivity)",
            "Targeted: imatinib (BCR-ABL inhibitor for CML), trastuzumab (HER2 antibody for breast cancer)"
        ],
        primary_authority=[
            "NCCN Guidelines by cancer type",
            "ASCO Clinical Practice Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "FOLFOX (colorectal): 5-FU + leucovorin + oxaliplatin q2 weeks",
            "R-CHOP (lymphoma): rituximab + cyclophosphamide + doxorubicin + vincristine + prednisone q3 weeks",
            "Cisplatin premedication: aggressive hydration (NS 1-2L pre/post), ondansetron + dexamethasone",
            "G-CSF (filgrastim) if ANC <500 or febrile neutropenia",
            "ECHO before anthracyclines; stop if LVEF drops >10% or <50%"
        ],
        adverse_effects=[
            "Myelosuppression (ANC nadir 7-14 days): neutropenic fever, thrombocytopenia, anemia",
            "Nausea/vomiting (highly emetogenic: cisplatin; moderately: cyclophosphamide)",
            "Mucositis (5-FU, methotrexate): oral ulcers, diarrhea",
            "Cardiotoxicity (anthracyclines): HF, cardiomyopathy (cumulative dose-related)",
            "Neurotoxicity (cisplatin: ototoxicity, peripheral neuropathy; taxanes: sensory neuropathy)",
            "Nephrotoxicity (cisplatin: AKI, hypomagnesemia)"
        ],
        contraindications=[
            "Cisplatin if baseline CrCl <60 (dose adjust or avoid)",
            "Anthracyclines if LVEF <50% or cumulative dose exceeded"
        ]
    ),

    "PHARMACOGENOMICS": DoctrineBlock(
        topic="Pharmacogenomics and Individualized Therapy",
        keywords=["pharmacogenomics", "CYP2D6", "CYP2C19", "TPMT", "G6PD", "HLA-B*1502", "warfarin"],
        conclusion_template=[
            "Genetic polymorphisms affect drug metabolism (CYP450), targets (warfarin VKORC1), and toxicity (HLA alleles)",
            "CYP2D6 poor metabolizers: codeine ineffective, high tamoxifen failure; ultra-rapid: morphine toxicity",
            "Pre-treatment testing recommended for abacavir (HLA-B*5701), carbamazepine (HLA-B*1502 in Asians), azathioprine (TPMT)"
        ],
        reasoning_framework="""
        Pharmacogenomic application:
        1. Drug with known genetic association (codeine, clopidogrel, warfarin, abacavir, azathioprine)
        2. Genotype testing (CYP2D6, CYP2C19, TPMT, HLA-B*5701, VKORC1)
        3. Phenotype prediction (poor, intermediate, extensive, ultra-rapid metabolizer)
        4. Dose adjustment or alternative agent selection
        5. Clinical decision support integration
        """,
        key_factors=[
            "CYP2D6: codeine (prodrug activation), tamoxifen (prodrug), TCAs, β-blockers (metoprolol)",
            "CYP2C19: clopidogrel (prodrug activation), PPIs, SSRIs",
            "TPMT: thiopurines (azathioprine, 6-MP) - low activity causes myelosuppression",
            "VKORC1/CYP2C9: warfarin dosing (genotype-guided algorithms)",
            "HLA-B*5701: abacavir hypersensitivity (screen all patients before starting)",
            "HLA-B*1502: carbamazepine Stevens-Johnson syndrome (screen Asians)",
            "G6PD deficiency: avoid oxidant drugs (sulfonamides, dapsone, rasburicase) - hemolysis"
        ],
        primary_authority=[
            "CPIC Pharmacogenomics Guidelines",
            "PharmGKB Database",
            "FDA Table of Pharmacogenomic Biomarkers"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Codeine: avoid in CYP2D6 poor metabolizers (ineffective); caution in ultra-rapid (toxicity)",
            "Clopidogrel: consider prasugrel/ticagrelor if CYP2C19 poor metabolizer",
            "Warfarin: genotype-guided dosing algorithms (VKORC1 + CYP2C9) improve INR stability",
            "Abacavir: HLA-B*5701 screen before starting; avoid if positive",
            "Azathioprine: TPMT testing; reduce dose 50% if heterozygous, avoid if homozygous deficient"
        ],
        adverse_effects=[
            "CYP2D6 ultra-rapid: codeine → morphine toxicity (respiratory depression, death in infants)",
            "Abacavir hypersensitivity: fever, rash, GI symptoms; rechallenge fatal",
            "Carbamazepine HLA-B*1502: Stevens-Johnson syndrome (10-15% Han Chinese)",
            "TPMT deficiency: severe myelosuppression from standard azathioprine doses",
            "G6PD deficiency: acute hemolytic anemia from oxidant drugs"
        ],
        contraindications=[
            "Abacavir if HLA-B*5701 positive",
            "Carbamazepine if HLA-B*1502 positive (in Asians)",
            "Standard azathioprine dose if TPMT homozygous deficient"
        ]
    ),

    "ADVERSE_DRUG_REACTIONS": DoctrineBlock(
        topic="Adverse Drug Reactions Classification",
        keywords=["ADR", "Type A", "Type B", "Stevens-Johnson", "anaphylaxis", "hepatotoxicity", "nephrotoxicity"],
        conclusion_template=[
            "Type A (Augmented): dose-dependent, predictable, common (e.g., β-blocker bradycardia)",
            "Type B (Bizarre): idiosyncratic, unpredictable, rare (e.g., penicillin anaphylaxis, SJS)",
            "Severe cutaneous adverse reactions (SCAR): SJS, TEN, DRESS; stop drug immediately"
        ],
        reasoning_framework="""
        ADR assessment:
        1. Temporal relationship (Naranjo scale)
        2. Type A vs Type B classification
        3. Severity (mild, moderate, severe, life-threatening)
        4. Causality (definite, probable, possible, unlikely)
        5. Management (continue, dose reduce, switch, discontinue)
        6. Reporting (FDA MedWatch for serious ADRs)
        """,
        key_factors=[
            "Type A: dose-dependent (warfarin bleeding, digoxin toxicity, NSAID GI bleed)",
            "Type B: immune-mediated or idiosyncratic (penicillin allergy, SJS, malignant hyperthermia)",
            "Stevens-Johnson syndrome (SJS): <10% BSA; TEN >30% BSA (mortality 25-35%)",
            "DRESS: rash + eosinophilia + systemic symptoms (2-8 weeks after drug start)",
            "Drug-induced liver injury (DILI): acetaminophen (dose-dependent), isoniazid (idiosyncratic)",
            "Drug-induced nephrotoxicity: aminoglycosides, NSAIDs, cisplatin, vancomycin"
        ],
        primary_authority=[
            "FDA Adverse Event Reporting System (FAERS)",
            "WHO ADR Causality Assessment"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "SJS/TEN: stop offending drug immediately, supportive care (burn unit), IVIG",
            "Anaphylaxis: epinephrine 0.3-0.5 mg IM, diphenhydramine, corticosteroids",
            "DRESS: stop drug, systemic corticosteroids (prednisone 0.5-1 mg/kg)",
            "DILI: N-acetylcysteine for acetaminophen, otherwise stop drug and support",
            "Aminoglycoside nephrotoxicity: stop drug, hydration, avoid re-exposure"
        ],
        adverse_effects=[
            "SJS/TEN triggers: allopurinol, sulfonamides, anticonvulsants, NSAIDs",
            "Anaphylaxis triggers: β-lactams, contrast media, NSAIDs",
            "DRESS triggers: anticonvulsants (phenytoin, carbamazepine), allopurinol, sulfonamides",
            "Hepatotoxicity: acetaminophen, isoniazid, valproate, statins",
            "Nephrotoxicity: aminoglycosides, NSAIDs, ACEi (in RAS), cisplatin"
        ],
        contraindications=[
            "Rechallenge with SJS/TEN-causing drug is contraindicated (fatal)",
            "Avoid structurally related drugs (cross-reactivity)"
        ]
    ),

    "CONTROLLED_SUBSTANCES": DoctrineBlock(
        topic="Controlled Substance Scheduling and Regulation",
        keywords=["DEA", "Schedule I", "Schedule II", "controlled substance", "opioid", "benzodiazepine", "PDMP"],
        conclusion_template=[
            "DEA schedules drugs by abuse potential: I (highest, no medical use), II-V (decreasing abuse potential)",
            "Schedule II (opioids, stimulants) requires written/e-prescription, no refills",
            "State PDMPs track controlled substance dispensing to identify diversion/abuse"
        ],
        reasoning_framework="""
        Controlled substance prescribing:
        1. DEA schedule identification
        2. State/federal prescribing requirements
        3. PDMP query (mandatory in most states)
        4. Risk assessment (SOAPP-R, ORT for opioids)
        5. Informed consent and treatment agreement
        6. Monitoring (urine drug screen, pill counts)
        7. Tapering and discontinuation protocols
        """,
        key_factors=[
            "Schedule I: heroin, LSD, marijuana (federal), MDMA (no accepted medical use)",
            "Schedule II: oxycodone, hydrocodone, fentanyl, morphine, amphetamine, cocaine (anesthetic)",
            "Schedule III: codeine combination, buprenorphine, testosterone, ketamine",
            "Schedule IV: benzodiazepines, tramadol, zolpidem, carisoprodol",
            "Schedule V: codeine <200 mg/100 mL (cough syrup), pregabalin",
            "Schedule II: written/e-prescribe only, no refills, 90-day supply max in some states"
        ],
        primary_authority=[
            "DEA Controlled Substances Act",
            "CDC Opioid Prescribing Guideline",
            "State PDMP regulations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Check state PDMP before prescribing controlled substances",
            "Opioid agreement: random UDS, no early refills, single prescriber/pharmacy",
            "Naloxone co-prescribe if MME >50/day or risk factors (sleep apnea, benzos, alcohol)",
            "Taper opioids if escalating dose without benefit or aberrant behavior",
            "Benzodiazepines: avoid long-term use; taper 10-25% every 1-2 weeks"
        ],
        adverse_effects=[
            "Opioids: respiratory depression, constipation, tolerance, dependence, overdose",
            "Benzodiazepines: sedation, cognitive impairment, dependence, falls in elderly",
            "Stimulants: tachycardia, hypertension, psychosis, addiction"
        ],
        contraindications=[
            "Concurrent opioid + benzodiazepine (black box warning: respiratory depression)",
            "Opioids in active substance use disorder without MAT"
        ]
    ),

    "PEDIATRIC_GERIATRIC_DOSING": DoctrineBlock(
        topic="Pediatric and Geriatric Pharmacology",
        keywords=["pediatric dosing", "geriatric", "Beers Criteria", "weight-based", "renal impairment", "elderly"],
        conclusion_template=[
            "Pediatric dosing weight-based (mg/kg) or BSA-based (mg/m²); developmental differences in PK/PD",
            "Geriatric patients have reduced renal/hepatic function, altered Vd, increased ADR risk",
            "Beers Criteria identify potentially inappropriate medications in elderly (avoid anticholinergics, benzodiazepines, NSAIDs)"
        ],
        reasoning_framework="""
        Age-appropriate dosing:
        1. Pediatric: weight-based (mg/kg) or BSA (mg/m²)
        2. Neonatal considerations (immature enzymes, renal function)
        3. Geriatric: Cockcroft-Gault CrCl, Beers Criteria review
        4. Dose adjustment for organ impairment
        5. Drug-disease interactions in elderly
        6. Polypharmacy reduction (deprescribing)
        """,
        key_factors=[
            "Pediatric: immature CYP450 (chloramphenicol gray baby syndrome), immature renal function",
            "Neonates: avoid sulfas (kernicterus), avoid ceftriaxone if hyperbilirubinemia",
            "Geriatric: decreased CrCl (use Cockcroft-Gault, not just Cr), decreased albumin (increased free drug fraction)",
            "Beers Criteria: avoid anticholinergics (confusion, falls), benzodiazepines (falls, cognitive impairment), NSAIDs (GI bleed, AKI)",
            "Geriatric Vd changes: hydrophilic drugs (digoxin) have lower Vd (reduce dose); lipophilic (benzos) higher Vd (prolonged effect)",
            "Polypharmacy (≥5 drugs) increases ADR risk 50%"
        ],
        primary_authority=[
            "Beers Criteria (AGS)",
            "STOPP/START Criteria (European)",
            "Pediatric dosing references (Lexicomp, Harriet Lane)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Amoxicillin pediatric: 40-90 mg/kg/day divided q8-12h (otitis media)",
            "Digoxin geriatric: 0.0625-0.125 mg daily (reduce dose due to decreased Vd and CrCl)",
            "Avoid diphenhydramine in elderly (anticholinergic, use cetirizine instead)",
            "Metformin: discontinue if CrCl <30 in elderly (lactic acidosis risk)",
            "Deprescribing: stop drugs with no clear indication, especially if polypharmacy"
        ],
        adverse_effects=[
            "Pediatric: chloramphenicol gray baby syndrome (bone marrow suppression)",
            "Geriatric falls: benzodiazepines, anticholinergics, antipsychotics, α-blockers",
            "Geriatric cognitive impairment: anticholinergics (diphenhydramine, oxybutynin, TCAs)",
            "Geriatric AKI: NSAIDs, ACEi in volume depletion"
        ],
        contraindications=[
            "Aspirin in children <18 with viral illness (Reye syndrome risk)",
            "Tetracyclines in children <8 (tooth discoloration)",
            "Fluoroquinolones in children (cartilage damage; cipro approved for UTI/anthrax only)"
        ]
    ),

    "RENAL_HEPATIC_DOSING": DoctrineBlock(
        topic="Renal and Hepatic Dose Adjustment",
        keywords=["renal dosing", "CrCl", "Cockcroft-Gault", "hepatic impairment", "Child-Pugh", "dialysis"],
        conclusion_template=[
            "Renally eliminated drugs require dose adjustment based on CrCl (Cockcroft-Gault)",
            "Hepatic impairment reduces metabolism of drugs with high extraction (propranolol, morphine)",
            "Hemodialysis removes drugs with low Vd, low protein binding, small molecular weight"
        ],
        reasoning_framework="""
        Organ dysfunction dosing:
        1. Renal: Cockcroft-Gault CrCl calculation
        2. Renal categories: CrCl >80, 50-80, 30-50, 15-30, <15, HD
        3. Dose reduction or interval extension
        4. Hepatic: Child-Pugh score (A, B, C)
        5. Hepatic metabolism reduction for high extraction drugs
        6. Dialyzability assessment (molecular weight, protein binding, Vd)
        7. Post-dialysis supplemental dose if dialyzable
        """,
        key_factors=[
            "Cockcroft-Gault: CrCl = [(140-age) × weight] / (72 × Cr) × 0.85 if female",
            "Renally eliminated drugs: aminoglycosides, vancomycin, digoxin, metformin, gabapentin, enoxaparin",
            "Child-Pugh A (5-6 points) mild, B (7-9) moderate, C (10-15) severe hepatic impairment",
            "High hepatic extraction drugs: propranolol, morphine, lidocaine (reduce dose in cirrhosis)",
            "Dialyzable: low Vd (<1 L/kg), low protein binding (<80%), molecular weight <500 Da",
            "Non-dialyzable: high Vd (digoxin), high protein binding (warfarin)"
        ],
        primary_authority=[
            "Kidney Disease: Improving Global Outcomes (KDIGO)",
            "FDA Drug Labeling for Renal/Hepatic Impairment"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        clinical_considerations=[
            "Vancomycin CrCl <50: reduce dose or extend interval (trough-based dosing)",
            "Gabapentin CrCl 30-60: reduce dose 50%; CrCl <30: reduce 75%",
            "Metformin: avoid if CrCl <30 (lactic acidosis risk)",
            "Enoxaparin CrCl <30: reduce dose to 1 mg/kg daily (from BID)",
            "Morphine cirrhosis: reduce dose 50% (impaired glucuronidation + increased CNS sensitivity)",
            "Aminoglycosides HD: redose post-dialysis (dialyzable)"
        ],
        adverse_effects=[
            "Aminoglycoside accumulation in renal failure → nephrotoxicity, ototoxicity",
            "Gabapentin accumulation → sedation, confusion",
            "Metformin in renal failure → lactic acidosis (fatal)",
            "Opioid accumulation (morphine-6-glucuronide) → respiratory depression"
        ],
        contraindications=[
            "Metformin if CrCl <30",
            "NSAIDs in severe CKD (CrCl <30)",
            "Enoxaparin if CrCl <15 (unpredictable levels)"
        ]
    )
}

# ============================================================================
# TELEMETRY & MONITORING
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.queries_processed = 0
        self.cache_hits = 0
        self.total_latency_ms = 0
        self.error_count = 0
        self.triggered_doctrines = {}

    def record_query(self, latency_ms: float, doctrines: List[str], error: bool = False):
        self.queries_processed += 1
        self.total_latency_ms += latency_ms
        if error:
            self.error_count += 1
        for doctrine in doctrines:
            self.triggered_doctrines[doctrine] = self.triggered_doctrines.get(doctrine, 0) + 1

    def record_cache_hit(self):
        self.cache_hits += 1

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "queries_processed": self.queries_processed,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": self.cache_hits / max(1, self.queries_processed),
            "avg_latency_ms": self.total_latency_ms / max(1, self.queries_processed),
            "error_rate": self.error_count / max(1, self.queries_processed),
            "top_doctrines": sorted(self.triggered_doctrines.items(), key=lambda x: x[1], reverse=True)[:10]
        }

TELEMETRY = TelemetryCollector()

class DriftWatcher:
    def __init__(self):
        self.doctrine_usage = {key: 0 for key in DOCTRINE_CACHE.keys()}

    def track_usage(self, doctrine_key: str):
        if doctrine_key in self.doctrine_usage:
            self.doctrine_usage[doctrine_key] += 1

    def get_unused_doctrines(self) -> List[str]:
        return [k for k, v in self.doctrine_usage.items() if v == 0]

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(self.doctrine_usage)
        used = sum(1 for v in self.doctrine_usage.values() if v > 0)
        return {
            "total_doctrines": total,
            "used_doctrines": used,
            "coverage_percentage": (used / total) * 100,
            "unused_doctrines": self.get_unused_doctrines()
        }

DRIFT_WATCHER = DriftWatcher()

# ============================================================================
# CORE QUERY ENGINE
# ============================================================================

def search_doctrines(query: str) -> List[str]:
    """Search doctrine cache for relevant blocks based on keyword matching."""
    query_lower = query.lower()
    matches = []

    for key, block in DOCTRINE_CACHE.items():
        score = 0
        for keyword in block.keywords:
            if keyword.lower() in query_lower:
                score += 2

        if any(word in query_lower for word in block.topic.lower().split()):
            score += 1

        if score > 0:
            matches.append((key, score))

    matches.sort(key=lambda x: x[1], reverse=True)
    return [key for key, _ in matches[:5]]

def build_response(query: str, mode: ResponseMode, triggered_keys: List[str]) -> str:
    """Build pharmacology analysis response based on mode and triggered doctrines."""

    if not triggered_keys:
        return "No specific pharmacology doctrines matched this query. Please provide more specific drug-related details."

    triggered_blocks = [DOCTRINE_CACHE[key] for key in triggered_keys]

    if mode == ResponseMode.FAST:
        # Concise summary
        response_parts = []
        for block in triggered_blocks[:2]:
            response_parts.append(f"**{block.topic}**: {' '.join(block.conclusion_template[:1])}")

        if len(triggered_blocks) > 0:
            key_factors = triggered_blocks[0].key_factors[:3]
            response_parts.append(f"\n**Key Factors**: {'; '.join(key_factors)}")

        return "\n\n".join(response_parts)

    elif mode == ResponseMode.DEFENSE:
        # Audit-ready comprehensive analysis
        sections = []

        for block in triggered_blocks:
            section = [f"### {block.topic}"]
            section.append("\n**Pharmacological Basis**:")
            section.append(block.reasoning_framework.strip())

            section.append("\n**Clinical Conclusion**:")
            for conclusion in block.conclusion_template:
                section.append(f"- {conclusion}")

            section.append("\n**Key Pharmacological Factors**:")
            for factor in block.key_factors:
                section.append(f"- {factor}")

            if block.clinical_considerations:
                section.append("\n**Clinical Recommendations**:")
                for rec in block.clinical_considerations:
                    section.append(f"- {rec}")

            if block.adverse_effects:
                section.append("\n**Adverse Effects Profile**:")
                for ae in block.adverse_effects:
                    section.append(f"- {ae}")

            if block.contraindications:
                section.append("\n**Contraindications**:")
                for contra in block.contraindications:
                    section.append(f"- {contra}")

            section.append("\n**Authoritative References**:")
            for auth in block.primary_authority:
                section.append(f"- {auth}")

            section.append(f"\n**Confidence Level**: {block.confidence.value}")

            sections.append("\n".join(section))

        return "\n\n---\n\n".join(sections)

    else:  # MEMO mode
        # Full documentation memo format
        memo = [
            "# PHARMACOLOGY INTELLIGENCE MEMORANDUM",
            f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Query**: {query}",
            f"**Analysis Mode**: {mode.value}",
            "",
            "## EXECUTIVE SUMMARY",
            ""
        ]

        # Executive summary from first doctrine
        if triggered_blocks:
            first = triggered_blocks[0]
            memo.append(f"This analysis addresses {first.topic.lower()}. " + " ".join(first.conclusion_template))
            memo.append("")

        # Detailed analysis
        memo.append("## DETAILED PHARMACOLOGICAL ANALYSIS")
        memo.append("")

        for idx, block in enumerate(triggered_blocks, 1):
            memo.append(f"### {idx}. {block.topic}")
            memo.append("")

            memo.append("**Mechanism of Action & Pharmacology**:")
            memo.append(block.reasoning_framework.strip())
            memo.append("")

            memo.append("**Evidence-Based Conclusions**:")
            for conclusion in block.conclusion_template:
                memo.append(f"- {conclusion}")
            memo.append("")

            memo.append("**Critical Pharmacological Factors**:")
            for factor in block.key_factors:
                memo.append(f"- {factor}")
            memo.append("")

            if block.clinical_considerations:
                memo.append("**Clinical Application**:")
                for rec in block.clinical_considerations:
                    memo.append(f"- {rec}")
                memo.append("")

            if block.adverse_effects:
                memo.append("**Adverse Effects & Safety Profile**:")
                for ae in block.adverse_effects:
                    memo.append(f"- {ae}")
                memo.append("")

            if block.contraindications:
                memo.append("**Absolute/Relative Contraindications**:")
                for contra in block.contraindications:
                    memo.append(f"- {contra}")
                memo.append("")

            memo.append("**Authoritative References**:")
            for auth in block.primary_authority:
                memo.append(f"- {auth}")
            memo.append("")

            memo.append(f"**Epistemic Confidence**: {block.confidence.value}")
            memo.append("")
            memo.append("---")
            memo.append("")

        # Recommendations
        memo.append("## CLINICAL RECOMMENDATIONS")
        memo.append("")
        all_recs = []
        for block in triggered_blocks:
            all_recs.extend(block.clinical_considerations)

        for rec in all_recs[:10]:
            memo.append(f"- {rec}")
        memo.append("")

        # Safety considerations
        memo.append("## SAFETY CONSIDERATIONS")
        memo.append("")
        all_aes = []
        all_contras = []
        for block in triggered_blocks:
            all_aes.extend(block.adverse_effects)
            all_contras.extend(block.contraindications)

        if all_aes:
            memo.append("**Adverse Effects to Monitor**:")
            for ae in all_aes[:10]:
                memo.append(f"- {ae}")
            memo.append("")

        if all_contras:
            memo.append("**Contraindications**:")
            for contra in all_contras[:10]:
                memo.append(f"- {contra}")
            memo.append("")

        memo.append("---")
        memo.append("")
        memo.append("*This memorandum is generated by MED02 Pharmacology Intelligence Engine v1.0.0*")
        memo.append("*For clinical decision support only. Not a substitute for professional medical judgment.*")

        return "\n".join(memo)

def calculate_determinism_hash(query: str, triggered_keys: List[str], mode: ResponseMode) -> str:
    """Generate SHA-256 hash for reproducibility verification."""
    content = f"{query}|{','.join(sorted(triggered_keys))}|{mode.value}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

# ============================================================================
# API ENDPOINTS
# ============================================================================

@APP.get("/health")
async def health_check():
    """Comprehensive health check with system metrics."""
    coverage = DRIFT_WATCHER.get_coverage_report()
    metrics = TELEMETRY.get_metrics()

    return {
        "status": "operational",
        "engine": "MED02_pharmacology",
        "version": "1.0.0",
        "port": 9092,
        "doctrine_cache_size": len(DOCTRINE_CACHE),
        "coverage": coverage,
        "telemetry": metrics,
        "capabilities": [
            "pharmacokinetics (absorption, distribution, metabolism, excretion)",
            "pharmacodynamics (dose-response, receptor theory)",
            "drug interactions (CYP450, P-gp, protein binding)",
            "autonomic pharmacology (cholinergics, anticholinergics, adrenergics, beta-blockers)",
            "cardiovascular drugs (antihypertensives, anticoagulants, antiplatelets, statins)",
            "CNS pharmacology (opioids, benzodiazepines, antidepressants, antipsychotics)",
            "antimicrobial agents (antibiotics, antivirals, resistance)",
            "anti-inflammatory drugs (NSAIDs, corticosteroids)",
            "endocrine pharmacology (insulin)",
            "chemotherapy agents (alkylating, antimetabolites, targeted)",
            "pharmacogenomics (CYP2D6, CYP2C19, HLA)",
            "adverse drug reactions (Type A/B, SJS, anaphylaxis)",
            "controlled substances (DEA scheduling)",
            "pediatric/geriatric dosing (Beers Criteria)",
            "renal/hepatic dose adjustment"
        ]
    }

@APP.post("/query", response_model=QueryResponse)
async def query_pharmacology(request: QueryRequest):
    """Main pharmacology query endpoint with comprehensive analysis."""
    start_time = datetime.now()

    try:
        logger.info(f"Processing query: {request.query[:100]}... | Mode: {request.mode}")

        # Search doctrine cache
        triggered_keys = search_doctrines(request.query)

        if triggered_keys:
            TELEMETRY.record_cache_hit()

        for key in triggered_keys:
            DRIFT_WATCHER.track_usage(key)

        # Build response
        answer = build_response(request.query, request.mode, triggered_keys)

        # Determine confidence
        if len(triggered_keys) >= 3:
            confidence = ConfidenceLevel.DEFENSIBLE
        elif len(triggered_keys) >= 1:
            confidence = ConfidenceLevel.AGGRESSIVE
        else:
            confidence = ConfidenceLevel.DISCLOSURE

        # Calculate determinism hash
        det_hash = calculate_determinism_hash(request.query, triggered_keys, request.mode)

        # Build reasoning chain
        reasoning_chain = [
            f"Searched {len(DOCTRINE_CACHE)} pharmacology doctrine blocks",
            f"Matched {len(triggered_keys)} relevant doctrines: {', '.join(triggered_keys)}",
            f"Mode: {request.mode.value}",
            f"Confidence: {confidence.value}"
        ]

        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        TELEMETRY.record_query(latency_ms, triggered_keys, error=False)

        logger.info(f"Query completed in {latency_ms:.2f}ms | Triggered: {len(triggered_keys)} doctrines")

        return QueryResponse(
            query=request.query,
            mode=request.mode,
            answer=answer,
            confidence=confidence,
            triggered_doctrines=triggered_keys,
            reasoning_chain=reasoning_chain,
            determinism_hash=det_hash,
            metadata={
                "latency_ms": round(latency_ms, 2),
                "timestamp": datetime.now().isoformat(),
                "doctrine_count": len(triggered_keys)
            }
        )

    except Exception as e:
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        TELEMETRY.record_query(latency_ms, [], error=True)
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/doctrines")
async def list_doctrines():
    """List all available pharmacology doctrine topics."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "key": key,
                "topic": block.topic,
                "keywords": block.keywords,
                "confidence": block.confidence.value
            }
            for key, block in DOCTRINE_CACHE.items()
        ]
    }

@APP.get("/coverage")
async def get_coverage():
    """Get doctrine coverage statistics."""
    return DRIFT_WATCHER.get_coverage_report()

@APP.get("/metrics")
async def get_metrics():
    """Get telemetry metrics."""
    return TELEMETRY.get_metrics()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting MED02 Pharmacology Engine on port 9092")
    uvicorn.run(APP, host="0.0.0.0", port=9092)
