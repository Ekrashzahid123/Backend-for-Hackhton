from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class UploadResponse(BaseModel):
    message: str
    hash: str
    subject: str
    extracted_stats: Dict[str, int]

class GenerateRequest(BaseModel):
    subject: str
    num_mcqs: int = 5
    num_short: int = 5
    num_long: int = 3

class GenerateResponse(BaseModel):
    message: str
    paper: Dict[str, Any]

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
