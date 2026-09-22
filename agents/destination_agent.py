"""
Destination Research Agent

Responsibilities:
- Get destination knowledge
- Get weather context
- Enrich with LLM if available
- Ensure shared LangGraph state always receives dictionaries
"""

import json

from tools.weather_tool import OpenMeteoWeatherTool
from tools.web_search_tool import DestinationKnowledgeTool
from services.llm_service import LLMService


class DestinationAgent:

    def __init__(self):

        # Tool for curated destination information
        self.knowledge = DestinationKnowledgeTool()

        # Free Open-Meteo weather/geocoding tool
        self.weather = OpenMeteoWeatherTool()

        # Groq/LLM enrichment service
        self.llm = LLMService()


    def __call__(self, state):

        # -------------------------------------------------
        # Step 1:
        # Retrieve destination base knowledge
        # -------------------------------------------------

        base = self.knowledge.lookup(
            state["destination"]
        )


        # -------------------------------------------------
        # Step 2:
        # Retrieve weather information
        # -------------------------------------------------

        weather = self.weather.get_weather(
            state["destination"]
        )


        # -------------------------------------------------
        # Step 3:
        # Fallback structure
        # This is used if LLM/API fails
        # -------------------------------------------------

        fallback = {

            "summary":
                f"Planning guide for {state['destination']}.",

            "popular_areas":
                base.get("areas", []),

            "major_attractions":
                base.get("attractions", []),

            "transportation":
                base.get("transport", []),

            "best_time_to_visit":
                base.get("best_time", ""),

            "travel_considerations":
                base.get("considerations", []),

            "recommended_neighborhoods":
                base.get("neighborhoods", []),

            "surrounding_places":
                base.get("surroundings", []),

            "approximate_costs":
            {
                "budget_meal_pp": 15,
                "local_transport_day_pp": 12
            }
        }


        # -------------------------------------------------
        # Step 4:
        # Ask LLM to enrich destination information
        # -------------------------------------------------

        prompt = f"""
Use the destination knowledge below.

Return ONLY JSON.

Preserve existing facts.
Add useful travel suggestions.

User interests:
{state.get("interests", [])}

Knowledge:
{json.dumps(base)}
"""


        research = self.llm.generate_json(
            "You are a destination research specialist. Return structured JSON.",
            prompt,
            fallback
        )


        # -------------------------------------------------
        # IMPORTANT FIX:
        # LLM may return JSON string instead of dict.
        # LangGraph shared state requires dict objects.
        # -------------------------------------------------

        if isinstance(research, str):

            try:
                research = json.loads(research)

            except Exception:

                research = fallback



        # -------------------------------------------------
        # Ensure required fields exist
        # -------------------------------------------------

        research.setdefault(
            "surrounding_places",
            base.get("surroundings", [])
        )


        research.setdefault(
            "recommended_neighborhoods",
            base.get("neighborhoods", [])
        )


        research.setdefault(
            "major_attractions",
            base.get("attractions", [])
        )


        research.setdefault(
            "transportation",
            base.get("transport", [])
        )


        # -------------------------------------------------
        # Return updated shared state
        # -------------------------------------------------

        return {

            "agent_trace": state.get("agent_trace", []) + [{
                "agent": "Destination Researcher",
                "llm_used": "Groq openai/gpt-oss-20b",
                "tool": "Open-Meteo Weather API + Destination Knowledge",
                "result": "Destination research completed"
            }],

            "destination_research": research,

            "surroundings":
                research.get(
                    "surrounding_places",
                    []
                ),

            "weather": weather,


            "execution_log":
                state.get(
                    "execution_log",
                    []
                )
                +
                [
                    "Destination researcher finished: destination, surroundings and weather are ready."
                ]
        }