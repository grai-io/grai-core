import typer

from grai_cli.api.callbacks import default_callback

demo_app = typer.Typer(
    no_args_is_help=True,
    help="Experiment with a demo environment",
    callback=default_callback,
)
