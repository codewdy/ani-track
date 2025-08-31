import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List, Dict
from schema.dtype import DateTimeWithTimeZone


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
    search_name: str
    url: str
    source_key: str
    dirname: str
    tracking: bool
    latest_update: DateTimeWithTimeZone
    episodes: List[Episode]


class AnimationStatus(str, Enum):
    Wanted = "wanted"
    Watching = "watching"
    Watched = "watched"
    Dropped = "dropped"


class Animation(BaseModel):
    animation_id: int
    name: str
    bangumi_id: str
    icon_url: str
    resource_dir: str
    dirname: str
    status: AnimationStatus
    channels: Dict[int, Channel]
    next_channel_id: int
    current_channel: int
    watched_episode: int = 0
    watched_episode_time: int = 0
    watched_episode_time_percent: float = 0


class DownloadError(BaseModel):
    animation_id: int
    channel_id: int
    episode_id: int


class AnimationDB(BaseModel):
    animations: Dict[int, Animation] = {}
    next_animation_id: int = 1
    download_errors: List[DownloadError] = []
