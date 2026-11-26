---
title: "Revoke a Credential"
description: "To revoke an existing VC (Verifiable Credential) or an entity, we need to make the following HTTP request"
---

# Revoke a Credential

To revoke an existing VC (Verifiable Credential) or an entity, we need to make the following HTTP request

## This revokes an existing  verifiable credential

<mark style="color:var(--vp-c-green-1);">`POST`</mark> `/api/v1/{entity-type}/{id}/revoke`

The API revokes a verifiable credential by updating the signature data attached to it. This is done by updating the *\_osSignedData* field in the corresponding entity table to an *Empty String*. and storing the signedData in the **RevokedCredential** Registry.

#### Path Parameters

| Name                                          | Type   | Description                |
| --------------------------------------------- | ------ | -------------------------- |
| entity-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Type of entity to update   |
| id<mark style="color:var(--vp-c-red-1);">\*</mark>          | String | id of the entity to revoke |

#### Headers

| Name                                           | Type   | Description                                                                                 |
| ---------------------------------------------- | ------ | ------------------------------------------------------------------------------------------- |
| authorization                                  | String | Set to `Bearer {access-token}` if roles in Schema is not anonymous. Else token can be empty |
| content-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Set to `application/json`                                                                   |

#### Request Body

| Name | Type   | Description |
| ---- | ------ | ----------- |
|      | String |             |

:::: tabs
== 200: OK Entity is Succesfully revoked

```json
{
    "id": "sunbird-rc.utils.revoke",
    "ver": "1.0",
    "ets": 1687421017075,
    "params": {
        "resmsgid": "",
        "msgid": "bbd1e0b7-aab4-4e91-988b-c832e9031bef",
        "err": "",
        "status": "SUCCESSFUL",
        "errmsg": ""
    },
    "responseCode": "OK"
}
```

== 401: Unauthorized Issue in the token authentication - unauthorised

== 500: Internal Server Error Credential is already revoked

```json
revoked response: {
    "id": "sunbird-rc.utils.revoke",
    "ver": "1.0",
    "ets": 1687421091703,
    "params": {
        "resmsgid": "",
        "msgid": "70047a46-a0f1-453a-b6cf-c1cfe8e1a544",
        "err": "",
        "status": "UNSUCCESSFUL",
        "errmsg": "Credential is already revoked"
    },
    "responseCode": "OK"
}
```
::::

## Usage

::: code-group
```shell [cURL]
curl --location \
	--request POST \
	--header 'Content-Type: application/json' \
	--header 'Accept: application/json' \
	'{registry-url}/api/v1/{entity-type}/{id}/revoke' \

```
```shell [HTTPie]
http POST \
	'{registry_url}/api/v1/{entity-type}/{id}/revoke' \
	'content-type: application/json' \
	'authorization: Bearer {access-token}'
	
```
:::

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`.
