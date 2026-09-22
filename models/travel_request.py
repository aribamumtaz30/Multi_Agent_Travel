"""Structured model for a traveler request."""

from datetime import date
from pydantic import BaseModel, Field, model_validator

class TravelRequest(BaseModel):
    destination: str = Field(min_length=2)
    start_date: date
    end_date: date
    travelers: int = Field(ge=1, le=20)
    budget: float = Field(gt=0)
    interests: list[str] = Field(default_factory=list)
    cuisine_preferences: list[str] = Field(default_factory=list)
    hotel_preference: str = "4-star"
    origin: str | None = None
    include_flights: bool = False
    flight_budget_estimate: float = Field(default=0.0, ge=0)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self

    @property
    def duration(self) -> int:
        return (self.end_date - self.start_date).days + 1
