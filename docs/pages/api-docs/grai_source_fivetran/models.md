---
sidebar_label: models
title: grai_source_fivetran.models
---

## TableResult Objects

```python
class TableResult(BaseModel)
```



## ColumnResult Objects

```python
class ColumnResult(BaseModel)
```



## SchemaResult Objects

```python
class SchemaResult(BaseModel)
```



## DestinationConfig Objects

```python
class DestinationConfig(BaseModel)
```



## DestinationMetadata Objects

```python
class DestinationMetadata(BaseModel)
```



### id

e.x. decent_dropsy

### group\_id

e.x. decent_dropsy

### service

e.x. snowflake

### region

e.x. GCP_US_EAST4

### time\_zone\_offset

e.x. -5

### setup\_status

e.x. connected

## ConnectorTablePatchSettings Objects

```python
class ConnectorTablePatchSettings(BaseModel)
```



## ConnectorTableColumnSchema Objects

```python
class ConnectorTableColumnSchema(BaseModel)
```



## ConnectorTableSchema Objects

```python
class ConnectorTableSchema(BaseModel)
```



## ConnectorSchema Objects

```python
class ConnectorSchema(BaseModel)
```



## ConnectorMetadata Objects

```python
class ConnectorMetadata(BaseModel)
```



## SourceTableColumnMetadata Objects

```python
class SourceTableColumnMetadata(BaseModel)
```



## NamespaceIdentifier Objects

```python
class NamespaceIdentifier(BaseModel)
```



## Column Objects

```python
class Column(BaseModel)
```



### full\_name

```python
@property
def full_name()
```



### from\_fivetran\_models

```python
@classmethod
def from_fivetran_models(cls, schema: SchemaMetadataResponse,
                         table: TableMetadataResponse,
                         column: ColumnMetadataResponse,
                         namespace: NamespaceIdentifier)
```

**Arguments**:

  schema (SchemaMetadataResponse):
  table (TableMetadataResponse):
  column (ColumnMetadataResponse):
  namespace (NamespaceIdentifier):


**Returns**:



## Table Objects

```python
class Table(BaseModel)
```



### full\_name

```python
@property
def full_name()
```



### from\_fivetran\_models

```python
@classmethod
def from_fivetran_models(cls, schema: SchemaMetadataResponse,
                         table: TableMetadataResponse,
                         namespace: NamespaceIdentifier)
```

**Arguments**:

  schema (SchemaMetadataResponse):
  table (TableMetadataResponse):
  namespace (NamespaceIdentifier):


**Returns**:



## Constraint Objects

```python
class Constraint(str, Enum)
```



## Edge Objects

```python
class Edge(BaseModel)
```
