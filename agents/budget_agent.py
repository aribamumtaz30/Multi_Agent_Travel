"""
Budget Agent

Responsibilities:

- Calculate complete trip cost
- Compare against user budget
- Trigger revision workflow
- Explain where money is spent
"""


class BudgetAgent:


    def __call__(self, state):


        hotel = state.get(
            "selected_hotel",
            {}
        )


        activities = state.get(
            "activities",
            []
        )


        flight = state.get(
            "flight_cost",
            state.get("flight_estimate", 0)
        )


        # -------------------------
        # Cost Calculation
        # -------------------------

        hotel_cost = hotel.get(
            "estimated_total",
            0
        )


        activity_cost = sum(
            item.get(
                "cost",
                0
            )
            for item in activities
            if isinstance(item,dict)
        )


        food_cost = (
            state.get(
                "travelers",
                1
            )
            *
            30
            *
            state.get(
                "duration",
                1
            )
        )


        transport_cost = (
            state.get(
                "duration",
                1
            )
            *
            20
        )


        misc_cost = 100



        total = (

            flight
            +
            hotel_cost
            +
            activity_cost
            +
            food_cost
            +
            transport_cost
            +
            misc_cost

        )


        budget = state.get(
            "budget",
            0
        )



        remaining = round(budget - total, 2)

        # Finalize only when no more than $100 remains unused.
        within_budget = 0 <= remaining <= 100

        if total > budget:
            budget_status = "Budget exceeded"
        elif remaining > 100:
            budget_status = "Budget underutilized"
        else:
            budget_status = "Budget fully utilized"



        # -------------------------
        # Analysis
        # -------------------------

        analysis = {


            "flights":
                flight,


            "hotel":
                hotel_cost,


            "food":
                food_cost,


            "activities":
                activity_cost,


            "transportation":
                transport_cost,


            "miscellaneous":
                misc_cost,


            "total":
                round(total,2),


            "budget":
                budget,


            "remaining":
                remaining,

            "budget_status":
                budget_status,


            "within_budget":
                within_budget

        }



        trace = state.get(
            "agent_trace",
            []
        )


        trace.append(

            {

            "agent":
                "Budget Agent",


             "llm_used": "Not required",

            "tool": "Cost Calculator",

            "result": f"Trip cost calculated ${round(total,2)}. {budget_status}. Remaining ${remaining}"

            }

        )



        return {


            "budget_analysis":
                analysis,


            "within_budget":
                within_budget,


            "agent_trace":
                trace,


            "execution_log":

                state.get(
                    "execution_log",
                    []
                )
                +
                [
                f"Budget calculated: ${round(total,2)}"
                ]

        }