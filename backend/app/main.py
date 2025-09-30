from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your database models and engine
from .db import models, database

# Import all of your API routers
from .api import submissions, websockets, rubrics

# This command tells SQLAlchemy to create all the database tables
# based on the models defined in `app/db/models.py`.
# It will only create tables that don't already exist.
models.Base.metadata.create_all(bind=database.engine)

# Initialize the FastAPI application
app = FastAPI(
    title="Neo-Tutor Hackathon API",
    description="API for real-time code evaluation and feedback.",
    version="1.0.0"
)

# --- Middleware ---
# This allows your frontend application to communicate with your backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- API Routers ---
# Include the different parts of your API
app.include_router(submissions.router, prefix="/api", tags=["Submissions"])
app.include_router(websockets.router, prefix="/ws", tags=["WebSockets"])
app.include_router(rubrics.router, prefix="/api", tags=["Rubrics"])

@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Neo-Tutor API!"}