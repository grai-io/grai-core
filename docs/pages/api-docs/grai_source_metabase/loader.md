---
sidebar_label: loader
title: grai_source_metabase.loader
---

## MetabaseAPI Objects

```python
class MetabaseAPI()
```

Wrapper class for interacting with the Metabase API.

**Arguments**:

- `username` _str, optional_ - Metabase username. Defaults to None or returns value from environment variable.
- `password` _str, optional_ - Metabase password. Defaults to None or returns value from environment variable.
- `endpoint` _str, optional_ - Metabase API endpoint URL. Defaults to None.

### authenticate

```python
@retry(stop_max_attempt_number=3, wait_fixed=5000)
def authenticate() -> Dict[str, str]
```

Authenticates the user and sets the session headers.

**Arguments**:

- `request` _callable_ - The HTTP request method to use for authentication.
- `url` _str_ - The URL for the authentication endpoint.


**Raises**:

- `ConnectionError` - If there is an error connecting to the endpoint.

### make\_request

```python
@staticmethod
def make_request(request: Callable[..., requests.Response], url: str) -> Dict
```

Makes an authenticated API request and returns the JSON response.

**Arguments**:

- `request` _callable_ - The HTTP request method to use for the API call.
- `url` _str_ - The URL for the API endpoint.


**Returns**:

- `dict` - The JSON response from the API.


**Raises**:

- `AssertionError` - If the response status code is not 200.

### get\_questions

```python
def get_questions() -> List[api.Question]
```

Retrieves the list of questions from the Metabase API.


### get\_tables

```python
def get_tables() -> List[api.Table]
```

Retrieves the list of tables from the Metabase API.


### get\_table\_metadata

```python
def get_table_metadata(table_id: int) -> api.TableMetadata
```

A table id to retrieve metadata for from Metabase

**Arguments**:

- `table_id` - A table id to retrieve metadata for from Metabase.


### get\_all\_table\_metadata

```python
async def get_all_table_metadata(
        table_ids: List[int]) -> List[api.TableMetadata]
```

**Arguments**:

- `table_ids` - A list of table id&#x27;s to retrieve metadata for from Metabase.


### get\_dbs

```python
def get_dbs() -> List[api.DB]
```

Retrieves the list of databases from the Metabase API.

**Returns**:

- `dict` - The JSON response containing the list of databases.

### get\_collections

```python
def get_collections() -> List[api.Collection]
```

Retrieves the list of collections from the Metabase API.

**Returns**:

- `dict` - The JSON response containing the list of collections.

## MetabaseConnector Objects

```python
class MetabaseConnector(MetabaseAPI)
```

Connector class for interacting with Metabase API and building lineage information.

**Arguments**:

- `namespaces` - A mapping of database IDs to their corresponding namespace names. Defaults to None.
- `default_namespace` - The default namespace to be used when a table or question does not have a specific namespace. Defaults to None.
- `*args` - Additional positional arguments to be passed to the base class constructor.
- `**kwargs` - Additional keyword arguments to be passed to the base class constructor.


**Attributes**:

- `metabase_namespace` _str_ - The default namespace to be used.
- `collections` - A list of active collections in Metabase
- `questions` - A list of non-archived questions returned by Metabase
- `tables` - The list of tables retrieved from the Metabase API.
- `columns` - The list of columns referenced by Metabase Questions

- `tables_map` - A mapping of table IDs to their corresponding table dictionaries.
- `default_namespace`0 - A mapping of database IDs to corresponding database responses.
- `default_namespace`1 - A mapping of question IDs to their corresponding question dictionaries.
- `default_namespace`2 - A mapping of database IDs to their corresponding namespace names.
- `default_namespace`3 - A mapping of question IDs to their corresponding table IDs.
- `default_namespace`4 - A mapping of table IDs to their corresponding database IDs.

### get\_nodes

```python
def get_nodes() -> List[NodeTypes]
```

Retrieves the list of nodes representing tables and questions.

**Returns**:

- `List[NodeTypes]` - The list of nodes.

### get\_edges

```python
def get_edges() -> List[Edge]
```

Retrieves the list of edges representing the relationships between questions and tables.

**Returns**:

- `List[Edge]` - The list of edges.
