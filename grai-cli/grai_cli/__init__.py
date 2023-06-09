from grai_cli import api, settings, utilities
from grai_cli.settings.config import config

if settings.cache.cache.first_install:
    if settings.cache.cache.first_install:
        settings.cache.cache.set("first_install", False)
        utilities.telemetry.Telemetry.capture("First install")


__version__ = "0.1.13"
