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

try:
    from mistralai.client import Mistral
except ImportError:
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

    prompt = f"""You are an expert exam paper creator. 

TASK: Based on the following educational content, generate multiple choice questions related to the topic: "{query}"

EDUCATIONAL CONTENT:
{context}

RELEVANCE RULE: 
If the topic "{query}" is NOT related to education, or if it's a general greeting/conversation (like "how are you", "hello", etc.) that cannot be answered using the educational content, return an empty JSON array [].

If relevant, generate exactly 10 MCQs. Return ONLY a valid JSON array with this exact structure:
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

TASK: Based on the educational content below, create an exam paper for the topic: "{query}"

EDUCATIONAL CONTENT:
{context}

RELEVANCE RULE:
If the topic "{query}" is NOT related to education, or if it's a general greeting/conversation (like "how are you", "hello", etc.) that cannot be answered using the educational content, return an empty JSON object: {{"mcqs": [], "short_questions": [], "long_questions": []}}.

Otherwise, generate:
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

# ═══════════════════════════════════════════════════════════════════════════════
# PAPER GENERATION — spec-mandated: SELECT ONLY, never invent
# ═══════════════════════════════════════════════════════════════════════════════

def generate_paper_from_questions(
    mcqs: List[str],
    short_questions: List[str],
    long_questions: List[str],
    number_of_mcqs: int,
    number_of_short_questions: int,
    number_of_long_questions: int,
    preference: str = "Mixed",
) -> Dict[str, List]:
    """
    Select and rank EXISTING questions only — LLM never invents.
    Implements the exact spec prompt.

    Returns:
    {
      "mcqs": [ MCQ objects ],
      "short_questions": [ {"id": 1, "question": "..."} ],
      "long_questions":  [ {"id": 1, "question": "..."} ]
    }
    """
    if not _client:
        return _fallback_select(
            mcqs, short_questions, long_questions,
            number_of_mcqs, number_of_short_questions, number_of_long_questions,
        )

    mcq_block   = "\n".join(f"{i+1}. {q}" for i, q in enumerate(mcqs))   or "None available."
    short_block = "\n".join(f"{i+1}. {q}" for i, q in enumerate(short_questions)) or "None available."
    long_block  = "\n".join(f"{i+1}. {q}" for i, q in enumerate(long_questions))  or "None available."

    prompt = f"""You are provided with a list of examination questions.

Use ONLY these questions. Do NOT generate new questions.

Select exactly:
{number_of_mcqs} MCQs
{number_of_short_questions} Short Questions
{number_of_long_questions} Long Questions

Preference: {preference}
(Easy = simpler questions, Medium = moderate difficulty, Hard = complex/analytical, Popular = commonly tested topics, Mixed = balanced selection across difficulty)

Only sort and select questions. Never rewrite or invent questions.

AVAILABLE MCQs:
{mcq_block}

AVAILABLE SHORT QUESTIONS:
{short_block}

AVAILABLE LONG QUESTIONS:
{long_block}

Return ONLY a valid JSON object with this exact structure:
{{
  "mcqs": [
    {{
      "id": 1,
      "prompt": "Exact question text copied from above",
      "options": [
        {{"id": "A", "label": "Option A text"}},
        {{"id": "B", "label": "Option B text"}},
        {{"id": "C", "label": "Option C text"}},
        {{"id": "D", "label": "Option D text"}}
      ],
      "answer": "A"
    }}
  ],
  "short_questions": [
    {{"id": 1, "question": "Exact question text copied from above"}}
  ],
  "long_questions": [
    {{"id": 1, "question": "Exact question text copied from above"}}
  ]
}}

Rules:
- Copy question texts EXACTLY as provided — do not rephrase
- If an MCQ in the source does not include A/B/C/D options, generate 4 plausible options and mark the correct answer
- Select no more than what is actually available in each list; if fewer than requested are available, return all that exist
- Do NOT include any text outside the JSON object"""

    try:
        raw = _chat(prompt)
        result = _safe_json(raw)
        result["mcqs"]            = result.get("mcqs", [])[:number_of_mcqs]
        result["short_questions"] = result.get("short_questions", [])[:number_of_short_questions]
        result["long_questions"]  = result.get("long_questions", [])[:number_of_long_questions]
        return result
    except Exception as e:
        print(f"[AI] generate_paper_from_questions error: {e}")
        return _fallback_select(
            mcqs, short_questions, long_questions,
            number_of_mcqs, number_of_short_questions, number_of_long_questions,
        )


def _fallback_select(
    mcqs: List[str],
    short_questions: List[str],
    long_questions: List[str],
    n_mcqs: int,
    n_short: int,
    n_long: int,
) -> Dict:
    """Simple slice-based fallback when LLM is unavailable."""
    def make_mcq(text: str, idx: int) -> Dict:
        return {
            "id": idx + 1,
            "prompt": text[:250],
            "options": [
                {"id": "A", "label": "Option A"},
                {"id": "B", "label": "Option B"},
                {"id": "C", "label": "Option C"},
                {"id": "D", "label": "Option D"},
            ],
            "answer": "A",
        }
    return {
        "mcqs":            [make_mcq(q, i) for i, q in enumerate(mcqs[:n_mcqs])],
        "short_questions": [{"id": i + 1, "question": q[:400]} for i, q in enumerate(short_questions[:n_short])],
        "long_questions":  [{"id": i + 1, "question": q[:600]} for i, q in enumerate(long_questions[:n_long])],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ GENERATION — spec-mandated: SELECT ONLY from verified store
# ═══════════════════════════════════════════════════════════════════════════════

def generate_quiz_from_questions(
    mcqs: List[str],
    number_of_mcqs: int,
    preference: str = "Mixed",
) -> List[Dict]:
    """
    Select MCQs from provided list — LLM never invents.
    Quiz generation ALWAYS uses the Verified Vector DB.

    Returns list of MCQ objects with correct answers.
    """
    if not _client:
        return _fallback_quiz_select(mcqs, number_of_mcqs)

    mcq_block = "\n".join(f"{i+1}. {q}" for i, q in enumerate(mcqs)) or "None available."

    prompt = f"""Use ONLY the supplied MCQs below.

Select {number_of_mcqs} MCQs based upon preference: {preference}
(Easy = simpler questions, Medium = moderate, Hard = complex/analytical, Popular = commonly tested topics, Mixed = balanced selection)

Return selected MCQs along with their correct answers.

Do not generate new MCQs. Copy question text exactly.

AVAILABLE MCQs:
{mcq_block}

Return ONLY a valid JSON array:
[
  {{
    "id": 1,
    "prompt": "Exact MCQ text copied from above",
    "options": [
      {{"id": "A", "label": "Option A text"}},
      {{"id": "B", "label": "Option B text"}},
      {{"id": "C", "label": "Option C text"}},
      {{"id": "D", "label": "Option D text"}}
    ],
    "answer": "B"
  }}
]

Rules:
- Copy MCQ text EXACTLY as provided — do not rephrase
- If options are not embedded in the source text, generate 4 plausible options and mark the correct answer
- Select no more than what is available; if fewer than {number_of_mcqs} exist, return all available
- Do NOT include text outside the JSON array"""

    try:
        raw = _chat(prompt)
        return _safe_json(raw)
    except Exception as e:
        print(f"[AI] generate_quiz_from_questions error: {e}")
        return _fallback_quiz_select(mcqs, number_of_mcqs)


def _fallback_quiz_select(mcqs: List[str], n_mcqs: int) -> List[Dict]:
    """Simple slice-based fallback for quiz selection."""
    result = []
    for i, q in enumerate(mcqs[:n_mcqs]):
        result.append({
            "id": i + 1,
            "prompt": q[:250],
            "options": [
                {"id": "A", "label": "Option A"},
                {"id": "B", "label": "Option B"},
                {"id": "C", "label": "Option C"},
                {"id": "D", "label": "Option D"},
            ],
            "answer": "A",
        })
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION EXTRACTION  (for uploaded papers)
# ═══════════════════════════════════════════════════════════════════════════════

def extract_questions_with_llm(text: str) -> Dict[str, List[str]]:
    """
    Use LLM to extract MCQs, short questions, and long questions from
    an uploaded paper's text. Falls back to empty lists if LLM unavailable.

    Returns: {"mcqs": [...], "short_questions": [...], "long_questions": [...]}
    """
    if not _client:
        return {"mcqs": [], "short_questions": [], "long_questions": []}

    sample = text[:5000]  # limit to avoid token overflow

    prompt = f"""You are an expert at parsing examination papers.

Extract all questions from the following exam paper text and classify each as:
- "mcq": Multiple-choice question (has options A/B/C/D or similar)
- "short_question": Short-answer question (1–4 marks, brief answer expected)
- "long_question": Long-answer question (requires detailed explanation, essay, derivation, or experiment)

PAPER TEXT:
\"\"\"
{sample}
\"\"\"

Return ONLY a valid JSON object:
{{
  "mcqs": ["complete question text including options", ...],
  "short_questions": ["complete question text", ...],
  "long_questions": ["complete question text", ...]
}}

Rules:
- Include the complete question text for each entry
- For MCQs, embed the options in the text string (e.g., "What is X? A) a  B) b  C) c  D) d")
- Do not include answers
- If no questions of a type are found, return an empty array for that type
- Do NOT include text outside the JSON"""

    try:
        raw = _chat(prompt)
        result = _safe_json(raw)
        return {
            "mcqs":            result.get("mcqs",            []),
            "short_questions": result.get("short_questions", []),
            "long_questions":  result.get("long_questions",  []),
        }
    except Exception as e:
        print(f"[AI] extract_questions_with_llm error: {e}")
        return {"mcqs": [], "short_questions": [], "long_questions": []}


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

    val_lower = value.strip().lower()
    # 1. Exact match (case-insensitive)
    for ev in existing_values:
        if ev.strip().lower() == val_lower:
            return ev

    # 2. Prefix / abbreviation match (e.g. "math" -> "Mathematics")
    for ev in existing_values:
        ev_lower = ev.strip().lower()
        if ev_lower.startswith(val_lower) or val_lower.startswith(ev_lower):
            return ev

    if not _client:
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
