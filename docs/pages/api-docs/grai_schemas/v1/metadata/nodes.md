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

- `generic` - todo
- `table` - todo
- `column` - todo
- `query` - todo
- `collection` - todo

## SourceType Objects

```python
class SourceType(Enum)
```



## BaseNodeMetadataV1 Objects

```python
class BaseNodeMetadataV1(GraiBaseModel)
```

Class definition of BaseNodeMetadataV1

**Attributes**:

- `type` - todo
- `version` - todo
- `node_type` - todo
- `node_attributes` - todo
- `tags` - todo

## MalformedNodeMetadataV1 Objects

```python
class MalformedNodeMetadataV1(MalformedMetadata, BaseNodeMetadataV1)
```

Class definition of MalformedNodeMetadataV1

**Attributes**:

- `node_type` - todo
- `node_attributes` - todo

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

- `node_type` - todo
- `node_attributes` - todo

## ColumnAttributes Objects

```python
class ColumnAttributes(GenericAttributes)
```

Class definition of ColumnAttributes

**Attributes**:

- `version` - todo
- `data_type` - todo
- `default_value` - todo
- `is_nullable` - todo
- `is_unique` - todo
- `is_primary_key` - todo

### data\_type

This will need to be standardized

## ColumnMetadata Objects

```python
class ColumnMetadata(BaseNodeMetadataV1)
```

Class definition of ColumnMetadata

**Attributes**:

- `node_type` - todo
- `node_attributes` - todo

## TableAttributes Objects

```python
class TableAttributes(GenericAttributes)
```

Class definition of TableAttributes

**Attributes**:

- `version` - todo

## TableMetadata Objects

```python
class TableMetadata(BaseNodeMetadataV1)
```

Class definition of TableMetadata

**Attributes**:

- `node_type` - todo
- `node_attributes` - todo

## QueryAttributes Objects

```python
class QueryAttributes(GenericAttributes)
```

Class definition of QueryAttributes

**Attributes**:

- `version` - todo

## QueryMetadata Objects

```python
class QueryMetadata(BaseNodeMetadataV1)
```

Class definition of QueryMetadata

**Attributes**:

- `node_type` - todo
- `node_attributes` - todo

## CollectionMetadata Objects

```python
class CollectionMetadata(BaseNodeMetadataV1)
```

Class definition of CollectionMetadata

**Attributes**:

- `node_type` - todo
- `node_attributes` - todo
