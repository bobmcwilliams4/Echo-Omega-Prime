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
        topic="Asset Purchase vs Stock Purchase Structure",
        keywords=["asset purchase", "stock purchase", "structure", "transaction form", "liabilities", "tax basis"],
        conclusion_template="The optimal transaction structure is a {structure_type} based on allocation of liabilities, tax implications, and consent requirements.",
        reasoning_framework=(
            "1. Identify the primary objectives of buyer and seller (e.g., liability allocation, tax treatment, speed).\n"
            "2. Analyze whether the target's assets or stock are being acquired, and the implications for assumed liabilities.\n"
            "3. Consider the effect on third-party consents, assignability of contracts, and regulatory approvals.\n"
            "4. Evaluate tax consequences for both parties, including step-up in basis and potential double taxation.\n"
            "5. Assess the impact on employees, permits, and ongoing operations.\n"
            "6. Weigh the commercial, legal, and tax risks associated with each structure.\n"
            "7. Determine whether the parties' goals are best served by an asset or stock purchase, or a hybrid structure.\n"
            "8. Document the rationale for the chosen structure and address any residual risks contractually."
        ),
        key_factors=[
            "Assumption of liabilities",
            "Tax basis step-up",
            "Third-party consents",
            "Regulatory approvals",
            "Employee transfer",
            "Contract assignability",
            "Seller's entity type"
        ],
        primary_authority=[
            "Internal Revenue Code (IRC) Sections 338, 1060",
            "Delaware General Corporation Law (DGCL)",
            "Relevant state corporate statutes"
        ],
        burden_holder="Buyer (to justify structure and diligence liabilities)",
        adversary_position="Seller may prefer stock sale for simplicity and tax reasons",
        counter_arguments=[
            "Asset purchase may trigger more consents and require asset-by-asset transfer",
            "Stock purchase may saddle buyer with unknown liabilities"
        ],
        resolution_strategy="Negotiate representations, indemnities, and structure to balance risks and benefits.",
        entity_scope="Corporations, LLCs, Partnerships",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Zenz v. Quinlivan, 213 F.2d 914 (6th Cir. 1954)"
    ),
    DoctrineBlock(
        topic="Hart-Scott-Rodino HSR Filing Thresholds",
        keywords=["HSR", "antitrust", "premerger notification", "thresholds", "FTC", "DOJ", "size-of-transaction"],
        conclusion_template="HSR notification is {required/not required} based on the transaction value and parties' size.",
        reasoning_framework=(
            "1. Determine if the transaction is subject to HSR by evaluating whether it involves the acquisition of voting securities, assets, or non-corporate interests.\n"
            "2. Calculate the 'size of transaction' under 16 C.F.R. § 801.10, considering all relevant consideration.\n"
            "3. Compare the transaction value to the current HSR reporting threshold (updated annually; e.g., $111.4 million for 2023).\n"
            "4. Assess the 'size of person' test: one party must have $222.7 million or more in total assets/sales and the other $22.3 million or more (2023 values), unless the transaction exceeds the higher threshold ($445.5 million).\n"
            "5. Identify any applicable exemptions (e.g., intraperson, foreign assets, real property).\n"
            "6. If thresholds are met and no exemptions apply, HSR filing is required; otherwise, it is not.\n"
            "7. Consider timing implications, waiting periods, and potential penalties for non-compliance."
        ),
        key_factors=[
            "Transaction value",
            "Parties' size (assets/sales)",
            "Type of transaction",
            "Exemptions applicability",
            "Annual threshold adjustments"
        ],
        primary_authority=[
            "Hart-Scott-Rodino Antitrust Improvements Act of 1976",
            "16 C.F.R. Parts 801-803",
            "FTC Premerger Notification Office Guidance"
        ],
        burden_holder="Acquiring party (to file and pay fee)",
        adversary_position="Target may resist disclosure or delay",
        counter_arguments=[
            "Transaction may qualify for an exemption",
            "Parties may dispute valuation or applicability"
        ],
        resolution_strategy="Conduct HSR analysis early and seek FTC guidance if unclear.",
        entity_scope="Corporations, LLCs, Partnerships, Non-U.S. entities with U.S. nexus",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="United States v. Archer-Daniels-Midland Co., 866 F.2d 242 (8th Cir. 1988)"
    ),
    DoctrineBlock(
        topic="CFIUS Foreign Investment Review FIRRMA",
        keywords=["CFIUS", "FIRRMA", "foreign investment", "national security", "critical technology", "real estate"],
        conclusion_template="CFIUS review is {triggered/not triggered} due to the involvement of a foreign person and covered transaction.",
        reasoning_framework=(
            "1. Identify whether the transaction involves a 'covered transaction' under FIRRMA, including non-controlling investments in critical technology, infrastructure, or sensitive data businesses.\n"
            "2. Determine if a 'foreign person' is acquiring control or certain rights in the U.S. business.\n"
            "3. Assess whether the target is involved in critical technology, infrastructure, or sensitive personal data.\n"
            "4. Evaluate mandatory declaration requirements (e.g., TID businesses, certain government contracts).\n"
            "5. Consider real estate transactions near sensitive sites.\n"
            "6. Analyze the risk of CFIUS review, including potential for mitigation or prohibition.\n"
            "7. Prepare for CFIUS filing, voluntary or mandatory, and consider timing and deal certainty impacts."
        ),
        key_factors=[
            "Foreign person involvement",
            "Control or substantial interest",
            "Critical technology/infrastructure/data",
            "Mandatory vs voluntary filing",
            "National security risk"
        ],
        primary_authority=[
            "Foreign Investment Risk Review Modernization Act (FIRRMA)",
            "50 U.S.C. § 4565",
            "31 C.F.R. Parts 800, 802"
        ],
        burden_holder="Acquirer (to file and disclose foreign ownership)",
        adversary_position="Seller may resist or seek to limit CFIUS review",
        counter_arguments=[
            "Transaction does not involve covered business",
            "No control or substantial interest is acquired"
        ],
        resolution_strategy="Conduct CFIUS risk assessment and engage with CFIUS counsel early.",
        entity_scope="U.S. businesses, foreign investors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Ralls Corp. v. CFIUS, 758 F.3d 296 (D.C. Cir. 2014)"
    ),
    DoctrineBlock(
        topic="Tax-Free Reorganizations IRC Section 368",
        keywords=["tax-free", "reorganization", "IRC 368", "merger", "continuity of interest", "continuity of business enterprise"],
        conclusion_template="The transaction {qualifies/does not qualify} as a tax-free reorganization under IRC §368.",
        reasoning_framework=(
            "1. Identify the type of reorganization (A, B, C, D, etc.) under IRC §368(a)(1).\n"
            "2. Analyze whether the statutory and regulatory requirements for the chosen form are met.\n"
            "3. Confirm continuity of interest (COI) and continuity of business enterprise (COBE) are satisfied.\n"
            "4. Evaluate the consideration mix (stock vs cash) and ensure the requisite percentage of equity is used.\n"
            "5. Assess whether the transaction has a bona fide business purpose and is not a device for tax avoidance.\n"
            "6. Review IRS rulings and relevant case law for interpretive guidance.\n"
            "7. Document compliance and seek a tax opinion if necessary."
        ),
        key_factors=[
            "Type of reorganization",
            "Continuity of interest",
            "Continuity of business enterprise",
            "Consideration structure",
            "Business purpose"
        ],
        primary_authority=[
            "Internal Revenue Code §368",
            "Treasury Regulations §1.368-1",
            "IRS Revenue Rulings"
        ],
        burden_holder="Taxpayer (to prove qualification for nonrecognition)",
        adversary_position="IRS may challenge if requirements not met",
        counter_arguments=[
            "Transaction lacks sufficient equity consideration",
            "No continuity of business enterprise"
        ],
        resolution_strategy="Structure transaction to satisfy all statutory and regulatory requirements.",
        entity_scope="Corporations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Helvering v. Southwest Consolidated Corp., 315 U.S. 194 (1942)"
    ),
    DoctrineBlock(
        topic="Delaware Merger Statute DGCL Section 251",
        keywords=["Delaware", "merger", "DGCL 251", "board approval", "stockholder vote"],
        conclusion_template="The merger is {valid/invalid} under DGCL §251 based on compliance with statutory requirements.",
        reasoning_framework=(
            "1. Confirm both constituent corporations are Delaware entities or at least one is and the other is permitted under its jurisdiction.\n"
            "2. Ensure the merger agreement is approved by the board of directors of each corporation.\n"
            "3. Provide notice to stockholders and obtain the requisite stockholder approval (majority of outstanding shares).\n"
            "4. File the certificate of merger with the Delaware Secretary of State.\n"
            "5. Address appraisal rights and dissenters' remedies if applicable.\n"
            "6. Confirm compliance with any special provisions (e.g., short-form merger, interested stockholder rules).\n"
            "7. Review for any defects in process that could render the merger void or voidable."
        ),
        key_factors=[
            "Board approval",
            "Stockholder approval",
            "Proper notice",
            "Certificate of merger filing",
            "Appraisal rights"
        ],
        primary_authority=[
            "Delaware General Corporation Law §251",
            "DGCL §§262, 228",
            "Delaware case law"
        ],
        burden_holder="Corporation (to comply with statutory process)",
        adversary_position="Dissenting stockholders may challenge process or valuation",
        counter_arguments=[
            "Failure to obtain proper approval",
            "Defective notice or disclosure"
        ],
        resolution_strategy="Strict adherence to statutory process and robust disclosure.",
        entity_scope="Delaware corporations",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="Weinberger v. UOP, Inc., 457 A.2d 701 (Del. 1983)"
    ),
    DoctrineBlock(
        topic="Material Adverse Change MAC Clauses",
        keywords=["MAC", "material adverse change", "material adverse effect", "deal termination", "risk allocation"],
        conclusion_template="A Material Adverse Change has {occurred/not occurred} under the agreement's MAC clause.",
        reasoning_framework=(
            "1. Review the definition of 'Material Adverse Change' or 'Material Adverse Effect' in the agreement.\n"
            "2. Compare the alleged adverse event to the definition and carve-outs (e.g., general market conditions, acts of God).\n"
            "3. Assess the quantitative and qualitative impact on the target's business, financial condition, or prospects.\n"
            "4. Consider the duration and severity of the change.\n"
            "5. Evaluate relevant case law interpreting MAC clauses, especially in the Delaware courts.\n"
            "6. Determine whether the event is excluded by a carve-out and, if so, whether the exclusion is overridden by disproportionate effect language.\n"
            "7. Document findings and prepare for potential litigation or renegotiation."
        ),
        key_factors=[
            "Definition of MAC in agreement",
            "Nature and scope of adverse event",
            "Carve-outs and exceptions",
            "Duration and severity",
            "Disproportionate impact"
        ],
        primary_authority=[
            "Delaware case law",
            "Akorn, Inc. v. Fresenius Kabi AG, 2018 WL 4719347 (Del. Ch. 2018)",
            "Transaction agreement"
        ],
        burden_holder="Party seeking to invoke MAC (usually buyer)",
        adversary_position="Counterparty will argue no MAC or event is carved out",
        counter_arguments=[
            "Adverse event is temporary or industry-wide",
            "Event is subject to a carve-out"
        ],
        resolution_strategy="Apply Delaware precedent and negotiate specific MAC language.",
        entity_scope="All M&A transactions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Akorn, Inc. v. Fresenius Kabi AG, 2018 WL 4719347 (Del. Ch. 2018)"
    ),
    DoctrineBlock(
        topic="Representations and Warranties Insurance",
        keywords=["RWI", "reps and warranties insurance", "indemnity", "risk allocation", "policy exclusions"],
        conclusion_template="RWI {covers/does not cover} the identified breach based on policy terms and exclusions.",
        reasoning_framework=(
            "1. Review the scope of the representations and warranties insurance policy, including covered reps and exclusions.\n"
            "2. Determine whether the alleged breach falls within the covered representations.\n"
            "3. Analyze policy exclusions (e.g., known breaches, interim breaches, forward-looking statements).\n"
            "4. Assess the impact of retention, caps, and survival periods.\n"
            "5. Consider the claims process, including notice, cooperation, and timing.\n"
            "6. Evaluate the interplay between RWI and seller indemnity (if any).\n"
            "7. Document findings and coordinate with insurance broker/counsel."
        ),
        key_factors=[
            "Policy scope",
            "Exclusions",
            "Retention and caps",
            "Claims process",
            "Interplay with indemnity"
        ],
        primary_authority=[
            "RWI policy",
            "Market practice",
            "Broker/insurer guidelines"
        ],
        burden_holder="Insured party (to prove covered loss)",
        adversary_position="Insurer may deny coverage based on exclusions",
        counter_arguments=[
            "Breach was known or disclosed",
            "Breach occurred outside policy period"
        ],
        resolution_strategy="Negotiate robust policy terms and coordinate with insurer on claims.",
        entity_scope="Private M&A transactions",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="No controlling precedent; market practice governs"
    ),
    DoctrineBlock(
        topic="Earnouts and Contingent Consideration",
        keywords=["earnout", "contingent consideration", "post-closing adjustment", "performance targets"],
        conclusion_template="The earnout payment is {owed/not owed} based on achievement of agreed performance metrics.",
        reasoning_framework=(
            "1. Review the earnout provisions, including performance metrics, measurement periods, and calculation methodology.\n"
            "2. Assess whether the target has achieved the specified financial or operational milestones.\n"
            "3. Evaluate the buyer's post-closing obligations regarding operation of the business (e.g., efforts standards, anti-sabotage covenants).\n"
            "4. Consider disputes over accounting methods, adjustments, or manipulation.\n"
            "5. Examine dispute resolution mechanisms, such as expert determination or arbitration.\n"
            "6. Document findings and communicate with counterparties as required."
        ),
        key_factors=[
            "Performance metrics",
            "Measurement period",
            "Calculation methodology",
            "Buyer's post-closing obligations",
            "Dispute resolution process"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law",
            "Accounting standards"
        ],
        burden_holder="Seller (to prove achievement of earnout targets)",
        adversary_position="Buyer may argue targets not met or dispute calculation",
        counter_arguments=[
            "Buyer failed to operate business in good faith",
            "Metrics were manipulated"
        ],
        resolution_strategy="Draft clear earnout provisions and provide for expert dispute resolution.",
        entity_scope="All M&A transactions with contingent consideration",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Airborne Health, Inc. v. Squid Soap, LP, 984 A.2d 126 (Del. Ch. 2009)"
    ),
    DoctrineBlock(
        topic="Due Diligence and Sandbagging",
        keywords=["due diligence", "sandbagging", "knowledge", "reps and warranties", "pre-closing awareness"],
        conclusion_template="The buyer {may/may not} bring a claim for breach despite pre-closing knowledge, based on sandbagging provisions.",
        reasoning_framework=(
            "1. Review the transaction agreement for express sandbagging or anti-sandbagging provisions.\n"
            "2. Analyze whether the buyer had actual or constructive knowledge of the breach prior to closing.\n"
            "3. Consider the governing law; Delaware generally permits sandbagging absent contractual prohibition.\n"
            "4. Evaluate the impact of disclosure schedules and diligence process.\n"
            "5. Assess the parties' intent as reflected in negotiation history and agreement language.\n"
            "6. Document findings and prepare for potential indemnity claims."
        ),
        key_factors=[
            "Contractual sandbagging provision",
            "Buyer's knowledge",
            "Governing law",
            "Disclosure schedules",
            "Negotiation history"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law",
            "Market practice"
        ],
        burden_holder="Buyer (to prove breach and lack of anti-sandbagging clause)",
        adversary_position="Seller may argue buyer knew of breach",
        counter_arguments=[
            "Agreement prohibits sandbagging",
            "Buyer had actual knowledge"
        ],
        resolution_strategy="Negotiate express sandbagging language and document diligence process.",
        entity_scope="All M&A transactions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="CBS Inc. v. Ziff-Davis Publishing Co., 553 N.E.2d 997 (N.Y. 1990)"
    ),
    DoctrineBlock(
        topic="Working Capital Adjustments",
        keywords=["working capital", "purchase price adjustment", "closing balance sheet", "net working capital target"],
        conclusion_template="The purchase price is {increased/decreased} by the working capital adjustment as calculated.",
        reasoning_framework=(
            "1. Review the agreement's working capital adjustment provisions, including definitions and target levels.\n"
            "2. Prepare or review the closing balance sheet in accordance with agreed accounting principles.\n"
            "3. Calculate actual net working capital at closing and compare to the target.\n"
            "4. Adjust the purchase price upward or downward based on the difference.\n"
            "5. Consider disputes over accounting policies, estimates, or post-closing adjustments.\n"
            "6. Utilize dispute resolution mechanisms as provided in the agreement."
        ),
        key_factors=[
            "Definition of working capital",
            "Target level",
            "Accounting principles",
            "Closing balance sheet",
            "Dispute resolution process"
        ],
        primary_authority=[
            "Transaction agreement",
            "GAAP or specified accounting standards",
            "Delaware case law"
        ],
        burden_holder="Buyer/Seller (as applicable, to support calculation)",
        adversary_position="Counterparty may dispute calculation or accounting treatment",
        counter_arguments=[
            "Improper accounting methods used",
            "Estimates manipulated"
        ],
        resolution_strategy="Draft clear definitions and provide for expert resolution of disputes.",
        entity_scope="All M&A transactions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Chicago Bridge & Iron Co. N.V. v. Westinghouse Electric Co. LLC, 166 A.3d 912 (Del. 2017)"
    ),
    DoctrineBlock(
        topic="Tender Offers and Williams Act",
        keywords=["tender offer", "Williams Act", "Schedule TO", "public company", "SEC", "disclosure"],
        conclusion_template="The tender offer {complies/does not comply} with the Williams Act and SEC requirements.",
        reasoning_framework=(
            "1. Determine whether the transaction constitutes a tender offer under the Williams Act.\n"
            "2. Review the requirements for disclosure, timing, and withdrawal rights under Sections 13(d), 14(d), and 14(e) of the Exchange Act.\n"
            "3. Ensure Schedule TO and related filings are made with the SEC.\n"
            "4. Provide required disclosures to security holders, including price, terms, and bidder identity.\n"
            "5. Observe the minimum offer period and proration requirements.\n"
            "6. Comply with anti-fraud and anti-manipulation provisions.\n"
            "7. Address state anti-takeover statutes as applicable."
        ),
        key_factors=[
            "Nature of offer",
            "Disclosure compliance",
            "Withdrawal rights",
            "Timing and proration",
            "SEC filings"
        ],
        primary_authority=[
            "Williams Act (Securities Exchange Act of 1934 §§13(d), 14(d), 14(e))",
            "SEC Rules 14d-1 et seq.",
            "State anti-takeover laws"
        ],
        burden_holder="Bidder (to comply with disclosure and process)",
        adversary_position="Target may challenge sufficiency of disclosure or process",
        counter_arguments=[
            "Failure to disclose material information",
            "Improper offer structure"
        ],
        resolution_strategy="Strict compliance with SEC rules and robust disclosure.",
        entity_scope="Public companies",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Piper v. Chris-Craft Industries, Inc., 430 U.S. 1 (1977)"
    ),
    DoctrineBlock(
        topic="Indemnification Baskets and Caps",
        keywords=["indemnity", "basket", "cap", "survival period", "deductible", "escrow"],
        conclusion_template="Indemnification for the claim is {available/not available} based on basket and cap provisions.",
        reasoning_framework=(
            "1. Review the indemnification provisions, including the basket (threshold) and cap (maximum liability).\n"
            "2. Determine whether the claim exceeds the basket or deductible.\n"
            "3. Assess whether the aggregate claims have reached the cap.\n"
            "4. Consider exceptions (e.g., fraud, fundamental reps) that may not be subject to basket or cap.\n"
            "5. Evaluate the survival period and whether the claim was timely made.\n"
            "6. Review escrow or holdback arrangements for satisfaction of claims."
        ),
        key_factors=[
            "Basket amount",
            "Cap amount",
            "Exceptions to basket/cap",
            "Survival period",
            "Escrow arrangements"
        ],
        primary_authority=[
            "Transaction agreement",
            "Market practice",
            "Delaware case law"
        ],
        burden_holder="Claimant (to prove claim exceeds basket and is within cap)",
        adversary_position="Indemnitor may argue claim is below basket or cap is exhausted",
        counter_arguments=[
            "Claim is for fraud (not subject to cap)",
            "Claim made after survival period"
        ],
        resolution_strategy="Negotiate clear indemnity provisions and track claims against basket/cap.",
        entity_scope="All M&A transactions",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Cigna Health & Life Ins. Co. v. Audax Health Solutions, Inc., 107 A.3d 1082 (Del. Ch. 2014)"
    ),
    DoctrineBlock(
        topic="Financing Conditions and Committed Financing",
        keywords=["financing", "debt commitment", "financing out", "reverse termination fee", "lender letters"],
        conclusion_template="The buyer {may/may not} terminate for failure to obtain financing based on agreement terms.",
        reasoning_framework=(
            "1. Review the agreement for a financing condition or 'financing out.'\n"
            "2. Analyze the buyer's obligations to use efforts to obtain financing (reasonable best efforts, etc.).\n"
            "3. Examine the terms of the debt commitment letter and any conditions precedent.\n"
            "4. Assess the consequences of financing failure (reverse termination fee, specific performance, etc.).\n"
            "5. Consider market practice and the parties' negotiation history.\n"
            "6. Document findings and prepare for potential enforcement or termination."
        ),
        key_factors=[
            "Existence of financing condition",
            "Efforts standard",
            "Debt commitment letter terms",
            "Reverse termination fee",
            "Remedies for breach"
        ],
        primary_authority=[
            "Transaction agreement",
            "Debt commitment letter",
            "Delaware case law"
        ],
        burden_holder="Buyer (to prove diligent efforts or satisfaction of condition)",
        adversary_position="Seller may seek specific performance or fee",
        counter_arguments=[
            "Buyer failed to use required efforts",
            "Financing condition not satisfied"
        ],
        resolution_strategy="Negotiate clear financing provisions and remedies for failure.",
        entity_scope="Leveraged buyouts, large M&A",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Hexion Specialty Chemicals, Inc. v. Huntsman Corp., 965 A.2d 715 (Del. Ch. 2008)"
    ),
    DoctrineBlock(
        topic="Regulatory Approval Conditions and Efforts Standards",
        keywords=["regulatory approval", "efforts", "best efforts", "reasonable efforts", "antitrust", "CFIUS"],
        conclusion_template="The parties {have/have not} satisfied their obligations to obtain regulatory approvals under the efforts standard.",
        reasoning_framework=(
            "1. Review the agreement for the applicable efforts standard (best efforts, reasonable best efforts, etc.).\n"
            "2. Identify required regulatory approvals (antitrust, CFIUS, industry-specific).\n"
            "3. Analyze the parties' actions to obtain approvals, including timing, filings, and cooperation.\n"
            "4. Consider whether the parties are required to accept conditions or divestitures.\n"
            "5. Evaluate any 'hell or high water' provisions or limitations on required actions.\n"
            "6. Document compliance and prepare for potential disputes."
        ),
        key_factors=[
            "Efforts standard",
            "Required approvals",
            "Parties' actions",
            "Willingness to accept conditions",
            "Timing"
        ],
        primary_authority=[
            "Transaction agreement",
            "FTC/DOJ guidance",
            "Delaware case law"
        ],
        burden_holder="Both parties (to act in good faith and use required efforts)",
        adversary_position="Counterparty may allege failure to use required efforts",
        counter_arguments=[
            "Efforts standard not met",
            "Party refused to accept reasonable conditions"
        ],
        resolution_strategy="Negotiate clear efforts standards and document compliance.",
        entity_scope="All regulated M&A transactions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Williams Cos. v. Energy Transfer Equity, L.P., 159 A.3d 264 (Del. 2017)"
    ),
    DoctrineBlock(
        topic="Non-Compete and Non-Solicitation Covenants",
        keywords=["non-compete", "non-solicit", "restrictive covenant", "enforceability", "blue pencil"],
        conclusion_template="The covenant is {enforceable/unenforceable} based on scope, duration, and jurisdiction.",
        reasoning_framework=(
            "1. Review the scope of the non-compete and non-solicitation provisions (geography, duration, activities).\n"
            "2. Assess whether the restrictions are reasonable and necessary to protect legitimate business interests.\n"
            "3. Consider applicable state law on enforceability and blue-penciling.\n"
            "4. Evaluate whether consideration was provided and whether the covenant is ancillary to the sale of a business.\n"
            "5. Analyze the impact on the seller's ability to earn a livelihood.\n"
            "6. Prepare for potential litigation or modification by court."
        ),
        key_factors=[
            "Scope of restriction",
            "Duration",
            "Geographic area",
            "Legitimate business interest",
            "State law"
        ],
        primary_authority=[
            "State law (e.g., Delaware, California)",
            "Transaction agreement",
            "Restatement (Second) of Contracts §188"
        ],
        burden_holder="Party seeking enforcement",
        adversary_position="Restricted party may argue overbreadth or lack of necessity",
        counter_arguments=[
            "Restriction is overbroad",
            "No legitimate business interest"
        ],
        resolution_strategy="Draft narrowly tailored covenants and comply with state law.",
        entity_scope="All M&A transactions",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="BAM Capital, LLC v. Pagliara, 2021 WL 1174693 (Del. Ch. 2021)"
    ),
    # Additional doctrines for comprehensive coverage (total 40+)
    DoctrineBlock(
        topic="Successor Liability in Asset Purchases",
        keywords=["successor liability", "asset purchase", "product liability", "fraudulent transfer"],
        conclusion_template="The buyer {is/is not} subject to successor liability based on exceptions to the general rule.",
        reasoning_framework=(
            "1. Apply the general rule that asset purchasers do not assume seller's liabilities unless an exception applies.\n"
            "2. Analyze exceptions: express/implied assumption, de facto merger, mere continuation, or fraudulent transfer.\n"
            "3. Evaluate transaction structure and documentation for assumption of liabilities.\n"
            "4. Consider product liability and environmental statutes that may impose successor liability.\n"
            "5. Review relevant case law for jurisdiction-specific application."
        ),
        key_factors=[
            "Express or implied assumption",
            "De facto merger",
            "Mere continuation",
            "Fraudulent transfer",
            "Statutory successor liability"
        ],
        primary_authority=[
            "State corporate law",
            "Product liability statutes",
            "Federal environmental statutes"
        ],
        burden_holder="Claimant (to prove exception applies)",
        adversary_position="Buyer argues no assumption of liability",
        counter_arguments=[
            "Transaction structured to avoid liability",
            "No exception to general rule"
        ],
        resolution_strategy="Draft clear assumption/exclusion provisions and conduct due diligence.",
        entity_scope="Asset purchases",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Ray v. Alad Corp., 560 P.2d 3 (Cal. 1977)"
    ),
    DoctrineBlock(
        topic="Appraisal Rights and Fair Value",
        keywords=["appraisal rights", "fair value", "DGCL 262", "dissenting stockholder", "merger consideration"],
        conclusion_template="The fair value of shares is determined to be ${fair_value} per share under DGCL §262.",
        reasoning_framework=(
            "1. Confirm that the transaction triggers appraisal rights under DGCL §262 or similar statute.\n"
            "2. Review the process for perfecting appraisal rights (timely demand, no vote in favor, etc.).\n"
            "3. Analyze the factors considered in determining 'fair value,' including going concern value, unaffected market price, and deal price.\n"
            "4. Exclude value arising from the merger itself (synergies, etc.).\n"
            "5. Consider expert testimony and valuation methodologies (DCF, comparable companies, etc.).\n"
            "6. Review Delaware case law for recent fair value determinations."
        ),
        key_factors=[
            "Triggering transaction",
            "Process compliance",
            "Valuation methodology",
            "Exclusion of merger synergies",
            "Recent precedent"
        ],
        primary_authority=[
            "DGCL §262",
            "Delaware case law"
        ],
        burden_holder="Dissenting stockholder (to perfect rights and support value)",
        adversary_position="Company argues for lower fair value",
        counter_arguments=[
            "Deal price reflects fair value",
            "Stockholder failed to perfect rights"
        ],
        resolution_strategy="Strict compliance with process and use of expert valuation.",
        entity_scope="Delaware corporations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Dell, Inc. v. Magnetar Global Event Driven Master Fund Ltd., 177 A.3d 1 (Del. 2017)"
    ),
    DoctrineBlock(
        topic="Anti-Assignment Clauses and Change of Control",
        keywords=["anti-assignment", "change of control", "contract consent", "assignment by operation of law"],
        conclusion_template="The transaction {requires/does not require} third-party consent due to anti-assignment or change of control provisions.",
        reasoning_framework=(
            "1. Review target's material contracts for anti-assignment and change of control clauses.\n"
            "2. Determine whether the transaction constitutes an assignment by operation of law (e.g., merger, stock sale).\n"
            "3. Analyze the scope of the clause and whether consent is required for the contemplated transaction.\n"
            "4. Consider the impact of non-consent on deal timing and value.\n"
            "5. Negotiate with counterparties or seek waivers as necessary."
        ),
        key_factors=[
            "Contract language",
            "Transaction structure",
            "Assignment by operation of law",
            "Counterparty consent",
            "Materiality to business"
        ],
        primary_authority=[
            "Contract law",
            "Delaware case law"
        ],
        burden_holder="Buyer (to identify and obtain consents)",
        adversary_position="Counterparty may withhold consent",
        counter_arguments=[
            "No assignment occurred",
            "Clause does not apply to transaction"
        ],
        resolution_strategy="Diligence all contracts and negotiate consents or waivers.",
        entity_scope="All M&A transactions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Meso Scale Diagnostics, LLC v. Roche Diagnostics GmbH, 62 A.3d 62 (Del. Ch. 2013)"
    ),
    DoctrineBlock(
        topic="Employee Matters and 280G Parachute Payments",
        keywords=["employee", "280G", "golden parachute", "change in control", "excise tax"],
        conclusion_template="Section 280G {applies/does not apply} and parachute payments are {subject/not subject} to excise tax.",
        reasoning_framework=(
            "1. Identify whether the transaction triggers a change in control for purposes of IRC §280G.\n"
            "2. Review compensation arrangements for potential parachute payments (aggregate >3x base amount).\n"
            "3. Analyze whether payments are subject to the excise tax or can be exempted by stockholder approval (private companies).\n"
            "4. Calculate potential excise tax and loss of deduction.\n"
            "5. Consider mitigation strategies (e.g., gross-ups, waivers, stockholder vote)."
        ),
        key_factors=[
            "Change in control",
            "Parachute payment calculation",
            "Stockholder approval",
            "Excise tax exposure",
            "Mitigation strategies"
        ],
        primary_authority=[
            "IRC §280G",
            "Treasury Regulations",
            "IRS guidance"
        ],
        burden_holder="Company (to calculate and disclose payments)",
        adversary_position="Employee may seek gross-up or alternative arrangements",
        counter_arguments=[
            "No change in control occurred",
            "Payments do not exceed threshold"
        ],
        resolution_strategy="Conduct 280G analysis and obtain stockholder approval if needed.",
        entity_scope="C corporations",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IRC §280G and related regulations"
    ),
    DoctrineBlock(
        topic="Interim Operating Covenants",
        keywords=["interim covenants", "ordinary course", "pre-closing operations", "negative covenant"],
        conclusion_template="The seller {complied/did not comply} with interim operating covenants prior to closing.",
        reasoning_framework=(
            "1. Review the agreement's interim operating covenants (e.g., operate in ordinary course, restrictions on capital expenditures).\n"
            "2. Assess seller's actions between signing and closing for compliance.\n"
            "3. Consider exceptions for emergencies or buyer consent.\n"
            "4. Analyze impact of any breaches on closing conditions or termination rights.\n"
            "5. Document findings and communicate with counterparties."
        ),
        key_factors=[
            "Ordinary course requirement",
            "Exceptions and consents",
            "Materiality of breach",
            "Impact on closing",
            "Remedies"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law"
        ],
        burden_holder="Buyer (to prove material breach)",
        adversary_position="Seller may argue actions were in ordinary course or consented",
        counter_arguments=[
            "No material breach",
            "Buyer waived compliance"
        ],
        resolution_strategy="Negotiate clear covenants and document consents.",
        entity_scope="All M&A transactions",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Akorn, Inc. v. Fresenius Kabi AG, 2018 WL 4719347 (Del. Ch. 2018)"
    ),
    DoctrineBlock(
        topic="Disclosure Schedules and Seller Disclosure",
        keywords=["disclosure schedules", "seller disclosure", "exceptions", "reps and warranties"],
        conclusion_template="The disclosure schedules {adequately/inadequately} disclose exceptions to the representations.",
        reasoning_framework=(
            "1. Review the disclosure schedules for completeness and specificity.\n"
            "2. Compare disclosed exceptions to the representations and warranties in the agreement.\n"
            "3. Assess whether the disclosures are sufficient to preclude a claim for breach.\n"
            "4. Consider the impact of general vs specific disclosures.\n"
            "5. Document findings and communicate with counterparties."
        ),
        key_factors=[
            "Completeness of schedules",
            "Specificity of disclosures",
            "Materiality",
            "Impact on reps and warranties",
            "Buyer knowledge"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law"
        ],
        burden_holder="Seller (to provide adequate disclosure)",
        adversary_position="Buyer may argue disclosure is insufficient",
        counter_arguments=[
            "Disclosure is too general",
            "Material facts omitted"
        ],
        resolution_strategy="Prepare detailed schedules and negotiate disclosure standards.",
        entity_scope="All M&A transactions",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Prairie Capital III, L.P. v. Double E Holding Corp., 132 A.3d 35 (Del. Ch. 2015)"
    ),
    DoctrineBlock(
        topic="Fraud Carve-Outs in Indemnification",
        keywords=["fraud", "indemnity", "carve-out", "cap", "basket"],
        conclusion_template="Fraud claims are {subject/not subject} to indemnification caps and baskets.",
        reasoning_framework=(
            "1. Review the indemnification provisions for express fraud carve-outs.\n"
            "2. Analyze whether the agreement defines fraud and allocates liability accordingly.\n"
            "3. Consider the impact of Delaware law, which generally does not permit caps on fraud liability.\n"
            "4. Assess the parties' negotiation history and intent.\n"
            "5. Document findings and prepare for potential litigation."
        ),
        key_factors=[
            "Fraud definition",
            "Express carve-out",
            "Delaware law",
            "Negotiation history",
            "Remedies"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law"
        ],
        burden_holder="Claimant (to prove fraud and applicability of carve-out)",
        adversary_position="Indemnitor may argue claim is not for fraud",
        counter_arguments=[
            "No fraud occurred",
            "Fraud not defined in agreement"
        ],
        resolution_strategy="Negotiate clear fraud carve-outs and definitions.",
        entity_scope="All M&A transactions",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Abry Partners V, L.P. v. F&W Acquisition LLC, 891 A.2d 1032 (Del. Ch. 2006)"
    ),
    DoctrineBlock(
        topic="Specific Performance as a Remedy",
        keywords=["specific performance", "remedy", "equitable relief", "irreparable harm"],
        conclusion_template="Specific performance is {available/not available} as a remedy for breach of the agreement.",
        reasoning_framework=(
            "1. Review the agreement for provisions permitting or limiting specific performance.\n"
            "2. Analyze whether monetary damages are inadequate and irreparable harm would result from breach.\n"
            "3. Consider whether the party seeking specific performance has satisfied all conditions precedent.\n"
            "4. Evaluate the court's willingness to enforce specific performance in the context of M&A.\n"
            "5. Document findings and prepare for potential litigation."
        ),
        key_factors=[
            "Agreement language",
            "Adequacy of damages",
            "Irreparable harm",
            "Conditions precedent",
            "Court's equitable discretion"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law"
        ],
        burden_holder="Party seeking specific performance",
        adversary_position="Counterparty may argue damages are adequate",
        counter_arguments=[
            "Damages are adequate",
            "Conditions precedent not satisfied"
        ],
        resolution_strategy="Negotiate express specific performance provisions.",
        entity_scope="All M&A transactions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IBP, Inc. v. Tyson Foods, Inc., 789 A.2d 14 (Del. Ch. 2001)"
    ),
    DoctrineBlock(
        topic="Reverse Termination Fees",
        keywords=["reverse termination fee", "break fee", "financing failure", "deal certainty"],
        conclusion_template="The buyer is {liable/not liable} for the reverse termination fee under the agreement.",
        reasoning_framework=(
            "1. Review the agreement for reverse termination fee provisions and triggers (e.g., financing failure, regulatory block).\n"
            "2. Analyze the circumstances leading to termination.\n"
            "3. Assess whether the buyer used required efforts to close the transaction.\n"
            "4. Consider the enforceability of the fee under Delaware law.\n"
            "5. Document findings and prepare for enforcement or negotiation."
        ),
        key_factors=[
            "Fee triggers",
            "Efforts standard",
            "Causation",
            "Enforceability",
            "Negotiation history"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law"
        ],
        burden_holder="Seller (to prove trigger event and enforceability)",
        adversary_position="Buyer may argue trigger not met or fee is penalty",
        counter_arguments=[
            "Fee is unenforceable penalty",
            "Buyer satisfied efforts standard"
        ],
        resolution_strategy="Negotiate clear triggers and enforceable fee provisions.",
        entity_scope="Large M&A transactions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Hexion Specialty Chemicals, Inc. v. Huntsman Corp., 965 A.2d 715 (Del. Ch. 2008)"
    ),
    DoctrineBlock(
        topic="Drag-Along and Tag-Along Rights",
        keywords=["drag-along", "tag-along", "minority protection", "stockholder agreement"],
        conclusion_template="The transaction {may/may not} be compelled under drag-along or tag-along provisions.",
        reasoning_framework=(
            "1. Review the stockholder or LLC agreement for drag-along and tag-along rights.\n"
            "2. Analyze the scope, triggers, and notice requirements for each right.\n"
            "3. Assess whether the transaction meets the conditions for exercise.\n"
            "4. Consider the impact on minority holders and required consents.\n"
            "5. Document findings and communicate with stakeholders."
        ),
        key_factors=[
            "Agreement language",
            "Triggering events",
            "Notice requirements",
            "Minority protection",
            "Consents"
        ],
        primary_authority=[
            "Stockholder/LLC agreement",
            "Delaware case law"
        ],
        burden_holder="Majority (drag-along) or minority (tag-along) holder",
        adversary_position="Counterparty may challenge exercise or process",
        counter_arguments=[
            "Conditions not satisfied",
            "Improper notice"
        ],
        resolution_strategy="Draft clear provisions and follow process strictly.",
        entity_scope="Private companies",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="In re Appraisal of Dell Inc., 2016 WL 3186538 (Del. Ch. 2016)"
    ),
    DoctrineBlock(
        topic="Disclosure Obligations Under Rule 10b-5",
        keywords=["Rule 10b-5", "disclosure", "material misstatement", "securities fraud"],
        conclusion_template="The disclosure is {adequate/inadequate} under Rule 10b-5.",
        reasoning_framework=(
            "1. Determine whether the disclosure omits or misstates a material fact.\n"
            "2. Analyze whether the fact would alter the total mix of information available to investors.\n"
            "3. Assess scienter and reliance elements for liability.\n"
            "4. Consider timing and context of the disclosure.\n"
            "5. Review recent SEC enforcement and case law."
        ),
        key_factors=[
            "Materiality",
            "Omission or misstatement",
            "Scienter",
            "Reliance",
            "SEC guidance"
        ],
        primary_authority=[
            "Securities Exchange Act of 1934 §10(b)",
            "SEC Rule 10b-5",
            "Supreme Court precedent"
        ],
        burden_holder="Plaintiff (to prove elements of claim)",
        adversary_position="Defendant may argue immateriality or lack of scienter",
        counter_arguments=[
            "Fact was immaterial",
            "No scienter or reliance"
        ],
        resolution_strategy="Ensure robust, timely disclosure and compliance with SEC rules.",
        entity_scope="Public companies",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Basic Inc. v. Levinson, 485 U.S. 224 (1988)"
    ),
    DoctrineBlock(
        topic="No-Shop and Go-Shop Provisions",
        keywords=["no-shop", "go-shop", "deal protection", "fiduciary out"],
        conclusion_template="The seller {may/may not} engage with other bidders under the no-shop/go-shop provisions.",
        reasoning_framework=(
            "1. Review the agreement for no-shop or go-shop provisions and exceptions (fiduciary out).\n"
            "2. Analyze the duration and scope of restrictions.\n"
            "3. Consider the board's fiduciary duties under Delaware law.\n"
            "4. Assess the process for engaging with competing bidders.\n"
            "5. Document findings and communicate with stakeholders."
        ),
        key_factors=[
            "Provision scope",
            "Fiduciary out",
            "Duration",
            "Process for exceptions",
            "Board duties"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law"
        ],
        burden_holder="Seller (to comply with restrictions)",
        adversary_position="Buyer may allege breach of exclusivity",
        counter_arguments=[
            "Fiduciary out applies",
            "Provision expired"
        ],
        resolution_strategy="Draft clear provisions and comply with fiduciary duties.",
        entity_scope="Public company M&A",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Lyondell Chemical Co. v. Ryan, 970 A.2d 235 (Del. 2009)"
    ),
    DoctrineBlock(
        topic="Representation and Warranty Survival Periods",
        keywords=["survival period", "reps and warranties", "indemnity", "statute of limitations"],
        conclusion_template="The claim is {timely/untimely} based on the survival period for representations.",
        reasoning_framework=(
            "1. Review the agreement for express survival periods for representations and warranties.\n"
            "2. Compare the timing of the claim to the survival period.\n"
            "3. Consider exceptions (e.g., fraud, fundamental reps) with longer or unlimited survival.\n"
            "4. Analyze the interplay with applicable statutes of limitations.\n"
            "5. Document findings and communicate with counterparties."
        ),
        key_factors=[
            "Survival period length",
            "Type of representation",
            "Claim timing",
            "Exceptions",
            "Statute of limitations"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law"
        ],
        burden_holder="Claimant (to prove claim is timely)",
        adversary_position="Indemnitor may argue claim is out of time",
        counter_arguments=[
            "Claim is for fraud (unlimited survival)",
            "Survival period tolled"
        ],
        resolution_strategy="Negotiate clear survival periods and track claims.",
        entity_scope="All M&A transactions",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="GRT, Inc. v. Marathon GTF Technology, Ltd., 2011 WL 2682898 (Del. Ch. 2011)"
    ),
    DoctrineBlock(
        topic="Escrow Arrangements in M&A",
        keywords=["escrow", "holdback", "indemnity", "purchase price"],
        conclusion_template="Escrow funds are {available/not available} to satisfy the indemnity claim.",
        reasoning_framework=(
            "1. Review escrow agreement for terms governing release of funds.\n"
            "2. Analyze the nature and timing of the indemnity claim.\n"
            "3. Assess whether claim was made within escrow period and in accordance with procedures.\n"
            "4. Consider exceptions or limitations on use of escrow.\n"
            "5. Document findings and coordinate with escrow agent."
        ),
        key_factors=[
            "Escrow period",
            "Claim procedure",
            "Exceptions",
            "Release triggers",
            "Coordination with agent"
        ],
        primary_authority=[
            "Escrow agreement",
            "Transaction agreement",
            "Delaware case law"
        ],
        burden_holder="Claimant (to comply with escrow procedures)",
        adversary_position="Counterparty may dispute claim or timing",
        counter_arguments=[
            "Claim made after escrow expired",
            "Escrow not available for type of claim"
        ],
        resolution_strategy="Negotiate clear escrow terms and track claims.",
        entity_scope="All M&A transactions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Cigna Health & Life Ins. Co. v. Audax Health Solutions, Inc., 107 A.3d 1082 (Del. Ch. 2014)"
    ),
    DoctrineBlock(
        topic="Interim Dividends and Pre-Closing Distributions",
        keywords=["dividends", "pre-closing distributions", "leakage", "purchase price adjustment"],
        conclusion_template="Pre-closing distributions are {permitted/not permitted} under the agreement.",
        reasoning_framework=(
            "1. Review the agreement for restrictions on dividends and distributions prior to closing.\n"
            "2. Analyze the impact of any distributions on purchase price and working capital.\n"
            "3. Consider exceptions for ordinary course distributions.\n"
            "4. Document findings and communicate with counterparties."
        ),
        key_factors=[
            "Agreement restrictions",
            "Materiality",
            "Purchase price adjustment",
            "Ordinary course exception",
            "Disclosure"
        ],
        primary_authority=[
            "Transaction agreement",
            "Delaware case law"
        ],
        burden_holder="Seller (to comply with restrictions)",
        adversary_position="Buyer may claim breach or seek adjustment",
        counter_arguments=[
            "Distribution permitted by agreement",
            "Buyer consented"
        ],
        resolution_strategy="Negotiate clear restrictions and monitor compliance.",
        entity_scope="All M&A transactions",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Akorn, Inc. v. Fresenius Kabi AG, 2018 WL 4719347 (Del. Ch. 2018)"
    ),
    DoctrineBlock(
        topic="409A and Equity Compensation in M&A",
        keywords=["409A", "equity compensation", "deferred compensation", "change in control"],
        conclusion_template="Section 409A {is/is not} triggered by the treatment of equity compensation in the transaction.",
        reasoning_framework=(
            "1. Identify whether any deferred compensation arrangements are subject to IRC §409A.\n"
            "2. Review the treatment of equity awards (vesting, acceleration, cash-out) in the transaction.\n"
            "3. Analyze whether the transaction constitutes a change in control for 409A purposes.\n"
            "4. Assess compliance with 409A distribution and acceleration rules.\n"
            "5. Consider potential penalties and mitigation strategies."
        ),
        key_factors=[
            "Deferred compensation arrangements",
            "Change in control",
            "Acceleration of vesting",
            "409A compliance",
            "Mitigation"
        ],
        primary_authority=[
            "IRC §409A",
            "Treasury Regulations",
            "IRS guidance"
        ],
        burden_holder="Company (to ensure compliance)",
        adversary_position="Employee may seek gross-up or alternative arrangements",
        counter_arguments=[
            "No deferred compensation subject to 409A",
            "No change in control"
        ],
        resolution_strategy="Conduct 409A analysis and structure awards accordingly.",
        entity_scope="C corporations, equity plans",
        confidence=0.88,
        confidence_zone="Moderate-High",
        controlling_precedent="IRC §409A and related regulations"
    ),
    DoctrineBlock(
        topic="Section 363 Bankruptcy Sales",
        keywords=["section 363", "bankruptcy", "asset sale", "free and clear", "stalking horse"],
        conclusion_template="The sale is {approved/not approved} under Section 363 of the Bankruptcy Code.",
        reasoning_framework=(
            "1. Confirm that the sale is conducted under Section 363 of the Bankruptcy Code.\n"
            "2. Review notice and bidding procedures, including stalking horse protections.\n"
            "3. Analyze whether the sale is free and clear of liens and claims.\n"
            "4. Consider objections from creditors or other parties in interest.\n"
            "5. Review court approval process and sale order."
        ),
        key_factors=[
            "Sale procedures",
            "Notice and opportunity to object",
            "Free and clear language",
            "Stalking horse protections",
            "Court approval"
        ],
        primary_authority=[
            "11 U.S.C. §363",
            "Bankruptcy court orders"
        ],
        burden_holder="Debtor (to comply with procedures)",
        adversary_position="Creditors may object to sale terms",
        counter_arguments=[
            "Procedures not followed",
            "Sale not in best interests of estate"
        ],
        resolution_strategy="Strict compliance with court procedures and robust notice.",
        entity_scope="Bankruptcy asset sales",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="In re Chrysler LLC, 576 F.3d 108 (2d Cir. 2009)"
    ),
    DoctrineBlock(
        topic="Shareholder Litigation and Injunctions",
        keywords=["shareholder litigation", "injunction", "deal challenge", "fiduciary duty"],
        conclusion_template="An injunction {is/is not} warranted to enjoin the transaction.",
        reasoning_framework=(
            "1. Review the grounds for shareholder litigation (breach of fiduciary duty, disclosure violations, etc.).\n"
            "2. Analyze the likelihood of success on the merits and irreparable harm.\n"
            "3. Consider the balance of equities and public interest.\n"
            "4. Evaluate the timing and impact of injunctive relief on the transaction.\n"
            "5. Review recent Delaware Chancery Court practice."
        ),
        key_factors=[
            "Likelihood of success",
            "Irreparable harm",
            "Balance of equities",
            "Timing",
            "Disclosure"
        ],
        primary_authority=[
            "Delaware case law",
            "Chancery Court rules"
        ],
        burden_holder="Plaintiff (to meet injunction standard)",
        adversary_position="Company may argue no harm or adequate remedy at law",
        counter_arguments=[
            "No irreparable harm",
            "Disclosure is adequate"
        ],
        resolution_strategy="Prepare robust disclosure and defend process.",
        entity_scope="Public company M&A",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Revlon, Inc. v. MacAndrews & Forbes Holdings, Inc., 506 A.2d 173 (Del. 1986)"
    ),
    DoctrineBlock(
        topic="Fiduciary Duties in Sale of Control",
        keywords=["fiduciary duty", "sale of control", "Revlon duties", "board process"],
        conclusion_template="The board {satisfied/did not satisfy} its fiduciary duties in the sale process.",
        reasoning_framework=(
            "1. Review the board's process for considering and approving the sale of control.\n"
            "2. Analyze whether the board acted on an informed basis and sought to maximize value for shareholders.\n"
            "3. Consider the adequacy of disclosure to shareholders.\n"
            "4. Evaluate conflicts of interest and use of independent advisors.\n"
            "5. Review recent Delaware Supreme Court guidance."
        ),
        key_factors=[
            "Board process",
            "Value maximization",
            "Disclosure",
            "Conflicts of interest",
            "Use of advisors"
        ],
        primary_authority=[
            "Delaware case law",
            "DGCL"
        ],
        burden_holder="Board (to demonstrate process and value maximization)",
        adversary_position="Shareholders may allege breach or conflicts",
        counter_arguments=[
            "Process was flawed",
            "Conflicts not addressed"
        ],
        resolution_strategy="Follow robust process and document decisions.",
        entity_scope="Public companies",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Revlon, Inc. v. MacAndrews & Forbes Holdings, Inc., 506 A.2d 173 (Del. 1986)"
    ),
    DoctrineBlock(
        topic="Interlocking Directorates and Clayton Act Section 8",
        keywords=["interlocking directorates", "Clayton Act", "Section 8", "antitrust"],
        conclusion_template="The proposed board composition {violates/does not violate} Section 8 of the Clayton Act.",
        reasoning_framework=(
            "1. Review the composition of the boards of directors of the merging companies.\n"
            "2. Analyze whether any individual will serve as a director or officer of competing corporations.\n"
            "3. Consider the revenue thresholds and exemptions under Section 8.\n"
            "4. Assess the competitive relationship between the companies post-transaction.\n"
            "5. Document findings and, if necessary, restructure board composition."
        ),
        key_factors=[
            "Board composition",
            "Competitive relationship",
            "Revenue thresholds",
            "Exemptions",
            "Remediation"
        ],
        primary_authority=[
            "Clayton Act §8, 15 U.S.C. §19",
            "FTC guidance"
        ],
        burden_holder="Companies (to ensure compliance)",
        adversary_position="FTC may challenge interlocks",
        counter_arguments=[
            "No competitive overlap",
            "Exemption applies"
        ],
        resolution_strategy="Conduct antitrust review and restructure as needed.",
        entity_scope="Public companies",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Clayton Act §8"
    ),
    DoctrineBlock(
        topic="Section 16(b) Short-Swing Profits in M&A",
        keywords=["Section 16(b)", "short-swing profits", "insider trading", "public company"],
        conclusion_template="Section 16(b) {applies/does not apply} to the transaction and profits are {recoverable/not recoverable}.",
        reasoning_framework=(
            "1. Identify whether the transaction involves Section 16 insiders (officers, directors, 10% holders).\n"
            "2. Analyze whether any purchase and sale (or sale and purchase) of equity securities occurred within a six-month period.\n"
            "3. Assess whether profits are realized and subject to disgorgement.\n"
            "4. Consider exemptions for mergers and tender offers.\n"
            "5. Document findings and, if necessary, seek board approval or exemption."
        ),
        key_factors=[
            "Insider status",
            "Timing of transactions",
            "Profit realization",
            "Exemptions",
            "Board approval"
        ],
        primary_authority=[
            "Securities Exchange Act of 1934 §16(b)",
            "SEC rules"
        ],
        burden_holder="Issuer or shareholder (to recover profits)",
        adversary_position="Insider may claim exemption",
        counter_arguments=[
            "Exemption applies",
            "No profit realized"
        ],
        resolution_strategy="Monitor insider transactions and seek exemptions as needed.",
        entity_scope="Public companies",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Kern County Land Co. v. Occidental Petroleum Corp., 411 U.S. 582 (1973)"
    ),
    DoctrineBlock(
        topic="Dissenters' Rights in Non-Delaware Jurisdictions",
        keywords=["dissenters' rights", "appraisal", "non-Delaware", "fair value"],
        conclusion_template="The dissenting shareholder {is/is not} entitled to appraisal rights under applicable state law.",
        reasoning_framework=(
            "1. Identify the governing state statute and whether the transaction triggers dissenters' rights.\n"
            "2. Review the process for perfecting rights (notice, demand, no vote in favor).\n"
            "3. Analyze the standard for 'fair value' under state law.\n"
            "4. Consider recent state court decisions.\n"
            "5. Document findings and communicate with shareholders."
        ),
        key_factors=[
            "State statute",
            "Triggering transaction",
            "Process compliance",
            "Fair value standard",
            "Recent precedent"
        ],
        primary_authority=[
            "State corporate statutes",
            "State case law"
        ],
        burden_holder="Dissenting shareholder",
        adversary_position="Company may argue rights not perfected",
        counter_arguments=[
            "Process not followed",
            "No triggering transaction"
        ],
        resolution_strategy="Strict compliance with statute and notice requirements.",
        entity_scope="Non-Delaware corporations",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Relevant state law"
    ),
    DoctrineBlock(
        topic="Successor Employer Liability under WARN Act",
        keywords=["WARN Act", "successor employer", "plant closing", "mass layoff"],
        conclusion_template="The buyer {is/is not} liable under the WARN Act for post-closing layoffs.",
        reasoning_framework=(
            "1. Determine whether the buyer is a 'successor employer' under the WARN Act.\n"
            "2. Analyze whether a plant closing or mass layoff occurred post-closing.\n"
            "3. Assess whether proper notice was given to employees.\n"
            "4. Consider exceptions (e.g., faltering company, unforeseeable business circumstances).\n"
            "5. Review recent DOL guidance and case law."
        ),
        key_factors=[
            "Successor employer status",
            "Layoff or closing",
            "Notice given",
            "Exceptions",
            "Remedies"
        ],
        primary_authority=[
            "WARN Act, 29 U.S.C. §2101 et seq.",
            "DOL guidance"
        ],
        burden_holder="Buyer (to provide notice if liable)",
        adversary_position="Employees may claim lack of notice",
        counter_arguments=[
            "No successor liability",
            "Exception applies"
        ],
        resolution_strategy="Conduct WARN analysis and provide notice if required.",
        entity_scope="Asset purchases, plant closings",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="Criswell v. Delta Air Lines, Inc., 868 F.2d 1093 (9th Cir. 1989)"
    ),
    DoctrineBlock(
        topic="Environmental Liabilities in M&A",
        keywords=["environmental liability", "CERCLA", "due diligence", "indemnity"],
        conclusion_template="The buyer {assumes/does not assume} environmental liabilities based on agreement and applicable law.",
        reasoning_framework=(
            "1. Conduct environmental due diligence to identify potential liabilities.\n"
            "2. Review the agreement for allocation of environmental liabilities and indemnities.\n"
            "3. Analyze the applicability of CERCLA and state statutes imposing successor liability.\n"
            "4. Consider the impact of disclosure and known/unknown conditions.\n"
            "5. Document findings and negotiate risk allocation."
        ),
        key_factors=[
            "Due diligence findings",
            "Agreement allocation",
            "CERCLA applicability",
            "Disclosure",
            "Indemnity"
        ],
        primary_authority=[
            "CERCLA, 42 U.S.C. §9601 et seq.",
            "State environmental statutes"
        ],
        burden_holder="Buyer (to conduct diligence and negotiate allocation)",
        adversary_position="Seller may seek to limit liability",
        counter_arguments=[
            "Liability excluded by agreement",
            "No successor liability"
        ],
        resolution_strategy="Conduct thorough diligence and negotiate indemnities.",
        entity_scope="All M&A transactions",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="United States v. Bestfoods, 524 U.S. 51 (1998)"
    ),
    DoctrineBlock(
        topic="Foreign Corrupt Practices Act (FCPA) Diligence",
        keywords=["FCPA", "anti-corruption", "diligence", "successor liability"],
        conclusion_template="The buyer {is/is not} exposed to FCPA liability based on diligence findings.",
        reasoning_framework=(
            "1. Conduct FCPA and anti-corruption diligence on the target's operations.\n"
            "2. Review the agreement for representations, warranties, and indemnities relating to FCPA compliance.\n"
            "3. Analyze the risk of successor liability for pre-closing violations.\n"
            "4. Consider post-closing remediation and disclosure obligations.\n"
            "5. Document findings and coordinate with counsel."
        ),
        key_factors=[
            "Diligence findings",
            "Agreement protections",
            "Successor liability",
            "Disclosure",
            "Remediation"
        ],
        primary_authority=[
            "FCPA, 15 U.S.C. §§78dd-1 et seq.",
            "DOJ/SEC guidance"
        ],
        burden_holder="Buyer (to conduct diligence and negotiate protections)",
        adversary_position="Seller may limit reps or indemnity",
        counter_arguments=[
            "No pre-closing violations",
            "Liability excluded by agreement"
        ],
        resolution_strategy="Conduct robust diligence and negotiate FCPA-specific protections.",
        entity_scope="Cross-border M&A",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FCPA and DOJ/SEC Resource Guide"
    ),
    DoctrineBlock(
        topic="Data Privacy and Cybersecurity in M&A",
        keywords=["data privacy", "cybersecurity", "GDPR", "CCPA", "due diligence"],
        conclusion_template="The buyer {is/is not} exposed to material data privacy or cybersecurity risk.",
        reasoning_framework=(
            "1. Conduct data privacy and cybersecurity diligence on the target's operations and compliance.\n"
            "2. Review the agreement for representations, warranties, and indemnities relating to privacy and security.\n"
            "3. Analyze the applicability of GDPR, CCPA, and other privacy laws.\n"
            "4. Consider the impact of prior breaches or ongoing investigations.\n"
            "5. Document findings and negotiate risk allocation."
        ),
        key_factors=[
            "Diligence findings",
            "Agreement protections",
            "Regulatory compliance",
            "Prior breaches",
            "Indemnity"
        ],
        primary_authority=[
            "GDPR",
            "CCPA",
            "FTC guidance"
        ],
        burden_holder="Buyer (to conduct diligence and negotiate protections)",
        adversary_position="Seller may limit reps or indemnity",
        counter_arguments=[
            "No material breaches",
            "Compliance representations adequate"
        ],
        resolution_strategy="Conduct robust diligence and negotiate privacy-specific protections.",
        entity_scope="All M&A transactions",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="GDPR, CCPA, FTC enforcement actions"
    ),
    DoctrineBlock(
        topic="Anti-Trust Gun Jumping and Pre-Closing Conduct",
        keywords=["antitrust", "gun jumping", "pre-closing", "HSR Act", "integration planning"],
        conclusion_template="The parties {have/have not} engaged in impermissible gun jumping prior to closing.",
        reasoning_framework=(
            "1. Review pre-closing conduct for coordination of competitive activities.\n"
            "2. Analyze whether the parties have exchanged competitively sensitive information or exercised control over each other's business.\n"
            "3. Consider the requirements of the HSR Act and Section 1 of the Sherman Act.\n"
            "4. Assess the use of clean teams and integration planning protocols.\n"
            "5. Document findings and, if necessary, remediate conduct."
        ),
        key_factors=[
            "Pre-closing conduct",
            "Information exchange",
            "Control over business",
            "Clean team protocols",
            "HSR compliance"
        ],
        primary_authority=[
            "HSR Act",
            "Sherman Act §1",
            "FTC/DOJ guidance"
        ],
        burden_holder="Both parties (to avoid gun jumping)",
        adversary_position="FTC/DOJ may investigate or penalize",
        counter_arguments=[
            "Conduct was permissible integration planning",
            "No control exercised"
        ],
        resolution_strategy="Implement protocols and train deal teams.",
        entity_scope="All M&A transactions",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="United States v. Computer Associates Int'l, Inc., 2002 WL 31961456 (D.D.C. 2002)"
    ),
    DoctrineBlock(
        topic="Minority Shareholder Protections in M&A",
        keywords=["minority shareholder", "protection", "fiduciary duty", "entire fairness"],
        conclusion_template="The transaction {satisfies/does not satisfy} entire fairness to minority shareholders.",
        reasoning_framework=(
            "1. Review the process for approval of the transaction, including use of special committees and majority-of-the-minority votes.\n"
            "2. Analyze the fairness of the price and process.\n"
            "3. Consider disclosure to minority shareholders.\n"
            "4. Evaluate recent Delaware case law on entire fairness review.\n"
            "5. Document findings and, if necessary, seek judicial review."
        ),
        key_factors=[
            "Process fairness",
            "Price fairness",
            "Special committee",
            "Majority-of-the-minority approval",
            "Disclosure"
        ],
        primary_authority=[
            "Delaware case law",
            "DGCL"
        ],
        burden_holder="Board/controlling shareholder",
        adversary_position="Minority may allege unfairness",
        counter_arguments=[
            "Process was robust",
            "Price was fair"
        ],
        resolution_strategy="Follow best practices and document process.",
        entity_scope="Public and private companies",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Kahn v. M&F Worldwide Corp., 88 A.3d 635 (Del. 2014)"
    ),
    DoctrineBlock(
        topic="Tax Gross-Ups and Purchase Price Adjustments",
        keywords=["tax gross-up", "purchase price adjustment", "tax indemnity", "change in law"],
        conclusion_template="A tax gross-up {is/is not} required under the agreement.",
        reasoning_framework=(
            "1. Review the agreement for tax gross-up provisions and triggers (e.g., change in law, withholding tax).\n"
            "2. Analyze the nature of the tax and whether it is indemnified or adjusted in purchase price.\n"
            "3. Assess the calculation and payment mechanics.\n"
            "4. Document findings and communicate with counterparties."
        ),
        key_factors=[
            "Gross-up triggers",
            "Type of tax",
            "Indemnity",
            "Calculation",
            "Payment mechanics"
        ],
        primary_authority=[
            "Transaction agreement",
            "IRC"
        ],
        burden_holder="Indemnified party",
        adversary_position="Counterparty may dispute trigger or calculation",
        counter_arguments=[
            "Tax is not indemnified",
            "No gross-up required"
        ],
        resolution_strategy="Negotiate clear gross-up and adjustment provisions.",
        entity_scope="Cross-border M&A",
        confidence=0.89,
        confidence_zone="Moderate-High",
        controlling_precedent="IRC and market practice"
    ),
    DoctrineBlock(
        topic="Section 338(h)(10) Elections",
        keywords=["338(h)(10)", "deemed asset sale", "tax election", "step-up in basis"],
        conclusion_template="A Section 338(h)(10) election {is/is not} available and {will/will not} result in a step-up in basis.",
        reasoning_framework=(
            "1. Determine whether the transaction is eligible for a Section 338(h)(10) election (qualified stock purchase of S corp or subsidiary).\n"
            "2. Analyze the tax consequences for buyer and seller.\n"
            "3. Review the agreement for allocation of tax benefits and burdens.\n"
            "4. Consider timing and filing requirements.\n"
            "5. Document findings and coordinate with tax advisors."
        ),
        key_factors=[
            "Eligibility",
            "Tax consequences",
            "Agreement allocation",
            "Filing requirements",
            "Timing"
        ],
        primary_authority=[
            "IRC §338(h)(10)",
            "Treasury Regulations"
        ],
        burden_holder="Buyer and seller (to elect and file)",
        adversary_position="Counterparty may dispute allocation",
        counter_arguments=[
            "Not a qualified stock purchase",
            "Election not timely"
        ],
        resolution_strategy="Coordinate with tax advisors and file timely elections.",
        entity_scope="S corps, subsidiaries",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IRC §338(h)(10) and regulations"
    ),
    DoctrineBlock(
        topic="Section 1060 Asset Allocation",
        keywords=["section 1060", "asset allocation", "purchase price", "Form 8594"],
        conclusion_template="The purchase price allocation {complies/does not comply} with Section 1060 and Form 8594 requirements.",
        reasoning_framework=(
            "