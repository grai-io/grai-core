---
sidebar_label: config
title: grai_cli.api.config.config
---

#### cli\_init\_config

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
                        callback=strip_style(password_callback),
                    ),
                    host: str = typer.Option(
                        default=default_styler(config.server.host),
                        prompt="Server host",
                        prompt_required=True,
                        callback=strip_style(host_callback),
                    ),
                    port: str = typer.Option(
                        default=default_styler(config.server.port),
                        prompt="Server port",
                        prompt_required=True,
                        callback=strip_style(port_callback),
                    ),
                    insecure: str = typer.Option(
                        default=default_styler("False"),
                        prompt="Insecure connection (i.e. http)?",
                        prompt_required=True,
                        callback=strip_style(insecure_callback),
                    ),
                    workspace: str = typer.Option(
                        default=default_styler(config.server.workspace),
                        prompt="The Grai workspace for this config",
                        prompt_required=True,
                        callback=strip_style(workspace_callback),
                    ))
```

Initialize a new config file

**Arguments**:

- `username` _str, optional_ - (Default value = typer.Option(..., prompt=True, callback=username_callback, prompt_required=True))
- `password` _str, optional_ - (Default value = typer.Option(...,prompt=True,prompt_required=True,hide_input=True,confirmation_prompt=True,callback=strip_style(password_callback))
  ):
- `host` _str, optional_ - (Default value = typer.Option(default=default_styler(config.server.host))
- `prompt` - (Default value = &quot;The Grai workspace for this config&quot;)
- `prompt_required` - (Default value = True)
- `callback` - (Default value = strip_style(workspace_callback))
- `port` _str, optional_ - (Default value = typer.Option(default=default_styler(config.server.port))
- `insecure` _str, optional_ - (Default value = typer.Option(default=default_styler(&quot;False&quot;))
- `workspace` _str, optional_ - (Default value = typer.Option(default=default_styler(config.server.workspace))


**Returns**:



#### view

```python
@config_app.command(help="Print config to console")
def view()
```

View the current config file
