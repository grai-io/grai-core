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

- `id` - Optional UUID of the workspace
- `name` - The name of the workspace
- `organisation` - The organisation the workspace belongs to
- `ref` - The reference of the workspace in the form of `organisation/name`
- `search_enabled` - Whether the workspace is searchable or not

### ref

This keeps mypy happy

### organization

```python
@property
def organization()
```

Alias for organisation

### \_\_hash\_\_

```python
def __hash__() -> int
```

Workspace hash definition

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
