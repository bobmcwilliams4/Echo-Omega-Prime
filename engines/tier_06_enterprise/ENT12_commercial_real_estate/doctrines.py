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
        topic="Triple Net Lease Structure",
        keywords=["NNN", "triple net", "lease", "tenant", "landlord", "operating expenses"],
        conclusion_template="Under a triple net lease, the tenant is responsible for payment of real estate taxes, building insurance, and maintenance, in addition to rent.",
        reasoning_framework="""
1. Define the lease structure and allocation of expenses.
2. Review lease language for explicit assignment of taxes, insurance, and maintenance.
3. Analyze jurisdictional norms and any statutory overrides.
4. Assess the parties' negotiation history and course of performance.
5. Consider the impact on rent calculation and risk allocation.
6. Evaluate implications for lender underwriting and property valuation.
7. Review any carve-outs or exceptions in the lease.
8. Confirm compliance with local law regarding expense pass-throughs.
9. Assess enforceability of expense obligations in the event of default.
10. Consider the effect on tenant improvements and capital expenditures.
11. Determine the scope of 'maintenance'—structural vs. non-structural.
12. Evaluate insurance requirements and adequacy.
13. Review remedies for non-payment of expenses.
14. Analyze any subordination or non-disturbance clauses affecting expense obligations.
15. Synthesize findings to conclude the tenant's obligations under the NNN lease.
""",
        key_factors=[
            "Lease language",
            "Jurisdictional law",
            "Negotiation history",
            "Expense definitions",
            "Remedies for breach"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Tenant",
        adversary_position="Landlord may argue for broader tenant expense responsibility.",
        counter_arguments=[
            "Ambiguity in lease terms",
            "Statutory limitations on expense pass-through",
            "Implied landlord obligations"
        ],
        resolution_strategy="Strict interpretation of lease language; contra proferentem if ambiguous.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="In re 114 Tenth Ave. Assoc. v. McCarthy, 2005 NY Slip Op 25243"
    ),
    DoctrineBlock(
        topic="CMBS Loan Servicing Standards",
        keywords=["CMBS", "servicing", "special servicer", "master servicer", "pooling and servicing agreement"],
        conclusion_template="CMBS loans are serviced according to the Pooling and Servicing Agreement (PSA), which allocates duties between master and special servicers.",
        reasoning_framework="""
1. Identify the relevant PSA governing the loan pool.
2. Distinguish between master and special servicer roles.
3. Analyze servicing standards for performing vs. non-performing loans.
4. Review requirements for consent, modifications, and waivers.
5. Assess the impact of REMIC tax compliance on servicing discretion.
6. Consider the duties of good faith, fair dealing, and prudent servicing.
7. Evaluate the servicer's obligations to certificate holders.
8. Examine the process for transferring servicing upon default.
9. Review reporting and remittance obligations.
10. Analyze limitations on servicer liability and indemnification provisions.
11. Consider the impact of servicing advances and recoverability.
12. Assess the effect of servicing standards on borrower remedies.
13. Synthesize to determine the applicable servicing standard in the dispute.
""",
        key_factors=[
            "Pooling and Servicing Agreement",
            "Loan performance status",
            "Servicer discretion",
            "REMIC compliance",
            "Borrower consent requirements"
        ],
        primary_authority=[
            "Pooling and Servicing Agreement",
            "REMIC regulations (IRC §§860A-860G)",
            "Industry servicing guides (CREFC, MBA)"
        ],
        burden_holder="Servicer",
        adversary_position="Borrower may challenge servicer's exercise of discretion.",
        counter_arguments=[
            "Servicer acted outside PSA authority",
            "Failure to act in good faith",
            "Improper servicing advances"
        ],
        resolution_strategy="Apply PSA terms and industry standards; review servicer's compliance with contractual and regulatory obligations.",
        entity_scope="CMBS servicers, borrowers, certificate holders",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CWCapital Asset Mgmt., LLC v. Chicago Properties, LLC, 610 F.3d 497 (7th Cir. 2010)"
    ),
    DoctrineBlock(
        topic="IRC Section 1031 Like-Kind Exchange",
        keywords=["1031", "like-kind exchange", "deferred exchange", "replacement property", "qualified intermediary"],
        conclusion_template="IRC §1031 allows deferral of capital gains tax on exchange of like-kind real property held for investment or business use.",
        reasoning_framework="""
1. Confirm both relinquished and replacement properties are held for investment or productive use in a trade or business.
2. Determine if both properties are 'real property' under current IRS definitions.
3. Verify the properties are 'like-kind' (broadly interpreted for real estate).
4. Ensure the taxpayer does not receive cash or other non-like-kind property (boot).
5. Confirm use of a qualified intermediary to facilitate the exchange.
6. Adhere to strict identification (45-day) and acquisition (180-day) deadlines.
7. Review documentation for compliance with IRS regulations.
8. Assess the effect of debt relief and replacement property financing.
9. Evaluate state-level conformity with federal 1031 rules.
10. Consider anti-abuse rules and related party restrictions.
11. Analyze the impact of recent legislative changes (e.g., Tax Cuts and Jobs Act).
12. Synthesize to determine eligibility for tax deferral under §1031.
""",
        key_factors=[
            "Holding purpose",
            "Like-kind status",
            "Qualified intermediary involvement",
            "Timing requirements",
            "Boot received"
        ],
        primary_authority=[
            "IRC §1031",
            "Treas. Reg. §1.1031",
            "IRS Notice 2008-41"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may challenge the exchange as a sale or disallow non-compliant exchanges.",
        counter_arguments=[
            "Properties not like-kind",
            "Failure to meet timing requirements",
            "Improper use of intermediary"
        ],
        resolution_strategy="Strict adherence to statutory and regulatory requirements; document all steps.",
        entity_scope="Real estate investors, business property owners",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Alderson v. Commissioner, 317 F.2d 790 (9th Cir. 1963)"
    ),
    DoctrineBlock(
        topic="Qualified Opportunity Zone Investment",
        keywords=["opportunity zone", "QOF", "capital gains", "deferral", "basis step-up"],
        conclusion_template="Investing eligible capital gains in a Qualified Opportunity Fund (QOF) allows for deferral and potential exclusion of gains under IRC §§1400Z-1 and 1400Z-2.",
        reasoning_framework="""
1. Confirm the investment is made in a certified Qualified Opportunity Fund.
2. Verify the fund invests at least 90% of assets in Qualified Opportunity Zone Property.
3. Ensure the taxpayer has eligible capital gains for deferral.
4. Adhere to the 180-day investment window from gain recognition.
5. Analyze the holding period for step-up in basis (5, 7, 10 years).
6. Review fund compliance with IRS testing and reporting requirements.
7. Assess the impact of interim gains and distributions.
8. Evaluate the effect of non-qualifying investments or fund failures.
9. Consider state-level conformity with federal Opportunity Zone rules.
10. Synthesize to determine eligibility for gain deferral and exclusion.
""",
        key_factors=[
            "QOF certification",
            "90% asset test",
            "Eligible capital gains",
            "Investment timing",
            "Holding period"
        ],
        primary_authority=[
            "IRC §§1400Z-1, 1400Z-2",
            "Treas. Reg. §§1.1400Z2(a)-1 et seq.",
            "IRS Opportunity Zones FAQs"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may challenge fund or investment qualification.",
        counter_arguments=[
            "Fund fails 90% test",
            "Late investment",
            "Non-qualifying property"
        ],
        resolution_strategy="Document all compliance steps; monitor fund reporting.",
        entity_scope="Real estate investors, QOF managers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IRS Opportunity Zone Regulations, T.D. 9889"
    ),
    DoctrineBlock(
        topic="REIT Qualification Requirements",
        keywords=["REIT", "real estate investment trust", "income test", "asset test", "distribution requirement"],
        conclusion_template="A REIT must satisfy organizational, income, asset, and distribution tests under IRC §§856-860 to maintain REIT status.",
        reasoning_framework="""
1. Confirm entity is organized as a corporation, trust, or association.
2. Verify transferability of shares and management by trustees or directors.
3. Ensure at least 100 shareholders after first year.
4. Confirm no more than 50% of shares held by five or fewer individuals.
5. Satisfy the 75% and 95% income tests for qualifying income.
6. Meet the 75% asset test for qualifying real estate assets.
7. Distribute at least 90% of taxable income to shareholders.
8. Review compliance with prohibited transaction rules.
9. Assess the effect of related party and tenant income.
10. Analyze compliance with recordkeeping and reporting requirements.
11. Synthesize to determine REIT qualification and risk of disqualification.
""",
        key_factors=[
            "Organizational structure",
            "Shareholder requirements",
            "Income and asset tests",
            "Distribution requirement",
            "Prohibited transactions"
        ],
        primary_authority=[
            "IRC §§856-860",
            "Treas. Reg. §§1.856-1 et seq.",
            "IRS REIT Audit Guidelines"
        ],
        burden_holder="REIT",
        adversary_position="IRS may challenge REIT status for test failures.",
        counter_arguments=[
            "Failure to meet income/asset tests",
            "Insufficient distributions",
            "Improper organizational structure"
        ],
        resolution_strategy="Annual compliance review; corrective distributions or restructuring if needed.",
        entity_scope="REITs, real estate investment entities",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Rev. Rul. 2004-24"
    ),
    DoctrineBlock(
        topic="Phase I Environmental Site Assessment",
        keywords=["Phase I", "ESA", "environmental due diligence", "CERCLA", "ASTM E1527"],
        conclusion_template="A Phase I ESA is conducted to identify potential or existing environmental contamination liabilities under CERCLA.",
        reasoning_framework="""
1. Retain a qualified environmental professional to conduct the assessment.
2. Review historical property records and prior uses.
3. Conduct site reconnaissance and interviews.
4. Identify recognized environmental conditions (RECs).
5. Assess the need for further investigation (Phase II).
6. Evaluate compliance with ASTM E1527-21 standards.
7. Determine if the assessment provides CERCLA 'innocent landowner' defense.
8. Analyze findings for impact on transaction risk and lender requirements.
9. Review timing and shelf-life of the assessment.
10. Synthesize to determine environmental liability and next steps.
""",
        key_factors=[
            "Qualified professional",
            "Historical use",
            "ASTM E1527 compliance",
            "Identification of RECs",
            "Timing of assessment"
        ],
        primary_authority=[
            "CERCLA (42 U.S.C. §9601 et seq.)",
            "ASTM E1527-21",
            "EPA All Appropriate Inquiries Rule (40 CFR Part 312)"
        ],
        burden_holder="Buyer/borrower",
        adversary_position="Seller/lender may dispute findings or require additional investigation.",
        counter_arguments=[
            "Incomplete assessment",
            "Failure to identify all RECs",
            "Outdated report"
        ],
        resolution_strategy="Strict adherence to ASTM and EPA standards; update assessment if necessary.",
        entity_scope="Buyers, lenders, environmental consultants",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="United States v. Bestfoods, 524 U.S. 51 (1998)"
    ),
    DoctrineBlock(
        topic="ALTA Title Insurance Endorsements",
        keywords=["ALTA", "title insurance", "endorsement", "lender policy", "owner policy"],
        conclusion_template="ALTA endorsements modify standard title insurance coverage to address specific risks or requirements in commercial real estate transactions.",
        reasoning_framework="""
1. Identify the base ALTA policy form in use (lender or owner).
2. Determine the specific risk or issue requiring endorsement (e.g., zoning, access, survey).
3. Review available ALTA endorsement forms and their coverage.
4. Assess the underwriter's willingness to issue the endorsement.
5. Analyze the effect of endorsements on policy exclusions and exceptions.
6. Evaluate any additional premium or underwriting requirements.
7. Confirm the endorsement's compatibility with local law and custom.
8. Review the impact on lender or owner protections.
9. Synthesize to determine appropriate endorsements for the transaction.
""",
        key_factors=[
            "Base policy form",
            "Risk to be covered",
            "Underwriter requirements",
            "Local law",
            "Premium/cost"
        ],
        primary_authority=[
            "ALTA Endorsement Forms",
            "State insurance statutes",
            "Title insurer underwriting guidelines"
        ],
        burden_holder="Insured (lender or owner)",
        adversary_position="Title insurer may deny or limit endorsement coverage.",
        counter_arguments=[
            "Endorsement not available in jurisdiction",
            "Insufficient underwriting",
            "Exclusions override endorsement"
        ],
        resolution_strategy="Negotiate with underwriter; obtain legal review of endorsements.",
        entity_scope="Lenders, owners, title insurers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="First American Title Ins. Co. v. J.P. Morgan Chase & Co., 402 F.3d 337 (2d Cir. 2005)"
    ),
    DoctrineBlock(
        topic="Subordination, Non-Disturbance, and Attornment Agreement (SNDA)",
        keywords=["SNDA", "subordination", "non-disturbance", "attornment", "tenant", "lender"],
        conclusion_template="An SNDA agreement clarifies the relationship between tenant, landlord, and lender in the event of foreclosure.",
        reasoning_framework="""
1. Define the three components: subordination, non-disturbance, and attornment.
2. Review lease and loan documents for SNDA requirements.
3. Analyze the effect of subordination on tenant's leasehold interest.
4. Assess lender's obligation to honor lease post-foreclosure (non-disturbance).
5. Confirm tenant's obligation to recognize lender as new landlord (attornment).
6. Evaluate the impact on tenant's remedies and rights.
7. Review negotiation points: cure rights, notice requirements, rent application.
8. Consider statutory protections for tenants in certain jurisdictions.
9. Synthesize to determine enforceability and adequacy of SNDA.
""",
        key_factors=[
            "Lease and loan terms",
            "SNDA language",
            "Jurisdictional tenant protections",
            "Notice and cure rights",
            "Foreclosure process"
        ],
        primary_authority=[
            "Lease agreement",
            "Loan agreement",
            "State foreclosure statutes"
        ],
        burden_holder="Tenant (for non-disturbance), Lender (for subordination)",
        adversary_position="Lender may seek broader subordination; tenant may seek stronger non-disturbance.",
        counter_arguments=[
            "SNDA not executed",
            "Statutory override",
            "Ambiguous terms"
        ],
        resolution_strategy="Negotiate clear SNDA; legal review for enforceability.",
        entity_scope="Tenants, landlords, lenders",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="In re 48th Street Steakhouse, Inc., 835 F.2d 427 (2d Cir. 1987)"
    ),
    DoctrineBlock(
        topic="Gross Lease vs Modified Gross Lease",
        keywords=["gross lease", "modified gross lease", "operating expenses", "base year", "expense stop"],
        conclusion_template="A gross lease requires the landlord to pay all operating expenses, while a modified gross lease allocates some expenses to the tenant.",
        reasoning_framework="""
1. Define the expense allocation in the lease document.
2. Identify any base year or expense stop provisions.
3. Analyze the impact on rent calculation and escalation clauses.
4. Review local law for default expense allocation.
5. Assess the effect on tenant's occupancy costs and landlord's risk.
6. Evaluate the implications for lender underwriting and property valuation.
7. Consider negotiation history and course of performance.
8. Synthesize to determine the parties' respective expense obligations.
""",
        key_factors=[
            "Lease language",
            "Base year/expense stop",
            "Local law",
            "Rent escalation provisions",
            "Negotiation history"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Landlord (gross lease), Tenant (modified gross lease)",
        adversary_position="Tenant may dispute expense allocation; landlord may seek to shift more costs.",
        counter_arguments=[
            "Ambiguity in lease",
            "Statutory overrides",
            "Implied obligations"
        ],
        resolution_strategy="Interpret lease strictly; apply contra proferentem if ambiguous.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Sullivan v. Commonwealth, 174 Va. 482 (1940)"
    ),
    DoctrineBlock(
        topic="Mezzanine Loan and Intercreditor Agreement",
        keywords=["mezzanine loan", "intercreditor agreement", "senior lender", "foreclosure", "UCC sale"],
        conclusion_template="Mezzanine loans are secured by equity interests and governed by intercreditor agreements that allocate rights between senior and mezzanine lenders.",
        reasoning_framework="""
1. Identify the collateral for the mezzanine loan (typically equity interests in property owner).
2. Review the intercreditor agreement for rights and restrictions.
3. Analyze foreclosure procedures (UCC sale vs. mortgage foreclosure).
4. Assess the impact of standstill and cure rights.
5. Evaluate the priority of payments and remedies.
6. Consider the effect of bankruptcy filings by borrower or property owner.
7. Review limitations on mezzanine lender's ability to take control.
8. Analyze the impact on property operations and tenant rights.
9. Synthesize to determine enforceability and risk allocation.
""",
        key_factors=[
            "Collateral type",
            "Intercreditor agreement terms",
            "Foreclosure process",
            "Bankruptcy implications",
            "Priority of payments"
        ],
        primary_authority=[
            "Intercreditor agreement",
            "UCC Article 9",
            "State foreclosure statutes"
        ],
        burden_holder="Mezzanine lender",
        adversary_position="Senior lender may restrict mezzanine lender remedies.",
        counter_arguments=[
            "Improper UCC sale",
            "Violation of standstill provisions",
            "Bankruptcy stay"
        ],
        resolution_strategy="Strict adherence to intercreditor agreement and UCC procedures.",
        entity_scope="Mezzanine lenders, senior lenders, borrowers",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="In re General Growth Properties, Inc., 409 B.R. 43 (Bankr. S.D.N.Y. 2009)"
    ),
    DoctrineBlock(
        topic="Construction Loan Mechanics and Holdbacks",
        keywords=["construction loan", "holdback", "draw request", "lien waiver", "inspection"],
        conclusion_template="Construction loans disburse funds in stages, with holdbacks to ensure completion and protect against liens.",
        reasoning_framework="""
1. Review loan agreement for draw schedule and conditions precedent.
2. Confirm requirements for lien waivers and contractor affidavits.
3. Analyze inspection and approval process for each draw.
4. Assess the calculation and release of holdbacks.
5. Evaluate the impact of change orders and cost overruns.
6. Consider statutory lien rights and notice requirements.
7. Review remedies for non-completion or defective work.
8. Synthesize to determine lender and borrower rights and obligations.
""",
        key_factors=[
            "Draw schedule",
            "Lien waiver requirements",
            "Inspection process",
            "Holdback calculation",
            "Change order procedures"
        ],
        primary_authority=[
            "Loan agreement",
            "State mechanic's lien statutes",
            "AIA contract documents"
        ],
        burden_holder="Borrower (to satisfy draw conditions), Lender (to disburse funds)",
        adversary_position="Borrower may challenge holdback or draw denial; contractor may assert lien rights.",
        counter_arguments=[
            "Improper denial of draw",
            "Failure to release holdback",
            "Unresolved liens"
        ],
        resolution_strategy="Strict compliance with loan and statutory requirements; negotiate resolution of disputes.",
        entity_scope="Lenders, borrowers, contractors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re 199 East 7th St. LLC, 572 B.R. 57 (Bankr. S.D.N.Y. 2017)"
    ),
    DoctrineBlock(
        topic="CAM Reconciliation and Audit Rights",
        keywords=["CAM", "common area maintenance", "reconciliation", "audit rights", "tenant"],
        conclusion_template="Tenants may audit landlord's CAM expense reconciliations to verify accuracy and compliance with lease terms.",
        reasoning_framework="""
1. Review lease for CAM expense definitions and reconciliation procedures.
2. Identify tenant's audit rights, including timing and scope.
3. Assess landlord's obligations to provide supporting documentation.
4. Analyze dispute resolution procedures for CAM disagreements.
5. Evaluate the impact of audit findings on future CAM charges.
6. Consider statutory requirements for expense disclosure.
7. Synthesize to determine tenant's audit and challenge rights.
""",
        key_factors=[
            "Lease language",
            "Audit right scope",
            "Documentation requirements",
            "Dispute resolution procedures",
            "Statutory disclosure"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Industry standards (BOMA)"
        ],
        burden_holder="Tenant (to request audit), Landlord (to provide records)",
        adversary_position="Landlord may limit audit scope or deny access.",
        counter_arguments=[
            "Audit right waived",
            "Insufficient documentation",
            "Statutory overrides"
        ],
        resolution_strategy="Negotiate clear audit provisions; enforce through lease remedies.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Wells Fargo Bank, N.A. v. 310 Associates, LLC, 2012 NY Slip Op 32442(U)"
    ),
    DoctrineBlock(
        topic="Percentage Rent in Retail Leases",
        keywords=["percentage rent", "retail lease", "gross sales", "breakpoint", "tenant reporting"],
        conclusion_template="Retail leases may require tenants to pay percentage rent based on gross sales above a specified breakpoint.",
        reasoning_framework="""
1. Review lease for percentage rent provisions and breakpoint calculation.
2. Define 'gross sales' and allowable exclusions.
3. Analyze tenant's reporting and audit obligations.
4. Assess landlord's remedies for underreporting or non-payment.
5. Evaluate the impact of returns, discounts, and online sales.
6. Consider industry standards for percentage rent structures.
7. Synthesize to determine tenant's percentage rent obligations.
""",
        key_factors=[
            "Lease language",
            "Breakpoint calculation",
            "Gross sales definition",
            "Audit/reporting requirements",
            "Industry standards"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "ICSC Retail Lease Guidelines"
        ],
        burden_holder="Tenant (to report and pay), Landlord (to audit)",
        adversary_position="Tenant may dispute gross sales calculation or exclusions.",
        counter_arguments=[
            "Ambiguous lease terms",
            "Improper breakpoint calculation",
            "Disputed sales reporting"
        ],
        resolution_strategy="Negotiate clear definitions and audit rights; enforce through lease remedies.",
        entity_scope="Retail landlords and tenants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Gimbel Bros., Inc. v. Brook Shopping Centers, Inc., 118 A.D.2d 532 (N.Y. App. Div. 1986)"
    ),
    DoctrineBlock(
        topic="Tenant Improvement Allowance and Delivery Condition",
        keywords=["tenant improvement", "TI allowance", "delivery condition", "work letter", "build-out"],
        conclusion_template="Tenant improvement allowances are governed by the lease work letter, specifying delivery condition, scope of work, and disbursement procedures.",
        reasoning_framework="""
1. Review lease and work letter for TI allowance amount and permitted uses.
2. Define landlord and tenant responsibilities for build-out.
3. Analyze delivery condition requirements (e.g., shell, white box).
4. Assess timing and process for disbursement of TI funds.
5. Evaluate documentation and lien waiver requirements.
6. Consider remedies for delays or non-compliance.
7. Synthesize to determine parties' rights and obligations regarding TI.
""",
        key_factors=[
            "Work letter terms",
            "Delivery condition",
            "Disbursement procedures",
            "Lien waiver requirements",
            "Remedies for delay"
        ],
        primary_authority=[
            "Lease agreement",
            "Work letter",
            "State construction statutes"
        ],
        burden_holder="Landlord (to deliver space), Tenant (to complete improvements)",
        adversary_position="Tenant may claim inadequate delivery; landlord may dispute TI usage.",
        counter_arguments=[
            "Ambiguous work letter",
            "Unapproved TI expenditures",
            "Delayed delivery"
        ],
        resolution_strategy="Negotiate detailed work letter; enforce through lease remedies.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Fidelity Federal Bank, FSB v. Park Place Associates, 60 Cal.App.4th 1433 (1998)"
    ),
    DoctrineBlock(
        topic="Zoning Variance and Special Use Permit",
        keywords=["zoning", "variance", "special use permit", "land use", "municipality"],
        conclusion_template="A zoning variance or special use permit allows property use not otherwise permitted under current zoning ordinances.",
        reasoning_framework="""
1. Identify the applicable zoning ordinance and property classification.
2. Determine the specific relief sought (variance or special use).
3. Review application requirements and supporting documentation.
4. Analyze criteria for granting relief (e.g., hardship, compatibility).
5. Assess public notice and hearing procedures.
6. Evaluate potential opposition and mitigation strategies.
7. Consider conditions or limitations imposed by the municipality.
8. Synthesize to determine likelihood of approval and compliance requirements.
""",
        key_factors=[
            "Zoning ordinance",
            "Relief criteria",
            "Application process",
            "Public hearing requirements",
            "Conditions of approval"
        ],
        primary_authority=[
            "Municipal zoning code",
            "State land use statutes",
            "Local planning board decisions"
        ],
        burden_holder="Applicant (property owner or developer)",
        adversary_position="Municipality or neighbors may oppose relief.",
        counter_arguments=[
            "Failure to meet hardship criteria",
            "Incompatibility with neighborhood",
            "Procedural defects"
        ],
        resolution_strategy="Prepare thorough application; address opposition; comply with conditions.",
        entity_scope="Property owners, developers, municipalities",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Village of Euclid v. Ambler Realty Co., 272 U.S. 365 (1926)"
    ),
    DoctrineBlock(
        topic="Defeasance in CMBS Loans",
        keywords=["defeasance", "CMBS", "loan payoff", "securities", "REMIC compliance"],
        conclusion_template="Defeasance allows a borrower to substitute collateral (usually government securities) for real property to release the lien and repay a CMBS loan.",
        reasoning_framework="""
1. Review loan documents for defeasance provisions and eligibility.
2. Analyze calculation of defeasance consideration (securities cost, fees).
3. Confirm compliance with REMIC and PSA requirements.
4. Assess timing and notice requirements for defeasance.
5. Evaluate the process for substitution of collateral and release of lien.
6. Consider the impact on borrower, lender, and servicer rights.
7. Synthesize to determine feasibility and cost of defeasance.
""",
        key_factors=[
            "Loan agreement terms",
            "Defeasance calculation",
            "REMIC/PSA compliance",
            "Notice and timing",
            "Collateral substitution process"
        ],
        primary_authority=[
            "Loan agreement",
            "Pooling and Servicing Agreement",
            "REMIC regulations"
        ],
        burden_holder="Borrower",
        adversary_position="Lender/servicer may dispute calculation or process.",
        counter_arguments=[
            "Improper notice",
            "Defeasance consideration dispute",
            "REMIC non-compliance"
        ],
        resolution_strategy="Strict compliance with loan and PSA terms; engage defeasance consultant.",
        entity_scope="CMBS borrowers, lenders, servicers",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re General Growth Properties, Inc., 409 B.R. 43 (Bankr. S.D.N.Y. 2009)"
    ),
    # Additional doctrines for breadth and depth
    DoctrineBlock(
        topic="Assignment and Subletting in Commercial Leases",
        keywords=["assignment", "subletting", "consent", "commercial lease", "landlord approval"],
        conclusion_template="Assignment and subletting are governed by lease terms, often requiring landlord consent, which may not be unreasonably withheld.",
        reasoning_framework="""
1. Review lease for assignment and subletting clauses.
2. Determine if landlord consent is required and any standards for withholding consent.
3. Analyze statutory or case law restrictions on withholding consent.
4. Assess the impact of assignment/subletting on tenant liability.
5. Consider the effect of assignment on lease guarantees and security deposits.
6. Evaluate procedures for requesting and documenting consent.
7. Synthesize to determine rights and remedies for both parties.
""",
        key_factors=[
            "Lease language",
            "Consent standards",
            "Statutory restrictions",
            "Tenant liability post-assignment",
            "Procedural requirements"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Tenant (to request consent), Landlord (to respond)",
        adversary_position="Landlord may withhold consent; tenant may challenge reasonableness.",
        counter_arguments=[
            "Unreasonable withholding of consent",
            "Assignment without consent",
            "Statutory overrides"
        ],
        resolution_strategy="Negotiate clear consent standards; enforce through lease remedies.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Kendall v. Ernest Pestana, Inc., 40 Cal.3d 488 (1985)"
    ),
    DoctrineBlock(
        topic="Estoppel Certificate in Commercial Transactions",
        keywords=["estoppel certificate", "tenant", "lender", "buyer", "lease representations"],
        conclusion_template="An estoppel certificate binds the tenant to representations about lease status, rent, and defaults, relied upon by lenders and buyers.",
        reasoning_framework="""
1. Review lease for estoppel certificate requirements and timing.
2. Analyze the scope of representations requested.
3. Assess the tenant's duty to disclose defaults or disputes.
4. Evaluate the impact of estoppel certificate on future claims.
5. Consider remedies for failure to deliver or inaccurate certificates.
6. Synthesize to determine enforceability and reliance by third parties.
""",
        key_factors=[
            "Lease requirements",
            "Scope of representations",
            "Disclosure of defaults",
            "Reliance by third parties",
            "Remedies for non-delivery"
        ],
        primary_authority=[
            "Lease agreement",
            "State real estate statutes",
            "Restatement (Second) of Contracts"
        ],
        burden_holder="Tenant (to deliver accurate certificate)",
        adversary_position="Lender/buyer may challenge accuracy; tenant may dispute reliance.",
        counter_arguments=[
            "Inaccurate or incomplete certificate",
            "Failure to disclose disputes",
            "Non-delivery"
        ],
        resolution_strategy="Negotiate clear estoppel requirements; enforce through transaction remedies.",
        entity_scope="Tenants, landlords, lenders, buyers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="In re 222 Liberty Associates, 108 B.R. 971 (Bankr. E.D. Pa. 1990)"
    ),
    DoctrineBlock(
        topic="Due Diligence in Commercial Real Estate Acquisitions",
        keywords=["due diligence", "acquisition", "property inspection", "title review", "environmental"],
        conclusion_template="Comprehensive due diligence is essential to identify risks and validate representations in commercial real estate acquisitions.",
        reasoning_framework="""
1. Conduct physical inspection of property and improvements.
2. Review title, survey, and zoning compliance.
3. Analyze environmental reports (Phase I/II).
4. Assess lease abstracts and rent rolls.
5. Evaluate service contracts, permits, and licenses.
6. Review financial statements and operating history.
7. Synthesize findings to determine transaction risk and negotiation points.
""",
        key_factors=[
            "Physical inspection",
            "Title and survey review",
            "Environmental assessment",
            "Lease analysis",
            "Financial due diligence"
        ],
        primary_authority=[
            "Purchase agreement",
            "State real estate statutes",
            "Industry due diligence checklists"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may limit access or representations.",
        counter_arguments=[
            "Incomplete due diligence",
            "Misrepresentation",
            "Access limitations"
        ],
        resolution_strategy="Negotiate access and representations; include due diligence contingencies.",
        entity_scope="Buyers, sellers, lenders",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Merrill Lynch Interfunding, Inc. v. Argenti, 155 F.3d 113 (2d Cir. 1998)"
    ),
    DoctrineBlock(
        topic="Non-Recourse Carveouts (Bad Boy Guarantees)",
        keywords=["non-recourse", "carveout", "bad boy guarantee", "loan", "recourse liability"],
        conclusion_template="Non-recourse loans may become partially or fully recourse if borrower triggers carveout events, such as fraud or misappropriation.",
        reasoning_framework="""
1. Review loan agreement and guaranty for carveout provisions.
2. Identify specific events that trigger recourse liability.
3. Analyze the scope of liability and parties responsible.
4. Assess the impact of carveouts on borrower and guarantor risk.
5. Consider recent case law on enforceability and interpretation.
6. Synthesize to determine exposure to recourse liability.
""",
        key_factors=[
            "Carveout events",
            "Scope of liability",
            "Guarantor parties",
            "Loan agreement terms",
            "Recent case law"
        ],
        primary_authority=[
            "Loan agreement",
            "Guaranty agreement",
            "State contract law"
        ],
        burden_holder="Lender (to prove carveout event)",
        adversary_position="Borrower/guarantor may dispute occurrence or scope.",
        counter_arguments=[
            "Event not covered by carveout",
            "Ambiguous language",
            "Waiver or estoppel"
        ],
        resolution_strategy="Negotiate clear carveout language; document events and communications.",
        entity_scope="Borrowers, lenders, guarantors",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Wells Fargo Bank, N.A. v. Cherryland Mall Ltd. P’ship, 812 N.W.2d 799 (Mich. Ct. App. 2011)"
    ),
    DoctrineBlock(
        topic="Condominium Conversion and Deconversion",
        keywords=["condominium", "conversion", "deconversion", "unit owner", "association"],
        conclusion_template="Condominium conversion and deconversion require compliance with statutory procedures and supermajority owner approval.",
        reasoning_framework="""
1. Review state condominium statutes for conversion/deconversion procedures.
2. Analyze association governing documents for voting requirements.
3. Assess notice and disclosure obligations to unit owners and tenants.
4. Evaluate the impact on existing leases and common area interests.
5. Consider lender consent and mortgage implications.
6. Synthesize to determine feasibility and compliance requirements.
""",
        key_factors=[
            "Statutory procedures",
            "Governing documents",
            "Owner approval thresholds",
            "Notice requirements",
            "Lender consent"
        ],
        primary_authority=[
            "State condominium statutes",
            "Association bylaws",
            "Purchase and sale agreements"
        ],
        burden_holder="Sponsor/association",
        adversary_position="Minority owners may challenge process or valuation.",
        counter_arguments=[
            "Insufficient owner approval",
            "Procedural defects",
            "Improper notice"
        ],
        resolution_strategy="Strict compliance with statutory and governing document requirements.",
        entity_scope="Unit owners, associations, sponsors",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="770 Park Ave. Condominium v. Patrician, 2019 NY Slip Op 30633(U)"
    ),
    DoctrineBlock(
        topic="Ground Lease Structure and Financing",
        keywords=["ground lease", "land lease", "financing", "leasehold mortgage", "term"],
        conclusion_template="Ground leases separate ownership of land and improvements, with long terms and unique financing considerations.",
        reasoning_framework="""
1. Review ground lease for term, rent structure, and permitted uses.
2. Analyze leasehold mortgage provisions and lender protections.
3. Assess reversion and surrender requirements at lease end.
4. Evaluate subordination and non-disturbance protections.
5. Consider impact on financing, including lender underwriting standards.
6. Synthesize to determine rights and risks for all parties.
""",
        key_factors=[
            "Lease term and rent",
            "Leasehold mortgage provisions",
            "Reversion requirements",
            "Lender protections",
            "Permitted uses"
        ],
        primary_authority=[
            "Ground lease agreement",
            "State real estate statutes",
            "Lender underwriting guidelines"
        ],
        burden_holder="Tenant/lessee",
        adversary_position="Landlord may restrict financing; lender may require additional protections.",
        counter_arguments=[
            "Insufficient lease term",
            "Restrictive use clauses",
            "Lack of lender protections"
        ],
        resolution_strategy="Negotiate lease and lender protections; legal review for enforceability.",
        entity_scope="Landlords, tenants, lenders",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Empire State Building Co. v. New York, 254 N.Y. 542 (1930)"
    ),
    DoctrineBlock(
        topic="Lease Guaranty Enforcement",
        keywords=["lease guaranty", "guarantor", "enforcement", "commercial lease", "default"],
        conclusion_template="Lease guaranties are strictly construed and enforceable according to their terms, subject to defenses such as fraud or material alteration.",
        reasoning_framework="""
1. Review guaranty agreement for scope and duration of liability.
2. Assess the occurrence of default under the lease.
3. Analyze any defenses asserted by guarantor (e.g., fraud, modification).
4. Evaluate notice and demand requirements.
5. Consider impact of lease amendments on guaranty enforceability.
6. Synthesize to determine likelihood of enforcement.
""",
        key_factors=[
            "Guaranty terms",
            "Default occurrence",
            "Defenses asserted",
            "Notice requirements",
            "Lease amendments"
        ],
        primary_authority=[
            "Guaranty agreement",
            "Lease agreement",
            "State contract law"
        ],
        burden_holder="Landlord (to prove default and guaranty terms)",
        adversary_position="Guarantor may assert defenses or limit liability.",
        counter_arguments=[
            "Material alteration of lease",
            "Lack of notice",
            "Fraud or duress"
        ],
        resolution_strategy="Strict construction of guaranty; document all amendments and notices.",
        entity_scope="Landlords, tenants, guarantors",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Chemical Bank v. Meltzer, 93 N.Y.2d 296 (1999)"
    ),
    DoctrineBlock(
        topic="Lease Renewal and Holdover Tenancy",
        keywords=["lease renewal", "holdover", "tenancy", "commercial lease", "rent escalation"],
        conclusion_template="Lease renewal and holdover are governed by lease terms and statutory law, with holdover tenants often liable for increased rent.",
        reasoning_framework="""
1. Review lease for renewal options and notice requirements.
2. Analyze automatic renewal or holdover provisions.
3. Assess statutory protections or limitations on holdover tenancies.
4. Evaluate calculation of holdover rent and damages.
5. Consider remedies for landlord and tenant upon holdover.
6. Synthesize to determine parties' rights and obligations.
""",
        key_factors=[
            "Lease renewal terms",
            "Notice requirements",
            "Holdover provisions",
            "Statutory protections",
            "Rent escalation"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Tenant (to exercise renewal), Landlord (to enforce holdover remedies)",
        adversary_position="Tenant may dispute holdover rent; landlord may seek eviction.",
        counter_arguments=[
            "Improper notice",
            "Ambiguous lease terms",
            "Statutory overrides"
        ],
        resolution_strategy="Strict compliance with notice and lease terms; seek judicial remedies if necessary.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Henderson v. Stevenson, 11 N.Y.2d 923 (1962)"
    ),
    DoctrineBlock(
        topic="Eminent Domain and Condemnation Provisions",
        keywords=["eminent domain", "condemnation", "compensation", "lease", "allocation"],
        conclusion_template="Eminent domain provisions allocate condemnation awards between landlord and tenant based on lease terms and applicable law.",
        reasoning_framework="""
1. Review lease for condemnation and eminent domain clauses.
2. Analyze allocation of compensation for taking of all or part of premises.
3. Assess tenant's right to terminate or abate rent.
4. Evaluate statutory requirements for notice and compensation.
5. Consider impact on lender rights and security interests.
6. Synthesize to determine distribution of award and parties' remedies.
""",
        key_factors=[
            "Lease condemnation clause",
            "Compensation allocation",
            "Tenant termination rights",
            "Statutory requirements",
            "Lender interests"
        ],
        primary_authority=[
            "Lease agreement",
            "State eminent domain statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Condemning authority (to pay compensation), Parties (to allocate)",
        adversary_position="Landlord and tenant may dispute allocation; lender may assert priority.",
        counter_arguments=[
            "Ambiguous lease terms",
            "Statutory overrides",
            "Lender priority"
        ],
        resolution_strategy="Negotiate clear allocation; seek judicial determination if disputed.",
        entity_scope="Landlords, tenants, lenders, condemning authorities",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="United States v. Petty Motor Co., 327 U.S. 372 (1946)"
    ),
    DoctrineBlock(
        topic="Environmental Indemnity in Commercial Loans",
        keywords=["environmental indemnity", "loan", "hazardous materials", "borrower liability", "lender protection"],
        conclusion_template="Environmental indemnity agreements shift liability for environmental contamination from lender to borrower, often surviving loan repayment.",
        reasoning_framework="""
1. Review indemnity agreement for scope and duration of liability.
2. Analyze covered events and excluded conditions.
3. Assess the impact of indemnity on borrower and guarantor risk.
4. Evaluate lender's remedies for breach or non-compliance.
5. Consider statutory limitations on indemnification.
6. Synthesize to determine enforceability and risk allocation.
""",
        key_factors=[
            "Indemnity scope",
            "Covered events",
            "Excluded conditions",
            "Remedies for breach",
            "Statutory limitations"
        ],
        primary_authority=[
            "Indemnity agreement",
            "Loan agreement",
            "CERCLA and state environmental statutes"
        ],
        burden_holder="Borrower/guarantor",
        adversary_position="Borrower may dispute scope or duration; lender may seek broader coverage.",
        counter_arguments=[
            "Statutory limits on indemnity",
            "Ambiguous language",
            "Lack of notice"
        ],
        resolution_strategy="Negotiate clear indemnity language; legal review for enforceability.",
        entity_scope="Borrowers, lenders, guarantors",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Bank of America v. CDP, 991 F. Supp. 2d 818 (S.D. Tex. 2014)"
    ),
    DoctrineBlock(
        topic="Brokerage Commission Agreements",
        keywords=["brokerage", "commission", "listing agreement", "procuring cause", "real estate broker"],
        conclusion_template="Brokerage commissions are governed by written agreements and the broker's status as procuring cause of the transaction.",
        reasoning_framework="""
1. Review brokerage agreement for commission terms and triggers.
2. Analyze broker's actions to determine procuring cause.
3. Assess statutory requirements for written agreements.
4. Evaluate timing and calculation of commission payments.
5. Consider disputes over dual agency or exclusivity.
6. Synthesize to determine entitlement and enforceability of commission.
""",
        key_factors=[
            "Written agreement",
            "Procuring cause",
            "Statutory requirements",
            "Commission calculation",
            "Agency disclosures"
        ],
        primary_authority=[
            "Brokerage agreement",
            "State real estate statutes",
            "NAR Code of Ethics"
        ],
        burden_holder="Broker (to prove procuring cause), Principal (to pay commission)",
        adversary_position="Principal may dispute broker's role or agreement validity.",
        counter_arguments=[
            "Lack of written agreement",
            "No procuring cause",
            "Dual agency conflict"
        ],
        resolution_strategy="Document broker's involvement; comply with statutory and ethical requirements.",
        entity_scope="Brokers, principals, buyers, sellers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Greene v. Hellman, 51 N.Y.2d 197 (1980)"
    ),
    DoctrineBlock(
        topic="Lease Default and Cure Rights",
        keywords=["lease default", "cure rights", "notice", "remedies", "commercial lease"],
        conclusion_template="Lease default and cure rights are governed by lease terms and statutory law, with notice and opportunity to cure required before remedies are enforced.",
        reasoning_framework="""
1. Review lease for default definitions and cure provisions.
2. Analyze notice requirements and timing.
3. Assess tenant's right to cure and landlord's remedies upon failure.
4. Evaluate statutory protections for tenants.
5. Consider impact of repeated or incurable defaults.
6. Synthesize to determine enforceability and available remedies.
""",
        key_factors=[
            "Default definitions",
            "Notice and cure provisions",
            "Statutory protections",
            "Remedies for breach",
            "Repeat/inexcusable defaults"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Landlord (to prove default and notice)",
        adversary_position="Tenant may dispute default or assert cure.",
        counter_arguments=[
            "Improper notice",
            "Timely cure",
            "Statutory overrides"
        ],
        resolution_strategy="Strict compliance with notice and cure provisions; seek judicial remedies if necessary.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Riverside Research Inst. v. KMGA, Inc., 68 N.Y.2d 689 (1986)"
    ),
    DoctrineBlock(
        topic="Subrogation Waivers in Commercial Leases",
        keywords=["subrogation", "waiver", "insurance", "commercial lease", "landlord", "tenant"],
        conclusion_template="Subrogation waivers prevent insurers from pursuing claims against the other party to the lease, reducing litigation risk.",
        reasoning_framework="""
1. Review lease for subrogation waiver clauses.
2. Analyze insurance policies for compatibility with waiver.
3. Assess the impact on risk allocation and premium costs.
4. Evaluate enforceability under state law.
5. Consider effect on third-party claims and indemnity provisions.
6. Synthesize to determine effectiveness and compliance.
""",
        key_factors=[
            "Lease waiver language",
            "Insurance policy terms",
            "State law",
            "Risk allocation",
            "Third-party claims"
        ],
        primary_authority=[
            "Lease agreement",
            "Insurance policy",
            "State insurance statutes"
        ],
        burden_holder="Party seeking enforcement",
        adversary_position="Insurer may deny coverage; opposing party may dispute waiver.",
        counter_arguments=[
            "Policy does not permit waiver",
            "Statutory restrictions",
            "Ambiguous lease terms"
        ],
        resolution_strategy="Coordinate lease and insurance terms; obtain insurer consent.",
        entity_scope="Landlords, tenants, insurers",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Great Northern Oil Co. v. St. Paul Fire & Marine Ins. Co., 303 Minn. 267 (1975)"
    ),
    DoctrineBlock(
        topic="Exclusive Use Provisions in Retail Leases",
        keywords=["exclusive use", "retail lease", "tenant", "landlord", "competing business"],
        conclusion_template="Exclusive use provisions restrict the landlord from leasing to competing businesses, protecting tenant's market position.",
        reasoning_framework="""
1. Review lease for exclusive use language and scope.
2. Analyze exceptions and carve-outs (e.g., existing tenants).
3. Assess remedies for breach, including rent abatement or termination.
4. Evaluate enforceability under state law and public policy.
5. Consider impact on landlord's leasing flexibility and property value.
6. Synthesize to determine effectiveness and risk of challenge.
""",
        key_factors=[
            "Exclusive use clause",
            "Exceptions/carve-outs",
            "Remedies for breach",
            "State law",
            "Landlord flexibility"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "ICSC Retail Lease Guidelines"
        ],
        burden_holder="Tenant (to prove breach), Landlord (to defend exceptions)",
        adversary_position="Landlord may challenge scope or assert exceptions.",
        counter_arguments=[
            "Ambiguous language",
            "Pre-existing tenants",
            "Public policy limits"
        ],
        resolution_strategy="Negotiate clear exclusive use terms; enforce through lease remedies.",
        entity_scope="Retail landlords and tenants",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Food Fair Stores, Inc. v. Blumberg, 234 Md. 521 (1964)"
    ),
    DoctrineBlock(
        topic="Operating Expense Gross-Up Provisions",
        keywords=["operating expense", "gross-up", "commercial lease", "occupancy", "CAM"],
        conclusion_template="Gross-up provisions adjust operating expenses to reflect full occupancy, ensuring equitable expense allocation among tenants.",
        reasoning_framework="""
1. Review lease for gross-up provision language and calculation method.
2. Analyze impact on tenant's share of expenses and rent escalation.
3. Assess compliance with industry standards (e.g., BOMA).
4. Evaluate transparency and documentation of gross-up calculations.
5. Consider disputes over expense allocation and reconciliation.
6. Synthesize to determine enforceability and fairness.
""",
        key_factors=[
            "Gross-up clause",
            "Calculation method",
            "Industry standards",
            "Transparency",
            "Expense reconciliation"
        ],
        primary_authority=[
            "Lease agreement",
            "BOMA standards",
            "State landlord-tenant statutes"
        ],
        burden_holder="Landlord (to justify calculation), Tenant (to challenge)",
        adversary_position="Tenant may dispute calculation or fairness.",
        counter_arguments=[
            "Improper calculation",
            "Lack of transparency",
            "Ambiguous lease terms"
        ],
        resolution_strategy="Negotiate clear gross-up terms; provide supporting documentation.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Gimbel Bros., Inc. v. Brook Shopping Centers, Inc., 118 A.D.2d 532 (N.Y. App. Div. 1986)"
    ),
    DoctrineBlock(
        topic="Force Majeure in Commercial Real Estate Contracts",
        keywords=["force majeure", "commercial lease", "contract", "impossibility", "excused performance"],
        conclusion_template="Force majeure clauses may excuse or delay performance due to specified extraordinary events beyond the parties' control.",
        reasoning_framework="""
1. Review contract or lease for force majeure language and covered events.
2. Analyze notice requirements and timing.
3. Assess the impact on rent, deadlines, and remedies.
4. Evaluate statutory or common law doctrines of impossibility or frustration.
5. Consider recent case law (e.g., COVID-19 pandemic).
6. Synthesize to determine applicability and enforceability.
""",
        key_factors=[
            "Force majeure clause",
            "Covered events",
            "Notice requirements",
            "Impact on obligations",
            "Recent case law"
        ],
        primary_authority=[
            "Lease or contract",
            "State contract law",
            "Restatement (Second) of Contracts"
        ],
        burden_holder="Party seeking excuse",
        adversary_position="Counterparty may dispute applicability or scope.",
        counter_arguments=[
            "Event not covered",
            "Improper notice",
            "Mitigation required"
        ],
        resolution_strategy="Strict compliance with notice and mitigation; legal review of clause.",
        entity_scope="Landlords, tenants, contracting parties",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="J.N.A. Realty Corp. v. Cross Bay Chelsea, Inc., 42 N.Y.2d 392 (1977)"
    ),
    DoctrineBlock(
        topic="SNDA Recording and Priority Issues",
        keywords=["SNDA", "recording", "priority", "leasehold", "mortgage"],
        conclusion_template="Recording SNDAs and related documents establishes priority and protects tenant and lender rights in foreclosure.",
        reasoning_framework="""
1. Review SNDA and lease for recording requirements.
2. Analyze state recording statutes and notice rules.
3. Assess impact of recording on priority of interests.
4. Evaluate risks of unrecorded SNDAs (e.g., bona fide purchaser).
5. Synthesize to determine steps for protecting parties' interests.
""",
        key_factors=[
            "Recording statutes",
            "Notice requirements",
            "Priority of interests",
            "Lease and SNDA terms",
            "Foreclosure risk"
        ],
        primary_authority=[
            "State recording statutes",
            "Lease agreement",
            "SNDA agreement"
        ],
        burden_holder="Tenant/lender (to record), Landlord (to cooperate)",
        adversary_position="Subsequent purchasers or lenders may challenge priority.",
        counter_arguments=[
            "Failure to record",
            "Improper indexing",
            "Statutory overrides"
        ],
        resolution_strategy="Record SNDA and lease promptly; obtain title insurance coverage.",
        entity_scope="Tenants, landlords, lenders, purchasers",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="In re 48th Street Steakhouse, Inc., 835 F.2d 427 (2d Cir. 1987)"
    ),
    DoctrineBlock(
        topic="Tenant Relocation Clauses",
        keywords=["tenant relocation", "commercial lease", "landlord right", "replacement space", "compensation"],
        conclusion_template="Tenant relocation clauses allow landlords to move tenants to comparable space, subject to notice and compensation requirements.",
        reasoning_framework="""
1. Review lease for relocation clause and triggering events.
2. Analyze requirements for replacement space (size, location, quality).
3. Assess notice and timing provisions.
4. Evaluate compensation for moving costs and business interruption.
5. Consider remedies for failure to provide comparable space.
6. Synthesize to determine enforceability and tenant protections.
""",
        key_factors=[
            "Relocation clause language",
            "Replacement space requirements",
            "Notice and timing",
            "Compensation provisions",
            "Remedies for breach"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Landlord (to provide comparable space and compensation)",
        adversary_position="Tenant may dispute comparability or adequacy of compensation.",
        counter_arguments=[
            "Inadequate replacement space",
            "Insufficient notice",
            "Uncompensated costs"
        ],
        resolution_strategy="Negotiate detailed relocation terms; enforce through lease remedies.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Wells Fargo Bank, N.A. v. 310 Associates, LLC, 2012 NY Slip Op 32442(U)"
    ),
    DoctrineBlock(
        topic="Lease Termination Options and Early Exit Rights",
        keywords=["lease termination", "early exit", "break clause", "commercial lease", "penalty"],
        conclusion_template="Early termination options are governed by lease terms, often requiring notice and payment of a penalty or unamortized costs.",
        reasoning_framework="""
1. Review lease for early termination or break clause provisions.
2. Analyze notice requirements and timing.
3. Assess calculation of penalty or reimbursement of costs.
4. Evaluate impact on landlord's leasing and financing.
5. Consider remedies for improper termination.
6. Synthesize to determine enforceability and risk allocation.
""",
        key_factors=[
            "Termination clause terms",
            "Notice requirements",
            "Penalty calculation",
            "Impact on landlord",
            "Remedies for breach"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Tenant (to comply with terms), Landlord (to enforce penalties)",
        adversary_position="Landlord may dispute compliance or seek additional damages.",
        counter_arguments=[
            "Improper notice",
            "Disputed penalty calculation",
            "Statutory overrides"
        ],
        resolution_strategy="Negotiate clear termination terms; enforce through lease remedies.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="J.N.A. Realty Corp. v. Cross Bay Chelsea, Inc., 42 N.Y.2d 392 (1977)"
    ),
    DoctrineBlock(
        topic="Security Deposit Requirements and Disputes",
        keywords=["security deposit", "commercial lease", "escrow", "return", "deductions"],
        conclusion_template="Security deposits must be handled in accordance with lease terms and applicable law, with disputes resolved through accounting and documentation.",
        reasoning_framework="""
1. Review lease for security deposit amount, escrow requirements, and permitted deductions.
2. Analyze statutory requirements for holding and returning deposits.
3. Assess timing and documentation of deductions.
4. Evaluate remedies for improper withholding or failure to return.
5. Synthesize to determine compliance and dispute resolution.
""",
        key_factors=[
            "Lease terms",
            "Statutory requirements",
            "Escrow/accounting",
            "Permitted deductions",
            "Remedies for breach"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Landlord (to account for and return deposit)",
        adversary_position="Tenant may dispute deductions or demand return.",
        counter_arguments=[
            "Improper deductions",
            "Failure to account",
            "Statutory penalties"
        ],
        resolution_strategy="Maintain detailed accounting; comply with statutory and lease requirements.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Matter of 89 Christopher Corp. v. Joy, 35 N.Y.2d 213 (1974)"
    ),
    DoctrineBlock(
        topic="Access and Quiet Enjoyment in Commercial Leases",
        keywords=["quiet enjoyment", "access", "landlord entry", "tenant rights", "commercial lease"],
        conclusion_template="Tenants are entitled to quiet enjoyment, subject to landlord's limited right of access for repairs, inspection, or emergencies.",
        reasoning_framework="""
1. Review lease for quiet enjoyment and access clauses.
2. Analyze scope and limits of landlord's right of entry.
3. Assess notice requirements and timing.
4. Evaluate remedies for breach of quiet enjoyment.
5. Consider statutory protections and common law principles.
6. Synthesize to determine enforceability and remedies.
""",
        key_factors=[
            "Lease terms",
            "Notice and access requirements",
            "Scope of landlord entry",
            "Remedies for breach",
            "Statutory protections"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "Restatement (Second) of Property: Landlord & Tenant"
        ],
        burden_holder="Landlord (to comply with entry limits), Tenant (to assert breach)",
        adversary_position="Tenant may claim constructive eviction; landlord may assert necessity.",
        counter_arguments=[
            "Emergency access",
            "Tenant consent",
            "Implied waiver"
        ],
        resolution_strategy="Comply with notice and entry requirements; document all access.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Barash v. Pennsylvania Terminal Real Estate Corp., 26 N.Y.2d 77 (1970)"
    ),
    DoctrineBlock(
        topic="Co-Tenancy Clauses in Retail Leases",
        keywords=["co-tenancy", "retail lease", "anchor tenant", "rent abatement", "termination right"],
        conclusion_template="Co-tenancy clauses allow tenants to reduce rent or terminate the lease if key tenants or occupancy thresholds are not met.",
        reasoning_framework="""
1. Review lease for co-tenancy requirements and remedies.
2. Analyze definitions of anchor tenants and occupancy thresholds.
3. Assess procedures for rent abatement or termination.
4. Evaluate impact on landlord's leasing strategy and property value.
5. Consider enforceability under state law and public policy.
6. Synthesize to determine effectiveness and risk allocation.
""",
        key_factors=[
            "Co-tenancy clause",
            "Anchor tenant/occupancy definitions",
            "Remedies for failure",
            "Landlord leasing strategy",
            "State law"
        ],
        primary_authority=[
            "Lease agreement",
            "State landlord-tenant statutes",
            "ICSC Retail Lease Guidelines"
        ],
        burden_holder="Tenant (to prove failure), Landlord (to cure or contest)",
        adversary_position="Landlord may dispute failure or assert cure.",
        counter_arguments=[
            "Ambiguous definitions",
            "Temporary closures",
            "Public policy limits"
        ],
        resolution_strategy="Negotiate clear co-tenancy terms; enforce through lease remedies.",
        entity_scope="Retail landlords and tenants",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Old Navy, LLC v. CenterMark Properties Meriden Square, Inc., 2013 Conn. Super. LEXIS 1707"
    ),
    DoctrineBlock(
        topic="Leasehold Mortgage and Foreclosure",
        keywords=["leasehold mortgage", "foreclosure", "ground lease", "lender", "tenant default"],
        conclusion_template="Leasehold mortgages secure tenant's leasehold interest, with foreclosure procedures governed by lease and state law.",
        reasoning_framework="""
1. Review lease and mortgage for foreclosure procedures and lender protections.
2. Analyze notice and cure rights for landlord and lender.
3. Assess impact of foreclosure on lease and tenant's rights.
4. Evaluate statutory requirements for leasehold foreclosure.
5. Consider remedies for landlord and lender upon default.
6. Synthesize to determine enforceability and risk allocation.
""",
        key_factors=[
            "Foreclosure procedures",
            "Notice and cure rights",
            "Lease and mortgage terms",
            "Statutory requirements",
            "Remedies for default"
        ],
        primary_authority=[
            "Lease agreement",
            "Mortgage agreement",
            "State foreclosure statutes"
        ],
        burden_holder="Lender (to comply with procedures), Landlord (to enforce remedies)",
        adversary_position="Tenant may dispute default; landlord may challenge lender rights.",
        counter_arguments=[
            "Improper notice",
            "Ambiguous lease terms",
            "Statutory overrides"
        ],
        resolution_strategy="Strict compliance with lease and statutory procedures; obtain SNDA.",
        entity_scope="Tenants, landlords, lenders",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="In re General Growth Properties, Inc., 409 B.R. 43 (Bankr. S.D.N.Y. 2009)"
    ),
    DoctrineBlock(
        topic="Rent Acceleration and Liquidated Damages",
        keywords=["rent acceleration", "liquidated damages", "lease default", "commercial lease", "remedies"],
        conclusion_template="Rent acceleration and liquidated damages clauses must be reasonable and not constitute a penalty to be enforceable.",
        reasoning_framework="""
1. Review lease for acceleration and liquidated damages provisions.
2. Analyze reasonableness of damages in relation to anticipated harm.
3. Assess enforceability under state law and public policy.
4. Evaluate calculation and mitigation of damages.
5. Consider recent case law on penalties and unconscionability.
6. Synthesize to determine enforceability and risk allocation.
""",
        key_factors=[
            "Lease clause terms",
            "Reasonableness of damages",
            "State law",
            "Mitigation requirements",
            "Recent case law"
        ],
        primary_authority=[
            "Lease agreement",
            "State contract law",
            "Restatement (Second) of Contracts"
        ],
        burden_holder="Landlord (to prove reasonableness), Tenant (to challenge as penalty)",
        adversary_position="Tenant may challenge as penalty or seek mitigation.",
        counter_arguments=[
            "Unreasonable damages",
            "Failure to mitigate",
            "Statutory overrides"
        ],
        resolution_strategy="Negotiate reasonable damages; comply with mitigation requirements.",
        entity_scope="Commercial landlords and tenants",
        confidence=0.89,
        confidence_zone="Medium-High",
        controlling_precedent="Truck Rent-A-Center, Inc. v. Puritan Farms 2nd, Inc., 41 N.Y.2d 420 (1977)"
    ),
    DoctrineBlock(
        topic="Americans with Disabilities Act (ADA) Compliance in CRE",
        keywords=["ADA", "compliance", "accessibility", "commercial property", "public accommodation"],
        conclusion_template="Commercial properties open to the public must comply with ADA accessibility standards, with liability for both landlords and tenants.",
        reasoning_framework="""
1. Determine if property is a place of public accommodation.
2. Review lease for allocation of ADA compliance responsibilities.
3. Analyze existing conditions for compliance with ADAAG standards.
4. Assess remedies for non-compliance, including injunctive relief and damages.
5. Consider recent case law and DOJ enforcement actions.
6. Synthesize to determine compliance obligations and risk allocation.
""",
        key_factors=[
            "Property use",
            "Lease allocation of responsibility",
            "ADAAG compliance",
            "Remedies for non-compliance",
            "Recent case law"
        ],
        primary_authority=[
            "42 U.S.C. §§12181-12189",
            "ADA Accessibility Guidelines (ADAAG)",
            "DOJ regulations"
        ],
        burden_holder="Landlord/tenant (per lease and law)",
        adversary_position="Counterparty may dispute allocation; DOJ or private plaintiff may sue.",
        counter_arguments=[
            "Impracticability",
            "Grandfathered conditions",
            "Lease overrides"
        ],
        resolution_strategy="Conduct accessibility audit; negotiate clear lease allocation.",
        entity_scope="Landlords, tenants, property managers",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Roberts v. Royal Atlantic Corp., 542 F.3d 363 (2d Cir. 2008)"
    ),
    DoctrineBlock(
        topic="Insurance Requirements in Commercial Leases",
        keywords=["insurance", "commercial lease", "coverage", "liability", "property damage"],
        conclusion_template="Commercial leases require tenants and/or landlords to maintain specified insurance coverage, with certificates and endorsements as evidence.",
        reasoning_framework="""
1. Review lease for insurance requirements (types, limits, endorsements).
2. Analyze allocation of responsibility for premiums and deductibles.
3. Assess compliance with lender and insurer requirements.
4. Evaluate remedies for failure to maintain coverage.
5. Consider impact on risk allocation and claims handling.
6. Synthesize to determine enforceability and compliance.
""",
        key_factors=[
            "Lease insurance terms",
            "Coverage types and limits",
            "Endorsements required",
            "Responsibility for premiums",
            "Remedies for breach"
        ],
        primary_authority=[
            "Lease agreement",
            "Insurance policy",
            "State insurance statutes"
        ],
        burden_holder="Tenant/landlord (per lease)",
        adversary_position="Counterparty may dispute adequacy or compliance.",
        counter_arguments=[
            "Insufficient coverage",
            "Failure to provide certificates",
            "Ambiguous lease terms"
        ],
        resolution_strategy="Negotiate clear insurance requirements; obtain certificates and endorsements.",
        entity_scope="Landlords, tenants, insurers",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="First American Title Ins. Co. v. J.P. Morgan Chase & Co., 402 F.3d 337 (2d Cir. 2005)"
    ),
    DoctrineBlock(
        topic="Assignment of Rents as Collateral",
        keywords=["assignment of rents", "collateral", "loan", "lender", "foreclosure"],
        conclusion_template="Assignment of rents clauses grant lenders the right to collect rents upon borrower default, subject to statutory and judicial requirements.",
        reasoning_framework="""
1. Review loan documents for assignment of rents provisions.
2. Analyze statutory requirements for perfection and enforcement.
3. Assess timing and procedures for lender to collect rents.
4. Evaluate impact on borrower and tenant rights.
5. Consider remedies for improper collection or application of rents.
6. Synthesize to determine enforceability and risk allocation.
""",
        key_factors=[
            "Assignment clause terms",
            "Statutory requirements",
            "Enforcement procedures",
            "Borrower/tenant rights",
            "Remedies for breach"
        ],
        primary_authority=[
            "Loan agreement",
            "State assignment of rents statutes",
            "Restatement (Third) of Property: Mortgages"
        ],
        burden_holder="Lender (to perfect and enforce), Borrower (to contest)",
        adversary_position="Borrower may challenge enforcement; tenants may dispute payment.",
        counter_arguments=[
            "Improper perfection",
            "Statutory overrides",
            "Tenant defenses"
        ],
        resolution_strategy="Comply with statutory and loan requirements; provide notice to tenants.",
        entity_scope="Lenders, borrowers, tenants",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="In re Jason Realty, L.P., 59 F.3d 423 (3d Cir. 1995)"
    ),
    DoctrineBlock(
        topic="Escrow Agreements in CRE Transactions",
        keywords=["escrow", "agreement", "commercial real estate", "closing", "disbursement"],
        conclusion_template="Escrow agreements govern the holding and disbursement of funds or documents in CRE transactions, protecting parties' interests.",
        reasoning_framework="""
1. Review escrow agreement for terms and conditions of release.
2. Analyze parties' rights and obligations.
3. Assess remedies for breach or dispute.
4. Evaluate statutory requirements for escrow agents.
5. Consider impact on closing and transaction risk.
6. Synthesize to determine enforceability and compliance.
""",
        key_factors=[
            "Escrow agreement terms",
            "Release conditions",
            "Parties' rights",
            "Statutory requirements",
            "Remedies for breach"
        ],
        primary_authority=[
            "Escrow agreement",
            "State escrow statutes",
            "Restatement (Third) of Agency"
        ],
        burden_holder="Escrow agent (to comply), Parties (to fulfill conditions)",
        adversary_position="Party may dispute release or allege breach.",
        counter_arguments=[
            "Improper release",
            "Ambiguous terms",
            "Statutory overrides"
        ],
        resolution_strategy="Negotiate clear escrow terms; legal review for compliance.",
        entity_scope="Buyers, sellers, lenders, escrow agents",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="In re First Alliance Mortgage Co., 471 F.3d 977 (9th Cir. 2006)"
    ),
    DoctrineBlock(
        topic="1031 Exchange Reverse and Improvement Structures",
        keywords=["1031 exchange", "reverse exchange", "improvement exchange", "qualified intermediary", "parking arrangement"],
        conclusion_template="Reverse and improvement 1031 exchanges allow taxpayers to acquire replacement property before selling relinquished property or to make improvements during the exchange period.",
        reasoning_framework="""
1. Review IRS guidelines for reverse and improvement exchanges.
2. Analyze use of Exchange Accommodation Titleholder (EAT) and parking arrangements.
3. Assess timing and identification requirements.
4. Evaluate documentation and compliance with safe harbor rules.
5. Consider impact on financing and title insurance.
6. Synthesize to determine eligibility and risk of IRS challenge.
""",
        key_factors=[
            "IRS safe harbor rules",
            "EAT/parking arrangements",
            "Timing and identification",
            "Documentation",
            "Financing/title issues"
        ],
        primary_authority=[
            "Rev. Proc. 2000-37",
            "IRC §1031",
            "Treas. Reg. §1.1031"
        ],
        burden_holder="Taxpayer",
        adversary_position="IRS may challenge non-compliant exchanges.",
        counter_arguments=[
            "Improper use of EAT",
            "Failure to meet timing",
            "Non-qualifying improvements"
        ],
        resolution_strategy="Strict compliance with IRS procedures; engage experienced intermediary.",
        entity_scope="Real estate investors, intermediaries",
        confidence=0.88,
        confidence_zone="Medium-High",
        controlling_precedent="Rev. Proc. 2000-37"
    ),
    DoctrineBlock(
        topic="Foreign Investment in Real Property Tax Act (FIRPTA) Withholding",
        keywords=["FIRPTA", "withholding", "foreign seller", "real property", "IRS"],
        conclusion_template="FIRPTA requires buyers to withhold and remit a percentage of the sale price when acquiring U.S.