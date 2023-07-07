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



## get\_nodes

```python
def get_nodes(name: Optional[str] = None,
              namespace: Optional[str] = None,
              print: bool = True,
              to_file: Optional[Path] = None)
```

**Arguments**:

- `name` _Optional[str], optional_ - (Default value = None)
- `namespace` _Optional[str], optional_ - (Default value = None)
- `print` _bool, optional_ - (Default value = True)
- `to_file` _Optional[Path], optional_ - (Default value = None)


**Returns**:



## get\_nodes\_cli

```python
@client_get_app.command(
    "nodes", help=f"Grab active {default_styler('nodes')} from the guide.")
def get_nodes_cli(
        name: Optional[str] = typer.Argument(None),
        namespace: Optional[str] = typer.Option(None,
                                                "--namespace",
                                                "-n",
                                                help="Namespace of node"),
        print: bool = typer.Option(True, "--p",
                                   help=f"Print nodes to console"),
        to_file: Optional[Path] = typer.Option(None,
                                               "--f",
                                               help="Write nodes to file"))
```

**Arguments**:

- `name` _Optional[str], optional_ - (Default value = typer.Argument(None))
- `namespace` _Optional[str], optional_ - (Default value = typer.Option(None, &quot;--namespace&quot;, &quot;-n&quot;, help=&quot;Namespace of node&quot;))
- `print` _bool, optional_ - (Default value = typer.Option(True, &quot;--p&quot;, help=f&quot;Print nodes to console&quot;))
- `to_file` _Optional[Path], optional_ - (Default value = typer.Option(None, &quot;--f&quot;, help=&quot;Write nodes to file&quot;))


**Returns**:



## get\_edges

```python
@client_get_app.command(
    "edges", help=f"Grab active {default_styler('edges')} from the guide.")
def get_edges(print: bool = typer.Option(True,
                                         "--p",
                                         help=f"Print edges to console"),
              to_file: Optional[Path] = typer.Option(
                  None, "--f", help="Write edges to file"))
```

**Arguments**:

- `print` _bool, optional_ - (Default value = typer.Option(True, &quot;--p&quot;, help=f&quot;Print edges to console&quot;))
- `to_file` _Optional[Path], optional_ - (Default value = typer.Option(None, &quot;--f&quot;, help=&quot;Write edges to file&quot;))


**Returns**:



## get\_workspaces

```python
@client_get_app.command(
    "workspaces",
    help=f"Grab active {default_styler('workspaces')} from the guide.")
def get_workspaces(name: str = typer.Argument(None),
                   print: bool = typer.Option(
                       True, "--p", help=f"Print workspaces to console"),
                   to_file: Optional[Path] = typer.Option(
                       None, "--f", help="Write workspaces to file"))
```

**Arguments**:

- `name` _str, optional_ - (Default value = typer.Argument(None))
- `print` _bool, optional_ - (Default value = typer.Option(True, &quot;--p&quot;, help=f&quot;Print workspaces to console&quot;))
- `to_file` _Optional[Path], optional_ - (Default value = typer.Option(None, &quot;--f&quot;, help=&quot;Write workspaces to file&quot;))


**Returns**:



## apply

```python
@app.command("apply", help="Apply a configuration to The Guide by file name")
def apply(file: Path = typer.Argument(...),
          dry_run: bool = typer.Option(False,
                                       "--d",
                                       help="Dry run of file application"))
```

**Arguments**:

- `file` _Path, optional_ - (Default value = typer.Argument(...))
- `dry_run` _bool, optional_ - (Default value = typer.Option(False, &quot;--d&quot;, help=&quot;Dry run of file application&quot;))


**Returns**:



## delete

```python
@app.command("delete",
             help="Delete a configuration from The Guide by file name")
def delete(file: Path = typer.Argument(...),
           dry_run: bool = typer.Option(False,
                                        "--d",
                                        help="Dry run of file application"))
```

**Arguments**:

- `file` _Path, optional_ - (Default value = typer.Argument(...))
- `dry_run` _bool, optional_ - (Default value = typer.Option(False, &quot;--d&quot;, help=&quot;Dry run of file application&quot;))


**Returns**:
