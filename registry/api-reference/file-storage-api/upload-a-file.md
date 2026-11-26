---
title: "Upload A File"
---

# Upload A File

<mark style="color:var(--vp-c-green-1);">`POST`</mark> `/api/v1/{entity-type}/{entity-id}/{property}/documents`

#### Path Parameters

| Name                                          | Type   | Description                                         |
| --------------------------------------------- | ------ | --------------------------------------------------- |
| entity-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Entity type for which the template will be uploaded |
| entity-id<mark style="color:var(--vp-c-red-1);">\*</mark>   | String | Entity ID for mentioned Entity Type                 |

#### Headers

| Name                                           | Type   | Description                                                                                        |
| ---------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------- |
| content-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Set to `multipart/form-data`                                                                       |
| authorization                                  | String | Set to `Bearer {access-token}` if `roles` in schema config is not anonymous else this can be empty |

#### Request Body

| Name                                    | Type   | Description                                                                                                              |
| --------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------ |
| files<mark style="color:var(--vp-c-red-1);">\*</mark> | Object | `files` is template-key which can be replaced with your choice. Requires a `html file` to be sent which will be uploaded |

:::: tabs
== 200: OK Success Response of File uploaded

```javascript
{
    "documentLocations": [
        "{url}"
    ],
    "errors": []
}
```
::::

## Usage

::: code-group
```shell [cURL]
curl --location \
    --header 'Authorization: {access-token}' \
    --form 'files=@"{file-path}"'
    --request POST 
    '{registry-url}/api/v1/{entity-type}/{entity-id}/{property}/documents' \
```
```shell [HTTPie]
http --ignore-stdin \
    --form POST \
    '{registry-url}/api/v1/{entity-type}/{entity-id}/{property}/documents' \
 'files'@{file-path} \
 Authorization:'Bearer {access-token}' \
```
:::

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`.
