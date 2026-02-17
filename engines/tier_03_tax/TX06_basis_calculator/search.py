"""
TX06 Basis Calculator - Vector Search (Fallback)
Semantic retrieval when doctrine cache misses
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class SearchResult:
    """Search result with relevance score"""
    topic: str
    content: str
    relevance_score: float
    authority: List[str]
    keywords: List[str]


class VectorSearch:
    """Semantic search for basis calculation doctrine"""

    def __init__(self):
        self.index_path = Path(__file__).parent / "vector_index.json"
        self.index = self._load_or_create_index()

    def _load_or_create_index(self) -> Dict[str, Any]:
        """Load existing index or create new"""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass

        # Create default index structure
        return {
            "version": "1.0.0",
            "documents": [],
            "inverted_index": {},
            "last_updated": None
        }

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.3
    ) -> List[SearchResult]:
        """
        Semantic search for relevant basis doctrine

        In production, this would use:
        - Embedding model (e.g., sentence-transformers)
        - Vector database (e.g., ChromaDB, FAISS)
        - Cosine similarity ranking

        For now, returns keyword-based results
        """
        results = []

        # Simple keyword matching (production would use embeddings)
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        for doc in self.index.get("documents", []):
            # Calculate simple relevance score
            doc_terms = set(doc.get("content", "").lower().split())
            overlap = len(query_terms & doc_terms)
            score = overlap / max(len(query_terms), 1)

            if score >= min_score:
                results.append(SearchResult(
                    topic=doc.get("topic", ""),
                    content=doc.get("content", ""),
                    relevance_score=score,
                    authority=doc.get("authority", []),
                    keywords=doc.get("keywords", [])
                ))

        # Sort by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)

        return results[:top_k]

    def add_document(
        self,
        topic: str,
        content: str,
        keywords: List[str],
        authority: List[str]
    ) -> None:
        """Add document to search index"""
        doc = {
            "topic": topic,
            "content": content,
            "keywords": keywords,
            "authority": authority
        }

        self.index["documents"].append(doc)

        # Update inverted index
        for keyword in keywords:
            if keyword not in self.index["inverted_index"]:
                self.index["inverted_index"][keyword] = []
            self.index["inverted_index"][keyword].append(len(self.index["documents"]) - 1)

    def save_index(self) -> None:
        """Persist index to disk"""
        try:
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2)
        except Exception as e:
            print(f"Failed to save index: {e}")

    def build_index_from_doctrines(self, doctrines: List[Any]) -> None:
        """Build search index from doctrine cache"""
        self.index["documents"] = []
        self.index["inverted_index"] = {}

        for doctrine in doctrines:
            self.add_document(
                topic=doctrine.topic,
                content=doctrine.reasoning_framework,
                keywords=doctrine.keywords,
                authority=doctrine.primary_authority
            )

        self.save_index()

    def keyword_search(
        self,
        keywords: List[str],
        top_k: int = 5
    ) -> List[SearchResult]:
        """Search by exact keywords using inverted index"""
        doc_scores: Dict[int, float] = {}

        for keyword in keywords:
            doc_indices = self.index["inverted_index"].get(keyword.lower(), [])
            for idx in doc_indices:
                doc_scores[idx] = doc_scores.get(idx, 0) + 1

        # Sort by score
        ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in ranked[:top_k]:
            doc = self.index["documents"][idx]
            results.append(SearchResult(
                topic=doc["topic"],
                content=doc["content"],
                relevance_score=score / len(keywords),  # Normalize
                authority=doc["authority"],
                keywords=doc["keywords"]
            ))

        return results

    def search_by_irc_section(self, section: str) -> List[SearchResult]:
        """Search for doctrine by IRC section reference"""
        results = []

        section_normalized = section.replace("§", "").replace("IRC", "").strip()

        for doc in self.index.get("documents", []):
            # Check if section mentioned in authority
            for auth in doc.get("authority", []):
                if section_normalized in auth:
                    results.append(SearchResult(
                        topic=doc["topic"],
                        content=doc["content"],
                        relevance_score=1.0,  # Exact match
                        authority=doc["authority"],
                        keywords=doc["keywords"]
                    ))
                    break

        return results

    def get_related_doctrines(
        self,
        topic: str,
        max_related: int = 3
    ) -> List[str]:
        """Get related doctrine topics based on keyword overlap"""
        related = []

        # Find source document
        source_doc = None
        for doc in self.index.get("documents", []):
            if doc["topic"] == topic:
                source_doc = doc
                break

        if not source_doc:
            return []

        source_keywords = set(source_doc["keywords"])

        # Find documents with overlapping keywords
        candidates = []
        for doc in self.index["documents"]:
            if doc["topic"] == topic:
                continue  # Skip self

            overlap = len(set(doc["keywords"]) & source_keywords)
            if overlap > 0:
                candidates.append((doc["topic"], overlap))

        # Sort by overlap count
        candidates.sort(key=lambda x: x[1], reverse=True)

        return [topic for topic, _ in candidates[:max_related]]
