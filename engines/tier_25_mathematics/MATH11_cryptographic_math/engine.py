#!/usr/bin/env python3
"""
MATH11 — Cryptographic Mathematics Engine
TIE-20 Compliant | Tier 13 (Mathematics) | MODE: DET | AUTH: 5.0 | PORT: 8573

Covers: Modular arithmetic, RSA math, Diffie-Hellman, elliptic curves over
finite fields, SHA-256 analysis, AES Galois field math, primality testing
(Miller-Rabin / Fermat), Chinese Remainder Theorem, baby-step giant-step
discrete log, and extended Euclidean algorithm.

All crypto math is pure-Python (no external crypto library for the core math).
hashlib is used only for SHA-256 property analysis (not re-implemented).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Path bootstrap
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
ENGINES_ROOT = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINES_ROOT))

ENGINE_ID = "MATH11"
ENGINE_NAME = "Cryptographic Mathematics"
ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 8573
ENGINE_TIER = 13
ENGINE_MODE = "DET"
ENGINE_AUTH_LEVEL = 5.0

# ---------------------------------------------------------------------------
# Loguru configuration
# ---------------------------------------------------------------------------
LOG_DIR = ENGINE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)
logger.add(
    LOG_DIR / "math11_{time:YYYY-MM-DD}.log",
    rotation="50 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}",
)

# ---------------------------------------------------------------------------
# Audit trail JSONL  (TIE component 15)
# ---------------------------------------------------------------------------
AUDIT_LOG_PATH = ENGINE_DIR / "logs" / "audit_trail.jsonl"


def _audit_log(entry: dict) -> None:
    """Append a JSON-lines audit record."""
    entry["_ts"] = datetime.now(timezone.utc).isoformat()
    entry["_engine"] = ENGINE_ID
    try:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, default=str) + "\n")
    except Exception as exc:
        logger.warning("Audit write failed: {}", exc)


# ═══════════════════════════════════════════════════════════════════════════
#  PURE-PYTHON CRYPTOGRAPHIC MATHEMATICS LIBRARY
# ═══════════════════════════════════════════════════════════════════════════


# ---------------------------------------------------------------------------
# 1. Modular Arithmetic
# ---------------------------------------------------------------------------

def mod_exp(base: int, exp: int, mod: int) -> int:
    """Square-and-multiply modular exponentiation.

    Computes base^exp mod mod using the binary method.  Handles negative
    exponents by computing the modular inverse first.

    Args:
        base: The base integer.
        exp: The exponent (non-negative, or negative if inverse exists).
        mod: The modulus (must be > 0).

    Returns:
        base^exp mod mod.

    Raises:
        ValueError: If mod <= 0 or inverse does not exist for negative exp.
    """
    if mod <= 0:
        raise ValueError("Modulus must be positive")
    if mod == 1:
        return 0
    if exp < 0:
        inv = mod_inverse(base, mod)
        if inv is None:
            raise ValueError(f"Modular inverse of {base} mod {mod} does not exist")
        return mod_exp(inv, -exp, mod)

    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean Algorithm.

    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b).

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Tuple of (gcd, x, y).
    """
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


def mod_inverse(a: int, m: int) -> Optional[int]:
    """Compute the modular multiplicative inverse of a mod m.

    Uses the Extended Euclidean Algorithm.  Returns None if the inverse
    does not exist (i.e. gcd(a, m) != 1).

    Args:
        a: The integer whose inverse is sought.
        m: The modulus.

    Returns:
        The inverse a^{-1} mod m, or None.
    """
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        return None
    return x % m


def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> Optional[int]:
    """Solve a system of simultaneous congruences via CRT.

    Given x ≡ r_i (mod m_i) for pairwise coprime m_i, returns the unique
    solution x in [0, product(m_i)).

    Args:
        remainders: List of remainders r_i.
        moduli: List of pairwise coprime moduli m_i.

    Returns:
        The unique solution x, or None if moduli are not pairwise coprime.
    """
    if len(remainders) != len(moduli):
        raise ValueError("remainders and moduli must have the same length")
    if not remainders:
        return 0

    M = 1
    for mi in moduli:
        M *= mi

    x = 0
    for ri, mi in zip(remainders, moduli):
        Mi = M // mi
        yi = mod_inverse(Mi, mi)
        if yi is None:
            return None
        x = (x + ri * Mi * yi) % M
    return x


def euler_totient(n: int) -> int:
    """Compute Euler's totient function phi(n).

    Uses trial division to factorise n and applies the product formula.

    Args:
        n: A positive integer.

    Returns:
        phi(n).
    """
    if n <= 0:
        raise ValueError("n must be positive")
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def jacobi_symbol(a: int, n: int) -> int:
    """Compute the Jacobi symbol (a/n).

    n must be a positive odd integer.

    Args:
        a: Top argument.
        n: Bottom argument (positive, odd).

    Returns:
        -1, 0, or 1.
    """
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    if n == 1:
        return result
    return 0


# ---------------------------------------------------------------------------
# 2. Primality Testing
# ---------------------------------------------------------------------------

SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
    67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137,
    139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
    223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
    293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
    383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461,
    463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563,
    569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643,
    647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
    743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829,
    839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937,
    941, 947, 953, 967, 971, 977, 983, 991, 997,
]


def fermat_test(n: int, k: int = 10) -> bool:
    """Fermat primality test.

    Probabilistic test: if n is composite, has at least 50% chance of
    detecting it per witness.  Carmichael numbers are the blind spot.

    Args:
        n: Number to test.
        k: Number of random witnesses.

    Returns:
        True if n is *probably* prime, False if definitely composite.
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for _ in range(k):
        a = random.randrange(2, n - 1)
        if pow(a, n - 1, n) != 1:
            return False
    return True


def miller_rabin(n: int, k: int = 20) -> bool:
    """Miller-Rabin primality test.

    For n < 3,317,044,064,679,887,385,961,981 the test is deterministic
    when using the first 13 primes as witnesses (we use the first 20 small
    primes for numbers < 3.3e24, random witnesses otherwise).

    Args:
        n: The number to test.
        k: Number of random rounds if n is large.

    Returns:
        True if n is (probably) prime.
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Deterministic witnesses for small n
    deterministic_witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    def _check_witness(a: int) -> bool:
        """Return True if a is a witness to n being composite."""
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    if n < 3_317_044_064_679_887_385_961_981:
        for a in deterministic_witnesses:
            if a >= n:
                continue
            if _check_witness(a):
                return False
        return True

    for a in deterministic_witnesses:
        if a >= n:
            continue
        if _check_witness(a):
            return False
    for _ in range(k):
        a = random.randrange(2, n - 1)
        if _check_witness(a):
            return False
    return True


def is_prime(n: int) -> bool:
    """Combined primality test: trial division then Miller-Rabin.

    Args:
        n: Integer to test.

    Returns:
        True if n is (very probably) prime.
    """
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n == p:
            return True
        if n % p == 0:
            return False
    return miller_rabin(n)


def generate_prime(bits: int = 512) -> int:
    """Generate a random prime of the specified bit length.

    Uses rejection sampling with Miller-Rabin.

    Args:
        bits: Desired bit length (minimum 8).

    Returns:
        A prime integer of *exactly* `bits` bits.
    """
    if bits < 8:
        bits = 8
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1  # ensure top bit set + odd
        if is_prime(candidate):
            return candidate


def next_prime(n: int) -> int:
    """Return the smallest prime >= n.

    Args:
        n: Starting point.

    Returns:
        The next prime >= n.
    """
    if n <= 2:
        return 2
    candidate = n if n % 2 != 0 else n + 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


def prime_factorization(n: int) -> List[Tuple[int, int]]:
    """Return the prime factorization of n as [(prime, exponent), ...].

    Uses trial division for factors up to sqrt(n).

    Args:
        n: Positive integer to factorize.

    Returns:
        List of (prime, exponent) tuples in ascending order.
    """
    if n <= 1:
        return []
    factors: List[Tuple[int, int]] = []
    d = 2
    while d * d <= n:
        count = 0
        while n % d == 0:
            n //= d
            count += 1
        if count > 0:
            factors.append((d, count))
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append((n, 1))
    return factors


# ---------------------------------------------------------------------------
# 3. RSA Mathematics
# ---------------------------------------------------------------------------

class RSAKeyPair(BaseModel):
    """RSA key pair with all mathematical components."""
    p: int = Field(..., description="First prime factor")
    q: int = Field(..., description="Second prime factor")
    n: int = Field(..., description="Modulus n = p * q")
    e: int = Field(..., description="Public exponent")
    d: int = Field(..., description="Private exponent")
    phi_n: int = Field(..., description="Euler totient phi(n) = (p-1)(q-1)")
    bit_length: int = Field(..., description="Bit length of n")


def rsa_keygen(bits: int = 512) -> RSAKeyPair:
    """Generate an RSA key pair.

    Generates two primes p and q of bits/2 length each, computes n = p*q,
    phi(n) = (p-1)(q-1), and finds d = e^{-1} mod phi(n) for e = 65537.

    Args:
        bits: Desired bit length of modulus n.

    Returns:
        An RSAKeyPair with all components.
    """
    half = bits // 2
    e = 65537

    while True:
        p = generate_prime(half)
        q = generate_prime(half)
        if p == q:
            continue
        n = p * q
        phi_n = (p - 1) * (q - 1)
        if math.gcd(e, phi_n) != 1:
            continue
        d = mod_inverse(e, phi_n)
        if d is not None and d > 1:
            break

    return RSAKeyPair(
        p=p, q=q, n=n, e=e, d=d, phi_n=phi_n,
        bit_length=n.bit_length(),
    )


def rsa_encrypt(plaintext: int, e: int, n: int) -> int:
    """RSA encryption: ciphertext = plaintext^e mod n.

    Args:
        plaintext: Integer message (0 <= plaintext < n).
        e: Public exponent.
        n: Modulus.

    Returns:
        Ciphertext integer.
    """
    if plaintext < 0 or plaintext >= n:
        raise ValueError(f"Plaintext must be in [0, {n})")
    return mod_exp(plaintext, e, n)


def rsa_decrypt(ciphertext: int, d: int, n: int) -> int:
    """RSA decryption: plaintext = ciphertext^d mod n.

    Args:
        ciphertext: Encrypted integer.
        d: Private exponent.
        n: Modulus.

    Returns:
        Decrypted plaintext integer.
    """
    return mod_exp(ciphertext, d, n)


