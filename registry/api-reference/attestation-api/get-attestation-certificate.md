---
title: "Get Attestation Certificate"
---

# Get Attestation Certificate

## Retrieve Attestation Certificate

<mark style="color:blue;">`GET`</mark> `/api/v1/{entity-type}/{entity-id}/attestation/{attestation-name}/{attestation-id}`

#### Path Parameters

| Name                                               | Type   | Description                                     |
| -------------------------------------------------- | ------ | ----------------------------------------------- |
| entity-name<mark style="color:red;">\*</mark>      | String | Name of Entity for which attestation was raised |
| entity-id<mark style="color:red;">\*</mark>        | String | ID of entity for which attestation was raised   |
| attestation-name<mark style="color:red;">\*</mark> | String | Name of attestation for that entity-type        |
| attestation-id<mark style="color:red;">\*</mark>   | String | ID of the attestation for that record of entity |

#### Headers

| Name                                     | Type   | Description                                                                                         |
| ---------------------------------------- | ------ | --------------------------------------------------------------------------------------------------- |
| accept<mark style="color:red;">\*</mark> | String | Set to `application/pdf, application/json, text/html, image/svg+xml`                                |
| template                                 | String | if `enable_external_templates` is set to true, send in a url which has html template                |
| template-key                             | String | A key pointing to html template which is present in `Schema`                                        |
| access-token                             | String | Set to `Bearer {access-token}` if roles in schema is not anonymous. Else authorization can be empty |

:::: tabs
== 200: OK Successful retrieval of certification

```markup
PDF File
```
::::

### Usage

::: code-group
```shell [cURL]
curl --location --request GET '{registry-url}/api/v1/{entity-type}/{entity-id}/attestation/{attestation-name}/{attestation-id}' \
--header 'Accept: application/pdf' \
--header 'template: {url}' \
--header 'Authorization: Bearer {access-token}'
```
```shell [HTTPie]
http GET '{registry-url}/api/v1/{entity-type}/{entity-id}/attestation/{attestation-name}/{attestation-id}' \
 Accept:'application/pdf' \
 template:'{url}' \
 Authorization:'Bearer {access-token}'
```
:::

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`
