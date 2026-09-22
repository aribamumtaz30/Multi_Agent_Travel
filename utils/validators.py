"""Input validation helpers for interactive travel-planning requests."""

from models.travel_request import TravelRequest

def validate_request(payload: dict) -> TravelRequest:
    return TravelRequest.model_validate(payload)
