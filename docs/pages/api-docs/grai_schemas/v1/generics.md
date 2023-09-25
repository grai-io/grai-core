---
sidebar_label: generics
title: grai_schemas.v1.generics
---

## BaseID Objects

```python
class BaseID(GraiBaseModel)
```

Class definition of BaseID

**Attributes**:

- `id` - Optional UUID of the object
- `name` - Optional name of the object
- `namespace` - Optional namespace of the object

## NamedID Objects

```python
class NamedID(BaseID)
```

Class definition of NamedID

**Attributes**:

- `id` - Optional UUID of the object
- `name` - Name of the object
- `namespace` - Namespace of the object

## UuidID Objects

```python
class UuidID(BaseID)
```

Class definition of UuidID

**Attributes**:

- `id` - UUID of the object
- `name` - Optional name of the object
- `namespace` - Optional namespace of the object
