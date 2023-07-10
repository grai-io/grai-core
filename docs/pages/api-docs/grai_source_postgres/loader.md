---
sidebar_label: loader
title: grai_source_postgres.loader
---

## get\_from\_env

```python
def get_from_env(label: str,
                 default: Optional[Any] = None,
                 validator: Callable = None)
```

**Arguments**:

  label (str):
- `default` _Optional[Any], optional_ - (Default value = None)
- `validator` _Callable, optional_ - (Default value = None)


**Returns**:



## PostgresConnector Objects

```python
class PostgresConnector()
```



### connection\_string

```python
@property
def connection_string() -> str
```

**Arguments**:



**Returns**:



### connect

```python
def connect()
```



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
def query_runner(query: str, param_dict: Dict = {}) -> List[Dict]
```

**Arguments**:

  query (str):
- `param_dict` _Dict, optional_ - (Default value = {})


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



### get\_table\_columns

```python
def get_table_columns(table: Table) -> List[Column]
```

**Arguments**:

  table (Table):


**Returns**:



### column\_map

```python
@cached_property
def column_map() -> Dict[Tuple[str, str], List[Column]]
```

**Arguments**:



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
def get_nodes() -> List[PostgresNode]
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
def get_nodes_and_edges() -> Tuple[List[PostgresNode], List[Edge]]
```

**Arguments**:



**Returns**:
