"""
LM05 Chain of Title Builder - Search Engine
==============================================
ECHO OMEGA PRIME - Landman Intelligence Division

Search instruments by:
- Grantor name (exact, fuzzy, soundex, metaphone)
- Grantee name (exact, fuzzy, soundex, metaphone)
- Legal description (abstract, survey, block, section)
- Date range (recording date, execution date)
- Book/page and document number
- Instrument type
- County and state
- Combined multi-field search

Integrates with:
- LANDMAN_ENRICHED classifications (NDJSON)
- ENCORE scraper results (JSON records)
- Reeves County data (G: drive, R2 archive)
- ShadowGlass D1 database
- Cognition Cloud EKM

Authority: Bobby Don McWilliams II (11.0 SUPREME SOVEREIGN)
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ENRICHED_ROOT = Path("O:/ECHO_OMEGA_PRIME/LANDMAN_ENRICHED")
ENCORE_ROOT = Path("O:/ECHO_OMEGA_PRIME/ENCORE")
LANDMAN_INTEL_ROOT = Path("O:/ECHO_OMEGA_PRIME/LANDMAN_INTELLIGENCE")
LANDMAN_DATA_ROOT = Path("O:/ECHO_OMEGA_PRIME/LANDMAN_DATA")
REEVES_DRIVE = Path("G:/")

DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 500
MAX_RESULTS = 2000
FUZZY_THRESHOLD = 0.80
DEFAULT_SEARCH_YEARS = 60


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class InstrumentRecord(BaseModel):
    """A recorded instrument with all searchable fields."""
    record_id: str = Field(..., description="Unique record identifier")
    instrument_type: str = Field(default="UNKNOWN", description="Instrument type")
    grantor: str = Field(default="", description="Grantor name(s)")
    grantee: str = Field(default="", description="Grantee name(s)")
    grantor_normalized: str = Field(default="", description="Normalized grantor name")
    grantee_normalized: str = Field(default="", description="Normalized grantee name")
    recording_date: Optional[str] = Field(default=None, description="Date recorded (YYYY-MM-DD)")
    execution_date: Optional[str] = Field(default=None, description="Date executed (YYYY-MM-DD)")
    volume: Optional[str] = Field(default=None, description="Volume/book number")
    page: Optional[str] = Field(default=None, description="Page number")
    document_number: Optional[str] = Field(default=None, description="Document/filing number")
    legal_description: str = Field(default="", description="Legal description text")
    abstract_number: Optional[str] = Field(default=None, description="Abstract number")
    survey_number: Optional[str] = Field(default=None, description="Survey/section number")
    block_number: Optional[str] = Field(default=None, description="Block number")
    county: str = Field(default="", description="County name")
    state: str = Field(default="TX", description="State code")
    interest_conveyed: Optional[str] = Field(default=None, description="Interest conveyed description")
    reservations: Optional[str] = Field(default=None, description="Reservations in conveyance")
    consideration: Optional[str] = Field(default=None, description="Consideration amount/description")
    source: str = Field(default="", description="Data source identifier")
    source_path: str = Field(default="", description="Original file/record path")
    confidence: float = Field(default=0.0, description="Entity extraction confidence")
    raw_data: Dict[str, Any] = Field(default_factory=dict, description="Original raw data")


class SearchQuery(BaseModel):
    """A search query with multiple filter criteria."""
    grantor: Optional[str] = Field(default=None, description="Grantor name to search")
    grantee: Optional[str] = Field(default=None, description="Grantee name to search")
    legal_description: Optional[str] = Field(default=None, description="Legal description text")
    abstract_number: Optional[str] = Field(default=None, description="Abstract number")
    survey_number: Optional[str] = Field(default=None, description="Survey/section number")
    block_number: Optional[str] = Field(default=None, description="Block number")
    county: Optional[str] = Field(default=None, description="County filter")
    state: Optional[str] = Field(default=None, description="State filter")
    instrument_type: Optional[str] = Field(default=None, description="Instrument type filter")
    date_from: Optional[str] = Field(default=None, description="Start date (YYYY-MM-DD)")
    date_to: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD)")
    volume: Optional[str] = Field(default=None, description="Volume/book number")
    page: Optional[str] = Field(default=None, description="Page number")
    document_number: Optional[str] = Field(default=None, description="Document number")
    fuzzy_matching: bool = Field(default=True, description="Enable fuzzy name matching")
    soundex_matching: bool = Field(default=True, description="Enable soundex matching")
    page_number: int = Field(default=1, description="Result page number")
    page_size: int = Field(default=DEFAULT_PAGE_SIZE, description="Results per page")
    sort_by: str = Field(default="recording_date", description="Sort field")
    sort_order: str = Field(default="asc", description="Sort order (asc/desc)")


class SearchResult(BaseModel):
    """Search result with pagination and relevance scoring."""
    query: SearchQuery
    total_results: int = 0
    page_number: int = 1
    page_size: int = DEFAULT_PAGE_SIZE
    total_pages: int = 0
    results: List[InstrumentRecord] = Field(default_factory=list)
    relevance_scores: Dict[str, float] = Field(default_factory=dict)
    search_time_ms: float = 0.0
    sources_searched: List[str] = Field(default_factory=list)


class SearchStats(BaseModel):
    """Search engine statistics."""
    total_records_indexed: int = 0
    records_by_source: Dict[str, int] = Field(default_factory=dict)
    records_by_county: Dict[str, int] = Field(default_factory=dict)
    records_by_type: Dict[str, int] = Field(default_factory=dict)
    index_build_time_ms: float = 0.0
    last_indexed: str = ""


# ---------------------------------------------------------------------------
# Name matching utilities
# ---------------------------------------------------------------------------

class NameMatcher:
    """Provides fuzzy, soundex, and metaphone name matching for chain search."""

    @staticmethod
    def normalize(name: str) -> str:
        """Normalize a name for matching."""
        if not name:
            return ""
        normalized = name.upper().strip()
        for suffix in [", LLC", " LLC", ", LP", " LP", ", INC", " INC",
                       ", CORP", " CORP", " ET AL", ", ET UX", " ET UX",
                       " ET VIR", ", ET VIR", " A/K/A", ", A/K/A", " F/K/A",
                       ", F/K/A", " JR", " JR.", " SR", " SR.", " III", " II",
                       " IV", ", TRUSTEE", " TRUSTEE", ", EXECUTOR", " EXECUTOR"]:
            normalized = normalized.replace(suffix, "")
        normalized = re.sub(r"[^\w\s]", "", normalized)
        normalized = " ".join(normalized.split())
        return normalized

    @staticmethod
    def soundex(name: str) -> str:
        """Generate Soundex code for a name."""
        if not name:
            return ""
        name = name.upper().strip()
        if not name:
            return ""

        mapping = {
            'B': '1', 'F': '1', 'P': '1', 'V': '1',
            'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
            'D': '3', 'T': '3',
            'L': '4',
            'M': '5', 'N': '5',
            'R': '6',
        }

        first_letter = name[0]
        code = [first_letter]
        prev_code = mapping.get(first_letter, '0')

        for char in name[1:]:
            char_code = mapping.get(char, '0')
            if char_code != '0' and char_code != prev_code:
                code.append(char_code)
                if len(code) == 4:
                    break
            if char not in ('H', 'W'):
                prev_code = char_code

        while len(code) < 4:
            code.append('0')

        return "".join(code[:4])

    @staticmethod
    def metaphone(name: str) -> str:
        """Generate simplified Metaphone code for a name."""
        if not name:
            return ""
        name = name.upper().strip()
        if not name:
            return ""

        replacements = [
            (r'^AE', 'E'), (r'^GN', 'N'), (r'^KN', 'N'), (r'^PN', 'N'), (r'^WR', 'R'),
            (r'MB$', 'M'), (r'PH', 'F'), (r'CK', 'K'),
            (r'SCH', 'SK'), (r'SH', 'X'), (r'TH', '0'),
            (r'GH', ''), (r'GN', 'N'),
        ]
        for pattern, replacement in replacements:
            name = re.sub(pattern, replacement, name)

        vowels = set('AEIOU')
        result = [name[0]] if name else []
        for i in range(1, len(name)):
            if name[i] not in vowels and name[i] != name[i - 1]:
                result.append(name[i])

        return "".join(result[:8])

    @staticmethod
    def similarity(name1: str, name2: str) -> float:
        """Calculate Jaro-Winkler similarity between two names."""
        if not name1 or not name2:
            return 0.0

        s1 = name1.upper().strip()
        s2 = name2.upper().strip()

        if s1 == s2:
            return 1.0

        len1, len2 = len(s1), len(s2)
        if len1 == 0 or len2 == 0:
            return 0.0

        match_distance = max(len1, len2) // 2 - 1
        if match_distance < 0:
            match_distance = 0

        s1_matches = [False] * len1
        s2_matches = [False] * len2
        matches = 0
        transpositions = 0

        for i in range(len1):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len2)
            for j in range(start, end):
                if s2_matches[j] or s1[i] != s2[j]:
                    continue
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break

        if matches == 0:
            return 0.0

        k = 0
        for i in range(len1):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

        jaro = (
            matches / len1 + matches / len2 + (matches - transpositions / 2) / matches
        ) / 3.0

        prefix_len = 0
        for i in range(min(4, len1, len2)):
            if s1[i] == s2[i]:
                prefix_len += 1
            else:
                break

        winkler = jaro + prefix_len * 0.1 * (1.0 - jaro)
        return min(1.0, winkler)

    def match(self, query_name: str, candidate_name: str, fuzzy: bool = True,
              use_soundex: bool = True, threshold: float = FUZZY_THRESHOLD) -> Tuple[bool, float]:
        """Check if two names match, returning (is_match, score)."""
        if not query_name or not candidate_name:
            return False, 0.0

        norm_query = self.normalize(query_name)
        norm_candidate = self.normalize(candidate_name)

        if norm_query == norm_candidate:
            return True, 1.0

        if norm_query in norm_candidate or norm_candidate in norm_query:
            return True, 0.95

        if fuzzy:
            sim = self.similarity(norm_query, norm_candidate)
            if sim >= threshold:
                return True, sim

        if use_soundex:
            query_words = norm_query.split()
            candidate_words = norm_candidate.split()
            if query_words and candidate_words:
                query_sdx = self.soundex(query_words[-1])
                candidate_sdx = self.soundex(candidate_words[-1])
                if query_sdx == candidate_sdx and query_sdx != "0000":
                    first_match = False
                    if len(query_words) > 1 and len(candidate_words) > 1:
                        first_sim = self.similarity(query_words[0], candidate_words[0])
                        first_match = first_sim >= 0.8
                    elif len(query_words) == 1 or len(candidate_words) == 1:
                        first_match = True

                    if first_match:
                        return True, 0.80

        return False, 0.0


# ---------------------------------------------------------------------------
# Legal description parser
# ---------------------------------------------------------------------------

class LegalDescriptionParser:
    """Parses and normalizes Texas legal descriptions for matching."""

    ABSTRACT_PATTERNS = [
        re.compile(r"(?:abstract|abst?\.?)\s*(?:no\.?\s*)?#?\s*(\d+)", re.IGNORECASE),
        re.compile(r"A-(\d+)", re.IGNORECASE),
    ]

    SURVEY_PATTERNS = [
        re.compile(r"(?:section|sec\.?|survey|surv\.?)\s*(?:no\.?\s*)?#?\s*(\d+)", re.IGNORECASE),
        re.compile(r"S(?:ec)?\.?\s*(\d+)", re.IGNORECASE),
    ]

    BLOCK_PATTERNS = [
        re.compile(r"(?:block|blk\.?)\s*(?:no\.?\s*)?#?\s*([\w\-]+)", re.IGNORECASE),
        re.compile(r"B(?:lk)?\.?\s*([\w\-]+)", re.IGNORECASE),
    ]

    TOWNSHIP_PATTERNS = [
        re.compile(r"(?:township|twp\.?)\s*(\d+\s*[NS])", re.IGNORECASE),
    ]

    RANGE_PATTERNS = [
        re.compile(r"(?:range|rge\.?)\s*(\d+\s*[EW])", re.IGNORECASE),
    ]

    ACREAGE_PATTERNS = [
        re.compile(r"(?:containing\s+)?(\d+(?:\.\d+)?)\s*acres?", re.IGNORECASE),
    ]

    COUNTY_PATTERNS = [
        re.compile(r"(\w+)\s+county", re.IGNORECASE),
    ]

    RAILROAD_PATTERNS = [
        re.compile(r"(H\s*&\s*GN|T\s*&\s*P|GC\s*&\s*SF|PSL|EL\s*&\s*RR)\s*(?:RR|R\.?R\.?|Ry\.?)?\s*(?:Co\.?|Survey)?", re.IGNORECASE),
    ]

    def parse(self, description: str) -> Dict[str, Any]:
        """Parse a legal description into structured components."""
        if not description:
            return {}

        result: Dict[str, Any] = {}

        for pattern in self.ABSTRACT_PATTERNS:
            match = pattern.search(description)
            if match:
                result["abstract_number"] = match.group(1).strip()
                break

        for pattern in self.SURVEY_PATTERNS:
            match = pattern.search(description)
            if match:
                result["survey_number"] = match.group(1).strip()
                break

        for pattern in self.BLOCK_PATTERNS:
            match = pattern.search(description)
            if match:
                result["block_number"] = match.group(1).strip()
                break

        for pattern in self.TOWNSHIP_PATTERNS:
            match = pattern.search(description)
            if match:
                result["township"] = match.group(1).strip()

        for pattern in self.RANGE_PATTERNS:
            match = pattern.search(description)
            if match:
                result["range"] = match.group(1).strip()

        for pattern in self.ACREAGE_PATTERNS:
            match = pattern.search(description)
            if match:
                try:
                    result["acreage"] = float(match.group(1))
                except ValueError:
                    pass

        for pattern in self.COUNTY_PATTERNS:
            match = pattern.search(description)
            if match:
                result["county"] = match.group(1).strip().upper()
                break

        for pattern in self.RAILROAD_PATTERNS:
            match = pattern.search(description)
            if match:
                result["railroad"] = match.group(1).strip().upper()
                break

        return result

    def normalize(self, description: str) -> str:
        """Normalize a legal description for consistent matching."""
        if not description:
            return ""

        normalized = description.upper().strip()
        replacements = [
            (r"\bSECTION\b", "SEC"),
            (r"\bSURVEY\b", "SURV"),
            (r"\bABSTRACT\b", "ABST"),
            (r"\bBLOCK\b", "BLK"),
            (r"\bTOWNSHIP\b", "TWP"),
            (r"\bCOUNTY\b", "CO"),
            (r"\bNO\.\s*", ""),
            (r"#\s*", ""),
            (r"\s+", " "),
        ]

        for pattern, replacement in replacements:
            normalized = re.sub(pattern, replacement, normalized)

        return normalized.strip()

    def matches(self, desc1: str, desc2: str) -> Tuple[bool, float]:
        """Check if two legal descriptions match the same tract."""
        if not desc1 or not desc2:
            return False, 0.0

        parsed1 = self.parse(desc1)
        parsed2 = self.parse(desc2)

        if not parsed1 or not parsed2:
            norm1 = self.normalize(desc1)
            norm2 = self.normalize(desc2)
            if norm1 == norm2:
                return True, 1.0
            return False, 0.0

        score = 0.0
        checks = 0

        if "abstract_number" in parsed1 and "abstract_number" in parsed2:
            checks += 1
            if parsed1["abstract_number"] == parsed2["abstract_number"]:
                score += 0.4
            else:
                return False, 0.0

        if "survey_number" in parsed1 and "survey_number" in parsed2:
            checks += 1
            if parsed1["survey_number"] == parsed2["survey_number"]:
                score += 0.25
            else:
                return False, 0.0

        if "block_number" in parsed1 and "block_number" in parsed2:
            checks += 1
            if parsed1["block_number"].upper() == parsed2["block_number"].upper():
                score += 0.2
            else:
                return False, 0.0

        if "county" in parsed1 and "county" in parsed2:
            checks += 1
            if parsed1["county"] == parsed2["county"]:
                score += 0.15

        if checks == 0:
            return False, 0.0

        return score >= 0.4, score


# ---------------------------------------------------------------------------
# Search engine
# ---------------------------------------------------------------------------

class ChainOfTitleSearchEngine:
    """Search engine for chain of title instrument records.

    Indexes records from multiple sources and provides fast multi-criteria
    search with fuzzy name matching, legal description parsing, and
    date range filtering.
    """

    def __init__(self) -> None:
        self._records: Dict[str, InstrumentRecord] = {}
        self._grantor_index: Dict[str, Set[str]] = {}
        self._grantee_index: Dict[str, Set[str]] = {}
        self._legal_desc_index: Dict[str, Set[str]] = {}
        self._date_index: Dict[str, Set[str]] = {}
        self._type_index: Dict[str, Set[str]] = {}
        self._county_index: Dict[str, Set[str]] = {}
        self._volume_page_index: Dict[str, Set[str]] = {}
        self._doc_number_index: Dict[str, Set[str]] = {}
        self._name_matcher = NameMatcher()
        self._legal_parser = LegalDescriptionParser()
        self._stats = SearchStats()
        self._indexed = False
        logger.info("ChainOfTitleSearchEngine initialized")

    def index_record(self, record: InstrumentRecord) -> None:
        """Add a single record to the search index."""
        self._records[record.record_id] = record

        grantor_norm = NameMatcher.normalize(record.grantor)
        if grantor_norm:
            record.grantor_normalized = grantor_norm
            key = grantor_norm.upper()
            if key not in self._grantor_index:
                self._grantor_index[key] = set()
            self._grantor_index[key].add(record.record_id)

        grantee_norm = NameMatcher.normalize(record.grantee)
        if grantee_norm:
            record.grantee_normalized = grantee_norm
            key = grantee_norm.upper()
            if key not in self._grantee_index:
                self._grantee_index[key] = set()
            self._grantee_index[key].add(record.record_id)

        if record.abstract_number:
            abs_key = f"A{record.abstract_number}"
            if abs_key not in self._legal_desc_index:
                self._legal_desc_index[abs_key] = set()
            self._legal_desc_index[abs_key].add(record.record_id)

        if record.survey_number and record.block_number:
            tract_key = f"S{record.survey_number}_B{record.block_number}".upper()
            if tract_key not in self._legal_desc_index:
                self._legal_desc_index[tract_key] = set()
            self._legal_desc_index[tract_key].add(record.record_id)

        if record.recording_date:
            year_match = re.search(r"\d{4}", record.recording_date)
            if year_match:
                year_key = year_match.group()
                if year_key not in self._date_index:
                    self._date_index[year_key] = set()
                self._date_index[year_key].add(record.record_id)

        if record.instrument_type and record.instrument_type != "UNKNOWN":
            type_key = record.instrument_type.upper()
            if type_key not in self._type_index:
                self._type_index[type_key] = set()
            self._type_index[type_key].add(record.record_id)

        if record.county:
            county_key = record.county.upper()
            if county_key not in self._county_index:
                self._county_index[county_key] = set()
            self._county_index[county_key].add(record.record_id)

        if record.volume and record.page:
            vp_key = f"V{record.volume}_P{record.page}"
            if vp_key not in self._volume_page_index:
                self._volume_page_index[vp_key] = set()
            self._volume_page_index[vp_key].add(record.record_id)

        if record.document_number:
            doc_key = record.document_number.upper().strip()
            if doc_key not in self._doc_number_index:
                self._doc_number_index[doc_key] = set()
            self._doc_number_index[doc_key].add(record.record_id)

    def index_from_ndjson(self, file_path: Path, source_name: str = "enriched") -> int:
        """Index records from an NDJSON classification file."""
        if not file_path.exists():
            logger.warning(f"NDJSON file not found: {file_path}")
            return 0

        count = 0
        with open(file_path, "r", encoding="utf-8") as fh:
            for line_num, line in enumerate(fh, 1):
                try:
                    data = json.loads(line.strip())
                    record_id = hashlib.md5(
                        f"{source_name}:{line_num}:{data.get('file_path', '')}".encode()
                    ).hexdigest()[:16]

                    legal_parts = self._legal_parser.parse(
                        data.get("legal_description", "") or data.get("file_path", "")
                    )

                    record = InstrumentRecord(
                        record_id=record_id,
                        instrument_type=data.get("doc_type") or "UNKNOWN",
                        grantor=data.get("grantor") or "",
                        grantee=data.get("grantee") or "",
                        recording_date=data.get("recording_date"),
                        legal_description=data.get("legal_description") or "",
                        abstract_number=legal_parts.get("abstract_number"),
                        survey_number=legal_parts.get("survey_number"),
                        block_number=legal_parts.get("block_number"),
                        county=data.get("county") or self._extract_county_from_path(data.get("file_path") or ""),
                        state=data.get("state") or "TX",
                        confidence=data.get("confidence") or 0.0,
                        source=source_name,
                        source_path=data.get("file_path", ""),
                        raw_data=data,
                    )
                    self.index_record(record)
                    count += 1
                except Exception as exc:
                    if line_num <= 5:
                        logger.debug(f"Skipping malformed line {line_num}: {exc}")

        logger.info(f"Indexed {count} records from {file_path.name} (source={source_name})")
        return count

    def index_from_json_records(self, file_path: Path, source_name: str = "encore") -> int:
        """Index records from a JSON array file (ENCORE format)."""
        if not file_path.exists():
            logger.warning(f"JSON file not found: {file_path}")
            return 0

        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                data = [data]
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.warning(f"Failed to parse {file_path}: {exc}")
            return 0

        count = 0
        for idx, item in enumerate(data):
            try:
                record_id = hashlib.md5(
                    f"{source_name}:{file_path.name}:{idx}".encode()
                ).hexdigest()[:16]

                legal_desc = item.get("legal_description", "") or item.get("legalDescription", "")
                legal_parts = self._legal_parser.parse(legal_desc)

                recording_date = item.get("recording_date") or item.get("recordedDate") or item.get("date")
                volume_raw = item.get("volume") or item.get("book")
                page_raw = item.get("page")

                volume_str: Optional[str] = None
                page_str: Optional[str] = None
                book_page = item.get("bookPage", "")
                if book_page and "/" in book_page:
                    parts = book_page.split("/", 1)
                    volume_str = parts[0].strip()
                    page_str = parts[1].strip()
                elif volume_raw:
                    volume_str = str(volume_raw)
                    page_str = str(page_raw) if page_raw else None

                record = InstrumentRecord(
                    record_id=record_id,
                    instrument_type=item.get("instrument_type") or item.get("instrumentType") or "UNKNOWN",
                    grantor=item.get("grantor") or item.get("grantorName") or "",
                    grantee=item.get("grantee") or item.get("granteeName") or "",
                    recording_date=recording_date,
                    volume=volume_str,
                    page=page_str,
                    document_number=item.get("document_number") or item.get("documentNumber") or item.get("docNumber"),
                    legal_description=legal_desc or "",
                    abstract_number=legal_parts.get("abstract_number"),
                    survey_number=legal_parts.get("survey_number"),
                    block_number=legal_parts.get("block_number"),
                    county=item.get("county", "").upper() if item.get("county") else legal_parts.get("county", ""),
                    state=item.get("state") or "TX",
                    interest_conveyed=item.get("interest_conveyed") or item.get("interestConveyed"),
                    reservations=item.get("reservations"),
                    consideration=item.get("consideration"),
                    source=source_name,
                    source_path=str(file_path),
                    confidence=item.get("confidence") or 0.5,
                    raw_data=item,
                )
                self.index_record(record)
                count += 1
            except Exception as exc:
                logger.debug(f"Skipping record {idx} in {file_path.name}: {exc}")

        if count > 0:
            logger.info(f"Indexed {count} records from {file_path.name} (source={source_name})")
        return count

    def load_all_sources(self) -> SearchStats:
        """Load and index records from all configured data sources."""
        import time
        start = time.perf_counter()
        total = 0
        sources: Dict[str, int] = {}

        classifications_file = ENRICHED_ROOT / "classified" / "classifications.ndjson"
        if classifications_file.exists():
            count = self.index_from_ndjson(classifications_file, "enriched")
            sources["enriched"] = count
            total += count

        encore_dirs = [ENCORE_ROOT, LANDMAN_DATA_ROOT]
        for encore_dir in encore_dirs:
            if encore_dir.exists():
                for json_file in encore_dir.glob("**/*.json"):
                    if json_file.stat().st_size < 100 * 1024 * 1024:
                        count = self.index_from_json_records(json_file, f"encore:{json_file.stem}")
                        if count > 0:
                            sources[f"encore:{json_file.stem}"] = count
                            total += count

        chain_dir = LANDMAN_INTEL_ROOT / "chains"
        if chain_dir.exists():
            for json_file in chain_dir.glob("*.json"):
                count = self.index_from_json_records(json_file, f"chain:{json_file.stem}")
                if count > 0:
                    sources[f"chain:{json_file.stem}"] = count
                    total += count

        elapsed_ms = (time.perf_counter() - start) * 1000

        county_counts: Dict[str, int] = {}
        type_counts: Dict[str, int] = {}
        for record in self._records.values():
            if record.county:
                county_counts[record.county] = county_counts.get(record.county, 0) + 1
            if record.instrument_type and record.instrument_type != "UNKNOWN":
                type_counts[record.instrument_type] = type_counts.get(record.instrument_type, 0) + 1

        self._stats = SearchStats(
            total_records_indexed=total,
            records_by_source=sources,
            records_by_county=county_counts,
            records_by_type=type_counts,
            index_build_time_ms=round(elapsed_ms, 2),
            last_indexed=datetime.now(timezone.utc).isoformat(),
        )
        self._indexed = True

        logger.info(
            f"Indexed {total} total records from {len(sources)} sources "
            f"in {elapsed_ms:.1f}ms"
        )
        return self._stats

    def search(self, query: SearchQuery) -> SearchResult:
        """Execute a multi-criteria search against the index."""
        import time
        start = time.perf_counter()

        candidate_sets: List[Set[str]] = []
        sources_searched: List[str] = []

        if query.document_number:
            doc_key = query.document_number.upper().strip()
            if doc_key in self._doc_number_index:
                candidate_sets.append(self._doc_number_index[doc_key])
                sources_searched.append("doc_number_index")

        if query.volume and query.page:
            vp_key = f"V{query.volume}_P{query.page}"
            if vp_key in self._volume_page_index:
                candidate_sets.append(self._volume_page_index[vp_key])
                sources_searched.append("volume_page_index")

        if query.county:
            county_key = query.county.upper()
            if county_key in self._county_index:
                candidate_sets.append(self._county_index[county_key])
                sources_searched.append("county_index")

        if query.instrument_type:
            type_key = query.instrument_type.upper()
            if type_key in self._type_index:
                candidate_sets.append(self._type_index[type_key])
                sources_searched.append("type_index")

        if query.abstract_number:
            abs_key = f"A{query.abstract_number}"
            if abs_key in self._legal_desc_index:
                candidate_sets.append(self._legal_desc_index[abs_key])
                sources_searched.append("abstract_index")

        if query.survey_number and query.block_number:
            tract_key = f"S{query.survey_number}_B{query.block_number}".upper()
            if tract_key in self._legal_desc_index:
                candidate_sets.append(self._legal_desc_index[tract_key])
                sources_searched.append("tract_index")

        if query.date_from or query.date_to:
            date_candidates = self._search_date_range(query.date_from, query.date_to)
            if date_candidates:
                candidate_sets.append(date_candidates)
                sources_searched.append("date_index")

        if candidate_sets:
            intersected = candidate_sets[0]
            for cs in candidate_sets[1:]:
                intersected = intersected.intersection(cs)
            candidates = intersected
        else:
            candidates = set(self._records.keys())

        relevance_scores: Dict[str, float] = {}
        matching_ids: List[str] = []

        for record_id in candidates:
            record = self._records.get(record_id)
            if not record:
                continue

            score = 1.0
            passes = True

            if query.grantor:
                is_match, name_score = self._name_matcher.match(
                    query.grantor, record.grantor,
                    fuzzy=query.fuzzy_matching,
                    use_soundex=query.soundex_matching,
                )
                if is_match:
                    score *= name_score
                else:
                    passes = False

            if query.grantee and passes:
                is_match, name_score = self._name_matcher.match(
                    query.grantee, record.grantee,
                    fuzzy=query.fuzzy_matching,
                    use_soundex=query.soundex_matching,
                )
                if is_match:
                    score *= name_score
                else:
                    passes = False

            if query.legal_description and passes:
                is_match, desc_score = self._legal_parser.matches(
                    query.legal_description, record.legal_description
                )
                if is_match:
                    score *= desc_score
                else:
                    passes = False

            if query.state and passes:
                if record.state and record.state.upper() != query.state.upper():
                    passes = False

            if passes:
                relevance_scores[record_id] = score
                matching_ids.append(record_id)

        matching_ids.sort(
            key=lambda rid: (
                relevance_scores.get(rid, 0.0),
                self._records[rid].recording_date or "",
            ),
            reverse=(query.sort_order.lower() == "desc"),
        )

        if query.sort_by == "recording_date":
            matching_ids.sort(
                key=lambda rid: self._records[rid].recording_date or "",
                reverse=(query.sort_order.lower() == "desc"),
            )
        elif query.sort_by == "relevance":
            matching_ids.sort(
                key=lambda rid: relevance_scores.get(rid, 0.0),
                reverse=True,
            )

        total = len(matching_ids)
        page_size = min(query.page_size, MAX_PAGE_SIZE)
        total_pages = max(1, (total + page_size - 1) // page_size)
        page_num = max(1, min(query.page_number, total_pages))
        offset = (page_num - 1) * page_size
        page_ids = matching_ids[offset:offset + page_size]

        results = [self._records[rid] for rid in page_ids]
        page_scores = {rid: relevance_scores.get(rid, 0.0) for rid in page_ids}

        elapsed_ms = (time.perf_counter() - start) * 1000
        sources_searched.append("name_matcher")

        return SearchResult(
            query=query,
            total_results=total,
            page_number=page_num,
            page_size=page_size,
            total_pages=total_pages,
            results=results,
            relevance_scores=page_scores,
            search_time_ms=round(elapsed_ms, 2),
            sources_searched=sources_searched,
        )

    def search_by_grantor(self, name: str, county: Optional[str] = None,
                          date_from: Optional[str] = None, date_to: Optional[str] = None,
                          page_size: int = DEFAULT_PAGE_SIZE) -> SearchResult:
        """Convenience method: search by grantor name."""
        query = SearchQuery(
            grantor=name, county=county, date_from=date_from, date_to=date_to,
            page_size=page_size,
        )
        return self.search(query)

    def search_by_grantee(self, name: str, county: Optional[str] = None,
                          date_from: Optional[str] = None, date_to: Optional[str] = None,
                          page_size: int = DEFAULT_PAGE_SIZE) -> SearchResult:
        """Convenience method: search by grantee name."""
        query = SearchQuery(
            grantee=name, county=county, date_from=date_from, date_to=date_to,
            page_size=page_size,
        )
        return self.search(query)

    def search_by_legal(self, abstract: Optional[str] = None, survey: Optional[str] = None,
                        block: Optional[str] = None, county: Optional[str] = None,
                        page_size: int = DEFAULT_PAGE_SIZE) -> SearchResult:
        """Convenience method: search by legal description components."""
        query = SearchQuery(
            abstract_number=abstract, survey_number=survey, block_number=block,
            county=county, page_size=page_size,
        )
        return self.search(query)

    def search_by_doc_number(self, doc_number: str) -> SearchResult:
        """Convenience method: search by document number."""
        query = SearchQuery(document_number=doc_number)
        return self.search(query)

    def search_by_volume_page(self, volume: str, page: str) -> SearchResult:
        """Convenience method: search by volume and page."""
        query = SearchQuery(volume=volume, page=page)
        return self.search(query)

    def get_record(self, record_id: str) -> Optional[InstrumentRecord]:
        """Retrieve a single record by ID."""
        return self._records.get(record_id)

    def get_stats(self) -> SearchStats:
        """Return search engine statistics."""
        return self._stats

    def get_total_records(self) -> int:
        """Return total number of indexed records."""
        return len(self._records)

    # -- internal helpers --

    def _search_date_range(self, date_from: Optional[str], date_to: Optional[str]) -> Set[str]:
        """Search the date index for records within a date range."""
        results: Set[str] = set()

        try:
            year_from = int(date_from[:4]) if date_from else 1800
            year_to = int(date_to[:4]) if date_to else 2030
        except (ValueError, IndexError):
            return results

        for year_str, record_ids in self._date_index.items():
            try:
                year = int(year_str)
                if year_from <= year <= year_to:
                    results.update(record_ids)
            except ValueError:
                continue

        if date_from or date_to:
            filtered: Set[str] = set()
            for rid in results:
                record = self._records.get(rid)
                if not record or not record.recording_date:
                    continue
                rec_date = record.recording_date
                if date_from and rec_date < date_from:
                    continue
                if date_to and rec_date > date_to:
                    continue
                filtered.add(rid)
            return filtered

        return results

    def _extract_county_from_path(self, file_path: str) -> str:
        """Extract county name from a file path."""
        if not file_path:
            return ""

        path_upper = file_path.upper().replace("\\", "/")
        permian_counties = [
            "REEVES", "ECTOR", "MIDLAND", "MARTIN", "HOWARD", "LOVING",
            "WARD", "CRANE", "UPTON", "PECOS", "TERRELL", "CULBERSON",
            "JEFF_DAVIS", "BREWSTER", "PRESIDIO", "ANDREWS", "GAINES",
            "DAWSON", "BORDEN", "SCURRY", "WINKLER", "LEA",
        ]
        for county in permian_counties:
            if county in path_upper:
                return county
        return ""
