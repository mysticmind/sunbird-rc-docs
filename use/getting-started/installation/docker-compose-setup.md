---
title: "Docker Compose Setup"
---

# Docker Compose Setup

::: info
**System requirements**: 4 cores · 8 GB RAM · 100 GB disk minimum — same as the Registry CLI path.
:::

::::: steps
::: step
### Get the compose file and environment template

Download the latest [docker-compose.yml](https://github.com/Sunbird-RC/sunbird-rc-core/blob/main/docker-compose.yml) and modify values as needed. Then download or create a `.env` file from the [`.env.example`](https://github.com/Sunbird-RC/sunbird-rc-core/blob/main/.env.example) template.
:::

::: step
### Set the required environment variables

| ENV               | Value     | Description                                                                                     |
| ----------------- | --------- | ----------------------------------------------------------------------------------------------- |
| `RELEASE_VERSION` | `v2.1.0`  | Use the latest [release](https://github.com/Sunbird-RC/sunbird-rc-core/releases) of Sunbird RC. |
| `SCHEMA_DIR`      | `schemas` | Relative path to the directory where schemas are created.                                       |
|
:::
     |           |                                                                                                 |

:::: step
### Add schemas and imports

Create the schema files in the `schemas` directory. Then create an `imports` directory and download the Keycloak realm file and the sample signing key file into it.

::: warning
The sample signing keys are for local use only — replace them before going to production.
:::
::::

::: step
### Set up Keycloak

```bash
docker-compose up -d db
docker-compose up -d keycloak
```

Open the Keycloak admin console at `http://localhost:8080/auth/`, go to **Clients** → `admin-api` → **Credentials** → **Regenerate Secret**, copy the value, and set `KEYCLOAK_SECRET` in `.env` with it.
:::

::: step
### Start everything and verify

```bash
docker-compose up -d
docker-compose ps
```

The registry swagger JSON is then available at `http://localhost:8081/api/docs/swagger.json`.
:::
:::::

