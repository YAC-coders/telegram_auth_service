from fastapi import APIRouter, Body, Depends

from service.auth import (
    SendCodeService,
    get_send_code_service,
    ValidateCodeService,
    get_validate_code_service,
)
from schema.auth import SendCodeRequest, ValidateCodeRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(path="/send_code")
async def send_code(
    send_code_request: SendCodeRequest = Body(
        description="Neccessary info to send code in telegram."
    ),
    send_code_service: SendCodeService = Depends(get_send_code_service),
):
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
async def validate_password():
    pass
