---
sidebar_label: mock_tools
title: grai_source_fivetran.mock_tools
---

#### faker\_dep\_wrapper

```python
def faker_dep_wrapper(fn: Callable[..., T])
```

**Arguments**:

  fn (Callable[..., T]):


**Returns**:



## MockFivetranObjects Objects

```python
class MockFivetranObjects()
```



#### mock\_column

```python
@staticmethod
@faker_dep_wrapper
def mock_column()
```



#### mock\_table

```python
@staticmethod
@faker_dep_wrapper
def mock_table()
```



#### mock\_edge

```python
@classmethod
@faker_dep_wrapper
def mock_edge(cls, type: str = "cc")
```

**Arguments**:

- `type` _str, optional_ - (Default value = &quot;cc&quot;)


**Returns**:
