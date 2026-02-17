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
        topic="FERC Jurisdiction Over Interstate Transmission",
        keywords=["FERC", "jurisdiction", "interstate", "transmission", "electricity", "Federal Power Act"],
        conclusion_template="FERC has exclusive jurisdiction over the rates, terms, and conditions of interstate transmission of electric energy in the United States.",
        reasoning_framework=(
            "The Federal Power Act (FPA) grants FERC exclusive jurisdiction over the transmission of electric energy in interstate commerce. "
            "The Supreme Court has consistently held that FERC's jurisdiction preempts state regulation where the transmission is interstate in character. "
            "The FPA defines 'transmission of electric energy in interstate commerce' broadly, and FERC's authority extends to setting rates, approving tariffs, and ensuring non-discriminatory access. "
            "State authority is limited to intrastate transmission and distribution. "
            "The 'bright line' test articulated in FERC v. Electric Power Supply Association (EPSA) and New York v. FERC distinguishes between FERC and state jurisdiction. "
            "Where transmission facilities are used for both interstate and intrastate purposes, FERC's jurisdiction prevails for the interstate component."
        ),
        key_factors=[
            "Nature of the transmission (interstate vs. intrastate)",
            "Applicability of the Federal Power Act",
            "Precedent from Supreme Court cases",
            "Tariff filings and FERC orders"
        ],
        primary_authority=[
            "Federal Power Act, 16 U.S.C. § 824",
            "FERC v. Electric Power Supply Association, 577 U.S. 260 (2016)",
            "New York v. FERC, 535 U.S. 1 (2002)"
        ],
        burden_holder="Entity seeking to challenge FERC jurisdiction",
        adversary_position="State regulatory authorities may assert jurisdiction over certain facilities or transactions",
        counter_arguments=[
            "Transmission is local and does not cross state lines",
            "Facilities are used primarily for distribution",
            "State law provides for concurrent jurisdiction"
        ],
        resolution_strategy="Apply the FPA's definitions and relevant Supreme Court precedent; evaluate the functional use of the facilities.",
        entity_scope="Public utilities, transmission owners, RTOs/ISOs",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="New York v. FERC, 535 U.S. 1 (2002)"
    ),
    DoctrineBlock(
        topic="NERC CIP Critical Infrastructure Protection Standards",
        keywords=["NERC", "CIP", "critical infrastructure", "cybersecurity", "compliance", "standards"],
        conclusion_template="Registered entities must comply with NERC CIP standards to ensure the security and reliability of the Bulk Electric System.",
        reasoning_framework=(
            "The North American Electric Reliability Corporation (NERC) develops and enforces Critical Infrastructure Protection (CIP) standards, "
            "which are approved by FERC and are mandatory for entities registered as responsible for Bulk Electric System (BES) assets. "
            "CIP standards address cybersecurity, physical security, and incident response. "
            "Entities must identify and categorize BES Cyber Systems, implement security controls, and maintain compliance documentation. "
            "Violations may result in significant penalties. "
            "FERC oversees NERC's enforcement and may direct modifications to the standards. "
            "Compliance is assessed through audits, spot checks, and self-reporting."
        ),
        key_factors=[
            "Registration status with NERC",
            "Asset categorization and risk assessment",
            "Implementation of security controls",
            "Audit and enforcement history"
        ],
        primary_authority=[
            "16 U.S.C. § 824o",
            "NERC CIP Standards (CIP-002 through CIP-014)",
            "FERC Orders 706, 822"
        ],
        burden_holder="Registered entity",
        adversary_position="NERC or FERC may allege non-compliance or insufficient controls",
        counter_arguments=[
            "Entity does not own/operate BES assets",
            "Controls are commensurate with risk",
            "Mitigation plans are in place"
        ],
        resolution_strategy="Review registration, asset lists, and compliance evidence; engage with NERC/FERC as needed.",
        entity_scope="Transmission owners, operators, generator owners",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FERC Order 706"
    ),
    DoctrineBlock(
        topic="ERCOT Nodal Market Protocols and Settlement",
        keywords=["ERCOT", "nodal market", "settlement", "protocols", "Texas", "energy market"],
        conclusion_template="Market participants must comply with ERCOT Nodal Protocols for participation, scheduling, and settlement in the ERCOT market.",
        reasoning_framework=(
            "ERCOT administers the Texas wholesale electricity market under the Nodal Protocols, which govern market participation, scheduling, dispatch, and settlement. "
            "All Qualified Scheduling Entities (QSEs) and market participants must adhere to these protocols, which are approved by the Public Utility Commission of Texas (PUCT). "
            "Protocols address energy and ancillary service markets, congestion management, and financial settlement. "
            "Compliance is monitored by ERCOT and PUCT, and violations may result in penalties or market suspension. "
            "Disputes are resolved through the ERCOT dispute resolution process or by appeal to the PUCT."
        ),
        key_factors=[
            "Registration as a market participant or QSE",
            "Adherence to scheduling and bidding rules",
            "Settlement accuracy and timeliness",
            "Dispute resolution procedures"
        ],
        primary_authority=[
            "ERCOT Nodal Protocols",
            "PUCT Substantive Rules §25.501 et seq.",
            "Texas Utilities Code, Chapter 39"
        ],
        burden_holder="Market participant",
        adversary_position="ERCOT or other market participants may allege protocol violations or settlement errors",
        counter_arguments=[
            "Protocol ambiguity or conflicting provisions",
            "System or data errors",
            "Force majeure or extenuating circumstances"
        ],
        resolution_strategy="Follow ERCOT dispute process; escalate to PUCT if necessary.",
        entity_scope="QSEs, market participants, ERCOT",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 31540 (ERCOT Nodal Market Implementation)"
    ),
    DoctrineBlock(
        topic="FERC Market-Based Rate Authority and Mitigation",
        keywords=["FERC", "market-based rates", "mitigation", "power sales", "electricity", "market power"],
        conclusion_template="Entities must obtain FERC market-based rate authority and are subject to ongoing market power mitigation requirements.",
        reasoning_framework=(
            "FERC grants market-based rate (MBR) authority to sellers of wholesale electricity if they demonstrate a lack of market power or adequate mitigation. "
            "Applicants must file an MBR application, including market power screens and asset disclosures. "
            "FERC may revoke MBR authority if market power is detected or mitigation is insufficient. "
            "Sellers are subject to ongoing reporting, affiliate restrictions, and must comply with FERC's anti-manipulation rules. "
            "Periodic triennial reviews and change-in-status filings are required."
        ),
        key_factors=[
            "Market power analysis (pivotal supplier, market share screens)",
            "Mitigation measures (must-offer, price caps)",
            "Ongoing compliance and reporting",
            "Affiliate restrictions"
        ],
        primary_authority=[
            "Federal Power Act, 16 U.S.C. § 824d",
            "FERC Orders 697, 816",
            "18 C.F.R. Part 35"
        ],
        burden_holder="Seller seeking MBR authority",
        adversary_position="FERC or intervenors may allege market power or non-compliance",
        counter_arguments=[
            "Market is sufficiently competitive",
            "Mitigation measures are effective",
            "No evidence of affiliate abuse"
        ],
        resolution_strategy="Submit robust market power analysis and comply with all FERC requirements.",
        entity_scope="Wholesale power sellers, generation owners",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FERC Order 697"
    ),
    DoctrineBlock(
        topic="FERC Section 205 Rate Filing Requirements",
        keywords=["FERC", "Section 205", "rate filing", "tariff", "public utility", "cost recovery"],
        conclusion_template="Public utilities must file proposed rates, terms, and conditions for FERC approval under Section 205 of the Federal Power Act.",
        reasoning_framework=(
            "Section 205 of the Federal Power Act requires public utilities to file all rates, charges, and terms of service with FERC before they become effective. "
            "FERC reviews filings to ensure rates are just and reasonable and not unduly discriminatory. "
            "Utilities must provide cost support, testimony, and notice to affected parties. "
            "FERC may suspend, modify, or reject filings and may set matters for hearing. "
            "Intervenors may protest filings, and FERC's review is subject to judicial review."
        ),
        key_factors=[
            "Completeness of filing (tariff, cost support, testimony)",
            "Notice to affected parties",
            "Just and reasonable standard",
            "Procedural compliance"
        ],
        primary_authority=[
            "Federal Power Act, 16 U.S.C. § 824d",
            "18 C.F.R. Part 35",
            "FERC Orders 888, 2001"
        ],
        burden_holder="Public utility making the filing",
        adversary_position="Intervenors may allege rates are unjust, unreasonable, or discriminatory",
        counter_arguments=[
            "Rates reflect prudent costs",
            "No undue discrimination",
            "Filing meets all procedural requirements"
        ],
        resolution_strategy="Ensure complete and well-supported filings; respond to protests and FERC data requests.",
        entity_scope="Public utilities, transmission owners",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FERC Order 888"
    ),
    DoctrineBlock(
        topic="Natural Gas Pipeline Certificate Authority Under NGA Section 7",
        keywords=["natural gas", "pipeline", "certificate", "NGA", "Section 7", "FERC"],
        conclusion_template="Pipeline developers must obtain a FERC certificate of public convenience and necessity under NGA Section 7 before constructing or operating interstate pipelines.",
        reasoning_framework=(
            "The Natural Gas Act (NGA) Section 7 requires that no natural gas company may construct or operate an interstate pipeline without a certificate of public convenience and necessity from FERC. "
            "Applicants must demonstrate need, environmental compliance, and market support. "
            "FERC evaluates applications under the public interest standard, considering impacts on landowners, communities, and markets. "
            "Opponents may intervene and raise environmental or market concerns. "
            "FERC's certificate confers eminent domain authority for pipeline construction."
        ),
        key_factors=[
            "Demonstration of public need",
            "Environmental review (NEPA compliance)",
            "Market support and contracts",
            "Stakeholder and landowner impacts"
        ],
        primary_authority=[
            "Natural Gas Act, 15 U.S.C. § 717f",
            "FERC Certificate Policy Statement (1999)",
            "18 C.F.R. Part 157"
        ],
        burden_holder="Pipeline developer",
        adversary_position="Landowners, environmental groups, or competitors may challenge need or impacts",
        counter_arguments=[
            "Project is necessary for reliability or market access",
            "Environmental impacts are mitigated",
            "Alternatives are less feasible"
        ],
        resolution_strategy="Prepare comprehensive application and engage stakeholders early.",
        entity_scope="Natural gas companies, pipeline developers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Certificate Policy Statement (1999)"
    ),
    DoctrineBlock(
        topic="Pipeline Safety Regulations 49 CFR 192 and 195",
        keywords=["pipeline", "safety", "PHMSA", "49 CFR 192", "49 CFR 195", "compliance"],
        conclusion_template="Operators must comply with PHMSA safety regulations for natural gas (49 CFR 192) and hazardous liquid (49 CFR 195) pipelines.",
        reasoning_framework=(
            "The Pipeline and Hazardous Materials Safety Administration (PHMSA) enforces safety regulations for natural gas pipelines (49 CFR 192) and hazardous liquid pipelines (49 CFR 195). "
            "Operators must develop and implement integrity management programs, conduct regular inspections, and maintain records. "
            "PHMSA conducts audits and may impose civil penalties for violations. "
            "State pipeline safety agencies may also enforce these regulations under certification from PHMSA."
        ),
        key_factors=[
            "Applicability of regulations to pipeline type",
            "Integrity management and inspection records",
            "Incident reporting and response",
            "PHMSA or state audit findings"
        ],
        primary_authority=[
            "49 CFR Part 192",
            "49 CFR Part 195",
            "Pipeline Safety Act, 49 U.S.C. § 60101 et seq."
        ],
        burden_holder="Pipeline operator",
        adversary_position="PHMSA or state agencies may allege non-compliance",
        counter_arguments=[
            "Compliance with all applicable requirements",
            "Corrective actions taken promptly",
            "Records demonstrate safety culture"
        ],
        resolution_strategy="Maintain robust compliance programs and documentation.",
        entity_scope="Pipeline operators, owners",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="PHMSA Interpretive Guidance"
    ),
    DoctrineBlock(
        topic="PUCT Ratemaking for Texas Electric Utilities",
        keywords=["PUCT", "ratemaking", "Texas", "electric utilities", "cost recovery", "rate case"],
        conclusion_template="Texas electric utilities must obtain PUCT approval for rates, demonstrating that rates are just and reasonable and based on prudent costs.",
        reasoning_framework=(
            "The Public Utility Commission of Texas (PUCT) regulates rates for investor-owned electric utilities. "
            "Utilities must file rate cases, providing cost-of-service studies, testimony, and supporting data. "
            "PUCT applies a just and reasonable standard, considering prudence, used and useful assets, and customer impacts. "
            "Intervenors may challenge cost recovery, return on equity, or allocation methods. "
            "PUCT decisions are subject to judicial review in Texas courts."
        ),
        key_factors=[
            "Prudence of costs",
            "Used and useful standard",
            "Return on equity",
            "Customer and intervenor positions"
        ],
        primary_authority=[
            "Texas Utilities Code, Chapter 36",
            "PUCT Substantive Rules §25.231",
            "PUCT Docket precedent"
        ],
        burden_holder="Utility seeking rate increase",
        adversary_position="PUCT staff or intervenors may dispute costs or rate design",
        counter_arguments=[
            "Costs are prudent and necessary",
            "Rate design is equitable",
            "Customer impacts are mitigated"
        ],
        resolution_strategy="Prepare thorough rate case and engage stakeholders.",
        entity_scope="Investor-owned utilities, PUCT",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 43695"
    ),
    DoctrineBlock(
        topic="Renewable Portfolio Standards and REC Compliance",
        keywords=["renewable portfolio standard", "RPS", "REC", "compliance", "state law", "renewable energy"],
        conclusion_template="Load-serving entities must comply with state Renewable Portfolio Standards by procuring and retiring sufficient Renewable Energy Credits (RECs).",
        reasoning_framework=(
            "Many states require load-serving entities (LSEs) to meet Renewable Portfolio Standards (RPS) by procuring renewable energy or RECs. "
            "Compliance is tracked through REC registries, and shortfalls may result in alternative compliance payments or penalties. "
            "LSEs must demonstrate compliance through annual filings and may trade RECs to meet obligations. "
            "State public utility commissions enforce RPS requirements and may audit compliance."
        ),
        key_factors=[
            "State RPS requirements and targets",
            "REC procurement and retirement records",
            "Alternative compliance mechanisms",
            "Regulatory filings and audits"
        ],
        primary_authority=[
            "State RPS statutes (e.g., Texas Utilities Code §39.904)",
            "PUCT Substantive Rules §25.173",
            "REC registry rules"
        ],
        burden_holder="Load-serving entity",
        adversary_position="State commission may allege non-compliance or insufficient REC retirement",
        counter_arguments=[
            "Sufficient RECs procured and retired",
            "Alternative compliance payments made",
            "Force majeure or regulatory changes"
        ],
        resolution_strategy="Maintain accurate REC records and monitor state RPS changes.",
        entity_scope="LSEs, utilities, competitive retailers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 41061"
    ),
    DoctrineBlock(
        topic="FERC Anti-Manipulation Rule and Market Behavior",
        keywords=["FERC", "anti-manipulation", "market behavior", "prohibition", "enforcement", "193.222"],
        conclusion_template="Market participants are prohibited from engaging in manipulative or deceptive practices in FERC-jurisdictional markets.",
        reasoning_framework=(
            "FERC's Anti-Manipulation Rule (18 C.F.R. § 1c.2) prohibits the use of any manipulative or deceptive device or contrivance in connection with the purchase or sale of electric energy or transmission services subject to FERC jurisdiction. "
            "The rule is modeled after Section 10(b) of the Securities Exchange Act and is interpreted broadly. "
            "FERC investigates and enforces violations through civil penalties, disgorgement, and market bans. "
            "Market participants must maintain compliance programs and monitor trading activity. "
            "Intent to manipulate is not required; recklessness may suffice."
        ),
        key_factors=[
            "Nature of the conduct (intentional, reckless, or negligent)",
            "Market impact",
            "Internal compliance controls",
            "FERC enforcement history"
        ],
        primary_authority=[
            "Federal Power Act, 16 U.S.C. § 824v",
            "18 C.F.R. § 1c.2",
            "FERC Orders 670, 784"
        ],
        burden_holder="FERC in enforcement proceedings",
        adversary_position="Market participant may argue conduct was legitimate or not manipulative",
        counter_arguments=[
            "Trading was consistent with market rules",
            "No intent or recklessness",
            "No market harm"
        ],
        resolution_strategy="Maintain robust compliance and respond promptly to FERC inquiries.",
        entity_scope="Market participants, traders, utilities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FERC Order 670"
    ),
    DoctrineBlock(
        topic="Large Generator Interconnection Process",
        keywords=["generator interconnection", "FERC", "LGIA", "transmission", "queue", "study process"],
        conclusion_template="Large generators must follow FERC's pro forma interconnection process, including studies and agreements, to connect to the transmission grid.",
        reasoning_framework=(
            "FERC's pro forma Large Generator Interconnection Procedures (LGIP) and Agreement (LGIA) establish the process for generators >20 MW to interconnect with the transmission system. "
            "Applicants enter the interconnection queue, undergo feasibility, system impact, and facilities studies, and negotiate an LGIA. "
            "Transmission providers must process requests in a non-discriminatory manner. "
            "Disputes may be resolved through FERC's dispute resolution process or complaint procedures."
        ),
        key_factors=[
            "Queue position and timeliness",
            "Study results and cost allocation",
            "LGIA negotiation and execution",
            "Transmission provider compliance"
        ],
        primary_authority=[
            "FERC Orders 2003, 845",
            "18 C.F.R. § 35.28",
            "Pro forma LGIP/LGIA"
        ],
        burden_holder="Generator seeking interconnection",
        adversary_position="Transmission provider may delay or impose unreasonable requirements",
        counter_arguments=[
            "Studies are complete and accurate",
            "Cost allocation is consistent with FERC policy",
            "No undue discrimination"
        ],
        resolution_strategy="Follow LGIP process and escalate disputes to FERC as needed.",
        entity_scope="Large generators, transmission providers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FERC Order 2003"
    ),
    DoctrineBlock(
        topic="FERC Reliability Coordinator and Balancing Authority Registration",
        keywords=["FERC", "reliability coordinator", "balancing authority", "NERC", "registration", "compliance"],
        conclusion_template="Entities performing reliability coordinator or balancing authority functions must register with NERC and comply with applicable reliability standards.",
        reasoning_framework=(
            "Entities that operate the Bulk Electric System as reliability coordinators or balancing authorities must register with NERC and comply with applicable reliability standards. "
            "Registration triggers obligations for operational planning, real-time monitoring, and event reporting. "
            "NERC and FERC oversee compliance, and violations may result in penalties. "
            "Entities may be subject to audits and must maintain documentation of compliance."
        ),
        key_factors=[
            "Functional role in BES operations",
            "Registration status with NERC",
            "Compliance with reliability standards",
            "Audit and enforcement history"
        ],
        primary_authority=[
            "16 U.S.C. § 824o",
            "NERC Functional Model",
            "NERC Reliability Standards"
        ],
        burden_holder="Entity performing reliability function",
        adversary_position="NERC/FERC may allege non-compliance or failure to register",
        counter_arguments=[
            "Entity does not perform triggering functions",
            "All standards are met",
            "Mitigation plans are in place"
        ],
        resolution_strategy="Review functional roles and ensure registration and compliance.",
        entity_scope="Reliability coordinators, balancing authorities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NERC Registration Criteria"
    ),
    DoctrineBlock(
        topic="Texas Transmission Cost Recovery Factor (TCCRF)",
        keywords=["Texas", "transmission", "cost recovery", "TCCRF", "PUCT", "rate adjustment"],
        conclusion_template="Texas electric utilities may recover transmission cost increases through the TCCRF mechanism, subject to PUCT approval.",
        reasoning_framework=(
            "The Transmission Cost Recovery Factor (TCCRF) allows Texas electric utilities to adjust rates to recover changes in transmission costs between base rate cases. "
            "Utilities must file TCCRF applications with supporting data, and PUCT reviews for prudence and compliance with rules. "
            "TCCRF adjustments are subject to reconciliation in future rate cases. "
            "Intervenors may challenge the prudence or allocation of costs."
        ),
        key_factors=[
            "Eligibility of transmission costs",
            "Supporting documentation",
            "Compliance with PUCT rules",
            "Customer impact"
        ],
        primary_authority=[
            "PUCT Substantive Rules §25.193",
            "Texas Utilities Code §36.209",
            "PUCT Docket precedent"
        ],
        burden_holder="Utility seeking TCCRF adjustment",
        adversary_position="PUCT staff or intervenors may dispute cost eligibility or allocation",
        counter_arguments=[
            "Costs are prudent and necessary",
            "Allocation is consistent with rules",
            "Customer impacts are reasonable"
        ],
        resolution_strategy="Prepare robust application and respond to PUCT inquiries.",
        entity_scope="Texas electric utilities, PUCT",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 48551"
    ),
    DoctrineBlock(
        topic="FERC Demand Response Compensation Order 745",
        keywords=["FERC", "demand response", "Order 745", "compensation", "wholesale market"],
        conclusion_template="Demand response resources must be compensated at the market price for energy if they meet FERC's net benefits test.",
        reasoning_framework=(
            "FERC Order 745 requires that demand response resources participating in organized wholesale energy markets be compensated at the market price for energy (LMP) if they provide net benefits to the market. "
            "The net benefits test ensures that demand response lowers the overall cost of electricity. "
            "RTOs/ISOs must implement measurement and verification protocols. "
            "Order 745 was upheld by the Supreme Court in FERC v. EPSA, affirming FERC's jurisdiction over demand response in wholesale markets."
        ),
        key_factors=[
            "Participation in organized wholesale market",
            "Net benefits test results",
            "Measurement and verification protocols",
            "Market rules compliance"
        ],
        primary_authority=[
            "FERC Order 745",
            "FERC v. EPSA, 577 U.S. 260 (2016)",
            "18 C.F.R. § 35.28"
        ],
        burden_holder="Demand response provider",
        adversary_position="Market operator or other participants may dispute eligibility or compensation",
        counter_arguments=[
            "Resource provides net benefits",
            "Measurement and verification are accurate",
            "Participation is consistent with market rules"
        ],
        resolution_strategy="Demonstrate compliance with Order 745 and market protocols.",
        entity_scope="Demand response providers, RTOs/ISOs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FERC v. EPSA, 577 U.S. 260 (2016)"
    ),
    DoctrineBlock(
        topic="Environmental Compliance for Generation Facilities",
        keywords=["environmental compliance", "generation", "air permits", "water permits", "EPA", "state agencies"],
        conclusion_template="Generation facilities must obtain and comply with all applicable environmental permits and standards.",
        reasoning_framework=(
            "Electric generation facilities are subject to a range of environmental regulations, including air emissions (Clean Air Act), water discharges (Clean Water Act), and waste management. "
            "Facilities must obtain permits from EPA or state agencies, comply with emission limits, and conduct monitoring and reporting. "
            "Non-compliance may result in enforcement actions, penalties, or permit revocation. "
            "State and federal requirements may overlap, and facilities must ensure compliance with both."
        ),
        key_factors=[
            "Type and size of generation facility",
            "Applicable federal and state permits",
            "Monitoring and reporting records",
            "Enforcement history"
        ],
        primary_authority=[
            "Clean Air Act, 42 U.S.C. § 7401 et seq.",
            "Clean Water Act, 33 U.S.C. § 1251 et seq.",
            "State environmental statutes"
        ],
        burden_holder="Generation facility owner/operator",
        adversary_position="EPA or state agencies may allege non-compliance",
        counter_arguments=[
            "All permits obtained and complied with",
            "Monitoring records are accurate",
            "Corrective actions taken promptly"
        ],
        resolution_strategy="Maintain robust environmental compliance programs and documentation.",
        entity_scope="Generation owners/operators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="EPA Enforcement Policy"
    ),
    DoctrineBlock(
        topic="FERC Open Access Transmission Tariff (OATT) Administration",
        keywords=["FERC", "OATT", "open access", "transmission", "tariff", "non-discrimination"],
        conclusion_template="Transmission providers must administer OATTs to ensure non-discriminatory access to transmission service.",
        reasoning_framework=(
            "FERC requires all public utilities that own, control, or operate transmission facilities to file and administer an Open Access Transmission Tariff (OATT). "
            "The OATT sets forth the terms and conditions for providing transmission service on a non-discriminatory basis. "
            "Transmission providers must process requests for service fairly, post available capacity, and comply with FERC standards of conduct. "
            "Disputes may be resolved through FERC's complaint process."
        ),
        key_factors=[
            "OATT compliance and administration",
            "Transmission service requests and queue management",
            "Transparency and posting requirements",
            "Standards of conduct"
        ],
        primary_authority=[
            "Federal Power Act, 16 U.S.C. § 824d",
            "FERC Orders 888, 890",
            "18 C.F.R. Part 37"
        ],
        burden_holder="Transmission provider",
        adversary_position="Customers may allege discrimination or OATT violations",
        counter_arguments=[
            "All requests processed fairly",
            "No undue discrimination",
            "OATT terms followed"
        ],
        resolution_strategy="Maintain robust OATT compliance and respond to FERC complaints.",
        entity_scope="Transmission providers, customers",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FERC Order 888"
    ),
    DoctrineBlock(
        topic="State Renewable Energy Siting and Permitting",
        keywords=["state", "renewable energy", "siting", "permitting", "local government", "land use"],
        conclusion_template="Renewable energy projects must obtain all required state and local permits for siting, construction, and operation.",
        reasoning_framework=(
            "State and local governments regulate the siting and permitting of renewable energy projects, including wind, solar, and storage. "
            "Developers must comply with zoning, land use, environmental, and construction permitting requirements. "
            "Public notice and stakeholder engagement are often required. "
            "Failure to obtain permits may result in project delays or enforcement actions."
        ),
        key_factors=[
            "State and local permitting requirements",
            "Zoning and land use compatibility",
            "Environmental impact assessments",
            "Public notice and opposition"
        ],
        primary_authority=[
            "State siting statutes (e.g., Texas Utilities Code §35.152)",
            "Local zoning ordinances",
            "Environmental review statutes"
        ],
        burden_holder="Project developer",
        adversary_position="Local governments or community groups may oppose siting",
        counter_arguments=[
            "Project complies with all requirements",
            "Community benefits are significant",
            "Mitigation measures are in place"
        ],
        resolution_strategy="Engage stakeholders early and address concerns in permitting process.",
        entity_scope="Renewable project developers, local governments",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Texas PUC Docket No. 37944"
    ),
    DoctrineBlock(
        topic="Electric Reliability Council (ERCOT) Governance and Oversight",
        keywords=["ERCOT", "governance", "oversight", "PUCT", "board", "market rules"],
        conclusion_template="ERCOT is governed by a board subject to PUCT oversight and must administer market rules transparently and impartially.",
        reasoning_framework=(
            "ERCOT's governance structure is established by Texas law and PUCT rules. "
            "The ERCOT board is responsible for market administration, reliability, and compliance with PUCT directives. "
            "PUCT oversees ERCOT's budget, protocols, and major decisions. "
            "Stakeholders may participate in protocol revision processes. "
            "Transparency and impartiality are required by statute and rule."
        ),
        key_factors=[
            "Board composition and independence",
            "PUCT oversight and directives",
            "Stakeholder engagement",
            "Transparency in decision-making"
        ],
        primary_authority=[
            "Texas Utilities Code §39.151",
            "PUCT Substantive Rules §25.362",
            "ERCOT Bylaws"
        ],
        burden_holder="ERCOT",
        adversary_position="Market participants may allege lack of transparency or impartiality",
        counter_arguments=[
            "Board and staff act independently",
            "All processes are transparent",
            "Stakeholder input is considered"
        ],
        resolution_strategy="Follow PUCT directives and maintain open stakeholder processes.",
        entity_scope="ERCOT, PUCT, market participants",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Texas Utilities Code §39.151"
    ),
    DoctrineBlock(
        topic="Tax Treatment of Renewable Energy Tax Credits",
        keywords=["tax", "renewable energy", "PTC", "ITC", "tax credits", "IRS"],
        conclusion_template="Renewable energy project owners must comply with IRS rules for claiming and monetizing production and investment tax credits.",
        reasoning_framework=(
            "The Internal Revenue Code provides for the Production Tax Credit (PTC) and Investment Tax Credit (ITC) for qualifying renewable energy projects. "
            "Project owners must meet eligibility criteria, including placed-in-service dates and ownership requirements. "
            "Tax credits may be monetized through tax equity structures. "
            "IRS guidance and private letter rulings provide interpretive authority. "
            "Improper claims may result in recapture or penalties."
        ),
        key_factors=[
            "Eligibility for PTC/ITC",
            "Placed-in-service date",
            "Ownership and financing structure",
            "IRS guidance and audits"
        ],
        primary_authority=[
            "26 U.S.C. § 45 (PTC)",
            "26 U.S.C. § 48 (ITC)",
            "IRS Notices and Revenue Procedures"
        ],
        burden_holder="Project owner or tax equity investor",
        adversary_position="IRS may challenge eligibility or recapture credits",
        counter_arguments=[
            "Project meets all requirements",
            "Documentation is complete",
            "IRS guidance is followed"
        ],
        resolution_strategy="Consult tax counsel and maintain robust documentation.",
        entity_scope="Renewable project owners, tax equity investors",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IRS Notice 2013-29"
    ),
    DoctrineBlock(
        topic="FERC Compliance and Self-Reporting Obligations",
        keywords=["FERC", "compliance", "self-reporting", "enforcement", "mitigation", "penalties"],
        conclusion_template="Entities subject to FERC jurisdiction must maintain compliance programs and self-report violations as required.",
        reasoning_framework=(
            "FERC expects entities under its jurisdiction to maintain effective compliance programs and to self-report violations of FERC rules and orders. "
            "Self-reporting may mitigate penalties and demonstrates a culture of compliance. "
            "FERC's Office of Enforcement reviews self-reports and may close matters without penalty if violations are minor and promptly corrected. "
            "Failure to self-report may result in enhanced penalties."
        ),
        key_factors=[
            "Existence and effectiveness of compliance program",
            "Timeliness and completeness of self-report",
            "Nature and impact of violation",
            "FERC enforcement history"
        ],
        primary_authority=[
            "FERC Policy Statement on Compliance (2008)",
            "18 C.F.R. § 1b.27",
            "FERC Enforcement Manual"
        ],
        burden_holder="FERC-jurisdictional entity",
        adversary_position="FERC may allege willful or reckless non-compliance",
        counter_arguments=[
            "Violation was minor and promptly corrected",
            "Self-report was timely and complete",
            "Compliance program is robust"
        ],
        resolution_strategy="Maintain compliance culture and self-report as required.",
        entity_scope="FERC-jurisdictional entities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FERC Policy Statement on Compliance (2008)"
    ),
    DoctrineBlock(
        topic="RTO/ISO Capacity Market Mechanisms",
        keywords=["RTO", "ISO", "capacity market", "resource adequacy", "FERC", "market design"],
        conclusion_template="RTOs/ISOs may operate capacity markets to ensure resource adequacy, subject to FERC approval and oversight.",
        reasoning_framework=(
            "Regional Transmission Organizations (RTOs) and Independent System Operators (ISOs) may operate capacity markets to procure sufficient resources for reliability. "
            "Capacity market rules must be filed with and approved by FERC. "
            "Market design must ensure just and reasonable rates, mitigate market power, and provide for resource qualification and performance. "
            "Stakeholders may challenge market rules or outcomes through FERC proceedings."
        ),
        key_factors=[
            "FERC approval of market rules",
            "Resource qualification and performance",
            "Market power mitigation",
            "Stakeholder participation"
        ],
        primary_authority=[
            "Federal Power Act, 16 U.S.C. § 824d",
            "FERC Orders 719, 1000",
            "RTO/ISO tariffs"
        ],
        burden_holder="RTO/ISO",
        adversary_position="Market participants may allege market flaws or discrimination",
        counter_arguments=[
            "Market rules are just and reasonable",
            "All resources are treated fairly",
            "Market power is mitigated"
        ],
        resolution_strategy="Engage stakeholders and maintain FERC-approved rules.",
        entity_scope="RTOs, ISOs, market participants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Order 719"
    ),
    DoctrineBlock(
        topic="FERC Abandonment Authority for Pipelines",
        keywords=["FERC", "abandonment", "pipeline", "NGA", "certificate", "decommissioning"],
        conclusion_template="Pipeline owners must obtain FERC abandonment authorization under NGA Section 7(b) before ceasing service or decommissioning facilities.",
        reasoning_framework=(
            "The Natural Gas Act Section 7(b) requires FERC authorization before a pipeline company may abandon facilities or service. "
            "Applicants must demonstrate that abandonment is in the public interest, considering impacts on customers, markets, and the environment. "
            "FERC may condition or deny abandonment if continued service is needed. "
            "Stakeholders may intervene and oppose abandonment requests."
        ),
        key_factors=[
            "Public interest analysis",
            "Customer and market impacts",
            "Environmental considerations",
            "Alternatives to abandonment"
        ],
        primary_authority=[
            "15 U.S.C. § 717f(b)",
            "18 C.F.R. Part 157",
            "FERC Certificate Policy Statement"
        ],
        burden_holder="Pipeline owner seeking abandonment",
        adversary_position="Customers or regulators may oppose abandonment",
        counter_arguments=[
            "Service is no longer needed",
            "Alternatives are available",
            "Environmental impacts are mitigated"
        ],
        resolution_strategy="Prepare robust application and engage with stakeholders.",
        entity_scope="Pipeline owners, FERC",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FERC Certificate Policy Statement (1999)"
    ),
    DoctrineBlock(
        topic="FERC Order 1000 Regional Transmission Planning",
        keywords=["FERC", "Order 1000", "transmission planning", "regional", "cost allocation", "public policy"],
        conclusion_template="Transmission providers must participate in regional planning processes and comply with FERC Order 1000 requirements.",
        reasoning_framework=(
            "FERC Order 1000 requires transmission providers to engage in regional transmission planning, consider public policy requirements, and establish cost allocation methods. "
            "Order 1000 mandates stakeholder participation, transparency, and non-discriminatory processes. "
            "Regional planning must address reliability, economic, and public policy needs. "
            "Cost allocation must be just, reasonable, and roughly commensurate with benefits."
        ),
        key_factors=[
            "Participation in regional planning",
            "Stakeholder engagement",
            "Cost allocation methodology",
            "Public policy consideration"
        ],
        primary_authority=[
            "FERC Order 1000",
            "18 C.F.R. § 35.28",
            "Regional planning tariffs"
        ],
        burden_holder="Transmission provider",
        adversary_position="Stakeholders may allege exclusion or unfair cost allocation",
        counter_arguments=[
            "Process is open and transparent",
            "Cost allocation is fair",
            "Public policy needs are addressed"
        ],
        resolution_strategy="Engage stakeholders and document compliance with Order 1000.",
        entity_scope="Transmission providers, RTOs/ISOs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FERC Order 1000"
    ),
    DoctrineBlock(
        topic="FERC Affiliate Restrictions and Code of Conduct",
        keywords=["FERC", "affiliate", "code of conduct", "separation", "market power", "standards of conduct"],
        conclusion_template="FERC-jurisdictional entities must comply with affiliate restrictions and standards of conduct to prevent market power abuse.",
        reasoning_framework=(
            "FERC's affiliate restrictions and Standards of Conduct require separation of functions, information sharing limits, and non-discriminatory treatment of affiliates. "
            "Transmission providers must ensure that marketing affiliates do not receive preferential access to information or services. "
            "Violations may result in enforcement actions and penalties. "
            "Entities must train employees and maintain compliance documentation."
        ),
        key_factors=[
            "Functional separation",
            "Information sharing controls",
            "Employee training",
            "Compliance audits"
        ],
        primary_authority=[
            "18 C.F.R. Part 358",
            "FERC Orders 2004, 717",
            "Federal Power Act"
        ],
        burden_holder="FERC-jurisdictional entity",
        adversary_position="FERC or market participants may allege affiliate abuse",
        counter_arguments=[
            "All standards of conduct are met",
            "No preferential treatment",
            "Robust compliance program"
        ],
        resolution_strategy="Maintain and audit compliance with standards of conduct.",
        entity_scope="Transmission providers, affiliates",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FERC Order 717"
    ),
    DoctrineBlock(
        topic="NERC Reliability Standards Enforcement",
        keywords=["NERC", "reliability standards", "enforcement", "compliance", "BES", "penalties"],
        conclusion_template="Registered entities must comply with NERC reliability standards and are subject to enforcement and penalties for violations.",
        reasoning_framework=(
            "NERC develops and enforces reliability standards for the Bulk Electric System (BES), subject to FERC approval. "
            "Registered entities must implement compliance programs, self-report violations, and cooperate with audits. "
            "Violations may result in penalties, mitigation plans, and public disclosure. "
            "NERC and Regional Entities conduct enforcement and may escalate matters to FERC."
        ),
        key_factors=[
            "Registration status",
            "Compliance program effectiveness",
            "Audit and enforcement history",
            "Mitigation plan implementation"
        ],
        primary_authority=[
            "16 U.S.C. § 824o",
            "NERC Reliability Standards",
            "FERC Orders 693, 822"
        ],
        burden_holder="Registered entity",
        adversary_position="NERC or FERC may allege non-compliance",
        counter_arguments=[
            "All standards are met",
            "Violations are minor and corrected",
            "Mitigation plans are effective"
        ],
        resolution_strategy="Maintain robust compliance and respond to audits.",
        entity_scope="BES owners, operators, users",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FERC Order 693"
    ),
    DoctrineBlock(
        topic="FERC Transmission Incentives Policy",
        keywords=["FERC", "transmission", "incentives", "policy", "investment", "rate of return"],
        conclusion_template="Transmission developers may seek FERC-approved incentives to promote investment in new or upgraded transmission facilities.",
        reasoning_framework=(
            "FERC's transmission incentives policy allows developers to request incentives such as higher return on equity, CWIP in rate base, or recovery of abandoned plant costs. "
            "Applicants must demonstrate that incentives are necessary to promote investment and that projects meet policy goals. "
            "FERC reviews applications for consistency with policy statements and orders."
        ),
        key_factors=[
            "Project eligibility",
            "Demonstration of need for incentives",
            "Consistency with policy goals",
            "Stakeholder support"
        ],
        primary_authority=[
            "Federal Power Act, 16 U.S.C. § 824s",
            "FERC Orders 679, 679-A",
            "Transmission Incentives Policy Statement"
        ],
        burden_holder="Transmission developer",
        adversary_position="FERC or intervenors may challenge need or magnitude of incentives",
        counter_arguments=[
            "Project faces significant risks",
            "Incentives are necessary for financing",
            "Benefits outweigh costs"
        ],
        resolution_strategy="Submit robust application with supporting analysis.",
        entity_scope="Transmission developers, FERC",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Order 679"
    ),
    DoctrineBlock(
        topic="ERCOT Resource Adequacy and Scarcity Pricing",
        keywords=["ERCOT", "resource adequacy", "scarcity pricing", "market signals", "Texas", "energy-only market"],
        conclusion_template="ERCOT relies on scarcity pricing and market signals to ensure resource adequacy in its energy-only market.",
        reasoning_framework=(
            "ERCOT operates an energy-only market without a mandatory capacity market. "
            "Resource adequacy is promoted through scarcity pricing mechanisms such as the Operating Reserve Demand Curve (ORDC). "
            "Scarcity prices signal the need for investment in new resources. "
            "The PUCT oversees market design and may adjust scarcity pricing parameters to ensure reliability."
        ),
        key_factors=[
            "Scarcity pricing design",
            "Market signals for new investment",
            "PUCT oversight",
            "Resource adequacy assessments"
        ],
        primary_authority=[
            "ERCOT Nodal Protocols",
            "PUCT Substantive Rules §25.505",
            "Texas Utilities Code §39.159"
        ],
        burden_holder="ERCOT",
        adversary_position="Market participants may allege inadequate resource adequacy or price volatility",
        counter_arguments=[
            "Scarcity pricing is effective",
            "Market signals are robust",
            "PUCT can adjust parameters"
        ],
        resolution_strategy="Monitor market outcomes and adjust design as needed.",
        entity_scope="ERCOT, market participants, PUCT",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="PUCT Project No. 40000"
    ),
    DoctrineBlock(
        topic="FERC Order 2222 Distributed Energy Resource Aggregation",
        keywords=["FERC", "Order 2222", "DER", "aggregation", "wholesale market", "participation"],
        conclusion_template="FERC Order 2222 requires RTOs/ISOs to allow distributed energy resource aggregations to participate in wholesale markets.",
        reasoning_framework=(
            "FERC Order 2222 directs RTOs/ISOs to remove barriers to the participation of distributed energy resource (DER) aggregations in wholesale markets. "
            "RTOs/ISOs must revise tariffs to enable DERs to provide all services they are technically capable of. "
            "Order 2222 establishes requirements for eligibility, coordination with distribution utilities, and metering. "
            "State and local authorities retain jurisdiction over interconnection and safety."
        ),
        key_factors=[
            "Eligibility of DERs and aggregators",
            "Tariff revisions and implementation",
            "Coordination with distribution utilities",
            "State and local jurisdiction"
        ],
        primary_authority=[
            "FERC Order 2222",
            "18 C.F.R. § 35.28",
            "RTO/ISO tariffs"
        ],
        burden_holder="RTO/ISO",
        adversary_position="Stakeholders may allege barriers or inadequate coordination",
        counter_arguments=[
            "Tariffs are compliant",
            "Coordination protocols are robust",
            "DERs are technically capable"
        ],
        resolution_strategy="Engage stakeholders and monitor DER participation.",
        entity_scope="RTOs, ISOs, DER aggregators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Order 2222"
    ),
    DoctrineBlock(
        topic="FERC PURPA Implementation and QF Rights",
        keywords=["FERC", "PURPA", "QF", "qualifying facility", "implementation", "rates"],
        conclusion_template="Utilities must purchase power from qualifying facilities (QFs) at avoided cost rates under FERC's PURPA regulations.",
        reasoning_framework=(
            "The Public Utility Regulatory Policies Act (PURPA) requires utilities to purchase power from QFs at rates not exceeding the utility's avoided cost. "
            "FERC's regulations define QF eligibility and establish implementation requirements. "
            "State commissions oversee avoided cost determinations and contract terms. "
            "Utilities may seek relief from purchase obligations if competitive markets exist."
        ),
        key_factors=[
            "QF certification and eligibility",
            "Avoided cost rate calculation",
            "State commission oversight",
            "Market structure"
        ],
        primary_authority=[
            "PURPA, 16 U.S.C. § 824a-3",
            "18 C.F.R. Part 292",
            "FERC Orders 872, 69"
        ],
        burden_holder="Utility",
        adversary_position="QFs may allege underpayment or contract disputes",
        counter_arguments=[
            "Rates reflect avoided cost",
            "QF meets eligibility requirements",
            "State rules are followed"
        ],
        resolution_strategy="Follow FERC and state PURPA rules and resolve disputes through commissions.",
        entity_scope="Utilities, QFs, state commissions",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FERC Order 872"
    ),
    DoctrineBlock(
        topic="ERCOT Emergency Operations and Load Shedding",
        keywords=["ERCOT", "emergency operations", "load shedding", "reliability", "grid emergency", "contingency"],
        conclusion_template="ERCOT may direct load shedding during grid emergencies to maintain system reliability, subject to PUCT oversight.",
        reasoning_framework=(
            "ERCOT is responsible for maintaining grid reliability and may declare emergency conditions requiring load shedding. "
            "Load shedding is implemented according to ERCOT protocols and PUCT rules. "
            "Market participants must comply with ERCOT directives. "
            "PUCT may review emergency actions and require post-event reporting."
        ),
        key_factors=[
            "Emergency declaration and protocols",
            "Compliance with directives",
            "PUCT oversight",
            "Post-event reporting"
        ],
        primary_authority=[
            "ERCOT Nodal Protocols",
            "PUCT Substantive Rules §25.503",
            "Texas Utilities Code §39.151"
        ],
        burden_holder="ERCOT",
        adversary_position="Market participants or customers may challenge emergency actions",
        counter_arguments=[
            "Actions were necessary for reliability",
            "Protocols were followed",
            "PUCT oversight was maintained"
        ],
        resolution_strategy="Document emergency actions and report to PUCT.",
        entity_scope="ERCOT, market participants, PUCT",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 51812"
    ),
    DoctrineBlock(
        topic="FERC Transmission Planning and Cost Allocation Principles",
        keywords=["FERC", "transmission planning", "cost allocation", "principles", "regional planning"],
        conclusion_template="Transmission planning and cost allocation must be open, transparent, and roughly commensurate with benefits.",
        reasoning_framework=(
            "FERC requires transmission providers to conduct open and transparent planning processes and to allocate costs in a manner roughly commensurate with benefits. "
            "Stakeholder participation is essential. "
            "Cost allocation methods must be filed with and approved by FERC. "
            "Disputes may be resolved through FERC's complaint process."
        ),
        key_factors=[
            "Stakeholder engagement",
            "Transparency of planning process",
            "Cost allocation methodology",
            "FERC approval"
        ],
        primary_authority=[
            "FERC Orders 890, 1000",
            "18 C.F.R. § 35.28",
            "Regional planning tariffs"
        ],
        burden_holder="Transmission provider",
        adversary_position="Stakeholders may allege unfair cost allocation",
        counter_arguments=[
            "Process is open and fair",
            "Cost allocation is justified",
            "Benefits are documented"
        ],
        resolution_strategy="Engage stakeholders and document cost allocation rationale.",
        entity_scope="Transmission providers, RTOs/ISOs",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FERC Order 1000"
    ),
    DoctrineBlock(
        topic="NERC Event Reporting and Disturbance Analysis",
        keywords=["NERC", "event reporting", "disturbance analysis", "BES", "compliance"],
        conclusion_template="Registered entities must report system disturbances and perform root cause analysis as required by NERC standards.",
        reasoning_framework=(
            "NERC reliability standards require registered entities to report system disturbances, misoperations, and events affecting the Bulk Electric System. "
            "Entities must perform root cause analysis and implement corrective actions. "
            "NERC and Regional Entities review reports and may require additional mitigation. "
            "Failure to report may result in penalties."
        ),
        key_factors=[
            "Event detection and reporting",
            "Root cause analysis",
            "Corrective action implementation",
            "NERC/Regional review"
        ],
        primary_authority=[
            "NERC Reliability Standards EOP-004, PRC-004",
            "16 U.S.C. § 824o",
            "FERC Orders 693, 822"
        ],
        burden_holder="Registered entity",
        adversary_position="NERC may allege failure to report or analyze events",
        counter_arguments=[
            "All events reported timely",
            "Root cause analysis is robust",
            "Corrective actions are effective"
        ],
        resolution_strategy="Maintain event reporting and analysis protocols.",
        entity_scope="BES owners, operators, users",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NERC EOP-004"
    ),
    DoctrineBlock(
        topic="FERC Order 841 Energy Storage Participation",
        keywords=["FERC", "Order 841", "energy storage", "wholesale market", "participation"],
        conclusion_template="FERC Order 841 requires RTOs/ISOs to enable energy storage resources to participate in all wholesale markets.",
        reasoning_framework=(
            "FERC Order 841 directs RTOs/ISOs to remove barriers to the participation of energy storage resources in wholesale markets. "
            "RTOs/ISOs must revise tariffs to allow storage resources to provide all services they are technically capable of. "
            "Order 841 establishes requirements for eligibility, metering, and market participation. "
            "State and local authorities retain jurisdiction over interconnection and safety."
        ),
        key_factors=[
            "Eligibility of storage resources",
            "Tariff revisions and implementation",
            "Coordination with distribution utilities",
            "State and local jurisdiction"
        ],
        primary_authority=[
            "FERC Order 841",
            "18 C.F.R. § 35.28",
            "RTO/ISO tariffs"
        ],
        burden_holder="RTO/ISO",
        adversary_position="Stakeholders may allege barriers or inadequate coordination",
        counter_arguments=[
            "Tariffs are compliant",
            "Coordination protocols are robust",
            "Storage resources are technically capable"
        ],
        resolution_strategy="Engage stakeholders and monitor storage participation.",
        entity_scope="RTOs, ISOs, storage resource owners",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Order 841"
    ),
    DoctrineBlock(
        topic="ERCOT Market Monitor and Enforcement",
        keywords=["ERCOT", "market monitor", "enforcement", "market power", "compliance"],
        conclusion_template="ERCOT's Independent Market Monitor oversees market behavior and enforces compliance with market rules.",
        reasoning_framework=(
            "ERCOT's Independent Market Monitor (IMM) is responsible for monitoring market participant behavior, detecting market power abuse, and enforcing compliance with ERCOT protocols. "
            "The IMM reports to the PUCT and may recommend penalties or corrective actions. "
            "Market participants must cooperate with investigations and maintain compliance programs."
        ),
        key_factors=[
            "Market participant behavior",
            "Protocol compliance",
            "IMM investigations",
            "PUCT oversight"
        ],
        primary_authority=[
            "ERCOT Nodal Protocols",
            "PUCT Substantive Rules §25.365",
            "Texas Utilities Code §39.1515"
        ],
        burden_holder="Market participant",
        adversary_position="IMM may allege market power abuse or protocol violations",
        counter_arguments=[
            "Behavior was consistent with protocols",
            "No market power abuse",
            "Compliance program is robust"
        ],
        resolution_strategy="Cooperate with IMM and address findings promptly.",
        entity_scope="ERCOT market participants, IMM",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 40480"
    ),
    DoctrineBlock(
        topic="FERC Order 2006 Small Generator Interconnection",
        keywords=["FERC", "Order 2006", "small generator", "interconnection", "SGIP", "SGIA"],
        conclusion_template="Small generators must follow FERC's pro forma SGIP and SGIA for interconnection to the transmission system.",
        reasoning_framework=(
            "FERC Order 2006 established pro forma Small Generator Interconnection Procedures (SGIP) and Agreement (SGIA) for generators up to 20 MW. "
            "The SGIP provides a standardized process for application, studies, and agreement negotiation. "
            "Transmission providers must process requests in a non-discriminatory manner. "
            "Disputes may be resolved through FERC's complaint process."
        ),
        key_factors=[
            "Generator size and eligibility",
            "SGIP process compliance",
            "Study results and cost allocation",
            "Agreement negotiation"
        ],
        primary_authority=[
            "FERC Order 2006",
            "18 C.F.R. § 35.28",
            "Pro forma SGIP/SGIA"
        ],
        burden_holder="Small generator",
        adversary_position="Transmission provider may delay or impose unreasonable requirements",
        counter_arguments=[
            "Process was followed",
            "Cost allocation is fair",
            "No undue discrimination"
        ],
        resolution_strategy="Follow SGIP process and escalate disputes to FERC as needed.",
        entity_scope="Small generators, transmission providers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Order 2006"
    ),
    DoctrineBlock(
        topic="FERC Transmission Rate Incentives for Advanced Technologies",
        keywords=["FERC", "transmission", "rate incentives", "advanced technology", "innovation"],
        conclusion_template="FERC may grant transmission rate incentives for deployment of advanced technologies that enhance grid reliability or efficiency.",
        reasoning_framework=(
            "FERC encourages the deployment of advanced transmission technologies by allowing rate incentives such as higher return on equity or accelerated depreciation. "
            "Applicants must demonstrate that the technology enhances reliability, efficiency, or capacity. "
            "FERC reviews applications for consistency with policy goals and stakeholder support."
        ),
        key_factors=[
            "Technology eligibility",
            "Demonstrated benefits",
            "Consistency with FERC policy",
            "Stakeholder support"
        ],
        primary_authority=[
            "Federal Power Act, 16 U.S.C. § 824s",
            "FERC Orders 679, 679-A",
            "Transmission Incentives Policy Statement"
        ],
        burden_holder="Transmission developer",
        adversary_position="FERC or intervenors may challenge need or benefits",
        counter_arguments=[
            "Technology enhances reliability or efficiency",
            "Benefits outweigh costs",
            "Stakeholder support is strong"
        ],
        resolution_strategy="Submit robust application with supporting analysis.",
        entity_scope="Transmission developers, FERC",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FERC Order 679"
    ),
    DoctrineBlock(
        topic="ERCOT Congestion Revenue Rights (CRRs) and Allocation",
        keywords=["ERCOT", "CRR", "congestion revenue rights", "allocation", "market", "hedging"],
        conclusion_template="Market participants may acquire CRRs through ERCOT auctions and allocations to hedge congestion costs.",
        reasoning_framework=(
            "ERCOT administers Congestion Revenue Rights (CRRs) to allow market participants to hedge congestion costs in the nodal market. "
            "CRRs are allocated and auctioned according to ERCOT protocols. "
            "Market participants must comply with eligibility and credit requirements. "
            "Disputes are resolved through ERCOT's dispute resolution process."
        ),
        key_factors=[
            "Eligibility for CRR allocation",
            "Auction participation",
            "Credit requirements",
            "Protocol compliance"
        ],
        primary_authority=[
            "ERCOT Nodal Protocols",
            "PUCT Substantive Rules §25.501",
            "Texas Utilities Code §39.151"
        ],
        burden_holder="Market participant",
        adversary_position="ERCOT or other participants may allege protocol violations",
        counter_arguments=[
            "All requirements met",
            "No protocol violations",
            "Dispute process followed"
        ],
        resolution_strategy="Follow ERCOT procedures and resolve disputes as provided.",
        entity_scope="ERCOT market participants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 31540"
    ),
    DoctrineBlock(
        topic="FERC Order 845 Interconnection Reforms",
        keywords=["FERC", "Order 845", "interconnection", "reforms", "queue management"],
        conclusion_template="FERC Order 845 implements reforms to improve generator interconnection processes and transparency.",
        reasoning_framework=(
            "FERC Order 845 reforms the generator interconnection process by improving transparency, flexibility, and efficiency. "
            "Key reforms include increased access to information, option to build, surplus interconnection service, and improved queue management. "
            "Transmission providers must revise tariffs to implement these reforms."
        ),
        key_factors=[
            "Tariff revisions",
            "Transparency and information access",
            "Queue management improvements",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "FERC Order 845",
            "18 C.F.R. § 35.28",
            "Pro forma LGIP/LGIA"
        ],
        burden_holder="Transmission provider",
        adversary_position="Generators may allege inadequate implementation",
        counter_arguments=[
            "Tariffs are compliant",
            "Process is transparent",
            "Stakeholder input is considered"
        ],
        resolution_strategy="Engage stakeholders and monitor implementation.",
        entity_scope="Transmission providers, generators",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Order 845"
    ),
    DoctrineBlock(
        topic="ERCOT Black Start Service and Restoration",
        keywords=["ERCOT", "black start", "restoration", "reliability", "emergency operations"],
        conclusion_template="ERCOT contracts for black start service to ensure system restoration capability after a blackout.",
        reasoning_framework=(
            "ERCOT is responsible for ensuring that black start resources are available to restore the system after a blackout. "
            "Black start service providers are selected through a competitive process and must meet technical and operational requirements. "
            "ERCOT periodically tests black start capability and coordinates restoration plans with market participants."
        ),
        key_factors=[
            "Provider eligibility",
            "Technical and operational requirements",
            "Testing and drills",
            "Restoration plan coordination"
        ],
        primary_authority=[
            "ERCOT Nodal Protocols",
            "PUCT Substantive Rules §25.362",
            "Texas Utilities Code §39.151"
        ],
        burden_holder="ERCOT",
        adversary_position="Market participants may allege inadequate restoration capability",
        counter_arguments=[
            "Providers meet all requirements",
            "Restoration plans are robust",
            "Testing is effective"
        ],
        resolution_strategy="Maintain and test restoration plans regularly.",
        entity_scope="ERCOT, black start providers",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 51812"
    ),
    DoctrineBlock(
        topic="FERC Order 719 RTO/ISO Governance and Market Monitoring",
        keywords=["FERC", "Order 719", "RTO", "ISO", "governance", "market monitoring"],
        conclusion_template="FERC Order 719 establishes governance and market monitoring requirements for RTOs/ISOs.",
        reasoning_framework=(
            "FERC Order 719 requires RTOs/ISOs to have independent market monitors, transparent governance, and stakeholder processes. "
            "Order 719 aims to ensure market integrity, fair competition, and responsiveness to stakeholder concerns. "
            "RTOs/ISOs must file compliance plans with FERC and address market power concerns."
        ),
        key_factors=[
            "Market monitor independence",
            "Governance transparency",
            "Stakeholder engagement",
            "FERC oversight"
        ],
        primary_authority=[
            "FERC Order 719",
            "18 C.F.R. § 35.28",
            "RTO/ISO tariffs"
        ],
        burden_holder="RTO/ISO",
        adversary_position="Market participants may allege governance or monitoring deficiencies",
        counter_arguments=[
            "Market monitor is independent",
            "Governance is transparent",
            "Stakeholders are engaged"
        ],
        resolution_strategy="Maintain compliance and address stakeholder concerns.",
        entity_scope="RTOs, ISOs, market participants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FERC Order 719"
    ),
    DoctrineBlock(
        topic="ERCOT Credit Requirements and Default Risk",
        keywords=["ERCOT", "credit requirements", "default risk", "market participant", "settlement"],
        conclusion_template="ERCOT enforces credit requirements to mitigate default risk among market participants.",
        reasoning_framework=(
            "ERCOT requires market participants to meet credit requirements to participate in the market and settle transactions. "
            "Credit limits are based on exposure calculations and financial strength. "
            "Failure to meet requirements may result in market suspension or termination. "
            "ERCOT monitors credit exposure and may adjust requirements as needed."
        ),
        key_factors=[
            "Creditworthiness assessment",
            "Exposure calculation",
            "Collateral and guarantees",
            "Default procedures"
        ],
        primary_authority=[
            "ERCOT Nodal Protocols",
            "PUCT Substantive Rules §25.501",
            "Texas Utilities Code §39.151"
        ],
        burden_holder="Market participant",
        adversary_position="ERCOT may suspend or terminate participation for default",
        counter_arguments=[
            "Credit requirements are met",
            "Collateral is sufficient",
            "Default risk is managed"
        ],
        resolution_strategy="Monitor credit exposure and maintain adequate collateral.",
        entity_scope="ERCOT market participants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 31540"
    ),
    DoctrineBlock(
        topic="FERC Order 2222A DER Aggregation Clarifications",
        keywords=["FERC", "Order 2222A", "DER", "aggregation", "clarification"],
        conclusion_template="FERC Order 2222A clarifies DER aggregation participation and coordination requirements in wholesale markets.",
        reasoning_framework=(
            "FERC Order 2222A provides clarifications to Order 2222 regarding the participation of DER aggregations in wholesale markets. "
            "Key clarifications address coordination with distribution utilities, opt-out provisions, and metering requirements. "
            "RTOs/ISOs must implement these clarifications in their tariffs."
        ),
        key_factors=[
            "Coordination protocols",
            "Opt-out provisions",
            "Metering and telemetry",
            "Tariff implementation"
        ],
        primary_authority=[
            "FERC Order 2222A",
            "18 C.F.R. § 35.28",
            "RTO/ISO tariffs"
        ],
        burden_holder="RTO/ISO",
        adversary_position="Stakeholders may allege insufficient coordination or clarity",
        counter_arguments=[
            "Protocols are robust",
            "Opt-out provisions are clear",
            "Metering is accurate"
        ],
        resolution_strategy="Implement clarifications and engage stakeholders.",
        entity_scope="RTOs, ISOs, DER aggregators",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FERC Order 2222A"
    ),
    DoctrineBlock(
        topic="NERC Supply Chain Risk Management Standards",
        keywords=["NERC", "supply chain", "risk management", "CIP-013", "cybersecurity"],
        conclusion_template="Registered entities must implement supply chain risk management plans as required by NERC CIP-013.",
        reasoning_framework=(
            "NERC CIP-013 requires registered entities to develop and implement supply chain risk management plans for BES Cyber Systems. "
            "Plans must address vendor risk, procurement controls, and ongoing monitoring. "
            "Entities must document compliance and cooperate with audits. "
            "Failure to comply may result in penalties."
        ),
        key_factors=[
            "Plan development and implementation",
            "Vendor risk assessment",
            "Procurement controls",
            "Audit and enforcement"
        ],
        primary_authority=[
            "NERC CIP-013",
            "16 U.S.C. § 824o",
            "FERC Order 822"
        ],
        burden_holder="Registered entity",
        adversary_position="NERC or FERC may allege non-compliance",
        counter_arguments=[
            "Plan is robust and implemented",
            "Vendor risks are managed",
            "Audit findings are addressed"
        ],
        resolution_strategy="Maintain and update supply chain risk management plans.",
        entity_scope="BES owners, operators, users",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FERC Order 822"
    ),
    DoctrineBlock(
        topic="ERCOT Weatherization and Extreme Weather Preparedness",
        keywords=["ERCOT", "weatherization", "extreme weather", "preparedness", "PUCT", "compliance"],
        conclusion_template="ERCOT market participants must comply with weatherization standards and report preparedness for extreme weather events.",
        reasoning_framework=(
            "Following extreme weather events, Texas law and PUCT rules require ERCOT market participants to implement weatherization measures and report preparedness. "
            "ERCOT and PUCT may inspect facilities and enforce compliance. "
            "Non-compliance may result in penalties or market suspension."
        ),
        key_factors=[
            "Weatherization measures implemented",
            "Reporting and documentation",
            "Inspection results",
            "Compliance with PUCT rules"
        ],
        primary_authority=[
            "Texas Utilities Code §35.0021",
            "PUCT Substantive Rules §25.55",
            "ERCOT Nodal Protocols"
        ],
        burden_holder="Market participant",
        adversary_position="ERCOT or PUCT may allege inadequate preparedness",
        counter_arguments=[
            "All measures implemented",
            "Reporting is accurate",
            "Inspections are passed"
        ],
        resolution_strategy="Implement and document weatherization measures.",
        entity_scope="ERCOT market participants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 51840"
    ),
    DoctrineBlock(
        topic="FERC Order 2222B DER Aggregation Further Clarifications",
        keywords=["FERC", "Order 2222B", "DER", "aggregation", "clarification"],
        conclusion_template="FERC Order 2222B provides further clarifications on DER aggregation participation in wholesale markets.",
        reasoning_framework=(
            "FERC Order 2222B addresses rehearing requests and provides further clarifications to Order 2222 regarding DER aggregation. "
            "Key issues include eligibility, coordination, and implementation timelines. "
            "RTOs/ISOs must update tariffs to reflect these clarifications."
        ),
        key_factors=[
            "Eligibility criteria",
            "Coordination protocols",
            "Implementation timelines",
            "Tariff revisions"
        ],
        primary_authority=[
            "FERC Order 2222B",
            "18 C.F.R. § 35.28",
            "RTO/ISO tariffs"
        ],
        burden_holder="RTO/ISO",
        adversary_position="Stakeholders may allege inadequate clarifications",
        counter_arguments=[
            "Clarifications are implemented",
            "Stakeholder concerns are addressed",
            "Tariffs are updated"
        ],
        resolution_strategy="Update tariffs and engage stakeholders.",
        entity_scope="RTOs, ISOs, DER aggregators",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FERC Order 2222B"
    ),
    DoctrineBlock(
        topic="ERCOT Emergency Pricing and Market Suspension",
        keywords=["ERCOT", "emergency pricing", "market suspension", "scarcity", "PUCT"],
        conclusion_template="ERCOT may implement emergency pricing and suspend market operations during extreme events, subject to PUCT oversight.",
        reasoning_framework=(
            "ERCOT protocols and PUCT rules allow for emergency pricing and market suspension during extreme events to maintain reliability. "
            "Emergency pricing signals scarcity and may trigger administrative price caps. "
            "Market suspension is a last resort and must be reported to PUCT. "
            "Post-event review is required."
        ),
        key_factors=[
            "Triggering events",
            "Emergency pricing protocols",
            "Market suspension procedures",
            "PUCT oversight"
        ],
        primary_authority=[
            "ERCOT Nodal Protocols",
            "PUCT Substantive Rules §25.502",
            "Texas Utilities Code §39.151"
        ],
        burden_holder="ERCOT",
        adversary_position="Market participants may challenge emergency actions",
        counter_arguments=[
            "Actions were necessary for reliability",
            "Protocols were followed",
            "PUCT oversight was maintained"
        ],
        resolution_strategy="Document actions and report to PUCT.",
        entity_scope="ERCOT, market participants, PUCT",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="PUCT Docket No. 51812"
    ),
    DoctrineBlock(
        topic="FERC Order 2222 DER Aggregation State Opt-Out",
        keywords=["FERC", "Order 2222", "DER", "aggregation", "state opt-out"],
        conclusion_template="States may opt out of allowing DER aggregation participation in FERC-jurisdictional markets under certain conditions.",
        reasoning_framework=(
            "FERC Order 2222 allows states to opt out of DER aggregation participation in RTO/ISO markets for retail customers. "
            "The opt-out applies to retail customers served by utilities not subject to FERC jurisdiction. "
            "RTOs/ISOs must implement opt-out provisions in their tariffs and coordinate with state commissions."
        ),
        key_factors=[
            "State opt-out decision",
            "Utility jurisdictional status",
            "Tariff implementation",
            "Coordination with state commissions"
        ],
        primary_authority=[
            "FERC Order 2222",
            "18 C.F.R. § 35.28",
            "RTO/ISO tariffs"
        ],
        burden_holder="RTO/ISO",
        adversary_position="Stakeholders may allege improper opt-out or lack of coordination",
        counter_arguments=[
            "Opt-out is consistent with FERC rules",
            "Coordination is robust",
            "Tariffs are updated"
        ],
        resolution_strategy="Implement opt-out provisions and engage with state commissions.",
        entity_scope="RTOs, ISOs, state commissions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FERC Order 2222"
    ),
    DoctrineBlock(
        topic="ERCOT Market Entry and Registration Requirements",
        keywords=["ERCOT", "market entry", "registration", "QSE", "market participant"],
        conclusion_template="Entities must register with ERCOT and meet eligibility requirements to participate in the market.",
        reasoning_framework=(
            "To participate in the ERCOT market, entities must register as Qualified Scheduling Entities (QSE