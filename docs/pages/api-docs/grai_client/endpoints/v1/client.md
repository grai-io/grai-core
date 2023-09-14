---
sidebar_label: client
title: grai_client.endpoints.v1.client
---

## ClientV1 Objects

```python
class ClientV1(BaseClient)
```



### check\_authentication

```python
def check_authentication() -> Response
```

**Arguments**:



**Returns**:



### workspace

```python
@property
def workspace() -> Optional[str]
```

**Arguments**:



**Returns**:



### workspace

```python
@workspace.setter
def workspace(workspace: Optional[Union[str, UUID]])
```

**Arguments**:

  workspace (Optional[Union[str, UUID]]):


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



## client\_patch\_url

```python
@patch.register
def client_patch_url(
    client: ClientV1,
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



## client\_post\_url

```python
@post.register
def client_post_url(
    client: ClientV1,
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



## client\_delete\_url

```python
@delete.register
def client_delete_url(
    client: ClientV1, url: str,
    options: ClientOptions = ClientOptions()) -> Response
```

**Arguments**:

  client (BaseClient):
  url (str):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## client\_get\_url

```python
@get.register
def client_get_url(
    client: ClientV1, url: str,
    options: ClientOptions = ClientOptions()) -> Response
```

**Arguments**:

  client (BaseClient):
  url (str):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:
