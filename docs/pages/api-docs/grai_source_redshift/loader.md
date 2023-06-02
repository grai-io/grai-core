---
sidebar_label: loader
title: grai_source_redshift.loader
---

## RedshiftConfig Objects

```python
class RedshiftConfig(BaseSettings)
```



## Config Objects

```python
class Config()
```



## RedshiftConnector Objects

```python
class RedshiftConnector()
```



#### connect

```python
def connect()
```



#### connection

```python
@property
def connection()
```



#### close

```python
def close() -> None
```

**Arguments**:



**Returns**:



#### query\_runner

```python
def query_runner(query: str) -> List[Dict]
```

**Arguments**:

  query (str):


**Returns**:



#### tables

```python
@cached_property
def tables() -> List[Table]
```

Create and return a list of dictionaries with the
schemas and names of tables in the database
connected to by the connection argument.

**Arguments**:



**Returns**:



#### columns

```python
@cached_property
def columns() -> List[Column]
```

Creates and returns a list of dictionaries for the specified
schema.table in the database connected to.

**Arguments**:



**Returns**:



#### get\_table\_columns

```python
def get_table_columns(table: Table)
```

**Arguments**:

  table (Table):


**Returns**:



#### column\_map

```python
@cached_property
def column_map() -> Dict[Tuple[str, str], List[Column]]
```

**Arguments**:



**Returns**:



#### foreign\_keys

```python
@cached_property
def foreign_keys() -> List[Edge]
```

This needs to be tested / evaluated

**Arguments**:



**Returns**:



#### get\_nodes

```python
def get_nodes() -> List[RedshiftNode]
```

**Arguments**:



**Returns**:



#### get\_edges

```python
def get_edges() -> List[Edge]
```

**Arguments**:



**Returns**:



#### get\_nodes\_and\_edges

```python
def get_nodes_and_edges() -> Tuple[List[RedshiftNode], List[Edge]]
```

**Arguments**:



**Returns**:
