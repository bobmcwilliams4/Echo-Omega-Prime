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
        topic="Prime Number Generation",
        keywords=["prime", "random", "generation", "probabilistic", "cryptography"],
        conclusion_template="A prime number suitable for cryptographic use can be efficiently generated using probabilistic primality tests.",
        reasoning_framework=(
            "Prime numbers are foundational to many cryptographic algorithms, such as RSA and Diffie-Hellman. "
            "Efficient generation of large primes is accomplished by randomly selecting odd numbers of the desired bit length and subjecting them to probabilistic primality tests, "
            "such as the Miller-Rabin or Baillie-PSW tests. Deterministic tests are computationally infeasible for large numbers, so probabilistic tests are preferred, "
            "offering an acceptably low error rate. The process involves rejecting candidates that fail small prime divisibility checks, then applying multiple rounds of probabilistic testing. "
            "The security of cryptosystems depends on the unpredictability and size of the primes, as well as the statistical independence of generated primes. "
            "Cryptographically secure random number generators (CSPRNGs) are used to ensure unpredictability. "
            "The process is repeated until a candidate passes all tests, at which point it is accepted as a prime. "
            "For additional assurance, some implementations use a combination of tests or additional checks for known weak primes."
        ),
        key_factors=[
            "Quality of random number generator",
            "Strength and rounds of primality test",
            "Bit length of generated prime",
            "Resistance to known attacks (e.g., small factors, weak primes)",
            "Compliance with cryptographic standards (e.g., FIPS 186-4)"
        ],
        primary_authority=[
            "NIST SP 800-56A",
            "RFC 3526",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Implementer of cryptographic system",
        adversary_position="Probabilistic tests may yield composite numbers, risking cryptographic failure.",
        counter_arguments=[
            "Error probability can be made negligible with sufficient rounds.",
            "Composite numbers passing tests are extremely rare at cryptographic sizes.",
            "Additional checks can further reduce risk."
        ],
        resolution_strategy="Use multiple rounds of strong probabilistic tests and CSPRNGs; follow established standards.",
        entity_scope="Cryptographic libraries, protocol designers, implementers",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-56A Section 5.5.1"
    ),
    DoctrineBlock(
        topic="Discrete Logarithm Problem Hardness",
        keywords=["discrete logarithm", "hardness", "security", "group theory", "cryptography"],
        conclusion_template="The security of discrete logarithm-based cryptosystems relies on the computational intractability of the discrete logarithm problem in the chosen group.",
        reasoning_framework=(
            "The discrete logarithm problem (DLP) is defined as finding x given g and h in a group G such that h = g^x. "
            "The hardness of DLP underpins the security of schemes like Diffie-Hellman key exchange and ElGamal encryption. "
            "The problem is believed to be hard in certain groups, such as the multiplicative group of a large prime field or elliptic curve groups. "
            "The best-known algorithms for solving DLP in these groups (e.g., baby-step giant-step, Pollard's rho, index calculus) have exponential or sub-exponential complexity. "
            "Selection of group parameters is critical: small subgroups, weak curves, or composite modulus can compromise security. "
            "Quantum computers threaten DLP security via Shor's algorithm, but classical security remains robust with sufficiently large parameters. "
            "Standards specify minimum group sizes to resist known attacks."
        ),
        key_factors=[
            "Group selection (prime field, elliptic curve, etc.)",
            "Group order and structure",
            "Algorithmic advances",
            "Quantum computing threat",
            "Parameter validation"
        ],
        primary_authority=[
            "NIST SP 800-56A",
            "RFC 7748",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Protocol designer and implementer",
        adversary_position="Advances in algorithms or quantum computing may render DLP easy.",
        counter_arguments=[
            "No efficient classical algorithms for DLP in well-chosen groups are known.",
            "Parameters can be increased to maintain security margin.",
            "Quantum-safe alternatives are being developed."
        ],
        resolution_strategy="Use recommended group sizes and validated parameters; monitor for advances in cryptanalysis.",
        entity_scope="Cryptographic protocol designers, implementers",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-56A Section 5.6.1"
    ),
    DoctrineBlock(
        topic="RSA Modulus Generation",
        keywords=["RSA", "modulus", "key generation", "primes", "cryptography"],
        conclusion_template="RSA moduli must be the product of two large, random, and independent primes to ensure cryptographic strength.",
        reasoning_framework=(
            "RSA security depends on the difficulty of factoring the modulus n = p * q, where p and q are large primes. "
            "Both primes must be chosen randomly and independently, and must be of similar bit length to prevent easy factorization. "
            "Special care is taken to avoid small or structured primes, as well as primes with small differences. "
            "Primes must be tested for primality using strong probabilistic tests, and checked against known weak primes. "
            "The modulus should not be reused across different key pairs, nor should primes be shared. "
            "Key generation procedures must use CSPRNGs and comply with standards such as FIPS 186-4. "
            "Additional checks, such as ensuring (p-1) and (q-1) are not smooth, are recommended to prevent certain attacks."
        ),
        key_factors=[
            "Randomness and independence of primes",
            "Bit length of modulus",
            "Primality testing strength",
            "Avoidance of weak or structured primes",
            "Compliance with standards"
        ],
        primary_authority=[
            "FIPS 186-4",
            "PKCS #1 v2.2",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Key generator/implementer",
        adversary_position="Poorly generated primes or reused moduli can be factored, breaking security.",
        counter_arguments=[
            "Standardized procedures and CSPRNGs mitigate these risks.",
            "Regular audits and compliance checks reinforce security.",
            "Automated tools detect weak primes."
        ],
        resolution_strategy="Strict adherence to key generation standards and regular validation of implementation.",
        entity_scope="Key generation modules, cryptographic libraries",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="FIPS 186-4 Section B.3.1"
    ),
    DoctrineBlock(
        topic="Elliptic Curve Selection",
        keywords=["elliptic curve", "selection", "parameters", "security", "cryptography"],
        conclusion_template="Elliptic curves used in cryptography must be selected from standardized, well-studied sets with verifiable security properties.",
        reasoning_framework=(
            "Elliptic curve cryptography (ECC) relies on the hardness of the elliptic curve discrete logarithm problem (ECDLP). "
            "The choice of curve parameters is critical: weak or poorly chosen curves may be vulnerable to attacks such as small subgroup attacks, invalid curve attacks, or special structure attacks. "
            "Standardized curves (e.g., NIST P-256, Curve25519) have undergone extensive public scrutiny and are recommended for most applications. "
            "Custom or proprietary curves should be avoided unless their security can be independently verified. "
            "Curve parameters must be generated in a transparent and reproducible manner, ideally with verifiable randomness. "
            "Implementations should validate all curve parameters before use and reject non-standard or deprecated curves. "
            "Compliance with relevant standards ensures interoperability and security."
        ),
        key_factors=[
            "Curve origin and transparency",
            "Resistance to known attacks",
            "Parameter validation",
            "Standardization and interoperability",
            "Community scrutiny"
        ],
        primary_authority=[
            "NIST SP 800-186",
            "RFC 7748",
            "SafeCurves Project"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Non-standard or weak curves may contain backdoors or be vulnerable to attacks.",
        counter_arguments=[
            "Standardized curves are widely analyzed and trusted.",
            "Transparent parameter generation reduces risk.",
            "Ongoing research monitors for new vulnerabilities."
        ],
        resolution_strategy="Use only standardized, widely accepted curves with transparent parameters.",
        entity_scope="Cryptographic libraries, protocol designers",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-186 Section 3"
    ),
    DoctrineBlock(
        topic="Cryptographically Secure Random Number Generation",
        keywords=["random number", "CSPRNG", "entropy", "cryptography", "security"],
        conclusion_template="Random numbers used in cryptographic applications must be generated using cryptographically secure methods with sufficient entropy.",
        reasoning_framework=(
            "The unpredictability of cryptographic keys, nonces, and other secret values depends on the quality of the random number generator (RNG). "
            "Cryptographically secure pseudorandom number generators (CSPRNGs) are designed to withstand prediction and backtracking attacks. "
            "CSPRNGs must be seeded with sufficient entropy from reliable sources, such as hardware RNGs or operating system entropy pools. "
            "Periodic reseeding and health checks are recommended to maintain security. "
            "Weak or predictable RNGs have led to catastrophic failures in deployed cryptosystems. "
            "Compliance with standards such as NIST SP 800-90A ensures best practices are followed. "
            "Implementations should avoid using general-purpose PRNGs for cryptographic purposes."
        ),
        key_factors=[
            "Entropy source quality",
            "CSPRNG design and implementation",
            "Seeding and reseeding procedures",
            "Monitoring and health checks",
            "Compliance with standards"
        ],
        primary_authority=[
            "NIST SP 800-90A",
            "RFC 4086",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Implementer of cryptographic system",
        adversary_position="Insufficient entropy or flawed RNG design can lead to predictable outputs.",
        counter_arguments=[
            "Hardware entropy sources and OS pools provide robust entropy.",
            "CSPRNGs are designed to resist state compromise.",
            "Regular audits and testing mitigate risks."
        ],
        resolution_strategy="Follow established standards for RNG design and use; monitor entropy sources.",
        entity_scope="Cryptographic libraries, key generation modules",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-90A Section 10"
    ),
    DoctrineBlock(
        topic="Hash Function Security",
        keywords=["hash function", "collision resistance", "preimage resistance", "cryptography"],
        conclusion_template="Cryptographic hash functions must provide collision, preimage, and second preimage resistance for secure use.",
        reasoning_framework=(
            "Hash functions are used for data integrity, digital signatures, and password storage. "
            "A secure hash function must make it computationally infeasible to find two distinct inputs with the same output (collision resistance), "
            "to find an input that hashes to a given output (preimage resistance), or to find a second input that hashes to the same output as a given input (second preimage resistance). "
            "Broken or weak hash functions (e.g., MD5, SHA-1) are vulnerable to attacks and should be avoided. "
            "Modern hash functions (e.g., SHA-256, SHA-3) are recommended. "
            "Hash output length must be sufficient to resist birthday and brute-force attacks. "
            "Hash function selection should follow current cryptographic standards and best practices."
        ),
        key_factors=[
            "Hash function selection",
            "Output length",
            "Resistance to known attacks",
            "Standardization",
            "Implementation correctness"
        ],
        primary_authority=[
            "NIST FIPS 180-4",
            "NIST FIPS 202",
            "RFC 6234"
        ],
        burden_holder="Implementer, protocol designer",
        adversary_position="Weak hash functions can be exploited for collisions or preimage attacks.",
        counter_arguments=[
            "Modern hash functions are widely analyzed and trusted.",
            "Transition plans exist for deprecated functions.",
            "Output length can be increased for higher security."
        ],
        resolution_strategy="Use only current, standardized hash functions with sufficient output length.",
        entity_scope="Cryptographic protocols, libraries",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NIST FIPS 180-4 Section 4"
    ),
    DoctrineBlock(
        topic="Key Derivation Functions (KDFs)",
        keywords=["KDF", "key derivation", "PBKDF2", "HKDF", "cryptography"],
        conclusion_template="Key derivation functions must be used to derive cryptographic keys from passwords or shared secrets, employing salt and iteration to resist attacks.",
        reasoning_framework=(
            "KDFs are used to derive strong cryptographic keys from passwords, passphrases, or shared secrets. "
            "They must incorporate a salt to prevent precomputed attacks (e.g., rainbow tables) and use multiple iterations to slow down brute-force attempts. "
            "Functions such as PBKDF2, scrypt, and Argon2 are widely recommended. "
            "KDFs must be parameterized according to the threat model: higher iteration counts and memory requirements increase resistance to attacks. "
            "For key agreement protocols, KDFs such as HKDF are used to derive session keys from shared secrets. "
            "KDF selection and parameterization must follow current standards and be regularly reviewed."
        ),
        key_factors=[
            "Salt usage",
            "Iteration count",
            "Memory hardness",
            "Standardization",
            "Threat model"
        ],
        primary_authority=[
            "NIST SP 800-132",
            "RFC 8018",
            "Password Hashing Competition"
        ],
        burden_holder="Implementer, protocol designer",
        adversary_position="Weak KDFs or poor parameters enable brute-force or precomputed attacks.",
        counter_arguments=[
            "Modern KDFs are designed to resist such attacks.",
            "Parameters can be tuned for higher security.",
            "Regular reviews ensure ongoing protection."
        ],
        resolution_strategy="Use standardized KDFs with appropriate parameters for the application.",
        entity_scope="Authentication systems, key management modules",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-132 Section 5"
    ),
    DoctrineBlock(
        topic="Side-Channel Attack Mitigation",
        keywords=["side-channel", "timing attack", "power analysis", "mitigation", "cryptography"],
        conclusion_template="Cryptographic implementations must be designed to resist side-channel attacks, including timing and power analysis.",
        reasoning_framework=(
            "Side-channel attacks exploit information leaked by the physical implementation of cryptographic algorithms, such as timing, power consumption, or electromagnetic emissions. "
            "Common attacks include timing attacks on modular exponentiation, differential power analysis, and cache attacks. "
            "Mitigations include constant-time algorithm implementations, masking, blinding, and hardware countermeasures. "
            "Software must avoid data-dependent branching and memory access patterns. "
            "Regular audits and testing for side-channel vulnerabilities are essential. "
            "Compliance with standards such as ISO/IEC 19790 is recommended for high-assurance systems."
        ),
        key_factors=[
            "Implementation technique",
            "Constant-time operation",
            "Physical security measures",
            "Testing and validation",
            "Compliance with standards"
        ],
        primary_authority=[
            "ISO/IEC 19790",
            "NIST SP 800-90B",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Implementer, hardware designer",
        adversary_position="Unprotected implementations may leak secret information via side channels.",
        counter_arguments=[
            "Constant-time and masked implementations reduce leakage.",
            "Hardware countermeasures are available.",
            "Regular testing detects vulnerabilities."
        ],
        resolution_strategy="Adopt constant-time techniques and conduct regular side-channel resistance testing.",
        entity_scope="Cryptographic hardware, software libraries",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="ISO/IEC 19790 Section 7.5"
    ),
    DoctrineBlock(
        topic="Forward Secrecy in Key Exchange",
        keywords=["forward secrecy", "key exchange", "ephemeral keys", "cryptography"],
        conclusion_template="Key exchange protocols must provide forward secrecy to ensure past communications remain secure even if long-term keys are compromised.",
        reasoning_framework=(
            "Forward secrecy (FS) ensures that the compromise of long-term keys does not compromise the confidentiality of past session keys. "
            "Protocols such as ephemeral Diffie-Hellman (DHE, ECDHE) provide FS by generating new ephemeral key pairs for each session. "
            "FS is critical for protecting sensitive communications against future key compromise. "
            "Protocols must avoid static key exchanges and ensure proper ephemeral key generation and disposal. "
            "FS is now a standard requirement in modern secure communication protocols (e.g., TLS 1.3)."
        ),
        key_factors=[
            "Ephemeral key generation",
            "Protocol design",
            "Key disposal",
            "Compliance with standards",
            "Threat model"
        ],
        primary_authority=[
            "RFC 8446",
            "NIST SP 800-56A",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Without FS, compromise of long-term keys exposes all past sessions.",
        counter_arguments=[
            "Ephemeral key exchanges are widely supported.",
            "FS is mandated in modern protocols.",
            "Proper key disposal ensures security."
        ],
        resolution_strategy="Use ephemeral key exchange mechanisms and enforce FS in protocol design.",
        entity_scope="Secure communication protocols, key management",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="RFC 8446 Section 7.2"
    ),
    DoctrineBlock(
        topic="Padding Oracle Attack Prevention",
        keywords=["padding oracle", "CBC mode", "encryption", "attack prevention", "cryptography"],
        conclusion_template="Implementations of block cipher modes with padding must prevent padding oracle attacks by avoiding distinguishable error messages.",
        reasoning_framework=(
            "Padding oracle attacks exploit differences in error messages or response times when decrypting improperly padded ciphertexts. "
            "CBC mode encryption with PKCS#7 padding is particularly vulnerable if error messages reveal whether padding is correct. "
            "Attackers can use this information to decrypt ciphertexts without the key. "
            "Mitigations include using authenticated encryption modes (e.g., GCM, CCM), ensuring uniform error responses, and avoiding detailed error messages. "
            "Implementations must be audited for side-channel leaks related to padding errors."
        ),
        key_factors=[
            "Error message uniformity",
            "Authenticated encryption usage",
            "Implementation audits",
            "Protocol design",
            "Threat awareness"
        ],
        primary_authority=[
            "RFC 5246",
            "NIST SP 800-38A",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Implementer, protocol designer",
        adversary_position="Improper error handling enables attackers to decrypt data via padding oracle attacks.",
        counter_arguments=[
            "Authenticated encryption eliminates the attack vector.",
            "Uniform error responses mitigate the risk.",
            "Regular audits detect vulnerabilities."
        ],
        resolution_strategy="Use authenticated encryption and ensure uniform error handling in implementations.",
        entity_scope="Encryption libraries, protocol implementations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="RFC 5246 Section 6.2.3.2"
    ),
    DoctrineBlock(
        topic="Authenticated Encryption with Associated Data (AEAD)",
        keywords=["AEAD", "authenticated encryption", "GCM", "CCM", "cryptography"],
        conclusion_template="AEAD modes must be used to provide both confidentiality and integrity for encrypted data and associated metadata.",
        reasoning_framework=(
            "AEAD schemes, such as AES-GCM and AES-CCM, provide both encryption and authentication in a single operation. "
            "They protect not only the confidentiality of the plaintext but also the integrity of both the ciphertext and associated data (e.g., headers). "
            "AEAD modes prevent attacks that exploit the lack of authentication, such as ciphertext manipulation or replay. "
            "Proper nonce management is critical: nonces must be unique for each encryption under a given key. "
            "AEAD is now a standard requirement in modern protocols (e.g., TLS 1.3, QUIC)."
        ),
        key_factors=[
            "Nonce uniqueness",
            "Mode selection",
            "Implementation correctness",
            "Standard compliance",
            "Associated data handling"
        ],
        primary_authority=[
            "NIST SP 800-38D",
            "RFC 5116",
            "RFC 8439"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Non-AEAD modes or nonce reuse can compromise confidentiality and integrity.",
        counter_arguments=[
            "AEAD modes are widely available and standardized.",
            "Proper nonce management prevents related attacks.",
            "Protocols now mandate AEAD usage."
        ],
        resolution_strategy="Use AEAD modes exclusively and enforce nonce uniqueness.",
        entity_scope="Encryption libraries, secure protocols",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-38D Section 8"
    ),
    DoctrineBlock(
        topic="Public Key Validation",
        keywords=["public key", "validation", "cryptography", "protocols"],
        conclusion_template="All public keys must be validated for correct structure and group membership before use in cryptographic operations.",
        reasoning_framework=(
            "Public key validation is essential to prevent attacks that exploit malformed or invalid keys. "
            "For elliptic curve keys, validation includes checking that the point is on the curve, has the correct order, and is not the point at infinity. "
            "For RSA, modulus and exponent must be within valid ranges. "
            "Failure to validate can enable small subgroup attacks, invalid curve attacks, or other exploits. "
            "Validation procedures must follow standards and be implemented consistently."
        ),
        key_factors=[
            "Key structure",
            "Group membership",
            "Order validation",
            "Standard compliance",
            "Implementation correctness"
        ],
        primary_authority=[
            "NIST SP 800-56A",
            "RFC 5280",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Implementer, protocol designer",
        adversary_position="Unvalidated keys may allow attackers to compromise security.",
        counter_arguments=[
            "Validation procedures are well-defined and standardized.",
            "Automated tools can assist in validation.",
            "Regular audits reinforce compliance."
        ],
        resolution_strategy="Implement comprehensive public key validation as specified in standards.",
        entity_scope="Cryptographic libraries, protocol implementations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-56A Section 5.6.2"
    ),
    DoctrineBlock(
        topic="Certificate Chain Validation",
        keywords=["certificate", "chain", "validation", "PKI", "cryptography"],
        conclusion_template="Certificate chains must be validated from end-entity to trusted root, including signature, revocation, and policy checks.",
        reasoning_framework=(
            "Public Key Infrastructure (PKI) relies on certificate chains to establish trust. "
            "Validation involves verifying digital signatures, checking certificate validity periods, ensuring no revoked certificates are present, and enforcing policy constraints. "
            "Revocation status is checked via CRLs or OCSP. "
            "All steps must be performed in the correct order, and failures at any stage must result in rejection. "
            "Implementations must follow standards such as RFC 5280 and be robust against malformed or malicious certificates."
        ),
        key_factors=[
            "Signature verification",
            "Validity period checks",
            "Revocation status",
            "Policy enforcement",
            "Standard compliance"
        ],
        primary_authority=[
            "RFC 5280",
            "NIST SP 800-57",
            "CA/Browser Forum Baseline Requirements"
        ],
        burden_holder="Implementer, relying party",
        adversary_position="Improper validation can allow forged or revoked certificates to be accepted.",
        counter_arguments=[
            "Standardized validation procedures are widely implemented.",
            "Automated tools assist in validation.",
            "Regular audits detect misconfigurations."
        ],
        resolution_strategy="Follow comprehensive validation procedures as specified in standards.",
        entity_scope="PKI clients, certificate validation libraries",
        confidence=0.99,
        confidence_zone="High",
        controlling_precedent="RFC 5280 Section 6"
    ),
    DoctrineBlock(
        topic="Key Length Recommendations",
        keywords=["key length", "security level", "cryptography", "recommendation"],
        conclusion_template="Cryptographic key lengths must meet or exceed current recommendations to provide adequate security against brute-force attacks.",
        reasoning_framework=(
            "The security of cryptographic algorithms is directly related to key length. "
            "Short keys are vulnerable to brute-force attacks. "
            "Current recommendations specify minimum key lengths for symmetric (e.g., 128 bits for AES), RSA (2048 bits), and ECC (256 bits) algorithms. "
            "Key lengths should be chosen based on the desired security level and anticipated advances in computing power. "
            "Quantum computing may necessitate longer keys or quantum-resistant algorithms."
        ),
        key_factors=[
            "Algorithm type",
            "Desired security level",
            "Anticipated threat model",
            "Standard recommendations",
            "Quantum computing considerations"
        ],
        primary_authority=[
            "NIST SP 800-57",
            "ENISA Algorithms, Key Size and Parameters Report",
            "RFC 3766"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Insufficient key lengths may be brute-forced by adversaries.",
        counter_arguments=[
            "Current recommendations provide adequate security margins.",
            "Key lengths can be increased as needed.",
            "Transition plans exist for quantum-safe algorithms."
        ],
        resolution_strategy="Adhere to current key length recommendations and monitor for updates.",
        entity_scope="Cryptographic protocols, key management",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-57 Part 1 Table 2"
    ),
    DoctrineBlock(
        topic="Quantum-Resistant Cryptography",
        keywords=["quantum", "post-quantum", "cryptography", "resistance"],
        conclusion_template="Cryptographic systems must transition to quantum-resistant algorithms to maintain security in the presence of quantum adversaries.",
        reasoning_framework=(
            "Quantum computers threaten classical cryptographic algorithms such as RSA, DSA, and ECC via Shor's algorithm. "
            "Symmetric algorithms are less affected but may require increased key lengths. "
            "NIST and other organizations are standardizing post-quantum algorithms (e.g., lattice-based, hash-based, code-based). "
            "Transition planning is essential to ensure long-term security. "
            "Hybrid schemes may be used during the transition period."
        ),
        key_factors=[
            "Algorithm selection",
            "Standardization status",
            "Transition planning",
            "Hybrid scheme support",
            "Threat assessment"
        ],
        primary_authority=[
            "NIST Post-Quantum Cryptography Project",
            "ENISA Post-Quantum Cryptography Study",
            "RFC 7696"
        ],
        burden_holder="Protocol designer, implementer, organization",
        adversary_position="Quantum computers will break classical public-key cryptography.",
        counter_arguments=[
            "Post-quantum algorithms are being standardized.",
            "Hybrid schemes provide interim protection.",
            "Symmetric key lengths can be increased."
        ],
        resolution_strategy="Adopt quantum-resistant algorithms as they become standardized; plan for migration.",
        entity_scope="All cryptographic systems",
        confidence=0.95,
        confidence_zone="Medium-High",
        controlling_precedent="NIST PQC Project"
    ),
    DoctrineBlock(
        topic="Digital Signature Scheme Selection",
        keywords=["digital signature", "scheme", "selection", "cryptography"],
        conclusion_template="Digital signature schemes must be selected based on security, efficiency, and compliance with current standards.",
        reasoning_framework=(
            "Digital signatures provide authentication, integrity, and non-repudiation. "
            "Common schemes include RSA, DSA, ECDSA, and EdDSA. "
            "Selection depends on security requirements, performance, and interoperability. "
            "Schemes must be implemented according to standards, and deprecated algorithms (e.g., DSA with small keys) should be avoided. "
            "Quantum-safe signature schemes are under development."
        ),
        key_factors=[
            "Algorithm security",
            "Performance",
            "Standardization",
            "Interoperability",
            "Quantum resistance"
        ],
        primary_authority=[
            "NIST FIPS 186-4",
            "RFC 8032",
            "NIST PQC Project"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Weak or deprecated signature schemes may be forgeable.",
        counter_arguments=[
            "Modern schemes are widely supported and standardized.",
            "Transition plans exist for quantum-safe signatures.",
            "Performance and security can be balanced."
        ],
        resolution_strategy="Select signature schemes based on current standards and security requirements.",
        entity_scope="Authentication protocols, digital signature libraries",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NIST FIPS 186-4 Section 4"
    ),
    DoctrineBlock(
        topic="Zero-Knowledge Proof Soundness",
        keywords=["zero-knowledge", "proof", "soundness", "cryptography"],
        conclusion_template="Zero-knowledge proofs must be constructed to ensure soundness, completeness, and zero-knowledge properties.",
        reasoning_framework=(
            "Zero-knowledge proofs (ZKPs) allow one party to prove knowledge of a secret without revealing it. "
            "Soundness ensures that a cheating prover cannot convince the verifier of a false statement. "
            "Completeness ensures that honest provers can convince honest verifiers. "
            "Zero-knowledge ensures that no information about the secret is leaked. "
            "Protocols must be carefully designed and analyzed to ensure these properties, and implementation errors can compromise security."
        ),
        key_factors=[
            "Protocol design",
            "Security proofs",
            "Implementation correctness",
            "Threat model",
            "Standardization"
        ],
        primary_authority=[
            "Goldwasser, Micali, Rackoff (1985)",
            "NIST ZKP Study",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Flawed ZKPs may leak information or allow false proofs.",
        counter_arguments=[
            "Formal security proofs provide assurance.",
            "Standardized protocols are available.",
            "Implementation reviews detect flaws."
        ],
        resolution_strategy="Use well-studied ZKP protocols with formal proofs and validated implementations.",
        entity_scope="Privacy-preserving protocols, authentication systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Goldwasser et al. 1985"
    ),
    DoctrineBlock(
        topic="Key Escrow Avoidance",
        keywords=["key escrow", "avoidance", "cryptography", "privacy"],
        conclusion_template="Cryptographic systems must avoid key escrow mechanisms unless strictly required by law and implemented with strong safeguards.",
        reasoning_framework=(
            "Key escrow involves storing copies of cryptographic keys with a trusted third party. "
            "While sometimes required for regulatory compliance, key escrow introduces significant risks, including unauthorized access, insider threats, and loss of privacy. "
            "Best practice is to avoid key escrow unless mandated by law. "
            "If implemented, strong technical and organizational safeguards must be in place, including multi-party controls, audit trails, and legal oversight."
        ),
        key_factors=[
            "Legal requirements",
            "Risk assessment",
            "Safeguard strength",
            "Transparency",
            "User consent"
        ],
        primary_authority=[
            "ENISA Key Management Guidelines",
            "NIST SP 800-57",
            "IETF Best Practices"
        ],
        burden_holder="Organization, implementer",
        adversary_position="Key escrow increases risk of unauthorized decryption and privacy loss.",
        counter_arguments=[
            "Strong safeguards can mitigate some risks.",
            "Legal compliance may require escrow.",
            "Transparency and oversight are essential."
        ],
        resolution_strategy="Avoid key escrow unless legally required; implement strong safeguards if necessary.",
        entity_scope="Enterprise key management, compliance systems",
        confidence=0.94,
        confidence_zone="Medium-High",
        controlling_precedent="ENISA Key Management Guidelines Section 4.3"
    ),
    DoctrineBlock(
        topic="Password Storage Best Practices",
        keywords=["password", "storage", "hashing", "best practices", "cryptography"],
        conclusion_template="Passwords must be stored using salted, slow, and memory-hard hash functions to resist offline attacks.",
        reasoning_framework=(
            "Storing plaintext or unsalted password hashes exposes users to offline attacks. "
            "Best practice is to use a unique salt for each password and a slow, memory-hard hash function (e.g., bcrypt, scrypt, Argon2). "
            "This increases the cost of brute-force and dictionary attacks. "
            "Regular review of storage practices and migration to stronger algorithms is recommended."
        ),
        key_factors=[
            "Salt usage",
            "Hash function selection",
            "Iteration and memory parameters",
            "Migration planning",
            "Implementation correctness"
        ],
        primary_authority=[
            "OWASP Password Storage Cheat Sheet",
            "NIST SP 800-63B",
            "Password Hashing Competition"
        ],
        burden_holder="System designer, implementer",
        adversary_position="Weak or unsalted hashes enable rapid offline attacks.",
        counter_arguments=[
            "Modern hash functions are designed for password storage.",
            "Salting and iteration slow down attacks.",
            "Migration plans address legacy storage."
        ],
        resolution_strategy="Use salted, slow, memory-hard hash functions and regularly review storage practices.",
        entity_scope="Authentication systems, user databases",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="OWASP Password Storage Cheat Sheet"
    ),
    DoctrineBlock(
        topic="Nonce Management in Cryptography",
        keywords=["nonce", "management", "uniqueness", "cryptography"],
        conclusion_template="Nonces must be unique for each operation under a given key to prevent replay and related-key attacks.",
        reasoning_framework=(
            "Nonces (numbers used once) are used in encryption, authentication, and key exchange protocols. "
            "Nonce reuse can lead to catastrophic failures, such as plaintext recovery or key compromise. "
            "Implementations must ensure nonce uniqueness, either via counters, random generation, or protocol mechanisms. "
            "Protocols should specify nonce management strategies, and implementations must enforce them."
        ),
        key_factors=[
            "Nonce generation method",
            "Protocol requirements",
            "Implementation correctness",
            "Replay prevention",
            "Key management"
        ],
        primary_authority=[
            "NIST SP 800-38A",
            "RFC 5116",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Implementer, protocol designer",
        adversary_position="Nonce reuse enables replay or cryptanalytic attacks.",
        counter_arguments=[
            "Protocols specify nonce management.",
            "Automated tools can enforce uniqueness.",
            "Regular audits detect implementation errors."
        ],
        resolution_strategy="Specify and enforce nonce uniqueness for all cryptographic operations.",
        entity_scope="Encryption protocols, authentication systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-38A Section 7"
    ),
    DoctrineBlock(
        topic="Random Oracle Model Applicability",
        keywords=["random oracle", "model", "applicability", "cryptography"],
        conclusion_template="The random oracle model is a useful abstraction for security proofs, but real-world hash functions may not fully realize its properties.",
        reasoning_framework=(
            "The random oracle model (ROM) treats hash functions as idealized random functions. "
            "Many cryptographic protocols are proven secure in the ROM, but real hash functions are deterministic and may have structural weaknesses. "
            "Security proofs in the ROM provide heuristic assurance, but do not guarantee real-world security. "
            "Protocol designers must consider the limitations of the ROM and select hash functions with strong empirical security."
        ),
        key_factors=[
            "Model limitations",
            "Hash function selection",
            "Security proof interpretation",
            "Empirical analysis",
            "Threat model"
        ],
        primary_authority=[
            "Bellare and Rogaway (1993)",
            "Handbook of Applied Cryptography",
            "NIST FIPS 180-4"
        ],
        burden_holder="Protocol designer, cryptanalyst",
        adversary_position="ROM proofs may not translate to real-world security.",
        counter_arguments=[
            "ROM provides a useful design tool.",
            "Empirical analysis supplements theoretical proofs.",
            "Protocols can be updated if weaknesses are found."
        ],
        resolution_strategy="Interpret ROM proofs cautiously and select robust hash functions.",
        entity_scope="Cryptographic protocol design",
        confidence=0.93,
        confidence_zone="Medium-High",
        controlling_precedent="Bellare and Rogaway 1993"
    ),
    DoctrineBlock(
        topic="Key Separation Principle",
        keywords=["key separation", "principle", "cryptography"],
        conclusion_template="Different cryptographic keys must be used for different purposes to prevent cross-protocol attacks.",
        reasoning_framework=(
            "Using the same key for multiple cryptographic purposes (e.g., encryption and authentication) can enable attacks that exploit interactions between protocols. "
            "Key separation ensures that compromise or misuse in one context does not affect others. "
            "Protocols should derive separate keys for each function using KDFs. "
            "Key separation is a fundamental principle in secure protocol design."
        ),
        key_factors=[
            "Protocol design",
            "KDF usage",
            "Threat model",
            "Implementation correctness",
            "Compliance with standards"
        ],
        primary_authority=[
            "NIST SP 800-56C",
            "RFC 5869",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Key reuse across functions enables cross-protocol attacks.",
        counter_arguments=[
            "KDFs facilitate key separation.",
            "Protocols can enforce separation.",
            "Audits detect key misuse."
        ],
        resolution_strategy="Derive and use separate keys for each cryptographic purpose.",
        entity_scope="Protocol design, key management",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-56C Section 4"
    ),
    DoctrineBlock(
        topic="Replay Attack Prevention",
        keywords=["replay attack", "prevention", "cryptography"],
        conclusion_template="Protocols must include mechanisms to detect and prevent replay attacks, such as nonces, timestamps, or sequence numbers.",
        reasoning_framework=(
            "Replay attacks involve retransmitting valid messages to trick a system into performing unauthorized actions. "
            "Prevention mechanisms include using nonces, timestamps, or sequence numbers to ensure message freshness. "
            "Protocols must specify how to handle duplicates and expired messages. "
            "Implementations must enforce these mechanisms and audit for compliance."
        ),
        key_factors=[
            "Freshness mechanism",
            "Protocol specification",
            "Implementation enforcement",
            "Auditability",
            "Threat model"
        ],
        primary_authority=[
            "RFC 4949",
            "NIST SP 800-63B",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Lack of replay prevention enables unauthorized actions.",
        counter_arguments=[
            "Standard mechanisms are widely implemented.",
            "Audits detect protocol weaknesses.",
            "Freshness checks are efficient."
        ],
        resolution_strategy="Specify and enforce replay prevention mechanisms in all protocols.",
        entity_scope="Authentication protocols, secure messaging",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="RFC 4949 Section 5"
    ),
    DoctrineBlock(
        topic="Key Agreement Protocol Security",
        keywords=["key agreement", "protocol", "security", "cryptography"],
        conclusion_template="Key agreement protocols must ensure mutual authentication, forward secrecy, and resistance to known attacks.",
        reasoning_framework=(
            "Key agreement protocols establish shared secrets between parties. "
            "Security requirements include mutual authentication, forward secrecy, and resistance to man-in-the-middle, replay, and downgrade attacks. "
            "Protocols such as TLS 1.3 and IKEv2 incorporate these features. "
            "Implementations must follow protocol specifications and be regularly audited."
        ),
        key_factors=[
            "Mutual authentication",
            "Forward secrecy",
            "Attack resistance",
            "Protocol compliance",
            "Implementation correctness"
        ],
        primary_authority=[
            "RFC 8446",
            "NIST SP 800-56A",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Weak protocols may allow key compromise or impersonation.",
        counter_arguments=[
            "Modern protocols address known attacks.",
            "Regular audits ensure compliance.",
            "Protocol updates address new threats."
        ],
        resolution_strategy="Use standardized, audited key agreement protocols with required security properties.",
        entity_scope="Secure communication protocols",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="RFC 8446 Section 7.2"
    ),
    DoctrineBlock(
        topic="Cryptographic Agility",
        keywords=["cryptographic agility", "algorithm agility", "cryptography"],
        conclusion_template="Systems must be designed for cryptographic agility, allowing algorithms to be updated or replaced as needed.",
        reasoning_framework=(
            "Cryptographic agility enables systems to transition to new algorithms in response to advances in cryptanalysis or changes in standards. "
            "Hardcoding algorithms or parameters makes updates difficult and increases long-term risk. "
            "Protocols should negotiate algorithms and support migration paths. "
            "Agility is essential for responding to deprecations and emerging threats."
        ),
        key_factors=[
            "Algorithm negotiation",
            "Migration planning",
            "Protocol design",
            "Implementation flexibility",
            "Threat monitoring"
        ],
        primary_authority=[
            "NIST SP 800-131A",
            "RFC 7696",
            "ENISA Algorithms, Key Size and Parameters Report"
        ],
        burden_holder="System architect, protocol designer",
        adversary_position="Lack of agility leads to insecure legacy systems.",
        counter_arguments=[
            "Agility is widely supported in modern protocols.",
            "Migration paths are documented.",
            "Threat monitoring informs updates."
        ],
        resolution_strategy="Design systems for algorithm agility and plan for regular updates.",
        entity_scope="All cryptographic systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-131A Section 3"
    ),
    DoctrineBlock(
        topic="Certificate Revocation Checking",
        keywords=["certificate", "revocation", "checking", "PKI", "cryptography"],
        conclusion_template="Certificate revocation status must be checked using CRLs or OCSP before accepting certificates.",
        reasoning_framework=(
            "Revoked certificates must not be trusted, as they may have been compromised or expired. "
            "Revocation status is checked using Certificate Revocation Lists (CRLs) or the Online Certificate Status Protocol (OCSP). "
            "Implementations must handle network failures and soft-fail policies carefully to avoid accepting revoked certificates. "
            "Regular updates and audits are necessary to maintain trust."
        ),
        key_factors=[
            "Revocation mechanism",
            "Network reliability",
            "Policy enforcement",
            "Auditability",
            "Standard compliance"
        ],
        primary_authority=[
            "RFC 5280",
            "CA/Browser Forum Baseline Requirements",
            "NIST SP 800-57"
        ],
        burden_holder="Relying party, implementer",
        adversary_position="Failure to check revocation enables use of compromised certificates.",
        counter_arguments=[
            "CRLs and OCSP are widely supported.",
            "Soft-fail policies can be tuned for risk tolerance.",
            "Audits detect misconfigurations."
        ],
        resolution_strategy="Implement robust revocation checking and regularly audit certificate validation.",
        entity_scope="PKI clients, certificate validation libraries",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="RFC 5280 Section 6.3"
    ),
    DoctrineBlock(
        topic="Cryptographic Parameter Validation",
        keywords=["parameter", "validation", "cryptography"],
        conclusion_template="All cryptographic parameters must be validated for correctness and security before use.",
        reasoning_framework=(
            "Parameters such as group orders, curve coefficients, and key sizes must be validated to prevent attacks that exploit weak or malformed parameters. "
            "Validation includes checking for compliance with standards, resistance to known attacks, and suitability for the intended use. "
            "Automated tools and libraries can assist in parameter validation."
        ),
        key_factors=[
            "Parameter correctness",
            "Standard compliance",
            "Attack resistance",
            "Automation",
            "Implementation correctness"
        ],
        primary_authority=[
            "NIST SP 800-56A",
            "RFC 7748",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Implementer, protocol designer",
        adversary_position="Weak or malformed parameters may enable attacks.",
        counter_arguments=[
            "Standardized parameters are widely available.",
            "Automated validation tools exist.",
            "Regular audits reinforce compliance."
        ],
        resolution_strategy="Validate all parameters against standards and known attack vectors.",
        entity_scope="Cryptographic libraries, protocol implementations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-56A Section 5.6.2"
    ),
    DoctrineBlock(
        topic="Implementation-Induced Vulnerabilities",
        keywords=["implementation", "vulnerability", "cryptography", "side-channel"],
        conclusion_template="Implementation errors, including side-channel leaks and incorrect protocol flows, must be identified and mitigated through rigorous testing and review.",
        reasoning_framework=(
            "Even mathematically secure algorithms can be compromised by implementation flaws. "
            "Common issues include side-channel leaks, incorrect error handling, and failure to follow protocol specifications. "
            "Rigorous code review, automated testing, and formal verification can identify and mitigate these vulnerabilities. "
            "Regular updates and security audits are essential."
        ),
        key_factors=[
            "Code review",
            "Testing coverage",
            "Formal verification",
            "Audit frequency",
            "Implementation correctness"
        ],
        primary_authority=[
            "NIST SP 800-53",
            "ISO/IEC 27001",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Developer, security auditor",
        adversary_position="Implementation flaws can be exploited regardless of algorithm strength.",
        counter_arguments=[
            "Rigorous review and testing mitigate risks.",
            "Automated tools assist in detection.",
            "Formal methods provide additional assurance."
        ],
        resolution_strategy="Adopt rigorous development and testing practices for all cryptographic implementations.",
        entity_scope="Software and hardware cryptographic modules",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-53 Section SI-3"
    ),
    DoctrineBlock(
        topic="Cryptographic Module Validation",
        keywords=["module", "validation", "FIPS 140", "cryptography"],
        conclusion_template="Cryptographic modules must be validated against recognized standards (e.g., FIPS 140-3) for use in regulated environments.",
        reasoning_framework=(
            "Validation of cryptographic modules ensures compliance with security requirements and regulatory standards. "
            "FIPS 140-3 specifies requirements for cryptographic modules used by US federal agencies. "
            "Validation involves testing for correct implementation, resistance to attacks, and secure key management. "
            "Validated modules provide assurance to users and regulators."
        ),
        key_factors=[
            "Standard compliance",
            "Testing and certification",
            "Key management",
            "Attack resistance",
            "Regulatory requirements"
        ],
        primary_authority=[
            "FIPS 140-3",
            "ISO/IEC 19790",
            "NIST SP 800-140A"
        ],
        burden_holder="Module developer, organization",
        adversary_position="Unvalidated modules may not meet security or regulatory requirements.",
        counter_arguments=[
            "Validation provides assurance and trust.",
            "Certification processes are well-established.",
            "Regular updates maintain compliance."
        ],
        resolution_strategy="Use validated cryptographic modules where required and maintain certification.",
        entity_scope="Regulated environments, government systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FIPS 140-3 Section 2"
    ),
    DoctrineBlock(
        topic="Key Lifecycle Management",
        keywords=["key lifecycle", "management", "generation", "destruction", "cryptography"],
        conclusion_template="Cryptographic keys must be securely generated, distributed, stored, rotated, and destroyed according to lifecycle management best practices.",
        reasoning_framework=(
            "Effective key management is critical to cryptographic security. "
            "The key lifecycle includes generation, distribution, storage, usage, rotation, archival, and destruction. "
            "Each phase must be secured against unauthorized access and loss. "
            "Automated key management systems and hardware security modules (HSMs) can assist in enforcing policies. "
            "Lifecycle management must comply with relevant standards and regulatory requirements."
        ),
        key_factors=[
            "Secure key generation",
            "Distribution and storage",
            "Rotation and archival",
            "Destruction procedures",
            "Policy enforcement"
        ],
        primary_authority=[
            "NIST SP 800-57",
            "ISO/IEC 11770",
            "ENISA Key Management Guidelines"
        ],
        burden_holder="Key custodian, organization",
        adversary_position="Poor key management can lead to key compromise or loss.",
        counter_arguments=[
            "Lifecycle management best practices are well-documented.",
            "Automated systems enforce policies.",
            "Regular audits ensure compliance."
        ],
        resolution_strategy="Implement comprehensive key lifecycle management policies and automate enforcement.",
        entity_scope="Enterprise key management, cryptographic systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-57 Part 1 Section 5"
    ),
    DoctrineBlock(
        topic="Entropy Assessment for Cryptographic Operations",
        keywords=["entropy", "assessment", "randomness", "cryptography"],
        conclusion_template="Entropy sources must be assessed for quality and sufficiency before use in cryptographic operations.",
        reasoning_framework=(
            "Entropy is essential for secure key generation, nonces, and random values. "
            "Sources of entropy must be unpredictable and resistant to manipulation. "
            "Assessment involves statistical testing and monitoring of entropy pools. "
            "Weak or insufficient entropy can lead to predictable outputs and compromise security. "
            "Standards specify requirements for entropy assessment and documentation."
        ),
        key_factors=[
            "Source unpredictability",
            "Statistical testing",
            "Monitoring and documentation",
            "Standard compliance",
            "Implementation correctness"
        ],
        primary_authority=[
            "NIST SP 800-90B",
            "ISO/IEC 18031",
            "RFC 4086"
        ],
        burden_holder="Implementer, system administrator",
        adversary_position="Poor entropy leads to predictable keys and values.",
        counter_arguments=[
            "Statistical tests detect weak sources.",
            "Hardware RNGs provide strong entropy.",
            "Regular monitoring maintains quality."
        ],
        resolution_strategy="Assess and monitor entropy sources according to standards.",
        entity_scope="Key generation, cryptographic modules",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-90B Section 3"
    ),
    DoctrineBlock(
        topic="Cryptographic Algorithm Deprecation",
        keywords=["algorithm", "deprecation", "transition", "cryptography"],
        conclusion_template="Deprecated cryptographic algorithms must be phased out in favor of secure, standardized alternatives.",
        reasoning_framework=(
            "Algorithms may be deprecated due to discovered vulnerabilities or advances in cryptanalysis. "
            "Continued use of deprecated algorithms exposes systems to unnecessary risk. "
            "Transition plans must be developed and executed to migrate to secure alternatives. "
            "Standards bodies regularly update lists of approved and deprecated algorithms."
        ),
        key_factors=[
            "Vulnerability assessment",
            "Transition planning",
            "Standard compliance",
            "Implementation updates",
            "User notification"
        ],
        primary_authority=[
            "NIST SP 800-131A",
            "ENISA Algorithms, Key Size and Parameters Report",
            "RFC 6151"
        ],
        burden_holder="System owner, implementer",
        adversary_position="Deprecated algorithms are vulnerable to attack.",
        counter_arguments=[
            "Transition plans minimize disruption.",
            "Standards provide guidance on alternatives.",
            "User education supports migration."
        ],
        resolution_strategy="Develop and execute transition plans to eliminate deprecated algorithms.",
        entity_scope="All cryptographic systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-131A Section 3"
    ),
    DoctrineBlock(
        topic="Multi-Party Computation Security",
        keywords=["multi-party computation", "MPC", "security", "cryptography"],
        conclusion_template="MPC protocols must ensure privacy, correctness, and robustness against collusion and active adversaries.",
        reasoning_framework=(
            "Multi-party computation (MPC) enables parties to jointly compute a function over their inputs while keeping those inputs private. "
            "Protocols must ensure privacy (inputs remain secret), correctness (outputs are accurate), and robustness (protocol completes despite adversarial behavior). "
            "Security proofs and rigorous analysis are required, and implementation must follow protocol specifications closely."
        ),
        key_factors=[
            "Protocol design",
            "Adversary model",
            "Security proofs",
            "Implementation correctness",
            "Standardization"
        ],
        primary_authority=[
            "Goldreich, Micali, Wigderson (1987)",
            "NIST MPC Study",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Weak protocols may leak inputs or allow incorrect outputs.",
        counter_arguments=[
            "Formal proofs provide assurance.",
            "Standardized protocols are available.",
            "Implementation reviews detect flaws."
        ],
        resolution_strategy="Use well-studied MPC protocols with formal proofs and validated implementations.",
        entity_scope="Privacy-preserving computation, collaborative systems",
        confidence=0.95,
        confidence_zone="Medium-High",
        controlling_precedent="Goldreich et al. 1987"
    ),
    DoctrineBlock(
        topic="Threshold Cryptography Security",
        keywords=["threshold cryptography", "secret sharing", "security", "cryptography"],
        conclusion_template="Threshold cryptosystems must ensure that no subset of participants below the threshold can reconstruct the secret.",
        reasoning_framework=(
            "Threshold cryptography splits a secret among multiple parties, requiring a minimum number (threshold) to reconstruct it. "
            "Schemes such as Shamir's Secret Sharing provide information-theoretic security. "
            "Protocols must prevent collusion below the threshold and ensure robustness against cheating participants. "
            "Implementation must handle key distribution, share verification, and secure reconstruction."
        ),
        key_factors=[
            "Threshold selection",
            "Collusion resistance",
            "Share verification",
            "Implementation correctness",
            "Standardization"
        ],
        primary_authority=[
            "Shamir (1979)",
            "NIST Threshold Cryptography Study",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Colluding participants may reconstruct the secret below the threshold.",
        counter_arguments=[
            "Information-theoretic security is achievable.",
            "Share verification detects cheating.",
            "Protocols can be audited for correctness."
        ],
        resolution_strategy="Use proven threshold schemes and validate implementation.",
        entity_scope="Key management, distributed systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="Shamir 1979"
    ),
    DoctrineBlock(
        topic="Cryptographic Backdoor Detection",
        keywords=["backdoor", "detection", "cryptography", "trust"],
        conclusion_template="Cryptographic systems must be analyzed for potential backdoors in algorithms, parameters, or implementations.",
        reasoning_framework=(
            "Backdoors may be introduced intentionally or unintentionally in cryptographic algorithms, parameters, or implementations. "
            "Detection involves transparency in parameter generation, public review of algorithms, and open-source implementations. "
            "Independent audits and reproducibility are essential for trust. "
            "Suspicious or opaque elements must be scrutinized and, if necessary, avoided."
        ),
        key_factors=[
            "Transparency",
            "Public review",
            "Auditability",
            "Reproducibility",
            "Community trust"
        ],
        primary_authority=[
            "ENISA Backdoor Study",
            "NIST SP 800-90A Revision 1",
            "SafeCurves Project"
        ],
        burden_holder="Algorithm designer, implementer, auditor",
        adversary_position="Undetected backdoors undermine all cryptographic assurances.",
        counter_arguments=[
            "Transparency and public review mitigate risk.",
            "Open-source implementations increase trust.",
            "Audits detect suspicious elements."
        ],
        resolution_strategy="Favor transparent, publicly reviewed algorithms and implementations; conduct regular audits.",
        entity_scope="All cryptographic systems",
        confidence=0.94,
        confidence_zone="Medium-High",
        controlling_precedent="ENISA Backdoor Study Section 3"
    ),
    DoctrineBlock(
        topic="Cryptographic Protocol Version Negotiation",
        keywords=["protocol", "version negotiation", "cryptography"],
        conclusion_template="Protocols must negotiate versions securely to prevent downgrade attacks.",
        reasoning_framework=(
            "Version negotiation allows parties to select the most secure protocol version supported by both. "
            "Downgrade attacks exploit negotiation to force use of weaker, deprecated versions. "
            "Protocols must authenticate version negotiation and reject insecure versions. "
            "Implementations must default to the highest supported version and log negotiation outcomes."
        ),
        key_factors=[
            "Negotiation authentication",
            "Default version selection",
            "Logging and monitoring",
            "Protocol specification",
            "Implementation correctness"
        ],
        primary_authority=[
            "RFC 8446",
            "NIST SP 800-52",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Downgrade attacks force use of insecure protocol versions.",
        counter_arguments=[
            "Authenticated negotiation prevents downgrades.",
            "Logging enables detection.",
            "Protocols specify secure negotiation procedures."
        ],
        resolution_strategy="Authenticate version negotiation and default to the most secure version.",
        entity_scope="Secure communication protocols",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="RFC 8446 Section 4.2.1"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Usage Constraints",
        keywords=["key usage", "constraints", "cryptography"],
        conclusion_template="Keys must be constrained to specific usages to prevent unintended or insecure operations.",
        reasoning_framework=(
            "Keys may be used for encryption, signing, authentication, or other purposes. "
            "Constraining keys to specific usages prevents misuse and reduces attack surface. "
            "Certificates and key management systems should enforce usage constraints via key usage extensions or policies."
        ),
        key_factors=[
            "Usage policy enforcement",
            "Certificate extensions",
            "Key management",
            "Auditability",
            "Standard compliance"
        ],
        primary_authority=[
            "RFC 5280",
            "NIST SP 800-57",
            "ISO/IEC 11770"
        ],
        burden_holder="Key custodian, implementer",
        adversary_position="Unconstrained keys may be misused for insecure operations.",
        counter_arguments=[
            "Usage constraints are widely supported.",
            "Policies can be enforced automatically.",
            "Audits detect misuse."
        ],
        resolution_strategy="Enforce key usage constraints in all key management and certificate systems.",
        entity_scope="Key management, PKI",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="RFC 5280 Section 4.2.1.3"
    ),
    DoctrineBlock(
        topic="Cryptographic Compliance Auditing",
        keywords=["compliance", "auditing", "cryptography"],
        conclusion_template="Regular compliance audits are required to ensure adherence to cryptographic standards and policies.",
        reasoning_framework=(
            "Compliance with cryptographic standards and organizational policies is essential for security and regulatory reasons. "
            "Regular audits verify correct implementation, usage, and management of cryptographic assets. "
            "Audit findings inform remediation and continuous improvement. "
            "Automated tools and third-party assessments can enhance audit effectiveness."
        ),
        key_factors=[
            "Audit frequency",
            "Scope and depth",
            "Remediation process",
            "Automation",
            "Third-party assessment"
        ],
        primary_authority=[
            "NIST SP 800-53",
            "ISO/IEC 27001",
            "ENISA Key Management Guidelines"
        ],
        burden_holder="Organization, auditor",
        adversary_position="Lack of audits allows non-compliance and undetected vulnerabilities.",
        counter_arguments=[
            "Audits are standard practice.",
            "Automation increases coverage.",
            "Remediation processes are well-established."
        ],
        resolution_strategy="Schedule and conduct regular compliance audits; act on findings.",
        entity_scope="All cryptographic systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-53 Section CA-2"
    ),
    DoctrineBlock(
        topic="Cryptographic Algorithm Interoperability",
        keywords=["algorithm", "interoperability", "cryptography"],
        conclusion_template="Algorithms and parameters must be selected to ensure interoperability between compliant implementations.",
        reasoning_framework=(
            "Interoperability ensures that different implementations of cryptographic protocols can communicate securely. "
            "Selection of standardized algorithms and parameters is essential. "
            "Protocols must specify algorithm suites and parameter formats. "
            "Testing and certification programs support interoperability."
        ),
        key_factors=[
            "Standardization",
            "Parameter formats",
            "Testing and certification",
            "Protocol specification",
            "Implementation correctness"
        ],
        primary_authority=[
            "RFC 8446",
            "NIST SP 800-56A",
            "ISO/IEC 19790"
        ],
        burden_holder="Protocol designer, implementer",
        adversary_position="Non-standard algorithms or parameters prevent secure communication.",
        counter_arguments=[
            "Standard suites are widely available.",
            "Certification programs support interoperability.",
            "Testing ensures compatibility."
        ],
        resolution_strategy="Select standardized algorithms and parameters; participate in interoperability testing.",
        entity_scope="Protocol design, cryptographic libraries",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="RFC 8446 Section 4.1"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Backup and Recovery",
        keywords=["key backup", "recovery", "cryptography"],
        conclusion_template="Key backup and recovery mechanisms must ensure confidentiality, integrity, and availability of cryptographic keys.",
        reasoning_framework=(
            "Loss of cryptographic keys can result in data loss or denial of service. "
            "Backup mechanisms must protect keys against unauthorized access while ensuring availability for recovery. "
            "Encryption, access controls, and audit trails are essential. "
            "Recovery procedures must be documented and tested regularly."
        ),
        key_factors=[
            "Backup encryption",
            "Access controls",
            "Auditability",
            "Recovery procedures",
            "Testing and documentation"
        ],
        primary_authority=[
            "NIST SP 800-57",
            "ISO/IEC 11770",
            "ENISA Key Management Guidelines"
        ],
        burden_holder="Key custodian, organization",
        adversary_position="Insecure backups may leak keys; lack of backups may cause data loss.",
        counter_arguments=[
            "Encryption and controls protect backups.",
            "Testing ensures recoverability.",
            "Audit trails detect unauthorized access."
        ],
        resolution_strategy="Implement secure backup and recovery procedures for all cryptographic keys.",
        entity_scope="Key management, enterprise systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-57 Part 1 Section 5.5"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Rotation",
        keywords=["key rotation", "lifetime", "cryptography"],
        conclusion_template="Keys must be rotated at regular intervals or upon suspicion of compromise to limit exposure.",
        reasoning_framework=(
            "Key rotation reduces the risk of long-term key compromise and limits the impact of potential breaches. "
            "Rotation intervals are specified in standards and depend on key usage and threat environment. "
            "Automated key management systems can enforce rotation policies. "
            "Rotation must be coordinated to avoid service disruption."
        ),
        key_factors=[
            "Rotation interval",
            "Automation",
            "Coordination",
            "Policy enforcement",
            "Threat assessment"
        ],
        primary_authority=[
            "NIST SP 800-57",
            "ISO/IEC 11770",
            "ENISA Key Management Guidelines"
        ],
        burden_holder="Key custodian, organization",
        adversary_position="Long-lived keys increase exposure to compromise.",
        counter_arguments=[
            "Automated systems simplify rotation.",
            "Policies can be tuned to threat level.",
            "Coordination prevents disruption."
        ],
        resolution_strategy="Enforce regular key rotation and respond promptly to suspected compromise.",
        entity_scope="Key management, enterprise systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-57 Part 1 Section 5.3"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Destruction",
        keywords=["key destruction", "zeroization", "cryptography"],
        conclusion_template="Keys must be securely destroyed (zeroized) when no longer needed to prevent recovery.",
        reasoning_framework=(
            "Secure destruction of cryptographic keys prevents unauthorized recovery after use. "
            "Zeroization involves overwriting key material in memory and storage. "
            "Procedures must be implemented for all key storage locations, including volatile and non-volatile memory. "
            "Automated tools and hardware features can assist in secure destruction."
        ),
        key_factors=[
            "Zeroization procedures",
            "Automation",
            "Coverage of storage locations",
            "Auditability",
            "Standard compliance"
        ],
        primary_authority=[
            "NIST SP 800-88",
            "ISO/IEC 11770",
            "ENISA Key Management Guidelines"
        ],
        burden_holder="Key custodian, implementer",
        adversary_position="Residual key material may be recovered by attackers.",
        counter_arguments=[
            "Automated tools assist in zeroization.",
            "Procedures are well-documented.",
            "Audits verify destruction."
        ],
        resolution_strategy="Implement and audit secure key destruction procedures for all key material.",
        entity_scope="Key management, cryptographic modules",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-88 Section 2"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Distribution Security",
        keywords=["key distribution", "security", "cryptography"],
        conclusion_template="Key distribution mechanisms must ensure confidentiality, integrity, and authenticity of keys in transit.",
        reasoning_framework=(
            "Secure key distribution is essential to prevent interception or tampering. "
            "Mechanisms include secure channels (e.g., TLS), authenticated key exchange protocols, and hardware-based distribution. "
            "Keys must be protected against eavesdropping, modification, and impersonation. "
            "Procedures must be documented and audited."
        ),
        key_factors=[
            "Secure channel usage",
            "Authentication",
            "Integrity protection",
            "Documentation",
            "Auditability"
        ],
        primary_authority=[
            "NIST SP 800-57",
            "ISO/IEC 11770",
            "Handbook of Applied Cryptography"
        ],
        burden_holder="Key custodian, implementer",
        adversary_position="Keys intercepted or modified in transit compromise security.",
        counter_arguments=[
            "Secure channels and protocols provide protection.",
            "Audits detect weaknesses.",
            "Procedures are well-documented."
        ],
        resolution_strategy="Use secure, authenticated channels for all key distribution and audit procedures.",
        entity_scope="Key management, enterprise systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-57 Part 1 Section 5.4"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Archival",
        keywords=["key archival", "long-term storage", "cryptography"],
        conclusion_template="Keys required for long-term access (e.g., for digital signatures) must be archived securely with controlled access.",
        reasoning_framework=(
            "Some keys must be retained for long periods to enable access to archived data or to verify digital signatures. "
            "Archival procedures must ensure confidentiality, integrity, and availability. "
            "Access controls, encryption, and audit trails are essential. "
            "Archival policies must comply with legal and regulatory requirements."
        ),
        key_factors=[
            "Access controls",
            "Encryption",
            "Auditability",
            "Policy compliance",
            "Availability"
        ],
        primary_authority=[
            "NIST SP 800-57",
            "ISO/IEC 11770",
            "ENISA Key Management Guidelines"
        ],
        burden_holder="Key custodian, organization",
        adversary_position="Improper archival may result in key loss or unauthorized access.",
        counter_arguments=[
            "Access controls and encryption protect archived keys.",
            "Audit trails detect unauthorized access.",
            "Policies ensure compliance."
        ],
        resolution_strategy="Implement secure archival procedures with strong access controls and regular audits.",
        entity_scope="Key management, enterprise systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-57 Part 1 Section 5.6"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Usage Monitoring",
        keywords=["key usage", "monitoring", "cryptography"],
        conclusion_template="Key usage must be monitored and logged to detect unauthorized or anomalous activities.",
        reasoning_framework=(
            "Monitoring key usage provides early detection of unauthorized access or misuse. "
            "Logs must capture key operations, access attempts, and anomalies. "
            "Automated analysis and alerting enhance detection. "
            "Logs must be protected against tampering and regularly reviewed."
        ),
        key_factors=[
            "Logging coverage",
            "Automated analysis",
            "Alerting",
            "Log protection",
            "Review procedures"
        ],
        primary_authority=[
            "NIST SP 800-53",
            "ISO/IEC 27001",
            "ENISA Key Management Guidelines"
        ],
        burden_holder="Key custodian, security team",
        adversary_position="Lack of monitoring allows undetected misuse or compromise.",
        counter_arguments=[
            "Automated tools enhance detection.",
            "Logs are protected and reviewed.",
            "Procedures are well-documented."
        ],
        resolution_strategy="Implement comprehensive key usage monitoring and regular log review.",
        entity_scope="Key management, enterprise systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-53 Section AU-2"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Compromise Response",
        keywords=["key compromise", "response", "cryptography"],
        conclusion_template="Procedures must be in place to respond promptly to key compromise, including revocation, replacement, and notification.",
        reasoning_framework=(
            "Key compromise can lead to unauthorized access and data breaches. "
            "Response procedures include revoking affected keys, replacing them, and notifying stakeholders. "
            "Incident response plans must be documented, tested, and regularly updated. "
            "Timely response limits the impact of compromise."
        ),
        key_factors=[
            "Incident response planning",
            "Revocation procedures",
            "Replacement mechanisms",
            "Notification processes",
            "Testing and documentation"
        ],
        primary_authority=[
            "NIST SP 800-61",
            "NIST SP 800-57",
            "ISO/IEC 27035"
        ],
        burden_holder="Key custodian, organization",
        adversary_position="Delayed or inadequate response increases damage from key compromise.",
        counter_arguments=[
            "Incident response plans are standard practice.",
            "Testing ensures effectiveness.",
            "Notification limits further impact."
        ],
        resolution_strategy="Develop, document, and test key compromise response procedures.",
        entity_scope="Key management, enterprise systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-61 Section 3"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Ownership and Accountability",
        keywords=["key ownership", "accountability", "cryptography"],
        conclusion_template="Key ownership must be clearly assigned and accountability enforced for all cryptographic keys.",
        reasoning_framework=(
            "Clear assignment of key ownership ensures responsibility for key management tasks. "
            "Accountability is enforced through access controls, logging, and regular reviews. "
            "Policies must specify ownership, transfer, and delegation procedures. "
            "Lack of accountability increases risk of misuse or loss."
        ),
        key_factors=[
            "Ownership assignment",
            "Access controls",
            "Logging and review",
            "Policy documentation",
            "Delegation procedures"
        ],
        primary_authority=[
            "NIST SP 800-57",
            "ISO/IEC 27001",
            "ENISA Key Management Guidelines"
        ],
        burden_holder="Organization, key custodian",
        adversary_position="Unclear ownership leads to unmanaged or misused keys.",
        counter_arguments=[
            "Policies clarify ownership.",
            "Access controls and logging enforce accountability.",
            "Regular reviews detect issues."
        ],
        resolution_strategy="Assign key ownership and enforce accountability through policy and controls.",
        entity_scope="Key management, enterprise systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NIST SP 800-57 Part 1 Section 5.2"
    ),
    DoctrineBlock(
        topic="Cryptographic Key Usage Documentation",
        keywords=["key usage", "documentation", "cryptography"],
        conclusion_template="All key usages must be documented, including purpose, authorized users, and operational constraints.",
        reasoning_framework=(
            "Documentation of key usage supports compliance, auditing, and incident response. "
            "Records must include key purpose, authorized users, operational constraints, and lifecycle events. "
            "Documentation must be maintained and reviewed regularly."
        ),
        key_factors=[
            "Purpose documentation",
            "User authorization records",
            "Operational constraints",
            "Lifecycle event logging",
            "Review procedures"
        ],
        primary_authority=[
            "NIST SP 800-57",
            "ISO/IEC 27001",
            "ENISA Key Management Guidelines"
        ],
        burden_holder="Key custodian, organization",
        adversary_position="Lack of documentation impedes compliance and incident response.",
        counter_arguments=[
            "Documentation supports compliance.",
            "Regular reviews ensure accuracy.",
            "Automation can assist in recordkeeping."
        ],
        resolution_strategy="Document all key usages and maintain records for compliance and auditing.",
        entity_scope="Key management, enterprise systems",