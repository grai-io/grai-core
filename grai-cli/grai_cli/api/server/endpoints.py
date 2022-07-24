import typer
from typing import Optional
from pathlib import Path
from grai_cli.api.server.setup import client_app, client_get_app
from grai_cli.api.entrypoint import app
from grai_cli.utilities.styling import default_styler
from grai_cli.utilities.utilities import write_yaml, merge_dicts
from grai_client.schemas.node import NodeType
from grai_client.schemas.edge import EdgeType
from grai_client.schemas.schema import validate_file, Schema, SchemaDispatcher
from grai_cli.api.server.setup import get_default_client
from rich import print as rprint


@client_app.command("is_authenticated", help="Verify auth credentials are valid")
def is_authenticated():
    client = get_default_client()
    authentication_status = client.check_authentication()
    if authentication_status.status_code == 200:
        rprint("Authenticated")
    else:
        rprint(
            f"Failed to Authenticate: Code {authentication_status.status_code}, {authentication_status.content}"
        )


@client_get_app.command('nodes', help=f"Grab active {default_styler('nodes')} from the guide.")
def get_nodes(
    print: bool = typer.Option(True, "--p", help=f"Print nodes to console"),
    to_file: Optional[Path] = typer.Option(None, "--f", help="Write nodes to file"),
):
    obj_type = NodeType()
    client = get_default_client()
    result = client.get(obj_type)

    if print or to_file:
        result = [
            Schema.to_model(item, client.id, obj_type) for item in result
        ]

    if print:
        rprint(result)
    if isinstance(to_file, Path):
        write_yaml(result, to_file)

    return result


@client_get_app.command('edges', help=f"Grab active {default_styler('edges')} from the guide.")
def get_edges(
    print: bool = typer.Option(True, "--p", help=f"Print edges to console"),
    to_file: Optional[Path] = typer.Option(None, "--f", help="Write nodes to file"),
):
    client = get_default_client()
    result = client.get(SchemaDispatcher.edge)

    if print or to_file:
        result = [
            Schema.to_model(item, client.id, SchemaDispatcher.edge) for item in result
        ]

    if print:
        rprint(result)
    if to_file:
        write_yaml(result, to_file)

    return result



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
            rprint(spec)
        typer.Exit()

    for spec in specs:
        records = client.get(spec)
        if (num_records := len(records)) == 0:
            client.post(spec)
        elif num_records == 1:
            record = records[0]
            provided_values = {k: v for k, v in spec.spec.dict().items() if v}
            merge_dicts(record, provided_values)
            client.patch(spec.from_spec(record))
        else:
            message = (
                f"Too many records returned for object {spec}, this is probably a bug. "
                "Please submit a bug report to https://github.com/grai-io/grai-core/issues"
            )
            rprint(message)
            typer.Exit()


@app.command("delete", help="Delete a configuration from The Guide by file name")
def delete(
    file: Path = typer.Argument(...),
    dry_run: bool = typer.Option(False, "--d", help="Dry run of file application"),
):

    # TODO: Edges don't have a human readable unique identifier
    client = get_default_client()
    specs = validate_file(file)
    if dry_run:
        for spec in specs:
            rprint(spec)
        typer.Exit()

    for spec in specs:
        client.delete(spec)
