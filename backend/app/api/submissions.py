from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from ..db import models, database
from ..schemas import submission as submission_schema
from ..services import parser_service
from ..services.evaluation_service import get_ai_feedback

router = APIRouter()

# Dependency to get a DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submissions/", response_model=submission_schema.Submission)
def create_submission(submission: submission_schema.SubmissionCreate, db: Session = Depends(get_db)):
    """
    Creates a new submission record in the database.
    This endpoint is called when a user starts an assignment.
    """
    db_submission = models.Submission(
        assignment_id=submission.assignment_id,
        user_id=1 # Placeholder user_id
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

@router.get("/submissions/{submission_id}", response_model=submission_schema.Submission)
def read_submission(submission_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a specific submission by its ID.
    """
    db_submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if db_submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    return db_submission

@router.post("/{submission_id}/upload")
async def upload_submission_file(submission_id: int, file: UploadFile = File(...)):
    """
    Accepts a file upload, parses its content using the parser_service,
    and associates it with a submission.
    """
    parsed_content = await parser_service.parse_file(file)
    # In a real app, you'd save this parsed_content to the submission record
    return {"filename": file.filename, "content": parsed_content}

@router.post("/{submission_id}/evaluate", status_code=200)
async def evaluate_submission(submission_id: int, db: Session = Depends(get_db)):
    """
    Triggers a final, comprehensive evaluation of a submission
    and saves the result to the database.
    """
    db_submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not db_submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # This is a simplified approach. In a full app, you would save the final code 
    # from the WebSocket session to the database before calling this.
    # For now, we'll use a placeholder.
    final_code = "FUNCTION main() PRINT 'Hello World' END FUNCTION"
    db_submission.final_content = final_code

    feedback_result = await get_ai_feedback(db, submission_id, final_code)

    evaluation = models.EvaluationResult(
        submission_id=submission_id,
        results={"final_feedback": feedback_result, "score": 85} # Placeholder score
    )
    db.add(evaluation)
    
    db_submission.status = models.SubmissionStatus.EVALUATED
    db.commit()

    return {"message": "Evaluation complete and results saved."}