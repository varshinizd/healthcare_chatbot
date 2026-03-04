import asyncio
from services.query_analyzer import QueryAnalyzer


async def test_logic():
    analyzer = QueryAnalyzer()

    # -------------------------------------------------
    # TEST 1 — VAGUE SYMPTOM
    # -------------------------------------------------
    print("\n--- TEST 1: Vague Symptom ---")

    history = []
    msg = "I have a stomach ache."

    result = await analyzer.analyze(msg, history)

    print(f"User: {msg}")
    print(f"Intent: {result.get('intent')}")
    print(f"Completeness: {result.get('completeness')}")
    print("Follow-up Questions:")
    for q in result.get("follow_up_questions", []):
        print("-", q)

    # -------------------------------------------------
    # TEST 2 — FOLLOWUP ANSWER
    # -------------------------------------------------
    print("\n--- TEST 2: Follow-up Response ---")

    history.append(f"user: {msg}")
    history.append(f"model: {result.get('follow_up_questions', [''])[0]}")

    msg_2 = "It started yesterday."

    result_2 = await analyzer.analyze(msg_2, history)

    print(f"User: {msg_2}")
    print(f"Intent: {result_2.get('intent')}")
    print(f"Completeness: {result_2.get('completeness')}")
    print("Follow-up Questions:")
    for q in result_2.get("follow_up_questions", []):
        print("-", q)

    # -------------------------------------------------
    # TEST 3 — SPECIFIC SYMPTOM
    # -------------------------------------------------
    print("\n--- TEST 3: Specific Symptom ---")

    msg_3 = (
        "Severe sharp stomach pain in lower right side, "
        "started 2 hours ago, with vomiting and fever."
    )

    result_3 = await analyzer.analyze(msg_3, [])

    print(f"User: {msg_3}")
    print(f"Intent: {result_3.get('intent')}")
    print(f"Completeness: {result_3.get('completeness')}")
    print(f"Potential Diseases: {result_3.get('potential_diseases')}")
    print(f"Search Term: {result_3.get('search_term')}")


if __name__ == "__main__":
    asyncio.run(test_logic())