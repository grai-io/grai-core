---
sidebar_label: models
title: grai_source_looker.models
---

## LookerNode Objects

```python
class LookerNode(BaseModel)
```



## ID Objects

```python
class ID(LookerNode)
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



## FieldID Objects

```python
class FieldID(ID)
```



### make\_full\_name

```python
@root_validator(pre=True)
def make_full_name(cls, values)
```

**Arguments**:

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



## Dashboard Objects

```python
class Dashboard(LookerNode)
```



### get\_queries

```python
def get_queries()
```



### get\_query\_edges

```python
def get_query_edges()
```



### get\_fields

```python
def get_fields()
```



### get\_edges

```python
def get_edges()
```
