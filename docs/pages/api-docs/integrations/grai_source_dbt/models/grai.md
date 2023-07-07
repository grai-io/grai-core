---
sidebar_label: grai
title: grai_source_dbt.models.grai
---

## Column Objects

```python
class Column(ID)
```



### full\_name

```python
@property
def full_name()
```



### from\_table\_column

```python
@classmethod
def from_table_column(cls, table: NodeTypes, column, namespace) -> "Column"
```

**Arguments**:

  table (NodeTypes):
  column:
  namespace:


**Returns**:



### unique\_id

```python
@property
def unique_id()
```



### Config Objects

```python
class Config()
```



## EdgeTerminus Objects

```python
class EdgeTerminus(BaseModel)
```



### identifier

```python
@property
def identifier()
```



### Config Objects

```python
class Config()
```



## Edge Objects

```python
class Edge(BaseModel)
```



### name

```python
@property
def name()
```



### Config Objects

```python
class Config()
```
