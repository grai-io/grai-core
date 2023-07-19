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



## MalformedEdgeMetadataV1 Objects

```python
class MalformedEdgeMetadataV1(MalformedMetadata, BaseEdgeMetadataV1)
```

### edge\_type

type: ignore

### edge\_attributes

type: ignore

## TableToColumnAttributes Objects

```python
class TableToColumnAttributes(GenericAttributes)
```



## TableToColumnMetadata Objects

```python
class TableToColumnMetadata(BaseEdgeMetadataV1)
```



## TableToTableAttributes Objects

```python
class TableToTableAttributes(GenericAttributes)
```



## TableToTableMetadata Objects

```python
class TableToTableMetadata(BaseEdgeMetadataV1)
```



## ColumnToColumnAttributes Objects

```python
class ColumnToColumnAttributes(GenericAttributes)
```



## ColumnToColumnMetadata Objects

```python
class ColumnToColumnMetadata(BaseEdgeMetadataV1)
```
