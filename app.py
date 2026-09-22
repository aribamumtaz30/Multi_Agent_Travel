"""Friendly command-line entry point for the multi-agent travel planner."""

from __future__ import annotations

from datetime import date, timedelta

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

from models.travel_request import TravelRequest
from graph.workflow import build_travel_graph
from config.settings import get_settings


console = Console()


AGENT_LABELS = {
    "destination_agent": "Destination Researcher",
    "hotel_agent": "Hotel Specialist",
    "activities_agent": "Activities Specialist",
    "restaurant_agent": "Restaurant Specialist",
    "itinerary_agent": "Itinerary Coordinator",
    "budget_agent": "Budget Checker",
    "revision_agent": "Revision Agent",
    "human_review_agent": "Human Approval",
    "finalizer_agent": "Finalizer",
}


def assistant_message(message):

    console.print(
        f"[bold cyan]Travel assistant:[/] {message}"
    )


def traveller_label(count):

    return "traveller" if count == 1 else "travellers"


def collect_request():

    console.print("[bold]Tell me about your trip[/]")

    destination = console.input("Destination [Dubai]: ").strip() or "Dubai"
    start_date = console.input("Start date [2026-12-10]: ").strip() or "2026-12-10"
    end_date = console.input("End date [2026-12-14]: ").strip() or "2026-12-14"
    travelers = int(console.input("Travelers [2]: ").strip() or "2")
    budget = float(console.input("Budget [2000]: ").strip() or "2000")
    interests = [x.strip() for x in (console.input("Interests [food,sightseeing]: ").strip() or "food,sightseeing").split(",")]
    cuisines = [x.strip() for x in (console.input("Cuisine [local]: ").strip() or "local").split(",")]
    hotel = console.input("Hotel preference [4-star]: ").strip() or "4-star"

    flight_choice = console.input("Do you already have a flight estimate? (y/N): ").strip().lower()
    flight_cost = 0
    if flight_choice == "y":
        flight_cost = float(console.input("Flight estimate USD: ").strip() or "0")

    return TravelRequest(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        travelers=travelers,
        budget=budget,
        interests=interests,
        cuisine_preferences=cuisines,
        hotel_preference=hotel,
        flight_cost=flight_cost,
    )


def example_request():

    return TravelRequest(

        destination="Dubai",

        start_date="2026-12-10",

        end_date="2026-12-14",

        travelers=2,

        budget=2000,

        interests=[
            "food",
            "shopping",
            "beaches",
            "sightseeing"
        ],

        cuisine_preferences=[
            "local",
            "Middle Eastern"
        ],

        hotel_preference="4-star",
        flight_cost=0
    )



def initial_state(req):

    return {

        **req.model_dump(mode="json"),

        "duration": req.duration,

        "revision_count":0,

        "max_revisions":
            get_settings().max_revision_attempts,

        "within_budget":False,

        "execution_log":[],

        "agent_trace":[],

        "api_calls":[],

        "mcp_connections":[],

        "tool_usage":[],

    }



def show_handoff(agent):

    console.print(

        Align.center(

            Panel(

                f"""
[bold green]{agent} completed[/]

TravelState passed to next agent
""",

                title="Agent Communication",

                border_style="green"

            )

        )

    )



def run_plan(req):


    console.print(

        Panel(

            f"""
Destination:
{req.destination}

Duration:
{req.duration} days

Travelers:
{req.travelers}

Budget:
${req.budget}
""",

            title="Trip Brief"

        )

    )


    console.print(Panel("""
✓ Groq LLM configured
✓ Open-Meteo Weather API configured
✓ OpenStreetMap / Overpass API configured
✓ OSRM Routing API configured
✓ Currency API configured
✓ MCP state tracking enabled
""", title="System Connections"))

    assistant_message(
        "I am sending your request to the AI travel team."
    )


    graph = build_travel_graph()


    state = initial_state(req)


    try:


        for update in graph.stream(

            state,

            config={
                "recursion_limit":40
            },

            stream_mode="updates"

        ):


            for node, changes in update.items():


                label = AGENT_LABELS.get(
                    node,
                    node
                )


                assistant_message(
                    f"✓ {label} completed"
                )


                logs = changes.get(
                    "execution_log",
                    []
                )


                if logs:


                    console.print(

                        Panel(

                            logs[-1],

                            title=f"{label} Output",

                            border_style="green"

                        )

                    )


                if changes.get("tool_usage"):


                    console.print(

                        Panel(

                            "\n".join(
                                changes["tool_usage"]
                            ),

                            title="Tools / APIs",

                            border_style="blue"

                        )

                    )


                state.update(changes)


                show_handoff(label)



    except Exception as e:


        assistant_message(
            f"Workflow failed: {e}"
        )

        return



    show_agent_report(state)


    show_final(

        state.get(
            "final_output",
            {}

        )

    )



def show_agent_report(state):


    console.print(

        Panel(

            "Agent execution transparency",

            title="AI Team Report",

            border_style="magenta"

        )

    )


    traces = state.get(
        "agent_trace",
        []
    )


    if traces:


        for trace in traces:


            console.print(

                f"""
Agent:
{trace.get('agent')}

LLM:
{trace.get('llm_used')}

Tool:
{trace.get('tool')}

Result:
{trace.get('result')}

-------------------
"""

            )


    else:

        console.print(
            "Trace information unavailable"
        )


    console.print(
        "\nExecution logs:"
    )


    for log in state.get(
        "execution_log",
        []
    ):

        console.print(
            f" • {log}"
        )




def show_final(plan):


    if not plan:

        assistant_message(
            "No final plan generated"
        )

        return



    overview = plan.get(
        "trip_overview",
        {}
    )


    console.print(

        Panel(

            f"""
Destination:
{overview.get('destination')}


Duration:
{overview.get('duration_days')} days


Travelers:
{overview.get('travelers')}


Budget:
${overview.get('budget',0):,.2f}


Estimated Cost:
${overview.get('estimated_cost',0):,.2f}


Remaining:
${overview.get('remaining_budget',0):,.2f}

""",

            title="Final Travel Plan"

        )

    )



    weather = plan.get(
        "weather",
        {}
    )

    if weather:
        console.print(
            Panel(
                str(weather),
                title="Weather Forecast",
                border_style="cyan"
            )
        )

    itinerary = plan.get(
        "itinerary",
        {}
    )


    days = itinerary.get(
        "days",
        []
    )


    if days:


        console.print(
            "\n[bold]Daily Itinerary[/]"
        )


        for day in days:


            console.print(

                f"""
Day {day.get('day')}

Morning:
{day.get('morning')}

Afternoon:
{day.get('afternoon')}

Evening:
{day.get('evening')}

"""

            )



    budget = plan.get(
        "budget",
        {}
    )


    table = Table(
        title="Budget Breakdown"
    )


    table.add_column(
        "Category"
    )

    table.add_column(
        "Amount"
    )


    for key,value in budget.items():


        if isinstance(
            value,
            (int,float)
        ):

            table.add_row(

                key,

                f"${value:,.2f}"

            )


    console.print(table)




def show_architecture():

    console.print(

        Panel(

"""
Traveller
 |
Destination Agent
 |
Hotel Agent
 |
Activities Agent
 |
Restaurant Agent
 |
Itinerary Agent
 |
Budget Agent
 |
Human Approval
 |
Finalizer

MCP / APIs / LLM tools connected through TravelState

""",

            title="Multi Agent Architecture"

        )

    )




def main():


    console.print(

        Panel(

            "Multi-Agent Travel Planner",

            title="AI Travel Team"

        )

    )


    while True:


        assistant_message(
            """
1) Plan trip
2) Dubai demo
3) Show architecture
4) Exit
"""
        )


        choice = console.input(
            "Choose: "
        )


        if choice=="1":

            run_plan(
                collect_request()
            )


        elif choice=="2":

            run_plan(
                example_request()
            )


        elif choice=="3":

            show_architecture()


        elif choice=="4":

            console.print("Safe travels!")
            break


        else:

            console.print("Please choose 1, 2, 3 or 4.")



if __name__=="__main__":

    main()