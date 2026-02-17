from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNCERTAIN = "Uncertain"

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
        topic="Convex Optimization",
        keywords=["convexity", "optimization", "global minimum", "feasibility", "objective function"],
        conclusion_template="If the objective function and constraints are convex, the global minimum is guaranteed.",
        reasoning_framework="""Convex optimization problems are characterized by convex objective functions and convex constraint sets. The fundamental property is that any local minimum is also a global minimum. The analysis begins by verifying the convexity of the objective function, typically through second-order conditions or by examining the Hessian matrix. Constraints are checked for convexity using set theory and function properties. Feasibility is determined by the intersection of convex sets. The solution method often involves gradient descent, interior-point methods, or duality theory. Duality provides bounds and sometimes exact solutions through the Lagrangian. The KKT conditions are necessary and sufficient for optimality in convex problems. The burden of proof lies in demonstrating convexity and feasibility. Counter-arguments may arise if the function is only pseudo-convex or if constraints are not strictly convex. The resolution strategy is to rigorously verify convexity and apply convex optimization algorithms. Precedents include the fundamental theorem of convex optimization and applications in signal processing, machine learning, and economics.""",
        key_factors=["Convexity of objective", "Convexity of constraints", "Feasibility", "Global optimality"],
        primary_authority=["Boyd & Vandenberghe, Convex Optimization", "Rockafellar, Convex Analysis"],
        burden_holder="Proponent of convexity",
        adversary_position="The problem is not convex; local minima may not be global.",
        counter_arguments=[
            "Objective function is not strictly convex.",
            "Constraints are non-convex.",
            "Feasibility is not guaranteed."
        ],
        resolution_strategy="Verify convexity analytically or numerically; apply convex optimization algorithms.",
        entity_scope="Mathematical optimization problems",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Boyd & Vandenberghe, Convex Optimization"
    ),
    DoctrineBlock(
        topic="Nonlinear Programming",
        keywords=["nonlinear", "optimization", "local minimum", "global minimum", "KKT conditions"],
        conclusion_template="Nonlinear programming problems may have multiple local minima; global optimality is not guaranteed without convexity.",
        reasoning_framework="""Nonlinear programming encompasses optimization problems where the objective or constraints are nonlinear. The analysis begins with problem formulation and identification of nonlinearity. Solution methods include gradient-based algorithms, Newton's method, and heuristic approaches. The Karush-Kuhn-Tucker (KKT) conditions provide necessary conditions for optimality, but not sufficiency unless convexity is present. The burden is on the analyst to demonstrate global optimality, often through global search or branch-and-bound methods. Adversaries may argue that solutions are only locally optimal. Counter-arguments focus on the non-convexity and possible existence of saddle points or multiple minima. Resolution involves global optimization techniques or proving convexity. Precedents include applications in engineering design, economics, and machine learning.""",
        key_factors=["Nonlinearity", "Local vs global optimality", "KKT conditions", "Feasibility"],
        primary_authority=["Bazaraa, Sherali & Shetty, Nonlinear Programming", "Nocedal & Wright, Numerical Optimization"],
        burden_holder="Proponent of global optimality",
        adversary_position="Only local optimality is achieved; global minimum is not guaranteed.",
        counter_arguments=[
            "Multiple local minima exist.",
            "Non-convex constraints.",
            "KKT conditions are not sufficient."
        ],
        resolution_strategy="Apply global optimization or verify convexity; use KKT conditions for necessary optimality.",
        entity_scope="Nonlinear optimization problems",
        confidence=0.85,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Bazaraa, Sherali & Shetty, Nonlinear Programming"
    ),
    DoctrineBlock(
        topic="Linear Programming Duality",
        keywords=["duality", "linear programming", "primal", "dual", "strong duality"],
        conclusion_template="Strong duality holds for linear programming; the optimal values of primal and dual problems are equal under feasibility.",
        reasoning_framework="""Linear programming duality is a foundational concept where every linear program (primal) has an associated dual program. The strong duality theorem states that if both primal and dual are feasible, their optimal values coincide. The analysis begins by formulating the dual problem from the primal. Feasibility is checked for both problems. The burden is on the proponent to demonstrate feasibility and optimality. Adversaries may argue infeasibility or unboundedness. Counter-arguments focus on degeneracy or lack of feasible solutions. The resolution strategy is to use simplex or interior-point methods to solve both problems and verify optimality. Precedents include the simplex method, dual simplex, and applications in resource allocation and logistics.""",
        key_factors=["Primal feasibility", "Dual feasibility", "Optimality", "Strong duality"],
        primary_authority=["Dantzig, Linear Programming", "Chvatal, Linear Programming"],
        burden_holder="Proponent of duality",
        adversary_position="Duality does not hold due to infeasibility or unboundedness.",
        counter_arguments=[
            "Primal or dual is infeasible.",
            "Unbounded solution in primal or dual.",
            "Degeneracy affects optimality."
        ],
        resolution_strategy="Check feasibility; solve both primal and dual; verify strong duality.",
        entity_scope="Linear optimization problems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Dantzig, Linear Programming"
    ),
    DoctrineBlock(
        topic="Integer Programming Complexity",
        keywords=["integer programming", "NP-hard", "complexity", "combinatorial optimization", "branch-and-bound"],
        conclusion_template="Integer programming is NP-hard; exact solutions require exponential time in the worst case.",
        reasoning_framework="""Integer programming involves optimization where some or all variables are constrained to take integer values. The complexity arises due to the combinatorial nature of the feasible region. The analysis starts by formulating the integer program and identifying the variables' integrality constraints. Solution methods include branch-and-bound, cutting planes, and heuristic algorithms. The burden is on the analyst to demonstrate computational feasibility. Adversaries argue that large-scale integer programs are intractable. Counter-arguments focus on the use of approximation algorithms or special structure (e.g., totally unimodular matrices). Resolution strategy involves using efficient solvers, exploiting problem structure, or relaxing integrality constraints. Precedents include applications in scheduling, logistics, and network design.""",
        key_factors=["Integrality constraints", "Combinatorial complexity", "Solution methods", "Approximation"],
        primary_authority=["Schrijver, Theory of Linear and Integer Programming", "Nemhauser & Wolsey, Integer and Combinatorial Optimization"],
        burden_holder="Proponent of tractability",
        adversary_position="Problem is computationally intractable for large instances.",
        counter_arguments=[
            "Exponential time complexity.",
            "No polynomial-time algorithms for general case.",
            "Approximate solutions may not be acceptable."
        ],
        resolution_strategy="Use branch-and-bound, cutting planes, or relax constraints; exploit problem structure.",
        entity_scope="Integer optimization problems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Schrijver, Theory of Linear and Integer Programming"
    ),
    DoctrineBlock(
        topic="Lagrangian Duality in Optimization",
        keywords=["lagrangian", "duality", "optimization", "constraints", "lagrange multipliers"],
        conclusion_template="Lagrangian duality provides bounds and sometimes exact solutions for constrained optimization problems.",
        reasoning_framework="""Lagrangian duality is a technique for analyzing constrained optimization problems by introducing Lagrange multipliers. The Lagrangian function combines the objective and constraints. The dual problem is formed by maximizing the Lagrangian over the multipliers. Weak duality always holds, providing lower bounds for minimization problems. Strong duality may hold under convexity and regularity conditions (e.g., Slater's condition). The burden is on the analyst to verify these conditions. Adversaries may argue lack of strong duality or duality gap. Counter-arguments focus on non-convexity or irregular constraints. Resolution strategy involves verifying convexity, applying KKT conditions, and using dual algorithms. Precedents include applications in economics, engineering, and machine learning.""",
        key_factors=["Lagrange multipliers", "Convexity", "Duality gap", "Regularity conditions"],
        primary_authority=["Rockafellar, Convex Analysis", "Boyd & Vandenberghe, Convex Optimization"],
        burden_holder="Proponent of duality",
        adversary_position="Duality gap exists; strong duality does not hold.",
        counter_arguments=[
            "Non-convexity of constraints.",
            "Irregularity (e.g., Slater's condition fails).",
            "Duality gap persists."
        ],
        resolution_strategy="Verify convexity and regularity; apply dual algorithms; check KKT conditions.",
        entity_scope="Constrained optimization problems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Rockafellar, Convex Analysis"
    ),
    DoctrineBlock(
        topic="Simplex Method Efficiency",
        keywords=["simplex method", "linear programming", "pivot", "efficiency", "degeneracy"],
        conclusion_template="The simplex method is efficient in practice but has exponential worst-case complexity.",
        reasoning_framework="""The simplex method is a widely used algorithm for solving linear programming problems. It operates by moving along the edges of the feasible region to find the optimal vertex. Although the worst-case complexity is exponential, practical performance is often polynomial due to problem structure and pivot rules. The burden is on the analyst to justify efficiency for specific instances. Adversaries may cite pathological cases (e.g., Klee-Minty cube) where the method performs poorly. Counter-arguments focus on average-case performance and improvements through pivot rules. Resolution strategy involves using alternative algorithms (e.g., interior-point methods) or preprocessing. Precedents include applications in economics, logistics, and operations research.""",
        key_factors=["Pivot rules", "Degeneracy", "Problem structure", "Worst-case complexity"],
        primary_authority=["Dantzig, Linear Programming", "Klee & Minty, Exponential Example"],
        burden_holder="Proponent of efficiency",
        adversary_position="Simplex method is inefficient for certain instances.",
        counter_arguments=[
            "Exponential complexity in worst case.",
            "Degeneracy slows convergence.",
            "Pathological examples exist."
        ],
        resolution_strategy="Use alternative algorithms or improved pivot rules; analyze problem structure.",
        entity_scope="Linear programming algorithms",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Dantzig, Linear Programming"
    ),
    DoctrineBlock(
        topic="Interior-Point Methods",
        keywords=["interior-point", "linear programming", "polynomial time", "barrier function", "optimization"],
        conclusion_template="Interior-point methods solve linear and convex optimization problems in polynomial time.",
        reasoning_framework="""Interior-point methods are algorithms for solving linear and convex optimization problems. They operate by traversing the interior of the feasible region using barrier functions. The theoretical complexity is polynomial, making them attractive for large-scale problems. The burden is on the analyst to demonstrate applicability and efficiency. Adversaries may argue numerical instability or difficulty in parameter tuning. Counter-arguments focus on robustness and scalability. Resolution strategy involves careful implementation, parameter selection, and hybrid approaches. Precedents include applications in finance, engineering, and machine learning.""",
        key_factors=["Barrier functions", "Polynomial complexity", "Numerical stability", "Scalability"],
        primary_authority=["Karmarkar, A New Polynomial-Time Algorithm", "Boyd & Vandenberghe, Convex Optimization"],
        burden_holder="Proponent of efficiency",
        adversary_position="Interior-point methods are numerically unstable or difficult to tune.",
        counter_arguments=[
            "Numerical instability.",
            "Parameter sensitivity.",
            "Difficulty in implementation."
        ],
        resolution_strategy="Careful implementation; hybrid algorithms; parameter tuning.",
        entity_scope="Optimization algorithms",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Karmarkar, A New Polynomial-Time Algorithm"
    ),
    DoctrineBlock(
        topic="Gradient Descent Convergence",
        keywords=["gradient descent", "convergence", "optimization", "learning rate", "convexity"],
        conclusion_template="Gradient descent converges to the global minimum for convex functions with appropriate learning rate.",
        reasoning_framework="""Gradient descent is an iterative algorithm for finding minima of differentiable functions. For convex functions, convergence to the global minimum is guaranteed with proper learning rate selection. The analysis involves checking convexity, differentiability, and step size. The burden is on the analyst to demonstrate convergence and avoid oscillations or divergence. Adversaries may argue poor convergence for non-convex functions or improper learning rate. Counter-arguments focus on adaptive learning rates and momentum. Resolution strategy involves tuning learning rate, using variants (e.g., Adam, RMSProp), and verifying convexity. Precedents include applications in machine learning, signal processing, and statistics.""",
        key_factors=["Convexity", "Learning rate", "Differentiability", "Step size"],
        primary_authority=["Boyd & Vandenberghe, Convex Optimization", "Nesterov, Introductory Lectures on Convex Optimization"],
        burden_holder="Proponent of convergence",
        adversary_position="Gradient descent fails to converge due to non-convexity or poor learning rate.",
        counter_arguments=[
            "Non-convex objective.",
            "Improper learning rate.",
            "Oscillations or divergence."
        ],
        resolution_strategy="Tune learning rate; use adaptive methods; verify convexity.",
        entity_scope="Optimization algorithms",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Boyd & Vandenberghe, Convex Optimization"
    ),
    DoctrineBlock(
        topic="Stochastic Gradient Descent",
        keywords=["stochastic gradient descent", "SGD", "optimization", "convergence", "noise"],
        conclusion_template="Stochastic gradient descent converges in expectation for convex functions but may oscillate due to noise.",
        reasoning_framework="""Stochastic gradient descent (SGD) is an optimization algorithm that uses random samples to estimate gradients. It is effective for large-scale problems and online learning. For convex functions, convergence in expectation is guaranteed, but noise can cause oscillations. The burden is on the analyst to demonstrate convergence and manage variance. Adversaries may argue instability or slow convergence. Counter-arguments focus on mini-batch methods, variance reduction, and adaptive learning rates. Resolution strategy involves using momentum, averaging, and batch normalization. Precedents include applications in deep learning, statistics, and signal processing.""",
        key_factors=["Convexity", "Noise", "Variance reduction", "Learning rate"],
        primary_authority=["Bottou, Stochastic Gradient Descent", "Robbins & Monro, Stochastic Approximation"],
        burden_holder="Proponent of convergence",
        adversary_position="SGD is unstable or converges slowly due to noise.",
        counter_arguments=[
            "High variance in gradient estimates.",
            "Slow convergence.",
            "Instability due to noise."
        ],
        resolution_strategy="Use mini-batch, momentum, and variance reduction techniques.",
        entity_scope="Optimization algorithms",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bottou, Stochastic Gradient Descent"
    ),
    DoctrineBlock(
        topic="KKT Conditions",
        keywords=["KKT conditions", "optimality", "constraints", "nonlinear programming", "necessary conditions"],
        conclusion_template="KKT conditions are necessary for optimality in constrained nonlinear programming; sufficiency requires convexity.",
        reasoning_framework="""The Karush-Kuhn-Tucker (KKT) conditions provide necessary conditions for optimality in constrained nonlinear programming. The analysis begins by formulating the problem and identifying constraints. The KKT conditions include stationarity, primal feasibility, dual feasibility, and complementary slackness. Sufficiency requires convexity of the objective and constraints. The burden is on the analyst to verify these conditions. Adversaries may argue non-convexity or violation of regularity conditions. Counter-arguments focus on constraint qualification and convexity. Resolution strategy involves verifying convexity, applying KKT conditions, and checking constraint qualifications. Precedents include applications in engineering, economics, and machine learning.""",
        key_factors=["Stationarity", "Feasibility", "Convexity", "Constraint qualification"],
        primary_authority=["Bazaraa, Sherali & Shetty, Nonlinear Programming", "Boyd & Vandenberghe, Convex Optimization"],
        burden_holder="Proponent of optimality",
        adversary_position="KKT conditions are not sufficient due to non-convexity.",
        counter_arguments=[
            "Non-convex objective or constraints.",
            "Constraint qualification fails.",
            "KKT conditions do not guarantee global optimality."
        ],
        resolution_strategy="Verify convexity and constraint qualification; apply KKT conditions.",
        entity_scope="Nonlinear optimization problems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bazaraa, Sherali & Shetty, Nonlinear Programming"
    ),
    DoctrineBlock(
        topic="Multi-objective Optimization",
        keywords=["multi-objective", "Pareto optimality", "trade-offs", "optimization", "scalarization"],
        conclusion_template="Multi-objective optimization seeks Pareto optimal solutions, balancing trade-offs between objectives.",
        reasoning_framework="""Multi-objective optimization involves optimizing multiple conflicting objectives. The analysis begins by identifying objectives and formulating the Pareto front. Scalarization techniques (e.g., weighted sum, epsilon constraint) are used to convert multi-objective problems into single-objective ones. The burden is on the analyst to justify trade-offs and select appropriate scalarization. Adversaries may argue subjective weighting or loss of diversity. Counter-arguments focus on Pareto optimality and robustness. Resolution strategy involves generating the Pareto front, using evolutionary algorithms, and stakeholder engagement. Precedents include applications in engineering design, economics, and environmental management.""",
        key_factors=["Trade-offs", "Pareto optimality", "Scalarization", "Diversity"],
        primary_authority=["Ehrgott, Multicriteria Optimization", "Deb, Multi-objective Optimization Using Evolutionary Algorithms"],
        burden_holder="Proponent of trade-off selection",
        adversary_position="Weighting is subjective; diversity is lost.",
        counter_arguments=[
            "Subjective weighting.",
            "Loss of diversity.",
            "Difficulty in stakeholder engagement."
        ],
        resolution_strategy="Generate Pareto front; use evolutionary algorithms; involve stakeholders.",
        entity_scope="Multi-objective optimization problems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Ehrgott, Multicriteria Optimization"
    ),
    DoctrineBlock(
        topic="Robust Optimization",
        keywords=["robust optimization", "uncertainty", "worst-case", "feasibility", "optimization"],
        conclusion_template="Robust optimization ensures feasibility and optimality under uncertainty by optimizing worst-case scenarios.",
        reasoning_framework="""Robust optimization addresses uncertainty in optimization problems by ensuring solutions remain feasible and near-optimal under worst-case scenarios. The analysis begins by modeling uncertainty (e.g., ellipsoidal, polyhedral sets) and reformulating the problem. The burden is on the analyst to justify the uncertainty model and solution robustness. Adversaries may argue conservatism or overestimation of uncertainty. Counter-arguments focus on practical feasibility and risk management. Resolution strategy involves sensitivity analysis, scenario generation, and robust reformulation. Precedents include applications in finance, engineering, and supply chain management.""",
        key_factors=["Uncertainty modeling", "Worst-case optimization", "Feasibility", "Risk management"],
        primary_authority=["Ben-Tal & Nemirovski, Robust Optimization", "Bertsimas & Sim, Robust Discrete Optimization"],
        burden_holder="Proponent of robustness",
        adversary_position="Robust solutions are overly conservative or impractical.",
        counter_arguments=[
            "Conservatism in solution.",
            "Overestimation of uncertainty.",
            "Reduced optimality."
        ],
        resolution_strategy="Model uncertainty accurately; use sensitivity analysis; balance robustness and optimality.",
        entity_scope="Optimization under uncertainty",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ben-Tal & Nemirovski, Robust Optimization"
    ),
    DoctrineBlock(
        topic="Dynamic Programming Principle",
        keywords=["dynamic programming", "Bellman equation", "optimality", "recursion", "state space"],
        conclusion_template="Dynamic programming solves optimization problems by recursive decomposition using the Bellman equation.",
        reasoning_framework="""Dynamic programming is a method for solving complex optimization problems by breaking them into simpler subproblems. The Bellman equation provides a recursive relationship for optimality. The analysis begins by defining the state space and formulating the recursion. The burden is on the analyst to ensure the principle of optimality holds. Adversaries may argue curse of dimensionality or infeasibility. Counter-arguments focus on problem decomposition and approximation. Resolution strategy involves using approximate dynamic programming, state aggregation, and pruning. Precedents include applications in control theory, operations research, and computer science.""",
        key_factors=["Principle of optimality", "Bellman equation", "State space", "Recursion"],
        primary_authority=["Bellman, Dynamic Programming", "Bertsekas, Dynamic Programming and Optimal Control"],
        burden_holder="Proponent of recursion",
        adversary_position="Curse of dimensionality makes dynamic programming infeasible.",
        counter_arguments=[
            "Exponential growth of state space.",
            "Infeasibility for large problems.",
            "Approximation errors."
        ],
        resolution_strategy="Use approximate dynamic programming; state aggregation; pruning.",
        entity_scope="Recursive optimization problems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Bellman, Dynamic Programming"
    ),
    DoctrineBlock(
        topic="Constraint Programming",
        keywords=["constraint programming", "feasibility", "search", "propagation", "optimization"],
        conclusion_template="Constraint programming solves optimization problems by search and propagation of constraints.",
        reasoning_framework="""Constraint programming is an approach for solving optimization problems by specifying constraints and searching for feasible solutions. The analysis begins by formulating constraints and variables. Propagation techniques reduce the search space by inferring variable domains. The burden is on the analyst to ensure completeness and efficiency. Adversaries may argue combinatorial explosion or lack of optimality. Counter-arguments focus on constraint propagation and pruning. Resolution strategy involves using efficient search algorithms, propagation, and hybrid methods. Precedents include applications in scheduling, planning, and resource allocation.""",
        key_factors=["Constraint propagation", "Search algorithms", "Feasibility", "Pruning"],
        primary_authority=["Dechter, Constraint Processing", "Rossi, van Beek & Walsh, Handbook of Constraint Programming"],
        burden_holder="Proponent of feasibility",
        adversary_position="Combinatorial explosion makes constraint programming inefficient.",
        counter_arguments=[
            "Exponential search space.",
            "Incomplete propagation.",
            "Lack of optimality."
        ],
        resolution_strategy="Use efficient search and propagation; hybrid algorithms; pruning.",
        entity_scope="Constraint-based optimization problems",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Dechter, Constraint Processing"
    ),
    DoctrineBlock(
        topic="Global Optimization",
        keywords=["global optimization", "non-convex", "multiple minima", "branch-and-bound", "heuristics"],
        conclusion_template="Global optimization seeks the global minimum in non-convex problems using exhaustive or heuristic methods.",
        reasoning_framework="""Global optimization addresses finding the global minimum in non-convex problems. The analysis begins by identifying non-convexity and multiple minima. Solution methods include branch-and-bound, simulated annealing, and genetic algorithms. The burden is on the analyst to justify global search and manage computational complexity. Adversaries may argue inefficiency or lack of guarantees. Counter-arguments focus on approximation and problem structure. Resolution strategy involves using hybrid methods, exploiting structure, and parallel computation. Precedents include applications in engineering, finance, and machine learning.""",
        key_factors=["Non-convexity", "Global search", "Heuristics", "Computational complexity"],
        primary_authority=["Horst & Pardalos, Handbook of Global Optimization", "Floudas, Nonlinear and Global Optimization"],
        burden_holder="Proponent of global optimality",
        adversary_position="Global optimization is computationally infeasible.",
        counter_arguments=[
            "Exponential complexity.",
            "No guarantees of global minimum.",
            "Heuristic methods may fail."
        ],
        resolution_strategy="Use hybrid and parallel methods; exploit problem structure.",
        entity_scope="Non-convex optimization problems",
        confidence=0.87,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Horst & Pardalos, Handbook of Global Optimization"
    ),
    DoctrineBlock(
        topic="Penalty Methods",
        keywords=["penalty methods", "constraints", "optimization", "feasibility", "objective function"],
        conclusion_template="Penalty methods enforce constraints by adding penalty terms to the objective function.",
        reasoning_framework="""Penalty methods are used in optimization to enforce constraints by augmenting the objective function with penalty terms. The analysis begins by formulating the penalty function and identifying constraints. The burden is on the analyst to select appropriate penalty parameters. Adversaries may argue ill-conditioning or slow convergence. Counter-arguments focus on parameter tuning and augmented Lagrangian methods. Resolution strategy involves using adaptive penalties, hybrid methods, and regularization. Precedents include applications in engineering, economics, and machine learning.""",
        key_factors=["Penalty parameters", "Constraint enforcement", "Convergence", "Ill-conditioning"],
        primary_authority=["Nocedal & Wright, Numerical Optimization", "Bertsekas, Constrained Optimization"],
        burden_holder="Proponent of feasibility",
        adversary_position="Penalty methods cause ill-conditioning or slow convergence.",
        counter_arguments=[
            "Ill-conditioning due to large penalties.",
            "Slow convergence.",
            "Difficulty in parameter selection."
        ],
        resolution_strategy="Use adaptive penalties; augmented Lagrangian methods; regularization.",
        entity_scope="Constrained optimization problems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Nocedal & Wright, Numerical Optimization"
    ),
    DoctrineBlock(
        topic="Augmented Lagrangian Methods",
        keywords=["augmented lagrangian", "constraints", "optimization", "penalty", "dual methods"],
        conclusion_template="Augmented Lagrangian methods combine penalty and dual approaches for efficient constraint enforcement.",
        reasoning_framework="""Augmented Lagrangian methods enhance penalty methods by incorporating dual variables, improving convergence and constraint enforcement. The analysis begins by formulating the augmented Lagrangian and identifying constraints. The burden is on the analyst to tune parameters and manage dual updates. Adversaries may argue complexity or instability. Counter-arguments focus on improved convergence and robustness. Resolution strategy involves adaptive parameter tuning, dual updates, and hybrid algorithms. Precedents include applications in engineering, economics, and machine learning.""",
        key_factors=["Penalty parameters", "Dual variables", "Convergence", "Constraint enforcement"],
        primary_authority=["Bertsekas, Constrained Optimization", "Nocedal & Wright, Numerical Optimization"],
        burden_holder="Proponent of efficiency",
        adversary_position="Augmented Lagrangian methods are complex or unstable.",
        counter_arguments=[
            "Complexity in implementation.",
            "Instability in dual updates.",
            "Parameter sensitivity."
        ],
        resolution_strategy="Adaptive parameter tuning; robust dual updates; hybrid algorithms.",
        entity_scope="Constrained optimization problems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Bertsekas, Constrained Optimization"
    ),
    DoctrineBlock(
        topic="Network Flow Optimization",
        keywords=["network flow", "optimization", "max-flow", "min-cut", "graph theory"],
        conclusion_template="Network flow optimization solves max-flow and min-cut problems efficiently using graph algorithms.",
        reasoning_framework="""Network flow optimization addresses problems involving flow through networks. The analysis begins by formulating the network, capacities, and flow conservation. Algorithms such as Ford-Fulkerson and Edmonds-Karp efficiently solve max-flow and min-cut problems. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue complexity in large networks or dynamic changes. Counter-arguments focus on algorithmic efficiency and scalability. Resolution strategy involves using efficient algorithms, decomposition, and parallel computation. Precedents include applications in transportation, telecommunications, and logistics.""",
        key_factors=["Flow conservation", "Capacity constraints", "Algorithmic efficiency", "Scalability"],
        primary_authority=["Ahuja, Magnanti & Orlin, Network Flows", "Ford & Fulkerson, Max-Flow Algorithm"],
        burden_holder="Proponent of efficiency",
        adversary_position="Network flow algorithms are inefficient for large or dynamic networks.",
        counter_arguments=[
            "Complexity in large networks.",
            "Dynamic changes affect feasibility.",
            "Scalability issues."
        ],
        resolution_strategy="Use efficient algorithms; decomposition; parallel computation.",
        entity_scope="Network optimization problems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ahuja, Magnanti & Orlin, Network Flows"
    ),
    DoctrineBlock(
        topic="Sensitivity Analysis in Optimization",
        keywords=["sensitivity analysis", "optimization", "parameter changes", "robustness", "stability"],
        conclusion_template="Sensitivity analysis evaluates the impact of parameter changes on optimal solutions.",
        reasoning_framework="""Sensitivity analysis in optimization assesses how changes in parameters affect the optimal solution. The analysis begins by identifying key parameters and their ranges. Methods include derivative analysis, scenario generation, and robustness checks. The burden is on the analyst to ensure solution stability and robustness. Adversaries may argue instability or lack of robustness. Counter-arguments focus on scenario analysis and robust optimization. Resolution strategy involves using sensitivity analysis tools, robust reformulation, and stakeholder engagement. Precedents include applications in finance, engineering, and supply chain management.""",
        key_factors=["Parameter changes", "Robustness", "Stability", "Scenario analysis"],
        primary_authority=["Winston, Operations Research", "Ben-Tal & Nemirovski, Robust Optimization"],
        burden_holder="Proponent of robustness",
        adversary_position="Optimal solutions are sensitive to parameter changes.",
        counter_arguments=[
            "Instability in solution.",
            "Lack of robustness.",
            "Difficulty in scenario generation."
        ],
        resolution_strategy="Use sensitivity analysis tools; robust reformulation; scenario analysis.",
        entity_scope="Optimization problems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Winston, Operations Research"
    ),
    DoctrineBlock(
        topic="Duality Gap",
        keywords=["duality gap", "optimization", "lagrangian", "convexity", "optimality"],
        conclusion_template="The duality gap measures the difference between primal and dual optimal values; it vanishes under strong duality.",
        reasoning_framework="""The duality gap is the difference between the optimal values of the primal and dual problems. In convex optimization, strong duality ensures the gap vanishes. The analysis begins by formulating primal and dual problems and checking regularity conditions. The burden is on the analyst to verify strong duality. Adversaries may argue non-convexity or irregular constraints. Counter-arguments focus on regularity and convexity. Resolution strategy involves verifying conditions, reformulating the problem, and using dual algorithms. Precedents include applications in economics, engineering, and machine learning.""",
        key_factors=["Primal and dual formulation", "Convexity", "Regularity conditions", "Optimality"],
        primary_authority=["Rockafellar, Convex Analysis", "Boyd & Vandenberghe, Convex Optimization"],
        burden_holder="Proponent of strong duality",
        adversary_position="Duality gap persists due to non-convexity or irregularity.",
        counter_arguments=[
            "Non-convex objective or constraints.",
            "Irregularity in constraints.",
            "Duality gap persists."
        ],
        resolution_strategy="Verify convexity and regularity; reformulate problem; use dual algorithms.",
        entity_scope="Optimization problems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Rockafellar, Convex Analysis"
    ),
    DoctrineBlock(
        topic="Optimality Conditions in Unconstrained Optimization",
        keywords=["optimality", "unconstrained", "gradient", "hessian", "second-order conditions"],
        conclusion_template="First-order and second-order conditions determine optimality in unconstrained optimization.",
        reasoning_framework="""Optimality in unconstrained optimization is determined by first-order (gradient) and second-order (Hessian) conditions. The analysis begins by computing the gradient and checking for stationary points. Second-order conditions involve the Hessian matrix; positive definiteness indicates a minimum. The burden is on the analyst to verify conditions and distinguish minima from saddle points. Adversaries may argue non-differentiability or multiple stationary points. Counter-arguments focus on numerical methods and regularization. Resolution strategy involves using gradient and Hessian analysis, regularization, and numerical optimization. Precedents include applications in engineering, economics, and statistics.""",
        key_factors=["Gradient", "Hessian", "Stationary points", "Second-order conditions"],
        primary_authority=["Nocedal & Wright, Numerical Optimization", "Boyd & Vandenberghe, Convex Optimization"],
        burden_holder="Proponent of optimality",
        adversary_position="Stationary points may be saddle points or maxima.",
        counter_arguments=[
            "Non-differentiability.",
            "Multiple stationary points.",
            "Hessian is not positive definite."
        ],
        resolution_strategy="Use gradient and Hessian analysis; regularization; numerical optimization.",
        entity_scope="Unconstrained optimization problems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Nocedal & Wright, Numerical Optimization"
    ),
    DoctrineBlock(
        topic="Feasibility in Optimization",
        keywords=["feasibility", "constraints", "optimization", "solution space", "infeasibility"],
        conclusion_template="Feasibility requires all constraints to be satisfied; infeasibility precludes optimality.",
        reasoning_framework="""Feasibility in optimization refers to the existence of solutions that satisfy all constraints. The analysis begins by formulating constraints and checking for intersection of feasible sets. The burden is on the analyst to demonstrate feasibility or identify infeasibility. Adversaries may argue conflicting constraints or empty feasible region. Counter-arguments focus on relaxation or reformulation. Resolution strategy involves constraint relaxation, reformulation, and feasibility analysis tools. Precedents include applications in engineering, economics, and logistics.""",
        key_factors=["Constraint satisfaction", "Feasible region", "Relaxation", "Reformulation"],
        primary_authority=["Winston, Operations Research", "Bazaraa, Sherali & Shetty, Nonlinear Programming"],
        burden_holder="Proponent of feasibility",
        adversary_position="Constraints are conflicting; no feasible solution exists.",
        counter_arguments=[
            "Conflicting constraints.",
            "Empty feasible region.",
            "Infeasibility due to parameter values."
        ],
        resolution_strategy="Constraint relaxation; reformulation; feasibility analysis tools.",
        entity_scope="Optimization problems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Winston, Operations Research"
    ),
    DoctrineBlock(
        topic="Heuristic Optimization",
        keywords=["heuristics", "optimization", "approximation", "metaheuristics", "global search"],
        conclusion_template="Heuristic optimization uses approximate methods to find near-optimal solutions in complex problems.",
        reasoning_framework="""Heuristic optimization employs approximate algorithms such as genetic algorithms, simulated annealing, and tabu search to solve complex optimization problems. The analysis begins by selecting appropriate heuristics based on problem structure. The burden is on the analyst to justify approximation and manage trade-offs. Adversaries may argue lack of guarantees or reproducibility. Counter-arguments focus on scalability and practical feasibility. Resolution strategy involves hybrid methods, parameter tuning, and benchmarking. Precedents include applications in engineering, logistics, and machine learning.""",
        key_factors=["Approximation", "Scalability", "Parameter tuning", "Benchmarking"],
        primary_authority=["Glover & Kochenberger, Handbook of Metaheuristics", "Goldberg, Genetic Algorithms"],
        burden_holder="Proponent of approximation",
        adversary_position="Heuristic methods lack guarantees and reproducibility.",
        counter_arguments=[
            "No guarantee of optimality.",
            "Results may vary between runs.",
            "Parameter sensitivity."
        ],
        resolution_strategy="Hybrid methods; parameter tuning; benchmarking.",
        entity_scope="Complex optimization problems",
        confidence=0.88,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Glover & Kochenberger, Handbook of Metaheuristics"
    ),
    DoctrineBlock(
        topic="Convex Hull Algorithms",
        keywords=["convex hull", "geometry", "optimization", "computational geometry", "algorithms"],
        conclusion_template="Convex hull algorithms efficiently compute the smallest convex set containing all points.",
        reasoning_framework="""Convex hull algorithms are used in computational geometry to find the smallest convex set containing a given set of points. The analysis begins by selecting appropriate algorithms (e.g., Graham scan, Quickhull). The burden is on the analyst to ensure efficiency and correctness. Adversaries may argue scalability or numerical instability. Counter-arguments focus on algorithmic improvements and preprocessing. Resolution strategy involves using efficient algorithms, preprocessing, and parallel computation. Precedents include applications in computer graphics, robotics, and optimization.""",
        key_factors=["Algorithmic efficiency", "Correctness", "Scalability", "Numerical stability"],
        primary_authority=["Preparata & Shamos, Computational Geometry", "Barber, Dobkin & Huhdanpaa, Quickhull Algorithm"],
        burden_holder="Proponent of efficiency",
        adversary_position="Convex hull algorithms are inefficient for large datasets.",
        counter_arguments=[
            "Scalability issues.",
            "Numerical instability.",
            "Complexity in high dimensions."
        ],
        resolution_strategy="Use efficient algorithms; preprocessing; parallel computation.",
        entity_scope="Computational geometry problems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Preparata & Shamos, Computational Geometry"
    ),
    DoctrineBlock(
        topic="Machine Learning Model Optimization",
        keywords=["machine learning", "model optimization", "hyperparameters", "gradient descent", "loss function"],
        conclusion_template="Model optimization in machine learning involves minimizing loss functions using gradient-based methods.",
        reasoning_framework="""Machine learning model optimization focuses on minimizing loss functions through gradient-based algorithms. The analysis begins by selecting appropriate loss functions and optimization algorithms. Hyperparameter tuning is critical for convergence and generalization. The burden is on the analyst to ensure convergence and avoid overfitting. Adversaries may argue poor generalization or instability. Counter-arguments focus on regularization, cross-validation, and adaptive algorithms. Resolution strategy involves hyperparameter tuning, regularization, and validation. Precedents include applications in deep learning, statistics, and computer vision.""",
        key_factors=["Loss function", "Gradient-based optimization", "Hyperparameter tuning", "Generalization"],
        primary_authority=["Goodfellow, Bengio & Courville, Deep Learning", "Bottou, Stochastic Gradient Descent"],
        burden_holder="Proponent of convergence",
        adversary_position="Model optimization leads to overfitting or instability.",
        counter_arguments=[
            "Overfitting due to improper tuning.",
            "Instability in optimization.",
            "Poor generalization."
        ],
        resolution_strategy="Hyperparameter tuning; regularization; cross-validation.",
        entity_scope="Machine learning optimization problems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Goodfellow, Bengio & Courville, Deep Learning"
    ),
    DoctrineBlock(
        topic="Resource Allocation Optimization",
        keywords=["resource allocation", "optimization", "constraints", "efficiency", "linear programming"],
        conclusion_template="Resource allocation optimization maximizes efficiency under constraints using linear programming.",
        reasoning_framework="""Resource allocation optimization involves distributing resources to maximize efficiency or minimize cost under constraints. The analysis begins by formulating the objective and constraints. Linear programming is commonly used for tractable problems. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue infeasibility or suboptimal allocation. Counter-arguments focus on constraint relaxation and reformulation. Resolution strategy involves using linear programming, constraint relaxation, and sensitivity analysis. Precedents include applications in logistics, economics, and engineering.""",
        key_factors=["Constraints", "Efficiency", "Feasibility", "Optimality"],
        primary_authority=["Dantzig, Linear Programming", "Winston, Operations Research"],
        burden_holder="Proponent of efficiency",
        adversary_position="Resource allocation is infeasible or suboptimal.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Suboptimal allocation.",
            "Difficulty in constraint formulation."
        ],
        resolution_strategy="Linear programming; constraint relaxation; sensitivity analysis.",
        entity_scope="Resource allocation problems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Dantzig, Linear Programming"
    ),
    DoctrineBlock(
        topic="Portfolio Optimization",
        keywords=["portfolio optimization", "finance", "risk", "return", "quadratic programming"],
        conclusion_template="Portfolio optimization balances risk and return using quadratic programming and risk constraints.",
        reasoning_framework="""Portfolio optimization in finance involves maximizing return while minimizing risk, subject to constraints. The analysis begins by formulating the objective (e.g., mean-variance) and constraints (e.g., budget, risk limits). Quadratic programming is used for tractable problems. The burden is on the analyst to justify risk modeling and constraint selection. Adversaries may argue unrealistic assumptions or instability. Counter-arguments focus on robust optimization and scenario analysis. Resolution strategy involves quadratic programming, robust reformulation, and scenario analysis. Precedents include applications in asset management, banking, and insurance.""",
        key_factors=["Risk modeling", "Return maximization", "Constraints", "Quadratic programming"],
        primary_authority=["Markowitz, Portfolio Selection", "Ben-Tal & Nemirovski, Robust Optimization"],
        burden_holder="Proponent of risk modeling",
        adversary_position="Portfolio optimization relies on unrealistic assumptions.",
        counter_arguments=[
            "Unrealistic risk assumptions.",
            "Instability in optimization.",
            "Difficulty in constraint selection."
        ],
        resolution_strategy="Quadratic programming; robust reformulation; scenario analysis.",
        entity_scope="Financial optimization problems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Markowitz, Portfolio Selection"
    ),
    DoctrineBlock(
        topic="Supply Chain Optimization",
        keywords=["supply chain", "optimization", "logistics", "constraints", "network flow"],
        conclusion_template="Supply chain optimization improves logistics and efficiency using network flow and linear programming.",
        reasoning_framework="""Supply chain optimization involves improving logistics, efficiency, and cost-effectiveness by modeling flows and constraints. The analysis begins by formulating the supply chain network and constraints. Network flow and linear programming are used for tractable problems. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue infeasibility or complexity. Counter-arguments focus on decomposition and scenario analysis. Resolution strategy involves network flow algorithms, decomposition, and scenario analysis. Precedents include applications in manufacturing, transportation, and retail.""",
        key_factors=["Network flow", "Constraints", "Efficiency", "Decomposition"],
        primary_authority=["Ahuja, Magnanti & Orlin, Network Flows", "Winston, Operations Research"],
        burden_holder="Proponent of efficiency",
        adversary_position="Supply chain optimization is infeasible or overly complex.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Complexity in large networks.",
            "Difficulty in decomposition."
        ],
        resolution_strategy="Network flow algorithms; decomposition; scenario analysis.",
        entity_scope="Supply chain optimization problems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ahuja, Magnanti & Orlin, Network Flows"
    ),
    DoctrineBlock(
        topic="Scheduling Optimization",
        keywords=["scheduling", "optimization", "constraints", "integer programming", "resource allocation"],
        conclusion_template="Scheduling optimization solves resource allocation problems using integer programming and constraint satisfaction.",
        reasoning_framework="""Scheduling optimization involves allocating resources over time to maximize efficiency or minimize cost. The analysis begins by formulating the scheduling problem and constraints. Integer programming and constraint satisfaction are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue infeasibility or computational complexity. Counter-arguments focus on decomposition and heuristic methods. Resolution strategy involves integer programming, decomposition, and heuristics. Precedents include applications in manufacturing, transportation, and project management.""",
        key_factors=["Constraints", "Integer programming", "Feasibility", "Decomposition"],
        primary_authority=["Nemhauser & Wolsey, Integer and Combinatorial Optimization", "Dechter, Constraint Processing"],
        burden_holder="Proponent of feasibility",
        adversary_position="Scheduling optimization is infeasible or computationally complex.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Computational complexity.",
            "Difficulty in decomposition."
        ],
        resolution_strategy="Integer programming; decomposition; heuristic methods.",
        entity_scope="Scheduling optimization problems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Nemhauser & Wolsey, Integer and Combinatorial Optimization"
    ),
    DoctrineBlock(
        topic="Optimal Transport Theory",
        keywords=["optimal transport", "optimization", "cost minimization", "measure theory", "linear programming"],
        conclusion_template="Optimal transport theory minimizes cost of moving distributions using measure theory and linear programming.",
        reasoning_framework="""Optimal transport theory addresses minimizing the cost of moving distributions from one location to another. The analysis begins by formulating the transport problem and cost function. Measure theory and linear programming are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue complexity or instability. Counter-arguments focus on algorithmic improvements and regularization. Resolution strategy involves linear programming, regularization, and efficient algorithms. Precedents include applications in economics, logistics, and machine learning.""",
        key_factors=["Cost minimization", "Measure theory", "Linear programming", "Feasibility"],
        primary_authority=["Villani, Optimal Transport", "Peyré & Cuturi, Computational Optimal Transport"],
        burden_holder="Proponent of feasibility",
        adversary_position="Optimal transport is computationally complex or unstable.",
        counter_arguments=[
            "Computational complexity.",
            "Instability in optimization.",
            "Difficulty in measure formulation."
        ],
        resolution_strategy="Linear programming; regularization; efficient algorithms.",
        entity_scope="Optimal transport problems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Villani, Optimal Transport"
    ),
    DoctrineBlock(
        topic="Game Theory Optimization",
        keywords=["game theory", "optimization", "Nash equilibrium", "strategy", "constraints"],
        conclusion_template="Game theory optimization finds equilibrium strategies using optimization and constraint satisfaction.",
        reasoning_framework="""Game theory optimization involves finding equilibrium strategies in multi-agent settings. The analysis begins by formulating the game, strategies, and constraints. Optimization and constraint satisfaction are used to find Nash equilibria. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue instability or lack of equilibrium. Counter-arguments focus on algorithmic improvements and regularization. Resolution strategy involves optimization algorithms, constraint satisfaction, and regularization. Precedents include applications in economics, politics, and computer science.""",
        key_factors=["Nash equilibrium", "Strategy formulation", "Constraints", "Feasibility"],
        primary_authority=["Osborne & Rubinstein, A Course in Game Theory", "Fudenberg & Tirole, Game Theory"],
        burden_holder="Proponent of equilibrium",
        adversary_position="Game theory optimization lacks equilibrium or is unstable.",
        counter_arguments=[
            "Instability in equilibrium.",
            "Lack of feasible strategies.",
            "Difficulty in constraint satisfaction."
        ],
        resolution_strategy="Optimization algorithms; constraint satisfaction; regularization.",
        entity_scope="Game theory optimization problems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Osborne & Rubinstein, A Course in Game Theory"
    ),
    DoctrineBlock(
        topic="Optimal Control Theory",
        keywords=["optimal control", "optimization", "dynamic systems", "constraints", "Pontryagin's principle"],
        conclusion_template="Optimal control theory optimizes dynamic systems using Pontryagin's principle and dynamic programming.",
        reasoning_framework="""Optimal control theory addresses optimization of dynamic systems over time. The analysis begins by formulating the control problem, constraints, and objective. Pontryagin's principle and dynamic programming are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue complexity or instability. Counter-arguments focus on algorithmic improvements and regularization. Resolution strategy involves dynamic programming, Pontryagin's principle, and efficient algorithms. Precedents include applications in engineering, economics, and robotics.""",
        key_factors=["Pontryagin's principle", "Dynamic programming", "Constraints", "Feasibility"],
        primary_authority=["Pontryagin, Mathematical Theory of Optimal Processes", "Bertsekas, Dynamic Programming and Optimal Control"],
        burden_holder="Proponent of feasibility",
        adversary_position="Optimal control is computationally complex or unstable.",
        counter_arguments=[
            "Computational complexity.",
            "Instability in optimization.",
            "Difficulty in constraint formulation."
        ],
        resolution_strategy="Dynamic programming; Pontryagin's principle; efficient algorithms.",
        entity_scope="Optimal control problems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Pontryagin, Mathematical Theory of Optimal Processes"
    ),
    DoctrineBlock(
        topic="Data Envelopment Analysis",
        keywords=["data envelopment analysis", "DEA", "efficiency", "optimization", "linear programming"],
        conclusion_template="Data envelopment analysis evaluates efficiency of decision-making units using linear programming.",
        reasoning_framework="""Data envelopment analysis (DEA) is a method for assessing efficiency of decision-making units using linear programming. The analysis begins by formulating input-output relationships and constraints. Linear programming is used to compute efficiency scores. The burden is on the analyst to ensure validity and robustness. Adversaries may argue subjectivity or instability. Counter-arguments focus on robust optimization and scenario analysis. Resolution strategy involves linear programming, robust reformulation, and scenario analysis. Precedents include applications in economics, healthcare, and education.""",
        key_factors=["Efficiency", "Input-output relationships", "Linear programming", "Robustness"],
        primary_authority=["Charnes, Cooper & Rhodes, DEA", "Banker, Charnes & Cooper, DEA"],
        burden_holder="Proponent of efficiency",
        adversary_position="DEA is subjective or unstable.",
        counter_arguments=[
            "Subjectivity in input-output selection.",
            "Instability in efficiency scores.",
            "Difficulty in constraint formulation."
        ],
        resolution_strategy="Linear programming; robust reformulation; scenario analysis.",
        entity_scope="Efficiency analysis problems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Charnes, Cooper & Rhodes, DEA"
    ),
    DoctrineBlock(
        topic="Optimal Design of Experiments",
        keywords=["design of experiments", "optimization", "statistical efficiency", "constraints", "robustness"],
        conclusion_template="Optimal design of experiments maximizes statistical efficiency under constraints using optimization.",
        reasoning_framework="""Optimal design of experiments involves maximizing statistical efficiency under constraints. The analysis begins by formulating the experimental design and constraints. Optimization algorithms are used to select optimal designs. The burden is on the analyst to ensure feasibility and robustness. Adversaries may argue subjectivity or instability. Counter-arguments focus on robust optimization and scenario analysis. Resolution strategy involves optimization algorithms, robust reformulation, and scenario analysis. Precedents include applications in engineering, healthcare, and agriculture.""",
        key_factors=["Statistical efficiency", "Constraints", "Optimization algorithms", "Robustness"],
        primary_authority=["Fisher, Design of Experiments", "Atkinson & Donev, Optimum Experimental Designs"],
        burden_holder="Proponent of efficiency",
        adversary_position="Design of experiments is subjective or unstable.",
        counter_arguments=[
            "Subjectivity in design selection.",
            "Instability in efficiency.",
            "Difficulty in constraint formulation."
        ],
        resolution_strategy="Optimization algorithms; robust reformulation; scenario analysis.",
        entity_scope="Experimental design problems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Fisher, Design of Experiments"
    ),
    DoctrineBlock(
        topic="Optimal Pricing Strategies",
        keywords=["pricing", "optimization", "constraints", "economics", "revenue maximization"],
        conclusion_template="Optimal pricing strategies maximize revenue under constraints using optimization and game theory.",
        reasoning_framework="""Optimal pricing strategies involve maximizing revenue under constraints using optimization and game theory. The analysis begins by formulating the pricing problem and constraints. Optimization algorithms and game theory are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue instability or unrealistic assumptions. Counter-arguments focus on robust optimization and scenario analysis. Resolution strategy involves optimization algorithms, game theory, and scenario analysis. Precedents include applications in economics, retail, and telecommunications.""",
        key_factors=["Revenue maximization", "Constraints", "Optimization algorithms", "Game theory"],
        primary_authority=["Varian, Microeconomic Analysis", "Osborne & Rubinstein, A Course in Game Theory"],
        burden_holder="Proponent of revenue maximization",
        adversary_position="Pricing strategies are unstable or rely on unrealistic assumptions.",
        counter_arguments=[
            "Instability in pricing.",
            "Unrealistic assumptions.",
            "Difficulty in constraint formulation."
        ],
        resolution_strategy="Optimization algorithms; game theory; scenario analysis.",
        entity_scope="Pricing optimization problems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Varian, Microeconomic Analysis"
    ),
    DoctrineBlock(
        topic="Optimal Routing in Networks",
        keywords=["routing", "network optimization", "constraints", "shortest path", "algorithms"],
        conclusion_template="Optimal routing in networks finds shortest paths under constraints using efficient algorithms.",
        reasoning_framework="""Optimal routing in networks involves finding shortest paths under constraints using efficient algorithms. The analysis begins by formulating the network and constraints. Algorithms such as Dijkstra's and Bellman-Ford are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue complexity or instability. Counter-arguments focus on algorithmic improvements and preprocessing. Resolution strategy involves efficient algorithms, preprocessing, and scenario analysis. Precedents include applications in transportation, telecommunications, and logistics.""",
        key_factors=["Shortest path", "Constraints", "Algorithmic efficiency", "Feasibility"],
        primary_authority=["Ahuja, Magnanti & Orlin, Network Flows", "Dijkstra, Shortest Path Algorithm"],
        burden_holder="Proponent of efficiency",
        adversary_position="Routing algorithms are inefficient or unstable.",
        counter_arguments=[
            "Complexity in large networks.",
            "Instability in routing.",
            "Difficulty in constraint satisfaction."
        ],
        resolution_strategy="Efficient algorithms; preprocessing; scenario analysis.",
        entity_scope="Network routing problems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ahuja, Magnanti & Orlin, Network Flows"
    ),
    DoctrineBlock(
        topic="Optimal Investment Strategies",
        keywords=["investment", "optimization", "risk", "return", "constraints"],
        conclusion_template="Optimal investment strategies balance risk and return under constraints using optimization.",
        reasoning_framework="""Optimal investment strategies involve balancing risk and return under constraints using optimization. The analysis begins by formulating the investment problem and constraints. Optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue instability or unrealistic assumptions. Counter-arguments focus on robust optimization and scenario analysis. Resolution strategy involves optimization algorithms, robust reformulation, and scenario analysis. Precedents include applications in finance, banking, and insurance.""",
        key_factors=["Risk", "Return", "Constraints", "Optimization algorithms"],
        primary_authority=["Markowitz, Portfolio Selection", "Ben-Tal & Nemirovski, Robust Optimization"],
        burden_holder="Proponent of risk modeling",
        adversary_position="Investment strategies rely on unrealistic assumptions.",
        counter_arguments=[
            "Unrealistic risk assumptions.",
            "Instability in optimization.",
            "Difficulty in constraint selection."
        ],
        resolution_strategy="Optimization algorithms; robust reformulation; scenario analysis.",
        entity_scope="Investment optimization problems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Markowitz, Portfolio Selection"
    ),
    DoctrineBlock(
        topic="Optimal Energy Management",
        keywords=["energy management", "optimization", "constraints", "network flow", "efficiency"],
        conclusion_template="Optimal energy management maximizes efficiency under constraints using network flow and optimization.",
        reasoning_framework="""Optimal energy management involves maximizing efficiency under constraints using network flow and optimization algorithms. The analysis begins by formulating the energy network and constraints. Network flow and optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue infeasibility or instability. Counter-arguments focus on decomposition and scenario analysis. Resolution strategy involves network flow algorithms, decomposition, and scenario analysis. Precedents include applications in power systems, transportation, and manufacturing.""",
        key_factors=["Network flow", "Constraints", "Efficiency", "Decomposition"],
        primary_authority=["Ahuja, Magnanti & Orlin, Network Flows", "Winston, Operations Research"],
        burden_holder="Proponent of efficiency",
        adversary_position="Energy management is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in decomposition."
        ],
        resolution_strategy="Network flow algorithms; decomposition; scenario analysis.",
        entity_scope="Energy management optimization problems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ahuja, Magnanti & Orlin, Network Flows"
    ),
    DoctrineBlock(
        topic="Optimal Traffic Flow",
        keywords=["traffic flow", "optimization", "constraints", "network flow", "efficiency"],
        conclusion_template="Optimal traffic flow maximizes efficiency under constraints using network flow and optimization.",
        reasoning_framework="""Optimal traffic flow involves maximizing efficiency under constraints using network flow and optimization algorithms. The analysis begins by formulating the traffic network and constraints. Network flow and optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue infeasibility or instability. Counter-arguments focus on decomposition and scenario analysis. Resolution strategy involves network flow algorithms, decomposition, and scenario analysis. Precedents include applications in transportation, urban planning, and logistics.""",
        key_factors=["Network flow", "Constraints", "Efficiency", "Decomposition"],
        primary_authority=["Ahuja, Magnanti & Orlin, Network Flows", "Winston, Operations Research"],
        burden_holder="Proponent of efficiency",
        adversary_position="Traffic flow optimization is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in decomposition."
        ],
        resolution_strategy="Network flow algorithms; decomposition; scenario analysis.",
        entity_scope="Traffic flow optimization problems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ahuja, Magnanti & Orlin, Network Flows"
    ),
    DoctrineBlock(
        topic="Optimal Healthcare Resource Allocation",
        keywords=["healthcare", "resource allocation", "optimization", "constraints", "efficiency"],
        conclusion_template="Optimal healthcare resource allocation maximizes efficiency under constraints using optimization algorithms.",
        reasoning_framework="""Optimal healthcare resource allocation involves maximizing efficiency under constraints using optimization algorithms. The analysis begins by formulating the healthcare resource allocation problem and constraints. Optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue infeasibility or instability. Counter-arguments focus on decomposition and scenario analysis. Resolution strategy involves optimization algorithms, decomposition, and scenario analysis. Precedents include applications in healthcare management, hospital operations, and public health.""",
        key_factors=["Constraints", "Efficiency", "Optimization algorithms", "Decomposition"],
        primary_authority=["Winston, Operations Research", "Bazaraa, Sherali & Shetty, Nonlinear Programming"],
        burden_holder="Proponent of efficiency",
        adversary_position="Healthcare resource allocation is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in decomposition."
        ],
        resolution_strategy="Optimization algorithms; decomposition; scenario analysis.",
        entity_scope="Healthcare resource allocation problems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Winston, Operations Research"
    ),
    DoctrineBlock(
        topic="Optimal Environmental Management",
        keywords=["environmental management", "optimization", "constraints", "efficiency", "robustness"],
        conclusion_template="Optimal environmental management maximizes efficiency and robustness under constraints using optimization algorithms.",
        reasoning_framework="""Optimal environmental management involves maximizing efficiency and robustness under constraints using optimization algorithms. The analysis begins by formulating the environmental management problem and constraints. Optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and robustness. Adversaries may argue infeasibility or instability. Counter-arguments focus on robust optimization and scenario analysis. Resolution strategy involves optimization algorithms, robust reformulation, and scenario analysis. Precedents include applications in environmental policy, resource management, and sustainability.""",
        key_factors=["Constraints", "Efficiency", "Robustness", "Optimization algorithms"],
        primary_authority=["Ben-Tal & Nemirovski, Robust Optimization", "Winston, Operations Research"],
        burden_holder="Proponent of robustness",
        adversary_position="Environmental management is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in robust formulation."
        ],
        resolution_strategy="Optimization algorithms; robust reformulation; scenario analysis.",
        entity_scope="Environmental management optimization problems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Ben-Tal & Nemirovski, Robust Optimization"
    ),
    DoctrineBlock(
        topic="Optimal Transportation Planning",
        keywords=["transportation planning", "optimization", "constraints", "network flow", "efficiency"],
        conclusion_template="Optimal transportation planning maximizes efficiency under constraints using network flow and optimization.",
        reasoning_framework="""Optimal transportation planning involves maximizing efficiency under constraints using network flow and optimization algorithms. The analysis begins by formulating the transportation network and constraints. Network flow and optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue infeasibility or instability. Counter-arguments focus on decomposition and scenario analysis. Resolution strategy involves network flow algorithms, decomposition, and scenario analysis. Precedents include applications in transportation, urban planning, and logistics.""",
        key_factors=["Network flow", "Constraints", "Efficiency", "Decomposition"],
        primary_authority=["Ahuja, Magnanti & Orlin, Network Flows", "Winston, Operations Research"],
        burden_holder="Proponent of efficiency",
        adversary_position="Transportation planning is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in decomposition."
        ],
        resolution_strategy="Network flow algorithms; decomposition; scenario analysis.",
        entity_scope="Transportation planning optimization problems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="Ahuja, Magnanti & Orlin, Network Flows"
    ),
    DoctrineBlock(
        topic="Optimal Manufacturing Process",
        keywords=["manufacturing", "process optimization", "constraints", "efficiency", "robustness"],
        conclusion_template="Optimal manufacturing process maximizes efficiency and robustness under constraints using optimization algorithms.",
        reasoning_framework="""Optimal manufacturing process optimization involves maximizing efficiency and robustness under constraints using optimization algorithms. The analysis begins by formulating the manufacturing process and constraints. Optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and robustness. Adversaries may argue infeasibility or instability. Counter-arguments focus on robust optimization and scenario analysis. Resolution strategy involves optimization algorithms, robust reformulation, and scenario analysis. Precedents include applications in manufacturing, engineering, and logistics.""",
        key_factors=["Constraints", "Efficiency", "Robustness", "Optimization algorithms"],
        primary_authority=["Ben-Tal & Nemirovski, Robust Optimization", "Winston, Operations Research"],
        burden_holder="Proponent of robustness",
        adversary_position="Manufacturing process optimization is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in robust formulation."
        ],
        resolution_strategy="Optimization algorithms; robust reformulation; scenario analysis.",
        entity_scope="Manufacturing process optimization problems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Ben-Tal & Nemirovski, Robust Optimization"
    ),
    DoctrineBlock(
        topic="Optimal Agricultural Management",
        keywords=["agricultural management", "optimization", "constraints", "efficiency", "robustness"],
        conclusion_template="Optimal agricultural management maximizes efficiency and robustness under constraints using optimization algorithms.",
        reasoning_framework="""Optimal agricultural management involves maximizing efficiency and robustness under constraints using optimization algorithms. The analysis begins by formulating the agricultural management problem and constraints. Optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and robustness. Adversaries may argue infeasibility or instability. Counter-arguments focus on robust optimization and scenario analysis. Resolution strategy involves optimization algorithms, robust reformulation, and scenario analysis. Precedents include applications in agriculture, resource management, and sustainability.""",
        key_factors=["Constraints", "Efficiency", "Robustness", "Optimization algorithms"],
        primary_authority=["Ben-Tal & Nemirovski, Robust Optimization", "Winston, Operations Research"],
        burden_holder="Proponent of robustness",
        adversary_position="Agricultural management optimization is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in robust formulation."
        ],
        resolution_strategy="Optimization algorithms; robust reformulation; scenario analysis.",
        entity_scope="Agricultural management optimization problems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Ben-Tal & Nemirovski, Robust Optimization"
    ),
    DoctrineBlock(
        topic="Optimal Water Resource Management",
        keywords=["water resource management", "optimization", "constraints", "efficiency", "robustness"],
        conclusion_template="Optimal water resource management maximizes efficiency and robustness under constraints using optimization algorithms.",
        reasoning_framework="""Optimal water resource management involves maximizing efficiency and robustness under constraints using optimization algorithms. The analysis begins by formulating the water resource management problem and constraints. Optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and robustness. Adversaries may argue infeasibility or instability. Counter-arguments focus on robust optimization and scenario analysis. Resolution strategy involves optimization algorithms, robust reformulation, and scenario analysis. Precedents include applications in water management, environmental policy, and sustainability.""",
        key_factors=["Constraints", "Efficiency", "Robustness", "Optimization algorithms"],
        primary_authority=["Ben-Tal & Nemirovski, Robust Optimization", "Winston, Operations Research"],
        burden_holder="Proponent of robustness",
        adversary_position="Water resource management optimization is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in robust formulation."
        ],
        resolution_strategy="Optimization algorithms; robust reformulation; scenario analysis.",
        entity_scope="Water resource management optimization problems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Ben-Tal & Nemirovski, Robust Optimization"
    ),
    DoctrineBlock(
        topic="Optimal Disaster Response Planning",
        keywords=["disaster response", "planning", "optimization", "constraints", "efficiency"],
        conclusion_template="Optimal disaster response planning maximizes efficiency under constraints using optimization algorithms.",
        reasoning_framework="""Optimal disaster response planning involves maximizing efficiency under constraints using optimization algorithms. The analysis begins by formulating the disaster response planning problem and constraints. Optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue infeasibility or instability. Counter-arguments focus on decomposition and scenario analysis. Resolution strategy involves optimization algorithms, decomposition, and scenario analysis. Precedents include applications in emergency management, logistics, and public safety.""",
        key_factors=["Constraints", "Efficiency", "Optimization algorithms", "Decomposition"],
        primary_authority=["Winston, Operations Research", "Bazaraa, Sherali & Shetty, Nonlinear Programming"],
        burden_holder="Proponent of efficiency",
        adversary_position="Disaster response planning is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in decomposition."
        ],
        resolution_strategy="Optimization algorithms; decomposition; scenario analysis.",
        entity_scope="Disaster response planning optimization problems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Winston, Operations Research"
    ),
    DoctrineBlock(
        topic="Optimal Public Policy Planning",
        keywords=["public policy", "planning", "optimization", "constraints", "efficiency"],
        conclusion_template="Optimal public policy planning maximizes efficiency under constraints using optimization algorithms.",
        reasoning_framework="""Optimal public policy planning involves maximizing efficiency under constraints using optimization algorithms. The analysis begins by formulating the public policy planning problem and constraints. Optimization algorithms are used for tractable solutions. The burden is on the analyst to ensure feasibility and optimality. Adversaries may argue infeasibility or instability. Counter-arguments focus on decomposition and scenario analysis. Resolution strategy involves optimization algorithms, decomposition, and scenario analysis. Precedents include applications in government, economics, and urban planning.""",
        key_factors=["Constraints", "Efficiency", "Optimization algorithms", "Decomposition"],
        primary_authority=["Winston, Operations Research", "Bazaraa, Sherali & Shetty, Nonlinear Programming"],
        burden_holder="Proponent of efficiency",
        adversary_position="Public policy planning is infeasible or unstable.",
        counter_arguments=[
            "Infeasibility due to constraints.",
            "Instability in optimization.",
            "Difficulty in decomposition."
        ],
        resolution_strategy="Optimization algorithms; decomposition; scenario analysis.",
        entity_scope="Public policy planning optimization problems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.MEDIUM.value,
        controlling_precedent="Winston, Operations Research"
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
        if keyword_lower in doctrine.topic.lower():
            results.append(doctrine)
            continue
        for k in doctrine.keywords:
            if keyword_lower in k.lower():
                results.append(doctrine)
                break
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]