---
sidebar_label: utilities
title: grai_schemas.utilities
---

#### unpack\_object

```python
def unpack_object(obj: Union[Dict, BaseModel]) -> Dict
```

**Arguments**:

  obj (Union[Dict, BaseModel]):


**Returns**:



#### merge

```python
@multimethod
def merge(a, b)
```

**Arguments**:

  a:
  b:


**Returns**:



#### merge\_atomic

```python
@merge.register
def merge_atomic(a: Any, b: T) -> T
```

**Arguments**:

  a (Any):
  b (T):


**Returns**:



#### merge\_missing

```python
@merge.register
def merge_missing(a: T, b: None) -> T
```

**Arguments**:

  a (T):
  b (None):


**Returns**:



#### merge\_dicts

```python
@merge.register
def merge_dicts(a: dict, b: dict) -> dict
```

**Arguments**:

  a (dict):
  b (dict):


**Returns**:



#### merge\_list

```python
@merge.register
def merge_list(a: list, b: list) -> list
```

**Arguments**:

  a (list):
  b (list):


**Returns**:



#### merge\_tuple

```python
@merge.register
def merge_tuple(a: tuple, b: tuple) -> tuple
```

**Arguments**:

  a (tuple):
  b (tuple):


**Returns**:



#### merge\_set

```python
@merge.register
def merge_set(a: set, b: set) -> set
```

**Arguments**:

  a (set):
  b (set):


**Returns**:



#### merge\_pydantic

```python
@merge.register
def merge_pydantic(a: BaseModel, b: Any) -> BaseModel
```

**Arguments**:

  a (BaseModel):
  b (Any):


**Returns**:



#### merge\_pydantic\_right

```python
@merge.register
def merge_pydantic_right(a: T, b: BaseModel) -> T
```

**Arguments**:

  a (T):
  b (BaseModel):


**Returns**:



#### merge\_models

```python
def merge_models(a: T, b: T) -> T
```

This function is deprecated. Use `merge` instead

**Arguments**:

  a (T):
  b (T):


**Returns**:
