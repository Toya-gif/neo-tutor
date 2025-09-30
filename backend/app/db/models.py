import enum
from sqlalchemy import (Column, Integer, String, Text, ForeignKey, DateTime, JSON, Enum)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class SubmissionStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EVALUATED = "evaluated"
    ERROR = "error"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    # ... other user fields like email, hashed_password

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(Text)

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.IN_PROGRESS)
    final_content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    evaluation = relationship("EvaluationResult", back_populates="submission", uselist=False)
    snapshots = relationship("SubmissionSnapshot", back_populates="submission")
    assignment = relationship("Assignment")

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    results = Column(JSON, nullable=False)
    
    submission = relationship("Submission", back_populates="evaluation")

class SubmissionSnapshot(Base):
    __tablename__ = "submission_snapshots"
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    content_snapshot = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    submission = relationship("Submission", back_populates="snapshots")

class Rubric(Base):
    __tablename__ = "rubrics"
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    name = Column(String, default="Default Rubric")

    criteria = relationship("RubricCriterion", back_populates="rubric", cascade="all, delete-orphan")
    assignment = relationship("Assignment")

class RubricCriterion(Base):
    __tablename__ = "rubric_criteria"
    id = Column(Integer, primary_key=True)
    rubric_id = Column(Integer, ForeignKey("rubrics.id"))
    description = Column(Text, nullable=False)
    points = Column(Integer, nullable=False)

    rubric = relationship("Rubric", back_populates="criteria")