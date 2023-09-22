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



## merge\_node\_sourced\_node

```python
@merge.register
def merge_node_sourced_node(node: NodeV1,
                            source_node: SourcedNodeV1) -> NodeV1
```



## merge\_edge\_sourced\_edge

```python
@merge.register
def merge_edge_sourced_edge(edge: EdgeV1,
                            source_edge: SourcedEdgeV1) -> EdgeV1
```



## merge\_grai\_node\_into\_node\_metadata

```python
@merge.register
def merge_grai_node_into_node_metadata(
        spec: NodeSpec, source_spec: SourcedNodeSpec) -> NodeSpec
```



## merge\_grai\_edge\_into\_edge\_metadata

```python
@merge.register
def merge_grai_edge_into_edge_metadata(
        spec: EdgeSpec, source_spec: SourcedEdgeSpec) -> NodeSpec
```
