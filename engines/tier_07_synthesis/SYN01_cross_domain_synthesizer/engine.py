#!/usr/bin/env python
"""SYN01 Cross-Domain Synthesizer Engine v1.0.0 - TIE-Grade Multi-Domain Integration"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

ENGINE_ID = "SYN01"
ENGINE_NAME = "Cross-Domain Synthesizer"
VERSION = "1.0.0"
PORT = 9161

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class DomainType(str, Enum):
    TAX = "TAX"
    LEGAL = "LEGAL"
    LANDMAN = "LANDMAN"
    REGULATORY = "REGULATORY"
    PROBATE = "PROBATE"
    ENTERPRISE = "ENTERPRISE"
    GEOSPATIAL = "GEOSPATIAL"
    INTELLIGENCE = "INTELLIGENCE"

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Multi-Domain Conflict Resolution",
        keywords=["conflict", "contradiction", "inconsistent", "domain clash", "authority hierarchy", "precedence"],
        conclusion_template=[
            "Cross-domain conflicts resolved using hierarchical authority matrix.",
            "Controlling authority: {primary_domain} per {authority_basis}.",
            "Subordinate domains harmonized through {resolution_method}."
        ],
        reasoning_framework="""When multiple domain engines produce conflicting findings:
1. Identify conflict type (factual, legal, procedural, interpretive)
2. Determine applicable authority hierarchy (statutory > regulatory > contractual > practice)
3. Assess temporal priority (later enactment controls unless retroactive prohibition)
4. Evaluate jurisdiction-specific rules (federal preemption, state law conflicts)
5. Weight confidence scores from each domain engine
6. Apply synthesis rules: highest authority + highest confidence + most recent + most specific
7. Document dissenting positions with materiality assessment
8. Flag unresolved conflicts requiring human review at DISCLOSURE confidence level""",
        key_factors=[
            "Authority source hierarchy per domain",
            "Temporal sequence of controlling rules",
            "Jurisdictional scope and preemption",
            "Confidence scores from source engines",
            "Materiality of conflict to overall conclusion",
            "Specificity vs. generality of conflicting rules",
            "Precedent for resolving similar cross-domain issues"
        ],
        primary_authority=[
            "Domain-specific statutes and regulations",
            "Inter-agency coordination agreements",
            "Judicial decisions on conflicts of law",
            "Professional practice standards for synthesis"
        ],
        burden_holder="Synthesizer must justify resolution methodology",
        adversary_position="Conflicts prove analysis unreliable, require disclaimer",
        counter_arguments=[
            "Conflicts are common in complex multi-domain scenarios",
            "Methodical resolution using authority hierarchy produces defensible synthesis",
            "Transparent documentation of conflicts and resolution enhances credibility",
            "Unresolved conflicts properly disclosed do not invalidate overall analysis",
            "Multiple domain checks improve accuracy vs. single-domain view"
        ],
        resolution_strategy="Apply authority hierarchy, document dissents, flag material unresolved conflicts",
        entity_scope="All entities with multi-domain regulatory exposure",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when conflicts resolved via documented methodology; DISCLOSURE when material conflicts unresolved",
        controlling_precedent="Restatement (Second) of Conflict of Laws principles adapted to regulatory domains"
    ),
    DoctrineBlock(
        topic="Weighted Confidence Aggregation",
        keywords=["confidence", "weighting", "aggregate", "combined probability", "uncertainty", "reliability"],
        conclusion_template=[
            "Aggregate confidence: {weighted_score} based on {num_sources} domain sources.",
            "Weighting methodology: {weight_basis}.",
            "Sensitivity analysis: +/- {variance_range} under alternative weighting."
        ],
        reasoning_framework="""Aggregate confidence from multiple domain engines:
1. Collect confidence scores from each contributing engine (0.0-1.0 scale)
2. Assign domain weights based on relevance to query (tax-heavy = tax engine weight 0.5, others 0.125)
3. Apply authority adjustment (statutory source +0.1, case law +0.05, practice -0.05)
4. Factor in recency (current year +0.05, 1-3 years 0.0, >3 years -0.05)
5. Calculate weighted average: sum(confidence * weight) / sum(weights)
6. Sensitivity test: recalculate with +/- 20% weight adjustments
7. If sensitivity variance > 0.15, downgrade to DISCLOSURE confidence tier
8. Document weighting rationale in audit trail""",
        key_factors=[
            "Number and diversity of contributing domain engines",
            "Relevance weighting per domain to specific query",
            "Authority level of sources cited by each engine",
            "Recency of controlling authorities",
            "Variance under sensitivity analysis",
            "Presence of dissenting domain conclusions",
            "Historical accuracy of each engine on similar queries"
        ],
        primary_authority=[
            "Statistical aggregation methodologies",
            "Expert elicitation and Delphi methods",
            "Bayesian evidence combination frameworks"
        ],
        burden_holder="Synthesizer must justify weighting scheme as reasonable",
        adversary_position="Arbitrary weighting manipulates outcome, lacks objective basis",
        counter_arguments=[
            "Weighting reflects materiality and relevance, not manipulation",
            "Sensitivity analysis demonstrates robustness across reasonable weight variations",
            "Unweighted average would give irrelevant domains undue influence",
            "Documented methodology enables replication and critique",
            "Domain experts routinely weight evidence by relevance and reliability"
        ],
        resolution_strategy="Document weighting rationale, run sensitivity analysis, disclose if high variance",
        entity_scope="All multi-domain analyses requiring aggregated confidence",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE if sensitivity variance < 0.15; DISCLOSURE if >= 0.15",
        controlling_precedent="FDA guidance on multi-study evidence synthesis"
    ),
    DoctrineBlock(
        topic="Cross-Reference Validation",
        keywords=["cross-reference", "citation", "validation", "verify", "fact-check", "consistency"],
        conclusion_template=[
            "Cross-reference validation: {pass_rate}% of {total_refs} references verified.",
            "Failed validations: {failed_count} ({failure_summary}).",
            "Validation methodology: {validation_method}."
        ],
        reasoning_framework="""Validate factual assertions across domain engines:
1. Extract factual claims from each engine response (dates, amounts, parties, statutes, case names)
2. Cross-reference claims against other domain engines and external sources
3. Flag mismatches (same fact, different values reported by different engines)
4. Classify mismatches: immaterial (<5% variance on amounts), material (conflicting legal conclusions)
5. Investigate material mismatches: re-query engines, check source documents, escalate to human
6. Calculate validation pass rate: verified facts / total factual claims
7. If pass rate < 90%, downgrade overall confidence to DISCLOSURE
8. Maintain validation ledger in audit trail""",
        key_factors=[
            "Number of factual claims requiring validation",
            "Availability of independent validation sources",
            "Materiality threshold for discrepancies",
            "Pass rate percentage across all cross-references",
            "Nature of failed validations (typographical vs. substantive)",
            "Consistency of engine responses on repeated queries",
            "External data source reliability"
        ],
        primary_authority=[
            "Accounting standards for factual verification",
            "Legal cite-checking standards (Bluebook)",
            "Audit trail documentation requirements"
        ],
        burden_holder="Synthesizer must validate material facts before relying on them",
        adversary_position="Unvalidated facts undermine entire analysis credibility",
        counter_arguments=[
            "Comprehensive validation of all facts is resource-prohibitive",
            "Materiality-based validation focuses effort on high-impact claims",
            "Validation pass rate >90% demonstrates reliable source engines",
            "Transparent disclosure of validation results enables informed reliance",
            "Failed validations on immaterial details do not invalidate core conclusions"
        ],
        resolution_strategy="Validate material facts, disclose validation pass rate, investigate failures",
        entity_scope="All synthesis reports containing factual assertions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE if pass rate >= 90%; DISCLOSURE if < 90%",
        controlling_precedent="PCAOB auditing standards on evidence corroboration"
    ),
    DoctrineBlock(
        topic="Hierarchical Summarization",
        keywords=["summary", "executive", "hierarchy", "rollup", "abstraction", "digest"],
        conclusion_template=[
            "Executive summary: {one_sentence_conclusion}.",
            "Key findings: {top_3_findings}.",
            "Detailed analysis available at {detail_level} levels of granularity."
        ],
        reasoning_framework="""Generate hierarchical summaries for stakeholder consumption:
