---
sidebar_label: base
title: grai_source_dbt.base
---

## get\_nodes\_and\_edges

```python
def get_nodes_and_edges(manifest_file: str,
                        namespace="default",
                        version: str = "v1") -> Tuple[List[Node], List[Edge]]
```

**Arguments**:

  manifest_file (str):
- `namespace` - (Default value = &quot;default&quot;)
- `version` _str, optional_ - (Default value = &quot;v1&quot;)


**Returns**:



## update\_server

```python
def update_server(client: BaseClient,
                  manifest_file: str,
                  namespace: str = "default") -> Tuple[List[Node], List[Edge]]
```

**Arguments**:

  client (BaseClient):
  manifest_file (str):
- `namespace` _str, optional_ - (Default value = &quot;default&quot;)


**Returns**:
