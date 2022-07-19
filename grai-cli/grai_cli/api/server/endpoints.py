import typer
from typing import Optional
from pathlib import Path
from grai_cli.api.server.setup import client_app, client_get_app
from grai_cli.api.entrypoint import app
from grai_cli.utilities.styling import default_styler
from grai_cli.utilities.utilities import write_yaml

from grai_client.schemas.schema import SchemaGenericTypes, validate_file, Schema
from grai_cli.api.server.setup import get_default_client


@app.command("apply")
def apply(file: Path = typer.Argument(...)):
    result = validate_file(file)


@client_app.command("is_authenticated", help="Verify auth credentials are valid")
def is_authenticated():
    client = get_default_client()
    authentication_status = client.check_authentication()
    if authentication_status.status_code == 200:
        typer.echo("Authenticated")
    else:
        typer.echo(
            f"Failed to Authenticate: Code {authentication_status.status_code}, {authentication_status.content}"
        )


def make_get_endpoint(grai_type):
    @client_get_app.command(
        grai_type.name,
        help=f"Grab active {default_styler(grai_type.name)} from the guide.",
    )
    def inner(
        print: bool = typer.Option(
            True, "--p", help=f"Print {grai_type.name} to console"
        ),
        to_file: Optional[Path] = typer.Option(None, "--f", help="Write nodes to file"),
    ):
        client = get_default_client()
        result = client.get(grai_type)

        if print or to_file:
            result = [
                Schema.to_model(item, client.id, grai_type.type) for item in result
            ]

        if print:
            typer.echo(result)
        if to_file:
            write_yaml(result, to_file)

        return result

    return inner


types = [SchemaGenericTypes.node, SchemaGenericTypes.edge]
for grai_type in types:
    make_get_endpoint(grai_type)


@app.command("apply", help="Apply a configuration to The Guide by file name")
def apply(
    file: Path = typer.Argument(...),
    dry_run: bool = typer.Option(False, "--d", help="Dry run of file application"),
):

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
