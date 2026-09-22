"""Regression tests that protect the travel-planning workflow behavior."""

from graph.state import TravelState

def test_state_accepts_shared_fields():
    state: TravelState = {"destination": "Dubai", "budget": 2000, "revision_count": 0}
    assert state["destination"] == "Dubai"
