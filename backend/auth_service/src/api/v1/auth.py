from fastapi import APIRouter, Body, Depends, status

from service.auth import (
    SendCodeService,
    get_send_code_service,
    ValidateCodeService,
    get_validate_code_service,
    ValidatePasswordService,
    get_validate_password_service,
)
from schema.auth import (
    SendCodeRequest,
    ValidateCodeRequest,
    ValidatePasswordRequest,
    SendCodeResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/send_code",
    summary="Send telegram code to phone number.",
    response_model=SendCodeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": SendCodeResponse,
            "description": "Code sent successfully.",
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Something went wrong"},
    },
)
async def send_code(
    send_code_request: SendCodeRequest = Body(
        description="Neccessary info to send code in telegram."
    ),
    send_code_service: SendCodeService = Depends(get_send_code_service),
) -> SendCodeResponse:
    """
    `Initiates` Telegram account authentication by `phone number`.

    Endpoint handler that:
    1. Parses and validates phone number
    2. Sends Telegram verification code
    3. Stores registration session

    Args:
    - `send_code_request`: Model containing:
        - phone_number: User's phone number

    Status Codes:
    - `200`: Verification code sent successfully
    - `400`: Something went wrong
    """
    return await send_code_service.send_code(send_code_request=send_code_request)


@router.post(path="/validate_code")
async def validate_code(
    validate_code_request: ValidateCodeRequest = Body(
        description="Neccessary info to verify telegram code."
    ),
    validate_code_service: ValidateCodeService = Depends(get_validate_code_service),
):
    return await validate_code_service.validate(
        validate_code_request=validate_code_request
    )


@router.post(path="/validate_password")
async def validate_password(
    validate_password_request: ValidatePasswordRequest = Body(
        description="Neccessary info to verify telegram code."
    ),
    validate_password_service: ValidatePasswordService = Depends(
        get_validate_password_service
    ),
):
    return await validate_password_service.validate(
        validate_password_request=validate_password_request
    )
