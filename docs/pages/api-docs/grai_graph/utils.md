---
sidebar_label: utils
title: grai_graph.utils
---

## TestNodeObj Objects

```python
class TestNodeObj(BaseModel)
```



#### mock\_v1\_node

```python
def mock_v1_node(node: Union[str, TestNodeObj])
```

**Arguments**:

  node (Union[str, TestNodeObj]):


**Returns**:



#### mock\_v1\_edge

```python
def mock_v1_edge(source_node: Union[str, TestNodeObj],
                 destination_node: Union[str, TestNodeObj],
                 metadata={})
```

**Arguments**:

  source_node (Union[str, TestNodeObj]):
  destination_node (Union[str, TestNodeObj]):
- `metadata` - (Default value = {})


**Returns**:



#### build\_graph\_from\_map

```python
def build_graph_from_map(
    map: Dict[Union[str, TestNodeObj], List[Tuple[str,
                                                  ColumnToColumnAttributes]]]
) -> graph.Graph
```

**Arguments**:

  map (Dict[Union[str, TestNodeObj]):
  List]]]:


**Returns**:



#### get\_analysis\_from\_map

```python
def get_analysis_from_map(
    map: Dict[Union[str, TestNodeObj], Dict[ColumnToColumnAttributes,
                                            List[str]]]
) -> analysis.GraphAnalyzer
```

**Arguments**:

  map (Dict[Union[str, TestNodeObj]):
  Dict]]]:


**Returns**:
