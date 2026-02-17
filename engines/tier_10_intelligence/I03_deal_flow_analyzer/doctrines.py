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
        topic="Unleased Mineral Identification",
        keywords=["unleased minerals", "ownership", "lease status", "mineral rights", "title analysis"],
        conclusion_template="Unleased mineral interests identified in the subject tract are held by {owner} and are not currently subject to a valid oil and gas lease.",
        reasoning_framework=(
            "1. Review county records for mineral ownership and lease status.\n"
            "2. Identify gaps in leasehold coverage and verify mineral ownership via chain-of-title.\n"
            "3. Cross-reference lease expiration dates, depth severances, and partial assignments.\n"
            "4. Confirm that no active lease encumbers the mineral interest.\n"
            "5. Assess potential for open acreage and verify against operator maps.\n"
            "6. Evaluate the impact of prior production and shut-in clauses.\n"
            "7. Consider statutory requirements for lease validity (e.g., Texas Property Code).\n"
            "8. Document findings and provide actionable recommendations for acquisition or leasing."
        ),
        key_factors=[
            "Current lease status",
            "Mineral ownership chain",
            "Lease expiration and holdover",
            "Depth severances",
            "Production history",
            "County records accuracy"
        ],
        primary_authority=[
            "Texas Property Code",
            "County Clerk Records",
            "Texas Railroad Commission",
            "Texas Supreme Court: Natural Gas Pipeline Co. v. Pool"
        ],
        burden_holder="Mineral interest owner",
        adversary_position="Lessee may claim holdover or extension rights",
        counter_arguments=[
            "Lessee claims continuous operations",
            "Production in paying quantities",
            "Shut-in royalty payments"
        ],
        resolution_strategy="Conduct thorough title and leasehold review; obtain affidavits of non-production; negotiate with lessee if ambiguity exists.",
        entity_scope="Mineral owners, operators, landmen",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 200 (Tex. 2003)"
    ),
    DoctrineBlock(
        topic="Dormant Mineral Act (Texas NRC Ch. 75) Application",
        keywords=["dormant minerals", "non-use", "surface owner", "mineral interest", "Texas Natural Resources Code Chapter 75"],
        conclusion_template="Mineral interests deemed dormant under Texas NRC Ch. 75 may be subject to reversion to surface owners if statutory requirements are met.",
        reasoning_framework=(
            "1. Identify mineral interests with no production or development for statutory period (20 years).\n"
            "2. Verify lack of mineral activity via RRC and county records.\n"
            "3. Determine if surface owner has filed notice of intent to claim dormant minerals.\n"
            "4. Assess compliance with Texas NRC Ch. 75 notice and publication requirements.\n"
            "5. Evaluate mineral owner's response or evidence of activity.\n"
            "6. Analyze potential for reversion and impact on title.\n"
            "7. Document findings and recommend actions for acquisition or contesting reversion."
        ),
        key_factors=[
            "Duration of non-use",
            "Notice filing by surface owner",
            "Mineral owner's response",
            "Production history",
            "Compliance with statutory requirements"
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 75",
            "Texas Supreme Court: Moser v. United States Steel Corp.",
            "County Clerk Records"
        ],
        burden_holder="Surface owner seeking reversion",
        adversary_position="Mineral owner claims activity or contests dormancy",
        counter_arguments=[
            "Mineral owner demonstrates recent activity",
            "Production or development within statutory period",
            "Failure to comply with notice requirements"
        ],
        resolution_strategy="Review statutory compliance; negotiate with mineral owner; pursue quiet title action if necessary.",
        entity_scope="Surface owners, mineral owners, landmen, title attorneys",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Moser v. United States Steel Corp., 676 S.W.2d 99 (Tex. 1984)"
    ),
    DoctrineBlock(
        topic="Heirship Opportunity Scoring",
        keywords=["heirship", "probate", "mineral interests", "intestate succession", "opportunity scoring"],
        conclusion_template="Heirship analysis reveals opportunities for acquisition due to fragmented ownership and lack of probate.",
        reasoning_framework=(
            "1. Identify mineral interests held by deceased owners without probate.\n"
            "2. Map family tree and determine heirs under Texas intestate succession laws.\n"
            "3. Assess likelihood of heirs' willingness to sell or lease.\n"
            "4. Evaluate title defects and marketability issues.\n"
            "5. Score opportunities based on number of heirs, degree of fragmentation, and legal complexity.\n"
            "6. Recommend acquisition strategies tailored to heirship scenarios."
        ),
        key_factors=[
            "Probate status",
            "Number of heirs",
            "Degree of ownership fragmentation",
            "Intestate succession laws",
            "Title defect risk"
        ],
        primary_authority=[
            "Texas Estates Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to establish clear title",
        adversary_position="Heirs may contest sale or refuse to cooperate",
        counter_arguments=[
            "Heirs dispute ownership",
            "Unresolved probate proceedings",
            "Competing claims"
        ],
        resolution_strategy="Conduct heirship affidavits; negotiate with heirs; pursue court approval if necessary.",
        entity_scope="Landmen, mineral buyers, title attorneys",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Texas Estates Code §201.001"
    ),
    DoctrineBlock(
        topic="Title Defect Acquisition Strategy",
        keywords=["title defects", "acquisition", "curative", "mineral interests", "marketability"],
        conclusion_template="Acquisition of mineral interests with title defects requires tailored curative measures to ensure marketability.",
        reasoning_framework=(
            "1. Identify and categorize title defects (e.g., missing links, ambiguous conveyances, unreleased liens).\n"
            "2. Assess impact of defects on mineral interest marketability.\n"
            "3. Develop curative strategies: affidavits, corrective deeds, quiet title actions.\n"
            "4. Evaluate risk tolerance and acquisition pricing.\n"
            "5. Negotiate with sellers regarding defect resolution.\n"
            "6. Document curative actions and monitor for future defects."
        ),
        key_factors=[
            "Nature and severity of defect",
            "Curative options",
            "Marketability standards",
            "Risk tolerance",
            "Seller cooperation"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Title Standards",
            "Texas Supreme Court: Reeder v. Wood County Energy"
        ],
        burden_holder="Acquirer seeking clear title",
        adversary_position="Seller may resist curative actions or dispute defect characterization",
        counter_arguments=[
            "Seller claims defect is immaterial",
            "Defect cured by operation of law",
            "Marketable title act applies"
        ],
        resolution_strategy="Negotiate curative actions; obtain title insurance; pursue legal remedies if necessary.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Reeder v. Wood County Energy, 395 S.W.3d 789 (Tex. 2012)"
    ),
    DoctrineBlock(
        topic="Mineral Interest Fragmentation Analysis",
        keywords=["fragmentation", "mineral interests", "ownership", "partition", "consolidation"],
        conclusion_template="Fragmented mineral interests present acquisition and leasing challenges; consolidation strategies are recommended.",
        reasoning_framework=(
            "1. Analyze ownership records to determine degree of fragmentation.\n"
            "2. Identify co-owners and their respective interests.\n"
            "3. Assess impact on leasing, development, and marketability.\n"
            "4. Evaluate partition options (voluntary, judicial).\n"
            "5. Recommend consolidation strategies (buyouts, exchanges, pooling).\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Number of owners",
            "Size of individual interests",
            "Partition feasibility",
            "Leasing challenges",
            "Consolidation incentives"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Partition Statutes",
            "Texas Supreme Court: Natural Gas Pipeline Co. v. Pool"
        ],
        burden_holder="Acquirer seeking to consolidate interests",
        adversary_position="Co-owners may resist partition or consolidation",
        counter_arguments=[
            "Co-owners prefer status quo",
            "Partition may reduce value",
            "Legal complexity"
        ],
        resolution_strategy="Negotiate buyouts; pursue partition actions; utilize pooling agreements.",
        entity_scope="Mineral owners, operators, landmen",
        confidence=0.81,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 200 (Tex. 2003)"
    ),
    DoctrineBlock(
        topic="Estate Planning Gaps and Mineral Acquisition",
        keywords=["estate planning", "gaps", "mineral acquisition", "probate", "succession"],
        conclusion_template="Estate planning gaps create acquisition opportunities for mineral interests due to unclear succession.",
        reasoning_framework=(
            "1. Identify mineral interests held by deceased owners with incomplete estate planning.\n"
            "2. Assess impact of lack of wills, trusts, or probate proceedings.\n"
            "3. Map potential heirs and analyze succession under Texas law.\n"
            "4. Evaluate risk of competing claims and title defects.\n"
            "5. Recommend acquisition strategies: heirship affidavits, court approval, curative actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Estate planning completeness",
            "Probate status",
            "Heir identification",
            "Title defect risk",
            "Acquisition feasibility"
        ],
        primary_authority=[
            "Texas Estates Code",
            "Texas Property Code",
            "Texas Supreme Court: Moser v. United States Steel Corp."
        ],
        burden_holder="Acquirer seeking clear title",
        adversary_position="Heirs may contest acquisition or claim ownership",
        counter_arguments=[
            "Heirs dispute succession",
            "Unresolved probate",
            "Competing claims"
        ],
        resolution_strategy="Conduct heirship affidavits; negotiate with heirs; pursue court approval if necessary.",
        entity_scope="Landmen, mineral buyers, title attorneys",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Texas Estates Code §201.001"
    ),
    DoctrineBlock(
        topic="Tax Delinquent Mineral Interest Acquisition",
        keywords=["tax delinquency", "mineral interests", "acquisition", "foreclosure", "tax sale"],
        conclusion_template="Mineral interests subject to tax delinquency may be acquired via foreclosure or tax sale, subject to statutory requirements.",
        reasoning_framework=(
            "1. Identify mineral interests with delinquent taxes via county tax records.\n"
            "2. Assess foreclosure status and eligibility for tax sale.\n"
            "3. Evaluate statutory requirements for notice, redemption, and sale procedures.\n"
            "4. Analyze risks of title defects and competing claims post-sale.\n"
            "5. Recommend acquisition strategies: bid at tax sale, negotiate with owner, pursue curative actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Tax delinquency status",
            "Foreclosure eligibility",
            "Notice and redemption requirements",
            "Title defect risk",
            "Acquisition feasibility"
        ],
        primary_authority=[
            "Texas Tax Code",
            "County Tax Assessor Records",
            "Texas Supreme Court: City of Dallas v. Stewart"
        ],
        burden_holder="Acquirer seeking to purchase at tax sale",
        adversary_position="Owner may redeem or contest sale",
        counter_arguments=[
            "Owner redeems property",
            "Sale invalid due to notice defects",
            "Competing claims post-sale"
        ],
        resolution_strategy="Verify statutory compliance; obtain title insurance; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="City of Dallas v. Stewart, 361 S.W.3d 562 (Tex. 2012)"
    ),
    DoctrineBlock(
        topic="Forced Pooling Opportunities",
        keywords=["forced pooling", "mineral interests", "Texas Railroad Commission", "unitization", "acquisition"],
        conclusion_template="Forced pooling under Texas law creates acquisition opportunities for unleased mineral interests within a unit.",
        reasoning_framework=(
            "1. Identify unleased mineral interests within proposed unit boundaries.\n"
            "2. Assess eligibility for forced pooling under Texas RRC regulations.\n"
            "3. Evaluate notice and hearing requirements.\n"
            "4. Analyze impact on acquisition strategy and compensation for unleased owners.\n"
            "5. Recommend negotiation or participation options for unleased owners.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Unleased mineral status",
            "Unit boundary determination",
            "RRC pooling eligibility",
            "Notice and hearing compliance",
            "Compensation structure"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "Texas Railroad Commission Rules",
            "Texas Supreme Court: Browning Oil Co. v. Luecke"
        ],
        burden_holder="Operator seeking to pool unleased interests",
        adversary_position="Unleased owner may contest pooling or compensation",
        counter_arguments=[
            "Owner objects to pooling",
            "Disputes compensation",
            "Challenges unit boundaries"
        ],
        resolution_strategy="Comply with RRC procedures; negotiate with owners; pursue legal remedies if necessary.",
        entity_scope="Operators, mineral owners, landmen",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Browning Oil Co. v. Luecke, 38 S.W.3d 193 (Tex. App.—Austin 2001)"
    ),
    DoctrineBlock(
        topic="Farmout Opportunity Identification",
        keywords=["farmout", "opportunity", "mineral interests", "leasehold", "exploration", "development"],
        conclusion_template="Farmout opportunities arise where leasehold owners seek to transfer exploration rights in exchange for drilling or development obligations.",
        reasoning_framework=(
            "1. Identify leasehold owners with undeveloped acreage.\n"
            "2. Assess willingness to enter farmout agreements.\n"
            "3. Evaluate terms: drilling obligations, earning acreage, assignment structure.\n"
            "4. Analyze impact on mineral interest acquisition and development.\n"
            "5. Recommend negotiation strategies and risk mitigation.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Leasehold ownership",
            "Acreage status",
            "Drilling obligations",
            "Assignment terms",
            "Development incentives"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "Texas Supreme Court: Amoco Production Co. v. Alexander",
            "Industry custom"
        ],
        burden_holder="Farmout party seeking to earn acreage",
        adversary_position="Leasehold owner may impose restrictive terms or refuse assignment",
        counter_arguments=[
            "Owner imposes restrictive terms",
            "Disputes earning criteria",
            "Challenges assignment structure"
        ],
        resolution_strategy="Negotiate favorable farmout terms; document obligations; pursue legal remedies if necessary.",
        entity_scope="Operators, mineral buyers, landmen",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Amoco Production Co. v. Alexander, 622 S.W.2d 563 (Tex. 1981)"
    ),
    DoctrineBlock(
        topic="JV Partner Matching for Acquisition",
        keywords=["joint venture", "JV", "partner matching", "acquisition", "mineral interests", "collaboration"],
        conclusion_template="JV partner matching facilitates mineral interest acquisition by pooling resources and expertise.",
        reasoning_framework=(
            "1. Identify acquisition targets requiring significant capital or expertise.\n"
            "2. Assess potential JV partners based on financial strength, technical capability, and strategic alignment.\n"
            "3. Evaluate JV structure: equity split, operator designation, governance.\n"
            "4. Analyze impact on acquisition strategy and risk allocation.\n"
            "5. Recommend negotiation strategies and documentation requirements.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Acquisition target profile",
            "Partner financial strength",
            "Technical capability",
            "JV structure",
            "Risk allocation"
        ],
        primary_authority=[
            "Texas Business Organizations Code",
            "Texas Supreme Court: Texaco, Inc. v. Pennzoil Co.",
            "Industry custom"
        ],
        burden_holder="JV partners seeking to acquire interests",
        adversary_position="Partners may dispute terms or governance",
        counter_arguments=[
            "Disputes over equity split",
            "Operator designation challenges",
            "Governance disagreements"
        ],
        resolution_strategy="Negotiate clear JV terms; document agreements; pursue dispute resolution mechanisms.",
        entity_scope="Operators, mineral buyers, investors",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Texaco, Inc. v. Pennzoil Co., 729 S.W.2d 768 (Tex. App.—Houston [1st Dist.] 1987)"
    ),
    DoctrineBlock(
        topic="Lease Expiration and Reversion Analysis",
        keywords=["lease expiration", "reversion", "mineral interests", "leasehold", "production"],
        conclusion_template="Mineral interests revert to owners upon lease expiration absent production or continuous operations.",
        reasoning_framework=(
            "1. Review lease terms for expiration and reversion clauses.\n"
            "2. Assess production status and continuous operations.\n"
            "3. Verify compliance with shut-in royalty provisions.\n"
            "4. Analyze impact of lease expiration on mineral interest acquisition.\n"
            "5. Document findings and recommend acquisition strategies."
        ),
        key_factors=[
            "Lease expiration date",
            "Production status",
            "Continuous operations",
            "Shut-in royalty compliance",
            "Reversion clauses"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Supreme Court: Natural Gas Pipeline Co. v. Pool",
            "County Clerk Records"
        ],
        burden_holder="Mineral owner seeking reversion",
        adversary_position="Lessee may claim extension or holdover rights",
        counter_arguments=[
            "Lessee claims continuous operations",
            "Production in paying quantities",
            "Shut-in royalty payments"
        ],
        resolution_strategy="Conduct leasehold review; obtain affidavits of non-production; negotiate with lessee if ambiguity exists.",
        entity_scope="Mineral owners, operators, landmen",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 200 (Tex. 2003)"
    ),
    DoctrineBlock(
        topic="Depth Severance and Acquisition Implications",
        keywords=["depth severance", "mineral interests", "acquisition", "leasehold", "ownership"],
        conclusion_template="Depth severances impact mineral interest acquisition by limiting ownership and leasehold rights to specified formations.",
        reasoning_framework=(
            "1. Identify depth severance clauses in deeds and leases.\n"
            "2. Map ownership by depth and formation.\n"
            "3. Assess impact on acquisition strategy and leasehold coverage.\n"
            "4. Evaluate potential for conflict between owners of different depths.\n"
            "5. Recommend acquisition strategies tailored to severed interests.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Depth severance clauses",
            "Ownership mapping",
            "Leasehold coverage",
            "Formation boundaries",
            "Conflict potential"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Supreme Court: Moser v. United States Steel Corp.",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to purchase severed interests",
        adversary_position="Owners of other depths may contest acquisition or leasehold rights",
        counter_arguments=[
            "Disputes over formation boundaries",
            "Challenges to severance validity",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough title review; negotiate with all owners; document severance boundaries.",
        entity_scope="Mineral buyers, operators, landmen",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Moser v. United States Steel Corp., 676 S.W.2d 99 (Tex. 1984)"
    ),
    DoctrineBlock(
        topic="Royalty Interest Acquisition and Verification",
        keywords=["royalty interest", "acquisition", "verification", "mineral interests", "leasehold"],
        conclusion_template="Acquisition of royalty interests requires verification of payment history, ownership, and lease terms.",
        reasoning_framework=(
            "1. Identify royalty interests and verify ownership via county records.\n"
            "2. Review lease terms for royalty provisions and payment obligations.\n"
            "3. Assess payment history and compliance with lease terms.\n"
            "4. Evaluate risk of title defects and competing claims.\n"
            "5. Recommend acquisition strategies and curative actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Royalty ownership",
            "Lease terms",
            "Payment history",
            "Title defect risk",
            "Acquisition feasibility"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Supreme Court: Hitz v. Texas Oil & Gas Corp.",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to purchase royalty interests",
        adversary_position="Owner may dispute payment history or title",
        counter_arguments=[
            "Disputes over payment history",
            "Challenges to ownership",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough title and payment review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hitz v. Texas Oil & Gas Corp., 522 S.W.2d 336 (Tex. Civ. App.—Dallas 1975)"
    ),
    DoctrineBlock(
        topic="Overriding Royalty Interest (ORRI) Acquisition",
        keywords=["overriding royalty", "ORRI", "acquisition", "leasehold", "verification"],
        conclusion_template="Acquisition of ORRIs requires verification of creation, assignment, and leasehold status.",
        reasoning_framework=(
            "1. Identify ORRI creation and assignment documents.\n"
            "2. Review leasehold status and expiration dates.\n"
            "3. Assess impact of lease expiration on ORRI validity.\n"
            "4. Evaluate risk of title defects and competing claims.\n"
            "5. Recommend acquisition strategies and curative actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "ORRI creation documents",
            "Assignment history",
            "Leasehold status",
            "Expiration dates",
            "Title defect risk"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Supreme Court: Hitz v. Texas Oil & Gas Corp.",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to purchase ORRIs",
        adversary_position="Owner may dispute assignment or leasehold status",
        counter_arguments=[
            "Disputes over assignment",
            "Lease expiration impacts ORRI",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough title and assignment review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hitz v. Texas Oil & Gas Corp., 522 S.W.2d 336 (Tex. Civ. App.—Dallas 1975)"
    ),
    DoctrineBlock(
        topic="Non-Participating Royalty Interest (NPRI) Acquisition",
        keywords=["NPRI", "non-participating royalty", "acquisition", "verification", "mineral interests"],
        conclusion_template="Acquisition of NPRIs requires verification of creation, ownership, and leasehold status.",
        reasoning_framework=(
            "1. Identify NPRI creation and ownership documents.\n"
            "2. Review leasehold status and expiration dates.\n"
            "3. Assess impact of lease expiration on NPRI validity.\n"
            "4. Evaluate risk of title defects and competing claims.\n"
            "5. Recommend acquisition strategies and curative actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "NPRI creation documents",
            "Ownership history",
            "Leasehold status",
            "Expiration dates",
            "Title defect risk"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Supreme Court: Hitz v. Texas Oil & Gas Corp.",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to purchase NPRIs",
        adversary_position="Owner may dispute ownership or leasehold status",
        counter_arguments=[
            "Disputes over ownership",
            "Lease expiration impacts NPRI",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough title and ownership review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Hitz v. Texas Oil & Gas Corp., 522 S.W.2d 336 (Tex. Civ. App.—Dallas 1975)"
    ),
    DoctrineBlock(
        topic="Executive Rights Acquisition and Analysis",
        keywords=["executive rights", "acquisition", "mineral interests", "lease negotiation", "ownership"],
        conclusion_template="Acquisition of executive rights enables control over lease negotiation and mineral development.",
        reasoning_framework=(
            "1. Identify executive rights holders via county records.\n"
            "2. Review deeds and assignments for executive rights provisions.\n"
            "3. Assess impact on lease negotiation and mineral development.\n"
            "4. Evaluate risk of title defects and competing claims.\n"
            "5. Recommend acquisition strategies and curative actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Executive rights ownership",
            "Deed provisions",
            "Lease negotiation control",
            "Title defect risk",
            "Acquisition feasibility"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Supreme Court: Lesley v. Lesley",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to purchase executive rights",
        adversary_position="Owner may dispute executive rights or lease negotiation authority",
        counter_arguments=[
            "Disputes over executive rights",
            "Challenges to deed provisions",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough title and deed review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Lesley v. Lesley, 957 S.W.2d 902 (Tex. App.—Texarkana 1997)"
    ),
    DoctrineBlock(
        topic="Surface Use and Mineral Acquisition Conflicts",
        keywords=["surface use", "mineral acquisition", "conflicts", "surface owner", "mineral owner"],
        conclusion_template="Conflicts between surface and mineral owners impact acquisition strategies and require negotiation or legal resolution.",
        reasoning_framework=(
            "1. Identify surface and mineral ownership via county records.\n"
            "2. Review deeds and leases for surface use provisions.\n"
            "3. Assess impact of surface use conflicts on acquisition strategy.\n"
            "4. Evaluate risk of legal disputes and title defects.\n"
            "5. Recommend negotiation or legal resolution strategies.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Surface and mineral ownership",
            "Surface use provisions",
            "Conflict potential",
            "Legal dispute risk",
            "Acquisition feasibility"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Supreme Court: Getty Oil Co. v. Jones",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to resolve surface use conflicts",
        adversary_position="Surface owner may resist mineral development",
        counter_arguments=[
            "Surface owner objects to use",
            "Disputes over deed provisions",
            "Legal challenges"
        ],
        resolution_strategy="Negotiate surface use agreements; pursue legal remedies if necessary.",
        entity_scope="Mineral buyers, operators, landmen",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Getty Oil Co. v. Jones, 470 S.W.2d 618 (Tex. 1971)"
    ),
    DoctrineBlock(
        topic="Pooling Agreement Verification and Acquisition",
        keywords=["pooling agreement", "verification", "acquisition", "mineral interests", "unitization"],
        conclusion_template="Verification of pooling agreements is essential for acquisition of mineral interests within units.",
        reasoning_framework=(
            "1. Identify pooling agreements via county records and operator files.\n"
            "2. Review agreement terms for unit boundaries, royalty allocation, and participation.\n"
            "3. Assess impact on acquisition strategy and mineral interest coverage.\n"
            "4. Evaluate risk of title defects and competing claims.\n"
            "5. Recommend acquisition strategies and curative actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Pooling agreement terms",
            "Unit boundaries",
            "Royalty allocation",
            "Participation provisions",
            "Title defect risk"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "Texas Supreme Court: Browning Oil Co. v. Luecke",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to purchase interests within units",
        adversary_position="Owner may dispute pooling agreement terms or participation",
        counter_arguments=[
            "Disputes over unit boundaries",
            "Challenges to royalty allocation",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough agreement review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, operators, landmen",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Browning Oil Co. v. Luecke, 38 S.W.3d 193 (Tex. App.—Austin 2001)"
    ),
    DoctrineBlock(
        topic="Unitization and Enhanced Recovery Acquisition",
        keywords=["unitization", "enhanced recovery", "acquisition", "mineral interests", "Texas Railroad Commission"],
        conclusion_template="Unitization for enhanced recovery creates acquisition opportunities and requires compliance with RRC regulations.",
        reasoning_framework=(
            "1. Identify unitization proposals and enhanced recovery projects.\n"
            "2. Assess eligibility for unitization under Texas RRC regulations.\n"
            "3. Review agreement terms for participation and royalty allocation.\n"
            "4. Evaluate impact on acquisition strategy and mineral interest coverage.\n"
            "5. Recommend negotiation strategies and compliance actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Unitization eligibility",
            "Enhanced recovery project status",
            "Agreement terms",
            "Royalty allocation",
            "RRC compliance"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "Texas Railroad Commission Rules",
            "Texas Supreme Court: Browning Oil Co. v. Luecke"
        ],
        burden_holder="Operator seeking to unitize interests",
        adversary_position="Owner may dispute unitization or participation terms",
        counter_arguments=[
            "Owner objects to unitization",
            "Disputes over royalty allocation",
            "Challenges to project status"
        ],
        resolution_strategy="Comply with RRC procedures; negotiate with owners; pursue legal remedies if necessary.",
        entity_scope="Operators, mineral owners, landmen",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Browning Oil Co. v. Luecke, 38 S.W.3d 193 (Tex. App.—Austin 2001)"
    ),
    DoctrineBlock(
        topic="Production History and Acquisition Risk Assessment",
        keywords=["production history", "acquisition", "risk assessment", "mineral interests", "leasehold"],
        conclusion_template="Production history impacts acquisition risk and marketability of mineral interests.",
        reasoning_framework=(
            "1. Review production history via RRC and operator records.\n"
            "2. Assess impact on leasehold validity and marketability.\n"
            "3. Evaluate risk of title defects and competing claims.\n"
            "4. Recommend acquisition strategies and risk mitigation actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Production history",
            "Leasehold validity",
            "Marketability",
            "Title defect risk",
            "Acquisition feasibility"
        ],
        primary_authority=[
            "Texas Railroad Commission",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to assess risk",
        adversary_position="Owner may dispute production history or leasehold validity",
        counter_arguments=[
            "Disputes over production history",
            "Challenges to leasehold validity",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough production and title review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, operators, landmen",
        confidence=0.81,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 200 (Tex. 2003)"
    ),
    DoctrineBlock(
        topic="Affidavit of Non-Production and Acquisition",
        keywords=["affidavit of non-production", "acquisition", "mineral interests", "leasehold", "curative"],
        conclusion_template="Affidavit of non-production is a curative tool for acquisition of mineral interests with ambiguous leasehold status.",
        reasoning_framework=(
            "1. Identify mineral interests with ambiguous leasehold status.\n"
            "2. Obtain affidavits of non-production from owners or operators.\n"
            "3. Assess impact on leasehold validity and acquisition strategy.\n"
            "4. Evaluate risk of title defects and competing claims.\n"
            "5. Recommend curative actions and acquisition strategies.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Ambiguous leasehold status",
            "Affidavit validity",
            "Curative impact",
            "Title defect risk",
            "Acquisition feasibility"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Title Standards",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to cure title",
        adversary_position="Owner or lessee may dispute affidavit validity",
        counter_arguments=[
            "Disputes over affidavit validity",
            "Challenges to leasehold status",
            "Competing claims"
        ],
        resolution_strategy="Obtain valid affidavits; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.80,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Texas Title Standards §2.10"
    ),
    DoctrineBlock(
        topic="Quiet Title Action and Mineral Acquisition",
        keywords=["quiet title", "action", "mineral acquisition", "title defect", "legal remedy"],
        conclusion_template="Quiet title actions resolve title defects and facilitate mineral interest acquisition.",
        reasoning_framework=(
            "1. Identify mineral interests with unresolved title defects.\n"
            "2. Assess eligibility for quiet title action under Texas law.\n"
            "3. Evaluate risk of legal disputes and competing claims.\n"
            "4. Recommend legal remedies and acquisition strategies.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Title defect severity",
            "Quiet title eligibility",
            "Legal dispute risk",
            "Acquisition feasibility",
            "Curative impact"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Civil Practice and Remedies Code",
            "Texas Supreme Court: Reeder v. Wood County Energy"
        ],
        burden_holder="Acquirer seeking to cure title",
        adversary_position="Owner or claimant may dispute quiet title action",
        counter_arguments=[
            "Disputes over defect characterization",
            "Challenges to legal remedy",
            "Competing claims"
        ],
        resolution_strategy="Pursue quiet title action; negotiate with claimants; obtain court approval.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Reeder v. Wood County Energy, 395 S.W.3d 789 (Tex. 2012)"
    ),
    DoctrineBlock(
        topic="Probate Proceedings and Mineral Acquisition",
        keywords=["probate", "proceedings", "mineral acquisition", "succession", "title defect"],
        conclusion_template="Probate proceedings impact mineral acquisition by clarifying ownership and curing title defects.",
        reasoning_framework=(
            "1. Identify mineral interests held by deceased owners.\n"
            "2. Review probate proceedings and court orders.\n"
            "3. Assess impact on succession and title marketability.\n"
            "4. Evaluate risk of competing claims and unresolved probate.\n"
            "5. Recommend acquisition strategies and curative actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Probate status",
            "Court orders",
            "Succession clarity",
            "Title defect risk",
            "Acquisition feasibility"
        ],
        primary_authority=[
            "Texas Estates Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to cure title",
        adversary_position="Heirs or claimants may dispute probate proceedings",
        counter_arguments=[
            "Disputes over succession",
            "Challenges to court orders",
            "Competing claims"
        ],
        resolution_strategy="Review probate proceedings; negotiate with heirs; pursue court approval if necessary.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.81,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Texas Estates Code §201.001"
    ),
    DoctrineBlock(
        topic="Curative Affidavit and Mineral Acquisition",
        keywords=["curative affidavit", "mineral acquisition", "title defect", "legal remedy", "verification"],
        conclusion_template="Curative affidavits resolve minor title defects and facilitate mineral interest acquisition.",
        reasoning_framework=(
            "1. Identify minor title defects impacting mineral acquisition.\n"
            "2. Obtain curative affidavits from owners or relevant parties.\n"
            "3. Assess impact on title marketability and acquisition strategy.\n"
            "4. Evaluate risk of legal disputes and competing claims.\n"
            "5. Recommend curative actions and acquisition strategies.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Title defect severity",
            "Affidavit validity",
            "Curative impact",
            "Acquisition feasibility",
            "Legal dispute risk"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Title Standards",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to cure title",
        adversary_position="Owner or claimant may dispute affidavit validity",
        counter_arguments=[
            "Disputes over affidavit validity",
            "Challenges to curative impact",
            "Competing claims"
        ],
        resolution_strategy="Obtain valid affidavits; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.80,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Texas Title Standards §2.10"
    ),
    DoctrineBlock(
        topic="Mineral Interest Exchange and Consolidation",
        keywords=["exchange", "consolidation", "mineral interests", "acquisition", "partition"],
        conclusion_template="Exchange and consolidation of mineral interests reduce fragmentation and enhance acquisition opportunities.",
        reasoning_framework=(
            "1. Identify fragmented mineral interests and co-owners.\n"
            "2. Assess feasibility of exchange or consolidation agreements.\n"
            "3. Evaluate impact on acquisition strategy and marketability.\n"
            "4. Recommend negotiation strategies and documentation requirements.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Fragmentation degree",
            "Exchange feasibility",
            "Consolidation incentives",
            "Marketability",
            "Acquisition impact"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Partition Statutes",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to consolidate interests",
        adversary_position="Co-owners may resist exchange or consolidation",
        counter_arguments=[
            "Co-owners prefer status quo",
            "Challenges to exchange terms",
            "Legal complexity"
        ],
        resolution_strategy="Negotiate exchange agreements; pursue consolidation actions; document transactions.",
        entity_scope="Mineral owners, operators, landmen",
        confidence=0.79,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Property Code §23.001"
    ),
    DoctrineBlock(
        topic="Adverse Possession and Mineral Acquisition",
        keywords=["adverse possession", "mineral acquisition", "title defect", "legal remedy", "ownership"],
        conclusion_template="Adverse possession claims impact mineral acquisition and require verification of statutory compliance.",
        reasoning_framework=(
            "1. Identify mineral interests subject to adverse possession claims.\n"
            "2. Review statutory requirements for adverse possession under Texas law.\n"
            "3. Assess impact on title marketability and acquisition strategy.\n"
            "4. Evaluate risk of legal disputes and competing claims.\n"
            "5. Recommend verification and curative actions.\n"
            "6. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Adverse possession claim",
            "Statutory compliance",
            "Title defect risk",
            "Acquisition feasibility",
            "Legal dispute risk"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Civil Practice and Remedies Code",
            "Texas Supreme Court: Natural Gas Pipeline Co. v. Pool"
        ],
        burden_holder="Acquirer seeking to cure title",
        adversary_position="Owner or claimant may dispute adverse possession claim",
        counter_arguments=[
            "Disputes over claim validity",
            "Challenges to statutory compliance",
            "Competing claims"
        ],
        resolution_strategy="Verify statutory compliance; negotiate with claimants; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.78,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Natural Gas Pipeline Co. v. Pool, 124 S.W.3d 200 (Tex. 2003)"
    ),
    DoctrineBlock(
        topic="Marketable Title Act and Mineral Acquisition",
        keywords=["marketable title act", "mineral acquisition", "title defect", "curative", "legal remedy"],
        conclusion_template="Marketable Title Act provides curative relief for mineral acquisition by extinguishing stale claims.",
        reasoning_framework=(
            "1. Identify mineral interests impacted by stale claims or defects.\n"
            "2. Review applicability of Marketable Title Act under Texas law.\n"
            "3. Assess impact on title marketability and acquisition strategy.\n"
            "4. Recommend curative actions and acquisition strategies.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Stale claim presence",
            "Marketable Title Act applicability",
            "Curative impact",
            "Acquisition feasibility",
            "Legal dispute risk"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Title Standards",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to cure title",
        adversary_position="Owner or claimant may dispute Act applicability",
        counter_arguments=[
            "Disputes over Act applicability",
            "Challenges to curative impact",
            "Competing claims"
        ],
        resolution_strategy="Review Act applicability; obtain title insurance; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.77,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Property Code §16.024"
    ),
    DoctrineBlock(
        topic="Fractional Interest Acquisition and Management",
        keywords=["fractional interest", "acquisition", "management", "mineral interests", "ownership"],
        conclusion_template="Acquisition and management of fractional interests require strategies to minimize fragmentation and enhance marketability.",
        reasoning_framework=(
            "1. Identify fractional interests and co-owners.\n"
            "2. Assess impact of fragmentation on acquisition and management.\n"
            "3. Recommend consolidation or management strategies.\n"
            "4. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Fractional interest degree",
            "Fragmentation impact",
            "Consolidation feasibility",
            "Management strategies",
            "Marketability"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Partition Statutes",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to manage interests",
        adversary_position="Co-owners may resist consolidation or management",
        counter_arguments=[
            "Co-owners prefer status quo",
            "Challenges to management strategies",
            "Legal complexity"
        ],
        resolution_strategy="Negotiate management agreements; pursue consolidation actions; document transactions.",
        entity_scope="Mineral owners, operators, landmen",
        confidence=0.76,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Property Code §23.001"
    ),
    DoctrineBlock(
        topic="Mineral Interest Partition and Acquisition",
        keywords=["partition", "acquisition", "mineral interests", "ownership", "legal remedy"],
        conclusion_template="Partition actions facilitate acquisition of mineral interests by resolving ownership disputes and fragmentation.",
        reasoning_framework=(
            "1. Identify mineral interests subject to partition.\n"
            "2. Review statutory requirements for partition under Texas law.\n"
            "3. Assess impact on acquisition strategy and marketability.\n"
            "4. Recommend partition actions and negotiation strategies.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Partition eligibility",
            "Ownership dispute",
            "Fragmentation degree",
            "Acquisition impact",
            "Legal remedy"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Partition Statutes",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to resolve disputes",
        adversary_position="Co-owners may resist partition",
        counter_arguments=[
            "Co-owners prefer status quo",
            "Challenges to partition terms",
            "Legal complexity"
        ],
        resolution_strategy="Pursue partition actions; negotiate with co-owners; document transactions.",
        entity_scope="Mineral owners, operators, landmen",
        confidence=0.75,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Property Code §23.001"
    ),
    DoctrineBlock(
        topic="Mineral Interest Assignment Verification",
        keywords=["assignment", "verification", "mineral interests", "acquisition", "ownership"],
        conclusion_template="Verification of mineral interest assignments is essential for acquisition and title clarity.",
        reasoning_framework=(
            "1. Identify assignment documents via county records.\n"
            "2. Review assignment terms for ownership transfer and validity.\n"
            "3. Assess impact on acquisition strategy and title clarity.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Assignment document validity",
            "Ownership transfer",
            "Title clarity",
            "Acquisition impact",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Title Standards",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to verify assignments",
        adversary_position="Owner may dispute assignment validity",
        counter_arguments=[
            "Disputes over assignment terms",
            "Challenges to validity",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough assignment review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.74,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Title Standards §2.10"
    ),
    DoctrineBlock(
        topic="Mineral Interest Reservation and Acquisition",
        keywords=["reservation", "acquisition", "mineral interests", "ownership", "deed"],
        conclusion_template="Mineral interest reservations impact acquisition strategies and require verification of deed provisions.",
        reasoning_framework=(
            "1. Identify mineral interest reservations in deeds.\n"
            "2. Review reservation terms for ownership and transferability.\n"
            "3. Assess impact on acquisition strategy and title clarity.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Reservation terms",
            "Ownership impact",
            "Transferability",
            "Title clarity",
            "Acquisition strategy"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Title Standards",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to verify reservations",
        adversary_position="Owner may dispute reservation terms",
        counter_arguments=[
            "Disputes over reservation validity",
            "Challenges to transferability",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough deed review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.73,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Title Standards §2.10"
    ),
    DoctrineBlock(
        topic="Mineral Interest Purchase Agreement Verification",
        keywords=["purchase agreement", "verification", "mineral interests", "acquisition", "contract"],
        conclusion_template="Verification of mineral interest purchase agreements is essential for acquisition and legal compliance.",
        reasoning_framework=(
            "1. Identify purchase agreements via county records and seller documentation.\n"
            "2. Review agreement terms for ownership transfer, price, and closing conditions.\n"
            "3. Assess impact on acquisition strategy and legal compliance.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Agreement terms",
            "Ownership transfer",
            "Price and closing conditions",
            "Legal compliance",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Business Organizations Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to verify agreements",
        adversary_position="Seller may dispute agreement terms",
        counter_arguments=[
            "Disputes over agreement validity",
            "Challenges to closing conditions",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough agreement review; negotiate with sellers; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.72,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Business Organizations Code §21.101"
    ),
    DoctrineBlock(
        topic="Mineral Interest Option Agreement Analysis",
        keywords=["option agreement", "analysis", "mineral interests", "acquisition", "contract"],
        conclusion_template="Option agreements provide acquisition flexibility and require analysis of terms and legal compliance.",
        reasoning_framework=(
            "1. Identify option agreements via county records and seller documentation.\n"
            "2. Review agreement terms for option exercise, price, and conditions.\n"
            "3. Assess impact on acquisition strategy and legal compliance.\n"
            "4. Recommend analysis and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Option exercise terms",
            "Price and conditions",
            "Legal compliance",
            "Acquisition flexibility",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Business Organizations Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to analyze options",
        adversary_position="Seller may dispute option terms",
        counter_arguments=[
            "Disputes over option validity",
            "Challenges to exercise conditions",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough agreement review; negotiate with sellers; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.71,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Business Organizations Code §21.101"
    ),
    DoctrineBlock(
        topic="Mineral Interest Escrow Agreement Verification",
        keywords=["escrow agreement", "verification", "mineral interests", "acquisition", "closing"],
        conclusion_template="Verification of escrow agreements is essential for mineral interest acquisition and secure closing.",
        reasoning_framework=(
            "1. Identify escrow agreements via county records and closing documentation.\n"
            "2. Review agreement terms for funds transfer, ownership transfer, and closing conditions.\n"
            "3. Assess impact on acquisition strategy and security.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Escrow terms",
            "Funds transfer",
            "Ownership transfer",
            "Closing conditions",
            "Security"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Business Organizations Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to verify escrow agreements",
        adversary_position="Seller may dispute escrow terms",
        counter_arguments=[
            "Disputes over escrow validity",
            "Challenges to closing conditions",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough agreement review; negotiate with sellers; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.70,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Business Organizations Code §21.101"
    ),
    DoctrineBlock(
        topic="Mineral Interest Due Diligence and Acquisition",
        keywords=["due diligence", "acquisition", "mineral interests", "verification", "risk assessment"],
        conclusion_template="Due diligence is essential for mineral interest acquisition and risk mitigation.",
        reasoning_framework=(
            "1. Conduct comprehensive due diligence on mineral interests.\n"
            "2. Review ownership, leasehold, production history, and title defects.\n"
            "3. Assess impact on acquisition strategy and risk mitigation.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Ownership verification",
            "Leasehold review",
            "Production history",
            "Title defect risk",
            "Acquisition feasibility"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Title Standards",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to conduct due diligence",
        adversary_position="Owner may dispute due diligence findings",
        counter_arguments=[
            "Disputes over findings",
            "Challenges to verification",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough due diligence; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.69,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Title Standards §2.10"
    ),
    DoctrineBlock(
        topic="Mineral Interest Title Insurance and Acquisition",
        keywords=["title insurance", "acquisition", "mineral interests", "risk mitigation", "verification"],
        conclusion_template="Title insurance mitigates acquisition risk for mineral interests by providing coverage for defects.",
        reasoning_framework=(
            "1. Obtain title insurance for mineral interest acquisition.\n"
            "2. Review policy terms for coverage and exclusions.\n"
            "3. Assess impact on acquisition strategy and risk mitigation.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Policy coverage",
            "Exclusions",
            "Acquisition impact",
            "Risk mitigation",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Insurance Code",
            "Texas Title Standards",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to obtain title insurance",
        adversary_position="Insurer may dispute coverage or exclusions",
        counter_arguments=[
            "Disputes over coverage",
            "Challenges to exclusions",
            "Competing claims"
        ],
        resolution_strategy="Review policy terms; negotiate with insurers; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.68,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Insurance Code §2551.001"
    ),
    DoctrineBlock(
        topic="Mineral Interest Environmental Due Diligence",
        keywords=["environmental due diligence", "mineral interests", "acquisition", "risk assessment", "compliance"],
        conclusion_template="Environmental due diligence is essential for mineral interest acquisition and compliance with regulations.",
        reasoning_framework=(
            "1. Conduct environmental due diligence on mineral interests.\n"
            "2. Review compliance with environmental regulations and impact assessments.\n"
            "3. Assess impact on acquisition strategy and risk mitigation.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Regulatory compliance",
            "Impact assessments",
            "Acquisition impact",
            "Risk mitigation",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Natural Resources Code",
            "Texas Commission on Environmental Quality",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to conduct environmental due diligence",
        adversary_position="Owner may dispute findings or compliance",
        counter_arguments=[
            "Disputes over compliance",
            "Challenges to impact assessments",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough due diligence; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.67,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Natural Resources Code §91.101"
    ),
    DoctrineBlock(
        topic="Mineral Interest Bankruptcy and Acquisition",
        keywords=["bankruptcy", "acquisition", "mineral interests", "ownership", "legal remedy"],
        conclusion_template="Bankruptcy proceedings impact mineral interest acquisition and require compliance with court orders.",
        reasoning_framework=(
            "1. Identify mineral interests subject to bankruptcy proceedings.\n"
            "2. Review court orders and bankruptcy filings.\n"
            "3. Assess impact on acquisition strategy and ownership transfer.\n"
            "4. Recommend compliance and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Bankruptcy status",
            "Court orders",
            "Ownership transfer",
            "Acquisition impact",
            "Legal remedy"
        ],
        primary_authority=[
            "Federal Bankruptcy Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to comply with bankruptcy proceedings",
        adversary_position="Owner or creditor may dispute acquisition",
        counter_arguments=[
            "Disputes over court orders",
            "Challenges to ownership transfer",
            "Competing claims"
        ],
        resolution_strategy="Review bankruptcy filings; negotiate with owners and creditors; pursue court approval.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.66,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Federal Bankruptcy Code §363"
    ),
    DoctrineBlock(
        topic="Mineral Interest Litigation and Acquisition",
        keywords=["litigation", "acquisition", "mineral interests", "ownership", "legal remedy"],
        conclusion_template="Litigation impacts mineral interest acquisition and requires compliance with court orders and legal remedies.",
        reasoning_framework=(
            "1. Identify mineral interests subject to litigation.\n"
            "2. Review court orders and legal filings.\n"
            "3. Assess impact on acquisition strategy and ownership transfer.\n"
            "4. Recommend compliance and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Litigation status",
            "Court orders",
            "Ownership transfer",
            "Acquisition impact",
            "Legal remedy"
        ],
        primary_authority=[
            "Texas Civil Practice and Remedies Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to comply with litigation proceedings",
        adversary_position="Owner or claimant may dispute acquisition",
        counter_arguments=[
            "Disputes over court orders",
            "Challenges to ownership transfer",
            "Competing claims"
        ],
        resolution_strategy="Review litigation filings; negotiate with owners and claimants; pursue court approval.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.65,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Civil Practice and Remedies Code §37.004"
    ),
    DoctrineBlock(
        topic="Mineral Interest Trust and Acquisition",
        keywords=["trust", "acquisition", "mineral interests", "ownership", "succession"],
        conclusion_template="Trust arrangements impact mineral interest acquisition and require verification of trust provisions.",
        reasoning_framework=(
            "1. Identify mineral interests held in trust.\n"
            "2. Review trust provisions for ownership and transferability.\n"
            "3. Assess impact on acquisition strategy and succession.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Trust provisions",
            "Ownership impact",
            "Transferability",
            "Succession",
            "Acquisition strategy"
        ],
        primary_authority=[
            "Texas Trust Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to verify trust arrangements",
        adversary_position="Trustee or beneficiary may dispute acquisition",
        counter_arguments=[
            "Disputes over trust validity",
            "Challenges to transferability",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough trust review; negotiate with trustees and beneficiaries; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.64,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Trust Code §112.051"
    ),
    DoctrineBlock(
        topic="Mineral Interest Corporate Acquisition",
        keywords=["corporate acquisition", "mineral interests", "ownership", "business organizations", "legal compliance"],
        conclusion_template="Corporate acquisitions impact mineral interest ownership and require compliance with business organizations code.",
        reasoning_framework=(
            "1. Identify mineral interests subject to corporate acquisition.\n"
            "2. Review business organizations code and corporate filings.\n"
            "3. Assess impact on ownership transfer and acquisition strategy.\n"
            "4. Recommend compliance and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Corporate acquisition terms",
            "Ownership transfer",
            "Legal compliance",
            "Acquisition impact",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Business Organizations Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to comply with corporate acquisition",
        adversary_position="Owner or shareholder may dispute acquisition",
        counter_arguments=[
            "Disputes over acquisition terms",
            "Challenges to ownership transfer",
            "Competing claims"
        ],
        resolution_strategy="Review corporate filings; negotiate with owners and shareholders; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.63,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Business Organizations Code §21.101"
    ),
    DoctrineBlock(
        topic="Mineral Interest Partnership Acquisition",
        keywords=["partnership acquisition", "mineral interests", "ownership", "business organizations", "legal compliance"],
        conclusion_template="Partnership acquisitions impact mineral interest ownership and require compliance with partnership agreements.",
        reasoning_framework=(
            "1. Identify mineral interests subject to partnership acquisition.\n"
            "2. Review partnership agreements and business organizations code.\n"
            "3. Assess impact on ownership transfer and acquisition strategy.\n"
            "4. Recommend compliance and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Partnership agreement terms",
            "Ownership transfer",
            "Legal compliance",
            "Acquisition impact",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Business Organizations Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to comply with partnership acquisition",
        adversary_position="Partner may dispute acquisition terms",
        counter_arguments=[
            "Disputes over partnership terms",
            "Challenges to ownership transfer",
            "Competing claims"
        ],
        resolution_strategy="Review partnership agreements; negotiate with partners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.62,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Business Organizations Code §152.002"
    ),
    DoctrineBlock(
        topic="Mineral Interest LLC Acquisition",
        keywords=["LLC acquisition", "mineral interests", "ownership", "business organizations", "legal compliance"],
        conclusion_template="LLC acquisitions impact mineral interest ownership and require compliance with operating agreements.",
        reasoning_framework=(
            "1. Identify mineral interests subject to LLC acquisition.\n"
            "2. Review operating agreements and business organizations code.\n"
            "3. Assess impact on ownership transfer and acquisition strategy.\n"
            "4. Recommend compliance and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Operating agreement terms",
            "Ownership transfer",
            "Legal compliance",
            "Acquisition impact",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Business Organizations Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to comply with LLC acquisition",
        adversary_position="Member may dispute acquisition terms",
        counter_arguments=[
            "Disputes over operating agreement terms",
            "Challenges to ownership transfer",
            "Competing claims"
        ],
        resolution_strategy="Review operating agreements; negotiate with members; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.61,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Business Organizations Code §101.101"
    ),
    DoctrineBlock(
        topic="Mineral Interest Probate Avoidance Strategies",
        keywords=["probate avoidance", "mineral interests", "acquisition", "succession", "estate planning"],
        conclusion_template="Probate avoidance strategies facilitate mineral interest acquisition and succession planning.",
        reasoning_framework=(
            "1. Identify mineral interests subject to probate avoidance strategies.\n"
            "2. Review estate planning documents and succession provisions.\n"
            "3. Assess impact on acquisition strategy and title clarity.\n"
            "4. Recommend probate avoidance actions and acquisition strategies.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Estate planning completeness",
            "Succession provisions",
            "Probate avoidance impact",
            "Acquisition strategy",
            "Title clarity"
        ],
        primary_authority=[
            "Texas Estates Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to implement probate avoidance",
        adversary_position="Heirs or claimants may dispute avoidance strategies",
        counter_arguments=[
            "Disputes over estate planning",
            "Challenges to succession provisions",
            "Competing claims"
        ],
        resolution_strategy="Review estate planning documents; negotiate with heirs; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.60,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Estates Code §201.001"
    ),
    DoctrineBlock(
        topic="Mineral Interest Acquisition via Auction",
        keywords=["auction", "acquisition", "mineral interests", "ownership", "legal compliance"],
        conclusion_template="Acquisition of mineral interests via auction requires compliance with statutory requirements and verification of ownership.",
        reasoning_framework=(
            "1. Identify mineral interests available for auction.\n"
            "2. Review statutory requirements for auction and ownership transfer.\n"
            "3. Assess impact on acquisition strategy and legal compliance.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Auction terms",
            "Ownership verification",
            "Legal compliance",
            "Acquisition impact",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Business Organizations Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to purchase at auction",
        adversary_position="Owner may dispute auction terms",
        counter_arguments=[
            "Disputes over auction validity",
            "Challenges to ownership transfer",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough auction review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.59,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Property Code §51.002"
    ),
    DoctrineBlock(
        topic="Mineral Interest Acquisition via Private Sale",
        keywords=["private sale", "acquisition", "mineral interests", "ownership", "legal compliance"],
        conclusion_template="Acquisition of mineral interests via private sale requires verification of ownership and compliance with statutory requirements.",
        reasoning_framework=(
            "1. Identify mineral interests available for private sale.\n"
            "2. Review ownership and statutory requirements for transfer.\n"
            "3. Assess impact on acquisition strategy and legal compliance.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Ownership verification",
            "Sale terms",
            "Legal compliance",
            "Acquisition impact",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Business Organizations Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to purchase via private sale",
        adversary_position="Owner may dispute sale terms",
        counter_arguments=[
            "Disputes over sale validity",
            "Challenges to ownership transfer",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough sale review; negotiate with owners; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.58,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Property Code §51.002"
    ),
    DoctrineBlock(
        topic="Mineral Interest Acquisition via Gift",
        keywords=["gift", "acquisition", "mineral interests", "ownership", "succession"],
        conclusion_template="Acquisition of mineral interests via gift requires verification of ownership and compliance with statutory requirements.",
        reasoning_framework=(
            "1. Identify mineral interests subject to gift.\n"
            "2. Review gift documentation and statutory requirements for transfer.\n"
            "3. Assess impact on acquisition strategy and succession.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Gift documentation",
            "Ownership verification",
            "Succession impact",
            "Legal compliance",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Property Code",
            "Texas Estates Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to accept gift",
        adversary_position="Owner or heir may dispute gift terms",
        counter_arguments=[
            "Disputes over gift validity",
            "Challenges to ownership transfer",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough gift review; negotiate with owners and heirs; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.57,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Estates Code §201.001"
    ),
    DoctrineBlock(
        topic="Mineral Interest Acquisition via Inheritance",
        keywords=["inheritance", "acquisition", "mineral interests", "succession", "ownership"],
        conclusion_template="Acquisition of mineral interests via inheritance requires verification of succession and compliance with statutory requirements.",
        reasoning_framework=(
            "1. Identify mineral interests subject to inheritance.\n"
            "2. Review succession documentation and statutory requirements for transfer.\n"
            "3. Assess impact on acquisition strategy and title clarity.\n"
            "4. Recommend verification and curative actions.\n"
            "5. Document findings and provide actionable recommendations."
        ),
        key_factors=[
            "Succession documentation",
            "Ownership verification",
            "Title clarity",
            "Legal compliance",
            "Curative actions"
        ],
        primary_authority=[
            "Texas Estates Code",
            "Texas Property Code",
            "County Clerk Records"
        ],
        burden_holder="Acquirer seeking to inherit interests",
        adversary_position="Heirs or claimants may dispute succession",
        counter_arguments=[
            "Disputes over succession validity",
            "Challenges to ownership transfer",
            "Competing claims"
        ],
        resolution_strategy="Conduct thorough succession review; negotiate with heirs; pursue curative actions.",
        entity_scope="Mineral buyers, landmen, title attorneys",
        confidence=0.56,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Texas Estates Code §201.001"
    ),
    DoctrineBlock(
        topic="Mineral Interest Acquisition via Foreclosure",
        keywords=["foreclosure", "acquisition", "