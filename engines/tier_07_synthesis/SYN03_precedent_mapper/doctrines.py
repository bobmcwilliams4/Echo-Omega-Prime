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
        topic="Stare Decisis Principles",
        keywords=["precedent", "stare decisis", "binding", "judicial consistency", "legal stability"],
        conclusion_template="The court is bound by prior decisions unless compelling justification exists for departure.",
        reasoning_framework=(
            "Stare decisis mandates adherence to previously decided cases to promote legal stability and predictability. "
            "The doctrine is rooted in the principle that like cases should be decided alike, fostering reliance interests and judicial economy. "
            "Departure from precedent is justified only when the prior decision is manifestly erroneous, unworkable, or inconsistent with subsequent legal developments. "
            "The court evaluates the strength of reliance interests, the clarity of the precedent, and the evolution of statutory or constitutional law. "
            "Where precedent is clear and controlling, the court must follow unless there is a compelling reason to overrule. "
            "Factors such as societal change, statutory amendments, or constitutional reinterpretation may warrant reconsideration. "
            "The court weighs the potential disruption to settled expectations against the need for doctrinal correction. "
            "Stare decisis is strongest in cases involving statutory interpretation and weakest in constitutional cases, where the court is the ultimate interpreter. "
            "The doctrine does not preclude the court from distinguishing prior cases based on factual or legal differences. "
            "Judges must articulate the rationale for departing from precedent to ensure transparency and accountability."
        ),
        key_factors=[
            "Reliance interests",
            "Clarity of precedent",
            "Legal evolution",
            "Manifest error",
            "Workability"
        ],
        primary_authority=[
            "Payne v. Tennessee, 501 U.S. 808 (1991)",
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)",
            "State v. McKinney, 245 P.3d 1172 (Ariz. 2011)"
        ],
        burden_holder="Party seeking departure from precedent",
        adversary_position="Advocates for adherence to prior decisions",
        counter_arguments=[
            "Prior decision is outdated",
            "Precedent is unworkable",
            "Societal changes justify reconsideration"
        ],
        resolution_strategy="Apply stare decisis unless compelling justification for departure is established",
        entity_scope="All courts within jurisdiction",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Payne v. Tennessee, 501 U.S. 808 (1991)"
    ),
    DoctrineBlock(
        topic="Binding vs Persuasive Authority",
        keywords=["binding", "persuasive", "authority", "precedent", "jurisdiction"],
        conclusion_template="The court must follow binding authority and may consider persuasive authority as guidance.",
        reasoning_framework=(
            "Binding authority consists of decisions from higher courts within the same jurisdiction, statutes, and constitutional provisions. "
            "Persuasive authority includes decisions from other jurisdictions, lower courts, academic commentary, and dicta. "
            "The court first identifies whether the precedent is binding based on jurisdictional hierarchy. "
            "If no binding authority exists, the court evaluates persuasive sources for their reasoning, factual similarity, and doctrinal coherence. "
            "Persuasive authority is most influential when the reasoning is robust and the factual context aligns closely with the present case. "
            "The court may adopt persuasive authority if it fills gaps in the law or provides clarity where binding precedent is absent. "
            "Binding authority must be followed unless overruled or distinguished. "
            "Persuasive authority cannot override binding precedent but may inform interpretation and application."
        ),
        key_factors=[
            "Jurisdictional hierarchy",
            "Factual similarity",
            "Reasoning strength",
            "Doctrinal coherence"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "People v. Williams, 22 Cal. 4th 1209 (2000)"
        ],
        burden_holder="Party relying on authority",
        adversary_position="Challenges applicability or weight of authority",
        counter_arguments=[
            "Authority is not binding",
            "Persuasive authority is factually distinguishable",
            "Reasoning is outdated"
        ],
        resolution_strategy="Apply binding authority; consider persuasive authority as guidance",
        entity_scope="Court within jurisdiction",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Circuit Split Identification",
        keywords=["circuit split", "conflict", "precedent", "jurisdiction", "federal courts"],
        conclusion_template="A circuit split exists when two or more federal appellate courts reach divergent conclusions on the same legal issue.",
        reasoning_framework=(
            "Circuit splits arise when federal appellate courts interpret statutes, constitutional provisions, or common law differently. "
            "Identification requires comparison of relevant decisions across circuits, focusing on the legal issue and outcome. "
            "The court analyzes whether the split is genuine, considering factual distinctions and the scope of the rulings. "
            "Circuit splits often prompt Supreme Court review to resolve inconsistencies and establish uniformity. "
            "The court may consider the reasoning of each circuit, the impact of the split on litigants, and the likelihood of Supreme Court intervention. "
            "Circuit splits can influence persuasive authority and may affect forum selection and litigation strategy."
        ),
        key_factors=[
            "Divergent legal interpretations",
            "Jurisdictional scope",
            "Factual distinctions",
            "Impact on litigants"
        ],
        primary_authority=[
            "Supreme Court Rule 10",
            "Smith v. United States, 508 U.S. 223 (1993)"
        ],
        burden_holder="Party asserting existence of split",
        adversary_position="Denies existence or relevance of split",
        counter_arguments=[
            "Split is not genuine",
            "Factual distinctions explain divergence",
            "Split is limited in scope"
        ],
        resolution_strategy="Identify and document circuit split; consider implications for litigation and Supreme Court review",
        entity_scope="Federal appellate courts",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Supreme Court Rule 10"
    ),
    DoctrineBlock(
        topic="En Banc Reconsideration",
        keywords=["en banc", "reconsideration", "panel", "precedent", "appellate"],
        conclusion_template="En banc reconsideration is appropriate when panel decisions conflict or present issues of exceptional importance.",
        reasoning_framework=(
            "En banc review allows the full appellate court to reconsider panel decisions. "
            "It is typically granted when there is a conflict among panel decisions, issues of exceptional importance, or to maintain uniformity in the court's jurisprudence. "
            "The court evaluates whether the panel decision is inconsistent with prior precedent or presents a question of broad significance. "
            "Petitions for en banc review must articulate the conflict or importance clearly. "
            "The court weighs the need for doctrinal consistency against judicial economy and resources. "
            "En banc review is rare and reserved for cases with significant impact or legal confusion."
        ),
        key_factors=[
            "Panel conflict",
            "Exceptional importance",
            "Doctrinal consistency",
            "Judicial economy"
        ],
        primary_authority=[
            "Fed. R. App. P. 35",
            "United States v. American-Foreign S.S. Corp., 363 U.S. 685 (1960)"
        ],
        burden_holder="Party seeking en banc review",
        adversary_position="Opposes en banc reconsideration",
        counter_arguments=[
            "No conflict exists",
            "Issue lacks exceptional importance",
            "Panel decision is consistent"
        ],
        resolution_strategy="Grant en banc review if conflict or importance is established",
        entity_scope="Federal appellate courts",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fed. R. App. P. 35"
    ),
    DoctrineBlock(
        topic="Supreme Court Certiorari Factors",
        keywords=["certiorari", "Supreme Court", "review", "factors", "precedent"],
        conclusion_template="The Supreme Court grants certiorari based on factors such as circuit splits, national importance, and legal confusion.",
        reasoning_framework=(
            "The Supreme Court exercises discretionary review through certiorari. "
            "Key factors include the existence of circuit splits, questions of national importance, conflicts with Supreme Court precedent, and issues affecting federal law uniformity. "
            "The Court also considers whether the case presents a novel legal question or addresses recurring issues. "
            "Certiorari is rarely granted solely to correct errors; the Court prioritizes cases with broad legal significance. "
            "Petitioners must frame the question presented to highlight its importance and the need for resolution."
        ),
        key_factors=[
            "Circuit split",
            "National importance",
            "Legal confusion",
            "Conflict with precedent"
        ],
        primary_authority=[
            "Supreme Court Rule 10",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Petitioner seeking certiorari",
        adversary_position="Respondent opposing certiorari",
        counter_arguments=[
            "No circuit split",
            "Issue lacks national importance",
            "No conflict with precedent"
        ],
        resolution_strategy="Grant certiorari if factors are met",
        entity_scope="Supreme Court",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Supreme Court Rule 10"
    ),
    DoctrineBlock(
        topic="Overruling Signals",
        keywords=["overruling", "signals", "precedent", "judicial intent", "doctrinal change"],
        conclusion_template="Judicial opinions may contain signals indicating intent to overrule prior precedent.",
        reasoning_framework=(
            "Overruling signals are explicit or implicit indications in judicial opinions that the court is reconsidering prior precedent. "
            "Signals include criticism of prior decisions, suggestions that precedent is outdated, or statements questioning the continued validity of the law. "
            "The court analyzes the language used, the context of the opinion, and subsequent citations. "
            "Strong signals may prompt parties to challenge precedent or anticipate doctrinal shifts. "
            "The court distinguishes between dicta and holdings when evaluating overruling signals. "
            "Overruling is formalized only through explicit decisions; signals alone do not change the law."
        ),
        key_factors=[
            "Explicit criticism",
            "Questioning validity",
            "Context of opinion",
            "Subsequent citations"
        ],
        primary_authority=[
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)",
            "State v. McKinney, 245 P.3d 1172 (Ariz. 2011)"
        ],
        burden_holder="Party relying on overruling signals",
        adversary_position="Asserts precedent remains controlling",
        counter_arguments=[
            "Signal is dicta",
            "No formal overruling",
            "Precedent remains valid"
        ],
        resolution_strategy="Identify and interpret overruling signals; await formal overruling",
        entity_scope="All courts",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Planned Parenthood v. Casey, 505 U.S. 833 (1992)"
    ),
    DoctrineBlock(
        topic="Distinguishing Methodology",
        keywords=["distinguishing", "methodology", "precedent", "factual differences", "legal differences"],
        conclusion_template="A court may distinguish prior precedent based on material factual or legal differences.",
        reasoning_framework=(
            "Distinguishing involves identifying material differences between the present case and prior precedent. "
            "The court analyzes the facts, legal issues, and procedural posture to determine whether the precedent applies. "
            "Material differences may render precedent inapplicable or limit its scope. "
            "The court articulates the distinguishing factors to justify departure from precedent. "
            "Distinguishing is not overruling; it preserves the integrity of precedent while adapting to new circumstances."
        ),
        key_factors=[
            "Material factual differences",
            "Legal distinctions",
            "Procedural posture",
            "Scope of precedent"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "People v. Williams, 22 Cal. 4th 1209 (2000)"
        ],
        burden_holder="Party seeking to distinguish precedent",
        adversary_position="Asserts precedent is controlling",
        counter_arguments=[
            "Differences are immaterial",
            "Precedent applies",
            "No legal distinction"
        ],
        resolution_strategy="Articulate distinguishing factors; limit application of precedent",
        entity_scope="All courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Case Treatment Taxonomy",
        keywords=["case treatment", "taxonomy", "precedent", "citator", "Shepardizing"],
        conclusion_template="Cases are categorized by treatment: followed, distinguished, overruled, criticized, or cited.",
        reasoning_framework=(
            "Case treatment taxonomy classifies judicial decisions based on how subsequent cases address them. "
            "Categories include followed, distinguished, overruled, criticized, and cited. "
            "Citator services such as Shepard's and KeyCite track case treatment to inform legal research and precedent analysis. "
            "The court considers the treatment history to assess the authority and reliability of precedent. "
            "Negative treatment may diminish the weight of precedent, while positive treatment reinforces its controlling status."
        ),
        key_factors=[
            "Treatment category",
            "Citator history",
            "Subsequent case analysis",
            "Authority reliability"
        ],
        primary_authority=[
            "Shepard's Citations",
            "KeyCite",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on case treatment",
        adversary_position="Challenges reliability or weight",
        counter_arguments=[
            "Negative treatment",
            "Overruled precedent",
            "Distinguished facts"
        ],
        resolution_strategy="Analyze case treatment taxonomy; adjust weight of precedent accordingly",
        entity_scope="All courts",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Shepard's Citations"
    ),
    DoctrineBlock(
        topic="Authority Weight Scoring",
        keywords=["authority", "weight", "scoring", "precedent", "citator"],
        conclusion_template="Precedent is scored based on its authority, treatment, and jurisdictional relevance.",
        reasoning_framework=(
            "Authority weight scoring evaluates the strength of precedent based on jurisdictional hierarchy, treatment history, and factual relevance. "
            "Binding precedent receives the highest score, followed by persuasive authority with robust reasoning. "
            "Negative treatment, such as criticism or overruling, reduces the score. "
            "Citator services provide scoring metrics to guide legal research. "
            "The court considers the score when selecting precedent for application or citation."
        ),
        key_factors=[
            "Jurisdictional hierarchy",
            "Treatment history",
            "Factual relevance",
            "Citator scoring"
        ],
        primary_authority=[
            "Shepard's Citations",
            "KeyCite",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on authority score",
        adversary_position="Challenges scoring methodology",
        counter_arguments=[
            "Score is inflated",
            "Negative treatment not accounted",
            "Jurisdictional mismatch"
        ],
        resolution_strategy="Apply authority weight scoring; adjust reliance based on score",
        entity_scope="All courts",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Shepard's Citations"
    ),
    DoctrineBlock(
        topic="Recency vs Landmark Weight",
        keywords=["recency", "landmark", "weight", "precedent", "authority"],
        conclusion_template="Landmark cases may outweigh recent decisions if their doctrinal impact is greater.",
        reasoning_framework=(
            "The court balances the recency of precedent against the doctrinal significance of landmark cases. "
            "Recent decisions may reflect current legal standards, but landmark cases often establish foundational principles. "
            "The court evaluates the impact, clarity, and acceptance of landmark cases. "
            "Recency is relevant when legal standards evolve, but landmark cases retain authority unless overruled. "
            "The court considers whether the recent decision is consistent with landmark precedent or represents a departure."
        ),
        key_factors=[
            "Doctrinal significance",
            "Recency",
            "Consistency",
            "Impact"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)"
        ],
        burden_holder="Party relying on landmark or recent precedent",
        adversary_position="Challenges weight or relevance",
        counter_arguments=[
            "Landmark case is outdated",
            "Recent decision reflects current law",
            "Doctrinal shift"
        ],
        resolution_strategy="Weigh recency against landmark impact; prioritize doctrinal significance",
        entity_scope="All courts",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Vertical Stare Decisis Absolute",
        keywords=["vertical", "stare decisis", "absolute", "binding", "hierarchy"],
        conclusion_template="Lower courts must follow decisions of higher courts within the same jurisdiction.",
        reasoning_framework=(
            "Vertical stare decisis requires lower courts to adhere absolutely to the decisions of higher courts in the same jurisdiction. "
            "The doctrine ensures uniformity and predictability in the application of law. "
            "Lower courts may not disregard or reinterpret controlling precedent. "
            "Exceptions exist only when the higher court has overruled or modified its prior decisions. "
            "The court identifies the controlling precedent and applies it unless distinguishing factors are present."
        ),
        key_factors=[
            "Jurisdictional hierarchy",
            "Controlling precedent",
            "Distinguishing factors",
            "Uniformity"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "State v. McKinney, 245 P.3d 1172 (Ariz. 2011)"
        ],
        burden_holder="Lower court",
        adversary_position="Challenges application of controlling precedent",
        counter_arguments=[
            "Precedent is distinguishable",
            "Higher court has modified decision",
            "Jurisdictional mismatch"
        ],
        resolution_strategy="Apply vertical stare decisis; follow higher court decisions",
        entity_scope="Lower courts",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Horizontal Stare Decisis Flexibility",
        keywords=["horizontal", "stare decisis", "flexibility", "same court", "precedent"],
        conclusion_template="Courts may depart from their own prior decisions if justified by compelling reasons.",
        reasoning_framework=(
            "Horizontal stare decisis applies to decisions within the same court. "
            "Courts may depart from their own prior decisions if compelling reasons exist, such as manifest error, legal evolution, or unworkability. "
            "The court evaluates reliance interests, doctrinal consistency, and the impact of departure. "
            "Departure must be justified and articulated to maintain transparency. "
            "Horizontal stare decisis is less absolute than vertical, allowing for doctrinal development."
        ),
        key_factors=[
            "Manifest error",
            "Legal evolution",
            "Reliance interests",
            "Doctrinal consistency"
        ],
        primary_authority=[
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)",
            "State v. McKinney, 245 P.3d 1172 (Ariz. 2011)"
        ],
        burden_holder="Court departing from prior decision",
        adversary_position="Advocates for adherence to prior decisions",
        counter_arguments=[
            "Departure undermines consistency",
            "Reliance interests are strong",
            "No compelling reason"
        ],
        resolution_strategy="Depart from prior decisions only if compelling reasons are established",
        entity_scope="Same court",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Planned Parenthood v. Casey, 505 U.S. 833 (1992)"
    ),
    DoctrineBlock(
        topic="Persuasive Authority Weight Factors",
        keywords=["persuasive", "authority", "weight", "factors", "precedent"],
        conclusion_template="Persuasive authority is weighed based on reasoning strength, factual similarity, and doctrinal coherence.",
        reasoning_framework=(
            "Persuasive authority is evaluated for its reasoning strength, factual similarity to the present case, and doctrinal coherence. "
            "The court considers whether the authority fills gaps in binding law or provides clarity. "
            "Persuasive authority is most influential when it is widely cited and accepted. "
            "The court may adopt persuasive authority if it aligns with the jurisdiction's legal principles."
        ),
        key_factors=[
            "Reasoning strength",
            "Factual similarity",
            "Doctrinal coherence",
            "Acceptance"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "People v. Williams, 22 Cal. 4th 1209 (2000)"
        ],
        burden_holder="Party relying on persuasive authority",
        adversary_position="Challenges weight or applicability",
        counter_arguments=[
            "Authority is not widely accepted",
            "Reasoning is weak",
            "Factual differences"
        ],
        resolution_strategy="Weigh persuasive authority; adopt if factors are met",
        entity_scope="All courts",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Shepardizing and Citator Services",
        keywords=["Shepardizing", "citator", "services", "case treatment", "precedent"],
        conclusion_template="Shepardizing and citator services track case treatment and inform precedent reliability.",
        reasoning_framework=(
            "Shepardizing and citator services such as KeyCite provide comprehensive tracking of case treatment. "
            "They identify whether cases are followed, distinguished, overruled, or criticized. "
            "Citator results inform the reliability and weight of precedent. "
            "The court uses citator data to assess whether precedent remains controlling or has been negatively treated. "
            "Legal researchers rely on citators to avoid reliance on overruled or criticized cases."
        ),
        key_factors=[
            "Case treatment",
            "Citator results",
            "Reliability",
            "Negative treatment"
        ],
        primary_authority=[
            "Shepard's Citations",
            "KeyCite"
        ],
        burden_holder="Party relying on citator data",
        adversary_position="Challenges reliability or accuracy",
        counter_arguments=[
            "Citator data is outdated",
            "Negative treatment not reflected",
            "Case is overruled"
        ],
        resolution_strategy="Use citator services to verify precedent reliability",
        entity_scope="All courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Shepard's Citations"
    ),
    DoctrineBlock(
        topic="Analogical Reasoning Framework",
        keywords=["analogical reasoning", "framework", "precedent", "comparison", "legal analysis"],
        conclusion_template="The court applies analogical reasoning by comparing facts and legal principles to prior cases.",
        reasoning_framework=(
            "Analogical reasoning involves comparing the facts and legal principles of the present case to prior decisions. "
            "The court identifies similarities and differences, evaluates the relevance of precedent, and applies legal principles accordingly. "
            "Analogical reasoning is used when direct precedent is absent or ambiguous. "
            "The court articulates the analogy to justify its decision and ensure consistency with prior jurisprudence."
        ),
        key_factors=[
            "Factual similarity",
            "Legal principle alignment",
            "Relevance",
            "Consistency"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "People v. Williams, 22 Cal. 4th 1209 (2000)"
        ],
        burden_holder="Party relying on analogical reasoning",
        adversary_position="Challenges analogy or relevance",
        counter_arguments=[
            "Facts are not analogous",
            "Legal principles differ",
            "Precedent is distinguishable"
        ],
        resolution_strategy="Apply analogical reasoning; justify analogy",
        entity_scope="All courts",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Plurality Opinion Precedential Effect",
        keywords=["plurality opinion", "precedential effect", "precedent", "Supreme Court", "fragmented decision"],
        conclusion_template="Plurality opinions have limited precedential effect; the narrowest grounds may control.",
        reasoning_framework=(
            "Plurality opinions occur when no single rationale garners majority support. "
            "The court applies the Marks rule, which holds that the narrowest grounds supporting the judgment control. "
            "The court analyzes the opinions to identify common reasoning and determine the controlling rationale. "
            "Plurality opinions are less authoritative and may be limited in scope. "
            "Subsequent courts may interpret plurality opinions differently, leading to doctrinal ambiguity."
        ),
        key_factors=[
            "Narrowest grounds",
            "Common reasoning",
            "Majority support",
            "Doctrinal ambiguity"
        ],
        primary_authority=[
            "Marks v. United States, 430 U.S. 188 (1977)",
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)"
        ],
        burden_holder="Party relying on plurality opinion",
        adversary_position="Challenges precedential effect",
        counter_arguments=[
            "No common rationale",
            "Opinion is ambiguous",
            "Limited scope"
        ],
        resolution_strategy="Apply Marks rule; identify narrowest grounds",
        entity_scope="All courts",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Marks v. United States, 430 U.S. 188 (1977)"
    ),
    DoctrineBlock(
        topic="Concurring and Dissenting Opinion Value",
        keywords=["concurring", "dissenting", "opinion", "value", "precedent"],
        conclusion_template="Concurring and dissenting opinions are not binding but may influence doctrinal development.",
        reasoning_framework=(
            "Concurring and dissenting opinions express alternative reasoning or disagreement with the majority. "
            "They are not binding precedent but may influence future decisions and doctrinal development. "
            "The court considers the reasoning, clarity, and acceptance of concurring and dissenting opinions. "
            "Such opinions may be cited as persuasive authority or to highlight doctrinal debates."
        ),
        key_factors=[
            "Reasoning clarity",
            "Doctrinal influence",
            "Acceptance",
            "Persuasive value"
        ],
        primary_authority=[
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party citing concurring/dissenting opinion",
        adversary_position="Challenges persuasive value",
        counter_arguments=[
            "Opinion is not binding",
            "Reasoning lacks clarity",
            "Limited influence"
        ],
        resolution_strategy="Consider concurring/dissenting opinions as persuasive authority",
        entity_scope="All courts",
        confidence=0.80,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Planned Parenthood v. Casey, 505 U.S. 833 (1992)"
    ),
    DoctrineBlock(
        topic="Per Curiam Opinion Precedential Weight",
        keywords=["per curiam", "opinion", "precedential weight", "precedent", "Supreme Court"],
        conclusion_template="Per curiam opinions may be binding if issued by the Supreme Court or appellate courts.",
        reasoning_framework=(
            "Per curiam opinions are issued collectively by the court without individual authorship. "
            "They may be binding precedent if issued by the Supreme Court or appellate courts. "
            "The court evaluates the scope, clarity, and reasoning of per curiam opinions. "
            "Per curiam opinions are often brief and may lack detailed reasoning, limiting their precedential weight. "
            "The court distinguishes between summary dispositions and substantive per curiam opinions."
        ),
        key_factors=[
            "Court issuing opinion",
            "Scope",
            "Reasoning clarity",
            "Summary disposition"
        ],
        primary_authority=[
            "Bush v. Gore, 531 U.S. 98 (2000)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on per curiam opinion",
        adversary_position="Challenges precedential weight",
        counter_arguments=[
            "Opinion lacks reasoning",
            "Summary disposition",
            "Limited scope"
        ],
        resolution_strategy="Evaluate per curiam opinion for binding effect",
        entity_scope="Supreme Court and appellate courts",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Bush v. Gore, 531 U.S. 98 (2000)"
    ),
    DoctrineBlock(
        topic="Unpublished Opinion Citation",
        keywords=["unpublished", "opinion", "citation", "precedent", "authority"],
        conclusion_template="Unpublished opinions may be cited as persuasive authority but are not binding.",
        reasoning_framework=(
            "Unpublished opinions are not officially reported and generally lack binding precedential effect. "
            "The court may cite unpublished opinions as persuasive authority if permitted by court rules. "
            "The court evaluates the reasoning, factual similarity, and acceptance of unpublished opinions. "
            "Some jurisdictions restrict citation of unpublished opinions; parties must comply with local rules."
        ),
        key_factors=[
            "Jurisdictional rules",
            "Reasoning strength",
            "Factual similarity",
            "Persuasive value"
        ],
        primary_authority=[
            "Fed. R. App. P. 32.1",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party citing unpublished opinion",
        adversary_position="Challenges citation or weight",
        counter_arguments=[
            "Opinion is not binding",
            "Jurisdictional rules prohibit citation",
            "Reasoning is weak"
        ],
        resolution_strategy="Cite unpublished opinions as persuasive authority if permitted",
        entity_scope="Federal and state courts",
        confidence=0.81,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Fed. R. App. P. 32.1"
    ),
    DoctrineBlock(
        topic="Interlocutory vs Final Judgment Precedent",
        keywords=["interlocutory", "final judgment", "precedent", "authority", "appeal"],
        conclusion_template="Final judgments carry greater precedential weight than interlocutory decisions.",
        reasoning_framework=(
            "Interlocutory decisions address preliminary issues and generally lack binding precedential effect. "
            "Final judgments resolve the merits and establish controlling precedent. "
            "The court distinguishes between interlocutory and final decisions when assessing authority. "
            "Interlocutory decisions may be cited as persuasive authority but are less influential."
        ),
        key_factors=[
            "Finality",
            "Scope",
            "Merits resolution",
            "Persuasive value"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Fed. R. Civ. P. 54(b)"
        ],
        burden_holder="Party relying on interlocutory or final decision",
        adversary_position="Challenges weight or applicability",
        counter_arguments=[
            "Decision is interlocutory",
            "No merits resolution",
            "Limited scope"
        ],
        resolution_strategy="Prioritize final judgments; cite interlocutory decisions as persuasive",
        entity_scope="All courts",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Fed. R. Civ. P. 54(b)"
    ),
    DoctrineBlock(
        topic="Dictum vs Holding Distinction",
        keywords=["dictum", "holding", "distinction", "precedent", "authority"],
        conclusion_template="Only holdings are binding; dicta may be persuasive but lack precedential force.",
        reasoning_framework=(
            "The court distinguishes between holdings, which resolve the legal issue, and dicta, which are extraneous statements. "
            "Holdings are binding precedent; dicta may be cited as persuasive authority. "
            "The court analyzes the opinion to identify the holding and distinguish it from dicta. "
            "Reliance on dicta is limited to persuasive value and does not establish controlling law."
        ),
        key_factors=[
            "Issue resolution",
            "Opinion analysis",
            "Persuasive value",
            "Binding effect"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "People v. Williams, 22 Cal. 4th 1209 (2000)"
        ],
        burden_holder="Party relying on holding or dicta",
        adversary_position="Challenges binding effect",
        counter_arguments=[
            "Statement is dicta",
            "No issue resolution",
            "Limited persuasive value"
        ],
        resolution_strategy="Apply holding as binding; cite dicta as persuasive",
        entity_scope="All courts",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="State Court Precedent in Federal Court",
        keywords=["state court", "precedent", "federal court", "Erie doctrine", "authority"],
        conclusion_template="Federal courts apply state court precedent in diversity cases unless federal law governs.",
        reasoning_framework=(
            "Under the Erie doctrine, federal courts sitting in diversity apply state substantive law, including state court precedent. "
            "Federal courts defer to the highest state court's interpretation of state law. "
            "If the state court has not addressed the issue, federal courts may predict how the state court would rule. "
            "Federal law governs procedural issues and federal questions."
        ),
        key_factors=[
            "Erie doctrine",
            "State substantive law",
            "Highest state court",
            "Federal procedural law"
        ],
        primary_authority=[
            "Erie Railroad Co. v. Tompkins, 304 U.S. 64 (1938)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Federal court applying state law",
        adversary_position="Challenges applicability of state precedent",
        counter_arguments=[
            "Issue is procedural",
            "Federal law governs",
            "State court has not addressed issue"
        ],
        resolution_strategy="Apply state court precedent in diversity cases; predict state law if necessary",
        entity_scope="Federal courts",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Erie Railroad Co. v. Tompkins, 304 U.S. 64 (1938)"
    ),
    DoctrineBlock(
        topic="Superseded by Statute Doctrine",
        keywords=["superseded", "statute", "doctrine", "precedent", "legislative override"],
        conclusion_template="Precedent is superseded by statute when legislative action overrides judicial interpretation.",
        reasoning_framework=(
            "Precedent may be superseded by statute when the legislature enacts a law that overrides judicial interpretation. "
            "The court analyzes the statutory language, legislative history, and intent to determine whether the statute abrogates prior precedent. "
            "Superseded precedent loses binding effect and must be reconciled with the new statutory framework. "
            "The court applies the statute as controlling law and may cite superseded precedent for historical context."
        ),
        key_factors=[
            "Statutory language",
            "Legislative history",
            "Intent",
            "Abrogation"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party asserting supersession",
        adversary_position="Challenges statutory override",
        counter_arguments=[
            "Statute does not abrogate precedent",
            "Legislative intent is unclear",
            "Precedent remains valid"
        ],
        resolution_strategy="Apply statute as controlling law; reconcile with prior precedent",
        entity_scope="All courts",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Landmark Case Identification Criteria",
        keywords=["landmark case", "identification", "criteria", "precedent", "authority"],
        conclusion_template="Landmark cases are identified by doctrinal impact, citation frequency, and acceptance.",
        reasoning_framework=(
            "Landmark cases are those with significant doctrinal impact, frequent citation, and broad acceptance. "
            "The court evaluates the case's influence on legal principles, its role in shaping jurisprudence, and its acceptance by courts and scholars. "
            "Landmark status may evolve over time as legal standards change. "
            "The court distinguishes landmark cases from routine decisions based on impact and citation history."
        ),
        key_factors=[
            "Doctrinal impact",
            "Citation frequency",
            "Acceptance",
            "Influence"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)"
        ],
        burden_holder="Party asserting landmark status",
        adversary_position="Challenges impact or acceptance",
        counter_arguments=[
            "Case is not widely cited",
            "Limited doctrinal impact",
            "Acceptance is disputed"
        ],
        resolution_strategy="Identify landmark cases based on criteria; prioritize doctrinal impact",
        entity_scope="All courts",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Trend Analysis Across Jurisdictions",
        keywords=["trend analysis", "jurisdictions", "precedent", "authority", "legal evolution"],
        conclusion_template="Trend analysis identifies evolving legal standards across jurisdictions.",
        reasoning_framework=(
            "Trend analysis involves reviewing decisions across multiple jurisdictions to identify evolving legal standards. "
            "The court considers the direction, frequency, and acceptance of trends. "
            "Trend analysis informs doctrinal development and may influence adoption of new legal principles. "
            "The court distinguishes between widespread trends and isolated decisions."
        ),
        key_factors=[
            "Direction",
            "Frequency",
            "Acceptance",
            "Doctrinal evolution"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party asserting trend",
        adversary_position="Challenges trend or acceptance",
        counter_arguments=[
            "Trend is isolated",
            "Limited acceptance",
            "No doctrinal evolution"
        ],
        resolution_strategy="Analyze trends across jurisdictions; inform doctrinal development",
        entity_scope="All courts",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Negative Precedent Treatment Analysis",
        keywords=["negative precedent", "treatment", "analysis", "overruled", "criticized"],
        conclusion_template="Negative treatment diminishes the authority and weight of precedent.",
        reasoning_framework=(
            "Negative precedent treatment includes overruling, criticism, and distinguishing. "
            "The court analyzes citator data and subsequent case treatment to assess authority. "
            "Negative treatment reduces the weight and reliability of precedent. "
            "The court avoids reliance on overruled or heavily criticized cases."
        ),
        key_factors=[
            "Overruling",
            "Criticism",
            "Distinguishing",
            "Citator data"
        ],
        primary_authority=[
            "Shepard's Citations",
            "KeyCite"
        ],
        burden_holder="Party relying on negatively treated precedent",
        adversary_position="Challenges authority or weight",
        counter_arguments=[
            "Precedent is overruled",
            "Criticism is widespread",
            "Limited reliability"
        ],
        resolution_strategy="Analyze negative treatment; adjust reliance accordingly",
        entity_scope="All courts",
        confidence=0.81,
        confidence_zone=ConfidenceZone.LOW.value,
        controlling_precedent="Shepard's Citations"
    ),
    # Additional DoctrineBlocks to reach 40+ instances
    DoctrineBlock(
        topic="Precedent Application in Statutory Interpretation",
        keywords=["statutory interpretation", "precedent", "application", "authority"],
        conclusion_template="Precedent guides statutory interpretation unless the statute is clear or has been amended.",
        reasoning_framework=(
            "Precedent plays a central role in statutory interpretation, providing guidance on ambiguous language and legislative intent. "
            "The court applies precedent unless the statute is clear or has been amended to override prior judicial interpretation. "
            "Statutory amendments may supersede precedent, requiring the court to reconcile new language with prior decisions."
        ),
        key_factors=[
            "Statutory clarity",
            "Amendments",
            "Legislative intent",
            "Precedent guidance"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on precedent",
        adversary_position="Challenges applicability due to statutory clarity or amendment",
        counter_arguments=[
            "Statute is clear",
            "Statute has been amended",
            "Precedent is outdated"
        ],
        resolution_strategy="Apply precedent unless statute is clear or amended",
        entity_scope="All courts",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Precedent in Constitutional Interpretation",
        keywords=["constitutional interpretation", "precedent", "authority", "Supreme Court"],
        conclusion_template="Precedent guides constitutional interpretation but may be reconsidered if societal values evolve.",
        reasoning_framework=(
            "Precedent is influential in constitutional interpretation, promoting stability and predictability. "
            "The Supreme Court may reconsider precedent if societal values evolve or if prior decisions are manifestly erroneous. "
            "The court weighs reliance interests, doctrinal consistency, and the impact of departure."
        ),
        key_factors=[
            "Societal values",
            "Manifest error",
            "Reliance interests",
            "Doctrinal consistency"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)"
        ],
        burden_holder="Party relying on constitutional precedent",
        adversary_position="Challenges precedent based on societal evolution",
        counter_arguments=[
            "Precedent is outdated",
            "Societal values have changed",
            "Manifest error"
        ],
        resolution_strategy="Apply precedent unless compelling reason for reconsideration",
        entity_scope="Supreme Court",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Precedent in Administrative Law",
        keywords=["administrative law", "precedent", "agency", "Chevron deference"],
        conclusion_template="Precedent guides interpretation of agency regulations; Chevron deference may apply.",
        reasoning_framework=(
            "Precedent informs interpretation of agency regulations and administrative law. "
            "The court applies Chevron deference, deferring to agency interpretation if the statute is ambiguous and the agency's interpretation is reasonable. "
            "Precedent may override agency interpretation if controlling authority exists."
        ),
        key_factors=[
            "Statutory ambiguity",
            "Agency interpretation",
            "Chevron deference",
            "Controlling precedent"
        ],
        primary_authority=[
            "Chevron U.S.A. Inc. v. Natural Resources Defense Council, Inc., 467 U.S. 837 (1984)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Agency or party relying on precedent",
        adversary_position="Challenges agency interpretation or precedent",
        counter_arguments=[
            "Statute is clear",
            "Agency interpretation is unreasonable",
            "Controlling precedent exists"
        ],
        resolution_strategy="Apply Chevron deference; reconcile with controlling precedent",
        entity_scope="Federal courts",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Chevron U.S.A. Inc. v. Natural Resources Defense Council, Inc., 467 U.S. 837 (1984)"
    ),
    DoctrineBlock(
        topic="Precedent in Criminal Law",
        keywords=["criminal law", "precedent", "authority", "Supreme Court"],
        conclusion_template="Precedent governs interpretation of criminal statutes and constitutional protections.",
        reasoning_framework=(
            "Precedent is critical in criminal law, guiding interpretation of statutes and constitutional protections. "
            "The court applies controlling precedent to ensure uniformity and protect due process rights. "
            "Departure from precedent is rare and must be justified by compelling reasons."
        ),
        key_factors=[
            "Statutory interpretation",
            "Constitutional protections",
            "Uniformity",
            "Compelling reasons"
        ],
        primary_authority=[
            "Miranda v. Arizona, 384 U.S. 436 (1966)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on criminal precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Compelling reason for departure"
        ],
        resolution_strategy="Apply criminal law precedent unless compelling reason for departure",
        entity_scope="All courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Miranda v. Arizona, 384 U.S. 436 (1966)"
    ),
    DoctrineBlock(
        topic="Precedent in Civil Law",
        keywords=["civil law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of civil statutes and common law principles.",
        reasoning_framework=(
            "Precedent is central to civil law, guiding interpretation of statutes and common law principles. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by manifest error or statutory amendment."
        ),
        key_factors=[
            "Statutory interpretation",
            "Common law principles",
            "Consistency",
            "Manifest error"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on civil precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply civil law precedent unless manifest error or statutory amendment",
        entity_scope="All courts",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Precedent in Family Law",
        keywords=["family law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of family law statutes and common law principles.",
        reasoning_framework=(
            "Precedent is influential in family law, guiding interpretation of statutes and common law principles. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Common law principles",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on family law precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply family law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Precedent in Tort Law",
        keywords=["tort law", "precedent", "authority", "common law"],
        conclusion_template="Precedent governs interpretation of tort principles and statutory provisions.",
        reasoning_framework=(
            "Precedent is central to tort law, guiding interpretation of common law principles and statutory provisions. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by manifest error or statutory amendment."
        ),
        key_factors=[
            "Common law principles",
            "Statutory provisions",
            "Consistency",
            "Manifest error"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on tort precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply tort law precedent unless manifest error or statutory amendment",
        entity_scope="All courts",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Precedent in Contract Law",
        keywords=["contract law", "precedent", "authority", "common law"],
        conclusion_template="Precedent guides interpretation of contract principles and statutory provisions.",
        reasoning_framework=(
            "Precedent is influential in contract law, guiding interpretation of common law principles and statutory provisions. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by manifest error or statutory amendment."
        ),
        key_factors=[
            "Common law principles",
            "Statutory provisions",
            "Consistency",
            "Manifest error"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on contract precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply contract law precedent unless manifest error or statutory amendment",
        entity_scope="All courts",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Precedent in Property Law",
        keywords=["property law", "precedent", "authority", "common law"],
        conclusion_template="Precedent governs interpretation of property principles and statutory provisions.",
        reasoning_framework=(
            "Precedent is central to property law, guiding interpretation of common law principles and statutory provisions. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by manifest error or statutory amendment."
        ),
        key_factors=[
            "Common law principles",
            "Statutory provisions",
            "Consistency",
            "Manifest error"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on property precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply property law precedent unless manifest error or statutory amendment",
        entity_scope="All courts",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Precedent in Environmental Law",
        keywords=["environmental law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of environmental statutes and regulations.",
        reasoning_framework=(
            "Precedent is influential in environmental law, guiding interpretation of statutes and regulations. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Regulatory provisions",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "Chevron U.S.A. Inc. v. Natural Resources Defense Council, Inc., 467 U.S. 837 (1984)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on environmental precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply environmental law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Chevron U.S.A. Inc. v. Natural Resources Defense Council, Inc., 467 U.S. 837 (1984)"
    ),
    DoctrineBlock(
        topic="Precedent in Intellectual Property Law",
        keywords=["intellectual property", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of intellectual property statutes and common law principles.",
        reasoning_framework=(
            "Precedent is central to intellectual property law, guiding interpretation of statutes and common law principles. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Common law principles",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on intellectual property precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply intellectual property law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.86,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Precedent in Bankruptcy Law",
        keywords=["bankruptcy law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of bankruptcy statutes and regulations.",
        reasoning_framework=(
            "Precedent is influential in bankruptcy law, guiding interpretation of statutes and regulations. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Regulatory provisions",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on bankruptcy precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply bankruptcy law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Precedent in Tax Law",
        keywords=["tax law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of tax statutes and regulations.",
        reasoning_framework=(
            "Precedent is central to tax law, guiding interpretation of statutes and regulations. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Regulatory provisions",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on tax precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply tax law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Precedent in Employment Law",
        keywords=["employment law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of employment statutes and common law principles.",
        reasoning_framework=(
            "Precedent is influential in employment law, guiding interpretation of statutes and common law principles. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Common law principles",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on employment precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply employment law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Precedent in Antitrust Law",
        keywords=["antitrust law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of antitrust statutes and regulations.",
        reasoning_framework=(
            "Precedent is central to antitrust law, guiding interpretation of statutes and regulations. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Regulatory provisions",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on antitrust precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply antitrust law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Precedent in Securities Law",
        keywords=["securities law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of securities statutes and regulations.",
        reasoning_framework=(
            "Precedent is influential in securities law, guiding interpretation of statutes and regulations. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Regulatory provisions",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on securities precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply securities law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Precedent in Immigration Law",
        keywords=["immigration law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of immigration statutes and regulations.",
        reasoning_framework=(
            "Precedent is central to immigration law, guiding interpretation of statutes and regulations. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Regulatory provisions",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on immigration precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply immigration law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Precedent in Consumer Protection Law",
        keywords=["consumer protection", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of consumer protection statutes and regulations.",
        reasoning_framework=(
            "Precedent is influential in consumer protection law, guiding interpretation of statutes and regulations. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Regulatory provisions",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on consumer protection precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply consumer protection law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Precedent in Health Law",
        keywords=["health law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of health statutes and regulations.",
        reasoning_framework=(
            "Precedent is central to health law, guiding interpretation of statutes and regulations. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Regulatory provisions",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "United States v. Mead Corp., 533 U.S. 218 (2001)",
            "Brown v. Board of Education, 347 U.S. 483 (1954)"
        ],
        burden_holder="Party relying on health law precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply health law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="United States v. Mead Corp., 533 U.S. 218 (2001)"
    ),
    DoctrineBlock(
        topic="Precedent in Education Law",
        keywords=["education law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of education statutes and regulations.",
        reasoning_framework=(
            "Precedent is influential in education law, guiding interpretation of statutes and regulations. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Regulatory provisions",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "United States v. Mead Corp., 533 U.S. 218 (2001)"
        ],
        burden_holder="Party relying on education law precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply education law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
    DoctrineBlock(
        topic="Precedent in Civil Rights Law",
        keywords=["civil rights law", "precedent", "authority", "statutory interpretation"],
        conclusion_template="Precedent guides interpretation of civil rights statutes and constitutional protections.",
        reasoning_framework=(
            "Precedent is critical in civil rights law, guiding interpretation of statutes and constitutional protections. "
            "The court applies controlling precedent to resolve disputes and promote consistency. "
            "Departure from precedent is justified only by statutory amendment or manifest error."
        ),
        key_factors=[
            "Statutory interpretation",
            "Constitutional protections",
            "Consistency",
            "Statutory amendment"
        ],
        primary_authority=[
            "Brown v. Board of Education, 347 U.S. 483 (1954)",
            "Planned Parenthood v. Casey, 505 U.S. 833 (1992)"
        ],
        burden_holder="Party relying on civil rights precedent",
        adversary_position="Challenges precedent or interpretation",
        counter_arguments=[
            "Precedent is outdated",
            "Statute has been amended",
            "Manifest error"
        ],
        resolution_strategy="Apply civil rights law precedent unless statutory amendment or manifest error",
        entity_scope="All courts",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Brown v. Board of Education, 347 U.S. 483 (1954)"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or \
           any(keyword_lower in k.lower() for k in doctrine.keywords) or \
           keyword_lower in doctrine.reasoning_framework.lower():
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]