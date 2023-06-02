---
sidebar_label: edge
title: grai_schemas.v1.edge
---

## EdgeNamedID Objects

```python
class EdgeNamedID(NamedID)
```



## EdgeUuidID Objects

```python
class EdgeUuidID(UuidID)
```



## BaseSpec Objects

```python
class BaseSpec(GraiBaseModel)
```



## NamedSpec Objects

```python
class NamedSpec(EdgeNamedID, BaseSpec)
```



## IDSpec Objects

```python
class IDSpec(EdgeUuidID, BaseSpec)
```



## EdgeV1 Objects

```python
class EdgeV1(GraiBaseModel)
```



#### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "EdgeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:
