---
sidebar_label: api
title: grai_source_cube.api
---

## TokenAuth Objects

```python
class TokenAuth(AuthBase)
```

Implements a custom authentication scheme.

## BaseCubeAPI Objects

```python
class BaseCubeAPI(ABC)
```



### meta

```python
@abstractmethod
def meta() -> MetaResponseSchema
```



### ready

```python
@abstractmethod
def ready() -> requests.Response
```



## CubeAPI Objects

```python
class CubeAPI(BaseCubeAPI)
```



### meta

```python
def meta() -> MetaResponseSchema
```



### ready

```python
def ready() -> requests.Response
```
