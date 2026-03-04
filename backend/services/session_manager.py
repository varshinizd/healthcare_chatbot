import uuid
import time
from typing import Dict, List, Optional


class SessionManager:
    def __init__(self):
        # session_id → session data
        self._sessions: Dict[str, dict] = {}

        # auto cleanup timeout (30 minutes)
        self.session_timeout = 60 * 30

    # =====================================================
    # SESSION LIFECYCLE
    # =====================================================

    def create_session(self) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())

        self._sessions[session_id] = {
            "history": [],
            "created_at": time.time(),
            "last_accessed": time.time(),

            # conversational diagnosis state
            "pending_questions": [],
            "collected_answers": [],
            "candidate_diseases": [],
            "diagnostic_state": "INITIAL",  # INITIAL | GATHERING | CLARIFYING | FINAL

            # session state
            "status": "ACTIVE"  # ACTIVE | ENDED | EMERGENCY_LOCKED
        }

        return session_id

    def end_session(self, session_id: str):
        """End and delete a session"""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def reset_all_sessions(self):
        """Hard reset like restarting server"""
        self._sessions.clear()

    def lock_emergency(self, session_id: str):
        """Lock session after emergency detection"""
        if session_id in self._sessions:
            self._sessions[session_id]["status"] = "EMERGENCY_LOCKED"

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup_expired_sessions(self):
        """Remove inactive sessions"""
        now = time.time()

        expired = [
            sid for sid, sess in self._sessions.items()
            if now - sess["last_accessed"] > self.session_timeout
        ]

        for sid in expired:
            del self._sessions[sid]

    # =====================================================
    # SESSION ACCESS
    # =====================================================

    def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve session if active"""
        session = self._sessions.get(session_id)

        if session and session["status"] in ["ACTIVE", "EMERGENCY_LOCKED"]:
            session["last_accessed"] = time.time()
            return session

        return None

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    def add_message(self, session_id: str, role: str, message: str):
        """Add message to chat history"""
        if session_id in self._sessions:
            history = self._sessions[session_id]["history"]

            history.append({
                "role": role,
                "parts": [message]
            })

            # keep history bounded (avoid token explosion)
            if len(history) > 20:
                history.pop(0)

    def get_history(self, session_id: str) -> List[dict]:
        """Get conversation history"""
        if session_id in self._sessions:
            return self._sessions[session_id]["history"]
        return []

    # =====================================================
    # FOLLOW-UP QUESTION FLOW
    # =====================================================

    def set_followups(self, session_id: str, questions: List[str]):
        """Store follow-up questions"""
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
        """Store user's follow-up answer"""
        if session_id in self._sessions:
            self._sessions[session_id]["collected_answers"].append(answer)

    def has_pending_questions(self, session_id: str) -> bool:
        """Check if follow-up questions remain"""
        if session_id in self._sessions:
            return len(self._sessions[session_id]["pending_questions"]) > 0
        return False

    def clear_followups(self, session_id: str):
        """Stop questioning flow"""
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
            return self._sessions[session_id].get(
                "diagnostic_state",
                "INITIAL"
            )
        return "INITIAL"