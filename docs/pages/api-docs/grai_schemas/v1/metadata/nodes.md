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
class BaseNodeMetadataV1(GraiBaseModel)
```



## MalformedNodeMetadataV1 Objects

```python
class MalformedNodeMetadataV1(MalformedMetadata, BaseNodeMetadataV1)
```



### node\_type

type: ignore

### node\_attributes

type: ignore

## ColumnAttributes Objects

```python
class ColumnAttributes(GenericAttributes)
```



### data\_type

This will need to be standardized

## ColumnMetadata Objects

```python
class ColumnMetadata(BaseNodeMetadataV1)
```



## TableAttributes Objects

```python
class TableAttributes(GenericAttributes)
```



## TableMetadata Objects

```python
class TableMetadata(BaseNodeMetadataV1)
```



## QueryAttributes Objects

```python
class QueryAttributes(GenericAttributes)
```



## QueryMetadata Objects

```python
class QueryMetadata(BaseNodeMetadataV1)
```
