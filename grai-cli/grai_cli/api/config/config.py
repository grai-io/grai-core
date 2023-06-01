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
    host: str = typer.Option(
        default=default_styler(config.server.host),
        prompt="Server host",
        prompt_required=True,
        callback=strip_style(host_callback),
    ),
    port: str = typer.Option(
        default=default_styler(config.server.port),
        prompt="Server port",
        prompt_required=True,
        callback=strip_style(port_callback),
    ),
    insecure: str = typer.Option(
        default=default_styler("False"),
        prompt="Insecure connection (i.e. http)?",
        prompt_required=True,
        callback=strip_style(insecure_callback),
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
        username (str, optional):  (Default value = typer.Option(..., prompt=True, callback=username_callback, prompt_required=True))
        password (str, optional):  (Default value = typer.Option(...,prompt=True,prompt_required=True,hide_input=True,confirmation_prompt=True,callback=strip_style(password_callback))
        ):
        host (str, optional):  (Default value = typer.Option(default=default_styler(config.server.host))
        prompt:  (Default value = "The Grai workspace for this config")
        prompt_required:  (Default value = True)
        callback:  (Default value = strip_style(workspace_callback))
        port (str, optional):  (Default value = typer.Option(default=default_styler(config.server.port))
        insecure (str, optional):  (Default value = typer.Option(default=default_styler("False"))
        workspace (str, optional):  (Default value = typer.Option(default=default_styler(config.server.workspace))

    Returns:

    Raises:

    """
    config.auth = BasicAuthSettings(username=username, password=password)
    config.server = ServerSettingsV1(host=host, port=port, insecure=insecure, workspace=workspace)
    config.save()


@config_app.command(help="Print config to console")
def view():
    """View the current config file"""
    utilities.print(config.view())
