from functools import wraps
from typing import Callable

import typer

from grai_cli.settings.config import config_handler


def requires_config_decorator(fn: Callable):
    @wraps(fn)
    def inner(*args, **kwargs):
        if not config_handler.has_config_file:
            message = (
                f"No config file found in ({config_handler.config_file}). "
                f"You should create a new config file by running `grai config init`."
            )
            print(message)
            exit()
        return fn(*args, **kwargs)

    return inner


def default_callback(ctx: typer.Context):
    """

    Args:
        ctx (typer.Context):

    Returns:

    Raises:

    """
    ctx.meta.setdefault("command_path", [])
    if ctx.invoked_subcommand is not None:
        ctx.meta["command_path"].append(ctx.invoked_subcommand)


@requires_config_decorator
def requires_config_callback(ctx: typer.Context):
    """Used when we wish to interrupt the callback chain if a config is not initialized

    Args:
        ctx (typer.Context):

    Returns:

    Raises:

    """
    default_callback(ctx)
