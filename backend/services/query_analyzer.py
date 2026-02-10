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
    completeness: str = Field(..., description="VAGUE, SPECIFIC, or N/A")
    question_to_ask: str = Field(..., description="Clarifying question if vague")
    search_term: str = Field(..., description="Search query if specific")


# -------- ANALYZER CLASS --------
class QueryAnalyzer:

    def __init__(self):
        self.system_prompt = """
You are an expert clinical triage AI.

Return ONLY valid JSON with:
intent: MEDICAL | NON_MEDICAL | GREETING
completeness: VAGUE | SPECIFIC | N/A
question_to_ask: ask only if vague
search_term: search query only if specific

Rules:
- If greeting → GREETING
- If normal talk → NON_MEDICAL
- If symptoms → MEDICAL
- If symptoms unclear → VAGUE
- If enough detail → SPECIFIC
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

                return json.loads(text)

            except Exception as e:
                print("Analyzer error:", e)
                await asyncio.sleep(1)

        # fallback if model fails
        return {
            "intent": "MEDICAL",
            "completeness": "VAGUE",
            "question_to_ask": "Could you describe your symptoms more clearly?",
            "search_term": ""
        }
