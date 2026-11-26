---
title: "Get Schema"
---

# Get Schema

## Request

## Fetch a Schema

<mark style="color:var(--vp-c-indigo-1);">`GET`</mark> `/api/v1/Schema/{id}`

#### Path Parameters

| Name                                 | Type   | Description                |
| ------------------------------------ | ------ | -------------------------- |
| id<mark style="color:var(--vp-c-red-1);">\*</mark> | String | ID of Schema to be fetched |

#### Headers

| Name                                           | Type   | Description                                                        |
| ---------------------------------------------- | ------ | ------------------------------------------------------------------ |
| content-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Set to `application/json`                                          |
| authorization                                  | String | Set to `Bearer {access-token}` . The token should be a admin token |

:::: tabs
== 200: OK Success Response

```javascript
{
    "schema": "...",
    "osUpdatedAt": "2022-11-22T10:30:27.602Z",
    "osCreatedAt": "2022-11-22T10:30:27.602Z",
    "osUpdatedBy": "0eaf6099-9591-42bb-ac5a-21bbc2b47493",
    "name": "schema",
    "osCreatedBy": "0eaf6099-9591-42bb-ac5a-21bbc2b47493",
    "osid": "1-1a2f15e7-6c54-40e9-a689-68628a3d69df",
    "osOwner": [
        "0eaf6099-9591-42bb-ac5a-21bbc2b47493"
    ],
    "status": "{schemaStatus}"
}
```
::::

### Usage

::: code-group
```shell [cURL]
curl --location --request GET '{registry-url}/api/v1/Schema/{id}' \
--header 'Authorization: Bearer {access-token}' \
--header 'Content-Type: application/json'
```
```shell [HTTPie]
http  GET '{registry-url}/api/v1/Schema/{id}' \
 Authorization:'Bearer {access-token}' \
 Content-Type:'application/json'
```
:::

`{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`
