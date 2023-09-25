---
sidebar_label: metadata
title: grai_schemas.v1.metadata.metadata
---

## GraiNodeMetadataV1 Objects

```python
class GraiNodeMetadataV1(Metadata)
```

Class definition of GraiNodeMetadataV1

**Attributes**:

- `grai` - todo

## GraiEdgeMetadataV1 Objects

```python
class GraiEdgeMetadataV1(Metadata)
```

Class definition of GraiEdgeMetadataV1

**Attributes**:

- `grai` - todo

## SourcesNodeMetadataV1 Objects

```python
class SourcesNodeMetadataV1(Metadata)
```

Class definition of SourcesNodeMetadataV1

**Attributes**:

- `sources` - todo

## SourcesEdgeMetadataV1 Objects

```python
class SourcesEdgeMetadataV1(Metadata)
```

Class definition of SourcesEdgeMetadataV1

**Attributes**:

- `sources` - todo

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

Class definition of GraiMalformedNodeMetadataV1

**Attributes**:

- `grai` - todo
- `sources` - todo

### grai

type: ignore

## GraiMalformedEdgeMetadataV1 Objects

```python
class GraiMalformedEdgeMetadataV1(MalformedMetadata, EdgeMetadataV1)
```

Class definition of GraiMalformedEdgeMetadataV1

**Attributes**:

- `grai` - todo
- `sources` - todo

### grai

type: ignore
