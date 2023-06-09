---
title: Grai Actions
description: Documentation for Grai's GitHub actions.
---

# Grai Actions


## Shared Fields

All actions share some common fields listed below.


### Authentication

| Field              | Required | Default             | Description              |
|--------------------|----------|---------------------|--------------------------|
| api-key            | no       |                     | Your Grai API key.       |
| grai-user          | no       |                     | Your Grai username.      |
| grai-password      | no       |                     | Your Grai password.      |
| workspace          | no       |                     | Your Grai workspace name |

You must provider either `api-key` or `grai-user` **and** `grai-password`.
If you're account is associated with multiple workspaces and you're using username/password authentication you must 
also provide your desired `workspace`.


### Other Parameters

| Field          | Required | Default             | Description                                                                                                 |
|----------------|----------|---------------------|-------------------------------------------------------------------------------------------------------------|
| namespace      | yes      |                     | The Grai namespace for the connection                                                                       |
| grai-api-url   | no       | https://api.grai.io | "The url of your grai instance. This is constructed as {scheme}://{host}:{port} where the port is optional" |
| grai-app-url   | no       | https://app.grai.io | The URL for your frontend instance of Grai. This might include a port depending on your configuration       |
| action         | no       | tests               | Which action to perform. Can be `tests` or `update`                                                         |
| github-token   | no       | `${{github.token}}` | The GITHUB_TOKEN secret for your repository                                                                 |


