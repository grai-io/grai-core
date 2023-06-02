---
title: PostgreSQL
description: Documentation for Grai's PostgreSQL GitHub action.
---

# Postgres

The Postgres action depends on the python psycopg2 library.
You can find complete documentation about the library [here](https://www.psycopg.org/docs/).


### Fields



| Field | Required | Default | Description |
|-----|-----|-----|-----|
| db-host | yes |  | The database host |
| db-port | no | 5432 | The database port |
| db-database-name | yes |  | The database name |
| db-user | yes |  | The database user |
| db-password | yes |  | The database password |




### Example



```yaml copy
'on':
- push
name: PostgreSQL
jobs:
  test_postgres:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    - name: Run Grai Action
      uses: grai-core/grai-actions/postgres
      with:
        namespace: my_apps_grai_namespace
        api-key: my_grai_api_key
        db-host: prod.db.com
        db-port: '5432'
        db-database-name: my_database
        db-user: my_user
        db-password: my_password

```
