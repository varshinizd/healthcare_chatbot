import requests
import json
import uuid
import time

BASE_URL = "http://localhost:8000"

def chat(message, session_id=None):
    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    return response.json()

def test_full_diagnostic_flow():
    print("Starting Full Diagnostic Flow Test...")
    
    # 1. Initial Symptoms
    # Using specific symptoms that should narrow down to a few diseases (e.g., joint pain, fatigue)
    symptoms = "I have persistent joint pain in my hands and I feel very tired lately."
    print(f"\nUser: {symptoms}")
    
    res = chat(symptoms)
    session_id = res["session_id"]
    print(f"Bot (Q1): {res['response']}")
    
    # 2-5. Answer clarifying questions (Simulating 4 questions)
    answers = [
        "The pain is mostly in my fingers and wrists.",
        "Yes, it's worse in the morning for about an hour.",
        "I've noticed some swelling in the joints.",
        "I haven't had any fever."
    ]
    
    for i, answer in enumerate(answers):
        time.sleep(1)
        print(f"\nUser: {answer}")
        res = chat(answer, session_id)
        print(f"Bot (Q{i+2}): {res['response']}")
        
    # Wait for final diagnosis (the last response after 4 answers should be the final diagnosis)
    print("\n--- Final Response Received ---")

if __name__ == "__main__":
    # Note: Make sure the server is running before executing this
    try:
        test_full_diagnostic_flow()
    except Exception as e:
        print(f"Test failed: {e}")
        print("Make sure the backend is running at http://localhost:8000")
