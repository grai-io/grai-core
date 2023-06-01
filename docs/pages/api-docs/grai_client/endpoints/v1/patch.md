---
sidebar_label: patch
title: grai_client.endpoints.v1.patch
---

## patch\_node\_v1

```python
@patch.register
def patch_node_v1(
    client: ClientV1,
    grai_type: NodeV1,
    options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]
```

**Arguments**:

  client (ClientV1):
  grai_type (NodeV1):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:



## patch\_edge\_v1

```python
@patch.register
def patch_edge_v1(
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
