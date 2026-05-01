from fastapi import FastAPI
from database.database import Base, engine
from routes import upload, generate, search

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Exam Paper Generator", version="1.0")

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(search.router, prefix="/api", tags=["search"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Intelligent Exam Paper Generator API"}
