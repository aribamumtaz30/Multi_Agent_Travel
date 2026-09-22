"""Regression tests that protect the travel-planning workflow behavior."""

from utils.cost_utils import calculate_budget_breakdown

def test_budget_math_is_deterministic():
    state = {
        "travelers": 2, "duration": 5, "budget": 2000,
        "selected_hotel": {"estimated_total": 600},
        "activities": [{"cost": 100}, {"cost": 150}],
        "restaurants": [{"estimated_cost_per_person": 20}],
        "include_flights": False,
    }
    result = calculate_budget_breakdown(state)
    assert result["hotel"] == 600
    assert result["activities"] == 250
    assert result["total"] == 1464.0
    assert result["within_budget"] is True


def test_budget_supports_one_traveller():
    state = {
        "travelers": 1, "duration": 3, "budget": 1500,
        "selected_hotel": {"estimated_total": 300},
        "activities": [{"cost": 75}],
        "restaurants": [{"estimated_cost_per_person": 20}],
        "include_flights": False,
    }
    result = calculate_budget_breakdown(state)
    assert result["food"] == 120.0
    assert result["within_budget"] is True
