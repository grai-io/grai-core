---
sidebar_label: base
title: grai_source_redshift.base
---

## RedshiftIntegration Objects

```python
class RedshiftIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from Redshift

**Attributes**:

- `connector` - The connector responsible for communicating with Redshift.

### \_\_init\_\_

```python
def __init__(namespace: str,
             source: SourceV1,
             version: Optional[str] = None,
             user: Optional[str] = None,
             password: Optional[str] = None,
             database: Optional[str] = None,
             host: Optional[str] = None,
             port: Optional[Union[str, int]] = None)
```

Initializes the Redshift integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `namespace` - The Grai namespace to associate with output from the integration
- `user` - The username to use when connecting to Redshift.
- `password` - The password to use when connecting to Redshift.
- `host` - The Redshift host address.
- `port` - The Redshift port.
- `database` - The Redshift database to connect to.

### get\_nodes\_and\_edges

```python
@cache
def get_nodes_and_edges() -> Tuple[List[SourcedNode], List[SourcedEdge]]
```

Returns a tuple of lists of SourcedNode and SourcedEdge objects

### ready

```python
def ready() -> bool
```

Returns True if the integration is ready to run

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
