---
sidebar_label: settings
title: grai_source_cube.settings
---

## CubeApiConfig Objects

```python
class CubeApiConfig(BaseSettings)
```

### validate\_api\_url

```python
@validator("api_url")
def validate_api_url(cls, value)
```

This should end in /v1

**Arguments**:

  value:


**Returns**:



### validate\_api\_token

```python
@validator("api_token")
def validate_api_token(cls, value: Optional[SecretStr])
```



### Config Objects

```python
class Config()
```
