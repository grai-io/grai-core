---
sidebar_label: source
title: grai_schemas.v1.source
---

## SourceSpec Objects

```python
class SourceSpec(GraiBaseModel)
```

Class definition of SourceSpec

**Attributes**:

- `id` - todo
- `name` - todo
- `workspace` - todo

## DataSourceMixin Objects

```python
class DataSourceMixin(GraiBaseModel)
```

Class definition of DataSourceMixin

**Attributes**:

- `data_source` - todo

## DataSourcesMixin Objects

```python
class DataSourcesMixin(GraiBaseModel)
```

Class definition of DataSourcesMixin

**Attributes**:

- `data_sources` - todo

## SourceV1 Objects

```python
class SourceV1(GraiBaseModel)
```

Class definition of SourceV1

**Attributes**:

- `type` - todo
- `version` - todo
- `spec` - todo

### from\_spec

```python
@classmethod
def from_spec(cls, spec: Union[dict, SourceSpec]) -> "SourceV1"
```

**Arguments**:

  spec:


**Returns**:
