---
sidebar_label: models
title: grai_source_mysql.models
---

## MysqlNode Objects

```python
class MysqlNode(BaseModel)
```



## ID Objects

```python
class ID(MysqlNode)
```



### Config Objects

```python
class Config()
```



## TableID Objects

```python
class TableID(ID)
```



### make\_full\_name

```python
@root_validator(pre=True)
def make_full_name(cls, values)
```

**Arguments**:

  values:


**Returns**:



## ColumnID Objects

```python
class ColumnID(ID)
```



### make\_full\_name

```python
@root_validator(pre=True)
def make_full_name(cls, values)
```

**Arguments**:

  values:


**Returns**:



## ColumnKey Objects

```python
class ColumnKey(Enum)
```



## Column Objects

```python
class Column(MysqlNode)
```



### Config Objects

```python
class Config()
```



### full\_name

```python
@property
def full_name() -> str
```

**Arguments**:



**Returns**:



## Constraint Objects

```python
class Constraint(str, Enum)
```



## Edge Objects

```python
class Edge(BaseModel)
```



## Table Objects

```python
class Table(MysqlNode)
```



### Config Objects

```python
class Config()
```



### make\_full\_name

```python
@validator("full_name", always=True)
def make_full_name(cls, full_name, values)
```

**Arguments**:

  full_name:
  values:


**Returns**:



### get\_edges

```python
def get_edges()
```



## EdgeQuery Objects

```python
class EdgeQuery(BaseModel)
```



### to\_edge

```python
def to_edge() -> Optional[Edge]
```

**Arguments**:



**Returns**:
