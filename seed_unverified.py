import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from services import vector_store

def seed_unverified_dummy_data():
    print("Seeding unverified vector store with dummy data...")
    
    dummy_papers = [
        {
            "country": "Pakistan",
            "class_name": "Class 10",
            "subject": "Physics",
            "questions": [
                "What is Newton's second law of motion?",
                "Explain the concept of inertia with an example.",
                "Calculate the force required to accelerate a 5kg mass at 2m/s^2."
            ]
        },
        {
            "country": "UK",
            "class_name": "O Level",
            "subject": "Biology",
            "questions": [
                "Describe the process of photosynthesis in green plants.",
                "What is the role of chlorophyll in capturing light energy?",
                "List the factors that affect the rate of photosynthesis."
            ]
        },
        {
            "country": "USA",
            "class_name": "A Level",
            "subject": "Chemistry",
            "questions": [
                "What is the difference between an ionic and a covalent bond?",
                "Explain the periodic trends in electronegativity.",
                "How do you balance a redox reaction using the half-reaction method?"
            ]
        }
    ]
    
    all_docs = []
    all_metas = []
    
    for paper in dummy_papers:
        country = paper["country"]
        class_name = paper["class_name"]
        subject = paper["subject"]
        
        # Add to vector store
        docs = paper["questions"]
        metas = [{"country": country, "class_name": class_name, "subject": subject, "question_type": "general"} for _ in docs]
        
        vector_store.add_to_unverified(docs, metas)
        
        # Update metadata JSON
        vector_store.save_unverified_paper_meta(country, class_name, subject, 2.00)
        
        print(f"Added {len(docs)} questions for {subject} ({class_name}, {country}).")

    print("Unverified store seeded successfully.")

if __name__ == "__main__":
    seed_unverified_dummy_data()
