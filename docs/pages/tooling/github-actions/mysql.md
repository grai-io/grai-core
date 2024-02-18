---
title: MySQL GitHub Action
description: Documentation for Grai's MySQL GitHub Action GitHub action.
---

# MySQL

The MySQL action depends on the python mysql library.
You can find complete documentation about the library [here](https://dev.mysql.com/doc/connector-python).


### Fields



| Field | Required | Default | Description |
|-----|-----|-----|-----|
| db-host | yes |  | The database host |
| db-port | no | 3306 | The database port |
| db-database-name | yes |  | The database name |
| db-user | yes |  | The database user |
| db-password | yes |  | The database password |




### Example



```yaml copy
on:
  - pull_request
name: MySQL
jobs:
  test_mysql:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/mysql@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          source-name: prod-db
          grai-api-url: https://api.grai.io
          db-host: dev.mysql.com
          db-port: '3306'
          db-database-name: my_db
          db-user: my_user
          db-password: my_password

```
