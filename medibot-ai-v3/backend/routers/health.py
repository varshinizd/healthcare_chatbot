import time
from fastapi import APIRouter
from backend.models.schemas import HealthResponse
from backend.config import settings
from backend.core.rag_pipeline import rag_pipeline

router = APIRouter(tags=["health"])
_start_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        app_name=settings.APP_NAME,
        rag_ready=rag_pipeline.is_ready(),
        uptime_seconds=round(time.time() - _start_time, 1),
    )
