"""
Final response generator
"""


class FinalizerAgent:


    def __call__(self,state):


        budget = state.get(
            "budget_analysis",
            {}
        )


        total_cost = budget.get(
            "total",
            budget.get("total_cost", 0)
        )



        return {


            "agent_trace": state.get("agent_trace", []) + [{
                "agent": "Finalizer",
                "llm_used": "Groq openai/gpt-oss-20b",
                "tool": "Final Report Generator",
                "result": "Final travel report generated"
            }],

            "final_output":{


                "trip_overview":{


                    "destination":
                        state.get(
                            "destination",
                            "Unknown"
                        ),


                    "duration_days":
                        state.get(
                            "duration",
                            0
                        ),


                    "travelers":
                        state.get(
                            "travelers",
                            0
                        ),


                    "budget":
                        state.get(
                            "budget",
                            0
                        ),


                    "estimated_cost":
                        total_cost,


                    "remaining_budget":
                        state.get(
                            "budget",
                            0
                        )
                        -
                        total_cost

                },


                "itinerary":

                    state.get(
                        "itinerary",
                        {}
                    ),



                "destination_research":

                    state.get(
                        "destination_research",
                        {}
                    ),



                "budget":

                    budget


            },



            "execution_log":

                state.get(
                    "execution_log",
                    []
                )
                +
                [
                    "Finalizer generated complete travel report."
                ]

        }