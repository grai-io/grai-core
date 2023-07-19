---
sidebar_label: edge
title: grai_client.endpoints.v1.get.edge
---

## finalize\_edge

```python
def finalize_edge(
    client: ClientV1, resp: Dict,
    options: ClientOptions = ClientOptions()) -> Dict
```

**Arguments**:

  client:
  resp:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_edge\_by\_label\_v1

```python
@get.register
def get_edge_by_label_v1(
    client: ClientV1,
    grai_type: EdgeLabels,
    options: ClientOptions = ClientOptions()
) -> List[EdgeV1]
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_edge\_by\_uuid\_str\_id

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

  client:
  grai_type:
  edge_uuid:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_edge\_v1

```python
@get.register
def get_edge_v1(
    client: ClientV1,
    grai_type: EdgeV1,
    options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_from\_edge\_uuid\_id

```python
@get.register
def get_from_edge_uuid_id(
    client: ClientV1,
    grai_type: EdgeUuidID,
    options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_from\_edge\_named\_id

```python
@get.register
def get_from_edge_named_id(
    client: ClientV1,
    grai_type: EdgeNamedID,
    options: ClientOptions = ClientOptions()) -> EdgeV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_source\_edge\_by\_label\_v1

```python
@get.register
def get_source_edge_by_label_v1(client: ClientV1,
                                grai_type: SourceEdgeLabels,
                                options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_source\_edge\_by\_label\_and\_id\_v1

```python
@get.register
def get_source_edge_by_label_and_id_v1(
    client: ClientV1,
    grai_type: SourceEdgeLabels,
    source_id: Union[str, UUID],
    options: ClientOptions = ClientOptions()
) -> List[SourcedEdgeV1]
```

**Arguments**:

  client:
  grai_type:
  source_id:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_source\_edge\_by\_source\_edge\_v1

```python
@get.register
def get_source_edge_by_source_edge_v1(
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



## get\_source\_edge\_by\_source\_edge\_spec

```python
@get.register
def get_source_edge_by_source_edge_spec(
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
