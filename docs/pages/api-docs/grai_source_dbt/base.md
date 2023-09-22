---
sidebar_label: base
title: grai_source_dbt.base
---

## DbtIntegration Objects

```python
class DbtIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from a dbt manifest.json file.

**Attributes**:

- `manifest_data` - A dictionary parsing of a manifest.json file
- `namespace` - The Grai namespace to associate with output from the integration

### \_\_init\_\_

```python
def __init__(manifest_data: Union[str, dict],
             source: SourceV1,
             version: Optional[str] = None,
             namespace: Optional[str] = "default")
```

Initializes the dbt integration.

**Arguments**:

- `manifest_data` - Either a string path to a manifest.json file, or a dictionary parsing of a manifest.json file
- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `namespace` - The Grai namespace to associate with output from the integration

### manifest

```python
@cached_property
def manifest() -> ManifestProcessor
```

Returns a ManifestProcessor object for the manifest.json file

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
