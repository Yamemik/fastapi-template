from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from db import run_migrations
from src.config.settings import settings
from src.api.router import api_router
from src.db.init_db import init_db
from src.db.session import engine  # если нужно закрывать соединение


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    # 🟢 Выполняется при запуске приложения
    await init_db()
    yield
    # 🔴 Выполняется при остановке приложения (опционально)
    await engine.dispose()


app = FastAPI(
    debug=settings.DEBUG,
    docs_url="/api/docs",
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

app.include_router(api_router, prefix="/api/v1")
