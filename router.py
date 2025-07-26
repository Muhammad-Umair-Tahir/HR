# router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from hr import HR_AI
import asyncio

router = APIRouter()
hr_agent = HR_AI()

class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"

class MessageResponse(BaseModel):
    role:"AI"
    response: str

@router.post("/api/v1/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        response = await hr_agent.generate(request.message, request.session_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
