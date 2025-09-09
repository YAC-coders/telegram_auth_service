
from pydantic import BaseModel, ConfigDict, Field



class BaseValidateCode(BaseModel):
    session: str = Field(
        ...,
        description="The telegram account's session",
    )


class ValidateCodeRequest(BaseValidateCode):
    model_config = ConfigDict(frozen=True, extra="ignore")
    code: int = Field(..., description="Code which telegram send to verify account ")


class ValidateCodeResponse(BaseValidateCode):
    model_config = ConfigDict(frozen=True, extra="ignore")

    step: str = Field(
        ..., description="Auth step."
    )
