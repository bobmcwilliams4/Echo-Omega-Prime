from dataclasses import dataclass, field
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
        topic="BSA Currency Transaction Reporting",
        keywords=["BSA", "Currency Transaction Report", "CTR", "FinCEN", "Bank Secrecy Act", "AML"],
        conclusion_template="A financial institution must file a Currency Transaction Report (CTR) for each transaction in currency of more than $10,000 by, through, or to the institution.",
        reasoning_framework="""
        1. Determine whether the transaction involves currency (coin and paper money).
        2. Assess if the aggregate amount exceeds $10,000 in a single business day.
        3. Evaluate whether the transactions are by or on behalf of the same person.
        4. Confirm the institution's obligation to file a CTR under 31 CFR 1010.311.
        5. Consider exemptions under 31 CFR 1020.315.
        6. Review internal controls and monitoring systems for aggregation.
        7. Ensure timely filing with FinCEN within 15 days.
        8. Document rationale for any decision not to file.
        9. Train staff to identify reportable transactions.
        10. Monitor for structuring attempts to evade reporting.
        """,
        key_factors=[
            "Transaction amount exceeds $10,000",
            "Currency involved (not checks or wires)",
            "Aggregation of multiple transactions",
            "Customer identity and relationship",
            "Exemptions and exception handling",
            "Timeliness of filing",
            "Internal controls and monitoring"
        ],
        primary_authority=[
            "31 U.S.C. § 5313",
            "31 CFR 1010.311",
            "FinCEN Guidance"
        ],
        burden_holder="Financial institution",
        adversary_position="The transaction is not subject to CTR requirements due to exemption or non-currency nature.",
        counter_arguments=[
            "Exemption does not apply to this customer or transaction type.",
            "Aggregation rules require reporting.",
            "Currency is defined broadly under BSA."
        ],
        resolution_strategy="Apply BSA and FinCEN rules, review transaction details, and consult legal/compliance if ambiguous.",
        entity_scope="All U.S. banks and financial institutions",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Bajakajian, 524 U.S. 321 (1998)"
    ),
    DoctrineBlock(
        topic="SAR Suspicious Activity Reporting",
        keywords=["SAR", "Suspicious Activity Report", "AML", "BSA", "FinCEN", "Reporting Obligation"],
        conclusion_template="A financial institution is required to file a SAR when it detects known or suspected violations of law or suspicious activity involving $5,000 or more.",
        reasoning_framework="""
        1. Identify transactions that are unusual or inconsistent with known customer patterns.
        2. Assess whether the activity involves potential money laundering, terrorist financing, or other criminal acts.
        3. Determine if the aggregate amount involved meets or exceeds $5,000.
        4. Evaluate the presence of red flags as outlined in FinCEN advisories.
        5. Consider the institution's internal SAR escalation procedures.
        6. Ensure confidentiality of SAR filings.
        7. File the SAR within 30 calendar days of initial detection.
        8. Document the basis for the SAR decision.
        9. Review for possible law enforcement notification.
        10. Maintain SAR records for five years.
        """,
        key_factors=[
            "Suspicious or unusual activity",
            "Aggregate transaction amount",
            "Pattern of behavior",
            "Internal escalation and review",
            "Timeliness and confidentiality"
        ],
        primary_authority=[
            "31 U.S.C. § 5318(g)",
            "31 CFR 1020.320",
            "FinCEN SAR Guidance"
        ],
        burden_holder="Financial institution",
        adversary_position="The activity is not sufficiently suspicious or does not meet the reporting threshold.",
        counter_arguments=[
            "Pattern of activity justifies suspicion.",
            "Threshold is met through aggregation.",
            "FinCEN guidance encourages reporting in cases of uncertainty."
        ],
        resolution_strategy="Apply FinCEN SAR rules, review internal policies, and err on the side of filing if doubt exists.",
        entity_scope="All U.S. banks and financial institutions",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. MacPherson, 424 F.3d 183 (2d Cir. 2005)"
    ),
    DoctrineBlock(
        topic="CDD Customer Due Diligence Rule",
        keywords=["CDD", "Customer Due Diligence", "Beneficial Ownership", "AML", "BSA", "FinCEN"],
        conclusion_template="Covered financial institutions must identify and verify the identity of beneficial owners of legal entity customers as part of CDD obligations.",
        reasoning_framework="""
        1. Determine whether the customer is a legal entity subject to CDD requirements.
        2. Obtain identifying information for each beneficial owner (25% or more ownership or control).
        3. Verify the identity of each beneficial owner using reliable documentation.
        4. Assess the nature and purpose of the customer relationship.
        5. Conduct ongoing monitoring for suspicious activity.
        6. Update customer information as necessary.
        7. Retain records of beneficial ownership and verification.
        8. Train staff on CDD requirements and red flags.
        9. Review for exemptions (e.g., certain government entities).
        10. Integrate CDD into the institution's overall AML program.
        """,
        key_factors=[
            "Legal entity customer status",
            "Beneficial ownership structure",
            "Verification of identity",
            "Ongoing monitoring",
            "Recordkeeping"
        ],
        primary_authority=[
            "31 CFR 1010.230",
            "FinCEN CDD Rule (2016)",
            "FFIEC BSA/AML Manual"
        ],
        burden_holder="Financial institution",
        adversary_position="The customer is exempt or beneficial ownership cannot be determined.",
        counter_arguments=[
            "CDD exemptions are limited and narrowly construed.",
            "Reasonable efforts must be documented.",
            "FinCEN expects robust procedures."
        ],
        resolution_strategy="Apply CDD rule, document efforts, and escalate unresolved cases to compliance.",
        entity_scope="Covered financial institutions (banks, brokers, mutual funds, etc.)",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FinCEN CDD Rule (81 FR 29398, May 11, 2016)"
    ),
    DoctrineBlock(
        topic="Regulation Z TILA APR Disclosure",
        keywords=["Regulation Z", "TILA", "Truth in Lending", "APR", "Disclosure", "Consumer Credit"],
        conclusion_template="Creditors must clearly and conspicuously disclose the annual percentage rate (APR) and other key terms to consumers before consummation of a credit transaction.",
        reasoning_framework="""
        1. Identify whether the transaction is covered by Regulation Z (consumer credit).
        2. Determine the finance charge and calculate the APR using the prescribed formula.
        3. Prepare disclosures in a clear and conspicuous manner.
        4. Provide required disclosures before consummation of the loan.
        5. Ensure accuracy of disclosed terms (APR, finance charge, payment schedule).
        6. Retain evidence of disclosures for regulatory review.
        7. Review for exceptions (e.g., business credit).
        8. Monitor for changes in terms requiring redisclosure.
        9. Train staff on disclosure requirements.
        10. Address consumer inquiries and disputes regarding disclosures.
        """,
        key_factors=[
            "Consumer credit transaction",
            "Calculation of APR",
            "Timing and clarity of disclosure",
            "Accuracy of terms",
            "Record retention"
        ],
        primary_authority=[
            "15 U.S.C. § 1638",
            "12 CFR 1026 (Regulation Z)",
            "CFPB Official Interpretations"
        ],
        burden_holder="Creditor",
        adversary_position="The transaction is not covered or disclosures were adequate.",
        counter_arguments=[
            "Coverage is broad for consumer credit.",
            "Disclosures must be clear and accurate.",
            "Errors may trigger liability."
        ],
        resolution_strategy="Apply Regulation Z, review disclosure forms, and correct errors promptly.",
        entity_scope="All creditors offering consumer credit",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ford Motor Credit Co. v. Milhollin, 444 U.S. 555 (1980)"
    ),
    DoctrineBlock(
        topic="RESPA Section 8 Kickback Prohibition",
        keywords=["RESPA", "Section 8", "Kickbacks", "Referral Fees", "Real Estate Settlement", "Prohibition"],
        conclusion_template="No person may give or accept any fee, kickback, or thing of value for the referral of settlement service business in connection with a federally related mortgage loan.",
        reasoning_framework="""
        1. Determine whether the transaction involves a federally related mortgage loan.
        2. Assess whether any thing of value was given or received for a referral.
        3. Evaluate the relationship between the parties (e.g., affiliated business arrangements).
        4. Review for exceptions (e.g., reasonable payments for services actually performed).
        5. Analyze documentation of services rendered.
        6. Consider HUD and CFPB enforcement guidance.
        7. Examine compensation structures for compliance.
        8. Document findings and rationale for compliance.
        9. Train staff on prohibited practices.
        10. Monitor for indirect kickbacks or disguised payments.
        """,
        key_factors=[
            "Federally related mortgage loan",
            "Referral of settlement service",
            "Thing of value exchanged",
            "Exceptions and safe harbors",
            "Documentation of services"
        ],
        primary_authority=[
            "12 U.S.C. § 2607",
            "12 CFR 1024.14 (Regulation X)",
            "CFPB RESPA Guidance"
        ],
        burden_holder="Person or entity providing or receiving value",
        adversary_position="Payment was for bona fide services, not a referral.",
        counter_arguments=[
            "Services must be actual, necessary, and distinct.",
            "Documentation must support the payment.",
            "Affiliated business disclosures required."
        ],
        resolution_strategy="Apply RESPA Section 8, review payment arrangements, and consult compliance/legal.",
        entity_scope="Settlement service providers, lenders, brokers",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Freeman v. Quicken Loans, Inc., 566 U.S. 624 (2012)"
    ),
    DoctrineBlock(
        topic="ECOA Regulation B Fair Lending",
        keywords=["ECOA", "Regulation B", "Fair Lending", "Discrimination", "Credit", "Protected Class"],
        conclusion_template="A creditor may not discriminate against an applicant in any aspect of a credit transaction on the basis of race, color, religion, national origin, sex, marital status, age, or receipt of public assistance.",
        reasoning_framework="""
        1. Identify whether the applicant is a member of a protected class.
        2. Assess the credit decision-making process for disparate treatment or impact.
        3. Review application forms and underwriting criteria for facially neutral policies.
        4. Examine adverse action notices for compliance.
        5. Analyze statistical data for patterns of discrimination.
        6. Consider legitimate business justifications for credit decisions.
        7. Document all credit decisions and rationale.
        8. Train staff on fair lending requirements.
        9. Monitor for complaints and regulatory inquiries.
        10. Implement corrective action when violations are identified.
        """,
        key_factors=[
            "Protected class status",
            "Credit decision process",
            "Adverse action notices",
            "Statistical evidence",
            "Business justification"
        ],
        primary_authority=[
            "15 U.S.C. § 1691",
            "12 CFR 1002 (Regulation B)",
            "CFPB ECOA Guidance"
        ],
        burden_holder="Creditor",
        adversary_position="Credit decision was based on legitimate, non-discriminatory factors.",
        counter_arguments=[
            "Disparate impact may still constitute discrimination.",
            "Documentation must support business necessity.",
            "Regulators may require corrective action."
        ],
        resolution_strategy="Apply ECOA and Regulation B, review policies, and conduct fair lending audits.",
        entity_scope="All creditors",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Texas Dept. of Housing v. Inclusive Communities Project, 576 U.S. 519 (2015)"
    ),
    DoctrineBlock(
        topic="CRA Community Reinvestment Act",
        keywords=["CRA", "Community Reinvestment", "Lending", "Assessment Area", "Low-Moderate Income", "Regulatory Rating"],
        conclusion_template="Banks are required to help meet the credit needs of the communities in which they operate, including low- and moderate-income neighborhoods, consistent with safe and sound operations.",
        reasoning_framework="""
        1. Define the bank's assessment area(s).
        2. Evaluate lending, investment, and service activities in those areas.
        3. Assess performance context (demographics, competition, economic conditions).
        4. Review public file and CRA-related complaints.
        5. Analyze lending patterns for low- and moderate-income borrowers.
        6. Consider innovative or flexible lending practices.
        7. Document community outreach and partnerships.
        8. Prepare for periodic CRA examinations.
        9. Address examiner feedback and recommendations.
        10. Monitor for changes in regulatory standards.
        """,
        key_factors=[
            "Assessment area definition",
            "Lending/investment/service activities",
            "Performance context",
            "Community outreach",
            "Regulatory examination results"
        ],
        primary_authority=[
            "12 U.S.C. §§ 2901-2908",
            "12 CFR 25, 228, 345 (OCC, FRB, FDIC CRA Rules)",
            "Interagency CRA Q&A"
        ],
        burden_holder="Bank",
        adversary_position="Bank's activities are insufficient or not targeted to low- and moderate-income communities.",
        counter_arguments=[
            "Performance context justifies current activity levels.",
            "Innovative products are being offered.",
            "Community needs are being met through alternative means."
        ],
        resolution_strategy="Apply CRA regulations, document efforts, and engage with community stakeholders.",
        entity_scope="Insured depository institutions",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OCC, FRB, FDIC Interagency Interpretations"
    ),
    DoctrineBlock(
        topic="Basel III Capital Requirements",
        keywords=["Basel III", "Capital", "Risk-Weighted Assets", "Tier 1", "CET1", "Leverage Ratio"],
        conclusion_template="Banks must maintain minimum capital ratios, including Common Equity Tier 1 (CET1), Tier 1, and Total Capital, relative to risk-weighted assets, as required by Basel III and U.S. implementation rules.",
        reasoning_framework="""
        1. Calculate risk-weighted assets (RWA) in accordance with regulatory standards.
        2. Determine the amount of CET1, Tier 1, and Total Capital.
        3. Compute capital ratios: CET1/RWA, Tier 1/RWA, Total Capital/RWA.
        4. Compare ratios to minimum requirements (e.g., CET1 ≥ 4.5%, Tier 1 ≥ 6%, Total ≥ 8%).
        5. Assess capital conservation buffer and countercyclical buffer applicability.
        6. Review leverage ratio requirements.
        7. Monitor for prompt corrective action triggers.
        8. Document capital planning and stress testing results.
        9. Report capital ratios to regulators as required.
        10. Prepare for regulatory capital adequacy reviews.
        """,
        key_factors=[
            "Risk-weighted asset calculation",
            "Capital components and quality",
            "Minimum ratio thresholds",
            "Buffer requirements",
            "Regulatory reporting"
        ],
        primary_authority=[
            "12 CFR 3 (OCC), 12 CFR 217 (FRB), 12 CFR 324 (FDIC)",
            "Basel III Accord",
            "Dodd-Frank Act"
        ],
        burden_holder="Bank",
        adversary_position="Bank's capital ratios are sufficient or buffers are not required.",
        counter_arguments=[
            "Capital conservation buffer is mandatory.",
            "Stress testing may reveal additional needs.",
            "Supervisory expectations may exceed minimums."
        ],
        resolution_strategy="Apply Basel III and U.S. capital rules, review capital planning, and consult with regulators.",
        entity_scope="Large and internationally active banks",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Basel Committee on Banking Supervision, Basel III Final Rule"
    ),
    DoctrineBlock(
        topic="DFAST Dodd-Frank Stress Testing",
        keywords=["DFAST", "Dodd-Frank", "Stress Test", "CCAR", "Capital Planning", "Scenario Analysis"],
        conclusion_template="Covered institutions must conduct annual Dodd-Frank Act Stress Tests (DFAST) to assess capital adequacy under adverse economic scenarios.",
        reasoning_framework="""
        1. Determine whether the institution meets DFAST coverage thresholds (asset size, type).
        2. Develop baseline, adverse, and severely adverse scenarios.
        3. Project capital, losses, revenues, and balance sheet under each scenario.
        4. Assess capital adequacy and ability to absorb losses.
        5. Document methodologies, assumptions, and results.
        6. Submit stress test results to regulators by required deadlines.
        7. Disclose summary results to the public.
        8. Integrate stress testing into capital planning and risk management.
        9. Review for changes in regulatory requirements.
        10. Prepare for supervisory review and follow-up.
        """,
        key_factors=[
            "Institution asset size and type",
            "Scenario design and rigor",
            "Capital projections",
            "Regulatory submission and disclosure",
            "Integration with risk management"
        ],
        primary_authority=[
            "12 U.S.C. § 5365",
            "12 CFR 252 (Regulation YY)",
            "Federal Reserve DFAST Guidance"
        ],
        burden_holder="Covered institution",
        adversary_position="Institution is not subject to DFAST or scenarios are insufficient.",
        counter_arguments=[
            "Thresholds may change; voluntary stress testing is encouraged.",
            "Supervisors may require additional scenarios.",
            "Public disclosure is required for covered institutions."
        ],
        resolution_strategy="Apply DFAST rules, document process, and consult with risk and compliance teams.",
        entity_scope="Large bank holding companies, certain savings and loan holding companies",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Federal Reserve DFAST Final Rule"
    ),
    DoctrineBlock(
        topic="Volcker Rule Proprietary Trading",
        keywords=["Volcker Rule", "Proprietary Trading", "Covered Fund", "Bank Holding Company", "Dodd-Frank"],
        conclusion_template="Banking entities are prohibited from engaging in proprietary trading and from acquiring or retaining ownership interests in, or sponsoring, covered funds, subject to certain exemptions.",
        reasoning_framework="""
        1. Determine whether the entity is a 'banking entity' under the Volcker Rule.
        2. Assess whether the activity constitutes proprietary trading or covered fund involvement.
        3. Review for permitted activities and exemptions (e.g., market making, underwriting).
        4. Evaluate risk management and compliance controls.
        5. Document trading activity and compliance with exemption criteria.
        6. Monitor for indirect or disguised proprietary trading.
        7. Train staff on Volcker Rule restrictions.
        8. Report significant trading metrics to regulators.
        9. Prepare for regulatory examinations and enforcement.
        10. Update policies and procedures for rule changes.
        """,
        key_factors=[
            "Banking entity status",
            "Nature of trading activity",
            "Exemptions and permitted activities",
            "Compliance controls",
            "Documentation and reporting"
        ],
        primary_authority=[
            "12 U.S.C. § 1851",
            "12 CFR Part 248 (Regulation VV)",
            "OCC, FRB, FDIC, SEC, CFTC Joint Rule"
        ],
        burden_holder="Banking entity",
        adversary_position="Activity falls within an exemption or is not proprietary trading.",
        counter_arguments=[
            "Exemptions are narrowly construed.",
            "Burden of proof is on the entity.",
            "Regulators may challenge exemption claims."
        ],
        resolution_strategy="Apply Volcker Rule, review trading activity, and consult with legal/compliance.",
        entity_scope="Bank holding companies, insured depository institutions, affiliates",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Volcker Rule Final Rule (79 FR 5536, Jan. 31, 2014)"
    ),
    DoctrineBlock(
        topic="Regulation E Electronic Fund Transfers",
        keywords=["Regulation E", "EFTA", "Electronic Fund Transfer", "Consumer Protection", "Error Resolution"],
        conclusion_template="Financial institutions must provide disclosures, error resolution procedures, and consumer protections for electronic fund transfers under Regulation E.",
        reasoning_framework="""
        1. Identify whether the transaction is an electronic fund transfer (EFT) covered by Regulation E.
        2. Provide required initial disclosures to consumers.
        3. Implement procedures for error resolution and unauthorized transfers.
        4. Limit consumer liability for unauthorized EFTs.
        5. Investigate and resolve errors within prescribed timeframes.
        6. Document communications and findings.
        7. Train staff on Regulation E requirements.
        8. Monitor for compliance with periodic statement requirements.
        9. Address consumer complaints promptly.
        10. Retain records of disclosures and investigations.
        """,
        key_factors=[
            "EFT coverage",
            "Disclosure content and timing",
            "Error resolution procedures",
            "Consumer liability limits",
            "Recordkeeping"
        ],
        primary_authority=[
            "15 U.S.C. § 1693 et seq.",
            "12 CFR 1005 (Regulation E)",
            "CFPB Regulation E Guidance"
        ],
        burden_holder="Financial institution",
        adversary_position="Transaction is not covered or procedures were followed.",
        counter_arguments=[
            "Coverage is broad for consumer EFTs.",
            "Strict timeframes for error resolution.",
            "Consumer liability is limited by law."
        ],
        resolution_strategy="Apply Regulation E, review disclosures, and investigate errors promptly.",
        entity_scope="All financial institutions offering EFT services",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation E Official Interpretations"
    ),
    DoctrineBlock(
        topic="GLBA Privacy and Safeguards",
        keywords=["GLBA", "Gramm-Leach-Bliley Act", "Privacy", "Safeguards Rule", "Consumer Information"],
        conclusion_template="Financial institutions must provide privacy notices, allow consumers to opt out of certain information sharing, and implement safeguards to protect customer information.",
        reasoning_framework="""
        1. Identify whether the entity is a financial institution under GLBA.
        2. Provide initial and annual privacy notices to consumers.
        3. Disclose information sharing practices and opt-out rights.
        4. Implement a written information security program.
        5. Assess risks to customer information and address them.
        6. Train staff on privacy and security requirements.
        7. Monitor for unauthorized access or disclosure.
        8. Review service provider contracts for compliance.
        9. Update policies as necessary for regulatory changes.
        10. Retain records of notices and consumer opt-outs.
        """,
        key_factors=[
            "Financial institution status",
            "Privacy notice content and delivery",
            "Opt-out mechanisms",
            "Safeguards program implementation",
            "Vendor management"
        ],
        primary_authority=[
            "15 U.S.C. §§ 6801-6809",
            "16 CFR Part 314 (FTC Safeguards Rule)",
            "GLBA Privacy Rule"
        ],
        burden_holder="Financial institution",
        adversary_position="Information sharing is permitted or safeguards are adequate.",
        counter_arguments=[
            "Consumers must be given clear opt-out rights.",
            "Safeguards must address all material risks.",
            "Regulators may require enhanced controls."
        ],
        resolution_strategy="Apply GLBA rules, review privacy and security programs, and address deficiencies.",
        entity_scope="All financial institutions (broadly defined)",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FTC v. Wyndham Worldwide Corp., 799 F.3d 236 (3d Cir. 2015)"
    ),
    DoctrineBlock(
        topic="Bank Secrecy Act Recordkeeping",
        keywords=["BSA", "Recordkeeping", "AML", "Transaction Records", "FinCEN"],
        conclusion_template="Financial institutions must retain records of certain transactions, including wire transfers and monetary instruments, as required by the Bank Secrecy Act.",
        reasoning_framework="""
        1. Identify transactions subject to BSA recordkeeping (e.g., wire transfers, monetary instruments).
        2. Retain required information (e.g., names, addresses, account numbers, transaction amounts).
        3. Maintain records for at least five years.
        4. Ensure records are accessible for regulatory review.
        5. Document internal procedures for record retention.
        6. Train staff on recordkeeping requirements.
        7. Monitor for completeness and accuracy of records.
        8. Review for exceptions or exemptions.
        9. Address deficiencies promptly.
        10. Prepare for regulatory examinations.
        """,
        key_factors=[
            "Transaction type and threshold",
            "Required information content",
            "Retention period",
            "Accessibility of records",
            "Internal controls"
        ],
        primary_authority=[
            "31 U.S.C. § 5311 et seq.",
            "31 CFR 1010.410, 1010.420",
            "FinCEN BSA Guidance"
        ],
        burden_holder="Financial institution",
        adversary_position="Records are not required or have been retained adequately.",
        counter_arguments=[
            "BSA requirements are strict and broadly applicable.",
            "Regulators expect robust recordkeeping.",
            "Deficiencies may trigger enforcement."
        ],
        resolution_strategy="Apply BSA recordkeeping rules, review internal procedures, and address gaps.",
        entity_scope="All financial institutions",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FinCEN Enforcement Actions"
    ),
    DoctrineBlock(
        topic="OFAC Sanctions Compliance",
        keywords=["OFAC", "Sanctions", "SDN List", "Blocked Transactions", "Compliance Program"],
        conclusion_template="Financial institutions must block or reject transactions involving sanctioned parties and report such actions to OFAC.",
        reasoning_framework="""
        1. Screen customers and transactions against OFAC lists (e.g., SDN, sectoral sanctions).
        2. Block or reject transactions as required.
        3. Report blocked or rejected transactions to OFAC within 10 business days.
        4. Retain records of blocked assets and related communications.
        5. Implement a risk-based OFAC compliance program.
        6. Train staff on sanctions screening and escalation.
        7. Monitor for changes in OFAC lists and regulations.
        8. Review for indirect or hidden ownership by sanctioned parties.
        9. Address false positives and escalate as needed.
        10. Prepare for OFAC audits and enforcement actions.
        """,
        key_factors=[
            "Screening effectiveness",
            "Timeliness of blocking/reporting",
            "Record retention",
            "Compliance program adequacy",
            "Training and escalation"
        ],
        primary_authority=[
            "50 U.S.C. §§ 1701-1706",
            "31 CFR Parts 500-599",
            "OFAC Guidance"
        ],
        burden_holder="Financial institution",
        adversary_position="Transaction is not subject to sanctions or screening was adequate.",
        counter_arguments=[
            "OFAC liability is strict; intent is not required.",
            "Indirect ownership triggers blocking.",
            "Regulators expect robust controls."
        ],
        resolution_strategy="Apply OFAC rules, review screening procedures, and escalate uncertain cases.",
        entity_scope="All U.S. financial institutions and foreign branches",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OFAC Enforcement Guidelines"
    ),
    DoctrineBlock(
        topic="LCR Liquidity Coverage Ratio",
        keywords=["LCR", "Liquidity Coverage Ratio", "Basel III", "High-Quality Liquid Assets", "Short-Term Outflows"],
        conclusion_template="Large banking organizations must maintain an adequate stock of high-quality liquid assets to cover total net cash outflows over a 30-day stress period.",
        reasoning_framework="""
        1. Determine whether the institution is subject to LCR requirements (size, complexity).
        2. Calculate total net cash outflows over a 30-day period.
        3. Identify and value high-quality liquid assets (HQLA).
        4. Compute the LCR: HQLA divided by net cash outflows.
        5. Ensure the LCR is at least 100%.
        6. Document methodologies and assumptions.
        7. Monitor for changes in liquidity risk profile.
        8. Report LCR to regulators as required.
        9. Integrate LCR into liquidity risk management framework.
        10. Prepare for regulatory review and stress testing.
        """,
        key_factors=[
            "Institution size and complexity",
            "Calculation of HQLA",
            "Net cash outflows estimation",
            "LCR threshold",
            "Regulatory reporting"
        ],
        primary_authority=[
            "12 CFR 50 (OCC), 12 CFR 249 (FRB), 12 CFR 329 (FDIC)",
            "Basel III LCR Standard"
        ],
        burden_holder="Covered banking organization",
        adversary_position="LCR is met or not applicable to the institution.",
        counter_arguments=[
            "Thresholds may change with regulatory updates.",
            "Supervisors may require higher buffers.",
            "LCR is a minimum, not a target."
        ],
        resolution_strategy="Apply LCR rules, review liquidity management, and consult with regulators.",
        entity_scope="Large, internationally active banking organizations",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Basel Committee on Banking Supervision, LCR Standard"
    ),
    DoctrineBlock(
        topic="UDAAP Unfair Deceptive Abusive Acts",
        keywords=["UDAAP", "Unfair", "Deceptive", "Abusive", "CFPB", "Consumer Protection"],
        conclusion_template="It is unlawful for any covered person or service provider to engage in any unfair, deceptive, or abusive act or practice in connection with consumer financial products or services.",
        reasoning_framework="""
        1. Assess whether the act or practice is unfair, deceptive, or abusive under CFPB standards.
        2. Review consumer complaints and regulatory guidance.
        3. Analyze marketing, disclosures, and product terms.
        4. Evaluate the impact on consumers, including monetary harm.
        5. Consider intent and business justification.
        6. Document findings and rationale for compliance.
        7. Train staff on UDAAP risks and prevention.
        8. Monitor for emerging risks and regulatory developments.
        9. Address violations promptly and remediate harm.
        10. Prepare for CFPB examinations and enforcement.
        """,
        key_factors=[
            "Nature of act or practice",
            "Consumer harm",
            "Disclosure clarity",
            "Business justification",
            "Regulatory guidance"
        ],
        primary_authority=[
            "12 U.S.C. §§ 5531, 5536",
            "CFPB UDAAP Examination Manual"
        ],
        burden_holder="Covered person or service provider",
        adversary_position="Act or practice is not unfair, deceptive, or abusive.",
        counter_arguments=[
            "CFPB interprets UDAAP broadly.",
            "Lack of intent is not a defense.",
            "Remediation may be required."
        ],
        resolution_strategy="Apply UDAAP standards, review practices, and remediate as necessary.",
        entity_scope="All providers of consumer financial products/services",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFPB v. ITT Educational Services, Inc., 219 F. Supp. 3d 878 (S.D. Ind. 2015)"
    ),
    DoctrineBlock(
        topic="Interchange Fee Regulation Durbin Amendment",
        keywords=["Durbin Amendment", "Interchange Fee", "Regulation II", "Debit Card", "Fee Cap"],
        conclusion_template="Issuers with $10 billion or more in assets must ensure that debit card interchange fees are reasonable and proportional to the cost incurred.",
        reasoning_framework="""
        1. Determine whether the issuer meets the asset threshold for coverage.
        2. Assess the interchange fee structure for debit card transactions.
        3. Compare fees to the caps set by Regulation II.
        4. Document cost analysis and fee calculations.
        5. Review for network exclusivity and routing requirements.
        6. Disclose fee practices to merchants as required.
        7. Monitor for compliance with evolving standards.
        8. Address merchant complaints and inquiries.
        9. Prepare for regulatory review and enforcement.
        10. Update policies for changes in fee caps or requirements.
        """,
        key_factors=[
            "Issuer asset size",
            "Fee structure and calculation",
            "Network exclusivity",
            "Routing requirements",
            "Documentation and disclosure"
        ],
        primary_authority=[
            "12 U.S.C. § 920",
            "12 CFR 235 (Regulation II)",
            "Federal Reserve Durbin Amendment Guidance"
        ],
        burden_holder="Debit card issuer",
        adversary_position="Issuer is exempt or fees are reasonable and proportional.",
        counter_arguments=[
            "Asset threshold is strictly enforced.",
            "Fee caps are mandatory for covered issuers.",
            "Documentation must support fee structure."
        ],
        resolution_strategy="Apply Regulation II, review fee calculations, and consult with compliance.",
        entity_scope="Large debit card issuers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACS v. Board of Governors, 746 F.3d 474 (D.C. Cir. 2014)"
    ),
    DoctrineBlock(
        topic="HMDA Home Mortgage Disclosure Act",
        keywords=["HMDA", "Mortgage Disclosure", "Loan Application Register", "Regulation C", "Data Reporting"],
        conclusion_template="Covered institutions must collect, report, and publicly disclose data about mortgage applications, originations, and purchases under HMDA.",
        reasoning_framework="""
        1. Determine whether the institution is subject to HMDA coverage.
        2. Collect required data fields for each mortgage application and loan.
        3. Prepare and maintain the Loan Application Register (LAR).
        4. Submit annual HMDA data to the CFPB by March 1.
        5. Disclose HMDA data to the public as required.
        6. Review for accuracy and completeness of reported data.
        7. Train staff on HMDA data collection and reporting.
        8. Monitor for changes in data fields and requirements.
        9. Address data errors and resubmit as necessary.
        10. Prepare for regulatory examinations and public scrutiny.
        """,
        key_factors=[
            "Institution coverage",
            "Data field completeness",
            "Timeliness of reporting",
            "Public disclosure",
            "Data accuracy"
        ],
        primary_authority=[
            "12 U.S.C. §§ 2801-2810",
            "12 CFR 1003 (Regulation C)",
            "CFPB HMDA Guidance"
        ],
        burden_holder="Covered institution",
        adversary_position="Institution is not covered or data is accurate.",
        counter_arguments=[
            "Coverage is broad for mortgage lenders.",
            "Data errors may trigger enforcement.",
            "Public disclosure is mandatory."
        ],
        resolution_strategy="Apply HMDA and Regulation C, review data, and address deficiencies.",
        entity_scope="Mortgage lenders, depository institutions",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFPB HMDA Enforcement Actions"
    ),
    DoctrineBlock(
        topic="TILA-RESPA Integrated Disclosures TRID",
        keywords=["TRID", "TILA", "RESPA", "Integrated Disclosure", "Loan Estimate", "Closing Disclosure"],
        conclusion_template="Creditors must provide consumers with a Loan Estimate and Closing Disclosure for most closed-end consumer mortgage loans, integrating TILA and RESPA requirements.",
        reasoning_framework="""
        1. Determine whether the loan is subject to TRID coverage.
        2. Provide the Loan Estimate within three business days of application.
        3. Deliver the Closing Disclosure at least three business days before consummation.
        4. Ensure accuracy and consistency between disclosures.
        5. Document delivery and receipt of disclosures.
        6. Address changes in terms requiring revised disclosures.
        7. Train staff on TRID requirements and timing.
        8. Monitor for compliance with tolerance thresholds.
        9. Retain records of disclosures for regulatory review.
        10. Address consumer inquiries and disputes.
        """,
        key_factors=[
            "Loan coverage",
            "Disclosure timing",
            "Accuracy and consistency",
            "Tolerance thresholds",
            "Record retention"
        ],
        primary_authority=[
            "12 CFR 1026 (Regulation Z)",
            "12 CFR 1024 (Regulation X)",
            "CFPB TRID Rule"
        ],
        burden_holder="Creditor",
        adversary_position="Loan is not covered or disclosures were timely and accurate.",
        counter_arguments=[
            "TRID coverage is broad for consumer mortgages.",
            "Strict timing and accuracy requirements.",
            "Errors may trigger liability."
        ],
        resolution_strategy="Apply TRID rules, review disclosures, and correct errors promptly.",
        entity_scope="Mortgage creditors",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFPB TRID Enforcement Actions"
    ),
    DoctrineBlock(
        topic="Affiliate Marketing Opt-Out FCRA 624",
        keywords=["FCRA", "Affiliate Marketing", "Opt-Out", "Section 624", "Consumer Reporting"],
        conclusion_template="Financial institutions must provide consumers with notice and a reasonable opportunity to opt out before using certain information received from affiliates for marketing purposes.",
        reasoning_framework="""
        1. Identify whether information is shared between affiliates for marketing.
        2. Provide clear and conspicuous opt-out notice to consumers.
        3. Allow a reasonable period (at least 30 days) for consumers to opt out.
        4. Honor consumer opt-out requests.
        5. Document delivery and receipt of notices.
        6. Train staff on FCRA Section 624 requirements.
        7. Monitor for compliance with opt-out procedures.
        8. Address consumer complaints and inquiries.
        9. Retain records of notices and opt-out elections.
        10. Update policies for regulatory changes.
        """,
        key_factors=[
            "Affiliate information sharing",
            "Notice content and delivery",
            "Opt-out mechanism",
            "Recordkeeping",
            "Staff training"
        ],
        primary_authority=[
            "15 U.S.C. § 1681s-3",
            "12 CFR 1022.21 (Regulation V)",
            "FTC FCRA Guidance"
        ],
        burden_holder="Financial institution",
        adversary_position="Information is not used for marketing or opt-out was provided.",
        counter_arguments=[
            "Notice must be clear and timely.",
            "Opt-out must be honored.",
            "Documentation is required."
        ],
        resolution_strategy="Apply FCRA Section 624, review notices, and address deficiencies.",
        entity_scope="Financial institutions and affiliates",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FTC v. ChoicePoint, Inc., No. 1:06-CV-198 (N.D. Ga. 2006)"
    ),
    DoctrineBlock(
        topic="Expedited Funds Availability Act Regulation CC",
        keywords=["Regulation CC", "Expedited Funds Availability", "EFAA", "Check Holds", "Deposit"],
        conclusion_template="Depository institutions must make funds from deposits available within specified timeframes and provide disclosures regarding funds availability.",
        reasoning_framework="""
        1. Determine whether the deposit is subject to Regulation CC.
        2. Apply standard availability schedules (e.g., next-day, second business day).
        3. Disclose funds availability policies to customers.
        4. Provide notice of exceptions or holds.
        5. Monitor for compliance with timing requirements.
        6. Document holds and reasons for exception.
        7. Train staff on Regulation CC requirements.
        8. Address customer inquiries and complaints.
        9. Retain records of disclosures and holds.
        10. Prepare for regulatory review and audits.
        """,
        key_factors=[
            "Deposit type and amount",
            "Availability schedule",
            "Disclosure content and timing",
            "Exception holds",
            "Record retention"
        ],
        primary_authority=[
            "12 U.S.C. §§ 4001-4010",
            "12 CFR 229 (Regulation CC)",
            "Federal Reserve EFAA Guidance"
        ],
        burden_holder="Depository institution",
        adversary_position="Deposit is not covered or funds were made available timely.",
        counter_arguments=[
            "Coverage is broad for consumer deposits.",
            "Strict timing requirements.",
            "Documentation is required for exceptions."
        ],
        resolution_strategy="Apply Regulation CC, review policies, and address deficiencies.",
        entity_scope="Depository institutions",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation CC Official Interpretations"
    ),
    DoctrineBlock(
        topic="HMDA Loan Data Integrity and Accuracy",
        keywords=["HMDA", "Loan Data", "Integrity", "Accuracy", "Regulation C", "CFPB"],
        conclusion_template="Institutions must ensure the integrity and accuracy of HMDA data submitted to regulators and disclosed to the public.",
        reasoning_framework="""
        1. Review data collection procedures for completeness and accuracy.
        2. Conduct periodic audits of Loan Application Register (LAR) entries.
        3. Correct identified errors and resubmit data as necessary.
        4. Train staff on HMDA data requirements and error prevention.
        5. Monitor for changes in regulatory requirements.
        6. Document data validation and correction efforts.
        7. Address public and regulatory inquiries about data.
        8. Retain records of audits and corrections.
        9. Prepare for regulatory examinations and enforcement.
        10. Implement controls to prevent recurring errors.
        """,
        key_factors=[
            "Data collection procedures",
            "Audit and validation processes",
            "Error correction and resubmission",
            "Staff training",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 CFR 1003 (Regulation C)",
            "CFPB HMDA Guidance"
        ],
        burden_holder="Covered institution",
        adversary_position="Data is accurate or errors are immaterial.",
        counter_arguments=[
            "Material errors may trigger enforcement.",
            "Regulators expect robust controls.",
            "Public disclosure increases scrutiny."
        ],
        resolution_strategy="Apply Regulation C, review data, and address deficiencies.",
        entity_scope="Mortgage lenders, depository institutions",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFPB HMDA Data Integrity Enforcement"
    ),
    DoctrineBlock(
        topic="OCC Heightened Standards for Large Banks",
        keywords=["OCC", "Heightened Standards", "Large Banks", "Risk Governance", "Internal Controls"],
        conclusion_template="Large national banks and federal savings associations must establish and maintain a risk governance framework and meet OCC's heightened standards for risk management.",
        reasoning_framework="""
        1. Determine whether the bank meets OCC's definition of a large institution.
        2. Establish a board-approved risk governance framework.
        3. Implement three lines of defense: business units, independent risk management, internal audit.
        4. Ensure board and management oversight of risk appetite and limits.
        5. Document risk management policies and procedures.
        6. Monitor for emerging risks and regulatory changes.
        7. Train staff on risk governance responsibilities.
        8. Conduct periodic independent reviews of risk framework.
        9. Address deficiencies and implement corrective action.
        10. Prepare for OCC examinations and enforcement.
        """,
        key_factors=[
            "Institution size and complexity",
            "Risk governance framework",
            "Board and management oversight",
            "Internal controls",
            "Independent review"
        ],
        primary_authority=[
            "12 CFR 30, Appendix D",
            "OCC Heightened Standards Guidance"
        ],
        burden_holder="Large national bank or federal savings association",
        adversary_position="Bank is not covered or framework is adequate.",
        counter_arguments=[
            "OCC expects robust, documented frameworks.",
            "Deficiencies may trigger enforcement.",
            "Board oversight is critical."
        ],
        resolution_strategy="Apply OCC standards, review risk framework, and address gaps.",
        entity_scope="Large national banks and federal savings associations",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OCC Heightened Standards Rule (79 FR 54518, Sept. 11, 2014)"
    ),
    # Additional doctrine blocks to reach 40+ entries
    DoctrineBlock(
        topic="Regulation DD Truth in Savings Disclosure",
        keywords=["Regulation DD", "Truth in Savings", "Disclosure", "APY", "Deposit Accounts"],
        conclusion_template="Depository institutions must provide clear and uniform disclosures of terms, fees, and annual percentage yield (APY) for deposit accounts.",
        reasoning_framework="""
        1. Determine whether the account is covered by Regulation DD.
        2. Provide initial disclosures before account opening.
        3. Disclose APY, fees, and terms in a clear and uniform manner.
        4. Notify consumers of changes in terms as required.
        5. Retain evidence of disclosures for regulatory review.
        6. Monitor for compliance with advertising requirements.
        7. Train staff on disclosure obligations.
        8. Address consumer inquiries and disputes.
        9. Review for changes in regulatory requirements.
        10. Prepare for examinations and audits.
        """,
        key_factors=[
            "Account coverage",
            "Disclosure content and timing",
            "APY calculation",
            "Change in terms notification",
            "Advertising compliance"
        ],
        primary_authority=[
            "12 U.S.C. § 4301 et seq.",
            "12 CFR 1030 (Regulation DD)"
        ],
        burden_holder="Depository institution",
        adversary_position="Account is not covered or disclosures were adequate.",
        counter_arguments=[
            "Coverage is broad for consumer deposit accounts.",
            "APY must be calculated as prescribed.",
            "Errors may trigger enforcement."
        ],
        resolution_strategy="Apply Regulation DD, review disclosures, and correct deficiencies.",
        entity_scope="Depository institutions",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation DD Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation X Mortgage Servicing Standards",
        keywords=["Regulation X", "Mortgage Servicing", "RESPA", "Loss Mitigation", "Error Resolution"],
        conclusion_template="Mortgage servicers must comply with RESPA's servicing standards, including loss mitigation, error resolution, and force-placed insurance requirements.",
        reasoning_framework="""
        1. Identify whether the loan is subject to Regulation X servicing standards.
        2. Provide timely and accurate information to borrowers.
        3. Implement error resolution and information request procedures.
        4. Evaluate and respond to loss mitigation applications.
        5. Provide required notices for force-placed insurance.
        6. Retain records of communications and actions taken.
        7. Train staff on servicing requirements.
        8. Monitor for compliance with timelines and procedural requirements.
        9. Address borrower complaints and regulatory inquiries.
        10. Prepare for CFPB examinations and enforcement.
        """,
        key_factors=[
            "Loan coverage",
            "Loss mitigation process",
            "Error resolution procedures",
            "Force-placed insurance notices",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 CFR 1024 (Regulation X)",
            "RESPA Section 6"
        ],
        burden_holder="Mortgage servicer",
        adversary_position="Loan is not covered or procedures were followed.",
        counter_arguments=[
            "Coverage is broad for consumer mortgage loans.",
            "Strict procedural requirements.",
            "Documentation is required."
        ],
        resolution_strategy="Apply Regulation X, review servicing practices, and address deficiencies.",
        entity_scope="Mortgage servicers",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFPB Mortgage Servicing Rules"
    ),
    DoctrineBlock(
        topic="Regulation P Privacy of Consumer Financial Information",
        keywords=["Regulation P", "Privacy", "Consumer Financial Information", "GLBA", "Disclosure"],
        conclusion_template="Financial institutions must provide privacy notices and limit disclosure of nonpublic personal information as required by Regulation P.",
        reasoning_framework="""
        1. Identify whether the entity is a financial institution under Regulation P.
        2. Provide initial and annual privacy notices to consumers.
        3. Disclose information sharing practices and opt-out rights.
        4. Limit disclosure of nonpublic personal information as required.
        5. Train staff on privacy requirements.
        6. Monitor for unauthorized disclosures.
        7. Address consumer inquiries and opt-out requests.
        8. Retain records of notices and opt-outs.
        9. Update policies for regulatory changes.
        10. Prepare for examinations and enforcement.
        """,
        key_factors=[
            "Financial institution status",
            "Notice content and delivery",
            "Opt-out mechanism",
            "Disclosure limitations",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 CFR 1016 (Regulation P)",
            "GLBA Privacy Rule"
        ],
        burden_holder="Financial institution",
        adversary_position="Information sharing is permitted or notices were provided.",
        counter_arguments=[
            "Notices must be clear and timely.",
            "Opt-out must be honored.",
            "Documentation is required."
        ],
        resolution_strategy="Apply Regulation P, review notices, and address deficiencies.",
        entity_scope="All financial institutions",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation P Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation O Insider Lending Restrictions",
        keywords=["Regulation O", "Insider Lending", "Executive Officer", "Director", "Principal Shareholder"],
        conclusion_template="Member banks must comply with lending limits and approval requirements for loans to insiders under Regulation O.",
        reasoning_framework="""
        1. Identify insiders (executive officers, directors, principal shareholders).
        2. Determine aggregate lending limits for insiders.
        3. Obtain required approvals for loans to insiders.
        4. Ensure terms are no more favorable than those to non-insiders.
        5. Document all loans and approvals.
        6. Monitor for compliance with reporting requirements.
        7. Train staff on insider lending restrictions.
        8. Address violations promptly.
        9. Retain records for regulatory review.
        10. Prepare for examinations and enforcement.
        """,
        key_factors=[
            "Insider status",
            "Lending limits",
            "Approval procedures",
            "Terms and conditions",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 U.S.C. § 375a, 375b",
            "12 CFR 215 (Regulation O)"
        ],
        burden_holder="Member bank",
        adversary_position="Loan is not to an insider or limits were not exceeded.",
        counter_arguments=[
            "Insider definition is broad.",
            "Aggregate limits apply.",
            "Documentation is required."
        ],
        resolution_strategy="Apply Regulation O, review loans, and address deficiencies.",
        entity_scope="Member banks",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation O Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation W Transactions with Affiliates",
        keywords=["Regulation W", "Transactions with Affiliates", "Section 23A", "Section 23B", "FRB"],
        conclusion_template="Member banks must comply with quantitative and qualitative limits on transactions with affiliates under Regulation W.",
        reasoning_framework="""
        1. Identify affiliates as defined by Regulation W.
        2. Determine covered transactions and aggregate limits.
        3. Ensure terms are consistent with safe and sound banking practices.
        4. Obtain required collateral for credit transactions.
        5. Document all affiliate transactions.
        6. Monitor for compliance with quantitative limits.
        7. Train staff on affiliate transaction restrictions.
        8. Address violations promptly.
        9. Retain records for regulatory review.
        10. Prepare for examinations and enforcement.
        """,
        key_factors=[
            "Affiliate status",
            "Covered transaction definition",
            "Quantitative limits",
            "Collateral requirements",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 U.S.C. § 371c, 371c-1",
            "12 CFR 223 (Regulation W)"
        ],
        burden_holder="Member bank",
        adversary_position="Transaction is not with an affiliate or limits were not exceeded.",
        counter_arguments=[
            "Affiliate definition is broad.",
            "Aggregate limits apply.",
            "Documentation is required."
        ],
        resolution_strategy="Apply Regulation W, review transactions, and address deficiencies.",
        entity_scope="Member banks",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation W Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation C Fair Lending Data Analysis",
        keywords=["Regulation C", "HMDA", "Fair Lending", "Data Analysis", "Disparate Impact"],
        conclusion_template="Institutions must analyze HMDA data for fair lending risks, including disparate impact and treatment.",
        reasoning_framework="""
        1. Collect and review HMDA data for completeness.
        2. Analyze data for patterns of disparate impact or treatment.
        3. Investigate outliers and anomalies.
        4. Document findings and corrective actions.
        5. Train staff on fair lending analysis.
        6. Monitor for changes in regulatory requirements.
        7. Address public and regulatory inquiries.
        8. Retain records of analysis and remediation.
        9. Prepare for examinations and enforcement.
        10. Implement controls to prevent recurring issues.
        """,
        key_factors=[
            "Data completeness",
            "Analytical methodology",
            "Disparate impact indicators",
            "Corrective action",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 CFR 1003 (Regulation C)",
            "CFPB Fair Lending Guidance"
        ],
        burden_holder="Covered institution",
        adversary_position="No evidence of disparate impact or treatment.",
        counter_arguments=[
            "Statistical evidence may be sufficient.",
            "Documentation is required.",
            "Remediation may be necessary."
        ],
        resolution_strategy="Apply Regulation C, analyze data, and address findings.",
        entity_scope="Mortgage lenders, depository institutions",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFPB Fair Lending Enforcement"
    ),
    DoctrineBlock(
        topic="Regulation F Debt Collection Practices",
        keywords=["Regulation F", "Debt Collection", "FDCPA", "Consumer Protection", "Communication"],
        conclusion_template="Debt collectors must comply with communication, disclosure, and conduct requirements under Regulation F and the FDCPA.",
        reasoning_framework="""
        1. Determine whether the entity is a debt collector under the FDCPA.
        2. Provide required disclosures to consumers.
        3. Limit communications as prescribed by Regulation F.
        4. Prohibit harassment, false statements, and unfair practices.
        5. Document all communications and actions taken.
        6. Train staff on Regulation F requirements.
        7. Address consumer complaints and disputes.
        8. Retain records for regulatory review.
        9. Monitor for compliance with evolving standards.
        10. Prepare for examinations and enforcement.
        """,
        key_factors=[
            "Debt collector status",
            "Disclosure content and timing",
            "Communication limits",
            "Prohibited practices",
            "Recordkeeping"
        ],
        primary_authority=[
            "15 U.S.C. § 1692 et seq.",
            "12 CFR 1006 (Regulation F)"
        ],
        burden_holder="Debt collector",
        adversary_position="Entity is not a debt collector or requirements were met.",
        counter_arguments=[
            "Debt collector definition is broad.",
            "Strict procedural requirements.",
            "Documentation is required."
        ],
        resolution_strategy="Apply Regulation F and FDCPA, review practices, and address deficiencies.",
        entity_scope="Debt collectors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation F Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation S Foreign Account Tax Compliance",
        keywords=["Regulation S", "FATCA", "Foreign Account", "Tax Compliance", "Reporting"],
        conclusion_template="Foreign financial institutions must report information about U.S. account holders to the IRS under FATCA and Regulation S.",
        reasoning_framework="""
        1. Determine whether the institution is a foreign financial institution under FATCA.
        2. Identify U.S. account holders and reportable accounts.
        3. Collect required information and documentation.
        4. Report information to the IRS or local authority as required.
        5. Withhold tax on certain payments to non-compliant account holders.
        6. Train staff on FATCA requirements.
        7. Monitor for changes in regulatory requirements.
        8. Retain records of reporting and withholding.
        9. Address inquiries from account holders and regulators.
        10. Prepare for examinations and enforcement.
        """,
        key_factors=[
            "Foreign financial institution status",
            "U.S. account holder identification",
            "Reporting and withholding",
            "Documentation",
            "Recordkeeping"
        ],
        primary_authority=[
            "26 U.S.C. §§ 1471-1474 (FATCA)",
            "IRS FATCA Regulations"
        ],
        burden_holder="Foreign financial institution",
        adversary_position="Institution is not covered or reporting was adequate.",
        counter_arguments=[
            "FATCA coverage is broad.",
            "Strict reporting and withholding requirements.",
            "Documentation is required."
        ],
        resolution_strategy="Apply FATCA and Regulation S, review procedures, and address deficiencies.",
        entity_scope="Foreign financial institutions",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="IRS FATCA Enforcement Actions"
    ),
    DoctrineBlock(
        topic="Regulation GG Unlawful Internet Gambling Enforcement",
        keywords=["Regulation GG", "Unlawful Internet Gambling", "UIGEA", "Payment Systems", "Prohibited Transactions"],
        conclusion_template="Financial institutions must establish policies and procedures to prevent restricted transactions in connection with unlawful internet gambling.",
        reasoning_framework="""
        1. Determine whether the institution processes payments for internet gambling.
        2. Identify restricted transactions as defined by UIGEA.
        3. Implement policies and procedures to prevent prohibited transactions.
        4. Train staff on UIGEA and Regulation GG requirements.
        5. Monitor for suspicious activity related to internet gambling.
        6. Address violations promptly.
        7. Retain records of policies and actions taken.
        8. Review for changes in regulatory requirements.
        9. Prepare for examinations and enforcement.
        10. Update procedures as necessary.
        """,
        key_factors=[
            "Payment processing activities",
            "Restricted transaction identification",
            "Policies and procedures",
            "Staff training",
            "Recordkeeping"
        ],
        primary_authority=[
            "31 U.S.C. §§ 5361-5367",
            "31 CFR 132 (Regulation GG)"
        ],
        burden_holder="Financial institution",
        adversary_position="Institution does not process restricted transactions.",
        counter_arguments=[
            "Policies must be effective.",
            "Documentation is required.",
            "Regulators expect ongoing monitoring."
        ],
        resolution_strategy="Apply Regulation GG, review procedures, and address deficiencies.",
        entity_scope="All financial institutions",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation GG Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation U Margin Stock Credit",
        keywords=["Regulation U", "Margin Stock", "Credit", "Federal Reserve", "Loan Collateral"],
        conclusion_template="Banks must comply with margin requirements when extending credit secured by margin stock under Regulation U.",
        reasoning_framework="""
        1. Determine whether the loan is secured by margin stock.
        2. Calculate the maximum loan value of collateral.
        3. Ensure the loan does not exceed margin requirements.
        4. Obtain required purpose statements from borrowers.
        5. Retain records of credit extensions and collateral.
        6. Monitor for changes in margin requirements.
        7. Train staff on Regulation U requirements.
        8. Address violations promptly.
        9. Prepare for examinations and enforcement.
        10. Update procedures as necessary.
        """,
        key_factors=[
            "Margin stock collateral",
            "Loan value calculation",
            "Purpose statement",
            "Recordkeeping",
            "Staff training"
        ],
        primary_authority=[
            "12 CFR 221 (Regulation U)",
            "Federal Reserve Margin Requirements"
        ],
        burden_holder="Bank",
        adversary_position="Loan is not secured by margin stock or requirements were met.",
        counter_arguments=[
            "Margin requirements are strict.",
            "Documentation is required.",
            "Regulators expect ongoing monitoring."
        ],
        resolution_strategy="Apply Regulation U, review loans, and address deficiencies.",
        entity_scope="Banks extending credit secured by margin stock",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation U Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation Z Ability-to-Repay and Qualified Mortgage",
        keywords=["Regulation Z", "Ability-to-Repay", "Qualified Mortgage", "ATR", "Consumer Protection"],
        conclusion_template="Creditors must make a reasonable, good faith determination of a consumer's ability to repay a mortgage loan before consummation.",
        reasoning_framework="""
        1. Determine whether the loan is covered by ATR/QM requirements.
        2. Evaluate the consumer's income, assets, employment, and debt obligations.
        3. Calculate the monthly payment for the loan and other obligations.
        4. Document the underwriting process and findings.
        5. Identify whether the loan meets Qualified Mortgage criteria.
        6. Retain records of ATR/QM determinations.
        7. Train staff on ATR/QM requirements.
        8. Address consumer inquiries and disputes.
        9. Monitor for changes in regulatory requirements.
        10. Prepare for examinations and enforcement.
        """,
        key_factors=[
            "Loan coverage",
            "Underwriting process",
            "Qualified Mortgage criteria",
            "Documentation",
            "Staff training"
        ],
        primary_authority=[
            "12 CFR 1026.43 (Regulation Z)",
            "CFPB ATR/QM Rule"
        ],
        burden_holder="Creditor",
        adversary_position="Loan is not covered or ATR/QM requirements were met.",
        counter_arguments=[
            "ATR/QM requirements are strict.",
            "Documentation is required.",
            "Regulators expect robust underwriting."
        ],
        resolution_strategy="Apply Regulation Z, review underwriting, and address deficiencies.",
        entity_scope="Mortgage creditors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFPB ATR/QM Enforcement Actions"
    ),
    DoctrineBlock(
        topic="Regulation Y Bank Holding Company Activities",
        keywords=["Regulation Y", "Bank Holding Company", "Permissible Activities", "FRB", "Acquisitions"],
        conclusion_template="Bank holding companies must engage only in activities permissible under Regulation Y and obtain prior approval for certain acquisitions.",
        reasoning_framework="""
        1. Determine whether the entity is a bank holding company under Regulation Y.
        2. Identify proposed activities and acquisitions.
        3. Assess permissibility under Regulation Y and FRB guidance.
        4. Obtain required approvals for acquisitions.
        5. Document activities and approvals.
        6. Monitor for changes in regulatory requirements.
        7. Train staff on permissible activities.
        8. Address violations promptly.
        9. Retain records for regulatory review.
        10. Prepare for examinations and enforcement.
        """,
        key_factors=[
            "Bank holding company status",
            "Permissible activities",
            "Approval requirements",
            "Documentation",
            "Staff training"
        ],
        primary_authority=[
            "12 CFR 225 (Regulation Y)",
            "Bank Holding Company Act"
        ],
        burden_holder="Bank holding company",
        adversary_position="Activity is permissible or approval was obtained.",
        counter_arguments=[
            "Permissible activities are limited.",
            "Prior approval is required for acquisitions.",
            "Documentation is required."
        ],
        resolution_strategy="Apply Regulation Y, review activities, and address deficiencies.",
        entity_scope="Bank holding companies",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation Y Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation H State Member Bank Requirements",
        keywords=["Regulation H", "State Member Bank", "FRB", "Membership", "Compliance"],
        conclusion_template="State member banks must comply with membership, capital, and reporting requirements under Regulation H.",
        reasoning_framework="""
        1. Determine whether the bank is a state member bank.
        2. Assess compliance with capital and reserve requirements.
        3. Submit required reports to the FRB.
        4. Implement policies and procedures for compliance.
        5. Train staff on Regulation H requirements.
        6. Monitor for changes in regulatory requirements.
        7. Address violations promptly.
        8. Retain records for regulatory review.
        9. Prepare for examinations and enforcement.
        10. Update procedures as necessary.
        """,
        key_factors=[
            "State member bank status",
            "Capital and reserve requirements",
            "Reporting",
            "Policies and procedures",
            "Staff training"
        ],
        primary_authority=[
            "12 CFR 208 (Regulation H)",
            "Federal Reserve Act"
        ],
        burden_holder="State member bank",
        adversary_position="Bank is not a member or requirements were met.",
        counter_arguments=[
            "Membership requirements are strict.",
            "Documentation is required.",
            "Regulators expect ongoing compliance."
        ],
        resolution_strategy="Apply Regulation H, review compliance, and address deficiencies.",
        entity_scope="State member banks",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation H Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation T Credit by Brokers and Dealers",
        keywords=["Regulation T", "Credit", "Brokers", "Dealers", "Margin Requirements"],
        conclusion_template="Brokers and dealers must comply with margin requirements for securities credit under Regulation T.",
        reasoning_framework="""
        1. Determine whether the entity is a broker or dealer under Regulation T.
        2. Calculate margin requirements for securities credit.
        3. Ensure compliance with initial and maintenance margin requirements.
        4. Obtain required documentation from customers.
        5. Retain records of credit extensions and collateral.
        6. Monitor for changes in margin requirements.
        7. Train staff on Regulation T requirements.
        8. Address violations promptly.
        9. Prepare for examinations and enforcement.
        10. Update procedures as necessary.
        """,
        key_factors=[
            "Broker/dealer status",
            "Margin calculation",
            "Documentation",
            "Recordkeeping",
            "Staff training"
        ],
        primary_authority=[
            "12 CFR 220 (Regulation T)",
            "Federal Reserve Margin Requirements"
        ],
        burden_holder="Broker or dealer",
        adversary_position="Entity is not a broker/dealer or requirements were met.",
        counter_arguments=[
            "Margin requirements are strict.",
            "Documentation is required.",
            "Regulators expect ongoing monitoring."
        ],
        resolution_strategy="Apply Regulation T, review credit extensions, and address deficiencies.",
        entity_scope="Brokers and dealers",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation T Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation V Fair Credit Reporting",
        keywords=["Regulation V", "Fair Credit Reporting", "FCRA", "Consumer Report", "Accuracy"],
        conclusion_template="Furnishers of information to consumer reporting agencies must ensure accuracy and integrity of information under Regulation V.",
        reasoning_framework="""
        1. Determine whether the entity is a furnisher under Regulation V.
        2. Establish policies and procedures for accuracy and integrity.
        3. Investigate and respond to consumer disputes.
        4. Correct and update information as necessary.
        5. Train staff on Regulation V requirements.
        6. Monitor for changes in regulatory requirements.
        7. Retain records of investigations and corrections.
        8. Address consumer complaints and regulatory inquiries.
        9. Prepare for examinations and enforcement.
        10. Update procedures as necessary.
        """,
        key_factors=[
            "Furnisher status",
            "Policies and procedures",
            "Dispute investigation",
            "Correction and updating",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 CFR 1022 (Regulation V)",
            "FCRA"
        ],
        burden_holder="Furnisher of information",
        adversary_position="Entity is not a furnisher or requirements were met.",
        counter_arguments=[
            "Accuracy and integrity are strictly enforced.",
            "Documentation is required.",
            "Regulators expect robust procedures."
        ],
        resolution_strategy="Apply Regulation V, review information furnished, and address deficiencies.",
        entity_scope="Furnishers of information to consumer reporting agencies",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Regulation V Official Interpretations"
    ),
    DoctrineBlock(
        topic="Regulation Z Credit Card Act Requirements",
        keywords=["Regulation Z", "Credit Card Act", "Consumer Protection", "Disclosure", "Penalty Fees"],
        conclusion_template="Creditors must comply with disclosure, penalty fee, and interest rate requirements for credit cards under Regulation Z and the Credit Card Act.",
        reasoning_framework="""
        1. Determine whether the account is a credit card covered by Regulation Z.
        2. Provide required disclosures for rates, fees, and terms.
        3. Limit penalty fees and interest rate increases as prescribed.
        4. Implement procedures for periodic statement delivery.
        5. Train staff on Regulation Z requirements.
        6. Monitor for changes in regulatory requirements.
        7. Address consumer complaints and disputes.
        8. Retain records of disclosures and communications.
        9. Prepare for examinations and enforcement.
        10. Update procedures as necessary.
        """,
        key_factors=[
            "Credit card coverage",
            "Disclosure content and timing",
            "Penalty fee limits",
            "Interest rate increase restrictions",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 CFR 1026 (Regulation Z)",
            "Credit Card Accountability Responsibility and Disclosure Act"
        ],
        burden_holder="Creditor",
        adversary_position="Account is not a credit card or requirements were met.",
        counter_arguments=[
            "Disclosure and fee requirements are strict.",
            "Documentation is required.",
            "Regulators expect ongoing compliance."
        ],
        resolution_strategy="Apply Regulation Z, review disclosures, and address deficiencies.",
        entity_scope="Credit card issuers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFPB Credit Card Act Enforcement"
    ),
    DoctrineBlock(
        topic="Regulation Z Loan Originator Compensation",
        keywords=["Regulation Z", "Loan Originator Compensation", "Mortgage", "Steering", "Consumer Protection"],
        conclusion_template="Creditors and mortgage brokers must not compensate loan originators based on loan terms or conditions, and must comply with anti-steering provisions under Regulation Z.",
        reasoning_framework="""
        1. Determine whether the compensation arrangement is covered by Regulation Z.
        2. Assess whether compensation is based on loan terms or conditions.
        3. Implement anti-steering policies and procedures.
        4. Train staff on compensation and steering prohibitions.
        5. Monitor for compliance with regulatory requirements.
        6. Retain records of compensation arrangements.
        7. Address consumer complaints and disputes.
        8. Prepare for examinations and enforcement.
        9. Update procedures as necessary.
        10. Correct violations promptly.
        """,
        key_factors=[
            "Compensation arrangement",
            "Loan terms or conditions",
            "Anti-steering policies",
            "Staff training",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 CFR 1026.36 (Regulation Z)",
            "CFPB Loan Originator Compensation Rule"
        ],
        burden_holder="Creditor or mortgage broker",
        adversary_position="Compensation is not based on loan terms or requirements were met.",
        counter_arguments=[
            "Compensation prohibitions are strict.",
            "Documentation is required.",
            "Regulators expect robust controls."
        ],
        resolution_strategy="Apply Regulation Z, review compensation, and address deficiencies.",
        entity_scope="Creditors and mortgage brokers",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFPB Loan Originator Compensation Enforcement"
    ),
    DoctrineBlock(
        topic="Regulation Z High-Cost Mortgage Protections",
        keywords=["Regulation Z", "High-Cost Mortgage", "HOEPA", "Consumer Protection", "Disclosure"],
        conclusion_template="Creditors must provide special disclosures and protections for high-cost mortgages under HOEPA and Regulation Z.",
        reasoning_framework="""
        1. Determine whether the loan is a high-cost mortgage under HOEPA thresholds.
        2. Provide required disclosures to consumers.
        3. Prohibit certain loan terms and practices (e.g., balloon payments, prepayment penalties).
        4. Implement procedures for counseling and consumer protections.
        5. Train staff on high-cost mortgage requirements.
        6. Monitor for compliance with regulatory requirements.
        7. Retain records of disclosures and counseling.
        8. Address consumer complaints and disputes.
        9. Prepare for examinations and enforcement.
        10. Update procedures as necessary.
        """,
        key_factors=[
            "High-cost mortgage threshold",
            "Disclosure content and timing",
            "Prohibited terms and practices",
            "Counseling requirements",
            "Recordkeeping"
        ],
        primary_authority=[
            "12 CFR