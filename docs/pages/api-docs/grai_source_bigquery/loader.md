---
sidebar_label: loader
title: grai_source_bigquery.loader
---

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



## BigqueryConnector Objects

```python
class BigqueryConnector()
```



#### connect

```python
def connect() -> "BigqueryConnector"
```

**Arguments**:



**Returns**:



#### connection

```python
@property
def connection() -> bigquery.Client
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
def get_table_columns(table: Table) -> List[Column]
```

**Arguments**:

  table (Table):


**Returns**:



#### get\_nodes

```python
def get_nodes() -> List[BigqueryNode]
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
def get_nodes_and_edges() -> Tuple[List[BigqueryNode], List[Edge]]
```

**Arguments**:



**Returns**:
