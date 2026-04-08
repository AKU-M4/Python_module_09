from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    radio = 'radio'
    visual = 'visual'
    physical = 'physical'
    telepathic = 'telepathic'


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=5, max_length=15)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_business_rules(self) -> 'AlienContact':
        # Abreviated version of all the contact types
        ct = self.contact_type
        ct_physical = ContactType.physical
        ct_telepathic = ContactType.telepathic

        # 1st Rule
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC' (Alien Contact)")
        # 2nd Rule
        if ct == ct_physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        # 3rd Rule
        if ct == ct_telepathic and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        # 4th Rule
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages")

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)

    try:
        valid_contact = AlienContact(
            contact_id="AC_2024_008",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received='Greeting from Zeta Reticuli',
            is_verified=False
        )
        print("Valid contact report:")
        print(f"ID: {valid_contact.contact_id}")
        print(f"Type: {valid_contact.contact_type.value}")
        print(f"Location: {valid_contact.location}")
        print(f"Signal: {valid_contact.signal_strength}/10")
        print(f"Duration: {valid_contact.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: '{valid_contact.message_received}'\n")

    except ValidationError as e:
        print(f"Unexpected Validation error {e}")

    print("=" * 40)
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.now(),
            location="Sedona, Arizona",
            contact_type=ContactType.telepathic,
            signal_strength=5.5,
            duration_minutes=120,
            witness_count=2,  # Validation trigger
        )

    except ValidationError as e:
        print("Expected validation error:")
        # Pydantic wraps custom ValueError messages with "Value error, ".
        # We strip it here to match the exact output requested.
        for error in e.errors():
            clean_msg = error['msg'].replace('Value error, ', '')
            print(clean_msg)


if __name__ == "__main__":
    main()
