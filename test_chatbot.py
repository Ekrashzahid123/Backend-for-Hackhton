import requests
import json

base_url = "http://localhost:7860/api/chatbot"

def test_query(msg):
    print(f"\nSending message: '{msg}'")
    try:
        res = requests.post(base_url, json={"message": msg}, timeout=30)
        print(f"Status Code: {res.status_code}")
        print("Response:")
        print(json.dumps(res.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== TESTING CHATBOT ENDPOINT ===")
    
    # 1. System query
    test_query("How do I generate an exam paper on this system?")
    
    # 2. Educational query
    test_query("Can you explain Coulomb's Law?")
    
    # 3. Off-topic query
    test_query("Tell me a recipe for baking a chocolate cake.")

    # 4. System Query
    test_query("What is NEXTQ. Who is it designed by?")
