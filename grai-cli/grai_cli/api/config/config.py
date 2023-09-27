from functools import partial

import typer
from typing_extensions import Annotated

from grai_cli.api.config.setup import config_app
from grai_cli.settings.config import (
    BasicAuthSettings,
    GraiConfig,
    ServerSettingsV1,
    config,
)
from grai_cli.utilities.styling import GraiColors, default_styler
from grai_cli.utilities.styling import print as print_styled
from grai_cli.utilities.validators import (
    password_callback,
    url_callback,
    username_callback,
    workspace_callback,
)


class InitDefaults:
    config = GraiConfig()

    @classmethod
    def url_default(cls):
        try:
            default_url = cls.config.server.url
        except:
            default_url = "https://app.grai.io"
        return default_styler(default_url)

    @classmethod
    def workspace_default(cls):
        try:
            default_workspace = cls.config.server.workspace
        except:
            default_workspace = "default2"
        return default_styler(default_workspace)


PartialPrompt = partial(typer.Option, prompt=True, prompt_required=True, callback=typer.unstyle)
typer.Argument()


@config_app.command("init")
def cli_init_config(
    username: Annotated[str, PartialPrompt(callback=username_callback)],
    password: Annotated[str, PartialPrompt(hide_input=True, confirmation_prompt=True, callback=password_callback)],
    url: Annotated[str, PartialPrompt(prompt="Server URL", callback=url_callback)] = InitDefaults.url_default(),
    workspace: Annotated[str, PartialPrompt(callback=workspace_callback)] = InitDefaults.workspace_default(),
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

    auth = BasicAuthSettings(username=username, password=password)
    server = ServerSettingsV1(url=url, workspace=workspace)
    config = GraiConfig(auth=auth, server=server)
    config.save()


@config_app.command(help="Print config file location")
def location():
    """View the current config file"""
    print_styled(config.config_location)


@config_app.command(help="Print config to console")
def view():
    """View the current config file"""
    print_styled(config.view())
