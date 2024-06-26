---
sidebar_label: base
title: grai_source_dbt_cloud.base
---

## DbtCloudIntegration Objects

```python
class DbtCloudIntegration(EventMixin, GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from the dbt cloud API.

**Attributes**:

- `connector` - The dbt cloud connector responsible for communicating with the dbt cloud api.

### \_\_init\_\_

```python
def __init__(api_key: str,
             source: SourceV1,
             version: Optional[str] = None,
             namespace: Optional[str] = "default")
```

Initializes the dbt cloud integration.

**Arguments**:

- `api_key` - A dbt cloud api key
- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `namespace` - The Grai namespace to associate with output from the integration

### get\_nodes\_and\_edges

```python
@cache
def get_nodes_and_edges() -> Tuple[List[SourcedNode], List[SourcedEdge]]
```

Returns a tuple of lists of SourcedNode and SourcedEdge objects

### nodes

```python
def nodes() -> List[SourcedNode]
```

Returns a list of SourcedNode objects

### edges

```python
def edges() -> List[SourcedEdge]
```

Returns a list of SourcedEdge objects

### events

```python
def events(last_event_date: Optional[str]) -> List[Event]
```

Returns a list of Event objects

### ready

```python
def ready() -> bool
```

Returns True if the integration is ready to run
