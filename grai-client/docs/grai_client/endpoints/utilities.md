---
sidebar_label: utilities
title: grai_client.endpoints.utilities
---

#### is\_valid\_uuid

```python
def is_valid_uuid(val: Union[str, UUID])
```

**Arguments**:

  val (Union[str, UUID]):


**Returns**:



#### response\_status\_check

```python
def response_status_check(resp: Response) -> Response
```

**Arguments**:

  resp (Response):


**Returns**:



#### orjson\_defaults

```python
def orjson_defaults(obj: Any) -> Any
```

**Arguments**:

  obj (Any):


**Returns**:



## GraiEncoder Objects

```python
class GraiEncoder(json.JSONEncoder)
```

Needed for the base python json implementation

#### default

```python
def default(obj: Any) -> Any
```

**Arguments**:

  obj (Any):


**Returns**:



#### serialize\_obj

```python
def serialize_obj(obj: Dict) -> bytes
```

**Arguments**:

  obj (Dict):


**Returns**:



#### serialize\_obj\_fallback

```python
def serialize_obj_fallback(obj: Dict) -> str
```

**Arguments**:

  obj (Dict):


**Returns**:



#### add\_query\_params

```python
def add_query_params(url: str, params: dict) -> str
```

**Arguments**:

  url (str):
  params (dict):


**Returns**:
