---
sidebar_label: base
title: grai_source_mssql.base
---

## MsSQLIntegration Objects

```python
class MsSQLIntegration(GraiIntegrationImplementation)
```

A class for extracting Grai compliant metadata from flat files like csv and parquet.

**Attributes**:

- `connector` - Responsible for communicating with MsSQL through odbc.

### \_\_init\_\_

```python
def __init__(source: SourceV1,
             version: Optional[str] = None,
             driver: Optional[str] = None,
             user: Optional[str] = None,
             password: Optional[str] = None,
             database: Optional[str] = None,
             server: Optional[str] = None,
             protocol: Optional[str] = None,
             host: Optional[str] = None,
             port: Optional[str] = None,
             encrypt: Optional[bool] = None,
             namespace: Optional[str] = None,
             additional_connection_strings: Optional[List[str]] = None)
```

Initializes the MsSQL integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `namespace` - The Grai namespace to associate with output from the integration
- `driver` - The odbc driver to use when connecting to MsSQL. If not provided, a default driver available on the system will be used.
- `user` - The username to use when connecting to MsSQL.
- `password` - The password to use when connecting to MsSQL.
- `database` - The MsSQL database to connect to.
- `server` - The MsSQL server to connect to.
- `protocol` - The protocol to use when connecting to MsSQL.
- `grai_schemas`0 - The MsSQL host address.
- `grai_schemas`1 - The MsSQL port.
- `grai_schemas`2 - Whether or not to encrypt the connection to MsSQL.
- `grai_schemas`3 - A list of additional ODBC connection strings to use when connecting to MsSQL.

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
