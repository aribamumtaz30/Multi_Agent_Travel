"""Regression tests that protect the travel-planning workflow behavior."""

from tools.web_search_tool import DestinationKnowledgeTool

def test_dubai_knowledge_includes_surroundings():
    data = DestinationKnowledgeTool().lookup("Dubai")
    assert "surroundings" in data
    assert "Abu Dhabi" in data["surroundings"]
