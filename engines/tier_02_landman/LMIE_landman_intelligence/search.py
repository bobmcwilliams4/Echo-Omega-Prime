"""
LMIE Search Module — Vector and keyword search for landman doctrines.

Provides TIE Component 7 (vector search) with local fallback when
cloud embedding pipeline is unavailable.

Commander: Bobby Don McWilliams II | Authority: 11.0 SOVEREIGN
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger


# ═══════════════════════════════════════════════════════════════════
# KEYWORD SEARCH — Local doctrine search fallback
# ═══════════════════════════════════════════════════════════════════

def keyword_score(query: str, text: str) -> float:
    """Score relevance of text to query using keyword overlap."""
    q_words = set(re.findall(r"\w+", query.lower()))
    t_words = set(re.findall(r"\w+", text.lower()))
    if not q_words:
        return 0.0
    overlap = q_words & t_words
    return len(overlap) / len(q_words)


def search_doctrines(
    query: str,
    doctrine_cache: Dict[str, Any],
    limit: int = 10,
    min_score: float = 0.1,
) -> List[Dict[str, Any]]:
    """Search doctrine cache by keyword relevance."""
    results: List[Tuple[float, str, Any]] = []

    for topic, block in doctrine_cache.items():
        # Score against keywords, conclusion, and topic name
        kw_text = " ".join(getattr(block, "keywords", []))
        conclusion = getattr(block, "conclusion_template", "")
        full_text = f"{topic} {kw_text} {conclusion}"

        score = keyword_score(query, full_text)
        if score >= min_score:
            results.append((score, topic, block))

    results.sort(key=lambda x: x[0], reverse=True)

    return [
        {
            "topic": topic,
            "score": round(score, 4),
            "conclusion": getattr(block, "conclusion_template", "")[:300],
            "keywords": getattr(block, "keywords", []),
            "authority": getattr(block, "primary_authority", []),
        }
        for score, topic, block in results[:limit]
    ]


def search_by_category(
    category: str,
    doctrine_cache: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Search doctrines by issue category."""
    results: List[Dict[str, Any]] = []

    for topic, block in doctrine_cache.items():
        categories = getattr(block, "issue_categories", [])
        cat_values = [c.value if hasattr(c, "value") else str(c) for c in categories]
        if category.upper() in cat_values:
            results.append({
                "topic": topic,
                "conclusion": getattr(block, "conclusion_template", "")[:300],
                "keywords": getattr(block, "keywords", []),
                "categories": cat_values,
            })

    return results


def search_by_authority(
    authority_query: str,
    doctrine_cache: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Search doctrines by controlling authority citation."""
    results: List[Dict[str, Any]] = []
    q_lower = authority_query.lower()

    for topic, block in doctrine_cache.items():
        authorities = getattr(block, "primary_authority", [])
        for auth in authorities:
            if q_lower in auth.lower():
                results.append({
                    "topic": topic,
                    "matched_authority": auth,
                    "all_authorities": authorities,
                    "conclusion": getattr(block, "conclusion_template", "")[:200],
                })
                break

    return results


logger.info("LMIE search module loaded")
