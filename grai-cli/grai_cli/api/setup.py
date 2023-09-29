from grai_cli.api.config.setup import config_app, set_app
from grai_cli.api.demo.setup import demo_app
from grai_cli.api.entrypoint import app
from grai_cli.api.server.setup import client_app, client_get_app
from grai_cli.api.telemetry.commands import telemetry_app

app.add_typer(config_app, name="config")
app.add_typer(demo_app, name="demo")
app.add_typer(client_app, name="client")
app.add_typer(client_get_app, name="get")
app.add_typer(telemetry_app, name="telemetry")
