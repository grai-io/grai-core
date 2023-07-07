---
sidebar_label: models
title: grai_source_postgres.models
---

## PostgresNode Objects

```python
class PostgresNode(BaseModel)
```



## ID Objects

```python
class ID(PostgresNode)
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



## ColumnConstraint Objects

```python
class ColumnConstraint(Enum)
```



## Column Objects

```python
class Column(PostgresNode)
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
class Table(PostgresNode)
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
