"""
Seed the verified ChromaDB collection from the existing mock_data.json.

This runs automatically on every server startup via the lifespan hook in app.py.
It is idempotent — already-stored documents are upserted (not duplicated).

You can also run it manually:
    python -m services.seed_verified
"""

import os
import json
from typing import List, Dict

_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mock_data.json")
_MAX_DOCS   = 5000   # cap to keep startup memory usage reasonable


def _chunk_text(text: str, max_chars: int = 500) -> List[str]:
    """Split long text into overlapping chunks for better retrieval."""
    if len(text) <= max_chars:
        return [text]
    chunks = []
    step = max_chars - 100  # 100-char overlap
    for i in range(0, len(text), step):
        chunk = text[i : i + max_chars].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def seed_verified_store() -> None:
    """Load mock_data.json and upsert all questions into the verified collection."""
    from services.vector_store import verified_col, add_to_verified

    # Skip if already seeded (check collection size)
    existing_count = verified_col.count()
    if existing_count > 0:
        print(f"[Seed] Verified store already has {existing_count} documents — skipping.")
        return

    if not os.path.exists(_DATA_PATH):
        print("[Seed] mock_data.json not found — verified store left empty.")
        return

    print("[Seed] Loading mock_data.json …")
    try:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[Seed] Failed to load mock_data.json: {e}")
        return

    documents: List[str] = []
    metadatas: List[Dict] = []

    # mock_data.json may be a list of paper objects or a dict — handle both
    entries = data if isinstance(data, list) else data.get("papers", [data])

    for paper in entries:
        subject    = str(paper.get("subject", "General"))
        class_name = str(paper.get("class", paper.get("class_name", paper.get("exam_type", "General"))))
        country    = str(paper.get("country", "General"))

        base_meta = {
            "subject":    subject,
            "class_name": class_name,
            "country":    country,
        }

        # MCQs
        for mcq in paper.get("mcqs", []):
            text = mcq if isinstance(mcq, str) else mcq.get("text", mcq.get("question", ""))
            if text.strip():
                documents.append(text.strip())
                metadatas.append({**base_meta, "question_type": "mcq"})

        # Short questions
        for sq in paper.get("short_questions", []):
            text = sq if isinstance(sq, str) else sq.get("text", sq.get("question", ""))
            if text.strip():
                documents.append(text.strip())
                metadatas.append({**base_meta, "question_type": "short"})

        # Long questions
        for lq in paper.get("long_questions", []):
            text = lq if isinstance(lq, str) else lq.get("text", lq.get("question", ""))
            if text.strip():
                documents.append(text.strip())
                metadatas.append({**base_meta, "question_type": "long"})

        # Raw text fallback — chunk it
        raw_text = paper.get("raw_text", "")
        if raw_text and not documents:
            for chunk in _chunk_text(raw_text):
                documents.append(chunk)
                metadatas.append({**base_meta, "question_type": "chunk"})

    if not documents:
        print("[Seed] No documents extracted from mock_data.json.")
        return

    # Cap to avoid excessive memory / time on very large files
    if len(documents) > _MAX_DOCS:
        print(f"[Seed] Capping at {_MAX_DOCS} docs (file has {len(documents)}).")
        documents = documents[:_MAX_DOCS]
        metadatas = metadatas[:_MAX_DOCS]

    print(f"[Seed] Upserting {len(documents)} documents into verified store …")
    add_to_verified(documents, metadatas)
    print(f"[Seed] Done. Verified store now has {verified_col.count()} documents.")


if __name__ == "__main__":
    seed_verified_store()
