from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional # Add these imports
from app.rag import get_context
from app.llm import get_socratic_response

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class TARequest(BaseModel):
    student_id: str
    code: str
    hypothesis: str
    history: Optional[List[Dict[str, str]]] = [] # NEW: Accept history from frontend

@router.post("/ask-ta")
async def ask_ta(request: TARequest):
    try:
        # 1. Get context from RAG
        context = get_context(f"{request.code} {request.hypothesis}")
        
        # 2. Pass history to the LLM function
        # Even if history is empty, it's now passed as an argument
        reply = get_socratic_response(
            request.code, 
            request.hypothesis, 
            context, 
            request.history
        )
        
        return {"status": "success", "reply": reply}
    except Exception as e:
        # This will help you see exactly what goes wrong in the future
        print(f"Error in ask_ta: {str(e)}")
        return {"status": "error", "reply": "SideKick AI is having a moment. Let's try again!"}