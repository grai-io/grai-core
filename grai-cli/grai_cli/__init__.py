import subprocess

import apipkg
import posthog
import typer
from grai_cli import api, settings, utilities
from grai_cli.settings.config import config

__version__ = "0.1.5"


def run_first_config_install(cache):
    from grai_cli.settings.config import config

    if not cache.run_config_init or config.has_configfile:
        return

    # TODO: This breaks automated testing. This may be worth coming back to in the future
    # message = f"No config file found in ({config.config_filename}). Would you like to create one now?"
    # install_config = typer.confirm(message)
    #
    # cache.set("run_config_init", False)
    # if install_config:
    #     subprocess.run(["grai", "config", "init"])

    message = f"No config file found in ({config.config_filename}). You can create one by running `grai config init`."
    typer.echo(message)
    cache.set("run_config_init", False)


def run_first_telemetry_consent(cache):

    if cache.has_asked_for_telemetry_consent:
        return

    message = (
        f"We use anonymous telemetry data to help us estimate our number of "
        f"users and identify failure hotspots. You can disable it using the `--no-telemetry` flag"
    )
    typer.echo(message)
    cache.set("has_telemetry_alert", True)


def check_first_install():
    from grai_cli.settings.cache import cache
    from grai_cli.utilities.telemetry import Telemetry

    if not cache.first_install:
        return

    run_first_telemetry_consent(cache)

    run_first_config_install(cache)
    cache.set("first_install", False)
    Telemetry.capture("First install")


def init_command():
    check_first_install()


init_command()
