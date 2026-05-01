from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from models.schemas import GenerateRequest, GenerateResponse
import hashlib

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
async def generate_paper(req: GenerateRequest, db: Session = Depends(get_db)):
    # Create a unique hash for this generation request to avoid re-generating
    req_string = f"{req.subject}_{req.num_mcqs}_{req.num_short}_{req.num_long}".lower()
    req_hash = hashlib.md5(req_string.encode('utf-8')).hexdigest()
    
    # 7. Existing Paper Check in Generation
    existing_gen = db.query(models.GeneratedPaper).filter(models.GeneratedPaper.request_hash == req_hash).first()
    if existing_gen:
        return GenerateResponse(message="Returning existing generated result", paper=existing_gen.content)
        
    # Fetch all papers for this subject
    papers = db.query(models.Paper).filter(models.Paper.subject.ilike(f"%{req.subject}%")).all()
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for this subject.")
        
    # Pool all questions
    all_mcqs = []
    all_short = []
    all_long = []
    
    for p in papers:
        if p.mcqs:
            all_mcqs.extend(p.mcqs)
        if p.short_questions:
            all_short.extend(p.short_questions)
        if p.long_questions:
            all_long.extend(p.long_questions)
        
    # Sort pooled questions by ranking score
    all_mcqs.sort(key=lambda x: x.get("ranking_score", 0.0), reverse=True)
    all_short.sort(key=lambda x: x.get("ranking_score", 0.0), reverse=True)
    all_long.sort(key=lambda x: x.get("ranking_score", 0.0), reverse=True)
    
    # De-duplicate by text
    def deduplicate(q_list, limit):
        seen = set()
        result = []
        for q in q_list:
            t = q.get("text", "")
            if t not in seen:
                seen.add(t)
                result.append(q)
                if len(result) >= limit:
                    break
        return result
        
    selected_mcqs = deduplicate(all_mcqs, req.num_mcqs)
    selected_short = deduplicate(all_short, req.num_short)
    selected_long = deduplicate(all_long, req.num_long)
    
    generated_content = {
        "subject": req.subject,
        "section_A_mcqs": [q["text"] for q in selected_mcqs],
        "section_B_short": [q["text"] for q in selected_short],
        "section_C_long": [q["text"] for q in selected_long]
    }
    
    # Save generated paper
    new_gen = models.GeneratedPaper(
        request_hash=req_hash,
        subject=req.subject,
        content=generated_content
    )
    db.add(new_gen)
    db.commit()
    
    return GenerateResponse(message="New paper generated successfully", paper=generated_content)
