from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from ..db.models import SubmissionStatus

# This is the data we expect when a user starts a new submission.
# We only need to know which assignment they're working on.
class SubmissionCreate(BaseModel):
    assignment_id: int
    # user_id will be handled by authentication later

# This is the data shape we will return from our API.
class Submission(BaseModel):
    id: int
    assignment_id: int
    status: SubmissionStatus
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)