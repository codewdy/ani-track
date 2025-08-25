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
    channels: List[Channel]
    current_channel: int
    status: AnimationStatus


class AnimationDB(BaseModel):
    animations: Dict[int, Animation]
    next_id: int


class ResourceConfig(BaseModel):
    root_dir: str
    sub_dirs: List[str]
    current_sub_dir: str


class Config(BaseModel):
    tmp_dir: str
    resource: ResourceConfig
    animationdb: str
