---
sidebar_label: quarantine
title: grai_schemas.integrations.quarantine
---

## MissingEdgeNodeReason Objects

```python
class MissingEdgeNodeReason(QuarantineReason)
```

Class definition of MissingEdgeNodeReason

**Attributes**:

- `side` - todo
- `node_name` - todo
- `node_namespace` - todo

## QuarantinedEdge Objects

```python
class QuarantinedEdge(BaseModel)
```

Class definition of QuarantinedEdge

**Attributes**:

- `edge` - todo
- `reasons` - todo

## QuarantinedNode Objects

```python
class QuarantinedNode(BaseModel)
```

Class definition of QuarantinedNode

**Attributes**:

- `node` - todo
- `reasons` - todo

## QuarantinedEvent Objects

```python
class QuarantinedEvent(BaseModel)
```

Class definition of QuarantinedEvent

**Attributes**:

- `event` - todo
- `reasons` - todo

## Quarantine Objects

```python
class Quarantine(BaseModel)
```

Class definition of Quarantine

**Attributes**:

- `nodes` - todo
- `edges` - todo
- `events` - todo
