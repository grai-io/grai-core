---
sidebar_label: base
title: grai_source_mysql.base
---

## MySQLIntegration Objects

```python
class MySQLIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from MySQL

**Attributes**:

- `connector` - Responsible for communicating with MySQL.

### \_\_init\_\_

```python
def __init__(source: SourceV1,
             version: Optional[str] = None,
             dbname: Optional[str] = None,
             user: Optional[str] = None,
             password: Optional[str] = None,
             host: Optional[str] = None,
             port: Optional[Union[str, int]] = None,
             namespace: Optional[str] = None)
```

Initializes the MsSQL integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `namespace` - The Grai namespace to associate with output from the integration
- `dbname` - The MySQL database to connect to.
- `user` - The username to use when connecting to MySQL.
- `password` - The password to use when connecting to MySQL.
- `host` - The MySQL host address.
- `port` - The MySQL port.

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
