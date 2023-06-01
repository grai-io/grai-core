---
sidebar_label: schema
title: grai_client.testing.schema
---

#### mock\_v1\_node

```python
def mock_v1_node(name=None,
                 namespace=None,
                 data_source=None,
                 display_name=None,
                 is_active=True,
                 metadata={})
```

**Arguments**:

- `name` - (Default value = None)
- `namespace` - (Default value = None)
- `data_source` - (Default value = None)
- `display_name` - (Default value = None)
- `is_active` - (Default value = True)
- `metadata` - (Default value = {})


**Returns**:



#### mock\_node\_id

```python
def mock_node_id()
```



#### mock\_v1\_edge

```python
def mock_v1_edge(name=None,
                 namespace=None,
                 data_source=None,
                 source=None,
                 destination=None,
                 is_active=True,
                 metadata={})
```

**Arguments**:

- `name` - (Default value = None)
- `namespace` - (Default value = None)
- `data_source` - (Default value = None)
- `source` - (Default value = None)
- `destination` - (Default value = None)
- `is_active` - (Default value = True)
- `metadata` - (Default value = {})


**Returns**:



#### mock\_v1\_edge\_and\_nodes

```python
def mock_v1_edge_and_nodes(name=None,
                           data_source=None,
                           is_active=True,
                           metadata={},
                           namespace=None)
```

**Arguments**:

- `name` - (Default value = None)
- `data_source` - (Default value = None)
- `is_active` - (Default value = True)
- `metadata` - (Default value = {})
- `namespace` - (Default value = None)


**Returns**:
