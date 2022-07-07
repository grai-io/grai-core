import typer
from grai_cli.api.entrypoint import app


config_app = typer.Typer(no_args_is_help=True)
app.add_typer(config_app, name="config")


set_app = typer.Typer(no_args_is_help=True)
config_app.add_typer(set_app, name="set")