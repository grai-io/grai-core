import typer

from grai_cli.api.config.setup import config_app
from grai_cli.settings.config import BasicAuthSettings, ServerSettingsV1, config
from grai_cli.utilities import utilities
from grai_cli.utilities.styling import GraiColors, default_styler, strip_style
from grai_cli.utilities.validators import (
    host_callback,
    password_callback,
    username_callback,
    workspace_callback,
)


class InitDefaults:
    @staticmethod
    def url_default():
        return default_styler(config.server.url)

    @staticmethod
    def workspace_default():
        return default_styler(config.server.workspace)


@config_app.command("init")
def cli_init_config(
    username: str = typer.Option(..., prompt=True, callback=username_callback, prompt_required=True),
    password: str = typer.Option(
        ...,
        prompt=True,
        prompt_required=True,
        hide_input=True,
        confirmation_prompt=True,
        callback=typer.unstyle,
    ),
    url: str = typer.Option(
        InitDefaults.url_default,
        prompt="Server URL",
        prompt_required=True,
        callback=typer.unstyle,
    ),
    workspace: str = typer.Option(
        InitDefaults.workspace_default,
        prompt="The Grai workspace for this config",
        prompt_required=True,
        callback=typer.unstyle,
    ),
):
    """Initialize a new config file

    Args:
        username:
        password:
        url:
        workspace:

    Returns:

    Raises:

    """
    config.auth = BasicAuthSettings(username=username, password=password)
    config.server = ServerSettingsV1(url=url, workspace=workspace)
    config.save()


@config_app.command(help="Print config to console")
def view():
    """View the current config file"""
    utilities.print(config.view())
