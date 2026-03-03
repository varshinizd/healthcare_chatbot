from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse

from services.session_manager import SessionManager
from services.llm_service import LLMService
from services.risk_classifier import RiskClassifier
from services.query_analyzer import QueryAnalyzer
from services.rag_engine import RAGEngine
from services.diagnosis_service import DiagnosisService

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
diagnosis_service = DiagnosisService(rag_engine)


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
    # ============================================================
    # CHECK IF QUESTIONING MODE ACTIVE (Clarifying or Gathering)
    # ============================================================
    state = session_manager.get_diagnostic_state(session_id)
    
    # Process answer if we were waiting for one
    if state in ["CLARIFYING", "GATHERING"]:
        session_manager.add_answer(session_id, request.message)
        
        if session_manager.has_pending_questions(session_id):
            next_q = session_manager.get_next_question(session_id)
            if next_q:
                session_manager.add_message(session_id, "model", next_q)
                return ChatResponse(response=next_q, session_id=session_id)
        
        # If no more questions, transition based on current state
        if state == "CLARIFYING":
            session_manager.set_diagnostic_state(session_id, "FINAL")
            state = "FINAL"
        else: # GATHERING -> try to narrow down now
            session_manager.set_diagnostic_state(session_id, "INITIAL")
            state = "INITIAL"
            # Proceed to analysis below with the collected info

    if state == "FINAL":
        history = session_manager.get_history(session_id)
        diseases = session_manager.get_candidate_diseases(session_id)
        bot_response_text = await diagnosis_service.get_final_diagnosis(diseases, history)
        session_manager.add_message(session_id, "model", bot_response_text)
        return ChatResponse(response=bot_response_text, session_id=session_id)

    # ============================================================
    # ANALYZE QUERY (INITIAL or NARROWING PHASE)
    # ============================================================
    history = session_manager.get_history(session_id)
    history_text = [f"{msg['role']}: {msg['parts'][0]}" for msg in history[-4:]]

    analysis = await query_analyzer.analyze(request.message, history_text)
    print(f"Query Analysis: {analysis}")

    intent = analysis.get("intent", "MEDICAL")
    completeness = analysis.get("completeness", "VAGUE")
    followups = analysis.get("follow_up_questions", [])
    potential_diseases = analysis.get("potential_diseases", [])

    # ---------------- NON MEDICAL ----------------
    if intent == "NON_MEDICAL":
        bot_response_text = "I am a healthcare assistant and can only help with medical queries."

    # ---------------- GREETING ----------------
    elif intent == "GREETING":
        bot_response_text = "Hello! I'm your AI Health Assistant. Tell me your symptoms."

    # ---------------- MEDICAL ----------------
    elif intent == "MEDICAL":
        # ENOUGH INFO TO NARROW DOWN -> START CLARIFICATION FLOW
        if potential_diseases and len(potential_diseases) >= 1:
            print(f"Narrowed down to: {potential_diseases}")
            session_manager.set_candidate_diseases(session_id, potential_diseases)
            session_manager.set_diagnostic_state(session_id, "CLARIFYING")
            
            # Generate 4 targeted questions
            clarifying_qs = await diagnosis_service.generate_clarifying_questions(potential_diseases, request.message)
            session_manager.set_followups(session_id, clarifying_qs[:4]) # Strict limit
            
            first_q = session_manager.get_next_question(session_id)
            bot_response_text = first_q if first_q else "Could you explain more?"

        # 🔍 NEED MORE INFO TO REACH NARROWING STAGE
        elif completeness == "VAGUE" and followups:
            session_manager.set_diagnostic_state(session_id, "GATHERING")
            session_manager.set_followups(session_id, followups[:4]) # Strict limit
            first_q = session_manager.get_next_question(session_id)
            bot_response_text = first_q if first_q else "Could you explain more?"

        # 🧠 FALLBACK (if something goes wrong)
        else:
            context = rag_engine.search(request.message)
            bot_response_text = await llm_service.generate_response(history[:-1], request.message, context=context)

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
