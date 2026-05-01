from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from models.schemas import SearchResponse
from typing import Optional

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search_papers(
    subject: Optional[str] = None, 
    country: Optional[str] = None, 
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Paper)
    
    if subject:
        query = query.filter(models.Paper.subject.ilike(f"%{subject}%"))
    if country:
        query = query.filter(models.Paper.country.ilike(f"%{country}%"))
    if keyword:
        query = query.filter(models.Paper.raw_text.ilike(f"%{keyword}%"))
        
    papers = query.order_by(models.Paper.ranking_score.desc()).all()
    
    result = []
    for p in papers:
        result.append({
            "hash": p.hash,
            "subject": p.subject,
            "country": p.country,
            "exam_type": p.exam_type,
            "language": p.language,
            "ranking_score": p.ranking_score
        })
        
    return SearchResponse(results=result)
