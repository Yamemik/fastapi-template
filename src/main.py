from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .common.config import settings
from .common.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


def create_app():
    app = FastAPI(
        debug=settings.debug,
        docs_url="/api/docs",
        title=f"{settings.app_name} API docs",
        lifespan= lifespan
    )

    return app
