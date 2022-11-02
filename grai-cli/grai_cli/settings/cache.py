import os
import shelve
import uuid

from grai_cli.settings.config import config


class GraiCache:
    def __init__(self):
        self.cache_filename = "cache"
        self.cache_file = os.path.join(config.config_dir(), self.cache_filename)

        with self.cache as cache:
            self.first_install = cache.get("first_install", True)
            self.run_config_init = cache.get("run_config_init", True)

            self.has_asked_for_telemetry_consent = cache.get(
                "has_asked_for_telemetry_consent", False
            )
            self.telemetry_consent = cache.get("telemetry_consent", True)

            if "telemetry_id" not in cache:
                cache["telemetry_id"] = uuid.uuid4()
            self.telemetry_id = cache["telemetry_id"]

    @property
    def cache(self):
        return shelve.open(self.cache_file)

    def set(self, key, value):
        super().__setattr__(key, value)

        with self.cache as cache:
            cache[key] = value

    def get(self, key, default=None):
        with self.cache as cache:
            if default:
                return cache[key]
            else:
                return cache.get(key, default)


cache = GraiCache()
