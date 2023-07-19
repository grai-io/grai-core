---
sidebar_label: patch
title: grai_client.endpoints.v1.patch
---

## patch\_node\_v1

```python
@patch.register
def patch_node_v1(
    client: ClientV1,
    grai_type: NodeV1,
    options: ClientOptions = ClientOptions()) -> NodeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_node\_spec

```python
@patch.register
def patch_node_spec(
    client: ClientV1,
    grai_type: NodeSpec,
    options: ClientOptions = ClientOptions()) -> NodeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_edge\_v1

```python
@patch.register
def patch_edge_v1(
    client: ClientV1,
    grai_type: EdgeV1,
    options: ClientOptions = ClientOptions()) -> NodeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_edge\_spec

```python
@patch.register
def patch_edge_spec(
    client: ClientV1,
    grai_type: EdgeSpec,
    options: ClientOptions = ClientOptions()) -> EdgeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_sourced\_node\_v1

```python
@patch.register
def patch_sourced_node_v1(
    client: ClientV1,
    grai_type: SourcedNodeV1,
    options: ClientOptions = ClientOptions()
) -> SourcedNodeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_sourced\_node\_spec

```python
@patch.register
def patch_sourced_node_spec(
    client: ClientV1,
    grai_type: SourcedNodeSpec,
    options: ClientOptions = ClientOptions()
) -> SourcedNodeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_sourced\_edge\_v1

```python
@patch.register
def patch_sourced_edge_v1(
    client: ClientV1,
    grai_type: SourcedEdgeV1,
    options: ClientOptions = ClientOptions()
) -> SourcedEdgeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_sourced\_edge\_spec

```python
@patch.register
def patch_sourced_edge_spec(
    client: ClientV1,
    grai_type: SourcedEdgeSpec,
    options: ClientOptions = ClientOptions()
) -> SourcedEdgeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_workspace\_v1

```python
@patch.register
def patch_workspace_v1(client: ClientV1,
                       grai_type: Union[WorkspaceV1, WorkspaceSpec],
                       options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_organisation\_v1

```python
@patch.register
def patch_organisation_v1(client: ClientV1,
                          grai_type: Union[OrganisationV1, OrganisationSpec],
                          options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## patch\_source\_v1

```python
@patch.register
def patch_source_v1(
    client: ClientV1,
    grai_type: SourceV1,
    options: ClientOptions = ClientOptions()) -> SourceV1
```

**Arguments**:

  client (ClientV1):
  grai_type (NodeV1):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## patch\_source\_spec

```python
@patch.register
def patch_source_spec(
    client: ClientV1,
    grai_type: SourceSpec,
    options: ClientOptions = ClientOptions()) -> SourceV1
```

**Arguments**:

  client (ClientV1):
  grai_type (NodeV1):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:
