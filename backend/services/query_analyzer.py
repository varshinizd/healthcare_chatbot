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


# -------- RESPONSE STRUCTURE --------
class QueryAnalysis(BaseModel):
    intent: str = Field(..., description="MEDICAL, NON_MEDICAL, GREETING")
    completeness: str = Field(..., description="VAGUE or SPECIFIC")
    follow_up_questions: list[str] = Field(default_factory=list, description="List of follow-up questions if vague")
    search_term: str = Field(default="", description="Search query if specific")


# -------- ANALYZER CLASS --------
class QueryAnalyzer:

    def __init__(self):
        self.system_prompt = """
You are an expert clinical triage AI acting like a real doctor.

Return ONLY valid JSON:
intent: MEDICAL | NON_MEDICAL | GREETING
completeness: VAGUE | SPECIFIC
follow_up_questions: list of questions if more info needed
search_term: search query if enough info

IMPORTANT RULES:
- NEVER repeat same fixed questions.
- Generate questions dynamically based on user symptoms.
- Each conversation should feel natural and different.
- Ask one key question at a time like a real consultation.
- Focus on duration, severity, triggers, associated symptoms.
- Avoid robotic or template questions.

Only mark SPECIFIC when enough information gathered.
"""

    async def analyze(self, user_message: str, history: list) -> dict:

        turn_count = (len(history) // 2) + 1

        prompt = f"""
SYSTEM:
{self.system_prompt}

Conversation Turn: {turn_count}/4
Chat History: {history}

User Message:
{user_message}

Return only JSON.
"""

        for _ in range(2):
            try:
                response = await asyncio.to_thread(
                    client.models.generate_content,
                    model="gemini-2.5-flash-lite",
                    contents=prompt,
                )

                text = response.text.strip()

                # remove ```json if model adds
                if text.startswith("```"):
                    text = text.replace("```json", "").replace("```", "").strip()

                data = json.loads(text)

                # 🛡 ensure at least 2 follow-up questions if vague medical
                if data.get("intent") == "MEDICAL" and data.get("completeness") == "VAGUE":
                    qs = data.get("follow_up_questions", [])

                    if len(qs) < 2:
                        qs.append("Since when are you experiencing this?")
                        qs.append("Are there any other symptoms like fever, pain, or fatigue?")

                    data["follow_up_questions"] = qs

                return data

            except Exception as e:
                print("Analyzer error:", e)
                await asyncio.sleep(1)

        # fallback if model fails
        return {
            "intent": "MEDICAL",
            "completeness": "VAGUE",
            "follow_up_questions": [
                "Since when are you experiencing this?",
                "Can you describe your symptoms more clearly?"
            ],
            "search_term": ""
        }
