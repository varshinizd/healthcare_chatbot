import wikipedia

def test_wiki():
    print("Testing Wikipedia Search...")
    try:
        # Search for a term
        query = "symptoms of flu"
        search_results = wikipedia.search(query, results=3)
        print(f"Search Results: {search_results}")
        
        if search_results:
            # Get page summary of first result
            page = wikipedia.page(search_results[0], auto_suggest=False)
            print(f"Title: {page.title}")
            print(f"URL: {page.url}")
            print(f"Summary: {page.summary[:200]}...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_wiki()
