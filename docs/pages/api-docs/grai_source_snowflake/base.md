---
sidebar_label: base
title: grai_source_snowflake.base
---

## SnowflakeIntegration Objects

```python
class SnowflakeIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from Snowflake

**Attributes**:

- `connector` - The connector responsible for communicating with Snowflake.

### \_\_init\_\_

```python
def __init__(source: SourceV1,
             version: Optional[str] = None,
             account: Optional[str] = None,
             user: Optional[str] = None,
             password: Optional[str] = None,
             warehouse: Optional[str] = None,
             role: Optional[str] = None,
             database: Optional[str] = None,
             namespace: Optional[str] = None,
             **kwargs)
```

Initializes the Snowflake integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `namespace` - The Grai namespace to associate with output from the integration
- `account` - Snowflake account, the characters in front of `.snowflakecomputing.com`
- `user` - The database user
- `role` - The Snowflake role to use.
- `warehouse` - The Snowflake warehouse to use.
- `database` - The Snowflake database to connect to.
- `grai_schemas`0 - The password to use when connecting to Snowflake.

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