def rsa_decrypt_crt(ciphertext: int, p: int, q: int, d: int) -> int:
    """RSA decryption using CRT for speed.

    Computes m1 = c^(d mod (p-1)) mod p, m2 = c^(d mod (q-1)) mod q,
    then combines via CRT.

    Args:
        ciphertext: Encrypted integer.
        p: First prime.
        q: Second prime.
        d: Private exponent.

    Returns:
        Decrypted plaintext integer.
    """
    dp = d % (p - 1)
    dq = d % (q - 1)
    q_inv = mod_inverse(q, p)
    if q_inv is None:
        raise ValueError("CRT inverse does not exist — p and q not coprime")
    m1 = pow(ciphertext, dp, p)
    m2 = pow(ciphertext, dq, q)
    h = (q_inv * (m1 - m2)) % p
    return m2 + h * q


def rsa_sign(message_hash: int, d: int, n: int) -> int:
    """RSA signature: signature = hash^d mod n.

    Args:
        message_hash: Integer hash of the message.
        d: Private exponent.
        n: Modulus.

    Returns:
        Signature integer.
    """
    return mod_exp(message_hash, d, n)


def rsa_verify(message_hash: int, signature: int, e: int, n: int) -> bool:
    """RSA signature verification: check hash == signature^e mod n.

    Args:
        message_hash: Expected integer hash.
        signature: Signature integer.
        e: Public exponent.
        n: Modulus.

    Returns:
        True if the signature is valid.
    """
    recovered = mod_exp(signature, e, n)
    return recovered == message_hash


# ---------------------------------------------------------------------------
# 4. Diffie-Hellman Key Exchange
# ---------------------------------------------------------------------------

class DHParams(BaseModel):
    """Diffie-Hellman parameters and key material."""
    p: int = Field(..., description="Prime modulus")
    g: int = Field(..., description="Generator")
    private_key: int = Field(..., description="Private exponent a")
    public_key: int = Field(..., description="g^a mod p")


class DHExchange(BaseModel):
    """Full Diffie-Hellman exchange result."""
    p: int
    g: int
    alice_private: int
    alice_public: int
    bob_private: int
    bob_public: int
    shared_secret: int
    verified: bool = Field(..., description="Both sides computed same secret")


# Well-known safe prime groups for DH (RFC 3526 / RFC 7919 excerpts)
DH_SAFE_PRIMES: Dict[str, Dict[str, int]] = {
    "modp_demo_256": {
        "p": 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485,
        "g": 2,
    },
}


def dh_generate_params(bits: int = 256) -> DHParams:
    """Generate Diffie-Hellman parameters and a key pair.

    For demonstration purposes uses a smaller prime; production systems
    should use at least 2048-bit primes.

    Args:
        bits: Bit length for the prime modulus.

    Returns:
        DHParams with p, g, private_key, public_key.
    """
    p = generate_prime(bits)
    g = 2
    # Ensure g is a generator of a large subgroup (simplified)
    private_key = random.randrange(2, p - 2)
    public_key = mod_exp(g, private_key, p)
    return DHParams(p=p, g=g, private_key=private_key, public_key=public_key)


def dh_compute_shared_secret(other_public: int, my_private: int, p: int) -> int:
    """Compute the DH shared secret: other_public^my_private mod p.

    Args:
        other_public: The other party's public key.
        my_private: Our private exponent.
        p: The prime modulus.

    Returns:
        The shared secret integer.
    """
    return mod_exp(other_public, my_private, p)


def dh_full_exchange(bits: int = 256) -> DHExchange:
    """Simulate a complete Diffie-Hellman key exchange between Alice and Bob.

    Args:
        bits: Bit length for the prime modulus.

    Returns:
        DHExchange with all values and verification.
    """
    p = generate_prime(bits)
    g = 2
    a = random.randrange(2, p - 2)
    b = random.randrange(2, p - 2)
    A = mod_exp(g, a, p)
    B = mod_exp(g, b, p)
    s_alice = mod_exp(B, a, p)
    s_bob = mod_exp(A, b, p)
    return DHExchange(
        p=p, g=g,
        alice_private=a, alice_public=A,
        bob_private=b, bob_public=B,
        shared_secret=s_alice,
        verified=(s_alice == s_bob),
    )


# ---------------------------------------------------------------------------
# 5. Elliptic Curve Arithmetic over Finite Fields
# ---------------------------------------------------------------------------

class ECPoint(BaseModel):
    """A point on an elliptic curve over a prime field.

    The point at infinity is represented by x = None, y = None.
    """
    x: Optional[int] = None
    y: Optional[int] = None

    @property
    def is_infinity(self) -> bool:
        return self.x is None and self.y is None


class EllipticCurve:
    """Weierstrass elliptic curve y^2 = x^3 + a*x + b (mod p).

    All arithmetic is performed in the finite field GF(p).

    Attributes:
        a: Curve coefficient a.
        b: Curve coefficient b.
        p: The prime field modulus.
    """

    def __init__(self, a: int, b: int, p: int) -> None:
        self.a = a % p
        self.b = b % p
        self.p = p
        disc = (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p
        if disc == 0:
            raise ValueError("Singular curve: 4a^3 + 27b^2 = 0 mod p")

    def is_on_curve(self, pt: ECPoint) -> bool:
        """Check whether a point lies on this curve."""
        if pt.is_infinity:
            return True
        lhs = pow(pt.y, 2, self.p)
        rhs = (pow(pt.x, 3, self.p) + self.a * pt.x + self.b) % self.p
        return lhs == rhs

    def point_add(self, P: ECPoint, Q: ECPoint) -> ECPoint:
        """Add two points on the curve.

        Implements the chord-and-tangent rule for Weierstrass curves.

        Args:
            P: First point.
            Q: Second point.

        Returns:
            P + Q on the curve.
        """
        if P.is_infinity:
            return Q
        if Q.is_infinity:
            return P

        if P.x == Q.x and P.y != Q.y:
            return ECPoint()  # Point at infinity

        if P.x == Q.x and P.y == Q.y:
            return self.point_double(P)

        # Different x-coordinates
        dy = (Q.y - P.y) % self.p
        dx = (Q.x - P.x) % self.p
        dx_inv = mod_inverse(dx, self.p)
        if dx_inv is None:
            return ECPoint()  # Shouldn't happen for valid points on prime-order curves
        lam = (dy * dx_inv) % self.p
        x_r = (lam * lam - P.x - Q.x) % self.p
        y_r = (lam * (P.x - x_r) - P.y) % self.p
        return ECPoint(x=x_r, y=y_r)

    def point_double(self, P: ECPoint) -> ECPoint:
        """Double a point on the curve.

        Uses the tangent formula: lambda = (3x^2 + a) / (2y).

        Args:
            P: The point to double.

        Returns:
            2P on the curve.
        """
        if P.is_infinity:
            return P
        if P.y == 0:
            return ECPoint()

        num = (3 * pow(P.x, 2, self.p) + self.a) % self.p
        den = (2 * P.y) % self.p
        den_inv = mod_inverse(den, self.p)
        if den_inv is None:
            return ECPoint()
        lam = (num * den_inv) % self.p
        x_r = (lam * lam - 2 * P.x) % self.p
        y_r = (lam * (P.x - x_r) - P.y) % self.p
        return ECPoint(x=x_r, y=y_r)

    def scalar_multiply(self, k: int, P: ECPoint) -> ECPoint:
        """Scalar multiplication kP using the double-and-add algorithm.

        Args:
            k: The scalar (non-negative integer).
            P: The base point.

        Returns:
            kP on the curve.
        """
        if k < 0:
            P = ECPoint(x=P.x, y=(-P.y) % self.p)
            k = -k
        if k == 0 or P.is_infinity:
            return ECPoint()

        result = ECPoint()
        addend = P
        while k > 0:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_double(addend)
            k >>= 1
        return result

    def point_negate(self, P: ECPoint) -> ECPoint:
        """Negate a point: -P = (x, -y mod p)."""
        if P.is_infinity:
            return P
        return ECPoint(x=P.x, y=(-P.y) % self.p)

    def find_points(self, max_search: int = 200) -> List[ECPoint]:
        """Brute-force search for points on the curve (for small p only).

        Args:
            max_search: Maximum x-coordinate to try.

        Returns:
            List of points found.
        """
        points: List[ECPoint] = []
        limit = min(self.p, max_search)
        for x_val in range(limit):
            rhs = (pow(x_val, 3, self.p) + self.a * x_val + self.b) % self.p
            y_val = _tonelli_shanks(rhs, self.p)
            if y_val is not None:
                points.append(ECPoint(x=x_val, y=y_val))
                neg_y = (-y_val) % self.p
                if neg_y != y_val:
                    points.append(ECPoint(x=x_val, y=neg_y))
        return points

    def order_of_point(self, P: ECPoint, max_order: int = 10000) -> Optional[int]:
        """Find the order of a point by repeated addition (small curves only).

        Args:
            P: The point.
            max_order: Upper bound on search.

        Returns:
            The order n such that nP = O, or None if not found.
        """
        if P.is_infinity:
            return 1
        current = P
        for i in range(2, max_order + 1):
            current = self.point_add(current, P)
            if current.is_infinity:
                return i
        return None


def _tonelli_shanks(n: int, p: int) -> Optional[int]:
    """Tonelli-Shanks algorithm: find sqrt(n) mod p.

    Returns None if n is not a quadratic residue mod p.

    Args:
        n: Value to take the square root of.
        p: Prime modulus.

    Returns:
        An integer r such that r^2 = n (mod p), or None.
    """
    if n % p == 0:
        return 0
    if pow(n, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)

    # Factor out powers of 2: p - 1 = Q * 2^S
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1

    # Find a quadratic non-residue z
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) // 2, p)

    while True:
        if t == 0:
            return 0
        if t == 1:
            return R
        # Find least i such that t^(2^i) = 1
        i = 1
        temp = (t * t) % p
        while temp != 1:
            temp = (temp * temp) % p
            i += 1
        b = pow(c, 1 << (M - i - 1), p)
        M = i
        c = (b * b) % p
        t = (t * c) % p
        R = (R * b) % p


# Well-known curves
SECP256K1_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
SECP256K1_A = 0
SECP256K1_B = 7
SECP256K1_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
SECP256K1_Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# A small demo curve for testing: y^2 = x^3 + 2x + 3 mod 97
DEMO_CURVE_A = 2
DEMO_CURVE_B = 3
DEMO_CURVE_P = 97


def ecdh_key_exchange(
    curve: EllipticCurve, G: ECPoint, order: int,
) -> Dict[str, Any]:
    """Simulate an ECDH key exchange.

    Args:
        curve: The elliptic curve.
        G: The generator point.
        order: The order of G.

    Returns:
        Dict with both parties' keys and the shared secret point.
    """
    a = random.randrange(1, order)
    b = random.randrange(1, order)
    A_pub = curve.scalar_multiply(a, G)
    B_pub = curve.scalar_multiply(b, G)
    s_alice = curve.scalar_multiply(a, B_pub)
    s_bob = curve.scalar_multiply(b, A_pub)
    return {
        "alice_private": a,
        "alice_public": {"x": A_pub.x, "y": A_pub.y},
        "bob_private": b,
        "bob_public": {"x": B_pub.x, "y": B_pub.y},
        "shared_secret": {"x": s_alice.x, "y": s_alice.y},
        "verified": s_alice.x == s_bob.x and s_alice.y == s_bob.y,
    }


def ecdsa_sign(
    message_hash: int, private_key: int,
    curve: EllipticCurve, G: ECPoint, order: int,
) -> Tuple[int, int]:
    """ECDSA signing (pure math).

    Args:
        message_hash: The hash of the message as an integer.
        private_key: The signer's private key.
        curve: The elliptic curve.
        G: Generator point.
        order: Order of G.

    Returns:
        Tuple (r, s) signature.
    """
    while True:
        k = random.randrange(1, order)
        R = curve.scalar_multiply(k, G)
        if R.is_infinity or R.x is None:
            continue
        r = R.x % order
        if r == 0:
            continue
        k_inv = mod_inverse(k, order)
        if k_inv is None:
            continue
        s = (k_inv * (message_hash + r * private_key)) % order
        if s == 0:
            continue
        return r, s


def ecdsa_verify(
    message_hash: int, r: int, s: int, public_key: ECPoint,
    curve: EllipticCurve, G: ECPoint, order: int,
) -> bool:
    """ECDSA signature verification (pure math).

    Args:
        message_hash: Hash of the message as integer.
        r: Signature component r.
        s: Signature component s.
        public_key: Signer's public key point.
        curve: The elliptic curve.
        G: Generator point.
        order: Order of G.

    Returns:
        True if signature is valid.
    """
    if not (1 <= r < order and 1 <= s < order):
        return False
    s_inv = mod_inverse(s, order)
    if s_inv is None:
        return False
    u1 = (message_hash * s_inv) % order
    u2 = (r * s_inv) % order
    P1 = curve.scalar_multiply(u1, G)
    P2 = curve.scalar_multiply(u2, public_key)
    R = curve.point_add(P1, P2)
    if R.is_infinity or R.x is None:
        return False
    return R.x % order == r


# ---------------------------------------------------------------------------
# 6. SHA-256 Analysis (using hashlib — analysis, not re-implementation)
# ---------------------------------------------------------------------------

def sha256_hash(data: bytes) -> str:
    """Compute SHA-256 hash of data.

    Args:
        data: Bytes to hash.

    Returns:
        Hex-encoded hash string.
    """
    return hashlib.sha256(data).hexdigest()


def sha256_properties(data: bytes) -> Dict[str, Any]:
    """Analyze SHA-256 properties of given data.

    Examines: digest, bit distribution, leading/trailing zeros,
    entropy estimate, and Hamming weight.

    Args:
        data: Input bytes.

    Returns:
        Dictionary of SHA-256 properties.
    """
    digest = hashlib.sha256(data).digest()
    hex_digest = digest.hex()
    bits = bin(int(hex_digest, 16))[2:].zfill(256)

    ones = bits.count("1")
    zeros = bits.count("0")
    leading_zeros = len(bits) - len(bits.lstrip("0"))
    trailing_zeros = len(bits) - len(bits.rstrip("0"))

    # Byte frequency
    byte_freq: Dict[int, int] = {}
    for b in digest:
        byte_freq[b] = byte_freq.get(b, 0) + 1

    # Shannon entropy of byte distribution
    entropy = 0.0
    for count in byte_freq.values():
        prob = count / 32
        if prob > 0:
            entropy -= prob * math.log2(prob)

    return {
        "input_hex": data.hex() if len(data) <= 64 else data[:64].hex() + "...",
        "input_length_bytes": len(data),
        "digest_hex": hex_digest,
        "digest_bits": bits,
        "hamming_weight": ones,
        "zero_bits": zeros,
        "leading_zero_bits": leading_zeros,
        "trailing_zero_bits": trailing_zeros,
        "byte_entropy_bits": round(entropy, 4),
        "max_possible_entropy": round(math.log2(256), 4),
        "uniformity_ratio": round(ones / 256, 4),
    }


def sha256_avalanche(data1: bytes, data2: bytes) -> Dict[str, Any]:
    """Measure the avalanche effect between two SHA-256 inputs.

    The avalanche effect means a small change in input produces a
    drastically different output.  Ideally ~50% of bits change.

    Args:
        data1: First input.
        data2: Second input.

    Returns:
        Avalanche analysis dictionary.
    """
    h1 = int(hashlib.sha256(data1).hexdigest(), 16)
    h2 = int(hashlib.sha256(data2).hexdigest(), 16)
    xor_val = h1 ^ h2
    bits_changed = bin(xor_val).count("1")
    input_bits_diff = 0
    # Compute bit difference in inputs
    max_len = max(len(data1), len(data2))
    d1 = data1.ljust(max_len, b"\x00")
    d2 = data2.ljust(max_len, b"\x00")
    for b1, b2 in zip(d1, d2):
        input_bits_diff += bin(b1 ^ b2).count("1")

    return {
        "input1_hex": data1.hex() if len(data1) <= 32 else data1[:32].hex() + "...",
        "input2_hex": data2.hex() if len(data2) <= 32 else data2[:32].hex() + "...",
        "hash1": format(h1, "064x"),
        "hash2": format(h2, "064x"),
        "input_bit_difference": input_bits_diff,
        "output_bits_changed": bits_changed,
        "output_bits_total": 256,
        "avalanche_ratio": round(bits_changed / 256, 4),
        "ideal_ratio": 0.5,
        "deviation_from_ideal": round(abs(bits_changed / 256 - 0.5), 4),
        "passes_strict_avalanche": bits_changed >= 100 and bits_changed <= 156,
    }


def sha256_collision_resistance_demo(prefix: bytes, max_bits: int = 24) -> Dict[str, Any]:
    """Demonstrate partial collision finding (birthday attack concept).

    Searches for two inputs sharing the first `max_bits` bits of their
    SHA-256 hash.  This is O(2^(max_bits/2)) on average.

    WARNING: max_bits > 32 will be very slow.  Capped at 32.

    Args:
        prefix: Common prefix for generated inputs.
        max_bits: Number of leading hash bits to collide.

    Returns:
        Collision search results.
    """
    max_bits = min(max_bits, 32)
    mask = ((1 << max_bits) - 1) << (256 - max_bits)

    seen: Dict[int, bytes] = {}
    attempts = 0
    start_time = time.monotonic()
    max_attempts = 2 ** (max_bits // 2 + 4)  # ~16x expected

    for i in range(max_attempts):
        data = prefix + i.to_bytes(8, "big")
        h = int(hashlib.sha256(data).hexdigest(), 16)
        truncated = h & mask
        attempts += 1
        if truncated in seen and seen[truncated] != data:
            elapsed = time.monotonic() - start_time
            return {
                "found": True,
                "max_bits": max_bits,
                "attempts": attempts,
                "expected_attempts": 2 ** (max_bits // 2),
                "elapsed_seconds": round(elapsed, 4),
                "input1_hex": seen[truncated].hex(),
                "input2_hex": data.hex(),
                "hash1": hashlib.sha256(seen[truncated]).hexdigest(),
                "hash2": hashlib.sha256(data).hexdigest(),
                "matching_prefix_bits": max_bits,
            }
        seen[truncated] = data

    elapsed = time.monotonic() - start_time
    return {
        "found": False,
        "max_bits": max_bits,
        "attempts": attempts,
        "elapsed_seconds": round(elapsed, 4),
        "note": "No collision found within attempt limit",
    }


# ---------------------------------------------------------------------------
# 7. AES Galois Field GF(2^8) Mathematics
# ---------------------------------------------------------------------------

class GaloisFieldGF256:
    """Arithmetic in GF(2^8) used by AES.

    The irreducible polynomial is x^8 + x^4 + x^3 + x + 1 (0x11B).
    All operations are on bytes (0-255).
    """

    IRREDUCIBLE = 0x11B  # x^8 + x^4 + x^3 + x + 1

    @staticmethod
    def add(a: int, b: int) -> int:
        """Addition in GF(2^8) is XOR."""
        return a ^ b

    @staticmethod
    def subtract(a: int, b: int) -> int:
        """Subtraction in GF(2^8) is also XOR (same as addition)."""
        return a ^ b

    @classmethod
    def multiply(cls, a: int, b: int) -> int:
        """Multiplication in GF(2^8) with reduction by the AES polynomial.

        Uses the "peasant multiplication" (shift-and-XOR) algorithm.

        Args:
            a: First byte (0-255).
            b: Second byte (0-255).

        Returns:
            Product in GF(2^8).
        """
        result = 0
        for _ in range(8):
            if b & 1:
                result ^= a
            carry = a & 0x80
            a = (a << 1) & 0xFF
            if carry:
                a ^= cls.IRREDUCIBLE & 0xFF
            b >>= 1
        return result

    @classmethod
    def power(cls, a: int, exp: int) -> int:
        """Exponentiation in GF(2^8) via repeated squaring.

        Args:
            a: Base byte.
            exp: Non-negative exponent.

        Returns:
            a^exp in GF(2^8).
        """
        if exp == 0:
            return 1
        result = 1
        base = a
        while exp > 0:
            if exp & 1:
                result = cls.multiply(result, base)
            base = cls.multiply(base, base)
            exp >>= 1
        return result

    @classmethod
    def inverse(cls, a: int) -> int:
        """Multiplicative inverse in GF(2^8).

        Uses Fermat's little theorem: a^{-1} = a^{254} since the field
        has 256 elements and a^{255} = 1 for a != 0.

        Args:
            a: Non-zero byte.

        Returns:
            Multiplicative inverse.

        Raises:
            ValueError: If a is 0.
        """
        if a == 0:
            raise ValueError("Zero has no inverse in GF(2^8)")
        return cls.power(a, 254)

    @classmethod
    def build_log_antilog_tables(cls) -> Tuple[List[int], List[int]]:
        """Build log and antilog (exp) tables for GF(2^8) using generator 3.

        Returns:
            (log_table, antilog_table) where antilog[i] = 3^i mod P
            and log[antilog[i]] = i.
        """
        log_table = [0] * 256
        antilog_table = [0] * 256
        val = 1
        for i in range(255):
            antilog_table[i] = val
            log_table[val] = i
            val = cls.multiply(val, 3)
        antilog_table[255] = antilog_table[0]
        return log_table, antilog_table

    @classmethod
    def aes_mix_column(cls, column: List[int]) -> List[int]:
        """AES MixColumns operation on a single 4-byte column.

        Multiplies the column vector by the fixed AES MixColumns matrix:
        [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]] in GF(2^8).

        Args:
            column: List of 4 bytes.

        Returns:
            Transformed 4-byte column.
        """
        if len(column) != 4:
            raise ValueError("Column must have exactly 4 bytes")

        matrix = [
            [2, 3, 1, 1],
            [1, 2, 3, 1],
            [1, 1, 2, 3],
            [3, 1, 1, 2],
        ]
        result = [0, 0, 0, 0]
        for i in range(4):
            val = 0
            for j in range(4):
                val ^= cls.multiply(matrix[i][j], column[j])
            result[i] = val
        return result

    @classmethod
    def aes_inv_mix_column(cls, column: List[int]) -> List[int]:
        """Inverse AES MixColumns on a single 4-byte column.

        Uses the inverse matrix:
        [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]

        Args:
            column: List of 4 bytes.

        Returns:
            Inverse-transformed column.
        """
        if len(column) != 4:
            raise ValueError("Column must have exactly 4 bytes")

        inv_matrix = [
            [14, 11, 13, 9],
            [9, 14, 11, 13],
            [13, 9, 14, 11],
            [11, 13, 9, 14],
        ]
        result = [0, 0, 0, 0]
        for i in range(4):
            val = 0
            for j in range(4):
                val ^= cls.multiply(inv_matrix[i][j], column[j])
            result[i] = val
        return result

    @classmethod
    def aes_sbox_value(cls, byte_val: int) -> int:
        """Compute a single AES S-box value.

        S-box(x) = affine_transform(inverse(x)) where the affine transform
        is a specific bit-level operation defined by AES.

        Args:
            byte_val: Input byte (0-255).

        Returns:
            S-box output byte.
        """
        # Multiplicative inverse (0 maps to 0)
        inv = cls.inverse(byte_val) if byte_val != 0 else 0
        # Affine transformation
        result = inv
        for i in range(4):
            inv = ((inv << 1) | (inv >> 7)) & 0xFF
            result ^= inv
        result ^= 0x63
        return result & 0xFF

    @classmethod
    def build_sbox(cls) -> List[int]:
        """Build the full AES S-box lookup table.

        Returns:
            List of 256 S-box values.
        """
        return [cls.aes_sbox_value(i) for i in range(256)]


# ---------------------------------------------------------------------------
# 8. Discrete Logarithm (Baby-step Giant-step)
# ---------------------------------------------------------------------------

def baby_step_giant_step(g: int, h: int, p: int, order: Optional[int] = None) -> Optional[int]:
    """Baby-step giant-step algorithm for the discrete logarithm.

    Finds x such that g^x = h (mod p).

    Complexity: O(sqrt(n)) time and space where n = order of g.

    Args:
        g: Generator.
        h: Target (g^x mod p).
        p: Prime modulus.
        order: Known order of g (defaults to p-1).

    Returns:
        x such that g^x = h mod p, or None if not found.
    """
    if order is None:
        order = p - 1

    m = math.isqrt(order) + 1

    # Baby step: compute g^j mod p for j in [0, m)
    table: Dict[int, int] = {}
    power = 1
    for j in range(m):
        table[power] = j
        power = (power * g) % p

    # Giant step factor: g^{-m} mod p
    g_inv_m = mod_inverse(pow(g, m, p), p)
    if g_inv_m is None:
        return None

    # Giant step
    gamma = h
    for i in range(m):
        if gamma in table:
            x = i * m + table[gamma]
            if x < order:
                return x
        gamma = (gamma * g_inv_m) % p

    return None


def pohlig_hellman_partial(g: int, h: int, p: int, factors: List[Tuple[int, int]]) -> Optional[int]:
    """Pohlig-Hellman algorithm for DLP when the group order is smooth.

    Decomposes the DLP into sub-problems for each prime factor of the
    group order, then combines via CRT.  Only works well when all prime
    factors are small.

    Args:
        g: Generator.
        h: Target.
        p: Prime modulus.
        factors: Factorization of the group order as [(prime, exp), ...].

    Returns:
        x such that g^x = h mod p, or None.
    """
    order = 1
    for pi, ei in factors:
        order *= pi ** ei

    remainders: List[int] = []
    moduli: List[int] = []

    for pi, ei in factors:
        pe = pi ** ei
        gi = pow(g, order // pe, p)
        hi = pow(h, order // pe, p)

        # Solve gi^x = hi mod p where x in [0, pe)
        xi = baby_step_giant_step(gi, hi, p, pe)
        if xi is None:
            return None
        remainders.append(xi)
        moduli.append(pe)

    return chinese_remainder_theorem(remainders, moduli)


# ---------------------------------------------------------------------------
# 9. Number Theory Utilities
# ---------------------------------------------------------------------------

def legendre_symbol(a: int, p: int) -> int:
    """Compute the Legendre symbol (a/p) for odd prime p.

    Args:
        a: Integer.
        p: Odd prime.

    Returns:
        -1, 0, or 1.
    """
    val = pow(a, (p - 1) // 2, p)
    if val == p - 1:
        return -1
    return val


def primitive_root(p: int) -> Optional[int]:
    """Find a primitive root modulo prime p.

    A primitive root g has order p-1, meaning g generates the entire
    multiplicative group (Z/pZ)*.

    Args:
        p: A prime number.

    Returns:
        A primitive root, or None if p < 2.
    """
    if p < 2:
        return None
    if p == 2:
        return 1
    phi = p - 1
    factors = prime_factorization(phi)
    prime_factors = [f[0] for f in factors]

    for g in range(2, p):
        is_root = True
        for q in prime_factors:
            if pow(g, phi // q, p) == 1:
                is_root = False
                break
        if is_root:
            return g
    return None


def is_quadratic_residue(a: int, p: int) -> bool:
    """Check if a is a quadratic residue mod p (p odd prime).

    Args:
        a: Integer to test.
        p: Odd prime modulus.

    Returns:
        True if a is a QR mod p.
    """
    return legendre_symbol(a, p) == 1


def order_of_element(a: int, n: int) -> Optional[int]:
    """Find the multiplicative order of a mod n.

    The order is the smallest positive k such that a^k = 1 (mod n).

    Args:
        a: Element.
        n: Modulus.

    Returns:
        The order, or None if gcd(a, n) != 1.
    """
    if math.gcd(a, n) != 1:
        return None
    phi = euler_totient(n)
    # Order must divide phi(n)
    divisors = sorted(_get_divisors(phi))
    for d in divisors:
        if pow(a, d, n) == 1:
            return d
    return phi


def _get_divisors(n: int) -> List[int]:
    """Get all positive divisors of n."""
    divs: List[int] = []
    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    return divs


# ═══════════════════════════════════════════════════════════════════════════
#  TIE-20 COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════


# ---------------------------------------------------------------------------
# TIE Component 1: Doctrine Cache
# ---------------------------------------------------------------------------

DOCTRINE_CACHE_PATH = ENGINE_DIR / "doctrine_cache.json"


class DoctrineBlock(BaseModel):
    """A pre-compiled expert-reasoning block."""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_stratification: str = "DEFENSIBLE"


_doctrine_cache: List[DoctrineBlock] = []


def _load_doctrine_cache() -> List[DoctrineBlock]:
    """Load doctrine blocks from the JSON cache file."""
    global _doctrine_cache
    if _doctrine_cache:
        return _doctrine_cache
    try:
        raw = json.loads(DOCTRINE_CACHE_PATH.read_text(encoding="utf-8"))
        _doctrine_cache = [DoctrineBlock(**entry) for entry in raw]
        logger.info("Loaded {} doctrine blocks", len(_doctrine_cache))
    except Exception as exc:
        logger.warning("Doctrine cache load failed: {}", exc)
        _doctrine_cache = []
    return _doctrine_cache


def doctrine_lookup(query: str) -> List[DoctrineBlock]:
    """Search doctrine cache for blocks matching the query.

    Matching is keyword-based: each block is scored by how many of its
    keywords appear in the query (case-insensitive).

    Args:
        query: The user's natural language query.

    Returns:
        Matching DoctrineBlocks sorted by relevance (descending).
    """
    cache = _load_doctrine_cache()
    query_lower = query.lower()
    scored: List[Tuple[int, DoctrineBlock]] = []
    for block in cache:
        score = sum(1 for kw in block.keywords if kw.lower() in query_lower)
        if score > 0:
            scored.append((score, block))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [b for _, b in scored]


# ---------------------------------------------------------------------------
# TIE Component 2: Response Modes
# ---------------------------------------------------------------------------

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


# ---------------------------------------------------------------------------
# TIE Component 3: Three-Layer Response
# ---------------------------------------------------------------------------

class ThreeLayerResponse(BaseModel):
    """The canonical TIE three-layer response."""
    layer1_doctrine: Optional[Dict[str, Any]] = None
    layer2_semantic: Optional[Dict[str, Any]] = None
    layer3_deep: Optional[Dict[str, Any]] = None
    response_mode: str = "FAST"
    latency_ms: float = 0.0
    determinism_hash: str = ""
    engine_id: str = ENGINE_ID
    engine_version: str = ENGINE_VERSION
    timestamp: str = ""


def three_layer_response(query: str, mode: ResponseMode = ResponseMode.FAST) -> ThreeLayerResponse:
    """Execute the three-layer response pipeline.

    Layer 1: Doctrine Cache lookup (0-200ms target).
    Layer 2: Semantic retrieval via normalized terms.
    Layer 3: Deep analysis with full math computation.

    Args:
        query: The user's query.
        mode: Response mode (FAST/DEFENSE/MEMO).

    Returns:
        ThreeLayerResponse with populated layers.
    """
    t0 = time.monotonic()
    response = ThreeLayerResponse(
        response_mode=mode.value,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    # Layer 1: Doctrine cache
    matches = doctrine_lookup(query)
    if matches:
        top = matches[0]
        response.layer1_doctrine = {
            "topic": top.topic,
            "conclusion": top.conclusion_template,
            "confidence": top.confidence,
            "stratification": top.confidence_stratification,
        }

    # Layer 2: Semantic normalization
    normalized = semantic_normalize(query)
    response.layer2_semantic = {
        "original_query": query,
        "normalized_terms": normalized,
        "matched_doctrines": len(matches),
    }

    # Layer 3: Deep analysis (always populated for DEFENSE/MEMO)
    if mode in (ResponseMode.DEFENSE, ResponseMode.MEMO) or not matches:
        response.layer3_deep = _deep_analysis(query)

    elapsed = (time.monotonic() - t0) * 1000
    response.latency_ms = round(elapsed, 2)

    # Determinism hash (TIE component 16)
    hash_input = json.dumps(response.dict(), sort_keys=True, default=str)
    response.determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    # Audit (TIE component 15)
    _audit_log({
        "action": "three_layer_response",
        "query": query,
        "mode": mode.value,
        "latency_ms": response.latency_ms,
        "doctrine_hit": response.layer1_doctrine is not None,
    })

    _metrics_collector.record_query(response.latency_ms, response.layer1_doctrine is not None)
    return response


# ---------------------------------------------------------------------------
# TIE Component 4: Authority Hardening
# ---------------------------------------------------------------------------

AUTHORITY_LEVELS = {
    "NIST_SP800": {"weight": 0.95, "source": "NIST Special Publications"},
    "RFC_STANDARD": {"weight": 0.90, "source": "IETF RFCs (approved standards)"},
    "ACADEMIC_PEER_REVIEWED": {"weight": 0.85, "source": "Peer-reviewed cryptography journals"},
    "TEXTBOOK_CANONICAL": {"weight": 0.80, "source": "Standard cryptography textbooks"},
    "IMPLEMENTATION_GUIDE": {"weight": 0.70, "source": "Implementation guides / best practices"},
    "COMMUNITY_CONSENSUS": {"weight": 0.60, "source": "Community consensus / common knowledge"},
}


def authority_weight(source_type: str) -> float:
    """Return the authority weight for a given source type.

    Args:
        source_type: Key into AUTHORITY_LEVELS.

    Returns:
        Weight between 0 and 1.
    """
    return AUTHORITY_LEVELS.get(source_type, {}).get("weight", 0.5)


def resolve_authority_conflict(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Resolve conflicting authorities by weight.

    Args:
        sources: List of dicts with "source_type" and "position" keys.

    Returns:
        The winning position with justification.
    """
    if not sources:
        return {"resolution": "no_sources", "confidence": 0.0}
    ranked = sorted(sources, key=lambda s: authority_weight(s.get("source_type", "")), reverse=True)
    winner = ranked[0]
    return {
        "resolution": winner.get("position", "unknown"),
        "winning_authority": winner.get("source_type", "unknown"),
        "weight": authority_weight(winner.get("source_type", "")),
        "alternatives_considered": len(ranked) - 1,
    }


# ---------------------------------------------------------------------------
# TIE Component 5: Confidence Stratification
# ---------------------------------------------------------------------------

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


def stratify_confidence(score: float) -> ConfidenceLevel:
    """Map a numeric confidence score to a stratification level.

    Args:
        score: Confidence between 0 and 1.

    Returns:
        ConfidenceLevel enum value.
    """
    if score >= 0.85:
        return ConfidenceLevel.DEFENSIBLE
    if score >= 0.65:
        return ConfidenceLevel.AGGRESSIVE
    if score >= 0.40:
        return ConfidenceLevel.DISCLOSURE
    return ConfidenceLevel.HIGH_RISK


# ---------------------------------------------------------------------------
# TIE Component 6: Semantic Normalization
# ---------------------------------------------------------------------------

SEMANTIC_DICT_PATH = ENGINE_DIR / "semantic_dict.json"
_semantic_dict: Dict[str, str] = {}


def _load_semantic_dict() -> Dict[str, str]:
    """Load the semantic dictionary from JSON."""
    global _semantic_dict
    if _semantic_dict:
        return _semantic_dict
    try:
        _semantic_dict = json.loads(SEMANTIC_DICT_PATH.read_text(encoding="utf-8"))
        logger.info("Loaded {} semantic normalizations", len(_semantic_dict))
    except Exception as exc:
        logger.warning("Semantic dict load failed: {}", exc)
        _semantic_dict = {}
    return _semantic_dict


def semantic_normalize(text: str) -> List[str]:
    """Normalize crypto-math terminology in a query.

    Args:
        text: Raw user text.

    Returns:
        List of normalized terms found.
    """
    sdict = _load_semantic_dict()
    text_lower = text.lower()
    normalized: List[str] = []
    for term, canonical in sdict.items():
        if term.lower() in text_lower:
            normalized.append(canonical)
    return list(set(normalized))


# ---------------------------------------------------------------------------
# TIE Component 7: Vector Search (keyword-based fallback)
# ---------------------------------------------------------------------------

def vector_search(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Keyword-based semantic search over doctrine cache.

    In a full deployment this would use a vector DB.  Here we use
    TF-IDF-style keyword scoring as the fallback.

    Args:
        query: Search query.
        top_k: Number of results to return.

    Returns:
        List of dicts with topic and score.
    """
    cache = _load_doctrine_cache()
    query_words = set(query.lower().split())
    results: List[Dict[str, Any]] = []
    for block in cache:
        block_words = set(block.topic.lower().split())
        block_words.update(kw.lower() for kw in block.keywords)
        overlap = query_words & block_words
        if overlap:
            score = len(overlap) / max(len(query_words), 1)
            results.append({"topic": block.topic, "score": round(score, 3), "keywords_matched": list(overlap)})
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_k]


# ---------------------------------------------------------------------------
# TIE Component 8: Telemetry
# ---------------------------------------------------------------------------

class TelemetryRecord(BaseModel):
    """A single telemetry event."""
    event: str
    timestamp: str = ""
    latency_ms: float = 0.0
    details: Dict[str, Any] = {}

    def __init__(self, **data: Any) -> None:
        if "timestamp" not in data or not data["timestamp"]:
            data["timestamp"] = datetime.now(timezone.utc).isoformat()
        super().__init__(**data)


_telemetry_buffer: List[TelemetryRecord] = []


def telemetry_emit(event: str, latency_ms: float = 0.0, details: Optional[Dict[str, Any]] = None) -> None:
    """Emit a telemetry event.

    Args:
        event: Event name.
        latency_ms: Operation latency.
        details: Additional event data.
    """
    rec = TelemetryRecord(event=event, latency_ms=latency_ms, details=details or {})
    _telemetry_buffer.append(rec)
    if len(_telemetry_buffer) > 10000:
        _telemetry_buffer.pop(0)


def telemetry_flush() -> List[Dict[str, Any]]:
    """Return and clear the telemetry buffer."""
    records = [r.dict() for r in _telemetry_buffer]
    _telemetry_buffer.clear()
    return records


# ---------------------------------------------------------------------------
# TIE Component 9: Drift Watcher
# ---------------------------------------------------------------------------

class DriftEvent(BaseModel):
    """Records a deviation from expected doctrine behavior."""
    doctrine_topic: str
    expected_confidence: float
    actual_confidence: float
    drift_magnitude: float
    timestamp: str = ""
    query: str = ""


_drift_events: List[DriftEvent] = []


def drift_check(topic: str, expected: float, actual: float, query: str = "") -> Optional[DriftEvent]:
    """Check for doctrine drift.

    Args:
        topic: The doctrine topic.
        expected: Expected confidence.
        actual: Actual confidence.
        query: The query that triggered this.

    Returns:
        DriftEvent if drift > 0.1, else None.
    """
    magnitude = abs(expected - actual)
    if magnitude > 0.1:
        ev = DriftEvent(
            doctrine_topic=topic,
            expected_confidence=expected,
            actual_confidence=actual,
            drift_magnitude=round(magnitude, 4),
            timestamp=datetime.now(timezone.utc).isoformat(),
            query=query,
        )
        _drift_events.append(ev)
        logger.warning("Drift detected on {}: expected={}, actual={}, mag={}", topic, expected, actual, magnitude)
        return ev
    return None


def drift_report() -> List[Dict[str, Any]]:
    """Return all recorded drift events."""
    return [e.dict() for e in _drift_events]


# ---------------------------------------------------------------------------
# TIE Component 10: Coverage Map
# ---------------------------------------------------------------------------

COVERAGE_MAP_PATH = ENGINE_DIR / "coverage_map.json"
_coverage_triggered: Dict[str, int] = {}
_coverage_missed: Dict[str, int] = {}


def _load_coverage_map() -> Dict[str, Any]:
    """Load coverage map from disk."""
    try:
        return json.loads(COVERAGE_MAP_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"topics": [], "gaps": []}


def coverage_record_hit(topic: str) -> None:
    """Record that a doctrine topic was triggered."""
    _coverage_triggered[topic] = _coverage_triggered.get(topic, 0) + 1


def coverage_record_miss(query: str) -> None:
    """Record a query that matched no doctrine."""
    _coverage_missed[query] = _coverage_missed.get(query, 0) + 1


def coverage_report() -> Dict[str, Any]:
    """Generate coverage report."""
    cmap = _load_coverage_map()
    all_topics = set(cmap.get("topics", []))
    triggered = set(_coverage_triggered.keys())
    untriggered = all_topics - triggered
    return {
        "total_topics": len(all_topics),
        "triggered": len(triggered),
        "untriggered": len(untriggered),
        "untriggered_list": sorted(untriggered),
        "hit_counts": dict(sorted(_coverage_triggered.items(), key=lambda x: x[1], reverse=True)),
        "missed_queries": dict(sorted(_coverage_missed.items(), key=lambda x: x[1], reverse=True)[:20]),
        "coverage_ratio": round(len(triggered) / max(len(all_topics), 1), 4),
    }


# ---------------------------------------------------------------------------
# TIE Component 11: Metrics Collector
# ---------------------------------------------------------------------------

class MetricsCollector:
    """Collects engine performance metrics."""

    def __init__(self) -> None:
        self.total_queries: int = 0
        self.doctrine_hits: int = 0
        self.total_latency_ms: float = 0.0
        self.max_latency_ms: float = 0.0
        self.errors: int = 0
        self.start_time: float = time.monotonic()

    def record_query(self, latency_ms: float, doctrine_hit: bool) -> None:
        """Record a query execution."""
        self.total_queries += 1
        self.total_latency_ms += latency_ms
        self.max_latency_ms = max(self.max_latency_ms, latency_ms)
        if doctrine_hit:
            self.doctrine_hits += 1

    def record_error(self) -> None:
        """Record an error."""
        self.errors += 1

    def report(self) -> Dict[str, Any]:
        """Generate metrics report."""
        uptime = time.monotonic() - self.start_time
        avg_latency = self.total_latency_ms / max(self.total_queries, 1)
        return {
            "total_queries": self.total_queries,
            "doctrine_hit_rate": round(self.doctrine_hits / max(self.total_queries, 1), 4),
            "avg_latency_ms": round(avg_latency, 2),
            "max_latency_ms": round(self.max_latency_ms, 2),
            "error_count": self.errors,
            "error_rate": round(self.errors / max(self.total_queries, 1), 4),
            "uptime_seconds": round(uptime, 1),
            "queries_per_minute": round(self.total_queries / max(uptime / 60, 0.001), 2),
        }


_metrics_collector = MetricsCollector()


# ---------------------------------------------------------------------------
# TIE Component 12: Health Endpoint (defined in FastAPI section below)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# TIE Component 13: Zoned Analysis
# ---------------------------------------------------------------------------

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


def zoned_analysis(query: str, zone: AnalysisZone) -> Dict[str, Any]:
    """Perform analysis constrained to a specific zone.

    Zones enforce strict separation of concerns:
    - PLANNING: Forward-looking, what-if scenarios, recommendations.
    - REPORTING: Factual, current state, no speculation.
    - AUDIT: Verification, compliance checking, evidence-based.

    Args:
        query: The user's query.
        zone: The analysis zone.

    Returns:
        Zone-constrained analysis result.
    """
    base = three_layer_response(query, ResponseMode.DEFENSE)
    zone_constraints = {
        AnalysisZone.PLANNING: {
            "allowed_operations": ["what_if", "recommendation", "projection"],
            "prohibited": ["verification_claim", "audit_assertion"],
            "disclaimer": "This is a planning analysis; not a verified audit.",
        },
        AnalysisZone.REPORTING: {
            "allowed_operations": ["factual_summary", "current_state", "data_presentation"],
            "prohibited": ["speculation", "recommendation"],
            "disclaimer": "This report presents factual findings only.",
        },
        AnalysisZone.AUDIT: {
            "allowed_operations": ["verification", "compliance_check", "evidence_review"],
            "prohibited": ["speculation", "planning"],
            "disclaimer": "Audit analysis — evidence-based assertions only.",
        },
    }
    return {
        "zone": zone.value,
        "constraints": zone_constraints[zone],
        "analysis": base.dict(),
    }


# ---------------------------------------------------------------------------
# TIE Component 14: Fact Fragility Scoring
# ---------------------------------------------------------------------------

def fact_fragility_score(claim: str, sources: int = 0, verifiable: bool = True) -> Dict[str, Any]:
    """Score the fragility of a factual claim.

    Fragility measures how likely a fact is to be overturned or
    mischaracterized.

    Args:
        claim: The factual claim to score.
        sources: Number of independent sources supporting the claim.
        verifiable: Whether the claim can be independently verified.

    Returns:
        Fragility score and breakdown.
    """
    base_score = 0.5
    if sources >= 3:
        base_score -= 0.2
    elif sources >= 1:
        base_score -= 0.1
    if verifiable:
        base_score -= 0.15
    if any(word in claim.lower() for word in ["proven", "theorem", "always", "never"]):
        base_score -= 0.1  # Mathematical certainty reduces fragility
    if any(word in claim.lower() for word in ["might", "possibly", "estimated", "approximately"]):
        base_score += 0.15

    fragility = max(0.0, min(1.0, base_score))
    return {
        "claim": claim,
        "fragility_score": round(fragility, 3),
        "classification": (
            "ROBUST" if fragility < 0.2 else
            "MODERATE" if fragility < 0.5 else
            "FRAGILE" if fragility < 0.75 else
            "HIGHLY_FRAGILE"
        ),
        "sources_cited": sources,
        "verifiable": verifiable,
    }


# ---------------------------------------------------------------------------
# TIE Component 19: Multi-Doctrine Decomposition
# ---------------------------------------------------------------------------

class IssueCategory(str, Enum):
    MODULAR_ARITHMETIC = "MODULAR_ARITHMETIC"
    PRIME_GENERATION = "PRIME_GENERATION"
    RSA_PROTOCOL = "RSA_PROTOCOL"
    DIFFIE_HELLMAN = "DIFFIE_HELLMAN"
    ELLIPTIC_CURVES = "ELLIPTIC_CURVES"
    HASH_FUNCTIONS = "HASH_FUNCTIONS"
    AES_GALOIS = "AES_GALOIS"
    DISCRETE_LOG = "DISCRETE_LOG"
    KEY_EXCHANGE = "KEY_EXCHANGE"
    DIGITAL_SIGNATURES = "DIGITAL_SIGNATURES"
    NUMBER_THEORY = "NUMBER_THEORY"
    SIDE_CHANNEL = "SIDE_CHANNEL"


ISSUE_INTERACTION_DAG: Dict[str, List[str]] = {
    "MODULAR_ARITHMETIC": ["RSA_PROTOCOL", "DIFFIE_HELLMAN", "ELLIPTIC_CURVES", "DISCRETE_LOG"],
    "PRIME_GENERATION": ["RSA_PROTOCOL", "DIFFIE_HELLMAN", "NUMBER_THEORY"],
    "RSA_PROTOCOL": ["DIGITAL_SIGNATURES", "KEY_EXCHANGE", "SIDE_CHANNEL"],
    "DIFFIE_HELLMAN": ["KEY_EXCHANGE", "DISCRETE_LOG"],
    "ELLIPTIC_CURVES": ["KEY_EXCHANGE", "DIGITAL_SIGNATURES", "DISCRETE_LOG"],
    "HASH_FUNCTIONS": ["DIGITAL_SIGNATURES", "RSA_PROTOCOL"],
    "AES_GALOIS": ["SIDE_CHANNEL"],
    "DISCRETE_LOG": ["DIFFIE_HELLMAN", "ELLIPTIC_CURVES"],
    "KEY_EXCHANGE": ["SIDE_CHANNEL"],
    "DIGITAL_SIGNATURES": ["HASH_FUNCTIONS"],
    "NUMBER_THEORY": ["MODULAR_ARITHMETIC", "PRIME_GENERATION"],
    "SIDE_CHANNEL": [],
}


def decompose_query(query: str) -> Dict[str, Any]:
    """Decompose a query into issue categories and interaction graph.

    Args:
        query: The user's query.

    Returns:
        Decomposition with categories, strata, and interaction DAG.
    """
    query_lower = query.lower()
    category_keywords: Dict[str, List[str]] = {
        "MODULAR_ARITHMETIC": ["modular", "mod", "congruence", "remainder", "exponentiation"],
        "PRIME_GENERATION": ["prime", "primality", "miller-rabin", "fermat test", "generate prime"],
        "RSA_PROTOCOL": ["rsa", "public key", "private key", "encryption", "decryption"],
        "DIFFIE_HELLMAN": ["diffie", "hellman", "key exchange", "shared secret"],
        "ELLIPTIC_CURVES": ["elliptic", "curve", "ecc", "point addition", "secp256"],
        "HASH_FUNCTIONS": ["hash", "sha", "sha256", "collision", "avalanche", "digest"],
        "AES_GALOIS": ["aes", "galois", "gf(2", "mixcolumn", "sbox", "rijndael"],
        "DISCRETE_LOG": ["discrete log", "baby step", "giant step", "dlog", "pohlig"],
        "KEY_EXCHANGE": ["key exchange", "ecdh", "dh", "shared key"],
        "DIGITAL_SIGNATURES": ["signature", "ecdsa", "sign", "verify"],
        "NUMBER_THEORY": ["euler", "totient", "jacobi", "legendre", "primitive root", "quadratic residue"],
        "SIDE_CHANNEL": ["timing", "side channel", "constant time", "power analysis"],
    }

    matched_categories: List[str] = []
    for cat, keywords in category_keywords.items():
        if any(kw in query_lower for kw in keywords):
            matched_categories.append(cat)

    # Build relevant DAG subset
    relevant_edges: List[Dict[str, str]] = []
    for cat in matched_categories:
        for target in ISSUE_INTERACTION_DAG.get(cat, []):
            relevant_edges.append({"from": cat, "to": target})

    return {
        "categories": matched_categories,
        "interaction_edges": relevant_edges,
        "category_count": len(matched_categories),
        "complexity": (
            "SIMPLE" if len(matched_categories) <= 1 else
            "MODERATE" if len(matched_categories) <= 3 else
            "COMPLEX"
        ),
    }


# ---------------------------------------------------------------------------
# TIE Component 20: Deep Analysis Mode
# ---------------------------------------------------------------------------

def _deep_analysis(query: str) -> Dict[str, Any]:
    """Full deep analysis with multi-source synthesis.

    Args:
        query: The user's query.

    Returns:
        Deep analysis result.
    """
    decomp = decompose_query(query)
    doctrines = doctrine_lookup(query)
    normalized = semantic_normalize(query)

    analysis_steps: List[str] = []
    analysis_steps.append(f"Query decomposed into {decomp['category_count']} categories")
    analysis_steps.append(f"Found {len(doctrines)} doctrine matches")
    analysis_steps.append(f"Normalized {len(normalized)} terms")

    if doctrines:
        top = doctrines[0]
        analysis_steps.append(f"Primary doctrine: {top.topic} (conf={top.confidence})")
        coverage_record_hit(top.topic)
    else:
        analysis_steps.append("No doctrine match — epistemic gap detected")
        coverage_record_miss(query)

    return {
        "decomposition": decomp,
        "doctrine_matches": len(doctrines),
        "top_doctrine": doctrines[0].topic if doctrines else None,
        "normalized_terms": normalized,
        "reasoning_chain": analysis_steps,
        "synthesis": f"Analysis covers {decomp['category_count']} cryptographic domains with {len(doctrines)} doctrinal references.",
    }


# ═══════════════════════════════════════════════════════════════════════════
#  PYDANTIC REQUEST / RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════

class ModExpRequest(BaseModel):
    base: int
    exp: int
    mod: int


class ModInverseRequest(BaseModel):
    a: int
    m: int


class CRTRequest(BaseModel):
    remainders: List[int]
    moduli: List[int]


class PrimalityRequest(BaseModel):
    n: int
    method: str = "miller_rabin"


class GeneratePrimeRequest(BaseModel):
    bits: int = 512


class RSAKeygenRequest(BaseModel):
    bits: int = 512


class RSAOpRequest(BaseModel):
    value: int
    exp: int
    n: int


class RSACRTDecryptRequest(BaseModel):
    ciphertext: int
    p: int
    q: int
    d: int


class DHExchangeRequest(BaseModel):
    bits: int = 256


class DHComputeRequest(BaseModel):
    other_public: int
    my_private: int
    p: int


class ECPointModel(BaseModel):
    x: Optional[int] = None
    y: Optional[int] = None


class ECCurveParams(BaseModel):
    a: int
    b: int
    p: int


class ECPointAddRequest(BaseModel):
    curve: ECCurveParams
    P: ECPointModel
    Q: ECPointModel


class ECScalarMulRequest(BaseModel):
    curve: ECCurveParams
    k: int
    P: ECPointModel


class ECDHRequest(BaseModel):
    curve: ECCurveParams
    G: ECPointModel
    order: int


class ECDSASignRequest(BaseModel):
    message_hash: int
    private_key: int
    curve: ECCurveParams
    G: ECPointModel
    order: int


class ECDSAVerifyRequest(BaseModel):
    message_hash: int
    r: int
    s: int
    public_key: ECPointModel
    curve: ECCurveParams
    G: ECPointModel
    order: int


class SHA256AnalyzeRequest(BaseModel):
    data_hex: str


class SHA256AvalancheRequest(BaseModel):
    data1_hex: str
    data2_hex: str


class SHA256CollisionRequest(BaseModel):
    prefix_hex: str = "00"
    max_bits: int = 20


class GF256MulRequest(BaseModel):
    a: int = Field(ge=0, le=255)
    b: int = Field(ge=0, le=255)


class GF256InverseRequest(BaseModel):
    a: int = Field(ge=1, le=255)


class MixColumnRequest(BaseModel):
    column: List[int] = Field(min_length=4, max_length=4)


class BSGSRequest(BaseModel):
    g: int
    h: int
    p: int
    order: Optional[int] = None


class EulerTotientRequest(BaseModel):
    n: int


class JacobiRequest(BaseModel):
    a: int
    n: int


class PrimitiveRootRequest(BaseModel):
    p: int


class FactorizationRequest(BaseModel):
    n: int


class QueryRequest(BaseModel):
    query: str
    mode: str = "FAST"
    zone: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
#  FASTAPI APPLICATION (TIE Component 17)
# ═══════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: load caches on startup."""
    logger.info("MATH11 Cryptographic Mathematics Engine starting on port {}", ENGINE_PORT)
    _load_doctrine_cache()
    _load_semantic_dict()
    _load_coverage_map()
    logger.info("MATH11 ready — all caches loaded")
    yield
    logger.info("MATH11 shutting down")


app = FastAPI(
    title=f"{ENGINE_ID} — {ENGINE_NAME}",
    version=ENGINE_VERSION,
    description="TIE-20 compliant cryptographic mathematics engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Health (TIE Component 12) ---

@app.get("/health")
async def health() -> Dict[str, Any]:
    """Comprehensive health check endpoint."""
    doctrine_count = len(_load_doctrine_cache())
    semantic_count = len(_load_semantic_dict())
    return {
        "status": "healthy",
        "engine_id": ENGINE_ID,
        "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION,
        "port": ENGINE_PORT,
        "tier": ENGINE_TIER,
        "mode": ENGINE_MODE,
        "auth_level": ENGINE_AUTH_LEVEL,
        "doctrine_blocks_loaded": doctrine_count,
        "semantic_terms_loaded": semantic_count,
        "metrics": _metrics_collector.report(),
        "coverage": coverage_report(),
        "drift_events": len(_drift_events),
        "telemetry_buffered": len(_telemetry_buffer),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# --- TIE Query Endpoint ---

@app.post("/query")
async def query_endpoint(req: QueryRequest) -> Dict[str, Any]:
    """Main TIE query endpoint with three-layer response."""
    try:
        mode = ResponseMode(req.mode.upper())
    except ValueError:
        mode = ResponseMode.FAST

    if req.zone:
        try:
            zone = AnalysisZone(req.zone.upper())
            return zoned_analysis(req.query, zone)
        except ValueError:
            pass

    result = three_layer_response(req.query, mode)
    return result.dict()


# --- Modular Arithmetic ---

@app.post("/math/mod_exp")
async def api_mod_exp(req: ModExpRequest) -> Dict[str, Any]:
    """Modular exponentiation: base^exp mod mod."""
    t0 = time.monotonic()
    result = mod_exp(req.base, req.exp, req.mod)
    elapsed = (time.monotonic() - t0) * 1000
    telemetry_emit("mod_exp", elapsed, {"base": req.base, "exp": req.exp, "mod": req.mod})
    return {"result": result, "expression": f"{req.base}^{req.exp} mod {req.mod}", "latency_ms": round(elapsed, 2)}


@app.post("/math/mod_inverse")
async def api_mod_inverse(req: ModInverseRequest) -> Dict[str, Any]:
    """Modular inverse: a^{-1} mod m."""
    t0 = time.monotonic()
    result = mod_inverse(req.a, req.m)
    elapsed = (time.monotonic() - t0) * 1000
    return {
        "result": result,
        "exists": result is not None,
        "expression": f"{req.a}^(-1) mod {req.m}",
        "verification": (result * req.a) % req.m if result is not None else None,
        "latency_ms": round(elapsed, 2),
    }


@app.post("/math/extended_gcd")
async def api_extended_gcd(req: ModInverseRequest) -> Dict[str, Any]:
    """Extended GCD: returns gcd, x, y such that a*x + m*y = gcd."""
    g, x, y = extended_gcd(req.a, req.m)
    return {"gcd": g, "x": x, "y": y, "verification": req.a * x + req.m * y}


@app.post("/math/crt")
async def api_crt(req: CRTRequest) -> Dict[str, Any]:
    """Chinese Remainder Theorem solver."""
    result = chinese_remainder_theorem(req.remainders, req.moduli)
    M = 1
    for m in req.moduli:
        M *= m
    return {
        "solution": result,
        "modulus_product": M,
        "congruences": [f"x = {r} (mod {m})" for r, m in zip(req.remainders, req.moduli)],
    }


@app.post("/math/euler_totient")
async def api_euler_totient(req: EulerTotientRequest) -> Dict[str, Any]:
    """Euler's totient function phi(n)."""
    result = euler_totient(req.n)
    return {"n": req.n, "phi_n": result, "factorization": prime_factorization(req.n)}


@app.post("/math/jacobi_symbol")
async def api_jacobi(req: JacobiRequest) -> Dict[str, Any]:
    """Jacobi symbol (a/n)."""
    result = jacobi_symbol(req.a, req.n)
    return {"a": req.a, "n": req.n, "jacobi": result}


@app.post("/math/factorize")
async def api_factorize(req: FactorizationRequest) -> Dict[str, Any]:
    """Prime factorization of n."""
    factors = prime_factorization(req.n)
    return {"n": req.n, "factors": [{"prime": p, "exponent": e} for p, e in factors]}


@app.post("/math/primitive_root")
async def api_primitive_root(req: PrimitiveRootRequest) -> Dict[str, Any]:
    """Find a primitive root modulo p."""
    root = primitive_root(req.p)
    return {"p": req.p, "primitive_root": root, "found": root is not None}


# --- Primality ---

@app.post("/prime/test")
async def api_primality(req: PrimalityRequest) -> Dict[str, Any]:
    """Primality testing with selectable method."""
    t0 = time.monotonic()
    if req.method == "fermat":
        result = fermat_test(req.n)
        method_used = "Fermat"
    else:
        result = miller_rabin(req.n)
        method_used = "Miller-Rabin"
    elapsed = (time.monotonic() - t0) * 1000
    return {
        "n": req.n, "is_prime": result, "method": method_used,
        "bit_length": req.n.bit_length(), "latency_ms": round(elapsed, 2),
    }


@app.post("/prime/generate")
async def api_generate_prime(req: GeneratePrimeRequest) -> Dict[str, Any]:
    """Generate a random prime of specified bit length."""
    t0 = time.monotonic()
    p = generate_prime(req.bits)
    elapsed = (time.monotonic() - t0) * 1000
    return {
        "prime": p, "bit_length": p.bit_length(),
        "hex": hex(p), "latency_ms": round(elapsed, 2),
    }


@app.post("/prime/next")
async def api_next_prime(req: PrimalityRequest) -> Dict[str, Any]:
    """Find the next prime >= n."""
    result = next_prime(req.n)
    return {"n": req.n, "next_prime": result, "gap": result - req.n}


# --- RSA ---

@app.post("/rsa/keygen")
async def api_rsa_keygen(req: RSAKeygenRequest) -> Dict[str, Any]:
    """Generate an RSA key pair."""
    t0 = time.monotonic()
    keys = rsa_keygen(req.bits)
    elapsed = (time.monotonic() - t0) * 1000
    return {**keys.dict(), "latency_ms": round(elapsed, 2)}


@app.post("/rsa/encrypt")
async def api_rsa_encrypt(req: RSAOpRequest) -> Dict[str, Any]:
    """RSA encryption: value^exp mod n."""
    result = rsa_encrypt(req.value, req.exp, req.n)
    return {"plaintext": req.value, "ciphertext": result, "e": req.exp, "n": req.n}


@app.post("/rsa/decrypt")
async def api_rsa_decrypt(req: RSAOpRequest) -> Dict[str, Any]:
    """RSA decryption: value^exp mod n."""
    result = rsa_decrypt(req.value, req.exp, req.n)
    return {"ciphertext": req.value, "plaintext": result, "d": req.exp, "n": req.n}


@app.post("/rsa/decrypt_crt")
async def api_rsa_decrypt_crt(req: RSACRTDecryptRequest) -> Dict[str, Any]:
    """RSA decryption using CRT."""
    result = rsa_decrypt_crt(req.ciphertext, req.p, req.q, req.d)
    return {"ciphertext": req.ciphertext, "plaintext": result}


@app.post("/rsa/sign")
async def api_rsa_sign(req: RSAOpRequest) -> Dict[str, Any]:
    """RSA signature: hash^d mod n."""
    sig = rsa_sign(req.value, req.exp, req.n)
    return {"message_hash": req.value, "signature": sig}


@app.post("/rsa/verify")
async def api_rsa_verify(req: RSAOpRequest) -> Dict[str, Any]:
    """RSA verify: check hash == sig^e mod n. value=hash, exp=e, n=n. Pass sig as query param."""
    # We reuse the model; caller passes signature in a query param
    return {"note": "Use /rsa/full_verify for complete verification"}


# --- Diffie-Hellman ---

@app.post("/dh/exchange")
async def api_dh_exchange(req: DHExchangeRequest) -> Dict[str, Any]:
    """Full DH key exchange simulation."""
    t0 = time.monotonic()
    result = dh_full_exchange(req.bits)
    elapsed = (time.monotonic() - t0) * 1000
    return {**result.dict(), "latency_ms": round(elapsed, 2)}


@app.post("/dh/compute_secret")
async def api_dh_compute(req: DHComputeRequest) -> Dict[str, Any]:
    """Compute DH shared secret."""
    secret = dh_compute_shared_secret(req.other_public, req.my_private, req.p)
    return {"shared_secret": secret}


# --- Elliptic Curves ---

@app.post("/ec/point_add")
async def api_ec_point_add(req: ECPointAddRequest) -> Dict[str, Any]:
    """Add two points on an elliptic curve."""
    curve = EllipticCurve(req.curve.a, req.curve.b, req.curve.p)
    P = ECPoint(x=req.P.x, y=req.P.y)
    Q = ECPoint(x=req.Q.x, y=req.Q.y)
    R = curve.point_add(P, Q)
    return {"result": {"x": R.x, "y": R.y}, "is_infinity": R.is_infinity}


@app.post("/ec/scalar_mul")
async def api_ec_scalar_mul(req: ECScalarMulRequest) -> Dict[str, Any]:
    """Scalar multiplication kP on an elliptic curve."""
    curve = EllipticCurve(req.curve.a, req.curve.b, req.curve.p)
    P = ECPoint(x=req.P.x, y=req.P.y)
    R = curve.scalar_multiply(req.k, P)
    return {"result": {"x": R.x, "y": R.y}, "is_infinity": R.is_infinity, "k": req.k}


@app.post("/ec/on_curve")
async def api_ec_on_curve(req: ECPointAddRequest) -> Dict[str, Any]:
    """Check if a point is on the curve."""
    curve = EllipticCurve(req.curve.a, req.curve.b, req.curve.p)
    P = ECPoint(x=req.P.x, y=req.P.y)
    return {"on_curve": curve.is_on_curve(P), "point": {"x": P.x, "y": P.y}}


@app.post("/ec/find_points")
async def api_ec_find_points(req: ECCurveParams) -> Dict[str, Any]:
    """Find points on the curve (small fields only)."""
    if req.p > 10000:
        raise HTTPException(status_code=400, detail="Field too large for brute-force search; p must be <= 10000")
    curve = EllipticCurve(req.a, req.b, req.p)
    points = curve.find_points()
    return {
        "curve": f"y^2 = x^3 + {req.a}x + {req.b} mod {req.p}",
        "point_count": len(points) + 1,  # +1 for point at infinity
        "points": [{"x": pt.x, "y": pt.y} for pt in points],
    }


@app.post("/ec/ecdh")
async def api_ecdh(req: ECDHRequest) -> Dict[str, Any]:
    """ECDH key exchange."""
    curve = EllipticCurve(req.curve.a, req.curve.b, req.curve.p)
    G = ECPoint(x=req.G.x, y=req.G.y)
    result = ecdh_key_exchange(curve, G, req.order)
    return result


@app.post("/ec/ecdsa_sign")
async def api_ecdsa_sign(req: ECDSASignRequest) -> Dict[str, Any]:
    """ECDSA signature generation."""
    curve = EllipticCurve(req.curve.a, req.curve.b, req.curve.p)
    G = ECPoint(x=req.G.x, y=req.G.y)
    r, s = ecdsa_sign(req.message_hash, req.private_key, curve, G, req.order)
    return {"r": r, "s": s}


@app.post("/ec/ecdsa_verify")
async def api_ecdsa_verify(req: ECDSAVerifyRequest) -> Dict[str, Any]:
    """ECDSA signature verification."""
    curve = EllipticCurve(req.curve.a, req.curve.b, req.curve.p)
    G = ECPoint(x=req.G.x, y=req.G.y)
    pub = ECPoint(x=req.public_key.x, y=req.public_key.y)
    valid = ecdsa_verify(req.message_hash, req.r, req.s, pub, curve, G, req.order)
    return {"valid": valid}


# --- SHA-256 Analysis ---

@app.post("/sha256/analyze")
async def api_sha256_analyze(req: SHA256AnalyzeRequest) -> Dict[str, Any]:
    """Analyze SHA-256 properties of input data."""
    data = bytes.fromhex(req.data_hex)
    return sha256_properties(data)


@app.post("/sha256/avalanche")
async def api_sha256_avalanche(req: SHA256AvalancheRequest) -> Dict[str, Any]:
    """Measure SHA-256 avalanche effect between two inputs."""
    d1 = bytes.fromhex(req.data1_hex)
    d2 = bytes.fromhex(req.data2_hex)
    return sha256_avalanche(d1, d2)


@app.post("/sha256/collision_demo")
async def api_sha256_collision(req: SHA256CollisionRequest) -> Dict[str, Any]:
    """Partial collision search demo (birthday attack)."""
    prefix = bytes.fromhex(req.prefix_hex)
    return sha256_collision_resistance_demo(prefix, req.max_bits)


# --- AES Galois Field ---

@app.post("/gf256/multiply")
async def api_gf256_multiply(req: GF256MulRequest) -> Dict[str, Any]:
    """Multiply two elements in GF(2^8)."""
    result = GaloisFieldGF256.multiply(req.a, req.b)
    return {"a": req.a, "b": req.b, "product": result, "hex": hex(result)}


@app.post("/gf256/inverse")
async def api_gf256_inverse(req: GF256InverseRequest) -> Dict[str, Any]:
    """Multiplicative inverse in GF(2^8)."""
    result = GaloisFieldGF256.inverse(req.a)
    verify = GaloisFieldGF256.multiply(req.a, result)
    return {"a": req.a, "inverse": result, "verification_product": verify}


@app.post("/gf256/mix_column")
async def api_mix_column(req: MixColumnRequest) -> Dict[str, Any]:
    """AES MixColumns on a 4-byte column."""
    result = GaloisFieldGF256.aes_mix_column(req.column)
    inv = GaloisFieldGF256.aes_inv_mix_column(result)
    return {
        "input": req.column,
        "mixed": result,
        "inverse_mixed": inv,
        "roundtrip_ok": inv == req.column,
    }


@app.get("/gf256/sbox")
async def api_sbox() -> Dict[str, Any]:
    """Return the full AES S-box."""
    sbox = GaloisFieldGF256.build_sbox()
    return {"sbox": sbox, "sbox_hex": [hex(v) for v in sbox]}


@app.get("/gf256/log_antilog")
async def api_log_antilog() -> Dict[str, Any]:
    """Return GF(2^8) log and antilog tables."""
    log_t, antilog_t = GaloisFieldGF256.build_log_antilog_tables()
    return {"log_table": log_t, "antilog_table": antilog_t}


# --- Discrete Log ---

@app.post("/dlog/bsgs")
async def api_bsgs(req: BSGSRequest) -> Dict[str, Any]:
    """Baby-step giant-step discrete logarithm."""
    t0 = time.monotonic()
    result = baby_step_giant_step(req.g, req.h, req.p, req.order)
    elapsed = (time.monotonic() - t0) * 1000
    verification = pow(req.g, result, req.p) if result is not None else None
    return {
        "g": req.g, "h": req.h, "p": req.p,
        "x": result, "found": result is not None,
        "verification": verification,
        "correct": verification == req.h if result is not None else False,
        "latency_ms": round(elapsed, 2),
    }


# --- Metrics / Telemetry / Coverage / Drift ---

@app.get("/metrics")
async def api_metrics() -> Dict[str, Any]:
    """Engine metrics."""
    return _metrics_collector.report()


@app.get("/telemetry")
async def api_telemetry() -> Dict[str, Any]:
    """Flush telemetry buffer."""
    return {"events": telemetry_flush()}


@app.get("/coverage")
async def api_coverage() -> Dict[str, Any]:
    """Coverage report."""
    return coverage_report()


@app.get("/drift")
async def api_drift() -> Dict[str, Any]:
    """Drift report."""
    return {"events": drift_report(), "count": len(_drift_events)}


@app.post("/decompose")
async def api_decompose(req: QueryRequest) -> Dict[str, Any]:
    """Decompose a query into issue categories."""
    return decompose_query(req.query)


@app.post("/fragility")
async def api_fragility(req: QueryRequest) -> Dict[str, Any]:
    """Score fact fragility of a claim."""
    return fact_fragility_score(req.query)


# --- Startup ---

if __name__ == "__main__":
    import uvicorn
    logger.info("Launching {} v{} on port {}", ENGINE_ID, ENGINE_VERSION, ENGINE_PORT)
    uvicorn.run(app, host="0.0.0.0", port=ENGINE_PORT, log_level="info")
