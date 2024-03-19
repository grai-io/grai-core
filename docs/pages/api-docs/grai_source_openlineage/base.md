---
sidebar_label: base
title: grai_source_openlineage.base
---

## OpenLineageIntegration Objects

```python
class OpenLineageIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from an OpenLineage json string.

**Attributes**:

- `lineage_data` - A dictionary parsing of a OpenLineage json file
- `namespace` - The Grai namespace to associate with output from the integration
- `namespaces` - A dictionary of namespace aliases to use when parsing the lineage data

### \_\_init\_\_

```python
def __init__(lineage_data: Union[str, dict],
             source: SourceV1,
             version: Optional[str] = None,
             namespace: Optional[str] = "default",
             namespaces: Optional[Dict[str, str]] = None)
```

Initializes the dbt integration.

**Arguments**:

- `lineage_data` - Either a string path to a manifest.json file, or a dictionary parsing of a manifest.json file
- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `namespace` - The Grai namespace to associate with output from the integration
- `namespaces` - A dictionary of namespace aliases to use when parsing the lineage data

### lineage

```python
@cached_property
def lineage() -> OpenLineageProcessor
```

Returns a ManifestProcessor object for the lineage json file

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
