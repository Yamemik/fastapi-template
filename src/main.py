from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.db.run_migrations import run_migrations_if_needed
from src.config.settings import settings
from src.api.router import api_router
from src.db.init_db import init_db
from src.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations_if_needed()
    
    await init_db()
    
    yield
    
    # 🔴 Выполняется при остановке приложения (опционально)
    await engine.dispose()


app = FastAPI(
    debug=settings.DEBUG,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    title=f"{settings.APP_NAME} API docs",
    lifespan=lifespan
)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # лучше ограничить доменами в продакшене
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version="1.0.0",
        description="API с JWT авторизацией",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(api_router, prefix="/api/v1")
