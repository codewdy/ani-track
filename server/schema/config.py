from pydantic import BaseModel
from typing import Dict


class Config(BaseModel):
    resource_dir: Dict[str, str]
    default_dir: str
    web_dir: str
