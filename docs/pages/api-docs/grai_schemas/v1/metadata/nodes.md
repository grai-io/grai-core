---
sidebar_label: nodes
title: grai_schemas.v1.metadata.nodes
---

## NodeMetadataTypeLabels Objects

```python
class NodeMetadataTypeLabels(Enum)
```

Class definition of NodeMetadataTypeLabels

**Attributes**:

- `generic` - The literal &quot;Generic
- `table` - The literal &quot;Table&quot;
- `column` - The literal &quot;Column&quot;
- `query` - The literal &quot;Query&quot;
- `collection` - The literal &quot;Collection&quot;

## SourceType Objects

```python
class SourceType(Enum)
```

Class definition of SourceType

**Attributes**:

- `database` - todo

## BaseNodeMetadataV1 Objects

```python
class BaseNodeMetadataV1(GraiBaseModel)
```

Class definition of BaseNodeMetadataV1

**Attributes**:

- `type` - Object type of the Metadata e.g. NodeV1, EdgeV1, etc.
- `version` - Schema version of the metadata
- `node_type` - The type of node e.g. Table, Column, etc.
- `node_attributes` - Attributes specific to the node type
- `tags` - Tags associated with the node

## MalformedNodeMetadataV1 Objects

```python
class MalformedNodeMetadataV1(MalformedMetadata, BaseNodeMetadataV1)
```

Class definition of MalformedNodeMetadataV1

**Attributes**:

- `node_type` - The literal &quot;Malformed&quot;
- `node_attributes` - Attributes specific to the node type

### node\_type

type: ignore

### node\_attributes

type: ignore

## GenericNodeMetadataV1 Objects

```python
class GenericNodeMetadataV1(BaseNodeMetadataV1)
```

Class definition of GenericNodeMetadataV1

**Attributes**:

- `node_type` - The literal &quot;Generic&quot;
- `node_attributes` - Attributes specific to the node type

## ColumnAttributes Objects

```python
class ColumnAttributes(GenericAttributes)
```

Class definition of ColumnAttributes

**Attributes**:

- `version` - Schema version of the metadata
- `data_type` - The data type of the column
- `default_value` - The default value of the column
- `is_nullable` - Whether values in the column is nullable
- `is_unique` - Whether values in the column are unique
- `is_primary_key` - Whether the column is a primary key

### data\_type

This will need to be standardized

## ColumnMetadata Objects

```python
class ColumnMetadata(BaseNodeMetadataV1)
```

Class definition of ColumnMetadata

**Attributes**:

- `node_type` - The type of node e.g. Table, Column, etc.
- `node_attributes` - Attributes specific to the node type

## TableAttributes Objects

```python
class TableAttributes(GenericAttributes)
```

Class definition of TableAttributes

**Attributes**:

- `version` - Schema version of the metadata

## TableMetadata Objects

```python
class TableMetadata(BaseNodeMetadataV1)
```

Class definition of TableMetadata

**Attributes**:

- `node_type` - The type of node e.g. Table, Column, etc.
- `node_attributes` - Attributes specific to the node type

## QueryAttributes Objects

```python
class QueryAttributes(GenericAttributes)
```

Class definition of QueryAttributes

**Attributes**:

- `version` - Schema version of the metadata

## QueryMetadata Objects

```python
class QueryMetadata(BaseNodeMetadataV1)
```

Class definition of QueryMetadata

**Attributes**:

- `node_type` - The type of node e.g. Table, Column, etc.
- `node_attributes` - Attributes specific to the node type

## CollectionMetadata Objects

```python
class CollectionMetadata(BaseNodeMetadataV1)
```

Class definition of CollectionMetadata

**Attributes**:

- `node_type` - The type of node e.g. Table, Column, etc.
- `node_attributes` - Attributes specific to the node type
