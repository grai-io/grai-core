---
sidebar_label: url
title: grai_client.endpoints.v1.url
---

## get\_node\_url

```python
@ClientV1.get_url.register
def get_node_url(
    client: ClientV1, obj: Union[NodeIdTypes, NodeV1, SourcedNodeV1,
                                 SourcedNodeSpec, NodeLabels]
) -> str
```

**Arguments**:

  client:
  obj:


**Returns**:



## get\_edge\_url

```python
@ClientV1.get_url.register
def get_edge_url(client: ClientV1, obj: Union[EdgeV1, EdgeLabels, EdgeIdTypes,
                                              EdgeSpec]) -> str
```

**Arguments**:

  client:
  obj:


**Returns**:



## get\_sourced\_node\_url\_by\_source\_id

```python
@ClientV1.get_url.register
def get_sourced_node_url_by_source_id(client: ClientV1,
                                      type_identifier: Union[SourceNodeLabels,
                                                             SourcedNodeV1,
                                                             SourcedNodeSpec],
                                      source_id: UUID) -> str
```

**Arguments**:

  client:
  type_identifier:
  source_id:


**Returns**:



## get\_sourced\_node\_url\_by\_source\_and\_node\_id

```python
@ClientV1.get_url.register
def get_sourced_node_url_by_source_and_node_id(client: ClientV1,
                                               type_identifier: Union[
                                                   SourceNodeLabels,
                                                   SourcedNodeV1,
                                                   SourcedNodeSpec],
                                               source_id: UUID,
                                               node_id: UUID) -> str
```

**Arguments**:

  client:
  type_identifier:
  source_id:
  node_id:


**Returns**:



## get\_workspace\_url

```python
@ClientV1.get_url.register
def get_workspace_url(
        client: ClientV1, obj: Union[WorkspaceLabels, WorkspaceV1,
                                     WorkspaceSpec]) -> str
```

**Arguments**:

  client:
  obj:


**Returns**:



## get\_source\_url

```python
@ClientV1.get_url.register
def get_source_url(client: ClientV1, obj: Union[SourceLabels, SourceV1,
                                                SourceSpec]) -> str
```

**Arguments**:

  client:
  obj:


**Returns**:



## get\_sourced\_edge\_url\_by\_source\_id

```python
@ClientV1.get_url.register
def get_sourced_edge_url_by_source_id(client: ClientV1,
                                      type_identifier: Union[SourceEdgeLabels,
                                                             SourcedEdgeV1,
                                                             SourcedEdgeSpec],
                                      source_id: UUID) -> str
```

**Arguments**:

  client:
  type_identifier:
  source_id:


**Returns**:



## get\_sourced\_edge\_url\_by\_source\_and\_edge\_id

```python
@ClientV1.get_url.register
def get_sourced_edge_url_by_source_and_edge_id(client: ClientV1,
                                               type_identifier: Union[
                                                   SourceEdgeLabels,
                                                   SourcedEdgeV1,
                                                   SourcedEdgeSpec],
                                               source_id: UUID,
                                               edge_id: UUID) -> str
```

**Arguments**:

  client:
  type_identifier:
  source_id:
  edge_id

**Returns**:
