---
sidebar_label: get
title: grai_client.endpoints.v1.get
---

#### get\_node\_by\_label\_v1

```python
@get.register
def get_node_by_label_v1(
    client: ClientV1,
    grai_type: NodeLabels,
    options: ClientOptions = ClientOptions()
) -> List[NodeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (NodeLabels):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_node\_v1

```python
@get.register
def get_node_v1(
    client: ClientV1,
    grai_type: NodeV1,
    options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (NodeV1):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_nodes\_by\_uuid\_str\_id

```python
@get.register
def get_nodes_by_uuid_str_id(
    client: ClientV1,
    grai_type: NodeLabels,
    node_uuid: Union[str, UUID],
    options: ClientOptions = ClientOptions()
) -> NodeV1
```

**Arguments**:

  client (ClientV1):
  grai_type (NodeLabels):
  node_uuid (Union[str, UUID]):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_from\_node\_uuid\_id

```python
@get.register
def get_from_node_uuid_id(
    client: ClientV1,
    grai_type: NodeUuidID,
    options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (NodeUuidID):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_from\_node\_named\_id

```python
@get.register
def get_from_node_named_id(
    client: ClientV1,
    grai_type: NodeNamedID,
    options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (NodeNamedID):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### finalize\_edge

```python
def finalize_edge(
    client: ClientV1, resp: Dict,
    options: ClientOptions = ClientOptions()) -> EdgeV1
```

**Arguments**:

  client (ClientV1):
  resp (Dict):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_edge\_by\_label\_v1

```python
@get.register
def get_edge_by_label_v1(
    client: ClientV1,
    grai_type: EdgeLabels,
    options: ClientOptions = ClientOptions()
) -> List[EdgeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (EdgeLabels):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_edge\_by\_uuid\_str\_id

```python
@get.register
def get_edge_by_uuid_str_id(
    client: ClientV1,
    grai_type: EdgeLabels,
    edge_uuid: Union[str, UUID],
    options: ClientOptions = ClientOptions()
) -> EdgeV1
```

**Arguments**:

  client (ClientV1):
  grai_type (EdgeLabels):
  edge_uuid (Union[str, UUID]):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_edge\_v1

```python
@get.register
def get_edge_v1(
    client: ClientV1,
    grai_type: EdgeV1,
    options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (EdgeV1):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_from\_edge\_uuid\_id

```python
@get.register
def get_from_edge_uuid_id(
    client: ClientV1,
    grai_type: EdgeUuidID,
    options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (EdgeUuidID):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_from\_edge\_named\_id

```python
@get.register
def get_from_edge_named_id(
    client: ClientV1,
    grai_type: EdgeNamedID,
    options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (EdgeNamedID):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_all\_workspaces

```python
@get.register
def get_all_workspaces(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    options: ClientOptions = ClientOptions()
) -> Optional[List[Workspace]]
```

**Arguments**:

  client (ClientV1):
  grai_type (WorkspaceLabels):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



#### get\_workspace\_by\_name\_v1

```python
@get.register
def get_workspace_by_name_v1(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    name: str,
    options: ClientOptions = ClientOptions()) -> Optional[Workspace]
```

**Arguments**:

  client (ClientV1):
  grai_type (WorkspaceLabels):
  name (str):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:
