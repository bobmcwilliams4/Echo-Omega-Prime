import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
from datetime import datetime
from enum import Enum
import hashlib
import json

ENGINE_ID = "SYN04"
ENGINE_NAME = "Risk Matrix Generator"
VERSION = "1.0.0"
PORT = 9164

logger.add(f"{ENGINE_ID}_engine.log", rotation="100 MB", retention="30 days", level="INFO")

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class ZoneType(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class ProbabilityScale(str, Enum):
    RARE = "RARE"
    UNLIKELY = "UNLIKELY"
    POSSIBLE = "POSSIBLE"
    LIKELY = "LIKELY"
    ALMOST_CERTAIN = "ALMOST_CERTAIN"

class ImpactSeverity(str, Enum):
    INSIGNIFICANT = "INSIGNIFICANT"
    MINOR = "MINOR"
    MODERATE = "MODERATE"
    MAJOR = "MAJOR"
    CATASTROPHIC = "CATASTROPHIC"

class RiskCategory(str, Enum):
    STRATEGIC = "STRATEGIC"
    OPERATIONAL = "OPERATIONAL"
    FINANCIAL = "FINANCIAL"
    COMPLIANCE = "COMPLIANCE"
    REPUTATIONAL = "REPUTATIONAL"

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: List[str]
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    entity_scope: str = "all_entities"

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="probability_assessment_scales",
        keywords=["probability", "likelihood", "frequency", "occurrence", "chance"],
        conclusion_template=[
            "Probability assessment uses five-tier scale from Rare to Almost Certain",
            "Quantitative thresholds: Rare <5%, Unlikely 5-25%, Possible 25-50%, Likely 50-75%, Almost Certain >75%",
            "Historical frequency data validates probability classification"
        ],
        reasoning_framework=[
            "ISO 31000 recommends standardized likelihood scales",
            "Probability must reflect both historical data and forward-looking analysis",
            "Expert judgment calibrates statistical models",
            "Rare events require special attention despite low probability",
            "Probability ratings update as conditions change"
        ],
        key_factors=["historical frequency", "expert judgment", "statistical models", "trend analysis", "scenario planning"],
        primary_authority=["ISO 31000:2018", "COSO ERM Framework", "Project Management Body of Knowledge"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="impact_severity_classification",
        keywords=["impact", "severity", "consequence", "damage", "loss"],
        conclusion_template=[
            "Impact severity measured across financial, operational, reputational, and compliance dimensions",
            "Five-tier scale from Insignificant to Catastrophic enables consistent rating",
            "Multi-dimensional impact assessment captures full risk exposure"
        ],
        reasoning_framework=[
            "Impact varies by dimension - financial loss may be moderate while reputational damage catastrophic",
            "Threshold definition requires organizational context",
            "Cascading effects amplify initial impact",
            "Recovery time influences severity rating",
            "Stakeholder impact analysis informs classification"
        ],
        key_factors=["financial threshold", "operational disruption", "regulatory penalty", "stakeholder harm", "recovery duration"],
        primary_authority=["COSO ERM", "ISO 31000", "Enterprise Risk Management principles"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_entities"
    ),
    DoctrineBlock(
        topic="risk_scoring_models",
        keywords=["risk score", "rating", "calculation", "quantification", "matrix"],
        conclusion_template=[
            "Risk score = Probability x Impact using numerical scales",
            "Matrix mapping assigns risk levels: Low, Medium, High, Critical",
            "Weighted scoring adjusts for organizational risk appetite"
        ],
        reasoning_framework=[
            "Multiplicative model reflects joint probability and consequence",
            "Five-by-five matrix generates 25 risk cells",
            "Color coding (green/yellow/orange/red) enables visual prioritization",
            "Risk appetite boundary determines action thresholds",
            "Consistent scoring enables portfolio comparison"
        ],
        key_factors=["probability rating", "impact rating", "risk appetite", "threshold boundaries", "weighting factors"],
        primary_authority=["ISO 31000", "COSO ERM", "Risk Management Standards"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="coso_erm_framework",
        keywords=["COSO", "enterprise risk management", "framework", "integrated", "governance"],
        conclusion_template=[
            "COSO ERM integrates risk management with strategy and performance",
            "Five components: governance, strategy, performance, review, information",
            "Risk culture and risk appetite alignment critical to effectiveness"
        ],
        reasoning_framework=[
            "Board oversight establishes risk governance",
            "Strategy setting considers risk in objective formulation",
            "Performance monitoring tracks risk responses",
            "Review and revision ensure framework remains relevant",
            "Information flows support risk-informed decisions"
        ],
        key_factors=["governance structure", "risk appetite statement", "strategy integration", "performance metrics", "communication"],
        primary_authority=["COSO ERM Framework 2017", "Sarbanes-Oxley guidance", "SEC disclosure requirements"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_entities"
    ),
    DoctrineBlock(
        topic="iso_31000_risk_management",
        keywords=["ISO 31000", "risk management", "principles", "process", "international"],
        conclusion_template=[
            "ISO 31000 provides principles-based risk management framework",
            "Seven principles including integration, customization, and continual improvement",
            "Risk assessment process: identification, analysis, evaluation"
        ],
        reasoning_framework=[
            "Principles guide implementation across diverse contexts",
            "Risk management integrates with organizational processes",
            "Structured process ensures consistent treatment",
            "Stakeholder involvement enhances risk identification",
            "Continual improvement adapts to changing risk landscape"
        ],
        key_factors=["risk identification", "risk analysis", "risk evaluation", "risk treatment", "monitoring and review"],
        primary_authority=["ISO 31000:2018", "ISO Guide 73", "Risk Management Standards"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="risk_appetite_definitions",
        keywords=["risk appetite", "risk tolerance", "risk capacity", "threshold", "boundary"],
        conclusion_template=[
            "Risk appetite: amount and type of risk organization willing to pursue",
            "Risk tolerance: acceptable variation around objectives",
            "Risk capacity: maximum risk organization can bear before failure"
        ],
        reasoning_framework=[
            "Risk appetite statement guides strategy formulation",
            "Tolerance bands define acceptable operating ranges",
            "Capacity analysis prevents catastrophic exposure",
            "Board approves appetite; management sets tolerance",
            "Appetite aligns with strategic objectives and culture"
        ],
        key_factors=["strategic objectives", "financial capacity", "stakeholder expectations", "regulatory requirements", "competitive position"],
        primary_authority=["COSO ERM", "ISO 31000", "IRM Risk Appetite Guidance"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_entities"
    ),
    DoctrineBlock(
        topic="inherent_vs_residual_risk",
        keywords=["inherent risk", "residual risk", "control", "mitigation", "net risk"],
        conclusion_template=[
            "Inherent risk: exposure before controls applied",
            "Residual risk: remaining exposure after control effectiveness",
            "Control gap analysis identifies additional mitigation needs"
        ],
        reasoning_framework=[
            "Inherent risk assessment establishes baseline exposure",
            "Control effectiveness reduces inherent to residual risk",
            "Residual risk must remain within tolerance",
            "Cost-benefit analysis guides control investment",
            "Monitoring ensures controls maintain effectiveness"
        ],
        key_factors=["inherent probability", "inherent impact", "control design", "control effectiveness", "residual exposure"],
        primary_authority=["COSO Internal Control Framework", "ISO 31000", "NIST Risk Management Framework"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="control_effectiveness_rating",
        keywords=["control effectiveness", "design", "operating", "testing", "assurance"],
        conclusion_template=[
            "Control effectiveness assessed on design adequacy and operating performance",
            "Rating scale: Ineffective, Partially Effective, Largely Effective, Fully Effective",
            "Testing provides evidence of control operation"
        ],
        reasoning_framework=[
            "Design effectiveness: control capable of mitigating risk",
            "Operating effectiveness: control performs as designed",
            "Testing frequency based on risk and control nature",
            "Deficiencies trigger remediation or additional controls",
            "Continuous monitoring enhances effectiveness assessment"
        ],
        key_factors=["control design", "implementation quality", "test results", "deficiency tracking", "remediation status"],
        primary_authority=["COSO Internal Control", "PCAOB AS 2201", "SOC 2 criteria"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_entities"
    ),
    DoctrineBlock(
        topic="monte_carlo_simulation",
        keywords=["Monte Carlo", "simulation", "probability distribution", "random", "iteration"],
        conclusion_template=[
            "Monte Carlo simulation models risk through repeated random sampling",
            "Probability distributions define input variable ranges",
            "Thousands of iterations generate outcome distribution"
        ],
        reasoning_framework=[
            "Simulation captures interaction of multiple risk factors",
            "Outcome distribution reveals probability of various results",
            "Sensitivity analysis identifies key drivers",
            "Correlation modeling prevents unrealistic scenarios",
            "Convergence testing ensures sufficient iterations"
        ],
        key_factors=["input distributions", "correlation matrix", "iteration count", "random seed", "convergence criteria"],
        primary_authority=["Risk Analysis methods", "Quantitative Risk Assessment standards", "Project Management techniques"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="quantitative_analysis"
    ),
    DoctrineBlock(
        topic="sensitivity_analysis_tornado",
        keywords=["sensitivity", "tornado diagram", "driver", "variable", "variance"],
        conclusion_template=[
            "Sensitivity analysis identifies which variables most impact outcomes",
            "Tornado diagram displays ranked impact of variable changes",
            "Focus risk mitigation on high-impact drivers"
        ],
        reasoning_framework=[
            "One-at-a-time variation isolates variable effects",
            "Percentage change basis enables cross-variable comparison",
            "Tornado chart ranks variables by impact magnitude",
            "High-sensitivity variables require closer monitoring",
            "Multi-variable sensitivity reveals interaction effects"
        ],
        key_factors=["variable range", "baseline value", "impact magnitude", "variable correlation", "threshold points"],
        primary_authority=["Risk Analysis standards", "Decision Analysis methods", "Quantitative techniques"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="quantitative_models"
    ),
    DoctrineBlock(
        topic="risk_register_structure",
        keywords=["risk register", "inventory", "documentation", "tracking", "repository"],
        conclusion_template=[
            "Risk register maintains comprehensive inventory of identified risks",
            "Standard fields: risk ID, description, category, owner, assessment, status",
            "Regular updates ensure register remains current"
        ],
        reasoning_framework=[
            "Centralized register enables portfolio view",
            "Unique identifier supports tracking and reporting",
            "Ownership assignment ensures accountability",
            "Assessment fields capture inherent and residual ratings",
            "Treatment plan documents mitigation approach"
        ],
        key_factors=["risk identification", "categorization", "ownership", "assessment", "treatment plan", "status tracking"],
        primary_authority=["ISO 31000", "COSO ERM", "Risk Management best practices"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="key_risk_indicators",
        keywords=["KRI", "key risk indicator", "metric", "threshold", "early warning"],
        conclusion_template=[
            "KRIs provide early warning of increasing risk exposure",
            "Leading indicators predict future risk; lagging indicators confirm materialization",
            "Threshold definition triggers risk response"
        ],
        reasoning_framework=[
            "KRI selection aligns with critical risk factors",
            "Measurement frequency matches risk velocity",
            "Threshold levels define escalation points",
            "Dashboard reporting enables timely response",
            "Trend analysis reveals risk trajectory"
        ],
        key_factors=["indicator selection", "data availability", "threshold setting", "measurement frequency", "reporting process"],
        primary_authority=["COSO ERM", "KRI frameworks", "Risk Monitoring standards"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="risk_adjusted_return",
        keywords=["risk-adjusted", "return", "Sharpe ratio", "RAROC", "hurdle rate"],
        conclusion_template=[
            "Risk-adjusted return metrics account for volatility and downside potential",
            "Sharpe ratio measures excess return per unit of total risk",
            "RAROC (Risk-Adjusted Return on Capital) compares return to capital at risk"
        ],
        reasoning_framework=[
            "Risk adjustment prevents distorted performance comparison",
            "Higher volatility requires higher return for equivalent value",
            "Capital allocation considers both return and risk",
            "Hurdle rates incorporate risk premium",
            "Portfolio optimization maximizes risk-adjusted return"
        ],
        key_factors=["expected return", "risk measure", "risk-free rate", "volatility", "capital allocation"],
        primary_authority=["Modern Portfolio Theory", "Capital Asset Pricing Model", "Basel III framework"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="financial_analysis"
    ),
    DoctrineBlock(
        topic="expected_value_analysis",
        keywords=["expected value", "EV", "probability weighted", "decision tree", "outcome"],
        conclusion_template=[
            "Expected value = sum of (probability x outcome) across all scenarios",
            "Decision trees map alternative paths and associated probabilities",
            "EV analysis supports rational decision-making under uncertainty"
        ],
        reasoning_framework=[
            "Probability weighting accounts for uncertainty",
            "Multiple outcome scenarios capture range of possibilities",
            "Sequential decisions modeled through tree branches",
            "Information value analysis determines worth of reducing uncertainty",
            "Sensitivity testing validates EV conclusions"
        ],
        key_factors=["scenario probabilities", "outcome values", "decision points", "information availability", "risk preference"],
        primary_authority=["Decision Analysis theory", "Expected Utility theory", "Risk Analysis methods"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="decision_analysis"
    ),
    DoctrineBlock(
        topic="risk_heat_map_generation",
        keywords=["heat map", "risk matrix", "visualization", "color coding", "prioritization"],
        conclusion_template=[
            "Heat map visualizes risk portfolio on probability-impact grid",
            "Color intensity indicates risk severity: green/yellow/orange/red",
            "Bubble size or annotation displays additional attributes"
        ],
        reasoning_framework=[
            "Visual representation enables rapid risk prioritization",
            "Grid position communicates both likelihood and consequence",
            "Color coding supports intuitive risk level understanding",
            "Multiple risks plotted reveal concentration patterns",
            "Dynamic heat maps track risk movement over time"
        ],
        key_factors=["probability axis", "impact axis", "color scheme", "risk count", "attribute display"],
        primary_authority=["Risk visualization standards", "ISO 31000", "Risk reporting best practices"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="risk_mitigation_strategies",
        keywords=["mitigation", "control", "response", "treatment", "reduction"],
        conclusion_template=[
            "Four primary strategies: Avoid, Reduce, Transfer, Accept",
            "Mitigation selection considers cost, feasibility, and residual risk",
            "Layered controls provide defense-in-depth"
        ],
        reasoning_framework=[
            "Avoidance eliminates risk by ceasing activity",
            "Reduction implements controls to lower probability or impact",
            "Transfer shifts risk through insurance or contracts",
            "Acceptance acknowledges risk within tolerance",
            "Combination strategies address complex risks"
        ],
        key_factors=["risk level", "cost-benefit", "feasibility", "residual risk", "risk appetite"],
        primary_authority=["ISO 31000", "COSO ERM", "Risk Treatment standards"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="risk_category_classification",
        keywords=["risk category", "type", "classification", "taxonomy", "grouping"],
        conclusion_template=[
            "Standard categories: Strategic, Operational, Financial, Compliance, Reputational",
            "Category assignment enables specialized analysis and reporting",
            "Taxonomy consistency supports aggregation and comparison"
        ],
        reasoning_framework=[
            "Strategic risks affect long-term objectives and competitive position",
            "Operational risks arise from process, systems, or people failures",
            "Financial risks impact capital, liquidity, or market exposure",
            "Compliance risks involve regulatory or legal violations",
            "Reputational risks damage stakeholder trust and brand value"
        ],
        key_factors=["risk nature", "impact domain", "ownership structure", "treatment approach", "reporting audience"],
        primary_authority=["ISO 31000", "COSO ERM", "Industry risk taxonomies"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="risk_aggregation_methods",
        keywords=["aggregation", "correlation", "portfolio", "concentration", "diversification"],
        conclusion_template=[
            "Risk aggregation combines individual risks into portfolio view",
            "Correlation analysis prevents double-counting or underestimation",
            "Concentration limits prevent excessive exposure to single factor"
        ],
        reasoning_framework=[
            "Simple summation ignores diversification benefits",
            "Correlation matrix models risk interdependencies",
            "Copula methods capture tail dependencies",
            "Scenario analysis tests portfolio behavior under stress",
            "Concentration metrics identify over-exposure"
        ],
        key_factors=["individual risks", "correlation structure", "concentration limits", "diversification effect", "tail risk"],
        primary_authority=["Basel III", "Solvency II", "Portfolio Risk Management"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="financial_institutions"
    ),
    DoctrineBlock(
        topic="risk_appetite_cascade",
        keywords=["cascade", "allocation", "limit", "delegation", "hierarchy"],
        conclusion_template=[
            "Risk appetite cascades from enterprise to business unit to process level",
            "Allocation methodology ensures sum of limits remains within total appetite",
            "Limit monitoring prevents breach of delegated authorities"
        ],
        reasoning_framework=[
            "Board sets enterprise risk appetite",
            "Business unit limits allocated based on strategy and capacity",
            "Process-level tolerances guide operational decisions",
            "Limit utilization tracking prevents aggregate breach",
            "Escalation process addresses limit exceptions"
        ],
        key_factors=["enterprise appetite", "allocation methodology", "limit structure", "monitoring process", "escalation triggers"],
        primary_authority=["COSO ERM", "Risk Appetite frameworks", "Limit management practices"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="scenario_analysis_design",
        keywords=["scenario", "stress test", "what-if", "simulation", "adverse"],
        conclusion_template=[
            "Scenario analysis tests risk response under specified conditions",
            "Three scenario types: baseline, adverse, severe adverse",
            "Scenario design considers plausibility and severity"
        ],
        reasoning_framework=[
            "Historical scenarios replicate past crises",
            "Hypothetical scenarios test novel risk combinations",
            "Reverse stress testing identifies breaking points",
            "Severity calibration balances plausibility and stress",
            "Multiple scenarios capture diverse risk paths"
        ],
        key_factors=["scenario definition", "severity level", "parameter assumptions", "time horizon", "impact measures"],
        primary_authority=["Basel III stress testing", "CCAR guidance", "Scenario analysis standards"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="regulated_entities"
    ),
    DoctrineBlock(
        topic="bow_tie_analysis",
        keywords=["bow tie", "preventive", "detective", "mitigative", "barrier"],
        conclusion_template=[
            "Bow tie diagrams map threats, event, consequences, and controls",
            "Left side shows preventive controls; right side shows mitigative controls",
            "Barrier analysis identifies control gaps"
        ],
        reasoning_framework=[
            "Central event represents risk materialization",
            "Threat pathways show how event could occur",
            "Consequence branches display potential impacts",
            "Control barriers interrupt threat or mitigate consequence",
            "Gap analysis reveals missing or weak controls"
        ],
        key_factors=["threat identification", "consequence mapping", "control inventory", "barrier effectiveness", "gap analysis"],
        primary_authority=["Risk Management standards", "Process Safety techniques", "Control frameworks"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="operational_risk"
    ),
    DoctrineBlock(
        topic="risk_velocity_assessment",
        keywords=["velocity", "speed", "time to impact", "reaction time", "warning period"],
        conclusion_template=[
            "Risk velocity measures time from emergence to impact",
            "High-velocity risks require automated or pre-positioned responses",
            "Velocity assessment informs monitoring frequency and response readiness"
        ],
        reasoning_framework=[
            "Velocity varies by risk nature and context",
            "Sudden risks demand immediate response capability",
            "Slow-moving risks allow deliberative treatment",
            "Early warning systems extend reaction time",
            "Response time must match risk velocity"
        ],
        key_factors=["emergence indicators", "impact timeline", "detection capability", "response time", "mitigation speed"],
        primary_authority=["COSO ERM", "Risk Management standards", "Operational Risk frameworks"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="risk_culture_assessment",
        keywords=["risk culture", "tone at top", "awareness", "accountability", "behavior"],
        conclusion_template=[
            "Risk culture reflects shared values, beliefs, and behaviors regarding risk",
            "Tone at top sets cultural foundation",
            "Culture assessment measures awareness, accountability, and decision-making"
        ],
        reasoning_framework=[
            "Strong risk culture supports effective risk management",
            "Leadership behavior signals cultural priorities",
            "Risk awareness training builds competence",
            "Accountability mechanisms reinforce expectations",
            "Cultural indicators include speak-up rates and override frequency"
        ],
        key_factors=["leadership tone", "awareness level", "accountability structure", "behavioral indicators", "speak-up culture"],
        primary_authority=["COSO ERM", "FSB Risk Culture guidance", "IIF risk culture reports"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="emerging_risk_identification",
        keywords=["emerging risk", "horizon scanning", "early warning", "trend", "foresight"],
        conclusion_template=[
            "Emerging risks are newly developing or changing risks with uncertain impact",
            "Horizon scanning monitors external environment for risk signals",
            "Early identification enables proactive response"
        ],
        reasoning_framework=[
            "Emerging risks often arise from convergence of trends",
            "Weak signal detection requires diverse information sources",
            "Expert networks provide early insights",
            "Scenario planning tests emerging risk implications",
            "Adaptive strategies maintain flexibility"
        ],
        key_factors=["trend monitoring", "signal detection", "expert input", "scenario testing", "response readiness"],
        primary_authority=["ISO 31000", "Emerging Risk frameworks", "Foresight methodologies"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="risk_reporting_structure",
        keywords=["reporting", "dashboard", "escalation", "communication", "disclosure"],
        conclusion_template=[
            "Risk reporting provides timely, accurate, and actionable information",
            "Audience-tailored reports: Board (strategic), Management (tactical), Operations (detailed)",
            "Escalation protocols ensure critical risks reach appropriate level"
        ],
        reasoning_framework=[
            "Board reporting focuses on top risks and appetite compliance",
            "Management reporting enables portfolio decisions",
            "Operational reporting supports day-to-day risk ownership",
            "Dashboard visualization enhances comprehension",
            "Escalation thresholds trigger upward communication"
        ],
        key_factors=["audience needs", "reporting frequency", "content depth", "visualization", "escalation triggers"],
        primary_authority=["COSO ERM", "Risk Reporting standards", "Disclosure requirements"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    ),
    DoctrineBlock(
        topic="three_lines_model",
        keywords=["three lines", "defense", "assurance", "internal audit", "risk management"],
        conclusion_template=[
            "First line: operational management owns and manages risk",
            "Second line: risk and compliance functions provide oversight",
            "Third line: internal audit provides independent assurance"
        ],
        reasoning_framework=[
            "Clear role delineation prevents gaps and redundancy",
            "First line accountability essential for effectiveness",
            "Second line challenge strengthens risk management",
            "Third line independence ensures objective assessment",
            "Coordination among lines enhances overall assurance"
        ],
        key_factors=["role clarity", "accountability", "independence", "coordination", "reporting lines"],
        primary_authority=["IIA Three Lines Model", "COSO frameworks", "Governance standards"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="all_organizations"
    )
]

TELEMETRY: Dict[str, Any] = {
    "queries_total": 0,
    "cache_hits": 0,
    "vector_retrievals": 0,
    "deep_analysis": 0,
    "errors": {},
    "latency_ms": [],
    "doctrines_triggered": {}
}

COVERAGE_MAP: Dict[str, int] = {d.topic: 0 for d in DOCTRINE_CACHE}
DRIFT_LOG: List[Dict] = []
AUDIT_TRAIL_PATH = Path(f"{ENGINE_ID}_audit.jsonl")

class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: ZoneType = ZoneType.PLANNING
    context: Optional[Dict[str, Any]] = None

class RiskMatrixRequest(BaseModel):
    risks: List[Dict[str, Any]]
    mode: ResponseMode = ResponseMode.FAST

class RiskAssessmentInput(BaseModel):
    risk_description: str
    category: RiskCategory
    probability: Optional[ProbabilityScale] = None
    impact: Optional[ImpactSeverity] = None

class ResponseOutput(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    reasoning: List[str]
    authorities: List[str]
    zone: ZoneType
    doctrines_used: List[str]
    determinism_hash: str
    timestamp: str

def doctrine_cache_lookup(query: str, zone: ZoneType) -> Optional[DoctrineBlock]:
    query_lower = query.lower()
    for doctrine in DOCTRINE_CACHE:
        if any(kw in query_lower for kw in doctrine.keywords):
            TELEMETRY["cache_hits"] += 1
            COVERAGE_MAP[doctrine.topic] += 1
            return doctrine
    return None

def semantic_search_fallback(query: str) -> List[DoctrineBlock]:
    TELEMETRY["vector_retrievals"] += 1
    query_lower = query.lower()
    matches = []
    for doctrine in DOCTRINE_CACHE:
        if any(kw in query_lower for kw in doctrine.keywords[:3]):
            matches.append(doctrine)
    return matches[:3]

def deep_analysis(query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    TELEMETRY["deep_analysis"] += 1
    return {
        "multi_source_synthesis": True,
        "reasoning_chain": ["Identified risk parameters", "Applied framework", "Generated matrix"],
        "context_integration": context or {}
    }

def generate_determinism_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def log_audit_trail(query: str, response: str, doctrines: List[str]):
    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "response_preview": response[:200],
        "doctrines": doctrines,
        "hash": generate_determinism_hash(response)
    }
    with AUDIT_TRAIL_PATH.open("a") as f:
        f.write(json.dumps(audit_entry) + "\n")

def three_layer_response(query: str, mode: ResponseMode, zone: ZoneType, context: Optional[Dict] = None) -> ResponseOutput:
    start_time = datetime.utcnow()

    doctrine = doctrine_cache_lookup(query, zone)
    if doctrine:
        answer = " ".join(doctrine.conclusion_template)
        reasoning = doctrine.reasoning_framework[:3] if mode == ResponseMode.FAST else doctrine.reasoning_framework
        authorities = doctrine.primary_authority
        doctrines_used = [doctrine.topic]
        confidence = doctrine.confidence
    else:
        fallback = semantic_search_fallback(query)
        if fallback:
            answer = f"Risk matrix analysis incorporates: {', '.join([d.topic for d in fallback])}"
            reasoning = fallback[0].reasoning_framework[:2]
            authorities = fallback[0].primary_authority
            doctrines_used = [d.topic for d in fallback]
            confidence = ConfidenceLevel.AGGRESSIVE
        else:
            deep = deep_analysis(query, context)
            answer = "Comprehensive risk matrix requires probability and impact assessment across multiple dimensions"
            reasoning = deep["reasoning_chain"]
            authorities = ["ISO 31000:2018", "COSO ERM Framework"]
            doctrines_used = ["deep_analysis"]
            confidence = ConfidenceLevel.DISCLOSURE

    if mode == ResponseMode.MEMO:
        answer += " Full documentation supports audit and compliance requirements."
        reasoning.append("Memo mode provides comprehensive analysis with full citations")

    elapsed = (datetime.utcnow() - start_time).total_seconds() * 1000
    TELEMETRY["latency_ms"].append(elapsed)
    TELEMETRY["queries_total"] += 1

    response_text = f"{answer} | Reasoning: {reasoning[0]}"
    det_hash = generate_determinism_hash(response_text)
    log_audit_trail(query, answer, doctrines_used)

    return ResponseOutput(
        answer=answer,
        confidence=confidence,
        reasoning=reasoning,
        authorities=authorities,
        zone=zone,
        doctrines_used=doctrines_used,
        determinism_hash=det_hash,
        timestamp=datetime.utcnow().isoformat()
    )

def generate_risk_matrix(risks: List[Dict[str, Any]]) -> Dict[str, Any]:
    matrix = [[[] for _ in range(5)] for _ in range(5)]
    prob_map = {p.value: i for i, p in enumerate(ProbabilityScale)}
    impact_map = {s.value: i for i, s in enumerate(ImpactSeverity)}

    for risk in risks:
        prob = risk.get("probability", "POSSIBLE")
        impact = risk.get("impact", "MODERATE")
        if prob in prob_map and impact in impact_map:
            matrix[prob_map[prob]][impact_map[impact]].append(risk.get("id", "unknown"))

    heat_map = []
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell:
                heat_map.append({
                    "probability": list(ProbabilityScale)[i].value,
                    "impact": list(ImpactSeverity)[j].value,
                    "risk_count": len(cell),
                    "risk_ids": cell,
                    "risk_level": calculate_risk_level(i, j)
                })

    return {
        "matrix": matrix,
        "heat_map": heat_map,
        "total_risks": len(risks),
        "high_priority": sum(1 for h in heat_map if h["risk_level"] in ["HIGH", "CRITICAL"])
    }

def calculate_risk_level(prob_idx: int, impact_idx: int) -> str:
    score = (prob_idx + 1) * (impact_idx + 1)
    if score >= 20: return "CRITICAL"
    if score >= 12: return "HIGH"
    if score >= 6: return "MEDIUM"
    return "LOW"

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    yield
    logger.info(f"{ENGINE_NAME} shutting down")

app = FastAPI(title=ENGINE_NAME, version=VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    avg_latency = sum(TELEMETRY["latency_ms"]) / len(TELEMETRY["latency_ms"]) if TELEMETRY["latency_ms"] else 0
    return {
        "status": "healthy",
        "engine": ENGINE_NAME,
        "version": VERSION,
        "port": PORT,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "queries_total": TELEMETRY["queries_total"],
        "cache_hit_rate": TELEMETRY["cache_hits"] / max(TELEMETRY["queries_total"], 1),
        "avg_latency_ms": round(avg_latency, 2)
    }

@app.post("/query", response_model=ResponseOutput)
def query_endpoint(req: QueryRequest):
    try:
        return three_layer_response(req.query, req.mode, req.zone, req.context)
    except Exception as e:
        logger.error(f"Query error: {e}")
        error_type = type(e).__name__
        TELEMETRY["errors"][error_type] = TELEMETRY["errors"].get(error_type, 0) + 1
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/risk-matrix")
def risk_matrix_endpoint(req: RiskMatrixRequest):
    try:
        matrix = generate_risk_matrix(req.risks)
        return {
            "matrix": matrix,
            "mode": req.mode.value,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Risk matrix error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/assess-risk")
def assess_risk_endpoint(req: RiskAssessmentInput):
    try:
        doctrine = next((d for d in DOCTRINE_CACHE if req.category.value.lower() in d.topic.lower()), None)

        if not doctrine:
            doctrine = DOCTRINE_CACHE[0]

        prob = req.probability or ProbabilityScale.POSSIBLE
        impact = req.impact or ImpactSeverity.MODERATE

        prob_idx = list(ProbabilityScale).index(prob)
        impact_idx = list(ImpactSeverity).index(impact)
        risk_level = calculate_risk_level(prob_idx, impact_idx)

        return {
            "risk_description": req.risk_description,
            "category": req.category.value,
            "probability": prob.value,
            "impact": impact.value,
            "risk_score": (prob_idx + 1) * (impact_idx + 1),
            "risk_level": risk_level,
            "mitigation_strategy": doctrine.conclusion_template[0],
            "key_factors": doctrine.key_factors,
            "confidence": doctrine.confidence.value
        }
    except Exception as e:
        logger.error(f"Risk assessment error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics_endpoint():
    return {
        "telemetry": TELEMETRY,
        "coverage_map": COVERAGE_MAP,
        "drift_events": len(DRIFT_LOG),
        "audit_trail_size": AUDIT_TRAIL_PATH.stat().st_size if AUDIT_TRAIL_PATH.exists() else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
