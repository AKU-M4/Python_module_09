from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000)

    @model_validator(mode='after')
    def mission_validation(self) -> 'SpaceMission':
        # 1st Rule
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        # 2nd Rule
        has_leader = any(
            c.rank in (Rank.commander, Rank.captain) for c in self.crew
        )
        if not has_leader:
            raise ValueError("Must have at least one Commander or Captain")

        # 3rd Rule
        if self.duration_days > 365:
            experienced = sum(1 for c in self.crew if c.years_experience >= 5)
            if (experienced / len(self.crew) < 0.5):
                raise ValueError(
                    'Long missions (> 365 days) need 50percent'
                    'experienced crew (5+ years)'
                )
        # 4th Rule
        if any(not c.is_active for c in self.crew):
            raise ValueError("All crew members must be active")

        return self


def demonstrate_validation():
    print("Space Mission Crew Validation")
    print("=========================================")

    try:
        # 1. Valid Mission Setup
        valid_crew = [
            CrewMember(
                member_id="C01",
                name="Sarah Connor",
                rank=Rank.commander,
                age=45,
                specialization="Mission Command",
                years_experience=15
            ),
            CrewMember(
                member_id="C02",
                name="John Smith",
                rank=Rank.lieutenant,
                age=32,
                specialization="Navigation",
                years_experience=6
            ),
            CrewMember(
                member_id="C03",
                name="Alice Johnson",
                rank=Rank.officer,
                age=28,
                specialization="Engineering",
                years_experience=3
            )
        ]

        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=valid_crew,
            budget_millions=2500.0
        )

        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(f"- {member.name} ({member.rank.value}) - "
                  f"{member.specialization}")

    except ValidationError as e:
        print(f"Unexpected validation error: {e}")

    print("=========================================")

    try:
        # 2. Invalid Mission (Fails Commander/Captain rule)
        invalid_crew = [
            CrewMember(
                member_id="C04",
                name="Bob Williams",
                rank=Rank.lieutenant,
                age=35,
                specialization="Pilot",
                years_experience=8
            )
        ]

        SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Lunar Outpost",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=30,
            crew=invalid_crew,
            budget_millions=500.0
        )

    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            clean_msg = error['msg'].replace('Value error, ', '')
            print(clean_msg)


if __name__ == "__main__":
    demonstrate_validation()