1. Identify target audience (executive, manager, analyst, auditor)
2. Define abstraction levels: L1=one sentence, L2=paragraph, L3=page, L4=full report
3. Extract salient points: material risks, financial impacts, compliance gaps, recommendations
4. Rank by materiality: dollar threshold, legal exposure, operational disruption
5. Compose L1: single sentence capturing overall conclusion and primary risk
6. Compose L2: 3-5 sentences adding key findings and top recommendation
7. Compose L3: 1-page summary with tables for quantitative findings
8. Link each level to next-lower detail level for drill-down navigation""",
        key_factors=[
            "Target audience role and decision authority",
            "Materiality thresholds for inclusion at each level",
            "Complexity of underlying multi-domain analysis",
            "Time constraints of executive readers",
            "Need for drill-down to supporting detail",
            "Regulatory disclosure requirements",
            "Consistency of terminology across hierarchy levels"
        ],
        primary_authority=[
            "SEC plain English guidance for executive summaries",
            "Government Accountability Office report writing standards",
            "ISO 30414 human capital reporting hierarchy"
        ],
        burden_holder="Synthesizer must not omit material information at executive levels",
        adversary_position="Oversimplified summaries conceal critical risks and uncertainties",
        counter_arguments=[
            "Hierarchical design allows readers to drill down to detail as needed",
            "Materiality-based filtering focuses executive attention on decision-critical items",
            "Standardized structure improves comprehension and comparability",
            "Full detail always accessible at L4 for comprehensive review",
            "Executive summaries are standard practice in professional reporting"
        ],
        resolution_strategy="Multi-level summaries with explicit materiality thresholds and drill-down links",
        entity_scope="All synthesis reports for management or regulatory use",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when material items disclosed at appropriate hierarchy level",
        controlling_precedent="SEC rules on layered disclosure in registration statements"
    ),
    DoctrineBlock(
        topic="Executive Report Generation",
        keywords=["executive", "report", "dashboard", "metrics", "KPI", "visualization"],
        conclusion_template=[
            "Executive report generated: {page_count} pages, {chart_count} visualizations.",
            "Key metrics: {metric_summary}.",
            "Risk score: {risk_score}/100 ({risk_level})."
        ],
        reasoning_framework="""Generate executive-level synthesis reports:
1. Aggregate findings from all queried domain engines
2. Calculate composite risk score (weighted average of domain-specific risk scores, 0-100 scale)
3. Identify top 5 risks by materiality (financial impact * probability)
4. Generate trend charts (time series if historical data available)
5. Create comparison tables (entity vs. peers, current vs. prior period)
6. Compose narrative: situation, complication, resolution (SCR structure)
7. Include action items with owner, deadline, and success criteria
8. Format as PDF with branding, TOC, executive summary on page 1""",
        key_factors=[
            "Scope of domains included in synthesis",
            "Risk scoring methodology and calibration",
            "Availability of comparative and historical data",
            "Stakeholder-specific presentation preferences",
            "Regulatory or contractual reporting requirements",
            "Visualization best practices for data types",
            "Narrative clarity and actionability"
        ],
        primary_authority=[
            "COSO Enterprise Risk Management framework",
            "Balanced Scorecard methodology",
            "Data visualization standards (Tufte, Few)"
        ],
        burden_holder="Report must present accurate, material, and actionable synthesis",
        adversary_position="Automated reports lack nuanced judgment of human expert",
        counter_arguments=[
            "Synthesis engine applies documented rules consistently across analyses",
            "Human oversight validates high-risk findings before report issuance",
            "Standardized format improves comparability and trend analysis",
            "Automation enables more frequent reporting vs. manual processes",
            "Expert rules encoded in doctrine cache reflect professional judgment"
        ],
        resolution_strategy="Automated generation with human validation of material findings",
        entity_scope="All entities requiring periodic executive-level synthesis reports",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with human validation; AGGRESSIVE if fully automated",
        controlling_precedent="SEC MD&A requirements for management discussion and analysis"
    ),
    DoctrineBlock(
        topic="Risk Matrix Construction",
        keywords=["risk matrix", "probability", "impact", "heat map", "risk scoring", "prioritization"],
        conclusion_template=[
            "Risk matrix: {high_risks} high, {medium_risks} medium, {low_risks} low risks identified.",
            "Highest priority: {top_risk_description} (impact={impact}, prob={probability}).",
            "Risk appetite threshold: {threshold_description}."
        ],
        reasoning_framework="""Construct multi-domain risk matrix:
1. Collect risk items from all domain engines (tax exposure, legal liability, operational disruption, compliance gaps)
2. Quantify impact for each risk: financial (dollars), operational (days disruption), reputational (severity scale)
3. Assess probability: percentage likelihood or ordinal scale (rare, possible, likely, certain)
4. Normalize to common scale (1-5 for both impact and probability)
5. Calculate risk score: impact * probability (1-25 scale)
6. Classify: Low (1-6), Medium (7-15), High (16-25)
7. Plot on 5x5 heat map matrix
8. Prioritize mitigation: High risks first, then Medium, defer Low unless quick wins""",
        key_factors=[
            "Completeness of risk identification across domains",
            "Accuracy of impact quantification (financial models, historical data)",
            "Reliability of probability assessment (actuarial data, expert judgment)",
            "Consistency of scaling across disparate risk types",
            "Risk appetite thresholds set by management",
            "Cost-benefit of mitigation actions",
            "Interdependencies among risks (cascading effects)"
        ],
        primary_authority=[
            "ISO 31000 Risk Management standard",
            "COSO ERM framework risk assessment guidance",
            "Project Management Institute risk matrix methodology"
        ],
        burden_holder="Risk assessment must use reasonable assumptions and disclose uncertainties",
        adversary_position="Oversimplified matrix obscures complexity and uncertainty in risk assessment",
        counter_arguments=[
            "Standardized matrix enables consistent comparison and prioritization",
            "Detailed risk descriptions and assumptions documented in supporting detail",
            "Sensitivity analysis on probability and impact inputs tests robustness",
            "Matrix is decision tool, not substitute for professional judgment",
            "Widely adopted methodology across industries and professions"
        ],
        resolution_strategy="Use standard matrix with transparent assumptions and sensitivity analysis",
        entity_scope="All entities with multi-domain risk exposure",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with documented assumptions; AGGRESSIVE if assumptions untested",
        controlling_precedent="ISO 31000:2018 risk assessment process"
    ),
    DoctrineBlock(
        topic="Temporal Analysis Across Domains",
        keywords=["temporal", "timeline", "chronology", "sequence", "historical", "trend"],
        conclusion_template=[
            "Temporal analysis: {event_count} events across {timespan} timeline.",
            "Critical sequence: {sequence_description}.",
            "Trend direction: {trend_summary}."
        ],
        reasoning_framework="""Analyze temporal patterns across domains:
1. Extract dated events from all domain engine responses (filings, transactions, regulatory changes, litigation)
2. Construct unified timeline with event type, domain, materiality tag
3. Identify causal sequences (regulatory change -> operational adjustment -> financial impact)
4. Detect temporal gaps (missing expected events, unexplained delays)
5. Analyze trends (increasing regulatory scrutiny, declining compliance scores)
6. Assess statute of limitations and deadline compliance
7. Project future events based on regulatory calendars and contractual terms
8. Highlight temporal conflicts (retroactive rule changes, statute of limitations expired)""",
        key_factors=[
            "Completeness of event capture across all domains",
            "Accuracy of event dating (filing date vs. effective date vs. discovery date)",
            "Identification of causal vs. coincidental temporal relationships",
            "Materiality of detected trends and patterns",
            "Deadline tracking for compliance and statute of limitations",
            "Retroactivity analysis for regulatory changes",
            "Projection reliability for future events"
        ],
        primary_authority=[
            "Statute of limitations rules per jurisdiction",
            "Regulatory effective date rules",
            "Contract law on timing and deadlines"
        ],
        burden_holder="Temporal analysis must use accurate dates and disclose gaps",
        adversary_position="Temporal correlations do not prove causation, analysis overstates connections",
        counter_arguments=[
            "Causal inference uses established legal and regulatory frameworks, not mere correlation",
            "Temporal sequence is necessary but not sufficient; analysis considers other evidence",
            "Trend identification helps predict regulatory and operational risks",
            "Deadline tracking prevents compliance failures and statute of limitations bars",
            "Transparent methodology allows critique of causal claims"
        ],
        resolution_strategy="Document temporal relationships, distinguish causation from correlation, track deadlines",
        entity_scope="All entities with time-sensitive compliance or litigation exposure",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE for deadline tracking; AGGRESSIVE for causal claims without corroboration",
        controlling_precedent="Civil procedure rules on statute of limitations computation"
    ),
    DoctrineBlock(
        topic="Jurisdiction Conflict Detection",
        keywords=["jurisdiction", "conflict", "preemption", "federal", "state", "local", "choice of law"],
        conclusion_template=[
            "Jurisdictional analysis: {jurisdiction_count} jurisdictions implicated.",
            "Controlling jurisdiction: {primary_jurisdiction} per {conflict_rule}.",
            "Preemption issues: {preemption_summary}."
        ],
        reasoning_framework="""Resolve multi-jurisdictional conflicts:
1. Identify all implicated jurisdictions (federal, state, local, tribal, international)
2. Determine choice of law rules (contract choice of law clause, Restatement, lex loci)
3. Analyze federal preemption (express, implied, field, conflict)
4. Assess state law conflicts (full faith and credit, comity, public policy exception)
5. Evaluate forum selection clauses and arbitration agreements
6. Identify unresolved conflicts requiring legal opinion or litigation
7. Document conflict resolution methodology in audit trail
8. Flag HIGH_RISK if material jurisdictional uncertainty exists""",
        key_factors=[
            "Number and diversity of jurisdictions involved",
            "Presence of federal vs. state law conflicts",
            "Choice of law clauses in governing contracts",
            "Public policy exceptions to conflict rules",
            "Forum selection and arbitration clauses",
            "International treaty obligations (if applicable)",
            "Historical resolution of similar conflicts in jurisdiction"
        ],
        primary_authority=[
            "U.S. Constitution Supremacy Clause (federal preemption)",
            "Restatement (Second) of Conflict of Laws",
            "Uniform Commercial Code choice of law rules",
            "International treaties and conventions (e.g., Hague, Vienna)"
        ],
        burden_holder="Analysis must identify controlling jurisdiction or disclose uncertainty",
        adversary_position="Jurisdictional conflicts create insurmountable legal uncertainty",
        counter_arguments=[
            "Conflict of law rules provide established methodology for resolution",
            "Choice of law clauses often resolve ambiguity in commercial contexts",
            "Preemption analysis follows clear Supreme Court framework",
            "Disclosure of unresolved conflicts allows informed legal strategy",
            "Multi-jurisdictional analysis is standard in complex transactions"
        ],
        resolution_strategy="Apply conflict of law rules, analyze preemption, disclose material uncertainties",
        entity_scope="All entities operating in multiple jurisdictions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE if conflict rules clearly apply; DISCLOSURE if material uncertainty; HIGH_RISK if litigation likely",
        controlling_precedent="Erie Railroad Co. v. Tompkins (federal vs. state law in diversity jurisdiction)"
    ),
    DoctrineBlock(
        topic="Authority Hierarchy Resolution",
        keywords=["authority", "hierarchy", "precedent", "controlling", "persuasive", "primary", "secondary"],
        conclusion_template=[
            "Authority hierarchy: {authority_count} sources analyzed.",
            "Controlling authority: {primary_authority}.",
            "Persuasive sources: {secondary_count} considered."
        ],
        reasoning_framework="""Resolve conflicts using authority hierarchy:
1. Classify sources: Constitution > Statute > Regulation > Case Law > Agency Guidance > Secondary Sources
2. Within statutes: Federal > State > Local (subject to preemption analysis)
3. Within case law: Binding precedent (same jurisdiction, higher court) > Persuasive (other jurisdiction, same level)
4. Temporal rule: Later enactment controls unless retroactivity prohibited
5. Specificity rule: Specific statute controls over general statute
6. Weight agency interpretations: Chevron deference (if applicable), Skidmore weight
7. Resolve conflicts: Highest authority + most recent + most specific
8. Document dissenting authorities and rationale for not following""",
        key_factors=[
            "Level of authority (constitutional, statutory, regulatory, judicial)",
            "Jurisdiction and binding vs. persuasive effect",
            "Temporal sequence and retroactivity rules",
            "Specificity vs. generality of rule",
            "Agency deference framework (Chevron, Auer, Skidmore)",
            "Precedential value (published vs. unpublished, en banc vs. panel)",
            "Contrary authority and weight of dissent"
        ],
        primary_authority=[
            "U.S. Constitution and state constitutions",
            "Federal and state statutes",
            "Code of Federal Regulations and state regulations",
            "Supreme Court and circuit court precedents"
        ],
        burden_holder="Analysis must follow controlling authority or justify departure",
        adversary_position="Cherry-picking favorable authority while ignoring contrary precedent",
        counter_arguments=[
            "Authority hierarchy is established legal methodology, not manipulation",
            "Contrary authority documented and distinguished, not ignored",
            "Binding precedent must be followed regardless of outcome preference",
            "Persuasive authority considered but does not override controlling law",
            "Transparent methodology enables critique and validation"
        ],
        resolution_strategy="Apply hierarchy rules consistently, document contrary authority, justify departures",
        entity_scope="All legal and regulatory analyses",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when following clear hierarchy; DISCLOSURE if authority conflicts unresolved",
        controlling_precedent="Chevron U.S.A., Inc. v. Natural Resources Defense Council (agency deference)"
    ),
    DoctrineBlock(
        topic="Materiality Thresholds",
        keywords=["materiality", "threshold", "significance", "de minimis", "substantial", "reasonable"],
        conclusion_template=[
            "Materiality assessment: {material_count} material items identified.",
            "Threshold applied: {threshold_description}.",
            "Immaterial items: {immaterial_count} excluded from executive summary."
        ],
        reasoning_framework="""Apply materiality thresholds to filter synthesis output:
1. Define materiality for context: financial (% of revenue/assets), legal (litigation risk), operational (service disruption)
2. Quantitative thresholds: Financial >5% revenue, >2% assets; Tax >$100K exposure; Legal >$500K potential liability
3. Qualitative factors: Reputational harm, regulatory scrutiny, strategic importance, precedent-setting
4. Aggregate de minimis items: Items below threshold reported in summary if aggregate is material
5. Disclose threshold methodology to enable reader assessment
6. Separate material items (executive summary) from immaterial (detailed appendix)
7. Flag items near threshold for management judgment
8. Document materiality determinations in audit trail""",
        key_factors=[
            "Context-specific materiality definition (financial, legal, operational)",
            "Quantitative thresholds calibrated to entity size and risk profile",
            "Qualitative factors beyond pure dollar amounts",
            "Aggregation of individually immaterial items",
            "Consistency with prior period and peer entity thresholds",
            "Regulatory or contractual materiality definitions",
            "Stakeholder expectations and disclosure norms"
        ],
        primary_authority=[
            "SEC materiality definition (TSC Industries, Basic Inc.)",
            "FASB accounting materiality guidance",
            "Audit materiality standards (PCAOB, ISA)"
        ],
        burden_holder="Materiality determination must be reasonable and consistently applied",
        adversary_position="Arbitrary thresholds conceal significant issues by labeling them immaterial",
        counter_arguments=[
            "Thresholds based on professional standards and entity-specific factors",
            "Qualitative factors supplement quantitative thresholds",
            "Immaterial items still documented, just not in executive summary",
            "Aggregation of de minimis items prevents concealment",
            "Consistent methodology enables comparability across periods"
        ],
        resolution_strategy="Apply professional standards, document methodology, aggregate de minimis items",
        entity_scope="All synthesis reports requiring materiality filtering",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when thresholds follow professional standards and entity context",
        controlling_precedent="TSC Industries, Inc. v. Northway, Inc. (SEC materiality standard)"
    ),
    DoctrineBlock(
        topic="Stakeholder-Specific Formatting",
        keywords=["stakeholder", "audience", "formatting", "presentation", "customization", "role-based"],
        conclusion_template=[
            "Report formatted for {stakeholder_role} audience.",
            "Presentation style: {format_description}.",
            "Customization: {customization_summary}."
        ],
        reasoning_framework="""Tailor synthesis output to stakeholder role:
1. Identify stakeholder: Executive, Board, Auditor, Regulator, Analyst, Counsel
2. Define presentation preferences: Executives want one-page summaries; Auditors want full documentation
3. Adjust detail level: Executive (L1-L2), Manager (L2-L3), Analyst (L3-L4), Auditor (L4 full detail)
4. Customize visualizations: Executives prefer dashboards; Analysts want raw data tables
5. Terminology calibration: Executives avoid jargon; Counsel use legal terms of art
6. Narrative vs. data: Executives want narrative; Auditors want evidence trails
7. Action orientation: Executives need decisions; Analysts need analysis
8. Format output: PDF for executives, Excel for analysts, JSON for systems""",
        key_factors=[
            "Stakeholder role and decision authority",
            "Time constraints and attention span",
            "Technical sophistication and domain expertise",
            "Regulatory or contractual reporting requirements",
            "Presentation medium (email, dashboard, formal report)",
            "Frequency of reporting (real-time, weekly, quarterly, annual)",
            "Precedent and stakeholder feedback on prior reports"
        ],
        primary_authority=[
            "SEC plain English disclosure rules",
            "PCAOB audit report formatting standards",
            "Government Accountability Office report design guidance"
        ],
        burden_holder="Report must convey material information appropriate to stakeholder needs",
        adversary_position="Customization enables selective disclosure and concealment of unfavorable information",
        counter_arguments=[
            "All material information disclosed, just formatted for audience comprehension",
            "Full detail always available in L4 reports for comprehensive review",
            "Stakeholder-specific formatting improves decision-making efficiency",
            "Regulatory requirements met regardless of internal presentation style",
            "Customization is standard practice in professional reporting"
        ],
        resolution_strategy="Tailor presentation to audience while maintaining comprehensive documentation",
        entity_scope="All multi-stakeholder reporting contexts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE when material information disclosed to all stakeholders at appropriate detail level",
        controlling_precedent="SEC rules on layered disclosure and plain English communication"
    ),
    DoctrineBlock(
        topic="Sub-Query Routing to Specialized Engines",
        keywords=["routing", "delegation", "specialization", "domain engine", "orchestration", "dispatch"],
        conclusion_template=[
            "Sub-queries routed to {engine_count} specialized engines.",
            "Routing logic: {routing_description}.",
            "Aggregated {response_count} responses into unified synthesis."
        ],
        reasoning_framework="""Route sub-queries to appropriate domain engines:
1. Parse incoming query to identify domain components (tax, legal, landman, regulatory)
2. Map query components to available engines: Tax->TIE, Legal->LIE, Landman->LMIE, Regulatory->RIE
3. Generate domain-specific sub-queries with context preservation
4. Dispatch sub-queries to engines via HTTP API (async parallel where independent)
5. Collect responses with timeout handling (30s per engine, 90s total)
6. Parse and normalize responses (extract facts, conclusions, confidence, authorities)
7. Synthesize cross-domain findings (conflict resolution, weighting, validation)
8. Generate unified response with audit trail of sub-query routing""",
        key_factors=[
            "Accuracy of domain classification from query text",
            "Availability and health of target domain engines",
            "Timeout and retry logic for engine failures",
            "Context preservation in sub-query generation",
            "Response normalization across heterogeneous engine APIs",
            "Conflict resolution when engines produce inconsistent findings",
            "Performance optimization (parallel dispatch, caching)"
        ],
        primary_authority=[
            "Service-oriented architecture design patterns",
            "API orchestration best practices",
            "Microservices communication standards"
        ],
        burden_holder="Routing logic must select appropriate engines and preserve query intent",
        adversary_position="Automated routing misclassifies queries, sends to wrong engines, produces garbage synthesis",
        counter_arguments=[
            "Domain classification uses NLP and keyword matching with high accuracy",
            "Engine health checks prevent routing to failed services",
            "Timeout and fallback logic ensures graceful degradation",
            "Sub-query context includes original query to prevent loss of intent",
            "Human-in-the-loop validation for high-stakes queries",
            "Audit trail enables debugging and improvement of routing logic"
        ],
        resolution_strategy="Robust routing with health checks, timeouts, and audit trails; human validation for critical queries",
        entity_scope="All synthesis queries requiring multi-domain analysis",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with robust routing and validation; AGGRESSIVE if fully automated without validation",
        controlling_precedent="Industry standards for API gateway and service mesh architectures"
    ),
    DoctrineBlock(
        topic="Cross-Domain Risk Aggregation",
        keywords=["risk aggregation", "combined risk", "portfolio risk", "correlation", "diversification"],
        conclusion_template=[
            "Aggregate risk score: {total_risk}/100.",
            "Domain contributions: {domain_breakdown}.",
            "Correlation effects: {correlation_summary}."
        ],
        reasoning_framework="""Aggregate risks across domains accounting for correlations:
1. Collect risk scores from each domain engine (0-100 scale)
2. Assess correlation between domain risks: Tax and legal often correlated; Landman and geospatial independent
3. Apply correlation matrix: Perfect correlation (no diversification), zero correlation (risks additive), negative (offset)
4. Calculate aggregate risk: sqrt(sum(risk_i^2 + 2*rho_ij*risk_i*risk_j)) for all pairs i,j
5. Normalize to 0-100 scale
6. Sensitivity test: recalculate with +/- 20% correlation assumptions
7. If high sensitivity, disclose uncertainty and correlation assumptions
8. Document risk aggregation methodology in audit trail""",
        key_factors=[
            "Number and diversity of domain risks",
            "Correlation estimates between domain risks",
            "Reliability of correlation estimates (historical data, expert judgment)",
            "Sensitivity of aggregate risk to correlation assumptions",
            "Diversification benefits from uncorrelated risks",
            "Common mode failures (correlated risks from single root cause)",
            "Tail risk and extreme events (correlations increase in crises)"
        ],
        primary_authority=[
            "Portfolio theory (Markowitz diversification)",
            "Basel III risk aggregation standards",
            "Actuarial credibility theory"
        ],
        burden_holder="Risk aggregation must use reasonable correlation assumptions and disclose uncertainties",
        adversary_position="Correlation assumptions are speculative and manipulated to produce desired risk score",
        counter_arguments=[
            "Correlation estimates based on historical data and expert judgment",
            "Sensitivity analysis demonstrates robustness across reasonable correlation ranges",
            "Conservative assumptions (high correlations) produce higher aggregate risk, not lower",
            "Transparent methodology enables critique and validation",
            "Risk aggregation is standard practice in financial and actuarial analysis"
        ],
        resolution_strategy="Use evidence-based correlations, run sensitivity analysis, disclose assumptions",
        entity_scope="All entities with multi-domain risk portfolios",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with documented correlations and sensitivity analysis; DISCLOSURE if high sensitivity",
        controlling_precedent="Basel III Pillar 3 risk aggregation disclosures"
    ),
    DoctrineBlock(
        topic="Conflict of Interest Detection",
        keywords=["conflict of interest", "bias", "independence", "related party", "self-dealing"],
        conclusion_template=[
            "Conflict of interest scan: {conflict_count} potential conflicts identified.",
            "Material conflicts: {material_conflicts}.",
            "Mitigation: {mitigation_summary}."
        ],
        reasoning_framework="""Detect and disclose conflicts of interest in synthesis:
1. Scan all domain engine responses for related party transactions, self-dealing, bias indicators
2. Cross-reference parties across domains (tax entity = legal party = landman owner)
3. Identify conflicts: Same party on both sides of transaction, advisor benefiting from own advice, undisclosed relationships
4. Assess materiality: Financial magnitude, legal enforceability, reputational harm
5. Evaluate disclosure: Were conflicts disclosed by source engines? Are they material to synthesis conclusion?
6. Recommend mitigation: Independent review, arms-length transaction terms, disclosure in report
7. Flag HIGH_RISK if material undisclosed conflicts detected
8. Document conflict analysis in audit trail""",
        key_factors=[
            "Completeness of party identification across domains",
            "Accuracy of related party detection (name variations, corporate structures)",
            "Materiality of identified conflicts",
            "Adequacy of disclosure by source engines",
            "Availability of mitigation measures (independence, disclosure)",
            "Legal and regulatory conflict of interest rules",
            "Reputational and ethical considerations"
        ],
        primary_authority=[
            "SEC related party transaction rules",
            "Sarbanes-Oxley conflict of interest provisions",
            "Professional ethics rules (ABA Model Rules, AICPA Code)"
        ],
        burden_holder="Analysis must identify and disclose material conflicts of interest",
        adversary_position="Undisclosed conflicts invalidate analysis and create liability",
        counter_arguments=[
            "Comprehensive scanning across all domain engines maximizes conflict detection",
            "Materiality threshold focuses disclosure on significant conflicts",
            "Mitigation recommendations address conflicts rather than concealing them",
            "Transparent conflict analysis enhances credibility",
            "Professional standards require conflict identification and disclosure"
        ],
        resolution_strategy="Scan for conflicts, assess materiality, disclose and mitigate material conflicts",
        entity_scope="All entities subject to conflict of interest rules (public companies, fiduciaries, professionals)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with comprehensive conflict scanning and disclosure; HIGH_RISK if material conflicts undisclosed",
        controlling_precedent="SEC Regulation S-K Item 404 (related party transactions)"
    ),
    DoctrineBlock(
        topic="Regulatory Deadline Tracking",
        keywords=["deadline", "due date", "filing", "compliance", "calendar", "statute of limitations"],
        conclusion_template=[
            "Deadline tracking: {upcoming_count} deadlines within {timeframe}.",
            "Critical deadlines: {critical_deadlines}.",
            "Overdue items: {overdue_count}."
        ],
        reasoning_framework="""Track regulatory and contractual deadlines across domains:
1. Extract deadline information from all domain engine responses (tax filing dates, legal SOL, regulatory reporting)
2. Normalize to common calendar format (date, time zone, jurisdiction)
3. Classify by criticality: Critical (SOL, regulatory), Important (contractual), Routine (internal)
4. Calculate lead time: Days until deadline, buffer for preparation
5. Identify dependencies: Task B cannot start until Task A complete
6. Generate alerts: 90 days, 30 days, 7 days, 1 day before deadline
7. Track completion status: Pending, In Progress, Complete, Overdue
8. Escalate overdue items to HIGH_RISK and notify management""",
        key_factors=[
            "Completeness of deadline extraction across all domains",
            "Accuracy of deadline dates (accounting for holidays, extensions, tolling)",
            "Criticality classification (SOL vs. internal milestones)",
            "Lead time requirements for preparation and review",
            "Dependency tracking for multi-step processes",
            "Alert timing and escalation procedures",
            "Completion tracking and overdue item management"
        ],
        primary_authority=[
            "Civil procedure rules on statute of limitations",
            "Regulatory filing deadline rules (SEC, IRS, state agencies)",
            "Contract law on time is of the essence clauses"
        ],
        burden_holder="Deadline tracking must be comprehensive and timely",
        adversary_position="Missed deadlines due to inadequate tracking create liability and compliance failures",
        counter_arguments=[
            "Multi-domain extraction maximizes deadline capture",
            "Automated alerts provide advance notice for preparation",
            "Criticality classification focuses attention on high-stakes deadlines",
            "Dependency tracking prevents process bottlenecks",
            "Overdue escalation ensures management awareness and corrective action"
        ],
        resolution_strategy="Comprehensive extraction, automated alerts, criticality-based escalation",
        entity_scope="All entities with regulatory, contractual, or litigation deadlines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with comprehensive tracking and timely alerts",
        controlling_precedent="Missed statute of limitations as legal malpractice"
    ),
    DoctrineBlock(
        topic="Natural Language Query Understanding",
        keywords=["NLP", "query parsing", "intent", "entity extraction", "disambiguation"],
        conclusion_template=[
            "Query understanding: {intent_description}.",
            "Entities identified: {entity_count} ({entity_list}).",
            "Disambiguation: {disambiguation_summary}."
        ],
        reasoning_framework="""Parse natural language queries for synthesis:
1. Tokenize query text and extract key terms
2. Identify named entities (companies, people, statutes, jurisdictions, dates)
3. Classify query intent (risk assessment, compliance check, transaction analysis, reporting)
4. Disambiguate ambiguous terms (multiple entities with same name, acronyms, pronouns)
5. Map entities to domain engines (tax entity -> TIE, legal party -> LIE)
6. Generate structured query parameters from unstructured text
7. Validate entity resolution (confirm unique identification)
8. If disambiguation fails, request clarification from user""",
        key_factors=[
            "Accuracy of entity extraction (names, dates, amounts, statutes)",
            "Intent classification reliability (training data, model performance)",
            "Disambiguation effectiveness (knowledge graph, context clues)",
            "Handling of ambiguous or incomplete queries",
            "Robustness to typos, abbreviations, informal language",
            "Multilingual support if applicable",
            "Validation of extracted entities against known databases"
        ],
        primary_authority=[
            "Natural language processing literature",
            "Named entity recognition standards",
            "Semantic web and knowledge graph methodologies"
        ],
        burden_holder="Query understanding must accurately capture user intent",
        adversary_position="NLP errors produce incorrect entity mappings and irrelevant synthesis",
        counter_arguments=[
            "State-of-art NLP models achieve high accuracy on entity extraction",
            "Disambiguation uses knowledge graphs and context for resolution",
            "Failed disambiguation triggers user clarification request, not incorrect assumption",
            "Structured query validation prevents garbage-in-garbage-out",
            "Continuous improvement from user feedback and error correction"
        ],
        resolution_strategy="Use robust NLP, disambiguate with knowledge graphs, request clarification when uncertain",
        entity_scope="All natural language synthesis queries",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with high entity extraction accuracy; DISCLOSURE if disambiguation uncertain",
        controlling_precedent="Industry standards for NLP in legal and financial applications"
    ),
    DoctrineBlock(
        topic="Audit Trail and Provenance Tracking",
        keywords=["audit trail", "provenance", "lineage", "traceability", "transparency", "reproducibility"],
        conclusion_template=[
            "Audit trail: {event_count} events logged.",
            "Provenance: {source_count} sources, {engine_count} engines queried.",
            "Reproducibility: SHA-256 hash {hash_value}."
        ],
        reasoning_framework="""Maintain comprehensive audit trail for synthesis:
1. Log all synthesis events: Query received, engines queried, responses received, conflicts detected, resolutions applied
2. Capture provenance: Source documents, engine versions, doctrine cache versions, timestamps
3. Record decision points: Weighting schemes, materiality thresholds, conflict resolutions, confidence downgrades
4. Link findings to sources: Each factual assertion traceable to source engine and underlying document
5. Generate SHA-256 hash of synthesis parameters for reproducibility
6. Store audit trail in append-only log (JSONL format)
7. Enable audit trail export for external review
8. Retain audit trails per retention policy (7 years for tax, indefinitely for litigation)""",
        key_factors=[
            "Completeness of event logging (all synthesis steps captured)",
            "Granularity of provenance (document-level vs. page-level vs. clause-level)",
            "Traceability of findings to sources (citation accuracy)",
            "Reproducibility via deterministic hashing",
            "Retention policy compliance (regulatory, contractual, best practice)",
            "Audit trail accessibility for internal and external review",
            "Performance impact of comprehensive logging"
        ],
        primary_authority=[
            "PCAOB audit documentation requirements",
            "SEC record retention rules",
            "Federal Rules of Civil Procedure on ESI preservation"
        ],
        burden_holder="Audit trail must enable reconstruction and validation of synthesis",
        adversary_position="Inadequate audit trail prevents verification of analysis reliability",
        counter_arguments=[
            "Comprehensive logging captures all material synthesis steps",
            "Provenance tracking enables validation of sources and methodologies",
            "Reproducibility via hashing ensures consistency across analyses",
            "Retention policies balance preservation needs with storage costs",
            "Audit trail accessibility supports transparency and accountability"
        ],
        resolution_strategy="Log all events, track provenance, hash for reproducibility, retain per policy",
        entity_scope="All synthesis analyses requiring auditability",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with comprehensive audit trail; DISCLOSURE if provenance gaps",
        controlling_precedent="PCAOB AS 1215 audit documentation standards"
    ),
    DoctrineBlock(
        topic="Error Propagation and Uncertainty Quantification",
        keywords=["error propagation", "uncertainty", "confidence interval", "variance", "Monte Carlo"],
        conclusion_template=[
            "Uncertainty quantification: {confidence_interval} confidence interval.",
            "Error sources: {error_sources}.",
            "Sensitivity: {sensitivity_summary}."
        ],
        reasoning_framework="""Quantify and propagate uncertainty through synthesis:
1. Identify error sources: Engine response variance, data quality, model assumptions, expert judgment
2. Quantify input uncertainties: Confidence scores from engines, data quality metrics, assumption sensitivity
3. Model error propagation: Simple (linear combination), Complex (Monte Carlo simulation)
4. Calculate output confidence interval: 90% CI for aggregate findings
5. Sensitivity analysis: Vary inputs +/- 20%, measure output variance
6. Classify uncertainty: Reducible (get better data), Irreducible (inherent randomness)
7. Communicate uncertainty: Point estimate + confidence interval + sensitivity caveats
8. Downgrade confidence if uncertainty exceeds materiality threshold""",
        key_factors=[
            "Number and magnitude of error sources",
            "Correlation of errors across domains (systematic vs. independent)",
            "Availability of data to quantify uncertainties",
            "Computational feasibility of error propagation (Monte Carlo vs. analytical)",
            "Materiality of uncertainty relative to decision thresholds",
            "Stakeholder sophistication in interpreting confidence intervals",
            "Regulatory requirements for uncertainty disclosure"
        ],
        primary_authority=[
            "Statistical literature on error propagation",
            "Monte Carlo simulation methodologies",
            "SEC guidance on forward-looking statement safe harbors"
        ],
        burden_holder="Uncertainty quantification must use reasonable methods and disclose limitations",
        adversary_position="Point estimates without uncertainty quantification are misleading",
        counter_arguments=[
            "Confidence intervals provide transparent uncertainty quantification",
            "Sensitivity analysis demonstrates robustness across reasonable input variations",
            "Professional judgment balances precision with practicality",
            "Disclosure of irreducible uncertainty manages stakeholder expectations",
            "Uncertainty quantification is standard practice in scientific and actuarial analysis"
        ],
        resolution_strategy="Quantify uncertainties, propagate via sensitivity or Monte Carlo, disclose confidence intervals",
        entity_scope="All synthesis analyses with material uncertainty",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with documented uncertainty quantification; DISCLOSURE if uncertainty material",
        controlling_precedent="SEC safe harbor for forward-looking statements with cautionary language"
    ),
    DoctrineBlock(
        topic="Multi-Scenario Analysis",
        keywords=["scenario", "sensitivity", "stress test", "what-if", "contingency", "alternative"],
        conclusion_template=[
            "Scenario analysis: {scenario_count} scenarios evaluated.",
            "Base case: {base_case_summary}.",
            "Worst case: {worst_case_summary}; Best case: {best_case_summary}."
        ],
        reasoning_framework="""Generate multi-scenario synthesis for decision support:
1. Define scenarios: Base case (most likely), Best case (optimistic), Worst case (pessimistic), Stress (extreme)
2. Vary key assumptions per scenario: Regulatory outcome, litigation result, tax treatment, operational performance
3. Re-run synthesis for each scenario with adjusted inputs
4. Compare scenario outcomes: Risk scores, financial impacts, compliance status
5. Assess scenario probabilities: Base 60%, Best 20%, Worst 15%, Stress 5%
6. Calculate probability-weighted expected value across scenarios
7. Identify scenario-robust strategies (perform well across all scenarios)
8. Present scenario analysis in matrix or decision tree format""",
        key_factors=[
            "Number and diversity of scenarios modeled",
            "Realism of scenario assumptions (grounded in evidence vs. speculation)",
            "Probability assignments to scenarios (based on forecasts, expert judgment)",
            "Range of outcomes across scenarios (narrow vs. wide dispersion)",
            "Identification of scenario-robust vs. scenario-dependent strategies",
            "Computational cost of re-running synthesis for each scenario",
            "Stakeholder use of scenario analysis for contingency planning"
        ],
        primary_authority=[
            "Decision analysis literature (Raiffa, Keeney)",
            "Scenario planning methodologies (Shell, GBN)",
            "Financial stress testing standards (Dodd-Frank, CCAR)"
        ],
        burden_holder="Scenario assumptions must be reasonable and probabilities disclosed",
        adversary_position="Cherry-picked scenarios bias analysis toward desired conclusion",
        counter_arguments=[
            "Comprehensive scenario set covers optimistic, pessimistic, and base cases",
            "Scenario assumptions grounded in forecasts and expert judgment",
            "Probability assignments disclosed and sensitivity-tested",
            "Scenario-robust strategies identified to mitigate outcome variance",
            "Scenario analysis is standard practice in strategic planning and risk management"
        ],
        resolution_strategy="Model comprehensive scenarios, assign probabilities, identify robust strategies",
        entity_scope="All strategic decisions under uncertainty",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with comprehensive scenarios and disclosed probabilities; AGGRESSIVE if scenarios biased",
        controlling_precedent="Dodd-Frank stress testing requirements for financial institutions"
    ),
    DoctrineBlock(
        topic="Continuous Synthesis Monitoring",
        keywords=["monitoring", "continuous", "real-time", "alerting", "trigger", "threshold"],
        conclusion_template=[
            "Monitoring active: {metric_count} metrics tracked.",
            "Alert thresholds: {threshold_summary}.",
            "Recent alerts: {alert_count} in past {timeframe}."
        ],
        reasoning_framework="""Enable continuous monitoring of synthesis metrics:
1. Define monitoring metrics: Risk score, confidence level, domain engine health, deadline proximity
2. Set alert thresholds: Risk score >80, confidence drops below DEFENSIBLE, engine downtime >5min, deadline <7 days
3. Establish monitoring cadence: Real-time for critical, hourly for important, daily for routine
4. Automate metric collection: Query engines, calculate aggregates, compare to thresholds
5. Generate alerts: Email, SMS, dashboard notification when threshold breached
6. Escalation protocol: L1 alert to analyst, L2 to manager, L3 to executive
7. Track alert history: False positive rate, response time, resolution effectiveness
8. Optimize thresholds: Adjust based on alert fatigue vs. missed events tradeoff""",
        key_factors=[
            "Selection of monitoring metrics (coverage, relevance, actionability)",
            "Calibration of alert thresholds (false positive vs. false negative tradeoff)",
            "Monitoring cadence and computational cost",
            "Alert delivery mechanisms and stakeholder preferences",
            "Escalation protocol and response SLAs",
            "Alert history analysis for threshold optimization",
            "Integration with incident response and remediation workflows"
        ],
        primary_authority=[
            "ITIL service monitoring best practices",
            "DevOps SRE monitoring standards",
            "SOC 2 continuous monitoring requirements"
        ],
        burden_holder="Monitoring must detect material issues without excessive false alarms",
        adversary_position="Alert fatigue from excessive false positives leads to ignored warnings",
        counter_arguments=[
            "Threshold calibration balances sensitivity and specificity",
            "Alert history analysis enables continuous improvement",
            "Escalation protocol ensures timely response to genuine issues",
            "Monitoring automation reduces manual oversight burden",
            "Industry standard practice for critical operational systems"
        ],
        resolution_strategy="Monitor key metrics, calibrate thresholds, escalate appropriately, optimize based on history",
        entity_scope="All entities requiring continuous synthesis oversight",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with calibrated thresholds and alert history optimization",
        controlling_precedent="SOC 2 Trust Services Criteria for monitoring and alerting"
    ),
    DoctrineBlock(
        topic="Federated Data Integration",
        keywords=["federated", "data integration", "ETL", "data quality", "schema mapping", "normalization"],
        conclusion_template=[
            "Data sources: {source_count} integrated.",
            "Data quality: {quality_score}/100.",
            "Schema mapping: {mapping_summary}."
        ],
        reasoning_framework="""Integrate data from federated domain engines:
1. Identify data sources: Each domain engine exposes different schema and data model
2. Map schemas: Align entity types (person, company, transaction), attribute names, data types
3. Extract data: Query engines via APIs, handle pagination, rate limits, errors
4. Transform data: Normalize formats (dates, currencies, names), resolve duplicates, validate integrity
5. Load data: Merge into unified synthesis data model
6. Assess data quality: Completeness, accuracy, consistency, timeliness (CAQT metrics)
7. Calculate quality score: Weighted average of CAQT dimensions (0-100 scale)
8. Flag data quality issues: Missing fields, outliers, stale data, conflicts""",
        key_factors=[
            "Number and heterogeneity of data sources",
            "Schema mapping complexity (simple alignment vs. complex transformation)",
            "Data volume and extraction performance",
            "Data quality across sources (some engines more reliable than others)",
            "Handling of conflicts and duplicates",
            "Freshness requirements (real-time vs. batch)",
            "Governance of data lineage and provenance"
        ],
        primary_authority=[
            "Data management literature (DAMA-DMBOK)",
            "ETL best practices",
            "ISO 8000 data quality standards"
        ],
        burden_holder="Data integration must preserve accuracy and completeness",
        adversary_position="Integration errors corrupt synthesis with garbage data",
        counter_arguments=[
            "Schema mapping uses documented transformations and validation rules",
            "Data quality metrics flag issues for review before synthesis",
            "Provenance tracking enables tracing errors to source",
            "Industry standard ETL methodologies applied",
            "Continuous improvement from data quality monitoring"
        ],
        resolution_strategy="Map schemas carefully, validate data quality, track provenance, monitor and improve",
        entity_scope="All multi-domain data integration contexts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with quality score >80; DISCLOSURE if 60-80; HIGH_RISK if <60",
        controlling_precedent="ISO 8000-61 data quality management standards"
    ),
    DoctrineBlock(
        topic="Regulatory Change Impact Analysis",
        keywords=["regulatory change", "impact analysis", "retroactivity", "transition", "effective date"],
        conclusion_template=[
            "Regulatory change detected: {change_description}.",
            "Effective date: {effective_date}.",
            "Impact: {impact_summary}."
        ],
        reasoning_framework="""Analyze impact of regulatory changes on synthesis:
1. Monitor regulatory feeds: IRS notices, SEC releases, state agency bulletins
2. Detect changes: New rules, amendments, repeals, guidance updates
3. Parse effective dates: Immediate, prospective, retroactive, phased
4. Assess impact: Entities affected, compliance burden, financial exposure
5. Map to domain engines: Tax change -> TIE, SEC rule -> Legal, state reg -> Regulatory
6. Trigger re-synthesis: Re-run affected analyses under new rules
7. Generate change alerts: Notify stakeholders of material impacts
8. Update doctrine cache: Incorporate new authorities into engine knowledge bases""",
        key_factors=[
            "Comprehensiveness of regulatory monitoring (all relevant agencies)",
            "Timeliness of change detection (real-time vs. periodic)",
            "Accuracy of effective date parsing (complex transition rules)",
            "Impact assessment methodology (materiality, affected entities)",
            "Automation of re-synthesis vs. manual review",
            "Stakeholder notification timing and content",
            "Doctrine cache update process and version control"
        ],
        primary_authority=[
            "Administrative Procedure Act (APA) on rulemaking",
            "Regulatory effective date rules per agency",
            "Retroactivity analysis (Landgraf v. USI Film Products)"
        ],
        burden_holder="Impact analysis must identify material regulatory changes and assess effects",
        adversary_position="Failure to detect regulatory changes leads to non-compliant synthesis",
        counter_arguments=[
            "Automated monitoring of regulatory feeds maximizes change detection",
            "Effective date parsing follows agency-specific rules",
            "Impact assessment uses materiality thresholds to focus attention",
            "Re-synthesis ensures analyses reflect current law",
            "Stakeholder alerts provide timely notice for compliance action"
        ],
        resolution_strategy="Monitor feeds, parse changes, assess impact, re-synthesize, alert stakeholders",
        entity_scope="All entities subject to dynamic regulatory environments",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with comprehensive monitoring and timely updates",
        controlling_precedent="Administrative Procedure Act notice-and-comment rulemaking requirements"
    ),
    DoctrineBlock(
        topic="Explainability and Interpretability",
        keywords=["explainability", "interpretability", "transparency", "black box", "reasoning chain"],
        conclusion_template=[
            "Reasoning chain: {step_count} steps documented.",
            "Key decision points: {decision_summary}.",
            "Explainability score: {explainability_score}/100."
        ],
        reasoning_framework="""Ensure synthesis is explainable and interpretable:
