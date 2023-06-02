---
title: Redshift
description: Documentation for Grai's Redshift GitHub action.
---

# Redshift

The Redshift action depends on Amazon's python connector library.
You can find complete documentation about the library in the AWS docs [here](https://github.com/aws/amazon-redshift-python-driver).


### Fields



| Field | Required | Default | Description |
|-----|-----|-----|-----|
| db-host | yes |  | The database host |
| db-port | no | 5439 | The database port |
| db-database-name | yes |  | The database name |
| db-user | yes |  | The database user |
| db-password | yes |  | The database password |




### Example



```yaml copy
'on':
- push
name: Redshift
jobs:
  test_redshift:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    - name: Run Grai Action
      uses: grai-core/grai-actions/redshift
      with:
        namespace: my_apps_grai_namespace
        api-key: my_grai_api_key
        db-host: redshift-cluster-1.abc123xyz789.us-east-1.redshift.amazonaws.com
        db-port: '5439'
        db-database-name: dev
        db-user: admin
        db-password: password

```
