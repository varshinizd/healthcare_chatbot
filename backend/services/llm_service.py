import os
import google.generativeai as genai
from typing import List, AsyncGenerator
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

class LLMService:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.system_instruction = """
You are a knowledgeable and cautious AI healthcare assistant.
Your goal is to help users understand their symptoms.
Always maintain a professional, empathetic tone.

IMPORTANT RESPONSE GUIDELINES:
For every medical query or symptom description, you MUST structure your response into two distinct sections:
1. **Assessment**: Briefly analyze the reported symptoms.
2. **Recommendations**: Provide actionable advice, home care tips, or suggestions for when to see a doctor.

If the user query is non-medical (greeting, general question), you may skip this structure.
"""

    async def generate_response(self, history: List[dict], user_message: str, context: str = "") -> str:
        """
        Generates a response. 
        If 'context' is provided, it assumes we are in REPORT mode and injects specific instructions.
        If 'context' is empty, it acts as a conversational pass-through (or the router handles the question asking).
        """
        
        # Transform history
        formatted_history = []
        for msg in history:
            formatted_history.append({
                "role": msg["role"], 
                "parts": msg["parts"]
            })
            
        chat = self.model.start_chat(history=formatted_history)
        
        if context:
            # REPORT MODE PROMPT
            prompt = f"""
            INSTRUCTIONS: 
            Generate a detailed Preliminary Health Assessment based on the User's symptoms and the provided Web Context.
            
            CONTEXT:
            {context}
            
            USER SYMPTOMS:
            {user_message}
            
            FORMAT:
            - ### Preliminary Assessment
            - ### Potential Causes
            - ### Home Care Guidance
            - ### Warning Signs
            - ### Conclusion
            - **Disclaimer**: (Standard AI Disclaimer)
            """
        else:
            # CONVERSATIONAL PROMPT
            # Enforce structure even for standard queries if they look medical
            prompt = f"""
            User Query: {user_message}
            
            Remember to provide an **Assessment** and **Recommendations** if this is a symptom-related query.
            """
            
        try:
            response = chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I'm having trouble connecting. Error: {str(e)}"


