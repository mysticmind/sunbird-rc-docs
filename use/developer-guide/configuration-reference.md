---
title: "Configuration Reference"
---

# Configuration Reference

The config files behind the frontend, proxy, audit, notification and view-template behavior. For registry-core environment variables, see the [Environment Variable Reference](/use/developer-guide/environment-variable-reference).

::::::: tabs
== Frontend

Edit `config.json` and update the values below for your deployment.

| Key             | Purpose                                                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `keycloak`      | Keycloak config object: `url` (`domainUrl/auth`), `clientId` (`registry-frontend`), `realm` (`sunbird-rc`)                   |
| `baseUrl`       | your API base URL, e.g. `domainUrl/registry/api/v1`                                                                          |
| `domainName`    | your site's domain, e.g. `https://demo-url.xiv.in`                                                                           |
| `schemaUrl`     | swagger API URL, e.g. `domainUrl/registry/api/docs/swagger.json`                                                             |
| `footerText`    | footer label text                                                                                                            |
| `languages`     | language codes for multilingual support — add translation files under `src/assets/i18n/global/` and `src/assets/i18n/local/` |
| `default_theme` | theme color / site logo object                                                                                               |
|
    |                                                                                                                              |

== Proxy

Needed to avoid CORS issues when running locally.

::::: steps
::: step
#### Create the config file

Create a `proxy.conf.json` in the project root if it doesn't exist.
:::

:::: step
#### Add the proxy config for your API endpoints

```json [proxy.conf.json]
{
  "/registry/api/docs": {
    "target": "https://domain_name/",
    "secure": false,
    "changeOrigin": true,
    "logLevel": "debug"
  }
}
```
::::

::: step
#### Start with the proxy

```bash
npm start
# or
ng serve --proxy-config proxy.conf.json
```
:::
:::::

== Audit

Sunbird RC logs schema-level `ADD`/`READ`/`UPDATE`/`DELETE`/`SEARCH` operations. Two logging modes:

| Mode       | Where logs go                                                     | Requires                                                                                                                                                                                                             |
| ---------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FILE`     | Files, with a 30 MB rolling policy                                | —                                                                                                                                                                                                                    |
| `DATABASE` | The configured primary database, and ElasticSearch too if enabled | An audit schema, per [`raw_audit_schema.json`](https://github.com/Sunbird-RC/sunbird-rc-core/blob/main/java/registry/src/main/resources/raw_audit_schema.json), placed in the registry's configured schema directory |

Toggle via `audit_enabled`; see `audit_frame_store`, `audit_suffix`, `audit_suffixSeparator` in the [Environment Variable Reference](broken://pages/NsJ5yoaHhT6KFQfHVTnq).

== Notifications

Sunbird RC can notify an entity's owner on Invite/Create/Modify/Delete/Revoke. Configure notification templates per schema, per operation: `create`, `update`, `invite`, `delete`, `revoke` — each a list, so multiple templates per operation are supported.

Both email (`subject` + `body`) and SMS (`body` only) are supported. Delivery is either:

| Mode                 | How it works                                                                                                               |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Asynchronous (Kafka) | The registry publishes a message to the configured topic; the notification service consumes it and sends the notification. |
| Synchronous (API)    | The registry calls the notification service directly.                                                                      |

The Notification Service itself expects SMS/SMTP gateway config — see its env vars in the [Environment Variable Reference](broken://pages/NsJ5yoaHhT6KFQfHVTnq).

== View Templates

View templates are JSON transformers applied to entity responses at runtime — they can rename/hide fields, evaluate JEXL expressions, and call custom provider functions.

```json [person\_view\_template.json]
{
  "id": "personDefaultView1",
  "subject": "Person",
  "fields": [
    { "name": "firstName", "title": "NAME" },
    { "name": "lastName", "display": true },
    { "name": "nationalIdentifier", "title": "OS number", "display": false },
    { "title": "Name in passport", "function": "#/functionDefinitions/concat($lastName, $firstName)" },
    { "title": "Name as in DL", "function": "#/functionDefinitions/userDefinedConcat($firstName, $lastName)" }
  ],
  "functionDefinitions": [
    { "name": "concat", "result": "arg1 + \", \" + arg2" },
    { "name": "userDefinedConcat", "provider": "dev.sunbirdrc.provider.SampleViewFunctionProvider" }
  ]
}
```

Applied to:

```json
{ "Person": { "nationalIdentifier": "nid823", "firstName": "Ram", "lastName": "Moorthy", "gender": "MALE", "dob": "1990-12-10" } }
```

...produces:

```json
{ "Person": { "NAME": "Ram", "lastName": "Moorthy", "Name in passport": "Moorthy, Ram", "Name as in DL": "Ram : Moorthy" } }
```

Fields default to `"display": true`; set `"display": false` to hide a field while still keeping it available for internal referencing (e.g. `nationalIdentifier` above).

**Applying a template** — to GET APIs (Get An Entity, Get An Entity By Id) via a `viewTemplateId` header:

```bash
curl --location 'localhost:8081/api/v1/StudentWithPassword/1-2ee0c034-0a81-4c7f-a971-058af35911cb' \
  --header 'viewTemplateId: student_view_template.json'
```

...and to search/discovery APIs via the request body:

```json
{ "filters": { }, "viewTemplateId": "student_view_template.json" }
```
:::::::

