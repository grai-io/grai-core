import typer
from pathlib import Path
from grai_cli.api.server.setup import client_app, client_get_app
from grai_cli.api.server.utilities import get_endpoints, get_endpoint_from_spec
from grai_cli.api.entrypoint import app
from grai_cli.settings.schemas.schema_resolver import validate_file


@app.command('apply')
def apply(file: Path = typer.Argument(...)):
    result = validate_file(file)


@client_app.command('is_authenticated', help="Verify auth credentials are valid")
def is_authenticated():
    server_config = get_endpoints()
    authentication_status = server_config.check_authentication()
    if authentication_status.status_code == 200:
        typer.echo("Authenticated")
    else:
        typer.echo(f"Failed to Authenticate: Code {authentication_status.status_code}, {authentication_status.content}")


@client_get_app.command('nodes')
def get_nodes(print: bool = typer.Option(False, "--p", help="Print nodes to console"),
              to_file: typer.FileTextWrite = typer.Option("--f", help="Write nodes to file")):
    server_config = get_endpoints()
    nodes = server_config.nodes().get()
    if print and to_file:
        typer.echo(nodes)
    elif print:
        typer.echo(nodes)
    elif to_file:
        pass
    return nodes


@app.command('apply')
def apply(file: Path = typer.Argument(...)):
    specs = validate_file(file)
    for spec in specs:
        endpoint = get_endpoint_from_spec(spec)
        result = endpoint().post(spec['spec'])
        typer.echo(spec['spec']['name'])

