import uuid
from typing import Dict, List, Optional
import time


class SessionManager:
    def __init__(self):
        # session_id → session data
        self._sessions: Dict[str, dict] = {}

    # =====================================================
    # SESSION LIFECYCLE
    # =====================================================

    def create_session(self) -> str:
        """Create new session"""
        session_id = str(uuid.uuid4())

        self._sessions[session_id] = {
            "history": [],
            "created_at": time.time(),
            "last_accessed": time.time(),

            # conversational diagnosis state
            "pending_questions": [],
            "collected_answers": [],
            "candidate_diseases": [],
            "diagnostic_state": "INITIAL",  # INITIAL | NARROWING | CLARIFYING | FINAL
            "status": "ACTIVE"              # ⭐ NEW → ACTIVE | ENDED
        }

        return session_id

    def end_session(self, session_id: str):
        """End and delete a session (like CTRL+C for one user)"""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def reset_all_sessions(self):
        """Hard reset like restarting the server"""
        self._sessions.clear()

    # =====================================================
    # SESSION ACCESS
    # =====================================================

    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session"""
        session = self._sessions.get(session_id)

        if session and session["status"] == "ACTIVE":
            session["last_accessed"] = time.time()
            return session

        return None

    # =====================================================
    # CHAT HISTORY
    # =====================================================

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

    # =====================================================
    # FOLLOW-UP QUESTION FLOW
    # =====================================================

    def set_followups(self, session_id: str, questions: List[str]):
        """Store follow-up questions and reset answers"""
        if session_id in self._sessions:
            self._sessions[session_id]["pending_questions"] = list(questions)
            self._sessions[session_id]["collected_answers"] = []

    def get_next_question(self, session_id: str) -> Optional[str]:
        """Return next follow-up question"""
        if session_id in self._sessions:
            pending = self._sessions[session_id]["pending_questions"]
            if pending:
                return pending.pop(0)
        return None

    def add_answer(self, session_id: str, answer: str):
        """Store user's answer"""
        if session_id in self._sessions:
            self._sessions[session_id]["collected_answers"].append(answer)

    def has_pending_questions(self, session_id: str) -> bool:
        """Check if more followups exist"""
        if session_id in self._sessions:
            return len(self._sessions[session_id]["pending_questions"]) > 0
        return False

    def clear_followups(self, session_id: str):
        """Stop follow-up questioning"""
        if session_id in self._sessions:
            self._sessions[session_id]["pending_questions"] = []
            self._sessions[session_id]["collected_answers"] = []

    # =====================================================
    # DIAGNOSTIC STATE MANAGEMENT
    # =====================================================

    def set_candidate_diseases(self, session_id: str, diseases: List[str]):
        if session_id in self._sessions:
            self._sessions[session_id]["candidate_diseases"] = diseases

    def get_candidate_diseases(self, session_id: str) -> List[str]:
        if session_id in self._sessions:
            return self._sessions[session_id].get("candidate_diseases", [])
        return []

    def set_diagnostic_state(self, session_id: str, state: str):
        if session_id in self._sessions:
            self._sessions[session_id]["diagnostic_state"] = state

    def get_diagnostic_state(self, session_id: str) -> str:
        if session_id in self._sessions:
            return self._sessions[session_id].get("diagnostic_state", "INITIAL")
        return "INITIAL"