from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..db import models, database
from ..schemas import rubric as rubric_schema

router = APIRouter()

# Dependency to get a DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/rubrics/", response_model=rubric_schema.Rubric)
def create_rubric(rubric: rubric_schema.RubricCreate, db: Session = Depends(get_db)):
    """
    Creates a new rubric with its criteria for a specific assignment.
    """
    db_rubric = models.Rubric(name=rubric.name, assignment_id=rubric.assignment_id)
    db.add(db_rubric)
    
    for criterion_data in rubric.criteria:
        db_criterion = models.RubricCriterion(**criterion_data.model_dump(), rubric=db_rubric)
        db.add(db_criterion)
        
    db.commit()
    db.refresh(db_rubric)
    return db_rubric

@router.get("/assignments/{assignment_id}/rubric", response_model=rubric_schema.Rubric)
def read_rubric_for_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the rubric for a given assignment.
    """
    db_rubric = db.query(models.Rubric).filter(models.Rubric.assignment_id == assignment_id).first()
    if db_rubric is None:
        raise HTTPException(status_code=404, detail="Rubric not found for this assignment")
    return db_rubric