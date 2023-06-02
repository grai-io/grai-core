---
sidebar_label: loader
title: grai_source_fivetran.loader
---

## FiveTranConfig Objects

```python
class FiveTranConfig(BaseSettings)
```



#### validate\_endpoint

```python
@validator("endpoint")
def validate_endpoint(cls, value)
```

**Arguments**:

  value:


**Returns**:



## Config Objects

```python
class Config()
```



#### has\_data\_items

```python
def has_data_items(item: Dict) -> bool
```

**Arguments**:

  item (Dict):


**Returns**:



## FivetranAPI Objects

```python
class FivetranAPI()
```



#### make\_request

```python
def make_request(request: Callable[..., requests.Response],
                 url: str,
                 headers: Optional[Dict] = None,
                 params: Optional[Dict] = None,
                 **kwargs) -> Dict
```

**Arguments**:

  request (Callable[..., requests.Response]):
  url (str):
- `headers` _Optional[Dict], optional_ - (Default value = None)
- `params` _Optional[Dict], optional_ - (Default value = None)
  **kwargs:


**Returns**:



#### paginated\_query

```python
def paginated_query(request: Callable[..., requests.Response],
                    url: str,
                    headers: Optional[Dict] = None,
                    params: Optional[Dict] = None,
                    **kwargs) -> Iterable[Dict]
```

**Arguments**:

  request (Callable[..., requests.Response]):
  url (str):
- `headers` _Optional[Dict], optional_ - (Default value = None)
- `params` _Optional[Dict], optional_ - (Default value = None)
  **kwargs:


**Returns**:



#### get\_paginated\_data\_items

```python
def get_paginated_data_items(url: str,
                             headers: Optional[Dict] = None,
                             params: Optional[Dict] = None) -> List[Dict]
```

**Arguments**:

  url (str):
- `headers` _Optional[Dict], optional_ - (Default value = None)
- `params` _Optional[Dict], optional_ - (Default value = None)


**Returns**:



#### get\_tables

```python
def get_tables(connector_id: str,
               limit: Optional[int] = None) -> List[TableMetadataResponse]
```

**Arguments**:

  connector_id (str):
- `limit` _Optional[int], optional_ - (Default value = None)


**Returns**:



#### get\_columns

```python
def get_columns(connector_id: str,
                limit: Optional[int] = None) -> List[ColumnMetadataResponse]
```

**Arguments**:

  connector_id (str):
- `limit` _Optional[int], optional_ - (Default value = None)


**Returns**:



#### get\_schemas

```python
def get_schemas(connector_id: str,
                limit: Optional[int] = None) -> List[SchemaMetadataResponse]
```

**Arguments**:

  connector_id (str):
- `limit` _Optional[int], optional_ - (Default value = None)


**Returns**:



#### get\_all\_groups

```python
def get_all_groups(limit: Optional[int] = None) -> List[GroupResponse]
```

**Arguments**:

- `limit` _Optional[int], optional_ - (Default value = None)


**Returns**:



#### get\_group\_connectors

```python
def get_group_connectors(group_id: str,
                         limit: Optional[int] = None
                         ) -> List[ConnectorResponse]
```

**Arguments**:

  group_id (str):
- `limit` _Optional[int], optional_ - (Default value = None)


**Returns**:



#### get\_destination\_metadata

```python
def get_destination_metadata(
        destination_id: str) -> V1DestinationsDestinationIdGetResponse
```

**Arguments**:

  destination_id (str):


**Returns**:



#### get\_connector\_metadata

```python
def get_connector_metadata(
        connector_id: str) -> V1ConnectorsConnectorIdSchemasGetResponse
```

**Arguments**:

  connector_id (str):


**Returns**:



#### get\_source\_table\_column\_metadata

```python
def get_source_table_column_metadata(
    connector_id: str, schema: str, table: str
) -> V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse
```

**Arguments**:

  connector_id (str):
  schema (str):
  table (str):


**Returns**:



#### get\_connectors

```python
def get_connectors() -> List[ConnectorResponse]
```

**Arguments**:



**Returns**:



#### caller

```python
async def caller(semaphore: asyncio.Semaphore, func: Callable[..., T], *args,
                 **kwargs) -> T
```

**Arguments**:

  semaphore (asyncio.Semaphore):
  func (Callable[..., T]):
  *args:
  **kwargs:


**Returns**:



#### parallelize\_http

```python
def parallelize_http(semaphore)
```

**Arguments**:

  semaphore:


**Returns**:



## SourceDestinationDict Objects

```python
class SourceDestinationDict(TypedDict)
```



#### build\_namespace\_map

```python
def build_namespace_map(
        connectors: Dict, namespace_map: Union[str, Optional[NamespaceTypes]],
        default_namespace: Optional[str]) -> Dict[str, NamespaceIdentifier]
```

**Arguments**:

  connectors (Dict):
  namespace_map (Union[str, Optional[NamespaceTypes]]):
  default_namespace (Optional[str]):


**Returns**:



## FivetranConnector Objects

```python
class FivetranConnector(FivetranAPI)
```



#### build\_lineage

```python
def build_lineage()
```



#### get\_nodes\_and\_edges

```python
def get_nodes_and_edges() -> Tuple[List[NodeTypes], List[Edge]]
```

**Arguments**:



**Returns**:
