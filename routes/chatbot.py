from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_service import handle_chatbot_query

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatbotRequest(BaseModel):
    message: str

class ChatbotResponse(BaseModel):
    reply: str

@router.post("", response_model=ChatbotResponse)
async def chatbot_endpoint(req: ChatbotRequest):
    """
    Chatbot endpoint for customer support.
    Handles system usage and educational queries, rejecting off-topic requests.
    """
    reply = handle_chatbot_query(req.message)
    return ChatbotResponse(reply=reply)
