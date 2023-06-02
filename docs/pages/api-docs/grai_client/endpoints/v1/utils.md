---
sidebar_label: utils
title: grai_client.endpoints.v1.utils
---

## process\_node\_id

```python
def process_node_id(
    client: ClientV1,
    grai_type: NodeIdTypes,
    options: ClientOptions = ClientOptions()
) -> NodeIdTypes
```

Process a NodeID object, either by returning if it has a known id, or by getting
the id from the server.

**Arguments**:

  client (ClientV1):
  grai_type (NodeIdTypes):
- `options` _ClientOptions, optional_ - (Default value = ClientOptions())


**Returns**:
