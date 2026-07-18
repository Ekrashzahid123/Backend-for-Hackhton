"""
Vector Store Service — manages two ChromaDB persistent collections:
  • verified_papers   — curated, trusted exam question data
  • unverified_papers — user-uploaded, community-contributed data

Each question is stored as a SEPARATE document (one vector per question).

Full metadata schema per vector:
  country, category, class_name, subject, paper_type,
  question_type, filename, paper_id, timestamp

question_type values : mcq | short | long
paper_type values    : verified | unverified
"""

import os
import json
import hashlib
import datetime
import chromadb
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
    raw = f"{prefix}_{index}_{extra}"
    return hashlib.md5(raw.encode()).hexdigest()


def _build_meta_filter(
    country: str = None,
    category: str = None,
    class_name: str = None,
    subject: str = None,
) -> Optional[Dict]:
    """Build a ChromaDB $and/$eq where-filter from metadata fields."""
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


def _append_type_filter(base_filter: Optional[Dict], question_type: str) -> Dict:
    """Append a question_type condition to an existing filter."""
    type_cond = {"question_type": {"$eq": question_type}}
    if not base_filter:
        return type_cond
    if "$and" in base_filter:
        return {"$and": base_filter["$and"] + [type_cond]}
    return {"$and": [base_filter, type_cond]}


def _get_docs_from_collection(
    col,
    where_filter: Optional[Dict],
    limit: int = 1000,
) -> List[str]:
    """Retrieve document texts using metadata filter (no semantic search)."""
    try:
        kwargs: Dict[str, Any] = {"include": ["documents"], "limit": limit}
        if where_filter:
            kwargs["where"] = where_filter
        res = col.get(**kwargs)
        return [d for d in res.get("documents", []) if d and d.strip()]
    except Exception as e:
        print(f"[VectorStore] _get_docs_from_collection error: {e}")
        return []


def _build_hierarchy_from_collection(col) -> Dict[str, Any]:
    """Build country → category → class_name → [subjects] from a ChromaDB collection."""
    try:
        res = col.get(include=["metadatas"])
        metas = res.get("metadatas", [])
    except Exception as e:
        print(f"[VectorStore] _build_hierarchy_from_collection error: {e}")
        return {}

    tree: Dict[str, Dict[str, Dict[str, set]]] = {}
    for m in metas:
        country  = m.get("country",    "Unknown")
        category = m.get("category",   "General")
        class_nm = m.get("class_name", "Unknown")
        subject  = m.get("subject",    "Unknown")
        tree.setdefault(country, {})
        tree[country].setdefault(category, {})
        tree[country][category].setdefault(class_nm, set())
        tree[country][category][class_nm].add(subject)

    # Convert sets → sorted lists
    result: Dict[str, Any] = {}
    for country, cats in tree.items():
        result[country] = {}
        for cat, classes in cats.items():
            result[country][cat] = {cls: sorted(subs) for cls, subs in classes.items()}
    return result


def _hierarchy_from_json_meta() -> Dict[str, Any]:
    """Build hierarchy from the JSON meta file (fallback for empty unverified_col)."""
    meta = _load_meta()
    tree: Dict[str, Dict[str, Dict[str, set]]] = {}
    for entry in meta:
        country  = entry.get("country",    "Unknown")
        category = entry.get("category",   "General")
        class_nm = entry.get("class_name", "Unknown")
        subject  = entry.get("subject",    "Unknown")
        tree.setdefault(country, {})
        tree[country].setdefault(category, {})
        tree[country][category].setdefault(class_nm, set())
        tree[country][category][class_nm].add(subject)

    result: Dict[str, Any] = {}
    for country, cats in tree.items():
        result[country] = {}
        for cat, classes in cats.items():
            result[country][cat] = {cls: sorted(subs) for cls, subs in classes.items()}
    return result


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
    count = verified_col.count()
    if count == 0:
        return []
    kwargs: Dict[str, Any] = {
        "query_texts": [query],
        "n_results": min(n_results, max(count, 1)),
    }
    if where:
        kwargs["where"] = where
    try:
        results = verified_col.query(**kwargs)
        docs  = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        return [{"text": d, "metadata": m} for d, m in zip(docs, metas)]
    except Exception as e:
        print(f"[VectorStore] verified query error: {e}")
        return []


def get_verified_questions_by_type(
    country: str = None,
    category: str = None,
    class_name: str = None,
    subject: str = None,
    limit_per_type: int = 500,
) -> Dict[str, List[str]]:
    """
    Metadata-filtered retrieval of ALL verified questions grouped by type.
    Metadata filtering happens BEFORE retrieval — no semantic search step.

    Returns: {"mcqs": [...], "short": [...], "long": [...]}
    """
    if verified_col.count() == 0:
        return {"mcqs": [], "short": [], "long": []}

    base = _build_meta_filter(
        country=country, category=category, class_name=class_name, subject=subject
    )
    return {
        "mcqs":  _get_docs_from_collection(verified_col, _append_type_filter(base, "mcq"),   limit_per_type),
        "short": _get_docs_from_collection(verified_col, _append_type_filter(base, "short"), limit_per_type),
        "long":  _get_docs_from_collection(verified_col, _append_type_filter(base, "long"),  limit_per_type),
    }


def get_verified_hierarchy() -> Dict[str, Any]:
    """Return country → category → class_name → [subjects] from verified collection."""
    return _build_hierarchy_from_collection(verified_col)


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
    kwargs: Dict[str, Any] = {
        "query_texts": [query],
        "n_results": min(n_results, count),
    }
    if where:
        kwargs["where"] = where
    try:
        results = unverified_col.query(**kwargs)
        docs  = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        return [{"text": d, "metadata": m} for d, m in zip(docs, metas)]
    except Exception as e:
        print(f"[VectorStore] unverified query error: {e}")
        return []


def get_unverified_questions_by_type(
    country: str = None,
    category: str = None,
    class_name: str = None,
    subject: str = None,
    limit_per_type: int = 500,
) -> Dict[str, List[str]]:
    """
    Metadata-filtered retrieval of ALL unverified questions grouped by type.
    Returns: {"mcqs": [...], "short": [...], "long": [...]}
    """
    if unverified_col.count() == 0:
        return {"mcqs": [], "short": [], "long": []}

    base = _build_meta_filter(
        country=country, category=category, class_name=class_name, subject=subject
    )
    return {
        "mcqs":  _get_docs_from_collection(unverified_col, _append_type_filter(base, "mcq"),   limit_per_type),
        "short": _get_docs_from_collection(unverified_col, _append_type_filter(base, "short"), limit_per_type),
        "long":  _get_docs_from_collection(unverified_col, _append_type_filter(base, "long"),  limit_per_type),
    }


def get_unverified_hierarchy() -> Dict[str, Any]:
    """Return country → category → class_name → [subjects] from unverified collection."""
    if unverified_col.count() == 0:
        return _hierarchy_from_json_meta()
    return _build_hierarchy_from_collection(unverified_col)


def compute_similarity_score(new_documents: List[str]) -> float:
    """
    Compute uniqueness score in range [0, 5].
    uniqueness_score = 5 - (average_max_similarity * 5)

    Example: avg similarity 90%  → uniqueness = 0.5
             avg similarity 25%  → uniqueness = 3.75
    Returns 5.0 if corpus is empty (first upload = fully unique).
    """
    count = unverified_col.count()
    if count == 0:
        return 5.0

    max_similarities = []
    for doc in new_documents[:10]:  # sample up to 10 docs for speed
        try:
            res = unverified_col.query(
                query_texts=[doc],
                n_results=min(5, count),
            )
            distances = res.get("distances", [[]])[0]
            if distances:
                # cosine distance: 0=identical, 1=orthogonal → similarity = 1 - distance
                max_sim = max(1.0 - d for d in distances)
                max_similarities.append(max_sim)
        except Exception:
            pass

    if not max_similarities:
        return 5.0

    avg_max_sim = sum(max_similarities) / len(max_similarities)
    score = (1.0 - avg_max_sim) * 5.0
    return round(max(0.0, min(5.0, score)), 2)



# ═══════════════════════════════════════════════════════════════════════════════
# Metadata helpers (unverified JSON catalogue)
# ═══════════════════════════════════════════════════════════════════════════════

def save_unverified_paper_meta(
    country: str,
    class_name: str,
    subject: str,
    score: float,
    category: str = "General",
    filename: str = "",
) -> None:
    """Append a new paper's normalized metadata to the JSON catalogue."""
    meta = _load_meta()
    meta.append({
        "country":    country,
        "category":   category,
        "class_name": class_name,
        "subject":    subject,
        "score":      score,
        "filename":   filename,
        "timestamp":  datetime.datetime.utcnow().isoformat(),
    })
    _save_meta(meta)




def get_existing_field_values() -> Dict[str, List[str]]:
    """Return existing distinct countries, classes, subjects for AI normalisation."""
    meta = _load_meta()
    countries = list({e.get("country", "")    for e in meta if e.get("country")})
    classes   = list({e.get("class_name", "") for e in meta if e.get("class_name")})
    subjects  = list({e.get("subject", "")    for e in meta if e.get("subject")})
    return {"countries": countries, "classes": classes, "subjects": subjects}


def get_verified_field_values() -> Dict[str, List[str]]:
    """Return existing distinct countries, classes, subjects in verified store."""
    hierarchy = get_verified_hierarchy()
    countries = list(hierarchy.keys())
    classes = set()
    subjects = set()
    for cats in hierarchy.values():
        for cls_dict in cats.values():
            for cls_name, subs in cls_dict.items():
                classes.add(cls_name)
                for s in subs:
                    subjects.add(s)
    return {
        "countries": countries,
        "classes": list(classes),
        "subjects": list(subjects)
    }
