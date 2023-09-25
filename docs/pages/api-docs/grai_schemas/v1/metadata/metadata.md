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

- `grai` - Grai defined operation attributes

## GraiEdgeMetadataV1 Objects

```python
class GraiEdgeMetadataV1(Metadata)
```

Class definition of GraiEdgeMetadataV1

**Attributes**:

- `grai` - Grai defined operation attributes

## SourcesNodeMetadataV1 Objects

```python
class SourcesNodeMetadataV1(Metadata)
```

Class definition of SourcesNodeMetadataV1

**Attributes**:

- `sources` - A dictionary of source names to source metadata

## SourcesEdgeMetadataV1 Objects

```python
class SourcesEdgeMetadataV1(Metadata)
```

Class definition of SourcesEdgeMetadataV1

**Attributes**:

- `sources` - A dictionary of source names to source metadata

## NodeMetadataV1 Objects

```python
class NodeMetadataV1(GraiNodeMetadataV1, SourcesNodeMetadataV1)
```

Class definition of NodeMetadataV1

## EdgeMetadataV1 Objects

```python
class EdgeMetadataV1(GraiEdgeMetadataV1, SourcesEdgeMetadataV1)
```

Class definition of EdgeMetadataV1

## GraiMalformedNodeMetadataV1 Objects

```python
class GraiMalformedNodeMetadataV1(MalformedMetadata, NodeMetadataV1)
```

Class definition of GraiMalformedNodeMetadataV1

**Attributes**:

- `grai` - Grai defined operation attributes
- `sources` - A dictionary of source names to source metadata

### grai

type: ignore

## GraiMalformedEdgeMetadataV1 Objects

```python
class GraiMalformedEdgeMetadataV1(MalformedMetadata, EdgeMetadataV1)
```

Class definition of GraiMalformedEdgeMetadataV1

**Attributes**:

- `grai` - Grai defined operation attributes
- `sources` - A dictionary of source names to source metadata

### grai

type: ignore
