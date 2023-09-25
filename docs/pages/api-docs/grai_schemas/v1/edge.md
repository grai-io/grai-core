---
sidebar_label: edge
title: grai_schemas.v1.edge
---

## EdgeNamedID Objects

```python
class EdgeNamedID(NamedID)
```

Class definition of EdgeNamedID

## EdgeUuidID Objects

```python
class EdgeUuidID(UuidID)
```

Class definition of EdgeUuidID

## BaseSourcedEdgeSpec Objects

```python
class BaseSourcedEdgeSpec(GraiBaseModel)
```

Class definition of BaseSourcedEdgeSpec

**Attributes**:

- `display_name` - An optional short form name for the edge
- `source` - The source node of the edge
- `destination` - The destination node of the edge
- `is_active` - Whether the edge is active or not
- `workspace` - The workspace the edge belongs to
- `data_source` - The data source which created this edge
- `metadata` - Metadata associated with the edge.

## NamedSourceSpec Objects

```python
class NamedSourceSpec(EdgeNamedID, BaseSourcedEdgeSpec)
```

Class definition of NamedSourceSpec

### to\_edge

```python
def to_edge() -> "NamedSpec"
```

**Returns**:

  A NamedSpec instance

## IDSourceSpec Objects

```python
class IDSourceSpec(EdgeUuidID, BaseSourcedEdgeSpec)
```

Class definition of IDSourceSpec

### to\_edge

```python
def to_edge() -> "IDSpec"
```

**Returns**:

  An IDSpec instance

## SourcedEdgeV1 Objects

```python
class SourcedEdgeV1(GraiBaseModel)
```

Class definition of SourcedEdgeV1

**Attributes**:

- `type` - The type of the edge e.g. NodeV1, EdgeV1, etc...
- `version` - Object version e.g. v1
- `spec` - The edge specification

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "SourcedEdgeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:

  A SourcedEdgeV1 instance


### to\_edge

```python
def to_edge() -> "EdgeV1"
```

Converts a SourcedEdgeV1 instance to an EdgeV1 instance

**Returns**:

  An EdgeV1 instance

## BaseEdgeSpec Objects

```python
class BaseEdgeSpec(GraiBaseModel)
```

Class definition of BaseEdgeSpec

**Attributes**:

- `display_name` - An optional short form name for the edge
- `source` - The source node of the edge
- `destination` - The destination node of the edge
- `is_active` - Whether the edge is active or not
- `workspace` - The workspace the edge belongs to
- `data_sources` - The data sources which have contributed to this edge
- `metadata` - Metadata associated with the edge.

## NamedSpec Objects

```python
class NamedSpec(EdgeNamedID, BaseEdgeSpec)
```

Class definition of NamedSpec

## IDSpec Objects

```python
class IDSpec(EdgeUuidID, BaseEdgeSpec)
```

Class definition of IDSpec

## EdgeV1 Objects

```python
class EdgeV1(GraiBaseModel)
```

Class definition of EdgeV1

**Attributes**:

- `type` - The type of the edge e.g. NodeV1, EdgeV1, etc...
- `version` - Object version e.g. v1
- `spec` - The edge specification

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "EdgeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:

  An EdgeV1 instance
