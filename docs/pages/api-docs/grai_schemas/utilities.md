---
sidebar_label: utilities
title: grai_schemas.utilities
---

## unpack\_object

```python
def unpack_object(obj: Union[Dict, BaseModel]) -> Dict
```

**Arguments**:

- `obj` - The object to unpack, generally a dict or BaseModel


**Returns**:



## merge

```python
@multimethod
def merge(a, b)
```

The base merge function

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:



## merge\_atomic

```python
@merge.register
def merge_atomic(a: Any, b: T) -> T
```

Merge an atomic value with any other value

This function effectively handles cases where a value is being replaced.
For example, if the value integer `5` needed to be updated to `6`, this function would handle that.

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:

  The new value


## merge\_missing

```python
@merge.register
def merge_missing(a: T, b: None) -> T
```

Merge an object with a missing value

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:

  The original object


## merge\_dict\_item

```python
@merge.register
def merge_dict_item(a: Dict, b: Dict) -> Dict
```

Merge two dictionaries

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:

  The merged dictionary


## merge\_list

```python
@merge.register
def merge_list(a: list, b: list) -> list
```

Merge two lists

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:

  A merged list


## merge\_tuple

```python
@merge.register
def merge_tuple(a: tuple, b: tuple) -> tuple
```

Merge two tuples

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:

  A merged tuple


## merge\_set

```python
@merge.register
def merge_set(a: set, b: set) -> set
```

Merge two sets

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:

  A merged set


## merge\_pydantic

```python
@merge.register
def merge_pydantic(a: BaseModel, b: Any) -> BaseModel
```

Merge a non-pydantic object into a pydantic model

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:

  An updated pydantic model


## merge\_pydantic\_right

```python
@merge.register
def merge_pydantic_right(a: T, b: BaseModel) -> T
```

Merge a pydantic model into a non-pydantic model

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:

  An updated non-pydantic model


## merge\_models

```python
def merge_models(a: T, b: T) -> T
```

This function is deprecated. Use `merge` instead

**Arguments**:

- `a` - The first object to merge
- `b` - The second object to merge


**Returns**:

  An updated model


## compute\_graph\_changes

```python
def compute_graph_changes(
    items: List[SpecProto], active_items: List[SpecProto]
) -> Tuple[List[SpecProto], List[SpecProto], List[SpecProto]]
```

Computes a graph update for a list of items and the corresponding set of currently active items.

**Arguments**:

- `items` - The new list of graph nodes
- `active_items` - The current list of graph nodes. This does not have to be the full graph, only those relevant to the items set. Most commonly, these are drawn from the same data source.


**Returns**:

  A three tuple of new items, updated items, and deleted items.
