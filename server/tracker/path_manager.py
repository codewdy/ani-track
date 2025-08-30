import pathlib
import enum
from schema.config import Config


class PathType(enum.Enum):
    LocalPath = 1
    WebPath = 2


class PathManager:
    def __init__(self, config: Config, path_type: PathType):
        self.config = config
        self.path_type = path_type

    def resource_path(self, db, animation_id):
        if self.path_type == PathType.LocalPath:
            return pathlib.Path(self.config.resource.dirs[db.animations[animation_id].info.resource_dir])
        else:
            return pathlib.Path(self.config.service.resource_web_path) / db.animations[animation_id].info.resource_dir

    def animation_path(self, db, animation_id):
        return self.resource_path(db, animation_id) / db.animations[animation_id].info.dirname

    def channel_path(self, db, animation_id, channel_id):
        return self.animation_path(db, animation_id) / db.animations[animation_id].channels[channel_id].dirname

    def episode_path(self, db, animation_id, channel_id, episode_id):
        return self.channel_path(db, animation_id, channel_id) / db.animations[animation_id].channels[channel_id].episodes[episode_id].filename
