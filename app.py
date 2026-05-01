from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import Base, engine
from routes import upload, generate, search

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Exam Paper Generator", version="1.0")

# Add CORS Middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(search.router, prefix="/api", tags=["search"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Intelligent Exam Paper Generator API"}
