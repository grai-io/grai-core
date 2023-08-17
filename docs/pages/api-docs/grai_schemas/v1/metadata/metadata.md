---
sidebar_label: metadata
title: grai_schemas.v1.metadata.metadata
---

## GraiNodeMetadataV1 Objects

```python
class GraiNodeMetadataV1(Metadata)
```



## GraiEdgeMetadataV1 Objects

```python
class GraiEdgeMetadataV1(Metadata)
```



## SourcesNodeMetadataV1 Objects

```python
class SourcesNodeMetadataV1(Metadata)
```



## SourcesEdgeMetadataV1 Objects

```python
class SourcesEdgeMetadataV1(Metadata)
```



## NodeMetadataV1 Objects

```python
class NodeMetadataV1(GraiNodeMetadataV1, SourcesNodeMetadataV1)
```



## EdgeMetadataV1 Objects

```python
class EdgeMetadataV1(GraiEdgeMetadataV1, SourcesEdgeMetadataV1)
```



## GraiMalformedNodeMetadataV1 Objects

```python
class GraiMalformedNodeMetadataV1(MalformedMetadata, NodeMetadataV1)
```



### grai

type: ignore

## GraiMalformedEdgeMetadataV1 Objects

```python
class GraiMalformedEdgeMetadataV1(MalformedMetadata, EdgeMetadataV1)
```



### grai

type: ignore
