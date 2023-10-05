---
sidebar_label: callbacks
title: grai_cli.api.callbacks
---

## default\_callback

```python
def default_callback(ctx: typer.Context)
```

**Arguments**:

  ctx (typer.Context):


**Returns**:



## requires\_config\_callback

```python
@requires_config_decorator
def requires_config_callback(ctx: typer.Context)
```

Used when we wish to interrupt the callback chain if a config is not initialized

**Arguments**:

  ctx (typer.Context):


**Returns**:
