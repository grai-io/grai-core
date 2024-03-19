---
title: BigQuery GitHub Action
description: Documentation for Grai's BigQuery GitHub Action GitHub action.
---

# BigQuery

The BigQuery action depends on Google's python BigQuery library.
More information can be found about specific connection credentials in Google's documentation [here](https://cloud.google.com/python/docs/reference/bigquery/latest).


### Fields



| Field | Required | Default | Description |
|-----|-----|-----|-----|
| project | yes |  | The BigQuery project string |
| dataset | yes |  | The BigQuery dataset string |
| credentials | yes |  | A JSON credential string for use with google oauth service account [connections](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials) |




### Example



```yaml copy
on:
  - pull_request
name: BigQuery
jobs:
  test_bigquery:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Run Grai Action
        uses: grai-io/grai-actions/bigquery@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          source-name: prod-db
          grai-api-url: https://api.grai.io
          project: my-bigquery-project
          dataset: my-bigquery-dataset
          credentials: '{ "type": "service_account", "project_id": "demo", "private_key_id":
            "your_private_key_id", "private_key": "your_private_key", "client_email":
            "your@email.iam.gserviceaccount.com", "client_id": "your_client_id", "auth_uri":
            "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/you%40email.iam.gserviceaccount.com"
            }'

```
