from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if (
            self.signal_strength > 7.0
            and not self.message_received
        ):
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )

        return self


def try_report(
    contact_id: str,
    contact_type: ContactType,
    signal_strength: float,
    witness_count: int,
    is_verified: bool = False,
    message: Optional[str] = None,
) -> None:
    try:
        AlienContact(
            contact_id=contact_id,
            timestamp=datetime.now(),
            location="Tirana, Albania",
            contact_type=contact_type,
            signal_strength=signal_strength,
            duration_minutes=30,
            witness_count=witness_count,
            message_received=message,
            is_verified=is_verified,
        )
    except ValidationError as errorsss:
        print("Expected validation error:")
        print(errorsss.errors()[0]["msg"].removeprefix("Value error, "))
        print("-" * 40)


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)

    # Valid contact
    contact = AlienContact(
        contact_id="AC_GRU_001",
        timestamp=datetime.now(),
        location="Gru's Basement Lab",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Delivery of 10'000 bananas inbound.",
    )

    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Timestamp: {contact.timestamp}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")

    print("=" * 40)

    # Invalid contacts
    try_report("AC_2026_001", ContactType.TELEPATHIC, 5.0, 1)
    try_report("AC_2026_002", ContactType.PHYSICAL, 5.0, 4, is_verified=False)
    try_report("42_2026_003", ContactType.VISUAL, 5.0, 4)
    try_report("AC_2026_004", ContactType.RADIO, 7.1, 4)


if __name__ == "__main__":
    main()
