---
sidebar_label: delete
title: grai_client.endpoints.v1.delete
---

## delete\_node\_v1

```python
@delete.register
def delete_node_v1(client: ClientV1,
                   grai_type: NodeV1,
                   options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## delete\_source\_node\_by\_source\_node\_v1

```python
@delete.register
def delete_source_node_by_source_node_v1(
    client: ClientV1,
    grai_type: SourcedNodeV1,
    options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## delete\_source\_node\_spec

```python
@delete.register
def delete_source_node_spec(client: ClientV1,
                            grai_type: SourcedNodeSpec,
                            options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## delete\_source\_edge\_by\_source\_node\_v1

```python
@delete.register
def delete_source_edge_by_source_node_v1(
    client: ClientV1,
    grai_type: SourcedEdgeV1,
    options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## delete\_source\_edge\_spec

```python
@delete.register
def delete_source_edge_spec(client: ClientV1,
                            grai_type: SourcedEdgeSpec,
                            options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## delete\_edge\_v1

```python
@delete.register
def delete_edge_v1(client: ClientV1,
                   grai_type: EdgeV1,
                   options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## delete\_workspace\_v1

```python
@delete.register
def delete_workspace_v1(client: ClientV1,
                        grai_type: Union[WorkspaceV1, WorkspaceSpec,
                                         WorkspaceLabels],
                        options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## delete\_organisation\_v1

```python
@delete.register
def delete_organisation_v1(client: ClientV1,
                           grai_type: Union[OrganisationV1, OrganisationSpec,
                                            OrganisationLabels],
                           options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## delete\_source\_by\_label

```python
@delete.register
def delete_source_by_label(client: ClientV1,
                           grai_type: SourceLabels,
                           options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:



## delete\_source\_by\_source\_v1

```python
@delete.register
def delete_source_by_source_v1(client: ClientV1,
                               grai_type: SourceV1,
                               options: ClientOptions = ClientOptions())
```

**Arguments**:

  client:
  grai_type:
- `options` - (Default value = ClientOptions())


**Returns**:
