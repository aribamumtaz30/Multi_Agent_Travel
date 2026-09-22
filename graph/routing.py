"""Conditional routing after the budget check."""
def route_after_budget(state):
    if state.get("within_budget", False): return "finalizer"
    if state.get("revision_count", 0) >= state.get("max_revisions", 4): return "finalizer"
    return "revision"
