# 🎓 Poster Presentation Guide: Intelligent Exam Paper Generator (v2)

This guide provides a clear, high-level, and technical walkthrough of the **Intelligent Exam Paper Generator**. Use this to explain the system's architecture, endpoints, and data flow during your poster presentation.

---

## 🌟 Core Concept: Dual-Store RAG System
At its heart, this is a **Retrieval-Augmented Generation (RAG)** system that uses **two separate databases** to power AI-assisted exam generation:
1. **Verified Store (Curated)**: High-quality, trusted, and structured exam papers (e.g., Cambridge, Federal Board, Punjab Board) pre-loaded by administrators.
2. **Unverified Store (Community)**: Past papers uploaded by teachers and students. These undergo a strict 7-step quality control and uniqueness validation pipeline before being accepted.

### Why RAG?
Standard AI models (like GPT or Gemini) can "hallucinate" (make up incorrect or unrealistic questions). This system uses **ChromaDB (a vector database)** to store real questions. When a user requests an exam paper, the system retrieves *actual* past questions matching the criteria and uses the AI only to select, rank, deduplicate, and format them. **The AI is not allowed to invent new questions.**

---

## 🛠️ System Architecture Diagram

```mermaid
graph TD
    User([User / frontend]) -->|Requests / Uploads| API[FastAPI Server]
    
    subgraph Quality Pipeline (Uploads)
        API -->|Upload Paper| Text[OCR & Text Extraction]
        Text -->|Validate| LLM_Val{AI Valid?}
        LLM_Val -->|No| Reject[Reject Upload]
        LLM_Val -->|Yes| LLM_Ext[Question Extractor]
        LLM_Ext -->|MCQs, Short, Long| Unique{Uniqueness Check}
        Unique -->|< 1 Unique Question| Reject
        Unique -->|>= 1 Unique Question| UnverifiedDB[(ChromaDB: Unverified Collection)]
    end

    subgraph Exam Generation (RAG)
        API -->|Generate Request| Filter[Metadata Filter]
        Filter -->|Retrieve Questions| DBs{Which Store?}
        DBs -->|Verified| VerifiedDB[(ChromaDB: Verified Collection)]
        DBs -->|Unverified| UnverifiedDB
        DBs -->|Fallback| Semantic[Semantic Search]
        
        VerifiedDB -->|Raw Questions| LLM_Gen[AI Selection & Ranking]
        UnverifiedDB -->|Raw Questions| LLM_Gen
        Semantic -->|Raw Questions| LLM_Gen
        LLM_Gen -->|Structured JSON Paper| API
    end
    
    API -->|Deliver Paper| User
```

---

## 🔌 API Endpoints Explained (In Easy Terms)

The API is divided into three primary categories: **Verified**, **Unverified (Community)**, and **Chatbot / Legacy Services**.

### 1. Verified Endpoints (Curated Data)

These endpoints interface directly with the secure, pre-seeded **Verified Database**.

#### 📁 `GET /verified/papers`
* **What it does**: Returns the structure of the verified database (Country $\rightarrow$ Category $\rightarrow$ Class $\rightarrow$ Subject) so the frontend can display dropdown menus.
* **How it works**: It scans the metadata of the verified database and groups items. For example: `Pakistan -> Federal Board -> Class 10 -> Physics`.
* **Poster Tip**: *Mention that this does not return question contents, keeping payload sizes small and secure.*

#### 📝 `POST /verified/generate-quiz`
* **What it does**: Generates a set of multiple-choice questions (MCQs) along with their answers.
* **How it works**: 
  1. Normalizes the user's input (e.g., matching "physics" to "Physics").
  2. Queries the verified database to retrieve all matching MCQs.
  3. Feeds these MCQs to the AI model to filter, deduplicate, and rank them based on user preferences.
  4. Returns the structured quiz.

#### 📄 `POST /verified/generate-paper/boards`
* **What it does**: Generates a complete board-style exam paper containing Section A (MCQs), Section B (Short Questions), and Section C (Long Questions).
* **How it works**: It retrieves all matches for MCQs, Short, and Long questions from the verified database, and uses the AI model to build a cohesive, balanced, and high-quality exam.

---

### 2. Unverified Endpoints (Community-Driven Data)

These endpoints power the community upload, validation, and generation features.

#### 📤 `POST /unverified/upload-paper`
* **What it does**: Allows users to upload past papers (PDF, DOCX, TXT formats) to contribute to the community pool.
* **How it works (The 7-Step Pipeline)**:
  1. **Read-in**: Read file bytes directly in memory (never written to disk to protect security).
  2. **Extraction**: Parse the text from PDF/Word/Text formats.
  3. **AI Validation**: A fast AI check rejects files containing spam, inappropriate language, corrupted characters, or non-educational content.
  4. **AI-Assisted Question Extraction**: Extract specific MCQs, Short, and Long questions.
  5. **Uniqueness Scan**: Compares each extracted question against the entire database. If a question is $\ge 75\%$ similar to an existing one, it is flagged as a duplicate.
  6. **Accept/Reject Decision**: If the document contains less than 1 unique question, the upload is rejected.
  7. **Vector Storage**: Accepted questions are converted into mathematical vectors and stored in the unverified collection with metadata for instant querying.
* **Poster Tip**: *This 7-step pipeline prevents database bloat, filters spam, and stops duplicate uploads.*

#### 📁 `GET /unverified/classes`
* **What it does**: Lists the metadata hierarchy of all successfully uploaded community papers so users can browse what subjects and classes are available in the community store.

#### 📄 `POST /unverified/generate-paper`
* **What it does**: Generates a complete exam paper utilizing the community-uploaded questions.
* **How it works**: Similar to the verified generator, but queries the `unverified_papers` collection. If metadata matching yields nothing, it relaxes and runs a semantic (conceptual) search.

---

### 3. Support & Legacy Endpoints

#### 🤖 `POST /api/chatbot`
* **What it does**: A customer support chatbot that answers educational and platform usage queries.
* **How it works**: It checks user prompts and rejects off-topic queries (e.g., asking for game cheats or programming code unrelated to the exam generator), maintaining a safe and focused educational utility.

#### ⏳ Legacy Endpoints (`/api/upload`, `/api/generate`, `/api/search`)
* **What it does**: Original v1 endpoints that use standard database search rather than the dual-store ChromaDB vector search. They are kept for backward compatibility.

---

## 💡 Key Technical Features to Mention on Your Poster

1. **Granular Vector Storage**: Unlike basic systems that upload a whole PDF as one block, we chunk papers into **individual questions** and store each as a separate vector database entry. This allows the generator to mix-and-match questions from different papers seamlessly.
2. **Cosimilarity Matching (The Uniqueness Score)**: We use cosine distance (mathematical angle between vectors) to check if a new question is conceptually identical to an old one. This ensures our database is populated with unique questions, not 100 copies of the same question with minor spelling changes.
3. **AI Normalization**: Users might search for "Grade 10" or "Class X". Our backend uses AI to normalize user searches against database metadata (e.g., mapping them all to `"Class 10"`), making search incredibly robust and user-friendly.
