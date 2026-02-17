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
        topic="Getting to Yes - Principled Negotiation Framework",
        keywords=["principled negotiation", "interest-based", "mutual gain", "objective criteria", "separating people from problem"],
        conclusion_template="Apply principled negotiation to achieve mutual gains and resolve disputes by focusing on interests, not positions.",
        reasoning_framework="""
Principled negotiation, as articulated by Fisher, Ury, and Patton, emphasizes four core tenets: (1) separating the people from the problem, (2) focusing on interests rather than positions, (3) generating options for mutual gain, and (4) insisting on objective criteria. Negotiators should identify underlying interests, avoid positional bargaining, and collaboratively develop creative solutions. Objective standards, such as market value or legal precedent, anchor the process. The framework is designed to reduce adversarial tension and foster durable agreements, even in complex or multiparty contexts. It is particularly effective where ongoing relationships are valued and parties are motivated to avoid impasse or escalation. The approach requires preparation, active listening, and a willingness to explore alternatives beyond initial demands.
""",
        key_factors=["Interests vs Positions", "Objective Criteria", "Mutual Gains", "Communication", "Relationship Management"],
        primary_authority=["Fisher, Ury & Patton, Getting to Yes"],
        burden_holder="Both parties",
        adversary_position="Positional bargaining; adversarial tactics",
        counter_arguments=[
            "Principled negotiation may be perceived as weak by competitive negotiators",
            "Not all parties are willing to disclose interests",
            "Objective criteria may be contested"
        ],
        resolution_strategy="Reframe negotiation around interests; propose objective standards; facilitate joint problem-solving",
        entity_scope="Individuals, teams, organizations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Getting to Yes (1981)"
    ),
    DoctrineBlock(
        topic="BATNA Analysis and Reservation Price",
        keywords=["BATNA", "Best Alternative", "reservation price", "walk-away", "negotiation threshold"],
        conclusion_template="Determine BATNA and reservation price to establish negotiation boundaries and leverage.",
        reasoning_framework="""
BATNA (Best Alternative to a Negotiated Agreement) is the foundational concept for establishing leverage and negotiation boundaries. Parties must rigorously assess their alternatives outside the current negotiation and quantify their reservation price—the minimum acceptable outcome. The BATNA provides a benchmark against which all proposals are measured; if an offer is inferior to the BATNA, it should be rejected. Accurate BATNA analysis requires objective evaluation of alternatives, risk assessment, and consideration of timing and costs. Reservation price is set based on BATNA, but may be adjusted for strategic reasons, such as relationship value or reputational concerns. Disclosing BATNA can be a tactical decision, potentially influencing the other party's behavior.
""",
        key_factors=["Alternative Options", "Reservation Price", "Leverage", "Risk Assessment", "Disclosure Strategy"],
        primary_authority=["Fisher, Ury & Patton", "Harvard Negotiation Project"],
        burden_holder="Each party",
        adversary_position="Overstating BATNA; bluffing; refusing to disclose reservation price",
        counter_arguments=[
            "BATNA may be misestimated",
            "Reservation price can be manipulated",
            "Disclosure may weaken bargaining position"
        ],
        resolution_strategy="Conduct thorough BATNA analysis; set clear reservation price; use BATNA as negotiation anchor",
        entity_scope="Individuals, organizations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Getting to Yes; Harvard Negotiation Project"
    ),
    DoctrineBlock(
        topic="ZOPA - Zone of Possible Agreement",
        keywords=["ZOPA", "agreement zone", "overlap", "negotiation range", "deal feasibility"],
        conclusion_template="Identify ZOPA to determine if a deal is possible and to guide negotiation strategy.",
        reasoning_framework="""
ZOPA (Zone of Possible Agreement) is the range between parties' reservation prices where a deal is feasible. Negotiators must estimate both their own and the counterpart's reservation price to assess whether ZOPA exists. If no overlap is found, negotiation may result in impasse. ZOPA analysis informs concession patterns, anchoring, and deal structure. Accurate ZOPA estimation requires information gathering, probing, and sometimes signaling. The existence and width of ZOPA influence negotiation dynamics, including competitive vs collaborative approaches. Parties may use tactics to expand ZOPA, such as adding value or adjusting terms.
""",
        key_factors=["Reservation Prices", "Information Gathering", "Deal Structure", "Concessions", "Value Creation"],
        primary_authority=["Fisher, Ury & Patton", "Raiffa, Negotiation Analysis"],
        burden_holder="Both parties",
        adversary_position="Withholding reservation price; misrepresenting ZOPA; refusing to negotiate",
        counter_arguments=[
            "ZOPA may be miscalculated",
            "Information asymmetry can obscure ZOPA",
            "Parties may manipulate perceived ZOPA"
        ],
        resolution_strategy="Probe for reservation prices; use objective criteria; expand ZOPA through creative options",
        entity_scope="Individuals, organizations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Negotiation Analysis (Raiffa, 2002)"
    ),
    DoctrineBlock(
        topic="Anchoring and Adjustment Heuristic",
        keywords=["anchoring", "first offer", "adjustment", "cognitive bias", "negotiation psychology"],
        conclusion_template="Leverage anchoring and adjustment to influence negotiation outcomes and counteract bias.",
        reasoning_framework="""
Anchoring refers to the cognitive bias where the first offer sets a reference point, influencing subsequent negotiation moves. Adjustment occurs as parties move away from the anchor, but often insufficiently. Skilled negotiators use anchoring to shape expectations and outcomes, making aggressive or strategic first offers. Counterparties must recognize anchoring effects and counteract them by preparing objective standards and counter-anchors. The heuristic is particularly impactful in distributive negotiations, where price or value is the primary concern. Awareness of anchoring bias is critical to avoid suboptimal agreements.
""",
        key_factors=["First Offer", "Reference Point", "Counter-anchoring", "Objective Criteria", "Bias Awareness"],
        primary_authority=["Tversky & Kahneman", "Bazerman & Neale"],
        burden_holder="Party making first offer",
        adversary_position="Rejecting anchor; counter-anchoring; ignoring objective standards",
        counter_arguments=[
            "Anchoring may be perceived as manipulative",
            "Counterparty may ignore anchor",
            "Objective criteria may override anchors"
        ],
        resolution_strategy="Prepare objective counter-anchors; educate parties on bias; use anchoring strategically",
        entity_scope="Individuals, teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Judgment under Uncertainty (Tversky & Kahneman, 1974)"
    ),
    DoctrineBlock(
        topic="Concession Strategy and Pattern",
        keywords=["concessions", "pattern", "reciprocity", "negotiation tactics", "incremental movement"],
        conclusion_template="Design concession patterns to signal intent, build reciprocity, and reach agreement.",
        reasoning_framework="""
Concession strategy involves planned, incremental movements in negotiation positions to signal flexibility and encourage reciprocity. Effective negotiators use concessions to communicate priorities, test counterpart's willingness, and build momentum toward agreement. Patterns may be symmetric, asymmetric, or conditional, depending on negotiation context. Excessive or premature concessions can undermine leverage, while rigid positions may lead to impasse. Concession tracking and signaling are essential, especially in multiparty or complex negotiations. Strategic concessions can be used to unlock ZOPA or break deadlocks.
""",
        key_factors=["Concession Size", "Timing", "Reciprocity", "Signaling", "Leverage"],
        primary_authority=["Lewicki, Saunders & Barry", "Fisher, Ury & Patton"],
        burden_holder="Party seeking agreement",
        adversary_position="Refusing to reciprocate; demanding excessive concessions; rigid positions",
        counter_arguments=[
            "Concessions may signal weakness",
            "Pattern may be misinterpreted",
            "Reciprocity may not be honored"
        ],
        resolution_strategy="Track concessions; use conditional offers; communicate intent clearly",
        entity_scope="Individuals, teams, organizations",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation (Lewicki et al., 2015)"
    ),
    DoctrineBlock(
        topic="Integrative (Win-Win) Negotiation",
        keywords=["integrative", "win-win", "value creation", "collaboration", "joint problem-solving"],
        conclusion_template="Apply integrative negotiation to maximize value and foster durable agreements.",
        reasoning_framework="""
Integrative negotiation seeks to expand the pie by identifying shared interests and creating value for all parties. Techniques include joint brainstorming, information sharing, and exploring creative options. The process is collaborative, emphasizing relationship-building and trust. Integrative strategies are most effective when parties have ongoing relationships or multiple issues to negotiate. Barriers include information asymmetry, lack of trust, and competitive mindsets. Facilitators may use structured frameworks, such as interest mapping or option generation, to guide parties toward win-win outcomes.
""",
        key_factors=["Shared Interests", "Value Creation", "Trust", "Information Sharing", "Option Generation"],
        primary_authority=["Fisher, Ury & Patton", "Lax & Sebenius"],
        burden_holder="Both parties",
        adversary_position="Competitive negotiation; withholding information; zero-sum mindset",
        counter_arguments=[
            "Integrative approach may be exploited by competitive parties",
            "Trust may be lacking",
            "Value creation may not be possible"
        ],
        resolution_strategy="Build trust; facilitate information sharing; use structured option generation",
        entity_scope="Individuals, teams, organizations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="The Manager as Negotiator (Lax & Sebenius, 1986)"
    ),
    DoctrineBlock(
        topic="Distributive (Win-Lose) Negotiation",
        keywords=["distributive", "win-lose", "zero-sum", "competitive", "claiming value"],
        conclusion_template="Use distributive negotiation tactics to claim value in zero-sum contexts.",
        reasoning_framework="""
Distributive negotiation is characterized by competitive tactics aimed at claiming value from a fixed pie. Strategies include aggressive anchoring, bluffing, and tactical concessions. The approach is appropriate when parties have opposing interests and no ongoing relationship. Preparation involves identifying reservation price, BATNA, and potential leverage points. Risks include damaging relationships, escalation, and impasse. Distributive tactics should be balanced with ethical considerations and awareness of potential long-term consequences.
""",
        key_factors=["Reservation Price", "BATNA", "Leverage", "Competitive Tactics", "Ethical Boundaries"],
        primary_authority=["Lewicki, Saunders & Barry", "Bazerman & Neale"],
        burden_holder="Party seeking maximum value",
        adversary_position="Collaborative negotiation; integrative tactics; relationship focus",
        counter_arguments=[
            "Distributive tactics may damage relationships",
            "Aggressive negotiation may lead to impasse",
            "Ethical boundaries may be crossed"
        ],
        resolution_strategy="Prepare thoroughly; use competitive tactics judiciously; monitor ethical boundaries",
        entity_scope="Individuals, organizations",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation (Lewicki et al., 2015)"
    ),
    DoctrineBlock(
        topic="Multiparty Negotiation Dynamics",
        keywords=["multiparty", "coalitions", "complexity", "agenda control", "group negotiation"],
        conclusion_template="Manage multiparty dynamics by building coalitions, controlling agenda, and facilitating consensus.",
        reasoning_framework="""
Multiparty negotiations introduce complexity due to multiple interests, shifting coalitions, and agenda control. Effective management requires mapping stakeholder interests, identifying potential allies, and anticipating coalition formation. Facilitators may use structured processes, such as caucusing or sequential issue resolution, to guide parties. Agenda control is critical to prevent manipulation and ensure fair participation. Consensus-building techniques, such as majority voting or unanimity requirements, may be employed. Risks include fragmentation, deadlock, and exclusion of minority voices.
""",
        key_factors=["Stakeholder Mapping", "Coalition Formation", "Agenda Control", "Consensus Building", "Process Facilitation"],
        primary_authority=["Susskind & Cruikshank", "Raiffa"],
        burden_holder="Facilitator/lead negotiator",
        adversary_position="Manipulating agenda; forming exclusive coalitions; blocking consensus",
        counter_arguments=[
            "Coalitions may be unstable",
            "Agenda control may be contested",
            "Consensus may be difficult to achieve"
        ],
        resolution_strategy="Use structured facilitation; map interests; build inclusive coalitions",
        entity_scope="Teams, organizations, governments",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Breaking the Impasse (Susskind & Cruikshank, 1987)"
    ),
    DoctrineBlock(
        topic="Impasse Breaking and Dispute Resolution Ladder",
        keywords=["impasse", "deadlock", "dispute resolution", "ladder", "mediation", "arbitration"],
        conclusion_template="Apply dispute resolution ladder to break impasse and escalate appropriately.",
        reasoning_framework="""
When negotiations reach impasse, parties should escalate through a dispute resolution ladder: (1) direct negotiation, (2) facilitated negotiation, (3) mediation, (4) arbitration, (5) litigation. Each step increases formality and cost, but may be necessary to resolve deadlock. The ladder approach encourages parties to exhaust informal methods before resorting to binding processes. Facilitators and mediators help reframe issues, identify interests, and propose creative solutions. Arbitration and litigation provide finality but may damage relationships and incur significant costs.
""",
        key_factors=["Impasse Identification", "Escalation Steps", "Facilitation", "Mediation", "Arbitration"],
        primary_authority=["Mnookin", "Susskind & Cruikshank"],
        burden_holder="Party seeking resolution",
        adversary_position="Refusing escalation; blocking mediation; insisting on litigation",
        counter_arguments=[
            "Escalation may increase costs",
            "Mediation may not resolve impasse",
            "Arbitration/litigation may damage relationships"
        ],
        resolution_strategy="Exhaust informal methods; use structured escalation; select appropriate dispute resolution mechanism",
        entity_scope="Individuals, organizations, governments",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Beyond Winning (Mnookin et al., 2000)"
    ),
    DoctrineBlock(
        topic="Deal Structure and Term Prioritization",
        keywords=["deal structure", "term prioritization", "negotiation package", "trade-offs", "multi-issue"],
        conclusion_template="Structure deals by prioritizing terms and leveraging trade-offs across issues.",
        reasoning_framework="""
Complex negotiations often involve multiple terms and issues. Effective deal structuring requires prioritizing terms based on importance, flexibility, and value. Parties may use package deals, conditional offers, and trade-offs to maximize outcomes. Prioritization is informed by interests, BATNA, and risk tolerance. Negotiators should identify non-negotiable terms and areas for flexibility. Structured approaches, such as issue mapping or scoring, facilitate efficient negotiation and reduce deadlock.
""",
        key_factors=["Term Importance", "Trade-offs", "Package Deals", "Issue Mapping", "Flexibility"],
        primary_authority=["Lax & Sebenius", "Bazerman & Neale"],
        burden_holder="Lead negotiator",
        adversary_position="Insisting on all terms; refusing trade-offs; rigid negotiation",
        counter_arguments=[
            "Prioritization may be misaligned",
            "Trade-offs may be rejected",
            "Complexity may lead to confusion"
        ],
        resolution_strategy="Map issues; prioritize terms; propose package deals and trade-offs",
        entity_scope="Individuals, teams, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="The Manager as Negotiator (Lax & Sebenius, 1986)"
    ),
    DoctrineBlock(
        topic="Information Asymmetry and Signaling",
        keywords=["information asymmetry", "signaling", "hidden information", "revelation", "negotiation tactics"],
        conclusion_template="Manage information asymmetry through strategic signaling and information revelation.",
        reasoning_framework="""
Information asymmetry occurs when one party possesses information not available to the other. Negotiators use signaling—verbal and nonverbal cues—to reveal or conceal information. Strategic disclosure can build trust, influence perceptions, and shape negotiation outcomes. Risks include misinterpretation, bluffing, and manipulation. Parties must assess the value of information, timing of disclosure, and potential impact on negotiation dynamics. Signaling is particularly important in high-stakes or complex negotiations.
""",
        key_factors=["Information Value", "Signaling Techniques", "Disclosure Timing", "Trust", "Perception Management"],
        primary_authority=["Raiffa", "Bazerman & Neale"],
        burden_holder="Party with superior information",
        adversary_position="Demanding full disclosure; bluffing; misinterpreting signals",
        counter_arguments=[
            "Signaling may be misread",
            "Disclosure may weaken position",
            "Information asymmetry may persist"
        ],
        resolution_strategy="Use strategic signaling; disclose selectively; manage perceptions",
        entity_scope="Individuals, organizations",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation Analysis (Raiffa, 2002)"
    ),
    DoctrineBlock(
        topic="Mnookin Beyond Winning Framework",
        keywords=["Mnookin", "beyond winning", "negotiation framework", "lawyer negotiation", "ethical boundaries"],
        conclusion_template="Apply Mnookin's framework to balance advocacy, ethics, and value creation in negotiation.",
        reasoning_framework="""
Mnookin's Beyond Winning framework emphasizes balancing client advocacy, ethical boundaries, and value creation. Lawyers and negotiators must navigate tensions between maximizing outcomes and maintaining integrity. The framework advocates for interest-based negotiation, creative problem-solving, and ethical conduct. It addresses challenges such as information asymmetry, power dynamics, and multiparty complexity. Negotiators should prepare thoroughly, anticipate ethical dilemmas, and seek durable, value-maximizing agreements.
""",
        key_factors=["Advocacy", "Ethical Boundaries", "Value Creation", "Preparation", "Durability"],
        primary_authority=["Mnookin et al.", "Harvard Negotiation Project"],
        burden_holder="Negotiator/advocate",
        adversary_position="Aggressive negotiation; ethical breaches; zero-sum tactics",
        counter_arguments=[
            "Ethical boundaries may be unclear",
            "Advocacy may conflict with value creation",
            "Framework may be difficult to apply"
        ],
        resolution_strategy="Prepare thoroughly; clarify ethical boundaries; balance advocacy and value creation",
        entity_scope="Lawyers, negotiators, organizations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Beyond Winning (Mnookin et al., 2000)"
    ),
    DoctrineBlock(
        topic="Game Theory Applications in Negotiation",
        keywords=["game theory", "strategic interaction", "payoff matrix", "Nash equilibrium", "negotiation tactics"],
        conclusion_template="Use game theory to model negotiation strategies and predict outcomes.",
        reasoning_framework="""
Game theory provides mathematical models for analyzing strategic interactions in negotiation. Concepts such as payoff matrices, Nash equilibrium, and mixed strategies inform negotiation tactics and predict outcomes. Negotiators use game theory to anticipate counterpart moves, identify optimal strategies, and assess risks. Applications include distributive bargaining, coalition formation, and multiparty negotiations. Limitations include assumptions of rationality and complete information. Game theory is most effective in structured, high-stakes negotiations.
""",
        key_factors=["Payoff Matrix", "Equilibrium Analysis", "Strategy Selection", "Risk Assessment", "Rationality"],
        primary_authority=["Nash", "Raiffa", "Axelrod"],
        burden_holder="Negotiator/modeler",
        adversary_position="Irrational behavior; incomplete information; rejecting game theory assumptions",
        counter_arguments=[
            "Game theory may oversimplify negotiation",
            "Assumptions may not hold",
            "Counterpart may act irrationally"
        ],
        resolution_strategy="Model negotiation; use game theory insights; adjust for real-world complexity",
        entity_scope="Individuals, teams, organizations",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation Analysis (Raiffa, 2002)"
    ),
    DoctrineBlock(
        topic="Deadline Pressure and Time Tactics",
        keywords=["deadline", "time pressure", "urgency", "negotiation tactics", "expiring offers"],
        conclusion_template="Leverage deadlines and time tactics to influence negotiation pace and outcomes.",
        reasoning_framework="""
Deadlines and time pressure are powerful negotiation levers. Parties use expiring offers, artificial deadlines, and urgency to accelerate decision-making and extract concessions. Risks include rushed agreements, suboptimal outcomes, and manipulation. Negotiators must assess the legitimacy of deadlines, prepare for time tactics, and use pacing strategically. Time pressure can be countered by requesting extensions, slowing negotiation, or exposing artificial deadlines.
""",
        key_factors=["Deadline Legitimacy", "Time Tactics", "Pacing", "Concession Extraction", "Countermeasures"],
        primary_authority=["Bazerman & Neale", "Lewicki et al."],
        burden_holder="Party imposing deadline",
        adversary_position="Rejecting deadlines; slowing negotiation; exposing artificial urgency",
        counter_arguments=[
            "Deadlines may be artificial",
            "Time pressure may lead to poor decisions",
            "Extensions may be requested"
        ],
        resolution_strategy="Assess deadlines; use time tactics judiciously; counter artificial urgency",
        entity_scope="Individuals, organizations",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Negotiation (Lewicki et al., 2015)"
    ),
    DoctrineBlock(
        topic="Cross-Cultural Negotiation Dynamics",
        keywords=["cross-cultural", "culture", "negotiation", "communication", "value differences"],
        conclusion_template="Adapt negotiation strategies to cross-cultural dynamics and value differences.",
        reasoning_framework="""
Cross-cultural negotiations require sensitivity to communication styles, value differences, and cultural norms. Negotiators must research counterpart's culture, adapt strategies, and avoid ethnocentric assumptions. Techniques include using interpreters, adjusting communication, and building rapport. Risks include miscommunication, misunderstanding, and value clashes. Successful cross-cultural negotiation relies on preparation, flexibility, and respect for diversity.
""",
        key_factors=["Cultural Research", "Communication Adaptation", "Value Differences", "Rapport Building", "Flexibility"],
        primary_authority=["Salacuse", "Fisher, Ury & Patton"],
        burden_holder="Party seeking agreement",
        adversary_position="Insisting on own norms; refusing adaptation; miscommunication",
        counter_arguments=[
            "Cultural differences may be insurmountable",
            "Miscommunication may persist",
            "Adaptation may be difficult"
        ],
        resolution_strategy="Research culture; adapt strategies; build rapport",
        entity_scope="Individuals, organizations, governments",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Negotiating the World (Salacuse, 1991)"
    ),
    DoctrineBlock(
        topic="Email and Virtual Negotiation Challenges",
        keywords=["email negotiation", "virtual", "remote", "asynchronous", "communication barriers"],
        conclusion_template="Mitigate virtual negotiation challenges by enhancing communication and building rapport.",
        reasoning_framework="""
Email and virtual negotiations introduce barriers such as lack of nonverbal cues, asynchronous communication, and reduced rapport. Negotiators must compensate by using clear, structured communication, confirming understanding, and building trust through consistent interaction. Risks include misinterpretation, escalation, and loss of nuance. Techniques include using video calls, structured agendas, and explicit signaling. Preparation and follow-up are critical to ensure alignment and avoid misunderstandings.
""",
        key_factors=["Communication Clarity", "Rapport Building", "Structured Agendas", "Follow-up", "Technology Use"],
        primary_authority=["Thompson", "Bazerman & Neale"],
        burden_holder="Initiator/lead negotiator",
        adversary_position="Refusing virtual negotiation; misinterpreting messages; escalating conflicts",
        counter_arguments=[
            "Virtual barriers may persist",
            "Misinterpretation may occur",
            "Rapport may be difficult to build"
        ],
        resolution_strategy="Use clear communication; build rapport; leverage technology",
        entity_scope="Individuals, teams, organizations",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="Negotiation (Thompson, 2015)"
    ),
    DoctrineBlock(
        topic="Power Dynamics and Leverage Sources",
        keywords=["power", "leverage", "negotiation", "authority", "dependency"],
        conclusion_template="Assess and leverage power dynamics to influence negotiation outcomes.",
        reasoning_framework="""
Power in negotiation arises from sources such as information, authority, resources, and dependency. Negotiators must assess their own and counterpart's power, identify leverage points, and use them strategically. Techniques include controlling information, building alliances, and exploiting dependency. Risks include power imbalances, escalation, and ethical breaches. Power dynamics are fluid and may shift during negotiation. Awareness and management of power are critical to achieving favorable outcomes.
""",
        key_factors=["Power Assessment", "Leverage Identification", "Authority", "Dependency", "Alliance Building"],
        primary_authority=["French & Raven", "Lewicki et al."],
        burden_holder="Party with power",
        adversary_position="Resisting power; building counter-leverage; exposing dependency",
        counter_arguments=[
            "Power may be contested",
            "Leverage may shift",
            "Ethical boundaries may be crossed"
        ],
        resolution_strategy="Assess power; use leverage judiciously; monitor ethical boundaries",
        entity_scope="Individuals, teams, organizations",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation (Lewicki et al., 2015)"
    ),
    DoctrineBlock(
        topic="Reactive Devaluation and Psychological Biases",
        keywords=["reactive devaluation", "psychological bias", "negotiation psychology", "perception", "cognitive errors"],
        conclusion_template="Identify and mitigate psychological biases, including reactive devaluation, in negotiation.",
        reasoning_framework="""
Reactive devaluation occurs when parties undervalue proposals from adversaries due to bias. Negotiators must recognize psychological biases, such as anchoring, confirmation bias, and loss aversion, that distort perception and decision-making. Techniques include using objective criteria, third-party facilitation, and bias education. Risks include impasse, suboptimal agreements, and damaged relationships. Awareness and mitigation of biases are critical to effective negotiation.
""",
        key_factors=["Bias Identification", "Objective Criteria", "Third-party Facilitation", "Education", "Perception Management"],
        primary_authority=["Bazerman & Neale", "Thompson"],
        burden_holder="Both parties",
        adversary_position="Denying bias; refusing mitigation; insisting on subjective criteria",
        counter_arguments=[
            "Bias may be unconscious",
            "Mitigation may be difficult",
            "Objective criteria may be contested"
        ],
        resolution_strategy="Educate parties; use objective criteria; employ third-party facilitation",
        entity_scope="Individuals, teams",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation (Bazerman & Neale, 1992)"
    ),
    DoctrineBlock(
        topic="Negotiating with Agents and Principals",
        keywords=["agents", "principals", "negotiation", "representation", "authority"],
        conclusion_template="Manage agent-principal dynamics by clarifying authority and aligning interests.",
        reasoning_framework="""
Negotiations involving agents and principals require clarity of authority, alignment of interests, and management of communication. Agents may have incentives misaligned with principals, leading to suboptimal outcomes. Techniques include explicit mandates, regular communication, and incentive alignment. Risks include unauthorized commitments, misrepresentation, and principal-agent conflicts. Negotiators must verify authority, monitor agent behavior, and ensure principal interests are represented.
""",
        key_factors=["Authority Clarification", "Interest Alignment", "Communication", "Mandate", "Incentive Structure"],
        primary_authority=["Mnookin", "Lewicki et al."],
        burden_holder="Agent/representative",
        adversary_position="Questioning authority; exploiting misalignment; bypassing agent",
        counter_arguments=[
            "Authority may be unclear",
            "Interests may be misaligned",
            "Agent may act independently"
        ],
        resolution_strategy="Clarify mandates; align incentives; maintain communication",
        entity_scope="Individuals, organizations",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Beyond Winning (Mnookin et al., 2000)"
    ),
    DoctrineBlock(
        topic="Contingent Contracts and Risk Management",
        keywords=["contingent contract", "risk management", "uncertainty", "conditional agreement", "future events"],
        conclusion_template="Use contingent contracts to manage risk and address uncertainty in negotiation.",
        reasoning_framework="""
Contingent contracts address uncertainty by linking agreement terms to future events or outcomes. Parties negotiate conditional terms, such as bonuses, penalties, or performance triggers, to manage risk and align interests. Contingent agreements require clear definitions, enforceability, and monitoring mechanisms. Risks include ambiguity, unenforceability, and unforeseen events. Negotiators must assess risk tolerance, structure contingencies, and ensure clarity.
""",
        key_factors=["Risk Assessment", "Contingency Structure", "Clarity", "Enforceability", "Monitoring"],
        primary_authority=["Bazerman & Neale", "Lax & Sebenius"],
        burden_holder="Party proposing contingency",
        adversary_position="Rejecting contingencies; demanding certainty; contesting enforceability",
        counter_arguments=[
            "Contingencies may be ambiguous",
            "Enforceability may be uncertain",
            "Future events may be unpredictable"
        ],
        resolution_strategy="Define contingencies clearly; assess enforceability; monitor outcomes",
        entity_scope="Individuals, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Negotiation (Bazerman & Neale, 1992)"
    ),
    DoctrineBlock(
        topic="Post-Settlement Settlement and Continuous Improvement",
        keywords=["post-settlement", "continuous improvement", "negotiation", "after agreement", "value maximization"],
        conclusion_template="Engage in post-settlement settlement to maximize value and improve agreements.",
        reasoning_framework="""
Post-settlement settlement involves revisiting agreements after initial deal to maximize value and address overlooked issues. Parties may identify new opportunities, resolve residual concerns, and improve terms. Continuous improvement requires ongoing communication, monitoring, and willingness to renegotiate. Risks include reopening settled issues, damaging trust, and escalating disputes. Negotiators must balance value maximization with stability and relationship management.
""",
        key_factors=["Value Maximization", "Continuous Improvement", "Communication", "Monitoring", "Relationship Management"],
        primary_authority=["Lax & Sebenius", "Bazerman & Neale"],
        burden_holder="Both parties",
        adversary_position="Refusing renegotiation; insisting on finality; escalating disputes",
        counter_arguments=[
            "Reopening settlement may damage trust",
            "Continuous improvement may be resisted",
            "Value maximization may be limited"
        ],
        resolution_strategy="Communicate openly; monitor agreements; pursue improvement judiciously",
        entity_scope="Individuals, organizations",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation (Bazerman & Neale, 1992)"
    ),
    DoctrineBlock(
        topic="Negotiation Ethics and Deception",
        keywords=["ethics", "deception", "negotiation", "integrity", "misrepresentation"],
        conclusion_template="Maintain ethical standards and avoid deception in negotiation.",
        reasoning_framework="""
Ethical negotiation requires integrity, honesty, and avoidance of deception or misrepresentation. Parties must adhere to legal and professional standards, balancing advocacy with ethical boundaries. Risks include reputational damage, legal liability, and escalation. Techniques include transparency, disclosure, and ethical education. Negotiators must anticipate ethical dilemmas, clarify boundaries, and monitor conduct. Deception may provide short-term gains but undermines long-term relationships and trust.
""",
        key_factors=["Ethical Standards", "Integrity", "Disclosure", "Legal Compliance", "Reputation"],
        primary_authority=["Mnookin", "Lewicki et al."],
        burden_holder="Both parties",
        adversary_position="Engaging in deception; refusing disclosure; ignoring ethical boundaries",
        counter_arguments=[
            "Ethical boundaries may be unclear",
            "Deception may be difficult to detect",
            "Short-term gains may tempt unethical conduct"
        ],
        resolution_strategy="Clarify ethical standards; educate parties; monitor conduct",
        entity_scope="Individuals, organizations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Beyond Winning (Mnookin et al., 2000)"
    ),
    DoctrineBlock(
        topic="Internal Alignment and Stakeholder Management",
        keywords=["internal alignment", "stakeholder management", "negotiation", "preparation", "consensus"],
        conclusion_template="Achieve internal alignment and manage stakeholders to support negotiation outcomes.",
        reasoning_framework="""
Internal alignment involves preparing all stakeholders, clarifying objectives, and building consensus before negotiation. Stakeholder management includes mapping interests, communicating priorities, and resolving internal conflicts. Risks include misalignment, internal sabotage, and conflicting mandates. Techniques include pre-negotiation meetings, issue mapping, and consensus-building. Successful negotiation requires unified support and clear mandates.
""",
        key_factors=["Stakeholder Mapping", "Consensus Building", "Communication", "Preparation", "Mandate Clarity"],
        primary_authority=["Lax & Sebenius", "Lewicki et al."],
        burden_holder="Lead negotiator",
        adversary_position="Exploiting misalignment; sowing internal discord; questioning mandate",
        counter_arguments=[
            "Internal conflicts may persist",
            "Consensus may be difficult",
            "Mandates may be unclear"
        ],
        resolution_strategy="Map stakeholders; build consensus; clarify mandates",
        entity_scope="Teams, organizations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="The Manager as Negotiator (Lax & Sebenius, 1986)"
    ),
    DoctrineBlock(
        topic="Gender and Diversity in Negotiation",
        keywords=["gender", "diversity", "negotiation", "bias", "inclusion"],
        conclusion_template="Address gender and diversity issues to foster inclusive and effective negotiation.",
        reasoning_framework="""
Negotiation outcomes may be influenced by gender and diversity dynamics, including bias, stereotypes, and inclusion. Parties must recognize and mitigate biases, promote diversity, and foster inclusive negotiation environments. Techniques include bias education, diverse team composition, and inclusive communication. Risks include discrimination, exclusion, and suboptimal outcomes. Inclusive negotiation enhances creativity, value creation, and relationship-building.
""",
        key_factors=["Bias Mitigation", "Diversity Promotion", "Inclusive Communication", "Team Composition", "Education"],
        primary_authority=["Thompson", "Bazerman & Neale"],
        burden_holder="Both parties",
        adversary_position="Perpetuating bias; excluding diverse voices; resisting inclusion",
        counter_arguments=[
            "Bias may be unconscious",
            "Diversity may be resisted",
            "Inclusion may be difficult"
        ],
        resolution_strategy="Educate parties; promote diversity; foster inclusion",
        entity_scope="Individuals, teams, organizations",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Negotiation (Thompson, 2015)"
    ),
    DoctrineBlock(
        topic="Relationship vs Transaction Focus",
        keywords=["relationship", "transaction", "negotiation", "long-term", "short-term"],
        conclusion_template="Balance relationship and transaction focus to optimize negotiation outcomes.",
        reasoning_framework="""
Negotiators must balance relationship-building with transactional outcomes. Relationship focus emphasizes trust, rapport, and long-term value, while transaction focus prioritizes immediate gains. The optimal approach depends on context, stakes, and future interactions. Techniques include trust-building, communication, and value creation. Risks include sacrificing value for relationship or vice versa. Negotiators should assess priorities, align strategies, and monitor outcomes.
""",
        key_factors=["Trust", "Rapport", "Value Creation", "Priority Assessment", "Outcome Monitoring"],
        primary_authority=["Fisher, Ury & Patton", "Lax & Sebenius"],
        burden_holder="Both parties",
        adversary_position="Insisting on transaction; ignoring relationship; refusing trust-building",
        counter_arguments=[
            "Relationship focus may undermine value",
            "Transaction focus may damage relationships",
            "Balance may be difficult to achieve"
        ],
        resolution_strategy="Assess priorities; align strategies; monitor outcomes",
        entity_scope="Individuals, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Getting to Yes (1981)"
    ),
    # Additional authoritative DoctrineBlock instances for domain coverage:
    DoctrineBlock(
        topic="Negotiation Preparation and Planning",
        keywords=["preparation", "planning", "negotiation strategy", "information gathering", "objective setting"],
        conclusion_template="Prepare thoroughly and plan negotiation strategy to maximize outcomes.",
        reasoning_framework="""
Effective negotiation begins with rigorous preparation and planning. Parties should gather relevant information, set clear objectives, analyze counterpart interests, and develop strategic approaches. Preparation includes BATNA analysis, stakeholder mapping, and scenario planning. Risks include inadequate information, unclear objectives, and reactive negotiation. Planning enables proactive negotiation, anticipation of counterpart moves, and structured concession strategy.
""",
        key_factors=["Information Gathering", "Objective Setting", "BATNA Analysis", "Stakeholder Mapping", "Scenario Planning"],
        primary_authority=["Fisher, Ury & Patton", "Lewicki et al."],
        burden_holder="Lead negotiator",
        adversary_position="Exploiting lack of preparation; introducing surprises; shifting objectives",
        counter_arguments=[
            "Preparation may be incomplete",
            "Objectives may change",
            "Counterpart may introduce new information"
        ],
        resolution_strategy="Prepare thoroughly; plan strategy; adapt to new information",
        entity_scope="Individuals, teams, organizations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Getting to Yes (1981)"
    ),
    DoctrineBlock(
        topic="Negotiation Opening and Framing",
        keywords=["opening", "framing", "first impression", "negotiation", "positioning"],
        conclusion_template="Frame negotiation opening to set tone and influence counterpart perceptions.",
        reasoning_framework="""
The opening phase of negotiation sets the tone, establishes rapport, and frames issues. Effective framing involves presenting positions, interests, and objectives in a manner that influences counterpart perceptions and expectations. Techniques include positive framing, highlighting mutual interests, and avoiding adversarial language. Risks include negative first impressions, escalation, and miscommunication. Opening strategies should be tailored to context, counterpart, and desired outcomes.
""",
        key_factors=["Framing", "Rapport", "Mutual Interests", "Language", "Context"],
        primary_authority=["Fisher, Ury & Patton", "Lewicki et al."],
        burden_holder="Initiator",
        adversary_position="Rejecting framing; escalating; misinterpreting opening",
        counter_arguments=[
            "Framing may be ignored",
            "Opening may escalate conflict",
            "Mutual interests may not be recognized"
        ],
        resolution_strategy="Frame positively; highlight mutual interests; avoid adversarial language",
        entity_scope="Individuals, teams, organizations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Getting to Yes (1981)"
    ),
    DoctrineBlock(
        topic="Negotiation Closing and Agreement Finalization",
        keywords=["closing", "agreement", "finalization", "negotiation", "commitment"],
        conclusion_template="Close negotiation effectively to finalize agreement and ensure commitment.",
        reasoning_framework="""
Closing negotiation involves finalizing terms, confirming commitments, and documenting agreement. Effective closing requires summarizing key points, addressing residual concerns, and ensuring clarity. Risks include last-minute changes, ambiguity, and lack of commitment. Techniques include written agreements, confirmation of understanding, and post-closing follow-up. Closing strategies should reinforce trust, clarify responsibilities, and ensure enforceability.
""",
        key_factors=["Agreement Finalization", "Commitment", "Clarity", "Documentation", "Follow-up"],
        primary_authority=["Lewicki et al.", "Bazerman & Neale"],
        burden_holder="Lead negotiator",
        adversary_position="Introducing last-minute changes; refusing commitment; contesting terms",
        counter_arguments=[
            "Agreement may be ambiguous",
            "Commitment may be lacking",
            "Documentation may be incomplete"
        ],
        resolution_strategy="Summarize agreement; confirm commitment; document terms",
        entity_scope="Individuals, teams, organizations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Negotiation (Lewicki et al., 2015)"
    ),
    DoctrineBlock(
        topic="Negotiation Communication Skills",
        keywords=["communication", "skills", "active listening", "clarity", "negotiation"],
        conclusion_template="Use effective communication skills, including active listening and clarity, to enhance negotiation.",
        reasoning_framework="""
Communication is central to negotiation success. Skills include active listening, clear articulation, questioning, and feedback. Active listening builds rapport, uncovers interests, and reduces misunderstanding. Clarity ensures accurate information exchange and reduces ambiguity. Risks include miscommunication, escalation, and loss of trust. Negotiators should use structured communication, confirm understanding, and adapt to counterpart styles.
""",
        key_factors=["Active Listening", "Clarity", "Questioning", "Feedback", "Adaptation"],
        primary_authority=["Fisher, Ury & Patton", "Lewicki et al."],
        burden_holder="Both parties",
        adversary_position="Refusing communication; misinterpreting messages; escalating",
        counter_arguments=[
            "Communication may break down",
            "Active listening may be ignored",
            "Clarity may be lacking"
        ],
        resolution_strategy="Use active listening; communicate clearly; confirm understanding",
        entity_scope="Individuals, teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Getting to Yes (1981)"
    ),
    DoctrineBlock(
        topic="Negotiation Trust Building",
        keywords=["trust", "building", "negotiation", "rapport", "relationship"],
        conclusion_template="Build trust to facilitate negotiation and foster durable agreements.",
        reasoning_framework="""
Trust is foundational to effective negotiation. Techniques include consistent behavior, transparency, honoring commitments, and rapport-building. Trust reduces adversarial tension, facilitates information sharing, and enables creative solutions. Risks include betrayal, loss of trust, and escalation. Negotiators should monitor trust levels, address breaches promptly, and reinforce trust through positive actions.
""",
        key_factors=["Consistency", "Transparency", "Commitment", "Rapport", "Monitoring"],
        primary_authority=["Fisher, Ury & Patton", "Lewicki et al."],
        burden_holder="Both parties",
        adversary_position="Betraying trust; refusing transparency; breaking commitments",
        counter_arguments=[
            "Trust may be difficult to build",
            "Betrayal may occur",
            "Rapport may be lacking"
        ],
        resolution_strategy="Behave consistently; honor commitments; address breaches",
        entity_scope="Individuals, teams, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Getting to Yes (1981)"
    ),
    DoctrineBlock(
        topic="Negotiation Emotional Intelligence",
        keywords=["emotional intelligence", "negotiation", "self-awareness", "empathy", "emotion management"],
        conclusion_template="Apply emotional intelligence to manage emotions and enhance negotiation outcomes.",
        reasoning_framework="""
Emotional intelligence enables negotiators to manage their own emotions, empathize with counterparts, and navigate emotional dynamics. Skills include self-awareness, self-regulation, empathy, and social awareness. Emotional intelligence reduces escalation, builds rapport, and facilitates creative solutions. Risks include emotional outbursts, misinterpretation, and damaged relationships. Negotiators should monitor emotions, use empathy, and address emotional issues constructively.
""",
        key_factors=["Self-awareness", "Self-regulation", "Empathy", "Social Awareness", "Emotion Management"],
        primary_authority=["Goleman", "Thompson"],
        burden_holder="Both parties",
        adversary_position="Emotional escalation; refusing empathy; misinterpreting emotions",
        counter_arguments=[
            "Emotions may be difficult to manage",
            "Empathy may be lacking",
            "Misinterpretation may occur"
        ],
        resolution_strategy="Monitor emotions; use empathy; address issues constructively",
        entity_scope="Individuals, teams",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="Emotional Intelligence (Goleman, 1995)"
    ),
    DoctrineBlock(
        topic="Negotiation Conflict Management",
        keywords=["conflict management", "negotiation", "resolution", "escalation", "collaboration"],
        conclusion_template="Manage conflict constructively to resolve disputes and enhance negotiation outcomes.",
        reasoning_framework="""
Conflict is inherent in negotiation. Constructive conflict management involves identifying sources, facilitating communication, and seeking collaborative solutions. Techniques include mediation, issue reframing, and structured problem-solving. Risks include escalation, impasse, and damaged relationships. Negotiators should address conflict promptly, use collaborative approaches, and seek win-win outcomes.
""",
        key_factors=["Conflict Identification", "Communication", "Collaboration", "Mediation", "Problem-solving"],
        primary_authority=["Lewicki et al.", "Fisher, Ury & Patton"],
        burden_holder="Both parties",
        adversary_position="Escalating conflict; refusing collaboration; blocking resolution",
        counter_arguments=[
            "Conflict may escalate",
            "Collaboration may be resisted",
            "Resolution may be difficult"
        ],
        resolution_strategy="Identify conflict; facilitate communication; use collaborative approaches",
        entity_scope="Individuals, teams, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Negotiation (Lewicki et al., 2015)"
    ),
    DoctrineBlock(
        topic="Negotiation Creativity and Option Generation",
        keywords=["creativity", "option generation", "negotiation", "brainstorming", "value creation"],
        conclusion_template="Use creativity and option generation to expand negotiation outcomes and create value.",
        reasoning_framework="""
Creativity in negotiation enables parties to generate options, expand the pie, and create value. Techniques include brainstorming, lateral thinking, and structured option generation. Risks include fixation, rejection of creative options, and lack of buy-in. Negotiators should encourage creativity, explore alternatives, and evaluate options collaboratively.
""",
        key_factors=["Brainstorming", "Lateral Thinking", "Option Evaluation", "Collaboration", "Value Creation"],
        primary_authority=["Fisher, Ury & Patton", "Lax & Sebenius"],
        burden_holder="Both parties",
        adversary_position="Rejecting creative options; insisting on fixed positions; refusing collaboration",
        counter_arguments=[
            "Creativity may be limited",
            "Options may be rejected",
            "Collaboration may be lacking"
        ],
        resolution_strategy="Encourage brainstorming; evaluate options; collaborate",
        entity_scope="Individuals, teams, organizations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Getting to Yes (1981)"
    ),
    DoctrineBlock(
        topic="Negotiation Influence and Persuasion",
        keywords=["influence", "persuasion", "negotiation", "communication", "power"],
        conclusion_template="Use influence and persuasion techniques to shape negotiation outcomes.",
        reasoning_framework="""
Influence and persuasion are critical negotiation skills. Techniques include framing, storytelling, appeals to authority, and reciprocity. Effective persuasion requires understanding counterpart interests, tailoring messages, and building credibility. Risks include manipulation, resistance, and loss of trust. Negotiators should use influence ethically, monitor counterpart responses, and adjust strategies.
""",
        key_factors=["Framing", "Storytelling", "Authority", "Reciprocity", "Credibility"],
        primary_authority=["Cialdini", "Lewicki et al."],
        burden_holder="Party seeking influence",
        adversary_position="Resisting persuasion; questioning credibility; refusing influence",
        counter_arguments=[
            "Persuasion may be resisted",
            "Influence may be perceived as manipulation",
            "Credibility may be lacking"
        ],
        resolution_strategy="Tailor messages; build credibility; use influence ethically",
        entity_scope="Individuals, teams, organizations",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="Influence (Cialdini, 1984)"
    ),
    DoctrineBlock(
        topic="Negotiation Decision Making Under Uncertainty",
        keywords=["decision making", "uncertainty", "negotiation", "risk", "probability"],
        conclusion_template="Make negotiation decisions under uncertainty by assessing risks and probabilities.",
        reasoning_framework="""
Negotiators often face uncertainty regarding counterpart actions, outcomes, and external factors. Decision making under uncertainty involves assessing risks, probabilities, and potential outcomes. Techniques include scenario planning, risk analysis, and use of decision trees. Risks include overconfidence, misestimation, and loss aversion. Negotiators should gather information, model scenarios, and make informed decisions.
""",
        key_factors=["Risk Assessment", "Probability Analysis", "Scenario Planning", "Decision Trees", "Information Gathering"],
        primary_authority=["Bazerman & Neale", "Raiffa"],
        burden_holder="Lead negotiator",
        adversary_position="Introducing uncertainty; refusing information; escalating risk",
        counter_arguments=[
            "Risks may be misestimated",
            "Information may be lacking",
            "Uncertainty may persist"
        ],
        resolution_strategy="Assess risks; model scenarios; make informed decisions",
        entity_scope="Individuals, teams, organizations",
        confidence=0.90,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation Analysis (Raiffa, 2002)"
    ),
    DoctrineBlock(
        topic="Negotiation Reputation Management",
        keywords=["reputation", "management", "negotiation", "trust", "credibility"],
        conclusion_template="Manage reputation to enhance negotiation credibility and outcomes.",
        reasoning_framework="""
Reputation influences negotiation outcomes by shaping counterpart perceptions of trustworthiness and credibility. Techniques include consistent behavior, honoring commitments, and managing public information. Risks include reputational damage, loss of trust, and exclusion from future negotiations. Negotiators should monitor reputation, address breaches, and reinforce positive actions.
""",
        key_factors=["Consistency", "Commitment", "Public Information", "Trustworthiness", "Monitoring"],
        primary_authority=["Lewicki et al.", "Bazerman & Neale"],
        burden_holder="Both parties",
        adversary_position="Damaging reputation; questioning credibility; refusing trust",
        counter_arguments=[
            "Reputation may be difficult to manage",
            "Breaches may occur",
            "Credibility may be questioned"
        ],
        resolution_strategy="Behave consistently; honor commitments; manage public information",
        entity_scope="Individuals, teams, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Negotiation (Lewicki et al., 2015)"
    ),
    DoctrineBlock(
        topic="Negotiation Escalation and De-escalation Techniques",
        keywords=["escalation", "de-escalation", "negotiation", "conflict", "resolution"],
        conclusion_template="Use escalation and de-escalation techniques to manage negotiation conflict and reach agreement.",
        reasoning_framework="""
Escalation and de-escalation techniques are used to manage conflict and facilitate agreement. Escalation may involve increasing stakes, introducing third parties, or formalizing processes. De-escalation includes calming language, reframing issues, and collaborative problem-solving. Risks include uncontrolled escalation, impasse, and damaged relationships. Negotiators should monitor conflict levels, use escalation judiciously, and prioritize de-escalation.
""",
        key_factors=["Conflict Monitoring", "Escalation Techniques", "De-escalation Techniques", "Third-party Involvement", "Problem-solving"],
        primary_authority=["Lewicki et al.", "Susskind & Cruikshank"],
        burden_holder="Both parties",
        adversary_position="Escalating conflict; refusing de-escalation; blocking resolution",
        counter_arguments=[
            "Escalation may be uncontrolled",
            "De-escalation may be resisted",
            "Resolution may be difficult"
        ],
        resolution_strategy="Monitor conflict; use escalation judiciously; prioritize de-escalation",
        entity_scope="Individuals, teams, organizations",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation (Lewicki et al., 2015)"
    ),
    DoctrineBlock(
        topic="Negotiation Third-party Facilitation",
        keywords=["third-party", "facilitation", "negotiation", "mediation", "neutral"],
        conclusion_template="Engage third-party facilitation to resolve negotiation impasse and enhance outcomes.",
        reasoning_framework="""
Third-party facilitation involves engaging a neutral mediator or facilitator to resolve negotiation impasse and enhance outcomes. Facilitators help reframe issues, identify interests, and propose creative solutions. Risks include loss of control, increased costs, and resistance to facilitation. Negotiators should select qualified facilitators, clarify roles, and monitor process.
""",
        key_factors=["Neutrality", "Issue Reframing", "Interest Identification", "Creative Solutions", "Process Monitoring"],
        primary_authority=["Susskind & Cruikshank", "Mnookin"],
        burden_holder="Party seeking facilitation",
        adversary_position="Resisting facilitation; questioning neutrality; blocking process",
        counter_arguments=[
            "Facilitation may be resisted",
            "Neutrality may be questioned",
            "Process may be costly"
        ],
        resolution_strategy="Select qualified facilitators; clarify roles; monitor process",
        entity_scope="Individuals, teams, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Breaking the Impasse (Susskind & Cruikshank, 1987)"
    ),
    DoctrineBlock(
        topic="Negotiation Issue Reframing",
        keywords=["issue reframing", "negotiation", "perspective", "problem-solving", "creative solutions"],
        conclusion_template="Reframe negotiation issues to facilitate creative problem-solving and agreement.",
        reasoning_framework="""
Issue reframing involves changing perspective on negotiation issues to facilitate creative problem-solving and agreement. Techniques include shifting focus from positions to interests, using positive language, and exploring alternatives. Risks include resistance to reframing, fixation, and escalation. Negotiators should use reframing constructively, encourage counterpart buy-in, and explore creative solutions.
""",
        key_factors=["Perspective Shift", "Positive Language", "Interest Focus", "Alternative Exploration", "Buy-in"],
        primary_authority=["Fisher, Ury & Patton", "Lewicki et al."],
        burden_holder="Lead negotiator",
        adversary_position="Resisting reframing; insisting on positions; refusing alternatives",
        counter_arguments=[
            "Reframing may be resisted",
            "Fixation may persist",
            "Creative solutions may be lacking"
        ],
        resolution_strategy="Use positive language; shift focus; explore alternatives",
        entity_scope="Individuals, teams, organizations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Getting to Yes (1981)"
    ),
    DoctrineBlock(
        topic="Negotiation Value Claiming vs Value Creating",
        keywords=["value claiming", "value creating", "negotiation", "distributive", "integrative"],
        conclusion_template="Balance value claiming and value creating strategies to optimize negotiation outcomes.",
        reasoning_framework="""
Negotiators must balance value claiming (distributive) and value creating (integrative) strategies. Value claiming focuses on maximizing individual outcomes, while value creating seeks joint gains. Techniques include competitive tactics, collaborative problem-solving, and creative option generation. Risks include imbalance, escalation, and missed opportunities. Negotiators should assess context, align strategies, and monitor outcomes.
""",
        key_factors=["Competitive Tactics", "Collaborative Problem-solving", "Option Generation", "Context Assessment", "Outcome Monitoring"],
        primary_authority=["Lax & Sebenius", "Fisher, Ury & Patton"],
        burden_holder="Both parties",
        adversary_position="Insisting on value claiming; refusing collaboration; missing joint gains",
        counter_arguments=[
            "Balance may be difficult",
            "Opportunities may be missed",
            "Collaboration may be resisted"
        ],
        resolution_strategy="Assess context; align strategies; monitor outcomes",
        entity_scope="Individuals, teams, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="The Manager as Negotiator (Lax & Sebenius, 1986)"
    ),
    DoctrineBlock(
        topic="Negotiation Multi-Issue Bargaining",
        keywords=["multi-issue", "bargaining", "negotiation", "trade-offs", "package deals"],
        conclusion_template="Use multi-issue bargaining to leverage trade-offs and maximize negotiation outcomes.",
        reasoning_framework="""
Multi-issue bargaining involves negotiating multiple issues simultaneously to leverage trade-offs and maximize outcomes. Techniques include package deals, conditional offers, and issue prioritization. Risks include complexity, confusion, and missed opportunities. Negotiators should map issues, prioritize terms, and use structured approaches.
""",
        key_factors=["Issue Mapping", "Trade-offs", "Package Deals", "Prioritization", "Structured Approaches"],
        primary_authority=["Lax & Sebenius", "Bazerman & Neale"],
        burden_holder="Lead negotiator",
        adversary_position="Insisting on single issue; refusing trade-offs; escalating complexity",
        counter_arguments=[
            "Complexity may lead to confusion",
            "Trade-offs may be rejected",
            "Opportunities may be missed"
        ],
        resolution_strategy="Map issues; prioritize terms; use package deals",
        entity_scope="Individuals, teams, organizations",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="The Manager as Negotiator (Lax & Sebenius, 1986)"
    ),
    DoctrineBlock(
        topic="Negotiation Outcome Evaluation and Learning",
        keywords=["outcome evaluation", "learning", "negotiation", "post-mortem", "continuous improvement"],
        conclusion_template="Evaluate negotiation outcomes and learn from experience to improve future performance.",
        reasoning_framework="""
Outcome evaluation and learning involve reviewing negotiation results, identifying successes and failures, and applying lessons to future negotiations. Techniques include post-mortem analysis, feedback, and continuous improvement. Risks include failure to learn, repetition of mistakes, and resistance to evaluation. Negotiators should review outcomes, seek feedback, and implement improvements.
""",
        key_factors=["Post-mortem Analysis", "Feedback", "Continuous Improvement", "Learning", "Implementation"],
        primary_authority=["Bazerman & Neale", "Lewicki et al."],
        burden_holder="Both parties",
        adversary_position="Resisting evaluation; repeating mistakes; refusing feedback",
        counter_arguments=[
            "Learning may be resisted",
            "Mistakes may be repeated",
            "Feedback may be ignored"
        ],
        resolution_strategy="Review outcomes; seek feedback; implement improvements",
        entity_scope="Individuals, teams, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Negotiation (Bazerman & Neale, 1992)"
    ),
    DoctrineBlock(
        topic="Negotiation Legal and Regulatory Compliance",
        keywords=["legal compliance", "regulatory", "negotiation", "law", "risk"],
        conclusion_template="Ensure legal and regulatory compliance in negotiation to avoid liability and risk.",
        reasoning_framework="""
Legal and regulatory compliance is essential in negotiation. Parties must understand relevant laws, regulations, and contractual requirements. Risks include legal liability, invalid agreements, and regulatory penalties. Techniques include legal review, compliance checks, and consultation with experts. Negotiators should clarify legal boundaries, document agreements, and monitor compliance.
""",
        key_factors=["Legal Review", "Compliance Checks", "Expert Consultation", "Documentation", "Monitoring"],
        primary_authority=["Mnookin", "Lewicki et al."],
        burden_holder="Both parties",
        adversary_position="Ignoring compliance; introducing illegal terms; refusing legal review",
        counter_arguments=[
            "Compliance may be overlooked",
            "Legal boundaries may be unclear",
            "Risks may be underestimated"
        ],
        resolution_strategy="Conduct legal review; clarify boundaries; monitor compliance",
        entity_scope="Individuals, teams, organizations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Beyond Winning (Mnookin et al., 2000)"
    ),
    DoctrineBlock(
        topic="Negotiation Technology and Data Analytics",
        keywords=["technology", "data analytics", "negotiation", "information", "decision support"],
        conclusion_template="Leverage technology and data analytics to enhance negotiation preparation and outcomes.",
        reasoning_framework="""
Technology and data analytics enhance negotiation by providing information, decision support, and process automation. Techniques include data analysis, modeling, and use of negotiation software. Risks include data misinterpretation, overreliance on technology, and privacy concerns. Negotiators should use technology judiciously, interpret data accurately, and maintain human judgment.
""",
        key_factors=["Data Analysis", "Modeling", "Software", "Judgment", "Privacy"],
        primary_authority=["Bazerman & Neale", "Raiffa"],
        burden_holder="Lead negotiator",
        adversary_position="Rejecting technology; misinterpreting data; overreliance",
        counter_arguments=[
            "Data may be misinterpreted",
            "Technology may fail",
            "Human judgment may be lacking"
        ],
        resolution_strategy="Use technology judiciously; interpret data; maintain judgment",
        entity_scope="Individuals, teams, organizations",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="Negotiation Analysis (Raiffa, 2002)"
    ),
    DoctrineBlock(
        topic="Negotiation Sustainability and Social Responsibility",
        keywords=["sustainability", "social responsibility", "negotiation", "ethics", "long-term"],
        conclusion_template="Integrate sustainability and social responsibility into negotiation to enhance outcomes and reputation.",
        reasoning_framework="""
Sustainability and social responsibility are increasingly important in negotiation. Parties should consider environmental, social, and ethical impacts of agreements. Techniques include sustainability clauses, ethical sourcing, and stakeholder engagement. Risks include reputational damage, regulatory penalties, and exclusion from markets. Negotiators should integrate sustainability, monitor impacts, and communicate commitments.
""",
        key_factors=["Sustainability Clauses", "Ethical Sourcing", "Stakeholder Engagement", "Monitoring", "Communication"],
        primary_authority=["Bazerman & Neale", "Mnookin"],
        burden_holder="Both parties",
        adversary_position="Ignoring sustainability; refusing social responsibility; contesting clauses",
        counter_arguments=[
            "Sustainability may be resisted",
            "Social responsibility may be ignored",
            "Impacts may be difficult to monitor"
        ],
        resolution_strategy="Integrate clauses; engage stakeholders; monitor impacts",
        entity_scope="Individuals, teams, organizations",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Negotiation (Bazerman & Neale, 1992)"
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
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]