---
sidebar_label: config
title: grai_cli.api.config.config
---

## cli\_init\_config

```python
@config_app.command("init")
def cli_init_config(
    username: Annotated[str, PartialPrompt(callback=username_callback)],
    password: Annotated[str,
                        PartialPrompt(hide_input=True,
                                      confirmation_prompt=True,
                                      callback=password_callback)],
    url: Annotated[str,
                   PartialPrompt(prompt="Server URL", callback=url_callback
                                 )] = InitDefaults.url_default(),
    workspace: Annotated[str, PartialPrompt(
        callback=workspace_callback)] = InitDefaults.workspace_default())
```

Initialize a new config file

**Arguments**:

  username:
  password:
  url:
  workspace:


**Returns**:



## location

```python
@config_app.command(help="Print config file location")
def location()
```

View the current config file

## view

```python
@config_app.command(help="Print config to console")
def view()
```

View the current config file
