"""
Verified data routes — queries the VERIFIED ChromaDB vector store.

Endpoints (names/paths unchanged):
  GET  /verified/papers              — metadata hierarchy
  POST /verified/generate-quiz       — select MCQs from verified DB
  POST /verified/generate-paper/cambridge
  POST /verified/generate-paper/boards
"""

from fastapi import APIRouter, HTTPException
from models.schemas import (
    VerifiedQuizRequest,
    VerifiedQuizResponse,
    VerifiedPaperRequest,
    VerifiedPaperResponse,
    VerifiedHierarchyResponse,
    MCQItem,
    MCQOption,
    ShortQuestion,
    LongQuestion,
)
from services import vector_store, ai_service
from typing import List

router = APIRouter(prefix="/verified", tags=["verified"])


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _parse_mcq(raw: dict, idx: int) -> MCQItem:
    """Safely coerce a raw dict from AI into an MCQItem."""
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


# ═══════════════════════════════════════════════════════════════════════════════
# GET /verified/papers  — metadata hierarchy
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/papers", response_model=VerifiedHierarchyResponse)
async def list_verified_papers():
    """
    Returns the full metadata hierarchy from the Verified Vector DB.
    Structure: Country → Categories → Classes → Subjects
    No question content is returned.
    """
    hierarchy = vector_store.get_verified_hierarchy()
    if not hierarchy:
        return VerifiedHierarchyResponse(hierarchy={})
    return VerifiedHierarchyResponse(hierarchy=hierarchy)


# ═══════════════════════════════════════════════════════════════════════════════
# POST /verified/generate-quiz
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/generate-quiz", response_model=VerifiedQuizResponse)
async def generate_quiz(req: VerifiedQuizRequest):
    """
    Generate MCQs (with answers) from the VERIFIED vector store only.

    Flow:
      1. Filter Verified DB by metadata (country, category, class, subject)
      2. Retrieve ALL matching MCQs
      3. Pass ALL MCQs to LLM — select & rank only, never invent
    """
    # Normalize metadata against existing values in DB
    existing = vector_store.get_verified_field_values()
    norm_country = ai_service.normalize_field(req.country, existing["countries"], "country") if req.country else None
    norm_class = ai_service.normalize_field(req.class_name, existing["classes"], "class/level") if req.class_name else None
    norm_subject = ai_service.normalize_field(req.subject, existing["subjects"], "subject") if req.subject else None

    # Step 1 + 2: Metadata-filtered retrieval of all verified MCQs
    questions = vector_store.get_verified_questions_by_type(
        country=norm_country,
        category=req.category,
        class_name=norm_class,
        subject=norm_subject,
    )
    mcqs = questions["mcqs"]

    # Fallback: semantic search if metadata filters yield no results
    if not mcqs:
        fallback_query = f"{req.subject or ''} {req.class_name or ''}".strip() or "exam questions"
        chunks = vector_store.query_verified(query=fallback_query, n_results=50)
        mcqs = [c["text"] for c in chunks
                if c.get("metadata", {}).get("question_type") == "mcq"]
        # If still empty, use all chunks
        if not mcqs:
            mcqs = [c["text"] for c in chunks]

    if not mcqs:
        raise HTTPException(
            status_code=404,
            detail="No verified MCQ data found. Please seed the verified vector store first.",
        )

    # Step 3: LLM selects & ranks — never invents
    n_mcqs = req.number_of_mcqs or 10
    preference = req.preference or "Mixed"

    raw_mcqs: List[dict] = ai_service.generate_quiz_from_questions(
        mcqs=mcqs,
        number_of_mcqs=n_mcqs,
        preference=preference,
    )

    if not raw_mcqs:
        raise HTTPException(status_code=404, detail="No data available for this query.")

    try:
        mcq_items = [_parse_mcq(m, i) for i, m in enumerate(raw_mcqs)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response: {e}")

    return VerifiedQuizResponse(mcqs=mcq_items)


# ═══════════════════════════════════════════════════════════════════════════════
# POST /verified/generate-paper/cambridge
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/generate-paper/cambridge", response_model=VerifiedPaperResponse)
async def generate_paper_cambridge(req: VerifiedPaperRequest):
    """
    Generate a Cambridge-style exam paper from the VERIFIED vector store.

    Flow:
      1. Filter Verified DB by metadata (country, category, class, subject)
      2. Retrieve ALL matching MCQs / Short / Long questions separately
      3. Pass ALL to LLM — select & rank only, never invent
    """
    # Normalize metadata against existing values in DB
    existing = vector_store.get_verified_field_values()
    norm_country = ai_service.normalize_field(req.country, existing["countries"], "country") if req.country else None
    norm_class = ai_service.normalize_field(req.class_name, existing["classes"], "class/level") if req.class_name else None
    norm_subject = ai_service.normalize_field(req.subject, existing["subjects"], "subject") if req.subject else None

    # Step 1 + 2: Metadata-filtered retrieval
    questions = vector_store.get_verified_questions_by_type(
        country=norm_country,
        category=req.category or "Cambridge",
        class_name=norm_class,
        subject=norm_subject,
    )

    # Fallback: semantic search when metadata yields nothing
    if not any(questions.values()):
        chunks = vector_store.query_verified(
            query=f"{req.subject} {req.class_name}",
            n_results=50,
            where={"class_name": {"$eq": req.class_name}} if req.class_name else None,
        )
        for c in chunks:
            qt = c.get("metadata", {}).get("question_type", "")
            text = c["text"]
            if qt == "mcq":
                questions["mcqs"].append(text)
            elif qt == "short":
                questions["short"].append(text)
            elif qt == "long":
                questions["long"].append(text)
            else:
                questions["mcqs"].append(text)  # default

    if not any(questions.values()):
        raise HTTPException(
            status_code=404,
            detail="No verified data found for the given subject/class.",
        )

    # Step 3: LLM selects & ranks — Cambridge style
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

    return VerifiedPaperResponse(
        mcqs=[_parse_mcq(m, i) for i, m in enumerate(raw.get("mcqs", []))],
        short_questions=[_parse_short(q, i) for i, q in enumerate(raw.get("short_questions", []))],
        long_questions=[_parse_long(q, i) for i, q in enumerate(raw.get("long_questions", []))],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# POST /verified/generate-paper/boards
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/generate-paper/boards", response_model=VerifiedPaperResponse)
async def generate_paper_boards(req: VerifiedPaperRequest):
    """
    Generate a Pakistani Boards-style exam paper from the VERIFIED vector store.

    Flow:
      1. Filter Verified DB by metadata (country, category, class, subject)
      2. Retrieve ALL matching MCQs / Short / Long questions separately
      3. Pass ALL to LLM — select & rank only, never invent
    """
    # Normalize metadata against existing values in DB
    existing = vector_store.get_verified_field_values()
    norm_country = ai_service.normalize_field(req.country or "Pakistan", existing["countries"], "country")
    norm_class = ai_service.normalize_field(req.class_name, existing["classes"], "class/level") if req.class_name else None
    norm_subject = ai_service.normalize_field(req.subject, existing["subjects"], "subject") if req.subject else None

    # Step 1 + 2: Metadata-filtered retrieval
    questions = vector_store.get_verified_questions_by_type(
        country=norm_country,
        category=req.category,
        class_name=norm_class,
        subject=norm_subject,
    )

    # Fallback: semantic search when metadata yields nothing
    if not any(questions.values()):
        chunks = vector_store.query_verified(
            query=f"{req.subject} {req.class_name}",
            n_results=50,
            where={"class_name": {"$eq": req.class_name}} if req.class_name else None,
        )
        for c in chunks:
            qt = c.get("metadata", {}).get("question_type", "")
            text = c["text"]
            if qt == "mcq":
                questions["mcqs"].append(text)
            elif qt == "short":
                questions["short"].append(text)
            elif qt == "long":
                questions["long"].append(text)
            else:
                questions["short"].append(text)  # default

    if not any(questions.values()):
        raise HTTPException(
            status_code=404,
            detail="No verified data found for the given subject/class.",
        )

    # Step 3: LLM selects & ranks — Boards style
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

    return VerifiedPaperResponse(
        mcqs=[_parse_mcq(m, i) for i, m in enumerate(raw.get("mcqs", []))],
        short_questions=[_parse_short(q, i) for i, q in enumerate(raw.get("short_questions", []))],
        long_questions=[_parse_long(q, i) for i, q in enumerate(raw.get("long_questions", []))],
    )
