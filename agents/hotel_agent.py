"""
Hotel Agent

Responsibilities:
- Recommend hotels based on:
    destination
    budget
    travelers
    preference
    location

Uses:
- OpenStreetMap hotel discovery
- fallback recommendations
- LLM ranking
"""


import json

from services.llm_service import LLMService
from tools.places_tool import PlacesTool



class HotelAgent:


    def __init__(self):

        self.llm = LLMService()

        self.places = PlacesTool()



    def __call__(self, state):


        # -------------------------------------------------
        # FIX:
        # Destination research must always be a dictionary
        # -------------------------------------------------

        destination_research = state.get(
            "destination_research",
            {}
        )


        if isinstance(destination_research, str):

            try:

                destination_research = json.loads(
                    destination_research
                )

            except Exception:

                destination_research = {}



        # Put cleaned value back into state

        state["destination_research"] = destination_research



        # -------------------------------------------------
        # Budget calculation
        # -------------------------------------------------

        nights = max(
            state["duration"] - 1,
            1
        )


        target_total = max(
            120.0,
            state["budget"] * 0.34
        )


        nightly = target_total / nights



        areas = destination_research.get(
            "recommended_neighborhoods",
            [
                "central area"
            ]
        )



        # -------------------------------------------------
        # Try live OSM hotel discovery
        # -------------------------------------------------

        location = state.get(
            "location",
            {}
        )


        latitude = location.get(
            "latitude"
        )

        longitude = location.get(
            "longitude"
        )


        live_hotels = []


        if latitude and longitude:

            live_hotels = self.places.find_hotels(
                latitude,
                longitude,
                limit=5
            )



        # -------------------------------------------------
        # Fallback hotels
        # -------------------------------------------------

        fallback_options = [

            {

                "name":
                    f"Central {state['hotel_preference']} Stay",

                "location":
                    str(areas[0]),

                "estimated_price_per_night":
                    round(nightly, 2),

                "estimated_total":
                    round(target_total, 2),

                "rating":
                    "Not verified",

                "why_recommended":
                    "Central location and budget friendly.",

                "data_source":
                    "Planner fallback"
            },


            {

                "name":
                    "Value Traveller Hotel",

                "location":
                    str(areas[-1]),

                "estimated_total":
                    round(
                        target_total * 0.78,
                        2
                    ),

                "rating":
                    "Not verified",

                "why_recommended":
                    "Lower cost alternative.",

                "data_source":
                    "Planner fallback"
            }

        ]



        # -------------------------------------------------
        # Convert live hotels
        # -------------------------------------------------

        if live_hotels:


            hotel_options = []


            for index, hotel in enumerate(
                live_hotels[:3]
            ):


                hotel_options.append(

                    {

                        "name":
                            hotel.get(
                                "name",
                                "Hotel"
                            ),

                        "location":
                            hotel.get(
                                "address",
                                str(areas[0])
                            ),

                        "estimated_price_per_night":
                            round(
                                nightly * (1 + index*0.08),
                                2
                            ),

                        "estimated_total":
                            round(
                                nightly * nights,
                                2
                            ),

                        "rating":
                            "Not verified",

                        "data_source":
                            "OpenStreetMap Overpass"

                    }

                )


            fallback_options = hotel_options



        fallback = {

            "hotel_options":
                fallback_options,

            "selected_hotel":
                fallback_options[0]

        }



        # -------------------------------------------------
        # LLM hotel ranking
        # -------------------------------------------------

        prompt = f"""

Destination:
{state['destination']}

Budget:
{state['budget']}

Hotels:
{json.dumps(fallback_options)}

Return JSON:

hotel_options
selected_hotel

Do not invent availability.

"""


        data = self.llm.generate_json(

            "You are a hotel recommendation agent.",

            prompt,

            fallback

        )



        # Safety check

        if isinstance(data, str):

            try:
                data = json.loads(data)

            except Exception:
                data = fallback



        options = data.get(
            "hotel_options",
            fallback_options
        )


        selected = data.get(
            "selected_hotel",
            options[0]
        )


        # Ensure dictionary

        if isinstance(selected, str):

            selected = options[0]



        selected.setdefault(
            "estimated_total",
            round(target_total,2)
        )



        return {

            "agent_trace": state.get("agent_trace", []) + [{
                "agent": "Hotel Specialist",
                "llm_used": "Groq openai/gpt-oss-20b",
                "tool": "OpenStreetMap / Places API",
                "result": "Hotel recommendations generated"
            }],

            "hotel_options":
                options,


            "selected_hotel":
                selected,


            "execution_log":

                state.get(
                    "execution_log",
                    []
                )
                +
                [
                    "Hotel specialist completed hotel selection."
                ]

        }