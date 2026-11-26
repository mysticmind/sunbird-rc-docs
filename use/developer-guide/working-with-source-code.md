---
title: "Working with Source Code"
---

# Working with Source Code

Use the `sunbird-rc-core` project — the `java` folder contains all the registry modules plus the claims service.

## Is this the right page for you?

This page is for building and running the **Registry** from source, for example to contribute code or to debug locally. Sunbird RC has two components, Registry and Credentials, which can be used on their own or together. Pick the path that matches what you need:

| You want to…                                      | Start here                                                                                                                                                      |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Try Sunbird RC quickly, without building anything | [Docker Compose Setup](/use/getting-started/installation/docker-compose-setup)                                                         |
| Deploy to a cluster                               | [Helm Setup](/use/getting-started/installation/helm-setup)                                                                             |
| Run only the Credentials services                 | [Credentialling Services setup (Dev / Docker / Helm)](/use/getting-started/installation/credentialling-services-setup-dev-docker-helm) |
| Build and run the Registry from source            | This page                                                                                                                                                       |
| Use Registry and Credentials together from source | This page, then enable **Credentials (Signature V2)** under [Feature services](#feature-services)                                                               |

::: info
**Already running Sunbird RC?** Read the release notes for the version you're moving to before rebuilding — [Credentials v2.1.0](/use/releases/credentialing/v2.1.0-latest-release) and [Registry v2.0.3](/use/releases/registry/v2.0.3). If your registry signs with the legacy signer, see **Signature V1 or V2** below before changing any signature settings.
:::

::: info
**Java version**: JDK 11
:::

::::: steps
::: step
### Compile the registry

```bash
$ sh configure-dependencies.sh
$ cd java
$ ./mvnw clean install -DskipTests
$ cd ..
```

This produces a JAR in `java/registry/target`.
:::

::: step
### Configure schemas

Create a `_schemas/` folder at `java/registry/src/main/resources/public/` and place your schema files there. A sample student-teacher schema set is available in the [registry-cli templates](https://github.com/Sunbird-RC/registry-cli/tree/main/src/templates/config/schemas). See [Creating Your Own Schemas](/use/developer-guide/schema-setup/creating-your-own-schemas) to write your own.
:::

::: step
### Install dependencies and run

1. `cd java`
2. `./mvnw clean install`
3. Set up the database and any feature-dependent services (see **Feature services** below)
4. Set the minimum required env vars: `connectionInfo_uri`, `connectionInfo_username`, `connectionInfo_password`, `authentication_enabled` — variables starting with `connectionInfo_` configure the database (see [Environment Variable Reference](/use/developer-guide/environment-variable-reference)); check `docker-compose.yml`'s `registry` service for examples.
5. `cd` to the `registry` package, export the env vars, run `../mvnw spring-boot:run`
:::

::: step
### Start the dependent services

```bash
$ curl https://raw.githubusercontent.com/Sunbird-RC/registry-cli/main/src/templates/docker-compose.yml > docker-compose.yml
$ curl https://raw.githubusercontent.com/Sunbird-RC/registry-cli/main/src/templates/config/keycloak/realm-export.json > imports/realm-export.json
$ docker-compose up kc db es cs
```

This starts Keycloak (`kc`), Postgres (`db`), ElasticSearch (`es`), and the Claims Service (`cs`).
:::

:::: step
### Configure the Keycloak secret

1. Go to `http://localhost:8080/auth/admin/master/console/#/realms`
2. Log in as `admin` / `admin`
3. Click **Sunbird RC** → **Clients** → **admin-api** → **Credentials** tab
4. Copy the secret

Then set the frontend URL in Keycloak to whatever URL you use to generate tokens (e.g. `http://localhost:8080/auth`): log in to the Keycloak UI, select realm `sunbird-rc`, and set it under General settings → frontend URL.

::: warning
Update the frontend URL whenever the deploy DNS changes.
:::
::::

::: step
### Run the registry

```bash
$ java -jar java/registry/target/registry.jar
```
:::
:::::

## Feature services

Most can run via the project's `docker-compose.yml` for local dev. Enable or disable each with its own flag:

| Service                      | Flag                                                                      | Notes                                                                                                                                                                                                                                                                               |
| ---------------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Encryption Service           | `encryption_enabled=true`                                                 | —                                                                                                                                                                                                                                                                                   |
| ID Gen Service               | `idgen_enabled=true`                                                      | —                                                                                                                                                                                                                                                                                   |
| Credentials (Signature V2)   | `signature_enabled=true`, `did_enabled=true`, `certificate_enabled=true`  | Also set `signature_provider=dev.sunbirdrc.registry.service.impl.SignatureV2ServiceImpl`; the other `signature_v2_*`/`did_*` envs default correctly in `docker-compose.yml`. `certificate_enabled` is what generates PDFs. Use this when running Registry and Credentials together. |
| Legacy signer (Signature V1) | `signature_enabled=true`                                                  | Uses `signature_provider=dev.sunbirdrc.registry.service.impl.SignatureV1ServiceImpl`, which is the registry's default. Configure with `sign_url`, `verify_url`, `keys_url` and `sign_health_check_url`.                                                                             |
| Keycloak Service             | `authentication_enabled=true`                                             | Plus `enableLogin` in the schema; check envs starting with `sunbird_sso_`, `sunbird_keycloak`, `oauth2_resource_`                                                                                                                                                                   |
| ElasticSearch Service        | `search_providerName=dev.sunbirdrc.registry.service.ElasticSearchService` | Supports v6; configure with `elastic_search_*` envs                                                                                                                                                                                                                                 |
| Claims Service               | `claims_enabled=true`                                                     | —                                                                                                                                                                                                                                                                                   |
| File Storage Service         | `filestorage_enabled=true`                                                | Configure with `filestorage_*` envs; backed by Minio (S3-compatible cloud storage or a local Minio instance)                                                                                                                                                                        |
| Kafka & Zookeeper            | —                                                                         | Needed for `async_enabled`, `event_enabled`, or `notification_enabled`/`notification_async_enabled`                                                                                                                                                                                 |
| Metrics Service              | `event_enabled=true`                                                      | Configure with `event_*` envs                                                                                                                                                                                                                                                       |
| Notification Service         | `notification_enabled=true`                                               | Configure with `notification_*` envs                                                                                                                                                                                                                                                |
| Redis Service                | `manager_type=DistributedDefinitionsManager`                              | Configure with `redis_*` envs                                                                                                                                                                                                                                                       |

## Signature V1 or V2

The registry can sign credentials in two ways:

* **Signature V1 (legacy signer)** — the registry's built-in default. Use this if you run the Registry on its own with an existing V1 signer.
* **Signature V2 (Credentials)** — the registry hands signing and DIDs to the Credentials services. The project's `docker-compose.yml` defaults to V2, and `enable-v2.sh` switches an existing setup over.

::: warning
**Existing adopters:** switching from V1 to V2 changes how new credentials are signed and which DIDs they use. Check the impact on credentials you have already issued before switching.
:::

::: danger
**Troubleshooting — Prisma migration issue.** Happens when Prisma migration tables aren't set and the database isn't empty.

* If you can wipe the database, do so and set up the identity service first.
* In production (or wherever cleanup isn't possible), [baseline the database](https://www.prisma.io/docs/orm/prisma-migrate/workflows/baselining) and restart the identity, credential-schema, and credential services.
:::

