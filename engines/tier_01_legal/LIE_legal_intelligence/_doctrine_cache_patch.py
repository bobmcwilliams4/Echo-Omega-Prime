LEGAL_DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="Contract Formation",
        keywords=["offer", "acceptance", "consideration", "mutual assent", "capacity", "statute of frauds", "intent", "terms"],
        conclusion_template="To determine whether a valid contract has been formed, analyze the presence of offer, acceptance, and consideration. Assess whether the parties had mutual assent and legal capacity. Evaluate compliance with the statute of frauds if applicable. Conclude on the enforceability of the agreement based on these elements.",
        reasoning_framework="""1. Identify the parties and their intent to contract.
2. Examine the existence of a clear offer and corresponding acceptance.
3. Evaluate the adequacy and legality of consideration exchanged.
4. Assess mutual assent, ensuring both parties understood and agreed to the terms.
5. Check for legal capacity of each party (age, mental competence).
6. Determine if the contract falls under the statute of frauds and requires writing.
7. Analyze the specificity and clarity of contract terms.
8. Review any conditions precedent or subsequent affecting formation.
9. Consider defenses to formation (duress, undue influence, misrepresentation).
10. Examine whether any public policy issues invalidate the contract.
11. Evaluate any relevant jurisdictional requirements.
12. Review prior communications for evidence of intent.
13. Analyze the impact of any modifications or amendments.
14. Consider the effect of silence or conduct as acceptance.
15. Conclude on enforceability and validity.""",
        key_factors=["offer", "acceptance", "consideration", "mutual assent", "capacity", "statute of frauds"],
        primary_authority=["Restatement (Second) of Contracts §17", "UCC §2-204", "Carlill v Carbolic Smoke Ball Co [1893] 1 QB 256"],
        burden_holder="Plaintiff",
        adversary_position="No valid contract exists due to lack of offer, acceptance, or consideration.",
        counter_arguments=[
            "Offer and acceptance are evidenced by conduct.",
            "Consideration can be nominal or implied.",
            "Statute of frauds does not apply to this contract.",
            "Capacity is presumed absent contrary evidence.",
            "Mutual assent can be inferred from communications.",
            "Terms are sufficiently definite for enforcement."
        ],
        resolution_strategy="Apply the elements of contract formation to facts; weigh evidence of offer, acceptance, and consideration; resolve ambiguities using parol evidence rule.",
        entity_scope="Contracting parties",
        confidence=0.95,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Restatement (Second) of Contracts §17"
    ),
    DoctrineBlock(
        topic="Breach of Contract Remedies",
        keywords=["damages", "specific performance", "rescission", "mitigation", "foreseeability", "liquidated damages", "restitution"],
        conclusion_template="Assess the nature and extent of the breach. Identify available remedies including damages, specific performance, and rescission. Evaluate the adequacy of mitigation efforts and the foreseeability of losses. Conclude on the most appropriate remedy based on the facts.",
        reasoning_framework="""1. Determine whether a breach occurred and its severity.
2. Identify the type of breach (material, minor, anticipatory).
3. Analyze the injured party's losses and causation.
4. Evaluate the foreseeability of damages at contract formation.
5. Assess the adequacy of mitigation efforts by the non-breaching party.
6. Consider the applicability of liquidated damages clauses.
7. Examine the possibility of specific performance (unique subject matter).
8. Review grounds for rescission or restitution.
9. Calculate expectation, reliance, and consequential damages.
10. Analyze any limitations or exclusions of liability.
11. Consider equitable remedies where legal remedies are inadequate.
12. Review relevant statutes and case law.
13. Assess the impact of any waiver or estoppel.
14. Evaluate the effect of partial performance.
15. Conclude on the remedy most likely to be awarded.""",
        key_factors=["type of breach", "damages", "mitigation", "foreseeability", "remedy sought"],
        primary_authority=["Hadley v Baxendale (1854) 9 Exch 341", "Restatement (Second) of Contracts §347", "UCC §2-713"],
        burden_holder="Plaintiff",
        adversary_position="No damages or remedy should be awarded due to lack of causation or mitigation.",
        counter_arguments=[
            "Damages were foreseeable at contract formation.",
            "Mitigation was reasonable and sufficient.",
            "Liquidated damages clause is enforceable.",
            "Specific performance is warranted due to unique subject matter.",
            "Rescission is justified by material breach.",
            "Restitution restores parties to pre-contract position."
        ],
        resolution_strategy="Apply relevant legal standards; quantify damages; consider equitable remedies; weigh mitigation efforts.",
        entity_scope="Contracting parties",
        confidence=0.92,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Hadley v Baxendale (1854) 9 Exch 341"
    ),
    DoctrineBlock(
        topic="Negligence",
        keywords=["duty", "breach", "causation", "proximate cause", "damages", "reasonable care", "foreseeability"],
        conclusion_template="Evaluate whether the defendant owed a duty of care to the plaintiff. Analyze breach of duty and causation. Assess damages and foreseeability. Conclude on liability for negligence based on these elements.",
        reasoning_framework="""1. Identify the existence of a duty owed by the defendant to the plaintiff.
2. Define the standard of care required in the circumstances.
3. Analyze whether the defendant breached that duty.
4. Establish factual causation (but-for test).
5. Assess proximate cause (foreseeability of harm).
6. Quantify damages suffered by the plaintiff.
7. Consider defenses (contributory negligence, assumption of risk).
8. Review statutory modifications to common law negligence.
9. Examine comparative fault principles.
10. Evaluate the impact of intervening or superseding causes.
11. Analyze the relationship between parties (invitee, licensee, trespasser).
12. Consider public policy implications.
13. Review relevant case law and statutes.
14. Assess whether breach was a substantial factor in causing harm.
15. Conclude on liability and apportionment of damages.""",
        key_factors=["duty", "breach", "causation", "damages", "foreseeability"],
        primary_authority=["Palsgraf v Long Island Railroad Co., 248 N.Y. 339 (1928)", "Restatement (Second) of Torts §282", "California Civil Code §1714"],
        burden_holder="Plaintiff",
        adversary_position="Defendant did not owe a duty or did not breach the standard of care.",
        counter_arguments=[
            "Duty was established by relationship or statute.",
            "Breach occurred based on objective standard.",
            "Causation is supported by evidence.",
            "Damages are quantifiable and proximate.",
            "Foreseeability is clear from circumstances.",
            "Comparative fault reduces but does not eliminate liability."
        ],
        resolution_strategy="Apply negligence elements; weigh evidence; allocate fault as appropriate.",
        entity_scope="Plaintiff and defendant",
        confidence=0.93,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Palsgraf v Long Island Railroad Co., 248 N.Y. 339 (1928)"
    ),
    DoctrineBlock(
        topic="Strict Liability",
        keywords=["abnormally dangerous", "product liability", "causation", "defective product", "foreseeability", "injury", "risk"],
        conclusion_template="Determine whether strict liability applies based on the nature of the activity or product. Analyze causation and injury. Assess whether the risk was abnormally dangerous and foreseeable. Conclude on liability regardless of fault.",
        reasoning_framework="""1. Identify the activity or product alleged to cause harm.
2. Determine if the activity is abnormally dangerous or the product is defective.
3. Analyze statutory and common law bases for strict liability.
4. Establish causation between defendant's conduct and plaintiff's injury.
5. Assess whether the risk was foreseeable and inherent.
6. Evaluate the extent of injury and damages.
7. Consider defenses (assumption of risk, misuse).
8. Review manufacturer and seller liability.
9. Examine regulatory standards for product safety.
10. Analyze the role of warnings and instructions.
11. Assess the impact of intervening causes.
12. Review relevant case law and statutes.
13. Consider public policy implications.
14. Evaluate the scope of liability (multiple defendants).
15. Conclude on strict liability and apportionment of damages.""",
        key_factors=["abnormally dangerous activity", "defective product", "causation", "injury", "foreseeability"],
        primary_authority=["Restatement (Second) of Torts §402A", "Greenman v Yuba Power Products, Inc., 59 Cal.2d 57 (1963)", "California Civil Code §1714.45"],
        burden_holder="Plaintiff",
        adversary_position="Defendant's activity was not abnormally dangerous or product was not defective.",
        counter_arguments=[
            "Activity meets criteria for abnormally dangerous.",
            "Product defect is established by evidence.",
            "Causation is direct and proximate.",
            "Injury is foreseeable and compensable.",
            "Defenses do not apply or are insufficient.",
            "Warnings were inadequate."
        ],
        resolution_strategy="Apply strict liability standards; review evidence; allocate damages.",
        entity_scope="Plaintiff and defendant",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Restatement (Second) of Torts §402A"
    ),
    DoctrineBlock(
        topic="Constitutional Due Process",
        keywords=["procedural due process", "substantive due process", "notice", "hearing", "liberty", "property", "government action"],
        conclusion_template="Analyze whether government action deprived an individual of liberty or property. Assess adequacy of notice and opportunity to be heard. Evaluate substantive and procedural due process requirements. Conclude on constitutionality of the action.",
        reasoning_framework="""1. Identify the government action at issue.
2. Determine if a liberty or property interest is implicated.
3. Analyze procedural due process requirements (notice, hearing).
4. Assess substantive due process standards (fundamental rights).
5. Evaluate the adequacy of procedures provided.
6. Review relevant constitutional provisions and case law.
7. Consider the balancing of interests (Mathews v Eldridge factors).
8. Examine the risk of erroneous deprivation.
9. Analyze the government's justification for the action.
10. Assess the impact on affected parties.
11. Review remedies for due process violations.
12. Consider public policy implications.
13. Evaluate the scope of judicial review.
14. Examine any exceptions or limitations.
15. Conclude on compliance with due process.""",
        key_factors=["government action", "liberty/property interest", "notice", "hearing", "procedural/substantive requirements"],
        primary_authority=["U.S. Const. amend. XIV", "Mathews v Eldridge, 424 U.S. 319 (1976)", "Goldberg v Kelly, 397 U.S. 254 (1970)"],
        burden_holder="Plaintiff",
        adversary_position="Government provided adequate process or no protected interest was implicated.",
        counter_arguments=[
            "Protected interest is clearly established.",
            "Notice and hearing were insufficient.",
            "Procedures failed to minimize erroneous deprivation.",
            "Government's justification is inadequate.",
            "Substantive due process rights were violated.",
            "Remedies are warranted for violation."
        ],
        resolution_strategy="Apply Mathews v Eldridge balancing test; review procedures; assess impact.",
        entity_scope="Individuals affected by government action",
        confidence=0.94,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Mathews v Eldridge, 424 U.S. 319 (1976)"
    ),
    DoctrineBlock(
        topic="Equal Protection",
        keywords=["discrimination", "suspect class", "rational basis", "strict scrutiny", "intermediate scrutiny", "government classification", "fundamental rights"],
        conclusion_template="Evaluate whether government classification discriminates against a protected class. Apply appropriate level of scrutiny. Assess justification for the classification. Conclude on constitutionality under the Equal Protection Clause.",
        reasoning_framework="""1. Identify the government classification at issue.
2. Determine if a suspect or quasi-suspect class is affected.
3. Analyze the nature of the right involved (fundamental or not).
4. Apply strict, intermediate, or rational basis scrutiny as appropriate.
5. Assess the government's interest and justification.
6. Evaluate whether the classification is narrowly tailored.
7. Review relevant constitutional provisions and case law.
8. Consider the impact on affected individuals.
9. Examine any evidence of discriminatory intent or effect.
10. Analyze the scope and breadth of the classification.
11. Review remedies for equal protection violations.
12. Consider public policy implications.
13. Evaluate the scope of judicial review.
14. Examine exceptions or limitations.
15. Conclude on compliance with equal protection.""",
        key_factors=["classification", "protected class", "level of scrutiny", "government interest", "tailoring"],
        primary_authority=["U.S. Const. amend. XIV", "Brown v Board of Education, 347 U.S. 483 (1954)", "United States v Virginia, 518 U.S. 515 (1996)"],
        burden_holder="Plaintiff",
        adversary_position="Classification is rationally related to a legitimate government interest.",
        counter_arguments=[
            "Classification affects a suspect class.",
            "Government interest is not compelling.",
            "Classification is not narrowly tailored.",
            "Discriminatory intent is evidenced.",
            "Fundamental rights are implicated.",
            "Remedies are warranted for violation."
        ],
        resolution_strategy="Apply appropriate level of scrutiny; review evidence; assess impact.",
        entity_scope="Individuals affected by government classification",
        confidence=0.93,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Brown v Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Statutory Interpretation",
        keywords=["plain meaning", "legislative intent", "canons of construction", "ambiguity", "context", "extrinsic evidence", "purpose"],
        conclusion_template="Interpret the statute using plain meaning and legislative intent. Apply canons of construction and consider context. Resolve ambiguities using extrinsic evidence. Conclude on the statute's meaning and application.",
        reasoning_framework="""1. Identify the statutory provision at issue.
2. Apply the plain meaning rule to the text.
3. Analyze legislative history and intent.
4. Consider the context of the statute within the broader legal framework.
5. Apply relevant canons of construction.
6. Assess ambiguity and potential interpretations.
7. Review extrinsic evidence as necessary.
8. Evaluate the purpose and policy underlying the statute.
9. Examine judicial interpretations and precedent.
10. Consider the impact on affected parties.
11. Analyze any exceptions or limitations.
12. Review remedies for misinterpretation.
13. Evaluate the scope of judicial review.
14. Examine the relationship to other statutes.
15. Conclude on the statute's meaning and application.""",
        key_factors=["text", "intent", "canons", "ambiguity", "context"],
        primary_authority=["Chevron U.S.A., Inc. v Natural Resources Defense Council, Inc., 467 U.S. 837 (1984)", "Holy Trinity Church v United States, 143 U.S. 457 (1892)", "Scalia & Garner, Reading Law (2012)"],
        burden_holder="Plaintiff or party asserting interpretation",
        adversary_position="Statute's plain meaning supports a different interpretation.",
        counter_arguments=[
            "Legislative intent supports this interpretation.",
            "Canons of construction resolve ambiguity.",
            "Extrinsic evidence clarifies meaning.",
            "Purpose aligns with interpretation.",
            "Judicial precedent supports this view.",
            "Context favors this reading."
        ],
        resolution_strategy="Apply interpretive tools; review legislative history; resolve ambiguity.",
        entity_scope="Parties subject to statute",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Chevron U.S.A., Inc. v Natural Resources Defense Council, Inc., 467 U.S. 837 (1984)"
    ),
    DoctrineBlock(
        topic="Regulatory Takings",
        keywords=["eminent domain", "just compensation", "public use", "regulation", "property rights", "Penn Central", "Lucas"],
        conclusion_template="Assess whether government regulation constitutes a taking. Analyze the impact on property rights and economic value. Evaluate public use and just compensation requirements. Conclude on the legality of the regulation under takings doctrine.",
        reasoning_framework="""1. Identify the government regulation at issue.
2. Determine if the regulation restricts property rights.
3. Analyze the economic impact on the property owner.
4. Apply Penn Central and Lucas standards for regulatory takings.
5. Assess the character of the government action.
6. Evaluate the extent of interference with investment-backed expectations.
7. Review relevant constitutional provisions and case law.
8. Consider public use and just compensation requirements.
9. Examine any exceptions or limitations.
10. Analyze remedies for takings violations.
11. Evaluate the scope of judicial review.
12. Consider public policy implications.
13. Assess the impact on affected parties.
14. Review the relationship to other property regulations.
15. Conclude on the legality of the regulation.""",
        key_factors=["regulation", "economic impact", "property rights", "public use", "just compensation"],
        primary_authority=["Penn Central Transportation Co. v New York City, 438 U.S. 104 (1978)", "Lucas v South Carolina Coastal Council, 505 U.S. 1003 (1992)", "U.S. Const. amend. V"],
        burden_holder="Plaintiff",
        adversary_position="Regulation does not constitute a taking; no compensation is required.",
        counter_arguments=[
            "Economic impact is severe and total.",
            "Regulation destroys investment-backed expectations.",
            "Character of government action favors finding a taking.",
            "No public use justification.",
            "Just compensation is required.",
            "Precedent supports finding a taking."
        ],
        resolution_strategy="Apply Penn Central and Lucas tests; review evidence; assess impact.",
        entity_scope="Property owners affected by regulation",
        confidence=0.89,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Penn Central Transportation Co. v New York City, 438 U.S. 104 (1978)"
    ),
    DoctrineBlock(
        topic="Employment Discrimination",
        keywords=["protected class", "disparate impact", "disparate treatment", "Title VII", "burden shifting", "reasonable accommodation", "retaliation"],
        conclusion_template="Analyze whether the plaintiff is a member of a protected class. Evaluate evidence of disparate treatment or impact. Apply burden-shifting framework. Assess reasonable accommodation and retaliation claims. Conclude on liability for employment discrimination.",
        reasoning_framework="""1. Identify the protected class status of the plaintiff.
2. Analyze evidence of disparate treatment or impact.
3. Apply McDonnell Douglas burden-shifting framework.
4. Assess employer's legitimate, non-discriminatory reasons.
5. Evaluate pretext for discrimination.
6. Review reasonable accommodation requirements.
7. Consider retaliation claims and evidence.
8. Examine relevant statutes and case law.
9. Assess remedies for discrimination.
10. Evaluate the impact on affected parties.
11. Review public policy implications.
12. Analyze exceptions or limitations.
13. Consider the scope of judicial review.
14. Examine statistical evidence.
15. Conclude on liability and remedies.""",
        key_factors=["protected class", "disparate treatment", "burden shifting", "accommodation", "retaliation"],
        primary_authority=["Title VII of the Civil Rights Act of 1964", "McDonnell Douglas Corp. v Green, 411 U.S. 792 (1973)", "42 U.S.C. §2000e"],
        burden_holder="Plaintiff",
        adversary_position="Employer acted for legitimate, non-discriminatory reasons.",
        counter_arguments=[
            "Employer's reasons are pretextual.",
            "Statistical evidence supports discrimination.",
            "Reasonable accommodation was denied.",
            "Retaliation is evidenced by adverse action.",
            "Protected class status is clear.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply burden-shifting analysis; review evidence; assess remedies.",
        entity_scope="Employees and employers",
        confidence=0.92,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="McDonnell Douglas Corp. v Green, 411 U.S. 792 (1973)"
    ),
    DoctrineBlock(
        topic="Wrongful Termination",
        keywords=["at-will employment", "public policy", "retaliation", "constructive discharge", "whistleblower", "employment contract", "good faith"],
        conclusion_template="Determine whether termination violated public policy or contractual obligations. Analyze evidence of retaliation or constructive discharge. Assess whistleblower protections. Conclude on liability for wrongful termination.",
        reasoning_framework="""1. Identify the nature of the employment relationship (at-will, contract).
2. Analyze the grounds for termination.
3. Assess whether termination violated public policy.
4. Evaluate evidence of retaliation or constructive discharge.
5. Review whistleblower protections and statutes.
6. Examine employment contract terms.
7. Consider implied covenant of good faith and fair dealing.
8. Analyze remedies for wrongful termination.
9. Review relevant case law and statutes.
10. Assess impact on affected parties.
11. Consider public policy implications.
12. Evaluate exceptions or limitations.
13. Analyze scope of judicial review.
14. Examine employer's legitimate reasons.
15. Conclude on liability and remedies.""",
        key_factors=["employment relationship", "public policy", "retaliation", "whistleblower", "good faith"],
        primary_authority=["California Labor Code §1102.5", "Foley v Interactive Data Corp., 47 Cal.3d 654 (1988)", "Title VII of the Civil Rights Act of 1964"],
        burden_holder="Plaintiff",
        adversary_position="Termination was lawful and based on legitimate reasons.",
        counter_arguments=[
            "Termination violated public policy.",
            "Retaliation is evidenced by timing and conduct.",
            "Whistleblower protections apply.",
            "Constructive discharge is supported by facts.",
            "Implied covenant was breached.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply public policy and contract analysis; review evidence; assess remedies.",
        entity_scope="Employees and employers",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Foley v Interactive Data Corp., 47 Cal.3d 654 (1988)"
    ),
    DoctrineBlock(
        topic="Patent Infringement",
        keywords=["claims", "novelty", "non-obviousness", "direct infringement", "indirect infringement", "Markman hearing", "prior art"],
        conclusion_template="Analyze patent claims and accused product or process. Evaluate novelty and non-obviousness. Assess evidence of direct or indirect infringement. Conclude on liability and available remedies.",
        reasoning_framework="""1. Identify the patent and claims at issue.
2. Analyze the accused product or process for overlap with claims.
3. Evaluate novelty and non-obviousness of the patent.
4. Review prior art and its impact on validity.
5. Assess evidence of direct or indirect infringement.
6. Apply claim construction principles (Markman hearing).
7. Examine defenses (invalidity, non-infringement).
8. Review relevant statutes and case law.
9. Analyze remedies for infringement.
10. Consider willful infringement and enhanced damages.
11. Evaluate impact on affected parties.
12. Review public policy implications.
13. Assess exceptions or limitations.
14. Analyze scope of judicial review.
15. Conclude on liability and remedies.""",
        key_factors=["claims", "novelty", "non-obviousness", "infringement", "prior art"],
        primary_authority=["35 U.S.C. §271", "Markman v Westview Instruments, Inc., 517 U.S. 370 (1996)", "35 U.S.C. §102"],
        burden_holder="Plaintiff",
        adversary_position="Accused product does not infringe or patent is invalid.",
        counter_arguments=[
            "Claim construction supports infringement.",
            "Novelty and non-obviousness are established.",
            "Prior art does not invalidate patent.",
            "Indirect infringement is evidenced.",
            "Remedies are warranted.",
            "Enhanced damages apply for willful infringement."
        ],
        resolution_strategy="Apply claim construction; review evidence; assess remedies.",
        entity_scope="Patent holders and alleged infringers",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Markman v Westview Instruments, Inc., 517 U.S. 370 (1996)"
    ),
    DoctrineBlock(
        topic="Copyright Fair Use",
        keywords=["purpose", "nature", "amount", "effect", "transformative", "infringement", "market"],
        conclusion_template="Evaluate the purpose and character of the use. Analyze the nature of the copyrighted work. Assess the amount and substantiality used. Consider the effect on the market. Conclude on the applicability of fair use defense.",
        reasoning_framework="""1. Identify the copyrighted work and alleged use.
2. Analyze the purpose and character of the use (commercial, educational, transformative).
3. Assess the nature of the copyrighted work (creative, factual).
4. Evaluate the amount and substantiality of the portion used.
5. Consider the effect of the use on the market for the original work.
6. Review relevant statutes and case law.
7. Examine evidence of transformative use.
8. Analyze defenses to infringement.
9. Assess remedies for infringement.
10. Evaluate impact on affected parties.
11. Review public policy implications.
12. Consider exceptions or limitations.
13. Analyze scope of judicial review.
14. Examine licensing or permissions.
15. Conclude on fair use applicability.""",
        key_factors=["purpose", "nature", "amount", "effect", "transformative"],
        primary_authority=["17 U.S.C. §107", "Campbell v Acuff-Rose Music, Inc., 510 U.S. 569 (1994)", "Sony Corp. of America v Universal City Studios, Inc., 464 U.S. 417 (1984)"],
        burden_holder="Defendant",
        adversary_position="Use is not fair and constitutes infringement.",
        counter_arguments=[
            "Use is transformative and non-commercial.",
            "Amount used is minimal and not substantial.",
            "Market effect is negligible.",
            "Nature of work favors fair use.",
            "Statutory factors support fair use.",
            "Precedent supports fair use defense."
        ],
        resolution_strategy="Apply four-factor fair use test; review evidence; assess impact.",
        entity_scope="Copyright holders and alleged infringers",
        confidence=0.89,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Campbell v Acuff-Rose Music, Inc., 510 U.S. 569 (1994)"
    ),
    DoctrineBlock(
        topic="Bankruptcy Discharge",
        keywords=["dischargeable debt", "non-dischargeable", "Chapter 7", "Chapter 13", "automatic stay", "fraud", "priority"],
        conclusion_template="Identify debts subject to discharge. Analyze exceptions for non-dischargeable debts. Evaluate impact of automatic stay and bankruptcy chapter. Conclude on the scope and effect of bankruptcy discharge.",
        reasoning_framework="""1. Identify the bankruptcy chapter filed (7, 13).
2. List all debts and classify as dischargeable or non-dischargeable.
3. Analyze exceptions for fraud, priority, and statutory exclusions.
4. Evaluate impact of automatic stay on creditors.
5. Review relevant statutes and case law.
6. Assess remedies for violation of discharge.
7. Consider public policy implications.
8. Examine scope of judicial review.
9. Analyze impact on affected parties.
10. Review procedures for objecting to discharge.
11. Assess evidence of fraud or misconduct.
12. Evaluate impact of reaffirmation agreements.
13. Analyze exceptions or limitations.
14. Examine relationship to other insolvency laws.
15. Conclude on discharge scope and effect.""",
        key_factors=["chapter", "dischargeable debt", "exceptions", "automatic stay", "priority"],
        primary_authority=["11 U.S.C. §523", "11 U.S.C. §727", "Grogan v Garner, 498 U.S. 279 (1991)"],
        burden_holder="Debtor",
        adversary_position="Debt is non-dischargeable due to fraud or statutory exclusion.",
        counter_arguments=[
            "Debt meets criteria for discharge.",
            "No evidence of fraud or misconduct.",
            "Automatic stay protects debtor.",
            "Priority debts are properly classified.",
            "Procedures were followed.",
            "Remedies are warranted for violation."
        ],
        resolution_strategy="Apply statutory exclusions; review evidence; assess impact.",
        entity_scope="Debtors and creditors",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Grogan v Garner, 498 U.S. 279 (1991)"
    ),
    DoctrineBlock(
        topic="Environmental Compliance",
        keywords=["EPA", "Clean Air Act", "Clean Water Act", "regulation", "permit", "violation", "remediation"],
        conclusion_template="Identify applicable environmental regulations. Analyze compliance with permits and standards. Assess evidence of violation and remediation efforts. Conclude on liability and required corrective actions.",
        reasoning_framework="""1. Identify applicable environmental statutes and regulations.
2. Analyze permit requirements and compliance status.
3. Assess evidence of violation (emissions, discharges).
4. Evaluate remediation efforts and corrective actions.
5. Review relevant statutes and case law.
6. Consider penalties and enforcement actions.
7. Examine impact on affected parties and environment.
8. Analyze public policy implications.
9. Review scope of judicial review.
10. Assess exceptions or limitations.
11. Evaluate procedures for reporting and remediation.
12. Analyze relationship to other regulatory frameworks.
13. Examine evidence of ongoing compliance.
14. Assess remedies for violation.
15. Conclude on liability and corrective actions.""",
        key_factors=["regulation", "permit", "violation", "remediation", "penalties"],
        primary_authority=["Clean Air Act, 42 U.S.C. §7401", "Clean Water Act, 33 U.S.C. §1251", "CERCLA, 42 U.S.C. §9601"],
        burden_holder="Regulator",
        adversary_position="Entity is in compliance or violation is minor.",
        counter_arguments=[
            "Violation is significant and ongoing.",
            "Remediation efforts are insufficient.",
            "Permit requirements were not met.",
            "Penalties are warranted.",
            "Statutory standards were breached.",
            "Public harm is evidenced."
        ],
        resolution_strategy="Apply statutory standards; review evidence; assess remedies.",
        entity_scope="Regulated entities and government",
        confidence=0.88,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Clean Air Act, 42 U.S.C. §7401"
    ),
    DoctrineBlock(
        topic="Securities Fraud",
        keywords=["material misrepresentation", "scienter", "reliance", "loss causation", "Rule 10b-5", "SEC", "insider trading"],
        conclusion_template="Analyze evidence of material misrepresentation or omission. Assess scienter and reliance by investors. Evaluate loss causation and application of Rule 10b-5. Conclude on liability for securities fraud.",
        reasoning_framework="""1. Identify the alleged misrepresentation or omission.
2. Analyze materiality of the information.
3. Assess scienter (intent or recklessness).
4. Evaluate reliance by investors.
5. Review loss causation and damages.
6. Apply Rule 10b-5 standards.
7. Examine evidence of insider trading.
8. Review relevant statutes and case law.
9. Analyze remedies for securities fraud.
10. Consider public policy implications.
11. Assess impact on affected parties.
12. Review scope of judicial review.
13. Analyze exceptions or limitations.
14. Examine procedures for reporting and enforcement.
15. Conclude on liability and remedies.""",
        key_factors=["materiality", "scienter", "reliance", "loss causation", "Rule 10b-5"],
        primary_authority=["Securities Exchange Act of 1934 §10(b)", "SEC Rule 10b-5", "Basic Inc. v Levinson, 485 U.S. 224 (1988)"],
        burden_holder="Plaintiff",
        adversary_position="Misrepresentation was not material or reliance was absent.",
        counter_arguments=[
            "Information was material to investors.",
            "Scienter is evidenced by conduct.",
            "Reliance is presumed under fraud-on-the-market theory.",
            "Loss causation is established.",
            "Rule 10b-5 applies.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply Rule 10b-5 elements; review evidence; assess remedies.",
        entity_scope="Investors and issuers",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Basic Inc. v Levinson, 485 U.S. 224 (1988)"
    ),
    DoctrineBlock(
        topic="Healthcare HIPAA Compliance",
        keywords=["privacy", "security", "protected health information", "breach", "covered entity", "authorization", "disclosure"],
        conclusion_template="Identify protected health information and covered entities. Analyze compliance with privacy and security standards. Assess evidence of breach or unauthorized disclosure. Conclude on liability and corrective actions under HIPAA.",
        reasoning_framework="""1. Identify protected health information (PHI) involved.
2. Determine covered entity status.
3. Analyze compliance with HIPAA privacy and security standards.
4. Assess evidence of breach or unauthorized disclosure.
5. Review relevant statutes and case law.
6. Evaluate impact on affected parties.
7. Consider penalties and enforcement actions.
8. Examine remediation and corrective actions.
9. Analyze public policy implications.
10. Review scope of judicial review.
11. Assess exceptions or limitations.
12. Evaluate procedures for reporting and notification.
13. Examine evidence of ongoing compliance.
14. Analyze remedies for violation.
15. Conclude on liability and corrective actions.""",
        key_factors=["PHI", "covered entity", "privacy", "security", "breach"],
        primary_authority=["HIPAA, 42 U.S.C. §1320d", "45 CFR Parts 160, 164", "HHS Guidance"],
        burden_holder="Regulator",
        adversary_position="Entity complied with all HIPAA requirements.",
        counter_arguments=[
            "PHI was disclosed without authorization.",
            "Security standards were breached.",
            "Remediation was insufficient.",
            "Penalties are warranted.",
            "Statutory standards were violated.",
            "Public harm is evidenced."
        ],
        resolution_strategy="Apply HIPAA standards; review evidence; assess remedies.",
        entity_scope="Healthcare providers and patients",
        confidence=0.89,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="HIPAA, 42 U.S.C. §1320d"
    ),
    DoctrineBlock(
        topic="Immigration Asylum",
        keywords=["persecution", "well-founded fear", "protected grounds", "credible testimony", "country conditions", "refugee", "burden of proof"],
        conclusion_template="Assess whether applicant has a well-founded fear of persecution. Analyze evidence of protected grounds and credible testimony. Evaluate country conditions and burden of proof. Conclude on eligibility for asylum.",
        reasoning_framework="""1. Identify the applicant's country of origin and protected grounds.
2. Assess evidence of past persecution or well-founded fear.
3. Analyze credible testimony and supporting documentation.
4. Evaluate country conditions and risk of harm.
5. Review relevant statutes and case law.
6. Consider burden of proof and standard of review.
7. Examine impact on affected parties.
8. Analyze public policy implications.
9. Review scope of judicial review.
10. Assess exceptions or limitations.
11. Evaluate procedures for asylum application.
12. Analyze remedies for denial.
13. Examine evidence of ongoing risk.
14. Assess eligibility for other forms of relief.
15. Conclude on asylum eligibility.""",
        key_factors=["persecution", "well-founded fear", "protected grounds", "country conditions", "burden of proof"],
        primary_authority=["Immigration and Nationality Act §208", "INS v Cardoza-Fonseca, 480 U.S. 421 (1987)", "8 U.S.C. §1158"],
        burden_holder="Applicant",
        adversary_position="Applicant lacks credible evidence or does not meet protected grounds.",
        counter_arguments=[
            "Credible testimony supports claim.",
            "Country conditions evidence risk.",
            "Protected grounds are established.",
            "Burden of proof is met.",
            "Past persecution is evidenced.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply statutory standards; review evidence; assess eligibility.",
        entity_scope="Asylum applicants and government",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="INS v Cardoza-Fonseca, 480 U.S. 421 (1987)"
    ),
    DoctrineBlock(
        topic="Family Law Custody",
        keywords=["best interests", "parental rights", "joint custody", "sole custody", "child welfare", "visitation", "fitness"],
        conclusion_template="Analyze the best interests of the child. Evaluate parental rights, fitness, and welfare. Assess evidence for joint or sole custody and visitation. Conclude on custody arrangement.",
        reasoning_framework="""1. Identify the child and parents involved.
2. Analyze evidence of parental fitness and rights.
3. Assess the best interests of the child.
4. Evaluate welfare, safety, and stability.
5. Review relevant statutes and case law.
6. Consider evidence for joint or sole custody.
7. Examine visitation arrangements.
8. Analyze impact on affected parties.
9. Review public policy implications.
10. Assess exceptions or limitations.
11. Evaluate scope of judicial review.
12. Examine procedures for custody determination.
13. Analyze remedies for violation.
14. Assess evidence of abuse or neglect.
15. Conclude on custody arrangement.""",
        key_factors=["best interests", "parental rights", "fitness", "welfare", "visitation"],
        primary_authority=["Uniform Child Custody Jurisdiction and Enforcement Act", "California Family Code §3011", "Troxel v Granville, 530 U.S. 57 (2000)"],
        burden_holder="Petitioner",
        adversary_position="Other parent is more fit or arrangement is not in child's best interests.",
        counter_arguments=[
            "Best interests favor this arrangement.",
            "Parental fitness is evidenced.",
            "Child welfare is paramount.",
            "Visitation supports stability.",
            "Statutory standards are met.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply best interests standard; review evidence; assess arrangement.",
        entity_scope="Children and parents",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Troxel v Granville, 530 U.S. 57 (2000)"
    ),
    DoctrineBlock(
        topic="Criminal Mens Rea",
        keywords=["intent", "knowledge", "recklessness", "negligence", "actus reus", "specific intent", "general intent"],
        conclusion_template="Identify the mental state required for the offense. Analyze evidence of intent, knowledge, recklessness, or negligence. Assess actus reus and statutory requirements. Conclude on criminal liability.",
        reasoning_framework="""1. Identify the offense and statutory requirements.
2. Analyze evidence of mental state (intent, knowledge, recklessness, negligence).
3. Assess actus reus and its relationship to mens rea.
4. Evaluate specific versus general intent.
5. Review relevant statutes and case law.
6. Consider defenses (mistake, insanity).
7. Examine impact on affected parties.
8. Analyze public policy implications.
9. Review scope of judicial review.
10. Assess exceptions or limitations.
11. Evaluate procedures for proving mens rea.
12. Analyze remedies for wrongful conviction.
13. Examine evidence of conduct and motive.
14. Assess burden of proof.
15. Conclude on criminal liability.""",
        key_factors=["intent", "knowledge", "recklessness", "negligence", "actus reus"],
        primary_authority=["Model Penal Code §2.02", "United States v Bailey, 444 U.S. 394 (1980)", "California Penal Code §20"],
        burden_holder="Prosecution",
        adversary_position="Defendant lacked required mental state.",
        counter_arguments=[
            "Evidence supports intent or knowledge.",
            "Recklessness is established by conduct.",
            "Negligence meets statutory requirements.",
            "Actus reus is clear.",
            "Defenses are insufficient.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply mens rea standards; review evidence; assess liability.",
        entity_scope="Defendants and prosecution",
        confidence=0.92,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Model Penal Code §2.02"
    ),
    DoctrineBlock(
        topic="Real Property Conveyance",
        keywords=["deed", "title", "recording", "delivery", "warranty", "encumbrance", "grantor"],
        conclusion_template="Identify the type of deed and parties involved. Analyze delivery, recording, and warranty provisions. Assess title and encumbrances. Conclude on validity of conveyance.",
        reasoning_framework="""1. Identify the property and parties to conveyance.
2. Analyze the type of deed (warranty, quitclaim, grant).
3. Assess delivery and acceptance of deed.
4. Evaluate recording requirements and priority.
5. Review warranty provisions and encumbrances.
6. Examine title and chain of ownership.
7. Consider statutory requirements for conveyance.
8. Analyze impact on affected parties.
9. Review relevant statutes and case law.
10. Assess exceptions or limitations.
11. Evaluate scope of judicial review.
12. Examine remedies for defective conveyance.
13. Analyze evidence of fraud or mistake.
14. Assess impact of unrecorded interests.
15. Conclude on validity and enforceability.""",
        key_factors=["deed", "delivery", "recording", "warranty", "encumbrance"],
        primary_authority=["California Civil Code §1091", "Restatement (Third) of Property: Mortgages", "St. Louis v. Smith, 184 U.S. 239 (1902)"],
        burden_holder="Grantor",
        adversary_position="Conveyance is invalid due to defective deed or lack of delivery.",
        counter_arguments=[
            "Deed was properly delivered and accepted.",
            "Recording establishes priority.",
            "Warranty provisions are enforceable.",
            "Title is clear.",
            "Encumbrances are disclosed.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply statutory and common law standards; review evidence; assess validity.",
        entity_scope="Grantors and grantees",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="California Civil Code §1091"
    ),
    DoctrineBlock(
        topic="Landlord-Tenant Law",
        keywords=["lease", "possession", "rent", "eviction", "habitability", "security deposit", "quiet enjoyment"],
        conclusion_template="Identify lease terms and parties. Analyze possession, rent, and habitability requirements. Assess evidence for eviction or breach. Conclude on rights and remedies under landlord-tenant law.",
        reasoning_framework="""1. Identify the lease and parties involved.
2. Analyze lease terms and duration.
3. Assess possession and rent payment.
4. Evaluate habitability and quiet enjoyment requirements.
5. Review evidence for eviction or breach.
6. Examine security deposit and return.
7. Consider statutory requirements and remedies.
8. Analyze impact on affected parties.
9. Review relevant statutes and case law.
10. Assess exceptions or limitations.
11. Evaluate scope of judicial review.
12. Examine procedures for eviction.
13. Analyze remedies for breach.
14. Assess evidence of retaliation or discrimination.
15. Conclude on rights and remedies.""",
        key_factors=["lease", "possession", "rent", "habitability", "eviction"],
        primary_authority=["California Civil Code §1941", "Uniform Residential Landlord and Tenant Act", "Hilder v St. Peter, 476 A.2d 612 (Vt. 1984)"],
        burden_holder="Landlord",
        adversary_position="Tenant breached lease or habitability requirements were met.",
        counter_arguments=[
            "Habitability was not maintained.",
            "Eviction was retaliatory.",
            "Security deposit was not returned.",
            "Quiet enjoyment was breached.",
            "Lease terms favor tenant.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply statutory standards; review evidence; assess remedies.",
        entity_scope="Landlords and tenants",
        confidence=0.89,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Hilder v St. Peter, 476 A.2d 612 (Vt. 1984)"
    ),
    DoctrineBlock(
        topic="Antitrust Law",
        keywords=["monopoly", "restraint of trade", "Sherman Act", "market power", "price fixing", "merger", "competition"],
        conclusion_template="Identify alleged antitrust violation. Analyze market power and restraint of trade. Evaluate evidence of monopoly, price fixing, or anti-competitive conduct. Conclude on liability under antitrust law.",
        reasoning_framework="""1. Identify the alleged violation and parties involved.
2. Analyze market power and relevant market definition.
3. Assess evidence of monopoly or restraint of trade.
4. Evaluate price fixing, merger, or anti-competitive conduct.
5. Review relevant statutes and case law.
6. Consider impact on competition and consumers.
7. Examine remedies for violation.
8. Analyze public policy implications.
9. Review scope of judicial review.
10. Assess exceptions or limitations.
11. Evaluate procedures for enforcement.
12. Analyze evidence of intent and conduct.
13. Assess impact on affected parties.
14. Examine defenses (pro-competitive justification).
15. Conclude on liability and remedies.""",
        key_factors=["market power", "restraint of trade", "price fixing", "merger", "competition"],
        primary_authority=["Sherman Act, 15 U.S.C. §1", "Clayton Act, 15 U.S.C. §12", "United States v Microsoft Corp., 253 F.3d 34 (D.C. Cir. 2001)"],
        burden_holder="Plaintiff",
        adversary_position="Conduct was pro-competitive or market power is lacking.",
        counter_arguments=[
            "Market power is established.",
            "Restraint of trade is evidenced.",
            "Price fixing is clear.",
            "Merger reduces competition.",
            "Remedies are warranted.",
            "Statutory standards are met."
        ],
        resolution_strategy="Apply antitrust standards; review evidence; assess remedies.",
        entity_scope="Businesses and consumers",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="United States v Microsoft Corp., 253 F.3d 34 (D.C. Cir. 2001)"
    ),
    DoctrineBlock(
        topic="Civil Procedure Jurisdiction",
        keywords=["personal jurisdiction", "subject matter", "minimum contacts", "venue", "forum", "long-arm statute", "service"],
        conclusion_template="Identify the court and parties. Analyze personal and subject matter jurisdiction. Assess minimum contacts and venue. Conclude on the court's authority to hear the case.",
        reasoning_framework="""1. Identify the court and parties involved.
2. Analyze personal jurisdiction and minimum contacts.
3. Assess subject matter jurisdiction.
4. Evaluate venue and forum selection.
5. Review long-arm statute applicability.
6. Examine service of process requirements.
7. Consider statutory and constitutional standards.
8. Analyze impact on affected parties.
9. Review relevant statutes and case law.
10. Assess exceptions or limitations.
11. Evaluate scope of judicial review.
12. Examine procedures for challenging jurisdiction.
13. Analyze remedies for improper jurisdiction.
14. Assess evidence of consent or waiver.
15. Conclude on court's authority.""",
        key_factors=["personal jurisdiction", "subject matter", "minimum contacts", "venue", "service"],
        primary_authority=["International Shoe Co. v Washington, 326 U.S. 310 (1945)", "28 U.S.C. §1332", "Fed. R. Civ. P. 4"],
        burden_holder="Plaintiff",
        adversary_position="Court lacks jurisdiction due to insufficient contacts or improper venue.",
        counter_arguments=[
            "Minimum contacts are established.",
            "Subject matter jurisdiction is clear.",
            "Venue is proper.",
            "Service was completed.",
            "Consent was given.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply jurisdictional standards; review evidence; assess authority.",
        entity_scope="Litigants and courts",
        confidence=0.92,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="International Shoe Co. v Washington, 326 U.S. 310 (1945)"
    ),
    DoctrineBlock(
        topic="Evidence Hearsay",
        keywords=["hearsay", "exception", "declarant", "statement", "admissibility", "confrontation", "reliability"],
        conclusion_template="Identify the statement and declarant. Analyze whether the statement is hearsay and applicable exceptions. Assess admissibility and reliability. Conclude on evidentiary status.",
        reasoning_framework="""1. Identify the statement and declarant.
2. Analyze whether the statement is hearsay.
3. Assess applicability of exceptions (business records, excited utterance, etc.).
4. Evaluate reliability and necessity.
5. Review confrontation clause requirements.
6. Examine impact on affected parties.
7. Consider statutory and constitutional standards.
8. Review relevant statutes and case law.
9. Analyze procedures for admitting hearsay.
10. Assess exceptions or limitations.
11. Evaluate scope of judicial review.
12. Examine remedies for improper admission.
13. Analyze evidence of reliability.
14. Assess impact on trial outcome.
15. Conclude on admissibility.""",
        key_factors=["hearsay", "exception", "declarant", "statement", "reliability"],
        primary_authority=["Fed. R. Evid. 801", "Fed. R. Evid. 803", "Crawford v Washington, 541 U.S. 36 (2004)"],
        burden_holder="Proponent of evidence",
        adversary_position="Statement is inadmissible hearsay.",
        counter_arguments=[
            "Exception applies (business records, excited utterance).",
            "Statement is reliable.",
            "Declarant is unavailable.",
            "Confrontation clause is satisfied.",
            "Necessity is established.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply hearsay rules; review evidence; assess admissibility.",
        entity_scope="Litigants and courts",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Crawford v Washington, 541 U.S. 36 (2004)"
    ),
    DoctrineBlock(
        topic="Tax Evasion vs Avoidance",
        keywords=["tax evasion", "tax avoidance", "intent", "statutory compliance", "IRS", "fraud", "penalty"],
        conclusion_template="Distinguish between lawful tax avoidance and unlawful tax evasion. Analyze evidence of intent and statutory compliance. Assess IRS procedures and penalties. Conclude on liability.",
        reasoning_framework="""1. Identify the taxpayer and relevant transactions.
2. Analyze evidence of intent to evade taxes.
3. Assess statutory compliance and reporting.
4. Evaluate distinction between avoidance and evasion.
5. Review IRS procedures and penalties.
6. Examine impact on affected parties.
7. Consider statutory and regulatory standards.
8. Review relevant statutes and case law.
9. Analyze remedies for violation.
10. Assess exceptions or limitations.
11. Evaluate scope of judicial review.
12. Examine evidence of fraud or misconduct.
13. Analyze public policy implications.
14. Assess burden of proof.
15. Conclude on liability and penalties.""",
        key_factors=["intent", "statutory compliance", "avoidance", "evasion", "penalty"],
        primary_authority=["26 U.S.C. §7201", "Cheek v United States, 498 U.S. 192 (1991)", "IRS Publication 17"],
        burden_holder="Government",
        adversary_position="Conduct was lawful avoidance, not evasion.",
        counter_arguments=[
            "Intent to evade is evidenced.",
            "Statutory compliance was lacking.",
            "Fraud is established.",
            "Penalties are warranted.",
            "Remedies are appropriate.",
            "Public policy supports enforcement."
        ],
        resolution_strategy="Apply statutory standards; review evidence; assess penalties.",
        entity_scope="Taxpayers and government",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Cheek v United States, 498 U.S. 192 (1991)"
    ),
    DoctrineBlock(
        topic="Fiduciary Duty",
        keywords=["fiduciary", "duty of loyalty", "duty of care", "conflict of interest", "breach", "trustee", "beneficiary"],
        conclusion_template="Identify fiduciary relationship and duties owed. Analyze evidence of breach of loyalty or care. Assess conflicts of interest and remedies. Conclude on liability for breach.",
        reasoning_framework="""1. Identify the fiduciary relationship (trustee, agent, director).
2. Analyze duties of loyalty and care.
3. Assess evidence of breach or conflict of interest.
4. Evaluate impact on beneficiary or principal.
5. Review relevant statutes and case law.
6. Consider remedies for breach.
7. Examine public policy implications.
8. Analyze scope of judicial review.
9. Assess exceptions or limitations.
10. Evaluate procedures for enforcement.
11. Analyze evidence of self-dealing.
12. Assess impact on affected parties.
13. Review statutory requirements.
14. Examine defenses to breach.
15. Conclude on liability and remedies.""",
        key_factors=["fiduciary relationship", "duty of loyalty", "duty of care", "conflict of interest", "breach"],
        primary_authority=["Restatement (Third) of Agency §8.01", "Meinhard v Salmon, 249 N.Y. 458 (1928)", "Delaware General Corporation Law §144"],
        burden_holder="Plaintiff",
        adversary_position="No breach occurred or duties were fulfilled.",
        counter_arguments=[
            "Duty of loyalty was breached.",
            "Conflict of interest is evidenced.",
            "Duty of care was violated.",
            "Remedies are warranted.",
            "Statutory standards support liability.",
            "Beneficiary suffered harm."
        ],
        resolution_strategy="Apply fiduciary standards; review evidence; assess remedies.",
        entity_scope="Fiduciaries and beneficiaries",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Meinhard v Salmon, 249 N.Y. 458 (1928)"
    ),
    DoctrineBlock(
        topic="Professional Liability",
        keywords=["malpractice", "standard of care", "negligence", "causation", "damages", "expert testimony", "license"],
        conclusion_template="Identify professional relationship and standard of care. Analyze evidence of negligence, causation, and damages. Assess expert testimony and licensing. Conclude on liability for malpractice.",
        reasoning_framework="""1. Identify the professional relationship (doctor, lawyer, accountant).
2. Analyze applicable standard of care.
3. Assess evidence of negligence or breach.
4. Evaluate causation and damages.
5. Review expert testimony requirements.
6. Examine licensing and regulatory compliance.
7. Consider remedies for malpractice.
8. Analyze public policy implications.
9. Review relevant statutes and case law.
10. Assess exceptions or limitations.
11. Evaluate scope of judicial review.
12. Examine procedures for proving malpractice.
13. Analyze impact on affected parties.
14. Assess defenses to liability.
15. Conclude on liability and remedies.""",
        key_factors=["standard of care", "negligence", "causation", "damages", "expert testimony"],
        primary_authority=["Restatement (Second) of Torts §299A", "California Business & Professions Code §6149", "Brune v Belinkoff, 235 N.E.2d 793 (Mass. 1968)"],
        burden_holder="Plaintiff",
        adversary_position="Professional met standard of care or causation is lacking.",
        counter_arguments=[
            "Standard of care was breached.",
            "Expert testimony supports negligence.",
            "Causation is established.",
            "Damages are quantifiable.",
            "Remedies are warranted.",
            "Licensing requirements were violated."
        ],
        resolution_strategy="Apply malpractice standards; review evidence; assess remedies.",
        entity_scope="Professionals and clients",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Brune v Belinkoff, 235 N.E.2d 793 (Mass. 1968)"
    ),
    DoctrineBlock(
        topic="ADR/Arbitration",
        keywords=["arbitration", "agreement", "enforceability", "FAA", "award", "procedure", "neutral"],
        conclusion_template="Identify arbitration agreement and parties. Analyze enforceability and procedures. Assess award and neutrality. Conclude on validity and enforcement of arbitration.",
        reasoning_framework="""1. Identify the arbitration agreement and parties.
2. Analyze enforceability under FAA and state law.
3. Assess procedures for arbitration.
4. Evaluate neutrality and selection of arbitrator.
5. Review relevant statutes and case law.
6. Consider remedies for violation.
7. Examine public policy implications.
8. Analyze scope of judicial review.
9. Assess exceptions or limitations.
10. Evaluate procedures for confirming or vacating award.
11. Analyze impact on affected parties.
12. Review statutory requirements.
13. Examine defenses to enforcement.
14. Assess evidence of unconscionability.
15. Conclude on validity and enforcement.""",
        key_factors=["arbitration agreement", "enforceability", "procedure", "award", "neutrality"],
        primary_authority=["Federal Arbitration Act, 9 U.S.C. §1", "AT&T Mobility LLC v Concepcion, 563 U.S. 333 (2011)", "California Code of Civil Procedure §1281"],
        burden_holder="Party seeking enforcement",
        adversary_position="Agreement is unconscionable or procedures were violated.",
        counter_arguments=[
            "Agreement is enforceable under FAA.",
            "Procedures were followed.",
            "Award is valid.",
            "Neutrality was maintained.",
            "Remedies are warranted.",
            "Statutory standards are met."
        ],
        resolution_strategy="Apply FAA and state law standards; review evidence; assess enforceability.",
        entity_scope="Contracting parties",
        confidence=0.89,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="AT&T Mobility LLC v Concepcion, 563 U.S. 333 (2011)"
    ),
    DoctrineBlock(
        topic="Class Action Certification",
        keywords=["numerosity", "commonality", "typicality", "adequacy", "Rule 23", "representative", "manageability"],
        conclusion_template="Analyze numerosity, commonality, typicality, and adequacy of representation. Assess manageability and Rule 23 requirements. Conclude on certification of class action.",
        reasoning_framework="""1. Identify the proposed class and claims.
2. Analyze numerosity (sufficient number of members).
3. Assess commonality of legal or factual issues.
4. Evaluate typicality of representative claims.
5. Review adequacy of representation.
6. Consider manageability of class action.
7. Apply Rule 23 requirements.
8. Review relevant statutes and case law.
9. Analyze impact on affected parties.
10. Assess exceptions or limitations.
11. Evaluate scope of judicial review.
12. Examine procedures for certification.
13. Analyze remedies for improper certification.
14. Assess evidence of predominance and superiority.
15. Conclude on certification.""",
        key_factors=["numerosity", "commonality", "typicality", "adequacy", "manageability"],
        primary_authority=["Fed. R. Civ. P. 23", "Wal-Mart Stores, Inc. v Dukes, 564 U.S. 338 (2011)", "Amchem Products, Inc. v Windsor, 521 U.S. 591 (1997)"],
        burden_holder="Plaintiff",
        adversary_position="Class does not meet Rule 23 requirements.",
        counter_arguments=[
            "Numerosity is established.",
            "Commonality is clear.",
            "Typicality is evidenced.",
            "Adequacy of representation is met.",
            "Manageability is feasible.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply Rule 23 standards; review evidence; assess certification.",
        entity_scope="Class members and defendants",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Wal-Mart Stores, Inc. v Dukes, 564 U.S. 338 (2011)"
    ),
    DoctrineBlock(
        topic="Appeals Standards of Review",
        keywords=["de novo", "abuse of discretion", "clear error", "appellate", "record", "preservation", "remand"],
        conclusion_template="Identify the issue on appeal and applicable standard of review. Analyze the record and preservation of error. Assess whether the lower court abused discretion or committed clear error. Conclude on appellate outcome.",
        reasoning_framework="""1. Identify the issue on appeal.
2. Analyze applicable standard of review (de novo, abuse of discretion, clear error).
3. Assess preservation of error in the record.
4. Evaluate lower court's findings and reasoning.
5. Review relevant statutes and case law.
6. Consider remedies (affirm, reverse, remand).
7. Examine impact on affected parties.
8. Analyze public policy implications.
9. Review scope of appellate review.
10. Assess exceptions or limitations.
11. Evaluate procedures for appeal.
12. Analyze evidence in the record.
13. Assess impact on trial outcome.
14. Examine standards for factual and legal review.
15. Conclude on appellate outcome.""",
        key_factors=["standard of review", "record", "preservation", "abuse of discretion", "remand"],
        primary_authority=["Fed. R. Civ. P. 52(a)", "Anderson v Bessemer City, 470 U.S. 564 (1985)", "Ornelas v United States, 517 U.S. 690 (1996)"],
        burden_holder="Appellant",
        adversary_position="Lower court's findings are supported by the record.",
        counter_arguments=[
            "Error was preserved and is reviewable.",
            "Abuse of discretion is evidenced.",
            "Clear error is established.",
            "De novo review applies.",
            "Remand is warranted.",
            "Remedies are appropriate."
        ],
        resolution_strategy="Apply appellate standards; review record; assess outcome.",
        entity_scope="Appellants and appellees",
        confidence=0.91,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Anderson v Bessemer City, 470 U.S. 564 (1985)"
    ),
    DoctrineBlock(
        topic="UCC Article 2 - Sales",
        keywords=["merchant", "goods", "warranty", "acceptance", "rejection", "remedy", "risk of loss"],
        conclusion_template="Identify parties and goods involved. Analyze merchant status and warranty provisions. Assess acceptance, rejection, and remedies. Conclude on rights and obligations under UCC Article 2.",
        reasoning_framework="""1. Identify the parties and goods subject to sale.
2. Analyze merchant status and implications.
3. Assess warranty provisions (express, implied).
4. Evaluate acceptance and rejection procedures.
5. Review remedies for breach.
6. Examine risk of loss and allocation.
7. Consider statutory requirements and exceptions.
8. Analyze impact on affected parties.
9. Review relevant statutes and case law.
10. Assess scope of judicial review.
11. Evaluate procedures for enforcement.
12. Analyze evidence of breach or compliance.
13. Assess remedies for defective goods.
14. Examine defenses to liability.
15. Conclude on rights and obligations.""",
        key_factors=["merchant", "goods", "warranty", "acceptance", "remedy"],
        primary_authority=["UCC §2-314", "UCC §2-601", "UCC §2-709"],
        burden_holder="Plaintiff",
        adversary_position="Goods were accepted or warranty was not breached.",
        counter_arguments=[
            "Warranty was breached.",
            "Goods were properly rejected.",
            "Remedies are available.",
            "Merchant status applies.",
            "Risk of loss favors plaintiff.",
            "Statutory standards are met."
        ],
        resolution_strategy="Apply UCC Article 2 standards; review evidence; assess remedies.",
        entity_scope="Buyers and sellers",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="UCC §2-601"
    ),
    DoctrineBlock(
        topic="Insurance Bad Faith",
        keywords=["bad faith", "claim denial", "duty to defend", "coverage", "unreasonable", "settlement", "policyholder"],
        conclusion_template="Identify insurance policy and claim. Analyze evidence of bad faith denial or failure to defend. Assess coverage and reasonableness. Conclude on liability and remedies for bad faith.",
        reasoning_framework="""1. Identify the insurance policy and claim at issue.
2. Analyze duty to defend and coverage provisions.
3. Assess evidence of bad faith denial or delay.
4. Evaluate reasonableness of insurer's conduct.
5. Review relevant statutes and case law.
6. Consider remedies for bad faith.
7. Examine impact on affected parties.
8. Analyze public policy implications.
9. Review scope of judicial review.
10. Assess exceptions or limitations.
11. Evaluate procedures for enforcement.
12. Analyze evidence of settlement offers.
13. Assess damages for bad faith.
14. Examine defenses to liability.
15. Conclude on liability and remedies.""",
        key_factors=["bad faith", "claim denial", "duty to defend", "coverage", "settlement"],
        primary_authority=["California Insurance Code §790.03", "Gruenberg v Aetna Ins. Co., 9 Cal.3d 566 (1973)", "Restatement (Second) of Contracts §205"],
        burden_holder="Plaintiff",
        adversary_position="Insurer acted reasonably and coverage was excluded.",
        counter_arguments=[
            "Bad faith denial is evidenced.",
            "Duty to defend was breached.",
            "Coverage applies.",
            "Settlement was unreasonably withheld.",
            "Remedies are warranted.",
            "Statutory standards support liability."
        ],
        resolution_strategy="Apply bad faith standards; review evidence; assess remedies.",
        entity_scope="Policyholders and insurers",
        confidence=0.89,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Gruenberg v Aetna Ins. Co., 9 Cal.3d 566 (1973)"
    ),
    DoctrineBlock(
        topic="Maritime Law",
        keywords=["admiralty", "Jones Act", "seaman", "vessel", "maintenance", "cure", "injury"],
        conclusion_template="Identify maritime claim and parties. Analyze status as seaman and vessel. Assess injury, maintenance, and cure. Conclude on liability and remedies under maritime law.",
        reasoning_framework="""1. Identify the maritime claim and parties involved.
2. Analyze status as seaman and vessel.
3. Assess injury and causation.
4. Evaluate maintenance and cure obligations.
5. Review relevant statutes and case law.
6. Consider remedies for injury.
7. Examine impact on affected parties.
8. Analyze public policy implications.
9. Review scope of judicial review.
10. Assess exceptions or limitations.
11. Evaluate procedures for enforcement.
12. Analyze evidence of negligence or unseaworthiness.
13. Assess damages for injury.
14. Examine defenses to liability.
15. Conclude on liability and remedies.""",
        key_factors=["seaman", "vessel", "injury", "maintenance", "cure"],
        primary_authority=["Jones Act, 46 U.S.C. §30104", "Admiralty Rules", "McDermott International, Inc. v Wilander, 498 U.S. 337 (1991)"],
        burden_holder="Plaintiff",
        adversary_position="Plaintiff is not a seaman or injury was not work-related.",
        counter_arguments=[
            "Seaman status is established.",
            "Vessel meets statutory definition.",
            "Injury is work-related.",
            "Maintenance and cure obligations apply.",
            "Remedies are warranted.",
            "Statutory standards support liability."
        ],
        resolution_strategy="Apply Jones Act and admiralty standards; review evidence; assess remedies.",
        entity_scope="Seamen and vessel owners",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="McDermott International, Inc. v Wilander, 498 U.S. 337 (1991)"
    ),
    DoctrineBlock(
        topic="Native American Sovereignty",
        keywords=["tribal sovereignty", "jurisdiction", "treaty", "Indian country", "federal trust", "self-government", "commerce"],
        conclusion_template="Identify tribal status and jurisdiction. Analyze treaty rights and federal trust obligations. Assess self-government and commerce powers. Conclude on scope of Native American sovereignty.",
        reasoning_framework="""1. Identify the tribe and status under federal law.
2. Analyze treaty rights and obligations.
3. Assess jurisdiction over Indian country.
4. Evaluate federal trust responsibilities.
5. Review relevant statutes and case law.
6. Consider self-government and commerce powers.
7. Examine impact on affected parties.
8. Analyze public policy implications.
9. Review scope of judicial review.
10. Assess exceptions or limitations.
11. Evaluate procedures for enforcement.
12. Analyze evidence of sovereignty and autonomy.
13. Assess remedies for violation.
14. Examine defenses to jurisdiction.
15. Conclude on scope and application.""",
        key_factors=["tribal sovereignty", "jurisdiction", "treaty", "federal trust", "self-government"],
        primary_authority=["Worcester v Georgia, 31 U.S. 515 (1832)", "Indian Reorganization Act, 25 U.S.C. §461", "United States v Kagama, 118 U.S. 375 (1886)"],
        burden_holder="Tribe",
        adversary_position="Federal or state jurisdiction overrides tribal sovereignty.",
        counter_arguments=[
            "Treaty rights are enforceable.",
            "Jurisdiction is exclusive to tribe.",
            "Federal trust obligations are clear.",
            "Self-government is established.",
            "Remedies are warranted.",
            "Statutory standards support sovereignty."
        ],
        resolution_strategy="Apply treaty and statutory standards; review evidence; assess scope.",
        entity_scope="Tribes and governments",
        confidence=0.89,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Worcester v Georgia, 31 U.S. 515 (1832)"
    ),
    DoctrineBlock(
        topic="Water Rights",
        keywords=["riparian", "prior appropriation", "allocation", "beneficial use", "permit", "priority", "public trust"],
        conclusion_template="Identify water source and parties. Analyze riparian or prior appropriation rights. Assess allocation, beneficial use, and permit requirements. Conclude on priority and scope of water rights.",
        reasoning_framework="""1. Identify the water source and parties involved.
2. Analyze riparian or prior appropriation rights.
3. Assess allocation and beneficial use.
4. Evaluate permit requirements and priority.
5. Review relevant statutes and case law.
6. Consider public trust doctrine.
7. Examine impact on affected parties.
8. Analyze public policy implications.
9. Review scope of judicial review.
10. Assess exceptions or limitations.
11. Evaluate procedures for enforcement.
12. Analyze evidence of use and allocation.
13. Assess remedies for violation.
14. Examine defenses to liability.
15. Conclude on priority and scope.""",
        key_factors=["riparian", "prior appropriation", "allocation", "beneficial use", "priority"],
        primary_authority=["California Water Code §1200", "Colorado Doctrine", "Illinois Central Railroad v Illinois, 146 U.S. 387 (1892)"],
        burden_holder="Claimant",
        adversary_position="Other party has superior rights or use is not beneficial.",
        counter_arguments=[
            "Riparian rights are established.",
            "Prior appropriation favors claimant.",
            "Beneficial use is evidenced.",
            "Permit requirements are met.",
            "Priority is clear.",
            "Remedies are warranted."
        ],
        resolution_strategy="Apply riparian and appropriation standards; review evidence; assess priority.",
        entity_scope="Water users and government",
        confidence=0.90,
        confidence_zone="DEFENSIBLE",
        controlling_precedent="Illinois Central Railroad v Illinois, 146 U.S. 387 (1892)"
    )
]