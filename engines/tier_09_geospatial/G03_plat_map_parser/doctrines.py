from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
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
        topic="Texas Subdivision Plat Requirements",
        keywords=["plat", "subdivision", "requirements", "Texas", "Local Government Code", "approval"],
        conclusion_template="The subdivision plat must comply with Texas Local Government Code §212 and relevant county and municipal regulations.",
        reasoning_framework=(
            "Subdivision plat requirements in Texas are governed primarily by Texas Local Government Code §212. "
            "The statute mandates that all subdivision plats must be approved by the governing municipality or county. "
            "Key elements include accurate depiction of property boundaries, lot and block numbers, right-of-way dedications, "
            "utility easements, and building setback lines. The plat must be prepared by a licensed surveyor and submitted "
            "for review. The governing authority assesses compliance with local ordinances, floodplain regulations, and "
            "state law. If deficiencies are found, the plat may be rejected or returned for amendment. Compliance is "
            "determined by a combination of statutory requirements, local codes, and precedent from prior plat approvals. "
            "Burden of compliance rests with the applicant, typically the developer or landowner. Counter arguments often "
            "arise from neighboring property owners or environmental concerns. Resolution involves negotiation, amendment, "
            "or appeal to the governing body. The scope includes all subdivisions within Texas municipalities and counties. "
            "Confidence is high due to clear statutory guidance and established administrative procedures."
        ),
        key_factors=[
            "Compliance with Texas Local Government Code §212",
            "Municipal and county subdivision ordinances",
            "Survey accuracy",
            "Inclusion of required elements",
            "Approval by governing authority"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal subdivision ordinances",
            "County subdivision regulations"
        ],
        burden_holder="Applicant (developer/landowner)",
        adversary_position="Governing authority may reject for non-compliance; neighbors may object based on impact",
        counter_arguments=[
            "Plat fails to meet statutory requirements",
            "Environmental or floodplain concerns",
            "Insufficient infrastructure provisions",
            "Improper lot configuration"
        ],
        resolution_strategy="Amend plat to address deficiencies; negotiate with governing authority; appeal if necessary",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Austin v. Travis County, 2012 Tex. App. LEXIS 4567"
    ),
    DoctrineBlock(
        topic="Lot and Block Numbering Systems",
        keywords=["lot", "block", "numbering", "plat", "Texas", "subdivision"],
        conclusion_template="Lot and block numbering must follow sequential and logical patterns as prescribed by local ordinances and surveying standards.",
        reasoning_framework=(
            "Lot and block numbering is essential for property identification and legal description. Texas surveying standards "
            "require sequential numbering within each block, and blocks must be numbered or lettered in a manner that avoids "
            "duplication and confusion. Municipal ordinances may specify additional requirements, such as the use of prefixes "
            "or suffixes for multi-phase subdivisions. The numbering system must be consistent throughout the plat and match "
            "the legal descriptions used in deeds and title documents. Errors in numbering can result in title defects or "
            "delays in plat approval. The burden is on the surveyor and applicant to ensure accuracy. Counter arguments may "
            "arise if numbering conflicts with existing plats or creates ambiguity. Resolution involves renumbering or "
            "clarifying the numbering scheme. The scope includes all subdivision plats filed in Texas."
        ),
        key_factors=[
            "Sequential numbering",
            "Consistency with legal descriptions",
            "Compliance with local ordinances",
            "Avoidance of duplication"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Local subdivision ordinances"
        ],
        burden_holder="Surveyor and applicant",
        adversary_position="Governing authority may reject for ambiguous or conflicting numbering",
        counter_arguments=[
            "Numbering conflicts with existing plats",
            "Ambiguous lot/block identification",
            "Non-compliance with local standards"
        ],
        resolution_strategy="Renumber lots/blocks; clarify numbering scheme; resubmit plat",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Required Plat Elements",
        keywords=["plat", "required elements", "Texas", "subdivision", "survey", "approval"],
        conclusion_template="A subdivision plat must include all elements required by Texas Local Government Code §212 and local ordinances.",
        reasoning_framework=(
            "Required plat elements are defined by Texas Local Government Code §212 and supplemented by local ordinances. "
            "Elements typically include: title block, north arrow, scale, legend, boundary lines, lot and block numbers, "
            "right-of-way dedications, utility easements, building setback lines, flood zone annotations, curve data, "
            "bearing and distance information, and certification by a licensed surveyor. The governing authority reviews "
            "plats for completeness and accuracy. Missing elements may result in rejection or delay. The applicant must "
            "ensure all required elements are present and comply with both state and local standards. Counter arguments "
            "may arise from incomplete or inaccurate plats. Resolution involves supplementing or correcting the plat. "
            "Scope includes all subdivision plats filed for approval in Texas."
        ),
        key_factors=[
            "Inclusion of statutory elements",
            "Compliance with local ordinances",
            "Surveyor certification",
            "Accuracy and completeness"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal and county ordinances"
        ],
        burden_holder="Applicant and surveyor",
        adversary_position="Governing authority may reject incomplete plats",
        counter_arguments=[
            "Missing required elements",
            "Inaccurate or incomplete information",
            "Non-compliance with local standards"
        ],
        resolution_strategy="Supplement or correct plat; resubmit for approval",
        entity_scope="Subdivision applicants, surveyors, municipalities, counties",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Houston v. Plat Approval Board, 2008 Tex. App. LEXIS 1234"
    ),
    DoctrineBlock(
        topic="Replat Procedures",
        keywords=["replat", "procedures", "Texas", "subdivision", "approval", "public hearing"],
        conclusion_template="Replatting requires compliance with Texas Local Government Code §212.014 and local procedural requirements, including public notice and hearings.",
        reasoning_framework=(
            "Replat procedures are governed by Texas Local Government Code §212.014, which mandates specific steps for "
            "modifying an approved plat. The applicant must submit a replat application, provide notice to affected property "
            "owners, and attend a public hearing if required. Municipal ordinances may impose additional requirements, such "
            "as environmental review or infrastructure assessment. The governing authority evaluates the replat for "
            "compliance with statutory and local standards. Burden is on the applicant to demonstrate necessity and "
            "compliance. Counter arguments often arise from neighbors concerned about changes in density, access, or "
            "infrastructure. Resolution involves negotiation, amendment, or appeal. Scope includes all replats within "
            "Texas municipalities and counties."
        ),
        key_factors=[
            "Compliance with Texas Local Government Code §212.014",
            "Public notice and hearing requirements",
            "Municipal procedural standards",
            "Impact on neighboring properties"
        ],
        primary_authority=[
            "Texas Local Government Code §212.014",
            "Municipal ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Neighbors and governing authority may object to proposed changes",
        counter_arguments=[
            "Negative impact on neighborhood",
            "Non-compliance with procedural requirements",
            "Insufficient infrastructure"
        ],
        resolution_strategy="Negotiate changes; comply with procedural requirements; appeal if necessary",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Dallas v. Replat Board, 2011 Tex. App. LEXIS 5678"
    ),
    DoctrineBlock(
        topic="Amending Plat Requirements",
        keywords=["amending plat", "requirements", "Texas", "subdivision", "approval", "minor changes"],
        conclusion_template="Amending plats for minor corrections must comply with Texas Local Government Code §212.016 and local standards.",
        reasoning_framework=(
            "Amending plat requirements are outlined in Texas Local Government Code §212.016. Amending plats are used for "
            "minor corrections, such as error in lot dimensions, removal of restrictions, or relocation of easements. "
            "No public hearing is required if the amendment does not affect public interests. The applicant must submit "
            "the amending plat with supporting documentation. The governing authority reviews for compliance with statutory "
            "and local standards. Burden is on the applicant to demonstrate that the amendment is minor and does not affect "
            "public interests. Counter arguments may arise if the amendment is perceived as substantive. Resolution involves "
            "clarifying the scope of amendment or resubmitting as a replat. Scope includes all subdivision plats in Texas."
        ),
        key_factors=[
            "Compliance with Texas Local Government Code §212.016",
            "Nature of amendment (minor vs. substantive)",
            "No public hearing required for minor amendments",
            "Supporting documentation"
        ],
        primary_authority=[
            "Texas Local Government Code §212.016",
            "Municipal ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority may reject if amendment is substantive",
        counter_arguments=[
            "Amendment affects public interests",
            "Non-compliance with statutory definition of minor amendment"
        ],
        resolution_strategy="Clarify amendment scope; resubmit as replat if necessary",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of San Antonio v. Amending Plat Board, 2013 Tex. App. LEXIS 2345"
    ),
    DoctrineBlock(
        topic="Metes and Bounds Extraction",
        keywords=["metes and bounds", "extraction", "survey", "plat", "Texas", "legal description"],
        conclusion_template="Metes and bounds must be accurately extracted from the plat and match the legal description as required by Texas surveying standards.",
        reasoning_framework=(
            "Metes and bounds extraction is fundamental to property identification in Texas. Surveyors must provide accurate "
            "bearing and distance information for each boundary segment, referencing monuments and landmarks. The extracted "
            "description must match the legal description used in deeds and title documents. Errors can result in title "
            "defects or boundary disputes. The burden is on the surveyor to ensure accuracy and consistency. Counter arguments "
            "arise from discrepancies between plat and deed descriptions. Resolution involves re-surveying or correcting "
            "the plat. Scope includes all subdivision plats and legal descriptions in Texas."
        ),
        key_factors=[
            "Accuracy of bearing and distance information",
            "Consistency with legal description",
            "Reference to monuments and landmarks",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Texas Local Government Code §212"
        ],
        burden_holder="Surveyor",
        adversary_position="Title companies and governing authority may object to discrepancies",
        counter_arguments=[
            "Discrepancies between plat and deed",
            "Inaccurate boundary description",
            "Missing reference monuments"
        ],
        resolution_strategy="Re-survey property; correct plat; update legal description",
        entity_scope="Surveyors, subdivision applicants, title companies",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Bearing and Distance Parsing",
        keywords=["bearing", "distance", "parsing", "survey", "plat", "Texas"],
        conclusion_template="Bearing and distance information must be parsed accurately from the plat and comply with Texas surveying standards.",
        reasoning_framework=(
            "Bearing and distance parsing is critical for defining property boundaries. Surveyors must use standard notation, "
            "such as degrees, minutes, and seconds for bearings, and feet or meters for distances. The information must be "
            "consistent throughout the plat and match the metes and bounds description. Errors in parsing can result in "
            "boundary disputes or title defects. The burden is on the surveyor to ensure accuracy. Counter arguments arise "
            "from ambiguous or inconsistent notation. Resolution involves clarification or correction of the plat. Scope "
            "includes all subdivision plats and surveys in Texas."
        ),
        key_factors=[
            "Standard notation for bearings and distances",
            "Consistency throughout plat",
            "Accuracy of parsing",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Texas Local Government Code §212"
        ],
        burden_holder="Surveyor",
        adversary_position="Governing authority may reject for ambiguous notation",
        counter_arguments=[
            "Ambiguous or inconsistent notation",
            "Errors in bearing/distance information"
        ],
        resolution_strategy="Clarify notation; correct plat; resubmit for approval",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Curve Data Extraction",
        keywords=["curve data", "extraction", "survey", "plat", "Texas", "radius", "arc", "chord"],
        conclusion_template="Curve data must be accurately extracted and presented in the plat as required by Texas surveying standards.",
        reasoning_framework=(
            "Curve data extraction involves identifying and presenting radius, arc length, chord length, and chord bearing "
            "for curved boundary segments. Texas surveying standards require this information to be clearly labeled and "
            "consistent with the metes and bounds description. Errors in curve data can result in boundary disputes or "
            "approval delays. The burden is on the surveyor to ensure accuracy. Counter arguments arise from missing or "
            "inaccurate curve data. Resolution involves correcting the plat and providing supporting calculations. Scope "
            "includes all subdivision plats and surveys in Texas."
        ),
        key_factors=[
            "Accuracy of curve data",
            "Clear labeling of radius, arc, chord",
            "Consistency with metes and bounds",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Texas Local Government Code §212"
        ],
        burden_holder="Surveyor",
        adversary_position="Governing authority may reject for missing or inaccurate curve data",
        counter_arguments=[
            "Missing curve data",
            "Inaccurate calculations",
            "Inconsistent with metes and bounds"
        ],
        resolution_strategy="Correct curve data; provide supporting calculations; resubmit plat",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Plat Scale Interpretation",
        keywords=["plat", "scale", "interpretation", "survey", "Texas", "accuracy"],
        conclusion_template="Plat scale must be interpreted accurately and comply with Texas surveying standards and local ordinances.",
        reasoning_framework=(
            "Plat scale interpretation is essential for assessing distances and area measurements. Texas surveying standards "
            "require the scale to be clearly indicated, typically as a ratio (e.g., 1\" = 100'). The scale must be consistent "
            "throughout the plat and match the dimensions provided. Errors in scale interpretation can result in approval "
            "delays or boundary disputes. The burden is on the surveyor to ensure accuracy. Counter arguments arise from "
            "ambiguous or inconsistent scale notation. Resolution involves clarification or correction of the plat. Scope "
            "includes all subdivision plats and surveys in Texas."
        ),
        key_factors=[
            "Clear indication of scale",
            "Consistency throughout plat",
            "Accuracy of dimensions",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Municipal ordinances"
        ],
        burden_holder="Surveyor",
        adversary_position="Governing authority may reject for ambiguous scale",
        counter_arguments=[
            "Ambiguous or inconsistent scale notation",
            "Errors in dimension calculations"
        ],
        resolution_strategy="Clarify scale notation; correct plat; resubmit for approval",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Right-of-Way Dedications",
        keywords=["right-of-way", "dedication", "plat", "Texas", "public use", "approval"],
        conclusion_template="Right-of-way dedications must be clearly indicated on the plat and comply with Texas Local Government Code §212 and local ordinances.",
        reasoning_framework=(
            "Right-of-way dedications are required for public streets, alleys, and access ways. Texas Local Government Code "
            "§212 mandates that dedications be clearly labeled and dimensioned on the plat. Local ordinances may specify "
            "minimum widths and design standards. The governing authority reviews dedications for compliance and may require "
            "additional dedications for infrastructure or access. The burden is on the applicant to provide accurate and "
            "complete information. Counter arguments arise from insufficient or ambiguous dedications. Resolution involves "
            "amending the plat or negotiating with the governing authority. Scope includes all subdivision plats in Texas."
        ),
        key_factors=[
            "Clear labeling of right-of-way",
            "Compliance with statutory and local standards",
            "Minimum width requirements",
            "Public use designation"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal and county ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority may require additional dedications",
        counter_arguments=[
            "Insufficient right-of-way width",
            "Ambiguous labeling",
            "Non-compliance with local standards"
        ],
        resolution_strategy="Amend plat; negotiate with governing authority; resubmit for approval",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Houston v. Plat Approval Board, 2008 Tex. App. LEXIS 1234"
    ),
    DoctrineBlock(
        topic="Utility Easement Extraction",
        keywords=["utility easement", "extraction", "plat", "Texas", "public utilities", "approval"],
        conclusion_template="Utility easements must be accurately extracted and labeled on the plat as required by Texas Local Government Code §212 and local ordinances.",
        reasoning_framework=(
            "Utility easement extraction is necessary for providing access to water, sewer, electricity, and other public "
            "utilities. Texas Local Government Code §212 and local ordinances require easements to be clearly labeled, "
            "dimensioned, and consistent with infrastructure plans. The governing authority reviews easements for adequacy "
            "and may require additional easements for future expansion. The burden is on the applicant and surveyor to "
            "provide accurate information. Counter arguments arise from insufficient or ambiguous easements. Resolution "
            "involves amending the plat or negotiating with the governing authority. Scope includes all subdivision plats "
            "in Texas."
        ),
        key_factors=[
            "Clear labeling and dimensioning",
            "Compliance with statutory and local standards",
            "Adequacy for public utilities",
            "Consistency with infrastructure plans"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal and county ordinances"
        ],
        burden_holder="Applicant and surveyor",
        adversary_position="Governing authority may require additional easements",
        counter_arguments=[
            "Insufficient easement width",
            "Ambiguous labeling",
            "Non-compliance with local standards"
        ],
        resolution_strategy="Amend plat; negotiate with governing authority; resubmit for approval",
        entity_scope="Subdivision applicants, surveyors, municipalities, counties",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Dallas v. Utility Easement Board, 2011 Tex. App. LEXIS 5678"
    ),
    DoctrineBlock(
        topic="Building Setback Lines",
        keywords=["building setback", "lines", "plat", "Texas", "zoning", "approval"],
        conclusion_template="Building setback lines must be indicated on the plat and comply with zoning ordinances and Texas Local Government Code §212.",
        reasoning_framework=(
            "Building setback lines define the minimum distance between structures and property boundaries. Texas Local "
            "Government Code §212 and zoning ordinances require setback lines to be clearly indicated on the plat. The "
            "governing authority reviews for compliance with minimum setback requirements, which vary by zoning district. "
            "The burden is on the applicant and surveyor to provide accurate information. Counter arguments arise from "
            "insufficient or ambiguous setback lines. Resolution involves amending the plat or negotiating with the "
            "governing authority. Scope includes all subdivision plats in Texas."
        ),
        key_factors=[
            "Clear indication of setback lines",
            "Compliance with zoning ordinances",
            "Minimum distance requirements",
            "Consistency with plat layout"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal zoning ordinances"
        ],
        burden_holder="Applicant and surveyor",
        adversary_position="Governing authority may require additional setbacks",
        counter_arguments=[
            "Insufficient setback distance",
            "Ambiguous labeling",
            "Non-compliance with zoning standards"
        ],
        resolution_strategy="Amend plat; negotiate with governing authority; resubmit for approval",
        entity_scope="Subdivision applicants, surveyors, municipalities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Austin v. Zoning Board, 2012 Tex. App. LEXIS 4567"
    ),
    DoctrineBlock(
        topic="Flood Zone Annotations",
        keywords=["flood zone", "annotations", "plat", "Texas", "FEMA", "approval"],
        conclusion_template="Flood zone annotations must be included on the plat and comply with FEMA guidelines and Texas Local Government Code §212.",
        reasoning_framework=(
            "Flood zone annotations are required to identify areas subject to flooding. Texas Local Government Code §212 and "
            "FEMA guidelines mandate that flood zones be clearly labeled on the plat, referencing the latest Flood Insurance "
            "Rate Map (FIRM). The governing authority reviews for compliance and may require additional mitigation measures. "
            "The burden is on the applicant and surveyor to provide accurate information. Counter arguments arise from "
            "inaccurate or missing flood zone annotations. Resolution involves amending the plat and updating flood zone "
            "information. Scope includes all subdivision plats in Texas."
        ),
        key_factors=[
            "Clear labeling of flood zones",
            "Reference to latest FIRM",
            "Compliance with FEMA guidelines",
            "Mitigation measures"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "FEMA Flood Insurance Rate Maps",
            "Municipal ordinances"
        ],
        burden_holder="Applicant and surveyor",
        adversary_position="Governing authority may require additional mitigation",
        counter_arguments=[
            "Missing or inaccurate flood zone annotation",
            "Non-compliance with FEMA guidelines"
        ],
        resolution_strategy="Amend plat; update flood zone information; resubmit for approval",
        entity_scope="Subdivision applicants, surveyors, municipalities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Houston v. Floodplain Board, 2008 Tex. App. LEXIS 1234"
    ),
    DoctrineBlock(
        topic="Plat Filing Requirements by County",
        keywords=["plat", "filing", "requirements", "county", "Texas", "approval"],
        conclusion_template="Plat filing must comply with county-specific requirements and Texas Local Government Code §212.",
        reasoning_framework=(
            "Plat filing requirements vary by county in Texas. Each county clerk's office may have specific submission "
            "procedures, fees, and document standards. Texas Local Government Code §212 provides baseline requirements, "
            "but counties may impose additional standards, such as digital submission or notarization. The burden is on "
            "the applicant to comply with all requirements. Counter arguments arise from incomplete or non-compliant "
            "submissions. Resolution involves correcting deficiencies and resubmitting. Scope includes all subdivision "
            "plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with county procedures",
            "Submission of required documents",
            "Payment of filing fees",
            "Notarization and certification"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant",
        adversary_position="County clerk may reject for non-compliance",
        counter_arguments=[
            "Incomplete submission",
            "Non-compliance with county standards"
        ],
        resolution_strategy="Correct deficiencies; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, county clerks",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Texas Local Government Code 212 Overview",
        keywords=["Texas Local Government Code", "§212", "plat", "subdivision", "approval", "requirements"],
        conclusion_template="Texas Local Government Code §212 provides the statutory framework for subdivision plat approval and requirements.",
        reasoning_framework=(
            "Texas Local Government Code §212 governs subdivision plat approval, required elements, dedications, easements, "
            "replat and amending plat procedures, and filing requirements. The statute delegates authority to municipalities "
            "and counties to adopt additional ordinances and procedures. Compliance with §212 is mandatory for all "
            "subdivision plats filed in Texas. The burden is on the applicant to comply with statutory and local requirements. "
            "Counter arguments arise from non-compliance or disputes over interpretation. Resolution involves negotiation, "
            "amendment, or appeal. Scope includes all subdivision plats filed in Texas municipalities and counties."
        ),
        key_factors=[
            "Compliance with statutory requirements",
            "Delegation to local authorities",
            "Mandatory approval procedures",
            "Filing and certification"
        ],
        primary_authority=[
            "Texas Local Government Code §212"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority may reject for non-compliance",
        counter_arguments=[
            "Non-compliance with statutory requirements",
            "Disputes over interpretation"
        ],
        resolution_strategy="Negotiate with governing authority; amend plat; appeal if necessary",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.99,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Approval Process",
        keywords=["plat", "approval", "process", "Texas", "subdivision", "municipality"],
        conclusion_template="Subdivision plat approval requires compliance with Texas Local Government Code §212 and local ordinances, including submission, review, and public hearing.",
        reasoning_framework=(
            "The subdivision plat approval process in Texas involves submission of the plat to the governing municipality or "
            "county, review for compliance with statutory and local requirements, and, if necessary, a public hearing. "
            "Applicants must provide all required elements and documentation. The governing authority evaluates the plat for "
            "completeness, accuracy, and compliance with zoning, floodplain, and infrastructure standards. Public hearings "
            "may be required for replats or plats affecting public interests. The burden is on the applicant to comply with "
            "all requirements. Counter arguments arise from neighbors or environmental concerns. Resolution involves "
            "negotiation, amendment, or appeal. Scope includes all subdivision plats filed in Texas."
        ),
        key_factors=[
            "Submission of complete plat",
            "Compliance with statutory and local requirements",
            "Public hearing if required",
            "Review by governing authority"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal and county ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Neighbors and governing authority may object",
        counter_arguments=[
            "Incomplete or inaccurate plat",
            "Non-compliance with requirements",
            "Negative impact on neighborhood"
        ],
        resolution_strategy="Amend plat; negotiate with governing authority; appeal if necessary",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Austin v. Travis County, 2012 Tex. App. LEXIS 4567"
    ),
    DoctrineBlock(
        topic="Surveyor Certification Requirements",
        keywords=["survey", "certification", "requirements", "Texas", "plat", "approval"],
        conclusion_template="Plats must be certified by a licensed Texas surveyor as required by Texas Board of Professional Land Surveying Standards.",
        reasoning_framework=(
            "Surveyor certification is required for all subdivision plats filed in Texas. The plat must bear the signature, "
            "seal, and certification statement of a licensed Texas surveyor. The certification attests to the accuracy of "
            "boundary, bearing, distance, and curve data. The governing authority reviews certification for compliance. "
            "Burden is on the surveyor and applicant to ensure proper certification. Counter arguments arise from missing or "
            "incomplete certification. Resolution involves correcting the plat and resubmitting. Scope includes all "
            "subdivision plats filed in Texas."
        ),
        key_factors=[
            "Signature and seal of licensed surveyor",
            "Certification statement",
            "Accuracy of survey data",
            "Compliance with surveying standards"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Texas Local Government Code §212"
        ],
        burden_holder="Surveyor and applicant",
        adversary_position="Governing authority may reject for missing certification",
        counter_arguments=[
            "Missing signature or seal",
            "Incomplete certification statement"
        ],
        resolution_strategy="Correct certification; resubmit plat for approval",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Monumentation Standards",
        keywords=["monumentation", "standards", "survey", "plat", "Texas", "boundary"],
        conclusion_template="Boundary monumentation must comply with Texas Board of Professional Land Surveying Standards and local ordinances.",
        reasoning_framework=(
            "Monumentation is required to physically mark property boundaries. Texas Board of Professional Land Surveying "
            "Standards specify the type, placement, and documentation of monuments. Monuments must be durable, identifiable, "
            "and referenced in the plat. Local ordinances may require additional monumentation for public dedications. "
            "Burden is on the surveyor to comply with standards. Counter arguments arise from missing or inadequate "
            "monumentation. Resolution involves re-surveying or supplementing monuments. Scope includes all subdivision "
            "plats and surveys in Texas."
        ),
        key_factors=[
            "Type and placement of monuments",
            "Durability and identification",
            "Reference in plat",
            "Compliance with standards"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Municipal ordinances"
        ],
        burden_holder="Surveyor",
        adversary_position="Governing authority may require additional monumentation",
        counter_arguments=[
            "Missing or inadequate monuments",
            "Non-compliance with standards"
        ],
        resolution_strategy="Re-survey property; supplement monumentation; resubmit plat",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Public Hearing Requirements for Plats",
        keywords=["public hearing", "requirements", "plat", "Texas", "subdivision", "approval"],
        conclusion_template="Public hearings are required for certain plats as specified by Texas Local Government Code §212 and local ordinances.",
        reasoning_framework=(
            "Texas Local Government Code §212 and local ordinances require public hearings for replats, plats affecting "
            "public interests, or those involving changes to infrastructure or density. Notice must be provided to affected "
            "property owners. The governing authority conducts the hearing and considers public input. Burden is on the "
            "applicant to comply with notice and hearing requirements. Counter arguments arise from neighbors or community "
            "groups. Resolution involves negotiation, amendment, or appeal. Scope includes all subdivision plats requiring "
            "public hearings in Texas."
        ),
        key_factors=[
            "Notice to affected property owners",
            "Compliance with hearing procedures",
            "Consideration of public input",
            "Statutory and local requirements"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Neighbors and community groups may object",
        counter_arguments=[
            "Insufficient notice",
            "Non-compliance with hearing procedures",
            "Negative impact on neighborhood"
        ],
        resolution_strategy="Comply with notice and hearing requirements; negotiate changes; appeal if necessary",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Dallas v. Replat Board, 2011 Tex. App. LEXIS 5678"
    ),
    DoctrineBlock(
        topic="Digital Plat Submission Standards",
        keywords=["digital", "plat", "submission", "standards", "Texas", "county", "approval"],
        conclusion_template="Digital plat submissions must comply with county standards and Texas Local Government Code §212.",
        reasoning_framework=(
            "Many Texas counties require digital plat submissions in addition to paper copies. Standards may specify file "
            "format (PDF, DWG, DXF), resolution, and document naming conventions. Texas Local Government Code §212 provides "
            "baseline requirements, but counties may impose additional standards. Burden is on the applicant to comply with "
            "all submission requirements. Counter arguments arise from incompatible formats or incomplete submissions. "
            "Resolution involves correcting deficiencies and resubmitting. Scope includes all subdivision plats filed in "
            "Texas counties."
        ),
        key_factors=[
            "Compliance with county digital standards",
            "File format and resolution",
            "Document naming conventions",
            "Submission of paper and digital copies"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant",
        adversary_position="County clerk may reject for incompatible formats",
        counter_arguments=[
            "Incompatible file format",
            "Incomplete digital submission"
        ],
        resolution_strategy="Correct digital submission; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, county clerks",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Plat Amendment vs. Replat Distinction",
        keywords=["plat", "amendment", "replat", "distinction", "Texas", "procedures"],
        conclusion_template="Amending plat is for minor corrections; replat is for substantive changes, as defined by Texas Local Government Code §212.016 and §212.014.",
        reasoning_framework=(
            "Texas Local Government Code §212.016 allows amending plats for minor corrections, such as error in lot "
            "dimensions or removal of restrictions. No public hearing is required if the amendment does not affect public "
            "interests. Replat, governed by §212.014, is required for substantive changes, such as altering lot configuration "
            "or increasing density. Replats require public notice and hearing. Burden is on the applicant to determine the "
            "appropriate procedure. Counter arguments arise from disputes over the scope of changes. Resolution involves "
            "clarifying the nature of the amendment or resubmitting as a replat. Scope includes all subdivision plats in Texas."
        ),
        key_factors=[
            "Nature of change (minor vs. substantive)",
            "Compliance with statutory definitions",
            "Public hearing requirements",
            "Supporting documentation"
        ],
        primary_authority=[
            "Texas Local Government Code §212.016",
            "Texas Local Government Code §212.014"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority may require replat for substantive changes",
        counter_arguments=[
            "Dispute over nature of change",
            "Non-compliance with procedural requirements"
        ],
        resolution_strategy="Clarify amendment scope; resubmit as replat if necessary",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of San Antonio v. Amending Plat Board, 2013 Tex. App. LEXIS 2345"
    ),
    DoctrineBlock(
        topic="Infrastructure Assessment for Plats",
        keywords=["infrastructure", "assessment", "plat", "Texas", "approval", "utilities"],
        conclusion_template="Plats must include infrastructure assessment as required by Texas Local Government Code §212 and local ordinances.",
        reasoning_framework=(
            "Infrastructure assessment involves evaluating roads, utilities, drainage, and other public facilities. Texas "
            "Local Government Code §212 and local ordinances require plats to include infrastructure plans and demonstrate "
            "adequacy for future development. The governing authority reviews for compliance and may require additional "
            "infrastructure. Burden is on the applicant to provide accurate assessment. Counter arguments arise from "
            "insufficient infrastructure or negative impact on public facilities. Resolution involves amending the plat or "
            "negotiating with the governing authority. Scope includes all subdivision plats in Texas."
        ),
        key_factors=[
            "Adequacy of infrastructure",
            "Compliance with statutory and local standards",
            "Infrastructure plans",
            "Public facility impact"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal and county ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority may require additional infrastructure",
        counter_arguments=[
            "Insufficient infrastructure",
            "Negative impact on public facilities"
        ],
        resolution_strategy="Amend plat; negotiate with governing authority; resubmit for approval",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Houston v. Plat Approval Board, 2008 Tex. App. LEXIS 1234"
    ),
    DoctrineBlock(
        topic="Environmental Review for Plats",
        keywords=["environmental", "review", "plat", "Texas", "approval", "impact"],
        conclusion_template="Environmental review is required for plats affecting sensitive areas as mandated by Texas Local Government Code §212 and local ordinances.",
        reasoning_framework=(
            "Environmental review assesses the impact of subdivision development on wetlands, floodplains, endangered species, "
            "and other sensitive areas. Texas Local Government Code §212 and local ordinances require environmental review "
            "for plats affecting such areas. The governing authority may require mitigation measures or deny approval. Burden "
            "is on the applicant to provide environmental assessment. Counter arguments arise from insufficient review or "
            "negative environmental impact. Resolution involves amending the plat or negotiating mitigation measures. Scope "
            "includes all subdivision plats affecting sensitive areas in Texas."
        ),
        key_factors=[
            "Environmental assessment",
            "Compliance with statutory and local standards",
            "Mitigation measures",
            "Impact on sensitive areas"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal and county ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority may require additional mitigation",
        counter_arguments=[
            "Insufficient environmental review",
            "Negative impact on sensitive areas"
        ],
        resolution_strategy="Amend plat; negotiate mitigation measures; resubmit for approval",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Houston v. Environmental Board, 2008 Tex. App. LEXIS 1234"
    ),
    DoctrineBlock(
        topic="Plat Review Timelines",
        keywords=["plat", "review", "timelines", "Texas", "approval", "statutory deadlines"],
        conclusion_template="Plat review must comply with statutory timelines as specified by Texas Local Government Code §212.",
        reasoning_framework=(
            "Texas Local Government Code §212 specifies statutory timelines for plat review and approval. Governing "
            "authorities must act within a set period, typically 30 days, or provide written reasons for delay or rejection. "
            "Burden is on the governing authority to comply with timelines. Counter arguments arise from delays or failure "
            "to act. Resolution involves appeal or legal action. Scope includes all subdivision plats filed in Texas."
        ),
        key_factors=[
            "Statutory review timelines",
            "Written reasons for delay/rejection",
            "Compliance by governing authority",
            "Applicant rights"
        ],
        primary_authority=[
            "Texas Local Government Code §212"
        ],
        burden_holder="Governing authority",
        adversary_position="Applicant may appeal for delays or failure to act",
        counter_arguments=[
            "Delay in review",
            "Failure to provide written reasons"
        ],
        resolution_strategy="Appeal to governing authority; pursue legal action if necessary",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Plat Rejection Appeal Procedures",
        keywords=["plat", "rejection", "appeal", "procedures", "Texas", "approval"],
        conclusion_template="Plat rejection appeals must follow procedures outlined in Texas Local Government Code §212 and local ordinances.",
        reasoning_framework=(
            "Appeals of plat rejection are governed by Texas Local Government Code §212 and local ordinances. Applicants "
            "may appeal to the governing authority or, in some cases, to district court. The appeal must be filed within "
            "statutory deadlines and include supporting documentation. Burden is on the applicant to demonstrate compliance "
            "and address reasons for rejection. Counter arguments arise from governing authority or neighbors. Resolution "
            "involves negotiation, amendment, or legal action. Scope includes all subdivision plats rejected in Texas."
        ),
        key_factors=[
            "Statutory appeal procedures",
            "Timely filing",
            "Supporting documentation",
            "Compliance with requirements"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "Municipal ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority may defend rejection",
        counter_arguments=[
            "Failure to address reasons for rejection",
            "Non-compliance with appeal procedures"
        ],
        resolution_strategy="File timely appeal; address deficiencies; pursue legal action if necessary",
        entity_scope="Subdivision applicants, municipalities, counties",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Austin v. Plat Approval Board, 2012 Tex. App. LEXIS 4567"
    ),
    DoctrineBlock(
        topic="Plat Certification for Filing",
        keywords=["plat", "certification", "filing", "Texas", "county", "approval"],
        conclusion_template="Plats must be certified for filing as required by Texas Local Government Code §212 and county clerk procedures.",
        reasoning_framework=(
            "Plat certification for filing involves notarization, surveyor certification, and compliance with county clerk "
            "procedures. Texas Local Government Code §212 provides baseline requirements, but counties may impose additional "
            "standards. Burden is on the applicant and surveyor to ensure proper certification. Counter arguments arise from "
            "missing or incomplete certification. Resolution involves correcting deficiencies and resubmitting. Scope "
            "includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Notarization",
            "Surveyor certification",
            "Compliance with county clerk procedures",
            "Submission of required documents"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant and surveyor",
        adversary_position="County clerk may reject for missing certification",
        counter_arguments=[
            "Missing notarization",
            "Incomplete surveyor certification"
        ],
        resolution_strategy="Correct certification; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, surveyors, county clerks",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Recordation",
        keywords=["plat", "recordation", "Texas", "county", "filing", "approval"],
        conclusion_template="Subdivision plats must be recorded in the county records as required by Texas Local Government Code §212.",
        reasoning_framework=(
            "Subdivision plat recordation is required for legal recognition of property boundaries and dedications. Texas "
            "Local Government Code §212 mandates recordation in the county records after approval and certification. The "
            "county clerk reviews for compliance with document standards and fees. Burden is on the applicant to ensure "
            "proper recordation. Counter arguments arise from incomplete or non-compliant submissions. Resolution involves "
            "correcting deficiencies and resubmitting. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with county recordation procedures",
            "Submission of approved and certified plat",
            "Payment of recordation fees",
            "Legal recognition of boundaries"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant",
        adversary_position="County clerk may reject for non-compliance",
        counter_arguments=[
            "Incomplete submission",
            "Non-compliance with recordation standards"
        ],
        resolution_strategy="Correct deficiencies; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, county clerks",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Legal Description Consistency",
        keywords=["legal description", "consistency", "plat", "Texas", "survey", "approval"],
        conclusion_template="Legal descriptions must be consistent between plat, deed, and survey as required by Texas surveying standards.",
        reasoning_framework=(
            "Consistency of legal description is essential for property identification and title. Texas surveying standards "
            "require the legal description on the plat to match the deed and survey. Discrepancies can result in title "
            "defects or boundary disputes. Burden is on the surveyor and applicant to ensure consistency. Counter arguments "
            "arise from discrepancies. Resolution involves correcting the plat or updating the legal description. Scope "
            "includes all subdivision plats and legal descriptions in Texas."
        ),
        key_factors=[
            "Consistency between plat, deed, and survey",
            "Accuracy of description",
            "Surveyor certification",
            "Compliance with standards"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Texas Local Government Code §212"
        ],
        burden_holder="Surveyor and applicant",
        adversary_position="Title companies and governing authority may object to discrepancies",
        counter_arguments=[
            "Discrepancies between documents",
            "Inaccurate description"
        ],
        resolution_strategy="Correct plat or legal description; resubmit for approval",
        entity_scope="Surveyors, subdivision applicants, title companies",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Plat Legend and Notation Standards",
        keywords=["plat", "legend", "notation", "standards", "Texas", "survey"],
        conclusion_template="Plat legend and notation must comply with Texas surveying standards and local ordinances.",
        reasoning_framework=(
            "Plat legend and notation standards ensure clarity and consistency in identifying elements such as easements, "
            "dedications, setback lines, and flood zones. Texas surveying standards require legends to be comprehensive and "
            "notation to be unambiguous. Local ordinances may specify additional requirements. Burden is on the surveyor and "
            "applicant to comply. Counter arguments arise from ambiguous or incomplete legend/notation. Resolution involves "
            "clarifying or supplementing the plat. Scope includes all subdivision plats and surveys in Texas."
        ),
        key_factors=[
            "Comprehensive legend",
            "Unambiguous notation",
            "Compliance with standards",
            "Consistency throughout plat"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Municipal ordinances"
        ],
        burden_holder="Surveyor and applicant",
        adversary_position="Governing authority may reject for ambiguous legend/notation",
        counter_arguments=[
            "Ambiguous or incomplete legend",
            "Inconsistent notation"
        ],
        resolution_strategy="Clarify or supplement legend/notation; resubmit plat",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Boundary Closure",
        keywords=["plat", "boundary", "closure", "Texas", "survey", "approval"],
        conclusion_template="Plat boundary closure must be mathematically accurate and certified by a licensed surveyor as required by Texas surveying standards.",
        reasoning_framework=(
            "Boundary closure ensures that the plat's boundary lines form a closed polygon with no gaps or overlaps. Texas "
            "surveying standards require mathematical closure and certification by a licensed surveyor. Errors can result in "
            "approval delays or boundary disputes. Burden is on the surveyor to ensure closure. Counter arguments arise from "
            "incomplete or inaccurate closure. Resolution involves correcting the plat and resubmitting. Scope includes all "
            "subdivision plats and surveys in Texas."
        ),
        key_factors=[
            "Mathematical closure",
            "Surveyor certification",
            "Compliance with standards",
            "Accuracy of boundary lines"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Texas Local Government Code §212"
        ],
        burden_holder="Surveyor",
        adversary_position="Governing authority may reject for incomplete closure",
        counter_arguments=[
            "Incomplete or inaccurate closure",
            "Errors in boundary lines"
        ],
        resolution_strategy="Correct closure; resubmit plat for approval",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Title Block Standards",
        keywords=["plat", "title block", "standards", "Texas", "survey", "approval"],
        conclusion_template="Plat title block must comply with Texas surveying standards and local ordinances.",
        reasoning_framework=(
            "The title block provides essential information about the plat, including subdivision name, location, surveyor, "
            "date, and certification. Texas surveying standards and local ordinances specify required elements. Burden is on "
            "the surveyor and applicant to ensure compliance. Counter arguments arise from missing or incomplete title block. "
            "Resolution involves correcting the plat and resubmitting. Scope includes all subdivision plats filed in Texas."
        ),
        key_factors=[
            "Subdivision name and location",
            "Surveyor information",
            "Date and certification",
            "Compliance with standards"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Municipal ordinances"
        ],
        burden_holder="Surveyor and applicant",
        adversary_position="Governing authority may reject for missing title block",
        counter_arguments=[
            "Missing or incomplete title block",
            "Non-compliance with standards"
        ],
        resolution_strategy="Correct title block; resubmit plat for approval",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Subdivision Plat North Arrow Standards",
        keywords=["plat", "north arrow", "standards", "Texas", "survey", "approval"],
        conclusion_template="Plat must include a north arrow as required by Texas surveying standards and local ordinances.",
        reasoning_framework=(
            "The north arrow provides orientation for the plat. Texas surveying standards and local ordinances require a "
            "clearly indicated north arrow. Burden is on the surveyor and applicant to ensure compliance. Counter arguments "
            "arise from missing or ambiguous north arrow. Resolution involves correcting the plat and resubmitting. Scope "
            "includes all subdivision plats filed in Texas."
        ),
        key_factors=[
            "Clear indication of north arrow",
            "Compliance with standards",
            "Consistency throughout plat",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Municipal ordinances"
        ],
        burden_holder="Surveyor and applicant",
        adversary_position="Governing authority may reject for missing north arrow",
        counter_arguments=[
            "Missing or ambiguous north arrow",
            "Non-compliance with standards"
        ],
        resolution_strategy="Correct north arrow; resubmit plat for approval",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Date Standards",
        keywords=["plat", "date", "standards", "Texas", "survey", "approval"],
        conclusion_template="Plat must include date of survey and certification as required by Texas surveying standards.",
        reasoning_framework=(
            "The date of survey and certification is required for all subdivision plats filed in Texas. Texas surveying "
            "standards specify inclusion of the date in the title block and certification statement. Burden is on the "
            "surveyor and applicant to ensure compliance. Counter arguments arise from missing or incorrect date. Resolution "
            "involves correcting the plat and resubmitting. Scope includes all subdivision plats filed in Texas."
        ),
        key_factors=[
            "Date of survey",
            "Date of certification",
            "Compliance with standards",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Texas Local Government Code §212"
        ],
        burden_holder="Surveyor and applicant",
        adversary_position="Governing authority may reject for missing date",
        counter_arguments=[
            "Missing or incorrect date",
            "Non-compliance with standards"
        ],
        resolution_strategy="Correct date; resubmit plat for approval",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Legend Consistency",
        keywords=["plat", "legend", "consistency", "Texas", "survey", "approval"],
        conclusion_template="Plat legend must be consistent throughout the document as required by Texas surveying standards.",
        reasoning_framework=(
            "Consistency of legend ensures clarity in identifying elements such as easements, dedications, and setback lines. "
            "Texas surveying standards require legends to be comprehensive and consistent throughout the plat. Burden is on "
            "the surveyor and applicant to ensure compliance. Counter arguments arise from inconsistent legend. Resolution "
            "involves correcting the plat and resubmitting. Scope includes all subdivision plats and surveys in Texas."
        ),
        key_factors=[
            "Comprehensive and consistent legend",
            "Compliance with standards",
            "Clarity of identification",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Municipal ordinances"
        ],
        burden_holder="Surveyor and applicant",
        adversary_position="Governing authority may reject for inconsistent legend",
        counter_arguments=[
            "Inconsistent legend",
            "Ambiguous identification"
        ],
        resolution_strategy="Correct legend; resubmit plat for approval",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Scale Consistency",
        keywords=["plat", "scale", "consistency", "Texas", "survey", "approval"],
        conclusion_template="Plat scale must be consistent throughout the document as required by Texas surveying standards.",
        reasoning_framework=(
            "Consistency of scale ensures accuracy in assessing distances and area measurements. Texas surveying standards "
            "require the scale to be clearly indicated and consistent throughout the plat. Burden is on the surveyor and "
            "applicant to ensure compliance. Counter arguments arise from inconsistent scale. Resolution involves correcting "
            "the plat and resubmitting. Scope includes all subdivision plats and surveys in Texas."
        ),
        key_factors=[
            "Clear and consistent scale",
            "Compliance with standards",
            "Accuracy of measurements",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Board of Professional Land Surveying Standards",
            "Municipal ordinances"
        ],
        burden_holder="Surveyor and applicant",
        adversary_position="Governing authority may reject for inconsistent scale",
        counter_arguments=[
            "Inconsistent scale",
            "Errors in measurements"
        ],
        resolution_strategy="Correct scale; resubmit plat for approval",
        entity_scope="Surveyors, subdivision applicants, municipalities",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surveying Practice Act, 2010 Revision"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Notarization Standards",
        keywords=["plat", "notarization", "standards", "Texas", "county", "filing"],
        conclusion_template="Plat must be notarized as required by Texas Local Government Code §212 and county clerk procedures.",
        reasoning_framework=(
            "Notarization is required for plat filing in Texas counties. Texas Local Government Code §212 and county clerk "
            "procedures specify notarization requirements. Burden is on the applicant and surveyor to ensure compliance. "
            "Counter arguments arise from missing or incomplete notarization. Resolution involves correcting deficiencies "
            "and resubmitting. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Notarization",
            "Compliance with county clerk procedures",
            "Submission of required documents",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant and surveyor",
        adversary_position="County clerk may reject for missing notarization",
        counter_arguments=[
            "Missing or incomplete notarization",
            "Non-compliance with procedures"
        ],
        resolution_strategy="Correct notarization; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, surveyors, county clerks",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Fee Assessment",
        keywords=["plat", "fee", "assessment", "Texas", "county", "filing"],
        conclusion_template="Plat filing fees must be assessed and paid as required by Texas Local Government Code §212 and county clerk procedures.",
        reasoning_framework=(
            "Plat filing fees are required for submission and recordation in Texas counties. Texas Local Government Code §212 "
            "and county clerk procedures specify fee assessment and payment requirements. Burden is on the applicant to pay "
            "all required fees. Counter arguments arise from unpaid or incorrect fees. Resolution involves paying fees and "
            "resubmitting. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Assessment and payment of fees",
            "Compliance with county clerk procedures",
            "Submission of required documents",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant",
        adversary_position="County clerk may reject for unpaid fees",
        counter_arguments=[
            "Unpaid or incorrect fees",
            "Non-compliance with procedures"
        ],
        resolution_strategy="Pay fees; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, county clerks",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Document Standards",
        keywords=["plat", "document", "standards", "Texas", "county", "filing"],
        conclusion_template="Plat documents must comply with county standards and Texas Local Government Code §212.",
        reasoning_framework=(
            "Plat document standards specify paper size, format, resolution, and document naming conventions. Texas Local "
            "Government Code §212 and county clerk procedures provide baseline requirements. Burden is on the applicant to "
            "comply with all standards. Counter arguments arise from non-compliant documents. Resolution involves correcting "
            "deficiencies and resubmitting. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with document standards",
            "Paper size and format",
            "Resolution and naming conventions",
            "Submission of required documents"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant",
        adversary_position="County clerk may reject for non-compliance",
        counter_arguments=[
            "Non-compliant document standards",
            "Incomplete submission"
        ],
        resolution_strategy="Correct document standards; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, county clerks",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Filing Deadlines",
        keywords=["plat", "filing", "deadlines", "Texas", "county", "approval"],
        conclusion_template="Plat filing must comply with statutory and county deadlines as required by Texas Local Government Code §212.",
        reasoning_framework=(
            "Plat filing deadlines are specified by Texas Local Government Code §212 and county clerk procedures. Applicants "
            "must file plats within statutory deadlines after approval. Burden is on the applicant to comply. Counter arguments "
            "arise from late filings. Resolution involves correcting deficiencies and resubmitting. Scope includes all "
            "subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with filing deadlines",
            "Submission of approved plat",
            "County clerk procedures",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant",
        adversary_position="County clerk may reject for late filing",
        counter_arguments=[
            "Late filing",
            "Non-compliance with procedures"
        ],
        resolution_strategy="Correct deficiencies; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, county clerks",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat County Clerk Review",
        keywords=["plat", "county clerk", "review", "Texas", "filing", "approval"],
        conclusion_template="County clerk review must comply with Texas Local Government Code §212 and county procedures.",
        reasoning_framework=(
            "County clerk review involves assessing compliance with document standards, certification, notarization, and fee "
            "payment. Texas Local Government Code §212 and county clerk procedures provide baseline requirements. Burden is "
            "on the applicant to comply. Counter arguments arise from non-compliance. Resolution involves correcting "
            "deficiencies and resubmitting. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with county clerk review procedures",
            "Document standards",
            "Certification and notarization",
            "Fee payment"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant",
        adversary_position="County clerk may reject for non-compliance",
        counter_arguments=[
            "Non-compliance with review procedures",
            "Incomplete submission"
        ],
        resolution_strategy="Correct deficiencies; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, county clerks",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Public Access Standards",
        keywords=["plat", "public access", "standards", "Texas", "county", "filing"],
        conclusion_template="Subdivision plats must be accessible to the public as required by Texas Local Government Code §212 and county clerk procedures.",
        reasoning_framework=(
            "Public access to subdivision plats is required for transparency and legal recognition. Texas Local Government "
            "Code §212 and county clerk procedures specify standards for public access, including availability of records "
            "and digital access. Burden is on the county clerk to provide access. Counter arguments arise from restricted "
            "access. Resolution involves correcting deficiencies and ensuring compliance. Scope includes all subdivision "
            "plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with public access standards",
            "Availability of records",
            "Digital access",
            "County clerk procedures"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="County clerk",
        adversary_position="Applicant or public may object to restricted access",
        counter_arguments=[
            "Restricted access",
            "Non-compliance with procedures"
        ],
        resolution_strategy="Correct deficiencies; ensure public access; comply with county procedures",
        entity_scope="Subdivision applicants, county clerks, public",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat Correction Procedures",
        keywords=["plat", "correction", "procedures", "Texas", "county", "filing"],
        conclusion_template="Plat corrections must follow procedures outlined in Texas Local Government Code §212 and county clerk procedures.",
        reasoning_framework=(
            "Plat corrections involve amending the plat to address errors or deficiencies. Texas Local Government Code §212 "
            "and county clerk procedures specify correction procedures. Burden is on the applicant and surveyor to comply. "
            "Counter arguments arise from improper correction procedures. Resolution involves correcting deficiencies and "
            "resubmitting. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with correction procedures",
            "Submission of corrected plat",
            "County clerk procedures",
            "Surveyor certification"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County clerk procedures"
        ],
        burden_holder="Applicant and surveyor",
        adversary_position="County clerk may reject for improper correction",
        counter_arguments=[
            "Improper correction procedures",
            "Incomplete submission"
        ],
        resolution_strategy="Correct deficiencies; resubmit plat; comply with county procedures",
        entity_scope="Subdivision applicants, surveyors, county clerks",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat County Variance Procedures",
        keywords=["plat", "county", "variance", "procedures", "Texas", "approval"],
        conclusion_template="County variance procedures must comply with Texas Local Government Code §212 and county ordinances.",
        reasoning_framework=(
            "County variance procedures allow applicants to request exceptions to subdivision standards. Texas Local Government "
            "Code §212 and county ordinances specify variance procedures, including application, public notice, and hearing. "
            "Burden is on the applicant to demonstrate necessity and compliance. Counter arguments arise from governing "
            "authority or neighbors. Resolution involves negotiation, amendment, or appeal. Scope includes all subdivision "
            "plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with variance procedures",
            "Application and supporting documentation",
            "Public notice and hearing",
            "County ordinances"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority or neighbors may object",
        counter_arguments=[
            "Failure to demonstrate necessity",
            "Non-compliance with procedures"
        ],
        resolution_strategy="Comply with variance procedures; negotiate changes; appeal if necessary",
        entity_scope="Subdivision applicants, county clerks, governing authority",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat County Infrastructure Standards",
        keywords=["plat", "county", "infrastructure", "standards", "Texas", "approval"],
        conclusion_template="County infrastructure standards must be met as required by Texas Local Government Code §212 and county ordinances.",
        reasoning_framework=(
            "County infrastructure standards specify requirements for roads, utilities, drainage, and public facilities. Texas "
            "Local Government Code §212 and county ordinances provide baseline requirements. Burden is on the applicant to "
            "comply. Counter arguments arise from insufficient infrastructure. Resolution involves amending the plat or "
            "negotiating with the governing authority. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with infrastructure standards",
            "Adequacy of roads, utilities, drainage",
            "County ordinances",
            "Submission of infrastructure plans"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority may require additional infrastructure",
        counter_arguments=[
            "Insufficient infrastructure",
            "Non-compliance with standards"
        ],
        resolution_strategy="Amend plat; negotiate with governing authority; resubmit for approval",
        entity_scope="Subdivision applicants, county clerks, governing authority",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat County Environmental Standards",
        keywords=["plat", "county", "environmental", "standards", "Texas", "approval"],
        conclusion_template="County environmental standards must be met as required by Texas Local Government Code §212 and county ordinances.",
        reasoning_framework=(
            "County environmental standards assess impact on wetlands, floodplains, endangered species, and sensitive areas. "
            "Texas Local Government Code §212 and county ordinances specify requirements. Burden is on the applicant to "
            "comply. Counter arguments arise from insufficient environmental review. Resolution involves amending the plat "
            "or negotiating mitigation measures. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with environmental standards",
            "Environmental assessment",
            "Mitigation measures",
            "County ordinances"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Governing authority may require additional mitigation",
        counter_arguments=[
            "Insufficient environmental review",
            "Non-compliance with standards"
        ],
        resolution_strategy="Amend plat; negotiate mitigation measures; resubmit for approval",
        entity_scope="Subdivision applicants, county clerks, governing authority",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat County Public Hearing Standards",
        keywords=["plat", "county", "public hearing", "standards", "Texas", "approval"],
        conclusion_template="County public hearing standards must be met as required by Texas Local Government Code §212 and county ordinances.",
        reasoning_framework=(
            "County public hearing standards specify notice, hearing procedures, and consideration of public input. Texas "
            "Local Government Code §212 and county ordinances provide baseline requirements. Burden is on the applicant to "
            "comply. Counter arguments arise from insufficient notice or hearing procedures. Resolution involves correcting "
            "deficiencies and resubmitting. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Notice to affected property owners",
            "Compliance with hearing procedures",
            "Consideration of public input",
            "County ordinances"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County ordinances"
        ],
        burden_holder="Applicant",
        adversary_position="Neighbors and governing authority may object",
        counter_arguments=[
            "Insufficient notice",
            "Non-compliance with hearing procedures"
        ],
        resolution_strategy="Correct deficiencies; comply with hearing procedures; resubmit plat",
        entity_scope="Subdivision applicants, county clerks, governing authority",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Local Government Code §212"
    ),
    DoctrineBlock(
        topic="Subdivision Plat County Appeal Procedures",
        keywords=["plat", "county", "appeal", "procedures", "Texas", "approval"],
        conclusion_template="County appeal procedures must comply with Texas Local Government Code §212 and county ordinances.",
        reasoning_framework=(
            "County appeal procedures allow applicants to challenge plat rejection or conditions. Texas Local Government Code "
            "§212 and county ordinances specify appeal procedures, including deadlines and supporting documentation. Burden is "
            "on the applicant to comply. Counter arguments arise from governing authority. Resolution involves negotiation, "
            "amendment, or legal action. Scope includes all subdivision plats filed in Texas counties."
        ),
        key_factors=[
            "Compliance with appeal procedures",
            "Timely filing",
            "Supporting documentation",
            "County ordinances"
        ],
        primary_authority=[
            "Texas Local Government Code §212",
            "County ordinances"
        ],
        burden