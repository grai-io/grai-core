---
sidebar_label: config
title: grai_cli.api.config.config
---

## cli\_init\_config

```python
@config_app.command("init")
def cli_init_config(username: str = typer.Option(...,
                                                 prompt=True,
                                                 callback=username_callback,
                                                 prompt_required=True),
                    password: str = typer.Option(
                        ...,
                        prompt=True,
                        prompt_required=True,
                        hide_input=True,
                        confirmation_prompt=True,
                        callback=typer.unstyle,
                    ),
                    url: str = typer.Option(
                        InitDefaults.url_default,
                        prompt="Server URL",
                        prompt_required=True,
                        callback=typer.unstyle,
                    ),
                    workspace: str = typer.Option(
                        InitDefaults.workspace_default,
                        prompt="The Grai workspace for this config",
                        prompt_required=True,
                        callback=typer.unstyle,
                    ))
```

Initialize a new config file

**Arguments**:

  username:
  password:
  url:
  workspace:


**Returns**:



## view

```python
@config_app.command(help="Print config to console")
def view()
```

View the current config file
