from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MODERATE = "Moderate"
    LOW = "Low"

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
        topic="dose_response_relationships",
        keywords=["dose", "response", "toxicity", "threshold", "LD50", "NOAEL", "risk assessment"],
        conclusion_template="The observed toxic effect is proportional to the dose administered, with a threshold below which no adverse effect is expected.",
        reasoning_framework="""
        Dose-response relationships are fundamental in toxicology, describing how the magnitude of exposure to a substance relates to the severity of the effect. The relationship is often sigmoidal, with a threshold (NOAEL) below which no effect is observed. The LD50 is used to compare acute toxicity. Risk assessments rely on extrapolation from animal studies to humans, considering interspecies variability and sensitive populations. The slope of the response curve informs regulatory limits. Exceptions exist for non-threshold carcinogens and idiosyncratic reactions. The doctrine emphasizes empirical data, statistical modeling, and regulatory guidance.
        """,
        key_factors=["Dose", "Duration", "Route of exposure", "Population sensitivity", "Chemical properties"],
        primary_authority=["EPA", "WHO", "OECD", "FDA"],
        burden_holder="Regulatory agency",
        adversary_position="Industry argues for higher thresholds based on limited human data.",
        counter_arguments=[
            "Human variability may be underestimated.",
            "Animal data may not extrapolate accurately.",
            "Chronic effects may occur below threshold."
        ],
        resolution_strategy="Apply conservative safety factors and require post-market surveillance.",
        entity_scope="Chemical substances, pharmaceuticals, environmental toxins",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Risk Assessment Guidelines (2019)"
    ),
    DoctrineBlock(
        topic="heavy_metal_poisoning_lead",
        keywords=["lead", "heavy metals", "poisoning", "blood lead level", "neurotoxicity", "chelators"],
        conclusion_template="Lead exposure above regulatory thresholds results in neurotoxicity, hematologic effects, and requires intervention.",
        reasoning_framework="""
        Lead is a cumulative toxicant affecting multiple organ systems, especially the nervous system. Blood lead levels above 5 µg/dL in children are associated with cognitive deficits. Chelation therapy is indicated for symptomatic patients or those with levels exceeding 45 µg/dL. Regulatory standards (OSHA, CDC) set occupational and environmental limits. The doctrine integrates epidemiological evidence, mechanistic studies, and clinical guidelines. Adversaries may argue for higher thresholds citing economic impact, but public health evidence prevails. The doctrine mandates environmental remediation and ongoing surveillance.
        """,
        key_factors=["Blood lead level", "Age", "Duration of exposure", "Clinical symptoms", "Source of exposure"],
        primary_authority=["CDC", "OSHA", "WHO", "AAP"],
        burden_holder="Employer or public health authority",
        adversary_position="Industry disputes low-level toxicity and remediation costs.",
        counter_arguments=[
            "Economic impact does not outweigh health risks.",
            "No safe threshold for children.",
            "Long-term effects persist after exposure ends."
        ],
        resolution_strategy="Enforce strict limits, provide chelation, and mandate remediation.",
        entity_scope="Children, workers, general population",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Blood Lead Reference Value (2021)"
    ),
    DoctrineBlock(
        topic="organophosphate_poisoning",
        keywords=["organophosphate", "cholinesterase inhibition", "pesticides", "acute toxicity", "atropine", "pralidoxime"],
        conclusion_template="Organophosphate poisoning is diagnosed by cholinesterase inhibition and treated with atropine and pralidoxime.",
        reasoning_framework="""
        Organophosphates irreversibly inhibit acetylcholinesterase, leading to cholinergic crisis. Diagnosis is clinical, supported by decreased plasma cholinesterase activity. Immediate treatment with atropine (antimuscarinic) and pralidoxime (reactivates enzyme) is essential. Regulatory doctrine emphasizes rapid identification, decontamination, and supportive care. Occupational exposure limits are set by EPA and OSHA. Adversaries may argue for less stringent controls, but acute toxicity and fatal outcomes justify strict regulation. Surveillance and education are mandated for at-risk populations.
        """,
        key_factors=["Cholinesterase activity", "Clinical symptoms", "Exposure history", "Timeliness of intervention"],
        primary_authority=["EPA", "OSHA", "WHO", "CDC"],
        burden_holder="Employer or healthcare provider",
        adversary_position="Agricultural industry resists stricter regulation.",
        counter_arguments=[
            "Economic necessity does not justify health risk.",
            "Alternative pesticides exist.",
            "Delayed intervention increases mortality."
        ],
        resolution_strategy="Mandate PPE, training, and emergency protocols.",
        entity_scope="Agricultural workers, emergency responders",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="WHO Organophosphate Poisoning Guidelines (2017)"
    ),
    DoctrineBlock(
        topic="acetaminophen_overdose",
        keywords=["acetaminophen", "paracetamol", "overdose", "hepatotoxicity", "N-acetylcysteine", "liver failure"],
        conclusion_template="Acetaminophen overdose is managed by early administration of N-acetylcysteine based on serum levels and time since ingestion.",
        reasoning_framework="""
        Acetaminophen is metabolized to a toxic intermediate (NAPQI) when glutathione is depleted. The Rumack-Matthew nomogram guides treatment based on serum levels and time post-ingestion. N-acetylcysteine replenishes glutathione and prevents liver injury. The doctrine emphasizes early intervention, accurate history, and risk stratification. Adversaries may argue for observation only in low-risk cases, but delayed treatment increases morbidity. Regulatory guidance prioritizes patient safety and mandates reporting of intentional overdoses.
        """,
        key_factors=["Serum acetaminophen level", "Time since ingestion", "Clinical symptoms", "Liver function tests"],
        primary_authority=["FDA", "AAPCC", "WHO", "ACMT"],
        burden_holder="Healthcare provider",
        adversary_position="Some clinicians advocate for less aggressive treatment.",
        counter_arguments=[
            "Delayed NAC increases risk of liver failure.",
            "Nomogram is validated for single acute ingestion.",
            "Chronic overdose requires clinical judgment."
        ],
        resolution_strategy="Follow nomogram, err on side of early NAC administration.",
        entity_scope="Emergency departments, poison centers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FDA Acetaminophen Overdose Guidance (2020)"
    ),
    DoctrineBlock(
        topic="opioid_toxicity_naloxone",
        keywords=["opioid", "toxicity", "naloxone", "respiratory depression", "overdose", "antagonist"],
        conclusion_template="Opioid toxicity is reversed by naloxone administration, with monitoring for recurrence due to long-acting opioids.",
        reasoning_framework="""
        Opioid overdose causes respiratory depression and can be fatal. Naloxone is a competitive antagonist at opioid receptors, rapidly reversing toxicity. The doctrine mandates immediate administration, titration to respiratory effort, and observation for recurrence, especially with long-acting opioids. Harm reduction strategies include public access to naloxone and education. Adversaries may argue for restricted access, but public health evidence supports widespread availability. Surveillance and follow-up are required for recurrent toxicity and withdrawal.
        """,
        key_factors=["Respiratory rate", "Level of consciousness", "Type of opioid", "Naloxone dose", "Duration of action"],
        primary_authority=["CDC", "FDA", "SAMHSA", "WHO"],
        burden_holder="Healthcare provider or first responder",
        adversary_position="Some policymakers oppose public naloxone distribution.",
        counter_arguments=[
            "Naloxone saves lives and does not encourage misuse.",
            "Long-acting opioids require extended monitoring.",
            "Withdrawal is preferable to fatality."
        ],
        resolution_strategy="Mandate naloxone access and training.",
        entity_scope="Emergency responders, community programs",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Opioid Overdose Prevention Guidelines (2018)"
    ),
    DoctrineBlock(
        topic="carbon_monoxide_poisoning",
        keywords=["carbon monoxide", "CO", "poisoning", "hypoxia", "carboxyhemoglobin", "hyperbaric oxygen"],
        conclusion_template="Carbon monoxide poisoning is diagnosed by elevated carboxyhemoglobin and treated with high-flow oxygen or hyperbaric therapy.",
        reasoning_framework="""
        Carbon monoxide binds hemoglobin with high affinity, causing tissue hypoxia. Diagnosis is based on history, symptoms, and carboxyhemoglobin levels. High-flow oxygen reduces half-life of CO; hyperbaric oxygen is indicated for severe cases. Regulatory doctrine emphasizes prevention via detectors and education. Adversaries may argue hyperbaric therapy is unnecessary, but evidence supports its use in neurological symptoms and pregnant patients. Surveillance and reporting are mandated for public health.
        """,
        key_factors=["Carboxyhemoglobin level", "Clinical symptoms", "Exposure history", "Pregnancy status"],
        primary_authority=["CDC", "NIOSH", "WHO", "FDA"],
        burden_holder="Healthcare provider",
        adversary_position="Some clinicians question hyperbaric oxygen indications.",
        counter_arguments=[
            "Neurological sequelae justify aggressive treatment.",
            "Pregnant patients require lower threshold.",
            "Delayed therapy increases morbidity."
        ],
        resolution_strategy="Follow evidence-based indications for hyperbaric therapy.",
        entity_scope="Emergency departments, occupational settings",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIOSH Carbon Monoxide Poisoning Guidelines (2019)"
    ),
    DoctrineBlock(
        topic="cyanide_poisoning",
        keywords=["cyanide", "poisoning", "antidote", "hydroxocobalamin", "nitrites", "thiosulfate"],
        conclusion_template="Cyanide poisoning is treated with hydroxocobalamin or nitrite/thiosulfate based on clinical severity and exposure type.",
        reasoning_framework="""
        Cyanide inhibits cellular respiration by binding cytochrome oxidase. Rapid diagnosis and treatment are critical. Hydroxocobalamin is preferred due to safety and efficacy; nitrite/thiosulfate is used when hydroxocobalamin is unavailable. Doctrine emphasizes clinical suspicion, rapid intervention, and supportive care. Adversaries may argue for limited antidote stockpiling, but mass casualty scenarios justify preparedness. Regulatory guidance mandates antidote availability in high-risk industries and emergency services.
        """,
        key_factors=["Exposure history", "Clinical severity", "Antidote availability", "Time to intervention"],
        primary_authority=["CDC", "FDA", "WHO", "NIOSH"],
        burden_holder="Healthcare provider or employer",
        adversary_position="Cost concerns limit antidote stockpiling.",
        counter_arguments=[
            "Mass casualty risk outweighs cost.",
            "Hydroxocobalamin is safer than nitrites.",
            "Delayed treatment increases mortality."
        ],
        resolution_strategy="Mandate antidote stockpiling and training.",
        entity_scope="Fire departments, chemical industries",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Cyanide Poisoning Guidelines (2016)"
    ),
    DoctrineBlock(
        topic="methanol_ethylene_glycol_poisoning",
        keywords=["methanol", "ethylene glycol", "poisoning", "fomepizole", "ethanol", "dialysis", "anion gap"],
        conclusion_template="Methanol and ethylene glycol poisoning are managed by inhibition of alcohol dehydrogenase and dialysis for severe cases.",
        reasoning_framework="""
        Methanol and ethylene glycol are metabolized to toxic acids causing metabolic acidosis and organ damage. Diagnosis relies on history, anion gap, and osmolar gap. Fomepizole or ethanol inhibits metabolism; dialysis removes toxins in severe cases. Doctrine emphasizes early intervention, laboratory confirmation, and risk stratification. Adversaries may argue for observation in mild cases, but delayed treatment increases morbidity. Regulatory guidance mandates antidote availability and reporting.
        """,
        key_factors=["Anion gap", "Osmolar gap", "Clinical severity", "Time since ingestion", "Antidote availability"],
        primary_authority=["FDA", "CDC", "WHO", "ACMT"],
        burden_holder="Healthcare provider",
        adversary_position="Some clinicians advocate for observation only.",
        counter_arguments=[
            "Delayed antidote increases risk of organ damage.",
            "Dialysis is life-saving in severe cases.",
            "Early intervention improves outcomes."
        ],
        resolution_strategy="Follow evidence-based protocols for antidote and dialysis.",
        entity_scope="Emergency departments, poison centers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FDA Methanol/Ethylene Glycol Poisoning Guidance (2017)"
    ),
    DoctrineBlock(
        topic="occupational_exposure_limits",
        keywords=["occupational", "exposure limits", "OSHA", "NIOSH", "threshold limit value", "PEL", "TLV"],
        conclusion_template="Occupational exposure limits are set to prevent adverse health effects and must be enforced by employers.",
        reasoning_framework="""
        Occupational exposure limits (OELs) are established to protect workers from hazardous substances. Limits include PELs (OSHA), TLVs (ACGIH), and RELs (NIOSH). Doctrine emphasizes risk assessment, monitoring, and enforcement. Adversaries may argue for higher limits based on economic impact, but worker safety prevails. Regulatory guidance mandates periodic review, exposure monitoring, and worker education. Surveillance and reporting are required for compliance.
        """,
        key_factors=["Substance toxicity", "Duration of exposure", "Worker population", "Regulatory standards"],
        primary_authority=["OSHA", "NIOSH", "ACGIH", "EPA"],
        burden_holder="Employer",
        adversary_position="Industry argues for less stringent limits.",
        counter_arguments=[
            "Worker health outweighs economic arguments.",
            "Chronic effects may occur below threshold.",
            "Periodic review ensures limits remain protective."
        ],
        resolution_strategy="Mandate compliance, periodic review, and worker education.",
        entity_scope="Industrial workplaces, laboratories",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Occupational Exposure Limits (2022)"
    ),
    DoctrineBlock(
        topic="carcinogenicity_classification",
        keywords=["carcinogenicity", "classification", "IARC", "EPA", "Group 1", "Group 2A", "Group 2B"],
        conclusion_template="Substances are classified by carcinogenic potential based on epidemiological and mechanistic evidence.",
        reasoning_framework="""
        Carcinogenicity classification relies on human and animal studies, mechanistic data, and regulatory guidance. IARC groups substances as Group 1 (carcinogenic), Group 2A (probably carcinogenic), Group 2B (possibly carcinogenic), etc. Doctrine emphasizes weight of evidence, peer review, and transparency. Adversaries may dispute classification based on economic impact or limited data, but precautionary principle prevails. Regulatory mandates include labeling, exposure reduction, and surveillance.
        """,
        key_factors=["Epidemiological evidence", "Animal studies", "Mechanistic data", "Regulatory guidance"],
        primary_authority=["IARC", "EPA", "FDA", "WHO"],
        burden_holder="Regulatory agency",
        adversary_position="Industry disputes classification based on limited evidence.",
        counter_arguments=[
            "Precautionary principle applies.",
            "Mechanistic data supports classification.",
            "Peer review ensures validity."
        ],
        resolution_strategy="Mandate labeling, exposure reduction, and ongoing review.",
        entity_scope="Chemical manufacturers, regulatory agencies",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IARC Monographs (2021)"
    ),
    DoctrineBlock(
        topic="snake_envenomation_crotalidae",
        keywords=["snakebite", "envenomation", "crotalidae", "antivenom", "coagulopathy", "compartment syndrome"],
        conclusion_template="Crotalidae envenomation is managed by antivenom administration, monitoring for coagulopathy and compartment syndrome.",
        reasoning_framework="""
        Crotalidae (pit viper) envenomation causes local tissue injury, coagulopathy, and systemic toxicity. Antivenom is indicated for progressive symptoms, coagulopathy, or systemic effects. Doctrine emphasizes rapid transport, clinical assessment, and avoidance of harmful interventions (tourniquets, incision). Adversaries may argue for observation only, but evidence supports early antivenom in severe cases. Regulatory guidance mandates antivenom availability and training.
        """,
        key_factors=["Severity of symptoms", "Coagulopathy", "Time since bite", "Antivenom availability"],
        primary_authority=["CDC", "WHO", "FDA", "ACMT"],
        burden_holder="Healthcare provider",
        adversary_position="Some clinicians advocate for observation only.",
        counter_arguments=[
            "Delayed antivenom increases morbidity.",
            "Compartment syndrome requires surgical intervention.",
            "Antivenom is safe and effective."
        ],
        resolution_strategy="Follow evidence-based protocols for antivenom and monitoring.",
        entity_scope="Emergency departments, rural clinics",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Snakebite Management Guidelines (2018)"
    ),
    DoctrineBlock(
        topic="lithium_toxicity",
        keywords=["lithium", "toxicity", "therapeutic drug monitoring", "renal function", "dialysis", "neurotoxicity"],
        conclusion_template="Lithium toxicity is managed by discontinuation, supportive care, and dialysis for severe cases.",
        reasoning_framework="""
        Lithium toxicity results from overdose or impaired renal clearance. Symptoms include neurotoxicity, GI upset, and renal dysfunction. Therapeutic drug monitoring guides management; levels >2.5 mmol/L or severe symptoms warrant dialysis. Doctrine emphasizes risk stratification, supportive care, and monitoring. Adversaries may argue for conservative management, but evidence supports dialysis in severe cases. Regulatory guidance mandates monitoring and reporting.
        """,
        key_factors=["Serum lithium level", "Renal function", "Clinical severity", "Time since ingestion"],
        primary_authority=["FDA", "WHO", "ACMT", "APA"],
        burden_holder="Healthcare provider",
        adversary_position="Some clinicians advocate for observation only.",
        counter_arguments=[
            "Delayed dialysis increases risk of permanent neurotoxicity.",
            "Renal impairment increases toxicity risk.",
            "Therapeutic monitoring improves outcomes."
        ],
        resolution_strategy="Follow evidence-based protocols for monitoring and dialysis.",
        entity_scope="Psychiatric clinics, emergency departments",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FDA Lithium Toxicity Guidance (2019)"
    ),
    DoctrineBlock(
        topic="mercury_poisoning",
        keywords=["mercury", "poisoning", "neurotoxicity", "chelation", "organic mercury", "elemental mercury"],
        conclusion_template="Mercury poisoning is diagnosed by clinical symptoms and blood/urine levels; chelation is indicated for severe cases.",
        reasoning_framework="""
        Mercury exists in elemental, inorganic, and organic forms, each with distinct toxicity profiles. Organic mercury (methylmercury) causes neurotoxicity, especially in children and fetuses. Diagnosis relies on exposure history, clinical symptoms, and laboratory confirmation. Chelation therapy (dimercaprol, succimer) is reserved for severe cases. Doctrine emphasizes prevention, risk assessment, and regulatory limits. Adversaries may argue for less stringent controls, but public health evidence supports strict regulation.
        """,
        key_factors=["Type of mercury", "Exposure history", "Clinical symptoms", "Laboratory levels"],
        primary_authority=["EPA", "CDC", "WHO", "FDA"],
        burden_holder="Employer or public health authority",
        adversary_position="Industry disputes low-level toxicity.",
        counter_arguments=[
            "No safe threshold for children.",
            "Long-term effects persist after exposure.",
            "Prevention is more effective than treatment."
        ],
        resolution_strategy="Mandate strict limits, surveillance, and remediation.",
        entity_scope="Children, workers, general population",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Mercury Risk Assessment (2020)"
    ),
    DoctrineBlock(
        topic="arsenic_poisoning",
        keywords=["arsenic", "poisoning", "chronic exposure", "skin lesions", "cancer", "chelators"],
        conclusion_template="Arsenic poisoning is diagnosed by history, symptoms, and laboratory confirmation; chelation is reserved for acute cases.",
        reasoning_framework="""
        Arsenic exposure occurs via contaminated water, food, and occupational sources. Chronic exposure causes skin lesions, neuropathy, and increased cancer risk. Diagnosis relies on history, clinical symptoms, and laboratory confirmation. Chelation therapy is indicated for acute poisoning. Doctrine emphasizes prevention, risk assessment, and regulatory limits. Adversaries may argue for less stringent controls, but evidence supports strict regulation and remediation.
        """,
        key_factors=["Exposure history", "Clinical symptoms", "Laboratory confirmation", "Type of arsenic"],
        primary_authority=["EPA", "CDC", "WHO", "FDA"],
        burden_holder="Employer or public health authority",
        adversary_position="Industry disputes low-level toxicity.",
        counter_arguments=[
            "Chronic exposure increases cancer risk.",
            "Prevention is more effective than treatment.",
            "Regulatory limits protect public health."
        ],
        resolution_strategy="Mandate strict limits, surveillance, and remediation.",
        entity_scope="Workers, general population",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Arsenic Risk Assessment (2018)"
    ),
    DoctrineBlock(
        topic="cadmium_poisoning",
        keywords=["cadmium", "poisoning", "renal toxicity", "bone disease", "occupational exposure", "chelators"],
        conclusion_template="Cadmium poisoning is diagnosed by history, symptoms, and laboratory confirmation; prevention is emphasized over chelation.",
        reasoning_framework="""
        Cadmium exposure occurs via industrial processes and contaminated food. Chronic exposure causes renal toxicity and bone disease. Diagnosis relies on history, clinical symptoms, and laboratory confirmation. Chelation therapy is rarely effective; prevention is emphasized. Doctrine mandates occupational limits, surveillance, and remediation. Adversaries may argue for less stringent controls, but evidence supports strict regulation.
        """,
        key_factors=["Exposure history", "Clinical symptoms", "Laboratory confirmation", "Duration of exposure"],
        primary_authority=["EPA", "OSHA", "WHO", "FDA"],
        burden_holder="Employer",
        adversary_position="Industry disputes low-level toxicity.",
        counter_arguments=[
            "Chronic exposure causes irreversible damage.",
            "Prevention is more effective than treatment.",
            "Regulatory limits protect worker health."
        ],
        resolution_strategy="Mandate strict occupational limits and surveillance.",
        entity_scope="Industrial workers, general population",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Cadmium Standards (2017)"
    ),
    DoctrineBlock(
        topic="pesticide_regulation",
        keywords=["pesticide", "regulation", "EPA", "risk assessment", "toxicity", "residue limits"],
        conclusion_template="Pesticide regulation is based on risk assessment, toxicity data, and residue limits to protect public health.",
        reasoning_framework="""
        Pesticide regulation integrates toxicity data, exposure assessment, and risk management. EPA sets residue limits and mandates registration. Doctrine emphasizes transparency, peer review, and periodic reassessment. Adversaries may argue for less stringent limits, but public health evidence supports precautionary principle. Regulatory mandates include labeling, exposure reduction, and surveillance.
        """,
        key_factors=["Toxicity data", "Exposure assessment", "Residue limits", "Regulatory standards"],
        primary_authority=["EPA", "FDA", "WHO", "CDC"],
        burden_holder="Manufacturer",
        adversary_position="Industry disputes limits based on economic impact.",
        counter_arguments=[
            "Public health outweighs economic arguments.",
            "Periodic reassessment ensures safety.",
            "Peer review ensures validity."
        ],
        resolution_strategy="Mandate compliance, labeling, and periodic review.",
        entity_scope="Agriculture, food industry",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Pesticide Regulation (2021)"
    ),
    DoctrineBlock(
        topic="chlorine_gas_exposure",
        keywords=["chlorine", "gas", "exposure", "respiratory toxicity", "emergency response", "decontamination"],
        conclusion_template="Chlorine gas exposure is managed by removal from source, decontamination, and supportive care.",
        reasoning_framework="""
        Chlorine gas causes respiratory irritation, pulmonary edema, and systemic toxicity. Immediate removal from source and decontamination are essential. Supportive care includes oxygen and bronchodilators. Doctrine emphasizes emergency response protocols, PPE, and regulatory limits. Adversaries may argue for less stringent controls, but evidence supports strict regulation and preparedness.
        """,
        key_factors=["Exposure history", "Clinical severity", "Time to intervention", "Emergency protocols"],
        primary_authority=["NIOSH", "OSHA", "WHO", "CDC"],
        burden_holder="Employer or emergency responder",
        adversary_position="Industry disputes need for emergency preparedness.",
        counter_arguments=[
            "Delayed intervention increases morbidity.",
            "Emergency protocols save lives.",
            "PPE is essential for responders."
        ],
        resolution_strategy="Mandate emergency protocols, PPE, and training.",
        entity_scope="Industrial workplaces, emergency services",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIOSH Chlorine Gas Exposure Guidelines (2019)"
    ),
    DoctrineBlock(
        topic="benzene_exposure",
        keywords=["benzene", "exposure", "hematotoxicity", "leukemia", "occupational limits", "carcinogenicity"],
        conclusion_template="Benzene exposure is regulated due to hematotoxicity and carcinogenicity; strict occupational limits are enforced.",
        reasoning_framework="""
        Benzene is a known carcinogen causing hematotoxicity and leukemia. Occupational exposure limits are set by OSHA and NIOSH. Doctrine emphasizes risk assessment, monitoring, and enforcement. Adversaries may argue for higher limits, but worker safety prevails. Regulatory mandates include surveillance, periodic review, and worker education.
        """,
        key_factors=["Exposure level", "Duration", "Worker population", "Regulatory standards"],
        primary_authority=["OSHA", "NIOSH", "EPA", "WHO"],
        burden_holder="Employer",
        adversary_position="Industry disputes carcinogenicity at low levels.",
        counter_arguments=[
            "No safe threshold for carcinogens.",
            "Chronic exposure increases cancer risk.",
            "Worker health outweighs economic arguments."
        ],
        resolution_strategy="Mandate strict limits, surveillance, and education.",
        entity_scope="Industrial workplaces",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Benzene Standards (2018)"
    ),
    DoctrineBlock(
        topic="polychlorinated_biphenyls_pcb_exposure",
        keywords=["PCB", "polychlorinated biphenyls", "exposure", "carcinogenicity", "neurotoxicity", "regulation"],
        conclusion_template="PCB exposure is regulated due to carcinogenicity and neurotoxicity; remediation and surveillance are mandated.",
        reasoning_framework="""
        PCBs are persistent organic pollutants causing carcinogenicity and neurotoxicity. EPA and WHO set regulatory limits and mandate remediation. Doctrine emphasizes risk assessment, environmental monitoring, and surveillance. Adversaries may argue for less stringent controls, but evidence supports strict regulation and remediation.
        """,
        key_factors=["Exposure history", "Environmental levels", "Health effects", "Regulatory standards"],
        primary_authority=["EPA", "WHO", "CDC", "FDA"],
        burden_holder="Manufacturer or public health authority",
        adversary_position="Industry disputes need for remediation.",
        counter_arguments=[
            "Persistent pollutants require remediation.",
            "Carcinogenicity justifies strict regulation.",
            "Surveillance ensures ongoing protection."
        ],
        resolution_strategy="Mandate remediation, surveillance, and regulatory compliance.",
        entity_scope="Industrial sites, general population",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA PCB Regulation (2017)"
    ),
    DoctrineBlock(
        topic="dioxin_exposure",
        keywords=["dioxin", "exposure", "carcinogenicity", "regulation", "environmental monitoring", "remediation"],
        conclusion_template="Dioxin exposure is regulated due to carcinogenicity; environmental monitoring and remediation are mandated.",
        reasoning_framework="""
        Dioxins are persistent organic pollutants causing carcinogenicity and reproductive toxicity. EPA and WHO set regulatory limits and mandate environmental monitoring. Doctrine emphasizes risk assessment, remediation, and surveillance. Adversaries may argue for less stringent controls, but evidence supports strict regulation and remediation.
        """,
        key_factors=["Exposure history", "Environmental levels", "Health effects", "Regulatory standards"],
        primary_authority=["EPA", "WHO", "CDC", "FDA"],
        burden_holder="Manufacturer or public health authority",
        adversary_position="Industry disputes need for remediation.",
        counter_arguments=[
            "Persistent pollutants require remediation.",
            "Carcinogenicity justifies strict regulation.",
            "Surveillance ensures ongoing protection."
        ],
        resolution_strategy="Mandate remediation, surveillance, and regulatory compliance.",
        entity_scope="Industrial sites, general population",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Dioxin Regulation (2018)"
    ),
    DoctrineBlock(
        topic="asbestos_exposure",
        keywords=["asbestos", "exposure", "mesothelioma", "lung cancer", "regulation", "remediation"],
        conclusion_template="Asbestos exposure is regulated due to carcinogenicity; remediation and surveillance are mandated.",
        reasoning_framework="""
        Asbestos is a known carcinogen causing mesothelioma and lung cancer. OSHA and EPA set regulatory limits and mandate remediation. Doctrine emphasizes risk assessment, environmental monitoring, and surveillance. Adversaries may argue for less stringent controls, but evidence supports strict regulation and remediation.
        """,
        key_factors=["Exposure history", "Environmental levels", "Health effects", "Regulatory standards"],
        primary_authority=["OSHA", "EPA", "WHO", "CDC"],
        burden_holder="Employer or public health authority",
        adversary_position="Industry disputes need for remediation.",
        counter_arguments=[
            "Carcinogenicity justifies strict regulation.",
            "Remediation prevents ongoing exposure.",
            "Surveillance ensures ongoing protection."
        ],
        resolution_strategy="Mandate remediation, surveillance, and regulatory compliance.",
        entity_scope="Industrial sites, general population",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Asbestos Standards (2019)"
    ),
    DoctrineBlock(
        topic="radon_exposure",
        keywords=["radon", "exposure", "lung cancer", "regulation", "environmental monitoring", "remediation"],
        conclusion_template="Radon exposure is regulated due to lung cancer risk; environmental monitoring and remediation are mandated.",
        reasoning_framework="""
        Radon is a radioactive gas causing lung cancer. EPA and WHO set regulatory limits and mandate environmental monitoring. Doctrine emphasizes risk assessment, remediation, and surveillance. Adversaries may argue for less stringent controls, but evidence supports strict regulation and remediation.
        """,
        key_factors=["Exposure history", "Environmental levels", "Health effects", "Regulatory standards"],
        primary_authority=["EPA", "WHO", "CDC", "FDA"],
        burden_holder="Homeowner or public health authority",
        adversary_position="Industry disputes need for remediation.",
        counter_arguments=[
            "Carcinogenicity justifies strict regulation.",
            "Remediation prevents ongoing exposure.",
            "Surveillance ensures ongoing protection."
        ],
        resolution_strategy="Mandate remediation, surveillance, and regulatory compliance.",
        entity_scope="Homes, workplaces",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Radon Regulation (2020)"
    ),
    DoctrineBlock(
        topic="phthalate_exposure",
        keywords=["phthalate", "exposure", "endocrine disruption", "regulation", "risk assessment", "surveillance"],
        conclusion_template="Phthalate exposure is regulated due to endocrine disruption; surveillance and periodic reassessment are mandated.",
        reasoning_framework="""
        Phthalates are endocrine disruptors affecting reproductive health. EPA and FDA set regulatory limits and mandate surveillance. Doctrine emphasizes risk assessment, periodic reassessment, and transparency. Adversaries may argue for less stringent controls, but evidence supports strict regulation and surveillance.
        """,
        key_factors=["Exposure history", "Health effects", "Regulatory standards", "Surveillance data"],
        primary_authority=["EPA", "FDA", "WHO", "CDC"],
        burden_holder="Manufacturer or public health authority",
        adversary_position="Industry disputes need for regulation.",
        counter_arguments=[
            "Endocrine disruption justifies regulation.",
            "Surveillance ensures ongoing protection.",
            "Periodic reassessment ensures safety."
        ],
        resolution_strategy="Mandate surveillance, periodic reassessment, and regulatory compliance.",
        entity_scope="Consumer products, general population",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Phthalate Regulation (2018)"
    ),
    DoctrineBlock(
        topic="bisphenol_a_bpa_exposure",
        keywords=["bisphenol A", "BPA", "exposure", "endocrine disruption", "regulation", "risk assessment"],
        conclusion_template="BPA exposure is regulated due to endocrine disruption; surveillance and periodic reassessment are mandated.",
        reasoning_framework="""
        BPA is an endocrine disruptor affecting reproductive health. EPA and FDA set regulatory limits and mandate surveillance. Doctrine emphasizes risk assessment, periodic reassessment, and transparency. Adversaries may argue for less stringent controls, but evidence supports strict regulation and surveillance.
        """,
        key_factors=["Exposure history", "Health effects", "Regulatory standards", "Surveillance data"],
        primary_authority=["EPA", "FDA", "WHO", "CDC"],
        burden_holder="Manufacturer or public health authority",
        adversary_position="Industry disputes need for regulation.",
        counter_arguments=[
            "Endocrine disruption justifies regulation.",
            "Surveillance ensures ongoing protection.",
            "Periodic reassessment ensures safety."
        ],
        resolution_strategy="Mandate surveillance, periodic reassessment, and regulatory compliance.",
        entity_scope="Consumer products, general population",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA BPA Regulation (2019)"
    ),
    DoctrineBlock(
        topic="paraquat_poisoning",
        keywords=["paraquat", "poisoning", "herbicide", "pulmonary toxicity", "regulation", "emergency response"],
        conclusion_template="Paraquat poisoning is managed by decontamination and supportive care; strict regulation is mandated due to high toxicity.",
        reasoning_framework="""
        Paraquat is a highly toxic herbicide causing pulmonary fibrosis and multi-organ failure. Immediate decontamination and supportive care are essential. Doctrine emphasizes strict regulation, emergency response protocols, and PPE. Adversaries may argue for less stringent controls, but evidence supports strict regulation and preparedness.
        """,
        key_factors=["Exposure history", "Clinical severity", "Time to intervention", "Regulatory standards"],
        primary_authority=["EPA", "WHO", "CDC", "FDA"],
        burden_holder="Employer or emergency responder",
        adversary_position="Industry disputes need for strict regulation.",
        counter_arguments=[
            "High toxicity justifies strict regulation.",
            "Emergency protocols save lives.",
            "PPE is essential for responders."
        ],
        resolution_strategy="Mandate strict regulation, emergency protocols, and PPE.",
        entity_scope="Agricultural workplaces, emergency services",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Paraquat Regulation (2020)"
    ),
    DoctrineBlock(
        topic="ethylene_oxide_exposure",
        keywords=["ethylene oxide", "exposure", "carcinogenicity", "regulation", "occupational limits", "surveillance"],
        conclusion_template="Ethylene oxide exposure is regulated due to carcinogenicity; surveillance and strict occupational limits are mandated.",
        reasoning_framework="""
        Ethylene oxide is a known carcinogen causing leukemia and reproductive toxicity. OSHA and EPA set occupational limits and mandate surveillance. Doctrine emphasizes risk assessment, monitoring, and enforcement. Adversaries may argue for higher limits, but worker safety prevails.
        """,
        key_factors=["Exposure level", "Duration", "Worker population", "Regulatory standards"],
        primary_authority=["OSHA", "EPA", "WHO", "CDC"],
        burden_holder="Employer",
        adversary_position="Industry disputes carcinogenicity at low levels.",
        counter_arguments=[
            "No safe threshold for carcinogens.",
            "Chronic exposure increases cancer risk.",
            "Worker health outweighs economic arguments."
        ],
        resolution_strategy="Mandate strict limits, surveillance, and education.",
        entity_scope="Industrial workplaces",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Ethylene Oxide Standards (2018)"
    ),
    DoctrineBlock(
        topic="hydrogen_sulfide_exposure",
        keywords=["hydrogen sulfide", "exposure", "respiratory toxicity", "emergency response", "regulation", "PPE"],
        conclusion_template="Hydrogen sulfide exposure is managed by removal from source, supportive care, and strict regulation.",
        reasoning_framework="""
        Hydrogen sulfide causes respiratory toxicity and can be fatal. Immediate removal from source and supportive care are essential. Doctrine emphasizes emergency response protocols, PPE, and regulatory limits. Adversaries may argue for less stringent controls, but evidence supports strict regulation and preparedness.
        """,
        key_factors=["Exposure history", "Clinical severity", "Time to intervention", "Regulatory standards"],
        primary_authority=["NIOSH", "OSHA", "WHO", "CDC"],
        burden_holder="Employer or emergency responder",
        adversary_position="Industry disputes need for emergency preparedness.",
        counter_arguments=[
            "Delayed intervention increases morbidity.",
            "Emergency protocols save lives.",
            "PPE is essential for responders."
        ],
        resolution_strategy="Mandate emergency protocols, PPE, and training.",
        entity_scope="Industrial workplaces, emergency services",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIOSH Hydrogen Sulfide Exposure Guidelines (2019)"
    ),
    DoctrineBlock(
        topic="chlorpyrifos_regulation",
        keywords=["chlorpyrifos", "regulation", "pesticide", "neurotoxicity", "EPA", "risk assessment"],
        conclusion_template="Chlorpyrifos regulation is based on neurotoxicity risk; EPA mandates strict limits and periodic reassessment.",
        reasoning_framework="""
        Chlorpyrifos is a pesticide causing neurotoxicity, especially in children. EPA mandates strict limits and periodic reassessment. Doctrine emphasizes risk assessment, transparency, and peer review. Adversaries may argue for less stringent controls, but evidence supports strict regulation.
        """,
        key_factors=["Neurotoxicity data", "Exposure assessment", "Regulatory standards", "Surveillance data"],
        primary_authority=["EPA", "FDA", "WHO", "CDC"],
        burden_holder="Manufacturer",
        adversary_position="Industry disputes limits based on economic impact.",
        counter_arguments=[
            "Public health outweighs economic arguments.",
            "Periodic reassessment ensures safety.",
            "Peer review ensures validity."
        ],
        resolution_strategy="Mandate compliance, labeling, and periodic review.",
        entity_scope="Agriculture, food industry",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Chlorpyrifos Regulation (2021)"
    ),
    DoctrineBlock(
        topic="tetraethyl_lead_exposure",
        keywords=["tetraethyl lead", "exposure", "neurotoxicity", "regulation", "remediation", "surveillance"],
        conclusion_template="Tetraethyl lead exposure is regulated due to neurotoxicity; remediation and surveillance are mandated.",
        reasoning_framework="""
        Tetraethyl lead is a neurotoxic compound formerly used in gasoline. EPA and WHO set regulatory limits and mandate remediation. Doctrine emphasizes risk assessment, environmental monitoring, and surveillance. Adversaries may argue for less stringent controls, but evidence supports strict regulation and remediation.
        """,
        key_factors=["Exposure history", "Environmental levels", "Health effects", "Regulatory standards"],
        primary_authority=["EPA", "WHO", "CDC", "FDA"],
        burden_holder="Manufacturer or public health authority",
        adversary_position="Industry disputes need for remediation.",
        counter_arguments=[
            "Neurotoxicity justifies strict regulation.",
            "Remediation prevents ongoing exposure.",
            "Surveillance ensures ongoing protection."
        ],
        resolution_strategy="Mandate remediation, surveillance, and regulatory compliance.",
        entity_scope="Industrial sites, general population",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Lead Regulation (2018)"
    ),
    DoctrineBlock(
        topic="formaldehyde_exposure",
        keywords=["formaldehyde", "exposure", "carcinogenicity", "regulation", "occupational limits", "surveillance"],
        conclusion_template="Formaldehyde exposure is regulated due to carcinogenicity; surveillance and strict occupational limits are mandated.",
        reasoning_framework="""
        Formaldehyde is a known carcinogen causing nasopharyngeal cancer. OSHA and EPA set occupational limits and mandate surveillance. Doctrine emphasizes risk assessment, monitoring, and enforcement. Adversaries may argue for higher limits, but worker safety prevails.
        """,
        key_factors=["Exposure level", "Duration", "Worker population", "Regulatory standards"],
        primary_authority=["OSHA", "EPA", "WHO", "CDC"],
        burden_holder="Employer",
        adversary_position="Industry disputes carcinogenicity at low levels.",
        counter_arguments=[
            "No safe threshold for carcinogens.",
            "Chronic exposure increases cancer risk.",
            "Worker health outweighs economic arguments."
        ],
        resolution_strategy="Mandate strict limits, surveillance, and education.",
        entity_scope="Industrial workplaces",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Formaldehyde Standards (2019)"
    ),
    DoctrineBlock(
        topic="pesticide_resistance_management",
        keywords=["pesticide", "resistance", "management", "rotation", "regulation", "surveillance"],
        conclusion_template="Pesticide resistance management is mandated by regulatory agencies; rotation and surveillance are required.",
        reasoning_framework="""
        Pesticide resistance threatens efficacy and public health. Regulatory agencies mandate resistance management, including rotation, surveillance, and education. Doctrine emphasizes transparency, peer review, and periodic reassessment. Adversaries may argue for less stringent controls, but evidence supports strict regulation.
        """,
        key_factors=["Resistance data", "Surveillance", "Regulatory standards", "Management protocols"],
        primary_authority=["EPA", "FDA", "WHO", "CDC"],
        burden_holder="Manufacturer",
        adversary_position="Industry disputes need for rotation and surveillance.",
        counter_arguments=[
            "Resistance threatens efficacy.",
            "Surveillance ensures ongoing protection.",
            "Periodic reassessment ensures safety."
        ],
        resolution_strategy="Mandate rotation, surveillance, and regulatory compliance.",
        entity_scope="Agriculture, food industry",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Pesticide Resistance Management (2020)"
    ),
    DoctrineBlock(
        topic="antidote_stockpiling_policy",
        keywords=["antidote", "stockpiling", "policy", "emergency preparedness", "regulation", "public health"],
        conclusion_template="Antidote stockpiling is mandated for emergency preparedness; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Antidote stockpiling ensures rapid response to mass casualty events. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced stockpiling based on cost, but public health evidence supports preparedness.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Emergency protocols"],
        primary_authority=["CDC", "FDA", "WHO", "EPA"],
        burden_holder="Public health authority",
        adversary_position="Budget constraints limit stockpiling.",
        counter_arguments=[
            "Preparedness outweighs cost concerns.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate stockpiling, training, and periodic review.",
        entity_scope="Hospitals, emergency services",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Antidote Stockpiling Policy (2017)"
    ),
    DoctrineBlock(
        topic="toxic_alcohol_screening_policy",
        keywords=["toxic alcohol", "screening", "policy", "methanol", "ethylene glycol", "laboratory protocols"],
        conclusion_template="Toxic alcohol screening is mandated for suspected cases; laboratory protocols ensure rapid diagnosis.",
        reasoning_framework="""
        Toxic alcohol screening ensures rapid diagnosis and intervention. Laboratory protocols include measurement of anion gap, osmolar gap, and specific assays. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced screening based on cost, but evidence supports rapid diagnosis and intervention.
        """,
        key_factors=["Clinical suspicion", "Laboratory protocols", "Regulatory standards", "Emergency response"],
        primary_authority=["FDA", "CDC", "WHO", "ACMT"],
        burden_holder="Healthcare provider",
        adversary_position="Budget constraints limit screening.",
        counter_arguments=[
            "Rapid diagnosis improves outcomes.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate screening, training, and periodic review.",
        entity_scope="Hospitals, emergency departments",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FDA Toxic Alcohol Screening Policy (2018)"
    ),
    DoctrineBlock(
        topic="poison_center_reporting_policy",
        keywords=["poison center", "reporting", "policy", "surveillance", "public health", "regulation"],
        conclusion_template="Poison center reporting is mandated for surveillance and public health; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Poison center reporting ensures surveillance and rapid response to toxic exposures. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced reporting based on privacy concerns, but public health evidence supports surveillance.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Surveillance protocols"],
        primary_authority=["CDC", "FDA", "WHO", "EPA"],
        burden_holder="Healthcare provider",
        adversary_position="Privacy concerns limit reporting.",
        counter_arguments=[
            "Surveillance outweighs privacy concerns.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate reporting, training, and periodic review.",
        entity_scope="Hospitals, poison centers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Poison Center Reporting Policy (2017)"
    ),
    DoctrineBlock(
        topic="child_lead_screening_policy",
        keywords=["child", "lead", "screening", "policy", "public health", "regulation"],
        conclusion_template="Child lead screening is mandated for at-risk populations; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Child lead screening ensures early detection and intervention. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced screening based on cost, but public health evidence supports early detection.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Screening protocols"],
        primary_authority=["CDC", "FDA", "WHO", "EPA"],
        burden_holder="Public health authority",
        adversary_position="Budget constraints limit screening.",
        counter_arguments=[
            "Early detection improves outcomes.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate screening, training, and periodic review.",
        entity_scope="Hospitals, public health clinics",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CDC Child Lead Screening Policy (2018)"
    ),
    DoctrineBlock(
        topic="occupational_ppe_policy",
        keywords=["occupational", "PPE", "policy", "regulation", "worker safety", "training"],
        conclusion_template="Occupational PPE policy is mandated for worker safety; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Occupational PPE policy ensures worker safety in hazardous environments. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced PPE based on cost, but worker safety evidence supports strict requirements.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Training protocols"],
        primary_authority=["OSHA", "NIOSH", "EPA", "WHO"],
        burden_holder="Employer",
        adversary_position="Budget constraints limit PPE.",
        counter_arguments=[
            "Worker safety outweighs cost concerns.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate PPE, training, and periodic review.",
        entity_scope="Industrial workplaces, laboratories",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Occupational PPE Policy (2019)"
    ),
    DoctrineBlock(
        topic="chemical_spill_response_policy",
        keywords=["chemical", "spill", "response", "policy", "emergency preparedness", "regulation"],
        conclusion_template="Chemical spill response policy is mandated for emergency preparedness; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Chemical spill response policy ensures rapid containment and remediation. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced response based on cost, but evidence supports rapid containment and remediation.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Emergency protocols"],
        primary_authority=["EPA", "OSHA", "NIOSH", "WHO"],
        burden_holder="Employer or emergency responder",
        adversary_position="Budget constraints limit response.",
        counter_arguments=[
            "Rapid containment prevents environmental damage.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate response protocols, training, and periodic review.",
        entity_scope="Industrial workplaces, emergency services",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Chemical Spill Response Policy (2018)"
    ),
    DoctrineBlock(
        topic="environmental_surveillance_policy",
        keywords=["environmental", "surveillance", "policy", "public health", "regulation", "monitoring"],
        conclusion_template="Environmental surveillance policy is mandated for public health; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Environmental surveillance policy ensures ongoing monitoring of hazardous substances. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced surveillance based on cost, but public health evidence supports ongoing monitoring.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Surveillance protocols"],
        primary_authority=["EPA", "CDC", "WHO", "FDA"],
        burden_holder="Public health authority",
        adversary_position="Budget constraints limit surveillance.",
        counter_arguments=[
            "Ongoing monitoring ensures early detection.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate surveillance, training, and periodic review.",
        entity_scope="Public health agencies, environmental monitoring",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Environmental Surveillance Policy (2019)"
    ),
    DoctrineBlock(
        topic="food_contaminant_regulation",
        keywords=["food", "contaminant", "regulation", "public health", "risk assessment", "surveillance"],
        conclusion_template="Food contaminant regulation is mandated for public health; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Food contaminant regulation ensures safety of the food supply. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, surveillance, and periodic review. Adversaries may argue for reduced regulation based on cost, but public health evidence supports strict requirements.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Surveillance protocols"],
        primary_authority=["FDA", "EPA", "WHO", "CDC"],
        burden_holder="Manufacturer",
        adversary_position="Budget constraints limit regulation.",
        counter_arguments=[
            "Food safety outweighs cost concerns.",
            "Periodic review ensures adequacy.",
            "Surveillance ensures ongoing protection."
        ],
        resolution_strategy="Mandate regulation, surveillance, and periodic review.",
        entity_scope="Food industry, public health agencies",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FDA Food Contaminant Regulation (2018)"
    ),
    DoctrineBlock(
        topic="water_contaminant_regulation",
        keywords=["water", "contaminant", "regulation", "public health", "risk assessment", "surveillance"],
        conclusion_template="Water contaminant regulation is mandated for public health; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Water contaminant regulation ensures safety of drinking water. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, surveillance, and periodic review. Adversaries may argue for reduced regulation based on cost, but public health evidence supports strict requirements.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Surveillance protocols"],
        primary_authority=["EPA", "CDC", "WHO", "FDA"],
        burden_holder="Water supplier",
        adversary_position="Budget constraints limit regulation.",
        counter_arguments=[
            "Water safety outweighs cost concerns.",
            "Periodic review ensures adequacy.",
            "Surveillance ensures ongoing protection."
        ],
        resolution_strategy="Mandate regulation, surveillance, and periodic review.",
        entity_scope="Water suppliers, public health agencies",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Water Contaminant Regulation (2019)"
    ),
    DoctrineBlock(
        topic="air_contaminant_regulation",
        keywords=["air", "contaminant", "regulation", "public health", "risk assessment", "surveillance"],
        conclusion_template="Air contaminant regulation is mandated for public health; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Air contaminant regulation ensures safety of ambient air. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, surveillance, and periodic review. Adversaries may argue for reduced regulation based on cost, but public health evidence supports strict requirements.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Surveillance protocols"],
        primary_authority=["EPA", "CDC", "WHO", "FDA"],
        burden_holder="Air supplier",
        adversary_position="Budget constraints limit regulation.",
        counter_arguments=[
            "Air safety outweighs cost concerns.",
            "Periodic review ensures adequacy.",
            "Surveillance ensures ongoing protection."
        ],
        resolution_strategy="Mandate regulation, surveillance, and periodic review.",
        entity_scope="Air suppliers, public health agencies",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Air Contaminant Regulation (2018)"
    ),
    DoctrineBlock(
        topic="hazardous_waste_management_policy",
        keywords=["hazardous waste", "management", "policy", "regulation", "public health", "remediation"],
        conclusion_template="Hazardous waste management policy is mandated for public health; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Hazardous waste management policy ensures safe disposal and remediation. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced management based on cost, but public health evidence supports strict requirements.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Remediation protocols"],
        primary_authority=["EPA", "CDC", "WHO", "FDA"],
        burden_holder="Waste generator",
        adversary_position="Budget constraints limit management.",
        counter_arguments=[
            "Safe disposal prevents environmental damage.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate management protocols, training, and periodic review.",
        entity_scope="Industrial workplaces, waste generators",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA Hazardous Waste Management Policy (2019)"
    ),
    DoctrineBlock(
        topic="chemical_labeling_policy",
        keywords=["chemical", "labeling", "policy", "regulation", "public health", "worker safety"],
        conclusion_template="Chemical labeling policy is mandated for public health and worker safety; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Chemical labeling policy ensures safe handling and worker safety. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced labeling based on cost, but evidence supports strict requirements.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Labeling protocols"],
        primary_authority=["OSHA", "EPA", "NIOSH", "WHO"],
        burden_holder="Manufacturer",
        adversary_position="Budget constraints limit labeling.",
        counter_arguments=[
            "Safe handling prevents injury.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate labeling, training, and periodic review.",
        entity_scope="Industrial workplaces, laboratories",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Chemical Labeling Policy (2018)"
    ),
    DoctrineBlock(
        topic="chemical_inventory_policy",
        keywords=["chemical", "inventory", "policy", "regulation", "public health", "worker safety"],
        conclusion_template="Chemical inventory policy is mandated for public health and worker safety; regulatory agencies set minimum requirements.",
        reasoning_framework="""
        Chemical inventory policy ensures safe storage and handling. Regulatory agencies set minimum requirements based on risk assessment and population size. Doctrine emphasizes preparedness, training, and periodic review. Adversaries may argue for reduced inventory based on cost, but evidence supports strict requirements.
        """,
        key_factors=["Risk assessment", "Population size", "Regulatory standards", "Inventory protocols"],
        primary_authority=["OSHA", "EPA", "NIOSH", "WHO"],
        burden_holder="Manufacturer",
        adversary_position="Budget constraints limit inventory.",
        counter_arguments=[
            "Safe storage prevents injury.",
            "Periodic review ensures adequacy.",
            "Training ensures effective response."
        ],
        resolution_strategy="Mandate inventory, training, and periodic review.",
        entity_scope="Industrial workplaces, laboratories",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Chemical Inventory Policy (2019)"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
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