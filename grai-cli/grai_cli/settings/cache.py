import os
import shelve
import tempfile
import uuid
import warnings
from functools import cached_property
from tempfile import NamedTemporaryFile
from typing import Optional

import typer
from pydantic import BaseModel

from grai_cli.settings.config import config, config_handler


class GraiCache(BaseModel):
    first_install: bool = True

    @classmethod
    def load_cache(cls, file: Optional[str] = None):
        if file is None:
            file = os.path.join(config_handler.config_dir, "cache")

        try:
            with shelve.open(file) as file_cache:
                result = dict(file_cache)
        except Exception as e:
            message = (
                f"Failed to open the cli cache file located at {file}. This sometimes indicates cache"
                f" corruption. We've moved your cache file to {file}.bak and replaced it with an empty file."
            )
            warnings.warn(message)
            os.rename(file, f"{file}.bak")
            result = {}

        return cls(**result)


class GraiCache:
    """ """

    cache_filename = "cache"

    def __init__(self):
        self.cache_file = os.path.join(config_handler.config_dir, self.cache_filename)

        self.run_config_init = cache.get("run_config_init", True)

        self.has_telemetry_alert = cache.get("has_telemetry_alert", False)
        self.telemetry_consent = cache.get("telemetry_consent", True)

        if "telemetry_id" not in cache:
            cache["telemetry_id"] = uuid.uuid4()

        self.telemetry_id = cache["telemetry_id"]

        if self.run_config_init or not os.path.exists(config_handler.config_file):
            message = (
                f"No config file found in ({config_handler.config_file}). CLI is operating using default values. "
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
    def first_install(self):
        return self.get("first_install", True)

    @property
    @cached_property
    def install_id(self):
        install_id = self.get("telemetry_id", None)
        if install_id is None:
            install_id = uuid.uuid4()
            self.set("telemetry_id", install_id)
        return install_id

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


breakpoint()
cache = GraiCache()
