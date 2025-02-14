"""
Tests for the pypubmech package
"""

import pytest
from pypubmech import PubMedClient


@pytest.fixture
def client():
    """Create a PubMedClient instance for testing."""
    return PubMedClient(email="test@example.com")


def test_search_by_keyword(client):
    """Test keyword search functionality."""
    pmids = client.search_by_keyword("test", 5)
    assert isinstance(pmids, list)
    assert len(pmids) <= 5


def test_search_by_mesh(client):
    """Test MeSH search functionality."""
    mesh_query = "Disease[MeSH]"
    pmids = client.search_by_mesh(mesh_query, 5)
    assert isinstance(pmids, list)


def test_find_uncommon_pmids(client):
    """Test finding uncommon PMIDs between two sets."""
    set1 = {"1", "2", "3"}
    set2 = {"2", "3", "4"}
    result = client.find_uncommon_pmids(set1, set2)
    assert result == {"1", "4"}


def test_create_dataframe(client):
    """Test DataFrame creation."""
    client.search_by_keyword("test", 2)
    client.fetch_article_metadata()
    df = client.create_dataframe()
    assert not df.empty
    assert "pmid" in df.columns