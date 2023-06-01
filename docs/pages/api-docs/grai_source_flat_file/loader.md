---
sidebar_label: loader
title: grai_source_flat_file.loader
---

#### get\_file\_name

```python
def get_file_name(file_name: str) -> str
```

**Arguments**:

  file_name (str):


**Returns**:



#### load\_file

```python
def load_file(file_name: str) -> pd.DataFrame
```

**Arguments**:

  file_name (str):


**Returns**:



#### map\_pandas\_types

```python
def map_pandas_types(dtype) -> str
```

**Arguments**:

  dtype:


**Returns**:



#### build\_column

```python
def build_column(data: pd.Series, namespace: str, table_name: str) -> Column
```

**Arguments**:

  data (pd.Series):
  namespace (str):
  table_name (str):


**Returns**:



#### column\_builder

```python
def column_builder(namespace: str,
                   table_name: str) -> Callable[[pd.Series], Column]
```

**Arguments**:

  namespace (str):
  table_name (str):


**Returns**:



#### table\_builder

```python
def table_builder(namespace: str, table_name: str,
                  file_location: str) -> Table
```

**Arguments**:

  namespace (str):
  table_name (str):
  file_location (str):


**Returns**:



#### build\_nodes\_and\_edges

```python
def build_nodes_and_edges(
        file_name: str,
        namespace: str) -> Tuple[List[Union[Table, Column]], List[Edge]]
```

**Arguments**:

  file_name (str):
  namespace (str):


**Returns**:
