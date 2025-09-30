from pydantic import BaseModel, ConfigDict
from typing import List

# Schema for an individual criterion
class RubricCriterionBase(BaseModel):
    description: str
    points: int

class RubricCriterionCreate(RubricCriterionBase):
    pass

class RubricCriterion(RubricCriterionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Main schema for creating a new rubric
class RubricCreate(BaseModel):
    assignment_id: int
    name: str
    criteria: List[RubricCriterionCreate]

class Rubric(BaseModel):
    id: int
    assignment_id: int
    name: str
    criteria: List[RubricCriterion] = []
    model_config = ConfigDict(from_attributes=True)