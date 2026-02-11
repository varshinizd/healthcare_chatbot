import os
import asyncio
from google import genai
from dotenv import load_dotenv
from typing import List

load_dotenv()

# ---------------- CONFIG ----------------
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY missing")

client = genai.Client(api_key=API_KEY)


# ---------------- LLM SERVICE ----------------
class LLMService:
    def __init__(self):
        self.system_instruction = """
You are a professional healthcare AI assistant.

RULES:
- Never give final diagnosis
- Give only educational guidance
- Encourage doctor consultation
- Use calm, empathetic tone

If user describes symptoms → respond in:
Assessment
Recommendations
"""

    async def generate_response(
        self,
        history: List[dict],
        user_message: str,
        context: str = ""
    ) -> str:

        # -------- build history --------
        history_text = ""
        for msg in history:
            role = msg["role"]
            content = msg["parts"][0]
            history_text += f"{role}: {content}\n"

        # -------- report mode (RAG used) --------
        if context:
            print("\n========== 🧠 RAG CONTEXT RECEIVED ==========\n")
            print(context[:1000])  # show first 1000 chars
            print("\n=============================================\n")

            prompt = f"""
SYSTEM:
{self.system_instruction}

REFERENCE CONTEXT FROM MEDICAL DATABASE:
{context}

USER SYMPTOMS:
{user_message}

IMPORTANT:
Use the provided medical context to generate the response.

FORMAT STRICTLY:

### Preliminary Assessment
### Possible Causes
### Home Care
### When to See Doctor
### Disclaimer
"""

        # -------- normal chat (no RAG) --------
        else:
            print("\n⚠️ No RAG context used for this query\n")

            prompt = f"""
SYSTEM:
{self.system_instruction}

CHAT HISTORY:
{history_text}

USER:
{user_message}
"""

        # -------- call gemini safely --------
        for _ in range(2):
            try:
                response = await asyncio.to_thread(
                    client.models.generate_content,
                    model="gemini-2.5-flash-lite",
                    contents=prompt,
                )
                return response.text

            except Exception as e:
                print("Gemini error:", e)
                await asyncio.sleep(1)

        return "Server busy. Try again."


# ---------------- TEST ----------------
if __name__ == "__main__":
    async def test():
        service = LLMService()
        history = []

        result = await service.generate_response(
            history,
            "I have headache and fever since morning",
            context="Test medical context: fever is caused by infection"
        )

        print("\nAI RESPONSE:\n")
        print(result)

    asyncio.run(test())
