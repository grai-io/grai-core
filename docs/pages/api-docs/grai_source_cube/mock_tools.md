---
sidebar_label: mock_tools
title: grai_source_cube.mock_tools
---

## CubeApiConfigFactory Objects

```python
class CubeApiConfigFactory(ModelFactory[CubeApiConfig])
```

### api\_token

```python
@post_generated
@classmethod
def api_token(cls, api_secret: Optional[SecretStr]) -> Optional[SecretStr]
```
