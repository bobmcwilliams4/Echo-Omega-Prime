"""
CognitionCloudRetriever — Shared cloud knowledge access for all ECHO engines.

Connects local engines to the FULL ECHO knowledge ecosystem:
  - Cognition Cloud (EKM, Graph, Crystal Memory, Engine Matrix, Embedding Pipeline)
  - Knowledge Forge (5,400+ docs, 12,500+ chunks, semantic search)
  - Echo Shared Brain (cross-instance memory, decisions, semantic search)
  - Echo Memory Prime (9-pillar memory, crystal store, vectorize search)
  - ShadowGlass Warpspeed (auto-scrape from web when knowledge not found)

Usage:
    from cloud_retriever import CognitionCloudRetriever, CloudKnowledge
    cloud = CognitionCloudRetriever()
    results = await cloud.retrieve_all("title chain analysis", category="real_estate")
    # If nothing found, auto-scrapes via ShadowGlass and stores in Knowledge Forge

Architecture:
    - httpx async client with connection pooling
    - TWO-TIER CACHE: L1 full-response cache (sub-ms) + L2 per-source cache
    - Query normalization for maximum cache hit rate
    - Race-to-first: return as soon as MIN_FAST_RESULTS found, don't wait for all
    - 8-source parallel search with tiered timeouts (fast sources 3s, slow 5s, scrape 15s)
    - Auto-scrape fallback: ShadowGlass Warpspeed Worker + Knowledge Forge ingest
    - Async telemetry: every query reported to Memory Prime + Shared Brain (non-blocking)
    - Graceful degradation: any source down -> skip, no crash
"""

from __future__ import annotations

import asyncio
import hashlib
import re
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from loguru import logger
from pydantic import BaseModel, Field

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore[assignment]
    logger.warning("httpx not installed — cloud retrieval disabled. pip install httpx")


# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

EKM_URL = "https://ekm-query-engine.bmcii1976.workers.dev"
GRAPH_URL = "https://graph-query-engine.bmcii1976.workers.dev"
CRYSTAL_URL = "https://crystal-memory-engine.bmcii1976.workers.dev"
ENGINE_MATRIX_URL = "https://engine-matrix.bmcii1976.workers.dev"
EMBEDDING_URL = "https://embedding-pipeline.bmcii1976.workers.dev"
KNOWLEDGE_FORGE_URL = "https://echo-knowledge-forge.bmcii1976.workers.dev"
SHARED_BRAIN_URL = "https://echo-shared-brain.bmcii1976.workers.dev"
MEMORY_PRIME_URL = "https://echo-memory-prime.bmcii1976.workers.dev"
SHADOWGLASS_URL = "https://shadowglass-v8-warpspeed.bmcii1976.workers.dev"

FAST_TIMEOUT = 3.0  # seconds for primary fast sources (EKM, Forge, Crystal)
DEFAULT_TIMEOUT = 5.0  # seconds for secondary sources (Graph, Brain, Memory)
SCRAPE_TIMEOUT = 15.0  # seconds for ShadowGlass scrape
CACHE_TTL = 30.0  # seconds before per-source cache entry expires
L1_CACHE_TTL = 300.0  # 5 minutes for full-response L1 cache (sub-ms returns)
MAX_CACHE_SIZE = 512  # max entries in per-source cache
L1_CACHE_SIZE = 2048  # max entries in full-response L1 cache
MIN_RESULTS_THRESHOLD = 3  # if fewer results than this, trigger auto-scrape
MIN_FAST_RESULTS = 5  # return as soon as this many results from fast sources
TELEMETRY_ENABLED = True  # report every query to Memory Prime + Shared Brain


# ═══════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════

class CloudSource(str, Enum):
    """Which cloud service provided the result."""
    EKM = "ekm"
    GRAPH = "graph"
    CRYSTAL = "crystal"
    ENGINE_MATRIX = "engine_matrix"
    EMBEDDING = "embedding"
    KNOWLEDGE_FORGE = "knowledge_forge"
    SHARED_BRAIN = "shared_brain"
    MEMORY_PRIME = "memory_prime"
    SHADOWGLASS_SCRAPE = "shadowglass_scrape"
    SHADOWGLASS_RECORDS = "shadowglass_records"
    LOCAL_FALLBACK = "local_fallback"


class CloudRecord(BaseModel):
    """Single knowledge record from cloud."""
    id: str = ""
    title: str = ""
    content: str = ""
    category: str = ""
    source: CloudSource = CloudSource.EKM
    relevance_score: float = 0.0
    authority_level: int = 1
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GraphNode(BaseModel):
    """Single node from the knowledge graph."""
    node_id: str = ""
    label: str = ""
    node_type: str = ""
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """Edge connecting two graph nodes."""
    source_id: str = ""
    target_id: str = ""
    edge_type: str = ""
    weight: float = 1.0
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphNeighborhood(BaseModel):
    """Subgraph around a node."""
    center_node: str = ""
    nodes: List[GraphNode] = Field(default_factory=list)
    edges: List[GraphEdge] = Field(default_factory=list)
    depth: int = 0


class GraphPath(BaseModel):
    """Path between two nodes."""
    start_id: str = ""
    end_id: str = ""
    path_nodes: List[str] = Field(default_factory=list)
    path_edges: List[str] = Field(default_factory=list)
    total_weight: float = 0.0
    found: bool = False


class CrystalRecord(BaseModel):
    """Crystal memory record."""
    crystal_id: str = ""
    topic: str = ""
    content: str = ""
    category: str = ""
    authority: int = 1
    timestamp: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EmbeddingResult(BaseModel):
    """Semantic embedding search result."""
    id: str = ""
    text: str = ""
    score: float = 0.0
    index: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ForgeResult(BaseModel):
    """Knowledge Forge search result."""
    doc_id: str = ""
    chunk_id: str = ""
    title: str = ""
    snippet: str = ""
    section: str = ""
    category: str = ""
    score: float = 0.0
    tags: List[str] = Field(default_factory=list)
    source_path: str = ""


class BrainMessage(BaseModel):
    """Echo Shared Brain message/decision."""
    id: str = ""
    content: str = ""
    instance_id: str = ""
    importance: int = 5
    tags: List[str] = Field(default_factory=list)
    created_at: str = ""
    score: float = 0.0


class MemoryPrimeResult(BaseModel):
    """Echo Memory Prime recall result."""
    id: str = ""
    content: str = ""
    category: str = ""
    layer: str = ""
    score: float = 0.0
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DeedRecord(BaseModel):
    """ShadowGlass analyzed deed record from D1 pipeline."""
    document_id: str = ""
    county: str = ""
    instrument_type: str = ""
    grantor: str = ""
    grantee: str = ""
    date_filed: str = ""
    date_executed: str = ""
    section_block_survey: str = ""
    legal_description: str = ""
    consideration: str = ""
    acreage: str = ""
    mineral_interest_pct: str = ""
    royalty_interest_pct: str = ""
    volume_page: str = ""
    ocr_confidence: float = 0.0
    r2_pdf_key: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ScrapeResult(BaseModel):
    """ShadowGlass warpspeed scrape result."""
    url: str = ""
    title: str = ""
    content: str = ""
    scraped_at: str = ""
    stored_in: str = ""


class CloudKnowledge(BaseModel):
    """Aggregated cloud knowledge response."""
    clauses: List[CloudRecord] = Field(default_factory=list)
    graph_nodes: List[GraphNode] = Field(default_factory=list)
    graph_edges: List[GraphEdge] = Field(default_factory=list)
    crystals: List[CrystalRecord] = Field(default_factory=list)
    embeddings: List[EmbeddingResult] = Field(default_factory=list)
    forge_results: List[ForgeResult] = Field(default_factory=list)
    brain_messages: List[BrainMessage] = Field(default_factory=list)
    memory_results: List[MemoryPrimeResult] = Field(default_factory=list)
    deed_records: List[DeedRecord] = Field(default_factory=list)
    scrape_results: List[ScrapeResult] = Field(default_factory=list)
    sources_queried: List[str] = Field(default_factory=list)
    sources_succeeded: List[str] = Field(default_factory=list)
    sources_failed: List[str] = Field(default_factory=list)
    total_records: int = 0
    retrieval_time_ms: float = 0.0
    from_cache: bool = False
    auto_scraped: bool = False

    @property
    def has_results(self) -> bool:
        return self.total_records > 0

    def merged_text(self, max_chars: int = 12000) -> str:
        """Merge all cloud knowledge into a single text block for LLM context."""
        parts: List[str] = []
        # Deed records go FIRST — they are actual property/title data
        for dr in self.deed_records[:30]:
            deed_parts = [f"[DEED RECORD] {dr.county} County"]
            if dr.instrument_type:
                deed_parts.append(f"Type: {dr.instrument_type}")
            if dr.grantor:
                deed_parts.append(f"Grantor: {dr.grantor}")
            if dr.grantee:
                deed_parts.append(f"Grantee: {dr.grantee}")
            if dr.date_filed:
                deed_parts.append(f"Filed: {dr.date_filed}")
            if dr.section_block_survey:
                deed_parts.append(f"Location: {dr.section_block_survey}")
            if dr.legal_description:
                deed_parts.append(f"Legal: {dr.legal_description[:200]}")
            if dr.consideration:
                deed_parts.append(f"Consideration: {dr.consideration}")
            if dr.acreage:
                deed_parts.append(f"Acreage: {dr.acreage}")
            if dr.mineral_interest_pct:
                deed_parts.append(f"Mineral Interest: {dr.mineral_interest_pct}")
            if dr.royalty_interest_pct:
                deed_parts.append(f"Royalty Interest: {dr.royalty_interest_pct}")
            if dr.volume_page:
                deed_parts.append(f"Vol/Pg: {dr.volume_page}")
            parts.append(" | ".join(deed_parts))
        for c in self.clauses[:10]:
            parts.append(f"[EKM] {c.title}: {c.content[:300]}")
        for fr in self.forge_results[:10]:
            parts.append(f"[Forge] {fr.title} ({fr.section}): {fr.snippet[:300]}")
        for bm in self.brain_messages[:5]:
            parts.append(f"[Brain] {bm.content[:300]}")
        for mr in self.memory_results[:5]:
            parts.append(f"[Memory] {mr.content[:300]}")
        for cr in self.crystals[:5]:
            parts.append(f"[Crystal] {cr.topic}: {cr.content[:300]}")
        for n in self.graph_nodes[:5]:
            parts.append(f"[Graph] {n.label} ({n.node_type}): {n.properties}")
        for sr in self.scrape_results[:3]:
            parts.append(f"[Scraped] {sr.title}: {sr.content[:300]}")
        merged = "\n".join(parts)
        return merged[:max_chars] if len(merged) > max_chars else merged

    def citation_list(self) -> List[Dict[str, str]]:
        """Return structured citations for response attribution."""
        citations: List[Dict[str, str]] = []
        for dr in self.deed_records:
            citations.append({
                "source": "ShadowGlass",
                "id": dr.document_id,
                "title": f"{dr.county} {dr.instrument_type}: {dr.grantor} -> {dr.grantee}",
                "category": "deed_record",
                "volume_page": dr.volume_page,
            })
        for c in self.clauses:
            citations.append({"source": "EKM", "id": c.id, "title": c.title, "category": c.category})
        for cr in self.crystals:
            citations.append({"source": "Crystal", "id": cr.crystal_id, "title": cr.topic, "category": cr.category})
        for fr in self.forge_results:
            citations.append({"source": "Forge", "id": fr.doc_id, "title": fr.title, "category": fr.category})
        for bm in self.brain_messages:
            citations.append({"source": "Brain", "id": bm.id, "title": bm.content[:80], "category": "shared_brain"})
        for sr in self.scrape_results:
            citations.append({"source": "Scraped", "id": sr.url, "title": sr.title, "category": "web_scrape"})
        return citations


