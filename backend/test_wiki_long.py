import wikipedia

def test_wiki():
    queries = [
        "symptoms of flu",
        "What are the causes of fever for 3 days with headache?"
    ]
    
    print("Testing Wikipedia Search...")
    for q in queries:
        print(f"\nQuery: '{q}'")
        try:
            results = wikipedia.search(q, results=3)
            print(f"Results: {results}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_wiki()
