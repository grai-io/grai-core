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
@multimethod
def update(*args, **kwargs)
```

**Arguments**:

  client:
  items:
- `active_items` - (Default value = None)

## update

```python
@multimethod
def update(client: BaseClient,
           items: List[Union[NodeV1, EdgeV1]],
           active_items: Any = None,
           source: Any = None)
```

**Arguments**:

  client:
  items:
- `active_items` - (Default value = None)


**Returns**:



## update

```python
@update.register
def update(client: BaseClient,
           items: List[T],
           active_items: Optional[List[T]] = None,
           source: Optional[SourceSpec] = None)
```

**Arguments**:

  client:
  items:
- `active_items` - (Default value = None)
- `source` - (Default value = None)


**Returns**:
