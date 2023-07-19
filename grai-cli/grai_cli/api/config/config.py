import typer

from grai_cli.api.config.setup import config_app
from grai_cli.settings.config import BasicAuthSettings, ServerSettingsV1, config
from grai_cli.utilities import utilities
from grai_cli.utilities.styling import GraiColors, default_styler, strip_style
from grai_cli.utilities.validators import (
    host_callback,
    insecure_callback,
    password_callback,
    port_callback,
    username_callback,
    workspace_callback,
)


@config_app.command("init")
def cli_init_config(
    username: str = typer.Option(..., prompt=True, callback=username_callback, prompt_required=True),
    password: str = typer.Option(
        ...,
        prompt=True,
        prompt_required=True,
        hide_input=True,
        confirmation_prompt=True,
        callback=strip_style(password_callback),
    ),
    url: str = typer.Option(
        default=default_styler(config.server.url),
        prompt="Server URL",
        prompt_required=True,
        callback=strip_style(host_callback),
    ),
    workspace: str = typer.Option(
        default=default_styler(config.server.workspace),
        prompt="The Grai workspace for this config",
        prompt_required=True,
        callback=strip_style(workspace_callback),
    ),
):
    """Initialize a new config file

    Args:
        username:  (Default value = typer.Option(..., prompt=True, callback=username_callback, prompt_required=True))
        password:  (Default value = typer.Option(...,prompt=True,prompt_required=True,hide_input=True,confirmation_prompt=True,callback=strip_style(password_callback))
        ):
        url:
        workspace:  (Default value = typer.Option(default=default_styler(config.server.workspace))

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
