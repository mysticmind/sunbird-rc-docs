---
title: "Environment Variable Reference"
---

# Environment Variable Reference

The Registry exposes its behavior almost entirely through environment variables. This is the full property reference — kept separate from the [Configuration Reference](/registry/configure/configuration-files), which covers the frontend/proxy/audit/notification/view-template config *files* rather than registry-core env vars.

::: warning
The **Certificate Api service** and **Certificate signer service** sections below still document `certificate-api` and `certificate-signer` by name. These services no longer exist in the current `services/` directory — certificate generation has moved into the core registry. Treat those env vars as historical until confirmed against the current signing/certificate implementation.
:::

## Registry

| Property                                                                                                                                 | Description                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `notification_enabled`                                                                                                                   | boolean — whether notifications are sent                                                                                      |
| `notification_url`                                                                                                                       | URL used to send notifications                                                                                                |
| `notification_async_enabled`                                                                                                             | send notifications asynchronously                                                                                             |
| `notification_topic`                                                                                                                     | if async, the Kafka topic notification events are sent to                                                                     |
| `registry_perRequest_indexCreation_enabled`                                                                                              | boolean — whether an index needs to be created at the database level                                                          |
| `external_entities`                                                                                                                      | comma-separated list of external entities                                                                                     |
| `workflow.enable`                                                                                                                        | boolean — enable/disable the workflow (attestation policy)                                                                    |
| `async_enabled`                                                                                                                          | create entities asynchronously                                                                                                |
| `kafka_create_entity_topic`                                                                                                              | if async, the topic new async create requests are pushed to                                                                   |
| `kafka_post_create_entity_topic`                                                                                                         | if async, the topic the create-entity response is pushed to                                                                   |
| `search_offset`                                                                                                                          | default search offset                                                                                                         |
| `search_limit`                                                                                                                           | default/max search result limit                                                                                               |
| `search_expandInternal`                                                                                                                  | boolean — expand search results to include internal objects                                                                   |
| `database_provider`                                                                                                                      | which database to use — `NEO4J`, `SQLG`, `CASSANDRA`, `ORIENTDB`, or `TINKERGRAPH` (in-memory)                                |
| `connectionInfo_uri`                                                                                                                     | DB connection URL, e.g. `jdbc:postgresql://localhost:5432/yourdb`                                                             |
| `connectionInfo_username`                                                                                                                | DB username                                                                                                                   |
| `connectionInfo_password`                                                                                                                | DB password                                                                                                                   |
| `connectionInfo_maxPoolSize`                                                                                                             | DB connection pool size                                                                                                       |
| `verify_url`                                                                                                                             | URL to verify an issued VC — point at `{certificate_signer}/verify`                                                           |
| `certificate_health_check_url`                                                                                                           | certificate API service health-check URL                                                                                      |
| `audit_enabled`                                                                                                                          | enable audit logging                                                                                                          |
| `audit_frame_store`                                                                                                                      | `FILE` (store logs in files) or `DATABASE` (store in the primary DB, and ElasticSearch if enabled)                            |
| `audit_suffix`                                                                                                                           | suffix appended to the schema name to store audit info per entity type                                                        |
| `audit_suffixSeparator`                                                                                                                  | separator between entity name and `audit_suffix`                                                                              |
| `validation_enabled`                                                                                                                     | boolean — validate request body against a specific format                                                                     |
| `validation_type`                                                                                                                        | format to validate against, e.g. `JSON`                                                                                       |
| `service_connection_timeout`                                                                                                             | connection timeout (ms) for the underlying request config                                                                     |
| `service_connection_request_timeout`                                                                                                     | timeout (ms) when requesting a connection from the connection manager                                                         |
| `service_read_timeout`                                                                                                                   | socket read timeout (ms)                                                                                                      |
| `http_max_connections`                                                                                                                   | max HTTP connections                                                                                                          |
| `taskExecutor_index_threadPoolName`                                                                                                      | thread name prefix for the index task executor                                                                                |
| `taskExecutor_index_corePoolSize`                                                                                                        | core pool size                                                                                                                |
| `taskExecutor_index_maxPoolSize`                                                                                                         | max pool size                                                                                                                 |
| `taskExecutor_index_queueCapacity`                                                                                                       | `BlockingQueue` capacity                                                                                                      |
| `auditTaskExecutor_threadPoolName`                                                                                                       | thread name prefix for the audit task executor                                                                                |
| `auditTaskExecutor_corePoolSize`                                                                                                         | core pool size                                                                                                                |
| `auditTaskExecutor_maxPoolSize`                                                                                                          | max pool size                                                                                                                 |
| `auditTaskExecutor_queueCapacity`                                                                                                        | `BlockingQueue` capacity                                                                                                      |
| `elastic_search_connection_url`                                                                                                          | ElasticSearch connection URL (used when `search_providerName` enables it)                                                     |
| `search_providerName`                                                                                                                    | `NativeSearchService` (writes DB doubles as search) or `ElasticSearchService` (default if unset is Native)                    |
| `sunbird_sso_realm`                                                                                                                      | identity-provider realm name                                                                                                  |
| `sunbird_sso_url`                                                                                                                        | identity-provider connection URL                                                                                              |
| `sunbird_sso_admin_client_id`                                                                                                            | admin client ID                                                                                                               |
| `sunbird_sso_admin_client_secret`                                                                                                        | secret for the above admin client                                                                                             |
| `sunbird_keycloak_user_set_password`                                                                                                     | boolean — set a default password for new entity owners                                                                        |
| `sunbird_keycloak_user_password`                                                                                                         | the default password, if the above is true                                                                                    |
| `identity_user_actions`                                                                                                                  | identity-provider actions to trigger, e.g. `VERIFY_EMAIL`, `UPDATE_PROFILE`, `UPDATE_PASSWORD`, `TERMS_AND_CONDITIONS`        |
| `identity_provider`                                                                                                                      | implementation class — `dev.sunbirdrc.auth.genericiam.AuthProviderImpl` or `dev.sunbirdrc.auth.keycloak.KeycloakProviderImpl` |
| `oauth2_resource_uri`                                                                                                                    | identity-provider resource URL, e.g. `http://keycloak:8080/auth/realms/sunbird-rc`                                            |
| `oauth2_resource_email_path`                                                                                                             | JWT path to email, e.g. `email`                                                                                               |
| `oauth2_resource_consent_path`                                                                                                           | JWT path to consent, e.g. `consent`                                                                                           |
| `oauth2_resource_roles_path`                                                                                                             | JWT path to roles, e.g. `realm_access.roles`                                                                                  |
| `oauth2_resource_entity_path`                                                                                                            | JWT path to entity, e.g. `entity`                                                                                             |
| `oauth2_resource_user_id_path`                                                                                                           | JWT path to user id, e.g. `sub`                                                                                               |
| `claims_enabled`                                                                                                                         | default `false` — whether attestation is enabled                                                                              |
| `claims_url`                                                                                                                             | claims service URL                                                                                                            |
| `did_enabled`                                                                                                                            | enable the DID service (required for signature v2)                                                                            |
| `did_health_check_url` / `did_generate_url` / `did_resolve_url`                                                                          | DID service endpoints                                                                                                         |
| `signature_enabled`                                                                                                                      | whether documents get signed                                                                                                  |
| `signature_provider`                                                                                                                     | `dev.sunbirdrc.registry.service.impl.SignatureV1ServiceImpl` or `...SignatureV2ServiceImpl`                                   |
| `signature_v2_credential_did_method`                                                                                                     | DID method for the credential's id                                                                                            |
| `signature_v2_issuer_did_method`                                                                                                         | DID method for the issuer DID                                                                                                 |
| `signature_v2_schema_author`                                                                                                             | credential schema author name                                                                                                 |
| `signature_v2_schema_author_did_method`                                                                                                  | DID method for the schema author                                                                                              |
| `signature_v2_health_check_url` / `_issue_url` / `_get_url` / `_delete_url` / `_verify_url` / `_verify_any_url` / `_revocation_list_url` | SignatureV2 service endpoints                                                                                                 |
| `signature_v2_schema_health_check_url` / `_create_url` / `_update_url` / `_get_by_id_and_version_url` / `_search_by_tags_url`            | SignatureV2 credential-schema endpoints                                                                                       |
| `sign_url` / `sign_health_check_url`                                                                                                     | certificate signer endpoints                                                                                                  |
| `certificate_enabled`                                                                                                                    | default `false` — whether certificates are generated                                                                          |
| `pdf_url`                                                                                                                                | URL to fetch the certificate from the certificate API service                                                                 |
| `template_base_url`                                                                                                                      | endpoint for default templates stored in Sunbird RC                                                                           |
| `filestorage_enabled`                                                                                                                    | default `false` — whether documents are stored                                                                                |
| `filestorage_connection_url` / `_access_key` / `_secret_key` / `_bucket_key`                                                             | Minio connection details                                                                                                      |
| `registry_base_apis_enable`                                                                                                              | enables the legacy `/add` `/update` APIs for backward compatibility                                                           |
| `logging.level.root`                                                                                                                     | log level — `INFO` (default), `DEBUG`, `WARN`, `ERROR`                                                                        |
| `enable_external_templates`                                                                                                              | boolean — allow certificate PDFs via external templates                                                                       |
| `authentication_enabled`                                                                                                                 | enable authentication system-wide                                                                                             |
| `kafka_bootstrap_address`                                                                                                                | Kafka connection URL                                                                                                          |
| `webhook_enabled`                                                                                                                        | enable webhooks (requires `async_enabled`)                                                                                    |
| `webhook_url`                                                                                                                            | URL the caller can retrieve created-entity info from once generated                                                           |
| `redis_host` / `redis_port`                                                                                                              | Redis connection                                                                                                              |
| `manager_type`                                                                                                                           | `DefinitionsManager` (single instance) or `DistributedDefinitionsManager`                                                     |
| `service_retry_maxAttempts` / `service_retry_backoff_delay`                                                                              | retry attempts and backoff interval (ms) when reaching a dependent service                                                    |
| `event_enabled`                                                                                                                          | emit events on ADD/UPDATE/DELETE/READ                                                                                         |
| `event_topic`                                                                                                                            | Kafka topic events are emitted to                                                                                             |
| `encryption_enabled`                                                                                                                     | default `false` — encrypt private fields at storage (requires an external encryption service)                                 |
| `encryption_health_check_url` / `encryption_uri` / `encryption_batch_uri` / `decryption_uri` / `decryption_batch_uri`                    | encryption service endpoints                                                                                                  |
| `encryption_tenant_id`                                                                                                                   | tenant id for encryption                                                                                                      |
| `idgen_enabled`                                                                                                                          | enable/disable ID generation                                                                                                  |
| `idgen_tenant_id`                                                                                                                        | tenant id for ID generation                                                                                                   |
| `idgen_health_check_url` / `idgen_generate_url` / `idgen_id_format_url`                                                                  | ID-gen service endpoints                                                                                                      |
| `swagger_enabled`                                                                                                                        | default `true` — enable/disable Swagger                                                                                       |
| `swagger_title` / `swagger_description` / `swagger_version`                                                                              | custom Swagger metadata                                                                                                       |

## Claims Service

| Property        | Description                                                     |
| --------------- | --------------------------------------------------------------- |
| `sunbirdrc_url` | URL (host + port) the claims service uses to reach the registry |

## Certificate Api Service

| Property                 | Description                                                                               |
| ------------------------ | ----------------------------------------------------------------------------------------- |
| `QR_TYPE`                | `W3C-VC`, `URL-W3C-VC` (VC sent as a URL), or `URL` (QR contains only entity name + osid) |
| `CERTIFICATE_DOMAIN_URL` | base URL used when `QR_TYPE` is `URL`                                                     |

## Certificate Signer Service

| Property             | Description                                               |
| -------------------- | --------------------------------------------------------- |
| `CACHE_CONTEXT_URLS` | context URLs to pre-cache, avoiding runtime network calls |
| `CONFIG_BASE_PATH`   | path to the `config.json` holding the signing keys        |

## Notification Service

| Property                  | Description                                  |
| ------------------------- | -------------------------------------------- |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers (`host:port`)        |
| `SMS_AUTH_KEY`            | authorization key for the SMS API            |
| `ENABLE_SMS`              | enable sending SMS                           |
| `TRACK_NOTIFICATIONS`     | track sent notifications for later retrieval |

## Metrics Service

<table data-search="false"><thead><tr><th>Property</th><th>Description</th></tr></thead><tbody><tr><td><code>CLICK_HOUSE_URL</code></td><td>Clickhouse URL + port</td></tr><tr><td><code>CLICKHOUSE_DATABASE</code></td><td>database name events are stored in</td></tr><tr><td><code>KAFKA_BOOTSTRAP_SERVERS</code></td><td>Kafka URL + port</td></tr><tr><td><code>KAFKA_METRICS_TOPIC</code></td><td>topic the registry publishes events to</td></tr><tr><td><code>DATABASE_PROVIDER_NAME</code></td><td>e.g. <code>clickhouse</code></td></tr><tr><td><code>REDIS_URL</code></td><td>Redis host</td></tr><tr><td><code>CRON_ENABLE</code></td><td>run the aggregation cron job</td></tr><tr><td><code>SCHEDULE_INTERVAL</code></td><td>days between cron runs</td></tr><tr><td><code>SCHEDULE_TIME</code></td><td>time (GMT) to run the cron job</td></tr></tbody></table>

