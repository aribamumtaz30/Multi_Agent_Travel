"""
Human In The Loop Agent

Purpose:
- Pause before final answer
- Ask user approval
- Allow revision request
"""



class HumanReviewAgent:


    def __call__(self, state):


        budget = state.get(
            "budget_analysis",
            {}
        )


        total = budget.get(
            "total",
            0
        )


        user_budget = state.get(
            "budget",
            0
        )


        print("\n")
        print("="*50)
        print(" HUMAN APPROVAL REQUIRED ")
        print("="*50)


        print(
            f"Estimated Trip Cost: ${total}"
        )


        print(
            f"Your Budget: ${user_budget}"
        )


        print("\nApprove this travel plan?")
        print("1. Approve and finalize")
        print("2. Request revision")


        choice = input(
            "Choose 1 or 2: "
        )


        if choice == "1":

            return {

                "agent_trace": state.get("agent_trace", []) + [{
                    "agent": "Human Approval",
                    "llm_used": "Not required",
                    "tool": "Human Input",
                    "result": "Travel plan approved"
                }],

                "human_approved": True,

                "execution_log":
                state.get(
                    "execution_log",
                    []
                )
                +
                [
                    "Human approved final travel plan."
                ]

            }


        else:

            return {

                "human_approved": False,

                "revision_requested": True,

                "execution_log":
                state.get(
                    "execution_log",
                    []
                )
                +
                [
                    "Human requested itinerary revision."
                ]

            }