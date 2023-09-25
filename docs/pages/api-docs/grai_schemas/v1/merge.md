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

Merge anything into a malformed metadata object

This handles cases where one might attempt to fix a malformed metadata object by merging a valid metadata object.

**Arguments**:

- `metadata` - The malformed metadata to merge into
- `other_metadata` - The metadata to merge from


**Returns**:

  A now valid piece of metadata

## merge\_malformed\_right

```python
@merge.register
def merge_malformed_right(metadata: Any, other_metadata: MalformedMetadata)
```

Merge a malformed metadata object into anything

**Arguments**:

- `metadata` - The metadata to merge into
- `other_metadata` - The malformed metadata to merge from


**Raises**:

- `ValueError` - This is always an invalid operation

## merge\_tags

```python
def merge_tags(a: Optional[list], b: Optional[list]) -> list
```

Merge two lists of tags insuring no duplicates

## merge\_grai\_node\_v1\_metadata

```python
@merge.register
def merge_grai_node_v1_metadata(
        metadata: BaseNodeMetadataV1,
        other_metadata: BaseNodeMetadataV1) -> BaseNodeMetadataV1
```

Merge two grai node metadata objects

**Arguments**:

- `metadata` - The node metadata to merge into
- `other_metadata` - The node metadata to merge from


**Returns**:

  The merged node metadata

## merge\_grai\_edge\_v1\_metadata

```python
@merge.register
def merge_grai_edge_v1_metadata(
        metadata: BaseEdgeMetadataV1,
        other_metadata: BaseEdgeMetadataV1) -> BaseEdgeMetadataV1
```

Merge two grai edge metadata objects

**Arguments**:

- `metadata` - The edge metadata to merge into
- `other_metadata` - The edge metadata to merge from


**Returns**:

  The merged edge metadata

## merge\_node\_sourced\_node

```python
@merge.register
def merge_node_sourced_node(node: NodeV1,
                            source_node: SourcedNodeV1) -> NodeV1
```

Merge a sourced node into a node

**Arguments**:

- `node` - The node to merge into
- `source_node` - The sourced node to merge from


**Returns**:

  The merged NodeV1

## merge\_edge\_sourced\_edge

```python
@merge.register
def merge_edge_sourced_edge(edge: EdgeV1,
                            source_edge: SourcedEdgeV1) -> EdgeV1
```

Merge a sourced edge into an edge

**Arguments**:

- `edge` - The edge to merge into
- `source_edge` - The sourced edge to merge from


**Returns**:

  The merged EdgeV1

## merge\_grai\_node\_into\_node\_metadata

```python
@merge.register
def merge_grai_node_into_node_metadata(
        spec: NodeSpec, source_spec: SourcedNodeSpec) -> NodeSpec
```

Merge a SourcedNodeSpec into a NodeSpec

**Arguments**:

- `spec` - The node spec to merge into
- `source_spec` - The sourced node spec to merge from


**Returns**:

  The merged node spec

## merge\_grai\_edge\_into\_edge\_metadata

```python
@merge.register
def merge_grai_edge_into_edge_metadata(
        spec: EdgeSpec, source_spec: SourcedEdgeSpec) -> EdgeSpec
```

Merge grai metadata from a sourced edge into an edge spec

**Arguments**:

- `spec` - The edge spec to merge into
- `source_spec` - The sourced edge spec to merge from


**Returns**:

  The merged edge spec
