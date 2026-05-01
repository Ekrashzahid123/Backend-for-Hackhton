import json
import random
import hashlib
import time

def generate_mock_data(num_records=100000, output_file="mock_data.json"):
    print(f"Generating {num_records} mock records...")
    
    subjects = ["Biology", "Chemistry", "Physics", "Math", "English", "History", "Computer Science"]
    countries = ["USA", "UK", "Pakistan", "India", "Canada", "Australia"]
    exam_types = ["Mid Term", "Final Term", "Board Exam", "Quiz"]
    
    start_time = time.time()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('[\n')
        
        for i in range(num_records):
            subject = random.choice(subjects)
            country = random.choice(countries)
            exam_type = random.choice(exam_types)
            
            raw_text = f"This is a mock paper for {subject}. Generated for {country} {exam_type} system."
            
            # Create a unique hash
            hash_str = hashlib.sha256(f"{raw_text}_{i}_{time.time()}".encode()).hexdigest()
            
            short_questions = [
                {"text": f"Explain the basic concept of {subject} (Q{i}.1)", "ranking_score": round(random.uniform(0.1, 5.0), 2)},
                {"text": f"What are the main principles of this topic? (Q{i}.2)", "ranking_score": round(random.uniform(0.1, 5.0), 2)}
            ]
            
            long_questions = [
                {"text": f"Describe in detail the historical impact and modern applications of {subject} in {country}. (Q{i}.1)", "ranking_score": round(random.uniform(2.0, 10.0), 2)}
            ]
            
            mcqs = [
                {"text": f"1. Which of the following is related to {subject}? (a) Option A (b) Option B", "ranking_score": round(random.uniform(0.1, 3.0), 2)}
            ]
            
            record = {
                "hash": hash_str,
                "country": country,
                "subject": subject,
                "exam_type": exam_type,
                "language": "en",
                "short_questions": short_questions,
                "long_questions": long_questions,
                "mcqs": mcqs,
                "raw_text": raw_text,
                "ranking_score": round(random.uniform(1.0, 10.0), 2)
            }
            
            # Write JSON string to avoid keeping 100k dicts in memory
            json_str = json.dumps(record)
            f.write(json_str)
            
            if i < num_records - 1:
                f.write(',\n')
            else:
                f.write('\n')
                
            if (i + 1) % 10000 == 0:
                print(f"Generated {i + 1} records...")
                
        f.write(']\n')
        
    print(f"Successfully generated {num_records} records in {output_file} (Took {round(time.time() - start_time, 2)}s).")

if __name__ == "__main__":
    generate_mock_data()
