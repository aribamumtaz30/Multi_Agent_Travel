"""Coordinator that combines hotel, activities, restaurants, weather,
traveler preferences, budget, routing information, and revision instructions.
"""

import json

from services.llm_service import LLMService
from tools.routing_tool import RoutingTool


class ItineraryAgent:
    """Build a practical day-by-day itinerary from previous agent outputs."""

    def __init__(self):
        self.llm = LLMService()
        self.routing = RoutingTool()

    def _fallback(self, state):
        """Create a deterministic itinerary if Groq is unavailable."""

        days = []
        activities = state.get("activities", [])
        restaurants = state.get("restaurants", [])

        for day_number in range(1, state["duration"] + 1):
            start = (day_number - 1) * 2
            chosen = activities[start:start + 2]

            if not chosen and activities:
                chosen = [
                    activities[
                        (day_number - 1) % len(activities)
                    ]
                ]

            morning = (
                chosen[0]["name"]
                if chosen
                else "Flexible local exploration"
            )

            afternoon = (
                chosen[1]["name"]
                if len(chosen) > 1
                else "Free time / nearby surroundings"
            )

            if restaurants:
                restaurant = restaurants[
                    (day_number - 1) % len(restaurants)
                ]
                evening = f"Dinner: {restaurant['name']}"
            else:
                evening = "Dinner near hotel"

            days.append(
                {
                    "day": day_number,
                    "morning": morning,
                    "afternoon": afternoon,
                    "evening": evening,
                    "transport_note": (
                        "Group nearby stops and allow transfer time. "
                        "Exact travel time is not verified where routing "
                        "coordinates are unavailable."
                    ),
                    "pace_note": (
                        "Balanced schedule with buffer time."
                    ),
                }
            )

        return {"days": days}

    def _build_route_context(self, state):
        """
        Calculate real OSRM route estimates when both the selected hotel
        and restaurants contain coordinates.

        If coordinates or OSRM are unavailable, return an empty list.
        The itinerary can still continue using its fallback behavior.
        """

        routes = []

        hotel = state.get("selected_hotel") or {}

        hotel_lat = hotel.get("latitude")
        hotel_lon = hotel.get("longitude")

        # We cannot calculate routes without hotel coordinates.
        if hotel_lat is None or hotel_lon is None:
            return routes

        restaurants = state.get("restaurants", [])

        for restaurant in restaurants[:3]:
            restaurant_lat = restaurant.get("latitude")
            restaurant_lon = restaurant.get("longitude")

            if restaurant_lat is None or restaurant_lon is None:
                continue

            try:
                route = self.routing.get_route(
                    hotel_lat,
                    hotel_lon,
                    restaurant_lat,
                    restaurant_lon,
                )
            except Exception:
                # Routing is optional. A failed external API must not
                # stop the entire travel-planning workflow.
                route = None

            if not route:
                continue

            routes.append(
                {
                    "from": hotel.get(
                        "name",
                        "Selected hotel",
                    ),
                    "to": restaurant.get(
                        "name",
                        "Restaurant",
                    ),
                    "distance_km": route.get(
                        "distance_km"
                    ),
                    "duration_minutes": route.get(
                        "duration_minutes"
                    ),
                    "source": route.get(
                        "source",
                        "OSRM",
                    ),
                }
            )

        return routes

    def __call__(self, state):
        """Generate the itinerary and attach available routing data."""

        fallback = self._fallback(state)

        # ---------------------------------------------------------
        # ROUTING TOOL
        # ---------------------------------------------------------
        route_context = self._build_route_context(state)

        # ---------------------------------------------------------
        # SHARED AGENT CONTEXT
        #
        # These values are deliberately passed directly to the
        # itinerary agent rather than relying only on indirect
        # information from previous agents.
        # ---------------------------------------------------------
        context = {
            "hotel": state.get("selected_hotel", {}),
            "activities": state.get(
                "activities",
                [],
            )[:6],
            "restaurants": state.get(
                "restaurants",
                [],
            )[:4],
            "weather": state.get(
                "weather",
                {},
            ),
            "destination_research": state.get(
                "destination_research",
                {},
            ),

            # Direct traveler requirements
            "traveler_interests": state.get(
                "interests",
                [],
            ),
            "budget_usd": state.get("budget"),
            "travelers": state.get("travelers"),
            "travel_dates": state.get(
                "travel_dates",
                state.get("dates"),
            ),

            # Real route estimates from OSRM where available.
            "routing_information": route_context,

            # Human/budget revision instructions.
            "revision_reason": state.get(
                "revision_reason",
                "",
            ),
            "human_feedback": state.get(
                "human_feedback",
                "",
            ),
        }

        prompt = (
            f"Build exactly {state['duration']} days for "
            f"{state['destination']}.\n\n"

            "Use the hotel, activities, restaurants, weather, traveler "
            "interests, budget, dates and routing information supplied "
            "in the context.\n\n"

            "Planning requirements:\n"
            "- Match the traveler's interests and preferences.\n"
            "- Keep the itinerary realistic for the stated budget.\n"
            "- Group geographically close activities together.\n"
            "- Consider activity duration when arranging each day.\n"
            "- Avoid overpacking the schedule.\n"
            "- Include reasonable buffer/transfer time.\n"
            "- Use OSRM distance and duration when routing_information "
            "is available.\n"
            "- Never invent exact transportation minutes when routing "
            "data is unavailable.\n"
            "- Consider opening hours only when they are available in "
            "the supplied data.\n"
            "- If opening hours are unavailable, clearly treat them as "
            "not verified rather than inventing hours.\n"
            "- Respect revision_reason and human_feedback when present.\n"
            "- Keep the overall pace balanced and practical.\n\n"

            f"Context:\n{json.dumps(context, default=str)}\n\n"

            "Return JSON only in this structure:\n"
            "{"
            '"days": ['
            "{"
            '"day": 1,'
            '"morning": "...",'
            '"afternoon": "...",'
            '"evening": "...",'
            '"transport_note": "...",'
            '"pace_note": "..."'
            "}"
            "]"
            "}"
        )

        data = self.llm.generate_json(
            (
                "You are the coordinating itinerary agent. "
                "Use outputs from previous agents and available routing "
                "data rather than inventing a disconnected plan."
            ),
            prompt,
            fallback,
        )

        itinerary = (
            data
            if isinstance(data, dict) and data.get("days")
            else fallback
        )

        # ---------------------------------------------------------
        # EXECUTION LOG
        # Makes it visible whether the routing API contributed data.
        # ---------------------------------------------------------
        if route_context:
            routing_log = (
                f"Itinerary agent used {len(route_context)} "
                "OSRM route estimate(s)."
            )
        else:
            routing_log = (
                "OSRM route data was unavailable or coordinates were "
                "missing; itinerary used geographic/transfer fallback."
            )

        return {
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": "Itinerary Coordinator",
                "llm_used": "Groq openai/gpt-oss-20b",
                "tool": "OSRM Routing API",
                "result": "Day-by-day itinerary created"
            }],
            "itinerary": itinerary,
            "routing_information": route_context,
            "execution_log": (
                state.get("execution_log", [])
                + [
                    (
                        "Itinerary agent combined hotel, activities, "
                        "restaurants, weather, preferences and budget "
                        "into a day-by-day plan."
                    ),
                    routing_log,
                ]
            ),
        }