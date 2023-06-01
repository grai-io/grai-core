---
sidebar_label: models
title: grai_source_snowflake.models
---

## SnowflakeNode Objects

```python
class SnowflakeNode(BaseModel)
```



## ID Objects

```python
class ID(SnowflakeNode)
```



## Config Objects

```python
class Config()
```



## TableID Objects

```python
class TableID(ID)
```



#### make\_full\_name

```python
@root_validator(pre=True)
def make_full_name(cls, values: Dict) -> Dict
```

**Arguments**:

  values (Dict):


**Returns**:



#### validate\_quoted\_string

```python
def validate_quoted_string(string: str) -> str
```

**Arguments**:

  string (str):


**Returns**:



## ColumnID Objects

```python
class ColumnID(ID)
```



#### make\_full\_name

```python
@root_validator(pre=True)
def make_full_name(cls, values: Dict) -> Dict
```

**Arguments**:

  values (Dict):


**Returns**:



#### validate\_name

```python
@validator("table_name")
def validate_name(cls, value)
```

**Arguments**:

  value:


**Returns**:



## Column Objects

```python
class Column(SnowflakeNode)
```



## Config Objects

```python
class Config()
```



#### make\_full\_name

```python
@validator("full_name", always=True)
def make_full_name(cls, full_name: Optional[str], values: Dict) -> str
```

**Arguments**:

  full_name (Optional[str]):
  values (Dict):


**Returns**:



#### validate\_name

```python
@validator("name", "table")
def validate_name(cls, value)
```

**Arguments**:

  value:


**Returns**:



## Constraint Objects

```python
class Constraint(str, Enum)
```



## Edge Objects

```python
class Edge(BaseModel)
```



## TableType Objects

```python
class TableType(str, Enum)
```



## Table Objects

```python
class Table(SnowflakeNode)
```



## Config Objects

```python
class Config()
```



#### id

```python
@property
def id()
```



#### make\_full\_name

```python
@validator("full_name", always=True)
def make_full_name(cls, full_name: Optional[str], values: Dict) -> str
```

**Arguments**:

  full_name (Optional[str]):
  values (Dict):


**Returns**:



#### validate\_name

```python
@validator("name")
def validate_name(cls, value)
```

**Arguments**:

  value:


**Returns**:



#### get\_edges

```python
def get_edges() -> List[Edge]
```

**Arguments**:



**Returns**:



## EdgeQuery Objects

```python
class EdgeQuery(BaseModel)
```



#### to\_edge

```python
def to_edge() -> Optional[Edge]
```

**Arguments**:



**Returns**:
