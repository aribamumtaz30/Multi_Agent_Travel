"""Deterministic trip-cost calculations shared by the budget workflow."""

from typing import Any

def calculate_budget_breakdown(state: dict[str, Any]) -> dict[str, Any]:
    travelers = max(int(state.get("travelers", 1)), 1)
    duration = max(int(state.get("duration", 1)), 1)
    user_budget = float(state.get("budget", 0))

    hotel = float(state.get("selected_hotel", {}).get("estimated_total", 0) or 0)
    activities = sum(float(a.get("cost", 0) or 0) for a in state.get("activities", []))

    # Restaurant recommendations are options; estimate meals from itinerary/budget assumptions.
    restaurants = state.get("restaurants", [])
    if restaurants:
        avg_meal_pp = sum(float(r.get("estimated_cost_per_person", 0) or 0) for r in restaurants) / len(restaurants)
        food = avg_meal_pp * travelers * duration * 2  # lunch + dinner
    else:
        food = 35.0 * travelers * duration

    # Deterministic estimate, deliberately separate from LLM arithmetic.
    transportation = 18.0 * duration + 6.0 * max(duration - 1, 0)
    miscellaneous = max(50.0, user_budget * 0.05)
    flights = float(state.get("flight_budget_estimate", 0) or 0) if state.get("include_flights") else 0.0

    total = flights + hotel + food + activities + transportation + miscellaneous
    remaining = user_budget - total
    warnings = []
    if total > user_budget:
        warnings.append(f"Estimated trip cost exceeds budget by ${abs(remaining):,.2f}.")
    if state.get("include_flights") and flights <= 0:
        warnings.append("Flights were requested but no flight estimate was supplied; flight cost is currently $0.")

    return {
        "flights": round(flights, 2),
        "hotel": round(hotel, 2),
        "food": round(food, 2),
        "activities": round(activities, 2),
        "transportation": round(transportation, 2),
        "miscellaneous": round(miscellaneous, 2),
        "total": round(total, 2),
        "remaining": round(remaining, 2),
        "within_budget": total <= user_budget,
        "warnings": warnings,
    }
