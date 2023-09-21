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

- `current` - The object to build grai metadata from.
- `desired` - The desired format of the metadata.


**Returns**:

- `None` - grai metadata object.


**Raises**:

- `NotImplementedError` - If no adapter is available between the `current` and `desired` types.

## build\_grai\_metadata\_from\_table

```python
@build_grai_metadata.register
def build_grai_metadata_from_table(current: Column,
                                   version: Literal["v1"] = "v1"
                                   ) -> ColumnMetadata
```

Build grai metadata for a Table object.

**Arguments**:

- `current` - The Table object to build grai metadata from.
- `version` - The version of grai metadata to build. Defaults to &quot;v1&quot;.


**Returns**:

- `TableMetadata` - grai metadata object for the Table.


**Raises**:

  None.

## build\_grai\_metadata\_from\_table

```python
@build_grai_metadata.register
def build_grai_metadata_from_table(current: Table,
                                   version: Literal["v1"] = "v1"
                                   ) -> TableMetadata
```

Build grai metadata for a Table object.

**Arguments**:

- `current` - The Table object to build grai metadata from.
- `version` - The version of grai metadata to build. Defaults to &quot;v1&quot;.


**Returns**:

- `TableMetadata` - grai metadata object for the Table.


**Raises**:

  None.

## build\_grai\_metadata\_from\_question

```python
@build_grai_metadata.register
def build_grai_metadata_from_question(current: Question,
                                      version: Literal["v1"] = "v1"
                                      ) -> QueryMetadata
```

Build grai metadata for a Question object.

**Arguments**:

- `current` _Question_ - The Question object to build grai metadata from.
- `version` _Literal[&quot;v1&quot;], optional_ - The version of grai metadata to build. Defaults to &quot;v1&quot;.


**Returns**:

- `GenericNodeMetadataV1` - grai metadata object for the Question.


**Raises**:

  None.

## build\_grai\_metadata\_from\_collection

```python
@build_grai_metadata.register
def build_grai_metadata_from_collection(
        current: Collection,
        version: Literal["v1"] = "v1") -> CollectionMetadata
```

Build grai metadata for a Collection object.

**Arguments**:

- `current` - The Collection object to build grai metadata from.
- `version` - The version of grai metadata to build. Defaults to &quot;v1&quot;.


**Returns**:

- `GenericNodeMetadataV1` - grai metadata object for the Collection.

## build\_grai\_metadata\_from\_edge

```python
@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge,
                                  version: Literal["v1"] = "v1"
                                  ) -> GenericEdgeMetadataV1
```

Build grai metadata for an Edge object.

**Arguments**:

- `current` - The Edge object to build grai metadata from.
- `version` - The version of grai metadata to build. Defaults to &quot;v1&quot;.


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

- `current` - The object to build application-specific metadata from.
- `desired` - The desired format of the metadata.


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

- `current` - The Table object to build application-specific metadata from.
- `version` - The version of the metadata to build. Defaults to &quot;v1&quot;.


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
def build_metadata(obj, version) -> Dict[str, Dict]
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
def adapt_table_to_client(current: Union[Table, Column],
                          source: SourceSpec,
                          version: Literal["v1"] = "v1") -> SourcedNodeV1
```

Adapt a Table object to the desired client format.

**Arguments**:

- `current` - The Table object to adapt.
- `source` - The Source associated with the Table
- `version` - The version of the client format to adapt to. Defaults to &quot;v1&quot;.


**Returns**:

- `NodeV1` - Adapted Table object in the desired client format.


**Raises**:

  None.

## adapt\_question\_to\_client

```python
@adapt_to_client.register
def adapt_question_to_client(current: Question,
                             source: SourceSpec,
                             version: Literal["v1"] = "v1") -> SourcedNodeV1
```

Adapt a Question object to the desired client format.

**Arguments**:

- `current` - The Question object to adapt.
- `source` - The source associated with the Question
- `version` - The version of the client format to adapt to. Defaults to &quot;v1&quot;.


**Returns**:

- `NodeV1` - Adapted Question object in the desired client format.


**Raises**:

  None.

## adapt\_collection\_to\_client

```python
@adapt_to_client.register
def adapt_collection_to_client(current: Collection,
                               source: SourceSpec,
                               version: Literal["v1"] = "v1") -> SourcedNodeV1
```

Adapt a Collection object to the desired client format.

**Arguments**:

  current:
  source:
  version:


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
                         source: SourceSpec,
                         version: Literal["v1"] = "v1") -> SourcedEdgeV1
```

Adapt an Edge object to the desired client format.

**Arguments**:

- `current` - The Edge object to adapt.
- `source` - The data source associated with the Edge
- `version` - The version of the client format to adapt to. Defaults to &quot;v1&quot;.


**Returns**:

- `EdgeV1` - Adapted Edge object in the desired client format.


**Raises**:

  None.

## adapt\_seq\_to\_client

```python
@adapt_to_client.register
def adapt_seq_to_client(objs: Sequence, source: SourceSpec,
                        version: Literal["v1"]) -> List[T]
```

Adapt a sequence of objects to the desired client format.

**Arguments**:

- `objs` - The sequence of objects to adapt.
- `source` - The source associated with each object in objs
- `version` - The version of the client format to adapt to.


**Returns**:

  List[Union[NodeV1, EdgeV1]]: Adapted sequence of objects in the desired client format.


**Raises**:

  None.

## adapt\_list\_to\_client

```python
@adapt_to_client.register
def adapt_list_to_client(objs: List, source: SourceSpec,
                         version: Literal["v1"]) -> List[T]
```

Adapt a list of objects to the desired client format.

**Arguments**:

- `objs` - The list of objects to adapt.
- `source` - The source associated with each object in objs
- `version` - The version of the client format to adapt to.


**Returns**:

  List[Union[NodeV1, EdgeV1]]: Adapted list of objects in the desired client format.


**Raises**:

  None.

## adapt\_source\_v1\_to\_client

```python
@adapt_to_client.register
def adapt_source_v1_to_client(objs: Any, source: SourceV1,
                              version: Any) -> List[T]
```

Adapt a list of objects to the desired client format.

**Arguments**:

- `objs` - The list of objects to adapt.
- `source` - The source associated with each object in objs
- `version` - The version of the client format to adapt to.


**Returns**:

  List[Union[NodeV1, EdgeV1]]: Adapted list of objects in the desired client format.


**Raises**:

  None.
