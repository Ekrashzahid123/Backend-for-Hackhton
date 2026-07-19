import requests
import io
import json

base_url = "http://localhost:7860"

# 3 duplicate questions (high similarity) and 7 unique questions (custom numerical ones)
paper_content = """
PHYSICS EXAM

Duplicate Questions:
1. The unit of electrical energy is: A) Joule B) Watt C) Kilowatt-hour D) Volt
2. State Ohm's Law and describe its verification experiment.
3. Explain how a transformer works. What are step-up and step-down transformers?

Unique Questions:
4. A wave of frequency 512 Hz travels in a medium with a wavelength of 0.65 meters. Calculate its velocity.
5. Find the force between two charges of 3 microcoulombs and 5 microcoulombs placed 0.15 meters apart in air.
6. If a transformer has 250 turns in the primary coil and 1250 turns in the secondary coil, calculate the secondary voltage if the input is 220 volts.
7. Calculate the energy released in kilowatt-hours when a 150-watt bulb is used for 8 hours daily for 30 days.
8. A sound wave takes 2.4 seconds to travel from a ship to the seabed and back. If the speed of sound in seawater is 1500 m/s, find the depth of the sea.
9. An object of mass 0.75 kg is attached to a spring of spring constant 35 N/m. Find the time period of its simple harmonic motion.
10. A radioactive isotope has a half-life of 15 hours. If the initial mass is 80 grams, how much mass will remain after 45 hours?
"""

def run_test():
    url = f"{base_url}/unverified/upload-paper"
    files = {
        "file": ("physics_test_7.txt", io.BytesIO(paper_content.encode("utf-8")), "text/plain")
    }
    data = {
        "country": "Pakistan",
        "class": "Class 10",
        "subject": "Physics",
        "category": "Punjab Boards"
    }
    
    print("Uploading paper with 3 existing and 7 unique questions...")
    try:
        res = requests.post(url, files=files, data=data, timeout=30)
        print(f"Status Code: {res.status_code}")
        print("Response:")
        print(json.dumps(res.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_test()
