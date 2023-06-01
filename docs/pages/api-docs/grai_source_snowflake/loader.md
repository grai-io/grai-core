---
sidebar_label: loader
title: grai_source_snowflake.loader
---

#### string\_is\_quoted

```python
def string_is_quoted(string: str) -> bool
```

**Arguments**:

  string (str):


**Returns**:



#### get\_from\_env

```python
def get_from_env(label: str,
                 default: Optional[Any] = None,
                 required: bool = True,
                 validator: Optional[Callable] = None)
```

**Arguments**:

  label (str):
- `default` _Optional[Any], optional_ - (Default value = None)
- `required` _bool, optional_ - (Default value = True)
- `validator` _Optional[Callable], optional_ - (Default value = None)


**Returns**:



## SnowflakeConnector Objects

```python
class SnowflakeConnector()
```



#### connection\_dict

```python
@property
def connection_dict() -> Dict[str, str]
```

Builds connection parameters for Snowflake

Full documentation of the API available here
https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods

**Arguments**:



**Returns**:



#### connect

```python
def connect() -> "SnowflakeConnector"
```

**Arguments**:



**Returns**:



#### connection

```python
@property
def connection() -> snowflake.connector.SnowflakeConnection
```

**Arguments**:



**Returns**:



#### close

```python
def close() -> None
```

**Arguments**:



**Returns**:



#### query\_runner

```python
def query_runner(query: str, param_dict: Dict = {}) -> List[Dict]
```

**Arguments**:

  query (str):
- `param_dict` _Dict, optional_ - (Default value = {})


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



#### column\_map

```python
@cached_property
def column_map() -> Dict[Tuple[str, str], List[Column]]
```

**Arguments**:



**Returns**:



#### get\_table\_columns

```python
def get_table_columns(table: Table)
```

**Arguments**:

  table (Table):


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
def get_nodes() -> List[SnowflakeNode]
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
def get_nodes_and_edges() -> Tuple[List[SnowflakeNode], List[Edge]]
```

**Arguments**:



**Returns**:
