---
sidebar_label: adapters
title: grai_source_cube.adapters
---

## build\_grai\_metadata

```python
@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None
```

**Arguments**:

  current:
  desired:


**Returns**:



## build\_grai\_metadata\_from\_dimension

```python
@build_grai_metadata.register
def build_grai_metadata_from_dimension(
        current: DimensionNode, version: Literal["v1"]) -> ColumnMetadata
```

**Arguments**:

  current:
  version:


**Returns**:



## build\_grai\_metadata\_from\_measure

```python
@build_grai_metadata.register
def build_grai_metadata_from_measure(current: MeasureNode,
                                     version: Literal["v1"]) -> ColumnMetadata
```

**Arguments**:

  current:
  version:


**Returns**:



## build\_grai\_metadata\_from\_node

```python
@build_grai_metadata.register
def build_grai_metadata_from_node(current: Union[CubeNode, SourceNode],
                                  version: Literal["v1"]) -> TableMetadata
```

**Arguments**:

  current:
  version:


**Returns**:



## build\_app\_metadata

```python
@multimethod
def build_app_metadata(current: Any, desired: Any) -> None
```

**Arguments**:

  current:
  desired:


**Returns**:



## build\_metadata\_from\_node

```python
@build_app_metadata.register
def build_metadata_from_node(current: CubeNodeTypes,
                             version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## build\_metadata\_from\_edge

```python
@build_app_metadata.register
def build_metadata_from_edge(current: CubeEdgeTypes,
                             version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## build\_metadata

```python
def build_metadata(obj, version)
```

**Arguments**:

  obj:
  version:


**Returns**:



## unsupported\_arguments

```python
@adapt_to_client.register
def unsupported_arguments(current: Any, source: Any, version: Any) -> None
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_source\_to\_client

```python
@adapt_to_client.register
def adapt_source_to_client(current: SourceNode, source: SourceSpec,
                           version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_column\_to\_client

```python
@adapt_to_client.register
def adapt_column_to_client(current: Union[MeasureNode, DimensionNode,
                                          CubeNode], source: SourceSpec,
                           version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## make\_name

```python
def make_name(node1: BaseNode, node2: BaseNode) -> str
```

**Arguments**:

  node1:
  node2:


**Returns**:



## adapt\_edge\_to\_client

```python
@adapt_to_client.register
def adapt_edge_to_client(current: BaseCubeEdge, source: SourceSpec,
                         version: Literal["v1"]) -> SourcedEdgeV1
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_seq\_to\_client

```python
@adapt_to_client.register
def adapt_seq_to_client(
        objs: Union[Sequence, List, Tuple], source: SourceSpec,
        version: Literal["v1"]) -> List[Union[SourcedNodeV1, SourcedEdgeV1]]
```

**Arguments**:

  objs:
  source:
  version:


**Returns**:
