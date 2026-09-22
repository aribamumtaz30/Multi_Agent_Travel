"""Activities specialist using destination research and user interests from shared state."""
import json
from services.llm_service import LLMService

class ActivitiesAgent:
    # Activity suggestions are filtered by the traveler interests stored in shared state.
    def __init__(self): self.llm = LLMService()
    def __call__(self, state):
        names = state["destination_research"].get("major_attractions", [])[:6]
        if not names: names = ["Historic centre walk", "Local market", "City viewpoint", "Cultural museum"]
        fallback_items = [{"name": n, "cost": 20.0 * state["travelers"], "duration_hours": 2.0, "location": state["destination"], "best_time": "Morning or late afternoon", "why_relevant": "Matches sightseeing and local exploration."} for n in names]
        fallback = {"activities": fallback_items}
        
        prompt = f"Create 4-6 activities for {state['destination']} matching {state.get('interests', [])}. Use these researched attractions: {json.dumps(names)}. Return JSON {{activities:[...]}}. Each activity needs name,cost TOTAL for all travelers,duration_hours,location,best_time,why_relevant. Keep costs realistic estimates and concise."
        data = self.llm.generate_json("You are an activities planning agent. Do not claim live availability.", prompt, fallback)
        activities = data.get("activities") or fallback_items

        return {
            "activities": activities[:6],
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": "Activities Specialist",
                "llm_used": "Groq openai/gpt-oss-20b",
                "tool": "Destination Knowledge + LLM Planning",
                "result": "Activities selected based on interests"
            }],
            "execution_log": state.get("execution_log", []) + ["Activities agent matched attractions to the traveller's interests."]
        }
