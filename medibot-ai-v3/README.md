# 🏥 MediBot AI

**An Intelligent Domain-Restricted Medical Conversational Agent with RAG, Safety Guardrails, and Emergency Detection**

> Final Year Computer Science Project — demonstrating LLM integration, Retrieval-Augmented Generation, multi-layer AI safety, and healthcare AI ethics.

---

## ✅ Features

- **💬 Medical Chat** — Gemini 2.5 Flash answers questions on symptoms, conditions, medications, anatomy, and more
- **🚨 Emergency Detection** — Regex-based detector covering 40+ patterns (cardiac, neurological, respiratory, toxicological, psychiatric, trauma) responds instantly without an API call
- **🛡️ 7-Layer Guardrail Pipeline** — Emergency detection → Input sanitization → Medical classifier → RAG retrieval → Generation → Response validation → Audit logging
- **📚 RAG Pipeline** — ChromaDB vector store with 300+ curated medical knowledge chunks for grounded, accurate responses
- **🔒 Domain Restriction** — Gemini Flash classifier blocks all non-medical queries
- **📝 Audit Logging** — Every interaction logged to `chat_log.jsonl` with full metadata
- **👍 Feedback System** — Thumbs up/down on each response, stored for analysis
- **⚕️ Safety by Design** — Every response validated for disclaimer presence; diagnostic language detection

---

## 🗂️ Project Structure

```
medibot-ai/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Centralized settings
│   ├── prompts.py               # System prompt + templates
│   ├── session.py               # In-memory session management
│   ├── core/
│   │   ├── emergency.py         # Regex emergency detector
│   │   ├── classifier.py        # Medical intent classifier
│   │   ├── gemini_client.py     # Gemini API wrapper
│   │   ├── rag_pipeline.py      # ChromaDB RAG retrieval
│   │   ├── guardrails.py        # 7-layer safety pipeline
│   │   ├── response_validator.py
│   │   └── audit_logger.py
│   ├── routers/
│   │   ├── chat.py              # POST /chat
│   │   ├── health.py            # GET /health
│   │   └── feedback.py          # POST /feedback
│   ├── models/schemas.py
│   ├── data/
│   │   ├── seed_kb.py           # Build ChromaDB index
│   │   └── medical_kb/          # Curated text knowledge base
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── context/ChatContext.jsx
│   │   ├── components/
│   │   │   ├── chat/            # ChatWindow, MessageBubble, InputBar, etc.
│   │   │   ├── layout/          # Header, Sidebar, DisclaimerBanner, AboutView
│   │   │   └── modals/          # EmergencyModal, HipaaModal
│   │   ├── hooks/useEmergencyDetect.js
│   │   ├── constants/           # Emergency keywords, quick prompts
│   │   └── utils/               # API, formatters
│   └── package.json
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Gemini API key from [Google AI Studio](https://aistudio.google.com)

### 1. Clone and configure

```bash
git clone <repo-url>
cd medibot-ai
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Build the ChromaDB vector index (requires Gemini API key in .env)
python -m backend.data.seed_kb

# Start the server
uvicorn backend.main:app --reload --port 8000
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | *required* | Google AI Studio API key |
| `GEMINI_PRO_MODEL` | `gemini-1.5-pro` | Main generation model |
| `GEMINI_FLASH_MODEL` | `gemini-1.5-flash` | Fast classifier model |
| `MAX_HISTORY_TURNS` | `10` | Conversation turns kept in memory |
| `SESSION_TIMEOUT_MINUTES` | `30` | Session expiry time |
| `RATE_LIMIT` | `20/minute` | Per-IP rate limit |
| `RAG_TOP_K` | `3` | Knowledge chunks retrieved per query |
| `MIN_CONFIDENCE_SCORE` | `0.75` | Classifier confidence threshold |

---

## 🛡️ Guardrail Pipeline

```
Layer 1  Emergency Detection     regex, <5ms      → instant 911 response
Layer 2  Input Sanitization      regex patterns   → block prompt injections
Layer 3  Medical Classifier      Gemini Flash     → block non-medical queries
Layer 4  RAG Retrieval           ChromaDB cosine  → enrich prompt with KB
Layer 5  Response Generation     Gemini Pro       → generate answer
Layer 6  Response Validation     pattern check    → ensure disclaimer present
Layer 7  Audit Logging           async JSONL      → record all metadata
```

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chat` | Send a message, get a response |
| `GET` | `/health` | App health + RAG status |
| `POST` | `/feedback` | Submit thumbs up/down feedback |

**POST /chat request:**
```json
{
  "message": "What are symptoms of Type 2 diabetes?",
  "session_id": "optional-existing-session-id",
  "stream": false
}
```

**POST /chat response:**
```json
{
  "reply": "Common symptoms of Type 2 diabetes include...",
  "session_id": "abc123",
  "blocked": false,
  "is_emergency": false,
  "category": "conditions",
  "rag_used": true,
  "latency_ms": 1423.5,
  "message_id": "msg-uuid"
}
```

---

## 🔬 Emergency Detection Categories

| Category | Examples |
|---|---|
| Cardiac | chest pain, heart attack, cardiac arrest |
| Neurological | stroke, seizure, loss of consciousness |
| Respiratory | can't breathe, choking, asthma attack |
| Toxicological | overdose, poisoning |
| Psychiatric | suicidal ideation, self-harm |
| Trauma | severe bleeding, unconscious |
| Allergic | anaphylaxis, throat swelling |

---

## 🎓 Academic Context

Built as a final-year Computer Science project demonstrating:
- Large Language Model integration and prompt engineering
- Retrieval-Augmented Generation (RAG) with vector databases
- Multi-layer AI safety architecture
- Healthcare AI ethics and HIPAA-aware design
- Full-stack system design with FastAPI + React

---

## 🛠️ Tech Stack

**Backend:** Python · FastAPI · Google Gemini AI · ChromaDB · Pydantic · uvicorn · slowapi

**Frontend:** React 18 · Vite · Tailwind CSS · react-markdown · Lucide React

---

## ⚠️ Disclaimer

MediBot AI is a computer science educational project. It does **not** provide medical advice, diagnosis, or treatment recommendations. Always consult a qualified healthcare professional.

---

## 📄 License

MIT License — see LICENSE for details.
