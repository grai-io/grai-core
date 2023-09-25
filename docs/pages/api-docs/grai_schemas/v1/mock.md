---
sidebar_label: mock
title: grai_schemas.v1.mock
---

## DefaultValueFactory Objects

```python
class DefaultValueFactory(ModelFactory[DefaultValue])
```

### data\_type

```python
@post_generated
@classmethod
def data_type(cls, default_value) -> Optional[str]
```



## NamedNodeSpecFactory Objects

```python
class NamedNodeSpecFactory(ModelFactory[NamedSpec])
```

### metadata

```python
@post_generated
@classmethod
def metadata(cls, data_sources: List[SourceSpec]) -> NodeMetadataV1
```



### is\_active

```python
@post_generated
@classmethod
def is_active(cls, data_sources: List[SourceSpec]) -> bool
```



## MockNode Objects

```python
class MockNode()
```

A class for generating mock nodes for testing.

**Attributes**:

- `workspace` - The workspace to associate with the mock nodes.
- `kwargs` - Additional keyword arguments to pass to the factories.

### \_\_init\_\_

```python
def __init__(workspace=None, **kwargs)
```

Initializes the MockNode class.

**Arguments**:

- `workspace` - The workspace to associate with the mock nodes.
- `kwargs` - Additional keyword arguments to pass to the factories.

### node

```python
def node(**kwargs) -> NodeV1
```

Generates a mocked NodeV1 object.

### named\_node\_spec

```python
def named_node_spec(**kwargs) -> NamedSpec
```

Generates a mocked NamedSpec object.

### id\_node\_spec

```python
def id_node_spec(**kwargs) -> IDSpec
```

Generates a mocked IDSpec object.

### sourced\_node

```python
def sourced_node(**kwargs) -> SourcedNodeV1
```

Generates a mocked SourcedNodeV1 object.

### named\_source\_node\_spec

```python
def named_source_node_spec(**kwargs) -> NamedSourceSpec
```

Generates a mocked NamedSourceSpec object.

### id\_source\_node\_spec

```python
def id_source_node_spec(**kwargs) -> IDSourceSpec
```

Generates a mocked IDSourceSpec object.

## NamedEdgeSpecFactory Objects

```python
class NamedEdgeSpecFactory(ModelFactory[NamedEdgeSpec])
```

### metadata

```python
@post_generated
@classmethod
def metadata(cls, data_sources: List[SourceSpec]) -> EdgeMetadataV1
```



### is\_active

```python
@post_generated
@classmethod
def is_active(cls, data_sources: List[SourceSpec]) -> bool
```



## MockEdge Objects

```python
class MockEdge()
```

A class for generating mock edges for testing.

**Attributes**:

- `workspace` - The workspace to associate with the mock edges.

### sourced\_edge

```python
def sourced_edge(**kwargs) -> SourcedEdgeV1
```

Generates a mocked SourcedEdgeV1 object.

### edge

```python
def edge(**kwargs) -> EdgeV1
```

Generates a mocked EdgeV1 object.

### named\_edge\_spec

```python
def named_edge_spec(**kwargs) -> NamedEdgeSpec
```

Generates a mocked NamedEdgeSpec object.

### id\_edge\_spec

```python
def id_edge_spec(**kwargs) -> EdgeIDSpec
```

Generates a mocked EdgeIDSpec object.

### named\_source\_edge\_spec

```python
def named_source_edge_spec(**kwargs) -> NamedEdgeSourceSpec
```

Generates a mocked NamedEdgeSourceSpec object.

### id\_source\_edge\_spec

```python
def id_source_edge_spec(**kwargs) -> EdgeIDSourceSpec
```

Generates a mocked EdgeIDSourceSpec object.

## MockOrganisation Objects

```python
class MockOrganisation()
```

A class for generating mock organisations for testing.

### organisation

```python
@classmethod
def organisation(cls, **kwargs) -> OrganisationV1
```

Generate a mocked OrganisationV1 object.

### organisation\_spec

```python
@classmethod
def organisation_spec(cls, **kwargs) -> OrganisationSpec
```

Generate a mocked OrganisationSpec object.

### organization

```python
@classmethod
def organization(cls, **kwargs) -> OrganisationV1
```

Generate a mocked OrganisationV1 object.

### organization\_spec

```python
@classmethod
def organization_spec(cls, **kwargs) -> OrganisationSpec
```

Generate a mocked OrganisationSpec object.

## WorkspaceSpecFactory Objects

```python
class WorkspaceSpecFactory(ModelFactory[WorkspaceSpec])
```

### ref

```python
@post_generated
@classmethod
def ref(cls, name, organisation) -> str
```



## MockWorkspace Objects

```python
class MockWorkspace()
```

A class for generating mock workspaces for testing.

**Attributes**:

- `organisation` - The organisation to associate with the mock workspaces.

### \_\_init\_\_

```python
def __init__(organisation=None)
```

Initializes the MockWorkspace class.

**Arguments**:

- `organisation` - The organisation to associate with the mock workspaces.

### workspace

```python
def workspace(**kwargs) -> WorkspaceV1
```

Generates a mocked WorkspaceV1 object.

### workspace\_spec

```python
def workspace_spec(**kwargs) -> WorkspaceSpec
```

Generates a mocked WorkspaceSpec object.

## MockSource Objects

```python
class MockSource()
```

A class for generating mocked source objects for testing.

**Attributes**:

- `workspace` - The workspace to associate with the mock sources.

### \_\_init\_\_

```python
def __init__(workspace=None)
```

Initializes the MockSource class.

**Arguments**:

- `workspace` - The workspace to associate with the mock sources.

### source

```python
def source(**kwargs) -> SourceV1
```

Generates a mocked SourceV1 object.

### source\_spec

```python
def source_spec(**kwargs) -> SourceSpec
```

Generates a mocked SourceSpec object.

## MockEvent Objects

```python
class MockEvent()
```

A class for generating mock events for testing.

**Attributes**:

- `workspace` - The workspace to associate with the mock events.

### \_\_init\_\_

```python
def __init__(workspace=None)
```

Initializes the MockEvent class.

**Arguments**:

- `workspace` - The workspace to associate with the mock events.

### event\_spec

```python
def event_spec(**kwargs) -> EventSpec
```

Generates a mocked EventSpec object.

### event

```python
def event(**kwargs) -> EventV1
```

Generates a mocked EventV1 object.

## MockV1 Objects

```python
class MockV1()
```

A class for generating mock objects for testing.

**Attributes**:

- `node` - Mocker for Node objects
- `edge` - Mocker for Edge objects
- `organisation` - Mocker for Organisation objects
- `workspace` - Mocker for Workspace objects
- `source` - Mocker for Source objects
- `event` - Mocker for Event objects

### \_\_init\_\_

```python
def __init__(workspace=None, organisation=None)
```

Initializes the MockV1 class.

**Arguments**:

- `workspace` - The workspace to associate with the mock objects.
- `organisation` - The organisation to associate with the mock objects.
