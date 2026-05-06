import requests
import json

base_url = "http://localhost:7860"

def test_endpoint(method, endpoint, data=None):
    url = f"{base_url}{endpoint}"
    print(f"Testing {method} {url}...")
    try:
        if method == "GET":
            response = requests.get(url, timeout=30)
        else:
            response = requests.post(url, json=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print("Response Content:")
        print(json.dumps(response.json(), indent=2))
        print("-" * 50)
    except Exception as e:
        print(f"Error testing {endpoint}: {e}")
        print("-" * 50)

if __name__ == "__main__":
    # Test Root
    test_endpoint("GET", "/")

    # Test Generate Quiz
    test_endpoint("POST", "/verified/generate-quiz", {"query": "Physics basics"})

    # Test Generate Paper
    test_endpoint("POST", "/verified/generate-paper/cambridge", {
        "class": "O Level",
        "subject": "Physics",
        "mcqs": 5,
        "short_questions": 2,
        "long_questions": 1,
        "query": "motion and force"
    })
