from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from ..services.evaluation_service import get_ai_feedback
from ..db import database # Import the database

# ... (ConnectionManager class remains the same) ...
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

manager = ConnectionManager()
router = APIRouter()

# Dependency to get a DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.websocket("/feedback/{submission_id}")
async def websocket_endpoint(websocket: WebSocket, submission_id: int, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            code_snippet = await websocket.receive_text()
            
            # Use the new, rubric-aware AI service
            feedback = await get_ai_feedback(db=db, submission_id=submission_id, code=code_snippet)
            
            await websocket.send_text(feedback)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client for submission {submission_id} disconnected.")