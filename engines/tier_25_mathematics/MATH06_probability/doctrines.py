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
        topic="Law of Large Numbers",
        keywords=["law of large numbers", "LLN", "convergence", "sample mean", "probability"],
        conclusion_template="As the number of trials increases, the sample mean converges to the expected value.",
        reasoning_framework=(
            "The Law of Large Numbers (LLN) asserts that for a sequence of independent and identically distributed "
            "random variables with finite expected value, the sample average converges in probability to the expected value. "
            "Formally, for X₁, X₂, ..., Xₙ i.i.d. with E[Xᵢ]=μ, for any ε>0, P(|(1/n)ΣXᵢ - μ| > ε) → 0 as n→∞. "
            "The proof leverages Chebyshev's inequality, showing that the variance of the sample mean decreases with n. "
            "The LLN underpins statistical inference, justifying the use of sample means to estimate population means. "
            "There are two main forms: the Weak Law (convergence in probability) and the Strong Law (almost sure convergence). "
            "The LLN requires independence and identical distribution, though extensions exist for weaker conditions. "
            "Violations of these assumptions can invalidate the result. "
            "The LLN does not predict outcomes in the short run, only in the limit. "
            "It is foundational for frequentist probability and underlies the reliability of empirical averages."
        ),
        key_factors=[
            "Independence of trials",
            "Identical distribution",
            "Finite expected value",
            "Sample size",
            "Variance"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability (1933)",
            "William Feller, An Introduction to Probability Theory and Its Applications, Vol. 1"
        ],
        burden_holder="Proponent of convergence",
        adversary_position="Sample means may not converge to the expected value",
        counter_arguments=[
            "If variables are not independent, convergence may fail.",
            "Infinite variance can prevent convergence.",
            "Short-run deviations do not contradict the LLN."
        ],
        resolution_strategy="Verify independence and identical distribution; apply Chebyshev's inequality.",
        entity_scope="Random variables with finite mean",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Strong Law of Large Numbers"
    ),
    DoctrineBlock(
        topic="Central Limit Theorem",
        keywords=["central limit theorem", "CLT", "normal approximation", "sum of random variables"],
        conclusion_template="The sum (or average) of a large number of independent, identically distributed random variables is approximately normal.",
        reasoning_framework=(
            "The Central Limit Theorem (CLT) states that, given a sequence of i.i.d. random variables with finite mean μ and variance σ², "
            "the normalized sum converges in distribution to the standard normal as the number of terms increases. "
            "That is, for Sₙ = X₁ + ... + Xₙ, (Sₙ - nμ)/(σ√n) → N(0,1) as n→∞. "
            "The CLT justifies the use of normal approximations in statistics, even when the underlying distribution is not normal. "
            "The rate of convergence depends on the third moment (Lyapunov's condition). "
            "The Lindeberg-Feller theorem generalizes the CLT to non-identically distributed variables. "
            "The theorem underpins hypothesis testing, confidence intervals, and many statistical procedures. "
            "The CLT does not apply if the variance is infinite or if variables are not independent. "
            "It is a cornerstone of probability theory and statistical inference."
        ),
        key_factors=[
            "Independence",
            "Identical distribution",
            "Finite mean and variance",
            "Sample size",
            "Third moment (for rate of convergence)"
        ],
        primary_authority=[
            "A.M. Lyapunov, 1901",
            "Lindeberg-Feller Central Limit Theorem",
            "William Feller, An Introduction to Probability Theory and Its Applications, Vol. 2"
        ],
        burden_holder="Proponent of normal approximation",
        adversary_position="Sum may not be approximately normal",
        counter_arguments=[
            "Non-identical distributions may violate conditions.",
            "Infinite variance prevents convergence to normal.",
            "Dependence among variables invalidates the CLT."
        ],
        resolution_strategy="Check Lyapunov or Lindeberg conditions; verify independence and finite variance.",
        entity_scope="Sums/averages of i.i.d. random variables",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Lindeberg-Feller CLT"
    ),
    DoctrineBlock(
        topic="Conditional Probability",
        keywords=["conditional probability", "Bayes", "P(A|B)", "dependence"],
        conclusion_template="The probability of event A given event B is P(A|B) = P(A ∩ B) / P(B), provided P(B) > 0.",
        reasoning_framework=(
            "Conditional probability quantifies the likelihood of event A occurring given that event B has occurred. "
            "It is defined as P(A|B) = P(A ∩ B) / P(B), provided P(B) > 0. "
            "This concept is foundational for understanding dependence, independence, and Bayesian inference. "
            "Conditional probability is used to update beliefs in light of new evidence. "
            "It is symmetric only if A and B are independent. "
            "Bayes' theorem is derived from the definition of conditional probability. "
            "Care must be taken to ensure the conditioning event has positive probability. "
            "Misinterpretation can lead to errors such as the base rate fallacy."
        ),
        key_factors=[
            "Joint probability",
            "Probability of conditioning event",
            "Dependence structure",
            "Proper event definition"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability",
            "Joseph L. Doob, Stochastic Processes"
        ],
        burden_holder="Proponent of conditional probability calculation",
        adversary_position="Conditional probability is not well-defined or is misapplied",
        counter_arguments=[
            "P(B) = 0 makes P(A|B) undefined.",
            "Events may not be properly specified.",
            "Confusion between P(A|B) and P(B|A)."
        ],
        resolution_strategy="Verify P(B) > 0; clarify event definitions; apply the formal definition.",
        entity_scope="Events in a probability space",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Axioms"
    ),
    DoctrineBlock(
        topic="Bayes' Theorem",
        keywords=["Bayes' theorem", "posterior", "prior", "likelihood", "conditional probability"],
        conclusion_template="The posterior probability is P(A|B) = [P(B|A) * P(A)] / P(B), provided P(B) > 0.",
        reasoning_framework=(
            "Bayes' theorem provides a way to update the probability of a hypothesis (A) given new evidence (B). "
            "It relates the conditional and marginal probabilities of events: P(A|B) = P(B|A)P(A)/P(B). "
            "P(A) is the prior probability, P(B|A) is the likelihood, and P(A|B) is the posterior. "
            "The denominator P(B) can be computed as Σ P(B|Aᵢ)P(Aᵢ) over all hypotheses. "
            "Bayes' theorem is the foundation of Bayesian inference, allowing for the incorporation of new data. "
            "It is widely used in statistics, machine learning, and decision theory. "
            "Care must be taken with prior selection and with events of zero probability."
        ),
        key_factors=[
            "Prior probability",
            "Likelihood",
            "Marginal probability of evidence",
            "Proper event partition"
        ],
        primary_authority=[
            "Thomas Bayes, An Essay towards solving a Problem in the Doctrine of Chances (1763)",
            "Pierre-Simon Laplace, Théorie analytique des probabilités"
        ],
        burden_holder="Proponent of posterior calculation",
        adversary_position="Posterior probability is not correctly computed",
        counter_arguments=[
            "Incorrect priors can distort results.",
            "P(B) = 0 makes the formula undefined.",
            "Improper partitioning of hypotheses."
        ],
        resolution_strategy="Justify choice of priors; ensure P(B) > 0; partition hypothesis space correctly.",
        entity_scope="Discrete and continuous probability spaces",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Bayes' original essay"
    ),
    DoctrineBlock(
        topic="Independence of Events",
        keywords=["independence", "events", "probability", "joint probability"],
        conclusion_template="Events A and B are independent if P(A ∩ B) = P(A)P(B).",
        reasoning_framework=(
            "Two events A and B are independent if the occurrence of one does not affect the probability of the other. "
            "Formally, P(A ∩ B) = P(A)P(B). "
            "For more than two events, independence requires that every subset of events is independent in this sense. "
            "Independence is a key assumption in many probabilistic models. "
            "It is stronger than uncorrelatedness and must be verified, not assumed. "
            "Conditional independence is a related but distinct concept."
        ),
        key_factors=[
            "Joint probability",
            "Marginal probabilities",
            "Event structure",
            "Conditional independence"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability",
            "William Feller, An Introduction to Probability Theory"
        ],
        burden_holder="Proponent of independence",
        adversary_position="Events are not independent",
        counter_arguments=[
            "Events may be dependent due to underlying structure.",
            "Apparent independence may be spurious.",
            "Conditional dependence may exist."
        ],
        resolution_strategy="Test joint and marginal probabilities; examine event definitions.",
        entity_scope="Events in probability spaces",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Axioms"
    ),
    DoctrineBlock(
        topic="Total Probability Theorem",
        keywords=["total probability", "law of total probability", "partition", "marginal probability"],
        conclusion_template="P(B) = Σ P(B|Aᵢ)P(Aᵢ) over all elements of a partition {Aᵢ}.",
        reasoning_framework=(
            "The law of total probability expresses the probability of an event B as a sum over a partition of the sample space. "
            "If {A₁, ..., Aₙ} is a partition with P(Aᵢ) > 0, then P(B) = Σ P(B|Aᵢ)P(Aᵢ). "
            "This theorem is essential for computing probabilities by conditioning on mutually exclusive and exhaustive events. "
            "It underlies Bayesian inference and is used to decompose complex probabilities."
        ),
        key_factors=[
            "Partition of sample space",
            "Conditional probabilities",
            "Marginal probabilities",
            "Exhaustiveness and exclusivity"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of probability decomposition",
        adversary_position="Partition or probabilities are misapplied",
        counter_arguments=[
            "Partition may not be exhaustive or mutually exclusive.",
            "Conditional probabilities may be miscomputed.",
            "Events may not be properly defined."
        ],
        resolution_strategy="Verify partition properties; check conditional probabilities.",
        entity_scope="Finite or countable probability spaces",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Law of Total Probability"
    ),
    DoctrineBlock(
        topic="Random Variable",
        keywords=["random variable", "measurable function", "probability space", "distribution"],
        conclusion_template="A random variable is a measurable function from a probability space to the real numbers.",
        reasoning_framework=(
            "A random variable is a function X: Ω → ℝ defined on a probability space (Ω, F, P), "
            "such that for every Borel set B, the preimage X⁻¹(B) is in F. "
            "Random variables allow the assignment of numerical values to outcomes, enabling analysis using calculus and algebra. "
            "They can be discrete or continuous, and their distribution is induced by P via P(X ∈ B). "
            "Random variables are the foundation of probability theory, enabling the study of distributions, expectations, and more."
        ),
        key_factors=[
            "Measurability",
            "Probability space",
            "Distribution",
            "Domain and codomain"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability",
            "Joseph L. Doob, Stochastic Processes"
        ],
        burden_holder="Proponent of random variable definition",
        adversary_position="Function is not measurable or not properly defined",
        counter_arguments=[
            "Function may not be measurable.",
            "Domain or codomain may be incorrect.",
            "Distribution may not be well-defined."
        ],
        resolution_strategy="Check measurability; verify probability space structure.",
        entity_scope="Probability spaces",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Definition"
    ),
    DoctrineBlock(
        topic="Expectation",
        keywords=["expectation", "expected value", "mean", "integral", "average"],
        conclusion_template="The expectation of X is E[X] = ∑ xP(X=x) for discrete, or ∫ x dP(x) for continuous variables.",
        reasoning_framework=(
            "The expectation (mean) of a random variable X is the long-run average value it takes. "
            "For discrete X, E[X] = Σ xP(X=x). For continuous X, E[X] = ∫ x dP(x). "
            "Expectation is linear: E[aX + bY] = aE[X] + bE[Y]. "
            "It may not exist if the sum or integral diverges. "
            "Expectation is central to probability, statistics, and decision theory."
        ),
        key_factors=[
            "Distribution of X",
            "Convergence of sum or integral",
            "Linearity",
            "Existence of moments"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of expected value calculation",
        adversary_position="Expectation does not exist or is miscalculated",
        counter_arguments=[
            "Divergent sums or integrals.",
            "Incorrect application of linearity.",
            "Non-measurable random variables."
        ],
        resolution_strategy="Verify convergence; check conditions for linearity.",
        entity_scope="Random variables with finite mean",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Definition"
    ),
    DoctrineBlock(
        topic="Variance",
        keywords=["variance", "dispersion", "second moment", "expected value", "spread"],
        conclusion_template="Variance is Var(X) = E[(X - E[X])²].",
        reasoning_framework=(
            "Variance measures the spread of a random variable around its mean. "
            "It is defined as Var(X) = E[(X - E[X])²]. "
            "For discrete X, Var(X) = Σ (x - μ)²P(X=x). "
            "Variance is non-negative and is zero only for constant random variables. "
            "It is additive for independent variables: Var(X+Y) = Var(X) + Var(Y). "
            "Variance may not exist if the second moment diverges."
        ),
        key_factors=[
            "Mean of X",
            "Second moment",
            "Independence (for additivity)",
            "Existence of variance"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of variance calculation",
        adversary_position="Variance does not exist or is misapplied",
        counter_arguments=[
            "Second moment may diverge.",
            "Incorrect application of additivity.",
            "Non-measurable random variables."
        ],
        resolution_strategy="Check existence of second moment; verify independence for additivity.",
        entity_scope="Random variables with finite variance",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Definition"
    ),
    DoctrineBlock(
        topic="Covariance",
        keywords=["covariance", "joint variability", "dependence", "second moment"],
        conclusion_template="Cov(X, Y) = E[(X - E[X])(Y - E[Y])].",
        reasoning_framework=(
            "Covariance measures the joint variability of two random variables. "
            "It is defined as Cov(X, Y) = E[(X - E[X])(Y - E[Y])]. "
            "Covariance is zero if X and Y are independent, but the converse is not necessarily true. "
            "It is used to assess linear relationships and is the basis for correlation."
        ),
        key_factors=[
            "Means of X and Y",
            "Joint distribution",
            "Existence of second moments",
            "Independence"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of covariance calculation",
        adversary_position="Covariance does not exist or is misapplied",
        counter_arguments=[
            "Second moments may diverge.",
            "Covariance may be zero without independence.",
            "Non-measurable random variables."
        ],
        resolution_strategy="Check existence of second moments; clarify interpretation.",
        entity_scope="Pairs of random variables with finite second moments",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Definition"
    ),
    DoctrineBlock(
        topic="Correlation",
        keywords=["correlation", "linear relationship", "Pearson", "dependence"],
        conclusion_template="The correlation coefficient is ρ(X, Y) = Cov(X, Y) / (σ_X σ_Y).",
        reasoning_framework=(
            "Correlation quantifies the linear relationship between two random variables. "
            "The Pearson correlation coefficient is ρ(X, Y) = Cov(X, Y) / (σ_X σ_Y), where σ_X and σ_Y are standard deviations. "
            "Correlation is dimensionless and lies in [-1, 1]. "
            "A value of 0 indicates no linear relationship, but not necessarily independence. "
            "Correlation is sensitive to outliers and only captures linear dependence."
        ),
        key_factors=[
            "Covariance",
            "Standard deviations",
            "Linearity",
            "Outlier sensitivity"
        ],
        primary_authority=[
            "Karl Pearson, 1896",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of correlation calculation",
        adversary_position="Correlation is misinterpreted or misapplied",
        counter_arguments=[
            "Correlation does not imply causation.",
            "Nonlinear relationships may exist.",
            "Outliers can distort correlation."
        ],
        resolution_strategy="Check for linearity; examine scatterplots; consider robust measures.",
        entity_scope="Pairs of random variables with finite variance",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Pearson's Definition"
    ),
    DoctrineBlock(
        topic="Markov's Inequality",
        keywords=["Markov's inequality", "tail bound", "non-negative random variable"],
        conclusion_template="For non-negative X and a > 0, P(X ≥ a) ≤ E[X]/a.",
        reasoning_framework=(
            "Markov's inequality provides an upper bound on the probability that a non-negative random variable exceeds a threshold. "
            "For X ≥ 0 and a > 0, P(X ≥ a) ≤ E[X]/a. "
            "It is a general result, requiring only the existence of the expectation. "
            "Markov's inequality is used to derive other inequalities, such as Chebyshev's."
        ),
        key_factors=[
            "Non-negativity of X",
            "Existence of expectation",
            "Threshold a > 0"
        ],
        primary_authority=[
            "A.A. Markov, 1884",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of probability bound",
        adversary_position="Inequality does not hold or is misapplied",
        counter_arguments=[
            "X may take negative values.",
            "Expectation may not exist.",
            "Threshold may be misapplied."
        ],
        resolution_strategy="Verify non-negativity and existence of expectation.",
        entity_scope="Non-negative random variables",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Markov's Inequality"
    ),
    DoctrineBlock(
        topic="Chebyshev's Inequality",
        keywords=["Chebyshev's inequality", "variance", "tail bound", "concentration"],
        conclusion_template="For any k > 0, P(|X - E[X]| ≥ k) ≤ Var(X)/k².",
        reasoning_framework=(
            "Chebyshev's inequality bounds the probability that a random variable deviates from its mean. "
            "For any random variable X with finite mean μ and variance σ², P(|X - μ| ≥ k) ≤ σ²/k² for k > 0. "
            "It requires only the existence of variance and is distribution-free. "
            "Chebyshev's inequality is used in proving the Law of Large Numbers."
        ),
        key_factors=[
            "Finite mean and variance",
            "Deviation threshold k > 0",
            "Distribution-free"
        ],
        primary_authority=[
            "P.L. Chebyshev, 1867",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of probability bound",
        adversary_position="Inequality does not hold or is misapplied",
        counter_arguments=[
            "Variance may not exist.",
            "Threshold may be misapplied.",
            "Inequality is loose for some distributions."
        ],
        resolution_strategy="Check existence of variance; clarify use case.",
        entity_scope="Random variables with finite variance",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Chebyshev's Inequality"
    ),
    DoctrineBlock(
        topic="Borel-Cantelli Lemma",
        keywords=["Borel-Cantelli", "almost sure", "infinite sequence", "probability zero"],
        conclusion_template="If Σ P(Aₙ) < ∞, then P(lim sup Aₙ) = 0.",
        reasoning_framework=(
            "The Borel-Cantelli lemma concerns the occurrence of events in infinite sequences. "
            "If {Aₙ} is a sequence of events with Σ P(Aₙ) < ∞, then with probability 1, only finitely many Aₙ occur. "
            "The second Borel-Cantelli lemma states that if the events are independent and Σ P(Aₙ) = ∞, then infinitely many Aₙ occur with probability 1."
        ),
        key_factors=[
            "Sum of probabilities",
            "Independence (for converse)",
            "Infinite sequence of events"
        ],
        primary_authority=[
            "Émile Borel, 1909",
            "Francesco Paolo Cantelli, 1917",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of almost sure statement",
        adversary_position="Events may occur infinitely often despite sum being finite",
        counter_arguments=[
            "Dependence can invalidate the converse.",
            "Events may not be properly defined.",
            "Sum may diverge."
        ],
        resolution_strategy="Check sum of probabilities; verify independence for converse.",
        entity_scope="Sequences of events in probability spaces",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Borel-Cantelli Lemma"
    ),
    DoctrineBlock(
        topic="Sigma-Algebra",
        keywords=["sigma-algebra", "measurable sets", "probability space", "events"],
        conclusion_template="A σ-algebra is a collection of subsets closed under complements and countable unions.",
        reasoning_framework=(
            "A σ-algebra F on a set Ω is a collection of subsets containing Ω, closed under complements and countable unions. "
            "It defines the set of events to which probabilities can be assigned. "
            "The triple (Ω, F, P) is the foundation of modern probability theory."
        ),
        key_factors=[
            "Closure under complements",
            "Closure under countable unions",
            "Contains Ω"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability"
        ],
        burden_holder="Proponent of σ-algebra structure",
        adversary_position="Collection is not a σ-algebra",
        counter_arguments=[
            "Closure properties may fail.",
            "Not all subsets are included.",
            "Improper definition of Ω."
        ],
        resolution_strategy="Check closure properties; verify inclusion of Ω.",
        entity_scope="Probability spaces",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Definition"
    ),
    DoctrineBlock(
        topic="Probability Measure",
        keywords=["probability measure", "axioms", "countable additivity", "non-negativity"],
        conclusion_template="A probability measure P assigns to each event a number in [0,1], with P(Ω)=1 and countable additivity.",
        reasoning_framework=(
            "A probability measure P on (Ω, F) assigns to each event in F a number in [0,1], with P(Ω)=1. "
            "It is countably additive: for disjoint events A₁, A₂, ..., P(∪Aᵢ) = ΣP(Aᵢ). "
            "Probability measures formalize the concept of chance in modern probability theory."
        ),
        key_factors=[
            "Non-negativity",
            "Normalization (P(Ω)=1)",
            "Countable additivity"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability"
        ],
        burden_holder="Proponent of probability measure",
        adversary_position="Measure does not satisfy axioms",
        counter_arguments=[
            "Additivity may fail.",
            "Normalization may be violated.",
            "Negative probabilities are not allowed."
        ],
        resolution_strategy="Check all three Kolmogorov axioms.",
        entity_scope="Probability spaces",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Axioms"
    ),
    DoctrineBlock(
        topic="Discrete Probability Distribution",
        keywords=["discrete distribution", "probability mass function", "pmf", "finite", "countable"],
        conclusion_template="A discrete probability distribution assigns probabilities to countable outcomes, summing to 1.",
        reasoning_framework=(
            "A discrete probability distribution is defined by a probability mass function (pmf) p(x), assigning P(X=x) for each x in a countable set. "
            "The sum over all x must be 1, and each p(x) ≥ 0. "
            "Examples include the binomial, Poisson, and geometric distributions."
        ),
        key_factors=[
            "Countable outcome space",
            "Non-negative probabilities",
            "Normalization"
        ],
        primary_authority=[
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of distribution definition",
        adversary_position="Distribution does not sum to 1 or includes negative probabilities",
        counter_arguments=[
            "Sum may not be 1.",
            "Negative probabilities are not allowed.",
            "Outcome space may not be countable."
        ],
        resolution_strategy="Check normalization and non-negativity.",
        entity_scope="Discrete random variables",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Feller's Definition"
    ),
    DoctrineBlock(
        topic="Continuous Probability Distribution",
        keywords=["continuous distribution", "probability density function", "pdf", "integration"],
        conclusion_template="A continuous probability distribution is described by a pdf f(x), with ∫ f(x) dx = 1.",
        reasoning_framework=(
            "A continuous probability distribution is specified by a probability density function (pdf) f(x), with f(x) ≥ 0 for all x and ∫ f(x) dx = 1. "
            "Probabilities are computed as integrals over intervals: P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx. "
            "Examples include the normal, exponential, and uniform distributions."
        ),
        key_factors=[
            "Non-negative pdf",
            "Normalization",
            "Integration over intervals"
        ],
        primary_authority=[
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of distribution definition",
        adversary_position="Pdf is not normalized or is negative",
        counter_arguments=[
            "Pdf may be negative.",
            "Integral may not be 1.",
            "Improper domain."
        ],
        resolution_strategy="Check normalization and non-negativity.",
        entity_scope="Continuous random variables",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Feller's Definition"
    ),
    DoctrineBlock(
        topic="Joint Distribution",
        keywords=["joint distribution", "multivariate", "pmf", "pdf", "dependence"],
        conclusion_template="A joint distribution specifies probabilities for all combinations of values of two or more random variables.",
        reasoning_framework=(
            "A joint distribution describes the probability structure of two or more random variables. "
            "For discrete variables, it is given by a joint pmf; for continuous, by a joint pdf. "
            "Marginal and conditional distributions can be derived from the joint distribution. "
            "Dependence and independence are characterized by the structure of the joint distribution."
        ),
        key_factors=[
            "Marginalization",
            "Conditional distributions",
            "Normalization",
            "Dependence structure"
        ],
        primary_authority=[
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of joint distribution",
        adversary_position="Joint distribution is not properly defined",
        counter_arguments=[
            "Normalization may fail.",
            "Dependence structure may be misrepresented.",
            "Marginals may not be consistent."
        ],
        resolution_strategy="Check normalization and marginal consistency.",
        entity_scope="Pairs or tuples of random variables",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Feller's Definition"
    ),
    DoctrineBlock(
        topic="Marginal Distribution",
        keywords=["marginal distribution", "joint distribution", "integration", "summation"],
        conclusion_template="The marginal distribution of X is obtained by summing/integrating the joint distribution over other variables.",
        reasoning_framework=(
            "The marginal distribution of a random variable is derived from the joint distribution by summing (discrete) or integrating (continuous) over the other variables. "
            "For example, if (X, Y) has joint pmf p(x, y), then the marginal pmf of X is p_X(x) = Σ_y p(x, y). "
            "Marginals are essential for understanding the behavior of individual variables in multivariate settings."
        ),
        key_factors=[
            "Joint distribution",
            "Summation or integration",
            "Proper domain"
        ],
        primary_authority=[
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of marginalization",
        adversary_position="Marginal distribution is not correctly computed",
        counter_arguments=[
            "Summation/integration may be over the wrong domain.",
            "Joint distribution may not be normalized.",
            "Variables may not be properly defined."
        ],
        resolution_strategy="Verify domain and normalization.",
        entity_scope="Multivariate random variables",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Feller's Definition"
    ),
    DoctrineBlock(
        topic="Conditional Expectation",
        keywords=["conditional expectation", "E[X|Y]", "random variable", "sigma-algebra"],
        conclusion_template="E[X|Y] is the expected value of X given Y, a random variable measurable with respect to Y.",
        reasoning_framework=(
            "Conditional expectation E[X|Y] is a random variable representing the expected value of X given the value of Y. "
            "It is defined as the best mean-square predictor of X given Y. "
            "Formally, E[X|Y] is measurable with respect to the σ-algebra generated by Y, and for any function g, E[Xg(Y)] = E[E[X|Y]g(Y)]. "
            "Conditional expectation generalizes the concept of conditioning to random variables and σ-algebras."
        ),
        key_factors=[
            "Measurability",
            "σ-algebra",
            "Integrability of X",
            "Law of total expectation"
        ],
        primary_authority=[
            "Joseph L. Doob, Stochastic Processes",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of conditional expectation",
        adversary_position="Conditional expectation is not properly defined",
        counter_arguments=[
            "X may not be integrable.",
            "σ-algebra may be misidentified.",
            "Measurability may fail."
        ],
        resolution_strategy="Check integrability and σ-algebra structure.",
        entity_scope="Integrable random variables",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Doob's Definition"
    ),
    DoctrineBlock(
        topic="Law of Total Expectation",
        keywords=["law of total expectation", "tower property", "iterated expectation"],
        conclusion_template="E[X] = E[E[X|Y]].",
        reasoning_framework=(
            "The law of total expectation (tower property) states that the expectation of X is the expectation of its conditional expectation given Y: E[X] = E[E[X|Y]]. "
            "This holds for integrable random variables and is fundamental in probability and statistics. "
            "It allows for the decomposition of expectations and is used in sequential analysis and Bayesian inference."
        ),
        key_factors=[
            "Integrability of X",
            "Proper conditioning",
            "σ-algebra structure"
        ],
        primary_authority=[
            "Joseph L. Doob, Stochastic Processes",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of law application",
        adversary_position="Law does not hold or is misapplied",
        counter_arguments=[
            "X may not be integrable.",
            "Conditioning may be improper.",
            "σ-algebra may be misidentified."
        ],
        resolution_strategy="Check integrability and conditioning.",
        entity_scope="Integrable random variables",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Doob's Tower Property"
    ),
    DoctrineBlock(
        topic="Moment Generating Function",
        keywords=["moment generating function", "mgf", "moments", "uniqueness"],
        conclusion_template="The mgf of X is M_X(t) = E[e^{tX}], which encodes all moments if it exists in a neighborhood of 0.",
        reasoning_framework=(
            "The moment generating function (mgf) of a random variable X is M_X(t) = E[e^{tX}]. "
            "If the mgf exists in a neighborhood of 0, it uniquely determines the distribution of X. "
            "The nth derivative at t=0 gives the nth moment. "
            "Not all random variables have an mgf, but when they do, it is a powerful tool for analysis."
        ),
        key_factors=[
            "Existence of mgf",
            "Neighborhood of 0",
            "Moment extraction",
            "Uniqueness"
        ],
        primary_authority=[
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of mgf use",
        adversary_position="Mgf does not exist or does not determine distribution",
        counter_arguments=[
            "Mgf may not exist everywhere.",
            "Different distributions may share the same moments.",
            "Characteristic function may be preferable."
        ],
        resolution_strategy="Check existence and uniqueness; consider characteristic function.",
        entity_scope="Random variables with mgf",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Feller's Definition"
    ),
    DoctrineBlock(
        topic="Characteristic Function",
        keywords=["characteristic function", "Fourier transform", "distribution", "uniqueness"],
        conclusion_template="The characteristic function of X is φ_X(t) = E[e^{itX}], which always exists and uniquely determines the distribution.",
        reasoning_framework=(
            "The characteristic function φ_X(t) = E[e^{itX}] exists for all real t and all random variables. "
            "It uniquely determines the distribution and is used in limit theorems and proofs of convergence. "
            "The characteristic function is the Fourier transform of the probability measure."
        ),
        key_factors=[
            "Existence for all t",
            "Uniqueness",
            "Fourier inversion",
            "Convergence in distribution"
        ],
        primary_authority=[
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of characteristic function use",
        adversary_position="Characteristic function does not determine distribution",
        counter_arguments=[
            "Pathological cases may exist.",
            "Inversion may be technically challenging.",
            "Interpretation may be non-intuitive."
        ],
        resolution_strategy="Apply Fourier inversion; check uniqueness.",
        entity_scope="All random variables",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="Feller's Definition"
    ),
    DoctrineBlock(
        topic="Poisson Process",
        keywords=["Poisson process", "counting process", "exponential interarrival", "stationarity", "independent increments"],
        conclusion_template="A Poisson process is a counting process with stationary, independent increments and exponential interarrival times.",
        reasoning_framework=(
            "A Poisson process is a stochastic process {N(t), t ≥ 0} with N(0)=0, stationary and independent increments, and P(N(t+h)-N(t)=1) ≈ λh for small h. "
            "Interarrival times are exponentially distributed with rate λ. "
            "The Poisson process models random arrivals in time and is foundational in queueing theory and stochastic processes."
        ),
        key_factors=[
            "Stationary increments",
            "Independent increments",
            "Exponential interarrival times",
            "Rate parameter λ"
        ],
        primary_authority=[
            "William Feller, Probability Theory",
            "Joseph L. Doob, Stochastic Processes"
        ],
        burden_holder="Proponent of Poisson process model",
        adversary_position="Process does not satisfy Poisson properties",
        counter_arguments=[
            "Increments may not be independent.",
            "Interarrival times may not be exponential.",
            "Rate parameter may be time-varying."
        ],
        resolution_strategy="Check increment properties and interarrival distribution.",
        entity_scope="Counting processes",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Feller's Definition"
    ),
    DoctrineBlock(
        topic="Martingale",
        keywords=["martingale", "fair game", "conditional expectation", "stochastic process"],
        conclusion_template="A process {Xₙ} is a martingale if E[Xₙ₊₁ | Fₙ] = Xₙ for all n.",
        reasoning_framework=(
            "A martingale is a stochastic process {Xₙ, Fₙ} such that E[|Xₙ|] < ∞ and E[Xₙ₊₁ | Fₙ] = Xₙ for all n. "
            "Martingales model fair games and are central in modern probability theory. "
            "They have important convergence properties and are used in finance and stochastic calculus."
        ),
        key_factors=[
            "Integrability",
            "Conditional expectation",
            "Filtration",
            "Fairness"
        ],
        primary_authority=[
            "Joseph L. Doob, Stochastic Processes"
        ],
        burden_holder="Proponent of martingale property",
        adversary_position="Process is not a martingale",
        counter_arguments=[
            "Conditional expectation may not equal current value.",
            "Filtration may be misdefined.",
            "Integrability may fail."
        ],
        resolution_strategy="Check conditional expectation and filtration.",
        entity_scope="Stochastic processes",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Doob's Martingale Theory"
    ),
    DoctrineBlock(
        topic="Stopping Time",
        keywords=["stopping time", "filtration", "random time", "optional sampling"],
        conclusion_template="A stopping time T is a random variable such that {T ≤ n} ∈ Fₙ for all n.",
        reasoning_framework=(
            "A stopping time with respect to a filtration {Fₙ} is a random variable T such that for each n, the event {T ≤ n} is in Fₙ. "
            "Stopping times formalize the idea of random times determined by observable information. "
            "They are essential in martingale theory and the optional sampling theorem."
        ),
        key_factors=[
            "Filtration",
            "Measurability",
            "Adaptedness",
            "Optional sampling"
        ],
        primary_authority=[
            "Joseph L. Doob, Stochastic Processes"
        ],
        burden_holder="Proponent of stopping time property",
        adversary_position="Random time is not a stopping time",
        counter_arguments=[
            "Measurability may fail.",
            "Filtration may be misdefined.",
            "Random time may depend on future information."
        ],
        resolution_strategy="Check measurability with respect to filtration.",
        entity_scope="Stochastic processes",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Doob's Definition"
    ),
    DoctrineBlock(
        topic="Optional Stopping Theorem",
        keywords=["optional stopping", "martingale", "stopping time", "fair game"],
        conclusion_template="If {Xₙ} is a martingale and T is a bounded stopping time, then E[X_T] = E[X_0].",
        reasoning_framework=(
            "The optional stopping theorem states that, under certain conditions, the expected value of a martingale at a stopping time equals its initial value. "
            "If T is a bounded stopping time and {Xₙ} is a martingale, then E[X_T] = E[X_0]. "
            "The theorem requires integrability and certain regularity conditions."
        ),
        key_factors=[
            "Martingale property",
            "Bounded stopping time",
            "Integrability",
            "Filtration"
        ],
        primary_authority=[
            "Joseph L. Doob, Stochastic Processes"
        ],
        burden_holder="Proponent of optional stopping",
        adversary_position="E[X_T] ≠ E[X_0] or conditions are not met",
        counter_arguments=[
            "T may not be bounded.",
            "Process may not be a martingale.",
            "Integrability may fail."
        ],
        resolution_strategy="Check all conditions for the theorem.",
        entity_scope="Martingales and stopping times",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Doob's Optional Stopping Theorem"
    ),
    DoctrineBlock(
        topic="Ergodic Theorem",
        keywords=["ergodic theorem", "time average", "ensemble average", "stationarity"],
        conclusion_template="For ergodic processes, time averages converge to ensemble averages.",
        reasoning_framework=(
            "The ergodic theorem states that, for ergodic stationary processes, the time average converges to the expected value. "
            "Formally, for a stationary process {Xₙ}, (1/n)Σ Xₖ → E[X₁] almost surely as n→∞. "
            "Ergodicity ensures that long-run averages reflect the underlying probability distribution."
        ),
        key_factors=[
            "Stationarity",
            "Ergodicity",
            "Time average",
            "Ensemble average"
        ],
        primary_authority=[
            "George D. Birkhoff, 1931",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of ergodic convergence",
        adversary_position="Process is not ergodic or stationary",
        counter_arguments=[
            "Process may not be stationary.",
            "Ergodicity may fail.",
            "Convergence may not occur."
        ],
        resolution_strategy="Check stationarity and ergodicity.",
        entity_scope="Stationary stochastic processes",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Birkhoff's Ergodic Theorem"
    ),
    DoctrineBlock(
        topic="Exchangeability",
        keywords=["exchangeability", "de Finetti", "symmetry", "random variables"],
        conclusion_template="A sequence is exchangeable if its joint distribution is invariant under permutations.",
        reasoning_framework=(
            "A sequence of random variables is exchangeable if the joint distribution is unchanged by any finite permutation. "
            "De Finetti's theorem states that any infinite exchangeable sequence is a mixture of i.i.d. sequences. "
            "Exchangeability generalizes independence and is important in Bayesian statistics."
        ),
        key_factors=[
            "Permutation invariance",
            "Joint distribution",
            "De Finetti's theorem",
            "Mixtures"
        ],
        primary_authority=[
            "Bruno de Finetti, 1931",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of exchangeability",
        adversary_position="Sequence is not exchangeable",
        counter_arguments=[
            "Joint distribution may change under permutation.",
            "Sequence may not be infinite.",
            "Dependence structure may be complex."
        ],
        resolution_strategy="Test for permutation invariance.",
        entity_scope="Sequences of random variables",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="de Finetti's Theorem"
    ),
    DoctrineBlock(
        topic="Zero-One Laws",
        keywords=["zero-one law", "Kolmogorov", "tail event", "probability"],
        conclusion_template="Tail events have probability 0 or 1.",
        reasoning_framework=(
            "Zero-one laws state that certain events, called tail events, must have probability 0 or 1. "
            "Kolmogorov's zero-one law applies to sequences of independent random variables: any event depending only on the tail σ-algebra has probability 0 or 1. "
            "This result is used to classify events as almost sure or almost impossible."
        ),
        key_factors=[
            "Tail σ-algebra",
            "Independence",
            "Event structure",
            "Kolmogorov's law"
        ],
        primary_authority=[
            "A.N. Kolmogorov, 1933",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of zero-one law",
        adversary_position="Tail event has probability strictly between 0 and 1",
        counter_arguments=[
            "Event may not be a tail event.",
            "Independence may fail.",
            "σ-algebra may be misidentified."
        ],
        resolution_strategy="Check tail σ-algebra and independence.",
        entity_scope="Sequences of independent random variables",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Zero-One Law"
    ),
    DoctrineBlock(
        topic="Large Deviations Principle",
        keywords=["large deviations", "rate function", "exponential decay", "rare events"],
        conclusion_template="The probability of large deviations decays exponentially with the sample size.",
        reasoning_framework=(
            "The large deviations principle (LDP) quantifies the exponential decay of probabilities of rare events. "
            "For sums of i.i.d. random variables, P(Sₙ/n ≥ a) ≈ exp(-nI(a)), where I(a) is the rate function. "
            "LDP provides precise asymptotics for probabilities of deviations from the mean."
        ),
        key_factors=[
            "Rate function",
            "Exponential decay",
            "Sample size",
            "Rare events"
        ],
        primary_authority=[
            "S.R.S. Varadhan, Large Deviations and Applications (1984)",
            "A. Dembo, O. Zeitouni, Large Deviations Techniques and Applications"
        ],
        burden_holder="Proponent of large deviations estimate",
        adversary_position="Decay is not exponential or rate function is misapplied",
        counter_arguments=[
            "Non-i.i.d. variables may not satisfy LDP.",
            "Rate function may be miscomputed.",
            "Finite sample corrections may be needed."
        ],
        resolution_strategy="Check LDP conditions and rate function.",
        entity_scope="Sums of random variables",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Varadhan's LDP"
    ),
    DoctrineBlock(
        topic="Measure-Theoretic Probability",
        keywords=["measure theory", "probability space", "integration", "modern probability"],
        conclusion_template="Probability is formalized as a measure on a σ-algebra.",
        reasoning_framework=(
            "Measure-theoretic probability defines probability as a measure P on a σ-algebra F over a sample space Ω. "
            "Random variables are measurable functions, and expectations are integrals with respect to P. "
            "This framework allows for rigorous treatment of continuous and infinite probability spaces."
        ),
        key_factors=[
            "σ-algebra",
            "Measure",
            "Integration",
            "Measurability"
        ],
        primary_authority=[
            "A.N. Kolmogorov, Foundations of the Theory of Probability"
        ],
        burden_holder="Proponent of measure-theoretic framework",
        adversary_position="Probability is not a measure or is not well-defined",
        counter_arguments=[
            "σ-algebra may be improperly defined.",
            "Measure may not be countably additive.",
            "Integration may fail."
        ],
        resolution_strategy="Verify all measure-theoretic axioms.",
        entity_scope="All probability spaces",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="Kolmogorov's Axioms"
    ),
    DoctrineBlock(
        topic="Bayesian Inference",
        keywords=["Bayesian inference", "posterior", "prior", "likelihood", "update"],
        conclusion_template="Bayesian inference updates beliefs via the posterior: P(θ|data) ∝ P(data|θ)P(θ).",
        reasoning_framework=(
            "Bayesian inference is a framework for updating beliefs about parameters θ given data. "
            "The posterior distribution is P(θ|data) = P(data|θ)P(θ)/P(data), where P(θ) is the prior and P(data|θ) is the likelihood. "
            "Bayesian methods incorporate prior information and provide a probabilistic interpretation of inference."
        ),
        key_factors=[
            "Prior distribution",
            "Likelihood",
            "Posterior normalization",
            "Model specification"
        ],
        primary_authority=[
            "Thomas Bayes, 1763",
            "Pierre-Simon Laplace, 1812"
        ],
        burden_holder="Proponent of Bayesian update",
        adversary_position="Posterior is not correctly computed or prior is inappropriate",
        counter_arguments=[
            "Choice of prior may be subjective.",
            "Likelihood may be mis-specified.",
            "Normalization may be intractable."
        ],
        resolution_strategy="Justify prior; check likelihood; use computational methods for normalization.",
        entity_scope="Statistical inference",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Bayes' Theorem"
    ),
    DoctrineBlock(
        topic="Frequentist Inference",
        keywords=["frequentist inference", "sampling distribution", "confidence interval", "hypothesis testing"],
        conclusion_template="Frequentist inference draws conclusions based on the sampling distribution of estimators.",
        reasoning_framework=(
            "Frequentist inference evaluates estimators and tests based on their sampling distributions under repeated sampling. "
            "Confidence intervals and p-values are interpreted in terms of long-run frequencies. "
            "Frequentist methods do not use prior distributions and focus on objective properties."
        ),
        key_factors=[
            "Sampling distribution",
            "Estimator properties",
            "Long-run frequency",
            "No prior"
        ],
        primary_authority=[
            "R.A. Fisher, Statistical Methods for Research Workers (1925)",
            "Jerzy Neyman, Egon Pearson, 1933"
        ],
        burden_holder="Proponent of frequentist method",
        adversary_position="Inference is not justified by sampling distribution",
        counter_arguments=[
            "Interpretation may be counterintuitive.",
            "No incorporation of prior information.",
            "Reliance on asymptotic properties."
        ],
        resolution_strategy="Clarify interpretation; check sampling distribution.",
        entity_scope="Statistical inference",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Fisher-Neyman-Pearson Theory"
    ),
    DoctrineBlock(
        topic="Maximum Likelihood Estimation",
        keywords=["maximum likelihood", "MLE", "estimation", "likelihood function"],
        conclusion_template="The MLE is the parameter value maximizing the likelihood function given the data.",
        reasoning_framework=(
            "Maximum likelihood estimation selects the parameter value θ̂ that maximizes the likelihood function L(θ|data). "
            "MLEs are consistent, asymptotically normal, and efficient under regularity conditions. "
            "They are widely used in statistical modeling and inference."
        ),
        key_factors=[
            "Likelihood function",
            "Parameter space",
            "Consistency",
            "Regularity conditions"
        ],
        primary_authority=[
            "R.A. Fisher, 1922"
        ],
        burden_holder="Proponent of MLE",
        adversary_position="MLE is not appropriate or does not exist",
        counter_arguments=[
            "Likelihood may be flat or multimodal.",
            "Parameter space may be constrained.",
            "Regularity conditions may fail."
        ],
        resolution_strategy="Check likelihood shape and regularity conditions.",
        entity_scope="Statistical models",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Fisher's MLE Theory"
    ),
    DoctrineBlock(
        topic="Confidence Interval",
        keywords=["confidence interval", "frequentist", "coverage probability", "estimation"],
        conclusion_template="A confidence interval is a random interval with a specified coverage probability for the parameter.",
        reasoning_framework=(
            "A confidence interval is constructed so that, over repeated samples, it contains the true parameter with a specified probability (e.g., 95%). "
            "The interval is random; the parameter is fixed. "
            "Interpretation is in terms of long-run frequency, not probability of the parameter."
        ),
        key_factors=[
            "Coverage probability",
            "Sampling distribution",
            "Estimator properties",
            "Interpretation"
        ],
        primary_authority=[
            "Jerzy Neyman, 1937"
        ],
        burden_holder="Proponent of interval construction",
        adversary_position="Interval does not have correct coverage",
        counter_arguments=[
            "Coverage probability may be miscomputed.",
            "Interpretation may be misunderstood.",
            "Estimator may be biased."
        ],
        resolution_strategy="Check construction and interpretation.",
        entity_scope="Statistical inference",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Neyman's Confidence Interval Theory"
    ),
    DoctrineBlock(
        topic="Hypothesis Testing",
        keywords=["hypothesis testing", "null hypothesis", "p-value", "significance level"],
        conclusion_template="Hypothesis testing evaluates evidence against a null hypothesis using a test statistic and p-value.",
        reasoning_framework=(
            "Hypothesis testing involves specifying a null hypothesis H₀, computing a test statistic, and evaluating the p-value. "
            "The p-value is the probability of observing data as extreme as, or more extreme than, the observed, under H₀. "
            "A significance level α is chosen to control the Type I error rate."
        ),
        key_factors=[
            "Null and alternative hypotheses",
            "Test statistic",
            "Significance level",
            "Type I and II errors"
        ],
        primary_authority=[
            "Jerzy Neyman, Egon Pearson, 1933"
        ],
        burden_holder="Proponent of test validity",
        adversary_position="Test is invalid or p-value is misinterpreted",
        counter_arguments=[
            "Test statistic may not follow assumed distribution.",
            "Multiple comparisons may inflate error rates.",
            "P-value may be misinterpreted."
        ],
        resolution_strategy="Check assumptions and control error rates.",
        entity_scope="Statistical inference",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Neyman-Pearson Testing Theory"
    ),
    DoctrineBlock(
        topic="p-Value",
        keywords=["p-value", "significance", "hypothesis testing", "Type I error"],
        conclusion_template="The p-value is the probability, under the null, of observing data as extreme as the observed.",
        reasoning_framework=(
            "The p-value quantifies the evidence against the null hypothesis. "
            "It is the probability, under H₀, of observing a test statistic at least as extreme as the one observed. "
            "A small p-value suggests evidence against H₀, but does not measure the probability that H₀ is true."
        ),
        key_factors=[
            "Null hypothesis",
            "Test statistic distribution",
            "Significance threshold",
            "Interpretation"
        ],
        primary_authority=[
            "Ronald Fisher, 1925"
        ],
        burden_holder="Proponent of p-value interpretation",
        adversary_position="p-value is misinterpreted or misapplied",
        counter_arguments=[
            "p-value is not the probability H₀ is true.",
            "Multiple testing inflates false positives.",
            "Thresholds are arbitrary."
        ],
        resolution_strategy="Clarify interpretation; adjust for multiple comparisons.",
        entity_scope="Statistical hypothesis testing",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Fisher's p-value Concept"
    ),
    DoctrineBlock(
        topic="Type I and Type II Errors",
        keywords=["Type I error", "Type II error", "false positive", "false negative", "power"],
        conclusion_template="Type I error is rejecting a true null; Type II is failing to reject a false null.",
        reasoning_framework=(
            "Type I error (α) is the probability of incorrectly rejecting the null hypothesis when it is true. "
            "Type II error (β) is the probability of failing to reject the null when it is false. "
            "Power is 1-β, the probability of correctly rejecting a false null. "
            "Balancing these errors is central to hypothesis testing."
        ),
        key_factors=[
            "Significance level",
            "Power",
            "Sample size",
            "Effect size"
        ],
        primary_authority=[
            "Jerzy Neyman, Egon Pearson, 1933"
        ],
        burden_holder="Proponent of error rate control",
        adversary_position="Error rates are not controlled or are misinterpreted",
        counter_arguments=[
            "Sample size may be inadequate.",
            "Effect size may be small.",
            "Multiple testing may inflate errors."
        ],
        resolution_strategy="Adjust sample size; control error rates.",
        entity_scope="Statistical hypothesis testing",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Neyman-Pearson Theory"
    ),
    DoctrineBlock(
        topic="Likelihood Ratio Test",
        keywords=["likelihood ratio", "hypothesis test", "test statistic", "Neyman-Pearson lemma"],
        conclusion_template="The likelihood ratio test compares the likelihoods under null and alternative hypotheses.",
        reasoning_framework=(
            "The likelihood ratio test (LRT) uses the ratio of maximum likelihoods under the null and alternative hypotheses as a test statistic. "
            "The Neyman-Pearson lemma shows that the LRT is the most powerful test for simple hypotheses. "
            "Critical values are determined by the distribution of the test statistic under the null."
        ),
        key_factors=[
            "Likelihood functions",
            "Null and alternative hypotheses",
            "Test statistic distribution",
            "Power"
        ],
        primary_authority=[
            "Jerzy Neyman, Egon Pearson, 1933"
        ],
        burden_holder="Proponent of LRT",
        adversary_position="LRT is not most powerful or is misapplied",
        counter_arguments=[
            "Composite hypotheses may complicate analysis.",
            "Distribution of statistic may be unknown.",
            "Assumptions may fail."
        ],
        resolution_strategy="Check assumptions and use asymptotic results if needed.",
        entity_scope="Statistical hypothesis testing",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Neyman-Pearson Lemma"
    ),
    DoctrineBlock(
        topic="Bootstrap",
        keywords=["bootstrap", "resampling", "confidence interval", "nonparametric"],
        conclusion_template="The bootstrap estimates sampling distributions by resampling with replacement from the data.",
        reasoning_framework=(
            "The bootstrap is a computational method for estimating the sampling distribution of a statistic by resampling with replacement from the observed data. "
            "It allows for the construction of confidence intervals and hypothesis tests without strong parametric assumptions. "
            "The method is widely used in modern statistics."
        ),
        key_factors=[
            "Resampling",
            "Sample size",
            "Statistic of interest",
            "Computational resources"
        ],
        primary_authority=[
            "Bradley Efron, 1979"
        ],
        burden_holder="Proponent of bootstrap method",
        adversary_position="Bootstrap estimates are biased or inconsistent",
        counter_arguments=[
            "Small sample sizes may limit accuracy.",
            "Dependence in data may violate assumptions.",
            "Computational cost may be high."
        ],
        resolution_strategy="Increase sample size; check assumptions; use computational power.",
        entity_scope="Statistical inference",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Efron's Bootstrap"
    ),
    DoctrineBlock(
        topic="Permutation Test",
        keywords=["permutation test", "randomization", "nonparametric", "hypothesis testing"],
        conclusion_template="Permutation tests assess significance by comparing observed statistics to those from randomly permuted data.",
        reasoning_framework=(
            "Permutation tests are nonparametric methods for testing hypotheses by comparing the observed test statistic to its distribution under random permutations of the data labels. "
            "They do not rely on parametric assumptions and are exact when all permutations are considered."
        ),
        key_factors=[
            "Randomization",
            "Test statistic",
            "Permutation distribution",
            "Sample size"
        ],
        primary_authority=[
            "Ronald Fisher, 1935"
        ],
        burden_holder="Proponent of permutation test",
        adversary_position="Permutation test is not valid or is computationally infeasible",
        counter_arguments=[
            "Sample size may be too large for all permutations.",
            "Test statistic may not be appropriate.",
            "Randomization may not be justified."
        ],
        resolution_strategy="Use Monte Carlo approximation for large samples; check test statistic.",
        entity_scope="Statistical hypothesis testing",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Fisher's Randomization Test"
    ),
    DoctrineBlock(
        topic="Monte Carlo Method",
        keywords=["Monte Carlo", "simulation", "random sampling", "approximation"],
        conclusion_template="Monte Carlo methods approximate quantities by random sampling and averaging.",
        reasoning_framework=(
            "Monte Carlo methods use random sampling to approximate integrals, probabilities, and other quantities. "
            "They are widely used when analytical solutions are intractable. "
            "Accuracy improves with the number of samples by the law of large numbers."
        ),
        key_factors=[
            "Random sampling",
            "Sample size",
            "Variance reduction",
            "Computational resources"
        ],
        primary_authority=[
            "Stanislaw Ulam, John von Neumann, 1940s"
        ],
        burden_holder="Proponent of Monte Carlo estimate",
        adversary_position="Estimates are inaccurate or computationally expensive",
        counter_arguments=[
            "Variance may be high.",
            "Sample size may be insufficient.",
            "Random number generation may be flawed."
        ],
        resolution_strategy="Increase sample size; use variance reduction techniques.",
        entity_scope="Numerical approximation",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Monte Carlo Method"
    ),
    DoctrineBlock(
        topic="Markov Chain",
        keywords=["Markov chain", "transition probability", "memoryless", "stochastic process"],
        conclusion_template="A Markov chain is a process where the future state depends only on the present state.",
        reasoning_framework=(
            "A Markov chain is a stochastic process with the Markov property: P(Xₙ₊₁=x|Xₙ, ..., X₀) = P(Xₙ₊₁=x|Xₙ). "
            "Transition probabilities define the dynamics. "
            "Markov chains are used in modeling, simulation, and statistical inference."
        ),
        key_factors=[
            "Markov property",
            "Transition matrix",
            "State space",
            "Stationarity"
        ],
        primary_authority=[
            "A.A. Markov, 1906"
        ],
        burden_holder="Proponent of Markov property",
        adversary_position="Process is not Markovian",
        counter_arguments=[
            "Dependence on past states may exist.",
            "Transition probabilities may be misdefined.",
            "State space may be infinite."
        ],
        resolution_strategy="Test Markov property; check transition matrix.",
        entity_scope="Stochastic processes",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Markov's Theory"
    ),
    DoctrineBlock(
        topic="Stationary Distribution",
        keywords=["stationary distribution", "Markov chain", "equilibrium", "long-run behavior"],
        conclusion_template="A stationary distribution π satisfies πP = π for the transition matrix P.",
        reasoning_framework=(
            "A stationary distribution for a Markov chain is a probability vector π such that πP = π, where P is the transition matrix. "
            "If the chain is irreducible and aperiodic, it converges to π regardless of the initial state."
        ),
        key_factors=[
            "Transition matrix",
            "Irreducibility",
            "Aperiodicity",
            "Convergence"
        ],
        primary_authority=[
            "A.A. Markov, 1906",
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of stationary distribution",
        adversary_position="Stationary distribution does not exist or is not unique",
        counter_arguments=[
            "Chain may not be irreducible.",
            "Chain may be periodic.",
            "Transition matrix may be misdefined."
        ],
        resolution_strategy="Check irreducibility and aperiodicity.",
        entity_scope="Markov chains",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Markov's Theory"
    ),
    DoctrineBlock(
        topic="Ergodicity of Markov Chains",
        keywords=["ergodicity", "Markov chain", "long-run average", "convergence"],
        conclusion_template="An ergodic Markov chain converges to a unique stationary distribution.",
        reasoning_framework=(
            "A Markov chain is ergodic if it is irreducible, aperiodic, and positive recurrent. "
            "Such chains converge in distribution to a unique stationary distribution, regardless of the initial state. "
            "Ergodicity ensures long-run averages converge to expected values under the stationary distribution."
        ),
        key_factors=[
            "Irreducibility",
            "Aperiodicity",
            "Positive recurrence",
            "Convergence"
        ],
        primary_authority=[
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of ergodicity",
        adversary_position="Chain is not ergodic or does not converge",
        counter_arguments=[
            "Chain may not be irreducible or aperiodic.",
            "Recurrence may fail.",
            "Transition matrix may be misdefined."
        ],
        resolution_strategy="Check all ergodicity conditions.",
        entity_scope="Markov chains",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Feller's Theory"
    ),
    DoctrineBlock(
        topic="Detailed Balance",
        keywords=["detailed balance", "reversibility", "Markov chain", "stationary distribution"],
        conclusion_template="A Markov chain satisfies detailed balance if π_i P_{ij} = π_j P_{ji} for all states i, j.",
        reasoning_framework=(
            "Detailed balance is a sufficient condition for a stationary distribution in reversible Markov chains. "
            "If π_i P_{ij} = π_j P_{ji} for all i, j, then π is stationary. "
            "Detailed balance is used in Markov Chain Monte Carlo methods."
        ),
        key_factors=[
            "Transition matrix",
            "Stationary distribution",
            "Reversibility",
            "Balance equations"
        ],
        primary_authority=[
            "William Feller, Probability Theory"
        ],
        burden_holder="Proponent of detailed balance",
        adversary_position="Chain does not satisfy detailed balance",
        counter_arguments=[
            "Transition matrix may not be reversible.",
            "Stationary distribution may not exist.",
            "Equations may not be satisfied."
        ],
        resolution_strategy="Check detailed balance equations.",
        entity_scope="Markov chains",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Feller's Theory"
    ),
    DoctrineBlock(
        topic="Markov Chain Monte Carlo",
        keywords=["MCMC", "Markov chain", "Monte Carlo", "sampling", "stationary distribution"],
        conclusion_template="MCMC uses Markov chains to sample from complex distributions via their stationary distribution.",
        reasoning_framework=(
            "Markov Chain Monte Carlo (MCMC) methods construct a Markov chain whose stationary distribution is the target distribution. "
            "Samples from the chain are used to approximate expectations and probabilities. "
            "MCMC is widely used in Bayesian inference and computational statistics."
        ),
        key_factors=[
            "Markov chain construction",
            "Stationary distribution",
            "Convergence diagnostics",
            "Mixing"
        ],
        primary_authority=[
            "W.K. Hastings, 1970",
            "S. Geman, D. Geman, 1984"
        ],
        burden_holder="Proponent of MCMC method",
        adversary_position="Chain does not converge or samples are not representative",
        counter_arguments=[
            "Chain may mix slowly.",
            "Convergence diagnostics may be inadequate.",
            "Stationary distribution may not be correct."
        ],
        resolution_strategy="Use diagnostics; tune chain parameters.",
        entity_scope="Computational statistics",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Hastings, Geman & Geman"
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