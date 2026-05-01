---
title: Intelligent Exam Paper Generator
emoji: 📚
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# Intelligent Exam Paper Generator Backend

This is a production-ready FastAPI backend for an intelligent exam paper generator. It processes uploaded PDF exam papers, extracts text via OCR (PyMuPDF/Tesseract), cleans it, identifies metadata and questions, and then ranks the questions to generate a balanced new paper.

## Features
- **Upload & OCR Pipeline**: Supports fast PDF parsing and fallback OCR for images.
- **Duplicate Detection**: Uses SHA-256 hashing to avoid reprocessing identical papers.
- **Question Extraction**: Uses NLP heuristics to split papers into MCQs, Short Questions, and Long Questions.
- **Ranking System**: Ranks questions based on keyword frequency using TF-IDF.
- **Paper Generation**: Generates new exam papers based on requested parameters, keeping content balanced and deduplicated.

## Local Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If you intend to process scanned PDFs, ensure you install `tesseract-ocr` on your host system.*

2. **Run the Server**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 7860 --reload
   ```

## Deployment on Hugging Face Spaces (CI/CD Pipeline)

This repository includes a pre-configured CI/CD mechanism to deploy directly to Hugging Face Spaces.

### Option 1: GitHub Actions (Recommended CI/CD)
The `.github/workflows/huggingface.yml` file contains a GitHub Actions workflow.
1. Create a Space on Hugging Face (choose Docker or Gradio depending on if you add a UI, but Docker is best for pure FastAPI).
2. Go to your GitHub repository settings -> Secrets and variables -> Actions.
3. Add a New repository secret named `HF_TOKEN`. You can generate this token in your Hugging Face account settings (ensure it has Write access).
4. Update the `YOUR_HF_USERNAME/YOUR_SPACE_NAME` string in `.github/workflows/huggingface.yml`.
5. Every time you push to the `main` branch, GitHub Actions will automatically sync your code to Hugging Face Spaces and trigger a rebuild.

### Option 2: Direct Hugging Face Push
You can push directly to Hugging Face via git:
```bash
git remote add space https://huggingface.co/spaces/YOUR_HF_USERNAME/YOUR_SPACE_NAME
git push --force space main
```

## Sample API Requests

### 1. Upload a Paper
```bash
curl -X POST "http://localhost:7860/api/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sample_exam.pdf"
```

### 2. Generate a New Paper
```bash
curl -X POST "http://localhost:7860/api/generate" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
           "subject": "Biology",
           "num_mcqs": 10,
           "num_short": 5,
           "num_long": 2
         }'
```

### 3. Search Database
```bash
curl -X GET "http://localhost:7860/api/search?subject=Biology&country=USA" \
     -H "accept: application/json"
```
