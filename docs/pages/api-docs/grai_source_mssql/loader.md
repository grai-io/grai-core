---
sidebar_label: loader
title: grai_source_mssql.loader
---

## BaseSettings Objects

```python
class BaseSettings(pydantic.BaseSettings)
```



### Config Objects

```python
class Config()
```



## Protocol Objects

```python
class Protocol(Enum)
```



## MsSqlSettings Objects

```python
class MsSqlSettings(BaseSettings)
```



### validate\_protocol

```python
@validator("protocol")
def validate_protocol(cls, value)
```

**Arguments**:

  value:


**Returns**:



### connection\_string

```python
def connection_string()
```



### validate\_driver

```python
@validator("driver")
def validate_driver(cls, value)
```

**Arguments**:

  value:


**Returns**:



### parse\_empty\_values

```python
@root_validator(pre=True)
def parse_empty_values(cls, values)
```

Empty strings should be treated as missing

**Arguments**:

  values:


**Returns**:



## MsSqlGraiSettings Objects

```python
class MsSqlGraiSettings(BaseSettings)
```



## ConnectorSettings Objects

```python
class ConnectorSettings(MsSqlSettings, MsSqlGraiSettings)
```



## MsSQLConnector Objects

```python
class MsSQLConnector()
```



### connect

```python
def connect() -> pyodbc.connect
```

**Arguments**:



**Returns**:



### connection

```python
@property
def connection()
```



### close

```python
def close() -> None
```

**Arguments**:



**Returns**:



### query\_runner

```python
def query_runner(query: str, params: List = []) -> List[Dict]
```

**Arguments**:

  query (str):
- `params` _List, optional_ - (Default value = [])


**Returns**:



### tables

```python
@cached_property
def tables() -> List[Table]
```

Create and return a list of dictionaries with the
schemas and names of tables in the database
connected to by the connection argument.

**Arguments**:



**Returns**:



### columns

```python
@cached_property
def columns() -> List[Column]
```

Creates and returns a list of dictionaries for the specified
schema.table in the database connected to.

**Arguments**:



**Returns**:



### column\_map

```python
@cached_property
def column_map() -> Dict[Tuple[str, str], List[Column]]
```

**Arguments**:



**Returns**:



### get\_table\_columns

```python
def get_table_columns(table: Table) -> List[Column]
```

**Arguments**:

  table (Table):


**Returns**:



### foreign\_keys

```python
@cached_property
def foreign_keys() -> List[Edge]
```

This needs to be tested / evaluated

**Arguments**:



**Returns**:



### get\_nodes

```python
def get_nodes() -> List[MsSqlNode]
```

**Arguments**:



**Returns**:



### get\_edges

```python
def get_edges() -> List[Edge]
```

**Arguments**:



**Returns**:



### get\_nodes\_and\_edges

```python
def get_nodes_and_edges() -> Tuple[List[MsSqlNode], List[Edge]]
```

**Arguments**:



**Returns**:
