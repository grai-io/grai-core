---
sidebar_label: adapters
title: grai_source_looker.adapters
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



## build\_grai\_metadata\_from\_dashboard

```python
@build_grai_metadata.register
def build_grai_metadata_from_dashboard(current: Dashboard,
                                       version: Literal["v1"] = "v1"
                                       ) -> TableMetadata
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## build\_grai\_metadata\_from\_query

```python
@build_grai_metadata.register
def build_grai_metadata_from_query(current: Query,
                                   version: Literal["v1"] = "v1"
                                   ) -> ColumnMetadata
```

**Arguments**:

  current (Query):
- `version` _Literal[&quot;v1&quot;], optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## build\_grai\_metadata\_from\_explore

```python
@build_grai_metadata.register
def build_grai_metadata_from_explore(current: Explore,
                                     version: Literal["v1"] = "v1"
                                     ) -> TableMetadata
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## build\_grai\_metadata\_from\_dimension

```python
@build_grai_metadata.register
def build_grai_metadata_from_dimension(current: Dimension,
                                       version: Literal["v1"] = "v1"
                                       ) -> ColumnMetadata
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## build\_grai\_metadata\_from\_edge

```python
@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge,
                                  version: Literal["v1"] = "v1"
                                  ) -> BaseEdgeMetadataV1
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


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



## build\_metadata\_from\_dashboard

```python
@build_app_metadata.register
def build_metadata_from_dashboard(current: Dashboard,
                                  version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## build\_metadata\_from\_query

```python
@build_app_metadata.register
def build_metadata_from_query(current: Query,
                              version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## build\_metadata\_from\_explore

```python
@build_app_metadata.register
def build_metadata_from_explore(current: Explore,
                                version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## build\_metadata\_from\_dimension

```python
@build_app_metadata.register
def build_metadata_from_dimension(current: Dimension,
                                  version: Literal["v1"] = "v1") -> Dict
```

**Arguments**:

  current:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## build\_metadata\_from\_edge

```python
@build_app_metadata.register
def build_metadata_from_edge(current: Edge,
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



## adapt\_to\_client

```python
@multimethod
def adapt_to_client(current: Any, desired: Any)
```

**Arguments**:

  current:
  desired:


**Returns**:



## adapt\_dashboard\_to\_client

```python
@adapt_to_client.register
def adapt_dashboard_to_client(current: Dashboard, source: SourceSpec,
                              version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_query\_to\_client

```python
@adapt_to_client.register
def adapt_query_to_client(current: Query, source: SourceSpec,
                          version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_explore\_to\_client

```python
@adapt_to_client.register
def adapt_explore_to_client(current: Explore, source: SourceSpec,
                            version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## adapt\_dimension\_to\_client

```python
@adapt_to_client.register
def adapt_dimension_to_client(current: Dimension, source: SourceSpec,
                              version: Literal["v1"]) -> SourcedNodeV1
```

**Arguments**:

  current:
  source:
- `version` - (Default value = &quot;v1&quot;)


**Returns**:



## make\_name

```python
def make_name(node1: ID, node2: ID) -> str
```

**Arguments**:

  node1:
  node2:


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
