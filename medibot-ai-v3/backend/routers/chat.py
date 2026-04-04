import uuid
from fastapi import APIRouter, Depends
from typing import Optional

from backend.models.schemas import ChatRequest, ChatResponse
from backend.models.database import User
from backend.core.guardrails import run_guardrails
from backend.core.auth import get_optional_user
from backend.session import get_or_create_session
from backend.core.audit_logger import log_event

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Optional[User] = Depends(get_optional_user),
):
    session = get_or_create_session(request.session_id)
    history = session.get_history_for_api()
    message_id = str(uuid.uuid4())

    result = await run_guardrails(
        query=request.message,
        history=history,
        user=current_user,  # pass full user object
    )

    if not result.blocked:
        session.add_exchange(request.message, result.response)

    await log_event(
        session_id=session.session_id,
        query=request.message,
        response=result.response,
        category=result.category,
        blocked=result.blocked,
        block_reason=result.block_reason,
        layer_triggered=result.layer_triggered,
        latency_ms=result.latency_ms,
        rag_used=result.rag_used,
        is_emergency=result.is_emergency,
        message_id=message_id,
    )

    return ChatResponse(
        reply=result.response,
        session_id=session.session_id,
        blocked=result.blocked,
        block_reason=result.block_reason,
        is_emergency=result.is_emergency,
        category=result.category,
        rag_used=result.rag_used,
        latency_ms=result.latency_ms,
        message_id=message_id,
        is_clarifying_question=result.is_clarifying_question,
    )
