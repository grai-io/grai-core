---
sidebar_label: base
title: grai_source_bigquery.base
---

#### get\_nodes\_and\_edges

```python
def get_nodes_and_edges(
        connector: BigqueryConnector,
        version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]
```

**Arguments**:

  connector (BigqueryConnector):
  version (Literal[&quot;v1&quot;]):


**Returns**:



#### update\_server

```python
def update_server(client: BaseClient,
                  namespace: Optional[str] = None,
                  project: Optional[str] = None,
                  dataset: Optional[str] = None,
                  credentials: Optional[str] = None) -> None
```

**Arguments**:

  client (BaseClient):
- `namespace` _Optional[str], optional_ - (Default value = None)
- `project` _Optional[str], optional_ - (Default value = None)
- `dataset` _Optional[str], optional_ - (Default value = None)
- `credentials` _Optional[str], optional_ - (Default value = None)


**Returns**:
