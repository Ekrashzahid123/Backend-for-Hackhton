import re
import hashlib
from langdetect import detect

def clean_text(text: str) -> str:
    """Removes noise, extra spaces while preserving necessary structural newlines."""
    # Remove unwanted special characters, but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\?\:\;\(\)\-]', '', text)
    # Collapse multiple spaces into one
    text = re.sub(r' +', ' ', text)
    return text.strip()

def detect_language(text: str) -> str:
    """Detects the language of the text. Defaults to English."""
    try:
        if not text.strip():
            return "en"
        return detect(text)
    except:
        return "en"

def generate_hash(text: str) -> str:
    """Generates a SHA-256 hash for duplicate detection."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def extract_metadata(text: str):
    """
    Extracts basic metadata such as country, subject, and exam type
    using heuristic keyword matching on the beginning of the text.
    """
    country = "Unknown"
    subject = "General"
    exam_type = "Unknown"
    
    # Analyze the first 30 lines for headers
    lines = text.split('\n')[:30]
    header = " ".join(lines).lower()
    
    if "mid" in header or "midterm" in header:
        exam_type = "Mid Term"
    elif "final" in header:
        exam_type = "Final Term"
    elif "board" in header:
        exam_type = "Board Exam"
        
    subjects = ["biology", "chemistry", "physics", "math", "mathematics", "english", "history", "computer", "science"]
    for sub in subjects:
        if sub in header:
            subject = sub.capitalize()
            if subject == "Mathematics":
                subject = "Math"
            break
            
    countries = ["usa", "uk", "pakistan", "india", "canada", "australia"]
    for c in countries:
        if c in header:
            country = c.capitalize()
            break

    return country, subject, exam_type

def extract_questions(text: str):
    """
    Extracts MCQs, Short Questions, and Long Questions using heuristic regex and NLP rules.
    """
    short_questions = []
    long_questions = []
    mcqs = []
    
    lines = text.split('\n')
    current_q = ""
    
    # Common pattern for questions: Q1, 1., 1), a)
    q_pattern = re.compile(r'^((Q|Question)?\s*\d+[\.\)]|[a-d]\))\s+(.*)', re.IGNORECASE)
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        match = q_pattern.match(line)
        if match:
            if current_q:
                _classify_and_append(current_q, short_questions, long_questions, mcqs)
            current_q = line
        else:
            if current_q:
                current_q += " " + line
                
    if current_q:
         _classify_and_append(current_q, short_questions, long_questions, mcqs)
         
    return short_questions, long_questions, mcqs

def _classify_and_append(q_text: str, short_q: list, long_q: list, mcqs: list):
    q_lower = q_text.lower()
    
    # Heuristics for MCQ: presence of options like (a), (b), (c)
    if ("(a)" in q_lower and "(b)" in q_lower) or ("a)" in q_lower and "b)" in q_lower):
        mcqs.append(q_text)
    # Heuristics for Long questions
    elif "explain" in q_lower or "describe" in q_lower or "detail" in q_lower or len(q_text.split()) > 25:
        long_q.append(q_text)
    # Otherwise short question
    else:
        short_q.append(q_text)
