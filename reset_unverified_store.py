"""
Reset script: clears the unverified ChromaDB collection and the
unverified_meta.json file so the new international seed data will be
loaded on the next application startup.

Usage:
    python reset_unverified_store.py Ekrash zahid 
"""
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def reset_unverified_store():
    print("[Reset] Clearing unverified ChromaDB collection ...")
    from services.vector_store import unverified_col

    count_before = unverified_col.count()
    print(f"[Reset] Current document count: {count_before}")

    if count_before > 0:
        # Get all IDs and delete them
        result = unverified_col.get(include=[])
        ids = result.get("ids", [])
        if ids:
            unverified_col.delete(ids=ids)
            print(f"[Reset] Deleted {len(ids)} documents from unverified_col.")
    else:
        print("[Reset] Collection already empty.")

    print(f"[Reset] Collection count after reset: {unverified_col.count()}")

    # Clear unverified_meta.json
    meta_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "unverified_meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump([], f)
        print(f"[Reset] Cleared {meta_path}")
    else:
        print("[Reset] unverified_meta.json not found — nothing to clear.")

    print("[Reset] Done. Restart the app or run seed_unverified_store to re-populate with new data.")


if __name__ == "__main__":
    reset_unverified_store()

    # Immediately re-seed with new international data
    print("\n[Reset] Now seeding with new international data ...")
    from services.seed_unverified_store import seed_unverified_store
    seed_unverified_store()
