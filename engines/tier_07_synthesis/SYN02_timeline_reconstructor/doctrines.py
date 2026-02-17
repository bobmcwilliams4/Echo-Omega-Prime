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
        topic="event_extraction_from_pleadings",
        keywords=["pleadings", "event extraction", "timeline", "facts", "legal documents"],
        conclusion_template="The extracted events from pleadings establish the factual timeline relevant to the dispute.",
        reasoning_framework="""
        Event extraction from pleadings involves parsing legal documents to identify and chronologically order factual assertions. The process leverages natural language processing techniques, legal heuristics, and domain-specific rules to distinguish between alleged facts, procedural events, and legal conclusions. The extracted events are mapped to a timeline, ensuring each event is anchored by a date or temporal reference. Ambiguities are resolved by cross-referencing with other filings and corroborating evidence. The completeness and accuracy of the event set are validated against the pleadings' structure and judicial requirements for materiality and relevance.
        """,
        key_factors=[
            "Clarity of event descriptions",
            "Presence of temporal markers",
            "Consistency across pleadings",
            "Materiality to the dispute",
            "Corroboration with evidence"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 8(a)",
            "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)",
            "Ashcroft v. Iqbal, 556 U.S. 662 (2009)"
        ],
        burden_holder="Plaintiff",
        adversary_position="Defendant may challenge factual sufficiency or temporal accuracy",
        counter_arguments=[
            "Events are conclusory rather than factual",
            "Temporal ambiguity undermines reliability",
            "Events are immaterial or irrelevant"
        ],
        resolution_strategy="Supplement extraction with cross-document validation and judicial review",
        entity_scope="All parties in litigation",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Twombly/Iqbal pleading standards"
    ),
    DoctrineBlock(
        topic="date_normalization_and_formatting",
        keywords=["date normalization", "formatting", "timeline", "ISO 8601", "legal documents"],
        conclusion_template="Normalized dates ensure consistent and accurate timeline reconstruction across all legal documents.",
        reasoning_framework="""
        Date normalization and formatting require converting all temporal references into a standardized format, typically ISO 8601. This process addresses variations in date expressions, ambiguous references (e.g., 'the following Monday'), and inconsistencies across documents. The framework applies regular expressions, context-aware parsing, and legal domain rules to resolve ambiguities. Where dates are missing or unclear, inferential logic and corroboration with related events are used. The normalized dates facilitate reliable timeline analysis and integration with downstream temporal algorithms.
        """,
        key_factors=[
            "Presence of explicit date references",
            "Consistency in date formats",
            "Resolution of ambiguous temporal expressions",
            "Integration with timeline algorithms"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 10(b)",
            "ISO 8601 Standard",
            "Federal Judicial Center, Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Document preparer",
        adversary_position="Opposing party may dispute inferred dates",
        counter_arguments=[
            "Date inference introduces error",
            "Formatting obscures original context",
            "Ambiguity remains unresolved"
        ],
        resolution_strategy="Document all normalization steps and provide audit trail",
        entity_scope="All timeline-relevant documents",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation guidance"
    ),
    DoctrineBlock(
        topic="temporal_ordering_algorithms",
        keywords=["temporal ordering", "timeline", "event sequencing", "chronology", "algorithm"],
        conclusion_template="Temporal ordering algorithms establish the correct sequence of events for legal analysis.",
        reasoning_framework="""
        Temporal ordering algorithms utilize extracted event dates and logical dependencies to sequence events chronologically. The framework incorporates sorting techniques, dependency graphs, and legal rules governing event precedence (e.g., filing before response). Where dates are missing, inferred ordering based on procedural rules or contextual clues is applied. The algorithm validates the sequence against legal requirements for event progression and identifies inconsistencies or gaps. Robust ordering is critical for statute of limitations, critical path analysis, and judicial review.
        """,
        key_factors=[
            "Availability of event dates",
            "Legal rules for event precedence",
            "Dependency relationships",
            "Handling of missing or ambiguous dates"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 6",
            "Federal Judicial Center, Timeline Analysis",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may challenge ordering assumptions",
        counter_arguments=[
            "Ordering relies on inferred dates",
            "Legal rules not properly applied",
            "Sequence conflicts with documentary evidence"
        ],
        resolution_strategy="Iterative validation with legal counsel and documentary review",
        entity_scope="All events in dispute",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="gap_detection_heuristics",
        keywords=["gap detection", "timeline", "missing events", "heuristics", "temporal analysis"],
        conclusion_template="Gap detection heuristics identify missing or ambiguous periods in the reconstructed timeline.",
        reasoning_framework="""
        Gap detection heuristics analyze the reconstructed timeline for periods lacking event coverage or containing ambiguous temporal references. The framework applies statistical analysis, legal procedural expectations, and domain-specific heuristics to flag gaps. Typical gaps include missing filings, unexplained delays, or periods between procedural milestones. The analysis considers legal requirements for event continuity and identifies potential areas for further investigation or supplementation. Gaps may indicate evidentiary deficiencies or procedural irregularities.
        """,
        key_factors=[
            "Expected procedural milestones",
            "Temporal continuity",
            "Presence of unexplained delays",
            "Legal requirements for event coverage"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Federal Judicial Center, Timeline Gap Analysis",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may argue gaps are immaterial",
        counter_arguments=[
            "Gaps do not affect material issues",
            "Heuristics misidentify normal procedural delays",
            "Gaps are explained elsewhere"
        ],
        resolution_strategy="Supplement timeline with additional discovery or judicial inquiry",
        entity_scope="Timeline-relevant periods",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="parallel_track_identification",
        keywords=["parallel tracks", "timeline", "multiple proceedings", "identification", "legal process"],
        conclusion_template="Parallel track identification reveals concurrent legal or procedural tracks impacting the timeline.",
        reasoning_framework="""
        Parallel track identification examines the timeline for concurrent proceedings, such as related cases, administrative actions, or parallel investigations. The framework maps events across tracks, identifies points of intersection, and analyzes the impact on deadlines, stays, or procedural requirements. Legal rules governing coordination, comity, and consolidation are applied. The analysis ensures that all relevant tracks are integrated into the master timeline, preventing oversight of material events or deadlines.
        """,
        key_factors=[
            "Existence of related proceedings",
            "Overlap of event dates",
            "Legal rules for coordination",
            "Impact on deadlines and stays"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 42",
            "28 U.S.C. § 1404",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may dispute relevance of parallel tracks",
        counter_arguments=[
            "Tracks are independent and immaterial",
            "Integration introduces confusion",
            "Legal coordination not required"
        ],
        resolution_strategy="Document track relationships and seek judicial guidance as needed",
        entity_scope="All related proceedings",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="statute_of_limitations_calculation",
        keywords=["statute of limitations", "calculation", "timeline", "deadline", "legal analysis"],
        conclusion_template="Statute of limitations calculation determines the deadline for filing claims based on event dates.",
        reasoning_framework="""
        Statute of limitations calculation applies relevant statutory or contractual deadlines to the timeline of events. The framework identifies the triggering event, calculates the limitation period, and accounts for tolling provisions, equitable exceptions, and jurisdictional variations. Legal research is conducted to determine the applicable statute, and all relevant dates are cross-referenced. The analysis ensures claims are timely or identifies potential defenses based on expiration.
        """,
        key_factors=[
            "Identification of triggering event",
            "Applicable statutory or contractual period",
            "Tolling provisions",
            "Jurisdictional rules"
        ],
        primary_authority=[
            "28 U.S.C. § 1658",
            "Relevant state statutes",
            "Case law interpreting limitation periods"
        ],
        burden_holder="Claimant",
        adversary_position="Defendant may assert limitations defense",
        counter_arguments=[
            "Tolling applies",
            "Triggering event is later than alleged",
            "Statute is inapplicable"
        ],
        resolution_strategy="Comprehensive legal research and timeline validation",
        entity_scope="All claims in dispute",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="28 U.S.C. § 1658"
    ),
    DoctrineBlock(
        topic="deadline_cascade_analysis",
        keywords=["deadline cascade", "timeline", "analysis", "procedural deadlines", "dependency"],
        conclusion_template="Deadline cascade analysis maps dependent procedural deadlines to ensure compliance.",
        reasoning_framework="""
        Deadline cascade analysis identifies and maps procedural deadlines that are dependent on prior events. The framework analyzes rules governing response periods, extensions, and cascading deadlines (e.g., answer due after complaint filing). Legal procedural rules and court orders are integrated into the timeline. The analysis validates compliance, flags missed deadlines, and identifies potential procedural defenses or remedies. Cascade mapping is critical for complex litigation and multi-track proceedings.
        """,
        key_factors=[
            "Identification of triggering deadlines",
            "Dependency relationships",
            "Procedural rules and court orders",
            "Compliance validation"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 6",
            "Fed. R. Civ. P. 12",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Litigant",
        adversary_position="Opposing party may dispute deadline calculations",
        counter_arguments=[
            "Extensions or stays apply",
            "Dependency relationships misapplied",
            "Deadline calculation error"
        ],
        resolution_strategy="Review procedural rules and validate with court records",
        entity_scope="All procedural deadlines",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="critical_path_identification",
        keywords=["critical path", "timeline", "identification", "event dependency", "legal process"],
        conclusion_template="Critical path identification isolates the sequence of events essential to case resolution.",
        reasoning_framework="""
        Critical path identification applies project management principles to legal timelines, isolating the sequence of dependent events that determine case progression. The framework constructs dependency graphs, identifies bottlenecks, and maps the minimum timeline for resolution. Legal rules governing event dependencies and procedural requirements are integrated. The analysis highlights events that, if delayed, impact the overall timeline and case outcome. Critical path mapping supports judicial management and strategic planning.
        """,
        key_factors=[
            "Event dependency relationships",
            "Procedural requirements",
            "Bottleneck identification",
            "Impact on case outcome"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Project Management Institute, PMBOK Guide",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may dispute path relevance",
        counter_arguments=[
            "Path does not reflect all material events",
            "Dependency relationships are incorrect",
            "Alternate paths exist"
        ],
        resolution_strategy="Validate with legal counsel and procedural review",
        entity_scope="Case-critical events",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="temporal_inconsistency_detection",
        keywords=["temporal inconsistency", "timeline", "detection", "event conflict", "legal analysis"],
        conclusion_template="Temporal inconsistency detection flags conflicting or impossible event sequences in the timeline.",
        reasoning_framework="""
        Temporal inconsistency detection analyzes the timeline for events that conflict with logical, procedural, or legal requirements. The framework applies consistency checks, dependency validation, and cross-document comparison to identify impossible sequences (e.g., response filed before complaint). Legal rules governing event order and procedural requirements are used to validate consistency. The analysis supports judicial review and evidentiary reliability.
        """,
        key_factors=[
            "Logical event order",
            "Procedural requirements",
            "Cross-document consistency",
            "Legal rules for event sequencing"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 6",
            "Manual for Complex Litigation (4th ed.)",
            "Federal Judicial Center, Timeline Consistency"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may dispute inconsistency materiality",
        counter_arguments=[
            "Inconsistency is immaterial",
            "Sequence reflects procedural exceptions",
            "Documentary evidence resolves conflict"
        ],
        resolution_strategy="Supplement timeline with additional evidence or judicial clarification",
        entity_scope="All timeline events",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="gantt_chart_representation",
        keywords=["gantt chart", "timeline", "visualization", "event mapping", "legal process"],
        conclusion_template="Gantt chart representation provides a visual mapping of the legal timeline for analysis and presentation.",
        reasoning_framework="""
        Gantt chart representation translates the reconstructed timeline into a visual format, mapping events, deadlines, and dependencies. The framework applies project management visualization principles, ensuring clarity, accuracy, and legal relevance. Events are color-coded by category, dependencies are illustrated, and critical paths are highlighted. The chart supports judicial review, case management, and strategic planning. Legal requirements for confidentiality and accuracy are observed.
        """,
        key_factors=[
            "Clarity of visual mapping",
            "Accuracy of event placement",
            "Representation of dependencies",
            "Compliance with confidentiality requirements"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Project Management Institute, PMBOK Guide",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may challenge chart accuracy",
        counter_arguments=[
            "Chart misrepresents event sequence",
            "Dependencies are incorrect",
            "Visual format obscures material issues"
        ],
        resolution_strategy="Validate chart with legal counsel and documentary review",
        entity_scope="All timeline events",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="relation_back_doctrine",
        keywords=["relation back", "doctrine", "timeline", "amendment", "statute of limitations"],
        conclusion_template="The relation back doctrine allows amended pleadings to relate to the original filing date for limitations purposes.",
        reasoning_framework="""
        The relation back doctrine, governed by Fed. R. Civ. P. 15(c), permits amended pleadings to relate back to the date of the original filing under specified circumstances. The framework analyzes whether the amendment arises from the same conduct, transaction, or occurrence as the original pleading. Legal rules and case law are applied to determine if the statute of limitations is satisfied. The doctrine supports equitable resolution and prevents procedural unfairness.
        """,
        key_factors=[
            "Same conduct, transaction, or occurrence",
            "Timeliness of amendment",
            "Notice to opposing party",
            "Statute of limitations compliance"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 15(c)",
            "Krupski v. Costa Crociere S.p.A., 560 U.S. 538 (2010)",
            "Case law interpreting relation back"
        ],
        burden_holder="Amending party",
        adversary_position="Opposing party may challenge relation back applicability",
        counter_arguments=[
            "Amendment introduces new claims",
            "Notice was insufficient",
            "Statute of limitations expired"
        ],
        resolution_strategy="Legal research and judicial motion practice",
        entity_scope="Amended pleadings",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Krupski v. Costa Crociere"
    ),
    DoctrineBlock(
        topic="nunc_pro_tunc_orders",
        keywords=["nunc pro tunc", "orders", "timeline", "retroactive", "judicial correction"],
        conclusion_template="Nunc pro tunc orders retroactively correct or clarify the record to reflect judicial intent.",
        reasoning_framework="""
        Nunc pro tunc orders are judicial instruments used to correct clerical errors or clarify the record retroactively. The framework analyzes whether the correction reflects the court's original intent and is limited to clerical, not substantive, matters. Legal rules and case law are applied to determine the propriety and effect of the order. The analysis ensures that retroactive correction does not prejudice parties or alter substantive rights.
        """,
        key_factors=[
            "Nature of correction (clerical vs. substantive)",
            "Judicial intent",
            "Potential prejudice to parties",
            "Compliance with procedural rules"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 60(a)",
            "Case law on nunc pro tunc orders",
            "Federal Judicial Center, Judicial Correction"
        ],
        burden_holder="Moving party",
        adversary_position="Opposing party may challenge retroactive effect",
        counter_arguments=[
            "Correction is substantive",
            "Retroactive effect prejudices rights",
            "Judicial intent is unclear"
        ],
        resolution_strategy="Motion practice and judicial review",
        entity_scope="Court orders and judgments",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Case law interpreting Fed. R. Civ. P. 60(a)"
    ),
    DoctrineBlock(
        topic="retroactive_application_of_law",
        keywords=["retroactive", "application", "law", "timeline", "statutory interpretation"],
        conclusion_template="Retroactive application of law is permitted only where statutory or judicial authority allows.",
        reasoning_framework="""
        Retroactive application of law is governed by statutory interpretation and judicial precedent. The framework analyzes whether the statute or rule expressly permits retroactivity, or whether judicial authority supports such application. Legal rules prohibit retroactivity absent clear legislative intent or compelling judicial rationale. The analysis considers fairness, reliance interests, and potential prejudice. Retroactive application is rare and subject to strict scrutiny.
        """,
        key_factors=[
            "Statutory language",
            "Legislative intent",
            "Judicial precedent",
            "Fairness and reliance interests"
        ],
        primary_authority=[
            "Landgraf v. USI Film Products, 511 U.S. 244 (1994)",
            "Relevant statutes",
            "Case law on retroactivity"
        ],
        burden_holder="Party seeking retroactive application",
        adversary_position="Opposing party may assert reliance and fairness arguments",
        counter_arguments=[
            "Statute is silent or prohibits retroactivity",
            "Reliance interests are prejudiced",
            "Judicial precedent prohibits retroactivity"
        ],
        resolution_strategy="Statutory and case law analysis",
        entity_scope="All parties affected by law change",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Landgraf v. USI Film Products"
    ),
    DoctrineBlock(
        topic="document_dating_forensics",
        keywords=["document dating", "forensics", "timeline", "authentication", "legal evidence"],
        conclusion_template="Document dating forensics authenticate the timing of document creation and modification.",
        reasoning_framework="""
        Document dating forensics apply technical and legal methods to authenticate the creation and modification dates of documents. The framework leverages metadata analysis, forensic examination, and corroboration with external evidence. Legal rules governing authentication and admissibility are applied. The analysis identifies potential tampering, backdating, or discrepancies. Forensic results support evidentiary reliability and judicial review.
        """,
        key_factors=[
            "Metadata analysis",
            "Forensic examination",
            "Corroboration with external evidence",
            "Legal rules for authentication"
        ],
        primary_authority=[
            "Fed. R. Evid. 901",
            "Case law on document authentication",
            "Federal Judicial Center, Evidence Forensics"
        ],
        burden_holder="Proponent of document",
        adversary_position="Opposing party may challenge authenticity",
        counter_arguments=[
            "Metadata is unreliable",
            "Forensic methods are flawed",
            "Document was tampered with"
        ],
        resolution_strategy="Expert testimony and judicial review",
        entity_scope="All documentary evidence",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fed. R. Evid. 901"
    ),
    DoctrineBlock(
        topic="multi_jurisdiction_timeline_conflicts",
        keywords=["multi-jurisdiction", "timeline", "conflicts", "legal process", "choice of law"],
        conclusion_template="Multi-jurisdiction timeline conflicts are resolved through choice of law and procedural coordination.",
        reasoning_framework="""
        Multi-jurisdiction timeline conflicts arise when events span multiple legal jurisdictions with differing procedural rules and deadlines. The framework applies choice of law principles, analyzes procedural requirements, and coordinates timelines across jurisdictions. Legal rules governing comity, consolidation, and conflict resolution are applied. The analysis ensures compliance with all relevant deadlines and prevents procedural prejudice.
        """,
        key_factors=[
            "Jurisdictional procedural rules",
            "Choice of law principles",
            "Coordination of deadlines",
            "Conflict resolution mechanisms"
        ],
        primary_authority=[
            "Restatement (Second) of Conflict of Laws",
            "Fed. R. Civ. P. 42",
            "Case law on multi-jurisdiction coordination"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may assert jurisdictional privilege",
        counter_arguments=[
            "Jurisdictional rules are incompatible",
            "Choice of law is disputed",
            "Procedural coordination is impractical"
        ],
        resolution_strategy="Legal research and judicial coordination",
        entity_scope="All parties in multi-jurisdiction cases",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Restatement (Second) of Conflict of Laws"
    ),
    DoctrineBlock(
        topic="discovery_timeline_planning",
        keywords=["discovery", "timeline", "planning", "legal process", "case management"],
        conclusion_template="Discovery timeline planning ensures timely and efficient completion of discovery obligations.",
        reasoning_framework="""
        Discovery timeline planning maps all discovery-related events, deadlines, and dependencies. The framework applies procedural rules, court orders, and case management guidelines to sequence discovery requests, responses, and motions. Legal requirements for timely completion and judicial management are integrated. The analysis identifies bottlenecks, flags missed deadlines, and supports strategic planning. Discovery timeline mapping is critical for complex litigation.
        """,
        key_factors=[
            "Procedural rules for discovery",
            "Court orders and case management",
            "Dependency relationships",
            "Timeliness and efficiency"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 26",
            "Fed. R. Civ. P. 37",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Litigant",
        adversary_position="Opposing party may challenge timeline adequacy",
        counter_arguments=[
            "Timeline is unrealistic",
            "Missed deadlines prejudice case",
            "Discovery obligations are unmet"
        ],
        resolution_strategy="Case management conference and judicial oversight",
        entity_scope="Discovery events",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="contract_performance_milestones",
        keywords=["contract", "performance", "milestones", "timeline", "legal obligations"],
        conclusion_template="Contract performance milestones are mapped to the timeline for compliance and enforcement analysis.",
        reasoning_framework="""
        Contract performance milestones are identified and mapped to the timeline based on contractual terms and legal requirements. The framework analyzes milestone dates, dependencies, and obligations. Legal rules governing contract interpretation and enforcement are applied. The analysis validates compliance, flags missed milestones, and supports breach or enforcement claims. Milestone mapping is critical for complex contracts and project management.
        """,
        key_factors=[
            "Contractual terms",
            "Milestone dates and dependencies",
            "Legal rules for interpretation",
            "Compliance validation"
        ],
        primary_authority=[
            "Restatement (Second) of Contracts",
            "Uniform Commercial Code",
            "Case law on contract performance"
        ],
        burden_holder="Contracting party",
        adversary_position="Opposing party may dispute milestone interpretation",
        counter_arguments=[
            "Milestones are ambiguous",
            "Obligations are disputed",
            "Compliance is excused"
        ],
        resolution_strategy="Legal research and contractual review",
        entity_scope="Contract parties",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Restatement (Second) of Contracts"
    ),
    DoctrineBlock(
        topic="appeal_timeline_and_finality",
        keywords=["appeal", "timeline", "finality", "legal process", "judgment"],
        conclusion_template="Appeal timeline and finality analysis determines the window for appeal and the finality of judgments.",
        reasoning_framework="""
        Appeal timeline and finality analysis applies procedural rules governing the time to appeal and the finality of judgments. The framework identifies triggering events, calculates appeal deadlines, and analyzes exceptions (e.g., post-judgment motions). Legal rules and case law are applied to determine finality and appealability. The analysis supports strategic planning and judicial review.
        """,
        key_factors=[
            "Procedural rules for appeal",
            "Triggering events",
            "Exceptions to finality",
            "Compliance with deadlines"
        ],
        primary_authority=[
            "Fed. R. App. P. 4",
            "28 U.S.C. § 1291",
            "Case law on appeal finality"
        ],
        burden_holder="Appellant",
        adversary_position="Appellee may challenge appeal timeliness",
        counter_arguments=[
            "Appeal is untimely",
            "Judgment is not final",
            "Exceptions apply"
        ],
        resolution_strategy="Legal research and motion practice",
        entity_scope="All parties to judgment",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="28 U.S.C. § 1291"
    ),
    DoctrineBlock(
        topic="regulatory_compliance_deadlines",
        keywords=["regulatory", "compliance", "deadlines", "timeline", "legal obligations"],
        conclusion_template="Regulatory compliance deadlines are mapped to the timeline to ensure timely fulfillment of obligations.",
        reasoning_framework="""
        Regulatory compliance deadlines are identified and mapped based on statutory, regulatory, and contractual requirements. The framework analyzes deadline dates, dependencies, and potential extensions. Legal rules governing compliance, enforcement, and penalty provisions are applied. The analysis validates timely fulfillment, flags missed deadlines, and supports compliance planning. Deadline mapping is critical for regulated entities and complex transactions.
        """,
        key_factors=[
            "Statutory and regulatory requirements",
            "Deadline dates and dependencies",
            "Extension provisions",
            "Compliance validation"
        ],
        primary_authority=[
            "Relevant statutes and regulations",
            "Case law on regulatory compliance",
            "Agency guidance"
        ],
        burden_holder="Regulated entity",
        adversary_position="Regulator may challenge compliance",
        counter_arguments=[
            "Deadline was missed",
            "Extension provisions were misapplied",
            "Compliance is disputed"
        ],
        resolution_strategy="Legal research and agency consultation",
        entity_scope="Regulated entities",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Agency guidance and case law"
    ),
    DoctrineBlock(
        topic="bankruptcy_timeline_and_automatic_stay",
        keywords=["bankruptcy", "timeline", "automatic stay", "legal process", "event mapping"],
        conclusion_template="Bankruptcy timeline and automatic stay analysis maps events and identifies periods of stay.",
        reasoning_framework="""
        Bankruptcy timeline and automatic stay analysis applies statutory and procedural rules to map bankruptcy events and identify periods during which the automatic stay is in effect. The framework analyzes filing dates, stay triggers, and exceptions. Legal rules governing stay scope, relief, and enforcement are applied. The analysis supports compliance, creditor strategy, and judicial review.
        """,
        key_factors=[
            "Bankruptcy filing date",
            "Automatic stay triggers",
            "Scope and exceptions",
            "Compliance with stay"
        ],
        primary_authority=[
            "11 U.S.C. § 362",
            "Fed. R. Bankr. P. 4001",
            "Case law on automatic stay"
        ],
        burden_holder="Debtor",
        adversary_position="Creditor may seek stay relief",
        counter_arguments=[
            "Stay does not apply",
            "Exceptions permit action",
            "Relief from stay is warranted"
        ],
        resolution_strategy="Motion practice and judicial review",
        entity_scope="Debtors and creditors",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="11 U.S.C. § 362"
    ),
    DoctrineBlock(
        topic="witness_testimony_timeline_consistency",
        keywords=["witness", "testimony", "timeline", "consistency", "legal evidence"],
        conclusion_template="Witness testimony timeline consistency analysis validates alignment of testimony with reconstructed timeline.",
        reasoning_framework="""
        Witness testimony timeline consistency analysis compares testimony with the reconstructed timeline to validate alignment and identify discrepancies. The framework applies cross-examination techniques, documentary corroboration, and legal rules for impeachment. The analysis supports evidentiary reliability, judicial review, and strategic planning. Discrepancies are flagged for further investigation or clarification.
        """,
        key_factors=[
            "Alignment with reconstructed timeline",
            "Documentary corroboration",
            "Legal rules for impeachment",
            "Materiality of discrepancies"
        ],
        primary_authority=[
            "Fed. R. Evid. 607",
            "Case law on witness impeachment",
            "Federal Judicial Center, Evidence Consistency"
        ],
        burden_holder="Proponent of testimony",
        adversary_position="Opposing party may impeach witness",
        counter_arguments=[
            "Testimony is inconsistent",
            "Discrepancies are material",
            "Documentary evidence contradicts testimony"
        ],
        resolution_strategy="Cross-examination and supplemental evidence",
        entity_scope="All witnesses",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fed. R. Evid. 607"
    ),
    DoctrineBlock(
        topic="corporate_transaction_timeline",
        keywords=["corporate", "transaction", "timeline", "event mapping", "legal process"],
        conclusion_template="Corporate transaction timeline mapping sequences all material events for compliance and risk analysis.",
        reasoning_framework="""
        Corporate transaction timeline mapping identifies and sequences all material events in corporate transactions, including negotiations, approvals, filings, and closings. The framework applies legal requirements for disclosure, regulatory approval, and contractual obligations. The analysis validates compliance, flags missed deadlines, and supports risk analysis. Timeline mapping is critical for mergers, acquisitions, and complex transactions.
        """,
        key_factors=[
            "Material event identification",
            "Legal and regulatory requirements",
            "Dependency relationships",
            "Compliance validation"
        ],
        primary_authority=[
            "Delaware General Corporation Law",
            "SEC regulations",
            "Case law on corporate transactions"
        ],
        burden_holder="Corporate parties",
        adversary_position="Opposing party may dispute event materiality",
        counter_arguments=[
            "Events are immaterial",
            "Compliance is disputed",
            "Deadlines were missed"
        ],
        resolution_strategy="Legal research and corporate counsel review",
        entity_scope="Corporate parties",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Delaware General Corporation Law"
    ),
    DoctrineBlock(
        topic="statute_of_repose",
        keywords=["statute of repose", "timeline", "deadline", "legal analysis", "limitations"],
        conclusion_template="Statute of repose analysis determines the absolute deadline for claims regardless of discovery.",
        reasoning_framework="""
        Statute of repose analysis applies statutory rules establishing an absolute deadline for claims, regardless of discovery or tolling. The framework identifies the triggering event, calculates the repose period, and analyzes exceptions. Legal rules and case law are applied to determine applicability and effect. The analysis supports defense strategy and judicial review.
        """,
        key_factors=[
            "Identification of triggering event",
            "Statutory repose period",
            "Exceptions and tolling",
            "Applicability to claims"
        ],
        primary_authority=[
            "Relevant state statutes",
            "Case law on statute of repose",
            "Restatement (Second) of Torts"
        ],
        burden_holder="Claimant",
        adversary_position="Defendant may assert repose defense",
        counter_arguments=[
            "Exceptions apply",
            "Triggering event is disputed",
            "Statute is inapplicable"
        ],
        resolution_strategy="Legal research and timeline validation",
        entity_scope="All claims subject to repose",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Case law interpreting statute of repose"
    ),
    DoctrineBlock(
        topic="laches_and_equitable_estoppel",
        keywords=["laches", "equitable estoppel", "timeline", "delay", "legal defense"],
        conclusion_template="Laches and equitable estoppel may bar claims where unreasonable delay prejudices the opposing party.",
        reasoning_framework="""
        Laches and equitable estoppel are equitable defenses that may bar claims where unreasonable delay prejudices the opposing party. The framework analyzes the length and reason for delay, prejudice to the defendant, and legal requirements for equitable relief. Case law and statutory rules are applied. The analysis supports defense strategy and judicial review.
        """,
        key_factors=[
            "Length and reason for delay",
            "Prejudice to opposing party",
            "Legal requirements for equitable relief",
            "Materiality of delay"
        ],
        primary_authority=[
            "Petrella v. MGM, 572 U.S. 663 (2014)",
            "Case law on laches and estoppel",
            "Restatement (Second) of Contracts"
        ],
        burden_holder="Defendant",
        adversary_position="Plaintiff may assert justification for delay",
        counter_arguments=[
            "Delay was reasonable",
            "No prejudice occurred",
            "Equitable relief is unwarranted"
        ],
        resolution_strategy="Legal research and evidentiary analysis",
        entity_scope="All parties",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Petrella v. MGM"
    ),
    DoctrineBlock(
        topic="insurance_notice_and_claim_timeline",
        keywords=["insurance", "notice", "claim", "timeline", "legal obligations"],
        conclusion_template="Insurance notice and claim timeline analysis validates timely notice and claim filing for coverage.",
        reasoning_framework="""
        Insurance notice and claim timeline analysis maps all notice and claim events to validate compliance with policy requirements. The framework analyzes policy language, statutory rules, and case law. Timely notice and claim filing are critical for coverage. The analysis flags late notice, missed deadlines, and supports coverage determination.
        """,
        key_factors=[
            "Policy language",
            "Notice and claim dates",
            "Statutory requirements",
            "Compliance validation"
        ],
        primary_authority=[
            "Relevant insurance statutes",
            "Case law on notice and claim",
            "Restatement (Second) of Insurance Contracts"
        ],
        burden_holder="Insured",
        adversary_position="Insurer may deny coverage for late notice",
        counter_arguments=[
            "Notice was timely",
            "Policy language is ambiguous",
            "Statutory exceptions apply"
        ],
        resolution_strategy="Legal research and policy review",
        entity_scope="Insured and insurer",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Restatement (Second) of Insurance Contracts"
    ),
    DoctrineBlock(
        topic="event_causality_analysis",
        keywords=["event causality", "timeline", "legal causation", "proximate cause", "sequence"],
        conclusion_template="Event causality analysis determines whether a sequence of events establishes legal causation.",
        reasoning_framework="""
        Event causality analysis applies legal principles of causation to the timeline, determining whether a sequence of events establishes proximate cause for liability or relief. The framework analyzes factual and legal causation, intervening events, and dependency relationships. Case law and statutory rules are applied. The analysis supports liability determination and judicial review.
        """,
        key_factors=[
            "Sequence of events",
            "Legal principles of causation",
            "Intervening events",
            "Materiality to liability"
        ],
        primary_authority=[
            "Restatement (Second) of Torts § 431",
            "Case law on proximate cause",
            "Relevant statutes"
        ],
        burden_holder="Plaintiff",
        adversary_position="Defendant may assert intervening cause",
        counter_arguments=[
            "Intervening events break causation",
            "Sequence is insufficient for liability",
            "Causation is disputed"
        ],
        resolution_strategy="Legal research and evidentiary analysis",
        entity_scope="All parties",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Restatement (Second) of Torts § 431"
    ),
    DoctrineBlock(
        topic="event_dependency_graph_construction",
        keywords=["event dependency", "graph", "timeline", "legal process", "sequencing"],
        conclusion_template="Event dependency graph construction maps relationships between events for sequencing and analysis.",
        reasoning_framework="""
        Event dependency graph construction applies graph theory and legal principles to map relationships between events in the timeline. The framework identifies dependencies, sequences events, and analyzes impact on deadlines and case outcome. Legal rules and procedural requirements are applied. The analysis supports timeline reconstruction, critical path identification, and judicial review.
        """,
        key_factors=[
            "Identification of dependencies",
            "Sequencing of events",
            "Impact on deadlines",
            "Legal and procedural requirements"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Project Management Institute, PMBOK Guide",
            "Case law on event dependency"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may dispute dependency mapping",
        counter_arguments=[
            "Dependencies are incorrect",
            "Sequence does not reflect material events",
            "Legal requirements are unmet"
        ],
        resolution_strategy="Iterative validation and legal review",
        entity_scope="All timeline events",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_reconstruction_from_incomplete_data",
        keywords=["timeline reconstruction", "incomplete data", "legal process", "event inference", "gap analysis"],
        conclusion_template="Timeline reconstruction from incomplete data infers missing events and sequences for legal analysis.",
        reasoning_framework="""
        Timeline reconstruction from incomplete data applies inferential logic, legal heuristics, and corroboration to fill gaps and sequence events. The framework analyzes available evidence, applies procedural expectations, and documents all inferences. Legal rules governing materiality and evidentiary reliability are observed. The analysis supports judicial review and case management.
        """,
        key_factors=[
            "Available evidence",
            "Inferential logic",
            "Procedural expectations",
            "Documentation of inferences"
        ],
        primary_authority=[
            "Fed. R. Evid. 401",
            "Case law on evidentiary inference",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may challenge inferences",
        counter_arguments=[
            "Inferences are speculative",
            "Evidence is insufficient",
            "Procedural expectations are misapplied"
        ],
        resolution_strategy="Supplement with additional discovery and judicial review",
        entity_scope="All timeline events",
        confidence=0.83,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="procedural_event_classification",
        keywords=["procedural event", "classification", "timeline", "legal process", "event mapping"],
        conclusion_template="Procedural event classification distinguishes between procedural and substantive events in the timeline.",
        reasoning_framework="""
        Procedural event classification applies legal principles to distinguish between procedural and substantive events in the timeline. The framework analyzes event descriptions, legal rules, and case law. Classification supports timeline mapping, compliance analysis, and judicial review. The analysis documents classification rationale and addresses ambiguities.
        """,
        key_factors=[
            "Event description",
            "Legal rules for classification",
            "Case law",
            "Materiality to case outcome"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Case law on procedural classification",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may dispute classification",
        counter_arguments=[
            "Classification is ambiguous",
            "Event is misclassified",
            "Materiality is disputed"
        ],
        resolution_strategy="Legal research and iterative classification",
        entity_scope="All timeline events",
        confidence=0.82,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_audit_trail_documentation",
        keywords=["timeline", "audit trail", "documentation", "legal process", "event mapping"],
        conclusion_template="Timeline audit trail documentation ensures transparency and reliability of timeline reconstruction.",
        reasoning_framework="""
        Timeline audit trail documentation records all steps, decisions, and evidence used in timeline reconstruction. The framework applies legal requirements for transparency, evidentiary reliability, and judicial review. Documentation supports validation, dispute resolution, and compliance. The analysis addresses ambiguities and provides an audit trail for all inferences and decisions.
        """,
        key_factors=[
            "Documentation of steps and decisions",
            "Legal requirements for transparency",
            "Evidentiary reliability",
            "Audit trail completeness"
        ],
        primary_authority=[
            "Fed. R. Evid. 803(6)",
            "Case law on audit trail",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may challenge audit trail sufficiency",
        counter_arguments=[
            "Documentation is incomplete",
            "Audit trail is unreliable",
            "Transparency is lacking"
        ],
        resolution_strategy="Supplement documentation and judicial review",
        entity_scope="All timeline events",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_integrity_verification",
        keywords=["timeline", "integrity", "verification", "legal process", "event mapping"],
        conclusion_template="Timeline integrity verification validates accuracy and reliability of reconstructed timeline.",
        reasoning_framework="""
        Timeline integrity verification applies legal and technical methods to validate accuracy and reliability of the reconstructed timeline. The framework analyzes event sequencing, date normalization, and dependency mapping. Legal rules governing evidentiary reliability and procedural requirements are applied. The analysis supports judicial review and dispute resolution.
        """,
        key_factors=[
            "Accuracy of event sequencing",
            "Date normalization",
            "Dependency mapping",
            "Evidentiary reliability"
        ],
        primary_authority=[
            "Fed. R. Evid. 401",
            "Case law on timeline integrity",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may challenge integrity",
        counter_arguments=[
            "Timeline is inaccurate",
            "Reliability is disputed",
            "Sequencing is flawed"
        ],
        resolution_strategy="Supplement with additional evidence and legal review",
        entity_scope="All timeline events",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_materiality_analysis",
        keywords=["timeline", "materiality", "analysis", "legal process", "event mapping"],
        conclusion_template="Timeline materiality analysis determines which events are material to case outcome.",
        reasoning_framework="""
        Timeline materiality analysis applies legal principles to determine which events are material to case outcome. The framework analyzes event descriptions, legal requirements, and case law. Materiality supports evidentiary reliability, judicial review, and strategic planning. The analysis documents materiality rationale and addresses ambiguities.
        """,
        key_factors=[
            "Event description",
            "Legal requirements for materiality",
            "Case law",
            "Impact on case outcome"
        ],
        primary_authority=[
            "Fed. R. Evid. 401",
            "Case law on materiality",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may dispute materiality",
        counter_arguments=[
            "Event is immaterial",
            "Materiality is ambiguous",
            "Impact is disputed"
        ],
        resolution_strategy="Legal research and iterative materiality analysis",
        entity_scope="All timeline events",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_confidentiality_and_privilege",
        keywords=["timeline", "confidentiality", "privilege", "legal process", "event mapping"],
        conclusion_template="Timeline confidentiality and privilege analysis ensures compliance with legal requirements for protected information.",
        reasoning_framework="""
        Timeline confidentiality and privilege analysis applies legal requirements for protected information in timeline reconstruction. The framework analyzes event descriptions, privilege claims, and statutory rules. Legal requirements for confidentiality, privilege, and disclosure are applied. The analysis supports compliance, dispute resolution, and judicial review.
        """,
        key_factors=[
            "Event description",
            "Privilege claims",
            "Statutory requirements",
            "Compliance with confidentiality"
        ],
        primary_authority=[
            "Fed. R. Evid. 501",
            "Case law on privilege",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may challenge privilege claims",
        counter_arguments=[
            "Privilege is inapplicable",
            "Confidentiality is disputed",
            "Disclosure is required"
        ],
        resolution_strategy="Legal research and privilege review",
        entity_scope="All timeline events",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Fed. R. Evid. 501"
    ),
    DoctrineBlock(
        topic="timeline_event_categorization",
        keywords=["timeline", "event categorization", "legal process", "event mapping", "classification"],
        conclusion_template="Timeline event categorization organizes events by legal category for analysis and presentation.",
        reasoning_framework="""
        Timeline event categorization applies legal and technical methods to organize events by category (e.g., procedural, substantive, discovery). The framework analyzes event descriptions, legal requirements, and case law. Categorization supports analysis, presentation, and judicial review. The analysis documents categorization rationale and addresses ambiguities.
        """,
        key_factors=[
            "Event description",
            "Legal requirements for categorization",
            "Case law",
            "Impact on analysis and presentation"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Case law on event categorization",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may dispute categorization",
        counter_arguments=[
            "Categorization is ambiguous",
            "Event is miscategorized",
            "Impact is disputed"
        ],
        resolution_strategy="Legal research and iterative categorization",
        entity_scope="All timeline events",
        confidence=0.84,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_event_priority_analysis",
        keywords=["timeline", "event priority", "analysis", "legal process", "event mapping"],
        conclusion_template="Timeline event priority analysis determines which events require immediate attention or action.",
        reasoning_framework="""
        Timeline event priority analysis applies legal and procedural requirements to determine which events require immediate attention or action. The framework analyzes event descriptions, deadlines, and impact on case outcome. Priority supports compliance, risk management, and strategic planning. The analysis documents priority rationale and addresses ambiguities.
        """,
        key_factors=[
            "Event description",
            "Deadlines and impact",
            "Legal and procedural requirements",
            "Risk management"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Case law on event priority",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may dispute priority",
        counter_arguments=[
            "Priority is ambiguous",
            "Event is misprioritized",
            "Impact is disputed"
        ],
        resolution_strategy="Legal research and iterative priority analysis",
        entity_scope="All timeline events",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_event_risk_analysis",
        keywords=["timeline", "event risk", "analysis", "legal process", "event mapping"],
        conclusion_template="Timeline event risk analysis identifies events that pose risk to case outcome or compliance.",
        reasoning_framework="""
        Timeline event risk analysis applies legal and technical methods to identify events that pose risk to case outcome or compliance. The framework analyzes event descriptions, deadlines, and impact. Risk analysis supports strategic planning, compliance, and dispute resolution. The analysis documents risk rationale and addresses ambiguities.
        """,
        key_factors=[
            "Event description",
            "Deadlines and impact",
            "Legal and procedural requirements",
            "Risk management"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Case law on event risk",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may dispute risk assessment",
        counter_arguments=[
            "Risk is overstated",
            "Event is misidentified",
            "Impact is disputed"
        ],
        resolution_strategy="Legal research and iterative risk analysis",
        entity_scope="All timeline events",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_event_dependency_validation",
        keywords=["timeline", "event dependency", "validation", "legal process", "event mapping"],
        conclusion_template="Timeline event dependency validation ensures all dependencies are accurately mapped and sequenced.",
        reasoning_framework="""
        Timeline event dependency validation applies legal and technical methods to ensure all dependencies are accurately mapped and sequenced. The framework analyzes event descriptions, legal requirements, and case law. Validation supports timeline reconstruction, compliance, and judicial review. The analysis documents validation rationale and addresses ambiguities.
        """,
        key_factors=[
            "Event description",
            "Legal requirements for dependency",
            "Case law",
            "Impact on timeline reconstruction"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Case law on event dependency",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may dispute dependency mapping",
        counter_arguments=[
            "Dependencies are incorrect",
            "Event is misidentified",
            "Impact is disputed"
        ],
        resolution_strategy="Legal research and iterative dependency validation",
        entity_scope="All timeline events",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_event_sequence_validation",
        keywords=["timeline", "event sequence", "validation", "legal process", "event mapping"],
        conclusion_template="Timeline event sequence validation ensures all events are accurately sequenced for legal analysis.",
        reasoning_framework="""
        Timeline event sequence validation applies legal and technical methods to ensure all events are accurately sequenced for legal analysis. The framework analyzes event descriptions, legal requirements, and case law. Validation supports timeline reconstruction, compliance, and judicial review. The analysis documents validation rationale and addresses ambiguities.
        """,
        key_factors=[
            "Event description",
            "Legal requirements for sequencing",
            "Case law",
            "Impact on timeline reconstruction"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Case law on event sequencing",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline analyst",
        adversary_position="Opposing party may dispute sequence mapping",
        counter_arguments=[
            "Sequence is incorrect",
            "Event is misidentified",
            "Impact is disputed"
        ],
        resolution_strategy="Legal research and iterative sequence validation",
        entity_scope="All timeline events",
        confidence=0.86,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_event_evidence_corroboration",
        keywords=["timeline", "event evidence", "corroboration", "legal process", "event mapping"],
        conclusion_template="Timeline event evidence corroboration validates events with supporting documentary or testimonial evidence.",
        reasoning_framework="""
        Timeline event evidence corroboration applies legal and technical methods to validate events with supporting documentary or testimonial evidence. The framework analyzes event descriptions, evidence, and legal requirements. Corroboration supports timeline reconstruction, evidentiary reliability, and judicial review. The analysis documents corroboration rationale and addresses ambiguities.
        """,
        key_factors=[
            "Event description",
            "Supporting evidence",
            "Legal requirements for corroboration",
            "Impact on timeline reconstruction"
        ],
        primary_authority=[
            "Fed. R. Evid. 401",
            "Case law on evidence corroboration",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may dispute evidence sufficiency",
        counter_arguments=[
            "Evidence is insufficient",
            "Event is uncorroborated",
            "Impact is disputed"
        ],
        resolution_strategy="Supplement with additional evidence and legal review",
        entity_scope="All timeline events",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
    DoctrineBlock(
        topic="timeline_event_dispute_resolution",
        keywords=["timeline", "event dispute", "resolution", "legal process", "event mapping"],
        conclusion_template="Timeline event dispute resolution applies legal and procedural methods to resolve event disputes.",
        reasoning_framework="""
        Timeline event dispute resolution applies legal and procedural methods to resolve disputes over event identification, sequencing, or materiality. The framework analyzes event descriptions, legal requirements, and case law. Resolution supports timeline reconstruction, compliance, and judicial review. The analysis documents resolution rationale and addresses ambiguities.
        """,
        key_factors=[
            "Event description",
            "Legal requirements for dispute resolution",
            "Case law",
            "Impact on timeline reconstruction"
        ],
        primary_authority=[
            "Fed. R. Civ. P. 16",
            "Case law on dispute resolution",
            "Manual for Complex Litigation (4th ed.)"
        ],
        burden_holder="Timeline reconstructor",
        adversary_position="Opposing party may dispute resolution",
        counter_arguments=[
            "Resolution is inadequate",
            "Event is misidentified",
            "Impact is disputed"
        ],
        resolution_strategy="Legal research and iterative dispute resolution",
        entity_scope="All timeline events",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Manual for Complex Litigation"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
            continue
        if any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
            continue
        if keyword_lower in doctrine.reasoning_framework.lower():
            results.append(doctrine)
            continue
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]