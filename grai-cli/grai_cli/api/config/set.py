from functools import wraps
from typing import Callable

import typer

from grai_cli.api.config.setup import set_app
from grai_cli.settings.config import config
from grai_cli.utilities.validators import (
    host_callback,
    insecure_callback,
    password_callback,
    port_callback,
    username_callback,
    workspace_callback,
)


def setter_helper(path: str) -> Callable:
    path_elems = path.split(".")
    name = path_elems[-1]

    def set_function_maker(fn: Callable) -> Callable:
        @set_app.command(name)
        @wraps(fn)
        def set_function(*args, **kwargs):
            item = config
            for sub_path in path_elems[:-1]:
                item = getattr(item, sub_path)
            setattr(item, name, kwargs.pop(name))
            config.save()

        return set_function

    return set_function_maker


@setter_helper("auth.username")
def _(username: str = typer.Argument(..., callback=username_callback)):
    """Sets config value for auth.username"""
    pass


@setter_helper("auth.password")
def _(
    password: str = typer.Option(
        ...,
        hide_input=True,
        callback=password_callback,
        prompt=True,
        prompt_required=True,
        confirmation_prompt=True,
    )
):
    """Sets config value for auth.password"""
    pass


@setter_helper("auth.api_key")
def _(
    api_key: str = typer.Option(
        ...,
        hide_input=True,
        prompt=True,
        prompt_required=True,
        confirmation_prompt=True,
    )
):
    """Sets config value for auth.api_key"""
    pass


@setter_helper("server.host")
def _(host: str = typer.Argument(..., callback=host_callback)):
    """Sets config value for server.host"""
    pass


@setter_helper("server.port")
def _(port: str = typer.Argument(..., callback=port_callback)):
    """Sets config value for server.port"""
    pass


@setter_helper("server.insecure")
def _(insecure: str = typer.Argument(..., callback=insecure_callback)):
    """Sets config value for server.insecure"""
    pass


@setter_helper("server.workspace")
def _(workspace: str = typer.Argument(..., callback=workspace_callback)):
    """Sets config value for server.workspace"""
    pass
