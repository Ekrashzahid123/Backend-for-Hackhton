"""
Unverified data routes — upload, browse, and generate from community papers.

Endpoints (names/paths unchanged):
  POST /unverified/upload-paper   — validate & store directly in Unverified Vector DB
  GET  /unverified/classes        — metadata hierarchy
  POST /unverified/generate-paper — generate paper from Unverified Vector DB
"""

import hashlib
import datetime
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from models.schemas import (
    UnverifiedUploadResponse,
    UnverifiedClassesResponse,
    ClassEntry,
    UnverifiedPaperRequest,
    UnverifiedPaperResponse,
    MCQItem,
    MCQOption,
    ShortQuestion,
    LongQuestion,
)
from services import vector_store, ai_service
from services.ocr_service import extract_text
from services.nlp_service import clean_text, extract_questions

router = APIRouter(prefix="/unverified", tags=["unverified"])

# Allowed file types
_ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}
# Reject if uniqueness score is below this threshold (out of 5.0)
_UNIQUENESS_THRESHOLD = 1.0


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _parse_mcq(raw: dict, idx: int) -> MCQItem:
    options = [
        MCQOption(id=str(o.get("id", "A")), label=str(o.get("label", "")))
        for o in raw.get("options", [])
    ]
    return MCQItem(
        id=raw.get("id", idx + 1),
        prompt=str(raw.get("prompt", "")),
        options=options,
        answer=str(raw.get("answer", "A")),
    )


def _parse_short(raw: dict, idx: int) -> ShortQuestion:
    return ShortQuestion(id=raw.get("id", idx + 1), question=str(raw.get("question", "")))


def _parse_long(raw: dict, idx: int) -> LongQuestion:
    return LongQuestion(id=raw.get("id", idx + 1), question=str(raw.get("question", "")))


def _build_filter(
    country: str = None,
    category: str = None,
    class_name: str = None,
    subject: str = None,
) -> dict | None:
    """Build ChromaDB where filter."""
    conditions = []
    if country:
        conditions.append({"country": {"$eq": country}})
    if category:
        conditions.append({"category": {"$eq": category}})
    if class_name:
        conditions.append({"class_name": {"$eq": class_name}})
    if subject:
        conditions.append({"subject": {"$eq": subject}})
    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


# ═══════════════════════════════════════════════════════════════════════════════
# POST /unverified/upload-paper
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/upload-paper", response_model=UnverifiedUploadResponse)
async def upload_paper(
    file: UploadFile = File(...),
    country: str = Form(...),
    class_name: str = Form(..., alias="class"),
    subject: str = Form(...),
    category: str = Form("General"),
):
    """
    Upload a community exam paper (PDF / DOCX / TXT).
    Papers are stored DIRECTLY in the Unverified Vector DB — no disk storage.

    Form fields:
      - file:     the document (PDF / DOCX / TXT)
      - class:    e.g. "Class 10"
      - subject:  e.g. "Physics"
      - country:  e.g. "Pakistan"
      - category: e.g. "Punjab Boards" (optional, defaults to "General")

    Processing flow (spec-compliant):
      Step 1: Read file bytes (no disk write)
      Step 2: Extract text via appropriate parser
      Step 3: Validate with LLM — reject if abusive/corrupt/not an exam paper
      Step 4: Extract MCQ / short / long questions (LLM-assisted)
      Step 5: Compute uniqueness score against Unverified Vector DB
      Step 6: Decision — reject if uniqueness < threshold
      Step 7: Store questions directly in Unverified Vector DB with full metadata
    """
    filename = file.filename or "unknown"

    # ── Step 1: Extension check ────────────────────────────────────────────────
    ext = ("." + filename.rsplit(".", 1)[-1].lower()) if "." in filename else ""
    if ext not in _ALLOWED_EXTENSIONS:
        return UnverifiedUploadResponse(
            accepted=False,
            score=0.0,
            reason=f"Unsupported file type '{ext}'. Allowed: PDF, DOCX, TXT.",
            filename=filename,
        )

    # ── Step 2: Extract text ───────────────────────────────────────────────────
    file_bytes = await file.read()
    raw_text = extract_text(file_bytes, filename)

    if not raw_text.strip():
        return UnverifiedUploadResponse(
            accepted=False,
            score=0.0,
            reason="Could not extract any text from the uploaded file. File may be corrupted or image-only without OCR support.",
            filename=filename,
        )

    cleaned = clean_text(raw_text)

    # ── Step 3: AI Validation ─────────────────────────────────────────────────
    validation = ai_service.validate_paper(cleaned, country, class_name, subject)
    if not validation["valid"]:
        return UnverifiedUploadResponse(
            accepted=False,
            score=0.0,
            reason=validation["reason"],
            filename=filename,
        )

    # ── Step 4: Extract questions (LLM-assisted, fallback to heuristic) ───────
    llm_extracted = ai_service.extract_questions_with_llm(cleaned)
    mcqs_text      = llm_extracted.get("mcqs", [])
    short_qs_text  = llm_extracted.get("short_questions", [])
    long_qs_text   = llm_extracted.get("long_questions", [])

    # NLP heuristic fallback if LLM extraction is empty
    if not any([mcqs_text, short_qs_text, long_qs_text]):
        short_qs_text, long_qs_text, mcqs_text = extract_questions(cleaned)

    total_questions = len(mcqs_text) + len(short_qs_text) + len(long_qs_text)
    if total_questions == 0:
        return UnverifiedUploadResponse(
            accepted=False,
            score=0.0,
            reason="No recognisable questions could be extracted from this document.",
            filename=filename,
        )

    # ── Step 5: Normalize metadata & build vectors ────────────────────────────
    existing = vector_store.get_existing_field_values()
    norm_country  = ai_service.normalize_field(country,    existing["countries"], "country")
    norm_class    = ai_service.normalize_field(class_name, existing["classes"],   "class/level")
    norm_subject  = ai_service.normalize_field(subject,    existing["subjects"],  "subject")

    timestamp = datetime.datetime.utcnow().isoformat()
    paper_id  = hashlib.sha256(cleaned.encode("utf-8")).hexdigest()[:16]

    base_meta = {
        "country":    norm_country,
        "category":   category,
        "class_name": norm_class,
        "subject":    norm_subject,
        "paper_type": "unverified",
        "filename":   filename,
        "paper_id":   paper_id,
        "timestamp":  timestamp,
    }

    docs:  List[str]  = []
    metas: List[dict] = []

    for q in mcqs_text:
        t = q if isinstance(q, str) else q.get("text", "")
        if t.strip():
            docs.append(t.strip())
            metas.append({**base_meta, "question_type": "mcq"})

    for q in short_qs_text:
        t = q if isinstance(q, str) else q.get("text", "")
        if t.strip():
            docs.append(t.strip())
            metas.append({**base_meta, "question_type": "short"})

    for q in long_qs_text:
        t = q if isinstance(q, str) else q.get("text", "")
        if t.strip():
            docs.append(t.strip())
            metas.append({**base_meta, "question_type": "long"})

    # ── Step 5: Uniqueness score ───────────────────────────────────────────────
    score = vector_store.compute_similarity_score(docs)

    # ── Step 6: Decision ───────────────────────────────────────────────────────
    if score < _UNIQUENESS_THRESHOLD:
        return UnverifiedUploadResponse(
            accepted=False,
            score=round(score, 2),
            reason=(
                f"Paper is too similar to existing content "
                f"(uniqueness score: {score:.2f}/5). "
                f"Minimum required uniqueness: {_UNIQUENESS_THRESHOLD}/5."
            ),
            filename=filename,
        )

    # ── Step 7: Store directly in Unverified Vector DB ────────────────────────
    ids = [f"{paper_id}_{i}" for i in range(len(docs))]
    vector_store.add_to_unverified(docs, metas, ids)

    # Persist metadata to JSON catalogue for hierarchy browsing
    vector_store.save_unverified_paper_meta(
        country=norm_country,
        class_name=norm_class,
        subject=norm_subject,
        score=score,
        category=category,
        filename=filename,
    )

    return UnverifiedUploadResponse(
        accepted=True,
        score=round(score, 2),
        reason="",
        filename=filename,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# GET /unverified/classes
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/classes", response_model=UnverifiedClassesResponse)
async def get_classes():
    """
    Returns metadata hierarchy from the Unverified Vector DB.
    Country → Category → Class → Subjects (no question content).
    """
    raw = vector_store.get_all_unverified_classes()
    entries = [
        ClassEntry(
            country=r["country"],
            class_name=r["class_name"],
            subjects=r["subjects"],
            category=r.get("category"),
        )
        for r in raw
    ]
    return UnverifiedClassesResponse(classes=entries)


# ═══════════════════════════════════════════════════════════════════════════════
# POST /unverified/generate-paper
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/generate-paper", response_model=UnverifiedPaperResponse)
async def generate_paper(req: UnverifiedPaperRequest):
    """
    Generate an exam paper from the UNVERIFIED (community) vector store.

    Flow:
      1. Filter Unverified DB by metadata (country, category, class, subject)
      2. Retrieve ALL matching MCQs / Short / Long questions
      3. Pass ALL to LLM — select & rank only, never invent
    """
    # Step 1 + 2: Metadata-filtered retrieval
    questions = vector_store.get_unverified_questions_by_type(
        country=req.country,
        category=req.category,
        class_name=req.class_name,
        subject=req.subject,
    )

    # Fallback: relax to semantic search if metadata yields nothing
    if not any(questions.values()):
        where = _build_filter(req.country, req.category, req.class_name, req.subject)
        chunks = vector_store.query_unverified(
            query=f"{req.subject} {req.class_name}",
            n_results=50,
            where=where,
        )
        for c in chunks:
            qt = c.get("metadata", {}).get("question_type", "")
            text = c["text"]
            if qt == "mcq":
                questions["mcqs"].append(text)
            elif qt == "long":
                questions["long"].append(text)
            else:
                questions["short"].append(text)

    if not any(questions.values()):
        raise HTTPException(
            status_code=404,
            detail=(
                f"No unverified data found for country='{req.country}', "
                f"class='{req.class_name}', subject='{req.subject}'."
            ),
        )

    # Step 3: LLM selects & ranks — never invents
    preference = req.preference or "Mixed"
    raw = ai_service.generate_paper_from_questions(
        mcqs=questions["mcqs"],
        short_questions=questions["short"],
        long_questions=questions["long"],
        number_of_mcqs=req.mcqs,
        number_of_short_questions=req.short_questions,
        number_of_long_questions=req.long_questions,
        preference=preference,
    )

    if not raw.get("mcqs") and not raw.get("short_questions") and not raw.get("long_questions"):
        raise HTTPException(status_code=404, detail="No data available for this query.")

    return UnverifiedPaperResponse(
        mcqs=[_parse_mcq(m, i) for i, m in enumerate(raw.get("mcqs", []))],
        short_questions=[_parse_short(q, i) for i, q in enumerate(raw.get("short_questions", []))],
        long_questions=[_parse_long(q, i) for i, q in enumerate(raw.get("long_questions", []))],
    )
