---
sidebar_label: adapters
title: grai_source_flat_file.adapters
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
                                  ) -> TableToColumnMetadata
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
def adapt_column_to_client(current: Union[Table, Column],
                           version: Literal["v1"] = "v1")
```

**Arguments**:

  current (Union[Table, Column]):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## make\_name

```python
def make_name(node1: ID, node2: ID) -> str
```

**Arguments**:

  node1 (ID):
  node2 (ID):


**Returns**:



## adapt\_column\_to\_client

```python
@adapt_to_client.register
def adapt_column_to_client(current: Edge, version: Literal["v1"] = "v1")
```

**Arguments**:

  current (Edge):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_list\_to\_client

```python
@adapt_to_client.register
def adapt_list_to_client(objs: Sequence,
                         version: Literal["v1"] = "v1") -> List
```

**Arguments**:

  objs (Sequence):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:
