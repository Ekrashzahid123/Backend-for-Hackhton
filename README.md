---
title: Intelligent Exam Paper Generator
emoji: 📚
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# Intelligent Exam Paper Generator Backend — v2

A production-ready FastAPI backend with **dual ChromaDB vector stores** for intelligent, AI-powered exam paper and quiz generation.

## Architecture

```
Verified Store  ──► curated, trusted exam data (seeded from mock_data.json)
Unverified Store ──► community-uploaded papers (scored 0.00 – 2.00 for uniqueness)

Both stores power semantic retrieval → Google Gemini AI → structured exam output
```

---

## Features

| Feature | Detail |
|---|---|
| **Dual Vector Stores** | Separate ChromaDB collections for verified and unverified data |
| **AI Quiz Generation** | MCQs with answers via Mistral AI |
| **AI Paper Generation** | MCQs + short + long questions (Cambridge & Board styles) |
| **AI Paper Validation** | Slang detection, subject/class relevance check on upload |
| **Uniqueness Scoring** | Cosine-distance score 0.00–2.00 for uploaded papers |
| **Field Normalisation** | AI deduplicates country/class/subject names on upload |
| **Multi-format Upload** | PDF, DOCX, DOC, TXT |
| **Auto Seeding** | Verified store seeded from `mock_data.json` on first startup |

---

## Local Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** For scanned PDF OCR, install Tesseract on your system.
> Windows: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your MISTRAL_API_KEY
```

Get a Mistral API key at: https://console.mistral.ai/api-keys

### 3. Run the Server

```bash
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

On first startup the server automatically seeds the verified ChromaDB collection from `mock_data.json`.

### 4. Interactive API Docs

Open http://localhost:7860/docs

---

## API Reference

### ✅ Verified Endpoints

These endpoints query the **verified (curated)** vector store.

---

#### `POST /verified/generate-quiz`

Generate MCQs with answers from verified exam data.

**Request Body:**
```json
{
  "query": "photosynthesis in plants"
}
```

**Response:**
```json
{
  "mcqs": [
    {
      "id": 1,
      "prompt": "What is the primary pigment used in photosynthesis?",
      "options": [
        {"id": "A", "label": "Chlorophyll"},
        {"id": "B", "label": "Melanin"},
        {"id": "C", "label": "Haemoglobin"},
        {"id": "D", "label": "Carotene"}
      ],
      "answer": "A"
    }
  ]
}
```

---

#### `POST /verified/generate-paper/cambridge`

Generate a Cambridge International Examinations style paper.

**Request Body:**
```json
{
  "class": "O Level",
  "subject": "Biology",
  "mcqs": 10,
  "short_questions": 5,
  "long_questions": 3,
  "query": "difficult, famous past paper questions"
}
```

**Response:**
```json
{
  "mcqs": [ ... ],
  "short_questions": [
    {"id": 1, "question": "Describe the process of osmosis."}
  ],
  "long_questions": [
    {"id": 1, "question": "Explain in detail how the heart pumps blood around the body."}
  ]
}
```

---

#### `POST /verified/generate-paper/boards`

Generate a Pakistani Board examination style paper.

**Request Body:** *(same structure as cambridge)*
```json
{
  "class": "Class 10",
  "subject": "Biology",
  "mcqs": 10,
  "short_questions": 6,
  "long_questions": 2,
  "query": "easy, frequently asked"
}
```

**Response:** *(same structure as cambridge)*

---

### 📤 Unverified Endpoints

These endpoints manage the **community-uploaded** vector store.

---

#### `POST /unverified/upload-paper`

Upload a community exam paper. AI validates content and scores uniqueness.

**Request:** `multipart/form-data`

| Field | Type | Example |
|---|---|---|
| `file` | File | `business_paper.pdf` |
| `country` | string | `Pakistan` |
| `class` | string | `O Level` |
| `subject` | string | `Business` |

**Response — Accepted:**
```json
{
  "accepted": true,
  "score": 1.74,
  "reason": ""
}
```

**Response — Rejected:**
```json
{
  "accepted": false,
  "score": 0.00,
  "reason": "The document contains inappropriate language not suitable for an academic setting."
}
```

**Score meaning (0.00 – 2.00):**
| Score | Meaning |
|---|---|
| `2.00` | Completely unique — first upload of this content |
| `1.50+` | Highly original content |
| `1.00` | Moderately similar to existing uploads |
| `0.50` | Largely similar to existing content |
| `0.00` | Rejected (invalid) or near-duplicate |

---

#### `GET /unverified/classes`

Returns all uploaded papers' countries, classes, and subjects.
Used by frontend to populate dropdown filters.

**Response:**
```json
{
  "classes": [
    {
      "country": "Pakistan",
      "class_name": "O Level",
      "subjects": ["Business", "Chemistry", "Physics"]
    },
    {
      "country": "UK",
      "class_name": "A Level",
      "subjects": ["Mathematics", "Economics"]
    }
  ]
}
```

---

#### `POST /unverified/generate-paper`

Generate an exam paper from community-uploaded data.

**Request Body:**
```json
{
  "country": "Pakistan",
  "class": "O Level",
  "subject": "Business",
  "mcqs": 10,
  "short_questions": 5,
  "long_questions": 3,
  "query": "famous, medium difficulty"
}
```

**Response:**
```json
{
  "mcqs": [ ... ],
  "short_questions": [ ... ],
  "long_questions": [ ... ]
}
```

---

## Sample curl Commands

```bash
# Generate quiz from verified data
curl -X POST "http://localhost:7860/verified/generate-quiz" \
  -H "Content-Type: application/json" \
  -d '{"query": "cell division mitosis"}'

# Generate Cambridge paper
curl -X POST "http://localhost:7860/verified/generate-paper/cambridge" \
  -H "Content-Type: application/json" \
  -d '{"class": "O Level", "subject": "Biology", "mcqs": 10, "short_questions": 5, "long_questions": 3, "query": "difficult"}'

# Upload community paper
curl -X POST "http://localhost:7860/unverified/upload-paper" \
  -F "file=@business_paper.pdf" \
  -F "country=Pakistan" \
  -F "class=O Level" \
  -F "subject=Business"

# Get all uploaded classes
curl "http://localhost:7860/unverified/classes"

# Generate paper from community data
curl -X POST "http://localhost:7860/unverified/generate-paper" \
  -H "Content-Type: application/json" \
  -d '{"country": "Pakistan", "class": "O Level", "subject": "Business", "mcqs": 10, "short_questions": 5, "long_questions": 3, "query": "easy, famous"}'
```

---

## File Structure

```
├── app.py                        # FastAPI entry point (v2)
├── routes/
│   ├── verified.py               # /verified/* endpoints
│   ├── unverified.py             # /unverified/* endpoints
│   ├── upload.py                 # Legacy /api/upload
│   ├── generate.py               # Legacy /api/generate
│   └── search.py                 # Legacy /api/search
├── services/
│   ├── vector_store.py           # ChromaDB collections & helpers
│   ├── ai_service.py             # Google Gemini API calls
│   ├── seed_verified.py          # Auto-seed from mock_data.json
│   ├── ocr_service.py            # PDF / DOCX / TXT extraction
│   ├── nlp_service.py            # Text cleaning & question extraction
│   └── ranking_service.py        # TF-IDF ranking (legacy)
├── models/
│   └── schemas.py                # All Pydantic models
├── database/
│   ├── database.py               # SQLAlchemy setup
│   └── models.py                 # SQLite ORM models (legacy)
├── data/
│   └── unverified_meta.json      # Country/class/subject catalogue
├── chroma_db/                    # ChromaDB persistent storage (auto-created)
├── .env.example                  # Environment variable template
├── Dockerfile
└── requirements.txt
```

---

## Deployment (Hugging Face Spaces)

Set your `MISTRAL_API_KEY` as a **Space Secret** in your Hugging Face Space settings.

The existing `.github/workflows/huggingface.yml` CI/CD pipeline deploys automatically on every push to `main`.
