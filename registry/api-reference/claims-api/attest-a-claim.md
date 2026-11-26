---
title: "Attest A Claim"
---

# Attest A Claim

## Attest a particular claim

<mark style="color:green;">`POST`</mark> `/api/v1/{entity-type}/claims/{claimId}/attest`

#### Path Parameters

| Name                                          | Type   | Description                            |
| --------------------------------------------- | ------ | -------------------------------------- |
| entity-type<mark style="color:red;">\*</mark> | String | Type of entity to which claim was sent |
| claimId<mark style="color:red;">\*</mark>     | String | ID of claim that is to be attested     |

#### Headers

| Name                                            | Type   | Description                                                                                |
| ----------------------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| authorization<mark style="color:red;">\*</mark> | String | Set to `Bearer {access-token}`. `access-token` should have a role with name as entity-type |
| content-type<mark style="color:red;">\*</mark>  | String | Set to `application/json`                                                                  |

#### Request Body

| Name | Type   | Description                                               |
| ---- | ------ | --------------------------------------------------------- |
| {    | String | action type can be either `GRANT_CLAIM` or `REJECT_CLAIM` |

### Usage

::: code-group
```shell [cURL]
curl --location --request POST '{registry-url}/api/v1/{entity-type}/claims/a52708f8-c06f-4df7-a078-d567ec769637/attest' \
--header 'Authorization: Bearer {access-token}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "action":"GRANT_CLAIM"
}'
```
```shell [HTTPie]
printf '{
    "action":"GRANT_CLAIM"
}'| http POST '{registry-url}/api/v1/{entity-type}/claims/a52708f8-c06f-4df7-a078-d567ec769637/attest' \
 Authorization:'Bearer {access-token}' \
 Content-Type:'application/json'
```
:::

`{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`
