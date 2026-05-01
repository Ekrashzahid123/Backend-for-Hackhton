from sqlalchemy import Column, Integer, String, Float, Text, JSON
from .database import Base

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True, index=True)
    country = Column(String, nullable=True)
    subject = Column(String, index=True)
    exam_type = Column(String, nullable=True)
    language = Column(String)
    short_questions = Column(JSON) # List of dicts with 'text' and 'ranking_score'
    long_questions = Column(JSON)
    mcqs = Column(JSON)
    raw_text = Column(Text)
    ranking_score = Column(Float, default=0.0)
    
class GeneratedPaper(Base):
    __tablename__ = "generated_papers"
    
    id = Column(Integer, primary_key=True, index=True)
    request_hash = Column(String, unique=True, index=True)
    subject = Column(String)
    content = Column(JSON)
