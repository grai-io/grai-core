---
sidebar_label: models
title: grai_source_flat_file.models
---

## ID Objects

```python
class ID(BaseModel)
```



## Table Objects

```python
class Table(ID)
```



### full\_name

```python
@property
def full_name()
```



### get\_edges

```python
def get_edges() -> List["Edge"]
```

**Arguments**:



**Returns**:



## Column Objects

```python
class Column(ID)
```



### Config Objects

```python
class Config()
```



### full\_name

```python
@property
def full_name()
```



## Edge Objects

```python
class Edge(BaseModel)
```
