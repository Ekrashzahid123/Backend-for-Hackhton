import os
import json
import numpy as np
from chromadb.utils import embedding_functions

# Use the default Chroma embedding function (all-MiniLM-L6-v2)
default_ef = embedding_functions.DefaultEmbeddingFunction()

docs = [
    {
        "title": "System Workflow Overview",
        "text": (
            "The Intelligent Exam Paper Generator is a dual-store RAG system. "
            "It consists of two main database stores: the 'Verified' store (which contains curated, trusted exam question data) "
            "and the 'Unverified' store (which holds community-contributed, user-uploaded exam papers). "
            "Users can upload exam papers, browse the question hierarchy, and generate custom papers or quizzes "
            "from either database store based on their parameters like subject, class, category, and country."
        )
    },
    {
        "title": "Paper Upload and Token/Uniqueness Score Generation",
        "text": (
            "When a user uploads an exam paper (PDF, DOCX, or TXT) via the '/unverified/upload-paper' endpoint, "
            "the system extracts the questions (MCQs, short questions, and long questions). "
            "To calculate the uniqueness score, each question is compared against BOTH the 'verified_papers' and 'unverified_papers' collections in ChromaDB. "
            "The system computes the maximum cosine similarity (1 - distance) for each question. "
            "If the similarity is less than 75% (cosine distance > 0.25), the question is considered unique and gets exactly 1 token. "
            "If similarity is 75% or more, the question has high similarity and gets 0 tokens. "
            "The overall uniqueness score of the paper is scaled from 0 to 10.0 using the formula: "
            "score = (unique_tokens / total_questions) * 10.0. "
            "If the paper has 0 unique questions (unique_tokens < 1), it is considered duplicate and rejected."
        )
    },
    {
        "title": "How to Generate Papers and Quizzes",
        "text": (
            "The system offers multiple endpoints for generating papers and quizzes. "
            "1. '/verified/generate-quiz' generates MCQs from the verified store. "
            "2. '/verified/generate-paper/cambridge' and '/verified/generate-paper/boards' generate structured papers from the verified store. "
            "3. '/unverified/generate-paper' generates papers from the unverified store. "
            "To generate a paper, specify parameters like subject, class, country, category, and desired counts of MCQs, short, and long questions. "
            "The system retrieves matches from the vector database, and the LLM selects and ranks them. The system only uses existing questions and never invents new ones."
        )
    },
    {
        "title": "Customer Assistance and Support Bot",
        "text": (
            "For customer support and query handling, the system exposes a chatbot endpoint at POST '/api/chatbot'. "
            "The chatbot assists customers with queries about generating papers, system workflows, and educational topics. "
            "If a query is unrelated to the system or education, the chatbot declines using the template message: "
            "'I'm sorry, but I can only assist you with queries related to the Intelligent Exam Paper Generator system or educational topics. Please let me know how I can help you with these!'"
        )
    }
]

def generate_and_save():
    print("Generating embeddings for system documentation chunks...")
    texts = [d["text"] for d in docs]
    embeddings = default_ef(texts)
    
    for d, emb in zip(docs, embeddings):
        # Convert to standard Python list of floats for JSON serialization
        d["embedding"] = [float(x) for x in emb]
        
    output_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "system_documentation.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)
        
    print(f"Successfully saved system documentation with embeddings to: {output_path}")

if __name__ == "__main__":
    generate_and_save()
