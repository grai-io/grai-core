---
sidebar_label: merge
title: grai_schemas.v1.merge
---

## merge\_malformed\_left

```python
@merge.register
def merge_malformed_left(metadata: MalformedMetadata,
                         other_metadata: Any) -> Metadata
```



## merge\_malformed\_right

```python
@merge.register
def merge_malformed_right(metadata: Any, other_metadata: MalformedMetadata)
```



## merge\_grai\_node\_v1\_metadata

```python
@merge.register
def merge_grai_node_v1_metadata(
        metadata: BaseNodeMetadataV1,
        other_metadata: BaseNodeMetadataV1) -> BaseNodeMetadataV1
```



## merge\_grai\_edge\_v1\_metadata

```python
@merge.register
def merge_grai_edge_v1_metadata(
        metadata: BaseEdgeMetadataV1,
        other_metadata: BaseEdgeMetadataV1) -> BaseEdgeMetadataV1
```
