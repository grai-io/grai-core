---
sidebar_label: nodes
title: grai_schemas.v1.metadata.nodes
---

## NodeMetadataTypeLabels Objects

```python
class NodeMetadataTypeLabels(Enum)
```



## SourceType Objects

```python
class SourceType(Enum)
```



## GenericNodeMetadataV1 Objects

```python
class GenericNodeMetadataV1(V1Mixin)
```



## ColumnAttributes Objects

```python
class ColumnAttributes(GraiBaseModel)
```



#### data\_type

This will need to be standardized

## ColumnMetadata Objects

```python
class ColumnMetadata(GenericNodeMetadataV1)
```



## TableAttributes Objects

```python
class TableAttributes(HashableBaseModel)
```



## TableMetadata Objects

```python
class TableMetadata(GenericNodeMetadataV1)
```
