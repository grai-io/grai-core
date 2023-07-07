---
sidebar_label: graph
title: grai_graph.graph
---

## GraphManifest Objects

```python
class GraphManifest()
```



### get\_node

```python
def get_node(namespace: str, name: str) -> Optional[NodeTypes]
```

**Arguments**:

  namespace (str):
  name (str):


**Returns**:



## Graph Objects

```python
class Graph()
```



### add\_nodes\_from\_manifest

```python
def add_nodes_from_manifest()
```



### add\_edges\_from\_manifest

```python
def add_edges_from_manifest()
```



### get\_node\_id

```python
@lru_cache
def get_node_id(namespace: str, name: str) -> Optional[int]
```

**Arguments**:

  namespace (str):
  name (str):


**Returns**:



### get\_node

```python
def get_node(namespace: Optional[str] = None,
             name: Optional[str] = None,
             node_id: Optional[int] = None) -> GraiType
```

**Arguments**:

- `namespace` _Optional[str], optional_ - (Default value = None)
- `name` _Optional[str], optional_ - (Default value = None)
- `node_id` _Optional[int], optional_ - (Default value = None)


**Returns**:



### label

```python
def label(namespace: str, name: str) -> str
```

**Arguments**:

  namespace (str):
  name (str):


**Returns**:



### id\_label

```python
def id_label(node_id: int) -> str
```

**Arguments**:

  node_id (int):


**Returns**:



### relabeled\_graph

```python
def relabeled_graph()
```



## process\_items

```python
@multimethod
def process_items(vals: Any, version: Any, type: Any) -> List[GraiType]
```

**Arguments**:

  vals (Any):
  version (Any):
  type (Any):


**Returns**:



## process\_dict

```python
@process_items.register
def process_dict(dict_item: Dict, version: str, type: str) -> GraiType
```

**Arguments**:

  dict_item (Dict):
  version (str):
  type (str):


**Returns**:



## process\_node

```python
@process_items.register
def process_node(item: GraiType, version: str, type: str) -> GraiType
```

**Arguments**:

  item (GraiType):
  version (str):
  type (str):


**Returns**:



## process\_sequence

```python
@process_items.register
def process_sequence(item_iter: Sequence, version: str,
                     type: str) -> List[GraiType]
```

**Arguments**:

  item_iter (Sequence):
  version (str):
  type (str):


**Returns**:



## build\_graph

```python
def build_graph(nodes: List[Dict], edges: List[Dict], version: str) -> Graph
```

**Arguments**:

  nodes (List[Dict]):
  edges (List[Dict]):
  version (str):


**Returns**:
