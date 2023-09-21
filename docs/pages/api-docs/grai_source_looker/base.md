---
sidebar_label: base
title: grai_source_looker.base
---

## LookerIntegration Objects

```python
class LookerIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from Looker.

**Attributes**:

- `connector` - The Looker connector responsible for communicating with the Looker API.

### \_\_init\_\_

```python
def __init__(source: SourceV1,
             version: Optional[str] = None,
             base_url: Optional[str] = None,
             client_id: Optional[str] = None,
             client_secret: Optional[str] = None,
             verify_ssl: Optional[bool] = None,
             namespace: Optional[str] = None,
             namespaces: Optional[Dict[str, str]] = None)
```

Initializes the Looker Integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `base_url` - The base url for the Looker API. This should exclude the /api path.
- `client_id` - The client id for the Looker API.
- `client_secret` - The client secret for the Looker API.
- `verify_ssl` - Whether or not to verify SSL certificates when connecting to the Looker API.
- `namespace` - The default Grai namespace to associate with output from the integration
- `namespaces` - A dictionary of namespaces to use for the integration. The keys of the dictionary should be the namespace names, and the values should be a list of Looker API endpoints to use for that namespace. If no namespaces are provided, the integration will use the default namespace.

### ready

```python
def ready() -> bool
```

Returns True if the integration is ready to run

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
