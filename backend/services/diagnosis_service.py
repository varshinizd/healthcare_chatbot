import os
import json
import asyncio
from google import genai
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ----------------
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY missing")

client = genai.Client(api_key=API_KEY)


# =====================================================
# DIAGNOSIS SERVICE
# =====================================================
class DiagnosisService:
    def __init__(self, rag_engine):
        self.rag_engine = rag_engine

    # -------------------------------------------------
    # Generate Clarifying Questions
    # -------------------------------------------------
    async def generate_clarifying_questions(
        self,
        diseases: list,
        initial_symptoms: str
    ) -> list:
        """
        Generate up to 4 clarifying questions to distinguish
        between candidate diseases.
        """

        # -------- Build RAG context safely --------
        context = ""

        for disease in diseases:
            disease_info = self.rag_engine.search(disease, top_k=1)

            # ⭐ Only include valid RAG results
            if disease_info:
                context += f"--- {disease} ---\n{disease_info}\n\n"

        # ⭐ If RAG has no useful data
        if not context.strip():
            context = (
                "No structured medical database context available. "
                "Use general medical knowledge."
            )

        prompt = f"""
You are a clinical diagnostic expert.

Based on the candidate diseases and descriptions below,
generate EXACTLY 4 targeted clarifying questions.

The questions must help distinguish which disease is most likely.

Initial Symptoms:
{initial_symptoms}

Candidate Diseases Context:
{context}

Return ONLY a JSON list of 4 strings.

Example:
["Question 1", "Question 2", "Question 3", "Question 4"]
"""

        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )

            text = response.text.strip()

            # ---------------- SAFE JSON EXTRACTION ----------------
            if "```" in text:
                parts = text.split("```")
                if len(parts) >= 3:
                    text = parts[-2].strip()

            start = text.find("[")
            end = text.rfind("]") + 1
            text = text[start:end]

            questions = json.loads(text)

            # ---------------- CLEAN QUESTIONS ----------------
            cleaned_questions = [
                q.strip().lstrip("1234. ").strip()
                for q in questions
            ]

            return cleaned_questions[:4]

        except Exception as e:
            print(f"Error generating clarifying questions: {e}")

            # Safe fallback questions
            return [
                "Can you describe your symptoms in more detail?",
                "When did this start?",
                "Is there anything that makes it better or worse?",
                "Are you experiencing any other symptoms?"
            ]

    # -------------------------------------------------
    # Final Diagnosis Generation
    # -------------------------------------------------
    async def get_final_diagnosis(
        self,
        diseases: list,
        history: list
    ) -> str:
        """
        Finalize assessment using conversation history
        and candidate diseases.
        """

        # -------- Format conversation history --------
        history_text = ""
        for msg in history:
            role = msg.get("role", "user")
            content = msg.get("parts", [""])[0]
            history_text += f"{role}: {content}\n"

        # -------- Build RAG context safely --------
        context = ""

        for disease in diseases:
            disease_info = self.rag_engine.search(disease, top_k=1)

            if disease_info:
                context += f"--- {disease} ---\n{disease_info}\n\n"

        # ⭐ Independent reasoning fallback
        if not context.strip():
            context = (
                "No structured medical database context available. "
                "Use general medical knowledge."
            )

        prompt = f"""
You are an expert doctor.

Based on the conversation history and candidate diseases,
provide a professional assessment.

Explain WHY a disease may be more likely.

RULES:
- Do NOT ask more questions.
- Provide educational guidance only.
- Include a clear medical disclaimer.

Conversation History:
{history_text}

Candidate Diseases Context:
{context}

Provide a detailed, empathetic response.
"""

        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )

            return response.text.strip()

        except Exception as e:
            print(f"Error finalizing diagnosis: {e}")

            return (
                "Based on your symptoms, it is difficult to be certain. "
                "Please consult a healthcare professional for a formal diagnosis."
            )