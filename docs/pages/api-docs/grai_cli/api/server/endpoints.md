---
sidebar_label: endpoints
title: grai_cli.api.server.endpoints
---

## is\_authenticated

```python
@client_app.command("is_authenticated",
                    help="Verify auth credentials are valid")
def is_authenticated()
```



## perform\_type\_query

```python
def perform_type_query(query_type: str,
                       print: bool = True,
                       to_file: Optional[Path] = None,
                       **kwargs) -> List
```

**Arguments**:

- `query_type` - The type of query to perform (Edge, Node, Workspace, etc...)
- `print` - Print the search response to the console. Defaults to True.
- `to_file` - Path to write the search response to. Does not write by default.
- `kwargs` - Additional kwargs to pass to the search.

**Returns**:



## get\_nodes\_cli

```python
@client_get_app.command("nodes",
                        context_settings={
                            "allow_extra_args": True,
                            "ignore_unknown_options": True
                        })
def get_nodes_cli(
    ctx: typer.Context,
    name: Optional[Annotated[
        str, typer.Option(..., "--name", "-n", help="Name of node")]] = None,
    namespace: Optional[Annotated[
        str,
        typer.Option(None, "--namespace", "-ns", help="Namespace of node"
                     )]] = None,
    print: Annotated[
        bool, typer.Option(..., "--p", help=f"Print nodes to console")] = True,
    to_file: Optional[Annotated[
        Path, typer.Option(None, "--f", help="Write nodes to file")]] = None)
```

Retrieve nodes from The Guide

You can pass additional arguments to the search by passing them after a `--` in the command line. For example:

* grai get nodes --is_active True --name my_node
* grai get nodes --metadata__grai__node_type Table

NOTE: Not all request parameters are supported by the REST api. See the documentation for more details.

**Arguments**:

- `ctx` - Typer context primarily used for passing additional keyword arguments to the search.
- `name` - The name of the node to retrieve. By default it will not search any specific name.
- `namespace` - The namespace of the node to retrieve. By default it will not search and specific namespace.
- `print` - Print the search response to the console. Defaults to True.
- `to_file` - Path to write the search response to. Does not write by default.


**Returns**:



## get\_edges

```python
@client_get_app.command("edges",
                        context_settings={
                            "allow_extra_args": True,
                            "ignore_unknown_options": True
                        })
def get_edges(
    ctx: typer.Context,
    name: Optional[Annotated[
        str, typer.Option(..., "--name", "-n", help="Name of edge")]] = None,
    namespace: Optional[Annotated[
        str,
        typer.Option(None, "--namespace", "-ns", help="Namespace of edge"
                     )]] = None,
    print: Annotated[
        bool, typer.Option(..., "--p", help=f"Print edges to console")] = True,
    to_file: Optional[Annotated[
        Path, typer.Option(None, "--f", help="Write edges to file")]] = None)
```

Performs a parameterized edge query against the guide.

**Arguments**:

- `ctx` - Typer context primarily used for passing additional keyword arguments to the search.
- `name` - The name of the edge to retrieve. By default it will not search any specific name.
- `namespace` - The namespace of the edge to retrieve. By default it will not search and specific namespace.
- `print` - Print the search response to the console. Defaults to True.
- `to_file` - Path to write the search response to. Does not write by default.
- `**kwargs` - Additional kwargs to pass to the search.


**Returns**:

  A list of edges matching the specified search query.


## get\_workspaces

```python
@client_get_app.command(
    "workspaces",
    help=f"Grab active {default_styler('workspaces')} from the guide.")
def get_workspaces(
    ctx: typer.Context,
    name: str = typer.Argument(None),
    print: bool = typer.Option(True,
                               "--p",
                               help=f"Print workspaces to console"),
    to_file: Optional[Path] = typer.Option(None,
                                           "--f",
                                           help="Write workspaces to file"))
```

**Arguments**:

- `ctx` - Typer context primarily used for passing additional keyword arguments to the search.
- `name` _str, optional_ - (Default value = typer.Argument(None))
- `print` _bool, optional_ - (Default value = typer.Option(True, &quot;--p&quot;, help=f&quot;Print workspaces to console&quot;))
- `to_file` _Optional[Path], optional_ - (Default value = typer.Option(None, &quot;--f&quot;, help=&quot;Write workspaces to file&quot;))


**Returns**:



## apply

```python
@app.command(help="Apply a configuration to The Guide by file name")
@requires_config_decorator
def apply(file: Path = typer.Argument(...),
          dry_run: bool = typer.Option(False,
                                       "--d",
                                       help="Dry run of file application"))
```

Apply a file to The Guide either creating or modifying the associated resource.

**Arguments**:

- `file` - yaml file to apply
- `dry_run` - Print the resulting yaml to the console without applying it to the guide.


**Returns**:



## delete

```python
@app.command("delete",
             help="Delete a configuration from The Guide by file name")
@requires_config_decorator
def delete(file: Path = typer.Argument(...),
           dry_run: bool = typer.Option(False,
                                        "--d",
                                        help="Dry run of file application"))
```

**Arguments**:

- `file` - yaml file to delete
- `dry_run` - Print the resulting yaml to the console without deleting resources from the guide.


**Returns**:
