---
sidebar_label: shared
title: grai_source_dbt.models.shared
---

## ManifestMetadata Objects

```python
class ManifestMetadata(BaseModel)
```



## ID Objects

```python
class ID(BaseModel)
```



## Constraint Objects

```python
class Constraint(str, Enum)
```



## DbtResourceType Objects

```python
class DbtResourceType(str, Enum)
```



## DbtMaterializationType Objects

```python
class DbtMaterializationType(str, Enum)
```



## NodeDeps Objects

```python
class NodeDeps(BaseModel)
```



### macros

TODO: macros not currently tested

## NodeConfig Objects

```python
class NodeConfig(BaseModel)
```



## DBTNodeColumn Objects

```python
class DBTNodeColumn(BaseModel)
```



## NodeChecksum Objects

```python
class NodeChecksum(BaseModel)
```



## NodeDocs Objects

```python
class NodeDocs(BaseModel)
```



## DBTNode Objects

```python
class DBTNode(ID)
```



### tag\_list

```python
@property
def tag_list() -> List[str]
```

**Arguments**:



**Returns**:



### full\_name

```python
@property
def full_name()
```
