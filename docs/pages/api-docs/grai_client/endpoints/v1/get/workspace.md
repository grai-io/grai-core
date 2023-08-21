---
sidebar_label: workspace
title: grai_client.endpoints.v1.get.workspace
---

## get\_workspace\_by\_url

```python
def get_workspace_by_url(
    client: ClientV1, url: str,
    options: ClientOptions = ClientOptions()) -> Response
```

**Arguments**:

  client:
  grai_type:
  url:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_all\_workspaces

```python
@get.register
def get_all_workspaces(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    options: ClientOptions = ClientOptions()
) -> List[WorkspaceV1]
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_workspace\_by\_uuid

```python
@get.register
def get_workspace_by_uuid(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    workspace_id: Union[UUID, str],
    options: ClientOptions = ClientOptions()
) -> WorkspaceV1
```

**Arguments**:

  client:
  grai_type:
  workspace_id:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_workspace\_by\_workspace\_v1

```python
@get.register
def get_workspace_by_workspace_v1(
    client: ClientV1,
    grai_type: WorkspaceV1,
    options: ClientOptions = ClientOptions()
) -> WorkspaceV1
```

**Arguments**:

  client:
  grai_type:
  name:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_workspace\_by\_spec

```python
@get.register
def get_workspace_by_spec(
    client: ClientV1,
    grai_type: WorkspaceSpec,
    options: ClientOptions = ClientOptions()
) -> WorkspaceV1
```

**Arguments**:

  client:
  grai_type:
  name:
- `options` - (Default value = ClientOptions())


**Returns**:
