from fastapi import APIRouter


router = APIRouter(prefix="/healthcheck", tags=["Health"])


@router.get(path="")
async def check_healt_status():
    return {"status": "ok"}
