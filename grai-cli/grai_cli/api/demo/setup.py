import typer

from grai_cli.api.entrypoint import app
from grai_cli.utilities.utilities import default_callback

demo_app = typer.Typer(
    no_args_is_help=True,
    help="Experiment with a demo environment",
    callback=default_callback,
)
app.add_typer(demo_app, name="demo")
