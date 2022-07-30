import typer

# from grai_cli.utilities.styling import command_styler
from rich.console import Console
from rich.text import Text

from grai_cli.api.entrypoint import app

config_app = typer.Typer(
    no_args_is_help=True, help="Interact with your config settings"
)
app.add_typer(config_app, name="config")


set_app = typer.Typer(
    no_args_is_help=True, help="Set individual elements of your config"
)
config_app.add_typer(set_app, name="set")
