---
sidebar_label: schema
title: grai_schemas.schema
---

## Schema Objects

```python
class Schema(GraiBaseModel)
```

Class definition of Schema

**Attributes**:

- `entity` - A Grai object

### to\_model

```python
@classmethod
def to_model(cls, item: Dict, version: Literal["v1"],
             typing_type: Literal["Node", "Edge"]) -> GraiType
```

Convert an item spec to a Grai object

**Arguments**:

- `item` - An item spec to be converted to a Grai object
- `version` - which version of the schema to use
- `typing_type` - The type of the object e.g. Node, Edge, etc.


**Returns**:

  The Grai object
