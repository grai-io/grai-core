---
sidebar_label: mock_tools
title: grai_source_looker.mock_tools
---

## faker\_dep\_wrapper

```python
def faker_dep_wrapper(fn: Callable[..., T])
```

**Arguments**:

  fn (Callable[..., T]):


**Returns**:



## MockLookerObjects Objects

```python
class MockLookerObjects()
```



### mock\_query

```python
@staticmethod
@faker_dep_wrapper
def mock_query()
```



### mock\_dashboard

```python
@staticmethod
@faker_dep_wrapper
def mock_dashboard()
```



### mock\_edge

```python
@classmethod
@faker_dep_wrapper
def mock_edge(cls, type: str = "cc")
```

**Arguments**:

- `type` _str, optional_ - (Default value = &quot;cc&quot;)


**Returns**:
