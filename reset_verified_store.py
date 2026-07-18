"""
Reset script: clears the verified ChromaDB collection so the corrected
seed_verified_store() function (Pakistan-only filter) can re-populate it
on next startup.

Usage:
    python reset_verified_store.py
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def reset_verified_store():
    print("[Reset] Clearing verified ChromaDB collection ...")
    from services.vector_store import verified_col

    count_before = verified_col.count()
    print(f"[Reset] Current document count: {count_before}")

    if count_before > 0:
        result = verified_col.get(include=[])
        ids = result.get("ids", [])
        if ids:
            # Delete in batches to avoid memory issues with large collections
            batch_size = 1000
            deleted = 0
            for start in range(0, len(ids), batch_size):
                batch = ids[start:start + batch_size]
                verified_col.delete(ids=batch)
                deleted += len(batch)
                print(f"[Reset] Deleted {deleted}/{len(ids)} documents ...")
        print(f"[Reset] Cleared verified_col.")
    else:
        print("[Reset] Collection already empty.")

    print(f"[Reset] Collection count after reset: {verified_col.count()}")
    print("[Reset] Done. Re-seeding with Pakistan-only data ...")

    # Immediately re-seed
    from services.seed_verified import seed_verified_store
    seed_verified_store()


if __name__ == "__main__":
    reset_verified_store()
