---
sidebar_label: node
title: grai_schemas.v1.node
---

## NodeNamedID Objects

```python
class NodeNamedID(NamedID)
```



## NodeUuidID Objects

```python
class NodeUuidID(UuidID)
```



## BaseSpec Objects

```python
class BaseSpec(GraiBaseModel)
```



## NamedSourceSpec Objects

```python
class NamedSourceSpec(NodeNamedID, BaseSpec, DataSourceMixin)
```



## IDSourceSpec Objects

```python
class IDSourceSpec(NodeUuidID, BaseSpec, DataSourceMixin)
```



## SourcedNodeV1 Objects

```python
class SourcedNodeV1(GraiBaseModel)
```

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "SourcedNodeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:



## NamedSpec Objects

```python
class NamedSpec(NodeNamedID, BaseSpec, DataSourcesMixin)
```



## IDSpec Objects

```python
class IDSpec(NodeUuidID, BaseSpec, DataSourcesMixin)
```



## NodeV1 Objects

```python
class NodeV1(GraiBaseModel)
```



### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "NodeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:
