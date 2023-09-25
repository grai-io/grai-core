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

- `id` - An optional UUID of the source.
- `name` - The name of the source.
- `workspace` - The workspace the source belongs to.

## DataSourceMixin Objects

```python
class DataSourceMixin(GraiBaseModel)
```

Class definition of DataSourceMixin

**Attributes**:

- `data_source` - The data source which created this object.

## DataSourcesMixin Objects

```python
class DataSourcesMixin(GraiBaseModel)
```

Class definition of DataSourcesMixin

**Attributes**:

- `data_sources` - The data sources which created this object.

## SourceV1 Objects

```python
class SourceV1(GraiBaseModel)
```

Class definition of SourceV1

**Attributes**:

- `type` - A string indicating the type of the object. In this case it is &quot;Source&quot;.
- `version` - The version of the object e.g. &quot;v1&quot;.
- `spec` - The specification of the object.

### from\_spec

```python
@classmethod
def from_spec(cls, spec: Union[dict, SourceSpec]) -> "SourceV1"
```

**Arguments**:

- `spec` - The specification of the object.


**Returns**:
