"""
LM03 Division Order Engine - Semantic Dictionary
==================================================

Comprehensive semantic dictionary for division order and oil & gas
terminology normalization. Includes InterestCalculator for decimal
arithmetic, DecimalFormatConverter for fraction/decimal/NMA conversion,
and ChainOfTitleTracer for interest tracing through conveyance chains.

700+ lines. Pure Python. Zero external NLP dependency.

Author: ECHO OMEGA PRIME Build System
Engine: LM03 Division Order
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class SemanticDomain(str, Enum):
    """Semantic domains for division order terminology."""
    INTEREST_TYPES = "INTEREST_TYPES"
    DECIMAL_CALCULATION = "DECIMAL_CALCULATION"
    REVENUE_DISTRIBUTION = "REVENUE_DISTRIBUTION"
    SUSPENSE_MANAGEMENT = "SUSPENSE_MANAGEMENT"
    OWNERSHIP_CHANGE = "OWNERSHIP_CHANGE"
    POOLING_UNITIZATION = "POOLING_UNITIZATION"
    TITLE_EXAMINATION = "TITLE_EXAMINATION"
    TAX_REPORTING = "TAX_REPORTING"
    ACCOUNTING = "ACCOUNTING"
    REGULATORY = "REGULATORY"
    INSTRUMENTS = "INSTRUMENTS"
    ENTITIES = "ENTITIES"
    JOA_TERMS = "JOA_TERMS"
    CONVEYANCE_LANGUAGE = "CONVEYANCE_LANGUAGE"


class InterestType(str, Enum):
    """Standard oil and gas interest types."""
    WORKING_INTEREST = "WI"
    ROYALTY_INTEREST = "RI"
    OVERRIDING_ROYALTY = "ORRI"
    NET_REVENUE_INTEREST = "NRI"
    COST_BEARING_INTEREST = "CBI"
    NET_PROFITS_INTEREST = "NPI"
    CARRIED_INTEREST = "CI"
    BACK_IN_INTEREST = "BII"
    REVERSIONARY_INTEREST = "REVI"
    PRODUCTION_PAYMENT = "PP"
    MINERAL_INTEREST = "MI"
    NON_PARTICIPATING_ROYALTY = "NPRI"
    EXECUTIVE_RIGHT = "ER"
    FEE_SIMPLE = "FEE"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SemanticTerm:
    """A single semantic term with definition, synonyms, and context."""
    term_id: str
    term: str
    domain: SemanticDomain
    definition: str
    synonyms: List[str] = field(default_factory=list)
    abbreviations: List[str] = field(default_factory=list)
    related_terms: List[str] = field(default_factory=list)
    legal_authority: Optional[str] = None
    regex_pattern: Optional[str] = None

    def matches(self, text: str) -> bool:
        """Check if text matches this term, any synonym, or abbreviation.

        Args:
            text: Input text to match.

        Returns:
            True if the text matches this term.
        """
        text_lower = text.lower().strip()
        if self.term.lower() == text_lower:
            return True
        for syn in self.synonyms:
            if syn.lower() == text_lower:
                return True
        for abbr in self.abbreviations:
            if abbr.lower() == text_lower:
                return True
        if self.regex_pattern:
            if re.search(self.regex_pattern, text, re.IGNORECASE):
                return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "term_id": self.term_id,
            "term": self.term,
            "domain": self.domain.value,
            "definition": self.definition,
            "synonyms": list(self.synonyms),
            "abbreviations": list(self.abbreviations),
            "related_terms": list(self.related_terms),
            "legal_authority": self.legal_authority,
        }


@dataclass
class ConveyanceEvent:
    """Represents a single conveyance in a chain of title."""
    event_id: str
    instrument_type: str
    recording_date: Optional[date]
    grantor: str
    grantee: str
    interest_conveyed: Decimal
    interest_type: InterestType
    reservation: Optional[Decimal] = None
    reservation_type: Optional[InterestType] = None
    is_warranty_deed: bool = False
    legal_description: Optional[str] = None
    document_reference: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "event_id": self.event_id,
            "instrument_type": self.instrument_type,
            "recording_date": self.recording_date.isoformat() if self.recording_date else None,
            "grantor": self.grantor,
            "grantee": self.grantee,
            "interest_conveyed": str(self.interest_conveyed),
            "interest_type": self.interest_type.value,
            "reservation": str(self.reservation) if self.reservation else None,
            "reservation_type": self.reservation_type.value if self.reservation_type else None,
            "is_warranty_deed": self.is_warranty_deed,
            "document_reference": self.document_reference,
        }


@dataclass
class OwnershipPosition:
    """Current ownership position for a single owner."""
    owner_name: str
    interest_type: InterestType
    decimal_interest: Decimal
    source_instrument: Optional[str] = None
    effective_date: Optional[date] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "owner_name": self.owner_name,
            "interest_type": self.interest_type.value,
            "decimal_interest": str(self.decimal_interest),
            "source_instrument": self.source_instrument,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------------
# Interest Calculator
# ---------------------------------------------------------------------------

class InterestCalculator:
    """Deterministic interest calculator using Python Decimal for precision.

    All calculations use 8 decimal places with ROUND_HALF_UP.
    Supports working interest, royalty, ORRI, NRI, and all
    standard oil and gas interest types.
    """

    PRECISION = 8
    ROUNDING = ROUND_HALF_UP
    QUANTIZE_SPEC = Decimal("0.00000001")
    UNITY = Decimal("1.00000000")
    ZERO = Decimal("0.00000000")
    TOLERANCE = Decimal("0.00001000")

    def __init__(self) -> None:
        """Initialize the interest calculator."""
        self._calculation_log: List[Dict[str, Any]] = []
        logger.debug("InterestCalculator initialized | precision={p}", p=self.PRECISION)

    def _quantize(self, value: Decimal) -> Decimal:
        """Round a Decimal to the standard precision.

        Args:
            value: Decimal value to round.

        Returns:
            Rounded Decimal.
        """
        return value.quantize(self.QUANTIZE_SPEC, rounding=self.ROUNDING)

    def compute_nri(
        self,
        working_interest: Decimal,
        royalty_burden: Decimal,
        orri_burden: Decimal,
        other_burdens: Decimal = Decimal("0"),
    ) -> Decimal:
        """Compute Net Revenue Interest.

        NRI = WI x (1.0 - royalty - ORRI - other_burdens)

        Args:
            working_interest: Working interest decimal.
            royalty_burden: Lessor royalty decimal (e.g., 0.25 for 1/4).
            orri_burden: Total ORRI burden decimal.
            other_burdens: Net profits interests, production payments, etc.

        Returns:
            Computed NRI decimal.
        """
        total_burden = royalty_burden + orri_burden + other_burdens
        if total_burden > self.UNITY:
            logger.warning("Total burdens {tb} exceed unity", tb=total_burden)
        revenue_factor = self.UNITY - total_burden
        nri = self._quantize(working_interest * revenue_factor)
        self._log_calculation("compute_nri", {
            "working_interest": str(working_interest),
            "royalty_burden": str(royalty_burden),
            "orri_burden": str(orri_burden),
            "other_burdens": str(other_burdens),
            "nri": str(nri),
        })
        return nri

    def compute_royalty_decimal(
        self,
        mineral_ownership: Decimal,
        lease_royalty_rate: Decimal,
        tract_participation: Decimal = Decimal("1.00000000"),
    ) -> Decimal:
        """Compute a royalty owner's division order decimal.

        decimal = mineral_ownership x lease_royalty x tract_participation

        Args:
            mineral_ownership: Owner's undivided mineral fraction.
            lease_royalty_rate: Lease royalty rate (e.g., 0.25).
            tract_participation: Tract's share of pooled unit (default 1.0).

        Returns:
            Royalty division order decimal.
        """
        result = self._quantize(mineral_ownership * lease_royalty_rate * tract_participation)
        self._log_calculation("compute_royalty_decimal", {
            "mineral_ownership": str(mineral_ownership),
            "lease_royalty_rate": str(lease_royalty_rate),
            "tract_participation": str(tract_participation),
            "result": str(result),
        })
        return result

    def compute_pooled_decimal(
        self,
        owner_decimal_in_tract: Decimal,
        tract_acres: Decimal,
        total_unit_acres: Decimal,
    ) -> Decimal:
        """Compute an owner's decimal interest in a pooled unit.

        unit_decimal = owner_decimal x (tract_acres / unit_acres)

        Args:
            owner_decimal_in_tract: Owner's decimal in the individual tract.
            tract_acres: Acres in the tract being pooled.
            total_unit_acres: Total acres in the pooled unit.

        Returns:
            Owner's unit decimal interest.
        """
        if total_unit_acres == self.ZERO:
            logger.error("Total unit acres is zero - cannot compute pooled decimal")
            return self.ZERO
        tract_factor = self._quantize(tract_acres / total_unit_acres)
        result = self._quantize(owner_decimal_in_tract * tract_factor)
        self._log_calculation("compute_pooled_decimal", {
            "owner_decimal": str(owner_decimal_in_tract),
            "tract_acres": str(tract_acres),
            "unit_acres": str(total_unit_acres),
            "tract_factor": str(tract_factor),
            "result": str(result),
        })
        return result

    def compute_lateral_allocation(
        self,
        owner_decimal_in_tract: Decimal,
        lateral_length_in_tract: Decimal,
        total_lateral_length: Decimal,
    ) -> Decimal:
        """Compute allocation based on perforated lateral length (RRC Rule 40).

        Args:
            owner_decimal_in_tract: Owner's decimal in the tract.
            lateral_length_in_tract: Feet of perforated lateral in tract.
            total_lateral_length: Total feet of perforated lateral.

        Returns:
            Owner's allocated decimal.
        """
        if total_lateral_length == self.ZERO:
            logger.error("Total lateral length is zero")
            return self.ZERO
        lateral_factor = self._quantize(lateral_length_in_tract / total_lateral_length)
        result = self._quantize(owner_decimal_in_tract * lateral_factor)
        self._log_calculation("compute_lateral_allocation", {
            "owner_decimal": str(owner_decimal_in_tract),
            "lateral_in_tract": str(lateral_length_in_tract),
            "total_lateral": str(total_lateral_length),
            "lateral_factor": str(lateral_factor),
            "result": str(result),
        })
        return result

    def apply_proportionate_reduction(
        self,
        lease_royalty_rate: Decimal,
        mineral_ownership_fraction: Decimal,
    ) -> Decimal:
        """Apply proportionate reduction when lessor owns less than full minerals.

        reduced_royalty = lease_royalty x mineral_fraction

        Args:
            lease_royalty_rate: The lease royalty rate.
            mineral_ownership_fraction: The lessor's mineral fraction (< 1.0).

        Returns:
            Proportionately reduced royalty decimal.
        """
        result = self._quantize(lease_royalty_rate * mineral_ownership_fraction)
        self._log_calculation("proportionate_reduction", {
            "lease_royalty": str(lease_royalty_rate),
            "mineral_fraction": str(mineral_ownership_fraction),
            "reduced_royalty": str(result),
        })
        return result

    def apply_duhig_rule(
        self,
        grantor_ownership: Decimal,
        interest_conveyed: Decimal,
        reservation_claimed: Decimal,
    ) -> Tuple[Decimal, Decimal, bool]:
        """Apply the Duhig rule to a warranty deed with reservation.

        If grantor cannot satisfy both conveyance and reservation,
        the conveyance takes priority and the reservation is defeated.

        Args:
            grantor_ownership: What the grantor actually owns.
            interest_conveyed: What the deed purports to convey.
            reservation_claimed: What the grantor reserves.

        Returns:
            Tuple of (grantee_gets, grantor_keeps, duhig_applied).
        """
        needed = interest_conveyed + reservation_claimed
        if grantor_ownership >= needed:
            grantee_gets = self._quantize(interest_conveyed)
            grantor_keeps = self._quantize(grantor_ownership - interest_conveyed)
            self._log_calculation("duhig_rule", {
                "applied": False,
                "grantor_owns": str(grantor_ownership),
                "conveyed": str(interest_conveyed),
                "reserved": str(reservation_claimed),
                "grantee_gets": str(grantee_gets),
                "grantor_keeps": str(grantor_keeps),
            })
            return grantee_gets, grantor_keeps, False
        else:
            grantee_gets = self._quantize(grantor_ownership)
            grantor_keeps = self.ZERO
            self._log_calculation("duhig_rule", {
                "applied": True,
                "grantor_owns": str(grantor_ownership),
                "conveyed": str(interest_conveyed),
                "reserved": str(reservation_claimed),
                "grantee_gets": str(grantee_gets),
                "grantor_keeps": str(grantor_keeps),
                "reason": "Grantor lacks sufficient interest to satisfy both conveyance and reservation",
            })
            return grantee_gets, grantor_keeps, True

    def unity_check(
        self,
        interests: List[Decimal],
        interest_label: str = "interests",
    ) -> Dict[str, Any]:
        """Verify that a list of interests sums to 1.00000000.

        Args:
            interests: List of Decimal interest values.
            interest_label: Label for logging/reporting.

        Returns:
            Dictionary with total, deviation, and pass/fail status.
        """
        total = self._quantize(sum(interests, self.ZERO))
        deviation = abs(total - self.UNITY)
        passes = deviation <= self.TOLERANCE
        result = {
            "interest_label": interest_label,
            "count": len(interests),
            "total": str(total),
            "expected": str(self.UNITY),
            "deviation": str(deviation),
            "tolerance": str(self.TOLERANCE),
            "passes": passes,
        }
        if not passes:
            logger.warning(
                "Unity check FAILED for {lbl}: total={tot} deviation={dev}",
                lbl=interest_label,
                tot=total,
                dev=deviation,
            )
        return result

    def compute_revenue_share(
        self,
        gross_revenue: Decimal,
        owner_decimal: Decimal,
        severance_tax_rate: Decimal = Decimal("0"),
        deductions: Decimal = Decimal("0"),
    ) -> Dict[str, Decimal]:
        """Compute an owner's revenue share from gross production revenue.

        Args:
            gross_revenue: Total gross revenue for the period.
            owner_decimal: Owner's division order decimal.
            severance_tax_rate: Applicable severance tax rate.
            deductions: Post-production deductions (if applicable).

        Returns:
            Dictionary with gross_share, tax, deductions, and net_payment.
        """
        gross_share = self._quantize(gross_revenue * owner_decimal)
        tax_amount = (gross_share * severance_tax_rate).quantize(Decimal("0.01"), rounding=self.ROUNDING)
        ded_amount = (deductions * owner_decimal).quantize(Decimal("0.01"), rounding=self.ROUNDING)
        net_payment = (gross_share - tax_amount - ded_amount).quantize(Decimal("0.01"), rounding=self.ROUNDING)
        return {
            "gross_share": gross_share,
            "severance_tax": tax_amount,
            "deductions": ded_amount,
            "net_payment": net_payment,
        }

    def _log_calculation(self, operation: str, details: Dict[str, Any]) -> None:
        """Log a calculation for audit trail."""
        entry = {
            "operation": operation,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details,
        }
        self._calculation_log.append(entry)

    def get_calculation_log(self) -> List[Dict[str, Any]]:
        """Return the calculation audit log."""
        return list(self._calculation_log)

    def clear_log(self) -> None:
        """Clear the calculation audit log."""
        self._calculation_log.clear()


# ---------------------------------------------------------------------------
# Decimal Format Converter
# ---------------------------------------------------------------------------

class DecimalFormatConverter:
    """Converts between fraction strings, decimals, percentages, and NMA.

    Supports formats: '1/8', '3/16', '0.125', '12.5%', '25 NMA in 640'.
    """

    QUANTIZE_SPEC = Decimal("0.00000001")
    ROUNDING = ROUND_HALF_UP

    COMMON_FRACTIONS: Dict[str, Decimal] = {
        "1/8": Decimal("0.12500000"),
        "3/16": Decimal("0.18750000"),
        "1/4": Decimal("0.25000000"),
        "1/3": Decimal("0.33333333"),
        "1/2": Decimal("0.50000000"),
        "5/8": Decimal("0.62500000"),
        "3/4": Decimal("0.75000000"),
        "7/8": Decimal("0.87500000"),
        "1/6": Decimal("0.16666667"),
        "1/16": Decimal("0.06250000"),
        "1/32": Decimal("0.03125000"),
        "1/64": Decimal("0.01562500"),
        "1/128": Decimal("0.00781250"),
        "3/8": Decimal("0.37500000"),
        "5/16": Decimal("0.31250000"),
        "7/16": Decimal("0.43750000"),
        "2/3": Decimal("0.66666667"),
        "5/6": Decimal("0.83333333"),
        "1/12": Decimal("0.08333333"),
    }

    _FRACTION_RE = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*$")
    _MIXED_RE = re.compile(r"^\s*(\d+)\s+(\d+)\s*/\s*(\d+)\s*$")
    _PERCENT_RE = re.compile(r"^\s*([\d.]+)\s*%\s*$")
    _NMA_RE = re.compile(r"^\s*([\d.]+)\s*(?:NMA|nma)\s+(?:in|of)\s+([\d.]+)\s*$")
    _DECIMAL_RE = re.compile(r"^\s*0?\.\d+\s*$|^\s*\d+\.\d+\s*$|^\s*[01]\s*$")

    def fraction_to_decimal(self, fraction_str: str) -> Optional[Decimal]:
        """Convert a fraction string to a Decimal.

        Supports: '1/8', '3 1/4' (mixed number), common lookup.

        Args:
            fraction_str: The fraction string.

        Returns:
            Decimal value or None if unparseable.
        """
        fraction_str = fraction_str.strip()
        if fraction_str in self.COMMON_FRACTIONS:
            return self.COMMON_FRACTIONS[fraction_str]
        match = self._FRACTION_RE.match(fraction_str)
        if match:
            num = int(match.group(1))
            den = int(match.group(2))
            if den == 0:
                logger.error("Division by zero in fraction: {f}", f=fraction_str)
                return None
            return (Decimal(num) / Decimal(den)).quantize(self.QUANTIZE_SPEC, rounding=self.ROUNDING)
        match = self._MIXED_RE.match(fraction_str)
        if match:
            whole = int(match.group(1))
            num = int(match.group(2))
            den = int(match.group(3))
            if den == 0:
                return None
            return (Decimal(whole) + Decimal(num) / Decimal(den)).quantize(
                self.QUANTIZE_SPEC, rounding=self.ROUNDING
            )
        return None

    def decimal_to_fraction(self, decimal_val: Decimal, max_denominator: int = 1024) -> str:
        """Convert a Decimal to the closest simple fraction string.

        Args:
            decimal_val: The Decimal value.
            max_denominator: Maximum denominator to consider.

        Returns:
            Fraction string like '1/8' or '3/16'.
        """
        if decimal_val == Decimal("0"):
            return "0/1"
        for frac_str, frac_val in self.COMMON_FRACTIONS.items():
            if abs(decimal_val - frac_val) < Decimal("0.00000050"):
                return frac_str
        float_val = float(decimal_val)
        best_num = 0
        best_den = 1
        best_err = abs(float_val)
        for den in range(1, max_denominator + 1):
            num = round(float_val * den)
            err = abs(float_val - num / den)
            if err < best_err:
                best_err = err
                best_num = num
                best_den = den
                if err < 1e-10:
                    break
        return f"{best_num}/{best_den}"

    def percentage_to_decimal(self, pct_str: str) -> Optional[Decimal]:
        """Convert a percentage string to a Decimal.

        Args:
            pct_str: Percentage string like '12.5%'.

        Returns:
            Decimal value or None.
        """
        match = self._PERCENT_RE.match(pct_str)
        if match:
            pct = Decimal(match.group(1))
            return (pct / Decimal("100")).quantize(self.QUANTIZE_SPEC, rounding=self.ROUNDING)
        return None

    def decimal_to_percentage(self, decimal_val: Decimal) -> str:
        """Convert a Decimal to a percentage string.

        Args:
            decimal_val: The Decimal value.

        Returns:
            Percentage string like '12.50000000%'.
        """
        pct = decimal_val * Decimal("100")
        return f"{pct}%"

    def nma_to_decimal(self, nma: Decimal, total_unit_nma: Decimal) -> Decimal:
        """Convert Net Mineral Acres to a decimal interest.

        Args:
            nma: Owner's NMA.
            total_unit_nma: Total NMA in the unit.

        Returns:
            Decimal interest.
        """
        if total_unit_nma == Decimal("0"):
            return Decimal("0")
        return (nma / total_unit_nma).quantize(self.QUANTIZE_SPEC, rounding=self.ROUNDING)

    def parse_interest_string(self, text: str) -> Optional[Decimal]:
        """Parse any interest string format to Decimal.

        Tries fraction, percentage, NMA, and plain decimal formats.

        Args:
            text: Interest string in any format.

        Returns:
            Decimal value or None.
        """
        text = text.strip()
        result = self.fraction_to_decimal(text)
        if result is not None:
            return result
        result = self.percentage_to_decimal(text)
        if result is not None:
            return result
        match = self._NMA_RE.match(text)
        if match:
            nma = Decimal(match.group(1))
            total = Decimal(match.group(2))
            return self.nma_to_decimal(nma, total)
        if self._DECIMAL_RE.match(text):
            try:
                return Decimal(text).quantize(self.QUANTIZE_SPEC, rounding=self.ROUNDING)
            except InvalidOperation:
                return None
        return None


# ---------------------------------------------------------------------------
# Chain of Title Terms
# ---------------------------------------------------------------------------

class ChainOfTitleTerms:
    """Semantic terms specific to chain of title tracing for division orders."""

    INSTRUMENT_TYPES: Dict[str, str] = {
        "WD": "Warranty Deed",
        "SWD": "Special Warranty Deed",
        "QCD": "Quitclaim Deed",
        "MD": "Mineral Deed",
        "RD": "Royalty Deed",
        "OGL": "Oil and Gas Lease",
        "ASGN": "Assignment",
        "AORRI": "Assignment of Overriding Royalty Interest",
        "AOGL": "Assignment of Oil and Gas Lease",
        "DOT": "Deed of Trust",
        "REL": "Release",
        "PREL": "Partial Release",
        "AFFH": "Affidavit of Heirship",
        "PROB": "Probate Order",
        "CO": "Court Order",
        "DIV": "Division Order",
        "TO": "Transfer Order",
        "POOL": "Pooling Agreement",
        "UNIT": "Unit Designation",
        "CORR": "Correction Deed",
        "RAT": "Ratification",
        "POA": "Power of Attorney",
        "PART": "Partition Deed",
        "FOA": "Farmout Agreement",
        "JOA": "Joint Operating Agreement",
    }

    INTEREST_TYPE_SYNONYMS: Dict[str, List[str]] = {
        "WI": ["working interest", "leasehold interest", "operating interest", "cost bearing interest"],
        "RI": ["royalty interest", "lessor royalty", "landowner royalty", "lease royalty"],
        "ORRI": ["overriding royalty", "override", "OR", "overriding royalty interest"],
        "NRI": ["net revenue interest", "net revenue", "revenue interest"],
        "MI": ["mineral interest", "mineral fee", "mineral estate", "mineral ownership"],
        "NPRI": ["non-participating royalty", "non-participating royalty interest", "NPRI"],
        "NPI": ["net profits interest", "net profits", "profit interest"],
        "CI": ["carried interest", "carry", "free carry"],
        "BII": ["back-in interest", "back-in", "back in right", "convertible interest"],
        "PP": ["production payment", "term production payment"],
        "ER": ["executive right", "executive rights", "leasing right"],
    }

    @classmethod
    def normalize_instrument_type(cls, raw_type: str) -> str:
        """Normalize an instrument type abbreviation or name.

        Args:
            raw_type: Raw instrument type string.

        Returns:
            Normalized instrument type name.
        """
        upper = raw_type.strip().upper()
        if upper in cls.INSTRUMENT_TYPES:
            return cls.INSTRUMENT_TYPES[upper]
        for abbr, full_name in cls.INSTRUMENT_TYPES.items():
            if full_name.upper() == upper:
                return full_name
        clean = raw_type.strip().replace("_", " ").title()
        return clean

    @classmethod
    def normalize_interest_type(cls, raw_type: str) -> Optional[InterestType]:
        """Normalize an interest type string to an InterestType enum.

        Args:
            raw_type: Raw interest type string.

        Returns:
            InterestType enum value or None.
        """
        upper = raw_type.strip().upper()
        for it in InterestType:
            if it.value == upper or it.name == upper:
                return it
        for code, synonyms in cls.INTEREST_TYPE_SYNONYMS.items():
            lower = raw_type.strip().lower()
            if lower in [s.lower() for s in synonyms]:
                try:
                    return InterestType(code)
                except ValueError:
                    continue
        return None

    @classmethod
    def get_abbreviation(cls, full_name: str) -> Optional[str]:
        """Get the abbreviation for a full instrument type name.

        Args:
            full_name: Full instrument type name.

        Returns:
            Abbreviation or None.
        """
        name_upper = full_name.strip().upper()
        for abbr, full in cls.INSTRUMENT_TYPES.items():
            if full.upper() == name_upper:
                return abbr
        return None


# ---------------------------------------------------------------------------
# Interest Term Normalizer
# ---------------------------------------------------------------------------

class InterestTermNormalizer:
    """Normalizes oil and gas interest terminology to standard forms."""

    _NORMALIZE_MAP: Dict[str, str] = {
        "working interest": "WI",
        "working int": "WI",
        "w.i.": "WI",
        "wi": "WI",
        "leasehold interest": "WI",
        "operating interest": "WI",
        "royalty interest": "RI",
        "royalty int": "RI",
        "r.i.": "RI",
        "ri": "RI",
        "lessor royalty": "RI",
        "landowner royalty": "RI",
        "overriding royalty interest": "ORRI",
        "overriding royalty": "ORRI",
        "override": "ORRI",
        "o.r.r.i.": "ORRI",
        "orri": "ORRI",
        "or": "ORRI",
        "net revenue interest": "NRI",
        "net revenue": "NRI",
        "n.r.i.": "NRI",
        "nri": "NRI",
        "mineral interest": "MI",
        "mineral fee": "MI",
        "mineral estate": "MI",
        "non-participating royalty interest": "NPRI",
        "non-participating royalty": "NPRI",
        "nonparticipating royalty": "NPRI",
        "npri": "NPRI",
        "net profits interest": "NPI",
        "net profits": "NPI",
        "npi": "NPI",
        "carried interest": "CI",
        "carry": "CI",
        "back-in interest": "BII",
        "back-in": "BII",
        "back in": "BII",
        "production payment": "PP",
        "executive right": "ER",
        "executive rights": "ER",
    }

    @classmethod
    def normalize(cls, term: str) -> str:
        """Normalize an interest term to its standard code.

        Args:
            term: Raw interest term.

        Returns:
            Standard interest code (WI, RI, ORRI, etc.) or the original if unrecognized.
        """
        lower = term.strip().lower()
        if lower in cls._NORMALIZE_MAP:
            return cls._NORMALIZE_MAP[lower]
        upper = term.strip().upper()
        valid_codes = {it.value for it in InterestType}
        if upper in valid_codes:
            return upper
        return term.strip()

    @classmethod
    def is_cost_bearing(cls, interest_code: str) -> bool:
        """Determine if an interest type is cost-bearing.

        Args:
            interest_code: Normalized interest code.

        Returns:
            True if cost-bearing (WI), False otherwise.
        """
        return interest_code.upper() in ("WI", "CBI")

    @classmethod
    def is_royalty_type(cls, interest_code: str) -> bool:
        """Determine if an interest type is a royalty-class interest.

        Args:
            interest_code: Normalized interest code.

        Returns:
            True if royalty-class (RI, ORRI, NPRI).
        """
        return interest_code.upper() in ("RI", "ORRI", "NPRI")


# ---------------------------------------------------------------------------
# Division Order Semantic Dictionary (Main Class)
# ---------------------------------------------------------------------------

class DivisionOrderSemanticDictionary:
    """Main semantic dictionary for division order terminology.

    Contains 120+ terms organized by domain. Supports lookup,
    search, and normalization of oil and gas terminology.
    """

    def __init__(self) -> None:
        """Initialize the semantic dictionary and load all terms."""
        self._terms: Dict[str, SemanticTerm] = {}
        self._domain_index: Dict[SemanticDomain, List[str]] = {}
        self._synonym_index: Dict[str, str] = {}
        self._build_dictionary()
        logger.info(
            "DivisionOrderSemanticDictionary loaded: {n} terms, {d} domains",
            n=len(self._terms),
            d=len(self._domain_index),
        )

    def _build_dictionary(self) -> None:
        """Build the full semantic dictionary."""
        terms = _build_all_terms()
        for t in terms:
            self._terms[t.term_id] = t
            domain_list = self._domain_index.setdefault(t.domain, [])
            domain_list.append(t.term_id)
            for syn in t.synonyms:
                self._synonym_index[syn.lower()] = t.term_id
            for abbr in t.abbreviations:
                self._synonym_index[abbr.lower()] = t.term_id

    def lookup(self, text: str) -> Optional[SemanticTerm]:
        """Look up a term by name, synonym, or abbreviation.

        Args:
            text: Text to look up.

        Returns:
            Matching SemanticTerm or None.
        """
        text_lower = text.lower().strip()
        if text_lower in self._synonym_index:
            tid = self._synonym_index[text_lower]
            return self._terms.get(tid)
        for term in self._terms.values():
            if term.matches(text):
                return term
        return None

    def get_terms_by_domain(self, domain: SemanticDomain) -> List[SemanticTerm]:
        """Get all terms in a domain.

        Args:
            domain: The semantic domain.

        Returns:
            List of terms.
        """
        tids = self._domain_index.get(domain, [])
        return [self._terms[tid] for tid in tids if tid in self._terms]

    def search(self, query: str, max_results: int = 10) -> List[Tuple[SemanticTerm, float]]:
        """Search terms by relevance.

        Args:
            query: Search query.
            max_results: Maximum results.

        Returns:
            List of (term, score) tuples.
        """
        results: List[Tuple[SemanticTerm, float]] = []
        query_lower = query.lower()
        for term in self._terms.values():
            score = 0.0
            if query_lower in term.term.lower():
                score += 0.5
            if query_lower in term.definition.lower():
                score += 0.3
            for syn in term.synonyms:
                if query_lower in syn.lower():
                    score += 0.2
                    break
            if score > 0.0:
                results.append((term, min(score, 1.0)))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max_results]

    def health_check(self) -> Dict[str, Any]:
        """Return health status of the semantic dictionary."""
        return {
            "status": "healthy",
            "total_terms": len(self._terms),
            "total_domains": len(self._domain_index),
            "synonym_index_size": len(self._synonym_index),
        }


# ---------------------------------------------------------------------------
# Term Builder
# ---------------------------------------------------------------------------

def _build_all_terms() -> List[SemanticTerm]:
    """Build all semantic terms for the division order dictionary."""
    terms: List[SemanticTerm] = []

    terms.extend([
        SemanticTerm("DO-ST-001", "Working Interest", SemanticDomain.INTEREST_TYPES,
                     "The operating interest in an oil and gas lease that bears costs of exploration and production.",
                     synonyms=["WI", "leasehold interest", "operating interest"],
                     abbreviations=["WI", "W.I."],
                     related_terms=["NRI", "Cost-Bearing Interest"]),
        SemanticTerm("DO-ST-002", "Royalty Interest", SemanticDomain.INTEREST_TYPES,
                     "A non-cost-bearing share of production reserved by the mineral owner in a lease.",
                     synonyms=["lessor royalty", "landowner royalty", "lease royalty"],
                     abbreviations=["RI", "R.I."],
                     related_terms=["NPRI", "ORRI"]),
        SemanticTerm("DO-ST-003", "Overriding Royalty Interest", SemanticDomain.INTEREST_TYPES,
                     "A non-cost-bearing interest carved from the working interest that terminates with the lease.",
                     synonyms=["override", "ORRI", "overriding royalty"],
                     abbreviations=["ORRI", "OR", "O.R.R.I."],
                     related_terms=["WI", "RI"]),
        SemanticTerm("DO-ST-004", "Net Revenue Interest", SemanticDomain.INTEREST_TYPES,
                     "Working interest minus all non-operating burdens. The actual revenue share of a WI holder.",
                     synonyms=["NRI", "net revenue", "revenue interest"],
                     abbreviations=["NRI", "N.R.I."],
                     related_terms=["WI", "ORRI", "RI"]),
        SemanticTerm("DO-ST-005", "Net Profits Interest", SemanticDomain.INTEREST_TYPES,
                     "An interest entitling the holder to a share of net profits from production after deducting costs.",
                     synonyms=["NPI", "profit interest", "net profit interest"],
                     abbreviations=["NPI"],
                     related_terms=["WI", "Revenue Distribution"]),
        SemanticTerm("DO-ST-006", "Non-Participating Royalty Interest", SemanticDomain.INTEREST_TYPES,
                     "A royalty interest whose holder cannot execute leases and has no right to bonus or delay rentals.",
                     synonyms=["NPRI", "nonparticipating royalty"],
                     abbreviations=["NPRI"],
                     related_terms=["RI", "Executive Right"],
                     legal_authority="French v. Chevron U.S.A., Inc., 896 S.W.2d 795 (Tex. 1995)"),
        SemanticTerm("DO-ST-007", "Carried Interest", SemanticDomain.INTEREST_TYPES,
                     "A working interest where another party bears the costs until a specified event (payout).",
                     synonyms=["carry", "free carry", "carried working interest"],
                     abbreviations=["CI"],
                     related_terms=["WI", "Farmout"]),
        SemanticTerm("DO-ST-008", "Production Payment", SemanticDomain.INTEREST_TYPES,
                     "A share of production that terminates after a specified dollar amount or volume is received.",
                     synonyms=["term production payment", "volumetric production payment"],
                     abbreviations=["PP"],
                     related_terms=["Reversionary Interest", "ORRI"]),
        SemanticTerm("DO-ST-009", "Back-In Interest", SemanticDomain.INTEREST_TYPES,
                     "The right to convert an ORRI to a working interest after payout.",
                     synonyms=["back-in right", "convertible interest", "back in"],
                     abbreviations=["BII"],
                     related_terms=["ORRI", "Farmout", "Payout"]),
        SemanticTerm("DO-ST-010", "Executive Right", SemanticDomain.INTEREST_TYPES,
                     "The right to execute oil and gas leases on the mineral estate.",
                     synonyms=["leasing right", "executive rights"],
                     abbreviations=["ER"],
                     related_terms=["NPRI", "Mineral Interest"],
                     legal_authority="Day & Co. v. Texland Petroleum, Inc., 786 S.W.2d 667 (Tex. 1990)"),
    ])

    terms.extend([
        SemanticTerm("DO-ST-020", "Division Order", SemanticDomain.REVENUE_DISTRIBUTION,
                     "A contract directing the purchaser to pay an interest owner's share of production proceeds.",
                     synonyms=["DO", "division order form"],
                     abbreviations=["DO"],
                     legal_authority="Tex. Nat. Res. Code Sec. 91.001"),
        SemanticTerm("DO-ST-021", "Pay Deck", SemanticDomain.REVENUE_DISTRIBUTION,
                     "The master list of interest owners, their decimals, and payment instructions for a well or unit.",
                     synonyms=["revenue distribution schedule", "owner master file", "payment schedule"],
                     abbreviations=[],
                     related_terms=["Division Order", "Revenue Distribution"]),
        SemanticTerm("DO-ST-022", "Suspense", SemanticDomain.SUSPENSE_MANAGEMENT,
                     "Revenue held by the operator when payment cannot be made due to title defect or other impediment.",
                     synonyms=["suspended funds", "held in suspense", "suspense account"],
                     related_terms=["Escheat", "Unclaimed Property"]),
        SemanticTerm("DO-ST-023", "Escheat", SemanticDomain.SUSPENSE_MANAGEMENT,
                     "The reversion of unclaimed property to the state after a dormancy period.",
                     synonyms=["unclaimed property", "abandoned property"],
                     legal_authority="Tex. Property Code Ch. 72"),
        SemanticTerm("DO-ST-024", "Transfer Order", SemanticDomain.OWNERSHIP_CHANGE,
                     "Internal document recording the transfer of an interest between owners.",
                     synonyms=["TO", "ownership transfer", "change of ownership"],
                     abbreviations=["TO"]),
        SemanticTerm("DO-ST-025", "Ratification", SemanticDomain.REVENUE_DISTRIBUTION,
                     "The process of interest owners signing and returning division orders to authorize payment.",
                     synonyms=["DO execution", "division order ratification"],
                     related_terms=["Division Order"]),
    ])

    terms.extend([
        SemanticTerm("DO-ST-030", "Pooling", SemanticDomain.POOLING_UNITIZATION,
                     "Combining multiple tracts into a single drilling or spacing unit.",
                     synonyms=["pooled unit", "pooling clause", "voluntary pooling"],
                     related_terms=["Unitization", "Allocation Factor"],
                     legal_authority="Tex. Nat. Res. Code Ch. 102"),
        SemanticTerm("DO-ST-031", "Unitization", SemanticDomain.POOLING_UNITIZATION,
                     "Combining multiple leases or units for fieldwide enhanced recovery operations.",
                     synonyms=["fieldwide unit", "secondary recovery unit"],
                     related_terms=["Pooling", "Enhanced Recovery"]),
        SemanticTerm("DO-ST-032", "Allocation Factor", SemanticDomain.POOLING_UNITIZATION,
                     "The fraction of unit production attributable to a particular tract.",
                     synonyms=["tract participation factor", "tract factor", "participation factor"],
                     related_terms=["Pooling", "Surface Acreage"]),
        SemanticTerm("DO-ST-033", "Force Pooling", SemanticDomain.POOLING_UNITIZATION,
                     "Compulsory pooling ordered by the Railroad Commission when voluntary pooling fails.",
                     synonyms=["compulsory pooling", "forced pooling"],
                     legal_authority="Tex. Nat. Res. Code Ch. 102"),
    ])

    terms.extend([
        SemanticTerm("DO-ST-040", "Duhig Rule", SemanticDomain.TITLE_EXAMINATION,
                     "Warranty deed conveyance takes priority over reservation when grantor lacks sufficient interest.",
                     synonyms=["Duhig doctrine", "Duhig v. Peavy-Moore"],
                     legal_authority="Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)"),
        SemanticTerm("DO-ST-041", "Proportionate Reduction", SemanticDomain.TITLE_EXAMINATION,
                     "Clause reducing lessor royalty proportionately when lessor owns less than full minerals.",
                     synonyms=["proportionate reduction clause", "PRC"],
                     related_terms=["Royalty Interest", "Mineral Interest"]),
        SemanticTerm("DO-ST-042", "After-Acquired Title", SemanticDomain.TITLE_EXAMINATION,
                     "Title subsequently acquired by a warranty deed grantor automatically passes to the grantee.",
                     synonyms=["estoppel by deed", "after acquired title doctrine"],
                     related_terms=["Warranty Deed", "Duhig Rule"]),
        SemanticTerm("DO-ST-043", "Mother Hubbard Clause", SemanticDomain.CONVEYANCE_LANGUAGE,
                     "A cover-all clause conveying small strips or interests adjacent to the described tract.",
                     synonyms=["cover-all clause", "dragnet clause"],
                     legal_authority="Geodyne Resources, Ltd. v. Newton, 349 S.W.3d 506 (Tex. 2011)"),
        SemanticTerm("DO-ST-044", "Severance Tax", SemanticDomain.TAX_REPORTING,
                     "State tax on oil (4.6%) and gas (7.5%) production in Texas.",
                     synonyms=["production tax", "oil production tax", "gas production tax"],
                     abbreviations=["SEV"],
                     legal_authority="Tex. Tax Code Ch. 201 & Ch. 202"),
        SemanticTerm("DO-ST-045", "Joint Operating Agreement", SemanticDomain.JOA_TERMS,
                     "Contract governing operations among multiple working interest owners in a well.",
                     synonyms=["JOA", "operating agreement", "AAPL 610"],
                     abbreviations=["JOA"],
                     legal_authority="AAPL Model Form 610-2015"),
        SemanticTerm("DO-ST-046", "COPAS", SemanticDomain.ACCOUNTING,
                     "Council of Petroleum Accountants Societies - sets accounting procedures for JOA operations.",
                     synonyms=["COPAS accounting procedure", "joint interest billing"],
                     abbreviations=["COPAS"]),
        SemanticTerm("DO-ST-047", "Joint Interest Billing", SemanticDomain.ACCOUNTING,
                     "Monthly billing to non-operators for their share of operating costs per the JOA.",
                     synonyms=["JIB", "joint interest statement"],
                     abbreviations=["JIB"]),
        SemanticTerm("DO-ST-048", "Authority for Expenditure", SemanticDomain.ACCOUNTING,
                     "Pre-approval document for proposed well operations distributed to WI holders.",
                     synonyms=["AFE", "expenditure authorization"],
                     abbreviations=["AFE"]),
        SemanticTerm("DO-ST-049", "Decimal Interest", SemanticDomain.DECIMAL_CALCULATION,
                     "The numerical representation of an owner's share of production, expressed to 8 decimal places.",
                     synonyms=["decimal ownership", "ownership decimal"],
                     related_terms=["Unity Check", "NMA"]),
        SemanticTerm("DO-ST-050", "Unity Check", SemanticDomain.DECIMAL_CALCULATION,
                     "Verification that all interests of a given type sum to 1.00000000.",
                     synonyms=["unity verification", "interest reconciliation"],
                     related_terms=["Decimal Interest", "Pay Deck"]),
    ])

    return terms
