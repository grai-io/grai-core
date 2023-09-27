from grai_cli import settings, utilities

if settings.cache.cache.first_install:
    settings.cache.cache.set("first_install", False)
    utilities.telemetry.Telemetry.capture("First install")

__version__ = "0.2.2"
