from pydantic import BaseModel
from schema.db import AnimationInfo, Animation, AnimationStatus
from typing import List, Optional


class AddAnimation:
    class Request(BaseModel):
        name: str
        bangumi_id: str
        icon_url: str
        status: AnimationStatus
        channel_name: str
        channel_search_name: str
        channel_url: str
        channel_source_key: str

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
