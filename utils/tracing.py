def create_trace(
    agent,
    llm=None,
    tool=None,
    result=None
):

    return {
        "agent": agent,
        "llm_used": llm or "Not used",
        "tool": tool or "No external tool",
        "result": result or "Completed"
    }