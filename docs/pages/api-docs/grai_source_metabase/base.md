---
sidebar_label: base
title: grai_source_metabase.base
---

## MetabaseIntegration Objects

```python
class MetabaseIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from Metabase

**Attributes**:

- `connector` - The Metabase connector responsible for communicating with the Metabase API.

### \_\_init\_\_

```python
def __init__(source: SourceV1,
             metabase_namespace: str,
             version: Optional[str] = None,
             namespace_map: Optional[Union[str, Dict[int, str]]] = None,
             endpoint: Optional[str] = None,
             username: Optional[str] = None,
             password: Optional[str] = None)
```

Initializes the Metabase integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `metabase_namespace` - The Grai namespace to associate with Metabase specific lineage like questions and dashboards.
- `namespace_map` - A dictionary mapping Metabase database ids to Grai namespaces
- `endpoint` - The url of your Metabase instance
- `username` - The username to use when authenticating with Metabase
- `password` - The password to use when authenticating with Metabase

### ready

```python
def ready() -> bool
```

Returns True if the integration is ready to run

### nodes

```python
@cache
def nodes() -> List[SourcedNode]
```

Returns a list of SourcedNode objects

### edges

```python
@cache
def edges() -> List[SourcedEdge]
```

Returns a list of SourcedEdge objects

### get\_nodes\_and\_edges

```python
def get_nodes_and_edges() -> Tuple[List[SourcedNode], List[SourcedEdge]]
```

Returns a tuple of lists of SourcedNode and SourcedEdge objects
