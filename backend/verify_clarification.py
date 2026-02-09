import asyncio
from services.query_analyzer import QueryAnalyzer

async def test_logic():
    analyzer = QueryAnalyzer()
    
    print("\n--- TEST 1: Vague Symptom ---")
    history = []
    msg = "I have a stomach ache."
    result = await analyzer.analyze(msg, history)
    print(f"User: {msg}")
    print(f"Completeness: {result.get('completeness')}")
    print(f"Question: {result.get('question_to_ask')}")
    
    print("\n--- TEST 2: Attempting to be Specific (but missing details) ---")
    history.append({"role": "user", "parts": [msg]})
    history.append({"role": "model", "parts": [result.get('question_to_ask', '')]})
    msg_2 = "It started yesterday."
    result_2 = await analyzer.analyze(msg_2, history)
    print(f"User: {msg_2}")
    print(f"Completeness: {result_2.get('completeness')}")
    print(f"Question: {result_2.get('question_to_ask')}")

    print("\n--- TEST 3: Specific Symptom ---")
    msg_3 = "Severe sharp stomach pain in lower right side, started 2 hours ago, with vomiting and fever."
    result_3 = await analyzer.analyze(msg_3, [])
    print(f"User: {msg_3}")
    print(f"Completeness: {result_3.get('completeness')}")
    print(f"Search Term: {result_3.get('search_term')}")

if __name__ == "__main__":
    asyncio.run(test_logic())
