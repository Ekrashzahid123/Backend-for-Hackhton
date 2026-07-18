from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def rank_questions(questions: list) -> list:
    """
    Ranks questions based on their TF-IDF scores to highlight
    frequency of important topics and keyword relevance.
    """
    if not questions:
        return []
    
    # If there's only one question or very few words, TF-IDF might not be super meaningful,
    # but it won't break if we handle it properly.
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(questions)
        
        # Calculate sum of tf-idf scores for each question
        scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
        
        # Combine questions with scores
        ranked = list(zip(questions, scores))
        # Sort descending by score
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        # Return sorted list of questions and their ranking score as dict
        return [{"text": q, "ranking_score": float(s)} for q, s in ranked]
    except Exception as e:
        # Fallback if tfidf fails (e.g. empty or stop words only)
        return [{"text": q, "ranking_score": 1.0} for q in questions]

def calculate_paper_ranking(short_q: list, long_q: list, mcqs: list) -> float:
    """
    Calculates an overall ranking score for the paper based on the 
    quality/complexity of its questions.
    """
    total_score = 0.0
    count = 0
    
    for q_list in [short_q, long_q, mcqs]:
        for q in q_list:
            total_score += q.get("ranking_score", 0.0)
            count += 1
            
    if count == 0:
        return 0.0
        
    return total_score / count
