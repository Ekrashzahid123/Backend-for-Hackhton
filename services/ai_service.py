"""
AI Service — wraps Mistral AI for:
  • Quiz generation (MCQs with answers)
  • Paper generation (mcqs + short + long sections)
  • Paper validation (slang check, subject/class/country relevance)
  • Field normalisation (dedup country/class/subject names)

Set MISTRAL_API_KEY in your .env file or environment variables.
"""

import os
import json
import re
from typing import List, Dict, Any

from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

_API_KEY    = os.getenv("MISTRAL_API_KEY", "")
_MODEL_NAME = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

_client: Mistral | None = Mistral(api_key=_API_KEY) if _API_KEY else None


# ─── Internal helpers ─────────────────────────────────────────────────────────

def _chat(prompt: str) -> str:
    """Send a single-turn chat message and return the reply text."""
    if not _client:
        raise RuntimeError("MISTRAL_API_KEY is not set.")
    response = _client.chat.complete(
        model=_MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _safe_json(text: str) -> Any:
    """Strip markdown fences and parse JSON from model output."""
    text = text.strip()
    text = re.sub(r"^```[a-z]*\n?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n?```$", "", text)
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"(\[.*\]|\{.*\})", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ GENERATION  (verified store)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_quiz(query: str, retrieved_chunks: List[Dict]) -> List[Dict]:
    """
    Generate MCQs with answers from retrieved chunks.
    Returns a list of MCQ objects:
    [{ "id": 1, "prompt": "...", "options": [{"id":"A","label":"..."},...], "answer": "A" }]
    """
    if not _client:
        return _fallback_quiz(retrieved_chunks)

    context = "\n\n".join([c["text"] for c in retrieved_chunks[:15]])

    prompt = f"""You are an expert exam paper creator. Based on the following educational content, 
generate multiple choice questions related to this topic: "{query}"

EDUCATIONAL CONTENT:
{context}

Generate exactly 10 MCQs. Return ONLY a valid JSON array with this exact structure:
[
  {{
    "id": 1,
    "prompt": "Question text here?",
    "options": [
      {{"id": "A", "label": "Option A text"}},
      {{"id": "B", "label": "Option B text"}},
      {{"id": "C", "label": "Option C text"}},
      {{"id": "D", "label": "Option D text"}}
    ],
    "answer": "A"
  }}
]

Rules:
- Each question must have exactly 4 options (A, B, C, D)
- The "answer" field must be one of: A, B, C, or D
- Questions must be clearly based on the provided content
- Do NOT include any explanation or text outside the JSON array"""

    try:
        raw = _chat(prompt)
        return _safe_json(raw)
    except Exception as e:
        print(f"[AI] generate_quiz error: {e}")
        return _fallback_quiz(retrieved_chunks)


def _fallback_quiz(chunks: List[Dict]) -> List[Dict]:
    mcqs = []
    for i, chunk in enumerate(chunks[:5]):
        text = chunk["text"][:100]
        mcqs.append({
            "id": i + 1,
            "prompt": f"Which of the following best describes: {text}?",
            "options": [
                {"id": "A", "label": "Option A"},
                {"id": "B", "label": "Option B"},
                {"id": "C", "label": "Option C"},
                {"id": "D", "label": "Option D"},
            ],
            "answer": "A",
        })
    return mcqs


# ═══════════════════════════════════════════════════════════════════════════════
# PAPER GENERATION  (verified & unverified)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_paper_sections(
    query: str,
    retrieved_chunks: List[Dict],
    num_mcqs: int,
    num_short: int,
    num_long: int,
    paper_style: str = "general",   # "cambridge" | "boards" | "general"
) -> Dict[str, List]:
    """
    Generate exam paper sections from retrieved chunks.
    Returns:
    {
      "mcqs": [ MCQ objects ],
      "short_questions": [ {"id": 1, "question": "..."} ],
      "long_questions":  [ {"id": 1, "question": "..."} ]
    }
    """
    if not _client:
        return _fallback_paper(retrieved_chunks, num_mcqs, num_short, num_long)

    context = "\n\n".join([c["text"] for c in retrieved_chunks[:20]])

    style_note = {
        "cambridge": "Follow Cambridge International Examinations style — precise, analytical, structured.",
        "boards":    "Follow Pakistani Board examination style — straightforward, curriculum-aligned.",
        "general":   "Use clear academic language suitable for students.",
    }.get(paper_style, "Use clear academic language suitable for students.")

    prompt = f"""You are an expert exam paper setter. {style_note}

Based on the educational content below, create an exam paper for the topic: "{query}"

EDUCATIONAL CONTENT:
{context}

Generate:
- {num_mcqs} MCQs (with 4 options A/B/C/D and correct answer)
- {num_short} short questions (1-2 sentences, 2-4 marks each)
- {num_long} long questions (detailed, 8-15 marks each)

Return ONLY a valid JSON object with this exact structure:
{{
  "mcqs": [
    {{
      "id": 1,
      "prompt": "Question?",
      "options": [
        {{"id": "A", "label": "..."}},
        {{"id": "B", "label": "..."}},
        {{"id": "C", "label": "..."}},
        {{"id": "D", "label": "..."}}
      ],
      "answer": "A"
    }}
  ],
  "short_questions": [
    {{"id": 1, "question": "Short question text?"}}
  ],
  "long_questions": [
    {{"id": 1, "question": "Long question text requiring detailed answer?"}}
  ]
}}

Rules:
- Strictly follow the counts ({num_mcqs} MCQs, {num_short} short, {num_long} long)
- All questions must relate to the provided content and topic query
- Do NOT include any text outside the JSON object"""

    try:
        raw = _chat(prompt)
        result = _safe_json(raw)
        result["mcqs"]            = result.get("mcqs", [])[:num_mcqs]
        result["short_questions"] = result.get("short_questions", [])[:num_short]
        result["long_questions"]  = result.get("long_questions", [])[:num_long]
        return result
    except Exception as e:
        print(f"[AI] generate_paper_sections error: {e}")
        return _fallback_paper(retrieved_chunks, num_mcqs, num_short, num_long)


def _fallback_paper(chunks, num_mcqs, num_short, num_long) -> Dict:
    texts = [c["text"] for c in chunks]
    mcqs = []
    for i in range(min(num_mcqs, len(texts))):
        mcqs.append({
            "id": i + 1,
            "prompt": texts[i][:120] + "?",
            "options": [
                {"id": "A", "label": "Option A"},
                {"id": "B", "label": "Option B"},
                {"id": "C", "label": "Option C"},
                {"id": "D", "label": "Option D"},
            ],
            "answer": "A",
        })
    short_qs = [{"id": i + 1, "question": texts[i][:200] + "?"} for i in range(min(num_short, len(texts)))]
    long_qs  = [{"id": i + 1, "question": texts[i][:400] + "?"} for i in range(min(num_long, len(texts)))]
    return {"mcqs": mcqs, "short_questions": short_qs, "long_questions": long_qs}


# ═══════════════════════════════════════════════════════════════════════════════
# PAPER VALIDATION  (unverified uploads)
# ═══════════════════════════════════════════════════════════════════════════════

def validate_paper(text: str, country: str, class_name: str, subject: str) -> Dict[str, Any]:
    """
    Validate an uploaded paper:
    1. Check for slang / inappropriate content
    2. Check relevance to declared subject/class/country

    Returns: {"valid": bool, "reason": str}
    """
    if not _client:
        return {"valid": True, "reason": ""}

    sample = text[:3000]

    prompt = f"""You are an academic content moderator. Analyse the following exam paper excerpt.

Paper metadata:
- Country: {country}
- Class / Level: {class_name}
- Subject: {subject}

Paper excerpt:
\"\"\"
{sample}
\"\"\"

Perform these checks:
1. SLANG CHECK: Does the paper contain slang words, profanity, offensive language, or highly informal text inappropriate for an academic setting?
2. RELEVANCE CHECK: Does the content appear to be related to the declared subject "{subject}" and appropriate for "{class_name}" level? (Be lenient — partial matches are fine.)
3. ACADEMIC QUALITY: Is this clearly an exam paper / question set (not random text, spam, or completely off-topic content)?

Return ONLY a valid JSON object:
{{
  "valid": true,
  "reason": ""
}}

If ANY check fails, set valid to false and provide a clear, user-friendly reason (1-2 sentences).
If all checks pass, set valid to true and reason to empty string "".
Do NOT include text outside the JSON."""

    try:
        raw = _chat(prompt)
        result = _safe_json(raw)
        return {
            "valid":  bool(result.get("valid", False)),
            "reason": str(result.get("reason", "")),
        }
    except Exception as e:
        print(f"[AI] validate_paper error: {e}")
        return {"valid": True, "reason": ""}


# ═══════════════════════════════════════════════════════════════════════════════
# FIELD NORMALISATION  (prevent duplicate country/class/subject names)
# ═══════════════════════════════════════════════════════════════════════════════

def normalize_field(value: str, existing_values: List[str], field_type: str = "value") -> str:
    """
    Use Mistral to decide if `value` is semantically the same as any existing value.
    Returns the canonical existing value if matched, otherwise returns title-cased `value`.
    """
    if not existing_values:
        return value.strip().title()

    if not _client:
        val_lower = value.strip().lower()
        for ev in existing_values:
            if ev.strip().lower() == val_lower:
                return ev
        return value.strip().title()

    prompt = f"""You are a data normalisation assistant.

New {field_type}: "{value}"
Existing {field_type} values: {json.dumps(existing_values)}

Task: Decide if the new value is essentially the same as one of the existing values (e.g. same meaning, abbreviation, or alternate spelling).
- If YES: return the exact matching existing value (do not modify it).
- If NO: return the new value in a clean, title-cased format.

Return ONLY a JSON object:
{{"normalized": "The chosen value"}}"""

    try:
        raw = _chat(prompt)
        result = _safe_json(raw)
        return str(result.get("normalized", value)).strip()
    except Exception as e:
        print(f"[AI] normalize_field error: {e}")
        return value.strip().title()
