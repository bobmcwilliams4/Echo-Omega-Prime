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
        topic="Bayesian Confidence Aggregation",
        keywords=["Bayesian", "confidence", "aggregation", "posterior", "prior", "probability"],
        conclusion_template="Aggregate confidence scores using Bayesian inference, updating prior beliefs with observed evidence.",
        reasoning_framework=(
            "Bayesian aggregation combines prior probabilities with observed likelihoods from multiple engines. "
            "Each engine's confidence score is treated as evidence, and the prior belief about the system's reliability "
            "is updated using Bayes' theorem. The posterior probability reflects the aggregated confidence, accounting "
            "for both the initial assumptions and the observed data. This method assumes conditional independence among "
            "engines unless correlation is explicitly modeled. The process involves specifying prior distributions, "
            "calculating likelihoods based on engine outputs, and normalizing the resulting posterior. The approach is "
            "robust to varying engine reliabilities and can incorporate expert knowledge through priors. Sensitivity "
            "analysis is recommended to assess the impact of prior selection. Bayesian model averaging can be applied "
            "when multiple plausible models exist. The final aggregated confidence is interpreted as the probability of "
            "correctness given all available evidence."
        ),
        key_factors=[
            "Choice of prior distribution",
            "Engine independence assumptions",
            "Quality of likelihood estimation",
            "Handling of conflicting evidence",
            "Sensitivity to outliers"
        ],
        primary_authority=[
            "Gelman et al., Bayesian Data Analysis (2013)",
            "Pearl, Probabilistic Reasoning in Intelligent Systems (1988)"
        ],
        burden_holder="Aggregator system designer",
        adversary_position="Bayesian methods are sensitive to prior selection and may not handle correlated errors well.",
        counter_arguments=[
            "Empirical priors can be estimated from historical data.",
            "Hierarchical Bayesian models can address correlation.",
            "Robustness checks mitigate prior sensitivity."
        ],
        resolution_strategy="Employ empirical Bayes or hierarchical models; validate with cross-validation.",
        entity_scope="All engine outputs subject to aggregation.",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="Gelman et al., Bayesian Data Analysis (2013)"
    ),
    DoctrineBlock(
        topic="Weighted Scoring by Engine Reliability",
        keywords=["weighted scoring", "engine reliability", "aggregation", "confidence weighting"],
        conclusion_template="Aggregate scores by assigning weights proportional to each engine's demonstrated reliability.",
        reasoning_framework=(
            "Weighted scoring assigns higher influence to engines with superior historical performance. "
            "Reliability metrics (e.g., accuracy, calibration, Brier score) are computed for each engine using validation data. "
            "Weights are normalized to sum to one and applied to the confidence scores before aggregation. "
            "This approach reduces the impact of unreliable engines and enhances the robustness of the final confidence estimate. "
            "Dynamic weighting schemes can adapt to changing engine performance over time. The method assumes that past reliability "
            "is indicative of future performance, which should be periodically validated. Outlier detection can be incorporated to "
            "down-weight anomalous engines. The final aggregated score is a convex combination of individual engine confidences."
        ),
        key_factors=[
            "Accurate reliability estimation",
            "Appropriate normalization of weights",
            "Temporal stability of engine performance",
            "Detection and handling of outliers"
        ],
        primary_authority=[
            "Kuncheva, Combining Pattern Classifiers (2004)",
            "Dietterich, Ensemble Methods in Machine Learning (2000)"
        ],
        burden_holder="System integrator",
        adversary_position="Reliability estimates may be outdated or based on insufficient data.",
        counter_arguments=[
            "Use rolling windows for reliability estimation.",
            "Bootstrap methods can quantify uncertainty in reliability.",
            "Regular recalibration ensures up-to-date weights."
        ],
        resolution_strategy="Periodically update reliability metrics; apply bootstrapping for uncertainty estimation.",
        entity_scope="All engines with available reliability data.",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="Kuncheva, Combining Pattern Classifiers (2004)"
    ),
    DoctrineBlock(
        topic="Inter-Engine Correlation Detection",
        keywords=["correlation", "engine dependence", "redundancy", "aggregation bias"],
        conclusion_template="Detect and adjust for correlations among engines to prevent aggregation bias.",
        reasoning_framework=(
            "Correlation among engine outputs can lead to overconfident aggregate scores if not properly accounted for. "
            "Pairwise and higher-order correlation coefficients (e.g., Pearson, Spearman) are computed across engine outputs. "
            "Significant correlations indicate redundancy or shared failure modes. Aggregation methods are adjusted by either "
            "down-weighting correlated engines or applying decorrelation techniques such as principal component analysis (PCA). "
            "Graph-based models can represent dependency structures. Regular monitoring is necessary as engine correlations may "
            "change over time due to updates or data drift. The goal is to ensure that the aggregate confidence reflects "
            "independent evidence rather than duplicated signals."
        ),
        key_factors=[
            "Magnitude and direction of correlations",
            "Temporal stability of dependencies",
            "Effectiveness of decorrelation methods",
            "Impact on aggregate confidence"
        ],
        primary_authority=[
            "Krogh & Vedelsby, Neural Network Ensembles, Cross Validation, and Active Learning (1995)",
            "Dietterich, Ensemble Methods in Machine Learning (2000)"
        ],
        burden_holder="Aggregator system analyst",
        adversary_position="Correlation detection may be computationally intensive and sensitive to sample size.",
        counter_arguments=[
            "Efficient algorithms exist for large-scale correlation analysis.",
            "Regularization can mitigate overfitting in decorrelation.",
            "Subsampling can reduce computational burden."
        ],
        resolution_strategy="Implement scalable correlation analysis; apply regularization and decorrelation as needed.",
        entity_scope="All engine pairs and groups.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Krogh & Vedelsby, Neural Network Ensembles (1995)"
    ),
    DoctrineBlock(
        topic="Confidence Calibration Methods",
        keywords=["calibration", "confidence", "probability", "Platt scaling", "isotonic regression"],
        conclusion_template="Apply calibration techniques to align engine confidence scores with true probabilities.",
        reasoning_framework=(
            "Calibration ensures that reported confidence scores correspond to actual probabilities of correctness. "
            "Common methods include Platt scaling (logistic regression), isotonic regression, and temperature scaling. "
            "Calibration curves (reliability diagrams) are used to assess and visualize calibration quality. "
            "Engines are calibrated on held-out validation data, and calibration parameters are periodically updated. "
            "Poorly calibrated engines can distort aggregate confidence, so recalibration is essential after major model updates. "
            "Ensemble calibration can be performed post-aggregation to correct for residual miscalibration."
        ),
        key_factors=[
            "Quality and representativeness of calibration data",
            "Choice of calibration method",
            "Frequency of recalibration",
            "Impact on aggregate confidence"
        ],
        primary_authority=[
            "Guo et al., On Calibration of Modern Neural Networks (2017)",
            "Niculescu-Mizil & Caruana, Predicting Good Probabilities with Supervised Learning (2005)"
        ],
        burden_holder="Model developer",
        adversary_position="Calibration may degrade discrimination or require large validation sets.",
        counter_arguments=[
            "Cross-validation can maximize data usage.",
            "Calibration and discrimination can be jointly optimized.",
            "Ensemble calibration methods are available."
        ],
        resolution_strategy="Use cross-validation for calibration; monitor discrimination and recalibrate as needed.",
        entity_scope="All engines reporting confidence scores.",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="Guo et al., On Calibration of Modern Neural Networks (2017)"
    ),
    DoctrineBlock(
        topic="Bootstrap Uncertainty Estimation",
        keywords=["bootstrap", "uncertainty", "confidence interval", "resampling"],
        conclusion_template="Estimate uncertainty in aggregated confidence using bootstrap resampling.",
        reasoning_framework=(
            "Bootstrap methods involve repeatedly resampling the available data with replacement to generate multiple pseudo-datasets. "
            "Aggregation is performed on each resampled set, yielding a distribution of aggregate confidence scores. "
            "Confidence intervals are constructed from the quantiles of this distribution, providing an empirical measure of uncertainty. "
            "This approach is non-parametric and does not assume normality. The number of bootstrap samples should be sufficient to ensure "
            "stability of the interval estimates. Bootstrap can be combined with other aggregation methods to quantify their uncertainty."
        ),
        key_factors=[
            "Number of bootstrap samples",
            "Representativeness of original data",
            "Stability of interval estimates",
            "Computational resources"
        ],
        primary_authority=[
            "Efron & Tibshirani, An Introduction to the Bootstrap (1993)"
        ],
        burden_holder="Aggregator analyst",
        adversary_position="Bootstrap may underestimate uncertainty with small or biased samples.",
        counter_arguments=[
            "Bias-corrected and accelerated (BCa) intervals improve accuracy.",
            "Stratified bootstrap can address sample imbalance.",
            "Increase sample size where possible."
        ],
        resolution_strategy="Use BCa intervals; validate bootstrap assumptions; increase sample size if needed.",
        entity_scope="Aggregated confidence estimates.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Efron & Tibshirani, An Introduction to the Bootstrap (1993)"
    ),
    DoctrineBlock(
        topic="Score Normalization",
        keywords=["normalization", "score scaling", "min-max", "z-score", "standardization"],
        conclusion_template="Normalize confidence scores to a common scale before aggregation.",
        reasoning_framework=(
            "Engines may output confidence scores on different scales or distributions. Normalization ensures comparability. "
            "Common techniques include min-max scaling (rescaling to [0,1]), z-score normalization (standardizing to zero mean and unit variance), "
            "and rank-based normalization. The choice of method depends on the underlying score distributions and aggregation requirements. "
            "Normalization parameters should be computed on representative data and periodically updated. Care must be taken to avoid information loss "
            "or distortion, especially with non-linear transformations. Post-aggregation normalization may also be applied to the final score."
        ),
        key_factors=[
            "Score distribution characteristics",
            "Choice of normalization method",
            "Frequency of parameter updates",
            "Impact on interpretability"
        ],
        primary_authority=[
            "Han et al., Data Mining: Concepts and Techniques (2011)"
        ],
        burden_holder="System integrator",
        adversary_position="Improper normalization can distort scores and reduce interpretability.",
        counter_arguments=[
            "Visualize score distributions before and after normalization.",
            "Select normalization method based on empirical analysis.",
            "Document normalization parameters for transparency."
        ],
        resolution_strategy="Empirically evaluate normalization impact; document and review normalization choices.",
        entity_scope="All engine confidence scores.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Han et al., Data Mining: Concepts and Techniques (2011)"
    ),
    DoctrineBlock(
        topic="Outlier Detection in Confidence Scores",
        keywords=["outlier detection", "anomaly", "robust aggregation", "score filtering"],
        conclusion_template="Identify and mitigate the influence of outlier confidence scores in aggregation.",
        reasoning_framework=(
            "Outlier detection aims to identify engine outputs that are inconsistent with the majority. "
            "Techniques include statistical tests (e.g., Grubbs', Dixon's), robust estimators (e.g., median, trimmed mean), "
            "and machine learning-based anomaly detection. Outliers may result from engine failures, data corruption, or adversarial attacks. "
            "Detected outliers can be down-weighted, excluded, or flagged for further review. The threshold for outlier detection should be "
            "tuned to balance sensitivity and specificity. Robust aggregation methods (e.g., Huber loss, M-estimators) can further mitigate outlier impact."
        ),
        key_factors=[
            "Choice of outlier detection method",
            "Threshold calibration",
            "Impact on aggregate confidence",
            "Handling of flagged outliers"
        ],
        primary_authority=[
            "Hampel et al., Robust Statistics (1986)",
            "Chandola et al., Anomaly Detection: A Survey (2009)"
        ],
        burden_holder="Aggregator analyst",
        adversary_position="Overzealous outlier filtering may discard valuable signals.",
        counter_arguments=[
            "Combine statistical and domain-based criteria.",
            "Review flagged outliers before exclusion.",
            "Use robust aggregation rather than outright exclusion."
        ],
        resolution_strategy="Adopt robust aggregation; review and document outlier handling decisions.",
        entity_scope="All engine confidence scores.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Hampel et al., Robust Statistics (1986)"
    ),
    DoctrineBlock(
        topic="Ensemble Methods for Confidence Aggregation",
        keywords=["ensemble", "aggregation", "bagging", "boosting", "stacking", "voting"],
        conclusion_template="Employ ensemble methods to combine engine confidence scores for improved reliability.",
        reasoning_framework=(
            "Ensemble methods aggregate predictions from multiple engines to improve accuracy and robustness. "
            "Bagging (bootstrap aggregating) reduces variance by averaging over resampled datasets. Boosting focuses on difficult cases by reweighting. "
            "Stacking combines engine outputs using a meta-model, which learns optimal aggregation weights. Voting (majority or weighted) is used for discrete decisions. "
            "The choice of ensemble method depends on engine diversity, independence, and the nature of the confidence scores. Ensembles can mitigate individual engine weaknesses "
            "and provide more stable aggregate confidence estimates. Proper validation is required to avoid overfitting."
        ),
        key_factors=[
            "Engine diversity",
            "Appropriate ensemble method selection",
            "Meta-model validation",
            "Risk of overfitting"
        ],
        primary_authority=[
            "Dietterich, Ensemble Methods in Machine Learning (2000)",
            "Opitz & Maclin, Popular Ensemble Methods: An Empirical Study (1999)"
        ],
        burden_holder="System architect",
        adversary_position="Ensembles may increase complexity and computational cost.",
        counter_arguments=[
            "Parallelization can mitigate computational overhead.",
            "Ensemble size can be tuned for efficiency.",
            "Complexity is justified by improved reliability."
        ],
        resolution_strategy="Optimize ensemble size; use parallel processing; validate ensemble performance.",
        entity_scope="All engines eligible for aggregation.",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Dietterich, Ensemble Methods in Machine Learning (2000)"
    ),
    DoctrineBlock(
        topic="Reliability Weighting in Score Fusion",
        keywords=["reliability weighting", "score fusion", "aggregation", "dynamic weighting"],
        conclusion_template="Fuse scores using weights dynamically adjusted based on real-time reliability metrics.",
        reasoning_framework=(
            "Reliability weighting extends static weighted scoring by updating weights in real time based on current engine performance. "
            "Metrics such as recent accuracy, calibration, and agreement with other engines are monitored. Weights are adjusted to reflect "
            "the most reliable engines at each aggregation instance. This approach adapts to changing conditions and engine drift. "
            "Automated monitoring and feedback loops are essential for timely updates. Dynamic weighting can be combined with ensemble methods "
            "for further robustness. Care must be taken to avoid instability due to rapid weight fluctuations."
        ),
        key_factors=[
            "Timeliness and accuracy of reliability metrics",
            "Stability of weight updates",
            "Integration with aggregation logic",
            "Monitoring for drift"
        ],
        primary_authority=[
            "Kuncheva, Combining Pattern Classifiers (2004)",
            "Polikar, Ensemble Based Systems in Decision Making (2006)"
        ],
        burden_holder="System operator",
        adversary_position="Frequent weight changes may introduce instability or oscillation.",
        counter_arguments=[
            "Apply smoothing or momentum to weight updates.",
            "Set minimum and maximum weight thresholds.",
            "Monitor for excessive volatility."
        ],
        resolution_strategy="Implement smoothing; monitor weight stability; adjust update frequency as needed.",
        entity_scope="All engines with real-time reliability data.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Kuncheva, Combining Pattern Classifiers (2004)"
    ),
    DoctrineBlock(
        topic="Score Fusion Techniques",
        keywords=["score fusion", "aggregation", "linear fusion", "nonlinear fusion", "combination rules"],
        conclusion_template="Combine confidence scores using appropriate fusion techniques tailored to score characteristics.",
        reasoning_framework=(
            "Score fusion involves combining multiple confidence scores into a single aggregate value. "
            "Linear fusion methods (e.g., weighted average, sum rule) are simple and interpretable. Nonlinear fusion (e.g., product rule, max/min rule) "
            "can capture interactions among scores. The choice of fusion technique depends on the distribution, scale, and independence of scores. "
            "Fusion rules should be validated empirically to ensure they improve aggregate reliability. Hybrid fusion methods can combine linear and nonlinear approaches."
        ),
        key_factors=[
            "Score distribution and scale",
            "Independence assumptions",
            "Empirical validation of fusion rule",
            "Interpretability"
        ],
        primary_authority=[
            "Kittler et al., On Combining Classifiers (1998)",
            "Kuncheva, Combining Pattern Classifiers (2004)"
        ],
        burden_holder="Aggregator designer",
        adversary_position="Inappropriate fusion rules can degrade performance.",
        counter_arguments=[
            "Empirical testing can identify optimal fusion rules.",
            "Hybrid methods can mitigate weaknesses of individual rules.",
            "Fusion rule selection should be data-driven."
        ],
        resolution_strategy="Test multiple fusion techniques; select based on empirical performance.",
        entity_scope="All confidence scores to be aggregated.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Kittler et al., On Combining Classifiers (1998)"
    ),
    DoctrineBlock(
        topic="Disagreement Quantification",
        keywords=["disagreement", "diversity", "variance", "engine conflict", "uncertainty"],
        conclusion_template="Quantify and report disagreement among engine confidence scores as a measure of uncertainty.",
        reasoning_framework=(
            "Disagreement among engines provides valuable information about uncertainty and potential failure modes. "
            "Metrics such as variance, entropy, and pairwise disagreement rates are computed across engine outputs. "
            "High disagreement may indicate ambiguous cases, data drift, or adversarial interference. Disagreement metrics "
            "are reported alongside aggregate confidence to inform downstream decision-making. Aggregation methods can be "
            "adjusted to account for disagreement, such as by reducing aggregate confidence or invoking human review."
        ),
        key_factors=[
            "Choice of disagreement metric",
            "Thresholds for actionable disagreement",
            "Interpretation of disagreement signals",
            "Integration with aggregation logic"
        ],
        primary_authority=[
            "Kuncheva & Whitaker, Measures of Diversity in Classifier Ensembles (2003)",
            "Krogh & Vedelsby, Neural Network Ensembles (1995)"
        ],
        burden_holder="System analyst",
        adversary_position="Disagreement may be misinterpreted or overemphasized.",
        counter_arguments=[
            "Combine disagreement with other uncertainty measures.",
            "Provide clear guidelines for interpreting disagreement.",
            "Use disagreement to trigger additional validation."
        ],
        resolution_strategy="Integrate disagreement metrics into uncertainty reporting; educate users on interpretation.",
        entity_scope="All engine outputs.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Kuncheva & Whitaker, Measures of Diversity in Classifier Ensembles (2003)"
    ),
    DoctrineBlock(
        topic="Dempster-Shafer Evidence Theory",
        keywords=["Dempster-Shafer", "evidence theory", "belief function", "uncertainty", "aggregation"],
        conclusion_template="Aggregate confidence using Dempster-Shafer theory to model and combine evidence with uncertainty.",
        reasoning_framework=(
            "Dempster-Shafer theory provides a framework for combining evidence from multiple sources, allowing for explicit modeling of uncertainty. "
            "Each engine's output is represented as a belief function over possible outcomes. Dempster's rule of combination is used to fuse these belief functions, "
            "accounting for both supporting and conflicting evidence. The resulting belief and plausibility intervals quantify the range of confidence. "
            "This approach is particularly useful when evidence is incomplete or ambiguous. Conflict resolution strategies are applied when evidence sources strongly disagree."
        ),
        key_factors=[
            "Construction of belief functions",
            "Handling of conflicting evidence",
            "Interpretation of belief and plausibility",
            "Computational complexity"
        ],
        primary_authority=[
            "Shafer, A Mathematical Theory of Evidence (1976)",
            "Yager & Liu, Classic Works of the Dempster-Shafer Theory of Belief Functions (2008)"
        ],
        burden_holder="Aggregator designer",
        adversary_position="Dempster-Shafer can be computationally intensive and difficult to interpret.",
        counter_arguments=[
            "Approximate algorithms reduce computational burden.",
            "Visualization aids can clarify belief intervals.",
            "Hybrid approaches can combine Dempster-Shafer with Bayesian methods."
        ],
        resolution_strategy="Use approximate combination methods; provide interpretive aids for users.",
        entity_scope="All engines with evidence-based outputs.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Shafer, A Mathematical Theory of Evidence (1976)"
    ),
    DoctrineBlock(
        topic="Confidence Interval Construction",
        keywords=["confidence interval", "uncertainty", "interval estimation", "bootstrap", "Bayesian credible interval"],
        conclusion_template="Construct and report confidence intervals for aggregated confidence estimates.",
        reasoning_framework=(
            "Confidence intervals provide a range within which the true aggregate confidence is expected to lie with a specified probability. "
            "Intervals can be constructed using parametric methods (e.g., normal approximation), non-parametric bootstrap, or Bayesian credible intervals. "
            "The choice of method depends on the distributional assumptions and available data. Intervals should be reported alongside point estimates "
            "to convey uncertainty. Coverage probability should be validated empirically. Interval width can inform decision thresholds and risk management."
        ),
        key_factors=[
            "Appropriateness of interval estimation method",
            "Coverage probability validation",
            "Interpretability of intervals",
            "Integration with reporting"
        ],
        primary_authority=[
            "Efron & Tibshirani, An Introduction to the Bootstrap (1993)",
            "Gelman et al., Bayesian Data Analysis (2013)"
        ],
        burden_holder="Aggregator analyst",
        adversary_position="Intervals may be misinterpreted or based on invalid assumptions.",
        counter_arguments=[
            "Provide clear interpretation guidelines.",
            "Validate interval coverage on held-out data.",
            "Use non-parametric methods when in doubt."
        ],
        resolution_strategy="Empirically validate intervals; educate users on interpretation.",
        entity_scope="Aggregated confidence estimates.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Efron & Tibshirani, An Introduction to the Bootstrap (1993)"
    ),
    DoctrineBlock(
        topic="Monte Carlo Confidence Estimation",
        keywords=["Monte Carlo", "simulation", "confidence estimation", "uncertainty quantification"],
        conclusion_template="Estimate aggregate confidence and uncertainty using Monte Carlo simulation.",
        reasoning_framework=(
            "Monte Carlo methods simulate the aggregation process by repeatedly sampling from the distributions of engine outputs. "
            "The resulting distribution of aggregate confidence scores provides empirical estimates of mean, variance, and higher moments. "
            "This approach is flexible and can accommodate complex dependencies and non-linear aggregation rules. The number of simulations "
            "should be sufficient to ensure stable estimates. Monte Carlo can be combined with Bayesian or bootstrap methods for comprehensive uncertainty quantification."
        ),
        key_factors=[
            "Number of simulation runs",
            "Quality of input distributions",
            "Computational resources",
            "Interpretation of simulation results"
        ],
        primary_authority=[
            "Robert & Casella, Monte Carlo Statistical Methods (2004)"
        ],
        burden_holder="System analyst",
        adversary_position="Monte Carlo can be computationally expensive and sensitive to input assumptions.",
        counter_arguments=[
            "Parallelization can accelerate simulations.",
            "Sensitivity analysis can assess input robustness.",
            "Variance reduction techniques improve efficiency."
        ],
        resolution_strategy="Optimize simulation parameters; validate input distributions; use parallel processing.",
        entity_scope="Aggregated confidence estimation.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Robert & Casella, Monte Carlo Statistical Methods (2004)"
    ),
    DoctrineBlock(
        topic="Calibration Curve Analysis",
        keywords=["calibration curve", "reliability diagram", "calibration assessment", "probability calibration"],
        conclusion_template="Use calibration curves to assess and improve the alignment of confidence scores with true outcomes.",
        reasoning_framework=(
            "Calibration curves (reliability diagrams) plot predicted confidence against observed frequencies of correctness. "
            "Deviations from the diagonal indicate miscalibration. The analysis identifies systematic over- or under-confidence, "
            "guiding recalibration efforts. Binning strategies and smoothing can improve curve stability. Calibration metrics such as "
            "expected calibration error (ECE) and maximum calibration error (MCE) quantify miscalibration. Regular calibration curve analysis "
            "is recommended after model updates or data distribution shifts."
        ),
        key_factors=[
            "Choice of binning and smoothing methods",
            "Sample size for stable estimates",
            "Interpretation of calibration metrics",
            "Frequency of calibration assessment"
        ],
        primary_authority=[
            "Niculescu-Mizil & Caruana, Predicting Good Probabilities with Supervised Learning (2005)",
            "Guo et al., On Calibration of Modern Neural Networks (2017)"
        ],
        burden_holder="Model developer",
        adversary_position="Small sample sizes can yield noisy calibration curves.",
        counter_arguments=[
            "Aggregate calibration curves across multiple runs.",
            "Use adaptive binning for better resolution.",
            "Report confidence intervals on calibration metrics."
        ],
        resolution_strategy="Use adaptive binning; report uncertainty in calibration metrics.",
        entity_scope="All engines with probabilistic outputs.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Niculescu-Mizil & Caruana, Predicting Good Probabilities (2005)"
    ),
    DoctrineBlock(
        topic="Brier Score Evaluation",
        keywords=["Brier score", "calibration", "accuracy", "probability scoring", "evaluation"],
        conclusion_template="Evaluate and compare engine confidence scores using the Brier score.",
        reasoning_framework=(
            "The Brier score measures the mean squared difference between predicted probabilities and actual outcomes. "
            "Lower Brier scores indicate better calibrated and more accurate confidence estimates. The score can be decomposed "
            "into reliability, resolution, and uncertainty components for detailed analysis. Brier scores are computed on held-out "
            "validation sets and used to compare engines and aggregation methods. Regular monitoring is recommended to detect calibration drift."
        ),
        key_factors=[
            "Availability of ground truth labels",
            "Appropriate decomposition of Brier score",
            "Frequency of evaluation",
            "Interpretation of score components"
        ],
        primary_authority=[
            "Brier, Verification of Forecasts Expressed in Terms of Probability (1950)",
            "Murphy, A New Vector Partition of the Probability Score (1973)"
        ],
        burden_holder="Model evaluator",
        adversary_position="Brier score may not capture all aspects of performance, especially in imbalanced settings.",
        counter_arguments=[
            "Complement Brier score with discrimination metrics (e.g., ROC AUC).",
            "Use stratified evaluation for imbalanced data.",
            "Interpret Brier score in context of application."
        ],
        resolution_strategy="Use Brier score alongside other metrics; stratify evaluation as needed.",
        entity_scope="All engines and aggregated outputs.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Brier, Verification of Forecasts Expressed in Terms of Probability (1950)"
    ),
    DoctrineBlock(
        topic="Log-Loss Scoring",
        keywords=["log-loss", "cross-entropy", "probability scoring", "evaluation", "calibration"],
        conclusion_template="Assess confidence score quality using log-loss (cross-entropy) as an evaluation metric.",
        reasoning_framework=(
            "Log-loss (cross-entropy) penalizes confident but incorrect predictions more heavily than Brier score. "
            "It is widely used for evaluating probabilistic classifiers and aggregated confidence scores. Lower log-loss indicates better calibration and discrimination. "
            "Log-loss is sensitive to extreme probabilities, so calibration is essential. Evaluation should be performed on representative validation data, "
            "and log-loss should be monitored over time to detect performance drift."
        ),
        key_factors=[
            "Availability of ground truth labels",
            "Calibration of confidence scores",
            "Interpretation of log-loss values",
            "Handling of extreme probabilities"
        ],
        primary_authority=[
            "Good, Rational Decisions (1952)",
            "Murphy, A New Vector Partition of the Probability Score (1973)"
        ],
        burden_holder="Model evaluator",
        adversary_position="Log-loss can be dominated by rare but extreme errors.",
        counter_arguments=[
            "Clip probabilities to avoid numerical instability.",
            "Complement log-loss with other metrics.",
            "Interpret log-loss in the context of application."
        ],
        resolution_strategy="Clip extreme probabilities; use log-loss with complementary metrics.",
        entity_scope="All engines and aggregated outputs.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Good, Rational Decisions (1952)"
    ),
    DoctrineBlock(
        topic="Precision-Recall Tradeoff",
        keywords=["precision", "recall", "tradeoff", "thresholding", "evaluation"],
        conclusion_template="Analyze and manage the tradeoff between precision and recall in confidence-based decisions.",
        reasoning_framework=(
            "Precision and recall measure the accuracy of positive predictions and the ability to identify all positives, respectively. "
            "Adjusting the confidence threshold affects this tradeoff. Precision-recall curves visualize performance across thresholds. "
            "The optimal threshold depends on application requirements (e.g., cost of false positives vs. false negatives). "
            "Aggregate confidence scores can be thresholded to balance precision and recall according to operational needs."
        ),
        key_factors=[
            "Application-specific cost of errors",
            "Selection of confidence threshold",
            "Interpretation of precision-recall curves",
            "Monitoring for threshold drift"
        ],
        primary_authority=[
            "Davis & Goadrich, The Relationship Between Precision-Recall and ROC Curves (2006)"
        ],
        burden_holder="System operator",
        adversary_position="Threshold selection may be arbitrary or unstable over time.",
        counter_arguments=[
            "Use validation data to select thresholds.",
            "Monitor and adjust thresholds as data evolves.",
            "Report performance across a range of thresholds."
        ],
        resolution_strategy="Empirically determine thresholds; monitor and adjust as needed.",
        entity_scope="All confidence-based decisions.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Davis & Goadrich, The Relationship Between Precision-Recall and ROC Curves (2006)"
    ),
    DoctrineBlock(
        topic="ROC AUC Aggregation",
        keywords=["ROC AUC", "receiver operating characteristic", "aggregation", "evaluation", "discrimination"],
        conclusion_template="Aggregate and report ROC AUC as a measure of discrimination for confidence scores.",
        reasoning_framework=(
            "ROC AUC (Area Under the Receiver Operating Characteristic Curve) quantifies the ability of confidence scores to discriminate between classes. "
            "Aggregate ROC AUC can be computed for individual engines and for the aggregated output. High ROC AUC indicates strong discrimination. "
            "ROC curves and AUC values should be monitored over time to detect performance drift. Stratified analysis can reveal performance across subgroups."
        ),
        key_factors=[
            "Availability of ground truth labels",
            "Interpretation of ROC AUC values",
            "Stratification by subgroup",
            "Monitoring for drift"
        ],
        primary_authority=[
            "Fawcett, An Introduction to ROC Analysis (2006)"
        ],
        burden_holder="Model evaluator",
        adversary_position="ROC AUC may mask poor performance in imbalanced datasets.",
        counter_arguments=[
            "Complement ROC AUC with precision-recall analysis.",
            "Stratify ROC AUC by relevant subgroups.",
            "Interpret ROC AUC in context."
        ],
        resolution_strategy="Use ROC AUC with complementary metrics; stratify analysis as needed.",
        entity_scope="All engines and aggregated outputs.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Fawcett, An Introduction to ROC Analysis (2006)"
    ),
    DoctrineBlock(
        topic="Confidence Decay Over Time",
        keywords=["confidence decay", "temporal drift", "aging", "time-dependent confidence"],
        conclusion_template="Adjust confidence scores to account for temporal decay and data drift.",
        reasoning_framework=(
            "Confidence in predictions may decrease over time due to data drift, model aging, or changing environments. "
            "Decay functions (e.g., exponential, linear) are applied to confidence scores based on the age of the underlying data or model. "
            "Periodic retraining and recalibration are recommended to counteract decay. Monitoring for concept drift and updating decay parameters "
            "ensures that confidence scores remain reliable. Decay-adjusted confidence can trigger alerts for model retraining or human review."
        ),
        key_factors=[
            "Choice of decay function",
            "Frequency of retraining and recalibration",
            "Detection of data and concept drift",
            "Integration with alerting systems"
        ],
        primary_authority=[
            "Gama et al., A Survey on Concept Drift Adaptation (2014)"
        ],
        burden_holder="System operator",
        adversary_position="Decay functions may be arbitrary or misaligned with real drift.",
        counter_arguments=[
            "Empirically estimate decay rates from performance data.",
            "Monitor for drift and adjust decay dynamically.",
            "Combine decay with active drift detection."
        ],
        resolution_strategy="Empirically estimate and validate decay parameters; integrate with drift detection.",
        entity_scope="All time-dependent confidence scores.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Gama et al., A Survey on Concept Drift Adaptation (2014)"
    ),
    # Additional doctrines for 40+ total, with real domain content:
    DoctrineBlock(
        topic="Hierarchical Bayesian Aggregation",
        keywords=["hierarchical Bayesian", "aggregation", "multi-level modeling", "engine groups"],
        conclusion_template="Apply hierarchical Bayesian models to aggregate confidence across engine groups with varying reliabilities.",
        reasoning_framework=(
            "Hierarchical Bayesian models introduce group-level parameters to capture variability among engine groups (e.g., by architecture or data domain). "
            "Each group has its own prior and likelihood, and group-level parameters are estimated jointly. This approach allows information sharing across groups, "
            "improving aggregation accuracy when some groups have limited data. Posterior inference is performed using Markov Chain Monte Carlo or variational methods. "
            "Model selection and convergence diagnostics are critical for reliable aggregation."
        ),
        key_factors=[
            "Definition of engine groups",
            "Choice of priors at each hierarchy level",
            "Convergence diagnostics",
            "Interpretability of group-level effects"
        ],
        primary_authority=[
            "Gelman et al., Bayesian Data Analysis (2013)"
        ],
        burden_holder="Aggregator modeler",
        adversary_position="Hierarchical models can be complex and computationally demanding.",
        counter_arguments=[
            "Variational inference can improve scalability.",
            "Model simplification is possible for small groups.",
            "Empirical Bayes can reduce complexity."
        ],
        resolution_strategy="Use scalable inference methods; validate model fit and convergence.",
        entity_scope="All engine groups with hierarchical structure.",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="Gelman et al., Bayesian Data Analysis (2013)"
    ),
    DoctrineBlock(
        topic="Meta-Learning for Aggregation Rule Selection",
        keywords=["meta-learning", "aggregation rule", "automatic selection", "learning to aggregate"],
        conclusion_template="Use meta-learning to select or learn optimal aggregation rules based on historical performance.",
        reasoning_framework=(
            "Meta-learning frameworks evaluate multiple aggregation strategies on historical data, learning which rules perform best under various conditions. "
            "Features such as engine diversity, reliability, and disagreement inform the meta-learner. The selected aggregation rule is dynamically adapted as new data arrives. "
            "This approach automates rule selection, reducing manual tuning and improving adaptability to changing environments."
        ),
        key_factors=[
            "Availability and quality of meta-training data",
            "Feature engineering for meta-learning",
            "Adaptation to non-stationary environments",
            "Interpretability of learned rules"
        ],
        primary_authority=[
            "Vilalta & Drissi, A Perspective View and Survey of Meta-Learning (2002)"
        ],
        burden_holder="System architect",
        adversary_position="Meta-learning may overfit to historical data and fail to generalize.",
        counter_arguments=[
            "Use cross-validation and regularization.",
            "Monitor for overfitting and update meta-models as needed.",
            "Incorporate domain knowledge into feature selection."
        ],
        resolution_strategy="Regularize meta-learning; validate on out-of-sample data.",
        entity_scope="All aggregation rule selection processes.",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="Vilalta & Drissi, A Perspective View and Survey of Meta-Learning (2002)"
    ),
    DoctrineBlock(
        topic="Adversarial Robustness in Confidence Aggregation",
        keywords=["adversarial robustness", "aggregation", "attack resilience", "outlier resistance"],
        conclusion_template="Design aggregation methods to be robust against adversarial manipulation of engine outputs.",
        reasoning_framework=(
            "Adversarial attacks may target individual engines to manipulate aggregate confidence. Robust aggregation methods, such as median, trimmed mean, "
            "or M-estimators, reduce the influence of compromised engines. Anomaly detection and adversarial training can further enhance resilience. "
            "Regular red-teaming and penetration testing are recommended to identify vulnerabilities. Aggregation logic should be auditable and transparent."
        ),
        key_factors=[
            "Choice of robust aggregation method",
            "Effectiveness of anomaly detection",
            "Frequency of adversarial testing",
            "Transparency and auditability"
        ],
        primary_authority=[
            "Biggio & Roli, Wild Patterns: Ten Years After the Rise of Adversarial Machine Learning (2018)"
        ],
        burden_holder="Security officer",
        adversary_position="Robust methods may reduce sensitivity to legitimate signals.",
        counter_arguments=[
            "Balance robustness and sensitivity through parameter tuning.",
            "Monitor for false positives in anomaly detection.",
            "Document tradeoffs in aggregation design."
        ],
        resolution_strategy="Tune robustness parameters; conduct regular adversarial testing.",
        entity_scope="All aggregation processes subject to adversarial risk.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Biggio & Roli, Wild Patterns (2018)"
    ),
    DoctrineBlock(
        topic="Transparency and Explainability in Aggregation",
        keywords=["transparency", "explainability", "aggregation", "auditability", "interpretability"],
        conclusion_template="Ensure aggregation logic is transparent and explainable to stakeholders.",
        reasoning_framework=(
            "Transparent aggregation enables stakeholders to understand how confidence scores are combined. "
            "Documentation of aggregation rules, weights, and calibration parameters is essential. Explainable aggregation methods (e.g., weighted average, decision rules) "
            "are preferred over opaque meta-models unless interpretability tools are provided. Audit trails should record aggregation decisions for accountability. "
            "User interfaces should present both aggregate and individual engine scores, along with explanations of aggregation logic."
        ),
        key_factors=[
            "Clarity of documentation",
            "Availability of audit trails",
            "Interpretability of aggregation method",
            "User interface design"
        ],
        primary_authority=[
            "Doshi-Velez & Kim, Towards a Rigorous Science of Interpretable Machine Learning (2017)"
        ],
        burden_holder="System owner",
        adversary_position="Transparency may conflict with proprietary methods or competitive advantage.",
        counter_arguments=[
            "Provide high-level explanations without revealing sensitive details.",
            "Use third-party audits to balance transparency and confidentiality.",
            "Adopt explainability standards."
        ],
        resolution_strategy="Document aggregation logic; provide user-friendly explanations; enable audits.",
        entity_scope="All aggregation logic and reporting.",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="Doshi-Velez & Kim, Towards a Rigorous Science of Interpretable Machine Learning (2017)"
    ),
    DoctrineBlock(
        topic="Human-in-the-Loop Aggregation Oversight",
        keywords=["human-in-the-loop", "oversight", "aggregation", "review", "escalation"],
        conclusion_template="Integrate human oversight for aggregation decisions in high-uncertainty or high-impact cases.",
        reasoning_framework=(
            "Automated aggregation may not capture all contextual factors, especially in high-stakes or ambiguous cases. "
            "Human reviewers can provide additional scrutiny, override automated decisions, or escalate for further review. "
            "Escalation criteria should be defined based on disagreement, uncertainty, or impact. User interfaces should facilitate efficient review, "
            "and reviewer feedback should be incorporated into future aggregation logic."
        ),
        key_factors=[
            "Definition of escalation criteria",
            "Efficiency of review interfaces",
            "Feedback incorporation",
            "Training and calibration of reviewers"
        ],
        primary_authority=[
            "Amershi et al., Power to the People: The Role of Humans in Interactive Machine Learning (2014)"
        ],
        burden_holder="System operator",
        adversary_position="Human review may introduce inconsistency or delay.",
        counter_arguments=[
            "Standardize review protocols.",
            "Monitor reviewer consistency and provide training.",
            "Limit human intervention to critical cases."
        ],
        resolution_strategy="Define clear escalation criteria; standardize review processes.",
        entity_scope="All aggregation decisions with high uncertainty or impact.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Amershi et al., Power to the People (2014)"
    ),
    DoctrineBlock(
        topic="Continuous Monitoring and Drift Detection",
        keywords=["monitoring", "drift detection", "aggregation", "performance monitoring", "data drift"],
        conclusion_template="Continuously monitor aggregation performance and detect data or concept drift.",
        reasoning_framework=(
            "Aggregation performance can degrade due to data or concept drift. Continuous monitoring tracks key metrics (e.g., calibration, discrimination, disagreement) "
            "over time. Drift detection algorithms (e.g., Page-Hinkley, ADWIN) identify significant changes in data distribution or engine behavior. "
            "Detected drift triggers recalibration, retraining, or aggregation rule updates. Monitoring dashboards and alerting systems support timely intervention."
        ),
        key_factors=[
            "Choice of drift detection algorithm",
            "Selection of monitoring metrics",
            "Timeliness of intervention",
            "Integration with retraining pipelines"
        ],
        primary_authority=[
            "Gama et al., A Survey on Concept Drift Adaptation (2014)"
        ],
        burden_holder="System operator",
        adversary_position="Frequent false alarms may lead to unnecessary interventions.",
        counter_arguments=[
            "Tune detection thresholds to balance sensitivity and specificity.",
            "Aggregate signals from multiple drift detectors.",
            "Document and review intervention decisions."
        ],
        resolution_strategy="Tune drift detectors; aggregate multiple signals; document interventions.",
        entity_scope="All aggregation processes.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Gama et al., A Survey on Concept Drift Adaptation (2014)"
    ),
    DoctrineBlock(
        topic="Fairness in Confidence Aggregation",
        keywords=["fairness", "aggregation", "bias mitigation", "equity", "group fairness"],
        conclusion_template="Ensure aggregation methods do not introduce or amplify bias across groups.",
        reasoning_framework=(
            "Aggregation methods may inadvertently introduce or amplify bias if engine reliabilities or calibration differ across groups (e.g., demographic, geographic). "
            "Fairness metrics (e.g., demographic parity, equalized odds) are computed for aggregated outputs. Bias mitigation techniques include group-wise calibration, "
            "fair weighting, and post-processing adjustments. Regular fairness audits and stakeholder engagement are recommended."
        ),
        key_factors=[
            "Definition of relevant groups",
            "Selection of fairness metrics",
            "Effectiveness of bias mitigation",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "Barocas et al., Fairness and Machine Learning (2023)"
        ],
        burden_holder="System owner",
        adversary_position="Fairness interventions may reduce aggregate accuracy.",
        counter_arguments=[
            "Balance fairness and accuracy through multi-objective optimization.",
            "Engage stakeholders in defining fairness objectives.",
            "Monitor and report tradeoffs transparently."
        ],
        resolution_strategy="Optimize for fairness and accuracy; audit and report regularly.",
        entity_scope="All aggregation processes affecting groups.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Barocas et al., Fairness and Machine Learning (2023)"
    ),
    DoctrineBlock(
        topic="Privacy Preservation in Aggregation",
        keywords=["privacy", "aggregation", "differential privacy", "data protection", "confidentiality"],
        conclusion_template="Implement privacy-preserving aggregation methods to protect sensitive information.",
        reasoning_framework=(
            "Aggregation may expose sensitive information if individual engine outputs are linked to protected data. "
            "Differential privacy techniques (e.g., noise addition, aggregation thresholds) can protect confidentiality. "
            "Access controls and audit logs further safeguard data. Privacy-preserving aggregation should comply with legal and ethical standards (e.g., GDPR, HIPAA)."
        ),
        key_factors=[
            "Choice of privacy-preserving technique",
            "Impact on aggregation accuracy",
            "Compliance with regulations",
            "Transparency and auditability"
        ],
        primary_authority=[
            "Dwork & Roth, The Algorithmic Foundations of Differential Privacy (2014)"
        ],
        burden_holder="Data protection officer",
        adversary_position="Privacy measures may degrade aggregation utility.",
        counter_arguments=[
            "Tune privacy parameters to balance utility and protection.",
            "Use secure multi-party computation for sensitive aggregation.",
            "Document privacy-utility tradeoffs."
        ],
        resolution_strategy="Tune privacy parameters; use secure computation as needed; document tradeoffs.",
        entity_scope="All aggregation involving sensitive data.",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="Dwork & Roth, The Algorithmic Foundations of Differential Privacy (2014)"
    ),
    DoctrineBlock(
        topic="Scalability of Aggregation Methods",
        keywords=["scalability", "aggregation", "large-scale systems", "distributed aggregation"],
        conclusion_template="Design aggregation methods to scale efficiently with increasing number of engines or data volume.",
        reasoning_framework=(
            "Aggregation methods must handle large numbers of engines and high data throughput. Distributed aggregation frameworks (e.g., MapReduce, Spark) "
            "enable parallel processing. Approximate aggregation algorithms can reduce computational burden. Scalability testing and profiling identify bottlenecks. "
            "Aggregation logic should be modular and stateless where possible to facilitate scaling."
        ),
        key_factors=[
            "Choice of distributed framework",
            "Efficiency of aggregation algorithms",
            "Profiling and optimization",
            "Modularity and statelessness"
        ],
        primary_authority=[
            "Dean & Ghemawat, MapReduce: Simplified Data Processing on Large Clusters (2008)"
        ],
        burden_holder="System architect",
        adversary_position="Scalability measures may sacrifice aggregation accuracy or transparency.",
        counter_arguments=[
            "Profile and optimize aggregation pipelines.",
            "Use approximate methods only where accuracy loss is acceptable.",
            "Document scalability tradeoffs."
        ],
        resolution_strategy="Profile and optimize; document and review scalability tradeoffs.",
        entity_scope="All large-scale aggregation processes.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Dean & Ghemawat, MapReduce (2008)"
    ),
    DoctrineBlock(
        topic="Resource-Efficient Aggregation",
        keywords=["resource efficiency", "aggregation", "low-latency", "energy efficiency", "cost optimization"],
        conclusion_template="Optimize aggregation methods for resource efficiency, minimizing latency and computational cost.",
        reasoning_framework=(
            "Aggregation must often operate under constraints of latency, computational resources, or energy consumption. "
            "Efficient algorithms (e.g., streaming aggregation, incremental updates) reduce resource usage. Profiling identifies hotspots, "
            "and aggregation logic can be tuned for target platforms (e.g., edge devices). Tradeoffs between efficiency and accuracy should be documented."
        ),
        key_factors=[
            "Algorithmic efficiency",
            "Profiling and optimization",
            "Platform-specific tuning",
            "Tradeoff documentation"
        ],
        primary_authority=[
            "Han et al., Data Mining: Concepts and Techniques (2011)"
        ],
        burden_holder="System engineer",
        adversary_position="Efficiency optimizations may reduce aggregation accuracy.",
        counter_arguments=[
            "Profile impact of optimizations on accuracy.",
            "Use adaptive algorithms that degrade gracefully.",
            "Document and review efficiency tradeoffs."
        ],
        resolution_strategy="Profile and optimize; use adaptive algorithms; document tradeoffs.",
        entity_scope="All resource-constrained aggregation processes.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Han et al., Data Mining: Concepts and Techniques (2011)"
    ),
    DoctrineBlock(
        topic="Aggregation under Missing Data",
        keywords=["missing data", "aggregation", "imputation", "robustness", "data gaps"],
        conclusion_template="Apply robust aggregation methods to handle missing engine outputs.",
        reasoning_framework=(
            "Engines may occasionally fail to produce outputs due to errors or data gaps. Aggregation methods should be robust to missing data. "
            "Imputation techniques (e.g., mean, median, model-based) can fill gaps, or aggregation can proceed with available scores using adjusted weights. "
            "The impact of missing data on aggregate confidence should be quantified and reported. Sensitivity analysis assesses robustness to missingness."
        ),
        key_factors=[
            "Pattern and mechanism of missingness",
            "Choice of imputation method",
            "Adjustment of aggregation weights",
            "Reporting of missing data impact"
        ],
        primary_authority=[
            "Little & Rubin, Statistical Analysis with Missing Data (2019)"
        ],
        burden_holder="System operator",
        adversary_position="Imputation may introduce bias or distort aggregate confidence.",
        counter_arguments=[
            "Use model-based imputation where possible.",
            "Report uncertainty due to missing data.",
            "Validate imputation impact empirically."
        ],
        resolution_strategy="Use robust imputation; report and validate impact of missing data.",
        entity_scope="All aggregation processes with missing engine outputs.",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="Little & Rubin, Statistical Analysis with Missing Data (2019)"
    ),
    DoctrineBlock(
        topic="Aggregation with Heterogeneous Engine Types",
        keywords=["heterogeneous engines", "aggregation", "multi-modal", "score harmonization"],
        conclusion_template="Harmonize and aggregate confidence scores from heterogeneous engine types and modalities.",
        reasoning_framework=(
            "Engines may differ in architecture, output scale, or modality (e.g., text, image, signal). Score harmonization aligns outputs to a common scale "
            "using normalization, calibration, or mapping functions. Aggregation methods are selected to accommodate heterogeneity, such as hierarchical or multi-modal fusion. "
            "Validation ensures that harmonization preserves relevant information and does not introduce bias."
        ),
        key_factors=[
            "Degree of heterogeneity",
            "Choice of harmonization method",
            "Validation of harmonized scores",
            "Selection of aggregation method"
        ],
        primary_authority=[
            "Atrey et al., Multimodal Fusion: A Survey (2010)"
        ],
        burden_holder="System architect",
        adversary_position="Harmonization may oversimplify or distort diverse outputs.",
        counter_arguments=[
            "Use modality-specific calibration and normalization.",
            "Validate harmonization empirically.",
            "Document harmonization procedures."
        ],
        resolution_strategy="Apply modality-specific harmonization; validate and document procedures.",
        entity_scope="All aggregation involving heterogeneous engines.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Atrey et al., Multimodal Fusion: A Survey (2010)"
    ),
    DoctrineBlock(
        topic="Aggregation under Real-Time Constraints",
        keywords=["real-time", "aggregation", "low-latency", "streaming", "online aggregation"],
        conclusion_template="Implement real-time aggregation methods for low-latency applications.",
        reasoning_framework=(
            "Real-time applications require aggregation methods that operate with minimal latency. Streaming and online aggregation algorithms process engine outputs as they arrive, "
            "updating aggregate confidence incrementally. Tradeoffs between speed and accuracy are managed through algorithm selection and parameter tuning. Profiling and monitoring "
            "ensure that latency targets are met without sacrificing reliability."
        ),
        key_factors=[
            "Latency requirements",
            "Choice of streaming algorithm",
            "Profiling and monitoring",
            "Accuracy-latency tradeoff"
        ],
        primary_authority=[
            "Babcock et al., Models and Issues in Data Stream Systems (2002)"
        ],
        burden_holder="System engineer",
        adversary_position="Real-time constraints may limit aggregation accuracy or robustness.",
        counter_arguments=[
            "Tune algorithms for target latency and accuracy.",
            "Monitor performance and adjust parameters dynamically.",
            "Document tradeoffs for stakeholders."
        ],
        resolution_strategy="Profile and tune for latency; monitor and document tradeoffs.",
        entity_scope="All real-time aggregation processes.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Babcock et al., Models and Issues in Data Stream Systems (2002)"
    ),
    DoctrineBlock(
        topic="Aggregation for Rare Event Detection",
        keywords=["rare events", "aggregation", "anomaly detection", "low prevalence"],
        conclusion_template="Tailor aggregation methods for effective detection of rare events.",
        reasoning_framework=(
            "Rare event detection poses challenges due to class imbalance and low prevalence. Aggregation methods should emphasize recall and sensitivity, "
            "possibly at the expense of precision. Thresholds may be lowered, and ensemble methods can improve detection rates. Evaluation should use metrics "
            "suitable for rare events (e.g., F1-score, recall at fixed precision). Synthetic data augmentation and oversampling can improve engine diversity."
        ),
        key_factors=[
            "Class imbalance",
            "Threshold selection",
            "Choice of evaluation metrics",
            "Use of data augmentation"
        ],
        primary_authority=[
            "Chandola et al., Anomaly Detection: A Survey (2009)"
        ],
        burden_holder="System analyst",
        adversary_position="Emphasizing recall may increase false positives.",
        counter_arguments=[
            "Balance recall and precision according to application needs.",
            "Monitor and adjust thresholds dynamically.",
            "Report false positive rates transparently."
        ],
        resolution_strategy="Optimize for recall; monitor and report false positives.",
        entity_scope="All rare event aggregation processes.",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="Chandola et al., Anomaly Detection: A Survey (2009)"
    ),
    DoctrineBlock(
        topic="Aggregation with Limited Ground Truth",
        keywords=["limited ground truth", "aggregation", "semi-supervised", "weak supervision"],
        conclusion_template="Leverage semi-supervised or weakly supervised methods for aggregation when ground truth is scarce.",
        reasoning_framework=(
            "When labeled data is limited, aggregation methods can incorporate semi-supervised learning, weak supervision, or transfer learning. "
            "Unlabeled data is used to estimate engine reliability or calibrate scores through self-training, co-training, or expectation-maximization. "
            "Uncertainty quantification is essential to reflect the limitations of available ground truth."
        ),
        key_factors=[
            "Availability of unlabeled data",
            "Choice of semi-supervised method",
            "Uncertainty quantification",
            "Validation with limited labels"
        ],
        primary_authority=[
            "Zhu, Semi-Supervised Learning Literature Survey (2005)"
        ],
        burden_holder="System analyst",
        adversary_position="Semi-supervised methods may propagate errors from unreliable engines.",
        counter_arguments=[
            "Monitor for error amplification.",
            "Use multiple weak supervision sources.",
            "Validate with available labels."
        ],
        resolution_strategy="Monitor and validate; use multiple supervision sources.",
        entity_scope="All aggregation with limited ground truth.",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="Zhu, Semi-Supervised Learning Literature Survey (2005)"
    ),
    DoctrineBlock(
        topic="Aggregation for Multi-Class Confidence Scores",
        keywords=["multi-class", "aggregation", "multi-label", "score fusion"],
        conclusion_template="Adapt aggregation methods to handle multi-class or multi-label confidence scores.",
        reasoning_framework=(
            "Aggregation for multi-class or multi-label problems requires methods that preserve class probabilities. "
            "Score fusion can be performed per class, followed by normalization to ensure valid probability distributions. "
            "Hierarchical or structured aggregation methods can exploit relationships among classes. Evaluation should use multi-class metrics (e.g., macro/micro-averaged Brier score, log-loss)."
        ),
        key_factors=[
            "Number and structure of classes",
            "Choice of aggregation method",
            "Normalization of class probabilities",
            "Selection of evaluation metrics"
        ],
        primary_authority=[
            "Tsoumakas & Katakis, Multi-Label Classification: An Overview (2007)"
        ],
        burden_holder="System architect",
        adversary_position="Aggregation may dilute confidence for minority classes.",
        counter_arguments=[
            "Use class-weighted aggregation.",
            "Monitor and report per-class performance.",
            "Adjust aggregation for class imbalance."
        ],
        resolution_strategy="Apply class-weighted aggregation; monitor per-class metrics.",
        entity_scope="All multi-class or multi-label aggregation processes.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Tsoumakas & Katakis, Multi-Label Classification: An Overview (2007)"
    ),
    DoctrineBlock(
        topic="Aggregation with Hierarchical Labels",
        keywords=["hierarchical labels", "aggregation", "taxonomy", "structured output"],
        conclusion_template="Incorporate label hierarchy into aggregation for structured prediction tasks.",
        reasoning_framework=(
            "When labels are organized hierarchically (e.g., taxonomy), aggregation methods should respect the structure. "
            "Confidence scores are aggregated at each level of the hierarchy, and dependencies among labels are modeled explicitly. "
            "Hierarchical aggregation can improve interpretability and performance for structured prediction tasks."
        ),
        key_factors=[
            "Definition of label hierarchy",
            "Aggregation at multiple hierarchy levels",
            "Modeling of label dependencies",
            "Interpretability"
        ],
        primary_authority=[
            "Silla & Freitas, A Survey of Hierarchical Classification Across Different Application Domains (2011)"
        ],
        burden_holder="System designer",
        adversary_position="Hierarchical aggregation may increase complexity and reduce transparency.",
        counter_arguments=[
            "Visualize hierarchical aggregation results.",
            "Document aggregation logic at each level.",
            "Simplify hierarchy where possible."
        ],
        resolution_strategy="Document and visualize hierarchy; simplify as needed.",
        entity_scope="All aggregation with hierarchical labels.",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="Silla & Freitas, A Survey of Hierarchical Classification (2011)"
    ),
    DoctrineBlock(
        topic="Aggregation for Continuous Outcomes",
        keywords=["continuous outcomes", "regression", "aggregation", "score fusion"],
        conclusion_template="Aggregate confidence scores for continuous outcome prediction using regression-based methods.",
        reasoning_framework=(
            "For continuous outcomes, aggregation methods such as weighted averaging, stacking regression, or Bayesian model averaging are used. "
            "Calibration and normalization ensure comparability of continuous confidence estimates. Evaluation uses regression metrics (e.g., RMSE, MAE). "
            "Uncertainty intervals are reported alongside point estimates."
        ),
        key_factors=[
            "Choice of regression aggregation method",
            "Calibration of continuous scores",
            "Selection of evaluation metrics",
            "Reporting of uncertainty"
        ],
        primary_authority=[
            "Breiman, Stacked Regressions (1996)"
        ],
        burden_holder="System analyst",
        adversary_position="Regression aggregation may be sensitive to outliers or heteroscedasticity.",
        counter_arguments=[
            "Use robust regression methods.",
            "Monitor residuals for heteroscedasticity.",
            "Report and address outlier impact."
        ],
        resolution_strategy="Apply robust regression; monitor and report residuals.",
        entity_scope="All continuous outcome aggregation processes.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Breiman, Stacked Regressions (1996)"
    ),
    DoctrineBlock(
        topic="Aggregation for Unsupervised Confidence Scores",
        keywords=["unsupervised", "aggregation", "clustering", "anomaly detection"],
        conclusion_template="Aggregate confidence scores from unsupervised engines using consensus or voting methods.",
        reasoning_framework=(
            "Unsupervised engines (e.g., clustering, anomaly detection) may produce confidence scores without ground truth. "
            "Consensus methods (e.g., majority voting, average confidence) aggregate outputs, and stability analysis assesses reliability. "
            "External validation (e.g., using labeled subsets) can calibrate and interpret aggregate confidence."
        ),
        key_factors=[
            "Choice of consensus method",
            "Stability analysis",
            "External validation",
            "Interpretation without ground truth"
        ],
        primary_authority=[
            "Fred & Jain, Combining Multiple Clusterings Using Evidence Accumulation (2005)"
        ],
        burden_holder="System analyst",
        adversary_position="Unsupervised aggregation may lack interpretability or validation.",
        counter_arguments=[
            "Use labeled subsets for validation.",
            "Report stability and consensus metrics.",
            "Document aggregation assumptions."
        ],
        resolution_strategy="Validate with labeled data; report stability and consensus.",
        entity_scope="All unsupervised aggregation processes.",
        confidence=0.87,
        confidence_zone="Medium",
        controlling_precedent="Fred & Jain, Combining Multiple Clusterings (2005)"
    ),
    DoctrineBlock(
        topic="Aggregation for Streaming Data",
        keywords=["streaming data", "aggregation", "online learning", "incremental aggregation"],
        conclusion_template="Implement incremental aggregation methods for streaming data environments.",
        reasoning_framework=(
            "Streaming data requires aggregation methods that update incrementally as new data arrives. Online learning algorithms (e.g., stochastic gradient descent, online averaging) "
            "enable real-time updates to aggregation parameters. Windowing and forgetting mechanisms manage memory and adapt to changing data distributions."
        ),
        key_factors=[
            "Choice of online aggregation algorithm",
            "Window size and forgetting mechanism",
            "Adaptation to data drift",
            "Resource constraints"
        ],
        primary_authority=[
            "Gama, Knowledge Discovery from Data Streams (2010)"
        ],
        burden_holder="System engineer",
        adversary_position="Incremental methods may lag in adapting to rapid changes.",
        counter_arguments=[
            "Tune window size and update frequency.",
            "Combine online and batch updates.",
            "Monitor adaptation performance."
        ],
        resolution_strategy="Tune and monitor online aggregation; combine with batch updates as needed.",
        entity_scope="All streaming data aggregation processes.",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="Gama, Knowledge Discovery from Data Streams (2010)"
    ),
    DoctrineBlock(
        topic="Aggregation for Federated Learning",
        keywords=["federated learning", "aggregation", "distributed", "privacy-preserving"],
        conclusion_template="Aggregate confidence scores in federated learning settings while preserving privacy and communication efficiency.",
        reasoning_framework=(
            "Federated learning aggregates model updates or confidence scores from distributed clients without centralizing raw data. Secure aggregation protocols "
            "ensure privacy, and communication-efficient algorithms (e.g., quantization, sparsification) reduce overhead. Aggregation must account for client heterogeneity "
            "and potential adversarial clients. Regular audits and monitoring are recommended."
        ),
        key_factors=[
            "Choice of secure aggregation protocol",
            "Communication efficiency",
            "Handling of client heterogeneity",
            "Adversarial robustness"
        ],
        primary_authority=[
            "Kairouz et al., Advances and Open Problems in Federated Learning (2021)"
        ],
        burden_holder="Federated system architect",
        adversary_position="Federated aggregation may be vulnerable to poisoning or privacy attacks.",
        counter_arguments=[
            "Implement robust and secure aggregation protocols.",
            "Monitor for anomalous client behavior.",
            "Audit aggregation processes regularly."
        ],
        resolution_strategy="Use secure and robust protocols; monitor and audit regularly.",
        entity_scope="All federated aggregation processes.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Kairouz et al., Advances and Open Problems in Federated Learning (2021)"
    ),
    DoctrineBlock(
        topic="Aggregation for Explainable AI Systems",
        keywords=["explainable AI", "aggregation", "interpretability", "transparency"],
        conclusion_template="Design aggregation logic to support explainability and user understanding.",
        reasoning_framework=(
            "Explainable AI systems require aggregation methods that are interpretable and transparent. Aggregation logic should be documented, and explanations of how "
            "individual engine scores contribute to the aggregate should be provided. Visualization tools and user interfaces enhance understanding. Tradeoffs between "
            "explainability and performance should be documented and communicated."
        ),
        key_factors=[
            "Clarity of aggregation logic",
            "Availability of explanations",
            "User interface design",
            "Documentation of tradeoffs"
        ],
        primary_authority=[
            "Doshi-Velez & Kim, Towards a Rigorous Science of Interpretable Machine Learning (2017)"
        ],
        burden_holder="System owner",
        adversary_position="Explainable aggregation may limit use of complex meta-models.",
        counter_arguments=[
            "Use interpretable meta-models where possible.",
            "Provide post-hoc explanations for complex models.",
            "Balance explainability and performance."
        ],
        resolution_strategy="Document and visualize aggregation logic; provide explanations.",
        entity_scope="All explainable AI aggregation processes.",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="Doshi-Velez & Kim, Towards a Rigorous Science of Interpretable Machine Learning (2017)"
    ),
    DoctrineBlock(
        topic="Aggregation for Regulatory Compliance",
        keywords=["regulatory compliance", "aggregation", "auditability", "documentation", "standards"],
        conclusion_template="Ensure aggregation processes comply with relevant regulations and standards.",
        reasoning_framework=(
            "Aggregation methods may be subject to regulatory requirements (e.g., GDPR, HIPAA, ISO standards). Documentation of aggregation logic, audit trails, "
            "and compliance checks are essential. Regular audits and updates ensure ongoing compliance. Stakeholder engagement and legal review are recommended."
        ),
        key_factors=[
            "Identification of applicable regulations",
            "Documentation and auditability",
            "Frequency of compliance checks",
            "Stakeholder engagement"
        ],
        primary_authority=[
            "European Commission, GDPR (2016)",
            "US Department of Health & Human Services, HIPAA (1996)"
        ],
        burden_holder="Compliance officer",
        adversary_position="Compliance may constrain aggregation method choices.",
        counter_arguments=[
            "Engage legal and compliance teams early.",
            "Document rationale for method selection.",
            "Update aggregation logic as regulations evolve."
        ],
        resolution_strategy="Document and audit aggregation logic; engage stakeholders.",
        entity_scope="All regulated aggregation processes.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="European Commission, GDPR (2016)"
    ),
    DoctrineBlock(
        topic="Aggregation for Model Lifecycle Management",
        keywords=["model lifecycle", "aggregation", "deployment", "maintenance", "retirement"],
        conclusion_template="Integrate aggregation logic into model lifecycle management, including deployment, monitoring, and retirement.",
        reasoning_framework=(
            "Aggregation logic should be versioned, tested, and monitored as part of the overall model lifecycle. Deployment pipelines should include aggregation validation. "
            "Monitoring tracks aggregation performance, and retirement criteria are defined for outdated or underperforming aggregation rules. Documentation and stakeholder "
            "communication support lifecycle management."
        ),
        key_factors=[
            "Versioning and testing of aggregation logic",
            "Monitoring and performance tracking",
            "Retirement criteria",
            "Stakeholder communication"
        ],
        primary_authority=[
            "Sculley et al., Hidden Technical Debt in Machine Learning Systems (2015)"
        ],
        burden_holder="Model operations manager",
        adversary_position="Lifecycle management may add operational overhead.",
        counter_arguments=[
            "Automate lifecycle management where possible.",
            "Integrate aggregation checks into CI/CD pipelines.",
            "Document and communicate lifecycle processes."
        ],
        resolution_strategy="Automate and document lifecycle management; integrate into deployment pipelines.",
        entity_scope="All aggregation logic across model lifecycle.",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="Sculley et al., Hidden Technical Debt in Machine Learning Systems (2015)"
    ),
    DoctrineBlock(
        topic="Aggregation for Edge and IoT Devices",
        keywords=["edge computing", "IoT", "aggregation", "resource constraints", "distributed"],
        conclusion_template="Adapt aggregation methods for deployment on edge and IoT devices with limited resources.",
        reasoning_framework=(
            "Edge and IoT devices require lightweight aggregation methods due to limited memory, compute, and power. Streaming and approximate aggregation algorithms are preferred. "
            "Aggregation logic should be modular and support distributed deployment. Communication-efficient protocols minimize bandwidth usage. Security and privacy must be considered."
        ),
        key_factors=[
            "Algorithmic efficiency",
            "Modularity and deployability",
            "Communication efficiency",
            "Security and privacy"
        ],
        primary_authority=[
            "Shi et al., Edge Computing: Vision and Challenges (2016)"
        ],
        burden_holder="Edge system engineer",
        adversary_position="Resource constraints may limit aggregation accuracy or robustness.",
        counter_arguments=[
            "Profile and optimize for target platforms.",
            "Use adaptive algorithms that degrade gracefully.",
            "Document and monitor tradeoffs."
        ],
        resolution_strategy="Optimize and adapt aggregation for edge; monitor and document tradeoffs.",
        entity_scope="All edge and IoT aggregation processes.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Shi et al., Edge Computing: Vision and Challenges (2016)"
    ),
    DoctrineBlock(
        topic="Aggregation for Cross-Domain Applications",
        keywords=["cross-domain", "aggregation", "domain adaptation", "transfer learning"],
        conclusion_template="Adapt aggregation methods for cross-domain applications using domain adaptation techniques.",
        reasoning_framework=(
            "Cross-domain aggregation requires methods that account for differences in data distribution, engine reliability, and calibration across domains. "
            "Domain adaptation techniques (e.g., reweighting, transfer learning) align confidence scores. Aggregation logic should be validated in each target domain, "
            "and domain-specific calibration may be necessary."
        ),
        key_factors=[
            "Degree of domain shift",
            "Choice of adaptation technique",
            "Validation in target domains",
            "Domain-specific calibration"
        ],
        primary_authority=[
            "Pan & Yang, A Survey on Transfer Learning (2010)"
        ],
        burden_holder="System architect",
        adversary_position="Domain adaptation may not fully correct for distributional differences.",
        counter_arguments=[
            "Validate adaptation empirically in each domain.",
            "Combine multiple adaptation techniques.",
            "Monitor and report domain-specific performance."
        ],
        resolution_strategy="Empirically validate and monitor adaptation; document domain-specific results.",
        entity_scope="All cross-domain aggregation processes.",
        confidence=0.88,
        confidence_zone="Medium",
        controlling_precedent="Pan & Yang, A Survey on Transfer Learning (2010)"
    ),
    DoctrineBlock(
        topic="Aggregation for Multi-Task Learning",
        keywords=["multi-task learning", "aggregation", "shared representation", "task-specific"],
        conclusion_template="Aggregate confidence scores across multiple tasks using shared or task-specific aggregation logic.",
        reasoning_framework=(
            "In multi-task learning, aggregation can leverage shared representations or task-specific logic. Joint aggregation improves generalization, "
            "while task-specific aggregation preserves specialization. Evaluation should use multi-task metrics, and aggregation logic should be modular to support task addition or removal."
        ),
        key_factors=[
            "Task similarity and relatedness",
            "Choice of shared vs. task-specific aggregation",
            "Evaluation with multi-task metrics",
            "Modularity of aggregation logic"
        ],
        primary_authority=[
            "Caruana, Multitask Learning (1997)"
        ],
        burden_holder="System designer",
        adversary_position="Joint aggregation may dilute performance on specialized tasks.",
        counter_arguments=[
            "Monitor per-task performance.",
            "Adjust aggregation logic for task specialization.",
            "Document tradeoffs between generalization and specialization."
        ],
        resolution_strategy="Monitor and adjust aggregation per task; document tradeoffs.",
        entity_scope="All multi-task aggregation processes.",
        confidence=0.89,
        confidence_zone="Medium",
        controlling_precedent="Caruana, Multitask Learning (1997)"
    ),
    DoctrineBlock(
        topic="Aggregation for Uncertainty-Aware Decision Making",
        keywords=["uncertainty-aware", "aggregation", "decision making", "risk management"],
        conclusion_template="Integrate uncertainty estimates from aggregation into downstream decision-making processes.",
        reasoning_framework=(
            "Uncertainty estimates from aggregation (e.g., confidence intervals, disagreement metrics) inform risk-aware decisions. Decision thresholds can be adjusted based on uncertainty, "
            "and high-uncertainty cases can be escalated for human review. Reporting uncertainty alongside aggregate confidence supports transparency and risk management."
        ),
        key_factors=[
            "Quality of uncertainty estimates",
            "Integration with decision thresholds",
            "Escalation criteria for high uncertainty",
            "Transparency in reporting"
        ],
        primary_authority=[
            "Gal & Ghahramani, Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning (2016)"
        ],
        burden_holder="Decision maker",
        adversary_position="Uncertainty estimates may be misinterpreted or ignored.",
        counter_arguments=[
            "Provide clear guidelines for interpreting uncertainty.",
            "Integrate uncertainty into automated decision logic.",
            "Monitor and audit decision outcomes."
        ],
        resolution_strategy="Educate users; integrate uncertainty into decision logic; audit outcomes.",
        entity_scope="All uncertainty-aware decision processes.",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="Gal & Ghahramani, Dropout as a Bayesian Approximation (2016)"
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
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in k.lower() for k in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower() or
            keyword_lower in doctrine.conclusion_template.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]