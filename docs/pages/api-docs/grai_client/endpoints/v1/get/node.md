---
sidebar_label: node
title: grai_client.endpoints.v1.get.node
---

## get\_node\_by\_label\_v1

```python
@get.register
def get_node_by_label_v1(
    client: ClientV1,
    grai_type: NodeLabels,
    options: ClientOptions = ClientOptions()
) -> List[NodeV1]
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_nodes\_by\_uuid\_str\_id

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

  client:
  grai_type:
  node_uuid:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_node\_v1

```python
@get.register
def get_node_v1(
    client: ClientV1,
    grai_type: NodeV1,
    options: ClientOptions = ClientOptions()) -> NodeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_from\_node\_spec

```python
@get.register
def get_from_node_spec(
    client: ClientV1,
    grai_type: NodeSpec,
    options: ClientOptions = ClientOptions()) -> NodeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_source\_node\_by\_label\_v1

```python
@get.register
def get_source_node_by_label_v1(client: ClientV1,
                                grai_type: SourceNodeLabels,
                                options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_source\_node\_by\_label\_and\_id\_v1

```python
@get.register
def get_source_node_by_label_and_id_v1(
    client: ClientV1,
    grai_type: SourceNodeLabels,
    source_id: Union[str, UUID],
    options: ClientOptions = ClientOptions()
) -> List[SourcedNodeV1]
```

**Arguments**:

  client:
  grai_type:
  source_id:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_source\_node\_by\_source\_node\_v1

```python
@get.register
def get_source_node_by_source_node_v1(
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



## get\_source\_node\_by\_source\_node\_spec

```python
@get.register
def get_source_node_by_source_node_spec(
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
