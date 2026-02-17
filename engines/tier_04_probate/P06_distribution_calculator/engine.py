"""
P06_distribution_calculator - Estate Distribution Calculation Engine
TIE-20 compliant engine for calculating estate distributions per will, intestacy, tax apportionment.
Version 1.0.0 | Port 8656 | No-LLM deterministic computation
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from dataclasses import dataclass, asdict
import sys

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Add parent directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "APPS" / "_SHARED"))

try:
    from cloud_retriever import CloudRetriever
    CLOUD_AVAILABLE = True
except ImportError:
    logger.warning("cloud_retriever not available, cloud fallback disabled")
    CLOUD_AVAILABLE = False


# Ensure sibling modules are importable
ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))
from doctrines import (
    DOCTRINE_BLOCKS,
    DoctrineBlock,
    ConfidenceLevel,
    AuthorityLevel,
    get_doctrine_by_topic,
    search_doctrines_by_keyword
)


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "P06_distribution_calculator"
VERSION = "1.0.0"
PORT = 8656
CONFIG_PATH = Path(__file__).parent / "config.json"
AUDIT_TRAIL_PATH = Path(__file__).parent / "audit_trail.jsonl"

# Load config
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

# Configure loguru
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "engine.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG"
)


# ============================================================================
# ENUMS & DATA MODELS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class BequestType(str, Enum):
    SPECIFIC = "SPECIFIC"
    GENERAL = "GENERAL"
    DEMONSTRATIVE = "DEMONSTRATIVE"
    RESIDUARY = "RESIDUARY"


class PropertyType(str, Enum):
    COMMUNITY = "COMMUNITY"
    SEPARATE_PERSONAL = "SEPARATE_PERSONAL"
    SEPARATE_REAL = "SEPARATE_REAL"


class DistributionMethod(str, Enum):
    PER_STIRPES = "PER_STIRPES"
    PER_CAPITA_EACH_GEN = "PER_CAPITA_EACH_GEN"
    EQUAL = "EQUAL"


@dataclass
class Beneficiary:
    name: str
    relationship: str
    is_alive: bool
    descendants: List['Beneficiary']
    generation: int


@dataclass
class Bequest:
    beneficiary_name: str
    bequest_type: BequestType
    description: str
    amount: Optional[Decimal]
    property_id: Optional[str]
    priority: int  # For abatement ordering


@dataclass
class Asset:
    asset_id: str
    description: str
    fmv_at_death: Decimal
    basis: Decimal
    property_type: PropertyType
    source: str  # "earned", "inherited_from_family", "gift", etc.


@dataclass
class Debt:
    creditor: str
    amount: Decimal
    priority: int  # 1=secured, 2=admin expenses, 3=taxes, 4=unsecured


class DistributionRequest(BaseModel):
    estate_id: str = Field(..., description="Unique estate identifier")
    decedent_name: str
    jurisdiction: str = "Texas"
    marital_status: str  # "married", "single", "divorced", "widowed"
    marriage_years: Optional[int] = None

    # Assets
    assets: List[Dict[str, Any]]

    # Debts
    debts: List[Dict[str, Any]] = []

    # Will provisions (if testate)
    has_will: bool = False
    bequests: List[Dict[str, Any]] = []

    # Intestacy (if no will or partial intestacy)
    descendants: List[Dict[str, Any]] = []
    surviving_spouse: Optional[str] = None
    parents_alive: bool = False
    siblings: List[str] = []

    # Distribution preferences
    distribution_method: DistributionMethod = DistributionMethod.PER_CAPITA_EACH_GEN
    response_mode: ResponseMode = ResponseMode.DEFENSE

    # Tax elections
    estate_tax_apportionment: str = "pro_rata"  # or "residuary_bears_all"
    make_643e_election: bool = False
    dni_optimization: bool = True


class DistributionResult(BaseModel):
    estate_id: str
    timestamp: str
    total_estate_value: Decimal
    total_debts: Decimal
    net_distributable: Decimal
    distributions: List[Dict[str, Any]]
    estate_tax: Decimal
    income_tax: Decimal
    executor_commission: Decimal
    attorney_fees: Decimal
    confidence: ConfidenceLevel
    reasoning: str
    authorities_cited: List[str]
    warnings: List[str]
    sha256_hash: str


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    """TIE-20 Component 8: Telemetry module for query tracking."""

    def __init__(self):
        self.queries_total = 0
        self.queries_by_type = {}
        self.latencies = []
        self.errors = []
        self.cache_hits = 0
        self.cache_misses = 0

    def record_query(self, query_type: str, latency_ms: float, success: bool, error: Optional[str] = None):
        self.queries_total += 1
        self.queries_by_type[query_type] = self.queries_by_type.get(query_type, 0) + 1
        self.latencies.append(latency_ms)
        if not success and error:
            self.errors.append({"type": query_type, "error": error, "timestamp": datetime.utcnow().isoformat()})

    def record_cache_hit(self):
        self.cache_hits += 1

    def record_cache_miss(self):
        self.cache_misses += 1

    def get_stats(self) -> Dict[str, Any]:
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        return {
            "queries_total": self.queries_total,
            "queries_by_type": self.queries_by_type,
            "avg_latency_ms": round(avg_latency, 2),
            "cache_hit_rate": round(self.cache_hits / (self.cache_hits + self.cache_misses), 2) if (self.cache_hits + self.cache_misses) > 0 else 0,
            "error_count": len(self.errors),
            "recent_errors": self.errors[-5:]
        }


# ============================================================================
# DRIFT WATCHER
# ============================================================================

class DriftWatcher:
    """TIE-20 Component 9: Detect doctrine drift over time."""

    def __init__(self):
        self.baseline_hash = self._compute_doctrine_hash()
        self.last_check = datetime.utcnow()

    def _compute_doctrine_hash(self) -> str:
        """Hash all doctrine blocks for drift detection."""
        content = json.dumps([asdict(block) for block in DOCTRINE_BLOCKS], sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()

    def check_drift(self) -> Dict[str, Any]:
        """Check if doctrines have drifted from baseline."""
        current_hash = self._compute_doctrine_hash()
        drifted = current_hash != self.baseline_hash
        return {
            "drifted": drifted,
            "baseline_hash": self.baseline_hash[:16],
            "current_hash": current_hash[:16],
            "last_check": self.last_check.isoformat()
        }


# ============================================================================
# COVERAGE MAP
# ============================================================================

class CoverageMap:
    """TIE-20 Component 10: Track triggered vs. missed doctrines."""

    def __init__(self):
        self.triggered = {}
        self.available = {block.topic: 0 for block in DOCTRINE_BLOCKS}

    def mark_triggered(self, topic: str):
        self.triggered[topic] = self.triggered.get(topic, 0) + 1
        self.available[topic] = self.available.get(topic, 0) + 1

    def get_coverage(self) -> Dict[str, Any]:
        total_topics = len(self.available)
        triggered_topics = len(self.triggered)
        coverage_pct = (triggered_topics / total_topics * 100) if total_topics > 0 else 0

        return {
            "total_topics": total_topics,
            "triggered_topics": triggered_topics,
            "coverage_percentage": round(coverage_pct, 2),
            "top_triggered": sorted(self.triggered.items(), key=lambda x: x[1], reverse=True)[:10],
            "never_triggered": [topic for topic in self.available if topic not in self.triggered]
        }


# ============================================================================
# AUDIT TRAIL
# ============================================================================

def append_audit_trail(query: Dict[str, Any], response: Dict[str, Any], latency_ms: float):
    """TIE-20 Component 15: Append-only audit trail in JSONL format."""
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "response": response,
        "latency_ms": latency_ms,
        "sha256": hashlib.sha256(json.dumps(response, sort_keys=True, default=str).encode()).hexdigest()
    }
    with open(AUDIT_TRAIL_PATH, "a") as f:
        f.write(json.dumps(record, default=str) + "\n")


# ============================================================================
# DISTRIBUTION CALCULATOR CORE
# ============================================================================

class DistributionCalculator:
    """Core estate distribution calculation engine."""

    def __init__(self):
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.coverage_map = CoverageMap()
        self.cloud_retriever = CloudRetriever() if CLOUD_AVAILABLE else None

    def calculate_distribution(self, request: DistributionRequest) -> DistributionResult:
        """
        TIE-20 Component 1: Three-layer response (doctrine cache, semantic, deep analysis).
        Main distribution calculation entry point.
        """
        start_time = datetime.utcnow()

        try:
            # Parse assets
            assets = [Asset(**a) for a in request.assets]
            total_estate_value = sum(a.fmv_at_death for a in assets)

            # Separate community and separate property (Texas)
            community_assets = [a for a in assets if a.property_type == PropertyType.COMMUNITY]
            separate_assets = [a for a in assets if a.property_type != PropertyType.COMMUNITY]

            # Community property division: surviving spouse gets 1/2
            if request.marital_status == "married" and community_assets:
                community_total = sum(a.fmv_at_death for a in community_assets)
                spouse_community_half = community_total / Decimal("2")
                decedent_community_half = community_total / Decimal("2")
                self.coverage_map.mark_triggered("community_property_division_at_death_texas")
            else:
                spouse_community_half = Decimal("0")
                decedent_community_half = Decimal("0")

            # Decedent's estate = separate property + 1/2 community
            separate_total = sum(a.fmv_at_death for a in separate_assets)
            decedent_estate_value = separate_total + decedent_community_half

            # Pay debts and expenses
            debts = [Debt(**d) for d in request.debts] if request.debts else []
            debts_sorted = sorted(debts, key=lambda d: d.priority)
            total_debts = sum(d.amount for d in debts)

            # Calculate executor commission (5% in/out)
            executor_commission = (decedent_estate_value + (decedent_estate_value - total_debts)) * Decimal("0.05")
            self.coverage_map.mark_triggered("executor_commissions_statutory_texas")

            # Attorney fees (estimated 5%, subject to reasonableness)
            attorney_fees = decedent_estate_value * Decimal("0.05")

            # Estate tax (simplified, would require full 706 calculation)
            estate_tax_exemption = Decimal("13610000")  # 2024 exemption
            taxable_estate = decedent_estate_value - estate_tax_exemption
            estate_tax = max(Decimal("0"), taxable_estate * Decimal("0.40"))  # 40% top rate

            # Net distributable after debts, expenses, commissions, taxes
            net_distributable = decedent_estate_value - total_debts - executor_commission - attorney_fees - estate_tax

            # Distribution calculation
            if request.has_will:
                distributions = self._calculate_testate_distribution(request, net_distributable, assets)
            else:
                distributions = self._calculate_intestate_distribution(request, net_distributable, assets)

            # Add spouse's community property half (not part of distribution, spouse already owns it)
            if spouse_community_half > 0:
                distributions.append({
                    "beneficiary": request.surviving_spouse,
                    "amount": float(spouse_community_half),
                    "source": "community_property_half",
                    "reasoning": "Surviving spouse's pre-existing 1/2 community property interest (not part of estate distribution)"
                })

            # Calculate determinism hash
            hash_input = json.dumps({
                "estate_id": request.estate_id,
                "assets": request.assets,
                "debts": request.debts,
                "bequests": request.bequests,
                "descendants": request.descendants
            }, sort_keys=True, default=str)
            sha256_hash = hashlib.sha256(hash_input.encode()).hexdigest()

            # Assemble response
            result = DistributionResult(
                estate_id=request.estate_id,
                timestamp=datetime.utcnow().isoformat(),
                total_estate_value=total_estate_value,
                total_debts=total_debts,
                net_distributable=net_distributable,
                distributions=distributions,
                estate_tax=estate_tax,
                income_tax=Decimal("0"),  # Would calculate DNI and beneficiary income tax
                executor_commission=executor_commission,
                attorney_fees=attorney_fees,
                confidence=ConfidenceLevel.DEFENSIBLE,
                reasoning=self._generate_reasoning(request, distributions),
                authorities_cited=self._gather_authorities(request),
                warnings=self._generate_warnings(request, net_distributable),
                sha256_hash=sha256_hash
            )

            # Record telemetry
            latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            self.telemetry.record_query("distribution_calculation", latency_ms, True)

            # Audit trail
            append_audit_trail(request.dict(), result.dict(), latency_ms)

            return result

        except Exception as e:
            logger.error(f"Distribution calculation failed: {e}")
            latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            self.telemetry.record_query("distribution_calculation", latency_ms, False, str(e))
            raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

    def _calculate_testate_distribution(self, request: DistributionRequest, net_distributable: Decimal, assets: List[Asset]) -> List[Dict[str, Any]]:
        """Calculate distribution per will provisions."""
        bequests = [Bequest(**b) for b in request.bequests]
        distributions = []

        # Calculate total specific and general bequests
        specific_total = sum(b.amount for b in bequests if b.bequest_type == BequestType.SPECIFIC and b.amount)
        general_total = sum(b.amount for b in bequests if b.bequest_type == BequestType.GENERAL and b.amount)

        # Check for abatement
        if (specific_total + general_total) > net_distributable:
            self.coverage_map.mark_triggered("abatement_order_specific_general_residuary")
            distributions = self._apply_abatement(bequests, net_distributable)
        else:
            # No abatement needed, pay all bequests
            for bequest in bequests:
                if bequest.bequest_type != BequestType.RESIDUARY:
                    distributions.append({
                        "beneficiary": bequest.beneficiary_name,
                        "amount": float(bequest.amount) if bequest.amount else 0,
                        "source": bequest.bequest_type.value,
                        "description": bequest.description,
                        "reasoning": f"{bequest.bequest_type.value} bequest per will"
                    })

            # Residuary gets remainder
            residuary_amount = net_distributable - specific_total - general_total
            residuary_bequests = [b for b in bequests if b.bequest_type == BequestType.RESIDUARY]
            if residuary_bequests:
                for res_bequest in residuary_bequests:
                    distributions.append({
                        "beneficiary": res_bequest.beneficiary_name,
                        "amount": float(residuary_amount / len(residuary_bequests)),
                        "source": "RESIDUARY",
                        "description": res_bequest.description,
                        "reasoning": "Residuary bequest - remainder after specific and general bequests paid"
                    })

        return distributions

    def _calculate_intestate_distribution(self, request: DistributionRequest, net_distributable: Decimal, assets: List[Asset]) -> List[Dict[str, Any]]:
        """Calculate distribution per Texas intestacy statutes."""
        distributions = []

        # Separate property vs. community property intestacy
        separate_assets = [a for a in assets if a.property_type != PropertyType.COMMUNITY]
        separate_total = sum(a.fmv_at_death for a in separate_assets)

        community_assets = [a for a in assets if a.property_type == PropertyType.COMMUNITY]
        community_total = sum(a.fmv_at_death for a in community_assets)
        decedent_community_half = community_total / Decimal("2")

        # Texas Estates Code §201.002 (separate property) and §201.003 (community property)
        if request.descendants:
            # DESCENDANTS EXIST: All separate property to descendants, community half to descendants or spouse based on parentage
            self.coverage_map.mark_triggered("separate_property_intestacy_texas_201_002")

            # Separate property: 100% to descendants
            desc_share_separate = self._distribute_by_representation(
                request.descendants,
                separate_total,
                request.distribution_method
            )

            # Community property half: check if all descendants are from current marriage
            all_from_current_marriage = all(d.get("from_current_marriage", True) for d in request.descendants)

            if all_from_current_marriage and request.surviving_spouse:
                # Spouse gets decedent's community half
                distributions.append({
                    "beneficiary": request.surviving_spouse,
                    "amount": float(decedent_community_half),
                    "source": "community_property_intestacy",
                    "reasoning": "Decedent's 1/2 community property - all descendants from current marriage (§201.003)"
                })
            else:
                # Descendants get decedent's community half
                desc_share_community = self._distribute_by_representation(
                    request.descendants,
                    decedent_community_half,
                    request.distribution_method
                )
                distributions.extend(desc_share_community)

            distributions.extend(desc_share_separate)

        elif request.surviving_spouse:
            # NO DESCENDANTS, SPOUSE EXISTS
            if request.marriage_years and request.marriage_years >= 10:
                # Married 10+ years: spouse gets 1/2 of separate property, parents/siblings get other 1/2 (if any)
                spouse_share = separate_total / Decimal("2")
                distributions.append({
                    "beneficiary": request.surviving_spouse,
                    "amount": float(spouse_share + decedent_community_half),
                    "source": "intestacy_spouse_10yr_rule",
                    "reasoning": "Spouse married 10+ years receives 1/2 separate property + entire community property half (§201.002)"
                })

                if request.parents_alive or request.siblings:
                    family_share = separate_total / Decimal("2")
                    distributions.append({
                        "beneficiary": "Parents/Siblings",
                        "amount": float(family_share),
                        "source": "intestacy_family_separate",
                        "reasoning": "Parents or siblings receive 1/2 separate property (§201.002)"
                    })
            else:
                # Married < 10 years: spouse gets life estate in separate realty from family, outright in other property
                distributions.append({
                    "beneficiary": request.surviving_spouse,
                    "amount": float(decedent_community_half),
                    "source": "community_property_intestacy",
                    "reasoning": "Spouse receives decedent's 1/2 community property (§201.003)"
                })

                # Separate property distribution depends on source
                distributions.append({
                    "beneficiary": request.surviving_spouse,
                    "amount": float(separate_total),
                    "source": "separate_property_intestacy",
                    "reasoning": "Spouse receives separate property subject to family land rules (§201.002)",
                    "warning": "If separate realty inherited from family, spouse gets life estate only; remainder to family"
                })

        else:
            # NO DESCENDANTS, NO SPOUSE: goes to parents, siblings, or extended family
            distributions.append({
                "beneficiary": "Parents or Siblings",
                "amount": float(net_distributable),
                "source": "intestacy_collateral",
                "reasoning": "No descendants or spouse - property to parents or siblings (§201.001)"
            })

        return distributions

    def _distribute_by_representation(self, descendants: List[Dict], amount: Decimal, method: DistributionMethod) -> List[Dict[str, Any]]:
        """Distribute amount among descendants by representation (per stirpes or per capita at each generation)."""
        if method == DistributionMethod.PER_STIRPES:
            self.coverage_map.mark_triggered("per_stirpes_distribution_methodology")
            return self._per_stirpes_distribution(descendants, amount)
        else:
            self.coverage_map.mark_triggered("per_capita_at_each_generation_modern_default")
            return self._per_capita_each_gen_distribution(descendants, amount)

    def _per_stirpes_distribution(self, descendants: List[Dict], amount: Decimal) -> List[Dict[str, Any]]:
        """Per stirpes distribution (divide at children level, subdivide within family lines)."""
        distributions = []

        # Count roots at first generation (children level)
        roots = [d for d in descendants if d.get("generation", 1) == 1]
        if not roots:
            return distributions

        share_per_root = amount / len(roots)

        for root in roots:
            if root.get("is_alive", False):
                distributions.append({
                    "beneficiary": root["name"],
                    "amount": float(share_per_root),
                    "source": "per_stirpes",
                    "reasoning": f"Per stirpes share (1/{len(roots)} of estate)"
                })
            else:
                # Root deceased, subdivide among their descendants
                root_descendants = root.get("descendants", [])
                if root_descendants:
                    share_per_desc = share_per_root / len(root_descendants)
                    for desc in root_descendants:
                        distributions.append({
                            "beneficiary": desc["name"],
                            "amount": float(share_per_desc),
                            "source": "per_stirpes_substitute",
                            "reasoning": f"Per stirpes - taking deceased parent {root['name']}'s share"
                        })

        return distributions

    def _per_capita_each_gen_distribution(self, descendants: List[Dict], amount: Decimal) -> List[Dict[str, Any]]:
        """Per capita at each generation (equal shares within each generation)."""
        distributions = []

        # Find nearest generation with living members
        all_descendants_flat = self._flatten_descendants(descendants)
        generations = {}
        for desc in all_descendants_flat:
            gen = desc.get("generation", 1)
            if gen not in generations:
                generations[gen] = []
            generations[gen].append(desc)

        # Start at first generation with living members or deceased with descendants
        for gen_num in sorted(generations.keys()):
            gen_members = generations[gen_num]
            living = [d for d in gen_members if d.get("is_alive", False)]
            deceased_with_desc = [d for d in gen_members if not d.get("is_alive", False) and d.get("descendants")]

            if living or deceased_with_desc:
                # This is the starting generation
                total_shares = len(living) + len(deceased_with_desc)
                share_amount = amount / total_shares

                # Give shares to living members
                for member in living:
                    distributions.append({
                        "beneficiary": member["name"],
                        "amount": float(share_amount),
                        "source": "per_capita_at_each_generation",
                        "reasoning": f"Per capita at each generation (1/{total_shares} of estate)"
                    })

                # Pool deceased members' shares for next generation
                if deceased_with_desc:
                    pooled_amount = share_amount * len(deceased_with_desc)
                    next_gen_members = []
                    for deceased in deceased_with_desc:
                        next_gen_members.extend(deceased.get("descendants", []))

                    if next_gen_members:
                        next_gen_share = pooled_amount / len(next_gen_members)
                        for ng_member in next_gen_members:
                            distributions.append({
                                "beneficiary": ng_member["name"],
                                "amount": float(next_gen_share),
                                "source": "per_capita_at_each_generation",
                                "reasoning": f"Per capita at each generation - next generation redistribution"
                            })

                break  # Stop after processing starting generation

        return distributions

    def _flatten_descendants(self, descendants: List[Dict]) -> List[Dict]:
        """Flatten nested descendants into single list."""
        flat = []
        for desc in descendants:
            flat.append(desc)
            if desc.get("descendants"):
                flat.extend(self._flatten_descendants(desc["descendants"]))
        return flat

    def _apply_abatement(self, bequests: List[Bequest], net_distributable: Decimal) -> List[Dict[str, Any]]:
        """Apply abatement when estate insufficient to pay all bequests."""
        distributions = []

        # Abatement order: specific (last to abate) -> demonstrative -> general -> residuary (first to abate)
        # Reverse for processing: pay in order residuary, general, demonstrative, specific

        residuary = [b for b in bequests if b.bequest_type == BequestType.RESIDUARY]
        general = [b for b in bequests if b.bequest_type == BequestType.GENERAL]
        demonstrative = [b for b in bequests if b.bequest_type == BequestType.DEMONSTRATIVE]
        specific = [b for b in bequests if b.bequest_type == BequestType.SPECIFIC]

        remaining = net_distributable

        # Specific bequests: pay first (last to abate)
        specific_total = sum(b.amount for b in specific if b.amount)
        if remaining >= specific_total:
            for beq in specific:
                distributions.append({
                    "beneficiary": beq.beneficiary_name,
                    "amount": float(beq.amount) if beq.amount else 0,
                    "source": "SPECIFIC",
                    "description": beq.description,
                    "reasoning": "Specific bequest paid in full (last to abate)"
                })
            remaining -= specific_total
        else:
            # Abate specific bequests pro rata
            abatement_factor = remaining / specific_total
            for beq in specific:
                paid_amount = (beq.amount if beq.amount else Decimal("0")) * abatement_factor
                distributions.append({
                    "beneficiary": beq.beneficiary_name,
                    "amount": float(paid_amount),
                    "source": "SPECIFIC_ABATED",
                    "description": beq.description,
                    "reasoning": f"Specific bequest abated to {float(abatement_factor * 100):.1f}% (insufficient assets)"
                })
            remaining = Decimal("0")

        # General bequests
        if remaining > 0:
            general_total = sum(b.amount for b in general if b.amount)
            if remaining >= general_total:
                for beq in general:
                    distributions.append({
                        "beneficiary": beq.beneficiary_name,
                        "amount": float(beq.amount) if beq.amount else 0,
                        "source": "GENERAL",
                        "description": beq.description,
                        "reasoning": "General bequest paid in full"
                    })
                remaining -= general_total
            else:
                # Abate general bequests pro rata
                abatement_factor = remaining / general_total if general_total > 0 else Decimal("0")
                for beq in general:
                    paid_amount = (beq.amount if beq.amount else Decimal("0")) * abatement_factor
                    distributions.append({
                        "beneficiary": beq.beneficiary_name,
                        "amount": float(paid_amount),
                        "source": "GENERAL_ABATED",
                        "description": beq.description,
                        "reasoning": f"General bequest abated to {float(abatement_factor * 100):.1f}% (insufficient assets)"
                    })
                remaining = Decimal("0")

        # Residuary gets whatever is left (usually nothing after abatement)
        if remaining > 0 and residuary:
            for beq in residuary:
                distributions.append({
                    "beneficiary": beq.beneficiary_name,
                    "amount": float(remaining / len(residuary)),
                    "source": "RESIDUARY",
                    "description": beq.description,
                    "reasoning": "Residuary bequest - minimal remainder after abatement"
                })

        return distributions

    def _generate_reasoning(self, request: DistributionRequest, distributions: List[Dict]) -> str:
        """Generate reasoning explanation for distribution."""
        reasoning_parts = []

        if request.has_will:
            reasoning_parts.append("Estate distributed per will provisions.")
            if any("ABATED" in d.get("source", "") for d in distributions):
                reasoning_parts.append("Abatement applied due to insufficient assets (specific -> general -> residuary hierarchy).")
        else:
            reasoning_parts.append(f"Estate distributed per Texas intestacy statutes (§201.001-201.003).")
            if request.descendants:
                reasoning_parts.append("Descendants exist - separate property to descendants, community property based on parentage.")
            elif request.surviving_spouse:
                reasoning_parts.append("No descendants - surviving spouse receives distributions subject to family land rules and marriage duration.")

        if request.marital_status == "married":
            reasoning_parts.append("Community property divided: surviving spouse retains 1/2, decedent's 1/2 distributed per will/intestacy.")

        reasoning_parts.append(f"Executor commission calculated at statutory 5% (receipts + disbursements).")
        reasoning_parts.append(f"Distribution method: {request.distribution_method.value}")

        return " ".join(reasoning_parts)

    def _gather_authorities(self, request: DistributionRequest) -> List[str]:
        """Gather relevant statutory and case law authorities."""
        authorities = [
            "Texas Estates Code §201.001-201.003 (intestate succession)",
            "Texas Estates Code §255.001-.406 (will provisions and interpretation)",
            "Texas Estates Code §352.001-.003 (executor compensation)",
            "Texas Family Code §3.001-3.007 (community property)",
        ]

        if request.has_will:
            authorities.append("UPC §3-902 (abatement)")
            authorities.append("Texas Estates Code §355.109 (abatement order)")

        authorities.extend([
            "IRC §2001-2209 (estate tax)",
            "IRC §641-685 (fiduciary income taxation)",
            "IRC §2056 (marital deduction)"
        ])

        return authorities

    def _generate_warnings(self, request: DistributionRequest, net_distributable: Decimal) -> List[str]:
        """Generate warnings about distribution risks and considerations."""
        warnings = []

        if net_distributable <= 0:
            warnings.append("Estate is insolvent (debts exceed assets) - creditors may not be paid in full")

        if request.marital_status == "married" and not request.marriage_years:
            warnings.append("Marriage duration not specified - affects separate property distribution under 10-year rule")

        if request.has_will and not request.bequests:
            warnings.append("Will indicated but no bequests provided - distribution may default to intestacy")

        warnings.append("Subject to court approval and creditor claim periods")
        warnings.append("Tax consequences depend on timing, elections, and final valuations")
        warnings.append("Beneficiary disclaimers can alter final distributions")

        return warnings

    def health_check(self) -> Dict[str, Any]:
        """TIE-20 Component 12: Health endpoint."""
        return {
            "engine_id": ENGINE_ID,
            "version": VERSION,
            "status": "healthy",
            "doctrine_topics": len(DOCTRINE_BLOCKS),
            "telemetry": self.telemetry.get_stats(),
            "drift": self.drift_watcher.check_drift(),
            "coverage": self.coverage_map.get_coverage(),
            "cloud_available": CLOUD_AVAILABLE
        }


# ============================================================================
# FASTAPI APPLICATION (TIE-20 Component 17)
# ============================================================================

app = FastAPI(
    title="P06 Distribution Calculator",
    description="Estate distribution calculation engine - TIE-20 compliant",
    version=VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize calculator
calculator = DistributionCalculator()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "engine": ENGINE_ID,
        "version": VERSION,
        "status": "operational",
        "endpoints": ["/calculate", "/health", "/doctrines", "/config"]
    }


@app.post("/calculate")
async def calculate_distribution(request: DistributionRequest):
    """Main distribution calculation endpoint."""
    logger.info(f"Distribution calculation request: estate_id={request.estate_id}")
    result = calculator.calculate_distribution(request)
    return result


@app.get("/health")
async def health():
    """Health check endpoint."""
    return calculator.health_check()


@app.get("/doctrines")
async def get_doctrines(keyword: Optional[str] = None):
    """Retrieve doctrine blocks."""
    if keyword:
        results = search_doctrines_by_keyword(keyword)
        return {"keyword": keyword, "results": [asdict(block) for block in results]}
    return {"total": len(DOCTRINE_BLOCKS), "doctrines": [block.topic for block in DOCTRINE_BLOCKS]}


@app.get("/doctrines/{topic}")
async def get_doctrine(topic: str):
    """Retrieve specific doctrine block."""
    block = get_doctrine_by_topic(topic)
    if not block:
        raise HTTPException(status_code=404, detail=f"Doctrine topic '{topic}' not found")
    return asdict(block)


@app.get("/config")
async def get_config():
    """Retrieve engine configuration."""
    return CONFIG


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_ID} v{VERSION} on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
