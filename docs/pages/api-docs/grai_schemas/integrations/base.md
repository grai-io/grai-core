---
sidebar_label: base
title: grai_schemas.integrations.base
---

## verify\_edge\_ids

```python
def verify_edge_ids(
    nodes: List[SourcedNode], edges: List[SourcedEdge]
) -> Tuple[List[SourcedEdge], List[QuarantinedEdge]]
```

Validates that all edges have a source and destination node in the graph

**Arguments**:

- `nodes` - A list of sourced nodes
- `edges` - A list of sourced edges


**Returns**:

  A tuple of lists of sourced edges. The first list contains all edges that have a source and destination node in the graph. The second list contains all edges that do not have a source or destination node in the graph.

## ValidatedResult Objects

```python
class ValidatedResult(BaseModel)
```

Class definition of ValidatedResult

**Attributes**:

- `nodes` - A list of sourced nodes
- `edges` - A list of sourced edges
- `events` - A list of events

## GraiIntegrationImplementation Objects

```python
class GraiIntegrationImplementation(ABC)
```

Base class for Grai integrations

**Attributes**:

- `source` - The Grai data source to associate with output from the integration.
- `version` - The Grai data version to associate with output from the integration.

### \_\_init\_\_

```python
def __init__(source: SourceV1, version: Optional[str] = None)
```

Initializes the Grai integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration.
- `version` - The Grai data version to associate with output from the integration.

### nodes

```python
@abstractmethod
def nodes() -> List[SourcedNode]
```

Returns a list of sourced nodes

### edges

```python
@abstractmethod
def edges() -> List[SourcedEdge]
```

Returns a list of sourced edges

### get\_nodes\_and\_edges

```python
@abstractmethod
def get_nodes_and_edges() -> Tuple[List[SourcedNode], List[SourcedEdge]]
```

Returns a tuple of lists of sourced nodes and sourced edges

### ready

```python
@abstractmethod
def ready() -> bool
```

Returns True if the integration is ready to run

### events

```python
def events(*args, **kwargs) -> List[Event]
```

Returns a list of events

## QuarantineAccessor Objects

```python
class QuarantineAccessor()
```

Class definition of QuarantineAccessor

**Attributes**:

- `nodes` - A list of quarantined nodes
- `edges` - A list of quarantined edges
- `events` - A list of quarantined events
- `has_quarantined` - True if there are any quarantined items.

### \_\_init\_\_

```python
def __init__(integration_instance: GraiIntegrationImplementation)
```

Initializes the QuarantineAccessor

### nodes

```python
@property
def nodes() -> List[QuarantinedNode]
```

Returns a list of quarantined nodes

### nodes

```python
@nodes.setter
def nodes(value: List[QuarantinedNode])
```

Sets the list of quarantined nodes

### edges

```python
@property
def edges() -> List[QuarantinedEdge]
```

Returns a list of quarantined edges

### edges

```python
@edges.setter
def edges(value: List[QuarantinedEdge])
```

Sets the list of quarantined edges

### events

```python
@property
def events() -> List[QuarantinedEvent]
```

Returns a list of quarantined events

### events

```python
@events.setter
def events(value: List[QuarantinedEvent])
```

Sets the list of quarantined events

### has\_quarantined

```python
@property
def has_quarantined() -> bool
```

Returns True if there are any quarantined items

## ValidatedIntegration Objects

```python
class ValidatedIntegration(GraiIntegrationImplementation)
```

A type of Integration which quarantines invalid integration output

**Attributes**:

- `integration` - The integration to validate

### \_\_init\_\_

```python
def __init__(integration: GraiIntegrationImplementation, *args, **kwargs)
```

Initializes the ValidatedIntegration

**Arguments**:

- `integration` - The integration to validate

### quarantine

```python
@property
def quarantine() -> QuarantineAccessor
```

Returns the QuarantineAccessor for the integration

### nodes

```python
@cache
def nodes() -> List[SourcedNode]
```

Returns a list of validated sourced nodes

### edges

```python
@cache
def edges() -> List[SourcedEdge]
```

Returns a list of validates sourced edges

### get\_nodes\_and\_edges

```python
@cache
def get_nodes_and_edges() -> Tuple[List[SourcedNode], List[SourcedEdge]]
```

Returns a tuple of lists of validated sourced nodes and sourced edges

### events

```python
@cache
def events(*args, **kwargs) -> List[Event]
```

Returns a list of validated events

### ready

```python
def ready() -> bool
```

Returns True if the integration is ready to run
