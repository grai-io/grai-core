---
sidebar_label: mock_tools
title: grai_source_metabase.mock_tools
---

## faker\_dep\_wrapper

```python
def faker_dep_wrapper(fn: Callable[..., T])
```

**Arguments**:

  fn (Callable[..., T]):


**Returns**:



## MockMetabaseObjects Objects

```python
class MockMetabaseObjects()
```



### mock\_question

```python
@staticmethod
@faker_dep_wrapper
def mock_question()
```



### mock\_table

```python
@staticmethod
@faker_dep_wrapper
def mock_table()
```



### mock\_edge

```python
@classmethod
@faker_dep_wrapper
def mock_edge(cls, type: str = "tq")
```

**Arguments**:

- `type` _str, optional_ - (Default value = &quot;tq&quot;)


**Returns**:
