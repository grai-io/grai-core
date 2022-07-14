from grai_cli.api.config.setup import set_app
import yaml
import typer
from typing import Callable
from grai_cli.api.config.setup import config_app
from grai_cli import config
from grai_cli.utilities.styling import default_styler
from grai_cli.utilities.validators import username_callback, password_callback, host_callback, port_callback
from grai_cli.utilities.utilities import writes_config, get_config_view
from functools import wraps


def setter_helper(path: str):
    name = path.split('.')[-1]

    def set_function_maker(fn: Callable):
        @set_app.command(name)
        @writes_config
        @wraps(fn)
        def set_function(*args, **kwargs):
            view = get_config_view(path)
            view.set(kwargs.pop(name))
        return set_function
    return set_function_maker


@setter_helper('auth.username')
def _(username: str = typer.Argument(..., callback=username_callback)):
    """ Sets config value for auth.username"""
    pass


@setter_helper('auth.password')
def _(password: str =typer.Option(..., hide_input=True, callback=password_callback, prompt=True, prompt_required=True, confirmation_prompt=True)):
    """ Sets config value for auth.password"""
    pass


@setter_helper('auth.api_key')
def _(api_key: str =typer.Option(..., hide_input=True, prompt=True, prompt_required=True, confirmation_prompt=True)):
    """ Sets config value for auth.api_key"""
    pass


@setter_helper('auth.token')
def _(token: str =typer.Option(..., hide_input=True, prompt=True, prompt_required=True, confirmation_prompt=True)):
    """ Sets config value for auth.token"""
    pass


@setter_helper('server.host')
def _(host: str = typer.Argument(..., callback=host_callback)):
    """ Sets config value for server.host"""
    pass


@setter_helper('server.port')
def _(port: str = typer.Argument(..., callback=port_callback)):
    """ Sets config value for server.port"""
    pass


@setter_helper('context.namespace')
def _(namespace: str = typer.Argument(...)):
    """ Sets config value for context.namespace"""
    pass
