from dataclasses import dataclass
from typing import Any

@dataclass
class DownloadTask:
    sourceKey: str
    url: str
    dst: str
    meta: Any = None
