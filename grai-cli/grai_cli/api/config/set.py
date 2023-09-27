from functools import wraps
from typing import Annotated, Callable

import typer

from grai_cli.api.config.setup import set_app
from grai_cli.settings.config import config
from grai_cli.utilities.validators import (
    api_key_callback,
    password_callback,
    url_callback,
    username_callback,
    workspace_callback,
)


def setter_helper(path: str) -> Callable:
    """

    Args:
        path (str):

    Returns:

    Raises:

    """
    path_elems = path.split(".")
    name = path_elems[-1]

    def set_function_maker(fn: Callable) -> Callable:
        """

        Args:
            fn (Callable):

        Returns:

        Raises:

        """

        @set_app.command(name)
        @wraps(fn)
        def set_function(*args, **kwargs):
            """

            Args:
                *args:
                **kwargs:

            Returns:

            Raises:

            """
            item = config
            for sub_path in path_elems[:-1]:
                item = getattr(item, sub_path)
            setattr(item, name, kwargs.pop(name))
            config.save()

        return set_function

    return set_function_maker


@setter_helper("auth.username")
def _(username: Annotated[str, typer.Argument(..., callback=username_callback)]):
    """Sets config value for auth.username

    Args:
        username (str, optional):  (Default value = typer.Argument(..., callback=username_callback))

    Returns:

    Raises:

    """
    pass


@setter_helper("auth.password")
def _(
    password: Annotated[
        str,
        typer.Option(
            ...,
            hide_input=True,
            callback=password_callback,
            prompt=True,
            prompt_required=True,
            confirmation_prompt=True,
        ),
    ]
):
    """Sets config value for auth.password

    Args:
        password (str, optional):  (Default value = typer.Option(...,hide_input=True,callback=password_callback,prompt=True,prompt_required=True,confirmation_prompt=True,))

    Returns:

    Raises:

    """
    pass


@setter_helper("auth.api_key")
def _(
    api_key: Annotated[
        str,
        typer.Option(
            ..., hide_input=True, prompt=True, prompt_required=True, confirmation_prompt=True, callback=api_key_callback
        ),
    ]
):
    """Sets config value for auth.api_key

    Args:
        api_key: Sets the api_key config in the config file.

    Returns:

    Raises:

    """
    pass


@setter_helper("server.url")
def _(url: Annotated[str, typer.Argument(..., callback=url_callback)]):
    """Sets config value for server.url

    Args:
        url: Sets the url config in the config file.

    Returns:

    Raises:

    """
    pass


@setter_helper("server.workspace")
def _(workspace: Annotated[str, typer.Argument(..., callback=workspace_callback)]):
    """Sets config value for server.workspace

    Args:
        workspace (str, optional):  (Default value = typer.Argument(..., callback=workspace_callback))

    Returns:

    Raises:

    """
    pass
