from fastapi import APIRouter


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(path="/send_code")
async def send_code():
    pass


@router.post(path="/validate_code")
async def validate_code():
    pass


@router.post(path="/validate_password")
async def validate_password():
    pass
