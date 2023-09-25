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

Class definition of BaseSpec

**Attributes**:

- `is_active` - todo
- `display_name` - todo
- `workspace` - todo

## SourcedNodeSpecMetadataMixin Objects

```python
class SourcedNodeSpecMetadataMixin(GraiBaseModel)
```

Class definition of SourcedNodeSpecMetadataMixin

**Attributes**:

- `metadata` - todo

## NamedSourceSpec Objects

```python
class NamedSourceSpec(NodeNamedID, BaseSpec, SourcedNodeSpecMetadataMixin,
                      DataSourceMixin)
```



### to\_node

```python
def to_node() -> "NamedSpec"
```



## IDSourceSpec Objects

```python
class IDSourceSpec(NodeUuidID, BaseSpec, SourcedNodeSpecMetadataMixin,
                   DataSourceMixin)
```



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

- `type` - todo
- `version` - todo
- `spec` - todo

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "SourcedNodeV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:



### to\_node

```python
def to_node() -> "NodeV1"
```



## NodeSpecMetadataMixin Objects

```python
class NodeSpecMetadataMixin(GraiBaseModel)
```

Class definition of NodeSpecMetadataMixin

**Attributes**:

- `metadata` - todo

## NamedSpec Objects

```python
class NamedSpec(NodeNamedID, BaseSpec, NodeSpecMetadataMixin,
                DataSourcesMixin)
```



## IDSpec Objects

```python
class IDSpec(NodeUuidID, BaseSpec, NodeSpecMetadataMixin, DataSourcesMixin)
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
