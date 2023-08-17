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
def data_type(cls, default_value) -> str
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
def node(**kwargs)
```



### named\_node\_spec

```python
def named_node_spec(**kwargs)
```



### id\_node\_spec

```python
def id_node_spec(**kwargs)
```



### sourced\_node

```python
def sourced_node(**kwargs)
```



### named\_source\_node\_spec

```python
def named_source_node_spec(**kwargs)
```



### id\_source\_node\_spec

```python
def id_source_node_spec(**kwargs)
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
def sourced_edge(**kwargs)
```



### edge

```python
def edge(**kwargs)
```



### named\_edge\_spec

```python
def named_edge_spec(**kwargs)
```



### id\_edge\_spec

```python
def id_edge_spec(**kwargs)
```



### named\_source\_edge\_spec

```python
def named_source_edge_spec(**kwargs)
```



### id\_source\_edge\_spec

```python
def id_source_edge_spec(**kwargs)
```



## MockOrganisation Objects

```python
class MockOrganisation()
```

### organisation

```python
@classmethod
def organisation(cls, **kwargs)
```



### organisation\_spec

```python
@classmethod
def organisation_spec(cls, **kwargs)
```



### organization

```python
@classmethod
def organization(cls, **kwargs)
```



### organization\_spec

```python
@classmethod
def organization_spec(cls, **kwargs)
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
def workspace(**kwargs)
```



### workspace\_spec

```python
def workspace_spec(**kwargs)
```



## MockSource Objects

```python
class MockSource()
```

### source

```python
def source(**kwargs)
```



### source\_spec

```python
def source_spec(**kwargs)
```
