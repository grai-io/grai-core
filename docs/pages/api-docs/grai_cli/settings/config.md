---
sidebar_label: config
title: grai_cli.settings.config
---

## unredact

```python
def unredact(obj: Any) -> Any
```

**Arguments**:

  obj (Any):


**Returns**:



## ServerSettingsV1 Objects

```python
class ServerSettingsV1(BaseModel)
```



### Config Objects

```python
class Config()
```



## AuthModeSettings Objects

```python
class AuthModeSettings(BaseModel)
```



### Config Objects

```python
class Config()
```



## BasicAuthSettings Objects

```python
class BasicAuthSettings(AuthModeSettings)
```



## ApiKeySettings Objects

```python
class ApiKeySettings(AuthModeSettings)
```



## ContextSettings Objects

```python
class ContextSettings(BaseModel)
```



## BaseGraiConfig Objects

```python
class BaseGraiConfig(LazyConfig)
```

### save

```python
def save(save_path: Optional[str] = None)
```



### view

```python
def view()
```
