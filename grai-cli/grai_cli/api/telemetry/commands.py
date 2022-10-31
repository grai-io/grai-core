import typer

from grai_cli.api.entrypoint import app
from grai_cli.utilities.telemetry import capture


def users_callback():
    print("Running a users command")


telemetry_app = typer.Typer(help="Event Logging Functionality", hidden=True)
app.add_typer(telemetry_app, name="telemetry")


@telemetry_app.command("log")
def log(event: str):
    capture(event)
