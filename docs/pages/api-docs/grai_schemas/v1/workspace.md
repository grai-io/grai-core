---
sidebar_label: workspace
title: grai_schemas.v1.workspace
---

## WorkspaceSpec Objects

```python
class WorkspaceSpec(GraiBaseModel)
```

Class definition of WorkspaceSpec

**Attributes**:

- `id` - todo
- `name` - todo
- `organisation` - todo
- `ref` - todo
- `search_enabled` - todo

### ref

This keeps mypy happy

## WorkspaceV1 Objects

```python
class WorkspaceV1(GraiBaseModel)
```

Class definition of WorkspaceV1

**Attributes**:

- `type` - todo
- `version` - todo
- `spec` - todo

### from\_spec

```python
@classmethod
def from_spec(cls, spec_dict: Dict) -> "WorkspaceV1"
```

**Arguments**:

  spec_dict (Dict):


**Returns**:
