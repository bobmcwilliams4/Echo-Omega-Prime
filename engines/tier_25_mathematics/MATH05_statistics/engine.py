"""
MATH05 — Statistics Intelligence Engine
TIE-20 Compliant | Tier 13 Mathematics | Port 8567
Pure Python statistical computation engine.

All core math implemented without scipy/numpy dependency.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
import uuid
from collections import Counter
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
SYSTEMS_DIR = ENGINE_DIR.parent
sys.path.insert(0, str(SYSTEMS_DIR))

# ---------------------------------------------------------------------------
# Loguru config
# ---------------------------------------------------------------------------
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>MATH05</cyan> | {message}",
    level="DEBUG",
)
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
logger.add(
    LOG_DIR / "math05_{time:YYYY-MM-DD}.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG",
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "MATH05"
ENGINE_NAME = "Statistics Intelligence Engine"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8567
ENGINE_TIER = 13
ENGINE_DOMAIN = "mathematics.statistics"
ENGINE_MODE = "DET"
ENGINE_AUTH_LEVEL = 5.0

AUDIT_LOG_PATH = ENGINE_DIR / "audit_trail.jsonl"
DOCTRINE_CACHE_PATH = ENGINE_DIR / "doctrine_cache.json"
SEMANTIC_DICT_PATH = ENGINE_DIR / "semantic_dict.json"
COVERAGE_MAP_PATH = ENGINE_DIR / "coverage_map.json"


# ═══════════════════════════════════════════════════════════════════════════
# PURE PYTHON MATH LIBRARY
# ═══════════════════════════════════════════════════════════════════════════

def _gamma_lanczos(z: float) -> float:
    """Lanczos approximation of the Gamma function."""
    if z < 0.5:
        return math.pi / (math.sin(math.pi * z) * _gamma_lanczos(1.0 - z))
    z -= 1.0
    g = 7
    c = [
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7,
    ]
    x = c[0]
    for i in range(1, g + 2):
        x += c[i] / (z + i)
    t = z + g + 0.5
    return math.sqrt(2.0 * math.pi) * (t ** (z + 0.5)) * math.exp(-t) * x


def _ln_gamma(z: float) -> float:
    """Natural log of the Gamma function."""
    return math.log(_gamma_lanczos(z))


def _beta_func(a: float, b: float) -> float:
    """Beta function B(a,b) = Gamma(a)*Gamma(b)/Gamma(a+b)."""
    return math.exp(_ln_gamma(a) + _ln_gamma(b) - _ln_gamma(a + b))


def _regularized_incomplete_beta(x: float, a: float, b: float, max_iter: int = 200, tol: float = 1e-12) -> float:
    """Regularized incomplete beta function I_x(a,b) via continued fraction."""
    if x < 0.0 or x > 1.0:
        raise ValueError("x must be in [0,1]")
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - _regularized_incomplete_beta(1.0 - x, b, a, max_iter, tol)
    ln_prefix = _ln_gamma(a + b) - _ln_gamma(a) - _ln_gamma(b) + a * math.log(x) + b * math.log(1.0 - x)
    prefix = math.exp(ln_prefix)
    # Lentz continued fraction
    f = 1.0
    c = 1.0
    d = 1.0 - (a + b) * x / (a + 1.0)
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    f = d
    for m in range(1, max_iter + 1):
        # even step
        numerator = m * (b - m) * x / ((a + 2.0 * m - 1.0) * (a + 2.0 * m))
        d = 1.0 + numerator * d
        if abs(d) < 1e-30:
            d = 1e-30
        d = 1.0 / d
        c = 1.0 + numerator / c
        if abs(c) < 1e-30:
            c = 1e-30
        f *= d * c
        # odd step
        numerator = -((a + m) * (a + b + m) * x) / ((a + 2.0 * m) * (a + 2.0 * m + 1.0))
        d = 1.0 + numerator * d
        if abs(d) < 1e-30:
            d = 1e-30
        d = 1.0 / d
        c = 1.0 + numerator / c
        if abs(c) < 1e-30:
            c = 1e-30
        delta = d * c
        f *= delta
        if abs(delta - 1.0) < tol:
            break
    return prefix * f / a


def _erf(x: float) -> float:
    """Error function via Abramowitz & Stegun approximation."""
    sign = 1 if x >= 0 else -1
    x = abs(x)
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    p = 0.3275911
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y


def _normal_cdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """CDF of normal distribution."""
    z = (x - mu) / sigma
    return 0.5 * (1.0 + _erf(z / math.sqrt(2.0)))


def _normal_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """PDF of normal distribution."""
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2.0 * math.pi))


def _t_cdf(t_val: float, df: float) -> float:
    """CDF of Student's t-distribution using regularized incomplete beta."""
    if df <= 0:
        raise ValueError("df must be positive")
    x_beta = df / (df + t_val * t_val)
    ib = _regularized_incomplete_beta(x_beta, df / 2.0, 0.5)
    if t_val >= 0:
        return 1.0 - 0.5 * ib
    return 0.5 * ib


def _t_pdf(t_val: float, df: float) -> float:
    """PDF of Student's t-distribution."""
    coeff = _gamma_lanczos((df + 1.0) / 2.0) / (math.sqrt(df * math.pi) * _gamma_lanczos(df / 2.0))
    return coeff * (1.0 + t_val * t_val / df) ** (-(df + 1.0) / 2.0)


def _chi2_cdf(x: float, df: float) -> float:
    """CDF of chi-squared distribution via regularized lower incomplete gamma."""
    if x <= 0:
        return 0.0
    return _regularized_lower_gamma(df / 2.0, x / 2.0)


def _regularized_lower_gamma(a: float, x: float, max_iter: int = 200, tol: float = 1e-12) -> float:
    """Regularized lower incomplete gamma P(a,x) via series expansion."""
    if x < 0:
        return 0.0
    if x == 0:
        return 0.0
    if x < a + 1.0:
        # series
        ap = a
        s = 1.0 / a
        delta = s
        for _ in range(max_iter):
            ap += 1.0
            delta *= x / ap
            s += delta
            if abs(delta) < abs(s) * tol:
                break
        return s * math.exp(-x + a * math.log(x) - _ln_gamma(a))
    else:
        # continued fraction for upper, return 1 - Q
        return 1.0 - _upper_gamma_cf(a, x, max_iter, tol)


def _upper_gamma_cf(a: float, x: float, max_iter: int = 200, tol: float = 1e-12) -> float:
    """Upper incomplete gamma Q(a,x) via continued fraction."""
    f = x - a + 1.0
    if abs(f) < 1e-30:
        f = 1e-30
    c = 1.0 / f
    d = 1.0
    result = c
    for n in range(1, max_iter + 1):
        an = -n * (n - a)
        bn = x - a + 1.0 + 2.0 * n
        d = bn + an * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = bn + an / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        result *= delta
        if abs(delta - 1.0) < tol:
            break
    return math.exp(-x + a * math.log(x) - _ln_gamma(a)) * result


def _f_cdf(x: float, df1: float, df2: float) -> float:
    """CDF of F-distribution."""
    if x <= 0:
        return 0.0
    v = df1 * x / (df1 * x + df2)
    return _regularized_incomplete_beta(v, df1 / 2.0, df2 / 2.0)


def _binomial_pmf(k: int, n: int, p: float) -> float:
    """PMF of binomial distribution."""
    if k < 0 or k > n:
        return 0.0
    ln_coeff = _ln_gamma(n + 1) - _ln_gamma(k + 1) - _ln_gamma(n - k + 1)
    if p == 0:
        return 1.0 if k == 0 else 0.0
    if p == 1:
        return 1.0 if k == n else 0.0
    return math.exp(ln_coeff + k * math.log(p) + (n - k) * math.log(1 - p))


def _binomial_cdf(k: int, n: int, p: float) -> float:
    """CDF of binomial distribution."""
    total = 0.0
    for i in range(k + 1):
        total += _binomial_pmf(i, n, p)
    return min(total, 1.0)


def _poisson_pmf(k: int, lam: float) -> float:
    """PMF of Poisson distribution."""
    if k < 0:
        return 0.0
    return math.exp(-lam + k * math.log(lam) - _ln_gamma(k + 1))


def _poisson_cdf(k: int, lam: float) -> float:
    """CDF of Poisson distribution."""
    total = 0.0
    for i in range(k + 1):
        total += _poisson_pmf(i, lam)
    return min(total, 1.0)


def _exponential_pdf(x: float, lam: float) -> float:
    """PDF of exponential distribution."""
    if x < 0:
        return 0.0
    return lam * math.exp(-lam * x)


def _exponential_cdf(x: float, lam: float) -> float:
    """CDF of exponential distribution."""
    if x < 0:
        return 0.0
    return 1.0 - math.exp(-lam * x)


def _normal_quantile(p: float) -> float:
    """Inverse normal CDF (quantile) via rational approximation (Beasley-Springer-Moro)."""
    if p <= 0:
        return -math.inf
    if p >= 1:
        return math.inf
    if p == 0.5:
        return 0.0
    a = [
        -3.969683028665376e+01, 2.209460984245205e+02,
        -2.759285104469687e+02, 1.383577518672690e+02,
        -3.066479806614716e+01, 2.506628277459239e+00,
    ]
    b = [
        -5.447609879822406e+01, 1.615858368580409e+02,
        -1.556989798598866e+02, 6.680131188771972e+01,
        -1.328068155288572e+01,
    ]
    c = [
        -7.784894002430293e-03, -3.223964580411365e-01,
        -2.400758277161838e+00, -2.549732539343734e+00,
        4.374664141464968e+00, 2.938163982698783e+00,
    ]
    d = [
        7.784695709041462e-03, 3.224671290700398e-01,
        2.445134137142996e+00, 3.754408661907416e+00,
    ]
    p_low = 0.02425
    p_high = 1.0 - p_low
    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
               (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)


# ═══════════════════════════════════════════════════════════════════════════
# DESCRIPTIVE STATISTICS
# ═══════════════════════════════════════════════════════════════════════════

def compute_mean(data: list[float]) -> float:
    """Arithmetic mean."""
    if not data:
        raise ValueError("Empty dataset")
    return sum(data) / len(data)


def compute_median(data: list[float]) -> float:
    """Median value."""
    if not data:
        raise ValueError("Empty dataset")
    s = sorted(data)
    n = len(s)
    mid = n // 2
    if n % 2 == 0:
        return (s[mid - 1] + s[mid]) / 2.0
    return s[mid]


def compute_mode(data: list[float]) -> list[float]:
    """Mode(s) — all values with highest frequency."""
    if not data:
        raise ValueError("Empty dataset")
    counts = Counter(data)
    max_count = max(counts.values())
    if max_count == 1:
        return []  # no mode
    return sorted([k for k, v in counts.items() if v == max_count])


def compute_variance(data: list[float], sample: bool = True) -> float:
    """Variance (sample or population)."""
    n = len(data)
    if n < 2 and sample:
        raise ValueError("Need at least 2 data points for sample variance")
    mean = compute_mean(data)
    ss = sum((x - mean) ** 2 for x in data)
    return ss / (n - 1) if sample else ss / n


def compute_std_dev(data: list[float], sample: bool = True) -> float:
    """Standard deviation."""
    return math.sqrt(compute_variance(data, sample))


def compute_skewness(data: list[float]) -> float:
    """Sample skewness (Fisher's definition)."""
    n = len(data)
    if n < 3:
        raise ValueError("Need at least 3 data points")
    mean = compute_mean(data)
    s = compute_std_dev(data, sample=True)
    if s == 0:
        return 0.0
    m3 = sum((x - mean) ** 3 for x in data) / n
    return m3 / (s ** 3)


def compute_kurtosis(data: list[float]) -> float:
    """Excess kurtosis (Fisher's definition, normal = 0)."""
    n = len(data)
    if n < 4:
        raise ValueError("Need at least 4 data points")
    mean = compute_mean(data)
    s = compute_std_dev(data, sample=True)
    if s == 0:
        return 0.0
    m4 = sum((x - mean) ** 4 for x in data) / n
    return m4 / (s ** 4) - 3.0


def compute_percentile(data: list[float], p: float) -> float:
    """Percentile using linear interpolation."""
    if not 0 <= p <= 100:
        raise ValueError("p must be in [0, 100]")
    s = sorted(data)
    n = len(s)
    if n == 1:
        return s[0]
    rank = (p / 100.0) * (n - 1)
    low = int(math.floor(rank))
    high = int(math.ceil(rank))
    if low == high:
        return s[low]
    frac = rank - low
    return s[low] * (1.0 - frac) + s[high] * frac


def compute_quartiles(data: list[float]) -> dict[str, float]:
    """Q1, Q2 (median), Q3."""
    return {
        "q1": compute_percentile(data, 25),
        "q2": compute_percentile(data, 50),
        "q3": compute_percentile(data, 75),
    }


def compute_iqr(data: list[float]) -> float:
    """Interquartile range."""
    q = compute_quartiles(data)
    return q["q3"] - q["q1"]


def descriptive_stats(data: list[float]) -> dict[str, Any]:
    """Full descriptive statistics summary."""
    n = len(data)
    if n == 0:
        raise ValueError("Empty dataset")
    mean = compute_mean(data)
    med = compute_median(data)
    modes = compute_mode(data)
    var_s = compute_variance(data) if n >= 2 else None
    sd_s = compute_std_dev(data) if n >= 2 else None
    var_p = compute_variance(data, sample=False)
    sd_p = compute_std_dev(data, sample=False)
    skew = compute_skewness(data) if n >= 3 else None
    kurt = compute_kurtosis(data) if n >= 4 else None
    quarts = compute_quartiles(data)
    iqr = compute_iqr(data)
    return {
        "n": n,
        "mean": mean,
        "median": med,
        "mode": modes,
        "sample_variance": var_s,
        "sample_std_dev": sd_s,
        "population_variance": var_p,
        "population_std_dev": sd_p,
        "skewness": skew,
        "excess_kurtosis": kurt,
        "min": min(data),
        "max": max(data),
        "range": max(data) - min(data),
        "q1": quarts["q1"],
        "median_q2": quarts["q2"],
        "q3": quarts["q3"],
        "iqr": iqr,
        "sum": sum(data),
        "se_mean": sd_s / math.sqrt(n) if sd_s else None,
    }


# ═══════════════════════════════════════════════════════════════════════════
# HYPOTHESIS TESTING
# ═══════════════════════════════════════════════════════════════════════════

class TestResult(BaseModel):
    """Standard output for all hypothesis tests."""
    test_name: str
    statistic: float
    p_value: float
    df: Optional[float] = None
    alpha: float = 0.05
    reject_null: bool
    conclusion: str
    effect_size: Optional[float] = None
    confidence_interval: Optional[dict[str, float]] = None


def z_test_one_sample(data: list[float], mu0: float, sigma: float, alpha: float = 0.05, alternative: str = "two-sided") -> TestResult:
    """One-sample z-test (known population std dev)."""
    n = len(data)
    xbar = compute_mean(data)
    se = sigma / math.sqrt(n)
    z = (xbar - mu0) / se
    if alternative == "two-sided":
        p_value = 2.0 * (1.0 - _normal_cdf(abs(z)))
    elif alternative == "greater":
        p_value = 1.0 - _normal_cdf(z)
    else:
        p_value = _normal_cdf(z)
    reject = p_value < alpha
    z_crit = _normal_quantile(1.0 - alpha / 2.0)
    ci = {"lower": xbar - z_crit * se, "upper": xbar + z_crit * se}
    cohens_d = (xbar - mu0) / sigma
    return TestResult(
        test_name="One-Sample Z-Test",
        statistic=round(z, 6),
        p_value=round(p_value, 8),
        alpha=alpha,
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (mu = {mu0}) at alpha={alpha}",
        effect_size=round(cohens_d, 6),
        confidence_interval={"lower": round(ci["lower"], 6), "upper": round(ci["upper"], 6)},
    )


def t_test_one_sample(data: list[float], mu0: float, alpha: float = 0.05, alternative: str = "two-sided") -> TestResult:
    """One-sample t-test."""
    n = len(data)
    if n < 2:
        raise ValueError("Need at least 2 data points")
    xbar = compute_mean(data)
    s = compute_std_dev(data, sample=True)
    se = s / math.sqrt(n)
    t_stat = (xbar - mu0) / se
    df = n - 1
    if alternative == "two-sided":
        p_value = 2.0 * (1.0 - _t_cdf(abs(t_stat), df))
    elif alternative == "greater":
        p_value = 1.0 - _t_cdf(t_stat, df)
    else:
        p_value = _t_cdf(t_stat, df)
    reject = p_value < alpha
    cohens_d = (xbar - mu0) / s
    return TestResult(
        test_name="One-Sample T-Test",
        statistic=round(t_stat, 6),
        p_value=round(p_value, 8),
        df=df,
        alpha=alpha,
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (mu = {mu0}) at alpha={alpha}",
        effect_size=round(cohens_d, 6),
    )


def t_test_two_sample(data1: list[float], data2: list[float], alpha: float = 0.05, equal_var: bool = True, alternative: str = "two-sided") -> TestResult:
    """Two-sample t-test (independent samples)."""
    n1, n2 = len(data1), len(data2)
    x1, x2 = compute_mean(data1), compute_mean(data2)
    s1, s2 = compute_std_dev(data1), compute_std_dev(data2)
    if equal_var:
        sp2 = ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)
        se = math.sqrt(sp2 * (1.0 / n1 + 1.0 / n2))
        df = n1 + n2 - 2
    else:
        se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
        num = (s1 ** 2 / n1 + s2 ** 2 / n2) ** 2
        denom = (s1 ** 2 / n1) ** 2 / (n1 - 1) + (s2 ** 2 / n2) ** 2 / (n2 - 1)
        df = num / denom if denom > 0 else n1 + n2 - 2
    t_stat = (x1 - x2) / se if se > 0 else 0.0
    if alternative == "two-sided":
        p_value = 2.0 * (1.0 - _t_cdf(abs(t_stat), df))
    elif alternative == "greater":
        p_value = 1.0 - _t_cdf(t_stat, df)
    else:
        p_value = _t_cdf(t_stat, df)
    reject = p_value < alpha
    pooled_s = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)) if (n1 + n2 > 2) else 1.0
    cohens_d = (x1 - x2) / pooled_s if pooled_s > 0 else 0.0
    return TestResult(
        test_name="Two-Sample T-Test" + (" (Welch)" if not equal_var else " (Pooled)"),
        statistic=round(t_stat, 6),
        p_value=round(p_value, 8),
        df=round(df, 4),
        alpha=alpha,
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (mu1 = mu2) at alpha={alpha}",
        effect_size=round(cohens_d, 6),
    )


def t_test_paired(data1: list[float], data2: list[float], alpha: float = 0.05, alternative: str = "two-sided") -> TestResult:
    """Paired t-test."""
    if len(data1) != len(data2):
        raise ValueError("Paired samples must have equal length")
    diffs = [a - b for a, b in zip(data1, data2)]
    return t_test_one_sample(diffs, mu0=0.0, alpha=alpha, alternative=alternative)


def chi_square_goodness_of_fit(observed: list[float], expected: list[float], alpha: float = 0.05) -> TestResult:
    """Chi-square goodness-of-fit test."""
    if len(observed) != len(expected):
        raise ValueError("Observed and expected must have same length")
    k = len(observed)
    chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0)
    df = k - 1
    p_value = 1.0 - _chi2_cdf(chi2, df)
    reject = p_value < alpha
    return TestResult(
        test_name="Chi-Square Goodness-of-Fit",
        statistic=round(chi2, 6),
        p_value=round(p_value, 8),
        df=df,
        alpha=alpha,
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (observed matches expected) at alpha={alpha}",
    )


