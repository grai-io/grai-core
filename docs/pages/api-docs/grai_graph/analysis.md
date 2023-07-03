---
sidebar_label: analysis
title: grai_graph.analysis
---

## GraphAnalyzer Objects

```python
class GraphAnalyzer()
```



### downstream\_nodes

```python
def downstream_nodes(namespace: str, name: str)
```

**Arguments**:

  namespace (str):
  name (str):


**Returns**:



### upstream\_nodes

```python
def upstream_nodes(namespace: str, name: str)
```

**Arguments**:

  namespace (str):
  name (str):


**Returns**:



### test\_delete\_node

```python
def test_delete_node(namespace: str, name: str)
```

**Arguments**:

  namespace (str):
  name (str):


**Returns**:



### traverse\_data\_type\_violations

```python
def traverse_data_type_violations(
    node: NodeTypes,
    new_type: str,
    path: Optional[List] = None
) -> Generator[Tuple[List[NodeTypes], bool], None, None]
```

**Arguments**:

  node (NodeTypes):
  new_type (str):
- `path` _Optional[List], optional_ - (Default value = None)


**Returns**:



### test\_data\_type\_change

```python
def test_data_type_change(
        namespace: str, name: str,
        new_type: bool) -> List[Tuple[List[NodeTypes], bool]]
```

**Arguments**:

  namespace (str):
  name (str):
  new_type (bool):


**Returns**:



### traverse\_unique\_violations

```python
def traverse_unique_violations(
    node: NodeTypes,
    expects_unique: bool,
    path: Optional[List] = None
) -> Generator[Tuple[List[NodeTypes], bool], None, None]
```

**Arguments**:

  node (NodeTypes):
  expects_unique (bool):
- `path` _Optional[List], optional_ - (Default value = None)


**Returns**:



### test\_unique\_violations

```python
def test_unique_violations(
        namespace: str, name: str,
        expects_unique: bool) -> List[Tuple[List[NodeTypes], bool]]
```

**Arguments**:

  namespace (str):
  name (str):
- `expects_unique` _bool_ - can&#x27;t evaluate anything in the case of None


**Returns**:



### traverse\_null\_violations

```python
def traverse_null_violations(
    node: NodeTypes,
    is_nullable: bool,
    path: Optional[List] = None
) -> Generator[Tuple[List[NodeTypes], bool], None, None]
```

**Arguments**:

  node (NodeTypes):
  is_nullable (bool):
- `path` _Optional[List], optional_ - (Default value = None)


**Returns**:



### test\_nullable\_violations

```python
def test_nullable_violations(
        namespace: str, name: str,
        is_nullable: bool) -> List[Tuple[List[NodeTypes], bool]]
```

**Arguments**:

  namespace (str):
  name (str):
- `is_nullable` _bool_ - can&#x27;t evaluate anything in the case of None


**Returns**:



### column\_predecessors

```python
def column_predecessors(namespace: str, name: str)
```

**Arguments**:

  namespace (str):
  name (str):


**Returns**:



### column\_successors

```python
def column_successors(namespace: str, name: str)
```

**Arguments**:

  namespace (str):
  name (str):


**Returns**:
