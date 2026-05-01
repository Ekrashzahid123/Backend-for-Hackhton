import json
from database.database import SessionLocal, engine, Base
from database.models import Paper
import time

def seed_database(json_file="mock_data.json"):
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    print(f"Loading data from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    db = SessionLocal()
    
    print(f"Inserting {len(data)} records into the database. This may take a minute...")
    start_time = time.time()
    
    # Batch insert for performance
    batch_size = 10000
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        papers = []
        for item in batch:
            paper = Paper(
                hash=item["hash"],
                country=item["country"],
                subject=item["subject"],
                exam_type=item["exam_type"],
                language=item["language"],
                short_questions=item["short_questions"],
                long_questions=item["long_questions"],
                mcqs=item["mcqs"],
                raw_text=item["raw_text"],
                ranking_score=item["ranking_score"]
            )
            papers.append(paper)
            
        db.add_all(papers)
        db.commit()
        print(f"Inserted {min(i+batch_size, len(data))} records...")
        
    db.close()
    print(f"Database seeded successfully in {round(time.time() - start_time, 2)}s.")

if __name__ == "__main__":
    seed_database()
