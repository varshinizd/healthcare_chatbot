import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from backend.config import settings
from backend.routers import chat, health, feedback
from backend.routers.auth import router as auth_router
from backend.session import cleanup_expired_sessions
from backend.models.database import create_tables

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Domain-Restricted Medical Conversational Agent",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(feedback.router)
app.include_router(auth_router)


@app.on_event("startup")
async def startup_event():
    create_tables()
    print(f"[MediBot] Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"[MediBot] Database initialised.")


async def _session_cleanup_loop():
    while True:
        await asyncio.sleep(300)
        cleaned = cleanup_expired_sessions()
        if cleaned:
            print(f"[MediBot] Cleaned {cleaned} expired sessions.")


@app.on_event("startup")
async def start_cleanup():
    asyncio.create_task(_session_cleanup_loop())
