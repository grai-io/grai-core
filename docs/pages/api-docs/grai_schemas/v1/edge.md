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



## NamedSourceSpec Objects

```python
class NamedSourceSpec(EdgeNamedID, BaseSpec, SourcedEdgeSpecMetadataMixin,
                      DataSourceMixin)
```



### to\_edge

```python
def to_edge() -> "NamedSpec"
```



## IDSourceSpec Objects

```python
class IDSourceSpec(EdgeUuidID, BaseSpec, SourcedEdgeSpecMetadataMixin,
                   DataSourceMixin)
```



### to\_edge

```python
def to_edge() -> "IDSpec"
```



## SourcedEdgeV1 Objects

```python
class SourcedEdgeV1(GraiBaseModel)
```

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "SourcedEdgeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:



## NamedSpec Objects

```python
class NamedSpec(EdgeNamedID, BaseSpec, EdgeSpecMetadataMixin,
                DataSourcesMixin)
```



## IDSpec Objects

```python
class IDSpec(EdgeUuidID, BaseSpec, EdgeSpecMetadataMixin, DataSourcesMixin)
```



## EdgeV1 Objects

```python
class EdgeV1(GraiBaseModel)
```



### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "EdgeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:
