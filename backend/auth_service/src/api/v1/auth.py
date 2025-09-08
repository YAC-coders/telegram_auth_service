from fastapi import APIRouter, Body, Depends, HTTPException, status

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
    ValidateCodeResponse,
    ValidatePasswordResponse,
)
from exception.telegram import AlreadyLoggedIn, CodeExpired, PasswordExpired


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
        status.HTTP_409_CONFLICT: {"description": "Telegram account already logged in"},
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
    - `409`: Already logged in
    """
    try:
        return await send_code_service.send_code(send_code_request=send_code_request)
    except AlreadyLoggedIn:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already logged in.")

@router.post(
    path="/validate_code",
    summary="Sign in by telegram code.",
    response_model=ValidateCodeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": ValidateCodeResponse,
            "description": "Sign in by code was successfully.",
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Something went wrong."},
        status.HTTP_409_CONFLICT: {"description": "Telegram sent code expired."},
    },
)
async def validate_code(
    validate_code_request: ValidateCodeRequest = Body(
        description="Neccessary info to verify telegram code."
    ),
    validate_code_service: ValidateCodeService = Depends(get_validate_code_service),
) -> ValidateCodeResponse:
    """`Authenticates` Telegram account using received verification `code`.

    Endpoint handler that:
    1. Validates verification code
    2. Completes Telegram authentication
    3. Initiates background data download

    Args:
    - account_auth: AccountAuthCode model containing:
        - registration_session: Handler reference
        - code: Received verification code
        - registration_id: Database registration ID

    Status Codes:
    - `200`: Authentication successful (background tasks started).
    - `400`: Something went wrong
    - `409`: Code expired
    """
    try:
        return await validate_code_service.validate(
            validate_code_request=validate_code_request
        )
    except CodeExpired:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Code expired.")


@router.post(
    path="/validate_password",
    summary="Sign in by cloud password.",
    response_model=ValidatePasswordResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": ValidatePasswordResponse,
            "description": "Sign in by cloud password was successfully.",
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Something went wrong"},
    },
)
async def validate_password(
    validate_password_request: ValidatePasswordRequest = Body(
        description="Neccessary info to verify telegram code."
    ),
    validate_password_service: ValidatePasswordService = Depends(
        get_validate_password_service
    ),
) -> ValidatePasswordResponse:
    """`Authenticates` Telegram account using `cloud password` (2FA).

    Endpoint handler that:
    1. Validates cloud password
    2. Completes Telegram authentication
    3. Initiates background data download

    Args:
    - account_auth: AccountAuthPassword model containing:
        - registration_session: Handler reference
        - password: Cloud password
        - registration_id: Database registration ID

    Status Codes:
    - `200`: Authentication successfull.
    - `400`: Something went wrong.
    - `409`: Session password expired.
    """
    try:
        return await validate_password_service.validate(
        validate_password_request=validate_password_request
    )
    except PasswordExpired:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Password expired")
