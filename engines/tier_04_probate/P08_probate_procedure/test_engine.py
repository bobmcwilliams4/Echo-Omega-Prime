"""
P08 Probate Procedure Engine - Test Suite
Validates TIE-20 compliance and probate procedure logic.
"""

import pytest
from fastapi.testclient import TestClient
from engine import app, CONFIG
from doctrines import DOCTRINE_CACHE
from semantic import normalize_query, extract_keywords, extract_entities
from telemetry import TelemetryCollector, PerformanceTracker


client = TestClient(app)


class TestEngineBasics:
    """Test basic engine functionality."""

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["engine_id"] == "P08_probate_procedure"
        assert data["version"] == "1.0.0"
        assert data["doctrine_count"] > 0

    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "query_count" in data
        assert "cache_hit_rate" in data

    def test_doctrines_list(self):
        """Test doctrine listing."""
        response = client.get("/doctrines")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0
        assert len(data["doctrines"]) > 0


class TestSemanticNormalization:
    """Test semantic normalization."""

    def test_normalize_independent_admin(self):
        """Test normalization of independent administration terms."""
        query = "Can I use an independent executor?"
        normalized = normalize_query(query)
        assert "independent administration" in normalized

    def test_normalize_muniment(self):
        """Test normalization of muniment of title terms."""
        query = "What is muniment title procedure?"
        normalized = normalize_query(query)
        assert "muniment of title" in normalized

    def test_extract_keywords(self):
        """Test keyword extraction."""
        query = "Texas probate venue requirements"
        keywords = extract_keywords(query)
        assert "texas" in keywords or "probate" in keywords
        assert "venue" in keywords

    def test_extract_entities(self):
        """Test entity extraction."""
        query = "independent administration venue requirements"
        entities = extract_entities(query)
        assert "procedures" in entities or "jurisdictional" in entities


class TestDoctrineCache:
    """Test doctrine cache content."""

    def test_cache_loaded(self):
        """Test doctrine cache is populated."""
        assert len(DOCTRINE_CACHE) >= 10

    def test_doctrine_structure(self):
        """Test doctrine blocks have required fields."""
        block = DOCTRINE_CACHE[0]
        assert hasattr(block, "topic")
        assert hasattr(block, "keywords")
        assert hasattr(block, "conclusion_template")
        assert hasattr(block, "reasoning_framework")
        assert hasattr(block, "primary_authority")
        assert len(block.keywords) > 0
        assert len(block.conclusion_template) > 0
        assert len(block.reasoning_framework) > 50

    def test_independent_admin_doctrine(self):
        """Test independent administration doctrine exists."""
        topics = [b.topic for b in DOCTRINE_CACHE]
        assert any("independent" in t.lower() and "admin" in t.lower() for t in topics)

    def test_muniment_doctrine(self):
        """Test muniment of title doctrine exists."""
        topics = [b.topic for b in DOCTRINE_CACHE]
        assert any("muniment" in t.lower() for t in topics)


class TestQueryProcessing:
    """Test query processing."""

    def test_fast_mode_query(self):
        """Test FAST mode query."""
        response = client.post(
            "/query",
            json={
                "query": "What is independent administration in Texas?",
                "mode": "FAST"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "FAST"
        assert len(data["response"]) > 0
        assert data["confidence_score"] > 0

    def test_defense_mode_query(self):
        """Test DEFENSE mode query."""
        response = client.post(
            "/query",
            json={
                "query": "What are the requirements for muniment of title?",
                "mode": "DEFENSE"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "DEFENSE"
        assert len(data["response"]) > 100  # Defense mode more detailed
        assert len(data["authorities_cited"]) > 0

    def test_memo_mode_query(self):
        """Test MEMO mode query."""
        response = client.post(
            "/query",
            json={
                "query": "Compare independent vs dependent administration",
                "mode": "MEMO"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "MEMO"
        assert len(data["response"]) > 200  # Memo mode comprehensive

    def test_venue_query(self):
        """Test venue-related query."""
        response = client.post(
            "/query",
            json={
                "query": "Where do I file probate if decedent lived in Dallas?",
                "mode": "DEFENSE"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "venue" in data["response"].lower() or "dallas" in data["response"].lower()

    def test_small_estate_query(self):
        """Test small estate affidavit query."""
        response = client.post(
            "/query",
            json={
                "query": "Can I use small estate affidavit for $70000 estate?",
                "mode": "DEFENSE"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "75000" in data["response"] or "75,000" in data["response"]


class TestTelemetry:
    """Test telemetry collection."""

    def test_telemetry_collector_init(self):
        """Test telemetry collector initializes."""
        collector = TelemetryCollector(CONFIG)
        assert collector.enabled == CONFIG.get("telemetry_enabled", True)

    def test_performance_tracker(self):
        """Test performance tracker."""
        tracker = PerformanceTracker()
        tracker.start("test")
        import time
        time.sleep(0.01)
        elapsed = tracker.stop("test")
        assert elapsed >= 10  # At least 10ms

    def test_metrics_after_query(self):
        """Test metrics updated after query."""
        # Execute query
        client.post(
            "/query",
            json={
                "query": "Test query for metrics",
                "mode": "FAST"
            }
        )

        # Check metrics updated
        response = client.get("/metrics")
        data = response.json()
        assert data["query_count"] > 0


class TestDeterminism:
    """Test deterministic behavior."""

    def test_same_query_same_hash(self):
        """Test same query produces same determinism hash."""
        query_data = {
            "query": "What is independent administration?",
            "mode": "FAST"
        }

        response1 = client.post("/query", json=query_data)
        response2 = client.post("/query", json=query_data)

        data1 = response1.json()
        data2 = response2.json()

        assert data1["determinism_hash"] == data2["determinism_hash"]


class TestAuthorityHardening:
    """Test authority citation."""

    def test_authorities_cited(self):
        """Test authorities cited in response."""
        response = client.post(
            "/query",
            json={
                "query": "Independent administration requirements Texas",
                "mode": "DEFENSE"
            }
        )
        data = response.json()
        assert len(data["authorities_cited"]) > 0
        # Check for Texas Estates Code citation
        authorities_str = " ".join(data["authorities_cited"])
        assert "texas estates code" in authorities_str.lower() or "§" in authorities_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
