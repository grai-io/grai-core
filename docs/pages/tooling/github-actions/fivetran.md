---
title: Fivetran GitHub Action
description: Documentation for Grai's Fivetran GitHub Action GitHub action.
---

# Fivetran

The Fivetran Action relies upon access to Fivetran's API endpoint. 
This endpoint is configurable if you have a non-standard implementation but should generally be left alone.

Authentication with their services will require an API key and secret but you can find more documentation about generating these values [here](https://fivetran.com/docs/rest-api/getting-started#instructions).

### Fields



| Field | Required | Default | Description |
|-----|-----|-----|-----|
| fivetran-endpoint | no | https://api.fivetran.com/v1 | Fivetran API endpoint |
| fivetran-api-key | yes |  | Your Fivetran user api key |
| fivetran-api-secret | yes |  | Your Fivetran user api secret |
| namespace-map | no |  | A JSON string containing a mapping between Fivetran connections and Grai namespaces |




The `namespace` field in the Fivetran Action works slightly differently than other action.
It is used as a default namespace for all connections not specified in the `namespace_map`. 
You can find more information about that below.


#### Namespace Map

Each Fivetran connection has a connector id and synchronizes from a source to a sync. 
For example, a sync from your production database to data warehouse would have an associated connector id.

Because the Fivetran Action synchronizes from all of your Fivetran connections it uses the `namespace_map` value to know which connectors belong to which Grai namespaces.
The namespace map should be a JSON string with the Grai namespace for each source and destination of each connector id e.g.

```json
{
    "<connector_id>": {
        "source": "<source_namespace>",
        "destination", "<destination_namespace>"
    }
}
```


You can find connector id's for all of your Fivetran connections in the [API](https://fivetran.com/docs/rest-api/faq/find-connector_id)

### Example



```yaml copy
on:
  - pull_request
name: Fivetran
jobs:
  test_fivetran:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/fivetran@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          fivetran-api-key: hHqP5c2nIY0B6fpa
          fivetran-api-secret: 1234567890abcdef1234567890abcdef
          namespace-map: '{"operative_combination": {"source": "source_namespace",
            "destination": "destination_namespace"}}'

```



