# Contributing to Grai

Below you'll find a set of guidelines for how to contribute to Grai.

# Opening issues

Before you submit an issue, please check all existing open and closed issues to see if your issue has previously been resolved or is already known. 
If there is already an issue logged, feel free to upvote it by adding a 👍 reaction. 
If you would like to submit a new issue, please fill out our Issue Template to the best of your ability so we can accurately understand your report.

# Security issues & vulnerabilities

If you come across an issue related to security, or a potential attack vector within Grai or one of its dependencies, please DO NOT create a publicly viewable issue. 
Instead, please contact us directly at hello@grai.io. 
We will do everything we can to respond to the issue as soon as possible.

If you find a vulnerability within the core Grai repository, and we determine that it is remediable and of significant nature, we will be happy to pay you a reward for your findings and diligence. 
Contact us to find out more.

# Documentation edits

Grai'sdocumentation can be found directly within its codebase and you can feel free to make changes / improvements to any of it through opening a PR. 
We utilize these files directly in our website and will periodically deploy documentation updates as necessary.

# Building additional features

If you're an incredibly awesome person and want to help us make Grai even better through new features or additions, we would be thrilled to work with you.


## Before Starting

To help us work on new features, you can create a new feature request post in GitHub Discussion or discuss it in our Slack. 
New functionality often has large implications across the entire Grai repo, so it is best to discuss the architecture and approach before starting work on a pull request.

## Code

## Monorepo Structure

Please insure contributions are submitted in appropriate locations in the monorepo.
For example, new integrations ought to be added to `grai-integrations`.
If you have any questions about where you should introduce your change please chat with us on Slack or email us at hello@grai.io

## Commits

We use Conventional Commits for our commit messages. Please follow this format when creating commits. Here are some examples:

    feat: adds new feature
    fix: fixes bug
    docs: adds documentation
    chore: does chore

Here's a breakdown of the format. At the top-level, we use the following types to categorize our commits:

    feat: new feature that adds functionality. These are automatically added to the changelog when creating new releases.
    fix: a fix to an existing feature. These are automatically added to the changelog when creating new releases.
    docs: changes to docs only. These do not appear in the changelog.
    chore: changes to code that is neither a fix nor a feature (e.g. refactoring, adding tests, etc.). These do not appear in the changelog.

If you are committing to templates or examples, use the chore type with the proper scope, like this:

    chore(templates): adds feature to template
    chore(examples): fixes bug in example

## Pull Requests

For all Pull Requests, you should be extremely descriptive about both your problem and proposed solution. If there are any affected open or closed issues, please leave the issue number in your PR message.

# Contributor Guidelines

Contributors to Grai are deemed to have acceppted

    [GitHub's Acceptable Use Policy](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies)
    [GitHub's Community Guidelines](https://docs.github.com/en/site-policy/github-terms/github-community-guidelines)
    [The Developer Certificate of Origin](https://developercertificate.org/)
 
