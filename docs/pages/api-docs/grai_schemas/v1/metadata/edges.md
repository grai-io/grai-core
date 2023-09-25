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

- `type` - Object type of the Metadata e.g. NodeV1, EdgeV1, etc.
- `version` - Schema version of the metadata
- `edge_type` - The type of edge e.g. TableToColumn, ColumnToColumn, etc.
- `edge_attributes` - Attributes specific to the edge type
- `tags` - Tags associated with the edge

## MalformedEdgeMetadataV1 Objects

```python
class MalformedEdgeMetadataV1(MalformedMetadata, BaseEdgeMetadataV1)
```

Class definition of MalformedEdgeMetadataV1

**Attributes**:

- `edge_type` - The literal &quot;Malformed&quot;
- `edge_attributes` - Attributes specific to the edge type

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

- `edge_type` - The literal &quot;Generic&quot;
- `edge_attributes` - Attributes specific to the edge type

## TableToColumnAttributes Objects

```python
class TableToColumnAttributes(GenericAttributes)
```

Class definition of TableToColumnAttributes

**Attributes**:

- `version` - Schema version of the attributes

## TableToColumnMetadata Objects

```python
class TableToColumnMetadata(BaseEdgeMetadataV1)
```

Class definition of TableToColumnMetadata

**Attributes**:

- `edge_type` - The literal &quot;TableToColumn&quot;
- `edge_attributes` - Attributes specific to the edge type

## TableToTableAttributes Objects

```python
class TableToTableAttributes(GenericAttributes)
```

Class definition of TableToTableAttributes

**Attributes**:

- `version` - Schema version of the attributes

## TableToTableMetadata Objects

```python
class TableToTableMetadata(BaseEdgeMetadataV1)
```

Class definition of TableToTableMetadata

**Attributes**:

- `edge_type` - The literal &quot;TableToTable&quot;
- `edge_attributes` - Attributes specific to the edge type

## ColumnToColumnAttributes Objects

```python
class ColumnToColumnAttributes(GenericAttributes)
```

Class definition of ColumnToColumnAttributes

**Attributes**:

- `version` - Schema version of the attributes
- `preserves_data_type` - Whether the data type is conserved between the source and destination columns
- `preserves_nullable` - Whether the nullability is conserved between the source and destination columns
- `preserves_unique` - Whether uniqueness is conserved between the source and destination columns

## ColumnToColumnMetadata Objects

```python
class ColumnToColumnMetadata(BaseEdgeMetadataV1)
```

Class definition of ColumnToColumnMetadata

**Attributes**:

- `edge_type` - The literal &quot;ColumnToColumn&quot;
- `edge_attributes` - Attributes specific to the edge type
