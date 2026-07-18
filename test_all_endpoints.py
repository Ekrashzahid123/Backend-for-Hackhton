import requests
import json
import io
import sys

# Ensure stdout uses UTF-8 to prevent encoding crashes on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_url = "http://localhost:7860"

def test_get(endpoint):
    url = f"{base_url}{endpoint}"
    print(f"\n[GET] Testing {url} ...")
    try:
        res = requests.get(url, timeout=30)
        print(f"Status Code: {res.status_code}")
        print("Response:")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False)[:1000])
    except Exception as e:
        print(f"Error: {e}")

def test_post(endpoint, data):
    url = f"{base_url}{endpoint}"
    print(f"\n[POST] Testing {url} with data: {data} ...")
    try:
        res = requests.post(url, json=data, timeout=30)
        print(f"Status Code: {res.status_code}")
        print("Response:")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False)[:2000])
    except Exception as e:
        print(f"Error: {e}")

def test_upload(endpoint, file_content, filename, extra_fields):
    url = f"{base_url}{endpoint}"
    print(f"\n[UPLOAD] Testing {url} with file: {filename} ...")
    try:
        files = {
            "file": (filename, io.BytesIO(file_content.encode("utf-8")), "text/plain")
        }
        res = requests.post(url, files=files, data=extra_fields, timeout=30)
        print(f"Status Code: {res.status_code}")
        print("Response:")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== STARTING DUAL VECTOR DB RAG SYSTEM TEST ===")
    
    # 1. Health check
    test_get("/")
    
    # 2. Get verified hierarchy
    test_get("/verified/papers")
    
    # 3. Generate quiz from verified store (O Level Physics)
    test_post("/verified/generate-quiz", {
        "query": "motion and force",
        "country": "Pakistan",
        "category": "Cambridge",
        "class": "O Level",
        "subject": "Physics",
        "number_of_mcqs": 5,
        "preference": "Mixed"
    })

    # 4. Generate paper (Cambridge style O Level Chemistry)
    test_post("/verified/generate-paper/cambridge", {
        "class": "O Level",
        "subject": "Chemistry",
        "mcqs": 3,
        "short_questions": 2,
        "long_questions": 1,
        "query": "bonding and molecular mass",
        "country": "Pakistan",
        "category": "Cambridge",
        "preference": "Medium"
    })

    # 5. Generate paper (Boards style Class 10 Physics)
    test_post("/verified/generate-paper/boards", {
        "class": "Class 10",
        "subject": "Physics",
        "mcqs": 4,
        "short_questions": 3,
        "long_questions": 1,
        "query": "electricity, current and Ohm's law",
        "country": "Pakistan",
        "category": "Punjab Boards",
        "preference": "Easy"
    })

    # 6. Upload community paper
    # Valid paper
    valid_paper = """
    PHYSICS EXAMINATION PAPER
    CLASS 10 - SECTION A
    Q1. The unit of electrical energy is: A) Joule B) Watt C) Kilowatt-hour D) Volt
    Q2. State Ohm's Law and describe its verification experiment.
    Q3. Explain how a transformer works. What are step-up and step-down transformers?
    """
    test_upload("/unverified/upload-paper", valid_paper, "physics_class10.txt", {
        "country": "Pakistan",
        "class": "Class 10",
        "subject": "Physics",
        "category": "Punjab Boards"
    })

    # Reject paper (abusive/slang/not exam paper)
    invalid_paper = "Hey check this cool song lyrics I wrote yesterday, it is awesome and crazy!"
    test_upload("/unverified/upload-paper", invalid_paper, "song.txt", {
        "country": "Pakistan",
        "class": "Class 10",
        "subject": "Physics",
        "category": "Punjab Boards"
    })

    # 7. Get unverified classes hierarchy
    test_get("/unverified/classes")

    # 8. Generate paper from unverified store
    test_post("/unverified/generate-paper", {
        "country": "Pakistan",
        "class": "Class 9",
        "subject": "Chemistry",
        "mcqs": 2,
        "short_questions": 2,
        "long_questions": 1,
        "query": "moles and physical change"
    })
    
    print("\n=== SYSTEM TEST COMPLETED ===")
