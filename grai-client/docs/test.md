<a id="grai_client"></a>

# grai\_client

<a id="grai_client.update"></a>

# grai\_client.update

<a id="grai_client.endpoints.v1.delete"></a>

# grai\_client.endpoints.v1.delete

<a id="grai_client.endpoints.v1.patch"></a>

# grai\_client.endpoints.v1.patch

<a id="grai_client.endpoints.v1.post"></a>

# grai\_client.endpoints.v1.post

<a id="grai_client.endpoints.v1.client"></a>

# grai\_client.endpoints.v1.client

<a id="grai_client.endpoints.v1.client.ClientV1"></a>

## ClientV1 Objects

```python
class ClientV1(BaseClient)
```

<a id="grai_client.endpoints.v1.client.ClientV1.authenticate"></a>

#### authenticate

```python
def authenticate(username: Optional[str] = None,
                 password: Optional[str] = None,
                 api_key: Optional[str] = None) -> None
```

Authenticate with the server.

Caution: This function is unstable and can produce unexpected results.

<a id="grai_client.endpoints.v1"></a>

# grai\_client.endpoints.v1

<a id="grai_client.endpoints.v1.url"></a>

# grai\_client.endpoints.v1.url

<a id="grai_client.endpoints.v1.utils"></a>

# grai\_client.endpoints.v1.utils

<a id="grai_client.endpoints.v1.utils.process_node_id"></a>

#### process\_node\_id

```python
async def process_node_id(
    client: ClientV1,
    grai_type: NodeIdTypes,
    options: ClientOptions = ClientOptions()
) -> NodeIdTypes
```

Process a NodeID object, either by returning if it has a known id, or by getting
the id from the server.

<a id="grai_client.endpoints.v1.get"></a>

# grai\_client.endpoints.v1.get

<a id="grai_client.endpoints.rest"></a>

# grai\_client.endpoints.rest

<a id="grai_client.endpoints.client"></a>

# grai\_client.endpoints.client

<a id="grai_client.endpoints"></a>

# grai\_client.endpoints

<a id="grai_client.endpoints.utilities"></a>

# grai\_client.endpoints.utilities

<a id="grai_client.endpoints.utilities.GraiEncoder"></a>

## GraiEncoder Objects

```python
class GraiEncoder(json.JSONEncoder)
```

Needed for the base python json implementation

<a id="grai_client.schemas.labels"></a>

# grai\_client.schemas.labels

<a id="grai_client.schemas"></a>

# grai\_client.schemas

<a id="grai_client.schemas.workspace"></a>

# grai\_client.schemas.workspace

<a id="grai_client.schemas.schema"></a>

# grai\_client.schemas.schema

<a id="grai_client.utilities"></a>

# grai\_client.utilities

<a id="grai_client.utilities.tests"></a>

# grai\_client.utilities.tests

<a id="grai_client.testing"></a>

# grai\_client.testing

<a id="grai_client.testing.schema"></a>

# grai\_client.testing.schema

<a id="grai_client.authentication"></a>

# grai\_client.authentication
