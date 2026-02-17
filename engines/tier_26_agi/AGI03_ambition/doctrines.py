from dataclasses import dataclass, field
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
        topic="Goal Decomposition via Hierarchical Task Networks",
        keywords=[
            "HTN", "goal decomposition", "task hierarchy", "subgoals", "planning", "task networks"
        ],
        conclusion_template="Decompose the high-level goal into a hierarchy of actionable sub-tasks using HTN principles.",
        reasoning_framework="""
1. Identify the primary goal.
2. Break the goal into major subgoals that collectively achieve the primary objective.
3. For each subgoal, recursively decompose into smaller, actionable tasks.
4. Establish dependencies and ordering among tasks.
5. Validate that all decomposed tasks, when completed, fulfill the original goal.
6. Assign resources and deadlines to each task node.
7. Monitor progress at each hierarchical level and adjust decomposition as needed.
8. Ensure traceability from sub-tasks to the overarching goal.
9. Use feedback loops to refine task breakdowns based on execution data.
10. Maintain documentation of the decomposition structure for transparency and review.
        """,
        key_factors=[
            "Clarity of the primary goal",
            "Granularity of task decomposition",
            "Dependency mapping",
            "Resource allocation",
            "Traceability",
            "Feedback mechanisms"
        ],
        primary_authority=[
            "Ghallab, M., Nau, D., & Traverso, P. (2004). Automated Planning: Theory and Practice.",
            "Russell, S., & Norvig, P. (2021). Artificial Intelligence: A Modern Approach."
        ],
        burden_holder="Goal owner",
        adversary_position="Flat task lists are sufficient; hierarchical decomposition adds unnecessary complexity.",
        counter_arguments=[
            "Hierarchical decomposition improves clarity and manageability.",
            "HTN enables parallelization and better resource allocation.",
            "Flat lists obscure dependencies and critical paths."
        ],
        resolution_strategy="Demonstrate improved project outcomes using HTN versus flat lists in pilot studies.",
        entity_scope="Project teams, AGI planning modules",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AGI02:HierarchicalDecompositionDoctrine"
    ),
    DoctrineBlock(
        topic="Objectives and Key Results (OKR) Framework",
        keywords=[
            "OKR", "objectives", "key results", "goal setting", "performance measurement"
        ],
        conclusion_template="Adopt the OKR framework to align objectives with measurable key results for effective goal tracking.",
        reasoning_framework="""
1. Define clear, ambitious, and qualitative objectives.
2. For each objective, specify 2-5 quantitative key results.
3. Ensure key results are outcome-focused, not activity-based.
4. Align OKRs across teams to support organizational strategy.
5. Set OKRs in quarterly cycles for agility and adaptability.
6. Track progress regularly and update stakeholders.
7. Encourage transparency by publishing OKRs organization-wide.
8. Review and grade OKRs at the end of each cycle.
9. Use OKR outcomes to inform future goal setting and resource allocation.
10. Foster a culture of stretch goals and learning from misses.
        """,
        key_factors=[
            "Objective clarity",
            "Measurability of key results",
            "Alignment with strategy",
            "Transparency",
            "Review cadence"
        ],
        primary_authority=[
            "Doerr, J. (2018). Measure What Matters.",
            "Grove, A. (1983). High Output Management."
        ],
        burden_holder="Objective setter",
        adversary_position="OKRs are too rigid and discourage creative exploration.",
        counter_arguments=[
            "OKRs are adaptable and encourage ambitious thinking.",
            "They provide focus and measurable progress.",
            "Creative exploration can be an explicit objective."
        ],
        resolution_strategy="Pilot OKRs in a creative team and measure impact on innovation and outcomes.",
        entity_scope="All AGI03 modules, leadership, project teams",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AGI01:OKRImplementation"
    ),
    DoctrineBlock(
        topic="SMART Goal Enforcement",
        keywords=[
            "SMART", "specific", "measurable", "achievable", "relevant", "time-bound", "goal setting"
        ],
        conclusion_template="Enforce the SMART criteria for all goal definitions to ensure clarity and achievability.",
        reasoning_framework="""
1. Ensure every goal is Specific: clearly defined and unambiguous.
2. Make goals Measurable: establish criteria for tracking progress and completion.
3. Confirm goals are Achievable: realistic given available resources and constraints.
4. Align goals to be Relevant: directly support broader objectives and mission.
5. Set goals to be Time-bound: include deadlines or timeframes.
6. Review goals for compliance with all SMART elements.
7. Reject or revise goals that fail to meet any SMART criterion.
8. Educate stakeholders on the importance of SMART goals.
9. Integrate SMART checks into goal-setting workflows.
10. Use SMART compliance as a metric for goal quality.
        """,
        key_factors=[
            "Goal specificity",
            "Measurability",
            "Feasibility",
            "Relevance",
            "Time constraints"
        ],
        primary_authority=[
            "Doran, G. T. (1981). There's a S.M.A.R.T. way to write management's goals and objectives.",
            "Locke, E. A., & Latham, G. P. (2002). Building a practically useful theory of goal setting and task motivation."
        ],
        burden_holder="Goal proposer",
        adversary_position="SMART criteria are overly restrictive and stifle ambition.",
        counter_arguments=[
            "SMART goals enhance clarity and focus.",
            "Ambitious goals can still be SMART if well-defined.",
            "Lack of specificity leads to poor execution."
        ],
        resolution_strategy="Facilitate workshops to demonstrate SMART goal benefits and address concerns.",
        entity_scope="All AGI03 goal-setting modules",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AGI02:SMARTGoalDoctrine"
    ),
    DoctrineBlock(
        topic="Eisenhower Priority Matrix (Urgent-Important Quadrants)",
        keywords=[
            "Eisenhower Matrix", "priority", "urgent", "important", "quadrants", "task management"
        ],
        conclusion_template="Apply the Eisenhower Matrix to categorize and prioritize tasks based on urgency and importance.",
        reasoning_framework="""
1. List all tasks and objectives.
2. For each task, assess its urgency and importance.
3. Assign tasks to one of four quadrants:
   - Q1: Urgent & Important (Do immediately)
   - Q2: Not Urgent & Important (Schedule)
   - Q3: Urgent & Not Important (Delegate)
   - Q4: Not Urgent & Not Important (Eliminate)
4. Focus on Q2 tasks to prevent future crises.
5. Regularly review and update task assignments.
6. Educate teams on the distinction between urgency and importance.
7. Use the matrix to inform daily and strategic planning.
8. Track time allocation across quadrants to optimize productivity.
9. Encourage elimination or delegation of Q3/Q4 tasks.
10. Integrate matrix analysis into AGI03 task selection algorithms.
        """,
        key_factors=[
            "Task urgency",
            "Task importance",
            "Time allocation",
            "Delegation opportunities",
            "Elimination of low-value tasks"
        ],
        primary_authority=[
            "Covey, S. R. (1989). The 7 Habits of Highly Effective People.",
            "Eisenhower, D. D. (1954). Presidential time management principles."
        ],
        burden_holder="Task manager",
        adversary_position="All tasks are important; prioritization is subjective and unnecessary.",
        counter_arguments=[
            "Not all tasks contribute equally to outcomes.",
            "Prioritization prevents burnout and improves results.",
            "Objective criteria can be established for urgency and importance."
        ],
        resolution_strategy="Analyze outcomes before and after matrix adoption to demonstrate effectiveness.",
        entity_scope="AGI03 task management, project teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AGI01:EisenhowerMatrixDoctrine"
    ),
    DoctrineBlock(
        topic="MoSCoW Prioritization",
        keywords=[
            "MoSCoW", "must have", "should have", "could have", "won't have", "prioritization", "requirements"
        ],
        conclusion_template="Utilize MoSCoW prioritization to categorize requirements and features for effective resource allocation.",
        reasoning_framework="""
1. Gather all requirements and desired features.
2. Classify each as Must have, Should have, Could have, or Won't have this time.
3. Ensure 'Must have' items are essential for project viability.
4. Allocate resources first to 'Must have', then 'Should have', and so on.
5. Revisit and adjust classifications as project context evolves.
6. Communicate prioritization rationale to stakeholders.
7. Use MoSCoW to manage scope and expectations.
8. Integrate prioritization into sprint and release planning.
9. Document decisions for future reference and audits.
10. Review the impact of MoSCoW on project delivery and satisfaction.
        """,
        key_factors=[
            "Requirement criticality",
            "Stakeholder alignment",
            "Resource constraints",
            "Scope management",
            "Transparency"
        ],
        primary_authority=[
            "Clegg, D., & Barker, R. (1994). Case Method Fast-Track: A RAD Approach.",
            "DSDM Consortium (2014). MoSCoW Prioritisation."
        ],
        burden_holder="Product owner",
        adversary_position="All features are equally important; MoSCoW is arbitrary.",
        counter_arguments=[
            "MoSCoW provides a structured, transparent prioritization method.",
            "Resource constraints necessitate clear prioritization.",
            "Not all features are critical for success."
        ],
        resolution_strategy="Demonstrate improved delivery predictability and stakeholder satisfaction using MoSCoW.",
        entity_scope="Product management, AGI03 planning modules",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI02:MoSCoWDoctrine"
    ),
    DoctrineBlock(
        topic="RICE Scoring for Prioritization",
        keywords=[
            "RICE", "reach", "impact", "confidence", "effort", "prioritization", "scoring"
        ],
        conclusion_template="Apply RICE scoring to prioritize initiatives based on reach, impact, confidence, and effort.",
        reasoning_framework="""
1. For each initiative, estimate:
   - Reach: Number of users or events affected.
   - Impact: Expected effect on target metric.
   - Confidence: Certainty in estimates.
   - Effort: Person-hours or resources required.
2. Calculate RICE score: (Reach x Impact x Confidence) / Effort.
3. Rank initiatives by RICE score.
4. Review and calibrate estimates with stakeholders.
5. Prioritize high RICE score initiatives for execution.
6. Reassess scores as new data emerges.
7. Document assumptions and rationale for transparency.
8. Use RICE to inform roadmap and resource allocation.
9. Encourage iterative improvement of scoring accuracy.
10. Integrate RICE scoring into AGI03 decision workflows.
        """,
        key_factors=[
            "Estimate accuracy",
            "Stakeholder input",
            "Resource constraints",
            "Transparency",
            "Continuous improvement"
        ],
        primary_authority=[
            "Intercom Product Management (2017). RICE Scoring Model.",
            "Cagan, M., & Jones, C. (2018). INSPIRED: How to Create Products Customers Love."
        ],
        burden_holder="Initiative proposer",
        adversary_position="RICE scoring is too subjective and time-consuming.",
        counter_arguments=[
            "RICE provides a structured, comparative framework.",
            "Subjectivity can be reduced with calibration and data.",
            "The time invested yields better prioritization decisions."
        ],
        resolution_strategy="Pilot RICE scoring and measure prioritization outcomes versus previous methods.",
        entity_scope="Product, engineering, AGI03 prioritization modules",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI01:RICEScoringDoctrine"
    ),
    DoctrineBlock(
        topic="Resource Allocation via Linear Programming",
        keywords=[
            "linear programming", "resource allocation", "optimization", "constraints", "objective function"
        ],
        conclusion_template="Utilize linear programming to optimize resource allocation under defined constraints.",
        reasoning_framework="""
1. Define the objective function to maximize or minimize (e.g., profit, efficiency).
2. List all resource constraints (e.g., time, budget, personnel).
3. Formulate the allocation problem as a set of linear equations and inequalities.
4. Use simplex or interior-point methods to solve the linear program.
5. Analyze the solution for feasibility and optimality.
6. Adjust constraints or objective as necessary based on real-world feedback.
7. Document assumptions and solution rationale.
8. Integrate LP solutions into AGI03 resource management workflows.
9. Monitor allocation outcomes and refine models iteratively.
10. Educate stakeholders on the benefits and limitations of LP-based allocation.
        """,
        key_factors=[
            "Objective clarity",
            "Constraint accuracy",
            "Solution feasibility",
            "Model transparency",
            "Iterative refinement"
        ],
        primary_authority=[
            "Dantzig, G. B. (1963). Linear Programming and Extensions.",
            "Winston, W. L. (2004). Operations Research: Applications and Algorithms."
        ],
        burden_holder="Resource allocator",
        adversary_position="Linear programming is too rigid for dynamic environments.",
        counter_arguments=[
            "LP can be updated with new data and constraints.",
            "It provides optimal solutions within defined parameters.",
            "Dynamic programming and stochastic models can supplement LP."
        ],
        resolution_strategy="Demonstrate improved allocation outcomes using LP versus heuristic methods.",
        entity_scope="Operations, AGI03 resource modules",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="AGI02:LinearProgrammingDoctrine"
    ),
    DoctrineBlock(
        topic="Opportunity Cost Analysis",
        keywords=[
            "opportunity cost", "trade-off", "decision analysis", "resource allocation", "alternative evaluation"
        ],
        conclusion_template="Conduct opportunity cost analysis for all major decisions to ensure optimal resource utilization.",
        reasoning_framework="""
1. Identify all feasible alternatives for a decision.
2. Estimate the value of each alternative (monetary, strategic, etc.).
3. Determine the next-best alternative forgone by each choice.
4. Quantify the opportunity cost for each option.
5. Incorporate opportunity cost into decision-making criteria.
6. Document assumptions and estimation methods.
7. Review opportunity cost analysis with stakeholders.
8. Update analyses as new information becomes available.
9. Use opportunity cost findings to inform future decisions.
10. Integrate opportunity cost modules into AGI03 decision engines.
        """,
        key_factors=[
            "Alternative identification",
            "Value estimation",
            "Transparency",
            "Stakeholder review",
            "Continuous update"
        ],
        primary_authority=[
            "Samuelson, P. A., & Nordhaus, W. D. (2010). Economics.",
            "Mankiw, N. G. (2017). Principles of Economics."
        ],
        burden_holder="Decision maker",
        adversary_position="Opportunity cost analysis is too theoretical for practical use.",
        counter_arguments=[
            "It prevents suboptimal resource allocation.",
            "Quantitative analysis supports better decisions.",
            "Practical frameworks exist for real-world application."
        ],
        resolution_strategy="Showcase case studies where opportunity cost analysis improved outcomes.",
        entity_scope="All AGI03 decision modules",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="AGI01:OpportunityCostDoctrine"
    ),
    DoctrineBlock(
        topic="Risk-Reward Balancing and Expected Value Analysis",
        keywords=[
            "risk-reward", "expected value", "decision analysis", "uncertainty", "probability", "payoff"
        ],
        conclusion_template="Balance risk and reward using expected value analysis for all significant decisions.",
        reasoning_framework="""
1. Identify possible outcomes for each decision.
2. Estimate the probability and payoff for each outcome.
3. Calculate the expected value: sum of (probability x payoff) for all outcomes.
4. Assess risk tolerance and organizational risk appetite.
5. Compare expected values across alternatives.
6. Consider variance and downside risk, not just mean expected value.
7. Document assumptions and estimation methods.
8. Use sensitivity analysis to test robustness of decisions.
9. Review findings with stakeholders.
10. Integrate expected value analysis into AGI03 decision protocols.
        """,
        key_factors=[
            "Outcome identification",
            "Probability estimation",
            "Payoff quantification",
            "Risk tolerance",
            "Sensitivity analysis"
        ],
        primary_authority=[
            "Raiffa, H., & Schlaifer, R. (1961). Applied Statistical Decision Theory.",
            "Savage, L. J. (1954). The Foundations of Statistics."
        ],
        burden_holder="Decision analyst",
        adversary_position="Expected value ignores qualitative factors and rare events.",
        counter_arguments=[
            "Qualitative factors can be incorporated as constraints or modifiers.",
            "Rare events can be modeled with scenario analysis.",
            "Expected value provides a rational baseline for decisions."
        ],
        resolution_strategy="Combine expected value with scenario planning for comprehensive analysis.",
        entity_scope="AGI03 risk management, strategic planning",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AGI02:ExpectedValueDoctrine"
    ),
    DoctrineBlock(
        topic="Stretch Goal Calibration (70% Achievability Target)",
        keywords=[
            "stretch goals", "calibration", "achievability", "goal setting", "performance"
        ],
        conclusion_template="Calibrate stretch goals to a 70% achievability target to maximize motivation and performance.",
        reasoning_framework="""
1. Analyze historical goal achievement data to determine baseline performance.
2. Set stretch goals that are ambitious but achievable by approximately 70% of attempts.
3. Use statistical analysis to calibrate goal difficulty.
4. Communicate the rationale for stretch targets to teams.
5. Monitor progress and adjust targets as needed.
6. Encourage learning from both successes and misses.
7. Avoid punitive measures for missed stretch goals.
8. Use stretch goal calibration to drive innovation and growth.
9. Review calibration annually to reflect changing capabilities.
10. Integrate calibration logic into AGI03 goal-setting modules.
        """,
        key_factors=[
            "Historical performance data",
            "Statistical calibration",
            "Motivation",
            "Feedback loops",
            "Continuous improvement"
        ],
        primary_authority=[
            "Locke, E. A., & Latham, G. P. (2002). Building a practically useful theory of goal setting and task motivation.",
            "Doerr, J. (2018). Measure What Matters."
        ],
        burden_holder="Goal setter",
        adversary_position="Stretch goals demotivate teams when missed.",
        counter_arguments=[
            "Proper calibration maintains achievability and motivation.",
            "Learning from misses is encouraged.",
            "70% target balances ambition and realism."
        ],
        resolution_strategy="Track engagement and performance metrics before and after calibration.",
        entity_scope="AGI03 goal-setting, leadership teams",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="AGI01:StretchGoalDoctrine"
    ),
    DoctrineBlock(
        topic="Moonshot Thinking (10x vs 10%)",
        keywords=[
            "moonshot", "10x thinking", "innovation", "radical goals", "disruptive change"
        ],
        conclusion_template="Promote moonshot thinking by encouraging 10x improvements over incremental 10% gains.",
        reasoning_framework="""
1. Challenge teams to envision solutions that are 10x better, not just 10% better.
2. Identify constraints that limit incremental thinking.
3. Foster a culture that rewards bold, high-risk ideas.
4. Allocate resources for exploratory, high-impact projects.
5. Encourage cross-disciplinary collaboration.
6. Accept higher failure rates as part of innovation.
7. Use scenario planning to assess potential impact.
8. Document lessons learned from moonshot attempts.
9. Balance moonshot projects with core business needs.
10. Integrate moonshot thinking into AGI03 innovation protocols.
        """,
        key_factors=[
            "Cultural support",
            "Resource allocation",
            "Risk tolerance",
            "Cross-disciplinary input",
            "Learning from failure"
        ],
        primary_authority=[
            "Schmidt, E., & Rosenberg, J. (2014). How Google Works.",
            "Astro Teller, X (2016). The Moonshot Factory."
        ],
        burden_holder="Innovation leader",
        adversary_position="Moonshot thinking wastes resources on unlikely successes.",
        counter_arguments=[
            "Breakthroughs require bold experimentation.",
            "Portfolio approach balances risk and reward.",
            "Incrementalism limits long-term growth."
        ],
        resolution_strategy="Allocate a fixed percentage of resources to moonshots and measure ROI.",
        entity_scope="AGI03 innovation, R&D teams",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="AGI01:MoonshotDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Alignment Across Organizational Levels",
        keywords=[
            "goal alignment", "vertical integration", "cascading goals", "strategy", "objectives"
        ],
        conclusion_template="Ensure alignment of goals from strategic to operational levels for coherent execution.",
        reasoning_framework="""
1. Define top-level strategic objectives.
2. Cascade objectives down to departmental and individual levels.
3. Ensure each lower-level goal supports a higher-level objective.
4. Use OKRs to maintain alignment and traceability.
5. Review alignment regularly in leadership meetings.
6. Adjust goals as strategy evolves.
7. Communicate alignment rationale to all stakeholders.
8. Use alignment metrics to identify gaps.
9. Integrate alignment checks into AGI03 goal workflows.
10. Document alignment processes for transparency.
        """,
        key_factors=[
            "Strategic clarity",
            "Traceability",
            "Communication",
            "Review cadence",
            "Adaptability"
        ],
        primary_authority=[
            "Kaplan, R. S., & Norton, D. P. (1996). The Balanced Scorecard.",
            "Doerr, J. (2018). Measure What Matters."
        ],
        burden_holder="Leadership",
        adversary_position="Alignment efforts slow down agility and innovation.",
        counter_arguments=[
            "Alignment prevents wasted effort and conflicting priorities.",
            "Agility is preserved through regular review and adjustment.",
            "Innovation can be an explicit strategic objective."
        ],
        resolution_strategy="Track project outcomes with and without alignment protocols.",
        entity_scope="AGI03 strategic planning, all teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AGI02:GoalAlignmentDoctrine"
    ),
    DoctrineBlock(
        topic="Dynamic Reprioritization in Response to Change",
        keywords=[
            "reprioritization", "agility", "change management", "dynamic priorities", "adaptation"
        ],
        conclusion_template="Implement dynamic reprioritization protocols to adapt to changing circumstances.",
        reasoning_framework="""
1. Monitor internal and external environments for changes.
2. Establish triggers for reprioritization (e.g., market shifts, resource changes).
3. Reassess priorities using established frameworks (Eisenhower, RICE, MoSCoW).
4. Communicate changes promptly to all stakeholders.
5. Document rationale for reprioritization decisions.
6. Minimize disruption through clear transition plans.
7. Integrate reprioritization logic into AGI03 planning modules.
8. Review effectiveness of reprioritization after implementation.
9. Foster a culture of adaptability.
10. Use feedback to improve future reprioritization protocols.
        """,
        key_factors=[
            "Change detection",
            "Clear triggers",
            "Stakeholder communication",
            "Transition planning",
            "Feedback loops"
        ],
        primary_authority=[
            "Kotter, J. P. (1996). Leading Change.",
            "Rigby, D. K., Sutherland, J., & Takeuchi, H. (2016). Embracing Agile."
        ],
        burden_holder="Project manager",
        adversary_position="Frequent reprioritization causes confusion and inefficiency.",
        counter_arguments=[
            "Structured protocols minimize confusion.",
            "Adaptability is critical in volatile environments.",
            "Communication and documentation mitigate inefficiency."
        ],
        resolution_strategy="Measure project outcomes and stakeholder satisfaction pre- and post-implementation.",
        entity_scope="AGI03 planning, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI01:DynamicReprioritizationDoctrine"
    ),
    DoctrineBlock(
        topic="Feedback-Driven Goal Adjustment",
        keywords=[
            "feedback", "goal adjustment", "continuous improvement", "learning", "agility"
        ],
        conclusion_template="Incorporate regular feedback to adjust goals and improve outcomes.",
        reasoning_framework="""
1. Establish feedback loops at all goal levels.
2. Collect quantitative and qualitative data on goal progress.
3. Analyze feedback for trends and anomalies.
4. Adjust goals, strategies, or tactics based on findings.
5. Communicate changes and rationale to stakeholders.
6. Document adjustments for transparency.
7. Integrate feedback mechanisms into AGI03 modules.
8. Foster a culture of learning and adaptation.
9. Review effectiveness of adjustments regularly.
10. Use feedback data to inform future goal setting.
        """,
        key_factors=[
            "Feedback quality",
            "Data analysis",
            "Transparency",
            "Stakeholder communication",
            "Continuous learning"
        ],
        primary_authority=[
            "Argyris, C., & Schön, D. A. (1978). Organizational Learning.",
            "Deming, W. E. (1986). Out of the Crisis."
        ],
        burden_holder="Goal owner",
        adversary_position="Frequent adjustments undermine commitment and focus.",
        counter_arguments=[
            "Adjustments are data-driven, not arbitrary.",
            "Commitment is maintained through transparent communication.",
            "Continuous improvement leads to better outcomes."
        ],
        resolution_strategy="Track goal achievement rates and stakeholder sentiment over time.",
        entity_scope="AGI03 goal management, all teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AGI02:FeedbackAdjustmentDoctrine"
    ),
    DoctrineBlock(
        topic="Transparent Decision Documentation",
        keywords=[
            "transparency", "decision documentation", "audit trail", "accountability", "traceability"
        ],
        conclusion_template="Mandate transparent documentation of all major decisions for accountability and learning.",
        reasoning_framework="""
1. Record the rationale, alternatives, and criteria for each major decision.
2. Document participants and their roles.
3. Store decision records in a centralized, accessible repository.
4. Review documentation for completeness and clarity.
5. Use decision logs for audits and post-mortems.
6. Encourage a culture of openness and accountability.
7. Integrate documentation protocols into AGI03 workflows.
8. Protect sensitive information while maintaining transparency.
9. Analyze decision records to identify patterns and improve future decisions.
10. Regularly update documentation standards.
        """,
        key_factors=[
            "Documentation quality",
            "Accessibility",
            "Accountability",
            "Continuous improvement",
            "Data security"
        ],
        primary_authority=[
            "Senge, P. M. (1990). The Fifth Discipline.",
            "ISO 9001:2015 Quality Management Systems."
        ],
        burden_holder="Decision maker",
        adversary_position="Documentation slows down decision-making and adds bureaucracy.",
        counter_arguments=[
            "Transparency improves accountability and learning.",
            "Efficient templates and tools minimize overhead.",
            "Documentation prevents repeated mistakes."
        ],
        resolution_strategy="Automate documentation and measure process efficiency.",
        entity_scope="AGI03 decision modules, all teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI01:DecisionDocumentationDoctrine"
    ),
    DoctrineBlock(
        topic="Cross-Functional Collaboration for Goal Achievement",
        keywords=[
            "collaboration", "cross-functional", "teamwork", "goal achievement", "synergy"
        ],
        conclusion_template="Promote cross-functional collaboration to leverage diverse expertise for goal achievement.",
        reasoning_framework="""
1. Identify goals requiring input from multiple disciplines.
2. Form cross-functional teams with relevant expertise.
3. Establish clear roles and responsibilities.
4. Facilitate regular communication and knowledge sharing.
5. Use collaborative tools to coordinate efforts.
6. Recognize and resolve inter-team conflicts promptly.
7. Measure and reward collaborative outcomes.
8. Integrate collaboration protocols into AGI03 workflows.
9. Review effectiveness of cross-functional teams regularly.
10. Document best practices and lessons learned.
        """,
        key_factors=[
            "Team composition",
            "Communication",
            "Conflict resolution",
            "Shared incentives",
            "Continuous review"
        ],
        primary_authority=[
            "Katzenbach, J. R., & Smith, D. K. (1993). The Wisdom of Teams.",
            "Edmondson, A. C. (2012). Teaming: How Organizations Learn, Innovate, and Compete in the Knowledge Economy."
        ],
        burden_holder="Team leader",
        adversary_position="Cross-functional teams slow down execution due to coordination overhead.",
        counter_arguments=[
            "Diverse expertise leads to better solutions.",
            "Coordination tools and protocols minimize overhead.",
            "Collaboration improves adaptability and innovation."
        ],
        resolution_strategy="Track project outcomes and time-to-delivery for collaborative versus siloed teams.",
        entity_scope="AGI03 goal execution, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI02:CrossFunctionalDoctrine"
    ),
    DoctrineBlock(
        topic="Timeboxing for Focused Execution",
        keywords=[
            "timeboxing", "focus", "execution", "productivity", "deadline"
        ],
        conclusion_template="Apply timeboxing to constrain work periods and enhance execution focus.",
        reasoning_framework="""
1. Define fixed time intervals (timeboxes) for specific tasks or goals.
2. Set clear objectives for each timebox.
3. Prohibit scope changes during the timebox.
4. Review progress at the end of each timebox.
5. Adjust future timeboxes based on outcomes and learnings.
6. Use timeboxing to prevent perfectionism and analysis paralysis.
7. Integrate timeboxing protocols into AGI03 scheduling modules.
8. Communicate timebox boundaries to all stakeholders.
9. Measure productivity and goal achievement rates.
10. Foster a culture of focused execution.
        """,
        key_factors=[
            "Timebox length",
            "Objective clarity",
            "Scope discipline",
            "Review cadence",
            "Cultural adoption"
        ],
        primary_authority=[
            "Schwaber, K., & Sutherland, J. (2017). The Scrum Guide.",
            "Pomodoro Technique (Cirillo, F. 2006)."
        ],
        burden_holder="Task owner",
        adversary_position="Timeboxing is artificial and disrupts natural workflow.",
        counter_arguments=[
            "Timeboxing enhances focus and prevents overwork.",
            "It enables predictable planning and review.",
            "Flexibility can be built in between timeboxes."
        ],
        resolution_strategy="Pilot timeboxing and measure impact on delivery speed and quality.",
        entity_scope="AGI03 execution modules, all teams",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="AGI01:TimeboxingDoctrine"
    ),
    DoctrineBlock(
        topic="Scenario Planning for Strategic Resilience",
        keywords=[
            "scenario planning", "strategic resilience", "uncertainty", "future-proofing", "contingency"
        ],
        conclusion_template="Use scenario planning to prepare for multiple plausible futures and enhance strategic resilience.",
        reasoning_framework="""
1. Identify key uncertainties and driving forces.
2. Develop a set of diverse, plausible scenarios.
3. Assess the impact of each scenario on current goals and plans.
4. Formulate contingency strategies for each scenario.
5. Monitor indicators that signal scenario emergence.
6. Update scenarios and strategies as new information arises.
7. Engage cross-functional teams in scenario development.
8. Integrate scenario planning into AGI03 strategic modules.
9. Communicate scenarios and plans to stakeholders.
10. Review scenario effectiveness post-event.
        """,
        key_factors=[
            "Uncertainty identification",
            "Scenario diversity",
            "Contingency planning",
            "Monitoring indicators",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "Schoemaker, P. J. H. (1995). Scenario Planning: A Tool for Strategic Thinking.",
            "Wack, P. (1985). Scenarios: Uncharted Waters Ahead."
        ],
        burden_holder="Strategic planner",
        adversary_position="Scenario planning is speculative and distracts from execution.",
        counter_arguments=[
            "Preparation reduces response time to change.",
            "Scenarios inform risk management and resource allocation.",
            "Engagement in planning increases buy-in."
        ],
        resolution_strategy="Track organizational resilience and response speed to external shocks.",
        entity_scope="AGI03 strategic planning, leadership",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI02:ScenarioPlanningDoctrine"
    ),
    DoctrineBlock(
        topic="Continuous Learning and Knowledge Integration",
        keywords=[
            "continuous learning", "knowledge integration", "organizational learning", "improvement", "adaptation"
        ],
        conclusion_template="Foster continuous learning and integrate new knowledge into goals and processes.",
        reasoning_framework="""
1. Encourage ongoing education and skill development.
2. Capture lessons learned from projects and initiatives.
3. Integrate new knowledge into existing processes and goals.
4. Use retrospectives and after-action reviews.
5. Share knowledge across teams and functions.
6. Reward learning and knowledge sharing behaviors.
7. Update AGI03 modules with new best practices.
8. Monitor the impact of knowledge integration.
9. Address barriers to learning and adaptation.
10. Review and refine learning protocols regularly.
        """,
        key_factors=[
            "Learning culture",
            "Knowledge capture",
            "Integration mechanisms",
            "Incentives",
            "Impact measurement"
        ],
        primary_authority=[
            "Senge, P. M. (1990). The Fifth Discipline.",
            "Argyris, C., & Schön, D. A. (1978). Organizational Learning."
        ],
        burden_holder="Learning officer",
        adversary_position="Continuous learning distracts from core work and slows progress.",
        counter_arguments=[
            "Learning improves long-term performance.",
            "Knowledge integration prevents repeated mistakes.",
            "Time invested in learning yields exponential returns."
        ],
        resolution_strategy="Track performance metrics before and after learning interventions.",
        entity_scope="AGI03 all modules, all teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AGI01:ContinuousLearningDoctrine"
    ),
    DoctrineBlock(
        topic="Bias Mitigation in Goal Setting and Prioritization",
        keywords=[
            "bias mitigation", "cognitive bias", "decision quality", "objectivity", "goal setting"
        ],
        conclusion_template="Implement protocols to identify and mitigate cognitive biases in goal setting and prioritization.",
        reasoning_framework="""
1. Educate teams on common cognitive biases (e.g., anchoring, confirmation bias).
2. Use structured frameworks (e.g., RICE, MoSCoW) to reduce subjectivity.
3. Encourage diverse perspectives in goal discussions.
4. Apply checklists and debiasing techniques during decision meetings.
5. Review decisions for evidence of bias.
6. Document identified biases and mitigation actions.
7. Integrate bias detection into AGI03 modules.
8. Foster a culture of critical thinking and challenge.
9. Use data-driven approaches to validate decisions.
10. Regularly review and update bias mitigation protocols.
        """,
        key_factors=[
            "Bias awareness",
            "Framework adoption",
            "Diversity of input",
            "Documentation",
            "Continuous review"
        ],
        primary_authority=[
            "Kahneman, D. (2011). Thinking, Fast and Slow.",
            "Bazerman, M. H., & Moore, D. A. (2012). Judgment in Managerial Decision Making."
        ],
        burden_holder="Decision facilitator",
        adversary_position="Bias mitigation slows down decision-making and is unnecessary.",
        counter_arguments=[
            "Bias leads to poor decisions and wasted resources.",
            "Structured frameworks increase speed and quality.",
            "Debiasing improves long-term outcomes."
        ],
        resolution_strategy="Analyze decision quality and outcomes with and without bias mitigation.",
        entity_scope="AGI03 goal and prioritization modules",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI02:BiasMitigationDoctrine"
    ),
    DoctrineBlock(
        topic="Stakeholder Engagement in Goal Setting",
        keywords=[
            "stakeholder engagement", "goal setting", "buy-in", "participation", "alignment"
        ],
        conclusion_template="Engage stakeholders in goal setting to ensure buy-in and alignment.",
        reasoning_framework="""
1. Identify all relevant stakeholders for each goal.
2. Involve stakeholders early in the goal-setting process.
3. Facilitate open discussions to capture diverse perspectives.
4. Document stakeholder input and rationale for decisions.
5. Communicate final goals and decision logic transparently.
6. Address concerns and objections constructively.
7. Review stakeholder satisfaction post-implementation.
8. Integrate engagement protocols into AGI03 workflows.
9. Use feedback to improve future engagement.
10. Foster a culture of inclusion and participation.
        """,
        key_factors=[
            "Stakeholder identification",
            "Early involvement",
            "Transparent communication",
            "Feedback mechanisms",
            "Continuous improvement"
        ],
        primary_authority=[
            "Freeman, R. E. (1984). Strategic Management: A Stakeholder Approach.",
            "Bryson, J. M. (2018). Strategic Planning for Public and Nonprofit Organizations."
        ],
        burden_holder="Goal owner",
        adversary_position="Stakeholder engagement slows down goal setting and leads to compromise.",
        counter_arguments=[
            "Engagement increases buy-in and execution success.",
            "Structured protocols minimize delays.",
            "Diverse input improves goal quality."
        ],
        resolution_strategy="Track goal achievement and stakeholder satisfaction rates.",
        entity_scope="AGI03 goal-setting, all teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AGI01:StakeholderEngagementDoctrine"
    ),
    DoctrineBlock(
        topic="Minimum Viable Goal (MVG) Definition",
        keywords=[
            "minimum viable goal", "MVG", "lean", "goal definition", "iteration"
        ],
        conclusion_template="Define minimum viable goals to enable rapid iteration and learning.",
        reasoning_framework="""
1. Identify the smallest goal that delivers meaningful value.
2. Prioritize speed of implementation and feedback over completeness.
3. Use MVG as a stepping stone to larger objectives.
4. Test and validate assumptions with each MVG iteration.
5. Adjust subsequent goals based on learnings.
6. Communicate MVG rationale to stakeholders.
7. Integrate MVG protocols into AGI03 goal workflows.
8. Document outcomes and lessons learned.
9. Use MVG to reduce risk and resource waste.
10. Review MVG effectiveness regularly.
        """,
        key_factors=[
            "Value delivery",
            "Speed of iteration",
            "Assumption testing",
            "Feedback integration",
            "Risk reduction"
        ],
        primary_authority=[
            "Ries, E. (2011). The Lean Startup.",
            "Blank, S. (2013). The Four Steps to the Epiphany."
        ],
        burden_holder="Goal owner",
        adversary_position="MVG leads to under-ambitious goals and incrementalism.",
        counter_arguments=[
            "MVG enables rapid learning and course correction.",
            "It reduces risk and resource waste.",
            "Ambitious goals can be built from validated MVGs."
        ],
        resolution_strategy="Measure speed and quality of goal achievement with and without MVG.",
        entity_scope="AGI03 goal-setting, innovation teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI02:MVGDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Traceability and Auditability",
        keywords=[
            "traceability", "auditability", "goal tracking", "compliance", "transparency"
        ],
        conclusion_template="Ensure all goals are traceable and auditable from inception to completion.",
        reasoning_framework="""
1. Assign unique identifiers to all goals.
2. Document the rationale, dependencies, and responsible parties.
3. Track progress and changes over time.
4. Store records in a secure, accessible system.
5. Enable audits by internal and external parties.
6. Review traceability regularly for gaps.
7. Integrate traceability protocols into AGI03 modules.
8. Use audit findings to improve processes.
9. Communicate traceability requirements to all teams.
10. Maintain records for regulatory and learning purposes.
        """,
        key_factors=[
            "Unique identification",
            "Comprehensive documentation",
            "Secure storage",
            "Audit readiness",
            "Continuous review"
        ],
        primary_authority=[
            "ISO 9001:2015 Quality Management Systems.",
            "CMMI Institute (2018). Capability Maturity Model Integration."
        ],
        burden_holder="Goal owner",
        adversary_position="Traceability adds unnecessary overhead and slows progress.",
        counter_arguments=[
            "Traceability ensures accountability and compliance.",
            "Efficient tools minimize overhead.",
            "Auditability supports continuous improvement."
        ],
        resolution_strategy="Automate traceability and measure process efficiency.",
        entity_scope="AGI03 goal management, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI01:GoalTraceabilityDoctrine"
    ),
    DoctrineBlock(
        topic="Resource Buffering for Uncertainty",
        keywords=[
            "resource buffering", "uncertainty", "risk management", "contingency", "resource allocation"
        ],
        conclusion_template="Allocate resource buffers to absorb uncertainty and prevent project overruns.",
        reasoning_framework="""
1. Identify sources of uncertainty in project plans.
2. Quantify potential impact on resource needs.
3. Allocate buffers (time, budget, personnel) proportional to risk.
4. Monitor buffer usage throughout execution.
5. Adjust buffers as new information emerges.
6. Communicate buffer rationale to stakeholders.
7. Integrate buffering protocols into AGI03 resource allocation.
8. Review buffer effectiveness post-project.
9. Use buffer data to improve future estimates.
10. Avoid over-buffering to maximize efficiency.
        """,
        key_factors=[
            "Uncertainty quantification",
            "Buffer sizing",
            "Monitoring",
            "Stakeholder communication",
            "Continuous improvement"
        ],
        primary_authority=[
            "Goldratt, E. M. (1997). Critical Chain.",
            "PMI (2017). A Guide to the Project Management Body of Knowledge (PMBOK Guide)."
        ],
        burden_holder="Project manager",
        adversary_position="Buffers waste resources and encourage inefficiency.",
        counter_arguments=[
            "Buffers prevent costly overruns and missed deadlines.",
            "Data-driven sizing minimizes waste.",
            "Transparency ensures accountability."
        ],
        resolution_strategy="Track project outcomes with and without resource buffers.",
        entity_scope="AGI03 resource modules, project teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI02:ResourceBufferingDoctrine"
    ),
    DoctrineBlock(
        topic="Key Performance Indicator (KPI) Integration",
        keywords=[
            "KPI", "key performance indicator", "measurement", "goal tracking", "performance"
        ],
        conclusion_template="Integrate KPIs into goal tracking to measure and drive performance.",
        reasoning_framework="""
1. Define KPIs aligned with strategic objectives.
2. Ensure KPIs are specific, measurable, and actionable.
3. Assign ownership for each KPI.
4. Track KPI progress regularly and transparently.
5. Use KPIs to inform decision-making and resource allocation.
6. Review and update KPIs as goals evolve.
7. Integrate KPI tracking into AGI03 modules.
8. Communicate KPI results to stakeholders.
9. Use KPI data for performance reviews and incentives.
10. Analyze KPI trends for continuous improvement.
        """,
        key_factors=[
            "Strategic alignment",
            "Measurability",
            "Ownership",
            "Transparency",
            "Continuous review"
        ],
        primary_authority=[
            "Parmenter, D. (2015). Key Performance Indicators.",
            "Kaplan, R. S., & Norton, D. P. (1996). The Balanced Scorecard."
        ],
        burden_holder="KPI owner",
        adversary_position="KPIs encourage gaming and narrow focus.",
        counter_arguments=[
            "Balanced KPIs prevent gaming.",
            "Transparency and review mitigate narrow focus.",
            "KPIs drive accountability and results."
        ],
        resolution_strategy="Use a balanced scorecard approach and review for unintended consequences.",
        entity_scope="AGI03 performance modules, all teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AGI01:KPIDoctrine"
    ),
    DoctrineBlock(
        topic="Automated Goal Progress Monitoring",
        keywords=[
            "automation", "goal monitoring", "progress tracking", "real-time", "alerts"
        ],
        conclusion_template="Implement automated monitoring of goal progress with real-time alerts for deviations.",
        reasoning_framework="""
1. Instrument goals with measurable indicators.
2. Use AGI03 modules to collect and analyze progress data in real time.
3. Set thresholds for acceptable progress and deviations.
4. Trigger alerts when deviations are detected.
5. Provide dashboards for transparent monitoring.
6. Review alert effectiveness and adjust thresholds as needed.
7. Integrate monitoring with feedback and adjustment protocols.
8. Ensure data privacy and security.
9. Document monitoring processes and outcomes.
10. Use monitoring data to inform future goal setting.
        """,
        key_factors=[
            "Instrumentation",
            "Threshold setting",
            "Alert responsiveness",
            "Transparency",
            "Data security"
        ],
        primary_authority=[
            "Davenport, T. H., & Harris, J. G. (2007). Competing on Analytics.",
            "ISO/IEC 27001:2013 Information Security Management."
        ],
        burden_holder="Goal owner",
        adversary_position="Automation leads to false alarms and over-reliance on data.",
        counter_arguments=[
            "Thresholds can be tuned to minimize false alarms.",
            "Automation increases speed and accuracy of response.",
            "Human oversight complements automated systems."
        ],
        resolution_strategy="Pilot automated monitoring and measure impact on goal achievement.",
        entity_scope="AGI03 monitoring modules, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI02:AutomatedMonitoringDoctrine"
    ),
    DoctrineBlock(
        topic="Ethical Considerations in Goal Selection",
        keywords=[
            "ethics", "goal selection", "responsibility", "impact assessment", "values"
        ],
        conclusion_template="Incorporate ethical considerations into all goal selection and prioritization processes.",
        reasoning_framework="""
1. Assess potential ethical impacts of proposed goals.
2. Consult organizational values and external standards.
3. Engage diverse stakeholders in ethical review.
4. Document ethical considerations and mitigation plans.
5. Reject or revise goals with unacceptable ethical risks.
6. Integrate ethics checks into AGI03 goal workflows.
7. Review ethical outcomes post-implementation.
8. Provide ethics training to goal setters.
9. Foster a culture of responsibility and integrity.
10. Update ethical protocols as standards evolve.
        """,
        key_factors=[
            "Impact assessment",
            "Stakeholder engagement",
            "Documentation",
            "Continuous review",
            "Cultural support"
        ],
        primary_authority=[
            "Floridi, L. (2013). The Ethics of Information.",
            "IEEE Global Initiative on Ethics of Autonomous and Intelligent Systems (2019)."
        ],
        burden_holder="Goal setter",
        adversary_position="Ethical reviews slow down innovation and are subjective.",
        counter_arguments=[
            "Ethics prevent harm and reputational damage.",
            "Structured protocols increase speed and objectivity.",
            "Ethical lapses have long-term costs."
        ],
        resolution_strategy="Track ethical incidents and stakeholder trust metrics.",
        entity_scope="AGI03 goal selection, all teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AGI01:EthicsDoctrine"
    ),
    DoctrineBlock(
        topic="Red Teaming for Goal Robustness",
        keywords=[
            "red teaming", "robustness", "challenge", "adversarial review", "goal testing"
        ],
        conclusion_template="Use red teaming to challenge and strengthen goal definitions and plans.",
        reasoning_framework="""
1. Form independent teams to critically assess goals and plans.
2. Identify vulnerabilities, assumptions, and blind spots.
3. Simulate adversarial scenarios and stress tests.
4. Document findings and recommendations.
5. Revise goals and plans based on red team input.
6. Foster a culture of constructive challenge.
7. Integrate red teaming into AGI03 goal workflows.
8. Review effectiveness of red teaming interventions.
9. Protect psychological safety during challenge processes.
10. Use lessons learned to improve future goal setting.
        """,
        key_factors=[
            "Independence",
            "Critical assessment",
            "Documentation",
            "Psychological safety",
            "Continuous improvement"
        ],
        primary_authority=[
            "Zenko, M. (2015). Red Team: How to Succeed By Thinking Like the Enemy.",
            "US Department of Defense (2019). Red Teaming Guide."
        ],
        burden_holder="Goal owner",
        adversary_position="Red teaming creates conflict and delays progress.",
        counter_arguments=[
            "Challenge strengthens plans and prevents failure.",
            "Protocols maintain psychological safety and focus.",
            "Delays are offset by reduced risk of failure."
        ],
        resolution_strategy="Track goal success rates and post-mortem findings.",
        entity_scope="AGI03 planning, all teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI02:RedTeamingDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Dependency Mapping",
        keywords=[
            "dependency mapping", "goal relationships", "critical path", "sequencing", "risk"
        ],
        conclusion_template="Map dependencies among goals to optimize sequencing and manage risk.",
        reasoning_framework="""
1. Identify all goals and subgoals.
2. Document dependencies (precedence, resource, informational).
3. Visualize dependencies using graphs or matrices.
4. Identify critical paths and bottlenecks.
5. Sequence goals to optimize resource use and minimize risk.
6. Review and update dependency maps as goals evolve.
7. Integrate mapping into AGI03 planning modules.
8. Communicate dependencies to all stakeholders.
9. Use dependency data for risk analysis and mitigation.
10. Archive maps for future reference and learning.
        """,
        key_factors=[
            "Comprehensive identification",
            "Visualization",
            "Critical path analysis",
            "Stakeholder communication",
            "Continuous update"
        ],
        primary_authority=[
            "Project Management Institute (2017). PMBOK Guide.",
            "Kerzner, H. (2017). Project Management: A Systems Approach."
        ],
        burden_holder="Project manager",
        adversary_position="Dependency mapping is too complex for fast-moving projects.",
        counter_arguments=[
            "Mapping prevents missed dependencies and rework.",
            "Tools and templates simplify the process.",
            "Fast-moving projects benefit from risk reduction."
        ],
        resolution_strategy="Pilot mapping and track project outcomes.",
        entity_scope="AGI03 planning modules, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI01:DependencyMappingDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Abandonment Protocols",
        keywords=[
            "goal abandonment", "sunsetting", "resource reallocation", "failure management", "pivot"
        ],
        conclusion_template="Establish protocols for timely abandonment of goals that are no longer viable.",
        reasoning_framework="""
1. Define clear criteria for goal abandonment (e.g., missed milestones, changed context).
2. Monitor progress and trigger reviews when criteria are met.
3. Engage stakeholders in abandonment decisions.
4. Document rationale and lessons learned.
5. Reallocate resources promptly to higher-value goals.
6. Communicate abandonment decisions transparently.
7. Integrate protocols into AGI03 goal management.
8. Review abandonment outcomes for process improvement.
9. Foster a culture that values learning from failure.
10. Archive abandoned goals for future reference.
        """,
        key_factors=[
            "Clear criteria",
            "Monitoring",
            "Stakeholder engagement",
            "Resource reallocation",
            "Learning culture"
        ],
        primary_authority=[
            "Christensen, C. M. (1997). The Innovator's Dilemma.",
            "Blank, S. (2013). The Four Steps to the Epiphany."
        ],
        burden_holder="Goal owner",
        adversary_position="Abandonment signals failure and demoralizes teams.",
        counter_arguments=[
            "Timely abandonment prevents resource waste.",
            "Learning from failure improves future outcomes.",
            "Transparent protocols maintain morale."
        ],
        resolution_strategy="Track resource utilization and team sentiment.",
        entity_scope="AGI03 goal management, all teams",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="AGI02:GoalAbandonmentDoctrine"
    ),
    DoctrineBlock(
        topic="Strategic Goal Bundling",
        keywords=[
            "goal bundling", "synergy", "strategic alignment", "resource efficiency", "portfolio management"
        ],
        conclusion_template="Bundle related goals strategically to maximize synergy and resource efficiency.",
        reasoning_framework="""
1. Identify goals with overlapping objectives, resources, or stakeholders.
2. Analyze potential synergies and conflicts.
3. Bundle compatible goals into strategic initiatives.
4. Allocate resources at the bundle level for efficiency.
5. Monitor bundle progress and adjust as needed.
6. Communicate bundling rationale to stakeholders.
7. Integrate bundling protocols into AGI03 planning.
8. Review bundle outcomes for continuous improvement.
9. Unbundle goals if synergies do not materialize.
10. Archive bundling decisions for future reference.
        """,
        key_factors=[
            "Synergy analysis",
            "Resource allocation",
            "Monitoring",
            "Stakeholder communication",
            "Continuous improvement"
        ],
        primary_authority=[
            "Kaplan, R. S., & Norton, D. P. (2006). Alignment: Using the Balanced Scorecard.",
            "PMI (2017). Portfolio Management Standard."
        ],
        burden_holder="Portfolio manager",
        adversary_position="Bundling creates complexity and dilutes focus.",
        counter_arguments=[
            "Synergy increases impact and efficiency.",
            "Clear protocols manage complexity.",
            "Unbundling is possible if needed."
        ],
        resolution_strategy="Track resource utilization and outcome metrics.",
        entity_scope="AGI03 strategic planning, all teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI01:GoalBundlingDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Visualization for Stakeholder Engagement",
        keywords=[
            "goal visualization", "stakeholder engagement", "communication", "transparency", "alignment"
        ],
        conclusion_template="Use visualizations to communicate goals and progress for enhanced stakeholder engagement.",
        reasoning_framework="""
1. Select appropriate visualization tools (e.g., Gantt charts, dashboards).
2. Map goals, dependencies, and progress visually.
3. Update visualizations in real time as data changes.
4. Share visualizations with all relevant stakeholders.
5. Use visuals to facilitate discussions and decision-making.
6. Integrate visualization protocols into AGI03 modules.
7. Review effectiveness of visualizations for engagement.
8. Solicit stakeholder feedback on visualization utility.
9. Iterate on visualization design for clarity and impact.
10. Archive visualizations for future reference.
        """,
        key_factors=[
            "Tool selection",
            "Data accuracy",
            "Real-time updates",
            "Stakeholder feedback",
            "Continuous improvement"
        ],
        primary_authority=[
            "Few, S. (2012). Show Me the Numbers.",
            "Tufte, E. R. (2001). The Visual Display of Quantitative Information."
        ],
        burden_holder="Goal owner",
        adversary_position="Visualizations distract from substantive work and are resource-intensive.",
        counter_arguments=[
            "Visuals improve understanding and alignment.",
            "Modern tools minimize resource use.",
            "Engagement increases execution success."
        ],
        resolution_strategy="Survey stakeholder engagement and goal achievement rates.",
        entity_scope="AGI03 communication modules, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI02:GoalVisualizationDoctrine"
    ),
    DoctrineBlock(
        topic="Retrospective Analysis for Continuous Improvement",
        keywords=[
            "retrospective", "continuous improvement", "post-mortem", "learning", "goal review"
        ],
        conclusion_template="Conduct regular retrospectives to analyze goal outcomes and drive continuous improvement.",
        reasoning_framework="""
1. Schedule retrospectives after major goal cycles or projects.
2. Gather data on outcomes, processes, and stakeholder experiences.
3. Facilitate open, blame-free discussions.
4. Identify successes, failures, and root causes.
5. Document action items for improvement.
6. Assign ownership and deadlines for action items.
7. Integrate learnings into AGI03 modules and future goals.
8. Review implementation of action items.
9. Foster a culture of transparency and learning.
10. Archive retrospective findings for future reference.
        """,
        key_factors=[
            "Data collection",
            "Facilitation quality",
            "Action item follow-up",
            "Cultural support",
            "Documentation"
        ],
        primary_authority=[
            "Derby, E., & Larsen, D. (2006). Agile Retrospectives.",
            "Senge, P. M. (1990). The Fifth Discipline."
        ],
        burden_holder="Retrospective facilitator",
        adversary_position="Retrospectives waste time and focus on the past.",
        counter_arguments=[
            "Learning from the past prevents repeated mistakes.",
            "Retrospectives drive actionable improvements.",
            "Structured facilitation maximizes value."
        ],
        resolution_strategy="Track improvement metrics and team sentiment.",
        entity_scope="AGI03 all modules, all teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AGI01:RetrospectiveDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Ownership and Accountability",
        keywords=[
            "ownership", "accountability", "responsibility", "goal management", "execution"
        ],
        conclusion_template="Assign clear ownership and accountability for every goal to ensure execution.",
        reasoning_framework="""
1. Assign a single owner for each goal.
2. Document owner responsibilities and authority.
3. Communicate ownership assignments to all stakeholders.
4. Track progress and hold owners accountable.
5. Provide support and resources to owners.
6. Review ownership effectiveness regularly.
7. Integrate ownership protocols into AGI03 modules.
8. Address ownership gaps or conflicts promptly.
9. Recognize and reward effective ownership.
10. Archive ownership records for audit and learning.
        """,
        key_factors=[
            "Clear assignment",
            "Responsibility documentation",
            "Progress tracking",
            "Support mechanisms",
            "Recognition"
        ],
        primary_authority=[
            "Bossidy, L., & Charan, R. (2002). Execution: The Discipline of Getting Things Done.",
            "Kaplan, R. S., & Norton, D. P. (1996). The Balanced Scorecard."
        ],
        burden_holder="Goal owner",
        adversary_position="Ownership creates blame culture and discourages collaboration.",
        counter_arguments=[
            "Ownership clarifies responsibility and drives execution.",
            "Collaboration is encouraged through shared goals.",
            "Recognition balances accountability."
        ],
        resolution_strategy="Monitor goal achievement and team dynamics.",
        entity_scope="AGI03 goal management, all teams",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="AGI02:GoalOwnershipDoctrine"
    ),
    DoctrineBlock(
        topic="Time-to-Value Optimization",
        keywords=[
            "time-to-value", "speed", "value delivery", "optimization", "agility"
        ],
        conclusion_template="Optimize time-to-value by prioritizing goals and tasks that deliver rapid impact.",
        reasoning_framework="""
1. Identify goals and tasks with the highest potential for rapid value delivery.
2. Prioritize these in planning and resource allocation.
3. Use MVP/MVG approaches to accelerate delivery.
4. Track time-to-value metrics for all major initiatives.
5. Adjust priorities based on real-time feedback.
6. Communicate time-to-value rationale to stakeholders.
7. Integrate optimization protocols into AGI03 planning.
8. Review outcomes and refine approaches regularly.
9. Balance speed with quality and sustainability.
10. Archive time-to-value data for future reference.
        """,
        key_factors=[
            "Value identification",
            "Prioritization",
            "Measurement",
            "Feedback integration",
            "Continuous improvement"
        ],
        primary_authority=[
            "McGrath, R. G., & MacMillan, I. C. (1995). Discovery-Driven Planning.",
            "Ries, E. (2011). The Lean Startup."
        ],
        burden_holder="Project manager",
        adversary_position="Speed sacrifices quality and increases risk.",
        counter_arguments=[
            "Protocols balance speed with quality.",
            "Rapid value delivery increases stakeholder satisfaction.",
            "Feedback loops enable course correction."
        ],
        resolution_strategy="Track value delivery speed and quality metrics.",
        entity_scope="AGI03 planning, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI01:TimeToValueDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Hierarchy Visualization",
        keywords=[
            "goal hierarchy", "visualization", "structure", "traceability", "alignment"
        ],
        conclusion_template="Visualize goal hierarchies to clarify structure and support alignment.",
        reasoning_framework="""
1. Map goals and subgoals in a hierarchical structure.
2. Use tree diagrams or mind maps for visualization.
3. Update visualizations as goals evolve.
4. Share hierarchies with all relevant stakeholders.
5. Use visualizations to identify gaps and overlaps.
6. Integrate hierarchy visualization into AGI03 modules.
7. Review effectiveness for alignment and understanding.
8. Solicit stakeholder feedback for improvement.
9. Archive visualizations for future reference.
10. Use hierarchy data for traceability and audits.
        """,
        key_factors=[
            "Accurate mapping",
            "Tool selection",
            "Stakeholder communication",
            "Continuous update",
            "Traceability"
        ],
        primary_authority=[
            "Ghallab, M., Nau, D., & Traverso, P. (2004). Automated Planning: Theory and Practice.",
            "Few, S. (2012). Show Me the Numbers."
        ],
        burden_holder="Goal owner",
        adversary_position="Hierarchy visualizations are unnecessary and resource-intensive.",
        counter_arguments=[
            "Visuals improve clarity and alignment.",
            "Modern tools minimize resource use.",
            "Traceability supports audits and learning."
        ],
        resolution_strategy="Survey stakeholder understanding and project outcomes.",
        entity_scope="AGI03 planning modules, all teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI02:GoalHierarchyVisualizationDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Interdependency Risk Analysis",
        keywords=[
            "interdependency", "risk analysis", "goal relationships", "failure propagation", "mitigation"
        ],
        conclusion_template="Analyze risks arising from goal interdependencies and implement mitigation strategies.",
        reasoning_framework="""
1. Identify all goal interdependencies.
2. Assess the risk of failure propagation across goals.
3. Quantify risk impact and likelihood.
4. Develop mitigation strategies for high-risk interdependencies.
5. Monitor interdependency risks throughout execution.
6. Communicate risks and mitigations to stakeholders.
7. Integrate risk analysis into AGI03 planning modules.
8. Review effectiveness of mitigations post-execution.
9. Update risk analysis as goals and dependencies evolve.
10. Archive risk findings for future reference.
        """,
        key_factors=[
            "Comprehensive identification",
            "Risk quantification",
            "Mitigation planning",
            "Monitoring",
            "Continuous update"
        ],
        primary_authority=[
            "Project Management Institute (2017). PMBOK Guide.",
            "Kerzner, H. (2017). Project Management: A Systems Approach."
        ],
        burden_holder="Risk manager",
        adversary_position="Interdependency risk analysis is too complex and slows progress.",
        counter_arguments=[
            "Unmanaged risks lead to cascading failures.",
            "Structured analysis prevents surprises.",
            "Tools simplify risk quantification."
        ],
        resolution_strategy="Track project outcomes and risk incidents.",
        entity_scope="AGI03 planning modules, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI01:InterdependencyRiskDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Lifecycle Management",
        keywords=[
            "goal lifecycle", "initiation", "execution", "closure", "review", "continuous improvement"
        ],
        conclusion_template="Manage goals through a defined lifecycle from initiation to closure and review.",
        reasoning_framework="""
1. Define stages: initiation, planning, execution, monitoring, closure, review.
2. Assign responsibilities for each stage.
3. Document progress and decisions at each stage.
4. Review goal status regularly and adjust as needed.
5. Close goals formally and document outcomes.
6. Conduct post-closure reviews for learning.
7. Integrate lifecycle management into AGI03 modules.
8. Communicate lifecycle protocols to all teams.
9. Archive lifecycle records for audits and improvement.
10. Refine lifecycle stages based on feedback and outcomes.
        """,
        key_factors=[
            "Stage definition",
            "Responsibility assignment",
            "Documentation",
            "Review cadence",
            "Continuous improvement"
        ],
        primary_authority=[
            "PMI (2017). A Guide to the Project Management Body of Knowledge (PMBOK Guide).",
            "CMMI Institute (2018). Capability Maturity Model Integration."
        ],
        burden_holder="Project manager",
        adversary_position="Lifecycle management adds bureaucracy and slows execution.",
        counter_arguments=[
            "Lifecycle protocols ensure completeness and learning.",
            "Templates and tools minimize overhead.",
            "Continuous improvement increases efficiency."
        ],
        resolution_strategy="Track goal completion rates and process efficiency.",
        entity_scope="AGI03 goal management, all teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AGI02:GoalLifecycleDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Value Realization Tracking",
        keywords=[
            "value realization", "tracking", "benefit measurement", "ROI", "goal outcomes"
        ],
        conclusion_template="Track value realization for all goals to ensure intended benefits are achieved.",
        reasoning_framework="""
1. Define value metrics for each goal at inception.
2. Track value delivery throughout execution.
3. Compare actual outcomes to expected benefits.
4. Document deviations and root causes.
5. Use findings to inform future goal setting and prioritization.
6. Integrate value tracking into AGI03 modules.
7. Communicate value realization to stakeholders.
8. Review value realization post-closure.
9. Archive value data for audits and learning.
10. Refine value tracking protocols based on feedback.
        """,
        key_factors=[
            "Metric definition",
            "Tracking mechanisms",
            "Deviation analysis",
            "Stakeholder communication",
            "Continuous improvement"
        ],
        primary_authority=[
            "Thorp, J. (2003). The Information Paradox.",
            "Kaplan, R. S., & Norton, D. P. (1996). The Balanced Scorecard."
        ],
        burden_holder="Goal owner",
        adversary_position="Value tracking is subjective and resource-intensive.",
        counter_arguments=[
            "Clear metrics increase objectivity.",
            "Automation reduces resource use.",
            "Value realization drives prioritization and learning."
        ],
        resolution_strategy="Automate value tracking and review outcomes.",
        entity_scope="AGI03 goal management, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI01:ValueTrackingDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Decomposition for Parallel Execution",
        keywords=[
            "goal decomposition", "parallel execution", "task splitting", "efficiency", "resource utilization"
        ],
        conclusion_template="Decompose goals to enable parallel execution and maximize efficiency.",
        reasoning_framework="""
1. Break down complex goals into independent subgoals.
2. Identify tasks that can be executed in parallel.
3. Allocate resources to parallel streams.
4. Monitor progress and synchronize at integration points.
5. Adjust decomposition as dependencies or constraints change.
6. Communicate parallelization plans to stakeholders.
7. Integrate decomposition protocols into AGI03 planning.
8. Review efficiency gains and resource utilization.
9. Archive decomposition strategies for future reference.
10. Refine decomposition based on outcomes and feedback.
        """,
        key_factors=[
            "Task independence",
            "Resource allocation",
            "Synchronization",
            "Monitoring",
            "Continuous refinement"
        ],
        primary_authority=[
            "Ghallab, M., Nau, D., & Traverso, P. (2004). Automated Planning: Theory and Practice.",
            "Kerzner, H. (2017). Project Management: A Systems Approach."
        ],
        burden_holder="Project manager",
        adversary_position="Parallel execution increases coordination complexity and risk.",
        counter_arguments=[
            "Decomposition enables faster delivery.",
            "Protocols manage coordination and risk.",
            "Efficiency gains outweigh added complexity."
        ],
        resolution_strategy="Track delivery speed and coordination incidents.",
        entity_scope="AGI03 planning modules, all teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI02:ParallelDecompositionDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Review and Renewal Protocols",
        keywords=[
            "goal review", "renewal", "continuous improvement", "relevance", "adaptation"
        ],
        conclusion_template="Conduct regular goal reviews and renew or retire goals based on relevance and performance.",
        reasoning_framework="""
1. Schedule periodic reviews for all active goals.
2. Assess relevance, progress, and alignment with strategy.
3. Renew, revise, or retire goals based on findings.
4. Document review outcomes and rationale.
5. Communicate changes to all stakeholders.
6. Integrate review protocols into AGI03 goal management.
7. Archive review records for audits and learning.
8. Use review data to inform future goal setting.
9. Foster a culture of continuous improvement.
10. Refine review protocols based on feedback.
        """,
        key_factors=[
            "Review cadence",
            "Relevance assessment",
            "Documentation",
            "Stakeholder communication",
            "Continuous improvement"
        ],
        primary_authority=[
            "Kaplan, R. S., & Norton, D. P. (1996). The Balanced Scorecard.",
            "PMI (2017). A Guide to the Project Management Body of Knowledge (PMBOK Guide)."
        ],
        burden_holder="Goal owner",
        adversary_position="Frequent reviews create churn and reduce focus.",
        counter_arguments=[
            "Reviews ensure goals remain relevant and high-impact.",
            "Protocols minimize unnecessary churn.",
            "Continuous improvement increases success rates."
        ],
        resolution_strategy="Track goal relevance and achievement rates.",
        entity_scope="AGI03 goal management, all teams",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="AGI01:GoalReviewDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Impact Forecasting",
        keywords=[
            "impact forecasting", "goal outcomes", "prediction", "scenario analysis", "planning"
        ],
        conclusion_template="Forecast the impact of goals using scenario analysis to inform prioritization.",
        reasoning_framework="""
1. Define intended outcomes and impact metrics for each goal.
2. Use historical data and models to forecast likely impacts.
3. Develop scenarios for best, worst, and expected cases.
4. Quantify impact for each scenario.
5. Integrate forecasts into prioritization frameworks (e.g., RICE, OKR).
6. Review and update forecasts as new data emerges.
7. Communicate forecasts and assumptions to stakeholders.
8. Document forecasting methods for transparency.
9. Use forecasts to inform resource allocation.
10. Archive forecasts for post-implementation review.
        """,
        key_factors=[
            "Metric definition",
            "Model accuracy",
            "Scenario diversity",
            "Stakeholder communication",
            "Continuous update"
        ],
        primary_authority=[
            "Makridakis, S., Wheelwright, S. C., & Hyndman, R. J. (1998). Forecasting: Methods and Applications.",
            "Schoemaker, P. J. H. (1995). Scenario Planning: A Tool for Strategic Thinking."
        ],
        burden_holder="Goal owner",
        adversary_position="Forecasting is unreliable and distracts from execution.",
        counter_arguments=[
            "Forecasts inform better prioritization and planning.",
            "Scenario analysis accounts for uncertainty.",
            "Continuous updates improve accuracy."
        ],
        resolution_strategy="Compare forecasted versus actual impacts.",
        entity_scope="AGI03 planning modules, all teams",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="AGI02:ImpactForecastingDoctrine"
    ),
    DoctrineBlock(
        topic="Goal Success Criteria Definition",
        keywords=[
            "success criteria", "goal definition", "measurement", "outcomes", "evaluation"
        ],
        conclusion_template="Define clear, measurable success criteria for all goals to enable objective evaluation.",
        reasoning_framework="""
1. Specify what constitutes success for each goal.
2. Use quantitative and qualitative metrics as appropriate.
3. Document criteria and communicate to all stakeholders.
4. Review criteria for clarity and measurability.
5. Integrate criteria into AGI03 tracking modules.
6. Use criteria to evaluate progress and completion.
7. Update criteria as goals evolve.
8. Archive criteria for audits and learning.
9. Use success data to inform future goal setting.
10. Foster a culture of objective evaluation.
        """,
        key_factors=[
            "Clarity",
            "Measurability",
            "Stakeholder communication",
            "Continuous update",
            "Objective evaluation"
        ],
        primary_authority=[
            "Doran, G. T. (1981). There's a S.M.A.R.T. way to write management's goals and objectives.",
            "Kaplan, R. S., & Norton, D. P. (1996). The Balanced Scorecard."
        ],
        burden_holder="Goal owner",
        adversary_position="Strict criteria limit flexibility and innovation.",
        counter_arguments=[
            "Criteria can be updated as needed.",
            "Objectivity improves evaluation and learning.",
            "Flexibility is preserved through regular review."
        ],
        resolution_strategy="Track goal achievement and stakeholder satisfaction.",
        entity_scope="AGI03 goal management, all teams",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="AGI01:SuccessCriteriaDoctrine"
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
        if (
            keyword_lower in doctrine.topic.lower()
            or any(keyword_lower in kw.lower() for kw in doctrine.keywords)
            or keyword_lower in doctrine.reasoning_framework.lower()