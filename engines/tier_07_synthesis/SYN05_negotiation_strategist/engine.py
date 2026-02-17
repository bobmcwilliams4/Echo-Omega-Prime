"""
SYN05 Negotiation Strategist Engine v1.0.0
TIE-Grade Intelligence Engine - Negotiation Strategy Analysis

Provides: BATNA assessment, ZOPA identification, anchoring strategies,
concession planning, interest-based negotiation, distributive vs integrative
approaches, multi-party negotiations, impasse breaking, deal structure
optimization, term prioritization.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# Engine Metadata
ENGINE_ID = "SYN05"
ENGINE_NAME = "Negotiation Strategist"
VERSION = "1.0.0"
PORT = 9165

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    f"logs/{ENGINE_ID}_audit.jsonl",
    rotation="100 MB",
    retention="90 days",
    format="{message}",
    level="INFO"
)

# Enums
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

class NegotiationCategory(str, Enum):
    BATNA_ANALYSIS = "BATNA_ANALYSIS"
    ZOPA_IDENTIFICATION = "ZOPA_IDENTIFICATION"
    ANCHORING_STRATEGY = "ANCHORING_STRATEGY"
    CONCESSION_PLANNING = "CONCESSION_PLANNING"
    INTEREST_BASED = "INTEREST_BASED"
    DISTRIBUTIVE_APPROACH = "DISTRIBUTIVE_APPROACH"
    INTEGRATIVE_APPROACH = "INTEGRATIVE_APPROACH"
    MULTIPARTY_DYNAMICS = "MULTIPARTY_DYNAMICS"
    IMPASSE_BREAKING = "IMPASSE_BREAKING"
    DEAL_STRUCTURE = "DEAL_STRUCTURE"
    TERM_PRIORITIZATION = "TERM_PRIORITIZATION"
    INFORMATION_ASYMMETRY = "INFORMATION_ASYMMETRY"

# Pydantic Models
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING)

class DoctrineBlock(BaseModel):
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

class TelemetryData(BaseModel):
    query_id: str
    timestamp: str
    latency_ms: float
    mode: str
    cache_hit: bool
    doctrines_triggered: List[str]
    confidence: str
    error_domain: Optional[str] = None

class QueryResponse(BaseModel):
    query_id: str
    response: str
    mode: str
    confidence: str
    doctrines_applied: List[str]
    telemetry: TelemetryData
    determinism_hash: str
    zone: str

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    engine_name: str
    version: str
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    doctrines_loaded: int

# Doctrine Cache
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Getting to Yes - Principled Negotiation Framework",
        keywords=["fisher", "ury", "principled negotiation", "interests", "options", "criteria", "BATNA"],
        conclusion_template="Apply Fisher and Ury's principled negotiation: separate people from problems, focus on interests not positions, generate options for mutual gain, insist on objective criteria, and develop strong BATNA.",
        reasoning_framework="""
Fisher and Ury's Getting to Yes establishes four core principles:
1. Separate people from the problem - Address relationship and substance independently
2. Focus on interests, not positions - Probe underlying needs, fears, and desires
3. Generate options for mutual gain - Brainstorm creative solutions before deciding
4. Insist on objective criteria - Use fair standards independent of will

The BATNA (Best Alternative to Negotiated Agreement) is the walk-away point.
Strong BATNA provides leverage; weak BATNA requires improving alternatives.
Never negotiate without knowing your BATNA and estimating theirs.
        """,
        key_factors=["BATNA strength", "interest alignment", "objective criteria", "relationship preservation", "creative options", "mutual gain potential"],
        primary_authority=["Fisher & Ury, Getting to Yes (1981)", "Harvard Negotiation Project", "Principled Negotiation Theory"],
        burden_holder="Negotiator proposing deviation from objective criteria",
        adversary_position="Positional bargaining, zero-sum framing, ignoring interests",
        counter_arguments=["Pure positional bargaining creates adversarial dynamics", "Objective criteria reduce power imbalances", "Interest-based approach expands pie"],
        resolution_strategy="Reframe from positions to interests, anchor to objective criteria, expand options through brainstorming",
        entity_scope="All negotiation contexts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Foundational negotiation theory with 40+ years empirical validation",
        controlling_precedent="Fisher & Ury seminal work, widely adopted in mediation and diplomacy"
    ),
    DoctrineBlock(
        topic="BATNA Analysis and Reservation Price",
        keywords=["BATNA", "reservation price", "walk away", "alternative", "leverage", "opportunity cost"],
        conclusion_template="Determine reservation price from BATNA value. Strong BATNA increases leverage; weak BATNA requires improving alternatives before negotiating. Never reveal true reservation price.",
        reasoning_framework="""
BATNA is the course of action if no agreement is reached.
Reservation price (RP) is the worst acceptable deal, derived from BATNA value.
BATNA strength determines negotiating power - better alternatives = higher RP.

Key steps:
1. Identify all alternatives to negotiated agreement
2. Develop the most promising alternative (improve BATNA)
3. Calculate reservation price from best alternative
4. Estimate counterparty's BATNA and RP
5. Assess BATNA asymmetry - who needs deal more?

Strong BATNA strategy: Signal alternatives without revealing details.
Weak BATNA strategy: Improve alternatives, build coalition, delay negotiation.
        """,
        key_factors=["Alternative value", "BATNA credibility", "opportunity costs", "time value", "BATNA improvement potential"],
        primary_authority=["Raiffa, The Art and Science of Negotiation", "Lax & Sebenius, 3-D Negotiation", "BATNA analysis methodology"],
        burden_holder="Party with weaker BATNA",
        adversary_position="Exploiting weak BATNA through aggressive tactics",
        counter_arguments=["Weak BATNA can be improved through preparation", "Credible alternatives shift power", "BATNA disclosure is strategic choice"],
        resolution_strategy="Build credible alternatives, delay if BATNA weak, improve BATNA before engaging",
        entity_scope="All negotiations with viable alternatives",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core concept in negotiation theory, empirically validated",
        controlling_precedent="Harvard Negotiation Project BATNA methodology"
    ),
    DoctrineBlock(
        topic="ZOPA - Zone of Possible Agreement",
        keywords=["ZOPA", "zone of possible agreement", "reservation price", "overlap", "bargaining range", "settlement range"],
        conclusion_template="ZOPA exists when buyer's maximum exceeds seller's minimum. Positive ZOPA enables agreement; negative ZOPA requires value creation or walk-away. Map ZOPA to identify settlement range.",
        reasoning_framework="""
ZOPA is the range between parties' reservation prices where agreement is possible.
Positive ZOPA: Buyer's max > Seller's min (deal possible)
Negative ZOPA: Buyer's max < Seller's min (no deal without value creation)

ZOPA mapping:
- Seller's RP is floor
- Buyer's RP is ceiling
- ZOPA is the overlap
- Final price falls within ZOPA
- Anchoring and concessions determine where in ZOPA settlement occurs

Negative ZOPA strategies:
1. Expand pie through value creation (integrative tactics)
2. Improve counterparty's BATNA perception
3. Worsen counterparty's BATNA
4. Accept no-deal outcome
        """,
        key_factors=["Reservation price accuracy", "ZOPA width", "anchor position", "information revelation", "value creation potential"],
        primary_authority=["Raiffa, Negotiation Analysis", "ZOPA theory", "Distributive bargaining literature"],
        burden_holder="Party seeking agreement with negative ZOPA",
        adversary_position="Claiming no ZOPA exists to extract concessions",
        counter_arguments=["ZOPA can be created through integrative tactics", "ZOPA estimation requires counterparty modeling", "Anchoring shapes ZOPA perception"],
        resolution_strategy="Estimate ZOPA, anchor strategically, create value if ZOPA negative",
        entity_scope="Distributive and integrative negotiations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fundamental negotiation concept with broad acceptance",
        controlling_precedent="Raiffa's negotiation analysis framework"
    ),
    DoctrineBlock(
        topic="Anchoring and Adjustment Heuristic",
        keywords=["anchoring", "first offer", "adjustment", "reference point", "framing", "extreme anchor"],
        conclusion_template="First offer anchors negotiation. Extreme anchors shift final settlement toward anchor. Counteract adverse anchor with objective criteria or immediate counter-anchor.",
        reasoning_framework="""
Anchoring effect: Initial reference point disproportionately influences final outcome.
Tversky & Kahneman demonstrated insufficient adjustment from anchors.

Anchoring strategy:
- Make first offer when confident in ZOPA estimate
- Anchor beyond reservation price but within credible range
- Extreme anchors shift settlement more than moderate anchors
- Justify anchor with objective criteria to enhance credibility

Counter-anchoring tactics:
- Reject anchor as outside reasonable range
- Immediately counter-anchor with own extreme position
- Reframe to objective criteria (market comps, industry standards)
- Ignore anchor and focus on interests

Research shows 30-50% of variance in outcomes explained by anchor value.
        """,
        key_factors=["Anchor credibility", "adjustment magnitude", "objective criteria", "anchor timing", "counterparty sophistication"],
        primary_authority=["Tversky & Kahneman, Judgment Under Uncertainty", "Galinsky & Mussweiler, First Offers as Anchors", "Anchoring research"],
        burden_holder="Party responding to anchor",
        adversary_position="Extreme anchoring to shift ZOPA perception",
        counter_arguments=["Sophisticated negotiators adjust for anchors", "Objective criteria mitigate anchoring", "Counter-anchors reset reference point"],
        resolution_strategy="Anchor first when informed, counter-anchor immediately if anchored adversely",
        entity_scope="All distributive negotiations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Robust empirical support from behavioral economics",
        controlling_precedent="Tversky & Kahneman heuristics and biases research"
    ),
    DoctrineBlock(
        topic="Concession Strategy and Pattern",
        keywords=["concessions", "concession pattern", "reciprocity", "diminishing concessions", "final offer"],
        conclusion_template="Make diminishing concessions to signal approaching reservation price. Demand reciprocal concessions. Final concession should be small to signal limit.",
        reasoning_framework="""
Concession pattern signals reservation price proximity:
- Large early concessions signal flexibility and invite further demands
- Small consistent concessions signal firm position
- Diminishing concessions (e.g., 1000, 500, 200, 50) signal approaching limit

Reciprocity norm: Concessions should be matched in magnitude and timing.
Unreciprocated concessions create perception of weakness.

Effective concession tactics:
1. Plan concession schedule in advance
2. Trade concessions on low-cost items for high-value gains
3. Bundle concessions to create package deals
4. Make conditional concessions (if-then framing)
5. Signal final offer clearly to avoid further demands

Avoid reactive concessions - only concede with strategic purpose.
        """,
        key_factors=["Concession magnitude", "concession timing", "reciprocity", "diminishing pattern", "conditional framing"],
        primary_authority=["Thompson, The Mind and Heart of the Negotiator", "Cialdini, Influence (Reciprocity)", "Concession research"],
        burden_holder="Party making unreciprocated concessions",
        adversary_position="Demanding concessions without reciprocation",
        counter_arguments=["Reciprocity is social norm", "Diminishing concessions are rational", "Conditional concessions protect value"],
        resolution_strategy="Plan concession schedule, demand reciprocity, use diminishing pattern",
        entity_scope="Distributive and integrative negotiations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established in negotiation practice and research",
        controlling_precedent="Reciprocity norm and diminishing concessions literature"
    ),
    DoctrineBlock(
        topic="Integrative (Win-Win) Negotiation",
        keywords=["integrative", "win-win", "value creation", "expanding pie", "tradeoffs", "logrolling"],
        conclusion_template="Create value through tradeoffs on differentially valued issues. Identify complementary interests and package deals. Integrative tactics expand ZOPA.",
        reasoning_framework="""
Integrative negotiation expands total value through:
1. Logrolling - Trading issues valued differently by parties
2. Non-specific compensation - Side payments unrelated to core issues
3. Cost-cutting - Reducing counterparty's costs to make offer attractive
4. Bridging - Creating new option satisfying both parties' interests

Conditions for integrative negotiation:
- Multiple issues to trade
- Differential valuation of issues
- Trust sufficient to share information
- Long-term relationship value

Tactics:
- Ask diagnostic questions about interests
- Share information about priorities (not reservation price)
- Brainstorm multiple options before deciding
- Use contingent agreements to manage risk

Integrative approach is superior to distributive when relationship matters.
        """,
        key_factors=["Issue differentials", "information sharing", "trust level", "relationship value", "creative options"],
        primary_authority=["Walton & McKersie, A Behavioral Theory of Labor Negotiations", "Lax & Sebenius, The Manager as Negotiator", "Integrative bargaining theory"],
        burden_holder="Party defaulting to distributive tactics",
        adversary_position="Zero-sum framing, refusing to share information",
        counter_arguments=["Value creation requires information sharing", "Integrative tactics expand pie", "Long-term relationships favor integration"],
        resolution_strategy="Identify issue tradeoffs, share priority information, brainstorm package deals",
        entity_scope="Multi-issue negotiations with relationship value",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core negotiation theory with strong empirical support",
        controlling_precedent="Walton & McKersie integrative bargaining framework"
    ),
    DoctrineBlock(
        topic="Distributive (Win-Lose) Negotiation",
        keywords=["distributive", "zero-sum", "claiming value", "competitive", "positional", "single issue"],
        conclusion_template="In distributive negotiation, claim value through anchoring, information control, and strategic concessions. Appropriate when single issue, no relationship value, or adversarial context.",
        reasoning_framework="""
Distributive negotiation treats fixed pie - one party's gain is other's loss.
Common in single-issue negotiations (price only) or adversarial contexts.

Distributive tactics:
- Anchor aggressively to shift ZOPA perception
- Withhold information about reservation price and BATNA
- Make small concessions to signal firmness
- Claim objective criteria support your position
- Create time pressure on counterparty
- Threaten to walk away (if credible BATNA)

Risks:
- Damages relationship
- Leaves value on table (misses integrative potential)
- Invites retaliation in future dealings
- Creates lose-lose if both parties use hard tactics

Use distributive approach when:
- Single issue with zero-sum structure
- No future relationship
- Counterparty using hard tactics
- Deal size too small to justify integrative effort
        """,
        key_factors=["Issue structure", "relationship value", "BATNA strength", "information asymmetry", "time pressure"],
        primary_authority=["Walton & McKersie, Distributive Bargaining", "Zero-sum game theory", "Competitive tactics research"],
        burden_holder="Party with weaker BATNA or less information",
        adversary_position="Extreme distributive tactics harming relationship",
        counter_arguments=["Distributive approach appropriate in adversarial contexts", "Claiming value is rational when pie is fixed", "Integrative tactics can be exploited"],
        resolution_strategy="Match counterparty's approach, protect reservation price, claim value strategically",
        entity_scope="Single-issue or adversarial negotiations",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Effective in zero-sum contexts but risks relationship damage",
        controlling_precedent="Distributive bargaining theory"
    ),
    DoctrineBlock(
        topic="Multiparty Negotiation Dynamics",
        keywords=["multiparty", "coalition", "voting", "blocking coalition", "veto power", "consensus"],
        conclusion_template="In multiparty negotiations, form coalitions, manage voting rules, and identify veto players. Coalition formation and agenda control are key power sources.",
        reasoning_framework="""
Multiparty negotiation complexity increases exponentially with parties.
Key dynamics:
1. Coalition formation - Subgroups with aligned interests
2. Voting rules - Unanimity vs. majority vs. supermajority
3. Agenda control - Who sets discussion sequence and options
4. Veto power - Parties who can block agreement

Coalition strategy:
- Identify natural allies based on interest alignment
- Form minimum winning coalition (avoid sharing value with unnecessary parties)
- Monitor countercoalitions and preempt formation
- Use side payments to recruit coalition members

Consensus challenges:
- Unanimity rule gives each party veto (high transaction costs)
- Majority rule excludes minority interests (implementation risk)
- Supermajority balances inclusivity and efficiency

Agenda control is powerful - early issues frame later discussions.
        """,
        key_factors=["Coalition structure", "voting rules", "veto players", "agenda control", "side payments", "implementation power"],
        primary_authority=["Sebenius, Negotiation Analysis: A Characterization and Review", "Coalition theory", "Multiparty bargaining research"],
        burden_holder="Party excluded from majority coalition",
        adversary_position="Exploiting agenda control or forming blocking coalition",
        counter_arguments=["Coalition formation is rational", "Voting rules affect outcomes", "Agenda control shapes options"],
        resolution_strategy="Build coalitions, influence agenda, manage voting rules",
        entity_scope="Negotiations with three or more parties",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established in political science and negotiation theory",
        controlling_precedent="Coalition theory and multiparty bargaining literature"
    ),
    DoctrineBlock(
        topic="Impasse Breaking and Dispute Resolution Ladder",
        keywords=["impasse", "deadlock", "mediation", "arbitration", "litigation", "dispute resolution", "BATNA trigger"],
        conclusion_template="Break impasse through process change: add mediator, use arbitration, or escalate to litigation. Choose dispute resolution method based on relationship preservation, cost, and control.",
        reasoning_framework="""
Dispute resolution ladder (increasing formality and cost):
1. Direct negotiation - Parties communicate directly
2. Mediation - Neutral third party facilitates (non-binding)
3. Arbitration - Neutral decides outcome (binding)
4. Litigation - Court imposes decision (public, expensive)

Impasse causes:
- Negative ZOPA (incompatible reservation prices)
- Information asymmetry (hidden information)
- Mistrust (relationship breakdown)
- Principal-agent problems (negotiator lacks authority)
- Reactive devaluation (rejecting ideas from opponent)

Impasse-breaking tactics:
- Change negotiators to reset relationship
- Add mediator to facilitate communication and generate options
- Use single-text procedure (mediator drafts, parties react)
- Make contingent agreements to manage uncertainty
- Agree to arbitration to avoid litigation costs
- Take cooling-off period to reduce emotional escalation

When BATNA is triggered, impasse becomes no-deal outcome.
        """,
        key_factors=["Impasse cause", "relationship value", "dispute costs", "control vs. efficiency", "BATNA attractiveness"],
        primary_authority=["Ury, Brett & Goldberg, Getting Disputes Resolved", "Mnookin, Beyond Winning", "ADR literature"],
        burden_holder="Party preferring agreement to BATNA",
        adversary_position="Strategic impasse to extract concessions",
        counter_arguments=["Mediation preserves relationship", "Arbitration is faster than litigation", "Process change can unlock value"],
        resolution_strategy="Diagnose impasse cause, escalate to mediation or arbitration if negotiation fails",
        entity_scope="Deadlocked negotiations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ADR methods widely used in practice with strong track record",
        controlling_precedent="Getting Disputes Resolved framework"
    ),
    DoctrineBlock(
        topic="Deal Structure and Term Prioritization",
        keywords=["deal structure", "term prioritization", "price vs. terms", "contingent payments", "escrow", "earnout"],
        conclusion_template="Optimize deal structure by prioritizing terms beyond price. Use contingent payments, escrows, and earnouts to bridge valuation gaps and manage risk.",
        reasoning_framework="""
Deal structure encompasses all terms, not just price:
- Payment timing (upfront, installments, contingent)
- Warranties and representations
- Indemnification and liability caps
- Non-compete and exclusivity
- Governance and control rights
- Earn-outs tied to performance
- Escrow for disputed items

Term prioritization matrix:
1. Identify high-value, low-cost terms (trade these)
2. Identify low-value, high-cost terms (concede these)
3. Protect must-have terms (non-negotiable)
4. Create contingent structures for uncertain items

Earnouts bridge valuation gaps:
- Seller believes business worth more (future performance)
- Buyer skeptical (wants proof)
- Earnout = payment contingent on hitting targets
- Aligns incentives and manages risk

Escrows manage post-close disputes:
- Hold portion of purchase price in escrow
- Release after contingencies resolved
- Reduces indemnification enforcement costs
        """,
        key_factors=["Term valuation differentials", "risk tolerance", "information asymmetry", "tax treatment", "enforceability"],
        primary_authority=["M&A structuring literature", "Earnout and escrow practice", "Deal design research"],
        burden_holder="Party bearing risk from uncertain terms",
        adversary_position="Focusing solely on price, ignoring term value",
        counter_arguments=["Terms can be more valuable than price", "Contingent structures manage risk", "Creative structures expand ZOPA"],
        resolution_strategy="Map term priorities, propose contingent structures, trade low-cost for high-value terms",
        entity_scope="Complex transactions with multiple terms",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard practice in M&A and complex commercial deals",
        controlling_precedent="Deal structuring best practices"
    ),
    DoctrineBlock(
        topic="Information Asymmetry and Signaling",
        keywords=["information asymmetry", "signaling", "screening", "adverse selection", "credible commitment", "costly signal"],
        conclusion_template="Manage information asymmetry through signaling (reveal private information credibly) and screening (elicit counterparty information). Use costly signals to establish credibility.",
        reasoning_framework="""
Information asymmetry: One party knows more than the other.
Creates adverse selection (hidden information) and moral hazard (hidden action).

Signaling: Informed party reveals information through credible actions.
Credible signals are costly to fake:
- Warranties backed by escrow (signal quality)
- Due diligence transparency (signal honesty)
- Specific investment in relationship (signal commitment)
- Third-party certification (signal expertise)

Screening: Uninformed party designs mechanisms to elicit information.
Examples:
- Contingent contracts (performance-based payments reveal beliefs)
- Asking for warranties (refusal signals hidden problems)
- Requesting due diligence access (resistance signals issues)

Strategic information revelation:
- Reveal information that strengthens your position
- Withhold information that weakens your position (within legal/ethical bounds)
- Use verifiable information to build trust
- Share priorities (not reservation price) in integrative negotiation

Cheap talk (costless claims) is not credible without backing.
        """,
        key_factors=["Information value", "signal cost", "verification", "legal constraints", "trust level"],
        primary_authority=["Spence, Market Signaling", "Akerlof, The Market for Lemons", "Screening and signaling theory"],
        burden_holder="Uninformed party at risk of adverse selection",
        adversary_position="Exploiting information asymmetry through deception",
        counter_arguments=["Credible signals mitigate asymmetry", "Screening reveals hidden information", "Verification builds trust"],
        resolution_strategy="Use costly signals, design screening mechanisms, verify claims",
        entity_scope="Negotiations with information asymmetry",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Core concept in information economics with strong theoretical foundation",
        controlling_precedent="Spence and Akerlof information asymmetry literature"
    ),
    DoctrineBlock(
        topic="Mnookin Beyond Winning Framework",
        keywords=["mnookin", "beyond winning", "interests", "rights", "power", "empathy", "assertiveness"],
        conclusion_template="Apply Mnookin's framework: balance empathy (understanding counterparty) with assertiveness (advancing own interests). Resolve through interests, rights, or power, in that order.",
        reasoning_framework="""
Mnookin's Beyond Winning emphasizes tension management:
1. Empathy vs. Assertiveness - Understand counterparty while advocating for self
2. Creating value vs. Distributing value - Balance integrative and distributive
3. Principals vs. Agents - Manage principal-agent conflicts

Dispute resolution hierarchy (escalating cost and relationship damage):
1. Interests - Negotiate mutual gain solution (lowest cost, preserves relationship)
2. Rights - Invoke legal/contractual rights (moderate cost, formal)
3. Power - Use coercion or impose costs (highest cost, destroys relationship)

Effective negotiators:
- Lead with interests (explore mutual gain)
- Fall back to rights if interests fail (invoke contract or law)
- Reserve power for last resort (litigation, strikes, walkout)

Empathy without assertiveness = exploitation risk.
Assertiveness without empathy = relationship damage and value left on table.
Balance both to achieve optimal outcomes.
        """,
        key_factors=["Empathy-assertiveness balance", "dispute resolution level", "relationship preservation", "value creation vs. claiming"],
        primary_authority=["Mnookin, Beyond Winning", "Interests-rights-power framework", "Harvard Negotiation Project"],
        burden_holder="Party escalating to rights or power prematurely",
        adversary_position="Defaulting to power tactics without exploring interests",
        counter_arguments=["Interests-based resolution is most efficient", "Rights provide fallback when interests fail", "Power is costly last resort"],
        resolution_strategy="Start with interests, escalate to rights, reserve power for last resort",
        entity_scope="All negotiation and dispute contexts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Influential framework in negotiation pedagogy and practice",
        controlling_precedent="Mnookin Beyond Winning and Harvard Negotiation Project"
    ),
    DoctrineBlock(
        topic="Game Theory Applications in Negotiation",
        keywords=["game theory", "nash equilibrium", "prisoners dilemma", "dominant strategy", "coordination game", "sequential game"],
        conclusion_template="Apply game theory to model strategic interactions. Identify dominant strategies, Nash equilibria, and coordination challenges. Use backward induction in sequential negotiations.",
        reasoning_framework="""
Game theory models strategic interdependence:

Prisoner's Dilemma - Dominant strategy leads to suboptimal outcome
- Both defect is Nash equilibrium (stable but inefficient)
- Cooperation requires trust or repeated interaction
- Relevant to concession dynamics and information sharing

Coordination games - Multiple equilibria, need focal point
- Battle of the Sexes - Parties prefer different outcomes but coordination better than conflict
- Relevant to standard-setting, format choice, jurisdictional selection

Sequential games - Backward induction reveals optimal strategy
- Subgame perfect equilibrium - Credible threats and commitments
- First-mover advantage if commitment is credible
- Relevant to anchoring and ultimatum structures

Key insights:
- Dominant strategy: Best choice regardless of counterparty action
- Nash equilibrium: No incentive to deviate unilaterally
- Commitment devices make threats credible (burn bridges, contractual penalties)
- Repetition enables cooperation through reciprocity and reputation

Model negotiation as game to identify strategic moves and equilibria.
        """,
        key_factors=["Payoff structure", "information completeness", "repetition", "commitment credibility", "equilibrium stability"],
        primary_authority=["Von Neumann & Morgenstern, Theory of Games", "Nash, Equilibrium Points", "Schelling, The Strategy of Conflict"],
        burden_holder="Party making non-credible threats",
        adversary_position="Exploiting coordination failures or defecting in cooperation games",
        counter_arguments=["Game theory identifies equilibria", "Commitment devices enhance credibility", "Repetition sustains cooperation"],
        resolution_strategy="Model interaction as game, identify equilibria, use commitment devices",
        entity_scope="Strategic negotiations with clear payoff structures",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Game theory provides insights but assumes rationality and complete information",
        controlling_precedent="Nash equilibrium and game theory literature"
    ),
    DoctrineBlock(
        topic="Deadline Pressure and Time Tactics",
        keywords=["deadline", "time pressure", "delay tactics", "patience", "time value", "urgency"],
        conclusion_template="Use deadline pressure strategically. Create urgency for counterparty while maintaining patience. Delay when time favors your position; accelerate when it favors counterparty.",
        reasoning_framework="""
Time as negotiating variable:

Deadline effects:
- Concessions cluster near deadlines (pressure to close)
- Party with tighter deadline has less leverage
- Artificial deadlines create urgency (exploding offers)
- Missing deadline can be strategic if BATNA improves over time

Time value asymmetry:
- Fast-moving party has lower discount rate or better outside options
- Patient party can extract concessions by outlasting opponent
- Status quo benefits one party (delay favors that party)

Time tactics:
- Create artificial deadlines (limited-time offers, competitive pressure)
- Delay tactics (request more information, seek approvals, scheduling conflicts)
- Accelerate when time favors you (market moving in your favor, competitor entry)
- Signal patience when you have strong BATNA

Research shows 80% of concessions occur in final 20% of negotiation time.
Plan concession schedule to avoid last-minute panic concessions.
        """,
        key_factors=["Deadline tightness", "time value differential", "BATNA trajectory", "patience capacity", "deadline credibility"],
        primary_authority=["Moore, The Mediation Process", "Time pressure research", "Deadline effects studies"],
        burden_holder="Party facing tighter deadline or higher time costs",
        adversary_position="Exploiting time pressure with delay tactics",
        counter_arguments=["Deadlines can be moved if both parties benefit", "Artificial deadlines lack credibility", "Patient party extracts value"],
        resolution_strategy="Assess time value asymmetry, create or resist deadline pressure strategically",
        entity_scope="Time-sensitive negotiations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-documented deadline effects in negotiation research",
        controlling_precedent="Time pressure and deadline research"
    ),
    DoctrineBlock(
        topic="Cross-Cultural Negotiation Dynamics",
        keywords=["cross-cultural", "culture", "hofstede", "high-context", "low-context", "relationship vs task"],
        conclusion_template="Adapt negotiation style to cultural context. High-context cultures prioritize relationship-building; low-context cultures focus on task efficiency. Individualism vs collectivism affects decision-making.",
        reasoning_framework="""
Hofstede's cultural dimensions:
1. Individualism vs Collectivism - Individual vs group interests
2. Power Distance - Acceptance of hierarchy
3. Uncertainty Avoidance - Tolerance for ambiguity
4. Masculinity vs Femininity - Competition vs cooperation
5. Long-term vs Short-term Orientation - Time horizon

High-context cultures (Asia, Middle East, Latin America):
- Communication is implicit, indirect
- Relationship-building is essential before business
- Group harmony prioritized over individual gain
- Non-verbal cues are critical
- Patience and long-term perspective

Low-context cultures (US, Germany, Scandinavia):
- Communication is explicit, direct
- Task focus, get to business quickly
- Individual accountability and decision-making
- Contracts are detailed and binding
- Efficiency and short-term results

Cultural adaptation strategy:
- Research counterparty's cultural norms
- Invest in relationship-building in high-context cultures
- Be explicit and detailed in low-context cultures
- Use interpreters and cultural advisors
- Avoid assuming your norms are universal
        """,
        key_factors=["Cultural distance", "context level", "power distance", "time orientation", "communication style"],
        primary_authority=["Hofstede, Culture's Consequences", "Hall, Beyond Culture", "Cross-cultural negotiation research"],
        burden_holder="Party negotiating in unfamiliar cultural context",
        adversary_position="Exploiting cultural misunderstandings",
        counter_arguments=["Cultural adaptation builds trust", "Awareness mitigates misunderstandings", "Flexibility enhances outcomes"],
        resolution_strategy="Research culture, adapt style, invest in relationship where appropriate",
        entity_scope="International and cross-cultural negotiations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Hofstede's framework is widely used but has limitations and critics",
        controlling_precedent="Hofstede cultural dimensions and Hall context theory"
    ),
    DoctrineBlock(
        topic="Email and Virtual Negotiation Challenges",
        keywords=["email negotiation", "virtual", "video", "rapport", "miscommunication", "escalation"],
        conclusion_template="Virtual negotiation lacks rapport-building and increases miscommunication risk. Use video for complex issues, reserve email for simple exchanges, and meet face-to-face for high-stakes negotiations.",
        reasoning_framework="""
Virtual negotiation challenges:
1. Reduced rapport - Harder to build trust and read emotions
2. Miscommunication - Tone and intent easily misinterpreted
3. Escalation - Email conflicts escalate faster than face-to-face
4. Coordination - Scheduling and time zones complicate multiparty talks
5. Technology failures - Connectivity issues disrupt flow

Medium richness hierarchy:
- Face-to-face: Richest (body language, tone, immediate feedback)
- Video: High (visual cues, synchronous)
- Phone: Medium (tone, synchronous)
- Email: Leanest (text only, asynchronous)

Best practices:
- Use richer medium for complex or emotional topics
- Build rapport via video before negotiating via email
- Clarify ambiguous emails with phone call
- Avoid negotiating when angry via email (24-hour rule)
- Use shared documents for collaborative drafting
- Test technology before critical meetings

Email advantages: Documentation, time to reflect, asynchronous.
Email risks: Misinterpretation, lack of nuance, escalation.
        """,
        key_factors=["Medium richness", "issue complexity", "relationship stage", "emotional content", "documentation needs"],
        primary_authority=["Thompson, Negotiating via Information Technology", "Media richness theory", "Virtual negotiation research"],
        burden_holder="Party disadvantaged by medium choice",
        adversary_position="Exploiting medium limitations or forcing lean channel",
        counter_arguments=["Rich media builds rapport", "Email enables reflection", "Video balances efficiency and richness"],
        resolution_strategy="Match medium to message complexity, escalate to richer medium when needed",
        entity_scope="Virtual and remote negotiations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Media richness theory supported by research; virtual negotiation best practices emerging",
        controlling_precedent="Media richness theory and virtual negotiation studies"
    ),
    DoctrineBlock(
        topic="Power Dynamics and Leverage Sources",
        keywords=["power", "leverage", "BATNA power", "information power", "positional power", "expert power", "relationship power"],
        conclusion_template="Leverage derives from BATNA strength, information advantage, positional authority, expertise, and relationship value. Build leverage before negotiating; signal power without overplaying.",
        reasoning_framework="""
French & Raven's power bases:
1. Legitimate power - Authority from role or position
2. Reward power - Ability to provide benefits
3. Coercive power - Ability to impose costs
4. Expert power - Specialized knowledge or skill
5. Referent power - Personal charisma or relationship

Negotiation-specific power sources:
- BATNA power: Strong alternatives create leverage (most important)
- Information power: Knowing more than counterparty
- Time power: Ability to wait or impose deadlines
- Coalition power: Allies who support your position
- Precedent power: Prior deals or industry standards

Power dynamics:
- Power is relational and context-dependent
- Overplaying power invites retaliation
- Weak party can build coalitions or improve BATNA
- Power imbalance doesn't guarantee outcome (weak can resist)

Building leverage:
- Improve BATNA before negotiating
- Gather information about counterparty
- Build coalitions and alliances
- Establish expertise and credibility
- Create dependence (make yourself valuable)
        """,
        key_factors=["BATNA strength", "information asymmetry", "positional authority", "expertise", "relationship dependence"],
        primary_authority=["French & Raven, Bases of Social Power", "Pfeffer, Managing with Power", "Power in negotiation research"],
        burden_holder="Party with less leverage",
        adversary_position="Exploiting power imbalance coercively",
        counter_arguments=["Power is multi-dimensional", "Weak can build coalitions", "Overuse of power invites resistance"],
        resolution_strategy="Build BATNA, gather information, form coalitions, establish expertise",
        entity_scope="All negotiations with power differentials",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Power theories well-established in social psychology and negotiation",
        controlling_precedent="French & Raven power bases framework"
    ),
    DoctrineBlock(
        topic="Reactive Devaluation and Psychological Biases",
        keywords=["reactive devaluation", "bias", "loss aversion", "status quo bias", "confirmation bias", "overconfidence"],
        conclusion_template="Counteract psychological biases: reactive devaluation (rejecting opponent's ideas), loss aversion (overvaluing what you have), overconfidence (underestimating counterparty). Use framing and process to mitigate biases.",
        reasoning_framework="""
Key negotiation biases:

Reactive devaluation - Proposals from opponent are valued less than identical proposals from neutral source.
Mitigation: Use third-party mediator, attribute idea to neutral source, let counterparty propose your idea.

Loss aversion - Losses loom larger than equivalent gains (endowment effect).
Mitigation: Frame concessions as gains not losses, use reference points strategically.

Status quo bias - Preference for current state over change.
Mitigation: Highlight costs of status quo, create sense of urgency, default to new option.

Anchoring - Over-reliance on first piece of information.
Mitigation: Counter-anchor, use objective criteria, ignore unreasonable anchors.

Overconfidence - Overestimating own position and underestimating counterparty.
Mitigation: Seek disconfirming evidence, model counterparty perspective, use advisors.

Confirmation bias - Seeking information that confirms beliefs.
Mitigation: Actively seek disconfirming evidence, consider alternative interpretations.

Framing effects - Presentation affects decisions (gain vs loss framing).
Mitigation: Reframe to highlight opportunities not threats.
        """,
        key_factors=["Bias awareness", "framing", "reference points", "process design", "third-party involvement"],
        primary_authority=["Kahneman & Tversky, Prospect Theory", "Ross & Stillinger, Reactive Devaluation", "Bazerman & Neale, Negotiating Rationally"],
        burden_holder="Party falling victim to biases",
        adversary_position="Exploiting counterparty biases",
        counter_arguments=["Awareness reduces bias impact", "Process design mitigates biases", "Framing can be reframed"],
        resolution_strategy="Identify biases, reframe issues, use third parties, seek disconfirming evidence",
        entity_scope="All negotiations subject to psychological biases",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Biases well-documented in behavioral economics; mitigation strategies have empirical support",
        controlling_precedent="Kahneman & Tversky behavioral economics and negotiation bias research"
    ),
    DoctrineBlock(
        topic="Negotiating with Agents and Principals",
        keywords=["agent", "principal", "authority", "ratification", "good cop bad cop", "limited authority"],
        conclusion_template="When negotiating with agents, clarify authority limits, seek direct principal access for key issues, and beware good cop/bad cop tactics. Agents have incentive conflicts with principals.",
        reasoning_framework="""
Principal-agent problem:
- Principal owns the problem; agent represents principal
- Agent's incentives may diverge from principal's (fee structure, risk aversion)
- Agent may lack full authority (limited mandate)
- Agent may use principal as ratification barrier ("I have to check with my client")

Agent negotiation tactics:
- Limited authority - "I can't agree to that without approval" (creates delay)
- Good cop/bad cop - Agent is reasonable, principal is difficult
- Commission incentives - Agent wants deal closed quickly (may accept suboptimal terms)
- Phantom principal - Agent claims principal won't accept terms

Strategies when facing agent:
- Clarify agent's authority at outset
- Request direct access to principal for major issues
- Understand agent's incentive structure
- Make proposals contingent on principal ratification
- Bypass agent if authority is too limited

Strategies when using agent:
- Give clear mandate with reservation price
- Allow agent flexibility within bounds
- Use agent as buffer (limited authority tactic)
- Monitor for agent incentive conflicts
        """,
        key_factors=["Authority scope", "incentive alignment", "ratification requirements", "access to principal", "agent expertise"],
        primary_authority=["Jensen & Meckling, Theory of the Firm", "Principal-agent theory", "Agency in negotiation research"],
        burden_holder="Party negotiating with agent lacking authority",
        adversary_position="Agent exploiting limited authority or phantom principal",
        counter_arguments=["Agents can facilitate deals", "Limited authority is legitimate", "Direct principal access for key issues"],
        resolution_strategy="Clarify authority, request principal access, understand incentives, make ratification-contingent offers",
        entity_scope="Negotiations involving representatives or agents",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Principal-agent theory well-established; tactics recognized in practice",
        controlling_precedent="Principal-agent theory and agency research"
    ),
    DoctrineBlock(
        topic="Contingent Contracts and Risk Management",
        keywords=["contingent contract", "earnout", "performance-based", "risk allocation", "uncertainty", "beliefs"],
        conclusion_template="Use contingent contracts to bridge differences in beliefs about uncertain future events. Earnouts, performance payments, and contingent terms allocate risk and align incentives.",
        reasoning_framework="""
Contingent contract = Payment or terms depend on future outcome.

Applications:
- Earnouts in M&A - Future payments based on performance metrics
- Performance-based compensation - Bonuses tied to results
- Risk-sharing agreements - Costs/profits allocated by outcome
- Warranties and indemnities - Liability contingent on defects

When to use:
- Parties disagree on uncertain future event (valuation, market, performance)
- Information asymmetry about quality or capability
- Risk allocation needs (transfer risk to party better able to bear it)

Contingent contract benefits:
- Bridges valuation gaps without concessions
- Aligns incentives (both benefit if optimistic scenario materializes)
- Manages moral hazard (seller stays engaged post-deal)
- Creates value through risk reallocation

Design considerations:
- Metrics must be objective and verifiable
- Avoid gaming (manipulation of metrics)
- Set caps and floors to bound risk
- Specify measurement and dispute resolution
- Consider tax and accounting treatment

Contingent contracts expand ZOPA when parties have different beliefs.
        """,
        key_factors=["Uncertainty magnitude", "belief divergence", "metric verifiability", "gaming risk", "risk tolerance"],
        primary_authority=["Bazerman & Gillespie, Betting on the Future", "Earnout design literature", "Contingent contract research"],
        burden_holder="Party bearing downside risk from contingent terms",
        adversary_position="Proposing unverifiable or gameable contingent metrics",
        counter_arguments=["Contingent contracts create value", "Risk allocation is efficient", "Metrics can be designed to resist gaming"],
        resolution_strategy="Propose contingent structures for uncertain items, ensure metrics are objective and verifiable",
        entity_scope="Negotiations with uncertainty about future events",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Contingent contracts widely used in practice with strong theoretical foundation",
        controlling_precedent="Earnout and contingent contract design research"
    ),
    DoctrineBlock(
        topic="Post-Settlement Settlement and Continuous Improvement",
        keywords=["post-settlement settlement", "PSS", "joint improvement", "value creation", "mediator proposal"],
        conclusion_template="After reaching agreement, propose post-settlement settlement (PSS) to find mutually preferred deal. PSS reveals Pareto improvements without risk since original deal is fallback.",
        reasoning_framework="""
Post-Settlement Settlement (PSS):
Raiffa's concept - After parties agree, third party (or parties themselves) seeks better deal.

PSS procedure:
1. Parties reach initial agreement (fallback position)
2. Mediator or facilitator proposes alternative deal
3. New deal is adopted only if both parties prefer it to original
4. If either rejects, original deal stands (no risk)

PSS benefits:
- Reveals Pareto improvements (makes at least one party better off without harming other)
- Overcomes anchoring to initial agreement
- Reduces strategic posturing (since deal is already secured)
- Demonstrates joint problem-solving

When to use PSS:
- Complex multi-issue negotiations with many options
- Parties have reached acceptable but suboptimal agreement
- Relationship allows for post-deal collaboration
- Third party has expertise to identify improvements

PSS is low-risk value creation - worst case is status quo.
Parties are more forthcoming about interests after deal is secured.

Related: Continuous improvement in ongoing relationships (renegotiation clauses).
        """,
        key_factors=["Pareto improvement potential", "relationship quality", "third-party expertise", "deal complexity"],
        primary_authority=["Raiffa, Post-Settlement Settlements", "Pareto efficiency", "Value creation research"],
        burden_holder="Party satisfied with initial agreement (may resist PSS exploration)",
        adversary_position="Rejecting PSS to protect initial favorable terms",
        counter_arguments=["PSS is risk-free (fallback to original deal)", "Reveals joint gains", "Builds relationship"],
        resolution_strategy="Propose PSS after agreement, use neutral facilitator, emphasize no-risk nature",
        entity_scope="Complex negotiations with multiple issues",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="PSS is theoretically sound but adoption is limited in practice",
        controlling_precedent="Raiffa's PSS concept and Pareto improvement theory"
    ),
    DoctrineBlock(
        topic="Negotiation Ethics and Deception",
        keywords=["ethics", "deception", "lying", "bluffing", "misrepresentation", "fiduciary duty", "disclosure"],
        conclusion_template="Distinguish legal bluffing (puffery, negotiation posturing) from illegal misrepresentation (material false statements). Fiduciary relationships impose higher disclosure duties. Reputation effects constrain deception.",
        reasoning_framework="""
Negotiation ethics spectrum:
1. Full disclosure - Reveal all information (rarely required)
2. Truthful but incomplete - Answer honestly, don't volunteer (standard)
3. Puffery - Exaggeration of value (legal, "this is a great deal")
4. Bluffing - Misrepresenting BATNA or reservation price (common, ethically debated)
5. Material misrepresentation - False statements about facts (illegal, tortious)
6. Fraud - Intentional deception for gain (criminal)

Legal standards:
- No duty to disclose unless fiduciary relationship, latent defect, or statute requires
- Misrepresentation of material fact is fraud (not opinion or puffery)
- Active concealment (hiding defects) is more culpable than passive nondisclosure

Fiduciary duties (higher standard):
- Lawyers to clients, agents to principals, trustees to beneficiaries
- Duty of candor, loyalty, full disclosure
- Cannot prioritize self-interest over principal

Ethical considerations:
- Reputation - Deception damages long-term relationships and reputation
- Reciprocity - Lying invites retaliation
- Norms - Industry and cultural norms vary
- Conscience - Personal moral standards

Most negotiators accept bluffing about reservation price but condemn lying about facts.
        """,
        key_factors=["Legal constraints", "fiduciary duties", "reputation effects", "relationship value", "industry norms"],
        primary_authority=["Model Rules of Professional Conduct (lawyers)", "Restatement of Contracts (misrepresentation)", "Negotiation ethics research"],
        burden_holder="Party relying on counterparty's representations",
        adversary_position="Material misrepresentation or fraud",
        counter_arguments=["Bluffing is standard practice", "No duty to disclose BATNA", "Reputation constrains deception"],
        resolution_strategy="Distinguish bluffing from fraud, verify material facts, build reputation for honesty",
        entity_scope="All negotiations with ethical considerations",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="Legal standards clear for fraud; ethical standards for bluffing debated",
        controlling_precedent="Fraud and misrepresentation law; legal ethics rules"
    ),
    DoctrineBlock(
        topic="Internal Alignment and Stakeholder Management",
        keywords=["internal alignment", "stakeholder", "constituency", "coalition", "mandate", "buy-in"],
        conclusion_template="Secure internal alignment before external negotiation. Identify stakeholders, build internal coalition, clarify mandate, and manage constituency pressure. Internal conflict undermines external bargaining power.",
        reasoning_framework="""
Internal negotiation precedes external negotiation:

Stakeholder mapping:
- Identify all parties with interest in outcome
- Assess each stakeholder's interests, power, and influence
- Distinguish decision-makers from influencers

Building internal coalition:
- Secure buy-in from key stakeholders
- Address concerns and objections proactively
- Create consensus on mandate and reservation price
- Identify spokesperson and decision authority

Constituency pressure:
- Principals may pressure agents to get "better deal"
- Negotiator must manage expectations
- Irrational constituency demands weaken position
- Use constituency as ratification barrier (tactic)

Risks of internal misalignment:
- Mixed messages to counterparty
- Inability to commit credibly
- Post-deal ratification failure
- Negotiator disempowerment

Best practices:
- Clarify authority and mandate upfront
- Keep stakeholders informed during negotiation
- Manage expectations about realistic outcomes
- Secure provisional agreement before final commitment
        """,
        key_factors=["Stakeholder power", "coalition stability", "mandate clarity", "constituency rationality", "communication"],
        primary_authority=["Lax & Sebenius, 3-D Negotiation", "Internal negotiation research", "Stakeholder management literature"],
        burden_holder="Negotiator caught between constituency and counterparty",
        adversary_position="Exploiting internal divisions or irrational constituency",
        counter_arguments=["Internal alignment is prerequisite", "Coalition-building is rational", "Manage expectations to avoid ratification failure"],
        resolution_strategy="Map stakeholders, build coalition, clarify mandate, manage expectations",
        entity_scope="Negotiations with multiple internal stakeholders",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Internal alignment recognized as critical in multi-stakeholder negotiations",
        controlling_precedent="3-D Negotiation and stakeholder management frameworks"
    ),
    DoctrineBlock(
        topic="Gender and Diversity in Negotiation",
        keywords=["gender", "diversity", "stereotypes", "backlash", "communal", "agentic", "bias"],
        conclusion_template="Gender and diversity affect negotiation through stereotypes and social expectations. Women face backlash for assertive tactics; mitigation strategies include framing, agents, and communal justification.",
        reasoning_framework="""
Gender differences in negotiation:
- Women ask less often and accept initial offers more (on average)
- Women face backlash for assertive negotiation (violates communal stereotype)
- Women negotiate as effectively as men when representing others
- Ambiguous situations (no clear norms) amplify gender gaps

Backlash effect:
- Assertive women perceived as aggressive, unlikeable
- Communal women perceived as weak negotiators
- Double bind - penalized for being too assertive or too communal

Mitigation strategies:
- Frame requests in communal terms ("This will help the team")
- Use agents or representatives (avoids backlash)
- Anchor to objective criteria (reduces bias)
- Signal competence and warmth simultaneously
- Negotiate on behalf of others (legitimizes advocacy)

Diversity considerations:
- Minority negotiators face stereotypes and bias
- Homogeneous teams miss diverse perspectives (groupthink)
- Diverse teams generate more creative options (if managed well)

Research shows awareness of bias and countermeasures reduce disparities.
        """,
        key_factors=["Gender stereotypes", "backlash risk", "framing", "agent use", "diversity effects"],
        primary_authority=["Bowles & Babcock, Women Don't Ask", "Amanatullah & Morris, Backlash Effect", "Gender in negotiation research"],
        burden_holder="Women and minorities facing stereotype-based bias",
        adversary_position="Exploiting or perpetuating gender/diversity biases",
        counter_arguments=["Framing mitigates backlash", "Objective criteria reduce bias", "Agents avoid personal backlash"],
        resolution_strategy="Frame communally, use agents, anchor to criteria, signal competence and warmth",
        entity_scope="Negotiations involving gender and diversity dynamics",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="Gender effects documented but mitigation strategies require further research",
        controlling_precedent="Gender and diversity in negotiation research"
    ),
    DoctrineBlock(
        topic="Relationship vs Transaction Focus",
        keywords=["relationship", "transaction", "one-shot", "repeat dealing", "reputation", "long-term"],
        conclusion_template="Balance relationship preservation with value claiming based on context. Prioritize relationship in repeat dealings; use distributive tactics in one-shot transactions. Reputation effects matter even in one-shot games.",
        reasoning_framework="""
Transaction vs. relationship continuum:

One-shot transaction:
- No future interaction expected
- Relationship has minimal value
- Distributive tactics more acceptable
- Example: One-time purchase from stranger

Repeat dealing:
- Ongoing relationship expected
- Relationship value exceeds single transaction
- Integrative approach essential
- Reputation and reciprocity constrain behavior
- Example: Vendor contracts, employment, partnerships

Relationship strategies:
- Invest in rapport and trust-building
- Share information to create value
- Make small concessions to preserve relationship
- Avoid extreme distributive tactics
- Prioritize long-term over short-term gains

Transaction strategies:
- Focus on value claiming
- Use anchoring and concession tactics
- Less information sharing
- Relationship is not constraint

Even in one-shot games, reputation effects matter:
- Word-of-mouth spreads (online reviews, industry networks)
- Counterparty may have ties to your future partners
- Ethical reputation affects opportunities

Default to relationship-preserving approach unless clearly one-shot.
        """,
        key_factors=["Relationship value", "repetition likelihood", "reputation effects", "network connectivity", "time horizon"],
        primary_authority=["Axelrod, The Evolution of Cooperation", "Repeat game theory", "Relationship vs transaction research"],
        burden_holder="Party prioritizing short-term transaction over long-term relationship",
        adversary_position="Exploiting relationship value to extract concessions",
        counter_arguments=["Relationship value justifies concessions", "Reputation matters even in one-shot", "Integrative approach builds trust"],
        resolution_strategy="Assess relationship value, adapt tactics to context, preserve reputation",
        entity_scope="All negotiations with varying relationship contexts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Transaction vs relationship trade-off well-established in negotiation theory",
        controlling_precedent="Repeat game theory and relationship negotiation research"
    ),
]

# Global State
class EngineState:
    def __init__(self):
        self.start_time = time.time()
        self.total_queries = 0
        self.cache_hits = 0
        self.total_latency_ms = 0.0
        self.doctrines_triggered: Set[str] = set()
        self.coverage_map: Dict[str, int] = {d.topic: 0 for d in DOCTRINE_CACHE}
        self.error_log: List[Dict[str, Any]] = []

STATE = EngineState()

# Core Functions
def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[str], ConfidenceLevel]:
    """Three-layer TIE response: cache -> semantic -> deep."""
    start = time.time()

    # Layer 1: Doctrine Cache
    triggered = []
    query_lower = query.lower()
    for doctrine in DOCTRINE_CACHE:
        if any(kw in query_lower for kw in doctrine.keywords):
            triggered.append(doctrine)
            STATE.coverage_map[doctrine.topic] += 1

    if triggered:
        STATE.cache_hits += 1
        latency = (time.time() - start) * 1000
        STATE.total_latency_ms += latency

        # Synthesize response
        response = _synthesize_doctrine_response(triggered, mode, zone)
        confidence = _calculate_confidence(triggered)
        return response, [d.topic for d in triggered], confidence

    # Layer 2: Semantic retrieval (fallback - simplified)
    response = _semantic_fallback(query, mode, zone)
    latency = (time.time() - start) * 1000
    STATE.total_latency_ms += latency
    return response, [], ConfidenceLevel.DISCLOSURE

def _synthesize_doctrine_response(doctrines: List[DoctrineBlock], mode: ResponseMode, zone: AnalysisZone) -> str:
    """Synthesize multi-doctrine response."""
    if mode == ResponseMode.FAST:
        return " ".join([d.conclusion_template for d in doctrines[:2]])

    # DEFENSE or MEMO mode
    parts = []
    for d in doctrines:
        parts.append(f"**{d.topic}**")
        parts.append(d.conclusion_template)
        if mode == ResponseMode.MEMO:
            parts.append(f"\n_Reasoning:_ {d.reasoning_framework[:300]}...")
            parts.append(f"\n_Authority:_ {', '.join(d.primary_authority)}")

    return "\n\n".join(parts)

def _calculate_confidence(doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
    """Calculate aggregate confidence from triggered doctrines."""
    if not doctrines:
        return ConfidenceLevel.DISCLOSURE

    # Use most conservative confidence
    levels = [d.confidence for d in doctrines]
    if ConfidenceLevel.HIGH_RISK in levels:
        return ConfidenceLevel.HIGH_RISK
    if ConfidenceLevel.DISCLOSURE in levels:
        return ConfidenceLevel.DISCLOSURE
    if ConfidenceLevel.AGGRESSIVE in levels:
        return ConfidenceLevel.AGGRESSIVE
    return ConfidenceLevel.DEFENSIBLE

def _semantic_fallback(query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
    """Semantic search fallback when cache misses."""
    return f"No direct doctrine match for query. Consider: BATNA analysis, ZOPA identification, and principled negotiation framework. Consult negotiation specialist for detailed strategy."

def determinism_hash(data: str) -> str:
    """Generate SHA-256 hash for determinism verification."""
    return hashlib.sha256(data.encode()).hexdigest()

def log_audit_trail(query_id: str, query: str, response: str, mode: str, doctrines: List[str]):
    """Append-only JSONL audit log."""
    record = {
        "query_id": query_id,
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "response": response,
        "mode": mode,
        "doctrines": doctrines
    }
    logger.info(json.dumps(record))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events."""
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    yield
    logger.info(f"{ENGINE_NAME} shutting down. Total queries: {STATE.total_queries}")

# FastAPI App
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

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    """Main query endpoint."""
    query_id = str(uuid.uuid4())
    start = time.time()

    try:
        response, doctrines, confidence = three_layer_response(req.query, req.mode, req.zone)
        latency = (time.time() - start) * 1000

        STATE.total_queries += 1
        hash_val = determinism_hash(response)

        telemetry = TelemetryData(
            query_id=query_id,
            timestamp=datetime.utcnow().isoformat(),
            latency_ms=latency,
            mode=req.mode.value,
            cache_hit=len(doctrines) > 0,
            doctrines_triggered=doctrines,
            confidence=confidence.value
        )

        log_audit_trail(query_id, req.query, response, req.mode.value, doctrines)

        return QueryResponse(
            query_id=query_id,
            response=response,
            mode=req.mode.value,
            confidence=confidence.value,
            doctrines_applied=doctrines,
            telemetry=telemetry,
            determinism_hash=hash_val,
            zone=req.zone.value
        )
    except Exception as e:
        logger.error(f"Query {query_id} failed: {e}")
        STATE.error_log.append({"query_id": query_id, "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health endpoint."""
    uptime = time.time() - STATE.start_time
    cache_rate = (STATE.cache_hits / STATE.total_queries * 100) if STATE.total_queries > 0 else 0.0
    avg_latency = STATE.total_latency_ms / STATE.total_queries if STATE.total_queries > 0 else 0.0

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        engine_name=ENGINE_NAME,
        version=VERSION,
        uptime_seconds=uptime,
        total_queries=STATE.total_queries,
        cache_hit_rate=cache_rate,
        avg_latency_ms=avg_latency,
        doctrines_loaded=len(DOCTRINE_CACHE)
    )

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics."""
    return {"doctrines": [d.topic for d in DOCTRINE_CACHE]}

@app.get("/coverage")
async def doctrine_coverage():
    """Doctrine coverage map."""
    return {"coverage": STATE.coverage_map}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