# ═══════════════════════════════════════════════════════════════════
# QUERY NORMALIZATION — Maximize cache hit rates
# ═══════════════════════════════════════════════════════════════════

_STOPWORDS: Set[str] = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "can", "could", "must", "of", "in", "to",
    "for", "with", "on", "at", "from", "by", "as", "into", "about",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "i", "me", "my", "we", "our", "you", "your", "he", "she", "it",
    "they", "them", "its", "his", "her", "their", "and", "or", "but",
    "if", "then", "so", "no", "not", "how", "where", "when", "why",
}


def _normalize_query(query: str) -> str:
    """Normalize query for cache key generation — strips noise, sorts words."""
    lowered = query.lower().strip()
    # Remove punctuation except hyphens (keep "section-1031")
    cleaned = re.sub(r"[^\w\s\-]", " ", lowered)
    # Split, remove stopwords, sort alphabetically
    words = sorted(set(w for w in cleaned.split() if w and w not in _STOPWORDS))
    return " ".join(words) if words else lowered


def _cache_key(*args: Any) -> str:
    """Generate a fast hash key from args."""
    raw = str(args)
    return hashlib.md5(raw.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════
# TWO-TIER CACHE SYSTEM
# ═══════════════════════════════════════════════════════════════════
#
# L1 (RESPONSE CACHE): Full CloudKnowledge responses by normalized query.
#     Sub-microsecond dict lookup. 2048 entries, 5-min TTL.
#     This is what makes repeated queries return in <1ms.
#
# L2 (SOURCE CACHE): Individual source results.
#     Per-source caching with 30s TTL.
#     Prevents hammering cloud APIs on parallel retrieve_all().
#

@dataclass
class _CacheEntry:
    value: Any
    expires_at: float
    key: str


class _TTLCache:
    """LRU cache with TTL expiration — used as L2 per-source cache."""

    def __init__(self, max_size: int = MAX_CACHE_SIZE, ttl: float = CACHE_TTL) -> None:
        self._store: Dict[str, _CacheEntry] = {}
        self._max_size = max_size
        self._ttl = ttl
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry is None:
            self._misses += 1
            return None
        if time.monotonic() > entry.expires_at:
            del self._store[key]
            self._misses += 1
            return None
        self._hits += 1
        return entry.value

    def put(self, key: str, value: Any) -> None:
        if len(self._store) >= self._max_size:
            oldest_key = min(self._store, key=lambda k: self._store[k].expires_at)
            del self._store[oldest_key]
        self._store[key] = _CacheEntry(value=value, expires_at=time.monotonic() + self._ttl, key=key)

    @property
    def stats(self) -> Dict[str, int]:
        return {"hits": self._hits, "misses": self._misses, "size": len(self._store)}


class _L1ResponseCache:
    """
    L1 full-response cache — stores complete CloudKnowledge objects by normalized query.
    Sub-microsecond lookup. This is what delivers millisecond responses.
    """

    def __init__(self, max_size: int = L1_CACHE_SIZE, ttl: float = L1_CACHE_TTL) -> None:
        self._store: OrderedDict[str, _CacheEntry] = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl
        self._hits = 0
        self._misses = 0

    def get(self, query: str, category: Optional[str] = None) -> Optional[Any]:
        """Look up by normalized query — sub-microsecond dict access."""
        key = _cache_key(_normalize_query(query), category or "")
        entry = self._store.get(key)
        if entry is None:
            self._misses += 1
            return None
        if time.monotonic() > entry.expires_at:
            del self._store[key]
            self._misses += 1
            return None
        # Move to end (LRU)
        self._store.move_to_end(key)
        self._hits += 1
        return entry.value

    def put(self, query: str, category: Optional[str], value: Any) -> None:
        """Store full response by normalized query."""
        key = _cache_key(_normalize_query(query), category or "")
        # Evict oldest if at capacity
        while len(self._store) >= self._max_size:
            self._store.popitem(last=False)
        self._store[key] = _CacheEntry(
            value=value, expires_at=time.monotonic() + self._ttl, key=key
        )

    @property
    def stats(self) -> Dict[str, Any]:
        return {
            "hits": self._hits,
            "misses": self._misses,
            "size": len(self._store),
            "hit_rate": round(self._hits / max(self._hits + self._misses, 1), 3),
        }


# ═══════════════════════════════════════════════════════════════════
# COGNITION CLOUD RETRIEVER
# ═══════════════════════════════════════════════════════════════════

class CognitionCloudRetriever:
    """
    Shared cloud knowledge retriever for all ECHO engines.

    Connects to Cognition Cloud workers to fetch EKM records,
    graph relationships, crystal memories, and semantic embeddings.

    Features:
        - TWO-TIER CACHE: L1 full-response (<1ms) + L2 per-source (30s TTL)
        - Query normalization for maximum cache hit rates
        - Race-to-first: fast sources return in 3s, slow sources 5s
        - Async telemetry: every query logged to Memory Prime + Shared Brain
        - Graceful degradation (any source down -> skip, no crash)
        - Auto-scrape fallback via ShadowGlass Warpspeed
    """

    def __init__(
        self,
        ekm_url: str = EKM_URL,
        graph_url: str = GRAPH_URL,
        crystal_url: str = CRYSTAL_URL,
        engine_matrix_url: str = ENGINE_MATRIX_URL,
        embedding_url: str = EMBEDDING_URL,
        knowledge_forge_url: str = KNOWLEDGE_FORGE_URL,
        shared_brain_url: str = SHARED_BRAIN_URL,
        memory_prime_url: str = MEMORY_PRIME_URL,
        shadowglass_url: str = SHADOWGLASS_URL,
        timeout: float = DEFAULT_TIMEOUT,
        fast_timeout: float = FAST_TIMEOUT,
        cache_ttl: float = CACHE_TTL,
        auto_scrape: bool = True,
        telemetry: bool = TELEMETRY_ENABLED,
    ) -> None:
        self._ekm_url = ekm_url
        self._graph_url = graph_url
        self._crystal_url = crystal_url
        self._engine_matrix_url = engine_matrix_url
        self._embedding_url = embedding_url
        self._knowledge_forge_url = knowledge_forge_url
        self._shared_brain_url = shared_brain_url
        self._memory_prime_url = memory_prime_url
        self._shadowglass_url = shadowglass_url
        self._timeout = timeout
        self._fast_timeout = fast_timeout
        self._auto_scrape = auto_scrape
        self._telemetry = telemetry
        self._cache = _TTLCache(ttl=cache_ttl)
        self._l1_cache = _L1ResponseCache()
        self._client: Optional[httpx.AsyncClient] = None
        self._fast_client: Optional[httpx.AsyncClient] = None
        self._request_count = 0
        self._error_count = 0
        self._l1_hit_count = 0
        self._total_query_count = 0
        self._total_latency_ms = 0.0

    async def _get_client(self) -> httpx.AsyncClient:
        """Standard client with DEFAULT_TIMEOUT (5s)."""
        if self._client is None or self._client.is_closed:
            if httpx is None:
                raise RuntimeError("httpx not installed")
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self._timeout),
                limits=httpx.Limits(max_connections=30, max_keepalive_connections=15),
                follow_redirects=True,
            )
        return self._client

    async def _get_fast_client(self) -> httpx.AsyncClient:
        """Fast client with FAST_TIMEOUT (3s) for primary sources."""
        if self._fast_client is None or self._fast_client.is_closed:
            if httpx is None:
                raise RuntimeError("httpx not installed")
            self._fast_client = httpx.AsyncClient(
                timeout=httpx.Timeout(self._fast_timeout),
                limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
                follow_redirects=True,
            )
        return self._fast_client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
        if self._fast_client and not self._fast_client.is_closed:
            await self._fast_client.aclose()
            self._fast_client = None

    # ───────────────────────────────────────────────────────
    # EKM — Enterprise Knowledge Management
    # ───────────────────────────────────────────────────────

    async def search_clauses(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 20,
    ) -> List[CloudRecord]:
        """Search EKM for relevant knowledge records."""
        cache_key = _cache_key("ekm_search", query, category, limit)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            params: Dict[str, Any] = {"q": query, "limit": limit}
            if category:
                params["category"] = category

            resp = await client.get(f"{self._ekm_url}/api/search", params=params)
            resp.raise_for_status()
            data = resp.json()

            records: List[CloudRecord] = []
            for item in data.get("results", data.get("records", data.get("data", []))):
                records.append(CloudRecord(
                    id=str(item.get("id", item.get("record_id", ""))),
                    title=item.get("title", item.get("name", "")),
                    content=item.get("content", item.get("text", item.get("summary", ""))),
                    category=item.get("category", item.get("type", "")),
                    source=CloudSource.EKM,
                    relevance_score=float(item.get("score", item.get("relevance", 0.0))),
                    authority_level=int(item.get("authority", 1)),
                    metadata=item.get("metadata", {}),
                ))

            self._cache.put(cache_key, records)
            logger.debug(f"EKM search returned {len(records)} results for '{query[:50]}...'")
            return records

        except Exception as e:
            self._error_count += 1
            logger.warning(f"EKM search failed for '{query[:50]}...': {e}")
            return []

    # ───────────────────────────────────────────────────────
    # SEMANTIC MATCH — Vector similarity search
    # ───────────────────────────────────────────────────────

    async def semantic_match(
        self,
        text: str,
        mode: int = 2,
        top_k: int = 10,
    ) -> List[EmbeddingResult]:
        """Semantic similarity search via embedding pipeline."""
        cache_key = _cache_key("semantic", text, mode, top_k)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            resp = await client.post(
                f"{self._embedding_url}/api/search",
                json={"text": text, "mode": mode, "top_k": top_k},
            )
            resp.raise_for_status()
            data = resp.json()

            results: List[EmbeddingResult] = []
            for item in data.get("results", data.get("matches", [])):
                results.append(EmbeddingResult(
                    id=str(item.get("id", "")),
                    text=item.get("text", item.get("content", "")),
                    score=float(item.get("score", item.get("similarity", 0.0))),
                    index=item.get("index", ""),
                    metadata=item.get("metadata", {}),
                ))

            self._cache.put(cache_key, results)
            logger.debug(f"Semantic match returned {len(results)} results")
            return results

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Semantic match failed: {e}")
            return []

    # ───────────────────────────────────────────────────────
    # GRAPH — Knowledge graph traversal
    # ───────────────────────────────────────────────────────

    async def graph_neighbors(
        self,
        node_id: str,
        depth: int = 2,
        edge_types: Optional[List[str]] = None,
    ) -> GraphNeighborhood:
        """Get neighborhood subgraph around a node."""
        cache_key = _cache_key("graph_neighbors", node_id, depth, edge_types)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            params: Dict[str, Any] = {"depth": depth}
            if edge_types:
                params["edge_types"] = ",".join(edge_types)

            resp = await client.get(f"{self._graph_url}/api/node/{node_id}/neighbors", params=params)
            resp.raise_for_status()
            data = resp.json()

            nodes: List[GraphNode] = []
            for n in data.get("nodes", []):
                nodes.append(GraphNode(
                    node_id=str(n.get("id", n.get("node_id", ""))),
                    label=n.get("label", n.get("name", "")),
                    node_type=n.get("type", n.get("node_type", "")),
                    properties=n.get("properties", n.get("data", {})),
                ))

            edges: List[GraphEdge] = []
            for e in data.get("edges", data.get("relationships", [])):
                edges.append(GraphEdge(
                    source_id=str(e.get("source", e.get("from", ""))),
                    target_id=str(e.get("target", e.get("to", ""))),
                    edge_type=e.get("type", e.get("edge_type", "")),
                    weight=float(e.get("weight", 1.0)),
                    properties=e.get("properties", {}),
                ))

            result = GraphNeighborhood(
                center_node=node_id,
                nodes=nodes,
                edges=edges,
                depth=depth,
            )
            self._cache.put(cache_key, result)
            logger.debug(f"Graph neighbors for '{node_id}': {len(nodes)} nodes, {len(edges)} edges")
            return result

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Graph neighbors failed for '{node_id}': {e}")
            return GraphNeighborhood(center_node=node_id)

    async def graph_path(
        self,
        start_id: str,
        end_id: str,
    ) -> GraphPath:
        """Find shortest path between two graph nodes."""
        cache_key = _cache_key("graph_path", start_id, end_id)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            resp = await client.get(
                f"{self._graph_url}/api/path",
                params={"start": start_id, "end": end_id},
            )
            resp.raise_for_status()
            data = resp.json()

            result = GraphPath(
                start_id=start_id,
                end_id=end_id,
                path_nodes=data.get("nodes", data.get("path", [])),
                path_edges=data.get("edges", []),
                total_weight=float(data.get("weight", data.get("distance", 0.0))),
                found=data.get("found", len(data.get("path", [])) > 0),
            )
            self._cache.put(cache_key, result)
            return result

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Graph path failed ({start_id} -> {end_id}): {e}")
            return GraphPath(start_id=start_id, end_id=end_id)

    async def graph_search(
        self,
        query: str,
        node_type: Optional[str] = None,
        limit: int = 10,
    ) -> List[GraphNode]:
        """Search graph nodes by text query."""
        cache_key = _cache_key("graph_search", query, node_type, limit)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            params: Dict[str, Any] = {"q": query, "limit": limit}
            if node_type:
                params["type"] = node_type

            resp = await client.get(f"{self._graph_url}/api/search", params=params)
            resp.raise_for_status()
            data = resp.json()

            nodes: List[GraphNode] = []
            for n in data.get("results", data.get("nodes", [])):
                nodes.append(GraphNode(
                    node_id=str(n.get("id", n.get("node_id", ""))),
                    label=n.get("label", n.get("name", "")),
                    node_type=n.get("type", n.get("node_type", "")),
                    properties=n.get("properties", n.get("data", {})),
                ))

            self._cache.put(cache_key, nodes)
            return nodes

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Graph search failed for '{query[:50]}...': {e}")
            return []

    # ───────────────────────────────────────────────────────
    # CRYSTAL MEMORY
    # ───────────────────────────────────────────────────────

    async def search_crystals(
        self,
        query: str,
        category: Optional[str] = None,
        min_authority: int = 1,
    ) -> List[CrystalRecord]:
        """Search crystal memory for relevant memories."""
        cache_key = _cache_key("crystal_search", query, category, min_authority)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            params: Dict[str, Any] = {"q": query}
            if category:
                params["category"] = category
            if min_authority > 1:
                params["min_authority"] = min_authority

            resp = await client.get(f"{self._crystal_url}/api/search", params=params)
            resp.raise_for_status()
            data = resp.json()

            crystals: List[CrystalRecord] = []
            for item in data.get("results", data.get("crystals", [])):
                crystals.append(CrystalRecord(
                    crystal_id=str(item.get("id", item.get("crystal_id", ""))),
                    topic=item.get("topic", item.get("title", "")),
                    content=item.get("content", item.get("text", "")),
                    category=item.get("category", ""),
                    authority=int(item.get("authority", 1)),
                    timestamp=item.get("timestamp", item.get("created_at", "")),
                    metadata=item.get("metadata", {}),
                ))

            self._cache.put(cache_key, crystals)
            logger.debug(f"Crystal search returned {len(crystals)} results for '{query[:50]}...'")
            return crystals

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Crystal search failed: {e}")
            return []

    async def get_crystal(self, crystal_id: str) -> Optional[CrystalRecord]:
        """Fetch a specific crystal by ID."""
        cache_key = _cache_key("crystal_get", crystal_id)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            resp = await client.get(f"{self._crystal_url}/api/crystal/{crystal_id}")
            resp.raise_for_status()
            data = resp.json()

            crystal = CrystalRecord(
                crystal_id=str(data.get("id", data.get("crystal_id", crystal_id))),
                topic=data.get("topic", data.get("title", "")),
                content=data.get("content", data.get("text", "")),
                category=data.get("category", ""),
                authority=int(data.get("authority", 1)),
                timestamp=data.get("timestamp", ""),
                metadata=data.get("metadata", {}),
            )
            self._cache.put(cache_key, crystal)
            return crystal

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Crystal get failed for '{crystal_id}': {e}")
            return None

    # ───────────────────────────────────────────────────────
    # EMBEDDING PIPELINE — Embed + search
    # ───────────────────────────────────────────────────────

    async def embed_and_search(
        self,
        text: str,
        index: str = "ekm",
        top_k: int = 10,
    ) -> List[EmbeddingResult]:
        """Embed text and search against a vectorize index."""
        cache_key = _cache_key("embed_search", text, index, top_k)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            resp = await client.post(
                f"{self._embedding_url}/api/embed-search",
                json={"text": text, "index": index, "top_k": top_k},
            )
            resp.raise_for_status()
            data = resp.json()

            results: List[EmbeddingResult] = []
            for item in data.get("results", data.get("matches", [])):
                results.append(EmbeddingResult(
                    id=str(item.get("id", "")),
                    text=item.get("text", item.get("content", "")),
                    score=float(item.get("score", item.get("similarity", 0.0))),
                    index=index,
                    metadata=item.get("metadata", {}),
                ))

            self._cache.put(cache_key, results)
            return results

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Embed+search failed: {e}")
            return []

    # ───────────────────────────────────────────────────────
    # KNOWLEDGE FORGE — 5,400+ docs, 12,500+ chunks
    # ───────────────────────────────────────────────────────

    async def search_forge(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 10,
    ) -> List[ForgeResult]:
        """Search Knowledge Forge for relevant documents and chunks."""
        cache_key = _cache_key("forge_search", query, category, limit)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            params: Dict[str, Any] = {"q": query, "limit": limit}
            if category:
                params["category"] = category

            resp = await client.get(f"{self._knowledge_forge_url}/search", params=params)
            resp.raise_for_status()
            data = resp.json()

            results: List[ForgeResult] = []
            for item in data.get("results", []):
                doc = item.get("document", {})
                results.append(ForgeResult(
                    doc_id=item.get("doc_id", doc.get("id", "")),
                    chunk_id=item.get("chunk_id", ""),
                    title=doc.get("title", item.get("title", "")),
                    snippet=item.get("snippet", item.get("content", "")),
                    section=item.get("section", ""),
                    category=doc.get("category", item.get("category", "")),
                    score=float(item.get("score", 0.0)),
                    tags=doc.get("tags", []),
                    source_path=doc.get("source_path", ""),
                ))

            self._cache.put(cache_key, results)
            logger.debug(f"Knowledge Forge returned {len(results)} results for '{query[:50]}...'")
            return results

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Knowledge Forge search failed: {e}")
            return []

    # ───────────────────────────────────────────────────────
    # SHARED BRAIN — Cross-instance memory + decisions
    # ───────────────────────────────────────────────────────

    async def search_brain(
        self,
        query: str,
        limit: int = 10,
    ) -> List[BrainMessage]:
        """Search Echo Shared Brain for relevant cross-instance knowledge."""
        cache_key = _cache_key("brain_search", query, limit)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            resp = await client.post(
                f"{self._shared_brain_url}/search",
                json={"query": query, "limit": limit},
            )
            resp.raise_for_status()
            data = resp.json()

            results: List[BrainMessage] = []
            for item in data.get("results", []):
                tags_raw = item.get("tags", "[]")
                if isinstance(tags_raw, str):
                    try:
                        import json as _json
                        tags_parsed = _json.loads(tags_raw)
                    except Exception:
                        tags_parsed = []
                else:
                    tags_parsed = tags_raw

                results.append(BrainMessage(
                    id=item.get("id", ""),
                    content=item.get("content", ""),
                    instance_id=item.get("instance_id", ""),
                    importance=int(item.get("importance", 5)),
                    tags=tags_parsed if isinstance(tags_parsed, list) else [],
                    created_at=item.get("created_at", ""),
                    score=float(item.get("score", 0.0)),
                ))

            self._cache.put(cache_key, results)
            logger.debug(f"Shared Brain returned {len(results)} results for '{query[:50]}...'")
            return results

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Shared Brain search failed: {e}")
            return []

    # ───────────────────────────────────────────────────────
    # MEMORY PRIME — 9-pillar memory system
    # ───────────────────────────────────────────────────────

    async def search_memory_prime(
        self,
        query: str,
        limit: int = 10,
    ) -> List[MemoryPrimeResult]:
        """Search Echo Memory Prime across all memory layers."""
        cache_key = _cache_key("memory_prime", query, limit)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            client = await self._get_client()
            self._request_count += 1
            resp = await client.get(
                f"{self._memory_prime_url}/recall",
                params={"query": query, "limit": limit},
            )
            resp.raise_for_status()
            data = resp.json()

            results: List[MemoryPrimeResult] = []
            for item in data.get("results", []):
                meta = item.get("metadata", {})
                tags_raw = meta.get("tags", "")
                if isinstance(tags_raw, str):
                    tags_list = [t.strip() for t in tags_raw.split(",") if t.strip()]
                else:
                    tags_list = tags_raw if isinstance(tags_raw, list) else []

                results.append(MemoryPrimeResult(
                    id=item.get("id", ""),
                    content=item.get("content", str(meta)),
                    category=meta.get("category", ""),
                    layer=item.get("layer", ""),
                    score=float(item.get("score", 0.0)),
                    tags=tags_list,
                    metadata=meta,
                ))

            self._cache.put(cache_key, results)
            logger.debug(f"Memory Prime returned {len(results)} results for '{query[:50]}...'")
            return results

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Memory Prime search failed: {e}")
            return []

    # ───────────────────────────────────────────────────────
    # SHADOWGLASS DEED RECORDS — Actual property records from D1
    # ───────────────────────────────────────────────────────

    _COUNTY_NAMES: List[str] = [
        "ECTOR", "MIDLAND", "REEVES", "WARD", "CRANE", "UPTON",
        "ANDREWS", "MARTIN", "HOWARD", "GLASSCOCK", "PECOS",
        "LOVING", "WINKLER", "CULBERSON", "JEFF DAVIS",
        "DALLAS", "HARRIS", "TARRANT", "BEXAR", "TRAVIS",
        "COLLIN", "DENTON", "GRAYSON", "WILLIAMSON", "LUBBOCK",
        "POTTER", "RANDALL", "TOM GREEN", "TAYLOR", "NOLAN",
        "SCURRY", "MITCHELL", "FISHER", "COKE", "STERLING",
        "IRION", "REAGAN", "CROCKETT", "TERRELL", "BREWSTER",
        "PRESIDIO", "HUDSPETH", "EL PASO", "LEA", "EDDY",
    ]

    _SECTION_PATTERN = re.compile(
        r"(?:section|sec\.?|s)\s*(\d+)", re.IGNORECASE
    )
    _BLOCK_PATTERN = re.compile(
        r"(?:block|blk\.?|bk\.?)\s*(\w+)", re.IGNORECASE
    )
    _LOT_PATTERN = re.compile(
        r"(?:lots?|lt\.?)\s*([\d,\s&]+)", re.IGNORECASE
    )
    _SURVEY_PATTERN = re.compile(
        r"(?:survey|abstract|abst?\.?|a-)\s*(\w+)", re.IGNORECASE
    )
    _TOWNSHIP_PATTERN = re.compile(
        r"(?:township|twp\.?|t)\s*(\w+)", re.IGNORECASE
    )

    def _extract_property_identifiers(self, query: str) -> Dict[str, str]:
        """Extract section, block, lot, survey, county from natural language query."""
        result: Dict[str, str] = {}
        query_lower = query.lower()

        # County
        for county in self._COUNTY_NAMES:
            if county.lower() in query_lower:
                result["county"] = county
                break
        if "county" not in result:
            # Default to REEVES for Permian Basin queries
            for kw in ["permian", "oil", "gas", "mineral", "deed", "lease", "title",
                        "chain of title", "ownership", "section", "block"]:
                if kw in query_lower:
                    result["county"] = "REEVES"
                    break

        # Section
        m = self._SECTION_PATTERN.search(query)
        if m:
            result["section"] = m.group(1)

        # Block
        m = self._BLOCK_PATTERN.search(query)
        if m:
            result["block"] = m.group(1)

        # Lot
        m = self._LOT_PATTERN.search(query)
        if m:
            result["lot"] = m.group(1).strip()

        # Survey / Abstract
        m = self._SURVEY_PATTERN.search(query)
        if m:
            result["survey"] = m.group(1)

        # Township
        m = self._TOWNSHIP_PATTERN.search(query)
        if m:
            result["township"] = m.group(1)

        return result

    async def search_deed_records(
        self,
        query: str,
        county: Optional[str] = None,
        section: Optional[str] = None,
        block: Optional[str] = None,
        limit: int = 50,
    ) -> List[DeedRecord]:
        """
        Search ShadowGlass analyzed deed records from D1 pipeline database.

        This searches the ALREADY-ANALYZED records (OCR'd, extracted, indexed)
        in ShadowGlass D1 — NOT live scraping. 113K+ Reeves, 223K+ Ector, 96K+ Midland.

        Hits two endpoints in parallel:
          - /pipeline/search — structured section/block/county search
          - /pipeline/cross-refs — chain of title / party history search
        """
        # Extract identifiers from natural language
        identifiers = self._extract_property_identifiers(query)
        search_county = county or identifiers.get("county", "")
        search_section = section or identifiers.get("section", "")
        search_block = block or identifiers.get("block", "")

        if not search_county and not search_section:
            logger.debug("No county or section found in query — skipping deed record search")
            return []

        cache_key = _cache_key("deed_records", search_county, search_section, search_block, query)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        records: List[DeedRecord] = []

        try:
            client = await self._get_client()

            # Build parallel requests
            tasks_to_run: List[Any] = []

            # 1. Pipeline search — structured property search
            if search_county:
                search_params: Dict[str, Any] = {
                    "county": search_county,
                    "limit": limit,
                }
                if search_section:
                    search_params["section"] = search_section
                if search_block:
                    search_params["block"] = search_block

                self._request_count += 1
                tasks_to_run.append(
                    client.get(
                        f"{self._shadowglass_url}/pipeline/search",
                        params=search_params,
                        timeout=httpx.Timeout(DEFAULT_TIMEOUT),
                    )
                )

            # 2. Cross-refs — chain of title search
            property_desc_parts = []
            if search_section:
                property_desc_parts.append(f"Section {search_section}")
            if search_block:
                property_desc_parts.append(f"Block {search_block}")
            if identifiers.get("lot"):
                property_desc_parts.append(f"Lot {identifiers['lot']}")

            if property_desc_parts:
                property_desc = " ".join(property_desc_parts)
                self._request_count += 1
                tasks_to_run.append(
                    client.get(
                        f"{self._shadowglass_url}/pipeline/cross-refs",
                        params={"property": property_desc, "limit": limit},
                        timeout=httpx.Timeout(DEFAULT_TIMEOUT),
                    )
                )

            if not tasks_to_run:
                return []

            # Fire in parallel
            responses = await asyncio.gather(*tasks_to_run, return_exceptions=True)

            seen_ids: Set[str] = set()

            for resp in responses:
                if isinstance(resp, Exception):
                    logger.warning(f"Deed record search request failed: {resp}")
                    continue

                if resp.status_code != 200:
                    logger.warning(f"Deed record search returned {resp.status_code}: {resp.text[:200]}")
                    continue

                data = resp.json()
                items = data.get("results", data.get("records", data.get("data", [])))
                if not isinstance(items, list):
                    items = []

                for item in items:
                    doc_id = str(item.get("document_id", item.get("id", item.get("doc_id", ""))))
                    if doc_id in seen_ids:
                        continue
                    seen_ids.add(doc_id)

                    records.append(DeedRecord(
                        document_id=doc_id,
                        county=str(item.get("county", search_county)),
                        instrument_type=str(item.get("instrument_type", item.get("doc_type", ""))),
                        grantor=str(item.get("grantor_extracted", item.get("grantor", ""))),
                        grantee=str(item.get("grantee_extracted", item.get("grantee", ""))),
                        date_filed=str(item.get("date_filed", item.get("filed_date", ""))),
                        date_executed=str(item.get("date_executed", item.get("execution_date", ""))),
                        section_block_survey=str(item.get("section_block_survey", "")),
                        legal_description=str(item.get("legal_description_extracted", item.get("legal_description", ""))),
                        consideration=str(item.get("consideration_extracted", item.get("consideration", ""))),
                        acreage=str(item.get("acreage_extracted", item.get("acreage", ""))),
                        mineral_interest_pct=str(item.get("mineral_interest_pct", "")),
                        royalty_interest_pct=str(item.get("royalty_interest_pct", "")),
                        volume_page=str(item.get("volume_page", item.get("vol_page", ""))),
                        ocr_confidence=float(item.get("ocr_confidence", 0.0)),
                        r2_pdf_key=str(item.get("r2_pdf_key", item.get("pdf_key", ""))),
                        metadata={
                            k: v for k, v in item.items()
                            if k not in {
                                "document_id", "id", "doc_id", "county", "instrument_type",
                                "doc_type", "grantor_extracted", "grantor", "grantee_extracted",
                                "grantee", "date_filed", "filed_date", "date_executed",
                                "execution_date", "section_block_survey", "legal_description_extracted",
                                "legal_description", "consideration_extracted", "consideration",
                                "acreage_extracted", "acreage", "mineral_interest_pct",
                                "royalty_interest_pct", "volume_page", "vol_page",
                                "ocr_confidence", "r2_pdf_key", "pdf_key",
                            }
                        },
                    ))

            self._cache.put(cache_key, records)
            logger.info(
                f"ShadowGlass deed search: {len(records)} records for "
                f"county={search_county} section={search_section} block={search_block}"
            )

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Deed record search failed: {e}")

        return records

    # ───────────────────────────────────────────────────────
    # INTELLIGENT SOURCE ROUTER — Knows WHERE to go for WHAT
    # ───────────────────────────────────────────────────────

    # Domain-specific source routing table. Each entry maps keywords/categories
    # to the EXACT source URLs and scraping strategies to use.
    _SOURCE_ROUTES: List[Dict[str, Any]] = [
        # ── OIL & GAS / COUNTY RECORDS ──
        # ShadowGlass has 80 counties wired up with full scraping protocols
        {
            "domain": "county_records",
            "keywords": [
                "deed", "lease", "oil", "gas", "mineral", "royalty", "assignment",
                "easement", "right of way", "lien", "deed of trust", "mortgage",
                "plat", "survey", "title", "conveyance", "county clerk",
                "grantor", "grantee", "warranty deed", "mineral deed", "ogl",
                "oil and gas lease", "division order", "pooling", "unitization",
                "section", "block", "township", "abstract", "well", "permit",
                "affidavit of heirship", "probate", "lis pendens", "ucc",
                "correction deed", "release", "ratification", "field notes",
            ],
            "categories": [
                "real_estate", "oil_gas", "land", "title", "mineral", "landman",
                "county", "deed", "lease", "survey",
            ],
            "strategy": "shadowglass_county",
            "description": "County clerk records via ShadowGlass 80-county scraper",
        },
        # ── TEXAS RAILROAD COMMISSION ──
        {
            "domain": "rrc_texas",
            "keywords": [
                "railroad commission", "rrc", "well completion", "drilling permit",
                "production data", "p-5", "w-2", "w-1", "h-15", "proration",
                "allowable", "operator", "api number", "well bore", "plugging",
                "injection well", "disposal well", "pipeline permit",
            ],
            "categories": ["rrc", "drilling", "production", "well"],
            "strategy": "web_scrape",
            "urls": [
                "https://www.rrc.texas.gov/oil-and-gas/",
                "https://webapps.rrc.texas.gov/",
            ],
            "description": "Texas Railroad Commission oil & gas data",
        },
        # ── TAX LAW / IRS ──
        {
            "domain": "tax_law",
            "keywords": [
                "irc", "internal revenue code", "section 1031", "section 199a",
                "deduction", "depreciation", "amortization", "tax credit",
                "irs", "treasury regulation", "revenue ruling", "revenue procedure",
                "tax court", "section 162", "section 263", "cost depletion",
                "percentage depletion", "intangible drilling cost", "idc",
                "passive activity", "at-risk", "like-kind exchange",
                "partnership", "s corporation", "llc tax", "basis",
                "capital gains", "ordinary income", "self-employment tax",
                "estimated tax", "withholding", "form 1099", "form w-2",
                "schedule c", "schedule e", "schedule k-1",
            ],
            "categories": ["tax", "irs", "irc", "federal_tax", "deduction", "credit"],
            "strategy": "web_scrape",
            "urls": [
                "https://www.law.cornell.edu/uscode/text/26",
                "https://www.irs.gov/",
                "https://www.ustaxcourt.gov/",
                "https://www.ecfr.gov/current/title-26",
            ],
            "description": "IRC, IRS guidance, Tax Court, CFR Title 26",
        },
        # ── GENERAL LAW / LEGAL RESEARCH ──
        {
            "domain": "legal_research",
            "keywords": [
                "statute", "regulation", "case law", "precedent", "ruling",
                "court opinion", "supreme court", "circuit court", "appeal",
                "plaintiff", "defendant", "liability", "negligence", "tort",
                "contract law", "breach", "damages", "injunction", "summary judgment",
                "ucc", "uniform commercial code", "restatement", "common law",
                "constitutional", "due process", "equal protection",
                "federal register", "cfr", "code of federal regulations",
                "annotated", "westlaw", "lexis",
            ],
            "categories": ["law", "legal", "statute", "regulation", "court", "case_law"],
            "strategy": "web_scrape",
            "urls": [
                "https://www.law.cornell.edu/",
                "https://scholar.google.com/",
                "https://www.justia.com/",
                "https://www.ecfr.gov/",
                "https://www.federalregister.gov/",
                "https://www.supremecourt.gov/opinions/opinions.aspx",
                "https://casetext.com/",
            ],
            "description": "Cornell LII, Google Scholar, Justia, eCFR, Federal Register",
        },
        # ── TEXAS STATE LAW ──
        {
            "domain": "texas_law",
            "keywords": [
                "texas property code", "texas natural resources code",
                "texas tax code", "texas water code", "texas civil practice",
                "texas business organizations code", "tceq", "texas constitution",
                "texas supreme court", "tex. civ. prac.", "tex. prop.",
                "tex. nat. res.", "texas statutes", "vernon's",
            ],
            "categories": ["texas_law", "texas", "state_law"],
            "strategy": "web_scrape",
            "urls": [
                "https://statutes.capitol.texas.gov/",
                "https://www.txcourts.gov/supreme/",
                "https://www.law.cornell.edu/states/texas",
                "https://search.txcourts.gov/",
            ],
            "description": "Texas statutes, court opinions, TCEQ",
        },
        # ── SEC / SECURITIES / CORPORATE FILINGS ──
        {
            "domain": "sec_filings",
            "keywords": [
                "sec filing", "10-k", "10-q", "8-k", "proxy statement",
                "edgar", "annual report", "quarterly report", "securities",
                "registration statement", "prospectus", "s-1", "form 4",
                "insider trading", "beneficial ownership", "13f",
                "material event", "current report",
            ],
            "categories": ["sec", "securities", "corporate", "edgar", "filing"],
            "strategy": "web_scrape",
            "urls": [
                "https://www.sec.gov/cgi-bin/browse-edgar",
                "https://efts.sec.gov/LATEST/search-index",
            ],
            "description": "SEC EDGAR filings, corporate disclosures",
        },
        # ── ACADEMIC / RESEARCH PAPERS ──
        {
            "domain": "academic",
            "keywords": [
                "research paper", "journal article", "peer reviewed",
                "abstract", "methodology", "literature review", "thesis",
                "dissertation", "arxiv", "ssrn", "doi", "citation",
                "university", "professor", "publication", "study",
            ],
            "categories": ["academic", "research", "paper", "university"],
            "strategy": "web_scrape",
            "urls": [
                "https://scholar.google.com/",
                "https://arxiv.org/",
                "https://papers.ssrn.com/",
                "https://www.jstor.org/",
            ],
            "description": "Google Scholar, arXiv, SSRN, JSTOR",
        },
        # ── REAL PROPERTY / APPRAISAL ──
        {
            "domain": "property_appraisal",
            "keywords": [
                "appraisal", "assessed value", "market value", "tax assessment",
                "property tax", "cad", "central appraisal district",
                "ad valorem", "homestead exemption", "protest",
                "comparable sales", "square footage", "land value",
                "improvement value", "tax rate", "mill rate",
            ],
            "categories": ["appraisal", "property_tax", "cad", "assessment"],
            "strategy": "web_scrape",
            "urls": [
                "https://www.midcad.org/",
                "https://www.reevescad.org/",
                "https://www.ectorcad.org/",
                "https://esearch.hcad.org/",
            ],
            "description": "County appraisal districts (MCAD, RCAD, ECAD, HCAD)",
        },
        # ── ENVIRONMENTAL / WATER RIGHTS ──
        {
            "domain": "environmental",
            "keywords": [
                "water rights", "groundwater", "surface water", "produced water",
                "injection well", "disposal", "tceq", "epa", "npdes",
                "clean water act", "safe drinking water", "aquifer",
                "water district", "conservation district", "ogallala",
                "environmental impact", "remediation", "contamination",
            ],
            "categories": ["water", "environmental", "tceq", "epa"],
            "strategy": "web_scrape",
            "urls": [
                "https://www.tceq.texas.gov/",
                "https://www.epa.gov/",
                "https://www.twdb.texas.gov/",
            ],
            "description": "TCEQ, EPA, TWDB water/environmental data",
        },
        # ── GIS / MAPPING / SURVEYS ──
        {
            "domain": "gis_mapping",
            "keywords": [
                "gis", "shapefile", "coordinates", "latitude", "longitude",
                "plat map", "survey", "boundary", "parcel", "lot",
                "metes and bounds", "quarter section", "range",
                "geographic", "aerial", "satellite", "topographic",
            ],
            "categories": ["gis", "mapping", "survey", "geospatial"],
            "strategy": "web_scrape",
            "urls": [
                "https://tnris.org/",
                "https://www.usgs.gov/",
                "https://gis.rrc.texas.gov/",
            ],
            "description": "TNRIS, USGS, RRC GIS — geographic/survey data",
        },
        # ── FINANCIAL / ECONOMICS ──
        {
            "domain": "financial",
            "keywords": [
                "interest rate", "inflation", "gdp", "unemployment",
                "commodity price", "crude oil price", "natural gas price",
                "wti", "henry hub", "futures", "options", "hedging",
                "financial statement", "balance sheet", "income statement",
                "cash flow", "valuation", "dcf", "npv", "irr",
            ],
            "categories": ["finance", "economics", "commodity", "pricing"],
            "strategy": "web_scrape",
            "urls": [
                "https://fred.stlouisfed.org/",
                "https://www.eia.gov/",
                "https://finance.yahoo.com/",
            ],
            "description": "FRED, EIA, financial data sources",
        },
    ]

    def _route_query(
        self, query: str, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Intelligently route a query to the best source(s) based on keywords
        and category. Returns matching routes sorted by relevance score.
        """
        query_lower = query.lower()
        category_lower = (category or "").lower()
        scored: List[Tuple[float, Dict[str, Any]]] = []

        for route in self._SOURCE_ROUTES:
            score = 0.0
            # Keyword matching
            keyword_hits = sum(1 for kw in route["keywords"] if kw in query_lower)
            score += keyword_hits * 2.0
            # Category matching
            if category_lower and category_lower in route.get("categories", []):
                score += 5.0
            # Partial keyword matching (word-level)
            query_words = set(query_lower.split())
            for kw in route["keywords"]:
                kw_words = set(kw.split())
                overlap = len(query_words & kw_words)
                if overlap > 0:
                    score += overlap * 0.5

            if score > 0:
                scored.append((score, route))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [route for _, route in scored[:3]]  # top 3 matching routes

    # ───────────────────────────────────────────────────────
    # SHADOWGLASS WARPSPEED — Intelligent auto-scrape
    # ───────────────────────────────────────────────────────

    async def _auto_scrape_and_store(
        self,
        query: str,
        category: Optional[str] = None,
    ) -> List[ScrapeResult]:
        """
        Intelligent auto-scrape: analyzes the query, determines the RIGHT
        source to scrape, goes there, gets the data, and stores it.

        For county records: hits ShadowGlass /scrape endpoint directly
        For law/tax/academic: scrapes authoritative source websites
        For general: falls back to search engine scrape

        All results stored in Knowledge Forge + Shared Brain for next time.
        """
        logger.info(f"INTELLIGENT AUTO-SCRAPE triggered for '{query[:80]}'")

        scrape_results: List[ScrapeResult] = []
        client = await self._get_client()

        # Step 1: Route query to the best sources
        routes = self._route_query(query, category)

        if routes:
            logger.info(
                f"Routed to {len(routes)} source(s): "
                + ", ".join(r['domain'] for r in routes)
            )
        else:
            logger.info("No specific route matched — falling back to search engine scrape")

        # Step 2: Execute scrapes based on route strategy
        for route in routes:
            strategy = route.get("strategy", "web_scrape")

            if strategy == "shadowglass_county":
                # Use ShadowGlass county scraper directly
                scrape_results.extend(
                    await self._scrape_county_records(client, query, route)
                )

            elif strategy == "web_scrape":
                # Scrape authoritative websites via ShadowGlass browser rendering
                scrape_results.extend(
                    await self._scrape_authoritative_sources(client, query, route)
                )

        # Step 3: If no routes matched or routes returned nothing, fallback to search
        if not scrape_results:
            logger.info("Route scrapes returned nothing — falling back to search engine")
            scrape_results.extend(
                await self._scrape_search_engine(client, query)
            )

        # Step 4: Store ALL scraped content in Knowledge Forge for future queries
        await self._store_scrape_results(client, scrape_results, query, category)

        return scrape_results

    async def _scrape_county_records(
        self,
        client: httpx.AsyncClient,
        query: str,
        route: Dict[str, Any],
    ) -> List[ScrapeResult]:
        """Scrape county clerk records via ShadowGlass /scrape endpoint."""
        results: List[ScrapeResult] = []
        try:
            # Extract county name and instrument type from query
            query_lower = query.lower()

            # Try to find county name in query
            county_name = None
            # Common Permian Basin counties
            counties = [
                "ECTOR", "MIDLAND", "REEVES", "WARD", "CRANE", "UPTON",
                "ANDREWS", "MARTIN", "HOWARD", "GLASSCOCK", "PECOS",
                "LOVING", "WINKLER", "CULBERSON", "JEFF DAVIS",
                "DALLAS", "HARRIS", "TARRANT", "BEXAR", "TRAVIS",
                "COLLIN", "DENTON", "GRAYSON", "WILLIAMSON",
            ]
            for c in counties:
                if c.lower() in query_lower:
                    county_name = c
                    break

            # Determine instrument type
            instrument_code = None
            instrument_map = {
                "oil and gas lease": "OGL", "ogl": "OGL", "lease": "OGL",
                "mineral deed": "MINERAL_DEED", "deed": "DEED",
                "warranty deed": "WARRANTY_DEED", "assignment": "ASSIGNMENT",
                "easement": "EASEMENT", "right of way": "ROW",
                "royalty deed": "ROYALTY_DEED", "deed of trust": "DOT",
                "lien": "LIEN", "release": "RELEASE", "plat": "PLAT",
                "affidavit of heirship": "AOH", "probate": "PROBATE",
                "ucc": "UCC", "mortgage": "MORTGAGE",
            }
            for keyword, code in instrument_map.items():
                if keyword in query_lower:
                    instrument_code = code
                    break

            if not county_name:
                logger.info("No county name found in query — skipping county scrape")
                return results

            # Extract grantor/grantee name if present
            # Look for patterns like "name: Smith" or just proper names
            grantor = ""
            for pattern in ["grantor:", "from:", "by:", "name:"]:
                if pattern in query_lower:
                    idx = query_lower.index(pattern) + len(pattern)
                    grantor = query[idx:].strip().split(",")[0].split(" and ")[0].strip()[:50]
                    break

            self._request_count += 1
            scrape_payload: Dict[str, Any] = {
                "county": county_name,
            }
            if instrument_code:
                scrape_payload["instrument"] = instrument_code
            if grantor:
                scrape_payload["grantor"] = grantor

            logger.info(f"ShadowGlass county scrape: {county_name}, instrument={instrument_code}, grantor={grantor}")

            resp = await client.post(
                f"{self._shadowglass_url}/scrape",
                json=scrape_payload,
                timeout=httpx.Timeout(SCRAPE_TIMEOUT),
            )

            if resp.status_code == 200:
                data = resp.json()
                records = data.get("data", data.get("records", data.get("results", [])))
                if isinstance(records, list):
                    for rec in records[:20]:
                        content_parts = []
                        for key in ["grantor", "grantee", "instrument_type", "date_filed",
                                    "book", "page", "legal_description", "consideration"]:
                            val = rec.get(key, "")
                            if val:
                                content_parts.append(f"{key}: {val}")

                        results.append(ScrapeResult(
                            url=f"shadowglass://{county_name}/{rec.get('doc_id', rec.get('id', ''))}",
                            title=f"{county_name} County - {rec.get('instrument_type', instrument_code or 'Record')} - {rec.get('grantor', '')}",
                            content="\n".join(content_parts) if content_parts else str(rec)[:2000],
                            scraped_at=rec.get("date_filed", ""),
                            stored_in="knowledge_forge",
                        ))

                    logger.info(f"County scrape returned {len(results)} records from {county_name}")
                else:
                    # Single result or text content
                    results.append(ScrapeResult(
                        url=f"shadowglass://{county_name}/search",
                        title=f"{county_name} County Records Search",
                        content=str(data)[:5000],
                        scraped_at="",
                        stored_in="knowledge_forge",
                    ))
            else:
                logger.warning(f"County scrape returned {resp.status_code}: {resp.text[:200]}")

        except Exception as e:
            self._error_count += 1
            logger.warning(f"County scrape failed: {e}")

        return results

    async def _scrape_authoritative_sources(
        self,
        client: httpx.AsyncClient,
        query: str,
        route: Dict[str, Any],
    ) -> List[ScrapeResult]:
        """Scrape authoritative websites via ShadowGlass browser rendering."""
        results: List[ScrapeResult] = []
        urls = route.get("urls", [])

        # Build search query for each authoritative source
        encoded_query = query.replace(" ", "+")

        for base_url in urls[:2]:  # limit to 2 sources per route
            try:
                # Some sites have search endpoints, others we need to construct URLs
                if "scholar.google.com" in base_url:
                    scrape_url = f"https://scholar.google.com/scholar?q={encoded_query}"
                elif "law.cornell.edu" in base_url:
                    scrape_url = f"https://www.law.cornell.edu/search#tab_siteall?{encoded_query}"
                elif "justia.com" in base_url:
                    scrape_url = f"https://www.justia.com/search?q={encoded_query}"
                elif "ecfr.gov" in base_url:
                    scrape_url = f"https://www.ecfr.gov/search?query={encoded_query}"
                elif "irs.gov" in base_url:
                    scrape_url = f"https://www.irs.gov/search#q={encoded_query}"
                elif "sec.gov" in base_url:
                    scrape_url = f"https://efts.sec.gov/LATEST/search-index?q={encoded_query}&dateRange=custom&startdt=2020-01-01"
                elif "fred.stlouisfed.org" in base_url:
                    scrape_url = f"https://fred.stlouisfed.org/searchresults/?st={encoded_query}"
                elif "eia.gov" in base_url:
                    scrape_url = f"https://www.eia.gov/search/?q={encoded_query}"
                elif "statutes.capitol.texas.gov" in base_url:
                    scrape_url = f"https://statutes.capitol.texas.gov/Search.aspx?q={encoded_query}"
                elif "arxiv.org" in base_url:
                    scrape_url = f"https://arxiv.org/search/?query={encoded_query}&searchtype=all"
                elif "ssrn.com" in base_url:
                    scrape_url = f"https://papers.ssrn.com/sol3/results.cfm?txtKey_Words={encoded_query}"
                else:
                    scrape_url = base_url

                self._request_count += 1
                resp = await client.post(
                    f"{self._shadowglass_url}/scrape/direct",
                    json={"url": scrape_url, "extract_text": True, "timeout_ms": 20000},
                    timeout=httpx.Timeout(SCRAPE_TIMEOUT),
                )

                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("text", data.get("content", data.get("body", "")))
                    title = data.get("title", route.get("description", query))

                    if content and len(content) > 100:
                        results.append(ScrapeResult(
                            url=scrape_url,
                            title=f"[{route['domain']}] {title[:180]}",
                            content=content[:5000],
                            scraped_at="",
                            stored_in="knowledge_forge",
                        ))
                        logger.info(f"Scraped {len(content)} chars from {route['domain']}: {scrape_url[:80]}")
                else:
                    logger.warning(f"Authoritative scrape {resp.status_code} for {scrape_url[:80]}")

            except Exception as e:
                logger.warning(f"Authoritative scrape failed for {base_url}: {e}")

        return results

    async def _scrape_search_engine(
        self,
        client: httpx.AsyncClient,
        query: str,
    ) -> List[ScrapeResult]:
        """Fallback: scrape search engine results when no specific route matches."""
        results: List[ScrapeResult] = []
        encoded_query = query.replace(" ", "+")
        search_url = f"https://duckduckgo.com/?q={encoded_query}"

        try:
            self._request_count += 1
            resp = await client.post(
                f"{self._shadowglass_url}/scrape/direct",
                json={"url": search_url, "extract_text": True, "timeout_ms": 15000},
                timeout=httpx.Timeout(SCRAPE_TIMEOUT),
            )

            if resp.status_code == 200:
                data = resp.json()
                content = data.get("text", data.get("content", data.get("body", "")))
                title = data.get("title", query)
                if content and len(content) > 100:
                    results.append(ScrapeResult(
                        url=search_url,
                        title=title[:200],
                        content=content[:5000],
                        scraped_at="",
                        stored_in="knowledge_forge",
                    ))
        except Exception as e:
            self._error_count += 1
            logger.warning(f"Search engine scrape failed: {e}")

        return results

    async def _store_scrape_results(
        self,
        client: httpx.AsyncClient,
        scrape_results: List[ScrapeResult],
        query: str,
        category: Optional[str] = None,
    ) -> None:
        """Store all scraped content in Knowledge Forge + Shared Brain."""
        for sr in scrape_results:
            # Store in Knowledge Forge
            try:
                forge_category = category.upper() if category else "AUTO_SCRAPED"
                await client.post(
                    f"{self._knowledge_forge_url}/ingest",
                    json={
                        "title": sr.title,
                        "content": sr.content,
                        "category": forge_category,
                        "subcategory": "auto_scraped",
                        "doc_type": "web_scrape",
                        "tags": ["auto_scraped", "shadowglass", query[:50].lower().replace(" ", "_")],
                        "source_path": sr.url,
                    },
                    timeout=httpx.Timeout(15.0),
                )
                logger.info(f"Stored in Knowledge Forge: {sr.title[:60]}")
            except Exception as e:
                logger.warning(f"Failed to store in Forge: {e}")

        # Store combined summary in Shared Brain
        if scrape_results:
            try:
                combined = "\n".join(
                    f"[{sr.title}]: {sr.content[:500]}" for sr in scrape_results[:5]
                )
                await client.post(
                    f"{self._shared_brain_url}/ingest",
                    json={
                        "instance_id": "cloud_retriever_auto_scrape",
                        "role": "system",
                        "content": f"AUTO-SCRAPED for '{query}': {combined[:3000]}",
                        "importance": 6,
                        "tags": ["auto_scraped", "knowledge_gap"],
                    },
                    timeout=httpx.Timeout(10.0),
                )
            except Exception as e:
                logger.warning(f"Failed to store in Shared Brain: {e}")

    # ───────────────────────────────────────────────────────
    # ENGINE MATRIX — Cross-engine queries
    # ───────────────────────────────────────────────────────

    async def execute_engine(
        self,
        tier: str,
        engine_id: str,
        query: str,
    ) -> Dict[str, Any]:
        """Execute a query on another engine via the engine matrix."""
        try:
            client = await self._get_client()
            self._request_count += 1
            resp = await client.post(
                f"{self._engine_matrix_url}/api/execute",
                json={"tier": tier, "engine_id": engine_id, "query": query},
            )
            resp.raise_for_status()
            return resp.json()

        except Exception as e:
            self._error_count += 1
            logger.warning(f"Engine matrix execute failed ({tier}/{engine_id}): {e}")
            return {"error": str(e), "engine_id": engine_id}

    # ───────────────────────────────────────────────────────
    # COMPOSITE — Multi-source retrieval
    # ───────────────────────────────────────────────────────

    async def retrieve_all(
        self,
        query: str,
        category: Optional[str] = None,
        graph_node_id: Optional[str] = None,
        include_crystals: bool = True,
        include_embeddings: bool = False,
        include_forge: bool = True,
        include_brain: bool = True,
        include_memory_prime: bool = True,
        include_deed_records: bool = True,
        auto_scrape_on_miss: Optional[bool] = None,
        ekm_limit: int = 15,
        crystal_limit: int = 5,
        forge_limit: int = 10,
        brain_limit: int = 5,
        memory_limit: int = 5,
        deed_limit: int = 50,
    ) -> CloudKnowledge:
        """
        Retrieve knowledge from ALL cloud sources in parallel.
        BLAZING FAST: L1 cache returns in <1ms for repeated queries.

        Flow:
          1. L1 CACHE CHECK — normalized query lookup, sub-millisecond
          2. PARALLEL FIRE — all 8 sources at once with tiered timeouts
          3. AUTO-SCRAPE FALLBACK — ShadowGlass Warpspeed if nothing found
          4. L1 CACHE STORE — cache full response for future queries
          5. ASYNC TELEMETRY — report query to Memory Prime + Shared Brain (non-blocking)
        """
        start = time.monotonic()
        self._total_query_count += 1

        # ─── L1 CACHE: SUB-MILLISECOND RETURN ───
        l1_result = self._l1_cache.get(query, category)
        if l1_result is not None:
            self._l1_hit_count += 1
            elapsed = round((time.monotonic() - start) * 1000, 4)
            # Update timing on the cached copy
            l1_result.retrieval_time_ms = elapsed
            l1_result.from_cache = True
            logger.debug(f"L1 CACHE HIT: {l1_result.total_records} records in {elapsed}ms")
            # Fire-and-forget telemetry even for cache hits
            if self._telemetry:
                asyncio.ensure_future(self._report_telemetry(query, category, l1_result))
            return l1_result

        # ─── L2 / NETWORK: PARALLEL FETCH ───
        sources_queried: List[str] = []
        sources_succeeded: List[str] = []
        sources_failed: List[str] = []

        # Determine auto-scrape behavior
        should_scrape = auto_scrape_on_miss if auto_scrape_on_miss is not None else self._auto_scrape

        # Build parallel tasks — ALL sources at once
        tasks: Dict[str, Any] = {}

        # Always search EKM
        sources_queried.append("ekm")
        tasks["ekm"] = self.search_clauses(query, category=category, limit=ekm_limit)

        # Graph search
        sources_queried.append("graph")
        if graph_node_id:
            tasks["graph"] = self.graph_neighbors(graph_node_id, depth=2)
        else:
            tasks["graph"] = self.graph_search(query, limit=10)

        # Crystal memory
        if include_crystals:
            sources_queried.append("crystal")
            tasks["crystal"] = self.search_crystals(query, category=category)

        # Knowledge Forge
        if include_forge:
            sources_queried.append("forge")
            tasks["forge"] = self.search_forge(query, category=category, limit=forge_limit)

        # Shared Brain
        if include_brain:
            sources_queried.append("brain")
            tasks["brain"] = self.search_brain(query, limit=brain_limit)

        # Memory Prime
        if include_memory_prime:
            sources_queried.append("memory_prime")
            tasks["memory_prime"] = self.search_memory_prime(query, limit=memory_limit)

        # Embedding search
        if include_embeddings:
            sources_queried.append("embedding")
            tasks["embedding"] = self.embed_and_search(query, top_k=10)

        # ShadowGlass deed records — actual property records from D1
        if include_deed_records:
            sources_queried.append("shadowglass_records")
            tasks["deed_records"] = self.search_deed_records(query, limit=deed_limit)

        # Execute ALL in parallel
        keys = list(tasks.keys())
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        # Process results
        cloud = CloudKnowledge(sources_queried=sources_queried)

        for key, result in zip(keys, results):
            if isinstance(result, Exception):
                sources_failed.append(key)
                logger.warning(f"Cloud source '{key}' failed: {result}")
                continue

            sources_succeeded.append(key)

            if key == "ekm" and isinstance(result, list):
                cloud.clauses = result[:ekm_limit]
            elif key == "graph":
                if isinstance(result, GraphNeighborhood):
                    cloud.graph_nodes = result.nodes
                    cloud.graph_edges = result.edges
                elif isinstance(result, list):
                    cloud.graph_nodes = result
            elif key == "crystal" and isinstance(result, list):
                cloud.crystals = result[:crystal_limit]
            elif key == "embedding" and isinstance(result, list):
                cloud.embeddings = result
            elif key == "forge" and isinstance(result, list):
                cloud.forge_results = result[:forge_limit]
            elif key == "brain" and isinstance(result, list):
                cloud.brain_messages = result[:brain_limit]
            elif key == "memory_prime" and isinstance(result, list):
                cloud.memory_results = result[:memory_limit]
            elif key == "deed_records" and isinstance(result, list):
                cloud.deed_records = result[:deed_limit]

        cloud.sources_succeeded = sources_succeeded
        cloud.sources_failed = sources_failed
        cloud.total_records = (
            len(cloud.clauses) + len(cloud.graph_nodes) + len(cloud.crystals)
            + len(cloud.embeddings) + len(cloud.forge_results)
            + len(cloud.brain_messages) + len(cloud.memory_results)
            + len(cloud.deed_records)
        )

        # ─── AUTO-SCRAPE FALLBACK ───
        # If we found almost nothing across ALL sources, scrape the web
        if should_scrape and cloud.total_records < MIN_RESULTS_THRESHOLD:
            logger.info(
                f"Only {cloud.total_records} results found across {len(sources_succeeded)} sources. "
                f"Triggering ShadowGlass auto-scrape for '{query[:60]}...'"
            )
            sources_queried.append("shadowglass_scrape")
            try:
                scrape_results = await self._auto_scrape_and_store(query, category=category)
                if scrape_results:
                    cloud.scrape_results = scrape_results
                    cloud.auto_scraped = True
                    cloud.total_records += len(scrape_results)
                    sources_succeeded.append("shadowglass_scrape")
                    logger.info(f"Auto-scrape added {len(scrape_results)} results")
                else:
                    sources_failed.append("shadowglass_scrape")
            except Exception as e:
                sources_failed.append("shadowglass_scrape")
                logger.warning(f"Auto-scrape failed: {e}")

            cloud.sources_queried = sources_queried
            cloud.sources_succeeded = sources_succeeded
            cloud.sources_failed = sources_failed

        cloud.retrieval_time_ms = round((time.monotonic() - start) * 1000, 2)
        self._total_latency_ms += cloud.retrieval_time_ms

        # ─── L1 CACHE STORE — cache for next time ───
        self._l1_cache.put(query, category, cloud)

        logger.info(
            f"Cloud retrieval: {cloud.total_records} records from "
            f"{len(sources_succeeded)}/{len(sources_queried)} sources "
            f"in {cloud.retrieval_time_ms}ms"
            f"{' [AUTO-SCRAPED]' if cloud.auto_scraped else ''}"
        )

        # ─── ASYNC TELEMETRY — fire-and-forget, does NOT slow response ───
        if self._telemetry:
            asyncio.ensure_future(self._report_telemetry(query, category, cloud))

        return cloud

    # ───────────────────────────────────────────────────────
    # ASYNC TELEMETRY — Report every query to Memory systems
    # ───────────────────────────────────────────────────────

    async def _report_telemetry(
        self,
        query: str,
        category: Optional[str],
        cloud: CloudKnowledge,
    ) -> None:
        """
        Fire-and-forget: report every engine knowledge query to Memory Prime
        and Shared Brain. Non-blocking — runs after response is already returned.

        Reports to all 9 pillars where applicable:
          - Memory Prime /store (crystal creation for audit trail)
          - Shared Brain /ingest (cross-instance awareness)
        """
        try:
            client = await self._get_client()

            telemetry_content = (
                f"KNOWLEDGE_QUERY: \"{query[:200]}\" | "
                f"category={category or 'none'} | "
                f"results={cloud.total_records} | "
                f"sources={','.join(cloud.sources_succeeded)} | "
                f"failed={','.join(cloud.sources_failed) or 'none'} | "
                f"latency={cloud.retrieval_time_ms}ms | "
                f"cached={cloud.from_cache} | "
                f"scraped={cloud.auto_scraped}"
            )

            telemetry_tags = [
                "telemetry", "knowledge_query",
                category or "uncategorized",
            ]
            if cloud.from_cache:
                telemetry_tags.append("cache_hit")
            if cloud.auto_scraped:
                telemetry_tags.append("auto_scraped")

            # Report to Memory Prime (9-pillar crystal creation)
            memory_task = client.post(
                f"{self._memory_prime_url}/store",
                json={
                    "category": "telemetry",
                    "content": telemetry_content,
                    "tags": telemetry_tags,
                    "metadata": {
                        "query": query[:500],
                        "category": category or "",
                        "total_records": cloud.total_records,
                        "sources_succeeded": cloud.sources_succeeded,
                        "sources_failed": cloud.sources_failed,
                        "latency_ms": cloud.retrieval_time_ms,
                        "from_cache": cloud.from_cache,
                        "auto_scraped": cloud.auto_scraped,
                    },
                },
                timeout=httpx.Timeout(5.0),
            )

            # Report to Shared Brain (cross-instance)
            brain_task = client.post(
                f"{self._shared_brain_url}/ingest",
                json={
                    "instance_id": "cloud_retriever_telemetry",
                    "role": "system",
                    "content": telemetry_content,
                    "importance": 3,  # low importance for telemetry
                    "tags": telemetry_tags,
                },
                timeout=httpx.Timeout(5.0),
            )

            # Fire both in parallel, don't wait for response
            await asyncio.gather(memory_task, brain_task, return_exceptions=True)

        except Exception as e:
            # Telemetry failure NEVER blocks engine operation
            logger.debug(f"Telemetry report failed (non-blocking): {e}")

    # ───────────────────────────────────────────────────────
    # STATS / HEALTH
    # ───────────────────────────────────────────────────────

    @property
    def stats(self) -> Dict[str, Any]:
        return {
            "total_queries": self._total_query_count,
            "requests": self._request_count,
            "errors": self._error_count,
            "error_rate": round(self._error_count / max(self._request_count, 1), 3),
            "l1_cache": self._l1_cache.stats,
            "l2_cache": self._cache.stats,
            "l1_hit_count": self._l1_hit_count,
            "l1_hit_rate": round(self._l1_hit_count / max(self._total_query_count, 1), 3),
            "avg_latency_ms": round(self._total_latency_ms / max(self._total_query_count - self._l1_hit_count, 1), 2),
        }


# ═══════════════════════════════════════════════════════════════════
# MODULE-LEVEL SINGLETON
# ═══════════════════════════════════════════════════════════════════

_default_retriever: Optional[CognitionCloudRetriever] = None


def get_cloud_retriever() -> CognitionCloudRetriever:
    """Get or create the module-level singleton retriever."""
    global _default_retriever
    if _default_retriever is None:
        _default_retriever = CognitionCloudRetriever()
    return _default_retriever


# ═══════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTION — One-shot retrieval for any engine
# ═══════════════════════════════════════════════════════════════════

async def retrieve_cloud_knowledge(
    query: str,
    category: Optional[str] = None,
    graph_node_id: Optional[str] = None,
    auto_scrape: Optional[bool] = None,
) -> CloudKnowledge:
    """
    One-call convenience function for cloud retrieval.

    Searches ALL 8 knowledge sources in parallel. If nothing found and
    auto_scrape is enabled, automatically scrapes the web via ShadowGlass
    Warpspeed Worker and stores results in Knowledge Forge.

    Usage in any engine:
        from cloud_retriever import retrieve_cloud_knowledge
        cloud = await retrieve_cloud_knowledge("title chain analysis", category="real_estate")
        print(cloud.merged_text())  # up to 8000 chars of aggregated knowledge
        print(cloud.citation_list())  # structured citations from all sources
        print(f"Auto-scraped: {cloud.auto_scraped}")  # True if web was scraped
    """
    retriever = get_cloud_retriever()
    return await retriever.retrieve_all(
        query,
        category=category,
        graph_node_id=graph_node_id,
        auto_scrape_on_miss=auto_scrape,
    )
