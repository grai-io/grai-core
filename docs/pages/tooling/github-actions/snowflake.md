---
title: Snowflake
description: Documentation for Grai's Snowflake GitHub action.
---

# Snowflake

The Snowflake action depends on Snowflake's python connector library. 
You can find complete documentation about the library in the Snowflake docs [here](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector) with more detail about the connector [here](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api).


### Fields



| Field | Required | Default | Description |
|-----|-----|-----|-----|
| db-user | yes |  | The database user |
| db-password | yes |  | The database password |
| account | yes |  | Associated Snowflake account |
| warehouse | yes |  | Associated Snowflake warehouse |
| role | no |  | Optional Snowflake role |
| database | no |  | Optional Snowflake database |
| schema | no |  | Optional snowflake schema |




### Example



```yaml copy
'on':
- pull_request
name: Snowflake
jobs:
  test_snowflake:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    - name: Run Grai Action
      uses: grai-io/grai-actions/snowflake@master
      with:
        namespace: my_apps_grai_namespace
        api-key: my_grai_api_key
        action: tests
        grai-api-url: https://api.grai.io
        db-user: my-user
        db-password: my-password
        account: my-account
        warehouse: my-warehouse

```



