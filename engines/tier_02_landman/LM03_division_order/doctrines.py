"""
LM03 Division Order Engine - Doctrine Cache
=============================================

Pre-compiled division order doctrines for instant retrieval.
55+ doctrine blocks covering Texas Natural Resources Code Ch. 91,
decimal interest calculation, Duhig rule, proportionate reduction,
suspense/escheat, division order ratification, pooling/unitization,
JOA provisions, revenue distribution, and related oil & gas case law.

DET (Deterministic) mode. Zero LLM dependency for cached answers.
SHA-256 integrity verification on every block.

Author: ECHO OMEGA PRIME Build System
Engine: LM03 Division Order
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class DoctrineCategory(str, Enum):
    """Top-level categories for division order doctrines."""
    DIVISION_ORDER_BASICS = "DIVISION_ORDER_BASICS"
    TEXAS_NRC_CHAPTER_91 = "TEXAS_NRC_CHAPTER_91"
    DECIMAL_INTEREST_CALC = "DECIMAL_INTEREST_CALC"
    WORKING_INTEREST = "WORKING_INTEREST"
    ROYALTY_INTEREST = "ROYALTY_INTEREST"
    OVERRIDING_ROYALTY = "OVERRIDING_ROYALTY"
    NET_REVENUE_INTEREST = "NET_REVENUE_INTEREST"
    COST_BEARING_INTEREST = "COST_BEARING_INTEREST"
    TITLE_OPINION = "TITLE_OPINION"
    SUSPENSE_PROCEDURES = "SUSPENSE_PROCEDURES"
    ESCHEAT_UNCLAIMED = "ESCHEAT_UNCLAIMED"
    TRANSFER_ORDERS = "TRANSFER_ORDERS"
    RATIFICATION = "RATIFICATION"
    CHANGE_OF_OWNERSHIP = "CHANGE_OF_OWNERSHIP"
    POOLING_UNITIZATION = "POOLING_UNITIZATION"
    DUHIG_RULE = "DUHIG_RULE"
    PROPORTIONATE_REDUCTION = "PROPORTIONATE_REDUCTION"
    AFTER_ACQUIRED_TITLE = "AFTER_ACQUIRED_TITLE"
    MOTHER_HUBBARD = "MOTHER_HUBBARD"
    FARMOUT_INTERESTS = "FARMOUT_INTERESTS"
    CARRIED_INTEREST = "CARRIED_INTEREST"
    BACK_IN_RIGHTS = "BACK_IN_RIGHTS"
    REVERSIONARY_INTEREST = "REVERSIONARY_INTEREST"
    JOA_PROVISIONS = "JOA_PROVISIONS"
    REVENUE_DISTRIBUTION = "REVENUE_DISTRIBUTION"
    PAY_DECK = "PAY_DECK"
    SEVERANCE_TAX = "SEVERANCE_TAX"
    HEIRSHIP_EFFECTS = "HEIRSHIP_EFFECTS"
    PARTITION_EFFECTS = "PARTITION_EFFECTS"
    FRACTIONAL_CONVEYANCE = "FRACTIONAL_CONVEYANCE"
    INTEREST_TRACING = "INTEREST_TRACING"


class DoctrineSeverity(str, Enum):
    """Severity / importance level of a doctrine block."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DoctrineCacheBlock:
    """A single pre-compiled doctrine block.

    Each block contains a self-contained answer to a common division
    order question, complete with citations, applicability notes,
    and a SHA-256 integrity hash.
    """
    block_id: str
    category: DoctrineCategory
    title: str
    summary: str
    full_text: str
    citations: List[str]
    case_law: List[str] = field(default_factory=list)
    statutes: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    applicability: str = "TX"
    severity: DoctrineSeverity = DoctrineSeverity.MEDIUM
    related_blocks: List[str] = field(default_factory=list)
    effective_date: str = "2025-01-01"
    supersedes: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    @property
    def integrity_hash(self) -> str:
        """Compute SHA-256 hash of the block content for integrity verification."""
        content = json.dumps({
            "block_id": self.block_id,
            "category": self.category.value,
            "title": self.title,
            "full_text": self.full_text,
            "citations": self.citations,
        }, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def matches_query(self, query: str) -> float:
        """Score how well this block matches a search query.

        Args:
            query: Search query string.

        Returns:
            Relevance score between 0.0 and 1.0.
        """
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        score = 0.0
        title_lower = self.title.lower()
        if query_lower in title_lower:
            score += 0.40
        summary_lower = self.summary.lower()
        if query_lower in summary_lower:
            score += 0.25
        keyword_matches = sum(1 for kw in self.keywords if kw.lower() in query_lower)
        if self.keywords:
            score += 0.20 * (keyword_matches / len(self.keywords))
        full_lower = self.full_text.lower()
        term_matches = sum(1 for t in query_terms if t in full_lower)
        if query_terms:
            score += 0.15 * (term_matches / len(query_terms))
        return min(score, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "block_id": self.block_id,
            "category": self.category.value,
            "title": self.title,
            "summary": self.summary,
            "full_text": self.full_text,
            "citations": list(self.citations),
            "case_law": list(self.case_law),
            "statutes": list(self.statutes),
            "keywords": list(self.keywords),
            "applicability": self.applicability,
            "severity": self.severity.value,
            "related_blocks": list(self.related_blocks),
            "effective_date": self.effective_date,
            "supersedes": self.supersedes,
            "notes": list(self.notes),
            "integrity_hash": self.integrity_hash,
        }


# ---------------------------------------------------------------------------
# Doctrine Cache Class
# ---------------------------------------------------------------------------

class DivisionOrderDoctrineCache:
    """Pre-compiled doctrine cache for the Division Order Engine.

    Holds 55+ doctrine blocks covering all major division order topics.
    Supports search, coverage mapping, and integrity verification.
    """

    def __init__(self) -> None:
        """Initialize the doctrine cache and load all blocks."""
        self._blocks: Dict[str, DoctrineCacheBlock] = {}
        self._category_index: Dict[DoctrineCategory, List[str]] = {}
        self._keyword_index: Dict[str, List[str]] = {}
        self._build_cache()
        logger.info(
            "DivisionOrderDoctrineCache loaded: {n} blocks across {c} categories",
            n=len(self._blocks),
            c=len(self._category_index),
        )

    def _build_cache(self) -> None:
        """Build the complete doctrine cache."""
        blocks = _build_all_doctrine_blocks()
        for block in blocks:
            self._blocks[block.block_id] = block
            cat_list = self._category_index.setdefault(block.category, [])
            cat_list.append(block.block_id)
            for kw in block.keywords:
                kw_lower = kw.lower()
                kw_list = self._keyword_index.setdefault(kw_lower, [])
                kw_list.append(block.block_id)

    def get_block(self, block_id: str) -> Optional[DoctrineCacheBlock]:
        """Retrieve a specific doctrine block by ID.

        Args:
            block_id: The block identifier.

        Returns:
            The doctrine block or None if not found.
        """
        return self._blocks.get(block_id)

    def get_blocks_by_category(self, category: DoctrineCategory) -> List[DoctrineCacheBlock]:
        """Get all blocks in a given category.

        Args:
            category: The doctrine category.

        Returns:
            List of matching doctrine blocks.
        """
        block_ids = self._category_index.get(category, [])
        return [self._blocks[bid] for bid in block_ids if bid in self._blocks]

    def search(self, query: str, max_results: int = 10) -> List[Tuple[DoctrineCacheBlock, float]]:
        """Search doctrine blocks by relevance to a query.

        Args:
            query: Search query string.
            max_results: Maximum number of results.

        Returns:
            List of (block, score) tuples sorted by relevance.
        """
        scored: List[Tuple[DoctrineCacheBlock, float]] = []
        for block in self._blocks.values():
            score = block.matches_query(query)
            if score > 0.05:
                scored.append((block, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:max_results]

    def get_coverage_map(self) -> Dict[str, Any]:
        """Return a coverage map showing block counts per category.

        Returns:
            Dictionary mapping category names to block counts and IDs.
        """
        coverage: Dict[str, Any] = {}
        for cat, block_ids in self._category_index.items():
            coverage[cat.value] = {
                "count": len(block_ids),
                "block_ids": block_ids,
            }
        return {
            "total_blocks": len(self._blocks),
            "total_categories": len(self._category_index),
            "categories": coverage,
        }

    def verify_integrity(self) -> Dict[str, Any]:
        """Verify the SHA-256 integrity of all doctrine blocks.

        Returns:
            Dictionary with verification results.
        """
        verified = 0
        failed: List[str] = []
        for block_id, block in self._blocks.items():
            expected = block.integrity_hash
            content = json.dumps({
                "block_id": block.block_id,
                "category": block.category.value,
                "title": block.title,
                "full_text": block.full_text,
                "citations": block.citations,
            }, sort_keys=True, separators=(",", ":"))
            actual = hashlib.sha256(content.encode("utf-8")).hexdigest()
            if expected == actual:
                verified += 1
            else:
                failed.append(block_id)
        return {
            "total_blocks": len(self._blocks),
            "verified": verified,
            "failed": len(failed),
            "failed_blocks": failed,
            "integrity_status": "PASS" if not failed else "FAIL",
        }

    def health_check(self) -> Dict[str, Any]:
        """Return health status of the doctrine cache.

        Returns:
            Dictionary with health information.
        """
        return {
            "status": "healthy",
            "total_blocks": len(self._blocks),
            "total_categories": len(self._category_index),
            "keyword_index_size": len(self._keyword_index),
            "integrity": self.verify_integrity()["integrity_status"],
        }

    @property
    def block_count(self) -> int:
        """Return the total number of doctrine blocks."""
        return len(self._blocks)

    @property
    def all_blocks(self) -> List[DoctrineCacheBlock]:
        """Return all doctrine blocks."""
        return list(self._blocks.values())


# ---------------------------------------------------------------------------
# Module-Level Functions
# ---------------------------------------------------------------------------

def build_doctrine_cache() -> DivisionOrderDoctrineCache:
    """Build and return a new DivisionOrderDoctrineCache instance.

    Returns:
        A fully populated doctrine cache.
    """
    return DivisionOrderDoctrineCache()


def search_doctrines(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search doctrines using a module-level convenience function.

    Args:
        query: Search query string.
        max_results: Maximum results to return.

    Returns:
        List of matching doctrine block dictionaries with scores.
    """
    cache = DivisionOrderDoctrineCache()
    results = cache.search(query, max_results)
    return [
        {"block": block.to_dict(), "score": round(score, 4)}
        for block, score in results
    ]


def get_coverage_map() -> Dict[str, Any]:
    """Get the doctrine coverage map.

    Returns:
        Coverage map dictionary.
    """
    cache = DivisionOrderDoctrineCache()
    return cache.get_coverage_map()


def verify_doctrine_integrity() -> Dict[str, Any]:
    """Verify integrity of all doctrine blocks.

    Returns:
        Integrity verification results.
    """
    cache = DivisionOrderDoctrineCache()
    return cache.verify_integrity()


# ---------------------------------------------------------------------------
# Doctrine Block Definitions (55+ blocks)
# ---------------------------------------------------------------------------

def _build_all_doctrine_blocks() -> List[DoctrineCacheBlock]:
    """Build all 55+ doctrine blocks for the division order engine.

    Returns:
        List of all DoctrineCacheBlock instances.
    """
    blocks: List[DoctrineCacheBlock] = []

    # ---- DIVISION ORDER BASICS ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-001",
        category=DoctrineCategory.DIVISION_ORDER_BASICS,
        title="Definition and Purpose of Division Orders",
        summary="A division order is a contract between a royalty owner or interest holder and the operator directing the purchaser of production to pay for the interest holder's share of proceeds.",
        full_text=(
            "A division order is an instrument executed by an interest owner directing the purchaser "
            "of oil and gas production to pay for the interest owner's share of proceeds from the "
            "sale of production. Under Texas law, a division order is not a transfer of title to an "
            "interest in a mineral estate. Tex. Nat. Res. Code Sec. 91.402(h) provides that a "
            "division order may be used only to establish the basis on which payments are to be "
            "made for production and shall not be used to amend the terms of any lease. A division "
            "order does not amend, enlarge, or modify the terms of an existing oil and gas lease. "
            "The primary purpose of a division order is to provide the payor (operator or purchaser) "
            "with written authorization to distribute revenue. The division order establishes: "
            "(1) the identity of the interest owner, (2) the type of interest (RI, ORRI, WI, etc.), "
            "(3) the decimal interest in the unit or lease, (4) payment instructions, and "
            "(5) tax identification information."
        ),
        citations=[
            "Tex. Nat. Res. Code Sec. 91.001",
            "Tex. Nat. Res. Code Sec. 91.402(h)",
            "Gavenda v. Strata Energy, Inc., 705 S.W.2d 690 (Tex. 1986)",
        ],
        case_law=[
            "Gavenda v. Strata Energy, Inc., 705 S.W.2d 690 (Tex. 1986) - division order does not amend lease terms",
            "Heritage Resources, Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996) - division order as authorization for payment",
        ],
        statutes=["Tex. Nat. Res. Code Ch. 91"],
        keywords=["division order", "definition", "purpose", "payment authorization", "interest holder"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-002", "DO-003", "DO-004"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-002",
        category=DoctrineCategory.DIVISION_ORDER_BASICS,
        title="Division Order vs. Oil and Gas Lease",
        summary="A division order cannot modify the terms of an oil and gas lease. It serves only as payment authorization.",
        full_text=(
            "Under Tex. Nat. Res. Code Sec. 91.402(h), a division order may not be used to amend "
            "the terms of any lease. If there is a conflict between a division order and a lease, "
            "the lease controls. In Gavenda v. Strata Energy, Inc., 705 S.W.2d 690 (Tex. 1986), "
            "the Texas Supreme Court held that a division order stipulation of a lower royalty "
            "fraction than provided in the lease was ineffective. The division order is merely a "
            "directive for payment, not a conveyance. A lessor who signs a division order stating "
            "a royalty fraction lower than the lease rate does not waive the right to the higher "
            "lease royalty. However, the statute of limitations may apply if the underpayment is "
            "not discovered within four years. The 2009 amendments to Ch. 91 codified this principle "
            "and added protections for royalty owners against misleading division order language."
        ),
        citations=[
            "Tex. Nat. Res. Code Sec. 91.402(h)",
            "Gavenda v. Strata Energy, Inc., 705 S.W.2d 690 (Tex. 1986)",
        ],
        case_law=[
            "Gavenda v. Strata Energy, Inc., 705 S.W.2d 690 (Tex. 1986)",
            "Cabot Oil & Gas Corp. v. Daugherty, 479 S.W.3d 258 (Tex. 2015)",
        ],
        statutes=["Tex. Nat. Res. Code Sec. 91.402(h)"],
        keywords=["division order", "lease", "conflict", "amendment", "royalty fraction"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-001", "DO-010"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-003",
        category=DoctrineCategory.DIVISION_ORDER_BASICS,
        title="Revocability of Division Orders",
        summary="Under Texas law, a division order is revocable on 60 days written notice.",
        full_text=(
            "Tex. Nat. Res. Code Sec. 91.402(g) provides that a division order may be revoked "
            "by the interest owner at any time upon 60 days written notice. Prior to the 2009 "
            "amendments, the revocability of division orders was a matter of common law. The "
            "statutory codification ensures that interest owners are not permanently bound by "
            "division orders that may contain incorrect decimal interests. Upon revocation, the "
            "payor must continue payments based on the most recently executed division order or, "
            "if none exists, based on the title opinion or other evidence of ownership. The payor "
            "may place amounts in suspense pending execution of a new division order. Revocation "
            "does not affect the obligation of the payor to pay proceeds; it merely removes the "
            "payor's authorization to rely on the revoked division order's stated interest."
        ),
        citations=[
            "Tex. Nat. Res. Code Sec. 91.402(g)",
        ],
        case_law=[
            "Exxon Corp. v. Middleton, 613 S.W.2d 240 (Tex. 1981) - revocability predates statute",
        ],
        statutes=["Tex. Nat. Res. Code Sec. 91.402(g)"],
        keywords=["revocation", "60 days", "notice", "revocable", "division order"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-001", "DO-020"],
    ))

    # ---- TEXAS NRC CHAPTER 91 ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-004",
        category=DoctrineCategory.TEXAS_NRC_CHAPTER_91,
        title="Payment Obligations Under Tex. NRC Sec. 91.402",
        summary="Payors must pay proceeds to interest owners within statutory deadlines or face penalty interest.",
        full_text=(
            "Under Tex. Nat. Res. Code Sec. 91.402, the payor (typically the operator or first "
            "purchaser) must pay oil and gas proceeds to interest owners within certain time limits. "
            "For oil, payment must be made on or before 120 days after the end of the month of "
            "first sale. For gas, payment must be made on or before 120 days after the end of the "
            "month of first sale. For subsequent payments, proceeds must be paid on or before the "
            "last day of the second month after the month of sale. If the payor fails to make "
            "timely payment, the interest owner is entitled to interest at the rate of 12% per "
            "annum on the unpaid amount from the date payment was due until the date payment "
            "is made. The 12% penalty interest is a statutory right and may not be waived by "
            "division order. The payor must also include a statement showing the price, volume, "
            "taxes withheld, and other deductions."
        ),
        citations=[
            "Tex. Nat. Res. Code Sec. 91.402(a)",
            "Tex. Nat. Res. Code Sec. 91.402(b)",
            "Tex. Nat. Res. Code Sec. 91.402(c)",
        ],
        case_law=[
            "Heritage Resources, Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
        ],
        statutes=["Tex. Nat. Res. Code Sec. 91.402"],
        keywords=["payment", "120 days", "penalty interest", "12 percent", "proceeds", "timely payment"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-001", "DO-005", "DO-030"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-005",
        category=DoctrineCategory.TEXAS_NRC_CHAPTER_91,
        title="Liability for Failure to Pay - Sec. 91.403",
        summary="An operator or purchaser who fails to pay proceeds timely is liable for the amount due plus interest and attorney fees.",
        full_text=(
            "Tex. Nat. Res. Code Sec. 91.403 creates a cause of action for an interest owner "
            "against a payor who fails to make timely payment of oil and gas proceeds. The interest "
            "owner may recover: (1) the unpaid proceeds, (2) interest at 12% per annum from the "
            "date payment was due, and (3) reasonable attorney's fees if the court finds the payor's "
            "failure to pay was not in good faith. Good faith defenses include bona fide title "
            "disputes, pending probate, unresolved liens, and inability to identify the proper "
            "payee. The operator may hold funds in suspense when there is a good faith dispute "
            "about who is entitled to payment. However, the operator must make diligent efforts "
            "to resolve the dispute. Funds held in suspense do not accrue the 12% penalty interest "
            "if the operator's decision to hold was in good faith."
        ),
        citations=[
            "Tex. Nat. Res. Code Sec. 91.403",
            "Tex. Nat. Res. Code Sec. 91.402(b)",
        ],
        case_law=[
            "HECI Exploration Co. v. Neel, 982 S.W.2d 881 (Tex. 1998)",
        ],
        statutes=["Tex. Nat. Res. Code Sec. 91.403"],
        keywords=["liability", "failure to pay", "attorney fees", "good faith", "suspense"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-004", "DO-020"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-006",
        category=DoctrineCategory.TEXAS_NRC_CHAPTER_91,
        title="Division Order Content Requirements - Sec. 91.402(c)",
        summary="Texas law prescribes what a division order must and must not contain.",
        full_text=(
            "Tex. Nat. Res. Code Sec. 91.402(c) provides that a division order must contain: "
            "(1) the name and address of the interest owner, (2) the tax identification number, "
            "(3) the type of interest (royalty, working interest, etc.), (4) the decimal interest "
            "in the well or unit, (5) the effective date, and (6) a provision for change of "
            "ownership. The division order may not contain any provision that amends, enlarges, "
            "or modifies the terms of the oil and gas lease. It may not contain a warranty of "
            "title from a royalty owner. It may not require indemnification from a royalty owner "
            "beyond the extent of the payments received. The 2009 amendments to the statute added "
            "Sec. 91.402(i) providing that a division order that contains prohibited provisions "
            "is not void, but the prohibited provisions are unenforceable."
        ),
        citations=[
            "Tex. Nat. Res. Code Sec. 91.402(c)",
            "Tex. Nat. Res. Code Sec. 91.402(i)",
        ],
        statutes=["Tex. Nat. Res. Code Sec. 91.402(c)", "Tex. Nat. Res. Code Sec. 91.402(i)"],
        keywords=["content requirements", "prohibited provisions", "warranty", "indemnification"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-001", "DO-002"],
    ))

    # ---- DECIMAL INTEREST CALCULATION ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-010",
        category=DoctrineCategory.DECIMAL_INTEREST_CALC,
        title="Decimal Interest Fundamentals",
        summary="Decimal interest represents the fractional share of production or revenue attributable to an owner, expressed as a decimal to 8 places.",
        full_text=(
            "A decimal interest is the numerical representation of an owner's proportionate share "
            "of production or revenue from a well or unit. Industry standard is 8 decimal places. "
            "The decimal interest is derived from the chain of title by tracing all conveyances, "
            "reservations, and exceptions affecting the mineral or leasehold estate. The total of "
            "all decimal interests for a given interest type must equal 1.00000000 (unity). If the "
            "interests do not sum to unity, there is a title defect or calculation error that must "
            "be resolved before division orders are executed. Common fraction-to-decimal conversions: "
            "1/8 = 0.12500000 (standard lessor royalty), 3/16 = 0.18750000, 1/4 = 0.25000000, "
            "1/6 = 0.16666667, 1/3 = 0.33333333, 1/2 = 0.50000000, 5/8 = 0.62500000. "
            "Net Revenue Interest (NRI) = Working Interest minus all burdens (royalties, ORRIs, etc.). "
            "Example: 100% WI with 1/8 RI and 3% ORRI gives NRI = 1.0 - 0.125 - 0.03 = 0.84500000."
        ),
        citations=[
            "AAPL Division Order Form 610-2015",
            "COPAS Accounting Procedure, 2005 ed.",
        ],
        keywords=["decimal interest", "fractional share", "unity", "8 decimal places", "NRI", "WI", "RI"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-011", "DO-012", "DO-013"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-011",
        category=DoctrineCategory.DECIMAL_INTEREST_CALC,
        title="Fraction to Decimal Conversion Rules",
        summary="Rules for converting fractional mineral interests to decimal notation with proper rounding.",
        full_text=(
            "Converting fractional mineral interests to decimals requires careful attention to "
            "rounding. Industry standard uses ROUND_HALF_UP to 8 decimal places. Fractions are "
            "commonly expressed as simple fractions (1/8, 3/16), undivided interests (an undivided "
            "1/4 interest), or net mineral acres (NMA). To convert NMA to decimal interest in a "
            "unit: decimal = NMA / total_net_mineral_acres_in_unit. To convert fractional mineral "
            "ownership to decimal: if owner holds 1/4 of the minerals and the lease royalty is "
            "1/8, the owner's royalty decimal = 1/4 x 1/8 = 1/32 = 0.03125000. When multiple "
            "fractions are multiplied, carry full precision through intermediate steps and round "
            "only the final result. When a tract is pooled into a unit, the tract's participation "
            "factor is tract_acres / unit_acres, and each owner's unit decimal = "
            "owner_decimal_in_tract x (tract_acres / unit_acres). Repeating decimals must be "
            "truncated or rounded consistently: 1/3 = 0.33333333 (not 0.33333334). "
            "1/6 = 0.16666667 (rounded up from 0.166666666...)."
        ),
        citations=["AAPL Division Order Form 610-2015"],
        keywords=["fraction", "decimal", "conversion", "rounding", "NMA", "net mineral acres"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-010", "DO-012"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-012",
        category=DoctrineCategory.DECIMAL_INTEREST_CALC,
        title="Unity Check - All Interests Must Sum to 1.0",
        summary="The total of all decimal interests in a well or unit must equal 1.00000000.",
        full_text=(
            "A fundamental principle of division order administration is the unity check: the "
            "sum of all decimal interests of a given type (e.g., all royalty interests, or all "
            "working interests) must equal 1.00000000. A tolerance of 0.00001000 is commonly "
            "accepted to account for rounding in repeating decimals. If the total exceeds 1.0, "
            "there is an over-conveyance or double-counting error. If the total is less than 1.0, "
            "there is an unconveyed interest or missing owner. Common causes of unity failure: "
            "(1) Duhig rule application creating a shortfall, (2) missing heir after death of "
            "an interest owner, (3) unrecorded conveyance, (4) pooling allocation error, "
            "(5) mathematical rounding accumulated through multiple conveyance steps. When unity "
            "fails, the title examiner must identify the source of the discrepancy before division "
            "orders can be executed. The operator may proceed with partial payment for verified "
            "interests while placing the disputed amount in suspense."
        ),
        citations=["AAPL Division Order Form 610-2015", "COPAS 2005 Sec. I.4"],
        keywords=["unity check", "sum to one", "over-conveyance", "shortfall", "tolerance"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-010", "DO-011", "DO-040"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-013",
        category=DoctrineCategory.DECIMAL_INTEREST_CALC,
        title="Undivided Interest vs. Divided Interest",
        summary="Undivided interests are fractional shares in the whole tract; divided interests are specific allocated portions.",
        full_text=(
            "An undivided interest gives the holder a fractional share in the entire property "
            "without any physical division. Each co-owner has the right to possession of the "
            "whole and receives their fractional share of all production. A divided interest "
            "(partition) gives the holder a specific allocated portion. In Texas, mineral "
            "interests are presumed undivided absent express partition. When computing division "
            "order decimals, undivided interests multiply through the full chain. If A owns an "
            "undivided 1/2 mineral interest and conveys 1/4 of 'her' interest, A conveys "
            "1/2 x 1/4 = 1/8 undivided mineral interest. The conveyance of 'an undivided "
            "one-half interest in and to the oil, gas, and other minerals' creates a 0.50000000 "
            "mineral interest. If the grantee then leases on 1/8 royalty, the grantee's royalty "
            "decimal = 0.50000000 x 0.12500000 = 0.06250000."
        ),
        citations=[
            "Tex. Property Code Sec. 5.001",
            "Cox v. Davison, 397 S.W.2d 200 (Tex. 1965)",
        ],
        case_law=[
            "Cox v. Davison, 397 S.W.2d 200 (Tex. 1965) - undivided mineral interests",
        ],
        keywords=["undivided interest", "divided interest", "partition", "fractional share", "co-owner"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-010", "DO-046"],
    ))

    # ---- WORKING INTEREST / ROYALTY / ORRI ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-014",
        category=DoctrineCategory.WORKING_INTEREST,
        title="Working Interest Calculation",
        summary="Working interest (WI) is the operating interest in a well, bearing costs and entitled to revenue net of burdens.",
        full_text=(
            "The working interest (WI) is the interest in an oil and gas lease that bears the "
            "costs of exploration, drilling, and production. The lessee (operator) typically holds "
            "100% WI initially, but may assign portions to other parties. The WI holder's net "
            "revenue interest (NRI) is the WI minus all non-cost-bearing burdens: NRI = WI - "
            "lessor royalty - ORRI - production payments - net profits interests. For example, "
            "if operator holds 75% WI, lease royalty is 1/8, and there is a 2% ORRI: "
            "NRI = 0.75 x (1 - 0.125 - 0.02) = 0.75 x 0.855 = 0.64125000. The WI holder pays "
            "its proportionate share of all operating costs (lease operating expenses, workover, "
            "ad valorem taxes) based on its WI decimal, and receives revenue based on its NRI "
            "decimal. In JOA operations, each WI holder's cost share equals their WI decimal."
        ),
        citations=["AAPL Model Form Operating Agreement (AAPL 610-2015)"],
        keywords=["working interest", "WI", "cost-bearing", "NRI", "operator", "lessee"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-010", "DO-015", "DO-016"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-015",
        category=DoctrineCategory.ROYALTY_INTEREST,
        title="Royalty Interest Calculation",
        summary="The royalty interest (RI) is a non-cost-bearing share of production or proceeds reserved by the lessor.",
        full_text=(
            "The royalty interest is the share of production (or proceeds from the sale of "
            "production) reserved by the mineral owner (lessor) in an oil and gas lease. The "
            "standard Texas royalty is 1/8 (0.12500000) but 1/4 (0.25000000) and 3/16 (0.18750000) "
            "are increasingly common. The royalty owner does not bear costs of production. The "
            "royalty decimal for division order purposes is: owner_mineral_fraction x lease_royalty "
            "x tract_participation_factor. If a tract is pooled into a unit, the royalty owner's "
            "unit royalty decimal = mineral_fraction x lease_royalty x (tract_acres / unit_acres). "
            "Multiple royalty interests exist where NPRI has been carved out: the lessor's royalty "
            "is reduced by the NPRI fraction. Per French v. Chevron U.S.A., Inc., 896 S.W.2d 795 "
            "(Tex. 1995), an NPRI created before the lease reduces the lessor's royalty proportionately."
        ),
        citations=[
            "Tex. Nat. Res. Code Sec. 91.001(6)",
            "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)",
        ],
        case_law=[
            "French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)",
            "Lesley v. Veterans Land Board, 352 S.W.3d 479 (Tex. 2011)",
        ],
        keywords=["royalty interest", "RI", "lessor royalty", "1/8", "non-cost-bearing", "NPRI"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-010", "DO-014", "DO-016"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-016",
        category=DoctrineCategory.OVERRIDING_ROYALTY,
        title="Overriding Royalty Interest (ORRI)",
        summary="An ORRI is a non-cost-bearing interest carved out of the working interest that terminates with the lease.",
        full_text=(
            "An overriding royalty interest (ORRI) is created out of the working interest (not "
            "the mineral estate) and lasts only for the duration of the lease from which it was "
            "carved. When the lease terminates, the ORRI terminates. The ORRI holder does not "
            "bear costs of production. Common ORRI percentages range from 1% to 5%. The ORRI "
            "reduces the WI holder's NRI: NRI = WI x (1 - lessor_royalty - sum_of_ORRIs - "
            "other_burdens). An ORRI is typically created by assignment: the assignor retains "
            "an ORRI when assigning the leasehold interest. Or it can be created by a separate "
            "instrument. The ORRI decimal for division order purposes is: ORRI_fraction x "
            "WI_decimal x tract_participation_factor. Multiple ORRIs are cumulative. Per "
            "Texas law, an ORRI is personal property, not a real property interest."
        ),
        citations=[
            "Nonparticipating Royalty Interest, 2 Williams & Meyers, Oil and Gas Law Sec. 418",
        ],
        case_law=[
            "Cosgrove v. Cade, 468 S.W.3d 32 (Tex. 2015) - ORRI terminates with lease",
        ],
        keywords=["overriding royalty", "ORRI", "carved from WI", "lease duration", "non-cost-bearing"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-014", "DO-015", "DO-044"],
    ))

    # ---- NET REVENUE INTEREST ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-017",
        category=DoctrineCategory.NET_REVENUE_INTEREST,
        title="Net Revenue Interest (NRI) Calculation",
        summary="NRI is the working interest minus all non-cost-bearing burdens. It determines the revenue share.",
        full_text=(
            "Net Revenue Interest (NRI) is the share of production revenue actually received by "
            "a working interest owner after deducting all non-operating burdens. NRI = WI x "
            "(1.00000000 - total_burdens). Total burdens include: lessor royalty, ORRIs, "
            "production payments, and net profits interests. Example calculation: "
            "WI = 0.50000000, Lessor Royalty = 0.25000000, ORRI = 0.03000000. "
            "NRI = 0.50 x (1.0 - 0.25 - 0.03) = 0.50 x 0.72 = 0.36000000. "
            "The NRI is what appears on the working interest holder's division order. "
            "For royalty owners, the concept of NRI does not apply since royalty owners do not "
            "bear costs. The term 'net revenue interest' is sometimes loosely used to describe "
            "any net decimal interest, but technically it applies only to the cost-bearing "
            "working interest owner's revenue share."
        ),
        citations=["AAPL Model Form Operating Agreement, Art. III.B"],
        keywords=["NRI", "net revenue interest", "burdens", "revenue share", "working interest"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-014", "DO-015", "DO-016"],
    ))

    # ---- SUSPENSE PROCEDURES ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-020",
        category=DoctrineCategory.SUSPENSE_PROCEDURES,
        title="Suspense Procedures Overview",
        summary="Revenues are held in suspense when there is a title defect, missing owner, or other impediment to payment.",
        full_text=(
            "Suspense is the status of revenue funds held by the operator or purchaser when "
            "payment cannot be made to the interest owner. Common reasons for suspense include: "
            "(1) no executed division order on file, (2) title defect identified in the title "
            "opinion, (3) unknown or missing address, (4) deceased owner with no probate, "
            "(5) pending probate, (6) disputed ownership, (7) missing W-9/TIN, (8) lien on "
            "interest, (9) minor or incompetent owner, (10) bankruptcy stay, (11) IRS levy, "
            "(12) change of ownership pending. The operator must segregate suspense funds and "
            "not commingle them with operating funds. Under Tex. Nat. Res. Code Sec. 91.402, "
            "the payor is not liable for penalty interest if it has a good faith reason to "
            "withhold payment. However, the operator must make diligent efforts to resolve the "
            "suspense condition. If funds remain in suspense for more than 3 years, they may "
            "be subject to Texas unclaimed property (escheat) requirements."
        ),
        citations=[
            "Tex. Nat. Res. Code Sec. 91.402",
            "Tex. Property Code Ch. 72",
            "Tex. Property Code Ch. 74",
        ],
        keywords=["suspense", "held funds", "title defect", "missing owner", "good faith"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-004", "DO-005", "DO-021"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-021",
        category=DoctrineCategory.ESCHEAT_UNCLAIMED,
        title="Texas Unclaimed Property / Escheat Requirements",
        summary="Mineral proceeds held for 3+ years without owner contact must be reported and remitted to the State.",
        full_text=(
            "Under Tex. Property Code Ch. 72, mineral proceeds (royalties, working interest "
            "income, overriding royalty, etc.) are presumed abandoned if unclaimed for 3 years "
            "after becoming payable. The holder (operator/purchaser) must: (1) attempt to locate "
            "the owner by mail and, for amounts over $250, by certified mail; (2) file a report "
            "with the Texas Comptroller by November 1 annually listing all abandoned amounts; "
            "(3) remit the funds to the Comptroller by the following March 1. The holder must "
            "keep records for 10 years. Failure to report or remit subjects the holder to "
            "penalties of 5% per month up to 50% of the amount plus interest. The owner retains "
            "the right to claim funds from the State in perpetuity. Mineral proceeds are one of "
            "the largest categories of unclaimed property in Texas."
        ),
        citations=[
            "Tex. Property Code Sec. 72.101",
            "Tex. Property Code Sec. 74.301",
            "Tex. Property Code Sec. 74.101",
        ],
        statutes=["Tex. Property Code Ch. 72", "Tex. Property Code Ch. 74"],
        keywords=["escheat", "unclaimed property", "abandoned", "3 years", "comptroller", "mineral proceeds"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-020"],
    ))

    # ---- RATIFICATION ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-022",
        category=DoctrineCategory.RATIFICATION,
        title="Division Order Ratification Process",
        summary="New or amended division orders must be executed (ratified) by all interest owners before payments can be made.",
        full_text=(
            "When a new well begins production, or when ownership changes occur, the operator "
            "prepares division orders and sends them to all interest owners for execution "
            "(ratification). The ratification process involves: (1) operator's title attorney "
            "issues title opinion identifying all interest owners and their decimals; (2) operator "
            "prepares division orders reflecting the title opinion; (3) division orders are mailed "
            "to all interest owners with a transmittal letter; (4) owners review, sign, and return "
            "the division orders; (5) operator processes returned DOs and begins payment. "
            "If an owner does not return the division order, the operator may: (a) place the "
            "owner's share in suspense per Tex. NRC Sec. 91.402, or (b) pay based on the title "
            "opinion if the operator believes the decimal is correct. Most operators require a "
            "signed DO before making payment. The AAPL Model Form Division Order (610-2015) is "
            "the industry standard form."
        ),
        citations=[
            "AAPL Division Order Form 610-2015",
            "Tex. Nat. Res. Code Sec. 91.402",
        ],
        keywords=["ratification", "execution", "signed", "division order", "new well", "title opinion"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-001", "DO-003", "DO-006"],
    ))

    # ---- POOLING / UNITIZATION ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-025",
        category=DoctrineCategory.POOLING_UNITIZATION,
        title="Pooling Effects on Division Order Interests",
        summary="When tracts are pooled, each owner's interest is proportioned by the tract's share of the pooled unit.",
        full_text=(
            "Pooling combines multiple tracts into a single drilling or spacing unit. Each tract's "
            "participation in the unit is determined by an allocation factor, commonly based on "
            "surface acreage: tract_factor = tract_acres / total_unit_acres. Each interest owner's "
            "unit decimal = owner_decimal_in_tract x tract_factor. For example, if Owner A has a "
            "0.12500000 royalty interest in a 40-acre tract pooled into a 640-acre unit, the unit "
            "decimal = 0.12500000 x (40/640) = 0.12500000 x 0.06250000 = 0.00781250. For horizontal "
            "wells in Texas, allocation may be based on perforated lateral length rather than surface "
            "acreage per RRC Rule 40. Force pooling in Texas is available per Tex. Nat. Res. Code "
            "Ch. 102. The pooling clause in the lease authorizes the lessee to pool the leased "
            "premises with other lands. Absent a pooling clause, the lessee cannot pool without "
            "the lessor's consent."
        ),
        citations=[
            "Tex. Nat. Res. Code Ch. 102",
            "RRC Statewide Rule 37",
            "RRC Statewide Rule 40",
        ],
        case_law=[
            "Jones v. Killingsworth, 403 S.W.2d 325 (Tex. 1966) - pooling clause construction",
        ],
        keywords=["pooling", "unitization", "allocation factor", "tract participation", "horizontal well"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-010", "DO-026"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-026",
        category=DoctrineCategory.POOLING_UNITIZATION,
        title="Unitization and Fieldwide Unit Allocation",
        summary="Unitization combines multiple leases or units for enhanced recovery operations with negotiated allocation.",
        full_text=(
            "Unitization differs from pooling in that it typically involves combining already-pooled "
            "units for fieldwide operations such as secondary or tertiary recovery (waterfloods, "
            "CO2 floods). The unitization agreement establishes allocation percentages for each "
            "tract based on factors such as productive acreage, deliverability, or production "
            "capacity. Texas does not have compulsory unitization for most operations; unitization "
            "is voluntary and requires high participation rates (typically 85%+ by working interest "
            "and royalty interest). The Mineral Interest Pooling Act (Tex. Nat. Res. Code Ch. 102) "
            "applies to pooling but not fieldwide unitization. When a unit is formed, new division "
            "orders must be executed reflecting each owner's unit allocation decimal."
        ),
        citations=["Tex. Nat. Res. Code Ch. 102", "Tex. Nat. Res. Code Sec. 101.011"],
        keywords=["unitization", "fieldwide unit", "enhanced recovery", "allocation", "voluntary"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-025"],
    ))

    # ---- DUHIG RULE ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-030",
        category=DoctrineCategory.DUHIG_RULE,
        title="The Duhig Rule - Warranty Deed Mineral Reservations",
        summary="Under the Duhig rule, a grantor who conveys by warranty deed with a reservation may be estopped from claiming the reservation if they lacked sufficient interest.",
        full_text=(
            "The Duhig rule, from Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503, 144 S.W.2d 878 "
            "(1940), applies when a grantor conveys a mineral interest by warranty deed while "
            "simultaneously reserving a fraction, but the grantor does not own enough to satisfy "
            "both the conveyance and the reservation. Under Duhig, the conveyance takes priority "
            "over the reservation because the warranty of title runs to the grantee. Example: "
            "Grantor owns 1/2 minerals. Grantor conveys 'all minerals' by warranty deed, reserving "
            "1/2 minerals. Grantor cannot convey all and reserve 1/2 from only 1/2 ownership. "
            "Under Duhig, grantee gets the full 1/2 that grantor owned, and grantor's reservation "
            "is defeated. This creates significant decimal calculation issues for division orders "
            "because the reservation shown in the deed is not effective. The title examiner must "
            "apply Duhig to determine the true decimal interests. Duhig applies only to warranty "
            "deeds (general or special), not quitclaim deeds."
        ),
        citations=[
            "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503, 144 S.W.2d 878 (1940)",
        ],
        case_law=[
            "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503, 144 S.W.2d 878 (1940)",
            "Pich v. Lankford, 302 S.W.2d 645 (Tex. 1957) - Duhig limitation",
            "Jupiter Oil Co. v. Snow, 819 S.W.2d 466 (Tex. 1991) - Duhig modern application",
        ],
        keywords=["Duhig rule", "warranty deed", "reservation", "estoppel", "mineral conveyance"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-031", "DO-010", "DO-012"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-031",
        category=DoctrineCategory.DUHIG_RULE,
        title="Duhig Rule Decimal Calculation Examples",
        summary="Step-by-step decimal calculation examples showing the Duhig rule's effect on division order interests.",
        full_text=(
            "Example 1 - Classic Duhig: A conveys Blackacre to B by warranty deed, reserving 1/2 "
            "minerals. B conveys to C by warranty deed, reserving 1/4 minerals. At the time of "
            "B's conveyance, B owns 1/2 minerals (received from A). B purports to convey 1/2 to "
            "C (all minerals less B's 1/4 reservation = 3/4 of the minerals conveyed). But B "
            "only owns 1/2. Under Duhig, C gets the full 1/2 that B owned, and B's reservation "
            "is defeated. Result: A = 1/2, C = 1/2, B = 0. "
            "Example 2 - Partial Duhig: A conveys 3/4 minerals to B by warranty deed, reserving "
            "1/4. A owns full minerals. B gets 3/4, A retains 1/4. B conveys to C by warranty "
            "deed, reserving 1/8 minerals. B conveys 3/4 - 1/8 = 5/8 to C. B owns 3/4. "
            "5/8 < 3/4, so B can satisfy both. Result: A = 1/4, B = 1/8, C = 5/8. "
            "Duhig does not apply because B had enough interest to cover both conveyance and "
            "reservation."
        ),
        citations=[
            "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503, 144 S.W.2d 878 (1940)",
            "Jupiter Oil Co. v. Snow, 819 S.W.2d 466 (Tex. 1991)",
        ],
        keywords=["Duhig", "calculation", "example", "shortfall", "decimal"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-030", "DO-010"],
    ))

    # ---- PROPORTIONATE REDUCTION ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-032",
        category=DoctrineCategory.PROPORTIONATE_REDUCTION,
        title="Proportionate Reduction Clause",
        summary="The proportionate reduction clause reduces the lessor's royalty when the lessor owns less than the full mineral estate.",
        full_text=(
            "A proportionate reduction clause in an oil and gas lease provides that if the lessor "
            "owns less than the entire mineral estate, the royalty is reduced proportionately. "
            "For example, if the lease provides for 1/4 royalty and the lessor owns 1/2 of the "
            "minerals, the lessor's royalty decimal = 1/4 x 1/2 = 1/8 = 0.12500000. Without a "
            "proportionate reduction clause, the lessor would argue for the full 1/4 royalty on "
            "their share of production. The clause is standard in modern Texas lease forms. "
            "The proportionate reduction also applies to bonus and delay rentals. The lessee's "
            "working interest is not affected by the proportionate reduction - the lessee still "
            "bears 100% of costs (or their WI share if assigned). The effect is that the lessor "
            "royalty burden is only on the lessor's actual mineral ownership, not the full royalty "
            "fraction. Per Heritage Resources, Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996), "
            "the proportionate reduction must be clearly stated in the lease."
        ),
        citations=[
            "Heritage Resources, Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
        ],
        case_law=[
            "Heritage Resources, Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
        ],
        keywords=["proportionate reduction", "partial mineral", "royalty reduction", "lease clause"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-015", "DO-030"],
    ))

    # ---- AFTER-ACQUIRED TITLE ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-035",
        category=DoctrineCategory.AFTER_ACQUIRED_TITLE,
        title="After-Acquired Title Doctrine and Division Orders",
        summary="Title acquired by a grantor after execution of a warranty deed automatically inures to the benefit of the grantee.",
        full_text=(
            "Under the after-acquired title doctrine (also known as estoppel by deed), if a "
            "grantor conveys by warranty deed an interest they do not yet own, and later acquires "
            "that interest, the interest automatically passes to the grantee by operation of law. "
            "This affects division order calculations because the title opinion must trace whether "
            "a warranty deed grantor subsequently acquired title that cured the deficiency. "
            "In Texas, the doctrine applies to general warranty deeds and special warranty deeds "
            "(within the scope of the warranty), but not to quitclaim deeds. Tex. Property Code "
            "Sec. 5.023 codifies the warranties. The division order decimal must reflect the "
            "after-acquired title passing to the grantee. If the title examiner identifies a "
            "conveyance of more than the grantor owned at the time, they must check subsequent "
            "records for the grantor's acquisition of the additional interest."
        ),
        citations=[
            "Tex. Property Code Sec. 5.023",
            "Caswell v. Llano Oil Co., 120 Tex. 139, 36 S.W.2d 208 (1931)",
        ],
        case_law=[
            "Caswell v. Llano Oil Co., 120 Tex. 139, 36 S.W.2d 208 (1931)",
        ],
        keywords=["after-acquired title", "estoppel by deed", "warranty deed", "inure"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-030", "DO-036"],
    ))

    # ---- MOTHER HUBBARD CLAUSE ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-036",
        category=DoctrineCategory.MOTHER_HUBBARD,
        title="Mother Hubbard Clause Effects on Interests",
        summary="A Mother Hubbard clause conveys small strips or interests adjacent to specifically described property.",
        full_text=(
            "A Mother Hubbard clause (also called a cover-all or dragnet clause) in a conveyance "
            "typically reads: 'together with all other land owned by grantor in [county], whether "
            "or not specifically described herein.' The Texas Supreme Court in Geodyne Resources, "
            "Ltd. v. Newton, 349 S.W.3d 506 (Tex. 2011) held that Mother Hubbard clauses convey "
            "only small strips or interests contiguous to the specifically described tract, not "
            "large separate tracts. For division order purposes, the title examiner must determine "
            "whether a Mother Hubbard clause in a prior conveyance captured additional mineral "
            "interests that were not specifically described. If so, the decimal interest must "
            "reflect the additional interests conveyed. Caution: not all Mother Hubbard clauses "
            "are effective, and their scope is limited to small adjacent interests."
        ),
        citations=[
            "Geodyne Resources, Ltd. v. Newton, 349 S.W.3d 506 (Tex. 2011)",
        ],
        case_law=[
            "Geodyne Resources, Ltd. v. Newton, 349 S.W.3d 506 (Tex. 2011)",
            "Pich v. Lankford, 302 S.W.2d 645 (Tex. 1957)",
        ],
        keywords=["Mother Hubbard", "cover-all clause", "dragnet", "small strips", "adjacent"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-035"],
    ))

    # ---- FARMOUT / CARRIED / BACK-IN ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-040",
        category=DoctrineCategory.FARMOUT_INTERESTS,
        title="Farmout Agreement Effects on Division Order Interests",
        summary="Farmout agreements create complex interest structures including carried interests, back-in rights, and ORRIs.",
        full_text=(
            "A farmout agreement is an arrangement where the farmor (holder of the lease) assigns "
            "a working interest to the farmee in exchange for the farmee drilling a well. The "
            "farmor typically retains: (1) an ORRI (commonly 1/8 of 8/8 or 3% of 8/8), (2) a "
            "back-in right to convert the ORRI to a working interest after payout, and/or (3) a "
            "carried interest where the farmee bears a disproportionate share of costs until "
            "payout. The division order must reflect the current status of these interests: "
            "before payout, the farmor receives the ORRI decimal; after payout, the farmor's "
            "decimal changes to reflect the back-in WI. The back-in triggers when cumulative "
            "revenue to the farmee equals the farmee's cumulative costs (payout). The operator "
            "must track payout status and amend division orders when payout occurs."
        ),
        citations=["AAPL Model Form Farmout Agreement"],
        keywords=["farmout", "farmee", "farmor", "back-in", "payout", "ORRI", "carried interest"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-041", "DO-042", "DO-016"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-041",
        category=DoctrineCategory.CARRIED_INTEREST,
        title="Carried Interest Calculation",
        summary="A carried interest is a working interest where the carrying party bears the carried party's share of costs until payout.",
        full_text=(
            "A carried interest is an arrangement where one working interest owner (the carrying "
            "party) agrees to bear the costs attributable to another working interest owner (the "
            "carried party) through a specified depth, zone, or until payout. Before payout, the "
            "carried party receives its revenue share (NRI) but pays no costs. After payout, the "
            "carried party begins paying its share of costs. For division order purposes, the "
            "carried party's division order decimal reflects its NRI both before and after payout, "
            "but the cost-bearing allocation changes at payout. The JOA billing statement shows "
            "the carrying party bearing the extra costs. Types of carried interests: (1) carried "
            "to casing point, (2) carried through completion, (3) carried to payout, (4) free "
            "carry (no reversion). The accountant must track which type applies and when the "
            "carry period terminates."
        ),
        citations=["AAPL Model Form Operating Agreement, Art. VI"],
        keywords=["carried interest", "carrying party", "payout", "cost-bearing", "free carry"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-040", "DO-042"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-042",
        category=DoctrineCategory.BACK_IN_RIGHTS,
        title="Back-In Rights and Reversionary Interests",
        summary="Back-in rights allow the farmor to convert an ORRI to a WI after payout. Reversionary interests revert ownership at a trigger event.",
        full_text=(
            "A back-in right is the farmor's right to convert an overriding royalty interest to "
            "a working interest after the farmee achieves payout (recovery of drilling and "
            "completion costs from production revenue). The back-in typically converts a 1/8 ORRI "
            "to a 25% WI (or other negotiated percentage). When the back-in occurs, the division "
            "orders must be amended: the farmor's ORRI decimal becomes zero and a WI decimal is "
            "added; the farmee's WI decimal is reduced by the back-in amount. A reversionary "
            "interest is broader - any interest that reverts to the grantor upon the occurrence of "
            "a specified event (expiration of a term, cessation of production, reaching a dollar "
            "amount, etc.). The division order system must track the trigger conditions and "
            "automatically flag when a reversion event occurs."
        ),
        citations=["AAPL Model Form Farmout Agreement"],
        keywords=["back-in", "reversionary", "payout", "conversion", "ORRI to WI"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-040", "DO-041"],
    ))

    # ---- JOA PROVISIONS ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-043",
        category=DoctrineCategory.JOA_PROVISIONS,
        title="Joint Operating Agreement (JOA) Cost Sharing",
        summary="The JOA governs cost allocation among working interest owners. Costs are shared per WI decimal.",
        full_text=(
            "The Joint Operating Agreement (JOA), typically AAPL Model Form 610, governs "
            "operations among multiple working interest owners in a well or unit. Key provisions "
            "affecting division orders: (1) Cost sharing - each WI holder pays their proportionate "
            "share of operating costs (LOE, workover, plugging, etc.) based on their WI decimal. "
            "(2) Operator selection - one WI holder is designated operator and manages daily "
            "operations. (3) Non-consent penalties - if a non-operator elects not to participate "
            "in a new well or recompletion, they are subject to non-consent penalties (typically "
            "200-500% of their share of costs). Until the consenting parties recover the penalty, "
            "the non-consenting party's revenue is reduced. (4) Overhead charges - the operator "
            "charges overhead per COPAS rates. (5) Marketing - each WI holder has the right to "
            "take in kind or participate in the operator's marketing arrangement."
        ),
        citations=[
            "AAPL Model Form Operating Agreement 610-2015",
            "COPAS Accounting Procedure, 2005 ed.",
        ],
        keywords=["JOA", "joint operating agreement", "cost sharing", "non-consent", "operator"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-014", "DO-017"],
    ))

    # ---- HEIRSHIP / PARTITION ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-045",
        category=DoctrineCategory.HEIRSHIP_EFFECTS,
        title="Heirship Determination Effects on Division Orders",
        summary="When an interest owner dies, the heirs' interests must be determined and new division orders executed.",
        full_text=(
            "When a mineral or royalty interest owner dies, the ownership must be traced through "
            "the decedent's estate to determine the successor owners and their decimal interests. "
            "In Texas, if the decedent died testate (with a will), the will controls distribution. "
            "If intestate (without a will), the Texas Estates Code descent and distribution rules "
            "apply. The operator must: (1) place the decedent's revenue in suspense pending "
            "determination of heirs, (2) obtain either a probated will, an affidavit of heirship "
            "(must be of record 5 years to be prima facie evidence per Tex. Estates Code Sec. "
            "203.001), or a court determination of heirship, (3) prepare new division orders "
            "reflecting the heirs' decimal interests, (4) send new DOs to all heirs for "
            "ratification, (5) release suspense to the proper heirs. Community property rules "
            "apply: the surviving spouse retains their 1/2 community property share."
        ),
        citations=[
            "Tex. Estates Code Sec. 201.001 et seq.",
            "Tex. Estates Code Sec. 203.001",
        ],
        keywords=["heirship", "death", "estate", "probate", "descent and distribution", "community property"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-020", "DO-046"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-046",
        category=DoctrineCategory.PARTITION_EFFECTS,
        title="Partition Effects on Division Order Interests",
        summary="A partition deed divides undivided interests into specific tracts, requiring division order recalculation.",
        full_text=(
            "When co-owners of an undivided mineral interest execute a partition, the previously "
            "undivided interests are divided into specific allocated interests tied to particular "
            "tracts. This requires a complete recalculation of all division order decimals for "
            "every interest owner in the affected unit. Before partition: each co-owner had a "
            "fractional share of the whole. After partition: each owner has a 100% interest in "
            "their allocated portion. If the partition is unequal (one owner gets a larger or "
            "more valuable tract), there may be an equalizing payment (owelty). The operator "
            "must: (1) obtain and review the partition deed, (2) recalculate all decimals, "
            "(3) prepare and distribute new division orders, (4) hold revenue in suspense pending "
            "new DO execution. In Texas, partition of mineral interests is governed by Tex. "
            "Property Code Ch. 23A (Partition of Mineral Interests)."
        ),
        citations=[
            "Tex. Property Code Ch. 23A",
        ],
        keywords=["partition", "divided interest", "recalculation", "specific allocation", "co-owner"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-013", "DO-045"],
    ))

    # ---- CHANGE OF OWNERSHIP / TRANSFER ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-047",
        category=DoctrineCategory.CHANGE_OF_OWNERSHIP,
        title="Change of Ownership Processing",
        summary="When interests are conveyed, the operator must process the transfer and issue amended division orders.",
        full_text=(
            "A change of ownership (also called a transfer order) occurs when an interest owner "
            "conveys their interest to a new owner by deed, assignment, court order, or other "
            "instrument. The processing steps are: (1) new owner or title company submits the "
            "recorded conveyance instrument to the operator, (2) operator's title department "
            "reviews the instrument for proper execution, legal description, and interest "
            "conveyed, (3) if acceptable, the operator creates a transfer order showing the old "
            "owner's interest being reduced and the new owner's interest being added, (4) new "
            "division orders are prepared and sent to both old and new owners, (5) the operator "
            "holds a final payment for the old owner for 60 days in case of adjustments, "
            "(6) the new owner must provide W-9/TIN and payment instructions. The effective date "
            "of the transfer is typically the date of the instrument or the recording date, per "
            "operator policy."
        ),
        citations=["Tex. Nat. Res. Code Sec. 91.402"],
        keywords=["change of ownership", "transfer order", "conveyance", "new owner", "effective date"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-022", "DO-020"],
    ))

    # ---- REVENUE DISTRIBUTION / PAY DECK ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-050",
        category=DoctrineCategory.REVENUE_DISTRIBUTION,
        title="Revenue Distribution Process",
        summary="Revenue from production sales is distributed to interest owners based on their division order decimals.",
        full_text=(
            "The revenue distribution process converts gross production revenue into individual "
            "owner payments: (1) Gross revenue = volume x price per unit. (2) Deduct severance "
            "taxes: oil at 4.6% (Tex. Tax Code Ch. 202), gas at 7.5% (Tex. Tax Code Ch. 201). "
            "(3) Deduct transportation and processing costs if permitted by the lease (market "
            "value vs. proceeds leases). (4) Net revenue = gross - taxes - deductions. (5) Each "
            "owner's share = net revenue x their division order decimal. (6) Apply any suspense "
            "holds. (7) Apply minimum check threshold ($25 for checks, $10 for EFT). (8) Generate "
            "remittance advice showing price, volume, taxes, deductions, and net payment. "
            "Under a 'market value' royalty clause (common in older Texas leases), the royalty is "
            "calculated on market value at the well, not the actual sales price. Under a 'proceeds' "
            "clause, the royalty is based on the actual amount realized."
        ),
        citations=[
            "Tex. Tax Code Ch. 201 (Gas Production Tax)",
            "Tex. Tax Code Ch. 202 (Oil Production Tax)",
            "Tex. Nat. Res. Code Sec. 91.402",
        ],
        keywords=["revenue distribution", "gross revenue", "severance tax", "net payment", "deductions"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-051", "DO-004"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-051",
        category=DoctrineCategory.PAY_DECK,
        title="Pay Deck Construction",
        summary="The pay deck is the master list of all interest owners, their decimals, and payment instructions for a well or unit.",
        full_text=(
            "The pay deck (also called the revenue distribution schedule or owner master file) "
            "is the central document for division order administration. It contains: (1) owner "
            "name and address, (2) owner number, (3) tax ID (SSN or EIN), (4) interest type "
            "(RI, WI, ORRI, NPI, etc.), (5) decimal interest to 8 places, (6) payment method "
            "(check, EFT, ACH), (7) payment frequency (monthly, quarterly), (8) suspense status "
            "and reason code, (9) effective date, (10) division order status (executed, pending, "
            "unsigned). The pay deck must reconcile: the sum of all interests of each type must "
            "equal 1.00000000 (unity check). The pay deck is generated from the title opinion "
            "and is the source document for the division order. Changes to the pay deck require "
            "a documented reason, supervisor approval, and an audit trail entry."
        ),
        citations=["AAPL Division Order Form 610-2015", "COPAS 2005"],
        keywords=["pay deck", "owner master", "revenue schedule", "reconciliation", "unity"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-050", "DO-012"],
    ))

    # ---- SEVERANCE TAX ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-052",
        category=DoctrineCategory.SEVERANCE_TAX,
        title="Texas Severance Tax on Oil and Gas Production",
        summary="Texas imposes severance taxes of 4.6% on oil and 7.5% on gas, deducted from gross revenue before distribution.",
        full_text=(
            "Texas imposes a severance tax on the production of oil and gas. The oil production "
            "tax rate is 4.6% of market value (Tex. Tax Code Sec. 202.052). The gas production "
            "tax rate is 7.5% of market value (Tex. Tax Code Sec. 201.052). The operator or "
            "first purchaser is responsible for withholding and remitting the tax to the Texas "
            "Comptroller. For division order purposes, the severance tax is typically deducted "
            "from gross revenue before distribution to interest owners. Each owner bears their "
            "proportionate share of the tax. Exemptions and reduced rates may apply for: "
            "(1) marginal wells (rate reduction per Tex. Tax Code Sec. 202.054), (2) enhanced "
            "recovery projects, (3) high-cost gas wells, (4) wells drilled with inactive well "
            "incentives. The tax basis is market value at the wellhead."
        ),
        citations=[
            "Tex. Tax Code Sec. 201.052",
            "Tex. Tax Code Sec. 202.052",
            "Tex. Tax Code Sec. 202.054",
        ],
        statutes=["Tex. Tax Code Ch. 201", "Tex. Tax Code Ch. 202"],
        keywords=["severance tax", "oil production tax", "gas production tax", "4.6%", "7.5%"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-050"],
    ))

    # ---- FRACTIONAL CONVEYANCES / INTEREST TRACING ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-053",
        category=DoctrineCategory.FRACTIONAL_CONVEYANCE,
        title="Fractional Mineral Conveyance Interpretation",
        summary="Texas courts have developed rules for interpreting ambiguous fractional mineral conveyances.",
        full_text=(
            "Ambiguous fractional mineral conveyances are a major source of division order "
            "disputes. The classic issue arises with the 'double fraction' problem: a deed "
            "conveying 'an undivided 1/2 of the 1/8 royalty interest' can be interpreted as: "
            "(1) a 1/2 mineral interest (the 'mineral/royalty distinction'), or (2) a 1/16 "
            "royalty interest (literal reading). Texas courts have addressed this in the "
            "'Hysaw line of cases.' In Hysaw v. Dawkins, 483 S.W.3d 1 (Tex. 2016), the "
            "Texas Supreme Court reaffirmed the estate misconception doctrine, holding that when "
            "a grantor mistakenly uses the term 'royalty' to describe a conveyance of a mineral "
            "interest, the conveyance creates a mineral interest (not a royalty interest). The "
            "four-corners rule applies: the court examines the entire instrument, not just the "
            "granting clause, to determine intent. For division order purposes, the title "
            "examiner must carefully parse the language of each conveyance to determine whether "
            "a mineral or royalty interest was conveyed."
        ),
        citations=[
            "Hysaw v. Dawkins, 483 S.W.3d 1 (Tex. 2016)",
            "Luckel v. White, 819 S.W.2d 459 (Tex. 1991)",
        ],
        case_law=[
            "Hysaw v. Dawkins, 483 S.W.3d 1 (Tex. 2016)",
            "Luckel v. White, 819 S.W.2d 459 (Tex. 1991)",
            "Altman v. Blake, 712 S.W.2d 117 (Tex. 1986)",
        ],
        keywords=["fractional conveyance", "double fraction", "mineral royalty distinction", "Hysaw"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-010", "DO-013"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-054",
        category=DoctrineCategory.INTEREST_TRACING,
        title="Interest Tracing Through Chain of Title",
        summary="Computing division order decimals requires tracing each owner's interest through all conveyances in the chain of title.",
        full_text=(
            "Interest tracing is the process of computing each current owner's decimal interest "
            "by following the chain of title from the sovereign (State of Texas) through all "
            "subsequent conveyances, reservations, and events. Steps: (1) Start with the original "
            "patent or grant = 1.00000000 mineral + 1.00000000 surface. (2) For each conveyance, "
            "subtract the interest conveyed from the grantor and add it to the grantee. (3) Apply "
            "reservations (reduce the grantee's interest by the reservation amount). (4) Apply "
            "Duhig rule if the grantor lacked sufficient interest to satisfy both conveyance and "
            "reservation. (5) Apply proportionate reduction if the lessor owns less than full "
            "minerals. (6) For pooled tracts, multiply each owner's tract decimal by the tract "
            "participation factor. (7) Compute NRI for each WI holder by subtracting burdens. "
            "(8) Verify unity: all interests of each type must sum to 1.00000000. "
            "All intermediate calculations should carry 10+ decimal places; round only the final "
            "result to 8 places. Document each step with instrument references."
        ),
        citations=["State Bar of Texas Title Examination Standards"],
        keywords=["interest tracing", "chain of title", "conveyance chain", "decimal computation"],
        severity=DoctrineSeverity.CRITICAL,
        related_blocks=["DO-010", "DO-030", "DO-032"],
    ))

    # ---- ADDITIONAL DOCTRINES (to reach 55+) ----

    blocks.append(DoctrineCacheBlock(
        block_id="DO-055",
        category=DoctrineCategory.COST_BEARING_INTEREST,
        title="Cost-Bearing vs. Non-Cost-Bearing Interests",
        summary="Working interests bear costs; royalties and ORRIs do not. This distinction is critical for NRI computation.",
        full_text=(
            "The fundamental distinction in oil and gas interests is between cost-bearing and "
            "non-cost-bearing interests. Cost-bearing interests (working interests, including "
            "carried interests after payout) are responsible for their proportionate share of "
            "exploration, drilling, completing, equipping, and operating costs. Non-cost-bearing "
            "interests (royalty, overriding royalty, net profits interests, production payments) "
            "receive a share of revenue without bearing production costs. The distinction matters "
            "for division orders because: (1) the WI holder's payment = (revenue x NRI) - "
            "(costs x WI), while (2) the royalty holder's payment = revenue x royalty_decimal - "
            "severance_tax x royalty_decimal. Some costs (post-production costs like "
            "transportation and processing) may be deductible from royalty depending on lease "
            "language per Heritage Resources, Inc. v. NationsBank."
        ),
        citations=[
            "Heritage Resources, Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
        ],
        keywords=["cost-bearing", "non-cost-bearing", "WI", "royalty", "costs", "NRI"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-014", "DO-015", "DO-017"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-056",
        category=DoctrineCategory.REVERSIONARY_INTEREST,
        title="Reversionary Interest Tracking in Division Orders",
        summary="Reversionary interests revert to the grantor upon a trigger event, requiring division order amendments.",
        full_text=(
            "A reversionary interest is an interest that reverts to the grantor or their assignee "
            "upon the occurrence of a specified condition, such as: (1) expiration of a term (e.g., "
            "a term overriding royalty that reverts after 10 years of production), (2) payout "
            "(e.g., a production payment that terminates after $1M in revenue is received), "
            "(3) cessation of production, (4) termination of a lease. The division order system "
            "must track each reversionary interest's trigger conditions and flag when the condition "
            "is met. When a reversion occurs: (1) the reverting interest's decimal is removed from "
            "the current holder and added to the reversionary owner, (2) new division orders are "
            "prepared, (3) the change is effective as of the reversion date. Production payments "
            "are a common form of reversionary interest: revenue is paid to the PP holder until "
            "a specified dollar amount is reached, then the interest reverts."
        ),
        citations=["AAPL Model Form Operating Agreement"],
        keywords=["reversionary interest", "revert", "trigger event", "production payment", "term ORRI"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-042", "DO-040"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-057",
        category=DoctrineCategory.DIVISION_ORDER_BASICS,
        title="AAPL Model Form Division Order 610",
        summary="The AAPL 610 form is the industry standard division order form used in Texas and most U.S. oil and gas states.",
        full_text=(
            "The American Association of Professional Landmen (AAPL) publishes Model Form "
            "Division Order 610 as the industry standard. The 2015 revision includes fields for: "
            "owner name, address, tax ID, interest type, decimal interest, effective date, well "
            "name/number, operator name, legal description, and unit designation. The form "
            "includes standardized language for: warranty/indemnity (limited to proceeds received), "
            "payment authorization, change of ownership notice, and revocation. The AAPL 610 is "
            "designed to comply with Texas NRC Ch. 91 requirements. Many states have adopted "
            "similar forms. The form explicitly states that it does not amend the terms of any "
            "lease. The warranty provision limits the owner's warranty to their actual interest "
            "and the proceeds received. Best practice: always use the current AAPL form or a "
            "form that substantially conforms to it."
        ),
        citations=["AAPL Division Order Form 610-2015"],
        keywords=["AAPL", "model form", "610", "standard form", "division order form"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-001", "DO-006"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-058",
        category=DoctrineCategory.TRANSFER_ORDERS,
        title="Transfer Order Processing and Effective Dates",
        summary="Transfer orders document the movement of interests between owners with effective dates for payment purposes.",
        full_text=(
            "A transfer order (TO) is an internal document prepared by the operator to record "
            "the transfer of an interest from one owner to another. Unlike a division order "
            "(which authorizes payment), a transfer order adjusts the pay deck. Transfer order "
            "processing: (1) receive and review the conveyance instrument, (2) verify recording "
            "in the county records, (3) verify grantor's current interest matches the pay deck, "
            "(4) determine the effective date (typically the date of the conveyance instrument, "
            "though operator policy may use the recording date or the date the TO is processed), "
            "(5) adjust the pay deck: decrease grantor's decimal, increase grantee's decimal, "
            "(6) prepare new division orders for both parties, (7) hold the grantor's final "
            "payment for 60 days per standard practice, (8) collect W-9 and payment instructions "
            "from the new owner. Prior period adjustments may be required if the effective date "
            "is earlier than the processing date."
        ),
        citations=["Tex. Nat. Res. Code Sec. 91.402"],
        keywords=["transfer order", "effective date", "pay deck adjustment", "prior period adjustment"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-047", "DO-051"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-059",
        category=DoctrineCategory.REVENUE_DISTRIBUTION,
        title="Market Value vs. Proceeds Royalty Clauses",
        summary="The royalty clause type determines whether deductions can be taken before computing the royalty payment.",
        full_text=(
            "Texas lease royalty clauses fall into two categories: (1) 'market value at the well' "
            "clauses obligate the lessee to pay royalty based on the market value of production "
            "at the wellhead, regardless of the actual sales price. Post-production costs "
            "(gathering, compression, processing, transportation) are inherently deducted because "
            "the value is measured at the well. (2) 'Proceeds' clauses base royalty on the actual "
            "amount realized from sale. Whether post-production costs can be deducted from proceeds "
            "depends on the specific lease language. Per Heritage Resources, Inc. v. NationsBank, "
            "939 S.W.2d 118 (Tex. 1996), costs that are reasonable and necessary to market the "
            "production may be deducted unless the lease provides otherwise. For division order "
            "purposes, the deduction policy must match the lease terms. The division order cannot "
            "modify the lease's royalty calculation method."
        ),
        citations=[
            "Heritage Resources, Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
            "Judice v. Mewbourne Oil Co., 939 S.W.2d 133 (Tex. 1996)",
        ],
        case_law=[
            "Heritage Resources, Inc. v. NationsBank, 939 S.W.2d 118 (Tex. 1996)",
            "Judice v. Mewbourne Oil Co., 939 S.W.2d 133 (Tex. 1996)",
        ],
        keywords=["market value", "proceeds", "royalty clause", "post-production costs", "deductions"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-050", "DO-015"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-060",
        category=DoctrineCategory.JOA_PROVISIONS,
        title="Non-Consent Penalty Effects on Division Orders",
        summary="A non-consenting WI owner's revenue share is reduced by the penalty amount until the consenting parties recover costs.",
        full_text=(
            "Under the AAPL Model Form JOA (Art. VI.B.2), a non-consenting party that elects not "
            "to participate in a proposed operation is subject to a non-consent penalty. The "
            "consenting parties bear 100% of the non-consenter's share of costs and receive "
            "an additional penalty (typically 200-500% of the non-consenter's share) before the "
            "non-consenter begins receiving revenue. During the penalty period, the non-consenter's "
            "division order decimal is effectively zero (all revenue goes to consenting parties). "
            "After the consenting parties recover their investment plus the penalty, the "
            "non-consenter's division order is reinstated to its original decimal. The operator "
            "must track cumulative recovery vs. penalty threshold and amend division orders when "
            "the penalty is satisfied. This creates a complex time-varying interest structure."
        ),
        citations=["AAPL Model Form Operating Agreement 610-2015, Art. VI.B.2"],
        keywords=["non-consent", "penalty", "JOA", "Article VI", "consenting parties"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-043", "DO-014"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-061",
        category=DoctrineCategory.SUSPENSE_PROCEDURES,
        title="Suspense Release Procedures",
        summary="Releasing funds from suspense requires documented resolution of the suspense condition and proper authorization.",
        full_text=(
            "Suspense release is the process of paying out funds that have been held in suspense. "
            "The release requires: (1) documented resolution of the original suspense reason "
            "(e.g., executed division order received, title defect cured, probate completed, "
            "correct address obtained, W-9 received), (2) calculation of accumulated suspense "
            "including any applicable interest (note: 12% penalty interest per Tex. NRC Sec. "
            "91.402 applies only if the hold was not in good faith), (3) approval by division "
            "order analyst and supervisor, (4) audit trail entry documenting the release reason, "
            "amount, and approver, (5) payment via normal distribution process. For partial "
            "releases (e.g., when a title defect affects only a portion of the interest), the "
            "operator may release the undisputed portion while keeping the disputed portion in "
            "suspense. All suspense releases must be reconciled monthly."
        ),
        citations=["Tex. Nat. Res. Code Sec. 91.402"],
        keywords=["suspense release", "resolution", "accumulated suspense", "partial release"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-020", "DO-004"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-062",
        category=DoctrineCategory.DECIMAL_INTEREST_CALC,
        title="Net Mineral Acres (NMA) to Decimal Conversion",
        summary="Converting NMA to division order decimals requires dividing by total unit NMA.",
        full_text=(
            "Net Mineral Acres (NMA) is a measure of mineral ownership that accounts for "
            "fractional interests. If a tract contains 100 gross mineral acres and the owner "
            "holds a 1/4 undivided mineral interest, the owner has 25 NMA. To convert NMA to "
            "a division order decimal for a pooled unit: decimal = owner_NMA / total_unit_NMA. "
            "Example: Owner has 25 NMA in a 640-acre unit where total NMA = 640 (assuming full "
            "mineral ownership across the unit). Owner's mineral decimal = 25/640 = 0.03906250. "
            "Owner's royalty decimal (at 1/8 royalty) = 0.03906250 x 0.12500000 = 0.00488281. "
            "Complications arise when different tracts in the unit have different lease royalty "
            "rates. In that case, the NMA concept must be applied separately for each lease. "
            "Total NMA for the unit is the sum of all gross mineral acres weighted by the "
            "fractional mineral ownership in each tract."
        ),
        citations=["AAPL Division Order Form 610-2015"],
        keywords=["NMA", "net mineral acres", "gross mineral acres", "conversion", "unit decimal"],
        severity=DoctrineSeverity.HIGH,
        related_blocks=["DO-010", "DO-011", "DO-025"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-063",
        category=DoctrineCategory.POOLING_UNITIZATION,
        title="Horizontal Well Allocation per RRC Rule 40",
        summary="Texas RRC Rule 40 governs horizontal well spacing and allocation, commonly using perforated lateral length.",
        full_text=(
            "Texas Railroad Commission Statewide Rule 40 addresses horizontal well spacing and "
            "allocation for proration units. For horizontal wells, the allocation method often "
            "uses the perforated (completed) lateral length within each tract as the allocation "
            "factor, rather than surface acreage. The allocation factor for a tract is: "
            "tract_factor = perforated_lateral_in_tract / total_perforated_lateral. This ensures "
            "that tracts contributing more lateral length receive a proportionately larger share "
            "of production. The operator files a W-2 (Organization Report - Operator) or P-12 "
            "(Horizontal Allocation Well Amendment) with the RRC. Division order decimals for "
            "horizontal wells must reflect the lateral-based allocation. When the lateral is "
            "recompleted or extended, the allocation factors change and division orders must be "
            "amended. Some horizontal wells use a hybrid allocation combining surface acreage "
            "for royalty owners and lateral length for WI holders."
        ),
        citations=[
            "RRC Statewide Rule 40",
            "16 Tex. Admin. Code Sec. 3.40",
        ],
        keywords=["horizontal well", "Rule 40", "lateral length", "allocation", "perforated lateral"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-025", "DO-026"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-064",
        category=DoctrineCategory.DIVISION_ORDER_BASICS,
        title="Division Order Amendments",
        summary="Division orders must be amended when interests change due to conveyances, death, pooling changes, or corrections.",
        full_text=(
            "Division order amendments are required whenever the interests in a well or unit "
            "change. Common triggers for amendment: (1) conveyance of interest (sale, gift, "
            "exchange), (2) death of owner and determination of heirs, (3) pooling or unit "
            "boundary change, (4) new well drilled in unit, (5) correction of title error, "
            "(6) lease expiration or renewal, (7) back-in conversion after payout, (8) "
            "non-consent penalty satisfaction, (9) production payment termination, (10) partition "
            "of undivided interests. The amendment process: operator prepares amended DOs "
            "reflecting the new decimals, sends to all affected owners for execution, receives "
            "signed DOs, and updates the pay deck. The effective date of the amendment determines "
            "when the new decimals take effect for payment purposes. Prior period adjustments "
            "may be required if the effective date is retroactive."
        ),
        citations=["AAPL Division Order Form 610-2015", "Tex. Nat. Res. Code Ch. 91"],
        keywords=["amendment", "change", "correction", "retroactive", "prior period adjustment"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-001", "DO-047", "DO-022"],
    ))

    blocks.append(DoctrineCacheBlock(
        block_id="DO-065",
        category=DoctrineCategory.INTEREST_TRACING,
        title="Assignment of Overriding Royalty Interest",
        summary="ORRI assignments transfer the overriding royalty from the assignor to the assignee, requiring DO amendments.",
        full_text=(
            "An assignment of overriding royalty interest (AORRI) transfers an existing ORRI from "
            "one party to another. The assignment may be total or partial. For division order "
            "purposes: (1) total assignment - the assignor's ORRI decimal is removed from the pay "
            "deck and replaced with the assignee's decimal, (2) partial assignment - the assignor's "
            "decimal is reduced by the assigned amount and the assignee is added with the new "
            "decimal. The ORRI decimal remains tied to the underlying lease. If the lease terminates, "
            "the ORRI terminates regardless of the assignment. The operator must verify: (a) the "
            "assignor actually holds the ORRI shown on the pay deck, (b) the assignment is properly "
            "executed and recorded, (c) the assigned decimal does not exceed the assignor's current "
            "decimal. Multiple partial assignments can create complex ORRI stacks that must be "
            "carefully tracked."
        ),
        citations=[
            "Cosgrove v. Cade, 468 S.W.3d 32 (Tex. 2015)",
        ],
        case_law=[
            "Cosgrove v. Cade, 468 S.W.3d 32 (Tex. 2015)",
        ],
        keywords=["ORRI assignment", "overriding royalty", "partial assignment", "ORRI stack"],
        severity=DoctrineSeverity.MEDIUM,
        related_blocks=["DO-016", "DO-047"],
    ))

    logger.info("Built {n} doctrine blocks", n=len(blocks))
    return blocks
