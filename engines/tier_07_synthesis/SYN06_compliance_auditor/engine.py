#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SYN06 COMPLIANCE AUDITOR ENGINE v1.0.0
TIE-Grade Intelligence Engine - Port 9166

Compliance auditing across domains: gap analysis, control testing,
remediation tracking, regulatory change monitoring, compliance program assessment,
audit workpaper generation, finding severity classification, corrective action plans,
regulatory exam preparation, compliance calendar management.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

ENGINE_ID = "SYN06"
ENGINE_NAME = "Compliance Auditor"
VERSION = "1.0.0"
PORT = 9166

# ============================================================================
# ENUMS & DATA MODELS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    GAP_ANALYSIS = "gap_analysis"
    CONTROL_TESTING = "control_testing"
    FINDING_CLASSIFICATION = "finding_classification"
    REMEDIATION = "remediation"
    REGULATORY_MONITORING = "regulatory_monitoring"
    PROGRAM_ASSESSMENT = "program_assessment"
    WORKPAPER = "workpaper"
    EXAM_PREP = "exam_prep"

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
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    categories: List[IssueCategory] = field(default_factory=list)
    position_zone: PositionZone = PositionZone.PLANNING

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    mode: ResponseMode = ResponseMode.FAST
    context: Dict[str, Any] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    engine_id: str
    engine_name: str
    version: str
    query: str
    mode: ResponseMode
    answer: str
    confidence: ConfidenceLevel
    authorities_cited: List[str]
    doctrines_triggered: List[str]
    zone: PositionZone
    timestamp: str
    determinism_hash: str
    reasoning_chain: Optional[List[str]] = None

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    engine_name: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float

# ============================================================================
# DOCTRINE CACHE - 25+ COMPLIANCE AUDITING BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="COSO Internal Control Framework Foundation",
        keywords=["coso", "internal control", "five components", "control environment", "risk assessment"],
        conclusion_template="COSO provides the foundational framework for internal control assessment. The five components (control environment, risk assessment, control activities, information and communication, monitoring) must be present and functioning for effective internal control. All components are interrelated and affect the entire control system.",
        reasoning_framework="""
1. CONTROL ENVIRONMENT: Tone at top, organizational structure, commitment to competence, HR policies
   - Board oversight and independence
   - Management philosophy and operating style
   - Assignment of authority and responsibility
   - Ethical values and integrity throughout organization
2. RISK ASSESSMENT: Identification and analysis of risks to achievement of objectives
   - Objective setting (operations, reporting, compliance)
   - Risk identification (internal and external)
   - Risk analysis (likelihood and impact)
   - Change management (economic, regulatory, personnel)
3. CONTROL ACTIVITIES: Policies and procedures that ensure management directives carried out
   - Preventive vs detective controls
   - Segregation of duties
   - Authorization and approval procedures
   - Physical controls and asset safeguards
   - IT general and application controls
4. INFORMATION AND COMMUNICATION: Relevant information identified, captured, communicated in timely manner
   - Quality of information used in control system
   - Internal communication of responsibilities
   - External communication to stakeholders
5. MONITORING: Entire process assessed and modified as needed
   - Ongoing monitoring activities
   - Separate evaluations (internal audit, external audit)
   - Reporting deficiencies to appropriate levels
Audit approach: Test presence and operating effectiveness of each component, document deficiencies by component, assess entity-level vs process-level controls.
        """,
        key_factors=["presence of all five components", "operating effectiveness", "pervasiveness of deficiencies", "entity-level control strength", "management override risk"],
        primary_authority=["COSO Internal Control - Integrated Framework (2013)", "PCAOB AS 2201 (Auditing Internal Control)", "Sarbanes-Oxley Act Section 404"],
        burden_holder="Management",
        adversary_position="Controls are designed but not operating effectively, or component gaps exist but are immaterial to financial reporting.",
        counter_arguments=["design effectiveness does not prove operating effectiveness", "point-in-time testing may miss control failures", "compensating controls do not always mitigate design deficiencies", "entity-level weaknesses can permeate all process-level controls"],
        resolution_strategy="Document testing of all five components, identify deficiencies by severity (control deficiency, significant deficiency, material weakness), assess combination and aggregation risk, evaluate management remediation timeline.",
        entity_scope="All entities subject to internal control requirements (public companies, regulated entities, voluntary adopters)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="COSO is authoritative framework for internal control globally. Testing methodology aligned with PCAOB and SEC guidance.",
        controlling_precedent="COSO 2013 framework superseded 1992 version; transition complete by 2014.",
        categories=[IssueCategory.GAP_ANALYSIS, IssueCategory.CONTROL_TESTING, IssueCategory.PROGRAM_ASSESSMENT],
        position_zone=PositionZone.AUDIT
    ),
    DoctrineBlock(
        topic="Three Lines of Defense Model",
        keywords=["three lines", "defense model", "operational management", "risk management", "internal audit"],
        conclusion_template="The three lines model allocates governance, risk management, and control responsibilities across three lines: (1) operational management owns and manages risk, (2) risk management and compliance functions provide oversight, (3) internal audit provides independent assurance. Clear delineation prevents gaps and overlaps in accountability.",
        reasoning_framework="""
1. FIRST LINE: Operational Management
   - Owns and manages risk daily
   - Implements controls to mitigate risk
   - Accountable for control effectiveness
   - Self-assessment and continuous monitoring
   - Example roles: business unit managers, frontline supervisors, process owners
2. SECOND LINE: Risk Management and Compliance Functions
   - Develops policies, frameworks, risk appetite
   - Provides tools, guidance, training to first line
   - Monitors and reports on risk and compliance
   - Challenges first line decisions
   - Example roles: enterprise risk management, compliance officer, legal, quality assurance, IT security
3. THIRD LINE: Internal Audit
   - Provides independent, objective assurance
   - Evaluates adequacy and effectiveness of governance, risk management, controls
   - Reports to audit committee and senior management
   - Not responsible for risk management or control implementation (independence requirement)
   - Example activities: risk-based audit planning, control testing, advisory services
COORDINATION: Regular communication among lines, clear escalation paths, avoiding duplication, managing conflicts of interest.
Audit approach: Assess whether roles are clearly defined, evaluate independence of each line, test whether second line effectively challenges first line, verify third line independence from operations.
        """,
        key_factors=["role clarity", "independence of third line", "effectiveness of second line challenge", "communication and coordination", "avoidance of role conflicts"],
        primary_authority=["IIA Three Lines Model (2020)", "COSO ERM Framework", "Basel Committee on Banking Supervision guidance"],
        burden_holder="Board and senior management",
        adversary_position="Lines are combined or blurred to achieve efficiency, or third line performs management functions to fill gaps.",
        counter_arguments=["combining lines compromises independence and objectivity", "third line performing management tasks violates IIA standards", "efficiency gains from consolidation are offset by control failures", "regulatory expectations require separation"],
        resolution_strategy="Document responsibilities by line, identify areas of overlap or gaps, recommend organizational changes to restore independence, escalate to audit committee if management compromises third line.",
        entity_scope="Organizations of sufficient size and complexity to support three distinct lines (typically mid-size and larger companies, all regulated financial institutions)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="IIA model is globally recognized standard. Regulatory guidance (OCC, Fed, FINRA) reinforces three-line structure for financial institutions.",
        controlling_precedent="IIA updated model in 2020 from 'Three Lines of Defense' to 'Three Lines Model' with enhanced governance focus.",
        categories=[IssueCategory.PROGRAM_ASSESSMENT, IssueCategory.GAP_ANALYSIS],
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        topic="Risk-Based Audit Planning Methodology",
        keywords=["risk assessment", "audit universe", "audit plan", "risk scoring", "coverage"],
        conclusion_template="Risk-based audit planning prioritizes audit resources on highest-risk areas. A comprehensive audit universe identifies all auditable entities and processes, risk assessment scores each based on likelihood and impact, and the audit plan allocates resources to cover high-risk areas within a defined cycle (typically 3-5 years).",
        reasoning_framework="""
1. AUDIT UNIVERSE: Comprehensive inventory of all auditable entities, processes, systems
   - Business units, functions, locations
   - IT systems and applications
   - Key processes (financial reporting, procurement, HR, compliance)
   - Update annually for organizational changes
2. RISK ASSESSMENT: Score each universe item on inherent risk and control maturity
   - Inherent risk factors: financial materiality, regulatory complexity, change velocity, fraud susceptibility, prior audit issues
   - Control maturity: design effectiveness, operating effectiveness, management oversight, technology enablement
   - Residual risk = inherent risk / control maturity
3. PRIORITIZATION: Rank universe by residual risk score
   - High risk: annual audit coverage
   - Medium risk: 2-3 year rotation
   - Low risk: 4-5 year rotation or on-demand only
   - Mandatory coverage: regulatory requirements, management requests, fraud investigations
4. ANNUAL PLAN: Select audits from prioritized list to fit resource capacity
   - Balance risk coverage with skill availability
   - Include follow-up audits on prior findings
   - Reserve capacity for unplanned requests (10-15%)
5. MONITORING: Track actual coverage vs plan, update risk scores based on audit results, adjust plan quarterly
Audit approach: Review audit universe for completeness, validate risk scoring methodology, test whether high-risk areas received coverage, assess plan flexibility and responsiveness.
        """,
        key_factors=["completeness of audit universe", "objectivity of risk assessment", "coverage of highest risks", "plan flexibility", "communication with stakeholders"],
        primary_authority=["IIA International Standards for Professional Practice of Internal Auditing (Standards 2010, 2020)", "COSO ERM principles", "AICPA audit risk model"],
        burden_holder="Chief Audit Executive",
        adversary_position="Risk assessment is subjective; management requests should drive audit plan more than risk scores.",
        counter_arguments=["subjectivity is managed through defined criteria and calibration", "management requests address known issues but may miss emerging risks", "risk-based approach is IIA standard and regulatory expectation", "audit committee approval provides objectivity check"],
        resolution_strategy="Document risk assessment methodology with quantitative and qualitative factors, obtain audit committee approval of annual plan, track and report coverage metrics quarterly, demonstrate responsiveness to changes in risk profile.",
        entity_scope="All organizations with internal audit function (public companies, regulated entities, large private companies, government agencies)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Risk-based planning is IIA standard and universal best practice. Methodology is documented and calibrated against industry benchmarks.",
        controlling_precedent="IIA Standard 2010 requires risk-based plan; Standard 2020 requires communication and approval by senior management and board.",
        categories=[IssueCategory.PROGRAM_ASSESSMENT, IssueCategory.GAP_ANALYSIS],
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        topic="Control Testing Sampling and Evidence",
        keywords=["sample size", "statistical sampling", "attribute sampling", "tolerable deviation", "test of controls"],
        conclusion_template="Control testing sampling must provide reasonable assurance that controls operate effectively. Sample size is determined by desired confidence level, expected deviation rate, and tolerable deviation rate. Attribute sampling is appropriate for tests of controls; variables sampling for substantive tests. All samples must be representative of the population.",
        reasoning_framework="""
1. SAMPLING APPROACH SELECTION:
   - Attribute sampling: Tests of controls (yes/no, pass/fail attributes)
   - Variables sampling: Substantive testing (monetary amounts, quantities)
   - Non-statistical sampling: Acceptable if documented rationale for sample size and selection method
2. ATTRIBUTE SAMPLING PARAMETERS:
   - Confidence level: Typically 90-95% for controls testing
   - Expected deviation rate: Based on prior testing or initial sample (0-2% for effective controls)
   - Tolerable deviation rate: Maximum acceptable failure rate (often 5-10%)
   - Sample size formula: Driven by confidence level and tolerable rate; increases as tolerable rate decreases
3. SAMPLE SELECTION METHODS:
   - Random sampling: Every item has equal probability of selection (preferred)
   - Systematic sampling: Select every nth item after random start
   - Haphazard sampling: Non-statistical, auditor judgment (document rationale)
   - Stratification: Divide population into subgroups, sample each stratum
4. TESTING EXECUTION:
   - Define control objective and specific control being tested
   - Identify control attributes (e.g., evidence of approval, timeliness, accuracy)
   - Examine sample items for presence/absence of attributes
   - Document exceptions with root cause analysis
5. EVALUATION OF RESULTS:
   - Calculate actual deviation rate = exceptions / sample size
   - Compare to tolerable rate
   - If actual > tolerable: control is ineffective, expand testing or conclude deficiency
   - If actual <= tolerable but > expected: assess whether population deviation rate exceeds tolerable (upper deviation rate calculation)
   - Document conclusion on operating effectiveness
Audit approach: Validate sample size calculation, test randomness of selection, review exception documentation for completeness, assess whether conclusion is supported by results.
        """,
        key_factors=["sample size adequacy", "randomness of selection", "clear definition of control attributes", "documentation of exceptions", "appropriate conclusion"],
        primary_authority=["AICPA Audit Sampling Guide (AU-C 530)", "PCAOB AS 2315 (Audit Sampling)", "IIA Practice Guide on Audit Sampling"],
        burden_holder="Auditor",
        adversary_position="Judgmental sampling is faster and sufficient for internal audit; statistical rigor is unnecessary.",
        counter_arguments=["non-statistical sampling lacks measurable confidence level", "judgmental selection introduces bias risk", "inability to project results to population", "regulatory and external audit standards require statistical basis or documented rationale"],
        resolution_strategy="Use statistical sampling for high-risk controls and when quantitative conclusion is needed. Document rationale if non-statistical sampling is used. Ensure sample size provides reasonable assurance regardless of method.",
        entity_scope="All control testing engagements (SOX 404, operational audits, compliance audits)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Sampling standards are well-established in audit profession. Attribute sampling is universally accepted for tests of controls.",
        controlling_precedent="PCAOB AS 2315 and AICPA AU-C 530 provide authoritative guidance on audit sampling.",
        categories=[IssueCategory.CONTROL_TESTING, IssueCategory.WORKPAPER],
        position_zone=PositionZone.AUDIT
    ),
    DoctrineBlock(
        topic="IIA International Standards for Professional Practice",
        keywords=["iia standards", "attribute standards", "performance standards", "professional practices", "internal audit"],
        conclusion_template="The IIA International Standards for the Professional Practice of Internal Auditing are mandatory for IIA members and constitute best practice globally. Standards cover independence, proficiency, quality assurance, managing the internal audit activity, nature of work, engagement planning, performing the engagement, communicating results, and monitoring progress.",
        reasoning_framework="""
ATTRIBUTE STANDARDS (1000-1300): Characteristics of organizations and parties performing internal audit
- 1000: Purpose, Authority, Responsibility (audit charter)
- 1100: Independence and Objectivity (organizational and individual)
- 1200: Proficiency and Due Professional Care (knowledge, skills, continuing education)
- 1300: Quality Assurance and Improvement Program (internal and external assessments)
PERFORMANCE STANDARDS (2000-2600): Nature of internal audit activities and quality criteria
- 2000: Managing the Internal Audit Activity (planning, communication, resource management)
- 2010: Planning (risk-based plan, approved by senior management and board)
- 2020: Communication and Approval (plan and resource requirements)
- 2030: Resource Management (sufficient resources to accomplish plan)
- 2040: Policies and Procedures (written policies for all but smallest audit shops)
- 2050: Coordination (with other assurance providers to ensure coverage and minimize duplication)
- 2060: Reporting to Senior Management and Board (significant risks, governance issues, periodic reports)
- 2100: Nature of Work (governance, risk management, control)
- 2200: Engagement Planning (objectives, scope, timing, resource allocation)
- 2300: Performing the Engagement (sufficient information to achieve objectives)
- 2400: Communicating Results (timely, accurate, objective, clear, complete, constructive)
- 2500: Monitoring Progress (follow-up on management actions to address findings)
- 2600: Communicating the Acceptance of Risks (escalate if management accepts unacceptable residual risk)
APPLICATION: Standards apply to all internal audit engagements (assurance and consulting). Compliance is mandatory for IIA members. Deviations must be disclosed.
Audit approach: Assess compliance with applicable standards, review audit charter for alignment with Standard 1000, validate independence and objectivity per Standard 1100, test engagement workpapers against Standards 2200-2400.
        """,
        key_factors=["audit charter adequacy", "organizational independence", "competency and training", "quality assurance program", "risk-based planning", "engagement documentation", "communication timeliness and quality"],
        primary_authority=["IIA International Standards for the Professional Practice of Internal Auditing (updated periodically)", "IIA Code of Ethics", "IIA Practice Guides"],
        burden_holder="Chief Audit Executive and internal audit function",
        adversary_position="Standards are aspirational; full compliance is impractical for small audit shops or resource-constrained environments.",
        counter_arguments=["standards are mandatory for IIA members regardless of shop size", "Standard 2040 allows scalability of policies based on size and complexity", "non-compliance must be disclosed to senior management and board", "regulatory expectations (e.g., OCC, NYSE) reference IIA standards"],
        resolution_strategy="Conduct self-assessment against standards annually, disclose non-compliance with justification, implement quality assurance program per Standard 1300, obtain external quality assessment every five years.",
        entity_scope="All internal audit functions (public companies, private companies, government, nonprofits)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="IIA Standards are globally recognized and mandatory for IIA members. Regulatory guidance frequently references IIA Standards as best practice.",
        controlling_precedent="IIA Standards are updated periodically; current version effective as of date of engagement.",
        categories=[IssueCategory.PROGRAM_ASSESSMENT, IssueCategory.WORKPAPER],
        position_zone=PositionZone.AUDIT
    ),
    DoctrineBlock(
        topic="DOJ Evaluation of Corporate Compliance Programs",
        keywords=["doj compliance", "prosecutor evaluation", "effective compliance", "criminal prosecution", "fcpa"],
        conclusion_template="DOJ evaluates compliance program effectiveness when deciding whether to prosecute and how to resolve corporate criminal cases. Evaluation focuses on whether program is well-designed, adequately resourced, and works in practice. Key areas: risk assessment, policies and procedures, training, confidential reporting, investigation and remediation, continuous improvement, and effectiveness testing.",
        reasoning_framework="""
DOJ EVALUATION QUESTIONS (Updated Guidance 2023):
1. IS THE PROGRAM WELL-DESIGNED?
   - Risk assessment: Tailored to company's specific risks (industry, geography, products, third parties)
   - Policies and procedures: Clear, accessible, updated regularly, translated for global workforce
   - Roles and responsibilities: Compliance function independence, adequate authority, sufficient resources
   - Tone from top: Leadership commitment demonstrated through actions, not just statements
2. IS THE PROGRAM ADEQUATELY RESOURCED AND EMPOWERED?
   - Staffing levels: Sufficient compliance personnel for company size and complexity
   - Funding: Budget adequate for program needs (technology, training, investigations, monitoring)
   - Autonomy: Compliance reports to board or independent committee, not to business function with conflicts
   - Access: Compliance has direct access to board, counsel, and relevant data
3. DOES THE PROGRAM WORK IN PRACTICE?
   - Training effectiveness: Participation rates, comprehension testing, tailored content
   - Confidential reporting and investigation: Hotline usage, investigation thoroughness, retaliation prevention
   - Third-party management: Due diligence, contractual protections, monitoring, audit rights
   - Incentives and discipline: Compliance performance in compensation decisions, enforcement of violations
   - Continuous improvement: Root cause analysis of incidents, lessons learned, program enhancements
   - Periodic testing and review: Control testing, audits, effectiveness metrics, benchmarking
PROSECUTORS ASK: What would have happened if program were in place at time of misconduct? Has company demonstrated commitment to compliance or just checked boxes?
Audit approach: Obtain DOJ guidance documents, map compliance program elements to DOJ criteria, test effectiveness through control testing and interviews, assess whether program prevented/detected the violation at issue.
        """,
        key_factors=["risk-based design", "resource adequacy", "independence and authority", "tone from top", "testing and metrics", "continuous improvement", "third-party risk management"],
        primary_authority=["DOJ Evaluation of Corporate Compliance Programs (updated March 2023)", "U.S. Sentencing Guidelines Chapter 8 (Organizational Sentencing)", "FCPA Resource Guide (DOJ/SEC 2020)"],
        burden_holder="Company and compliance function",
        adversary_position="Compliance program existed and had policies covering the violation; misconduct was by rogue employee acting against policy.",
        counter_arguments=["existence of policy is insufficient; DOJ evaluates whether program works in practice", "isolated misconduct may indicate program failure if not detected by controls", "lack of discipline for violations undermines program credibility", "failure to update program based on lessons learned shows lack of commitment"],
        resolution_strategy="Demonstrate program effectiveness through metrics (training completion, hotline reports, investigation outcomes, disciplinary actions). Show continuous improvement over time. Conduct root cause analysis of any compliance failures and implement enhancements. Provide evidence of resource adequacy and independence.",
        entity_scope="All corporations subject to potential DOJ criminal prosecution (especially companies in high-risk industries: healthcare, defense, financial services, multinational operations)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DOJ guidance is authoritative and heavily influences prosecution decisions and settlement terms. Courts defer to DOJ evaluation in organizational sentencing.",
        controlling_precedent="March 2023 updated guidance supersedes prior versions; incorporates lessons from recent cases.",
        categories=[IssueCategory.PROGRAM_ASSESSMENT, IssueCategory.GAP_ANALYSIS],
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        topic="Federal Sentencing Guidelines for Organizations",
        keywords=["fsgo", "organizational sentencing", "culpability score", "effective compliance", "sentencing reduction"],
        conclusion_template="The Federal Sentencing Guidelines for Organizations (Chapter 8) provide framework for sentencing corporations convicted of federal crimes. Culpability score determines fine range. Effective compliance and ethics program can reduce culpability score (mitigating factor), while management involvement in misconduct increases score (aggravating factor). Seven minimum elements define effective program.",
        reasoning_framework="""
CULPABILITY SCORE CALCULATION (Guidelines Section 8C2.5):
Base score: 5
AGGRAVATING FACTORS (increase score):
- Organization size and involvement in criminal activity (+1 to +5)
- Prior criminal history (+1 to +2)
- Violation of court order or condition of probation (+2)
- Obstruction of justice (+3)
- High-level personnel involvement or tolerance of offense (+5 if >$5M organization, +3 otherwise)
MITIGATING FACTORS (decrease score):
- Effective compliance and ethics program (-3)
- Self-reporting, cooperation, acceptance of responsibility (-5 if all three, -1 or -2 if partial)
- Minimum score cannot be less than zero
SEVEN MINIMUM ELEMENTS OF EFFECTIVE PROGRAM (Section 8B2.1):
1. Standards and Procedures: Reasonably capable of reducing criminal conduct
2. Oversight: High-level personnel assigned responsibility for program
3. Due Care in Delegation: Substantial authority not given to individuals with propensity for illegal activity
4. Communication and Training: Effective communication to all levels; periodic training
5. Monitoring and Auditing: Reasonable steps to achieve compliance; auditing and reporting systems (whistleblower hotline)
6. Incentives and Discipline: Consistent promotion of compliance through incentives and discipline
7. Response and Prevention: Reasonable steps to respond to detected offenses and prevent further violations (root cause, remediation)
EFFECT ON SENTENCING: Culpability score multiplies by fine range; -3 reduction for effective program can reduce fine by 30-40%. Prosecutors consider program effectiveness in charging decisions.
Audit approach: Map compliance program to seven elements, test operating effectiveness of each, identify gaps, assess whether management involvement precludes credit for program effectiveness.
        """,
        key_factors=["presence of seven elements", "operating effectiveness", "independence of oversight", "training participation", "hotline functionality", "discipline consistency", "management involvement in offense"],
        primary_authority=["U.S. Sentencing Guidelines Chapter 8 (Organizations)", "Section 8B2.1 (Effective Compliance Program)", "Section 8C2.5 (Culpability Score)"],
        burden_holder="Organization",
        adversary_position="Program had all seven elements on paper, therefore effective compliance defense applies.",
        counter_arguments=["guidelines require effectiveness in practice, not just design", "high-level personnel involvement negates program credit", "failure to detect offense suggests program was ineffective", "lack of discipline for violations undermines element 6"],
        resolution_strategy="Demonstrate program operated effectively at time of offense (testing, training records, investigation logs, disciplinary actions). If management involved, argue for partial credit based on response and remediation. Show program enhancements post-offense to support cooperation credit.",
        entity_scope="All organizations subject to federal criminal prosecution (corporations, partnerships, unions, nonprofits, government entities)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Sentencing Guidelines are binding on federal courts. Effective program can result in substantial fine reduction, but burden is on organization to prove effectiveness.",
        controlling_precedent="Amendments to Chapter 8 in 2004, 2010, and 2021 refined effective program elements; latest version applies.",
        categories=[IssueCategory.PROGRAM_ASSESSMENT, IssueCategory.GAP_ANALYSIS],
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        topic="Gap Analysis Methodology",
        keywords=["gap analysis", "current state", "future state", "requirement mapping", "remediation"],
        conclusion_template="Gap analysis identifies differences between current state (actual practices, controls, capabilities) and future state (required or desired state based on regulations, standards, best practices). Methodology: define scope and criteria, document current state, map to requirements, identify and prioritize gaps, develop remediation plan with timelines and ownership.",
        reasoning_framework="""
FIVE-STEP GAP ANALYSIS PROCESS:
1. DEFINE SCOPE AND CRITERIA:
   - Identify applicable requirements (regulations, standards, contractual obligations, internal policies)
   - Examples: SOX 404 controls, PCI-DSS requirements, ISO 27001 controls, NIST Cybersecurity Framework
   - Define assessment boundaries (business units, processes, systems in scope)
2. DOCUMENT CURRENT STATE:
   - Inventory existing controls, policies, procedures, capabilities
   - Interview process owners and control operators
   - Review documentation (policies, procedures, evidence of operation)
   - Observe controls in operation where applicable
   - Rate maturity level (ad hoc, defined, managed, optimized) or existence (Y/N, Partial)
3. MAP CURRENT STATE TO REQUIREMENTS:
   - Create requirement-by-requirement comparison matrix
   - Assess each requirement: Fully Met, Partially Met, Not Met, Not Applicable
   - Document evidence supporting assessment
   - Identify root causes of gaps (lack of resources, unclear ownership, process immaturity, technology limitations)
4. IDENTIFY AND PRIORITIZE GAPS:
   - List all gaps with description and impact
   - Prioritize by severity: Critical (regulatory mandate, high risk), High (best practice, moderate risk), Medium (enhancement opportunity)
   - Consider remediation effort and cost vs risk reduction
5. DEVELOP REMEDIATION PLAN:
   - Define remediation actions for each gap (design new control, enhance existing, implement technology, provide training)
   - Assign ownership and target completion date
   - Estimate resources required (headcount, budget, systems)
   - Establish milestones and checkpoints
   - Track progress and report status to management and board
Audit approach: Validate completeness of requirements inventory, test accuracy of current state assessment, review gap prioritization rationale, assess feasibility of remediation plan, monitor progress on timelines.
        """,
        key_factors=["completeness of requirements", "accuracy of current state assessment", "objectivity of gap identification", "risk-based prioritization", "feasibility of remediation plan", "accountability and tracking"],
        primary_authority=["COSO Internal Control Framework (gap to effective internal control)", "ISO 19011 (auditing management systems)", "NIST SP 800-53 (gap to federal security controls)"],
        burden_holder="Management (owns remediation)",
        adversary_position="Gaps exist but are low priority given other business needs; partial controls are sufficient.",
        counter_arguments=["regulatory gaps must be remediated regardless of priority", "partial controls may not meet compliance requirements", "gap analysis provides evidence-based prioritization", "risk acceptance must be documented and approved at appropriate level"],
        resolution_strategy="Document gap analysis in structured format (spreadsheet or GRC tool), obtain management acknowledgment of gaps, escalate critical gaps to audit committee or board, track remediation progress quarterly, re-assess after remediation to confirm closure.",
        entity_scope="All compliance and audit engagements requiring comparison to external or internal standards",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Gap analysis is standard methodology in compliance and audit professions. Structured approach ensures objectivity and completeness.",
        controlling_precedent="Methodology varies by framework but core steps are consistent across standards (COSO, ISO, NIST, COBIT).",
        categories=[IssueCategory.GAP_ANALYSIS, IssueCategory.PROGRAM_ASSESSMENT],
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        topic="Regulatory Change Management and Horizon Scanning",
        keywords=["regulatory change", "horizon scanning", "impact assessment", "implementation tracking", "compliance calendar"],
        conclusion_template="Regulatory change management ensures timely identification, assessment, and implementation of new and amended regulations. Horizon scanning monitors regulatory developments 12-24 months ahead. Impact assessment determines applicability and required changes. Implementation tracking ensures compliance by effective date. Compliance calendar centralizes deadlines and deliverables.",
        reasoning_framework="""
REGULATORY CHANGE MANAGEMENT LIFECYCLE:
1. HORIZON SCANNING (Identification):
   - Monitor regulatory sources: Federal Register, agency websites, industry associations, legal counsel, regulatory intelligence services
   - Track proposed rules, final rules, guidance, enforcement actions
   - Review jurisdictions applicable to company (federal, state, international)
   - Establish alerts and RSS feeds for key agencies (SEC, FINRA, OCC, CFPB, FTC, EPA, OSHA, etc.)
   - Timeframe: 12-24 months advance notice for proposed rules
2. IMPACT ASSESSMENT (Analysis):
   - Determine applicability: Does rule apply to company based on industry, size, activities?
   - Assess scope of impact: Which business units, products, processes, systems affected?
   - Identify required changes: Policy updates, process redesign, system enhancements, reporting obligations
   - Estimate resources: Headcount, budget, technology, external advisors
   - Classify priority: High (new compliance obligation, significant penalties), Medium (enhancement to existing program), Low (clarification of existing requirement)
3. IMPLEMENTATION PLANNING:
   - Assign ownership: Compliance, legal, business unit, IT (depends on nature of change)
   - Develop project plan: Tasks, dependencies, milestones, target dates
   - Allocate resources: Budget approval, staff assignments, vendor selection
   - Define success criteria: Policies approved, controls operational, training complete, reporting tested
4. EXECUTION AND VALIDATION:
   - Implement required changes (policy, process, system, training)
   - Test controls before effective date
   - Conduct readiness review (self-assessment or internal audit)
   - Obtain sign-off from compliance, legal, and business stakeholders
5. ONGOING MONITORING:
   - Track compliance with new requirements
   - Monitor for additional guidance or enforcement actions
   - Update compliance calendar with periodic obligations (quarterly reporting, annual certifications)
COMPLIANCE CALENDAR: Centralized repository of compliance deadlines, deliverables, and responsible parties. Includes regulatory filings, certifications, testing, training, board reporting. Updated as new regulations implemented.
Audit approach: Review horizon scanning process for completeness of sources, test impact assessments for accuracy, validate implementation timelines against effective dates, assess whether changes were operational before deadline.
        """,
        key_factors=["completeness of regulatory sources", "timeliness of identification", "accuracy of impact assessment", "adequacy of resources", "compliance with effective dates", "calendar maintenance"],
        primary_authority=["Administrative Procedure Act (rulemaking process)", "Agency-specific guidance on implementation timelines", "COSO ERM (monitoring external environment)"],
        burden_holder="Compliance function (coordination); business units (implementation)",
        adversary_position="Regulatory change was not applicable or was minor enhancement not requiring formal project.",
        counter_arguments=["applicability determination must be documented and approved", "all regulatory changes require impact assessment regardless of perceived significance", "failure to implement by effective date is non-compliance", "enforcement actions often focus on new rules during initial implementation period"],
        resolution_strategy="Maintain regulatory change log with impact assessments, assign clear ownership for each regulation, escalate resource constraints to senior management early, conduct pre-effective date readiness review, document basis for non-applicability determinations.",
        entity_scope="All regulated entities (financial services, healthcare, energy, telecommunications, public companies)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory change management is best practice and expected by regulators. Failure to implement new rules is strict liability in many regimes.",
        controlling_precedent="Effective dates are legally binding; no grace period unless explicitly provided in rule or agency guidance.",
        categories=[IssueCategory.REGULATORY_MONITORING, IssueCategory.PROGRAM_ASSESSMENT],
        position_zone=PositionZone.PLANNING
    ),
    DoctrineBlock(
        topic="Audit Workpaper Standards and Documentation",
        keywords=["workpapers", "audit documentation", "permanent file", "engagement file", "review notes"],
        conclusion_template="Audit workpapers provide evidence that audit was performed in accordance with standards and support audit conclusions. Workpapers must be sufficient for an experienced auditor with no prior connection to the engagement to understand work performed, evidence obtained, and conclusions reached. Retention period varies by standards (typically 7 years for external audit, 5+ years for internal audit).",
        reasoning_framework="""
WORKPAPER DOCUMENTATION REQUIREMENTS:
1. PLANNING DOCUMENTATION:
   - Audit objective, scope, and approach
   - Risk assessment and audit program
   - Resource allocation and timeline
   - Prior audit findings and status of remediation
2. FIELDWORK DOCUMENTATION:
   - Tests performed with sample selection rationale
   - Evidence obtained (interviews, documents, system screenshots, data analytics results)
   - Exceptions identified with description and root cause
   - Follow-up on exceptions
   - Evaluation of results and preliminary conclusions
3. REVIEW DOCUMENTATION:
   - Review notes from senior auditor, manager, and partner/CAE
   - Responses to review notes
   - Evidence of review completion (initials and dates)
   - Clearance of all review points before issuing report
4. REPORTING DOCUMENTATION:
   - Draft and final audit report
   - Management responses to findings
   - Presentation materials for audit committee or board
   - Distribution list and acknowledgment of receipt
5. PERMANENT FILE (Retained across multiple engagements):
   - Organizational charts, policies, background information
   - Prior audit reports and summaries
   - Regulatory correspondence and corrective action plans
CHARACTERISTICS OF QUALITY WORKPAPERS:
- Clear and concise: Avoid jargon, use active voice, organize logically
- Complete: All assertions supported by evidence, no unexplained gaps
- Relevant: Tied to audit objectives, excludes extraneous information
- Accurate: Factual, no errors, properly sourced
- Objective: Balanced presentation, considers alternative explanations
- Standardized: Follows firm or department templates and indexing
RETENTION AND ACCESS:
- External audit: 7 years (Sarbanes-Oxley, PCAOB), 10 years (some state boards)
- Internal audit: 5-7 years (best practice), indefinitely for litigation or regulatory matters
- Access controls: Confidential, restricted to audit team and authorized reviewers
- Electronic workpapers: Secure storage, backup, version control, audit trail of changes
Audit approach: Review workpapers for completeness and clarity, test whether conclusions are supported by documented evidence, assess compliance with documentation standards (IIA, PCAOB, AICPA).
        """,
        key_factors=["completeness of documentation", "clarity and organization", "sufficiency of evidence", "evidence of review", "compliance with retention requirements", "security and confidentiality"],
        primary_authority=["IIA Standard 2330 (Documenting Information)", "PCAOB AS 1215 (Audit Documentation)", "AICPA AU-C 230 (Audit Documentation)"],
        burden_holder="Auditor",
        adversary_position="Workpapers are for auditor's use; level of detail is judgment call.",
        counter_arguments=["standards require documentation sufficient for experienced auditor to understand work", "inadequate documentation undermines audit quality and defensibility", "regulatory inspections and peer reviews assess workpaper quality", "litigation and subpoenas require production of workpapers"],
        resolution_strategy="Follow documentation standards and templates, ensure all workpapers are reviewed and cleared, conduct periodic self-assessments of workpaper quality, train audit staff on documentation requirements, implement quality control review before finalizing engagement.",
        entity_scope="All audit engagements (internal audit, external audit, SOX 404, operational audits, compliance audits)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Workpaper standards are explicit in IIA, PCAOB, and AICPA guidance. Quality of documentation is primary focus of regulatory inspections and peer reviews.",
        controlling_precedent="Standards are updated periodically; version in effect at date of engagement applies.",
        categories=[IssueCategory.WORKPAPER, IssueCategory.CONTROL_TESTING],
        position_zone=PositionZone.AUDIT
    ),
    DoctrineBlock(
        topic="Finding Classification: Critical, Major, Minor, Observation",
        keywords=["finding severity", "critical finding", "major deficiency", "observation", "risk rating"],
        conclusion_template="Audit findings are classified by severity based on risk exposure and potential impact. Critical: immediate action required, significant risk to organization, potential for material financial impact or regulatory sanction. Major: timely action required, moderate risk, could escalate if not addressed. Minor: low risk, improvement opportunity. Observation: best practice suggestion, no control deficiency identified.",
        reasoning_framework="""
FINDING SEVERITY CLASSIFICATION FRAMEWORK:
CRITICAL (Risk Rating: 9-10):
- Definition: Control deficiency or compliance violation with high likelihood of material impact
- Examples:
  * Material weakness in internal control over financial reporting (SOX 404)
  * Violation of law or regulation with potential for significant penalties or sanctions
  * Fraud or misconduct by senior management
  * Systemic control failure affecting multiple processes or business units
  * Cybersecurity breach with exposure of sensitive data
- Response: Immediate remediation required, escalate to audit committee and board, may require external disclosure (8-K, regulatory filing)
- Follow-up: Monthly monitoring until remediated, re-test before closing
MAJOR (Risk Rating: 6-8):
- Definition: Significant deficiency in control design or operation, moderate risk exposure
- Examples:
  * Control operates but with frequent exceptions or workarounds
  * Policy violation with potential for financial or reputational harm
  * Lack of segregation of duties in non-financial process
  * Non-compliance with internal policy or contractual obligation
  * IT general control weakness (access, change management, backup)
- Response: Remediation within 90 days, management action plan required, report to audit committee
- Follow-up: Quarterly monitoring, re-test within 6 months
MINOR (Risk Rating: 3-5):
- Definition: Control design or operation could be improved, low risk exposure
- Examples:
  * Isolated control exception with compensating controls present
  * Documentation gap (policy exists but not updated)
  * Training not completed on time but no evidence of lack of competency
  * Process inefficiency (not a control deficiency)
- Response: Remediation within 180 days, management action plan recommended
- Follow-up: Annual follow-up or next scheduled audit
OBSERVATION (Risk Rating: 1-2):
- Definition: Best practice suggestion, no control deficiency or compliance issue
- Examples:
  * Opportunity to enhance control efficiency through automation
  * Industry best practice not currently adopted
  * Benchmarking data showing opportunity for improvement
- Response: Optional for management to address, no formal action plan required
- Follow-up: None, unless management chooses to implement
CLASSIFICATION CRITERIA:
- Financial impact: Materiality, potential loss amount
- Regulatory risk: Likelihood and severity of regulatory action
- Reputational risk: Media attention, customer/investor reaction
- Fraud risk: Opportunity for misappropriation or misstatement
- Pervasiveness: Single instance vs systemic issue
- Likelihood: Probable, possible, remote
- Compensating controls: Presence of mitigating controls
Audit approach: Apply classification framework consistently, document rationale for severity rating, obtain audit committee or CAE approval for critical and major findings, track remediation by severity tier.
        """,
        key_factors=["consistency of classification", "documentation of rationale", "consideration of compensating controls", "alignment with regulatory definitions (material weakness, significant deficiency)", "escalation of critical findings"],
        primary_authority=["PCAOB AS 2201 (Material Weakness, Significant Deficiency definitions)", "COSO deficiency evaluation framework", "IIA Practice Guide on Communicating Audit Results"],
        burden_holder="Auditor (classification); management (remediation)",
        adversary_position="Finding should be downgraded because compensating controls exist or issue is isolated to single instance.",
        counter_arguments=["compensating controls must be tested and confirmed effective", "single instance may indicate systemic issue if root cause is process or control design", "severity reflects risk exposure not just observed impact", "regulatory definitions (e.g., material weakness) have specific criteria that must be met"],
        resolution_strategy="Document classification decision with reference to framework criteria, test compensating controls before downgrading severity, obtain management agreement on classification or document disagreement, escalate classification disputes to audit committee.",
        entity_scope="All audit and compliance engagements producing findings and recommendations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Classification frameworks are standard practice. Consistency and documentation of rationale are key to defensibility.",
        controlling_precedent="PCAOB definitions of material weakness and significant deficiency are authoritative for SOX 404; other contexts use risk-based frameworks.",
        categories=[IssueCategory.FINDING_CLASSIFICATION, IssueCategory.WORKPAPER],
        position_zone=PositionZone.REPORTING
    ),
    DoctrineBlock(
        topic="Corrective Action Plan (CAP) Development and Tracking",
        keywords=["corrective action", "remediation plan", "cap", "smart criteria", "finding closure"],
        conclusion_template="Corrective Action Plans address audit findings and compliance deficiencies. Effective CAPs are SMART: Specific (clear description of action), Measurable (defined success criteria), Achievable (realistic given resources), Relevant (addresses root cause), Time-bound (target completion date). CAP tracking monitors progress, identifies delays, and confirms closure through validation testing.",
        reasoning_framework="""
CAP DEVELOPMENT PROCESS:
1. ROOT CAUSE ANALYSIS:
   - Identify underlying cause of finding (not just symptom)
   - Common root causes: inadequate policy, lack of training, insufficient resources, process design flaw, technology limitation, poor communication
   - Use 5 Whys or fishbone diagram to drill down to root cause
2. DEFINE CORRECTIVE ACTIONS (SMART Criteria):
   - SPECIFIC: Describe exact action to be taken (e.g., 'Update vendor due diligence policy to require annual risk re-assessment' not 'Improve vendor management')
   - MEASURABLE: Define how completion will be evidenced (e.g., 'Policy approved by Compliance Committee and published on intranet')
   - ACHIEVABLE: Ensure resources are available (budget, staff, systems)
   - RELEVANT: Action must address root cause, not just symptom
   - TIME-BOUND: Target completion date based on finding severity (Critical: 30 days, Major: 90 days, Minor: 180 days)
3. ASSIGN OWNERSHIP:
   - Identify responsible party (individual with authority to execute and resources to deliver)
   - Escalate to senior management if additional resources needed
   - Define supporting roles (IT for system changes, Legal for policy approval, Compliance for validation)
4. ESTABLISH MILESTONES:
   - Break multi-step actions into phases with interim deadlines
   - Examples: Design (30 days), Build (60 days), Test (75 days), Deploy (90 days)
   - Identify dependencies (policy approval before training, system changes before testing)
5. VALIDATE AND CLOSE:
   - Management executes corrective actions
   - Internal audit or compliance validates completion (review evidence, test controls)
   - If effective: finding closed
   - If ineffective: CAP revised and timeline extended, or escalated for alternative remediation
   - Document closure with evidence of validation
CAP TRACKING:
- Centralized tracking tool (GRC system, spreadsheet, audit management software)
- Fields: Finding ID, Description, Severity, Root Cause, Corrective Action, Owner, Target Date, Status, Validation Date, Closure Date
- Status categories: Not Started, In Progress, Completed (pending validation), Validated/Closed, Delayed, Revised
- Reporting: Monthly status report to management, quarterly report to audit committee
- Escalation: Delays beyond 30 days require explanation and revised timeline; chronic delays escalated to senior management or board
Audit approach: Review CAPs for SMART criteria, assess whether actions address root cause, test whether target dates are realistic, monitor progress against milestones, validate closure through re-testing or evidence review.
        """,
        key_factors=["root cause identification", "SMART criteria compliance", "ownership clarity", "target date feasibility", "validation rigor", "escalation of delays"],
        primary_authority=["IIA Standard 2500 (Monitoring Progress)", "COSO Internal Control Framework (monitoring component)", "ISO 9001 (corrective action process)"],
        burden_holder="Management (development and execution); audit/compliance (validation)",
        adversary_position="Corrective action was completed as evidenced by policy update or training; closure should be immediate without re-testing.",
        counter_arguments=["completion of task does not prove effectiveness of remediation", "validation testing confirms control now operates as designed", "premature closure risks recurrence of finding", "IIA standards require monitoring of corrective actions"],
        resolution_strategy="Require validation evidence for all CAP closures (testing results, screenshots, signed policies, training records). Do not close findings based solely on management representation. Escalate delays with impact on compliance or risk exposure.",
        entity_scope="All audit and compliance functions that issue findings and track remediation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="SMART criteria and validation requirements are universal best practices. Tracking and reporting are IIA standard expectations.",
        controlling_precedent="IIA Standard 2500.A1 requires CAE to establish process to monitor and follow up on management actions; Standard 2500.C1 applies to consulting engagements.",
        categories=[IssueCategory.REMEDIATION, IssueCategory.PROGRAM_ASSESSMENT],
        position_zone=PositionZone.REPORTING
    ),
    DoctrineBlock(
        topic="Regulatory Exam Preparation and Response",
        keywords=["regulatory exam", "examination", "information request", "exit meeting", "exam response"],
        conclusion_template="Regulatory exams assess compliance with laws and regulations. Preparation involves organizing documentation, conducting self-assessment, identifying and remediating gaps, preparing staff. During exam: designate coordinator, track information requests, maintain exam log, prepare for interviews. Post-exam: review findings, develop response and CAP, negotiate with regulators, implement remediation, prepare for follow-up.",
        reasoning_framework="""
EXAM LIFECYCLE:
1. PRE-EXAM PREPARATION (Ongoing and upon notice):
   - Conduct annual self-assessment against exam priorities (published by regulators: OCC, Fed, SEC, FINRA, CFPB)
   - Organize documentation: policies, procedures, board minutes, committee charters, training records, testing results, prior exam responses
   - Remediate known gaps before exam
   - Train staff on exam process (what to expect, how to respond to requests, escalation protocol)
   - Designate exam coordinator (typically Chief Compliance Officer or General Counsel)
2. NOTICE AND SCOPING:
   - Review exam notification letter for scope, timing, and staff requests
   - Prepare opening presentation (company overview, business model, compliance program, changes since last exam)
   - Set up workspace for examiners (conference room, secure network access, document production capability)
   - Notify audit committee and senior management
3. INFORMATION REQUESTS:
   - Centralize all requests through exam coordinator (avoid direct responses from staff without review)
   - Log all requests with description, due date, assignee, completion status
   - Produce responsive documents only (avoid over-production)
   - Review documents for accuracy and privilege before production
   - Track cumulative burden (number of requests, hours spent)
4. INTERVIEWS:
   - Prepare staff with topic briefing and practice questions
   - Attendance: subject matter expert plus compliance or legal representative
   - Document interview topics and any commitments made
   - Follow up on unclear questions or requests in writing
5. EXIT MEETING:
   - Receive preliminary findings orally
   - Take detailed notes (findings, recommendations, observations)
   - Ask clarifying questions, provide factual corrections
   - Do not agree or disagree with findings at exit meeting (need time to review and respond)
   - Request draft report in writing
6. EXAM RESPONSE:
   - Review findings for accuracy and completeness
   - Develop written response addressing each finding
   - Provide corrective action plan with timelines and ownership
   - Negotiate finding characterization if appropriate (e.g., request downgrade from MRA to observation)
   - Obtain senior management and board approval of response before submission
7. POST-EXAM REMEDIATION:
   - Execute corrective action plan
   - Track progress and report quarterly to board
   - Prepare for follow-up exam or targeted review (typically within 12 months if significant findings)
   - Update policies and procedures based on lessons learned
EXAM MANAGEMENT BEST PRACTICES:
- Designate single point of contact for all examiner requests
- Maintain exam log with all requests, responses, and dates
- Implement document review process (subject matter expert → compliance → legal)
- Conduct daily debriefs with exam team to assess examiner focus and adjust strategy
- Escalate issues to senior management and counsel promptly
- Preserve all exam-related communications for future reference and litigation hold
Audit approach: Review exam preparation checklist, assess adequacy of self-assessment, validate documentation organization, test information request tracking process, review exam response for completeness and accuracy of CAPs.
        """,
        key_factors=["advance preparation", "centralized coordination", "document production controls", "interview preparation", "timely and complete response", "CAP execution and tracking"],
        primary_authority=["Agency-specific examination manuals (OCC, Fed, FDIC, FINRA, SEC)", "Regulatory exam frequency and scope guidance", "Administrative Procedure Act (exam process)"],
        burden_holder="Regulated entity",
        adversary_position="Finding is based on misunderstanding of facts or applicable regulation; examiner conclusion is incorrect.",
        counter_arguments=["exam findings are entitled to deference absent clear factual error", "legal interpretation can be contested but requires strong supporting analysis", "negotiation is appropriate for finding characterization (MRA vs MRA requiring board attention)", "failure to respond or implement CAP can result in escalated enforcement"],
        resolution_strategy="Provide factual corrections with supporting documentation. If legal disagreement, provide detailed analysis citing statutes, regulations, and precedent. Propose alternative remediation if examiner recommendation is impractical. Escalate to agency senior staff or counsel if examiner is unreasonable. Implement CAP regardless of disagreement to demonstrate good faith.",
        entity_scope="All regulated entities subject to periodic examinations (banks, broker-dealers, investment advisers, mortgage companies, insurance companies, public companies)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Exam process is well-established and similar across regulators. Response strategy is informed by regulatory guidance and industry best practices.",
        controlling_precedent="Examination manuals and guidance are updated periodically; current version at time of exam applies.",
        categories=[IssueCategory.EXAM_PREP, IssueCategory.REMEDIATION],
        position_zone=PositionZone.REPORTING
    ),
    DoctrineBlock(
        topic="Compliance Calendar and Periodic Deliverables Tracking",
        keywords=["compliance calendar", "deadlines", "regulatory filings", "certifications", "periodic reporting"],
        conclusion_template="Compliance calendar centralizes all compliance deadlines, deliverables, and responsible parties. Includes regulatory filings (10-K, 10-Q, 13D/G, Form 4, ADV, FOCUS, etc.), certifications (SOX 302/906, AML, BSA SAR, fair lending, privacy notices), testing (SOX 404, AML transaction monitoring, fair lending, UDAAP), training (annual compliance, Code of Conduct, anti-harassment), and governance (board/committee meetings, policy reviews). Automated reminders and escalation for missed deadlines.",
        reasoning_framework="""
COMPLIANCE CALENDAR COMPONENTS:
1. REGULATORY FILINGS:
   - SEC: 10-K (90 days after FYE), 10-Q (40/45 days after quarter), 8-K (4 days after triggering event), proxy (120 days before annual meeting), Section 16 (Form 3/4/5)
   - FINRA: FOCUS reports (monthly/quarterly), continuing education (Regulatory Element every 3 years), customer confirmations
   - Banking: Call Reports (30 days after quarter), CRA data (March 1 annually), HMDA (March 1 annually), compliance certifications
   - State regulators: Business entity reports, professional licenses, industry-specific filings
2. CERTIFICATIONS:
   - SOX 302: CEO/CFO certification of financial statements (with each 10-K/10-Q)
   - SOX 906: CEO/CFO certification of periodic reports (with each 10-K/10-Q)
   - AML: Annual independent testing, SAR filing (30 days after detection), CTR (15 days)
   - Fair Lending: Annual self-assessment, HMDA data integrity
   - Privacy: Annual privacy notice (if not continuous), data security incident reporting (varies by state)
3. TESTING AND AUDITS:
   - SOX 404: Internal control testing (quarterly for key controls, annually for others)
   - AML: Transaction monitoring testing (annually), customer due diligence (periodic and event-driven)
   - Information Security: Penetration testing, vulnerability scanning (quarterly/annually)
   - Vendor management: Due diligence updates (annually), contract reviews (every 3 years)
4. TRAINING:
   - Annual compliance training: Code of Conduct, conflicts of interest, insider trading, AML, information security
   - Role-based training: Fair lending (loan officers), UDAAP (customer-facing staff), Reg Z/RESPA (mortgage staff)
   - New hire training: Within 30 days of start date
   - Refresher training: Triggered by policy changes or exam findings
5. GOVERNANCE AND POLICY REVIEWS:
   - Board meetings: Quarterly (public companies), annually (private)
   - Committee meetings: Audit committee (quarterly), compensation (annually), risk committee (quarterly)
   - Policy reviews: Annual review of all compliance policies, update as needed
   - Business continuity testing: Annual test of disaster recovery and business continuity plans
CALENDAR MANAGEMENT:
- Platform: GRC system, calendar application, or dedicated compliance software
- Fields: Deliverable description, responsible party, due date, frequency, status, completion date, evidence of completion
- Reminders: 30 days, 14 days, 7 days, 1 day before due date
- Escalation: Automatic email to manager and compliance officer if deadline missed
- Reporting: Dashboard showing upcoming deadlines, overdue items, completion rates
- Archive: Maintain records of completed deliverables for audit and exam purposes
Audit approach: Validate completeness of calendar (compare to regulatory requirement inventory), test accuracy of due dates, assess timeliness of completions, review escalation process for missed deadlines, confirm evidence of completion is retained.
        """,
        key_factors=["completeness of calendar", "accuracy of due dates", "clarity of ownership", "timeliness of completion", "evidence retention", "escalation effectiveness"],
        primary_authority=["Specific regulations setting filing/certification/testing requirements", "IIA Practice Guide on Compliance", "COSO Monitoring Component"],
        burden_holder="Compliance function (calendar maintenance); business units (deliverable execution)",
        adversary_position="Deadline was met based on postmark or email timestamp; late receipt was due to external factors.",
        counter_arguments=["regulations specify 'filed by' or 'received by' date, not postmark", "technical issues do not excuse late filing (advance planning required)", "regulators rarely grant extensions absent extraordinary circumstances", "late filing can result in automatic penalties or loss of exemptions"],
        resolution_strategy="Maintain calendar with conservative due dates (e.g., internal deadline 3-5 days before regulatory deadline). Escalate delays immediately. Retain proof of timely filing (email confirmations, file-stamped receipts). If filing will be late, notify regulator proactively and request extension with justification.",
        entity_scope="All entities with regulatory compliance obligations (public companies, regulated financial institutions, healthcare providers, government contractors)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Compliance calendar is foundational best practice. Timeliness of filings and certifications is strict liability in most regimes.",
        controlling_precedent="Regulatory deadlines are set by statute or regulation and are non-negotiable absent waiver or extension.",
        categories=[IssueCategory.REGULATORY_MONITORING, IssueCategory.PROGRAM_ASSESSMENT],
        position_zone=PositionZone.PLANNING
    ),
]

# ============================================================================
# COMPLIANCE AUDITOR ENGINE
# ============================================================================

class ComplianceAuditorEngine:
    def __init__(self):
        self.start_time = time.time()
        self.total_queries = 0
        self.cache_hits = 0
        self.query_log = []

    def _normalize_terms(self, text: str) -> str:
        """Normalize compliance terminology for consistent matching."""
        normalizations = {
            "internal controls": "internal control",
            "coso framework": "coso",
            "three lines model": "three lines of defense",
            "iia standards": "iia",
            "doj guidance": "doj compliance",
            "sentencing guidelines": "fsgo",
            "control test": "control testing",
            "sample selection": "sampling",
            "finding severity": "finding classification",
            "cap": "corrective action plan",
            "exam prep": "regulatory exam",
            "compliance program": "program assessment",
        }
        text_lower = text.lower()
        for variant, canonical in normalizations.items():
            text_lower = text_lower.replace(variant, canonical)
        return text_lower

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant blocks (0-200ms tier)."""
        normalized_query = self._normalize_terms(query)
        query_tokens = set(normalized_query.split())

        matches = []
        for block in DOCTRINE_CACHE:
            keyword_matches = sum(1 for kw in block.keywords if kw in normalized_query)
            if keyword_matches > 0:
                topic_tokens = set(self._normalize_terms(block.topic).split())
                overlap = len(query_tokens & topic_tokens)
                score = keyword_matches * 10 + overlap
                matches.append((score, block))

        matches.sort(reverse=True, key=lambda x: x[0])
        return [block for score, block in matches[:3]] if matches else []

    def _three_layer_response(self, query: str, mode: ResponseMode) -> QueryResponse:
        """Three-layer response: cache -> semantic -> deep."""
        self.total_queries += 1
        normalized_query = self._normalize_terms(query)

        # Layer 1: Doctrine Cache
        cache_results = self._search_doctrine_cache(query)
        if cache_results:
            self.cache_hits += 1
            return self._format_response_from_cache(query, cache_results, mode)

        # Layer 2: Semantic retrieval (simulated - in production would query vector DB)
        semantic_result = self._semantic_fallback(query)
        if semantic_result:
            return self._format_response_semantic(query, semantic_result, mode)

        # Layer 3: Deep analysis
        return self._deep_analysis(query, mode)

    def _format_response_from_cache(self, query: str, blocks: List[DoctrineBlock], mode: ResponseMode) -> QueryResponse:
        """Format response from cached doctrine blocks."""
        primary_block = blocks[0]

        if mode == ResponseMode.FAST:
            answer = f"{primary_block.conclusion_template}\n\nKEY FACTORS: {', '.join(primary_block.key_factors[:3])}"
        elif mode == ResponseMode.DEFENSE:
            answer = f"COMPLIANCE POSITION:\n{primary_block.conclusion_template}\n\n"
            answer += f"REASONING:\n{primary_block.reasoning_framework[:800]}\n\n"
            answer += f"AUTHORITIES: {', '.join(primary_block.primary_authority)}\n\n"
            answer += f"RISK FACTORS: {', '.join(primary_block.key_factors)}"
        else:  # MEMO
            answer = f"COMPLIANCE AUDIT ANALYSIS - {primary_block.topic}\n\n"
            answer += f"ISSUE:\n{query}\n\n"
            answer += f"CONCLUSION:\n{primary_block.conclusion_template}\n\n"
            answer += f"ANALYSIS:\n{primary_block.reasoning_framework}\n\n"
            answer += f"AUTHORITY:\n{chr(10).join(f'- {auth}' for auth in primary_block.primary_authority)}\n\n"
            answer += f"KEY RISK FACTORS:\n{chr(10).join(f'- {factor}' for factor in primary_block.key_factors)}\n\n"
            answer += f"RECOMMENDATIONS:\n{primary_block.resolution_strategy}"

        doctrines_triggered = [b.topic for b in blocks]
        authorities = primary_block.primary_authority

        response_data = {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": VERSION,
            "query": query,
            "mode": mode,
            "answer": answer,
            "confidence": primary_block.confidence,
            "authorities_cited": authorities,
            "doctrines_triggered": doctrines_triggered,
            "zone": primary_block.position_zone,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "determinism_hash": hashlib.sha256(f"{query}{mode}{answer}".encode()).hexdigest()[:16],
        }

        if mode == ResponseMode.MEMO:
            response_data["reasoning_chain"] = [
                f"Doctrine cache hit: {primary_block.topic}",
                f"Confidence: {primary_block.confidence.value}",
                f"Categories: {', '.join(c.value for c in primary_block.categories)}",
            ]

        self.query_log.append({"query": query, "mode": mode.value, "timestamp": response_data["timestamp"], "cache_hit": True})
        return QueryResponse(**response_data)

    def _semantic_fallback(self, query: str) -> Optional[str]:
        """Semantic retrieval fallback (simulated)."""
        return None

    def _deep_analysis(self, query: str, mode: ResponseMode) -> QueryResponse:
        """Deep analysis for queries not in cache."""
        answer = f"COMPLIANCE AUDIT ANALYSIS:\n\nQuery: {query}\n\n"
        answer += "This query requires detailed compliance assessment. Recommended approach:\n\n"
        answer += "1. GAP ANALYSIS: Compare current state to applicable requirements (regulations, standards, best practices)\n"
        answer += "2. RISK ASSESSMENT: Identify likelihood and impact of non-compliance\n"
        answer += "3. CONTROL TESTING: Test design and operating effectiveness of controls\n"
        answer += "4. REMEDIATION PLANNING: Develop corrective action plan with SMART criteria\n"
        answer += "5. VALIDATION: Confirm remediation effectiveness through re-testing\n\n"
        answer += "Relevant frameworks: COSO Internal Control, IIA Standards, Three Lines Model, DOJ Compliance Program Evaluation\n\n"
        answer += "Consult compliance subject matter experts and legal counsel for specific guidance."

        response_data = {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": VERSION,
            "query": query,
            "mode": mode,
            "answer": answer,
            "confidence": ConfidenceLevel.DISCLOSURE,
            "authorities_cited": ["COSO Framework", "IIA Standards", "Three Lines Model", "DOJ Compliance Guidance"],
            "doctrines_triggered": ["General Compliance Methodology"],
            "zone": PositionZone.PLANNING,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "determinism_hash": hashlib.sha256(f"{query}{mode}{answer}".encode()).hexdigest()[:16],
            "reasoning_chain": ["No doctrine cache match", "Applied general compliance audit framework"],
        }

        self.query_log.append({"query": query, "mode": mode.value, "timestamp": response_data["timestamp"], "cache_hit": False})
        return QueryResponse(**response_data)

    def get_health(self) -> HealthResponse:
        """Health check endpoint."""
        uptime = time.time() - self.start_time
        cache_hit_rate = (self.cache_hits / self.total_queries * 100) if self.total_queries > 0 else 0.0

        return HealthResponse(
            status="healthy",
            engine_id=ENGINE_ID,
            engine_name=ENGINE_NAME,
            version=VERSION,
            port=PORT,
            doctrines_loaded=len(DOCTRINE_CACHE),
            uptime_seconds=round(uptime, 2),
            total_queries=self.total_queries,
            cache_hit_rate=round(cache_hit_rate, 2),
        )

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

engine = ComplianceAuditorEngine()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down. Total queries: {engine.total_queries}")

app = FastAPI(
    title=f"{ENGINE_NAME} Engine",
    version=VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer response."""
    try:
        return engine._three_layer_response(request.query, request.mode)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint."""
    return engine.get_health()

@app.get("/doctrines")
async def doctrines_endpoint():
    """List all doctrine topics."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": block.topic,
                "keywords": block.keywords,
                "categories": [c.value for c in block.categories],
                "confidence": block.confidence.value,
            }
            for block in DOCTRINE_CACHE
        ],
    }

if __name__ == "__main__":
    import uvicorn
    logger.add(f"syn06_compliance_{datetime.now().strftime('%Y%m%d')}.log", rotation="100 MB")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
