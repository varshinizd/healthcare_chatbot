import uuid
from typing import Dict, List, Optional
import time

class SessionManager:
    def __init__(self):
        # session_id → session data
        self._sessions: Dict[str, dict] = {}

    def create_session(self) -> str:
        """Create new session"""
        session_id = str(uuid.uuid4())

        self._sessions[session_id] = {
            "history": [],
            "created_at": time.time(),
            "last_accessed": time.time(),

            # ⭐ NEW (for conversational questioning)
            "pending_questions": [],     # questions yet to ask
            "collected_answers": []      # user answers
        }

        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session"""
        if session_id in self._sessions:
            self._sessions[session_id]["last_accessed"] = time.time()
            return self._sessions[session_id]
        return None

    def add_message(self, session_id: str, role: str, message: str):
        """Add chat message"""
        if session_id in self._sessions:
            self._sessions[session_id]["history"].append({
                "role": role,
                "parts": [message]
            })

    def get_history(self, session_id: str) -> List[dict]:
        """Get conversation history"""
        if session_id in self._sessions:
            return self._sessions[session_id]["history"]
        return []

    # ⭐ NEW HELPERS FOR FOLLOW-UP FLOW
    def set_followups(self, session_id: str, questions: list):
        if session_id in self._sessions:
            self._sessions[session_id]["pending_questions"] = questions
            self._sessions[session_id]["collected_answers"] = []

    def get_next_question(self, session_id: str) -> Optional[str]:
        if session_id in self._sessions:
            pending = self._sessions[session_id]["pending_questions"]
            if pending:
                return pending.pop(0)
        return None

    def add_answer(self, session_id: str, answer: str):
        if session_id in self._sessions:
            self._sessions[session_id]["collected_answers"].append(answer)

    def has_pending_questions(self, session_id: str) -> bool:
        if session_id in self._sessions:
            return len(self._sessions[session_id]["pending_questions"]) > 0
        return False

    def clear_followups(self, session_id: str):
        if session_id in self._sessions:
            self._sessions[session_id]["pending_questions"] = []
            self._sessions[session_id]["collected_answers"] = []
