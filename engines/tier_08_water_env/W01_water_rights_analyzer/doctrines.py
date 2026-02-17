import enum
from dataclasses import dataclass
from typing import List, Optional
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
        topic="Texas Water Code Fundamentals",
        keywords=["Texas Water Code", "statutory framework", "water rights", "surface water", "groundwater"],
        conclusion_template="Under the Texas Water Code, the allocation and regulation of surface and groundwater are governed by distinct statutory regimes.",
        reasoning_framework=(
            "1. Identify the type of water resource (surface or groundwater).\n"
            "2. Review relevant chapters of the Texas Water Code (TWC), focusing on Title 2 (Water Administration) and Title 4 (Groundwater Regulation).\n"
            "3. Determine the applicable permitting or registration requirements for the water use in question.\n"
            "4. Assess the role of state agencies such as TCEQ and local entities like Groundwater Conservation Districts (GCDs).\n"
            "5. Examine any exemptions, grandfathered rights, or special provisions.\n"
            "6. Evaluate compliance with reporting, metering, and conservation mandates.\n"
            "7. Consider judicial interpretations of ambiguous statutory language.\n"
            "8. Analyze the interplay between statutory law and common law doctrines (e.g., Rule of Capture).\n"
            "9. Assess the applicability of federal preemption or interstate compacts.\n"
            "10. Synthesize findings to determine the legal status of the water right or use."
        ),
        key_factors=[
            "Type of water (surface or groundwater)",
            "Applicable statutory provisions",
            "Permitting requirements",
            "Agency jurisdiction",
            "Exemptions and grandfathered uses"
        ],
        primary_authority=[
            "Texas Water Code, Titles 2 & 4",
            "Texas Commission on Environmental Quality (TCEQ) regulations"
        ],
        burden_holder="Applicant or water user",
        adversary_position="State or local regulator may contest compliance or eligibility",
        counter_arguments=[
            "Statutory ambiguity",
            "Pre-existing rights",
            "Federal preemption",
            "Regulatory overreach"
        ],
        resolution_strategy="Statutory interpretation, agency guidance, and judicial review",
        entity_scope="All water users and regulators in Texas",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="In re Adjudication of the Upper Guadalupe Segment, 642 S.W.2d 438 (Tex. 1982)"
    ),
    DoctrineBlock(
        topic="Prior Appropriation Doctrine",
        keywords=["prior appropriation", "first in time", "beneficial use", "surface water", "priority date"],
        conclusion_template="The right to use surface water in Texas is generally determined by the prior appropriation doctrine: 'first in time, first in right.'",
        reasoning_framework=(
            "1. Establish the priority date of the water right or permit.\n"
            "2. Confirm that the appropriation was for a beneficial use recognized by law.\n"
            "3. Determine if the right has been maintained through continued beneficial use (use it or lose it).\n"
            "4. Assess if any forfeiture, abandonment, or cancellation has occurred.\n"
            "5. Analyze the impact of drought, shortage, or curtailment orders on junior rights.\n"
            "6. Review any amendments, transfers, or changes in place or purpose of use.\n"
            "7. Consider the effect of adjudication or basin-wide priority calls.\n"
            "8. Evaluate the role of TCEQ in administering priorities during shortages.\n"
            "9. Synthesize findings to determine the enforceability and scope of the right."
        ),
        key_factors=[
            "Priority date",
            "Beneficial use",
            "Maintenance of use",
            "TCEQ administration",
            "Shortage orders"
        ],
        primary_authority=[
            "Texas Water Code § 11.027",
            "TCEQ Surface Water Rights Administration"
        ],
        burden_holder="Junior appropriator or applicant",
        adversary_position="Senior appropriator may assert priority to exclude junior use",
        counter_arguments=[
            "Non-use or abandonment",
            "Change in beneficial use",
            "Statutory exceptions"
        ],
        resolution_strategy="Priority call enforcement, administrative hearings, judicial review",
        entity_scope="Surface water right holders and applicants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="State v. Hidalgo County Water Control & Improvement Dist. No. 18, 443 S.W.2d 728 (Tex. 1969)"
    ),
    DoctrineBlock(
        topic="Rule of Capture for Groundwater",
        keywords=["rule of capture", "groundwater", "ownership in place", "landowner rights", "common law"],
        conclusion_template="Under the Rule of Capture, Texas landowners may pump and use groundwater beneath their land, subject to limited exceptions.",
        reasoning_framework=(
            "1. Confirm that the water in question is groundwater, not surface water or state-owned.\n"
            "2. Establish landowner status and the location of the well.\n"
            "3. Determine if the pumping is within the landowner's property boundaries.\n"
            "4. Review any applicable local regulations (e.g., GCD rules) that may limit pumping.\n"
            "5. Assess whether the pumping constitutes waste, malicious intent, or subsidence.\n"
            "6. Examine any statutory limitations or exceptions (e.g., Edwards Aquifer Authority).\n"
            "7. Consider the impact on neighboring wells and potential liability for damages.\n"
            "8. Synthesize findings to determine the scope and limits of the right."
        ),
        key_factors=[
            "Landowner status",
            "Location of well",
            "Local GCD regulations",
            "Waste or malicious pumping",
            "Statutory exceptions"
        ],
        primary_authority=[
            "Houston & T.C. Ry. Co. v. East, 81 S.W. 279 (Tex. 1904)",
            "Texas Water Code Chapter 36"
        ],
        burden_holder="Challenger (neighbor or GCD)",
        adversary_position="Landowner asserts right to unlimited pumping",
        counter_arguments=[
            "Waste or malicious intent",
            "Subsidence",
            "Local GCD restrictions"
        ],
        resolution_strategy="Litigation, GCD enforcement, legislative amendment",
        entity_scope="Landowners, GCDs, groundwater users",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Houston & T.C. Ry. Co. v. East, 81 S.W. 279 (Tex. 1904)"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation District Rules",
        keywords=["groundwater conservation district", "GCD", "local regulation", "permitting", "production limits"],
        conclusion_template="Groundwater Conservation Districts (GCDs) may regulate groundwater production through permitting and spacing rules within their jurisdiction.",
        reasoning_framework=(
            "1. Identify the GCD with jurisdiction over the property or well.\n"
            "2. Review the GCD's enabling legislation and adopted rules.\n"
            "3. Determine whether the well or use is exempt from permitting (e.g., domestic/livestock).\n"
            "4. Assess the requirements for well spacing, production limits, and metering.\n"
            "5. Evaluate the application process for new or amended permits.\n"
            "6. Consider any contested case procedures or appeals.\n"
            "7. Examine enforcement mechanisms and penalties for noncompliance.\n"
            "8. Analyze the interplay with state law and the Rule of Capture.\n"
            "9. Synthesize findings to determine the legal status of the groundwater use."
        ),
        key_factors=[
            "GCD jurisdiction",
            "Well type and use",
            "Permitting requirements",
            "Production limits",
            "Exemptions"
        ],
        primary_authority=[
            "Texas Water Code Chapter 36",
            "Local GCD rules"
        ],
        burden_holder="Applicant or well owner",
        adversary_position="GCD may deny or limit permit",
        counter_arguments=[
            "Exemption claims",
            "Overly restrictive rules",
            "State law preemption"
        ],
        resolution_strategy="Administrative appeal, judicial review, legislative amendment",
        entity_scope="Groundwater users within GCD boundaries",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Day v. Edwards Aquifer Authority, 369 S.W.3d 814 (Tex. 2012)"
    ),
    DoctrineBlock(
        topic="Permian Basin GCD Regulations",
        keywords=["Permian Basin", "GCD", "groundwater", "production limits", "regional rules"],
        conclusion_template="The Permian Basin Groundwater Conservation District enforces specific production limits, permitting, and monitoring requirements for wells within its jurisdiction.",
        reasoning_framework=(
            "1. Confirm the well's location within the Permian Basin GCD boundaries.\n"
            "2. Review the District's enabling act and adopted rules.\n"
            "3. Determine the type of well and whether it is exempt from permitting.\n"
            "4. Assess annual production limits, spacing requirements, and metering obligations.\n"
            "5. Evaluate permit application and renewal procedures.\n"
            "6. Consider any special rules for oil and gas operations or brackish groundwater.\n"
            "7. Examine enforcement actions and available defenses.\n"
            "8. Synthesize findings to determine compliance and risk exposure."
        ),
        key_factors=[
            "District boundaries",
            "Well classification",
            "Production and spacing rules",
            "Metering requirements",
            "Special rules for oil/gas"
        ],
        primary_authority=[
            "Permian Basin GCD Rules",
            "Texas Water Code Chapter 36"
        ],
        burden_holder="Well operator or applicant",
        adversary_position="District may deny, limit, or revoke permit",
        counter_arguments=[
            "Exemption status",
            "Reasonableness of rules",
            "Conflict with state law"
        ],
        resolution_strategy="District hearings, administrative appeal, judicial review",
        entity_scope="Groundwater users in Permian Basin GCD",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Permian Basin Underground Water Conservation Dist. v. Bragg, 346 S.W.3d 781 (Tex. App.—El Paso 2011, pet. denied)"
    ),
    DoctrineBlock(
        topic="Surface Water Permits (TCEQ)",
        keywords=["surface water", "permit", "TCEQ", "appropriation", "application", "public interest"],
        conclusion_template="A permit from the TCEQ is required to appropriate state surface water for most uses, subject to statutory and regulatory criteria.",
        reasoning_framework=(
            "1. Confirm the water source is state surface water (not groundwater or exempt).\n"
            "2. Review the application requirements under Texas Water Code Chapter 11.\n"
            "3. Assess whether the proposed use is beneficial and consistent with public interest.\n"
            "4. Determine if unappropriated water is available at the requested location.\n"
            "5. Evaluate potential impacts on existing rights and environmental flows.\n"
            "6. Consider public notice and opportunity for protest.\n"
            "7. Analyze TCEQ's findings and any special conditions imposed.\n"
            "8. Synthesize findings to determine likelihood of permit issuance."
        ),
        key_factors=[
            "Source of water",
            "Beneficial use",
            "Availability of unappropriated water",
            "Impact on existing rights",
            "Public interest"
        ],
        primary_authority=[
            "Texas Water Code Chapter 11",
            "TCEQ Rules (30 TAC Chapter 295)"
        ],
        burden_holder="Applicant",
        adversary_position="Protestants may challenge on public interest or impairment grounds",
        counter_arguments=[
            "No unappropriated water available",
            "Environmental harm",
            "Impairment of senior rights"
        ],
        resolution_strategy="TCEQ hearing, administrative appeal, judicial review",
        entity_scope="Surface water appropriators",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="City of San Antonio v. Texas Water Comm’n, 407 S.W.2d 752 (Tex. 1966)"
    ),
    DoctrineBlock(
        topic="Water Rights Transfers",
        keywords=["water rights", "transfer", "assignment", "change of ownership", "TCEQ approval"],
        conclusion_template="Transfers of surface water rights generally require TCEQ approval and must not impair existing rights or the public interest.",
        reasoning_framework=(
            "1. Identify the type of water right (permit, certificate, adjudicated right).\n"
            "2. Review statutory and regulatory requirements for transfer or assignment.\n"
            "3. Assess whether the transfer involves a change in place, purpose, or diversion point.\n"
            "4. Determine if TCEQ approval is required and the standards for approval.\n"
            "5. Evaluate potential impacts on other rights and environmental flows.\n"
            "6. Consider notice and protest procedures.\n"
            "7. Analyze any special conditions imposed by TCEQ.\n"
            "8. Synthesize findings to determine validity and enforceability of the transfer."
        ),
        key_factors=[
            "Type of right",
            "Nature of transfer",
            "TCEQ approval",
            "Impact on other rights",
            "Public interest"
        ],
        primary_authority=[
            "Texas Water Code § 11.083",
            "TCEQ Rules (30 TAC § 295.73)"
        ],
        burden_holder="Transferor and transferee",
        adversary_position="Protestants may allege impairment or public interest harm",
        counter_arguments=[
            "Impairment of senior rights",
            "Environmental impact",
            "Procedural defects"
        ],
        resolution_strategy="TCEQ review, administrative appeal, litigation",
        entity_scope="Surface water right holders",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="State v. Texas Irrigation Co., 190 S.W. 867 (Tex. Civ. App.—Austin 1916, writ ref’d)"
    ),
    DoctrineBlock(
        topic="Produced Water Regulations",
        keywords=["produced water", "oil and gas", "regulation", "disposal", "reuse", "Railroad Commission"],
        conclusion_template="Produced water from oil and gas operations is regulated primarily by the Texas Railroad Commission, with specific requirements for disposal, reuse, and discharge.",
        reasoning_framework=(
            "1. Identify the source and composition of the produced water.\n"
            "2. Review Railroad Commission rules for handling, disposal, and reuse.\n"
            "3. Determine if TCEQ or EPA regulations also apply (e.g., discharge to surface water).\n"
            "4. Assess permitting requirements for disposal wells or surface discharge.\n"
            "5. Evaluate reporting, monitoring, and recordkeeping obligations.\n"
            "6. Consider liability for spills, contamination, or unauthorized discharge.\n"
            "7. Analyze opportunities for beneficial reuse and associated regulatory hurdles.\n"
            "8. Synthesize findings to determine compliance and risk."
        ),
        key_factors=[
            "Source of produced water",
            "Disposal/reuse method",
            "Permitting requirements",
            "Agency jurisdiction",
            "Environmental impact"
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 91",
            "Railroad Commission Rules (16 TAC Chapter 3)"
        ],
        burden_holder="Operator",
        adversary_position="Regulators or affected landowners may allege noncompliance",
        counter_arguments=[
            "Improper disposal",
            "Unauthorized reuse",
            "Environmental harm"
        ],
        resolution_strategy="Agency enforcement, administrative hearings, civil litigation",
        entity_scope="Oil and gas operators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Railroad Comm’n of Tex. v. Texas Citizens for a Safe Future, 336 S.W.3d 619 (Tex. 2011)"
    ),
    DoctrineBlock(
        topic="Recycled Water Permits",
        keywords=["recycled water", "reuse", "TCEQ", "permit", "wastewater", "beneficial use"],
        conclusion_template="A TCEQ permit is required for the direct or indirect reuse of treated wastewater for beneficial purposes.",
        reasoning_framework=(
            "1. Identify the source of wastewater and proposed reuse application.\n"
            "2. Review TCEQ rules for direct and indirect reuse.\n"
            "3. Assess treatment standards and monitoring requirements.\n"
            "4. Determine if the reuse will impact downstream water rights or environmental flows.\n"
            "5. Evaluate public notice and opportunity for protest.\n"
            "6. Analyze the permit application process and likely conditions imposed.\n"
            "7. Synthesize findings to determine feasibility and compliance."
        ),
        key_factors=[
            "Source and quality of wastewater",
            "Proposed reuse application",
            "TCEQ treatment standards",
            "Impact on other rights",
            "Permit conditions"
        ],
        primary_authority=[
            "Texas Water Code § 26.0271",
            "TCEQ Rules (30 TAC Chapter 210)"
        ],
        burden_holder="Applicant",
        adversary_position="Downstream users or environmental groups may protest",
        counter_arguments=[
            "Impairment of rights",
            "Insufficient treatment",
            "Public health concerns"
        ],
        resolution_strategy="TCEQ hearing, permit conditions, judicial review",
        entity_scope="Wastewater generators and users",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="City of Fort Worth v. TCEQ, 346 S.W.3d 834 (Tex. App.—Austin 2011, pet. denied)"
    ),
    DoctrineBlock(
        topic="Water Marketing",
        keywords=["water marketing", "sale", "lease", "transfer", "surface water", "groundwater"],
        conclusion_template="Water rights may be marketed (sold or leased) in Texas, subject to statutory and regulatory constraints designed to protect other rights and the public interest.",
        reasoning_framework=(
            "1. Identify the type of water right (surface or groundwater, permit or certificate).\n"
            "2. Review statutory and regulatory requirements for sale, lease, or transfer.\n"
            "3. Assess the need for agency approval (TCEQ for surface water, GCD for groundwater).\n"
            "4. Evaluate the impact on existing rights, environmental flows, and local supplies.\n"
            "5. Consider notice, protest, and public interest review procedures.\n"
            "6. Analyze any special rules for interbasin transfers or out-of-district sales.\n"
            "7. Synthesize findings to determine legal validity and enforceability."
        ),
        key_factors=[
            "Type of right",
            "Nature of transaction",
            "Agency approval",
            "Impact on other rights",
            "Public interest"
        ],
        primary_authority=[
            "Texas Water Code § 11.0831",
            "Texas Water Code Chapter 36"
        ],
        burden_holder="Seller and buyer",
        adversary_position="Regulators or affected parties may challenge",
        counter_arguments=[
            "Impairment of rights",
            "Local supply depletion",
            "Procedural defects"
        ],
        resolution_strategy="Agency review, administrative appeal, litigation",
        entity_scope="Water right holders and market participants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="South Plains Lamesa R.R. v. High Plains Underground Water Conservation Dist., 52 S.W.3d 770 (Tex. App.—Amarillo 2001, no pet.)"
    ),
    DoctrineBlock(
        topic="Edwards Aquifer Authority",
        keywords=["Edwards Aquifer", "authority", "groundwater", "permitting", "special district"],
        conclusion_template="The Edwards Aquifer Authority regulates groundwater withdrawals from the Edwards Aquifer through a permit system that supersedes the Rule of Capture.",
        reasoning_framework=(
            "1. Confirm the well's location within the Edwards Aquifer Authority boundaries.\n"
            "2. Review the Authority's enabling act and adopted rules.\n"
            "3. Determine eligibility for a groundwater withdrawal permit.\n"
            "4. Assess permit limits, metering, and reporting requirements.\n"
            "5. Consider exemptions and grandfathered rights.\n"
            "6. Evaluate enforcement mechanisms and available appeals.\n"
            "7. Synthesize findings to determine compliance and risk."
        ),
        key_factors=[
            "Location within Authority",
            "Permit eligibility",
            "Withdrawal limits",
            "Metering and reporting",
            "Exemptions"
        ],
        primary_authority=[
            "Edwards Aquifer Authority Act",
            "Texas Water Code Chapter 36"
        ],
        burden_holder="Applicant or well owner",
        adversary_position="Authority may deny or limit permit",
        counter_arguments=[
            "Exemption claims",
            "Unconstitutional taking",
            "Pre-existing rights"
        ],
        resolution_strategy="Authority hearing, administrative appeal, litigation",
        entity_scope="Groundwater users in Edwards Aquifer region",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)"
    ),
    DoctrineBlock(
        topic="Ogallala Aquifer Depletion",
        keywords=["Ogallala Aquifer", "depletion", "groundwater", "conservation", "GCD"],
        conclusion_template="Depletion of the Ogallala Aquifer is managed primarily through local GCD rules, with a focus on conservation and sustainable yield.",
        reasoning_framework=(
            "1. Identify the GCD(s) with jurisdiction over the relevant portion of the Ogallala Aquifer.\n"
            "2. Review GCD rules on production limits, well spacing, and conservation measures.\n"
            "3. Assess the impact of pumping on aquifer levels and neighboring wells.\n"
            "4. Consider state and regional planning efforts (e.g., Desired Future Conditions).\n"
            "5. Evaluate enforcement and compliance mechanisms.\n"
            "6. Synthesize findings to determine the adequacy of depletion management."
        ),
        key_factors=[
            "GCD jurisdiction",
            "Production limits",
            "Conservation measures",
            "Regional planning",
            "Aquifer monitoring"
        ],
        primary_authority=[
            "Texas Water Code Chapter 36",
            "Local GCD rules"
        ],
        burden_holder="Well owner",
        adversary_position="GCD may impose stricter limits or deny permits",
        counter_arguments=[
            "Economic hardship",
            "Pre-existing rights",
            "Insufficient scientific basis"
        ],
        resolution_strategy="GCD hearings, stakeholder engagement, judicial review",
        entity_scope="Groundwater users in Ogallala region",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="City of Lubbock v. Coyote Lake Ranch, LLC, 498 S.W.3d 53 (Tex. 2016)"
    ),
    DoctrineBlock(
        topic="Brackish Water Zones",
        keywords=["brackish water", "groundwater", "desalination", "GCD", "TCEQ"],
        conclusion_template="Brackish groundwater production is subject to special permitting and monitoring requirements to encourage development while protecting freshwater resources.",
        reasoning_framework=(
            "1. Identify the location and classification of the brackish water zone.\n"
            "2. Review TCEQ and GCD rules for brackish groundwater production.\n"
            "3. Assess permitting, reporting, and monitoring requirements.\n"
            "4. Evaluate potential impacts on freshwater aquifers and other users.\n"
            "5. Consider incentives or expedited permitting for brackish water projects.\n"
            "6. Synthesize findings to determine compliance and project viability."
        ),
        key_factors=[
            "Zone classification",
            "Permitting requirements",
            "Monitoring and reporting",
            "Impact on freshwater",
            "Project incentives"
        ],
        primary_authority=[
            "Texas Water Code Chapter 36, Subchapter L",
            "TCEQ Brackish Groundwater Production Zones"
        ],
        burden_holder="Project developer",
        adversary_position="GCD or other users may challenge on impact grounds",
        counter_arguments=[
            "Freshwater contamination",
            "Insufficient monitoring",
            "Resource depletion"
        ],
        resolution_strategy="Agency review, stakeholder consultation, adaptive management",
        entity_scope="Brackish water producers",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="Texas Water Code § 36.1015"
    ),
    DoctrineBlock(
        topic="Desalination Permits",
        keywords=["desalination", "permit", "brackish water", "surface water", "TCEQ", "reuse"],
        conclusion_template="Desalination projects require TCEQ permits for water rights, discharge, and, in some cases, groundwater production.",
        reasoning_framework=(
            "1. Identify the source water for desalination (brackish groundwater, seawater, surface water).\n"
            "2. Review TCEQ permitting requirements for intake, discharge, and reuse.\n"
            "3. Assess compliance with water quality and environmental standards.\n"
            "4. Evaluate potential impacts on other water rights and resources.\n"
            "5. Consider public notice, protest, and hearing procedures.\n"
            "6. Synthesize findings to determine project feasibility and compliance."
        ),
        key_factors=[
            "Source water type",
            "Permitting requirements",
            "Discharge standards",
            "Impact on other rights",
            "Public participation"
        ],
        primary_authority=[
            "Texas Water Code § 11.1405",
            "TCEQ Rules (30 TAC Chapter 318)"
        ],
        burden_holder="Project sponsor",
        adversary_position="Regulators or affected parties may protest",
        counter_arguments=[
            "Environmental harm",
            "Impairment of rights",
            "Insufficient mitigation"
        ],
        resolution_strategy="TCEQ hearing, permit conditions, judicial review",
        entity_scope="Desalination project developers",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="Texas Water Code § 11.1405"
    ),
    DoctrineBlock(
        topic="Interstate Compacts",
        keywords=["interstate compact", "water allocation", "state boundaries", "federal law", "Rio Grande Compact", "Pecos River Compact"],
        conclusion_template="Texas is party to several interstate water compacts that allocate river flows among states and are enforceable as federal law.",
        reasoning_framework=(
            "1. Identify the relevant interstate compact and its terms.\n"
            "2. Review the allocation formula and obligations for each state.\n"
            "3. Assess compliance with compact delivery requirements.\n"
            "4. Consider the role of federal agencies in enforcement.\n"
            "5. Evaluate remedies for noncompliance, including litigation in the U.S. Supreme Court.\n"
            "6. Synthesize findings to determine Texas’s rights and obligations."
        ),
        key_factors=[
            "Compact terms",
            "Allocation formula",
            "Compliance monitoring",
            "Federal oversight",
            "Remedies for breach"
        ],
        primary_authority=[
            "Rio Grande Compact, 53 Stat. 785 (1939)",
            "Pecos River Compact, 63 Stat. 159 (1949)",
            "U.S. Constitution Art. I, § 10, cl. 3"
        ],
        burden_holder="State of Texas",
        adversary_position="Other compact states may allege underdelivery",
        counter_arguments=[
            "Force majeure (drought)",
            "Measurement disputes",
            "Federal preemption"
        ],
        resolution_strategy="Interstate negotiation, compact commission, U.S. Supreme Court litigation",
        entity_scope="State governments and agencies",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Texas v. New Mexico, 462 U.S. 554 (1983)"
    ),
    DoctrineBlock(
        topic="Rio Grande Compact",
        keywords=["Rio Grande Compact", "interstate", "allocation", "Texas", "New Mexico", "Colorado"],
        conclusion_template="The Rio Grande Compact apportions the waters of the Rio Grande among Colorado, New Mexico, and Texas, with specific delivery obligations.",
        reasoning_framework=(
            "1. Review the Compact’s apportionment formula and delivery schedules.\n"
            "2. Assess Texas’s annual entitlements and obligations.\n"
            "3. Monitor compliance by upstream states and report discrepancies.\n"
            "4. Consider the role of the Rio Grande Compact Commission and federal agencies.\n"
            "5. Evaluate remedies for underdelivery or breach, including Supreme Court litigation.\n"
            "6. Synthesize findings to determine Texas’s position and options."
        ),
        key_factors=[
            "Compact formula",
            "Annual deliveries",
            "Measurement and reporting",
            "Interstate enforcement",
            "Federal oversight"
        ],
        primary_authority=[
            "Rio Grande Compact, 53 Stat. 785 (1939)",
            "Texas Water Code § 11.302"
        ],
        burden_holder="State of Texas",
        adversary_position="New Mexico or Colorado may contest Texas’s claims",
        counter_arguments=[
            "Drought or force majeure",
            "Measurement error",
            "Equitable apportionment"
        ],
        resolution_strategy="Compact commission, negotiation, Supreme Court litigation",
        entity_scope="State governments and agencies",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Texas v. New Mexico, 462 U.S. 554 (1983)"
    ),
    DoctrineBlock(
        topic="Pecos River Compact",
        keywords=["Pecos River Compact", "interstate", "allocation", "Texas", "New Mexico"],
        conclusion_template="The Pecos River Compact governs allocation of the Pecos River between Texas and New Mexico, with oversight by a federal river master.",
        reasoning_framework=(
            "1. Review the Compact’s allocation formula and obligations.\n"
            "2. Assess Texas’s annual water entitlements and delivery requirements.\n"
            "3. Monitor compliance and report disputes to the river master.\n"
            "4. Consider remedies for underdelivery, including litigation.\n"
            "5. Synthesize findings to determine Texas’s rights and enforcement options."
        ),
        key_factors=[
            "Compact formula",
            "Annual entitlements",
            "River master oversight",
            "Dispute resolution",
            "Federal enforcement"
        ],
        primary_authority=[
            "Pecos River Compact, 63 Stat. 159 (1949)",
            "Texas Water Code § 11.303"
        ],
        burden_holder="State of Texas",
        adversary_position="New Mexico may allege overuse or underdelivery",
        counter_arguments=[
            "Measurement disputes",
            "Force majeure",
            "Equitable apportionment"
        ],
        resolution_strategy="River master review, negotiation, Supreme Court litigation",
        entity_scope="State governments and agencies",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Texas v. New Mexico, 482 U.S. 124 (1987)"
    ),
    DoctrineBlock(
        topic="Water Conservation Requirements",
        keywords=["water conservation", "requirements", "TCEQ", "municipal", "industrial", "conservation plan"],
        conclusion_template="Water right holders and permittees must implement conservation measures and submit conservation plans as required by TCEQ.",
        reasoning_framework=(
            "1. Identify the type of water use (municipal, industrial, agricultural).\n"
            "2. Review TCEQ rules for conservation planning and reporting.\n"
            "3. Assess the adequacy of the submitted conservation plan.\n"
            "4. Evaluate compliance with conservation targets and best management practices.\n"
            "5. Consider enforcement actions for noncompliance.\n"
            "6. Synthesize findings to determine compliance and risk."
        ),
        key_factors=[
            "Type of use",
            "Conservation plan content",
            "TCEQ requirements",
            "Implementation and reporting",
            "Enforcement actions"
        ],
        primary_authority=[
            "Texas Water Code § 11.1271",
            "TCEQ Rules (30 TAC § 288)"
        ],
        burden_holder="Water right holder or permittee",
        adversary_position="TCEQ may find plan inadequate or noncompliant",
        counter_arguments=[
            "Economic hardship",
            "Technological infeasibility",
            "Alternative measures"
        ],
        resolution_strategy="TCEQ review, administrative appeal, plan revision",
        entity_scope="Municipal, industrial, and agricultural users",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.1271"
    ),
    DoctrineBlock(
        topic="Drought Contingency",
        keywords=["drought", "contingency plan", "TCEQ", "curtailment", "emergency order"],
        conclusion_template="Water suppliers must adopt and implement drought contingency plans to manage water use during shortages, subject to TCEQ oversight.",
        reasoning_framework=(
            "1. Review TCEQ requirements for drought contingency planning.\n"
            "2. Assess the adequacy and enforceability of the plan.\n"
            "3. Evaluate triggers for implementation and stages of curtailment.\n"
            "4. Consider public notice and stakeholder input.\n"
            "5. Analyze compliance with emergency orders and curtailment priorities.\n"
            "6. Synthesize findings to determine legal sufficiency and risk."
        ),
        key_factors=[
            "Plan content",
            "Implementation triggers",
            "Curtailment priorities",
            "TCEQ oversight",
            "Stakeholder input"
        ],
        primary_authority=[
            "Texas Water Code § 11.1272",
            "TCEQ Rules (30 TAC § 288)"
        ],
        burden_holder="Water supplier",
        adversary_position="TCEQ may require plan revision or enforcement",
        counter_arguments=[
            "Insufficient curtailment",
            "Economic impact",
            "Alternative measures"
        ],
        resolution_strategy="TCEQ review, administrative appeal, plan revision",
        entity_scope="Municipal and wholesale water suppliers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.1272"
    ),
    DoctrineBlock(
        topic="Water Availability Modeling",
        keywords=["water availability", "modeling", "TCEQ", "surface water", "WRAP", "hydrology"],
        conclusion_template="TCEQ uses Water Availability Models (WAMs) to evaluate the availability of unappropriated surface water for permitting decisions.",
        reasoning_framework=(
            "1. Identify the relevant river basin and WAM model.\n"
            "2. Review the assumptions and data inputs for the model.\n"
            "3. Assess the reliability and limitations of model outputs.\n"
            "4. Evaluate the impact of existing rights, environmental flows, and return flows.\n"
            "5. Consider the role of modeling in permit application review and protests.\n"
            "6. Synthesize findings to determine the likelihood of water availability."
        ),
        key_factors=[
            "Model selection",
            "Data inputs",
            "Existing rights",
            "Environmental flows",
            "Model limitations"
        ],
        primary_authority=[
            "Texas Water Code § 11.150",
            "TCEQ Water Availability Modeling Rules"
        ],
        burden_holder="Permit applicant",
        adversary_position="Protestants may challenge model assumptions or outputs",
        counter_arguments=[
            "Model uncertainty",
            "Unaccounted return flows",
            "Changing hydrology"
        ],
        resolution_strategy="TCEQ review, technical hearings, model refinement",
        entity_scope="Surface water permit applicants and protestants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.150"
    ),
    # Additional doctrines to reach 40+ entries
    DoctrineBlock(
        topic="Groundwater Ownership in Place",
        keywords=["groundwater", "ownership in place", "property right", "landowner", "Day v. EAA"],
        conclusion_template="Groundwater beneath the land is owned in place by the landowner, subject to reasonable regulation by the state.",
        reasoning_framework=(
            "1. Establish landowner title to the surface estate.\n"
            "2. Confirm that the water in question is groundwater, not state-owned surface water.\n"
            "3. Review the Texas Supreme Court’s recognition of ownership in place.\n"
            "4. Assess the scope of the right, including the right to produce and use groundwater.\n"
            "5. Evaluate limits imposed by GCDs or special districts.\n"
            "6. Consider takings claims and regulatory compensation.\n"
            "7. Synthesize findings to determine the extent of the property right."
        ),
        key_factors=[
            "Landowner status",
            "Nature of groundwater",
            "Regulatory limits",
            "Takings claims",
            "District rules"
        ],
        primary_authority=[
            "Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)",
            "Texas Water Code Chapter 36"
        ],
        burden_holder="Landowner",
        adversary_position="State or GCD may limit production",
        counter_arguments=[
            "Reasonable regulation",
            "Public interest",
            "Takings compensation"
        ],
        resolution_strategy="Litigation, administrative appeal, legislative amendment",
        entity_scope="Landowners and groundwater users",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Edwards Aquifer Authority v. Day, 369 S.W.3d 814 (Tex. 2012)"
    ),
    DoctrineBlock(
        topic="Groundwater Production Permits",
        keywords=["groundwater", "production permit", "GCD", "application", "hearing"],
        conclusion_template="A production permit from the local GCD is required for most non-exempt groundwater wells.",
        reasoning_framework=(
            "1. Identify the GCD with jurisdiction over the well.\n"
            "2. Review GCD rules for permit application and review.\n"
            "3. Assess whether the well qualifies for an exemption.\n"
            "4. Evaluate the criteria for permit issuance, including spacing, production limits, and conservation goals.\n"
            "5. Consider notice, protest, and hearing procedures.\n"
            "6. Analyze the likelihood of permit approval and conditions imposed."
        ),
        key_factors=[
            "GCD jurisdiction",
            "Exemption status",
            "Permit criteria",
            "Notice and protest",
            "Hearing procedures"
        ],
        primary_authority=[
            "Texas Water Code Chapter 36",
            "Local GCD rules"
        ],
        burden_holder="Applicant",
        adversary_position="GCD or protestants may challenge application",
        counter_arguments=[
            "Resource depletion",
            "Impairment of existing wells",
            "Noncompliance with rules"
        ],
        resolution_strategy="GCD hearing, administrative appeal, judicial review",
        entity_scope="Groundwater users in GCDs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 36.113"
    ),
    DoctrineBlock(
        topic="Groundwater Export Permits",
        keywords=["groundwater", "export", "permit", "GCD", "out-of-district transfer"],
        conclusion_template="Exporting groundwater outside a GCD’s boundaries generally requires a special export permit, subject to additional scrutiny.",
        reasoning_framework=(
            "1. Identify the GCD with jurisdiction over the well.\n"
            "2. Review statutory and GCD rules for export permits.\n"
            "3. Assess the impact of export on local resources and users.\n"
            "4. Evaluate permit criteria, including conservation and mitigation requirements.\n"
            "5. Consider notice, protest, and hearing procedures.\n"
            "6. Analyze the likelihood of permit approval and conditions imposed."
        ),
        key_factors=[
            "GCD jurisdiction",
            "Export permit criteria",
            "Impact on local resources",
            "Mitigation requirements",
            "Hearing procedures"
        ],
        primary_authority=[
            "Texas Water Code § 36.122",
            "Local GCD rules"
        ],
        burden_holder="Exporter",
        adversary_position="GCD or local users may protest export",
        counter_arguments=[
            "Resource depletion",
            "Impairment of local supply",
            "Noncompliance with rules"
        ],
        resolution_strategy="GCD hearing, administrative appeal, judicial review",
        entity_scope="Groundwater exporters",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 36.122"
    ),
    DoctrineBlock(
        topic="Surface Water Adjudication",
        keywords=["surface water", "adjudication", "certificate of adjudication", "TCEQ", "priority date"],
        conclusion_template="Surface water rights not previously permitted were adjudicated and converted to certificates of adjudication by the state.",
        reasoning_framework=(
            "1. Identify the water right and its historical basis.\n"
            "2. Review the adjudication process and resulting certificate.\n"
            "3. Assess the priority date and conditions of use.\n"
            "4. Evaluate the validity of the certificate and any amendments.\n"
            "5. Consider challenges to the adjudication or certificate.\n"
            "6. Synthesize findings to determine enforceability."
        ),
        key_factors=[
            "Historical right",
            "Certificate of adjudication",
            "Priority date",
            "Conditions of use",
            "Challenges to adjudication"
        ],
        primary_authority=[
            "Texas Water Code Chapter 11, Subchapter G",
            "TCEQ Rules"
        ],
        burden_holder="Certificate holder",
        adversary_position="Protestants may challenge validity or priority",
        counter_arguments=[
            "Improper adjudication",
            "Forfeiture or abandonment",
            "Procedural defects"
        ],
        resolution_strategy="TCEQ review, administrative appeal, litigation",
        entity_scope="Surface water right holders",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="State v. Hidalgo County Water Control & Improvement Dist. No. 18, 443 S.W.2d 728 (Tex. 1969)"
    ),
    DoctrineBlock(
        topic="Surface Water Cancellation",
        keywords=["surface water", "cancellation", "forfeiture", "nonuse", "TCEQ"],
        conclusion_template="Surface water rights may be cancelled by TCEQ for nonuse, subject to statutory procedures and defenses.",
        reasoning_framework=(
            "1. Identify the right and period of nonuse.\n"
            "2. Review TCEQ rules for cancellation proceedings.\n"
            "3. Assess any defenses to cancellation (e.g., force majeure, good cause).\n"
            "4. Evaluate notice and hearing procedures.\n"
            "5. Consider the impact of cancellation on other rights and system operations.\n"
            "6. Synthesize findings to determine risk of cancellation."
        ),
        key_factors=[
            "Period of nonuse",
            "Defenses to cancellation",
            "Notice and hearing",
            "Impact on other rights",
            "TCEQ procedures"
        ],
        primary_authority=[
            "Texas Water Code § 11.173",
            "TCEQ Rules (30 TAC § 297.71)"
        ],
        burden_holder="Right holder",
        adversary_position="TCEQ may initiate cancellation",
        counter_arguments=[
            "Good cause for nonuse",
            "Force majeure",
            "Statutory exceptions"
        ],
        resolution_strategy="TCEQ hearing, administrative appeal, judicial review",
        entity_scope="Surface water right holders",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.173"
    ),
    DoctrineBlock(
        topic="Surface Water Reallocation",
        keywords=["surface water", "reallocation", "priority call", "curtailment", "TCEQ"],
        conclusion_template="During shortages, TCEQ may reallocate or curtail surface water use based on priority, subject to statutory exceptions.",
        reasoning_framework=(
            "1. Identify the nature and cause of the shortage.\n"
            "2. Review the priority dates of affected rights.\n"
            "3. Assess statutory exceptions (e.g., municipal preference, domestic/livestock use).\n"
            "4. Evaluate TCEQ’s curtailment orders and enforcement mechanisms.\n"
            "5. Consider remedies for affected junior appropriators.\n"
            "6. Synthesize findings to determine the legal effect of curtailment."
        ),
        key_factors=[
            "Shortage cause",
            "Priority dates",
            "Statutory exceptions",
            "Curtailment order",
            "Remedies for juniors"
        ],
        primary_authority=[
            "Texas Water Code § 11.053",
            "TCEQ Rules"
        ],
        burden_holder="Junior appropriator",
        adversary_position="Senior appropriator may demand curtailment",
        counter_arguments=[
            "Statutory preference",
            "Public health and safety",
            "Alternative supplies"
        ],
        resolution_strategy="TCEQ enforcement, administrative appeal, litigation",
        entity_scope="Surface water right holders",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.053"
    ),
    DoctrineBlock(
        topic="Surface Water Return Flows",
        keywords=["surface water", "return flows", "reuse", "TCEQ", "downstream rights"],
        conclusion_template="Return flows from permitted surface water use may be recaptured or reused, subject to TCEQ approval and protection of downstream rights.",
        reasoning_framework=(
            "1. Identify the source and nature of the return flow.\n"
            "2. Review TCEQ rules for reuse and recapture.\n"
            "3. Assess the impact on downstream appropriators and environmental flows.\n"
            "4. Evaluate the need for a new or amended permit.\n"
            "5. Consider notice, protest, and hearing procedures.\n"
            "6. Synthesize findings to determine legal status of reuse."
        ),
        key_factors=[
            "Source of return flow",
            "Reuse proposal",
            "Impact on downstream rights",
            "Permit requirements",
            "TCEQ procedures"
        ],
        primary_authority=[
            "Texas Water Code § 11.042",
            "TCEQ Rules (30 TAC § 297.101)"
        ],
        burden_holder="Applicant for reuse",
        adversary_position="Downstream users may protest",
        counter_arguments=[
            "Impairment of rights",
            "Environmental harm",
            "Procedural defects"
        ],
        resolution_strategy="TCEQ review, administrative appeal, judicial review",
        entity_scope="Surface water right holders",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.042"
    ),
    DoctrineBlock(
        topic="Groundwater Well Spacing",
        keywords=["groundwater", "well spacing", "GCD", "protection of wells", "production limits"],
        conclusion_template="GCDs may adopt well spacing rules to prevent interference and protect aquifer resources.",
        reasoning_framework=(
            "1. Identify the GCD and its adopted well spacing rules.\n"
            "2. Review the minimum distances required between wells and property lines.\n"
            "3. Assess the impact of spacing on well performance and aquifer protection.\n"
            "4. Evaluate exemptions or variances available under GCD rules.\n"
            "5. Consider enforcement and remedies for violations.\n"
            "6. Synthesize findings to determine compliance."
        ),
        key_factors=[
            "GCD rules",
            "Well location",
            "Spacing requirements",
            "Exemptions or variances",
            "Enforcement"
        ],
        primary_authority=[
            "Texas Water Code § 36.116",
            "Local GCD rules"
        ],
        burden_holder="Well owner",
        adversary_position="GCD may deny permit or require relocation",
        counter_arguments=[
            "Variance request",
            "Technical infeasibility",
            "Minimal impact"
        ],
        resolution_strategy="GCD hearing, administrative appeal, judicial review",
        entity_scope="Groundwater users in GCDs",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 36.116"
    ),
    DoctrineBlock(
        topic="Groundwater Metering and Reporting",
        keywords=["groundwater", "metering", "reporting", "GCD", "compliance"],
        conclusion_template="GCDs may require metering and periodic reporting of groundwater production to ensure compliance with district rules.",
        reasoning_framework=(
            "1. Review GCD rules for metering and reporting requirements.\n"
            "2. Assess the type of meter required and installation standards.\n"
            "3. Evaluate reporting frequency and data submission procedures.\n"
            "4. Consider penalties for noncompliance or falsification.\n"
            "5. Synthesize findings to determine compliance and risk."
        ),
        key_factors=[
            "GCD rules",
            "Meter installation",
            "Reporting frequency",
            "Penalties for noncompliance",
            "Data accuracy"
        ],
        primary_authority=[
            "Texas Water Code § 36.121",
            "Local GCD rules"
        ],
        burden_holder="Well owner",
        adversary_position="GCD may impose penalties or revoke permit",
        counter_arguments=[
            "Technical infeasibility",
            "Economic hardship",
            "Minimal production"
        ],
        resolution_strategy="GCD hearing, administrative appeal, compliance plan",
        entity_scope="Groundwater users in GCDs",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 36.121"
    ),
    DoctrineBlock(
        topic="Groundwater Conservation Tax",
        keywords=["groundwater", "conservation tax", "GCD", "funding", "ad valorem tax"],
        conclusion_template="GCDs may levy an ad valorem tax to fund district operations, subject to statutory limits and voter approval.",
        reasoning_framework=(
            "1. Review the GCD’s enabling legislation for taxing authority.\n"
            "2. Assess the statutory limits on tax rates.\n"
            "3. Evaluate the process for voter approval of tax levies.\n"
            "4. Consider the use of tax revenues for district operations and conservation programs.\n"
            "5. Synthesize findings to determine legality and scope of tax."
        ),
        key_factors=[
            "GCD enabling act",
            "Tax rate limits",
            "Voter approval",
            "Use of funds",
            "Statutory compliance"
        ],
        primary_authority=[
            "Texas Water Code § 36.201",
            "Local GCD rules"
        ],
        burden_holder="GCD",
        adversary_position="Taxpayers may challenge tax or rate",
        counter_arguments=[
            "Excessive tax rate",
            "Improper use of funds",
            "Procedural defects"
        ],
        resolution_strategy="Voter referendum, administrative appeal, litigation",
        entity_scope="Landowners in GCDs",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 36.201"
    ),
    DoctrineBlock(
        topic="Groundwater Management Areas (GMAs)",
        keywords=["groundwater management area", "GMA", "desired future conditions", "joint planning", "GCD"],
        conclusion_template="GCDs within a GMA must jointly adopt Desired Future Conditions (DFCs) for aquifers, subject to state oversight.",
        reasoning_framework=(
            "1. Identify the GMA and participating GCDs.\n"
            "2. Review the process for joint planning and DFC adoption.\n"
            "3. Assess the scientific basis and stakeholder input for DFCs.\n"
            "4. Evaluate state oversight by the Texas Water Development Board.\n"
            "5. Consider remedies for disputes or noncompliance.\n"
            "6. Synthesize findings to determine legal sufficiency."
        ),
        key_factors=[
            "GMA boundaries",
            "Joint planning process",
            "DFC scientific basis",
            "Stakeholder input",
            "State oversight"
        ],
        primary_authority=[
            "Texas Water Code § 36.108",
            "Texas Water Development Board rules"
        ],
        burden_holder="GCDs in GMA",
        adversary_position="Stakeholders may challenge DFCs",
        counter_arguments=[
            "Insufficient scientific basis",
            "Lack of stakeholder input",
            "Noncompliance with process"
        ],
        resolution_strategy="TWDB review, administrative appeal, litigation",
        entity_scope="GCDs and stakeholders",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 36.108"
    ),
    DoctrineBlock(
        topic="Aquifer Storage and Recovery (ASR)",
        keywords=["ASR", "aquifer storage and recovery", "permit", "TCEQ", "groundwater recharge"],
        conclusion_template="ASR projects require TCEQ authorization for recharge and recovery of water in aquifers, subject to protection of existing rights.",
        reasoning_framework=(
            "1. Identify the aquifer and proposed ASR project.\n"
            "2. Review TCEQ rules for ASR authorization and monitoring.\n"
            "3. Assess the impact on existing water rights and aquifer resources.\n"
            "4. Evaluate recharge water quality and recovery efficiency.\n"
            "5. Consider public notice, protest, and hearing procedures.\n"
            "6. Synthesize findings to determine project feasibility."
        ),
        key_factors=[
            "Aquifer suitability",
            "ASR permit requirements",
            "Impact on rights",
            "Water quality",
            "Monitoring and reporting"
        ],
        primary_authority=[
            "Texas Water Code Chapter 27",
            "TCEQ Rules (30 TAC § 331.181)"
        ],
        burden_holder="ASR project sponsor",
        adversary_position="Regulators or affected parties may protest",
        counter_arguments=[
            "Impairment of rights",
            "Contamination risk",
            "Low recovery efficiency"
        ],
        resolution_strategy="TCEQ hearing, permit conditions, judicial review",
        entity_scope="ASR project developers",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Water Code Chapter 27"
    ),
    DoctrineBlock(
        topic="Managed Groundwater Recharge",
        keywords=["managed recharge", "groundwater", "recharge project", "permit", "TCEQ"],
        conclusion_template="Managed groundwater recharge projects require TCEQ or GCD approval and must protect water quality and existing rights.",
        reasoning_framework=(
            "1. Identify the recharge project and receiving aquifer.\n"
            "2. Review TCEQ and GCD rules for recharge authorization.\n"
            "3. Assess water quality standards and monitoring requirements.\n"
            "4. Evaluate the impact on existing wells and rights.\n"
            "5. Consider notice, protest, and hearing procedures.\n"
            "6. Synthesize findings to determine compliance."
        ),
        key_factors=[
            "Project design",
            "Permit requirements",
            "Water quality",
            "Impact on rights",
            "Monitoring"
        ],
        primary_authority=[
            "Texas Water Code Chapter 27",
            "TCEQ Rules"
        ],
        burden_holder="Project sponsor",
        adversary_position="Regulators or affected parties may protest",
        counter_arguments=[
            "Contamination risk",
            "Impairment of rights",
            "Insufficient monitoring"
        ],
        resolution_strategy="TCEQ or GCD hearing, permit conditions, judicial review",
        entity_scope="Recharge project developers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Texas Water Code Chapter 27"
    ),
    DoctrineBlock(
        topic="Groundwater Monitoring and Data Collection",
        keywords=["groundwater", "monitoring", "data collection", "GCD", "Texas Water Development Board"],
        conclusion_template="GCDs and the Texas Water Development Board monitor groundwater levels and quality to inform management decisions.",
        reasoning_framework=(
            "1. Identify monitoring wells and data collection protocols.\n"
            "2. Review GCD and TWDB monitoring programs.\n"
            "3. Assess data quality and reporting frequency.\n"
            "4. Evaluate use of data in management and planning.\n"
            "5. Synthesize findings to determine adequacy of monitoring."
        ),
        key_factors=[
            "Monitoring program design",
            "Data quality",
            "Reporting frequency",
            "Use in management",
            "Stakeholder access"
        ],
        primary_authority=[
            "Texas Water Code § 36.1071",
            "TWDB rules"
        ],
        burden_holder="GCDs and TWDB",
        adversary_position="Stakeholders may allege inadequate monitoring",
        counter_arguments=[
            "Insufficient data",
            "Infrequent reporting",
            "Limited access"
        ],
        resolution_strategy="Program improvement, stakeholder engagement, legislative amendment",
        entity_scope="GCDs, TWDB, stakeholders",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Texas Water Code § 36.1071"
    ),
    DoctrineBlock(
        topic="Groundwater Production Fees",
        keywords=["groundwater", "production fee", "GCD", "funding", "user fee"],
        conclusion_template="GCDs may assess production fees on groundwater withdrawals to fund district operations, subject to statutory limits.",
        reasoning_framework=(
            "1. Review GCD rules for production fee assessment.\n"
            "2. Assess statutory limits on fee rates and exemptions.\n"
            "3. Evaluate the process for fee collection and enforcement.\n"
            "4. Consider use of fee revenues for district operations.\n"
            "5. Synthesize findings to determine legality and scope."
        ),
        key_factors=[
            "GCD rules",
            "Fee rate limits",
            "Exemptions",
            "Collection process",
            "Use of funds"
        ],
        primary_authority=[
            "Texas Water Code § 36.205",
            "Local GCD rules"
        ],
        burden_holder="GCD",
        adversary_position="Users may challenge fee or rate",
        counter_arguments=[
            "Excessive fee",
            "Improper use of funds",
            "Procedural defects"
        ],
        resolution_strategy="Administrative appeal, litigation, legislative amendment",
        entity_scope="Groundwater users in GCDs",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 36.205"
    ),
    DoctrineBlock(
        topic="Groundwater Contamination and Remediation",
        keywords=["groundwater", "contamination", "remediation", "TCEQ", "liability"],
        conclusion_template="Groundwater contamination is regulated by TCEQ, with liability for remediation imposed on responsible parties under state and federal law.",
        reasoning_framework=(
            "1. Identify the source and extent of contamination.\n"
            "2. Review TCEQ rules for remediation and reporting.\n"
            "3. Assess liability under state and federal statutes (e.g., CERCLA).\n"
            "4. Evaluate remediation standards and monitoring requirements.\n"
            "5. Consider enforcement actions and penalties.\n"
            "6. Synthesize findings to determine compliance and risk."
        ),
        key_factors=[
            "Source of contamination",
            "Remediation requirements",
            "Liability standards",
            "Monitoring",
            "Enforcement"
        ],
        primary_authority=[
            "Texas Water Code Chapter 26",
            "TCEQ Rules",
            "CERCLA (42 U.S.C. § 9601 et seq.)"
        ],
        burden_holder="Responsible party",
        adversary_position="TCEQ or affected parties may demand remediation",
        counter_arguments=[
            "No causation",
            "Compliance with standards",
            "Statute of limitations"
        ],
        resolution_strategy="TCEQ enforcement, litigation, settlement",
        entity_scope="Groundwater users and responsible parties",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Water Code Chapter 26"
    ),
    DoctrineBlock(
        topic="Surface Water Quality Standards",
        keywords=["surface water", "quality standards", "TCEQ", "discharge permit", "Clean Water Act"],
        conclusion_template="Surface water quality is regulated by TCEQ under state and federal law, with discharge permits required for point sources.",
        reasoning_framework=(
            "1. Identify the source and nature of the discharge.\n"
            "2. Review TCEQ and EPA water quality standards.\n"
            "3. Assess permit requirements and effluent limits.\n"
            "4. Evaluate monitoring and reporting obligations.\n"
            "5. Consider enforcement actions for violations.\n"
            "6. Synthesize findings to determine compliance."
        ),
        key_factors=[
            "Discharge source",
            "Permit requirements",
            "Effluent limits",
            "Monitoring",
            "Enforcement"
        ],
        primary_authority=[
            "Texas Water Code Chapter 26",
            "TCEQ Rules",
            "Clean Water Act (33 U.S.C. § 1251 et seq.)"
        ],
        burden_holder="Discharger",
        adversary_position="TCEQ or EPA may enforce violations",
        counter_arguments=[
            "Compliance with permit",
            "No significant impact",
            "Best management practices"
        ],
        resolution_strategy="TCEQ enforcement, administrative appeal, judicial review",
        entity_scope="Surface water dischargers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Water Code Chapter 26"
    ),
    DoctrineBlock(
        topic="Surface Water Instream Flows",
        keywords=["surface water", "instream flow", "environmental flow", "TCEQ", "permit condition"],
        conclusion_template="TCEQ may impose instream flow requirements on surface water permits to protect environmental flows.",
        reasoning_framework=(
            "1. Identify the proposed permit and affected watercourse.\n"
            "2. Review TCEQ rules for instream flow protection.\n"
            "3. Assess the scientific basis for instream flow requirements.\n"
            "4. Evaluate permit conditions and monitoring obligations.\n"
            "5. Consider challenges by applicants or protestants.\n"
            "6. Synthesize findings to determine enforceability."
        ),
        key_factors=[
            "Permit application",
            "Instream flow science",
            "Permit conditions",
            "Monitoring",
            "Challenges"
        ],
        primary_authority=[
            "Texas Water Code § 11.147",
            "TCEQ Rules"
        ],
        burden_holder="Permit applicant",
        adversary_position="TCEQ or protestants may require stricter flows",
        counter_arguments=[
            "Economic impact",
            "Alternative mitigation",
            "Insufficient scientific basis"
        ],
        resolution_strategy="TCEQ hearing, permit conditions, judicial review",
        entity_scope="Surface water permit applicants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.147"
    ),
    DoctrineBlock(
        topic="Surface Water Interbasin Transfers",
        keywords=["surface water", "interbasin transfer", "TCEQ", "permit", "third-party impacts"],
        conclusion_template="Interbasin transfers of surface water require TCEQ approval and are subject to special statutory requirements to protect the basin of origin.",
        reasoning_framework=(
            "1. Identify the source and receiving basins.\n"
            "2. Review TCEQ rules for interbasin transfer permits.\n"
            "3. Assess statutory requirements for public interest and mitigation.\n"
            "4. Evaluate notice, protest, and hearing procedures.\n"
            "5. Consider conditions to protect the basin of origin.\n"
            "6. Synthesize findings to determine likelihood of approval."
        ),
        key_factors=[
            "Source and receiving basins",
            "Permit requirements",
            "Mitigation measures",
            "Public interest",
            "Basin of origin protection"
        ],
        primary_authority=[
            "Texas Water Code § 11.085",
            "TCEQ Rules"
        ],
        burden_holder="Applicant",
        adversary_position="Basin of origin interests may protest",
        counter_arguments=[
            "Local supply depletion",
            "Economic impact",
            "Alternative sources"
        ],
        resolution_strategy="TCEQ hearing, permit conditions, judicial review",
        entity_scope="Surface water right holders",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.085"
    ),
    DoctrineBlock(
        topic="Surface Water Environmental Flows",
        keywords=["surface water", "environmental flows", "TCEQ", "permit", "instream flow"],
        conclusion_template="TCEQ must consider environmental flow standards in surface water permitting to protect aquatic ecosystems.",
        reasoning_framework=(
            "1. Identify the affected watercourse and proposed permit.\n"
            "2. Review TCEQ rules and adopted environmental flow standards.\n"
            "3. Assess the impact of the proposed diversion on environmental flows.\n"
            "4. Evaluate permit conditions and monitoring requirements.\n"
            "5. Consider challenges by applicants or protestants.\n"
            "6. Synthesize findings to determine compliance."
        ),
        key_factors=[
            "Environmental flow standards",
            "Permit application",
            "Impact assessment",
            "Permit conditions",
            "Monitoring"
        ],
        primary_authority=[
            "Texas Water Code § 11.147",
            "TCEQ Rules"
        ],
        burden_holder="Permit applicant",
        adversary_position="TCEQ or protestants may require stricter flows",
        counter_arguments=[
            "Economic impact",
            "Alternative mitigation",
            "Insufficient scientific basis"
        ],
        resolution_strategy="TCEQ hearing, permit conditions, judicial review",
        entity_scope="Surface water permit applicants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.147"
    ),
    DoctrineBlock(
        topic="Surface Water Domestic and Livestock Use",
        keywords=["surface water", "domestic use", "livestock use", "exemption", "TCEQ"],
        conclusion_template="Domestic and livestock use of surface water is generally exempt from permitting, subject to statutory limits.",
        reasoning_framework=(
            "1. Identify the nature of the use (domestic or livestock).\n"
            "2. Review statutory exemptions for small-scale use.\n"
            "3. Assess the quantity and method of diversion.\n"
            "4. Evaluate compliance with statutory limits and conditions.\n"
            "5. Consider challenges by TCEQ or other users.\n"
            "6. Synthesize findings to determine exemption status."
        ),
        key_factors=[
            "Nature of use",
            "Quantity diverted",
            "Statutory limits",
            "Method of diversion",
            "Challenges"
        ],
        primary_authority=[
            "Texas Water Code § 11.142",
            "TCEQ Rules"
        ],
        burden_holder="User",
        adversary_position="TCEQ or other users may challenge exemption",
        counter_arguments=[
            "Exceeding statutory limits",
            "Non-domestic use",
            "Impairment of rights"
        ],
        resolution_strategy="TCEQ enforcement, administrative appeal, judicial review",
        entity_scope="Small-scale surface water users",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 11.142"
    ),
    DoctrineBlock(
        topic="Groundwater Domestic and Livestock Use",
        keywords=["groundwater", "domestic use", "livestock use", "exemption", "GCD"],
        conclusion_template="Domestic and livestock use of groundwater is generally exempt from GCD permitting, subject to statutory and district limits.",
        reasoning_framework=(
            "1. Identify the nature of the use (domestic or livestock).\n"
            "2. Review statutory and GCD exemptions for small-scale wells.\n"
            "3. Assess the quantity and method of production.\n"
            "4. Evaluate compliance with GCD rules and limits.\n"
            "5. Consider challenges by GCD or other users.\n"
            "6. Synthesize findings to determine exemption status."
        ),
        key_factors=[
            "Nature of use",
            "Quantity produced",
            "Statutory and GCD limits",
            "Well construction",
            "Challenges"
        ],
        primary_authority=[
            "Texas Water Code § 36.117",
            "Local GCD rules"
        ],
        burden_holder="User",
        adversary_position="GCD or other users may challenge exemption",
        counter_arguments=[
            "Exceeding statutory limits",
            "Non-domestic use",
            "Impairment of rights"
        ],
        resolution_strategy="GCD enforcement, administrative appeal, judicial review",
        entity_scope="Small-scale groundwater users",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 36.117"
    ),
    DoctrineBlock(
        topic="Groundwater Well Registration",
        keywords=["groundwater", "well registration", "GCD", "inventory", "compliance"],
        conclusion_template="Most groundwater wells must be registered with the local GCD, even if exempt from permitting.",
        reasoning_framework=(
            "1. Review GCD rules for well registration requirements.\n"
            "2. Assess the process and deadlines for registration.\n"
            "3. Evaluate exemptions and penalties for noncompliance.\n"
            "4. Consider the use of registration data for management and planning.\n"
            "5. Synthesize findings to determine compliance."
        ),
        key_factors=[
            "GCD rules",
            "Registration process",
            "Exemptions",
            "Penalties",
            "Data use"
        ],
        primary_authority=[
            "Texas Water Code § 36.053",
            "Local GCD rules"
        ],
        burden_holder="Well owner",
        adversary_position="GCD may impose penalties for noncompliance",
        counter_arguments=[
            "Exemption status",
            "Administrative error",
            "Minimal impact"
        ],
        resolution_strategy="GCD enforcement, administrative appeal, compliance plan",
        entity_scope="Groundwater well owners",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 36.053"
    ),
    DoctrineBlock(
        topic="Groundwater Well Drilling Standards",
        keywords=["groundwater", "well drilling", "standards", "TCEQ", "GCD"],
        conclusion_template="Well drilling and construction must comply with TCEQ and GCD standards to protect groundwater quality.",
        reasoning_framework=(
            "1. Review TCEQ and GCD rules for well drilling and construction.\n"
            "2. Assess standards for casing, sealing, and location.\n"
            "3. Evaluate inspection and reporting requirements.\n"
            "4. Consider penalties for noncompliance or improper construction.\n"
            "5. Synthesize findings to determine compliance."
        ),
        key_factors=[
            "Drilling standards",
            "Well construction",
            "Inspection",
            "Reporting",
            "Penalties"
        ],
        primary_authority=[
            "Texas Water Code § 1901",
            "TCEQ Rules",
            "Local GCD rules"
        ],
        burden_holder="Well driller/owner",
        adversary_position="TCEQ or GCD may impose penalties",
        counter_arguments=[
            "Compliance with standards",
            "Technical infeasibility",
            "Minimal impact"
        ],
        resolution_strategy="TCEQ or GCD enforcement, administrative appeal, compliance plan",
        entity_scope="Well drillers and owners",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 1901"
    ),
    DoctrineBlock(
        topic="Groundwater Well Plugging",
        keywords=["groundwater", "well plugging", "abandonment", "TCEQ", "GCD"],
        conclusion_template="Abandoned groundwater wells must be properly plugged according to TCEQ and GCD standards to prevent contamination.",
        reasoning_framework=(
            "1. Identify abandoned wells subject to plugging requirements.\n"
            "2. Review TCEQ and GCD rules for plugging standards and procedures.\n"
            "3. Assess deadlines and reporting obligations.\n"
            "4. Evaluate penalties for noncompliance or improper plugging.\n"
            "5. Synthesize findings to determine compliance."
        ),
        key_factors=[
            "Plugging standards",
            "Abandonment determination",
            "Deadlines",
            "Reporting",
            "Penalties"
        ],
        primary_authority=[
            "Texas Water Code § 1901.255",
            "TCEQ Rules",
            "Local GCD rules"
        ],
        burden_holder="Well owner",
        adversary_position="TCEQ or GCD may impose penalties",
        counter_arguments=[
            "Well not abandoned",
            "Compliance with standards",
            "Minimal impact"
        ],
        resolution_strategy="TCEQ or GCD enforcement, administrative appeal, compliance plan",
        entity_scope="Well owners",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Texas Water Code § 1901.255"
    ),
    DoctrineBlock(
        topic="Surface Water Recreational Use",
        keywords=["surface water", "recreational use", "public access", "navigable streams", "TPWD"],
        conclusion_template="Navigable streams are open to public recreational use, subject to state law and private property rights.",
        reasoning_framework=(
            "1. Determine if the stream is legally navigable under Texas law.\n"
            "2. Review statutes and case law on public access rights.\n"
            "3. Assess limitations imposed by private property boundaries.\n"
            "4. Evaluate TPWD rules for recreational use and safety.\n"
            "5. Synthesize findings to determine scope of public use."
        ),
        key_factors=[
            "Navigability",
            "Public access rights",
            "Private property boundaries",
            "TPWD rules",
            "Safety requirements"
        ],
        primary_authority=[
            "Texas Parks & Wildlife Code § 90.001",
            "Texas Water Code § 11.096"
        ],
        burden_holder="Recreational user",
        adversary_position="Landowners may challenge access",
        counter_arguments=[
            "Non-navigable stream",
            "Trespass",
            "Safety violations"
        ],
        resolution_strategy="TPWD enforcement, litigation, legislative amendment",
        entity_scope="Recreational users and landowners",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="State v. Bryan, 284 S.W. 219 (Tex. 1926)"
    ),
    DoctrineBlock(
        topic="Surface Water Flood Control",
        keywords=["surface water", "flood control", "levee", "district", "TCEQ", "permit"],
        conclusion_template="Flood control projects require TCEQ approval and must comply with state and federal standards for safety and environmental protection.",
        reasoning_framework=(
            "1. Identify the proposed flood control project and affected watercourse.\n"
            "2. Review TCEQ rules for project approval and permitting.\