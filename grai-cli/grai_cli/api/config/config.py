import typer
from rich import print as rprint

from grai_cli.api.config.setup import config_app
from grai_cli.settings.config import config
from grai_cli.utilities.styling import GraiColors, default_styler, strip_style
from grai_cli.utilities.utilities import writes_config
from grai_cli.utilities.validators import (
    host_callback,
    password_callback,
    port_callback,
    username_callback,
)


@config_app.command("init")
@writes_config
def cli_init_config(
    username: str = typer.Option(
        ..., prompt=True, callback=username_callback, prompt_required=True
    ),
    password: str = typer.Option(
        ...,
        prompt=True,
        prompt_required=True,
        hide_input=True,
        confirmation_prompt=True,
        callback=strip_style(password_callback),
    ),
    host: str = typer.Option(
        default=default_styler(config["server"]["host"].get(str)),
        prompt="Server host",
        prompt_required=True,
        callback=strip_style(host_callback),
    ),
    port: str = typer.Option(
        default=default_styler(config["server"]["port"].get(str)),
        prompt="Server port",
        prompt_required=True,
        callback=strip_style(port_callback),
    ),
    # config_location: str = typer.Option(
    #     default=default_styler(config.config_filename),
    #     prompt="Config path",
    #     prompt_required=True,
    #     callback=strip_style(lambda x: x),
    # ),
):
    """Initialize a new config file"""
    config["auth"]["username"].set(username)
    config["auth"]["password"].set(password)
    config["server"]["host"].set(host)
    config["server"]["port"].set(port)


@config_app.command(help="Print config to console")
def view():
    """Initialize a new config file"""
    rprint(config.view())
