---
sidebar_label: main
title: grai_source_fivetran.fivetran_api.main
---

#### approve\_certificate

```python
@app.post("/v1/certificates", response_model=V1CertificatesPostResponse)
def approve_certificate(accept: Optional[str] = Header("application/json",
                                                       alias="Accept"),
                        body: TrustCertificateRequest = None
                        ) -> V1CertificatesPostResponse
```

Approve a certificate

**Arguments**:

- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _TrustCertificateRequest, optional_ - (Default value = None)


**Returns**:



#### create\_connector

```python
@app.post(
    "/v1/connectors",
    response_model=None,
    responses={"201": {
        "model": V1ConnectorsPostResponse
    }},
)
def create_connector(
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept"),
    body: NewConnectorRequestV1 = None
) -> Union[None, V1ConnectorsPostResponse]
```

Create a Connector

**Arguments**:

- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))
- `body` _NewConnectorRequestV1, optional_ - (Default value = None)


**Returns**:



#### connector\_details

```python
@app.get("/v1/connectors/{connector_id}",
         response_model=V1ConnectorsConnectorIdGetResponse)
def connector_details(connector_id: str = Path(..., alias="connectorId"),
                      accept: Optional[str] = Header(
                          "application/json;version=2", alias="Accept")
                      ) -> V1ConnectorsConnectorIdGetResponse
```

Retrieve Connector Details

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_connector

```python
@app.delete(
    "/v1/connectors/{connector_id}",
    response_model=V1ConnectorsConnectorIdDeleteResponse,
)
def delete_connector(connector_id: str = Path(..., alias="connectorId"),
                     accept: Optional[str] = Header(
                         "application/json;version=2", alias="Accept")
                     ) -> V1ConnectorsConnectorIdDeleteResponse
```

Delete a Connector

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### modify\_connector

```python
@app.patch("/v1/connectors/{connector_id}",
           response_model=V1ConnectorsConnectorIdPatchResponse)
def modify_connector(
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept"),
    body: UpdateConnectorRequest = None
) -> V1ConnectorsConnectorIdPatchResponse
```

Modify a Connector

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateConnectorRequest, optional_ - (Default value = None)


**Returns**:



#### connect\_card

```python
@app.post(
    "/v1/connectors/{connector_id}/connect-card",
    response_model=V1ConnectorsConnectorIdConnectCardPostResponse,
)
def connect_card(
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept"),
    body: ConnectCardConfigRequest = None
) -> V1ConnectorsConnectorIdConnectCardPostResponse
```

Connect Card

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))
- `body` _ConnectCardConfigRequest, optional_ - (Default value = None)


**Returns**:



#### connect\_card\_token

```python
@app.post(
    "/v1/connectors/{connector_id}/connect-card-token",
    response_model=CreatePbfTokenResponse,
)
def connect_card_token(connector_id: str = Path(..., alias="connectorId"),
                       accept: Optional[str] = Header(
                           "application/json;version=2",
                           alias="Accept")) -> CreatePbfTokenResponse
```

Connect Card Token

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### resync\_connector

```python
@app.post(
    "/v1/connectors/{connector_id}/resync",
    response_model=V1ConnectorsConnectorIdResyncPostResponse,
)
def resync_connector(
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept"),
    body: ResyncConnectorRequest = None
) -> V1ConnectorsConnectorIdResyncPostResponse
```

Re-sync Connector Data (Historical Sync)

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))
- `body` _ResyncConnectorRequest, optional_ - (Default value = None)


**Returns**:



#### connector\_schema\_config

```python
@app.get(
    "/v1/connectors/{connector_id}/schemas",
    response_model=V1ConnectorsConnectorIdSchemasGetResponse,
)
def connector_schema_config(connector_id: str = Path(..., alias="connectorId"),
                            accept: Optional[str] = Header("application/json",
                                                           alias="Accept")
                            ) -> V1ConnectorsConnectorIdSchemasGetResponse
```

Retrieve a Connector Schema Config

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### modify\_connector\_schema\_config

```python
@app.patch(
    "/v1/connectors/{connector_id}/schemas",
    response_model=V1ConnectorsConnectorIdSchemasPatchResponse,
)
def modify_connector_schema_config(
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: StandardConfigUpdateRequest = None
) -> V1ConnectorsConnectorIdSchemasPatchResponse
```

Modify a Connector Schema Config

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _StandardConfigUpdateRequest, optional_ - (Default value = None)


**Returns**:



#### reload\_connector\_schema\_config

```python
@app.post(
    "/v1/connectors/{connector_id}/schemas/reload",
    response_model=V1ConnectorsConnectorIdSchemasReloadPostResponse,
)
def reload_connector_schema_config(
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: ReloadStandardConfigRequest = None
) -> V1ConnectorsConnectorIdSchemasReloadPostResponse
```

Reload a Connector Schema Config

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _ReloadStandardConfigRequest, optional_ - (Default value = None)


**Returns**:



#### resync\_tables

```python
@app.post(
    "/v1/connectors/{connector_id}/schemas/tables/resync",
    response_model=V1ConnectorsConnectorIdSchemasTablesResyncPostResponse,
)
def resync_tables(
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: V1ConnectorsConnectorIdSchemasTablesResyncPostRequest = None
) -> V1ConnectorsConnectorIdSchemasTablesResyncPostResponse
```

Re-sync Connector Table Data

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _V1ConnectorsConnectorIdSchemasTablesResyncPostRequest, optional_ - (Default value = None)


**Returns**:



#### modify\_connector\_database\_schema\_config

