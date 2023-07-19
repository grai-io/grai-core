---
sidebar_label: post
title: grai_client.endpoints.v1.post
---

## collect\_data\_sources

```python
def collect_data_sources(
    data_sources: List[Union[UUID,
                             SourceSpec]]) -> List[Union[Dict, SourceSpec]]
```

**Arguments**:

  data_sources:


**Returns**:



## post\_node\_by\_node\_v1

```python
@post.register
def post_node_by_node_v1(
    client: ClientV1,
    grai_type: NodeV1,
    options: ClientOptions = ClientOptions()) -> NodeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## post\_node\_by\_spec

```python
@post.register
def post_node_by_spec(
    client: ClientV1,
    grai_type: NodeSpec,
    options: ClientOptions = ClientOptions()) -> NodeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## post\_sourced\_node\_v1

```python
@post.register
def post_sourced_node_v1(
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



## post\_sourced\_node\_spec

```python
@post.register
def post_sourced_node_spec(
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



## post\_sourced\_edge\_v1

```python
@post.register
def post_sourced_edge_v1(
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



## post\_sourced\_edge\_spec

```python
@post.register
def post_sourced_edge_spec(
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



## post\_edge\_by\_spec

```python
@post.register
def post_edge_by_spec(
    client: ClientV1,
    grai_type: EdgeSpec,
    options: ClientOptions = ClientOptions()) -> EdgeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## post\_edge\_by\_edge\_v1

```python
@post.register
def post_edge_by_edge_v1(
    client: ClientV1,
    grai_type: EdgeV1,
    options: ClientOptions = ClientOptions()) -> EdgeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## post\_workspace\_v1

```python
@post.register
def post_workspace_v1(
    client: ClientV1,
    grai_type: Union[WorkspaceV1, WorkspaceSpec],
    options: ClientOptions = ClientOptions()
) -> WorkspaceV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## post\_source\_v1

```python
@post.register
def post_source_v1(
    client: ClientV1,
    grai_type: SourceSpec,
    options: ClientOptions = ClientOptions()) -> SourceV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## post\_source\_v1

```python
@post.register
def post_source_v1(
    client: ClientV1,
    grai_type: SourceV1,
    options: ClientOptions = ClientOptions()) -> SourceV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## post\_organisation\_v1

```python
@post.register
def post_organisation_v1(client: ClientV1,
                         grai_type: Union[OrganisationV1, OrganisationSpec],
                         options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:
