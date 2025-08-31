import pathlib
import enum
from schema.config import Config


class PathManager:
    def __init__(self, config: Config):
        self.config = config

    def resource_path(self, db, animation_id):
        return pathlib.Path(self.config.resource.dirs[db.animations[animation_id].resource_dir])

    def animation_path(self, db, animation_id):
        return self.resource_path(db, animation_id) / db.animations[animation_id].dirname

    def channel_path(self, db, animation_id, channel_id):
        return self.animation_path(db, animation_id) / db.animations[animation_id].channels[channel_id].dirname

    def episode_path(self, db, animation_id, channel_id, episode_id):
        return (self.channel_path(db, animation_id, channel_id) /
                db.animations[animation_id].channels[channel_id].episodes[episode_id].filename)

    def episode_web_path(self, db, animation_id, channel_id, episode_id):
        return (pathlib.Path(self.config.service.resource_web_path) / db.animations[animation_id].resource_dir /
                db.animations[animation_id].dirname / db.animations[animation_id].channels[channel_id].dirname /
                db.animations[animation_id].channels[channel_id].episodes[episode_id].filename)

    def resource_name(self, db, animation_id, channel_id, episode_id):
        return f"{db.animations[animation_id].name} - {db.animations[animation_id].channels[channel_id].name}" +\
            f" - {db.animations[animation_id].channels[channel_id].episodes[episode_id].name}"
