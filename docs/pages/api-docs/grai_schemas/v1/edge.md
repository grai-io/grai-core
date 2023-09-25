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



## BaseSourcedEdgeSpec Objects

```python
class BaseSourcedEdgeSpec(GraiBaseModel)
```

Class definition of BaseSourcedEdgeSpec

**Attributes**:

- `display_name` - todo
- `source` - todo
- `destination` - todo
- `is_active` - todo
- `workspace` - todo
- `data_source` - todo
- `metadata` - todo

## NamedSourceSpec Objects

```python
class NamedSourceSpec(EdgeNamedID, BaseSourcedEdgeSpec)
```



### to\_edge

```python
def to_edge() -> "NamedSpec"
```



## IDSourceSpec Objects

```python
class IDSourceSpec(EdgeUuidID, BaseSourcedEdgeSpec)
```



### to\_edge

```python
def to_edge() -> "IDSpec"
```



## SourcedEdgeV1 Objects

```python
class SourcedEdgeV1(GraiBaseModel)
```

Class definition of SourcedEdgeV1

**Attributes**:

- `type` - todo
- `version` - todo
- `spec` - todo

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "SourcedEdgeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:



## BaseEdgeSpec Objects

```python
class BaseEdgeSpec(GraiBaseModel)
```

Class definition of BaseEdgeSpec

**Attributes**:

- `display_name` - todo
- `source` - todo
- `destination` - todo
- `is_active` - todo
- `workspace` - todo
- `data_sources` - todo
- `metadata` - todo

## NamedSpec Objects

```python
class NamedSpec(EdgeNamedID, BaseEdgeSpec)
```



## IDSpec Objects

```python
class IDSpec(EdgeUuidID, BaseEdgeSpec)
```



## EdgeV1 Objects

```python
class EdgeV1(GraiBaseModel)
```

Class definition of EdgeV1

**Attributes**:

- `type` - todo
- `version` - todo
- `spec` - todo

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "EdgeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:
