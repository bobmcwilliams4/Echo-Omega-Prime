"""
LG01 Contract Analysis Engine - Semantic Normalization Dictionary
Version: 1.0.0
Authority: 11.0 SOVEREIGN

GOVERNANCE PROTOCOL:
- This dictionary is IMMUTABLE at runtime
- No auto-learning or runtime modifications permitted
- All changes require explicit version bump and audit trail
- Frozen at module load time via FrozenDict enforcement

PURPOSE:
Normalize contract law terminology, legal jargon, abbreviations, and variant phrasings
into canonical forms for consistent semantic search and analysis.

ARCHITECTURE:
- 150+ normalization entries organized by contract law domain categories
- Word-boundary regex patterns for surgical text replacement
- Longest-match-first ordering via _SORTED_KEYS tuple
- Governance metadata tracking version, lock status, and integrity

CATEGORIES:
1. Contract Type Abbreviations (NDA, MSA, SLA, SOW, LOI, MOU, etc.)
2. Legal Term Variants (breach, parol evidence, force majeure, etc.)
3. UCC Terminology (Article 2, merchantability, perfect tender, etc.)
4. Remedies Variants (consequential damages, specific performance, etc.)
5. Party Role Variants (promisor, promisee, assignor, assignee, etc.)
6. Clause Type Variants (indemnity, limitation of liability, etc.)
7. Common Abbreviations (k, agt, amend, para, sec, etc.)
8. Industry Jargon (boilerplate, four corners, meeting of minds, etc.)
9. Restatement References (Restatement 2d Contracts, etc.)
10. Contract Formation Terms (offer, acceptance, consideration, etc.)
11. Performance Terms (substantial performance, material breach, etc.)
12. Defenses & Excuses (mistake, duress, undue influence, etc.)
13. Third Party Rights (assignment, delegation, third party beneficiary, etc.)
14. Discharge & Termination (rescission, novation, accord and satisfaction, etc.)
15. Interpretation Rules (contra proferentem, ejusdem generis, etc.)
"""

import re
from typing import Dict, Tuple, FrozenSet, Optional
from dataclasses import dataclass, field
from loguru import logger
import hashlib
import json


# ============================================================================
# SEMANTIC NORMALIZATION MAP - IMMUTABLE GOVERNANCE
# ============================================================================

SEMANTIC_MAP_VERSION = "1.0.0"

SEMANTIC_MAP: Dict[str, str] = {
    # ========================================================================
    # CATEGORY 1: CONTRACT TYPE ABBREVIATIONS (20 entries)
    # ========================================================================
    r"\bNDA\b": "non-disclosure agreement",
    r"\bMSA\b": "master service agreement",
    r"\bSLA\b": "service level agreement",
    r"\bSOW\b": "statement of work",
    r"\bLOI\b": "letter of intent",
    r"\bMOU\b": "memorandum of understanding",
    r"\bMOA\b": "memorandum of agreement",
    r"\bIP\b": "intellectual property",
    r"\bJV\b": "joint venture",
    r"\bLLC\b": "limited liability company",
    r"\bAPA\b": "asset purchase agreement",
    r"\bSPA\b": "stock purchase agreement",
    r"\bPSA\b": "purchase and sale agreement",
    r"\bESA\b": "employment separation agreement",
    r"\bCDA\b": "confidential disclosure agreement",
    r"\bMTA\b": "material transfer agreement",
    r"\bTSA\b": "transition services agreement",
    r"\bJDA\b": "joint development agreement",
    r"\bOEM\b": "original equipment manufacturer agreement",
    r"\bVAR\b": "value added reseller agreement",

    # ========================================================================
    # CATEGORY 2: LEGAL TERM VARIANTS (30 entries)
    # ========================================================================
    r"\bbreach of contract\b": "contract breach",
    r"\bcontractual breach\b": "contract breach",
    r"\bbreached the agreement\b": "contract breach",
    r"\bstatute of frauds\b": "statute of frauds",
    r"\bfrauds statute\b": "statute of frauds",
    r"\bparol evidence\b": "parol evidence rule",
    r"\bparol evidence rule\b": "parol evidence rule",
    r"\bextrinsic evidence\b": "parol evidence rule",
    r"\bforce maj\b": "force majeure",
    r"\bforce majeure\b": "force majeure",
    r"\bact of god\b": "force majeure",
    r"\bliq damages\b": "liquidated damages",
    r"\bliquidated damages\b": "liquidated damages",
    r"\bpre-liquidated damages\b": "liquidated damages",
    r"\bspec perf\b": "specific performance",
    r"\bspecific performance\b": "equitable specific performance",
    r"\bequitable relief\b": "equitable remedy",
    r"\bnon-compete\b": "non-competition agreement",
    r"\bnon compete\b": "non-competition agreement",
    r"\brestrictive covenant\b": "non-competition agreement",
    r"\bnon-disclosure\b": "non-disclosure agreement",
    r"\bnon disclosure\b": "non-disclosure agreement",
    r"\bconfidentiality agreement\b": "non-disclosure agreement",
    r"\bgood faith\b": "good faith and fair dealing",
    r"\bfair dealing\b": "good faith and fair dealing",
    r"\bgood faith and fair dealing\b": "implied covenant of good faith and fair dealing",
    r"\bunconsc\b": "unconscionability",
    r"\bunconscionable\b": "unconscionability",
    r"\bconscionability\b": "unconscionability",
    r"\badhesion contract\b": "contract of adhesion",

    # ========================================================================
    # CATEGORY 3: UCC TERMINOLOGY (25 entries)
    # ========================================================================
    r"\bucc\b": "uniform commercial code",
    r"\buniform commercial code\b": "uniform commercial code",
    r"\barticle 2\b": "ucc article 2",
    r"\bucc 2\b": "ucc article 2",
    r"\bucc article 2\b": "ucc article 2 sales",
    r"\barticle 2A\b": "ucc article 2A leases",
    r"\bucc 2A\b": "ucc article 2A leases",
    r"\bbattle of the forms\b": "ucc 2-207 battle of forms",
    r"\bucc 2-207\b": "ucc 2-207 battle of forms",
    r"\bperfect tender\b": "ucc perfect tender rule",
    r"\bperfect tender rule\b": "ucc perfect tender rule",
    r"\bmerchantability\b": "implied warranty of merchantability",
    r"\bimplied warranty\b": "implied warranty of merchantability",
    r"\bfitness for purpose\b": "implied warranty of fitness for particular purpose",
    r"\bfitness warranty\b": "implied warranty of fitness for particular purpose",
    r"\bexpress warranty\b": "express warranty ucc 2-313",
    r"\bwarranty of title\b": "warranty of title ucc 2-312",
    r"\bcure\b": "right to cure ucc 2-508",
    r"\bright to cure\b": "right to cure ucc 2-508",
    r"\bcover\b": "buyer right to cover ucc 2-712",
    r"\bbuyer cover\b": "buyer right to cover ucc 2-712",
    r"\bincidental damages\b": "incidental damages ucc 2-715",
    r"\bconsequential damages\b": "consequential damages ucc 2-715",
    r"\bfirm offer\b": "firm offer ucc 2-205",
    r"\bmerchant firm offer\b": "firm offer ucc 2-205",

    # ========================================================================
    # CATEGORY 4: REMEDIES VARIANTS (20 entries)
    # ========================================================================
    r"\bconsequential damages\b": "consequential damages",
    r"\bindirect damages\b": "consequential damages",
    r"\bspecial damages\b": "consequential damages",
    r"\bpunitive damages\b": "punitive damages",
    r"\bexemplary damages\b": "punitive damages",
    r"\bnominal damages\b": "nominal damages",
    r"\bcompensatory damages\b": "compensatory damages",
    r"\bactual damages\b": "compensatory damages",
    r"\bgeneral damages\b": "general damages",
    r"\bexpectation damages\b": "expectation damages",
    r"\bbenefit of bargain\b": "expectation damages",
    r"\breliance damages\b": "reliance damages",
    r"\bpromissory estoppel damages\b": "reliance damages",
    r"\brestitution\b": "restitutionary remedy",
    r"\bunjust enrichment\b": "restitutionary remedy",
    r"\bquantum meruit\b": "restitutionary remedy quantum meruit",
    r"\binjunctive relief\b": "injunctive relief",
    r"\bpreliminary injunction\b": "preliminary injunctive relief",
    r"\bpermanent injunction\b": "permanent injunctive relief",
    r"\bTRO\b": "temporary restraining order",

    # ========================================================================
    # CATEGORY 5: PARTY ROLE VARIANTS (18 entries)
    # ========================================================================
    r"\bpromisor\b": "obligor",
    r"\bpromisee\b": "obligee",
    r"\bofferor\b": "offering party",
    r"\bofferee\b": "receiving party offer",
    r"\bassignor\b": "assigning party",
    r"\bassignee\b": "receiving party assignment",
    r"\bdelegator\b": "delegating party",
    r"\bdelegatee\b": "receiving party delegation",
    r"\bthird party beneficiary\b": "third party beneficiary",
    r"\bintended beneficiary\b": "intended third party beneficiary",
    r"\bincidental beneficiary\b": "incidental third party beneficiary",
    r"\bcreditor beneficiary\b": "creditor beneficiary",
    r"\bdonee beneficiary\b": "donee beneficiary",
    r"\bobligor\b": "obligor",
    r"\bobligee\b": "obligee",
    r"\bmerchant\b": "merchant ucc 2-104",
    r"\bconsumer\b": "consumer party",
    r"\badhering party\b": "adhering party contract of adhesion",

    # ========================================================================
    # CATEGORY 6: CLAUSE TYPE VARIANTS (22 entries)
    # ========================================================================
    r"\bindemnity clause\b": "indemnification clause",
    r"\bindemnification clause\b": "indemnification clause",
    r"\bhold harmless\b": "indemnification clause",
    r"\bhold harmless clause\b": "indemnification clause",
    r"\blimitation of liability\b": "liability limitation clause",
    r"\bliability cap\b": "liability limitation clause",
    r"\bcap on damages\b": "damages cap",
    r"\bdamages cap\b": "damages cap",
    r"\bexculpatory clause\b": "exculpatory clause",
    r"\bwaiver of liability\b": "exculpatory clause",
    r"\bliquidated damages clause\b": "liquidated damages clause",
    r"\bpenalty clause\b": "penalty clause",
    r"\barbitration clause\b": "arbitration clause",
    r"\balternative dispute resolution\b": "alternative dispute resolution clause",
    r"\bADR clause\b": "alternative dispute resolution clause",
    r"\bchoice of law\b": "choice of law clause",
    r"\bgoverning law\b": "choice of law clause",
    r"\bforum selection\b": "forum selection clause",
    r"\bjurisdiction clause\b": "forum selection clause",
    r"\bintegration clause\b": "integration clause",
    r"\bmerger clause\b": "integration clause",
    r"\bentire agreement\b": "integration clause",

    # ========================================================================
    # CATEGORY 7: COMMON ABBREVIATIONS (18 entries)
    # ========================================================================
    r"\b k\b": "contract",
    r"\bK\b": "contract",
    r"\bagt\b": "agreement",
    r"\bamend\b": "amendment",
    r"\bpara\b": "paragraph",
    r"\bsec\b": "section",
    r"\bart\b": "article",
    r"\bcl\b": "clause",
    r"\bex\b": "exhibit",
    r"\bapp\b": "appendix",
    r"\bsched\b": "schedule",
    r"\brep\b": "representation",
    r"\bwarr\b": "warranty",
    r"\bcov\b": "covenant",
    r"\bcond\b": "condition",
    r"\bterm\b": "termination",
    r"\beff date\b": "effective date",
    r"\bexec date\b": "execution date",

    # ========================================================================
    # CATEGORY 8: INDUSTRY JARGON (16 entries)
    # ========================================================================
    r"\bboilerplate\b": "standard contract provisions",
    r"\bfour corners\b": "four corners doctrine",
    r"\bfour corners doctrine\b": "four corners rule",
    r"\bmeeting of the minds\b": "mutual assent",
    r"\bmeeting of minds\b": "mutual assent",
    r"\bmutual assent\b": "mutual assent",
    r"\bmutuality of obligation\b": "mutuality of obligation",
    r"\bmirror image\b": "mirror image rule",
    r"\bmirror image rule\b": "common law mirror image rule",
    r"\blast shot\b": "last shot rule",
    r"\blast shot rule\b": "last shot rule ucc",
    r"\bknockout rule\b": "knockout rule ucc 2-207",
    r"\bmailbox rule\b": "mailbox rule acceptance",
    r"\bposted acceptance\b": "mailbox rule acceptance",
    r"\boption contract\b": "option contract",
    r"\boption to purchase\b": "option contract",

    # ========================================================================
    # CATEGORY 9: RESTATEMENT REFERENCES (12 entries)
    # ========================================================================
    r"\brestatement\b": "restatement second of contracts",
    r"\brestatement 2d\b": "restatement second of contracts",
    r"\bRst 2d\b": "restatement second of contracts",
    r"\bR2d Contracts\b": "restatement second of contracts",
    r"\brestatement second\b": "restatement second of contracts",
    r"\brestatement first\b": "restatement first of contracts",
    r"\brestatement third\b": "restatement third",
    r"\bRst\b": "restatement",
    r"\brestatement section 90\b": "restatement second section 90 promissory estoppel",
    r"\bsection 90\b": "restatement second section 90 promissory estoppel",
    r"\brestatement 71\b": "restatement second section 71 consideration",
    r"\brestatement 175\b": "restatement second section 175 duress",

    # ========================================================================
    # CATEGORY 10: CONTRACT FORMATION TERMS (20 entries)
    # ========================================================================
    r"\boffer\b": "offer",
    r"\boffering\b": "offer",
    r"\bacceptance\b": "acceptance",
    r"\baccept\b": "acceptance",
    r"\bconsideration\b": "consideration",
    r"\bbargained for exchange\b": "consideration bargained for exchange",
    r"\blegal detriment\b": "consideration legal detriment",
    r"\bpast consideration\b": "past consideration",
    r"\bpre-existing duty\b": "pre-existing duty rule",
    r"\bpreexisting duty\b": "pre-existing duty rule",
    r"\bmoral obligation\b": "moral obligation",
    r"\bcapacity\b": "contractual capacity",
    r"\bmental capacity\b": "mental capacity to contract",
    r"\binfancy\b": "infancy defense",
    r"\bminor\b": "minor contractual capacity",
    r"\bvoidable\b": "voidable contract",
    r"\bvoid\b": "void contract",
    r"\bunenforceable\b": "unenforceable contract",
    r"\billegal contract\b": "illegal contract void",
    r"\bpublic policy\b": "public policy defense",

    # ========================================================================
    # CATEGORY 11: PERFORMANCE TERMS (18 entries)
    # ========================================================================
    r"\bsubstantial performance\b": "substantial performance doctrine",
    r"\bperfect performance\b": "perfect performance",
    r"\bmaterial breach\b": "material breach",
    r"\bminor breach\b": "minor breach",
    r"\bpartial breach\b": "partial breach",
    r"\btotal breach\b": "total breach",
    r"\banticipatory breach\b": "anticipatory repudiation",
    r"\banticipatory repudiation\b": "anticipatory repudiation",
    r"\brepudiation\b": "repudiation",
    r"\bcondition precedent\b": "condition precedent",
    r"\bcondition subsequent\b": "condition subsequent",
    r"\bconcurrent condition\b": "concurrent condition",
    r"\bexpress condition\b": "express condition",
    r"\bimplied condition\b": "implied condition",
    r"\bconstructive condition\b": "constructive condition",
    r"\bdivisible contract\b": "divisible contract",
    r"\bseverable contract\b": "divisible contract",
    r"\binstallment contract\b": "installment contract",

    # ========================================================================
    # CATEGORY 12: DEFENSES & EXCUSES (20 entries)
    # ========================================================================
    r"\bmistake\b": "mistake defense",
    r"\bmutual mistake\b": "mutual mistake",
    r"\bunilateral mistake\b": "unilateral mistake",
    r"\bduress\b": "duress defense",
    r"\beconomic duress\b": "economic duress",
    r"\bundue influence\b": "undue influence defense",
    r"\bmisrepresentation\b": "misrepresentation defense",
    r"\bfraudulent misrepresentation\b": "fraudulent misrepresentation",
    r"\binnocent misrepresentation\b": "innocent misrepresentation",
    r"\bnegligent misrepresentation\b": "negligent misrepresentation",
    r"\bfraud\b": "fraud defense",
    r"\bfraud in the inducement\b": "fraud in the inducement",
    r"\bfraud in the execution\b": "fraud in the execution",
    r"\bimpossibility\b": "impossibility of performance",
    r"\bimpracticability\b": "impracticability defense",
    r"\bcommercial impracticability\b": "commercial impracticability ucc 2-615",
    r"\bfrustration of purpose\b": "frustration of purpose doctrine",
    r"\bfailure of consideration\b": "failure of consideration",
    r"\billegal\b": "illegality defense",
    r"\billegality\b": "illegality defense",

    # ========================================================================
    # CATEGORY 13: THIRD PARTY RIGHTS (15 entries)
    # ========================================================================
    r"\bassignment\b": "assignment of rights",
    r"\bassignment of rights\b": "assignment of rights",
    r"\bdelegation\b": "delegation of duties",
    r"\bdelegation of duties\b": "delegation of duties",
    r"\bthird party beneficiary\b": "third party beneficiary rights",
    r"\b3rd party beneficiary\b": "third party beneficiary rights",
    r"\bintended beneficiary\b": "intended third party beneficiary",
    r"\bincidental beneficiary\b": "incidental third party beneficiary",
    r"\bcreditor beneficiary\b": "creditor beneficiary",
    r"\bdonee beneficiary\b": "donee beneficiary",
    r"\bprivity\b": "privity of contract",
    r"\bprivity of contract\b": "privity of contract",
    r"\banti-assignment clause\b": "anti-assignment clause",
    r"\bnon-assignable\b": "non-assignable rights",
    r"\bpersonal service\b": "personal service contract non-delegable",

    # ========================================================================
    # CATEGORY 14: DISCHARGE & TERMINATION (16 entries)
    # ========================================================================
    r"\brescission\b": "rescission",
    r"\bmutual rescission\b": "mutual rescission",
    r"\bunilateral rescission\b": "unilateral rescission",
    r"\bnovation\b": "novation",
    r"\baccord and satisfaction\b": "accord and satisfaction",
    r"\baccord\b": "accord",
    r"\bsatisfaction\b": "satisfaction",
    r"\brelease\b": "release of obligation",
    r"\bwaiver\b": "waiver of rights",
    r"\bmodification\b": "contract modification",
    r"\bsuperseding agreement\b": "superseding agreement",
    r"\btermination for convenience\b": "termination for convenience",
    r"\btermination for cause\b": "termination for cause",
    r"\bsubstituted contract\b": "substituted contract",
    r"\bexecutory accord\b": "executory accord",
    r"\bdischarge\b": "discharge of obligation",

    # ========================================================================
    # CATEGORY 15: INTERPRETATION RULES (14 entries)
    # ========================================================================
    r"\bcontra proferentem\b": "contra proferentem rule",
    r"\bagainst the drafter\b": "contra proferentem rule",
    r"\bejusdem generis\b": "ejusdem generis rule",
    r"\bexpressio unius\b": "expressio unius est exclusio alterius",
    r"\bnoscitur a sociis\b": "noscitur a sociis",
    r"\bplain meaning\b": "plain meaning rule",
    r"\bplain language\b": "plain meaning rule",
    r"\bcanon of construction\b": "canon of construction",
    r"\brule of construction\b": "rule of construction",
    r"\bcustom and usage\b": "custom and usage",
    r"\bcourse of dealing\b": "course of dealing",
    r"\bcourse of performance\b": "course of performance",
    r"\btrade usage\b": "trade usage",
    r"\bcommercial reasonableness\b": "commercial reasonableness",
}


# ============================================================================
# GOVERNANCE ENFORCEMENT - FROZEN DICT
# ============================================================================

class FrozenDict(dict):
    """Immutable dictionary that raises errors on mutation attempts."""

    def __setitem__(self, key, value):
        raise RuntimeError(
            f"GOVERNANCE VIOLATION: Semantic map is IMMUTABLE. "
            f"Attempted to set '{key}' = '{value}'. "
            f"Version: {SEMANTIC_MAP_VERSION}"
        )

    def __delitem__(self, key):
        raise RuntimeError(
            f"GOVERNANCE VIOLATION: Semantic map is IMMUTABLE. "
            f"Attempted to delete '{key}'. "
            f"Version: {SEMANTIC_MAP_VERSION}"
        )

    def pop(self, *args, **kwargs):
        raise RuntimeError("GOVERNANCE VIOLATION: pop() not allowed on immutable semantic map")

    def popitem(self):
        raise RuntimeError("GOVERNANCE VIOLATION: popitem() not allowed on immutable semantic map")

    def clear(self):
        raise RuntimeError("GOVERNANCE VIOLATION: clear() not allowed on immutable semantic map")

    def update(self, *args, **kwargs):
        raise RuntimeError("GOVERNANCE VIOLATION: update() not allowed on immutable semantic map")

    def setdefault(self, *args, **kwargs):
        raise RuntimeError("GOVERNANCE VIOLATION: setdefault() not allowed on immutable semantic map")


# ============================================================================
# SORTED KEYS - LONGEST MATCH FIRST
# ============================================================================

_SORTED_KEYS: Tuple[str, ...] = tuple(
    sorted(SEMANTIC_MAP.keys(), key=len, reverse=True)
)


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass(frozen=True)
class NormalizationResult:
    """Frozen result from semantic normalization operation."""
    original_query: str
    normalized_query: str
    transformations_applied: Tuple[Tuple[str, str], ...] = field(default_factory=tuple)
    version: str = SEMANTIC_MAP_VERSION

    def __post_init__(self):
        """Ensure transformations is a tuple."""
        if not isinstance(self.transformations_applied, tuple):
            object.__setattr__(
                self,
                'transformations_applied',
                tuple(self.transformations_applied)
            )


# ============================================================================
# NORMALIZATION FUNCTION
# ============================================================================

def normalize_query(query: str) -> NormalizationResult:
    """
    Apply semantic normalization to a contract law query.

    Replaces abbreviations, jargon, and variant phrasings with canonical forms
    using word-boundary regex patterns. Longest patterns matched first.

    Args:
        query: Raw user query string

    Returns:
        NormalizationResult with original, normalized, and transformations log

    Example:
        >>> result = normalize_query("Does the NDA have a non-compete clause?")
        >>> result.normalized_query
        'Does the non-disclosure agreement have a non-competition agreement clause?'
    """
    if not query or not isinstance(query, str):
        logger.warning(f"Invalid query type: {type(query)}")
        return NormalizationResult(
            original_query=str(query),
            normalized_query=str(query),
            transformations_applied=()
        )

    normalized = query
    transformations = []

    # Apply patterns longest-first for surgical precision
    for pattern in _SORTED_KEYS:
        replacement = SEMANTIC_MAP[pattern]
        new_normalized = re.sub(
            pattern,
            replacement,
            normalized,
            flags=re.IGNORECASE
        )

        if new_normalized != normalized:
            transformations.append((pattern, replacement))
            normalized = new_normalized

    logger.debug(
        f"Normalized query: {len(transformations)} transformations applied",
        extra={
            "original": query,
            "normalized": normalized,
            "transformation_count": len(transformations)
        }
    )

    return NormalizationResult(
        original_query=query,
        normalized_query=normalized,
        transformations_applied=tuple(transformations)
    )


# ============================================================================
# SEMANTIC MAP ACCESSOR - SINGLETON
# ============================================================================

class SemanticMapAccessor:
    """
    Singleton accessor providing read-only access to semantic map with governance.

    Enforces:
    - Immutability via FrozenDict
    - Version tracking
    - Integrity verification
    - Audit trail for access patterns
    """

    _instance = None
    _frozen_map: Optional[FrozenDict] = None
    _governance_locked: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize frozen map and lock governance."""
        if not self._governance_locked:
            self._frozen_map = FrozenDict(SEMANTIC_MAP)
            self._governance_locked = True
            logger.info(
                f"Semantic map initialized: {len(SEMANTIC_MAP)} entries, "
                f"version {SEMANTIC_MAP_VERSION}, governance LOCKED"
            )

    def get_semantic_map(self) -> FrozenDict:
        """Return frozen (immutable) semantic map."""
        return self._frozen_map

    def get_sorted_keys(self) -> Tuple[str, ...]:
        """Return sorted keys tuple (longest first)."""
        return _SORTED_KEYS

    def get_governance_metadata(self) -> Dict[str, any]:
        """Return governance metadata."""
        return {
            "version": SEMANTIC_MAP_VERSION,
            "entry_count": len(SEMANTIC_MAP),
            "governance_locked": self._governance_locked,
            "immutable": True,
            "auto_learning": False,
            "integrity_hash": self._compute_integrity_hash()
        }

    def _compute_integrity_hash(self) -> str:
        """Compute SHA-256 hash of semantic map for integrity verification."""
        map_json = json.dumps(SEMANTIC_MAP, sort_keys=True)
        return hashlib.sha256(map_json.encode()).hexdigest()


# ============================================================================
# MODULE-LEVEL ACCESSORS
# ============================================================================

_accessor = SemanticMapAccessor()

def get_semantic_map() -> FrozenDict:
    """Get frozen semantic map."""
    return _accessor.get_semantic_map()

def get_sorted_keys() -> Tuple[str, ...]:
    """Get sorted keys tuple."""
    return _accessor.get_sorted_keys()

def get_governance_metadata() -> Dict[str, any]:
    """Get governance metadata."""
    return _accessor.get_governance_metadata()


# ============================================================================
# INTEGRITY VERIFICATION
# ============================================================================

def verify_dictionary_integrity() -> bool:
    """
    Verify semantic dictionary integrity.

    Checks:
    - All patterns compile as valid regex
    - No duplicate patterns
    - No empty replacements
    - Governance lock is active
    - Map is frozen

    Returns:
        True if all checks pass, False otherwise
    """
    try:
        # Check governance lock
        if not _accessor._governance_locked:
            logger.error("INTEGRITY FAILURE: Governance not locked")
            return False

        # Check frozen map exists
        if _accessor._frozen_map is None:
            logger.error("INTEGRITY FAILURE: Frozen map not initialized")
            return False

        # Check all patterns compile
        for pattern in SEMANTIC_MAP.keys():
            try:
                re.compile(pattern)
            except re.error as e:
                logger.error(f"INTEGRITY FAILURE: Invalid regex pattern '{pattern}': {e}")
                return False

        # Check for duplicate patterns (case-insensitive)
        pattern_set = set()
        for pattern in SEMANTIC_MAP.keys():
            pattern_lower = pattern.lower()
            if pattern_lower in pattern_set:
                logger.error(f"INTEGRITY FAILURE: Duplicate pattern '{pattern}'")
                return False
            pattern_set.add(pattern_lower)

        # Check for empty replacements
        for pattern, replacement in SEMANTIC_MAP.items():
            if not replacement or not replacement.strip():
                logger.error(f"INTEGRITY FAILURE: Empty replacement for '{pattern}'")
                return False

        # Check frozen dict mutation protection
        try:
            _accessor._frozen_map['test'] = 'value'
            logger.error("INTEGRITY FAILURE: FrozenDict allows mutation")
            return False
        except RuntimeError:
            pass  # Expected behavior

        logger.info(
            f"Semantic dictionary integrity verified: {len(SEMANTIC_MAP)} entries, "
            f"version {SEMANTIC_MAP_VERSION}"
        )
        return True

    except Exception as e:
        logger.error(f"INTEGRITY FAILURE: Unexpected error during verification: {e}")
        return False


# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

# Verify integrity on module load
if not verify_dictionary_integrity():
    raise RuntimeError(
        f"LG01 Semantic Dictionary FAILED integrity check. "
        f"Version: {SEMANTIC_MAP_VERSION}. "
        f"Module cannot be safely imported."
    )

logger.info(
    f"LG01 Semantic Dictionary loaded successfully: "
    f"{len(SEMANTIC_MAP)} entries, version {SEMANTIC_MAP_VERSION}, "
    f"governance LOCKED, integrity VERIFIED"
)
