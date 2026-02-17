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
        topic="Daubert Standard Federal Admissibility",
        keywords=["Daubert", "admissibility", "expert witness", "federal", "scientific evidence"],
        conclusion_template="The expert testimony is admissible under the Daubert standard if it is both relevant and reliable.",
        reasoning_framework="""The Daubert standard requires the trial judge to act as a gatekeeper, ensuring that scientific testimony or evidence is not only relevant but also reliable. The judge evaluates whether the methodology used by the expert is scientifically valid and applicable to the facts at issue. Factors considered include testability, peer review, error rates, standards, and general acceptance. The judge must weigh these factors and determine if the expert’s reasoning or methodology can be properly applied to the facts in question.""",
        key_factors=[
            "Testability of theory or technique",
            "Peer review and publication",
            "Known or potential error rate",
            "Existence and maintenance of standards",
            "General acceptance in scientific community"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc., 509 U.S. 579 (1993)", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue lack of reliability or relevance",
        counter_arguments=[
            "Methodology is not generally accepted",
            "High error rate",
            "Lack of peer review",
            "Not relevant to facts"
        ],
        resolution_strategy="Judicial gatekeeping through pretrial motions and hearings",
        entity_scope="Federal courts",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Frye General Acceptance Test",
        keywords=["Frye", "general acceptance", "expert witness", "scientific evidence", "state courts"],
        conclusion_template="The expert testimony is admissible if the methodology is generally accepted by the relevant scientific community.",
        reasoning_framework="""Under the Frye test, the admissibility of scientific evidence depends on whether the technique or principle is generally accepted by experts in the relevant field. The judge must determine if the scientific community recognizes the methodology as valid. This is often established through expert testimony, scientific literature, or consensus statements. The Frye test is less flexible than Daubert and does not consider other factors such as error rates or peer review.""",
        key_factors=[
            "Consensus in scientific community",
            "Recognition by professional organizations",
            "Supporting scientific literature"
        ],
        primary_authority=["Frye v. United States, 293 F. 1013 (D.C. Cir. 1923)"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue lack of general acceptance",
        counter_arguments=[
            "Technique is novel or controversial",
            "Lack of consensus",
            "Conflicting scientific literature"
        ],
        resolution_strategy="Judicial determination based on expert evidence",
        entity_scope="State courts applying Frye",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Frye v. United States"
    ),
    DoctrineBlock(
        topic="FRE 702 Expert Testimony Requirements",
        keywords=["FRE 702", "expert testimony", "qualification", "reliability", "relevance"],
        conclusion_template="Expert testimony is admissible if the expert is qualified, the testimony is based on sufficient facts or data, and the methodology is reliable and relevant.",
        reasoning_framework="""Federal Rule of Evidence 702 governs the admissibility of expert testimony. The rule requires that the expert be qualified by knowledge, skill, experience, training, or education. The testimony must be based on sufficient facts or data, use reliable principles and methods, and apply those methods reliably to the facts of the case. The judge must evaluate the expert's qualifications and the reliability of the methodology, often through pretrial hearings and motions.""",
        key_factors=[
            "Expert qualifications",
            "Sufficiency of facts or data",
            "Reliability of methodology",
            "Relevance to case"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue lack of qualification or unreliable methodology",
        counter_arguments=[
            "Expert lacks relevant experience",
            "Insufficient factual basis",
            "Methodology not reliable",
            "Testimony not relevant"
        ],
        resolution_strategy="Judicial evaluation and pretrial hearings",
        entity_scope="Federal courts",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Kumho Tire Extension to Technical Experts",
        keywords=["Kumho Tire", "technical expert", "Daubert", "reliability", "non-scientific"],
        conclusion_template="The Daubert standard applies to all expert testimony, including technical and specialized knowledge.",
        reasoning_framework="""The Supreme Court in Kumho Tire Co. v. Carmichael extended the Daubert standard to all types of expert testimony, not just scientific. The judge must ensure that technical or specialized knowledge is reliable and relevant. The same factors used in Daubert may be applied flexibly, depending on the nature of the expertise. The court evaluates the methodology, qualifications, and application to the facts, regardless of whether the testimony is scientific or technical.""",
        key_factors=[
            "Nature of expertise",
            "Reliability of methodology",
            "Relevance to case",
            "Expert qualifications"
        ],
        primary_authority=["Kumho Tire Co. v. Carmichael, 526 U.S. 137 (1999)", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue methodology is not reliable for technical experts",
        counter_arguments=[
            "Methodology not applicable to technical field",
            "Expert lacks technical qualifications",
            "Testimony not relevant"
        ],
        resolution_strategy="Judicial gatekeeping and flexible application of Daubert factors",
        entity_scope="Federal courts",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Kumho Tire Co. v. Carmichael"
    ),
    DoctrineBlock(
        topic="FRCP Rule 26(a)(2) Expert Disclosure",
        keywords=["FRCP 26(a)(2)", "expert disclosure", "report", "timing", "civil procedure"],
        conclusion_template="Expert disclosures must comply with FRCP 26(a)(2), including timely submission of written reports.",
        reasoning_framework="""Federal Rule of Civil Procedure 26(a)(2) requires parties to disclose the identity of expert witnesses and provide a written report prepared and signed by the expert. The report must contain a complete statement of all opinions, the basis and reasons for them, and supporting data. Disclosure deadlines are set by the court or by rule. Failure to comply may result in exclusion of testimony or other sanctions.""",
        key_factors=[
            "Timeliness of disclosure",
            "Completeness of report",
            "Compliance with court deadlines"
        ],
        primary_authority=["Federal Rules of Civil Procedure 26(a)(2)"],
        burden_holder="Party offering expert",
        adversary_position="Challenger may argue late or incomplete disclosure",
        counter_arguments=[
            "Report lacks required information",
            "Disclosure not timely",
            "Expert not properly identified"
        ],
        resolution_strategy="Judicial enforcement of disclosure requirements and sanctions",
        entity_scope="Federal civil litigation",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRCP 26(a)(2)"
    ),
    DoctrineBlock(
        topic="Expert Report Content Requirements",
        keywords=["expert report", "content", "FRCP 26", "opinions", "basis", "data"],
        conclusion_template="Expert reports must include all opinions, supporting data, and reasons, as required by FRCP 26(a)(2)(B).",
        reasoning_framework="""Expert reports must provide a complete statement of all opinions the expert will express, the basis and reasons for those opinions, and the data or information considered. The report must also include exhibits, qualifications, compensation, and prior testimony. The purpose is to ensure transparency and allow opposing parties to prepare for cross-examination and rebuttal. Failure to meet content requirements may result in exclusion or limitation of testimony.""",
        key_factors=[
            "Completeness of opinions",
            "Disclosure of supporting data",
            "Explanation of reasoning",
            "Inclusion of exhibits and qualifications"
        ],
        primary_authority=["FRCP 26(a)(2)(B)"],
        burden_holder="Party offering expert",
        adversary_position="Challenger may argue report is incomplete or insufficient",
        counter_arguments=[
            "Missing opinions",
            "Lack of supporting data",
            "Insufficient explanation"
        ],
        resolution_strategy="Judicial review and potential exclusion of testimony",
        entity_scope="Federal civil litigation",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FRCP 26(a)(2)(B)"
    ),
    DoctrineBlock(
        topic="FRE 703 Basis of Expert Opinion",
        keywords=["FRE 703", "basis", "expert opinion", "facts", "data"],
        conclusion_template="Expert opinions may be based on facts or data that are not admissible, if they are of a type reasonably relied upon by experts in the field.",
        reasoning_framework="""Federal Rule of Evidence 703 allows experts to base their opinions on facts or data that may be inadmissible, provided such information is reasonably relied upon by experts in the field. The court must determine whether the reliance is reasonable and whether the information is sufficiently trustworthy. The underlying facts or data may be disclosed to the jury if their probative value outweighs the risk of prejudice.""",
        key_factors=[
            "Reasonableness of reliance",
            "Trustworthiness of data",
            "Probative value vs. prejudice"
        ],
        primary_authority=["Federal Rules of Evidence 703"],
        burden_holder="Expert proponent",
        adversary_position="Challenger may argue reliance is unreasonable or data is unreliable",
        counter_arguments=[
            "Data not commonly relied upon",
            "Data is unreliable or prejudicial",
            "Opinion lacks factual basis"
        ],
        resolution_strategy="Judicial determination of reasonableness and disclosure",
        entity_scope="Federal courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRE 703"
    ),
    DoctrineBlock(
        topic="Daubert Motion Practice and Timing",
        keywords=["Daubert motion", "timing", "pretrial", "admissibility", "expert witness"],
        conclusion_template="Daubert motions must be filed in accordance with court deadlines to challenge expert admissibility.",
        reasoning_framework="""Daubert motions are used to challenge the admissibility of expert testimony under the Daubert standard. Courts typically set deadlines for filing such motions in pretrial orders. The motion must identify specific grounds for exclusion, such as unreliability or irrelevance. The court may hold hearings to evaluate the expert’s methodology and qualifications. Untimely motions may be denied or considered waived.""",
        key_factors=[
            "Compliance with court deadlines",
            "Specificity of grounds",
            "Opportunity for hearing"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Local court rules"],
        burden_holder="Challenger of expert testimony",
        adversary_position="Proponent may argue motion is untimely or lacks merit",
        counter_arguments=[
            "Motion filed after deadline",
            "Grounds are insufficient",
            "Expert testimony is reliable"
        ],
        resolution_strategy="Judicial enforcement of deadlines and pretrial hearings",
        entity_scope="Federal and state courts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Qualifications of Expert Witness",
        keywords=["expert witness", "qualification", "FRE 702", "experience", "education"],
        conclusion_template="An expert is qualified if they possess sufficient knowledge, skill, experience, training, or education relevant to the subject matter.",
        reasoning_framework="""Under FRE 702, the court must determine whether the expert is qualified to testify on the subject matter. Qualifications may include academic degrees, professional experience, specialized training, or demonstrated skill. The court evaluates the relevance and sufficiency of qualifications in relation to the issues in the case. Lack of qualification may result in exclusion of testimony or limitation of scope.""",
        key_factors=[
            "Relevant education",
            "Professional experience",
            "Specialized training",
            "Demonstrated skill"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue expert lacks relevant qualifications",
        counter_arguments=[
            "Insufficient experience",
            "Lack of relevant education",
            "No specialized training"
        ],
        resolution_strategy="Judicial evaluation and potential exclusion",
        entity_scope="Federal and state courts",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Hypothetical Questions to Experts",
        keywords=["hypothetical question", "expert witness", "testimony", "FRE 705"],
        conclusion_template="Experts may answer hypothetical questions if the facts assumed are supported by evidence.",
        reasoning_framework="""Hypothetical questions are used to elicit expert opinions based on assumed facts. The court must ensure that the facts assumed in the question are supported by evidence in the record. The expert’s answer is admissible if the hypothetical is reasonable and relevant. Opposing counsel may challenge the assumptions or pose alternative hypotheticals during cross-examination.""",
        key_factors=[
            "Support for assumed facts",
            "Reasonableness of hypothetical",
            "Relevance to case"
        ],
        primary_authority=["Federal Rules of Evidence 705"],
        burden_holder="Party posing hypothetical",
        adversary_position="Challenger may argue assumptions are unsupported",
        counter_arguments=[
            "Facts not in evidence",
            "Hypothetical is misleading",
            "Irrelevant assumptions"
        ],
        resolution_strategy="Judicial review and cross-examination",
        entity_scope="Federal and state courts",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="FRE 705"
    ),
    DoctrineBlock(
        topic="Cross-Examination of Expert Witnesses",
        keywords=["cross-examination", "expert witness", "credibility", "FRE 705", "impeachment"],
        conclusion_template="Expert witnesses may be cross-examined on qualifications, methodology, and basis of opinions.",
        reasoning_framework="""Cross-examination is a fundamental right in adversarial proceedings. Opposing counsel may challenge the expert’s qualifications, methodology, factual basis, and conclusions. The purpose is to test the reliability and credibility of the testimony. Impeachment may include exposing bias, errors, or inconsistencies. The court may limit cross-examination if it becomes repetitive or irrelevant.""",
        key_factors=[
            "Scope of testimony",
            "Expert qualifications",
            "Methodology and data",
            "Potential bias"
        ],
        primary_authority=["Federal Rules of Evidence 705", "Federal Rules of Evidence 611"],
        burden_holder="Opposing party",
        adversary_position="Expert may defend methodology and qualifications",
        counter_arguments=[
            "Methodology is sound",
            "Qualifications are sufficient",
            "Bias is minimal"
        ],
        resolution_strategy="Judicial oversight and limitation of scope",
        entity_scope="Federal and state courts",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRE 705"
    ),
    DoctrineBlock(
        topic="Rebuttal Expert Testimony",
        keywords=["rebuttal", "expert testimony", "FRCP 26", "timing", "scope"],
        conclusion_template="Rebuttal expert testimony is permitted to address issues raised by opposing experts, subject to disclosure requirements.",
        reasoning_framework="""Rebuttal experts may testify to counter opinions offered by opposing experts. The scope is limited to matters raised in the initial expert reports. Disclosure requirements under FRCP 26 apply, including timely submission of rebuttal reports. The court may exclude rebuttal testimony that exceeds the scope or is untimely disclosed.""",
        key_factors=[
            "Scope of rebuttal",
            "Timeliness of disclosure",
            "Compliance with FRCP 26"
        ],
        primary_authority=["FRCP 26(a)(2)(D)", "FRCP 26(a)(2)(B)"],
        burden_holder="Party offering rebuttal expert",
        adversary_position="Challenger may argue rebuttal is untimely or exceeds scope",
        counter_arguments=[
            "Rebuttal is within scope",
            "Disclosure is timely",
            "Testimony is relevant"
        ],
        resolution_strategy="Judicial review and enforcement of disclosure rules",
        entity_scope="Federal civil litigation",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="FRCP 26(a)(2)(D)"
    ),
    DoctrineBlock(
        topic="Expert Deposition Preparation",
        keywords=["expert deposition", "preparation", "FRCP 30", "disclosure", "strategy"],
        conclusion_template="Experts may prepare for depositions with counsel, but preparation materials may be subject to disclosure.",
        reasoning_framework="""Expert witnesses may meet with counsel to prepare for depositions. Preparation materials, such as drafts and notes, may be discoverable under FRCP 26(b)(4). Communications regarding facts, data, or assumptions considered by the expert are generally subject to disclosure, while attorney work product and legal theories may be protected. The court may resolve disputes over discoverability of preparation materials.""",
        key_factors=[
            "Nature of preparation materials",
            "Scope of discoverability",
            "Attorney work product protection"
        ],
        primary_authority=["FRCP 26(b)(4)", "FRCP 30"],
        burden_holder="Party seeking disclosure",
        adversary_position="Expert may assert privilege or protection",
        counter_arguments=[
            "Materials are protected work product",
            "Preparation is routine",
            "Disclosure is unnecessary"
        ],
        resolution_strategy="Judicial determination of discoverability and privilege",
        entity_scope="Federal civil litigation",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="FRCP 26(b)(4)"
    ),
    DoctrineBlock(
        topic="Opinion Scope and Ultimate Issue",
        keywords=["ultimate issue", "opinion scope", "FRE 704", "expert testimony"],
        conclusion_template="Experts may express opinions on ultimate issues, except as prohibited by law.",
        reasoning_framework="""Federal Rule of Evidence 704 allows experts to express opinions on ultimate issues in the case, except in criminal cases where opinions on mental state are prohibited. The court must ensure that the opinion does not usurp the role of the jury or violate statutory prohibitions. The expert’s opinion must be based on reliable methodology and relevant facts.""",
        key_factors=[
            "Relevance to ultimate issue",
            "Reliability of opinion",
            "Statutory prohibitions"
        ],
        primary_authority=["Federal Rules of Evidence 704"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue opinion invades jury function",
        counter_arguments=[
            "Opinion is within permissible scope",
            "Methodology is reliable",
            "No statutory prohibition"
        ],
        resolution_strategy="Judicial review and limitation of scope",
        entity_scope="Federal and state courts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRE 704"
    ),
    DoctrineBlock(
        topic="Expert Witness Immunity and Ethics",
        keywords=["expert witness", "immunity", "ethics", "malpractice", "testimony"],
        conclusion_template="Expert witnesses are generally immune from civil liability for testimony, but ethical obligations apply.",
        reasoning_framework="""Expert witnesses are afforded immunity from civil liability for statements made during testimony, to encourage candid participation in judicial proceedings. However, experts must adhere to ethical standards, including honesty, objectivity, and avoidance of conflicts of interest. Malpractice claims may arise from conduct outside testimony, such as negligent preparation or fraud. Courts may sanction unethical conduct or exclude testimony.""",
        key_factors=[
            "Scope of immunity",
            "Ethical obligations",
            "Conduct outside testimony"
        ],
        primary_authority=["Briscoe v. LaHue, 460 U.S. 325 (1983)", "State ethics rules"],
        burden_holder="Party alleging misconduct",
        adversary_position="Expert may assert immunity or compliance with ethics",
        counter_arguments=[
            "Testimony is protected",
            "Conduct was ethical",
            "No conflict of interest"
        ],
        resolution_strategy="Judicial determination and potential sanctions",
        entity_scope="Federal and state courts",
        confidence=0.87,
        confidence_zone="Moderate",
        controlling_precedent="Briscoe v. LaHue"
    ),
    DoctrineBlock(
        topic="Testability and Falsifiability Daubert Factor",
        keywords=["testability", "falsifiability", "Daubert", "scientific method", "reliability"],
        conclusion_template="The expert’s methodology is reliable if it can be tested and potentially falsified.",
        reasoning_framework="""Testability and falsifiability are core principles of scientific methodology. Under Daubert, the court evaluates whether the expert’s theory or technique can be empirically tested and subjected to falsification. The ability to test and refute the methodology increases its reliability and admissibility. Lack of testability may weigh against admissibility, especially in scientific cases.""",
        key_factors=[
            "Empirical testability",
            "Potential for falsification",
            "Scientific rigor"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue methodology is not testable",
        counter_arguments=[
            "Theory cannot be tested",
            "Method lacks scientific rigor",
            "No empirical validation"
        ],
        resolution_strategy="Judicial evaluation of methodology",
        entity_scope="Federal courts",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Peer Review and Publication Daubert Factor",
        keywords=["peer review", "publication", "Daubert", "scientific evidence", "reliability"],
        conclusion_template="Methodologies subjected to peer review and publication are more likely to be reliable under Daubert.",
        reasoning_framework="""Peer review and publication are indicators of scientific validity. The court considers whether the expert’s methodology has been published in reputable journals and subjected to scrutiny by other experts. Peer-reviewed methods are generally more reliable and accepted. Lack of peer review may weigh against admissibility, but is not dispositive. The court must balance this factor with others under Daubert.""",
        key_factors=[
            "Peer-reviewed publication",
            "Scientific scrutiny",
            "Acceptance by experts"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue methodology lacks peer review",
        counter_arguments=[
            "Method not published",
            "No peer review",
            "Lack of scientific scrutiny"
        ],
        resolution_strategy="Judicial evaluation and balancing of factors",
        entity_scope="Federal courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Known or Potential Error Rate Daubert Factor",
        keywords=["error rate", "Daubert", "scientific evidence", "reliability", "methodology"],
        conclusion_template="Methodologies with known or low error rates are more reliable under Daubert.",
        reasoning_framework="""The court evaluates whether the expert’s methodology has a known or potential error rate. Reliable scientific techniques should have quantifiable error rates, supported by empirical studies or validation. High or unknown error rates may undermine reliability and weigh against admissibility. The court must consider error rates in context and balance with other Daubert factors.""",
        key_factors=[
            "Empirical error rate",
            "Validation studies",
            "Impact on reliability"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue error rate is high or unknown",
        counter_arguments=[
            "Error rate is acceptable",
            "Method validated",
            "Error rate not relevant"
        ],
        resolution_strategy="Judicial evaluation and balancing of factors",
        entity_scope="Federal courts",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Standards and Controls Daubert Factor",
        keywords=["standards", "controls", "Daubert", "scientific evidence", "reliability"],
        conclusion_template="Methodologies with established standards and controls are more reliable under Daubert.",
        reasoning_framework="""The existence and maintenance of standards and controls is a key indicator of reliability. The court considers whether the expert’s methodology follows established protocols, guidelines, or industry standards. Proper controls reduce bias and error, increasing reliability. Lack of standards may weigh against admissibility, especially in scientific and technical cases.""",
        key_factors=[
            "Established standards",
            "Industry protocols",
            "Quality controls"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue lack of standards or controls",
        counter_arguments=[
            "Method follows standards",
            "Controls are adequate",
            "Industry protocols applied"
        ],
        resolution_strategy="Judicial evaluation and balancing of factors",
        entity_scope="Federal courts",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="General Acceptance in Scientific Community",
        keywords=["general acceptance", "scientific community", "Daubert", "Frye", "reliability"],
        conclusion_template="Methodologies generally accepted in the scientific community are more likely to be reliable and admissible.",
        reasoning_framework="""General acceptance is a factor under both Frye and Daubert. The court considers whether the expert’s methodology is recognized by the relevant scientific community, supported by consensus statements, professional organizations, and scientific literature. General acceptance increases reliability and admissibility, but lack of acceptance may weigh against it. The court must balance this factor with others under Daubert.""",
        key_factors=[
            "Consensus in scientific community",
            "Recognition by professional organizations",
            "Supporting literature"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Frye v. United States"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue methodology is not generally accepted",
        counter_arguments=[
            "Method is widely accepted",
            "Professional consensus",
            "Supporting literature"
        ],
        resolution_strategy="Judicial evaluation and balancing of factors",
        entity_scope="Federal and state courts",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Relevance and Fit Requirement",
        keywords=["relevance", "fit", "Daubert", "FRE 702", "expert testimony"],
        conclusion_template="Expert testimony must be relevant and fit the facts of the case to be admissible.",
        reasoning_framework="""The court must determine whether the expert testimony is relevant and fits the facts at issue. Relevance means the testimony will assist the trier of fact in understanding evidence or determining a fact in issue. Fit refers to the connection between the expert’s methodology and the facts of the case. Testimony that does not fit or is irrelevant may be excluded under Daubert and FRE 702.""",
        key_factors=[
            "Connection to facts",
            "Assistance to trier of fact",
            "Methodology relevance"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue testimony is irrelevant or does not fit",
        counter_arguments=[
            "Testimony assists jury",
            "Methodology is relevant",
            "Facts are connected"
        ],
        resolution_strategy="Judicial evaluation and exclusion of irrelevant testimony",
        entity_scope="Federal courts",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Supplementation of Expert Disclosures",
        keywords=["supplementation", "expert disclosure", "FRCP 26", "timing", "accuracy"],
        conclusion_template="Expert disclosures must be supplemented in a timely manner if new information arises.",
        reasoning_framework="""FRCP 26(e) requires parties to supplement expert disclosures if new information renders prior disclosures incomplete or inaccurate. Supplementation must occur in a timely manner, as ordered by the court or as soon as practicable. Failure to supplement may result in exclusion or sanctions. The court evaluates the necessity and timing of supplementation.""",
        key_factors=[
            "Timeliness of supplementation",
            "Materiality of new information",
            "Compliance with court orders"
        ],
        primary_authority=["FRCP 26(e)"],
        burden_holder="Party offering expert",
        adversary_position="Challenger may argue supplementation is untimely or unnecessary",
        counter_arguments=[
            "Supplementation is timely",
            "New information is material",
            "Disclosure is accurate"
        ],
        resolution_strategy="Judicial review and enforcement of supplementation",
        entity_scope="Federal civil litigation",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="FRCP 26(e)"
    ),
    DoctrineBlock(
        topic="Exclusion of Expert Testimony as Sanction",
        keywords=["exclusion", "sanction", "expert testimony", "FRCP 37", "disclosure"],
        conclusion_template="Expert testimony may be excluded as a sanction for failure to comply with disclosure requirements.",
        reasoning_framework="""FRCP 37(c)(1) authorizes exclusion of expert testimony as a sanction for failure to disclose information required by FRCP 26(a) or (e). The court may exclude testimony, impose monetary sanctions, or allow additional discovery. Exclusion is discretionary and depends on the prejudice to opposing parties, the reason for noncompliance, and the importance of the testimony.""",
        key_factors=[
            "Prejudice to opposing party",
            "Reason for noncompliance",
            "Importance of testimony"
        ],
        primary_authority=["FRCP 37(c)(1)", "FRCP 26(a)", "FRCP 26(e)"],
        burden_holder="Party seeking exclusion",
        adversary_position="Expert proponent may argue exclusion is unwarranted",
        counter_arguments=[
            "Noncompliance was inadvertent",
            "Testimony is critical",
            "Prejudice is minimal"
        ],
        resolution_strategy="Judicial discretion and balancing of factors",
        entity_scope="Federal civil litigation",
        confidence=0.89,
        confidence_zone="Moderate",
        controlling_precedent="FRCP 37(c)(1)"
    ),
    DoctrineBlock(
        topic="Court-Appointed Experts Under FRE 706",
        keywords=["court-appointed expert", "FRE 706", "neutral expert", "testimony"],
        conclusion_template="The court may appoint an expert under FRE 706 to provide neutral testimony.",
        reasoning_framework="""Federal Rule of Evidence 706 allows the court to appoint an expert to provide impartial testimony on technical or scientific issues. The appointed expert must disclose findings to all parties and may be subject to cross-examination. The court may allocate costs among parties. The purpose is to assist the court in complex cases and ensure objectivity.""",
        key_factors=[
            "Need for neutral expertise",
            "Complexity of issues",
            "Disclosure and cross-examination"
        ],
        primary_authority=["Federal Rules of Evidence 706"],
        burden_holder="Court",
        adversary_position="Parties may object to appointment or findings",
        counter_arguments=[
            "Expert is not impartial",
            "Findings are flawed",
            "Appointment is unnecessary"
        ],
        resolution_strategy="Judicial appointment and oversight",
        entity_scope="Federal and state courts",
        confidence=0.86,
        confidence_zone="Moderate",
        controlling_precedent="FRE 706"
    ),
    DoctrineBlock(
        topic="Treating Physician as Expert Witness",
        keywords=["treating physician", "expert witness", "FRE 702", "disclosure", "medical testimony"],
        conclusion_template="Treating physicians may testify as experts on diagnosis and treatment, subject to disclosure requirements.",
        reasoning_framework="""Treating physicians may offer expert testimony on diagnosis, treatment, and causation. They are not required to submit expert reports if testimony is limited to personal knowledge. If opinions extend beyond treatment, full disclosure and expert reports may be required under FRCP 26(a)(2). The court must determine the scope and admissibility of testimony based on qualifications and relevance.""",
        key_factors=[
            "Scope of testimony",
            "Personal knowledge",
            "Disclosure requirements"
        ],
        primary_authority=["FRCP 26(a)(2)", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of testimony",
        adversary_position="Challenger may argue testimony exceeds scope or lacks disclosure",
        counter_arguments=[
            "Testimony is within scope",
            "Disclosure is sufficient",
            "Physician is qualified"
        ],
        resolution_strategy="Judicial review and limitation of scope",
        entity_scope="Federal civil litigation",
        confidence=0.88,
        confidence_zone="Moderate",
        controlling_precedent="FRCP 26(a)(2)"
    ),
    DoctrineBlock(
        topic="Ipse Dixit Rejection and Explained Methodology",
        keywords=["ipse dixit", "explained methodology", "Daubert", "expert opinion", "reliability"],
        conclusion_template="Expert opinions based solely on ipse dixit are inadmissible; methodology must be explained and reliable.",
        reasoning_framework="""Courts reject expert opinions based on ipse dixit, meaning unsupported assertions by the expert. The expert must explain the methodology and reasoning underlying the opinion. The court evaluates whether the methodology is reliable, relevant, and sufficiently explained. Unsupported opinions are inadmissible under Daubert and FRE 702.""",
        key_factors=[
            "Explanation of methodology",
            "Reliability of reasoning",
            "Support for opinion"
        ],
        primary_authority=["General Electric Co. v. Joiner, 522 U.S. 136 (1997)", "Daubert v. Merrell Dow Pharmaceuticals, Inc."],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue opinion is unsupported",
        counter_arguments=[
            "Methodology is explained",
            "Opinion is supported",
            "Reasoning is reliable"
        ],
        resolution_strategy="Judicial evaluation and exclusion of unsupported opinions",
        entity_scope="Federal courts",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="General Electric Co. v. Joiner"
    ),
    DoctrineBlock(
        topic="Expert Testimony in Criminal Cases",
        keywords=["expert testimony", "criminal case", "FRE 702", "mental state", "ultimate issue"],
        conclusion_template="Expert testimony is admissible in criminal cases, except opinions on defendant’s mental state as ultimate issue.",
        reasoning_framework="""Federal Rule of Evidence 702 governs expert testimony in criminal cases. Experts may testify on scientific, technical, or specialized issues, but FRE 704(b) prohibits opinions on whether the defendant did or did not have a mental state constituting an element of the crime. The court must ensure reliability and relevance, and may limit scope as necessary.""",
        key_factors=[
            "Reliability of testimony",
            "Relevance to case",
            "Compliance with FRE 704(b)"
        ],
        primary_authority=["Federal Rules of Evidence 702", "Federal Rules of Evidence 704(b)"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue opinion invades ultimate issue",
        counter_arguments=[
            "Opinion is within permissible scope",
            "Testimony is reliable",
            "No violation of FRE 704(b)"
        ],
        resolution_strategy="Judicial review and limitation of scope",
        entity_scope="Federal criminal cases",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRE 704(b)"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Causation",
        keywords=["expert testimony", "causation", "Daubert", "FRE 702", "scientific evidence"],
        conclusion_template="Expert testimony on causation is admissible if methodology is reliable and fits the facts.",
        reasoning_framework="""Expert testimony on causation must be based on reliable scientific methodology and fit the facts of the case. The court evaluates whether the expert’s reasoning is sound, methodology is validated, and conclusions are supported by evidence. Unsupported or speculative causation opinions are inadmissible under Daubert and FRE 702.""",
        key_factors=[
            "Reliability of methodology",
            "Fit to facts",
            "Support for causation"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue causation opinion is speculative",
        counter_arguments=[
            "Methodology is validated",
            "Facts support causation",
            "Opinion is reliable"
        ],
        resolution_strategy="Judicial evaluation and exclusion of speculative opinions",
        entity_scope="Federal courts",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Expert Testimony on Damages",
        keywords=["expert testimony", "damages", "FRE 702", "economic expert", "quantification"],
        conclusion_template="Expert testimony on damages is admissible if based on reliable methodology and sufficient data.",
        reasoning_framework="""Experts may testify on damages, including economic loss, lost profits, and valuation. The court evaluates whether the methodology is reliable, data is sufficient, and conclusions are supported. Speculative or unsupported damages opinions may be excluded. The expert must explain the basis and reasoning for quantification.""",
        key_factors=[
            "Reliability of methodology",
            "Sufficiency of data",
            "Explanation of quantification"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue damages opinion is speculative",
        counter_arguments=[
            "Methodology is reliable",
            "Data is sufficient",
            "Opinion is explained"
        ],
        resolution_strategy="Judicial evaluation and exclusion of speculative opinions",
        entity_scope="Federal and state courts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Industry Standards",
        keywords=["expert testimony", "industry standards", "technical expert", "FRE 702"],
        conclusion_template="Expert testimony on industry standards is admissible if expert is qualified and methodology is reliable.",
        reasoning_framework="""Technical experts may testify on industry standards, practices, and protocols. The court evaluates qualifications, reliability of methodology, and relevance to the case. Testimony must assist the trier of fact and be based on recognized standards. Unsupported or irrelevant opinions may be excluded.""",
        key_factors=[
            "Expert qualifications",
            "Reliability of methodology",
            "Relevance to industry standards"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue expert lacks qualifications or opinion is irrelevant",
        counter_arguments=[
            "Expert is qualified",
            "Methodology is reliable",
            "Opinion is relevant"
        ],
        resolution_strategy="Judicial evaluation and exclusion of unsupported opinions",
        entity_scope="Federal and state courts",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Medical Causation",
        keywords=["expert testimony", "medical causation", "FRE 702", "Daubert", "medical expert"],
        conclusion_template="Medical causation testimony is admissible if methodology is reliable and fits the facts.",
        reasoning_framework="""Medical experts may testify on causation, diagnosis, and treatment. The court evaluates whether the methodology is reliable, validated, and fits the facts. Unsupported or speculative medical causation opinions are inadmissible under Daubert and FRE 702. The expert must explain the reasoning and support for conclusions.""",
        key_factors=[
            "Reliability of medical methodology",
            "Fit to medical facts",
            "Support for causation"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue medical causation opinion is speculative",
        counter_arguments=[
            "Methodology is validated",
            "Facts support causation",
            "Opinion is reliable"
        ],
        resolution_strategy="Judicial evaluation and exclusion of speculative opinions",
        entity_scope="Federal and state courts",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Expert Testimony on Technical Failures",
        keywords=["expert testimony", "technical failure", "engineering expert", "FRE 702"],
        conclusion_template="Technical failure testimony is admissible if expert is qualified and methodology is reliable.",
        reasoning_framework="""Engineering and technical experts may testify on failures, defects, and causation. The court evaluates qualifications, reliability of methodology, and relevance to the case. Testimony must assist the trier of fact and be based on recognized engineering principles. Unsupported or irrelevant opinions may be excluded.""",
        key_factors=[
            "Expert qualifications",
            "Reliability of methodology",
            "Relevance to technical failure"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue expert lacks qualifications or opinion is irrelevant",
        counter_arguments=[
            "Expert is qualified",
            "Methodology is reliable",
            "Opinion is relevant"
        ],
        resolution_strategy="Judicial evaluation and exclusion of unsupported opinions",
        entity_scope="Federal and state courts",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Statistical Analysis",
        keywords=["expert testimony", "statistical analysis", "FRE 702", "Daubert", "data"],
        conclusion_template="Statistical analysis testimony is admissible if methodology is reliable and data is sufficient.",
        reasoning_framework="""Experts may testify on statistical analysis, modeling, and interpretation of data. The court evaluates reliability of methodology, sufficiency of data, and relevance to the case. Unsupported or speculative statistical opinions may be excluded. The expert must explain the basis and reasoning for conclusions.""",
        key_factors=[
            "Reliability of statistical methodology",
            "Sufficiency of data",
            "Explanation of analysis"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue statistical opinion is speculative",
        counter_arguments=[
            "Methodology is validated",
            "Data is sufficient",
            "Opinion is reliable"
        ],
        resolution_strategy="Judicial evaluation and exclusion of speculative opinions",
        entity_scope="Federal and state courts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Expert Testimony on Product Defects",
        keywords=["expert testimony", "product defect", "FRE 702", "Daubert", "technical expert"],
        conclusion_template="Product defect testimony is admissible if expert is qualified and methodology is reliable.",
        reasoning_framework="""Technical experts may testify on product defects, design flaws, and causation. The court evaluates qualifications, reliability of methodology, and relevance to the case. Testimony must assist the trier of fact and be based on recognized principles. Unsupported or irrelevant opinions may be excluded.""",
        key_factors=[
            "Expert qualifications",
            "Reliability of methodology",
            "Relevance to product defect"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue expert lacks qualifications or opinion is irrelevant",
        counter_arguments=[
            "Expert is qualified",
            "Methodology is reliable",
            "Opinion is relevant"
        ],
        resolution_strategy="Judicial evaluation and exclusion of unsupported opinions",
        entity_scope="Federal and state courts",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Forensic Evidence",
        keywords=["expert testimony", "forensic evidence", "FRE 702", "Daubert", "scientific expert"],
        conclusion_template="Forensic evidence testimony is admissible if methodology is reliable and fits the facts.",
        reasoning_framework="""Forensic experts may testify on scientific evidence, including DNA, fingerprints, and ballistics. The court evaluates reliability of methodology, validation studies, and relevance to the case. Unsupported or speculative forensic opinions may be excluded. The expert must explain the reasoning and support for conclusions.""",
        key_factors=[
            "Reliability of forensic methodology",
            "Validation studies",
            "Fit to facts"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue forensic opinion is speculative",
        counter_arguments=[
            "Methodology is validated",
            "Facts support opinion",
            "Opinion is reliable"
        ],
        resolution_strategy="Judicial evaluation and exclusion of speculative opinions",
        entity_scope="Federal and state courts",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Expert Testimony on Intellectual Property Valuation",
        keywords=["expert testimony", "intellectual property", "valuation", "FRE 702", "economic expert"],
        conclusion_template="Intellectual property valuation testimony is admissible if methodology is reliable and data is sufficient.",
        reasoning_framework="""Experts may testify on valuation of patents, trademarks, and copyrights. The court evaluates reliability of methodology, sufficiency of data, and relevance to the case. Unsupported or speculative valuation opinions may be excluded. The expert must explain the basis and reasoning for conclusions.""",
        key_factors=[
            "Reliability of valuation methodology",
            "Sufficiency of data",
            "Explanation of valuation"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue valuation opinion is speculative",
        counter_arguments=[
            "Methodology is reliable",
            "Data is sufficient",
            "Opinion is explained"
        ],
        resolution_strategy="Judicial evaluation and exclusion of speculative opinions",
        entity_scope="Federal and state courts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Environmental Impact",
        keywords=["expert testimony", "environmental impact", "FRE 702", "Daubert", "scientific expert"],
        conclusion_template="Environmental impact testimony is admissible if methodology is reliable and fits the facts.",
        reasoning_framework="""Environmental experts may testify on impact assessments, pollution, and causation. The court evaluates reliability of methodology, validation studies, and relevance to the case. Unsupported or speculative environmental opinions may be excluded. The expert must explain the reasoning and support for conclusions.""",
        key_factors=[
            "Reliability of environmental methodology",
            "Validation studies",
            "Fit to facts"
        ],
        primary_authority=["Daubert v. Merrell Dow Pharmaceuticals, Inc.", "Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue environmental opinion is speculative",
        counter_arguments=[
            "Methodology is validated",
            "Facts support opinion",
            "Opinion is reliable"
        ],
        resolution_strategy="Judicial evaluation and exclusion of speculative opinions",
        entity_scope="Federal and state courts",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Daubert v. Merrell Dow Pharmaceuticals, Inc."
    ),
    DoctrineBlock(
        topic="Expert Testimony on Financial Fraud",
        keywords=["expert testimony", "financial fraud", "FRE 702", "economic expert", "methodology"],
        conclusion_template="Financial fraud testimony is admissible if methodology is reliable and data is sufficient.",
        reasoning_framework="""Experts may testify on financial fraud, accounting irregularities, and economic loss. The court evaluates reliability of methodology, sufficiency of data, and relevance to the case. Unsupported or speculative fraud opinions may be excluded. The expert must explain the basis and reasoning for conclusions.""",
        key_factors=[
            "Reliability of fraud detection methodology",
            "Sufficiency of data",
            "Explanation of analysis"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue fraud opinion is speculative",
        counter_arguments=[
            "Methodology is reliable",
            "Data is sufficient",
            "Opinion is explained"
        ],
        resolution_strategy="Judicial evaluation and exclusion of speculative opinions",
        entity_scope="Federal and state courts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Construction Defects",
        keywords=["expert testimony", "construction defect", "FRE 702", "technical expert", "methodology"],
        conclusion_template="Construction defect testimony is admissible if expert is qualified and methodology is reliable.",
        reasoning_framework="""Technical experts may testify on construction defects, design flaws, and causation. The court evaluates qualifications, reliability of methodology, and relevance to the case. Testimony must assist the trier of fact and be based on recognized principles. Unsupported or irrelevant opinions may be excluded.""",
        key_factors=[
            "Expert qualifications",
            "Reliability of methodology",
            "Relevance to construction defect"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue expert lacks qualifications or opinion is irrelevant",
        counter_arguments=[
            "Expert is qualified",
            "Methodology is reliable",
            "Opinion is relevant"
        ],
        resolution_strategy="Judicial evaluation and exclusion of unsupported opinions",
        entity_scope="Federal and state courts",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Insurance Coverage",
        keywords=["expert testimony", "insurance coverage", "FRE 702", "industry expert", "methodology"],
        conclusion_template="Insurance coverage testimony is admissible if expert is qualified and methodology is reliable.",
        reasoning_framework="""Industry experts may testify on insurance coverage, policy interpretation, and claims handling. The court evaluates qualifications, reliability of methodology, and relevance to the case. Testimony must assist the trier of fact and be based on recognized industry practices. Unsupported or irrelevant opinions may be excluded.""",
        key_factors=[
            "Expert qualifications",
            "Reliability of methodology",
            "Relevance to insurance coverage"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue expert lacks qualifications or opinion is irrelevant",
        counter_arguments=[
            "Expert is qualified",
            "Methodology is reliable",
            "Opinion is relevant"
        ],
        resolution_strategy="Judicial evaluation and exclusion of unsupported opinions",
        entity_scope="Federal and state courts",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Patent Infringement",
        keywords=["expert testimony", "patent infringement", "FRE 702", "technical expert", "methodology"],
        conclusion_template="Patent infringement testimony is admissible if expert is qualified and methodology is reliable.",
        reasoning_framework="""Technical experts may testify on patent infringement, claim interpretation, and technical comparisons. The court evaluates qualifications, reliability of methodology, and relevance to the case. Testimony must assist the trier of fact and be based on recognized principles. Unsupported or irrelevant opinions may be excluded.""",
        key_factors=[
            "Expert qualifications",
            "Reliability of methodology",
            "Relevance to patent infringement"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue expert lacks qualifications or opinion is irrelevant",
        counter_arguments=[
            "Expert is qualified",
            "Methodology is reliable",
            "Opinion is relevant"
        ],
        resolution_strategy="Judicial evaluation and exclusion of unsupported opinions",
        entity_scope="Federal and state courts",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Trade Secrets",
        keywords=["expert testimony", "trade secrets", "FRE 702", "industry expert", "methodology"],
        conclusion_template="Trade secrets testimony is admissible if expert is qualified and methodology is reliable.",
        reasoning_framework="""Industry experts may testify on trade secrets, misappropriation, and valuation. The court evaluates qualifications, reliability of methodology, and relevance to the case. Testimony must assist the trier of fact and be based on recognized industry practices. Unsupported or irrelevant opinions may be excluded.""",
        key_factors=[
            "Expert qualifications",
            "Reliability of methodology",
            "Relevance to trade secrets"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue expert lacks qualifications or opinion is irrelevant",
        counter_arguments=[
            "Expert is qualified",
            "Methodology is reliable",
            "Opinion is relevant"
        ],
        resolution_strategy="Judicial evaluation and exclusion of unsupported opinions",
        entity_scope="Federal and state courts",
        confidence=0.90,
        confidence_zone="Moderate",
        controlling_precedent="FRE 702"
    ),
    DoctrineBlock(
        topic="Expert Testimony on Antitrust Damages",
        keywords=["expert testimony", "antitrust damages", "FRE 702", "economic expert", "methodology"],
        conclusion_template="Antitrust damages testimony is admissible if methodology is reliable and data is sufficient.",
        reasoning_framework="""Economic experts may testify on antitrust damages, market analysis, and quantification. The court evaluates reliability of methodology, sufficiency of data, and relevance to the case. Unsupported or speculative damages opinions may be excluded. The expert must explain the basis and reasoning for conclusions.""",
        key_factors=[
            "Reliability of economic methodology",
            "Sufficiency of data",
            "Explanation of damages"
        ],
        primary_authority=["Federal Rules of Evidence 702"],
        burden_holder="Proponent of expert testimony",
        adversary_position="Challenger may argue damages opinion is speculative",
        counter_arguments=[
            "Methodology is reliable",
            "Data is sufficient",
            "Opinion is explained"
        ],
        resolution_strategy="Judicial evaluation and exclusion of speculative opinions",
        entity_scope="Federal and state courts",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FRE 702"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    results = []
    query_lower = query.lower()
    for doctrine in DOCTRINE_CACHE:
        if query_lower in doctrine.topic.lower() or any(query_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]