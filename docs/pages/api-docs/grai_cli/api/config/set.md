---
sidebar_label: set
title: grai_cli.api.config.set
---

## setter\_helper

```python
def setter_helper(path: str) -> Callable
```

**Arguments**:

  path (str):


**Returns**:



## \_

```python
@setter_helper("auth.username")
def _(username: str = typer.Argument(..., callback=username_callback))
```

Sets config value for auth.username

**Arguments**:

- `username` _str, optional_ - (Default value = typer.Argument(..., callback=username_callback))


**Returns**:



## \_

```python
@setter_helper("auth.password")
def _(password: str = typer.Option(
    ...,
    hide_input=True,
    callback=password_callback,
    prompt=True,
    prompt_required=True,
    confirmation_prompt=True,
))
```

Sets config value for auth.password

**Arguments**:

- `password` _str, optional_ - (Default value = typer.Option(...,hide_input=True,callback=password_callback,prompt=True,prompt_required=True,confirmation_prompt=True,))


**Returns**:



## \_

```python
@setter_helper("auth.api_key")
def _(api_key: str = typer.Option(
    ...,
    hide_input=True,
    prompt=True,
    prompt_required=True,
    confirmation_prompt=True,
))
```

Sets config value for auth.api_key

**Arguments**:

- `api_key` _str, optional_ - (Default value = typer.Option(...,hide_input=True,prompt=True,prompt_required=True,confirmation_prompt=True,))


**Returns**:



## \_

```python
@setter_helper("server.host")
def _(host: str = typer.Argument(..., callback=host_callback))
```

Sets config value for server.host

**Arguments**:

- `host` _str, optional_ - (Default value = typer.Argument(..., callback=host_callback))


**Returns**:



## \_

```python
@setter_helper("server.port")
def _(port: str = typer.Argument(..., callback=port_callback))
```

Sets config value for server.port

**Arguments**:

- `port` _str, optional_ - (Default value = typer.Argument(..., callback=port_callback))


**Returns**:



## \_

```python
@setter_helper("server.insecure")
def _(insecure: str = typer.Argument(..., callback=insecure_callback))
```

Sets config value for server.insecure

**Arguments**:

- `insecure` _str, optional_ - (Default value = typer.Argument(..., callback=insecure_callback))


**Returns**:



## \_

```python
@setter_helper("server.workspace")
def _(workspace: str = typer.Argument(..., callback=workspace_callback))
```

Sets config value for server.workspace

**Arguments**:

- `workspace` _str, optional_ - (Default value = typer.Argument(..., callback=workspace_callback))


**Returns**:
