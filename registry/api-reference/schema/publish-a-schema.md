---
title: "Publish A Schema"
---

# Publish A Schema

## Request

## Publish a Schema

<mark style="color:var(--vp-c-brand-1);">`PUT`</mark> `/api/v1/Schema/{id}`

#### Path Parameters

| Name                                 | Type   | Description                              |
| ------------------------------------ | ------ | ---------------------------------------- |
| id<mark style="color:var(--vp-c-red-1);">\*</mark> | String | id of the schema that is to be published |

#### Headers

| Name                                           | Type   | Description                                                        |
| ---------------------------------------------- | ------ | ------------------------------------------------------------------ |
| content-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Set to `application/json`                                          |
| authorization                                  | String | Set to `Bearer {access-token}` . The token should be a admin token |

#### Request Body

| Name                                     | Type | Description |
| ---------------------------------------- | ---- | ----------- |
| status<mark style="color:var(--vp-c-red-1);">\*</mark> |      | PUBLISHED   |

:::: tabs
== 200: OK Success Response of Published Schema

```javascript
{
    "id": "sunbird-rc.registry.update",
    "ver": "1.0",
    "ets": 1669117705369,
    "params": {
        "resmsgid": "",
        "msgid": "2ff44354-bb9a-4dce-93ba-053f97587df6",
        "err": "",
        "status": "SUCCESSFUL",
        "errmsg": ""
    },
    "responseCode": "OK"
}
```
::::

Sample Schema Request Payload

```json
{
  "status": "PUBLISHED"
}
```

### Usage

::: code-group
```shell [cURL]
curl --location --request PUT '{registry-url}/api/v1/Schema/{id}' \
--header 'Authorization: Bearer {access-token}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "status": "PUBLISHED"
}'
```
```shell [HTTPie]
printf '{
  "status": "PUBLISHED"
}'| http  PUT '{registry-url}/api/v1/Schema' \
 Authorization:'Bearer {access-token}' \
 Content-Type:'application/json'
```
:::

`{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`