```python
@app.patch(
    "/v1/connectors/{connector_id}/schemas/{schema_name}",
    response_model=V1ConnectorsConnectorIdSchemasSchemaNamePatchResponse,
)
def modify_connector_database_schema_config(
    connector_id: str = Path(..., alias="connectorId"),
    schema_name: str = Path(..., alias="schemaName"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: SchemaUpdateRequest = None
) -> V1ConnectorsConnectorIdSchemasSchemaNamePatchResponse
```

Modify a Connector Database Schema Config

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `schema_name` _str, optional_ - (Default value = Path(..., alias=&quot;schemaName&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _SchemaUpdateRequest, optional_ - (Default value = None)


**Returns**:



#### modify\_connector\_table\_config

```python
@app.patch(
    "/v1/connectors/{connector_id}/schemas/{schema_name}/tables/{table_name}",
    response_model=
    V1ConnectorsConnectorIdSchemasSchemaNameTablesTableNamePatchResponse,
)
def modify_connector_table_config(
    connector_id: str = Path(..., alias="connectorId"),
    schema_name: str = Path(..., alias="schemaName"),
    table_name: str = Path(..., alias="tableName"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: TableUpdateRequest = None
) -> V1ConnectorsConnectorIdSchemasSchemaNameTablesTableNamePatchResponse
```

Modify a Connector Table Config

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `schema_name` _str, optional_ - (Default value = Path(..., alias=&quot;schemaName&quot;))
- `table_name` _str, optional_ - (Default value = Path(..., alias=&quot;tableName&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _TableUpdateRequest, optional_ - (Default value = None)


**Returns**:



#### modify\_connector\_column\_config

```python
@app.patch(
    "/v1/connectors/{connector_id}/schemas/{schema_name}/tables/{table_name}/columns/{column_name}",
    response_model=
    V1ConnectorsConnectorIdSchemasSchemaNameTablesTableNameColumnsColumnNamePatchResponse,
)
def modify_connector_column_config(
    connector_id: str = Path(..., alias="connectorId"),
    schema_name: str = Path(..., alias="schemaName"),
    table_name: str = Path(..., alias="tableName"),
    column_name: str = Path(..., alias="columnName"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: ColumnUpdateRequest = None
) -> V1ConnectorsConnectorIdSchemasSchemaNameTablesTableNameColumnsColumnNamePatchResponse
```

Modify a Connector Column Config

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `schema_name` _str, optional_ - (Default value = Path(..., alias=&quot;schemaName&quot;))
- `table_name` _str, optional_ - (Default value = Path(..., alias=&quot;tableName&quot;))
- `column_name` _str, optional_ - (Default value = Path(..., alias=&quot;columnName&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _ColumnUpdateRequest, optional_ - (Default value = None)


**Returns**:



#### connector\_column\_config

```python
@app.get(
    "/v1/connectors/{connector_id}/schemas/{schema}/tables/{table}/columns",
    response_model=
    V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse,
)
def connector_column_config(
    connector_id: str = Path(..., alias="connectorId"),
    schema: str = ...,
    table: str = ...,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse
```

Retrieve Source Table Columns Config

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `schema` _str, optional_ - (Default value = ...)
- `table` _str, optional_ - (Default value = ...)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### sync\_connector

```python
@app.post(
    "/v1/connectors/{connector_id}/sync",
    response_model=V1ConnectorsConnectorIdSyncPostResponse,
)
def sync_connector(
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept"),
    body: SyncConnectorRequest = None
) -> V1ConnectorsConnectorIdSyncPostResponse
```

Sync Connector Data

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))
- `body` _SyncConnectorRequest, optional_ - (Default value = None)


**Returns**:



#### run\_setup\_tests

```python
@app.post(
    "/v1/connectors/{connector_id}/test",
    response_model=V1ConnectorsConnectorIdTestPostResponse,
)
def run_setup_tests(
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept"),
    body: RunSetupTestsRequest = None
) -> V1ConnectorsConnectorIdTestPostResponse
```

Run connector setup tests

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))
- `body` _RunSetupTestsRequest, optional_ - (Default value = None)


**Returns**:



#### dbt\_model\_details

```python
@app.get("/v1/dbt/models/{model_id}",
         response_model=V1DbtModelsModelIdGetResponse)
def dbt_model_details(model_id: str = Path(..., alias="modelId"),
                      accept: Optional[str] = Header(
                          "application/json",
                          alias="Accept")) -> V1DbtModelsModelIdGetResponse
```

Retrieve DBT Model Details

**Arguments**:

- `model_id` _str, optional_ - (Default value = Path(..., alias=&quot;modelId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### list\_dbt\_projects

```python
@app.get("/v1/dbt/projects", response_model=V1DbtProjectsGetResponse)
def list_dbt_projects(
    group_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1DbtProjectsGetResponse
```

List All DBT Projects

**Arguments**:

- `group_id` _Optional[str], optional_ - (Default value = None)
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### create\_dbt\_project

```python
@app.post(
    "/v1/dbt/projects",
    response_model=None,
    responses={"201": {
        "model": V1DbtProjectsPostResponse
    }},
)
def create_dbt_project(
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: NewDbtProjectRequest = None
) -> Union[None, V1DbtProjectsPostResponse]
```

Create DBT Project

**Arguments**:

- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _NewDbtProjectRequest, optional_ - (Default value = None)


**Returns**:



#### dbt\_project\_details

```python
@app.get("/v1/dbt/projects/{project_id}",
         response_model=V1DbtProjectsProjectIdGetResponse)
def dbt_project_details(project_id: str = Path(..., alias="projectId"),
                        accept: Optional[str] = Header("application/json",
                                                       alias="Accept")
                        ) -> V1DbtProjectsProjectIdGetResponse
```

Retrieve DBT Project Details

**Arguments**:

- `project_id` _str, optional_ - (Default value = Path(..., alias=&quot;projectId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### list\_dbt\_project\_models

```python
@app.get(
    "/v1/dbt/projects/{project_id}/models",
    response_model=V1DbtProjectsProjectIdModelsGetResponse,
)
def list_dbt_project_models(
    project_id: str = Path(..., alias="projectId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1DbtProjectsProjectIdModelsGetResponse
```

List All DBT Models

**Arguments**:

- `project_id` _str, optional_ - (Default value = Path(..., alias=&quot;projectId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### test\_dbt\_project

```python
@app.post(
    "/v1/dbt/projects/{project_id}/test",
    response_model=V1DbtProjectsProjectIdTestPostResponse,
)
def test_dbt_project(project_id: str = Path(..., alias="projectId"),
                     accept: Optional[str] = Header("application/json",
                                                    alias="Accept")
                     ) -> V1DbtProjectsProjectIdTestPostResponse
```

Test DBT Project

**Arguments**:

- `project_id` _str, optional_ - (Default value = Path(..., alias=&quot;projectId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### list\_dbt\_project\_transformations

```python
@app.get(
    "/v1/dbt/projects/{project_id}/transformations",
    response_model=V1DbtProjectsProjectIdTransformationsGetResponse,
)
def list_dbt_project_transformations(
    project_id: str = Path(..., alias="projectId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1DbtProjectsProjectIdTransformationsGetResponse
```

List All DBT Transformations

**Arguments**:

- `project_id` _str, optional_ - (Default value = Path(..., alias=&quot;projectId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### create\_dbt\_transformation

```python
@app.post(
    "/v1/dbt/projects/{project_id}/transformations",
    response_model=None,
    responses={
        "201": {
            "model": V1DbtProjectsProjectIdTransformationsPostResponse
        }
    },
)
def create_dbt_transformation(
    project_id: str = Path(..., alias="projectId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: NewTransformationRequest = None
) -> Union[None, V1DbtProjectsProjectIdTransformationsPostResponse]
```

Create DBT Transformation

**Arguments**:

- `project_id` _str, optional_ - (Default value = Path(..., alias=&quot;projectId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _NewTransformationRequest, optional_ - (Default value = None)


**Returns**:



#### dbt\_transformation\_details

```python
@app.get(
    "/v1/dbt/transformations/{transformation_id}",
    response_model=V1DbtTransformationsTransformationIdGetResponse,
)
def dbt_transformation_details(
        transformation_id: str = Path(..., alias="transformationId"),
        accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1DbtTransformationsTransformationIdGetResponse
```

Retrieve DBT Transformation Details

**Arguments**:

- `transformation_id` _str, optional_ - (Default value = Path(..., alias=&quot;transformationId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_dbt\_transformation

```python
@app.delete(
    "/v1/dbt/transformations/{transformation_id}",
    response_model=V1DbtTransformationsTransformationIdDeleteResponse,
)
def delete_dbt_transformation(
        transformation_id: str = Path(..., alias="transformationId"),
        accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1DbtTransformationsTransformationIdDeleteResponse
```

Delete DBT Transformation

**Arguments**:

- `transformation_id` _str, optional_ - (Default value = Path(..., alias=&quot;transformationId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### modify\_dbt\_transformation

```python
@app.patch(
    "/v1/dbt/transformations/{transformation_id}",
    response_model=V1DbtTransformationsTransformationIdPatchResponse,
)
def modify_dbt_transformation(
    transformation_id: str = Path(..., alias="transformationId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: UpdateTransformationRequest = None
) -> V1DbtTransformationsTransformationIdPatchResponse
```

Modify DBT Transformation

**Arguments**:

- `transformation_id` _str, optional_ - (Default value = Path(..., alias=&quot;transformationId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateTransformationRequest, optional_ - (Default value = None)


**Returns**:



#### create\_destination

```python
@app.post(
    "/v1/destinations",
    response_model=None,
    responses={"201": {
        "model": V1DestinationsPostResponse
    }},
)
def create_destination(
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept"),
    body: NewDestinationRequest = None
) -> Union[None, V1DestinationsPostResponse]
```

Create destination

**Arguments**:

- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))
- `body` _NewDestinationRequest, optional_ - (Default value = None)


**Returns**:



#### destination\_details

```python
@app.get(
    "/v1/destinations/{destination_id}",
    response_model=V1DestinationsDestinationIdGetResponse,
)
def destination_details(destination_id: str = Path(..., alias="destinationId"),
                        accept: Optional[str] = Header(
                            "application/json;version=2", alias="Accept")
                        ) -> V1DestinationsDestinationIdGetResponse
```

Retrieve Destination Details

**Arguments**:

- `destination_id` _str, optional_ - (Default value = Path(..., alias=&quot;destinationId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_destination

```python
@app.delete(
    "/v1/destinations/{destination_id}",
    response_model=V1DestinationsDestinationIdDeleteResponse,
)
def delete_destination(destination_id: str = Path(..., alias="destinationId"),
                       accept: Optional[str] = Header(
                           "application/json;version=2", alias="Accept")
                       ) -> V1DestinationsDestinationIdDeleteResponse
```

Delete a destination

**Arguments**:

- `destination_id` _str, optional_ - (Default value = Path(..., alias=&quot;destinationId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### modify\_destination

```python
@app.patch(
    "/v1/destinations/{destination_id}",
    response_model=V1DestinationsDestinationIdPatchResponse,
)
def modify_destination(
    destination_id: str = Path(..., alias="destinationId"),
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept"),
    body: UpdateDestinationRequest = None
) -> V1DestinationsDestinationIdPatchResponse
```

Modify a Destination

**Arguments**:

- `destination_id` _str, optional_ - (Default value = Path(..., alias=&quot;destinationId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateDestinationRequest, optional_ - (Default value = None)


**Returns**:



#### run\_destination\_setup\_tests

```python
@app.post(
    "/v1/destinations/{destination_id}/test",
    response_model=V1DestinationsDestinationIdTestPostResponse,
)
def run_destination_setup_tests(
    destination_id: str = Path(..., alias="destinationId"),
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept"),
    body: RunSetupTestsRequest = None
) -> V1DestinationsDestinationIdTestPostResponse
```

Run Destination Setup Tests

**Arguments**:

- `destination_id` _str, optional_ - (Default value = Path(..., alias=&quot;destinationId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))
- `body` _RunSetupTestsRequest, optional_ - (Default value = None)


**Returns**:



#### approve\_fingerprint

```python
@app.post("/v1/fingerprints", response_model=V1FingerprintsPostResponse)
def approve_fingerprint(accept: Optional[str] = Header("application/json",
                                                       alias="Accept"),
                        body: TrustFingerprintRequest = None
                        ) -> V1FingerprintsPostResponse
```

Approve a fingerprint

**Arguments**:

- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _TrustFingerprintRequest, optional_ - (Default value = None)


**Returns**:



#### list\_all\_groups

```python
@app.get("/v1/groups", response_model=V1GroupsGetResponse)
def list_all_groups(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1GroupsGetResponse
```

List All Groups

**Arguments**:

- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### create\_group

```python
@app.post(
    "/v1/groups",
    response_model=None,
    responses={"201": {
        "model": V1GroupsPostResponse
    }},
)
def create_group(accept: Optional[str] = Header("application/json",
                                                alias="Accept"),
                 body: NewGroupRequest = None
                 ) -> Union[None, V1GroupsPostResponse]
```

Create a Group

**Arguments**:

- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _NewGroupRequest, optional_ - (Default value = None)


**Returns**:



#### group\_details

```python
@app.get("/v1/groups/{group_id}", response_model=V1GroupsGroupIdGetResponse)
def group_details(group_id: str = Path(..., alias="groupId"),
                  accept: Optional[str] = Header(
                      "application/json",
                      alias="Accept")) -> V1GroupsGroupIdGetResponse
```

Retrieve Group Details

**Arguments**:

- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_group

```python
@app.delete("/v1/groups/{group_id}",
            response_model=V1GroupsGroupIdDeleteResponse)
def delete_group(group_id: str = Path(..., alias="groupId"),
                 accept: Optional[str] = Header(
                     "application/json",
                     alias="Accept")) -> V1GroupsGroupIdDeleteResponse
```

Delete a group

**Arguments**:

- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### modify\_group

```python
@app.patch("/v1/groups/{group_id}",
           response_model=V1GroupsGroupIdPatchResponse)
def modify_group(group_id: str = Path(..., alias="groupId"),
                 accept: Optional[str] = Header("application/json",
                                                alias="Accept"),
                 body: UpdateGroupRequest = None
                 ) -> V1GroupsGroupIdPatchResponse
```

Modify a Group

**Arguments**:

- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateGroupRequest, optional_ - (Default value = None)


**Returns**:



#### list\_all\_connectors\_in\_group

```python
@app.get(
    "/v1/groups/{group_id}/connectors",
    response_model=V1GroupsGroupIdConnectorsGetResponse,
)
def list_all_connectors_in_group(
    group_id: str = Path(..., alias="groupId"),
    schema: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1GroupsGroupIdConnectorsGetResponse
```

List All Connectors within a Group

**Arguments**:

- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `schema` _Optional[str], optional_ - (Default value = None)
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### list\_all\_users\_in\_group

```python
@app.get("/v1/groups/{group_id}/users",
         response_model=V1GroupsGroupIdUsersGetResponse)
def list_all_users_in_group(
    group_id: str = Path(..., alias="groupId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1GroupsGroupIdUsersGetResponse
```

List All Users within a Group

**Arguments**:

- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### add\_user\_to\_group

```python
@app.post("/v1/groups/{group_id}/users",
          response_model=V1GroupsGroupIdUsersPostResponse)
def add_user_to_group(
        group_id: str = Path(..., alias="groupId"),
        accept: Optional[str] = Header("application/json", alias="Accept"),
        body: AddUserToGroupRequest = None
) -> V1GroupsGroupIdUsersPostResponse
```

Add a User to a Group

**Arguments**:

- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _AddUserToGroupRequest, optional_ - (Default value = None)


**Returns**:



#### delete\_user\_from\_group

```python
@app.delete(
    "/v1/groups/{group_id}/users/{user_id}",
    response_model=V1GroupsGroupIdUsersUserIdDeleteResponse,
)
def delete_user_from_group(group_id: str = Path(..., alias="groupId"),
                           user_id: str = Path(..., alias="userId"),
                           accept: Optional[str] = Header("application/json",
                                                          alias="Accept")
                           ) -> V1GroupsGroupIdUsersUserIdDeleteResponse
```

Remove a User from a Group

**Arguments**:

- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### column\_metadata

```python
@app.get(
    "/v1/metadata/connectors/{connector_id}/columns",
    response_model=V1MetadataConnectorsConnectorIdColumnsGetResponse,
)
def column_metadata(
    connector_id: str = Path(..., alias="connectorId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1MetadataConnectorsConnectorIdColumnsGetResponse
```

Retrieve column metadata

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### schema\_metadata

```python
@app.get(
    "/v1/metadata/connectors/{connector_id}/schemas",
    response_model=V1MetadataConnectorsConnectorIdSchemasGetResponse,
)
def schema_metadata(
    connector_id: str = Path(..., alias="connectorId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1MetadataConnectorsConnectorIdSchemasGetResponse
```

Retrieve schema metadata

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### table\_metadata

```python
@app.get(
    "/v1/metadata/connectors/{connector_id}/tables",
    response_model=V1MetadataConnectorsConnectorIdTablesGetResponse,
)
def table_metadata(
    connector_id: str = Path(..., alias="connectorId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1MetadataConnectorsConnectorIdTablesGetResponse
```

Retrieve table metadata

**Arguments**:

- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### metadata\_connectors

```python
@app.get("/v1/metadata/{name}", response_model=V1MetadataNameGetResponse)
def metadata_connectors(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept")
) -> V1MetadataNameGetResponse
```

Retrieve source metadata

**Arguments**:

- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### metadata\_connector\_config

```python
@app.get("/v1/metadata/{name}/{service}",
         response_model=V1MetadataNameServiceGetResponse)
def metadata_connector_config(
    service: str,
    accept: Optional[str] = Header("application/json;version=2",
                                   alias="Accept")
) -> V1MetadataNameServiceGetResponse
```

Retrieve connector configuration metadata

**Arguments**:

  service (str):
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json;version=2&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### list\_all\_roles

```python
@app.get("/v1/roles", response_model=V1RolesGetResponse)
def list_all_roles(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1RolesGetResponse
```

List all roles

**Arguments**:

- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### list\_all\_teams

```python
@app.get("/v1/teams", response_model=V1TeamsGetResponse)
def list_all_teams(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1TeamsGetResponse
```

List all teams

**Arguments**:

- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### create\_team

```python
@app.post("/v1/teams",
          response_model=None,
          responses={"201": {
              "model": V1TeamsPostResponse
          }})
def create_team(accept: Optional[str] = Header("application/json",
                                               alias="Accept"),
                body: TeamRequest = None) -> Union[None, V1TeamsPostResponse]
```

Create a team

**Arguments**:

- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _TeamRequest, optional_ - (Default value = None)


**Returns**:



#### team\_details

```python
@app.get("/v1/teams/{team_id}", response_model=V1TeamsTeamIdGetResponse)
def team_details(team_id: str = Path(..., alias="teamId"),
                 accept: Optional[str] = Header(
                     "application/json",
                     alias="Accept")) -> V1TeamsTeamIdGetResponse
```

Retrieve team details

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_team

```python
@app.delete("/v1/teams/{team_id}", response_model=V1TeamsTeamIdDeleteResponse)
def delete_team(team_id: str = Path(..., alias="teamId"),
                accept: Optional[str] = Header(
                    "application/json",
                    alias="Accept")) -> V1TeamsTeamIdDeleteResponse
```

Delete a team

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### modify\_team

```python
@app.patch("/v1/teams/{team_id}", response_model=V1TeamsTeamIdPatchResponse)
def modify_team(team_id: str = Path(..., alias="teamId"),
                accept: Optional[str] = Header("application/json",
                                               alias="Accept"),
                body: TeamRequest = None) -> V1TeamsTeamIdPatchResponse
```

Modify a team

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _TeamRequest, optional_ - (Default value = None)


**Returns**:



#### get\_team\_memberships\_in\_connectors

```python
@app.get("/v1/teams/{team_id}/connectors",
         response_model=V1TeamsTeamIdConnectorsGetResponse)
def get_team_memberships_in_connectors(
    team_id: str = Path(..., alias="teamId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1TeamsTeamIdConnectorsGetResponse
```

List all connector memberships

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### add\_team\_membership\_in\_connector

```python
@app.post(
    "/v1/teams/{team_id}/connectors",
    response_model=None,
    responses={"201": {
        "model": V1TeamsTeamIdConnectorsPostResponse
    }},
)
def add_team_membership_in_connector(
    team_id: str = Path(..., alias="teamId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: MembershipRequest = None
) -> Union[None, V1TeamsTeamIdConnectorsPostResponse]
```

Add connector membership

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _MembershipRequest, optional_ - (Default value = None)


**Returns**:



#### get\_team\_membership\_in\_connector

```python
@app.get(
    "/v1/teams/{team_id}/connectors/{connector_id}",
    response_model=V1TeamsTeamIdConnectorsConnectorIdGetResponse,
)
def get_team_membership_in_connector(
        team_id: str = Path(..., alias="teamId"),
        connector_id: str = Path(..., alias="connectorId"),
        accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1TeamsTeamIdConnectorsConnectorIdGetResponse
```

Retrieve connector membership

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_team\_membership\_in\_connector

```python
@app.delete(
    "/v1/teams/{team_id}/connectors/{connector_id}",
    response_model=V1TeamsTeamIdConnectorsConnectorIdDeleteResponse,
)
def delete_team_membership_in_connector(
        team_id: str = Path(..., alias="teamId"),
        connector_id: str = Path(..., alias="connectorId"),
        accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1TeamsTeamIdConnectorsConnectorIdDeleteResponse
```

Delete connector membership

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### update\_team\_membership\_in\_connector

```python
@app.patch(
    "/v1/teams/{team_id}/connectors/{connector_id}",
    response_model=V1TeamsTeamIdConnectorsConnectorIdPatchResponse,
)
def update_team_membership_in_connector(
    team_id: str = Path(..., alias="teamId"),
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: UpdateMembershipRequest = None
) -> V1TeamsTeamIdConnectorsConnectorIdPatchResponse
```

Update connector membership

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateMembershipRequest, optional_ - (Default value = None)


**Returns**:



#### get\_team\_memberships\_in\_groups

```python
@app.get("/v1/teams/{team_id}/groups",
         response_model=V1TeamsTeamIdGroupsGetResponse)
def get_team_memberships_in_groups(
    team_id: str = Path(..., alias="teamId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1TeamsTeamIdGroupsGetResponse
```

List all group memberships

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### add\_team\_membership\_in\_group

```python
@app.post(
    "/v1/teams/{team_id}/groups",
    response_model=None,
    responses={"201": {
        "model": V1TeamsTeamIdGroupsPostResponse
    }},
)
def add_team_membership_in_group(
    team_id: str = Path(..., alias="teamId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: MembershipRequest = None
) -> Union[None, V1TeamsTeamIdGroupsPostResponse]
```

Add group membership

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _MembershipRequest, optional_ - (Default value = None)


**Returns**:



#### get\_team\_membership\_in\_group

```python
@app.get(
    "/v1/teams/{team_id}/groups/{group_id}",
    response_model=V1TeamsTeamIdGroupsGroupIdGetResponse,
)
def get_team_membership_in_group(team_id: str = Path(..., alias="teamId"),
                                 group_id: str = Path(..., alias="groupId"),
                                 accept: Optional[str] = Header(
                                     "application/json", alias="Accept")
                                 ) -> V1TeamsTeamIdGroupsGroupIdGetResponse
```

Retrieve group membership

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_team\_membership\_in\_group

```python
@app.delete(
    "/v1/teams/{team_id}/groups/{group_id}",
    response_model=V1TeamsTeamIdGroupsGroupIdDeleteResponse,
)
def delete_team_membership_in_group(
        team_id: str = Path(..., alias="teamId"),
        group_id: str = Path(..., alias="groupId"),
        accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1TeamsTeamIdGroupsGroupIdDeleteResponse
```

Delete group membership

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### update\_team\_membership\_in\_group

```python
@app.patch(
    "/v1/teams/{team_id}/groups/{group_id}",
    response_model=V1TeamsTeamIdGroupsGroupIdPatchResponse,
)
def update_team_membership_in_group(
    team_id: str = Path(..., alias="teamId"),
    group_id: str = Path(..., alias="groupId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: UpdateMembershipRequest = None
) -> V1TeamsTeamIdGroupsGroupIdPatchResponse
```

Update group membership

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateMembershipRequest, optional_ - (Default value = None)


**Returns**:



#### delete\_team\_membership\_in\_account

```python
@app.delete("/v1/teams/{team_id}/role",
            response_model=V1TeamsTeamIdRoleDeleteResponse)
def delete_team_membership_in_account(team_id: str = Path(..., alias="teamId"),
                                      accept: Optional[str] = Header(
                                          "application/json", alias="Accept")
                                      ) -> V1TeamsTeamIdRoleDeleteResponse
```

Delete team role in account

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### list\_users\_in\_team

```python
@app.get("/v1/teams/{team_id}/users",
         response_model=V1TeamsTeamIdUsersGetResponse)
def list_users_in_team(
    team_id: str = Path(..., alias="teamId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1TeamsTeamIdUsersGetResponse
```

List all user memberships

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### add\_user\_to\_team

```python
@app.post(
    "/v1/teams/{team_id}/users",
    response_model=None,
    responses={"201": {
        "model": V1TeamsTeamIdUsersPostResponse
    }},
)
def add_user_to_team(
    team_id: str = Path(..., alias="teamId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: TeamMembershipRequest = None
) -> Union[None, V1TeamsTeamIdUsersPostResponse]
```

Add a user to a team

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _TeamMembershipRequest, optional_ - (Default value = None)


**Returns**:



#### get\_user\_in\_team

```python
@app.get(
    "/v1/teams/{team_id}/users/{user_id}",
    response_model=V1TeamsTeamIdUsersUserIdGetResponse,
)
def get_user_in_team(team_id: str = Path(..., alias="teamId"),
                     user_id: str = Path(..., alias="userId"),
                     accept: Optional[str] = Header("application/json",
                                                    alias="Accept")
                     ) -> V1TeamsTeamIdUsersUserIdGetResponse
```

Retrieve user membership in a team

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_user\_from\_team

```python
@app.delete(
    "/v1/teams/{team_id}/users/{user_id}",
    response_model=V1TeamsTeamIdUsersUserIdDeleteResponse,
)
def delete_user_from_team(team_id: str = Path(..., alias="teamId"),
                          user_id: str = Path(..., alias="userId"),
                          accept: Optional[str] = Header("application/json",
                                                         alias="Accept")
                          ) -> V1TeamsTeamIdUsersUserIdDeleteResponse
```

Delete a user from a team

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### update\_user\_membership

```python
@app.patch(
    "/v1/teams/{team_id}/users/{user_id}",
    response_model=V1TeamsTeamIdUsersUserIdPatchResponse,
)
def update_user_membership(
    team_id: str = Path(..., alias="teamId"),
    user_id: str = Path(..., alias="userId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: UpdateMembershipRequest = None
) -> V1TeamsTeamIdUsersUserIdPatchResponse
```

Modify a user membership

**Arguments**:

- `team_id` _str, optional_ - (Default value = Path(..., alias=&quot;teamId&quot;))
- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateMembershipRequest, optional_ - (Default value = None)


**Returns**:



#### list\_all\_users

```python
@app.get("/v1/users", response_model=V1UsersGetResponse)
def list_all_users(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1UsersGetResponse
```

List All Users

**Arguments**:

- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### create\_user

```python
@app.post("/v1/users",
          response_model=None,
          responses={"201": {
              "model": V1UsersPostResponse
          }})
def create_user(accept: Optional[str] = Header("application/json",
                                               alias="Accept"),
                body: NewUserRequest = None
                ) -> Union[None, V1UsersPostResponse]
```

Invite a User

**Arguments**:

- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _NewUserRequest, optional_ - (Default value = None)


**Returns**:



#### delete\_user

```python
@app.delete("/v1/users/{id}", response_model=V1UsersIdDeleteResponse)
def delete_user(
    id: str,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1UsersIdDeleteResponse
```

Delete a user

**Arguments**:

  id (str):
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### user\_details

```python
@app.get("/v1/users/{user_id}", response_model=V1UsersUserIdGetResponse)
def user_details(user_id: str = Path(..., alias="userId"),
                 accept: Optional[str] = Header(
                     "application/json",
                     alias="Accept")) -> V1UsersUserIdGetResponse
```

Retrieve User Details

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### modify\_user

```python
@app.patch("/v1/users/{user_id}", response_model=V1UsersUserIdPatchResponse)
def modify_user(user_id: str = Path(..., alias="userId"),
                accept: Optional[str] = Header("application/json",
                                               alias="Accept"),
                body: UpdateUserRequest = None) -> V1UsersUserIdPatchResponse
```

Modify a User

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateUserRequest, optional_ - (Default value = None)


**Returns**:



#### get\_user\_memberships\_in\_connectors

```python
@app.get("/v1/users/{user_id}/connectors",
         response_model=V1UsersUserIdConnectorsGetResponse)
def get_user_memberships_in_connectors(
    user_id: str = Path(..., alias="userId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1UsersUserIdConnectorsGetResponse
```

List all connector memberships

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### add\_user\_membership\_in\_connector

```python
@app.post(
    "/v1/users/{user_id}/connectors",
    response_model=None,
    responses={"201": {
        "model": MembershipResponse
    }},
)
def add_user_membership_in_connector(user_id: str = Path(..., alias="userId"),
                                     accept: Optional[str] = Header(
                                         "application/json", alias="Accept"),
                                     body: MembershipRequest = None
                                     ) -> Union[None, MembershipResponse]
```

Add connector membership

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _MembershipRequest, optional_ - (Default value = None)


**Returns**:



#### get\_user\_membership\_in\_connector

```python
@app.get(
    "/v1/users/{user_id}/connectors/{connector_id}",
    response_model=V1UsersUserIdConnectorsConnectorIdGetResponse,
)
def get_user_membership_in_connector(
        user_id: str = Path(..., alias="userId"),
        connector_id: str = Path(..., alias="connectorId"),
        accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1UsersUserIdConnectorsConnectorIdGetResponse
```

Retrieve connector membership

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_user\_membership\_in\_connector

```python
@app.delete(
    "/v1/users/{user_id}/connectors/{connector_id}",
    response_model=V1UsersUserIdConnectorsConnectorIdDeleteResponse,
)
def delete_user_membership_in_connector(
        user_id: str = Path(..., alias="userId"),
        connector_id: str = Path(..., alias="connectorId"),
        accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1UsersUserIdConnectorsConnectorIdDeleteResponse
```

Delete connector membership

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### update\_user\_membership\_in\_connector

```python
@app.patch(
    "/v1/users/{user_id}/connectors/{connector_id}",
    response_model=V1UsersUserIdConnectorsConnectorIdPatchResponse,
)
def update_user_membership_in_connector(
    user_id: str = Path(..., alias="userId"),
    connector_id: str = Path(..., alias="connectorId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: UpdateMembershipRequest = None
) -> V1UsersUserIdConnectorsConnectorIdPatchResponse
```

Update connector membership

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `connector_id` _str, optional_ - (Default value = Path(..., alias=&quot;connectorId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateMembershipRequest, optional_ - (Default value = None)


**Returns**:



#### get\_user\_memberships\_in\_groups

```python
@app.get("/v1/users/{user_id}/groups",
         response_model=V1UsersUserIdGroupsGetResponse)
def get_user_memberships_in_groups(
    user_id: str = Path(..., alias="userId"),
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1UsersUserIdGroupsGetResponse
```

List all group memberships

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### add\_user\_membership\_in\_group

```python
@app.post(
    "/v1/users/{user_id}/groups",
    response_model=None,
    responses={"201": {
        "model": V1UsersUserIdGroupsPostResponse
    }},
)
def add_user_membership_in_group(
    user_id: str = Path(..., alias="userId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: MembershipRequest = None
) -> Union[None, V1UsersUserIdGroupsPostResponse]
```

Add group membership

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _MembershipRequest, optional_ - (Default value = None)


**Returns**:



#### get\_user\_membership\_in\_group

```python
@app.get(
    "/v1/users/{user_id}/groups/{group_id}",
    response_model=V1UsersUserIdGroupsGroupIdGetResponse,
)
def get_user_membership_in_group(user_id: str = Path(..., alias="userId"),
                                 group_id: str = Path(..., alias="groupId"),
                                 accept: Optional[str] = Header(
                                     "application/json", alias="Accept")
                                 ) -> V1UsersUserIdGroupsGroupIdGetResponse
```

Retrieve group membership

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_user\_membership\_in\_group

```python
@app.delete(
    "/v1/users/{user_id}/groups/{group_id}",
    response_model=V1UsersUserIdGroupsGroupIdDeleteResponse,
)
def delete_user_membership_in_group(
        user_id: str = Path(..., alias="userId"),
        group_id: str = Path(..., alias="groupId"),
        accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1UsersUserIdGroupsGroupIdDeleteResponse
```

Delete group membership

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### update\_user\_membership\_in\_group

```python
@app.patch(
    "/v1/users/{user_id}/groups/{group_id}",
    response_model=V1UsersUserIdGroupsGroupIdPatchResponse,
)
def update_user_membership_in_group(
    user_id: str = Path(..., alias="userId"),
    group_id: str = Path(..., alias="groupId"),
    accept: Optional[str] = Header("application/json", alias="Accept"),
    body: UpdateMembershipRequest = None
) -> V1UsersUserIdGroupsGroupIdPatchResponse
```

Update group membership

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _UpdateMembershipRequest, optional_ - (Default value = None)


**Returns**:



#### delete\_user\_membership\_in\_account

```python
@app.delete("/v1/users/{user_id}/role",
            response_model=V1UsersUserIdRoleDeleteResponse)
def delete_user_membership_in_account(user_id: str = Path(..., alias="userId"),
                                      accept: Optional[str] = Header(
                                          "application/json", alias="Accept")
                                      ) -> V1UsersUserIdRoleDeleteResponse
```

Delete user role in account

**Arguments**:

- `user_id` _str, optional_ - (Default value = Path(..., alias=&quot;userId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### list\_all\_webhooks

```python
@app.get("/v1/webhooks", response_model=V1WebhooksGetResponse)
def list_all_webhooks(
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    accept: Optional[str] = Header("application/json", alias="Accept")
) -> V1WebhooksGetResponse
```

Retrieve the list of webhooks

**Arguments**:

- `cursor` _Optional[str], optional_ - (Default value = None)
- `limit` _Optional[int], optional_ - (Default value = None)
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### create\_account\_webhook

```python
@app.post("/v1/webhooks/account", response_model=WebhookResponse)
def create_account_webhook(accept: Optional[str] = Header("application/json",
                                                          alias="Accept"),
                           body: WebhookRequest = None) -> WebhookResponse
```

Create account webhook

**Arguments**:

- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _WebhookRequest, optional_ - (Default value = None)


**Returns**:



#### create\_group\_webhook

```python
@app.post("/v1/webhooks/group/{group_id}", response_model=WebhookResponse)
def create_group_webhook(group_id: str = Path(..., alias="groupId"),
                         accept: Optional[str] = Header("application/json",
                                                        alias="Accept"),
                         body: WebhookRequest = None) -> WebhookResponse
```

Create group webhook

**Arguments**:

- `group_id` _str, optional_ - (Default value = Path(..., alias=&quot;groupId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _WebhookRequest, optional_ - (Default value = None)


**Returns**:



#### webhook\_details

```python
@app.get("/v1/webhooks/{webhook_id}", response_model=WebhookResponse)
def webhook_details(webhook_id: str = Path(..., alias="webhookId"),
                    accept: Optional[str] = Header(
                        "application/json",
                        alias="Accept")) -> WebhookResponse
```

Retrieve webhook details

**Arguments**:

- `webhook_id` _str, optional_ - (Default value = Path(..., alias=&quot;webhookId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### delete\_webhook

```python
@app.delete("/v1/webhooks/{webhook_id}",
            response_model=None,
            responses={"204": {
                "model": str
            }})
def delete_webhook(webhook_id: str = Path(..., alias="webhookId"),
                   accept: Optional[str] = Header(
                       "application/json",
                       alias="Accept")) -> Union[None, str]
```

Delete webhook

**Arguments**:

- `webhook_id` _str, optional_ - (Default value = Path(..., alias=&quot;webhookId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))


**Returns**:



#### modify\_webhook

```python
@app.patch("/v1/webhooks/{webhook_id}", response_model=WebhookResponse)
def modify_webhook(webhook_id: str = Path(..., alias="webhookId"),
                   accept: Optional[str] = Header("application/json",
                                                  alias="Accept"),
                   body: WebhookRequest = None) -> WebhookResponse
```

Update webhook

**Arguments**:

- `webhook_id` _str, optional_ - (Default value = Path(..., alias=&quot;webhookId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _WebhookRequest, optional_ - (Default value = None)


**Returns**:



#### test\_webhook

```python
@app.post("/v1/webhooks/{webhook_id}/test", response_model=WebhookTestResponse)
def test_webhook(webhook_id: str = Path(..., alias="webhookId"),
                 accept: Optional[str] = Header("application/json",
                                                alias="Accept"),
                 body: WebhookTestRequest = None) -> WebhookTestResponse
```

Test webhook

**Arguments**:

- `webhook_id` _str, optional_ - (Default value = Path(..., alias=&quot;webhookId&quot;))
- `accept` _Optional[str], optional_ - (Default value = Header(&quot;application/json&quot;, alias=&quot;Accept&quot;))
- `body` _WebhookTestRequest, optional_ - (Default value = None)


**Returns**:
