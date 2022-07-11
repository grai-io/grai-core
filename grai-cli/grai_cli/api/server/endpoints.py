import typer
from grai_cli.api.server.setup import client_app
from grai_cli.api.server.utilities import GraiV1Endpoints


@client_app.command('is_authenticated')
def is_authenticated():
    server_config = GraiV1Endpoints()
    authentication_status = server_config.check_authentication()
    if authentication_status.status_code == 200:
        typer.echo("Authenticated")
    else:
        typer.echo(f"Failed to Authenticate: Code {authentication_status.status_code}, {authentication_status.content}")