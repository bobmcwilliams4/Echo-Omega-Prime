"""
LM13 Water Rights Analyzer - Search Engine
=============================================

Full-featured search engine for water rights data including permits,
aquifers, operators, well types, locations, and compliance records.

Supports multi-field search, geo-spatial filtering, temporal queries,
and aggregation across water rights datasets.

Author: ECHO OMEGA PRIME Build System
Engine: LM13 v1.0.0
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class WaterRightType(str, Enum):
    """Water right / permit type classification."""
    SURFACE_WATER_APPROPRIATION = "surface_water_appropriation"
    GCD_PRODUCTION_PERMIT = "gcd_production_permit"
    GCD_EXPORT_PERMIT = "gcd_export_permit"
    INJECTION_WELL_H1 = "injection_well_h1"
    INJECTION_WELL_EOR = "injection_well_eor"
    TPDES_DISCHARGE = "tpdes_discharge"
    EDWARDS_AQUIFER = "edwards_aquifer"
    TEMPORARY_PERMIT = "temporary_permit"
    EMERGENCY_AUTHORIZATION = "emergency_authorization"
    WATER_TRANSPORT = "water_transport"
    BED_AND_BANKS = "bed_and_banks"
    RECYCLING_FACILITY = "recycling_facility"
    BRACKISH_DESALINATION = "brackish_desalination"


class WellType(str, Enum):
    """Well classification for search filtering."""
    DISPOSAL_SWD = "disposal_swd"
    INJECTION_EOR = "injection_eor"
    WATER_SUPPLY = "water_supply"
    MONITORING = "monitoring"
    DOMESTIC = "domestic"
    IRRIGATION = "irrigation"
    INDUSTRIAL = "industrial"
    MUNICIPAL = "municipal"
    PLUGGED = "plugged"
    ABANDONED = "abandoned"


class AquiferName(str, Enum):
    """Major aquifer names for search indexing."""
    OGALLALA = "Ogallala"
    PECOS_VALLEY = "Pecos Valley"
    EDWARDS_TRINITY = "Edwards-Trinity (Plateau)"
    DOCKUM = "Dockum"
    RUSTLER = "Rustler"
    SANTA_ROSA = "Santa Rosa"
    EDWARDS = "Edwards"
    GULF_COAST = "Gulf Coast"
    ELLENBURGER = "Ellenburger"
    DELAWARE_MTN = "Delaware Mountain Group"
    SAN_ANDRES = "San Andres"
    CAPITAN_REEF = "Capitan Reef Complex"
    CENOZOIC_ALLUVIUM = "Cenozoic Alluvium"


class ComplianceStatus(str, Enum):
    """Compliance status for search filtering."""
    COMPLIANT = "compliant"
    MINOR_VIOLATION = "minor_violation"
    MAJOR_VIOLATION = "major_violation"
    ENFORCEMENT_ACTION = "enforcement_action"
    PERMIT_SUSPENDED = "permit_suspended"
    PERMIT_REVOKED = "permit_revoked"
    UNDER_REVIEW = "under_review"
    NOT_ASSESSED = "not_assessed"


class SortField(str, Enum):
    """Available sort fields."""
    RELEVANCE = "relevance"
    DATE_ISSUED = "date_issued"
    DATE_EXPIRES = "date_expires"
    OPERATOR_NAME = "operator_name"
    COUNTY = "county"
    PERMIT_NUMBER = "permit_number"
    VOLUME = "volume"
    COMPLIANCE_SCORE = "compliance_score"
    DISTANCE = "distance"


class SortOrder(str, Enum):
    """Sort direction."""
    ASC = "asc"
    DESC = "desc"


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class GeoCoordinate:
    """Geographic coordinate for spatial search."""
    latitude: float
    longitude: float

    def validate(self) -> bool:
        """Validate coordinate ranges."""
        return -90.0 <= self.latitude <= 90.0 and -180.0 <= self.longitude <= 180.0

    def distance_miles(self, other: GeoCoordinate) -> float:
        """Calculate approximate distance in miles using Haversine formula."""
        import math
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        earth_radius_miles = 3959.0
        return earth_radius_miles * c


@dataclass
class BoundingBox:
    """Geographic bounding box for area search."""
    north: float
    south: float
    east: float
    west: float

    def contains(self, coord: GeoCoordinate) -> bool:
        """Check if a coordinate falls within this bounding box."""
        return (self.south <= coord.latitude <= self.north and
                self.west <= coord.longitude <= self.east)

    def validate(self) -> bool:
        return self.south < self.north and self.west < self.east


@dataclass
class DateRange:
    """Date range for temporal search."""
    start: Optional[date] = None
    end: Optional[date] = None

    def contains(self, check_date: date) -> bool:
        """Check if a date falls within this range."""
        if self.start and check_date < self.start:
            return False
        if self.end and check_date > self.end:
            return False
        return True


@dataclass
class VolumeRange:
    """Volume range for filtering."""
    min_bbls_per_day: Optional[float] = None
    max_bbls_per_day: Optional[float] = None
    min_af_per_year: Optional[float] = None
    max_af_per_year: Optional[float] = None


@dataclass
class WaterSearchQuery:
    """Comprehensive search query for water rights data."""
    # Text search
    text_query: Optional[str] = None
    # Specific filters
    permit_number: Optional[str] = None
    permit_type: Optional[WaterRightType] = None
    well_type: Optional[WellType] = None
    aquifer: Optional[AquiferName] = None
    operator_name: Optional[str] = None
    operator_rrc_id: Optional[str] = None
    county: Optional[str] = None
    gcd_name: Optional[str] = None
    compliance_status: Optional[ComplianceStatus] = None
    # Spatial search
    location: Optional[GeoCoordinate] = None
    radius_miles: Optional[float] = None
    bounding_box: Optional[BoundingBox] = None
    # Temporal search
    issued_date_range: Optional[DateRange] = None
    expiration_date_range: Optional[DateRange] = None
    last_mit_date_range: Optional[DateRange] = None
    # Volume filters
    volume_range: Optional[VolumeRange] = None
    # Pagination and sorting
    sort_by: SortField = SortField.RELEVANCE
    sort_order: SortOrder = SortOrder.DESC
    page: int = 1
    page_size: int = 50
    max_results: int = 1000
    # Options
    include_expired: bool = False
    include_plugged: bool = False
    include_related: bool = True
    highlight_matches: bool = True

    def compute_hash(self) -> str:
        """Deterministic hash of the query for caching."""
        content = json.dumps({
            "text": self.text_query,
            "permit": self.permit_number,
            "type": self.permit_type.value if self.permit_type else None,
            "well_type": self.well_type.value if self.well_type else None,
            "aquifer": self.aquifer.value if self.aquifer else None,
            "operator": self.operator_name,
            "county": self.county,
            "compliance": self.compliance_status.value if self.compliance_status else None,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class WaterPermitRecord:
    """A single water permit / right record in the search index."""
    record_id: str
    permit_number: str
    permit_type: WaterRightType
    well_type: Optional[WellType] = None
    operator_name: str = ""
    operator_rrc_id: str = ""
    lease_name: str = ""
    well_number: str = ""
    api_number: str = ""
    county: str = ""
    state: str = "TX"
    gcd_name: str = ""
    aquifer: str = ""
    formation: str = ""
    location: Optional[GeoCoordinate] = None
    legal_description: str = ""
    date_issued: Optional[date] = None
    date_expires: Optional[date] = None
    status: str = "active"
    compliance_status: ComplianceStatus = ComplianceStatus.NOT_ASSESSED
    compliance_score: float = 100.0
    authorized_volume_bbls_per_day: float = 0.0
    authorized_volume_af_per_year: float = 0.0
    actual_volume_bbls_per_day: float = 0.0
    max_injection_pressure_psi: float = 0.0
    injection_zone_depth_ft: float = 0.0
    surface_casing_depth_ft: float = 0.0
    last_mit_date: Optional[date] = None
    last_mit_result: str = ""
    violations: list[str] = field(default_factory=list)
    notes: str = ""
    source_url: str = ""
    data_hash: str = ""

    def compute_hash(self) -> str:
        """Compute deterministic hash of record content."""
        content = json.dumps({
            "id": self.record_id,
            "permit": self.permit_number,
            "operator": self.operator_name,
            "county": self.county,
            "aquifer": self.aquifer,
            "status": self.status,
        }, sort_keys=True)
        self.data_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.data_hash

    def is_expired(self) -> bool:
        """Check if the permit has expired."""
        if not self.date_expires:
            return False
        return self.date_expires < date.today()

    def days_until_expiry(self) -> Optional[int]:
        """Days until permit expiration, or None if no expiry date."""
        if not self.date_expires:
            return None
        delta = self.date_expires - date.today()
        return delta.days


@dataclass
class WaterSearchResult:
    """Single search result with scoring and highlighting."""
    record: WaterPermitRecord
    relevance_score: float = 0.0
    distance_miles: Optional[float] = None
    matched_fields: list[str] = field(default_factory=list)
    highlights: dict[str, str] = field(default_factory=dict)
    related_records: list[str] = field(default_factory=list)


@dataclass
class WaterSearchResponse:
    """Complete search response with results and metadata."""
    query_hash: str
    total_results: int
    page: int
    page_size: int
    total_pages: int
    results: list[WaterSearchResult]
    facets: dict[str, dict[str, int]] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Index structures
# ---------------------------------------------------------------------------

class PermitIndex:
    """Index of permits by permit number for O(1) lookup."""

    def __init__(self) -> None:
        self._index: dict[str, WaterPermitRecord] = {}
        self._prefix_index: dict[str, list[str]] = {}
        logger.info("PermitIndex initialized")

    def add(self, record: WaterPermitRecord) -> None:
        """Add a record to the permit index."""
        key = record.permit_number.strip().upper()
        self._index[key] = record
        prefix = key[:4] if len(key) >= 4 else key
        self._prefix_index.setdefault(prefix, []).append(key)

    def get(self, permit_number: str) -> Optional[WaterPermitRecord]:
        """Get a record by exact permit number."""
        return self._index.get(permit_number.strip().upper())

    def search_prefix(self, prefix: str) -> list[WaterPermitRecord]:
        """Search by permit number prefix."""
        prefix_upper = prefix.strip().upper()
        matching_keys: list[str] = []
        for pfx, keys in self._prefix_index.items():
            if pfx.startswith(prefix_upper):
                matching_keys.extend(keys)
        return [self._index[k] for k in matching_keys if k in self._index]

    def search_pattern(self, pattern: str) -> list[WaterPermitRecord]:
        """Search by regex pattern against permit numbers."""
        try:
            compiled = re.compile(pattern, re.IGNORECASE)
        except re.error:
            logger.warning("Invalid regex pattern: {}", pattern)
            return []
        return [
            record for key, record in self._index.items()
            if compiled.search(key)
        ]

    def count(self) -> int:
        return len(self._index)

    def all_permits(self) -> list[str]:
        return sorted(self._index.keys())


class AquiferIndex:
    """Index of records by aquifer name for faceted search."""

    def __init__(self) -> None:
        self._index: dict[str, list[str]] = {}
        self._records: dict[str, WaterPermitRecord] = {}
        logger.info("AquiferIndex initialized")

    def add(self, record: WaterPermitRecord) -> None:
        """Add a record to the aquifer index."""
        aquifer_key = record.aquifer.strip().lower()
        if aquifer_key:
            self._index.setdefault(aquifer_key, []).append(record.record_id)
            self._records[record.record_id] = record

    def get_by_aquifer(self, aquifer_name: str) -> list[WaterPermitRecord]:
        """Get all records for a specific aquifer."""
        key = aquifer_name.strip().lower()
        record_ids = self._index.get(key, [])
        return [self._records[rid] for rid in record_ids if rid in self._records]

    def search_aquifer(self, query: str) -> list[WaterPermitRecord]:
        """Search across aquifer names with partial matching."""
        query_lower = query.lower()
        results: list[WaterPermitRecord] = []
        seen: set[str] = set()
        for aquifer_key, record_ids in self._index.items():
            if query_lower in aquifer_key:
                for rid in record_ids:
                    if rid not in seen and rid in self._records:
                        results.append(self._records[rid])
                        seen.add(rid)
        return results

    def get_aquifer_counts(self) -> dict[str, int]:
        """Get record count per aquifer for faceting."""
        return {k: len(v) for k, v in sorted(self._index.items())}

    def count(self) -> int:
        return sum(len(v) for v in self._index.values())


class OperatorIndex:
    """Index of records by operator name / RRC ID."""

    def __init__(self) -> None:
        self._name_index: dict[str, list[str]] = {}
        self._rrc_id_index: dict[str, list[str]] = {}
        self._records: dict[str, WaterPermitRecord] = {}
        logger.info("OperatorIndex initialized")

    def add(self, record: WaterPermitRecord) -> None:
        """Add a record to the operator index."""
        name_key = record.operator_name.strip().lower()
        if name_key:
            self._name_index.setdefault(name_key, []).append(record.record_id)
        rrc_key = record.operator_rrc_id.strip()
        if rrc_key:
            self._rrc_id_index.setdefault(rrc_key, []).append(record.record_id)
        self._records[record.record_id] = record

    def get_by_name(self, name: str) -> list[WaterPermitRecord]:
        """Get all records for a specific operator name (exact match)."""
        key = name.strip().lower()
        record_ids = self._name_index.get(key, [])
        return [self._records[rid] for rid in record_ids if rid in self._records]

    def get_by_rrc_id(self, rrc_id: str) -> list[WaterPermitRecord]:
        """Get all records by RRC operator ID."""
        record_ids = self._rrc_id_index.get(rrc_id.strip(), [])
        return [self._records[rid] for rid in record_ids if rid in self._records]

    def search_name(self, query: str) -> list[WaterPermitRecord]:
        """Search operator names with partial matching."""
        query_lower = query.lower()
        results: list[WaterPermitRecord] = []
        seen: set[str] = set()
        for name_key, record_ids in self._name_index.items():
            if query_lower in name_key:
                for rid in record_ids:
                    if rid not in seen and rid in self._records:
                        results.append(self._records[rid])
                        seen.add(rid)
        return results

    def get_operator_counts(self) -> dict[str, int]:
        """Get record count per operator for faceting."""
        return {k: len(v) for k, v in sorted(self._name_index.items())}

    def count(self) -> int:
        return len(self._records)


class CountyIndex:
    """Index of records by county for geographic filtering."""

    def __init__(self) -> None:
        self._index: dict[str, list[str]] = {}
        self._records: dict[str, WaterPermitRecord] = {}
        logger.info("CountyIndex initialized")

    def add(self, record: WaterPermitRecord) -> None:
        county_key = record.county.strip().lower()
        if county_key:
            self._index.setdefault(county_key, []).append(record.record_id)
            self._records[record.record_id] = record

    def get_by_county(self, county: str) -> list[WaterPermitRecord]:
        key = county.strip().lower()
        record_ids = self._index.get(key, [])
        return [self._records[rid] for rid in record_ids if rid in self._records]

    def get_county_counts(self) -> dict[str, int]:
        return {k: len(v) for k, v in sorted(self._index.items())}

    def count(self) -> int:
        return sum(len(v) for v in self._index.values())


class WellTypeIndex:
    """Index of records by well type."""

    def __init__(self) -> None:
        self._index: dict[str, list[str]] = {}
        self._records: dict[str, WaterPermitRecord] = {}
        logger.info("WellTypeIndex initialized")

    def add(self, record: WaterPermitRecord) -> None:
        if record.well_type:
            key = record.well_type.value
            self._index.setdefault(key, []).append(record.record_id)
            self._records[record.record_id] = record

    def get_by_type(self, well_type: WellType) -> list[WaterPermitRecord]:
        record_ids = self._index.get(well_type.value, [])
        return [self._records[rid] for rid in record_ids if rid in self._records]

    def get_type_counts(self) -> dict[str, int]:
        return {k: len(v) for k, v in sorted(self._index.items())}


class ComplianceIndex:
    """Index of records by compliance status."""

    def __init__(self) -> None:
        self._index: dict[str, list[str]] = {}
        self._records: dict[str, WaterPermitRecord] = {}
        logger.info("ComplianceIndex initialized")

    def add(self, record: WaterPermitRecord) -> None:
        key = record.compliance_status.value
        self._index.setdefault(key, []).append(record.record_id)
        self._records[record.record_id] = record

    def get_by_status(self, status: ComplianceStatus) -> list[WaterPermitRecord]:
        record_ids = self._index.get(status.value, [])
        return [self._records[rid] for rid in record_ids if rid in self._records]

    def get_status_counts(self) -> dict[str, int]:
        return {k: len(v) for k, v in sorted(self._index.items())}


# ---------------------------------------------------------------------------
# Main search engine
# ---------------------------------------------------------------------------

class WaterRightsSearchEngine:
    """Multi-index search engine for water rights data."""

    def __init__(self) -> None:
        self._all_records: dict[str, WaterPermitRecord] = {}
        self.permit_index = PermitIndex()
        self.aquifer_index = AquiferIndex()
        self.operator_index = OperatorIndex()
        self._county_index = CountyIndex()
        self._well_type_index = WellTypeIndex()
        self._compliance_index = ComplianceIndex()
        self._spatial_records: list[tuple[GeoCoordinate, str]] = []
        logger.info("WaterRightsSearchEngine initialized")

    def index_record(self, record: WaterPermitRecord) -> None:
        """Add a record to all indexes."""
        record.compute_hash()
        self._all_records[record.record_id] = record
        self.permit_index.add(record)
        self.aquifer_index.add(record)
        self.operator_index.add(record)
        self._county_index.add(record)
        self._well_type_index.add(record)
        self._compliance_index.add(record)
        if record.location and record.location.validate():
            self._spatial_records.append((record.location, record.record_id))
        logger.debug("Indexed record: {} ({})", record.record_id, record.permit_number)

    def index_batch(self, records: list[WaterPermitRecord]) -> int:
        """Index multiple records. Returns count indexed."""
        count = 0
        for record in records:
            self.index_record(record)
            count += 1
        logger.info("Batch indexed {} records (total: {})", count, len(self._all_records))
        return count

    def search(self, query: WaterSearchQuery) -> WaterSearchResponse:
        """Execute a search query against all indexes."""
        start_time = datetime.now(timezone.utc)
        query_hash = query.compute_hash()
        candidates: Optional[set[str]] = None

        # Apply specific filters to narrow candidates
        if query.permit_number:
            record = self.permit_index.get(query.permit_number)
            if record:
                candidates = {record.record_id}
            else:
                prefix_results = self.permit_index.search_prefix(query.permit_number)
                candidates = {r.record_id for r in prefix_results}

        if query.aquifer:
            aquifer_records = self.aquifer_index.get_by_aquifer(query.aquifer.value)
            aquifer_ids = {r.record_id for r in aquifer_records}
            candidates = aquifer_ids if candidates is None else candidates & aquifer_ids

        if query.operator_name:
            op_records = self.operator_index.search_name(query.operator_name)
            op_ids = {r.record_id for r in op_records}
            candidates = op_ids if candidates is None else candidates & op_ids

        if query.operator_rrc_id:
            rrc_records = self.operator_index.get_by_rrc_id(query.operator_rrc_id)
            rrc_ids = {r.record_id for r in rrc_records}
            candidates = rrc_ids if candidates is None else candidates & rrc_ids

        if query.county:
            county_records = self._county_index.get_by_county(query.county)
            county_ids = {r.record_id for r in county_records}
            candidates = county_ids if candidates is None else candidates & county_ids

        if query.well_type:
            wt_records = self._well_type_index.get_by_type(query.well_type)
            wt_ids = {r.record_id for r in wt_records}
            candidates = wt_ids if candidates is None else candidates & wt_ids

        if query.compliance_status:
            comp_records = self._compliance_index.get_by_status(query.compliance_status)
            comp_ids = {r.record_id for r in comp_records}
            candidates = comp_ids if candidates is None else candidates & comp_ids

        # If no specific filters, start with all records
        if candidates is None:
            candidates = set(self._all_records.keys())

        # Apply text search scoring
        scored_results: list[WaterSearchResult] = []
        for rid in candidates:
            record = self._all_records.get(rid)
            if not record:
                continue

            # Skip expired unless requested
            if not query.include_expired and record.is_expired():
                continue

            # Skip plugged unless requested
            if not query.include_plugged and record.well_type in (WellType.PLUGGED, WellType.ABANDONED):
                continue

            # Apply permit type filter
            if query.permit_type and record.permit_type != query.permit_type:
                continue

            # Apply GCD filter
            if query.gcd_name and query.gcd_name.lower() not in record.gcd_name.lower():
                continue

            # Apply date range filters
            if query.issued_date_range and record.date_issued:
                if not query.issued_date_range.contains(record.date_issued):
                    continue

            if query.expiration_date_range and record.date_expires:
                if not query.expiration_date_range.contains(record.date_expires):
                    continue

            if query.last_mit_date_range and record.last_mit_date:
                if not query.last_mit_date_range.contains(record.last_mit_date):
                    continue

            # Apply volume range filter
            if query.volume_range:
                vr = query.volume_range
                if vr.min_bbls_per_day and record.authorized_volume_bbls_per_day < vr.min_bbls_per_day:
                    continue
                if vr.max_bbls_per_day and record.authorized_volume_bbls_per_day > vr.max_bbls_per_day:
                    continue
                if vr.min_af_per_year and record.authorized_volume_af_per_year < vr.min_af_per_year:
                    continue
                if vr.max_af_per_year and record.authorized_volume_af_per_year > vr.max_af_per_year:
                    continue

            # Apply spatial filters
            distance = None
            if query.location and query.radius_miles and record.location:
                distance = query.location.distance_miles(record.location)
                if distance > query.radius_miles:
                    continue

            if query.bounding_box and record.location:
                if not query.bounding_box.contains(record.location):
                    continue

            # Compute relevance score
            score = 0.0
            matched_fields: list[str] = []
            highlights: dict[str, str] = {}

            if query.text_query:
                text_lower = query.text_query.lower()
                searchable_fields = {
                    "permit_number": record.permit_number,
                    "operator_name": record.operator_name,
                    "lease_name": record.lease_name,
                    "county": record.county,
                    "aquifer": record.aquifer,
                    "formation": record.formation,
                    "gcd_name": record.gcd_name,
                    "notes": record.notes,
                    "legal_description": record.legal_description,
                }
                for field_name, field_value in searchable_fields.items():
                    if text_lower in field_value.lower():
                        if field_name == "permit_number":
                            score += 20.0
                        elif field_name == "operator_name":
                            score += 15.0
                        elif field_name in ("county", "aquifer"):
                            score += 10.0
                        else:
                            score += 5.0
                        matched_fields.append(field_name)
                        if query.highlight_matches:
                            idx = field_value.lower().find(text_lower)
                            if idx >= 0:
                                match_text = field_value[idx:idx + len(query.text_query)]
                                highlights[field_name] = field_value.replace(
                                    match_text, f"**{match_text}**"
                                )
            else:
                score = 10.0  # base score for filter-only queries

            # Boost score for compliance issues
            if record.compliance_status in (ComplianceStatus.MAJOR_VIOLATION,
                                           ComplianceStatus.ENFORCEMENT_ACTION):
                score += 5.0

            # Boost for proximity
            if distance is not None:
                proximity_boost = max(0, 10.0 - distance)
                score += proximity_boost

            result = WaterSearchResult(
                record=record,
                relevance_score=score,
                distance_miles=distance,
                matched_fields=matched_fields,
                highlights=highlights,
            )
            scored_results.append(result)

        # Sort results
        if query.sort_by == SortField.RELEVANCE:
            scored_results.sort(key=lambda r: r.relevance_score, reverse=(query.sort_order == SortOrder.DESC))
        elif query.sort_by == SortField.DATE_ISSUED:
            scored_results.sort(
                key=lambda r: r.record.date_issued or date.min,
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.DATE_EXPIRES:
            scored_results.sort(
                key=lambda r: r.record.date_expires or date.min,
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.OPERATOR_NAME:
            scored_results.sort(
                key=lambda r: r.record.operator_name.lower(),
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.COUNTY:
            scored_results.sort(
                key=lambda r: r.record.county.lower(),
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.VOLUME:
            scored_results.sort(
                key=lambda r: r.record.authorized_volume_bbls_per_day,
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.COMPLIANCE_SCORE:
            scored_results.sort(
                key=lambda r: r.record.compliance_score,
                reverse=(query.sort_order == SortOrder.DESC),
            )
        elif query.sort_by == SortField.DISTANCE:
            scored_results.sort(
                key=lambda r: r.distance_miles if r.distance_miles is not None else float('inf'),
                reverse=(query.sort_order == SortOrder.DESC),
            )

        # Apply max results cap
        total_results = len(scored_results)
        if total_results > query.max_results:
            scored_results = scored_results[:query.max_results]
            total_results = query.max_results

        # Paginate
        total_pages = max(1, (total_results + query.page_size - 1) // query.page_size)
        start_idx = (query.page - 1) * query.page_size
        end_idx = start_idx + query.page_size
        page_results = scored_results[start_idx:end_idx]

        # Build facets
        facets = self._build_facets(scored_results)

        end_time = datetime.now(timezone.utc)
        execution_time_ms = (end_time - start_time).total_seconds() * 1000

        response = WaterSearchResponse(
            query_hash=query_hash,
            total_results=total_results,
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages,
            results=page_results,
            facets=facets,
            execution_time_ms=execution_time_ms,
        )

        logger.info(
            "Search completed: {} results in {:.1f}ms (query_hash={})",
            total_results, execution_time_ms, query_hash,
        )
        return response

    def _build_facets(self, results: list[WaterSearchResult]) -> dict[str, dict[str, int]]:
        """Build facet counts from search results."""
        facets: dict[str, dict[str, int]] = {
            "county": {},
            "aquifer": {},
            "well_type": {},
            "permit_type": {},
            "compliance_status": {},
            "operator": {},
        }
        for result in results:
            record = result.record
            if record.county:
                facets["county"][record.county] = facets["county"].get(record.county, 0) + 1
            if record.aquifer:
                facets["aquifer"][record.aquifer] = facets["aquifer"].get(record.aquifer, 0) + 1
            if record.well_type:
                wt = record.well_type.value
                facets["well_type"][wt] = facets["well_type"].get(wt, 0) + 1
            pt = record.permit_type.value
            facets["permit_type"][pt] = facets["permit_type"].get(pt, 0) + 1
            cs = record.compliance_status.value
            facets["compliance_status"][cs] = facets["compliance_status"].get(cs, 0) + 1
            if record.operator_name:
                facets["operator"][record.operator_name] = (
                    facets["operator"].get(record.operator_name, 0) + 1
                )
        return facets

    def get_nearby_records(
        self,
        location: GeoCoordinate,
        radius_miles: float,
        well_type: Optional[WellType] = None,
        max_results: int = 100,
    ) -> list[tuple[WaterPermitRecord, float]]:
        """Get records within a radius of a location, sorted by distance."""
        results: list[tuple[WaterPermitRecord, float]] = []
        for coord, rid in self._spatial_records:
            distance = location.distance_miles(coord)
            if distance <= radius_miles:
                record = self._all_records.get(rid)
                if record:
                    if well_type and record.well_type != well_type:
                        continue
                    results.append((record, distance))
        results.sort(key=lambda x: x[1])
        return results[:max_results]

    def get_expiring_permits(self, days_ahead: int = 90) -> list[WaterPermitRecord]:
        """Get permits expiring within the specified number of days."""
        cutoff = date.today()
        results: list[WaterPermitRecord] = []
        for record in self._all_records.values():
            remaining = record.days_until_expiry()
            if remaining is not None and 0 <= remaining <= days_ahead:
                results.append(record)
        results.sort(key=lambda r: r.date_expires or date.max)
        logger.info("Found {} permits expiring within {} days", len(results), days_ahead)
        return results

    def get_mit_due(self, days_overdue: int = 0) -> list[WaterPermitRecord]:
        """Get injection wells with MIT due or overdue."""
        results: list[WaterPermitRecord] = []
        five_years_ago = date.today().replace(year=date.today().year - 5)
        for record in self._all_records.values():
            if record.well_type not in (WellType.DISPOSAL_SWD, WellType.INJECTION_EOR):
                continue
            if record.last_mit_date and record.last_mit_date < five_years_ago:
                results.append(record)
            elif not record.last_mit_date:
                results.append(record)
        logger.info("Found {} wells with MIT due/overdue", len(results))
        return results

    def get_compliance_summary(self) -> dict[str, Any]:
        """Get overall compliance summary across all indexed records."""
        summary: dict[str, int] = {}
        for record in self._all_records.values():
            status = record.compliance_status.value
            summary[status] = summary.get(status, 0) + 1
        return {
            "total_records": len(self._all_records),
            "status_counts": summary,
            "avg_compliance_score": (
                sum(r.compliance_score for r in self._all_records.values()) /
                max(len(self._all_records), 1)
            ),
            "records_with_violations": sum(
                1 for r in self._all_records.values() if r.violations
            ),
        }

    def export_results(self, results: list[WaterSearchResult], output_path: Path) -> int:
        """Export search results to JSON file."""
        export_data = {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "total_results": len(results),
            "results": [
                {
                    "record_id": r.record.record_id,
                    "permit_number": r.record.permit_number,
                    "operator": r.record.operator_name,
                    "county": r.record.county,
                    "aquifer": r.record.aquifer,
                    "well_type": r.record.well_type.value if r.record.well_type else None,
                    "compliance_status": r.record.compliance_status.value,
                    "compliance_score": r.record.compliance_score,
                    "relevance_score": r.relevance_score,
                    "distance_miles": r.distance_miles,
                }
                for r in results
            ],
        }
        output_path.write_text(json.dumps(export_data, indent=2))
        logger.info("Exported {} results to {}", len(results), output_path)
        return len(results)

    def get_statistics(self) -> dict[str, Any]:
        """Return summary statistics of the search engine."""
        return {
            "total_records": len(self._all_records),
            "permit_index_size": self.permit_index.count(),
            "aquifer_index_size": self.aquifer_index.count(),
            "operator_index_size": self.operator_index.count(),
            "county_index_size": self._county_index.count(),
            "spatial_records": len(self._spatial_records),
            "aquifer_facets": self.aquifer_index.get_aquifer_counts(),
            "county_facets": self._county_index.get_county_counts(),
            "well_type_facets": self._well_type_index.get_type_counts(),
            "compliance_facets": self._compliance_index.get_status_counts(),
        }
