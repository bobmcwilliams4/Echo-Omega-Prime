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
        topic="Lease Primary Term Expiration",
        keywords=["lease expiration", "primary term", "oil and gas lease", "termination", "automatic expiration"],
        conclusion_template="The lease expires at the end of the primary term unless extended by operations or production.",
        reasoning_framework="""
        The primary term of an oil and gas lease is a fixed period during which the lessee has the right to explore and produce hydrocarbons without obligation to maintain production. If no production or qualifying operations occur during this term, the lease terminates automatically. The lease may contain savings clauses, such as a shut-in royalty provision or continuous operations clause, which can extend the lease beyond the primary term. The burden is on the lessee to demonstrate compliance with any lease extension provisions. Texas courts strictly construe lease expiration, favoring automatic termination unless clear evidence of extension exists.
        """,
        key_factors=[
            "Duration of primary term",
            "Presence of production or operations",
            "Savings clauses (e.g., shut-in royalty)",
            "Notice requirements",
            "Lease language"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.101",
            "BP Amoco Prod. Co. v. Marshall, 288 S.W.3d 430 (Tex. App. 2009)",
            "Huth v. Hoffman, 61 S.W.2d 879 (Tex. Civ. App. 1933)"
        ],
        burden_holder="Lessee",
        adversary_position="Lessor may assert automatic expiration if no production or operations occurred.",
        counter_arguments=[
            "Lessee claims extension via savings clause",
            "Equitable estoppel due to lessor conduct"
        ],
        resolution_strategy="Strict construction of lease terms; review operations and production records; apply controlling precedent.",
        entity_scope="Oil and gas lease parties",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="BP Amoco Prod. Co. v. Marshall, 288 S.W.3d 430 (Tex. App. 2009)"
    ),
    DoctrineBlock(
        topic="Continuous Drilling Clause Deadline",
        keywords=["continuous drilling", "drilling obligation", "lease extension", "deadline", "operations"],
        conclusion_template="The lessee must commence drilling operations within the specified period to maintain the lease.",
        reasoning_framework="""
        Continuous drilling clauses require the lessee to begin drilling new wells within a set timeframe after completing or abandoning a well, typically to maintain lease acreage or avoid lease termination. Courts interpret these clauses according to their plain language, and strict compliance is generally required. Failure to commence operations within the deadline results in loss of leasehold rights or reduction of acreage. The lessee bears the burden to prove timely commencement of operations, which may include preparatory work, not just spudding in. The lessor may challenge the sufficiency of operations or timing.
        """,
        key_factors=[
            "Deadline for commencing operations",
            "Definition of 'operations' under lease",
            "Evidence of commencement",
            "Lease language specificity"
        ],
        primary_authority=[
            "Texaco, Inc. v. Wolfe, 601 S.W.2d 737 (Tex. Civ. App. 1980)",
            "Texas Natural Resources Code §91.101"
        ],
        burden_holder="Lessee",
        adversary_position="Lessor may assert lease termination or reduction of acreage.",
        counter_arguments=[
            "Lessee claims substantial compliance",
            "Lessee asserts ambiguity in clause"
        ],
        resolution_strategy="Review lease terms, drilling records, and apply strict construction; resolve ambiguities in favor of lessor.",
        entity_scope="Oil and gas lease parties",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texaco, Inc. v. Wolfe, 601 S.W.2d 737 (Tex. Civ. App. 1980)"
    ),
    DoctrineBlock(
        topic="Shut-In Royalty Payment Deadline",
        keywords=["shut-in royalty", "payment deadline", "lease extension", "non-producing well", "timely payment"],
        conclusion_template="The lessee must pay shut-in royalties within the time specified to maintain the lease during periods of non-production.",
        reasoning_framework="""
        Shut-in royalty clauses allow the lessee to maintain the lease when a well capable of production is not producing, typically due to lack of market or other temporary circumstances. The lessee must pay the shut-in royalty within the deadline specified in the lease, often annually. Courts require strict compliance with payment deadlines, and failure to pay timely results in lease termination. The lessee bears the burden to prove timely payment and compliance with all lease requirements. The lessor may challenge payment sufficiency or timeliness.
        """,
        key_factors=[
            "Deadline for payment",
            "Well capable of production",
            "Lease language",
            "Proof of payment"
        ],
        primary_authority=[
            "Freeman v. Magnolia Petroleum Co., 171 S.W.2d 339 (Tex. 1943)",
            "Texas Natural Resources Code §91.101"
        ],
        burden_holder="Lessee",
        adversary_position="Lessor may assert lease termination for untimely payment.",
        counter_arguments=[
            "Lessee claims substantial compliance",
            "Lessee asserts payment was timely"
        ],
        resolution_strategy="Strict construction of lease terms; review payment records; resolve ambiguities in favor of lessor.",
        entity_scope="Oil and gas lease parties",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Freeman v. Magnolia Petroleum Co., 171 S.W.2d 339 (Tex. 1943)"
    ),
    DoctrineBlock(
        topic="Pooling Election Deadlines",
        keywords=["pooling", "election deadline", "unitization", "lease pooling", "timely election"],
        conclusion_template="The lessee must exercise pooling rights within the deadline specified in the lease or applicable regulations.",
        reasoning_framework="""
        Pooling clauses permit the lessee to combine leased acreage with other lands to form a production unit. The lease may require the lessee to exercise pooling rights within a certain timeframe, often before the expiration of the primary term or commencement of drilling. Courts enforce pooling deadlines strictly, and failure to timely elect pooling may result in loss of pooling rights or lease termination. The lessee bears the burden to prove timely election and compliance with all procedural requirements. The lessor may challenge the validity or timeliness of pooling.
        """,
        key_factors=[
            "Pooling election deadline",
            "Lease language",
            "Notice requirements",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Natural Resources Code §102.001",
            "Jones v. Killingsworth, 353 S.W.2d 514 (Tex. 1962)"
        ],
        burden_holder="Lessee",
        adversary_position="Lessor may assert loss of pooling rights or lease termination.",
        counter_arguments=[
            "Lessee claims substantial compliance",
            "Lessee asserts ambiguity in pooling clause"
        ],
        resolution_strategy="Review lease terms, pooling records, and regulatory filings; resolve ambiguities in favor of lessor.",
        entity_scope="Oil and gas lease parties",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Jones v. Killingsworth, 353 S.W.2d 514 (Tex. 1962)"
    ),
    DoctrineBlock(
        topic="Lease Option Exercise Dates",
        keywords=["lease option", "exercise date", "renewal", "extension", "timely exercise"],
        conclusion_template="The lessee must exercise lease options within the specified date to renew or extend the lease.",
        reasoning_framework="""
        Lease options allow the lessee to renew or extend the lease for an additional term. The option must be exercised within the date specified in the lease, usually by written notice and payment of consideration. Courts require strict compliance with option exercise deadlines, and failure to timely exercise results in loss of renewal or extension rights. The lessee bears the burden to prove timely exercise and compliance with all procedural requirements. The lessor may challenge the sufficiency or timeliness of exercise.
        """,
        key_factors=[
            "Option exercise date",
            "Notice requirements",
            "Payment of consideration",
            "Lease language"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.101",
            "W.T. Waggoner Estate v. Sigler Oil Co., 19 S.W.2d 27 (Tex. 1929)"
        ],
        burden_holder="Lessee",
        adversary_position="Lessor may assert loss of renewal or extension rights.",
        counter_arguments=[
            "Lessee claims substantial compliance",
            "Lessee asserts ambiguity in option clause"
        ],
        resolution_strategy="Strict construction of lease terms; review notice and payment records; resolve ambiguities in favor of lessor.",
        entity_scope="Oil and gas lease parties",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="W.T. Waggoner Estate v. Sigler Oil Co., 19 S.W.2d 27 (Tex. 1929)"
    ),
    DoctrineBlock(
        topic="W-1 Permit Expiration",
        keywords=["W-1 permit", "drilling permit", "expiration", "Texas Railroad Commission", "permit deadline"],
        conclusion_template="The W-1 drilling permit expires if operations are not commenced within the period specified by the Railroad Commission.",
        reasoning_framework="""
        The Texas Railroad Commission issues W-1 permits for drilling oil and gas wells. Permits typically expire one year from issuance unless drilling operations commence. If operations are not begun within the permit period, the permit lapses and must be renewed. Compliance with permit deadlines is required for lawful drilling. Operators bear the burden to monitor permit expiration and renew as necessary. Failure to comply may result in enforcement actions and loss of drilling rights.
        """,
        key_factors=[
            "Permit issuance date",
            "Commencement of operations",
            "Permit expiration period",
            "Renewal procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.5",
            "Texas Railroad Commission Rule 3.5"
        ],
        burden_holder="Operator",
        adversary_position="RRC may deny drilling or impose penalties for expired permit.",
        counter_arguments=[
            "Operator claims substantial compliance",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review permit records, commencement dates, and apply RRC rules; renew permit if necessary.",
        entity_scope="Operators, RRC",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.5"
    ),
    DoctrineBlock(
        topic="RRC Compliance Deadlines",
        keywords=["Railroad Commission", "compliance deadline", "regulatory deadline", "reporting", "enforcement"],
        conclusion_template="Operators must comply with Railroad Commission deadlines for reporting, permitting, and operations.",
        reasoning_framework="""
        The Texas Railroad Commission sets deadlines for various regulatory requirements, including reporting, permitting, and operational compliance. Operators must adhere to these deadlines to avoid enforcement actions, fines, or permit revocation. Compliance is monitored through filings, inspections, and audits. The burden is on the operator to ensure timely compliance. The RRC may grant extensions for good cause but generally enforces deadlines strictly.
        """,
        key_factors=[
            "Regulatory deadline",
            "Type of compliance required",
            "Extension procedures",
            "Operator records"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.1-3.100",
            "Texas Railroad Commission Rules"
        ],
        burden_holder="Operator",
        adversary_position="RRC may impose penalties or revoke permits for non-compliance.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review regulatory filings, compliance records, and apply RRC rules; seek extension if needed.",
        entity_scope="Operators, RRC",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16"
    ),
    DoctrineBlock(
        topic="Well Plugging Deadlines (Rule 14)",
        keywords=["well plugging", "Rule 14", "plugging deadline", "abandoned well", "RRC compliance"],
        conclusion_template="Operators must plug abandoned wells within the deadline specified by Rule 14 of the Texas Railroad Commission.",
        reasoning_framework="""
        Rule 14 of the Texas Railroad Commission requires operators to plug abandoned wells within a specified timeframe, typically one year after abandonment. Failure to comply may result in enforcement actions, fines, and liability for environmental damages. The operator bears the burden to demonstrate timely plugging and compliance with all procedural requirements. The RRC may extend deadlines for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Date of well abandonment",
            "Plugging deadline under Rule 14",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.14",
            "Texas Railroad Commission Rule 14"
        ],
        burden_holder="Operator",
        adversary_position="RRC may impose penalties or require plugging at operator expense.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review abandonment and plugging records; apply Rule 14; seek extension if necessary.",
        entity_scope="Operators, RRC",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.14"
    ),
    DoctrineBlock(
        topic="P-4 Operator Transfer Deadlines",
        keywords=["P-4 form", "operator transfer", "deadline", "Railroad Commission", "transfer compliance"],
        conclusion_template="Operators must file P-4 forms to transfer well operatorship within the deadline specified by the Railroad Commission.",
        reasoning_framework="""
        The Texas Railroad Commission requires operators to file P-4 forms to transfer well operatorship. The deadline for filing is typically set by RRC rules and must be strictly complied with. Failure to timely file may result in delays, enforcement actions, or loss of operatorship. The burden is on both the outgoing and incoming operator to ensure timely filing and compliance with all procedural requirements.
        """,
        key_factors=[
            "Transfer deadline",
            "Filing of P-4 form",
            "Operator records",
            "RRC procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.58",
            "Texas Railroad Commission Rule 58"
        ],
        burden_holder="Outgoing and incoming operator",
        adversary_position="RRC may deny transfer or impose penalties for late filing.",
        counter_arguments=[
            "Operator claims administrative error",
            "Operator asserts extension granted"
        ],
        resolution_strategy="Review transfer records, apply RRC rules, and ensure timely filing.",
        entity_scope="Operators, RRC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.58"
    ),
    DoctrineBlock(
        topic="Production Report Due Dates",
        keywords=["production report", "due date", "Railroad Commission", "reporting deadline", "compliance"],
        conclusion_template="Operators must file production reports with the Railroad Commission by the due dates specified in regulations.",
        reasoning_framework="""
        The Texas Railroad Commission requires operators to file monthly production reports by the due date specified in regulations. Failure to comply may result in enforcement actions, fines, or permit suspension. The operator bears the burden to demonstrate timely filing and compliance with all reporting requirements. The RRC may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Report due date",
            "Operator records",
            "Extension procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.27",
            "Texas Railroad Commission Rule 27"
        ],
        burden_holder="Operator",
        adversary_position="RRC may impose penalties or suspend permits for late filing.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review reporting records, apply RRC rules, and seek extension if necessary.",
        entity_scope="Operators, RRC",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.27"
    ),
    DoctrineBlock(
        topic="Tax Payment Deadlines (Mineral Severance)",
        keywords=["tax payment", "mineral severance", "deadline", "Texas Comptroller", "tax compliance"],
        conclusion_template="Mineral severance taxes must be paid by the deadlines specified by the Texas Comptroller.",
        reasoning_framework="""
        The Texas Comptroller requires payment of mineral severance taxes by specified deadlines, typically monthly or quarterly. Failure to pay timely may result in penalties, interest, and enforcement actions. The operator or taxpayer bears the burden to demonstrate timely payment and compliance with all tax requirements. Extensions may be granted for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Tax payment deadline",
            "Taxpayer records",
            "Extension procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Tax Code §201.101",
            "Texas Comptroller Rules"
        ],
        burden_holder="Operator or taxpayer",
        adversary_position="Comptroller may impose penalties or take enforcement action for late payment.",
        counter_arguments=[
            "Taxpayer claims extension granted",
            "Taxpayer asserts administrative error"
        ],
        resolution_strategy="Review payment records, apply Comptroller rules, and seek extension if necessary.",
        entity_scope="Operators, taxpayers, Comptroller",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Tax Code §201.101"
    ),
    DoctrineBlock(
        topic="Statute of Limitations for Title Claims",
        keywords=["statute of limitations", "title claim", "deadline", "quiet title", "adverse possession"],
        conclusion_template="Title claims must be brought within the statute of limitations period specified by Texas law.",
        reasoning_framework="""
        Texas law imposes statutes of limitations on title claims, including quiet title actions and adverse possession. The period varies depending on the nature of the claim, typically ranging from 3 to 10 years. Failure to bring a claim within the limitations period bars recovery. The claimant bears the burden to demonstrate timely filing. The defendant may assert the limitations defense, and courts strictly enforce deadlines.
        """,
        key_factors=[
            "Type of title claim",
            "Limitations period",
            "Date of accrual",
            "Claimant records"
        ],
        primary_authority=[
            "Texas Civil Practice & Remedies Code §16.024-16.027",
            "Glover v. Union Pac. R.R. Co., 187 S.W.3d 201 (Tex. App. 2006)"
        ],
        burden_holder="Claimant",
        adversary_position="Defendant may assert limitations defense.",
        counter_arguments=[
            "Claimant asserts discovery rule",
            "Claimant claims equitable tolling"
        ],
        resolution_strategy="Review claim records, apply limitations statutes, and resolve ambiguities in favor of defendant.",
        entity_scope="Claimants, defendants, courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Glover v. Union Pac. R.R. Co., 187 S.W.3d 201 (Tex. App. 2006)"
    ),
    DoctrineBlock(
        topic="Recording Deadline Requirements",
        keywords=["recording", "deadline", "county clerk", "title", "notice"],
        conclusion_template="Documents affecting title must be recorded within the deadline specified by Texas law to provide constructive notice.",
        reasoning_framework="""
        Texas law requires certain documents affecting title, such as deeds and leases, to be recorded with the county clerk to provide constructive notice. While there is no strict statutory deadline, timely recording is essential to protect against subsequent purchasers. Failure to record promptly may result in loss of priority or rights. The party seeking to protect title bears the burden to record timely. Courts may consider equitable factors in resolving disputes.
        """,
        key_factors=[
            "Type of document",
            "Date of execution",
            "Recording date",
            "Notice requirements"
        ],
        primary_authority=[
            "Texas Property Code §13.001",
            "Texaco, Inc. v. Wolfe, 601 S.W.2d 737 (Tex. Civ. App. 1980)"
        ],
        burden_holder="Party seeking to protect title",
        adversary_position="Subsequent purchaser may assert superior rights.",
        counter_arguments=[
            "Party claims equitable notice",
            "Party asserts recording delay was excusable"
        ],
        resolution_strategy="Review recording records, apply Property Code, and resolve ambiguities in favor of subsequent purchaser.",
        entity_scope="Title holders, county clerks, courts",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Property Code §13.001"
    ),
    DoctrineBlock(
        topic="Probate Filing Deadlines",
        keywords=["probate", "filing deadline", "estate", "court", "timely filing"],
        conclusion_template="Probate applications must be filed within the deadline specified by Texas law to administer the estate.",
        reasoning_framework="""
        Texas law requires probate applications to be filed within four years of the decedent's death, unless exceptions apply. Failure to file timely may bar administration or result in loss of rights. The applicant bears the burden to demonstrate timely filing or applicability of exceptions. Courts strictly enforce deadlines but may allow late filing for good cause.
        """,
        key_factors=[
            "Date of death",
            "Filing deadline",
            "Applicant records",
            "Exception procedures"
        ],
        primary_authority=[
            "Texas Estates Code §256.003",
            "Estate of Gainer, 201 S.W.3d 423 (Tex. App. 2006)"
        ],
        burden_holder="Applicant",
        adversary_position="Interested parties may assert bar to administration.",
        counter_arguments=[
            "Applicant claims exception applies",
            "Applicant asserts equitable tolling"
        ],
        resolution_strategy="Review death and filing records, apply Estates Code, and resolve ambiguities in favor of interested parties.",
        entity_scope="Applicants, courts, estates",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Estates Code §256.003"
    ),
    DoctrineBlock(
        topic="Heirship Affidavit Timing",
        keywords=["heirship affidavit", "timing", "estate", "title", "notice"],
        conclusion_template="Heirship affidavits should be filed promptly to establish title and provide notice to third parties.",
        reasoning_framework="""
        Heirship affidavits are used to establish title in the absence of probate. Texas law does not specify a strict deadline, but prompt filing is recommended to provide constructive notice and avoid disputes. Delay in filing may result in loss of priority or rights. The party seeking to establish title bears the burden to file timely. Courts may consider equitable factors in resolving disputes.
        """,
        key_factors=[
            "Date of death",
            "Filing date",
            "Notice requirements",
            "Title records"
        ],
        primary_authority=[
            "Texas Estates Code §201.001",
            "Texas Property Code §13.001"
        ],
        burden_holder="Party seeking to establish title",
        adversary_position="Subsequent purchaser may assert superior rights.",
        counter_arguments=[
            "Party claims equitable notice",
            "Party asserts delay was excusable"
        ],
        resolution_strategy="Review filing records, apply Estates and Property Codes, and resolve ambiguities in favor of subsequent purchaser.",
        entity_scope="Heirs, title holders, courts",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Estates Code §201.001"
    ),
    DoctrineBlock(
        topic="Surface Damage Notice Deadlines",
        keywords=["surface damage", "notice deadline", "landowner", "operator", "Texas law"],
        conclusion_template="Operators must provide notice of surface damage within the deadline specified by Texas law or lease terms.",
        reasoning_framework="""
        Texas law and lease terms may require operators to provide notice to landowners before commencing operations that may cause surface damage. The deadline for notice is typically specified in the lease or statute. Failure to provide timely notice may result in liability for damages or injunction. The operator bears the burden to demonstrate compliance with notice requirements. Landowners may challenge sufficiency or timeliness of notice.
        """,
        key_factors=[
            "Notice deadline",
            "Lease or statutory requirements",
            "Operator records",
            "Landowner rights"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.101",
            "Texas Surface Damage Act"
        ],
        burden_holder="Operator",
        adversary_position="Landowner may assert damages or seek injunction.",
        counter_arguments=[
            "Operator claims substantial compliance",
            "Operator asserts notice was timely"
        ],
        resolution_strategy="Review lease terms, notice records, and apply statutory requirements.",
        entity_scope="Operators, landowners",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Surface Damage Act"
    ),
    DoctrineBlock(
        topic="Drill Site Restoration Deadlines",
        keywords=["drill site restoration", "deadline", "operator", "landowner", "environmental compliance"],
        conclusion_template="Operators must restore drill sites within the deadline specified by lease terms or Texas law.",
        reasoning_framework="""
        Lease terms and Texas law may require operators to restore drill sites to their original condition within a specified deadline after completion of operations. Failure to comply may result in liability for damages or enforcement actions. The operator bears the burden to demonstrate timely restoration and compliance with all requirements. Landowners may challenge sufficiency or timeliness of restoration.
        """,
        key_factors=[
            "Restoration deadline",
            "Lease or statutory requirements",
            "Operator records",
            "Landowner rights"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.101",
            "Texas Administrative Code Title 16, §3.8"
        ],
        burden_holder="Operator",
        adversary_position="Landowner may assert damages or seek enforcement.",
        counter_arguments=[
            "Operator claims substantial compliance",
            "Operator asserts restoration was timely"
        ],
        resolution_strategy="Review lease terms, restoration records, and apply statutory requirements.",
        entity_scope="Operators, landowners",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.8"
    ),
    DoctrineBlock(
        topic="Environmental Permit Renewal Deadlines",
        keywords=["environmental permit", "renewal deadline", "Texas Commission on Environmental Quality", "operator", "compliance"],
        conclusion_template="Operators must renew environmental permits by the deadlines specified by TCEQ regulations.",
        reasoning_framework="""
        The Texas Commission on Environmental Quality (TCEQ) requires operators to renew environmental permits, such as air and water permits, by specified deadlines. Failure to renew timely may result in permit revocation, fines, or enforcement actions. The operator bears the burden to demonstrate timely renewal and compliance with all requirements. TCEQ may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Permit renewal deadline",
            "Operator records",
            "Extension procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Administrative Code Title 30, §305.65",
            "TCEQ Rules"
        ],
        burden_holder="Operator",
        adversary_position="TCEQ may revoke permit or impose penalties for late renewal.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review permit records, apply TCEQ rules, and seek extension if necessary.",
        entity_scope="Operators, TCEQ",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 30, §305.65"
    ),
    DoctrineBlock(
        topic="Water Well Permit Renewal Deadlines",
        keywords=["water well permit", "renewal deadline", "Texas Water Development Board", "operator", "compliance"],
        conclusion_template="Operators must renew water well permits by the deadlines specified by TWDB regulations.",
        reasoning_framework="""
        The Texas Water Development Board (TWDB) requires operators to renew water well permits by specified deadlines. Failure to renew timely may result in permit revocation, fines, or enforcement actions. The operator bears the burden to demonstrate timely renewal and compliance with all requirements. TWDB may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Permit renewal deadline",
            "Operator records",
            "Extension procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Water Code §27.051",
            "TWDB Rules"
        ],
        burden_holder="Operator",
        adversary_position="TWDB may revoke permit or impose penalties for late renewal.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review permit records, apply TWDB rules, and seek extension if necessary.",
        entity_scope="Operators, TWDB",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Water Code §27.051"
    ),
    DoctrineBlock(
        topic="GCD Reporting Deadlines",
        keywords=["GCD", "Groundwater Conservation District", "reporting deadline", "operator", "compliance"],
        conclusion_template="Operators must file reports with Groundwater Conservation Districts by the deadlines specified in regulations.",
        reasoning_framework="""
        Groundwater Conservation Districts (GCDs) require operators to file reports, such as water use and well status, by specified deadlines. Failure to comply may result in enforcement actions, fines, or permit suspension. The operator bears the burden to demonstrate timely filing and compliance with all reporting requirements. GCDs may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Reporting deadline",
            "Operator records",
            "Extension procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Water Code §36.113",
            "GCD Rules"
        ],
        burden_holder="Operator",
        adversary_position="GCD may impose penalties or suspend permits for late filing.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review reporting records, apply GCD rules, and seek extension if necessary.",
        entity_scope="Operators, GCDs",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Water Code §36.113"
    ),
    DoctrineBlock(
        topic="Royalty Payment Deadline",
        keywords=["royalty payment", "deadline", "lease", "timely payment", "lessor rights"],
        conclusion_template="Lessee must pay royalties within the deadline specified in the lease or Texas law.",
        reasoning_framework="""
        Royalty payments are typically due monthly or quarterly as specified in the lease. Failure to pay timely may result in breach of contract and potential lease termination. The lessee bears the burden to demonstrate timely payment and compliance with all requirements. The lessor may challenge payment sufficiency or timeliness.
        """,
        key_factors=[
            "Payment deadline",
            "Lease language",
            "Payment records",
            "Lessor rights"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.401",
            "Texas Administrative Code Title 16, §3.91"
        ],
        burden_holder="Lessee",
        adversary_position="Lessor may assert breach or seek lease termination.",
        counter_arguments=[
            "Lessee claims substantial compliance",
            "Lessee asserts payment was timely"
        ],
        resolution_strategy="Review lease terms, payment records, and apply statutory requirements.",
        entity_scope="Lessee, lessor",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Natural Resources Code §91.401"
    ),
    DoctrineBlock(
        topic="Division Order Execution Deadline",
        keywords=["division order", "execution deadline", "royalty payment", "operator", "timely execution"],
        conclusion_template="Division orders must be executed within the deadline specified by Texas law or operator policy.",
        reasoning_framework="""
        Division orders allocate royalty payments among interest owners. Texas law requires operators to issue division orders and owners to execute them promptly. Failure to execute timely may delay royalty payments. The operator bears the burden to demonstrate timely issuance, and owners bear the burden to execute promptly. Courts may enforce deadlines strictly or allow reasonable extensions.
        """,
        key_factors=[
            "Execution deadline",
            "Operator records",
            "Owner records",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.402",
            "Texas Administrative Code Title 16, §3.91"
        ],
        burden_holder="Operator and owners",
        adversary_position="Operator may delay payments for late execution.",
        counter_arguments=[
            "Owner claims administrative error",
            "Owner asserts extension granted"
        ],
        resolution_strategy="Review division order records, apply statutory requirements, and resolve ambiguities in favor of timely payment.",
        entity_scope="Operators, owners",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Natural Resources Code §91.402"
    ),
    DoctrineBlock(
        topic="Notice of Assignment Filing Deadline",
        keywords=["assignment", "notice", "filing deadline", "lease", "operator"],
        conclusion_template="Assignments of lease interests must be filed and notice given within the deadline specified by Texas law or lease terms.",
        reasoning_framework="""
        Assignments of lease interests must be filed with the county clerk and notice given to the lessor or operator within the deadline specified in the lease or Texas law. Failure to file and give notice timely may result in loss of rights or breach of contract. The assignor and assignee bear the burden to demonstrate timely filing and notice. Courts may enforce deadlines strictly.
        """,
        key_factors=[
            "Filing deadline",
            "Notice requirements",
            "Lease language",
            "County clerk records"
        ],
        primary_authority=[
            "Texas Property Code §13.001",
            "Texas Natural Resources Code §91.101"
        ],
        burden_holder="Assignor and assignee",
        adversary_position="Lessor or operator may assert breach or loss of rights.",
        counter_arguments=[
            "Assignor claims substantial compliance",
            "Assignor asserts notice was timely"
        ],
        resolution_strategy="Review lease terms, filing and notice records, and apply statutory requirements.",
        entity_scope="Assignor, assignee, lessor, operator",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Property Code §13.001"
    ),
    DoctrineBlock(
        topic="Operating Agreement Election Deadline",
        keywords=["operating agreement", "election deadline", "joint operations", "operator", "timely election"],
        conclusion_template="Parties must exercise election rights under operating agreements within the deadline specified.",
        reasoning_framework="""
        Operating agreements may grant parties election rights, such as participation in operations or acceptance of proposals. The deadline for election is specified in the agreement. Failure to exercise timely may result in loss of participation rights. The party seeking to participate bears the burden to demonstrate timely election. The operator may challenge sufficiency or timeliness.
        """,
        key_factors=[
            "Election deadline",
            "Agreement language",
            "Notice requirements",
            "Party records"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.101",
            "Model Form Joint Operating Agreement"
        ],
        burden_holder="Party seeking to participate",
        adversary_position="Operator may deny participation for late election.",
        counter_arguments=[
            "Party claims substantial compliance",
            "Party asserts ambiguity in agreement"
        ],
        resolution_strategy="Review agreement terms, election records, and resolve ambiguities in favor of operator.",
        entity_scope="Agreement parties, operator",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Model Form Joint Operating Agreement"
    ),
    DoctrineBlock(
        topic="Force Majeure Notice Deadline",
        keywords=["force majeure", "notice deadline", "lease", "operator", "timely notice"],
        conclusion_template="Operators must provide force majeure notice within the deadline specified in the lease.",
        reasoning_framework="""
        Force majeure clauses excuse performance for certain events but typically require timely notice to the lessor. The deadline for notice is specified in the lease. Failure to provide timely notice may result in loss of force majeure protection. The operator bears the burden to demonstrate timely notice and compliance with all requirements. The lessor may challenge sufficiency or timeliness.
        """,
        key_factors=[
            "Notice deadline",
            "Lease language",
            "Operator records",
            "Force majeure event"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.101",
            "Texas Supreme Court precedent"
        ],
        burden_holder="Operator",
        adversary_position="Lessor may deny force majeure protection for late notice.",
        counter_arguments=[
            "Operator claims substantial compliance",
            "Operator asserts ambiguity in clause"
        ],
        resolution_strategy="Review lease terms, notice records, and resolve ambiguities in favor of lessor.",
        entity_scope="Operators, lessors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Supreme Court precedent"
    ),
    DoctrineBlock(
        topic="Unitization Election Deadline",
        keywords=["unitization", "election deadline", "lease", "operator", "timely election"],
        conclusion_template="Operators must exercise unitization rights within the deadline specified in the lease or statute.",
        reasoning_framework="""
        Unitization clauses allow operators to combine leases for efficient development. The deadline for election is specified in the lease or statute. Failure to exercise timely may result in loss of unitization rights. The operator bears the burden to demonstrate timely election and compliance with all requirements. The lessor may challenge sufficiency or timeliness.
        """,
        key_factors=[
            "Election deadline",
            "Lease or statutory requirements",
            "Operator records",
            "Notice requirements"
        ],
        primary_authority=[
            "Texas Natural Resources Code §101.001",
            "Texas Administrative Code Title 16, §3.40"
        ],
        burden_holder="Operator",
        adversary_position="Lessor may deny unitization for late election.",
        counter_arguments=[
            "Operator claims substantial compliance",
            "Operator asserts ambiguity in clause"
        ],
        resolution_strategy="Review lease terms, election records, and resolve ambiguities in favor of lessor.",
        entity_scope="Operators, lessors",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.40"
    ),
    DoctrineBlock(
        topic="Operating Expense Payment Deadline",
        keywords=["operating expense", "payment deadline", "joint operations", "operator", "timely payment"],
        conclusion_template="Parties must pay operating expenses within the deadline specified in the operating agreement.",
        reasoning_framework="""
        Operating agreements require parties to pay their share of operating expenses within a specified deadline. Failure to pay timely may result in loss of participation rights or penalties. The party responsible bears the burden to demonstrate timely payment. The operator may challenge sufficiency or timeliness.
        """,
        key_factors=[
            "Payment deadline",
            "Agreement language",
            "Payment records",
            "Operator rights"
        ],
        primary_authority=[
            "Model Form Joint Operating Agreement",
            "Texas Natural Resources Code §91.101"
        ],
        burden_holder="Party responsible for payment",
        adversary_position="Operator may impose penalties or deny participation.",
        counter_arguments=[
            "Party claims substantial compliance",
            "Party asserts payment was timely"
        ],
        resolution_strategy="Review agreement terms, payment records, and resolve ambiguities in favor of operator.",
        entity_scope="Agreement parties, operator",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Model Form Joint Operating Agreement"
    ),
    DoctrineBlock(
        topic="Lien Foreclosure Deadline",
        keywords=["lien", "foreclosure", "deadline", "operator", "contractor"],
        conclusion_template="Lien foreclosure actions must be brought within the deadline specified by Texas law.",
        reasoning_framework="""
        Texas law imposes deadlines for foreclosure of liens, including mineral and mechanics liens. The period varies depending on the type of lien, typically ranging from 2 to 4 years. Failure to bring foreclosure action timely bars recovery. The lienholder bears the burden to demonstrate timely filing. The defendant may assert the limitations defense.
        """,
        key_factors=[
            "Type of lien",
            "Foreclosure deadline",
            "Lienholder records",
            "Limitations period"
        ],
        primary_authority=[
            "Texas Property Code §53.158",
            "Texas Civil Practice & Remedies Code §16.004"
        ],
        burden_holder="Lienholder",
        adversary_position="Defendant may assert limitations defense.",
        counter_arguments=[
            "Lienholder asserts discovery rule",
            "Lienholder claims equitable tolling"
        ],
        resolution_strategy="Review lien records, apply limitations statutes, and resolve ambiguities in favor of defendant.",
        entity_scope="Lienholders, defendants, courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Property Code §53.158"
    ),
    DoctrineBlock(
        topic="Permit Appeal Filing Deadline",
        keywords=["permit appeal", "filing deadline", "operator", "regulatory agency", "timely appeal"],
        conclusion_template="Permit appeals must be filed within the deadline specified by Texas law or agency rules.",
        reasoning_framework="""
        Texas law and agency rules specify deadlines for filing appeals of permit decisions, typically ranging from 10 to 30 days after the decision. Failure to file timely may bar appeal. The appellant bears the burden to demonstrate timely filing. The agency may challenge sufficiency or timeliness.
        """,
        key_factors=[
            "Appeal deadline",
            "Agency rules",
            "Appellant records",
            "Notice requirements"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §1.11",
            "Texas Water Code §27.051"
        ],
        burden_holder="Appellant",
        adversary_position="Agency may deny appeal for late filing.",
        counter_arguments=[
            "Appellant claims extension granted",
            "Appellant asserts administrative error"
        ],
        resolution_strategy="Review appeal records, apply agency rules, and seek extension if necessary.",
        entity_scope="Appellants, agencies",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §1.11"
    ),
    DoctrineBlock(
        topic="Environmental Remediation Deadline",
        keywords=["environmental remediation", "deadline", "operator", "regulatory agency", "compliance"],
        conclusion_template="Operators must complete environmental remediation by the deadline specified in agency orders or regulations.",
        reasoning_framework="""
        Regulatory agencies may issue orders requiring operators to complete environmental remediation by a specified deadline. Failure to comply may result in fines, permit revocation, or enforcement actions. The operator bears the burden to demonstrate timely remediation and compliance with all requirements. Agencies may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Remediation deadline",
            "Agency orders",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 30, §334.81",
            "TCEQ Rules"
        ],
        burden_holder="Operator",
        adversary_position="Agency may impose penalties or revoke permits for late remediation.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review remediation records, apply agency rules, and seek extension if necessary.",
        entity_scope="Operators, agencies",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 30, §334.81"
    ),
    DoctrineBlock(
        topic="Well Completion Reporting Deadline",
        keywords=["well completion", "reporting deadline", "operator", "Railroad Commission", "compliance"],
        conclusion_template="Operators must file well completion reports by the deadline specified by the Railroad Commission.",
        reasoning_framework="""
        The Texas Railroad Commission requires operators to file well completion reports within a specified deadline, typically 30 days after completion. Failure to comply may result in enforcement actions, fines, or permit suspension. The operator bears the burden to demonstrate timely filing and compliance with all requirements. RRC may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Reporting deadline",
            "Operator records",
            "Extension procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.16",
            "Texas Railroad Commission Rule 16"
        ],
        burden_holder="Operator",
        adversary_position="RRC may impose penalties or suspend permits for late filing.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review reporting records, apply RRC rules, and seek extension if necessary.",
        entity_scope="Operators, RRC",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.16"
    ),
    DoctrineBlock(
        topic="Well Testing Deadline",
        keywords=["well testing", "deadline", "operator", "Railroad Commission", "compliance"],
        conclusion_template="Operators must conduct well testing and file results by the deadline specified by the Railroad Commission.",
        reasoning_framework="""
        The Texas Railroad Commission requires operators to conduct well testing and file results within a specified deadline, typically annually or after completion. Failure to comply may result in enforcement actions, fines, or permit suspension. The operator bears the burden to demonstrate timely testing and filing. RRC may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Testing deadline",
            "Operator records",
            "Extension procedures",
            "Regulatory compliance"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.28",
            "Texas Railroad Commission Rule 28"
        ],
        burden_holder="Operator",
        adversary_position="RRC may impose penalties or suspend permits for late testing.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review testing records, apply RRC rules, and seek extension if necessary.",
        entity_scope="Operators, RRC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.28"
    ),
    DoctrineBlock(
        topic="Annual Lease Rental Payment Deadline",
        keywords=["annual lease rental", "payment deadline", "lease", "operator", "timely payment"],
        conclusion_template="Lessee must pay annual lease rentals by the deadline specified in the lease.",
        reasoning_framework="""
        Annual lease rental payments are due by the deadline specified in the lease. Failure to pay timely may result in lease termination. The lessee bears the burden to demonstrate timely payment and compliance with all requirements. The lessor may challenge payment sufficiency or timeliness.
        """,
        key_factors=[
            "Payment deadline",
            "Lease language",
            "Payment records",
            "Lessor rights"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.101",
            "Texas Administrative Code Title 16, §3.91"
        ],
        burden_holder="Lessee",
        adversary_position="Lessor may assert lease termination for late payment.",
        counter_arguments=[
            "Lessee claims substantial compliance",
            "Lessee asserts payment was timely"
        ],
        resolution_strategy="Review lease terms, payment records, and apply statutory requirements.",
        entity_scope="Lessee, lessor",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Natural Resources Code §91.101"
    ),
    DoctrineBlock(
        topic="Permit Renewal Application Deadline",
        keywords=["permit renewal", "application deadline", "operator", "regulatory agency", "timely application"],
        conclusion_template="Operators must file permit renewal applications by the deadline specified by agency rules.",
        reasoning_framework="""
        Regulatory agencies specify deadlines for filing permit renewal applications, typically before permit expiration. Failure to file timely may result in permit revocation or enforcement actions. The operator bears the burden to demonstrate timely filing and compliance with all requirements. Agencies may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Application deadline",
            "Agency rules",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 30, §305.65",
            "TCEQ Rules"
        ],
        burden_holder="Operator",
        adversary_position="Agency may revoke permit or impose penalties for late application.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review application records, apply agency rules, and seek extension if necessary.",
        entity_scope="Operators, agencies",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 30, §305.65"
    ),
    DoctrineBlock(
        topic="Notice of Non-Compliance Deadline",
        keywords=["non-compliance", "notice deadline", "operator", "regulatory agency", "timely notice"],
        conclusion_template="Operators must provide notice of non-compliance within the deadline specified by agency rules.",
        reasoning_framework="""
        Regulatory agencies require operators to provide notice of non-compliance within a specified deadline after discovery. Failure to provide timely notice may result in penalties or enforcement actions. The operator bears the burden to demonstrate timely notice and compliance with all requirements. Agencies may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Notice deadline",
            "Agency rules",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 30, §305.65",
            "TCEQ Rules"
        ],
        burden_holder="Operator",
        adversary_position="Agency may impose penalties for late notice.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review notice records, apply agency rules, and seek extension if necessary.",
        entity_scope="Operators, agencies",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 30, §305.65"
    ),
    DoctrineBlock(
        topic="Annual Environmental Reporting Deadline",
        keywords=["annual environmental reporting", "deadline", "operator", "regulatory agency", "compliance"],
        conclusion_template="Operators must file annual environmental reports by the deadline specified by agency rules.",
        reasoning_framework="""
        Regulatory agencies require operators to file annual environmental reports by a specified deadline. Failure to comply may result in penalties or enforcement actions. The operator bears the burden to demonstrate timely filing and compliance with all requirements. Agencies may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Reporting deadline",
            "Agency rules",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 30, §305.65",
            "TCEQ Rules"
        ],
        burden_holder="Operator",
        adversary_position="Agency may impose penalties for late filing.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review reporting records, apply agency rules, and seek extension if necessary.",
        entity_scope="Operators, agencies",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 30, §305.65"
    ),
    DoctrineBlock(
        topic="Annual Groundwater Monitoring Reporting Deadline",
        keywords=["annual groundwater monitoring", "reporting deadline", "operator", "GCD", "compliance"],
        conclusion_template="Operators must file annual groundwater monitoring reports by the deadline specified by GCD rules.",
        reasoning_framework="""
        Groundwater Conservation Districts require operators to file annual groundwater monitoring reports by a specified deadline. Failure to comply may result in penalties or enforcement actions. The operator bears the burden to demonstrate timely filing and compliance with all requirements. GCDs may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Reporting deadline",
            "GCD rules",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Water Code §36.113",
            "GCD Rules"
        ],
        burden_holder="Operator",
        adversary_position="GCD may impose penalties for late filing.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review reporting records, apply GCD rules, and seek extension if necessary.",
        entity_scope="Operators, GCDs",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Water Code §36.113"
    ),
    DoctrineBlock(
        topic="Annual Severance Tax Reporting Deadline",
        keywords=["annual severance tax", "reporting deadline", "operator", "Texas Comptroller", "compliance"],
        conclusion_template="Operators must file annual severance tax reports by the deadline specified by Comptroller rules.",
        reasoning_framework="""
        The Texas Comptroller requires operators to file annual severance tax reports by a specified deadline. Failure to comply may result in penalties or enforcement actions. The operator bears the burden to demonstrate timely filing and compliance with all requirements. Comptroller may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Reporting deadline",
            "Comptroller rules",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Tax Code §201.101",
            "Texas Comptroller Rules"
        ],
        burden_holder="Operator",
        adversary_position="Comptroller may impose penalties for late filing.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review reporting records, apply Comptroller rules, and seek extension if necessary.",
        entity_scope="Operators, Comptroller",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Tax Code §201.101"
    ),
    DoctrineBlock(
        topic="Annual Production Reporting Deadline",
        keywords=["annual production reporting", "deadline", "operator", "Railroad Commission", "compliance"],
        conclusion_template="Operators must file annual production reports by the deadline specified by Railroad Commission rules.",
        reasoning_framework="""
        The Texas Railroad Commission requires operators to file annual production reports by a specified deadline. Failure to comply may result in penalties or enforcement actions. The operator bears the burden to demonstrate timely filing and compliance with all requirements. RRC may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Reporting deadline",
            "RRC rules",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.27",
            "Texas Railroad Commission Rule 27"
        ],
        burden_holder="Operator",
        adversary_position="RRC may impose penalties for late filing.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review reporting records, apply RRC rules, and seek extension if necessary.",
        entity_scope="Operators, RRC",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.27"
    ),
    DoctrineBlock(
        topic="Annual Lease Compliance Certification Deadline",
        keywords=["annual lease compliance", "certification deadline", "operator", "Railroad Commission", "compliance"],
        conclusion_template="Operators must file annual lease compliance certifications by the deadline specified by Railroad Commission rules.",
        reasoning_framework="""
        The Texas Railroad Commission requires operators to file annual lease compliance certifications by a specified deadline. Failure to comply may result in penalties or enforcement actions. The operator bears the burden to demonstrate timely filing and compliance with all requirements. RRC may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Certification deadline",
            "RRC rules",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.91",
            "Texas Railroad Commission Rule 91"
        ],
        burden_holder="Operator",
        adversary_position="RRC may impose penalties for late filing.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review certification records, apply RRC rules, and seek extension if necessary.",
        entity_scope="Operators, RRC",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.91"
    ),
    DoctrineBlock(
        topic="Annual Operator Registration Renewal Deadline",
        keywords=["annual operator registration", "renewal deadline", "operator", "Railroad Commission", "compliance"],
        conclusion_template="Operators must renew annual registration by the deadline specified by Railroad Commission rules.",
        reasoning_framework="""
        The Texas Railroad Commission requires operators to renew annual registration by a specified deadline. Failure to comply may result in penalties or enforcement actions. The operator bears the burden to demonstrate timely renewal and compliance with all requirements. RRC may grant extensions for good cause, but strict compliance is generally enforced.
        """,
        key_factors=[
            "Renewal deadline",
            "RRC rules",
            "Operator records",
            "Extension procedures"
        ],
        primary_authority=[
            "Texas Administrative Code Title 16, §3.1",
            "Texas Railroad Commission Rule 1"
        ],
        burden_holder="Operator",
        adversary_position="RRC may impose penalties for late renewal.",
        counter_arguments=[
            "Operator claims extension granted",
            "Operator asserts administrative error"
        ],
        resolution_strategy="Review renewal records, apply RRC rules, and seek extension if necessary.",
        entity_scope="Operators, RRC",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Administrative Code Title 16, §3.1"
    ),
    DoctrineBlock(
        topic="Annual Lease Option Exercise Deadline",
        keywords=["annual lease option", "exercise deadline", "lease", "operator", "timely exercise"],
        conclusion_template="Lessee must exercise annual lease options by the deadline specified in the lease.",
        reasoning_framework="""
        Annual lease options allow lessees to extend or renew leases for additional terms. The deadline for exercise is specified in the lease. Failure to exercise timely may result in loss of renewal rights. The lessee bears the burden to demonstrate timely exercise and compliance with all requirements. The lessor may challenge sufficiency or timeliness.
        """,
        key_factors=[
            "Exercise deadline",
            "Lease language",
            "Notice requirements",
            "Payment records"
        ],
        primary_authority=[
            "Texas Natural Resources Code §91.101",
            "W.T. Waggoner Estate v. Sigler Oil Co., 19 S.W.2d 27 (Tex. 1929)"
        ],
        burden_holder="Lessee",
        adversary_position="Lessor may assert loss of renewal rights.",
        counter_arguments=[
            "Lessee claims substantial compliance",
            "Lessee asserts ambiguity in option clause"
        ],
        resolution_strategy="Review lease terms, exercise records, and resolve ambiguities in favor of lessor.",
        entity_scope="Lessee, lessor",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="W.T. Waggoner Estate v. Sigler Oil Co., 19 S.W.2d 27 (Tex. 1929)"
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