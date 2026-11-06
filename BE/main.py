
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Video
from schemas import VideoCreate, VideoResponse

app = FastAPI(title="Project Video Short AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/videos", response_model=VideoResponse)
def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    new_video = Video(
        title=video.title,
        description=video.description
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video


@app.get("/videos", response_model=list[VideoResponse])
def get_videos(db: Session = Depends(get_db)):
    return db.query(Video).all()


@app.put("/videos/{video_id}", response_model=VideoResponse)
def update_video(
    video_id: int,
    video: VideoCreate,
    db: Session = Depends(get_db)
):
    db_video = db.query(Video).filter(Video.id == video_id).first()

    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    db_video.title = video.title
    db_video.description = video.description

    db.commit()
    db.refresh(db_video)
    return db_video


@app.delete("/videos/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.id == video_id).first()

    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    db.delete(db_video)
    db.commit()

    return {"message": "Video deleted successfully"}
