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



## BaseNodeMetadataV1 Objects

```python
class BaseNodeMetadataV1(V1Mixin)
```



## MalformedNodeMetadataV1 Objects

```python
class MalformedNodeMetadataV1(MalformedMetadata, BaseNodeMetadataV1)
```



## ColumnAttributes Objects

```python
class ColumnAttributes(V1Mixin, GenericAttributes)
```



### data\_type

This will need to be standardized

## ColumnMetadata Objects

```python
class ColumnMetadata(BaseNodeMetadataV1)
```



## TableAttributes Objects

```python
class TableAttributes(V1Mixin, GenericAttributes)
```



## TableMetadata Objects

```python
class TableMetadata(BaseNodeMetadataV1)
```



## QueryAttributes Objects

```python
class QueryAttributes(V1Mixin, GenericAttributes)
```



## QueryMetadata Objects

```python
class QueryMetadata(BaseNodeMetadataV1)
```
