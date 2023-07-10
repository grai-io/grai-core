---
sidebar_label: update
title: grai_client.update
---

## compute\_graph\_changes

```python
def compute_graph_changes(
        items: List[T],
        active_items: List[T]) -> Tuple[List[T], List[T], List[T]]
```

**Arguments**:

  items:
  active_items:


**Returns**:



## update

```python
def update(client: BaseClient,
           items: List[Union[SourcedNodeV1, SourcedEdgeV1]],
           active_items: Optional[List[T]] = None,
           source: Optional[Union[SourceV1, SourceSpec]] = None)
```

**Arguments**:

  client:
  items:
- `active_items` - (Default value = None)
- `source` - (Default value = None)


**Returns**:
