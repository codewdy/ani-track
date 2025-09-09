import resource
from pydantic import BaseModel
from typing import Dict
from schema.dtype import TimeDelta, to_timedelta


class ResourceConfig(BaseModel):
    dirs: Dict[str, str]
    default: str


class ServiceConfig(BaseModel):
    web_dir: str = ""
    resource_web_path: str = "/resource"
    api_port: int = 8080
    port: int = 8081


class TrackerConfig(BaseModel):
    db_file: str
    save_interval: TimeDelta = to_timedelta("1h")
    check_interval: TimeDelta = to_timedelta("1h")
    update_interval: TimeDelta = to_timedelta("1h")
    untrack_timeout: TimeDelta = to_timedelta("30d")
    max_download_concurrent: int = 5
    tmp_dir: str = "/tmp/ani_track"
    episode_watch_end_ratio: float = 0.9


class Config(BaseModel):
    resource: ResourceConfig
    service: ServiceConfig
    tracker: TrackerConfig
