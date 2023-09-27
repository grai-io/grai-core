import typer

from grai_cli.api.callbacks import default_callback, requires_config_callback

config_app = typer.Typer(no_args_is_help=True, help="Interact with your config settings", callback=default_callback)


set_app = typer.Typer(
    no_args_is_help=True,
    help="Set individual elements of your config",
    callback=default_callback,
)

config_app.add_typer(set_app, name="set")
