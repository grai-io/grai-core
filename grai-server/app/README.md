# Grai Server (aka The Guide)

> There is a theory which states that if ever anyone discovers exactly what the Universe is for and why it is here, it will instantly disappear and be replaced by something even more bizarre and inexplicable. There is another theory which states that this has already happened.
> - Douglas Adams, The Hitchhiker's Guide To the Galaxy


The guide is the core server library exposed as part of Grai.

# Introduction

Grai consists of multiple different independent services including

### Server

- Postgres + Django
- Redis
- Celery + Celery Beat
- flower

For more information about the server see [Grai Server](/core/server/).

### Web App

For more information about the web app see [Grai Web App](/core/web-app/)

### Container Registry

We maintain up to date docker images for all of the Grai services on GitHub's Container Registry `ghcr`

| Service | Image                                   | Tags           |
| ------- | --------------------------------------- | -------------- |
| Server  | ghcr.io/grai-io/grai-core/grai-server   | latest, semver |
| Web App | ghcr.io/grai-io/grai-core/grai-frontend | latest, semver |
