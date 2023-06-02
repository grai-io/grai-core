---
sidebar_label: client
title: grai_client.endpoints.client
---

## ClientOptions Objects

```python
class ClientOptions(BaseModel)
```



## validate\_connection\_arguments

```python
def validate_connection_arguments(
    url: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    protocol: Optional[ProtocolType] = None,
    insecure: Optional[bool] = None
) -> Tuple[str, str, Optional[str], ProtocolType, bool]
```

**Arguments**:

- `url` _Optional[str], optional_ - (Default value = None)
- `host` _Optional[str], optional_ - (Default value = None)
- `port` _Optional[str], optional_ - (Default value = None)
- `protocol` _Optional[ProtocolType], optional_ - (Default value = None)
- `insecure` _Optional[bool], optional_ - (Default value = None)


**Returns**:



## AuthValues Objects

```python
class AuthValues(BaseModel)
```



### is\_valid

```python
def is_valid() -> bool
```

**Arguments**:



**Returns**:



### get\_auth

```python
def get_auth() -> Auth
```

**Arguments**:



**Returns**:



## async\_requires\_auth

```python
def async_requires_auth(func)
```

**Arguments**:

  func:


**Returns**:



## requires\_auth

```python
def requires_auth(func)
```

**Arguments**:

  func:


**Returns**:



## BaseClient Objects

```python
class BaseClient(abc.ABC)
```



### get\_session

```python
def get_session() -> httpx.Client
```

**Arguments**:



**Returns**:



### default\_options

```python
@property
def default_options() -> ClientOptions
```

**Arguments**:



**Returns**:



### server\_health\_status

```python
def server_health_status() -> Response
```

**Arguments**:



**Returns**:



### auth

```python
@property
def auth() -> Auth
```

**Arguments**:



**Returns**:



### auth

```python
@auth.setter
def auth(auth: Auth) -> None
```

**Arguments**:

  auth (Auth):


**Returns**:



### authenticate

```python
def authenticate(username: Optional[str] = None,
                 password: Optional[str] = None,
                 api_key: Optional[str] = None) -> None
```

**Arguments**:

- `username` _Optional[str], optional_ - (Default value = None)
- `password` _Optional[str], optional_ - (Default value = None)
- `api_key` _Optional[str], optional_ - (Default value = None)


**Returns**:



### check\_authentication

```python
@abc.abstractmethod
def check_authentication() -> Response
```

**Arguments**:



**Returns**:



### get\_url

```python
@multimethod
def get_url(grai_type: Any) -> str
```

**Arguments**:

  grai_type (Any):


**Returns**:



### session\_manager

```python
def session_manager(func: Callable,
                    *args,
                    options: Optional[OptionType] = None,
                    **kwargs)
```

**Arguments**:

  func (Callable):
  *args:
- `options` _Optional[OptionType], optional_ - (Default value = None)
  **kwargs:


**Returns**:



### get

```python
@requires_auth
def get(*args, options: Optional[OptionType] = None, **kwargs)
```

**Arguments**:

  *args:
- `options` _Optional[OptionType], optional_ - (Default value = None)
  **kwargs:


**Returns**:



### post

```python
@requires_auth
def post(*args, options: Optional[OptionType] = None, **kwargs)
```

**Arguments**:

  *args:
- `options` _Optional[OptionType], optional_ - (Default value = None)
  **kwargs:


**Returns**:



### patch

```python
@requires_auth
def patch(*args, options: Optional[OptionType] = None, **kwargs)
```

**Arguments**:

  *args:
- `options` _Optional[OptionType], optional_ - (Default value = None)
  **kwargs:


**Returns**:



### delete

```python
@requires_auth
def delete(*args, options: Optional[OptionType] = None, **kwargs)
```

**Arguments**:

  *args:
- `options` _Optional[OptionType], optional_ - (Default value = None)
  **kwargs:


**Returns**:



## type\_segmentation

```python
def type_segmentation(
    objs: Sequence, priority_order: Optional[Tuple[Type[T]]]
) -> List[Tuple[List[int], Union[Sequence[T], Iterable[T]], Type[T]]]
```

**Arguments**:

  objs (Sequence):
  priority_order (Optional[Tuple[Type[T]]]):


**Returns**:



## segmented\_caller

```python
def segmented_caller(
    func: Callable[[BaseClient, Sequence[T], ClientOptions], R],
    priority_order: Optional[Tuple] = None
) -> Callable[[BaseClient, Sequence[T], ClientOptions], list[R]]
```

**Arguments**:

  func (Callable[[BaseClient, Sequence[T]):
  ClientOptions]:
  R]:
- `priority_order` _Optional[Tuple], optional_ - (Default value = None)


**Returns**:



## get\_sequence

```python
@get.register
def get_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions()) -> Sequence[T]
```

**Arguments**:

  client (BaseClient):
  objs (Sequence):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## delete\_sequence

```python
@delete.register
def delete_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions()) -> None
```

**Arguments**:

  client (BaseClient):
  objs (Sequence):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## post\_sequence

```python
@post.register
def post_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions()) -> List[T]
```

**Arguments**:

  client (BaseClient):
  objs (Sequence):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## patch\_sequence

```python
@patch.register
def patch_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions()) -> List[T]
```

**Arguments**:

  client (BaseClient):
  objs (Sequence):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## client\_get\_url

```python
@get.register
def client_get_url(
    client: BaseClient, url: str,
    options: ClientOptions = ClientOptions()) -> Response
```

**Arguments**:

  client (BaseClient):
  url (str):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## client\_delete\_url

```python
@delete.register
def client_delete_url(
    client: BaseClient, url: str,
    options: ClientOptions = ClientOptions()) -> Response
```

**Arguments**:

  client (BaseClient):
  url (str):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## client\_post\_url

```python
@post.register
def client_post_url(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions()) -> Response
```

**Arguments**:

  client (BaseClient):
  url (str):
  payload (Dict):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## client\_patch\_url

```python
@patch.register
def client_patch_url(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions()) -> Response
```

**Arguments**:

  client (BaseClient):
  url (str):
  payload (Dict):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:
