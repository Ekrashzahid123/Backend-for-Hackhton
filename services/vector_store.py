"""
Vector Store Service — manages two ChromaDB persistent collections:
  • verified_papers   — curated, trusted exam question data
  • unverified_papers — user-uploaded, community-contributed data

Each question is stored as a separate document so semantic search
retrieves individual questions rather than whole papers.
"""

import os
import json
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional

# ─── ChromaDB client (persistent, stored in ./chroma_db/) ──────────────────────
_CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

_client = chromadb.PersistentClient(path=_CHROMA_PATH)

# Two named collections — created if they don't exist
verified_col = _client.get_or_create_collection(
    name="verified_papers",
    metadata={"hnsw:space": "cosine"},
)

unverified_col = _client.get_or_create_collection(
    name="unverified_papers",
    metadata={"hnsw:space": "cosine"},
)

# ─── Path to unverified metadata JSON ──────────────────────────────────────────
_META_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "unverified_meta.json")
os.makedirs(os.path.dirname(_META_PATH), exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# Internal helpers
# ═══════════════════════════════════════════════════════════════════════════════

def _load_meta() -> List[Dict]:
    if os.path.exists(_META_PATH):
        try:
            with open(_META_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_meta(meta: List[Dict]) -> None:
    with open(_META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


def _make_doc_id(prefix: str, index: int, extra: str = "") -> str:
    import hashlib
    raw = f"{prefix}_{index}_{extra}"
    return hashlib.md5(raw.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFIED store operations
# ═══════════════════════════════════════════════════════════════════════════════

def add_to_verified(
    documents: List[str],
    metadatas: List[Dict],
    ids: Optional[List[str]] = None,
) -> None:
    """Upsert documents into the verified collection."""
    if not documents:
        return
    if ids is None:
        ids = [_make_doc_id("verified", i, documents[i][:30]) for i in range(len(documents))]
    # Batch to avoid ChromaDB limits
    batch_size = 100
    for start in range(0, len(documents), batch_size):
        end = start + batch_size
        verified_col.upsert(
            documents=documents[start:end],
            metadatas=metadatas[start:end],
            ids=ids[start:end],
        )


def query_verified(
    query: str,
    n_results: int = 20,
    where: Optional[Dict] = None,
) -> List[Dict]:
    """Semantic search on the verified collection. Returns list of {text, metadata}."""
    kwargs: Dict[str, Any] = {"query_texts": [query], "n_results": min(n_results, max(verified_col.count(), 1))}
    if where:
        kwargs["where"] = where
    try:
        results = verified_col.query(**kwargs)
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        return [{"text": d, "metadata": m} for d, m in zip(docs, metas)]
    except Exception as e:
        print(f"[VectorStore] verified query error: {e}")
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# UNVERIFIED store operations
# ═══════════════════════════════════════════════════════════════════════════════

def add_to_unverified(
    documents: List[str],
    metadatas: List[Dict],
    ids: Optional[List[str]] = None,
) -> None:
    """Upsert documents into the unverified collection."""
    if not documents:
        return
    if ids is None:
        ids = [_make_doc_id("unverified", i, documents[i][:30]) for i in range(len(documents))]
    batch_size = 100
    for start in range(0, len(documents), batch_size):
        end = start + batch_size
        unverified_col.upsert(
            documents=documents[start:end],
            metadatas=metadatas[start:end],
            ids=ids[start:end],
        )


def query_unverified(
    query: str,
    n_results: int = 20,
    where: Optional[Dict] = None,
) -> List[Dict]:
    """Semantic search on the unverified collection. Returns list of {text, metadata}."""
    count = unverified_col.count()
    if count == 0:
        return []
    kwargs: Dict[str, Any] = {"query_texts": [query], "n_results": min(n_results, count)}
    if where:
        kwargs["where"] = where
    try:
        results = unverified_col.query(**kwargs)
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        return [{"text": d, "metadata": m} for d, m in zip(docs, metas)]
    except Exception as e:
        print(f"[VectorStore] unverified query error: {e}")
        return []


def compute_similarity_score(new_documents: List[str]) -> float:
    """
    Compute uniqueness score in range [0.00, 2.00].
    Compares new_documents against the existing unverified corpus.
    Score = (1 - avg_max_distance) * 2.0
    where distance 0 = identical, 1 = completely different (cosine space).
    Returns 2.00 if corpus is empty (first upload = fully unique).
    """
    count = unverified_col.count()
    if count == 0:
        return 2.00

    max_similarities = []
    for doc in new_documents[:10]:   # sample up to 10 docs for speed
        try:
            res = unverified_col.query(
                query_texts=[doc],
                n_results=min(5, count),
            )
            distances = res.get("distances", [[]])[0]
            if distances:
                # cosine distance: 0=same, 1=opposite → similarity = 1 - distance
                max_sim = max(1.0 - d for d in distances)
                max_similarities.append(max_sim)
        except Exception:
            pass

    if not max_similarities:
        return 2.00

    avg_max_sim = sum(max_similarities) / len(max_similarities)
    score = (1.0 - avg_max_sim) * 2.0
    return round(max(0.00, min(2.00, score)), 2)


# ═══════════════════════════════════════════════════════════════════════════════
# Metadata helpers (country / class / subject catalogue)
# ═══════════════════════════════════════════════════════════════════════════════

def save_unverified_paper_meta(country: str, class_name: str, subject: str, score: float) -> None:
    """Append a new paper's normalized metadata to the JSON catalogue."""
    meta = _load_meta()
    meta.append({"country": country, "class_name": class_name, "subject": subject, "score": score})
    _save_meta(meta)


def get_all_unverified_classes() -> List[Dict]:
    """
    Returns a list of unique {country, class_name, subjects: []} objects
    suitable for the GET /unverified/classes endpoint.
    """
    meta = _load_meta()
    # Group subjects under (country, class_name) keys
    catalogue: Dict[tuple, set] = {}
    for entry in meta:
        key = (entry.get("country", ""), entry.get("class_name", ""))
        catalogue.setdefault(key, set()).add(entry.get("subject", ""))

    result = []
    for (country, class_name), subjects in catalogue.items():
        result.append({
            "country": country,
            "class_name": class_name,
            "subjects": sorted(subjects),
        })
    return result


def get_existing_field_values() -> Dict[str, List[str]]:
    """Return existing distinct countries, classes, subjects for AI normalisation."""
    meta = _load_meta()
    countries = list({e.get("country", "") for e in meta if e.get("country")})
    classes = list({e.get("class_name", "") for e in meta if e.get("class_name")})
    subjects = list({e.get("subject", "") for e in meta if e.get("subject")})
    return {"countries": countries, "classes": classes, "subjects": subjects}
