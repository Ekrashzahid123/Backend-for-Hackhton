import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from services import vector_store

def seed_unverified_dummy_data():
    print("Seeding unverified vector store with international dummy data...")
    
    dummy_papers = [
        {
            "country": "UK",
            "category": "Board Exam",
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
            "category": "Mid Term",
            "class_name": "Grade 11",
            "subject": "Chemistry",
            "questions": [
                "What is the difference between an ionic and a covalent bond?",
                "Explain the periodic trends in electronegativity.",
                "How do you balance a redox reaction using the half-reaction method?"
            ]
        },
        {
            "country": "India",
            "category": "Board Exam",
            "class_name": "Class 12",
            "subject": "Physics",
            "questions": [
                "State and explain Gauss's Law for electric fields.",
                "Derive the expression for the magnetic force on a current-carrying conductor.",
                "Explain the principle of superposition of waves."
            ]
        }
    ]
    
    for paper in dummy_papers:
        country = paper["country"]
        category = paper["category"]
        class_name = paper["class_name"]
        subject = paper["subject"]
        
        # Add to vector store
        docs = paper["questions"]
        metas = [{
            "country": country,
            "category": category,
            "class_name": class_name,
            "subject": subject,
            "question_type": "general"
        } for _ in docs]
        
        vector_store.add_to_unverified(docs, metas)
        
        # Update metadata JSON
        vector_store.save_unverified_paper_meta(country, class_name, subject, 2.00, category=category)
        
        print(f"Added {len(docs)} questions for {subject} ({class_name}, {country}, {category}).")

    print("Unverified store seeded successfully.")

if __name__ == "__main__":
    seed_unverified_dummy_data()
