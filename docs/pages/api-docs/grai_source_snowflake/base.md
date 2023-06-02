---
sidebar_label: base
title: grai_source_snowflake.base
---

#### get\_nodes\_and\_edges

```python
def get_nodes_and_edges(
        connector: SnowflakeConnector,
        version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]
```

**Arguments**:

  connector (SnowflakeConnector):
  version (Literal[&quot;v1&quot;]):


**Returns**:



#### update\_server

```python
def update_server(client: BaseClient,
                  namespace: Optional[str] = None,
                  account: Optional[str] = None,
                  user: Optional[str] = None,
                  password: Optional[str] = None,
                  role: Optional[str] = None,
                  warehouse: Optional[str] = None,
                  database: Optional[str] = None,
                  schema: Optional[str] = None) -> None
```

**Arguments**:

  client (BaseClient):
- `namespace` _Optional[str], optional_ - (Default value = None)
- `account` _Optional[str], optional_ - (Default value = None)
- `user` _Optional[str], optional_ - (Default value = None)
- `password` _Optional[str], optional_ - (Default value = None)
- `role` _Optional[str], optional_ - (Default value = None)
- `warehouse` _Optional[str], optional_ - (Default value = None)
- `database` _Optional[str], optional_ - (Default value = None)
- `schema` _Optional[str], optional_ - (Default value = None)


**Returns**:
