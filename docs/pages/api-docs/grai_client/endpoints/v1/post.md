---
sidebar_label: post
title: grai_client.endpoints.v1.post
---

## post\_node\_v1

```python
@post.register
def post_node_v1(
    client: ClientV1,
    grai_type: NodeV1,
    options: ClientOptions = ClientOptions()) -> NodeV1
```

**Arguments**:

  client (ClientV1):
  grai_type (NodeV1):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## post\_edge\_v1

```python
@post.register
def post_edge_v1(
    client: ClientV1,
    grai_type: EdgeV1,
    options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (EdgeV1):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:
