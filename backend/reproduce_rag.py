from googlesearch import search
import json

def test_search():
    print("Testing Google Search (googlesearch-python)...")
    try:
        # advanced=True returns objects with title, url, description
        results = list(search("symptoms of flu", num_results=3, advanced=True))
        print(f"Results found: {len(results)}")
        for res in results:
            print(f"Title: {res.title}")
            print(f"URL: {res.url}")
            print(f"Desc: {res.description}")
            print("-" * 20)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
