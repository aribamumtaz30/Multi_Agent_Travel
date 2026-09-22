"""Structured output models used by specialist agents."""

from pydantic import BaseModel, Field

class HotelOption(BaseModel):
    name: str
    location: str
    estimated_total: float = Field(ge=0)
    rating: float | None = None
    why_recommended: str = ""
    distance_from_major_attractions: str = ""
    source_note: str = ""

class Activity(BaseModel):
    name: str
    cost: float = Field(ge=0)
    duration_hours: float = Field(gt=0)
    location: str
    best_time: str = ""
    relevance: str = ""

class Restaurant(BaseModel):
    name: str
    cuisine: str = ""
    location: str
    estimated_cost_per_person: float = Field(ge=0)
    quality_note: str = ""
    near_activity: str = ""

class BudgetBreakdown(BaseModel):
    flights: float = 0
    hotel: float = 0
    food: float = 0
    activities: float = 0
    transportation: float = 0
    miscellaneous: float = 0
    total: float = 0
    remaining: float = 0
    within_budget: bool = False
    warnings: list[str] = Field(default_factory=list)
