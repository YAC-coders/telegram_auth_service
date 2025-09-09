
from pydantic import BaseModel, ConfigDict, Field


class BaseValidatePassword(BaseModel):
    session: str = Field(
        ...,
        description="The telegram account's session",
    )


class ValidatePasswordRequest(BaseValidatePassword):
    model_config = ConfigDict(frozen=True, extra="ignore")
    password: str = Field(..., description="Telegram account cloud password.")


class ValidatePasswordResponse(BaseValidatePassword):
    model_config = ConfigDict(frozen=True, extra="ignore")

    step: str = Field(
        ..., description="Auth step."
    )
