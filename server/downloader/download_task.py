from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class DownloadTask:
    sourceKey: str
    url: str
    dst: str
    retry: int = 1
    retry_interval: float = 60
    timeout: float = 3600
    meta: Any = None
    on_finished: Optional[Callable[[], None]] = None
    on_error: Optional[Callable[[Exception], None]] = None
