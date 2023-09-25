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

- `id` - todo
- `connection_id` - todo
- `date` - todo
- `workspace` - todo
- `diff` - todo

## EventV1 Objects

```python
class EventV1(GraiBaseModel)
```

Class definition of EventV1

**Attributes**:

- `type` - todo
- `version` - todo
- `spec` - todo

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "EventV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:
