---
sidebar_label: organization
title: grai_schemas.v1.organization
---

## OrganisationSpec Objects

```python
class OrganisationSpec(GraiBaseModel)
```

Class definition of OrganisationSpec

**Attributes**:

- `name` - The name of the organisation.
- `id` - Optional UUID of the organisation

## OrganisationV1 Objects

```python
class OrganisationV1(GraiBaseModel)
```

Class definition of OrganisationV1

**Attributes**:

- `type` - The type of the object e.g. Node, Edge, etc.
- `version` - The version of the object e.g. v1
- `spec` - The specification of the object.

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: dict) -> "OrganisationV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:
