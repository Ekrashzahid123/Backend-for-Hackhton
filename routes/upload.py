from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from services import ocr_service, nlp_service, ranking_service

router = APIRouter()

@router.post("/upload")
async def upload_paper(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    file_bytes = await file.read()
    
    # 1. OCR Pipeline
    raw_text = ocr_service.extract_text_from_pdf(file_bytes)
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
        
    # 2. Clean Text
    clean_text = nlp_service.clean_text(raw_text)
    
    # 3. Duplicate Detection
    paper_hash = nlp_service.generate_hash(clean_text)
    existing_paper = db.query(models.Paper).filter(models.Paper.hash == paper_hash).first()
    if existing_paper:
        return {"message": "Paper already exists in database", "hash": paper_hash}
        
    # 4. Metadata Extraction
    lang = nlp_service.detect_language(clean_text)
    country, subject, exam_type = nlp_service.extract_metadata(clean_text)
    
    # 5. Question Extraction
    short_q, long_q, mcqs = nlp_service.extract_questions(clean_text)
    
    # 6. Ranking
    ranked_short = ranking_service.rank_questions(short_q)
    ranked_long = ranking_service.rank_questions(long_q)
    ranked_mcqs = ranking_service.rank_questions(mcqs)
    
    paper_ranking = ranking_service.calculate_paper_ranking(ranked_short, ranked_long, ranked_mcqs)
    
    # 7. Store in DB
    new_paper = models.Paper(
        hash=paper_hash,
        country=country,
        subject=subject,
        exam_type=exam_type,
        language=lang,
        short_questions=ranked_short,
        long_questions=ranked_long,
        mcqs=ranked_mcqs,
        raw_text=clean_text,
        ranking_score=paper_ranking
    )
    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)
    
    return {
        "message": "Paper uploaded and processed successfully",
        "hash": paper_hash,
        "subject": subject,
        "extracted_stats": {
            "short_questions": len(short_q),
            "long_questions": len(long_q),
            "mcqs": len(mcqs)
        }
    }
