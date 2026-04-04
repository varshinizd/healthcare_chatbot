import json
import re
from typing import Optional
import google.generativeai as genai
from backend.config import settings
from backend.prompts import build_system_prompt, CLASSIFIER_PROMPT

genai.configure(api_key=settings.GEMINI_API_KEY)

_flash_model = genai.GenerativeModel(model_name=settings.GEMINI_FLASH_MODEL)


def _make_pro_model(user=None):
    system_prompt = build_system_prompt(user)
    return genai.GenerativeModel(
        model_name=settings.GEMINI_PRO_MODEL,
        system_instruction=system_prompt,
    )


class GeminiClient:
    async def classify_query(self, query: str) -> dict:
        prompt = CLASSIFIER_PROMPT.format(query=query)
        try:
            response = _flash_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(temperature=0.1, max_output_tokens=100),
            )
            raw = re.sub(r"```json|```", "", response.text.strip()).strip()
            result = json.loads(raw)
            return {
                "is_medical": result.get("is_medical", True),
                "confidence": float(result.get("confidence", 0.5)),
                "category": result.get("category", "unknown"),
            }
        except Exception:
            return {"is_medical": True, "confidence": 0.5, "category": "unknown"}

    async def generate_response(
        self,
        messages: list[dict],
        user=None,
        injected_context: Optional[str] = None,
    ) -> str:
        model = _make_pro_model(user)
        history = []
        for msg in messages[:-1]:
            role = "model" if msg["role"] == "assistant" else msg["role"]
            history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=history)
        user_message = messages[-1]["content"]
        if injected_context:
            user_message = f"{injected_context}\n\nUser: {user_message}"

        response = chat.send_message(
            user_message,
            generation_config=genai.GenerationConfig(temperature=0.4, max_output_tokens=1024),
        )
        return response.text

    def embed_text(self, text: str) -> list[float]:
        result = genai.embed_content(
            model=settings.EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query",
        )
        return result["embedding"]


gemini_client = GeminiClient()
