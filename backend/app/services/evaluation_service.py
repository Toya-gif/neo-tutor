import os
import google.generativeai as genai
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..db import models

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_ai_feedback(db: Session, submission_id: int, code: str) -> str:
    """
    Gets AI feedback based on a dynamic rubric found in the database.
    """
    if not code.strip():
        return "Start typing your pseudocode for feedback..."

    # Find the submission and its associated rubric
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        return "Error: Submission not found."

    rubric = db.query(models.Rubric).filter(models.Rubric.assignment_id == submission.assignment_id).first()
    
    # Format the rubric for the prompt
    rubric_text = "No specific rubric found. Provide general feedback."
    if rubric:
        criteria_list = [f"- {c.description} ({c.points} points)" for c in rubric.criteria]
        rubric_text = "Analyze the code based on the following criteria:\n" + "\n".join(criteria_list)

    prompt = f"""
    You are an expert AI tutor. Your task is to provide real-time feedback on a student's pseudocode.
    
    {rubric_text}

    Provide brief, constructive feedback in one or two sentences based on the code snippet provided.
    
    Code Snippet:
    ---
    {code}
    ---
    """
    
    try:
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error getting feedback from AI."