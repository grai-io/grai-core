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

- `entity` - todo

### to\_model

```python
@classmethod
def to_model(cls, item: Dict, version: Literal["v1"],
             typing_type: Literal["Node", "Edge"]) -> GraiType
```

**Arguments**:

  item (Dict):
  version (Literal[&quot;v1&quot;]):
  typing_type (Literal[&quot;Node&quot;, &quot;Edge&quot;]):


**Returns**:
