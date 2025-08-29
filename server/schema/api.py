from pydantic import BaseModel
from schema.data import AnimationInfo, Animation, AnimationStatus
from datetime import datetime
from typing import List


class AddAnimation:
    class Request(BaseModel):
        name: str
        source_key: str
        channel_url: str

    class Response(BaseModel):
        animation_id: int


class GetAnimations:
    class Request(BaseModel):
        pass

    class Response(BaseModel):
        animations: List[AnimationInfo]


class GetAnimation:
    class Request(BaseModel):
        animation_id: int

    class Response(BaseModel):
        animation: Animation


class UpdateAnimation:
    class Request(BaseModel):
        animation_id: int
        status: Optional[AnimationStatus] = None
        watched_episode: Optional[int] = None
        watched_episode_time: Optional[int] = None

    class Response(BaseModel):
        pass
