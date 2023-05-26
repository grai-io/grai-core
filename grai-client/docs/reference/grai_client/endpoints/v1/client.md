---
sidebar_label: client
title: grai_client.endpoints.v1.client
---

## ClientV1 Objects

```python
class ClientV1(BaseClient)
```

#### authenticate

```python
def authenticate(username: Optional[str] = None,
                 password: Optional[str] = None,
                 api_key: Optional[str] = None) -> None
```

Authenticate with the server.

Caution: This function is unstable and can produce unexpected results.
