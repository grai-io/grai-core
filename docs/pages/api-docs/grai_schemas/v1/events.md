---
sidebar_label: events
title: grai_schemas.v1.events
---

## EventSpec Objects

```python
class EventSpec(GraiBaseModel)
```

Class definition of EventSpec

**Attributes**:

- `id` - UUID of the event.
- `connection_id` - UUID of the events connection.
- `date` - Datetime of the event.
- `workspace` - WorkspaceSpec of the event.
- `diff` - Json of the changes from the event.

## EventV1 Objects

```python
class EventV1(GraiBaseModel)
```

Class definition of EventV1

**Attributes**:

- `type` - Object type of the Metadata e.g. NodeV1, EdgeV1, etc.
- `version` - Schema version of the object.
- `spec` - The event specification.

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "EventV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:

  An EventV1 instance
