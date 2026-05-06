"""
Unverified data routes — upload, browse, and generate from community papers.

Endpoints:
  POST /unverified/upload-paper
  GET  /unverified/classes
  POST /unverified/generate-paper
"""

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
import hashlib
from typing import List

router = APIRouter(prefix="/unverified", tags=["unverified"])

# Allowed file types
_ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}


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


def _build_filter(country: str = None, class_name: str = None, subject: str = None) -> dict | None:
    """Build ChromaDB where filter."""
    conditions = []
    if country:
        conditions.append({"country": {"$eq": country}})
    if class_name:
        conditions.append({"class_name": {"$eq": class_name}})
    if subject:
        conditions.append({"subject": {"$eq": subject}})
    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def _questions_to_docs(
    short_qs: list,
    long_qs: list,
    mcqs: list,
    country: str,
    class_name: str,
    subject: str,
) -> tuple[List[str], List[dict]]:
    """Convert extracted question lists into (documents, metadatas) for ChromaDB."""
    docs, metas = [], []
    base_meta = {"country": country, "class_name": class_name, "subject": subject}

    for q in mcqs:
        text = q if isinstance(q, str) else q.get("text", "")
        if text.strip():
            docs.append(text)
            metas.append({**base_meta, "question_type": "mcq"})

    for q in short_qs:
        text = q if isinstance(q, str) else q.get("text", "")
        if text.strip():
            docs.append(text)
            metas.append({**base_meta, "question_type": "short"})

    for q in long_qs:
        text = q if isinstance(q, str) else q.get("text", "")
        if text.strip():
            docs.append(text)
            metas.append({**base_meta, "question_type": "long"})

    return docs, metas


# ═══════════════════════════════════════════════════════════════════════════════
# POST /unverified/upload-paper
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/upload-paper", response_model=UnverifiedUploadResponse)
async def upload_paper(
    file: UploadFile = File(...),
    country: str = Form(...),
    class_name: str = Form(..., alias="class"),
    subject: str = Form(...),
):
    """
    Upload a community exam paper (PDF / DOCX / TXT).
    Validates content with AI, scores uniqueness (0.00–2.00), stores in unverified vector store.

    Form fields:
      - file:    the document
      - class:   e.g. "O Level"
      - subject: e.g. "Business"
      - country: e.g. "Pakistan"
    """
    # ── 1. Extension check ─────────────────────────────────────────────────────
    filename = file.filename or ""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in _ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: PDF, DOCX, DOC, TXT.",
        )

    # ── 2. Read & extract text ────────────────────────────────────────────────
    file_bytes = await file.read()
    raw_text = extract_text(file_bytes, filename)

    if not raw_text.strip():
        return UnverifiedUploadResponse(
            accepted=False,
            score=0.00,
            reason="Could not extract any text from the uploaded file.",
        )

    cleaned = clean_text(raw_text)

    # ── 3. AI validation ──────────────────────────────────────────────────────
    validation = ai_service.validate_paper(cleaned, country, class_name, subject)
    if not validation["valid"]:
        return UnverifiedUploadResponse(
            accepted=False,
            score=0.00,
            reason=validation["reason"],
        )

    # ── 4. Normalize country / class / subject (AI dedup) ────────────────────
    existing = vector_store.get_existing_field_values()
    norm_country = ai_service.normalize_field(country, existing["countries"], "country")
    norm_class   = ai_service.normalize_field(class_name, existing["classes"], "class/level")
    norm_subject = ai_service.normalize_field(subject, existing["subjects"], "subject")

    # ── 5. Extract questions ──────────────────────────────────────────────────
    short_qs, long_qs, mcqs = extract_questions(cleaned)
    total_questions = len(short_qs) + len(long_qs) + len(mcqs)

    if total_questions == 0:
        return UnverifiedUploadResponse(
            accepted=False,
            score=0.00,
            reason="No recognisable questions could be extracted from this document.",
        )

    # ── 6. Build ChromaDB documents ───────────────────────────────────────────
    docs, metas = _questions_to_docs(
        short_qs, long_qs, mcqs, norm_country, norm_class, norm_subject
    )

    # ── 7. Compute similarity / uniqueness score ──────────────────────────────
    score = vector_store.compute_similarity_score(docs)

    # ── 8. Deduplicate via hash before storing ───────────────────────────────
    doc_hash = hashlib.sha256(cleaned.encode("utf-8")).hexdigest()
    ids = [f"{doc_hash}_{i}" for i in range(len(docs))]

    # ── 9. Store in vector DB ─────────────────────────────────────────────────
    vector_store.add_to_unverified(docs, metas, ids)

    # ── 10. Save metadata to JSON catalogue ──────────────────────────────────
    vector_store.save_unverified_paper_meta(norm_country, norm_class, norm_subject, score)

    return UnverifiedUploadResponse(accepted=True, score=score, reason="")


# ═══════════════════════════════════════════════════════════════════════════════
# GET /unverified/classes
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/classes", response_model=UnverifiedClassesResponse)
async def get_classes():
    """
    Returns all uploaded papers' countries, classes, and subjects.
    Used by frontend to populate filter dropdowns.
    """
    raw = vector_store.get_all_unverified_classes()
    entries = [
        ClassEntry(country=r["country"], class_name=r["class_name"], subjects=r["subjects"])
        for r in raw
    ]
    return UnverifiedClassesResponse(classes=entries)


# ═══════════════════════════════════════════════════════════════════════════════
# POST /unverified/generate-paper
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/generate-paper", response_model=UnverifiedPaperResponse)
async def generate_paper(req: UnverifiedPaperRequest):
    """
    Generate an exam paper from the unverified (community) vector store.
    Body: {
      "country": "Pakistan", "class": "O Level", "subject": "Business",
      "mcqs": 10, "short_questions": 5, "long_questions": 3,
      "query": "famous, easy"
    }
    """
    where = _build_filter(req.country, req.class_name, req.subject)

    chunks = vector_store.query_unverified(
        query=f"{req.query} {req.subject} {req.class_name}",
        n_results=30,
        where=where,
    )

    # Fallback: relax filters if not enough results
    if len(chunks) < 5 and where:
        subject_filter = {"subject": {"$eq": req.subject}} if req.subject else None
        chunks = vector_store.query_unverified(
            query=f"{req.query} {req.subject}",
            n_results=30,
            where=subject_filter,
        )

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No unverified data found for country='{req.country}', "
                f"class='{req.class_name}', subject='{req.subject}'. "
                "Please upload papers first."
            ),
        )

    raw = ai_service.generate_paper_sections(
        query=req.query,
        retrieved_chunks=chunks,
        num_mcqs=req.mcqs,
        num_short=req.short_questions,
        num_long=req.long_questions,
        paper_style="general",
    )

    return UnverifiedPaperResponse(
        mcqs=[_parse_mcq(m, i) for i, m in enumerate(raw.get("mcqs", []))],
        short_questions=[_parse_short(q, i) for i, q in enumerate(raw.get("short_questions", []))],
        long_questions=[_parse_long(q, i) for i, q in enumerate(raw.get("long_questions", []))],
    )
