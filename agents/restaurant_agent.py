"""Restaurant specialist using OSM places plus Groq/fallback."""

import json

from services.llm_service import LLMService
from tools.places_tool import PlacesTool


class RestaurantAgent:
    def __init__(self):
        self.llm = LLMService()
        self.places = PlacesTool()

    def __call__(self, state):
        activity_locations = [
            activity.get("location", state["destination"])
            for activity in state.get("activities", [])
        ][:4]

        cuisines = (
            state.get("cuisine_preferences")
            or ["local"]
        )

        location = state.get("location", {})
        latitude = location.get("latitude")
        longitude = location.get("longitude")

        live_restaurants = []

        if latitude is not None and longitude is not None:
            live_restaurants = self.places.find_restaurants(
                latitude,
                longitude,
                limit=8,
            )

        # Existing deterministic fallback.
        fallback_items = [
            {
                "name": (
                    f"Local Kitchen near "
                    f"{activity_locations[i % len(activity_locations)]}"
                    if activity_locations
                    else f"Local Kitchen {i + 1}"
                ),
                "cuisine": cuisines[i % len(cuisines)],
                "location": (
                    activity_locations[i % len(activity_locations)]
                    if activity_locations
                    else state["destination"]
                ),
                "estimated_cost_per_person": 18 + i * 4,
                "quality_note":
                    "Suitable fallback option for the day's route.",
                "nearby_activity": (
                    state["activities"][
                        i % len(state["activities"])
                    ].get("name", "city sightseeing")
                    if state.get("activities")
                    else "city sightseeing"
                ),
                "opening_hours": "Not verified",
                "data_source": "Planner fallback",
            }
            for i in range(3)
        ]

        # Convert real OSM results into our schema.
        if live_restaurants:
            osm_items = []

            for i, restaurant in enumerate(
                live_restaurants[:4]
            ):
                nearby_activity = (
                    state["activities"][
                        i % len(state["activities"])
                    ].get("name", "city sightseeing")
                    if state.get("activities")
                    else "city sightseeing"
                )

                osm_items.append(
                    {
                        "name": restaurant.get(
                            "name",
                            "Local Restaurant",
                        ),
                        "cuisine": (
                            restaurant.get("cuisine")
                            or cuisines[i % len(cuisines)]
                        ),
                        "location": restaurant.get(
                            "address",
                            state["destination"],
                        ),
                        "latitude": restaurant.get("latitude"),
                        "longitude": restaurant.get("longitude"),
                        "estimated_cost_per_person": 18 + i * 4,
                        "quality_note":
                            "Real nearby restaurant discovered "
                            "through OpenStreetMap.",
                        "nearby_activity": nearby_activity,
                        "opening_hours": restaurant.get(
                            "opening_hours",
                            "Not verified",
                        ),
                        "data_source":
                            "OpenStreetMap Overpass",
                    }
                )

            fallback_items = osm_items

        fallback = {
            "restaurants": fallback_items,
        }

        prompt = (
            f"Recommend only 3-4 food options for "
            f"{state['destination']}. "
            f"Cuisine preferences: {cuisines}. "
            f"Activity locations: "
            f"{json.dumps(activity_locations)}. "
            f"Available restaurant candidates: "
            f"{json.dumps(fallback_items)}. "
            "Preserve real candidate names. "
            "Prefer proximity to activities and user cuisines. "
            "Do not invent ratings or verified opening hours."
        )

        data = self.llm.generate_json(
            "You are a restaurant planning agent focused on "
            "route proximity and budget.",
            prompt,
            fallback,
        )

        restaurants = (
            data.get("restaurants")
            or fallback_items
        )[:4]

        return {
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": "Restaurant Specialist",
                "llm_used": "Groq openai/gpt-oss-20b",
                "tool": "OpenStreetMap Restaurant API",
                "result": "Restaurant recommendations generated"
            }],
            "restaurants": restaurants,
            "execution_log": state.get(
                "execution_log",
                [],
            )
            + [
                (
                    "Restaurant agent used OpenStreetMap place data."
                    if live_restaurants
                    else "Restaurant API unavailable/no results; "
                    "restaurant fallback used."
                )
            ],
        }