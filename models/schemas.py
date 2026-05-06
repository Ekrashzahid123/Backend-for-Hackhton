from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ─── Shared types ────────────────────────────────────────────────────────────

class MCQOption(BaseModel):
    id: str           # "A" | "B" | "C" | "D"
    label: str


class MCQItem(BaseModel):
    id: int
    prompt: str
    options: List[MCQOption]
    answer: str       # "A" | "B" | "C" | "D"


class ShortQuestion(BaseModel):
    id: int
    question: str


class LongQuestion(BaseModel):
    id: int
    question: str


class PaperSections(BaseModel):
    mcqs: List[MCQItem]
    short_questions: List[ShortQuestion]
    long_questions: List[LongQuestion]


# ─── Existing schemas (kept intact) ─────────────────────────────────────────

class UploadResponse(BaseModel):
    message: str
    hash: str
    subject: str
    extracted_stats: Dict[str, int]


class GenerateRequest(BaseModel):
    subject: str
    num_mcqs: int = 5
    num_short: int = 5
    num_long: int = 3


class GenerateResponse(BaseModel):
    message: str
    paper: Dict[str, Any]


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]


# ─── Verified endpoints ───────────────────────────────────────────────────────

class VerifiedQuizRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Topic or concept to generate MCQs about")


class VerifiedQuizResponse(BaseModel):
    mcqs: List[MCQItem]


class VerifiedPaperRequest(BaseModel):
    class_name: str = Field(..., alias="class", description="e.g. 'O Level', 'Class 10', 'Grade 11'")
    subject: str
    mcqs: int = Field(10, ge=1, le=50)
    short_questions: int = Field(5, ge=0, le=30)
    long_questions: int = Field(3, ge=0, le=20)
    query: str = Field(..., min_length=3, description="Description of desired difficulty/focus, e.g. 'difficult, famous'")

    model_config = {"populate_by_name": True}


class VerifiedPaperResponse(BaseModel):
    mcqs: List[MCQItem]
    short_questions: List[ShortQuestion]
    long_questions: List[LongQuestion]


# ─── Unverified endpoints ─────────────────────────────────────────────────────

class UnverifiedUploadResponse(BaseModel):
    accepted: bool
    score: float        # 0.00 – 2.00 (or 0.00 if rejected)
    reason: str         # empty string when accepted


class ClassEntry(BaseModel):
    country: str
    class_name: str
    subjects: List[str]


class UnverifiedClassesResponse(BaseModel):
    classes: List[ClassEntry]


class UnverifiedPaperRequest(BaseModel):
    country: str
    class_name: str = Field(..., alias="class", description="e.g. 'O Level', 'Class 10'")
    subject: str
    mcqs: int = Field(10, ge=1, le=50)
    short_questions: int = Field(5, ge=0, le=30)
    long_questions: int = Field(3, ge=0, le=20)
    query: str = Field(..., min_length=3, description="Difficulty/focus descriptor")

    model_config = {"populate_by_name": True}


class UnverifiedPaperResponse(BaseModel):
    mcqs: List[MCQItem]
    short_questions: List[ShortQuestion]
    long_questions: List[LongQuestion]
