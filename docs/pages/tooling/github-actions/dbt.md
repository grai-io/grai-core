---
title: dbt
description: Documentation for Grai's dbt GitHub action.
---

# dbt

The dbt action reads a manifest.json file inside of your github project to perform tests and update your grai instance.
Because of this, it's critical your manifest.json file is up to date on each pull request. 
One way to do this is to perform `dbt build` as part of your CI action but there are multiple ways to generate an up-to-date manifest file.

* More information about manifest.json files can be found [here](https://docs.getdbt.com/reference/artifacts/manifest-json).
* Make sure to include an `- uses: actions/checkout@v3` step in your workflow so that your repo code is available.



### Fields



| Field | Required | Default | Description |
|-----|-----|-----|-----|
| manifest-file | yes |  | The file location in your repository of the updated manifest.json file |




### Example



```yaml copy
'on':
- push
name: dbt
jobs:
  test_dbt:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    - name: Run Grai Action
      uses: grai-io/grai-actions/dbt@master
      with:
        namespace: my_apps_grai_namespace
        api-key: my_grai_api_key
        action: tests
        grai-api-url: https://api.grai.io
        manifest-file: ./tests/dbt/manifest.json

```



