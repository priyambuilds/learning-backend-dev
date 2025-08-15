from datetime import datetime
import uuid

from fastapi import APIRouter, BackgroundTasks, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from backend.db.database import SessionLocal, get_db
from backend.models.job import StoryJob
from backend.models.story import Story, StoryNode
from backend.schemas.job import StoryJobResponse
from backend.schemas.story import (
    CompleteStoryNodeResponse,
    CompleteStoryResponse,
    CreateStoryRequest,
)

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

def get_session_id(session_id: str | None = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post(path="/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id = job_id,
        session_id = session_id,
        theme = request.theme,
        status = "pending"
    )
    db.add(job)
    db.commit()

    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )

    return job

def generate_story_task(job_id:str, theme:str, session_id:str):
    db = SessionLocal()

    try:
        job = db.query(Story.job).filter(StoryJob.job_id == job_id).first()

        if not job:
            return

        try:
            job.status = "processing"
            db.commit()

            story = {}

            job.story_id = 1
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()

        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()

    finally:
        db.close()


@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db:Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    complete_story = build_complete_story_tree(db, story)
    return complete_story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    pass
