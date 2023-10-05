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
def _(username: Annotated[str,
                          typer.Argument(..., callback=username_callback)])
```

Sets config value for auth.username

**Arguments**:

- `username` _str, optional_ - (Default value = typer.Argument(..., callback=username_callback))


**Returns**:



## \_

```python
@setter_helper("auth.password")
def _(password: Annotated[
    str,
    typer.Option(
        ...,
        hide_input=True,
        callback=password_callback,
        prompt=True,
        prompt_required=True,
        confirmation_prompt=True,
    ),
])
```

Sets config value for auth.password

**Arguments**:

- `password` _str, optional_ - (Default value = typer.Option(...,hide_input=True,callback=password_callback,prompt=True,prompt_required=True,confirmation_prompt=True,))


**Returns**:



## \_

```python
@setter_helper("auth.api_key")
def _(api_key: Annotated[
    str,
    typer.Option(...,
                 hide_input=True,
                 prompt=True,
                 prompt_required=True,
                 confirmation_prompt=True,
                 callback=api_key_callback),
])
```

Sets config value for auth.api_key

**Arguments**:

- `api_key` - Sets the api_key config in the config file.


**Returns**:



## \_

```python
@setter_helper("server.url")
def _(url: Annotated[str, typer.Argument(..., callback=url_callback)])
```

Sets config value for server.url

**Arguments**:

- `url` - Sets the url config in the config file.


**Returns**:



## \_

```python
@setter_helper("server.workspace")
def _(workspace: Annotated[str,
                           typer.Argument(..., callback=workspace_callback)])
```

Sets config value for server.workspace

**Arguments**:

- `workspace` _str, optional_ - (Default value = typer.Argument(..., callback=workspace_callback))


**Returns**:
