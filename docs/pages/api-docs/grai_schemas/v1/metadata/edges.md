---
sidebar_label: edges
title: grai_schemas.v1.metadata.edges
---

## EdgeMetadataTypeLabels Objects

```python
class EdgeMetadataTypeLabels(Enum)
```



## BaseEdgeMetadataV1 Objects

```python
class BaseEdgeMetadataV1(GraiBaseModel)
```

Class definition of BaseEdgeMetadataV1

**Attributes**:

- `type` - todo
- `version` - todo
- `edge_type` - todo
- `edge_attributes` - todo
- `tags` - todo

## MalformedEdgeMetadataV1 Objects

```python
class MalformedEdgeMetadataV1(MalformedMetadata, BaseEdgeMetadataV1)
```

Class definition of MalformedEdgeMetadataV1

**Attributes**:

- `edge_type` - todo
- `edge_attributes` - todo

### edge\_type

type: ignore

### edge\_attributes

type: ignore

## GenericEdgeMetadataV1 Objects

```python
class GenericEdgeMetadataV1(BaseEdgeMetadataV1)
```

Class definition of GenericEdgeMetadataV1

**Attributes**:

- `edge_type` - todo
- `edge_attributes` - todo

## TableToColumnAttributes Objects

```python
class TableToColumnAttributes(GenericAttributes)
```

Class definition of TableToColumnAttributes

**Attributes**:

- `version` - todo

## TableToColumnMetadata Objects

```python
class TableToColumnMetadata(BaseEdgeMetadataV1)
```

Class definition of TableToColumnMetadata

**Attributes**:

- `edge_type` - todo
- `edge_attributes` - todo

## TableToTableAttributes Objects

```python
class TableToTableAttributes(GenericAttributes)
```

Class definition of TableToTableAttributes

**Attributes**:

- `version` - todo

## TableToTableMetadata Objects

```python
class TableToTableMetadata(BaseEdgeMetadataV1)
```

Class definition of TableToTableMetadata

**Attributes**:

- `edge_type` - todo
- `edge_attributes` - todo

## ColumnToColumnAttributes Objects

```python
class ColumnToColumnAttributes(GenericAttributes)
```

Class definition of ColumnToColumnAttributes

**Attributes**:

- `version` - todo
- `preserves_data_type` - todo
- `preserves_nullable` - todo
- `preserves_unique` - todo

## ColumnToColumnMetadata Objects

```python
class ColumnToColumnMetadata(BaseEdgeMetadataV1)
```

Class definition of ColumnToColumnMetadata

**Attributes**:

- `edge_type` - todo
- `edge_attributes` - todo
