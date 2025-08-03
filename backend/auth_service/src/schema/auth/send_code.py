from pydantic import BaseModel, ConfigDict, Field, field_validator


class BaseSendCode(BaseModel):
    phone_number: str = Field(
        ...,
        description="The telegram account's phone number",
        min_length=8,
        max_length=18,
        examples=["9996621234"],
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Phone number must contains only digits")
        return value


class SendCodeRequest(BaseSendCode):
    model_config = ConfigDict(frozen=True, extra="ignore")


class SendCodeResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    session: str = Field(..., description="The session string.")
