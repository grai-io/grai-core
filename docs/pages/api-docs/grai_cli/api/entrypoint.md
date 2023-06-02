---
sidebar_label: entrypoint
title: grai_cli.api.entrypoint
---

#### result\_callback

```python
def result_callback(*args, **kwargs)
```

**Arguments**:

  *args:
  **kwargs:


**Returns**:



#### callback

```python
@app.callback()
def callback(ctx: typer.Context,
             telemetry: Optional[bool] = typer.Option(
                 None, show_default=False,
                 help="Enable or disable telemetry"))
```

Grai CLI

**Arguments**:

  ctx (typer.Context):
- `telemetry` _Optional[bool], optional_ - (Default value = typer.Option(None, show_default=False, help=&quot;Enable or disable telemetry&quot;))


**Returns**:
