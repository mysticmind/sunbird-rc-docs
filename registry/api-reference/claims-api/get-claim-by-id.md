---
title: "Get Claim by ID"
---

# Get Claim by ID

<mark style="color:blue;">`GET`</mark> `/api/v1/{entity-name}/claims/{claimId}`

#### Path Parameters

| Name                                          | Type   | Description                                              |
| --------------------------------------------- | ------ | -------------------------------------------------------- |
| entity-name<mark style="color:red;">\*</mark> | String | Name of the entity to which attestation request was sent |
| claimId<mark style="color:red;">\*</mark>     | String | ID of the claim to be returned                           |

#### Headers

| Name                                           | Type   | Description                                                                                        |
| ---------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------- |
| content-type<mark style="color:red;">\*</mark> | String | Set to `application/json`                                                                          |
| authorization                                  | String | Set to `Bearer {access-token}` if `roles` in schema config is not anonymous else this can be empty |

:::: tabs
== 200: OK

```json
{
    "id": "{claimId}",
    "entity": "{entityName",
    "entityId": "{entityId}",
    "status": "OPEN",
    "attestationId": "{attestationID}",
    "attestationName": "{attestationName}",
    "closed": false        
}
```
::::

### Usage

::: code-group
```shell [cURL]
curl --location --request GET '{registry-url}/api/v1/{entity-name}/claims/{claimId}' \
--header 'Authorization: Bearer {access-token}'
```
```shell [HTTPie]
http GET '{registry-url}/api/v1/{entity-name}/claims/{claimId}' \
 Authorization:'Bearer {access-token}'
```
:::

`{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`
