---
sidebar_label: processor
title: grai_source_dbt.processor
---

## ManifestProcessor Objects

```python
class ManifestProcessor()
```



### adapted\_nodes

```python
@cached_property
def adapted_nodes() -> List[SourcedNodeV1]
```

**Arguments**:



**Returns**:



### adapted\_edges

```python
@cached_property
def adapted_edges() -> List[SourcedEdgeV1]
```

**Arguments**:



**Returns**:



### nodes

```python
@property
def nodes() -> List[Union[AllDbtNodeTypes, Column]]
```

**Arguments**:



**Returns**:



### edges

```python
@property
def edges() -> List[Edge]
```

**Arguments**:



**Returns**:



### manifest

```python
@property
def manifest() -> ManifestTypes
```

**Arguments**:



**Returns**:



### load

```python
@classmethod
def load(cls, manifest_obj: Union[str, dict], namespace: str,
         source: SourceSpec) -> "ManifestProcessor"
```

**Arguments**:

  manifest_obj (Union[str, dict]):
  namespace (str):


**Returns**:
