import uuid
import time
from typing import Optional
from dataclasses import dataclass, field
from backend.config import settings

SESSIONS: dict[str, "Session"] = {}


@dataclass
class Session:
    session_id: str
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    history: list[dict] = field(default_factory=list)
    query_count: int = 0

    def is_expired(self) -> bool:
        timeout_seconds = settings.SESSION_TIMEOUT_MINUTES * 60
        return (time.time() - self.last_active) > timeout_seconds

    def add_exchange(self, user_message: str, assistant_message: str):
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "model", "content": assistant_message})
        self.query_count += 1
        self.last_active = time.time()
        # Keep only the last N turns
        max_messages = settings.MAX_HISTORY_TURNS * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]

    def get_history_for_api(self) -> list[dict]:
        return self.history.copy()


def get_or_create_session(session_id: Optional[str] = None) -> Session:
    if session_id and session_id in SESSIONS:
        session = SESSIONS[session_id]
        if not session.is_expired():
            session.last_active = time.time()
            return session
    new_id = session_id or str(uuid.uuid4())
    session = Session(session_id=new_id)
    SESSIONS[new_id] = session
    return session


def clear_session(session_id: str) -> bool:
    if session_id in SESSIONS:
        del SESSIONS[session_id]
        return True
    return False


def cleanup_expired_sessions():
    expired = [sid for sid, s in SESSIONS.items() if s.is_expired()]
    for sid in expired:
        del SESSIONS[sid]
    return len(expired)
