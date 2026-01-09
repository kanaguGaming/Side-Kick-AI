from fastapi import APIRouter
from pydantic import BaseModel
from app.rag import load_lab_manuals, get_relevant_context
from app.llm import get_socratic_response

router = APIRouter()
knowledge_base = load_lab_manuals()

class HelpRequest(BaseModel):
    student_id: str
    code: str
    hypothesis: str

@router.post("/ask-ta")
async def ask_ta(request: HelpRequest):
    try:
        # Search Hugging Face vector DB
        context = get_relevant_context(request.hypothesis, knowledge_base)
        
        # Get response from Hugging Face LLM
        reply = get_socratic_response(request.code, request.hypothesis, context)
        
        return {"status": "success", "reply": reply}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "reply": "Hugging Face is busy. Try again!"}