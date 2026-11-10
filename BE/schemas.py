
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class VideoCreate(BaseModel):
    title: str
    description: str = ""


class VideoResponse(VideoCreate):
    id: int
    like_count: int = Field(ge=0)
    comment_count: int = Field(ge=0)
    share_count: int = Field(ge=0)

    model_config = ConfigDict(from_attributes=True)


class LikeResponse(BaseModel):
    user_id: int
    video_id: int

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    parent_id: int | None = None


class CommentResponse(BaseModel):
    id: int
    video_id: int
    user_id: int
    parent_id: int | None
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FollowResponse(BaseModel):
    follower_id: int
    following_id: int

    model_config = ConfigDict(from_attributes=True)


class AiChatLogCreate(BaseModel):
    role: Literal["user", "assistant"]
    message: str = Field(min_length=1, max_length=10000)


class AiChatLogResponse(AiChatLogCreate):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
