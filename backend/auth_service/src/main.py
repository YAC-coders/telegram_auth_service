import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.logger import LOGGING
from core.settings import settings
from api.v1 import router as v1_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.info("Starup the application")
    yield
    logging.info("Stop the application")


app = FastAPI(
    lifespan=lifespan,
    title=settings.project.title,
    description=settings.project.description,
    default_response_class=ORJSONResponse,
)

app.include_router(router=v1_router)


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.uvcorn.host,
        port=settings.uvcorn.port,
        reload=False,
        workers=settings.uvcorn.workers,
        log_config=LOGGING,
    )
