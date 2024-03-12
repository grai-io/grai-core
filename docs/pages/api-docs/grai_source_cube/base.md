---
sidebar_label: base
title: grai_source_cube.base
---

## CubeIntegration Objects

```python
class CubeIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from the Cube.dev REST API

### \_\_init\_\_

```python
def __init__(source: Union[SourceV1, SourceSpec],
             namespace: str,
             config: Optional[CubeApiConfig] = None,
             namespace_map: Optional[Union[NamespaceMap, Dict, str]] = None,
             version: str = "v1")
```

Initializes the Cube.js integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration.
- `namespace` - The Grai namespace to associate with output from the integration
- `config` - The connection configuration for your cube API. If not provided, an effort will be made to load
  these from the environment.
- `namespace_map` - An optional mapping between cube data sources and Grai namespaces
- `version` - The version of the Grai API to use for the integration

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

### get\_nodes\_and\_edges

```python
def get_nodes_and_edges() -> Tuple[List[SourcedNode], List[SourcedEdge]]
```

Returns a tuple of lists of SourcedNode and SourcedEdge objects

### ready

```python
def ready() -> bool
```

Returns True if the integration is ready to run
