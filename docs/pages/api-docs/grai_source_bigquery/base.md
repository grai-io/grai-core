---
sidebar_label: base
title: grai_source_bigquery.base
---

## BigQueryIntegration Objects

```python
class BigQueryIntegration(GraiIntegrationImplementation)
```

BigQuery integration.

**Attributes**:

- `connector` - The BigQuery connector

### \_\_init\_\_

```python
def __init__(source: SourceV1,
             version: Optional[str] = None,
             namespace: Optional[str] = None,
             project: Optional[str] = None,
             dataset: Optional[Union[str, List[str]]] = None,
             credentials: Optional[str] = None,
             log_parsing: Optional[bool] = False,
             log_parsing_window: Optional[int] = 7)
```

Initializes the BigQuery integration.

**Arguments**:

- `source` - The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
- `version` - The Grai data version to associate with output from the integration
- `namespace` - The Grai namespace to associate with output from the integration
- `project` - GCP project id
- `dataset` - BigQuery Dataset Id, or multiple datasets seperated by a comma (`,`)
- `credentials` - JSON credentials for service account
- `log_parsing` - The number of days to read logs

### nodes

```python
@cache
def nodes() -> List[SourcedNode]
```

Return nodes from the connector.

### edges

```python
@cache
def edges() -> List[SourcedEdge]
```

Return edges from the connector.

### get\_nodes\_and\_edges

```python
def get_nodes_and_edges() -> Tuple[List[SourcedNode], List[SourcedEdge]]
```

Return nodes and edges from the connector.

### ready

```python
def ready() -> bool
```

Check if the connector is ready to be used.
