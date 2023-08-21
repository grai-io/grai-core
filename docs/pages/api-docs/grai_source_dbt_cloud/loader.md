---
sidebar_label: loader
title: grai_source_dbt_cloud.loader
---

## Event Objects

```python
class Event()
```



## DbtCloudConnector Objects

```python
class DbtCloudConnector()
```



### default\_account

```python
@cached_property
def default_account() -> dict
```



### get\_nodes\_and\_edges

```python
def get_nodes_and_edges()
```



### get\_events

```python
def get_events(last_event_date) -> List[Event]
```

**Arguments**:

  last_event_date:


**Returns**:



### get\_run\_nodes

```python
def get_run_nodes(account_id: str, run_id: str) -> List[str]
```

**Arguments**:

  account_id (str):
  run_id (str):


**Returns**:



### get\_runs

```python
def get_runs(account_id: str, last_event_date)
```

**Arguments**:

  account_id (str):
  last_event_date:


**Returns**:
