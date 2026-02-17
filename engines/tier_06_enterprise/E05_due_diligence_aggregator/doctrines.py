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
        topic="Due Diligence Checklist Management",
        keywords=["checklist", "organization", "workflow", "risk identification", "scope definition"],
        conclusion_template="The due diligence checklist is comprehensive, tailored to the transaction, and addresses all relevant risk categories.",
        reasoning_framework=(
            "1. Identify the scope of the transaction and relevant risk domains.\n"
            "2. Review historical checklists and adapt for current context.\n"
            "3. Engage stakeholders to ensure completeness.\n"
            "4. Prioritize items based on materiality and risk profile.\n"
            "5. Ensure checklist items are actionable and assignable.\n"
            "6. Regularly update checklist as new risks emerge.\n"
            "7. Validate checklist against regulatory and legal requirements.\n"
            "8. Use feedback loops to improve checklist quality.\n"
            "9. Document rationale for inclusion/exclusion of items.\n"
            "10. Integrate checklist into project management tools.\n"
            "11. Monitor completion status and escalate overdue items.\n"
            "12. Cross-reference checklist with data room contents.\n"
            "13. Ensure checklist aligns with transaction timeline.\n"
            "14. Maintain version control and audit trail.\n"
            "15. Conduct periodic reviews with legal and compliance teams.\n"
            "16. Address gaps identified during diligence process.\n"
            "17. Benchmark checklist against industry standards.\n"
            "18. Incorporate lessons learned from prior transactions.\n"
            "19. Ensure checklist is accessible to all relevant parties.\n"
            "20. Use checklist to drive due diligence reporting.\n"
            "21. Validate checklist coverage with external advisors.\n"
            "22. Ensure checklist supports red flag identification.\n"
            "23. Link checklist items to underlying documents.\n"
            "24. Assign responsibility for checklist maintenance.\n"
            "25. Review checklist for redundancy and overlap.\n"
            "26. Ensure checklist supports regulatory filings.\n"
            "27. Align checklist with deal structure and objectives.\n"
            "28. Use checklist to facilitate closing readiness.\n"
            "29. Ensure checklist supports post-closing integration.\n"
            "30. Document checklist evolution for future reference."
        ),
        key_factors=[
            "Transaction scope",
            "Stakeholder input",
            "Regulatory requirements",
            "Materiality thresholds",
            "Industry best practices"
        ],
        primary_authority=[
            "ABA Model Asset Purchase Agreement",
            "SEC Guidance on Due Diligence",
            "ACQUIS Handbook"
        ],
        burden_holder="Buyer diligence team",
        adversary_position="Seller may resist broad scope or disclosure",
        counter_arguments=[
            "Checklist is overly burdensome",
            "Checklist includes irrelevant items",
            "Checklist duplicates existing processes"
        ],
        resolution_strategy="Negotiate scope, prioritize material items, document rationale for exclusions.",
        entity_scope="Buyer, Seller, Advisors",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="In re: M&A Transaction Best Practices, ABA 2018"
    ),
    DoctrineBlock(
        topic="A&D Transaction Due Diligence",
        keywords=["acquisition", "divestiture", "asset evaluation", "risk assessment", "deal structuring"],
        conclusion_template="The due diligence process for A&D transactions adequately identifies and mitigates risks associated with asset transfer.",
        reasoning_framework=(
            "1. Define transaction objectives and asset scope.\n"
            "2. Assess asset quality, ownership, and encumbrances.\n"
            "3. Review historical performance and operational data.\n"
            "4. Evaluate legal, regulatory, and environmental risks.\n"
            "5. Analyze financial statements and cash flow projections.\n"
            "6. Identify key contracts and obligations.\n"
            "7. Assess reserve reports and technical data.\n"
            "8. Review title and ownership documentation.\n"
            "9. Evaluate compliance with applicable laws.\n"
            "10. Assess litigation and contingent liabilities.\n"
            "11. Identify material contracts and change of control provisions.\n"
            "12. Review tax implications and structuring options.\n"
            "13. Analyze integration risks and post-closing obligations.\n"
            "14. Engage subject matter experts as needed.\n"
            "15. Document findings and escalate red flags.\n"
            "16. Negotiate representations, warranties, and indemnities.\n"
            "17. Validate asset valuation and purchase price.\n"
            "18. Coordinate with data room management.\n"
            "19. Ensure diligence aligns with deal timeline.\n"
            "20. Prepare diligence report for investment committee."
        ),
        key_factors=[
            "Asset quality",
            "Legal and regulatory compliance",
            "Financial performance",
            "Operational risks",
            "Title and ownership"
        ],
        primary_authority=[
            "ABA Model Asset Purchase Agreement",
            "SEC Regulation S-K",
            "A&D Transaction Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may limit access to information or dispute asset quality",
        counter_arguments=[
            "Buyer requests excessive information",
            "Seller asserts asset quality is sufficient",
            "Seller disputes risk assessment"
        ],
        resolution_strategy="Negotiate access, use third-party verification, document risk mitigation.",
        entity_scope="Buyer, Seller, Advisors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Re: Asset Purchase Diligence, ABA 2019"
    ),
    DoctrineBlock(
        topic="Title Due Diligence",
        keywords=["title", "ownership", "encumbrances", "chain of title", "defects"],
        conclusion_template="Title due diligence confirms valid ownership, absence of material encumbrances, and clear chain of title.",
        reasoning_framework=(
            "1. Obtain and review title documents for all assets.\n"
            "2. Conduct title search through public records.\n"
            "3. Identify and analyze liens, mortgages, and encumbrances.\n"
            "4. Verify chain of title and historical transfers.\n"
            "5. Assess risks of title defects and adverse claims.\n"
            "6. Engage title counsel or experts as needed.\n"
            "7. Review title insurance policies and coverage.\n"
            "8. Evaluate impact of easements and rights of way.\n"
            "9. Confirm compliance with recording statutes.\n"
            "10. Document findings and escalate material defects.\n"
            "11. Negotiate remediation or indemnity for defects.\n"
            "12. Ensure title is transferable under deal structure.\n"
            "13. Validate title status against asset list.\n"
            "14. Review title opinions and certifications.\n"
            "15. Incorporate title findings into diligence report.\n"
            "16. Coordinate with closing and escrow agents.\n"
            "17. Address title issues in representations and warranties.\n"
            "18. Monitor post-closing title updates.\n"
            "19. Ensure title diligence aligns with regulatory requirements.\n"
            "20. Maintain title documentation for audit trail."
        ),
        key_factors=[
            "Chain of title",
            "Encumbrances",
            "Title defects",
            "Transferability",
            "Title insurance"
        ],
        primary_authority=[
            "State Recording Statutes",
            "Title Insurance Guidelines",
            "ABA Title Opinion Standards"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute title defects or refuse remediation",
        counter_arguments=[
            "Title defects are immaterial",
            "Title insurance provides sufficient coverage",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, obtain title insurance, remediate defects.",
        entity_scope="Buyer, Seller, Title Counsel",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Title Opinion Standards, ABA 2017"
    ),
    DoctrineBlock(
        topic="Environmental Due Diligence",
        keywords=["environmental", "contamination", "regulatory compliance", "permits", "liabilities"],
        conclusion_template="Environmental due diligence identifies material environmental risks, compliance gaps, and potential liabilities.",
        reasoning_framework=(
            "1. Review environmental permits and compliance history.\n"
            "2. Assess site contamination risks through Phase I/II assessments.\n"
            "3. Evaluate historical environmental incidents and remediation.\n"
            "4. Analyze regulatory enforcement actions and penalties.\n"
            "5. Review environmental management systems and policies.\n"
            "6. Identify material environmental liabilities and obligations.\n"
            "7. Engage environmental consultants as needed.\n"
            "8. Assess impact of environmental risks on asset value.\n"
            "9. Review environmental indemnities and insurance.\n"
            "10. Document findings and escalate red flags.\n"
            "11. Negotiate remediation or indemnity for environmental issues.\n"
            "12. Ensure compliance with applicable environmental laws.\n"
            "13. Incorporate environmental findings into diligence report.\n"
            "14. Coordinate with regulatory agencies as needed.\n"
            "15. Address environmental risks in deal structuring.\n"
            "16. Monitor post-closing environmental obligations.\n"
            "17. Validate environmental data against asset list.\n"
            "18. Review environmental disclosures in data room.\n"
            "19. Ensure environmental diligence aligns with transaction timeline.\n"
            "20. Maintain environmental documentation for audit trail."
        ),
        key_factors=[
            "Site contamination",
            "Regulatory compliance",
            "Environmental permits",
            "Historical incidents",
            "Environmental liabilities"
        ],
        primary_authority=[
            "CERCLA",
            "EPA Guidance",
            "State Environmental Laws"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may minimize environmental risks or dispute findings",
        counter_arguments=[
            "Environmental risks are overstated",
            "Remediation is complete",
            "Buyer is responsible post-closing"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain environmental insurance.",
        entity_scope="Buyer, Seller, Environmental Consultants",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CERCLA Due Diligence Standards"
    ),
    DoctrineBlock(
        topic="Regulatory Due Diligence",
        keywords=["regulatory", "permits", "licenses", "compliance", "approvals"],
        conclusion_template="Regulatory due diligence confirms all required permits, licenses, and approvals are valid and transferable.",
        reasoning_framework=(
            "1. Identify all regulatory permits, licenses, and approvals required for asset operation.\n"
            "2. Review validity, expiration, and transferability of permits.\n"
            "3. Assess compliance history and regulatory enforcement actions.\n"
            "4. Evaluate impact of regulatory risks on transaction.\n"
            "5. Engage regulatory counsel as needed.\n"
            "6. Review regulatory filings and disclosures.\n"
            "7. Confirm regulatory approvals for transaction structure.\n"
            "8. Document findings and escalate red flags.\n"
            "9. Negotiate remediation or indemnity for regulatory issues.\n"
            "10. Ensure compliance with applicable laws and regulations.\n"
            "11. Incorporate regulatory findings into diligence report.\n"
            "12. Coordinate with regulatory agencies as needed.\n"
            "13. Address regulatory risks in deal structuring.\n"
            "14. Monitor post-closing regulatory obligations.\n"
            "15. Validate regulatory data against asset list.\n"
            "16. Review regulatory disclosures in data room.\n"
            "17. Ensure regulatory diligence aligns with transaction timeline.\n"
            "18. Maintain regulatory documentation for audit trail."
        ),
        key_factors=[
            "Permit validity",
            "Transferability",
            "Compliance history",
            "Regulatory approvals",
            "Regulatory risks"
        ],
        primary_authority=[
            "Federal and State Regulatory Agencies",
            "SEC Regulation S-K",
            "Industry Regulatory Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute regulatory risks or refuse remediation",
        counter_arguments=[
            "Permits are valid and transferable",
            "Regulatory risks are immaterial",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain regulatory counsel opinion.",
        entity_scope="Buyer, Seller, Regulatory Counsel",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SEC Regulation S-K Guidance"
    ),
    DoctrineBlock(
        topic="Financial Due Diligence",
        keywords=["financial", "statements", "cash flow", "valuation", "accounting"],
        conclusion_template="Financial due diligence confirms accuracy of financial statements, identifies material risks, and supports asset valuation.",
        reasoning_framework=(
            "1. Obtain and review audited financial statements.\n"
            "2. Analyze historical financial performance and trends.\n"
            "3. Assess quality of earnings and cash flow.\n"
            "4. Evaluate accounting policies and practices.\n"
            "5. Identify material financial risks and liabilities.\n"
            "6. Engage financial advisors or auditors as needed.\n"
            "7. Review internal controls and audit reports.\n"
            "8. Validate asset valuation and purchase price.\n"
            "9. Document findings and escalate red flags.\n"
            "10. Negotiate remediation or indemnity for financial issues.\n"
            "11. Ensure compliance with applicable accounting standards.\n"
            "12. Incorporate financial findings into diligence report.\n"
            "13. Coordinate with finance and accounting teams.\n"
            "14. Address financial risks in deal structuring.\n"
            "15. Monitor post-closing financial obligations.\n"
            "16. Validate financial data against asset list.\n"
            "17. Review financial disclosures in data room.\n"
            "18. Ensure financial diligence aligns with transaction timeline.\n"
            "19. Maintain financial documentation for audit trail."
        ),
        key_factors=[
            "Financial statement accuracy",
            "Quality of earnings",
            "Cash flow",
            "Accounting policies",
            "Financial risks"
        ],
        primary_authority=[
            "GAAP",
            "IFRS",
            "SEC Regulation S-X"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute financial risks or refuse remediation",
        counter_arguments=[
            "Financial statements are audited",
            "Financial risks are immaterial",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain auditor opinion.",
        entity_scope="Buyer, Seller, Financial Advisors",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SEC Regulation S-X Guidance"
    ),
    DoctrineBlock(
        topic="Operational Due Diligence",
        keywords=["operations", "performance", "management", "efficiency", "risks"],
        conclusion_template="Operational due diligence assesses asset performance, management quality, and identifies operational risks.",
        reasoning_framework=(
            "1. Review operational performance data and KPIs.\n"
            "2. Assess management team quality and experience.\n"
            "3. Evaluate operational efficiency and cost structure.\n"
            "4. Identify material operational risks and liabilities.\n"
            "5. Engage operational advisors as needed.\n"
            "6. Review operational policies and procedures.\n"
            "7. Validate asset performance against industry benchmarks.\n"
            "8. Document findings and escalate red flags.\n"
            "9. Negotiate remediation or indemnity for operational issues.\n"
            "10. Ensure compliance with applicable operational standards.\n"
            "11. Incorporate operational findings into diligence report.\n"
            "12. Coordinate with operations and management teams.\n"
            "13. Address operational risks in deal structuring.\n"
            "14. Monitor post-closing operational obligations.\n"
            "15. Validate operational data against asset list.\n"
            "16. Review operational disclosures in data room.\n"
            "17. Ensure operational diligence aligns with transaction timeline.\n"
            "18. Maintain operational documentation for audit trail."
        ),
        key_factors=[
            "Operational performance",
            "Management quality",
            "Operational efficiency",
            "Operational risks",
            "Cost structure"
        ],
        primary_authority=[
            "Industry Operational Standards",
            "ISO 9001",
            "Operational Best Practices"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute operational risks or refuse remediation",
        counter_arguments=[
            "Operational performance is sufficient",
            "Operational risks are immaterial",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain operational advisor opinion.",
        entity_scope="Buyer, Seller, Operational Advisors",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001 Operational Standards"
    ),
    DoctrineBlock(
        topic="Reserve Due Diligence",
        keywords=["reserves", "resource evaluation", "technical review", "valuation", "risk assessment"],
        conclusion_template="Reserve due diligence confirms accuracy of reserve reports, identifies material technical risks, and supports asset valuation.",
        reasoning_framework=(
            "1. Obtain and review reserve reports and technical data.\n"
            "2. Assess reserve estimation methodologies and assumptions.\n"
            "3. Evaluate historical production and performance.\n"
            "4. Identify material technical risks and uncertainties.\n"
            "5. Engage reserve engineers or consultants as needed.\n"
            "6. Validate reserve estimates against industry benchmarks.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for reserve issues.\n"
            "9. Ensure compliance with applicable reserve reporting standards.\n"
            "10. Incorporate reserve findings into diligence report.\n"
            "11. Coordinate with technical and engineering teams.\n"
            "12. Address reserve risks in deal structuring.\n"
            "13. Monitor post-closing reserve obligations.\n"
            "14. Validate reserve data against asset list.\n"
            "15. Review reserve disclosures in data room.\n"
            "16. Ensure reserve diligence aligns with transaction timeline.\n"
            "17. Maintain reserve documentation for audit trail."
        ),
        key_factors=[
            "Reserve report accuracy",
            "Estimation methodologies",
            "Technical risks",
            "Historical production",
            "Asset valuation"
        ],
        primary_authority=[
            "SPE Petroleum Reserves Definitions",
            "SEC Regulation S-K",
            "Industry Reserve Reporting Standards"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute reserve estimates or refuse remediation",
        counter_arguments=[
            "Reserve reports are industry standard",
            "Technical risks are immaterial",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain reserve engineer opinion.",
        entity_scope="Buyer, Seller, Reserve Engineers",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SPE Petroleum Reserves Definitions"
    ),
    DoctrineBlock(
        topic="Contractual Due Diligence",
        keywords=["contracts", "obligations", "change of control", "material contracts", "termination"],
        conclusion_template="Contractual due diligence identifies material contracts, obligations, and risks associated with change of control.",
        reasoning_framework=(
            "1. Obtain and review all material contracts.\n"
            "2. Identify change of control provisions and termination rights.\n"
            "3. Assess contract obligations and liabilities.\n"
            "4. Evaluate impact of contract risks on transaction.\n"
            "5. Engage contract counsel as needed.\n"
            "6. Review contract disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for contract issues.\n"
            "9. Ensure compliance with applicable contract laws.\n"
            "10. Incorporate contract findings into diligence report.\n"
            "11. Coordinate with legal and contract teams.\n"
            "12. Address contract risks in deal structuring.\n"
            "13. Monitor post-closing contract obligations.\n"
            "14. Validate contract data against asset list.\n"
            "15. Ensure contractual diligence aligns with transaction timeline.\n"
            "16. Maintain contract documentation for audit trail."
        ),
        key_factors=[
            "Material contracts",
            "Change of control provisions",
            "Contract obligations",
            "Termination rights",
            "Contract risks"
        ],
        primary_authority=[
            "Contract Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Contract Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute contract risks or refuse remediation",
        counter_arguments=[
            "Contracts are standard",
            "Contract risks are immaterial",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain contract counsel opinion.",
        entity_scope="Buyer, Seller, Contract Counsel",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ABA Model Asset Purchase Agreement"
    ),
    DoctrineBlock(
        topic="Litigation Due Diligence",
        keywords=["litigation", "disputes", "claims", "contingent liabilities", "legal risks"],
        conclusion_template="Litigation due diligence identifies material disputes, claims, and contingent liabilities impacting the transaction.",
        reasoning_framework=(
            "1. Obtain and review litigation history and pending claims.\n"
            "2. Assess materiality and impact of disputes on transaction.\n"
            "3. Evaluate contingent liabilities and legal risks.\n"
            "4. Engage litigation counsel as needed.\n"
            "5. Review litigation disclosures in data room.\n"
            "6. Document findings and escalate red flags.\n"
            "7. Negotiate remediation or indemnity for litigation issues.\n"
            "8. Ensure compliance with applicable legal standards.\n"
            "9. Incorporate litigation findings into diligence report.\n"
            "10. Coordinate with legal and litigation teams.\n"
            "11. Address litigation risks in deal structuring.\n"
            "12. Monitor post-closing litigation obligations.\n"
            "13. Validate litigation data against asset list.\n"
            "14. Ensure litigation diligence aligns with transaction timeline.\n"
            "15. Maintain litigation documentation for audit trail."
        ),
        key_factors=[
            "Litigation history",
            "Pending claims",
            "Contingent liabilities",
            "Legal risks",
            "Materiality"
        ],
        primary_authority=[
            "Litigation Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Litigation Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute litigation risks or refuse remediation",
        counter_arguments=[
            "Litigation risks are immaterial",
            "Claims are resolved",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain litigation counsel opinion.",
        entity_scope="Buyer, Seller, Litigation Counsel",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ABA Model Asset Purchase Agreement"
    ),
    DoctrineBlock(
        topic="Tax Due Diligence",
        keywords=["tax", "liabilities", "structuring", "compliance", "implications"],
        conclusion_template="Tax due diligence confirms accuracy of tax liabilities, identifies material risks, and supports transaction structuring.",
        reasoning_framework=(
            "1. Obtain and review tax returns and filings.\n"
            "2. Assess accuracy and completeness of tax liabilities.\n"
            "3. Evaluate tax compliance history and risks.\n"
            "4. Analyze tax implications of transaction structure.\n"
            "5. Engage tax advisors as needed.\n"
            "6. Review tax disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for tax issues.\n"
            "9. Ensure compliance with applicable tax laws.\n"
            "10. Incorporate tax findings into diligence report.\n"
            "11. Coordinate with tax and finance teams.\n"
            "12. Address tax risks in deal structuring.\n"
            "13. Monitor post-closing tax obligations.\n"
            "14. Validate tax data against asset list.\n"
            "15. Ensure tax diligence aligns with transaction timeline.\n"
            "16. Maintain tax documentation for audit trail."
        ),
        key_factors=[
            "Tax liabilities",
            "Tax compliance",
            "Transaction structuring",
            "Tax risks",
            "Materiality"
        ],
        primary_authority=[
            "Internal Revenue Code",
            "IRS Guidance",
            "ABA Model Asset Purchase Agreement"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute tax risks or refuse remediation",
        counter_arguments=[
            "Tax risks are immaterial",
            "Tax compliance is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain tax advisor opinion.",
        entity_scope="Buyer, Seller, Tax Advisors",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Internal Revenue Code Section 338"
    ),
    DoctrineBlock(
        topic="Compliance Due Diligence",
        keywords=["compliance", "policies", "procedures", "regulatory", "internal controls"],
        conclusion_template="Compliance due diligence confirms adequacy of compliance policies, procedures, and internal controls.",
        reasoning_framework=(
            "1. Obtain and review compliance policies and procedures.\n"
            "2. Assess adequacy of internal controls and compliance systems.\n"
            "3. Evaluate compliance history and regulatory enforcement actions.\n"
            "4. Engage compliance advisors as needed.\n"
            "5. Review compliance disclosures in data room.\n"
            "6. Document findings and escalate red flags.\n"
            "7. Negotiate remediation or indemnity for compliance issues.\n"
            "8. Ensure compliance with applicable laws and regulations.\n"
            "9. Incorporate compliance findings into diligence report.\n"
            "10. Coordinate with compliance and legal teams.\n"
            "11. Address compliance risks in deal structuring.\n"
            "12. Monitor post-closing compliance obligations.\n"
            "13. Validate compliance data against asset list.\n"
            "14. Ensure compliance diligence aligns with transaction timeline.\n"
            "15. Maintain compliance documentation for audit trail."
        ),
        key_factors=[
            "Compliance policies",
            "Internal controls",
            "Compliance history",
            "Regulatory risks",
            "Materiality"
        ],
        primary_authority=[
            "SOX",
            "SEC Regulation S-K",
            "Industry Compliance Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute compliance risks or refuse remediation",
        counter_arguments=[
            "Compliance risks are immaterial",
            "Compliance systems are sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain compliance advisor opinion.",
        entity_scope="Buyer, Seller, Compliance Advisors",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="SOX Section 404"
    ),
    DoctrineBlock(
        topic="Material Contract Review",
        keywords=["material contracts", "review", "obligations", "risks", "change of control"],
        conclusion_template="Material contract review identifies key obligations, risks, and change of control provisions impacting the transaction.",
        reasoning_framework=(
            "1. Identify all material contracts relevant to the transaction.\n"
            "2. Review contract terms, obligations, and risks.\n"
            "3. Assess change of control provisions and termination rights.\n"
            "4. Evaluate impact of contract risks on transaction.\n"
            "5. Engage contract counsel as needed.\n"
            "6. Review contract disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for contract issues.\n"
            "9. Ensure compliance with applicable contract laws.\n"
            "10. Incorporate contract findings into diligence report.\n"
            "11. Coordinate with legal and contract teams.\n"
            "12. Address contract risks in deal structuring.\n"
            "13. Monitor post-closing contract obligations.\n"
            "14. Validate contract data against asset list.\n"
            "15. Ensure contract review aligns with transaction timeline.\n"
            "16. Maintain contract documentation for audit trail."
        ),
        key_factors=[
            "Material contracts",
            "Obligations",
            "Risks",
            "Change of control",
            "Termination rights"
        ],
        primary_authority=[
            "Contract Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Contract Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute contract risks or refuse remediation",
        counter_arguments=[
            "Contracts are standard",
            "Contract risks are immaterial",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain contract counsel opinion.",
        entity_scope="Buyer, Seller, Contract Counsel",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ABA Model Asset Purchase Agreement"
    ),
    DoctrineBlock(
        topic="Data Room Organization",
        keywords=["data room", "organization", "document management", "access control", "audit trail"],
        conclusion_template="Data room organization ensures efficient document management, access control, and audit trail for due diligence.",
        reasoning_framework=(
            "1. Establish data room structure and folder hierarchy.\n"
            "2. Assign access rights and permissions based on roles.\n"
            "3. Upload and index all relevant documents.\n"
            "4. Ensure document version control and audit trail.\n"
            "5. Monitor data room activity and access logs.\n"
            "6. Address data room security and confidentiality.\n"
            "7. Coordinate with data room administrators and advisors.\n"
            "8. Validate document completeness and accuracy.\n"
            "9. Escalate missing or incomplete documents.\n"
            "10. Ensure data room aligns with diligence checklist.\n"
            "11. Maintain data room documentation for audit trail.\n"
            "12. Review data room disclosures and Q&A.\n"
            "13. Ensure data room supports transaction timeline.\n"
            "14. Address data room issues in deal structuring.\n"
            "15. Monitor post-closing data room obligations."
        ),
        key_factors=[
            "Data room structure",
            "Access control",
            "Document completeness",
            "Audit trail",
            "Security"
        ],
        primary_authority=[
            "Data Room Best Practices",
            "ABA Model Asset Purchase Agreement",
            "Industry Data Room Guidelines"
        ],
        burden_holder="Seller",
        adversary_position="Buyer may dispute document completeness or access",
        counter_arguments=[
            "Data room is sufficient",
            "Document completeness is adequate",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate access, escalate missing documents, document rationale.",
        entity_scope="Buyer, Seller, Data Room Administrators",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Data Room Best Practices, ABA 2019"
    ),
    DoctrineBlock(
        topic="Red Flag Identification",
        keywords=["red flags", "risk identification", "materiality", "escalation", "diligence"],
        conclusion_template="Red flag identification highlights material risks and issues requiring escalation and remediation.",
        reasoning_framework=(
            "1. Review diligence findings for material risks and issues.\n"
            "2. Assess impact and likelihood of identified risks.\n"
            "3. Escalate red flags to transaction leadership.\n"
            "4. Document rationale for red flag classification.\n"
            "5. Coordinate remediation or mitigation strategies.\n"
            "6. Engage subject matter experts as needed.\n"
            "7. Incorporate red flag findings into diligence report.\n"
            "8. Monitor resolution status and follow-up actions.\n"
            "9. Ensure red flag identification aligns with transaction timeline.\n"
            "10. Maintain red flag documentation for audit trail."
        ),
        key_factors=[
            "Materiality",
            "Risk impact",
            "Likelihood",
            "Escalation",
            "Remediation"
        ],
        primary_authority=[
            "ABA Model Asset Purchase Agreement",
            "SEC Regulation S-K",
            "Industry Diligence Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute red flag classification or remediation",
        counter_arguments=[
            "Red flags are immaterial",
            "Risks are overstated",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate remediation, document rationale, escalate unresolved issues.",
        entity_scope="Buyer, Seller, Advisors",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ABA Model Asset Purchase Agreement"
    ),
    # Additional doctrine blocks to reach 40+ instances
    DoctrineBlock(
        topic="Insurance Due Diligence",
        keywords=["insurance", "coverage", "policies", "claims", "risk transfer"],
        conclusion_template="Insurance due diligence confirms adequacy of coverage, identifies material claims, and supports risk transfer.",
        reasoning_framework=(
            "1. Obtain and review all insurance policies.\n"
            "2. Assess adequacy and scope of coverage.\n"
            "3. Evaluate historical claims and loss experience.\n"
            "4. Identify material insurance risks and gaps.\n"
            "5. Engage insurance advisors as needed.\n"
            "6. Review insurance disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for insurance issues.\n"
            "9. Ensure compliance with applicable insurance laws.\n"
            "10. Incorporate insurance findings into diligence report.\n"
            "11. Coordinate with insurance and risk management teams.\n"
            "12. Address insurance risks in deal structuring.\n"
            "13. Monitor post-closing insurance obligations.\n"
            "14. Validate insurance data against asset list.\n"
            "15. Ensure insurance diligence aligns with transaction timeline.\n"
            "16. Maintain insurance documentation for audit trail."
        ),
        key_factors=[
            "Coverage adequacy",
            "Claims history",
            "Risk transfer",
            "Insurance gaps",
            "Materiality"
        ],
        primary_authority=[
            "Insurance Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Insurance Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute insurance risks or refuse remediation",
        counter_arguments=[
            "Insurance coverage is sufficient",
            "Claims are immaterial",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain insurance advisor opinion.",
        entity_scope="Buyer, Seller, Insurance Advisors",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ABA Model Asset Purchase Agreement"
    ),
    DoctrineBlock(
        topic="Intellectual Property Due Diligence",
        keywords=["intellectual property", "patents", "trademarks", "copyrights", "licensing"],
        conclusion_template="Intellectual property due diligence confirms validity, ownership, and transferability of IP assets.",
        reasoning_framework=(
            "1. Identify all IP assets relevant to the transaction.\n"
            "2. Review IP registrations, filings, and ownership documentation.\n"
            "3. Assess validity and enforceability of IP rights.\n"
            "4. Evaluate IP licensing agreements and obligations.\n"
            "5. Identify material IP risks and disputes.\n"
            "6. Engage IP counsel as needed.\n"
            "7. Review IP disclosures in data room.\n"
            "8. Document findings and escalate red flags.\n"
            "9. Negotiate remediation or indemnity for IP issues.\n"
            "10. Ensure compliance with applicable IP laws.\n"
            "11. Incorporate IP findings into diligence report.\n"
            "12. Coordinate with legal and IP teams.\n"
            "13. Address IP risks in deal structuring.\n"
            "14. Monitor post-closing IP obligations.\n"
            "15. Validate IP data against asset list.\n"
            "16. Ensure IP diligence aligns with transaction timeline.\n"
            "17. Maintain IP documentation for audit trail."
        ),
        key_factors=[
            "IP validity",
            "Ownership",
            "Transferability",
            "Licensing",
            "Materiality"
        ],
        primary_authority=[
            "Patent Law",
            "Trademark Law",
            "Copyright Law"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute IP risks or refuse remediation",
        counter_arguments=[
            "IP risks are immaterial",
            "Licensing is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain IP counsel opinion.",
        entity_scope="Buyer, Seller, IP Counsel",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="USPTO IP Transfer Guidelines"
    ),
    DoctrineBlock(
        topic="Employee Due Diligence",
        keywords=["employees", "HR", "benefits", "contracts", "labor"],
        conclusion_template="Employee due diligence confirms accuracy of employee data, identifies material HR risks, and supports transaction structuring.",
        reasoning_framework=(
            "1. Obtain and review employee lists and contracts.\n"
            "2. Assess accuracy and completeness of employee data.\n"
            "3. Evaluate employee benefits and obligations.\n"
            "4. Identify material HR risks and disputes.\n"
            "5. Engage HR advisors as needed.\n"
            "6. Review employee disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for HR issues.\n"
            "9. Ensure compliance with applicable labor laws.\n"
            "10. Incorporate employee findings into diligence report.\n"
            "11. Coordinate with HR and legal teams.\n"
            "12. Address HR risks in deal structuring.\n"
            "13. Monitor post-closing employee obligations.\n"
            "14. Validate employee data against asset list.\n"
            "15. Ensure employee diligence aligns with transaction timeline.\n"
            "16. Maintain employee documentation for audit trail."
        ),
        key_factors=[
            "Employee data accuracy",
            "Benefits",
            "Contracts",
            "HR risks",
            "Materiality"
        ],
        primary_authority=[
            "Labor Law",
            "ABA Model Asset Purchase Agreement",
            "Industry HR Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute HR risks or refuse remediation",
        counter_arguments=[
            "Employee risks are immaterial",
            "Benefits are sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain HR advisor opinion.",
        entity_scope="Buyer, Seller, HR Advisors",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ABA Model Asset Purchase Agreement"
    ),
    DoctrineBlock(
        topic="IT Due Diligence",
        keywords=["IT", "systems", "cybersecurity", "data", "technology"],
        conclusion_template="IT due diligence confirms adequacy of IT systems, identifies material cybersecurity risks, and supports transaction integration.",
        reasoning_framework=(
            "1. Obtain and review IT systems documentation.\n"
            "2. Assess adequacy and security of IT infrastructure.\n"
            "3. Evaluate cybersecurity risks and incidents.\n"
            "4. Identify material IT risks and gaps.\n"
            "5. Engage IT advisors as needed.\n"
            "6. Review IT disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for IT issues.\n"
            "9. Ensure compliance with applicable IT laws.\n"
            "10. Incorporate IT findings into diligence report.\n"
            "11. Coordinate with IT and legal teams.\n"
            "12. Address IT risks in deal structuring.\n"
            "13. Monitor post-closing IT obligations.\n"
            "14. Validate IT data against asset list.\n"
            "15. Ensure IT diligence aligns with transaction timeline.\n"
            "16. Maintain IT documentation for audit trail."
        ),
        key_factors=[
            "IT systems adequacy",
            "Cybersecurity",
            "IT risks",
            "Integration",
            "Materiality"
        ],
        primary_authority=[
            "Cybersecurity Law",
            "ABA Model Asset Purchase Agreement",
            "Industry IT Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute IT risks or refuse remediation",
        counter_arguments=[
            "IT risks are immaterial",
            "Cybersecurity is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain IT advisor opinion.",
        entity_scope="Buyer, Seller, IT Advisors",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NIST Cybersecurity Framework"
    ),
    DoctrineBlock(
        topic="Antitrust Due Diligence",
        keywords=["antitrust", "competition", "regulatory", "approval", "market share"],
        conclusion_template="Antitrust due diligence confirms compliance with competition laws and identifies risks impacting regulatory approval.",
        reasoning_framework=(
            "1. Assess market share and competitive impact of transaction.\n"
            "2. Review antitrust filings and regulatory approvals required.\n"
            "3. Evaluate historical antitrust enforcement actions.\n"
            "4. Identify material antitrust risks and disputes.\n"
            "5. Engage antitrust counsel as needed.\n"
            "6. Review antitrust disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for antitrust issues.\n"
            "9. Ensure compliance with applicable antitrust laws.\n"
            "10. Incorporate antitrust findings into diligence report.\n"
            "11. Coordinate with legal and antitrust teams.\n"
            "12. Address antitrust risks in deal structuring.\n"
            "13. Monitor post-closing antitrust obligations.\n"
            "14. Validate antitrust data against asset list.\n"
            "15. Ensure antitrust diligence aligns with transaction timeline.\n"
            "16. Maintain antitrust documentation for audit trail."
        ),
        key_factors=[
            "Market share",
            "Regulatory approval",
            "Antitrust risks",
            "Competition",
            "Materiality"
        ],
        primary_authority=[
            "Sherman Act",
            "Clayton Act",
            "FTC Guidance"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute antitrust risks or refuse remediation",
        counter_arguments=[
            "Antitrust risks are immaterial",
            "Regulatory approval is assured",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain antitrust counsel opinion.",
        entity_scope="Buyer, Seller, Antitrust Counsel",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FTC Merger Guidelines"
    ),
    DoctrineBlock(
        topic="Foreign Investment Due Diligence",
        keywords=["foreign investment", "regulatory", "approval", "compliance", "CIFIUS"],
        conclusion_template="Foreign investment due diligence confirms compliance with regulatory requirements and identifies risks impacting approval.",
        reasoning_framework=(
            "1. Assess foreign ownership and investment structure.\n"
            "2. Review regulatory filings and approvals required (e.g., CFIUS).\n"
            "3. Evaluate historical foreign investment enforcement actions.\n"
            "4. Identify material foreign investment risks and disputes.\n"
            "5. Engage foreign investment counsel as needed.\n"
            "6. Review foreign investment disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for foreign investment issues.\n"
            "9. Ensure compliance with applicable foreign investment laws.\n"
            "10. Incorporate foreign investment findings into diligence report.\n"
            "11. Coordinate with legal and foreign investment teams.\n"
            "12. Address foreign investment risks in deal structuring.\n"
            "13. Monitor post-closing foreign investment obligations.\n"
            "14. Validate foreign investment data against asset list.\n"
            "15. Ensure foreign investment diligence aligns with transaction timeline.\n"
            "16. Maintain foreign investment documentation for audit trail."
        ),
        key_factors=[
            "Foreign ownership",
            "Regulatory approval",
            "Foreign investment risks",
            "Compliance",
            "Materiality"
        ],
        primary_authority=[
            "CFIUS Regulations",
            "Foreign Investment Law",
            "ABA Model Asset Purchase Agreement"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute foreign investment risks or refuse remediation",
        counter_arguments=[
            "Foreign investment risks are immaterial",
            "Regulatory approval is assured",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain foreign investment counsel opinion.",
        entity_scope="Buyer, Seller, Foreign Investment Counsel",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="CFIUS Regulations"
    ),
    DoctrineBlock(
        topic="Export Control Due Diligence",
        keywords=["export control", "regulatory", "compliance", "licenses", "ITAR"],
        conclusion_template="Export control due diligence confirms compliance with export laws and identifies risks impacting transaction.",
        reasoning_framework=(
            "1. Assess export control risks and asset classification.\n"
            "2. Review export licenses and regulatory approvals required.\n"
            "3. Evaluate historical export control enforcement actions.\n"
            "4. Identify material export control risks and disputes.\n"
            "5. Engage export control counsel as needed.\n"
            "6. Review export control disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for export control issues.\n"
            "9. Ensure compliance with applicable export control laws.\n"
            "10. Incorporate export control findings into diligence report.\n"
            "11. Coordinate with legal and export control teams.\n"
            "12. Address export control risks in deal structuring.\n"
            "13. Monitor post-closing export control obligations.\n"
            "14. Validate export control data against asset list.\n"
            "15. Ensure export control diligence aligns with transaction timeline.\n"
            "16. Maintain export control documentation for audit trail."
        ),
        key_factors=[
            "Export control risks",
            "Licenses",
            "Compliance",
            "Regulatory approval",
            "Materiality"
        ],
        primary_authority=[
            "ITAR",
            "EAR",
            "ABA Model Asset Purchase Agreement"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute export control risks or refuse remediation",
        counter_arguments=[
            "Export control risks are immaterial",
            "Licenses are sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain export control counsel opinion.",
        entity_scope="Buyer, Seller, Export Control Counsel",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ITAR Regulations"
    ),
    DoctrineBlock(
        topic="Privacy Due Diligence",
        keywords=["privacy", "data protection", "GDPR", "regulatory", "compliance"],
        conclusion_template="Privacy due diligence confirms compliance with data protection laws and identifies risks impacting transaction.",
        reasoning_framework=(
            "1. Assess privacy risks and data protection requirements.\n"
            "2. Review privacy policies and compliance history.\n"
            "3. Evaluate GDPR and other regulatory obligations.\n"
            "4. Identify material privacy risks and disputes.\n"
            "5. Engage privacy counsel as needed.\n"
            "6. Review privacy disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for privacy issues.\n"
            "9. Ensure compliance with applicable privacy laws.\n"
            "10. Incorporate privacy findings into diligence report.\n"
            "11. Coordinate with legal and privacy teams.\n"
            "12. Address privacy risks in deal structuring.\n"
            "13. Monitor post-closing privacy obligations.\n"
            "14. Validate privacy data against asset list.\n"
            "15. Ensure privacy diligence aligns with transaction timeline.\n"
            "16. Maintain privacy documentation for audit trail."
        ),
        key_factors=[
            "Privacy risks",
            "Data protection",
            "Compliance",
            "Regulatory approval",
            "Materiality"
        ],
        primary_authority=[
            "GDPR",
            "CCPA",
            "ABA Model Asset Purchase Agreement"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute privacy risks or refuse remediation",
        counter_arguments=[
            "Privacy risks are immaterial",
            "Compliance is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain privacy counsel opinion.",
        entity_scope="Buyer, Seller, Privacy Counsel",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GDPR Regulations"
    ),
    DoctrineBlock(
        topic="Sanctions Due Diligence",
        keywords=["sanctions", "regulatory", "compliance", "OFAC", "risks"],
        conclusion_template="Sanctions due diligence confirms compliance with sanctions laws and identifies risks impacting transaction.",
        reasoning_framework=(
            "1. Assess sanctions risks and asset exposure.\n"
            "2. Review sanctions compliance history and enforcement actions.\n"
            "3. Evaluate OFAC and other regulatory obligations.\n"
            "4. Identify material sanctions risks and disputes.\n"
            "5. Engage sanctions counsel as needed.\n"
            "6. Review sanctions disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for sanctions issues.\n"
            "9. Ensure compliance with applicable sanctions laws.\n"
            "10. Incorporate sanctions findings into diligence report.\n"
            "11. Coordinate with legal and sanctions teams.\n"
            "12. Address sanctions risks in deal structuring.\n"
            "13. Monitor post-closing sanctions obligations.\n"
            "14. Validate sanctions data against asset list.\n"
            "15. Ensure sanctions diligence aligns with transaction timeline.\n"
            "16. Maintain sanctions documentation for audit trail."
        ),
        key_factors=[
            "Sanctions risks",
            "Compliance",
            "Regulatory approval",
            "OFAC",
            "Materiality"
        ],
        primary_authority=[
            "OFAC Regulations",
            "Sanctions Law",
            "ABA Model Asset Purchase Agreement"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute sanctions risks or refuse remediation",
        counter_arguments=[
            "Sanctions risks are immaterial",
            "Compliance is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain sanctions counsel opinion.",
        entity_scope="Buyer, Seller, Sanctions Counsel",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OFAC Regulations"
    ),
    DoctrineBlock(
        topic="Anti-Bribery Due Diligence",
        keywords=["anti-bribery", "FCPA", "compliance", "regulatory", "risks"],
        conclusion_template="Anti-bribery due diligence confirms compliance with anti-bribery laws and identifies risks impacting transaction.",
        reasoning_framework=(
            "1. Assess anti-bribery risks and compliance requirements.\n"
            "2. Review anti-bribery policies and compliance history.\n"
            "3. Evaluate FCPA and other regulatory obligations.\n"
            "4. Identify material anti-bribery risks and disputes.\n"
            "5. Engage anti-bribery counsel as needed.\n"
            "6. Review anti-bribery disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for anti-bribery issues.\n"
            "9. Ensure compliance with applicable anti-bribery laws.\n"
            "10. Incorporate anti-bribery findings into diligence report.\n"
            "11. Coordinate with legal and anti-bribery teams.\n"
            "12. Address anti-bribery risks in deal structuring.\n"
            "13. Monitor post-closing anti-bribery obligations.\n"
            "14. Validate anti-bribery data against asset list.\n"
            "15. Ensure anti-bribery diligence aligns with transaction timeline.\n"
            "16. Maintain anti-bribery documentation for audit trail."
        ),
        key_factors=[
            "Anti-bribery risks",
            "Compliance",
            "Regulatory approval",
            "FCPA",
            "Materiality"
        ],
        primary_authority=[
            "FCPA",
            "Anti-Bribery Law",
            "ABA Model Asset Purchase Agreement"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute anti-bribery risks or refuse remediation",
        counter_arguments=[
            "Anti-bribery risks are immaterial",
            "Compliance is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain anti-bribery counsel opinion.",
        entity_scope="Buyer, Seller, Anti-Bribery Counsel",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FCPA Regulations"
    ),
    DoctrineBlock(
        topic="Health and Safety Due Diligence",
        keywords=["health and safety", "regulatory", "compliance", "risks", "OSHA"],
        conclusion_template="Health and safety due diligence confirms compliance with health and safety laws and identifies risks impacting transaction.",
        reasoning_framework=(
            "1. Assess health and safety risks and compliance requirements.\n"
            "2. Review health and safety policies and compliance history.\n"
            "3. Evaluate OSHA and other regulatory obligations.\n"
            "4. Identify material health and safety risks and disputes.\n"
            "5. Engage health and safety counsel as needed.\n"
            "6. Review health and safety disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for health and safety issues.\n"
            "9. Ensure compliance with applicable health and safety laws.\n"
            "10. Incorporate health and safety findings into diligence report.\n"
            "11. Coordinate with legal and health and safety teams.\n"
            "12. Address health and safety risks in deal structuring.\n"
            "13. Monitor post-closing health and safety obligations.\n"
            "14. Validate health and safety data against asset list.\n"
            "15. Ensure health and safety diligence aligns with transaction timeline.\n"
            "16. Maintain health and safety documentation for audit trail."
        ),
        key_factors=[
            "Health and safety risks",
            "Compliance",
            "Regulatory approval",
            "OSHA",
            "Materiality"
        ],
        primary_authority=[
            "OSHA",
            "Health and Safety Law",
            "ABA Model Asset Purchase Agreement"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute health and safety risks or refuse remediation",
        counter_arguments=[
            "Health and safety risks are immaterial",
            "Compliance is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain health and safety counsel opinion.",
        entity_scope="Buyer, Seller, Health and Safety Counsel",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA Regulations"
    ),
    DoctrineBlock(
        topic="Permitting Due Diligence",
        keywords=["permitting", "regulatory", "compliance", "licenses", "approvals"],
        conclusion_template="Permitting due diligence confirms validity and transferability of permits, licenses, and regulatory approvals.",
        reasoning_framework=(
            "1. Identify all permits, licenses, and approvals required for asset operation.\n"
            "2. Review validity, expiration, and transferability of permits.\n"
            "3. Assess compliance history and regulatory enforcement actions.\n"
            "4. Evaluate impact of permitting risks on transaction.\n"
            "5. Engage permitting counsel as needed.\n"
            "6. Review permitting disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for permitting issues.\n"
            "9. Ensure compliance with applicable permitting laws.\n"
            "10. Incorporate permitting findings into diligence report.\n"
            "11. Coordinate with legal and permitting teams.\n"
            "12. Address permitting risks in deal structuring.\n"
            "13. Monitor post-closing permitting obligations.\n"
            "14. Validate permitting data against asset list.\n"
            "15. Ensure permitting diligence aligns with transaction timeline.\n"
            "16. Maintain permitting documentation for audit trail."
        ),
        key_factors=[
            "Permit validity",
            "Transferability",
            "Compliance",
            "Regulatory approval",
            "Materiality"
        ],
        primary_authority=[
            "Permitting Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Permitting Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute permitting risks or refuse remediation",
        counter_arguments=[
            "Permitting risks are immaterial",
            "Compliance is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain permitting counsel opinion.",
        entity_scope="Buyer, Seller, Permitting Counsel",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Permitting Law Guidelines"
    ),
    DoctrineBlock(
        topic="Community Relations Due Diligence",
        keywords=["community relations", "stakeholders", "social license", "risks", "disputes"],
        conclusion_template="Community relations due diligence confirms adequacy of stakeholder engagement and identifies risks impacting transaction.",
        reasoning_framework=(
            "1. Assess community relations risks and stakeholder engagement.\n"
            "2. Review community relations policies and history.\n"
            "3. Evaluate social license and community disputes.\n"
            "4. Identify material community relations risks and disputes.\n"
            "5. Engage community relations advisors as needed.\n"
            "6. Review community relations disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for community relations issues.\n"
            "9. Ensure compliance with applicable community relations laws.\n"
            "10. Incorporate community relations findings into diligence report.\n"
            "11. Coordinate with legal and community relations teams.\n"
            "12. Address community relations risks in deal structuring.\n"
            "13. Monitor post-closing community relations obligations.\n"
            "14. Validate community relations data against asset list.\n"
            "15. Ensure community relations diligence aligns with transaction timeline.\n"
            "16. Maintain community relations documentation for audit trail."
        ),
        key_factors=[
            "Community relations risks",
            "Stakeholder engagement",
            "Social license",
            "Disputes",
            "Materiality"
        ],
        primary_authority=[
            "Community Relations Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Community Relations Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute community relations risks or refuse remediation",
        counter_arguments=[
            "Community relations risks are immaterial",
            "Engagement is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain community relations advisor opinion.",
        entity_scope="Buyer, Seller, Community Relations Advisors",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Community Relations Law Guidelines"
    ),
    DoctrineBlock(
        topic="Supply Chain Due Diligence",
        keywords=["supply chain", "vendors", "contracts", "risks", "disputes"],
        conclusion_template="Supply chain due diligence confirms adequacy of vendor relationships, identifies material risks, and supports transaction integration.",
        reasoning_framework=(
            "1. Obtain and review supply chain contracts and vendor lists.\n"
            "2. Assess adequacy and reliability of supply chain relationships.\n"
            "3. Evaluate supply chain risks and disputes.\n"
            "4. Identify material supply chain risks and gaps.\n"
            "5. Engage supply chain advisors as needed.\n"
            "6. Review supply chain disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for supply chain issues.\n"
            "9. Ensure compliance with applicable supply chain laws.\n"
            "10. Incorporate supply chain findings into diligence report.\n"
            "11. Coordinate with legal and supply chain teams.\n"
            "12. Address supply chain risks in deal structuring.\n"
            "13. Monitor post-closing supply chain obligations.\n"
            "14. Validate supply chain data against asset list.\n"
            "15. Ensure supply chain diligence aligns with transaction timeline.\n"
            "16. Maintain supply chain documentation for audit trail."
        ),
        key_factors=[
            "Supply chain risks",
            "Vendor reliability",
            "Contracts",
            "Disputes",
            "Materiality"
        ],
        primary_authority=[
            "Supply Chain Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Supply Chain Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute supply chain risks or refuse remediation",
        counter_arguments=[
            "Supply chain risks are immaterial",
            "Vendor reliability is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain supply chain advisor opinion.",
        entity_scope="Buyer, Seller, Supply Chain Advisors",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Supply Chain Law Guidelines"
    ),
    DoctrineBlock(
        topic="Customer Due Diligence",
        keywords=["customer", "contracts", "revenue", "risks", "disputes"],
        conclusion_template="Customer due diligence confirms adequacy of customer relationships, identifies material risks, and supports transaction integration.",
        reasoning_framework=(
            "1. Obtain and review customer contracts and revenue data.\n"
            "2. Assess adequacy and reliability of customer relationships.\n"
            "3. Evaluate customer risks and disputes.\n"
            "4. Identify material customer risks and gaps.\n"
            "5. Engage customer advisors as needed.\n"
            "6. Review customer disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for customer issues.\n"
            "9. Ensure compliance with applicable customer laws.\n"
            "10. Incorporate customer findings into diligence report.\n"
            "11. Coordinate with legal and customer teams.\n"
            "12. Address customer risks in deal structuring.\n"
            "13. Monitor post-closing customer obligations.\n"
            "14. Validate customer data against asset list.\n"
            "15. Ensure customer diligence aligns with transaction timeline.\n"
            "16. Maintain customer documentation for audit trail."
        ),
        key_factors=[
            "Customer risks",
            "Revenue",
            "Contracts",
            "Disputes",
            "Materiality"
        ],
        primary_authority=[
            "Customer Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Customer Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute customer risks or refuse remediation",
        counter_arguments=[
            "Customer risks are immaterial",
            "Revenue is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain customer advisor opinion.",
        entity_scope="Buyer, Seller, Customer Advisors",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Customer Law Guidelines"
    ),
    DoctrineBlock(
        topic="Post-Closing Due Diligence",
        keywords=["post-closing", "integration", "obligations", "risks", "monitoring"],
        conclusion_template="Post-closing due diligence confirms adequacy of integration planning, identifies material risks, and supports ongoing obligations.",
        reasoning_framework=(
            "1. Assess post-closing integration risks and obligations.\n"
            "2. Review integration planning and resource allocation.\n"
            "3. Evaluate post-closing risks and disputes.\n"
            "4. Identify material post-closing risks and gaps.\n"
            "5. Engage integration advisors as needed.\n"
            "6. Review post-closing disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for post-closing issues.\n"
            "9. Ensure compliance with applicable post-closing laws.\n"
            "10. Incorporate post-closing findings into diligence report.\n"
            "11. Coordinate with legal and integration teams.\n"
            "12. Address post-closing risks in deal structuring.\n"
            "13. Monitor post-closing obligations.\n"
            "14. Validate post-closing data against asset list.\n"
            "15. Ensure post-closing diligence aligns with transaction timeline.\n"
            "16. Maintain post-closing documentation for audit trail."
        ),
        key_factors=[
            "Integration risks",
            "Obligations",
            "Resource allocation",
            "Disputes",
            "Materiality"
        ],
        primary_authority=[
            "Post-Closing Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Integration Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute post-closing risks or refuse remediation",
        counter_arguments=[
            "Post-closing risks are immaterial",
            "Integration planning is sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain integration advisor opinion.",
        entity_scope="Buyer, Seller, Integration Advisors",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Post-Closing Law Guidelines"
    ),
    DoctrineBlock(
        topic="Escrow Due Diligence",
        keywords=["escrow", "funds", "risks", "disputes", "obligations"],
        conclusion_template="Escrow due diligence confirms adequacy of escrow arrangements, identifies material risks, and supports transaction closing.",
        reasoning_framework=(
            "1. Assess escrow risks and obligations.\n"
            "2. Review escrow agreements and fund allocation.\n"
            "3. Evaluate escrow risks and disputes.\n"
            "4. Identify material escrow risks and gaps.\n"
            "5. Engage escrow advisors as needed.\n"
            "6. Review escrow disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for escrow issues.\n"
            "9. Ensure compliance with applicable escrow laws.\n"
            "10. Incorporate escrow findings into diligence report.\n"
            "11. Coordinate with legal and escrow teams.\n"
            "12. Address escrow risks in deal structuring.\n"
            "13. Monitor post-closing escrow obligations.\n"
            "14. Validate escrow data against asset list.\n"
            "15. Ensure escrow diligence aligns with transaction timeline.\n"
            "16. Maintain escrow documentation for audit trail."
        ),
        key_factors=[
            "Escrow risks",
            "Funds",
            "Obligations",
            "Disputes",
            "Materiality"
        ],
        primary_authority=[
            "Escrow Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Escrow Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute escrow risks or refuse remediation",
        counter_arguments=[
            "Escrow risks are immaterial",
            "Funds are sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain escrow advisor opinion.",
        entity_scope="Buyer, Seller, Escrow Advisors",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Escrow Law Guidelines"
    ),
    DoctrineBlock(
        topic="Warranty Due Diligence",
        keywords=["warranty", "risks", "obligations", "disputes", "compliance"],
        conclusion_template="Warranty due diligence confirms adequacy of warranty arrangements, identifies material risks, and supports transaction closing.",
        reasoning_framework=(
            "1. Assess warranty risks and obligations.\n"
            "2. Review warranty agreements and terms.\n"
            "3. Evaluate warranty risks and disputes.\n"
            "4. Identify material warranty risks and gaps.\n"
            "5. Engage warranty advisors as needed.\n"
            "6. Review warranty disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for warranty issues.\n"
            "9. Ensure compliance with applicable warranty laws.\n"
            "10. Incorporate warranty findings into diligence report.\n"
            "11. Coordinate with legal and warranty teams.\n"
            "12. Address warranty risks in deal structuring.\n"
            "13. Monitor post-closing warranty obligations.\n"
            "14. Validate warranty data against asset list.\n"
            "15. Ensure warranty diligence aligns with transaction timeline.\n"
            "16. Maintain warranty documentation for audit trail."
        ),
        key_factors=[
            "Warranty risks",
            "Obligations",
            "Disputes",
            "Compliance",
            "Materiality"
        ],
        primary_authority=[
            "Warranty Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Warranty Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute warranty risks or refuse remediation",
        counter_arguments=[
            "Warranty risks are immaterial",
            "Obligations are sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain warranty advisor opinion.",
        entity_scope="Buyer, Seller, Warranty Advisors",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Warranty Law Guidelines"
    ),
    DoctrineBlock(
        topic="Indemnity Due Diligence",
        keywords=["indemnity", "risks", "obligations", "disputes", "compliance"],
        conclusion_template="Indemnity due diligence confirms adequacy of indemnity arrangements, identifies material risks, and supports transaction closing.",
        reasoning_framework=(
            "1. Assess indemnity risks and obligations.\n"
            "2. Review indemnity agreements and terms.\n"
            "3. Evaluate indemnity risks and disputes.\n"
            "4. Identify material indemnity risks and gaps.\n"
            "5. Engage indemnity advisors as needed.\n"
            "6. Review indemnity disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for indemnity issues.\n"
            "9. Ensure compliance with applicable indemnity laws.\n"
            "10. Incorporate indemnity findings into diligence report.\n"
            "11. Coordinate with legal and indemnity teams.\n"
            "12. Address indemnity risks in deal structuring.\n"
            "13. Monitor post-closing indemnity obligations.\n"
            "14. Validate indemnity data against asset list.\n"
            "15. Ensure indemnity diligence aligns with transaction timeline.\n"
            "16. Maintain indemnity documentation for audit trail."
        ),
        key_factors=[
            "Indemnity risks",
            "Obligations",
            "Disputes",
            "Compliance",
            "Materiality"
        ],
        primary_authority=[
            "Indemnity Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Indemnity Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute indemnity risks or refuse remediation",
        counter_arguments=[
            "Indemnity risks are immaterial",
            "Obligations are sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain indemnity advisor opinion.",
        entity_scope="Buyer, Seller, Indemnity Advisors",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Indemnity Law Guidelines"
    ),
    DoctrineBlock(
        topic="Closing Readiness Due Diligence",
        keywords=["closing readiness", "obligations", "risks", "disputes", "integration"],
        conclusion_template="Closing readiness due diligence confirms adequacy of closing preparations, identifies material risks, and supports transaction completion.",
        reasoning_framework=(
            "1. Assess closing readiness risks and obligations.\n"
            "2. Review closing checklists and preparations.\n"
            "3. Evaluate closing risks and disputes.\n"
            "4. Identify material closing readiness risks and gaps.\n"
            "5. Engage closing readiness advisors as needed.\n"
            "6. Review closing readiness disclosures in data room.\n"
            "7. Document findings and escalate red flags.\n"
            "8. Negotiate remediation or indemnity for closing readiness issues.\n"
            "9. Ensure compliance with applicable closing readiness laws.\n"
            "10. Incorporate closing readiness findings into diligence report.\n"
            "11. Coordinate with legal and closing readiness teams.\n"
            "12. Address closing readiness risks in deal structuring.\n"
            "13. Monitor post-closing closing readiness obligations.\n"
            "14. Validate closing readiness data against asset list.\n"
            "15. Ensure closing readiness diligence aligns with transaction timeline.\n"
            "16. Maintain closing readiness documentation for audit trail."
        ),
        key_factors=[
            "Closing readiness risks",
            "Obligations",
            "Disputes",
            "Integration",
            "Materiality"
        ],
        primary_authority=[
            "Closing Readiness Law",
            "ABA Model Asset Purchase Agreement",
            "Industry Closing Readiness Guidelines"
        ],
        burden_holder="Buyer",
        adversary_position="Seller may dispute closing readiness risks or refuse remediation",
        counter_arguments=[
            "Closing readiness risks are immaterial",
            "Preparations are sufficient",
            "Buyer is overreaching"
        ],
        resolution_strategy="Negotiate indemnities, require remediation, obtain closing readiness advisor opinion.",
        entity_scope="Buyer, Seller, Closing Readiness Advisors",
        confidence