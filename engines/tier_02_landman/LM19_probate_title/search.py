"""
LM19 Probate Title Engine — Vector Search
==========================================
Semantic vector search for probate doctrine retrieval.
Embeddings-based fallback when doctrine cache misses.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    from sentence_transformers import SentenceTransformer
    _TRANSFORMERS_AVAILABLE = True
except ImportError:
    _TRANSFORMERS_AVAILABLE = False

import numpy as np
from pydantic import BaseModel


@dataclass
class SearchDocument:
    """A searchable document for vector retrieval."""
    id: str
    topic: str
    content: str
    keywords: list[str]
    category: str
    embedding: Optional[np.ndarray] = None


class SearchResponse(BaseModel):
    """Vector search response."""
    query: str
    results: list[dict]
    scores: list[float]
    total_results: int


class VectorIndex:
    """Vector search index for probate doctrines."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", index_path: Optional[Path] = None) -> None:
        """
        Initialize vector index.

        Args:
            model_name: SentenceTransformer model name
            index_path: Path to saved index (optional)
        """
        self.model_name = model_name
        self.index_path = index_path
        self.documents: list[SearchDocument] = []
        self.model: Optional[SentenceTransformer] = None

        global _TRANSFORMERS_AVAILABLE
        if _TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
            except Exception:
                self.model = None
                _TRANSFORMERS_AVAILABLE = False

        # Load index if path provided
        if index_path and index_path.exists():
            self.load_index(index_path)

    def add_document(self, doc: SearchDocument) -> None:
        """
        Add document to index and compute embedding.

        Args:
            doc: SearchDocument to add
        """
        if self.model and doc.embedding is None:
            # Create embedding from content + keywords
            text = f"{doc.topic} {doc.content} {' '.join(doc.keywords)}"
            doc.embedding = self.model.encode(text, convert_to_numpy=True)

        self.documents.append(doc)

    def build_from_doctrines(self, doctrines: list) -> None:
        """
        Build index from doctrine blocks.

        Args:
            doctrines: List of DoctrineBlock objects
        """
        for doctrine in doctrines:
            # Create searchable text from doctrine components
            content = f"{doctrine.conclusion_template} {doctrine.reasoning_framework} {doctrine.resolution_strategy}"
            doc = SearchDocument(
                id=doctrine.topic,
                topic=doctrine.topic,
                content=content[:1000],  # Truncate for embedding
                keywords=doctrine.keywords,
                category=doctrine.category.value
            )
            self.add_document(doc)

    def search(self, query: str, top_k: int = 5, threshold: float = 0.72) -> SearchResponse:
        """
        Search index for relevant doctrines.

        Args:
            query: Search query
            top_k: Number of results to return
            threshold: Minimum similarity threshold

        Returns:
            SearchResponse with results and scores
        """
        if not self.model or not self.documents:
            return SearchResponse(query=query, results=[], scores=[], total_results=0)

        # Encode query
        query_embedding = self.model.encode(query, convert_to_numpy=True)

        # Calculate cosine similarity with all documents
        similarities: list[tuple[float, SearchDocument]] = []
        for doc in self.documents:
            if doc.embedding is not None:
                # Cosine similarity
                similarity = float(np.dot(query_embedding, doc.embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc.embedding)
                ))
                if similarity >= threshold:
                    similarities.append((similarity, doc))

        # Sort by similarity descending
        similarities.sort(reverse=True, key=lambda x: x[0])

        # Take top_k results
        top_results = similarities[:top_k]

        # Format response
        results = [
            {
                "topic": doc.topic,
                "category": doc.category,
                "keywords": doc.keywords,
                "score": score,
            }
            for score, doc in top_results
        ]
        scores = [score for score, _ in top_results]

        return SearchResponse(
            query=query,
            results=results,
            scores=scores,
            total_results=len(similarities)
        )

    def save_index(self, path: Path) -> None:
        """
        Save index to disk.

        Args:
            path: Path to save index
        """
        data = {
            "model_name": self.model_name,
            "documents": [
                {
                    "id": doc.id,
                    "topic": doc.topic,
                    "content": doc.content,
                    "keywords": doc.keywords,
                    "category": doc.category,
                    "embedding": doc.embedding.tolist() if doc.embedding is not None else None
                }
                for doc in self.documents
            ]
        }
        path.write_text(json.dumps(data, indent=2))

    def load_index(self, path: Path) -> None:
        """
        Load index from disk.

        Args:
            path: Path to load index from
        """
        data = json.loads(path.read_text())
        self.model_name = data.get("model_name", self.model_name)

        self.documents = []
        for doc_data in data.get("documents", []):
            embedding = doc_data.get("embedding")
            if embedding:
                embedding = np.array(embedding)
            doc = SearchDocument(
                id=doc_data["id"],
                topic=doc_data["topic"],
                content=doc_data["content"],
                keywords=doc_data["keywords"],
                category=doc_data["category"],
                embedding=embedding
            )
            self.documents.append(doc)


# Global index instance
_VECTOR_INDEX: Optional[VectorIndex] = None


def get_vector_index() -> VectorIndex:
    """Get global vector index instance."""
    global _VECTOR_INDEX
    if _VECTOR_INDEX is None:
        # Create index (will be populated on engine startup)
        _VECTOR_INDEX = VectorIndex()
    return _VECTOR_INDEX
