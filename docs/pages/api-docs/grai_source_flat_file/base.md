---
sidebar_label: base
title: grai_source_flat_file.base
---

## FlatFileIntegration Objects

```python
class FlatFileIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from flat files like csv and parquet.

**Attributes**:

- `file_name` - A path to the file
- `namespace` - The Grai namespace to associate with output from the integration

### \_\_init\_\_

```python
def __init__(file_name: str,
             namespace: str,
             source: SourceV1,
             version: Optional[str] = None)
```

Initializes the Flat File integration.

**Arguments**:

- `file_name` - A path to the file
- `namespace` - The Grai namespace to associate with output from the integration
- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration

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

### ready

```python
def ready() -> bool
```

Returns True if the integration is ready to run
