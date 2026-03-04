import requests
import uuid
import time

BASE_URL = "http://localhost:8000"


# =====================================================
# HELPER
# =====================================================
def chat(message, session_id=None):
    payload = {"message": message}

    if session_id:
        payload["session_id"] = session_id

    response = requests.post(f"{BASE_URL}/chat", json=payload)

    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code}")

    data = response.json()

    if "response" not in data or "session_id" not in data:
        raise Exception("Invalid API response format")

    return data


def print_bot(text):
    print(f"Bot: {text}\n")


# =====================================================
# TEST 1 — FULL DIAGNOSTIC FLOW
# =====================================================
def test_full_diagnostic_flow():
    print("\n==============================")
    print("TEST 1: FULL DIAGNOSTIC FLOW")
    print("==============================")

    symptoms = "I have persistent joint pain in my hands and feel very tired lately."
    print(f"\nUser: {symptoms}")

    res = chat(symptoms)
    session_id = res["session_id"]

    print_bot(res["response"])

    answers = [
        "The pain is mostly in my fingers and wrists.",
        "Yes, it's worse in the morning for about an hour.",
        "There is swelling in the joints.",
        "No fever."
    ]

    for answer in answers:
        time.sleep(1)

        print(f"User: {answer}")
        res = chat(answer, session_id)
        print_bot(res["response"])

        # stop automatically if diagnosis appears
        if "disclaimer" in res["response"].lower():
            print("✅ Final diagnosis reached.")
            break


# =====================================================
# TEST 2 — TOPIC SHIFT
# =====================================================
def test_topic_shift():
    print("\n==============================")
    print("TEST 2: TOPIC SHIFT RESET")
    print("==============================")

    res = chat("I have acne.")
    session_id = res["session_id"]

    print_bot(res["response"])

    # user suddenly changes disease
    msg = "I have diabetes."
    print(f"User: {msg}")

    res = chat(msg, session_id)
    print_bot(res["response"])

    print("✅ If new questions appear, reset works.")


# =====================================================
# TEST 3 — EMERGENCY OVERRIDE
# =====================================================
def test_emergency_override():
    print("\n==============================")
    print("TEST 3: EMERGENCY DETECTION")
    print("==============================")

    res = chat("I have severe chest pain and can't breathe.")
    session_id = res["session_id"]

    print_bot(res["response"])

    # try chatting again
    print("User: hello?")
    res = chat("hello?", session_id)
    print_bot(res["response"])

    print("✅ Session should remain locked.")


# =====================================================
# MAIN RUNNER
# =====================================================
if __name__ == "__main__":
    try:
        test_full_diagnostic_flow()
        test_topic_shift()
        test_emergency_override()

        print("\n🎉 ALL TESTS COMPLETED")

    except Exception as e:
        print("\n❌ Test failed:", e)
        print("Make sure backend is running at http://localhost:8000")