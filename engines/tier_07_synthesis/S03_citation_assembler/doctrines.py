from dataclasses import dataclass, field
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
        topic="Bluebook Citation Format: Case Law",
        keywords=["Bluebook", "case law", "citation", "format", "reporter", "court", "year"],
        conclusion_template="The citation should conform to Bluebook Rule 10, including party names, reporter, court, and year.",
        reasoning_framework=(
            "1. Identify the full case name, omitting given names and abbreviating per Bluebook T6.\n"
            "2. Select the official reporter and parallel citations if applicable (R10.3).\n"
            "3. Include the volume number, reporter abbreviation, and first page of the case.\n"
            "4. Add pinpoint citations if referencing specific pages (R10.9).\n"
            "5. Specify the court and year in parenthesis, omitting the court for U.S. Supreme Court cases (R10.4).\n"
            "6. Apply appropriate signal words and parentheticals as needed (R1.2, R10.6).\n"
            "7. Ensure all abbreviations and punctuation conform to Bluebook tables and rules.\n"
            "8. If subsequent history exists, append per R10.7.\n"
            "9. Confirm the citation is free of duplications and is normalized for consistency.\n"
            "10. Cross-reference with parallel citations for completeness."
        ),
        key_factors=[
            "Proper abbreviation of party names",
            "Correct reporter selection",
            "Inclusion of court and year",
            "Pinpoint citation accuracy",
            "Use of parallel citations"
        ],
        primary_authority=[
            "The Bluebook: A Uniform System of Citation, Rule 10",
            "Bluebook Table T6, T7, T10"
        ],
        burden_holder="Citing party",
        adversary_position="Citation is incomplete or improperly formatted",
        counter_arguments=[
            "Alternative citation styles may be acceptable in certain courts",
            "Local rules may override Bluebook requirements"
        ],
        resolution_strategy="Apply Bluebook Rule 10 strictly unless local rules dictate otherwise.",
        entity_scope="Federal and state courts adhering to Bluebook",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 10"
    ),
    DoctrineBlock(
        topic="ALWD Citation Format: Statutes",
        keywords=["ALWD", "statutes", "citation", "format", "code", "section", "year"],
        conclusion_template="Statutory citations should follow ALWD Rule 12, including title, code, section, and year.",
        reasoning_framework=(
            "1. Identify the official code and title for the statute.\n"
            "2. Abbreviate the code name according to ALWD Appendix 3.\n"
            "3. Include the section symbol (§) and the section number.\n"
            "4. Add the publisher or editor if required by jurisdiction.\n"
            "5. Insert the year of the code edition in parenthesis at the end.\n"
            "6. For federal statutes, use U.S.C. as the code abbreviation.\n"
            "7. For state statutes, follow state-specific abbreviations as listed in ALWD Appendix 3.\n"
            "8. If citing to a supplement or annotated code, indicate this in the citation.\n"
            "9. Ensure the citation is free of duplications and normalized for consistency.\n"
            "10. Cross-reference with parallel citations if available."
        ),
        key_factors=[
            "Correct code abbreviation",
            "Accurate section number",
            "Proper year of code edition",
            "Jurisdiction-specific requirements"
        ],
        primary_authority=[
            "ALWD Guide to Legal Citation, Rule 12",
            "ALWD Appendix 3"
        ],
        burden_holder="Citing party",
        adversary_position="Citation omits necessary code information or uses incorrect abbreviation",
        counter_arguments=[
            "Some courts may accept unofficial code abbreviations",
            "Year of code edition may be omitted in certain contexts"
        ],
        resolution_strategy="Apply ALWD Rule 12 and jurisdictional requirements strictly.",
        entity_scope="Jurisdictions using ALWD",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ALWD Rule 12"
    ),
    DoctrineBlock(
        topic="Texas Citation Rules: Case Law",
        keywords=["Texas", "citation", "case law", "format", "reporter", "court", "year"],
        conclusion_template="Texas case law citations must conform to Texas Rule of Appellate Procedure 38.1(i) and Texas Greenbook.",
        reasoning_framework=(
            "1. Use the case name as it appears in the reporter, abbreviating per Texas Greenbook Rule 4.1.\n"
            "2. Cite to the official reporter, using the correct abbreviation (Greenbook Rule 6.1).\n"
            "3. Include the volume number, reporter abbreviation, and first page.\n"
            "4. Add pinpoint citations for specific references (Greenbook Rule 6.3).\n"
            "5. Specify the court and year in parenthesis, using Greenbook Table 7 for court abbreviations.\n"
            "6. Include subsequent history if relevant (Greenbook Rule 6.4).\n"
            "7. Apply parallel citations if required by the court.\n"
            "8. Normalize citation format to avoid duplication and inconsistency.\n"
            "9. Cross-reference with Bluebook if citation is for federal court in Texas.\n"
            "10. Ensure compliance with local court rules."
        ),
        key_factors=[
            "Proper party name abbreviation",
            "Correct reporter and court abbreviation",
            "Inclusion of year",
            "Pinpoint citation accuracy"
        ],
        primary_authority=[
            "Texas Rules of Appellate Procedure 38.1(i)",
            "Texas Greenbook, Rule 6"
        ],
        burden_holder="Citing party",
        adversary_position="Citation does not conform to Texas Greenbook or omits necessary elements",
        counter_arguments=[
            "Federal courts in Texas may require Bluebook format",
            "Some courts may accept alternative abbreviations"
        ],
        resolution_strategy="Follow Texas Greenbook unless federal or local rules override.",
        entity_scope="Texas state courts",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Texas Greenbook Rule 6"
    ),
    DoctrineBlock(
        topic="Federal Citation Format: Statutes",
        keywords=["federal", "statutes", "citation", "U.S.C.", "section", "year"],
        conclusion_template="Federal statutory citations must include title, U.S.C., section, and year per Bluebook Rule 12.",
        reasoning_framework=(
            "1. Identify the title number and section of the United States Code (U.S.C.).\n"
            "2. Format as: [Title] U.S.C. § [Section] ([Year]).\n"
            "3. Use the section symbol (§) and ensure correct spacing.\n"
            "4. If citing to a supplement, indicate the supplement year.\n"
            "5. For annotated codes, use the official abbreviation and indicate the publisher if required.\n"
            "6. Omit the year if referencing the current code unless required by context.\n"
            "7. Normalize the citation to avoid duplication and ensure consistency.\n"
            "8. Cross-reference with parallel citations if necessary.\n"
            "9. Apply Bluebook Table T1 for federal statutory abbreviations.\n"
            "10. Confirm accuracy with the latest code edition."
        ),
        key_factors=[
            "Correct title and section number",
            "Proper abbreviation of U.S.C.",
            "Inclusion of year when necessary",
            "Use of section symbol"
        ],
        primary_authority=[
            "Bluebook Rule 12",
            "Bluebook Table T1"
        ],
        burden_holder="Citing party",
        adversary_position="Citation omits title, section, or year, or uses incorrect abbreviation",
        counter_arguments=[
            "Year may be omitted for current code",
            "Some courts may accept unofficial abbreviations"
        ],
        resolution_strategy="Apply Bluebook Rule 12 and Table T1 for all federal statutory citations.",
        entity_scope="Federal courts",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 12"
    ),
    DoctrineBlock(
        topic="Regulatory Citation Format: Federal Regulations",
        keywords=["federal regulations", "C.F.R.", "citation", "format", "section", "year"],
        conclusion_template="Citations to federal regulations must include title, C.F.R., section, and year per Bluebook Rule 14.",
        reasoning_framework=(
            "1. Identify the title number and section of the Code of Federal Regulations (C.F.R.).\n"
            "2. Format as: [Title] C.F.R. § [Section] ([Year]).\n"
            "3. Use the section symbol (§) and ensure correct abbreviation of C.F.R.\n"
            "4. Include the year of the code edition in parenthesis.\n"
            "5. For proposed or pending regulations, cite to the Federal Register per Bluebook Rule 14.2.\n"
            "6. Normalize the citation to avoid duplication and ensure consistency.\n"
            "7. Cross-reference with parallel citations if available.\n"
            "8. Apply Bluebook Table T1 for regulatory abbreviations.\n"
            "9. Confirm the citation with the current code edition.\n"
            "10. Use pinpoint citations for specific provisions."
        ),
        key_factors=[
            "Correct title and section number",
            "Proper abbreviation of C.F.R.",
            "Inclusion of year",
            "Pinpoint citation accuracy"
        ],
        primary_authority=[
            "Bluebook Rule 14",
            "Bluebook Table T1"
        ],
        burden_holder="Citing party",
        adversary_position="Citation omits title, section, or year, or uses incorrect abbreviation",
        counter_arguments=[
            "Year may be omitted for current regulations in some contexts",
            "Some courts may accept unofficial abbreviations"
        ],
        resolution_strategy="Apply Bluebook Rule 14 and Table T1 for all federal regulatory citations.",
        entity_scope="Federal courts and agencies",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 14"
    ),
    DoctrineBlock(
        topic="Case Law Citation Hierarchies",
        keywords=["case law", "citation", "hierarchy", "precedent", "authority", "court level"],
        conclusion_template="Citations should prioritize higher court decisions within the same jurisdiction.",
        reasoning_framework=(
            "1. Identify the jurisdiction relevant to the legal issue.\n"
            "2. Prioritize citations to the highest court within the jurisdiction (e.g., U.S. Supreme Court, state supreme court).\n"
            "3. Cite intermediate appellate courts if no controlling supreme court authority exists.\n"
            "4. Use trial court decisions only when no higher authority is available or for persuasive value.\n"
            "5. Recognize that federal circuit courts are binding within their circuit but only persuasive elsewhere.\n"
            "6. State court decisions are binding within their state but persuasive in other jurisdictions.\n"
            "7. When citing multiple authorities, list them in order of precedential value.\n"
            "8. Use signal words to indicate the nature of authority (e.g., 'see', 'cf.').\n"
            "9. Normalize citations to avoid duplication and ensure consistency.\n"
            "10. Cross-reference with parallel citations if necessary."
        ),
        key_factors=[
            "Jurisdiction of the court",
            "Level of the court",
            "Binding versus persuasive authority",
            "Recency of the decision"
        ],
        primary_authority=[
            "Bluebook Rule 1.4",
            "Federal Rules of Appellate Procedure",
            "State court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Lower court decision cited when higher authority is available",
        counter_arguments=[
            "Higher court may not have addressed the specific issue",
            "Lower court decision may provide persuasive reasoning"
        ],
        resolution_strategy="Always cite the highest available authority; explain reliance on lower courts if necessary.",
        entity_scope="All U.S. courts",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Bluebook Rule 1.4"
    ),
    DoctrineBlock(
        topic="Statutory Citation Assembly",
        keywords=["statute", "citation", "assembly", "format", "code", "section", "year"],
        conclusion_template="Statutory citations must include code name, section, and year per controlling citation manual.",
        reasoning_framework=(
            "1. Determine the controlling citation manual (Bluebook, ALWD, state guide).\n"
            "2. Identify the official code and section for the statute.\n"
            "3. Abbreviate the code name per the manual's tables.\n"
            "4. Use the section symbol (§) and the correct section number.\n"
            "5. Include the year of the code edition in parenthesis if required.\n"
            "6. For annotated or unofficial codes, indicate the publisher if required.\n"
            "7. Normalize the citation to avoid duplication and ensure consistency.\n"
            "8. Cross-reference with parallel citations if available.\n"
            "9. Apply jurisdiction-specific rules as necessary.\n"
            "10. Confirm accuracy with the latest code edition."
        ),
        key_factors=[
            "Correct code and section number",
            "Proper abbreviation",
            "Inclusion of year",
            "Jurisdictional requirements"
        ],
        primary_authority=[
            "Bluebook Rule 12",
            "ALWD Rule 12",
            "State citation guides"
        ],
        burden_holder="Citing party",
        adversary_position="Citation omits necessary elements or uses incorrect format",
        counter_arguments=[
            "Some courts may accept unofficial abbreviations",
            "Year may be omitted for current codes"
        ],
        resolution_strategy="Apply the controlling citation manual and jurisdictional rules.",
        entity_scope="All U.S. jurisdictions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 12"
    ),
    DoctrineBlock(
        topic="Citation Deduplication",
        keywords=["citation", "deduplication", "normalization", "redundancy", "parallel citations"],
        conclusion_template="Duplicate citations should be removed unless parallel citations are required.",
        reasoning_framework=(
            "1. Identify all citations to the same authority within the document.\n"
            "2. Determine if parallel citations are required by court rules.\n"
            "3. Remove duplicate citations to the same reporter or code.\n"
            "4. Retain parallel citations only if required or if they add clarity.\n"
            "5. Normalize citation format to ensure consistency.\n"
            "6. Use cross-references to avoid unnecessary repetition.\n"
            "7. Confirm compliance with local court rules regarding parallel citations.\n"
            "8. Document any retained parallel citations in a footnote if necessary.\n"
            "9. Ensure that deduplication does not omit required authority.\n"
            "10. Review for inadvertent omission of necessary citations."
        ),
        key_factors=[
            "Court rules on parallel citations",
            "Clarity and completeness",
            "Avoidance of redundancy",
            "Consistency of citation format"
        ],
        primary_authority=[
            "Bluebook Rule 10.3.1",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission of required parallel citations",
        counter_arguments=[
            "Parallel citations may be required for clarity",
            "Some courts mandate parallel citations"
        ],
        resolution_strategy="Remove duplicates unless parallel citations are required by rule.",
        entity_scope="All U.S. courts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 10.3.1"
    ),
    DoctrineBlock(
        topic="Authority Ranking by Court Level",
        keywords=["authority", "ranking", "court level", "precedent", "hierarchy"],
        conclusion_template="Citations should be ranked by precedential value, highest court first.",
        reasoning_framework=(
            "1. Identify all authorities relevant to the legal issue.\n"
            "2. Determine the court level for each authority (e.g., Supreme Court, appellate, trial).\n"
            "3. Rank authorities by precedential value: Supreme Court > Appellate > Trial.\n"
            "4. For federal issues, U.S. Supreme Court is highest; for state issues, state supreme court is highest.\n"
            "5. Within federal circuits, circuit court decisions are binding within the circuit.\n"
            "6. State appellate decisions are binding within their state unless overruled.\n"
            "7. Use signal words to indicate the weight of authority.\n"
            "8. Normalize citation format for consistency.\n"
            "9. Cross-reference with parallel citations if necessary.\n"
            "10. Explain reliance on lower court authority if higher authority is unavailable."
        ),
        key_factors=[
            "Jurisdiction",
            "Court level",
            "Binding versus persuasive authority",
            "Recency of decision"
        ],
        primary_authority=[
            "Bluebook Rule 1.4",
            "Federal Rules of Appellate Procedure"
        ],
        burden_holder="Citing party",
        adversary_position="Improper ranking of authority",
        counter_arguments=[
            "Lower court may address issue not reached by higher court",
            "Persuasive value may justify citation"
        ],
        resolution_strategy="Rank citations by court level and explain deviations.",
        entity_scope="All U.S. courts",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 1.4"
    ),
    DoctrineBlock(
        topic="Citation String Normalization",
        keywords=["citation", "normalization", "format", "consistency", "standardization"],
        conclusion_template="All citations must be normalized to a consistent format as per the controlling manual.",
        reasoning_framework=(
            "1. Identify the controlling citation manual (Bluebook, ALWD, state guide).\n"
            "2. Standardize abbreviations, punctuation, and sequence of elements.\n"
            "3. Remove redundant or unnecessary information.\n"
            "4. Ensure consistent use of signals, parentheticals, and pinpoint citations.\n"
            "5. Apply normalization across all citations in the document.\n"
            "6. Cross-reference with parallel citations for consistency.\n"
            "7. Use citation management tools to check for errors.\n"
            "8. Review for compliance with court-specific requirements.\n"
            "9. Document any deviations from standard format.\n"
            "10. Confirm final citation format before submission."
        ),
        key_factors=[
            "Consistency of format",
            "Correct abbreviations",
            "Proper sequence of elements",
            "Compliance with controlling manual"
        ],
        primary_authority=[
            "Bluebook Rule 1.1",
            "ALWD Rule 1.1"
        ],
        burden_holder="Citing party",
        adversary_position="Inconsistent or non-standard citation format",
        counter_arguments=[
            "Local rules may permit alternative formats",
            "Some courts may prioritize clarity over strict format"
        ],
        resolution_strategy="Normalize all citations unless local rules dictate otherwise.",
        entity_scope="All U.S. jurisdictions",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 1.1"
    ),
    DoctrineBlock(
        topic="Parallel Citations",
        keywords=["parallel citations", "reporters", "case law", "citation", "format"],
        conclusion_template="Parallel citations must be included if required by court rules.",
        reasoning_framework=(
            "1. Identify all official and unofficial reporters for the case.\n"
            "2. Determine if the court requires parallel citations (Bluebook Rule 10.3.1).\n"
            "3. Include all required parallel citations in the prescribed order.\n"
            "4. Separate parallel citations with commas.\n"
            "5. Normalize abbreviations and punctuation for consistency.\n"
            "6. Omit parallel citations if not required by the court.\n"
            "7. Cross-reference with local court rules for specific requirements.\n"
            "8. Document any omitted parallel citations and the reason.\n"
            "9. Ensure that parallel citations do not create redundancy.\n"
            "10. Confirm accuracy of all reporter citations."
        ),
        key_factors=[
            "Court requirements",
            "Official and unofficial reporters",
            "Order of citations",
            "Consistency of format"
        ],
        primary_authority=[
            "Bluebook Rule 10.3.1",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission of required parallel citations",
        counter_arguments=[
            "Parallel citations may not be required",
            "Some courts prohibit parallel citations"
        ],
        resolution_strategy="Include parallel citations only if required by rule.",
        entity_scope="All U.S. courts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 10.3.1"
    ),
    DoctrineBlock(
        topic="Subsequent History",
        keywords=["subsequent history", "case law", "citation", "appeal", "reversal", "affirmance"],
        conclusion_template="Subsequent history must be included for all cited cases not in their final disposition.",
        reasoning_framework=(
            "1. Determine if the cited case has been appealed, reversed, affirmed, or otherwise modified.\n"
            "2. Include subsequent history in the citation per Bluebook Rule 10.7.\n"
            "3. Use appropriate abbreviations for subsequent history (e.g., aff’d, rev’d, cert. denied).\n"
            "4. Place subsequent history after the main citation, separated by a comma.\n"
            "5. Omit subsequent history for U.S. Supreme Court cases unless necessary for clarity.\n"
            "6. Normalize format for consistency.\n"
            "7. Cross-reference with court rules for any additional requirements.\n"
            "8. Document any omitted subsequent history and the reason.\n"
            "9. Confirm accuracy of subsequent history information.\n"
            "10. Update citations if subsequent history changes before submission."
        ),
        key_factors=[
            "Existence of subsequent appellate action",
            "Proper abbreviation",
            "Placement in citation",
            "Clarity and completeness"
        ],
        primary_authority=[
            "Bluebook Rule 10.7",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission or misstatement of subsequent history",
        counter_arguments=[
            "Subsequent history may not be relevant in all contexts",
            "Some courts may not require subsequent history"
        ],
        resolution_strategy="Include subsequent history unless clearly inapplicable.",
        entity_scope="All U.S. courts",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 10.7"
    ),
    DoctrineBlock(
        topic="Pinpoint Citations",
        keywords=["pinpoint citation", "page number", "section", "citation", "accuracy"],
        conclusion_template="Pinpoint citations must be included when referencing specific material.",
        reasoning_framework=(
            "1. Identify the specific page or section being referenced in the authority.\n"
            "2. Add the pinpoint page or section after the first page in the citation (Bluebook Rule 3.2(a)).\n"
            "3. Use correct punctuation and abbreviation for pinpoint citations.\n"
            "4. For statutes and regulations, use subsection or paragraph numbers as appropriate.\n"
            "5. Normalize format for consistency.\n"
            "6. Cross-reference with court rules for any additional requirements.\n"
            "7. Omit pinpoint citations only if referencing the entire authority.\n"
            "8. Confirm accuracy of pinpoint information.\n"
            "9. Document any omitted pinpoint citations and the reason.\n"
            "10. Update pinpoint citations if the referenced material changes."
        ),
        key_factors=[
            "Specificity of reference",
            "Correct page or section number",
            "Proper placement in citation",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 3.2(a)",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission of necessary pinpoint citation",
        counter_arguments=[
            "Pinpoint citation may not be necessary for general references",
            "Some courts may not require pinpoint citations"
        ],
        resolution_strategy="Include pinpoint citations unless referencing the entire authority.",
        entity_scope="All U.S. courts",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 3.2(a)"
    ),
    DoctrineBlock(
        topic="Signal Words Usage",
        keywords=["signal words", "citation", "support", "contrast", "see", "cf.", "e.g."],
        conclusion_template="Signal words must be used to indicate the relationship of cited authority.",
        reasoning_framework=(
            "1. Determine the relationship between the cited authority and the proposition.\n"
            "2. Use appropriate signal words (e.g., see, cf., e.g., accord, but see) per Bluebook Rule 1.2.\n"
            "3. Place the signal at the beginning of the citation sentence.\n"
            "4. Use italics for signal words.\n"
            "5. Separate multiple citations with semicolons.\n"
            "6. Normalize format for consistency.\n"
            "7. Omit signal words only if the authority directly states the proposition.\n"
            "8. Cross-reference with court rules for any additional requirements.\n"
            "9. Document any omitted signal words and the reason.\n"
            "10. Confirm that signal words accurately reflect the relationship."
        ),
        key_factors=[
            "Nature of relationship to proposition",
            "Correct signal word",
            "Proper placement and formatting",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 1.2",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or omitted signal word",
        counter_arguments=[
            "Signal words may be omitted for direct quotations",
            "Some courts may not require signal words"
        ],
        resolution_strategy="Use signal words unless authority directly supports the proposition.",
        entity_scope="All U.S. courts",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 1.2"
    ),
    DoctrineBlock(
        topic="Parenthetical Construction",
        keywords=["parenthetical", "citation", "explanation", "clarity", "format"],
        conclusion_template="Parentheticals should be used to clarify the relevance of cited authority.",
        reasoning_framework=(
            "1. Determine if an explanation is necessary to clarify the relevance of the authority.\n"
            "2. Construct a concise parenthetical after the citation, per Bluebook Rule 1.5.\n"
            "3. Use present participle phrases or short statements.\n"
            "4. Place the parenthetical after the citation and before any subsequent history.\n"
            "5. Normalize punctuation and format for consistency.\n"
            "6. Omit unnecessary parentheticals to avoid clutter.\n"
            "7. Cross-reference with court rules for any additional requirements.\n"
            "8. Document any omitted parentheticals and the reason.\n"
            "9. Confirm that parentheticals add clarity.\n"
            "10. Update parentheticals if the context changes."
        ),
        key_factors=[
            "Need for clarification",
            "Conciseness",
            "Proper placement",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 1.5",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission or overuse of parentheticals",
        counter_arguments=[
            "Parentheticals may not be necessary for clear citations",
            "Excessive parentheticals may reduce clarity"
        ],
        resolution_strategy="Use parentheticals only when necessary for clarity.",
        entity_scope="All U.S. courts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 1.5"
    ),
    DoctrineBlock(
        topic="Citation Verification",
        keywords=["citation", "verification", "accuracy", "authority", "validation"],
        conclusion_template="All citations must be verified for accuracy and current validity.",
        reasoning_framework=(
            "1. Check each citation against the original source for accuracy.\n"
            "2. Confirm that the cited authority is still good law (e.g., not overruled or superseded).\n"
            "3. Use citation validation tools (e.g., Shepard's, KeyCite) to check status.\n"
            "4. Update citations if the authority has changed.\n"
            "5. Normalize format for consistency.\n"
            "6. Cross-reference with court rules for any additional requirements.\n"
            "7. Document any changes to citations and the reason.\n"
            "8. Confirm that all citations are complete and accurate.\n"
            "9. Review for inadvertent citation errors.\n"
            "10. Finalize citation verification before submission."
        ),
        key_factors=[
            "Accuracy of citation",
            "Current validity of authority",
            "Completeness",
            "Use of validation tools"
        ],
        primary_authority=[
            "Bluebook Rule 1.1",
            "Shepard's Citations",
            "KeyCite"
        ],
        burden_holder="Citing party",
        adversary_position="Citation to overruled or inaccurate authority",
        counter_arguments=[
            "Some authorities may be cited for historical context",
            "Validation tools may have limitations"
        ],
        resolution_strategy="Verify all citations and update as necessary.",
        entity_scope="All U.S. courts",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="Bluebook Rule 1.1"
    ),
    DoctrineBlock(
        topic="Cross-Reference Linking",
        keywords=["cross-reference", "citation", "linking", "internal citation", "footnote"],
        conclusion_template="Cross-references should be used to link related citations within the document.",
        reasoning_framework=(
            "1. Identify all related authorities cited in the document.\n"
            "2. Use cross-references to direct the reader to related citations (e.g., 'see supra note 5').\n"
            "3. Place cross-references in footnotes or parentheticals as appropriate.\n"
            "4. Normalize format for consistency.\n"
            "5. Avoid excessive cross-referencing that may confuse the reader.\n"
            "6. Cross-reference with court rules for any additional requirements.\n"
            "7. Document any omitted cross-references and the reason.\n"
            "8. Confirm accuracy of cross-reference links.\n"
            "9. Update cross-references if citation numbering changes.\n"
            "10. Review for clarity and ease of navigation."
        ),
        key_factors=[
            "Clarity of cross-references",
            "Accuracy of links",
            "Proper placement",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 3.5",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission or inaccuracy in cross-references",
        counter_arguments=[
            "Cross-references may not be necessary in short documents",
            "Excessive cross-referencing may reduce clarity"
        ],
        resolution_strategy="Use cross-references judiciously for clarity.",
        entity_scope="All U.S. courts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 3.5"
    ),
    DoctrineBlock(
        topic="Citation Count per Authority",
        keywords=["citation count", "authority", "frequency", "repetition", "support"],
        conclusion_template="The number of citations to an authority should reflect its importance and relevance.",
        reasoning_framework=(
            "1. Track the frequency of citations to each authority within the document.\n"
            "2. Ensure that repeated citations are necessary for clarity or emphasis.\n"
            "3. Use 'id.' for repeated citations to the same authority in close succession (Bluebook Rule 4.1).\n"
            "4. Avoid excessive repetition that may clutter the document.\n"
            "5. Normalize format for consistency.\n"
            "6. Cross-reference with court rules for any additional requirements.\n"
            "7. Document any deviations from standard citation count and the reason.\n"
            "8. Confirm that citation count accurately reflects the authority's importance.\n"
            "9. Review for inadvertent omission of necessary citations.\n"
            "10. Finalize citation count before submission."
        ),
        key_factors=[
            "Importance of authority",
            "Clarity",
            "Avoidance of repetition",
            "Proper use of 'id.'"
        ],
        primary_authority=[
            "Bluebook Rule 4.1",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Excessive or insufficient citation to authority",
        counter_arguments=[
            "Repetition may be necessary for emphasis",
            "Some courts may require repeated citations"
        ],
        resolution_strategy="Cite authority as needed for clarity and support.",
        entity_scope="All U.S. courts",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 4.1"
    ),
    DoctrineBlock(
        topic="Citation Freshness Scoring",
        keywords=["citation", "freshness", "recency", "authority", "scoring"],
        conclusion_template="Recent authority is generally preferred unless older precedent is controlling.",
        reasoning_framework=(
            "1. Assess the date of each cited authority.\n"
            "2. Prefer more recent decisions when they are controlling or persuasive.\n"
            "3. Use older precedent only if it remains good law and is controlling.\n"
            "4. Score citations for freshness based on recency and relevance.\n"
            "5. Normalize format for consistency.\n"
            "6. Cross-reference with court rules for any additional requirements.\n"
            "7. Document any reliance on older precedent and the reason.\n"
            "8. Confirm that all authorities cited are still good law.\n"
            "9. Review for inadvertent omission of recent authority.\n"
            "10. Finalize citation selection before submission."
        ),
        key_factors=[
            "Recency of authority",
            "Controlling versus persuasive value",
            "Current validity",
            "Relevance"
        ],
        primary_authority=[
            "Bluebook Rule 1.1",
            "Shepard's Citations"
        ],
        burden_holder="Citing party",
        adversary_position="Reliance on outdated authority",
        counter_arguments=[
            "Older precedent may be controlling",
            "Recent decisions may not address the issue"
        ],
        resolution_strategy="Prefer recent authority unless older precedent is controlling.",
        entity_scope="All U.S. courts",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 1.1"
    ),
    DoctrineBlock(
        topic="Citation Relevance Ranking",
        keywords=["citation", "relevance", "ranking", "authority", "support"],
        conclusion_template="Citations should be ranked by relevance to the legal issue.",
        reasoning_framework=(
            "1. Identify the legal issue being addressed.\n"
            "2. Assess the relevance of each authority to the issue.\n"
            "3. Rank citations in order of relevance, with the most directly on-point authority first.\n"
            "4. Use signal words to indicate the strength of support.\n"
            "5. Normalize format for consistency.\n"
            "6. Cross-reference with court rules for any additional requirements.\n"
            "7. Document any deviations from relevance ranking and the reason.\n"
            "8. Confirm that all relevant authority is cited.\n"
            "9. Review for inadvertent omission of relevant authority.\n"
            "10. Finalize citation ranking before submission."
        ),
        key_factors=[
            "Directness of authority",
            "Strength of support",
            "Clarity",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 1.4",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper ranking of citations",
        counter_arguments=[
            "Less relevant authority may provide useful context",
            "Some courts may require chronological order"
        ],
        resolution_strategy="Rank citations by relevance unless court rules dictate otherwise.",
        entity_scope="All U.S. courts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 1.4"
    ),
    # Additional 20+ doctrine blocks with real content follow:
    DoctrineBlock(
        topic="Short Form Citations",
        keywords=["short form", "id.", "supra", "infra", "citation", "format"],
        conclusion_template="Short form citations may be used after full citation per Bluebook Rule 4.",
        reasoning_framework=(
            "1. Provide a full citation to the authority at first mention.\n"
            "2. Use 'id.' for immediately preceding authority if no intervening citations exist.\n"
            "3. Use 'supra' and 'infra' for previously cited authorities, with correct pinpoint references.\n"
            "4. Ensure clarity by not overusing short forms.\n"
            "5. Normalize format for consistency.\n"
            "6. Cross-reference with court rules for any additional requirements.\n"
            "7. Document any deviations from standard short form usage and the reason.\n"
            "8. Confirm that short forms are not ambiguous.\n"
            "9. Review for clarity and ease of reference.\n"
            "10. Finalize short form citations before submission."
        ),
        key_factors=[
            "Clarity",
            "Proper use of short forms",
            "Avoidance of ambiguity",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 4",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Ambiguous or improper short form citation",
        counter_arguments=[
            "Full citation may be preferable for clarity",
            "Some courts may restrict short form usage"
        ],
        resolution_strategy="Use short forms only when unambiguous and permitted.",
        entity_scope="All U.S. courts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 4"
    ),
    DoctrineBlock(
        topic="Unpublished Opinions",
        keywords=["unpublished", "opinion", "citation", "precedent", "authority"],
        conclusion_template="Unpublished opinions may be cited only if permitted by court rules.",
        reasoning_framework=(
            "1. Determine if the opinion is unpublished or non-precedential.\n"
            "2. Check court rules for citation of unpublished opinions (e.g., Fed. R. App. P. 32.1).\n"
            "3. Include a parenthetical indicating unpublished status.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with local court rules for any additional requirements.\n"
            "6. Document any reliance on unpublished opinions and the reason.\n"
            "7. Confirm that unpublished opinions are not cited as binding precedent.\n"
            "8. Review for inadvertent citation of prohibited opinions.\n"
            "9. Update citations if publication status changes.\n"
            "10. Finalize unpublished opinion citations before submission."
        ),
        key_factors=[
            "Publication status",
            "Court rules",
            "Proper parenthetical",
            "Clarity"
        ],
        primary_authority=[
            "Fed. R. App. P. 32.1",
            "Bluebook Rule 10.8.1"
        ],
        burden_holder="Citing party",
        adversary_position="Improper citation of unpublished opinion",
        counter_arguments=[
            "Unpublished opinions may provide persuasive value",
            "Some courts prohibit citation"
        ],
        resolution_strategy="Cite unpublished opinions only if permitted and with proper notation.",
        entity_scope="Federal and state courts",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Fed. R. App. P. 32.1"
    ),
    DoctrineBlock(
        topic="Internet and Electronic Source Citations",
        keywords=["internet", "electronic", "online", "citation", "format", "URL"],
        conclusion_template="Citations to internet sources must include author, title, URL, and date per Bluebook Rule 18.",
        reasoning_framework=(
            "1. Identify the author and title of the online source.\n"
            "2. Provide the full URL and date of last visit.\n"
            "3. Use the format: Author, Title, Website (Date), URL.\n"
            "4. For sources without authors, use the organization as author.\n"
            "5. Normalize format for consistency.\n"
            "6. Cross-reference with court rules for any additional requirements.\n"
            "7. Document any deviations from standard format and the reason.\n"
            "8. Confirm that the URL is accurate and accessible.\n"
            "9. Update citations if the online source changes.\n"
            "10. Finalize internet citations before submission."
        ),
        key_factors=[
            "Author and title identification",
            "Accurate URL",
            "Date of access",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 18",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission of necessary elements or use of inaccessible sources",
        counter_arguments=[
            "Some courts may not accept internet citations",
            "Print sources may be preferred"
        ],
        resolution_strategy="Cite internet sources per Bluebook Rule 18 and ensure accessibility.",
        entity_scope="All U.S. courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 18"
    ),
    DoctrineBlock(
        topic="Foreign Law Citations",
        keywords=["foreign law", "citation", "format", "international", "authority"],
        conclusion_template="Citations to foreign law must conform to Bluebook Rule 20.",
        reasoning_framework=(
            "1. Identify the jurisdiction and official source for the foreign law.\n"
            "2. Use the format prescribed by Bluebook Rule 20, including language and translation if necessary.\n"
            "3. Provide parallel citations if available.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy of translation and citation.\n"
            "8. Update citations if the foreign law changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize foreign law citations before submission."
        ),
        key_factors=[
            "Jurisdiction identification",
            "Official source",
            "Translation accuracy",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 20",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or unclear foreign law citation",
        counter_arguments=[
            "Foreign law may be cited for persuasive value only",
            "Translation may be disputed"
        ],
        resolution_strategy="Cite foreign law per Bluebook Rule 20 and provide translation if needed.",
        entity_scope="All U.S. courts",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="Bluebook Rule 20"
    ),
    DoctrineBlock(
        topic="Treaty and International Agreement Citations",
        keywords=["treaty", "international agreement", "citation", "format", "authority"],
        conclusion_template="Citations to treaties must conform to Bluebook Rule 21.",
        reasoning_framework=(
            "1. Identify the official source for the treaty or agreement.\n"
            "2. Use the format prescribed by Bluebook Rule 21, including parties, title, and date.\n"
            "3. Provide parallel citations if available.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy of citation and parties.\n"
            "8. Update citations if the treaty status changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize treaty citations before submission."
        ),
        key_factors=[
            "Official source identification",
            "Parties and title",
            "Date of agreement",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 21",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete treaty citation",
        counter_arguments=[
            "Treaty status may be disputed",
            "Multiple sources may exist"
        ],
        resolution_strategy="Cite treaties per Bluebook Rule 21 and ensure completeness.",
        entity_scope="All U.S. courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 21"
    ),
    DoctrineBlock(
        topic="Legislative History Citations",
        keywords=["legislative history", "citation", "format", "authority", "congressional record"],
        conclusion_template="Citations to legislative history must follow Bluebook Rule 13.5.",
        reasoning_framework=(
            "1. Identify the type of legislative history (e.g., bill, report, hearing).\n"
            "2. Use the format prescribed by Bluebook Rule 13.5, including title, number, and date.\n"
            "3. Provide parallel citations if available.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if legislative history changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize legislative history citations before submission."
        ),
        key_factors=[
            "Type of legislative history",
            "Official source",
            "Date",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 13.5",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete legislative history citation",
        counter_arguments=[
            "Legislative history may be cited for context only",
            "Multiple sources may exist"
        ],
        resolution_strategy="Cite legislative history per Bluebook Rule 13.5 and ensure completeness.",
        entity_scope="All U.S. courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 13.5"
    ),
    DoctrineBlock(
        topic="Administrative Decision Citations",
        keywords=["administrative decision", "agency", "citation", "format", "authority"],
        conclusion_template="Citations to administrative decisions must conform to Bluebook Rule 14.3.",
        reasoning_framework=(
            "1. Identify the agency and official source for the decision.\n"
            "2. Use the format prescribed by Bluebook Rule 14.3, including party names, docket number, and date.\n"
            "3. Provide parallel citations if available.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the decision status changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize administrative decision citations before submission."
        ),
        key_factors=[
            "Agency identification",
            "Official source",
            "Docket number and date",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 14.3",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete administrative decision citation",
        counter_arguments=[
            "Agency decisions may be unpublished",
            "Multiple sources may exist"
        ],
        resolution_strategy="Cite administrative decisions per Bluebook Rule 14.3 and ensure completeness.",
        entity_scope="All U.S. courts",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="Bluebook Rule 14.3"
    ),
    DoctrineBlock(
        topic="Constitutional Provision Citations",
        keywords=["constitution", "provision", "citation", "format", "authority"],
        conclusion_template="Citations to constitutional provisions must follow Bluebook Rule 11.",
        reasoning_framework=(
            "1. Identify the constitution (U.S. or state) and the specific provision.\n"
            "2. Use the format prescribed by Bluebook Rule 11, including article, section, and clause.\n"
            "3. Abbreviate per Bluebook Table T16.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the provision changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize constitutional provision citations before submission."
        ),
        key_factors=[
            "Constitution identification",
            "Provision",
            "Proper abbreviation",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 11",
            "Bluebook Table T16"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete constitutional citation",
        counter_arguments=[
            "Provision may be cited for context only",
            "Multiple versions may exist"
        ],
        resolution_strategy="Cite constitutional provisions per Bluebook Rule 11 and Table T16.",
        entity_scope="All U.S. courts",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 11"
    ),
    DoctrineBlock(
        topic="Restatement and Uniform Law Citations",
        keywords=["restatement", "uniform law", "citation", "format", "authority"],
        conclusion_template="Citations to Restatements and Uniform Laws must follow Bluebook Rule 12.9.4.",
        reasoning_framework=(
            "1. Identify the Restatement or Uniform Law and the specific section.\n"
            "2. Use the format prescribed by Bluebook Rule 12.9.4, including title, section, and year.\n"
            "3. Abbreviate per Bluebook Table T1.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the Restatement or Uniform Law changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize citations before submission."
        ),
        key_factors=[
            "Title and section identification",
            "Proper abbreviation",
            "Year",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 12.9.4",
            "Bluebook Table T1"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete Restatement citation",
        counter_arguments=[
            "Restatement may be cited for persuasive value only",
            "Multiple versions may exist"
        ],
        resolution_strategy="Cite Restatements and Uniform Laws per Bluebook Rule 12.9.4 and Table T1.",
        entity_scope="All U.S. courts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 12.9.4"
    ),
    DoctrineBlock(
        topic="Legal Periodical Citations",
        keywords=["legal periodical", "journal", "law review", "citation", "format"],
        conclusion_template="Citations to legal periodicals must follow Bluebook Rule 16.",
        reasoning_framework=(
            "1. Identify the author, title, journal, volume, page, and year.\n"
            "2. Use the format prescribed by Bluebook Rule 16, including proper abbreviation of journal names.\n"
            "3. Abbreviate per Bluebook Table T13.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the article is republished or corrected.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize periodical citations before submission."
        ),
        key_factors=[
            "Author and title identification",
            "Journal abbreviation",
            "Volume, page, year",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 16",
            "Bluebook Table T13"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete periodical citation",
        counter_arguments=[
            "Article may be cited for context only",
            "Multiple versions may exist"
        ],
        resolution_strategy="Cite legal periodicals per Bluebook Rule 16 and Table T13.",
        entity_scope="All U.S. courts",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 16"
    ),
    DoctrineBlock(
        topic="Books and Treatises Citations",
        keywords=["book", "treatise", "citation", "format", "authority"],
        conclusion_template="Citations to books and treatises must follow Bluebook Rule 15.",
        reasoning_framework=(
            "1. Identify the author, title, edition, publisher, page, and year.\n"
            "2. Use the format prescribed by Bluebook Rule 15, including proper abbreviation of publisher names.\n"
            "3. Normalize format for consistency.\n"
            "4. Cross-reference with court rules for any additional requirements.\n"
            "5. Document any deviations from standard format and the reason.\n"
            "6. Confirm accuracy and completeness of citation.\n"
            "7. Update citations if the book is republished or corrected.\n"
            "8. Review for clarity and completeness.\n"
            "9. Finalize book and treatise citations before submission.\n"
            "10. Use pinpoint citations for specific references."
        ),
        key_factors=[
            "Author and title identification",
            "Edition and publisher",
            "Page and year",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 15",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete book citation",
        counter_arguments=[
            "Book may be cited for context only",
            "Multiple editions may exist"
        ],
        resolution_strategy="Cite books and treatises per Bluebook Rule 15.",
        entity_scope="All U.S. courts",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 15"
    ),
    DoctrineBlock(
        topic="Court Rule Citations",
        keywords=["court rule", "citation", "format", "authority", "federal rules"],
        conclusion_template="Citations to court rules must follow Bluebook Rule 12.9.3.",
        reasoning_framework=(
            "1. Identify the specific court rule and its official source.\n"
            "2. Use the format prescribed by Bluebook Rule 12.9.3, including rule number and abbreviation.\n"
            "3. Abbreviate per Bluebook Table T1.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the rule changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize court rule citations before submission."
        ),
        key_factors=[
            "Rule identification",
            "Proper abbreviation",
            "Clarity",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 12.9.3",
            "Bluebook Table T1"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete court rule citation",
        counter_arguments=[
            "Rule may be cited for context only",
            "Multiple versions may exist"
        ],
        resolution_strategy="Cite court rules per Bluebook Rule 12.9.3 and Table T1.",
        entity_scope="All U.S. courts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 12.9.3"
    ),
    DoctrineBlock(
        topic="Docket Number Citations",
        keywords=["docket number", "case", "citation", "format", "authority"],
        conclusion_template="Docket numbers may be included for clarity, especially for unpublished or pending cases.",
        reasoning_framework=(
            "1. Identify the case and its docket number.\n"
            "2. Include the docket number in the citation if the case is unpublished, pending, or otherwise difficult to locate.\n"
            "3. Place the docket number after the case name and before the court and year.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the docket number changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize docket number citations before submission."
        ),
        key_factors=[
            "Case identification",
            "Docket number accuracy",
            "Clarity",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 10.8.3",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission or inaccuracy of docket number",
        counter_arguments=[
            "Docket number may not be necessary for published cases",
            "Some courts may prohibit docket numbers"
        ],
        resolution_strategy="Include docket numbers when necessary for clarity.",
        entity_scope="All U.S. courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 10.8.3"
    ),
    DoctrineBlock(
        topic="Table and Appendix Citations",
        keywords=["table", "appendix", "citation", "format", "authority"],
        conclusion_template="Citations to tables and appendices must follow Bluebook Rule 6.2.",
        reasoning_framework=(
            "1. Identify the table or appendix and its official source.\n"
            "2. Use the format prescribed by Bluebook Rule 6.2, including title and location.\n"
            "3. Normalize format for consistency.\n"
            "4. Cross-reference with court rules for any additional requirements.\n"
            "5. Document any deviations from standard format and the reason.\n"
            "6. Confirm accuracy and completeness of citation.\n"
            "7. Update citations if the table or appendix changes.\n"
            "8. Review for clarity and completeness.\n"
            "9. Finalize table and appendix citations before submission.\n"
            "10. Use pinpoint citations for specific references."
        ),
        key_factors=[
            "Table or appendix identification",
            "Official source",
            "Clarity",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 6.2",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete table or appendix citation",
        counter_arguments=[
            "Table or appendix may be cited for context only",
            "Multiple versions may exist"
        ],
        resolution_strategy="Cite tables and appendices per Bluebook Rule 6.2.",
        entity_scope="All U.S. courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 6.2"
    ),
    DoctrineBlock(
        topic="Pending Legislation Citations",
        keywords=["pending legislation", "bill", "citation", "format", "authority"],
        conclusion_template="Citations to pending legislation must follow Bluebook Rule 13.2.",
        reasoning_framework=(
            "1. Identify the bill or resolution and its official source.\n"
            "2. Use the format prescribed by Bluebook Rule 13.2, including bill number, session, and year.\n"
            "3. Normalize format for consistency.\n"
            "4. Cross-reference with court rules for any additional requirements.\n"
            "5. Document any deviations from standard format and the reason.\n"
            "6. Confirm accuracy and completeness of citation.\n"
            "7. Update citations if the bill status changes.\n"
            "8. Review for clarity and completeness.\n"
            "9. Finalize pending legislation citations before submission.\n"
            "10. Use pinpoint citations for specific references."
        ),
        key_factors=[
            "Bill identification",
            "Official source",
            "Session and year",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 13.2",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete pending legislation citation",
        counter_arguments=[
            "Bill may be cited for context only",
            "Multiple versions may exist"
        ],
        resolution_strategy="Cite pending legislation per Bluebook Rule 13.2.",
        entity_scope="All U.S. courts",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="Bluebook Rule 13.2"
    ),
    DoctrineBlock(
        topic="Model Code Citations",
        keywords=["model code", "citation", "format", "authority", "model penal code"],
        conclusion_template="Citations to model codes must follow Bluebook Rule 12.9.5.",
        reasoning_framework=(
            "1. Identify the model code and the specific section.\n"
            "2. Use the format prescribed by Bluebook Rule 12.9.5, including title, section, and year.\n"
            "3. Abbreviate per Bluebook Table T1.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the model code changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize model code citations before submission."
        ),
        key_factors=[
            "Model code identification",
            "Section and year",
            "Proper abbreviation",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 12.9.5",
            "Bluebook Table T1"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete model code citation",
        counter_arguments=[
            "Model code may be cited for persuasive value only",
            "Multiple versions may exist"
        ],
        resolution_strategy="Cite model codes per Bluebook Rule 12.9.5 and Table T1.",
        entity_scope="All U.S. courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 12.9.5"
    ),
    DoctrineBlock(
        topic="Amicus Brief Citations",
        keywords=["amicus brief", "citation", "format", "authority", "friend of the court"],
        conclusion_template="Citations to amicus briefs must follow Bluebook Rule 10.8.4.",
        reasoning_framework=(
            "1. Identify the amicus brief and the case in which it was filed.\n"
            "2. Use the format prescribed by Bluebook Rule 10.8.4, including case name, docket number, and court.\n"
            "3. Normalize format for consistency.\n"
            "4. Cross-reference with court rules for any additional requirements.\n"
            "5. Document any deviations from standard format and the reason.\n"
            "6. Confirm accuracy and completeness of citation.\n"
            "7. Update citations if the brief status changes.\n"
            "8. Review for clarity and completeness.\n"
            "9. Finalize amicus brief citations before submission.\n"
            "10. Use pinpoint citations for specific references."
        ),
        key_factors=[
            "Brief identification",
            "Case and docket number",
            "Court",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 10.8.4",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete amicus brief citation",
        counter_arguments=[
            "Brief may be cited for context only",
            "Multiple versions may exist"
        ],
        resolution_strategy="Cite amicus briefs per Bluebook Rule 10.8.4.",
        entity_scope="All U.S. courts",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="Bluebook Rule 10.8.4"
    ),
    DoctrineBlock(
        topic="En Banc and Per Curiam Decision Citations",
        keywords=["en banc", "per curiam", "decision", "citation", "format"],
        conclusion_template="Citations must indicate en banc or per curiam status per Bluebook Rule 10.6.2.",
        reasoning_framework=(
            "1. Identify if the decision was rendered en banc or per curiam.\n"
            "2. Indicate en banc status in parenthesis after the court and year.\n"
            "3. Indicate per curiam status as required by Bluebook Rule 10.6.2.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the decision status changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize en banc and per curiam citations before submission."
        ),
        key_factors=[
            "Decision status identification",
            "Proper parenthetical",
            "Clarity",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 10.6.2",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission or inaccuracy of en banc or per curiam status",
        counter_arguments=[
            "Status may be clear from context",
            "Some courts may not require notation"
        ],
        resolution_strategy="Indicate en banc or per curiam status per Bluebook Rule 10.6.2.",
        entity_scope="All U.S. courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Bluebook Rule 10.6.2"
    ),
    DoctrineBlock(
        topic="Slip Opinion Citations",
        keywords=["slip opinion", "citation", "format", "authority", "pending"],
        conclusion_template="Citations to slip opinions must follow Bluebook Rule 10.8.1.",
        reasoning_framework=(
            "1. Identify the slip opinion and its official source.\n"
            "2. Use the format prescribed by Bluebook Rule 10.8.1, including case name, docket number, and court.\n"
            "3. Indicate slip opinion status in parenthesis.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the slip opinion is published.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize slip opinion citations before submission."
        ),
        key_factors=[
            "Slip opinion identification",
            "Proper parenthetical",
            "Clarity",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 10.8.1",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete slip opinion citation",
        counter_arguments=[
            "Slip opinion may be cited for context only",
            "Some courts may prohibit slip opinion citations"
        ],
        resolution_strategy="Cite slip opinions per Bluebook Rule 10.8.1.",
        entity_scope="All U.S. courts",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="Bluebook Rule 10.8.1"
    ),
    DoctrineBlock(
        topic="Statutory Note Citations",
        keywords=["statutory note", "citation", "format", "authority", "note"],
        conclusion_template="Citations to statutory notes must follow Bluebook Rule 12.9.2.",
        reasoning_framework=(
            "1. Identify the statute and the specific note being cited.\n"
            "2. Use the format prescribed by Bluebook Rule 12.9.2, including title, section, and note.\n"
            "3. Normalize format for consistency.\n"
            "4. Cross-reference with court rules for any additional requirements.\n"
            "5. Document any deviations from standard format and the reason.\n"
            "6. Confirm accuracy and completeness of citation.\n"
            "7. Update citations if the note changes.\n"
            "8. Review for clarity and completeness.\n"
            "9. Finalize statutory note citations before submission.\n"
            "10. Use pinpoint citations for specific references."
        ),
        key_factors=[
            "Statute and note identification",
            "Proper format",
            "Clarity",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 12.9.2",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete statutory note citation",
        counter_arguments=[
            "Note may be cited for context only",
            "Multiple versions may exist"
        ],
        resolution_strategy="Cite statutory notes per Bluebook Rule 12.9.2.",
        entity_scope="All U.S. courts",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="Bluebook Rule 12.9.2"
    ),
    DoctrineBlock(
        topic="Pending Case Citations",
        keywords=["pending case", "citation", "format", "authority", "docket number"],
        conclusion_template="Citations to pending cases must include docket number and court.",
        reasoning_framework=(
            "1. Identify the pending case and its docket number.\n"
            "2. Include the court and status in the citation.\n"
            "3. Use the format prescribed by Bluebook Rule 10.8.3.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the case status changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize pending case citations before submission."
        ),
        key_factors=[
            "Case identification",
            "Docket number and court",
            "Status",
            "Clarity"
        ],
        primary_authority=[
            "Bluebook Rule 10.8.3",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Improper or incomplete pending case citation",
        counter_arguments=[
            "Case may be cited for context only",
            "Some courts may prohibit pending case citations"
        ],
        resolution_strategy="Cite pending cases per Bluebook Rule 10.8.3.",
        entity_scope="All U.S. courts",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="Bluebook Rule 10.8.3"
    ),
    DoctrineBlock(
        topic="Rehearing and Reconsideration Citations",
        keywords=["rehearing", "reconsideration", "citation", "format", "authority"],
        conclusion_template="Citations must indicate rehearing or reconsideration status per Bluebook Rule 10.7.1.",
        reasoning_framework=(
            "1. Identify if the decision is subject to rehearing or reconsideration.\n"
            "2. Indicate status in parenthesis after the main citation.\n"
            "3. Use the format prescribed by Bluebook Rule 10.7.1.\n"
            "4. Normalize format for consistency.\n"
            "5. Cross-reference with court rules for any additional requirements.\n"
            "6. Document any deviations from standard format and the reason.\n"
            "7. Confirm accuracy and completeness of citation.\n"
            "8. Update citations if the status changes.\n"
            "9. Review for clarity and completeness.\n"
            "10. Finalize rehearing and reconsideration citations before submission."
        ),
        key_factors=[
            "Decision status",
            "Proper parenthetical",
            "Clarity",
            "Consistency"
        ],
        primary_authority=[
            "Bluebook Rule 10.7.1",
            "Local court rules"
        ],
        burden_holder="Citing party",
        adversary_position="Omission or inaccuracy of rehearing or reconsideration status",
        counter_arguments=[
            "Status may be clear from context",
            "Some courts may not require notation"
        ],
        resolution_strategy="Indicate rehearing or reconsideration status per Bluebook Rule 10.7.1.",
        entity_scope="All U.S. courts",
        confidence=0.93,
        confidence_zone="Medium",
        controlling_precedent="Bluebook Rule 10.7.1"
    ),
    DoctrineBlock(
        topic="Errata and Correction Citations",
        keywords=["errata", "correction", "citation", "format", "authority"],
        conclusion_template="Citations must indicate errata or correction status per Bluebook Rule 10.7.2.",
        reasoning_framework=(
            "1. Identify if the authority has been corrected or has errata issued.\n"