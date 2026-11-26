---
title: "Delete A File/ Multiple Files"
---

# Delete A File/ Multiple Files

<mark style="color:red;">`DELETE`</mark> `/api/v1/{entity-type}/{entity-id}/{property}/documents/{document-id}`

#### Path Parameters

| Name                                          | Type   | Description                                                                                                            |
| --------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------- |
| entity-type<mark style="color:red;">\*</mark> | String | Entity type for which the template will be uploaded                                                                    |
| entity-id<mark style="color:red;">\*</mark>   | String | Entity ID for mentioned Entity Type                                                                                    |
| property<mark style="color:red;">\*</mark>    | String | any String for eg templates for uploading html template                                                                |
| document-id                                   | String | ID of document that was uploaded. If this is not provided, entire directory that holds any no of files will be deleted |

#### Headers

| Name          | Type   | Description                                                                                         |
| ------------- | ------ | --------------------------------------------------------------------------------------------------- |
| authorization | String | Set to `Bearer {access-token}` if roles in schema is not anonymous. Else authorization can be empty |

:::: tabs
== 200: OK Success in deleting a/multiple files

```javascript
```
::::

### Usage

::: code-group
```shell [cURL]
curl --location \
    --request DELETE '{registry-url}/api/v1/{entity-type/{entity-id}/{property}/documents/{document-id}' \
    --header 'Authorization: Bearer {access-token}'
```
```shell [HTTPie]
http DELETE '{registry-url}/api/v1/{entity-type/{entity-id}/{property}/documents/{document-id}' \
 Authorization:'Bearer {access-token}'
```
:::

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`.
