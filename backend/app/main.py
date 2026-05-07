from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from .api.routes.events import router as events_router
from .api.routes.health import router as health_router
from .api.routes.recommendations import router as recommendations_router
from .core.config import get_settings
from .core.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except SQLAlchemyError as exc:
        print(f"[KouzinaReco] database startup skipped: {exc}")
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API minima para recomendacoes da Kouzina Reco.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(events_router)
app.include_router(recommendations_router)
