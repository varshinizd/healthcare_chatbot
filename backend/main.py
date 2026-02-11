from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse

from services.session_manager import SessionManager
from services.llm_service import LLMService
from services.risk_classifier import RiskClassifier
from services.query_analyzer import QueryAnalyzer
from services.rag_engine import RAGEngine

app = FastAPI(title="Healthcare Symptom Chatbot")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- SERVICES ----------------
session_manager = SessionManager()
llm_service = LLMService()
risk_classifier = RiskClassifier()
query_analyzer = QueryAnalyzer()
rag_engine = RAGEngine("medical_clean.json")


# ---------------- CHAT ENDPOINT ----------------
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    session_id = request.session_id

    # 1️⃣ Create session if needed
    if not session_id:
        session_id = session_manager.create_session()

    session = session_manager.get_session(session_id)
    if not session:
        session_id = session_manager.create_session()
        session = session_manager.get_session(session_id)

    # 2️⃣ Add user message
    session_manager.add_message(session_id, "user", request.message)

    # ============================================================
    # 🚨 RISK CHECK
    # ============================================================
    risk_level = risk_classifier.classify_risk(request.message)
    print(f"Detected Risk Level: {risk_level}")

    if risk_level == "HIGH":
        bot_response_text = risk_classifier.get_emergency_response()
        session_manager.add_message(session_id, "model", bot_response_text)
        return ChatResponse(response=bot_response_text, session_id=session_id)

    # ============================================================
    # 🧠 CHECK IF FOLLOW-UP MODE ACTIVE
    # ============================================================
    if session_manager.has_pending_questions(session_id):
        # store user's answer
        session_manager.add_answer(session_id, request.message)

        # ask next question
        next_q = session_manager.get_next_question(session_id)

        if next_q:
            bot_response_text = next_q
            session_manager.add_message(session_id, "model", bot_response_text)
            return ChatResponse(response=bot_response_text, session_id=session_id)
        else:
            # finished all questions → continue to diagnosis
            pass

    # ============================================================
    # 🧠 ANALYZE QUERY
    # ============================================================
    history = session_manager.get_history(session_id)

    history_text = [
        f"{msg['role']}: {msg['parts'][0]}"
        for msg in history[-4:]
    ]

    analysis = await query_analyzer.analyze(request.message, history_text)
    print(f"Query Analysis: {analysis}")

    intent = analysis.get("intent", "MEDICAL")
    completeness = analysis.get("completeness", "VAGUE")
    followups = analysis.get("follow_up_questions", [])

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

        # 🔍 NEED MORE INFO → START QUESTION FLOW
        if completeness == "VAGUE" and followups:
            session_manager.set_followups(session_id, followups)

            first_q = session_manager.get_next_question(session_id)
            bot_response_text = first_q if first_q else "Could you explain more?"

        # 🧠 ENOUGH INFO → RAG + LLM
        else:
            print("🔎 RAG searching knowledge base...")

            context = rag_engine.search(request.message)

            past_history = history[:-1]

            bot_response_text = await llm_service.generate_response(
                past_history,
                request.message,
                context=context
            )

    # ---------------- FALLBACK ----------------
    else:
        bot_response_text = "I'm not sure I understand. Could you explain your symptoms?"

    # 5️⃣ store bot message
    session_manager.add_message(session_id, "model", bot_response_text)

    return ChatResponse(response=bot_response_text, session_id=session_id)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
