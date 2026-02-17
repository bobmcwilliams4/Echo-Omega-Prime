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
        topic="New Filing Detection",
        keywords=["filing", "document", "record", "submission", "regulatory"],
        conclusion_template="A new filing has been detected for {entity}.",
        reasoning_framework="""
        The detection of a new filing is based on monitoring regulatory submissions and document records associated with the entity. 
        The framework involves periodic polling of relevant databases, cross-referencing entity identifiers, and validating document authenticity.
        Key factors include the timeliness of the filing, the completeness of documentation, and the relevance to the entity's operational scope.
        The burden holder is typically the regulatory authority, ensuring filings are properly recorded.
        Adversary positions may arise from disputes over filing legitimacy or completeness.
        Counter arguments focus on procedural errors or misidentification.
        Resolution involves verification through primary sources and cross-checking with regulatory databases.
        Confidence is high when filings are corroborated by multiple sources.
        """,
        key_factors=["timeliness", "completeness", "entity identifier", "document authenticity"],
        primary_authority=["Texas Railroad Commission", "County Clerk"],
        burden_holder="Regulatory Authority",
        adversary_position="Challenger disputing filing legitimacy",
        counter_arguments=["Procedural error", "Misidentification", "Incomplete documentation"],
        resolution_strategy="Cross-verification with authoritative databases and document validation.",
        entity_scope="All regulated entities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="RRC Filing Procedures 16 TAC §3.1"
    ),
    DoctrineBlock(
        topic="Ownership Transfer Detection",
        keywords=["ownership", "transfer", "assignment", "title", "conveyance"],
        conclusion_template="Ownership transfer detected for {asset} from {previous_owner} to {new_owner}.",
        reasoning_framework="""
        Ownership transfer is detected by monitoring assignments, conveyances, and title changes recorded in official registries.
        The framework includes matching asset identifiers, reviewing deed records, and validating signatures.
        Key factors are legal documentation, chain of title, and regulatory approval.
        Burden holder is the transferring party, ensuring proper documentation.
        Adversary positions may include contesting parties or claimants.
        Counter arguments focus on chain of title defects or unauthorized transfers.
        Resolution strategy involves legal review and title insurance verification.
        Confidence increases with notarized documents and regulatory confirmation.
        """,
        key_factors=["legal documentation", "chain of title", "regulatory approval"],
        primary_authority=["County Clerk", "Texas Railroad Commission"],
        burden_holder="Transferring Party",
        adversary_position="Contesting Claimant",
        counter_arguments=["Title defect", "Unauthorized transfer", "Forgery"],
        resolution_strategy="Legal review and title insurance verification.",
        entity_scope="Mineral and surface assets",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas Property Code §13.001"
    ),
    DoctrineBlock(
        topic="Lease Expiration Warning",
        keywords=["lease", "expiration", "term", "renewal", "deadline"],
        conclusion_template="Lease expiration warning issued for {lease} expiring on {date}.",
        reasoning_framework="""
        Lease expiration is tracked by monitoring lease terms and renewal deadlines.
        The framework involves calculation of lease duration, review of renewal clauses, and notification of impending expiration.
        Key factors include lease term, renewal option, and notice requirements.
        Burden holder is the lessee, responsible for timely renewal.
        Adversary position may be lessor seeking to terminate or renegotiate.
        Counter arguments include automatic renewal provisions or force majeure extensions.
        Resolution involves legal review of lease terms and communication with parties.
        Confidence is moderate to high, depending on document clarity.
        """,
        key_factors=["lease term", "renewal option", "notice requirements"],
        primary_authority=["Lease Agreement", "Texas Property Code"],
        burden_holder="Lessee",
        adversary_position="Lessor seeking termination",
        counter_arguments=["Automatic renewal", "Force majeure extension"],
        resolution_strategy="Legal review and party notification.",
        entity_scope="Mineral and surface leases",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="Texas Property Code §91.001"
    ),
    DoctrineBlock(
        topic="Lease Extension Deadline",
        keywords=["lease", "extension", "deadline", "renewal", "option"],
        conclusion_template="Lease extension deadline approaching for {lease} on {date}.",
        reasoning_framework="""
        Lease extension deadlines are monitored by tracking lease terms and renewal options.
        The framework includes calculation of extension periods, review of option clauses, and notification of deadlines.
        Key factors are extension period, option exercise requirements, and notice provisions.
        Burden holder is lessee, responsible for exercising extension option.
        Adversary position may be lessor disputing extension validity.
        Counter arguments focus on missed deadlines or improper notice.
        Resolution involves legal review and timely communication.
        Confidence is high when deadlines are clearly documented.
        """,
        key_factors=["extension period", "option exercise", "notice provisions"],
        primary_authority=["Lease Agreement", "Texas Property Code"],
        burden_holder="Lessee",
        adversary_position="Lessor disputing extension",
        counter_arguments=["Missed deadline", "Improper notice"],
        resolution_strategy="Legal review and timely notification.",
        entity_scope="Mineral and surface leases",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Texas Property Code §91.002"
    ),
    DoctrineBlock(
        topic="Drilling Permit Issued",
        keywords=["drilling", "permit", "issuance", "approval", "regulatory"],
        conclusion_template="Drilling permit issued for {well} on {date}.",
        reasoning_framework="""
        Drilling permit issuance is detected by monitoring regulatory approvals and permit records.
        The framework involves validation of permit applications, review of compliance documents, and confirmation of regulatory approval.
        Key factors include permit application completeness, compliance with regulations, and approval date.
        Burden holder is applicant, responsible for submitting required documents.
        Adversary position may be regulatory authority or affected parties.
        Counter arguments focus on environmental concerns or procedural deficiencies.
        Resolution strategy involves regulatory review and public notice.
        Confidence is high when permit is recorded in official registry.
        """,
        key_factors=["permit application", "regulatory compliance", "approval date"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Applicant",
        adversary_position="Regulatory authority or affected party",
        counter_arguments=["Environmental concern", "Procedural deficiency"],
        resolution_strategy="Regulatory review and public notice.",
        entity_scope="Oil and gas wells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.5"
    ),
    DoctrineBlock(
        topic="Permit Expiration Warning",
        keywords=["permit", "expiration", "deadline", "regulatory", "compliance"],
        conclusion_template="Permit expiration warning issued for {permit} expiring on {date}.",
        reasoning_framework="""
        Permit expiration is monitored by tracking permit terms and regulatory deadlines.
        The framework includes calculation of permit duration, review of renewal requirements, and notification of impending expiration.
        Key factors are permit term, renewal process, and compliance status.
        Burden holder is permit holder, responsible for renewal.
        Adversary position may be regulatory authority enforcing expiration.
        Counter arguments include pending renewal applications or force majeure.
        Resolution involves regulatory review and communication with permit holder.
        Confidence is high when expiration dates are documented.
        """,
        key_factors=["permit term", "renewal process", "compliance status"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Permit Holder",
        adversary_position="Regulatory authority enforcing expiration",
        counter_arguments=["Pending renewal", "Force majeure"],
        resolution_strategy="Regulatory review and notification.",
        entity_scope="Oil and gas permits",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.5"
    ),
    DoctrineBlock(
        topic="RRC Violation Detection",
        keywords=["violation", "RRC", "compliance", "regulatory", "enforcement"],
        conclusion_template="RRC violation detected for {entity} on {date}.",
        reasoning_framework="""
        RRC violation detection is based on monitoring regulatory enforcement actions and compliance records.
        The framework involves review of inspection reports, violation notices, and enforcement orders.
        Key factors are nature of violation, regulatory response, and corrective actions.
        Burden holder is regulated entity, responsible for compliance.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural errors or compliance efforts.
        Resolution strategy involves regulatory hearing and corrective action plan.
        Confidence is high when violation is confirmed by official notice.
        """,
        key_factors=["inspection report", "violation notice", "corrective action"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Regulated Entity",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Compliance effort"],
        resolution_strategy="Regulatory hearing and corrective action.",
        entity_scope="Oil and gas operators",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.8"
    ),
    DoctrineBlock(
        topic="Production Change Detection",
        keywords=["production", "change", "volume", "reporting", "trend"],
        conclusion_template="Production change detected for {well} on {date}.",
        reasoning_framework="""
        Production change detection is based on monitoring production reports and volume trends.
        The framework includes analysis of monthly production data, comparison with historical averages, and identification of anomalies.
        Key factors are production volume, reporting frequency, and operational changes.
        Burden holder is operator, responsible for accurate reporting.
        Adversary position may be royalty owners or regulatory authority.
        Counter arguments focus on reporting errors or operational disruptions.
        Resolution involves data verification and operational review.
        Confidence is moderate to high, depending on data quality.
        """,
        key_factors=["production volume", "reporting frequency", "operational change"],
        primary_authority=["Texas Railroad Commission", "Production Reports"],
        burden_holder="Operator",
        adversary_position="Royalty owner or regulatory authority",
        counter_arguments=["Reporting error", "Operational disruption"],
        resolution_strategy="Data verification and operational review.",
        entity_scope="Oil and gas wells",
        confidence=0.93,
        confidence_zone="Moderate-High",
        controlling_precedent="16 TAC §3.27"
    ),
    DoctrineBlock(
        topic="Operator Change Detection",
        keywords=["operator", "change", "assignment", "transfer", "notification"],
        conclusion_template="Operator change detected for {well} from {previous_operator} to {new_operator}.",
        reasoning_framework="""
        Operator change is detected by monitoring assignments, regulatory notifications, and permit transfers.
        The framework involves review of operator assignment documents, regulatory filings, and confirmation of transfer.
        Key factors are regulatory approval, assignment documentation, and notification to stakeholders.
        Burden holder is outgoing operator, responsible for proper notification.
        Adversary position may be affected parties or regulatory authority.
        Counter arguments focus on unauthorized transfer or incomplete notification.
        Resolution strategy involves regulatory review and stakeholder communication.
        Confidence is high when changes are recorded in official registry.
        """,
        key_factors=["regulatory approval", "assignment documentation", "stakeholder notification"],
        primary_authority=["Texas Railroad Commission", "Assignment Records"],
        burden_holder="Outgoing Operator",
        adversary_position="Affected party or regulatory authority",
        counter_arguments=["Unauthorized transfer", "Incomplete notification"],
        resolution_strategy="Regulatory review and stakeholder communication.",
        entity_scope="Oil and gas wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.4"
    ),
    DoctrineBlock(
        topic="Lien Filed Detection",
        keywords=["lien", "filing", "recording", "claim", "security interest"],
        conclusion_template="Lien filed detected for {asset} by {claimant} on {date}.",
        reasoning_framework="""
        Lien filing is detected by monitoring county records and regulatory filings.
        The framework involves review of lien documents, verification of claimant identity, and validation of asset description.
        Key factors are lien type, asset identification, and claimant legitimacy.
        Burden holder is claimant, responsible for proper filing.
        Adversary position may be asset owner or competing claimants.
        Counter arguments focus on improper filing or invalid claim.
        Resolution strategy involves legal review and title search.
        Confidence is high when lien is recorded in official registry.
        """,
        key_factors=["lien type", "asset identification", "claimant legitimacy"],
        primary_authority=["County Clerk", "Texas Property Code"],
        burden_holder="Claimant",
        adversary_position="Asset owner or competing claimant",
        counter_arguments=["Improper filing", "Invalid claim"],
        resolution_strategy="Legal review and title search.",
        entity_scope="Mineral and surface assets",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Property Code §53.052"
    ),
    DoctrineBlock(
        topic="Lien Release Detection",
        keywords=["lien", "release", "recording", "claim", "security interest"],
        conclusion_template="Lien release detected for {asset} by {claimant} on {date}.",
        reasoning_framework="""
        Lien release is detected by monitoring county records and regulatory filings.
        The framework includes review of release documents, verification of claimant identity, and validation of asset description.
        Key factors are release documentation, asset identification, and claimant legitimacy.
        Burden holder is claimant, responsible for proper release filing.
        Adversary position may be asset owner or competing claimants.
        Counter arguments focus on improper release or unresolved claim.
        Resolution strategy involves legal review and title search.
        Confidence is high when release is recorded in official registry.
        """,
        key_factors=["release documentation", "asset identification", "claimant legitimacy"],
        primary_authority=["County Clerk", "Texas Property Code"],
        burden_holder="Claimant",
        adversary_position="Asset owner or competing claimant",
        counter_arguments=["Improper release", "Unresolved claim"],
        resolution_strategy="Legal review and title search.",
        entity_scope="Mineral and surface assets",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Property Code §53.152"
    ),
    DoctrineBlock(
        topic="Probate Filing Detection",
        keywords=["probate", "filing", "estate", "inheritance", "court"],
        conclusion_template="Probate filing detected for estate of {decedent} on {date}.",
        reasoning_framework="""
        Probate filing is detected by monitoring court records and estate filings.
        The framework involves review of probate petitions, verification of decedent identity, and validation of estate assets.
        Key factors are probate petition, decedent identification, and asset inventory.
        Burden holder is petitioner, responsible for proper filing.
        Adversary position may be heirs or creditors.
        Counter arguments focus on contested will or improper asset inventory.
        Resolution strategy involves legal review and court hearing.
        Confidence is high when filing is recorded in court registry.
        """,
        key_factors=["probate petition", "decedent identification", "asset inventory"],
        primary_authority=["County Probate Court", "Texas Estates Code"],
        burden_holder="Petitioner",
        adversary_position="Heir or creditor",
        counter_arguments=["Contested will", "Improper asset inventory"],
        resolution_strategy="Legal review and court hearing.",
        entity_scope="Estates",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas Estates Code §256.051"
    ),
    DoctrineBlock(
        topic="Court Order Detection",
        keywords=["court", "order", "judgment", "decree", "legal"],
        conclusion_template="Court order detected for {entity} on {date}.",
        reasoning_framework="""
        Court order detection is based on monitoring court filings and legal decrees.
        The framework includes review of court orders, validation of legal authority, and confirmation of affected parties.
        Key factors are court order documentation, legal authority, and party identification.
        Burden holder is court, responsible for proper issuance.
        Adversary position may be affected parties.
        Counter arguments focus on appeal or procedural error.
        Resolution strategy involves legal review and appeal process.
        Confidence is high when order is recorded in court registry.
        """,
        key_factors=["court order documentation", "legal authority", "party identification"],
        primary_authority=["County Court", "Texas Civil Practice & Remedies Code"],
        burden_holder="Court",
        adversary_position="Affected party",
        counter_arguments=["Appeal", "Procedural error"],
        resolution_strategy="Legal review and appeal process.",
        entity_scope="All entities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Texas Civil Practice & Remedies Code §11.001"
    ),
    DoctrineBlock(
        topic="Tax Delinquency Detection",
        keywords=["tax", "delinquency", "arrears", "property", "assessment"],
        conclusion_template="Tax delinquency detected for {property} on {date}.",
        reasoning_framework="""
        Tax delinquency detection is based on monitoring tax assessment records and payment histories.
        The framework includes review of tax rolls, payment status, and delinquency notices.
        Key factors are tax assessment, payment history, and delinquency notice.
        Burden holder is property owner, responsible for payment.
        Adversary position is taxing authority.
        Counter arguments focus on payment dispute or assessment error.
        Resolution strategy involves payment verification and dispute resolution.
        Confidence is high when delinquency is recorded in official registry.
        """,
        key_factors=["tax assessment", "payment history", "delinquency notice"],
        primary_authority=["County Tax Assessor", "Texas Tax Code"],
        burden_holder="Property Owner",
        adversary_position="Taxing authority",
        counter_arguments=["Payment dispute", "Assessment error"],
        resolution_strategy="Payment verification and dispute resolution.",
        entity_scope="Property owners",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Texas Tax Code §31.01"
    ),
    DoctrineBlock(
        topic="Competitive Activity Detection",
        keywords=["competitive", "activity", "operator", "lease", "drilling"],
        conclusion_template="Competitive activity detected near {lease} by {operator} on {date}.",
        reasoning_framework="""
        Competitive activity detection is based on monitoring drilling permits, lease assignments, and production reports in proximity to subject lease.
        The framework includes spatial analysis, review of regulatory filings, and identification of new operators.
        Key factors are proximity, operator identity, and activity type.
        Burden holder is competitor, responsible for regulatory compliance.
        Adversary position may be incumbent operator or leaseholder.
        Counter arguments focus on regulatory violations or lease encroachment.
        Resolution strategy involves regulatory review and lease boundary analysis.
        Confidence is moderate to high, depending on data accuracy.
        """,
        key_factors=["proximity", "operator identity", "activity type"],
        primary_authority=["Texas Railroad Commission", "Lease Records"],
        burden_holder="Competitor",
        adversary_position="Incumbent operator or leaseholder",
        counter_arguments=["Regulatory violation", "Lease encroachment"],
        resolution_strategy="Regulatory review and boundary analysis.",
        entity_scope="Oil and gas leases",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="16 TAC §3.37"
    ),
    DoctrineBlock(
        topic="Price Threshold Alert",
        keywords=["price", "threshold", "market", "commodity", "alert"],
        conclusion_template="Price threshold alert triggered for {commodity} at {price} on {date}.",
        reasoning_framework="""
        Price threshold alerts are triggered by monitoring commodity market prices and comparing against predefined thresholds.
        The framework includes real-time price monitoring, historical trend analysis, and threshold configuration.
        Key factors are market price, threshold setting, and commodity type.
        Burden holder is operator or royalty owner, affected by price changes.
        Adversary position may be market participants.
        Counter arguments focus on market volatility or threshold misconfiguration.
        Resolution strategy involves threshold adjustment and market analysis.
        Confidence is high when price data is sourced from authoritative markets.
        """,
        key_factors=["market price", "threshold setting", "commodity type"],
        primary_authority=["NYMEX", "Texas Railroad Commission"],
        burden_holder="Operator or Royalty Owner",
        adversary_position="Market participant",
        counter_arguments=["Market volatility", "Threshold misconfiguration"],
        resolution_strategy="Threshold adjustment and market analysis.",
        entity_scope="Oil and gas commodities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NYMEX Pricing Rules"
    ),
    DoctrineBlock(
        topic="Royalty Payment Alert",
        keywords=["royalty", "payment", "distribution", "owner", "alert"],
        conclusion_template="Royalty payment alert issued for {owner} on {date}.",
        reasoning_framework="""
        Royalty payment alerts are triggered by monitoring payment records and distribution schedules.
        The framework includes review of payment history, calculation of distribution amounts, and notification of payment events.
        Key factors are payment amount, distribution schedule, and owner identification.
        Burden holder is operator, responsible for payment.
        Adversary position may be royalty owner disputing payment.
        Counter arguments focus on calculation errors or payment delays.
        Resolution strategy involves payment verification and dispute resolution.
        Confidence is high when payment records are corroborated.
        """,
        key_factors=["payment amount", "distribution schedule", "owner identification"],
        primary_authority=["Texas Railroad Commission", "Division Order Records"],
        burden_holder="Operator",
        adversary_position="Royalty owner disputing payment",
        counter_arguments=["Calculation error", "Payment delay"],
        resolution_strategy="Payment verification and dispute resolution.",
        entity_scope="Royalty owners",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Natural Resources Code §91.402"
    ),
    DoctrineBlock(
        topic="Well Shut-In Detection",
        keywords=["well", "shut-in", "status", "production", "regulatory"],
        conclusion_template="Well shut-in detected for {well} on {date}.",
        reasoning_framework="""
        Well shut-in detection is based on monitoring production status and regulatory filings.
        The framework includes review of production reports, shut-in notifications, and regulatory compliance documents.
        Key factors are production status, shut-in notice, and regulatory approval.
        Burden holder is operator, responsible for notification.
        Adversary position may be regulatory authority or royalty owner.
        Counter arguments focus on operational necessity or regulatory exemption.
        Resolution strategy involves regulatory review and operational analysis.
        Confidence is high when shut-in is documented.
        """,
        key_factors=["production status", "shut-in notice", "regulatory approval"],
        primary_authority=["Texas Railroad Commission", "Production Reports"],
        burden_holder="Operator",
        adversary_position="Regulatory authority or royalty owner",
        counter_arguments=["Operational necessity", "Regulatory exemption"],
        resolution_strategy="Regulatory review and operational analysis.",
        entity_scope="Oil and gas wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.15"
    ),
    DoctrineBlock(
        topic="Plugging Notice Detection",
        keywords=["plugging", "notice", "well", "abandonment", "regulatory"],
        conclusion_template="Plugging notice detected for {well} on {date}.",
        reasoning_framework="""
        Plugging notice detection is based on monitoring regulatory filings and abandonment notifications.
        The framework includes review of plugging applications, regulatory approvals, and well status reports.
        Key factors are plugging application, regulatory approval, and well status.
        Burden holder is operator, responsible for proper notification.
        Adversary position may be regulatory authority or affected parties.
        Counter arguments focus on environmental concerns or procedural errors.
        Resolution strategy involves regulatory review and environmental assessment.
        Confidence is high when notice is recorded.
        """,
        key_factors=["plugging application", "regulatory approval", "well status"],
        primary_authority=["Texas Railroad Commission", "Plugging Records"],
        burden_holder="Operator",
        adversary_position="Regulatory authority or affected party",
        counter_arguments=["Environmental concern", "Procedural error"],
        resolution_strategy="Regulatory review and environmental assessment.",
        entity_scope="Oil and gas wells",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.16"
    ),
    DoctrineBlock(
        topic="Unitization Application",
        keywords=["unitization", "application", "pooling", "regulatory", "approval"],
        conclusion_template="Unitization application detected for {unit} on {date}.",
        reasoning_framework="""
        Unitization application detection is based on monitoring regulatory filings and pooling agreements.
        The framework includes review of unitization petitions, regulatory approvals, and stakeholder notifications.
        Key factors are unitization petition, regulatory approval, and stakeholder consent.
        Burden holder is applicant, responsible for proper filing.
        Adversary position may be non-consenting parties.
        Counter arguments focus on lack of consent or regulatory deficiency.
        Resolution strategy involves regulatory hearing and stakeholder negotiation.
        Confidence is high when application is recorded.
        """,
        key_factors=["unitization petition", "regulatory approval", "stakeholder consent"],
        primary_authority=["Texas Railroad Commission", "Unitization Records"],
        burden_holder="Applicant",
        adversary_position="Non-consenting party",
        counter_arguments=["Lack of consent", "Regulatory deficiency"],
        resolution_strategy="Regulatory hearing and stakeholder negotiation.",
        entity_scope="Oil and gas units",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Texas Natural Resources Code §104.001"
    ),
    DoctrineBlock(
        topic="Force Pooling Application",
        keywords=["force pooling", "application", "regulatory", "approval", "compulsory"],
        conclusion_template="Force pooling application detected for {unit} on {date}.",
        reasoning_framework="""
        Force pooling application detection is based on monitoring regulatory filings and compulsory pooling petitions.
        The framework includes review of force pooling applications, regulatory approvals, and affected party notifications.
        Key factors are force pooling application, regulatory approval, and affected party identification.
        Burden holder is applicant, responsible for proper filing.
        Adversary position may be non-consenting parties.
        Counter arguments focus on lack of notice or regulatory deficiency.
        Resolution strategy involves regulatory hearing and party negotiation.
        Confidence is high when application is recorded.
        """,
        key_factors=["force pooling application", "regulatory approval", "affected party identification"],
        primary_authority=["Texas Railroad Commission", "Pooling Records"],
        burden_holder="Applicant",
        adversary_position="Non-consenting party",
        counter_arguments=["Lack of notice", "Regulatory deficiency"],
        resolution_strategy="Regulatory hearing and party negotiation.",
        entity_scope="Oil and gas units",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Natural Resources Code §102.011"
    ),
    DoctrineBlock(
        topic="Surface Damage Claim",
        keywords=["surface", "damage", "claim", "compensation", "property"],
        conclusion_template="Surface damage claim detected for {property} by {claimant} on {date}.",
        reasoning_framework="""
        Surface damage claim detection is based on monitoring property records and compensation claims.
        The framework includes review of damage claim documents, verification of claimant identity, and assessment of property impact.
        Key factors are damage documentation, claimant legitimacy, and property impact assessment.
        Burden holder is claimant, responsible for proper filing.
        Adversary position may be property owner or operator.
        Counter arguments focus on lack of evidence or compensation dispute.
        Resolution strategy involves legal review and property assessment.
        Confidence is moderate to high, depending on documentation.
        """,
        key_factors=["damage documentation", "claimant legitimacy", "property impact assessment"],
        primary_authority=["County Clerk", "Texas Property Code"],
        burden_holder="Claimant",
        adversary_position="Property owner or operator",
        counter_arguments=["Lack of evidence", "Compensation dispute"],
        resolution_strategy="Legal review and property assessment.",
        entity_scope="Surface property",
        confidence=0.91,
        confidence_zone="Moderate-High",
        controlling_precedent="Texas Property Code §21.042"
    ),
    DoctrineBlock(
        topic="Environmental Release Detection",
        keywords=["environmental", "release", "spill", "contamination", "regulatory"],
        conclusion_template="Environmental release detected for {site} on {date}.",
        reasoning_framework="""
        Environmental release detection is based on monitoring regulatory filings, spill reports, and site inspections.
        The framework includes review of release notifications, regulatory compliance documents, and site assessment reports.
        Key factors are release documentation, regulatory approval, and site impact assessment.
        Burden holder is operator, responsible for notification and remediation.
        Adversary position may be regulatory authority or affected parties.
        Counter arguments focus on lack of evidence or regulatory exemption.
        Resolution strategy involves regulatory review and environmental assessment.
        Confidence is high when release is documented.
        """,
        key_factors=["release documentation", "regulatory approval", "site impact assessment"],
        primary_authority=["Texas Railroad Commission", "Texas Commission on Environmental Quality"],
        burden_holder="Operator",
        adversary_position="Regulatory authority or affected party",
        counter_arguments=["Lack of evidence", "Regulatory exemption"],
        resolution_strategy="Regulatory review and environmental assessment.",
        entity_scope="Oil and gas sites",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.8"
    ),
    DoctrineBlock(
        topic="Bankruptcy Filing Detection",
        keywords=["bankruptcy", "filing", "debtor", "court", "insolvency"],
        conclusion_template="Bankruptcy filing detected for {entity} on {date}.",
        reasoning_framework="""
        Bankruptcy filing detection is based on monitoring court records and debtor filings.
        The framework includes review of bankruptcy petitions, verification of debtor identity, and assessment of asset impact.
        Key factors are bankruptcy petition, debtor identification, and asset inventory.
        Burden holder is debtor, responsible for proper filing.
        Adversary position may be creditors or affected parties.
        Counter arguments focus on improper filing or asset concealment.
        Resolution strategy involves legal review and court hearing.
        Confidence is high when filing is recorded in court registry.
        """,
        key_factors=["bankruptcy petition", "debtor identification", "asset inventory"],
        primary_authority=["Federal Bankruptcy Court", "Texas Bankruptcy Code"],
        burden_holder="Debtor",
        adversary_position="Creditor or affected party",
        counter_arguments=["Improper filing", "Asset concealment"],
        resolution_strategy="Legal review and court hearing.",
        entity_scope="All entities",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="11 U.S.C. §301"
    ),
    DoctrineBlock(
        topic="Title Defect Detection",
        keywords=["title", "defect", "chain", "ownership", "record"],
        conclusion_template="Title defect detected for {asset} on {date}.",
        reasoning_framework="""
        Title defect detection is based on monitoring title records, chain of ownership, and legal filings.
        The framework includes review of title documents, chain of title analysis, and identification of defects.
        Key factors are title documentation, chain of ownership, and defect identification.
        Burden holder is asset owner, responsible for curing defects.
        Adversary position may be competing claimants.
        Counter arguments focus on lack of evidence or procedural error.
        Resolution strategy involves legal review and title insurance.
        Confidence is moderate to high, depending on documentation.
        """,
        key_factors=["title documentation", "chain of ownership", "defect identification"],
        primary_authority=["County Clerk", "Texas Property Code"],
        burden_holder="Asset Owner",
        adversary_position="Competing claimant",
        counter_arguments=["Lack of evidence", "Procedural error"],
        resolution_strategy="Legal review and title insurance.",
        entity_scope="Mineral and surface assets",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="Texas Property Code §13.001"
    ),
    DoctrineBlock(
        topic="Assignment Recording",
        keywords=["assignment", "recording", "transfer", "ownership", "document"],
        conclusion_template="Assignment recording detected for {asset} from {assignor} to {assignee} on {date}.",
        reasoning_framework="""
        Assignment recording is detected by monitoring county records and regulatory filings.
        The framework includes review of assignment documents, verification of assignor and assignee identities, and validation of asset description.
        Key factors are assignment documentation, asset identification, and party legitimacy.
        Burden holder is assignor, responsible for proper recording.
        Adversary position may be assignee or competing claimants.
        Counter arguments focus on improper recording or invalid assignment.
        Resolution strategy involves legal review and title search.
        Confidence is high when assignment is recorded in official registry.
        """,
        key_factors=["assignment documentation", "asset identification", "party legitimacy"],
        primary_authority=["County Clerk", "Texas Property Code"],
        burden_holder="Assignor",
        adversary_position="Assignee or competing claimant",
        counter_arguments=["Improper recording", "Invalid assignment"],
        resolution_strategy="Legal review and title search.",
        entity_scope="Mineral and surface assets",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Texas Property Code §13.002"
    ),
    DoctrineBlock(
        topic="Division Order Change",
        keywords=["division order", "change", "royalty", "payment", "owner"],
        conclusion_template="Division order change detected for {owner} on {date}.",
        reasoning_framework="""
        Division order change detection is based on monitoring payment records and owner notifications.
        The framework includes review of division order documents, verification of owner identity, and calculation of payment changes.
        Key factors are division order documentation, owner identification, and payment calculation.
        Burden holder is operator, responsible for proper notification.
        Adversary position may be royalty owner or affected party.
        Counter arguments focus on calculation error or improper notification.
        Resolution strategy involves payment verification and dispute resolution.
        Confidence is high when changes are documented.
        """,
        key_factors=["division order documentation", "owner identification", "payment calculation"],
        primary_authority=["Texas Railroad Commission", "Division Order Records"],
        burden_holder="Operator",
        adversary_position="Royalty owner or affected party",
        counter_arguments=["Calculation error", "Improper notification"],
        resolution_strategy="Payment verification and dispute resolution.",
        entity_scope="Royalty owners",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Texas Natural Resources Code §91.402"
    ),
    DoctrineBlock(
        topic="Well Completion Notice",
        keywords=["well", "completion", "notice", "regulatory", "production"],
        conclusion_template="Well completion notice detected for {well} on {date}.",
        reasoning_framework="""
        Well completion notice detection is based on monitoring regulatory filings and production reports.
        The framework includes review of completion documents, regulatory approvals, and production status.
        Key factors are completion documentation, regulatory approval, and production status.
        Burden holder is operator, responsible for proper notification.
        Adversary position may be regulatory authority or affected parties.
        Counter arguments focus on procedural error or regulatory deficiency.
        Resolution strategy involves regulatory review and operational analysis.
        Confidence is high when notice is recorded.
        """,
        key_factors=["completion documentation", "regulatory approval", "production status"],
        primary_authority=["Texas Railroad Commission", "Completion Records"],
        burden_holder="Operator",
        adversary_position="Regulatory authority or affected party",
        counter_arguments=["Procedural error", "Regulatory deficiency"],
        resolution_strategy="Regulatory review and operational analysis.",
        entity_scope="Oil and gas wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.13"
    ),
    DoctrineBlock(
        topic="Spacing Order Detection",
        keywords=["spacing", "order", "regulatory", "well", "permit"],
        conclusion_template="Spacing order detected for {well} on {date}.",
        reasoning_framework="""
        Spacing order detection is based on monitoring regulatory filings and permit applications.
        The framework includes review of spacing order documents, regulatory approvals, and well location analysis.
        Key factors are spacing order documentation, regulatory approval, and well location.
        Burden holder is operator, responsible for compliance.
        Adversary position may be regulatory authority or affected parties.
        Counter arguments focus on regulatory deficiency or location dispute.
        Resolution strategy involves regulatory review and location analysis.
        Confidence is high when order is recorded.
        """,
        key_factors=["spacing order documentation", "regulatory approval", "well location"],
        primary_authority=["Texas Railroad Commission", "Spacing Order Records"],
        burden_holder="Operator",
        adversary_position="Regulatory authority or affected party",
        counter_arguments=["Regulatory deficiency", "Location dispute"],
        resolution_strategy="Regulatory review and location analysis.",
        entity_scope="Oil and gas wells",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.37"
    ),
    DoctrineBlock(
        topic="Force Majeure Declaration",
        keywords=["force majeure", "declaration", "event", "contract", "regulatory"],
        conclusion_template="Force majeure declaration detected for {entity} on {date}.",
        reasoning_framework="""
        Force majeure declaration detection is based on monitoring contract filings and regulatory notifications.
        The framework includes review of force majeure documents, validation of event description, and assessment of contractual impact.
        Key factors are force majeure documentation, event description, and contract impact.
        Burden holder is declaring party, responsible for proper notification.
        Adversary position may be counterparty or regulatory authority.
        Counter arguments focus on event legitimacy or contractual exclusion.
        Resolution strategy involves legal review and contract analysis.
        Confidence is moderate to high, depending on event documentation.
        """,
        key_factors=["force majeure documentation", "event description", "contract impact"],
        primary_authority=["Contract Documents", "Texas Railroad Commission"],
        burden_holder="Declaring Party",
        adversary_position="Counterparty or regulatory authority",
        counter_arguments=["Event legitimacy", "Contractual exclusion"],
        resolution_strategy="Legal review and contract analysis.",
        entity_scope="All entities",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="Texas Business & Commerce Code §2.615"
    ),
    DoctrineBlock(
        topic="Well Recompletion Notice",
        keywords=["well", "recompletion", "notice", "regulatory", "production"],
        conclusion_template="Well recompletion notice detected for {well} on {date}.",
        reasoning_framework="""
        Well recompletion notice detection is based on monitoring regulatory filings and production reports.
        The framework includes review of recompletion documents, regulatory approvals, and production status.
        Key factors are recompletion documentation, regulatory approval, and production status.
        Burden holder is operator, responsible for proper notification.
        Adversary position may be regulatory authority or affected parties.
        Counter arguments focus on procedural error or regulatory deficiency.
        Resolution strategy involves regulatory review and operational analysis.
        Confidence is high when notice is recorded.
        """,
        key_factors=["recompletion documentation", "regulatory approval", "production status"],
        primary_authority=["Texas Railroad Commission", "Recompletion Records"],
        burden_holder="Operator",
        adversary_position="Regulatory authority or affected party",
        counter_arguments=["Procedural error", "Regulatory deficiency"],
        resolution_strategy="Regulatory review and operational analysis.",
        entity_scope="Oil and gas wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.13"
    ),
    DoctrineBlock(
        topic="Permit Suspension Detection",
        keywords=["permit", "suspension", "regulatory", "compliance", "enforcement"],
        conclusion_template="Permit suspension detected for {permit} on {date}.",
        reasoning_framework="""
        Permit suspension detection is based on monitoring regulatory enforcement actions and compliance records.
        The framework includes review of suspension notices, regulatory orders, and compliance documents.
        Key factors are suspension notice, regulatory order, and compliance status.
        Burden holder is permit holder, responsible for compliance.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural error or compliance effort.
        Resolution strategy involves regulatory hearing and corrective action.
        Confidence is high when suspension is confirmed by official notice.
        """,
        key_factors=["suspension notice", "regulatory order", "compliance status"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Permit Holder",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Compliance effort"],
        resolution_strategy="Regulatory hearing and corrective action.",
        entity_scope="Oil and gas permits",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.8"
    ),
    DoctrineBlock(
        topic="Well Abandonment Detection",
        keywords=["well", "abandonment", "status", "regulatory", "notification"],
        conclusion_template="Well abandonment detected for {well} on {date}.",
        reasoning_framework="""
        Well abandonment detection is based on monitoring regulatory filings and well status reports.
        The framework includes review of abandonment documents, regulatory approvals, and production status.
        Key factors are abandonment documentation, regulatory approval, and production status.
        Burden holder is operator, responsible for proper notification.
        Adversary position may be regulatory authority or affected parties.
        Counter arguments focus on procedural error or regulatory deficiency.
        Resolution strategy involves regulatory review and operational analysis.
        Confidence is high when abandonment is recorded.
        """,
        key_factors=["abandonment documentation", "regulatory approval", "production status"],
        primary_authority=["Texas Railroad Commission", "Abandonment Records"],
        burden_holder="Operator",
        adversary_position="Regulatory authority or affected party",
        counter_arguments=["Procedural error", "Regulatory deficiency"],
        resolution_strategy="Regulatory review and operational analysis.",
        entity_scope="Oil and gas wells",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.16"
    ),
    DoctrineBlock(
        topic="Permit Revocation Detection",
        keywords=["permit", "revocation", "regulatory", "compliance", "enforcement"],
        conclusion_template="Permit revocation detected for {permit} on {date}.",
        reasoning_framework="""
        Permit revocation detection is based on monitoring regulatory enforcement actions and compliance records.
        The framework includes review of revocation notices, regulatory orders, and compliance documents.
        Key factors are revocation notice, regulatory order, and compliance status.
        Burden holder is permit holder, responsible for compliance.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural error or compliance effort.
        Resolution strategy involves regulatory hearing and corrective action.
        Confidence is high when revocation is confirmed by official notice.
        """,
        key_factors=["revocation notice", "regulatory order", "compliance status"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Permit Holder",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Compliance effort"],
        resolution_strategy="Regulatory hearing and corrective action.",
        entity_scope="Oil and gas permits",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.8"
    ),
    DoctrineBlock(
        topic="Production Allocation Change",
        keywords=["production", "allocation", "change", "reporting", "owner"],
        conclusion_template="Production allocation change detected for {well} on {date}.",
        reasoning_framework="""
        Production allocation change detection is based on monitoring allocation reports and owner notifications.
        The framework includes review of allocation documents, verification of owner identity, and calculation of allocation changes.
        Key factors are allocation documentation, owner identification, and allocation calculation.
        Burden holder is operator, responsible for proper notification.
        Adversary position may be royalty owner or affected party.
        Counter arguments focus on calculation error or improper notification.
        Resolution strategy involves allocation verification and dispute resolution.
        Confidence is high when changes are documented.
        """,
        key_factors=["allocation documentation", "owner identification", "allocation calculation"],
        primary_authority=["Texas Railroad Commission", "Allocation Records"],
        burden_holder="Operator",
        adversary_position="Royalty owner or affected party",
        counter_arguments=["Calculation error", "Improper notification"],
        resolution_strategy="Allocation verification and dispute resolution.",
        entity_scope="Oil and gas wells",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.27"
    ),
    DoctrineBlock(
        topic="Production Reporting Error",
        keywords=["production", "reporting", "error", "regulatory", "compliance"],
        conclusion_template="Production reporting error detected for {well} on {date}.",
        reasoning_framework="""
        Production reporting error detection is based on monitoring production reports and regulatory filings.
        The framework includes review of reporting documents, comparison with historical data, and identification of anomalies.
        Key factors are reporting documentation, historical data, and anomaly identification.
        Burden holder is operator, responsible for accurate reporting.
        Adversary position may be regulatory authority or royalty owner.
        Counter arguments focus on operational disruption or regulatory exemption.
        Resolution strategy involves data verification and operational review.
        Confidence is moderate to high, depending on data quality.
        """,
        key_factors=["reporting documentation", "historical data", "anomaly identification"],
        primary_authority=["Texas Railroad Commission", "Production Reports"],
        burden_holder="Operator",
        adversary_position="Regulatory authority or royalty owner",
        counter_arguments=["Operational disruption", "Regulatory exemption"],
        resolution_strategy="Data verification and operational review.",
        entity_scope="Oil and gas wells",
        confidence=0.92,
        confidence_zone="Moderate-High",
        controlling_precedent="16 TAC §3.27"
    ),
    DoctrineBlock(
        topic="Permit Application Deficiency",
        keywords=["permit", "application", "deficiency", "regulatory", "compliance"],
        conclusion_template="Permit application deficiency detected for {permit} on {date}.",
        reasoning_framework="""
        Permit application deficiency detection is based on monitoring regulatory filings and application reviews.
        The framework includes review of application documents, identification of missing information, and notification of deficiency.
        Key factors are application documentation, missing information, and regulatory requirements.
        Burden holder is applicant, responsible for correcting deficiencies.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural error or regulatory exemption.
        Resolution strategy involves application correction and regulatory review.
        Confidence is high when deficiency is documented.
        """,
        key_factors=["application documentation", "missing information", "regulatory requirements"],
        primary_authority=["Texas Railroad Commission", "Permit Application Records"],
        burden_holder="Applicant",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Regulatory exemption"],
        resolution_strategy="Application correction and regulatory review.",
        entity_scope="Oil and gas permits",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.5"
    ),
    DoctrineBlock(
        topic="Regulatory Notice Detection",
        keywords=["regulatory", "notice", "filing", "compliance", "enforcement"],
        conclusion_template="Regulatory notice detected for {entity} on {date}.",
        reasoning_framework="""
        Regulatory notice detection is based on monitoring regulatory filings and enforcement actions.
        The framework includes review of notice documents, validation of regulatory authority, and identification of affected parties.
        Key factors are notice documentation, regulatory authority, and party identification.
        Burden holder is regulatory authority, responsible for proper notification.
        Adversary position may be affected parties.
        Counter arguments focus on procedural error or lack of notice.
        Resolution strategy involves legal review and party communication.
        Confidence is high when notice is recorded.
        """,
        key_factors=["notice documentation", "regulatory authority", "party identification"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Regulatory Authority",
        adversary_position="Affected party",
        counter_arguments=["Procedural error", "Lack of notice"],
        resolution_strategy="Legal review and party communication.",
        entity_scope="All entities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.8"
    ),
    DoctrineBlock(
        topic="Regulatory Compliance Warning",
        keywords=["regulatory", "compliance", "warning", "filing", "enforcement"],
        conclusion_template="Regulatory compliance warning issued for {entity} on {date}.",
        reasoning_framework="""
        Regulatory compliance warning is based on monitoring enforcement actions and compliance records.
        The framework includes review of warning documents, validation of regulatory authority, and identification of affected parties.
        Key factors are warning documentation, regulatory authority, and compliance status.
        Burden holder is regulated entity, responsible for compliance.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural error or compliance effort.
        Resolution strategy involves corrective action and regulatory review.
        Confidence is high when warning is documented.
        """,
        key_factors=["warning documentation", "regulatory authority", "compliance status"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Regulated Entity",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Compliance effort"],
        resolution_strategy="Corrective action and regulatory review.",
        entity_scope="All regulated entities",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.8"
    ),
    DoctrineBlock(
        topic="Regulatory Enforcement Action",
        keywords=["regulatory", "enforcement", "action", "compliance", "violation"],
        conclusion_template="Regulatory enforcement action detected for {entity} on {date}.",
        reasoning_framework="""
        Regulatory enforcement action detection is based on monitoring enforcement actions and compliance records.
        The framework includes review of enforcement documents, validation of regulatory authority, and identification of affected parties.
        Key factors are enforcement documentation, regulatory authority, and compliance status.
        Burden holder is regulated entity, responsible for compliance.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural error or compliance effort.
        Resolution strategy involves corrective action and regulatory review.
        Confidence is high when enforcement is documented.
        """,
        key_factors=["enforcement documentation", "regulatory authority", "compliance status"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Regulated Entity",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Compliance effort"],
        resolution_strategy="Corrective action and regulatory review.",
        entity_scope="All regulated entities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.8"
    ),
    DoctrineBlock(
        topic="Regulatory Approval Detection",
        keywords=["regulatory", "approval", "permit", "filing", "compliance"],
        conclusion_template="Regulatory approval detected for {entity} on {date}.",
        reasoning_framework="""
        Regulatory approval detection is based on monitoring permit filings and approval records.
        The framework includes review of approval documents, validation of regulatory authority, and identification of affected parties.
        Key factors are approval documentation, regulatory authority, and party identification.
        Burden holder is applicant, responsible for compliance.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural error or regulatory deficiency.
        Resolution strategy involves legal review and regulatory confirmation.
        Confidence is high when approval is documented.
        """,
        key_factors=["approval documentation", "regulatory authority", "party identification"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Applicant",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Regulatory deficiency"],
        resolution_strategy="Legal review and regulatory confirmation.",
        entity_scope="All regulated entities",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.5"
    ),
    DoctrineBlock(
        topic="Regulatory Denial Detection",
        keywords=["regulatory", "denial", "permit", "filing", "compliance"],
        conclusion_template="Regulatory denial detected for {entity} on {date}.",
        reasoning_framework="""
        Regulatory denial detection is based on monitoring permit filings and denial records.
        The framework includes review of denial documents, validation of regulatory authority, and identification of affected parties.
        Key factors are denial documentation, regulatory authority, and party identification.
        Burden holder is applicant, responsible for compliance.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural error or regulatory deficiency.
        Resolution strategy involves legal review and regulatory confirmation.
        Confidence is high when denial is documented.
        """,
        key_factors=["denial documentation", "regulatory authority", "party identification"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Applicant",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Regulatory deficiency"],
        resolution_strategy="Legal review and regulatory confirmation.",
        entity_scope="All regulated entities",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.5"
    ),
    DoctrineBlock(
        topic="Regulatory Appeal Detection",
        keywords=["regulatory", "appeal", "permit", "filing", "compliance"],
        conclusion_template="Regulatory appeal detected for {entity} on {date}.",
        reasoning_framework="""
        Regulatory appeal detection is based on monitoring permit filings and appeal records.
        The framework includes review of appeal documents, validation of regulatory authority, and identification of affected parties.
        Key factors are appeal documentation, regulatory authority, and party identification.
        Burden holder is applicant, responsible for compliance.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural error or regulatory deficiency.
        Resolution strategy involves legal review and regulatory confirmation.
        Confidence is high when appeal is documented.
        """,
        key_factors=["appeal documentation", "regulatory authority", "party identification"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Applicant",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Regulatory deficiency"],
        resolution_strategy="Legal review and regulatory confirmation.",
        entity_scope="All regulated entities",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.5"
    ),
    DoctrineBlock(
        topic="Regulatory Hearing Detection",
        keywords=["regulatory", "hearing", "permit", "filing", "compliance"],
        conclusion_template="Regulatory hearing detected for {entity} on {date}.",
        reasoning_framework="""
        Regulatory hearing detection is based on monitoring permit filings and hearing records.
        The framework includes review of hearing documents, validation of regulatory authority, and identification of affected parties.
        Key factors are hearing documentation, regulatory authority, and party identification.
        Burden holder is applicant, responsible for compliance.
        Adversary position is regulatory authority.
        Counter arguments focus on procedural error or regulatory deficiency.
        Resolution strategy involves legal review and regulatory confirmation.
        Confidence is high when hearing is documented.
        """,
        key_factors=["hearing documentation", "regulatory authority", "party identification"],
        primary_authority=["Texas Railroad Commission", "Texas Administrative Code"],
        burden_holder="Applicant",
        adversary_position="Regulatory authority",
        counter_arguments=["Procedural error", "Regulatory deficiency"],
        resolution_strategy="Legal review and regulatory confirmation.",
        entity_scope="All regulated entities",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="16 TAC §3.5"
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