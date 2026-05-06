from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading

from database.database import Base, engine
from routes import upload, generate, search
from routes import verified, unverified


def _seed_in_background():
    """Run verified store seeding in a daemon thread — non-blocking."""
    try:
        from services.seed_verified import seed_verified_store
        seed_verified_store()
    except Exception as e:
        print(f"[Startup] Verified store seeding error: {e}")


# ─── Startup lifespan ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Kick off verified store seeding in the background; don't block startup."""
    t = threading.Thread(target=_seed_in_background, daemon=True)
    t.start()
    print("[Startup] Verified store seeding started in background thread.")
    yield


# ─── App ──────────────────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intelligent Exam Paper Generator",
    version="2.0",
    description=(
        "Dual-store RAG system: verified exam data (curated) "
        "and unverified community uploads — both powering AI-generated papers."
    ),
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────

# Legacy routes (unchanged)
app.include_router(upload.router,   prefix="/api", tags=["legacy"])
app.include_router(generate.router, prefix="/api", tags=["legacy"])
app.include_router(search.router,   prefix="/api", tags=["legacy"])

# New verified & unverified routes
app.include_router(verified.router)
app.include_router(unverified.router)


@app.get("/", tags=["health"])
def read_root():
    return {
        "message": "Intelligent Exam Paper Generator API v2",
        "verified_endpoints": [
            "POST /verified/generate-quiz",
            "POST /verified/generate-paper/cambridge",
            "POST /verified/generate-paper/boards",
        ],
        "unverified_endpoints": [
            "POST /unverified/upload-paper",
            "GET  /unverified/classes",
            "POST /unverified/generate-paper",
        ],
    }
