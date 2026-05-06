"""
Verified data routes — queries the VERIFIED ChromaDB vector store.

Endpoints:
  POST /verified/generate-quiz
  POST /verified/generate-paper/cambridge
  POST /verified/generate-paper/boards
"""

from fastapi import APIRouter, HTTPException
from models.schemas import (
    VerifiedQuizRequest,
    VerifiedQuizResponse,
    VerifiedPaperRequest,
    VerifiedPaperResponse,
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
    return ShortQuestion(
        id=raw.get("id", idx + 1),
        question=str(raw.get("question", "")),
    )


def _parse_long(raw: dict, idx: int) -> LongQuestion:
    return LongQuestion(
        id=raw.get("id", idx + 1),
        question=str(raw.get("question", "")),
    )


def _build_filter(class_name: str = None, subject: str = None) -> dict | None:
    """Build a ChromaDB $and/$eq where filter from optional fields."""
    conditions = []
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
# POST /verified/generate-quiz
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/generate-quiz", response_model=VerifiedQuizResponse)
async def generate_quiz(req: VerifiedQuizRequest):
    """
    Generate MCQs (with answers) from the verified vector store.
    Body: { "query": "photosynthesis" }
    """
    # 1. Semantic retrieval
    chunks = vector_store.query_verified(query=req.query, n_results=20)
    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No verified data found. Please seed the verified vector store first.",
        )

    # 2. AI generation
    raw_mcqs: List[dict] = ai_service.generate_quiz(req.query, chunks)

    # 3. Parse & validate
    try:
        mcqs = [_parse_mcq(m, i) for i, m in enumerate(raw_mcqs)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response: {e}")

    return VerifiedQuizResponse(mcqs=mcqs)


# ═══════════════════════════════════════════════════════════════════════════════
# POST /verified/generate-paper/cambridge
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/generate-paper/cambridge", response_model=VerifiedPaperResponse)
async def generate_paper_cambridge(req: VerifiedPaperRequest):
    """
    Generate a Cambridge-style exam paper from the verified vector store.
    Body: { "class": "O Level", "subject": "Biology", "mcqs": 10,
            "short_questions": 5, "long_questions": 3, "query": "difficult, famous" }
    """
    where = _build_filter(req.class_name, req.subject)
    chunks = vector_store.query_verified(
        query=f"{req.query} {req.subject} {req.class_name}",
        n_results=30,
        where=where,
    )

    # Fallback: search without strict filter if insufficient results
    if len(chunks) < 5:
        chunks = vector_store.query_verified(
            query=f"{req.query} {req.subject}",
            n_results=30,
        )

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No verified data found for the given subject/class.",
        )

    raw = ai_service.generate_paper_sections(
        query=req.query,
        retrieved_chunks=chunks,
        num_mcqs=req.mcqs,
        num_short=req.short_questions,
        num_long=req.long_questions,
        paper_style="cambridge",
    )

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
    Generate a Pakistani Boards-style exam paper from the verified vector store.
    Body: { "class": "Class 10", "subject": "Biology", "mcqs": 10,
            "short_questions": 5, "long_questions": 3, "query": "easy, famous" }
    """
    where = _build_filter(req.class_name, req.subject)
    chunks = vector_store.query_verified(
        query=f"{req.query} {req.subject} {req.class_name}",
        n_results=30,
        where=where,
    )

    if len(chunks) < 5:
        chunks = vector_store.query_verified(
            query=f"{req.query} {req.subject}",
            n_results=30,
        )

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No verified data found for the given subject/class.",
        )

    raw = ai_service.generate_paper_sections(
        query=req.query,
        retrieved_chunks=chunks,
        num_mcqs=req.mcqs,
        num_short=req.short_questions,
        num_long=req.long_questions,
        paper_style="boards",
    )

    return VerifiedPaperResponse(
        mcqs=[_parse_mcq(m, i) for i, m in enumerate(raw.get("mcqs", []))],
        short_questions=[_parse_short(q, i) for i, q in enumerate(raw.get("short_questions", []))],
        long_questions=[_parse_long(q, i) for i, q in enumerate(raw.get("long_questions", []))],
    )
