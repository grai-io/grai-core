---
sidebar_label: base
title: grai_source_metabase.base
---

## get\_nodes\_and\_edges

```python
def get_nodes_and_edges(
        connector: MetabaseConnector,
        version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]
```

**Arguments**:

  connector (MetabaseConnector):
  version (Literal[&quot;v1&quot;]):


**Returns**:



## update\_server

```python
def update_server(client: BaseClient,
                  namespaces: Optional = None,
                  metabase_namespace: Optional[str] = None,
                  username: Optional[str] = None,
                  password: Optional[str] = None,
                  endpoint: Optional[str] = None)
```

**Arguments**:

  password:
- `username` - Optional[str]
  client:
- `namespaces` - (Default value = None)
- `metabase_namespace` - (Default value = None)
- `endpoint` - (Default value = None)


**Returns**:
