from typing import TypedDict, List, Dict, Any



class TravelState(TypedDict, total=False):


    # USER INPUT

    destination:str

    travel_dates:str

    duration:int

    travelers:int

    budget:float


    interests:List[str]

    food_preferences:List[str]

    hotel_preference:str



    # AGENT OUTPUT


    destination_research:Dict[str,Any]

    hotel_options:List[Dict[str,Any]]

    selected_hotel:Dict[str,Any]


    activities:List[Dict[str,Any]]

    restaurants:List[Dict[str,Any]]


    itinerary:Dict[str,Any]


    budget_analysis:Dict[str,Any]



    # CONTROL


    within_budget:bool

    revision_count:int

    max_revisions:int



    # HUMAN


    human_approved:bool

    revision_requested:bool



    # OBSERVABILITY


    agent_trace:List[Dict[str,Any]]

    api_calls:List[Dict[str,Any]]

    mcp_connections:List[Dict[str,Any]]

    tool_usage:List[str]

    execution_log:List[str]



    # FINAL


    final_output:Dict[str,Any]