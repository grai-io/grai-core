---
title: Grai Actions
description: Documentation for Grai's GitHub actions.
---

# Grai Actions

## Shared Fields

All actions share some common fields listed below.

### Authentication

| Field         | Required | Default | Description              |
| ------------- | -------- | ------- | ------------------------ |
| api-key       | no       |         | Your Grai API key.       |
| grai-user     | no       |         | Your Grai username.      |
| grai-password | no       |         | Your Grai password.      |
| workspace     | no       |         | Your Grai workspace name |

You must provider either `api-key` or `grai-user` **and** `grai-password`.
If you're account is associated with multiple workspaces and you're using username/password authentication you must
also provide your desired `workspace`.

### Other Parameters

| Field        | Required | Default               | Description                                                                                                 |
| ------------ | -------- | --------------------- | ----------------------------------------------------------------------------------------------------------- |
| namespace    | yes      |                       | The Grai namespace for the connection                                                                       |
| grai-api-url | no       | `https://api.grai.io` | "The url of your grai instance. This is constructed as {scheme}://{host}:{port} where the port is optional" |
| grai-app-url | no       | `https://app.grai.io` | The URL for your frontend instance of Grai. This might include a port depending on your configuration       |
| action       | no       | tests                 | Which action to perform. Can be `tests` or `update`                                                         |
| github-token | no       | `${{github.token}}`   | The GITHUB_TOKEN secret for your repository                                                                 |

## Notes and Caveats

### Github Authentication

By default we use a `github-token` provided by your repository to write comments back to your PR with test results.
In some cases, such as when the pull request is coming from a forked repository, the default token will not have write
permissions.
If this is the case, you'll receive an error message in the workflow indicating such.
There are a few ways you can resolve the issue but you should first check your repository action settings under
`Settings -> Actions -> General` aren't blocking workflows from running.

Some alternatives include.

#### Explicit Workflow Permissions

GitHub has provided helpful [documentation](https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs)
to provide explicit permissions for your workflows.
Make sure the Grai Action has, at minimum, write permissions for `pull-request` and `issues`.
You can set this at the job level by adding a `permission` key in your workflow. e.g.

```yaml copy
jobs:
  my-grai-action:
    runs-on: ubuntu-latest

    permissions:
      issues: write
      pull-requests: write
```

#### Personal Access Tokens

You can also use personal access tokens or [PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)'s
in place of the default github-token.
You'll need to create a token following the linked instructions but make sure to store it in your repository secrets
`Settings -> Secrets and variables -> Actions -> New Repository Secret`.
If you were to create a secret called `MY_PAT` you would pass it into your grai action job as

```yaml copy
jobs:
  my-grai-action:
    runs-on: ubuntu-latest

  steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Run Grai Action
      uses: grai-io/grai-actions/redshift@master
      with:
        github-token: ${{ secrets.MY_PAT }}
```