## Bulk Issuance Service

| Property                                                                                    | Description         |
| ------------------------------------------------------------------------------------------- | ------------------- |
| `REGISTRY_BASE_URL`                                                                         | registry host       |
| `DATABASE_HOST` / `DATABASE_PORT` / `DATABASE_USER` / `DATABASE_PASSWORD` / `DATABASE_NAME` | database connection |
| `KEYCLOAK_PUBLIC_KEY` / `KEYCLOAK_URL` / `KEYCLOAK_REALM`                                   | Keycloak connection |

## Digilocker Certificate API

<table data-search="false"><thead><tr><th>Property</th><th>Description</th></tr></thead><tbody><tr><td><code>DIGILOCKER_HMAC_AUTHKEY</code></td><td>random string used to verify the request HMAC — this is DigiLocker's API key</td></tr><tr><td><code>DIGILOCKER_AUTH_KEYNAME</code></td><td>header name to read the HMAC from (default <code>x-digilocker-hmac</code>)</td></tr><tr><td><code>DIGILOCKER_DOC_ID_PREFIX</code></td><td>document prefix sent in the response, mapping to the correct DigiLocker document (varies per issuer)</td></tr><tr><td><code>KEYCLOAK_TOKEN_URL</code></td><td>Keycloak connection URL</td></tr><tr><td><code>KEYCLOAK_CLIENT_SECRET</code></td><td>secret for the admin client</td></tr><tr><td><code>KEYCLOAK_CLIENT_ID</code></td><td>admin client id</td></tr><tr><td><code>REGISTRY_URL</code></td><td>registry URL</td></tr></tbody></table>

## Encryption Service

Enable via `.env`: `ENCRYPTION_ENABLED=true`

| Property                                      | Description                                                     |
| --------------------------------------------- | --------------------------------------------------------------- |
| `server.port`                                 | port to run on                                                  |
| `server.servlet.context-path`                 | context path                                                    |
| `spring.datasource.url` / `spring.flyway.url` | DB connection, e.g. `jdbc:postgresql://localhost:5432/yourdb`   |
| `spring.flyway.baseline-on-migrate`           | boolean — handle migration versioning                           |
| masterDataProvider                            | `org.egov.enc.masterdata.provider.WebServiceMasterDataProvider` |

## ID Gen Service

Enable via `.env`: `IDGEN_ENABLED=true`. Also see `uniqueIdentifierFields` in [Schema Configuration](/registry/schemas/schema-configuration).

| Property                            | Description                                                    |
| ----------------------------------- | -------------------------------------------------------------- |
| `spring.datasource.url`             | DB connection                                                  |
| `spring.flyway.baseline-on-migrate` | boolean — migration versioning                                 |
| `idformat.from.mdms`                | boolean — fetch id format from MDMS                            |
| masterDataProvider                  | `org.egov.id.masterdata.provider.WebServiceMasterDataProvider` |
