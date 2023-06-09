import os
import shelve
import uuid
import warnings

import typer

from grai_cli.settings.config import config


class GraiCache:
    """ """

    def __init__(self):
        self.cache_filename = "cache"
        self.cache_file = os.path.join(config.handler.config_dir, self.cache_filename)

        with self.cache as cache:
            self.first_install = cache.get("first_install", True)
            self.run_config_init = cache.get("run_config_init", True)

            self.has_telemetry_alert = cache.get("has_telemetry_alert", False)
            self.telemetry_consent = cache.get("telemetry_consent", True)

            if "telemetry_id" not in cache:
                cache["telemetry_id"] = uuid.uuid4()
            self.telemetry_id = cache["telemetry_id"]

            if self.run_config_init or not config.handler.has_config_file:
                message = (
                    f"No config file found in ({config.handler.config_file}). CLI is operating using default values. "
                    f"You can create a new config file by running `grai config init`."
                )
                typer.echo(message)
                cache["run_config_init"] = False
            self.run_config_init = cache["run_config_init"]

            if not self.has_telemetry_alert:
                message = (
                    f"We use anonymous telemetry data to help us estimate our number of "
                    f"users and identify failure hotspots. You can disable it using the `--no-telemetry` flag"
                )
                typer.echo(message)
                cache["has_telemetry_alert"] = True
            self.has_telemetry_alert = cache["has_telemetry_alert"]

    @property
    def cache(self):
        """ """
        try:
            return shelve.open(self.cache_file)
        except Exception as e:
            message = (
                f"Failed to open the cli cache file located at {self.cache_file}. This sometimes indicates cache"
                f" corruption. We've moved your cache file to {self.cache_file}.bak and replaced it with an empty file."
            )
            warnings.warn(message)
            os.rename(self.cache_file, f"{self.cache_file}.bak")

        return shelve.open(self.cache_file)

    def set(self, key, value):
        """

        Args:
            key:
            value:

        Returns:

        Raises:

        """
        super().__setattr__(key, value)

        with self.cache as cache:
            cache[key] = value

    def get(self, key, default=None):
        """

        Args:
            key:
            default:  (Default value = None)

        Returns:

        Raises:

        """
        with self.cache as cache:
            if default:
                return cache[key]
            else:
                return cache.get(key, default)


cache = GraiCache()
