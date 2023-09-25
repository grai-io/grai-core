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



## BaseSourcedNodeSpec Objects

```python
class BaseSourcedNodeSpec(GraiBaseModel)
```

Class definition of BaseSourcedNodeSpec

**Attributes**:

- `is_active` - whether the node is active or not
- `display_name` - An optional short form name for the node
- `workspace` - The workspace the node belongs to
- `metadata` - Metadata associated with the node.

## NamedSourceSpec Objects

```python
class NamedSourceSpec(NodeNamedID, BaseSourcedNodeSpec)
```

Class definition of NamedSourceSpec

### to\_node

```python
def to_node() -> "NamedSpec"
```



## IDSourceSpec Objects

```python
class IDSourceSpec(NodeUuidID, BaseSourcedNodeSpec)
```

Class definition of IDSourceSpec

### to\_node

```python
def to_node() -> "IDSpec"
```



## SourcedNodeV1 Objects

```python
class SourcedNodeV1(GraiBaseModel)
```

Class definition of SourcedNodeV1

**Attributes**:

- `type` - The type of the object e.g. Node, Edge, etc.
- `version` - The version of the object e.g. v1
- `spec` - The sourced node specification.

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "SourcedNodeV1"
```

**Arguments**:

  spec_dict:


**Returns**:



### \_\_hash\_\_

```python
def __hash__()
```

Custom hash for SourcedNodeV1

### to\_node

```python
def to_node() -> "NodeV1"
```

Convert a SourcedNodeV1 to a NodeV1


## BaseNodeSpec Objects

```python
class BaseNodeSpec(GraiBaseModel)
```

Class definition of BaseSpec

**Attributes**:

- `is_active` - whether the node is active or not
- `display_name` - An optional short form name for the node
- `workspace` - The workspace the node belongs to
- `data_sources` - The data sources which created this object.
- `metadata` - Metadata associated with the node.

## NamedSpec Objects

```python
class NamedSpec(NodeNamedID, BaseNodeSpec)
```



## IDSpec Objects

```python
class IDSpec(NodeUuidID, BaseNodeSpec)
```



## NodeV1 Objects

```python
class NodeV1(GraiBaseModel)
```

Class definition of NodeV1

**Attributes**:

- `type` - todo
- `version` - todo
- `spec` - todo

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "NodeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:
