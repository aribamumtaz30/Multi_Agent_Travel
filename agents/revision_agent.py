"""Revision specialist for both over-budget and under-utilized trip plans."""

class RevisionAgent:
    def __call__(self, state):
        count = state.get("revision_count", 0) + 1
        budget = float(state.get("budget", 0) or 0)
        analysis = state.get("budget_analysis", {}) or {}
        total = float(analysis.get("total", 0) or 0)
        remaining = round(budget - total, 2)

        options = state.get("hotel_options", [])
        selected = state.get("selected_hotel", {}).copy()
        activities = list(state.get("activities", []))

        if total > budget:
            if len(options) > 1:
                selected = min(options, key=lambda h: float(h.get("estimated_total", 10**9) or 10**9)).copy()
            if len(activities) > 2:
                expensive = max(range(len(activities)), key=lambda i: float(activities[i].get("cost", 0) or 0))
                activities.pop(expensive)
            reason = f"Revision {count}: plan was ${abs(remaining):.2f} over budget; switched to lower-cost choices."

        elif remaining > 100:
            # Spend all but $100 of the unused budget on better facilities/experiences.
            amount_to_use = round(remaining - 100, 2)
            current_hotel_cost = float(selected.get("estimated_total", 0) or 0)

            affordable_upgrades = []
            for option in options:
                option_cost = float(option.get("estimated_total", 0) or 0)
                increase = option_cost - current_hotel_cost
                if increase > 0 and increase <= amount_to_use:
                    affordable_upgrades.append(option)

            if affordable_upgrades:
                selected = max(affordable_upgrades, key=lambda h: float(h.get("estimated_total", 0) or 0)).copy()
                hotel_increase = float(selected.get("estimated_total", 0) or 0) - current_hotel_cost
                amount_to_use = round(max(0, amount_to_use - hotel_increase), 2)

            if amount_to_use > 0:
                activities.append({
                    "name": "Trip Experience & Facilities Upgrade",
                    "cost": amount_to_use,
                    "category": "upgrade",
                    "description": "Budget allocated to better facilities, comfort, meals, transport, and local experiences."
                })

            reason = f"Revision {count}: plan had ${remaining:.2f} unused; upgraded facilities/experiences to use the available budget."
        else:
            reason = f"Revision {count}: budget efficiently used with ${max(remaining, 0):.2f} remaining."

        return {
            "selected_hotel": selected,
            "activities": activities,
            "revision_count": count,
            "revision_reason": reason,
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": "Revision Agent",
                "llm_used": "Groq openai/gpt-oss-20b",
                "tool": "Budget Feedback Loop",
                "result": reason
            }],
            "execution_log": state.get("execution_log", []) + [reason]
        }
