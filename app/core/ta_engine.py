from app.core.guardrails import clean_response
from app.llm import get_llm_response

async def generate_ta_help(request, context_docs):
    # Construct the Socratic Prompt
    prompt = f"""
    You are a Socratic Lab TA. 
    Context: {context_docs}
    Student Code: {request.code}
    Student Hypothesis: {request.hypothesis}
    
    Instruction: Do NOT provide code. Ask questions to lead them to the answer.
    """
    
    raw_reply = await get_llm_response(prompt)
    return clean_response(raw_reply)