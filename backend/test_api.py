import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"

def test_chat():
    print("Testing Chatbot API with Extensions...")
    
    # 1. HIGH RISK TEST
    print("\n1. [HIGH RISK] Testing Emergency Trigger: 'I have severe chest pain'")
    try:
        start_t = time.time()
        response = requests.post(f"{BASE_URL}/chat", json={"message": "I have severe chest pain"})
        duration = time.time() - start_t
        
        data = response.json()
        bot_response = data.get("response", "")
        
        if "EMERGENCY ALERT" in bot_response:
             print("   PASS: Emergency Alert triggered.")
             print(f"   Response Time: {duration:.2f}s (Should be fast, no LLM)")
        else:
             print("   FAIL: Emergency Alert NOT triggered.")
             print(f"   Response: {bot_response[:100]}...")
             
    except Exception as e:
        print(f"   FAIL: {e}")

    # 2. SCOPE TEST (Irrelevant Query)
    print("\n2. [SCOPE] Testing Irrelevant Query: 'Who won the World Cup?'")
    try:
        response = requests.post(f"{BASE_URL}/chat", json={"message": "Who won the World Cup?"})
        data = response.json()
        bot_response = data.get("response", "")
        
        # Router should return the hardcoded refusal string or similar
        if "only help with medical" in bot_response:
             print("   PASS: Router refused irrelevant query.")
        else:
             print("   WARNING: Router might have allowed it.")
        print(f"   Response: {bot_response.strip()}")

    except Exception as e:
        print(f"   FAIL: {e}")

    # 3. INTERACTIVE FLOW TEST (Vague Input)
    print("\n3. [INTERACTIVE] Testing Vague Input: 'I have a fever'")
    try:
        response = requests.post(f"{BASE_URL}/chat", json={"message": "I have a fever"})
        data = response.json()
        bot_response = data.get("response", "")
        
        # Expectation: Single clarifying question from Analyzer
        if "?" in bot_response and len(bot_response.split()) < 30:
             print("   PASS: Bot asked a concise clarifying question.")
             print(f"   Response: {bot_response.strip()}")
        else:
             print("   WARNING: Response might be too long or not a question.")
             print(f"   Response: {bot_response.strip()}")

    except Exception as e:
        print(f"   FAIL: {e}")

    # 4. REPORT TEST (Specific Input)
    print("\n4. [REPORT] Testing Specific Input: 'I have a fever of 102 for 3 days and severe headache'")
    try:
        response = requests.post(f"{BASE_URL}/chat", json={"message": "I have a fever of 102 for 3 days and severe headache"})
        data = response.json()
        bot_response = data.get("response", "")
        
        # Expectation: Full Report with structure (Router -> SPECIFIC -> RAG -> LLM Report)
        if "Preliminary Assessment" in bot_response:
             print("   PASS: Bot generated full report for specific input.")
             
             sources = data.get("sources", [])
             if sources and len(sources) > 0:
                 print(f"   PASS: Sources returned: {len(sources)}")
                 print(f"         First source: {sources[0].get('title', 'No Title')}")
             else:
                 print("   FAIL: No sources returned for specific query.")
        else:
             print("   FAIL: Bot did not generate report for specific input.")
             
    except Exception as e:
        print(f"   FAIL: {e}")
             
    except Exception as e:
        print(f"   FAIL: {e}")

    print("\nVerification Complete.")

if __name__ == "__main__":
    test_chat()
