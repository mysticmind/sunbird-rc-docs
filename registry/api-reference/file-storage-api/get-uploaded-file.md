---
title: "Get Uploaded File"
---

# Get Uploaded File

<mark style="color:var(--vp-c-indigo-1);">`GET`</mark> `/api/v1/{entity-type}/{entity-id}/{property}/documents/{document-id}`

#### Path Parameters

| Name                                          | Type   | Description                                             |
| --------------------------------------------- | ------ | ------------------------------------------------------- |
| entity-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Entity for which file was uploaded                      |
| entity-id<mark style="color:var(--vp-c-red-1);">\*</mark>   | String | Entity ID of corresponding entity                       |
| property<mark style="color:var(--vp-c-red-1);">\*</mark>    | String | any String for eg templates for uploading html template |
| document-id<mark style="color:var(--vp-c-red-1);">\*</mark> | String | ID of document that was uploaded                        |

#### Headers

| Name                                            | Type   | Description                                                                                        |
| ----------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------- |
| content-type<mark style="color:var(--vp-c-red-1);">\*</mark>  | String | Set to `application/octet-stream`                                                                  |
| authorization<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Set to `Bearer {access-token}` if `roles` in schema config is not anonymous else this can be empty |

:::: tabs
== 200: OK Success response of uploaded file

```javascript
{file contents that was uploaded}
```
::::

## Usage

::: code-group
```shell [cURL]
curl --location \
    --request GET '{registry-url}/api/v1/{entity-type/{entity-id}/{property}/documents/{document-id}' \
    --header 'Authorization: Bearer {access-token}'
```
```shell [HTTPie]
http '{registry-url}/api/v1/{entity-type/{entity-id}/{property}/documents/{document-id}' \
 Authorization:'Bearer {access-token}'
```
:::

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`.