1. Document reasoning chain: Step-by-step logic from query to conclusion
2. Expose decision points: Conflict resolutions, weighting schemes, threshold applications
3. Cite authorities: Link each conclusion to supporting doctrine, statute, case, regulation
4. Visualize logic: Decision trees, flowcharts, dependency graphs
5. Provide counterfactuals: What would change if key assumption varied?
6. Measure explainability: Can a domain expert follow and validate the reasoning?
7. Generate plain language narrative: Translate technical synthesis into accessible summary
8. Enable drill-down: From summary to detailed reasoning to raw source data""",
        key_factors=[
            "Completeness of reasoning documentation (all steps captured)",
            "Clarity of decision point explanations (understandable to stakeholders)",
            "Traceability of conclusions to authorities (citation accuracy)",
            "Visualization effectiveness for complex logic",
            "Counterfactual analysis for key assumptions",
            "Stakeholder feedback on explainability (expert validation)",
            "Balance between detail and accessibility in plain language narrative"
        ],
        primary_authority=[
            "Explainable AI literature (DARPA XAI program)",
            "GDPR Article 22 right to explanation",
            "Professional standards for transparent expert analysis"
        ],
        burden_holder="Synthesis must be explainable to enable stakeholder validation",
        adversary_position="Black box synthesis lacks credibility and prevents informed reliance",
        counter_arguments=[
            "Comprehensive reasoning chain documentation provides full transparency",
            "Decision point exposure enables critique and validation",
            "Citation traceability links conclusions to authoritative sources",
            "Visualization and plain language improve accessibility",
            "Drill-down capability balances summary and detail needs",
            "Industry trend toward explainable AI and transparent analytics"
        ],
        resolution_strategy="Document reasoning, expose decisions, cite authorities, visualize, provide plain language",
        entity_scope="All synthesis analyses requiring stakeholder trust and validation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE with comprehensive explainability; DISCLOSURE if reasoning gaps",
        controlling_precedent="GDPR Article 22 right to explanation for automated decision-making"
    )
]

class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language synthesis query")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.REPORTING, description="Analysis context zone")
    engines: Optional[List[str]] = Field(None, description="Specific engines to query (auto-detect if None)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for synthesis")

class EngineResponse(BaseModel):
    engine_id: str
    response: str
    confidence: float
    authorities: List[str]
    facts: List[str]
    timestamp: str
    status: str

class SynthesisResponse(BaseModel):
    query_id: str
    query: str
    synthesis: str
    confidence: ConfidenceLevel
    risk_score: int
    engines_queried: List[str]
    key_findings: List[str]
    conflicts: List[str]
    recommendations: List[str]
    determinism_hash: str
    timestamp: str
    zone: AnalysisZone
    mode: ResponseMode

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float

class Metrics:
    def __init__(self):
        self.queries_total = 0
        self.queries_by_mode: Dict[str, int] = defaultdict(int)
        self.latencies: List[float] = []
        self.confidence_distribution: Dict[str, int] = defaultdict(int)
        self.engine_call_counts: Dict[str, int] = defaultdict(int)
        self.conflict_count = 0
        self.start_time = time.time()

    def record_query(self, mode: str, latency: float, confidence: str):
        self.queries_total += 1
        self.queries_by_mode[mode] += 1
        self.latencies.append(latency)
        self.confidence_distribution[confidence] += 1

    def record_engine_call(self, engine_id: str):
        self.engine_call_counts[engine_id] += 1

    def record_conflict(self):
        self.conflict_count += 1

    def get_stats(self) -> Dict[str, Any]:
        return {
            "queries_total": self.queries_total,
            "queries_by_mode": dict(self.queries_by_mode),
            "avg_latency_ms": sum(self.latencies) / len(self.latencies) * 1000 if self.latencies else 0,
            "p95_latency_ms": sorted(self.latencies)[int(len(self.latencies) * 0.95)] * 1000 if self.latencies else 0,
            "confidence_distribution": dict(self.confidence_distribution),
            "engine_call_counts": dict(self.engine_call_counts),
            "conflicts_detected": self.conflict_count,
            "uptime_seconds": time.time() - self.start_time
        }

metrics = Metrics()

async def query_engine(engine_url: str, query: str, timeout: int = 30) -> Optional[EngineResponse]:
    """Query a domain engine and return structured response"""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{engine_url}/query",
                json={"query": query, "mode": "FAST"}
            )
            if response.status_code == 200:
                data = response.json()
                return EngineResponse(
                    engine_id=engine_url.split(":")[-1],
                    response=data.get("response", ""),
                    confidence=data.get("confidence", 0.5),
                    authorities=data.get("authorities", []),
                    facts=data.get("facts", []),
                    timestamp=datetime.utcnow().isoformat(),
                    status="success"
                )
            else:
                logger.warning(f"Engine {engine_url} returned {response.status_code}")
                return None
    except Exception as e:
        logger.error(f"Failed to query engine {engine_url}: {e}")
        return None

def detect_conflicts(responses: List[EngineResponse]) -> List[str]:
    """Detect conflicts between domain engine responses"""
    conflicts = []
    facts_by_engine = {r.engine_id: set(r.facts) for r in responses}

    for i, r1 in enumerate(responses):
        for r2 in responses[i+1:]:
            conflicting_facts = []
            for fact1 in r1.facts:
                for fact2 in r2.facts:
                    if fact1.lower() != fact2.lower() and any(word in fact1.lower() and word in fact2.lower()
                                                               for word in ["tax", "liability", "amount", "date", "entity"]):
                        conflicting_facts.append((fact1, fact2))
            if conflicting_facts:
                conflicts.append(f"Conflict between {r1.engine_id} and {r2.engine_id}: {conflicting_facts[0]}")

    return conflicts

def weighted_confidence_aggregation(responses: List[EngineResponse], weights: Optional[Dict[str, float]] = None) -> float:
    """Aggregate confidence scores with domain weighting"""
    if not responses:
        return 0.0

    if weights is None:
        weights = {r.engine_id: 1.0 for r in responses}

    total_weight = sum(weights.get(r.engine_id, 1.0) for r in responses)
    weighted_sum = sum(r.confidence * weights.get(r.engine_id, 1.0) for r in responses)

    return weighted_sum / total_weight if total_weight > 0 else 0.0

def calculate_risk_score(responses: List[EngineResponse], conflicts: List[str]) -> int:
    """Calculate aggregate risk score 0-100"""
    if not responses:
        return 50

    avg_confidence = sum(r.confidence for r in responses) / len(responses)
    conflict_penalty = len(conflicts) * 5

    risk_score = int((1.0 - avg_confidence) * 100) + conflict_penalty
    return min(100, max(0, risk_score))

def generate_synthesis(query: str, responses: List[EngineResponse], conflicts: List[str], mode: ResponseMode) -> str:
    """Generate synthesized response from domain engine outputs"""
    if not responses:
        return "No domain engine responses available for synthesis."

    if mode == ResponseMode.FAST:
        return f"Synthesis of {len(responses)} domain engines: " + " ".join([r.response[:100] for r in responses[:3]])

    synthesis_parts = [f"Cross-domain synthesis of {len(responses)} engines:"]

    for response in responses:
        synthesis_parts.append(f"\n[{response.engine_id}] {response.response[:200]}")

    if conflicts:
        synthesis_parts.append(f"\n\nConflicts detected ({len(conflicts)}): {'; '.join(conflicts[:3])}")

    return "\n".join(synthesis_parts)

def calculate_determinism_hash(query: str, responses: List[EngineResponse]) -> str:
    """Calculate SHA-256 hash for reproducibility"""
    content = query + "".join([r.engine_id + r.response for r in responses])
    return hashlib.sha256(content.encode()).hexdigest()[:16]

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrine_count=len(DOCTRINE_CACHE),
        uptime_seconds=time.time() - metrics.start_time
    )

@app.post("/query", response_model=SynthesisResponse)
async def query(request: QueryRequest):
    start_time = time.time()
    query_id = hashlib.sha256(f"{request.query}{time.time()}".encode()).hexdigest()[:12]

    logger.info(f"Query {query_id}: {request.query[:100]}")

    # Mock engine detection and querying (would call actual engines in production)
    engine_urls = request.engines or ["http://localhost:8391", "http://localhost:8392", "http://localhost:8393"]

    tasks = [query_engine(url, request.query) for url in engine_urls]
    responses = [r for r in await asyncio.gather(*tasks) if r is not None]

    for r in responses:
        metrics.record_engine_call(r.engine_id)

    conflicts = detect_conflicts(responses)
    if conflicts:
        metrics.record_conflict()

    confidence_score = weighted_confidence_aggregation(responses)

    if confidence_score >= 0.8:
        confidence_level = ConfidenceLevel.DEFENSIBLE
    elif confidence_score >= 0.6:
        confidence_level = ConfidenceLevel.AGGRESSIVE
    elif confidence_score >= 0.4:
        confidence_level = ConfidenceLevel.DISCLOSURE
    else:
        confidence_level = ConfidenceLevel.HIGH_RISK

    risk_score = calculate_risk_score(responses, conflicts)
    synthesis = generate_synthesis(request.query, responses, conflicts, request.mode)
    determinism_hash = calculate_determinism_hash(request.query, responses)

    key_findings = []
    for r in responses[:5]:
        if r.facts:
            key_findings.extend(r.facts[:2])

    recommendations = [
        "Review conflicting findings for materiality",
        "Validate cross-references against source documents",
        "Consider multi-scenario analysis for risk assessment"
    ]

    latency = time.time() - start_time
    metrics.record_query(request.mode.value, latency, confidence_level.value)

    logger.info(f"Query {query_id} completed in {latency:.2f}s, confidence={confidence_level.value}")

    return SynthesisResponse(
        query_id=query_id,
        query=request.query,
        synthesis=synthesis,
        confidence=confidence_level,
        risk_score=risk_score,
        engines_queried=[r.engine_id for r in responses],
        key_findings=key_findings[:10],
        conflicts=conflicts,
        recommendations=recommendations,
        determinism_hash=determinism_hash,
        timestamp=datetime.utcnow().isoformat(),
        zone=request.zone,
        mode=request.mode
    )

@app.get("/metrics")
async def get_metrics():
    return metrics.get_stats()

@app.get("/doctrines")
async def get_doctrines():
    return {
        "count": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
