---
sidebar_label: source
title: grai_client.endpoints.v1.get.source
---

## get\_all\_sources

```python
@get.register
def get_all_sources(
    client: ClientV1,
    grai_type: SourceLabels,
    options: ClientOptions = ClientOptions()
) -> List[SourceV1]
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_source\_by\_id

```python
@get.register
def get_source_by_id(
    client: ClientV1,
    grai_type: SourceLabels,
    source_id: Union[str, UUID],
    options: ClientOptions = ClientOptions()
) -> SourceV1
```

**Arguments**:

  client:
  grai_type:
  source_id:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_source\_from\_source\_v1

```python
@get.register
def get_source_from_source_v1(
    client: ClientV1,
    grai_type: SourceV1,
    options: ClientOptions = ClientOptions()) -> SourceV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## get\_source\_from\_spec

```python
@get.register
def get_source_from_spec(
    client: ClientV1,
    grai_type: SourceSpec,
    options: ClientOptions = ClientOptions()) -> SourceV1
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:
