import typer
from pathlib import Path
from grai_cli.api.server.setup import client_app, client_get_app
#from grai_cli.api.server.utilities import get_endpoints, get_endpoint_from_spec
from grai_cli.settings.schemas.schema import SchemaGenericTypes
from grai_cli.api.entrypoint import app
from grai_cli.settings.schemas.schema import validate_file
from grai_cli.utilities.styling import default_styler
from grai_cli.server import get_default_client


@app.command('apply')
def apply(file: Path = typer.Argument(...)):
    result = validate_file(file)


@client_app.command('is_authenticated', help="Verify auth credentials are valid")
def is_authenticated():
    client = get_default_client()
    authentication_status = client.check_authentication()
    if authentication_status.status_code == 200:
        typer.echo("Authenticated")
    else:
        typer.echo(f"Failed to Authenticate: Code {authentication_status.status_code}, {authentication_status.content}")


@client_get_app.command('nodes', help=f"Grab active {default_styler('nodes')} from the guide.")
def get_nodes(print: bool = typer.Option(True, "--p", help="Print nodes to console"),
              to_file: typer.FileTextWrite = typer.Option("--f", help="Write nodes to file")):
    client = get_default_client()
    nodes = client.get(SchemaGenericTypes.node)
    if print and to_file:
        typer.echo(nodes)
    elif print:
        typer.echo(nodes)
    elif to_file:
        pass
    return nodes


@client_get_app.command('edges', help=f"Grab active {default_styler('edges')} from the guide.")
def get_edges(print: bool = typer.Option(True, "--p", help="Print nodes to console"),
              to_file: typer.FileTextWrite = typer.Option("--f", help="Write nodes to file")):
    client = get_default_client()
    nodes = client.get(SchemaGenericTypes.edge)
    if print and to_file:
        typer.echo(nodes)
    elif print:
        typer.echo(nodes)
    elif to_file:
        pass
    return nodes


@app.command('apply', help="Apply a configuration to the guide by file name")
def apply(file: Path = typer.Argument(...),
          dry_run: bool = typer.Option(False, "--d", help="Dry run of file application")):

    # TODO: Edges don't have a human readable unique identifier
    client = get_default_client()
    specs = validate_file(file)
    if dry_run:
        for spec in specs:
            typer.echo(spec)
        typer.Exit()

    specs = validate_file(file)
    for spec in specs:
        client.post(spec)

