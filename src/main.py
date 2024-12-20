from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from common.config import settings


def create_app():
    app = FastAPI(
        debug=settings.debug,
        docs_url="/api/docs",
        title=f"{settings.app_name} API docs",
    )

    return app
