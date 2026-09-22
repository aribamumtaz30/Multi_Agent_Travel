"""
LangGraph workflow

Flow:

Destination
    ↓
Hotel
    ↓
Activities
    ↓
Restaurant
    ↓
Itinerary
    ↓
Budget
    ↓
Human Review
    ↓
Finalizer

If budget fails:

Budget
    ↓
Revision
    ↓
Itinerary
"""

from langgraph.graph import StateGraph, END

from graph.state import TravelState

from agents.destination_agent import DestinationAgent
from agents.hotel_agent import HotelAgent
from agents.activities_agent import ActivitiesAgent
from agents.restaurant_agent import RestaurantAgent
from agents.itinerary_agent import ItineraryAgent
from agents.budget_agent import BudgetAgent
from agents.revision_agent import RevisionAgent
from agents.human_review_agent import HumanReviewAgent
from agents.finalizer_agent import FinalizerAgent



class TravelPlanningGraph:


    def __init__(self):


        self.graph = self.build()



    def build(self):


        workflow = StateGraph(
            TravelState
        )


        workflow.add_node(
            "destination",
            DestinationAgent()
        )


        workflow.add_node(
            "hotel",
            HotelAgent()
        )


        workflow.add_node(
            "activities",
            ActivitiesAgent()
        )


        workflow.add_node(
            "restaurant",
            RestaurantAgent()
        )


        workflow.add_node(
            "itinerary",
            ItineraryAgent()
        )


        workflow.add_node(
            "budget",
            BudgetAgent()
        )


        workflow.add_node(
            "revision",
            RevisionAgent()
        )


        workflow.add_node(
            "human_review",
            HumanReviewAgent()
        )


        workflow.add_node(
            "finalizer",
            FinalizerAgent()
        )



        workflow.set_entry_point(
            "destination"
        )


        workflow.add_edge(
            "destination",
            "hotel"
        )


        workflow.add_edge(
            "hotel",
            "activities"
        )


        workflow.add_edge(
            "activities",
            "restaurant"
        )


        workflow.add_edge(
            "restaurant",
            "itinerary"
        )


        workflow.add_edge(
            "itinerary",
            "budget"
        )



        def budget_router(state):

            if state.get(
                "within_budget",
                False
            ):
                return "human_review"

            return "revision"



        workflow.add_conditional_edges(

            "budget",

            budget_router,

            {

            "human_review":
                "human_review",

            "revision":
                "revision"

            }

        )



        workflow.add_edge(
            "revision",
            "itinerary"
        )


        workflow.add_edge(
            "human_review",
            "finalizer"
        )


        workflow.add_edge(
            "finalizer",
            END
        )


        return workflow.compile()



def build_travel_graph():

    return TravelPlanningGraph().graph