"""Regression tests that protect the travel-planning workflow behavior."""

from graph.workflow import build_travel_graph

def test_graph_compiles():
    graph = build_travel_graph()
    assert graph is not None
