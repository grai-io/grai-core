---
sidebar_label: base
title: grai_source_fivetran.base
---

## FivetranIntegration Objects

```python
class FivetranIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from the Fivetran API.

**Attributes**:

- `connector` - The connector responsible for communicating with the Fivetran api.

### \_\_init\_\_

```python
def __init__(source: SourceV1,
             version: Optional[str] = None,
             namespaces: Optional[NamespaceTypes] = None,
             default_namespace: Optional[str] = None,
             parallelization: int = 10,
             api_key: Optional[str] = None,
             api_secret: Optional[str] = None,
             endpoint: Optional[str] = None,
             limit: Optional[int] = None)
```

Initializes the Fivetran integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `default_namespace` - The default Grai namespace to associate with output from the integration
- `namespaces` - A dictionary of namespaces to use for the integration. The keys of the dictionary should be the namespace names, and the values should be a list of Fivetran connectors to use for that namespace. If no namespaces are provided, the integration will use the default namespace.
- `parallelization` - The number of parallel connections to make with the Fivetran API
- `api_key` - A Fivetran API key
- `api_secret` - A Fivetran API secret
- `endpoint` - Your Fivetran API endpoint. Usually https://api.fivetran.com/v1
- `limit` - The maximum number of results to return in each API call

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

### edges

```python
def edges() -> List[SourcedEdge]
```

Returns a list of SourcedEdge objects
