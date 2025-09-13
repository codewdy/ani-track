from pydantic import BaseModel
from schema.db import AnimationStatus
from typing import List, Optional


__all__ = [
    "AddAnimation",
    "GetAnimations",
    "GetAnimationInfo",
    "GetDownloadManagerStatus",
    "SearchBangumi",
    "SearchChannel",
    "SetWatchStatus",
    "SetWatchedTime",
]


class AddAnimation:
    class Request(BaseModel):
        name: str
        bangumi_id: str
        icon_url: str
        status: AnimationStatus
        channel_name: str
        channel_search_name: str
        channel_url: str
        channel_source_key: str

    class Response(BaseModel):
        animation_id: int


class GetAnimations:
    class AnimationInfo(BaseModel):
        animation_id: int
        name: str
        bangumi_id: str
        icon_url: str
        status: AnimationStatus
        watched_episode: int
        total_episode: int

    class Request(BaseModel):
        version: str

    class Response(BaseModel):
        is_new: bool
        version: str
        animations: List['GetAnimations.AnimationInfo']


class GetAnimationInfo:
    class EpisodeInfo(BaseModel):
        name: str
        url: str

    class Request(BaseModel):
        animation_id: int

    class Response(BaseModel):
        animation_id: int
        name: str
        bangumi_id: str
        icon_url: str
        status: AnimationStatus
        watched_episode: int
        watched_episode_time: float
        episodes: List['GetAnimationInfo.EpisodeInfo']


class GetDownloadManagerStatus:
    class DownloadTask(BaseModel):
        resource_name: str
        status: Optional[str]

    class Request(BaseModel):
        pass

    class Response(BaseModel):
        downloading: List['GetDownloadManagerStatus.DownloadTask']
        pending: List['GetDownloadManagerStatus.DownloadTask']


class SearchBangumi:
    class Request(BaseModel):
        keyword: str

    class Response(BaseModel):
        animations: List['SearchBangumi.AnimationInfo']

    class AnimationInfo(BaseModel):
        id: str
        name: str
        image: str


class SearchChannel:
    class Request(BaseModel):
        keyword: str

    class Response(BaseModel):
        channels: List['SearchChannel.ChannelInfo']
        search_errors: List['SearchChannel.SearchErrorInfo']

    class ChannelInfo(BaseModel):
        name: str
        search_name: str
        url: str
        source_key: str
        episodes: List['SearchChannel.EpisodeInfo']

    class EpisodeInfo(BaseModel):
        name: str
        url: str

    class SearchErrorInfo(BaseModel):
        source: str
        error: str


class SetWatchStatus:
    class Request(BaseModel):
        animation_id: int
        status: AnimationStatus

    class Response(BaseModel):
        pass


class SetWatchedTime:
    class Request(BaseModel):
        animation_id: int
        watched_episode: int
        watched_episode_time: float

    class Response(BaseModel):
        pass
