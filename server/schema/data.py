import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List, Dict
from datetime import datetime


class DownloadStatus(Enum):
    Running = "running"
    Finished = "finished"
    Failed = "failed"


class Episode(BaseModel):
    name: str
    url: str
    filename: str
    download_status: DownloadStatus
    download_error: Optional[str] = None


class Channel(BaseModel):
    name: str
    url: str
    source_key: str
    dirname: str
    episodes: List[Episode]
    tracking: bool
    latest_update: datetime


class AnimationStatus(str, Enum):
    Wanted = "wanted"
    Watching = "watching"
    Watched = "watched"
    Dropped = "dropped"


class Animation(BaseModel):
    name: str
    dirname: str
    resource_dir: str
    channels: Dict[int, Channel]
    next_channel_id: int
    current_channel: int
    status: AnimationStatus


class DownloadError(BaseModel):
    animation_id: int
    channel_id: int
    episode_id: int


class AnimationDB(BaseModel):
    animations: Dict[int, Animation]
    next_animation_id: int
    download_errors: List[DownloadError]
