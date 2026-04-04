import json
import asyncio
import hashlib
from datetime import datetime
from pathlib import Path
from backend.config import settings


LOG_PATH = Path(settings.LOG_FILE)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def _hash_query(query: str) -> str:
    return hashlib.sha256(query.encode()).hexdigest()[:16]


async def log_event(
    session_id: str,
    query: str,
    response: str,
    category: str,
    blocked: bool,
    block_reason: str | None,
    layer_triggered: str | None,
    latency_ms: float,
    rag_used: bool,
    is_emergency: bool,
    message_id: str,
):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": session_id,
        "message_id": message_id,
        "query_hash": _hash_query(query),
        "query_length": len(query),
        "response_length": len(response),
        "category": category,
        "blocked": blocked,
        "block_reason": block_reason,
        "layer_triggered": layer_triggered,
        "latency_ms": latency_ms,
        "rag_used": rag_used,
        "is_emergency": is_emergency,
    }
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _write_log, event)


def _write_log(event: dict):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