def chi_square_independence(contingency_table: list[list[float]], alpha: float = 0.05) -> TestResult:
    """Chi-square test of independence on a contingency table."""
    rows = len(contingency_table)
    cols = len(contingency_table[0])
    row_totals = [sum(row) for row in contingency_table]
    col_totals = [sum(contingency_table[r][c] for r in range(rows)) for c in range(cols)]
    grand_total = sum(row_totals)
    chi2 = 0.0
    for r in range(rows):
        for c in range(cols):
            expected = row_totals[r] * col_totals[c] / grand_total
            if expected > 0:
                chi2 += (contingency_table[r][c] - expected) ** 2 / expected
    df = (rows - 1) * (cols - 1)
    p_value = 1.0 - _chi2_cdf(chi2, df)
    reject = p_value < alpha
    n = grand_total
    k = min(rows, cols)
    cramers_v = math.sqrt(chi2 / (n * (k - 1))) if n > 0 and k > 1 else 0.0
    return TestResult(
        test_name="Chi-Square Test of Independence",
        statistic=round(chi2, 6),
        p_value=round(p_value, 8),
        df=df,
        alpha=alpha,
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (variables are independent) at alpha={alpha}",
        effect_size=round(cramers_v, 6),
    )


def f_test_two_variances(data1: list[float], data2: list[float], alpha: float = 0.05) -> TestResult:
    """F-test for equality of two variances."""
    s1_sq = compute_variance(data1)
    s2_sq = compute_variance(data2)
    if s2_sq == 0:
        raise ValueError("Second sample has zero variance")
    f_stat = s1_sq / s2_sq
    df1 = len(data1) - 1
    df2 = len(data2) - 1
    if f_stat >= 1.0:
        p_value = 2.0 * (1.0 - _f_cdf(f_stat, df1, df2))
    else:
        p_value = 2.0 * _f_cdf(f_stat, df1, df2)
    p_value = min(p_value, 1.0)
    reject = p_value < alpha
    return TestResult(
        test_name="F-Test for Equality of Variances",
        statistic=round(f_stat, 6),
        p_value=round(p_value, 8),
        df=df1,
        alpha=alpha,
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (sigma1^2 = sigma2^2) at alpha={alpha}",
    )


# ═══════════════════════════════════════════════════════════════════════════
# CONFIDENCE INTERVALS
# ═══════════════════════════════════════════════════════════════════════════

def confidence_interval_z(data: list[float], sigma: float, confidence: float = 0.95) -> dict[str, float]:
    """Confidence interval for mean (known sigma)."""
    n = len(data)
    xbar = compute_mean(data)
    alpha = 1.0 - confidence
    z_crit = _normal_quantile(1.0 - alpha / 2.0)
    margin = z_crit * sigma / math.sqrt(n)
    return {"mean": round(xbar, 6), "lower": round(xbar - margin, 6), "upper": round(xbar + margin, 6), "margin_of_error": round(margin, 6), "confidence": confidence}


def confidence_interval_t(data: list[float], confidence: float = 0.95) -> dict[str, float]:
    """Confidence interval for mean (unknown sigma, uses t-distribution)."""
    n = len(data)
    if n < 2:
        raise ValueError("Need at least 2 observations")
    xbar = compute_mean(data)
    s = compute_std_dev(data)
    se = s / math.sqrt(n)
    alpha = 1.0 - confidence
    df = n - 1
    # approximate t critical via normal for large df, iterative for small
    t_crit = _t_quantile_approx(1.0 - alpha / 2.0, df)
    margin = t_crit * se
    return {"mean": round(xbar, 6), "lower": round(xbar - margin, 6), "upper": round(xbar + margin, 6), "margin_of_error": round(margin, 6), "confidence": confidence, "df": df}


def _t_quantile_approx(p: float, df: float) -> float:
    """Approximate t-quantile using normal approximation with correction."""
    z = _normal_quantile(p)
    # Cornish-Fisher expansion for small df
    g1 = (z ** 3 + z) / (4.0 * df)
    g2 = (5.0 * z ** 5 + 16.0 * z ** 3 + 3.0 * z) / (96.0 * df ** 2)
    g3 = (3.0 * z ** 7 + 19.0 * z ** 5 + 17.0 * z ** 3 - 15.0 * z) / (384.0 * df ** 3)
    return z + g1 + g2 + g3


# ═══════════════════════════════════════════════════════════════════════════
# LINEAR REGRESSION
# ═══════════════════════════════════════════════════════════════════════════

def _matrix_multiply(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Matrix multiplication A * B."""
    rows_a, cols_a = len(a), len(a[0])
    cols_b = len(b[0])
    result = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            s = 0.0
            for k in range(cols_a):
                s += a[i][k] * b[k][j]
            result[i][j] = s
    return result


def _matrix_transpose(m: list[list[float]]) -> list[list[float]]:
    """Matrix transpose."""
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]


def _matrix_inverse(m: list[list[float]]) -> list[list[float]]:
    """Matrix inverse via Gauss-Jordan elimination."""
    n = len(m)
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(m)]
    for col in range(n):
        max_row = col
        for row in range(col + 1, n):
            if abs(aug[row][col]) > abs(aug[max_row][col]):
                max_row = row
        aug[col], aug[max_row] = aug[max_row], aug[col]
        pivot = aug[col][col]
        if abs(pivot) < 1e-15:
            raise ValueError("Matrix is singular, cannot invert")
        for j in range(2 * n):
            aug[col][j] /= pivot
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                for j in range(2 * n):
                    aug[row][j] -= factor * aug[col][j]
    return [row[n:] for row in aug]


class RegressionResult(BaseModel):
    """Linear regression output."""
    coefficients: list[float]
    intercept: float
    r_squared: float
    adjusted_r_squared: float
    residual_std_error: float
    f_statistic: float
    f_p_value: float
    residuals: list[float]
    fitted_values: list[float]
    coefficient_names: list[str]
    n: int
    p: int


def linear_regression(y: list[float], x_matrix: list[list[float]], feature_names: Optional[list[str]] = None) -> RegressionResult:
    """OLS linear regression via normal equations: beta = (X'X)^(-1) X'y."""
    n = len(y)
    if n == 0:
        raise ValueError("Empty dataset")
    p_features = len(x_matrix[0]) if x_matrix and x_matrix[0] else 0
    # add intercept column
    X = [[1.0] + row for row in x_matrix]
    p = p_features + 1  # including intercept
    Xt = _matrix_transpose(X)
    XtX = _matrix_multiply(Xt, X)
    XtX_inv = _matrix_inverse(XtX)
    y_col = [[yi] for yi in y]
    Xty = _matrix_multiply(Xt, y_col)
    beta_col = _matrix_multiply(XtX_inv, Xty)
    beta = [beta_col[i][0] for i in range(p)]
    # fitted values and residuals
    fitted = []
    for i in range(n):
        yhat = sum(X[i][j] * beta[j] for j in range(p))
        fitted.append(yhat)
    residuals = [y[i] - fitted[i] for i in range(n)]
    # R-squared
    y_mean = compute_mean(y)
    ss_tot = sum((yi - y_mean) ** 2 for yi in y)
    ss_res = sum(r ** 2 for r in residuals)
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    adj_r_squared = 1.0 - (1.0 - r_squared) * (n - 1) / (n - p) if n > p else 0.0
    # residual standard error
    rse = math.sqrt(ss_res / (n - p)) if n > p else 0.0
    # F-statistic
    ss_reg = ss_tot - ss_res
    df_reg = p - 1
    df_res = n - p
    ms_reg = ss_reg / df_reg if df_reg > 0 else 0.0
    ms_res = ss_res / df_res if df_res > 0 else 1.0
    f_stat = ms_reg / ms_res if ms_res > 0 else 0.0
    f_p = 1.0 - _f_cdf(f_stat, df_reg, df_res) if df_reg > 0 and df_res > 0 else 1.0
    names = ["intercept"] + (feature_names if feature_names else [f"x{i+1}" for i in range(p_features)])
    return RegressionResult(
        coefficients=[round(b, 8) for b in beta[1:]],
        intercept=round(beta[0], 8),
        r_squared=round(r_squared, 8),
        adjusted_r_squared=round(adj_r_squared, 8),
        residual_std_error=round(rse, 8),
        f_statistic=round(f_stat, 6),
        f_p_value=round(f_p, 8),
        residuals=[round(r, 8) for r in residuals],
        fitted_values=[round(f, 8) for f in fitted],
        coefficient_names=names,
        n=n,
        p=p,
    )


def simple_linear_regression(x: list[float], y: list[float]) -> RegressionResult:
    """Simple linear regression y = a + b*x."""
    x_mat = [[xi] for xi in x]
    return linear_regression(y, x_mat, feature_names=["x"])


# ═══════════════════════════════════════════════════════════════════════════
# CORRELATION
# ═══════════════════════════════════════════════════════════════════════════

def pearson_correlation(x: list[float], y: list[float]) -> dict[str, float]:
    """Pearson product-moment correlation coefficient."""
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Need equal-length data with n>=2")
    x_mean = compute_mean(x)
    y_mean = compute_mean(y)
    cov = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    sx = math.sqrt(sum((xi - x_mean) ** 2 for xi in x))
    sy = math.sqrt(sum((yi - y_mean) ** 2 for yi in y))
    r = cov / (sx * sy) if sx > 0 and sy > 0 else 0.0
    # t-test for significance
    if abs(r) < 1.0:
        t_stat = r * math.sqrt((n - 2) / (1.0 - r * r))
    else:
        t_stat = float('inf') if r > 0 else float('-inf')
    df = n - 2
    p_value = 2.0 * (1.0 - _t_cdf(abs(t_stat), df)) if df > 0 else 0.0
    return {"r": round(r, 8), "r_squared": round(r * r, 8), "t_statistic": round(t_stat, 6), "p_value": round(p_value, 8), "n": n}


def spearman_correlation(x: list[float], y: list[float]) -> dict[str, float]:
    """Spearman rank correlation coefficient."""
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Need equal-length data with n>=2")

    def _rank(data: list[float]) -> list[float]:
        indexed = sorted(enumerate(data), key=lambda t: t[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and indexed[j + 1][1] == indexed[i][1]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[indexed[k][0]] = avg_rank
            i = j + 1
        return ranks

    rx = _rank(x)
    ry = _rank(y)
    return pearson_correlation(rx, ry)


# ═══════════════════════════════════════════════════════════════════════════
# ANOVA
# ═══════════════════════════════════════════════════════════════════════════

class AnovaResult(BaseModel):
    """One-way ANOVA result."""
    f_statistic: float
    p_value: float
    df_between: int
    df_within: int
    ss_between: float
    ss_within: float
    ms_between: float
    ms_within: float
    eta_squared: float
    reject_null: bool
    conclusion: str


def anova_one_way(groups: list[list[float]], alpha: float = 0.05) -> AnovaResult:
    """One-way analysis of variance."""
    k = len(groups)
    if k < 2:
        raise ValueError("Need at least 2 groups")
    all_data = [x for g in groups for x in g]
    grand_mean = compute_mean(all_data)
    n_total = len(all_data)
    # Between-group sum of squares
    ss_between = sum(len(g) * (compute_mean(g) - grand_mean) ** 2 for g in groups)
    # Within-group sum of squares
    ss_within = sum(sum((x - compute_mean(g)) ** 2 for x in g) for g in groups)
    df_between = k - 1
    df_within = n_total - k
    ms_between = ss_between / df_between if df_between > 0 else 0.0
    ms_within = ss_within / df_within if df_within > 0 else 1.0
    f_stat = ms_between / ms_within if ms_within > 0 else 0.0
    p_value = 1.0 - _f_cdf(f_stat, df_between, df_within) if df_between > 0 and df_within > 0 else 1.0
    ss_total = ss_between + ss_within
    eta_sq = ss_between / ss_total if ss_total > 0 else 0.0
    reject = p_value < alpha
    return AnovaResult(
        f_statistic=round(f_stat, 6),
        p_value=round(p_value, 8),
        df_between=df_between,
        df_within=df_within,
        ss_between=round(ss_between, 6),
        ss_within=round(ss_within, 6),
        ms_between=round(ms_between, 6),
        ms_within=round(ms_within, 6),
        eta_squared=round(eta_sq, 6),
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (all group means equal) at alpha={alpha}",
    )


# ═══════════════════════════════════════════════════════════════════════════
# NON-PARAMETRIC TESTS
# ═══════════════════════════════════════════════════════════════════════════

def mann_whitney_u(data1: list[float], data2: list[float], alpha: float = 0.05) -> TestResult:
    """Mann-Whitney U test (Wilcoxon rank-sum test)."""
    n1, n2 = len(data1), len(data2)
    combined = [(v, 0) for v in data1] + [(v, 1) for v in data2]
    combined.sort(key=lambda t: t[0])
    n = n1 + n2
    # assign ranks with tie handling
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and combined[j + 1][0] == combined[i][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[k] = avg_rank
        i = j + 1
    r1 = sum(ranks[i] for i in range(n) if combined[i][1] == 0)
    u1 = r1 - n1 * (n1 + 1) / 2.0
    u2 = n1 * n2 - u1
    u_stat = min(u1, u2)
    # normal approximation for large samples
    mu_u = n1 * n2 / 2.0
    sigma_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12.0)
    z = (u_stat - mu_u) / sigma_u if sigma_u > 0 else 0.0
    p_value = 2.0 * _normal_cdf(z)  # z will be negative
    p_value = min(p_value, 1.0)
    reject = p_value < alpha
    # rank-biserial correlation as effect size
    r_rb = 1.0 - (2.0 * u_stat) / (n1 * n2) if n1 * n2 > 0 else 0.0
    return TestResult(
        test_name="Mann-Whitney U Test",
        statistic=round(u_stat, 6),
        p_value=round(p_value, 8),
        alpha=alpha,
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (distributions equal) at alpha={alpha}",
        effect_size=round(r_rb, 6),
    )


def wilcoxon_signed_rank(data1: list[float], data2: list[float], alpha: float = 0.05) -> TestResult:
    """Wilcoxon signed-rank test for paired samples."""
    if len(data1) != len(data2):
        raise ValueError("Paired samples must have equal length")
    diffs = [a - b for a, b in zip(data1, data2) if a != b]
    n = len(diffs)
    if n == 0:
        return TestResult(test_name="Wilcoxon Signed-Rank", statistic=0.0, p_value=1.0, alpha=alpha, reject_null=False, conclusion="No differences to test")
    abs_diffs = [(abs(d), 1 if d > 0 else -1) for d in diffs]
    abs_diffs.sort(key=lambda t: t[0])
    # rank with ties
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and abs_diffs[j + 1][0] == abs_diffs[i][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[k] = avg_rank
        i = j + 1
    w_plus = sum(ranks[i] for i in range(n) if abs_diffs[i][1] > 0)
    w_minus = sum(ranks[i] for i in range(n) if abs_diffs[i][1] < 0)
    w_stat = min(w_plus, w_minus)
    # normal approximation
    mu_w = n * (n + 1) / 4.0
    sigma_w = math.sqrt(n * (n + 1) * (2 * n + 1) / 24.0)
    z = (w_stat - mu_w) / sigma_w if sigma_w > 0 else 0.0
    p_value = 2.0 * _normal_cdf(z)
    p_value = min(p_value, 1.0)
    reject = p_value < alpha
    return TestResult(
        test_name="Wilcoxon Signed-Rank Test",
        statistic=round(w_stat, 6),
        p_value=round(p_value, 8),
        alpha=alpha,
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (symmetric distribution around 0) at alpha={alpha}",
    )


def kruskal_wallis(groups: list[list[float]], alpha: float = 0.05) -> TestResult:
    """Kruskal-Wallis H test (non-parametric one-way ANOVA)."""
    k = len(groups)
    if k < 2:
        raise ValueError("Need at least 2 groups")
    all_data = []
    for gi, g in enumerate(groups):
        for v in g:
            all_data.append((v, gi))
    all_data.sort(key=lambda t: t[0])
    n = len(all_data)
    # rank with ties
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and all_data[j + 1][0] == all_data[i][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for idx in range(i, j + 1):
            ranks[idx] = avg_rank
        i = j + 1
    group_rank_sums = [0.0] * k
    group_sizes = [len(g) for g in groups]
    for idx in range(n):
        group_rank_sums[all_data[idx][1]] += ranks[idx]
    h_stat = (12.0 / (n * (n + 1))) * sum(group_rank_sums[i] ** 2 / group_sizes[i] for i in range(k)) - 3.0 * (n + 1)
    df = k - 1
    p_value = 1.0 - _chi2_cdf(h_stat, df)
    reject = p_value < alpha
    eta_h = (h_stat - k + 1) / (n - k) if n > k else 0.0
    return TestResult(
        test_name="Kruskal-Wallis H Test",
        statistic=round(h_stat, 6),
        p_value=round(p_value, 8),
        df=df,
        alpha=alpha,
        reject_null=reject,
        conclusion=f"{'Reject' if reject else 'Fail to reject'} H0 (all group distributions equal) at alpha={alpha}",
        effect_size=round(eta_h, 6),
    )


# ═══════════════════════════════════════════════════════════════════════════
# EFFECT SIZE
# ═══════════════════════════════════════════════════════════════════════════

def cohens_d(group1: list[float], group2: list[float]) -> dict[str, Any]:
    """Cohen's d effect size for two groups."""
    n1, n2 = len(group1), len(group2)
    m1, m2 = compute_mean(group1), compute_mean(group2)
    s1, s2 = compute_std_dev(group1), compute_std_dev(group2)
    pooled_s = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
    d = (m1 - m2) / pooled_s if pooled_s > 0 else 0.0
    magnitude = "negligible"
    if abs(d) >= 0.2:
        magnitude = "small"
    if abs(d) >= 0.5:
        magnitude = "medium"
    if abs(d) >= 0.8:
        magnitude = "large"
    return {"d": round(d, 6), "magnitude": magnitude, "pooled_std": round(pooled_s, 6)}


def eta_squared(ss_effect: float, ss_total: float) -> dict[str, float]:
    """Eta-squared effect size."""
    eta2 = ss_effect / ss_total if ss_total > 0 else 0.0
    return {"eta_squared": round(eta2, 6)}


# ═══════════════════════════════════════════════════════════════════════════
# POWER ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

def power_analysis_t_test(effect_size: float, n: int, alpha: float = 0.05, alternative: str = "two-sided") -> dict[str, float]:
    """Statistical power for a one-sample t-test (approximate)."""
    df = n - 1
    ncp = effect_size * math.sqrt(n)  # non-centrality parameter
    if alternative == "two-sided":
        z_crit = _normal_quantile(1.0 - alpha / 2.0)
        power = 1.0 - _normal_cdf(z_crit - ncp) + _normal_cdf(-z_crit - ncp)
    elif alternative == "greater":
        z_crit = _normal_quantile(1.0 - alpha)
        power = 1.0 - _normal_cdf(z_crit - ncp)
    else:
        z_crit = _normal_quantile(alpha)
        power = _normal_cdf(z_crit - ncp)
    return {"power": round(max(0.0, min(1.0, power)), 6), "effect_size": effect_size, "n": n, "alpha": alpha, "alternative": alternative}


def sample_size_for_power(effect_size: float, power: float = 0.80, alpha: float = 0.05) -> dict[str, Any]:
    """Required sample size for desired power (two-sided t-test, approximate)."""
    z_alpha = _normal_quantile(1.0 - alpha / 2.0)
    z_beta = _normal_quantile(power)
    n = math.ceil(((z_alpha + z_beta) / effect_size) ** 2) if effect_size > 0 else float('inf')
    return {"required_n": n, "effect_size": effect_size, "target_power": power, "alpha": alpha}


# ═══════════════════════════════════════════════════════════════════════════
# PROBABILITY DISTRIBUTIONS (PDF/CDF)
# ═══════════════════════════════════════════════════════════════════════════

def distribution_compute(dist_type: str, x: float, params: dict[str, float], calc: str = "both") -> dict[str, Any]:
    """Compute PDF and/or CDF for a specified distribution."""
    result: dict[str, Any] = {"distribution": dist_type, "x": x, "params": params}
    if dist_type == "normal":
        mu = params.get("mu", 0.0)
        sigma = params.get("sigma", 1.0)
        if calc in ("pdf", "both"):
            result["pdf"] = round(_normal_pdf(x, mu, sigma), 10)
        if calc in ("cdf", "both"):
            result["cdf"] = round(_normal_cdf(x, mu, sigma), 10)
    elif dist_type == "t":
        df = params.get("df", 1.0)
        if calc in ("pdf", "both"):
            result["pdf"] = round(_t_pdf(x, df), 10)
        if calc in ("cdf", "both"):
            result["cdf"] = round(_t_cdf(x, df), 10)
    elif dist_type == "chi_square":
        df = params.get("df", 1.0)
        if calc in ("cdf", "both"):
            result["cdf"] = round(_chi2_cdf(x, df), 10)
        if calc in ("pdf", "both"):
            if x > 0:
                pdf_val = (x ** (df / 2.0 - 1.0) * math.exp(-x / 2.0)) / (2.0 ** (df / 2.0) * _gamma_lanczos(df / 2.0))
                result["pdf"] = round(pdf_val, 10)
            else:
                result["pdf"] = 0.0
    elif dist_type == "f":
        df1 = params.get("df1", 1.0)
        df2 = params.get("df2", 1.0)
        if calc in ("cdf", "both"):
            result["cdf"] = round(_f_cdf(x, df1, df2), 10)
        if calc in ("pdf", "both"):
            if x > 0:
                num = math.sqrt((df1 * x) ** df1 * df2 ** df2 / (df1 * x + df2) ** (df1 + df2))
                den = x * _beta_func(df1 / 2.0, df2 / 2.0)
                result["pdf"] = round(num / den, 10) if den > 0 else 0.0
            else:
                result["pdf"] = 0.0
    elif dist_type == "binomial":
        n_trials = int(params.get("n", 10))
        p_success = params.get("p", 0.5)
        k = int(x)
        if calc in ("pdf", "both") or calc in ("pmf", "both"):
            result["pmf"] = round(_binomial_pmf(k, n_trials, p_success), 10)
        if calc in ("cdf", "both"):
            result["cdf"] = round(_binomial_cdf(k, n_trials, p_success), 10)
    elif dist_type == "poisson":
        lam = params.get("lambda", 1.0)
        k = int(x)
        if calc in ("pdf", "both") or calc in ("pmf", "both"):
            result["pmf"] = round(_poisson_pmf(k, lam), 10)
        if calc in ("cdf", "both"):
            result["cdf"] = round(_poisson_cdf(k, lam), 10)
    elif dist_type == "exponential":
        lam = params.get("lambda", 1.0)
        if calc in ("pdf", "both"):
            result["pdf"] = round(_exponential_pdf(x, lam), 10)
        if calc in ("cdf", "both"):
            result["cdf"] = round(_exponential_cdf(x, lam), 10)
    else:
        raise ValueError(f"Unknown distribution: {dist_type}")
    return result


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 1: THREE-LAYER RESPONSE
# ═══════════════════════════════════════════════════════════════════════════

class ResponseLayer(str, Enum):
    DOCTRINE_CACHE = "doctrine_cache"
    SEMANTIC_RETRIEVAL = "semantic_retrieval"
    DEEP_ANALYSIS = "deep_analysis"


class ResponseMode(str, Enum):
    FAST = "fast"
    DEFENSE = "defense"
    MEMO = "memo"


class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 4: AUTHORITY HARDENING
# ═══════════════════════════════════════════════════════════════════════════

AUTHORITY_HIERARCHY: list[dict[str, Any]] = [
    {"level": 1, "source": "mathematical_axiom", "weight": 1.0, "description": "Axioms, definitions, proven theorems"},
    {"level": 2, "source": "statistical_theorem", "weight": 0.95, "description": "Central Limit Theorem, Law of Large Numbers, etc."},
    {"level": 3, "source": "established_method", "weight": 0.90, "description": "Peer-reviewed methodology (OLS, MLE, Bayesian)"},
    {"level": 4, "source": "domain_convention", "weight": 0.80, "description": "Standard alpha=0.05, Cohen's d thresholds"},
    {"level": 5, "source": "practical_guideline", "weight": 0.70, "description": "Rule of thumb (n>30 for CLT, etc.)"},
    {"level": 6, "source": "expert_opinion", "weight": 0.55, "description": "Textbook recommendation without formal proof"},
]


def resolve_authority_conflict(sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Resolve conflict between authorities by weight."""
    if not sources:
        return {"resolution": "no_sources", "weight": 0.0}
    sorted_sources = sorted(sources, key=lambda s: s.get("weight", 0), reverse=True)
    winner = sorted_sources[0]
    return {
        "resolution": winner["source"],
        "weight": winner["weight"],
        "overruled": [s["source"] for s in sorted_sources[1:]],
    }


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 5: CONFIDENCE STRATIFICATION
# ═══════════════════════════════════════════════════════════════════════════

def stratify_confidence(p_value: float, effect_size: float, sample_size: int) -> dict[str, Any]:
    """Classify result confidence based on statistical evidence."""
    if p_value < 0.001 and abs(effect_size) >= 0.8 and sample_size >= 30:
        level = ConfidenceLevel.DEFENSIBLE
        reasoning = "Strong statistical significance, large effect size, adequate sample"
    elif p_value < 0.05 and abs(effect_size) >= 0.2:
        level = ConfidenceLevel.AGGRESSIVE
        reasoning = "Statistically significant but may lack practical significance or power"
    elif p_value < 0.10:
        level = ConfidenceLevel.DISCLOSURE
        reasoning = "Marginal significance; disclose limitations and consider larger sample"
    else:
        level = ConfidenceLevel.HIGH_RISK
        reasoning = "Insufficient evidence; risk of Type II error or negligible effect"
    return {
        "level": level.value,
        "reasoning": reasoning,
        "p_value": p_value,
        "effect_size": effect_size,
        "sample_size": sample_size,
    }


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 6: SEMANTIC NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════════

_SEMANTIC_MAP: dict[str, str] = {}


def _load_semantic_dict() -> None:
    """Load semantic dictionary from JSON file."""
    global _SEMANTIC_MAP
    if SEMANTIC_DICT_PATH.exists():
        with open(SEMANTIC_DICT_PATH, "r", encoding="utf-8") as f:
            _SEMANTIC_MAP = json.load(f)
    else:
        logger.warning("semantic_dict.json not found, using empty map")


def normalize_term(term: str) -> str:
    """Normalize a statistical term to its canonical form."""
    if not _SEMANTIC_MAP:
        _load_semantic_dict()
    lower = term.strip().lower()
    return _SEMANTIC_MAP.get(lower, lower)


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 7: VECTOR SEARCH (simplified in-memory)
# ═══════════════════════════════════════════════════════════════════════════

def _jaccard_similarity(a: set[str], b: set[str]) -> float:
    """Jaccard similarity between two sets."""
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def vector_search_doctrines(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Search doctrine cache by keyword overlap."""
    query_tokens = set(query.lower().split())
    results = []
    for doctrine in _DOCTRINE_CACHE:
        kw_set = set(k.lower() for k in doctrine.get("keywords", []))
        topic_tokens = set(doctrine.get("topic", "").lower().split())
        combined = kw_set | topic_tokens
        score = _jaccard_similarity(query_tokens, combined)
        if score > 0:
            results.append({"doctrine": doctrine["topic"], "score": round(score, 4), "conclusion": doctrine.get("conclusion_template", "")})
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_k]


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 8: TELEMETRY
# ═══════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    """Query telemetry for latency, errors, and throughput."""

    def __init__(self) -> None:
        self.queries: list[dict[str, Any]] = []
        self.start_time: float = time.time()
        self.error_count: int = 0
        self.total_count: int = 0

    def record_query(self, query_id: str, operation: str, latency_ms: float, success: bool, layer: str) -> None:
        """Record a single query event."""
        self.total_count += 1
        if not success:
            self.error_count += 1
        self.queries.append({
            "query_id": query_id,
            "operation": operation,
            "latency_ms": round(latency_ms, 3),
            "success": success,
            "layer": layer,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def get_stats(self) -> dict[str, Any]:
        """Return aggregated telemetry stats."""
        uptime = time.time() - self.start_time
        latencies = [q["latency_ms"] for q in self.queries if q["success"]]
        return {
            "total_queries": self.total_count,
            "error_count": self.error_count,
            "error_rate": round(self.error_count / max(self.total_count, 1), 4),
            "uptime_seconds": round(uptime, 1),
            "queries_per_minute": round(self.total_count / max(uptime / 60, 0.01), 2),
            "avg_latency_ms": round(sum(latencies) / max(len(latencies), 1), 3),
            "p95_latency_ms": round(compute_percentile(latencies, 95), 3) if len(latencies) >= 2 else 0.0,
            "max_latency_ms": round(max(latencies), 3) if latencies else 0.0,
        }


TELEMETRY = TelemetryCollector()


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 9: DRIFT WATCHER
# ═══════════════════════════════════════════════════════════════════════════

class DriftWatcher:
    """Detect doctrine drift over time."""

    def __init__(self) -> None:
        self.baseline_hashes: dict[str, str] = {}
        self.drift_events: list[dict[str, Any]] = []

    def set_baseline(self, doctrine_id: str, content_hash: str) -> None:
        """Set baseline hash for a doctrine."""
        self.baseline_hashes[doctrine_id] = content_hash

    def check_drift(self, doctrine_id: str, current_hash: str) -> bool:
        """Check if doctrine has drifted from baseline."""
        baseline = self.baseline_hashes.get(doctrine_id)
        if baseline is None:
            self.set_baseline(doctrine_id, current_hash)
            return False
        if current_hash != baseline:
            self.drift_events.append({
                "doctrine_id": doctrine_id,
                "old_hash": baseline,
                "new_hash": current_hash,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return True
        return False

    def get_drift_report(self) -> dict[str, Any]:
        """Return all drift events."""
        return {
            "total_baselines": len(self.baseline_hashes),
            "drift_events": len(self.drift_events),
            "events": self.drift_events[-50:],
        }


DRIFT_WATCHER = DriftWatcher()


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 10: COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════

class CoverageTracker:
    """Track which doctrines are triggered and which have gaps."""

    def __init__(self) -> None:
        self.triggered: dict[str, int] = {}
        self.missed: list[str] = []

    def record_hit(self, doctrine_topic: str) -> None:
        """Record a doctrine cache hit."""
        self.triggered[doctrine_topic] = self.triggered.get(doctrine_topic, 0) + 1

    def record_miss(self, query: str) -> None:
        """Record a query that missed all doctrines."""
        self.missed.append(query)

    def get_coverage(self) -> dict[str, Any]:
        """Return coverage report."""
        total_doctrines = len(_DOCTRINE_CACHE)
        triggered_count = len(self.triggered)
        return {
            "total_doctrines": total_doctrines,
            "triggered_count": triggered_count,
            "coverage_pct": round(100.0 * triggered_count / max(total_doctrines, 1), 1),
            "top_triggered": sorted(self.triggered.items(), key=lambda t: t[1], reverse=True)[:10],
            "recent_misses": self.missed[-20:],
            "epistemic_gaps": len(self.missed),
        }


COVERAGE = CoverageTracker()


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 11: METRICS COLLECTOR
# ═══════════════════════════════════════════════════════════════════════════

class MetricsCollector:
    """Aggregate operational metrics."""

    def __init__(self) -> None:
        self.operation_counts: dict[str, int] = {}
        self.latencies_by_op: dict[str, list[float]] = {}
        self.start_time: float = time.time()

    def record(self, operation: str, latency_ms: float) -> None:
        """Record an operation."""
        self.operation_counts[operation] = self.operation_counts.get(operation, 0) + 1
        self.latencies_by_op.setdefault(operation, []).append(latency_ms)

    def summary(self) -> dict[str, Any]:
        """Return metrics summary."""
        uptime = time.time() - self.start_time
        total = sum(self.operation_counts.values())
        op_stats = {}
        for op, lats in self.latencies_by_op.items():
            op_stats[op] = {
                "count": self.operation_counts[op],
                "avg_ms": round(sum(lats) / len(lats), 3),
                "max_ms": round(max(lats), 3),
            }
        return {
            "uptime_seconds": round(uptime, 1),
            "total_operations": total,
            "operations_per_minute": round(total / max(uptime / 60, 0.01), 2),
            "by_operation": op_stats,
        }


METRICS = MetricsCollector()


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 13: ZONED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

def apply_zone(zone: PositionZone, result: dict[str, Any]) -> dict[str, Any]:
    """Apply position zone restrictions to a result."""
    result["position_zone"] = zone.value
    if zone == PositionZone.PLANNING:
        result["zone_note"] = "Planning zone: forward-looking estimates, not final conclusions"
    elif zone == PositionZone.REPORTING:
        result["zone_note"] = "Reporting zone: observed results, report as-is without advocacy"
    elif zone == PositionZone.AUDIT:
        result["zone_note"] = "Audit zone: all assumptions and limitations must be explicitly stated"
    return result


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 14: FACT FRAGILITY SCORING
# ═══════════════════════════════════════════════════════════════════════════

def fact_fragility_score(p_value: float, sample_size: int, assumptions_met: bool, replication_count: int = 0) -> dict[str, Any]:
    """Score the fragility of a statistical finding."""
    score = 0.0
    factors = []
    # p-value proximity to threshold
    if p_value > 0.04 and p_value < 0.06:
        score += 0.3
        factors.append("p-value near 0.05 boundary (fragile)")
    elif p_value > 0.01:
        score += 0.15
        factors.append("p-value above 0.01 (moderate fragility)")
    # sample size
    if sample_size < 30:
        score += 0.25
        factors.append(f"Small sample (n={sample_size})")
    elif sample_size < 100:
        score += 0.1
        factors.append("Moderate sample size")
    # assumptions
    if not assumptions_met:
        score += 0.3
        factors.append("Statistical assumptions may be violated")
    # replication
    if replication_count == 0:
        score += 0.15
        factors.append("No independent replication")
    elif replication_count >= 3:
        score -= 0.1
        factors.append(f"Replicated {replication_count} times (robust)")
    score = max(0.0, min(1.0, score))
    fragility = "low" if score < 0.3 else ("moderate" if score < 0.6 else "high")
    return {"fragility_score": round(score, 4), "fragility_level": fragility, "factors": factors}


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 15: AUDIT TRAIL
# ═══════════════════════════════════════════════════════════════════════════

def _write_audit_entry(entry: dict[str, Any]) -> None:
    """Append an entry to the JSONL audit trail."""
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    entry["engine"] = ENGINE_ID
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 16: DETERMINISM HASH
# ═══════════════════════════════════════════════════════════════════════════

def compute_determinism_hash(data: Any) -> str:
    """SHA-256 hash for reproducibility verification."""
    serialized = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 19: MULTI-DOCTRINE DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════

class IssueCategory(str, Enum):
    DESCRIPTIVE = "descriptive_statistics"
    INFERENTIAL = "inferential_testing"
    REGRESSION = "regression_analysis"
    CORRELATION = "correlation_analysis"
    ANOVA_COMPARISON = "anova_comparison"
    DISTRIBUTION = "probability_distribution"
    NON_PARAMETRIC = "non_parametric"
    EFFECT_SIZE = "effect_size_analysis"
    POWER = "power_analysis"
    BAYESIAN = "bayesian_inference"


INTERACTION_EDGES: list[dict[str, str]] = [
    {"from": "descriptive_statistics", "to": "inferential_testing", "reason": "Descriptive stats inform test selection"},
    {"from": "descriptive_statistics", "to": "regression_analysis", "reason": "Outlier detection affects regression"},
    {"from": "inferential_testing", "to": "effect_size_analysis", "reason": "Significance requires effect size context"},
    {"from": "inferential_testing", "to": "power_analysis", "reason": "Non-significant results need power assessment"},
    {"from": "regression_analysis", "to": "correlation_analysis", "reason": "Regression coefficients relate to correlation"},
    {"from": "anova_comparison", "to": "non_parametric", "reason": "ANOVA assumption violations trigger non-parametric"},
    {"from": "probability_distribution", "to": "inferential_testing", "reason": "Test statistics follow known distributions"},
    {"from": "correlation_analysis", "to": "regression_analysis", "reason": "Correlation motivates regression modeling"},
    {"from": "power_analysis", "to": "inferential_testing", "reason": "Power determines test feasibility"},
    {"from": "non_parametric", "to": "effect_size_analysis", "reason": "Non-parametric tests need appropriate effect sizes"},
]


def decompose_query(query: str) -> list[dict[str, Any]]:
    """Decompose a statistical query into issue categories."""
    query_lower = query.lower()
    categories = []
    keyword_map = {
        IssueCategory.DESCRIPTIVE: ["mean", "median", "mode", "variance", "std", "skew", "kurtosis", "quartile", "percentile", "descriptive", "summary"],
        IssueCategory.INFERENTIAL: ["test", "hypothesis", "p-value", "significance", "reject", "null", "z-test", "t-test", "chi-square"],
        IssueCategory.REGRESSION: ["regression", "predict", "ols", "coefficient", "r-squared", "linear model", "slope", "intercept"],
        IssueCategory.CORRELATION: ["correlation", "pearson", "spearman", "kendall", "association", "relationship"],
        IssueCategory.ANOVA_COMPARISON: ["anova", "group comparison", "between groups", "factor", "one-way"],
        IssueCategory.DISTRIBUTION: ["distribution", "normal", "binomial", "poisson", "exponential", "pdf", "cdf", "probability"],
        IssueCategory.NON_PARAMETRIC: ["mann-whitney", "wilcoxon", "kruskal", "non-parametric", "rank", "nonparametric"],
        IssueCategory.EFFECT_SIZE: ["effect size", "cohen", "eta squared", "practical significance"],
        IssueCategory.POWER: ["power", "sample size", "type ii", "beta error"],
    }
    for cat, keywords in keyword_map.items():
        matched = [kw for kw in keywords if kw in query_lower]
        if matched:
            categories.append({"category": cat.value, "matched_keywords": matched, "confidence": min(1.0, len(matched) * 0.3 + 0.2)})
    if not categories:
        categories.append({"category": IssueCategory.DESCRIPTIVE.value, "matched_keywords": [], "confidence": 0.1})
    # add interaction edges
    active_cats = {c["category"] for c in categories}
    relevant_edges = [e for e in INTERACTION_EDGES if e["from"] in active_cats or e["to"] in active_cats]
    return categories


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 20: DEEP ANALYSIS MODE
# ═══════════════════════════════════════════════════════════════════════════

def deep_analysis(data: list[float], groups: Optional[list[list[float]]] = None) -> dict[str, Any]:
    """Full deep analysis: descriptive + normality check + recommended tests."""
    result: dict[str, Any] = {"layer": "deep_analysis"}
    # Descriptive
    desc = descriptive_stats(data)
    result["descriptive"] = desc
    # Normality heuristic (skewness/kurtosis)
    n = len(data)
    normality_assessment = "unknown"
    if n >= 4:
        skew = desc.get("skewness", 0) or 0
        kurt = desc.get("excess_kurtosis", 0) or 0
        if abs(skew) < 0.5 and abs(kurt) < 1.0:
            normality_assessment = "approximately_normal"
        elif abs(skew) < 1.0 and abs(kurt) < 3.0:
            normality_assessment = "mildly_non_normal"
        else:
            normality_assessment = "non_normal"
    result["normality_assessment"] = normality_assessment
    # Recommendations
    recs = []
    if n < 30:
        recs.append("Small sample (n<30): use t-tests or non-parametric methods")
    if normality_assessment == "non_normal":
        recs.append("Non-normal data detected: consider Mann-Whitney U or Wilcoxon instead of t-test")
    if n >= 30:
        recs.append("Adequate sample for CLT: z-tests appropriate if population sigma known")
    if groups and len(groups) >= 2:
        recs.append("Multiple groups: use ANOVA (parametric) or Kruskal-Wallis (non-parametric)")
    result["recommendations"] = recs
    # Effect size guidance
    result["effect_size_guide"] = {
        "cohens_d": {"small": 0.2, "medium": 0.5, "large": 0.8},
        "eta_squared": {"small": 0.01, "medium": 0.06, "large": 0.14},
        "r": {"small": 0.1, "medium": 0.3, "large": 0.5},
    }
    result["determinism_hash"] = compute_determinism_hash(result)
    return result


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE LOADING
# ═══════════════════════════════════════════════════════════════════════════

_DOCTRINE_CACHE: list[dict[str, Any]] = []


def _load_doctrine_cache() -> None:
    """Load doctrine cache from JSON file."""
    global _DOCTRINE_CACHE
    if DOCTRINE_CACHE_PATH.exists():
        with open(DOCTRINE_CACHE_PATH, "r", encoding="utf-8") as f:
            _DOCTRINE_CACHE = json.load(f)
        logger.info(f"Loaded {len(_DOCTRINE_CACHE)} doctrine blocks")
        for d in _DOCTRINE_CACHE:
            h = compute_determinism_hash(d)
            DRIFT_WATCHER.set_baseline(d["topic"], h)
    else:
        logger.warning("doctrine_cache.json not found")


def doctrine_lookup(query: str) -> Optional[dict[str, Any]]:
    """Fast doctrine cache lookup by keyword matching."""
    query_tokens = set(query.lower().split())
    best_match: Optional[dict[str, Any]] = None
    best_score = 0.0
    for doctrine in _DOCTRINE_CACHE:
        kw_set = set(k.lower() for k in doctrine.get("keywords", []))
        overlap = len(query_tokens & kw_set)
        if overlap > best_score:
            best_score = overlap
            best_match = doctrine
    if best_match and best_score > 0:
        COVERAGE.record_hit(best_match["topic"])
        return best_match
    COVERAGE.record_miss(query)
    return None


# ═══════════════════════════════════════════════════════════════════════════
# THREE-LAYER RESPONSE ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════

def three_layer_response(query: str, data: Optional[list[float]] = None, mode: ResponseMode = ResponseMode.FAST) -> dict[str, Any]:
    """TIE-20 three-layer response: doctrine cache -> semantic -> deep analysis."""
    start = time.time()
    query_id = str(uuid.uuid4())[:12]
    result: dict[str, Any] = {"query_id": query_id, "query": query, "mode": mode.value}
    # Layer 1: Doctrine Cache (target 0-200ms)
    doctrine = doctrine_lookup(query)
    if doctrine:
        result["layer"] = ResponseLayer.DOCTRINE_CACHE.value
        result["doctrine"] = doctrine["topic"]
        result["conclusion"] = doctrine.get("conclusion_template", "")
        result["confidence_stratification"] = doctrine.get("confidence_stratification", "DEFENSIBLE")
        latency = (time.time() - start) * 1000
        result["latency_ms"] = round(latency, 3)
        TELEMETRY.record_query(query_id, "doctrine_lookup", latency, True, "doctrine_cache")
        METRICS.record("doctrine_lookup", latency)
        _write_audit_entry({"query_id": query_id, "operation": "three_layer_response", "layer": "doctrine_cache", "query": query})
        result["determinism_hash"] = compute_determinism_hash(result)
        return result
    # Layer 2: Semantic Retrieval
    semantic_results = vector_search_doctrines(query, top_k=3)
    if semantic_results and semantic_results[0]["score"] > 0.1:
        result["layer"] = ResponseLayer.SEMANTIC_RETRIEVAL.value
        result["semantic_matches"] = semantic_results
        result["conclusion"] = semantic_results[0]["conclusion"]
        latency = (time.time() - start) * 1000
        result["latency_ms"] = round(latency, 3)
        TELEMETRY.record_query(query_id, "semantic_search", latency, True, "semantic_retrieval")
        METRICS.record("semantic_search", latency)
        _write_audit_entry({"query_id": query_id, "operation": "three_layer_response", "layer": "semantic_retrieval", "query": query})
        result["determinism_hash"] = compute_determinism_hash(result)
        return result
    # Layer 3: Deep Analysis
    result["layer"] = ResponseLayer.DEEP_ANALYSIS.value
    if data:
        result["analysis"] = deep_analysis(data)
    else:
        categories = decompose_query(query)
        result["decomposition"] = categories
        result["note"] = "Provide data for full statistical computation"
    latency = (time.time() - start) * 1000
    result["latency_ms"] = round(latency, 3)
    TELEMETRY.record_query(query_id, "deep_analysis", latency, True, "deep_analysis")
    METRICS.record("deep_analysis", latency)
    _write_audit_entry({"query_id": query_id, "operation": "three_layer_response", "layer": "deep_analysis", "query": query})
    result["determinism_hash"] = compute_determinism_hash(result)
    return result


# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════

class DataRequest(BaseModel):
    data: list[float] = Field(..., min_length=1, description="Numeric dataset")


class TwoSampleRequest(BaseModel):
    data1: list[float] = Field(..., min_length=2)
    data2: list[float] = Field(..., min_length=2)
    alpha: float = Field(default=0.05, ge=0.001, le=0.5)
    alternative: str = Field(default="two-sided")


class OneSampleTTestRequest(BaseModel):
    data: list[float] = Field(..., min_length=2)
    mu0: float = Field(..., description="Hypothesized population mean")
    alpha: float = Field(default=0.05)
    alternative: str = Field(default="two-sided")


class ZTestRequest(BaseModel):
    data: list[float] = Field(..., min_length=1)
    mu0: float
    sigma: float = Field(..., gt=0)
    alpha: float = Field(default=0.05)
    alternative: str = Field(default="two-sided")


class ChiSquareGOFRequest(BaseModel):
    observed: list[float]
    expected: list[float]
    alpha: float = Field(default=0.05)


class ChiSquareIndRequest(BaseModel):
    contingency_table: list[list[float]]
    alpha: float = Field(default=0.05)


class RegressionRequest(BaseModel):
    y: list[float]
    x_matrix: list[list[float]]
    feature_names: Optional[list[str]] = None


class SimpleRegressionRequest(BaseModel):
    x: list[float]
    y: list[float]


class CorrelationRequest(BaseModel):
    x: list[float]
    y: list[float]


class AnovaRequest(BaseModel):
    groups: list[list[float]]
    alpha: float = Field(default=0.05)


class DistributionRequest(BaseModel):
    dist_type: str
    x: float
    params: dict[str, float]
    calc: str = Field(default="both")


class PowerRequest(BaseModel):
    effect_size: float = Field(..., gt=0)
    n: int = Field(..., gt=1)
    alpha: float = Field(default=0.05)
    alternative: str = Field(default="two-sided")


class SampleSizeRequest(BaseModel):
    effect_size: float = Field(..., gt=0)
    power: float = Field(default=0.80, ge=0.5, le=0.999)
    alpha: float = Field(default=0.05)


class ConfidenceIntervalZRequest(BaseModel):
    data: list[float]
    sigma: float = Field(..., gt=0)
    confidence: float = Field(default=0.95)


class ConfidenceIntervalTRequest(BaseModel):
    data: list[float] = Field(..., min_length=2)
    confidence: float = Field(default=0.95)


class QueryRequest(BaseModel):
    query: str
    data: Optional[list[float]] = None
    mode: str = Field(default="fast")


class EffectSizeRequest(BaseModel):
    group1: list[float]
    group2: list[float]


class FragilityRequest(BaseModel):
    p_value: float
    sample_size: int
    assumptions_met: bool = True
    replication_count: int = 0


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION (TIE COMPONENT 17)
# ═══════════════════════════════════════════════════════════════════════════

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    logger.info(f"MATH05 Statistics Engine v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    _load_doctrine_cache()
    _load_semantic_dict()
    yield
    logger.info("MATH05 shutting down")


app = FastAPI(
    title=ENGINE_NAME,
    version=ENGINE_VERSION,
    description="TIE-20 compliant statistics intelligence engine with pure Python math implementations",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════════════
# TIE COMPONENT 12: HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check() -> dict[str, Any]:
    """Comprehensive health check."""
    return {
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "status": "healthy",
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "domain": ENGINE_DOMAIN,
        "mode": ENGINE_MODE,
        "auth_level": ENGINE_AUTH_LEVEL,
        "uptime_seconds": round(time.time() - TELEMETRY.start_time, 1),
        "telemetry": TELEMETRY.get_stats(),
        "metrics": METRICS.summary(),
        "coverage": COVERAGE.get_coverage(),
        "drift": DRIFT_WATCHER.get_drift_report(),
        "doctrines_loaded": len(_DOCTRINE_CACHE),
        "semantic_terms_loaded": len(_SEMANTIC_MAP),
        "tie_components": 20,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# --- Descriptive Stats ---
@app.post("/stats/descriptive")
async def api_descriptive(req: DataRequest) -> dict[str, Any]:
    """Full descriptive statistics."""
    start = time.time()
    result = descriptive_stats(req.data)
    result["determinism_hash"] = compute_determinism_hash(result)
    METRICS.record("descriptive_stats", (time.time() - start) * 1000)
    _write_audit_entry({"operation": "descriptive_stats", "n": len(req.data)})
    return result


# --- Hypothesis Tests ---
@app.post("/test/z-test")
async def api_z_test(req: ZTestRequest) -> dict[str, Any]:
    """One-sample z-test."""
    start = time.time()
    result = z_test_one_sample(req.data, req.mu0, req.sigma, req.alpha, req.alternative)
    METRICS.record("z_test", (time.time() - start) * 1000)
    _write_audit_entry({"operation": "z_test", "mu0": req.mu0, "n": len(req.data)})
    return result.model_dump()


@app.post("/test/t-test/one-sample")
async def api_t_test_one(req: OneSampleTTestRequest) -> dict[str, Any]:
    """One-sample t-test."""
    start = time.time()
    result = t_test_one_sample(req.data, req.mu0, req.alpha, req.alternative)
    METRICS.record("t_test_one", (time.time() - start) * 1000)
    _write_audit_entry({"operation": "t_test_one_sample", "mu0": req.mu0, "n": len(req.data)})
    return result.model_dump()


@app.post("/test/t-test/two-sample")
async def api_t_test_two(req: TwoSampleRequest) -> dict[str, Any]:
    """Two-sample t-test."""
    start = time.time()
    result = t_test_two_sample(req.data1, req.data2, req.alpha, alternative=req.alternative)
    METRICS.record("t_test_two", (time.time() - start) * 1000)
    return result.model_dump()


@app.post("/test/t-test/paired")
async def api_t_test_paired(req: TwoSampleRequest) -> dict[str, Any]:
    """Paired t-test."""
    start = time.time()
    result = t_test_paired(req.data1, req.data2, req.alpha, req.alternative)
    METRICS.record("t_test_paired", (time.time() - start) * 1000)
    return result.model_dump()


@app.post("/test/chi-square/goodness-of-fit")
async def api_chi2_gof(req: ChiSquareGOFRequest) -> dict[str, Any]:
    """Chi-square goodness-of-fit."""
    start = time.time()
    result = chi_square_goodness_of_fit(req.observed, req.expected, req.alpha)
    METRICS.record("chi2_gof", (time.time() - start) * 1000)
    return result.model_dump()


@app.post("/test/chi-square/independence")
async def api_chi2_ind(req: ChiSquareIndRequest) -> dict[str, Any]:
    """Chi-square independence."""
    start = time.time()
    result = chi_square_independence(req.contingency_table, req.alpha)
    METRICS.record("chi2_ind", (time.time() - start) * 1000)
    return result.model_dump()


@app.post("/test/f-test")
async def api_f_test(req: TwoSampleRequest) -> dict[str, Any]:
    """F-test for equality of variances."""
    start = time.time()
    result = f_test_two_variances(req.data1, req.data2, req.alpha)
    METRICS.record("f_test", (time.time() - start) * 1000)
    return result.model_dump()


@app.post("/test/mann-whitney")
async def api_mann_whitney(req: TwoSampleRequest) -> dict[str, Any]:
    """Mann-Whitney U test."""
    start = time.time()
    result = mann_whitney_u(req.data1, req.data2, req.alpha)
    METRICS.record("mann_whitney", (time.time() - start) * 1000)
    return result.model_dump()


@app.post("/test/wilcoxon")
async def api_wilcoxon(req: TwoSampleRequest) -> dict[str, Any]:
    """Wilcoxon signed-rank test."""
    start = time.time()
    result = wilcoxon_signed_rank(req.data1, req.data2, req.alpha)
    METRICS.record("wilcoxon", (time.time() - start) * 1000)
    return result.model_dump()


@app.post("/test/kruskal-wallis")
async def api_kruskal(req: AnovaRequest) -> dict[str, Any]:
    """Kruskal-Wallis H test."""
    start = time.time()
    result = kruskal_wallis(req.groups, req.alpha)
    METRICS.record("kruskal_wallis", (time.time() - start) * 1000)
    return result.model_dump()


# --- Confidence Intervals ---
@app.post("/ci/z-interval")
async def api_ci_z(req: ConfidenceIntervalZRequest) -> dict[str, Any]:
    """Z-based confidence interval."""
    return confidence_interval_z(req.data, req.sigma, req.confidence)


@app.post("/ci/t-interval")
async def api_ci_t(req: ConfidenceIntervalTRequest) -> dict[str, Any]:
    """T-based confidence interval."""
    return confidence_interval_t(req.data, req.confidence)


# --- Regression ---
@app.post("/regression/linear")
async def api_regression(req: RegressionRequest) -> dict[str, Any]:
    """Multiple linear regression."""
    start = time.time()
    result = linear_regression(req.y, req.x_matrix, req.feature_names)
    METRICS.record("linear_regression", (time.time() - start) * 1000)
    _write_audit_entry({"operation": "linear_regression", "n": len(req.y), "p": len(req.x_matrix[0]) if req.x_matrix else 0})
    return result.model_dump()


@app.post("/regression/simple")
async def api_simple_regression(req: SimpleRegressionRequest) -> dict[str, Any]:
    """Simple linear regression."""
    start = time.time()
    result = simple_linear_regression(req.x, req.y)
    METRICS.record("simple_regression", (time.time() - start) * 1000)
    return result.model_dump()


# --- Correlation ---
@app.post("/correlation/pearson")
async def api_pearson(req: CorrelationRequest) -> dict[str, Any]:
    """Pearson correlation."""
    start = time.time()
    result = pearson_correlation(req.x, req.y)
    METRICS.record("pearson", (time.time() - start) * 1000)
    return result


@app.post("/correlation/spearman")
async def api_spearman(req: CorrelationRequest) -> dict[str, Any]:
    """Spearman correlation."""
    start = time.time()
    result = spearman_correlation(req.x, req.y)
    METRICS.record("spearman", (time.time() - start) * 1000)
    return result


# --- ANOVA ---
@app.post("/anova/one-way")
async def api_anova(req: AnovaRequest) -> dict[str, Any]:
    """One-way ANOVA."""
    start = time.time()
    result = anova_one_way(req.groups, req.alpha)
    METRICS.record("anova_one_way", (time.time() - start) * 1000)
    return result.model_dump()


# --- Distributions ---
@app.post("/distribution/compute")
async def api_distribution(req: DistributionRequest) -> dict[str, Any]:
    """Compute PDF/CDF for a distribution."""
    start = time.time()
    result = distribution_compute(req.dist_type, req.x, req.params, req.calc)
    METRICS.record("distribution_compute", (time.time() - start) * 1000)
    return result


# --- Effect Size ---
@app.post("/effect-size/cohens-d")
async def api_cohens_d(req: EffectSizeRequest) -> dict[str, Any]:
    """Cohen's d effect size."""
    return cohens_d(req.group1, req.group2)


# --- Power Analysis ---
@app.post("/power/t-test")
async def api_power(req: PowerRequest) -> dict[str, Any]:
    """Power analysis for t-test."""
    return power_analysis_t_test(req.effect_size, req.n, req.alpha, req.alternative)


@app.post("/power/sample-size")
async def api_sample_size(req: SampleSizeRequest) -> dict[str, Any]:
    """Required sample size calculation."""
    return sample_size_for_power(req.effect_size, req.power, req.alpha)


# --- Fragility ---
@app.post("/fragility")
async def api_fragility(req: FragilityRequest) -> dict[str, Any]:
    """Fact fragility score."""
    return fact_fragility_score(req.p_value, req.sample_size, req.assumptions_met, req.replication_count)


# --- Three-Layer Query ---
@app.post("/query")
async def api_query(req: QueryRequest) -> dict[str, Any]:
    """TIE-20 three-layer response."""
    mode_map = {"fast": ResponseMode.FAST, "defense": ResponseMode.DEFENSE, "memo": ResponseMode.MEMO}
    rm = mode_map.get(req.mode, ResponseMode.FAST)
    return three_layer_response(req.query, req.data, rm)


# --- Telemetry/Metrics/Coverage/Drift ---
@app.get("/telemetry")
async def api_telemetry() -> dict[str, Any]:
    """Telemetry stats."""
    return TELEMETRY.get_stats()


@app.get("/metrics")
async def api_metrics() -> dict[str, Any]:
    """Metrics summary."""
    return METRICS.summary()


@app.get("/coverage")
async def api_coverage() -> dict[str, Any]:
    """Coverage map."""
    return COVERAGE.get_coverage()


@app.get("/drift")
async def api_drift() -> dict[str, Any]:
    """Drift report."""
    return DRIFT_WATCHER.get_drift_report()


@app.get("/doctrines")
async def api_doctrines() -> list[dict[str, Any]]:
    """List all doctrine blocks."""
    return _DOCTRINE_CACHE


@app.post("/normalize")
async def api_normalize(term: str) -> dict[str, str]:
    """Normalize a statistical term."""
    return {"original": term, "normalized": normalize_term(term)}


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Launching {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
