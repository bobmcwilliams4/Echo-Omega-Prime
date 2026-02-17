"""
R09 - Vector Search Fallback Module
Semantic retrieval when doctrine cache misses
"""

from typing import List, Dict, Any
import math
from doctrines import DOCTRINE_BLOCKS


def compute_tfidf_score(query_terms: List[str], document_terms: List[str]) -> float:
    """
    Compute TF-IDF score for query against document

    Args:
        query_terms: List of query keywords
        document_terms: List of document keywords

    Returns:
        TF-IDF similarity score
    """
    if not query_terms or not document_terms:
        return 0.0

    # Term frequency in document
    doc_term_freq = {}
    for term in document_terms:
        doc_term_freq[term] = doc_term_freq.get(term, 0) + 1

    # Calculate score
    score = 0.0
    for query_term in query_terms:
        if query_term in doc_term_freq:
            tf = doc_term_freq[query_term] / len(document_terms)
            # Simplified IDF (would use corpus stats in production)
            idf = math.log(len(DOCTRINE_BLOCKS) / (1 + sum(1 for b in DOCTRINE_BLOCKS if query_term in b.keywords)))
            score += tf * idf

    return score


def vector_search_fallback(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Fallback semantic search when doctrine cache misses

    Args:
        query: Normalized query string
        top_k: Number of results to return

    Returns:
        List of matching doctrine blocks with scores
    """
    query_terms = query.lower().split()

    results = []

    for block in DOCTRINE_BLOCKS:
        # Combine keywords and topic for matching
        doc_terms = block.keywords + [block.topic]
        doc_text = ' '.join(doc_terms).lower()

        # Calculate similarity score
        score = compute_tfidf_score(query_terms, doc_text.split())

        # Boost score if exact topic match
        if block.topic in query:
            score *= 1.5

        # Boost by confidence level
        confidence_multiplier = {
            "high": 1.2,
            "medium": 1.0,
            "low": 0.8,
            "speculative": 0.5
        }
        score *= confidence_multiplier.get(block.confidence.value, 1.0)

        if score > 0:
            results.append({
                "topic": block.topic,
                "category": block.category.value,
                "score": score,
                "keywords": block.keywords,
                "confidence": block.confidence.value
            })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]


def keyword_search(keyword: str) -> List[Dict[str, Any]]:
    """
    Simple keyword search across doctrine blocks

    Args:
        keyword: Single keyword to search

    Returns:
        List of matching blocks
    """
    keyword_lower = keyword.lower()
    matches = []

    for block in DOCTRINE_BLOCKS:
        # Check if keyword in topic or keywords list
        if keyword_lower in block.topic.lower():
            matches.append({
                "topic": block.topic,
                "category": block.category.value,
                "match_type": "topic",
                "confidence": block.confidence.value
            })
        elif any(keyword_lower in kw.lower() for kw in block.keywords):
            matches.append({
                "topic": block.topic,
                "category": block.category.value,
                "match_type": "keyword",
                "confidence": block.confidence.value
            })

    return matches


def category_search(category: str) -> List[Dict[str, Any]]:
    """
    Search by issue category

    Args:
        category: IssueCategory value

    Returns:
        All blocks in that category
    """
    matches = []

    for block in DOCTRINE_BLOCKS:
        if block.category.value == category:
            matches.append({
                "topic": block.topic,
                "category": block.category.value,
                "keywords": block.keywords,
                "confidence": block.confidence.value
            })

    return matches


def hybrid_search(query: str, category_filter: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Hybrid search combining vector and keyword approaches

    Args:
        query: Search query
        category_filter: Optional category to filter
        top_k: Number of results

    Returns:
        Combined ranked results
    """
    # Get vector search results
    vector_results = vector_search_fallback(query, top_k=top_k * 2)

    # Get keyword results
    query_terms = query.lower().split()
    keyword_results = []
    for term in query_terms:
        keyword_results.extend(keyword_search(term))

    # Combine and deduplicate
    combined = {}
    for result in vector_results:
        topic = result["topic"]
        combined[topic] = {
            **result,
            "vector_score": result["score"],
            "keyword_match": False
        }

    for result in keyword_results:
        topic = result["topic"]
        if topic in combined:
            combined[topic]["keyword_match"] = True
            combined[topic]["vector_score"] *= 1.3  # Boost if both match
        else:
            combined[topic] = {
                **result,
                "vector_score": 0.5,
                "keyword_match": True
            }

    # Filter by category if specified
    if category_filter:
        combined = {k: v for k, v in combined.items() if v["category"] == category_filter}

    # Sort by combined score
    results = list(combined.values())
    results.sort(key=lambda x: x["vector_score"], reverse=True)

    return results[:top_k]
