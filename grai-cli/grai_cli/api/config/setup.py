import typer
from grai_cli.api.entrypoint import app
from grai_cli.utilities.utilities import default_callback

config_app = typer.Typer(
    no_args_is_help=True,
    help="Interact with your config settings",
    callback=default_callback,
)
app.add_typer(config_app, name="config")


set_app = typer.Typer(
    no_args_is_help=True,
    help="Set individual elements of your config",
    callback=default_callback,
)
config_app.add_typer(set_app, name="set")
