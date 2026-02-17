from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: float
    confidence_zone: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Drug Absorption Mechanisms",
        keywords=["absorption", "bioavailability", "pharmacokinetics", "oral", "parenteral", "first-pass effect", "membrane transport"],
        conclusion_template="Drug absorption is determined by route of administration, physicochemical properties, and biological barriers.",
        reasoning_framework="""
Drug absorption refers to the process by which a drug enters the systemic circulation from its site of administration. The efficiency of absorption depends on the drug's solubility, ionization state, molecular size, and the presence of transporters or barriers such as the gastrointestinal epithelium. Oral drugs may undergo first-pass metabolism in the liver, reducing bioavailability. Parenteral routes bypass these barriers, leading to more predictable absorption. Passive diffusion, facilitated diffusion, and active transport are key mechanisms. The rate and extent of absorption are influenced by gastric emptying, blood flow, and formulation factors.
""",
        key_factors=["route of administration", "drug solubility", "membrane permeability", "first-pass metabolism", "transport mechanisms"],
        primary_authority=["Goodman & Gilman's The Pharmacological Basis of Therapeutics", "FDA Guidance on Bioavailability"],
        burden_holder="Prescriber",
        adversary_position="Drug absorption is unpredictable and cannot be reliably estimated.",
        counter_arguments=[
            "Clinical studies provide absorption profiles for most drugs.",
            "Bioavailability is routinely measured and standardized."
        ],
        resolution_strategy="Utilize pharmacokinetic data and clinical guidelines to optimize absorption.",
        entity_scope="All drugs administered systemically",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FDA Bioavailability Guidelines"
    ),
    DoctrineBlock(
        topic="Volume of Distribution and Tissue Binding",
        keywords=["volume of distribution", "Vd", "tissue binding", "plasma protein binding", "pharmacokinetics"],
        conclusion_template="Volume of distribution reflects the extent of drug distribution into tissues relative to plasma.",
        reasoning_framework="""
The volume of distribution (Vd) is a calculated pharmacokinetic parameter that quantifies the distribution of a drug between plasma and tissues. Drugs with high tissue binding or lipophilicity exhibit large Vd, indicating extensive extravascular distribution. Plasma protein binding restricts Vd, while low binding increases it. Vd is used to estimate loading doses and interpret plasma concentrations. Factors such as age, disease, and body composition affect Vd. Understanding tissue binding is crucial for predicting drug effects and toxicity.
""",
        key_factors=["lipophilicity", "plasma protein binding", "tissue affinity", "body composition", "disease states"],
        primary_authority=["Goodman & Gilman's", "Clinical Pharmacokinetics Texts"],
        burden_holder="Pharmacologist",
        adversary_position="Vd is an unreliable measure due to variable tissue binding.",
        counter_arguments=[
            "Vd is empirically determined and clinically validated.",
            "Adjustments are made for special populations."
        ],
        resolution_strategy="Apply population-specific Vd values and monitor plasma levels.",
        entity_scope="Systemically distributed drugs",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Clinical Pharmacokinetics Standards"
    ),
    DoctrineBlock(
        topic="Hepatic Drug Metabolism and CYP450 System",
        keywords=["hepatic metabolism", "CYP450", "phase I", "phase II", "enzyme induction", "enzyme inhibition"],
        conclusion_template="Hepatic metabolism via CYP450 enzymes is the primary determinant of drug clearance and interaction potential.",
        reasoning_framework="""
The liver is the principal organ for drug metabolism, utilizing cytochrome P450 (CYP450) enzymes for phase I reactions (oxidation, reduction, hydrolysis) and conjugation enzymes for phase II (glucuronidation, sulfation). CYP450 isoforms (e.g., CYP3A4, CYP2D6) exhibit genetic variability, leading to differences in metabolic rates. Enzyme induction increases metabolism, reducing drug efficacy, while inhibition raises plasma concentrations and toxicity risk. Drug-drug interactions often involve CYP450 modulation. Hepatic impairment alters metabolism, requiring dose adjustments.
""",
        key_factors=["CYP450 isoform", "enzyme induction", "enzyme inhibition", "genetic polymorphism", "hepatic function"],
        primary_authority=["FDA Drug Interaction Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="CYP450 metabolism is too variable for clinical prediction.",
        counter_arguments=[
            "Genotyping and phenotyping improve prediction.",
            "Clinical guidelines address common interactions."
        ],
        resolution_strategy="Screen for CYP450 interactions and adjust therapy accordingly.",
        entity_scope="Drugs metabolized by liver",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FDA Drug Interaction Guidance"
    ),
    DoctrineBlock(
        topic="Renal and Biliary Elimination",
        keywords=["renal elimination", "biliary elimination", "glomerular filtration", "tubular secretion", "hepatic clearance"],
        conclusion_template="Renal and biliary elimination are key pathways for drug excretion, influenced by organ function and drug properties.",
        reasoning_framework="""
Drugs are eliminated from the body primarily via renal (urine) and biliary (feces) routes. Renal elimination involves glomerular filtration, tubular secretion, and reabsorption. Biliary elimination depends on hepatic transporters and conjugation. Renal impairment reduces clearance, necessitating dose adjustments. Drugs with high molecular weight or conjugated metabolites are often excreted in bile. Monitoring renal and hepatic function is essential for safe drug therapy.
""",
        key_factors=["renal function", "hepatic function", "drug molecular weight", "conjugation", "transporters"],
        primary_authority=["FDA Renal Impairment Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Renal and biliary elimination are unpredictable in disease states.",
        counter_arguments=[
            "Renal and hepatic function tests guide dosing.",
            "Clinical pharmacokinetics provide elimination profiles."
        ],
        resolution_strategy="Adjust dosing based on organ function and monitor for toxicity.",
        entity_scope="Drugs eliminated via urine or bile",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FDA Renal Impairment Guidance"
    ),
    DoctrineBlock(
        topic="Dose-Response Relationships and Therapeutic Window",
        keywords=["dose-response", "therapeutic window", "EC50", "toxicity", "efficacy"],
        conclusion_template="The therapeutic window is defined by the range between minimum effective and minimum toxic concentrations.",
        reasoning_framework="""
Dose-response relationships describe how drug effects change with increasing doses. The therapeutic window is the concentration range where efficacy is achieved without toxicity. EC50 represents the concentration producing 50% maximal effect. Drugs with narrow therapeutic windows require close monitoring (e.g., warfarin, digoxin). Individual variability, drug interactions, and disease states can alter the window. Understanding dose-response is critical for safe and effective therapy.
""",
        key_factors=["EC50", "minimum effective concentration", "minimum toxic concentration", "individual variability", "drug interactions"],
        primary_authority=["FDA Therapeutic Drug Monitoring Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Therapeutic windows are too variable for clinical use.",
        counter_arguments=[
            "Therapeutic drug monitoring ensures safety.",
            "Population data inform dosing guidelines."
        ],
        resolution_strategy="Monitor plasma concentrations and adjust dosing as needed.",
        entity_scope="Drugs with narrow therapeutic windows",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FDA Therapeutic Drug Monitoring Guidance"
    ),
    DoctrineBlock(
        topic="Receptor Theory and Drug-Receptor Interactions",
        keywords=["receptor theory", "drug-receptor interaction", "affinity", "efficacy", "agonist", "antagonist"],
        conclusion_template="Drug effects are mediated by interactions with specific receptors, governed by affinity and efficacy.",
        reasoning_framework="""
Receptor theory posits that drugs exert effects by binding to specific cellular receptors. Affinity describes the strength of binding, while efficacy reflects the ability to activate the receptor. Agonists activate receptors, antagonists block them, and partial agonists produce intermediate responses. Receptor density, subtype, and signal transduction pathways influence drug effects. Understanding receptor interactions is fundamental to pharmacology and drug development.
""",
        key_factors=["receptor subtype", "affinity", "efficacy", "agonist/antagonist", "signal transduction"],
        primary_authority=["Goodman & Gilman's", "Pharmacology Textbooks"],
        burden_holder="Pharmacologist",
        adversary_position="Receptor theory is overly simplistic for complex drug actions.",
        counter_arguments=[
            "Receptor theory is supported by molecular and clinical evidence.",
            "Complex signaling is incorporated into modern models."
        ],
        resolution_strategy="Integrate receptor theory with systems pharmacology for comprehensive understanding.",
        entity_scope="All drugs acting on receptors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Goodman & Gilman's"
    ),
    DoctrineBlock(
        topic="CYP450-Mediated Drug-Drug Interactions",
        keywords=["CYP450", "drug-drug interaction", "enzyme induction", "enzyme inhibition", "pharmacokinetics"],
        conclusion_template="CYP450-mediated interactions can alter drug metabolism, leading to changes in efficacy and toxicity.",
        reasoning_framework="""
Cytochrome P450 enzymes are responsible for metabolizing many drugs. Co-administration of drugs that induce or inhibit CYP450 isoforms can significantly alter plasma concentrations. Inducers (e.g., rifampin) increase metabolism, reducing efficacy. Inhibitors (e.g., ketoconazole) decrease metabolism, increasing toxicity risk. Genetic polymorphisms further complicate interactions. Clinical management involves screening for interactions and adjusting therapy.
""",
        key_factors=["CYP450 isoform", "inducer/inhibitor", "genetic polymorphism", "drug plasma concentration", "clinical outcome"],
        primary_authority=["FDA Drug Interaction Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="CYP450 interactions are too complex for routine management.",
        counter_arguments=[
            "Drug interaction databases facilitate management.",
            "Clinical guidelines address common scenarios."
        ],
        resolution_strategy="Use drug interaction resources and monitor therapy.",
        entity_scope="Drugs metabolized by CYP450",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FDA Drug Interaction Guidance"
    ),
    DoctrineBlock(
        topic="P-glycoprotein Drug Interactions",
        keywords=["P-glycoprotein", "drug interaction", "efflux transporter", "bioavailability", "pharmacokinetics"],
        conclusion_template="P-glycoprotein modulates drug absorption and elimination, affecting bioavailability and interaction risk.",
        reasoning_framework="""
P-glycoprotein (P-gp) is an efflux transporter expressed in intestinal, hepatic, and renal tissues. It limits drug absorption by pumping substrates back into the lumen. Inhibitors of P-gp increase bioavailability, while inducers decrease it. P-gp also affects drug elimination and tissue distribution. Drug-drug interactions involving P-gp can alter therapeutic outcomes. Genetic variability and disease states influence P-gp activity.
""",
        key_factors=["P-gp substrate", "P-gp inhibitor", "P-gp inducer", "bioavailability", "genetic variability"],
        primary_authority=["FDA Drug Interaction Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="P-gp interactions are not clinically significant.",
        counter_arguments=[
            "Clinical studies demonstrate altered drug levels.",
            "FDA guidance addresses P-gp interactions."
        ],
        resolution_strategy="Screen for P-gp interactions and adjust therapy.",
        entity_scope="Drugs transported by P-gp",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FDA Drug Interaction Guidance"
    ),
    DoctrineBlock(
        topic="Cholinergic Agonists and Parasympathomimetics",
        keywords=["cholinergic agonist", "parasympathomimetic", "acetylcholine", "muscarinic", "nicotinic"],
        conclusion_template="Cholinergic agonists mimic acetylcholine, activating muscarinic and/or nicotinic receptors.",
        reasoning_framework="""
Cholinergic agonists stimulate the parasympathetic nervous system by mimicking acetylcholine. Muscarinic agonists (e.g., pilocarpine) activate muscarinic receptors, producing effects such as bradycardia, increased secretions, and smooth muscle contraction. Nicotinic agonists (e.g., nicotine) stimulate ganglionic and neuromuscular junction receptors. Clinical uses include glaucoma, xerostomia, and myasthenia gravis. Adverse effects include cholinergic toxicity.
""",
        key_factors=["receptor subtype", "drug selectivity", "clinical indication", "adverse effects", "toxicity"],
        primary_authority=["Goodman & Gilman's", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Cholinergic agonists are unsafe due to toxicity.",
        counter_arguments=[
            "Dosing and monitoring mitigate risks.",
            "Therapeutic benefits outweigh risks in selected patients."
        ],
        resolution_strategy="Use lowest effective dose and monitor for toxicity.",
        entity_scope="Drugs acting on cholinergic receptors",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Goodman & Gilman's"
    ),
    DoctrineBlock(
        topic="Anticholinergic Agents and Muscarinic Antagonists",
        keywords=["anticholinergic", "muscarinic antagonist", "acetylcholine", "parasympathetic", "atropine"],
        conclusion_template="Anticholinergic agents block muscarinic receptors, reducing parasympathetic activity.",
        reasoning_framework="""
Anticholinergic agents competitively inhibit muscarinic receptors, reducing the effects of acetylcholine. Clinical uses include treatment of bradycardia, motion sickness, and overactive bladder. Common agents include atropine, scopolamine, and oxybutynin. Adverse effects include dry mouth, blurred vision, urinary retention, and cognitive impairment, especially in elderly patients. Contraindications include glaucoma and prostatic hypertrophy.
""",
        key_factors=["receptor selectivity", "clinical indication", "adverse effects", "contraindications", "patient age"],
        primary_authority=["Goodman & Gilman's", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Anticholinergic agents are contraindicated due to adverse effects.",
        counter_arguments=[
            "Careful patient selection reduces risk.",
            "Alternative therapies are considered when necessary."
        ],
        resolution_strategy="Assess risk-benefit and monitor for anticholinergic toxicity.",
        entity_scope="Drugs acting on muscarinic receptors",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Goodman & Gilman's"
    ),
    DoctrineBlock(
        topic="Adrenergic Agonists and Sympathomimetics",
        keywords=["adrenergic agonist", "sympathomimetic", "epinephrine", "norepinephrine", "alpha", "beta"],
        conclusion_template="Adrenergic agonists stimulate alpha and/or beta receptors, increasing sympathetic activity.",
        reasoning_framework="""
Adrenergic agonists activate alpha and beta adrenergic receptors, mimicking the effects of endogenous catecholamines. Alpha agonists (e.g., phenylephrine) cause vasoconstriction, while beta agonists (e.g., albuterol) produce bronchodilation. Mixed agonists (e.g., epinephrine) have broad effects. Clinical uses include anaphylaxis, asthma, and shock. Adverse effects include hypertension, tachycardia, and arrhythmias.
""",
        key_factors=["receptor subtype", "drug selectivity", "clinical indication", "adverse effects", "contraindications"],
        primary_authority=["Goodman & Gilman's", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Adrenergic agonists cause excessive sympathetic stimulation.",
        counter_arguments=[
            "Dosing and monitoring minimize adverse effects.",
            "Therapeutic benefits are substantial in acute settings."
        ],
        resolution_strategy="Use lowest effective dose and monitor cardiovascular status.",
        entity_scope="Drugs acting on adrenergic receptors",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Goodman & Gilman's"
    ),
    DoctrineBlock(
        topic="β-Adrenergic Antagonists (Beta-Blockers)",
        keywords=["beta-blocker", "β-adrenergic antagonist", "hypertension", "arrhythmia", "heart failure"],
        conclusion_template="Beta-blockers inhibit β-adrenergic receptors, reducing heart rate and blood pressure.",
        reasoning_framework="""
Beta-blockers competitively inhibit β-adrenergic receptors, decreasing heart rate, contractility, and blood pressure. They are used in hypertension, arrhythmias, angina, and heart failure. Selective beta-1 blockers (e.g., metoprolol) minimize pulmonary effects. Non-selective agents (e.g., propranolol) affect both β1 and β2 receptors. Adverse effects include bradycardia, fatigue, and bronchospasm. Contraindications include asthma and severe heart failure.
""",
        key_factors=["receptor selectivity", "clinical indication", "adverse effects", "contraindications", "patient comorbidities"],
        primary_authority=["Goodman & Gilman's", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Beta-blockers worsen pulmonary and cardiac conditions.",
        counter_arguments=[
            "Selective agents reduce pulmonary risk.",
            "Clinical guidelines recommend monitoring and titration."
        ],
        resolution_strategy="Select agent based on patient profile and monitor therapy.",
        entity_scope="Drugs acting on β-adrenergic receptors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Goodman & Gilman's"
    ),
    DoctrineBlock(
        topic="Antihypertensive Agents",
        keywords=["antihypertensive", "ACE inhibitor", "ARB", "calcium channel blocker", "diuretic"],
        conclusion_template="Antihypertensive agents lower blood pressure via diverse mechanisms targeting vascular, renal, and neurohormonal pathways.",
        reasoning_framework="""
Antihypertensive drugs include ACE inhibitors, ARBs, calcium channel blockers, diuretics, and beta-blockers. Each class targets different pathways: ACE inhibitors block angiotensin II formation, ARBs block its receptor, calcium channel blockers reduce vascular tone, diuretics decrease plasma volume, and beta-blockers reduce cardiac output. Combination therapy is often required. Adverse effects vary by class and patient factors. Guidelines recommend individualized therapy based on comorbidities.
""",
        key_factors=["drug class", "mechanism of action", "patient comorbidities", "adverse effects", "guideline recommendations"],
        primary_authority=["JNC 8 Hypertension Guidelines", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Antihypertensive agents are ineffective in resistant hypertension.",
        counter_arguments=[
            "Combination therapy improves efficacy.",
            "Lifestyle modification enhances drug effects."
        ],
        resolution_strategy="Follow guideline-based therapy and monitor response.",
        entity_scope="Patients with hypertension",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="JNC 8 Hypertension Guidelines"
    ),
    DoctrineBlock(
        topic="Anticoagulants and Thrombolytics",
        keywords=["anticoagulant", "thrombolytic", "warfarin", "heparin", "DOAC", "clot"],
        conclusion_template="Anticoagulants and thrombolytics prevent and dissolve clots, reducing thromboembolic risk.",
        reasoning_framework="""
Anticoagulants inhibit clotting factors to prevent thrombus formation. Warfarin inhibits vitamin K-dependent factors, heparin activates antithrombin, and DOACs target specific factors (e.g., factor Xa). Thrombolytics (e.g., alteplase) dissolve existing clots by activating plasminogen. Indications include atrial fibrillation, venous thromboembolism, and acute myocardial infarction. Risks include bleeding and drug interactions. Monitoring is essential, especially with warfarin.
""",
        key_factors=["drug class", "mechanism of action", "clinical indication", "bleeding risk", "monitoring"],
        primary_authority=["ACC/AHA Guidelines", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Anticoagulants and thrombolytics increase bleeding risk.",
        counter_arguments=[
            "Risk stratification and monitoring reduce adverse events.",
            "Therapeutic benefits outweigh risks in high-risk patients."
        ],
        resolution_strategy="Individualize therapy and monitor coagulation parameters.",
        entity_scope="Patients at risk for thromboembolism",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ACC/AHA Guidelines"
    ),
    DoctrineBlock(
        topic="Antiplatelet Agents",
        keywords=["antiplatelet", "aspirin", "clopidogrel", "platelet aggregation", "stroke", "MI"],
        conclusion_template="Antiplatelet agents inhibit platelet aggregation, reducing risk of arterial thrombosis.",
        reasoning_framework="""
Antiplatelet drugs (e.g., aspirin, clopidogrel) block platelet activation and aggregation, preventing arterial thrombosis. Aspirin irreversibly inhibits COX-1, while clopidogrel blocks ADP receptors. Indications include prevention of myocardial infarction, stroke, and stent thrombosis. Risks include bleeding and gastrointestinal toxicity. Drug interactions may reduce efficacy. Guidelines recommend therapy based on risk stratification.
""",
        key_factors=["drug mechanism", "clinical indication", "bleeding risk", "drug interactions", "guideline recommendations"],
        primary_authority=["ACC/AHA Guidelines", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Antiplatelet agents cause excessive bleeding.",
        counter_arguments=[
            "Risk assessment and monitoring minimize adverse effects.",
            "Therapeutic benefits are substantial in high-risk patients."
        ],
        resolution_strategy="Individualize therapy and monitor for bleeding.",
        entity_scope="Patients at risk for arterial thrombosis",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ACC/AHA Guidelines"
    ),
    DoctrineBlock(
        topic="HMG-CoA Reductase Inhibitors (Statins)",
        keywords=["statin", "HMG-CoA reductase inhibitor", "cholesterol", "LDL", "cardiovascular risk"],
        conclusion_template="Statins lower LDL cholesterol and reduce cardiovascular risk via inhibition of HMG-CoA reductase.",
        reasoning_framework="""
Statins inhibit HMG-CoA reductase, the rate-limiting enzyme in cholesterol synthesis. This reduces LDL cholesterol and lowers cardiovascular risk. Statins are first-line therapy for hyperlipidemia and secondary prevention of cardiovascular events. Adverse effects include myopathy, liver enzyme elevation, and rare rhabdomyolysis. Drug interactions (e.g., CYP3A4 inhibitors) may increase toxicity. Guidelines recommend statin intensity based on risk profile.
""",
        key_factors=["drug potency", "LDL reduction", "cardiovascular risk", "adverse effects", "drug interactions"],
        primary_authority=["ACC/AHA Cholesterol Guidelines", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Statins cause unacceptable muscle toxicity.",
        counter_arguments=[
            "Incidence of severe myopathy is low.",
            "Monitoring and dose adjustment reduce risk."
        ],
        resolution_strategy="Select statin and dose based on patient risk and monitor for toxicity.",
        entity_scope="Patients with hyperlipidemia",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="ACC/AHA Cholesterol Guidelines"
    ),
    DoctrineBlock(
        topic="Opioid Analgesics",
        keywords=["opioid", "analgesic", "morphine", "mu receptor", "pain management", "addiction"],
        conclusion_template="Opioid analgesics activate mu receptors to relieve pain but carry risks of addiction and respiratory depression.",
        reasoning_framework="""
Opioids bind to mu, delta, and kappa receptors in the CNS, producing analgesia, euphoria, and sedation. Clinical uses include acute and chronic pain management. Risks include addiction, tolerance, respiratory depression, and constipation. Guidelines recommend lowest effective dose, short duration, and risk assessment for addiction. Naloxone is used for overdose reversal. Monitoring and patient education are essential.
""",
        key_factors=["receptor subtype", "analgesic efficacy", "addiction risk", "respiratory depression", "monitoring"],
        primary_authority=["CDC Opioid Prescribing Guidelines", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Opioids are unsafe due to addiction and overdose risk.",
        counter_arguments=[
            "Risk mitigation strategies reduce adverse outcomes.",
            "Opioids are essential for severe pain management."
        ],
        resolution_strategy="Follow guidelines, educate patients, and monitor therapy.",
        entity_scope="Patients with moderate to severe pain",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="CDC Opioid Prescribing Guidelines"
    ),
    DoctrineBlock(
        topic="Benzodiazepines and GABA-A Agonists",
        keywords=["benzodiazepine", "GABA-A agonist", "anxiolytic", "sedative", "diazepam", "dependence"],
        conclusion_template="Benzodiazepines enhance GABA-A receptor activity, producing anxiolytic and sedative effects but risk dependence.",
        reasoning_framework="""
Benzodiazepines bind to GABA-A receptors, increasing chloride influx and neuronal inhibition. Clinical uses include anxiety, insomnia, seizures, and muscle relaxation. Risks include dependence, tolerance, withdrawal, and cognitive impairment. Short-term use is recommended. Alternatives (e.g., SSRIs) are preferred for chronic anxiety. Monitoring and gradual tapering reduce withdrawal risk.
""",
        key_factors=["receptor subtype", "clinical indication", "dependence risk", "withdrawal", "monitoring"],
        primary_authority=["FDA Drug Labeling", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Benzodiazepines are unsafe due to dependence and withdrawal.",
        counter_arguments=[
            "Short-term use and monitoring reduce risk.",
            "Alternatives are available for chronic therapy."
        ],
        resolution_strategy="Limit duration and monitor for dependence.",
        entity_scope="Patients with acute anxiety or insomnia",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FDA Drug Labeling"
    ),
    DoctrineBlock(
        topic="Antidepressant Agents",
        keywords=["antidepressant", "SSRI", "SNRI", "TCA", "MAOI", "depression"],
        conclusion_template="Antidepressants modulate neurotransmitter levels to treat depression, with efficacy and side effects varying by class.",
        reasoning_framework="""
Antidepressants include SSRIs, SNRIs, TCAs, and MAOIs. SSRIs (e.g., fluoxetine) increase serotonin, SNRIs (e.g., venlafaxine) affect serotonin and norepinephrine, TCAs block multiple neurotransmitters, and MAOIs inhibit monoamine breakdown. Efficacy is comparable, but side effect profiles differ. Risks include serotonin syndrome, withdrawal, and suicidality in young patients. Guidelines recommend individualized therapy and monitoring.
""",
        key_factors=["drug class", "mechanism of action", "side effects", "clinical indication", "monitoring"],
        primary_authority=["APA Depression Guidelines", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Antidepressants are ineffective and cause severe side effects.",
        counter_arguments=[
            "Efficacy is supported by clinical trials.",
            "Monitoring and patient education reduce risks."
        ],
        resolution_strategy="Select agent based on patient profile and monitor therapy.",
        entity_scope="Patients with depression",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="APA Depression Guidelines"
    ),
    DoctrineBlock(
        topic="Antipsychotic Agents",
        keywords=["antipsychotic", "dopamine antagonist", "schizophrenia", "typical", "atypical"],
        conclusion_template="Antipsychotics block dopamine receptors to treat psychosis, with efficacy and side effects varying by class.",
        reasoning_framework="""
Antipsychotics include typical (e.g., haloperidol) and atypical (e.g., risperidone) agents. Typical antipsychotics block D2 receptors, reducing positive symptoms of schizophrenia but causing extrapyramidal side effects. Atypical agents also affect serotonin receptors, improving negative symptoms and reducing motor side effects. Risks include metabolic syndrome, sedation, and QT prolongation. Guidelines recommend monitoring and individualized therapy.
""",
        key_factors=["drug class", "receptor profile", "side effects", "clinical indication", "monitoring"],
        primary_authority=["APA Schizophrenia Guidelines", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Antipsychotics cause severe metabolic and motor side effects.",
        counter_arguments=[
            "Atypical agents reduce motor risk.",
            "Monitoring and dose adjustment mitigate metabolic effects."
        ],
        resolution_strategy="Select agent based on patient profile and monitor therapy.",
        entity_scope="Patients with psychosis",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="APA Schizophrenia Guidelines"
    ),
    DoctrineBlock(
        topic="Antibiotic Mechanisms and Resistance",
        keywords=["antibiotic", "mechanism", "resistance", "bacterial", "penicillin", "MRSA"],
        conclusion_template="Antibiotics target bacterial processes but resistance arises via genetic and environmental factors.",
        reasoning_framework="""
Antibiotics inhibit bacterial cell wall synthesis, protein synthesis, nucleic acid synthesis, or metabolic pathways. Resistance develops through genetic mutations, horizontal gene transfer, and selective pressure from misuse. MRSA and ESBL-producing bacteria exemplify resistance challenges. Stewardship programs, susceptibility testing, and combination therapy are key strategies. Guidelines recommend targeted therapy based on culture and sensitivity.
""",
        key_factors=["mechanism of action", "resistance mechanism", "susceptibility testing", "stewardship", "combination therapy"],
        primary_authority=["CDC Antibiotic Stewardship Guidelines", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Antibiotic resistance renders therapy ineffective.",
        counter_arguments=[
            "Stewardship and targeted therapy preserve efficacy.",
            "New agents address resistant strains."
        ],
        resolution_strategy="Follow stewardship principles and monitor resistance patterns.",
        entity_scope="Patients with bacterial infections",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="CDC Antibiotic Stewardship Guidelines"
    ),
    DoctrineBlock(
        topic="Antiviral Agents",
        keywords=["antiviral", "mechanism", "resistance", "HIV", "influenza", "herpes"],
        conclusion_template="Antiviral agents inhibit viral replication, with efficacy limited by resistance and viral diversity.",
        reasoning_framework="""
Antivirals target viral entry, replication, or assembly. HIV therapy uses combination agents to prevent resistance. Influenza drugs inhibit neuraminidase or M2 protein. Herpes antivirals block DNA polymerase. Resistance arises from viral mutations and suboptimal therapy. Monitoring viral load and resistance testing guide therapy. Guidelines recommend combination and individualized therapy.
""",
        key_factors=["mechanism of action", "viral resistance", "combination therapy", "monitoring", "guideline recommendations"],
        primary_authority=["CDC HIV Guidelines", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Antiviral resistance limits clinical efficacy.",
        counter_arguments=[
            "Combination therapy reduces resistance.",
            "Monitoring and resistance testing optimize outcomes."
        ],
        resolution_strategy="Follow guidelines and monitor viral load.",
        entity_scope="Patients with viral infections",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="CDC HIV Guidelines"
    ),
    DoctrineBlock(
        topic="Non-Steroidal Anti-Inflammatory Drugs",
        keywords=["NSAID", "anti-inflammatory", "COX inhibitor", "ibuprofen", "GI toxicity"],
        conclusion_template="NSAIDs inhibit COX enzymes, reducing inflammation and pain but increasing GI and renal risk.",
        reasoning_framework="""
NSAIDs block cyclooxygenase (COX) enzymes, reducing prostaglandin synthesis. This alleviates pain and inflammation. Risks include gastrointestinal bleeding, renal impairment, and cardiovascular events. Selective COX-2 inhibitors (e.g., celecoxib) reduce GI risk but may increase cardiovascular risk. Guidelines recommend lowest effective dose and monitoring for adverse effects.
""",
        key_factors=["COX selectivity", "clinical indication", "GI risk", "renal risk", "monitoring"],
        primary_authority=["FDA Drug Labeling", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="NSAIDs cause unacceptable GI and renal toxicity.",
        counter_arguments=[
            "Risk mitigation strategies reduce adverse outcomes.",
            "Alternatives are available for high-risk patients."
        ],
        resolution_strategy="Use lowest effective dose and monitor for toxicity.",
        entity_scope="Patients with pain or inflammation",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FDA Drug Labeling"
    ),
    DoctrineBlock(
        topic="Corticosteroids and Glucocorticoid Therapy",
        keywords=["corticosteroid", "glucocorticoid", "anti-inflammatory", "immunosuppression", "prednisone"],
        conclusion_template="Corticosteroids suppress inflammation and immune responses but carry risks of metabolic and infectious complications.",
        reasoning_framework="""
Glucocorticoids bind to intracellular receptors, altering gene expression to suppress inflammation and immune activity. Clinical uses include autoimmune diseases, asthma, and allergic reactions. Risks include hyperglycemia, osteoporosis, infection, and adrenal suppression. Tapering is required to prevent withdrawal. Guidelines recommend lowest effective dose and monitoring for complications.
""",
        key_factors=["dose", "duration", "clinical indication", "adverse effects", "monitoring"],
        primary_authority=["FDA Drug Labeling", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Corticosteroids cause severe metabolic and infectious complications.",
        counter_arguments=[
            "Short-term use and monitoring reduce risk.",
            "Therapeutic benefits are substantial in acute settings."
        ],
        resolution_strategy="Limit duration, taper dose, and monitor for complications.",
        entity_scope="Patients requiring anti-inflammatory therapy",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FDA Drug Labeling"
    ),
    DoctrineBlock(
        topic="Insulin Therapy and Diabetes Management",
        keywords=["insulin", "diabetes", "glucose", "hypoglycemia", "HbA1c"],
        conclusion_template="Insulin therapy is essential for type 1 diabetes and advanced type 2, requiring individualized dosing and monitoring.",
        reasoning_framework="""
Insulin lowers blood glucose by promoting cellular uptake. Therapy is essential for type 1 diabetes and advanced type 2. Types include rapid, short, intermediate, and long-acting. Risks include hypoglycemia and weight gain. Dosing is individualized based on glucose monitoring and HbA1c targets. Guidelines recommend patient education, monitoring, and adjustment. Insulin analogs improve pharmacokinetics and reduce risk.
""",
        key_factors=["insulin type", "dosing", "glucose monitoring", "hypoglycemia risk", "patient education"],
        primary_authority=["ADA Diabetes Guidelines", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Insulin therapy is unsafe due to hypoglycemia.",
        counter_arguments=[
            "Patient education and monitoring reduce risk.",
            "Insulin is essential for glycemic control."
        ],
        resolution_strategy="Individualize dosing and monitor glucose.",
        entity_scope="Patients with diabetes",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="ADA Diabetes Guidelines"
    ),
    DoctrineBlock(
        topic="Chemotherapy Mechanisms and Toxicity",
        keywords=["chemotherapy", "mechanism", "toxicity", "cancer", "cytotoxic", "neutropenia"],
        conclusion_template="Chemotherapy targets rapidly dividing cells, causing cytotoxicity and adverse effects including neutropenia and organ toxicity.",
        reasoning_framework="""
Chemotherapeutic agents disrupt cell division via DNA damage, mitotic inhibition, or metabolic interference. Efficacy is limited by tumor resistance and toxicity to normal cells. Adverse effects include neutropenia, nausea, mucositis, and organ toxicity. Supportive care and dose adjustment mitigate risks. Guidelines recommend combination therapy and monitoring for toxicity.
""",
        key_factors=["mechanism of action", "tumor resistance", "adverse effects", "combination therapy", "monitoring"],
        primary_authority=["NCCN Cancer Guidelines", "FDA Drug Labeling"],
        burden_holder="Oncologist",
        adversary_position="Chemotherapy causes unacceptable toxicity.",
        counter_arguments=[
            "Supportive care and dose adjustment reduce risk.",
            "Therapeutic benefits outweigh risks in cancer patients."
        ],
        resolution_strategy="Individualize therapy and monitor for toxicity.",
        entity_scope="Patients with cancer",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="NCCN Cancer Guidelines"
    ),
    DoctrineBlock(
        topic="Pharmacogenomics and Individualized Therapy",
        keywords=["pharmacogenomics", "genetic polymorphism", "CYP450", "individualized therapy", "drug response"],
        conclusion_template="Pharmacogenomics enables individualized therapy by predicting drug response and adverse effects based on genetic profile.",
        reasoning_framework="""
Pharmacogenomics studies genetic variations affecting drug metabolism, efficacy, and toxicity. CYP450 polymorphisms (e.g., CYP2D6, CYP2C19) alter drug metabolism, requiring dose adjustment. Genetic testing improves prediction and reduces adverse events. Guidelines recommend testing for certain drugs (e.g., warfarin, clopidogrel). Individualized therapy optimizes outcomes and minimizes risk.
""",
        key_factors=["genetic polymorphism", "drug metabolism", "clinical indication", "testing", "dose adjustment"],
        primary_authority=["FDA Pharmacogenomics Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Pharmacogenomics is too costly and complex for routine use.",
        counter_arguments=[
            "Testing is increasingly accessible.",
            "Clinical benefits justify cost in selected patients."
        ],
        resolution_strategy="Apply pharmacogenomic testing for high-risk drugs and patients.",
        entity_scope="Patients with genetic variability affecting drug response",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FDA Pharmacogenomics Guidance"
    ),
    DoctrineBlock(
        topic="Adverse Drug Reactions Classification",
        keywords=["adverse drug reaction", "ADR", "type A", "type B", "toxicity", "idiosyncratic"],
        conclusion_template="Adverse drug reactions are classified as predictable (type A) or unpredictable (type B), guiding risk mitigation.",
        reasoning_framework="""
ADRs are divided into type A (predictable, dose-dependent) and type B (unpredictable, idiosyncratic). Type A reactions include toxicity and side effects, while type B includes allergic and idiosyncratic responses. Risk factors include age, comorbidities, and genetic variability. Reporting and monitoring are essential for detection and prevention. Guidelines recommend risk assessment and mitigation strategies.
""",
        key_factors=["reaction type", "dose-dependency", "patient risk factors", "monitoring", "reporting"],
        primary_authority=["FDA Adverse Event Reporting Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="ADRs are unavoidable and unpredictable.",
        counter_arguments=[
            "Risk assessment and monitoring reduce incidence.",
            "Reporting improves detection and prevention."
        ],
        resolution_strategy="Classify reaction, assess risk, and implement mitigation strategies.",
        entity_scope="All drug recipients",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FDA Adverse Event Reporting Guidance"
    ),
    DoctrineBlock(
        topic="Controlled Substance Scheduling and Regulation",
        keywords=["controlled substance", "scheduling", "DEA", "regulation", "abuse potential"],
        conclusion_template="Controlled substances are regulated by scheduling based on abuse potential, medical use, and safety.",
        reasoning_framework="""
Controlled substances are classified into schedules (I-V) by the DEA based on abuse potential, accepted medical use, and safety. Schedule I drugs have no accepted medical use and high abuse risk. Schedules II-V have decreasing abuse potential and increasing medical use. Prescribing and dispensing are regulated to prevent misuse. Guidelines require documentation, monitoring, and compliance with regulations.
""",
        key_factors=["schedule", "abuse potential", "medical use", "regulation", "monitoring"],
        primary_authority=["DEA Controlled Substance Act", "FDA Drug Labeling"],
        burden_holder="Prescriber",
        adversary_position="Controlled substance regulation restricts access to needed therapy.",
        counter_arguments=[
            "Regulation balances access and abuse prevention.",
            "Exceptions are available for medical necessity."
        ],
        resolution_strategy="Comply with regulations and document medical necessity.",
        entity_scope="Controlled substance prescribers and recipients",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="DEA Controlled Substance Act"
    ),
    DoctrineBlock(
        topic="Pediatric and Geriatric Pharmacology",
        keywords=["pediatric", "geriatric", "pharmacology", "dose adjustment", "organ function", "age"],
        conclusion_template="Drug therapy in pediatric and geriatric patients requires dose adjustment and monitoring due to age-related pharmacokinetic changes.",
        reasoning_framework="""
Children and elderly patients exhibit altered pharmacokinetics due to organ immaturity or decline. Pediatric dosing is based on weight or surface area, while geriatric dosing considers renal, hepatic, and cognitive function. Risks include toxicity, underdosing, and drug interactions. Guidelines recommend individualized dosing and monitoring for adverse effects.
""",
        key_factors=["age", "organ function", "dose adjustment", "adverse effects", "monitoring"],
        primary_authority=["FDA Pediatric and Geriatric Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Age-related changes make drug therapy unsafe.",
        counter_arguments=[
            "Individualized dosing and monitoring reduce risk.",
            "Guidelines provide dosing recommendations."
        ],
        resolution_strategy="Adjust dose based on age and organ function, monitor therapy.",
        entity_scope="Pediatric and geriatric patients",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FDA Pediatric and Geriatric Guidance"
    ),
    DoctrineBlock(
        topic="Drug Formulation and Delivery Systems",
        keywords=["formulation", "delivery system", "extended-release", "bioavailability", "pharmacokinetics"],
        conclusion_template="Drug formulation and delivery systems optimize pharmacokinetics, adherence, and therapeutic outcomes.",
        reasoning_framework="""
Formulation affects drug stability, absorption, and bioavailability. Delivery systems (e.g., extended-release, transdermal, inhaled) improve adherence and therapeutic outcomes. Extended-release formulations provide steady plasma concentrations. Transdermal systems bypass GI tract and first-pass metabolism. Selection depends on clinical indication, patient preference, and pharmacokinetic profile.
""",
        key_factors=["formulation type", "delivery system", "bioavailability", "adherence", "clinical indication"],
        primary_authority=["FDA Drug Labeling", "Goodman & Gilman's"],
        burden_holder="Pharmacologist",
        adversary_position="Complex formulations increase risk of dosing errors.",
        counter_arguments=[
            "Patient education reduces errors.",
            "Benefits outweigh risks in selected patients."
        ],
        resolution_strategy="Select formulation based on patient needs and educate on proper use.",
        entity_scope="All drug recipients",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FDA Drug Labeling"
    ),
    DoctrineBlock(
        topic="Drug Stability and Storage",
        keywords=["drug stability", "storage", "expiration", "degradation", "temperature"],
        conclusion_template="Proper storage and stability are essential to maintain drug efficacy and safety.",
        reasoning_framework="""
Drug stability depends on formulation, temperature, humidity, and light exposure. Improper storage leads to degradation, loss of efficacy, and potential toxicity. Expiration dates are based on stability testing. Guidelines recommend storage at specified temperature and protection from moisture and light. Pharmacists ensure proper storage and educate patients.
""",
        key_factors=["formulation", "temperature", "humidity", "light", "expiration"],
        primary_authority=["USP Drug Storage Standards", "FDA Drug Labeling"],
        burden_holder="Pharmacist",
        adversary_position="Drug degradation is unavoidable and compromises therapy.",
        counter_arguments=[
            "Proper storage preserves stability.",
            "Expiration dates are based on rigorous testing."
        ],
        resolution_strategy="Follow storage guidelines and monitor for degradation.",
        entity_scope="All drug recipients",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="USP Drug Storage Standards"
    ),
    DoctrineBlock(
        topic="Drug Allergies and Hypersensitivity Reactions",
        keywords=["drug allergy", "hypersensitivity", "immune response", "anaphylaxis", "rash"],
        conclusion_template="Drug allergies are immune-mediated and require avoidance and alternative therapy.",
        reasoning_framework="""
Drug allergies involve immune responses (IgE-mediated, delayed hypersensitivity) leading to rash, anaphylaxis, or organ involvement. Risk factors include prior exposure, genetic predisposition, and drug structure. Diagnosis is based on history, testing, and exclusion of other causes. Management involves avoidance, alternative therapy, and emergency treatment for anaphylaxis.
""",
        key_factors=["immune mechanism", "clinical presentation", "diagnosis", "management", "alternative therapy"],
        primary_authority=["FDA Drug Labeling", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Drug allergies cannot be reliably diagnosed or prevented.",
        counter_arguments=[
            "History and testing improve diagnosis.",
            "Alternative therapies are available."
        ],
        resolution_strategy="Avoid offending drug and provide alternatives.",
        entity_scope="All drug recipients",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FDA Drug Labeling"
    ),
    DoctrineBlock(
        topic="Drug Approval and Post-Marketing Surveillance",
        keywords=["drug approval", "FDA", "clinical trial", "post-marketing", "surveillance"],
        conclusion_template="Drug approval requires clinical trials and ongoing post-marketing surveillance for safety and efficacy.",
        reasoning_framework="""
FDA approval is based on preclinical and clinical trial data demonstrating safety and efficacy. Post-marketing surveillance detects rare adverse events and long-term outcomes. Reporting systems (e.g., MedWatch) and registries monitor drug safety. Regulatory actions include labeling changes, warnings, or withdrawal. Continuous evaluation ensures public safety.
""",
        key_factors=["clinical trial data", "post-marketing surveillance", "adverse event reporting", "regulatory action", "public safety"],
        primary_authority=["FDA Drug Approval Guidance", "Goodman & Gilman's"],
        burden_holder="Regulatory authority",
        adversary_position="Post-marketing surveillance is insufficient to detect rare events.",
        counter_arguments=[
            "Reporting systems improve detection.",
            "Regulatory actions address safety concerns."
        ],
        resolution_strategy="Enhance surveillance and respond to safety signals.",
        entity_scope="All approved drugs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FDA Drug Approval Guidance"
    ),
    DoctrineBlock(
        topic="Drug Labeling and Patient Education",
        keywords=["drug labeling", "patient education", "FDA", "adherence", "safety"],
        conclusion_template="Accurate drug labeling and patient education are essential for safe and effective therapy.",
        reasoning_framework="""
Drug labeling provides essential information on indication, dosing, adverse effects, and contraindications. Patient education improves adherence, reduces errors, and enhances outcomes. FDA requires clear labeling and risk communication. Pharmacists and prescribers play key roles in educating patients and monitoring therapy.
""",
        key_factors=["labeling accuracy", "patient education", "adherence", "risk communication", "monitoring"],
        primary_authority=["FDA Drug Labeling Guidance", "Goodman & Gilman's"],
        burden_holder="Pharmacist",
        adversary_position="Labeling and education are insufficient for safe therapy.",
        counter_arguments=[
            "Education programs improve outcomes.",
            "Labeling is continuously updated for accuracy."
        ],
        resolution_strategy="Provide comprehensive education and monitor adherence.",
        entity_scope="All drug recipients",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FDA Drug Labeling Guidance"
    ),
    DoctrineBlock(
        topic="Drug Recall and Withdrawal Procedures",
        keywords=["drug recall", "withdrawal", "FDA", "safety", "adverse event"],
        conclusion_template="Drug recall and withdrawal procedures protect public safety by removing unsafe products from the market.",
        reasoning_framework="""
Recalls are initiated for safety, efficacy, or quality concerns. FDA and manufacturers coordinate recall procedures, including notification, removal, and follow-up. Withdrawals occur for severe adverse events or lack of efficacy. Public communication and monitoring ensure compliance. Guidelines require prompt action and reporting.
""",
        key_factors=["recall procedure", "withdrawal criteria", "notification", "public safety", "regulatory compliance"],
        primary_authority=["FDA Recall Guidance", "Goodman & Gilman's"],
        burden_holder="Regulatory authority",
        adversary_position="Recall procedures are slow and ineffective.",
        counter_arguments=[
            "Guidelines ensure prompt action.",
            "Public communication improves compliance."
        ],
        resolution_strategy="Follow recall procedures and monitor outcomes.",
        entity_scope="All drug recipients",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FDA Recall Guidance"
    ),
    DoctrineBlock(
        topic="Drug Pricing and Access",
        keywords=["drug pricing", "access", "insurance", "cost", "generic"],
        conclusion_template="Drug pricing and access are influenced by market, regulation, and insurance, affecting patient outcomes.",
        reasoning_framework="""
Pricing is determined by market forces, patent status, and regulation. Access depends on insurance coverage, formulary status, and generics. High prices limit access and adherence. Regulation and negotiation aim to improve affordability. Guidelines recommend prescribing generics and considering patient cost.
""",
        key_factors=["pricing", "access", "insurance", "generic availability", "regulation"],
        primary_authority=["FDA Drug Pricing Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="High prices prevent access to essential drugs.",
        counter_arguments=[
            "Generics and insurance improve access.",
            "Regulation addresses affordability."
        ],
        resolution_strategy="Prescribe generics and assist with access programs.",
        entity_scope="All drug recipients",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FDA Drug Pricing Guidance"
    ),
    DoctrineBlock(
        topic="Drug Interaction Databases and Clinical Decision Support",
        keywords=["drug interaction", "database", "clinical decision support", "electronic health record", "safety"],
        conclusion_template="Drug interaction databases and clinical decision support systems enhance safety by identifying and managing interactions.",
        reasoning_framework="""
Databases provide comprehensive information on drug-drug, drug-food, and drug-disease interactions. Clinical decision support integrates with electronic health records to alert prescribers. Limitations include alert fatigue and incomplete data. Guidelines recommend using databases and support systems to improve safety and outcomes.
""",
        key_factors=["database accuracy", "clinical decision support", "alert fatigue", "integration", "safety"],
        primary_authority=["FDA Drug Interaction Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Databases are unreliable and cause alert fatigue.",
        counter_arguments=[
            "Integration and customization improve utility.",
            "Databases are continuously updated."
        ],
        resolution_strategy="Use databases judiciously and customize alerts.",
        entity_scope="All drug recipients",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FDA Drug Interaction Guidance"
    ),
    DoctrineBlock(
        topic="Drug Administration Routes and Techniques",
        keywords=["administration route", "oral", "parenteral", "topical", "inhaled", "bioavailability"],
        conclusion_template="Drug administration routes and techniques affect bioavailability, onset, and patient adherence.",
        reasoning_framework="""
Routes include oral, parenteral (IV, IM, SC), topical, inhaled, and transdermal. Each route affects absorption, onset, and bioavailability. Selection depends on clinical indication, patient preference, and drug properties. Proper technique reduces errors and improves outcomes. Guidelines recommend route selection based on efficacy and safety.
""",
        key_factors=["route", "technique", "bioavailability", "onset", "adherence"],
        primary_authority=["FDA Drug Labeling", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Complex routes increase risk of error and reduce adherence.",
        counter_arguments=[
            "Patient education improves technique and adherence.",
            "Route selection is based on clinical need."
        ],
        resolution_strategy="Educate patients and select optimal route.",
        entity_scope="All drug recipients",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FDA Drug Labeling"
    ),
    DoctrineBlock(
        topic="Drug Compounding and Custom Formulations",
        keywords=["compounding", "custom formulation", "pharmacist", "regulation", "safety"],
        conclusion_template="Compounding allows custom formulations for patient needs but requires strict regulation and quality control.",
        reasoning_framework="""
Compounding involves preparing custom drug formulations for patients with unique needs (e.g., allergies, pediatric dosing). Risks include contamination, dosing errors, and lack of standardization. Regulation and quality control are essential. Guidelines require documentation, labeling, and monitoring for safety.
""",
        key_factors=["compounding procedure", "regulation", "quality control", "patient need", "safety"],
        primary_authority=["USP Compounding Standards", "FDA Drug Labeling"],
        burden_holder="Pharmacist",
        adversary_position="Compounding increases risk of contamination and error.",
        counter_arguments=[
            "Regulation and quality control mitigate risks.",
            "Compounding is essential for unique patient needs."
        ],
        resolution_strategy="Follow standards and monitor for safety.",
        entity_scope="Patients requiring custom formulations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="USP Compounding Standards"
    ),
    DoctrineBlock(
        topic="Drug Patent and Exclusivity",
        keywords=["patent", "exclusivity", "generic", "FDA", "market"],
        conclusion_template="Drug patents and exclusivity protect innovation but delay generic entry and affect pricing.",
        reasoning_framework="""
Patents grant exclusive marketing rights for new drugs, incentivizing innovation. FDA exclusivity periods further protect products. Generic entry reduces prices and increases access. Regulation balances innovation and affordability. Guidelines recommend prescribing generics when available.
""",
        key_factors=["patent status", "exclusivity", "generic availability", "pricing", "regulation"],
        primary_authority=["FDA Patent Guidance", "Goodman & Gilman's"],
        burden_holder="Manufacturer",
        adversary_position="Patents delay access to affordable generics.",
        counter_arguments=[
            "Exclusivity incentivizes innovation.",
            "Regulation ensures eventual generic entry."
        ],
        resolution_strategy="Prescribe generics when available and monitor patent status.",
        entity_scope="All drug recipients",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FDA Patent Guidance"
    ),
    DoctrineBlock(
        topic="Drug Shortages and Supply Chain Management",
        keywords=["drug shortage", "supply chain", "distribution", "FDA", "access"],
        conclusion_template="Drug shortages impact therapy and require supply chain management and regulatory intervention.",
        reasoning_framework="""
Shortages arise from manufacturing issues, distribution problems, and regulatory actions. FDA monitors shortages and coordinates response. Supply chain management ensures distribution and access. Guidelines recommend alternative therapy and communication with stakeholders.
""",
        key_factors=["shortage cause", "supply chain", "regulation", "alternative therapy", "communication"],
        primary_authority=["FDA Drug Shortage Guidance", "Goodman & Gilman's"],
        burden_holder="Manufacturer",
        adversary_position="Shortages compromise patient care and outcomes.",
        counter_arguments=[
            "Regulatory intervention and supply chain management mitigate impact.",
            "Alternative therapies are available."
        ],
        resolution_strategy="Monitor shortages and communicate alternatives.",
        entity_scope="All drug recipients",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FDA Drug Shortage Guidance"
    ),
    DoctrineBlock(
        topic="Drug Environmental Impact and Disposal",
        keywords=["environmental impact", "drug disposal", "waste", "regulation", "water contamination"],
        conclusion_template="Proper drug disposal reduces environmental impact and prevents contamination.",
        reasoning_framework="""
Improper disposal leads to environmental contamination and public health risk. Guidelines recommend take-back programs, incineration, and avoidance of flushing. Regulation ensures safe disposal and monitoring. Education reduces improper disposal and environmental harm.
""",
        key_factors=["disposal method", "regulation", "environmental impact", "education", "monitoring"],
        primary_authority=["FDA Drug Disposal Guidance", "EPA Guidelines"],
        burden_holder="Pharmacist",
        adversary_position="Disposal guidelines are ineffective and environmental harm persists.",
        counter_arguments=[
            "Education and regulation improve compliance.",
            "Take-back programs reduce contamination."
        ],
        resolution_strategy="Follow disposal guidelines and educate patients.",
        entity_scope="All drug recipients",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FDA Drug Disposal Guidance"
    ),
    DoctrineBlock(
        topic="Drug Safety in Pregnancy and Lactation",
        keywords=["pregnancy", "lactation", "drug safety", "teratogenicity", "FDA"],
        conclusion_template="Drug safety in pregnancy and lactation requires risk assessment and avoidance of teratogenic agents.",
        reasoning_framework="""
Drugs may cross placenta or enter breast milk, affecting fetus or infant. Teratogenicity is a major concern. FDA labeling provides risk categories. Risk assessment and alternative therapy are recommended. Monitoring and patient education reduce adverse outcomes.
""",
        key_factors=["teratogenicity", "placental transfer", "breast milk", "risk assessment", "education"],
        primary_authority=["FDA Pregnancy and Lactation Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="Drug therapy is unsafe in pregnancy and lactation.",
        counter_arguments=[
            "Risk assessment and alternative therapy reduce risk.",
            "Labeling provides essential information."
        ],
        resolution_strategy="Avoid teratogenic drugs and educate patients.",
        entity_scope="Pregnant and lactating patients",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FDA Pregnancy and Lactation Guidance"
    ),
    DoctrineBlock(
        topic="Drug Therapeutic Drug Monitoring",
        keywords=["therapeutic drug monitoring", "TDM", "plasma concentration", "narrow therapeutic window", "safety"],
        conclusion_template="Therapeutic drug monitoring optimizes efficacy and safety for drugs with narrow therapeutic windows.",
        reasoning_framework="""
TDM measures plasma concentrations to guide dosing for drugs with narrow therapeutic windows (e.g., digoxin, lithium). Monitoring prevents toxicity and ensures efficacy. Guidelines recommend TDM for high-risk drugs. Interpretation requires understanding of pharmacokinetics and patient factors.
""",
        key_factors=["drug", "therapeutic window", "monitoring", "pharmacokinetics", "patient factors"],
        primary_authority=["FDA Therapeutic Drug Monitoring Guidance", "Goodman & Gilman's"],
        burden_holder="Prescriber",
        adversary_position="TDM is unnecessary and costly.",
        counter_arguments=[
            "TDM improves safety and outcomes.",
            "Guidelines recommend TDM for high-risk drugs."
        ],
        resolution_strategy="Apply TDM for selected drugs and interpret results.",
        entity_scope="Patients receiving high-risk drugs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FDA Therapeutic Drug Monitoring Guidance"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    results = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]