from itertools import tee
from pathlib import Path
from typing import Dict, List, Optional

import typer
from grai_client.schemas.schema import validate_file
from grai_schemas.utilities import merge
from typing_extensions import Annotated

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


def perform_type_query(query_type: str, print: bool = True, to_file: Optional[Path] = None, **kwargs) -> List:
    """

    Args:
        query_type: The type of query to perform (Edge, Node, Workspace, etc...)
        print: Print the search response to the console. Defaults to True.
        to_file:  Path to write the search response to. Does not write by default.
        kwargs: Additional kwargs to pass to the search.
    Returns:

    Raises:

    """
    client = get_default_client()
    result = client.get(query_type, **kwargs)

    if print:
        print_styled(result)
    if isinstance(to_file, Path):
        write_yaml(result, to_file)

    return result


def pairwise(iterable):
    # s -> (s0,s1), (s1,s2), (s2, s3), ...
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def parse_extra_args(args_list: List[str]) -> Dict[str, str]:
    args_dict = {}

    for key, value in pairwise(args_list):
        if not key.startswith("--"):
            message = f"Invalid argument: {key}. Arguments must start with `--`."
            raise typer.BadParameter(message)
        args_dict[key[2:]] = value

    return args_dict


@client_get_app.command("nodes", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def get_nodes_cli(
    ctx: typer.Context,
    name: Optional[Annotated[str, typer.Option(..., "--name", "-n", help="Name of node")]] = None,
    namespace: Optional[Annotated[str, typer.Option(None, "--namespace", "-ns", help="Namespace of node")]] = None,
    print: Annotated[bool, typer.Option(..., "--p", help=f"Print nodes to console")] = True,
    to_file: Optional[Annotated[Path, typer.Option(None, "--f", help="Write nodes to file")]] = None,
):
    """Retrieve nodes from The Guide

    You can pass additional arguments to the search by passing them after a `--` in the command line. For example:

    * grai get nodes --is_active True --name my_node
    * grai get nodes --metadata__grai__node_type Table

    NOTE: Not all request parameters are supported by the REST api. See the documentation for more details.

    Args:
        ctx: Typer context primarily used for passing additional keyword arguments to the search.
        name: The name of the node to retrieve. By default it will not search any specific name.
        namespace:  The namespace of the node to retrieve. By default it will not search and specific namespace.
        print:  Print the search response to the console. Defaults to True.
        to_file: Path to write the search response to. Does not write by default.

    Returns:

    Raises:

    """
    kwargs = parse_extra_args(ctx.args)
    if name is not None:
        kwargs["name"] = name
    if namespace is not None:
        kwargs["namespace"] = namespace
    return perform_type_query("Node", print=print, to_file=to_file, **kwargs)


@client_get_app.command("edges", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def get_edges(
    ctx: typer.Context,
    name: Optional[Annotated[str, typer.Option(..., "--name", "-n", help="Name of edge")]] = None,
    namespace: Optional[Annotated[str, typer.Option(None, "--namespace", "-ns", help="Namespace of edge")]] = None,
    print: Annotated[bool, typer.Option(..., "--p", help=f"Print edges to console")] = True,
    to_file: Optional[Annotated[Path, typer.Option(None, "--f", help="Write edges to file")]] = None,
):
    """Performs a parameterized edge query against the guide.

    Args:
        ctx: Typer context primarily used for passing additional keyword arguments to the search.
        name: The name of the edge to retrieve. By default it will not search any specific name.
        namespace:  The namespace of the edge to retrieve. By default it will not search and specific namespace.
        print:  Print the search response to the console. Defaults to True.
        to_file: Path to write the search response to. Does not write by default.
        **kwargs: Additional kwargs to pass to the search.

    Returns:
        A list of edges matching the specified search query.

    Raises:

    """
    kwargs = parse_extra_args(ctx.args)
    if name is not None:
        kwargs["name"] = name
    if namespace is not None:
        kwargs["namespace"] = namespace
    return perform_type_query("Edge", print=print, to_file=to_file, **kwargs)


@client_get_app.command("workspaces", help=f"Grab active {default_styler('workspaces')} from the guide.")
def get_workspaces(
    ctx: typer.Context,
    name: str = typer.Argument(None),
    print: bool = typer.Option(True, "--p", help=f"Print workspaces to console"),
    to_file: Optional[Path] = typer.Option(None, "--f", help="Write workspaces to file"),
):
    """

    Args:
        ctx: Typer context primarily used for passing additional keyword arguments to the search.
        name (str, optional):  (Default value = typer.Argument(None))
        print (bool, optional):  (Default value = typer.Option(True, "--p", help=f"Print workspaces to console"))
        to_file (Optional[Path], optional):  (Default value = typer.Option(None, "--f", help="Write workspaces to file"))

    Returns:

    Raises:

    """
    kwargs = parse_extra_args(ctx.args)
    if name is not None:
        kwargs["name"] = name
    return perform_type_query("Workspace", print=print, to_file=to_file, **kwargs)


@app.command(help="Apply a configuration to The Guide by file name")
@requires_config_decorator
def apply(
    file: Path = typer.Argument(...),
    dry_run: bool = typer.Option(False, "--d", help="Dry run of file application"),
):
    """Apply a file to The Guide either creating or modifying the associated resource.

    Args:
        file:  yaml file to apply
        dry_run:  Print the resulting yaml to the console without applying it to the guide.

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
        file:  yaml file to delete
        dry_run:  Print the resulting yaml to the console without deleting resources from the guide.

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
