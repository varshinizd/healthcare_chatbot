import google.generativeai as genai
import json
import os
from pydantic import BaseModel, Field

class QueryAnalysis(BaseModel):
    intent: str = Field(..., description="The intent of the user query. Can be 'MEDICAL', 'NON_MEDICAL', or 'GREETING'.")
    completeness: str = Field(..., description="For MEDICAL intent, whether the information is 'VAGUE' (needs more details) or 'SPECIFIC' (ready for analysis). For others, use 'N/A'.")
    question_to_ask: str = Field(..., description="If intent is MEDICAL and completeness is VAGUE, provide ONE clarifying question. Otherwise empty.")
    search_term: str = Field(..., description="If intent is MEDICAL and completeness is SPECIFIC, provide a natural language search question (e.g. 'What are the causes of...'). Otherwise empty.")

class QueryAnalyzer:

    def __init__(self):
        self.system_prompt = """
        You are an expert clinical triage AI. Your goal is to gather sufficient information to form a reasonable differential diagnosis.
        
        Output JSON with these fields:
        - intent: "MEDICAL", "NON_MEDICAL", "GREETING".
        - completeness: "VAGUE" or "SPECIFIC".
        - question_to_ask: clarifying question if VAGUE.
        - search_term: natural language search query if SPECIFIC.

        CRITERIA FOR COMPLETENESS:
        - Mark as "VAGUE" if the current information is insufficient to rule in/out common serious causes.
        - Mark as "SPECIFIC" ONLY when you have a clear clinical picture (Diagnostic Level Context).
        
        INSTRUCTIONS:
        1. Dynamic Reasoning: Do NOT rely on a fixed checklist.
        2. Efficiency (MAX 4 TURNS)
        3. Persistence: Continue marking as VAGUE until enough context.
        """

    async def analyze(self, user_message: str, history: list) -> dict:
        turn_count = (len(history) // 2) + 1
        prompt = f"Current Conversation Turn: {turn_count}/4\nChat History: {history}\n\nLast User Message: {user_message}"
        try:
            response = self.model.generate_content([self.system_prompt, prompt])
            return json.loads(response.text)
        except Exception as e:
            print(f"Analyzer Error: {e}")
            return {
                "intent": "MEDICAL",
                "completeness": "VAGUE",
                "question_to_ask": "Could you describe your symptoms in more detail?",
                "search_term": ""
            }
