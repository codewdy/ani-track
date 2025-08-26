from pydantic import BaseModel
from schema.data import AnimationStatus
from datetime import datetime


class AddAnimationRequest(BaseModel):
    name: str
    source_key: str
    channel_url: str


class AddAnimationResponse(BaseModel):
    animation_id: int


class AnimationInfo(BaseModel):
    animation_id: int
    name: str
    status: AnimationStatus
    unwatched_episodes: int
    last_touch_time: datetime


class GetAnimationsResponse(BaseModel):
    animations: List[AnimationInfo]
