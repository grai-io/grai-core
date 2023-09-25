---
sidebar_label: quarantine
title: grai_schemas.integrations.quarantine
---

## QuarantineReason Objects

```python
class QuarantineReason(BaseModel, ABC)
```

Base class for quarantine reasons

### reason

```python
@property
@abstractmethod
def reason() -> str
```

Returns a string describing the reason for quarantine

## MissingEdgeNodeReason Objects

```python
class MissingEdgeNodeReason(QuarantineReason)
```

Class definition of MissingEdgeNodeReason

**Attributes**:

- `side` - Either Source or Destination
- `node_name` - The name of the missing node
- `node_namespace` - The namespace of the missing node

### reason

```python
@property
def reason() -> str
```

Returns a string describing the reason for quarantine

## QuarantinedEdge Objects

```python
class QuarantinedEdge(BaseModel)
```

Class definition of QuarantinedEdge

**Attributes**:

- `edge` - The edge that was quarantined
- `reasons` - A list of reasons for quarantine

## QuarantinedNode Objects

```python
class QuarantinedNode(BaseModel)
```

Class definition of QuarantinedNode

**Attributes**:

- `node` - The node that was quarantined
- `reasons` - A list of reasons for quarantine

## QuarantinedEvent Objects

```python
class QuarantinedEvent(BaseModel)
```

Class definition of QuarantinedEvent

**Attributes**:

- `event` - The event that was quarantined
- `reasons` - A list of reasons for quarantine

## Quarantine Objects

```python
class Quarantine(BaseModel)
```

Class definition of Quarantine

**Attributes**:

- `nodes` - A list of quarantined nodes
- `edges` - A list of quarantined edges
- `events` - A list of quarantined events

### has\_quarantined

```python
@property
def has_quarantined()
```

Returns True if there are any quarantined objects in the Quarantine
