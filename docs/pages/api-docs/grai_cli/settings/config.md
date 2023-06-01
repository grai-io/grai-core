---
sidebar_label: config
title: grai_cli.settings.config
---

## ConfigDirHandler Objects

```python
class ConfigDirHandler()
```



#### config\_content

```python
@property
def config_content()
```



#### config\_content

```python
@config_content.setter
def config_content(value: Dict)
```

**Arguments**:

  value (Dict):


**Returns**:



#### save\_content

```python
def save_content()
```



#### get\_config\_dir

```python
def get_config_dir() -> str
```

**Arguments**:



**Returns**:



#### get\_config\_file

```python
def get_config_file() -> Optional[str]
```

**Arguments**:



**Returns**:



#### unredact

```python
def unredact(obj: Any) -> Any
```

**Arguments**:

  obj (Any):


**Returns**:



#### yaml\_config\_settings\_source

```python
def yaml_config_settings_source(settings: BaseSettings) -> dict[str, Any]
```

**Arguments**:

  settings (BaseSettings):


**Returns**:



## ServerSettingsV1 Objects

```python
class ServerSettingsV1(BaseModel)
```



## Config Objects

```python
class Config()
```



## AuthModeSettings Objects

```python
class AuthModeSettings(BaseModel)
```



## Config Objects

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



## GraiConfig Objects

```python
class GraiConfig(YamlModelMixin, BaseSettings)
```



#### save

```python
def save()
```



#### view

```python
def view()
```



## Config Objects

```python
class Config()
```



#### customise\_sources

```python
@classmethod
def customise_sources(cls, init_settings, env_settings, file_secret_settings)
```

**Arguments**:

  init_settings:
  env_settings:
  file_secret_settings:


**Returns**:
