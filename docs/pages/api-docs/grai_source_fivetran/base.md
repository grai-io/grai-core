---
sidebar_label: base
title: grai_source_fivetran.base
---

#### validate\_nodes\_and\_edges

```python
def validate_nodes_and_edges(nodes: List[Node], edges: List[Edge])
```

**Arguments**:

  nodes (List[Node]):
  edges (List[Edge]):


**Returns**:



#### get\_nodes\_and\_edges

```python
def get_nodes_and_edges(
        connector: FivetranConnector,
        version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]
```

**Arguments**:

  connector (FivetranConnector):
  version (Literal[&quot;v1&quot;]):


**Returns**:



#### update\_server

```python
def update_server(client: BaseClient,
                  namespaces: Optional[NamespaceTypes] = None,
                  default_namespace: Optional[str] = None,
                  api_key: Optional[str] = None,
                  api_secret: Optional[str] = None,
                  endpoint: Optional[str] = None,
                  limit: Optional[int] = None,
                  parallelization: Optional[int] = None)
```

**Arguments**:

  client (BaseClient):
- `namespaces` _Optional[NamespaceTypes], optional_ - (Default value = None)
- `default_namespace` _Optional[str], optional_ - (Default value = None)
- `api_key` _Optional[str], optional_ - (Default value = None)
- `api_secret` _Optional[str], optional_ - (Default value = None)
- `endpoint` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `parallelization` _Optional[int], optional_ - (Default value = None)


**Returns**:
