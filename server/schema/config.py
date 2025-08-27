from pydantic import BaseModel
from typing import Dict


class ResourceConfig(BaseModel):
    dirs: Dict[str, str]
    default: str


class ServiceConfig(BaseModel):
    web_dir: str
    api_port: int
    port: int


class Config(BaseModel):
    resource: ResourceConfig
    service: ServiceConfig
    tmp_dir: str
    db_file: str
