---
sidebar_label: adapters
title: grai_source_fivetran.adapters
---

## build\_grai\_metadata

```python
@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None
```

**Arguments**:

  current (Any):
  desired (Any):


**Returns**:



## build\_grai\_metadata\_from\_column

```python
@build_grai_metadata.register
def build_grai_metadata_from_column(current: Column,
                                    version: Literal["v1"] = "v1"
                                    ) -> ColumnMetadata
```

**Arguments**:

  current (Column):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## build\_grai\_metadata\_from\_node

```python
@build_grai_metadata.register
def build_grai_metadata_from_node(current: Table,
                                  version: Literal["v1"] = "v1"
                                  ) -> TableMetadata
```

**Arguments**:

  current (Table):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## build\_grai\_metadata\_from\_edge

```python
@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge,
                                  version: Literal["v1"] = "v1"
                                  ) -> GenericEdgeMetadataV1
```

**Arguments**:

  current (Edge):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## build\_app\_metadata

```python
@multimethod
def build_app_metadata(current: Any, desired: Any) -> None
```

**Arguments**:

  current (Any):
  desired (Any):


**Returns**:



## build\_metadata\_from\_column

```python
@build_app_metadata.register
def build_metadata_from_column(current: Column,
                               version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current (Column):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## build\_metadata\_from\_edge

```python
@build_app_metadata.register
def build_metadata_from_edge(current: Edge,
                             version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current (Edge):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## build\_metadata\_from\_node

```python
@build_app_metadata.register
def build_metadata_from_node(current: Table,
                             version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current (Table):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## build\_metadata

```python
def build_metadata(obj, version)
```

**Arguments**:

  obj:
  version:


**Returns**:



## adapt\_to\_client

```python
@multimethod
def adapt_to_client(current: Any, desired: Any)
```

**Arguments**:

  current (Any):
  desired (Any):


**Returns**:



## adapt\_column\_to\_client

```python
@adapt_to_client.register
def adapt_column_to_client(current: Column, source: SourceSpec,
                           version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_table\_to\_client

```python
@adapt_to_client.register
def adapt_table_to_client(current: Table, source: SourceSpec,
                          version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## make\_name

```python
def make_name(node1: NodeTypes, node2: NodeTypes) -> str
```

**Arguments**:

  node1 (NodeTypes):
  node2 (NodeTypes):


**Returns**:



## adapt\_edge\_to\_client

```python
@adapt_to_client.register
def adapt_edge_to_client(current: Edge, source: SourceSpec,
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
        objs: Sequence, source: SourceSpec,
        version: Literal["v1"]) -> List[Union[SourcedNodeV1, SourcedEdgeV1]]
```

**Arguments**:

  objs:
  version:


**Returns**:



## adapt\_list\_to\_client

```python
@adapt_to_client.register
def adapt_list_to_client(
        objs: List, source: SourceSpec,
        version: Literal["v1"]) -> List[Union[SourcedNodeV1, SourcedEdgeV1]]
```

**Arguments**:

  objs:
  source:
  version:


**Returns**:
