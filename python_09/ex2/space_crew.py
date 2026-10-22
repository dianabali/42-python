from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_safety_requirements(self) -> "SpaceMission":
        errors: list[str] = []

        if not self.mission_id.startswith("M"):
            errors.append('Mission ID must start with "M"')

        if not any(
            m.rank in (Rank.COMMANDER, Rank.CAPTAIN) for m in self.crew
        ):
            errors.append(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            if experienced * 2 < len(self.crew):
                errors.append(
                    "Long missions (> 365 days) need 50% "
                    "experienced crew (5+ years)"
                )

        if not all(member.is_active for member in self.crew):
            errors.append("All crew members must be active")

        if errors:
            raise ValueError("\n".join(errors))

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    # Valid mission
    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C001",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=42,
                    specialization="Mission Command",
                    years_experience=15,
                ),
                CrewMember(
                    member_id="C002",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=35,
                    specialization="Navigation",
                    years_experience=8,
                ),
                CrewMember(
                    member_id="C003",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=29,
                    specialization="Engineering",
                    years_experience=3,
                ),
            ],
        )
    except ValidationError as error:
        print("Expected validation errors:")
        print(error.errors()[0]["msg"])

    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - {member.specialization}"
        )

    print("=" * 41)

    # Invalid mission - testing model_validator
    try:
        SpaceMission(
            mission_id="M2024_LUNAR",  # doesn't start with M
            mission_name="Lunar Survey",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=1000,  # long mission
            budget_millions=300.0,
            crew=[
                CrewMember(
                    member_id="C010",
                    name="Bob Marley",
                    rank=Rank.CADET,  # no Commander/Captain
                    age=33,
                    specialization="Geology",
                    years_experience=2,  # under 5 years
                    is_active=True,
                ),
                CrewMember(
                    member_id="C011",
                    name="Eve Adams",
                    rank=Rank.LIEUTENANT,
                    age=22,
                    specialization="Robotics",
                    years_experience=0,  # under 5 years
                    is_active=True,
                ),
            ],
        )
    except ValidationError as error:
        print("Expected validation errors:")
        print(error.errors()[0]["msg"])

    print("=" * 41)

    # Invalid mission - testing nested errors
    try:
        SpaceMission(
            mission_id="M2024_TEST",
            mission_name="Nested Test",
            destination="Venus",
            launch_date=datetime.now(),
            duration_days=10,
            budget_millions=50.0,
            crew=[
                CrewMember(
                    member_id="C",  # short
                    name="T",  # short
                    rank=Rank.LIEUTENANT,
                    age=17,  # young
                    specialization="AI",  # short
                    years_experience=-20,  # negative
                ),
            ],
        )
    except ValidationError as error:
        print("Nested validation error:")
        for eerroorr in error.errors():
            print(
                f"Location: "
                f"{' -> '.join(str(part) for part in eerroorr['loc'])}"
            )
            print(eerroorr["msg"])
            print()


if __name__ == "__main__":
    main()
