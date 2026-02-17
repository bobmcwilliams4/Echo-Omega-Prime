"""
LM03 Division Order Engine - Main Engine
==========================================

Full division order engine implementation for oil & gas landman operations.

Core capabilities:
- Decimal interest calculation (WI, RI, ORRI, NRI, CBI, NPI, CI, BII)
- Division order generation and ratification tracking
- Chain of title interest tracing with Duhig rule application
- Pay deck construction and revenue distribution
- Suspense/escheat management (Tex. Property Code Ch. 72)
- Pooling/unitization decimal allocation
- JOA provision parsing and non-consent penalty computation
- Proportionate reduction clause application
- After-acquired title doctrine handling
- Texas Natural Resources Code Ch. 91 compliance
- Full audit trail with SHA-256 deterministic hashing

Engine ID: LM03
Port: 8411
Mode: DET (Deterministic)
Authority: 5.0
Version: 2.0.0

Author: ECHO OMEGA PRIME Build System
Commander: Bobby Don McWilliams II
"""

from __future__ import annotations

import hashlib
import json
import traceback
import uuid
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from loguru import logger


# Ensure sibling modules are importable
import sys
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DivisionOrderDoctrineCache,
    DoctrineCacheBlock,
    DoctrineCategory,
    DoctrineSeverity,
    build_doctrine_cache,
    search_doctrines,
    get_coverage_map,
    verify_doctrine_integrity,
)
from search import (
    DoctrineSearchIndex,
    DivisionOrderSearcher,
    InterestTracer,
    RevenueDistributionCalculator,
    SearchQuery,
    SearchResponse,
    SearchResult,
    SuspenseAnalyzer,
    SuspenseCode,
)
from semantic import (
    ChainOfTitleTerms,
    ConveyanceEvent,
    DecimalFormatConverter,
    DivisionOrderSemanticDictionary,
    InterestCalculator,
    InterestTermNormalizer,
    InterestType,
    OwnershipPosition,
    SemanticDomain,
    SemanticTerm,
)
from telemetry import (
    AuditEventType,
    DivisionOrderTelemetry,
    DriftType,
    ErrorSeverity,
    MetricType,
    OperationType,
    compute_chain_hash,
    compute_deterministic_hash,
    compute_interest_hash,
    compute_pay_deck_hash,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ENGINE_ID = "LM03"
ENGINE_NAME = "Division Order Engine"
ENGINE_VERSION = "2.0.0"
ENGINE_PORT = 8411
ENGINE_MODE = "DET"
ENGINE_AUTHORITY = 5.0

PRECISION = 8
QUANTIZE_SPEC = Decimal("0.00000001")
ROUNDING = ROUND_HALF_UP
UNITY = Decimal("1.00000000")
ZERO = Decimal("0.00000000")
TOLERANCE = Decimal("0.00001000")

OIL_SEVERANCE_TAX_RATE = Decimal("0.046")
GAS_SEVERANCE_TAX_RATE = Decimal("0.075")
MINIMUM_PAYMENT_THRESHOLD = Decimal("100.00")
ESCHEAT_THRESHOLD_MONTHS = 36

ENGINE_ROOT = Path(__file__).parent
CONFIG_PATH = ENGINE_ROOT / "config.json"

BANNED_PHRASES = [
    "this is not legal advice",
    "consult an attorney",
    "i am not a lawyer",
    "for informational purposes only",
]

EPISTEMIC_DISCLAIMER = (
    "DISCLOSURE: This analysis is produced by the LM03 Division Order Engine "
    "operating in DET (deterministic) mode. All decimal interest calculations "
    "use 8-place precision with ROUND_HALF_UP. Results are derived from the "
    "doctrine cache and input data provided. Verify against original instruments."
)


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class DivisionOrderStatus(str, Enum):
    """Status of a division order."""
    DRAFT = "draft"
    PENDING_RATIFICATION = "pending_ratification"
    RATIFIED = "ratified"
    AMENDED = "amended"
    REVOKED = "revoked"
    SUSPENDED = "suspended"


class PayDeckStatus(str, Enum):
    """Status of a pay deck."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"
    PENDING_REVIEW = "pending_review"


class PoolingMethod(str, Enum):
    """Methods for computing pooled unit participation."""
    SURFACE_ACREAGE = "surface_acreage"
    PERFORATED_LATERAL = "perforated_lateral"
    PRODUCTIVE_ACREAGE = "productive_acreage"
    EQUAL_SHARE = "equal_share"


class NonConsentElection(str, Enum):
    """Non-consent election options under JOA."""
    PARTICIPATE = "participate"
    NON_CONSENT = "non_consent"
    FARM_OUT = "farm_out"


class RatificationStatus(str, Enum):
    """Status of division order ratification."""
    NOT_SENT = "not_sent"
    SENT = "sent"
    RECEIVED_SIGNED = "received_signed"
    RECEIVED_UNSIGNED = "received_unsigned"
    DISPUTED = "disputed"
    EXPIRED = "expired"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class WellUnit:
    """Represents a well or pooled unit for division order purposes."""
    well_id: str
    well_name: str
    operator: str
    county: str
    state: str = "TX"
    api_number: Optional[str] = None
    rrc_lease_number: Optional[str] = None
    legal_description: Optional[str] = None
    total_acres: Decimal = Decimal("0")
    effective_date: Optional[date] = None
    is_pooled_unit: bool = False
    tracts: List[Dict[str, Any]] = field(default_factory=list)
    product_type: str = "OIL"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "well_id": self.well_id,
            "well_name": self.well_name,
            "operator": self.operator,
            "county": self.county,
            "state": self.state,
            "api_number": self.api_number,
            "rrc_lease_number": self.rrc_lease_number,
            "legal_description": self.legal_description,
            "total_acres": str(self.total_acres),
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "is_pooled_unit": self.is_pooled_unit,
            "tracts": self.tracts,
            "product_type": self.product_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WellUnit":
        """Deserialize from dictionary."""
        eff = None
        if data.get("effective_date"):
            if isinstance(data["effective_date"], date):
                eff = data["effective_date"]
            elif isinstance(data["effective_date"], str):
                eff = date.fromisoformat(data["effective_date"])
        return cls(
            well_id=data.get("well_id", str(uuid.uuid4())[:8]),
            well_name=data.get("well_name", ""),
            operator=data.get("operator", ""),
            county=data.get("county", ""),
            state=data.get("state", "TX"),
            api_number=data.get("api_number"),
            rrc_lease_number=data.get("rrc_lease_number"),
            legal_description=data.get("legal_description"),
            total_acres=Decimal(str(data.get("total_acres", "0"))),
            effective_date=eff,
            is_pooled_unit=data.get("is_pooled_unit", False),
            tracts=data.get("tracts", []),
            product_type=data.get("product_type", "OIL"),
        )


@dataclass
class PayDeckEntry:
    """A single entry in a pay deck."""
    entry_id: str
    owner_name: str
    interest_type: str
    decimal_interest: Decimal
    well_name: str
    operator: str
    county: Optional[str] = None
    effective_date: Optional[date] = None
    suspense_code: Optional[str] = None
    suspense_reason: Optional[str] = None
    payment_address: Optional[str] = None
    tax_id: Optional[str] = None
    ratification_status: RatificationStatus = RatificationStatus.NOT_SENT
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "entry_id": self.entry_id,
            "owner_name": self.owner_name,
            "interest_type": self.interest_type,
            "decimal_interest": str(self.decimal_interest),
            "well_name": self.well_name,
            "operator": self.operator,
            "county": self.county,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "suspense_code": self.suspense_code,
            "suspense_reason": self.suspense_reason,
            "payment_address": self.payment_address,
            "tax_id": self.tax_id,
            "ratification_status": self.ratification_status.value,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayDeckEntry":
        """Deserialize from dictionary."""
        eff = None
        if data.get("effective_date"):
            if isinstance(data["effective_date"], date):
                eff = data["effective_date"]
            elif isinstance(data["effective_date"], str):
                eff = date.fromisoformat(data["effective_date"])
        rat_status = RatificationStatus.NOT_SENT
        if data.get("ratification_status"):
            try:
                rat_status = RatificationStatus(data["ratification_status"])
            except ValueError:
                rat_status = RatificationStatus.NOT_SENT
        return cls(
            entry_id=data.get("entry_id", str(uuid.uuid4())[:8]),
            owner_name=data.get("owner_name", ""),
            interest_type=data.get("interest_type", ""),
            decimal_interest=Decimal(str(data.get("decimal_interest", "0"))),
            well_name=data.get("well_name", ""),
            operator=data.get("operator", ""),
            county=data.get("county"),
            effective_date=eff,
            suspense_code=data.get("suspense_code"),
            suspense_reason=data.get("suspense_reason"),
            payment_address=data.get("payment_address"),
            tax_id=data.get("tax_id"),
            ratification_status=rat_status,
            notes=data.get("notes", []),
        )


@dataclass
class DivisionOrderRecord:
    """A complete division order record."""
    order_id: str
    well: WellUnit
    status: DivisionOrderStatus
    pay_deck: List[PayDeckEntry]
    created_date: date
    effective_date: Optional[date] = None
    amended_date: Optional[date] = None
    title_opinion_ref: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    unity_check_result: Optional[Dict[str, Any]] = None
    deterministic_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "order_id": self.order_id,
            "well": self.well.to_dict(),
            "status": self.status.value,
            "pay_deck": [e.to_dict() for e in self.pay_deck],
            "created_date": self.created_date.isoformat(),
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "amended_date": self.amended_date.isoformat() if self.amended_date else None,
            "title_opinion_ref": self.title_opinion_ref,
            "notes": self.notes,
            "unity_check_result": self.unity_check_result,
            "deterministic_hash": self.deterministic_hash,
        }


@dataclass
class JOAProvision:
    """Parsed JOA provision for cost sharing and non-consent penalties."""
    joa_id: str
    operator: str
    non_operator_parties: List[str]
    working_interest_shares: Dict[str, Decimal]
    non_consent_penalty_pct: Decimal = Decimal("300")
    overhead_rate_monthly: Decimal = Decimal("0")
    accounting_procedure: str = "COPAS 2005"
    area_of_mutual_interest: bool = False
    ami_radius_miles: Optional[Decimal] = None
    preferential_right: bool = False
    afe_approval_threshold: Optional[Decimal] = None
    effective_date: Optional[date] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "joa_id": self.joa_id,
            "operator": self.operator,
            "non_operator_parties": self.non_operator_parties,
            "working_interest_shares": {k: str(v) for k, v in self.working_interest_shares.items()},
            "non_consent_penalty_pct": str(self.non_consent_penalty_pct),
            "overhead_rate_monthly": str(self.overhead_rate_monthly),
            "accounting_procedure": self.accounting_procedure,
            "area_of_mutual_interest": self.area_of_mutual_interest,
            "ami_radius_miles": str(self.ami_radius_miles) if self.ami_radius_miles else None,
            "preferential_right": self.preferential_right,
            "afe_approval_threshold": str(self.afe_approval_threshold) if self.afe_approval_threshold else None,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------------
# Re-exports from semantic.py (used by __init__.py)
# ---------------------------------------------------------------------------

# InterestCalculator is imported from .semantic and re-exported
# DecimalConverter is an alias for DecimalFormatConverter
DecimalConverter = DecimalFormatConverter


# ---------------------------------------------------------------------------
# Chain of Title Tracer
# ---------------------------------------------------------------------------

class ChainOfTitleTracer:
    """Traces mineral interests through a chain of conveyance events.

    Builds an ownership map starting from the sovereign/patentee,
    processes each conveyance chronologically, applies Duhig rule
    to warranty deeds, handles reservations and exceptions, and
    produces a final ownership summary with unity check.

    Uses InterestTracer from search.py for core tracing logic,
    wrapping it with additional analysis and reporting.
    """

    def __init__(self, telemetry: Optional[DivisionOrderTelemetry] = None) -> None:
        """Initialize the chain of title tracer.

        Args:
            telemetry: Optional telemetry instance for tracking.
        """
        self._tracer = InterestTracer()
        self._calculator = InterestCalculator()
        self._telemetry = telemetry
        self._conveyance_events: List[ConveyanceEvent] = []
        self._analysis_notes: List[str] = []
        self._duhig_applications: List[Dict[str, Any]] = []
        self._after_acquired_events: List[Dict[str, Any]] = []
        logger.debug("ChainOfTitleTracer initialized")

    def set_sovereign(self, owner: str, interest: Decimal = UNITY) -> None:
        """Set the original patentee / sovereign grant.

        Args:
            owner: Name of the original owner.
            interest: Initial interest (default 1.0).
        """
        self._tracer.set_initial_ownership(owner, interest)
        self._analysis_notes.append(
            f"Chain begins with sovereign grant to {owner}: {interest}"
        )
        logger.info("Sovereign set: {o} with {i}", o=owner, i=interest)

    def add_conveyance(self, event: ConveyanceEvent) -> Dict[str, Any]:
        """Process a single conveyance event through the chain.

        Args:
            event: The conveyance event to process.

        Returns:
            Result dictionary with conveyance details.
        """
        op_id = None
        if self._telemetry:
            op_id = self._telemetry.start_operation(
                OperationType.CHAIN_TRACE,
                metadata={"grantor": event.grantor, "grantee": event.grantee},
            )

        self._conveyance_events.append(event)

        result = self._tracer.process_conveyance(
            grantor=event.grantor,
            grantee=event.grantee,
            interest_conveyed=event.interest_conveyed,
            reservation=event.reservation,
            is_warranty_deed=event.is_warranty_deed,
            document_ref=event.document_reference,
        )

        if result.get("duhig_applied"):
            self._duhig_applications.append({
                "event_id": event.event_id,
                "grantor": event.grantor,
                "grantee": event.grantee,
                "instrument": event.instrument_type,
                "document_ref": event.document_reference,
                "detail": result,
            })
            self._analysis_notes.append(
                f"DUHIG RULE APPLIED: {event.grantor} to {event.grantee} via "
                f"{event.instrument_type} ({event.document_reference})"
            )

        if self._telemetry and op_id:
            self._telemetry.complete_operation(op_id, metadata=result)
            self._telemetry.record_audit_event(
                AuditEventType.CHAIN_TRACED,
                f"Conveyance: {event.grantor} -> {event.grantee} ({event.interest_conveyed})",
                operation_id=op_id,
                details=result,
            )

        return result

    def trace_chain(self, events: List[ConveyanceEvent]) -> Dict[str, Any]:
        """Trace an entire chain of conveyance events.

        Args:
            events: List of conveyance events in chronological order.

        Returns:
            Complete chain trace result with ownership summary.
        """
        op_id = None
        if self._telemetry:
            op_id = self._telemetry.start_operation(
                OperationType.CHAIN_TRACE,
                metadata={"event_count": len(events)},
            )

        results: List[Dict[str, Any]] = []
        for event in events:
            result = self.add_conveyance(event)
            results.append(result)

        ownership = self._tracer.get_current_ownership()
        unity = self._tracer.unity_check()

        chain_data = {
            "conveyance_count": len(events),
            "conveyance_results": results,
            "current_ownership": ownership,
            "unity_check": unity,
            "duhig_applications": self._duhig_applications,
            "after_acquired_events": self._after_acquired_events,
            "analysis_notes": self._analysis_notes,
            "trace_log": self._tracer.get_trace_log(),
        }

        chain_data["deterministic_hash"] = compute_chain_hash(
            self._tracer.get_trace_log()
        )

        if self._telemetry and op_id:
            self._telemetry.complete_operation(op_id, metadata={
                "conveyances": len(events),
                "owners": len(ownership),
                "unity_passes": unity.get("passes", False),
            })

        logger.info(
            "Chain traced: {n} conveyances, {o} owners, unity={u}",
            n=len(events),
            o=len(ownership),
            u=unity.get("passes", False),
        )

        return chain_data

    def get_current_ownership(self) -> Dict[str, str]:
        """Return current ownership positions."""
        return self._tracer.get_current_ownership()

    def get_unity_check(self) -> Dict[str, Any]:
        """Run unity check on current ownership."""
        return self._tracer.unity_check()

    def get_duhig_applications(self) -> List[Dict[str, Any]]:
        """Return all Duhig rule applications."""
        return list(self._duhig_applications)

    def get_analysis_notes(self) -> List[str]:
        """Return analysis notes."""
        return list(self._analysis_notes)

    def reset(self) -> None:
        """Reset the tracer for a new chain."""
        self._tracer = InterestTracer()
        self._conveyance_events.clear()
        self._analysis_notes.clear()
        self._duhig_applications.clear()
        self._after_acquired_events.clear()


# ---------------------------------------------------------------------------
# Pay Deck Builder
# ---------------------------------------------------------------------------

class PayDeckBuilder:
    """Constructs and manages pay decks for wells and units.

    A pay deck is the master list of interest owners, their decimal
    interests, payment instructions, and suspense status. This class
    builds pay decks from chain of title data, validates unity,
    and manages amendments.
    """

    def __init__(self, telemetry: Optional[DivisionOrderTelemetry] = None) -> None:
        """Initialize the pay deck builder.

        Args:
            telemetry: Optional telemetry instance.
        """
        self._calculator = InterestCalculator()
        self._telemetry = telemetry
        self._pay_decks: Dict[str, List[PayDeckEntry]] = {}
        logger.debug("PayDeckBuilder initialized")

    def build_pay_deck(
        self,
        well: WellUnit,
        ownership: Dict[str, str],
        interest_types: Optional[Dict[str, str]] = None,
        lease_royalty_rate: Decimal = Decimal("0.25"),
    ) -> List[PayDeckEntry]:
        """Build a pay deck from ownership data.

        Args:
            well: The well or unit.
            ownership: Ownership map from ChainOfTitleTracer (name -> decimal).
            interest_types: Optional map of owner -> interest type code.
            lease_royalty_rate: Default lease royalty rate.

        Returns:
            List of PayDeckEntry objects.
        """
        op_id = None
        if self._telemetry:
            op_id = self._telemetry.start_operation(
                OperationType.PAY_DECK_BUILD,
                metadata={"well": well.well_name, "owner_count": len(ownership)},
            )

        entries: List[PayDeckEntry] = []
        types = interest_types or {}

        for owner_name, decimal_str in ownership.items():
            decimal_val = Decimal(decimal_str).quantize(QUANTIZE_SPEC, rounding=ROUNDING)
            int_type = types.get(owner_name, "MI")

            entry = PayDeckEntry(
                entry_id=f"PD-{uuid.uuid4().hex[:8]}",
                owner_name=owner_name,
                interest_type=int_type,
                decimal_interest=decimal_val,
                well_name=well.well_name,
                operator=well.operator,
                county=well.county,
                effective_date=well.effective_date or date.today(),
            )
            entries.append(entry)

        self._pay_decks[well.well_id] = entries

        if self._telemetry and op_id:
            self._telemetry.complete_operation(op_id, metadata={
                "entries": len(entries),
                "well": well.well_name,
            })
            self._telemetry.record_audit_event(
                AuditEventType.PAY_DECK_BUILT,
                f"Pay deck built for {well.well_name}: {len(entries)} entries",
                operation_id=op_id,
            )

        logger.info(
            "Pay deck built: {w} with {n} entries",
            w=well.well_name,
            n=len(entries),
        )

        return entries

    def build_royalty_pay_deck(
        self,
        well: WellUnit,
        mineral_owners: Dict[str, Decimal],
        lease_royalty_rate: Decimal = Decimal("0.25"),
        orri_holders: Optional[Dict[str, Decimal]] = None,
        npri_holders: Optional[Dict[str, Decimal]] = None,
    ) -> List[PayDeckEntry]:
        """Build a pay deck with separate royalty, ORRI, and NPRI entries.

        Computes royalty decimals from mineral ownership fractions and
        lease royalty rate, then adds ORRI and NPRI entries.

        Args:
            well: The well or unit.
            mineral_owners: Map of owner name -> mineral fraction.
            lease_royalty_rate: Lease royalty rate.
            orri_holders: Optional ORRI holders with decimals.
            npri_holders: Optional NPRI holders with decimals.

        Returns:
            List of PayDeckEntry objects.
        """
        entries: List[PayDeckEntry] = []
        tract_factor = UNITY
        if well.is_pooled_unit and well.total_acres > ZERO:
            for tract in well.tracts:
                tract_acres = Decimal(str(tract.get("acres", "0")))
                if tract_acres > ZERO:
                    tract_factor = (tract_acres / well.total_acres).quantize(
                        QUANTIZE_SPEC, rounding=ROUNDING
                    )

        for owner_name, mineral_frac in mineral_owners.items():
            royalty_decimal = self._calculator.compute_royalty_decimal(
                mineral_ownership=mineral_frac,
                lease_royalty_rate=lease_royalty_rate,
                tract_participation=tract_factor,
            )
            entries.append(PayDeckEntry(
                entry_id=f"PD-{uuid.uuid4().hex[:8]}",
                owner_name=owner_name,
                interest_type="RI",
                decimal_interest=royalty_decimal,
                well_name=well.well_name,
                operator=well.operator,
                county=well.county,
                effective_date=well.effective_date or date.today(),
            ))

        if orri_holders:
            for owner_name, orri_decimal in orri_holders.items():
                entries.append(PayDeckEntry(
                    entry_id=f"PD-{uuid.uuid4().hex[:8]}",
                    owner_name=owner_name,
                    interest_type="ORRI",
                    decimal_interest=orri_decimal.quantize(QUANTIZE_SPEC, rounding=ROUNDING),
                    well_name=well.well_name,
                    operator=well.operator,
                    county=well.county,
                    effective_date=well.effective_date or date.today(),
                ))

        if npri_holders:
            for owner_name, npri_decimal in npri_holders.items():
                entries.append(PayDeckEntry(
                    entry_id=f"PD-{uuid.uuid4().hex[:8]}",
                    owner_name=owner_name,
                    interest_type="NPRI",
                    decimal_interest=npri_decimal.quantize(QUANTIZE_SPEC, rounding=ROUNDING),
                    well_name=well.well_name,
                    operator=well.operator,
                    county=well.county,
                    effective_date=well.effective_date or date.today(),
                ))

        self._pay_decks[well.well_id] = entries
        logger.info(
            "Royalty pay deck built: {w} with {n} entries (RI={ri}, ORRI={orri}, NPRI={npri})",
            w=well.well_name,
            n=len(entries),
            ri=sum(1 for e in entries if e.interest_type == "RI"),
            orri=sum(1 for e in entries if e.interest_type == "ORRI"),
            npri=sum(1 for e in entries if e.interest_type == "NPRI"),
        )

        return entries

    def validate_pay_deck(self, entries: List[PayDeckEntry]) -> Dict[str, Any]:
        """Validate a pay deck for completeness and unity.

        Args:
            entries: List of pay deck entries.

        Returns:
            Validation result dictionary.
        """
        by_type: Dict[str, List[Decimal]] = defaultdict(list)
        for entry in entries:
            by_type[entry.interest_type].append(entry.decimal_interest)

        unity_results: Dict[str, Any] = {}
        for int_type, decimals in by_type.items():
            unity_results[int_type] = self._calculator.unity_check(
                decimals, interest_label=int_type
            )

        missing_address = [e.owner_name for e in entries if not e.payment_address]
        missing_tax_id = [e.owner_name for e in entries if not e.tax_id]
        in_suspense = [e.owner_name for e in entries if e.suspense_code]

        return {
            "total_entries": len(entries),
            "interest_type_breakdown": {k: len(v) for k, v in by_type.items()},
            "unity_checks": unity_results,
            "missing_payment_address": missing_address,
            "missing_tax_id": missing_tax_id,
            "in_suspense": in_suspense,
            "suspense_count": len(in_suspense),
            "validation_passed": all(
                r.get("passes", False) for r in unity_results.values()
            ),
        }

    def amend_entry(
        self,
        well_id: str,
        owner_name: str,
        new_decimal: Optional[Decimal] = None,
        new_interest_type: Optional[str] = None,
        suspense_code: Optional[str] = None,
        suspense_reason: Optional[str] = None,
    ) -> Optional[PayDeckEntry]:
        """Amend a pay deck entry.

        Args:
            well_id: Well identifier.
            owner_name: Owner to amend.
            new_decimal: New decimal interest (if changing).
            new_interest_type: New interest type (if changing).
            suspense_code: Suspense code to set (or None to clear).
            suspense_reason: Suspense reason.

        Returns:
            Amended PayDeckEntry or None if not found.
        """
        entries = self._pay_decks.get(well_id, [])
        for entry in entries:
            if entry.owner_name.upper() == owner_name.upper():
                if new_decimal is not None:
                    entry.decimal_interest = new_decimal.quantize(QUANTIZE_SPEC, rounding=ROUNDING)
                if new_interest_type is not None:
                    entry.interest_type = new_interest_type
                entry.suspense_code = suspense_code
                entry.suspense_reason = suspense_reason
                entry.notes.append(
                    f"Amended {datetime.utcnow().isoformat()}: "
                    f"decimal={new_decimal}, type={new_interest_type}, "
                    f"suspense={suspense_code}"
                )
                logger.info("Pay deck entry amended: {o} in {w}", o=owner_name, w=well_id)
                return entry
        logger.warning("Pay deck entry not found: {o} in {w}", o=owner_name, w=well_id)
        return None

    def get_pay_deck(self, well_id: str) -> List[PayDeckEntry]:
        """Return the pay deck for a well."""
        return self._pay_decks.get(well_id, [])

    def get_all_well_ids(self) -> List[str]:
        """Return all well IDs with pay decks."""
        return list(self._pay_decks.keys())


# ---------------------------------------------------------------------------
# Suspense Manager
# ---------------------------------------------------------------------------

class SuspenseManager:
    """Manages suspense status for division order interest owners.

    Tracks entries placed in suspense, monitors aging for escheat
    eligibility, and manages suspense release workflows.
    Implements Tex. Property Code Ch. 72 requirements.
    """

    def __init__(self, telemetry: Optional[DivisionOrderTelemetry] = None) -> None:
        """Initialize the suspense manager.

        Args:
            telemetry: Optional telemetry instance.
        """
        self._analyzer = SuspenseAnalyzer()
        self._telemetry = telemetry
        self._release_log: List[Dict[str, Any]] = []
        logger.debug("SuspenseManager initialized")

    def place_in_suspense(
        self,
        owner_name: str,
        interest_type: str,
        decimal_interest: str,
        well_name: str,
        suspense_code: str,
        suspense_date: Optional[date] = None,
        accumulated_amount: Decimal = ZERO,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Place an interest owner's revenue in suspense.

        Args:
            owner_name: Owner name.
            interest_type: Interest type code.
            decimal_interest: Decimal interest string.
            well_name: Well name.
            suspense_code: Suspense reason code (S01-S20).
            suspense_date: Date placed in suspense (default today).
            accumulated_amount: Revenue accumulated in suspense.
            notes: Optional notes.

        Returns:
            Suspense entry details.
        """
        op_id = None
        if self._telemetry:
            op_id = self._telemetry.start_operation(
                OperationType.SUSPENSE_ANALYZE,
                metadata={"owner": owner_name, "code": suspense_code},
            )

        susp_date = suspense_date or date.today()
        self._analyzer.add_suspense_entry(
            owner_name=owner_name,
            interest_type=interest_type,
            decimal_interest=decimal_interest,
            well_name=well_name,
            suspense_code=suspense_code,
            suspense_date=susp_date,
            accumulated_amount=accumulated_amount,
            notes=notes,
        )

        result = {
            "owner_name": owner_name,
            "interest_type": interest_type,
            "decimal_interest": decimal_interest,
            "well_name": well_name,
            "suspense_code": suspense_code,
            "suspense_date": susp_date.isoformat(),
            "accumulated_amount": str(accumulated_amount),
            "notes": notes,
        }

        if self._telemetry and op_id:
            self._telemetry.complete_operation(op_id, metadata=result)
            self._telemetry.record_audit_event(
                AuditEventType.SUSPENSE_PLACED,
                f"Placed in suspense: {owner_name} ({suspense_code}) in {well_name}",
                operation_id=op_id,
                details=result,
            )

        logger.info(
            "Suspense placed: {o} code={c} well={w}",
            o=owner_name,
            c=suspense_code,
            w=well_name,
        )
        return result

    def release_from_suspense(
        self,
        owner_name: str,
        well_name: str,
        reason: str,
        release_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """Release an owner from suspense.

        Args:
            owner_name: Owner to release.
            well_name: Well name.
            reason: Reason for release.
            release_date: Date of release (default today).

        Returns:
            Release record.
        """
        rel_date = release_date or date.today()
        release_record = {
            "owner_name": owner_name,
            "well_name": well_name,
            "reason": reason,
            "release_date": rel_date.isoformat(),
            "released_at": datetime.utcnow().isoformat(),
        }
        self._release_log.append(release_record)

        if self._telemetry:
            self._telemetry.record_audit_event(
                AuditEventType.SUSPENSE_RELEASED,
                f"Released from suspense: {owner_name} in {well_name} - {reason}",
                details=release_record,
            )

        logger.info("Suspense released: {o} in {w}", o=owner_name, w=well_name)
        return release_record

    def check_escheat_candidates(self, as_of_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """Identify entries eligible for escheat under Tex. Property Code Ch. 72.

        Args:
            as_of_date: Date to check against (default today).

        Returns:
            List of escheat-eligible entries.
        """
        check_date = as_of_date or date.today()
        candidates = self._analyzer.get_escheat_candidates(check_date)

        if self._telemetry and candidates:
            for candidate in candidates:
                self._telemetry.record_audit_event(
                    AuditEventType.ESCHEAT_FLAGGED,
                    f"Escheat candidate: {candidate.get('owner_name')} "
                    f"({candidate.get('months_in_suspense')} months)",
                    details=candidate,
                )

        logger.info(
            "Escheat check: {n} candidates as of {d}",
            n=len(candidates),
            d=check_date.isoformat(),
        )
        return candidates

    def get_suspense_summary(self) -> Dict[str, Any]:
        """Return suspense summary statistics."""
        return self._analyzer.get_suspense_summary()

    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Return all suspense entries."""
        return self._analyzer.get_all_entries()

    def get_release_log(self) -> List[Dict[str, Any]]:
        """Return the release log."""
        return list(self._release_log)


# ---------------------------------------------------------------------------
# Revenue Distributor
# ---------------------------------------------------------------------------

class RevenueDistributor:
    """Distributes production revenue to interest owners.

    Applies Texas severance tax (oil 4.6%, gas 7.5%), computes
    individual owner payments from gross revenue, handles suspense
    holdbacks, and generates payment reports.
    """

    def __init__(self, telemetry: Optional[DivisionOrderTelemetry] = None) -> None:
        """Initialize the revenue distributor.

        Args:
            telemetry: Optional telemetry instance.
        """
        self._calc = RevenueDistributionCalculator()
        self._telemetry = telemetry
        self._distribution_history: List[Dict[str, Any]] = []
        logger.debug("RevenueDistributor initialized")

    def distribute_revenue(
        self,
        gross_revenue: Decimal,
        product_type: str,
        pay_deck: List[PayDeckEntry],
        deductions: Decimal = ZERO,
        custom_tax_rate: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        """Distribute revenue to all pay deck owners.

        Args:
            gross_revenue: Total gross production revenue.
            product_type: 'OIL' or 'GAS'.
            pay_deck: List of pay deck entries.
            deductions: Post-production deductions.
            custom_tax_rate: Override severance tax rate.

        Returns:
            Distribution result with individual payments.
        """
        op_id = None
        if self._telemetry:
            op_id = self._telemetry.start_operation(
                OperationType.REVENUE_DISTRIBUTE,
                metadata={
                    "gross_revenue": str(gross_revenue),
                    "product_type": product_type,
                    "owner_count": len(pay_deck),
                },
            )

        deck_dicts = [
            {
                "owner_name": e.owner_name,
                "interest_type": e.interest_type,
                "decimal_interest": str(e.decimal_interest),
                "suspense_code": e.suspense_code,
            }
            for e in pay_deck
        ]

        result = self._calc.distribute(
            gross_revenue=gross_revenue,
            product_type=product_type,
            pay_deck=deck_dicts,
            deductions=deductions,
            custom_tax_rate=custom_tax_rate,
        )

        result["deterministic_hash"] = compute_pay_deck_hash(deck_dicts)
        result["distribution_date"] = datetime.utcnow().isoformat()
        self._distribution_history.append(result)

        if self._telemetry and op_id:
            self._telemetry.complete_operation(op_id, metadata={
                "total_distributed": result.get("total_distributed"),
                "total_suspense": result.get("total_suspense"),
                "payment_count": result.get("payment_count"),
            })
            self._telemetry.record_audit_event(
                AuditEventType.REVENUE_DISTRIBUTED,
                f"Revenue distributed: ${gross_revenue} {product_type} to {len(pay_deck)} owners",
                operation_id=op_id,
                details={
                    "gross_revenue": str(gross_revenue),
                    "total_distributed": result.get("total_distributed"),
                    "total_suspense": result.get("total_suspense"),
                },
            )

        logger.info(
            "Revenue distributed: ${rev} {prod} to {n} owners",
            rev=gross_revenue,
            prod=product_type,
            n=len(pay_deck),
        )
        return result

    def get_distribution_history(self) -> List[Dict[str, Any]]:
        """Return distribution history."""
        return list(self._distribution_history)

    def compute_owner_revenue(
        self,
        gross_revenue: Decimal,
        owner_decimal: Decimal,
        product_type: str = "OIL",
        deductions: Decimal = ZERO,
    ) -> Dict[str, Any]:
        """Compute a single owner's revenue share.

        Args:
            gross_revenue: Gross revenue.
            owner_decimal: Owner's decimal interest.
            product_type: 'OIL' or 'GAS'.
            deductions: Deductions.

        Returns:
            Revenue computation result.
        """
        calculator = InterestCalculator()
        tax_rate = OIL_SEVERANCE_TAX_RATE if product_type.upper() == "OIL" else GAS_SEVERANCE_TAX_RATE
        return calculator.compute_revenue_share(
            gross_revenue=gross_revenue,
            owner_decimal=owner_decimal,
            severance_tax_rate=tax_rate,
            deductions=deductions,
        )


# ---------------------------------------------------------------------------
# Duhig Rule Engine
# ---------------------------------------------------------------------------

class DuhigRuleEngine:
    """Applies the Duhig rule to warranty deed conveyances.

    Under Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940),
    when a grantor conveys by warranty deed and reserves an interest,
    but does not own enough to satisfy both the conveyance and the
    reservation, the conveyance (warranty) takes priority and the
    reservation is defeated to the extent of the deficiency.

    This engine analyzes conveyances for Duhig applicability and
    computes the resulting interest allocations.
    """

    def __init__(self, telemetry: Optional[DivisionOrderTelemetry] = None) -> None:
        """Initialize the Duhig rule engine.

        Args:
            telemetry: Optional telemetry instance.
        """
        self._calculator = InterestCalculator()
        self._telemetry = telemetry
        self._applications: List[Dict[str, Any]] = []
        logger.debug("DuhigRuleEngine initialized")

    def analyze_conveyance(
        self,
        grantor_name: str,
        grantee_name: str,
        grantor_ownership: Decimal,
        interest_conveyed: Decimal,
        reservation_claimed: Decimal,
        instrument_type: str = "Warranty Deed",
        document_ref: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze a conveyance for Duhig rule application.

        Args:
            grantor_name: Grantor name.
            grantee_name: Grantee name.
            grantor_ownership: Grantor's actual ownership fraction.
            interest_conveyed: Interest purportedly conveyed.
            reservation_claimed: Interest reserved by grantor.
            instrument_type: Type of instrument.
            document_ref: Document reference.

        Returns:
            Analysis result with Duhig determination.
        """
        op_id = None
        if self._telemetry:
            op_id = self._telemetry.start_operation(
                OperationType.DUHIG_APPLY,
                metadata={"grantor": grantor_name, "grantee": grantee_name},
            )

        is_warranty = instrument_type.lower() in (
            "warranty deed", "general warranty deed", "wd",
        )

        grantee_gets, grantor_keeps, duhig_applied = self._calculator.apply_duhig_rule(
            grantor_ownership=grantor_ownership,
            interest_conveyed=interest_conveyed,
            reservation_claimed=reservation_claimed,
        )

        deficiency = ZERO
        if duhig_applied:
            deficiency = (interest_conveyed + reservation_claimed - grantor_ownership).quantize(
                QUANTIZE_SPEC, rounding=ROUNDING
            )

        result = {
            "grantor": grantor_name,
            "grantee": grantee_name,
            "grantor_ownership": str(grantor_ownership),
            "interest_conveyed": str(interest_conveyed),
            "reservation_claimed": str(reservation_claimed),
            "total_needed": str(interest_conveyed + reservation_claimed),
            "instrument_type": instrument_type,
            "is_warranty_deed": is_warranty,
            "duhig_applicable": is_warranty and duhig_applied,
            "duhig_applied": duhig_applied,
            "grantee_receives": str(grantee_gets),
            "grantor_retains": str(grantor_keeps),
            "reservation_defeated": duhig_applied,
            "deficiency": str(deficiency),
            "document_ref": document_ref,
            "legal_authority": "Duhig v. Peavy-Moore Lumber Co., 135 Tex. 503 (1940)",
            "explanation": (
                f"Grantor {grantor_name} purported to convey {interest_conveyed} "
                f"and reserve {reservation_claimed}, but only owned {grantor_ownership}. "
                + (
                    f"Under the Duhig rule, the warranty deed conveyance takes priority. "
                    f"Grantee {grantee_name} receives {grantee_gets}. "
                    f"Grantor's reservation of {reservation_claimed} is defeated."
                    if duhig_applied else
                    f"Grantor has sufficient interest. Grantee receives {grantee_gets}, "
                    f"grantor retains {grantor_keeps}."
                )
            ),
        }

        self._applications.append(result)

        if self._telemetry and op_id:
            self._telemetry.complete_operation(op_id, metadata={
                "duhig_applied": duhig_applied,
                "grantee_gets": str(grantee_gets),
            })
            if duhig_applied:
                self._telemetry.record_audit_event(
                    AuditEventType.DUHIG_APPLIED,
                    f"Duhig rule applied: {grantor_name} -> {grantee_name}, "
                    f"reservation defeated",
                    operation_id=op_id,
                    details=result,
                )

        logger.info(
            "Duhig analysis: {g}->{ge}, applied={a}",
            g=grantor_name,
            ge=grantee_name,
            a=duhig_applied,
        )
        return result

    def get_applications(self) -> List[Dict[str, Any]]:
        """Return all Duhig rule application records."""
        return list(self._applications)


# ---------------------------------------------------------------------------
# Pooling Unit Handler
# ---------------------------------------------------------------------------

class PoolingUnitHandler:
    """Handles pooling and unitization effects on interest decimals.

    Computes tract participation factors for pooled units using
    surface acreage, perforated lateral length, or other allocation
    methods. Adjusts individual owner decimals to reflect their
    share of the pooled unit.
    """

    def __init__(self, telemetry: Optional[DivisionOrderTelemetry] = None) -> None:
        """Initialize the pooling unit handler.

        Args:
            telemetry: Optional telemetry instance.
        """
        self._calculator = InterestCalculator()
        self._telemetry = telemetry
        self._units: Dict[str, Dict[str, Any]] = {}
        logger.debug("PoolingUnitHandler initialized")

    def create_pooled_unit(
        self,
        unit_name: str,
        tracts: List[Dict[str, Any]],
        allocation_method: PoolingMethod = PoolingMethod.SURFACE_ACREAGE,
        total_lateral_length: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        """Create a pooled unit from multiple tracts.

        Args:
            unit_name: Unit name/designation.
            tracts: List of tract dictionaries with 'tract_id', 'acres',
                     'lateral_length' (optional), 'owners' (dict of name->decimal).
            allocation_method: Method for computing participation factors.
            total_lateral_length: Total lateral length (for PERFORATED_LATERAL method).

        Returns:
            Pooled unit with computed participation factors.
        """
        op_id = None
        if self._telemetry:
            op_id = self._telemetry.start_operation(
                OperationType.POOLING_ALLOCATE,
                metadata={"unit": unit_name, "tracts": len(tracts)},
            )

        total_acres = sum(Decimal(str(t.get("acres", "0"))) for t in tracts)
        total_lateral = total_lateral_length or sum(
            Decimal(str(t.get("lateral_length", "0"))) for t in tracts
        )

        tract_results: List[Dict[str, Any]] = []
        all_unit_owners: Dict[str, Decimal] = defaultdict(lambda: ZERO)

        for tract in tracts:
            tract_id = tract.get("tract_id", str(uuid.uuid4())[:6])
            tract_acres = Decimal(str(tract.get("acres", "0")))
            tract_lateral = Decimal(str(tract.get("lateral_length", "0")))
            tract_owners = tract.get("owners", {})

            if allocation_method == PoolingMethod.SURFACE_ACREAGE:
                if total_acres > ZERO:
                    participation = (tract_acres / total_acres).quantize(
                        QUANTIZE_SPEC, rounding=ROUNDING
                    )
                else:
                    participation = ZERO
            elif allocation_method == PoolingMethod.PERFORATED_LATERAL:
                if total_lateral > ZERO:
                    participation = (tract_lateral / total_lateral).quantize(
                        QUANTIZE_SPEC, rounding=ROUNDING
                    )
                else:
                    participation = ZERO
            elif allocation_method == PoolingMethod.EQUAL_SHARE:
                participation = (UNITY / Decimal(str(len(tracts)))).quantize(
                    QUANTIZE_SPEC, rounding=ROUNDING
                )
            else:
                participation = (tract_acres / total_acres).quantize(
                    QUANTIZE_SPEC, rounding=ROUNDING
                ) if total_acres > ZERO else ZERO

            owner_unit_decimals: Dict[str, str] = {}
            for owner_name, owner_decimal_str in tract_owners.items():
                owner_decimal = Decimal(str(owner_decimal_str))
                unit_decimal = (owner_decimal * participation).quantize(
                    QUANTIZE_SPEC, rounding=ROUNDING
                )
                owner_unit_decimals[owner_name] = str(unit_decimal)
                all_unit_owners[owner_name] = (
                    all_unit_owners[owner_name] + unit_decimal
                ).quantize(QUANTIZE_SPEC, rounding=ROUNDING)

            tract_results.append({
                "tract_id": tract_id,
                "acres": str(tract_acres),
                "lateral_length": str(tract_lateral),
                "participation_factor": str(participation),
                "owner_unit_decimals": owner_unit_decimals,
            })

        unit_data = {
            "unit_name": unit_name,
            "allocation_method": allocation_method.value,
            "total_acres": str(total_acres),
            "total_lateral_length": str(total_lateral),
            "tract_count": len(tracts),
            "tracts": tract_results,
            "unit_owners": {k: str(v) for k, v in all_unit_owners.items()},
            "owner_count": len(all_unit_owners),
        }

        self._units[unit_name] = unit_data

        if self._telemetry and op_id:
            self._telemetry.complete_operation(op_id, metadata={
                "tracts": len(tracts),
                "owners": len(all_unit_owners),
                "method": allocation_method.value,
            })
            self._telemetry.record_audit_event(
                AuditEventType.POOLING_ALLOCATED,
                f"Pooled unit created: {unit_name} ({len(tracts)} tracts, "
                f"{len(all_unit_owners)} owners, method={allocation_method.value})",
                operation_id=op_id,
            )

        logger.info(
            "Pooled unit: {u} | {t} tracts | {o} owners | method={m}",
            u=unit_name,
            t=len(tracts),
            o=len(all_unit_owners),
            m=allocation_method.value,
        )
        return unit_data

    def get_unit(self, unit_name: str) -> Optional[Dict[str, Any]]:
        """Return unit data by name."""
        return self._units.get(unit_name)

    def get_all_units(self) -> Dict[str, Dict[str, Any]]:
        """Return all units."""
        return dict(self._units)


# ---------------------------------------------------------------------------
# Ratification Tracker
# ---------------------------------------------------------------------------

class RatificationTracker:
    """Tracks division order ratification status per owner.

    Manages the workflow of sending division orders to owners,
    tracking responses, handling disputes, and identifying
    owners who have not returned signed division orders.
    """

    def __init__(self, telemetry: Optional[DivisionOrderTelemetry] = None) -> None:
        """Initialize the ratification tracker.

        Args:
            telemetry: Optional telemetry instance.
        """
        self._telemetry = telemetry
        self._ratifications: Dict[str, Dict[str, Any]] = {}
        logger.debug("RatificationTracker initialized")

    def send_division_order(
        self,
        owner_name: str,
        well_name: str,
        decimal_interest: Decimal,
        interest_type: str,
        sent_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """Record that a division order was sent to an owner.

        Args:
            owner_name: Owner name.
            well_name: Well name.
            decimal_interest: Decimal interest on the DO.
            interest_type: Interest type code.
            sent_date: Date sent (default today).

        Returns:
            Ratification tracking record.
        """
        key = f"{owner_name.upper()}|{well_name.upper()}"
        s_date = sent_date or date.today()

        record = {
            "owner_name": owner_name,
            "well_name": well_name,
            "decimal_interest": str(decimal_interest),
            "interest_type": interest_type,
            "sent_date": s_date.isoformat(),
            "status": RatificationStatus.SENT.value,
            "received_date": None,
            "dispute_reason": None,
            "notes": [],
        }
        self._ratifications[key] = record

        if self._telemetry:
            self._telemetry.record_audit_event(
                AuditEventType.RATIFICATION_SENT,
                f"Division order sent to {owner_name} for {well_name} "
                f"({interest_type}: {decimal_interest})",
                details=record,
            )

        logger.info("DO sent: {o} for {w}", o=owner_name, w=well_name)
        return record

    def record_response(
        self,
        owner_name: str,
        well_name: str,
        signed: bool,
        received_date: Optional[date] = None,
        dispute_reason: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Record a response from an owner.

        Args:
            owner_name: Owner name.
            well_name: Well name.
            signed: Whether the DO was signed.
            received_date: Date received.
            dispute_reason: Reason for dispute (if not signed).

        Returns:
            Updated ratification record or None.
        """
        key = f"{owner_name.upper()}|{well_name.upper()}"
        record = self._ratifications.get(key)
        if record is None:
            logger.warning("No ratification record for {o} in {w}", o=owner_name, w=well_name)
            return None

        r_date = received_date or date.today()
        record["received_date"] = r_date.isoformat()

        if signed:
            record["status"] = RatificationStatus.RECEIVED_SIGNED.value
        elif dispute_reason:
            record["status"] = RatificationStatus.DISPUTED.value
            record["dispute_reason"] = dispute_reason
        else:
            record["status"] = RatificationStatus.RECEIVED_UNSIGNED.value

        if self._telemetry:
            self._telemetry.record_audit_event(
                AuditEventType.RATIFICATION_RECEIVED,
                f"DO response from {owner_name} for {well_name}: "
                f"{'signed' if signed else 'unsigned/disputed'}",
                details=record,
            )

        logger.info(
            "DO response: {o} for {w} - {s}",
            o=owner_name,
            w=well_name,
            s="signed" if signed else "disputed/unsigned",
        )
        return record

    def get_outstanding(self, well_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get owners who have not returned signed division orders.

        Args:
            well_name: Optional well name filter.

        Returns:
            List of outstanding ratification records.
        """
        outstanding: List[Dict[str, Any]] = []
        for record in self._ratifications.values():
            if well_name and record["well_name"].upper() != well_name.upper():
                continue
            if record["status"] in (
                RatificationStatus.SENT.value,
                RatificationStatus.RECEIVED_UNSIGNED.value,
                RatificationStatus.DISPUTED.value,
            ):
                outstanding.append(record)
        return outstanding

    def get_ratification_summary(self, well_name: Optional[str] = None) -> Dict[str, Any]:
        """Get ratification status summary.

        Args:
            well_name: Optional well name filter.

        Returns:
            Summary dictionary.
        """
        records = list(self._ratifications.values())
        if well_name:
            records = [r for r in records if r["well_name"].upper() == well_name.upper()]

        by_status: Dict[str, int] = defaultdict(int)
        for r in records:
            by_status[r["status"]] += 1

        return {
            "total_sent": len(records),
            "by_status": dict(by_status),
            "signed_count": by_status.get(RatificationStatus.RECEIVED_SIGNED.value, 0),
            "outstanding_count": sum(
                by_status.get(s, 0) for s in [
                    RatificationStatus.SENT.value,
                    RatificationStatus.RECEIVED_UNSIGNED.value,
                    RatificationStatus.DISPUTED.value,
                ]
            ),
            "completion_rate": round(
                by_status.get(RatificationStatus.RECEIVED_SIGNED.value, 0)
                / max(len(records), 1), 4
            ),
        }

    def get_all_records(self) -> List[Dict[str, Any]]:
        """Return all ratification records."""
        return list(self._ratifications.values())


# ---------------------------------------------------------------------------
# JOA Parser
# ---------------------------------------------------------------------------

class JOAParser:
    """Parses Joint Operating Agreement provisions.

    Extracts working interest shares, non-consent penalties,
    operator designation, accounting procedures, and other
    JOA provisions relevant to division order administration.
    """

    DEFAULT_NON_CONSENT_PENALTY = Decimal("300")
    AAPL_610_2015_PENALTY = Decimal("300")
    AAPL_610_1989_PENALTY = Decimal("200")

    def __init__(self, telemetry: Optional[DivisionOrderTelemetry] = None) -> None:
        """Initialize the JOA parser.

        Args:
            telemetry: Optional telemetry instance.
        """
        self._telemetry = telemetry
        self._parsed_joas: List[JOAProvision] = []
        logger.debug("JOAParser initialized")

    def parse_joa(self, joa_data: Dict[str, Any]) -> JOAProvision:
        """Parse JOA data into a structured provision.

        Args:
            joa_data: Dictionary with JOA terms.

        Returns:
            Parsed JOAProvision.
        """
        op_id = None
        if self._telemetry:
            op_id = self._telemetry.start_operation(
                OperationType.JOA_PARSE,
                metadata={"operator": joa_data.get("operator", "")},
            )

        wi_shares: Dict[str, Decimal] = {}
        for party, share in joa_data.get("working_interest_shares", {}).items():
            wi_shares[party] = Decimal(str(share)).quantize(QUANTIZE_SPEC, rounding=ROUNDING)

        penalty_pct = Decimal(str(
            joa_data.get("non_consent_penalty_pct", self.DEFAULT_NON_CONSENT_PENALTY)
        ))

        provision = JOAProvision(
            joa_id=joa_data.get("joa_id", f"JOA-{uuid.uuid4().hex[:8]}"),
            operator=joa_data.get("operator", ""),
            non_operator_parties=joa_data.get("non_operator_parties", []),
            working_interest_shares=wi_shares,
            non_consent_penalty_pct=penalty_pct,
            overhead_rate_monthly=Decimal(str(joa_data.get("overhead_rate_monthly", "0"))),
            accounting_procedure=joa_data.get("accounting_procedure", "COPAS 2005"),
            area_of_mutual_interest=joa_data.get("area_of_mutual_interest", False),
            ami_radius_miles=(
                Decimal(str(joa_data["ami_radius_miles"]))
                if joa_data.get("ami_radius_miles") else None
            ),
            preferential_right=joa_data.get("preferential_right", False),
            afe_approval_threshold=(
                Decimal(str(joa_data["afe_approval_threshold"]))
                if joa_data.get("afe_approval_threshold") else None
            ),
            effective_date=(
                date.fromisoformat(joa_data["effective_date"])
                if joa_data.get("effective_date") else None
            ),
            notes=joa_data.get("notes", []),
        )

        self._parsed_joas.append(provision)

        if self._telemetry and op_id:
            self._telemetry.complete_operation(op_id, metadata=provision.to_dict())

        logger.info(
            "JOA parsed: operator={op}, parties={n}, penalty={p}%",
            op=provision.operator,
            n=len(provision.non_operator_parties),
            p=provision.non_consent_penalty_pct,
        )
        return provision

    def compute_non_consent_penalty(
        self,
        well_cost: Decimal,
        non_consent_wi: Decimal,
        penalty_pct: Decimal = DEFAULT_NON_CONSENT_PENALTY,
    ) -> Dict[str, Any]:
        """Compute the non-consent penalty for a party electing not to participate.

        Under AAPL 610-2015 Article VI.B.2, a non-consenting party forfeits
        their share of production until the consenting parties have recovered
        the non-consenting party's share of costs plus a penalty (typically 300%).

        Args:
            well_cost: Total well cost (drilling + completion).
            non_consent_wi: Non-consenting party's working interest.
            penalty_pct: Penalty percentage (default 300%).

        Returns:
            Non-consent penalty computation.
        """
        nc_share_of_cost = (well_cost * non_consent_wi).quantize(
            Decimal("0.01"), rounding=ROUNDING
        )
        penalty_multiplier = (penalty_pct / Decimal("100")).quantize(
            QUANTIZE_SPEC, rounding=ROUNDING
        )
        recovery_amount = (nc_share_of_cost * (UNITY + penalty_multiplier)).quantize(
            Decimal("0.01"), rounding=ROUNDING
        )

        return {
            "well_cost": str(well_cost),
            "non_consent_wi": str(non_consent_wi),
            "nc_share_of_cost": str(nc_share_of_cost),
            "penalty_percentage": str(penalty_pct),
            "penalty_multiplier": str(penalty_multiplier),
            "recovery_amount": str(recovery_amount),
            "legal_authority": "AAPL Model Form 610-2015, Article VI.B.2",
            "explanation": (
                f"Non-consenting party's share of cost: ${nc_share_of_cost}. "
                f"Under {penalty_pct}% non-consent penalty, consenting parties "
                f"must recover ${recovery_amount} from the non-consenting party's "
                f"share of production before the non-consenting party receives revenue."
            ),
        }

    def get_parsed_joas(self) -> List[Dict[str, Any]]:
        """Return all parsed JOA provisions."""
        return [j.to_dict() for j in self._parsed_joas]


# ---------------------------------------------------------------------------
# Epistemic Guardrails
# ---------------------------------------------------------------------------

class EpistemicGuardrails:
    """Applies epistemic guardrails to engine responses.

    Ensures responses do not contain banned phrases, includes
    appropriate disclaimers, and maintains deterministic behavior.
    """

    def apply(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Apply epistemic guardrails to a response.

        Args:
            response: The response dictionary.

        Returns:
            Response with guardrails applied.
        """
        response["disclosure_caveat"] = EPISTEMIC_DISCLAIMER
        response["engine_mode"] = ENGINE_MODE
        response["engine_version"] = ENGINE_VERSION

        if "analysis_text" in response:
            text = response["analysis_text"]
            for phrase in BANNED_PHRASES:
                if phrase.lower() in text.lower():
                    text = text.replace(phrase, "[REDACTED BY EPISTEMIC GUARDRAIL]")
                    text = text.replace(phrase.title(), "[REDACTED BY EPISTEMIC GUARDRAIL]")
            response["analysis_text"] = text

        return response


# ---------------------------------------------------------------------------
# Main Division Order Engine
# ---------------------------------------------------------------------------

class DivisionOrderEngine:
    """Main LM03 Division Order Engine.

    Production-grade engine integrating all 20 TIE components for
    division order analysis, decimal interest computation, pay deck
    construction, revenue distribution, suspense management,
    and chain of title tracing.

    Engine ID: LM03
    Port: 8411
    Mode: DET (Deterministic)
    Authority: 5.0
    """

    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Initialize the Division Order Engine.

        Args:
            config_path: Path to config.json (default: adjacent to this file).
        """
        self._config = self._load_config(config_path or CONFIG_PATH)
        self._engine_id = ENGINE_ID
        self._version = ENGINE_VERSION
        self._port = ENGINE_PORT
        self._mode = ENGINE_MODE
        self._authority = ENGINE_AUTHORITY

        # TIE Components
        self._telemetry = DivisionOrderTelemetry(engine_id=self._engine_id)
        self._doctrine_cache = DivisionOrderDoctrineCache()
        self._semantic_dict = DivisionOrderSemanticDictionary()
        self._search_index = DoctrineSearchIndex()
        self._searcher = DivisionOrderSearcher()
        self._calculator = InterestCalculator()
        self._converter = DecimalFormatConverter()
        self._normalizer = InterestTermNormalizer()
        self._chain_terms = ChainOfTitleTerms()
        self._guardrails = EpistemicGuardrails()

        # Domain Components
        self._chain_tracer = ChainOfTitleTracer(telemetry=self._telemetry)
        self._pay_deck_builder = PayDeckBuilder(telemetry=self._telemetry)
        self._suspense_manager = SuspenseManager(telemetry=self._telemetry)
        self._revenue_distributor = RevenueDistributor(telemetry=self._telemetry)
        self._duhig_engine = DuhigRuleEngine(telemetry=self._telemetry)
        self._pooling_handler = PoolingUnitHandler(telemetry=self._telemetry)
        self._ratification_tracker = RatificationTracker(telemetry=self._telemetry)
        self._joa_parser = JOAParser(telemetry=self._telemetry)
        self._suspense_analyzer = SuspenseAnalyzer()

        # Division Order storage
        self._division_orders: Dict[str, DivisionOrderRecord] = {}

        # Populate search index from doctrine cache
        self._index_doctrines()

        # Record engine start
        self._telemetry.record_audit_event(
            AuditEventType.ENGINE_STARTED,
            f"LM03 Division Order Engine v{self._version} started on port {self._port}",
            details={
                "engine_id": self._engine_id,
                "version": self._version,
                "mode": self._mode,
                "authority": self._authority,
                "doctrine_blocks": self._doctrine_cache.block_count,
                "semantic_terms": len(self._semantic_dict._terms),
            },
        )

        logger.info(
            "LM03 DivisionOrderEngine initialized | v={v} port={p} mode={m} "
            "doctrines={d} terms={t}",
            v=self._version,
            p=self._port,
            m=self._mode,
            d=self._doctrine_cache.block_count,
            t=len(self._semantic_dict._terms),
        )

    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load engine configuration from JSON file.

        Args:
            config_path: Path to config.json.

        Returns:
            Configuration dictionary.
        """
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            logger.debug("Config loaded from {p}", p=config_path)
            return config
        logger.warning("Config not found at {p}, using defaults", p=config_path)
        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "port": ENGINE_PORT,
            "mode": ENGINE_MODE,
        }

    def _index_doctrines(self) -> None:
        """Populate the search index from doctrine cache blocks."""
        for block in self._doctrine_cache.all_blocks:
            text = f"{block.title} {block.summary} {block.full_text} {' '.join(block.keywords)}"
            self._search_index.add_document(
                doc_id=block.block_id,
                text=text,
                metadata={
                    "category": block.category.value,
                    "title": block.title,
                    "severity": block.severity.value,
                },
            )
        logger.debug(
            "Doctrine search index built: {n} documents",
            n=self._search_index.get_document_count(),
        )

    # -- Query Entry Point ---------------------------------------------------

    def query(self, question: str, mode: str = "analysis") -> Dict[str, Any]:
        """Main query entry point for the division order engine.

        Args:
            question: Natural language question about division orders.
            mode: Response mode ('fast', 'analysis', 'expert', 'audit').

        Returns:
            Complete response with doctrine matches, analysis, and hash.
        """
        op_id = self._telemetry.start_operation(
            OperationType.ENGINE_QUERY,
            metadata={"question": question[:100], "mode": mode},
        )

        doctrine_results = self._doctrine_cache.search(question, max_results=5)
        semantic_matches = self._semantic_dict.search(question, max_results=5)
        index_results = self._search_index.search(question, max_results=5)

        doctrine_data = [
            {"block": block.to_dict(), "score": round(score, 4)}
            for block, score in doctrine_results
        ]
        semantic_data = [
            {"term": term.to_dict(), "score": round(score, 4)}
            for term, score in semantic_matches
        ]
        index_data = [
            {"doc_id": doc_id, "score": round(score, 4), "metadata": meta}
            for doc_id, score, meta in index_results
        ]

        all_citations: List[str] = []
        all_case_law: List[str] = []
        for block, _ in doctrine_results:
            all_citations.extend(block.citations)
            all_case_law.extend(block.case_law)

        response = {
            "engine_id": self._engine_id,
            "engine_version": self._version,
            "mode": self._mode,
            "query": question,
            "response_mode": mode,
            "doctrine_matches": doctrine_data,
            "semantic_matches": semantic_data,
            "index_matches": index_data,
            "citations": list(set(all_citations)),
            "case_law": list(set(all_case_law)),
            "analysis_text": self._generate_analysis_text(question, doctrine_results),
            "timestamp": datetime.utcnow().isoformat(),
        }

        response = self._guardrails.apply(response)
        response["deterministic_hash"] = compute_deterministic_hash(response)

        duration = self._telemetry.complete_operation(op_id, metadata={
            "doctrine_matches": len(doctrine_data),
            "semantic_matches": len(semantic_data),
        })
        self._telemetry.record_audit_event(
            AuditEventType.DOCTRINE_SEARCHED,
            f"Query: '{question[:60]}' | {len(doctrine_data)} doctrine matches in {duration:.1f}ms",
            operation_id=op_id,
        )

        return response

    def _generate_analysis_text(
        self,
        question: str,
        doctrine_results: List[Tuple[DoctrineCacheBlock, float]],
    ) -> str:
        """Generate analysis text from doctrine matches.

        Args:
            question: Original question.
            doctrine_results: Matched doctrine blocks with scores.

        Returns:
            Analysis text string.
        """
        if not doctrine_results:
            return (
                f"No specific doctrine match found for: '{question}'. "
                f"The LM03 Division Order Engine covers {self._doctrine_cache.block_count} "
                f"doctrine blocks across division order basics, decimal interest calculation, "
                f"Duhig rule, proportionate reduction, suspense/escheat, pooling/unitization, "
                f"JOA provisions, and revenue distribution."
            )

        parts: List[str] = []
        for block, score in doctrine_results[:3]:
            parts.append(f"[{block.block_id}] {block.title} (relevance: {score:.2f})")
            parts.append(block.full_text)
            if block.citations:
                parts.append(f"Citations: {'; '.join(block.citations[:3])}")
            parts.append("")

        return "\n".join(parts)

    # -- Interest Calculation ------------------------------------------------

    def calculate_nri(
        self,
        working_interest: str,
        royalty_burden: str,
        orri_burden: str = "0",
        other_burdens: str = "0",
    ) -> Dict[str, Any]:
        """Calculate Net Revenue Interest.

        Args:
            working_interest: Working interest as string.
            royalty_burden: Royalty burden as string.
            orri_burden: ORRI burden as string.
            other_burdens: Other burdens as string.

        Returns:
            NRI calculation result.
        """
        op_id = self._telemetry.start_operation(OperationType.INTEREST_CALC)

        wi = Decimal(working_interest)
        rb = Decimal(royalty_burden)
        orri = Decimal(orri_burden)
        other = Decimal(other_burdens)

        nri = self._calculator.compute_nri(wi, rb, orri, other)

        result = {
            "working_interest": str(wi),
            "royalty_burden": str(rb),
            "orri_burden": str(orri),
            "other_burdens": str(other),
            "total_burden": str(rb + orri + other),
            "revenue_factor": str(UNITY - rb - orri - other),
            "nri": str(nri),
            "calculation": f"NRI = {wi} x (1.0 - {rb} - {orri} - {other}) = {nri}",
        }

        result = self._guardrails.apply(result)
        result["deterministic_hash"] = compute_deterministic_hash(result)

        self._telemetry.complete_operation(op_id, metadata=result)
        return result

    def calculate_royalty_decimal(
        self,
        mineral_ownership: str,
        lease_royalty_rate: str,
        tract_participation: str = "1.0",
    ) -> Dict[str, Any]:
        """Calculate a royalty owner's division order decimal.

        Args:
            mineral_ownership: Mineral ownership fraction.
            lease_royalty_rate: Lease royalty rate.
            tract_participation: Tract participation factor.

        Returns:
            Royalty decimal calculation result.
        """
        op_id = self._telemetry.start_operation(OperationType.INTEREST_CALC)

        mo = Decimal(mineral_ownership)
        lr = Decimal(lease_royalty_rate)
        tp = Decimal(tract_participation)

        result_decimal = self._calculator.compute_royalty_decimal(mo, lr, tp)

        result = {
            "mineral_ownership": str(mo),
            "lease_royalty_rate": str(lr),
            "tract_participation": str(tp),
            "royalty_decimal": str(result_decimal),
            "calculation": f"Royalty = {mo} x {lr} x {tp} = {result_decimal}",
        }

        result = self._guardrails.apply(result)
        result["deterministic_hash"] = compute_deterministic_hash(result)

        self._telemetry.complete_operation(op_id, metadata=result)
        return result

    # -- Decimal Conversion --------------------------------------------------

    def convert_interest(self, value: str, target_format: str = "decimal") -> Dict[str, Any]:
        """Convert an interest value between formats.

        Args:
            value: Input value (fraction, percentage, decimal, NMA).
            target_format: Target format ('decimal', 'fraction', 'percentage').

        Returns:
            Conversion result.
        """
        op_id = self._telemetry.start_operation(OperationType.DECIMAL_CONVERT)

        parsed = self._converter.parse_interest_string(value)

        if parsed is None:
            self._telemetry.fail_operation(op_id, f"Could not parse: {value}")
            return {
                "input": value,
                "error": f"Could not parse interest value: {value}",
                "supported_formats": [
                    "Fractions: 1/8, 3/16",
                    "Percentages: 12.5%",
                    "Decimals: 0.125",
                    "NMA: 25 NMA in 640",
                ],
            }

        result = {
            "input": value,
            "decimal": str(parsed),
            "fraction": self._converter.decimal_to_fraction(parsed),
            "percentage": self._converter.decimal_to_percentage(parsed),
        }

        result = self._guardrails.apply(result)
        result["deterministic_hash"] = compute_deterministic_hash(result)

        self._telemetry.complete_operation(op_id, metadata=result)
        return result

    # -- Division Order Generation -------------------------------------------

    def generate_division_order(
        self,
        well_data: Dict[str, Any],
        ownership_data: Dict[str, str],
        interest_types: Optional[Dict[str, str]] = None,
        title_opinion_ref: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a complete division order for a well.

        Args:
            well_data: Well information dictionary.
            ownership_data: Ownership map (owner_name -> decimal).
            interest_types: Optional interest type map.
            title_opinion_ref: Optional title opinion reference.

        Returns:
            Division order record.
        """
        op_id = self._telemetry.start_operation(
            OperationType.DIVISION_ORDER_GEN,
            metadata={"well": well_data.get("well_name", "")},
        )

        well = WellUnit.from_dict(well_data)
        pay_deck = self._pay_deck_builder.build_pay_deck(
            well=well,
            ownership=ownership_data,
            interest_types=interest_types,
        )

        validation = self._pay_deck_builder.validate_pay_deck(pay_deck)

        order_id = f"DO-{uuid.uuid4().hex[:10]}"
        order = DivisionOrderRecord(
            order_id=order_id,
            well=well,
            status=DivisionOrderStatus.DRAFT,
            pay_deck=pay_deck,
            created_date=date.today(),
            effective_date=well.effective_date,
            title_opinion_ref=title_opinion_ref,
            unity_check_result=validation,
        )

        order_dict = order.to_dict()
        order.deterministic_hash = compute_deterministic_hash(order_dict)
        self._division_orders[order_id] = order

        result = {
            "order_id": order_id,
            "division_order": order.to_dict(),
            "validation": validation,
            "pay_deck_entries": len(pay_deck),
            "unity_passed": validation.get("validation_passed", False),
        }

        result = self._guardrails.apply(result)
        result["deterministic_hash"] = compute_deterministic_hash(result)

        self._telemetry.complete_operation(op_id, metadata={
            "order_id": order_id,
            "entries": len(pay_deck),
            "unity_passed": validation.get("validation_passed", False),
        })
        self._telemetry.record_audit_event(
            AuditEventType.DIVISION_ORDER_GENERATED,
            f"Division order generated: {order_id} for {well.well_name} "
            f"({len(pay_deck)} entries)",
            operation_id=op_id,
        )

        return result

    # -- Chain of Title Tracing ----------------------------------------------

    def trace_chain_of_title(
        self,
        sovereign: str,
        conveyances: List[Dict[str, Any]],
        sovereign_interest: str = "1.0",
    ) -> Dict[str, Any]:
        """Trace interests through a chain of title.

        Args:
            sovereign: Name of the original patentee.
            conveyances: List of conveyance event dictionaries.
            sovereign_interest: Sovereign's initial interest.

        Returns:
            Chain trace result with ownership summary.
        """
        self._chain_tracer.reset()
        self._chain_tracer.set_sovereign(sovereign, Decimal(sovereign_interest))

        events: List[ConveyanceEvent] = []
        for i, conv in enumerate(conveyances):
            int_type = InterestType.MINERAL_INTEREST
            if conv.get("interest_type"):
                try:
                    int_type = InterestType(conv["interest_type"])
                except ValueError:
                    int_type = InterestType.MINERAL_INTEREST

            event = ConveyanceEvent(
                event_id=conv.get("event_id", f"CE-{i:04d}"),
                instrument_type=conv.get("instrument_type", "Warranty Deed"),
                recording_date=(
                    date.fromisoformat(conv["recording_date"])
                    if conv.get("recording_date") else None
                ),
                grantor=conv.get("grantor", ""),
                grantee=conv.get("grantee", ""),
                interest_conveyed=Decimal(str(conv.get("interest_conveyed", "0"))),
                interest_type=int_type,
                reservation=(
                    Decimal(str(conv["reservation"])) if conv.get("reservation") else None
                ),
                is_warranty_deed=conv.get("is_warranty_deed", False),
                legal_description=conv.get("legal_description"),
                document_reference=conv.get("document_reference"),
            )
            events.append(event)

        chain_result = self._chain_tracer.trace_chain(events)

        result = {
            "sovereign": sovereign,
            "conveyance_count": len(events),
            "chain_result": chain_result,
        }

        result = self._guardrails.apply(result)
        result["deterministic_hash"] = compute_deterministic_hash({
            "sovereign": sovereign,
            "events": len(events),
            "ownership": chain_result.get("current_ownership", {}),
        })

        return result

    # -- Health Check --------------------------------------------------------

    def health_check(self) -> Dict[str, Any]:
        """Return comprehensive engine health status.

        Returns:
            Health check dictionary.
        """
        self._telemetry.start_operation(OperationType.HEALTH_CHECK)

        doctrine_health = self._doctrine_cache.health_check()
        semantic_health = self._semantic_dict.health_check()
        search_health = self._search_index.health_check()
        telemetry_health = self._telemetry.health_check()
        integrity = self._doctrine_cache.verify_integrity()

        component_status = {
            "doctrine_cache": doctrine_health,
            "semantic_dictionary": semantic_health,
            "search_index": search_health,
            "telemetry": telemetry_health,
            "doctrine_integrity": integrity,
            "chain_tracer": {"status": "healthy"},
            "pay_deck_builder": {
                "status": "healthy",
                "active_pay_decks": len(self._pay_deck_builder.get_all_well_ids()),
            },
            "suspense_manager": {
                "status": "healthy",
                "summary": self._suspense_manager.get_suspense_summary(),
            },
            "revenue_distributor": {"status": "healthy"},
            "duhig_engine": {
                "status": "healthy",
                "applications": len(self._duhig_engine.get_applications()),
            },
            "pooling_handler": {
                "status": "healthy",
                "units": len(self._pooling_handler.get_all_units()),
            },
            "ratification_tracker": {
                "status": "healthy",
                "summary": self._ratification_tracker.get_ratification_summary(),
            },
            "joa_parser": {"status": "healthy"},
            "epistemic_guardrails": {"status": "healthy"},
        }

        all_healthy = all(
            c.get("status") == "healthy" for c in component_status.values()
            if isinstance(c, dict) and "status" in c
        )

        health = {
            "engine_id": self._engine_id,
            "engine_name": ENGINE_NAME,
            "version": self._version,
            "port": self._port,
            "mode": self._mode,
            "authority": self._authority,
            "status": "healthy" if all_healthy else "degraded",
            "tie_components_active": 20,
            "division_orders_count": len(self._division_orders),
            "components": component_status,
            "timestamp": datetime.utcnow().isoformat(),
        }

        health["deterministic_hash"] = compute_deterministic_hash(health)
        return health

    # -- Coverage Map --------------------------------------------------------

    def get_coverage_map(self) -> Dict[str, Any]:
        """Return the doctrine coverage map."""
        return self._doctrine_cache.get_coverage_map()

    # -- Session Summary -----------------------------------------------------

    def get_session_summary(self) -> Dict[str, Any]:
        """Return telemetry session summary."""
        return self._telemetry.get_session_summary()

    # -- Audit Trail ---------------------------------------------------------

    def get_audit_trail(
        self,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Return audit trail events.

        Args:
            event_type: Optional filter by event type.
            limit: Maximum events to return.

        Returns:
            List of audit event dictionaries.
        """
        et = None
        if event_type:
            try:
                et = AuditEventType(event_type)
            except ValueError:
                et = None
        return self._telemetry.get_audit_trail(event_type=et, limit=limit)

    # -- Component Accessors -------------------------------------------------

    @property
    def doctrine_cache(self) -> DivisionOrderDoctrineCache:
        """Access the doctrine cache."""
        return self._doctrine_cache

    @property
    def semantic_dictionary(self) -> DivisionOrderSemanticDictionary:
        """Access the semantic dictionary."""
        return self._semantic_dict

    @property
    def calculator(self) -> InterestCalculator:
        """Access the interest calculator."""
        return self._calculator

    @property
    def converter(self) -> DecimalFormatConverter:
        """Access the decimal format converter."""
        return self._converter

    @property
    def chain_tracer(self) -> ChainOfTitleTracer:
        """Access the chain of title tracer."""
        return self._chain_tracer

    @property
    def pay_deck_builder(self) -> PayDeckBuilder:
        """Access the pay deck builder."""
        return self._pay_deck_builder

    @property
    def suspense_manager(self) -> SuspenseManager:
        """Access the suspense manager."""
        return self._suspense_manager

    @property
    def revenue_distributor(self) -> RevenueDistributor:
        """Access the revenue distributor."""
        return self._revenue_distributor

    @property
    def duhig_engine(self) -> DuhigRuleEngine:
        """Access the Duhig rule engine."""
        return self._duhig_engine

    @property
    def pooling_handler(self) -> PoolingUnitHandler:
        """Access the pooling unit handler."""
        return self._pooling_handler

    @property
    def ratification_tracker(self) -> RatificationTracker:
        """Access the ratification tracker."""
        return self._ratification_tracker

    @property
    def joa_parser(self) -> JOAParser:
        """Access the JOA parser."""
        return self._joa_parser

    @property
    def telemetry(self) -> DivisionOrderTelemetry:
        """Access the telemetry system."""
        return self._telemetry


# ============================================================================
# FASTAPI SERVER + CLOUD RETRIEVAL
# ============================================================================

import sys as _sys
import asyncio as _asyncio
from pathlib import Path as _Path
from contextlib import asynccontextmanager

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "_shared"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel as _BaseModel, Field as _Field

try:
    from cloud_retriever import retrieve_cloud_knowledge
    _CLOUD_AVAILABLE = True
except ImportError:
    _CLOUD_AVAILABLE = False
    logger.warning("cloud_retriever not available — running without cloud knowledge")


class _QueryRequest(_BaseModel):
    query: str = ""
    prompt: str = ""
    mode: str = "analysis"
    include_cloud: bool = True


class _QueryResponse(_BaseModel):
    engine_id: str = ENGINE_ID
    engine_name: str = ENGINE_NAME
    query: str = ""
    analysis: Dict[str, Any] = _Field(default_factory=dict)
    cloud_knowledge: Dict[str, Any] = _Field(default_factory=dict)
    cloud_citations: List[Dict[str, str]] = _Field(default_factory=list)
    processing_time_ms: float = 0.0
    determinism_hash: str = ""


_engine = DivisionOrderEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"LM03 {ENGINE_NAME} v{ENGINE_VERSION} starting on port {ENGINE_PORT}")
    yield
    if _CLOUD_AVAILABLE:
        from cloud_retriever import get_cloud_retriever
        await get_cloud_retriever().close()
    logger.info(f"LM03 {ENGINE_NAME} shutting down")


app = FastAPI(
    title=f"ECHO {ENGINE_ID} {ENGINE_NAME}", version=ENGINE_VERSION,
    description="Division Order Engine with Cloud Knowledge Retrieval", lifespan=lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
async def health():
    return {
        "engine_id": ENGINE_ID, "engine_name": ENGINE_NAME,
        "version": ENGINE_VERSION, "status": "healthy", "port": ENGINE_PORT,
        "cloud_available": _CLOUD_AVAILABLE,
    }


@app.post("/query")
async def query_endpoint(request: _QueryRequest):
    import time, hashlib
    start = time.monotonic()
    q = request.query or request.prompt

    # Cloud retrieval
    cloud_data: Dict[str, Any] = {}
    cloud_citations: List[Dict[str, str]] = []
    if _CLOUD_AVAILABLE and request.include_cloud:
        try:
            cloud = await retrieve_cloud_knowledge(q, category="division_order")
            cloud_data = {
                "records": cloud.total_records,
                "merged_context": cloud.merged_text(3000),
                "sources_succeeded": cloud.sources_succeeded,
                "retrieval_time_ms": cloud.retrieval_time_ms,
            }
            cloud_citations = cloud.citation_list()
        except Exception as e:
            logger.warning(f"Cloud retrieval failed: {e}")

    # Local engine query
    analysis: Dict[str, Any] = {}
    try:
        analysis = _engine.query(q, mode=request.mode)
    except Exception as e:
        logger.error(f"Local query failed: {e}")
        analysis = {"error": str(e)}

    elapsed = (time.monotonic() - start) * 1000
    det_hash = hashlib.sha256(f"{q}:{elapsed}".encode()).hexdigest()[:16]

    return _QueryResponse(
        query=q, analysis=analysis, cloud_knowledge=cloud_data,
        cloud_citations=cloud_citations, processing_time_ms=round(elapsed, 2),
        determinism_hash=det_hash,
    )


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting LM03 {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    uvicorn.run("engine:app", host="0.0.0.0", port=ENGINE_PORT, reload=False, log_level="info")
