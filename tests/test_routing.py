"""Regression tests that protect the travel-planning workflow behavior."""

from graph.routing import route_after_budget

def test_routes_to_finalizer_when_under_budget():
    assert route_after_budget({"within_budget": True, "revision_count": 0, "max_revisions": 4}) == "finalizer"

def test_routes_to_revision_when_over_budget_and_attempts_remain():
    assert route_after_budget({"within_budget": False, "revision_count": 2, "max_revisions": 4}) == "revision"

def test_stops_after_four_revisions():
    assert route_after_budget({"within_budget": False, "revision_count": 4, "max_revisions": 4}) == "finalizer"
