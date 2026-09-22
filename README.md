# Multi-Agent Travel Planning System

A LangGraph-based Multi-Agent Travel Planning Assistant that uses
specialized AI agents to collaboratively research, plan, optimize, and
generate complete travel itineraries.

## Project Objective

The system accepts travel requirements such as: - Destination - Travel
dates - Duration - Travelers - Budget - Interests - Cuisine
preferences - Hotel preference - Flight estimate

Multiple AI agents collaborate through shared LangGraph state to
generate a complete travel plan.

## Architecture

User Request\
↓\
Destination Agent\
↓\
Hotel Agent + Activities Agent + Restaurant Agent\
↓\
Budget Agent\
↓\
Human Approval\
↓\
Finalizer Agent

## Agents

### Destination Researcher

Handles destination research: - Attractions - Neighborhoods - Weather -
Transportation - Travel considerations - Approximate costs

### Hotel Agent

Provides hotel recommendations based on: - Budget - Dates - Travelers -
Preferences - Location

### Activities Agent

Creates activities based on traveler interests with: - Cost - Duration -
Location - Best time

### Restaurant Agent

Recommends restaurants based on: - Cuisine - Budget - Location -
Activities

### Budget Agent

Calculates: - Flights - Hotel - Food - Activities - Transportation -
Miscellaneous

Determines if the trip fits the budget.

### Itinerary Agent

Creates day-by-day itinerary considering: - Locations - Travel time -
Activity duration - Preferences - Budget

### Human Review Agent

Allows approval or revision.

### Finalizer Agent

Creates the final travel report.

## Shared LangGraph State

The agents communicate through a shared TravelState containing: -
Destination - Travel dates - Duration - Travelers - Budget -
Preferences - Destination research - Hotels - Activities - Restaurants -
Budget analysis - Itinerary - Agent trace

## External Tools and APIs

### Groq LLM

Used for AI reasoning and planning.

### Open-Meteo Weather API

Used for weather information.

### OpenStreetMap / Overpass API

Used for location, hotel, and restaurant discovery.

### OSRM Routing API

Used for route planning.

### Currency API

Used for currency conversion.

### MCP Tracking

Used for tool execution visibility.

## Running the Application

Create environment:

``` bash
python -m venv travel_agent
```

Activate environment:

``` bash
travel_agent\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run:

``` bash
python app.py
```

## Testing

Run:

``` bash
pytest -q
```

Expected:

``` text
8 passed
```

## Example Input

    Destination: Dubai
    Duration: 5 days
    Travelers: 2
    Budget: $2000
    Interests: Food, shopping, beaches, sightseeing
    Hotel preference: 4-star

## Example Output

    Destination: Dubai
    Duration: 5 days
    Travelers: 2
    Budget: $2000

    Estimated Cost: $1180
    Remaining Budget: $820

## Agent Transparency Example

    Agent:
    Destination Researcher

    LLM:
    Groq openai/gpt-oss-20b

    Tool:
    Open-Meteo Weather API + Destination Knowledge

    Result:
    Destination research completed

## Error Handling

The system supports: - API fallback handling - Missing data handling -
Routing fallback - Restaurant fallback

## Completed Requirements

-   Python implementation
-   LangGraph orchestration
-   Specialized AI agents
-   Shared state communication
-   Conditional routing
-   External API integration
-   Weather integration
-   Budget calculation
-   Day-by-day itinerary
-   Human approval workflow
-   Error handling
-   Agent collaboration tracking
-   Final travel report
