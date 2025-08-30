from pydantic import BaseModel
from typing import Dict
from datetime import timedelta


class ResourceConfig(BaseModel):
    dirs: Dict[str, str]
    default: str


class ServiceConfig(BaseModel):
    web_dir: str = ""
    api_port: int = 8080
    port: int = 8081


class TrackerConfig(BaseModel):
    save_interval: timedelta = timedelta(hours=1)
    check_interval: timedelta = timedelta(hours=1)
    update_interval: timedelta = timedelta(days=1)
    max_download_concurrent: int = 5
    tmp_dir: str = "/tmp/ani_track"


class Config(BaseModel):
    resource: ResourceConfig
    service: ServiceConfig
    tracker: TrackerConfig
    db_file: str
