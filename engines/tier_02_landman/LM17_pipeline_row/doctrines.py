"""
LM17 Pipeline ROW Engine - Doctrine Definitions
=================================================
Domain doctrine blocks for pipeline right-of-way acquisition,
FERC compliance, eminent domain, environmental permitting,
and landowner dispute resolution.

Engine ID: LM17 | Port: 8517
TIE Gold Standard Doctrine Cache
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================================
# ENUMS
# ============================================================================

class IssueCategory(str, Enum):
    ROW_ACQUISITION = "ROW_ACQUISITION"
    EASEMENT_NEGOTIATION = "EASEMENT_NEGOTIATION"
    FERC_COMPLIANCE = "FERC_COMPLIANCE"
    EMINENT_DOMAIN = "EMINENT_DOMAIN"
    CROSSING_PERMITS = "CROSSING_PERMITS"
    ENVIRONMENTAL_PERMITTING = "ENVIRONMENTAL_PERMITTING"
    SURFACE_DAMAGE = "SURFACE_DAMAGE"
    PIPELINE_SAFETY = "PIPELINE_SAFETY"
    ABANDONMENT = "ABANDONMENT"
    DISPUTE_RESOLUTION = "DISPUTE_RESOLUTION"
    TEMPORARY_WORKSPACE = "TEMPORARY_WORKSPACE"
    ENCROACHMENT = "ENCROACHMENT"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class BurdenHolder(str, Enum):
    PIPELINE_COMPANY = "pipeline_company"
    LANDOWNER = "landowner"
    REGULATORY_AGENCY = "regulatory_agency"
    SHARED = "shared"


# ============================================================================
# DOCTRINE BLOCK MODEL
# ============================================================================

class DoctrineBlock(BaseModel):
    """A single pre-compiled doctrine reasoning block."""
    topic: str
    category: IssueCategory
    keywords: list[str] = Field(min_length=5)
    conclusion_template: str
    reasoning_framework: str
    key_factors: list[str] = Field(min_length=4)
    primary_authority: list[str] = Field(min_length=2)
    burden_holder: BurdenHolder
    adversary_position: str
    counter_arguments: list[str] = Field(min_length=3)
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    position_zone: PositionZone = PositionZone.PLANNING
    fragility_score: float = Field(default=0.3, ge=0.0, le=1.0)
    disclosure_caveat: Optional[str] = None


# ============================================================================
# DOCTRINE CACHE - 45 BLOCKS
# ============================================================================

DOCTRINE_CACHE: list[DoctrineBlock] = [
    # ---- ROW ACQUISITION ----
    DoctrineBlock(
        topic="gathering_line_row_acquisition",
        category=IssueCategory.ROW_ACQUISITION,
        keywords=["gathering", "line", "right-of-way", "acquisition", "wellhead", "processing", "midstream"],
        conclusion_template=(
            "Gathering line ROW acquisition requires negotiation of permanent easements from wellhead or tank "
            "battery to central processing or compression facilities. Texas does not grant eminent domain to "
            "gathering systems absent common carrier or gas utility status. Voluntary negotiation and competitive "
            "compensation are the primary acquisition pathways."
        ),
        reasoning_framework=(
            "Step 1: Classify the pipeline as gathering vs transmission under FERC/state definitions. "
            "Gathering lines connect individual wells or production facilities to the first point of interstate "
            "commerce or processing plant. Step 2: Determine regulatory jurisdiction - intrastate gathering "
            "typically falls under Railroad Commission of Texas jurisdiction, not FERC. Step 3: Evaluate "
            "eminent domain eligibility. Under Texas Natural Resources Code Ch. 111, only common carrier "
            "pipelines have condemnation authority. Pure gathering systems serving a single producer generally "
            "lack this power. Step 4: Negotiate voluntary easements with landowners. Typical gathering ROW "
            "widths range from 25-50 feet permanent, with 25-75 feet additional temporary workspace during "
            "construction. Step 5: Address parallel line provisions if existing pipelines occupy adjacent ROW. "
            "Step 6: Ensure easement language covers the specific products (gas, oil, produced water, condensate) "
            "and operational activities (pigging, maintenance, cathodic protection). Step 7: Execute and record "
            "the easement instrument in the county deed records."
        ),
        key_factors=[
            "Pipeline classification (gathering vs transmission)",
            "Single-producer vs multi-producer service",
            "Common carrier status availability",
            "Landowner willingness and compensation expectations",
            "Existing ROW or utility corridor availability",
            "Environmental constraints along proposed route",
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 111",
            "Railroad Commission of Texas Statewide Rule 8",
            "FERC Policy Statement on Gathering (Docket PL92-1)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Landowner argues gathering line serves only one producer, provides no public benefit, "
            "and pipeline company should pay premium compensation for voluntary easement since no "
            "condemnation authority exists."
        ),
        counter_arguments=[
            "Gathering infrastructure enables production that generates royalty income for mineral owners",
            "Competitive gathering rates benefit all working interest owners in the area",
            "Gathering systems are essential infrastructure for resource development",
            "Industry standard compensation rates reflect fair market value",
        ],
        resolution_strategy=(
            "Negotiate voluntary easements at competitive rates. Offer above-market compensation if route "
            "options are limited. Include surface damage provisions, crop damage payments, and restoration "
            "commitments. Consider alternative routes if landowner resistance is strong."
        ),
        entity_scope="Midstream gathering companies, E&P operators, landowners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established Texas law on gathering vs common carrier distinction",
        controlling_precedent="Railroad Commission of Texas v. Lone Star Gas Co., gathering classification",
    ),

    DoctrineBlock(
        topic="transmission_pipeline_row_ferc_regulated",
        category=IssueCategory.ROW_ACQUISITION,
        keywords=["transmission", "pipeline", "interstate", "ferc", "right-of-way", "certificate", "natural gas"],
        conclusion_template=(
            "Interstate natural gas transmission pipelines regulated by FERC under the Natural Gas Act "
            "have federal eminent domain authority upon receiving a Section 7 certificate of public "
            "convenience and necessity. ROW acquisition involves both voluntary negotiation and, where "
            "necessary, condemnation proceedings in federal court."
        ),
        reasoning_framework=(
            "Step 1: Confirm FERC jurisdiction - pipeline must transport natural gas in interstate commerce "
            "or be interconnected with an interstate system. Step 2: Obtain Section 7 certificate of public "
            "convenience and necessity from FERC, which includes environmental review under NEPA. Step 3: "
            "Begin voluntary ROW acquisition through negotiation with affected landowners. FERC encourages "
            "good-faith negotiation before exercising eminent domain. Step 4: If negotiation fails, the "
            "certificate holder may file condemnation proceedings under 15 USC 717f(h) in federal district "
            "court. Step 5: Court determines just compensation based on fair market value of the easement. "
            "Step 6: Pipeline company must comply with all certificate conditions including environmental "
            "mitigation, construction specifications, and restoration requirements."
        ),
        key_factors=[
            "FERC Section 7 certificate status",
            "Interstate vs intrastate classification",
            "Environmental impact statement or assessment completion",
            "Landowner negotiation history and good-faith efforts",
            "Fair market value of easement rights",
            "Certificate conditions and mitigation requirements",
        ],
        primary_authority=[
            "Natural Gas Act, 15 USC 717 et seq.",
            "15 USC 717f(h) (eminent domain authority)",
            "18 CFR Part 157 (FERC certificate regulations)",
            "FERC Certificate Policy Statement (Docket PL99-3)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Landowner challenges necessity of taking, argues route alternatives exist that would avoid "
            "their property, and disputes fair market value determination."
        ),
        counter_arguments=[
            "FERC certificate establishes public convenience and necessity",
            "Route selection underwent extensive NEPA environmental review",
            "Federal eminent domain authority under NGA is well-established",
            "Just compensation determined by independent appraisal",
        ],
        resolution_strategy=(
            "Pursue good-faith negotiation first. Document all contact attempts and offers. If condemnation "
            "necessary, file in federal court with supporting appraisals. Seek quick-take authority where "
            "available to begin construction while compensation is litigated."
        ),
        entity_scope="Interstate pipeline companies, FERC, federal courts, landowners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Federal statutory authority with extensive case law support",
        controlling_precedent="Atlantic Coast Pipeline v. Nelson (cert granted), eminent domain under NGA",
    ),

    DoctrineBlock(
        topic="intrastate_pipeline_row_state_regulated",
        category=IssueCategory.ROW_ACQUISITION,
        keywords=["intrastate", "pipeline", "state", "regulated", "texas", "common carrier", "rrc"],
        conclusion_template=(
            "Intrastate pipelines in Texas may acquire ROW through eminent domain if they qualify as "
            "common carriers under Texas Natural Resources Code Chapter 111 or as gas utilities under "
            "Chapter 117. The Railroad Commission of Texas determines common carrier status. Condemnation "
            "proceeds in state court under Texas Property Code Chapter 21."
        ),
        reasoning_framework=(
            "Step 1: Determine pipeline common carrier or gas utility eligibility. Texas NRC 111.002 "
            "defines common carrier pipelines as those transporting crude oil, natural gas, or products "
            "for hire or as common purchasers. Step 2: File T-4 permit application with Railroad Commission "
            "establishing common carrier status. Step 3: Negotiate voluntary easements with landowners. "
            "Step 4: If negotiation fails, initiate condemnation under Texas Property Code Ch. 21. Must "
            "make bona fide offer and demonstrate inability to agree. Step 5: Special commissioners appointed "
            "to assess damages. Either party may object and demand jury trial. Step 6: Pipeline company "
            "may deposit commissioners' award and take immediate possession."
        ),
        key_factors=[
            "Common carrier or gas utility qualification",
            "T-4 permit from Railroad Commission",
            "Bona fide offer requirement before condemnation",
            "Special commissioners damage assessment",
            "State court jurisdiction for condemnation",
        ],
        primary_authority=[
            "Texas Natural Resources Code Chapter 111",
            "Texas Natural Resources Code Chapter 117",
            "Texas Property Code Chapter 21",
            "Railroad Commission of Texas T-4 Permit Requirements",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Landowner challenges common carrier status as pretextual, argues pipeline serves only one "
            "shipper and is actually a private gathering line without condemnation authority."
        ),
        counter_arguments=[
            "T-4 permit filing with RRC establishes prima facie common carrier status",
            "Pipeline offers service to all shippers on non-discriminatory basis",
            "Texas Supreme Court has upheld common carrier status where pipeline serves public interest",
        ],
        resolution_strategy=(
            "Secure T-4 permit early in project. Document common carrier status through tariff filings and "
            "open access commitments. Negotiate in good faith with above-market offers. Use condemnation "
            "only as last resort after exhausting negotiation."
        ),
        entity_scope="Intrastate pipeline operators, Railroad Commission of Texas, state courts, landowners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established Texas statutory framework with RRC oversight",
        controlling_precedent="Texas Rice Land Partners v. Denbury Green Pipeline (Tex. 2012)",
    ),

    # ---- EASEMENT NEGOTIATION ----
    DoctrineBlock(
        topic="pipeline_easement_width_depth_products",
        category=IssueCategory.EASEMENT_NEGOTIATION,
        keywords=["easement", "width", "depth", "products", "negotiation", "permanent", "pipeline"],
        conclusion_template=(
            "Pipeline easement negotiation requires precise specification of permanent ROW width (typically "
            "30-75 feet for major pipelines), minimum depth of cover (36-48 inches depending on location "
            "class), authorized products, and operational rights. Ambiguous easement language creates "
            "future encroachment and scope disputes."
        ),
        reasoning_framework=(
            "Step 1: Determine required permanent ROW width based on pipe diameter, operating pressure, "
            "and PHMSA class location requirements. Typical widths: 4-8 inch = 25-30 feet, 10-16 inch = "
            "30-50 feet, 20-36 inch = 50-75 feet. Step 2: Specify minimum depth of cover per 49 CFR 192 "
            "(natural gas) or 195 (hazardous liquids). Class 1 = 30 inches, Class 2 = 30 inches, Class 3 = "
            "36 inches, Class 4 = 36 inches for gas; 36 inches standard for liquids. Step 3: Enumerate "
            "authorized products precisely - natural gas, crude oil, refined products, NGLs, produced water, "
            "CO2. Overbroad product clauses invite future disputes. Step 4: Define operational rights including "
            "access for maintenance, pigging, cathodic protection, inspection. Step 5: Address surface use "
            "restrictions within the permanent easement - no permanent structures, tree clearance, plowing "
            "depth limitations. Step 6: Include provisions for parallel lines and future expansion."
        ),
        key_factors=[
            "Pipe diameter and operating pressure class",
            "PHMSA class location designation (1-4)",
            "Product specificity in easement language",
            "Operational access and maintenance rights",
            "Surface use restrictions within easement",
            "Parallel line and expansion provisions",
        ],
        primary_authority=[
            "49 CFR Part 192 Subpart G (General Construction for Transmission Lines)",
            "49 CFR Part 195 Subpart F (Operation and Maintenance)",
            "Texas Property Code on easement construction",
        ],
        burden_holder=BurdenHolder.SHARED,
        adversary_position=(
            "Landowner seeks narrowest possible permanent easement, maximum depth of cover, limited product "
            "authorization, and extensive surface use rights within the easement corridor."
        ),
        counter_arguments=[
            "Adequate width is essential for pipeline safety and maintenance access",
            "PHMSA regulations mandate minimum depth of cover standards",
            "Product flexibility enables efficient infrastructure utilization",
            "Surface use restrictions protect pipeline integrity and public safety",
        ],
        resolution_strategy=(
            "Negotiate reasonable permanent width with clear surveyed boundaries. Specify products with "
            "reasonable flexibility. Include maintenance and access provisions that minimize landowner "
            "disruption. Offer enhanced compensation for wider easements or additional product authority."
        ),
        entity_scope="Pipeline companies, landowners, ROW agents, surveyors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standards well-established; PHMSA regulations provide clear minimums",
        controlling_precedent="PHMSA class location requirements under 49 CFR 192.5",
    ),

    DoctrineBlock(
        topic="parallel_line_easement_provisions",
        category=IssueCategory.EASEMENT_NEGOTIATION,
        keywords=["parallel", "line", "easement", "additional", "pipeline", "corridor", "co-location"],
        conclusion_template=(
            "Parallel pipeline installation within or adjacent to existing ROW requires careful analysis "
            "of original easement terms, additional easement acquisition, interference considerations, "
            "and cumulative impact compensation. Many legacy easements do not authorize additional lines "
            "without supplemental agreements."
        ),
        reasoning_framework=(
            "Step 1: Review original easement instrument for parallel line or additional line authorization. "
            "Many legacy easements from the 1940s-1970s used broad language that may or may not authorize "
            "additional lines. Step 2: If original easement is silent on parallel lines, additional easement "
            "or amendment is required. Step 3: Assess safety setback requirements between parallel pipelines "
            "per PHMSA and API RP 1102 standards. Step 4: Evaluate cumulative impact on landowner surface use "
            "from multiple pipelines in a corridor. Step 5: Negotiate supplemental easement or amendment with "
            "additional compensation reflecting the incremental burden. Step 6: Consider whether parallel "
            "installation triggers class location change under 49 CFR 192.5."
        ),
        key_factors=[
            "Original easement language and parallel line authorization",
            "Safety setback between parallel pipelines",
            "Cumulative surface impact assessment",
            "Supplemental compensation for additional burden",
            "Class location implications of increased pipeline density",
        ],
        primary_authority=[
            "Original easement instrument terms",
            "API RP 1102 (Steel Pipelines Crossing Railroads and Highways)",
            "49 CFR 192.5 (Class Location Requirements)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Landowner argues original easement authorizes only a single pipeline and any additional line "
            "requires a new easement with full compensation at current market rates."
        ),
        counter_arguments=[
            "Some legacy easements use broad 'pipeline and appurtenances' language authorizing additional lines",
            "Co-location reduces total land disturbance compared to separate corridors",
            "Industry practice supports reasonable parallel installation within existing corridors",
        ],
        resolution_strategy=(
            "Carefully parse original easement language. If ambiguous, negotiate supplemental easement rather "
            "than litigate. Offer premium compensation for additional line authorization. Include cathodic "
            "protection interference provisions between parallel metallic pipelines."
        ),
        entity_scope="Pipeline companies, landowners, easement title examiners",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="Outcome depends heavily on specific easement language interpretation",
        controlling_precedent="Texas easement construction principles - grant construed against grantor",
        disclosure_caveat="Original easement language must be reviewed before providing definitive guidance",
    ),

    # ---- FERC COMPLIANCE ----
    DoctrineBlock(
        topic="ferc_section_7_certificate_process",
        category=IssueCategory.FERC_COMPLIANCE,
        keywords=["ferc", "section", "certificate", "convenience", "necessity", "natural gas", "interstate"],
        conclusion_template=(
            "FERC Section 7 certification under the Natural Gas Act requires demonstration that the proposed "
            "pipeline project is in the public convenience and necessity. The process involves pre-filing, "
            "formal application, environmental review under NEPA, public comment, and commission order. "
            "Certificate conditions govern construction, operation, and ROW acquisition."
        ),
        reasoning_framework=(
            "Step 1: Evaluate whether pre-filing process is appropriate. FERC encourages pre-filing for "
            "major projects to facilitate early stakeholder engagement. Step 2: Prepare and file formal "
            "application under 18 CFR 157.14 including engineering, environmental, market, and financial "
            "data. Step 3: FERC staff conducts environmental review - EA for most projects, EIS for projects "
            "with significant environmental impact. Step 4: Public comment period and intervenor participation. "
            "Step 5: FERC issues certificate order with conditions. Step 6: Applicant must comply with all "
            "certificate conditions before and during construction. Step 7: Post-construction compliance "
            "filings and in-service notification."
        ),
        key_factors=[
            "Public convenience and necessity demonstration",
            "Market demand and precedent agreements",
            "Environmental review scope (EA vs EIS)",
            "Stakeholder and landowner engagement",
            "Certificate conditions compliance",
            "Construction timeline and seasonal restrictions",
        ],
        primary_authority=[
            "Natural Gas Act Section 7, 15 USC 717f",
            "18 CFR Part 157 (Certificate Regulations)",
            "18 CFR Part 380 (NEPA Regulations)",
            "FERC Certificate Policy Statement (Docket PL99-3-000)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Intervenors challenge project need, argue demand projections are inflated, and claim "
            "environmental impacts outweigh public benefits."
        ),
        counter_arguments=[
            "Executed precedent agreements demonstrate binding market demand",
            "Environmental mitigation measures reduce impacts to acceptable levels",
            "FERC balancing test weighs economic benefits against adverse impacts",
            "No-action alternative fails to meet demonstrated market need",
        ],
        resolution_strategy=(
            "Prepare comprehensive application with strong market evidence. Engage stakeholders early through "
            "pre-filing. Propose robust environmental mitigation. Address intervenor concerns proactively. "
            "Demonstrate compliance capability for all certificate conditions."
        ),
        entity_scope="Interstate pipeline companies, FERC, intervenors, affected landowners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established FERC regulatory process with extensive precedent",
        controlling_precedent="FERC Certificate Policy Statement, Docket PL99-3-000 (1999)",
    ),

    # ---- EMINENT DOMAIN ----
    DoctrineBlock(
        topic="eminent_domain_common_carrier_texas",
        category=IssueCategory.EMINENT_DOMAIN,
        keywords=["eminent domain", "common carrier", "texas", "condemnation", "nrc", "chapter 111", "taking"],
        conclusion_template=(
            "Texas common carrier pipelines possess eminent domain authority under NRC Chapter 111 and "
            "Texas Property Code Chapter 21. Following Texas Rice Land Partners v. Denbury Green Pipeline "
            "(2012), the pipeline must demonstrate actual common carrier status through reasonable "
            "probability of serving the public, not merely filing a T-4 permit."
        ),
        reasoning_framework=(
            "Step 1: Establish common carrier status under NRC 111.002. After Denbury Green, mere T-4 "
            "filing is insufficient - must show reasonable probability of serving public as common carrier. "
            "Step 2: Make bona fide written offer to landowner under Property Code 21.0113. Must include "
            "appraisal, landowner bill of rights, and description of property to be acquired. Step 3: "
            "Allow mandatory 30-day negotiation period. Step 4: File condemnation petition in county court "
            "or district court. Step 5: Court appoints three special commissioners to assess damages. "
            "Step 6: Commissioners hearing and award. Step 7: Either party may object and demand jury trial. "
            "Step 8: Pipeline company may deposit award amount and take possession immediately."
        ),
        key_factors=[
            "Actual common carrier status (not merely T-4 filing)",
            "Reasonable probability of serving public as common carrier",
            "Bona fide offer with required disclosures",
            "30-day mandatory negotiation period",
            "Special commissioners damage assessment",
            "Right to jury trial on compensation",
        ],
        primary_authority=[
            "Texas Natural Resources Code Section 111.002",
            "Texas Property Code Chapter 21",
            "Texas Rice Land Partners v. Denbury Green Pipeline-Texas, LLC, 363 S.W.3d 192 (Tex. 2012)",
            "Texas Government Code Section 2206 (Eminent Domain Reporting)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Landowner challenges common carrier status as pretextual, argues pipeline will serve only "
            "one shipper, and demands maximum compensation including consequential damages."
        ),
        counter_arguments=[
            "Pipeline company has filed open access tariff and posts rates",
            "Multiple potential shippers have expressed interest",
            "Legislative intent supports pipeline infrastructure development",
        ],
        resolution_strategy=(
            "Document common carrier status thoroughly before initiating condemnation. Maintain evidence of "
            "open access commitment and multiple shipper interest. Make generous bona fide offer to minimize "
            "litigation risk. Prepare for commissioners hearing with qualified appraisals."
        ),
        entity_scope="Texas common carrier pipelines, landowners, state courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Post-Denbury Green framework is clear but fact-intensive",
        controlling_precedent="Texas Rice Land Partners v. Denbury Green Pipeline-Texas, LLC (Tex. 2012)",
    ),

    DoctrineBlock(
        topic="condemnation_compensation_determination",
        category=IssueCategory.EMINENT_DOMAIN,
        keywords=["condemnation", "compensation", "just", "fair market value", "damages", "appraisal", "easement"],
        conclusion_template=(
            "Just compensation in pipeline condemnation includes the fair market value of the easement rights "
            "taken plus any diminution in value to the remainder of the property. Compensation must reflect "
            "the highest and best use of the property. Both pipeline company and landowner typically present "
            "competing appraisals."
        ),
        reasoning_framework=(
            "Step 1: Determine the interest being acquired - permanent easement value based on percentage "
            "of fee simple value burdened by the easement. Step 2: Assess fair market value of the easement "
            "corridor using comparable sales approach, income approach, or before-and-after methodology. "
            "Step 3: Calculate remainder damages - diminution in value to the property not taken, including "
            "impact on farming operations, development potential, and aesthetic value. Step 4: Consider "
            "special damages - crop losses during construction, temporary workspace damages, tree removal, "
            "fence replacement. Step 5: Address potential for enhanced compensation if taking fragments the "
            "property or eliminates access. Step 6: Present appraisal evidence to commissioners or jury."
        ),
        key_factors=[
            "Fair market value of easement rights",
            "Highest and best use determination",
            "Remainder damages to balance of property",
            "Crop loss and agricultural impact",
            "Development potential impairment",
            "Property fragmentation and access issues",
        ],
        primary_authority=[
            "Texas Property Code Chapter 21",
            "State v. Carpenter, 126 S.W.3d 879 (Tex. 2004)",
            "United States v. 564.54 Acres of Land, 441 U.S. 506 (1979)",
        ],
        burden_holder=BurdenHolder.SHARED,
        adversary_position=(
            "Landowner argues highest and best use is residential or commercial development, not agricultural, "
            "and that pipeline easement permanently impairs development potential."
        ),
        counter_arguments=[
            "Highest and best use must be legally permissible, physically possible, and financially feasible",
            "Speculative future development does not establish current fair market value",
            "Pipeline easement is compatible with many surface uses including agriculture",
        ],
        resolution_strategy=(
            "Engage qualified appraisers experienced in pipeline easement valuation. Document comparable "
            "easement transactions in the area. Address remainder damages proactively. Consider offering "
            "above-appraised value to avoid litigation costs."
        ),
        entity_scope="Pipeline companies, landowners, appraisers, commissioners, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established valuation principles with case-specific application",
        controlling_precedent="State v. Carpenter (Tex. 2004) on highest and best use",
    ),

    # ---- CROSSING PERMITS ----
    DoctrineBlock(
        topic="road_creek_river_crossing_methods",
        category=IssueCategory.CROSSING_PERMITS,
        keywords=["crossing", "road", "creek", "river", "hdd", "open-cut", "bore", "directional drill", "permit"],
        conclusion_template=(
            "Pipeline crossings of roads, creeks, and rivers require crossing-method-specific permits "
            "and engineering. HDD is preferred for major waterway and highway crossings to minimize "
            "surface disturbance. Open-cut requires USACE Section 404 permit for navigable waters "
            "and state water quality certification."
        ),
        reasoning_framework=(
            "Step 1: Classify the crossing - public road, state highway, navigable waterway, non-navigable "
            "stream, drainage ditch. Step 2: Select crossing method based on depth, width, soil conditions, "
            "and environmental sensitivity. HDD for major crossings (rivers, highways, railroads); bore and "
            "jack for roads with shallow utilities; open-cut for minor drainages. Step 3: Obtain required "
            "permits - TxDOT utility permit for state highways, county road crossing permit, USACE Section "
            "404 permit for waters of the US, TCEQ 401 water quality certification. Step 4: Engineer the "
            "crossing with adequate depth of cover - minimum 5 feet below riverbed scour depth for HDD, "
            "minimum 48 inches below roadway surface. Step 5: Implement erosion control and turbidity "
            "mitigation measures. Step 6: Post-crossing restoration and monitoring."
        ),
        key_factors=[
            "Crossing classification and jurisdictional status",
            "Crossing method selection (HDD vs bore vs open-cut)",
            "Required permits (federal, state, local)",
            "Depth of cover below scour or grade",
            "Environmental protection measures",
            "Restoration and monitoring requirements",
        ],
        primary_authority=[
            "Clean Water Act Section 404 (33 USC 1344)",
            "TxDOT Utility Accommodation Rules (43 TAC Chapter 21)",
            "49 CFR 192.327 (Cover Requirements for Pipelines at Crossings)",
            "USACE Nationwide Permit 12 (Utility Line Activities)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Regulatory agency requires HDD for waterway crossing, increasing project cost significantly, "
            "or landowner objects to open-cut method through their property."
        ),
        counter_arguments=[
            "HDD minimizes environmental impact and surface disturbance",
            "Open-cut with proper BMPs meets regulatory requirements for minor crossings",
            "Bore and jack provides sealed crossing with minimal surface impact",
        ],
        resolution_strategy=(
            "Conduct geotechnical investigation early to determine feasibility of preferred crossing method. "
            "Apply for permits with alternative methods as contingency. Budget for HDD at major crossings. "
            "Engage environmental consultants for Section 404 compliance."
        ),
        entity_scope="Pipeline companies, USACE, TxDOT, county road departments, TCEQ",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Permit requirements well-defined; method selection is engineering judgment",
        controlling_precedent="USACE Nationwide Permit 12 conditions and regional conditions",
    ),

    DoctrineBlock(
        topic="railroad_crossing_permits",
        category=IssueCategory.CROSSING_PERMITS,
        keywords=["railroad", "crossing", "permit", "encroachment", "bore", "jack", "api 1102", "fra"],
        conclusion_template=(
            "Pipeline crossings of railroad rights-of-way require encroachment permits from the railroad "
            "company and compliance with API RP 1102 design standards. Crossings must be cased or designed "
            "to withstand railroad loads. Permit fees and annual rental are standard."
        ),
        reasoning_framework=(
            "Step 1: Identify railroad owner and submit crossing application. Major railroads (BNSF, UP, "
            "CPKC) have standardized permit processes. Step 2: Design crossing per API RP 1102 standards "
            "for wall thickness, depth of cover (minimum 5 feet below base of rail), and casing requirements. "
            "Step 3: Crossing method is typically bore and jack or HDD - open-cut of active rail is rarely "
            "permitted. Step 4: Pay application fee, plan review fee, and negotiate annual occupancy rental. "
            "Step 5: Comply with railroad flagging and safety requirements during construction. Step 6: "
            "Submit as-built drawings and testing documentation."
        ),
        key_factors=[
            "Railroad company permit requirements",
            "API RP 1102 design compliance",
            "Casing requirements and specifications",
            "Minimum depth of cover below base of rail",
            "Permit fees and annual rental costs",
            "Construction safety and flagging requirements",
        ],
        primary_authority=[
            "API RP 1102 (Steel Pipelines Crossing Railroads and Highways)",
            "49 CFR 192.325 (Underground Clearance at Railroad Crossings)",
            "Railroad company standard permit agreements",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Railroad demands excessive permit fees, restrictive construction windows, and onerous "
            "insurance and indemnification requirements."
        ),
        counter_arguments=[
            "Surface Transportation Board has jurisdiction over unreasonable crossing denials",
            "State common carrier pipeline has statutory crossing rights in many jurisdictions",
            "API RP 1102 compliance ensures safe crossing design",
        ],
        resolution_strategy=(
            "Submit permit applications early as railroad review takes 60-120 days. Budget for permit fees "
            "($5,000-$25,000 per crossing) and annual rental ($500-$2,000/year). Design to API RP 1102 "
            "standards from the outset. Coordinate construction windows with railroad operations."
        ),
        entity_scope="Pipeline companies, railroad companies, FRA, STB",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established industry practice with standardized permit processes",
        controlling_precedent="API RP 1102 industry standard adopted by reference in railroad permits",
    ),

    # ---- ENVIRONMENTAL PERMITTING ----
    DoctrineBlock(
        topic="usace_section_404_wetland_permitting",
        category=IssueCategory.ENVIRONMENTAL_PERMITTING,
        keywords=["section 404", "wetland", "usace", "permit", "clean water act", "waters", "nationwide", "individual"],
        conclusion_template=(
            "Pipeline construction impacting wetlands or waters of the United States requires USACE "
            "authorization under Clean Water Act Section 404. Most pipeline projects qualify for "
            "Nationwide Permit 12 (Utility Line Activities), but impacts exceeding NWP thresholds "
            "require an Individual Permit with longer timelines and compensatory mitigation."
        ),
        reasoning_framework=(
            "Step 1: Conduct wetland delineation to identify jurisdictional waters within the project area. "
            "Step 2: Determine if project qualifies for NWP 12. Current threshold: loss of no more than "
            "1/2 acre of waters per single and complete project. Step 3: If NWP 12 applies, submit "
            "pre-construction notification to USACE district. Step 4: If impacts exceed NWP thresholds, "
            "apply for Individual Permit (12-18 month timeline). Step 5: Prepare alternatives analysis "
            "demonstrating no practicable alternative with less environmental impact (404(b)(1) guidelines). "
            "Step 6: Develop compensatory mitigation plan for unavoidable wetland impacts - mitigation bank "
            "credits, in-lieu fee, or permittee-responsible mitigation. Step 7: Obtain state 401 water "
            "quality certification."
        ),
        key_factors=[
            "Jurisdictional wetland delineation results",
            "NWP 12 eligibility and acreage thresholds",
            "Alternatives analysis under 404(b)(1) guidelines",
            "Compensatory mitigation requirements",
            "State 401 water quality certification",
            "Regional and district-specific conditions",
        ],
        primary_authority=[
            "Clean Water Act Section 404, 33 USC 1344",
            "40 CFR Part 230 (404(b)(1) Guidelines)",
            "33 CFR Part 330 (Nationwide Permit Regulations)",
            "USACE Nationwide Permit 12 and General Conditions",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Environmental groups argue pipeline should avoid all wetlands, NWP 12 is improperly segmented, "
            "and compensatory mitigation is insufficient."
        ),
        counter_arguments=[
            "NWP 12 specifically designed for utility line activities",
            "Route optimization minimized wetland impacts to maximum extent practicable",
            "Compensatory mitigation achieves no net loss of wetland function",
            "USACE retains discretionary authority to add conditions",
        ],
        resolution_strategy=(
            "Conduct thorough wetland delineation early in project planning. Optimize route to minimize "
            "wetland crossings. Use HDD for major wetland crossings where feasible. Pre-purchase mitigation "
            "bank credits. Engage USACE early for pre-application meetings."
        ),
        entity_scope="Pipeline companies, USACE, EPA, environmental consultants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established regulatory framework; district-specific interpretation varies",
        controlling_precedent="USACE NWP 12 reissuance conditions and regional conditions",
    ),

    DoctrineBlock(
        topic="cultural_resource_section_106_review",
        category=IssueCategory.ENVIRONMENTAL_PERMITTING,
        keywords=["cultural", "resource", "section 106", "nhpa", "historic", "preservation", "archaeological", "shpo"],
        conclusion_template=(
            "Pipeline projects requiring federal permits or involving federal lands trigger Section 106 "
            "review under the National Historic Preservation Act. The process requires identification of "
            "historic properties within the area of potential effects, assessment of adverse effects, "
            "and resolution through avoidance, minimization, or mitigation."
        ),
        reasoning_framework=(
            "Step 1: Determine if Section 106 is triggered - any federal undertaking (FERC certificate, "
            "USACE permit, BLM crossing) triggers the review. Step 2: Define the Area of Potential Effects "
            "(APE) - typically the construction ROW plus visual APE for above-ground facilities. Step 3: "
            "Conduct Phase I cultural resource survey (pedestrian survey, shovel testing) within the APE. "
            "Step 4: Identify properties potentially eligible for the National Register of Historic Places. "
            "Step 5: Consult with SHPO/THPO on eligibility and effect determinations. Step 6: If adverse "
            "effect found, negotiate Memorandum of Agreement (MOA) with mitigation measures. Step 7: "
            "Mitigation may include data recovery excavation, route modification, or monitoring during "
            "construction."
        ),
        key_factors=[
            "Federal undertaking trigger identification",
            "Area of Potential Effects definition",
            "Phase I/II/III survey requirements",
            "National Register eligibility determination",
            "SHPO/THPO consultation outcomes",
            "Tribal consultation requirements",
        ],
        primary_authority=[
            "National Historic Preservation Act Section 106, 54 USC 306108",
            "36 CFR Part 800 (Advisory Council Regulations)",
            "FERC guidance on cultural resource compliance",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "SHPO determines multiple sites are eligible for National Register and requires extensive "
            "Phase III data recovery, significantly increasing project cost and timeline."
        ),
        counter_arguments=[
            "Route modification can avoid most significant cultural resources",
            "Programmatic Agreement can streamline review for linear projects",
            "Construction monitoring provides adequate protection for low-probability areas",
        ],
        resolution_strategy=(
            "Conduct Phase I surveys early to identify potential conflicts. Modify route to avoid significant "
            "sites where feasible. Engage tribal consultation early for projects on tribal or ancestral lands. "
            "Negotiate programmatic approach with SHPO for long linear projects."
        ),
        entity_scope="Pipeline companies, FERC, USACE, SHPO, THPO, tribes, archaeologists",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established regulatory process but site-specific outcomes vary",
        controlling_precedent="36 CFR Part 800 procedural requirements",
    ),

    DoctrineBlock(
        topic="endangered_species_section_7_consultation",
        category=IssueCategory.ENVIRONMENTAL_PERMITTING,
        keywords=["endangered", "species", "section 7", "esa", "consultation", "biological", "assessment", "critical habitat"],
        conclusion_template=(
            "Pipeline projects with a federal nexus require Section 7 consultation under the Endangered "
            "Species Act if listed species or critical habitat may be affected. Formal consultation results "
            "in a Biological Opinion with an incidental take statement and reasonable and prudent measures."
        ),
        reasoning_framework=(
            "Step 1: Determine federal nexus (FERC certificate, USACE permit, BLM authorization). Step 2: "
            "Conduct desktop review of USFWS IPaC database and state natural heritage databases for listed "
            "species within project area. Step 3: If potential effects identified, prepare Biological "
            "Assessment (BA) evaluating impacts to each listed species. Step 4: Submit BA to USFWS (or NMFS "
            "for marine species). Step 5: If 'may affect, likely to adversely affect' determination, enter "
            "formal consultation (135-day timeline). Step 6: USFWS issues Biological Opinion (BiOp) with "
            "jeopardy/no-jeopardy finding. Step 7: If no-jeopardy, incidental take statement with reasonable "
            "and prudent measures authorizes limited take. Step 8: Implement all terms and conditions."
        ),
        key_factors=[
            "Listed species presence in project area",
            "Critical habitat designation overlap",
            "Federal nexus identification",
            "Biological Assessment preparation and findings",
            "Formal vs informal consultation pathway",
            "Incidental take authorization and conditions",
        ],
        primary_authority=[
            "Endangered Species Act Section 7, 16 USC 1536",
            "50 CFR Part 402 (Interagency Cooperation Regulations)",
            "USFWS Section 7 Consultation Handbook",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "USFWS determines project will adversely affect listed species and requires extensive seasonal "
            "construction restrictions, biological monitoring, and habitat restoration."
        ),
        counter_arguments=[
            "Pipeline construction impacts are temporary and localized",
            "Habitat restoration returns disturbed areas to pre-construction condition",
            "Construction timing restrictions adequately protect breeding seasons",
            "Pipeline operation has minimal ongoing impact to listed species",
        ],
        resolution_strategy=(
            "Screen for listed species early using IPaC and state databases. Conduct species-specific surveys "
            "during appropriate seasons. Modify route to avoid critical habitat where feasible. Propose "
            "robust avoidance and minimization measures in the BA. Engage USFWS informally before formal "
            "consultation to identify key concerns."
        ),
        entity_scope="Pipeline companies, USFWS, NMFS, FERC, environmental consultants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established consultation process; species-specific outcomes vary",
        controlling_precedent="50 CFR Part 402 procedural requirements for Section 7 consultation",
    ),

    # ---- SURFACE DAMAGE ----
    DoctrineBlock(
        topic="surface_damage_crop_compensation",
        category=IssueCategory.SURFACE_DAMAGE,
        keywords=["surface", "damage", "crop", "compensation", "restoration", "agriculture", "loss", "payment"],
        conclusion_template=(
            "Pipeline construction causes surface and crop damage requiring compensation to landowners. "
            "Texas has no statutory surface damage act for pipeline construction, so compensation is "
            "governed by easement terms, common law, and negotiation. Typical payments cover crop loss, "
            "soil compaction remediation, fence repair, and inconvenience."
        ),
        reasoning_framework=(
            "Step 1: Document pre-construction conditions through photography, soil sampling, and crop "
            "yield records. Step 2: Calculate crop loss based on expected yield at commodity prices for "
            "the construction season plus any residual yield loss in subsequent years. Step 3: Assess soil "
            "impacts - compaction from heavy equipment, topsoil/subsoil mixing, drainage disruption. Step 4: "
            "Quantify infrastructure damage - fences, irrigation systems, water wells, drainage tiles, "
            "terraces, windbreaks. Step 5: Determine restoration costs - re-grading, decompaction, topsoil "
            "replacement, reseeding. Step 6: Negotiate surface damage agreement concurrent with easement. "
            "Step 7: Include post-construction monitoring and remediation provisions."
        ),
        key_factors=[
            "Pre-construction condition documentation",
            "Crop loss calculation methodology",
            "Soil compaction and restoration requirements",
            "Infrastructure damage and repair costs",
            "Multi-year yield impact assessment",
            "Post-construction remediation provisions",
        ],
        primary_authority=[
            "Easement agreement surface damage provisions",
            "Texas common law on surface damage",
            "USDA crop yield and commodity price data",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Landowner claims construction permanently damaged soil productivity, disrupted irrigation, "
            "and reduced property value beyond the surface damage payment."
        ),
        counter_arguments=[
            "Pre-construction documentation establishes baseline conditions",
            "Topsoil segregation and decompaction restores soil productivity",
            "Post-construction monitoring identifies and remediates residual impacts",
            "Surface damage payments are separate from easement compensation",
        ],
        resolution_strategy=(
            "Negotiate comprehensive surface damage agreement with specific restoration standards. Document "
            "pre-construction conditions thoroughly. Segregate and replace topsoil during construction. "
            "Conduct post-construction soil testing and remediation. Make prompt crop damage payments."
        ),
        entity_scope="Pipeline companies, landowners, agricultural consultants, ROW agents",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Compensation standards well-established in industry practice",
        controlling_precedent="Texas common law duty to restore surface after pipeline construction",
    ),

    # ---- PIPELINE SAFETY ----
    DoctrineBlock(
        topic="phmsa_pipeline_safety_regulations",
        category=IssueCategory.PIPELINE_SAFETY,
        keywords=["phmsa", "safety", "regulation", "49 cfr", "192", "195", "class location", "integrity"],
        conclusion_template=(
            "PHMSA regulations under 49 CFR Parts 190-199 govern pipeline safety including design, "
            "construction, operation, maintenance, and integrity management. Class location designation "
            "determines design factor, depth of cover, and population monitoring requirements. Operators "
            "must maintain integrity management programs for high consequence areas."
        ),
        reasoning_framework=(
            "Step 1: Classify pipeline segments by class location (1-4) based on building count within "
            "220 yards of centerline per 49 CFR 192.5. Step 2: Apply design factors per class location - "
            "Class 1: 0.72, Class 2: 0.60, Class 3: 0.50, Class 4: 0.40. Step 3: Determine minimum "
            "depth of cover - Class 1-2: 30 inches, Class 3-4: 36 inches (gas); 36 inches for liquid. "
            "Step 4: Establish maximum allowable operating pressure based on pipe specifications and design "
            "factor. Step 5: Develop integrity management program for high consequence areas (HCAs). Step 6: "
            "Implement damage prevention program including one-call participation, patrol, and encroachment "
            "monitoring. Step 7: Maintain records per 49 CFR 192 Subpart P or 195 Subpart G."
        ),
        key_factors=[
            "Class location designation and monitoring",
            "Design factor and MAOP calculation",
            "Depth of cover requirements",
            "Integrity management program requirements",
            "Damage prevention and one-call participation",
            "Population encroachment monitoring",
        ],
        primary_authority=[
            "49 CFR Part 192 (Transportation of Natural and Other Gas by Pipeline)",
            "49 CFR Part 195 (Transportation of Hazardous Liquids by Pipeline)",
            "PHMSA Advisory Bulletins and Interpretive Letters",
            "API 1160 (Managing System Integrity for Hazardous Liquid Pipelines)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "PHMSA finds operator noncompliant with integrity management or class location monitoring "
            "and issues corrective action order or civil penalty."
        ),
        counter_arguments=[
            "Operator maintains comprehensive compliance program exceeding minimum requirements",
            "Class location surveys conducted on required schedule",
            "Integrity assessments performed using approved methods within required intervals",
        ],
        resolution_strategy=(
            "Maintain rigorous compliance program with documented procedures. Conduct class location surveys "
            "annually. Perform integrity assessments per required intervals. Report incidents per 49 CFR "
            "191/195.50. Engage PHMSA proactively on interpretation questions."
        ),
        entity_scope="Pipeline operators, PHMSA, state pipeline safety offices",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Federal regulations with established compliance framework",
        controlling_precedent="49 CFR Parts 192/195 regulatory requirements",
    ),

    # ---- ABANDONMENT ----
    DoctrineBlock(
        topic="abandonment_in_place_vs_removal",
        category=IssueCategory.ABANDONMENT,
        keywords=["abandonment", "in place", "removal", "decommission", "pipeline", "purge", "cap", "easement"],
        conclusion_template=(
            "Pipeline abandonment involves either abandonment in place (purge, fill, cap, and leave) or "
            "removal (excavate and remove). Abandonment in place is standard for buried pipelines where "
            "removal would cause greater environmental impact. Easement rights upon abandonment depend "
            "on easement language - some terminate, others persist."
        ),
        reasoning_framework=(
            "Step 1: Review easement terms regarding abandonment. Many easements are silent on abandonment; "
            "some require removal. Step 2: Evaluate environmental impact of removal vs abandonment in place. "
            "Removal disturbs the surface and can impact wetlands, streams, and cultural resources. Step 3: "
            "If abandoning in place: disconnect from supply, purge product, clean pipeline interior, fill "
            "with inert material (grout, foam, or cap and vent), and cap and seal all openings. Step 4: "
            "If removing: excavate, remove pipe, backfill, restore surface. Step 5: Notify PHMSA and state "
            "agencies per applicable regulations. Step 6: Determine whether easement terminates upon "
            "abandonment or continues for the abandoned pipe. Step 7: Record notice of abandonment in "
            "county deed records."
        ),
        key_factors=[
            "Easement language regarding abandonment and termination",
            "Environmental impact comparison (removal vs in-place)",
            "Pipeline purging and cleaning requirements",
            "PHMSA notification and reporting requirements",
            "Landowner notification and consent",
            "County recording of abandonment status",
        ],
        primary_authority=[
            "49 CFR 192.727 (Abandonment or Deactivation of Facilities - Gas)",
            "49 CFR 195.402(c)(10) (Abandonment - Hazardous Liquids)",
            "FERC Certificate Abandonment Authorization (Interstate)",
            "Easement agreement terms and conditions",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Landowner demands complete removal of abandoned pipeline, argues abandonment in place creates "
            "permanent encumbrance and interferes with surface use."
        ),
        counter_arguments=[
            "Abandonment in place causes less surface disturbance than removal",
            "Properly abandoned pipeline poses no safety risk",
            "Removal would impact previously restored surface and vegetation",
            "Industry standard practice favors abandonment in place for buried lines",
        ],
        resolution_strategy=(
            "Review easement terms first. If silent on abandonment, propose abandonment in place with "
            "compensation for permanent encumbrance. Offer enhanced surface restoration. Provide written "
            "notice and record abandonment in county records. Consider voluntary removal payments for "
            "resistant landowners."
        ),
        entity_scope="Pipeline operators, landowners, PHMSA, FERC (interstate), state agencies",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="Outcome depends heavily on specific easement language",
        controlling_precedent="49 CFR 192.727 abandonment requirements; easement-specific interpretation",
        disclosure_caveat="Easement terms must be individually reviewed to determine abandonment obligations",
    ),

    # ---- DISPUTE RESOLUTION ----
    DoctrineBlock(
        topic="landowner_complaint_dispute_resolution",
        category=IssueCategory.DISPUTE_RESOLUTION,
        keywords=["landowner", "complaint", "dispute", "resolution", "mediation", "arbitration", "damage claim"],
        conclusion_template=(
            "Pipeline landowner disputes arise from construction damage, easement scope disagreements, "
            "encroachment, and compensation disputes. Resolution pathways include direct negotiation, "
            "mediation, arbitration (if provided in the easement), and litigation. Early resolution "
            "reduces costs and preserves landowner relationships for ongoing operations."
        ),
        reasoning_framework=(
            "Step 1: Receive and document landowner complaint with specificity - nature of claim, location, "
            "timeline, evidence. Step 2: Conduct field investigation to verify claim. Document conditions "
            "with photography and measurements. Step 3: Classify the dispute - construction damage (surface, "
            "crop, infrastructure), easement scope (unauthorized activity, width dispute), compensation "
            "(inadequate payment, disputed valuation), or encroachment (third-party or pipeline company). "
            "Step 4: Attempt direct resolution through ROW agent or landowner liaison. Step 5: If direct "
            "resolution fails, offer mediation with a neutral third party. Step 6: If easement provides for "
            "arbitration, follow contractual ADR provisions. Step 7: If all else fails, prepare for "
            "litigation defense or prosecution."
        ),
        key_factors=[
            "Nature and classification of the dispute",
            "Easement terms governing dispute resolution",
            "Documentation of pre-construction conditions",
            "Field investigation findings",
            "Applicable statute of limitations",
            "Cost-benefit of settlement vs litigation",
        ],
        primary_authority=[
            "Easement agreement dispute resolution provisions",
            "Texas Property Code (damages and remedies)",
            "Texas Civil Practice and Remedies Code",
        ],
        burden_holder=BurdenHolder.SHARED,
        adversary_position=(
            "Landowner alleges pipeline company exceeded easement scope, caused undisclosed damage during "
            "construction, and demands restoration to pre-construction condition plus consequential damages."
        ),
        counter_arguments=[
            "Pipeline company operated within easement rights as defined in the instrument",
            "Pre-construction documentation shows conditions were accurately captured",
            "Restoration was performed per contractual standards",
        ],
        resolution_strategy=(
            "Respond promptly to all complaints. Investigate within 48 hours. Maintain professional "
            "landowner relations. Settle meritorious claims quickly. Document all communications and "
            "resolution efforts. Use mediation for complex disputes before litigation."
        ),
        entity_scope="Pipeline companies, landowners, ROW agents, mediators, courts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Resolution approach well-established; outcomes are case-specific",
        controlling_precedent="Texas common law on easement disputes and surface damage",
    ),

    # ---- TEMPORARY WORKSPACE ----
    DoctrineBlock(
        topic="temporary_workspace_agreements",
        category=IssueCategory.TEMPORARY_WORKSPACE,
        keywords=["temporary", "workspace", "construction", "staging", "agreement", "duration", "restoration"],
        conclusion_template=(
            "Temporary workspace agreements authorize pipeline construction activities beyond the permanent "
            "easement corridor. Standard TWS width is 25-75 feet adjacent to the permanent ROW, with "
            "additional workspace at road crossings, HDD entry/exit pits, and wetland crossings. Duration "
            "is typically limited to the construction period plus restoration."
        ),
        reasoning_framework=(
            "Step 1: Determine required temporary workspace based on construction method, pipe diameter, "
            "and terrain. Standard: 25 ft additional for small diameter, 50-75 ft for large diameter (24+). "
            "Step 2: Identify additional workspace needs - HDD entry/exit pits (100x200 ft), road/stream "
            "crossings (additional 50-100 ft), tie-in locations, pipe storage yards. Step 3: Negotiate TWS "
            "agreement separately from permanent easement. Step 4: Specify duration - typically 12-24 months "
            "from commencement of construction. Step 5: Define permitted activities within TWS - equipment "
            "passage, material storage, spoil placement, vehicle parking. Step 6: Restoration requirements - "
            "re-grade to original contour, replace topsoil, reseed, repair fences. Step 7: Compensation "
            "based on duration and impact to surface use."
        ),
        key_factors=[
            "Required workspace dimensions based on construction method",
            "Additional workspace at crossings and special features",
            "Agreement duration and extension provisions",
            "Permitted activities within workspace",
            "Restoration standards and timeline",
            "Compensation structure (per acre or lump sum)",
        ],
        primary_authority=[
            "FERC Plan and Profile requirements (interstate)",
            "Industry standard construction specifications",
            "Easement agreement temporary workspace provisions",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Landowner argues requested temporary workspace is excessive, construction duration is too "
            "long, and compensation is inadequate for the disruption period."
        ),
        counter_arguments=[
            "Workspace dimensions are based on engineering requirements and safety standards",
            "Adequate workspace reduces construction duration and surface impact",
            "Compensation reflects fair rental value for the temporary use period",
        ],
        resolution_strategy=(
            "Justify workspace dimensions with engineering analysis. Minimize duration through efficient "
            "construction scheduling. Offer competitive per-acre or lump-sum compensation. Include clear "
            "restoration standards with warranty period. Conduct pre-construction condition documentation."
        ),
        entity_scope="Pipeline companies, landowners, construction contractors, ROW agents",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standards well-established for workspace dimensions",
        controlling_precedent="FERC construction workspace standards for certificated projects",
    ),

    # ---- ENCROACHMENT ----
    DoctrineBlock(
        topic="encroachment_monitoring_enforcement",
        category=IssueCategory.ENCROACHMENT,
        keywords=["encroachment", "monitoring", "enforcement", "building", "structure", "setback", "one-call"],
        conclusion_template=(
            "Pipeline encroachment occurs when unauthorized structures, activities, or land use changes "
            "occur within the permanent easement or setback area. Operators must monitor for encroachment "
            "per PHMSA requirements, enforce easement terms, and may need to require removal of "
            "unauthorized structures to maintain pipeline safety."
        ),
        reasoning_framework=(
            "Step 1: Conduct regular ROW patrols - aerial (quarterly-annually) and ground-based (semi-annually "
            "to annually). Step 2: Identify encroachments - buildings, fences, deep-rooted trees, paved "
            "surfaces, stored materials, excavation activity. Step 3: Assess safety impact based on class "
            "location and pipeline operating parameters. Step 4: Notify encroaching party in writing of "
            "easement violation and required corrective action. Step 5: If voluntary compliance not achieved, "
            "escalate through legal counsel with demand for removal. Step 6: If class location changes due "
            "to building encroachment within the 220-yard measurement area, operator must upgrade pipeline "
            "or reduce MAOP per 49 CFR 192.611. Step 7: Document all monitoring and enforcement actions."
        ),
        key_factors=[
            "Patrol frequency and method (aerial vs ground)",
            "Type and severity of encroachment",
            "Impact on class location designation",
            "Easement enforcement rights and procedures",
            "PHMSA damage prevention requirements",
            "One-call system participation and enforcement",
        ],
        primary_authority=[
            "49 CFR 192.611 (Change in Class Location)",
            "49 CFR 192.614 (Damage Prevention Program)",
            "49 CFR 192.706 (Transmission Line Patrol)",
            "Easement agreement use restriction provisions",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position=(
            "Encroaching party argues pipeline company failed to maintain markers, never objected to "
            "gradual encroachment, and has effectively acquiesced to the changed use."
        ),
        counter_arguments=[
            "Pipeline safety regulations impose non-waivable safety obligations",
            "Easement enforcement is not subject to acquiescence defense where safety is at issue",
            "PHMSA damage prevention requirements mandate encroachment monitoring",
            "Operator cannot waive public safety obligations through inaction",
        ],
        resolution_strategy=(
            "Maintain proactive patrol program. Respond promptly to all identified encroachments. Document "
            "all notifications and enforcement actions. Engage legal counsel for persistent violations. "
            "Report class location changes to PHMSA as required."
        ),
        entity_scope="Pipeline operators, landowners, PHMSA, local building authorities",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PHMSA requirements are non-negotiable; enforcement effectiveness varies",
        controlling_precedent="49 CFR 192.611 class location change requirements",
    ),

    # ---- ADDITIONAL DOCTRINE BLOCKS ----
    DoctrineBlock(
        topic="highway_crossing_txdot_permits",
        category=IssueCategory.CROSSING_PERMITS,
        keywords=["highway", "crossing", "txdot", "permit", "state highway", "utility", "accommodation"],
        conclusion_template=(
            "Pipeline crossings of Texas state highways require TxDOT utility accommodation permits "
            "under 43 TAC Chapter 21. Crossings must be by bore, jack, or HDD - open-cut of state "
            "highways is generally prohibited. Minimum depth of cover is 48 inches below the roadway."
        ),
        reasoning_framework=(
            "Step 1: Submit TxDOT utility installation permit application to the appropriate district. "
            "Step 2: Provide engineering plans showing crossing method, depth, and alignment. Step 3: "
            "Crossing method must be bore/jack or HDD for state highways. Open-cut may be permitted only "
            "on very low-traffic roads with TxDOT approval. Step 4: Minimum depth of cover is 48 inches "
            "below the bottom of the roadway pavement structure. Step 5: Casing may be required depending "
            "on pipe diameter, product, and traffic volume. Step 6: Comply with TxDOT traffic control "
            "requirements during construction. Step 7: Submit as-built documentation."
        ),
        key_factors=[
            "TxDOT district permit requirements",
            "Crossing method restrictions",
            "Minimum depth of cover below pavement",
            "Casing requirements determination",
            "Traffic control plan requirements",
            "Construction timing restrictions",
        ],
        primary_authority=[
            "43 TAC Chapter 21 (TxDOT Utility Accommodation Rules)",
            "TxDOT Utility Manual",
            "AASHTO Policy on Accommodation of Utilities",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="TxDOT requires costly casing or relocation of proposed crossing point.",
        counter_arguments=[
            "Uncased crossing is permitted where pipeline meets design standards",
            "Alternative crossing locations may have lower impact",
            "Industry standards support uncased crossings for qualified pipelines",
        ],
        resolution_strategy=(
            "Submit complete permit application with professional engineering plans. Coordinate with TxDOT "
            "district utility coordinator early. Budget 30-90 days for permit review. Have contingency "
            "plans for casing or relocation requirements."
        ),
        entity_scope="Pipeline companies, TxDOT, county road departments",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established TxDOT permit process with clear requirements",
        controlling_precedent="43 TAC Chapter 21 utility accommodation requirements",
    ),

    DoctrineBlock(
        topic="nepa_environmental_review_pipeline",
        category=IssueCategory.ENVIRONMENTAL_PERMITTING,
        keywords=["nepa", "environmental", "review", "impact", "statement", "assessment", "eis", "ea", "fonsi"],
        conclusion_template=(
            "Pipeline projects with a federal nexus require environmental review under NEPA. FERC-certificated "
            "projects undergo NEPA review as part of the Section 7 process. The scope determines whether "
            "an Environmental Assessment (EA) or Environmental Impact Statement (EIS) is required."
        ),
        reasoning_framework=(
            "Step 1: Identify the federal action triggering NEPA - FERC certificate, USACE permit, BLM "
            "right-of-way grant, Forest Service crossing permit. Step 2: Determine review level. Categorical "
            "exclusion for minor actions, EA for projects without likely significant impact, EIS for major "
            "projects with significant environmental effects. Step 3: Scoping process for EIS - public "
            "meetings, comment period, identification of issues and alternatives. Step 4: Draft EIS/EA "
            "preparation analyzing purpose and need, alternatives, affected environment, and environmental "
            "consequences. Step 5: Public comment period (45 days for draft EIS). Step 6: Final EIS and "
            "Record of Decision, or EA and Finding of No Significant Impact (FONSI). Step 7: Agency "
            "decision incorporating NEPA analysis."
        ),
        key_factors=[
            "Federal action and lead agency identification",
            "Review level determination (CE/EA/EIS)",
            "Scoping and public involvement",
            "Alternatives analysis",
            "Cumulative impacts assessment",
            "Mitigation measures and monitoring",
        ],
        primary_authority=[
            "National Environmental Policy Act, 42 USC 4321 et seq.",
            "40 CFR Parts 1500-1508 (CEQ NEPA Regulations)",
            "18 CFR Part 380 (FERC NEPA Regulations)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="Environmental groups challenge EA/FONSI and demand full EIS with alternatives analysis.",
        counter_arguments=[
            "EA adequately analyzes environmental impacts for projects below significance threshold",
            "Alternatives analysis included in EA demonstrates no significant impacts",
            "Mitigation measures reduce all impacts below significance levels",
        ],
        resolution_strategy=(
            "Prepare thorough environmental resource reports for FERC pre-filing. Support agency in EA/EIS "
            "preparation with complete data. Address all scoping comments substantively. Propose meaningful "
            "mitigation measures. Engage environmental groups early."
        ),
        entity_scope="Pipeline companies, FERC, CEQ, cooperating agencies, public",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established NEPA process; significance determination is judgment-based",
        controlling_precedent="40 CFR Parts 1500-1508 CEQ regulations (2020 revisions)",
    ),

    DoctrineBlock(
        topic="cathodic_protection_easement",
        category=IssueCategory.EASEMENT_NEGOTIATION,
        keywords=["cathodic", "protection", "rectifier", "anode", "easement", "corrosion", "ground bed"],
        conclusion_template=(
            "Cathodic protection systems require easement rights for rectifier installations, anode ground "
            "beds, and test stations along the pipeline ROW. These rights should be explicitly included "
            "in the pipeline easement or obtained through separate cathodic protection easements."
        ),
        reasoning_framework=(
            "Step 1: Pipeline easement should explicitly authorize cathodic protection installations within "
            "the permanent easement corridor. Step 2: Rectifier sites and deep anode ground beds may require "
            "locations outside the pipeline ROW - separate easements needed. Step 3: Test stations installed "
            "at road crossings, foreign pipeline crossings, and regular intervals. Step 4: Shallow anode "
            "ground beds typically installed within the pipeline easement during construction. Step 5: Deep "
            "anode ground beds may extend 200-500 feet from the pipeline and require separate easement. "
            "Step 6: Stray current mitigation may require bonds with adjacent metallic structures. Step 7: "
            "Access rights for regular monitoring and rectifier maintenance must be documented."
        ),
        key_factors=[
            "Easement authorization for CP installations",
            "Rectifier and ground bed location requirements",
            "Test station placement at crossings and intervals",
            "Access for monitoring and maintenance",
            "Stray current mitigation provisions",
            "Interference testing with adjacent structures",
        ],
        primary_authority=[
            "49 CFR 192 Subpart I (Requirements for Corrosion Control)",
            "49 CFR 195.571-589 (Corrosion Control for Hazardous Liquid Pipelines)",
            "NACE SP0169 (Control of External Corrosion on Underground Metallic Piping)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="Landowner objects to above-ground rectifier installation and access for monitoring.",
        counter_arguments=[
            "Cathodic protection is federally mandated for pipeline safety",
            "Rectifier installations are small and unobtrusive",
            "Regular monitoring ensures pipeline integrity and public safety",
        ],
        resolution_strategy=(
            "Include CP rights in primary pipeline easement. Negotiate separate easements for off-ROW "
            "rectifier and ground bed locations. Compensate for above-ground installations. Minimize visual "
            "impact through screening and low-profile equipment."
        ),
        entity_scope="Pipeline operators, landowners, corrosion engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Federal CP requirements are non-negotiable; installation specifics negotiable",
        controlling_precedent="49 CFR 192 Subpart I mandatory corrosion control requirements",
    ),

    DoctrineBlock(
        topic="row_release_termination",
        category=IssueCategory.ABANDONMENT,
        keywords=["row", "release", "termination", "easement", "quitclaim", "reversion", "expiration"],
        conclusion_template=(
            "Pipeline ROW easement release occurs through express release (quitclaim deed), abandonment "
            "of purpose, or expiration of term. Landowners may request release when pipeline is permanently "
            "abandoned. Pipeline companies should formally release unused easements to maintain good "
            "landowner relations and clear title."
        ),
        reasoning_framework=(
            "Step 1: Determine if easement has a fixed term or is perpetual. Fixed-term easements expire "
            "automatically. Perpetual easements require affirmative release. Step 2: Evaluate whether "
            "pipeline has been abandoned. Non-use alone does not terminate an easement; intent to abandon "
            "plus non-use is required. Step 3: If pipeline is abandoned and no future use is contemplated, "
            "prepare and execute quitclaim deed releasing the easement. Step 4: Record the release in county "
            "deed records where the easement was originally recorded. Step 5: If pipeline is abandoned in "
            "place, consider partial release (release surface rights but retain subsurface pipe encumbrance "
            "notice). Step 6: Coordinate with any co-lessees or assignees who may have interests in the "
            "easement."
        ),
        key_factors=[
            "Easement term (fixed vs perpetual)",
            "Evidence of abandonment (intent plus non-use)",
            "Quitclaim deed preparation and recording",
            "Partial release considerations for AIP",
            "Co-lessee and assignee coordination",
            "Title clearing for landowner benefit",
        ],
        primary_authority=[
            "Texas Property Code on easement termination",
            "Texas case law on abandonment of easements",
            "County recording requirements",
        ],
        burden_holder=BurdenHolder.SHARED,
        adversary_position="Landowner demands immediate release of unused easement and argues abandonment by non-use.",
        counter_arguments=[
            "Non-use alone does not constitute abandonment under Texas law",
            "Pipeline company retains right to future use during easement term",
            "Partial release may be appropriate for portions no longer needed",
        ],
        resolution_strategy=(
            "Review easement terms and current use. Release easements that are no longer needed. Execute "
            "and record quitclaim deeds promptly. For AIP situations, consider partial release with "
            "retained pipe encumbrance notice."
        ),
        entity_scope="Pipeline companies, landowners, title companies, county clerks",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Texas easement termination law well-established",
        controlling_precedent="Texas law on abandonment of easements (intent plus non-use)",
    ),

    DoctrineBlock(
        topic="pipeline_restoration_reclamation",
        category=IssueCategory.SURFACE_DAMAGE,
        keywords=["restoration", "reclamation", "regrade", "topsoil", "reseed", "erosion", "construction", "cleanup"],
        conclusion_template=(
            "Post-construction restoration requires returning the ROW to substantially pre-construction "
            "condition. Key elements include regrading to original contour, topsoil replacement, reseeding "
            "with approved seed mix, erosion control installation, and fence/infrastructure repair. "
            "Restoration standards are defined in the easement and regulatory conditions."
        ),
        reasoning_framework=(
            "Step 1: Begin cleanup and restoration immediately following pipeline installation and backfill. "
            "Step 2: Rough grade the ROW to approximate original contour. Remove construction debris, "
            "rocks, and excess material. Step 3: Decompact subsoil in agricultural areas using deep ripping. "
            "Step 4: Replace segregated topsoil to original depth. Step 5: Install permanent erosion control "
            "measures - silt fence until vegetation established, permanent slope breakers on steep grades. "
            "Step 6: Reseed with landowner-approved seed mix or agency-specified seed mix for regulated "
            "crossings. Step 7: Repair or replace fences, gates, and other infrastructure. Step 8: Conduct "
            "post-construction monitoring for 2-3 growing seasons."
        ),
        key_factors=[
            "Regrading to original contour accuracy",
            "Topsoil segregation and replacement depth",
            "Decompaction of subsoil in agricultural areas",
            "Seed mix selection and application timing",
            "Erosion control installation and maintenance",
            "Post-construction monitoring duration",
        ],
        primary_authority=[
            "FERC Upland Erosion Control, Revegetation, and Maintenance Plan",
            "FERC Wetland and Waterbody Construction and Mitigation Procedures",
            "Easement agreement restoration provisions",
            "State and local erosion control requirements",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="Landowner claims restoration is inadequate, soil productivity not restored, drainage disrupted.",
        counter_arguments=[
            "Restoration performed per contractual and regulatory standards",
            "Post-construction monitoring identifies and addresses deficiencies",
            "Soil testing confirms topsoil replacement and fertility",
        ],
        resolution_strategy=(
            "Document pre-construction conditions thoroughly. Segregate and replace topsoil per plan. "
            "Conduct final cleanup inspection with landowner present. Address deficiencies promptly. "
            "Monitor for 2-3 growing seasons and remediate as needed."
        ),
        entity_scope="Pipeline companies, contractors, landowners, environmental inspectors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Restoration standards well-defined in FERC plans and industry practice",
        controlling_precedent="FERC Upland Erosion Control Plan standard conditions",
    ),

    DoctrineBlock(
        topic="tceq_state_environmental_permits",
        category=IssueCategory.ENVIRONMENTAL_PERMITTING,
        keywords=["tceq", "texas", "environmental", "permit", "water quality", "air", "stormwater", "discharge"],
        conclusion_template=(
            "Pipeline construction in Texas requires various TCEQ permits including stormwater discharge "
            "(TPDES construction general permit), water quality certification (Section 401), and potentially "
            "air permits for compressor stations. Hydrostatic test water discharge requires TPDES permit "
            "or approved disposal method."
        ),
        reasoning_framework=(
            "Step 1: Obtain TPDES Construction General Permit (TXR150000) for stormwater discharges from "
            "construction activity disturbing one or more acres. Step 2: Prepare Stormwater Pollution "
            "Prevention Plan (SW3P). Step 3: Obtain Section 401 Water Quality Certification from TCEQ "
            "for projects requiring USACE Section 404 permit. Step 4: Plan hydrostatic test water "
            "management - discharge permit, filtration, or disposal by injection well. Step 5: If "
            "compressor station included, evaluate air permit requirements under TCEQ New Source Review. "
            "Step 6: Comply with Edwards Aquifer rules if project crosses Edwards Aquifer recharge or "
            "contributing zone. Step 7: Obtain any required TCEQ groundwater protection permits."
        ),
        key_factors=[
            "TPDES construction general permit threshold (1+ acre)",
            "SW3P development and implementation",
            "Section 401 water quality certification",
            "Hydrostatic test water management",
            "Air permit requirements for compression",
            "Edwards Aquifer protection rules",
        ],
        primary_authority=[
            "TPDES Construction General Permit TXR150000",
            "Texas Water Code Chapter 26",
            "30 TAC Chapter 213 (Edwards Aquifer Rules)",
            "30 TAC Chapter 116 (Air Permits)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="TCEQ requires enhanced erosion controls or limits hydrostatic test water discharge.",
        counter_arguments=[
            "SW3P addresses all potential pollutant sources with appropriate BMPs",
            "Hydrostatic test water will be filtered and tested before discharge",
            "Project design minimizes disturbance within sensitive areas",
        ],
        resolution_strategy=(
            "File NOI for TPDES construction general permit before construction begins. Develop comprehensive "
            "SW3P with site-specific BMPs. Plan hydrostatic test water management early. Engage TCEQ on "
            "Edwards Aquifer compliance if applicable."
        ),
        entity_scope="Pipeline companies, TCEQ, construction contractors, environmental consultants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established state permit framework with clear requirements",
        controlling_precedent="TPDES Construction General Permit TXR150000 conditions",
    ),

    DoctrineBlock(
        topic="ferc_eminent_domain_federal_court",
        category=IssueCategory.EMINENT_DOMAIN,
        keywords=["ferc", "eminent domain", "federal court", "section 7h", "nga", "quick take", "certificate"],
        conclusion_template=(
            "FERC certificate holders exercise eminent domain under 15 USC 717f(h) in federal district "
            "court. Upon filing and depositing estimated compensation, the pipeline company may obtain "
            "immediate possession. The landowner retains the right to contest compensation but cannot "
            "challenge the taking itself once FERC has issued a valid certificate."
        ),
        reasoning_framework=(
            "Step 1: Obtain FERC Section 7 certificate with eminent domain authorization. Step 2: Attempt "
            "good-faith negotiation with each affected landowner. Document all offers and contacts. Step 3: "
            "If negotiation fails, file condemnation complaint in federal district court. Step 4: Move for "
            "immediate possession by depositing estimated just compensation with the court. Step 5: Court "
            "grants possession upon finding valid certificate and deposit of estimated compensation. Step 6: "
            "Compensation is determined by jury trial or bench trial. Step 7: Landowner may withdraw "
            "deposited amount without prejudice to claim for additional compensation."
        ),
        key_factors=[
            "Valid FERC certificate with eminent domain authority",
            "Good-faith negotiation documentation",
            "Federal court jurisdiction and venue",
            "Deposit for immediate possession",
            "Just compensation determination process",
            "Landowner withdrawal rights",
        ],
        primary_authority=[
            "15 USC 717f(h) (NGA Eminent Domain Authority)",
            "Fed. R. Civ. P. 71.1 (Condemnation Proceedings)",
            "Transwestern Pipeline Co. v. 17.19 Acres, 550 F.3d 770 (9th Cir. 2008)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="Landowner challenges certificate validity, seeks to delay possession, demands maximum compensation.",
        counter_arguments=[
            "FERC certificate is subject to judicial review only in Court of Appeals, not district court",
            "NGA provides right to immediate possession upon deposit",
            "Compensation will be determined by trier of fact based on evidence",
        ],
        resolution_strategy=(
            "Document good-faith negotiation efforts thoroughly. File condemnation promptly when negotiation "
            "is at impasse. Move for immediate possession with adequate deposit. Prepare strong valuation "
            "evidence for compensation trial."
        ),
        entity_scope="Interstate pipeline companies, federal courts, landowners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Federal NGA eminent domain authority well-established",
        controlling_precedent="15 USC 717f(h); East Tennessee Natural Gas v. Sage, 361 F.3d 808 (4th Cir. 2004)",
    ),

    DoctrineBlock(
        topic="blm_federal_land_row_grant",
        category=IssueCategory.ROW_ACQUISITION,
        keywords=["blm", "federal land", "right-of-way", "grant", "mineral leasing act", "flpma", "public land"],
        conclusion_template=(
            "Pipeline ROW across federal lands managed by BLM requires a right-of-way grant under FLPMA "
            "Title V or the Mineral Leasing Act. BLM evaluates environmental impacts under NEPA, assesses "
            "rental fees, and imposes construction and operation stipulations."
        ),
        reasoning_framework=(
            "Step 1: File SF-299 application with BLM field office. Step 2: BLM assigns cost recovery for "
            "processing (applicant pays). Step 3: Environmental review under NEPA - categorical exclusion, "
            "EA, or EIS depending on project scope. Step 4: BLM evaluates consistency with Resource "
            "Management Plan for the area. Step 5: BLM issues ROW grant with terms and conditions including "
            "width, construction stipulations, bonding, and annual rental. Step 6: Annual rental based on "
            "BLM linear ROW schedule. Step 7: Grant holder must maintain compliance with all stipulations "
            "and report annually."
        ),
        key_factors=[
            "SF-299 application and cost recovery",
            "NEPA environmental review scope",
            "Resource Management Plan consistency",
            "ROW grant terms and stipulations",
            "Annual rental fee schedule",
            "Bonding and insurance requirements",
        ],
        primary_authority=[
            "Federal Land Policy and Management Act Title V, 43 USC 1761-1771",
            "Mineral Leasing Act Section 28, 30 USC 185",
            "43 CFR Part 2880 (BLM ROW Regulations)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="BLM requires extensive environmental review or imposes restrictive construction stipulations.",
        counter_arguments=[
            "Pipeline is consistent with Resource Management Plan and multiple use mandate",
            "Environmental impacts are mitigable through standard construction practices",
            "Pipeline provides public benefit through energy transportation",
        ],
        resolution_strategy=(
            "File application early as BLM processing takes 12-24 months. Engage BLM field office at "
            "pre-application stage. Support NEPA review with complete resource reports. Comply with all "
            "stipulations and maintain annual reporting."
        ),
        entity_scope="Pipeline companies, BLM, DOI, environmental consultants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established federal ROW grant process with clear regulations",
        controlling_precedent="43 CFR Part 2880 BLM ROW regulations",
    ),

    DoctrineBlock(
        topic="water_crossing_hdd_design",
        category=IssueCategory.CROSSING_PERMITS,
        keywords=["water", "crossing", "hdd", "horizontal directional drilling", "river", "creek", "design", "frac-out"],
        conclusion_template=(
            "HDD is the preferred method for major waterway crossings to avoid stream disturbance. Design "
            "must account for pipe diameter, crossing length, soil conditions, entry/exit angles, and "
            "frac-out risk. A frac-out contingency plan and inadvertent return plan are required for "
            "all HDD crossings of waterways."
        ),
        reasoning_framework=(
            "Step 1: Conduct geotechnical investigation along the proposed HDD path to characterize soil "
            "and rock conditions. Step 2: Design HDD profile with entry angle (8-12 degrees), minimum depth "
            "below waterway (typically 25-50 feet below deepest scour point), and exit angle. Step 3: Select "
            "appropriate pilot hole and reaming equipment based on crossing length and pipe diameter. Step 4: "
            "Prepare drilling fluid management plan - closed-loop system preferred. Step 5: Develop frac-out "
            "contingency plan - monitoring locations, response procedures, containment and cleanup. Step 6: "
            "Prepare inadvertent return plan per USACE permit conditions. Step 7: Execute HDD with real-time "
            "tracking and pressure monitoring. Step 8: Hydrostatic test completed crossing."
        ),
        key_factors=[
            "Geotechnical conditions along HDD path",
            "Crossing length and pipe diameter",
            "Minimum depth below scour point",
            "Frac-out risk assessment and contingency",
            "Drilling fluid management and disposal",
            "Real-time tracking and monitoring",
        ],
        primary_authority=[
            "FERC Wetland and Waterbody Construction and Mitigation Procedures",
            "USACE NWP 12 HDD conditions",
            "API RP 1108 (Pipeline Construction by HDD)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="Regulatory agency requires minimum 50-foot depth below waterway, increasing HDD cost significantly.",
        counter_arguments=[
            "HDD design depth accounts for maximum scour with safety factor",
            "Geotechnical data supports shallower profile in competent formation",
            "Industry standard design criteria ensure adequate depth of cover",
        ],
        resolution_strategy=(
            "Invest in thorough geotechnical investigation. Design conservatively with adequate depth. "
            "Have contingency plan for HDD failure including alternative crossing method. Prepare frac-out "
            "response equipment and personnel on-site during drilling."
        ),
        entity_scope="Pipeline companies, HDD contractors, USACE, environmental consultants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Engineering design standards well-established; site conditions variable",
        controlling_precedent="API RP 1108 and FERC waterbody construction procedures",
    ),

    DoctrineBlock(
        topic="pipeline_integrity_management_hca",
        category=IssueCategory.PIPELINE_SAFETY,
        keywords=["integrity", "management", "hca", "high consequence area", "assessment", "ili", "pressure test"],
        conclusion_template=(
            "Pipeline integrity management programs are required for transmission pipelines that could "
            "affect high consequence areas (HCAs). Operators must identify HCAs, assess pipeline segments "
            "using ILI, pressure testing, or direct assessment, and remediate identified anomalies within "
            "prescribed timeframes."
        ),
        reasoning_framework=(
            "Step 1: Identify HCAs along the pipeline using the cluster, potential impact, or prescribed "
            "methodology per 49 CFR 192.903-905. HCAs include populated areas, drinking water sources, "
            "and unusually sensitive areas. Step 2: Develop baseline assessment plan with prioritized "
            "segments. Step 3: Perform integrity assessment using one of three methods: inline inspection "
            "(ILI/smart pig), pressure testing, or direct assessment (ECDA, ICDA, SCCDA). Step 4: Evaluate "
            "assessment results and classify anomalies. Step 5: Remediate immediate conditions within "
            "required timeframes - immediate (upon discovery), 60-day, and 180-day conditions per 49 CFR "
            "192.933. Step 6: Establish reassessment intervals not exceeding 7 years (10 years for certain "
            "confirmed assessments). Step 7: Maintain records and report per 49 CFR 192 Subpart O."
        ),
        key_factors=[
            "HCA identification methodology",
            "Assessment method selection (ILI, pressure test, direct assessment)",
            "Anomaly classification and repair criteria",
            "Remediation timeframe requirements",
            "Reassessment interval compliance",
            "Preventive and mitigative measures",
        ],
        primary_authority=[
            "49 CFR 192 Subpart O (Gas Transmission Pipeline Integrity Management)",
            "49 CFR 195.452 (Hazardous Liquid Pipeline Integrity Management)",
            "ASME B31.8S (Managing System Integrity of Gas Pipelines)",
            "API 1160 (Managing System Integrity for Hazardous Liquid Pipelines)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="PHMSA finds inadequate integrity assessment coverage or untimely anomaly remediation.",
        counter_arguments=[
            "Comprehensive IMP covers all HCA segments per required schedule",
            "Assessment results demonstrate pipeline integrity within design limits",
            "All identified anomalies remediated within regulatory timeframes",
        ],
        resolution_strategy=(
            "Maintain comprehensive IMP with documented procedures. Prioritize HCA assessments. Use ILI "
            "as primary assessment method where pipeline is piggable. Remediate all conditions within "
            "required timeframes. Document everything for regulatory review."
        ),
        entity_scope="Pipeline operators, PHMSA, ILI vendors, integrity engineers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Federal regulations with prescriptive requirements and clear deadlines",
        controlling_precedent="49 CFR 192 Subpart O and 195.452 integrity management rules",
    ),

    DoctrineBlock(
        topic="one_call_damage_prevention",
        category=IssueCategory.PIPELINE_SAFETY,
        keywords=["one-call", "damage prevention", "811", "excavation", "locate", "mark", "third party damage"],
        conclusion_template=(
            "One-call damage prevention programs are mandatory under 49 CFR 192.614 and state law (Texas "
            "Underground Facility Damage Prevention and Safety Act). Pipeline operators must participate "
            "in the state one-call system, respond to locate requests within required timeframes, and "
            "accurately mark pipeline locations."
        ),
        reasoning_framework=(
            "Step 1: Register all pipelines with Texas 811 one-call system. Step 2: Respond to locate "
            "requests within 48 hours (2 business days) per Texas law. Step 3: Accurately mark pipeline "
            "centerline and approximate corridor width using APWA color standards (yellow for gas, oil, "
            "steam). Step 4: Monitor excavation activity near pipelines. Step 5: If third-party damage "
            "occurs, respond immediately, secure the area, and report per applicable regulations. Step 6: "
            "Investigate root cause and pursue damage claim against responsible party. Step 7: Report "
            "incidents to PHMSA per 49 CFR 191 (gas) or 195.50 (hazardous liquid)."
        ),
        key_factors=[
            "One-call system registration and participation",
            "Locate response time requirements",
            "Marking accuracy and APWA standards",
            "Excavation monitoring protocols",
            "Third-party damage response procedures",
            "Incident reporting requirements",
        ],
        primary_authority=[
            "49 CFR 192.614 (Damage Prevention Program)",
            "Texas Utilities Code Chapter 251 (Underground Facility Damage Prevention)",
            "PHMSA Damage Prevention Guidance",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="Excavator claims pipeline was not properly marked, causing third-party damage incident.",
        counter_arguments=[
            "Locate request received and responded to within required timeframe",
            "Pipeline marked accurately per GPS coordinates and as-built records",
            "Excavator failed to observe and protect located facilities per state law",
        ],
        resolution_strategy=(
            "Maintain GPS-accurate pipeline location data. Respond to all locate requests within 48 hours. "
            "Use qualified locators with modern equipment. Document all locate activities. Pursue damage "
            "claims aggressively for negligent excavation."
        ),
        entity_scope="Pipeline operators, excavators, Texas 811, PHMSA",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statutory framework clear; damage liability is fact-specific",
        controlling_precedent="Texas Utilities Code Chapter 251; 49 CFR 192.614",
    ),

    DoctrineBlock(
        topic="eminent_domain_bona_fide_offer",
        category=IssueCategory.EMINENT_DOMAIN,
        keywords=["bona fide", "offer", "initial", "landowner", "bill of rights", "appraisal", "property code 21"],
        conclusion_template=(
            "Texas Property Code 21.0113 requires a bona fide offer before initiating condemnation. The "
            "offer must be in writing, include a copy of the landowner's bill of rights, disclose the "
            "appraisal, and allow a minimum 30-day negotiation period. Failure to make a proper bona fide "
            "offer is grounds for dismissal of the condemnation petition."
        ),
        reasoning_framework=(
            "Step 1: Obtain independent appraisal of the easement value and damages. Step 2: Prepare "
            "written bona fide offer including: offer amount, property description, easement terms, copy "
            "of appraisal, and Landowner's Bill of Rights per Government Code 402.031. Step 3: Deliver "
            "offer by certified mail or personal service. Step 4: Allow minimum 30 days for landowner "
            "to accept, reject, or counter-offer. Step 5: Document all negotiation contacts and offers. "
            "Step 6: If agreement not reached after good-faith negotiation, entity may file condemnation "
            "petition. Step 7: Maintain records demonstrating compliance with bona fide offer requirements."
        ),
        key_factors=[
            "Independent appraisal requirement",
            "Written offer with all required disclosures",
            "Landowner's Bill of Rights delivery",
            "30-day minimum negotiation period",
            "Good-faith negotiation documentation",
            "Compliance with Property Code 21.0113",
        ],
        primary_authority=[
            "Texas Property Code Section 21.0113",
            "Texas Government Code Section 402.031 (Landowner's Bill of Rights)",
            "Texas Property Code Chapter 21 (Eminent Domain)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="Landowner argues bona fide offer was deficient - missing bill of rights or inadequate appraisal.",
        counter_arguments=[
            "Offer letter included all required components per Property Code 21.0113",
            "Independent appraiser qualified and appraisal methodology sound",
            "Landowner's Bill of Rights attached to offer per Government Code 402.031",
        ],
        resolution_strategy=(
            "Use standardized bona fide offer letter template that includes all statutory requirements. "
            "Engage qualified independent appraisers. Deliver offer by certified mail with return receipt. "
            "Document the 30-day waiting period. Keep copies of all correspondence."
        ),
        entity_scope="Pipeline companies with eminent domain authority, landowners, appraisers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Statutory requirements are clear and prescriptive",
        controlling_precedent="Texas Property Code Section 21.0113 requirements",
    ),

    DoctrineBlock(
        topic="oil_spill_response_liability",
        category=IssueCategory.PIPELINE_SAFETY,
        keywords=["oil", "spill", "response", "liability", "cleanup", "opa", "cercla", "reportable", "release"],
        conclusion_template=(
            "Pipeline spills and releases trigger federal and state reporting, response, and cleanup "
            "obligations. Operators face strict liability under OPA, CERCLA, and state environmental "
            "statutes. Prompt reporting, containment, and remediation are essential to minimize "
            "liability exposure and regulatory penalties."
        ),
        reasoning_framework=(
            "Step 1: Activate spill response plan immediately upon discovery of release. Step 2: Report "
            "to National Response Center (NRC) for reportable quantities - any discharge to navigable "
            "waters, and releases above CERCLA reportable quantities. Step 3: Report to TCEQ and Railroad "
            "Commission as applicable. Step 4: Deploy containment and recovery equipment per facility "
            "response plan. Step 5: Retain qualified environmental remediation contractor. Step 6: Conduct "
            "site assessment to determine extent of contamination. Step 7: Implement remediation plan "
            "meeting state cleanup standards. Step 8: Pursue cost recovery from responsible third parties "
            "if third-party damage caused the release."
        ),
        key_factors=[
            "Spill detection and initial response time",
            "Federal and state reporting obligations",
            "Containment and recovery effectiveness",
            "Remediation to regulatory cleanup standards",
            "Potential penalties and enforcement",
            "Third-party liability and cost recovery",
        ],
        primary_authority=[
            "Oil Pollution Act of 1990 (33 USC 2701 et seq.)",
            "CERCLA (42 USC 9601 et seq.)",
            "49 CFR 195.50 (Reporting Requirements for Hazardous Liquid Pipelines)",
            "Texas Water Code Chapter 26 (Water Quality)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="Regulatory agency and affected landowners seek maximum cleanup standards and natural resource damages.",
        counter_arguments=[
            "Operator activated response plan immediately and contained release",
            "Remediation meets applicable state risk-based corrective action standards",
            "Operator cooperated fully with regulatory agencies throughout response",
        ],
        resolution_strategy=(
            "Maintain current spill response plans and equipment. Train personnel on response procedures. "
            "Report immediately - never delay. Contain first, then assess. Engage qualified remediation "
            "contractors. Document all response activities for regulatory and litigation record."
        ),
        entity_scope="Pipeline operators, EPA, USCG, TCEQ, RRC, landowners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Strict liability framework with clear response and reporting obligations",
        controlling_precedent="OPA Section 1002 strict liability for pipeline operators",
    ),

    DoctrineBlock(
        topic="construction_timing_seasonal_restrictions",
        category=IssueCategory.ENVIRONMENTAL_PERMITTING,
        keywords=["construction", "timing", "seasonal", "restriction", "migratory bird", "breeding", "window"],
        conclusion_template=(
            "Pipeline construction timing may be restricted by seasonal windows for migratory bird nesting, "
            "endangered species breeding, wetland work, and agricultural operations. FERC certificate "
            "conditions and USACE permits commonly impose timing restrictions that must be incorporated "
            "into construction scheduling."
        ),
        reasoning_framework=(
            "Step 1: Identify all applicable seasonal restrictions from FERC certificate conditions, "
            "USACE permit conditions, USFWS biological opinion terms, and state permits. Step 2: Common "
            "restrictions include: migratory bird nesting (March-August in most areas), listed species "
            "breeding seasons, in-stream work windows for fish spawning, and winter ground-disturbance "
            "restrictions. Step 3: Map restrictions onto project schedule to identify construction windows. "
            "Step 4: Request variances or modifications where restrictions conflict with project timeline. "
            "Step 5: Implement pre-construction surveys (nest surveys, species surveys) to verify restriction "
            "necessity. Step 6: If variance granted, implement alternative mitigation measures."
        ),
        key_factors=[
            "Migratory bird nesting season timing",
            "Listed species breeding window requirements",
            "In-stream work timing restrictions",
            "Agricultural timing coordination",
            "Variance request process and criteria",
            "Pre-construction survey requirements",
        ],
        primary_authority=[
            "Migratory Bird Treaty Act (16 USC 703-712)",
            "FERC Certificate Conditions on construction timing",
            "USFWS Biological Opinion terms and conditions",
            "USACE permit special conditions",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="USFWS insists on full breeding season restriction eliminating 6-month construction window.",
        counter_arguments=[
            "Pre-construction surveys confirm no active nests within project area",
            "Construction activities occur below disturbance threshold for species",
            "Alternative mitigation measures provide equivalent protection",
        ],
        resolution_strategy=(
            "Plan construction schedule around seasonal restrictions from the outset. Conduct pre-construction "
            "species surveys to support variance requests. Request variances early in the process. Build "
            "schedule float for potential weather and restriction delays."
        ),
        entity_scope="Pipeline companies, FERC, USFWS, USACE, construction contractors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Restrictions are mandatory; variance availability depends on site conditions",
        controlling_precedent="MBTA and FERC certificate conditions on construction timing",
    ),

    DoctrineBlock(
        topic="pipeline_marker_requirements",
        category=IssueCategory.PIPELINE_SAFETY,
        keywords=["marker", "sign", "warning", "post", "requirement", "phmsa", "identification", "location"],
        conclusion_template=(
            "PHMSA requires pipeline markers at public road crossings, railroad crossings, navigable "
            "waterway crossings, and at intervals along the ROW where underground pipeline is present. "
            "Markers must display operator name, emergency telephone number, and product transported."
        ),
        reasoning_framework=(
            "Step 1: Install pipeline markers per 49 CFR 192.707 (gas) or 195.410 (hazardous liquid). "
            "Step 2: Required locations: each public road crossing, each railroad crossing, each navigable "
            "waterway crossing, and at other locations to identify the presence of the pipeline where the "
            "pipeline is buried. Step 3: Marker content must include: operator name, emergency telephone "
            "number (usually 811), and product information. Step 4: Marker placement should be visible "
            "and legible from a reasonable distance. Step 5: Maintain markers - replace damaged or missing "
            "markers promptly. Step 6: Additional markers may be required by state regulations or easement "
            "agreements."
        ),
        key_factors=[
            "Required marker locations per PHMSA regulations",
            "Marker content requirements",
            "Visibility and legibility standards",
            "Maintenance and replacement obligations",
            "State and local additional requirements",
            "Landowner preferences on marker placement",
        ],
        primary_authority=[
            "49 CFR 192.707 (Line Markers for Gas Transmission and Distribution)",
            "49 CFR 195.410 (Line Markers for Hazardous Liquid Pipelines)",
            "API RP 1109 (Marking Liquid Petroleum Pipelines)",
        ],
        burden_holder=BurdenHolder.PIPELINE_COMPANY,
        adversary_position="Landowner demands removal of unsightly markers or relocation to less visible positions.",
        counter_arguments=[
            "Pipeline markers are federally mandated safety requirements",
            "Marker removal would violate PHMSA regulations and create safety hazard",
            "Marker placement can be adjusted within reason while maintaining visibility",
        ],
        resolution_strategy=(
            "Install markers per regulatory requirements at all required locations. Coordinate with landowners "
            "on marker placement where flexibility exists. Use low-profile markers in sensitive areas while "
            "maintaining compliance. Maintain marker inventory and replacement schedule."
        ),
        entity_scope="Pipeline operators, PHMSA, landowners",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Federal requirements are non-negotiable",
        controlling_precedent="49 CFR 192.707 and 195.410 marker requirements",
    ),
]


def get_doctrine_cache() -> list[DoctrineBlock]:
    """Return the full doctrine cache."""
    return DOCTRINE_CACHE


def get_doctrine_by_topic(topic: str) -> DoctrineBlock | None:
    """Retrieve a specific doctrine block by topic name."""
    for block in DOCTRINE_CACHE:
        if block.topic == topic:
            return block
    return None


def get_doctrines_by_category(category: IssueCategory) -> list[DoctrineBlock]:
    """Retrieve all doctrine blocks for a given issue category."""
    return [b for b in DOCTRINE_CACHE if b.category == category]


def get_doctrine_topic_keyword_map() -> dict[str, list[str]]:
    """Return a map of topic -> keywords for semantic matching."""
    return {block.topic: block.keywords for block in DOCTRINE_CACHE}


def get_all_topics() -> list[str]:
    """Return all doctrine topic names."""
    return [block.topic for block in DOCTRINE_CACHE]


def get_all_categories() -> list[str]:
    """Return all unique issue categories present in the cache."""
    return list(set(block.category.value for block in DOCTRINE_CACHE))
