import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

# Initialize Groq
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def get_socratic_response(student_code, student_hypothesis, lab_context, history):
    try:
        # The Persona: Friendly Senior Brother / Mentor
        system_prompt = f"""
        IDENTITY:
        You are "SideKick AI", a friendly and calm senior brother figure helping a younger sibling with their programming lab. 
        You are highly encouraging, patient, and use a motivating tone.

        ROLE:
        You are a Socratic TA. You guide the student to the answer by asking thought-provoking questions.
        
        LAB MANUAL CONTEXT: 
        {lab_context}

        BEHAVIORAL RULES:
        1. NO DIRECT SOLUTIONS: Never provide the full fixed code. If you must show code, only show a tiny 1-line conceptual snippet.
        2. ENCOURAGEMENT: Start or end with motivating phrases like "You're on the right track," "Good thinking," or "Almost there, buddy!"
        3. SOCRATIC METHOD: Use the student's HYPOTHESIS to point out a logical gap. Ask 1 or 2 targeted questions.
        4. IDENTIFY LAB: Briefly mention which experiment you think they are doing (e.g., "I see you're working on the Lexical Analyzer...").
        5. TONE: Calm, brotherly, and professional. Avoid sounding like a robotic manual.
        """
        
        # Build the message thread for memory
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add history so he remembers previous encouragement
        for msg in history[-6:]: 
            messages.append({"role": msg["role"], "content": msg["content"]})
            
        # Add the current query
        user_msg = f"STUDENT_CODE:\n{student_code}\n\nSTUDENT_HYPOTHESIS: {student_hypothesis}"
        messages.append({"role": "user", "content": user_msg})

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "Hey there! My brain feels a bit foggy right now. Double-check if the server is running, and let's try again!"