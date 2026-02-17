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
        topic="UCC 2-201 Statute of Frauds",
        keywords=["UCC", "Statute of Frauds", "writing requirement", "goods", "merchant", "contract formation"],
        conclusion_template="A contract for the sale of goods priced at $500 or more is unenforceable unless there is a writing sufficient to indicate that a contract has been made between the parties and signed by the party against whom enforcement is sought.",
        reasoning_framework=(
            "1. Determine if the transaction involves the sale of goods (UCC Article 2 applies).\n"
            "2. Assess whether the price of goods is $500 or more.\n"
            "3. Examine if there is a writing that evidences the contract and is signed by the party to be charged.\n"
            "4. Consider exceptions: merchant's confirmation, specially manufactured goods, admission in court, or part performance.\n"
            "5. Analyze whether the writing contains a quantity term and is otherwise sufficient.\n"
            "6. Evaluate if any defenses to enforcement exist (e.g., fraud, duress).\n"
            "7. Conclude enforceability based on compliance with UCC 2-201 and exceptions."
        ),
        key_factors=[
            "Sale of goods",
            "Price threshold ($500 or more)",
            "Existence of a writing",
            "Signature of party to be charged",
            "Exceptions applicability"
        ],
        primary_authority=["UCC §2-201", "Official Comments to UCC §2-201"],
        burden_holder="Party seeking enforcement",
        adversary_position="No enforceable contract exists due to lack of signed writing",
        counter_arguments=[
            "Merchant's confirmation exception applies",
            "Part performance exception applies",
            "Admission in pleadings or court"
        ],
        resolution_strategy="Apply UCC 2-201 and analyze exceptions; if none apply, contract is unenforceable.",
        entity_scope="Merchants and non-merchants in sale of goods contracts",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Bazak Int'l Corp. v. Mast Indus., Inc., 73 N.Y.2d 113 (1989)"
    ),
    DoctrineBlock(
        topic="UCC 2-207 Battle of Forms",
        keywords=["UCC", "Battle of Forms", "acceptance", "additional terms", "different terms", "contract formation"],
        conclusion_template="A definite and seasonable expression of acceptance or a written confirmation operates as an acceptance even though it states terms additional to or different from those offered, unless acceptance is expressly made conditional on assent to the additional or different terms.",
        reasoning_framework=(
            "1. Identify if the transaction involves an exchange of forms (offer and acceptance) under UCC Article 2.\n"
            "2. Determine if the response is a definite and seasonable expression of acceptance.\n"
            "3. Assess whether acceptance is expressly conditional on assent to new terms.\n"
            "4. If not conditional, a contract is formed; analyze the status of additional/different terms.\n"
            "5. If both parties are merchants, additional terms become part of the contract unless they materially alter it, offeror objects, or offer limits acceptance.\n"
            "6. Different terms may be subject to the 'knockout rule' or replaced by UCC gap-fillers.\n"
            "7. If acceptance is conditional, no contract unless offeror expressly assents.\n"
            "8. If conduct by both parties recognizes a contract, UCC 2-207(3) applies and terms consist of agreed terms plus UCC gap-fillers."
        ),
        key_factors=[
            "Definite and seasonable acceptance",
            "Expressly conditional language",
            "Merchant status of parties",
            "Material alteration",
            "Objection to terms"
        ],
        primary_authority=["UCC §2-207", "Dorton v. Collins & Aikman Corp., 453 F.2d 1161 (6th Cir. 1972)"],
        burden_holder="Party asserting inclusion/exclusion of terms",
        adversary_position="Additional/different terms are not part of the contract",
        counter_arguments=[
            "Terms materially alter contract",
            "Timely objection made",
            "Offer expressly limits acceptance"
        ],
        resolution_strategy="Apply UCC 2-207 analysis to determine contract formation and which terms control.",
        entity_scope="Merchants and non-merchants in sale of goods contracts",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Step-Saver Data Sys., Inc. v. Wyse Tech., 939 F.2d 91 (3d Cir. 1991)"
    ),
    DoctrineBlock(
        topic="UCC 2-302 Unconscionability",
        keywords=["UCC", "Unconscionability", "contract terms", "procedural", "substantive", "remedies"],
        conclusion_template="If a court finds a contract or any clause to have been unconscionable at the time it was made, it may refuse to enforce the contract, enforce the remainder without the unconscionable clause, or limit the application of any unconscionable clause.",
        reasoning_framework=(
            "1. Identify the allegedly unconscionable term or contract.\n"
            "2. Analyze procedural unconscionability: Was there oppression, surprise, or unequal bargaining power?\n"
            "3. Analyze substantive unconscionability: Are the terms overly harsh, one-sided, or unreasonably favorable to one party?\n"
            "4. Consider the context at the time of contract formation.\n"
            "5. Evaluate whether both procedural and substantive unconscionability are present (most jurisdictions require both).\n"
            "6. Assess the availability of remedies: refuse enforcement, sever the clause, or limit its application.\n"
            "7. Consider public policy and the intent of the UCC to prevent unfair surprise and oppression."
        ),
        key_factors=[
            "Procedural unconscionability",
            "Substantive unconscionability",
            "Bargaining power",
            "Clarity of terms",
            "Public policy"
        ],
        primary_authority=["UCC §2-302", "Williams v. Walker-Thomas Furniture Co., 350 F.2d 445 (D.C. Cir. 1965)"],
        burden_holder="Party seeking to avoid enforcement",
        adversary_position="Contract was entered into voluntarily and terms are not unconscionable",
        counter_arguments=[
            "No procedural or substantive unconscionability",
            "Parties had equal bargaining power",
            "Terms are standard in the industry"
        ],
        resolution_strategy="Court evaluates both procedural and substantive unconscionability and applies appropriate remedy.",
        entity_scope="All parties to contracts for the sale of goods",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Williams v. Walker-Thomas Furniture Co., 350 F.2d 445 (D.C. Cir. 1965)"
    ),
    DoctrineBlock(
        topic="UCC 2-615 Commercial Impracticability",
        keywords=["UCC", "Commercial Impracticability", "excuse", "performance", "unforeseen event", "allocation"],
        conclusion_template="Delay in delivery or non-delivery by a seller is not a breach if performance has been made impracticable by the occurrence of a contingency the non-occurrence of which was a basic assumption of the contract.",
        reasoning_framework=(
            "1. Identify the event causing non-performance or delay.\n"
            "2. Determine if the event was unforeseen and its non-occurrence was a basic assumption of the contract.\n"
            "3. Assess whether the event has made performance commercially impracticable, not merely more difficult or expensive.\n"
            "4. Evaluate if the seller gave seasonable notice to the buyer of the delay or non-delivery.\n"
            "5. If only part of the seller's capacity is affected, assess whether allocation among customers was fair and reasonable.\n"
            "6. Consider whether the risk was allocated by agreement or custom.\n"
            "7. Analyze whether the seller made reasonable efforts to avoid or mitigate the impact."
        ),
        key_factors=[
            "Unforeseen event",
            "Basic assumption of contract",
            "Degree of impracticability",
            "Notice to buyer",
            "Allocation among customers"
        ],
        primary_authority=["UCC §2-615", "Official Comments to UCC §2-615"],
        burden_holder="Party seeking excuse from performance",
        adversary_position="Event was foreseeable or risk was assumed",
        counter_arguments=[
            "Event was foreseeable",
            "Risk was allocated to the party",
            "Performance is still possible"
        ],
        resolution_strategy="Apply UCC 2-615 to determine if excuse is warranted and whether allocation was proper.",
        entity_scope="Sellers in contracts for the sale of goods",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Eastern Air Lines, Inc. v. Gulf Oil Corp., 415 F. Supp. 429 (S.D. Fla. 1975)"
    ),
    DoctrineBlock(
        topic="SaaS License vs Sale Distinction",
        keywords=["SaaS", "license", "sale", "software", "ownership", "intellectual property"],
        conclusion_template="A SaaS agreement typically constitutes a license to use software rather than a sale of goods, affecting the application of UCC Article 2 and the allocation of rights and obligations.",
        reasoning_framework=(
            "1. Examine the nature of the transaction: Is the customer obtaining a copy of software or access to a hosted service?\n"
            "2. Determine whether the agreement transfers ownership or merely grants a right to use.\n"
            "3. Assess the language of the contract for terms such as 'license', 'subscription', or 'sale'.\n"
            "4. Consider the intent of the parties and the economic realities of the transaction.\n"
            "5. Analyze the implications for UCC Article 2 applicability (sale of goods vs. service).\n"
            "6. Evaluate the impact on warranties, remedies, and intellectual property rights.\n"
            "7. Consider relevant case law and industry practice."
        ),
        key_factors=[
            "Nature of transaction",
            "Transfer of ownership",
            "Contract language",
            "Intent of parties",
            "Industry standards"
        ],
        primary_authority=["UCC Article 2", "ProCD, Inc. v. Zeidenberg, 86 F.3d 1447 (7th Cir. 1996)"],
        burden_holder="Party asserting sale or license characterization",
        adversary_position="Agreement constitutes a sale of goods, not a license",
        counter_arguments=[
            "Customer receives a copy and can transfer it",
            "Economic realities support sale characterization",
            "UCC Article 2 applies"
        ],
        resolution_strategy="Analyze transaction structure and contract terms to determine proper classification.",
        entity_scope="Software vendors and customers in SaaS transactions",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="ProCD, Inc. v. Zeidenberg, 86 F.3d 1447 (7th Cir. 1996)"
    ),
    DoctrineBlock(
        topic="Force Majeure Clauses",
        keywords=["force majeure", "excuse", "performance", "unforeseeable event", "contractual allocation", "risk"],
        conclusion_template="A force majeure clause may excuse a party's performance if an enumerated unforeseeable event occurs, provided the event is beyond the party's control and directly prevents performance.",
        reasoning_framework=(
            "1. Identify the force majeure clause and its scope in the contract.\n"
            "2. Determine whether the event in question is covered by the clause (e.g., acts of God, war, pandemic).\n"
            "3. Assess whether the event was unforeseeable and beyond the party's control.\n"
            "4. Evaluate the causal connection between the event and the inability to perform.\n"
            "5. Consider any notice requirements and whether they were met.\n"
            "6. Analyze whether the party made reasonable efforts to mitigate the impact.\n"
            "7. Examine the duration and effect of the force majeure event on contractual obligations."
        ),
        key_factors=[
            "Scope of force majeure clause",
            "Enumerated events",
            "Foreseeability",
            "Causal connection",
            "Notice and mitigation"
        ],
        primary_authority=["Contract language", "Kel Kim Corp. v. Central Markets, Inc., 70 N.Y.2d 900 (1987)"],
        burden_holder="Party invoking force majeure",
        adversary_position="Event is not covered or does not excuse performance",
        counter_arguments=[
            "Event was foreseeable",
            "Party failed to mitigate",
            "Performance is still possible"
        ],
        resolution_strategy="Interpret contract language and apply to facts to determine if performance is excused.",
        entity_scope="All commercial contract parties",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Kel Kim Corp. v. Central Markets, Inc., 70 N.Y.2d 900 (1987)"
    ),
    DoctrineBlock(
        topic="Limitation of Liability Clauses",
        keywords=["limitation of liability", "damages", "cap", "exclusion", "enforceability", "public policy"],
        conclusion_template="Limitation of liability clauses are generally enforceable unless unconscionable, against public policy, or precluded by statute.",
        reasoning_framework=(
            "1. Identify the limitation of liability clause and its scope (e.g., cap on damages, exclusion of consequential damages).\n"
            "2. Assess whether the clause was negotiated and conspicuous.\n"
            "3. Determine if the limitation is reasonable and not unconscionable.\n"
            "4. Evaluate whether the limitation violates public policy (e.g., excludes liability for gross negligence or willful misconduct).\n"
            "5. Consider statutory restrictions (e.g., UCC 2-719).\n"
            "6. Analyze whether the limitation deprives a party of the essential purpose of the contract.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Scope and conspicuousness of clause",
            "Negotiation and assent",
            "Reasonableness",
            "Public policy considerations",
            "Statutory restrictions"
        ],
        primary_authority=["UCC §2-719", "New York Gen. Oblig. Law § 5-322.1", "Metropolitan Life Ins. Co. v. Noble Lowndes Int'l, Inc., 84 N.Y.2d 430 (1994)"],
        burden_holder="Party seeking to enforce or avoid limitation",
        adversary_position="Limitation is unenforceable due to unconscionability or public policy",
        counter_arguments=[
            "Clause is unconscionable",
            "Violates public policy",
            "Deprives party of essential purpose"
        ],
        resolution_strategy="Analyze clause under UCC and public policy; enforce if reasonable and not unconscionable.",
        entity_scope="All commercial contract parties",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Metropolitan Life Ins. Co. v. Noble Lowndes Int'l, Inc., 84 N.Y.2d 430 (1994)"
    ),
    DoctrineBlock(
        topic="Indemnification Clauses",
        keywords=["indemnification", "hold harmless", "third-party claims", "scope", "enforceability"],
        conclusion_template="Indemnification clauses allocate risk by requiring one party to compensate the other for certain losses or claims, subject to limitations imposed by law and the contract.",
        reasoning_framework=(
            "1. Identify the indemnification clause and its scope (e.g., third-party claims, direct damages).\n"
            "2. Determine the types of claims and losses covered (e.g., negligence, breach, IP infringement).\n"
            "3. Assess whether the clause is clear, specific, and conspicuous.\n"
            "4. Evaluate any limitations or exclusions (e.g., gross negligence, willful misconduct).\n"
            "5. Consider statutory or public policy restrictions on indemnification.\n"
            "6. Analyze notice and defense obligations for indemnified claims.\n"
            "7. Review relevant case law for enforceability and interpretation."
        ),
        key_factors=[
            "Scope of indemnification",
            "Types of claims covered",
            "Clarity and specificity",
            "Limitations and exclusions",
            "Notice and defense obligations"
        ],
        primary_authority=["Contract language", "New York Gen. Oblig. Law § 5-322.1", "Hooper Assocs., Ltd. v. AGS Computers, Inc., 74 N.Y.2d 487 (1989)"],
        burden_holder="Party seeking indemnification",
        adversary_position="Indemnification does not cover the claim or is unenforceable",
        counter_arguments=[
            "Claim is outside scope",
            "Clause is ambiguous",
            "Prohibited by statute"
        ],
        resolution_strategy="Interpret clause in light of contract language and applicable law; enforce if clear and lawful.",
        entity_scope="All commercial contract parties",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Hooper Assocs., Ltd. v. AGS Computers, Inc., 74 N.Y.2d 487 (1989)"
    ),
    DoctrineBlock(
        topic="Warranty Disclaimers",
        keywords=["warranty disclaimer", "UCC", "merchantability", "fitness for purpose", "conspicuousness"],
        conclusion_template="Warranty disclaimers are enforceable if they are conspicuous, specific, and comply with statutory requirements.",
        reasoning_framework=(
            "1. Identify the warranty disclaimer and its scope (e.g., merchantability, fitness for a particular purpose).\n"
            "2. Assess whether the disclaimer is conspicuous and in writing if required (UCC 2-316).\n"
            "3. Determine if the disclaimer uses specific language (e.g., 'AS IS', 'WITH ALL FAULTS').\n"
            "4. Evaluate whether the disclaimer is consistent with express warranties.\n"
            "5. Consider statutory restrictions and public policy.\n"
            "6. Analyze whether the disclaimer was negotiated and assented to by the parties.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Conspicuousness",
            "Specificity of language",
            "Consistency with express warranties",
            "Negotiation and assent",
            "Statutory compliance"
        ],
        primary_authority=["UCC §2-316", "Official Comments to UCC §2-316"],
        burden_holder="Party seeking to enforce disclaimer",
        adversary_position="Disclaimer is ineffective or inconsistent with express warranties",
        counter_arguments=[
            "Disclaimer is not conspicuous",
            "Fails to use required language",
            "Conflicts with express warranties"
        ],
        resolution_strategy="Apply UCC 2-316 and interpret disclaimer in context of the contract.",
        entity_scope="All commercial contract parties",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="CBS Inc. v. Ziff-Davis Pub. Co., 75 N.Y.2d 496 (1990)"
    ),
    DoctrineBlock(
        topic="Choice of Law and Forum Selection",
        keywords=["choice of law", "forum selection", "jurisdiction", "venue", "enforceability"],
        conclusion_template="Choice of law and forum selection clauses are generally enforceable if reasonable and not contrary to public policy.",
        reasoning_framework=(
            "1. Identify the choice of law and forum selection clauses in the contract.\n"
            "2. Assess whether the clauses were negotiated and agreed to by both parties.\n"
            "3. Determine if the selected law or forum has a substantial relationship to the parties or transaction.\n"
            "4. Evaluate whether enforcement would be unreasonable, unjust, or against public policy.\n"
            "5. Consider statutory restrictions and relevant case law.\n"
            "6. Analyze whether the clause was obtained by fraud or overreaching.\n"
            "7. Review the effect of the clause on the parties' substantive rights."
        ),
        key_factors=[
            "Negotiation and assent",
            "Substantial relationship to forum/law",
            "Reasonableness",
            "Public policy considerations",
            "Absence of fraud or overreaching"
        ],
        primary_authority=["The Bremen v. Zapata Off-Shore Co., 407 U.S. 1 (1972)", "UCC §1-301"],
        burden_holder="Party seeking to enforce or avoid clause",
        adversary_position="Clause is unenforceable due to unreasonableness or public policy",
        counter_arguments=[
            "Forum is inconvenient or unrelated",
            "Clause was not negotiated",
            "Violates public policy"
        ],
        resolution_strategy="Apply contract and public policy analysis; enforce if reasonable and lawful.",
        entity_scope="All commercial contract parties",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="The Bremen v. Zapata Off-Shore Co., 407 U.S. 1 (1972)"
    ),
    DoctrineBlock(
        topic="Non-Disclosure Agreements (NDAs)",
        keywords=["NDA", "confidentiality", "trade secrets", "enforceability", "scope", "duration"],
        conclusion_template="NDAs are enforceable if they protect legitimate business interests, are reasonable in scope and duration, and do not violate public policy.",
        reasoning_framework=(
            "1. Identify the scope of information covered by the NDA.\n"
            "2. Assess whether the information is truly confidential or a trade secret.\n"
            "3. Determine the duration and geographic scope of the NDA.\n"
            "4. Evaluate whether the NDA is necessary to protect a legitimate business interest.\n"
            "5. Consider whether the NDA is overbroad or unduly restrictive.\n"
            "6. Analyze public policy implications and statutory requirements.\n"
            "7. Review remedies for breach and enforceability under state law."
        ),
        key_factors=[
            "Legitimate business interest",
            "Scope of confidential information",
            "Duration and geographic scope",
            "Reasonableness",
            "Public policy"
        ],
        primary_authority=["Uniform Trade Secrets Act", "Restatement (Third) of Unfair Competition § 41"],
        burden_holder="Party seeking to enforce NDA",
        adversary_position="NDA is overbroad or unenforceable",
        counter_arguments=[
            "Information is not confidential",
            "Scope is unreasonable",
            "Violates public policy"
        ],
        resolution_strategy="Interpret NDA in light of business needs and legal standards; enforce if reasonable.",
        entity_scope="All parties to NDAs",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Ashland Mgmt. Inc. v. Janien, 82 N.Y.2d 395 (1993)"
    ),
    DoctrineBlock(
        topic="Material Breach vs Minor Breach",
        keywords=["material breach", "minor breach", "substantial performance", "remedies", "termination"],
        conclusion_template="A material breach excuses the non-breaching party from further performance and may justify termination, while a minor breach does not.",
        reasoning_framework=(
            "1. Identify the alleged breach and its impact on the contract.\n"
            "2. Assess whether the breach goes to the essence of the contract or deprives the non-breaching party of the benefit of the bargain.\n"
            "3. Consider the extent to which the injured party can be compensated for the breach.\n"
            "4. Evaluate whether the breaching party will suffer forfeiture.\n"
            "5. Analyze the likelihood of cure and good faith of the breaching party.\n"
            "6. Review the effect on the contract as a whole.\n"
            "7. Apply the Restatement (Second) of Contracts § 241 factors."
        ),
        key_factors=[
            "Nature and gravity of breach",
            "Benefit of the bargain",
            "Possibility of cure",
            "Good faith",
            "Effect on contract"
        ],
        primary_authority=["Restatement (Second) of Contracts § 241", "Jacob & Youngs v. Kent, 230 N.Y. 239 (1921)"],
        burden_holder="Party alleging material breach",
        adversary_position="Breach is minor and does not justify termination",
        counter_arguments=[
            "Breach is not material",
            "Substantial performance exists",
            "Damages are adequate remedy"
        ],
        resolution_strategy="Apply materiality factors and determine appropriate remedy.",
        entity_scope="All commercial contract parties",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Jacob & Youngs v. Kent, 230 N.Y. 239 (1921)"
    ),
    DoctrineBlock(
        topic="Anti-Assignment Clauses",
        keywords=["anti-assignment", "assignment", "delegation", "enforceability", "novation"],
        conclusion_template="Anti-assignment clauses restrict or prohibit the transfer of contractual rights or obligations, and are generally enforceable unless contrary to law or public policy.",
        reasoning_framework=(
            "1. Identify the anti-assignment clause and its scope (rights, obligations, or both).\n"
            "2. Determine whether the assignment in question falls within the prohibition.\n"
            "3. Assess whether the clause prohibits assignment of rights, delegation of duties, or both.\n"
            "4. Evaluate whether the assignment is permitted by law (e.g., assignment of payment rights).\n"
            "5. Consider whether the clause requires consent or is absolute.\n"
            "6. Analyze the effect of a prohibited assignment (void, voidable, or breach).\n"
            "7. Review relevant statutory and case law."
        ),
        key_factors=[
            "Scope of anti-assignment clause",
            "Type of assignment",
            "Consent requirements",
            "Statutory exceptions",
            "Effect of breach"
        ],
        primary_authority=["Restatement (Second) of Contracts § 322", "UCC §2-210"],
        burden_holder="Party seeking to enforce or avoid assignment",
        adversary_position="Assignment is permitted or clause is unenforceable",
        counter_arguments=[
            "Clause does not cover this assignment",
            "Statutory exception applies",
            "Clause is contrary to public policy"
        ],
        resolution_strategy="Interpret clause and apply statutory and case law to determine enforceability.",
        entity_scope="All commercial contract parties",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Bel-Ray Co., Inc. v. Chemrite (Pty) Ltd., 181 F.3d 435 (3d Cir. 1999)"
    ),
    DoctrineBlock(
        topic="Most Favored Nation (MFN) Clauses",
        keywords=["most favored nation", "MFN", "pricing", "terms", "discrimination", "enforceability"],
        conclusion_template="MFN clauses require a party to provide terms no less favorable than those offered to any other party, and are generally enforceable unless anti-competitive or contrary to public policy.",
        reasoning_framework=(
            "1. Identify the MFN clause and its scope (pricing, terms, services).\n"
            "2. Assess whether the clause is clear, specific, and mutually agreed upon.\n"
            "3. Determine the effect of the clause on competition and market dynamics.\n"
            "4. Evaluate whether the clause is anti-competitive or violates antitrust laws.\n"
            "5. Consider public policy implications and statutory restrictions.\n"
            "6. Analyze the remedies for breach of the MFN clause.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Scope and specificity",
            "Effect on competition",
            "Mutual assent",
            "Public policy considerations",
            "Remedies for breach"
        ],
        primary_authority=["Contract language", "Blue Cross Blue Shield v. Marshfield Clinic, 65 F.3d 1406 (7th Cir. 1995)"],
        burden_holder="Party seeking to enforce MFN clause",
        adversary_position="Clause is anti-competitive or unenforceable",
        counter_arguments=[
            "Clause violates antitrust law",
            "Is ambiguous or overbroad",
            "Contrary to public policy"
        ],
        resolution_strategy="Interpret clause and analyze under antitrust and contract law.",
        entity_scope="All commercial contract parties",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Blue Cross Blue Shield v. Marshfield Clinic, 65 F.3d 1406 (7th Cir. 1995)"
    ),
    DoctrineBlock(
        topic="CISG Application to International Sales",
        keywords=["CISG", "international sales", "United Nations Convention", "opt-out", "applicability"],
        conclusion_template="The CISG applies to contracts for the sale of goods between parties whose places of business are in different signatory states, unless expressly excluded.",
        reasoning_framework=(
            "1. Determine if both parties have places of business in different CISG signatory countries.\n"
            "2. Assess whether the contract is for the sale of goods (not services or excluded goods).\n"
            "3. Examine whether the parties have opted out of the CISG explicitly in the contract.\n"
            "4. Evaluate the scope of the CISG and any exclusions under Article 2.\n"
            "5. Consider the effect of choice of law clauses on CISG applicability.\n"
            "6. Analyze the interplay between CISG and domestic law.\n"
            "7. Review relevant case law and interpretative sources."
        ),
        key_factors=[
            "Places of business in signatory countries",
            "Nature of contract (sale of goods)",
            "Opt-out language",
            "Choice of law",
            "CISG exclusions"
        ],
        primary_authority=["CISG Articles 1-6", "Delchi Carrier SpA v. Rotorex Corp., 71 F.3d 1024 (2d Cir. 1995)"],
        burden_holder="Party asserting or denying CISG applicability",
        adversary_position="CISG does not apply due to opt-out or exclusion",
        counter_arguments=[
            "Parties opted out",
            "Contract is not for sale of goods",
            "Domestic law governs"
        ],
        resolution_strategy="Analyze contract and parties' locations; apply CISG if requirements are met and not excluded.",
        entity_scope="Parties to international sales contracts",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Delchi Carrier SpA v. Rotorex Corp., 71 F.3d 1024 (2d Cir. 1995)"
    ),
    DoctrineBlock(
        topic="Master Service Agreement (MSA) Structure",
        keywords=["MSA", "master service agreement", "structure", "SOW", "governing terms"],
        conclusion_template="An MSA establishes the general terms and conditions governing multiple transactions or statements of work (SOWs) between parties.",
        reasoning_framework=(
            "1. Identify the MSA and its relationship to subordinate documents (SOWs, purchase orders).\n"
            "2. Assess the scope of the MSA and which terms are incorporated into each transaction.\n"
            "3. Determine the process for issuing and accepting SOWs under the MSA.\n"
            "4. Evaluate the hierarchy of documents in case of conflict (MSA vs. SOW).\n"
            "5. Analyze amendment and modification procedures.\n"
            "6. Consider the duration, termination, and renewal provisions of the MSA.\n"
            "7. Review relevant case law and industry standards."
        ),
        key_factors=[
            "Relationship between MSA and SOWs",
            "Scope of governing terms",
            "Document hierarchy",
            "Amendment procedures",
            "Duration and termination"
        ],
        primary_authority=["Contract language", "Industry practice"],
        burden_holder="Party asserting or disputing MSA terms",
        adversary_position="SOW or subordinate document controls",
        counter_arguments=[
            "Conflicting terms in SOW",
            "MSA does not govern specific transaction",
            "Amendment not properly executed"
        ],
        resolution_strategy="Interpret contract documents and apply hierarchy and amendment procedures.",
        entity_scope="All parties to MSAs",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="N/A (industry standard practice)"
    ),
    DoctrineBlock(
        topic="Liquidated Damages vs Penalties",
        keywords=["liquidated damages", "penalty", "enforceability", "reasonable estimate", "actual damages"],
        conclusion_template="Liquidated damages clauses are enforceable if they represent a reasonable estimate of anticipated harm and are not punitive.",
        reasoning_framework=(
            "1. Identify the liquidated damages clause and its stated amount or formula.\n"
            "2. Assess whether actual damages would be difficult to estimate at the time of contracting.\n"
            "3. Determine if the amount is a reasonable forecast of probable loss.\n"
            "4. Evaluate whether the clause is punitive or grossly disproportionate to anticipated harm.\n"
            "5. Consider public policy and statutory restrictions.\n"
            "6. Analyze the parties' intent and negotiation history.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Difficulty of estimating damages",
            "Reasonableness of amount",
            "Intent of parties",
            "Proportionality",
            "Public policy"
        ],
        primary_authority=["Restatement (Second) of Contracts § 356", "UCC §2-718", "JMD Holding Corp. v. Congress Fin. Corp., 4 N.Y.3d 373 (2005)"],
        burden_holder="Party seeking to enforce or avoid clause",
        adversary_position="Clause is an unenforceable penalty",
        counter_arguments=[
            "Amount is punitive",
            "Damages are easily ascertainable",
            "Clause violates public policy"
        ],
        resolution_strategy="Apply reasonableness and proportionality tests; enforce if not punitive.",
        entity_scope="All commercial contract parties",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="JMD Holding Corp. v. Congress Fin. Corp., 4 N.Y.3d 373 (2005)"
    ),
    DoctrineBlock(
        topic="Duty of Good Faith and Fair Dealing",
        keywords=["good faith", "fair dealing", "implied covenant", "performance", "enforcement"],
        conclusion_template="Every contract imposes an obligation of good faith and fair dealing in its performance and enforcement.",
        reasoning_framework=(
            "1. Identify the conduct alleged to violate the duty of good faith and fair dealing.\n"
            "2. Assess whether the party acted honestly and in accordance with reasonable commercial standards.\n"
            "3. Determine if the party's conduct deprived the other party of the benefits of the contract.\n"
            "4. Evaluate whether the conduct was arbitrary, capricious, or intended to frustrate the contract.\n"
            "5. Consider the express terms of the contract and whether the conduct is permitted.\n"
            "6. Analyze the remedies available for breach of the duty.\n"
            "7. Review relevant statutory and case law."
        ),
        key_factors=[
            "Honesty in fact",
            "Commercial reasonableness",
            "Deprivation of contract benefits",
            "Intent",
            "Consistency with express terms"
        ],
        primary_authority=["UCC §1-304", "Restatement (Second) of Contracts § 205", "Dalton v. Educational Testing Serv., 87 N.Y.2d 384 (1995)"],
        burden_holder="Party alleging breach of duty",
        adversary_position="Conduct was permitted by contract and in good faith",
        counter_arguments=[
            "Actions were commercially reasonable",
            "No deprivation of contract benefits",
            "Express terms control"
        ],
        resolution_strategy="Apply good faith standard to facts and contract terms.",
        entity_scope="All commercial contract parties",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Dalton v. Educational Testing Serv., 87 N.Y.2d 384 (1995)"
    ),
    DoctrineBlock(
        topic="Integration and Merger Clauses",
        keywords=["integration", "merger", "parol evidence", "entire agreement", "enforceability"],
        conclusion_template="An integration or merger clause establishes that the written contract is the complete and final agreement, limiting the use of parol evidence to vary its terms.",
        reasoning_framework=(
            "1. Identify the integration or merger clause in the contract.\n"
            "2. Assess whether the contract is fully integrated (complete and exclusive statement of terms).\n"
            "3. Determine whether parol evidence is offered to contradict, vary, or supplement the written terms.\n"
            "4. Evaluate exceptions to the parol evidence rule (fraud, mistake, ambiguity, subsequent modification).\n"
            "5. Analyze the effect of the clause on prior or contemporaneous agreements.\n"
            "6. Consider the parties' intent and negotiation history.\n"
            "7. Review relevant statutory and case law."
        ),
        key_factors=[
            "Presence and clarity of clause",
            "Completeness of written agreement",
            "Purpose of parol evidence",
            "Exceptions to parol evidence rule",
            "Intent of parties"
        ],
        primary_authority=["Restatement (Second) of Contracts § 213", "UCC §2-202", "Primex Int'l Corp. v. Wal-Mart Stores, Inc., 89 N.Y.2d 594 (1997)"],
        burden_holder="Party seeking to introduce or exclude parol evidence",
        adversary_position="Contract is not fully integrated or exception applies",
        counter_arguments=[
            "Ambiguity exists",
            "Fraud or mistake",
            "Subsequent modification"
        ],
        resolution_strategy="Apply parol evidence rule and exceptions; enforce clause if agreement is fully integrated.",
        entity_scope="All commercial contract parties",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Primex Int'l Corp. v. Wal-Mart Stores, Inc., 89 N.Y.2d 594 (1997)"
    ),
    DoctrineBlock(
        topic="Best Efforts vs Reasonable Efforts Obligations",
        keywords=["best efforts", "reasonable efforts", "performance standard", "contractual obligation", "enforceability"],
        conclusion_template="A 'best efforts' obligation generally requires greater diligence than 'reasonable efforts', but both are interpreted in light of the parties' intent and commercial context.",
        reasoning_framework=(
            "1. Identify the language of the efforts clause ('best efforts', 'reasonable efforts', etc.).\n"
            "2. Assess the commercial context and the parties' intent.\n"
            "3. Determine industry standards for performance.\n"
            "4. Evaluate the feasibility and cost of compliance.\n"
            "5. Analyze whether the party acted diligently and in good faith.\n"
            "6. Consider the consequences of non-performance.\n"
            "7. Review relevant case law for interpretation and enforcement."
        ),
        key_factors=[
            "Language of clause",
            "Commercial context",
            "Industry standards",
            "Good faith and diligence",
            "Feasibility of performance"
        ],
        primary_authority=["Bloor v. Falstaff Brewing Corp., 601 F.2d 609 (2d Cir. 1979)", "Restatement (Second) of Contracts § 205"],
        burden_holder="Party alleging breach of efforts obligation",
        adversary_position="Efforts were reasonable under the circumstances",
        counter_arguments=[
            "Performance met industry standards",
            "Best efforts is not absolute",
            "Commercial impracticability"
        ],
        resolution_strategy="Interpret clause in context and apply diligence standard.",
        entity_scope="All commercial contract parties",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Bloor v. Falstaff Brewing Corp., 601 F.2d 609 (2d Cir. 1979)"
    ),
    DoctrineBlock(
        topic="Modification and No Oral Modification Clauses",
        keywords=["modification", "no oral modification", "writing requirement", "UCC", "enforceability"],
        conclusion_template="A no oral modification clause requires that contract modifications be in writing, but under the UCC, oral modifications may be enforceable under certain circumstances.",
        reasoning_framework=(
            "1. Identify the no oral modification clause and its requirements.\n"
            "2. Assess whether the alleged modification was made orally or in writing.\n"
            "3. Determine if the UCC or common law applies.\n"
            "4. Under UCC 2-209, assess whether oral modification is enforceable (e.g., waiver, estoppel).\n"
            "5. Evaluate whether the modification is supported by consideration (common law) or not required (UCC).\n"
            "6. Consider the parties' conduct and reliance.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Presence of no oral modification clause",
            "Form of alleged modification",
            "Applicability of UCC or common law",
            "Waiver or estoppel",
            "Consideration"
        ],
        primary_authority=["UCC §2-209", "Rose v. Spa Realty Assocs., 42 N.Y.2d 338 (1977)"],
        burden_holder="Party asserting or denying modification",
        adversary_position="Modification is unenforceable due to lack of writing",
        counter_arguments=[
            "Waiver or estoppel applies",
            "UCC permits oral modification",
            "Conduct evidences modification"
        ],
        resolution_strategy="Apply UCC or common law rules and analyze facts for enforceability.",
        entity_scope="All commercial contract parties",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Rose v. Spa Realty Assocs., 42 N.Y.2d 338 (1977)"
    ),
    DoctrineBlock(
        topic="Arbitration Clauses in Commercial Contracts",
        keywords=["arbitration", "dispute resolution", "enforceability", "FAA", "scope"],
        conclusion_template="Arbitration clauses are generally enforceable under the Federal Arbitration Act unless unconscionable or contrary to public policy.",
        reasoning_framework=(
            "1. Identify the arbitration clause and its scope (claims covered, procedures).\n"
            "2. Assess whether the clause is clear, specific, and mutually agreed upon.\n"
            "3. Determine if the Federal Arbitration Act (FAA) or state law applies.\n"
            "4. Evaluate whether the clause is unconscionable or violates public policy.\n"
            "5. Analyze the arbitrability of the dispute (gateway issues).\n"
            "6. Consider the effect of the clause on substantive rights and remedies.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Scope and clarity of clause",
            "Mutual assent",
            "FAA applicability",
            "Unconscionability",
            "Public policy"
        ],
        primary_authority=["Federal Arbitration Act, 9 U.S.C. § 1 et seq.", "AT&T Mobility LLC v. Concepcion, 563 U.S. 333 (2011)"],
        burden_holder="Party seeking to enforce or avoid arbitration",
        adversary_position="Clause is unconscionable or dispute is not arbitrable",
        counter_arguments=[
            "Unconscionability",
            "Public policy violation",
            "Dispute is outside scope"
        ],
        resolution_strategy="Apply FAA and contract law; enforce if clause is clear and not unconscionable.",
        entity_scope="All commercial contract parties",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AT&T Mobility LLC v. Concepcion, 563 U.S. 333 (2011)"
    ),
    DoctrineBlock(
        topic="Intellectual Property Ownership in Services Contracts",
        keywords=["intellectual property", "ownership", "services contract", "work for hire", "assignment"],
        conclusion_template="Intellectual property created under a services contract is owned as specified by the contract; absent clear language, default rules may apply.",
        reasoning_framework=(
            "1. Identify the IP provisions in the services contract (ownership, assignment, license).\n"
            "2. Assess whether the contract specifies ownership of deliverables and inventions.\n"
            "3. Determine if the work qualifies as 'work for hire' under copyright law.\n"
            "4. Evaluate whether an assignment or license of IP rights is required or has occurred.\n"
            "5. Consider the parties' intent and negotiation history.\n"
            "6. Analyze the effect of default rules (creator owns absent assignment).\n"
            "7. Review relevant statutory and case law."
        ),
        key_factors=[
            "Contract language on IP ownership",
            "Work for hire status",
            "Assignment or license",
            "Intent of parties",
            "Default legal rules"
        ],
        primary_authority=["17 U.S.C. § 101 et seq.", "Community for Creative Non-Violence v. Reid, 490 U.S. 730 (1989)"],
        burden_holder="Party asserting ownership or assignment",
        adversary_position="IP is owned by creator absent assignment",
        counter_arguments=[
            "No assignment or work for hire",
            "Contract is ambiguous",
            "Default rules apply"
        ],
        resolution_strategy="Interpret contract and apply statutory default rules.",
        entity_scope="All parties to services contracts",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="Community for Creative Non-Violence v. Reid, 490 U.S. 730 (1989)"
    ),
    DoctrineBlock(
        topic="Termination for Convenience Clauses",
        keywords=["termination for convenience", "unilateral termination", "notice", "remedies", "commercial contracts"],
        conclusion_template="A termination for convenience clause allows a party to terminate the contract without cause, subject to notice and any specified remedies.",
        reasoning_framework=(
            "1. Identify the termination for convenience clause and its requirements (notice, compensation).\n"
            "2. Assess whether the terminating party complied with notice and procedural requirements.\n"
            "3. Determine the effect of termination on the parties' rights and obligations.\n"
            "4. Evaluate any limitations on the right to terminate (timing, minimum commitment).\n"
            "5. Analyze the remedies available to the non-terminating party (e.g., payment for work performed).\n"
            "6. Consider public policy and good faith requirements.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Clause language and requirements",
            "Compliance with notice",
            "Remedies for non-terminating party",
            "Limitations on termination",
            "Good faith"
        ],
        primary_authority=["Contract language", "Quinn Constr., Inc. v. Skanska USA Bldg. Inc., 730 F. Supp. 2d 401 (E.D. Pa. 2010)"],
        burden_holder="Party seeking to terminate or challenge termination",
        adversary_position="Termination was improper or notice was insufficient",
        counter_arguments=[
            "Notice was not provided",
            "Termination violates good faith",
            "Remedies are inadequate"
        ],
        resolution_strategy="Interpret clause and ensure compliance with procedural and substantive requirements.",
        entity_scope="All commercial contract parties",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Quinn Constr., Inc. v. Skanska USA Bldg. Inc., 730 F. Supp. 2d 401 (E.D. Pa. 2010)"
    ),
    DoctrineBlock(
        topic="Joint Venture Agreements",
        keywords=["joint venture", "partnership", "agreement", "fiduciary duty", "profit sharing"],
        conclusion_template="A joint venture agreement creates a relationship in which parties combine resources for a specific business purpose, sharing profits, losses, and control.",
        reasoning_framework=(
            "1. Identify the joint venture agreement and its purpose.\n"
            "2. Assess the parties' contributions (capital, resources, expertise).\n"
            "3. Determine the allocation of profits, losses, and control.\n"
            "4. Evaluate the existence of fiduciary duties between joint venturers.\n"
            "5. Analyze the duration and termination provisions.\n"
            "6. Consider the effect of the agreement on third parties (liability, authority).\n"
            "7. Review relevant statutory and case law."
        ),
        key_factors=[
            "Purpose and scope of venture",
            "Contributions of parties",
            "Profit/loss sharing",
            "Control and management",
            "Fiduciary duties"
        ],
        primary_authority=["Partnership statutes", "Restatement (Third) of Agency", "Gramercy Equities Corp. v. Dumont, 72 N.Y.2d 560 (1988)"],
        burden_holder="Party asserting or denying joint venture status",
        adversary_position="No joint venture exists or duties are limited",
        counter_arguments=[
            "No mutual control or sharing",
            "Agreement is not a joint venture",
            "No fiduciary duty"
        ],
        resolution_strategy="Interpret agreement and apply statutory and common law criteria.",
        entity_scope="All parties to joint venture agreements",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="Gramercy Equities Corp. v. Dumont, 72 N.Y.2d 560 (1988)"
    ),
    DoctrineBlock(
        topic="Supply Chain and Distribution Agreements",
        keywords=["supply chain", "distribution", "exclusive", "non-exclusive", "termination", "UCC"],
        conclusion_template="Supply chain and distribution agreements set forth the terms for supplying and distributing goods, including exclusivity, pricing, and termination provisions.",
        reasoning_framework=(
            "1. Identify the supply or distribution agreement and its scope (exclusive, non-exclusive).\n"
            "2. Assess the parties' rights and obligations regarding supply, distribution, and territory.\n"
            "3. Determine pricing, payment, and delivery terms.\n"
            "4. Evaluate exclusivity provisions and their enforceability.\n"
            "5. Analyze termination rights and procedures.\n"
            "6. Consider UCC and antitrust implications.\n"
            "7. Review relevant case law and industry practice."
        ),
        key_factors=[
            "Scope of agreement",
            "Exclusivity",
            "Pricing and payment terms",
            "Termination provisions",
            "Compliance with UCC and antitrust law"
        ],
        primary_authority=["UCC Article 2", "Restatement (Second) of Contracts", "Bloor v. Falstaff Brewing Corp., 601 F.2d 609 (2d Cir. 1979)"],
        burden_holder="Party asserting or denying rights under agreement",
        adversary_position="Provisions are unenforceable or violated",
        counter_arguments=[
            "Exclusivity is anti-competitive",
            "Termination was improper",
            "Pricing violates law"
        ],
        resolution_strategy="Interpret agreement and apply UCC, antitrust, and industry standards.",
        entity_scope="All parties to supply and distribution agreements",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="Bloor v. Falstaff Brewing Corp., 601 F.2d 609 (2d Cir. 1979)"
    ),
    # Additional doctrines to reach 40+ entries:
    DoctrineBlock(
        topic="Assignment of Receivables",
        keywords=["assignment", "receivables", "UCC", "notification", "priority"],
        conclusion_template="Assignment of receivables is generally permitted unless contractually prohibited; notification and priority rules under the UCC may apply.",
        reasoning_framework=(
            "1. Identify the receivables and the assignment agreement.\n"
            "2. Assess whether the underlying contract prohibits or restricts assignment.\n"
            "3. Determine if notification to the account debtor is required.\n"
            "4. Evaluate priority among multiple assignees under UCC Article 9.\n"
            "5. Analyze the effect of assignment on the rights and obligations of all parties.\n"
            "6. Consider statutory exceptions and public policy.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Contractual restrictions",
            "Notification requirements",
            "Priority rules",
            "Effect on parties",
            "Statutory exceptions"
        ],
        primary_authority=["UCC §9-406", "Restatement (Second) of Contracts § 322"],
        burden_holder="Party asserting or challenging assignment",
        adversary_position="Assignment is prohibited or ineffective",
        counter_arguments=[
            "Contract prohibits assignment",
            "No notification given",
            "Priority dispute"
        ],
        resolution_strategy="Apply UCC Article 9 and contract terms to determine validity and priority.",
        entity_scope="All parties to receivables assignments",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="N/A (UCC controls)"
    ),
    DoctrineBlock(
        topic="Change of Control Provisions",
        keywords=["change of control", "trigger", "assignment", "termination", "notice"],
        conclusion_template="Change of control provisions may trigger rights such as termination or consent requirements upon a change in ownership or control of a party.",
        reasoning_framework=(
            "1. Identify the change of control provision and its triggers (merger, sale, reorganization).\n"
            "2. Assess whether the triggering event has occurred.\n"
            "3. Determine the rights and obligations that arise upon change of control (termination, consent, notice).\n"
            "4. Evaluate any notice and procedural requirements.\n"
            "5. Analyze the effect on the contract and third parties.\n"
            "6. Consider public policy and statutory restrictions.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Triggering events",
            "Rights and obligations upon change",
            "Notice requirements",
            "Procedural compliance",
            "Public policy"
        ],
        primary_authority=["Contract language", "Restatement (Second) of Contracts"],
        burden_holder="Party invoking or resisting change of control rights",
        adversary_position="Event does not trigger provision or rights are limited",
        counter_arguments=[
            "No change of control occurred",
            "Notice not given",
            "Provision is unenforceable"
        ],
        resolution_strategy="Interpret provision and apply to facts; ensure compliance with notice and procedure.",
        entity_scope="All commercial contract parties",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="N/A (contractual interpretation)"
    ),
    DoctrineBlock(
        topic="Setoff and Netting Rights",
        keywords=["setoff", "netting", "mutual debts", "bankruptcy", "contractual rights"],
        conclusion_template="Setoff and netting rights allow parties to offset mutual debts, subject to contractual terms and bankruptcy law limitations.",
        reasoning_framework=(
            "1. Identify the existence of mutual debts or obligations.\n"
            "2. Assess whether the contract provides for setoff or netting rights.\n"
            "3. Determine if the debts are due and payable.\n"
            "4. Evaluate any statutory or bankruptcy law limitations on setoff.\n"
            "5. Analyze the effect of setoff on the parties' obligations.\n"
            "6. Consider public policy and equitable considerations.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Mutuality of debts",
            "Contractual setoff/netting rights",
            "Bankruptcy limitations",
            "Due and payable status",
            "Public policy"
        ],
        primary_authority=["11 U.S.C. § 553", "Restatement (Second) of Contracts § 318"],
        burden_holder="Party asserting setoff/netting",
        adversary_position="Setoff is contractually or statutorily barred",
        counter_arguments=[
            "No mutuality",
            "Bankruptcy stay applies",
            "Contract prohibits setoff"
        ],
        resolution_strategy="Apply contract and bankruptcy law to determine validity of setoff/netting.",
        entity_scope="All commercial contract parties",
        confidence=0.87,
        confidence_zone="Medium-High",
        controlling_precedent="N/A (statutory and contract law)"
    ),
    DoctrineBlock(
        topic="Escrow Arrangements in Commercial Contracts",
        keywords=["escrow", "third party", "release conditions", "security", "dispute resolution"],
        conclusion_template="Escrow arrangements provide for a third party to hold assets or documents pending satisfaction of specified conditions.",
        reasoning_framework=(
            "1. Identify the escrow agreement and the parties involved.\n"
            "2. Assess the conditions for release of escrowed assets or documents.\n"
            "3. Determine the rights and duties of the escrow agent.\n"
            "4. Evaluate the remedies for breach or failure of conditions.\n"
            "5. Analyze the effect of escrow on the underlying contract.\n"
            "6. Consider statutory and regulatory requirements.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Escrow conditions",
            "Duties of escrow agent",
            "Remedies for breach",
            "Effect on underlying contract",
            "Statutory compliance"
        ],
        primary_authority=["Contract language", "Restatement (Third) of Agency"],
        burden_holder="Party seeking release or retention of escrow",
        adversary_position="Conditions not satisfied or agent breached duty",
        counter_arguments=[
            "Conditions not met",
            "Agent acted improperly",
            "Escrow is unenforceable"
        ],
        resolution_strategy="Interpret escrow agreement and ensure compliance with conditions and duties.",
        entity_scope="All parties to escrow arrangements",
        confidence=0.86,
        confidence_zone="Medium-High",
        controlling_precedent="N/A (contractual interpretation)"
    ),
    DoctrineBlock(
        topic="Non-Compete Clauses in Commercial Contracts",
        keywords=["non-compete", "restrictive covenant", "enforceability", "reasonableness", "public policy"],
        conclusion_template="Non-compete clauses are enforceable if reasonable in scope, duration, and geography, and necessary to protect legitimate business interests.",
        reasoning_framework=(
            "1. Identify the non-compete clause and its restrictions (scope, duration, geography).\n"
            "2. Assess whether the clause protects a legitimate business interest.\n"
            "3. Determine if the restrictions are reasonable and not unduly burdensome.\n"
            "4. Evaluate public policy considerations and statutory restrictions.\n"
            "5. Analyze the effect of the clause on competition and the parties.\n"
            "6. Consider the availability of less restrictive alternatives.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Scope, duration, and geography",
            "Legitimate business interest",
            "Reasonableness",
            "Public policy",
            "Alternatives"
        ],
        primary_authority=["BDO Seidman v. Hirshberg, 93 N.Y.2d 382 (1999)", "Restatement (Second) of Contracts § 188"],
        burden_holder="Party seeking to enforce or avoid non-compete",
        adversary_position="Clause is unreasonable or contrary to public policy",
        counter_arguments=[
            "Overbroad restrictions",
            "No legitimate interest",
            "Violates public policy"
        ],
        resolution_strategy="Apply reasonableness and necessity tests; enforce if justified.",
        entity_scope="All commercial contract parties",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="BDO Seidman v. Hirshberg, 93 N.Y.2d 382 (1999)"
    ),
    DoctrineBlock(
        topic="Step-In Rights in Outsourcing Agreements",
        keywords=["step-in rights", "outsourcing", "remedy", "default", "continuity of service"],
        conclusion_template="Step-in rights allow a customer to assume control of outsourced services upon supplier default, subject to contractual conditions.",
        reasoning_framework=(
            "1. Identify the step-in rights clause and its triggers (default, insolvency, performance failure).\n"
            "2. Assess whether the triggering event has occurred.\n"
            "3. Determine the scope of rights and obligations upon exercise of step-in.\n"
            "4. Evaluate notice and procedural requirements.\n"
            "5. Analyze the effect on third parties and continuity of service.\n"
            "6. Consider remedies for improper exercise of step-in rights.\n"
            "7. Review relevant case law and industry standards."
        ),
        key_factors=[
            "Triggering events",
            "Scope of step-in rights",
            "Notice and procedure",
            "Effect on service continuity",
            "Remedies for breach"
        ],
        primary_authority=["Contract language", "Industry practice"],
        burden_holder="Party seeking to exercise or resist step-in rights",
        adversary_position="Step-in is not permitted or conditions unmet",
        counter_arguments=[
            "No default occurred",
            "Notice not given",
            "Step-in exceeds scope"
        ],
        resolution_strategy="Interpret contract and ensure compliance with step-in conditions.",
        entity_scope="All parties to outsourcing agreements",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="N/A (contractual interpretation)"
    ),
    DoctrineBlock(
        topic="Audit Rights in Commercial Contracts",
        keywords=["audit rights", "inspection", "records", "compliance", "remedies"],
        conclusion_template="Audit rights clauses permit a party to inspect the other party's records to verify compliance, subject to scope and procedural requirements.",
        reasoning_framework=(
            "1. Identify the audit rights clause and its scope (records, frequency, notice).\n"
            "2. Assess whether the requesting party has complied with procedural requirements (notice, confidentiality).\n"
            "3. Determine the extent of records subject to audit.\n"
            "4. Evaluate remedies for non-compliance or discovery of discrepancies.\n"
            "5. Analyze the effect on business operations and confidentiality.\n"
            "6. Consider statutory or regulatory requirements.\n"
            "7. Review relevant case law and industry standards."
        ),
        key_factors=[
            "Scope of audit rights",
            "Procedural compliance",
            "Remedies for non-compliance",
            "Confidentiality",
            "Regulatory requirements"
        ],
        primary_authority=["Contract language", "Industry practice"],
        burden_holder="Party seeking to exercise or resist audit rights",
        adversary_position="Audit exceeds scope or violates confidentiality",
        counter_arguments=[
            "Scope is limited",
            "Notice not given",
            "Confidentiality breached"
        ],
        resolution_strategy="Interpret clause and ensure compliance with procedural and substantive requirements.",
        entity_scope="All commercial contract parties",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="N/A (contractual interpretation)"
    ),
    DoctrineBlock(
        topic="Survival of Obligations Post-Termination",
        keywords=["survival", "post-termination", "obligations", "confidentiality", "warranties"],
        conclusion_template="Certain contractual obligations may survive termination if expressly stated or implied by their nature.",
        reasoning_framework=(
            "1. Identify the survival clause and obligations specified (confidentiality, indemnity, warranties).\n"
            "2. Assess whether the contract expressly provides for survival post-termination.\n"
            "3. Determine if obligations should survive by their nature or purpose.\n"
            "4. Evaluate the duration and scope of surviving obligations.\n"
            "5. Analyze the effect on the parties' rights and liabilities.\n"
            "6. Consider public policy and statutory requirements.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Express survival language",
            "Nature of obligation",
            "Duration and scope",
            "Effect on parties",
            "Public policy"
        ],
        primary_authority=["Contract language", "Restatement (Second) of Contracts"],
        burden_holder="Party asserting or denying survival",
        adversary_position="Obligation does not survive or is limited",
        counter_arguments=[
            "No express survival",
            "Obligation is not intended to survive",
            "Contrary to public policy"
        ],
        resolution_strategy="Interpret contract and apply default rules for survival.",
        entity_scope="All commercial contract parties",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="N/A (contractual interpretation)"
    ),
    DoctrineBlock(
        topic="Force Majeure and COVID-19",
        keywords=["force majeure", "COVID-19", "pandemic", "performance", "excuse"],
        conclusion_template="COVID-19 may constitute a force majeure event if covered by the clause and directly prevents performance.",
        reasoning_framework=(
            "1. Identify the force majeure clause and whether it includes pandemics or government actions.\n"
            "2. Assess whether COVID-19 or related government orders directly prevented performance.\n"
            "3. Determine if the event was unforeseeable at the time of contracting.\n"
            "4. Evaluate notice and mitigation requirements.\n"
            "5. Analyze the causal connection between COVID-19 and non-performance.\n"
            "6. Consider public policy and relevant case law.\n"
            "7. Review remedies and allocation of risk."
        ),
        key_factors=[
            "Clause language (pandemic, government action)",
            "Causal connection",
            "Foreseeability",
            "Notice and mitigation",
            "Public policy"
        ],
        primary_authority=["Contract language", "J. Crew Group, Inc. v. Simon Property Group, L.P., No. 20-01212 (Del. Ch. 2020)"],
        burden_holder="Party invoking force majeure",
        adversary_position="COVID-19 does not excuse performance",
        counter_arguments=[
            "Clause does not cover pandemic",
            "Performance is still possible",
            "No causal connection"
        ],
        resolution_strategy="Interpret clause and facts; apply force majeure doctrine to COVID-19 context.",
        entity_scope="All commercial contract parties",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="J. Crew Group, Inc. v. Simon Property Group, L.P., No. 20-01212 (Del. Ch. 2020)"
    ),
    DoctrineBlock(
        topic="Payment Terms and Late Payment Interest",
        keywords=["payment terms", "late payment", "interest", "UCC", "enforceability"],
        conclusion_template="Payment terms and late payment interest are enforceable if clearly stated and not usurious or contrary to law.",
        reasoning_framework=(
            "1. Identify the payment terms and interest provisions in the contract.\n"
            "2. Assess whether the terms are clear, specific, and agreed upon.\n"
            "3. Determine if the interest rate complies with applicable usury laws.\n"
            "4. Evaluate the remedies for late payment (interest, suspension of services).\n"
            "5. Analyze the effect of non-payment on contract performance.\n"
            "6. Consider statutory requirements (UCC, state law).\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Clarity of terms",
            "Compliance with usury laws",
            "Agreement by parties",
            "Remedies for late payment",
            "Statutory requirements"
        ],
        primary_authority=["UCC §2-207", "State usury statutes"],
        burden_holder="Party seeking to enforce or avoid payment terms",
        adversary_position="Interest is usurious or terms are unclear",
        counter_arguments=[
            "Interest exceeds legal limit",
            "Terms are ambiguous",
            "No agreement on interest"
        ],
        resolution_strategy="Interpret contract and apply statutory limits; enforce if lawful.",
        entity_scope="All commercial contract parties",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="N/A (statutory and contract law)"
    ),
    DoctrineBlock(
        topic="Data Security and Privacy Obligations",
        keywords=["data security", "privacy", "obligations", "breach", "compliance"],
        conclusion_template="Data security and privacy obligations require parties to protect personal and confidential information, subject to contract terms and applicable law.",
        reasoning_framework=(
            "1. Identify the data security and privacy provisions in the contract.\n"
            "2. Assess the types of data covered and required security measures.\n"
            "3. Determine the parties' obligations in the event of a data breach.\n"
            "4. Evaluate compliance with applicable laws (GDPR, CCPA, etc.).\n"
            "5. Analyze remedies for breach of data security obligations.\n"
            "6. Consider public policy and industry standards.\n"
            "7. Review relevant case law and regulatory guidance."
        ),
        key_factors=[
            "Scope of data covered",
            "Security measures",
            "Breach notification",
            "Compliance with law",
            "Remedies for breach"
        ],
        primary_authority=["GDPR", "CCPA", "Contract language"],
        burden_holder="Party asserting or denying breach",
        adversary_position="Obligations were met or breach is excused",
        counter_arguments=[
            "No breach occurred",
            "Obligations are unclear",
            "Compliance with law"
        ],
        resolution_strategy="Interpret contract and apply legal requirements; enforce if obligations are clear.",
        entity_scope="All commercial contract parties",
        confidence=0.83,
        confidence_zone="Medium",
        controlling_precedent="N/A (statutory and contract law)"
    ),
    DoctrineBlock(
        topic="Subcontracting and Flow-Down Clauses",
        keywords=["subcontracting", "flow-down", "prime contract", "obligations", "enforceability"],
        conclusion_template="Flow-down clauses require subcontractors to comply with certain obligations of the prime contract, and are enforceable if clearly incorporated.",
        reasoning_framework=(
            "1. Identify the flow-down clause and its scope in the subcontract.\n"
            "2. Assess whether the prime contract obligations are clearly incorporated.\n"
            "3. Determine the extent of subcontractor's obligations.\n"
            "4. Evaluate the remedies for breach of flow-down obligations.\n"
            "5. Analyze the effect on the parties and third parties.\n"
            "6. Consider public policy and statutory requirements.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Clarity of incorporation",
            "Scope of obligations",
            "Remedies for breach",
            "Effect on parties",
            "Public policy"
        ],
        primary_authority=["Contract language", "Restatement (Second) of Contracts"],
        burden_holder="Party seeking to enforce or resist flow-down",
        adversary_position="Obligations are not clearly incorporated",
        counter_arguments=[
            "Clause is ambiguous",
            "Obligations exceed scope",
            "Contrary to public policy"
        ],
        resolution_strategy="Interpret contract and ensure clear incorporation of obligations.",
        entity_scope="All parties to subcontracts",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="N/A (contractual interpretation)"
    ),
    DoctrineBlock(
        topic="Public Policy Limits on Contractual Freedom",
        keywords=["public policy", "contractual freedom", "unenforceability", "illegality", "restraint of trade"],
        conclusion_template="Contracts or clauses that violate public policy or law are unenforceable, regardless of party agreement.",
        reasoning_framework=(
            "1. Identify the contract or clause alleged to violate public policy.\n"
            "2. Assess the nature and purpose of the provision.\n"
            "3. Determine the relevant public policy or statutory prohibition.\n"
            "4. Evaluate the effect of enforcement on the parties and the public.\n"
            "5. Analyze whether the provision can be severed or reformed.\n"
            "6. Consider the parties' intent and alternatives.\n"
            "7. Review relevant statutory and case law."
        ),
        key_factors=[
            "Nature of provision",
            "Public policy or law violated",
            "Effect on parties and public",
            "Severability",
            "Intent of parties"
        ],
        primary_authority=["Restatement (Second) of Contracts §§ 178-179", "Illegality statutes"],
        burden_holder="Party asserting or resisting unenforceability",
        adversary_position="Provision does not violate public policy",
        counter_arguments=[
            "No public policy violation",
            "Provision can be severed",
            "Intent was lawful"
        ],
        resolution_strategy="Apply public policy analysis; sever or void provision if necessary.",
        entity_scope="All commercial contract parties",
        confidence=0.85,
        confidence_zone="Medium",
        controlling_precedent="N/A (statutory and public policy)"
    ),
    DoctrineBlock(
        topic="Notice Provisions and Effective Delivery",
        keywords=["notice", "delivery", "provision", "effective date", "method"],
        conclusion_template="Notice provisions specify how and when notices are effective; compliance is required for enforceability.",
        reasoning_framework=(
            "1. Identify the notice provision and required methods (mail, email, courier).\n"
            "2. Assess whether the notice was delivered in accordance with the provision.\n"
            "3. Determine the effective date of notice under the contract.\n"
            "4. Evaluate consequences of defective or late notice.\n"
            "5. Analyze any waiver or estoppel arguments.\n"
            "6. Consider statutory requirements for notice.\n"
            "7. Review relevant case law for enforceability."
        ),
        key_factors=[
            "Method of delivery",
            "Compliance with provision",
            "Effective date",
            "Consequences of non-compliance",
            "Statutory requirements"
        ],
        primary_authority=["Contract language", "Restatement (Second) of Contracts"],
        burden_holder="Party asserting or challenging notice",
        adversary_position="Notice was not effective or properly delivered",
        counter_arguments=[
            "Improper method",
            "Notice was late",
            "Provision was waived"
        ],
        resolution_strategy="Interpret contract and ensure strict compliance with notice requirements.",
        entity_scope="All commercial contract parties",
        confidence=0.84,
        confidence_zone="Medium",
        controlling_precedent="N/A (contractual interpretation)"
    ),
    DoctrineBlock(
        topic="Waiver and Estoppel in Contract Enforcement",
        keywords=["waiver", "estoppel", "contract enforcement", "conduct", "reliance"],
        conclusion_template="A party may waive contractual rights by words or conduct, and may be estopped from enforcing rights if the other party reasonably relied to their detriment.",
        reasoning_framework=(
            "1. Identify the right or provision allegedly waived.\n"
            "2. Assess whether waiver occurred by express statement or conduct.\n"
            "3. Determine if the other party relied on the waiver to their detriment.\n"
            "4. Evaluate whether estoppel bars enforcement of the right.\n"
            "5. Analyze the effect of waiver or estoppel on contract obligations.\n"
            "6. Consider public policy and statutory requirements.\n"
            "7. Review relevant case law for enforceability."