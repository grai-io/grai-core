---
sidebar_label: adapters
title: grai_source_metabase.adapters
---

## build\_grai\_metadata

```python
@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None
```

Build grai metadata for a given object.

**Arguments**:

- `current` _Any_ - The object to build grai metadata from.
- `desired` _Any_ - The desired format of the metadata.


**Returns**:

- `None` - grai metadata object.


**Raises**:

- `NotImplementedError` - If no adapter is available between the `current` and `desired` types.

## build\_grai\_metadata\_from\_table

```python
@build_grai_metadata.register
def build_grai_metadata_from_table(current: Table,
                                   version: Literal["v1"] = "v1"
                                   ) -> TableMetadata
```

Build grai metadata for a Table object.

**Arguments**:

- `current` _Table_ - The Table object to build grai metadata from.
- `version` _Literal[&quot;v1&quot;], optional_ - The version of grai metadata to build. Defaults to &quot;v1&quot;.


**Returns**:

- `TableMetadata` - grai metadata object for the Table.


**Raises**:

  None.

## build\_grai\_metadata\_from\_question

```python
@build_grai_metadata.register
def build_grai_metadata_from_question(
        current: Question,
        version: Literal["v1"] = "v1") -> GenericNodeMetadataV1
```

Build grai metadata for a Question object.

**Arguments**:

- `current` _Question_ - The Question object to build grai metadata from.
- `version` _Literal[&quot;v1&quot;], optional_ - The version of grai metadata to build. Defaults to &quot;v1&quot;.


**Returns**:

- `GenericNodeMetadataV1` - grai metadata object for the Question.


**Raises**:

  None.

## build\_grai\_metadata\_from\_edge

```python
@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge,
                                  version: Literal["v1"] = "v1"
                                  ) -> GenericEdgeMetadataV1
```

Build grai metadata for an Edge object.

**Arguments**:

- `current` _Edge_ - The Edge object to build grai metadata from.
- `version` _Literal[&quot;v1&quot;], optional_ - The version of grai metadata to build. Defaults to &quot;v1&quot;.


**Returns**:

- `GenericEdgeMetadataV1` - grai metadata object for the Edge.


**Raises**:

  None.

## build\_app\_metadata

```python
@multimethod
def build_app_metadata(current: Any, desired: Any) -> None
```

Build application-specific metadata for a given object.

**Arguments**:

- `current` _Any_ - The object to build application-specific metadata from.
- `desired` _Any_ - The desired format of the metadata.


**Returns**:

- `None` - Application-specific metadata object.


**Raises**:

- `NotImplementedError` - If no adapter is available between the `current` and `desired` types.

## build\_metadata\_from\_table

```python
@build_app_metadata.register
def build_metadata_from_table(current: BaseModel,
                              version: Literal["v1"] = "v1") -> Dict
```

Build application-specific metadata for a Table object.

**Arguments**:

- `current` _Table_ - The Table object to build application-specific metadata from.
- `version` _Literal[&quot;v1&quot;], optional_ - The version of the metadata to build. Defaults to &quot;v1&quot;.


**Returns**:

- `Dict` - Application-specific metadata object for the Table.


**Raises**:

  None.

## build\_metadata\_from\_edge

```python
@build_app_metadata.register
def build_metadata_from_edge(current: Edge,
                             version: Literal["v1"] = "v1") -> Dict
```

Build application-specific metadata for an Edge object.

**Arguments**:

- `current` _Edge_ - The Edge object to build application-specific metadata from.
- `version` _Literal[&quot;v1&quot;], optional_ - The version of the metadata to build. Defaults to &quot;v1&quot;.


**Returns**:

- `Dict` - Application-specific metadata object for the Edge.


**Raises**:

  None.

## build\_metadata

```python
def build_metadata(obj, version)
```

Build metadata for a given object.

**Arguments**:

- `obj` - The object to build metadata from.
- `version` - The version of the metadata to build.


**Returns**:

- `Dict` - Metadata object containing both grai and application-specific metadata.


**Raises**:

  None.

## adapt\_to\_client

```python
@multimethod
def adapt_to_client(current: Any, desired: Any)
```

Adapt a given object to the desired client format.

**Arguments**:

- `current` _Any_ - The object to adapt.
- `desired` _Any_ - The desired format to adapt to.


**Returns**:

- `None` - Adapted object in the desired format.


**Raises**:

- `NotImplementedError` - If no adapter is available between the `current` and `desired` types.

## adapt\_table\_to\_client

```python
@adapt_to_client.register
def adapt_table_to_client(current: Table,
                          version: Literal["v1"] = "v1") -> NodeV1
```

Adapt a Table object to the desired client format.

**Arguments**:

- `current` _Table_ - The Table object to adapt.
- `version` _Literal[&quot;v1&quot;], optional_ - The version of the client format to adapt to. Defaults to &quot;v1&quot;.


**Returns**:

- `NodeV1` - Adapted Table object in the desired client format.


**Raises**:

  None.

## adapt\_question\_to\_client

```python
@adapt_to_client.register
def adapt_question_to_client(current: Question,
                             version: Literal["v1"] = "v1") -> NodeV1
```

Adapt a Question object to the desired client format.

**Arguments**:

- `current` _Question_ - The Question object to adapt.
- `version` _Literal[&quot;v1&quot;], optional_ - The version of the client format to adapt to. Defaults to &quot;v1&quot;.


**Returns**:

- `NodeV1` - Adapted Question object in the desired client format.


**Raises**:

  None.

## make\_name

```python
def make_name(node1: NodeTypes, node2: NodeTypes) -> str
```

Creates a name for an edge based on the given nodes.

**Arguments**:

  node1 (NodeTypes)
  node2 (NodeTypes)


**Returns**:

- `str` - The name of the edge.


**Raises**:

  None.

## adapt\_edge\_to\_client

```python
@adapt_to_client.register
def adapt_edge_to_client(current: Edge,
                         version: Literal["v1"] = "v1") -> EdgeV1
```

Adapt an Edge object to the desired client format.

**Arguments**:

- `current` _Edge_ - The Edge object to adapt.
- `version` _Literal[&quot;v1&quot;], optional_ - The version of the client format to adapt to. Defaults to &quot;v1&quot;.


**Returns**:

- `EdgeV1` - Adapted Edge object in the desired client format.


**Raises**:

  None.

## adapt\_seq\_to\_client

```python
@adapt_to_client.register
def adapt_seq_to_client(objs: Sequence,
                        version: Literal["v1"]) -> List[Union[NodeV1, EdgeV1]]
```

Adapt a sequence of objects to the desired client format.

**Arguments**:

- `objs` _Sequence_ - The sequence of objects to adapt.
- `version` _Literal[&quot;v1&quot;]_ - The version of the client format to adapt to.


**Returns**:

  List[Union[NodeV1, EdgeV1]]: Adapted sequence of objects in the desired client format.


**Raises**:

  None.

## adapt\_list\_to\_client

```python
@adapt_to_client.register
def adapt_list_to_client(
        objs: List, version: Literal["v1"]) -> List[Union[NodeV1, EdgeV1]]
```

Adapt a list of objects to the desired client format.

**Arguments**:

- `objs` _List_ - The list of objects to adapt.
- `version` _Literal[&quot;v1&quot;]_ - The version of the client format to adapt to.


**Returns**:

  List[Union[NodeV1, EdgeV1]]: Adapted list of objects in the desired client format.


**Raises**:

  None.
