---
sidebar_label: base
title: grai_source_dbt_cloud.base
---

#### get\_events

```python
def get_events(connector: DbtCloudConnector, last_event_date: Optional[str])
```

**Arguments**:

  connector (DbtCloudConnector):
  last_event_date (Optional[str]):


**Returns**:



#### get\_nodes\_and\_edges

```python
def get_nodes_and_edges(connector: DbtCloudConnector,
                        version: str = "v1") -> Tuple[List[Node], List[Edge]]
```

**Arguments**:

  connector (DbtCloudConnector):
- `version` _str, optional_ - (Default value = &quot;v1&quot;)


**Returns**:



#### update\_server

```python
def update_server(client: BaseClient,
                  api_key: str,
                  namespace: str = "default") -> None
```

**Arguments**:

  client (BaseClient):
  api_key (str):
- `namespace` _str, optional_ - (Default value = &quot;default&quot;)


**Returns**:
