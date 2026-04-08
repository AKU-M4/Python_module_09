from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(None, max_length=200)


def main():
    print("Space Station Data Validation")
    print("=" * 40)
    # 1. Valid station input
    try:
        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=20,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-04-01T12:00:00"
        )
        print("\nValida Sation Created:")
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size}")
        print(f"Power: {valid_station.power_level}")
        print(f"Oxygen: {valid_station.oxygen_level}")
        print(f"Status: {valid_station.last_maintenance}")

    except ValidationError as e:
        print(f"\nUnexpected error: {e}")

    print("=" * 40)
    # 2. Invalid station input
    try:
        SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-04-01T12:00:00"
        )
    except ValidationError as e:
        print("\nExpected validation error")
        print(f"{e.errors()[0]['msg']}")


if __name__ == "__main__":
    main()
