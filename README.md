<div align="center">
  <img src="docs/assets/Grai-Logo-Horizontal-2.png" width="375px"><br>
</div>

<p align="center">
  <a href="https://join.slack.com/t/graicommunity/shared_invite/zt-1il70kfeb-TaCm5fwHg_quWCpKNYyj6w">
    <img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white" height=22/>
  </a>
   <a href="https://github.com/grai-io/grai-core">
    <img src="https://img.shields.io/github/issues/grai-io/grai-core?style=flat-square" height=22/>
  </a>
  </a>
   <a href="https://github.com/grai-io/grai-core">
    <img src="https://img.shields.io/github/languages/top/grai-io/grai-core?style=flat-square" height=22/>
  </a>
  </a>
   <a href="https://github.com/grai-io/grai-core">
    <img src="https://img.shields.io/pypi/pyversions/grai-graph?style=for-the-badge" height=22/>
  </a>
  <a href=https://www.ycombinator.com/launches/H8h-grai-open-source-version-control-for-metadata target='_blank'>
    <img alt=Launch YC: ✨ Grai - Open-source   version control for metadata src=https://www.ycombinator.com/launches/H8h-grai-open-source-version-control-for-metadata/upvote_embed.svg height=22/>
   </a>
</p>

## Introduction

**Data lineage made simple.**
Grai makes it easy to understand how your data relates together across databases, warehouses, APIs and dashboards.


* **Pre-built connectors.** Automatically synchronize lineage from across the stack so your metadata is never out of date.
* **Centralized data tests.** Write data validation tests which run whenever upstream data sources change (coming soon).
* **Integrated with git.** Run data validation tasks as part of your CI/CD process to test changes everywhere you data is used. No coordination meetings required.
* **Your data, your cloud.** Grai is fully open sourced and self hosted. You maintain full control over your data and hosting environment.


## Quick Start

```
git clone https://github.com/grai-io/grai-core
cd grai-core/grai-server
docker compose up
```

The server should now be available at [http://localhost:8000/admin](http://localhost:8000/admin).

Default login credentials:

```
username: null@grai.io
password: super_secret
```

You can also explore the API backend at [http://localhost:8000/docs](http://localhost:8000/docs).

Check out this [guide](https://github.com/grai-io/grai-core/tree/master/examples/quick_start_postgres) for a walk through populating lineage using the postgres connector.

## Docker Image

Although you'll need to provide your own postgres container you can also get started with a basic image of Grai is
avaialable at `ghcr.io/grai-io/grai-core/grai-server`.



## Other Features

#### CLI Library

Programmatically interact with your data lineage from the command line using the grai-cli.

```
pip install grai-cli
```

#### Client Library

Provides programmatic access to the data lineage server.

```
pip install grai-client
```

#### Python Library

Dynamically interact with the data lineage graph for your organization.

```
pip install grai-graph
```


#### Connectors

Postgres:

```
pip install grai-source-postgres
```

DBT (coming soon):

```
pip install grai-source-dbt
```

## Community

Come and join our [Slack](https://join.slack.com/t/graicommunity/shared_invite/zt-1il70kfeb-TaCm5fwHg_quWCpKNYyj6w)! We're on hand for support, help or just to hang out and chat.

To stay looped into updates, join our [email list](https://www.grai.io/signup/).
