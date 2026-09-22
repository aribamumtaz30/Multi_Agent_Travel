"""Date parsing and duration helpers for travel requests."""

from datetime import date, timedelta

def trip_dates(start_date: str, duration: int) -> list[str]:
    start = date.fromisoformat(start_date)
    return [(start + timedelta(days=i)).isoformat() for i in range(duration)]
