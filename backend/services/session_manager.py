import uuid
from typing import Dict, List, Optional
import time

class SessionManager:
    def __init__(self):
        # In-memory storage: {session_id: [{'role': 'user'|'model', 'parts': [text]}]}
        # Also storing timestamps to potentially clean up old sessions (not implemented yet but good hygiene)
        self._sessions: Dict[str, dict] = {}

    def create_session(self) -> str:
        """Generates a new session ID and initializes memory."""
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "history": [],
            "created_at": time.time(),
            "last_accessed": time.time()
        }
        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieves session data if it exists."""
        if session_id in self._sessions:
            self._sessions[session_id]["last_accessed"] = time.time()
            return self._sessions[session_id]
        return None

    def add_message(self, session_id: str, role: str, message: str):
        """Adds a message to the session history."""
        if session_id in self._sessions:
            self._sessions[session_id]["history"].append({"role": role, "parts": [message]})

    def get_history(self, session_id: str) -> List[dict]:
        """Returns the conversation history for the LLM."""
        if session_id in self._sessions:
            return self._sessions[session_id]["history"]
        return []
