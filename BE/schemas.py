
from pydantic import BaseModel, ConfigDict


class VideoCreate(BaseModel):
    title: str
    description: str = ""


class VideoResponse(VideoCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
