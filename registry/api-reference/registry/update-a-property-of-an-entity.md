---
title: "Update A Property Of An Entity"
description: "To update the property of an existing entity, we need to make the following HTTP request"
---

# Update A Property Of An Entity

To update the property of an existing entity, we need to make the following HTTP request

## Update a property which is already added to entity

<mark style="color:var(--vp-c-brand-1);">`PUT`</mark> `/api/v1/{entity-type}/{id}/{entity-property}/{property-id}`

#### Path Parameters

| Name                                              | Type   | Description                                                                        |
| ------------------------------------------------- | ------ | ---------------------------------------------------------------------------------- |
| entity-type<mark style="color:var(--vp-c-red-1);">\*</mark>     | String | Type of entity to update                                                           |
| id<mark style="color:var(--vp-c-red-1);">\*</mark>              | String | id of the entity to update                                                         |
| entity-property<mark style="color:var(--vp-c-red-1);">\*</mark> | String | entity Property which to be updated in already existing entity                     |
| property-id<mark style="color:var(--vp-c-red-1);">\*</mark>     | String | entity property osid which is to be updated in already existing property in entity |

#### Headers

| Name                                           | Type   | Description                                                                                 |
| ---------------------------------------------- | ------ | ------------------------------------------------------------------------------------------- |
| content-type<mark style="color:var(--vp-c-red-1);">\*</mark> | String | Set to `application/json`                                                                   |
| authorization                                  | String | Set to `Bearer {access-token}` if roles in Schema is not anonymous. Else token can be empty |

:::: tabs
== 200: OK

```json
{
    "id": "sunbird-rc.registry.update",
    "ver": "1.0",
    "ets": 1669113253859,
    "params": {
        "resmsgid": "",
        "msgid": "129c291e-f089-4052-811f-025330c9b239",
        "err": "",
        "status": "SUCCESSFUL",
        "errmsg": ""
    },
    "responseCode": "OK"
}
```
::::

## Usage

::: code-group
```shell [cURL]
curl --location \
	--request 'POST' \
	--header 'content-type: application/json' \
	--header 'authorization: bearer {access-token}' \
	--data-raw '{
		"city": "Surat"
	}' \
	'{registry-url}/api/v1/{entity-type}/{id}/{entity-property}/{property-id}'
```
```shell [HTTPie]
printf '{
		"city": "Surat"
	}' | http POST \
	'/api/v1/{entity-type}/{id}/{entity-property}/{property-id}' \
	'content-type: application/json' \
	'authorization: Bearer {access-token}'
```
:::

> `{registry-url}` is usually <a href="http://localhost:{port}">http://localhost:{port}</a>. The port can be found under the `registry` section in the `docker-compose.yml` file and is usually `8081`.
