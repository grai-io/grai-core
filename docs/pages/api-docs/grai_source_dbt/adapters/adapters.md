---
sidebar_label: adapters
title: grai_source_dbt.adapters.adapters
---

## build\_grai\_metadata

```python
@multimethod
def build_grai_metadata(current: Any, version: Any) -> None
```

**Arguments**:

  current (Any):
  version (Any):


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
def build_grai_metadata_from_node(
        current: AllDbtNodeTypes,
        version: Literal["v1"] = "v1") -> TableMetadata
```

**Arguments**:

  current (AllDbtNodeTypes):
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
def build_app_metadata(current: Any, version: Any) -> None
```

**Arguments**:

  current (Any):
  version (Any):


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
def build_metadata_from_node(current: AllDbtNodeTypes,
                             version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current (AllDbtNodeTypes):
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
def adapt_to_client(current: Any, version: Any) -> None
```

**Arguments**:

  current (Any):
  version (Any):


**Returns**:



## adapt\_table\_to\_client

```python
@adapt_to_client.register
def adapt_table_to_client(current: AllDbtNodeTypes, source: SourceSpec,
                          version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current (AllDbtNodeTypes):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_column\_to\_client

```python
@adapt_to_client.register
def adapt_column_to_client(current: Column, source: SourceSpec,
                           version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current (Column):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_edge\_to\_client

```python
@adapt_to_client.register
def adapt_edge_to_client(current: Edge, source: SourceSpec,
                         version: Literal["v1"]) -> SourcedEdgeV1
```

**Arguments**:

  current (Edge):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_list\_to\_client

```python
@adapt_to_client.register
def adapt_list_to_client(
        objs: Sequence, source: SourceSpec,
        version: Literal["v1"]) -> List[Union[SourcedNodeV1, SourcedEdgeV1]]
```

**Arguments**:

  objs (Sequence):
  version (Literal[&quot;v1&quot;]):


**Returns**:



## adapt\_to\_client\_default\_version

```python
@adapt_to_client.register
def adapt_to_client_default_version(obj: Any, source: SourceV1)
```

**Arguments**:

  obj (Any):


**Returns**:
