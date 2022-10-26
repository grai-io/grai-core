import os
import shelve

from grai_cli.settings.config import config


class GraiCache:
    def __init__(self):
        self.cache_filename = "cache"
        self.cache_file = os.path.join(config.config_dir(), self.cache_filename)

        self.has_init = False

        self.startup()

    @property
    def cache(self):
        return shelve.open(self.cache_file)

    def startup(self):
        with self.cache as cache:
            if "has_init" in cache:
                self.has_init = cache["has_init"]

    def set(self, key, value):
        super().__setattr__(key, value)

        with self.cache as cache:
            cache[key] = value


cache = GraiCache()
