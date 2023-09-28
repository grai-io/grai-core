from pathlib import Path
from typing import Optional

import typer
from grai_client.schemas.schema import validate_file
from grai_schemas.utilities import merge

from grai_cli.api.callbacks import requires_config_decorator
from grai_cli.api.entrypoint import app
from grai_cli.api.server.setup import client_app, client_get_app, get_default_client
from grai_cli.utilities import utilities
from grai_cli.utilities.styling import default_styler
from grai_cli.utilities.styling import print as print_styled
from grai_cli.utilities.utilities import write_yaml


@client_app.command("is_authenticated", help="Verify auth credentials are valid")
def is_authenticated():
    """ """
    client = get_default_client()
    authentication_status = client.check_authentication()
    if authentication_status.status_code == 200:
        print_styled("Authenticated")
    else:
        print_styled(
            f"Failed to Authenticate: Code {authentication_status.status_code}, {authentication_status.content}"
        )


def get_nodes(print: bool = True, to_file: Optional[Path] = None, **kwargs):
    """

    Args:
        name (Optional[str], optional):  (Default value = None)
        namespace (Optional[str], optional):  (Default value = None)
        print (bool, optional):  (Default value = True)
        to_file (Optional[Path], optional):  (Default value = None)

    Returns:

    Raises:

    """
    client = get_default_client()
    result = client.get("Node", **kwargs)

    if print:
        print_styled(result)
    if isinstance(to_file, Path):
        write_yaml(result, to_file)

    return result


@client_get_app.command("nodes", help=f"Grab active {default_styler('nodes')} from the guide.")
def get_nodes_cli(
    name: Optional[str] = typer.Argument(None),
    namespace: Optional[str] = typer.Option(None, "--namespace", "-n", help="Namespace of node"),
    print: bool = typer.Option(True, "--p", help=f"Print nodes to console"),
    to_file: Optional[Path] = typer.Option(None, "--f", help="Write nodes to file"),
):
    """

    Args:
        name (Optional[str], optional):  (Default value = typer.Argument(None))
        namespace (Optional[str], optional):  (Default value = typer.Option(None, "--namespace", "-n", help="Namespace of node"))
        print (bool, optional):  (Default value = typer.Option(True, "--p", help=f"Print nodes to console"))
        to_file (Optional[Path], optional):  (Default value = typer.Option(None, "--f", help="Write nodes to file"))

    Returns:

    Raises:

    """
    return get_nodes(name=name, namespace=namespace, print=print, to_file=to_file)


@client_get_app.command("edges", help=f"Grab active {default_styler('edges')} from the guide.")
def get_edges(
    print: bool = typer.Option(True, "--p", help=f"Print edges to console"),
    to_file: Optional[Path] = typer.Option(None, "--f", help="Write edges to file"),
):
    """

    Args:
        print (bool, optional):  (Default value = typer.Option(True, "--p", help=f"Print edges to console"))
        to_file (Optional[Path], optional):  (Default value = typer.Option(None, "--f", help="Write edges to file"))

    Returns:

    Raises:

    """
    client = get_default_client()
    breakpoint()
    result = client.get("Edge")

    if print:
        print_styled(result)
    if to_file:
        write_yaml(result, to_file)

    return result


@client_get_app.command("workspaces", help=f"Grab active {default_styler('workspaces')} from the guide.")
def get_workspaces(
    name: str = typer.Argument(None),
    print: bool = typer.Option(True, "--p", help=f"Print workspaces to console"),
    to_file: Optional[Path] = typer.Option(None, "--f", help="Write workspaces to file"),
):
    """

    Args:
        name (str, optional):  (Default value = typer.Argument(None))
        print (bool, optional):  (Default value = typer.Option(True, "--p", help=f"Print workspaces to console"))
        to_file (Optional[Path], optional):  (Default value = typer.Option(None, "--f", help="Write workspaces to file"))

    Returns:

    Raises:

    """
    client = get_default_client()
    if name is None:
        result = client.get("workspaces")
    else:
        result = client.get("workspaces", name=name)

    if print:
        print_styled(result)
    if to_file:
        write_yaml(result, to_file)

    return result


@app.command(help="Apply a configuration to The Guide by file name")
@requires_config_decorator
def apply(
    file: Path = typer.Argument(...),
    dry_run: bool = typer.Option(False, "--d", help="Dry run of file application"),
):
    """

    Args:
        file:  (Default value = typer.Argument(...))
        dry_run:  (Default value = typer.Option(False, "--d", help="Dry run of file application"))

    Returns:

    Raises:

    """

    # TODO: Edges don't have a human readable unique identifier
    client = get_default_client()
    specs = validate_file(file)

    if dry_run:
        for spec in specs:
            print_styled(spec)
        typer.Exit()

    for spec in specs:
        record = None
        try:
            record = client.get(spec)
        except:
            client.post(spec)

        if record is not None:
            updated_record = merge(record, spec)
            client.patch(updated_record)


@app.command("delete", help="Delete a configuration from The Guide by file name")
@requires_config_decorator
def delete(
    file: Path = typer.Argument(...),
    dry_run: bool = typer.Option(False, "--d", help="Dry run of file application"),
):
    """

    Args:
        file (Path, optional):  (Default value = typer.Argument(...))
        dry_run (bool, optional):  (Default value = typer.Option(False, "--d", help="Dry run of file application"))

    Returns:

    Raises:

    """
    from grai_client.schemas.schema import validate_file

    # TODO: Edges don't have a human readable unique identifier
    client = get_default_client()
    specs = validate_file(file)
    if dry_run:
        for spec in specs:
            print_styled(spec)
        typer.Exit()

    for spec in specs:
        client.delete(spec)
