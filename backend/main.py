from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse
from services.session_manager import SessionManager
from services.llm_service import LLMService
from services.risk_classifier import RiskClassifier
from services.risk_classifier import RiskClassifier
from services.query_analyzer import QueryAnalyzer

app = FastAPI(title="Healthcare Symptom Chatbot")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
session_manager = SessionManager()
llm_service = LLMService()
risk_classifier = RiskClassifier()
query_analyzer = QueryAnalyzer()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id
    
    # 1. Get or Create Session
    if not session_id:
        session_id = session_manager.create_session()
    
    session = session_manager.get_session(session_id)
    if not session:
        session_id = session_manager.create_session()
        session = session_manager.get_session(session_id)

    # 2. Add User Message to History
    session_manager.add_message(session_id, "user", request.message)

    # ============================================================
    # DETERMINISTIC LAYER
    # ============================================================
    
    # 3. Classify Risk (Fail-safe)
    risk_level = risk_classifier.classify_risk(request.message)
    print(f"Detected Risk Level: {risk_level}")

    bot_response_text = ""

    if risk_level == "HIGH":
        # BYPASS LLM completely for High Risk
        bot_response_text = risk_classifier.get_emergency_response()
    
    else:
        # LOW or MEDIUM: Use Router to decide action
        
        # 4. Analyze Intent
        # Get history properly for analysis
        history = session_manager.get_history(session_id)
        # Convert to simple list of strings for analyzer if needed, or pass full logic
        # For simplicity, pass the last few messages text
        history_text = [f"{msg['role']}: {msg['parts'][0]}" for msg in history[-4:]] # Last 4 turns
        
        analysis = await query_analyzer.analyze(request.message, history_text)
        print(f"Query Analysis: {analysis}")
        
        intent = analysis.get("intent", "MEDICAL")
        completeness = analysis.get("completeness", "VAGUE")
        question_to_ask = analysis.get("question_to_ask", "")

        if intent == "NON_MEDICAL":
             bot_response_text = "I apologize, but I am a healthcare assistant and can only help with medical queries."
             
        elif intent == "GREETING":
             bot_response_text = "Hello! I am your AI Health Assistant. How can I help you today?"
             
        elif intent == "MEDICAL":
             if completeness == "VAGUE":
                  # Ask the question provided by analyzer
                  bot_response_text = question_to_ask if question_to_ask else "Could you provide more details about your symptoms?"
             else:
                  # SPECIFIC -> Just ask Gemini directly (No RAG)
                  
                  # Generate Report
                  past_history = history[:-1]
                  bot_response_text = await llm_service.generate_response(past_history, request.message)
        
        else:
             # Fallback
             bot_response_text = "I'm not sure I understand. Could you describe your symptoms?"
    
    # 7. Add Bot Response to History
    session_manager.add_message(session_id, "model", bot_response_text)
    
    return ChatResponse(response=bot_response_text, session_id=session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
