import os
import json
import asyncio
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY missing")

client = genai.Client(api_key=API_KEY)


# =====================================================
# RESPONSE STRUCTURE
# =====================================================
class QueryAnalysis(BaseModel):
    intent: str = Field(..., description="MEDICAL, NON_MEDICAL, GREETING")
    completeness: str = Field(..., description="VAGUE or SPECIFIC")
    follow_up_questions: list[str] = Field(default_factory=list)
    search_term: str = Field(default="")
    potential_diseases: list[str] = Field(default_factory=list)


# =====================================================
# ANALYZER CLASS
# =====================================================
class QueryAnalyzer:

    def __init__(self):
        self.system_prompt = """
You are an expert clinical triage AI acting like a real doctor.

Return ONLY valid JSON with keys:
intent
completeness
follow_up_questions
potential_diseases
search_term

RULES:
- intent = MEDICAL | NON_MEDICAL | GREETING
- Identify up to 3 likely diseases ONLY if enough symptoms exist.
- If greeting → GREETING
- If not health related → NON_MEDICAL
- If symptoms unclear → VAGUE
- Ask natural follow-up questions when vague.
- Prefer duration, severity, progression, triggers, associated symptoms.
- NEVER include explanations outside JSON.
"""

    # =====================================================
    # ANALYZE QUERY
    # =====================================================
    async def analyze(self, user_message: str, history: list) -> dict:

        # ---- build readable history ----
        history_text = "\n".join(history[-4:]) if history else ""

        turn_count = (len(history) // 2) + 1

        prompt = f"""
SYSTEM:
{self.system_prompt}

Conversation Turn: {turn_count}/4

Chat History:
{history_text}

User Message:
{user_message}

Return ONLY JSON.
"""

        for _ in range(2):
            try:
                response = await asyncio.to_thread(
                    client.models.generate_content,
                    model="gemini-2.5-flash-lite",
                    contents=prompt,
                )

                text = response.text.strip()

                # -------------------------------------------------
                # SAFE JSON EXTRACTION ⭐ (important)
                # -------------------------------------------------
                if "```" in text:
                    parts = text.split("```")
                    if len(parts) >= 3:
                        text = parts[-2].strip()

                start = text.find("{")
                end = text.rfind("}") + 1
                text = text[start:end]

                data = json.loads(text)

                # -------------------------------------------------
                # NORMALIZATION SAFETY
                # -------------------------------------------------
                data.setdefault("intent", "MEDICAL")
                data.setdefault("completeness", "VAGUE")
                data.setdefault("follow_up_questions", [])
                data.setdefault("potential_diseases", [])
                data.setdefault("search_term", "")

                # limit diseases strictly
                data["potential_diseases"] = data["potential_diseases"][:3]

                # ensure followups exist if vague medical
                if (
                    data["intent"] == "MEDICAL"
                    and data["completeness"] == "VAGUE"
                ):
                    qs = data["follow_up_questions"]

                    if len(qs) < 2:
                        qs.extend([
                            "Since when are you experiencing this?",
                            "Are there any associated symptoms like fever, pain, or fatigue?"
                        ])

                    data["follow_up_questions"] = qs[:4]

                return data

            except Exception as e:
                print("Analyzer error:", e)
                await asyncio.sleep(1)

        # -------------------------------------------------
        # SAFE FALLBACK
        # -------------------------------------------------
        return {
            "intent": "MEDICAL",
            "completeness": "VAGUE",
            "follow_up_questions": [
                "Since when are you experiencing this?",
                "Can you describe your symptoms more clearly?"
            ],
            "potential_diseases": [],
            "search_term": ""
        }