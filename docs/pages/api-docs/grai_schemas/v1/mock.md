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

### node

```python
def node(**kwargs) -> NodeV1
```



### named\_node\_spec

```python
def named_node_spec(**kwargs) -> NamedSpec
```



### id\_node\_spec

```python
def id_node_spec(**kwargs) -> IDSpec
```



### sourced\_node

```python
def sourced_node(**kwargs) -> SourcedNodeV1
```



### named\_source\_node\_spec

```python
def named_source_node_spec(**kwargs) -> NamedSourceSpec
```



### id\_source\_node\_spec

```python
def id_source_node_spec(**kwargs) -> IDSourceSpec
```



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

### sourced\_edge

```python
def sourced_edge(**kwargs) -> SourcedEdgeV1
```



### edge

```python
def edge(**kwargs) -> EdgeV1
```



### named\_edge\_spec

```python
def named_edge_spec(**kwargs) -> NamedEdgeSpec
```



### id\_edge\_spec

```python
def id_edge_spec(**kwargs) -> EdgeIDSpec
```



### named\_source\_edge\_spec

```python
def named_source_edge_spec(**kwargs) -> NamedEdgeSourceSpec
```



### id\_source\_edge\_spec

```python
def id_source_edge_spec(**kwargs) -> EdgeIDSourceSpec
```



## MockOrganisation Objects

```python
class MockOrganisation()
```

### organisation

```python
@classmethod
def organisation(cls, **kwargs) -> OrganisationV1
```



### organisation\_spec

```python
@classmethod
def organisation_spec(cls, **kwargs) -> OrganisationSpec
```



### organization

```python
@classmethod
def organization(cls, **kwargs) -> OrganisationV1
```



### organization\_spec

```python
@classmethod
def organization_spec(cls, **kwargs) -> OrganisationSpec
```



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

### workspace

```python
def workspace(**kwargs) -> WorkspaceV1
```



### workspace\_spec

```python
def workspace_spec(**kwargs) -> WorkspaceSpec
```



## MockSource Objects

```python
class MockSource()
```

### source

```python
def source(**kwargs) -> SourceV1
```



### source\_spec

```python
def source_spec(**kwargs) -> SourceSpec
```



## MockEvent Objects

```python
class MockEvent()
```

### event\_spec

```python
def event_spec(**kwargs) -> EventSpec
```



### event

```python
def event(**kwargs) -> EventV1
```
