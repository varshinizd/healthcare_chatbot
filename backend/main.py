from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse

from services.session_manager import SessionManager
from services.llm_service import LLMService
from services.risk_classifier import RiskClassifier
from services.query_analyzer import QueryAnalyzer
from services.rag_engine import RAGEngine
from services.diagnosis_service import DiagnosisService

# =====================================================
# APP SETUP
# =====================================================

app = FastAPI(title="Healthcare Symptom Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# SERVICES INITIALIZATION
# =====================================================

session_manager = SessionManager()
llm_service = LLMService()
risk_classifier = RiskClassifier()
query_analyzer = QueryAnalyzer()
rag_engine = RAGEngine("medical_clean.json")
diagnosis_service = DiagnosisService(rag_engine)


# =====================================================
# TOPIC SHIFT DETECTOR
# =====================================================

def is_topic_shift(user_message: str, has_pending: bool) -> bool:
    """
    Detect when user introduces a new condition
    during followup questioning.
    """

    if not has_pending:
        return False

    msg = user_message.lower()

    # short answers usually belong to followups
    if len(msg.split()) <= 3:
        return False

    triggers = [
        "i have",
        "i feel",
        "i am having",
        "diagnosed",
        "pain",
        "symptom",
    ]

    return any(t in msg for t in triggers)


# =====================================================
# CHAT ENDPOINT
# =====================================================

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    session_id = request.session_id

    # ---------------- CREATE SESSION ----------------
    if not session_id:
        session_id = session_manager.create_session()

    session = session_manager.get_session(session_id)
    if not session:
        session_id = session_manager.create_session()
        session = session_manager.get_session(session_id)

    user_message = request.message

    # store message
    session_manager.add_message(session_id, "user", user_message)

    # =====================================================
    # RISK CHECK
    # =====================================================
    risk_level = risk_classifier.classify_risk(user_message)
    print(f"Detected Risk Level: {risk_level}")

    if risk_level == "HIGH":
        bot_response_text = risk_classifier.get_emergency_response()
        session_manager.lock_emergency(session_id)
        session_manager.add_message(session_id, "model", bot_response_text)

        return ChatResponse(
            response=bot_response_text,
            session_id=session_id
        )

    # =====================================================
    # FOLLOWUP MODE + TOPIC SHIFT
    # =====================================================

    state = session_manager.get_diagnostic_state(session_id)
    has_pending = session_manager.has_pending_questions(session_id)

    # detect new condition mid conversation
    if is_topic_shift(user_message, has_pending):
        print("Topic shift detected → resetting diagnosis")

        session_manager.clear_followups(session_id)
        session_manager.set_candidate_diseases(session_id, [])
        session_manager.set_diagnostic_state(session_id, "INITIAL")

        state = "INITIAL"
        has_pending = False

    # continue questioning
    if state in ["CLARIFYING", "GATHERING"] and has_pending:

        session_manager.add_answer(session_id, user_message)

        next_q = session_manager.get_next_question(session_id)
        if next_q:
            session_manager.add_message(session_id, "model", next_q)
            return ChatResponse(response=next_q, session_id=session_id)

        # transition state
        if state == "CLARIFYING":
            session_manager.set_diagnostic_state(session_id, "FINAL")
            state = "FINAL"
        else:
            session_manager.set_diagnostic_state(session_id, "INITIAL")
            state = "INITIAL"

    # =====================================================
    # FINAL DIAGNOSIS
    # =====================================================

    if state == "FINAL":
        history = session_manager.get_history(session_id)
        diseases = session_manager.get_candidate_diseases(session_id)

        bot_response_text = await diagnosis_service.get_final_diagnosis(
            diseases,
            history
        )

        session_manager.add_message(session_id, "model", bot_response_text)

        return ChatResponse(
            response=bot_response_text,
            session_id=session_id
        )

    # =====================================================
    # ANALYSIS PHASE
    # =====================================================

    history = session_manager.get_history(session_id)
    history_text = [
        f"{m['role']}: {m['parts'][0]}"
        for m in history[-4:]
    ]

    analysis = await query_analyzer.analyze(user_message, history_text)
    print(f"Query Analysis: {analysis}")

    intent = analysis.get("intent", "MEDICAL")
    completeness = analysis.get("completeness", "VAGUE")
    followups = analysis.get("follow_up_questions", [])
    potential_diseases = analysis.get("potential_diseases", [])

    # ---------------- NON MEDICAL ----------------
    if intent == "NON_MEDICAL":
        bot_response_text = (
            "I am a healthcare assistant and can only help with medical queries."
        )

    # ---------------- GREETING ----------------
    elif intent == "GREETING":
        bot_response_text = (
            "Hello! I'm your AI Health Assistant. Tell me your symptoms."
        )

    # ---------------- MEDICAL ----------------
    elif intent == "MEDICAL":

        # clarification stage
        if potential_diseases:
            print(f"Narrowed down to: {potential_diseases}")

            session_manager.set_candidate_diseases(
                session_id,
                potential_diseases
            )

            session_manager.set_diagnostic_state(
                session_id,
                "CLARIFYING"
            )

            clarifying_qs = await diagnosis_service.generate_clarifying_questions(
                potential_diseases,
                user_message
            )

            session_manager.set_followups(session_id, clarifying_qs[:4])

            first_q = session_manager.get_next_question(session_id)
            bot_response_text = first_q or "Could you explain more?"

        # need more info
        elif completeness == "VAGUE" and followups:
            session_manager.set_diagnostic_state(session_id, "GATHERING")
            session_manager.set_followups(session_id, followups[:4])

            first_q = session_manager.get_next_question(session_id)
            bot_response_text = first_q or "Could you explain more?"

        # RAG + self reasoning fallback
        else:
            context = rag_engine.search(user_message)

            bot_response_text = await llm_service.generate_response(
                history[:-1],
                user_message,
                context=context if context else "",
                mode="NORMAL"
            )

    # ---------------- UNKNOWN ----------------
    else:
        bot_response_text = (
            "I'm not sure I understand. Could you explain your symptoms?"
        )

    # store bot reply
    session_manager.add_message(session_id, "model", bot_response_text)

    return ChatResponse(
        response=bot_response_text,
        session_id=session_id
    )


# =====================================================
# RUN SERVER (WORKS WITH python main.py)
# =====================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )